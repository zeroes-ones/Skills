#!/usr/bin/env python3
"""check-chain-coherence.py — advisory report: do chain edges and declared artifacts agree?

A skill states its handoff relationships in two independent places:

  chain.consumes_from / chain.feeds_into   the 327-node chain graph (validate_chains.py)
  workflow.artifacts.inputs / .outputs     the declared node contract (lint-workflow.py)

Nothing checks that the two agree, so the graph can say "system-architect is upstream of
code-reviewer" while the contracts say the two exchange no artifact at all. This tool reports
that disagreement instead of assuming it away:

  (a) chain x artifact — for a skill declaring both a contract and consumes_from edges, whether
      any upstream's artifacts.outputs intersects this skill's artifacts.inputs.
  (b) manifest x skill — for every node of a workflow manifest, whether its node-level
      `inputs:`/`outputs:` match the bound skill's declared workflow.artifacts. A node bound to
      a skill with no contract is unconstrained (default mode) and is reported, not failed.

Advisory by default: mismatches are printed, the exit code stays 0, so this can run alongside
the corpus before it is coherent. --strict turns the same report into exit 1 for callers that
have adopted it as a gate.

Exit codes: 0 = report produced (clean or advisory), 1 = --strict and at least one mismatch in
the section named by --section.

Usage:
    python3 scripts/check-chain-coherence.py                # workflow/manifests/ (advisory)
    python3 scripts/check-chain-coherence.py --all           # also scan examples/ manifests
    python3 scripts/check-chain-coherence.py --json          # machine-readable report
    python3 scripts/check-chain-coherence.py --strict        # exit 1 on any mismatch
    python3 scripts/check-chain-coherence.py --strict --section manifest   # manifest check only
"""

import argparse
import importlib.util
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from lib import safe_yaml  # noqa: E402

SKILLS_DIR = os.path.join(ROOT, "skills")
MANIFESTS_DIR = os.path.join(ROOT, "workflow", "manifests")
EXAMPLES_DIR = os.path.join(ROOT, "examples")
_SLUG = r"[a-z0-9][a-z0-9-]*"
_FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*$", re.S | re.M)


