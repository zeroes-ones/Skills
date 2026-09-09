# Payments API Ship — A Real-World Delivery Lifecycle as a Workflow Graph

> **New here?** Start with **[`TUTORIAL.md`](TUTORIAL.md)** — the 45-minute developer/consumer
> onboarding that reads this whole repo top to bottom (install → read a skill → read the chain →
> run this graph → escalation & handoffs → make it yours). This README is the quick reference for
> the example itself.

A single runnable example of how skills become **executable work** in this library: taking one
real feature — *"add a payments/checkout API change with code review, security review, QA, and a
controlled production release"* — from idea to human-approved ship.

It exercises every layer in one graph:

| Real-world step | Layer | Construct in this example |
|---|---|---|
| Turn the vague ask into a spec | skill chain | `spec` node → `idea-to-spec` |
| Design before you code | skill chain | `architect` node → `system-architect` |
| Implement | skill chain | `backend` node → `backend-developer` |
| Two specialists audit in parallel | graph | `parallel` block `auditors`: `code-reviewer` + `security-reviewer`, `join: all` |
| Fix + re-verify until green | graph | bounded loop `fix-verify-loop` (`fixer` ↔ `qa`), `exit_when: qa.verdict == pass` |
| Loop can't converge → try the right channel first | graph | `escalate_to: identify-agent-gate` (`kind: agent`, `pool: [fixer, qa]`, `max_reroutes: 3`) |
| Human signs off the release | graph | `release-gate` (`kind: human`) — terminal |

Files:

```
examples/payments-api-ship/
├── payments-api-ship.yaml   # the workflow manifest (validated by validate-workflows.py --all)
├── executor_demo.py         # deterministic stand-in for agentic content (two scenarios)
└── README.md                # this walkthrough
```

## The graph

```
  spec ──► architect ──► backend
                              │
              ┌───────────────┴───────────────┐   parallel: auditors (join: all)
              ▼                               ▼
        code-reviewer                  security-reviewer
              └───────────────┬───────────────┘
                              ▼
        ┌───────────── fix-verify-loop (max_iterations: 2) ─────────────┐
        │   fixer (backend-developer) ──► qa (qa-engineer)              │
        │        ▲                               │                      │
        │        └── qa.verdict != pass? ────────┘                      │
        └───────────────┬────────────────────────┘
                        │ qa.verdict == pass (exit)          exhaustion
                        ▼                                        ▼
        qa ──(handoff)──► release-gate (human) ◄── escalate_to: identify-agent-gate
                                                (kind: agent, bounded reroute,
                                                 then escalate_to: release-gate)
```

Why this order is not arbitrary — it is the skill chain made executable. The same
`consumes_from` / `feeds_into` declarations in `SKILL.md` frontmatter say: `idea-to-spec`
feeds `system-architect`; `backend-developer` consumes architecture and feeds
`code-reviewer`, `security-reviewer`, `qa-engineer`; `qa-engineer` consumes the implemented
change. The manifest simply picks the skills and asserts the ordering as edges + a loop.

> **Detailed annotated diagrams for all six examples:** [`../DETAILED-DIAGRAMS.md`](../DETAILED-DIAGRAMS.md)

## Run it

```bash
# 1) Headless smoke test — stub executor passes everything (shows traversal + handoff)
python3 scripts/workflow-runner.py --manifest examples/payments-api-ship/payments-api-ship.yaml

# 2) The real story — QA fails twice, the loop exhausts, the agent gate reroutes a
#    bounded window (fixer first), QA passes, the human approves the release:
python3 scripts/workflow-runner.py \
    --manifest examples/payments-api-ship/payments-api-ship.yaml \
    --executor examples/payments-api-ship/executor_demo.py \
    --state /tmp/pay-happy.json

# 3) The escalation story — QA never passes; every channel is tried, then the graph
#    escalates to the human release gate with the evidence trail:
PAYMENTS_SCENARIO=exhaust python3 scripts/workflow-runner.py \
    --manifest examples/payments-api-ship/payments-api-ship.yaml \
    --executor examples/payments-api-ship/executor_demo.py \
    --state /tmp/pay-exhaust.json
```

