# Check 5 - mean reversion, 0.75R target on a 1R stop: MARGINAL

**Status:** [ILLUSTRATIVE]. An assumed win rate on an assumed payoff corner.

**Command:**

```
py -3 skills/14-finance/equity-trading-playbook/scripts/payoff_check.py --tp 0.75 --sl 1.0 --p 0.65
```

## Why this card exists

A dip-buying or range-fade entry usually exits *before* the original stop distance, because the point
of the trade is that the move is short and the mean is close. A 0.75R target on a 1R stop is that
shape: `b = 0.75`, so `p* = 1/(1+0.75) = 0.571429`. At a 65% hit rate the card is genuinely
positive - and genuinely thin: `+0.1375R` gross, `+0.1275R` net at a 1% cost drag.

## Hand arithmetic, computed independently of the tool

| Quantity | Formula | Working | Result |
|---|---|---|---|
| `b` | `tp/sl` | `0.75/1.0` | **0.750000** |
| `E` | `p*b - (1-p)` | `0.65*0.75 - 0.35 = 0.4875 - 0.35` | **+0.137500R** |
| `b*` | `(1-p)/p` | `0.35/0.65` | **0.538462** |
| `p*` | `1/(1+b)` | `1/1.75` | **0.571429** |
| `f*` | `E/b` | `0.1375/0.75` | **0.183333** |
| `sd` | `sqrt(p(b-E)^2 + (1-p)(-1-E)^2)` | `sqrt(0.65*0.6125^2 + 0.35*1.1375^2) = sqrt(0.243852 + 0.452867) = sqrt(0.696719)` | **0.834697** |
| `n_req` | `4*(sd/abs(E))^2` | `4*(0.834697/0.1375)^2 = 4*6.070522^2 = 4*36.851240` | **147.405** |
| `L` at n = 250 | `ln(n)/ln(1/(1-p))` | `ln(250)/ln(2.857143) = 5.521461/1.049822` | **5.259** |
| `R_max` | `D_tol/(L*1.5)` | `20/(5.259*1.5)` | **2.5351%** |
| `c_R*` | `E` | `0.137500` | **0.137500R** |

147.405 trades to a 2 sigma mean, at 250 trades a year: **0.59 years** of measurement before this
edge is separable from zero at all. That is what "thin edge" means numerically, and it is why the
verdict band calls it MARGINAL rather than POSITIVE.

## Verbatim tool output

```
==============================================================================
PAYOFF CARD: tp = 0.75R   sl = 1.00R   p = 0.6500   cost = 0.0000R   n = 250   safety = 1.50
==============================================================================

PAYOFF ARITHMETIC (every line prints its own formula)
  payoff ratio b        : 0.750000
      b = tp/sl = 0.75/1.00 = 0.750000
  expectancy E          : +0.137500R
      E = p*b - (1-p) = 0.650000*0.750000 - 0.350000 = +0.137500R
  cost drag c_R         : 0.000000R
      c_R = --cost-r = 0.0000
  net expectancy E_net  : +0.137500R
      E_net = E - c_R = +0.137500 - 0.000000 = +0.137500R
  break-even payoff b*  : 0.538462
      b* = (1-p)/p = 0.350000/0.650000 = 0.538462
  break-even win rate p*: 0.571429
      p* = 1/(1+b) = 1/(1+0.750000) = 0.571429
  edge (p - p*)         : +0.078571
      edge = p - p* = 0.650000 - 0.571429 = +0.078571 (win-rate points)
  Kelly f* / half       : +0.183333 / +0.091667
      f* = E/b = +0.137500/0.750000 = +0.183333   (half-Kelly +0.091667)

DISTRIBUTION AND SURVIVAL (in R units)
  two-point sd          : 0.834697
      sd^2 = p*(b-E)^2 + (1-p)*(-1-E)^2 = 0.650000*(0.750000-(+0.137500))^2 + 0.350000*(-1.000000-(+0.137500))^2 = 0.650000*0.375156 + 0.350000*1.293906 = 0.696719
  trades to a 2-sigma mean : 147.405
      n_req = 4*(sd/|E_net|)^2 = 4*(0.834697/0.137500)^2 = 147.405 trades
  years at pace         : 0.590
      147.405 trades / 250.0 per year = 0.590 years
  expected worst streak L  : 5.259
      L ~ ln(n)/ln(1/(1-p)) = ln(250.0)/ln(2.857143) = 5.521461/1.049822 = 5.259 consecutive losses
  R_max (risk/trade)    : 2.5351%
      R_max = D_tol/(L*safety) = 20.0000%/(5.259*1.50) = 2.5351% of equity per trade
  break-even cost c_R*  : 0.137500
      c_R* = E = 0.137500R. At or above this round-trip cost in R the corner crosses zero regardless of p and b.
      supply --cost-bps and --stop-pct to see the tightest break-even stop distance.

  sd guard: sd is a TWO-POINT distribution sd -- it knows only {win at +b, loss at -1}. It is not the sample sd of your realised R-multiples, which is larger because real exits land between the two points. n_req derived from it is a FLOOR on the sample you need, never a target.
  COST SHIFTS THE MEAN, NOT THE SPREAD. Net outcomes are (b - c_R) and (-1 - c_R), so sd^2 = p*(b-c_R-E_net)^2 + (1-p)*(-1-c_R-E_net)^2 reduces algebraically to the same p*(b-E)^2 + (1-p)*(-1-E)^2. A cost increase moves E down and leaves sd, and therefore n_req's numerator, where it was.

VERDICT: MARGINAL
  MARGINAL. E_net = +0.137500R is positive but below the 0.20R band. n_req = 147.405 trades, so a p estimated from a small sample cannot separate this from zero. Trade it small, or widen b, or do not trade it.

SENSITIVITY (one lever at a time; everything else held fixed)
  lever                 b          p        c_R     E_net(R)  verdict    n_req
  p - 5pp           0.750     0.6000     0.0000      +0.0500  MARGINAL   1,176.000
  p + 5pp           0.750     0.7000     0.0000      +0.2250  POSITIVE   50.815
  b - 0.25          0.500     0.6500     0.0000      -0.0250  NEGATIVE   n/a
  b + 0.25          1.000     0.6500     0.0000      +0.3000  POSITIVE   40.444
  cost x0.5         0.750     0.6500     0.0000      +0.1375  MARGINAL   147.405
  cost x2           0.750     0.6500     0.0000      +0.1375  MARGINAL   147.405
  Read the SIGN column, not the decimals: if `p - 5pp` is NEGATIVE, the card rests on a win rate you cannot miss by five points.
```

## What the card says - and what it does not

The card is positive, and it is positive by less than the `0.20R` MARGINAL band and by less than
2 percentage points of win rate above its own break-even. Every part of the result is fragile: 147
trades of measurement, a 0.1375R break-even cost, and a 0.078571 win-rate-point edge over `p*`.
A reader who trades this corner must be willing to record 147 trades before concluding anything -
and the sensitivity block in the real output shows `p - 5pp` at `+0.100000R`, still positive, which
is the one encouraging line on the card.
