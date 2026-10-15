# Common Misreadings

**Portability target:** spec-level. Each entry is a sentence someone actually writes in a
review, followed by what is wrong with it and what to write instead.

The illustrative numbers quoted here come from `examples/run-output.txt` for
`examples/logs/illustrative-year-synthetic.csv` — **synthetic, illustrative, seed 20260414,
carrying no market information.**

## 1. "More periods is more evidence"

**The misreading.** "The daily bucket gives me 120 observations and the monthly gives me 13,
so the daily view is more reliable."

**Why it is wrong.** The 120 daily periods are built from the same 120 trades as the 13 monthly
periods. Re-arranging one body of data does not create information. And on this log the daily
t-statistic (1.293) is *larger* than the monthly one (0.948) only because a one-trade period
has a small `sd` relative to nothing — not because the daily view knows more.

**Write instead.** "The daily bucket has 120 periods at 1.00 trades per period, so its periods
carry no within-period averaging and no per-period edge; it fails the trades-per-period gate.
The monthly bucket has 13 periods at 9.23 trades per period and is the only bucket that clears
both gates."

## 2. "The weekly and monthly views agree, so the edge is confirmed"

**The misreading.** Two buckets agreeing is independent corroboration.

**Why it is wrong.** The buckets are nested by construction. `H` contains `Q` contains `M`.
Agreement between them is guaranteed; disagreement would be the anomaly worth investigating.
The engine prints this as the DEPENDENCE CAVEAT on every run.

**Write instead.** "Weekly and monthly summaries of the same 120 trades agree, which is
arithmetic rather than corroboration: the buckets are nested and the same trades are
re-aggregated, not resampled. This is one stability check, not two tests."

## 3. "Annualising the monthly figures"

**The misreading.** "`mean_period_pnl = 131.41` monthly, so the book runs at
131.414615 × 12 = $1,576.98 a year." Or worse: "`period_sharpe = 0.2629` monthly, so annualised
Sharpe is 0.2629 × sqrt(12) = 0.911." [COMPUTED — both derivations are arithmetic, and both
are wrong as claims]

**Why it is wrong.** The engine's actual `annualised_return_simple_pct` for this log at
`--capital 250000` is **0.631%**, computed from 13 months of realised P&L and explicitly
labelled *simple (not compounded) mean-period return × periods_per_year; shown only because
`--capital` was supplied; annualising a short sample is a trap, not a result*. And the engine
**refuses to annualise Sharpe at all**, because `trade-performance-analyst` requires a lookback
period, a return frequency and a risk-free rate before a Sharpe can be stated — and none of
those are guessed here.

**Write instead.** "Over the 13 monthly periods observed, the mean monthly P&L was 131.41.
That is a description of 13 months, not a forecast. No annualisation is quoted: the sample
does not support it, and a Sharpe would need a declared lookback, frequency and risk-free rate
before it could be stated."

## 4. "The yearly t-statistic is 2.079, so the yearly view shows significance"

**The misreading.** Pick the bucket with `|t| > 2` and report it.

**Why it is wrong.** Two periods. A t-statistic with one degree of freedom in the denominator's
estimator is the least stable number in the table, and it is the *only* bucket on this log that
clears |t| = 2. The engine's verdict excludes it: `Y : n_periods=2 < 12`. The yearly bucket
also reports `max_drawdown = 0.00` on a book that actually fell 2,007.03 at daily resolution —
a bucket that cannot see risk is not a bucket that measures it.

**Write instead.** "The year bucket reports |t| = 2.079 across two periods and fails the gate on
`n_periods`. It is excluded from the verdict. Its zero drawdown is an artefact of two
observations, not evidence of low risk."

## 5. "My win rate is 55%, I am beating the market"

**The misreading.** A win rate compared to 50%, or to a market return.

**Why it is wrong.** Break-even for this book is **48.88%**, not 50%, because its payoff ratio
is 1.046. And a win rate is not a return: there is no benchmark, no risk-free rate and no
capital base anywhere in that comparison. The engine compares the win rate to its own
break-even and to nothing else.

**Write instead.** "Pooled `win_rate` is 55.00% against a `break_even_win_rate` of 48.88%, an
`edge` of 6.12 points, which is inside `2 × se_win_rate` (9.08 points) — the engine reports
`edge_test = FAIL`. The edge is not distinguishable from break-even at 120 trades."

## 6. "The drawdown is only −1,656.33, so the book is low risk"

**The misreading.** Read `max_drawdown` from whichever bucket is convenient.

**Why it is wrong.** `max_drawdown` by bucket on this log: `D` −2,007.03, `W` −1,859.05,
`2W` −1,853.02, `M` −1,656.33, `Q` −1,082.85, `H` −1,082.85, `Y` **0.00**. The monthly figure
understates the daily peak-to-trough by 21.17% [COMPUTED], and the yearly figure says the book
never fell at all. Drawdown is a path statistic: order is what coarsening destroys.