(The demo executor is a deterministic stand-in for an LLM running each node's SKILL.md. To use
real agents, pass `--executor scripts/executors/agent_executor.py` with `AGENT_CMD` set.)

## What actually happens (real traces, scenario 2 — "happy")

Execution order from the run-state log:

```
spec → architect → backend → code-reviewer → security-reviewer
  → fixer → qa → fixer → qa        (window 1: qa fails twice → loop exhausts)
  → identify-agent-gate: agent-gate | reroute 1/3 -> fixer (max-iterations)
  → fixer → qa → fixer → qa        (window 2: qa passes on run 4 → exit)
  → release-gate (human approved)
```

Measured result: `outcome: complete`, `steps_used: 14`, loop iterations `{fix-verify-loop: 2}`,
`qa.verdict: pass`, `release-gate: approved`, one agent-gate reroute used, human gate reached
only for final approval.

Key log line (the pre-human escalation — agent gate, not human):

```
9 identify-agent-gate agent-gate | reroute 1/3 -> fixer (loop fix-verify-loop, max-iterations)
```

Last handoff (single-agent, point-to-point, with the sender-record hash for integrity):

```json
{"from": "qa", "to": "release-gate", "payload": "handoff-v1", "sha": "99a735cf7df6"}
```

## What happens when automation can't converge (scenario 3 — "exhaust")

QA never goes green, so the agent gate spends its bounded budget and then escalates to the
human release gate:

```
 9 identify-agent-gate agent-gate | reroute 1/3 -> fixer (max-iterations)
13 identify-agent-gate agent-gate | reroute 2/3 -> qa    (max-iterations)
17 identify-agent-gate escalate   | all channels tried (fixer,qa) (reroutes 3/3)
   -> release-gate (human)        # decides with the escalation report, not automation
```

Measured result: `outcome: complete`, `steps_used: 18`, `qa.verdict: changes_requested`,
`release-gate: approved` (in the demo the human always approves; in real life this is the point
where a person reads `workflow/templates/escalate.md` and decides).

## Single-agent vs multi-agent handoff in this example

| Phase | Shape | Handoff |
|---|---|---|
| spec → architect → backend | **single-agent, serial** | point-to-point: one sender payload → one receiver, each edge stamps `{from, to, payload, sha}` |
| code-reviewer + security-reviewer | **multi-agent, parallel** | one `backend` payload **fanned out** to both auditors; they write disjoint outputs (`code-findings`, `security-findings`); the `join: all` fires `fixer` only after both report |
| qa → release-gate | single-agent | final handoff carries status/summary/artifacts/decisions/open_questions/verification_evidence/context/budget/next (the `handoff-v1` registry) |

The payload registry (`status, summary, artifacts, decisions, open_questions,
verification_evidence, context, budget, next`) is why the next node — human or agent — never has
to re-derive context: the handoff *is* the context.

## Escalate to agent vs escalate to human — the rule in action

- **`escalate_to: identify-agent-gate` (agent)**: the failure is *reroutable* — the loop just
  needs the right channel leading a fresh bounded window (`max_reroutes: 3`, no-delta across
  reroutes escalates, budget/guardrail reasons escalate directly). Cost: cheap, autonomous.
- **`escalate_to: release-gate` (human)**: the terminal decision — ship or don't. Cost: expensive,
  and it only fires after automation tried (or is declared unable).

That ordering is the real-world contract: *automation iterates to zero known errors; a person
owns the release.*

## Extending it

- Change `executor_demo.py` so `security-reviewer` fails until round 2 — you will see the
  parallel auditors drive a second fixer activation.
- Raise `max_iterations` or lower `max_reroutes` to feel the budgets.
- Swap node skills for your real stack (e.g. `frontend-developer`, `devops-engineer`) — any skill
  with Core Workflow + Verification is a valid node.
