# Dependence and Autocorrelation

**Portability target:** spec-level. Everything here is arithmetic on one series of period
P&Ls.

## Two different kinds of dependence, often conflated

The engine's output carries one unconditional caveat, printed on every run, and it names the
first kind. The second kind is measured and printed as two fields. They are not the same
problem and they need different responses.

### Kind 1 — Structural nesting. Not measurable, not fixable by data.

`H` contains `Q` contains `M`. `Y` contains all of them. The same 120 trades are re-summed
into 2 yearly numbers, 3 half-yearly numbers, 5 quarterly numbers and 13 monthly numbers.

Therefore:

- A t-statistic across `Y` periods and a t-statistic across `M` periods are **not two tests**.
  They are two summaries of one body of evidence.
- If the yearly bucket shows |t| = 2.079 and the monthly bucket shows |t| = 0.948, the correct
  reading is not "the yearly view is more significant". It is "one bucket has 2 periods and
  the other has 13, and the estimator with one degree of freedom is the unstable one."
- Adding a bucket does not add evidence. **More periods ≠ more information.** This is trap 1
  in the skill's Core Workflow and the single most common error in timeframe analysis.

The response is not a formula. It is a sentence in the report: *this is a stability indicator
for one book, not a significance test of an edge.* The engine prints that sentence
unconditionally, precisely so a good month cannot produce an output without it.

### Kind 2 — Serial dependence in the period P&L series. Measurable.

Real books are not white noise. Losses cluster: a regime turns, a thesis class breaks at
once, several correlated positions lose together, and three consecutive weeks lose while the
six before them won. When period P&L is positively autocorrelated, the period count
overstates how much independent information the series carries, and the t-statistic is
optimistic.

The engine measures lag-1 autocorrelation as the Pearson correlation of the period P&L
series against itself shifted one period:

```
rho = corr(x[0..n-2], x[1..n-1])
```

It is reported as `n/a` when there are fewer than three periods (a two-point series has a
correlation of ±1 by construction and carries no information) or when either lagged
sub-series has zero variance.

Then the effective sample:

```
n_eff = n_periods × (1 − rho) / (1 + rho)
```

reported as `n/a` when `rho` is unavailable or when `|rho| >= 0.999`, where the formula's
denominator collapses. The engine additionally prints `n_eff_capped`, which is `n_eff`
limited to the total trade count in the bucket — because for `rho < 0` the raw formula can
return more "effective periods" than there were trades, which is impossible and must not be
quoted.

## The shipped illustrative log's dependence, quoted from engine output

Data: `examples/logs/illustrative-year-synthetic.csv` — **synthetic, illustrative, generated
at fixed seed 20260414, carries no market information.** Values below are pasted from
`examples/run-output.txt`.

| Bucket | n_periods | rho | n_eff | n_eff_capped | n_eff / n_periods |
|---|---|---|---|---|---|
| `D` | 120 | 0.2128 | 77.894 | 77.894 | 0.649 |
| `W` | 53 | 0.0722 | 45.866 | 45.866 | 0.865 |
| `2W` | 27 | 0.1979 | 18.079 | 18.079 | 0.670 |
| `M` | 13 | 0.0933 | 10.782 | 10.782 | 0.829 |
| `Q` | 5 | 0.0323 | 4.687 | 4.687 | 0.937 |
| `H` | 3 | −1.0000 | n/a | n/a | n/a |
| `Y` | 2 | n/a | n/a | n/a | n/a |

Four things in that table are worth reading closely.

**1. The monthly bucket carries 10.8 effective periods, not 13.** `M` is the bucket the
verdict names, and the verdict is required to print `n_eff` next to `n_periods` for exactly
this reason. A 13-period t-statistic of 0.948 is really a 10.8-period statistic, and the
honest confidence is lower than the number alone suggests. The engine's verdict line reads
`n_periods = 13, n_eff = 10.78`.

**2. The daily bucket loses a third of its periods to dependence.** `D` has 120 periods but
77.9 effective ones — 35% of the apparent sample is autocorrelation. This is the regime
structure in the generator: a bad regime produces consecutive losing days, so consecutive
daily P&Ls are not independent draws.

**3. A three-period bucket can produce `rho` of exactly −1.0000, and the engine refuses it.**
`H` has three periods. Alternating signs across three points give a perfect negative
correlation, which is an artefact of the sample size, not a mean-reverting strategy. The
`|rho| >= 0.999` guard reports `n/a`. **A guard firing is a result**, and it should appear in
the report rather than being replaced by a number.

**4. Negative autocorrelation can produce an absurd `n_eff`.** On the six-trade hand-check
fixture, the two-week bucket's series is `250, −100, 300, −75`, which yields
`rho = −0.985453` and `n_eff = 545.952` — from four periods and six trades. The engine caps it
at `6.000` and says why in `n_eff_note`. Anyone quoting 545.95 as "effective sample size"
would be quoting a formula outside its domain. See
`examples/logs/hand-check-synthetic.csv` for the full expected-value block.

