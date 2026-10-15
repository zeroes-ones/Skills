# Check 3 — exactly break-even: 50%-of-credit target, 2×-credit stop, at an 80% win rate

**What this check is for.** The arithmetic identity at the centre of the whole
skill. The popular premium-selling management card needs an **80.00% win rate**
just to break even, and at that win rate the expectancy is exactly zero. This run
enters the card the way an options trader actually thinks about it — a credit and
a strike width — so the `1R = max loss` basis is derived rather than asserted.

**The card under test.**

| Field | Value |
|---|---|
| Structure | credit spread / condor, credit `$1.00` on a `$5.00` width (per share) |
| Max loss per spread | `(W − C) × 100 = $400.00` → this is `1R` |
| Target | `$50.00` = **50% of the credit** |
| Stop | `$200.00` = **2 × the credit** |
| Payoff ratio | `b = 50.00 / 200.00 = 0.25` (scale-free, so it does not matter that the stop is not the max loss) |
| Win rate | `p = 0.80` |
| Contract multiplier | `100` (US equity-option standard) |

**Run it.**

```bash
py -3 scripts/payoff_check.py --credit 1.00 --width 5.00 \
    --tp-money 50 --sl-money 200 --p 0.80
```

**What the run says.** `b* = (1−p)/p = 0.2500` — identical to `b`. `p* = 80.00%` —
identical to `p`. `E = 0.0000R`. At exactly its break-even win rate the card pays
nothing, and the tool reports `MARGINAL` rather than inventing a direction,
because `|E_net| = 0.0000` is inside one standard error. The sensitivity panel is
the useful part: at `p = 0.75` the corner pays `−0.0625R`; at `p = 0.85` it pays
`+0.0625R`. **The entire result lives inside a five-point band around a win rate
almost nobody measures.**

This is the arithmetic conclusion, not folklore: taking half the credit while
risking twice the credit is `b = 0.25`, and `b = 0.25` demands `p* = 0.80`.

**Hand-check.** `b = 50/200 = 0.25`. `E = 0.80 × 0.25 − 0.20 = 0.20 − 0.20 = 0.0000`.
`b* = 0.20/0.80 = 0.25`. `p* = 1/1.25 = 0.80`. `sd² = 0.80(0.25)² + 0.20(1.0)² = 0.05 + 0.20 = 0.25`,
`sd = 0.5000`. `n_req`: refused, `E = 0`. `L = ceil(5.521461/ln(5)) = ceil(3.43) = 4`.
`R_max = 0.20/(4 × 1.5) = 3.33%`.

The output below is the tool's own, captured verbatim with no editing.

```
==============================================================================
OPTIONS PAYOFF CHECK  --  payoff_check.py 1.0.0
==============================================================================

R BASIS
  structural: 1R = the structure's max loss (W - C) x multiplier = 400.00

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
  input mode      : CREDIT/WIDTH
  credit          : 1.00 (per share)   width: 5.00 (per share)   multiplier: 100
  per spread      : credit 100.00   width 500.00   max loss (W-C): 400.00
  target          : 50.00 (50.00% of credit)   stop: 200.00 (2.00 x credit)
  p (win rate)    : 80.00%
  cost            : 0.0000 R per trade (round trip)
  n (planned)     : 250
  d-tol / safety  : 20.00% of equity / 1.50 x

PAYOFF
  b       = tp/sl                  : 0.2500
  E       = p*b - (1-p)            : 0.0000 R per trade
  E_net   = E - c_R                : 0.0000 R per trade

BREAK-EVEN
  b*      = (1-p)/p                : 0.2500
  p*      = 1/(1+b)                : 80.00%
  edge    = p - p*                 : 0.00%

SIZE
  f*      = E/b                    : 0.00% of capital
  half-Kelly                       : 0.00% of capital

SAMPLE AND SURVIVAL
  sd      = sqrt(p(b-E)^2+(1-p)(-1-E)^2) : 0.5000 R
  se_E    = sd/sqrt(n)                   : 0.0316 R
  n_req   = 4*(sd/|E|)^2                 : n/a  (ceil: n/a)
  years_at_pace = n_req / trades_per_year: n/a
  L       = ceil(ln(n)/ln(1/(1-p)))      : 4 trades  (raw: 3.43)
  R_max   = d_tol/(L*safety)             : 3.33% of equity per trade
  NOTE n_req         : n/a: E = 0.0000 <= 0. You cannot see an edge that is not there, and no trade count creates one.
  NOTE years_at_pace : n/a: n_req is undefined
  INPUT NOTE      : quote units: credit 1.00 and width 5.00 are PER SHARE; x multiplier 100 gives 100.00 credit and 500.00 width per spread
  INPUT NOTE      : R basis: max loss = (width - credit) x multiplier = (5.00 - 1.00) x 100 = 400.00
  INPUT NOTE      : target is 50.00% of the credit; stop is 2.00 x the credit

SENSITIVITY  (the cost of being wrong about an input)
  scenario                                      E        E_net
  p -5pp -> 75.0%                         -0.0625      -0.0625
  p +5pp -> 85.0%                          0.0625       0.0625
  b -0.25 -> 0.000                        -0.2000      -0.2000
  b +0.25 -> 0.500                         0.2000       0.2000
  cost x0.5 -> 0.0000 R                    0.0000       0.0000
  cost x2.0 -> 0.0000 R                    0.0000       0.0000

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

  MARGINAL: |E_net| = 0.0000 < se_E = 0.0316: the expectancy is within one standard error of zero at n = 250, so it is not separable from noise at this sample.

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
