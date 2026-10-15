# Action Router — Decision Matrix

Eight actions. For each: the **trigger**, the **precondition**, the **forbidden version** (the thing people call by the same name and should not), and the **owner of the numbers** (which skill supplies the arithmetic, because this skill never invents a number).

## The eight actions

| Action | One-line job |
|--------|--------------|
| HOLD | Change nothing, keep the level armed, set the date |
| ADD | Increase a winner's size, inside its band, after a re-underwrite |
| RESTRUCTURE | The only legal form of "average down": a defined-risk roll for a capped debit |
| TRIM | Book profit in whole structure units on a ladder |
| CUT | Leave, by level or by band, into strength |
| ROLL | Buy time, credit-or-flat, at most twice |
| CONVERT | Change the structure into a strictly better one |
| CLOSE | Finish the position because nothing paid for is left |

## Priority order (the rule that makes the router deterministic)

When more than one action qualifies, the highest rung below wins. This is deliberately ordered by **what cannot be recovered later**, not by expected value.

```text
1. Desk circuit breaker ......... CLOSE / reduce only. Everything else defers.
2. Calendar force ................ CLOSE or ROLL inside the window.
3. Thesis broken ................. CUT (or CONVERT if strictly better and defined-risk).
4. Loss band breached ............ CUT; RESTRUCTURE only if the written gate passes.
5. Profit rung hit ............... TRIM whole units.
6. Structure degraded but alive .. CONVERT, or ROLL if credit-or-flat and max loss holds.
7. Nothing triggered ............. HOLD with a date; ADD only on a winner at rung 1+.
```

The order is not a preference. Rolling a position whose thesis broke (rung 3) is how a known loss becomes an unknown one. Trimming a position that should be cut (rung 4) books a small win out of a position you should not own.

---

## HOLD (+ tighten)

**Trigger.** Thesis intact, position inside its band, no event inside the window, structure unchanged.

**Precondition.** A written date and a written level. No date → not a HOLD, it is an omission.

**What "tighten" means.** Not "move the stop closer for comfort". It means: re-arm the review at the level, refresh the liquidity read, and confirm the event list is current. If the level has *not* moved but the position is closer to it in DTE terms, tighten only the cadence.

**Forbidden version.** "Hold and revisit when it feels right." A HOLD without a date and a level is a decision not to decide, and it will be re-examined only when the market forces it — which is the worst possible time.

**Owner of the numbers.** `trade-sizing-recovery` for the band the position is inside; `options-risk-engineer` for the calendar and margin state.

**Escalation.** Two consecutive HOLDs on the same position with no change in state is a signal: the position is consuming attention without earning it. Consider the attention budget explicitly at the third review.

---

## ADD (pyramid a winner only)

**Trigger.** A winner has reached at least rung 1, the underlying is testing a fresh level, and the thesis has been re-underwritten from scratch.

**Precondition — all five.**
1. The structure is at or above rung 1 (never add to a position below its first rung).
2. The underlying is at a *fresh* level test, not the same level it was at when the position was opened.
3. The thesis has been re-underwritten as if it were a new trade, in writing.
4. Blended cost and buying-power impact are recomputed, not estimated.
5. The add leaves the structure **inside its band**. If the resulting max loss breaches the band, the add is refused — no exceptions for conviction.

**Forbidden version.** Adding to a position to "make the average better" — that is average-down wearing an ADD's name, and it is rung 4 or rung 3, never rung 7.

**Owner of the numbers.** Contract count and dollar risk: `trade-sizing-recovery`. Resulting structure and fill sequencing: `options-leg-management`.

**Worked arithmetic.** A debit vertical originally $1.80 ($180). It is marked $3.30 and the trader wants to add one spread at $3.30. Blended cost = ($180 + $330) ÷ 2 = **$255 per spread [COMPUTED]**. That $2.55 is the blended **basis**, not the break-even — a debit vertical breaks even at `long strike + basis`, so the $2.55 has to be added to the strike before it means anything on a chart. New max loss = the debit paid = 2 × $255 = **$510 [COMPUTED: contracts × blended debit × 100]**, against a per-trade band that was previously satisfied by $180. The add must be refused if $510 exceeds the band for this name, regardless of how good the chart looks.

