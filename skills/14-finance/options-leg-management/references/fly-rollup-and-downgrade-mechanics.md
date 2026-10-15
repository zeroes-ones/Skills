# Fly Roll-Up and Vertical Downgrade Mechanics

Two leg operations dominate fly management: moving the whole fly up when the underlying has run
(**financed roll-up**, tag `RU`), and removing the far wing when it has stopped paying
(**vertical downgrade**, tag `VD`). They solve opposite problems and are routinely confused.

| | Financed roll-up (`RU`) | Vertical downgrade (`VD`) |
|---|---|---|
| Problem it solves | The body is now below spot; the profit zone has moved away | The far wing is dead or illiquid; you are paying theta for a tail you no longer believe |
| Package | Close the current fly, open the same fly at higher strikes — ONE order at a net price | `{ sell 1× K3 + buy 1× K2 }` — ONE order |
| Result | Same fly shape, higher strikes | `+1 K1 / −1 K2`, a debit call spread |
| Direction of cash | Prefer a credit; a debit must be funded by realized proceeds | Always a net debit (you buy back a body worth more than the wing) |
| Gate | Net debit ≤ realized proceeds AND new body above spot with room AND DTE ≥ 5 | Far wing ≥ 30% of structure value, OR DTE ≤ 7, OR IV percentile ≥ 80 |
| Failure signature | A roll funded by new capital — a disguised size increase | Downgrading a wing that was still carrying the tail's value |

## Financed roll-up mechanics

### What "financed" means, exactly

A roll-up is financed when its cash flow is non-negative **or** when its debit is covered by
cash already realized from the same structure. It is *not* financed when the debit is paid out of
the account's general cash. That distinction is the whole rule.

```text
  roll is LEGAL  when:  package_net_credit >= 0
                    OR  package_net_debit <= realized_proceeds_from_this_structure
  roll is an ADD when:  package_net_debit >  realized_proceeds        (R8 territory)
```

Worked arithmetic lives in `(references/leg-arithmetic-worked-examples.md)`, Example G:
`current mark $2.80 − new fly cost $1.95 = $0.85 credit = $85 per unit` `[COMPUTED]` from
`[ESTIMATED]` inputs. Both gates pass there, so the roll is legal.

### The geometry gate

Financing is necessary, not sufficient. A roll-up must also leave the **new body above spot**.
A body that is rolled up into but sits below spot is a position that has been moved deeper into
the money while being called an extension.

| Spot relative to the new body | Verdict |
|---|---|
| New body > spot, by more than roughly the remaining expected move | Legal — this is what the roll is for |
| New body ≈ spot | Marginal: the fly's maximum-profit point is at the money, which is where the risk is highest during the roll window |
| New body < spot | Reject. That is not an extension, it is a chase |

### The roll cap

`[COMMON-PRACTICE]` Two roll-ups per position is the desk's working cap. The reason is not
superstition: each roll is a new position with a new expiry and a new event window, and a
position that needs a third roll has produced evidence that the thesis is wrong. The cap is a
desk rule, not an exchange rule.

| Roll count after this one | Action |
|---|---|
| 1 | Normal; re-arm the take-profit rung at the new strikes |
| 2 | Proceed only with a written thesis update: what changed, and why the new strikes are right |
| 3 | Do not roll. Close the structure. A third roll is an exit you are avoiding |

### The hidden-add test

Ask one question before submitting a roll-up: **does the net contract count increase?**

| Change | Meaning |
|---|---|
| Same strikes count, same quantities, higher strikes | A genuine roll |
| Same strikes count, LARGER quantities | A size increase wearing a roll's name — R8 |
| Fewer units rolled than held, remainder untouched | A partial roll — legal only if the resulting two positions are each defined-risk and each has its own plan |
| Roll plus an added wing | A construction, not a roll — route to `advanced-options-structures` if it is new, or treat it as a separate deliberate decision |

## Vertical downgrade mechanics

### The exact package and its sign discipline

For a fly `+1× K1 / −2× K2 / +1× K3`:

```text
  package: { sell 1x K3  ;  buy 1x K2 }
  result : +1 x K1  /  -1 x K2        (debit call spread, defined risk)
```

The body must be **bought back**, not left short. The single most common execution error is to
sell the wing on its own first — an uncovered-short state (see
`(references/no-naked-risk-guardrails.md)`, Test 2).

### Basis re-derivation

The downgraded vertical's basis is not the fly's basis, and the vertical's width is not the fly's
width. Recompute both from the actual fills:

```text
  vertical basis  = fly entry debit + package net debit      (per unit)
  vertical width  = |K2 - K1| x multiplier
  break-even      = K1 + basis-per-share
  max profit      = width - basis
```

Worked: fly debit `$135`, package debit `$170` → basis `$305`; width `$500`; break-even
`95 + 3.05 = $98.05`; max profit `500 − 305 = $195 per unit` `[COMPUTED]` from `[ESTIMATED]`
inputs. If the package filled at a worse price than drafted, the basis moves and the take-profit
rung must move with it.

### When the downgrade is the wrong call

| Situation | Why the downgrade loses | Do instead |
|---|---|---|
| The far wing is cheap and the fly still has time | You are removing the tail that pays for the body's decay | Hold, or scale out whole units |
| IV percentile is low and rising | The wing's value is depressed by low implied vol; selling it now sells the volatility at its cheapest | Wait for the spike, then monetize |
| The body's strike is above spot and the structure is a "reverse" fly | The shape's profit zone is elsewhere; a downgrade can leave a spread that needs a move you do not expect | Re-derive the geometry first |
| Only one unit of a multi-unit fly is affected | Downgrading one unit leaves two structures with two plans — legal but it doubles the bookkeeping | Downgrade whole units only, and give each remaining unit its own rung |

## Downgrade versus house-money conversion

These two are frequently confused because both remove legs from a fly.

| | Downgrade (`VD`) | House-money conversion (`HM`) |
|---|---|---|
| Legs removed | Far wing `K3`, and one body contract `K2` | Both body contracts `K2`, and the far wing `K3` |
| Legs kept | `+1 K1 / −1 K2` (still short a call) | `+1 K1` only (long-only) |
| Assignment surface | Still present on `K2` | Zero |
| Cost | A debit of roughly `K2 − K3` | A debit of roughly `2 × K2 − K3`, materially larger |
| Use when | You want to keep an elevated but no longer extreme view, with less theta drag | You want the position's risk to be the premium already paid, or an event is imminent |

If the question is "should I still be short anything here?", the answer selects the operation.

## Sources and provenance

- `[VERIFIED]` A listed option is separately exercisable and a multi-leg position is not one
  instrument to the exchange: OCC standard options disclosure document, US options exchange rules.
- `[VERIFIED]` US options exchanges provide complex/package order types at a single net price:
  CBOE and other US options exchange rulebooks. Named order-type labels differ by venue.
- `[COMPUTED]` All arithmetic above follows deterministically from the stated inputs; the worked
  numbers live in `(references/leg-arithmetic-worked-examples.md)`.
- `[ESTIMATED]` Gate thresholds (`DTE ≥ 5` for a roll-up, `≥ 30%` wing value, `≤ 7` DTE, the
  two-roll cap) are data-backed desk thresholds derived from data on this desk's own study. They
  are approximate, are not exchange rules, and are not a guarantee.
- `[BROKER-VERIFIED]` Nothing in this file depends on a specific broker's behaviour, but the
  order types available to you do. Verify complex-order support on the venue you route to.
