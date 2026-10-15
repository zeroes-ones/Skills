# Cut and Stop Discipline

The cut is the action that keeps a book solvent. It is also the action most often converted into something else — a hold, a "repair", a wider stop, a new structure in the same name. This reference defines what a stop is here (a level, not an order), how a cut is executed (into strength, not into a gap), the 0DTE exception, and the honest alternative when no cut is possible.

## A stop is a level, not a resting order

The single most important sentence in this reference:

> **The stop is a level on the underlying, plus an action. It is not a resting order.**

Why:

1. **Options books gap.** Liquidity in an option can vanish between the quote and the fill. A stop order that triggers into a thin book fills at whatever the next bid is, which can be far from the level it was meant to defend.
2. **The level is about the thesis, not the premium.** A position can be at −30% of debit with a level that is perfectly intact, and at −5% with a level that has broken. A premium-based stop cannot distinguish these; a level-based stop can.
3. **The action is a decision, and decisions should be made by someone.** A resting order removes the decision from the only moment where the trader still has options (session, size, structure).

The resting order is allowed as a **convenience** — a GTC order that captures a target if the market happens to get there — but it is never the plan, and the level is tracked independently.

### What a usable level looks like

| Property | Bad example | Good example |
|----------|-------------|--------------|
| Measurable | "if it keeps falling" | "closing basis under 112.50" |
| Stable | Redrawn weekly | Unchanged since entry, or changed with a written reason |
| Commensurate with the band | Implies a 4× band loss | Implies a loss inside the size band |
| Session-defined | Unclear whether it is intraday | "closing basis, RTH" |
| Action-attached | Level with no stated action | "level breach → CUT into the first 30 minutes of RTH" |

The fourth row matters more than it looks. A level measured intraday will fire on noise; a level measured on the close will occasionally cost a day. Pick one at entry, record it, and do not switch when the other would have been convenient.

## Loss-band triage

The cut decision is driven by the band, not by the number that feels relevant. Bands come from `trade-sizing-recovery`. Position-management adds the mechanism, not the band.

| Band state | Disposition | Mechanism |
|------------|-------------|-----------|
| Inside band | HOLD (with a date and a level) | None — continue the review |
| Rung hit | TRIM | Whole units, ladder |
| Band breach, thesis intact, DTE ≥ 15 | CUT, or RESTRUCTURE if the written gate passes | Into strength, or first 30 min of RTH |
| Band breach, thesis broken | CUT | Into strength, or first 30 min of RTH |
| Band breach, thesis broken, no executable bid | WRITE-OFF | Stop paying attention, not money |
| 0–2 DTE with a live assignment or pin risk | Expiry protocol | Decide by 15:45 ET; act same session |

Two rules govern this table:

- **A thesis breach outranks a band breach.** If the level broke, the disposition is CUT regardless of where the P&L sits — including if the position is *profitable*.
- **A calendar force outranks both.** Near expiry, mechanics decide, and the disposition is whatever the mechanics require.

## Cutting into strength, not into a gap

Execution is where a correct decision becomes a bad outcome. The rules:

### Standard structures

1. **Never cut into a gap.** A gap-down open is the worst liquidity of the session for a long position and the widest spread of the session for a spread. If the book gapped through the level overnight, the action is *not* "sell at the open".
2. **Use the first 30 minutes of RTH.** Liquidity builds after the open as the auction clears and participants establish the day's range. The first 30 minutes is a compromise: early enough to act on the news, late enough to avoid the opening print.
3. **Cut into strength, when strength exists.** If the position is a losing long premium and the underlying bounces into a known level, that bounce is a liquidity gift and should be taken. Waiting for "a bit more bounce" converts a mechanism into a forecast.
4. **Size the exit as a structure trade.** Close the spread or the condor as a structure; leg-by-leg exits on a losing position are where slippage compounds. If the structure must be legged, that belongs to `options-leg-management` and must be planned in advance.
5. **Accept the fill and record the gap.** The difference between the mark and the fill is an execution cost. Record it as one. Do not reinterpret it as "the band was wrong", and do not chase it by holding for a better price.
6. **Confirm the cancellation of every bracket.** After a cut, no resting order should remain that could open a new position in that structure.

### Order-placement detail

| Situation | Approach |
|-----------|----------|
| Wide, illiquid structure | Limit order at a defensible price; be prepared to work it over the session |
| Liquid structure, ordinary session | Marketable limit near the mid — capture the spread rather than paying it |
| Multi-leg structure | One structure order where supported; otherwise a planned legging sequence, never an improvised one |
| Thin single-leg long | Work it in slices; a single market order on a thin book is a donation |
| Half-day session | Compress the timeline; the "first 30 minutes" window is shorter and the close comes earlier |

### The session rule, stated plainly

> A position whose level broke must be acted on in the **same session** if the market is open, or in the **first 30 minutes of the next RTH session** if it is not.

"Gap risk until the window opens" is a real risk that the trader accepts knowingly, in writing, with brackets in place if the structure permits it. It is not an excuse to defer the decision until a more comfortable moment.

## The 0DTE exception

A 0DTE position is decided and executed **in the same session**. There is no overnight plan because there is no overnight.

| Rule | Why |
|------|-----|
| The stop is intraday, on the underlying | The option's price can move more than the plan assumed in minutes |
| The decision deadline is before 15:45 ET | After that, the decision is made by the closing auction and the clearing house, not by you |
| No new extrinsic is paid | There is no time left for a level test |
| No averaging | There is no opportunity for the thesis to be validated |
| Assignment risk is live from the open | An ITM 0DTE short can be assigned; the stock leg becomes a next-session problem |
| Record the exit plan at entry, not at noon | The moment of maximum gamma is the worst moment to design a plan |

