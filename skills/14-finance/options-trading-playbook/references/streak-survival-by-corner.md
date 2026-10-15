# Streak Survival by Corner

Every corner produces losing streaks, and the length of the streak is a function
of the win rate alone. This file derives the expected longest streak, turns it
into the largest risk per trade a streak of that length can be survived at, and
shows why the two central options corners need **different** risk per trade. Every
number is `[COMPUTED]`.

**Scope.** This file owns the *derivation* of one number — `R_max`, the largest
risk per trade a streak of length `L` can be survived at, given a drawdown
tolerance. It does not own the size you actually place. Size bands, ladders and
recovery protocols are `trade-sizing-recovery`; the book's aggregate exposure is
`options-risk-engineer`. What follows is an upper bound, not an instruction.

---

## The formula

```
L     = ceil( ln(N) / ln(1/(1-p)) )        expected longest losing streak
R_max = D_tol / (L x safety)               largest risk per trade, as a
                                           fraction of equity
```

- `N` — the number of trades over which the streak can occur (a year, a cycle).
- `p` — the win rate, as a fraction. `1/(1-p)` is the reciprocal of the loss rate.
- `D_tol` — the fraction of equity the method may lose before it is abandoned.
  A percentage, not a currency amount.
- `safety` — a multiple on the streak, because `L` is an *expectation* and the
  realised streak can be longer.

The ceiling is deliberate. `ln(N)/ln(1/(1−p))` is the expected maximum; rounding
it down would understate the streak you must survive. `payoff_check.py` prints the
raw value beside the ceiling so the rounding is auditable.

---

## The streak table

