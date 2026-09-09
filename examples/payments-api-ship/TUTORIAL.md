# Developer Onboarding — How to Read, Run, and Extend the Skills Repo

> **Audience:** a developer or a "consumer" of this repository (you want to use these skills in
> your AI agent, or you want to build workflows out of them) who has never opened the repo.
> **Time:** ~45 minutes hands-on. You will finish able to: install the library, explain what a
> skill is, read a skill's dependency chain, run a real multi-agent workflow graph headlessly,
> interpret its traces, and wire your own skills into the same graph.
> **Working example throughout:** the **payments API ship** workflow in
> `examples/payments-api-ship/` — a realistic "take a feature from idea to production release".

---

## 0. The one-paragraph mental model

The repo is three layers stacked on each other:

```
┌────────────────────────────────────────────────────────────────────┐
│ 1  SKILLS  — ~300 markdown files, one per expertise                │
│    skills/05-development/backend-developer/SKILL.md                │
│    Each says: what it does, WHEN to use it, HOW to do the work,    │
│    and which other skills it depends on / feeds (chain:).          │
├────────────────────────────────────────────────────────────────────┤
│ 2  WORKFLOW MANIFESTS — YAML that turns chosen skills into a graph │
│    workflow/manifests/*.yaml, examples/*/*.yaml                    │
│    Each says: which skill-nodes run, in what order, in which       │
│    loops, and who gets the handoff / who approves (gates).         │
├────────────────────────────────────────────────────────────────────┤
│ 3  EXECUTOR — the thing that does one node's work                  │
│    scripts/executors/agent_executor.py   (real agent CLI)          │
│    scripts/executors/repo_checks.py      (deterministic gates)     │
│    examples/payments-api-ship/executor_demo.py (teaching stub)     │
└────────────────────────────────────────────────────────────────────┘
```

Rule that explains everything else: **layer 1 is content, layer 3 is also content
(doing), and layer 2 is pure control flow** ("control flow is code, content is agentic").
An AI agent reads a `SKILL.md` and does what it says; the workflow engine only decides
*which* skill runs next, how many times to retry, and who gets the result.

---

## 1. Install (so you can follow along)

Three ways, pick one:

```bash
# (a) One-shot installer — clones to ~/.zeroes-ones/skills and symlinks for your agents
curl -sSL https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh | bash

# (b) Activate inside a project afterwards (creates .claude/skills, .copilot/skills, ...)
cd your-project && skills-init          # default = full library; --solo=8 skills, --grow=18

# (c) Just clone the repo to read it (what this tutorial assumes)
git clone https://github.com/zeroes-ones/Skills.git && cd Skills
```

Verify install: `ls ~/.zeroes-ones/skills/skills/` should list `00-framework … 36-travel-adventure`
(37 domain folders). The **flat index** `skills-flat/` is a copy of every `SKILL.md` one level
deep — that is what most agents' skill scanners actually consume.

Where your agent looks (from `README.md`, "Supported Agents"):

| Agent | Skill directory | Invoke a skill with |
|---|---|---|
| Claude Code | `.claude/skills/` | `/{skill-name}` e.g. `/system-architect` |
| GitHub Copilot CLI | `.copilot/skills/` | `/copilot-skill {name}` |
| Cursor | `.cursor/skills/` | `@skill-{name}` |
| OpenClaw | `.openclaw/workspace/skills/` | `/{name}` |
| Gemini CLI | `.gemini/skills/` | paste content / custom injection |

Keep installed skills current: `skills-update` (all symlinked projects see it instantly).

---

## 2. Read one skill end to end (10 minutes)

Open `skills/05-development/backend-developer/SKILL.md`. It is one markdown file with YAML
frontmatter on top. That is the whole unit — no code, no magic.

### 2a. Frontmatter — the machine-readable identity

```yaml
name: backend-developer                      # slug = folder name = node id
description: >                               # THE routing trigger (<= ~1024 chars)
  Use when building REST APIs, implementing authentication, designing database schemas,
  writing server-side business logic, or debugging backend performance issues. Handles ...
  Do NOT use for frontend UI work, ...
license: MIT
compatibility: requires-python-3.10-or-node-18-or-go-1.21   # content prerequisites
tags: [backend, api, fastapi, express, go, authentication, database, ...]
author: / status: / version: / updated:      # provenance fields
token_budget: ...                            # declared per-skill load budget (tokens)
chain:                                       # <-- the part this tutorial cares about
  consumes_from: [...]                       # skills whose output should exist BEFORE this one
  feeds_into: [...]                          # skills that should run AFTER this one
workflow:                                    # optional: typed artifact contract for graphs
  ...                                        #   inputs/outputs with schemas
```

