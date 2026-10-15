# Liquidity and Exit-Cost Planning

For a diversified equity book, liquidity is a nuisance. For a concentrated one, it is the risk. This
file states the exit contract every position must satisfy **before** it is taken, the participation
and cost arithmetic, and the reason the phrase "the risk is the drawdown" is wrong for any position
that is large relative to its own market.

## §1 — Plan the Exit at Entry

A position without a recorded exit is not a position. It is a future forced sale. Four fields are
recorded before the fill, in the same record as the entry:

| Field | Meaning | Default or cap |
|---|---|---|
| `exit_route` | The named mechanism by which the position leaves the book | (a) scale out against a target; (b) sell into strength over N sessions at a stated participation rate; (c) sell into a known event window (index add, lock-up expiry, tender); (d) sell the whole position on a stated trigger; (e) hold to a stated horizon and reassess; (f) **broker liquidation — this is not a route.** If (f) is the only route, the position fails the gate |
| `exit_cost_pct` | Round-trip cost as a percentage of position value | `(ask − bid) / mid` plus the impact term of §3 |
| `exit_cost_cap` | The worst round-trip cost this position may carry | **core ≤ 3%; satellite ≤ 5%** of position value (the same caps the options book uses, so the two skills speak one language) |
| `size_vs_adv` | The sizing input that makes the exit cost reachable | `position_shares ≤ min(20% of 20-day ADV, position value ≤ 25% of 20-day dollar volume)` — and see §4 for why 20% is a ceiling and 10% is a plan |

**Why the ADV cap is really an exit-cost cap.** Spread is a per-share term while position value is
linear in shares, so the *percentage* cost does not rise through the spread at all — it rises
through the **impact** term, which grows with the fraction of daily volume the holder represents.
Sizing past a quarter of the day's dollar volume is how a position that looked cheap to enter
becomes expensive to leave.

## §2 — The Exit Route Is a Schedule, Not an Intention

An acceptable `exit_route` answers all four of these:

1. **What instrument or mechanism** — and if it is a limit order, at what price relative to mid.
2. **Over how many sessions**, at what participation rate.
3. **What fills it** — a target price, a date, an event, a rebalance.
4. **What the fallback is** if the first three do not occur.

"The market" is not a mechanism. "When it recovers" is not a schedule. "The broker will handle it"
is route (f) wearing a costume.

## §3 — Cost Arithmetic [COMPUTED]

Define, for one round trip (enter and exit):

```
one_way_cost_pct   = 0.5 × spread_pct + impact_pct
round_trip_cost_pct =        spread_pct + 2 × impact_pct
```

where

```
spread_pct = (ask − bid) / mid
impact_pct = k × σ_daily × sqrt(Q / ADV)          [ESTIMATED ±50%]
```

`k` is a desk constant and `σ_daily` is a daily-volatility window; both are **modelling choices, not
published facts**, which is why the impact term carries an error bound and the spread term does not.
The square-root shape is the part that matters: **impact grows with the square root of the fraction
of daily volume traded**, so going from 5% of ADV to 20% of ADV doubles the impact, and going from
5% to 80% quadruples it.

### §3.1 — A concentrated position, end to end

Position: **$150,000** — 12,500 shares of a small-cap at $12.00, in a $500,000 NAV book (30% of NAV).
Market: bid $11.95 / ask $12.05, 20-day ADV 80,000 shares/day.

```
SPREAD                          $0.10 / $12.00                = 0.83% of mid
SIZE                           12,500 / 80,000               = 15.6% of ADV
IMPACT  (k = 1.0, σ_daily = 3%) 1.0 × 0.03 × sqrt(0.156)      = 1.19%  [ESTIMATED ±50%]
ONE-WAY EXIT COST               0.42% + 1.19%                = 1.61%
ROUND-TRIP COST                 0.83% + (2 × 1.19%)          = 3.21%
EXIT-ONLY DOLLARS              1.61% × $150,000             = $2,415
ROUND-TRIP DOLLARS             3.21% × $150,000             = $4,815
```

Against the caps in §1: **3.21% sits between the 3% core cap and the 5% satellite cap**, so this is a
satellite position — or it is sized down until it fits the core cap.

### §3.2 — Why the exit, not the drawdown, is the real risk

Same position. Two ways to lose money:

```
A 20% DRAWDOWN          $150,000 × 0.20 = $30,000  — a paper loss. It can recover.
                                                        It does recover, or it does not.
THE EXIT                $150,000 × 3.21% = $4,815   — gone the moment the position is closed.
                                                        It cannot recover. It is the price of
                                                        having been in the position at all.
STRESSED EXIT           spread widening of 1.3× to 2.0×  [ESTIMATED ±25%]
                        at 1.3×:  spread 0.8333% × 1.3 = 1.0833%
                                  round trip 1.0833% + 2.3717% = 3.4550%
                                  → × $150,000 ≈ $5,183
                        at 2.0×:  spread 0.8333% × 2.0 = 1.6667%
                                  round trip 1.6667% + 2.3717% = 4.0384%
                                  → × $150,000 ≈ $6,058
                        REACHABLE RANGE ≈ $5,183 to ≈ $6,058
                        ($7,000 would be a 4.6667% round trip, i.e. a ×2.75 spread widening —
                         outside the modelled 1.3×–2.0× band, so it is not an endpoint of it)
```

