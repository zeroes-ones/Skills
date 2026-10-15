# Calendar Roll Windows

A calendar (or diagonal) holds a short front leg against a long back leg. The front leg is the
part that carries pin risk and gamma; the back leg is the part that carries the thesis. Rolling is
therefore a question about the **front leg's remaining life**, not about the position's mood.

## The window

```text
   front-leg DTE
       |
   > 10 |  too early: rolling pays two spreads to remove risk that is
        |            not yet being carried; the front leg still has theta to give
        |
   6-10 |  watch window: mark the roll cost each session, do not act
        |
   <= 5 |  ACTION WINDOW: roll the whole structure as one package, or close.
        |            The front leg's remaining theta is small, its gamma and
        |            assignment surface are not
        |
   <= 2 |  GUARD: the pin guard takes priority over any roll
        |
     0  |  act by 15:45 ET on expiry day; a roll is no longer the operation --
        |  closing the front leg (or letting a deep-OTM front expire) is
```

`[COMMON-PRACTICE]` The DTE ≤ 5 action window and the ≤ 2 DTE guard are data-backed desk
thresholds derived from data on this desk's study. They are approximate, are not exchange rules,
and must be re-derived on your own book.

## The cost cap

A roll is only worth doing if it is cheap relative to what it removes. The desk's working cap:

```text
  roll cost cap:  net package cost <= ~50% of the calendar's current mark

  worked example:   current mark $2.20 per unit
                    cap = 0.50 x 2.20 = $1.10                          [COMPUTED]
                    package costs $0.95  ->  0.95 <= 1.10  -> ROLL    [COMPUTED]
                    package costs $1.25  ->  1.25 >  1.10  -> CLOSE   [COMPUTED]
```

The cap exists because a roll above it is a debit-funded extension of a losing position — the
same economic event as an add, wearing a roll's name (Ground Rule R8). R8 admits an add only as a
*defined-risk restructure* that passes the written five-clause gate `options-position-lifecycle`
owns and `trade-sizing-recovery` sizes — and that gate's own cost clause is the same
half-of-mark budget used here, so a roll above this cap will normally fail it as well. If the roll
is above the cap and the thesis is intact, the honest alternatives are: close now, route the
proposal through that gate and let it decide, or accept that you are opening a new position and
size it as one.

## Gates that must all pass before the roll ticket

| Gate | Test | Reject if |
|---|---|---|
| Window | Front-leg DTE ≤ 5 | DTE > 5 — the roll removes risk that is not yet being carried |
| Cost | Net package cost ≤ ~50% of the current mark | Exceeds the cap — close instead |
| Thesis | The original reason for the structure is still true | The thesis has changed — this is a new position, not a roll |
| Term structure | The back month is not trading at a structurally worse implied vol than the front for the same right | The roll is buying a worse volatility exposure as well as a later date |
| Liquidity | Both the closing and the opening legs have a market you can transact at | The far month is thin — the "roll" is a donation to the spread |
| Events | The new front leg's life is event-clean, or the event is deliberate | A known event lands inside the new front leg and was not intended |
| Size | Net contract count is unchanged | Count increased — R8 |

## Why the term structure gate matters

A calendar's edge comes from the front leg's faster decay relative to the back leg's. A roll that
moves into a term structure where the front month is no longer the faster-decaying one has bought
a later date and sold the edge.

| Term structure at the roll moment | What the roll does |
|---|---|
| Front IV > back IV for the same right (normal contango of decay) | The roll preserves the structure's rationale |
| Front IV ≈ back IV | Neutral: the roll is a date extension with no vol edge; acceptable only if the thesis needs the time |
| Front IV < back IV | The roll buys a *more expensive* long leg and a *cheaper* short leg — the calendar's decay edge is inverted. Reject the roll |

`[COMMON-PRACTICE]` This test is stated as a shape, not a numeric threshold, because the crossing
point depends on the product, the strike and the horizon. Compare like with like: same right,
same strike where possible, adjacent expiries.

