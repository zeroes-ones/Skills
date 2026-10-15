# Cost Drag per Leg and per Rung

Cost is a first-class term in the expectancy, not a rounding error appended at the
end. This file derives where it bites: per leg (it scales), per rung (it scales
faster), and per structure size (it does not scale at all). Every number is
`[COMPUTED]` from the ticket-count arithmetic.

---

## The cost model

Options cost is charged **per contract, per leg, per ticket**, and a position
generates two tickets per leg: one to open, one to close. So

```
tickets_round_trip = legs x 2                              [COMPUTED]
cost_per_trade     = fee_per_contract x legs x 2           [COMPUTED]
c_R                = cost_per_trade / R_dollars            [COMPUTED]
E_net              = E - c_R                               [COMPUTED]
```

`fee_per_contract` here is the all-in per-ticket cost: commission plus exchange and
regulatory fees plus the half-spread you cross. `[COMMON-PRACTICE]` The half-spread
is usually the largest of the three and the one most often left out, which is why a
zero-cost comparison between a 1-leg and a 4-leg structure is always wrong in the
same direction.

**The structural fact this file exists to state:** the ticket count is set by the
structure, and `R` is set by the market. The fee does not shrink when `R` does.

---

## Per leg: the fee multiplies, the edge does not

At `$0.65` per contract per ticket:

| Legs | Tickets (round trip) | Cost per trade | `c_R` on `R = $500` | `c_R` on `R = $100` |
|---|---|---|---|---|
| 1 (long call / short put) | 2 | `$1.30` | 0.0026 | 0.0130 |
| 2 (vertical spread) | 4 | `$2.60` | 0.0052 | 0.0260 |
| 3 (broken-wing butterfly / ratio) | 6 | `$3.90` | 0.0078 | 0.0390 |
| 4 (iron condor / iron butterfly) | 8 | `$5.20` | 0.0104 | 0.0520 |

The same table as an expectancy cost, on the long-premium card
(`b = 2.5`, `p = 0.35`, `E = 0.2250R` `[COMPUTED]`):

| Legs | `c_R` on `R = $500` | `E_net` | Verdict | `c_R` on `R = $100` | `E_net` | Verdict |
|---|---|---|---|---|---|---|
| 1 | 0.0026 | +0.2224 | POSITIVE | 0.0130 | +0.2120 | POSITIVE |
| 2 | 0.0052 | +0.2198 | POSITIVE | 0.0260 | +0.1990 | POSITIVE |
| 4 | 0.0104 | +0.2146 | POSITIVE | 0.0520 | **+0.1730** | POSITIVE, but 23% of the edge is gone |

At `R = $500` the leg count is nearly irrelevant. At `R = $100` the fourth leg
costs 23% of the edge. **Leg count is a cost decision only when `R` is small** —
which is the whole subject of `references/small-account-instrument-choice.md`.

Now take the same structure down to a size where the fee wins:

| `R_dollars` | Legs | `c_R` (`[COMPUTED]`) | `E_net` (`[COMPUTED]`) | Verdict |
|---|---|---|---|---|
| 500 | 4 | 0.0104 | +0.2146 | POSITIVE |
| 200 | 4 | 0.0260 | +0.1990 | POSITIVE |
| 100 | 4 | 0.0520 | +0.1730 | POSITIVE |
| 50 | 4 | 0.1040 | +0.1210 | POSITIVE |
| 25 | 4 | 0.2080 | +0.0170 | MARGINAL |
| **15** | **4** | **0.3467** | **−0.1217** | **NEGATIVE** |

At `R = $15` — a narrow structure, say a 1-wide spread carrying 85 cents of credit
— the fee alone is larger than the entire gross edge. The tool prints this without
softening it:

```
NOTE cost: cost 0.3467 R >= gross E 0.2250 R: after cost this corner pays nothing
or loses. Cost is not a rounding term here; it is the whole result.
```

---

## Per rung: the fee multiplies by the rung count, the cash divides

A scale-out splits one closing decision into `N` closing decisions, each of which
pays one ticket per leg.

```
fee_per_rung   = legs x fee_per_contract          [COMPUTED]
total_fee      = N x legs x fee_per_contract      [COMPUTED]
single_close   = legs x fee_per_contract          [COMPUTED]
extra_fee      = (N - 1) x legs x fee_per_contract  [COMPUTED]
banked_per_rung = position_value / N              [COMPUTED]
```

A rung is **fee-negative** when the cash it banks is smaller than the fee it pays
to bank it:

```
fee_negative  iff  position_value / N  <  legs x fee_per_contract
```

Solving for the whole remaining structure:

```
fee_negative  iff  position_value  <  N x legs x fee_per_contract       [COMPUTED]
```

For a 4-leg structure at `$0.65` and 3 rungs, the threshold is
`3 × 4 × 0.65 = $7.80` per spread `[COMPUTED]`. **The threshold is paid per
spread, so it is a size test, not a tactics test.** A structure worth three cents a
share ($3.00 per spread) never clears it; a structure worth ten cents ($10.00)
clears it comfortably.

