# Workflow System — Loops, Graphs, and Smooth Handoffs Over the Skill Library

> **Version 1.0.0** — Canonical specification for executing the skill library as graphs and loops:
> iterate until done, hand off state without loss, escalate instead of looping forever or stopping early.
> Portable across Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI. No framework required at the
> canonical level; optional mappings to LangGraph/CrewAI are documented and demonstrated in
> `examples/workflow-runtime/`.

> **Implementation status.** This document separates **intent** from **what the engine enforces**.
> A claim is a guarantee only if the runner implements it. Where the two differ, a *Runtime caveat
> (verified)* block or the *Declared but not yet implemented* table (Section 4.5) says so explicitly,
> with a reproduction. Section 4.5 is the single table to read before depending on any field.
>
> Citations inside `scripts/workflow-runner.py` name the function or method rather than a line
> number where practical: that file carries a large in-flight change set in this checkout, so line
> numbers move. Line-number citations elsewhere were checked against the working tree when this
> revision was written and reproduced with the commands in each block.

## Why This Exists

The library already has a **static graph** (the symmetric `chain:` dependency DAG, **2,213** distinct
directed edges over 327 nodes, exported by `scripts/emit-skill-graph.py` to
`docs/graph-explorer/skill-graph.json`) and **prose workflows** (each skill's Core Workflow +
Verification sections, and narrative flows like `examples/orchestra-platform/`). What has been
missing is the **execution layer**: a machine-checkable way to say

- *which* skills participate in a piece of work and in what shape (sequence, fan-out, loop, gate),
- *when a node is actually done* (completion criteria with evidence — not vibes),
- *what happens when it is not done* (revise within a budget, then escalate — never silently stop,
  never loop forever),
- *what exactly crosses the boundary between nodes* (a handoff payload that a downstream agent can
  consume without re-deriving upstream context).

This document defines that layer. It deliberately separates **control flow** (deterministic, owned
by code and linters) from **content** (agentic, owned by skills). Agents stay agents; the boring,
error-prone bookkeeping — traversal, iteration budgets, stagnation detection, cycle rejection,
checkpointing — moves to deterministic machinery.

## The Three-Layer Model

```
┌────────────────────────────────────────────────────────────────────────┐
│  L2  EXECUTION  run-state JSON + loop protocol + boundary templates   │
│      (the runner does control flow; the agent does content)           │
├────────────────────────────────────────────────────────────────────────┤
│  L1  MANIFEST   workflow YAML: nodes / edges / loops / gates          │
│      (one executable statement per piece of work)                     │
├────────────────────────────────────────────────────────────────────────┤
│  L0  CONTRACT   optional "workflow:" frontmatter on a SKILL.md        │
│      (artifacts, completion criteria, iteration budget, escalation)   │
├────────────────────────────────────────────────────────────────────────┤
│  BASE  the library: SKILL.md content, chain: graph, handoff protocol │
└────────────────────────────────────────────────────────────────────────┘
```

- **L0 — Node contract.** Optional, additive `workflow:` frontmatter that makes one skill usable as a
  graph node: what it consumes, what it produces, what counts as done, how many revision attempts it
  tolerates, where it escalates. Skills without the block run in **default mode** (Section 8).
- **L1 — Workflow manifest.** A YAML file that composes skills into a graph. The manifest is the unit
  of review, versioning, and reuse — the workflow equivalent of a `SKILL.md`.
- **L2 — Execution semantics.** The canonical, portable way any agent CLI can run a manifest: a
  run-state JSON file the executing agent reads and writes, a four-step node protocol
  (intake → execute → verify → decide), deterministic guardrails, and fixed prompt templates at
  every boundary.

The base layer is the existing library; this spec only adds to it.

## 1. L0 — Node Contract (per-skill `workflow:` frontmatter)

Optional, additive YAML in a `SKILL.md` frontmatter:

```yaml
workflow:
  artifacts:
    inputs: [brief, system-context]        # names of expected inputs (run-state fields / files)
    outputs: [spec]                        # names of produced artifacts
  completion:                              # what "done" means for THIS node
    criteria:
      - "Every explicit requirement has a matching section in the spec"
      - "All open questions are resolved or flagged open_questions"
    evidence: required                     # required | optional
  iteration:
    max: 3                                 # revision attempts before escalation (1 = no loop)
    on_exhaustion: escalate                # escalate | next | fail
  escalate_to: [human-gate, agent-handoff-protocol]   # where exhaustion goes
```

Rules:

| Rule | Meaning |
|------|---------|
| Additive | Absent `workflow:` block = default mode. Existing skills are untouched and valid. |
| Shallow | The block may contain only scalars and one level of lists/maps (safe YAML subset, Section 3). |
| Completion is asserted only under `--enforce-contracts` | With enforcement on, `completion.evidence: required` must be satisfied and every `completion.criteria` entry must be covered by the node's `criteria_met` report (`workflow-runner.py`, `Runner._contract_violations`; short-circuited by `enforce_contracts` at the top of that method). With enforcement off (the default), the block is parsed but not asserted. |
| `artifacts.inputs` is declarative, `artifacts.outputs` is a warning | `artifacts.inputs` is linted (`scripts/lib/lint-workflow.py`) but never read at runtime. Declared `artifacts.outputs` that were not produced is recorded as `action: contract-warning` and is **never** blocking (`workflow-runner.py`, `Runner._contract_violations` → `Runner._apply_contract`). |
| `iteration.max` / `on_exhaustion` / `escalate_to` are declarative | These keys are parsed into the contract but not read by the runner. Revision bounds and exhaustion routing come from the manifest's `loops[].max_iterations` and `loops[].escalate_to`, not from the node block. See Section 4.5. |
| Verification section is the fallback (executor-side) | With no `criteria`, the node's Verification / Production Checklist tables are the criteria source by convention, applied by the executing agent. The runner itself never reads a skill's body. |