def _load_module(path, modname):
    """Load a hyphenated sibling script as a module (the idiom used by workflow-runner.py)."""
    spec = importlib.util.spec_from_file_location(modname, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# The manifest is executed by workflow-runner.py, which reads a skill's contract through this
# extractor. Reusing it keeps the report about the contract the engine actually sees.
_LINT_WORKFLOW = _load_module(os.path.join(ROOT, "scripts", "lib", "lint-workflow.py"),
                              "lint_workflow")


def _read(path):
    try:
        return open(path, encoding="utf-8").read()
    except OSError:
        return ""


def _dedent(lines):
    """Strip the common leading indentation of a block's non-blank lines."""
    kept = [ln for ln in lines if ln.strip()]
    if not kept:
        return ""
    ind = min(len(ln) - len(ln.lstrip(" ")) for ln in kept)
    return "\n".join(ln[ind:] if len(ln) >= ind else ln for ln in kept)


def _frontmatter(text):
    m = _FRONT_RE.search(text)
    return m.group(1).splitlines() if m else None


def _chain_lists(text):
    """Read chain.consumes_from / chain.feeds_into as lists of names.

    The full frontmatter is outside the Safe YAML Subset in most of the corpus (four-space
    sequence items under a two-space key), so only the two lists are extracted by a line scan
    and handed to safe_yaml for parsing. Both indentation styles in the corpus are handled:
    items indented under their key, and items at the key's own indentation.
    """
    front = _frontmatter(text)
    if front is None:
        return [], []
    return _list_field(front, "consumes_from"), _list_field(front, "feeds_into")


def _list_field(lines, key):
    pat = re.compile(r"^%s:\s*(.*)$" % re.escape(key))
    for i, raw in enumerate(lines):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        ind = len(raw) - len(raw.lstrip(" "))
        m = pat.match(raw[ind:])
        if not m:
            continue
        inline = m.group(1).strip()
        if inline:
            return _parse_list(inline, key)
        items = []
        for nxt in lines[i + 1:]:
            if not nxt.strip():
                continue
            nind = len(nxt) - len(nxt.lstrip(" "))
            if nind > ind or (nind == ind and nxt[nind:].startswith("- ")):
                items.append(nxt)
                continue
            break
        return _parse_list("\n".join(items), key) if items else []
    return []


def _parse_list(body, key):
    """Parse a list body (inline flow list, or `- item` lines) with safe_yaml."""
    body = body.strip("\n")
    if not body.strip():
        return []
    if body.lstrip().startswith("["):
        text = "%s: %s\n" % (key, body.strip())
    else:
        lines = [ln for ln in body.splitlines() if ln.strip()]
        ind = min(len(ln) - len(ln.lstrip(" ")) for ln in lines)
        text = "%s:\n%s\n" % (key, "\n".join(
            "  " + ln[ind:] for ln in lines))
    try:
        parsed = safe_yaml.parse(text)
    except safe_yaml.SafeYamlError:
        return []
    values = parsed.get(key) if isinstance(parsed, dict) else None
    return _norm_list(values) or []


def _norm_list(value):
    """Normalize a scalar / list into a list of strings, or None when absent."""
    if value is None:
        return None
    if isinstance(value, str):
        return [value.strip()]
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return None


def contract_artifacts(text):
    """Return {'inputs': [...], 'outputs': [...]} for a skill, or None in default mode.

    A key that is absent from the contract stays absent (None) so that "declares no outputs"
    is distinguishable from "declares an empty output list".
    """
    block = _LINT_WORKFLOW.extract_workflow_block(text)
    if not block or not block.strip():
        return None
    try:
        parsed = safe_yaml.parse(_dedent(block.splitlines()))
    except safe_yaml.SafeYamlError:
        return None
    if not isinstance(parsed, dict):
        return None
    artifacts = parsed.get("artifacts")
    if not isinstance(artifacts, dict):
        return {"inputs": None, "outputs": None}
    return {"inputs": _norm_list(artifacts.get("inputs")),
            "outputs": _norm_list(artifacts.get("outputs"))}


def find_all_skills():
    """{directory name: path} for every skills/<domain>/<name>/SKILL.md.

    Keyed by directory name: validate-skills.sh enforces frontmatter name == directory name,
    which is also how validate_chains.py builds its lookup.
    """
    found = {}
    if not os.path.isdir(SKILLS_DIR):
        return found
    for root, _dirs, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            path = os.path.join(root, "SKILL.md")
            found[os.path.basename(root)] = path
    return found


def load_skills():
    skills = {}
    for name, path in find_all_skills().items():
        text = _read(path)
        consumes, feeds = _chain_lists(text)
        skills[name] = {
            "path": os.path.relpath(path, ROOT),
            "consumes_from": consumes,
            "feeds_into": feeds,
            "artifacts": contract_artifacts(text),
        }
    return skills


def check_chain(skills):
    """(a) Does any consumes_from upstream's declared output intersect this skill's input?

    Returns (details, counts). Only edges where both ends declare artifacts can be judged;
    an edge with a contract-less end is counted as skipped, never as a mismatch.
    """
    details = []
    counts = {"edges": 0, "compared": 0, "matched": 0, "disjoint": 0, "skipped": 0}
    for name, rec in sorted(skills.items()):
        art = rec["artifacts"]
        for up in rec["consumes_from"]:
            counts["edges"] += 1
            upstream = skills.get(up)
            if upstream is None:
                # Dangling references are validate_chains.py's report, not this one's.
                counts["skipped"] += 1
                continue
            if not art or not upstream["artifacts"]:
                counts["skipped"] += 1
                continue
            outs = upstream["artifacts"]["outputs"]
            ins = art["inputs"]
            if not outs or not ins:
                counts["skipped"] += 1
                continue
            counts["compared"] += 1
            shared = sorted(set(outs) & set(ins))
            if shared:
                counts["matched"] += 1
            else:
                counts["disjoint"] += 1
            details.append({
                "skill": name,
                "skill_file": rec["path"],
                "upstream": up,
                "upstream_file": upstream["path"],
                "shared": shared,
                "upstream_outputs": outs,
                "skill_inputs": ins,
                "coherent": bool(shared),
            })
    return details, counts


def example_manifests():
    """example/ manifests: any YAML parsing to a dict with a slug name (mirrors
    validate-workflows.py discovery, so both tools consider the same set of graphs)."""
    found = []
    if not os.path.isdir(EXAMPLES_DIR):
        return found
    for root, dirs, files in os.walk(EXAMPLES_DIR):
        dirs[:] = [d for d in dirs if d not in ("tests", "fixtures", "state")]
        for f in sorted(files):
            if not f.endswith((".yaml", ".yml")):
                continue
            path = os.path.join(root, f)
            try:
                data = safe_yaml.parse(_read(path))
            except safe_yaml.SafeYamlError:
                continue
            if isinstance(data, dict) and isinstance(data.get("name"), str) \
                    and re.match(r"^" + _SLUG + r"$", data["name"]):
                found.append(path)
    return sorted(found)


def manifest_paths(include_examples):
    paths = []
    if os.path.isdir(MANIFESTS_DIR):
        paths = [os.path.join(MANIFESTS_DIR, f) for f in sorted(os.listdir(MANIFESTS_DIR))
                 if f.endswith(".yaml")]
    if include_examples:
        paths += example_manifests()
    return paths


def check_manifests(paths, skills):
    """(b) Does every node's inputs/outputs match the bound skill's declared artifacts?"""
    details, unconstrained, unresolved, unreadable = [], [], [], []
    counts = {"manifests": 0, "nodes": 0, "nodes_bound": 0, "nodes_without_contract": 0,
              "nodes_unresolved": 0, "mismatched": 0}
    for path in paths:
        text = _read(path)
        try:
            data = safe_yaml.parse(text)
        except safe_yaml.SafeYamlError as exc:
            unreadable.append({"manifest": os.path.relpath(path, ROOT), "error": str(exc)})
            continue
        if not isinstance(data, dict):
            continue
        counts["manifests"] += 1
        label = os.path.relpath(path, ROOT)
        for node in data.get("nodes") or []:
            if not isinstance(node, dict):
                continue
            counts["nodes"] += 1
            skill = node.get("skill")
            if not skill:
                continue  # gate / supervisor / task nodes bind no skill
            rec = skills.get(skill)
            entry = {"manifest": label, "node": node.get("id"), "skill": skill}
            if rec is None:
                counts["nodes_unresolved"] += 1
                entry["reason"] = "skill does not resolve under skills/"
                unresolved.append(entry)
                continue
            art = rec["artifacts"]
            if art is None:
                counts["nodes_without_contract"] += 1
                entry["node_inputs"] = _norm_list(node.get("inputs")) or []
                entry["node_outputs"] = _norm_list(node.get("outputs")) or []
                entry["reason"] = "skill declares no workflow contract (default mode)"
                unconstrained.append(entry)
                continue
            counts["nodes_bound"] += 1
            node_in = _norm_list(node.get("inputs")) or []
            node_out = _norm_list(node.get("outputs")) or []
            dec_in = art["inputs"] or []
            dec_out = art["outputs"] or []
            missing_in = sorted(set(dec_in) - set(node_in))
            extra_in = sorted(set(node_in) - set(dec_in))
            missing_out = sorted(set(dec_out) - set(node_out))
            extra_out = sorted(set(node_out) - set(dec_out))
            if missing_in or extra_in or missing_out or extra_out:
                counts["mismatched"] += 1
                entry.update({"coherent": False, "node_inputs": node_in,
                              "node_outputs": node_out, "skill_inputs": dec_in,
                              "skill_outputs": dec_out, "missing_inputs": missing_in,
                              "extra_inputs": extra_in, "missing_outputs": missing_out,
                              "extra_outputs": extra_out})
                details.append(entry)
    return details, unconstrained, unresolved, unreadable, counts


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Advisory report on chain-edge / declared-artifact agreement")
    ap.add_argument("--all", action="store_true",
                    help="also scan manifests under examples/ (default: workflow/manifests/)")
    ap.add_argument("--json", action="store_true", help="machine-readable report")
    ap.add_argument("--strict", action="store_true", help="exit 1 on any mismatch")
    ap.add_argument("--section", choices=("chain", "manifest", "all"), default="all",
                    help="which section decides the --strict exit code (default: all). "
                         "--section manifest lets the manifest check gate on its own while "
                         "the corpus-wide chain findings stay advisory.")
    ap.add_argument("--top", type=int, default=15, help="rows per section in text output")
    args = ap.parse_args(argv)

    skills = load_skills()
    chain_details, chain_counts = check_chain(skills)
    m_details, m_unconstrained, m_unresolved, m_unreadable, m_counts = check_manifests(
        manifest_paths(args.all), skills)

    mismatch_edges = [d for d in chain_details if not d["coherent"]]
    compared_skills = {d["skill"] for d in chain_details}
    artifact_skills = sum(1 for r in skills.values() if r["artifacts"])
    total = len(mismatch_edges) + m_counts["mismatched"]
    fail = len(mismatch_edges) if args.section == "chain" else m_counts["mismatched"]
    if args.section == "all":
        fail = total

    if args.json:
        print(json.dumps({
            "skills_scanned": len(skills),
            "skills_with_contract": sum(1 for r in skills.values()
                                        if r["artifacts"] is not None),
            "skills_with_artifacts": artifact_skills,
            "chain_edges_consumes_from": chain_counts["edges"],
            "chain_edges_compared": chain_counts["compared"],
            "chain_edges_matched": chain_counts["matched"],
            "chain_edges_disjoint": chain_counts["disjoint"],
            "chain_edges_skipped": chain_counts["skipped"],
            "chain_skills_compared": len(compared_skills),
            "chain_skills_disjoint": len({d["skill"] for d in mismatch_edges}),
            "chain_details": mismatch_edges,
            "manifests_checked": m_counts["manifests"],
            "manifest_nodes": m_counts["nodes"],
            "manifest_nodes_bound": m_counts["nodes_bound"],
            "manifest_nodes_without_contract": m_counts["nodes_without_contract"],
            "manifest_nodes_unresolved": m_counts["nodes_unresolved"],
            "manifest_mismatches": m_counts["mismatched"],
            "manifest_details": m_details,
            "manifest_unconstrained": m_unconstrained,
            "manifest_unresolved": m_unresolved,
            "manifest_unreadable": m_unreadable,
            "mismatches": total,
            "strict": args.strict,
            "strict_section": args.section,
            "strict_failures": fail,
        }, indent=2))
        return 1 if (args.strict and fail) else 0

    print("=== Chain <-> Artifact Coherence (advisory) ===")
    print(f"skills scanned: {len(skills)}   "
          f"declaring a workflow contract: {sum(1 for r in skills.values() if r['artifacts'] is not None)}"
          f"   with artifacts: {artifact_skills}")
    print()

    print(f"(a) chain x artifact — {chain_counts['edges']} consumes_from edges; "
          f"{chain_counts['compared']} judged (both ends declare artifacts)")
    print(f"    matched: {chain_counts['matched']}   "
          f"disjoint: {chain_counts['disjoint']}   "
          f"skipped (no contract at one end or no names): {chain_counts['skipped']}")
    if chain_details:
        pct = 100.0 * chain_counts["disjoint"] / max(chain_counts["compared"], 1)
        print(f"    disjoint share of judged edges: {pct:.1f}%")
        by_skill = {}
        for d in mismatch_edges:
            by_skill.setdefault(d["skill"], []).append(d)
        if by_skill:
            print()
            print(f"    worst offenders ({min(args.top, len(by_skill))} of "
                  f"{len(by_skill)} skills, by disjoint upstream count):")
            for name, rows in sorted(by_skill.items(), key=lambda x: -len(x[1]))[:args.top]:
                print(f"      {len(rows):>3}  {name:34s} {rows[0]['skill_file']}")
            print()
            print(f"    disjoint edges (first {min(args.top, len(mismatch_edges))} of "
                  f"{len(mismatch_edges)}):")
            for d in mismatch_edges[:args.top]:
                print(f"      - {d['skill']} consumes_from {d['upstream']}: "
                      f"upstream outputs {d['upstream_outputs']} vs inputs {d['skill_inputs']}")
    if not chain_counts["disjoint"]:
        print("    ✓ every judged chain edge shares at least one artifact name")
    print()

    print(f"(b) manifest x skill — {m_counts['manifests']} manifests, {m_counts['nodes']} nodes; "
          f"{m_counts['nodes_bound']} bound to a contract, "
          f"{m_counts['nodes_without_contract']} bound to a contract-less skill, "
          f"{m_counts['nodes_unresolved']} unresolved")
    print(f"    mismatches: {m_counts['mismatched']}")
    for d in m_details:
        print(f"      FAIL {d['manifest']} {d['node']} ({d['skill']})")
        print(f"           node  inputs={d['node_inputs']} outputs={d['node_outputs']}")
        print(f"           skill inputs={d['skill_inputs']} outputs={d['skill_outputs']}")
        bits = []
        if d["missing_inputs"]:
            bits.append("missing inputs: " + ", ".join(d["missing_inputs"]))
        if d["extra_inputs"]:
            bits.append("extra inputs: " + ", ".join(d["extra_inputs"]))
        if d["missing_outputs"]:
            bits.append("missing outputs: " + ", ".join(d["missing_outputs"]))
        if d["extra_outputs"]:
            bits.append("extra outputs: " + ", ".join(d["extra_outputs"]))
        print("           " + "; ".join(bits))
    for d in m_unconstrained:
        print(f"      SKIP {d['manifest']} {d['node']} ({d['skill']}): {d['reason']}; "
              f"node artifacts left as declared (inputs={d['node_inputs']}, "
              f"outputs={d['node_outputs']})")
    for d in m_unresolved:
        print(f"      ERR  {d['manifest']} {d['node']} ({d['skill']}): {d['reason']}")
    for d in m_unreadable:
        print(f"      ERR  {d['manifest']}: {d['error']}")
    if not m_counts["mismatched"]:
        print("    ✓ every node bound to a contract matches that contract")
    print()

    if total:
        print(f"mismatches: {total} (advisory — an advisory run never fails the build)")
        if args.strict:
            print(f"--strict decided on section '{args.section}': {fail} failure(s)")
    else:
        print("✓ no mismatches")
    return 1 if (args.strict and fail) else 0


if __name__ == "__main__":
    sys.exit(main())
