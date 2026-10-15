# Check 2 - the 1:1 corner at a 45% win rate: NEGATIVE

**Status:** [ILLUSTRATIVE]. An assumed win rate on an assumed payoff corner.

**Command:**

```
py -3 skills/14-finance/equity-trading-playbook/scripts/payoff_check.py --tp 1.0 --sl 1.0 --p 0.45
```

## Why this card exists

Equal stop and equal target is where most retail equity trading happens, because a 1:1 card is the
easiest one to describe and the easiest one to automate. The arithmetic is unkind to it: `b = 1`
puts `p* = 1/(1+1) = 0.50`, so a 1:1 card is a coin-flip card, and a 45% hit rate on a coin flip
loses exactly what the coin flip implies.

## Hand arithmetic, computed independently of the tool

| Quantity | Formula | Working | Result |
|---|---|---|---|
| `b` | `tp/sl` | `1.0/1.0` | **1.000000** |
| `E` | `p*b - (1-p)` | `0.45*1.0 - 0.55` | **-0.100000R** |
| `b*` | `(1-p)/p` | `0.55/0.45` | **1.222222** |
| `p*` | `1/(1+b)` | `1/2` | **0.500000** |
| `f*` | `E/b` | `-0.10/1.0` | **-0.100000** (negative: no fraction of a bankroll is right) |
| `sd` | `sqrt(p(b-E)^2 + (1-p)(-1-E)^2)` | `sqrt(0.45*1.10^2 + 0.55*0.90^2) = sqrt(0.5445 + 0.4455) = sqrt(0.99)` | **0.994987** |
| `n_req` | `4*(sd/abs(E))^2` | `E < 0`, so no sample size reaches +2 sigma | **n/a** |
| `L` at n = 250 | `ln(n)/ln(1/(1-p))` | `ln(250)/ln(1.818182) = 5.521461/0.597837` | **9.236** |
| `R_max` | `D_tol/(L*1.5)` | `20/(9.236*1.5)` | **1.4437%** |

`n_req` is reported as `n/a`, and that is the correct answer rather than a defect: with a negative
mean, more trades move the arithmetic *further* from break-even. A tool that printed a number here
would be inviting the reader to wait for one.

## Verbatim tool output

```
==============================================================================
PAYOFF CARD: tp = 1.00R   sl = 1.00R   p = 0.4500   cost = 0.0000R   n = 250   safety = 1.50
==============================================================================

PAYOFF ARITHMETIC (every line prints its own formula)
  payoff ratio b        : 1.000000
      b = tp/sl = 1.00/1.00 = 1.000000
  expectancy E          : -0.100000R
      E = p*b - (1-p) = 0.450000*1.000000 - 0.550000 = -0.100000R
  cost drag c_R         : 0.000000R
      c_R = --cost-r = 0.0000
  net expectancy E_net  : -0.100000R
      E_net = E - c_R = -0.100000 - 0.000000 = -0.100000R
  break-even payoff b*  : 1.222222
      b* = (1-p)/p = 0.550000/0.450000 = 1.222222
  break-even win rate p*: 0.500000
      p* = 1/(1+b) = 1/(1+1.000000) = 0.500000
  edge (p - p*)         : -0.050000
      edge = p - p* = 0.450000 - 0.500000 = -0.050000 (win-rate points)
  Kelly f* / half       : -0.100000 / -0.050000
      f* = E/b = -0.100000/1.000000 = -0.100000   (half-Kelly -0.050000)  -- NEGATIVE: no fraction of the bankroll is the right fraction of a negative edge.

DISTRIBUTION AND SURVIVAL (in R units)
  two-point sd          : 0.994987
      sd^2 = p*(b-E)^2 + (1-p)*(-1-E)^2 = 0.450000*(1.000000-(-0.100000))^2 + 0.550000*(-1.000000-(-0.100000))^2 = 0.450000*1.210000 + 0.550000*0.810000 = 0.990000
  trades to a 2-sigma mean : n/a
      n_req = n/a. E_net = -0.100000R is not positive, so no sample size moves the mean to +2 sigma; more trades carry you further from break-even, not closer.
  years at pace         : n/a
      pacing needs n_req.
  expected worst streak L  : 9.236
      L ~ ln(n)/ln(1/(1-p)) = ln(250.0)/ln(1.818182) = 5.521461/0.597837 = 9.236 consecutive losses
  R_max (risk/trade)    : 1.4437%
      R_max = D_tol/(L*safety) = 20.0000%/(9.236*1.50) = 1.4437% of equity per trade
  break-even cost c_R*  : n/a
      E <= 0, so there is no positive cost at which the corner breaks even. Cost only adds to the loss.

  sd guard: sd is a TWO-POINT distribution sd -- it knows only {win at +b, loss at -1}. It is not the sample sd of your realised R-multiples, which is larger because real exits land between the two points. n_req derived from it is a FLOOR on the sample you need, never a target.
  COST SHIFTS THE MEAN, NOT THE SPREAD. Net outcomes are (b - c_R) and (-1 - c_R), so sd^2 = p*(b-c_R-E_net)^2 + (1-p)*(-1-c_R-E_net)^2 reduces algebraically to the same p*(b-E)^2 + (1-p)*(-1-E)^2. A cost increase moves E down and leaves sd, and therefore n_req's numerator, where it was.

VERDICT: NEGATIVE
  NEGATIVE. the corner is already negative before cost (E = -0.100000R). Do NOT trade this card at this p. Either the payoff ratio or the win rate has to change; position size cannot rescue a negative expectancy, it only scales the loss.

SENSITIVITY (one lever at a time; everything else held fixed)
  lever                 b          p        c_R     E_net(R)  verdict    n_req
  p - 5pp           1.000     0.4000     0.0000      -0.2000  NEGATIVE   n/a
  p + 5pp           1.000     0.5000     0.0000      +0.0000  NEGATIVE   n/a
  b - 0.25          0.750     0.4500     0.0000      -0.2125  NEGATIVE   n/a
  b + 0.25          1.250     0.4500     0.0000      +0.0125  MARGINAL   32,076.000
  cost x0.5         1.000     0.4500     0.0000      -0.1000  NEGATIVE   n/a
  cost x2           1.000     0.4500     0.0000      -0.1000  NEGATIVE   n/a
  Read the SIGN column, not the decimals: if `p - 5pp` is NEGATIVE, the card rests on a win rate you cannot miss by five points.
```

## What the card says - and what it does not

Nothing in this card can be fixed by discipline, and nothing can be fixed by size: position size
scales a negative expectancy, it does not change its sign. There are exactly two levers - raise `b`
above `b* = 1.222222`, or raise `p` above `p* = 0.50`. The card does not say which of those is
achievable; that is a signal question and belongs to `technical-signals-engineer`, not to this
arithmetic.