### The three-rung result

At a `$5.00` mark on a 4-leg structure, 3 rungs:

| Term | Derivation | Value |
|---|---|---|
| Fee per rung | `4 × 0.65` | `$2.60` |
| Cash banked per rung | `5.00 / 3` | `$1.67` |
| Shortfall per rung | `1.67 − 2.60` | `−$0.93` |
| Total fee, 3 rungs | `3 × 2.60` | `$7.80` |
| Single close | `4 × 0.65` | `$2.60` |
| **Extra fee vs one close** | `7.80 − 2.60` | **`$5.20`** |

`$5.20` is `4 × 2 × 0.65` `[COMPUTED]` — **exactly the round-trip fee of opening
the same four-leg structure in the first place.** The scale-out pays a whole extra
opening fee to bank two-thirds of what it would have received for one close. A
management technique that costs an entire additional trade is not a refinement of
the trade; it is a second trade.

Note also the shape: the fee ratio worsens as `N²` while the cash per rung worsens
as `N`. Multi-rung scaling is the single most fee-inefficient thing a small options
account can do, and it is usually recommended without a fee threshold attached.

---

## Cost as a required win rate

Because the cost enters the expectancy additively, it enters the required win rate
as an offset. Solving `p(b+1) − 1 − c_R = 0`:

```
p*_net = (1 + c_R) / (1 + b)                       [COMPUTED]
```

At `b = 0.5` (the defensible credit card):

| `c_R` | `p*_net` | vs the gross 66.67% |
|---|---|---|
| 0.000 | 66.67% | — |
| 0.005 | 67.00% | +0.33 pp |
| 0.026 | 68.40% | +1.73 pp |
| 0.052 | 70.13% | +3.47 pp |
| 0.104 | 73.60% | +6.93 pp |

At `b = 0.25` (the 50%/2× card):

| `c_R` | `p*_net` | vs the gross 80.00% |
|---|---|---|
| 0.000 | 80.00% | — |
| 0.005 | 80.40% | +0.40 pp |
| 0.026 | 82.08% | +2.08 pp |
| 0.052 | 84.16% | +4.16 pp |
| 0.104 | 88.32% | +8.32 pp |

The wide-stop card pays a **higher** cost penalty in win-rate points than the
tight-stop card, for the same `c_R`, because `1/(1+b)` is larger when `b` is small.
Cost and payoff width compound against each other.

---

## Failure modes

1. **Failure mode — commission is counted and the half-spread is not.** The
   half-spread is usually the largest component and it scales with the number of
   legs crossed, exactly like the commission does.
2. **Failure mode — one ticket is counted per leg instead of two.** A round trip is
   two tickets per leg. A four-leg structure pays eight, and a card costed at four
   tickets understates `c_R` by 100%.
3. **Failure mode — cost is amortised across the whole year rather than charged per
   trade.** `E_net = E − c_R` is per trade. Averaging the fee across winners only
   hides it from the losers, where it also applies.
4. **Failure mode — a multi-rung exit is adopted without checking the threshold.**
   The threshold is `N × legs × fee_per_contract` per spread. Below it, every rung
   banks less than it pays.
5. **Failure mode — the fee is treated as fixed while `R` is reduced.** Cutting size
   to reduce risk raises `c_R`; there is a size below which the card has no edge left
   and the iteration protocol's cost cycle is the only thing that finds it.
6. **Failure mode — a wide structure is compared to a narrow one on gross
   expectancy.** The comparison must be `E_net` on both sides, at the real `R`.
7. **Failure mode — assignment or exercise fees are omitted.** Assignment,
   exercise and expiry-processing fees exist and are quoted by the exchange, not by
   the broker's headline commission. A card whose exits include assignment must
   include them.
8. **Failure mode — `c_R` is computed against the structural max loss while the
   trade is managed at a tighter stop.** Same trap as in
   `references/stop-and-target-arithmetic.md`: a larger `R` makes the fee look
   smaller than it is.
9. **Failure mode — cost is revisited only after a losing month.** Cost is a
   constant in the card. It should be checked when the card is written, not when a
   month disappoints.

---

## Worked checks

```bash
# the fee turns a positive corner negative on a small structure
py -3 scripts/payoff_check.py --tp 2.5 --sl 1.0 --p 0.35 \
    --fee-per-contract 0.65 --legs 4 --r-dollars 15

# the same fee on a large structure: +0.2146 R net
py -3 scripts/payoff_check.py --tp 2.5 --sl 1.0 --p 0.35 \
    --fee-per-contract 0.65 --legs 4 --r-dollars 500

# the three-rung threshold, derived
py -3 scripts/payoff_check.py --scaling-check --legs 4 \
    --fee-per-contract 0.65 --rung-split 3 --position-value 5.00
```

Captured verbatim output: `examples/checks/06-cost-turns-positive-into-negative.md`
and `examples/checks/04-fee-negative-rung-scaling.md`.

See also: `references/small-account-instrument-choice.md`,
`references/payoff-corners-for-options.md`,
`references/the-iteration-protocol.md`.
