# Close versus Hold

CLOSE is the last rung and the simplest action in the router. It is also the one holders avoid longest, because closing makes a loss permanent and makes a decision visible. This file draws the line between CLOSE and the other exits — particularly CUT — and lists the situations in which CLOSE is the correct answer and nothing else is.

**Portability target:** spec-level. Lot selection and the post-trade account state belong to the tax and risk owners.

## CLOSE is not CUT

They look similar from the outside and they are different decisions:

| | CUT | CLOSE |
|---|---|---|
| **Trigger** | A breached invalidation level or a broken thesis, with the name still potentially ownable | The reason to own the name is gone, or the capital is required, or a forced action leaves no alternative |
| **What it leaves behind** | A name that may be re-entered on a new thesis after cooldown | A position that is finished; the name is out of the book |
| **Contract status** | The contract is void; a cooldown and any wash-sale window apply | The contract is resolved; no cooldown is needed to justify the next decision because there is no "next" |
| **Typical follow-up** | Re-entry gate, if a new thesis appears | Nothing, or a rotation sized as a separate decision |

The distinction matters because it changes what happens next. A CUT is followed by a **re-entry gate**; a CLOSE is followed by nothing, and treating a CLOSE as a CUT is how a holder ends up re-buying a name they had already concluded was finished.

## When CLOSE is the answer

### 1. The thesis is broken and the name is not ownable

The invalidation broke, and the re-underwrite that would be required to keep the position produces nothing. Not "the re-underwrite is inconvenient" — nothing. The reason the position existed is gone and no price makes it come back.

This is the most common CLOSE, and it should be reached by the rung-2 test rather than by accumulated frustration. The test is the same one the hold protocol uses: can you restate the thesis in one sentence, at the *current* price, and is it about the business rather than about the chart?

### 2. The capital is required

The money is needed for something else that has already been decided: a better idea that has been sized, a cash need, a margin situation that has to be resolved by reducing rather than by funding.

CLOSE for capital is not a judgement about the position at all, which is exactly why it is easy to postpone and expensive to postpone. The position is not a verdict on the holding; it is a claim on the capital.

### 3. A forced action leaves no alternative

A margin call above a $1,000 deficiency must be satisfied by liquidation unless funded, and **no advance notice is required** [VERIFIED — 12 CFR 220.4(d)]. The Reg T payment window is the settlement cycle plus two business days — three business days under T+1 [VERIFIED — 12 CFR 220.2, 220.4(c)(3)(i)]. At that rung, CLOSE or reduce is the only action the router authorises; the tax calendar is not consulted, because the firm's timetable is not negotiable.

### 4. The position cannot be held at the required size

A position that has become too small to trim, too small to hedge and too small to size is a position that costs more attention than it can earn. Closing it converts a permanent background cost into a single realised number.

### 5. A corporate action delivered a security you would not have bought

A merger, a spin-off or a cash-and-stock election can hand a holder an instrument they never chose: a small-cap spinco, a stub position, a different currency, a different sector. The question is not "do I like the price" but "would I buy this today with cash". If the answer is no, the CLOSE is the answer, and it is best taken deliberately rather than drifted into.

## The comparison CLOSE must pass

CLOSE and HOLD are not the only two options; CLOSE competes with CUT-with-a-plan, TRIM, ROTATE and HEDGE. The comparison is at the router level, and it resolves like this:

```text
Rung 1 forced action?          → CLOSE or reduce; stop here.
Rung 2 level breached?         → CUT; CLOSE if the name is not ownable at any price.
Rung 3 capital needed or a
        computed better idea?  → ROTATE: close here, size there, in that order.
Rung 4 thesis intact, tax
        argues against selling,
        structure exists?      → HEDGE.
Rung 5 rung hit, level intact? → TRIM.
Rung 6 winner, fresh level,
        re-underwrite?         → ADD.
Rung 7 loser, level intact,
        gate passes?           → AVERAGE DOWN (once).
Rung 8 nothing triggered?      → HOLD-WITH-DEADLINE.
                                 CLOSE is never the default; it is a conclusion.
```

That last line is the discipline: **CLOSE is never the default.** A holder who reaches for CLOSE because a position is tiring has skipped the router, and skipping the router is how a position is closed at a level that had not been breached, or kept past the level that had.

