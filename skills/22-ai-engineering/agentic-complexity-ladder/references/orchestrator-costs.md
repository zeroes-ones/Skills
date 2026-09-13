# Orchestrator Costs

<!-- DEEP: 5+min -- planning tokens, unpredictable latency, and the debugging penalty -->

## What the orchestrator rung is

A central step decomposes the task dynamically, delegates to workers, and synthesises their results.

```
input → [orchestrator] → decides the decomposition
                       → ┬→ [worker] task 1
                         ├→ [worker] task 2
                         └→ [worker] task N
                       → [synthesise]
```

The defining property: **the decomposition is not fixed in advance.** That is its entire justification,
and its entire cost.

## The three costs

### 1. Planning tokens

The orchestrator's decomposition is itself a model call — usually a long one, since it reasons about
the task before delegating.

| Cost | Note |
|---|---|
| The planning call itself | often comparable to a full worker call |
| Re-planning on failure | if the plan fails, the orchestrator may replan — unbounded |
| Reasoning tokens before any work | paid before the first useful output |

### 2. Unpredictable cost and latency

This is the property that makes orchestrators hard to operate, not merely expensive.

| Property | Fixed workflow | Orchestrator |
|---|---|---|
| Number of calls per run | known | decided at runtime |
| Cost per run | predictable | a distribution with a long tail |
| Latency | bounded by the node count | unbounded by design |
| Budget enforcement | a step cap means something | the cap is hit mid-plan |
| Capacity planning | arithmetic | a tail estimate |

**The long tail is the operational problem.** A workflow's p99 cost is close to its median. An
orchestrator's p99 can be many times the median, because a task that decomposes into twenty
sub-tasks costs twenty times one that decomposes into one — and both look identical on entry.

### 3. The debugging penalty

| Question | Workflow | Orchestrator |
|---|---|---|
| Which step failed? | visible in the manifest | the plan must be inspected |
| Why? | the step's prompt and input | the plan's reasoning, reconstructed |
| Reproducible? | yes — same path | only with the same plan, which is data |
| Testable per step? | yes, each step has a contract | the trajectory is the test |
| On-call knowledge | the manifest is the map | the trajectory is the map |

**The plan is data, not code.** That means a defect in the plan is a data defect, and there is no
"line of code" to point at. Reproducing it means capturing and replaying the plan.

## The 20-input test

The test that decides whether the orchestrator rung is warranted, and it takes an afternoon.

```text
1. Take 20 real inputs.
2. Decompose each one BY HAND — write the sub-tasks.
3. Look at the 20 decompositions:
   ├── They repeat a small number of shapes
   │   → the decomposition IS enumerable → you need a CHAIN or ROUTING, not an
   │     orchestrator. Cheaper, faster, debuggable.
   └── They genuinely differ, in ways you cannot enumerate
       → the orchestrator is warranted. Proceed.
```

**Why this works:** the orchestrator's justification is that the decomposition *varies* beyond
enumeration. Twenty hand-decompositions either reveal the pattern or demonstrate that it is
genuinely absent. Either answer is useful, and neither requires building anything.

**The most common outcome is the first branch.** Most "we need an orchestrator" tasks turn out to
decompose into three or four recurring shapes, which is routing or a chain.

## The bounded requirement

If the orchestrator is warranted, it must still be bounded in two dimensions:

| Bound | Why |
|---|---|
| **Action space** — an allow-listed tool set | unbounded agency is a security decision (see `workflow-vs-agent.md`) |
| **Plan size** — a maximum sub-task count | otherwise the cost tail is unbounded |

```yaml
orchestrator:
  max_subtasks: 8          # bounds the cost tail
  max_replans: 2           # bounds the re-planning loop
  tools: [read, search, write, test, review]   # the allow-list
  budget:
    max_cost_usd: 2.00     # enforced, halting
```

**Without `max_subtasks`, capacity planning is impossible** — the p99 is the sum of an unbounded
number of workers. Without an allow-list, the security posture is undefined.

## Verifying an orchestrator

| Requirement | Why |
|---|---|
| The outcome is verifiable | an unverifiable orchestrator cannot be gated |
| Plan quality is measured | a bad plan is the rung's own failure mode |
| The cost distribution is measured (median **and** p99) | the tail is the operational risk |
| The subtask count distribution is known | it drives both cost and capacity |
| Re-planning is bounded and measured | an unbounded replan loop is a runaway |

## When the orchestrator is the wrong rung

| Situation | Better |
|---|---|
| 20 hand-decompositions repeat | routing or a chain — the decomposition was knowable |
| The action space cannot be bounded | stop; this is a security decision, not an architecture one |
| The outcome cannot be verified | add verification first, or choose a simpler rung |
| Cost must be predictable | a chain; the orchestrator's variance is inherent |
| The team cannot debug a trajectory | a workflow; the operational capacity is a real constraint |

**The last row is a legitimate reason**, and it is honest to state: a team without the capacity to
operate an orchestrator should not run one, whatever the task's shape.

## Recording an orchestrator decision

```text
Rung:      5 (orchestrator–workers)
Baseline:  Rung 3 routing — 84% pass; the residual failures are tasks that need
           an unknown number of sub-steps

20-input test: the decompositions genuinely differ; 17 of 20 have a unique shape
               (this is the justification)

Bounds:    max_subtasks 8, max_replans 2, tools allow-listed (6 tools)
Trade:     planning call + variable worker count; cost median $0.14, p99 $1.10
           latency median 4 s, p99 26 s; debugging requires plan capture
Verification: outcome checked against a rule set; plan quality sampled weekly
Exit:      if a task taxonomy emerges covering >90% of inputs, replace with
           routing (check 2027-04, by running the 20-input test again)
```

The `20-input test` line is what makes this an evidence-based decision rather than a preference.

## Checklist

- [ ] The 20-input test showed the decomposition genuinely varies beyond enumeration (R6)
- [ ] The action space is bounded by an allow-list (Anti-Hallucination)
- [ ] `max_subtasks` bounds the cost tail
- [ ] Re-planning is bounded
- [ ] The cost distribution is measured as median **and** p99, not just median
- [ ] The subtask count distribution is known
- [ ] The outcome is verifiable, and plan quality is measured
- [ ] The debugging cost is accepted with the operational capacity considered
- [ ] An exit condition exists, tied to the emergence of a task taxonomy
