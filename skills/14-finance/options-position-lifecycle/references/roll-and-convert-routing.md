# Roll and Convert Routing

Two actions change a position rather than ending it: **ROLL** (temporal change — the same structure, later) and **CONVERT** (structural change — a different structure). This reference defines when each is available, what is forbidden, who owns the numbers, and how the two are told apart when a proposal is described vaguely.

## Roll versus convert, in one table

| | ROLL | CONVERT |
|---|------|---------|
| What changes | Expiry, and optionally strikes along the same axis | The structure itself (kind, width, ratio, orientation) |
| Why | To buy time for an intact thesis | To express an intact thesis better |
| Bound | Credit-or-flat; maximum **two rolls per position** | Must be strictly better on stated criteria |
| Owner of mechanics | `options-leg-management` | `options-leg-management` |
| Owner of the window | `options-risk-engineer` | `options-risk-engineer` |
| Owner of the numbers | `trade-sizing-recovery` (band and credit/debit) | `trade-sizing-recovery` |
| Forbidden version | Rolling to fix a broken thesis | Converting to hide a loss |

If a proposal cannot be classified as one of these two, it is not a structure edit. It is either a CLOSE or a new position.

## ROLL

### The rule set

1. **Credit-or-flat only.** A roll that costs a net debit is not a roll; it is a RESTRUCTURE and must pass the five-clause gate.
2. **Maximum two rolls per position**, counted from original entry. A third roll is a schedule hiding a loss.
3. **New max loss ≤ the remaining band.** Recomputed on the resulting structure, in dollars, not on the sign of the credit.
4. **The new expiry's DTE must fit the plan.** Buying 45 more days for a plan that needed 10 is buying something you will not use.
5. **The thesis must be intact.** If it is not, the action is CUT.

### The most common invalid roll

> Rolling **out and down** for a credit, where the new short strike is closer to the money than the old one.

This passes rules 1, 2 and often 3 (if the width is unchanged), and it fails on rule 5 in spirit: the position now needs *more* of the same directional view to work, for a *smaller* credit, over a *longer* period. The credit is not payment for the extra risk; it is the market's price for taking it.

Detect it by computing the new break-even next to the old one. If the break-even moved **against** the thesis, the roll is a size increase in disguise, and the correct routing is the RESTRUCTURE gate (which will usually refuse it), or CUT.

### Roll windows

A roll window is decided by the calendar, not by the P&L:

| Family | Typical window | Why |
|--------|---------------|-----|
| Short premium (spread, condor, fly) | 21–45 DTE | Gamma is still small, and there is enough extrinsic left to sell |
| Long premium (single, vertical) | 21–45 DTE, or when the remaining extrinsic is no longer worth paying for | Rolling close to expiry pays for time you barely get |
| Calendars and diagonals | Near-leg expiry, or a stated extrinsic floor on the near leg | The near leg is the engine; roll it on its own terms |
| LEAPS | Planned windows only, months ahead | The position is rho- and dividend-driven; ad-hoc rolls pay spread for nothing |
| Any position with a live assignment risk | Immediately, and separately from the roll plan | Assignment is a mechanics problem, not a roll |

`options-risk-engineer` owns the window computation because the window is a portfolio- and calendar-level fact (expirations, margin cycles, event dates), not a per-position preference.

### Roll mechanics summary

These are summaries, not instructions; the mechanics belong to `options-leg-management`, and the fill assumptions to your venue.

| Roll type | Shape | Main risk |
|-----------|-------|-----------|
| Same strikes, later expiry | A pure time purchase | Paying up in extrinsic; the debit can be material at long DTE |
| Up and out (short strike moved away, later expiry) | More room for the thesis | Requires a credit to satisfy rule 1; often unavailable |
| Out and down (short strike moved closer) | Looks like a credit roll | Break-even moves against you; the invalid roll above |
| Diagonal roll (different strikes and expiries per leg) | Repairs a drifted delta | Creates a diagonal unintentionally; must be a deliberate design |
| Whole-structure roll as one order | Best fill quality | Requires the venue to support structure orders; otherwise plan the sequence |

### Roll checklist

```text
1. Classification: is this temporal (ROLL) or structural (CONVERT)?
2. Thesis: intact at the level, on the stated measurement?          if NO -> CUT
3. Roll count: is this roll 1 or 2?                                 if 3 -> refuse, route to CUT
4. Net credit/debit: credit or flat?                               if debit -> RESTRUCTURE gate
5. New max loss computed in dollars, compared to the band          if over -> refuse
6. New break-even computed and compared to the old one             if worse -> refuse
7. DTE headroom: does the new expiry fit the plan that must complete?
8. Window: is this inside the family's roll window (options-risk-engineer)?
9. Events: anything inside the new expiry that was not inside the old one?
10. Brackets: replaced and re-priced for the resulting structure
11. Record: expectation and grading date
```

