#!/usr/bin/env python3
"""
validate-workflows.py — Workflow manifest + graph-integrity validator (stdlib only).

Validates L1 workflow manifests against workflow/schema/workflow-manifest.schema.yaml
(WORKFLOW-SYSTEM.md Sections 2 and 2.4-2.7). Pure static checks: shape, references,
cycles, loop budgets, parallel write ownership, condition vocabulary, payload registry.

Exit codes: 0 = all checked manifests valid; 1 = at least one error.

Usage:
    python3 scripts/validate-workflows.py --selftest        # run fixture + parser self-tests
    python3 scripts/validate-workflows.py --manifest FILE   # validate one manifest
    python3 scripts/validate-workflows.py --all             # validate workflow/manifests/ + examples
    python3 scripts/validate-workflows.py --json            # machine-readable report
"""

import argparse
import json
import os
import re
import sys
import hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from lib import safe_yaml  # noqa: E402

SKILLS_DIR = os.path.join(ROOT, "skills")
MANIFESTS_DIR = os.path.join(ROOT, "workflow", "manifests")
EXAMPLES_DIR = os.path.join(ROOT, "examples")

NODE_TYPES = ("skill", "gate", "supervisor", "task")
STATUS_WORDS = ("done", "blocked", "needs_review", "skipped", "pass", "fail", "changes_requested")
CANONICAL_PAYLOAD_KEYS = {
    "status", "summary", "artifacts", "decisions", "open_questions",
    "verification_evidence", "context", "budget", "next",
}
_SLUG = r"[a-z0-9][a-z0-9-]*"
_COND_RE = re.compile(
    r"^(?:always"
    r"|" + _SLUG + r"\.status\s*(?:==|!=)\s*(?:done|blocked|needs_review|skipped)"
    r"|" + _SLUG + r"\.status\s+in\s+\([a-z_,\s]+\)"
    r"|" + _SLUG + r"\.verdict\s*(?:==|!=)\s*[A-Za-z0-9_]+"
    r"|loop\.iterations\s*<\s*\d+"
    r")$"
)


def _err(msg):
    return {"error": msg}


def _find_skill_names():
    """Return {frontmatter name: relpath} for every skills/*/*/SKILL.md (stdlib regex parse)."""
    found = {}
    if not os.path.isdir(SKILLS_DIR):
        return found
    for domain in os.listdir(SKILLS_DIR):
        dpath = os.path.join(SKILLS_DIR, domain)
        if not os.path.isdir(dpath):
            continue
        for name_dir in os.listdir(dpath):
            skill_file = os.path.join(dpath, name_dir, "SKILL.md")
            if not os.path.isfile(skill_file):
                continue
            try:
                text = open(skill_file, encoding="utf-8").read()
            except OSError:
                continue
            m = re.search(r"^---\s*\n(.*?)\n---", text, re.S | re.M)
            if not m:
                continue
            nm = re.search(r"(?m)^name:\s*[\"']?([^\"'\n]+)[\"']?\s*$", m.group(1))
            if nm:
                found[nm.group(1).strip()] = os.path.relpath(skill_file, ROOT)
    return found


def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


