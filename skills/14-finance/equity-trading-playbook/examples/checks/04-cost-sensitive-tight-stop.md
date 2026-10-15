# Check 4 - the same card at two stop distances: cost decides the verdict

**Status:** [ILLUSTRATIVE]. An assumed win rate on an assumed payoff corner. The *cost rate* is a
stated assumption too, and it is the variable under test.

**Commands:**

```
py -3 skills/14-finance/equity-trading-playbook/scripts/payoff_check.py --tp 2.0 --sl 1.0 --p 0.45 --cost-bps 5 --stop-pct 0.10
py -3 skills/14-finance/equity-trading-playbook/scripts/payoff_check.py --tp 2.0 --sl 1.0 --p 0.45 --cost-bps 5 --stop-pct 5.0
```

Only `--stop-pct` changes between the two runs. Same assumed round-trip cost of 5 basis points, same
payoff corner, same win rate.

## Why this pair exists

The cost term in R units is

```
c_R = round_trip_cost / R_dollars
    = (notional * bps/10000) / (notional * stop_pct/100)
    = bps / (100 * stop_pct)
```

The notional **cancels**. Cost drag in R depends on the cost *rate* and on the *stop distance as a
fraction of price*, and on nothing else - not on account size, not on share count. Worked for this
pair at 5 bps: a 0.10% stop gives `c_R = 5/(100 * 0.10) = 0.500000R`; a 5.0% stop gives
`c_R = 5/(100 * 5.0) = 0.010000R`. That is a **50x** difference in the cost term from one flag.

## Hand arithmetic, computed independently of the tool

Shared by both runs: `b = 2.0`, `E = 0.45*2.0 - 0.55 = +0.350000R`, `b* = 0.55/0.45 = 1.222222`,
`p* = 1/(1+2) = 0.333333`, `sd = sqrt(0.45*1.65^2 + 0.55*1.35^2) = sqrt(1.225125 + 1.002375) =
sqrt(2.2275) = 1.492481`, `L = ln(250)/ln(1.818182) = 9.236`, `R_max = 20/(9.236*1.5) = 1.4436%`.

| Variable | Tight stop | Wide stop |
|---|---|---|
| stop distance | 0.10% of price | 5.0% of price |
| `c_R = bps/(100*stop_pct)` | `5/10 =` **0.500000R** | `5/500 =` **0.010000R** |
| `E_net = E - c_R` | `0.35 - 0.50 =` **-0.150000R** | `0.35 - 0.01 =` **+0.340000R** |
| verdict | **NEGATIVE** | **POSITIVE** |
| `n_req` | n/a (E_net < 0) | `4*(1.492481/0.34)^2 =` **77.076** |
| break-even stop `S* = bps/(100*E)` | 0.142857% of price | 0.142857% of price |

The break-even stop **is the same in both runs** - it depends only on the cost rate and the corner,
not on the stop you chose. A stop tighter than 0.1429% of price makes this card a net loser at 5 bps;
a stop wider than that keeps it positive. That is the whole strategic conclusion of the cost
derivation.

## Verbatim tool output - tight stop (0.10%)

