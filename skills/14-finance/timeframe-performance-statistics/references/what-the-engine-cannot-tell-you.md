# What the Engine Cannot Tell You

**Portability target:** spec-level. This is the limits list. It is written as hard limits, not
as a roadmap: several of these are things no calculator should claim, and the rest belong to
other skills.

Read this file before quoting any engine output. Every field the engine prints is arithmetic
on the CSV you gave it, and nothing else.

## 1. It cannot tell you whether the strategy is good

It tells you what the trade record says: counts, sums, ratios, a mean, a spread, a
t-statistic, a peak-to-trough fall. "Is this a good strategy" requires a benchmark, a
risk-free rate, a capital base, an out-of-sample period and an independent check — four of
which are outside this engine and the fifth of which is a governance question.

## 2. It has no benchmark and no risk-free rate

There is no comparison anywhere in the output. A 6.12-point edge over break-even is not
outperformance; it is arithmetic about a win rate. An S&P 500 return, a Treasury yield or a
peer's Sharpe are all absent, deliberately, because the engine has no data for them and will
not invent one.

**This is the single largest reason not to read the output as a performance report.** For
benchmark-relative and risk-adjusted work — Sharpe, Sortino, Calmar, alpha, information
ratio — the owning skill is `trade-performance-analyst`.

## 3. It refuses to annualise

No annualised Sharpe. No CAGR. No annualised volatility. `--capital` adds three simple return
figures with a printed warning, and nothing else.

The refusal is deliberate: `trade-performance-analyst` requires a lookback period, a return
frequency and a risk-free rate before a Sharpe can be stated, and this engine knows only one of
those (the frequency, from the bucket). `periods_per_year` is printed as a calendar fact, not
as a licence.

## 4. It knows nothing about fees, financing or spread

`pnl` is whatever the ledger says. If the ledger is gross, every bucket is gross, and the
agreement between buckets is worthless as evidence about net performance. The engine cannot
detect this; only the log's `# PROVENANCE:` block can say it, and only a human can verify it.

## 5. It cannot attribute P&L to anything

No by-symbol attribution in the summary (the `symbol` column is carried, not grouped). No
by-strategy, by-regime, by-DTE-bucket or by-holding-period attribution. No decomposition of
the win rate into selection versus sizing versus exits. `trade-performance-analyst` owns
attribution methodology.

## 6. It cannot see open positions or marks

It reads closed trades only. Unrealised P&L, current marks, open risk, aggregate Greeks,
margin and buying power are all invisible. A book with a large unrealised loss against a
positive realised series will look healthy in every line the engine prints.

## 7. It cannot see the path inside a period

For any bucket coarser than `D` the engine knows only the period total. Three losses inside a
month are one number. That is exactly why `max_drawdown` shrinks as the bucket coarsens, and why
the intra-period trough needs either a finer run or the coarse-bucket adjustment owned by
`trade-performance-analyst` (its SKILL.md: daily data preferred; where only monthly exists,
multiply by 1.3–1.5× and label the result an estimate).

## 8. It cannot correct for multiple comparisons

The verdict searches seven buckets and reports the best. The engine does not adjust the
threshold, does not print a Bonferroni-corrected figure and does not disclose the search beyond
naming the rule. If you look at all seven and pick one, that selection is yours to disclose.
Pre-committing the bucket from the cadence rule is the clean answer; see
[cadence-versus-holding-period.md](cadence-versus-holding-period.md).

## 9. It cannot bootstrap, resample or produce intervals

There are no confidence intervals in the output — no interval on `mean_period_pnl`, none on
`win_rate`, none on `max_drawdown`. `se_win_rate` is a standard error, not an interval, and
`2 × se_win_rate` is a threshold, not a bound. A block bootstrap of the period series would
produce honest intervals and the engine does not do one; the recipe is in
[dependence-and-autocorrelation.md](dependence-and-autocorrelation.md) if you want to.

## 10. It cannot check the log for the biases that matter most

- **Survivorship.** Trades that were never opened, ideas that were abandoned before entry, and
  instruments that were delisted do not appear. The engine sees rows; it cannot see what is
  missing from them.
- **Not-logged trades.** A discretionary trade excluded from the ledger, or a leg that was
  managed outside the log, is simply absent. Every statistic is computed on the subset someone
  chose to write down.