## Why the correction is a ratio, not a subtraction

`(1 − rho) / (1 + rho)` is the standard variance-inflation adjustment for a first-order
autoregressive series: an AR(1) process with parameter `rho` has a long-run variance inflated
by `(1 + rho)/(1 − rho)` relative to `n × σ²`, so the effective sample is deflated by the
reciprocal. [COMPUTED] It assumes AR(1) — one lag, constant variance, no trend. A book with a
strong regime change or a structural break violates that, and the correction is then
indicative rather than exact.

**Do not treat `n_eff` as a correction that fixes the t-statistic.** It is a disclosure that
the t-statistic is optimistic, printed next to it so nobody can quote one without the other.
The engine intentionally does not recompute `t_stat` using `n_eff`, because that would hide
the raw number a reader needs in order to disagree.

## What a positively autocorrelated series does to each field

| Field | Effect of positive `rho` |
|---|---|
| `sd_period_pnl` | Understated relative to the long-run spread, because clustering inflates the mean without fully showing up in consecutive differences |
| `t_stat` | Inflated. The denominator is too small and the period count is overstated |
| `period_sharpe` | Inflated by exactly the same factor, since it is `t_stat / sqrt(n_periods)` |
| `max_drawdown` | **Understated, and dangerously so.** Clustering is what creates drawdowns: three losses in a row is a drawdown, the same three losses spread across a quarter are not. A high `rho` and a small drawdown should not be quoted together as a low-risk result |
| `n_eff` | Below `n_periods`, which is the point |

The drawdown row is the one that gets missed. Drawdown is a **path** statistic: it depends on
*order*, and order is exactly what autocorrelation measures. A bucket that smooths order —
yearly, half-yearly — destroys most of the drawdown information it was asked to carry. See
[pnl-and-drawdown-by-period.md](pnl-and-drawdown-by-period.md).

## How to test the dependence properly (three options, in order of cost)

1. **Read `rho` and `n_eff`, and report them with the t-statistic.** Free, and it is what the
   engine already does. This is the minimum.
2. **Re-run on the trade date-bucketed series and compare.** If the daily and monthly
   `n_eff / n_periods` ratios differ sharply, the dependence lives at a frequency the monthly
   bucket cannot see.
3. **Block bootstrap the period series.** Resample contiguous blocks of periods (block length
   at least `1/rho` rounded up) rather than individual periods, and recompute the t-statistic
   on each resample. This produces an honest interval at the cost of a few lines of code and
   a distributional assumption you can state. The engine does **not** do this, and says so —
   see [what-the-engine-cannot-tell-you.md](what-the-engine-cannot-tell-you.md).

## The dependence disclosure the engine always prints

Reproduced here so it can be argued with rather than only obeyed:

> DEPENDENCE CAVEAT — these buckets are not independent tests. H literally contains the M
> periods, Q contains the M periods, Y contains them all; the same trades are re-aggregated,
> not resampled. A t-statistic computed across a bucket series is therefore a STABILITY
> INDICATOR for that book, not a significance test of an edge. Read n_eff next to n_periods:
> where the period P&L series is positively autocorrelated, the effective sample is smaller
> than the period count suggests, and the t-statistic above is optimistic.

If a report of yours quotes a bucket's t-statistic without that sentence, the report is
incomplete regardless of how right the arithmetic is.

## Failure modes that produce fake independence

1. **Failure mode: buckets presented as parallel evidence.** "The weekly, monthly and quarterly
   views all agree the edge is positive" — three views of one body of data. Countermeasure:
   label every multi-bucket claim as one stability check, not as agreement between tests.
2. **Failure mode: the best bucket is quoted and the rest are dropped.** A search across seven
   buckets reported as one finding. Countermeasure: pre-commit to the bucket from the cadence
   rule, or disclose the search.
3. **Failure mode: `n_eff` omitted because the t-statistic looked good.** Countermeasure: the
   engine prints them on the same line; carry the line, not the number.
4. **Failure mode: `rho` treated as a strategy signal.** "The monthly P&L is autocorrelated, so
   I can predict next month." The autocorrelation here is a property of clustering, not a
   forecast; `n = 13` cannot support a forecast. Countermeasure: autocorrelation is used to
   *discount* the sample, never to generate a signal.
5. **Failure mode: a negative `rho` read as mean reversion.** With three or four periods,
   `rho` near −1 is a small-sample artefact and the engine refuses it. Countermeasure: treat a
   guard firing as a guard firing.
6. **Failure mode: drawdown quoted from a smooth bucket alongside a high `rho`.** An
   understated drawdown next to a clustering disclosure is a contradiction. Countermeasure:
   compute drawdown at the finest bucket with enough trades per period, and apply
   `trade-performance-analyst`'s coarse-bucket adjustment if you cannot.
7. **Failure mode: dependence measured but not acted on.** A report that prints `n_eff` and
   then quotes `t_stat` as if `n_eff` were `n_periods`. Countermeasure: state the confidence in
   `n_eff` terms in the same sentence as the t-statistic.
