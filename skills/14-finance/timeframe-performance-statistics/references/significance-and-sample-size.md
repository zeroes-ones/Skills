# Significance and Sample Size

**Portability target:** spec-level. Every formula here is arithmetic on a list of numbers.
No vendor, no data feed, no calibration to any market.

## What the engine's `t_stat` actually is

```
mean_period_pnl        ─ over the periods of ONE bucket
sd_period_pnl          ─ the SAMPLE standard deviation of those period P&Ls (n − 1)
n_periods              ─ the number of periods in that bucket

t_stat = mean_period_pnl / (sd_period_pnl / sqrt(n_periods))
```

That is the one-sample t-statistic of "is the mean period P&L different from zero". It is
not a test of the strategy, and it is not a test of the *edge*: it asks whether the
collection of period totals has a mean that could plausibly have come from a distribution
centred on zero, given the spread of those same period totals.

Three consequences follow immediately, and all three are traps:

1. **It is a stability indicator, not a significance test.** The periods are nested and
   overlapping in the way described in
   [dependence-and-autocorrelation.md](dependence-and-autocorrelation.md). H contains M
   contains nothing, but M contains the trades, Q contains the M periods, and Y contains
   them all. Aggregating the same trades differently does not create evidence.
2. **It does not test the win rate.** `t_stat` tests period *P&L*; the win-rate test is the
   separate `edge > 2 × se_win_rate` check. A book can pass one and fail the other, and on
   the shipped illustrative log it fails both.
3. **It rewards small `sd` as much as it rewards large `mean`.** A bucket whose periods all
   look alike will produce a large t-statistic even when every period is small. That is not
   automatically good: it can mean the strategy has done the same thing nine times.

## The engine's verdict gate, and why those numbers

```
rank buckets by descending |t_stat|, but only among buckets with:
    n_periods         >= 12
    trades_per_period >= 5
mark any bucket with |t_stat| < 2 as NOT DISTINGUISHABLE FROM NOISE
```

**Why 12 periods.** Twelve is the point at which a bucket covers a year at monthly
resolution, a quarter at weekly resolution, or about six weeks at two-week resolution. Below
twelve periods, the sample standard deviation is too unstable for the t-statistic's
denominator to mean much — and the estimator's own uncertainty is comparable to the effect
being estimated. A bucket with four periods can produce `|t_stat| > 2` from one lucky
cluster; that is arithmetic, not evidence.

**Why 5 trades per period.** Below five, a period's `win_rate` is a coin flip's worth of
information, `payoff_ratio` is unavailable whenever the period has no loser, and
`break_even_win_rate` is therefore missing from most periods. A bucket whose periods have
one trade each is a bucket of individual trades wearing a period's name.

These two thresholds are **a rule, chosen and named, not a law**. Change them and say so. The
engine prints them every run precisely so they can be argued with.

**Why |t| < 2 is called noise.** Under the (strong, and violated) assumption of independent
periods, |t| = 2 corresponds to roughly a 5% two-sided false-positive rate. On the shipped
120-trade illustrative log **every** bucket with a computable t-statistic except the
two-period year bucket falls inside that band — and the two-period year bucket is the single
bucket with the least claim to be a series at all. That result is the honest one, and it is
the point of the demonstration.

## Reading the shipped log's t-statistics

Engine output, quoted verbatim from `examples/run-output.txt` (the data is
`examples/logs/illustrative-year-synthetic.csv`, which is **synthetic, illustrative and
carries no market information**):

| Bucket | n_periods | trades/period | t_stat | |t| ≥ 2? | Passes the gate? |
|---|---|---|---|---|---|
| `D` | 120 | 1.00 | 1.293 | no | no — `trades_per_period` |
| `W` | 53 | 2.26 | 1.113 | no | no — `trades_per_period` |
| `2W` | 27 | 4.44 | 1.056 | no | no — `trades_per_period` |
| `M` | 13 | 9.23 | 0.948 | no | **yes** |
| `Q` | 5 | 24.00 | 0.852 | no | no — `n_periods` |
| `H` | 3 | 40.00 | 0.574 | no | no — `n_periods` |
| `Y` | 2 | 60.00 | **2.079** | yes | no — `n_periods` |

Read that table again and notice the shape of it:

- The **only** bucket that clears the |t| ≥ 2 bar is `Y`, with two periods. Two points can
  always be made to look different; the t-statistic's denominator is estimated from a single
  degree of freedom.
- The **only** bucket that clears the two gates is `M`, and its t-statistic is 0.948 —
  inside the noise band. So the verdict is `M`, and the verdict's own confidence status is
  `NOT DISTINGUISHABLE FROM NOISE`.
- More periods did not buy more certainty. `D` has 120 periods and the weakest t-statistic
  of the three fine buckets, because a one-trade period has no averaging inside it.

## How many trades would it take?

This is the question the whole skill exists to answer honestly, so here is the arithmetic
for the shipped log. The engine reports, pooled across all 120 trades:

