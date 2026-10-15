# Break-even payoff and the disposition trap

`b* = (1−p)/p` is the payoff ratio at which a strategy breaks even. `p* = 1/(1+b)` is the win rate
at which it breaks even. They are the same equation rearranged, and between them they answer the
only question that matters before capital is risked: **is the payoff my rules produce enough for the
win rate I actually have?**

## The identities

```
E  = p*b - (1-p)         expectancy per trade, in R
   = p*(b - b*)          equivalently, in units of the win rate above break-even
   = (b + 1)*(p - p*)    equivalently, in units of the win rate above break-even

b* = (1-p)/p
p* = 1/(1+b)
E  = 0  <=>  b = b*  <=>  p = p*  <=>  p*b = 1 - p
```

The third line is worth stating plainly: on this arithmetic, break-even is the condition
`p*b = (1−p)`, i.e. **the expected win in R equals the probability of losing at all.** A card with
`b = 3` breaks even when `p*3 = 1−p`, i.e. `4p = 1`, i.e. `p = 0.25`.

## The break-even table

For each payoff ratio, the win rate required. Nothing here is a recommendation; it is the algebra.

| `b` | `p*` | What the corner needs | Retail frequency |
|---|---|---|---|
| 0.25 | 0.800000 | 4 of 5 trades must win | rare, and usually unintentional |
| 0.33 | **0.750000** | **3 of 4 must win** — the disposition profile | very common |
| 0.50 | 0.666667 | 2 of 3 | common |
| 0.75 | 0.571429 | 4 of 7 | common (mean reversion) |
| 1.00 | **0.500000** | a coin flip | the most common card of all |
| 1.50 | 0.400000 | 2 of 5 | — |
| 2.00 | **0.333333** | 1 of 3 | breakout / event |
| 3.00 | **0.250000** | 1 of 4 | trend following |
| 4.00 | 0.200000 | 1 of 5 | long-horizon trend |
| 10.00 | 0.090909 | 1 in 11 | tail-driven, and rarely equity |

Read the table from the `b` column: **the win rate a card needs is a property of the card's exits,
and of nothing else.** No amount of analysis of entries changes `p*`.

## The disposition trap, derived in full

The trap is a pair of ordinary, individually reasonable rules:

- take the profit early, at about 0.5R — "don't let a winner turn into a loser";
- give the loser room, to about 1.5R — "don't get shaken out".

Both rules are stated in R, so the corner they produce is exact: `b = 0.5/1.5 = 0.333333`, hence
`p* = 1/(1+0.333333) = 0.75`. Worked at a 62% hit rate with a 2% cost drag:

| Step | Formula | Value |
|---|---|---|
| payoff ratio | `0.5/1.5` | `b = 0.333333` |
| break-even payoff | `(1−0.62)/0.62 = 0.38/0.62` | `b* = 0.612903` |
| break-even win rate | `1/(1+0.333333)` | **`p* = 0.750000`** |
| expectancy | `0.62*0.333333 − 0.38 = 0.206667 − 0.38` | `E = −0.173333R` |
| net expectancy | `−0.173333 − 0.02` | `E_net = −0.193333R` |
| Kelly | `−0.173333/0.333333` | `f* = −0.520000` |
| gap to break-even | `0.62 − 0.75` | **−0.130000 win-rate points** |

A trader on this card needs **thirteen percentage points more win rate** than they have. There is no
discipline that closes a thirteen-point gap; there is only a rules change.

## Why the trap is invisible from inside

Four features make it self-concealing, and all four are arithmetic rather than psychological:

1. **The win rate is high, and high win rates feel like skill.** 62% is above the 50% that a coin
   flip provides, and above most people's intuition of "break-even". It is *below* this card's 75%.
   The comparison that matters is against `p*`, never against 50%.
2. **The average win is positive and the average loss is bigger, in a ratio that is easy to misread.**
   Winning 0.5R twice as often as losing 1.5R sounds like a wash. It is not: `p*b = 0.62*0.333333 =
   0.206667` against `1 − p = 0.38`.
3. **Losing streaks look short, so the card feels safe.** `L = ln(250)/ln(2.631579) = 5.706` — about
   6 losses in a row, at 250 trades. The *streak* is comfortable; the *mean* is not. Comfortable
   streaks are exactly what a small `b` buys, and it is not a gift.
4. **The sample never gets large enough to contradict it.** With `E < 0`, `n_req` is reported `n/a`
   — no sample size reaches +2σ. There is no amount of data that will tell a disposition trader that
   their card is fine, and no amount that will show them, in the noise, that it is not.

## The three repairs, each a rules change

All three are available today. None requires a better signal.

| Repair | Change | New `b` | New `p*` | Win-rate relief |
|---|---|---|---|---|
| Widen the target to 1.0R, stop unchanged | `b = 1.0/1.5 = 0.666667` | 0.666667 | **0.600000** | needs 60% instead of 75% |
| Tighten the stop to 1.0R, target unchanged | `b = 0.5/1.0 = 0.500000` | 0.500000 | **0.666667** | needs 66.7% |
| Do both: 1.0R target, 1.0R stop | `b = 1.0/1.0 = 1.000000` | 1.000000 | **0.500000** | back to a coin flip |
| Do both, asymmetric: 2.0R target, 1.0R stop | `b = 2.0/1.0 = 2.000000` | 2.000000 | **0.333333** | needs 33.3% |

At the *unchanged* assumed `p = 0.62`:

| Repair | `E` at `p = 0.62` |
|---|---|
| none (0.5R / 1.5R) | `0.62*0.333333 − 0.38 = **−0.173333R**` |
| 1.0R target on a 1.5R stop | `0.62*0.666667 − 0.38 = **+0.033333R**` |
| 0.5R target on a 1.0R stop | `0.62*0.500000 − 0.38 = **−0.070000R**` |
| 1.0R target on a 1.0R stop | `0.62*1.000000 − 0.38 = **+0.240000R**` |
| 2.0R target on a 1.0R stop | `0.62*2.000000 − 0.38 = **+0.860000R**` |

**Same entries. Same win rate. Same trader.** The exits move the card from `−0.173333R` to
`+0.860000R`.

## The honest caveat on the repairs

Each repair trades one problem for another, and the trade is not free:

- **Widening the target lowers the realised `p`**, because fewer trades reach a farther target. The
  table above holds `p` fixed precisely to isolate the payoff lever; in the market, `p` and `b` move
  against each other. Whether the net effect is positive is an empirical question, and the answer
  requires the `n_req` measurement in `the-iteration-protocol.md`, not a back-of-envelope.
- **Tightening the stop raises `c_R`, because `c_R = bps/(100*stop_pct)`.** A 5 bps round trip on a
  stop tightened from 1.5R-in-price to 1.0R-in-price raises cost drag by 50%. See
  `cost-drag-and-stop-distance.md`.
- **Tightening the stop can turn winners into losers**, which is a `p` problem in disguise, and it is
  measured, not assumed.

The disposition trap's lesson is not "wide targets are good". It is that **`p*` is decided by the
exits, so a card whose exits imply `p* = 0.75` is a card that has already lost the argument.**

## Cross-references

- The corner table these derivations come from: `payoff-corners-for-equities.md`
- The exits that produce each `b`: `stop-and-target-arithmetic.md`
- Measuring whether a repair worked without fooling yourself: `the-iteration-protocol.md`,
  `overfitting-by-iteration.md`
- Why a high win rate is not evidence: `what-this-cannot-promise.md`