Why criteria-with-evidence? A node that cannot say what "done" means cannot be looped safely. The
single most expensive failure in agent workflows is **premature completion** — declaring done with
zero evidence. The second is **infinite refinement** — polishing past the point of return. The node
contract exists to make both *detectable* — asserted when `--enforce-contracts` is on, and declared
for the executor to honour when it is off.

## 2. L1 — Workflow Manifest

### 2.1 File conventions

- Manifests live under `workflow/manifests/` (library-owned, versioned) or inside an example/use
  directory (e.g. `examples/workflow-runtime/workflow.yaml`).
- One workflow = one `.yaml` file. Filename is the workflow `name`.
- `name` must be a lowercase slug (`[a-z0-9][a-z0-9-]*`).
- Every `skill:` reference must resolve to a directory under `skills/` by frontmatter `name`.

### 2.2 Minimal manifest

```yaml
name: spec-to-arch
version: "1.0.0"
description: Draft a spec, then design architecture, then review once.
start: idea-to-spec
nodes:
  - id: idea-to-spec
    skill: idea-to-spec
    outputs: [spec]
  - id: system-architect
    skill: system-architect
    inputs: [spec]
    outputs: [architecture]
  - id: arch-review
    skill: code-reviewer
    inputs: [architecture]
    outputs: [review-verdict]
edges:
  - from: idea-to-spec
    to: system-architect
    when: idea-to-spec.status == done
    payload: handoff-v1
  - from: system-architect
    to: arch-review
    when: system-architect.status == done
    payload: handoff-v1
end: [arch-review]
```

### 2.3 Node types

| `type` | Default | Role |
|--------|---------|------|
| `skill` | yes | Executes one skill from the library. `skill:` required. |
| `gate` | no | Checkpoint that does no work: automated (condition on state), agent (identify + bounded reroute before a human), or human (requires approval). `type: gate` + `kind: human|auto|agent`. |
| `supervisor` | no | Routing node. Delegates to `workers` by capability; performs no content work itself. |
| `task` | no | Reserved for non-skill work (script, stub executor in examples). `executor:` names the handler. |

**Runtime caveat (verified):** the runner never dispatches on `type`. `Runner.__init__` builds
`self.nodes` as a flat id → entry map (`workflow-runner.py`) and every node — `skill`, `gate`,
`supervisor`, `task` — is handled by the one traversal path (`Runner.run`; `Runner._run_loop_pass`
inside a loop). `type` is validated statically (`scripts/validate-workflows.py:159-171`) and is
meaningful for gates, whose `kind` **is** read; `supervisor` and `task` semantics are declared and
validated but not yet executed. See Section 4.5.

### 2.4 Edges, loops, parallel, gates

**Edges** — directed transitions, validated for endpoint existence:

```yaml
edges:
  - from: idea-to-spec
    to: system-architect
    when: idea-to-spec.status == done   # condition vocabulary, see 2.6
    payload: handoff-v1                 # optional registry name
```

**Loops** — the heart of "iterate until done". A loop declares which nodes repeat, when they exit,
and what the budget is:

```yaml
loops:
  - id: review-fix-loop
    nodes: [reviewers, fixer]           # node ids executed per pass, in order
    exit_when: reviewers.verdict == pass   # evaluated after each pass
    max_iterations: 3
    escalate_to: human-gate             # node id of a gate
    convergence:
      window: 2                         # stop looping if N consecutive passes
      require_delta: true               #   produce no delta in diagnostics
```

Loop invariants (enforced by the validator and the runner):

| Invariant | Why | Enforced by |
|-----------|-----|-------------|
| Every loop has `exit_when` + `max_iterations` | No unbounded repetition by construction. | Validator (`scripts/validate-workflows.py:224-237`); runner reads both (`Runner._run_loop_pass`) |
| `max_iterations >= 1` | A loop is a loop. | Validator (`scripts/validate-workflows.py:236`) |
| Exhaustion target exists | `escalate_to` must resolve to a node id in the same manifest. | Validator (`scripts/validate-workflows.py:240-241`); runner routes to it (`Runner.run`) |
| No node appears in two loops | Nested/overlapping loops are ambiguous; flatten instead. | **Validator does not check this** — a node listed in two loops validates clean (verified). Treat as an authoring rule, not a gate. |
| Stagnation detector optional, default on | Identical consecutive passes produce no new information; keep looping = burning budget. | Runner (`Runner._run_loop_pass` → `Runner._stagnant`) |

**Parallel blocks** — fan-out with an explicit join:

