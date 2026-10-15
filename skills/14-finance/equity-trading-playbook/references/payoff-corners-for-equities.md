# Payoff corners for equities and ETFs

A **payoff corner** is the pair `(b, p)` a set of rules mechanically buys — the payoff ratio and the
win rate. Everything else about a strategy (the entry pattern, the indicator, the timeframe, the
instrument) exists to produce one of a small number of corners. Two strategies with different stories
and the same corner are the same bet.

This file maps the corners available to an equity or ETF book, derives each one's arithmetic, and
states what each corner asks of the regime.

## The arithmetic, stated once

In R units, where `R` is the planned risk per trade:

| Quantity | Formula | Meaning |
|---|---|---|
| `b` | `tp / sl` | the payoff ratio the rules produce |
| `E` | `p*b − (1−p)` | expectancy per trade, in R |
| `b*` | `(1−p)/p` | the payoff ratio at which the corner breaks even |
| `p*` | `1/(1+b)` | the win rate at which the corner breaks even |
| `f*` | `E/b` | the Kelly fraction (negative when `E` is) |
| `sd²` | `p(b−E)² + (1−p)(−1−E)²` | two-point variance of the outcome set `{+b, −1}` |
| `n_req` | `4(sd/|E|)²` | trades needed for the mean to reach +2σ |

`E = p*b − (1−p)` is exact only when the average loss is exactly `−1R`. When a book's realised
average loss is `−L_mag R` with `L_mag` not equal to 1, the closed form becomes
`E = L_mag * (p*b − (1−p))` and the truth is the sample mean of the R-multiples. **Compute the sample
mean.** It is always right, and it is the only figure that survives a book whose stops slip.

## The corner table

Every row below is derived, not asserted. `p*` follows from `b` alone; `E` follows from `p` and `b`;
`L` is at `n = 250`; `R_max` is at `D_tol = 20%` of equity and `safety = 1.5`.

| Corner | `b` | `p*` | assumed `p` | `E` at assumed `p` | `sd` | `n_req` (E>0) | `L` | `R_max` |
|---|---|---|---|---|---|---|---|---|
| Trend / breakout, 1R stop, 3R target | 3.00 | **0.250000** | 0.40 | **+0.600000R** | 1.959592 | 42.667 | 10.809 | **1.2336%** |
| Trend / breakout, 1R stop, 2R target | 2.00 | **0.333333** | 0.40 | **+0.200000R** | 1.469694 | 216.000 | 10.809 | **1.2336%** |
| The 1:1 corner | 1.00 | **0.500000** | 0.45 | **−0.100000R** | 0.994987 | n/a (E<0) | 9.236 | 1.4437% |
| Mean reversion, 1R stop, 0.75R target | 0.75 | **0.571429** | 0.65 | **+0.137500R** | 0.834697 | 147.405 | 5.259 | 2.5351% |
| **Disposition: 0.5R TP, 1.5R stop** | 0.33 | **0.750000** | 0.62 | **−0.173333R** | 0.647182 | n/a (E<0) | 5.706 | 2.3365% |
| Event drift, gap stop, 2R target | 2.00 | 0.333333 | 0.45 | +0.350000R | 1.492481 | 77.088 | 9.236 | 1.4437% |
| Failed breakout, 2R target | 2.00 | 0.333333 | 0.42 | +0.260000R | 1.480675 | 129.728 | 10.136 | 1.3155% |

Reproduce every cell:
`py -3 scripts/payoff_check.py --tp 3.0 --sl 1.0 --p 0.40 --quiet` and so on. The tool prints the
formula under each line, so the table and the tool cannot drift apart silently.

## Why the 3R corner is the outlier

`b = 3` drops `p*` to 0.25. That is the entire reason trend following can survive a 40% hit rate:
the corner does not need to be right often, it needs to be paid well when it is. Two consequences
follow directly from the algebra and neither is intuitive:

