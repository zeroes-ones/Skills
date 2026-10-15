# Average-Down Restructure Gate

**Averaging down is forbidden as such.** This is not a stylistic preference; it is the single most reliable path from a managed loss to an unmanaged one. What is sometimes permitted is a different action with a similar shape: a **defined-risk restructure** — a roll that buys a capped, known outcome — and it is permitted only if it passes the five-clause gate below, in writing, with arithmetic attached.

The distinction is not semantic. Averaging down adds risk to a broken thesis at an undefined or unexamined cost. A restructure changes the shape of a live thesis at a cost that has been computed and capped. The gate exists to make sure that is what is happening.

## The forbidden forms

Before the gate, name what is refused. Each of these is routinely described as "fixing the position".

1. **Buying more contracts at a lower price** to lower the average. Undefined additional risk, thesis usually already broken.
2. **Selling additional premium** (a new short leg) to "pay for" a losing long leg. That converts a defined-risk position into a ratio, and ratios are short gamma exactly where you are already wrong.
3. **Rolling out and down for a credit** where the new short strike is closer to the money. The credit is small; the new risk is larger.
4. **Widening the spread** to collect more credit. Max loss grows faster than the credit does.
5. **Doubling on a 0DTE position** because "it has to come back by the close". There is no time for a level test; there is no plan.
6. **Adding to a position with no written invalidation.** If step 1 of the health check cannot be graded, no restructure can be evaluated either.
7. **Restructuring a position that is being held only because of its P&L.** If the only reason to keep it is that selling crystallises a loss, the action is CUT.
8. **Restructuring across a scheduled event** without pricing the event. The restructure's break-even must be evaluated against what will happen before expiry, not against a quiet market that no longer exists.

## The five-clause gate

All five clauses pass, or the restructure is refused. There is no partial credit and no "mostly passes".

### Clause 1 — The level is intact

The original invalidation, on the stated measurement (closing basis, for example), is still satisfied. The last close is on the correct side of it.

If the level broke, the action is CUT. A restructure on a broken thesis is not a repair; it is a second bet on a thesis the market has already answered.

### Clause 2 — DTE ≥ 15

A restructure needs a level test to complete, and a level test takes sessions. Below roughly fifteen days to expiry, the repair is being bought with time the plan cannot use.

Two exceptions, both narrow:
- A restructure whose *entire purpose* is to move away from an assignment or a pin inside the last two sessions — that is not a repair, it is an exit, and it is routed through the calendar force, not through this gate.
- A restructure into a deliberately long-dated expiry (the "roll out a quarter" pattern), where the new DTE provides the headroom even though the old one did not. In that case the gate is evaluated **against the new expiry's DTE**, and the credit-or-debit terms are evaluated against the current mark.

### Clause 3 — New max loss ≤ remaining band

Compute the max loss of the **resulting** structure, not of the leg being changed:

```text
new_max_loss = contracts x (new_width - new_blended_credit) x 100     [credit structure]
new_max_loss = contracts x new_blended_debit x 100                    [debit structure]
```

> **The subtraction is the tell.** `width − credit` is a *loss* only for a credit structure, because a credit structure has to pay the width out. For a debit structure the width caps the **profit**: the worst case is the debit paid, and `width − debit` is the max profit, not the max loss. Credit structures keep `width − credit`; debit structures use the debit paid.

Compare against the band for this name, which is not the same as the original position's max loss. The band is a property of the account; the original max loss was whatever the trade happened to be.

Worked refusal:

```text
Original: 1 put credit spread, width $5, credit $1.20 -> max loss $380
Current:  mark $2.90  (unrealised about -$170 plus the exit spread)
Proposal: roll down to a width-10 spread and collect $2.40
  new_max_loss = 1 x ($10.00 - $2.40) x 100 = $760   [COMPUTED]
Band for this name at this DTE: $600
  $760 > $600  ->  REFUSED. The proposal doubles the loss to buy a better mark.
```

### Clause 4 — The new break-even is reachable within the horizon

The break-even must be a price the underlying can plausibly touch before expiry, given its realised volatility and the event calendar.

```text
required_move = |new_breakeven - spot| / spot
```

Then sanity-check it against how much the underlying typically moves in the remaining sessions. A restructure that needs a 9% move in 20 sessions is not a repair; it is a different, harder trade in the same name.

