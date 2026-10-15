# Reading the Engine Output

**Portability target:** spec-level. This file reads the output of
`scripts/timeframe_stats.py`, which is described in full in `examples/README.md`.

Every number quoted below is **actual engine output** for
`examples/logs/illustrative-year-synthetic.csv`, pasted from `examples/run-output.txt`. That
log is **synthetic and illustrative** — generated at fixed seed 20260414, carrying no market
information and describing no instrument, strategy or period.

## The order the output arrives in

```
1  PROVENANCE          — what the input says it is
2  BUCKETING CONVENTION— the one rule that assigns trades to periods
3  METRIC PROVENANCE   — what this engine does not own
4  PER-BUCKET SUMMARY  — a transposed table: rows are fields, columns are buckets
5  VERDICT             — the named bucket, the rule, and the dependence caveat
6  BEAT LOSSES TEST    — win rate against break-even, per bucket
7  PERIOD SERIES (CSV) — only with --csv
8  RETURN-BASED NOTE   — only with --capital
```

Sections 1 to 3 exist so that no number in sections 4 onward can be quoted without its label,
its convention and its ownership. If you paste a table into a report, paste its header.

## 1 — PROVENANCE

The engine reads `#` comment lines from the CSV and echoes every line beginning
`# PROVENANCE:` verbatim. For the illustrative log it prints five declared lines, the first of
which is:

```
declared : SYNTHETIC / ILLUSTRATIVE -- invented trade log. NOT market data. NOT a backtest.
           NOT a result. It carries no market information whatsoever and must never be
           quoted as a finding about any instrument, strategy or period.
```

**This is the honesty mechanism, and it is not decorative.** An output produced from an
unlabelled log prints:

```
declared : NONE -- the input declares no provenance.
           Tag the source of this log before using any number below.
```

If you see that line in your own run, stop and go tag the log. Everything below it is
arithmetic on data of unknown origin.

The block also prints `trade rows` and `comment lines`. If `trade rows` is not what you expect,
you have exported the wrong file, or a row failed to parse — the engine exits with code 2 and a
line number rather than skipping bad rows silently.

## 2 — BUCKETING CONVENTION

Printed every run:

```
A trade belongs to the bucket containing its CLOSE date, never its open date.
```

Plus the actual span: `Close dates in this log span 2025-01-20 to 2026-01-21.` Check that span
against your expectation. **A one-day-off range is the single most common input error** and it
is visible only here. See [bucket-definitions.md](bucket-definitions.md) for the reasoning
behind the close-date convention and its cost.

## 3 — METRIC PROVENANCE

Names `trade-performance-analyst` as the owner of Sharpe, Sortino, Calmar, maximum drawdown
and profit-factor **definitions**, and states that this engine does not annualise a Sharpe.
That sentence is the handoff, in the output, where a reader will see it.

## 4 — PER-BUCKET SUMMARY

One **transposed** table: rows are fields, columns are the seven buckets. Rows are grouped by a
bracketed label. Read the groups in this order.

### `[coverage]` — does this bucket even have a population?

| Row | Illustration (`D` / `M` / `Y`) | What to check |
|---|---|---|
| `n_periods` | 120 / 13 / 2 | The number of periods the bucket produced. Fewer periods = less across-period information |
| `n_trades` | 120 / 120 / 120 | Must equal the row count of the log for **every** bucket. If it does not, a trade was lost in bucketing |
| `trades_per_period` | 1.00 / 9.23 / 60.00 | The gate field. Below 5, per-period statistics barely exist |
| `periods_per_year` | 365.250 / 12.000 / 1.000 | A property of the calendar, **not** of the book. Never use it to annualise a session-based series |
| `first_period` / `last_period` | `2025-01-20` / `2026-01` / `2025` | The span actually covered. Watch for a stub first or last period |

**`n_trades` identical across all seven columns is a reconciliation, not a coincidence.** It is
the proof that every trade fell into exactly one period of each bucket. Check it first.

### `[trade totals]` — pooled across every trade in the bucket, and therefore identical in every column

`gross_profit`, `gross_loss` (a positive magnitude), `net_pnl`, `wins`, `losses`,
`breakeven_trades`, `win_rate`, `avg_win`, `avg_loss`, `payoff_ratio`,
`expectancy_per_trade`, `profit_factor`.