## What a "roll" that is really a new position looks like

| Symptom | Diagnosis |
|---|---|
| The new strikes are different from the old ones | Not a roll — a new structure. Roll means same strikes, later expiry |
| The new structure has more legs than the old one | A construction. Route to the structure-building skills |
| The roll changes the position's direction or net delta materially | A new trade; write a new thesis |
| The roll's cost exceeds the cap and is funded from general cash | An add (R8) |
| The old front leg is left open alongside the new one | Not a roll at all — you now hold two front legs |

## The package, exactly

```text
  calendar roll, one unit, ONE order at one net price:

     buy  1 x <front>   (close the short front leg)
     sell 1 x <back>    (close the long back leg)
     sell 1 x <new front>
     buy  1 x <new back>

  resulting leg list: -1 x <new front> / +1 x <new back>
  -> defined-risk calendar, same shape, later expiry
```

If the venue cannot take a four-leg complex order, the sequencing rule applies and it is not
obvious here: a calendar's short front leg is covered by the long back leg. Closing the **back**
leg first leaves a naked short front — forbidden. Closing the front leg first leaves a long-only
back leg, which is defined-risk. So the safe split order for a calendar roll is
**front legs first, back legs after** — the opposite of the rule for a fly, because the calendar's
protecting leg is the long. Derive the sequencing from the coverage map every time; do not carry
a remembered order from another structure.

## Post-roll housekeeping

| Item | Action |
|---|---|
| Basis | Re-derive from the actual fill, not the plan |
| Take-profit rung | Re-arm against the new front leg's life, not the old one |
| Guard queue | Register the new front leg's DTE and its ≤ 2 DTE pin-guard date |
| Ledger | One row, tag `CR`, with net cost, the new strikes, and the counterfactual close price |
| Roll cap | Count it. A position on its third roll is an exit you are avoiding |

## Anti-patterns

| ❌ | Why | ✅ |
|---|---|---|
| ❌ Rolling above the ~50% cost cap "because the thesis is intact" | The cost is the evidence the thesis is being paid for twice | ✅ Close, or re-underwrite it as a new position at a size you would open today |
| ❌ Rolling with different strikes and calling it a roll | The strikes ARE the structure | ✅ Same strikes, later expiry; otherwise it is a new trade with a new ledger row |
| ❌ Rolling while the front leg's DTE is above the window | Pays to remove risk that is not yet being carried | ✅ Wait for the window; mark the cost each session |
| ❌ Rolling a calendar whose front leg is inside the pin-guard band | The guard takes priority: close or guard the front leg first | ✅ Guard, then decide about the roll |
| ❌ Closing the long back leg first when splitting a rejected package | Leaves a naked short front leg | ✅ Front legs first for a calendar; derive the order from the coverage map |

## Sources, provenance and limits

- `[VERIFIED]` A listed option is separately exercisable and a multi-leg position is not one
  instrument to the exchange: OCC standard options disclosure document, US options exchange rules.
- `[VERIFIED]` US options exchanges provide complex/package order types at a single net price:
  CBOE and other US options exchange rulebooks. Four-leg support is venue-specific; verify.
- `[COMPUTED]` The cost-cap arithmetic above follows deterministically from the stated inputs; the
  full worked form is in `(references/leg-arithmetic-worked-examples.md)`, Example I.
- `[ESTIMATED]` The `DTE ≤ 5` window, the `≤ ~50%` cost cap and the DTE bands in the diagram are
  data-backed desk thresholds derived from data on this desk's study. Approximate, not exchange
  rules, not a guarantee.
- `[COMMON-PRACTICE]` The term-structure gate is stated qualitatively by design; do not treat any
  numeric IV comparison as exact without a live quote source you trust.
- Past performance of rolling does not predict the next roll's result, and a roll executed at a
  worse fill than the model assumes changes the arithmetic entirely.
