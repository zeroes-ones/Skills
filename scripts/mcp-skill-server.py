#!/usr/bin/env python3
"""mcp-skill-server.py — expose this skill library to any MCP client (stdlib only, no dependencies).

WHY THIS EXISTS
---------------
The library is normally consumed by symlinking `skills/` into an agent's discovery directory, or by
an agent reading SKILL.md files off disk. Both work, but neither gives a client the *engine* — the
graph, the declared contracts, the validator, or the ability to actually run a workflow. This server
speaks the Model Context Protocol over stdio so any MCP-capable client (Claude Code, Cursor, Cline,
and others) can query and drive the whole thing with no install step and no Node/npm dependency.

DESIGN
------
- **Zero dependencies.** Python stdlib only. The protocol surface needed here (initialize,
  tools/list, tools/call, ping) is newline-delimited JSON-RPC 2.0, which is small enough to
  implement directly and test end to end. This keeps the library's documented "no Node, no npm in
  the core" invariant intact. If you later want the official SDK, the tool layer below is
  transport-independent and reusable.
- **Reuses the repo's own machinery, never re-implements it.** Skill discovery comes from
  `validate-workflows._find_skill_names`, YAML parsing from `lib/safe_yaml`, contract extraction from
  `lib/lint-workflow.extract_workflow_block`, manifest validation from `WorkflowValidator`, and
  workflow execution from `workflow-runner.py`. There is exactly one source of truth per concern.
- **stdout is protocol-only.** Every diagnostic goes to stderr; a stray print on stdout would
  corrupt the stream.

SECURITY POSTURE
----------------
- `run_workflow` executes a manifest with the **deterministic stub executor** — no LLM call, no
  agent, no shell. It exercises control flow (loops, budgets, gates, contracts) and returns the
  summary. It cannot execute node content.
- Manifest paths are confined to the repository root; anything resolving outside is rejected.
- The server reads files under the repository only. It performs no network access.

Usage:
    python3 scripts/mcp-skill-server.py                 # serve MCP over stdio
    python3 scripts/mcp-skill-server.py --selftest       # in-process protocol + tool checks
    python3 scripts/mcp-skill-server.py --list-tools     # human-readable tool catalogue

Client config (project scope): see .mcp.json at the repository root.
"""

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
SKILLS = os.path.join(ROOT, "skills")
sys.path.insert(0, SCRIPTS)

SERVER_NAME = "zeroes-ones-skills"
SERVER_VERSION = "1.0.0"
DEFAULT_PROTOCOL = "2024-11-05"
KNOWN_PROTOCOLS = ("2024-11-05", "2025-03-26", "2025-06-18")

sys.path.insert(0, os.path.join(SCRIPTS, "lib"))
from lib import safe_yaml  # noqa: E402