For the illustrative log: `gross_profit = 7,851.87`, `gross_loss = 6,143.48`,
`net_pnl = 1,708.39`, `win_rate = 55.00%`, `payoff_ratio = 1.046`, `profit_factor = 1.278`.

**These rows are the same in every column because every trade is in the bucket whichever
bucket you pick.** That is a fact about pooling, not a bug. It also means the trade totals
cannot tell you which timeframe to review — only the `[across periods]` group can.

`profit_factor` prints `inf` when `gross_loss` is 0 (no losing trades at all). `inf` is a real
answer, not a placeholder: it says the sample contains no loss to divide by.

### `[beat losses]` — the second test, bucketing-invariant

`break_even_win_rate` (48.88%), `edge` (6.12%), `se_win_rate` (0.0454),
`2 x se_win_rate` (0.0908), `edge > 2 x se?` (**FAIL**), `periods_positive_edge`.

The `periods_positive_edge` row counts how many *individual periods* had a computable positive
edge. For `M` it is 6 of the 13 periods; for `D` it is 0, because a one-trade period has no
payoff ratio and therefore no edge. This row is a good diagnostic of whether a bucket's periods
are informative at all.

Full treatment: [win-rate-versus-break-even.md](win-rate-versus-break-even.md).

### `[across periods]` — the group that actually answers the timeframe question

| Row | `D` | `M` | `Y` | Meaning |
|---|---|---|---|---|
| `mean_period_pnl` | 14.24 | 131.41 | 854.20 | Expected P&L per period at this frequency |
| `median_period_pnl` | 81.30 | 66.36 | 854.20 | Compare with the mean. A mean far above the median says the series is carried by a few periods |
| `sd_period_pnl` | 120.65 | 499.89 | 581.05 | Sample sd (n−1). `n/a` for a single period |
| `t_stat` | 1.293 | 0.948 | **2.079** | `mean / (sd / sqrt(n_periods))`. Read with `n_eff` |
| `period_sharpe` | 0.1180 | 0.2629 | 1.4701 | `mean / sd` at this bucket's frequency. Note `t_stat = period_sharpe × sqrt(n_periods)` |
| `cumulative_pnl` | 1,708.39 | 1,708.39 | 1,708.39 | Must equal total trade P&L for every bucket |
| `max_drawdown` | −2,007.03 | −1,656.33 | **0.00** | Peak-to-trough of the cumulative series, negative. The yearly `0.00` is the trap |
| `lag1_autocorrelation` | 0.2128 | 0.0933 | n/a | Clustering disclosure |
| `n_eff` | 77.894 | 10.782 | n/a | `n_periods × (1−rho)/(1+rho)`, guarded |
| `n_eff_capped` | 77.894 | 10.782 | n/a | `n_eff` limited to the trade count, because `rho < 0` can inflate it absurdly |

Read `t_stat` and `n_eff` **on the same line**. `M` reports a 13-period t-statistic of 0.948
with an effective sample of 10.8 — the honest confidence is nearer 11 periods than 13.

`median_period_pnl` vs `mean_period_pnl` on `M`: 66.36 vs 131.41. The mean is roughly twice the
median, which says the monthly series is carried by a minority of months. That is a
distribution-shape warning the t-statistic does not give you, sitting one row above it.

### `[verdict inputs]`

`verdict eligible` (`yes`/`no`) and `noise flag`. The engine shortens the noise string to
`NOISE (|t|<2)` in the table for width; the full phrase `NOT DISTINGUISHABLE FROM NOISE`
appears in the VERDICT section and in `--json`.

### `[return basis (--capital)]` — only with `--capital`

`capital`, `cumulative_return_pct`, `max_drawdown_pct`, `annualised_return_simple_pct`. With
`--capital 250000` the `M` bucket reports `cumulative_return_pct = 0.683`,
`max_drawdown_pct = -0.663` and `annualised_return_simple_pct = 0.631`.

**Two warnings attached to those three numbers.** They are simple, not compounded. And they are
only as honest as the capital figure: a starting equity that ignores deposits, withdrawals and
concurrent positions makes every return below it fiction. The engine prints that warning itself.