Step 6 is the one that catches the most bad rolls, and it is the cheapest to compute.

### Worked example — a legitimate roll

```text
Position: call credit spread, short 108 / long 113, credit $1.30 -> max loss $370
  DTE 21, spot 105.5, level "closing basis over 107" not breached
  band for this name: $600

Proposal: roll to the same strikes, +35 days, for a $0.05 debit (near flat)

1  ROLL (temporal) ................................................. PASS
2  level intact at the close ..................................... PASS
3  this is roll 1 of a maximum of 2 ............................. PASS
4  net $0.05 debit -> technically a restructure, so run the gate:
     clause 1 level intact ...................................... PASS
     clause 2 new DTE 56 >= 15 ............................... PASS
     clause 3 new max loss = 1 x ($5.00 - $1.30 + $0.05) x 100
                = $375  [COMPUTED]  vs band $600 .............. PASS
     clause 4 new breakeven 108 + 1.25 = 109.25  [COMPUTED -- CALL credit
                spread: short strike + net credit, 108 + (1.30 - 0.05)];
                required move 3.55% from 105.5  [COMPUTED:
                (109.25 - 105.50) / 105.50];
                1-sigma over 56 sessions at ~16% implied vol is
                about 6.3%  [ESTIMATED: 0.16 x sqrt(56/365)] .... PASS
     clause 5 debit $5 vs half the mark -- current mark is about
                $1.85, so the budget is $0.92  [COMPUTED] ..... PASS
6  break-even moved from 109.30 to 109.25 -- essentially unchanged, not worse ... PASS
   [COMPUTED: 108 + 1.30 before the roll, 108 + 1.25 after it]
7  DTE headroom: the plan needs 8-10 sessions of level holding; 56 days fits ... PASS
8  window: 21 DTE is inside the 21-45 window ..................... PASS
9  events: no earnings inside the old window; the new window adds a
     scheduled macro print -> add it to Field 3 of the exit contract . noted
10 brackets replaced at the resulting levels and size
11 expectation: "the level holds and the position decays to the credit-vertical
     TP rung, a 50% capture of the $1.25 net credit ($0.63 debit to close)
     [COMPUTED: 0.5 x $1.25] within 25 sessions"
```

A five-cent debit roll that changes nothing about the risk and buys 35 days is a legitimate time purchase. Note that it passed the RESTRUCTURE gate rather than the "credit-or-flat" test — the classification rule sent it there, and the gate was cheap to run.

### Worked example — a roll that must be refused

```text
Position: put credit spread, short 100 / long 95, credit $1.60 -> max loss $340
  DTE 9, spot 101, mark $2.40 (about -$80 unrealised)
  level "closing basis under 99.5" -- last close 101 -> intact

Proposal: roll out 30 days and down 4 strikes, short 96 / long 91, for a $0.30 credit

1  temporal? expiry and strikes both change -> arguably a CONVERT, but it keeps its kind,
   so treat it as a roll and run both tests
2  level intact ................................................... PASS
3  roll 1 ........................................................ PASS
4  net credit $0.30 -- the "credit-or-flat" box is ticked
5  new max loss, on the convention adopted below:
     whole-life accounting (the one clause 3 above already uses): the credit
     earned on this name is 1.60 - 2.40 + 2.70 = $1.90, so
       max loss = 1 x ($5.00 - $1.90) x 100 = $310  [COMPUTED]  vs band $600 -> PASS
     (structure-only accounting: the new spread carries the $2.40 buy-back plus
      the $0.30 roll credit = $2.70, so max loss = 1 x ($5.00 - $2.70) x 100 =
      $230  [COMPUTED]. Either way the band holds; the $80 already realised stays
      on the name's record, which is why the whole-life figure is $310, not $230)
6  new break-even = 96.00 - $0.30 = 95.70  [COMPUTED -- PUT credit spread:
   short strike - credit]
   old break-even = 100.00 - $1.60 = 98.40  [COMPUTED]
   The break-even moved from 98.40 DOWN to 95.70 -- the position now needs the
   underlying to fall 5.25% instead of 2.6% before it stops being profitable at
   expiry [COMPUTED: (101 - 95.70) / 101 and (101 - 98.40) / 101].
   The roll moved the break-even AGAINST the thesis. -> REFUSE
   The credit was the price of the extra 2.7% of required move, not a gift.
   (On structure-only accounting the new break-even is 96.00 - $2.70 = 93.30 and
    the required fall is 7.6% -- the same refusal, for the same reason.)

Alternative routing: this is an out-and-down roll, i.e. a risk increase dressed as a
credit. If the trader genuinely wants a wider structure, that is a new position and it
goes through entry. Otherwise: CUT, at 9 DTE, in the first 30 minutes of RTH.
```

