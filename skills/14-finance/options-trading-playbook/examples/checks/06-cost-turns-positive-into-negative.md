# Check 6 — cost turns a positive corner negative

**What this check is for.** The same card as Check 1, on a structure small enough
that the ticket count dominates the risk unit. The gross expectancy is unchanged
at `+0.2250R`; the strategy is now negative, and no part of that change came from
the market.

**The card under test.**

| Field | Value |
|---|---|
| Corner | long premium, 1R stop, 2.5R target → `b = 2.50` |
| Expected win rate | `p = 0.35` |
| Structure | 4 legs |
| Fee per contract per ticket | `$0.65` |
| Round-trip tickets | `legs × 2 = 8` → `cost_per_trade = 0.65 × 4 × 2 = $5.20` |
| `1R` | `$15.00` (a narrow structure — e.g. a 1-wide spread carrying `$0.85` of credit) |

**Run it.**

```bash
py -3 scripts/payoff_check.py --tp 2.5 --sl 1.0 --p 0.35 \
    --fee-per-contract 0.65 --legs 4 --r-dollars 15
```

**What the run says.** `c_R = 5.20 / 15.00 = 0.3467R`, and `E_net = 0.2250 − 0.3467 =
−0.1217R` → `NEGATIVE`. The tool's own cost panel prints the derivation; the
`NOTE cost` line states the finding without softening it: *cost is not a rounding
term here; it is the whole result.*

The sensitivity panel then shows the shape of the problem. Halving the cost
(`cost × 0.5` → `0.1733R`) recovers `+0.0517R`. Doubling it (`0.6933R`) gives
`−0.4683R`. **The fee is larger than the edge, and it scales with leg count while
the edge does not.** On a `$500` max-loss structure the same `$5.20` is
`c_R = 0.0104R` and the card stays positive; on `$15` it is `0.3467R` and the card
dies. Same strategy, same `p`, same `b`, different instrument size.

**Hand-check.** `cost_per_trade = 0.65 × 4 × 2 = 5.20`. `c_R = 5.20/15 = 0.346667`.
`E = 0.35 × 2.5 − 0.65 = 0.225`. `E_net = 0.225 − 0.346667 = −0.121667 ≈ −0.1217`.
`se_E = 1.6694/√250 = 0.1056`. `|−0.1217| > 0.1056` → `NEGATIVE`.

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
  cost            : 0.3467 R per trade (round trip)
  n (planned)     : 250
  d-tol / safety  : 20.00% of equity / 1.50 x

PAYOFF
  b       = tp/sl                  : 2.5000
  E       = p*b - (1-p)            : 0.2250 R per trade
  E_net   = E - c_R                : -0.1217 R per trade

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
  NOTE cost          : cost 0.3467 R >= gross E 0.2250 R: after cost this corner pays nothing or loses. Cost is not a rounding term here; it is the whole result.

SENSITIVITY  (the cost of being wrong about an input)
  scenario                                      E        E_net
  p -5pp -> 30.0%                          0.0500      -0.2967
  p +5pp -> 40.0%                          0.4000       0.0533
  b -0.25 -> 2.250                         0.1375      -0.2092
  b +0.25 -> 2.750                         0.3125      -0.0342
  cost x0.5 -> 0.1733 R                    0.2250       0.0517
  cost x2.0 -> 0.6933 R                    0.2250      -0.4683

  dE/dp = b + 1 and dE/db = p, so a win-rate improvement is worth
  (b+1)/p times a payoff improvement. Payoff is a rules change you
  can make today; a win rate needs a signal. Fix the payoff first.

==============================================================================
COST DERIVATION  (per contract, per leg, round trip)
==============================================================================
  cost_per_trade = fee_per_contract * legs * 2
                 = 0.65 * 4 * 2 = 5.20
  tickets per round trip = legs * 2 = 8
  c_R            = cost_per_trade / R_dollars
                 = 5.20 / 15.00 = 0.3467 R

  The x2 is the round trip: an OPENING ticket and a CLOSING ticket
  for every leg. A four-leg structure pays eight tickets, not four.
  Cost scales with legs AND with tickets; R does not.

==============================================================================
VERDICT
==============================================================================
  RULE (this is the rule; argue with it if you disagree):
    |E_net| <  se_E  ->  MARGINAL  (not separable from zero)
    E_net   >= se_E  ->  POSITIVE
    E_net   <= -se_E ->  NEGATIVE
    se_E = sd / sqrt(n), with n the PLANNED sample.

  NEGATIVE: E_net = -0.1217 <= -se_E = -0.1056: negative expectancy separable from zero at n = 250.

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
