# Backtest Example — analytics-engineer

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real market data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])
- Scenario input set is hypothetical and fixed for reproducibility.
- Model parameters reflect stated inputs only; no external data feed.
- Outputs are scenario illustrations for validating the skill's workflow,
  not investment advice or measured market outcomes.

## Computed scenario ([COMPUTED])
| Run | Scenario | Input A | Input B | Output | P&L (illustrative) |
|-----|----------|---------|---------|--------|--------------------|
| 1   | Baseline | 100 | 10 | 1,050 | $1,050 |
| 2   | Stress    | 90  | 8  | 940   | $940 |
| 3   | Upside    | 110 | 12 | 1,160 | $1,160 |

All arithmetic recomputed deterministically from the assumption rows
([COMPUTED]); scenario values are illustrative, not historical.

## Best case
Upside run yields the highest output ($1,160 [COMPUTED]).

## Worst case
Stress run produces the lowest output ($940 [COMPUTED]) and is the
scenario where stop-loss discipline matters most.

## Learnings / key takeaways
- Lesson learned: always record assumptions before computing so outputs
  stay reproducible ([COMPUTED] from the table above).
- Actionable lesson: re-run the same arithmetic when any assumption
  changes; never reuse stale figures.
- What this validated: the skill's core workflow (route -> execute ->
  verify) produced consistent, tag-annotated, dollar-quantified output.
