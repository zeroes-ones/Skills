# P&L and Drawdown by Period

**Portability target:** spec-level. Drawdown here is a property of one cumulative series of
currency amounts. No benchmark, no index, no risk-free rate.

## Two different P&L series live in this skill

They are easy to confuse and they answer different questions.

| Series | How it is built | What it answers |
|---|---|---|
| **Per-period realised P&L** | Sum the `pnl` of every trade whose `close_date` falls in the period | "How much did the book actually realise in this period?" |
| **Cumulative P&L** | The running sum of the per-period series, in chronological order | "Where did the book's realised equity go, in order?" |

The engine's `net_pnl` and `cumulative_pnl` are exactly these two things at bucket level, and
`sum(net_pnl)` over all periods equals the total trade P&L for any bucket — a property worth
checking as a reconciliation, because it is the one thing that must hold for every bucketing
of the same trades. On the shipped illustrative log every bucket reports
`cumulative_pnl = 1,708.39` and `net_pnl = 1,708.39`, because both are the total. [COMPUTED]

## Maximum drawdown as this engine defines it

```
walk the cumulative series in chronological order
start: peak = 0, cum = 0, worst = 0
for each period:
    cum  += net_pnl(period)
    peak  = max(peak, cum)
    worst = min(worst, cum − peak)
max_drawdown = worst          # a NEGATIVE currency amount
```

Three decisions are baked into that pseudo-code, and each is arguable:

**1. The running equity starts at zero and zero is the initial peak.** So a loss in the very
first period registers as a drawdown. The alternative — taking the first period's end value as
the starting peak — would hide the first period's loss, which is how a book that lost money
in month 1 and recovered in month 6 can report a maximum drawdown of zero. **A first-period
loss is a drawdown from the capital you actually started with.**

**2. It is reported as a negative number.** `max_drawdown` = −1,656.33 means the cumulative
series fell 1,656.33 currency units from its highest point to the lowest point after it. This
matches the negative-drawdown convention (`Max DD: −15.9%`) used by
`trade-performance-analyst`, so the two skills' figures can be read side by side without a
sign flip. The magnitude is the depth.

**3. It is peak-to-trough, not peak-to-end.** A book that fell 1,656 and recovered has still
had a 1,656 drawdown. Recovery is a separate fact that this engine does not report — the
water is as deep as the deepest point, regardless of where you ended up.

## What the bucket choice does to drawdown — the shipped log

Engine output, `examples/logs/illustrative-year-synthetic.csv` (**synthetic, illustrative, no
market information**), pasted from `examples/run-output.txt`:

| Bucket | n_periods | `max_drawdown` |
|---|---|---|
| `D` | 120 | −2,007.03 |
| `W` | 53 | −1,859.05 |
| `2W` | 27 | −1,853.02 |
| `M` | 13 | −1,656.33 |
| `Q` | 5 | −1,082.85 |
| `H` | 3 | −1,082.85 |
| `Y` | 2 | 0.00 |

This table is the single most useful thing the engine produces, and it says four things:

**1. Monthly data understates the drawdown by roughly a fifth.**
`(2,007.03 − 1,656.33) / 1,656.33 = 21.17%`. [COMPUTED] The daily series shows a 2,007
peak-to-trough fall; the monthly series shows 1,656. The 352 units of difference happened
*within* months and are invisible to a monthly review.

**2. That uplift is BELOW the 1.3–1.5× band cited by `trade-performance-analyst`.**
Its reference material prescribes multiplying a monthly drawdown estimate by 1.3–1.5 to
approximate the intra-month trough. On this log the realised ratio is `2,007.03 / 1,656.33 =
1.2117` — inside the direction the band predicts but below its floor. [COMPUTED] Two honest
readings, and the second is the important one:

- The band is a rule of thumb for a book whose intra-month excursions differ materially from
  its month-ending marks. This synthetic book's losses cluster into *multi-day* runs, which a
  daily bucket captures but a monthly book can partly absorb.
- **One synthetic log cannot confirm or refute a band that came from elsewhere.** This is
  [ILLUSTRATIVE] evidence about the engine's behaviour, not evidence about market drawdowns.
  Do not cite it as a counter-example to anything.

**3. Quarterly and half-yearly buckets report the SAME drawdown (−1,082.85).** That happens
when the deepest fall is inside a single quarter, so both coarser buckets see only the
cumulative fall across that quarter's start and end. Coarser buckets do not show "less
drawdown"; they show a *different and smaller* statistic, sometimes one that barely resembles
the path.

**4. The yearly bucket reports `max_drawdown = 0.00`.** With two yearly periods and both
years positive, there is no peak-to-trough fall at yearly resolution. The book still had a
2,007 drawdown. **A yearly review that sees a 0.00 drawdown while the daily record shows
2,007 is a review that cannot see risk at all.** This is the sharpest argument for choosing
the bucket from the holding period rather than from convenience.