Read the `description` like a routing rule, not marketing copy: it starts with **"Use when …"**
(trigger conditions) and **"Handles …"** (scope), and ends with **"Do NOT use for …"** (negative
boundaries that stop the wrong skill from being chosen). Agents and routers match user intent
against these strings, so this is also where routing quality lives.

### 2b. Body — the progressive-disclosure sections

Sections are marked for reading depth; the agent reads what the task needs:

```markdown
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE ...
## Route the Request            # entry router: "Auto-Route" vs "Intent Route" branches
## Ground Rules — Read Before Anything Else
## The Expert's Mindset         # what masters know + cognitive biases
## Operating at Different Levels            # L1 Apprentice -> L5 Transformative
## When to Use                  # decision table vs neighbouring skills
## Decision Trees               # branching logic (the 30-second entry point)
## Core Workflow                # phased steps w/ time estimates + completion criteria
## Cross-Skill Coordination     # upstream/downstream, communication triggers
## Proactive Triggers / What Good Looks Like / Deliberate Practice
## Error Recovery               # symptom -> root cause -> fix -> lesson
## Verification                 # exit-criteria checklist (evidence, not vibes)
```

A real skill folder is more than the file:

```
skills/05-development/backend-developer/
├── SKILL.md            # the instructions (read by the agent)
├── scripts/            # deterministic tools (run, don't read)
├── references/         # deep knowledge loaded on demand (progressive disclosure)
│   ├── decision-guide.md
│   └── patterns-catalog.md
└── assets/             # templates + samples
```

This is why "load cost" stays low: the agent reads the ~450-char description to route, a
~200-line section to act, and pulls `references/` only when it needs depth.

---

## 3. Read the dependency chain — `consumes_from` / `feeds_into` (10 minutes)

The `chain:` block is a **static dependency map across skills**. Real excerpts:

```yaml
# skills/04-architecture/api-designer/SKILL.md
chain:
  consumes_from: [idea-to-spec, system-architect, domain-modeling, database-designer,
                  backend-developer, ...]
  feeds_into:    [secure-api-design, graphql-engineer, deprecation-engineer,
                  fintech-app-developer, ...]
```

How to read it like a developer:

1. **`consumes_from` = "this must already exist before you start me."** `api-designer`
   consumes `database-designer` because you design the API contract *after* you know the
   schema. It consumes `backend-developer` because a good API design accounts for how it will
   be implemented.
2. **`feeds_into` = "give your output to these next."** `backend-developer` feeds
   `code-reviewer`, `qa-engineer`, `security-reviewer` — implementing code *produces* the
   artifact reviewers consume.
3. **Symmetry is a repo law.** If A `feeds_into` B, then B must `consumes_from` A. The whole
   graph is checked: `python3 scripts/validate_chains.py` (0 asymmetries is the enforced bar,
   and the full symmetric edge set — 1,675 pairs / 1,916 directed edges — is published in
   `README.md` / `COORDINATION-MATRIX.md`).
4. **The chain is not execution.** It answers "who comes before/after me", never "run now".
   Execution happens in layer 2.

Try the mental exercise now: trace a feature — "checkout API change" — through the chain.
`idea-to-spec` → `system-architect` → `api-designer`/`database-designer` →
`backend-developer` → `code-reviewer` + `security-reviewer` + `qa-engineer`. Open
`COORDINATION-MATRIX.md` to see this as a real graph (or the interactive explorer at
`docs/graph-explorer/index.html`).

> **Sub-skills:** many skills point at domain variants (`references/`, `SUB-SKILL-MAP.md`
> lists 2,000+). `skills/04-architecture/api-designer` stays universal; the fintech/health/
> gaming variants live one level deeper. Start at the parent, drill in only when your domain
> needs it.

---

## 4. Understand how skills get *chosen* (5 minutes)

Three mechanisms, all live in the repo:

1. **Agent auto-routing.** When you type a task, the agent matches intent against each skill's
   `description` triggers and loads the best one. `skills/00-framework/using-agent-skills/`
   is the meta-skill that teaches the agent to route itself. Routing precision is *measured*
   (`docs/benchmarks-vs-agent-skills.md`).