## The arithmetic of a close

A close realises a gain or a loss, and both sides of that should be on the page before the order.

**Closing a loser.** A position down 15% on $30,000 is a **$4,500 loss** [COMPUTED]: 30,000 × 0.15 = 4,500. If a broken thesis is allowed to run to −40%, the loss is **$12,000** [COMPUTED]: 30,000 × 0.40 = 12,000 — an additional **$7,500** [COMPUTED]: 12,000 − 4,500 = 7,500. The close is what stops that number from growing while the story is being constructed.

**Closing a winner.** The realised gain's tax depends on which lots leave and on the holding period. The holding period begins the day after the buy trade date and ends on the sale trade date, so the earliest long-term sale is buy date + 1 year + 1 day [VERIFIED — IRC §1222, IRS Pub 550]. The lot instruction is issued to the tax owner as *"close the whole position at price P on date D — choose the lots."*

**Closing at a loss.** This opens a 61-day wash-sale window in the name: 30 days before through 30 days after the sale, with replacement shares inheriting the old holding period [VERIFIED — IRC §1091, §1223(3)]. No purchase in the name, in any account, inside the window — which is the single most common way a carefully harvested loss is wasted.

**Friction.** Round-trip commission and spread is a real cost and belongs in the decision when the close is marginal. A 0.3% band on a liquid large-cap name is a common working assumption [ESTIMATED] — an operating band, not a measured cost; read your own schedule.

## Recording a close

```text
action:            CLOSE
reason_class:      thesis_broken | capital_required | forced_action | unmanageable_size | corporate_action
rung:              <1-3 per the router>
level_state:       <breached | intact | not_applicable>
lots:              equity-tax-lot-and-exit-management — instruction issued: "close whole, price P, date D"
realised:          <gain|loss> <$>  [COMPUTED from basis and lots]
wash_sale_window:  <open until DATE | not opened>   (if a loss was realised)
friction:          <$>   [ESTIMATED from the round-trip band]
capital_released:  <$>   (and re-sized against the actual freed amount, not the assumed one)
expectation:       "the position is out of the book and the capital is available for <named use>"
grade_on:          the next book review
```

## Failure modes

1. **CLOSE as the default for a tiring position.** Countermeasure: the router runs first; CLOSE must be a conclusion reached at rungs 1–3.
2. **Closing a winner to fund a loser.** Countermeasure: dispositions are chosen by the level, never by the sign of the P&L.
3. **Closing at a loss with no wash-sale flag.** Countermeasure: the flag is set before execution and the name is frozen for 61 days in every account.
4. **Treating a CLOSE as a CUT and re-entering.** Countermeasure: the reason class is recorded; a `thesis_broken` close does not generate a re-entry gate because there is nothing to re-enter.
5. **Closing in the opening print after a gap.** Countermeasure: the first 30 minutes of regular hours, or a limit you can defend, with partial fills accepted.
6. **Closing before checking whether the action belonged to rung 3.** A close that was really a rotation leaves the capital idle and the better idea unsized.
7. **CLOSE used to avoid the average-down gate.** A failed gate means CUT, which usually means closing — but the difference in the record matters: `gate_failed` is a finding about the thesis.
8. **The corporate-action stub closed by accident.** A spin-off's stub position is a position; it gets its own review, its own level, and its own decision to close or keep.
9. **Not re-sizing the replacement against actual freed capital.** Commission, spread and tax all reduce the proceeds; a rotation sized on the pre-exit assumption is oversized on arrival.
10. **Skipping the grading record.** A close is the last chance to learn from the position; without the grade, the lesson leaves with the capital.

## Verification

- **Complete when** the reason class is recorded and the rung that produced it is named.
- **Complete when** the router was actually run — CLOSE reached at rungs 1–3, not arrived at by exhaustion.
- **Complete when** the lot instruction to the tax owner names price, size and date.
- **Complete when** the wash-sale window is set or explicitly recorded as not opened.
- **Complete when** the capital released is known and the replacement (if any) is sized against the actual amount.
- **Complete when** the expectation and grading date are written, even though the position no longer exists.