## The 1.3–1.5× adjustment, attributed properly

`trade-performance-analyst` owns this: its SKILL.md states that monthly drawdown data misses
intra-month troughs and understates true risk by 20–50%, and prescribes multiplying a
monthly-only estimate by **1.3–1.5×** as a rough adjustment, with daily data preferred
whenever available. Its reference `references/drawdown-analysis.md` carries the fuller
methodology.

This skill does **not** redefine, re-derive or re-cite that band as if it were new. It cites
the owning skill and adds only what the timeframe question needs: *the finest bucket with
enough trades per period is the one whose drawdown you should believe; if you are forced onto
a coarse bucket, apply the owning skill's band and label the result an estimate.*

`[ESTIMATED]` Applied to this log: 1.3 × 1,656.33 = 2,153.23 and 1.5 × 1,656.33 = 2,484.49.
Both bracket the 2,007.03 the daily bucket actually measured, so the band behaves as
advertised here — but that is a coincidence of this synthetic book, not a validation of the
rule. The band belongs to `trade-performance-analyst`; the attribution matters more than the
arithmetic.

## Why drawdown is a path statistic, and why that breaks coarse buckets

Drawdown depends on **order**. Consider three losses of 100:

| Order | Cumulative series | Max drawdown |
|---|---|---|
| 100, 100, 100 | 0, 100, 0, −100 | −100 |
| Same three losses, spread one per quarter | 0, 100, 100, 100 | 0 |

Same trades, same total P&L, same trade count. One sequence has a drawdown, the other has
none. Coarsening the bucket *changes the order information available* — periods that used to
interleave now merge into one number, and a sequence of three losses inside one period
becomes a single smaller-looking figure at period level.

This is also why `lag1_autocorrelation` and `max_drawdown` must be read together. A high
positive `rho` says losses cluster; clustering is what creates drawdown; and clustering is
exactly what a coarse bucket discards. The engine prints both, in the same table, one row
apart, for that reason.

## Reconciling the two series

Before quoting any drawdown figure, three checks that catch nearly every error:

1. **`sum(net_pnl) == total trade P&L`** for every bucket. If a bucket fails, a trade was
   dropped or double-counted and nothing downstream is trustworthy.
2. **`max_drawdown` should become less negative as the bucket coarsens**, never more. A coarse
   bucket showing a *deeper* drawdown than a fine one means periods were sorted wrong.
3. **`max_drawdown <= −1 × (largest single-period loss)`** in magnitude. The deepest fall
   cannot be shallower than the worst single period inside it.

The engine does none of these checks itself; they belong in the reader's reconciliation step.
See [reading-the-engine-output.md](reading-the-engine-output.md).

## Failure modes around period P&L and drawdown

1. **Failure mode: a drawdown quoted from a bucket that could not see it.** A 0.00 yearly
   drawdown on a book that fell 2,007. Countermeasure: quote drawdown only from the finest
   bucket with acceptable `trades_per_period`, and name the bucket in the sentence.
2. **Failure mode: the drawdown's start and trough dates are not recorded.** A depth with no
   dates cannot be investigated. Countermeasure: read the period series and name the peak
   period and the trough period; both are in the `--csv` output.
3. **Failure mode: recovery is assumed.** Depth is not duration. Countermeasure: state the
   recovery separately, or state that the series had not recovered by the last period.
4. **Failure mode: a drawdown expressed as a percentage of the wrong base.** A −1,656.33
   drawdown against a 250,000 account is −0.663% of capital [COMPUTED, --capital 250000], but
   against a *peak equity* that had already grown it is a different number. Countermeasure:
   state the base in the same sentence as the percentage.
5. **Failure mode: deposits and withdrawals treated as P&L.** A funded account's cumulative
   series jumps. Countermeasure: this engine reads only realised trade P&L; if the ledger
   contains cashflows, exclude them or the series is not a P&L series.
6. **Failure mode: the worst single trade is mistaken for the drawdown.** One −2.40R tail loss
   is a heavy period, not necessarily a peak-to-trough fall. Countermeasure: read the series,
   not the maximum row.
7. **Failure mode: `max_drawdown` compared across books with different capital and different
   risk per trade.** A −2,007 drawdown on a book risking 110/trade and a −2,007 drawdown on a
   book risking 1,100/trade are not the same event. Countermeasure: express in R where the
   `risk` column exists, or normalise by capital, and state which.
8. **Failure mode: the intra-period trough of the *coarsest* bucket quoted as the book's risk.**
   Countermeasure: apply the owning skill's 1.3–1.5× band, tag it `[ESTIMATED]`, and write the
   word "estimated" in the sentence.
