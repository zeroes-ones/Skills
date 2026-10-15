# Unbalanced-Legacy Repair (tag `UD`)

Some positions arrive already unbalanced: a ticket inherited or imported from another platform, a
partial fill nobody noticed, an old naked short left behind by a closed leg, an odd-lot contract
count that never divided into whole units. Repair is a different discipline from management: the
first order **creates** a defined-risk state, and there is no earlier state to protect.

## Sources of imbalance

| Source | Signature | Immediate risk |
|---|---|---|
| Partial package fill, never completed | Leg count missing one side of a pair; a short with no long | Naked short if the missing leg was a long |
| A leg closed on its own at some point in the past | Ratio is not the shape's canonical ratio | Depends on which leg was closed — could be naked or merely odd |
| Imported ticket from another platform | Strikes/expiries may not map to a named shape at all | Unknown until classified |
| Odd-lot size | Quantities are not integer multiples of the shape's unit ratio | Not naked, but unmanageable by the original plan's rules |
| Corporate action or assignment | A stock position appears; option legs may be partly exercised | Stock leg unbanded; option remainder possibly uncovered |
| Two structures accidentally netted at the broker | The screen shows a single netted position | The leg list must be reconstructed before anything can be tested |

## Triage order — do not reorder this

```text
   1. RECONSTRUCT the true leg list from the broker's records (not from memory,
      not from a netted summary)
        │
        ▼
   2. CLASSIFY the shape:
        ├── a named defined-risk shape with an odd multiple  ──▶ odd-lot repair
        ├── a named shape with a leg missing                  ──▶ ratio repair
        └── nothing recognizable                             ──▶ treat as
                                                                 independent legs
        │
        ▼
   3. RUN THE R1 TEST on the reconstructed list
        │
        ├── FAIL (uncovered shorts exist) ──▶ define risk FIRST, in one order
        └── PASS ──▶ decide whether to keep, reduce, or close
        │
        ▼
   4. RE-BAND into the capital plan: basis, max loss, first decision
        │
        ▼
   5. LEDGER ROW with tag UD, then (and only then) manage it like any other
      position
```

Step 1 must come before step 3. The R1 test run on a wrong leg list is worse than no test, because
it produces a false pass.

## Repair 1 — the naked short

The only repair that is urgent. The goal is to make the exposure bounded in the **first** order,
not in a sequence.

| Situation | First order | Result |
|---|---|---|
| Naked short call, account holds no shares | Buy back the short contracts, OR buy a long call at a higher strike equal in quantity | Flat, or a defined credit vertical |
| Naked short put, cash is available | Buy a long put at a lower strike, equal quantity | A defined put credit vertical |
| Naked short put, cash is not available | Buy back the short contracts | Flat |
| Naked short of a size that cannot be closed at any price | Buy underlying-equivalent protection (shares for a call; cash-secured exposure for a put) | A known, bounded payoff |

The repair order is **one package**. Do not "work into" a defined shape with a leg-by-leg
sequence unless the sequence's intermediate states are each defined-risk — and for a naked short,
the intermediate state of "close half of it" is a smaller naked short, which is still the forbidden
state. Buy back the whole short, or cover the whole short.

```text
  naked short:  -2 x 100C
  repair A:     buy 2 x 100C                          -> flat
  repair B:     buy 2 x 105C  (2 units of a 100/105) -> -2 x 100C / +2 x 105C
                                                        defined credit vertical
  NOT a repair: buy 1 x 105C  -> -2 x 100C / +1 x 105C, one short still uncovered
```

## Repair 2 — the non-integer ratio

A structure whose quantities are not in whole-unit multiples is not "a smaller position"; it is a
shape the original plan cannot manage, because the plan's take-profit and stop levels assume the
canonical ratio.

```text
  canonical fly unit:  +1 x K1 / -2 x K2 / +1 x K3
  legacy mismatch:     +1 x K1 / -1 x K2 / +1 x K3     (one body closed long ago)

  options:
    A. restore the ratio:  { sell 1x K2' }  -- but this SELLS a body, adding a short
         -> check R1: after the sale, shorts = 2, covers = 2 (K1, K3)  PASS
         -> legal, but it re-creates assignment surface you may not want
    B. reduce to a smaller legal shape: close the wing(s) to leave a spread, or
         close the body to leave a long strangle -- choose the shape you would
         open today, not the one you happen to hold
    C. close the whole position as one package

  NOT an option: partially closing legs to "even things up" without naming the
  resulting shape
```

