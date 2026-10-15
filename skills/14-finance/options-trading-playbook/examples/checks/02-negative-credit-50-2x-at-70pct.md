# Check 2 — a clearly negative corner: the credit spread, 50%-of-credit target, 2×-credit stop

**What this check is for.** The most common premium-selling management card in
the retail options market — take profit at 50% of the credit, stop at 2× the
credit — priced on the win rate most traders actually achieve with it. It is
negative, and the reason is visible in one number.

**The card under test.**

| Field | Value |
|---|---|
| Corner | short premium (credit spread / iron condor / short put) |
| Payoff | target 0.5 × credit, stop 2 × credit → `b = 0.5C / 2C = 0.25` |
| Realised win rate | `p = 0.70` |
| Cost | `c_R = 0R` (set to zero deliberately, so the negativity cannot be blamed on fees) |

**Run it.**

```bash
py -3 scripts/payoff_check.py --tp 0.5 --sl 2.0 --p 0.70
```

**What the run says.** `b = 0.2500`, so `p* = 1/1.25 = 80.00%`. At `p = 0.70`,
`E = 0.70 × 0.25 − 0.30 = −0.1250R`. The edge is `−10.00%` — ten percentage
points *below* the break-even rate. `f*` is negative, which the tool prints
un-clipped because the sign is the answer: do not bet this corner at this p and
b. `n_req` is refused rather than quoted, because a trade count cannot reveal an
edge that is not there.

The important reading is the sensitivity panel: `b + 0.25` (payoff 0.5 rather
than 0.25) turns `E` to `+0.0500R`. That is a **rules change**, not a forecast.

**Hand-check.** `b = 0.5/2.0 = 0.25`. `E = 0.70 × 0.25 − 0.30 = 0.175 − 0.300 = −0.125`.
`b* = 0.30/0.70 = 0.4286`. `p* = 1/1.25 = 0.80`. `edge = 0.70 − 0.80 = −0.10`.
`sd² = 0.70(0.375)² + 0.30(0.875)² = 0.098437 + 0.229688 = 0.328125`, `sd = 0.5728`.
`n_req`: refused, `E ≤ 0`. `L = ceil(5.521461/1.203973) = ceil(4.59) = 5`.
`R_max = 0.20/(5 × 1.5) = 2.67%`.

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
  tp / sl         : 0.5000 / 2.0000  (both in R)
  p (win rate)    : 70.00%
  cost            : 0.0000 R per trade (round trip)
  n (planned)     : 250
  d-tol / safety  : 20.00% of equity / 1.50 x

PAYOFF
  b       = tp/sl                  : 0.2500
  E       = p*b - (1-p)            : -0.1250 R per trade
  E_net   = E - c_R                : -0.1250 R per trade

BREAK-EVEN
  b*      = (1-p)/p                : 0.4286
  p*      = 1/(1+b)                : 80.00%
  edge    = p - p*                 : -10.00%

SIZE
  f*      = E/b                    : -50.00% of capital
  half-Kelly                       : -25.00% of capital

SAMPLE AND SURVIVAL
  sd      = sqrt(p(b-E)^2+(1-p)(-1-E)^2) : 0.5728 R
  se_E    = sd/sqrt(n)                   : 0.0362 R
  n_req   = 4*(sd/|E|)^2                 : n/a  (ceil: n/a)
  years_at_pace = n_req / trades_per_year: n/a
  L       = ceil(ln(n)/ln(1/(1-p)))      : 5 trades  (raw: 4.59)
  R_max   = d_tol/(L*safety)             : 2.67% of equity per trade
  NOTE f*            : f* is negative: the Kelly criterion says do not bet this corner at this p and b. A negative fraction is information, not a sizing instruction -- it is reported un-clipped.
  NOTE n_req         : n/a: E = -0.1250 <= 0. You cannot see an edge that is not there, and no trade count creates one.
  NOTE years_at_pace : n/a: n_req is undefined

SENSITIVITY  (the cost of being wrong about an input)
  scenario                                      E        E_net
  p -5pp -> 65.0%                         -0.1875      -0.1875
  p +5pp -> 75.0%                         -0.0625      -0.0625
  b -0.25 -> 0.000                        -0.3000      -0.3000
  b +0.25 -> 0.500                         0.0500       0.0500
  cost x0.5 -> 0.0000 R                   -0.1250      -0.1250
  cost x2.0 -> 0.0000 R                   -0.1250      -0.1250

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

  NEGATIVE: E_net = -0.1250 <= -se_E = -0.0362: negative expectancy separable from zero at n = 250.

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
