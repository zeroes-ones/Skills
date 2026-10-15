# Check 1 - the trend/breakout corner, 1R stop and 3R target: POSITIVE

**Status:** [ILLUSTRATIVE]. `p = 0.40` is an *assumed* win rate, not a measured one. The card is a
hypothesis about a payoff corner, and the arithmetic below is what that hypothesis implies. It is
not a result and it is not a prediction.

**Command** (run from the repository root):

```
py -3 skills/14-finance/equity-trading-playbook/scripts/payoff_check.py --tp 3.0 --sl 1.0 --p 0.40
```

## Why this card exists

This is the corner a breakout or trend-following entry is trying to buy: a 1R stop and a 3R target,
held with a win rate below half. `tp/sl = 3.0` puts the break-even win rate at
`p* = 1/(1+3) = 0.25`, so the card does not need a good hit rate - it needs the losers to be small
and the winners to be three times as large, which is what the 1R stop and the 3R target are for.

## Hand arithmetic, computed independently of the tool

| Quantity | Formula | Working | Result |
|---|---|---|---|
| payoff ratio `b` | `tp/sl` | `3.0/1.0` | **3.000000** |
| expectancy `E` | `p*b - (1-p)` | `0.40*3.0 - 0.60 = 1.20 - 0.60` | **+0.600000R** |
| break-even payoff `b*` | `(1-p)/p` | `0.60/0.40` | **1.500000** |
| break-even win rate `p*` | `1/(1+b)` | `1/4` | **0.250000** |
| Kelly `f*` | `E/b` | `0.60/3.0` | **0.200000** |
| two-point `sd` | `sqrt(p(b-E)^2 + (1-p)(-1-E)^2)` | `sqrt(0.40*2.40^2 + 0.60*1.60^2) = sqrt(2.304 + 1.536) = sqrt(3.84)` | **1.959592** |
| `n_req` | `4*(sd/abs(E))^2` | `4*(1.959592/0.60)^2 = 4*3.265986^2 = 4*10.666667` | **42.667** |
| `L` at n = 250 | `ln(n)/ln(1/(1-p))` | `ln(250)/ln(1.666667) = 5.521461/0.510826` | **10.809** |
| `R_max` | `D_tol/(L*1.5)` | `20/(10.809*1.5) = 20/16.213` | **1.2336%** |
| `c_R*` break-even cost | `E` | `0.600000` | **0.600000R** |

`n_req` is a *floor*, not a target: the `sd` here is the **two-point** sd over the set
`{+b, -1}`, so it is smaller than the sd of real R-multiples whose exits land between the two
points. The sample you actually need is larger than 42.667 trades.

## Verbatim tool output

```
==============================================================================
PAYOFF CARD: tp = 3.00R   sl = 1.00R   p = 0.4000   cost = 0.0000R   n = 250   safety = 1.50
==============================================================================

PAYOFF ARITHMETIC (every line prints its own formula)
  payoff ratio b        : 3.000000
      b = tp/sl = 3.00/1.00 = 3.000000
  expectancy E          : +0.600000R
      E = p*b - (1-p) = 0.400000*3.000000 - 0.600000 = +0.600000R
  cost drag c_R         : 0.000000R
      c_R = --cost-r = 0.0000
  net expectancy E_net  : +0.600000R
      E_net = E - c_R = +0.600000 - 0.000000 = +0.600000R
  break-even payoff b*  : 1.500000
      b* = (1-p)/p = 0.600000/0.400000 = 1.500000
  break-even win rate p*: 0.250000
      p* = 1/(1+b) = 1/(1+3.000000) = 0.250000
  edge (p - p*)         : +0.150000
      edge = p - p* = 0.400000 - 0.250000 = +0.150000 (win-rate points)
  Kelly f* / half       : +0.200000 / +0.100000
      f* = E/b = +0.600000/3.000000 = +0.200000   (half-Kelly +0.100000)

DISTRIBUTION AND SURVIVAL (in R units)
  two-point sd          : 1.959592
      sd^2 = p*(b-E)^2 + (1-p)*(-1-E)^2 = 0.400000*(3.000000-(+0.600000))^2 + 0.600000*(-1.000000-(+0.600000))^2 = 0.400000*5.760000 + 0.600000*2.560000 = 3.840000
  trades to a 2-sigma mean : 42.667
      n_req = 4*(sd/|E_net|)^2 = 4*(1.959592/0.600000)^2 = 42.667 trades
  years at pace         : 0.171
      42.667 trades / 250.0 per year = 0.171 years
  expected worst streak L  : 10.809
      L ~ ln(n)/ln(1/(1-p)) = ln(250.0)/ln(1.666667) = 5.521461/0.510826 = 10.809 consecutive losses
  R_max (risk/trade)    : 1.2336%
      R_max = D_tol/(L*safety) = 20.0000%/(10.809*1.50) = 1.2336% of equity per trade
  break-even cost c_R*  : 0.600000
      c_R* = E = 0.600000R. At or above this round-trip cost in R the corner crosses zero regardless of p and b.
      supply --cost-bps and --stop-pct to see the tightest break-even stop distance.

  sd guard: sd is a TWO-POINT distribution sd -- it knows only {win at +b, loss at -1}. It is not the sample sd of your realised R-multiples, which is larger because real exits land between the two points. n_req derived from it is a FLOOR on the sample you need, never a target.
  COST SHIFTS THE MEAN, NOT THE SPREAD. Net outcomes are (b - c_R) and (-1 - c_R), so sd^2 = p*(b-c_R-E_net)^2 + (1-p)*(-1-c_R-E_net)^2 reduces algebraically to the same p*(b-E)^2 + (1-p)*(-1-E)^2. A cost increase moves E down and leaves sd, and therefore n_req's numerator, where it was.

VERDICT: POSITIVE
  POSITIVE. E_net = +0.600000R per trade on the assumed card. This is a statement about the ASSUMED p and b, not about the market: run --from-log to see what your own record says, and read the sensitivity block before believing p to the point.

SENSITIVITY (one lever at a time; everything else held fixed)
  lever                 b          p        c_R     E_net(R)  verdict    n_req
  p - 5pp           3.000     0.3500     0.0000      +0.4000  POSITIVE   91.000
  p + 5pp           3.000     0.4500     0.0000      +0.8000  POSITIVE   24.750
  b - 0.25          2.750     0.4000     0.0000      +0.5000  POSITIVE   54.000
  b + 0.25          3.250     0.4000     0.0000      +0.7000  POSITIVE   35.388
  cost x0.5         3.000     0.4000     0.0000      +0.6000  POSITIVE   42.667
  cost x2           3.000     0.4000     0.0000      +0.6000  POSITIVE   42.667
  Read the SIGN column, not the decimals: if `p - 5pp` is NEGATIVE, the card rests on a win rate you cannot miss by five points.
```

## What the card says - and what it does not

The corner pays `+0.60R` per trade gross and `+0.59R` net on the same assumed card, which is the
arithmetic reason trend following is one of the few equity corners that can survive a sub-50% hit
rate. It says **nothing** about whether a 40% hit rate is achievable on any instrument, in any
regime, or by any particular person; the sensitivity block at the bottom of the real output is the
honest test of that. Note the consequence in the last lines above: this is the *safest* corner in
the map and it still demands the **smallest** size, because an 11-trade losing streak at a 40% hit
rate forces `R_max` down to 1.2336% of equity.