```yaml
parallel:
  - id: reviewers
    nodes: [code-reviewer, security-reviewer, qa-engineer]
    join: all          # all | majority | any
    outputs: [findings]  # merged into one run-state field
```

Parallel nodes must not write the same run-state field (no shared-mutable writes; merge happens at
the join, Section 5.3).

**Runtime caveat (verified):** the runner's join is always `all`. `Runner._advance_from` holds at the
join until every member has reached a *terminal status* — `_STATUS_WORDS = {done, blocked,
needs_review, skipped}` — and `Runner.__init__` reads `pb.get("join", "all")` only to store it; the
value never branches. So the hold is "all members stopped", not "all members succeeded": a `blocked`
member releases the join exactly like a `done` one. A manifest declaring `join: any` or
`join: majority` behaves identically to `join: all` (verified with one `blocked` and one `done`
member: `sink` fires for all three values). The docstring on `_advance_from` claims `any/majority`
"degrades to 'any'"; the code proves `all`, and this document now states `all`. `parallel[].outputs`
is likewise stored in `Runner.__init__` and never merged.

**Gates** — deliberate pauses in the graph:

```yaml
gates:
  - id: human-gate
    type: gate
    kind: human
    requires: [findings, fix-report]    # artifact refs that must exist before this gate
    description: Production change requires human approval.
```

**Identify-agent gates (`kind: agent`)** — the pre-human escalation step. A loop that cannot
converge (max-iterations or stagnation) escalates to an agent gate *before* any human gate. The
gate names the corrective channel and grants the loop a fresh bounded window with that channel
first; only a spent reroute budget, a no-delta window across reroutes, or a non-reroutable reason
routes it onward to the terminal `escalate_to` (the human gate):

```yaml
gates:
  - id: identify-agent-gate
    type: gate
    kind: agent
    pool: [fixer, qa]          # corrective channels — must be members of the escalating loop
    max_reroutes: 3            # bounded reroute budget before the human gate
    escalate_to: human-gate    # terminal target after budget / no-delta / non-reroutable
loops:
  - id: quality-loop
    nodes: [fixer, qa]
    exit_when: qa.verdict == pass
    max_iterations: 3
    escalate_to: identify-agent-gate
```

Semantics (runner-enforced, executor-assisted; see `workflow/templates/escalate.md` and the
`valid-agent-gate-reroute` fixture):

| Rule | Why |
|------|-----|
| Triggered only by loop exhaustion (`escalate_to` from a loop) | A working loop never needs triage. |
| `pool` must be members of the escalating loop | The fix lives inside one of the loop's own channels; the gate decides which channel leads. |
| `max_reroutes` bounds reroute windows | No infinite agent-recursion by construction. |
| Identify is a content step (`ctx.mode == "identify"`) | The executor names the channel; deterministic fallback = first untried pool member. |
| No delta across reroutes escalates | Identical end-states across fresh windows produce no new information. |
| Human gate stays terminal and reachable | `escalate_to` on the agent gate must resolve; the human remains the last authority. |
| Non-reroutable reasons (step-budget, guardrail-block) escalate directly | Re-routing cannot fix a spent global budget or a blocked payload. |

### 2.5 Supervisor nodes (multi-agent mode)

A supervisor node routes to workers and owns the outcome of its fan-out. It performs routing only —
no content work (matches the multi-agent-orchestration ground rule: supervisors route, workers work).

```yaml
nodes:
  - id: lead
    type: supervisor
    skill: multi-agent-orchestration     # optional: guidance skill for the router
    workers: [code-reviewer, security-reviewer, qa-engineer]
    routing: parallel                    # parallel | sequential | select
    select: code-reviewer                # routing: select → fixed worker
    escalate_to: human-gate
```

Canonical semantics: a supervisor's pass is done when all `workers` (parallel), the chain of
`workers` (sequential), or the selected worker has produced a result with status; failure of any
worker follows the manifest's `on_exhaustion` path. This maps 1:1 to LangGraph supervisor
patterns — see `examples/workflow-runtime/references/langgraph-mapping.md`.

**Runtime caveat (verified):** these supervisor semantics are declared, not executed. The runner does
not branch on `type` (see Section 2.3), so a `type: supervisor` node is executed as an ordinary
single-skill node through the one traversal path; `workers`, `routing`, and `select` are validated
(`scripts/validate-workflows.py:314-329`) and never read by the runner. The `on_exhaustion` path named
above does not exist at runtime — see Section 4.5. The mapping to LangGraph remains the *intended*
translation, not a description of the stdlib engine's behaviour.

### 2.6 Condition vocabulary (edges and loops)

Conditions are deliberately small. Executors and the runner interpret exactly this vocabulary; the
validator checks syntax only:

| Form | Meaning |
|------|---------|
| `always` | Unconditional. |
| `NODE.status == done` / `!= done` | Node terminal status (done, blocked, needs_review, skipped). |
| `NODE.status in (a, b)` | Membership on terminal status. |
| `NODE.verdict == VALUE` / `!= VALUE` | Verdict equality (strings only). The runner implements `!=` for verdict as well as `==` (`workflow-runner.py`, `eval_condition`). |
| `loop.iterations < N` | Loop budget remaining (loop context only). |

Anything else is a validation error. This keeps manifests readable by humans and executable by the
runner without a general-purpose expression engine.

