# Check 1 — a positive-expectancy corner: long premium, 1R stop, 2.5R target

**What this check is for.** The `long premium` corner of the payoff map, priced
end to end. A directional debit structure with a mechanical 1R stop and a 2.5R
target does not need a high win rate, because the payoff ratio carries the
arithmetic. This run shows where that line sits and how long it takes to see it.

**The card under test.**

| Field | Value |
|---|---|
| Corner | long premium (directional, or a vol catalyst) |
| Payoff | 1R stop, 2.5R target → `b = 2.50` |
| Expected win rate | `p = 0.35` |
| Cost | `c_R = 0.02R` per trade (2-leg, round trip) |
| Planned sample | 250 trades |

**Run it.**

```bash
py -3 scripts/payoff_check.py --tp 2.5 --sl 1.0 --p 0.35 --cost-r 0.02
```

**What the run says.** `b = 2.5000`, so `p* = 1/(1+2.5) = 28.57%`. A 35% win rate
clears that bar, and `E = 0.2250R` gross, `0.2050R` after cost — enough to be
`POSITIVE` against the sample's own resolution (`se_E = 0.1056R`). Note the two
things the run does *not* say: it does not say the strategy is profitable, and it
does not say `p = 0.35` is achievable. Both are the trader's estimate, and the
sensitivity panel prices the being-wrong case: five points off the win rate
(`p = 0.30`) drops `E` from `0.2250R` to `0.0500R`.

**Hand-check.** `b = 2.5/1.0 = 2.5`. `E = 0.35 × 2.5 − 0.65 = 0.225`.
`b* = 0.65/0.35 = 1.8571`. `p* = 1/3.5 = 0.2857`. `f* = 0.225/2.5 = 0.09`.
`sd² = 0.35(2.5−0.225)² + 0.65(−1.225)² = 1.811469 + 0.975406 = 2.786875`,
`sd = 1.6694`. `n_req = 4(1.6694/0.225)² = 220.20`. `L = ceil(5.521461/0.430783) = ceil(12.82) = 13`.
`R_max = 0.20/(13 × 1.5) = 1.03%`.

The output below is the tool's own, captured verbatim with no editing.

```
==============================================================================
OPTIONS PAYOFF CHECK  --  payoff_check.py 1.0.0
==============================================================================

R BASIS
  numeraire: 1R is the money lost when the stop fires; --tp and --sl share a unit and b = tp/sl re-bases it

ALGEBRA  (formulas are literal; substitute and check)
ALL QUANTITIES ARE IN R, where 1R is the money lost when the stop fires.
  b     = tp / sl                     the payoff ratio (win / loss)
  E     = p*b - (1-p)                 gross expectancy per trade, in R
  E_net = E - c_R                     expectancy after cost, in R
  b*    = (1-p) / p                   break-even payoff at this p
  p*    = 1 / (1+b)                   break-even win rate at this b
  edge  = p - p*                      win rate above the break-even rate
  f*    = E / b                       Kelly fraction of capital
  sd^2  = p*(b-E)^2 + (1-p)*(-1-E)^2  two-point std deviation, in R
  n_req = 4 * (sd / |E|)^2            trades needed to see the edge at 2 sigma
  L     = ceil( ln(N) / ln(1/(1-p)) ) expected longest losing streak in N
  R_max = D_tol / (L * safety)        largest risk per trade a streak survives

INPUTS
  input mode      : TP/SL
  tp / sl         : 2.5000 / 1.0000  (both in R)
  p (win rate)    : 35.00%
  cost            : 0.0200 R per trade (round trip)
  n (planned)     : 250
  d-tol / safety  : 20.00% of equity / 1.50 x

PAYOFF
  b       = tp/sl                  : 2.5000
  E       = p*b - (1-p)            : 0.2250 R per trade
  E_net   = E - c_R                : 0.2050 R per trade

BREAK-EVEN
  b*      = (1-p)/p                : 1.8571
  p*      = 1/(1+b)                : 28.57%
  edge    = p - p*                 : 6.43%

SIZE
  f*      = E/b                    : 9.00% of capital
  half-Kelly                       : 4.50% of capital

SAMPLE AND SURVIVAL
  sd      = sqrt(p(b-E)^2+(1-p)(-1-E)^2) : 1.6694 R
  se_E    = sd/sqrt(n)                   : 0.1056 R
  n_req   = 4*(sd/|E|)^2                 : 220.20  (ceil: 221)
  years_at_pace = n_req / trades_per_year: 0.88 years
  L       = ceil(ln(n)/ln(1/(1-p)))      : 13 trades  (raw: 12.82)
  R_max   = d_tol/(L*safety)             : 1.03% of equity per trade

SENSITIVITY  (the cost of being wrong about an input)
  scenario                                      E        E_net
  p -5pp -> 30.0%                          0.0500       0.0300
  p +5pp -> 40.0%                          0.4000       0.3800
  b -0.25 -> 2.250                         0.1375       0.1175
  b +0.25 -> 2.750                         0.3125       0.2925
  cost x0.5 -> 0.0100 R                    0.2250       0.2150
  cost x2.0 -> 0.0400 R                    0.2250       0.1850

  dE/dp = b + 1 and dE/db = p, so a win-rate improvement is worth
  (b+1)/p times a payoff improvement. Payoff is a rules change you
  can make today; a win rate needs a signal. Fix the payoff first.

==============================================================================
VERDICT
==============================================================================
  RULE (this is the rule; argue with it if you disagree):
    |E_net| <  se_E  ->  MARGINAL  (not separable from zero)
    E_net   >= se_E  ->  POSITIVE
    E_net   <= -se_E ->  NEGATIVE
    se_E = sd / sqrt(n), with n the PLANNED sample.

  POSITIVE: E_net = 0.2050 >= se_E = 0.1056: positive expectancy separable from zero at n = 250.

  This is arithmetic on YOUR inputs, not a forecast and not a
  backtest. It says what the corner pays if p and b are what you
  think they are. It cannot tell you whether they are.

==============================================================================
PROVENANCE AND LIMITS
==============================================================================
  This output is arithmetic on the inputs above. It is NOT market data,
  NOT a backtest, and NOT a forecast. No result here says a strategy is
  profitable; it says what a corner pays IF p and b are what you think
  they are, and p is an estimate with sampling error you have not
  measured. Sourced from CBOE and OCC exchange rules only for the
  mechanics of ticket counts and contract multipliers; no vendor, no
  network, no third-party dependency anywhere in this engine.
```