Both examples ticked "credit". Only one was a roll.

## CONVERT

### Convert rule set

1. **Strictly better on stated criteria.** Name the criteria before evaluating: max loss, break-even, probability of touching the short strike, capital efficiency, assignment profile. "Different" is not a criterion.
2. **The thesis is unchanged.** A convert expresses the same view better. If the view changed, this is a new position.
3. **Not a way to hide a loss.** Selling more premium into a losing spread to "pay for it" is an ADD to a loser. It fails here and at the router's rung 3.
4. **Defined risk afterwards.** A convert that leaves naked exposure is a step-2 failure at the next review, by construction.
5. **All numbers recomputed.** New max loss, new break-even, new margin, new pin profile.

### Legitimate converts

| From | To | The criterion that improves |
|------|----|---------------------------|
| A vertical whose delta drifted far from the thesis | A vertical at the new level | Delta alignment with the still-intact level |
| A single long that has become deep ITM | A vertical (sell a higher strike) | Capital efficiency: the far-OTM upside is cheap to give up for a collected credit |
| A condor with one side tested | A vertical on the tested side plus a fresh opposite side later | Defined risk on the tested side, and no naked exposure |
| A calendar whose near leg has decayed | A fresh calendar | The engine (the near leg's extrinsic) is renewed on purpose, not by accident |
| A position with two redundant legs | The equivalent narrower structure | Margin and commission efficiency, with the same payoff by construction |

### The conversion worksheet

```text
position:            <identifier>
from:                <structure, strikes, expiries, contracts>
to:                  <structure, strikes, expiries, contracts>
criteria improved:   <named list, with before/after values>
  max_loss:          before <$>  after <$>       [COMPUTED]
  breakeven:         before <price> after <price> [COMPUTED]
  delta:             before <n>  after <n>
  margin:            before <$>  after <$>        [BROKER-VERIFIED from your schedule]
naked exposure after: none (required)
thesis unchanged:    yes (required)
events in new window: <list|none>
decision:            PROCEED | REFUSE
grade_on:            <date>
```

Any convert that cannot fill this worksheet is not a convert; it is an improvisation.

## Routing interfaces

### To `options-leg-management`

Hand over the **design and the constraints**, not the order:

- The target structure after the edit, leg by leg.
- The credit or debit you are willing to accept (a floor for a credit, a cap for a debit).
- Whether the edit must be atomic or can be legged, and the maximum time the legging may take.
- The fill-quality constraint: if the structure order is unavailable, what is the acceptable slippage versus a leg-by-leg sequence.

### To `options-risk-engineer`

Hand over the **calendar and risk facts**:

- The resulting expiries and strikes, so the DTE calendar and aggregate Greeks can be updated.
- The new max loss in dollars.
- Any change to assignment or pin exposure near the new expiry.
- Whether the edit consumes additional buying power, so the capital floor can be re-checked.

### To `trade-sizing-recovery`

Hand over the **arithmetic inputs** and take back the verdict:

- The resulting structure's width, credit/debit and contract count.
- The band that applies to this name at the new DTE.
- The returned verdict: inside band / outside band, and the max loss that follows.

This skill never invents a band and never modifies one.

## Anti-patterns

| ❌ | ✅ |
|----|-----|
| Rolling to fix a broken thesis | CUT. A roll buys time, not a level |
| Rolling out and down for a credit without recomputing the break-even | Compute both break-evens; if the new one is worse, refuse |
| A third roll | Two is the cap. The third is a schedule hiding a loss |
| Converting to hide a loss by selling more premium | That is an ADD to a loser; refused at rung 3 |
| Rolling on the day of an event "to see what happens" | Events are priced before the edit, not after |
| Legging into a roll with no plan | Hand the sequence to `options-leg-management` before starting |
| Leaving the old brackets live after the roll | Replace and re-price in the same action |
| Rolling a 0DTE position | There is nothing to roll; the position is decided and executed same session |

## Provenance

- The credit-or-flat convention, the two-roll cap and the "don't repair a broken thesis" rule are standard practice in disciplined options management [COMMON-PRACTICE], stated here as a routing spec so that two people on the same desk reach the same answer.
- All dollar figures in the worked examples are `[COMPUTED]` from the stated widths, credits and contract counts, and are reproducible by hand.
- Strategy margin treatment of rolled and converted structures follows published exchange margin material [VERIFIED] Cboe margin manual; requirements for listed option positions are set by the relevant regulator [VERIFIED] FINRA Rule 4210; the schedules your broker actually applies differ and should be read directly and tagged `[BROKER-VERIFIED]`.
- Assignment, expiration and exercise-by-exception behaviour near expiry is governed by the clearing house [VERIFIED] OCC expiration processing.
- Past performance is not a guarantee. A roll that was right last month is evidence about a process, not a forecast about a price.
