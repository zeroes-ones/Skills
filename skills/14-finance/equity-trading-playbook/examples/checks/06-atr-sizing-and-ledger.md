# Check 6 - from an R-unit card to a share count, and from a card to a ledger

**Status:** [ILLUSTRATIVE] for the card. The ledger run reads
`examples/logs/equity-book-synthetic.csv`, which is **SYNTHETIC** throughout - invented trades,
invented symbols (all prefixed `X`), invented currency, no market information of any kind.

**Commands:**

```
py -3 skills/14-finance/equity-trading-playbook/scripts/payoff_check.py --tp 3.0 --sl 1.0 --p 0.40 --atr 2.0 --atr-value 5.00 --price 50.00 --capital 100000 --cost-bps 5
py -3 skills/14-finance/equity-trading-playbook/scripts/payoff_check.py --from-log skills/14-finance/equity-trading-playbook/examples/logs/equity-book-synthetic.csv
```

## Why these two runs exist

The first turns the abstract `R_max` into the only form a person can act on: a share count and a
dollar risk figure. The second turns the same arithmetic on a record instead of an assumption - and
reports the R-unit statistic beside the currency-unit statistic so that the contamination of `b` by
position size is visible rather than argued about.

## Hand arithmetic for the ATR sizing, computed independently of the tool

`R_max = 1.2336%` of `$100,000 = $1,233.55`. The ATR stop is `2.0 * $5.00 = $10.00` per share, which
is `$10.00/$50.00 = 20.0%` of price. The share count is `floor($1,233.55/$10.00) = 123` shares, a
`$6,150` notional at a 5 bps round trip of `$6,150 * 5/10000 = $3.08`. Cross-check the cost with the
derived formula: `c_R = bps/(100 * stop_pct) = 5/(100 * 20) = 0.002500R`, and
`0.0025 * $1,233.55 = $3.08`. The two routes agree.

## Hand arithmetic for the ledger, computed independently of the tool

| Cohort | n | p | `b_R` | `E` (mean R) | `c_R` | `E_net` |
|---|---|---|---|---|---|---|
| `trend-breakout` | 15 | `6/15 = 0.400000` | `3.0/1.0 = 3.000000` | `(6*3 - 9*1)/15 =` **+0.600000R** | `75/7500 = 0.010000` | **+0.590000R** |
| `range-meanrev` | 20 | `13/20 = 0.650000` | `0.75/1.0 = 0.750000` | `(9.75 - 7)/20 =` **+0.137500R** | `80/8000 = 0.010000` | **+0.127500R** |
| `disposition-quick-tp` | 24 | `15/24 = 0.625000` | `0.5/1.5 = 0.333333` | `(7.5 - 13.5)/24 =` **-0.250000R** | `72/7200 = 0.010000` | **-0.260000R** |
| `sizing-slip` | 3 | `1/3 = 0.333333` | `1.0/1.0 = 1.000000` | `(-1 -1 +1)/3 =` **-0.333333R** | `24/2400 = 0.010000` | **-0.343333R** |
| pooled book | 62 | `35/62 = 0.564516` | `1.035714/1.166667 = 0.887755` | `4.75/62 =` **+0.076613R** | `251/25100 = 0.010000` | **+0.066613R** |

The `sizing-slip` cohort is the contamination demonstration. Three trades, risks `200 / 200 / 2000`:
`-1.0R`, `-1.0R`, `+1.0R`. In R the payoff ratio is `1.0/1.0 = 1.000000`. In **currency** the
oversized winner returns `$2,000` against an average loss of `$200`, so the currency payoff ratio is
`2000/200 = 10.000000` and the currency ratio-view expectancy is `+2.666667` while the R ratio view
is `-0.333333`. Same three trades, opposite signs. The 10x is sizing, not edge.

## Verbatim tool output - ATR sizing

