# Bucket Definitions

**Portability target:** spec-level. Every bucket below is a pure calendar function of one
date. There is no broker, venue, timezone database or vendor convention behind them, so the
definitions are reproducible on any machine and arguable by anyone.

## The one convention that decides everything

**A trade belongs to the bucket containing its `close_date`. Never its `open_date`.**

That single sentence resolves more disagreements than any other line in this skill. It is
also a choice, not a fact, so here is the reasoning and the cost:

| Why close date | What it costs |
|---|---|
| P&L is realised at the close. A period's P&L should be the P&L the period actually produced | A trade opened in March and closed in April is an April trade, so March's activity is invisible in March's statistics |
| It makes periods non-overlapping: each trade lands in exactly one period of exactly one bucket | A book that opens a 60-day position every week shows the full loss in one month and nothing in the two before it |
| It makes `sum(period net_pnl) == sum(trade pnl)` trivially true, so the bucket series reconciles to the ledger | Position activity and realised activity are different series; this engine reports only the second |

If you want an *entry-dated* view, that is a different question — "how did the trades I chose
in March do?" — and it needs its own run against an `open_date`-keyed export. Do not mix the
two in one series and then compare the bucket t-statistics; you will be comparing two
different trade sets that happen to share a file.

The engine states this convention in its own output every time it runs, so an output can
never be detached from the convention that produced it.

## The seven buckets

| Bucket | Key format | Example key | Nominal length | Periods/year |
|---|---|---|---|---|
| `D` | `YYYY-MM-DD` | `2025-03-04` | 1 day | 365.25 |
| `W` | `YYYY-Www` (ISO) | `2025-W10` | 7 days | 52.1786 |
| `2W` | anchor Monday, `YYYY-MM-DD` | `2025-03-03` | 14 days | 26.0893 |
| `M` | `YYYY-MM` | `2025-03` | 30.4375 days | 12 |
| `Q` | `YYYY-Qn` | `2025-Q1` | 91.3125 days | 4 |
| `H` | `YYYY-Hn` | `2025-H1` | 182.625 days | 2 |
| `Y` | `YYYY` | `2025` | 365.25 days | 1 |

`periods_per_year = 365.25 / nominal_length`. The month, quarter, half and year rows are
chosen so that this lands on exactly 12, 4, 2 and 1 — a nominal month of 30.4375 days is
what a twelfth of a 365.25-day year actually is. The day, week and two-week rows are the
literal calendar counts. A reader is entitled to disagree with this; that is why the divisor
is printed rather than the periods-per-year count alone.

## Day (`D`)

The key is the close date itself. Two trades closing the same day share a period.

`D` is the bucket where **`trades_per_period` is almost always 1**, which is the whole
problem with it. A single-trade period has `win_rate` of 1.0 or 0.0, no payoff ratio, no
break-even win rate and therefore no edge — every trade is its own population. The
across-period statistics (mean, sd, t-stat) still compute, but they are statistics about
*trade outcomes ordered by date*, not about any period's performance.

On the shipped 120-trade illustrative log `D` yields 120 periods at 1.00 trades per period
and fails the verdict gate on `trades_per_period` — see
[reading-the-engine-output.md](reading-the-engine-output.md).

## Week (`W`) — ISO weeks

ISO 8601 weeks: weeks start on Monday, and **week 1 of a year is the week containing the
first Thursday of that year**. That means the last days of December can belong to
`2026-W01`, and the first days of January can belong to the previous year's final week.

`2025-01-01` was a Wednesday, so ISO week 1 of 2025 ran from Monday 2024-12-30 to Sunday
2025-01-05, and ISO week 2 ran from 2025-01-06. A log whose first trade closes on
2025-01-02 therefore carries a period keyed to 2025-W01 while the trade itself is a
2024-12-30-week trade. **This is correct, not a bug**, and it is the reason the key carries
the ISO year rather than the calendar year.

`W` is the smallest bucket that usually gives more than one trade per period for a
multi-symbol book. It is the natural review unit for a strategy whose holding period is
days to a couple of weeks.

## Two-week (`2W`) — paired ISO weeks anchored on the odd week

Pairing is the one definition here that could reasonably have gone two ways, so it is
stated precisely:

1. Take the ISO week of the close date and find its Monday.
2. If that ISO week number is **even**, step back seven days to the Monday of the odd week.
3. That odd-week Monday is the **anchor**, and the anchor is the sort key.
4. The human label is `YYYY-2Wnn`, where `nn = (odd_week_number + 1) / 2` within the
   anchor's ISO year,

So odd ISO weeks always start a pair and even ISO weeks always end one. The consequence to
know about: **pairs straddle calendar months and years routinely.** On the illustrative log
the first `2W` period anchors on `2025-01-13` while the first trade closes on `2025-01-20`,
and the final period anchors on `2026-01-12`. A 2W report is not a monthly report with wider
bars, and a 2W bucket can hold 13 to 27 periods in a year depending on where the year
boundary falls.

