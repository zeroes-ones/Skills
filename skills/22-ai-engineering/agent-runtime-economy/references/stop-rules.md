# Stop Rules

Stopping is the cheapest optimisation available and the one most often missing.

## Why a cap is not a stop rule

A cap spends to the cap regardless of progress. A task that converged at turn four will run to turn twenty and produce nothing further, because the only condition is "budget remains".

## Measurable convergence conditions

| Condition | Detection |
|---|---|
| No outcome improvement | Metric flat over the last N turns |
| Repetition | Current attempt matches a prior one |
| Self-reading | Agent is revisiting its own earlier output |
| Goal loss | It can no longer state what "done" means |
| Diminishing return | Cost per unit of progress rising |

Any one of these should stop the session and report, not continue.

## Where the rule belongs

Written **before** it is needed, alongside the budget. A stop rule improvised in a stuck session is written under pressure and will be wrong.

## Failure modes

- **Cap only.** Burns budget on a converged task.
- **Unfalsifiable convergence.** "When it's done" is not a condition.
- **Rule defined mid-crisis.** Too late and too optimistic.
- **Stopping without reporting.** The stop must say what was achieved and what remains.
- **Ignoring diminishing return.** Slow progress is treated as progress.
- **Never stopping a successful loop.** A loop that works is still paying per turn.