- **Partial exits collapsed into one row.** If a position is trimmed three times and recorded
  as one row, the log understates trade count and overstates per-trade size. The engine cannot
  detect it; the `n_trades` reconciliation against the broker's trade blotter can.
- **Look-ahead in the log itself.** Backfilled dates, `open_date` set to the date the idea was
  first remembered rather than the date of the fill, or `pnl` computed from a later price.
- **Selection of the sample window.** The log starts when the trader started keeping it, which
  is usually after a good month.

None of these are detectable from inside the file. The countermeasure is reconciliation against
an independent record — `trading-decision-data-catalogue` owns which sources those are, and
`verification-independence-engineer` owns who checks the work.

## 11. It cannot tell you whether the trades were independent of each other

`lag1_autocorrelation` measures one lag on the period series. Two correlated positions held at
the same time, a single macro event that hits five names, or a book that is really one bet
expressed five ways are all invisible at period level, because period P&L is a sum.

A book with 120 trades that were really 20 decisions will report 120 trades and a
trade-count-based `se_win_rate`. **The engine's `N` is a row count, not an independent-decision
count.**

## 12. It cannot decide what the risk unit was

The `risk` column is carried through the pipeline and used for nothing. R-multiple framing —
"did the average loss come in at the risk I planned" — requires comparing `pnl` to `risk`
per trade, which is a per-trade question, not a bucket question. `trade-sizing-recovery` owns
sizing and loss bands; `portfolio-signal-manager` owns position sizing across the book.

## 13. It cannot grade the review process

The engine says nothing about whether reviews happened, whether written exit levels were
honoured, whether the cadence was met, or whether the plan matched the action. That record
belongs to the review log kept on the monitoring cadence owned by
`options-position-lifecycle` and `equity-position-lifecycle`.

## 14. It cannot see regimes

It buckets by calendar, not by market state. A 13-month sample may contain a bull market, a
correction, a bear market and a crash in unequal and unknown proportions; the engine will
report one mean across all of them. **Whether a strategy works in a regime the sample barely
contains is not answerable from the sample.** Any regime claim needs a regime label on the
trades, which the CSV does not have.

## 15. It cannot resolve ambiguity in your `close_date`

If the ledger's `close_date` is a settlement date, an expiry date, or the date an order was
placed rather than filled, every bucket is keyed to the wrong day. The engine prints the span
it found so a gross error is visible, but a systematic one-day or one-week shift is invisible
unless you know your own ledger. State the convention in the provenance block.

## 16. It has no view on whether you should be trading this book at all

The engine reports statistics. Whether the strategy should be run, at what size, with what
capital, under whose mandate and against which risk limits are four decisions owned by other
skills and, ultimately, by the person accountable for the account.

## What the engine *can* be trusted for

| Claim type | Supported? |
|---|---|
| "In these 120 closed trades, the win rate was 55.00% against a 48.88% break-even" | Yes — arithmetic on the file |
| "The monthly bucket produced 13 periods at 9.23 trades per period" | Yes |
| "The daily bucket measured a −2,007.03 peak-to-trough fall" | Yes, within that bucket's resolution |
| "The edge is statistically distinguishable from break-even" | Arithmetic says no: `edge_test = FAIL` |
| "The weekly bucket is more significant than the monthly bucket" | No — nested buckets, one body of evidence |
| "The strategy has a proven edge" | No |
| "This is how the strategy will perform next quarter" | No |
| "The book is low risk because the yearly drawdown is zero" | No — the bucket cannot see risk at that resolution |

## The honesty requirement this file exists for

Every figure the engine prints is either `[COMPUTED]` from the input file or derived arithmetically
from such a figure. The input file's provenance is the reader's responsibility. Two rules, and
they are not optional in this library:

1. **Never present an engine output as a market finding, a backtest result, or a strategy's
   expected performance.** Tag it with the provenance of the data behind it — the engine echoes
   the log's own `# PROVENANCE:` lines for exactly this purpose.
2. **Never quote a number from this skill that you have not re-run.** Thresholds, examples and
   figures in these references are illustrative of the shipped synthetic logs at fixed seed
   20260414. Change the seed and every number changes; the arithmetic does not.
