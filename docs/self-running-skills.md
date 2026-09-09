# Self-Running Skills — Handoff-and-Continue in Every Direction

The end state you're describing: **give any skill a goal, and it works in all directions —
back (what must exist before), front (what should run next), up (framework/ground rules), down
(sub-skills/depth), diagonal (cross-domain neighbors) — handing off context at every step and
repeating in a loop until its Verification passes, then handing off to a human at the end.
By itself.**

This repo already has every primitive. This page explains the **handoff-and-continue
protocol**, maps your directions onto real data, and points to the generator that lets **any**
eligible skill self-run that way.

## 1. The protocol (what "hand off and continue" means here)

Every node execution produces a **handoff record** — the runner already stamps it:

```json
{"from": "api-designer", "to": "backend-developer",
 "payload": "handoff-v1", "sha": "99a735cf7df6"}
```

`handoff-v1` carries: `status, summary, artifacts, decisions, open_questions,
verification_evidence, context, budget, next`. The `sha` is the sender's node-record hash, so
the receiver can detect corrupted state (mismatch aborts — never propagate).

Rules that make continuation safe and automatic:

| Rule | Meaning |
|---|---|
| **Every completion hands off** | a node is "done" only when it emitted evidence + a `next` decision |
| **Continue by decision, not by habit** | edges (`when:` conditions) decide the next node; loops decide "try again"; escalation decides "human" |
| **Loop until verification** | `exit_when` is evaluated after every pass; only then does the loop hand off forward |
| **Never dead-end silently** | exhausted loops escalate (agent gate → human gate) with the evidence trail |
| **Human at the end** | terminal gates (acceptance/release/cutover/close) approve once green |

## 2. Your directions → the data + mechanics they use

| Direction | Means | Repo source | Mechanic |
|---|---|---|---|
| **Back** (trace back) | prerequisites / what failed before | `chain.consumes_from`; loop history (stagnation, guardrail-block) | pre-nodes executed first; loops re-run the failing channel |
| **Front** (continue ahead) | what should run next | `chain.feeds_into`; edge `when` + `payload` | satisfied edges hand off to the next node |
| **Up** (context above) | ground rules, meta, seniority | `00-framework/` skills (`using-agent-skills`, `skill-levels`, `senior-engineer-mode-router`) | loaded as context when the node runs |
| **Down** (drill deep) | sub-skills, references, variants | `references/*.md`, `SUB-SKILL-MAP.md`, deeper skill dirs | progressive disclosure: pulled on demand inside the node |
| **Diagonal** (cross-domain) | neighbors in other domains | `Cross-Skill Coordination` sections, `COORDINATION-MATRIX.md` | edge to the named skill or handoff note |

The engine then composes them: **pre-nodes (back) → your skill (loop until Verification passes,
reading up/down/diagonal context each pass) → continue forward (front) → human gate (end)**.

## 3. "All skills should do it by itself" — what's true today

- **Any skill with `Core Workflow` + `Verification` is already a valid workflow node** — the
  repo audits this (`~300/303` eligible) and proves it with `validate-workflows.py --coverage`.
- Content is agentic: when a node runs, the agent reads that skill's sections (up/down/
  diagonal context) and its `Core Workflow` executes the work; the engine owns ordering, loops,
  handoffs, budgets, and gates.
- The missing piece was *materializing the all-directions graph for a single skill without
  hand-writing a manifest* → that is `scripts/skill-self-run.py` (see §4).

Honest limits:
- Skills don't self-execute without an **executor** (a real agent or the deterministic stub).
- "By itself" is **bounded** self-correction: loops exit on `exit_when`, budgets cap steps,
  no-delta across reroutes escalates — then a human decides.
- Chain "up/down/diagonal" content is loaded *in context* by the agent, not executed as
  separate nodes (except where you declare them as edges).

## 4. Using it

```bash
# generate an all-directions manifest + executor for ANY eligible skill
python3 scripts/skill-self-run.py --skill code-reviewer --depth 2 --fix-rounds 3 \
    --out examples/self-run/code-reviewer

# run: backtrace prereqs -> skill loops until Verification -> continue to human gate
python3 scripts/workflow-runner.py \
    --manifest examples/self-run/code-reviewer/code-reviewer.yaml \
    --executor examples/self-run/code-reviewer/code-reviewer_executor.py \
    --state /tmp/code-reviewer.json
```

Generated shape (auto-built from the skill's `chain`):

```
[back]  prereq₁ → prereq₂ … (chain.consumes_from, capped by --depth)
           │ (handoff-v1, when: done)
           ▼
[loop]  main-skill  → exit_when: main.verdict == pass (its Verification as the bar)
           │  not pass → next pass (bounded)  ·  exhaust → identify-agent-gate (reroute)
           ▼ (green)
[front] → continue-node / accept-gate (HUMAN)     ◄── exhaustion escalates here too
```

## 5. Adoption path to "every skill does this"

1. **Default mode (today):** any eligible skill can be wrapped by `skill-self-run.py` —
   backtrace prereqs, self-loop to Verification, human end. Run it per skill on demand.
2. **Make handoff the norm in every SKILL.md:** the quality standard already requires
   `Cross-Skill Coordination` + `Verification`; add the expectation that Core Workflow output
   names `next` (route target) — the runner's payload registry already carries it.
3. **Governance:** enforce that every eligible skill stays node-valid and that each
   `Core Workflow` phase lists a `Complete when` (gate) — both already checked by the
   16-gate pre-commit.
4. **Fully autonomous:** replace the deterministic stub executor with a real agent executor +
   memory, then a goal → graph → run → human-release pipeline (see
   `scripts/goal-to-graph.py` and `examples/goal-to-ship/`) applies the same protocol to
   whole engagements.

## 6. Where to look

- Handoff semantics + payload registry: `WORKFLOW-SYSTEM.md` §5, `workflow/templates/handoff-*.md`
- Engine: `scripts/workflow-runner.py` (loops, stagnation, escalate, handoff `sha`)
- Chain data: any skill's `chain:` + `COORDINATION-MATRIX.md`
- Generated goal graphs: `examples/goal-to-ship/`; per-skill self-run: this page + generator
