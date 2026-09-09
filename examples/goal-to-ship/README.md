# Goal → Graph → Ship — Describe a Goal, Get a Runnable Spec-to-Ship Pipeline

The "builds itself, human at the end" demo: give `scripts/goal-to-graph.py` a one-line goal,
and it generates a **validated workflow manifest + deterministic executor** that runs skill
nodes, iterates a bounded fix-verify loop until verification passes (exhaustion reroutes via a
`kind: agent` gate), and ends at a **HUMAN release gate** once everything is green.

## Quickstart

```bash
# generate a manifest + executor for any goal
python3 scripts/goal-to-graph.py \
    --goal "Build me a booking SaaS MVP with auth and payments" \
    --name booking-mvp --kind build --size m --fix-rounds 3 \
    --out examples/goal-to-ship/booking-mvp

# run it (loop -> agent reroute -> verification green -> HUMAN release gate)
python3 scripts/workflow-runner.py \
    --manifest examples/goal-to-ship/booking-mvp/booking-mvp.yaml \
    --executor examples/goal-to-ship/booking-mvp/booking-mvp_executor.py \
    --state /tmp/booking-mvp.json
```

`--kind`: `build | ui | api | db | support` · `--size`: `xs|s|m|l|xl|xxl` (scales
`budget.max_steps`) · `FIX_ROUNDS=<n>` env overrides when verification turns green.

## The auto-generated anatomy (booking sample)

```
[goal] --> spec (idea-to-spec)
            --> build (backend-developer)
            --> verify (qa-engineer)
        fix-verify-loop: exit_when verify.verdict == pass · max_iterations 2
            exhaust -> identify-agent-gate (kind agent, pool [build, verify],
                       bounded reroutes, escalate_to release-gate)
        verify green -> release-gate (kind human) -> approved
```

Real trace (deterministic executor, `FIX_ROUNDS=3`): verification fails twice, the loop
exhausts, the agent gate reroutes one bounded window, verification passes, the **human release
gate approves**:

```
outcome: complete · steps_used: 8
spec → build → verify → build → verify → build → verify → release-gate
5 identify-agent-gate agent-gate | reroute 1/3 -> build (fix-verify-loop, max-iterations)
```

Support archetype (`--kind support`) real trace — monthly bucket → loop → agent reroute →
human month-close gate:

```
intake → fix → verify → fix → verify → fix → verify → close-gate
5 identify-agent-gate agent-gate | reroute 1/3 -> fix (fix-verify-loop, max-iterations)
```

Generated artifacts are plain files you can edit: swap the skill behind `build`, add nodes,
change the human gate — everything still validates with
`python3 scripts/validate-workflows.py --all`.

## How this plugs into the repo (what's linked, what's on demand)

Nothing is a monolith; everything is **on-demand and layered**:

| Layer | Role | Loaded/runs when |
|---|---|---|
| `SKILL.md` files (304) | playbooks (content) | an agent reads one when routing/invoked |
| Planner skills (`workflow-graph-authoring`, `iterative-task-execution`, `multi-agent-orchestration`) | decide *which* skills/order for a goal | you ask the agent to plan |
| `scripts/goal-to-graph.py` | materializes the plan as manifest + executor | you run it for a goal |
| `scripts/workflow-runner.py` | executes the graph (loops, budgets, handoffs, gates) | you run a manifest |
| Executor (`agent_executor.py` or generated) | does each node's content by running that node's skill | engine calls it per node |
| Skills' own `scripts/` | deterministic tools ("run, don't read") | a SKILL.md workflow step tells the agent to run them |
| Governance (`pre-commit`, `validate_*.py`, freshness `emit-*`) | checks | on commit/CI, not at runtime |

So: skills never "call" each other at runtime — routing selects one; a workflow manifest
selects a subset as nodes; scripts are invoked explicitly by the engine, an agent step, or you,
exactly "whenever required". Progressive disclosure keeps it lean: description for routing,
sections on demand, `references/` only when depth is needed.