2. **Slash commands** (Claude Code / Gemini CLI / Copilot CLI, parity-verified):
   `/spec`, `/plan`, `/build`, `/test`, `/review`, `/code-simplify`, `/webperf`, `/ship`.
3. **Manual invocation** by name: `/{skill-name}` (Claude), `@skill-{name}` (Cursor), etc.
   (table in §1).

For a human, the mental shortcut is: *name the outcome you want* — `idea-to-spec`,
`code-reviewer`, `qa-engineer` — and the routing layer fills in the rest.

---

## 5. Run a real graph end to end (20 minutes — the heart of the tutorial)

Everything below is runnable today in this repo with plain Python 3 (no node, no API keys):

```bash
cd Skills
python3 scripts/validate-workflows.py --all          # every manifest is valid (8/8)
python3 scripts/workflow-runner.py --selftest        # the engine's own tests (11/11)
```

### 5a. The manifest, annotated line by line

Open `examples/payments-api-ship/payments-api-ship.yaml`. Top to bottom:

```yaml
name: payments-api-ship          # slug; must match the filename
description: "..."               # single line — the Safe-YAML subset forbids block scalars
payloads:                        # registry of handoff payload shapes (what travels between nodes)
  handoff-v1: [status, summary, artifacts, decisions, open_questions,
               verification_evidence, context, budget, next]
budget:
  max_steps: 80                  # global backstop: the whole run may take at most 80 steps
start: spec                      # entry node id
nodes:                           # the executable units
  - id: spec                     # node id (unique across nodes/gates/loops/parallel)
    skill: idea-to-spec          # WHICH skill runs here (must resolve under skills/)
    outputs: [spec]              # run-state fields this node writes
  - id: qa
    skill: qa-engineer
    inputs: [change, fix-report] # run-state fields this node reads
    outputs: [qa-report]
gates:                           # decision points (no content work)
  - id: identify-agent-gate
    type: gate
    kind: agent                  # agent gate: pre-human triage (see §6)
    pool: [fixer, qa]            # corrective channels it may pick
    max_reroutes: 3              # bounded reroute budget
    escalate_to: release-gate    # terminal target when it gives up
  - id: release-gate
    type: gate
    kind: human                  # human gate: terminal approval
parallel:                        # multi-agent fan-out
  - id: auditors
    nodes: [code-reviewer, security-reviewer]
    join: all                    # downstream edges fire only after BOTH report
    outputs: [audit-findings]
edges:                           # directed transitions
  - from: spec
    to: architect
    when: spec.status == done    # condition vocabulary: <node>.status == done | verdict == pass ...
    payload: handoff-v1          # what rides along this edge
loops:                           # iteration is EXPLICIT and bounded
  - id: fix-verify-loop
    nodes: [fixer, qa]           # one pass = fixer then qa, in order
    exit_when: qa.verdict == pass # leave the loop when this is true after a pass
    max_iterations: 2            # hard cap per window
    escalate_to: identify-agent-gate  # exhaustion/stagnation routes here first
    convergence: { window: 2, require_delta: true }  # stop on identical consecutive passes
end: [release-gate]              # the run is complete when these are done
```

Rules the validator enforces that will save you later (each has a real error message):
`validate-workflows.py` checks ids are unique and resolve, skills exist, `when`/`exit_when`
strings are in the condition vocabulary, parallel writers are disjoint, loops have
`exit_when` + `max_iterations`, agent gates have `pool`/`max_reroutes`/`escalate_to`, and
every node is reachable from `start` (escalation arcs count as reachability).

### 5b. The executor contract (layer 3)

A workflow node *calls* the executor for its content. The contract is one function:

```python
def execute_node(node_id, state, ctx) -> dict:
    return {"status": "done",          # done | blocked | needs_review | skipped
            "verdict": "pass",         # free-form; loops match on it (qa.verdict == pass)
            "summary": "...",          # <= 400 chars, what happened
            "evidence": ["..."],       # refs that prove it (the anti-hallucination gate)
            "diagnostics": ["..."],    # feeds the stagnation detector
            "decisions": [...], "open_questions": [...], "artifacts": [...]}
```

