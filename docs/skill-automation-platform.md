# Skill Automation Platform — n8n-Class Orchestration, Skill-Superior Nodes

> **Version 1.0.0** — Design + gap plan answering one question: *can this library ship an n8n-class
> automation platform — visual graphs, event triggers, always-on runs, run history — where the node
> is not a fixed API call but a skill that reasons, verifies, and escalates?* This document is the
> architecture, the measured capability map, and the phased build plan. It is a design document:
> nothing here is built yet beyond what the "Have" column cites. Every capability claim carries the
> command that produced it, so any reader can re-measure rather than trust.
>
> Companions: [`WORKFLOW-SYSTEM.md`](../WORKFLOW-SYSTEM.md) (execution semantics: node contract,
> manifest, run-state, handoffs), [`BEYOND-LOOPS-GRAPHS.md`](../BEYOND-LOOPS-GRAPHS.md) (the
> post-loops frontier: memory, evals, self-improvement, observability, guardrails, retrieval).

## 0. The short answer

**Yes — and most of the hard part is already built.** n8n's value splits into nine primitives. This
library already implements the four *hard* ones (node contract, graph manifest, deterministic
engine, agentic node content) with semantics n8n does not have (verified completion, bounded loops,
escalation, edge guardrails). It is missing the four *operational* ones (triggers, always-on
service, run history/replay/approvals UI, credential+connector layer) and the *authoring* one
(visual builder).

So the build is not "port n8n." It is: **keep the engine, add a trigger/serve/observe shell, and
win on the thing that actually decides output quality — what a node *is*.** That is the axis this
plan optimizes, per the decision to prioritize agentic skill nodes.

| Question | Answer |
|----------|--------|
| Can we build it? | Yes — the engine, contract, and content layers exist and pass validation today |
| Is it a rewrite? | No — the missing work is additive (new `platform/` shell + 4 script surfaces) |
| Where do we beat n8n? | Node content: judgment, standards, verification criteria, escalation, domain breadth |
| Where does n8n still win? | Connector count, hosted SaaS, non-technical UX, community templates (§7) |
| What is the first shippable step? | Phase 1: prove the agentic node end-to-end, unchanged engine (§6) |

## 1. What n8n is, decomposed

n8n markets itself as one thing ("workflow automation"). Technically it is nine separable
primitives. Naming them separately is what makes an honest gap analysis possible — "we have n8n"
is meaningless, "we have primitives 2–4 and 6, and are missing 1, 5, 7–9" is a plan.

| # | Primitive | What it is in n8n | Why it matters |
|---|-----------|-------------------|----------------|
| 1 | **Trigger** | Workflow starts on an *event* — webhook, schedule/cron, app event, chat message | Automation means no human in the loop at start time |
| 2 | **Node** | A unit of work: typed inputs/outputs + configuration | The node is where quality is won or lost |
| 3 | **Connection** | Declared edge: node → node, with branch/merge semantics | Makes the process reviewable and diffable |
| 4 | **Data mapping** | Expressions reference upstream output (`$json.field`) | Nodes compose without copy-paste |
| 5 | **Credential store** | Secrets injected into nodes at run time, never stored in the graph | Needed for any real external action |
| 6 | **Execution engine** | Traverses the graph, retries, persists execution state | Deterministic bookkeeping, not vibes |
| 7 | **Run history** | Every execution recorded: per-node status, logs, retry, error workflow | Operability: you can debug and prove what ran |
| 8 | **Human-in-the-loop** | Wait/approval nodes: pause mid-run, resume on a human decision | Automation that keeps a human at the irreversible step |
| 9 | **Distribution** | Self-host or cloud; community nodes + template library | Adoption: someone else's graph as a starting point |

Two nuances worth stating, because they are where our superiority argument lives:

- **n8n's "AI Agent" nodes exist** (LangChain-wrapped LLM calls). They make an LLM call a node
  body. They do **not** give the node a standard to meet, verifiable completion criteria, a
  bounded revision budget, or an escalation target. In our terms, they are a level-1 node (§3).
- **n8n nodes are integrations.** Value comes from *number of connectors*. Our nodes are
  *judgments*. Value comes from *quality of reasoning and correctness guarantees*. These are
  different products that overlap on primitives 1, 3, 6, 7.

## 2. Measured capability map

