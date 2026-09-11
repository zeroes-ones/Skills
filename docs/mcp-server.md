# MCP Server — Drive the Skill Library From Any MCP Client

> **What this is.** `scripts/mcp-skill-server.py` exposes this skill library and its workflow engine
> over the **Model Context Protocol** on stdio. Any MCP-capable client — Claude Code, Cursor, Cline —
> can then search for a skill, read one, inspect its declared completion contract, validate a
> workflow, and **actually run one** — without symlinking directories and without installing
> anything.

---

## 1. Why this exists (and what it is not)

Before this server, consuming the library meant one of two things:

| Approach | What it gives you | What it does not |
|---|---|---|
| Symlink `skills/` into the agent's discovery directory | The agent can *read* playbooks | No search, no graph, no contracts, no engine |
| Read `SKILL.md` files off disk by hand | Same | Same |

Neither gives a client the **engine**: the dependency graph, the declared contracts, the manifest
validator, or the ability to execute a workflow. That is what this server adds.

**It is not** a replacement for the existing distribution paths (npm/skills.sh/plugins) — those
install *files*. This serves *capability*. They coexist.

**It is also not** a second implementation of anything. Every answer it gives comes from the repo's
own machinery:

| Concern | Single source of truth it reuses |
|---|---|
| Skill discovery | `validate-workflows._find_skill_names()` |
| YAML parsing | `lib/safe_yaml` |
| Contract extraction | `lib/lint-workflow.extract_workflow_block()` |
| Manifest validation | `validate-workflows.WorkflowValidator` |
| Workflow execution | `scripts/workflow-runner.py` |

---

## 2. Install

### Claude Code (project scope — already wired)

The repository ships `.mcp.json`:

```json
{
  "mcpServers": {
    "zeroes-ones-skills": {
      "command": "python3",
      "args": ["scripts/mcp-skill-server.py"],
      "env": {}
    }
  }
}
```

Open Claude Code in this repository and the server is discovered automatically. Approve it when
prompted (project-scoped MCP servers require an explicit trust step the first time).

### Cursor

Create `.cursor/mcp.json` with the same `mcpServers` block, using an **absolute** path:

```json
{
  "mcpServers": {
    "zeroes-ones-skills": {
      "command": "python3",
      "args": ["/absolute/path/to/Skills/scripts/mcp-skill-server.py"]
    }
  }
}
```

### Any other client

Point it at `python3 <repo>/scripts/mcp-skill-server.py` over stdio. No environment variables, no
tokens, no network.

### Requirements

Python 3. **Nothing else** — no `pip install`, no `npm install`, no Node. The server is stdlib-only.

---

## 3. Tool reference

Run `python3 scripts/mcp-skill-server.py --list-tools` for the same catalogue from the CLI.

### `list_skills`

List skills, optionally filtered.

| Input | Type | Notes |
|---|---|---|
| `domain` | string | e.g. `05-development`, or a skill directory name like `devops` |
| `declared_only` | boolean | only skills that declare a `workflow:` contract |
| `limit` | integer | default 100 |

```json
{"total": 304, "shown": 3, "skills": [
  {"skill": "code-reviewer", "domain": "06-quality", "declared": true,
   "description": "Use when performing structured code reviews on pull requests…"}
]}
```

### `get_skill`

Fetch the complete `SKILL.md` — the same content the engine injects into a node prompt.

| Input | Type | Notes |
|---|---|---|
| `name` | string **required** | frontmatter name, e.g. `code-reviewer` |

Returns the raw markdown as text. This is the "load a playbook" call.

### `get_skill_contract`

The most interesting tool: a skill's optional `workflow:` contract — what it consumes, what it
produces, its checklist for "done", whether evidence is required, and where it escalates.

| Input | Type | Notes |
|---|---|---|
| `name` | string **required** | skill name |

Declared contract:

