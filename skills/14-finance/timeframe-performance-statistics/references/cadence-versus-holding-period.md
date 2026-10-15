# Cadence versus Holding Period

**Portability target:** spec-level. The rule below is a design rule, not a broker setting and
not a regulatory requirement. The two lifecycle skills it defers to are the authority on
position-monitoring cadence; this file states only how the *review timeframe* is derived.

## THE RULE

> **The performance-review cadence should be roughly one-quarter to one-half of the average
> holding period.**

The reasoning, in one paragraph: your statistics measure the quality of your *thesis*, and a
thesis has a life. If you review faster than a quarter of the average holding period, each
review window contains mostly entries and exits — the mechanics of getting in and out — and
you are measuring entry/exit noise rather than thesis quality. If you review slower than half
the holding period, a window can contain a thesis that opened and closed without the review
ever seeing a decision it was meant to examine. Between a quarter and a half, each review
window tends to contain at least one complete position life cycle and therefore at least one
real thesis outcome.

| Average holding period | Cadence window (¼ to ½) | Review bucket |
|---|---|---|
| 2 DTE (0DTE–3 DTE book) | under a day to 1.5 days | session-level; buckets are not the right tool |
| 7 days | 1.75 to 3.5 days | `D` (with `trades_per_period` almost certainly failing) |
| 14 days | 3.5 to 7 days | `W` |
| 30 days | 7.5 to 15 days | `W` to `2W` |
| 90 days | 22.5 to 45 days | `M` |
| 180 days | 45 to 90 days | `M` to `Q` |
| 540 days | 135 to 270 days | `Q` |
| 2 years | 6 to 12 months | `Q` to `H` |

**Worked examples the rule is stated with:**

- **An options book with a 2–30 DTE holding period.** Take the midpoint-ish working life of
  the position, not the DTE at entry: a 21-DTE credit spread often resolves in 7–14 days. The
  quarter-to-half window lands at 2–7 days, i.e. **weekly to monthly** — weekly for the
  short-DTE end of the book, monthly for the 30-DTE end.
- **A stock book with a 6–18 month holding period.** 180–540 days, so a quarter to half is
  45–270 days, i.e. **monthly to quarterly** — monthly for the 6-month end, quarterly for
  the 18-month end.

## This must agree with the two lifecycle skills, and here is how it does

`options-position-lifecycle` and `equity-position-lifecycle` already publish cadence tables.
They are the owners of position-monitoring cadence, and this skill does not overwrite them.
Read them:

- `options-position-lifecycle/references/review-cadence-by-dte-zone.md` — the DTE-zone table:
  **> 45 DTE weekly; 21–45 DTE twice a week; 8–21 DTE daily; 3–7 DTE daily plus an intraday
  gamma watch; 0–2 DTE the expiry protocol with a 15:45 ET decision deadline; LEAPS (> 365
  DTE) monthly plus every planned roll window.** Its SKILL.md also states the cadence as the
  floor and the level as the trigger, and its L4 "Expert" row reads *weekly + monthly*.
- `equity-position-lifecycle/SKILL.md` — the "Review Cadence by Time-Axis State" table:
  **the ordinary state is weekly on a fixed day**, tightening to **daily** as earnings, an
  ex-dividend date, an index reconstitution, the long-term anniversary or margin stress come
  into range, with wash-sale and qualified-dividend windows flagged at every review.
  `equity-position-lifecycle/references/equity-time-axes-cadence.md` carries the full rules.

The two cadences are **not the same quantity**, and the apparent disagreement disappears once
the distinction is named:

| | Position-monitoring cadence (the lifecycle skills) | Performance-review cadence (this skill) |
|---|---|---|
| Question | "What should I do about this open position right now?" | "Is my edge real, and at what resolution do my statistics support a claim?" |
| Unit | A single position | The whole book's realised P&L |
| Set by | Event and expiry risk (clocks) | Average holding period |
| Tightens because | A date came into range, or a level broke | Never — it is a fixed design choice |
| Result for a 2–30 DTE options book | daily to weekly, daily at short DTE | weekly to monthly |
| Result for a 6–18 month equity book | weekly in the ordinary state, daily near a clock | monthly to quarterly |

**They are compatible, and here is the compatibility test to run:**

1. **The performance review must never be faster than the position-monitoring cadence.**
   Reviewing P&L monthly is fine for a book monitored daily; reviewing P&L daily for a book
   monitored weekly is measuring marks you are not acting on.
2. **The performance review must never be slower than half the holding period.** A book whose
   positions live 14 days and are reviewed for performance annually is not being reviewed.
3. **A tightening of the monitoring cadence does not tighten the performance cadence.** A
   position entering its earnings window moves to daily *monitoring*; it does not mean your
   monthly P&L review should become daily. The two cadences answer different questions and
   the second one needs the trade count a month provides.
4. **For equities, the ordinary-state weekly monitoring cadence and the monthly-to-quarterly
   performance cadence sit in different places on purpose.** The weekly floor exists so a
   level breach is noticed; the monthly-to-quarterly performance review exists because a book
   holding positions for 6–18 months does not produce 12 independent monthly outcomes.

Where the two tables could be read as conflicting, the resolution is the holding period, not
the DTE zone: **the DTE zone governs how often you look at the position; the holding period
governs how often you look at the statistics.**

## Applying the rule to the shipped illustrative log

The log's mean holding period is **11.14 calendar days** (engine-adjacent fact, printed by
`examples/logs/generate_synthetic.py`: min 2, mean 11.14, max 21). [COMPUTED]

