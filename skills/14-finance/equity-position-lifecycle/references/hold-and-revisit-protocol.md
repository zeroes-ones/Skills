# Hold and Revisit Protocol

The HOLD-WITH-DEADLINE contract is how a losing or stalled equity position is allowed to stay open. It is not a reward for conviction. It is a written agreement that the position has a job to do, a date by which it must do it, and a level below which the agreement is void.

**Portability target:** spec-level. The contract is five fields; the numbers in it come from the tax and risk owners.

## Why a deadline has to be manufactured

An option expires. Nobody has to decide anything for the position to stop existing. An equity position does not: it will sit there for a decade, through every quarter, without ever once demanding an answer. That is the structural difference that makes the equity failure mode **not deciding**, and it is why this protocol exists.

The contract's function is to convert an open-ended position into a dated one. It does this with five fields, and a hold missing any of them is not a hold; it fails step 8 of the health check and counts as unmanaged.

## The five fields

| Field | Rule | What "good" looks like |
|---|---|---|
| **Invalidation level** | A price, written before the contract is granted, versioned | "54.20, set 2026-10-14" — not "around 54" |
| **Target** | A price or a named condition the position is expected to reach | "the position reaches rung 2 at 68.00" |
| **Improve-by date** | A calendar date, no conditions attached | a date, not "next quarter" |
| **Event calendar** | Every dated event before the improve-by date | earnings, ex-dividend, reconstitution, FOMC |
| **Queued actions** | What the router decided against, in writing | the CUT that lost, and why |

## The improve-by date, and the no-renegotiation rule

The improve-by date is a **decision date**, not a review date. At that date the question is binary: **at plan, or cut.** There is no third option, because the third option is the one that turns a two-month hold into a permanent position with a story attached.

**No renegotiation.** If the date moves once it will move every time. The mechanism that makes this enforceable is that the date is written in the contract, the contract is part of the record, and the record is the evidence format in `examples/backtest/README.md`. A moved date is visible; an unmoved story is not.

Two legitimate exceptions, and only two:

1. **A forced action intervened.** A margin call, a recall or a halt changed the position. That is rung 1; the contract is void and a new one is required for whatever the position now is.
2. **A corporate action delivered a different security.** The held instrument changed identity. That is a new position, and new positions get new contracts.

Neither exception is "the market moved", and neither is "I still believe".

## The equity-specific trap: "I'll hold it until it's long-term"

This is the most common pseudo-plan in equity position management, and it fails in a specific, checkable way.

Waiting for the long-term anniversary is a decision about the **tax on a sale you have already decided to make**. It is not a reason to own a position you would otherwise exit. If the position is one you intend to sell, the anniversary changes *when* the sale happens; if the position is one you would not sell at any price, the anniversary is irrelevant.

Two tests make the trap visible:

- **The level test.** Is the invalidation level intact? If not, the anniversary is rung 4 and the level is rung 2. The level wins.
- **The arithmetic test.** Put the rate difference against one standard deviation of the wait.

Worked, on a $33,000 position 20 sessions from the anniversary:

| Item | Value | Formula |
|---|---|---|
| Gain at stake | **$3,000** | 500 sh × ($66.00 − $60.00) = 3,000 [COMPUTED] |
| Rate difference (40.8% vs 23.8%, an assumed pair) | **$510** | 3,000 × (0.408 − 0.238) = 510 [COMPUTED]; the 40.8% / 23.8% pair is [ESTIMATED] — substitute your own bracket — while the statutory rates it derives from are [VERIFIED] — IRC §1(h) and §1411 |
| One-sigma move over 20 sessions | **$2,789** | (33,000 × 0.30 ÷ √252) × √20 = 623.7 × 4.472 = 2,789 [COMPUTED] |
| The tax saving as a share of one sigma | **18%** | 510 ÷ 2,789 = 18.3% [COMPUTED] |

The tax argument is worth 18% of the price risk it requires to capture. That is not a reason to hold; it is a reason to choose the *timing* of a sale you were making anyway.

If a hold for the anniversary is nevertheless granted, it still requires all five fields — including a target and a level. **"I'll hold until it's long-term" is not a plan; with a target and a date it can become one.**