**Write instead.** "The daily bucket measures a −2,007.03 peak-to-trough fall; the monthly
bucket measures −1,656.33, understating it by 21.17%. `trade-performance-analyst` prescribes a
1.3–1.5× adjustment where only coarse data exists; here the realised ratio is 1.2117, below
that band, which is a property of this synthetic book and not evidence about the band."

## 7. "Zero-P&L trades are wins"

**The misreading.** A position cut at breakeven counted as a win, or as part of the win rate.

**Why it is wrong.** The engine's win test is `pnl > 0`, strictly. A scratch trade is counted in
`breakeven_trades`, reported on its own row, and **excluded from the win-rate denominator**:
`win_rate = wins / (wins + losses)`. On the six-trade hand-check fixture, one trade has
`pnl = 0`, so the engine reports `win_rate = 0.600000` from 5 decided trades — not
`3/6 = 0.500000`. That choice is printed; a report that silently reverses it is not readable
against an engine run.

**Write instead.** "One of six trades closed flat and is reported as `breakeven_trades = 1`,
excluded from the denominator. `win_rate` is 3/5 = 0.60."

## 8. "The bucket with the best numbers is the right review cadence"

**The misreading.** Try all seven, keep the one with the strongest statistic.

**Why it is wrong.** That is a selection across seven candidates, and the chance that at least
one of seven independent tests clears a 5% threshold by luck is roughly 30% — and the buckets
are not independent, so the true figure is worse. The cadence should come from the holding
period, via the quarter-to-half rule in
[cadence-versus-holding-period.md](cadence-versus-holding-period.md), *before* the P&L is
looked at.

**Write instead.** "The book's mean holding period is 11.14 days, so the review cadence is
weekly by the quarter-to-half rule; this was fixed before the statistics were run. The verdict's
monthly bucket is the finest bucket the trade count supports, and the gap between the two is
itself the finding."

## 9. "Fees are a detail"

**The misreading.** Report the edge without asking what is inside `pnl`.

**Why it is wrong.** Fees are per trade. They reduce every bucket's edge roughly equally, which
means **the agreement between the weekly and monthly views survives a fee load that destroys
the strategy**. On this log the edge is 6.12 points; a round-trip cost that removes more than
6.12 points of win-rate-equivalent value turns the headline positive into a negative and every
bucket will still say the same thing.

**Write instead.** "`pnl` is gross of commission, fees and spread — stated in the log's
provenance block. The 6.12-point edge is gross. No net figure is quoted until the cost per
trade is subtracted and the engine re-run."

## 10. "Half-yearly looks smoother, so it is more stable"

**The misreading.** Smoothness read as quality.

**Why it is wrong.** The half-yearly bucket reports `lag1_autocorrelation = -1.0000` and the
engine refuses it as `n/a` — with three periods, a perfect negative correlation is an artefact
of having three points, not evidence of mean reversion. Smoothing also destroys the drawdown:
`H` reports −1,082.85 against `D`'s −2,007.03.

**Write instead.** "The half-yearly autocorrelation is `n/a`: the engine's `|rho| >= 0.999`
guard fired because three periods cannot estimate a correlation. Its drawdown understates the
daily figure by 46%."

## 11. "A bucket that reports `n/a` is broken"

**The misreading.** `n/a` treated as an error to be worked around.

**Why it is wrong.** Every `n/a` in this engine is a deliberate refusal with a stated reason:
one period has no `sd`; zero variance has no `period_sharpe`; fewer than three periods has no
autocorrelation; a bucket with no losing trades has no `payoff_ratio` and therefore no
`break_even_win_rate`; `|rho| >= 0.999` collapses the `n_eff` formula. The `--json` output
carries the reason in `t_stat_note`, `autocorr_note` and `n_eff_note`.

**Write instead.** Quote the `n/a` and its reason. A guard firing is a result.

## 12. "Two years of monthly data proves the strategy"

**The misreading.** `n_periods = 24` read as enough.

**Why it is wrong.** 24 periods at a gate-passing trade rate is a real series, and it is
still 24 observations of one strategy in one regime. The t-statistic is a stability indicator
within the sample. It cannot speak to whether the edge persists, whether the sample period
contained a bull market, a correction, a bear market or a crash, or whether the trades were
independent of each other. See
[what-the-engine-cannot-tell-you.md](what-the-engine-cannot-tell-you.md).

**Write instead.** "24 monthly periods is a real series: quote its `n_periods`, its `n_eff` and
its t-statistic, and add that the statistic describes the 24 months observed. It does not test
persistence, regime robustness or out-of-sample performance, and none of those are claimed."

## The habit that prevents all twelve

Before any sentence containing a statistic, name three things: **the bucket**, **the trade
count**, and **the direction of the claim** (description, or inference). Most of the twelve
misreadings above are a description wearing an inference's clothes.