[COMPUTED] from the §3 cost model and the stated inputs, at the stated widening multipliers; the
multipliers themselves are [ESTIMATED ±25%]. **Both endpoints come from the multiplier, not from the
midpoint** — 1.3× gives the low end and 2.0× the high end, and the mid-range figure the model is
sometimes quoted with (3.75% × $150,000 = $5,625) is a **midpoint**, not a bound. The drawdown is the
number that appears on a screen every day, so it gets all the attention. The exit cost is the number
that appears once, at the end, when the holder has the least ability to negotiate — and for a
position that is 15% of its own daily volume, it is the number that actually decides the outcome.
**A concentrated position's real risk is the exit, not the drawdown.** Say that to the user in those words.

## §4 — Participation and Days to Liquidate

```
days_to_liquidate = (position_shares / ADV) / participation_rate
```

| Position as % of ADV | At 10% participation | At 20% participation | At 30% participation |
|---|---|---|---|
| 1% | 0.1 days | 0.05 days | 0.03 days |
| 5% | 0.5 days | 0.25 days | 0.17 days |
| 10% | 1.0 day | 0.5 days | 0.33 days |
| 20% | 2.0 days | 1.0 day | 0.67 days |
| 50% | 5.0 days | 2.5 days | 1.7 days |
| 100% | 10.0 days | 5.0 days | 3.3 days |

Two readings of the same table:

- **At 10% participation, a position equal to its full ADV takes ten sessions.** Ten sessions of
  exposure to a market that can move 3% a day is a much bigger risk than the spread.
- **At 30% participation the impact term punishes you.** The table shows the *time* falling; §3
  shows the *cost* rising with the square root of the participation. Participation above 20% is
  how a holder becomes the market in their own position — the equity analogue of being the market
  maker.

The ceiling is 20% of ADV. The plan is 10%. The 20% figure is for a forced exit; if the position can
only be exited at 20%, the exit is already an emergency.

## §5 — Liquidity Deterioration Is a Trigger, Not a Detail

ADV and spread are not constants. Both change on news, on index events, on a halt, on a change in
borrow, and on ordinary seasonal thinning. The exit record therefore has a **re-measurement
cadence**, not a single measurement:

- Re-measure spread and ADV **weekly** for ordinary positions.
- Re-measure **immediately** on any of: a new 52-week low, a gap open of more than 5%, a halt, a
  delisting-related announcement, a threshold-list appearance, an index reconstitution effective
  date, or a lock-up expiry in the name.
- Re-compute `exit_cost_pct` every time the two inputs move, and re-test against `exit_cost_cap`.
  A position that has drifted from 3.0% to 5.5% while nothing was "decided" has quietly become
  unsellable at its own cap.

## §6 — Failure Modes

1. **No exit route recorded at entry.** The most common failure in the entire skill.
2. **Exit route (f) in disguise.** "The broker will manage it" is a liquidation, not a plan.
3. **Sizing on the entry cost and not the exit cost.** Entry into a thin name is easier than exit
   from it; the round trip is the number that matters.
4. **Treating the ADV cap as the comfort zone.** 20% of ADV is a ceiling for emergencies; the plan
   is 10%.
5. **Ignoring the square-root shape of impact.** Doubling size doubles the dollar cost but raises
   the percentage cost by roughly 41%.
6. **Measuring `exit_cost_pct` once.** Spreads and volume move; a liquid position becomes illiquid
   without any decision being made.
7. **Believing a limit order at mid will fill at size.** At 15% of ADV it will not, and the position
   is then exited in pieces at whatever the pieces fetch.
8. **Confusing price risk with exit risk.** The drawdown is the visible number; the exit is the
   binding one.
9. **Scheduling an exit into an event window without checking the event's own clock.** See
   `index-and-event-calendar.md` — reconstitution, lock-up and expiry all move the opposite way to
   the concentrated seller.
10. **Holding a position whose exit cost exceeds its expected edge.** At 3.21% round trip, an
    expected edge of 2% is a position that loses money on the round trip even when the thesis is
    right.

## §7 — Verification

- [ ] Every open position has a non-null `exit_route` that is not (f).
- [ ] Every open position has `exit_cost_pct ≤ exit_cost_cap`, with both figures shown.
- [ ] Every open position's `size_vs_adv` is recorded and within the 20% ceiling.
- [ ] A `days_to_liquidate` figure is reported for every position at 10% participation.
- [ ] The spread-re-measurement cadence is set, and the trigger list of §5 is wired.
- [ ] Where the user holds a concentrated position, the sentence stating that the exit, not the
      drawdown, is the real risk has been said out loud with their own numbers.