def _load_module(path, modname):
    spec = importlib.util.spec_from_file_location(modname, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_VALIDATOR = _load_module(os.path.join(SCRIPTS, "validate-workflows.py"), "validate_workflows")
_LINT_WORKFLOW = _load_module(os.path.join(SCRIPTS, "lib", "lint-workflow.py"), "lint_workflow")


# ---------------------------------------------------------------- library index
class Library(object):
    """Read-only view over the skill corpus. Built once, reused for every tool call."""

    def __init__(self, root=ROOT):
        self.root = root
        self.skills_dir = os.path.join(root, "skills")
        self._index = None

    def _build(self):
        index = {}
        find = _VALIDATOR._find_skill_names()  # noqa: SLF001 - same-repo tool reuse
        for name, rel in find.items():
            path = os.path.join(self.root, rel)
            try:
                text = open(path, encoding="utf-8").read()
            except OSError:
                continue
            front = self._raw_frontmatter(text) or ""
            parts = rel.split(os.sep)
            index[name] = {
                "name": name,
                "path": rel,
                "abs": path,
                "domain": parts[1] if len(parts) > 2 else "",
                "dir": parts[2] if len(parts) > 2 else "",
                "description": self._scalar(text, "description"),
                "declared": bool(re.search(r"(?m)^workflow:\s*$", front)),
                "has_core_workflow": bool(re.search(r"(?m)^#+\s+Core Workflow", text)),
                "has_verification": bool(re.search(r"(?m)^#+\s+Verification", text)),
            }
        return index

    @staticmethod
    def _raw_frontmatter(text):
        m = re.match(r"^---\s*\n(.*?)\n---\s*$", text, re.S | re.M)
        return m.group(1) if m else None

    @staticmethod
    def _chain(text):
        """Extract the `consumes_from` / `feeds_into` lists from the chain block, positionally.

        The repository's Safe YAML Subset parser cannot read this block: it contains folded block
        scalars (`description: >` elsewhere in the frontmatter), and `chain.examples` entries are
        written with their list items at the *same* indentation as the key (`examples:` then
        `- path`), which the subset grammar rejects. A silent parse failure here is expensive — it
        reported 638 edges instead of 1,932 — so the two lists this server needs are read from
        their `- ` lines directly and no YAML is involved.
        """
        raw = Library._raw_frontmatter(text)
        if raw is None:
            return {}
        lines = raw.splitlines()
        out, i = {}, 0
        while i < len(lines):
            m = re.match(r"^(\s*)(consumes_from|feeds_into):\s*(.*)$", lines[i])
            if not m:
                i += 1
                continue
            key, indent, inline = m.group(2), len(m.group(1)), m.group(3).strip()
            items = []
            if inline.startswith("["):
                items = [x.strip().strip("'\"") for x in inline.strip("[]").split(",") if x.strip()]
                i += 1
            else:
                j = i + 1
                while j < len(lines):
                    line = lines[j]
                    if not line.strip() or line.lstrip().startswith("#"):
                        j += 1
                        continue
                    ind = len(line) - len(line.lstrip(" "))
                    if ind < indent:
                        break  # left the block
                    if ind == indent and not line.lstrip().startswith("-"):
                        break  # sibling key (e.g. feeds_into:)
                    item = re.match(r"^\s*-\s+(.+?)\s*$", line)
                    if item:
                        items.append(item.group(1).strip().strip("'\""))
                    j += 1
                i = j
            out[key] = items
        return out

    @staticmethod
    def _scalar(text, key):
        """Value of a scalar or folded-block frontmatter key, without a full YAML parse."""
        raw = Library._raw_frontmatter(text)
        if raw is None:
            return ""
        lines = raw.splitlines()
        for i, line in enumerate(lines):
            m = re.match(r"^%s:\s*(.*)$" % re.escape(key), line)
            if not m:
                continue
            inline = m.group(1).strip()
            if inline in (">", "|", ">-", "|-"):
                buf = []
                for cont in lines[i + 1:]:
                    if cont.strip() == "":
                        continue
                    if len(cont) - len(cont.lstrip(" ")) == 0:
                        break
                    buf.append(cont.strip())
                return " ".join(buf)
            return inline.strip("'\"")
        return ""

    @property
    def index(self):
        if self._index is None:
            self._index = self._build()
        return self._index

    def skill(self, name):
        return self.index.get(name)

    def read(self, name):
        entry = self.skill(name)
        if not entry:
            return None
        try:
            return open(entry["abs"], encoding="utf-8").read()
        except OSError:
            return None

    def contract(self, name):
        text = self.read(name)
        if text is None:
            return None
        block = _LINT_WORKFLOW.extract_workflow_block(text)
        if not block or not block.strip():
            return {}
        lines = [ln for ln in block.splitlines() if ln.strip()]
        indent = min(len(ln) - len(ln.lstrip(" ")) for ln in lines) if lines else 0
        dedented = "\n".join(ln[indent:] if len(ln) >= indent else ln for ln in lines)
        try:
            parsed = safe_yaml.parse(dedented)
        except Exception:  # noqa: BLE001
            return {}
        return parsed if isinstance(parsed, dict) else {}

    def graph(self):
        """Directed/undirected edge counts and hub ranking, from chain: frontmatter.

        Degrees count *distinct* neighbours (in plus out), matching the semantics of
        scripts/emit-skill-graph.py so the two never disagree.
        """
        directed, pairs, degree = 0, set(), {}
        for name, entry in self.index.items():
            chain = self._chain(self.read(name) or "")
            incoming = [str(t) for t in (chain.get("consumes_from") or []) if t]
            outgoing = [str(t) for t in (chain.get("feeds_into") or []) if t]
            neighbours = set(incoming) | set(outgoing)
            if neighbours:
                degree[name] = len(neighbours)
            for t in outgoing:
                directed += 1
                pairs.add(tuple(sorted((name, t))))
        hubs = sorted(degree.items(), key=lambda kv: (-kv[1], kv[0]))[:8]
        return {
            "skills": len(self.index),
            "domains": len({e["domain"] for e in self.index.values() if e["domain"]}),
            "directed_edges": directed,
            "undirected_edges": len(pairs),
            "declared_contracts": sum(1 for e in self.index.values() if e["declared"]),
            "eligible_default_mode": sum(
                1 for e in self.index.values() if e["has_core_workflow"] and e["has_verification"]),
            "top_hubs": [{"skill": n, "edges": c} for n, c in hubs],
        }

    def search(self, query, limit=10):
        terms = [t for t in re.split(r"[^a-z0-9]+", (query or "").lower()) if t]
        if not terms:
            return []
        scored = []
        for name, entry in self.index.items():
            hay_name = name.lower().replace("-", " ")
            hay_desc = (entry["description"] or "").lower()
            score = 0
            for t in terms:
                if t in hay_name:
                    score += 10
                score += 3 * hay_desc.count(t)
            if score:
                scored.append((score, name, entry))
        scored.sort(key=lambda x: (-x[0], x[1]))
        return [
            {"skill": n, "domain": e["domain"], "declared": e["declared"],
             "description": _trim(e["description"], 240)}
            for _s, n, e in scored[:max(1, min(limit, 50))]
        ]

    def workflows(self):
        out = []
        for base in (os.path.join(self.root, "workflow", "manifests"),
                     os.path.join(self.root, "examples")):
            if not os.path.isdir(base):
                continue
            for dirpath, _dirs, files in os.walk(base):
                for f in sorted(files):
                    if not f.endswith(".yaml"):
                        continue
                    path = os.path.join(dirpath, f)
                    rel = os.path.relpath(path, self.root)
                    try:
                        manifest = safe_yaml.parse(open(path, encoding="utf-8").read())
                    except Exception:  # noqa: BLE001 - unparseable manifests are listed as invalid
                        out.append({"manifest": rel, "valid": False})
                        continue
                    if not isinstance(manifest, dict) or "nodes" not in manifest:
                        continue  # not a workflow manifest (e.g. a fixture or schema)
                    out.append({
                        "manifest": rel,
                        "name": manifest.get("name"),
                        "description": _trim(manifest.get("description", ""), 200),
                        "nodes": len(manifest.get("nodes") or []),
                        "loops": len(manifest.get("loops") or []),
                        "gates": len(manifest.get("gates") or []),
                    })
        return out

    def validate(self, path):
        abs_path = self._resolve(path)
        if abs_path is None:
            return {"valid": False, "errors": [{"error": "path is outside the repository: %s" % path}]}
        if not os.path.isfile(abs_path):
            return {"valid": False, "errors": [{"error": "no such file: %s" % path}]}
        validator = _VALIDATOR.WorkflowValidator(_VALIDATOR._find_skill_names())
        return validator.validate_file(abs_path)

    def _resolve(self, path):
        """Resolve a manifest path, confined to the repository root."""
        if not path:
            return None
        candidate = path if os.path.isabs(path) else os.path.join(self.root, path)
        real = os.path.realpath(candidate)
        if not real.startswith(os.path.realpath(self.root) + os.sep):
            return None
        if not real.endswith((".yaml", ".yml")):
            return None
        return real

    def run(self, path, max_steps=None, enforce_contracts=False, timeout=120):
        """Run a manifest with the deterministic stub executor and return the summary.

        Node content is a stub: this exercises control flow only and never calls an agent.
        """
        abs_path = self._resolve(path)
        if abs_path is None:
            return {"error": "manifest path must be inside the repository and end in .yaml"}
        args = [sys.executable, os.path.join(SCRIPTS, "workflow-runner.py"),
                "--manifest", abs_path]
        if max_steps:
            args += ["--max-steps", str(int(max_steps))]
        if enforce_contracts:
            args += ["--enforce-contracts"]
        try:
            proc = subprocess.run(args, cwd=self.root, capture_output=True, text=True,
                                  timeout=timeout)
        except subprocess.TimeoutExpired:
            return {"error": "run timed out after %ss" % timeout}
        out = (proc.stdout or "").strip()
        try:
            summary = json.loads(out)
        except ValueError:
            return {"error": "runner produced no parseable summary",
                    "stderr": _trim(proc.stderr or "", 600)}
        summary["note"] = ("executed with the deterministic stub executor: control flow only, "
                           "no agent and no node content")
        summary["exit_code"] = proc.returncode
        return summary


def _trim(text, n):
    text = " ".join((text or "").split())
    return text if len(text) <= n else text[: n - 1] + "\u2026"


# ---------------------------------------------------------------- tool catalogue
def tool_specs():
    return [
        {
            "name": "list_skills",
            "description": "List the skills in this library, optionally filtered by domain. Returns name, domain, whether the skill declares a workflow: contract, and a short description.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "Filter to one domain directory, e.g. '05-development' or 'devops'."},
                    "declared_only": {"type": "boolean", "description": "Only skills that declare a workflow: contract.", "default": False},
                    "limit": {"type": "integer", "description": "Maximum results.", "default": 100},
                },
            },
        },
        {
            "name": "get_skill",
            "description": "Fetch the complete SKILL.md playbook for one skill by name — the same content the workflow engine injects into a node prompt.",
            "inputSchema": {
                "type": "object",
                "properties": {"name": {"type": "string", "description": "Skill name as it appears in frontmatter, e.g. 'code-reviewer'."}},
                "required": ["name"],
            },
        },
        {
            "name": "get_skill_contract",
            "description": "Return a skill's optional workflow: contract — typed artifacts, the checklist for 'done', whether evidence is required, and where it escalates. Explains default mode when no contract is declared.",
            "inputSchema": {
                "type": "object",
                "properties": {"name": {"type": "string", "description": "Skill name."}},
                "required": ["name"],
            },
        },
        {
            "name": "search_skills",
            "description": "Lexical search over skill names and descriptions. Use this to find the right skill for a task.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search terms, e.g. 'database migration rollback'."},
                    "limit": {"type": "integer", "default": 10},
                },
                "required": ["query"],
            },
        },
        {
            "name": "get_skill_graph",
            "description": "The skill dependency graph. With a skill name: that skill's upstream and downstream neighbours. Without: library totals (skills, domains, edges, declared contracts) and the most connected hub skills.",
            "inputSchema": {
                "type": "object",
                "properties": {"name": {"type": "string", "description": "Optional skill name for a local neighbourhood."}},
            },
        },
        {
            "name": "list_workflows",
            "description": "List the executable workflow manifests in this repository with their node, loop and gate counts.",
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "validate_manifest",
            "description": "Validate a workflow manifest: structure, cycle rejection, loop budgets, payload registry and reachability. Returns the validator's verdict and any errors.",
            "inputSchema": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Manifest path relative to the repository root, e.g. 'workflow/manifests/senior-dev-loop.yaml'."}},
                "required": ["path"],
            },
        },
        {
            "name": "run_workflow",
            "description": "Execute a workflow manifest with the DETERMINISTIC STUB executor and return the run summary (outcome, steps used, per-node verdicts, handoff). Control flow only — no agent, no node content. Use --enforce-contracts semantics via the flag to see declared criteria asserted.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Manifest path relative to the repository root."},
                    "max_steps": {"type": "integer", "description": "Override the global step budget."},
                    "enforce_contracts": {"type": "boolean", "default": False, "description": "Assert each node's declared completion contract (evidence + criteria coverage)."},
                },
                "required": ["path"],
            },
        },
    ]