- `ctx` tells you the context: `{"loop_id", "pass", "skill", ...}` — and for agent gates,
  `ctx["mode"] == "identify"` with `ctx["pool"]` (you return `verdict: reroute` + `next: <id>`).
- `state` is the shared run-state dict (nodes, fields, budget, log) — inspect `--state` JSON.
- Real usage: `scripts/executors/agent_executor.py` turns each node into a skill-grounded
  prompt for an agent CLI (`AGENT_CMD` env). `examples/payments-api-ship/executor_demo.py` is
  the teaching stub that scripts verdicts so the graph is fully deterministic.

### 5c. Run it and read the trace

```bash
# run 1 — smoke (stub passes everything): proves traversal + handoff
python3 scripts/workflow-runner.py \
    --manifest examples/payments-api-ship/payments-api-ship.yaml \
    --state /tmp/pay-smoke.json

# run 2 — the real story (QA fails twice -> loop exhausts -> agent gate reroutes
#         a bounded window -> QA passes -> human approves)
python3 scripts/workflow-runner.py \
    --manifest examples/payments-api-ship/payments-api-ship.yaml \
    --executor examples/payments-api-ship/executor_demo.py \
    --state /tmp/pay-happy.json

# run 3 — escalation story (QA never passes; all channels tried -> human decides)
PAYMENTS_SCENARIO=exhaust python3 scripts/workflow-runner.py \
    --manifest examples/payments-api-ship/payments-api-ship.yaml \
    --executor examples/payments-api-ship/executor_demo.py \
    --state /tmp/pay-exhaust.json
```

The `--state` file is the full run-state JSON. Learn to read these three parts:

```jsonc
// outcome summary printed to stdout:
{ "outcome": "complete", "steps_used": 14,
  "iterations": {"fix-verify-loop": 2}, "nodes": {...} }

// state.nodes.<id> — per-node record {status, verdict, iterations, evidence, summary, sha}
// state.log      — chronological actions: done | agent-gate | escalate | guardrail ...
// state.handoff  — the last handoff: {"from": "qa", "to": "release-gate",
//                   "payload": "handoff-v1", "sha": "99a735cf7df6"}
```

Annotated trace of **run 2** (`state.log`, filtered to `done` nodes):

```
spec → architect → backend          single-agent serial phase (idea → design → code)
  → code-reviewer → security-reviewer     multi-agent parallel audits (join: all)
  → fixer → qa → fixer → qa               loop window 1: QA fails twice → exhaustion
  → identify-agent-gate: agent-gate | reroute 1/3 -> fixer     ← escalate to AGENT first
  → fixer → qa → fixer → qa               loop window 2: QA passes on run 4 → exit
  → release-gate (human approved)         ← human sign-off is the terminal step
```

Measured: `outcome: complete`, `steps_used: 14`, `qa.verdict: pass`, `release-gate: approved`,
one agent reroute consumed, and the human gate ran **only to approve**, not to rescue.

---

## 6. Escalation, precisely: agent gate vs human gate

Both exist, and the difference is the answer to *"can re-routing fix this, and is it cheap?"*:

| | `kind: agent` gate (identify-agent-gate) | `kind: human` gate (release-gate) |
|---|---|---|
| Trigger | loop exhaustion (`escalate_to` from a loop) | edge into the gate, or an agent gate's terminal `escalate_to` |
| What it does | identifies the corrective channel (`pool`) and grants a fresh bounded window, channel first | pauses; a person approves/rejects with the escalation report |
| Bounded by | `max_reroutes` + no-delta-across-reroutes + step budget | the human's judgment |
| Real trace (happy) | `agent-gate \| reroute 1/3 -> fixer (max-iterations)` | `release-gate: approved` |
| Real trace (exhaust) | reroutes `1/3 -> fixer`, `2/3 -> qa`, then `escalate \| all channels tried (fixer,qa) (reroutes 3/3)` | human decides on the evidence trail |

Why this ordering is safe (the three guardrails): reroute budget is bounded; identical
end-state across two reroutes escalates (no new information); and non-reroutable reasons —
global `step-budget` or a `guardrail-block` — escalate straight to the human gate because
re-routing can't fix a spent budget or a blocked payload. `workflow/templates/escalate.md`
defines what the human receives: per-pass attempts with evidence, the blocker, and a
recommended next step. **Never escalate empty-handed.**

---

## 7. Handoffs: single-agent vs multi-agent, and the payload registry

