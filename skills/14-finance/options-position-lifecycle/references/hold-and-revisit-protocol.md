# Hold and Revisit Protocol

This is the protocol for keeping a losing or stalled position alive on purpose. It answers the question "can I hold this and make it profitable later" with a contract rather than an opinion, and it removes the two failure modes that make holds dangerous: an undated hold, and a date that gets renegotiated every time it arrives.

## The core rule

> **A HOLD-WITH-TP is a dated contract, not a hope.** It names the level that must hold, the target multiple, the events inside the window, and the date by which the position must be at plan. At that date there is no renegotiation: the position is at plan, or it is cut.

Everything else in this reference is machinery for making that rule usable.

## When HOLD-WITH-TP is available

| Precondition | Requirement | Why |
|--------------|-------------|-----|
| Thesis intact | The level holds on the stated measurement | A hold on a broken thesis is a refusal to cut |
| DTE headroom | At least 15 sessions for a repair, at least 8 for anything needing a level test | The plan must fit inside the clock |
| Executable exit | A bid that fills at size today | If you cannot leave, you are not choosing to stay |
| Target multiple | A number, expressed in the position's own terms | "Higher" is not a target |
| Improve-by date | A specific date, and the sessions it represents | The date is the entire mechanism |

Fail any one of these and the protocol does not apply. The consequence in the losing case is CUT; in the "no executable bid" case it is WRITE-OFF with removal from the attention set.

## The four fields of the contract

A HOLD-WITH-TP contract has exactly four fields. All four are required, in writing, in the review record.

### Field 1 — The level that must hold

The same level as step 1 of the health check, restated with its measurement and its session.

```text
level:       112.50, closing basis, RTH
re-arm:      any close under 112.50 pulls the review to that session
```

The re-arm clause matters. The contract has a *date*, but the level can fire earlier. A hold that only responds to its date will sit through a level breach for a week.

### Field 2 — The target multiple

The multiple of the current mark (or the current debit) that defines "at plan". Examples:

```text
target:      2.0x the current mark of $0.85  ->  $1.70
target:      recover to the debit paid of $3.00 (1.0x cost) within 34 sessions
target:      achieve the family's take-profit rung on the spread, i.e. a $0.60 debit
             to close on a $1.20 credit  [COMPUTED: the credit-vertical rung applied
             to $1.20; the rung value itself is owned by trade-sizing-recovery]
```

Two rules about the target:

- **It must be reachable in the remaining time**, not merely desirable. Check it against the one-sigma move over the remaining sessions and against the event calendar.
- **It must be stated in the position's own unit** — the mark, the credit, the debit. A target expressed as "the stock going back to 130" is a forecast; a target expressed as "$1.70 on the mark" is a test that can be graded.

### Field 3 — The event calendar to expiry

Every event inside the window, with the action to be taken at each. The point is that the hold is not a bet on the event; it is a plan that survives it.

```text
events:
  2026-11-04  earnings, after close   -> decision required before the print:
                                          reduce to half, or close, or hold-only-if
                                          implied move < stated threshold
  2026-11-19  FOMC                    -> review at the print; no new extrinsic after
  none other to expiry 2026-12-19
```

An event inside the window that has no stated action is the most common way a well-argued hold becomes an unplanned position.

### Field 4 — The improve-by date

**A specific date**, plus:
- the number of sessions it represents,
- whether it is bounded by the expiry or chosen independently,
- what happens at that date.

```text
improve_by:  2026-11-14 (18 sessions from today)
at the date: if the mark is at or above $1.70, take the target (or trail);
             otherwise CLOSE the position in that session.
```

Recommended horizons:

| Situation | Improve-by horizon |
|-----------|-------------------|
| Long premium with a level test required | 10–15 sessions, or 3 sessions before a DTE floor of 8 |
| Short premium in a breach | 5–10 sessions, or until 21 DTE, whichever comes first |
| LEAPS thesis under review | One month, aligned with the monthly re-underwrite |
| 0DTE | Not applicable — the protocol does not exist at 0DTE |