`2W` exists because for a book with a holding period of roughly two weeks it produces a
period count near the trade count divided by the trades-per-period you actually have —
which is the trade-off every other bucket distorts. On the shipped log it yields 27 periods
at 4.44 trades per period, narrowly missing the verdict gate.

## Month (`M`), Quarter (`Q`), Half (`H`), Year (`Y`)

Calendar months, calendar quarters, calendar halves (Jan–Jun / Jul–Dec) and calendar years.
No fiscal calendars, no offset quarters, no 4-4-5 retail weeks. If your reporting year is
not the calendar year, re-key the export before bucketing rather than asking the engine to
guess a fiscal convention it cannot see.

The important property of these four is that they are **nested**: every `M` period lies
wholly inside exactly one `Q`, one `H` and one `Y`. That nesting is why a t-statistic across
`Y` periods is not an independent confirmation of a t-statistic across `M` periods — see
[dependence-and-autocorrelation.md](dependence-and-autocorrelation.md).

## Partial periods are periods

The illustrative log's final year bucket contains only the trades that closed before
2026-01-21, while its first year bucket contains a full year. Both appear as one period
each. The engine does not annualise, prorate, drop or flag partial periods, because any of
those choices would change a t-statistic silently.

**The rule that follows: compare period lengths before you compare period values.** A year
bucket whose second period is three weeks long is not a comparison; it is one real
observation and one stub. If a partial period matters, either exclude it explicitly in the
export or re-run with a bucket that does not need it.

## Boundary assignment, stated once

A trade that closes on the last calendar day of a month belongs to that month and **not** to
the next one. A trade closing at 15:59 on a Friday belongs to that ISO week, not to the next
one, whatever the settlement date says. A trade closing on 31 December belongs to that
calendar year, however the tax year treats it.

Settlement dates are a different calendar; this engine never reads them and never infers
them. If your ledger's `close_date` is the *trade* date, the buckets are trade-date buckets,
and that is the right choice for a statistics engine: a trade is a decision that closed.

## Worked assignments (all checkable on a calendar)

| Trade | `open_date` | `close_date` | `D` | `W` | `2W` anchor | `M` | `Q` | `H` | `Y` |
|---|---|---|---|---|---|---|---|---|---|
| T001 | 2025-01-06 | 2025-01-10 | 2025-01-10 | 2025-W02 | 2024-12-30 | 2025-01 | 2025-Q1 | 2025-H1 | 2025 |
| T002 | 2025-01-13 | 2025-01-17 | 2025-01-17 | 2025-W03 | 2025-01-13 | 2025-01 | 2025-Q1 | 2025-H1 | 2025 |
| T003 | 2025-01-20 | 2025-01-24 | 2025-01-24 | 2025-W04 | 2025-01-13 | 2025-01 | 2025-Q1 | 2025-H1 | 2025 |
| T004 | 2025-02-03 | 2025-02-07 | 2025-02-07 | 2025-W06 | 2025-01-27 | 2025-02 | 2025-Q1 | 2025-H1 | 2025 |
| T005 | 2025-02-10 | 2025-02-14 | 2025-02-14 | 2025-W07 | 2025-02-10 | 2025-02 | 2025-Q1 | 2025-H1 | 2025 |
| T006 | 2025-02-17 | 2025-02-21 | 2025-02-21 | 2025-W08 | 2025-02-10 | 2025-02 | 2025-Q1 | 2025-H1 | 2025 |

These are the six rows of `examples/logs/hand-check-synthetic.csv`, and the engine's own
output for them is in `examples/run-output.txt`. Note T002 and T003 share a `2W` pair and
T005 and T006 share the next one: pairing is by ISO week parity, not by "every two weeks of
data".

## Why the keys sort

Every key format above sorts lexicographically into chronological order:
`2024-2W01` before `2025-2W02`; `2025-W02` before `2025-W10` because the week number is
zero-padded; `2025-01` before `2026-01`. That is the reason `2W` uses the anchor date as its
sort key rather than the `YYYY-2Wnn` label — a label alone would sort `2025-2W02` before
`2024-2W01` only by accident of the year prefix, and would break the moment a pair's ISO
year and its label year disagreed across a boundary.

## What this file deliberately does not define

`D`, `W`, `2W`, `M`, `Q`, `H`, `Y` are **review** timeframes. They are not:
holding periods, DTE zones, option expiration cycles, tax years, fiscal quarters, or
settlement cycles. Three of those belong to other skills and the fourth belongs to a
calendar the exchange publishes. See `## Cross-Skill Coordination` in `SKILL.md`.