**What changes afterwards.** The new position is a new position: it has a new break-even, a new max loss, and its own rungs. Re-run the health check on it in the same session (see Phase 3, "re-run after any action").

---

## RESTRUCTURE (the only legal average-down)

**Trigger.** Loss band reached, thesis still intact, DTE ≥ 15, and a defined-risk roll can reduce the break-even without increasing max loss beyond the remaining band.

**Precondition.** The five-clause gate in `(average-down-restructure-gate.md)` must pass, in writing, with arithmetic:

1. Level intact on the stated measurement.
2. DTE ≥ 15 (the repair needs a level test to complete).
3. New max loss ≤ remaining band.
4. New break-even reachable within the horizon (DTE left, or a stated extension).
5. Net debit ≤ a stated share of the current mark (typically well under half — see the gate reference for the working rule).

**Forbidden version.** "Rolling out and down for a credit" that widens the loss and moves the strike closer to the money. That is not a restructure; it is a larger bet financed by a small credit.

**Owner of the numbers.** The entire gate: `trade-sizing-recovery`. Leg mechanics: `options-leg-management`.

**Refusal is a valid output.** Most proposals fail the gate. A router that can only say yes is not a router.

---

## TRIM

**Trigger.** Price at or above a take-profit rung.

**Precondition.** The remaining size divides into **whole structure units**. A four-leg condor trimmed by half is not a smaller condor; it is a condor plus a naked structure. If the unit count is 1, TRIM degrades to CLOSE.

**What it looks like.** Ladder 1/3 of units at rung 1, 1/3 at rung 2, runner with a written trailing rule. See `(trim-and-scale-out-ladder.md)`.

**Forbidden version.** "Selling a leg to lock in some profit." Closing one leg of a spread changes the structure — that is a CONVERT at best, and usually a step-2 failure at the next review.

**Owner of the numbers.** Rung levels: `trade-sizing-recovery`. Execution: the venue, with the fill assumptions stated.

---

## CUT

**Trigger.** Loss band breached, or thesis broken, or a calendar force makes the plan unavailable.

**Precondition.** A stated mechanism: into strength, or in the first 30 minutes of RTH. Never into a gap, never at the opening print.

**Forbidden version.** "Cut when it bounces a bit more." A bounce is not a level; if the plan requires a bounce, that is a HOLD-WITH-TP with a date, and it must pass that protocol instead.

**Owner of the numbers.** The band and the disposition matrix: `trade-sizing-recovery`. Margin and pin consequences: `options-risk-engineer`.

**Session rules.** Standard structures: first 30 minutes of RTH. 0DTE: same-session, and the decision must be executed before 15:45 ET. Thin names: expect the fill to be worse than the mark and record the difference as execution cost rather than adjusting the band.

---

## ROLL

**Trigger.** Time is worth more than the current structure, and the thesis is intact. A roll for any other reason is a rescue in disguise.

**Precondition.**
- Credit-or-flat only. A debit roll must pass the RESTRUCTURE gate instead.
- At most **two** rolls per position, counted from the original entry.
- New max loss ≤ remaining band.
- The new expiry's DTE fits the plan that needs to complete.

**Forbidden version.** "Rolling to fix the thesis." If the thesis broke, the action is CUT; a roll buys time for a plan that no longer has a reason.

**Owner of the numbers.** Roll window and calendar: `options-risk-engineer`. Leg mechanics and fill sequencing: `options-leg-management`. Credit/debit and band check: `trade-sizing-recovery`.

**Why the cap matters.** Roll one is a purchase of time. Roll two is a purchase of time with a smaller margin for error. Roll three is a schedule hiding a loss that has been renamed three times.

---

## CONVERT

**Trigger.** The thesis is intact but the structure no longer expresses it well: delta has drifted, a ratio has slipped, the risk/reward has inverted, or a leg is now redundant.

