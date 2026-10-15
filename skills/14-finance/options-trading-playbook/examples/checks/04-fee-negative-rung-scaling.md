# Check 4 — fee-negative scaling: a three-rung scale-out on a four-leg structure

**What this check is for.** Cost is a first-class term, not a rounding error.
Splitting an exit into rungs multiplies a fixed per-spread closing fee by the
rung count while dividing the banked cash by the same count. This run derives the
threshold at which multi-rung scaling turns fee-negative, and shows a concrete
structure that is on the wrong side of it.

**The structure under test.**

| Field | Value |
|---|---|
| Structure | 4-leg (iron condor / iron butterfly) |
| Fee per contract per ticket | `$0.65` |
| Tickets to close | one per leg → `legs × fee = 4 × 0.65 = $2.60` per rung |
| Rungs | 3 |
| Current mark of the whole structure | `$5.00` per spread |

**Run it.**

```bash
py -3 scripts/payoff_check.py --scaling-check --legs 4 \
    --fee-per-contract 0.65 --rung-split 3 --position-value 5.00
```

**What the run says.** The derived threshold is `position_value < rung_split × legs × fee_per_contract`
= `3 × 4 × 0.65 = $7.80`. At a `$5.00` mark the split is `FEE-NEGATIVE`: each rung
banks `$1.67` and pays `$2.60`, a shortfall of `$0.93` per rung, `$2.80` across
the three rungs. The extra cost over a single close is `(3 − 1) × 4 × 0.65 = $5.20`
— **exactly the round-trip fee of opening the same four-leg structure in the first
place.** A scale-out that pays a whole extra opening fee is not a management
technique; it is a second trade.

The strategic consequence, derived rather than asserted: a scale-out is
fee-positive only when the *whole remaining structure* is worth more than
`rung_split × legs × fee_per_contract` per spread. For a 4-leg structure at
`$0.65` and 3 rungs, that is `$7.80` — which a structure worth three cents per
share ($3.00) never reaches, and which a structure worth ten cents ($10.00)
clears comfortably.

**Hand-check.** `fee_per_rung = 4 × 0.65 = 2.60`. `banked_per_rung = 5.00/3 = 1.6667`.
`1.6667 < 2.60` → fee-negative by `0.9333` per rung. `total_fee = 3 × 2.60 = 7.80`.
`single_close_fee = 2.60`. `extra_fee = 7.80 − 2.60 = 5.20`. `threshold = 3 × 2.60 = 7.80`.

The output below is the tool's own, captured verbatim with no editing.

```
==============================================================================
OPTIONS PAYOFF CHECK  --  payoff_check.py 1.0.0
==============================================================================

==============================================================================
SCALING CHECK  (multi-rung fee threshold)
==============================================================================
  fee_per_rung   = legs * fee_per_contract = 4 * 0.65 = 2.60
  banked_per_rung= position_value / rung_split = 5.00 / 3 = 1.67
  total_fee      = rung_split * fee_per_rung = 3 * 2.60 = 7.80
  single close   = 2.60 (one rung's worth of tickets)
  extra_fee      = (rung_split - 1) * legs * fee = 2 * 4 * 0.65 = 5.20

  THRESHOLD (derived, not asserted):
    a rung is fee-negative when  position_value / rung_split
    < legs * fee_per_contract. Solving for the whole position:

      fee_negative  iff  position_value < rung_split * legs * fee_per_contract = 3 * 4 * 0.65 = 7.80

    threshold = 7.80 per spread. At position_value = 5.00 the split is
    FEE-NEGATIVE: each rung banks 1.67 and pays 2.60, a shortfall of
    0.93 per rung, 2.80 across 3 rungs.

  Note the shape of this: the threshold is paid per SPREAD, so a
  small structure crosses it never. Scaling rungs multiplies a fixed
  per-spread fee by the rung count while dividing the banked cash by
  the same count -- the fee ratio worsens by rung_split^2.

==============================================================================
VERDICT
==============================================================================
  No card was supplied, so there is no verdict. A scaling check or
  a realised-cohort table answers a different question.

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
