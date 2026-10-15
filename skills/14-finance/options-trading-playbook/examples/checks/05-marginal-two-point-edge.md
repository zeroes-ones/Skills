# Check 5 — marginal: a two-percentage-point edge over the break-even win rate

**What this check is for.** The most dangerous card in the book is not the
negative one — a negative expectancy announces itself. It is the one that is
*positive on paper and unmeasurable in practice*. Here the payoff ratio is
`b = 0.50` (a 50%-of-credit target with a 1×-credit stop), the break-even win
rate is `66.67%`, and the trader believes they win `68%`. The edge is two
percentage points. This run prices what that is worth.

**The card under test.**

| Field | Value |
|---|---|
| Corner | short premium, target 0.5 × credit, stop at 1 × credit |
| Payoff ratio | `b = 0.5` |
| Break-even win rate | `p* = 1/1.5 = 66.67%` |
| Believed win rate | `p = 0.68` |
| Planned sample | 250 trades |

**Run it.**

```bash
py -3 scripts/payoff_check.py --tp 0.5 --sl 1.0 --p 0.68
```

**What the run says.** `E = +0.0200R` gross and after cost — genuinely positive,
and `POSITIVE` in sign. But `se_E = 0.0443R` at 250 trades, so `|E_net| = 0.0200`
sits **inside** the noise: `MARGINAL`. `n_req = 4 × (0.6997/0.02)² = 4,896` trades
to see that edge at two sigma, which at 250 trades a year is **19.58 years**.

That is the honest answer to "is a 68% win rate good enough on a 0.5-payoff
structure?" It is good enough to break even and barely good enough to pay. It is
not good enough to *know*. And the sensitivity panel makes the sample problem
worse rather than better: `p − 5pp` (`63%`, a one-in-twenty sampling miss) turns
`E` to `−0.0550R`. **A card whose sign flips inside five points of its own input
is a card you cannot grade in a decade of trading.**

**Hand-check.** `b = 0.5/1.0 = 0.5`. `E = 0.68 × 0.5 − 0.32 = 0.34 − 0.32 = 0.02`.
`b* = 0.32/0.68 = 0.4706`. `p* = 1/1.5 = 0.6667`. `edge = 0.68 − 0.6667 = 1.33%`.
`sd² = 0.68(0.48)² + 0.32(1.02)² = 0.156672 + 0.332928 = 0.4896`, `sd = 0.6997`.
`n_req = 4 × (0.6997/0.02)² = 4 × 1224 = 4,896`. `se_E = 0.6997/√250 = 0.0443`.
`L = ceil(5.521461/1.139434) = ceil(4.85) = 5`. `R_max = 0.20/7.5 = 2.67%`.

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
  tp / sl         : 0.5000 / 1.0000  (both in R)
  p (win rate)    : 68.00%
  cost            : 0.0000 R per trade (round trip)
  n (planned)     : 250
  d-tol / safety  : 20.00% of equity / 1.50 x

PAYOFF
  b       = tp/sl                  : 0.5000
  E       = p*b - (1-p)            : 0.0200 R per trade
  E_net   = E - c_R                : 0.0200 R per trade

BREAK-EVEN
  b*      = (1-p)/p                : 0.4706
  p*      = 1/(1+b)                : 66.67%
  edge    = p - p*                 : 1.33%

SIZE
  f*      = E/b                    : 4.00% of capital
  half-Kelly                       : 2.00% of capital

SAMPLE AND SURVIVAL
  sd      = sqrt(p(b-E)^2+(1-p)(-1-E)^2) : 0.6997 R
  se_E    = sd/sqrt(n)                   : 0.0443 R
  n_req   = 4*(sd/|E|)^2                 : 4896.00  (ceil: 4896)
  years_at_pace = n_req / trades_per_year: 19.58 years
  L       = ceil(ln(n)/ln(1/(1-p)))      : 5 trades  (raw: 4.85)
  R_max   = d_tol/(L*safety)             : 2.67% of equity per trade

SENSITIVITY  (the cost of being wrong about an input)
  scenario                                      E        E_net
  p -5pp -> 63.0%                         -0.0550      -0.0550
  p +5pp -> 73.0%                          0.0950       0.0950
  b -0.25 -> 0.250                        -0.1500      -0.1500
  b +0.25 -> 0.750                         0.1900       0.1900
  cost x0.5 -> 0.0000 R                    0.0200       0.0200
  cost x2.0 -> 0.0000 R                    0.0200       0.0200

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

  MARGINAL: |E_net| = 0.0200 < se_E = 0.0443: the expectancy is within one standard error of zero at n = 250, so it is not separable from noise at this sample.

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
