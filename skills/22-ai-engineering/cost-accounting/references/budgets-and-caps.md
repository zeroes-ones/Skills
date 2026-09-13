# Budgets and Caps

<!-- STANDARD: 3min -- run-level caps, halting versus truncating, and the recorded increase path -->

## The rule

A budget that nothing enforces is decoration (R4). Two things must exist: a mechanism that fails,
and a recorded way to raise the limit.

## The cap, and where it lives

A run-level cost cap belongs in the manifest beside the step budget, because both bound the same
thing — how much work a run may do before it must stop and ask.

```yaml
budget:
  max_steps: 40
  max_cost_usd: 1.50      # halt the run when measured spend crosses this
```

**Why both are needed.** `max_steps` bounds activity; `max_cost_usd` bounds spend. They diverge
exactly when it matters: a run of 40 cheap steps and a run of 40 expensive steps have the same step
count and very different bills. Without the cost cap, the step budget is a proxy that can be 100×
wrong.

## Halting, not truncating

```text
CORRECT:   the run stops at the boundary, records `outcome: cost-budget`, and reports
           what it completed. A decision, clearly stated.

INCORRECT: the run continues but stops recording cost, or silently drops a node, or
           finishes with a summary that omits the breach.
```

Why this matters: a halted run is a fact someone can act on ("this workflow needs a bigger budget or
fewer nodes"). A truncated run that does not say why is a mystery that will be blamed on the engine.

The run-state must therefore carry the breach:

```json
{"phase": "escalated",
 "log": [{"step": 3, "node": "ship-gate", "action": "escalate",
          "detail": "cost budget exhausted ($0.0288 of $0.02)"}]}
```

## Where the check runs

| Point | Why |
|---|---|
| **After each node** | the earliest moment the breach is known; limits the overspend to one node |
| **Inside a loop pass** | a loop multiplies cost fastest, so the check must be per-member there too |
| **Before a gate or escalation** | escalations are the most expensive per-unit action; checking first avoids paying for one that will immediately breach |

**The overshoot is bounded by one node.** A cap of $1.50 may be crossed to $1.62 by a node that cost
$0.12 — the cap is a *stop*, not a *guarantee*. State that, so nobody expects precision the mechanism
cannot deliver.

## Why a cap cannot always trip

```text
cost cap set, but the executor reports nothing
  → measured: false
  → cost is 0.0
  → the cap does not trip

That is CORRECT behaviour, and it must be visible: a cap that appears to be
enforced while nothing is measured is worse than no cap, because it implies
a control that is not operating.
```

This is why the runner refuses to trip a cost budget on an unmeasured run, and why the run-state
carries `measured`. A cap on an unmeasured workflow protects nothing.

## The increase path

Required, or the cap becomes either permanent (and wrong) or silently edited (and pointless).

```text
When a budget genuinely needs to rise — scope grew, a model got dearer, a legitimate
run is longer — the increase must record:

  who        the person accepting the new spend
  why        the cause (scope, price, shape)
  from/to    the old and new cap
  review     the date this will be revisited
```

**The silent-raise failure** is the one the path prevents: editing the cap in a config file to match
the spend, with no record, so the budget reports success because it always equals reality. A budget
that cannot fail is not a budget.

| Acceptable raise | Unacceptable raise |
|---|---|
| Recorded with a reason and a review date | The number edited to fit the invoice |
| After a price change, with the delta explained | To "unblock the release" with no note |
| Alongside a recorded scope change | Applied per-workflow so one workflow's raise hides another's overrun |

## The three levels of bounding

Different questions need different mechanisms.

| Level | Bounds | Mechanism | Fails when |
|---|---|---|---|
| **Run** | one run's spend | `budget.max_cost_usd`, halting | measured spend crosses the cap |
| **Workflow over time** | the trend | CI gate on cost-per-success delta | the delta exceeds the threshold |
| **Team / product / fleet** | the total | showback, then chargeback, then an authorisation | the period total exceeds the authorised amount |

**Do not confuse them.** A run cap does not control a fleet's spend: a fleet of 10,000 cheap runs can
overshoot any per-run cap. A fleet authorisation does not protect a single runaway loop: it is
enforced monthly, and the loop burns in minutes. Both are needed for a production fleet.

## Escalating instead of failing

A cap breach is not always a defect. Two legitimate responses:

```text
1. HALT and escalate — the default. The run stops, a human or a gate decides.
2. HALT and continue with a cheaper strategy — where the workflow declares a
   degradation path (a smaller model, fewer nodes). Record that it degraded.
```

The second is a genuine design option: a workflow that can finish at lower quality rather than stop
is more useful than one that fails outright. But it must be *declared*, and the degradation recorded,
or the quality drop appears unexplained.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| A cap with no enforcement | protects nothing; the spend is unbounded while the config looks careful |
| Truncating silently | the breach is hidden, so it cannot be acted on |
| Raising the cap to fit the spend | the budget becomes a report of the past, not a constraint on the future |
| A per-run cap used as fleet governance | 10,000 runs each under the cap can still overshoot any budget |
| A cap on an unmeasured workflow | cannot trip, so it implies a control that is not operating |
| One cap for every workflow | shapes differ; a generous cap for one is a loose cap for all |
| Checking only at the end | a loop can overshoot the cap many times over before the check |

## Checklist

- [ ] Every cost-bearing workflow declares `budget.max_cost_usd` alongside `max_steps` (R4)
- [ ] The cap is checked after each node, and inside loop passes
- [ ] A breach halts the run and records `cost-budget` with the amounts
- [ ] The overshoot is understood to be bounded by one node, and nobody expects precision
- [ ] An unmeasured workflow's cap is known not to trip, and that fact is visible
- [ ] Every raise records who, why, from/to, and a review date
- [ ] Run, workflow-trend and fleet levels are bounded by different mechanisms, none mistaken for another
- [ ] Any halting-and-continuing path is declared and its degradation recorded