### 2.7 State schema (typed shared state)

```yaml
state:
  shared: true
  schema: review-state-v1      # optional name; fields are declared by node outputs
  merge: append-unique         # how parallel outputs merge at the join
```

Canonical rule (from agent-handoff-protocol / multi-agent-orchestration): **every run-state field
has exactly one writer role at a time.** Parallel fan-out writes disjoint fields; the join merges
them. No two live nodes write the same field. The validator flags conflicting `outputs` within a
parallel block.

**Runtime caveat (verified):** the `state:` block is not read by the runner. `merge` is stored by
nothing and applied by nothing (`scripts/workflow-runner.py` has zero `merge` references outside
comments; `scripts/validate-workflows.py` likewise). The write-ownership rule above is enforced only
as the static `outputs`-disjointness check inside `parallel` blocks
(`scripts/validate-workflows.py:262-271`) — it is not enforced at merge time, because there is no
merge step. Run-state `fields` are initialised empty by `fresh_state` (`scripts/workflow-runner.py`)
and written by executors directly; the runner performs no field-merge of its own.

### 3. Safe YAML Subset

Manifests and `workflow:` frontmatter blocks are YAML — but a **documented subset** that a
dependency-free validator and runner can parse safely:

- Scalars: strings (quoted or bare alphanumerics, `-`, `_`, `/`, `.`, `==`, `,`, spaces), integers,
  booleans (`true`/`false`).
- Scalar-only flow lists: `[a, b, c]` as a value (no nesting, no flow maps).
- Structures: indentation-based maps and lists, one structural level deep inside each list item.
- Comments (`#`) allowed on their own lines or trailing a value.
- No anchors/aliases, no flow maps, no block scalars (`|`, `>`), no multi-document files.

The normative parser is `scripts/lib/safe_yaml.py` (stdlib-only, 259 lines) — one file shared by
`scripts/validate-workflows.py`, the frontmatter lint (`scripts/lib/lint-workflow.py`), and
`scripts/workflow-runner.py`. The schema files in `workflow/schema/` document fields; validation
logic lives in the scripts and is exercised by their fixture suites.

## 4. L2 — Execution Semantics (canonical, portable)

### 4.1 Run-state file

One JSON file per run: `run-state.json` (location chosen by the runner; `.agent-run/` when inside a
repo). Schema in `workflow/schema/run-state.schema.yaml`. Canonical shape:

```json
{
  "workflow": "review-and-fix",
  "manifest_sha": "9f2c…",
  "created": "2026-09-08T10:00:00Z",
  "updated": "2026-09-08T10:04:12Z",
  "node": "code-reviewer",
  "phase": "execute",
  "iteration": 1,
  "budget": { "max_steps": 40, "steps_used": 7, "iterations": { "review-fix-loop": 1 } },
  "nodes": {
    "code-reviewer": { "status": "done", "verdict": "changes_requested", "iterations": 1,
                       "evidence": ["review.md"], "summary": "…", "sha": "…" }
  },
  "fields": {
    "findings": { "value": [{"severity": "high", "file": "src/auth.py", "note": "…"}],
                  "writer": "reviewers" }
  },
  "artifacts": { "review.md": { "path": "artifacts/review.md", "sha": "…", "type": "doc" } },
  "decisions": [ { "at": "code-reviewer", "what": "auth refactor required", "by": "code-reviewer" } ],
  "open_questions": [],
  "handoff": { "from": "fixer", "to": "reviewers", "payload": "handoff-v1", "sha": "…",
               "integrity": { "frozen": { "status": "done", "…": "…" }, "digest": "…" } },
  "log": [ { "step": 7, "node": "code-reviewer", "action": "done", "detail": "verdict=changes_requested" } ]
}
```

**Vocabulary caveat (verified).** The runner writes, and only writes:

| Field | Values the runner actually writes | Where |
|-------|-----------------------------------|-------|
| `phase` | `idle` (fresh state), `execute`, `escalated`, `complete`, `error` | `workflow-runner.py`: `fresh_state`, `Runner.run`, `Runner._apply_guardrail`, `Runner._run_loop_pass`, `Runner._crash_checkpoint` |
| `log[].action` | `done`, `guardrail`, `contract`, `contract-warning`, `contract-rework`, `contract-rework-ok`, `escalate`, `error`, `agent-gate` | `workflow-runner.py`: `Runner._mark_done`, `_apply_guardrail`, `_apply_contract`, `_run_contract_rework`, `_crash_checkpoint`, `_agent_gate_visit`, and `Runner.run` |

The `phase` enum in `workflow/schema/run-state.schema.yaml` also lists `intake`, `verify`, `decide`,
`done`, and `blocked`, and its `log.action` enum lists `intake`, `execute`, `verify`, `revise`,
`handoff-out`, `handoff-in`, `checkpoint` — **none of which the runner writes**. Those values describe
the protocol an *executor* follows (Section 4.2), not state the engine produces. A consumer parsing
run-state should therefore treat the engine-written values above as the reliable set and the schema
enums as the wider, executor-level vocabulary.

**Fresh-state keys (verified):** `fresh_state` (`scripts/workflow-runner.py`) creates `workflow,
manifest_sha, created, updated, node, phase, iteration, budget, nodes, fields, artifacts, decisions,
open_questions, handoff, reroutes, log`. `reroutes` is engine-owned bookkeeping for `kind: agent`
gates and is not in the schema document.