- One quarter of 11.14 days is 2.8 days; one half is 5.6 days.
- A cadence in that range is **weekly**.
- The engine's verdict for that log is **`M`** — not `W` — and the two are not in conflict:
  the verdict answers "which bucket's statistics are *usable*", and `W` fails the
  `trades_per_period >= 5` gate (2.26 trades per period). The rule answers "which bucket
  *should* I be reviewing". Here the rule says weekly and the data says weekly is too coarse
  to support a claim, which is a real and common finding: **the cadence you want is finer than
  the one your trade count supports.**

The response to that gap is not to move the cadence to monthly because monthly is the only
bucket that passes. The response is to run the weekly review *anyway* — as a description, with
no statistical claim attached — and to let the monthly bucket be the one that carries the
claim. The engine's verdict rule is designed to make that distinction visible rather than to
let the bucket choice be driven backwards from the answer.

## The trades-per-period versus periods-per-year trade-off

This is the central tension, and it is arithmetically unavoidable.

```
trades_per_period × n_periods = total trades      (for any bucket)
```

Total trades is fixed by the book. So **every step toward more periods is a step toward fewer
trades per period, and vice versa.** There is no bucket that maximises both.

| Bucket | Periods/year | What it buys | What it costs |
|---|---|---|---|
| `D` | 365.25 | The most periods, the fastest recognition of a regime change, the only bucket that sees intra-period order | Almost always 1 trade per period: no per-period win rate, no payoff ratio, no per-period edge, and a t-statistic across single-trade periods |
| `W` | 52.18 | ~4–8× more trades per period than daily for the same book; still fast enough to catch a bad month | 2–4× fewer periods than daily; for a book trading twice a week, still under 5 trades/period |
| `2W` | 26.09 | A middle point most books have never tried; pairs naturally with a 2-week holding period | Pairs straddle months and years; the period count in a year varies with ISO parity |
| `M` | 12 | Enough trades per period for the per-period statistics to exist; the natural reporting unit; a year of periods | 12 periods is the gate's floor, so a single bad month dominates; intra-month drawdown is invisible |
| `Q` | 4 | Large periods, so per-period statistics are stable | Four observations: `n_periods` fails the gate; a quarter *is* the sample, not a series of them |
| `H` | 2 | Almost no noise inside a period | Two observations is not a series |
| `Y` | 1 | — | One period. `sd`, `t_stat`, `period_sharpe`, `rho` and `n_eff` are all `n/a` |

The engine's gate (`n_periods >= 12` AND `trades_per_period >= 5`) is a statement about where
this trade-off usually lands. Solving it for the shipped log:

- `D` gives 120 periods at 1.00 trades/period — fails trades.
- `W` gives 53 at 2.26 — fails trades.
- `2W` gives 27 at 4.44 — **narrowly** fails trades (4.44 vs 5).
- `M` gives 13 at 9.23 — passes both. The gate's own floor.
- `Q` gives 5 at 24.00 — fails periods.

**No bucket clears both gates comfortably, and that is the honest answer for a 120-trade,
14-month book.** It is what a real, marginal book looks like. The instinct to "find the bucket
where the numbers work" is the trap; see [common-misreadings.md](common-misreadings.md).

## What fixes this, and what does not

| Action | Does it fix the trade-off? |
|---|---|
| Review the same 120 trades monthly instead of weekly | No. Same trades, fewer periods, more per period. One side of the trade-off bought, the other paid for |
| Add months to the sample (keep trading at the same rate) | Yes, partly. `n_periods` rises at fixed `trades_per_period`, so it is the only action that improves one side without costing the other |
| Increase trade frequency at the same edge | Yes for the statistics, but it changes the strategy, and it converts the book into a higher-turnover book whose payoff ratio usually falls |
| Report the best of seven buckets | No. It is a selection step, not evidence |
| Annualise a short sample | No. It changes units, not information |
| Pool several accounts or instrument classes to raise `trades_per_period` | Usually no. Mixing populations creates a series whose periods blend two different strategies — see [per-instrument-interpretation.md](per-instrument-interpretation.md) |

## Failure modes around cadence

1. **Failure mode: the cadence is set by calendar habit, not by the holding period.** Monthly
   because reports are monthly. Countermeasure: derive the cadence from the average holding
   period, compute that average from the log, and write both down.
2. **Failure mode: the cadence is set to whichever bucket has the best t-statistic.** Backward
   selection from the answer. Countermeasure: pre-commit the bucket before running.
3. **Failure mode: a review cadence faster than the strategy's own turnover.** Daily reviews of
   a book holding positions for months produces a stream of P&L noise mistaken for information.
   Countermeasure: the quarter-to-half rule.
4. **Failure mode: the monitoring cadence and the review cadence conflated.** A position
   entering earnings moves to daily monitoring, and the whole book's P&L review is dragged to
   daily with it. Countermeasure: keep the two tables separate; say which cadence a sentence is
   about.
5. **Failure mode: the average holding period computed over open positions.** Unrealised
   positions have no holding period; only closed trades do. Countermeasure: compute the mean
   over `close_date − open_date` for closed trades, which is what the `--csv` series plus the
   log's open dates give you.
6. **Failure mode: a bimodal book averaged into one cadence.** A book with 3-day swing trades
   and 12-month core positions has a mean holding period that describes neither. Countermeasure:
   split the book by holding-period class and run the engine on each, or bucket by class.
7. **Failure mode: the cadence table read as a promise that a finer review will produce
   significance.** Countermeasure: the cadence rule tells you what you *should* review; the
   verdict rule tells you what your trades *support*. They can disagree, and the shipped log
   is an example of them disagreeing.