The decision between A, B and C is a real decision and must be made explicitly, with the
resulting shape named. "Repair" never means "make the numbers look tidy".

## Repair 3 — the odd-lot

An odd-lot multiple (for example 3 units of a 2-lot structure) is not a risk problem, it is a
manageability problem. The fix is process, not structure:

| Item | Action |
|---|---|
| Unit count | State it explicitly; scale-outs are whole units, so an odd count is fine as long as it is known |
| Take-profit rungs | Define in units, not in "half" |
| Ledger | One row per unit if the units will be managed differently; otherwise a unit count and one plan |
| Guard queue | Every short leg in every unit gets a pin-guard date |

## Repair 4 — the netted or partially-exercised position

A partial assignment (some short contracts exercised, others not) leaves a smaller short plus a
stock position. Reconstruct, then decide:

```text
  example after a partial exercise of 2 short calls of 5:
      shares: +200 x <strike>
      remaining: -3 x <short strike>C   (uncovered unless a long exists)

  step 1: R1 test on the remaining shorts
  step 2: re-band the shares as their own position (basis, capital, first decision)
  step 3: repair or close the option remainder -- but never by selling the shares
          "to pay for" the option leg; those are two positions with two plans
```

## The legacy-repair ledger row

| Field | Value |
|---|---|
| Tag | `UD` |
| Trigger | "position arrived with a non-integer ratio / an uncovered short / an unrecognized shape" |
| Resulting leg list | Written out, with the R1 test result |
| Reason for the chosen repair | A / B / C from the options above, stated |
| Cost | The repair's net debit or credit in dollars `[COMPUTED]` from named inputs |
| New plan | Basis, invalidation, take-profit rung, guard date |
| Counterfactual | The close-the-whole-position price at the repair's timestamp |

## Anti-patterns

| ❌ | Why | ✅ |
|---|---|---|
| ❌ Running the R1 test on a remembered or netted leg list | A false pass is worse than no test | ✅ Reconstruct from the broker's records first |
| ❌ Repairing a naked short by covering half of it | Half a naked short is a naked short | ✅ One package: cover or close the whole short |
| ❌ "Evening up" legs without naming the resulting shape | You cannot manage a shape you have not named, and you cannot test it for defined risk | ✅ Choose the shape you would open today; name it in the ledger |
| ❌ Treating an odd-lot as a structural defect | It is a manageability issue, and forcing it to a whole number can create unwanted shorts | ✅ Count units, define rungs in units, register every guard date |
| ❌ Selling shares to fund an option repair | Two positions, two plans | ✅ Repair the option side on the option side's merits |
| ❌ Managing a legacy position by its original (unknown) plan | The plan's levels assume a shape you do not hold | ✅ Write a new plan after repair, and re-band it |

## Sources, provenance and limits

- `[VERIFIED]` Assignment of a physically settled option results in a position in the underlying,
  and a listed option is separately exercisable: OCC standard options disclosure document; US
  options exchange rules on exercise and assignment.
- `[VERIFIED]` An uncovered short option carries unbounded (call) or strike-to-zero (put) risk,
  which is why the repair of a naked short is the one urgent operation in this file.
- `[COMPUTED]` Any dollar figures above follow deterministically from stated strike and quantity
  inputs; the worked forms live in `(references/leg-arithmetic-worked-examples.md)`.
- `[COMMON-PRACTICE]` The triage order, the A/B/C repair options and the "name the resulting shape"
  rule are desk conventions, not exchange requirements.
- `[BROKER-VERIFIED]` How a broker records a partial exercise, whether it nets positions, and what
  its records expose are broker-specific. Verify against your broker's statements before
  reconstructing; do not infer the leg list from a summary screen.
- This file is a framework, **not a guarantee**, and is approximate for edge cases such as
  positions netted across structures. Past performance of a repair does not predict the next one.