```
win_rate      = 0.5500      (66 wins / 120 decided trades; 0 break-even trades)
payoff_ratio  = 1.045703
break_even_win_rate = 1 / (1 + 1.045703) = 0.488829
edge          = 0.5500 − 0.488829 = 0.061171
se_win_rate   = sqrt(0.55 × 0.45 / 120) = 0.045415      [COMPUTED]
2 × se_win_rate = 0.090830      →  edge / (2 × se) = 0.6735
```

The edge is 0.67 of the distance needed to clear two standard errors. Solving
`edge = 2 × sqrt(p(1−p)/N)` for N, with p fixed at 0.55:

```
N at 2 sigma = 0.55 × 0.45 / (0.061171 / 2)^2      = 264.6 trades   (2.20× the log)  [COMPUTED]
N at 3 sigma = 0.55 × 0.45 / (0.061171 / 3)^2      = 595.3 trades   (4.96× the log)  [COMPUTED]
N for 80% power, alpha = 0.05 two-sided:
    N = (1.9600 + 0.8416)^2 × 0.55 × 0.45 / edge^2 = 519.1 trades   (4.33× the log)  [COMPUTED]
```

**A "two-sigma" result is not the same as a demonstrated edge.** Detecting an effect with 80%
power costs roughly `(2.8 / 2)^2 ≈ 2×` the sample a bare two-sigma threshold needs. Anyone
who quotes "you need about 265 trades" has answered the wrong question; the right answer for
this book is nearer 520, and it is still only a *statistical* answer — see
[what-the-engine-cannot-tell-you.md](what-the-engine-cannot-tell-you.md).

Every one of those figures is a function of the *strategy's* edge and variance. A book with a
20-point edge needs far fewer trades; a book with a 2-point edge may never have enough. The
formula is the transferable part; the numbers are not.

## Sharpe's standard error, and why small-sample Sharpe comparisons are meaningless

This skill does not compute or annualise Sharpe — that is
`trade-performance-analyst`'s job, and its reference `references/small-sample-statistics.md`
carries the standard error formula `SE(Sharpe) ≈ sqrt((1 + 0.5·SR²) / n)` with its
per-sample-size table and its minimum-sample guidance. **Read it there rather than trusting a
paraphrase here.**

What belongs *here* is the consequence for timeframe choice:

- `period_sharpe = mean_period_pnl / sd_period_pnl` is printed by the engine because it falls
  out of the same two numbers as `t_stat`, and it is a *per-period* ratio at that bucket's
  frequency — a daily-return Sharpe, a monthly-return Sharpe, and so on. They are not
  comparable to each other and they are not comparable to an annualised Sharpe.
- The relation between the two printed numbers is exact and worth internalising:
  `t_stat = period_sharpe × sqrt(n_periods)`. **The engine's `period_sharpe` and `t_stat` are
  the same piece of information.** Presenting both as if they were two findings is a mistake
  that doubles the apparent weight of one number. On the shipped log `M` reports
  `period_sharpe = 0.2629` and `t_stat = 0.948` over 13 periods, and
  `0.2629 × sqrt(13) = 0.948`. [COMPUTED]
- Because `SE(Sharpe) ≈ 1/sqrt(N)`, halving a Sharpe's error costs four times the data.
  Comparing a 53-period weekly Sharpe against a 13-period monthly Sharpe is comparing a
  tighter estimate against a looser one, not a better regime against a worse one.
- And the engine refuses to annualise it. `period_sharpe × sqrt(periods_per_year)` is a
  one-line computation that would multiply the weekly figure by `sqrt(52.1786) = 7.22` and the
  yearly figure by 1 — an ordering that follows from the calendar, not from the book. See
  [common-misreadings.md](common-misreadings.md).

## The sample-size arithmetic is not the only constraint

Even a 519-trade sample answers only "was this book's win rate distinguishable from its own
break-even, over the period covered". It does not answer:

- whether the edge persists out of sample,
- whether the trades are independent of each other,
- whether the edge is a fees-and-slippage artefact,
- whether the bucket choice was made after seeing the answer (see the multiple-comparison
  note below).

## Multiple comparisons: the timeframe search is itself a search

The engine tries seven buckets on the same trades. Reporting the best of seven is a
selection. If each bucket's t-statistic were an independent test at the 5% level, the chance
that at least one of seven clears |t| = 2 by luck is roughly `1 − 0.95^7 = 30%` — before any
dependence adjustment, which makes the true figure worse, not better. [COMPUTED]

Two honest responses:

1. **Pre-commit to the bucket before looking.** The cadence rule in
   [cadence-versus-holding-period.md](cadence-versus-holding-period.md) produces a bucket from
   the holding period without consulting the P&L. Use that one.
2. **If you did look at all seven, say so.** A verdict that names its bucket without naming
   that it chose among seven is a verdict with a hidden multiple-comparison step.

## The floor, stated plainly

| Claim | What supports it |
|---|---|
| "I have 120 trades and the win rate is 55% against a 48.9% break-even" | Arithmetic. Reportable as a description of the sample |
| "The edge is statistically distinguishable from break-even" | Requires roughly 2.2× this sample at two sigma, and the engine says `FAIL` |
| "This book has a proven edge" | Requires substantially more than 120 trades, an out-of-sample period, and independent verification of who checks the result. Not supported |