## When the cut is unexecutable: write-off discipline

Sometimes the correct decision cannot be executed. The bid is pennies wide, there is no depth, or the position is too small for the fees to be worth it. In that case:

1. **Reclassify as a WRITE-OFF candidate.** The decision is still "we are leaving"; the mechanism changes.
2. **Mark it "no-TP by construction"** in the record.
3. **Remove it from the attention set.** This is the point. A dead lot reviewed daily costs more attention than it costs dollars.
4. **Leave one resting order** at a level you would genuinely accept, if the structure is single-leg and the order costs nothing to maintain. Do not monitor it.
5. **Let it expire** if there is no bid. Collect the lesson row.

The temptation is to keep reviewing a write-off "just in case". That temptation is the reason the attention budget exists as an explicit concept: a position that cannot change its outcome should not be consuming any of it.

## Worked examples

### Example 1 — cut on a level breach while profitable

```text
Position: put credit spread, short strike 112, invalidation "closing basis under 112"
  credit received $1.20 -> max loss $380
  current mark $0.55 (a debit of $55 to close) -> unrealised about +$65
  spot 111.20 on the close

Step 1 fails: the closing basis is under the invalidation level.
Disposition: CUT, despite the position being profitable.

Why: the level is what justified the trade. With the level gone, the remaining $0.55
is compensation for keeping a risk the thesis no longer describes. Closing locks in
about +$65  [COMPUTED] (the mark, before the exit spread) and removes the assignment
and directional risk from the book.
Action: close in the first 30 minutes of RTH, as a structure order.
```

Traders who only have a P&L rule cannot make this decision. This is the case that argues for level-based stops more clearly than any other: a profitable position with a broken thesis is a position you are being paid to keep, for a reason you no longer believe.

### Example 2 — gap through the stop

```text
Position: long call, debit $3.00 per contract, level "closing basis under 96"
  overnight: the name reported and opens at 92 (a gap under the level)
  the option indicates $0.85 at the open against a $1.30 mid from yesterday

Wrong action: sell at the open into the widest spread of the day.
Right action:  do not chase the print. Queue the exit for the first 30 minutes of RTH;
               if the option's market widens further, work a limit at a level you can
               defend. Accept the fill and record the gap.

Reality check: the level broke. The decision was already made; only the mechanism
remains, and the mechanism is a session-timing question, not a thesis question.
```

### Example 3 — the "repair" that is really a hold

```text
Position: iron condor, call side breached, 11 DTE
  Proposal: "roll the call side up and out for a credit"

Test the proposal against the action router:
  rung 3 (thesis broken at the call level) fires before rung 6 (structure degraded)
  -> the action is CUT, not ROLL.
  If the trader believes the level will be reclaimed, that is a HOLD-WITH-TP, and it
     requires a level, a target multiple, an improve-by date and an event list --
     and 11 DTE fails the DTE-headroom precondition. So: CUT.
```

The mechanism here matters as much as the answer: the proposal *was* a roll, and rolls are legitimate actions at rung 6. It loses because rung 3 fires first. Priority order is what prevents a repair from being used to defer a cut.

## Cut-discipline anti-patterns

| ❌ | ✅ |
|----|-----|
| "It only broke the level on the close, let's see tomorrow" | The measurement was chosen at entry. Closing basis under the level → act next session |
| Cutting at the open into a gap | First 30 minutes of RTH, or a defensible limit |
| Moving the stop to keep the position alive | A level change requires a written reason and a grading date |
| Holding a profitable position whose thesis broke | Level outranks P&L; the profit is a reason to exit well, not to stay |
| Reviewing a write-off daily | Remove from the attention set; one resting order at most |
| Legging out of a losing structure on the fly | Plan the legging with `options-leg-management`, or trade it as a structure |
| Leaving brackets live after a cut | Cancel every resting order that could reopen the structure |
| Treating "no executable bid" as "the band was wrong" | The band was right; the mechanism changed. Write off, record the lesson |

## Post-cut obligations

1. **Cancel and re-verify brackets.** No resting orders that could reopen the position.
2. **Record the action above HOLD** with the expectation, the fill, and a grading date.
3. **Grade the fill against the mark** and log the execution cost separately from the loss.
4. **Report the freed risk** to `options-risk-engineer` and the freed capital to the book.
5. **Start the name's cooldown.** Re-entry in the same name requires the gate in `hold-and-revisit-protocol.md`, not a fresh price.
6. **Write the lesson row** — one line, actionable, and specific enough to change a rule.

## Provenance

- The level-based stop, the cut-into-strength convention and the session rules are standard risk-management practice for options positions [COMMON-PRACTICE], adapted here into an ordered disposition with explicit mechanisms.
- Every dollar figure is `[COMPUTED]` from the stated credit, debit and mark.
- Expiration, assignment and exercise-by-exception behaviour is governed by the clearing house [VERIFIED] OCC expiration processing, and by the exchange rules for the venue; verify against your own venue's published rules before relying on a specific session time.
- The 15:45 ET decision deadline reflects late-day liquidity and closing-auction handling in US equity options sessions; confirm on your venue's session calendar, especially on half-days.
- Past performance is not a guarantee. A level that worked last month is evidence about a process, not a forecast about a price.
