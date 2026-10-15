# Pin Risk and the Assignment Guard

Expiry week is the only part of an option's life when a leg operation can be forced on you. This
file is the guard: what pin risk actually is, why an assignment is a new position rather than a
late payment, the early-exercise surface that exists **before** expiry day, and the fallback
ladder for when you cannot close.

## Why a short ITM leg near expiry is a new position, not an exit

`[VERIFIED]` Exercise of a physically settled option results in a position in the underlying —
stock — at the strike price, plus the cash to pay for it (call) or the stock to deliver (put).
The option contract is gone; what remains is a stock position with:

| New exposure | Why it is new, not old |
|---|---|
| Overnight and weekend gap risk | The option's loss was bounded by its strike arithmetic at expiry; a stock position's loss is bounded by zero |
| A new margin requirement | Stock margin is computed on the settlement value of the shares, not on the option's requirement |
| A new capital charge | The shares consume buying power the option did not |
| A new decision | Whether to hold, hedge, or liquidate the shares — a decision that did not exist before the assignment |
| Dividend and corporate-action exposure | Share ownership carries entitlements and obligations the option did not |

The practical consequence: an assignment is a **structure change performed by the exchange
without your consent**. Ground Rule R5 exists because the desk's experience is that this is the
single most common way a carefully sized options position becomes an unsized equity position.

## What pin risk actually is

Pin risk is the risk that an at-the-money short leg's exercise outcome is **uncertain** at the
moment you can no longer do anything about it. The uncertainty itself is the risk, not the
direction.

| Situation at the close of expiry day | What is unknown |
|---|---|
| Short strike 0.05% OTM | Whether the clearing house will treat it as ITM at the settlement print |
| Short strike exactly ATM | Whether it will be exercised; either outcome is plausible |
| Short strike slightly ITM | Almost certainly exercised — but "almost" is not "certainly", and the stock gap is what remains |
| Short strike deep ITM | Exercised; the question is the size and quality of the resulting stock position |

`[VERIFIED]` A short option that finishes in the money is normally exercised **unless the holder
files a contrary instruction** with the clearing member — the OCC's exercise-by-exception
process. The exact cut-off time for that instruction is set by the clearing member and is later
than the market close; it is not a fixed universal clock. `[BROKER-VERIFIED]` Verify your broker's
cut-off before relying on any specific time.

### The desk's 15:45 ET working deadline

The desk acts by **15:45 ET on expiry day**. The reasoning is mechanical, not superstitious:

```text
  before the close  →  a two-sided market still exists; the close is achievable
  after the close   →  the only remaining tools are the contrary instruction
                        (broker cut-off, later and broker-specific) and the
                        fallback ladder below
```

`[COMMON-PRACTICE]` 15:45 ET is the desk's working rule, derived from data on when closes
actually fill. It is deliberately earlier than any cut-off you may read about, because the
failure mode it prevents (no fill, no contrary instruction, surprise assignment) is expensive
and the failure mode it creates (closing a leg that would have expired worthless, losing a few
cents) is cheap.

## Early exercise exists before expiry day

This is the trap that catches traders who guard only on expiry Friday.

`[VERIFIED]` An American-style option may be exercised on any business day before expiry. A
short call therefore carries early-assignment risk whenever the economic incentive exists — the
canonical case being the day before an ex-dividend date, when the dividend the holder will
receive by exercising exceeds the option's remaining extrinsic value.

| Question | Why it decides the outcome |
|---|---|
| Is this product American- or European-style? | Only American-style carries early exercise. Do not infer it — verify the product specification |
| Is there an ex-dividend date inside the remaining life? | This is the trigger date, not the expiry date |
| What is the dividend per share, and what is the option's remaining extrinsic value? | If dividend > remaining extrinsic, the holder has an economic incentive to exercise |
| Is the short already ITM? | Early exercise is only rational on an ITM option |
| How many short contracts, and can the resulting stock position be funded? | The assignment is the outcome; sizing the outcome is the preparation |

```text
  ex-dividend risk screen, run every session on every short call:

     for each short call leg:
         if style == AMERICAN and ITM and ex_div_date <= expiry:
             compute remaining_extrinsic = option_mid - intrinsic
             if dividend_per_share > remaining_extrinsic:
                 FLAG: early-assignment window open
                 action: close or roll the short before the ex-dividend date,
                         or pre-accept the assignment with the stock sized
```

## The fallback ladder when you cannot close

