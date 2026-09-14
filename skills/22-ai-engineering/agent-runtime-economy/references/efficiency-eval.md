# Efficiency Evaluation

Measuring that a session got cheaper *and* no worse.

## The pair

Never report cost alone. Every figure appears with its success metric:

| Cost | Paired with |
|---|---|
| Tokens per session | Task success rate |
| Turns per task | Outcome quality |
| Cost per run | Cost per *successful* outcome |

Cost per successful outcome is the number that matters; cost per run can improve while outcomes collapse.

## Protocol

1. Fix a held-out task set.
2. Run with the current configuration; record tokens, turns, wall-clock, success.
3. Change one lever.
4. Re-run the same set.
5. Report the delta on **both** axes, or report no result.

## What counts as a win

A win is: cost down, success not down. A cost reduction with a success reduction is a trade, not a win, and must be reported as a trade.

## Failure modes

- **Cost-only reporting.** The classic error; a saving can hide a quality collapse.
- **Moving the task set.** Comparing unlike runs.
- **Changing several levers at once.** Attribution becomes impossible.
- **No held-out set.** The task drifts toward whatever is convenient.
- **Reporting only wins.** Null results are what stop the next team repeating the measurement.
- **Optimising a proxy.** Token count falling while success also falls is not efficiency.