Worked example:

```text
spot 118, new breakeven 124.5 -> required move = 5.5%   [COMPUTED]
realised one-sigma move over 20 sessions: 4.8%          [ESTIMATED]
-> the break-even sits just beyond one standard deviation: demanding but not absurd,
   PROVIDED no earnings print sits inside the window. If one does, the event makes the
   distribution bimodal and the one-sigma arithmetic no longer describes it.
```

That last caveat matters: standard-deviation reasoning assumes a continuous, roughly normal path. An earnings print inside the window breaks that assumption, so an event window tightens clause 4 substantially.

### Clause 5 — Net debit ≤ a stated share of the current mark

The cost of the repair must be small relative to what is being repaired. The working rule used with this gate:

```text
net_debit_of_restructure <= 0.5 x current_mark_of_position
```

Worked example:

```text
current mark $1.90  ->  debit budget = $0.95 per unit  [COMPUTED]
proposed roll costs $0.35 debit   -> within budget    [COMPUTED]
proposed roll costs $1.20 debit   -> REFUSED; the "repair" costs more than the
                                     remaining value of what it repairs
```

Why half? Because a repair costing more than half of the remaining position is a new position financed by the old one's loss. If the trader genuinely believes in a new structure at the new level, they should close and open it fresh, through the full entry process — which is a higher bar, and deliberately so.

A roll **for credit** trivially satisfies clause 5. That is exactly why clause 3 exists: a credit roll that widens the loss is the most common way to pass a "no-debit" rule while taking on more risk.

## The gate worksheet

Every proposal is written on this worksheet. A proposal without a completed worksheet has not been evaluated.

```text
position:              <name, structure, expiry, contracts>
proposal:              <what changes: expiry, strikes, width, count>
reviewed_at:           <timestamp, source of marks>

clause 1  level intact
  level:               <level>          measurement: <close|intraday>
  last reading:        <value>          result: PASS|FAIL
clause 2  dte >= 15
  current dte:         <n>              new dte: <n>        result: PASS|FAIL
clause 3  new max loss <= band
  new max loss:        <$>              [COMPUTED] from width, credit/debit, contracts
  band for name:       <$>                                 result: PASS|FAIL
clause 4  break-even reachable
  new breakeven:       <price>          required move: <pct>   [COMPUTED]
  one-sigma over dte:  <pct>            [ESTIMATED]           result: PASS|FAIL
  events in window:    <list|none>
clause 5  debit within budget
  current mark:        <price>          debit budget: <0.5 x mark>  [COMPUTED]
  net debit of roll:   <price>                               result: PASS|FAIL

decision:              PROCEED | REFUSE
refusal_reason:        <which clause, and the number that failed>
grade_on:              <date>
expectation:           <one sentence>
```

**Refusal is the expected outcome.** Most proposals fail clause 3 or clause 5. A gate that mostly says yes is not a gate.

## What "proceed" entails

A restructure that passes is still an action above HOLD, so R8 applies: write the expectation and the grading date. Beyond that:

1. **Execute the whole structure, not the legs.** A restructure is one decision; legging into it introduces fill risk that belongs to `options-leg-management` and must be planned, not improvised.
2. **Replace every bracket.** The old TP and SL reflect the old structure. An unrestructured bracket is worse than no bracket, because it pretends to protect something.
3. **Re-run the health check on the resulting position today.** Clause 3 was computed from the design; verify the fill delivered the design.
4. **Report the new max loss downstream.** `options-risk-engineer` needs it for aggregate risk; the band it was checked against is the account's, not the trade's.
5. **Record the refusal if it was refused.** Refusals are data. A name that generates repeated failing proposals is a name whose entry process should be examined.

## Worked full example — a passing restructure