Every "Have" entry is an artifact in this repo at this HEAD. Every number is reproducible with the
command shown. Counts are as measured; where README/`package.json` state a slightly older count
(303 vs. 304), the measured value is used here.

| Primitive | Status | Have (artifact) | Residual gap |
|-----------|--------|-----------------|--------------|
| 2 · Node | **Have** | 304 `SKILL.md` under `skills/` (`find skills -name SKILL.md \| wc -l`); 301 eligible as default-mode nodes, 30 with declared `workflow:` contracts (`python3 scripts/validate-workflows.py --coverage`) | Node *contract* coverage is 10%: the criteria/evidence/budget/escalation semantics live only on 30 skills; the other 271 rely on their Verification section as the fallback source |
| 3 · Connection | **Have** | Executable graph manifests in `workflow/manifests/*.yaml` (6 library manifests) + schema `workflow/schema/workflow-manifest.schema.yaml`; validated by `python3 scripts/validate-workflows.py --all` (structure, cycle rejection, loop budgets, payloads, reachability) | Manifest shapes beyond serial/parallel/loop/gate (e.g. dynamic fan-out at run time) are not expressible |
| 4 · Data mapping | **Partial** | Canonical handoff payload registry (`control.payloads` in the manifest schema) + `workflow/templates/handoff-{in,out}.md` + payload sha checks at the boundary | No expression language: mapping is by named artifact, not a computed expression over upstream state |
| 6 · Execution engine | **Have** | `scripts/workflow-runner.py` — traversal, per-loop `max_iterations`, stagnation detection, global step budget, checkpoint/resume, parallel join, `--memory`, `--guardrail` | No retry-with-backoff policy per node; no priority/queue semantics (needed for §5 A2) |
| 6b · Real node content | **Have** | `scripts/executors/agent_executor.py` — calls a real agent CLI per node (`AGENT_CMD`, any backend: claude/gemini/codex/ollama), and injects the node's referenced skill into the prompt so every node is skill-grounded | Cost/latency per node are not reported back into run-state (traces carry 0 placeholders) |
| 6c · Edge guardrails | **Have** | `scripts/lib/guardrails.py` `classify(node_id, result, state)` called before a payload is recorded/handed off; per-node `safety:` policy overrides the runner global | Classifiers are heuristic demo detectors, not a model-based safety boundary (documented as such) |
| 7 · Run history | **Partial** | Durable run-state checkpoints (`--state`) + `scripts/export-traces.py` (OTel-shaped spans: `session.<workflow>`, `workflow.<w>.node.<id>`) + `scripts/skill-sli-report.py` (per-workflow SLIs + escalation-rate CI gate) | No run *index*, no inspect/replay/retry-from-node command, no page over past runs — history is files you name yourself |
| 1 · Trigger | **Gap** | — | Nothing starts a workflow except a manual/agent invocation |
| 5 · Credentials | **Gap** | — | No secret store, no scoped injection, no connector contract |
| 8 · Human-in-the-loop | **Partial** | Gate nodes (`type: gate`, `kind: human\|auto\|agent`) already halt and route runs; exhaustion escalates to a gate rather than stopping silently | Gates require a live operator attached to the running process; no pending-approval queue, no resume-after-pause, no approval surface |
| 9 · Distribution | **Partial** | `scripts/emit-marketplace.py` + `plugins/` (39 domain bundles) + `scripts/install.sh`, `scripts/npx-skills.sh`, `scripts/project-init.sh` (scaffolds `.agent/` into ANY repo) + cross-agent flat layer `skills-flat/` (304) for every agent's scanner | No public template gallery of *workflows* (manifests are shareable as files but not browsable/installable as such) |

Raw evidence for the rows above (run from the repo root):

```bash
find skills -name SKILL.md | wc -l                      # 304
ls skills-flat | wc -l                                  # 304
ls .skills-compiled | wc -l                             # 303
ls workflow/manifests/*.yaml | wc -l                    # 6
find workflow/tests/fixtures -name '*.yaml' | wc -l     # 11 fixtures
python3 scripts/validate-workflows.py --coverage        # 304 distinct names / 304 resolve / 301 eligible / 30 declared
python3 scripts/validate-workflows.py --all             # all manifests OK
python3 scripts/audit-library.py                        # Workflow Readiness: 30 declared / 301 eligible
```

### 2.1 What the existing visual surface actually is