```
==============================================================================
PAYOFF CARD: tp = 2.00R   sl = 1.00R   p = 0.4500   cost = 0.5000R   n = 250   safety = 1.50
==============================================================================

PAYOFF ARITHMETIC (every line prints its own formula)
  payoff ratio b        : 2.000000
      b = tp/sl = 2.00/1.00 = 2.000000
  expectancy E          : +0.350000R
      E = p*b - (1-p) = 0.450000*2.000000 - 0.550000 = +0.350000R
  cost drag c_R         : 0.500000R
      derived from 5.0000 bps round trip at a 0.1000% stop: c_R = bps/(100*stop_pct) = 5.0000/(100*0.1000) = 0.500000
  net expectancy E_net  : -0.150000R
      E_net = E - c_R = +0.350000 - 0.500000 = -0.150000R
  break-even payoff b*  : 1.222222
      b* = (1-p)/p = 0.550000/0.450000 = 1.222222
  break-even win rate p*: 0.333333
      p* = 1/(1+b) = 1/(1+2.000000) = 0.333333
  edge (p - p*)         : +0.116667
      edge = p - p* = 0.450000 - 0.333333 = +0.116667 (win-rate points)
  Kelly f* / half       : +0.175000 / +0.087500
      f* = E/b = +0.350000/2.000000 = +0.175000   (half-Kelly +0.087500)

DISTRIBUTION AND SURVIVAL (in R units)
  two-point sd          : 1.492481
      sd^2 = p*(b-E)^2 + (1-p)*(-1-E)^2 = 0.450000*(2.000000-(+0.350000))^2 + 0.550000*(-1.000000-(+0.350000))^2 = 0.450000*2.722500 + 0.550000*1.822500 = 2.227500
  trades to a 2-sigma mean : n/a
      n_req = n/a. E_net = -0.150000R is not positive, so no sample size moves the mean to +2 sigma; more trades carry you further from break-even, not closer.
  years at pace         : n/a
      pacing needs n_req.
  expected worst streak L  : 9.236
      L ~ ln(n)/ln(1/(1-p)) = ln(250.0)/ln(1.818182) = 5.521461/0.597837 = 9.236 consecutive losses
  R_max (risk/trade)    : 1.4437%
      R_max = D_tol/(L*safety) = 20.0000%/(9.236*1.50) = 1.4437% of equity per trade
  break-even cost c_R*  : 0.350000
      c_R* = E = 0.350000R. At or above this round-trip cost in R the corner crosses zero regardless of p and b.
      tightest break-even stop at 5.0000 bps round trip: S* = bps/(100*E) = 5.0000/(100*0.350000) = 0.1429% of price. Below this stop distance the corner is a net loser, however good p and b look.

  sd guard: sd is a TWO-POINT distribution sd -- it knows only {win at +b, loss at -1}. It is not the sample sd of your realised R-multiples, which is larger because real exits land between the two points. n_req derived from it is a FLOOR on the sample you need, never a target.
  COST SHIFTS THE MEAN, NOT THE SPREAD. Net outcomes are (b - c_R) and (-1 - c_R), so sd^2 = p*(b-c_R-E_net)^2 + (1-p)*(-1-c_R-E_net)^2 reduces algebraically to the same p*(b-E)^2 + (1-p)*(-1-E)^2. A cost increase moves E down and leaves sd, and therefore n_req's numerator, where it was.

VERDICT: NEGATIVE
  NEGATIVE. cost alone consumes the edge: c_R = 0.500000R against E = +0.350000R, so c_R* = 0.350000R. Do NOT trade this card at this p. Either the payoff ratio or the win rate has to change; position size cannot rescue a negative expectancy, it only scales the loss.

SENSITIVITY (one lever at a time; everything else held fixed)
  lever                 b          p        c_R     E_net(R)  verdict    n_req
  p - 5pp           2.000     0.4000     0.5000      -0.3000  NEGATIVE   n/a
  p + 5pp           2.000     0.5000     0.5000      +0.0000  NEGATIVE   n/a
  b - 0.25          1.750     0.4500     0.5000      -0.2625  NEGATIVE   n/a
  b + 0.25          2.250     0.4500     0.5000      -0.0375  NEGATIVE   n/a
  cost x0.5         2.000     0.4500     0.2500      +0.1000  MARGINAL   891.000
  cost x2           2.000     0.4500     1.0000      -0.6500  NEGATIVE   n/a
  Read the SIGN column, not the decimals: if `p - 5pp` is NEGATIVE, the card rests on a win rate you cannot miss by five points.
```

## Verbatim tool output - wide stop (5.0%)

