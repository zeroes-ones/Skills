# workflow-runtime — Executable Multi-Agent Review Graph

The executable counterpart to the narrative chains in `examples/orchestra-platform/`: one
**workflow manifest**, a deterministic **executor**, and two **run-state checkpoints** that prove
the loop machinery from `WORKFLOW-SYSTEM.md` actually terminates, hands off, and escalates.

```
┌────────────────────────────── review-fix-loop (max_iterations: 3) ──────────────────────────────┐
│                                                                                                 │
│   code-reviewer ─┐                                                                              │
│   security-      ├─► reviewers (parallel: join all)                                             │
│   reviewer       │                                                                              │
│   qa-engineer   ─┘                                                                              │
│        │                                                                                        │
│        ▼                                                                                        │
│   review-verdict ─── verdict == pass? ──no──► fixer (backend-developer)                         │
│        │                     │                     │                                            │
│        │                (exit_when)               └────► back to reviewers                      │
└────────┼─────────────────────┼──────────────────────────────────────────────────────────────────┘
         │ (exit)              │ (exhaustion at 3 passes)
         ▼                     ▼
   fixer no-ops ──► release-gate (human) ◄── escalate_to: release-gate
                        │
                        ▼
                     approved
```

**Manifest:** `multi-agent-review-graph.yaml` — a `parallel` fan-out of three specialist
reviewers (`code-reviewer`, `security-reviewer`, `qa-engineer`), an aggregate `review-verdict`
node (join: all semantics), a `fixer` node, a bounded `review-fix-loop` with
`exit_when: review-verdict.verdict == pass`, and a human `release-gate` that is both the happy-path
destination and the loop's `escalate_to` target.

**Executor:** `executors/review_board.py` — a deterministic stand-in for agentic node content. It
implements exactly what the boundary templates ask of a real agent: each reviewer only returns
`pass` once its criteria are met; the aggregate node applies join-all; the fixer only acts when the
aggregate verdict is `changes_requested`. Scenario is selected with `REVIEW_SCENARIO=happy`
(reviewers pass from round 3) or `REVIEW_SCENARIO=exhaust` (they never pass).

## How to run

```bash
# 1. Static validation (structure, refs, cycles, loop budgets, payloads)
python3 scripts/validate-workflows.py --manifest examples/workflow-runtime/multi-agent-review-graph.yaml

# 2a. Happy path — reviewers converge on round 3, loop exits, gate approves
REVIEW_SCENARIO=happy python3 scripts/workflow-runner.py \
  --manifest examples/workflow-runtime/multi-agent-review-graph.yaml \
  --executor examples/workflow-runtime/executors/review_board.py \
  --state examples/workflow-runtime/state/happy-run-state.json

# 2b. Exhaustion — reviewers never pass, loop hits max_iterations and escalates to the gate
REVIEW_SCENARIO=exhaust python3 scripts/workflow-runner.py \
  --manifest examples/workflow-runtime/multi-agent-review-graph.yaml \
  --executor examples/workflow-runtime/executors/review_board.py \
  --state examples/workflow-runtime/state/exhaust-run-state.json
```

The runner also self-checks: `python3 scripts/workflow-runner.py --selftest`.

## Observed results (committed checkpoints in `state/`)

| Scenario | Loop iterations | Steps | Outcome | Evidence in state |
|----------|-----------------|-------|---------|-------------------|
| happy | 3 (passes on round 3) | 16 | complete | all reviewers + aggregate `verdict: pass`; fixer `no-op` on final round; handoff fixer→release-gate with sha |
| exhaust | 3 (max_iterations) | 16 | complete (via escalation) | reviewers stuck at `changes_requested`; `log` contains an `escalate` action (node `null`, reason max-iterations); release-gate executed as the exhaustion destination |

Note both runs end at the human `release-gate` by design — that is the loop's designed termination
in both directions. The difference is *how* it got there: happy path traverses the `fixer →
release-gate` edge with a handoff payload; exhaustion is routed directly by `escalate_to` with an
escalation log entry and no edge handoff.

## Semantics notes (what this example proves)

- **Bounded iteration is enforced in code.** The loop cannot run past `max_iterations: 3`, cannot
  run past the global step budget, and stops early on stagnation (2 identical passes) when enabled.
- **One gatekeeper per loop.** `review-verdict` is the single node whose verdict the exit condition
  reads — three independent reviewer verdicts collapse through it (this is what an aggregate or
  supervisor node is for in a real engine; see `references/langgraph-mapping.md`).
- **Loop-owned transitions.** Edges between loop members are suppressed during passes; the loop
  decides when a pass repeats and when it exits. Members' outgoing edges fire only after the loop
  exits, so `fixer → release-gate` cannot short-circuit a failing pass.
- **Handoffs are payloads.** Every edge in the manifest names `handoff-v1` from the payload
  registry; the runner records `{from, to, payload, sha}` on every boundary crossing.
- **Headless vs. engine execution.** The stdlib runner executes nodes sequentially for
  determinism; the `reviewers` parallel block is honored for write-ownership and validation but its
  members run in order. Real engines map the same manifest to true fan-out (LangGraph/CrewAI), and
  the executor here is a stand-in for an agent running the referenced SKILL.md.

## File map

| File | Role |
|------|------|
| `multi-agent-review-graph.yaml` | Flagship manifest (validates clean) |
| `executors/review_board.py` | Deterministic node content stand-in |
| `state/happy-run-state.json` | Checkpoint proving convergence path |
| `state/exhaust-run-state.json` | Checkpoint proving escalation path |
| `walkthrough.md` | One iteration narrated with the boundary templates applied |
| `references/langgraph-mapping.md` + `graph.py` | Illustrative LangGraph translation of the manifest |