`L` at `N = 250` and `N = 500`, with `R_max` at `D_tol = 20%` and `safety = 1.5`
(`[COMPUTED]`, and the tool's own output):

| `p` | Loss rate | `L` at N=250 | `L` at N=500 | `R_max` at N=250 | `R_max` at N=500 |
|---|---|---|---|---|---|
| 0.20 | 0.80 | 25 | 28 | 0.53% | 0.48% |
| 0.30 | 0.70 | 16 | 18 | 0.83% | 0.74% |
| **0.35** | 0.65 | **13** | 15 | **1.03%** | 0.89% |
| 0.40 | 0.60 | 11 | 13 | 1.21% | 1.03% |
| **0.50** | 0.50 | **8** | 9 | **1.67%** | 1.48% |
| 0.60 | 0.40 | 7 | 7 | 1.90% | 1.90% |
| 0.70 | 0.30 | 5 | 6 | 2.67% | 2.22% |
| **0.80** | 0.20 | **4** | 4 | **3.33%** | 3.33% |
| 0.85 | 0.15 | 3 | 4 | 4.44% | 3.33% |
| 0.90 | 0.10 | 3 | 3 | 4.44% | 4.44% |
| 0.95 | 0.05 | 2 | 3 | 6.67% | 4.44% |

Check any row by hand. At `p = 0.35`: `ln(250)/ln(1/0.65) = 5.521461/0.430783 =
12.817` → `ceil = 13`. `R_max = 0.20/(13 × 1.5) = 0.20/19.5 = 1.03%`.
At `p = 0.50`: `5.521461/0.693147 = 7.966` → `8`. `0.20/(8 × 1.5) = 1.67%`.
At `p = 0.80`: `5.521461/1.609438 = 3.431` → `4`. `0.20/(4 × 1.5) = 3.33%`.

---

## The consequence: the two corners need different risk per trade

Read the `p = 0.35` row and the `p = 0.80` row together.

| | Low-p / high-b corner | High-p / low-b corner |
|---|---|---|
| Typical card | 1R stop, 2.5R target (`b = 2.5`) | 0.5×C target, 2×C stop (`b = 0.25`) |
| Break-even win rate | 28.6% | 80.0% |
| Expected longest streak at `N = 250` | **13 losses** | **4 losses** |
| `R_max` at `D_tol = 20%`, `safety = 1.5` | **1.03%** of equity | **3.33%** of equity |
| Ratio of permissible risk | 1.0 | **3.2×** |

**A 13-loss streak at 1% risk per trade is a 13% drawdown. A 4-loss streak at 3.3%
risk per trade is also a 13% drawdown.** The two corners land in the same place
because the risk per trade was set to match the streak, not to match a feeling
about the trade.

This is the arithmetic answer to "why can't I size the same on every strategy?"
The streak length is a property of the win rate, and the win rate is set by the
corner. The high-win-rate corner earns a larger per-trade risk precisely because
its losing runs are shorter. A trader who uses 1% on a `p = 0.80` corner is
under-using a real but small allowance; a trader who uses 3.3% on a `p = 0.35`
corner is betting the account on a streak that has not happened yet.

Now the trap in the same table. Look at the `R_max` column as `p` rises: `0.53% →
1.03% → 1.67% → 2.67% → 3.33% → 6.67%`. The *permissible* risk rises as the win
rate rises — but so does the cost of being wrong about the win rate. At `p = 0.95`,
`R_max = 6.67%`; at `p = 0.90` it is `4.44%`. **A five-point win-rate estimation
error nearly double-counts on the way in and under-states the drawdown on the way
out.** The allowance is only as good as the `p` inside it.

---

## Where this bound meets Kelly

`R_max` is a *survival* bound. Kelly's `f* = E/b` is an *optimal-growth* bound.
They are different constraints and the smaller one binds.

| Card | `p` | `b` | `E` | `f*` | `R_max` | Binding constraint |
|---|---|---|---|---|---|---|
| Long premium, 2.5R target | 0.35 | 2.50 | +0.2250 | 9.00% | **1.03%** | `R_max` |
| Long premium, 2.5R target | 0.40 | 2.50 | +0.4000 | 16.00% | 1.21% | `R_max` |
| Credit, 0.5×C target, 1×C stop | 0.68 | 0.50 | +0.0200 | 4.00% | 2.67% | `R_max` |
| Credit, 0.5×C target, 1×C stop | 0.80 | 0.50 | +0.2000 | 40.00% | 3.33% | `R_max` |
| Symmetric long premium | 0.50 | 1.00 | 0.0000 | 0.00% | 1.67% | `f*` (exactly zero) |

`R_max` binds in every profitable row, and by a large margin — 1.03% versus 9.00%
on the first row. That is the honest relationship: **the streak constraint is far
tighter than the growth constraint on the corners this skill covers.** Kelly tells
you the fraction that maximises long-run growth *if you know `E` exactly*. Streak
survival tells you the fraction that keeps you solvent while you find out.

Note also the fifth row. A symmetric card has `E = 0` and `f* = 0`, so no `R_max`
rescues it: **there is no risk per trade at which a zero-expectancy card becomes
profitable.** Position sizing is a survival tool, not an edge.

---

## Streak length versus measurement

The streak table says a `p = 0.80` book should expect a 4-loss run in 250 trades.
The measurement question is different: how many trades before the *win rate itself*
is known? At `p = 0.80` with 40 trades, `se_p = sqrt(0.8 × 0.2 / 40) = 0.063`
`[COMPUTED]` — the interval is roughly 74% to 86%, and `R_max` runs from **2.67%**
to **4.44%** across it (both are the tool's own output at `p = 0.74` and `p = 0.86`).

So the sequence is: measure `p` with enough trades to narrow the interval, then read
`R_max` off the narrow interval, then place size. **Reading `R_max` off an
unmeasured `p` gives a precise-looking number with no content.** The iteration
protocol in `references/the-iteration-protocol.md` is what produces the measured
`p`; `scripts/payoff_check.py --from-log` is what reports it.

---

## Failure modes

1. **Failure mode — `L` is treated as a guarantee.** It is the expected maximum.
   Realised streaks exceed it, which is what the `safety` multiple is for. A
   `safety` of 1.0 is a decision to have no allowance for the tail.
2. **Failure mode — the same risk per trade is used across both corners.** The
   streak lengths differ by a factor of more than three. A `p = 0.35` corner sized
   at the `p = 0.80` allowance loses the account on a streak that was predicted in
   advance.
3. **Failure mode — `D_tol` is set to a number the trader would not actually
   accept.** `R_max` is a fraction of equity lost before the method is abandoned.
   If abandonment would really happen at half that, `R_max` is twice as large as it
   should be. `trade-sizing-recovery` owns the bands; this file only needs the
   honest tolerance.
4. **Failure mode — the streak is computed over the wrong `N`.** `N` is the number
   of trades the streak can occur within. A 250-trade-a-year book and a 40-trade-
   a-year book have different `L` and therefore different `R_max`, even at identical
   `p`.
5. **Failure mode — `R_max` is read off a win rate with a wide interval.** The
   allowance moves materially across a plausible interval; quoting `R_max` to two
   decimals from a 30-trade sample is false precision.
6. **Failure mode — `p = 1` is entered and `L` returns 0.** The tool reports
   `R_max: n/a` with the reason rather than dividing by zero. A win rate of 1 is a
   modelling error, not a sizing input.
7. **Failure mode — streaks are assumed to be independent across positions.** Five
   correlated short-premium structures in the same index lose together. The book's
   streak is not the per-strategy streak; `options-risk-engineer` owns the
   correlation question and the strategy consequence is that `R_max` is smaller than
   the single-strategy table says.
8. **Failure mode — a streak is "traded through" at full size to recover faster.**
   Size ladders that increase after losses are a `trade-sizing-recovery` concern,
   and the streak table is precisely why an anti-martingale rule exists: the streak
   is the worst moment to increase size.
9. **Failure mode — `R_max` is confused with a position size.** It is a cap derived
   from a tolerance. It says nothing about what a *specific* trade deserves, which
   depends on the setup class and the DTE bucket — `trade-sizing-recovery`'s
   numbers.

---

## Worked checks

```bash
# the two corners' streaks and allowances, at N = 250
py -3 scripts/payoff_check.py --tp 2.5 --sl 1.0 --p 0.35   # L = 13, R_max = 1.03%
py -3 scripts/payoff_check.py --tp 1.0 --sl 1.0 --p 0.50   # L =  8, R_max = 1.67%
py -3 scripts/payoff_check.py --tp 0.5 --sl 2.0 --p 0.80   # L =  4, R_max = 3.33%

# the allowance is only as good as the p inside it
py -3 scripts/payoff_check.py --tp 2.5 --sl 1.0 --p 0.35 --n 500   # L = 15, R_max = 0.89%
```

See also: `references/payoff-corners-for-options.md`,
`references/the-iteration-protocol.md`,
`references/what-this-cannot-promise.md`.