```
==============================================================================
PAYOFF CARD: tp = 2.00R   sl = 1.00R   p = 0.4500   cost = 0.0100R   n = 250   safety = 1.50
==============================================================================

PAYOFF ARITHMETIC (every line prints its own formula)
  payoff ratio b        : 2.000000
      b = tp/sl = 2.00/1.00 = 2.000000
  expectancy E          : +0.350000R
      E = p*b - (1-p) = 0.450000*2.000000 - 0.550000 = +0.350000R
  cost drag c_R         : 0.010000R
      derived from 5.0000 bps round trip at a 5.0000% stop: c_R = bps/(100*stop_pct) = 5.0000/(100*5.0000) = 0.010000
  net expectancy E_net  : +0.340000R
      E_net = E - c_R = +0.350000 - 0.010000 = +0.340000R
  break-even payoff b*  : 1.222222
      b* = (1-p)/p = 0.550000/0.450000 = 1.222222
  break-even win rate p*: 0.333333
      p* = 1/(1+b) = 1/(1+2.000000) = 0.333333
  edge (p - p*)         : +0.116667
      edge = p - p* = 0.450000 - 0.333333 = +0.116667 (win-rate points)
  Kelly f* / half       : +0.175000 / +0.087500
      f* = E/b = +0.350000/2.000000 = +0.175000   (half-Kelly +0.087500)

DISTRIBUTION AND SURVIVAL (in R units)
  two-point sd          : 1.492481
      sd^2 = p*(b-E)^2 + (1-p)*(-1-E)^2 = 0.450000*(2.000000-(+0.350000))^2 + 0.550000*(-1.000000-(+0.350000))^2 = 0.450000*2.722500 + 0.550000*1.822500 = 2.227500
  trades to a 2-sigma mean : 77.076
      n_req = 4*(sd/|E_net|)^2 = 4*(1.492481/0.340000)^2 = 77.076 trades
  years at pace         : 0.308
      77.076 trades / 250.0 per year = 0.308 years
  expected worst streak L  : 9.236
      L ~ ln(n)/ln(1/(1-p)) = ln(250.0)/ln(1.818182) = 5.521461/0.597837 = 9.236 consecutive losses
  R_max (risk/trade)    : 1.4437%
      R_max = D_tol/(L*safety) = 20.0000%/(9.236*1.50) = 1.4437% of equity per trade
  break-even cost c_R*  : 0.350000
      c_R* = E = 0.350000R. At or above this round-trip cost in R the corner crosses zero regardless of p and b.
      tightest break-even stop at 5.0000 bps round trip: S* = bps/(100*E) = 5.0000/(100*0.350000) = 0.1429% of price. Below this stop distance the corner is a net loser, however good p and b look.

  sd guard: sd is a TWO-POINT distribution sd -- it knows only {win at +b, loss at -1}. It is not the sample sd of your realised R-multiples, which is larger because real exits land between the two points. n_req derived from it is a FLOOR on the sample you need, never a target.
  COST SHIFTS THE MEAN, NOT THE SPREAD. Net outcomes are (b - c_R) and (-1 - c_R), so sd^2 = p*(b-c_R-E_net)^2 + (1-p)*(-1-c_R-E_net)^2 reduces algebraically to the same p*(b-E)^2 + (1-p)*(-1-E)^2. A cost increase moves E down and leaves sd, and therefore n_req's numerator, where it was.

VERDICT: POSITIVE
  POSITIVE. E_net = +0.340000R per trade on the assumed card. This is a statement about the ASSUMED p and b, not about the market: run --from-log to see what your own record says, and read the sensitivity block before believing p to the point.

SENSITIVITY (one lever at a time; everything else held fixed)
  lever                 b          p        c_R     E_net(R)  verdict    n_req
  p - 5pp           2.000     0.4000     0.0100      +0.1900  MARGINAL   239.335
  p + 5pp           2.000     0.5000     0.0100      +0.4900  POSITIVE   37.484
  b - 0.25          1.750     0.4500     0.0100      +0.2275  POSITIVE   144.656
  b + 0.25          2.250     0.4500     0.0100      +0.4525  POSITIVE   51.070
  cost x0.5         2.000     0.4500     0.0050      +0.3450  POSITIVE   74.858
  cost x2           2.000     0.4500     0.0200      +0.3300  POSITIVE   81.818
  Read the SIGN column, not the decimals: if `p - 5pp` is NEGATIVE, the card rests on a win rate you cannot miss by five points.
```

## What these two runs say - and what they do not

Cost is **not** a rounding detail in equity, but equity is cost-forgiving compared with the
alternatives: a 5 bps round trip is small, and at a swing-trade stop distance of several percent it
consumes a tenth of the edge. It is only when the stop is forced tight - intraday, scalping, a tight
trailing stop, an ATR stop on a low-volatility name - that `c_R` becomes the largest single term on
the card. Neither run says which stop the market will let you use; that is a volatility and
liquidity question and belongs to `equity-risk-and-capital-engineer` and
`technical-signals-engineer`.