| Step | Action | What it buys you |
|---|---|---|
| 1 | Re-price the close once toward the natural; a wider limit still beats an assignment if the assignment outcome is unwanted | A fill at a known cost instead of an unknown state |
| 2 | Buy underlying-equivalent protection (for a short call, shares or a further long call) so the exposure becomes a **known** position | Converts pin risk into a defined payoff |
| 3 | Exercise the matching long wing, if the structure holds one and it is American-style and sufficiently ITM, so the assignment is paired | A wash instead of a naked stock leg |
| 4 | File the contrary instruction where the broker supports it and the economics say do-not-exercise | Avoids an assignment you do not want, when the option is marginal |
| 5 | Pre-accept the assignment in writing: the resulting stock position, its cost basis, its funding, and its first decision | Removes the surprise; the assignment becomes a planned structure change |

`[BROKER-VERIFIED]` Steps 3–5 depend on broker capabilities and product specification. Step 4 in
particular is broker- and product-specific: not all products and not all members support a
contrary instruction the same way, and the cut-off differs. Verify before the expiry session, not
during it.

## Post-assignment triage, the same day

An assignment changes the book without an order. Triage it before the next leg decision.

| Step | Action | Output |
|---|---|---|
| 1 | Read the actual resulting position: shares, price, cash movement, any residual option legs | The new leg list |
| 2 | Re-run the R1 test (see `(references/no-naked-risk-guardrails.md)`) | A pass/fail on coverage |
| 3 | Re-band the position: cost basis, capital charge, maximum loss, first decision | A row in the capital plan |
| 4 | Decide: hold, close, or re-establish as a covered structure | One of three, explicitly, with a reason |
| 5 | Log it in `assignment_events` with a timestamp, cost and disposition | The ledger stays continuous |

Doing nothing is a valid step-4 outcome **only after** steps 1–3 have run. An untriaged
assignment is capital and risk sitting outside the plan.

## Failure modes this guard exists to prevent

1. **What goes wrong — eating the pin.** The short finishes marginally ITM, is exercised, and
   the stock gaps over the weekend. The option loss was capped; the stock loss was not.
2. **What goes wrong — the ex-dividend surprise.** A short call is assigned three days before
   expiry because the dividend exceeded the remaining extrinsic value. No guard was scheduled
   because the calendar only showed expiry Friday.
3. **Worst case — the unfundable assignment.** The short is deep ITM on an expensive underlying;
   assignment requires cash or margin the account does not have, forcing a liquidation at an
   uncontrolled price.
4. **Edge case — the partial-assignment.** Only some of the short contracts are exercised,
   leaving a smaller short plus a stock position — a structure nobody planned.
5. **What goes wrong — the closing-cost fallacy.** A leg worth `$0.02` is left alone to save the
   commission, without evaluating the assignment outcome. The commission saved is trivial
   against the stock position's gap risk.
6. **Known limitation — the settlement print.** For OCC exercise-by-exception, the classification
   depends on the settlement value, which is not knowable in advance. Any guard that assumes
   certainty about a marginal strike is over-claiming.
7. **Edge case — the halted underlying.** No closing market exists; the ladder is the only tool
   left, and it starts at step 2 or 3.

## Sources, provenance and limits

- `[VERIFIED]` Assignment of a physically settled option results in a position in the underlying:
  OCC standard options disclosure document, "Characteristics and Risks of Standardized Options",
  and US options exchange rules on exercise and assignment.
- `[VERIFIED]` In-the-money expiring options are exercised automatically unless a contrary
  instruction is filed; that process is the OCC's exercise-by-exception — OCC clearing
  documentation.
- `[VERIFIED]` American-style options may be exercised on any business day before expiry, so
  early-assignment risk exists around ex-dividend dates when the dividend exceeds remaining
  extrinsic value.
- `[BROKER-VERIFIED]` Contrary-instruction cut-offs, supported instruction methods and the timing
  of assignment notices are broker- and member-specific. Verify against your broker's current
  exercise/assignment documentation before an expiry session; the 15:45 ET figure used here is the
  desk's own early working deadline, not a published cut-off.
- `[COMMON-PRACTICE]` The fallback ladder and the same-day triage sequence are desk conventions.
- `[COMPUTED]` Any arithmetic in this file follows deterministically from stated inputs; worked
  numbers are in `(references/leg-arithmetic-worked-examples.md)`.
- Uncertainty: this is a general framework, **not a guarantee**, and it is approximate for
  marginal strikes. Past performance of the guard does not predict its next result. Verify
  product style, settlement and broker behaviour against current documentation — nothing in this
  file substitutes for your broker's rules.