## The re-underwrite gate

A hold that has been running for a while gets re-underwritten before it is extended:

1. **Restate the thesis in one sentence**, at the current price. Not the original sentence with a new date.
2. **Re-verify the level on the current close.**
3. **Re-check the band**: is the position still inside its per-idea cap? A position that grew into oversize while being held has a problem the hold did not address.
4. **Re-read the event calendar** to the new improve-by date.
5. **State the queued actions** that lost, and whether any of them now fires.

A hold that cannot pass the re-underwrite is a hold that has stopped being a plan. The disposition is CUT.

## Cooldown and the re-entry gate

After a cut or a close, the name enters a **cooldown**: a defined period during which re-entry is barred. The cooldown is not punishment; it is the mechanism that prevents the two most expensive post-exit behaviours:

- **Revenge re-entry.** Re-buying the same name at a larger size to recover the loss. This is an unmanaged position created by a managed one.
- **Nostalgia re-entry.** Re-buying because you understand the name, rather than because a thesis exists. Re-entry requires a **new** thesis, a **new** level, a **new** size inside the band, and a **new** date. It is a fresh position in a familiar name, and it carries a fresh position's obligations.

**The wash-sale interaction.** If the cut realised a loss, the name is frozen for 61 days — 30 days before through 30 days after the sale, with replacement shares inheriting the old holding period [VERIFIED — IRC §1091, §1223(3)]. The wash-sale freeze overrides any cooldown that is shorter than it, in **every account**, including retirement accounts.

## The contract template

```text
position:          <ticker> <shares> sh, basis <price>, opened <date>
granted:           <date>
invalidation:      <price>   (version: <date set>)
target:            <price or named condition>
improve_by:        <date>    (binding; no renegotiation)
events:            <event: date> · <event: date>   (to the improve-by date)
tax_flags:         anniversary <date>; wash-sale window <open|closed>; qual-div window <state>
band_state:        <n>% of book, against a <n>% cap   [owner: portfolio-signal-manager]
queued_actions:    <action that lost, and why>
re_arm_at:         <level that pulls the review forward to now>
expectation:       <one falsifiable sentence>
grade_on:          <date>
```

## Failure modes

1. **The undated hold.** A HOLD with no improve-by date is a deferral. Countermeasure: the contract fails step 8 and the position is flagged unmanaged.
2. **The renegotiated date.** Countermeasure: the date is in the record and a change is visible as a defect.
3. **The level that moves.** Countermeasure: the invalidation is versioned; a change requires a written reason and a new grading date.
4. **"Hold until long-term" with no target.** Countermeasure: the arithmetic test, and the requirement that an anniversary hold still carries a target and a date.
5. **The contract granted on a broken thesis.** A hold is never available at rung 2. Countermeasure: the level test precedes the grant.
6. **The event list that stops at the improve-by date.** Countermeasure: everything dated between grant and improve-by is listed.
7. **Re-entry inside the cooldown.** Countermeasure: the cooldown is recorded by name and checked before any new order.
8. **Re-entry inside a wash-sale window.** Countermeasure: the window overrides the cooldown; the check is on the name, in every account.
9. **The re-underwrite that restates rather than re-underwrites.** Countermeasure: the restated sentence must be about the business at the current price.
10. **The hold that never gets graded.** Countermeasure: the grading record is written at the improve-by date, or at resolution, whichever comes first.
11. **The position that grew into oversize while held.** Countermeasure: the band check is part of the re-underwrite, not a separate quarterly exercise.
12. **The contract that exists only in the holder's head.** Countermeasure: the five fields are written; a contract that cannot be shown cannot be enforced.

## Verification

- **Complete when** all five fields exist in writing, dated.
- **Complete when** the invalidation is a price with a version date.
- **Complete when** the improve-by date is a calendar date and the no-renegotiation rule is recorded.
- **Complete when** every event between grant and improve-by is listed with its date.
- **Complete when** the queued actions and their reasons are recorded.
- **Complete when** the band state and its owner are named.
- **Complete when** the expectation is falsifiable and carries a grading date.
- **Complete when** the cooldown and any wash-sale window are recorded by name, so a later re-entry can be checked rather than remembered.