`docs/graph-explorer/` is generated by `scripts/emit-skill-graph.py` and published as a
self-contained page (`index.html` + `graph-explorer.js` + `skill-graph.json`). It is a **read-only
viewer**: pan/zoom, search, and a path-finder between two skills. It has no editing model and no
manifest concept — it renders the `chain:` dependency graph, not a runnable workflow. That is the
distinction behind "builder is a gap": our explorer answers *"how are skills related?"*, n8n's
canvas answers *"what will run, in what order, with what data?"*

## 3. The superiority thesis — the node is the product

> **Decision recorded:** the priority axis for this platform is **agentic skill nodes — domain
> expertise that reasons inside the node, not just an API call.** Everything in §6 Phase 1 serves it.

An n8n node is a configured request: fixed endpoint, fixed parameters, mapping from upstream data.
Its intelligence is *outside* the platform. A skill node carries its own standards, judgment,
failure modes, and definition of done:

| Dimension | n8n node (incl. AI Agent node) | Skill node (this library) |
|-----------|-------------------------------|---------------------------|
| Body | Deterministic API call, or one LLM call | A reasoning procedure with steps, rules, and domain rules-of-thumb |
| Definition of done | Node succeeded / errored | Verification criteria + required evidence (`workflow.completion`) |
| Failure behavior | Error, retry, error workflow | Bounded revision within `iteration.max`, then `escalate` to a named gate |
| Quality control | Retry on transient failure | Criteria-with-evidence, edge guardrails, review gates |
| Breadth | N API connectors | 30+ domains of professional judgment (legal, finance, security, health, growth, …) |
| Cost control | Per-execution pricing tiers | Global step budget + per-loop iteration budget + efficiency skills |
| Improvement | You rewrite the node config | Eval-gated skill evolution, run memory, trace-driven promotion |
| Reviewability | JSON of credentials + parameters | Prose contract a non-engineer can review and a validator can check |

### 3.1 Node-quality ladder

```
L0  stub            ── runner default: no content, exercises control flow      (test-only)
L1  integration     ── fixed API call / single LLM call                        (n8n's ceiling for AI)
L2  skill-grounded  ── agent runs the node's SKILL.md procedure                (301 skills today)
L3  verified node   ── L2 + declared criteria/evidence + bounded loop
                       + named escalation target                              (30 skills today)
```

n8n tops out at L1. This library's floor for a real run is L2, and L3 is a frontmatter block away
from any skill. **The platform work in Phase 2+ does not raise node quality — it raises node
*operability*.** That is why Phase 1 comes first and needs no new platform code.

Interfaces that already exist and make L3 checkable:

```bash
# lint a node contract
python3 scripts/lib/lint-workflow.py <domain>/<skill>/SKILL.md
# prove a manifest is executable and correctly shaped
python3 scripts/validate-workflows.py --all
# run it headless (stub content) or with a real agent per node
python3 scripts/workflow-runner.py --manifest workflow/manifests/<name>.yaml
AGENT_CMD='claude -p' python3 scripts/workflow-runner.py \
    --manifest workflow/manifests/<name>.yaml \
    --executor scripts/executors/agent_executor.py \
    --guardrail scripts/lib/guardrails.py --memory ./agent-memory
```

## 4. Target architecture