What travels between nodes is the registered payload. Keys (`handoff-v1`) and their meaning:

| Key | Meaning |
|---|---|
| `status` / `summary` | what the sender concluded, in one line |
| `artifacts` | produced files ({name, path, sha, type}) |
| `decisions` | choices made and why (ADR seeds) |
| `open_questions` | unresolved items the receiver must resolve or carry |
| `verification_evidence` | proof the sender's work met criteria |
| `context` / `budget` / `next` | shared state, remaining budget, what the receiver should do |

Single-agent serial: exactly one sender → one receiver per edge (`spec → architect →
backend`). Multi-agent parallel: one sender fans out to N (`backend → code-reviewer` and
`backend → security-reviewer`), auditors write **disjoint** outputs (enforced), and the
`join: all` gates downstream firing until every auditor reports. The `sha` on each handoff is
the sender's node-record hash — receivers can detect corrupted state (run-state rule R3:
mismatch aborts rather than propagate).

In real life with `agent_executor.py`, "multi-agent" means each node is answered by a
separate agent invocation grounded in that node's `SKILL.md`; the engine guarantees ordering,
budget, and context integrity between them.

---

## 8. Make it yours (10 minutes)

1. **Pick your own skills for a feature.** Walk the chain: which skill produces the input you
   need? Which consumes your output? Copy the smallest manifest shape from
   `workflow/manifests/serial-feature-delivery.yaml` and swap node skills/ids.
2. **Write your own minimal skill** (any skill with `Core Workflow` + `Verification` headings
   is a valid default-mode node):

   ```markdown
   ---
   name: my-service-validator
   description: Use when validating my-service configs. Handles ... Do NOT use for ...
   license: MIT
   tags: [my-service, validation]
   ---
   ## When to Use
   ...
   ## Core Workflow
   ...
   ## Verification
   ...
   ```

   Validate: `python3 scripts/validate-workflows.py --coverage` proves every library skill
   resolves as a workflow node; your local file must be under `skills/` to be found.
3. **Restrictions that will trip you up** (all enforced, all with clear errors):
   - The Safe-YAML subset has **no block scalars** (`>-`, `|`) — keep descriptions on one line.
   - `when:` / `exit_when:` strings must match the condition vocabulary
     (`node.status == done`, `node.verdict == pass`, `node.status in (a, b)`).
   - A node may belong to at most one loop; parallel writers must be disjoint.
   - Agent-gate `pool` members must belong to the loop that escalates to the gate.
   - Every manifest needs `start`; ids are `^[a-z0-9][a-z0-9-]*$`.
4. **Run with real agents**: `--executor scripts/executors/agent_executor.py` (set
   `AGENT_CMD`). Everything else — budgets, loops, gates, handoff integrity — is engine code
   you get for free.

---

## 9. Glossary (quick)

| Term | Meaning |
|---|---|
| Skill | one `SKILL.md` = expertise + workflow, loadable by an agent |
| Chain | `consumes_from` / `feeds_into` — static dependencies between skills (not execution) |
| Node | one skill (or gate) instance inside a manifest, referenced by `id` |
| Edge | `from → to` with a `when` condition and optional handoff payload |
| Loop | bounded repeat of a node group: `exit_when`, `max_iterations`, stagnation window |
| Parallel | fan-out of members with a join policy (`all`/`majority`/`any`) |
| Gate | decision point: `human` (terminal approval) or `agent` (bounded pre-human reroute) |
| Escalate | loop exhaustion routes to `escalate_to` — an agent gate first, a human gate last |
| Handoff | the payload + integrity hash passed along an edge |
| Run-state | the JSON file (`--state`) recording nodes, budget, log, handoff |
| Executor | the function that does one node's content work |

## 10. Where to go next

- `QUICKSTART.md` (5-minute version), `USAGE-GUIDE.md` (deep usage), `docs/USING-IN-PROJECTS.md`
- `WORKFLOW-SYSTEM.md` — full engine spec (§2.4 covers `kind: agent` gates)
- `workflow/templates/` — `handoff-in.md`, `handoff-out.md`, `escalate.md`, `loop-reflect.md`
- `docs/benchmarks-vs-agent-skills.md` — how routing quality is measured
- `CONTRIBUTING-SKILLS.md` / `SKILL-QUALITY-STANDARDS.md` — if you want to add a skill
