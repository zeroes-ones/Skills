# When NOT to Touch a Leg

Every other reference in this skill explains how to perform a leg operation. This one explains
when performing one is the mistake. Doing nothing is an action with a price tag, and it is the
correct action more often than a busy trader's instincts suggest.

## The no-op conditions

Holding is correct when **all** of these are true:

| # | Condition | How to check it mechanically |
|---|---|---|
| 1 | No decision-matrix row fires | Walk the matrix. Zero rows triggered means zero operations |
| 2 | The structure's invalidation line has not been touched | Compare the last RTH close to the stated invalidation |
| 3 | No short leg is inside the pin band | DTE ≤ 2 and within ~1% of spot → the guard fires and this file does not apply |
| 4 | No event lands inside the remaining life that the position was not designed for | Earnings, ex-dividend, macro prints; each either absent or explicitly accounted for |
| 5 | The position sits inside its authorized size and loss band | Size is `trade-sizing-recovery`'s field; if the band is breached, that is a different conversation |
| 6 | The thesis is intact as written at entry | If you cannot state the thesis in one sentence, you cannot claim it is intact |
| 7 | A leg operation would change nothing about the risk you are actually carrying | The test that matters: does any operation available to you reduce a loss you are exposed to? |

If all seven hold, the correct output is a **no-op review**: hold, log it, set the next check date.

## The cost of acting when nothing has fired

| Acting "to be safe" | What it actually costs |
|---|---|
| Closing a structure whose thesis is intact because "it feels exposed" | The remaining expectancy, plus a spread of slippage, plus a re-entry decision you now have to make |
| Downgrading a healthy fly | The tail value, converted into a position with a capped payoff and a lower break-even margin |
| Rolling early, outside the window | Two spreads paid to remove risk that is not yet being carried |
| Taking profit in fractional legs | A position that is neither the original nor an exit, and cannot be managed by the original plan |
| Adding a protective wing "just in case" | A new leg, a new structure, a new ledger row, and a cost — a construction, not a guard |

The common thread: each of these operations changes the position **without changing the risk you
are facing**. The risk that matters is the one you are exposed to today, and if no operation
reduces it, the operation is decoration.

## The "should I do something?" flowchart

```text
   Position reviewed
        │
        ▼
   Does ANY decision-matrix row fire?
        ├── NO ──▶ is any short inside the pin band (DTE <= 2, within ~1%)?
        │              ├── NO  ──▶ NO-OP REVIEW
        │              │             · hold
        │              │             · log the decision + the condition that keeps it valid
        │              │             · set the re-check date
        │              │             · do not re-open the question before that date
        │              └── YES ──▶ PIN GUARD. This file does not apply
        └── YES ──▶ the fired row names the operation; execute it per its gates
```

## What a no-op review must contain

A no-op review is a decision, not an absence. It has the same evidence standard as an operation,
minus the order.

| Field | Value |
|---|---|
| Timestamp | When the review ran |
| Leg list | The live list, verbatim, with signs |
| Matrix walk | The rows checked and the result of each — "no row fired" is a finding, not an omission |
| Pin-band check | Short legs, their DTE and their distance from spot |
| Event scan | Any event inside the remaining life, and why it does not change the plan |
| Thesis restatement | One sentence, verbatim from the entry plan |
| Validity condition | The specific thing that would make this hold wrong |
| Re-check date | When this decision is revisited |

`[COMMON-PRACTICE]` Logging no-op reviews is a desk convention with a measurable purpose: it makes
"we did nothing and the position lost money" a recorded decision that can be scored, rather than
an unexamined default.

## When "do nothing" is the wrong answer

The mirror image matters too. Holding is wrong — and the failure is the same failure, just
inverted — when:

| Situation | Why holding is the mistake |
|---|---|
| A short leg is inside the pin band | The guard is a scheduled action; not acting is a decision to accept assignment |
| The invalidation line has been crossed | The thesis is dead; the position is now an unmanaged bet on a different outcome |
| A pin-band short, an event inside the life, and no plan for either | Two unmanaged risks at once |
| The structure is below its band and above its stop | A stop is a stop; the band is not a suggestion |
| An assignment has landed and has not been triaged | Capital and risk outside the plan, growing more expensive to resolve with each session |
| A package fill produced a state that fails the R1 test | That state is not "the position"; it is a defect to be fixed today |

## The discipline of not re-opening the question

The most common failure of the no-op is not the decision — it is re-deciding it. A position
reviewed and held at 10:00 and re-examined at 11:00, 12:00 and 14:00 has not been held; it has been
traded emotionally four times, with four chances to talk yourself into an operation that no
trigger supports.

```text
   no-op review  ──▶ decisions: HOLD, with a condition and a date
                        │
                        ▼
   the question re-opens ONLY when:
        · the validity condition breaks, OR
        · the re-check date arrives, OR
        · a NEW matrix row fires (a new trigger, not the same one re-felt)
```

`[COMMON-PRACTICE]` The re-check date is the desk's convention; the interval is a book-level
choice, not a market fact.

## Anti-patterns

| ❌ | Why | ✅ |
|---|---|---|
| ❌ "Doing something" as a substitute for a thesis | An operation without a trigger is decoration with a price tag | ✅ Walk the matrix; if nothing fires, hold and log |
| ❌ Closing a healthy structure to make the book "feel lighter" | Costs the remaining expectancy and a spread, and creates a re-entry decision | ✅ Reduce in whole units only when a profit rung fires |
| ❌ Treating a no-op as an omission in the log | Then it cannot be scored, and unexamined defaults hide the real edge | ✅ Log the walk, the pin check, the event scan and the validity condition |
| ❌ Re-deciding the hold every hour | Four reviews, four chances to act on nothing | ✅ Re-open only on the validity condition, the re-check date, or a new trigger |
| ❌ Rolling early "so it is done before it gets busy" | Pays to remove risk that is not yet being carried | ✅ Respect the window; mark the cost each session instead |
| ❌ Confusing "the position is fine" with "no matrix row fires" | The first is a feeling; the second is a test with a written result | ✅ Write the matrix walk down |

## Sources, provenance and limits

- `[COMMON-PRACTICE]` The no-op review format, the validity-condition field and the re-check cadence
  are desk conventions. They are not regulatory requirements, and no exchange or clearing
  organisation prescribes them.
- `[VERIFIED]` The exceptions listed under "when holding is the wrong answer" rest on established
  facts: an uncovered short carries unbounded (call) or strike-to-zero (put) risk, and assignment
  of a physically settled option results in a position in the underlying — per the OCC's standard
  options disclosure document and US options exchange rules.
- `[ESTIMATED]` The pin-band figures (DTE ≤ 2, within ~1% of spot) are data-backed desk thresholds
  derived from data on this desk's own study. They are approximate, are not exchange rules, and
  are not a guarantee.
- This file makes no claim about measured outcomes. Past performance of a holding decision does
  not predict the next one, and any statement about what "usually" happens is a convention, not a
  measured result.