## The no-renegotiation rule (and how it actually holds)

At the improve-by date the position is graded against Field 2. Two outcomes:

1. **At or above target** → take it, or hand the remainder to a written trailing rule.
2. **Below target** → **close in that session**.

The rule is absolute, and the reason is arithmetic rather than moral. A date that moves once will move every time, because the *reason* to move a date never expires:

- "It's close to the target" is true at every date, by construction — the position is always close to something.
- "There is a catalyst next week" — there is always a catalyst next week.
- "We would be selling at the low" — that judgement is only available in hindsight, so it can always be made.

Once the date is negotiable, the hold has no termination condition except total loss or expiry, which converts a managed risk into an unmanaged one carried by inertia. That is the definition of the failure this protocol exists to prevent.

**One legitimate amendment exists:** the *level* can force an earlier exit (Field 1's re-arm clause). That is not a renegotiation of the date; it is an earlier and stricter deadline firing. It only ever brings the decision forward.

### The amendment record

If someone insists on an amendment, it is recorded rather than refused:

```text
amendment:   improve_by moved 2026-11-14 -> 2026-11-28 (10 sessions)
reason:      <written reason>
approver:    <who>
cost:        the position now consumes attention and capital for 10 more sessions
graded_on:   the new date
outcome:     at plan | worse than plan | better than plan
```

This is how the culture holds itself accountable without pretending that exceptions never happen. A pattern of amendments on the same name is itself the finding.

## Worked example — a full contract

```text
position:      long call, 41 DTE, 2 contracts
debit paid:    $3.10 per contract = $620 total
current mark:  $1.35  -> unrealised about -$350
underlying:    104.20, level 103 holds on the close
liquidity:     0.05 wide on $1.35, open interest in the thousands -> tradeable

Field 1 level
  level:        103.00, closing basis, RTH
  re-arm:       any close under 103.00 pulls the review that session and escalates ACT

Field 2 target
  target:       2.0x the current mark = $2.70 on the option  [COMPUTED]
  reachability: required move on the underlying implied by $2.70 is roughly +7.5%
                over 30 sessions  [ESTIMATED: premium gap $2.70 - $1.35 = $1.35 divided
                by (contract delta ~0.17 x spot $104.20) = $1.35 / $17.71 = 7.6%; delta is
                the binding assumption, so re-derive from the position's own greeks
                before relying on the number]. One-sigma over 30 sessions is about
                6.5%  [ESTIMATED: implied vol ~23% x sqrt(30/365) = 0.23 x 0.287] ->
                demanding but within a plausible distribution, and only if no event
                sits inside the window

Field 3 events
  earnings in 12 sessions, after close
    action at the print: reduce to 1 contract unless the implied move is below 4%
    (measured from the at-the-money straddle)  [ESTIMATED] threshold
  no other scheduled events to expiry

Field 4 improve_by
  2026-11-14 (18 sessions)
  at the date: at or above $2.70 -> trail the remainder; otherwise CLOSE in that session

decision: HOLD-WITH-TP granted
expectation: the level holds, the position reaches $2.70 by the improve-by date, or the
             level forces an earlier exit
grade_on:   2026-11-14 or the level breach, whichever comes first
```

Note the shape of the reasoning: nothing in the contract depends on the trader's beliefs about the stock. Every clause is testable on a date, at a price, or on a close.

## Worked refusal — the same position, no contract

```text
Same position, but:
  - no level is written
  - the "target" is described as "back to even"
  - the improve-by date is "when it turns"
  - earnings are not mentioned

Every precondition fails or is untestable:
  thesis intact .......... cannot be graded (no level)
  target multiple ........ "$620 to $0 loss" is a breakeven, not a multiple, and it
                           implies a move the contract never checked for reachability
  improve-by date ........ does not exist
  events ................. unknown

decision: HOLD-WITH-TP is NOT available.
Two honest options remain:
  a) CUT in the next session into strength, or
  b) build the contract first (write the level, the target, the date, the events),
     and apply the protocol from that moment -- which is a legitimate and better
     option, and is the point of this reference.
```

Option (b) is usually the right answer for a position that is genuinely alive. The failure is not holding a loser; it is holding one without a contract.

## Re-entry: the gate after a cut

A cut is not permanent exile, but re-entry in the same name is a distinct decision with its own gate, and it does not inherit anything from the cut position.

### Cooldown

| Situation | Cooldown |
|-----------|----------|
| Cut on a level breach, thesis genuinely dead | 5 sessions minimum, or until the next scheduled event passes |
| Cut on a band breach, thesis intact | 5 sessions, and the level must hold for at least 2 sessions before re-entry is considered |
| Write-off (no executable exit) | Not applicable; the position left the book |
| Any cut after an amendment was granted | double the standard cooldown — the amendment is evidence of a discipline problem, not of a good name |

The cooldown exists because the day after a cut is exactly when a trader is most likely to re-enter at the wrong size, for the wrong reason, at a worse price. The market will still be there in a week.

### The four-part re-entry gate

All four must pass. This is a deliberately higher bar than a fresh idea, because the name now carries history.

1. **Thesis** — a new, written, level-anchored reason to own it, produced as if the position had never existed. If the re-entry write-up mentions the previous position's loss, it fails: that is revenge wearing analysis.
2. **IV rank** — where is implied volatility relative to its own recent range? Re-entering a premium-selling structure after IV has collapsed means selling the same risk for less; re-entering a long-premium structure at a high IV rank means paying more for the same optionality. Either way it is a check, not an automatic veto.
3. **DTE headroom** — the new position must have room for its plan to complete. A re-entry at 8 DTE with a plan that needs a level test is the same mistake, twice.
4. **Credit/debit floor** — the new position must be priced at least as well as the standard for its family. If the market is offering materially less than the family's normal terms, the correct action is to wait, not to accept less because the name is familiar.

### What re-entry is not

- **Not a way to recover.** Recovery happens at base size on the next qualifying setup anywhere in the book. Re-entering the same name to "get it back" is the recovery-seeking pattern the loss-recovery discipline names directly.
- **Not automatic on a level reclaim.** A level being reclaimed is an input, not a decision. The gate still applies.
- **Not a way to avoid the cooldown by changing the structure.** A different structure on the same name at the same level is the same trade with new labels.

## Failure modes of the protocol

| Failure mode | What goes wrong | Countermeasure |
|--------------|-----------------|----------------|
| The date arrives and is moved | The hold becomes permanent; the loss becomes the position | No renegotiation; amendments are recorded with a cost and a re-grade |
| The target is a breakeven, not a multiple | The contract tests the wrong thing and can never be "at plan" without the full recovery | State the target in the position's own unit and check reachability |
| The level exists but the re-arm clause does not | The hold sits through a breach until the date | Field 1 always includes the re-arm clause |
| The event list stops at the next review | An earnings print arrives inside the contract window | Events run to expiry, always |
| A repair is granted without the DTE headroom | The plan cannot complete; the position reaches expiry unresolved | DTE headroom is a precondition, not a preference |
| Re-entry inside the cooldown at a larger size | One managed loss becomes one unmanaged position | Cooldown is by name and by calendar; the gate is checked, not assumed |
| The contract is written but never graded | Nothing is learned and the next hold starts from zero | An ungraded contract keeps the position flagged as unmanaged |

## Provenance

- The contract structure, the no-renegotiation rule and the cooldown convention are standard practice in disciplined discretionary trading [COMMON-PRACTICE]; they are presented here as an operating specification with testable fields rather than as advice.
- All dollar figures are `[COMPUTED]` from the stated debit, mark and contract count.
- Reachability estimates use one-sigma move arithmetic over the remaining sessions and are `[ESTIMATED]`; they assume a roughly continuous price path, which an event window breaks — that is exactly why Field 3 exists.
- Implied-move thresholds drawn from an at-the-money straddle are a market-implied quantity, not a forecast; read them from the current chain and note the source and timestamp.
- Past performance is not a guarantee. A contract that was honoured last month is evidence about a process, not a promise about the next position.
