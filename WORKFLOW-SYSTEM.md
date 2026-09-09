# Workflow System — Loops, Graphs, and Smooth Handoffs Over the Skill Library

> **Version 1.0.0** — Canonical specification for executing the skill library as graphs and loops:
> iterate until done, hand off state without loss, escalate instead of looping forever or stopping early.
> Portable across Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI. No framework required at the
> canonical level; optional mappings to LangGraph/CrewAI are documented and demonstrated in
> `examples/workflow-runtime/`.

## Why This Exists

The library already has a **static graph** (the symmetric `chain:` dependency DAG, 1,130+ edges,
exported by `scripts/skill-router.py`) and **prose workflows** (each skill's Core Workflow +
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
| Completion drives loops | `completion.criteria` are the *verifiable* claims; `iteration.max` bounds revision; `on_exhaustion` decides the exhausted outcome. |
| Escalation is a target, not a feeling | `escalate_to` names a gate node id in the manifest or a skill name. If neither exists, exhaustion = report with full context, no further looping. |
| Verification section is the fallback | No `criteria` → the node's Verification / Production Checklist tables are treated as the criteria source at execution time. |

Why criteria-with-evidence? A node that cannot say what "done" means cannot be looped safely. The
single most expensive failure in agent workflows is **premature completion** — declaring done with
zero evidence. The second is **infinite refinement** — polishing past the point of return. The node
contract exists to make both detectable by construction.

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

| Invariant | Why |
|-----------|-----|
| Every loop has `exit_when` + `max_iterations` | No unbounded repetition by construction. |
| `max_iterations >= 1` | A loop is a loop. |
| Exhaustion target exists | `escalate_to` must resolve to a node id in the same manifest. |
| No node appears in two active loops | Nested/overlapping loops are ambiguous; flatten instead. |
| Stagnation detector optional, default on | Identical consecutive passes produce no new information; keep looping = burning budget. |

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

### 2.6 Condition vocabulary (edges and loops)

Conditions are deliberately small. Executors and the runner interpret exactly this vocabulary; the
validator checks syntax only:

| Form | Meaning |
|------|---------|
| `always` | Unconditional. |
| `NODE.status == done` / `!= done` | Node terminal status (done, blocked, needs_review, skipped). |
| `NODE.status in (a, b)` | Membership on terminal status. |
| `NODE.verdict == VALUE` | Verdict equality (strings only). |
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

## 3. Safe YAML Subset

Manifests and `workflow:` frontmatter blocks are YAML — but a **documented subset** that a
dependency-free validator and runner can parse safely:

- Scalars: strings (quoted or bare alphanumerics, `-`, `_`, `/`, `.`, `==`, `,`, spaces), integers,
  booleans (`true`/`false`).
- Scalar-only flow lists: `[a, b, c]` as a value (no nesting, no flow maps).
- Structures: indentation-based maps and lists, one structural level deep inside each list item.
- Comments (`#`) allowed on their own lines or trailing a value.
- No anchors/aliases, no flow maps, no block scalars (`|`, `>`), no multi-document files.

The normative parser is `scripts/lib/safe_yaml.py` (stdlib-only, ~90 lines) — one file shared by
`scripts/validate-workflows.py`, the frontmatter lint, and `scripts/workflow-runner.py`. The schema
files in `workflow/schema/` document fields; validation logic lives in the scripts and is exercised
by their fixture suites.

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
  "iteration": 1,
  "budget": { "max_steps": 40, "steps_used": 7, "iterations": { "review-fix-loop": 1 } },
  "nodes": {
    "code-reviewer": { "status": "done", "verdict": "changes_requested", "iterations": 1,
                       "evidence": ["review.md"], "summary": "…", "sha": "…" }
  },
  "fields": {
    "findings": { "value": [{"severity": "high", "file": "src/auth.py", "note": "…"}],
                  "writer": "reviewers", "sha": "…" }
  },
  "artifacts": { "review.md": { "path": "artifacts/review.md", "sha": "…", "type": "doc" } },
  "decisions": [ { "at": "code-reviewer", "what": "auth refactor required", "by": "code-reviewer" } ],
  "open_questions": [],
  "handoff": { "from": "fixer", "to": "reviewers", "payload": "handoff-v1", "sha": "…" },
  "log": [ { "step": 7, "node": "code-reviewer", "action": "verify", "verdict": "changes_requested" } ]
}
```

Every write by a node updates `updated`, appends to `log`, and re-hashes `nodes`, `fields`,
`artifacts` (short `sha`). The runner compares hashes across a handoff — a mismatch aborts with a
state-corruption error instead of propagating bad state (agent-handoff-protocol rule: no handoff
without state-hash verification).

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

### 4.3 Loop protocol (the heart of "iterate until done")

1. **Pass N runs**: execute the loop's nodes in order against current run-state.
2. **Exit check**: evaluate `exit_when`. True → loop complete; advance along the loop's continuation
   edges.
3. **Delta check** (stagnation): compare diagnostics with the previous pass. No delta for
   `convergence.window` passes → treat as exhaustion (looping identical work is budget burning).
4. **Budget check**: `iteration >= max_iterations` → exhaustion.
5. **Exhaustion**: follow `on_exhaustion`/`escalate_to` (default `escalate`). Escalation carries the
   full context: what was tried (per pass), evidence, remaining blockers, recommended next action.
6. Never stop silently mid-loop; never continue past budget; never repeat an identical pass
   (REVISE must change approach or inputs — the revise template enforces this).

### 4.4 Deterministic guardrails (runner-enforced, not prompt-requested)

| Guardrail | Mechanism |
|-----------|-----------|
| Cycle rejection | A node may not be its own ancestor except through a declared loop. Validator rejects undeclared cycles; runner tracks the active node stack. |
| Step budget | Global `budget.max_steps` hard cap; runner halts and reports when exceeded. |
| Iteration budget | Per-loop `max_iterations`; enforced in code. |
| Stagnation | Delta over `convergence.window`; enforced in code when diagnostics are structured. |
| Write ownership | Parallel writers must write disjoint `fields`; validated statically (manifest) and at merge time (runner). |
| Handoff hash | Every handoff payload hash is verified on receipt. Mismatch aborts, never propagates. |
| Idempotency | Re-running a `done` node is a no-op unless `force: true`; checkpoints make runs resumable. |

Guardrails are code because prompts are advisory. Multi-agent-orchestration lists these as
*guidance*; here they are *mechanisms*.

## 5. Handoff Payload Registry

A handoff payload is the only thing that crosses a node boundary. It is produced by the upstream
node (EXIT template), verified by the runner, and consumed by the downstream node (INTAKE template).
It composes the five context elements required by agent-handoff-protocol with the library's
verification discipline.

| Key | Required | Contents |
|-----|----------|----------|
| `status` | yes | `done` \| `blocked` \| `needs_review` \| `skipped` |
| `summary` | yes | ≤200 words: what was done, headline result |
| `artifacts` | yes | `[{name, path, sha, type}]` produced by the node |
| `decisions` | yes | Decisions made, with rationale (`[]` allowed) |
| `open_questions` | yes | What the next node must resolve/decide (`[]` allowed) |
| `verification_evidence` | yes | Criterion → evidence mapping; empty = not done |
| `context` | yes | Files/lines read, assumptions, things tried and failed (error paths) |
| `budget` | yes | Tokens/steps/iterations used by this node |
| `next` | optional | Suggested downstream skill / action |

Named payload variants (e.g. `handoff-v1`) may be registered in a manifest under `payloads:` to fix
field requirements per edge. Unregistered payload names are a validation error.

**Intake contract** — the downstream node must, before doing anything else, answer: What did I
receive? What do I owe? What did upstream leave open? The `handoff-in` template asks exactly these
three questions and refuses to start work until `artifacts` and `open_questions` are acknowledged.

## 6. Multi-Agent Mapping (hybrid model)

Canonical semantics are framework-agnostic. For teams that want hard guarantees from an engine, the
same manifest maps onto execution frameworks:

| Canonical concept | LangGraph | CrewAI |
|-------------------|-----------|--------|
| Manifest | `StateGraph` definition | `Process.sequential` / hierarchical crew |
| Node (skill) | Graph node calling the skill prompt | Task with agent bound to the skill |
| Edge `when:` | Conditional edge function | Task context / conditions |
| Loop with `exit_when` | Cycle with conditional break to `END` | Sequential loop in process |
| Parallel + join | Fan-out nodes + reducer on shared state | `Process.hierarchical` |
| Gate (human) | `interrupt_before` | Human-in-the-loop task |
| Run-state | Typed state + checkpointer | Task outputs aggregation |

`examples/workflow-runtime/references/langgraph-mapping.md` and `graph.py` scaffold translate the
flagship manifest 1:1. The scaffold is illustrative reference code, not a dependency of this repo.

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
| **Manifest only** | Graphs + loops + handoffs over existing skills; skills run in default mode (Verification section = criteria). | You author manifests; validator enforces shape. |
| **Manifest + node contracts** | Strongest guarantees: typed artifacts, explicit criteria/iteration, named escalation. | You add `workflow:` blocks to the high-value nodes. |

Adoption is deliberately bottom-up: author a manifest for one real flow, add node contracts only to
the skills that flow uses, run the validators, measure readiness with the audit dimension
(`scripts/audit-library.py --workflow-readiness`).

## 9. Verification Checklist

| # | Check | How to verify |
|---|-------|---------------|
| ☐ | Manifest schema honored | `python3 scripts/validate-workflows.py --manifest <file>` passes |
| ☐ | No undeclared cycles | Validator rejects; runner never executes one |
| ☐ | Every loop bounded | Validator requires `exit_when` + `max_iterations` |
| ☐ | Handoff payloads resolve | Registry names exist; runner verifies hashes |
| ☐ | Parallel writers disjoint | Static check on `outputs` inside `parallel` blocks |
| ☐ | Exhaustion targets exist | `escalate_to` resolves to a node id |
| ☐ | Templates applied at boundaries | Transcript walkthrough shows verify/revise/handoff/escalate markers |
| ☐ | Stagnation + budget enforced in code | Runner fixture suite proves both paths |

## 10. Relationship to Existing Material

| Existing artifact | Role under this spec |
|-------------------|----------------------|
| `chain:` frontmatter + `skill-router.py` | Static capability graph; a *menu* of possible edges. Manifests are the *order*. |
| `agent-handoff-protocol` | Canonical handoff contract; Section 5 makes its payload machine-checkable. |
| `multi-agent-orchestration` | Topology guidance (supervisor/peer/swarm); Section 2.5 + 6 pin it to manifests. |
| Skill Verification sections | Default completion-criteria source when no `workflow:` block exists. |
| `examples/orchestra-platform/` | Narrative demonstration; `examples/workflow-runtime/` is the executable counterpart. |
| `evals/tier3-behavioral/` + `agent-eval-pipeline` | Behavioral proof that loops stop, escalate, and hand off correctly. |