class WorkflowValidator(object):
    def __init__(self, skills):
        self.skills = skills

    def validate_file(self, path):
        try:
            text = open(path, encoding="utf-8").read()
        except OSError as exc:
            return {"file": path, "valid": False, "errors": [_err("unreadable: %s" % exc)]}
        try:
            data = safe_yaml.parse(text)
        except safe_yaml.SafeYamlError as exc:
            return {"file": path, "valid": False, "errors": [_err("yaml: %s" % exc)]}
        if not isinstance(data, dict):
            return {"file": path, "valid": False, "errors": [_err("manifest must be a mapping")]}
        errors = self._validate(data, path)
        return {
            "file": path,
            "name": data.get("name"),
            "manifest_sha": _sha(text),
            "valid": not errors,
            "errors": errors,
        }

    def validate_data(self, data, label="<manifest>"):
        """Validate an already-parsed manifest dict (used by the library-coverage check)."""
        if not isinstance(data, dict):
            return {"file": label, "valid": False, "errors": [_err("manifest must be a mapping")]}
        errors = self._validate(data, None)
        return {"file": label, "name": data.get("name"),
                "valid": not errors, "errors": errors}

    # ------------------------------------------------------------ validation body
    def _validate(self, data, path):
        errors = []
        self._check_meta(data, path, errors)

        nodes, groups, gates_raw = self._collect_ids(data, errors)
        self._check_edges(data, nodes, errors)
        self._check_loops(data, nodes, errors)
        self._check_parallel(data, nodes, errors)
        self._check_gates(data, nodes, errors)
        self._check_supervisors(data, nodes, errors)
        self._check_cycles(data, nodes, errors)
        self._check_reachability(data, nodes, errors)
        self._check_payloads(data, errors)
        return errors

    def _check_meta(self, data, path, errors):
        name = data.get("name")
        if not isinstance(name, str) or not re.match(r"^" + _SLUG + r"$", name):
            errors.append(_err("meta.name must match [a-z0-9][a-z0-9-]*"))
        if path and os.path.basename(path).endswith(".yaml"):
            fname = os.path.basename(path)
            if name and fname != name + ".yaml":
                errors.append(_err("filename must equal name + .yaml: %s != %s" % (fname, name)))
        version = data.get("version")
        if version is not None and not isinstance(version, str):
            errors.append(_err("meta.version must be a string"))

    def _collect_ids(self, data, errors):
        """Executable node ids = nodes[] entries + gates[] entries (gates are valid edge
        targets and exhaustion destinations). loops[]/parallel[] ids are group ids only."""
        nodes, gates_raw, groups = {}, {}, {}
        seen_nodes = set()
        for n in data.get("nodes") or []:
            if not isinstance(n, dict) or "id" not in n:
                errors.append(_err("nodes[] entries need an 'id'"))
                continue
            nid = n["id"]
            if nid in seen_nodes:
                errors.append(_err("duplicate node id: %s" % nid))
                continue
            seen_nodes.add(nid)
            ntype = n.get("type", "skill")
            if ntype not in NODE_TYPES:
                errors.append(_err("node %s: unknown type %r" % (nid, ntype)))
            elif ntype == "skill":
                if not n.get("skill"):
                    errors.append(_err("node %s: type skill requires 'skill'" % nid))
                elif n.get("skill") not in self.skills:
                    errors.append(_err(
                        "node %s: skill %r does not resolve under skills/" % (nid, n.get("skill"))))
            elif ntype == "supervisor" and not n.get("workers"):
                errors.append(_err("node %s: supervisor requires 'workers'" % nid))
            elif ntype == "gate" and not n.get("kind"):
                errors.append(_err("node %s: gate requires 'kind'" % nid))
            nodes[nid] = n
        for bucket in ("loops", "parallel"):
            for item in data.get(bucket) or []:
                if not isinstance(item, dict) or "id" not in item:
                    errors.append(_err("%s[] entries need an 'id'" % bucket))
                    continue
                groups[item["id"]] = (bucket, item)
        # gates[] are executable nodes: mirror them into the node set for reference checks
        seen_gates = set()
        for g in data.get("gates") or []:
            if not isinstance(g, dict) or "id" not in g:
                errors.append(_err("gates[] entries need an 'id'"))
                continue
            gid = g["id"]
            if gid in seen_gates:
                errors.append(_err("duplicate gate id: %s" % gid))
                continue
            seen_gates.add(gid)
            if gid not in nodes:
                nodes[gid] = {"id": gid, "type": "gate", "kind": g.get("kind"),
                              "requires": g.get("requires"), "pass_when": g.get("pass_when")}
            else:
                errors.append(_err("duplicate id across sections: %s" % gid))
        # uniqueness across all four sections
        all_ids = {}
        for i in list(nodes) + list(groups):
            all_ids.setdefault(i, []).append(i)
        for i, owners in all_ids.items():
            if len(owners) > 1:
                errors.append(_err("duplicate id across sections: %s" % i))
        return nodes, groups, gates_raw

    def _node_ref_ok(self, ref, nodes, errors, ctx):
        if ref not in nodes:
            errors.append(_err("%s references unknown node id %r" % (ctx, ref)))

    def _check_edges(self, data, nodes, errors):
        for e in data.get("edges") or []:
            if not isinstance(e, dict):
                errors.append(_err("edges[] entries must be mappings"))
                continue
            frm, to = e.get("from"), e.get("to")
            for ref, role in ((frm, "edge.from"), (to, "edge.to")):
                if not ref:
                    errors.append(_err("edge missing %s" % role))
                else:
                    self._node_ref_ok(ref, nodes, errors, role)
            cond = e.get("when", "always")
            if not _COND_RE.match(str(cond)):
                errors.append(_err("edge %s->%s: condition outside vocabulary: %r"
                                   % (frm, to, cond)))

    def _check_loops(self, data, nodes, errors):
        for lp in data.get("loops") or []:
            if not isinstance(lp, dict):
                errors.append(_err("loops[] entries must be mappings"))
                continue
            lid = lp.get("id")
            if not lp.get("exit_when"):
                errors.append(_err("loop %s: exit_when is required" % lid))
            elif not _COND_RE.match(str(lp["exit_when"])):
                errors.append(_err("loop %s: exit_when outside vocabulary: %r"
                                   % (lid, lp["exit_when"])))
            mi = lp.get("max_iterations")
            if not isinstance(mi, int) or isinstance(mi, bool) or mi < 1:
                errors.append(_err("loop %s: max_iterations must be an integer >= 1" % lid))
            for ref in lp.get("nodes") or []:
                self._node_ref_ok(ref, nodes, errors, "loop %s.nodes" % lid)
            if lp.get("escalate_to"):
                self._node_ref_ok(lp["escalate_to"], nodes, errors, "loop %s.escalate_to" % lid)
            conv = lp.get("convergence") or {}
            if conv:
                w = conv.get("window")
                if not isinstance(w, int) or w < 1:
                    errors.append(_err("loop %s: convergence.window must be an integer >= 1" % lid))

    def _check_parallel(self, data, nodes, errors):
        for pb in data.get("parallel") or []:
            if not isinstance(pb, dict):
                errors.append(_err("parallel[] entries must be mappings"))
                continue
            pid = pb.get("id")
            members = pb.get("nodes") or []
            if len(members) < 2:
                errors.append(_err("parallel %s: needs >= 2 members" % pid))
            for ref in members:
                self._node_ref_ok(ref, nodes, errors, "parallel %s.nodes" % pid)
            join = pb.get("join", "all")
            if join not in ("all", "majority", "any"):
                errors.append(_err("parallel %s: join must be all|majority|any" % pid))
            # write ownership: member nodes must declare disjoint outputs
            outs = []
            for m in members:
                node = nodes.get(m)
                if node and node.get("outputs"):
                    outs.extend(node["outputs"])
            dup = sorted({o for o in outs if outs.count(o) > 1})
            for o in dup:
                errors.append(_err("parallel %s: conflicting writer for field/artifact %r"
                                   % (pid, o)))

    def _check_gates(self, data, nodes, errors):
        loops = data.get("loops") or []
        for g in data.get("gates") or []:
            if not isinstance(g, dict):
                continue
            gid = g.get("id")
            if g.get("type") != "gate":
                errors.append(_err("gate %s: type must be 'gate'" % gid))
            kind = g.get("kind")
            if kind not in ("human", "auto", "agent"):
                errors.append(_err("gate %s: kind must be human|auto|agent" % gid))
            if g.get("pass_when") and not _COND_RE.match(str(g["pass_when"])):
                errors.append(_err("gate %s: pass_when outside vocabulary: %r"
                                   % (gid, g["pass_when"])))
            if kind != "agent":
                continue
            # V10: identify-agent gate contract
            pool = g.get("pool")
            if not isinstance(pool, list) or not pool:
                errors.append(_err("gate %s: kind agent requires a non-empty pool" % gid))
            for p in pool or []:
                self._node_ref_ok(p, nodes, errors, "gate %s.pool" % gid)
            mr = g.get("max_reroutes")
            if not isinstance(mr, int) or isinstance(mr, bool) or mr < 1:
                errors.append(_err("gate %s: kind agent requires max_reroutes >= 1" % gid))
            if not g.get("escalate_to"):
                errors.append(_err("gate %s: kind agent requires a terminal escalate_to" % gid))
            else:
                self._node_ref_ok(g["escalate_to"], nodes, errors,
                                  "gate %s.escalate_to" % gid)
            referencing = [lp for lp in loops if lp.get("escalate_to") == gid]
            if not referencing:
                errors.append(_err("gate %s: kind agent must be referenced by a loop "
                                   "escalate_to" % gid))
            for lp in referencing:
                members = set(lp.get("nodes") or [])
                for p in pool or []:
                    if p not in members:
                        errors.append(_err("gate %s: pool member %r is not a member of "
                                           "referencing loop %s" % (gid, p, lp.get("id"))))

    def _check_supervisors(self, data, nodes, errors):
        for n in data.get("nodes") or []:
            if not isinstance(n, dict) or n.get("type") != "supervisor":
                continue
            nid = n["id"]
            routing = n.get("routing", "parallel")
            if routing not in ("parallel", "sequential", "select"):
                errors.append(_err("supervisor %s: routing must be parallel|sequential|select" % nid))
            if routing == "select" and not n.get("select"):
                errors.append(_err("supervisor %s: routing select requires 'select'" % nid))
            if routing == "select" and n.get("select"):
                self._node_ref_ok(n["select"], nodes, errors, "supervisor %s.select" % nid)
            for w in n.get("workers") or []:
                self._node_ref_ok(w, nodes, errors, "supervisor %s.workers" % nid)
            if n.get("escalate_to"):
                self._node_ref_ok(n["escalate_to"], nodes, errors, "supervisor %s.escalate_to" % nid)

    def _loop_members(self, data):
        members = set()
        for lp in data.get("loops") or []:
            if isinstance(lp, dict):
                members.update(lp.get("nodes") or [])
        return members

    def _check_cycles(self, data, nodes, errors):
        loop_members = self._loop_members(data)
        adj = {}
        for e in data.get("edges") or []:
            if not isinstance(e, dict):
                continue
            adj.setdefault(e.get("from"), []).append(e.get("to"))
        seen = set()
        stack = []
        path = []

        def dfs(nid):
            if nid in stack:
                cycle = path[path.index(nid):] + [nid]
                if set(cycle[:-1]) <= loop_members:
                    return  # allowed: inside a declared loop
                errors.append(_err("undeclared cycle: %s" % " -> ".join(cycle)))
                return
            if nid in seen:
                return
            seen.add(nid)
            stack.append(nid)
            path.append(nid)
            for nxt in adj.get(nid, []):
                if nxt in nodes or nxt in stack:
                    dfs(nxt)
            stack.pop()
            path.pop()

        for nid in nodes:
            dfs(nid)

    def _check_reachability(self, data, nodes, errors):
        start = data.get("start")
        ends = data.get("end") or []
        if start and start not in nodes:
            errors.append(_err("start references unknown node %r" % start))
        if not data.get("nodes"):
            return
        if start is None:
            # default: node with no incoming edge
            incoming = {e.get("to") for e in data.get("edges") or [] if isinstance(e, dict)}
            starts = [nid for nid in nodes if nid not in incoming]
            if len(starts) != 1:
                errors.append(_err("no explicit start and %d candidate entry nodes; set 'start'"
                                   % len(starts)))
                return
            start = starts[0]
        adj = {}
        for e in data.get("edges") or []:
            if isinstance(e, dict):
                adj.setdefault(e.get("from"), []).append(e.get("to"))
        loop_members = self._loop_members(data)
        # Escalation arcs are reachability arcs at runtime: a loop reaches its escalate_to
        # target (kind: agent gates), and an agent gate reaches its terminal escalate_to.
        loop_escalate = {}
        for lp in data.get("loops") or []:
            if isinstance(lp, dict) and lp.get("escalate_to"):
                for nid in lp.get("nodes") or []:
                    loop_escalate[nid] = lp["escalate_to"]
        gate_escalate = {g["id"]: g["escalate_to"] for g in data.get("gates") or []
                         if isinstance(g, dict) and g.get("kind") == "agent"
                         and g.get("escalate_to")}
        reachable = set()
        frontier = [start]
        while frontier:
            cur = frontier.pop()
            if cur in reachable:
                continue
            reachable.add(cur)
            if cur in loop_members:
                frontier.extend(loop_members)  # loop members iterate among themselves
                if cur in loop_escalate:
                    frontier.append(loop_escalate[cur])
            if cur in gate_escalate:
                frontier.append(gate_escalate[cur])
            for nxt in adj.get(cur, []):
                if nxt not in reachable:
                    frontier.append(nxt)
        unreachable = [nid for nid in nodes if nid not in reachable]
        if unreachable:
            errors.append(_err("nodes not reachable from start: %s" % ", ".join(sorted(unreachable))))
        if ends:
            for ref in ends:
                self._node_ref_ok(ref, nodes, errors, "end")

    def _check_payloads(self, data, errors):
        declared = data.get("payloads") or {}
        if declared:
            if not isinstance(declared, dict):
                errors.append(_err("payloads must be a mapping of name -> key list"))
                declared = {}
            for pname, keys in declared.items():
                if not isinstance(keys, list):
                    errors.append(_err("payload %s: keys must be a list" % pname))
                    continue
                bad = [k for k in keys if k not in CANONICAL_PAYLOAD_KEYS]
                if bad:
                    errors.append(_err("payload %s: keys outside registry: %s"
                                       % (pname, ", ".join(bad))))
        for e in data.get("edges") or []:
            if isinstance(e, dict) and e.get("payload"):
                if declared and e["payload"] not in declared:
                    errors.append(_err("edge payload %r not declared in payloads" % e["payload"]))

