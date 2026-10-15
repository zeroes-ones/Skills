# Action Router Decision Matrix

Eight actions. For each: the trigger, the precondition, the forbidden version, the owner of the numbers, and the failure mode. The router picks exactly one per review; the rest are queued in writing.

**This skill owns the DECISION, the ORDER and the PRECEDENCE. It never owns a number.** Every numeric field below names the skill that supplies it.

## The priority order

Resolve top-down and stop at the first rung whose trigger fires. This order is not a preference; it is what makes two operators reach the same answer on the same position.

| Rung | Action | Fires when |
|---|---|---|
| 1 | **CLOSE / reduce only** | A forced action or desk breaker is live |
| 2 | **CUT** (or CLOSE) | The invalidation level is breached, or the thesis is broken |
| 3 | **ROTATE** | Capital is needed elsewhere, or a computed better idea wins after tax and costs |
| 4 | **HEDGE** | Thesis intact, the tax clock argues against realizing, a defined structure exists |
| 5 | **TRIM** | Level intact, plan rung hit |
| 6 | **ADD / PYRAMID** | Level intact, winner above rung 1, fresh level test, thesis re-underwritten |
| 7 | **AVERAGE DOWN** | Level intact, loser below entry, all five gate clauses pass |
| 8 | **HOLD** | Nothing above fired |

Rung 1 is not an action, it is a permission-to-reduce: when a margin call is outstanding the firm must liquidate above a $1,000 deficiency and need give no advance notice [VERIFIED — 12 CFR 220.4(d)], so the only choice left is who executes.

## Action 1 — HOLD (+ tighten)

- **Trigger:** the thesis is intact at the level, no hot clock is live, the position is inside its band, and it is not at a rung.
- **Precondition:** a written level, a written target, a written improve-by date and an event list. All four.
- **Forbidden version:** "HOLD" as a synonym for "I have not decided". A hold with no date and no level is not an action in this router; it is a deferral, and the review is incomplete.
- **Numbers owner:** none at the moment of the hold — but the *next* review needs `equity-risk-and-capital-engineer` for the level context and the event calendar.
- **Failure mode:** the hold becomes permanent. Countermeasure: every third consecutive HOLD on the same position forces a written re-underwrite.

## Action 2 — ADD / pyramid a WINNER

- **Trigger:** the position is above trim rung 1, price is testing a fresh level, and the thesis has survived the move up.
- **Precondition — all five, in writing:**
  1. Already above rung 1 (it is a winner, not a hope).
  2. A **fresh level test** — an add on the way up at a level that means something.
  3. The thesis **re-underwritten in writing** at the higher price. "It keeps going up" is not a thesis.
  4. **Blended cost and blended break-even recomputed.**
  5. The **enlarged position still inside the per-idea band**.
- **Forbidden version:** the add whose size is chosen by conviction, or the add that pushes a full position over its band. An add is not permitted to be the moment a position becomes oversized.
- **Numbers owner:** the pyramid gate belongs to `algorithmic-trader` — its published gate requires the position to be a confirmed winner (gain above 5% of entry), volume confirmation on the add, the add on a pullback to support rather than at highs, trend structure intact, the add no larger than 50% of the original size, one add per position, and the blended stop after the add tighter than the original [VERIFIED — `algorithmic-trader` SKILL.md R13]. The **total position never above 10% of NAV** is a separate portfolio constraint, published in `algorithmic-trader/references/core-workflow.md` ("Max single position: 10% of NAV (absolute hard cap)"), not in R13 [VERIFIED — `algorithmic-trader/references/core-workflow.md`]. Size comes from `portfolio-signal-manager`.
- **Failure mode:** adding at highs because the last add worked. Countermeasure: the fresh level test is a precondition, not a bonus.

Detail and worked arithmetic: `(references/add-and-pyramid-gate.md)`.

## Action 3 — AVERAGE DOWN (the honest form)

- **Trigger:** the position is below entry, the level is intact, and someone proposes buying more.
- **Precondition — the five-clause gate:**
  1. The thesis is **re-underwritten to the lower price**, not merely restated because the price is lower.
  2. The **blended basis and blended break-even are recomputed and written down.**
  3. The total position after the add is **still inside the per-idea band**.
  4. A **written invalidation level for the enlarged position.**
  5. The add count is **under a stated maximum.**
- **Forbidden version:** any add to a position whose level is already breached, and any "just one more tranche" beyond the maximum. Equities have **no defined-risk restructure** — the options escape hatch of converting to a bounded structure does not exist here, so the gate is the only thing standing between an average-down and an unmanaged concentrated loss.
- **Numbers owner:** blended basis arithmetic and the band test are `portfolio-signal-manager`; the tax consequence of the new lot is `equity-tax-lot-and-exit-management`.
- **Failure mode:** averaging down converts a small loss into a large one in exactly the cases where the thesis broke.

Detail: `(references/average-down-honest-form.md)`.

## Action 4 — TRIM / scale out

- **Trigger:** the position reaches a plan rung with the level intact.
- **Precondition:** a ladder defined before the position reached the rung, and a rule for what remains.
- **Forbidden version:** a fractional trim of a position sized so that thirds are not whole shares; and the "trim" that leaves the remainder with no rule at all.
- **Numbers owner:** the **lot choice** belongs to `equity-tax-lot-and-exit-management`. This skill names the interaction and refuses to pick the lot — whole-share ladders and lot selection are different decisions and confusing them is how a good trim produces a bad tax year.
- **Failure mode:** the trim happens but the runner is unmanaged and gives everything back.

