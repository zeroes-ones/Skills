# Backtest Example — configuration-change-safety

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A payments API is deployed across 200 instances behind a load balancer.
- Model parameters reflect the stated inputs only; no external data feed.
- Outputs are scenario illustrations for validating the skill's workflow, not measured
  production outcomes.

| Parameter | Value | Tag |
|---|---|---|
| Instances | 200 | [ESTIMATED] |
| Blast-radius percentage proposed | 1% (= 2 instances) | [ESTIMATED] |
| Requests per minute at peak | 60,000 | [ESTIMATED] |
| Revenue per minute at peak | $4,500 | [ESTIMATED] |
| Shared connection-pool limit | 500 connections, per-instance | [ESTIMATED] |
| Mean requests per instance | 300 rpm | [ESTIMATED] |
| Config drift window (undetected) | 6 hours | [ESTIMATED] |

## Computed scenario ([COMPUTED])

Blast-radius arithmetic (Decision Tree 1 / R3):

```
proposed scope        = 1% of 200 instances = 2 instances
traffic per instance  = 60000 / 200        = 300 rpm
"safe" scope impact   = 2 * 300            = 600 rpm  (1% of traffic)
```

Three application strategies, computed from the assumptions above:

| Run | Strategy | Reversibility | Selector verified? | Outcome | Illustrative loss |
|-----|----------|---------------|--------------------|---------|-------------------|
| 1 | Apply to all 200 instances at once | No (connection-pool change took effect immediately) | Not checked | Full outage, 22 min | **$99,000** |
| 2 | 1% canary (2 instances), selector unverified | Yes | No — selector matched 2 instances that both held the app's only leader-election lock | 100% of writes failed, 14 min | **$63,000** |
| 3 | 1% canary, selector verified, staged 1% → 10% → 100% | Yes (rehearsed rollback) | Yes | Config applied; no customer impact | **$0** |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario values
are illustrative, not historical.

**Run 1 loss derivation** [COMPUTED]: 22 min outage × $4,500/min = **$99,000**. Root cause: the
connection-pool change was applied to 100% of instances simultaneously, and the new value exceeded
the upstream database's per-client connection cap — every instance failed at once.

**Run 2 loss derivation** [COMPUTED]: 14 min × $4,500/min = **$63,000**. Root cause: the scope was
correct by *count* (1% of instances) but wrong by *dependency graph* — the selector's two instances
happened to hold the sole leader-election lock, so "1% of instances" produced 100% of write failures.

**Run 3 loss derivation** [COMPUTED]: $0. The selector was verified against the dependency graph,
the change was classified reversible, the rollback had been executed once outside production, and
staging 1% → 10% → 100% caught a quota warning at the 10% stage (a warning, not a failure) before
full rollout.

## Best case

Run 3 — the fully classified and staged change. Reversibility was established before apply (R1), the
selector was verified to match exactly the intended targets (R3), and the rollback was rehearsed
rather than assumed. Customer impact: $0 ([COMPUTED] from the table above).

## Worst case

Run 2 is the more instructive failure: the change was *reversible* and the scope was *numerically
small* (1%), yet it caused an outage costing **$63,000** ([COMPUTED]). The blast radius was measured
by instance count instead of by what depended on those instances — the exact error R3 exists to
prevent. It is also the failure that most teams believe they have already avoided, because they
*did* canary.

Run 1 is the blunt failure: 100% simultaneous application of an unvalidated value, **$99,000**
([COMPUTED]).

## Learnings / key takeaways

- **Lesson learned:** "1% of instances" is not a blast-radius measurement. In Run 2 the selector
  matched two instances holding the sole leader-election lock, turning 1% of instances into 100% of
  write failures — **$63,000** for a change that looked cautious ([COMPUTED] from the table above).
- **Actionable lesson:** classify reversibility *before* apply. Run 1's pool change was not
  reversible in practice — the value took effect immediately and the upstream cap rejected new
  connections, so "revert" meant "restart every instance", which is an outage of its own
  ([COMPUTED]).
- **Actionable lesson:** validate on the target, not only in CI. The proposed pool value passed CI
  schema validation (an integer within range) and failed on the target because the upstream database
  capped per-client connections. Schema validation cannot see target state (Decision Tree 2).
- **What this validated:** the skill's core workflow (inventory → classify → schema → blast radius →
  rollout → rehearse → apply → observe → drift → record) distinguished a $99,000 change from a $63,000
  change from a $0 change using only the classification and selector-verification steps, and named
  the specific step responsible for each outcome difference.

## What this does not show

- No real production system was measured. Instance counts, traffic and revenue rates are [ESTIMATED].
- The skill's *output quality* on a real change set is not assessed here. As with
  `examples/resilience-node/README.md`, the meaningful test is a run with real inputs — a change set
  and an environment topology — where the agent either produces a classified plan or correctly
  refuses for lack of them.