def _looks_like_manifest(path):
    """Discovery helper: include examples YAML only when it parses to a dict with a slug name."""
    try:
        text = open(path, encoding="utf-8").read()
        data = safe_yaml.parse(text)
    except Exception:
        return False
    return isinstance(data, dict) and isinstance(data.get("name"), str) \
        and re.match(r"^" + _SLUG + r"$", data["name"])


def _discover_manifests():
    found = []
    if os.path.isdir(MANIFESTS_DIR):
        for f in sorted(os.listdir(MANIFESTS_DIR)):
            if f.endswith(".yaml"):
                found.append(os.path.join(MANIFESTS_DIR, f))
    if os.path.isdir(EXAMPLES_DIR):
        for root, dirs, files in os.walk(EXAMPLES_DIR):
            dirs[:] = [d for d in dirs if d not in ("tests", "fixtures", "state")]
            for f in sorted(files):
                if f.endswith((".yaml", ".yml")) and _looks_like_manifest(
                        os.path.join(root, f)):
                    found.append(os.path.join(root, f))
    return sorted(found)


def _count_eligibility():
    """Library readiness counters mirroring audit-library.py: eligible = Core Workflow + a
    Verification heading (default-mode node), declared = frontmatter carries a workflow: block."""
    eligible = declared = 0
    if not os.path.isdir(SKILLS_DIR):
        return eligible, declared
    for domain in os.listdir(SKILLS_DIR):
        dpath = os.path.join(SKILLS_DIR, domain)
        if not os.path.isdir(dpath):
            continue
        for name_dir in os.listdir(dpath):
            path = os.path.join(dpath, name_dir, "SKILL.md")
            if not os.path.isfile(path):
                continue
            try:
                text = open(path, encoding="utf-8").read()
            except OSError:
                continue
            fm = re.search(r"^---\s*\n(.*?)\n---", text, re.S | re.M)
            if fm and re.search(r"(?m)^workflow:\s*$", fm.group(1)):
                declared += 1
            if re.search(r"^#+\s+Core Workflow", text, re.M) and \
                    re.search(r"^#+\s+Verification", text, re.M):
                eligible += 1
    return eligible, declared