```text
Position: 1 call credit spread on a name at 100
  short 105 call, long 110 call, credit $1.40 -> max loss $360
  invalidation: closing basis over 104
  DTE: 34

Today (day 12 of the position)
  spot 103.5, closing basis under 104 -> level intact
  mark $2.20 (debit to close) -> unrealised about -$80
  proposal: roll up and out, short 107 / long 112, expiry +21 days, collect $0.10 credit

clause 1  level intact: last close 103.5 < 104 ................ PASS
clause 2  DTE: current 22, new 43 -> both >= 15 .............. PASS
clause 3  new max loss: 1 x ($5.00 - $1.40 - $0.10) x 100
            = $350   [COMPUTED]
          band for this name: $600 .......................... PASS
clause 4  new breakeven: 107.00 + $1.50 = 108.50  [COMPUTED -- CALL credit
            spread: short strike + net credit, 107.00 + (1.40 + 0.10)]
          required move from 103.5: 4.83%  [COMPUTED: (108.50 - 103.50) / 103.50]
          one-sigma over 43 sessions: about 5.5%  [ESTIMATED] .. PASS
            (but at the boundary: the break-even now sits just inside one
             standard deviation, so the level has to hold on its first test)
          events in window: none ........................... PASS
clause 5  debit: -$0.10 (a credit, not a debit) -> within budget .. PASS

decision: PROCEED
expectation:  with 43 days and the level holding, the spread decays to the
              credit-vertical TP rung, a 50% capture of the $1.50 blended credit
              ($0.75 debit to close) [COMPUTED: 0.5 x $1.50] or the level forces
              an exit
grade_on:     the earlier of the level test and day 30
```

Note what the example does **not** do: it does not lower the break-even. It moves the whole structure up to follow the level, keeps max loss roughly the same, and buys time. That is what a restructure is. Lowering the break-even by taking more risk is what a restructure is not.

## Worked full example — a refused restructure

```text
Position: 3 long calls on a name at 42, debit $2.60 each = $780 total
  no written invalidation  <- step 1 of the health check cannot be graded
  mark $1.30 -> unrealised about -$390
  proposal: buy 3 more contracts at $1.30 to bring the average to $1.95

clause 1  no level exists ............................... FAIL
clause 3  new max loss would be $780 + $390 = $1,170, on a name whose band is $500
          -> also FAIL  [COMPUTED]
clause 5  debit $390 against a current mark of $390 -> 1.0 x mark
          > 0.5 x mark budget ............................ FAIL

decision: REFUSE
  This is average-down. The permitted actions are:
    - CUT into strength (the position has a bid and a level can be chosen now)
    - CLOSE and re-underwrite from scratch if the thesis is genuinely live
  Note: with no invalidation level, the position cannot be held under HOLD-WITH-TP
  either; step 1 must be fixed before any protocol can be applied.
```

## Failure modes of the gate itself

1. **Clause 1 graded against the mid instead of the close.** The measurement was chosen at entry; deviating from it when convenient is how a level becomes optional.
2. **Clause 3 computed on the changed leg rather than the resulting structure.** Countermeasure: recompute from the resulting design every time, and write the number down.
3. **Clause 4 hand-waved as "the stock usually moves".** Countermeasure: one explicit percentage and one explicit required move; no move, no pass.
4. **Clause 5 measured against the original cost rather than the current mark.** Countermeasure: the mark is what is left; the cost is history.
5. **Passing by construction — a credit roll with a widened loss.** Countermeasure: clause 3 is checked on max loss in dollars, never on the sign of the credit.
6. **The gate is run after the roll.** Countermeasure: the worksheet comes first; an executed restructure without a worksheet is recorded as a rule violation, not as a restructure.
7. **The restructure is granted but the thesis is a story.** Countermeasure: clause 1 requires a written level; if there is none, the answer is CUT, and the missing contract is the actual finding.

## Provenance

- The five clauses are **derived from data** about how options positions actually fail — wide-loss restructures, credit rolls that increase risk, and repairs that cost more than the position — expressed as arithmetic rather than as opinions. The 15-DTE floor and the half-of-mark debit budget are operating bands [ESTIMATED], calibrated so that a repair has a plausible chance to complete.
- All dollar figures in the worked examples are `[COMPUTED]` from the position's own width, credit/debit and contract count, and are reproducible by hand.
- Strategy-based margin treatment of a widened or ratiod structure is governed by published exchange margin material [VERIFIED] Cboe margin manual, and by the margin requirements of the relevant regulator [VERIFIED] FINRA Rule 4210 for listed option positions. Always compute against the schedule your own broker applies, and tag that result `[BROKER-VERIFIED]`.
- Nothing here is a prediction. Past performance is not a guarantee; a gate that passes says the proposal is bounded, not that it will work.