def _text(payload, is_error=False):
    body = payload if isinstance(payload, str) else json.dumps(payload, indent=2, sort_keys=True)
    return {"content": [{"type": "text", "text": body}], "isError": bool(is_error)}


def call_tool(lib, name, args):
    """Dispatch one tools/call. Returns an MCP result dict."""
    args = args or {}
    if name == "list_skills":
        rows = []
        for entry in lib.index.values():
            if args.get("domain"):
                needle = str(args["domain"]).lower()
                if needle not in entry["domain"].lower() and needle not in entry["dir"].lower():
                    continue
            if args.get("declared_only") and not entry["declared"]:
                continue
            rows.append({"skill": entry["name"], "domain": entry["domain"],
                         "declared": entry["declared"],
                         "description": _trim(entry["description"], 200)})
        rows.sort(key=lambda r: (r["domain"], r["skill"]))
        limit = int(args.get("limit") or 100)
        shown = rows[:max(1, min(limit, 500))]
        return _text({"total": len(rows), "shown": len(shown), "skills": shown})

    if name == "get_skill":
        skill = args.get("name")
        text = lib.read(skill)
        if text is None:
            return _text({"error": "unknown skill: %s" % skill}, is_error=True)
        return _text(text)

    if name == "get_skill_contract":
        skill = args.get("name")
        entry = lib.skill(skill)
        if not entry:
            return _text({"error": "unknown skill: %s" % skill}, is_error=True)
        contract = lib.contract(skill)
        if contract:
            return _text({"skill": skill, "declared": True, "mode": "L3 contract",
                          "contract": contract,
                          "enforceable": True,
                          "note": "Asserted by workflow-runner.py --enforce-contracts: evidence "
                                  "required plus coverage of every declared criterion."})
        return _text({
            "skill": skill,
            "declared": False,
            "mode": "default",
            "contract": None,
            "enforceable": False,
            "criteria_source": "the skill's Verification / Production Checklist tables, read at "
                               "execution time",
            "eligible_default_mode": entry["has_core_workflow"] and entry["has_verification"],
            "note": "A contract is optional and additive. Without it the node still runs; its "
                    "completion claim simply cannot be asserted by the engine.",
        })

    if name == "search_skills":
        if not args.get("query"):
            return _text({"error": "query is required"}, is_error=True)
        results = lib.search(args["query"], int(args.get("limit") or 10))
        return _text({"query": args["query"], "count": len(results), "results": results})

    if name == "get_skill_graph":
        if args.get("name"):
            entry = lib.skill(args["name"])
            if not entry:
                return _text({"error": "unknown skill: %s" % args["name"]}, is_error=True)
            chain = lib._chain(lib.read(args["name"]) or "")
            return _text({"skill": args["name"], "domain": entry["domain"],
                          "consumes_from": chain.get("consumes_from") or [],
                          "feeds_into": chain.get("feeds_into") or [],
                          "declared": entry["declared"]})
        return _text(lib.graph())

    if name == "list_workflows":
        rows = lib.workflows()
        return _text({"total": len(rows), "workflows": rows})

    if name == "validate_manifest":
        if not args.get("path"):
            return _text({"error": "path is required"}, is_error=True)
        report = lib.validate(args["path"])
        return _text(report, is_error=not report.get("valid", False))

    if name == "run_workflow":
        if not args.get("path"):
            return _text({"error": "path is required"}, is_error=True)
        summary = lib.run(args["path"], args.get("max_steps"),
                          bool(args.get("enforce_contracts")))
        return _text(summary, is_error=bool(summary.get("error")))

    return _text({"error": "unknown tool: %s" % name}, is_error=True)