**Precondition.** The conversion produces a structure that is **strictly better on the defined criteria** — max loss, break-even, probability of touching, capital efficiency. "Different" is not a reason.

**Forbidden version.** Converting to hide a loss (for example, selling more premium into a losing spread to "pay for it"). That is an ADD to a loser with extra steps.

**Owner of the numbers.** Mechanics: `options-leg-management`. Resulting risk and margin: `options-risk-engineer`. Sizing of any new leg: `trade-sizing-recovery`.

**Note.** CONVERT is the natural home for what people call "repairing" a position. The repair is allowed; the arithmetic is not optional.

---

## CLOSE

**Trigger.** Any of:
- The remaining value is mostly extrinsic tail you are not paid for.
- The level is broken and the action is not a defined-risk restructure.
- The clock forces it (0–2 DTE, assignment, pin).
- The structure no longer exists as designed (step 2 fail) and rebuilding it is not worth the cost.
- The thesis cannot be restated in one sentence.

**Precondition.** Any TP or SL brackets attached to the structure are cancelled, and any queued actions on the name are cleared.

**Forbidden version.** Closing at the open on a gap, then calling the slippage a strategy outcome. Note the price; grade the action against the fill, not against the mark.

**Owner of the numbers.** Nothing new needs computing — the loss is the loss. What is owed is the **graded record**: expectation, outcome, lesson.

---

## Choosing between near-neighbours

These are the pairs that get confused, and the tie-break for each:

| Pair | Tie-break |
|------|-----------|
| CUT vs RESTRUCTURE | Does the gate pass, with arithmetic, in writing? If it cannot be shown, CUT. |
| HOLD vs HOLD-WITH-TP | A loser needs the full protocol (level, target, improve-by date, events). A winner inside its band merely needs a date. |
| ROLL vs CONVERT | Is the change temporal (same structure, later expiry) or structural (different structure)? Temporal → ROLL. Structural → CONVERT. |
| TRIM vs CLOSE | Do whole units remain after the trim? If not, CLOSE. |
| ADD vs CONVERT | Does the position's risk *increase* in the same shape? ADD. Does the shape change? CONVERT. |
| CUT vs WRITE-OFF | Is there an executable exit at size? If not, the decision is still "leave"; the mechanism becomes write-off. |

## Router output contract

Every routed decision produces these lines, and a decision without them is not routed:

```text
position:      <identifier>
action:        HOLD|ADD|RESTRUCTURE|TRIM|CUT|ROLL|CONVERT|CLOSE
priority_rung: <1-7, the rung that fired>
why:           <one sentence, naming the trigger>
queued:        <actions that qualified but lost, if any>
numbers:       new_max_loss=<...> new_breakeven=<...> credit|debit=<...>  owner=<skill>
mechanism:     <into strength | first 30 min RTH | before 15:45 ET | at the event boundary>
expectation:   <one sentence>
grade_on:      <date>
re-arm_at:     <level that pulls the review forward>
```

## Failure modes of the router itself

1. **Rung 7 becomes the default.** When nothing triggers, HOLD accumulates; a book of unexamined holds is a book of positions nobody decided about. Countermeasure: at the third consecutive HOLD, force a full re-underwrite.
2. **Rung 3 is under-detected.** "Thesis broken" requires a written thesis; positions without one can never reach rung 3. Countermeasure: no exit contract, no position — the freeze rule (R3).
3. **Rung 5 fires too early because rungs were set too tight.** Trimming at the first twitch converts a good trade into a commission generator. Countermeasure: rungs come from `trade-sizing-recovery`, not from nerves.
4. **Rung 4 is bypassed by a "repair" that never runs the gate.** Countermeasure: the gate is arithmetic and must be attached to the decision record.
5. **The queued action is forgotten.** A queued action is a standing state, not a note. Countermeasure: it appears in the record and in the next review's inputs.
6. **Two people route the same position differently in the same session.** Countermeasure: one router output per position per session; later inputs amend it explicitly rather than silently replacing it.