```
==============================================================================
PAYOFF CARD: tp = 3.00R   sl = 1.00R   p = 0.4000   cost = 0.0025R   n = 250   safety = 1.50
==============================================================================

PAYOFF ARITHMETIC (every line prints its own formula)
  payoff ratio b        : 3.000000
      b = tp/sl = 3.00/1.00 = 3.000000
  expectancy E          : +0.600000R
      E = p*b - (1-p) = 0.400000*3.000000 - 0.600000 = +0.600000R
  cost drag c_R         : 0.002500R
      derived from 5.0000 bps round trip at a 20.0000% stop: c_R = bps/(100*stop_pct) = 5.0000/(100*20.0000) = 0.002500
  net expectancy E_net  : +0.597500R
      E_net = E - c_R = +0.600000 - 0.002500 = +0.597500R
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
  trades to a 2-sigma mean : 43.024
      n_req = 4*(sd/|E_net|)^2 = 4*(1.959592/0.597500)^2 = 43.024 trades
  years at pace         : 0.172
      43.024 trades / 250.0 per year = 0.172 years
  expected worst streak L  : 10.809
      L ~ ln(n)/ln(1/(1-p)) = ln(250.0)/ln(1.666667) = 5.521461/0.510826 = 10.809 consecutive losses
  R_max (risk/trade)    : 1.2336%
      R_max = D_tol/(L*safety) = 20.0000%/(10.809*1.50) = 1.2336% of equity per trade
  break-even cost c_R*  : 0.600000
      c_R* = E = 0.600000R. At or above this round-trip cost in R the corner crosses zero regardless of p and b.
      tightest break-even stop at 5.0000 bps round trip: S* = bps/(100*E) = 5.0000/(100*0.600000) = 0.0833% of price. Below this stop distance the corner is a net loser, however good p and b look.

  sd guard: sd is a TWO-POINT distribution sd -- it knows only {win at +b, loss at -1}. It is not the sample sd of your realised R-multiples, which is larger because real exits land between the two points. n_req derived from it is a FLOOR on the sample you need, never a target.
  COST SHIFTS THE MEAN, NOT THE SPREAD. Net outcomes are (b - c_R) and (-1 - c_R), so sd^2 = p*(b-c_R-E_net)^2 + (1-p)*(-1-c_R-E_net)^2 reduces algebraically to the same p*(b-E)^2 + (1-p)*(-1-E)^2. A cost increase moves E down and leaves sd, and therefore n_req's numerator, where it was.

VERDICT: POSITIVE
  POSITIVE. E_net = +0.597500R per trade on the assumed card. This is a statement about the ASSUMED p and b, not about the market: run --from-log to see what your own record says, and read the sensitivity block before believing p to the point.

POSITION SIZING (--atr mode)
  stop distance per share = atr_mult * atr = 2.00 * $5.00 = $10.00
  stop distance           = $10.00/$50.00 = 20.0000% of price
  R_max                   = 1.2336% of equity
  risk dollars per R      = 1.2336% * $100,000.00 = $1,233.55
  share count             = floor($1,233.55/$10.00) = 123 shares
  position notional       = 123 * $50.00 = $6,150.00
  round-trip cost @ 5.0000 bps = $6,150.00 * 5.0000/10000 = $3.08
  This is a CEILING derived from streak survival, not a recommendation. The sizing BAND belongs to trade-sizing-recovery, portfolio-signal-manager and algorithmic-trader.

SENSITIVITY (one lever at a time; everything else held fixed)
  lever                 b          p        c_R     E_net(R)  verdict    n_req
  p - 5pp           3.000     0.3500     0.0025      +0.3975  POSITIVE   92.148
  p + 5pp           3.000     0.4500     0.0025      +0.7975  POSITIVE   24.905
  b - 0.25          2.750     0.4000     0.0025      +0.4975  POSITIVE   54.544
  b + 0.25          3.250     0.4000     0.0025      +0.6975  POSITIVE   35.642
  cost x0.5         3.000     0.4000     0.0013      +0.5988  POSITIVE   42.845
  cost x2           3.000     0.4000     0.0050      +0.5950  POSITIVE   43.387
  Read the SIGN column, not the decimals: if `p - 5pp` is NEGATIVE, the card rests on a win rate you cannot miss by five points.
```