Every write by a node updates `updated` and appends to `log`. The runner hashes exactly one thing:
the **node record** — `rec["sha"] = _sha(rec)` in `Runner._mark_done`. It does not hash `fields` or
`artifacts`; the `sha` on an artifact record is passed through from whatever the executor reported
(`Runner._mark_done`), and `fields` is initialised empty by `fresh_state` with no runner-applied hash.

**Handoff integrity — `sha` recorded (not verifiable), `integrity` verified (implemented).** The
runner writes a `handoff {from, to, payload, sha, budget, integrity}` record when it selects the next
node (`Runner._handoff_record`, called from `Runner._advance_from` and `Runner.run`). `sha` is
`_sha(state["nodes"][src])` — the **sender's node record**, not the payload content — and it is still
written and never compared, because it *cannot* be: the sender's record is legitimately rewritten
after the hop (loop re-entry resets members to `pending`, `Runner._mark_done` re-hashes, contract
rework resets again), so re-reading it later would report corruption on a healthy run.

The verifiable object is `integrity = {frozen, digest}`: `frozen` is a JSON snapshot of
`nodes[src]` taken at send time, and `digest` is `_sha({from, to, payload, frozen, budget})`. It is
checked twice — at send time in `_handoff_record`, and on every `--state` resume
(`resume_state` → `_verify_handoff`), where a mismatch raises `StateCorruption` naming the hop. A
state file written before this existed has no `integrity` block: it loads and runs, and the run
records `last_handoff_verified: false` rather than implying the digest was checked.

| | Detects | Does not detect |
|---|---|---|
| `handoff.integrity` digest | An edited/corrupted `handoff` record: its frozen snapshot, or hop metadata (`from`/`to`/`payload`/`budget`) | Edits to `nodes[...]` themselves — the frozen record is a copy, not a hash of the live record, so it cannot attest it. A checkpoint-wide (Merkle) digest over the whole state file would be the change that closes this. |
| `handoff.sha` | Nothing | — (written for downstream executors; the `handoff-in` template asks the receiving agent to check hashes, which is a prompt-level obligation, not a runner guardrail) |

### 4.2 Node lifecycle

```
INTAKE  →  EXECUTE  →  VERIFY  →  DECIDE
                                    ├─ DONE      → write handoff payload, advance edges
                                    ├─ REVISE    → write diagnostics, iterate (budget guard)
                                    └─ ESCALATE  → exhaustion / blockage → gate or report
```

| Step | What happens | Failure to do it |
|------|--------------|------------------|
| INTAKE | Read run-state + `handoff` payload + node's SKILL.md (Route the Request + Ground Rules + the `workflow:` criteria). | Downstream re-derives upstream context; context rot; regression reintroduction. |
| EXECUTE | Perform the node work per the skill. Record artifacts, decisions, open questions. | — |
| VERIFY | Check every completion criterion against concrete evidence (artifact path/hash, test output, checklist). No criterion without evidence = not done. | Premature completion. |
| DECIDE | Criteria pass → `done`; fail with budget left → `REVISE`; fail at budget → exhaustion path; blocked on missing info → `blocked`, escalate (never loop on an external blocker). | Infinite refinement or silent stop. |

The four steps are prompted, not assumed — templates in `workflow/templates/` (Section 7) encode
them so the executing agent performs VERIFY before ever claiming done.

**Scope of the engine (verified).** INTAKE/EXECUTE/VERIFY/DECIDE is the executor's protocol, not the
runner's control flow. The runner offers the executor a context dict and reads back a result dict
(`status`, `verdict`, `summary`, `evidence`, `artifacts`, `decisions`, `open_questions`,
`diagnostics`, `criteria_met`, `usage` — the runner's module docstring, "Executor contract"); it never
prompts, never reads a SKILL.md body, and never inspects an artifact's contents. Where this document
says a step is "enforced", the enforcement is either a prompt obligation the executor carries, or the
narrower result-shape check named in Section 4.4.

### 4.3 Loop protocol (the heart of "iterate until done")

1. **Pass N runs**: execute the loop's nodes in order against current run-state.
2. **Exit check**: evaluate `exit_when`. True → loop complete; advance along the loop's continuation
   edges.
3. **Delta check** (stagnation): compare diagnostics with the previous pass. No delta for
   `convergence.window` passes → treat as exhaustion (looping identical work is budget burning).
4. **Budget check**: `iteration >= max_iterations` → exhaustion.
5. **Exhaustion**: route to the **loop's** `escalate_to` when set, else end the run with the exit
   reason. There is no node-level `on_exhaustion` at runtime — that key is declarative only
   (Section 4.5). Escalation carries the exit reason and the per-pass end-state signature.
6. Never continue past budget; never repeat an identical pass (the stagnation detector
   `Runner._stagnant`, called from `Runner._run_loop_pass`, fires on identical diagnostics; an agent
   gate additionally escalates on `no delta across reroutes`, `Runner._agent_gate_visit`).

The loop's exit reason — `exit-condition`, `max-iterations`, `stagnation`, `step-budget`, or
`cost-budget` — is what the run summary's `outcome` is built from (`Runner.run`, which sets
`self._loop_exit_reason`, and `Runner._summary`). A consumer should read `outcome`, not infer the
reason from the absence of a handoff.

