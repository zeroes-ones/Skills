# Check 3 - the disposition profile: a 62% win rate that LOSES MONEY

**Status:** [ILLUSTRATIVE]. An assumed win rate on an assumed payoff corner - but this particular
card is the most common real shape in a retail equity book.

**Command:**

```
py -3 skills/14-finance/equity-trading-playbook/scripts/payoff_check.py --tp 0.5 --sl 1.5 --p 0.62 --cost-r 0.02
```

## Why this card exists

Take the profit early - at half the risk - and give the loser room, out to one and a half times the
risk. That is what "book the win, give it time to come back" does mechanically. `b = 0.5/1.5 =
0.333333`, so the break-even win rate is `p* = 1/(1+0.333333) = 0.75`. **Three out of four trades
must win.** At a 62% hit rate the card loses 0.173333R per trade before cost.

## Hand arithmetic, computed independently of the tool

| Quantity | Formula | Working | Result |
|---|---|---|---|
| `b` | `tp/sl` | `0.5/1.5` | **0.333333** |
| `E` | `p*b - (1-p)` | `0.62*0.333333 - 0.38 = 0.206667 - 0.38` | **-0.173333R** |
| `E_net` | `E - c_R` | `-0.173333 - 0.02` | **-0.193333R** |
| `b*` | `(1-p)/p` | `0.38/0.62` | **0.612903** |
| `p*` | `1/(1+b)` | `1/(1+0.333333) = 1/(4/3)` | **0.750000** |
| `f*` | `E/b` | `-0.173333/0.333333` | **-0.520000** |
| `sd` | `sqrt(p(b-E)^2 + (1-p)(-1-E)^2)` | `sqrt(0.62*0.506667^2 + 0.38*0.826667^2) = sqrt(0.159161 + 0.259684) = sqrt(0.418844)` | **0.647182** |
| `n_req` | `4*(sd/abs(E))^2` | `E < 0` | **n/a** |
| `L` at n = 250 | `ln(n)/ln(1/(1-p))` | `ln(250)/ln(2.631579) = 5.521461/0.967584` | **5.706** |
| `R_max` | `D_tol/(L*1.5)` | `20/(5.706*1.5)` | **2.3365%** |

The hand-computed `p* = 0.75` is the number to carry away. It is not an opinion about discipline; it
is what `b = 0.333333` requires, and it is why the sensitivity block shows `p + 5pp` still NEGATIVE:
even **67%** is not enough on this corner.

## Verbatim tool output

```
==============================================================================
PAYOFF CARD: tp = 0.50R   sl = 1.50R   p = 0.6200   cost = 0.0200R   n = 250   safety = 1.50
==============================================================================

PAYOFF ARITHMETIC (every line prints its own formula)
  payoff ratio b        : 0.333333
      b = tp/sl = 0.50/1.50 = 0.333333
  expectancy E          : -0.173333R
      E = p*b - (1-p) = 0.620000*0.333333 - 0.380000 = -0.173333R
  cost drag c_R         : 0.020000R
      c_R = --cost-r = 0.0200
  net expectancy E_net  : -0.193333R
      E_net = E - c_R = -0.173333 - 0.020000 = -0.193333R
  break-even payoff b*  : 0.612903
      b* = (1-p)/p = 0.380000/0.620000 = 0.612903
  break-even win rate p*: 0.750000
      p* = 1/(1+b) = 1/(1+0.333333) = 0.750000
  edge (p - p*)         : -0.130000
      edge = p - p* = 0.620000 - 0.750000 = -0.130000 (win-rate points)
  Kelly f* / half       : -0.520000 / -0.260000
      f* = E/b = -0.173333/0.333333 = -0.520000   (half-Kelly -0.260000)  -- NEGATIVE: no fraction of the bankroll is the right fraction of a negative edge.

DISTRIBUTION AND SURVIVAL (in R units)
  two-point sd          : 0.647182
      sd^2 = p*(b-E)^2 + (1-p)*(-1-E)^2 = 0.620000*(0.333333-(-0.173333))^2 + 0.380000*(-1.000000-(-0.173333))^2 = 0.620000*0.256711 + 0.380000*0.683378 = 0.418844
  trades to a 2-sigma mean : n/a
      n_req = n/a. E_net = -0.193333R is not positive, so no sample size moves the mean to +2 sigma; more trades carry you further from break-even, not closer.
  years at pace         : n/a
      pacing needs n_req.
  expected worst streak L  : 5.706
      L ~ ln(n)/ln(1/(1-p)) = ln(250.0)/ln(2.631579) = 5.521461/0.967584 = 5.706 consecutive losses
  R_max (risk/trade)    : 2.3365%
      R_max = D_tol/(L*safety) = 20.0000%/(5.706*1.50) = 2.3365% of equity per trade
  break-even cost c_R*  : n/a
      E <= 0, so there is no positive cost at which the corner breaks even. Cost only adds to the loss.

  sd guard: sd is a TWO-POINT distribution sd -- it knows only {win at +b, loss at -1}. It is not the sample sd of your realised R-multiples, which is larger because real exits land between the two points. n_req derived from it is a FLOOR on the sample you need, never a target.
  COST SHIFTS THE MEAN, NOT THE SPREAD. Net outcomes are (b - c_R) and (-1 - c_R), so sd^2 = p*(b-c_R-E_net)^2 + (1-p)*(-1-c_R-E_net)^2 reduces algebraically to the same p*(b-E)^2 + (1-p)*(-1-E)^2. A cost increase moves E down and leaves sd, and therefore n_req's numerator, where it was.

VERDICT: NEGATIVE
  NEGATIVE. the corner is already negative before cost (E = -0.173333R). Do NOT trade this card at this p. Either the payoff ratio or the win rate has to change; position size cannot rescue a negative expectancy, it only scales the loss.

SENSITIVITY (one lever at a time; everything else held fixed)
  lever                 b          p        c_R     E_net(R)  verdict    n_req
  p - 5pp           0.333     0.5700     0.0200      -0.2600  NEGATIVE   n/a
  p + 5pp           0.333     0.6700     0.0200      -0.1267  NEGATIVE   n/a
  b - 0.25          0.083     0.6200     0.0200      -0.3483  NEGATIVE   n/a
  b + 0.25          0.583     0.6200     0.0200      -0.0383  NEGATIVE   n/a
  cost x0.5         0.333     0.6200     0.0100      -0.1833  NEGATIVE   n/a
  cost x2           0.333     0.6200     0.0400      -0.2133  NEGATIVE   n/a
  Read the SIGN column, not the decimals: if `p - 5pp` is NEGATIVE, the card rests on a win rate you cannot miss by five points.
```

## What the card says - and what it does not

A high win rate is evidence about *how often* the exit fires, and nothing else. It is not evidence
of a profitable strategy, and it never has been. The card is negative at 62%, negative at 67%, and
becomes positive only around `p = 0.75` - where the whole result rests on the top quartile of the
assumed distribution. The correct response is to rotate the payoff corner (widen the target,
tighten the stop, or stop capping the winner), not to improve the hit rate by another point.