The platform is described as layers P0–P7. Lowercase `Have` marks the layers that exist today;
each gap layer maps to an A-item in §5 and a phase in §6. The rule inherited from
`WORKFLOW-SYSTEM.md` holds unchanged: **control flow is deterministic code; content is agentic.**

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ P7  DISTRIBUTION   plugins/ · marketplace emit · template gallery      GAP →  A9 │
├──────────────────────────────────────────────────────────────────────────────┤
│ P6  AUTHOR         visual builder → validated manifest                 GAP →  A6 │
│                    (viewer exists: docs/graph-explorer/)                          │
├──────────────────────────────────────────────────────────────────────────────┤
│ P5  OPERATE        run index · inspect · replay/retry-from-node ·      GAP →  A3 │
│                    approval inbox · trace/SLI page                     A5, A8    │
│                    (spans + SLIs exist as scripts/CLI)                            │
├──────────────────────────────────────────────────────────────────────────────┤
│ P4  SERVE          always-on service: scheduler + worker + HTTP API    GAP →  A1 │
│                    (self-hosted, stdlib-only)                          A2         │
├──────────────────────────────────────────────────────────────────────────────┤
│ P3  EXECUTE    ✅  workflow-runner.py — loops, budgets, checkpoints,              │
│                    guardrails, memory, parallel join, resume                      │
├──────────────────────────────────────────────────────────────────────────────┤
│ P2  CONTENT    ✅  executors/agent_executor.py — real agent CLI per node,         │
│                    skill-grounded prompt (the "superior node" leg)                 │
├──────────────────────────────────────────────────────────────────────────────┤
│ P1  CONTRACT   ✅  workflow/manifests/*.yaml + schema + validator                 │
├──────────────────────────────────────────────────────────────────────────────┤
│ P0  LIBRARY    ✅  304 SKILL.md · chain graph · handoff protocol · personas       │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Invariants for every layer above P0** (non-negotiable; they are why this is not a rewrite):

1. **Stdlib-only core.** No Node, no npm, no broker, no database server. n8n needs Node + Postgres
   for anything serious; this platform must run with Python 3 and a directory of files.
2. **File-first state.** Every run is a JSON checkpoint you can read, diff, commit, or archive.
   The service layer indexes files; it never becomes the source of truth.
3. **Agent-agnostic.** Node content goes through `AGENT_CMD`. No layer may hard-code one vendor.
4. **Content stays in the library.** The platform adds no new place to put a prompt. Node bodies
   are `SKILL.md`, referenced by name, so the whole audit/eval/quality apparatus keeps applying.
5. **Deterministic where it can be.** Traversal, budgets, retry, resume, and indexing are code;
   only node content is probabilistic.

## 5. Gap register

Each item names the gap, the artifact to build, where it plugs into existing machinery, and the
acceptance bar that proves it. IDs `A1..A9` are referenced by §6 phases.

### A1 — Trigger layer (primitive 1)

- **Gap.** No workflow can start from an event. Entry is always a human or an agent invocation.
- **Build.** `workflow/schema/trigger.schema.yaml` + `platform/triggers/` with three first
  triggers: `schedule` (cron expression), `webhook` (HTTP POST payload → run-state fields),
  `git` (post-commit / tag via the existing `.githooks/` install path). Extend the manifest with an
  optional `triggers:` block; extend `scripts/validate-workflows.py` to validate it (Safe-YAML
  subset: single-line scalars, no anchors).
- **Plugs into.** `workflow/manifests/` (declaration), `scripts/workflow-runner.py` (invocation),
  `.githooks/` + `scripts/install-hooks.sh` (git trigger delivery).
- **Acceptance.** A manifest declaring `triggers: [schedule, webhook]` passes the validator; a
  `--trigger` invocation starts the same run-state a manual run produces; a fixture suite covers
  malformed cron and unauthenticated webhook.

### A2 — Always-on service (primitive 6, operational shell)

- **Gap.** The runner is one-shot. There is no scheduler, no worker, no queue, no API.
- **Build.** `scripts/skill-automationd.py` — stdlib `http.server` API + interval scheduler +
  worker loop that spawns `workflow-runner.py` per due trigger, writes a run index, and exposes
  `GET /runs`, `POST /run/<manifest>`, `GET /health`. Single-writer file lock over the runs dir.
- **Plugs into.** `scripts/workflow-runner.py` (unchanged CLI, invoked as a subprocess or import),
  `scripts/project-init.sh` (service scaffold into any project's `.agent/`).
- **Acceptance.** Service starts with zero third-party dependencies; a `schedule` trigger fires a
  manifest at its interval; killing the service mid-run leaves a resumable checkpoint; a second
  concurrent run of the same manifest is serialized by the lock, not corrupted.

### A3 — Run store + inspect/replay (primitive 7)

- **Gap.** History is unnamed files; there is no index, no inspect, no replay, no retry-from-node.
- **Build.** `runs/<workflow>/<run-id>.json` + `runs/index.jsonl`; `scripts/run-inspect.py`
  (`--run <id>`, `--timeline`, `--diff <other-run>`); `scripts/workflow-runner.py --resume-from
  <node>` (checkpoint machinery already supports resume — this adds a node anchor).
- **Plugs into.** Existing `--state` checkpoints, `scripts/export-traces.py`,
  `scripts/skill-sli-report.py`.
- **Acceptance.** `run-inspect --diff` shows the node where two runs diverged; `--resume-from`
  re-enters at the named node without re-running completed nodes; the index is append-only and
  rebuildable from the checkpoint files alone (proved by deleting it and regenerating).

### A4 — Human-in-the-loop wait/resume (primitive 8)

- **Gap.** Gate nodes halt the *process*, so a human must be attached to the running terminal. No
  pending-approval queue, no resume-after-pause, no approval surface.
- **Build.** Gate nodes of `kind: human` write a `pending_approval` record and **exit cleanly**
  instead of blocking; `scripts/run-approve.py --run <id> --gate <node> --decision approve|reject
  --note "..."` records the decision and resumes the run. Optional notification hook (reuse
  `hooks/`), and the decision is written into the durable run memory.
- **Plugs into.** Existing gate/escalation semantics in `workflow-runner.py`, `--memory` (B1),
  `workflow/templates/escalate.md`.
- **Acceptance.** A run reaches a human gate, exits 0 with status `awaiting-approval`, resumes on
  decision, and `reject` routes to the gate's declared alternative — with the decision visible in
  run-state, the trace, and the run index.

### A5 — Credential + connector layer (primitive 5)

- **Gap.** No secret store; nodes cannot make authenticated external calls with scoped credentials.
- **Build.** `.agent/secrets.env` (git-ignored by default) loaded into the runner environment per
  node, with a **per-node allow-list** declared in the manifest (`credentials: [stripe, github]`)
  so a node sees only what it declares. A connector skill contract (a `SKILL.md` shape) for
  reusable, credentialed actions, so connectors are skills — reviewable and eval-gated — not a
  separate plugin runtime.
- **Plugs into.** `scripts/executors/agent_executor.py` (env injection), `workflow/schema`
  (`credentials:` field), `scripts/validate-workflows.py` (declared-vs-used check),
  `scripts/lib/guardrails.py` (block a node that touches an undeclared secret).
- **Acceptance.** A node using an undeclared credential is blocked by the guardrail and the run
  escalates; no secret value appears in any run-state, trace, or log (asserted by a test that greps
  the run artifacts for the secret).

### A6 — Visual builder (primitive 3, authoring)

- **Gap.** `docs/graph-explorer/` views the static `chain:` graph. No canvas authors a workflow.
- **Build.** An **author mode** for the explorer: drag skill nodes, draw edges, set gate/loop
  fields, then **emit a manifest** and run `validate-workflows.py` in-page-adjacent (via the
  existing CI script) before offering the download. Reuses `skill-graph.json` as the node palette
  and the manifest schema for field definitions, so the builder cannot produce an invalid manifest.
- **Plugs into.** `scripts/emit-skill-graph.py` (palette data), `workflow/schema`
  (field constraints), `scripts/validate-workflows.py` (the gate before export).
- **Acceptance.** A graph drawn in the browser yields a manifest that passes `validate-workflows.py
  --all` unmodified; every schema enum is exposed as a control (no free-text where an enum exists);
  the generated manifest is byte-stable across two exports of the same graph.

### A7 — Live observability surface (primitive 7, UI)

- **Gap.** Spans and SLIs exist as CLI output. There is no view of a run in progress or of history.
- **Build.** `docs/run-explorer/` — a static page generated from `runs/` (index + checkpoints +
  spans): run list, per-node timeline, verdict/evidence per node, escalation markers, cost/latency
  once executors report them. Same generator discipline as the graph explorer (`--check` freshness
  gate, deterministic output).
- **Plugs into.** `scripts/export-traces.py`, `scripts/skill-sli-report.py`, A3's run index.
- **Acceptance.** `scripts/emit-run-explorer.py --check` fails when committed output is stale (CI
  gate parity with `emit-skill-graph.py --check`); a run with an escalation is visually distinct
  from a clean run without reading logs.

### A8 — Trigger-aware node contract (primitive 2, extended)

- **Gap.** Node contracts declare artifacts/criteria/budget/escalation but not how a node may be
  entered, and coverage is 30 of 301 eligible skills.
- **Build.** Add optional `workflow.triggers`/`workflow.credentials` to the node-contract YAML;
  extend `scripts/lib/lint-workflow.py`; then **raise declared coverage** on the delivery-hub
  skills that library manifests actually exercise, in batches, each proven by
  `scripts/lib/lint-workflow.py` + `validate-workflows.py --coverage`.
- **Plugs into.** `scripts/lib/lint-workflow.py`, `scripts/audit-library.py` (Workflow Readiness
  dimension), `WORKFLOW-SYSTEM.md` §1 (must be updated in the same change).
- **Acceptance.** Workflow Readiness moves off 30 declared; every newly declared skill's criteria
  are checkable against its Verification section (no criteria invented that the skill cannot show
  evidence for).

### A9 — Workflow gallery (primitive 9)

- **Gap.** Manifests are shareable as files but not discoverable, browsable, or installable.
- **Build.** A generated `workflow/gallery.md` + machine index (`workflow/gallery.json`) from every
  manifest: shape, skills used, gate count, budget, and the one-line "what this proves". Wire into
  `scripts/emit-marketplace.py` so plugins ship the workflows alongside the skills.
- **Plugs into.** `workflow/manifests/`, `scripts/emit-marketplace.py`, `plugins/`, README table.
- **Acceptance.** The gallery is regenerable and freshness-checked in CI; every manifest appears
  exactly once; installing a domain plugin makes its workflows discoverable with no extra step.

## 6. Phased roadmap

Phases are independently shippable and ordered by the recorded priority: **node quality first, then
operability.** Each phase lists its acceptance bar; a phase is done only when its commands pass.

### Phase 1 — Prove the agentic node (priority axis; no new platform code)

> **Status: Phase 1 delivered** — see
> [`examples/phase1-agentic-node/`](../examples/phase1-agentic-node/README.md). One real run of
> `senior-dev-loop` with `AGENT_CMD='claude -p'` and `AGENT_FALLBACK=0`: 3 real agent turns
> (no fallback), grounded in 405- and 1,200-word skill excerpts, outcome `complete`,
> effectiveness **100/100**, SLI escalation rate **0.00**. Item 3 (the L2→L3 delta, documented
> with its honest limit) and item 4 (declared contracts **30 → 43** skills) are also delivered.
>
> That run also produced three defects, now fixed: **D1** (`AGENT_TIMEOUT` default 90s was below
> the measured 149.6s per node → raised to 600s), **D2** (a node raising inside a loop pass
> discarded the entire run-state, so a crashed run could not be resumed → `_crash_checkpoint()`
> + per-node checkpoints + a `--selftest` regression fixture), and **D3** (`save_state` wrote no
> final newline, so any committed run-state failed the repo's own FMT004 gate). D2 is why the
> acceptance bar below can be trusted: the first attempt failed and lost everything.

Goal: demonstrate, end to end and reproducibly, that a node in this library is an L3 skill node —
not an API call — using only machinery that exists today.

1. Run one library manifest with the **real** agent executor and the guardrail + memory flags;
   archive the run-state, trace, and SLI report under `examples/`.
2. Record the same manifest's 0-100 effectiveness score
   (`python3 scripts/run-effectiveness.py`) and the SLI escalation rate.
3. Document the L2→L3 delta on one skill: same task, default-mode node vs. declared-contract node,
   with the evidence difference shown (criteria coverage, evidence completeness).
4. Close A8 partially: declare contracts on the highest-traffic delivery-hub skills, in batches,
   each batch proven by `scripts/lib/lint-workflow.py` and `--coverage`.

**Acceptance.** `python3 scripts/run-effectiveness.py` reports a gateable score for the run;
`python3 scripts/skill-sli-report.py --gate-escalation <threshold>` passes; `--coverage` shows a
declared count above 30; all existing manifests still pass `validate-workflows.py --all`.

### Phase 2 — Triggers and the always-on service (A1, A2)

**Acceptance.** Service runs with stdlib only; a `schedule` and a `webhook` trigger each start a
real manifest; kill/resume leaves no lost or duplicated run; validator rejects malformed triggers.

### Phase 3 — Operate the runs: history, replay, approvals (A3, A4, A7)

**Acceptance.** A human gate pauses a run, exit code is clean, an approval resumes it; replay/retry
from a node works; the run explorer is generated, freshness-checked, and shows escalations.

### Phase 4 — Act on the world: credentials, connectors, gallery (A5, A9)

**Acceptance.** No secret leaks into any run artifact (grepped by test); undeclared credential use
escalates; connector skills pass the same eval gates as every other skill; the gallery is
regenerable, freshness-checked, and shipped inside domain plugins.

### Phase 5 — Author visually (A6)

**Acceptance.** A browser-authored graph produces a manifest that passes validation unmodified, and
the builder cannot express an invalid graph (schema enums drive every field).

## 7. Honest comparison — where n8n still wins

A superiority claim that omits this is marketing, not engineering.

| n8n advantage | Our position |
|---------------|--------------|
| **Hundreds of maintained connectors** | We ship judgment, not 400 integrations. The credible answer is connectors-as-skills (A5) plus MCP-style external tool servers — fewer, higher-quality, eval-gated connections |
| **Hosted SaaS, zero-setup** | By design we are self-hosted and file-first (a feature for regulated/offline work; a cost for a non-technical user) |
| **Non-technical UI** | Our authoring surface (A6) targets someone who can read a manifest — not a no-code audience. That is a scope choice, not a limitation to fix |
| **Community template library** | A9 gets us a gallery of *reviewed* workflows; it will not match community volume |
| **Enterprise RBAC/SSO/audit** | Out of scope for this library; the audit trail we do have is stronger on *content* (verdicts, evidence, escalation reasons) than on user permissions |

## 8. Non-goals

- **Not a hosted product.** No SaaS, no accounts, no telemetry phone-home.
- **No new runtime dependency.** Python 3 stdlib + files. No Node, no npm, no Postgres, no broker.
- **No second place to put prompts.** Node content stays `SKILL.md`; the platform never becomes a
  prompt store, so the audit/eval/quality machinery keeps applying to everything.
- **No vendor coupling.** Every layer goes through `AGENT_CMD`; adding or removing an agent CLI
  changes no platform code.
- **Not a rewrite of `WORKFLOW-SYSTEM.md`.** P1–P3 semantics are frozen; this plan only adds layers
  above them and extends the schema additively.

## 9. How to prove the plan (reproduce everything in this doc)

```bash
# capability map (§2)
find skills -name SKILL.md | wc -l                     # 304
python3 scripts/validate-workflows.py --coverage       # 304 names / 304 resolve / 301 eligible / 30 declared
python3 scripts/validate-workflows.py --all            # every manifest OK
python3 scripts/audit-library.py                       # Workflow Readiness: 30 declared / 301 eligible

# engine + node content exists (§2, §3)
python3 scripts/workflow-runner.py --selftest
python3 scripts/workflow-runner.py --manifest workflow/manifests/senior-dev-loop.yaml

# observability primitives exist as CLI (§2, A3/A7 inputs)
python3 scripts/export-traces.py --state examples/workflow-runtime/state/happy-run-state.json
python3 scripts/skill-sli-report.py --dir examples/workflow-runtime/state

# the superiority claim, end to end (Phase 1)
AGENT_CMD='claude -p' python3 scripts/workflow-runner.py \
    --manifest workflow/manifests/senior-dev-loop.yaml \
    --executor scripts/executors/agent_executor.py \
    --guardrail scripts/lib/guardrails.py --memory ./agent-memory
```

## 10. Status

| Layer | Today | After this plan |
|-------|-------|-----------------|
| P0 Library | 304 skills, chain graph, handoff protocol | unchanged |
| P1 Contract | 6 manifests + schema + validator; 30 declared contracts | + triggers, credentials, A8 coverage growth |
| P2 Content | real agent executor, skill-grounded, per-node | + cost/latency reporting into run-state |
| P3 Execute | loops, budgets, checkpoints, guardrails, memory, resume | + `--resume-from <node>` |
| P4 Serve | — | scheduler + worker + HTTP API (stdlib) |
| P5 Operate | spans + SLIs as CLI | run index, inspect/replay, approval inbox, run explorer |
| P6 Author | read-only graph viewer | author mode → validated manifest |
| P7 Distribution | plugins + install for 39 domains | + workflow gallery shipped in plugins |

**Enforcement now exists, but it is opt-in.** The limit item 3 documented — that the engine read only
a node's skill *name* and never asserted declared criteria — was closed subsequently:
`workflow-runner.py --enforce-contracts` requires `evidence: required` to be satisfied and every
declared criterion to be covered by the node's `criteria_met` report, refusing to mark an
unsubstantiated node done (retrying inside a loop, escalating outside one). It is **off by default**
because most executors do not yet report per-criterion coverage, so an L3 contract is not enforced
unless you ask for it. Evidence: 4 dedicated self-tests (suite 12 → 16 checks, 0 failed), and a live
A/B on `senior-dev-loop` where the effectiveness score fell from 95/100 to 45/100 once enforcement
was on. Phase 2 (A1 triggers, A2 always-on service) is the first work that needs new platform code.