### 4.4 Deterministic guardrails (runner-enforced, not prompt-requested)

| Guardrail | Mechanism | Actually enforced? |
|-----------|-----------|--------------------|
| Cycle rejection | A node may not be its own ancestor except through a declared loop. | **Validator only.** `_check_cycles` performs a DFS and rejects undeclared cycles (`scripts/validate-workflows.py:338-368`). The runner has **no node stack**: it keeps a `seen` set (`workflow-runner.py`, `Runner.run`) and silently prunes a back-edge rather than aborting. Run the runner on an unvalidated cyclic manifest and it completes rather than reporting a cycle. |
| Step budget | Global `budget.max_steps` hard cap; runner halts and reports when exceeded. | Yes — `Runner.run` checks before each step and `_run_loop_pass` checks per member; the run ends with outcome `step-budget`. The budget comes from `--max-steps`, else manifest `budget.max_steps`, else `10 × node count` (`workflow-runner.py`, `main`). |
| Cost budget | Optional manifest `budget.max_cost_usd`; halts when reached. | Yes, when the executor reported usage (`cost_exceeded`, `workflow-runner.py`). An unmeasured run records `cost.measured: false` and is flagged, never treated as free. |
| Iteration budget | Per-loop `max_iterations`; enforced in code. | Yes (`_run_loop_pass`, `workflow-runner.py`). |
| Stagnation | Delta over `convergence.window`; enforced in code when diagnostics are structured. | Yes (`_run_loop_pass` → `_stagnant`). "When structured" is the real limit: the signature is each member's `evidence` or else its `verdict`, JSON-encoded (`_stagnant`), so a node reporting neither is treated as having an empty, constant signature. |
| Write ownership | Parallel writers must write disjoint `fields`. | **Static check only.** `_check_parallel` flags duplicate `outputs` across members (`scripts/validate-workflows.py:262-271`). There is no merge-time check because there is no merge step (Section 2.7). |
| Handoff integrity | A corrupted or tampered handoff is detected, not propagated. | **Partly enforced.** `handoff.sha` is *written* and never *compared*, and cannot be (it covers the sender's live node record, which is rewritten after the hop). `handoff.integrity` — a frozen snapshot + digest — **is** verified at send time and on every `--state` resume; a mismatch aborts with `StateCorruption` naming the hop. It does not cover edits to `nodes[...]`. See Section 4.1 for the detects/does-not-detect split. |
| Idempotency | Re-running a `done` node is a no-op; checkpoints make runs resumable. | Resumability, yes: state is checkpointed via `save_state` after every node, and a resumed run seeds `done` from the state file (`Runner.run`). The `force: true` opt-out **does not exist** — the runner has no `force` key; re-running a completed node is unconditionally a no-op. |

Guardrails are code because prompts are advisory. Multi-agent-orchestration lists these as
*guidance*; the rows marked "enforced" here are *mechanisms*. The rows marked validator-only or not
enforced are neither — they are stated intent, and a consumer planning around them should not.

### 4.5 Declared but not yet implemented

This is the table a consumer should read before trusting any field above. Each row is a key that the
validator accepts (and in most cases checks) but the runner never reads, verified by grepping
`scripts/workflow-runner.py` for the key name: **a zero count means the runner cannot act on it.**

| Declared contract | Where declared | Runner reads it? | Effect today |
|-------------------|----------------|------------------|--------------|
| `nodes[].inputs` | schema `nodes.item_fields.inputs` | No | None. Inputs are never checked against `fields`/`artifacts` before a node runs. |
| `nodes[].outputs` | same | No (validator only) | A node's declared `outputs` are never written to run-state by the runner; the executor writes artifacts directly. `_check_parallel` uses them for the disjointness check. |
| `nodes[].max_iterations` | schema `nodes.item_fields.max_iterations` | No (as a node field) | Node-level revision bounds do not exist. `_contract_rework_budget` reads the key only to compute a *floor* for `--contract-rework`; loop revision is governed by `loops[].max_iterations`. |
| `nodes[].on_exhaustion` | schema `nodes.item_fields.on_exhaustion` | No | Zero occurrences in the runner. Exhaustion routing is `loops[].escalate_to` only. |
| `nodes[].escalate_to` | schema `nodes.item_fields.escalate_to` | No | Zero occurrences as a node-level read. Only `loops[].escalate_to` and `gates[].escalate_to` are honoured. |
| `nodes[].executor` | schema `nodes.item_fields.executor` | No | The executor is chosen by the `--executor` CLI flag for the whole run; there is no per-node handler dispatch. |
| `type: supervisor` (+ `workers`, `routing`, `select`) | schema `nodes.item_fields` | No | Validated (`_check_supervisors`, `scripts/validate-workflows.py:314-329`) then executed as an ordinary single-skill node. Section 2.5. |
| `type: task` | schema `nodes.item_fields.type` enum | No | Accepted as a node type; executed like any other node. |
| `gate.gate.pass_when` / `gate.gate.else_go` (auto gate) | schema `nodes.item_fields.gate` | No | Zero `else_go` occurrences; `pass_when` appears only in the runner's own self-test fixtures. An `auto` gate does not evaluate a condition or branch — verified: a gate with `pass_when: a.status == blocked` and `else_go: c` still passes through to its `always` edge and leaves `c` pending. |
| `gates[].pass_when` | schema `gates.item_fields.pass_when` | No | Syntax-checked by the validator (`_check_gates`); not evaluated at runtime. |
| `gates[].requires` | schema `gates.item_fields.requires` | No | A gate does not assert the named artifacts/fields exist before firing. |
| `parallel[].join: any \| majority` | schema `parallel.item_fields.join` | Stored, never branched on | Always behaves as `all`. Section 2.4. |
| `parallel[].outputs` merge | schema `parallel.item_fields.outputs` | Stored, never used | No merge happens; nothing is written to run-state at the join. |
| `control.state.merge` (flat: `state.merge`) | schema `control.state.fields.merge` | No | Zero `merge` references in either script. §2.7. |
| `meta.name` / `meta.version` / `control.*` (nested form) | schema top-level `meta:` / `control:` | No | The schema's nested names are **stale** — see the note at the head of `workflow-manifest.schema.yaml`. Both the validator (`data.get("name")`) and the runner read the **flat** top-level form. |

Conversely, these *are* live runner behaviours, and a consumer can rely on them: node `when`
conditions, `loops[].exit_when`, `loops[].max_iterations`, `loops[].escalate_to`,
`loops[].convergence`, `parallel` membership (as an `all`-join hold), `gates[].kind == "agent"` with
`pool`/`max_reroutes`/`escalate_to`, `budget.max_steps`, `budget.max_cost_usd`, per-node
checkpointing and resume, and the `--enforce-contracts` completion assertion.

## 5. Handoff Payload Registry

A handoff payload is the only thing that crosses a node boundary. It is produced by the upstream
node (EXIT template) and consumed by the downstream node (INTAKE template). It composes the five
context elements required by agent-handoff-protocol with the library's verification discipline.

**What the runner does with a payload (verified).** It selects the edge's `payload` name into the
`handoff` record and nothing more (`scripts/workflow-runner.py`, `_advance_from`). It does not read,
validate, hash, or compare payload *content*. Payload-name resolution is a static check: when a
manifest declares a `payloads:` block, every edge `payload` must be one of its keys
(`scripts/validate-workflows.py:468-485`). If a manifest declares **no** `payloads:` block, an
arbitrary payload name validates clean — so "unregistered payload names are a validation error" is
true only once a registry exists.

| Key | Required | Contents |
|-----|----------|----------|
| `status` | yes | `done` \| `blocked` \| `needs_review` \| `skipped` |
| `summary` | yes | ≤200 words: what was done, headline result |
| `artifacts` | yes | `[{name, path, sha, type}]` produced by the node |
| `decisions` | yes | Decisions made, with rationale (`[]` allowed) |
| `open_questions` | yes | What the next node must resolve/decide (`[]` allowed) |
| `constraints` | yes | `[{type, value, source, non_negotiable}]` — limits the receiver must not lose (`[]` allowed). A dropped `non_negotiable: true` entry is a handoff defect; see `agent-handoff-protocol` R2 and `references/state-schema-spec.md`. |
| `verification_evidence` | yes | Criterion → evidence mapping; empty = not done |
| `context` | yes | Files/lines read, assumptions, things tried and failed (error paths) |
| `budget` | yes | Tokens/steps/iterations used by this node |
| `next` | optional | Suggested downstream skill / action |

Named payload variants (e.g. `handoff-v1`) may be registered in a manifest under `payloads:` to fix
field requirements per edge. The `payloads` map is validated against the canonical key list above
(`scripts/validate-workflows.py:468-485`); the keys are not enforced against what an executor actually
emits. The list above and the validator's `CANONICAL_PAYLOAD_KEYS` (`validate-workflows.py:37-40`)
are asserted identical by `validate-workflows.py --selftest`.

**Intake contract** — the downstream node must, before doing anything else, answer: What did I
receive? What do I owe? What did upstream leave open? The `handoff-in` template asks exactly these
three questions and refuses to start work until `artifacts` and `open_questions` are acknowledged.
This is an executor obligation: the runner does not block intake on it.

## 6. Multi-Agent Mapping (hybrid model)

Canonical semantics are framework-agnostic. For teams that want hard guarantees from an engine, the
same manifest maps onto execution frameworks:

| Canonical concept | LangGraph | CrewAI | Google ADK |
|-------------------|-----------|--------|------------|
| Manifest | `StateGraph` definition | `Process.sequential` / hierarchical crew | `Workflow` (graph) or a prebuilt workflow agent |
| Node (skill) | Graph node calling the skill prompt | Task with agent bound to the skill | Node function/agent in `edges` |
| Edge `when:` | Conditional edge function | Task context / conditions | Router node emitting `route=[...]`; dict-dispatch edges |
| Loop with `exit_when` | Cycle with conditional break to `END` | Sequential loop in process | Loop workflow agent, or a cycle with a route out |
| Parallel + join | Fan-out nodes + reducer on shared state | `Process.hierarchical` | Parallel workflow agent; join node for fan-in |
| Gate (human) | `interrupt_before` | Human-in-the-loop task | Human-input graph step |
| Run-state | Typed state + checkpointer | Task outputs aggregation | Session state + events (with context compression/memory) |

`examples/workflow-runtime/references/langgraph-mapping.md` and `graph.py` scaffold translate the
flagship manifest 1:1. The scaffold is illustrative reference code, not a dependency of this repo.
For ADK, see `skills/13-specialized/multi-agent-orchestration/references/adk-patterns.md`.

## 7. Prompt-Engineering Layer (boundary templates)

Control flow is code; *judgment* is prompts. Six templates in `workflow/templates/` encode the
judgment calls at every boundary. Each template states: when to use, inputs it reads, behavior
rules, and the output marker the runner/log expects.

| Template | Boundary | Encodes |
|----------|----------|---------|
| `verify-node.md` | EXECUTE → VERIFY | Criterion ↔ evidence mapping; no evidence = not done; evidence list is mandatory output |
| `revise-iteration.md` | VERIFY → REVISE | Root-cause the last diagnostics; change approach; never repeat an identical action; external blocker ⇒ escalate |
| `handoff-out.md` | DONE | Writes the payload registry block (Section 5) as the node's terminal output |
| `handoff-in.md` | INTAKE | Acknowledge received/owed/open; refuse to start on missing artifacts |
| `escalate.md` | exhaustion / blocked | Full-context escalation report (tried, evidence, blockers, next) |
| `loop-reflect.md` | loop complete / run end | Expected-vs-actual comparison; learnings written to the decision ledger |

Two anti-patterns the templates exist to kill:

- **Premature done** — claiming completion without artifact-level evidence. Defeated by
  `verify-node.md`'s hard rule: *a completion criterion with no evidence is an open item, not a
  checkbox.*
- **Refinement death spiral** — REVISE passes that repeat the same action or polish past the exit
  condition. Defeated by `revise-iteration.md`'s *change-or-escalate* rule plus the code-level
  stagnation detector.

## 8. Progressive Adoption

| Level | What you get | What it costs |
|-------|--------------|---------------|
| **Default** (no changes) | Existing skills keep working exactly as today. | No loop/graph guarantees. |
| **Manifest only** | Graphs + loops + handoffs over existing skills; skills run in default mode (Verification section = criteria as an executor convention). | You author manifests; validator enforces shape. |
| **Manifest + node contracts** | Criteria become *assertable* rather than declarative: run with `--enforce-contracts` and `completion.evidence`/`completion.criteria` are checked. Artifact names, `iteration`, and `escalate_to` remain declarations the executor honours (Section 4.5). | You add `workflow:` blocks to the high-value nodes. |

Adoption is deliberately bottom-up: author a manifest for one real flow, add node contracts only to
the skills that flow uses, run the validators, and read the readiness split from
`python3 scripts/audit-library.py` (the "Workflow Readiness" row reports *declared / eligible* — 64
declared of 324 eligible as of this checkout). The flag `--workflow-readiness` is **not** a real
option on `audit-library.py`; its only flags are `--brief` and `--json`.

## 9. Verification Checklist

| # | Check | How to verify |
|---|-------|---------------|
| ☐ | Manifest schema honored | `python3 scripts/validate-workflows.py --manifest <file>` passes |
| ☐ | No undeclared cycles | Validator rejects (`_check_cycles`). The runner does **not** — run the runner only on validated manifests, or cycles are silently pruned rather than reported. |
| ☐ | Every loop bounded | Validator requires `exit_when` + `max_iterations`; runner enforces `max_iterations` |
| ☐ | Handoff payload names resolve | Registry names exist **when a `payloads:` block is present** (`_check_payloads`). The runner does not verify payload content or hashes — see Sections 4.1 and 5. |
| ☐ | Parallel writers disjoint | Static check on `outputs` inside `parallel` blocks (validator only; the runner has no merge step) |
| ☐ | Exhaustion targets exist | `escalate_to` resolves to a node id — loops and `kind: agent` gates only, not node-level `escalate_to` |
| ☐ | Templates applied at boundaries | Transcript walkthrough shows verify/revise/handoff/escalate markers |
| ☐ | Stagnation + step budget enforced in code | Runner fixture suite proves both paths (`python3 scripts/workflow-runner.py --selftest`) |
| ☐ | Completion contract asserted | Re-run with `--enforce-contracts`; an unsubstantiated completion must not be marked done |

## 10. Relationship to Existing Material

| Existing artifact | Role under this spec |
|-------------------|----------------------|
| `chain:` frontmatter + `skill-router.py` | Static capability graph; a *menu* of possible edges. Manifests are the *order*. |
| `agent-handoff-protocol` | Canonical handoff contract; Section 5 makes its payload machine-checkable. |
| `multi-agent-orchestration` | Topology guidance (supervisor/peer/swarm); Section 2.5 + 6 pin it to manifests. |
| Skill Verification sections | Default completion-criteria source when no `workflow:` block exists. |
| `examples/orchestra-platform/` | Narrative demonstration; `examples/workflow-runtime/` is the executable counterpart. |
| `evals/tier3-behavioral/` + `agent-eval-pipeline` | Behavioral proof that loops stop, escalate, and hand off correctly. |