# ---------------------------------------------------------------- JSON-RPC / MCP
def handle(lib, message):
    """Handle one JSON-RPC message. Returns a response dict, or None for notifications."""
    if not isinstance(message, dict):
        return _error(None, -32600, "invalid request: not an object")
    msg_id = message.get("id")
    method = message.get("method")
    params = message.get("params") or {}

    if method is None:
        return _error(msg_id, -32600, "invalid request: missing method")
    if msg_id is None:
        return None  # notification — never answered, per JSON-RPC 2.0

    if method == "initialize":
        requested = params.get("protocolVersion")
        version = requested if requested in KNOWN_PROTOCOLS else DEFAULT_PROTOCOL
        return _ok(msg_id, {
            "protocolVersion": version,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            "instructions": ("Skill library + workflow engine. Use search_skills to find a skill, "
                             "get_skill to read one, get_skill_contract for its completion "
                             "criteria, and run_workflow to execute a manifest deterministically."),
        })

    if method == "ping":
        return _ok(msg_id, {})

    if method == "tools/list":
        return _ok(msg_id, {"tools": tool_specs()})

    if method == "tools/call":
        name = params.get("name")
        if not name:
            return _error(msg_id, -32602, "invalid params: 'name' is required")
        try:
            result = call_tool(lib, name, params.get("arguments"))
        except Exception as exc:  # noqa: BLE001 - never crash the server on a tool error
            return _text_error(msg_id, "%s: %s" % (type(exc).__name__, exc))
        return _ok(msg_id, result)

    return _error(msg_id, -32601, "method not found: %s" % method)