## 5 — VERDICT

Four things, in order:

```
RULE                — the gate and the noise band, restated, so it can be argued with
VERDICT: M          — the named bucket, the |t_stat| ordering, the status line
CONFIDENCE CAPPED   — n_periods and n_eff and n_eff_capped on one line
DID NOT QUALIFY     — per bucket, the constraint that failed
PER-BUCKET NOISE    — every bucket's noise-band status
DEPENDENCE CAVEAT   — printed unconditionally
```

For the illustrative log:

```
VERDICT: M is the most reliable review timeframe for this book.
         highest |t_stat| (0.948) among the 1 bucket(s) satisfying n_periods >= 12
         and trades_per_period >= 5
         t_stat = 0.948 over n_periods = 13; trades_per_period = 9.23
         status: NOT DISTINGUISHABLE FROM NOISE

CONFIDENCE IS CAPPED BY DEPENDENCE -- n_periods = 13, n_eff = 10.78 (capped: 10.78)

Buckets that did NOT qualify:
  D    : trades_per_period=1.00 < 5
  W    : trades_per_period=2.26 < 5
  2W   : trades_per_period=4.44 < 5
  Q    : n_periods=5 < 12
  H    : n_periods=3 < 12
  Y    : n_periods=2 < 12
```

**Read the "did NOT qualify" list as the finding, not as an obstacle.** It is a turnover
statement: at this book's trade rate, no bucket has both enough periods and enough trades per
period to support a claim. `2W` at 4.44 trades per period is the near miss, and the honest
conclusion is *fifteen more trades would have put 27 periods at exactly 5.00 trades per
period* — not *run
2W and ignore the gate*.

If **no** bucket qualifies, the verdict reads `INSUFFICIENT DATA` and the same per-bucket list
is printed. That is the output for the six-trade hand-check fixture, and it is the correct
output: six trades over two months cannot answer a timeframe question.

## 6 — BEAT LOSSES TEST

A compact table, one row per bucket, all rows identical — with a printed explanation that this
test is bucketing-invariant by construction. Then a per-bucket sentence:

```
M  edge of 0.0612 is inside 2 x se_win_rate (0.0908): the win rate is NOT
   distinguishable from its own break-even. More periods will not fix this;
   more INDEPENDENT trades will.
```

That sentence is deliberately blunt. `More periods will not fix this` is the answer to
"should I review weekly or monthly?" when the real problem is the trade count.

## 7 — PERIOD SERIES (CSV) — with `--csv`

One CSV block per bucket, each preceded by a comment line naming the bucket:

```
# bucket=M  calendar month  (13 period rows)
bucket,period,period_label,n_trades,gross_profit,gross_loss,net_pnl,wins,losses,
breakeven_trades,win_rate,avg_win,avg_loss,payoff_ratio,expectancy_per_trade,
profit_factor,break_even_win_rate,edge,cumulative_pnl,drawdown_from_peak
```

`cumulative_pnl` and `drawdown_from_peak` are the two columns the summary table cannot give
you per period: they let you name the peak period and the trough period of the maximum
drawdown, which is what makes a drawdown actionable. Empty fields mean `n/a` (a one-sided
period has no payoff ratio, hence no break-even win rate and no edge). `--csv-out FILE` writes
all buckets into one file with the `bucket` column as the first field.

`--periods` prints the same series as an aligned human table instead.

## 8 — RETURN-BASED NOTE — with `--capital`

Restates the basis and the fiction warning.

## A five-minute reading routine

1. **Provenance.** Is the log labelled? Is `trade rows` right?
2. **Span.** Does the close-date range match your expectation?
3. **`n_trades` row.** Same in all seven columns?
4. **`cumulative_pnl` row.** Same in all seven columns, and equal to total trade P&L?
5. **Verdict.** Which bucket, and what did the others fail on?
6. **`t_stat` and `n_eff` together.** Then the noise-band status.
7. **`max_drawdown` at the finest bucket with a defensible `trades_per_period`.**
8. **Beat-losses sentence.** `PASS` or `FAIL`, and the edge measured against `2 × se`.

If steps 3 or 4 fail, stop. Nothing after them is trustworthy.