def _coverage():
    """Prove library-wide graph capability: synthesize a one-node manifest for every skill name
    and validate it. A skill that cannot be a node fails the check."""
    skills = _find_skill_names()
    validator = WorkflowValidator(skills)
    failures = []
    for name in sorted(skills):
        manifest = {"name": "coverage-" + name, "version": "1.0.0",
                    "description": "coverage probe",
                    "nodes": [{"id": "node0", "skill": name}]}
        report = validator.validate_data(manifest, label="skill:" + name)
        if not report["valid"]:
            failures.append((name, [e["error"] for e in report["errors"]]))
    eligible, declared = _count_eligibility()
    print("coverage: %d distinct skill names; %d resolve as workflow nodes"
          % (len(skills), len(skills) - len(failures)))
    for name, errs in failures:
        print("  FAIL %s: %s" % (name, "; ".join(errs)))
    print("readiness: %d eligible (default-mode nodes), %d declared workflow: blocks"
          % (eligible, declared))
    return 1 if failures else 0


def _selftest():
    """Parser + validator self-tests incl. fixtures under workflow/tests/fixtures."""
    results = []
    fixtures = os.path.join(ROOT, "workflow", "tests", "fixtures")
    validator = WorkflowValidator(_find_skill_names())
    # --- parser basics
    parsed = safe_yaml.parse("a: 1\nb: true\nc: hello world\nd:\n  - x\n  - y\n")
    ok = parsed == {"a": 1, "b": True, "c": "hello world", "d": ["x", "y"]}
    results.append(("parser: scalars + nested list", ok))
    parsed_flow = safe_yaml.parse("outs: [a, b, c]\n")
    results.append(("parser: scalar-only flow list",
                    parsed_flow == {"outs": ["a", "b", "c"]}))
    parsed2 = safe_yaml.parse(
        "nodes:\n  - id: spec\n    skill: idea-to-spec\n    outputs:\n      - spec\n")
    ok2 = parsed2 == {"nodes": [{"id": "spec", "skill": "idea-to-spec", "outputs": ["spec"]}]}
    results.append(("parser: list of maps", ok2))
    for bad_text, why in (
        ("a:\n\t- x\n", "tabs"), ("a: |\n  x\n", "block scalar"),
        ("a: 1\na: 2\n", "duplicate key")):
        try:
            safe_yaml.parse(bad_text)
            results.append(("parser rejects %s" % why, False))
        except safe_yaml.SafeYamlError:
            results.append(("parser rejects %s" % why, True))
    # --- fixtures: valid-*.yaml must pass; invalid-*.yaml must fail
    if os.path.isdir(fixtures):
        for f in sorted(os.listdir(fixtures)):
            fpath = os.path.join(fixtures, f)
            report = validator.validate_file(fpath)
            expect_valid = f.startswith("valid-")
            got_valid = report["valid"]
            results.append(("fixture %s (expect valid=%s)" % (f, expect_valid),
                            got_valid == expect_valid))
            if not got_valid and not expect_valid:
                # require at least one specific error on invalid fixtures
                results.append(("fixture %s produced errors" % f, bool(report["errors"])))
    failed = [name for name, ok in results if not ok]
    for name, ok in results:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    print("selftest: %d checks, %d failed" % (len(results), len(failed)))
    return 1 if failed else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate L1 workflow manifests")
    ap.add_argument("--manifest", action="append", default=[], help="manifest file to validate")
    ap.add_argument("--all", action="store_true", help="validate workflow/manifests/ + examples/")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--coverage", action="store_true",
                    help="prove every library skill resolves as a workflow node")
    ap.add_argument("--selftest", action="store_true", help="run parser + fixture self-tests")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()
    if args.coverage:
        return _coverage()

    skills = _find_skill_names()
    validator = WorkflowValidator(skills)
    targets = list(args.manifest)
    if args.all or not targets:
        targets += _discover_manifests()
    if not targets:
        print("no manifests found to validate")
        return 0
    reports = [validator.validate_file(t) for t in targets]
    if args.json:
        print(json.dumps(reports, indent=2))
    else:
        for r in reports:
            mark = "OK  " if r["valid"] else "FAIL"
            print("%s %s" % (mark, r["file"]))
            for e in r["errors"]:
                print("     - %s" % e["error"])
    return 0 if all(r["valid"] for r in reports) else 1


if __name__ == "__main__":
    sys.exit(main())