```json
{"skill": "incremental-implementation", "declared": true, "mode": "L3 contract",
 "enforceable": true,
 "contract": {
   "artifacts": {"inputs": ["spec"], "outputs": ["change"]},
   "completion": {"criteria": [
      "Every slice ships behind a feature flag defaulting to false",
      "Tests pass with the flag both ON and OFF",
      "No destructive schema changes (ADD only, no DROP or ALTER)"],
     "evidence": "required"},
   "escalate_to": ["human-gate"]}}
```

No contract declared — the server explains default mode instead of pretending there is one:

```json
{"skill": "skill-levels", "declared": false, "mode": "default", "enforceable": false,
 "criteria_source": "the skill's Verification / Production Checklist tables, read at execution time",
 "eligible_default_mode": true,
 "note": "A contract is optional and additive. Without it the node still runs; its completion
          claim simply cannot be asserted by the engine."}
```

`enforceable: true` is the meaningful distinction: only a declared contract can be asserted by
`--enforce-contracts`.

### `search_skills`

Lexical search over skill names and descriptions — how a client finds the right skill for a task.

| Input | Type | Notes |
|---|---|---|
| `query` | string **required** | terms, e.g. `database migration rollback` |
| `limit` | integer | default 10 |

Scoring favours name matches (weight 10 per term) over description matches (weight 3 per
occurrence), then sorts by score and name for a stable order.

### `get_skill_graph`

With `name`: that skill's upstream and downstream neighbours. Without: library totals and hubs.

```json
{"skills": 304, "domains": 37, "directed_edges": 1932, "undirected_edges": 1577,
 "declared_contracts": 43, "eligible_default_mode": 301,
 "top_hubs": [{"skill": "backend-developer", "edges": 85},
              {"skill": "using-agent-skills", "edges": 66}]}
```

### `list_workflows`

The executable manifests in the repo, with node/loop/gate counts.

```json
{"total": 20, "workflows": [
  {"manifest": "workflow/manifests/senior-dev-loop.yaml", "name": "senior-dev-loop",
   "nodes": 2, "loops": 1, "gates": 1}]}
```

### `validate_manifest`

Validate a manifest: structure, cycle rejection, loop budgets, payload registry, reachability.

| Input | Type | Notes |
|---|---|---|
| `path` | string **required** | relative to the repository root |

```json
{"valid": true, "errors": []}
```

Invalid input returns `isError: true` with the reasons, so a client sees failure rather than a
plausible-looking pass.

### `run_workflow`

Execute a manifest and return the run summary. **Read the security note in §5.**

| Input | Type | Notes |
|---|---|---|
| `path` | string **required** | relative to the repository root, must end `.yaml` |
| `max_steps` | integer | override the global step budget |
| `enforce_contracts` | boolean | assert each node's declared completion contract |

```json
{"workflow": "senior-dev-loop", "outcome": "complete", "steps_used": 3,
 "iterations": {"micro-sdlc-loop": 1},
 "nodes": {"implement": {"status": "done", "verdict": "pass", "iterations": 1}},
 "note": "executed with the deterministic stub executor: control flow only, no agent and no node content",
 "exit_code": 0}
```

---

## 4. Protocol notes

- **Transport:** stdio. One JSON object per line in, one per line out (newline-delimited JSON-RPC
  2.0). No `Content-Length` framing.
- **Methods implemented:** `initialize`, `notifications/initialized` (notification, never answered),
  `ping`, `tools/list`, `tools/call`.
- **Protocol versions accepted:** `2024-11-05`, `2025-03-26`, `2025-06-18`. The server echoes the
  client's requested version when it is one of these, and otherwise replies with `2024-11-05`.
- **Errors** use standard JSON-RPC codes: `-32700` parse, `-32600` invalid request, `-32601` method
  not found, `-32602` invalid params. A tool that fails returns a normal result with `isError: true`
  and a message, so the client can read the failure rather than lose the session.