## Verbatim tool output - ledger cohorts

```
==============================================================================
LEDGER VIEW (--from-log): C:\Users\sande\Documents\Projects\Skills\skills\14-finance\equity-trading-playbook\examples\logs\equity-book-synthetic.csv
==============================================================================
# PROVENANCE: SYNTHETIC / ILLUSTRATIVE -- equity payoff-cohort fixture. NOT market data, NOT a
# PROVENANCE: backtest, NOT a result, NOT advice, and NOT the record of any person's account.
# PROVENANCE: 62 invented trades across four invented setups and six invented symbols (all prefixed
# PROVENANCE: X to make clear they are not tickers). Dates are invented: 2025-01-06 .. 2026-03-13.
# PROVENANCE: pnl is invented currency, GROSS of the `cost` column. risk is the planned per-trade
# PROVENANCE: risk in the same invented currency, so r = pnl/risk is the R-multiple of a trade.
# PROVENANCE: Built by hand from the cohort design below, so every row is checkable in your head and
# PROVENANCE: every figure this log produces can be derived without running anything.

  rows read : 62

POOLED BOOK
  n = 62   wins = 35   losses = 27   break-even = 0   p = 0.564516
  realised mean R-multiple  : +0.076613R   (the truth; sample mean of pnl/risk)
  cost drag c_R             : 0.010000
  net expectancy E_net      : +0.066613R
  b_R = 0.887755   b_$ = 1.125957   (contamination control)
  E_R_ratio = +0.065668   E$_ratio = +0.200137   (ratio views, same units)
  gross P&L = $5,400.00   cost = $251.00   net P&L = $5,149.00

COHORTS (one row per `setup` tag; sorted by name)
  setup                     n  wins        p       b_R       b_$   E$_ratio  E_R_ratio      c_R   E_net(R)
  disposition-quick-tp     24    15   0.6250    0.3333    0.3333    -0.1667    -0.1667  0.01000    -0.2600
  range-meanrev            20    13   0.6500    0.7500    0.7500    +0.1375    +0.1375  0.01000    +0.1275
  sizing-slip               3     1   0.3333    1.0000   10.0000    +2.6667    -0.3333  0.01000    -0.3433
  trend-breakout           15     6   0.4000    3.0000    3.0000    +0.6000    +0.6000  0.01000    +0.5900

  E_R_ratio and E$_ratio are the SAME statistic -- p*b - (1-p), in units of the average loss -- differing only in the unit b was measured in. E_net(R) is the realised mean R-multiple minus c_R, which is the truth; it equals E_R_ratio only when the average loss is exactly 1R.

  sizing-slip: currency b = 10.0000 against R b = 1.0000 -- a gap of 9.0000. The gap IS the sizing, not the strategy.
  sizing-slip: CONTAMINATED: currency ratio view +2.6667 against R ratio view -0.3333 -- opposite signs

  R UNITS OR NOTHING. A payoff ratio computed on currency P&L mixes sizing skill into entry skill: the numerator is the average of (R_multiple x risk) and so is the denominator, and the two do not cancel unless every trade risked the same amount. Convert to R before computing p and b. The --from-log table prints both views side by side so the gap is visible.
```

## What these runs say - and what they do not

The sizing run produces a *ceiling*, not a recommendation. `R_max` answers "the most I can risk per
trade and still survive the streak this card implies"; it does not say the position is worth taking,
and the sizing *band* it sits in belongs to `trade-sizing-recovery`, `portfolio-signal-manager` and
`algorithmic-trader`. The ledger run produces a description of 62 invented trades; the `+0.590000R`
on `trend-breakout` is arithmetic on a synthetic fixture, **not** a track record, and the pooled
`+0.066613R` is exactly the number that hides two cohorts of opposite sign. Neither run is a
backtest, a forecast, or evidence about any instrument.