1. **`n_req = 42.667` is the SMALLEST measurement burden in the table.** A large `b` with a
   sub-50% `p` produces a wide outcome spread (`sd = 1.959592`) but a large mean (`E = 0.60`), and
   `n_req` depends on the *ratio*. Trend corners are measurable sooner than thin mean-reversion
   corners, by a factor of about 3.5.
2. **`R_max = 1.2336%` is the SMALLEST size in the table.** `L` depends on `p` and `n` only. A 40%
   hit rate over 250 trades implies an 11-trade losing streak, and surviving 11 consecutive losses
   at a 20% drawdown tolerance allows only 1.2336% of equity per trade. **The corner that pays best
   demands the smallest size.** There is nothing paradoxical about it: it is what the streak
   arithmetic says.

## Why the disposition corner is the most common way a book bleeds

`b = 0.333333` requires `p* = 0.75`. The rules that produce it are ordinary and feel responsible:
take the profit when it is available, give the loser room. Each half of that sentence moves `b` in
the wrong direction at once — the numerator of `b` shrinks and the denominator grows — and the
product of the two moves is a break-even win rate of three in four.

At `p = 0.62` the corner loses `0.173333R` per trade. The sensitivity block on the tool shows
`p + 5pp` at 67% is *still* negative. A trader on this corner who improves their entry by two
percentage points of win rate has changed nothing they can feel: the card is still red.

**The correct response is a rules change, not a better signal.** Widening the target from 0.5R to
1.0R moves `b` from 0.333333 to 0.666667 and `p*` from 0.75 to 0.60. Tightening the stop from 1.5R
to 1.0R with the same 0.5R target moves `b` to 0.50 and `p*` to 0.667. Either is a today change.

## Why payoff and win rate are not interchangeable levers

Differentiate `E = p*b − (1−p)`:

```
dE/dp = b + 1          (R per unit of p)
dE/db = p              (R per unit of b)
```

So one **full unit** (100 percentage points) of win rate is worth `(b+1)/p` units of payoff ratio.
For the corners above:

| Corner | `(b+1)/p` | Reading |
|---|---|---|
| `b = 3`, `p = 0.40` | **10.000** | 100pp of win rate ≡ 10.0 units of `b`. One point of win rate ≡ 0.10 units of `b` — 3.3% of the payoff ratio |
| `b = 2`, `p = 0.40` | **7.500** | one point of win rate ≡ 0.075 units of `b` — 3.8% of it |
| `b = 1`, `p = 0.45` | **4.444** | on a 1:1 card, win rate and payoff are nearly the same kind of lever — which is exactly why a 1:1 card has no room to manoeuvre |
| `b = 0.75`, `p = 0.65` | **2.692** | on a thin mean-reversion corner, payoff is by far the cheaper lever |
| `b = 0.333333`, `p = 0.62` | **2.151** | on the disposition corner, a 1.0-unit payoff improvement is worth 2.15 units of win rate |

**Fix payoff first.** `dE/db = p` is a coefficient you can change *today* — widen the target, tighten
the stop, remove a cap on the winner. `dE/dp = b + 1` is a coefficient you can only change by having
a better signal, which is a research programme measured over `n_req` trades. The payoff lever is
available now and its arithmetic is visible before a single trade is taken; the win-rate lever is
neither.

## What a corner is not

A corner does not know the instrument, the regime, the timeframe, or the reason the market paid. Two
corners with the same `(b, p)` are the same arithmetic and the same risk, whatever the story
attached to them. The story decides whether `p` is *achievable*; the arithmetic decides whether it
is *enough*. This file is only the second half of that sentence.

## Cross-references

- Which corner pays in which regime: `regime-to-strategy-map.md`
- The break-even algebra in full, and the disposition trap in detail:
  `break-even-payoff-and-the-disposition-trap.md`
- The stop and target distances that produce each `b`: `stop-and-target-arithmetic.md`
- Streak survival per corner: `streak-survival-by-corner.md`
- Cost drag, which bites the tight-stop corners: `cost-drag-and-stop-distance.md`
- Concrete cards, one per corner: `strategy-cards.md`