Detail: `(references/trim-and-scale-out-ladder.md)`.

## Action 5 — CUT

- **Trigger:** a **breached invalidation level** or a **broken thesis**. Never a P&L percentage.
- **Precondition:** a level that was written before the position was opened. If none exists, the position fails step 2 of the health check, is frozen, and the level is written before any cut is considered.
- **Forbidden version:** "I'll cut it if it gets back to my entry", which is not a cut rule; and the percentage stop, which has no anchor because the basis moves.
- **Numbers owner:** execution mechanics (gap behaviour, the first 30 minutes of regular hours) are desk practice [COMMON-PRACTICE]; the loss arithmetic is `trade-sizing-recovery`-style band arithmetic supplied by the sizing owner.
- **Failure mode:** the level is restated lower each time the price falls. Countermeasure: the level is versioned, and a change needs a written reason and a new grading date.

Detail: `(references/cut-and-rotation-decision.md)`.

## Action 6 — ROTATE

- **Trigger:** the capital is needed elsewhere, or a computed better idea wins after tax and costs.
- **Precondition:** the **friction is computed in dollars** — realized gain or loss times the applicable rate, plus commission and spread — and the new idea's edge is sized by the sizing owner. A rotation is a **CUT plus a sized ADD**, executed in that order; holding both "temporarily" is not a rotation.
- **Forbidden version:** rotating because a name is exciting, without computing the friction; and rotating out of a winner to buy a loser, which is disposition selection by the sign of the P&L.
- **Numbers owner:** tax and friction from `equity-tax-lot-and-exit-management` and `equity-risk-and-capital-engineer`; the new size from `portfolio-signal-manager`.
- **Failure mode:** rotation is never considered at all, because "it might come back" never expires — unlike a position, an excuse has no clock.
- **Why it is first-class:** rotation is the only action here with **no options analogue**. An option position resolves at expiry; an equity position that is never rotated simply occupies capital forever.

Detail: `(references/cut-and-rotation-decision.md)`.

## Action 7 — HEDGE

- **Trigger:** the thesis is intact, the tax clock argues against realizing now, and a defined structure exists.
- **Precondition:** the decision is made at the level of **whether to hedge**, the granularity is understood (100 shares per contract, so a 300-share position can be at most one-third protected by a single contract), and the tax interaction is flagged to the tax owner before the order is written.
- **Forbidden version:** hedging as a substitute for a decision. A collar on a broken thesis is a broken thesis with a collar.
- **Numbers owner:** the structure is `options-strategist` (non-standard structures: `advanced-options-structures`); the premium and sizing arithmetic is `trade-sizing-recovery`.
- **Failure mode:** the hedge is treated as tax-neutral. It is not assumed to be; the rule is owned elsewhere and is flagged, never guessed.

Detail: `(references/hedging-an-equity-position.md)`.

## Action 8 — CLOSE

- **Trigger:** the thesis is broken and the reason to own the name is gone; or the capital is required; or a forced action leaves no other option.
- **Precondition:** nothing — CLOSE is available at every rung and is the correct answer more often than holders admit.
- **Forbidden version:** CLOSE used as a synonym for CUT when the difference matters. CUT is "the level broke but the name may be re-entered on a new thesis"; CLOSE is "this position is finished".
- **Numbers owner:** `equity-tax-lot-and-exit-management` for the lots, `equity-risk-and-capital-engineer` for what the account looks like after.
- **Failure mode:** closing a winner to pay for a loss. That is the same disposition error as rung 6, one step further along.

Detail: `(references/close-versus-hold.md)`.

## Numbers-owner map

| Number | Owner |
|---|---|
| Which lot a trim or sale touches; harvest sizing; holding-period arithmetic; wash-sale measurement | `equity-tax-lot-and-exit-management` |
| Margin, borrow, recall, concentration, liquidity, the event calendar | `equity-risk-and-capital-engineer` |
| Per-idea band, sector cap, position size, correlation | `portfolio-signal-manager` |
| The pyramid gate for adding to a winner | `algorithmic-trader` |
| The original thesis and the level itself | `fundamental-analyst` / `technical-signals-engineer` |
| Hedge structure and strikes | `options-strategist`, `advanced-options-structures` |

A router record with an unowned number is an incomplete record, and an incomplete record leaves the position flagged unmanaged.

## Failure modes of the router itself

1. **Two actions executed.** Countermeasure: one winner, the rest queued.
2. **The router applied to conviction rather than to triggers.** Countermeasure: each rung's trigger is a fact, not a feeling.
3. **Rung 1 skipped because the position "is not that bad".** The forced rung is not subject to opinion.
4. **Rung 3 never reached because no better idea was ever written down.** Countermeasure: the rotation question is asked on the cadence and "nothing better" is recorded as an answer with a date.
5. **Rung 7 used as a way to avoid rung 2.** A failed gate is answered by CUT, not by waiting.
6. **The queued losers forgotten.** Countermeasure: the queue is re-read at the next review before any new action is chosen.