def _ok(msg_id, result):
    return {"jsonrpc": "2.0", "id": msg_id, "result": result}


def _error(msg_id, code, message):
    return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}}


def _text_error(msg_id, message):
    return _ok(msg_id, _text({"error": message}, is_error=True))


def serve(lib):
    """Serve MCP over stdio: one JSON object per line in, one per line out."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except ValueError:
            response = _error(None, -32700, "parse error")
        else:
            if isinstance(message, list):
                response = _error(None, -32600, "batch requests are not supported")
            else:
                response = handle(lib, message)
        if response is None:
            continue
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    return 0


# ---------------------------------------------------------------- self-test
def _selftest():
    lib = Library()
    checks = []

    def check(label, ok, detail=""):
        checks.append((label, bool(ok), detail))

    # protocol: initialize
    r = handle(lib, {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                     "params": {"protocolVersion": "2025-06-18"}})
    check("initialize echoes a known protocol version",
          r["result"]["protocolVersion"] == "2025-06-18"
          and r["result"]["capabilities"]["tools"]["listChanged"] is False)
    r = handle(lib, {"jsonrpc": "2.0", "id": 2, "method": "initialize",
                     "params": {"protocolVersion": "bogus"}})
    check("initialize falls back for an unknown protocol version",
          r["result"]["protocolVersion"] == DEFAULT_PROTOCOL)

    # notifications get no response
    check("notification gets no response",
          handle(lib, {"jsonrpc": "2.0", "method": "notifications/initialized"}) is None)

    # ping + unknown method
    check("ping responds", "result" in handle(lib, {"id": 3, "method": "ping"}))
    r = handle(lib, {"id": 4, "method": "nope"})
    check("unknown method returns -32601", r["error"]["code"] == -32601)

    # tools/list
    r = handle(lib, {"id": 5, "method": "tools/list"})
    tools = {t["name"] for t in r["result"]["tools"]}
    expected = {"list_skills", "get_skill", "get_skill_contract", "search_skills",
                "get_skill_graph", "list_workflows", "validate_manifest", "run_workflow"}
    check("tools/list advertises every tool and each has an inputSchema",
          tools == expected
          and all("inputSchema" in t and "description" in t for t in r["result"]["tools"]))

    # every tool is callable
    def call(name, args):
        resp = handle(lib, {"id": 9, "method": "tools/call",
                            "params": {"name": name, "arguments": args}})
        res = resp.get("result") or {}
        return res

    res = call("list_skills", {"limit": 5})
    check("list_skills returns entries", "skills" in _first_json(res) and len(_first_json(res)["skills"]) <= 5)

    res = call("get_skill", {"name": "code-reviewer"})
    check("get_skill returns the playbook",
          (res.get("content") or [{}])[0].get("text", "").startswith("---"))

    res = call("get_skill_contract", {"name": "code-reviewer"})
    body = _first_json(res)
    check("get_skill_contract reports a declared contract with criteria",
          body.get("declared") is True
          and bool((body.get("contract") or {}).get("completion", {}).get("criteria")))

    res = call("get_skill_contract", {"name": "skill-levels"})
    body = _first_json(res)
    check("get_skill_contract explains default mode for an undeclared skill",
          body.get("declared") is False and body.get("mode") == "default")

    res = call("search_skills", {"query": "database migration", "limit": 5})
    check("search_skills finds migration-architect",
          any(r["skill"] == "migration-architect" for r in _first_json(res)["results"]))

    res = call("get_skill_graph", {})
    g = _first_json(res)
    check("get_skill_graph returns library totals with sane numbers",
          g["skills"] == 304 and g["directed_edges"] > 1000 and len(g["top_hubs"]) == 8)

    res = call("get_skill_graph", {"name": "code-reviewer"})
    check("get_skill_graph neighbourhood has both directions",
          _first_json(res)["consumes_from"] and _first_json(res)["feeds_into"])

    res = call("list_workflows", {})
    workflows = _first_json(res)["workflows"]
    check("list_workflows lists manifests with node counts",
          any(w.get("manifest") == "workflow/manifests/senior-dev-loop.yaml" and w.get("nodes") == 2
              for w in workflows))

    res = call("validate_manifest", {"path": "workflow/manifests/senior-dev-loop.yaml"})
    check("validate_manifest accepts a valid manifest", _first_json(res).get("valid") is True)

    res = call("validate_manifest", {"path": "workflow/tests/fixtures/invalid-ambiguous-start.yaml"})
    check("validate_manifest rejects a known-invalid fixture",
          _first_json(res).get("valid") is False)

    res = call("validate_manifest", {"path": "../../etc/passwd.yaml"})
    check("path confinement rejects an escape attempt",
          (res.get("isError") is True)
          and "outside the repository" in json.dumps(_first_json(res)))

    res = call("run_workflow", {"path": "workflow/manifests/senior-dev-loop.yaml"})
    body = _first_json(res)
    check("run_workflow completes and labels itself a stub run",
          body.get("outcome") == "complete" and "stub executor" in (body.get("note") or ""))

    res = call("run_workflow", {"path": "workflow/manifests/senior-dev-loop.yaml",
                                "enforce_contracts": True})
    body = _first_json(res)
    check("run_workflow with enforce_contracts flags contract violations",
          any(n.get("verdict") == "contract-violation" for n in body.get("nodes", {}).values()))

    res = call("run_workflow", {"path": "/etc/hosts"})
    check("run_workflow refuses a path outside the repository", res.get("isError") is True)

    res = call("no_such_tool", {})
    check("unknown tool returns an error result, not a crash", res.get("isError") is True)

    failed = [c for c in checks if not c[1]]
    for label, ok, detail in checks:
        print("%s %s%s" % ("PASS" if ok else "FAIL", label,
                           ("  [%s]" % detail) if detail and not ok else ""))
    print("selftest: %d checks, %d failed" % (len(checks), len(failed)))
    return 1 if failed else 0


def _first_json(result):
    try:
        return json.loads((result.get("content") or [{}])[0].get("text", "{}"))
    except ValueError:
        return {}


def main(argv=None):
    ap = argparse.ArgumentParser(description="MCP server over the skill library (stdlib only)")
    ap.add_argument("--selftest", action="store_true", help="run in-process protocol/tool checks")
    ap.add_argument("--list-tools", action="store_true", help="print the tool catalogue and exit")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()
    if args.list_tools:
        for spec in tool_specs():
            print("%s\n    %s" % (spec["name"], spec["description"]))
        return 0
    return serve(Library())


if __name__ == "__main__":
    sys.exit(main())