- **stdout is protocol-only.** All diagnostics go to stderr. A stray `print()` on stdout would
  corrupt the stream — worth knowing before editing the server.
- **Batch requests are rejected** with `-32600` rather than silently mishandled.

---

## 5. Security posture

| Property | Behaviour |
|---|---|
| **Node content** | `run_workflow` uses the **deterministic stub executor**. No LLM, no agent, no shell. It exercises control flow (loops, budgets, gates, contracts) and returns the summary. It cannot execute work. |
| **Path confinement** | Manifest paths must resolve inside the repository and end in `.yaml`. `../../etc/passwd.yaml` and `/etc/hosts` are rejected. |
| **Filesystem** | Reads only, under the repository. |
| **Network** | None. The server makes no outbound connections. |
| **Secrets** | None read, none required. |
| **Writes** | None. The server never modifies the repository. |

If you want MCP clients to run workflows with **real agent content**, that is a deliberate step up in
blast radius and should be a separate, explicitly-enabled tool — not the default.

---

## 6. Testing

```bash
# in-process protocol + tool checks
python3 scripts/mcp-skill-server.py --selftest

# the tool catalogue, for humans
python3 scripts/mcp-skill-server.py --list-tools

# a real stdio round-trip (what a client does)
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18"}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_skill_graph","arguments":{}}}' \
  | python3 scripts/mcp-skill-server.py
```

`--selftest` covers: version echo and fallback, notifications getting no reply, `ping`, an unknown
method returning `-32601`, `tools/list` advertising every tool with a schema, every tool being
callable, default-mode vs declared contracts, search relevance, graph totals, manifest validation
both ways, **path-confinement rejection**, and `--enforce-contracts` surfacing a
`contract-violation`.

---

## 7. Design decisions worth knowing

### Why stdlib instead of the official TypeScript SDK

The obvious move is `@modelcontextprotocol/sdk` and a `node_modules` tree. It was rejected because:

1. **The library's core is dependency-free by design** — a documented invariant, and the reason the
   engine runs anywhere Python 3 runs.
2. **The protocol surface needed is small** — four methods and a result envelope. That is
   implementable and testable directly.
3. **The tool layer is transport-independent.** If you later want the official SDK, `call_tool()` and
   `tool_specs()` are reusable as-is; only the ~60-line transport would change.

The trade-off is honest: a hand-rolled transport can drift from the spec as MCP evolves, and there is
no community code to lean on. `--selftest` plus the round-trip above is the mitigation.

### Three defects in the "obvious" MCP server that this implementation does not have

A commonly-circulated snippet for this repo had:

| Defect | Here |
|---|---|
| Resolved `skills/<name>/SKILL.md` — one directory level, but this repo is `skills/<domain>/<name>/SKILL.md` — so every lookup would fail | Resolution goes through the repo's own `_find_skill_names()`, which walks the real two-level layout |
| Declared a `projectTier` input and never read it — a documented parameter that silently does nothing | No parameter is declared unless it is implemented. Tier-scoped listing is a documented *future* addition, not a fake control |
| Mixed TypeScript (`as { skillName: string }`) into a `.js` example | Plain Python, compiled and exercised by `--selftest` |

### Not implemented (deliberately)

- **MCP *resources*** — only tools are exposed. Resources would let a client browse skills as a tree;
  useful, but tools cover the read paths already and resources add surface area.
- **Tier filtering** (`solo` / `grow` / `enterprise`) — the library has tiers for *installation*; a
  `tier` filter on `list_skills` would be a natural next addition. Not declared until implemented.
- **Real-agent execution** (`run_workflow` with the agent executor) — see §5.
- **Streaming / progress notifications** — every tool returns a single result.

---

## 8. Status

Verified by `--selftest` and by a piped stdio round-trip. Both are commands you can run yourself in
under a second — see §6. If a check fails after a change, the failure is named in the output; that is
what the suite is for.
