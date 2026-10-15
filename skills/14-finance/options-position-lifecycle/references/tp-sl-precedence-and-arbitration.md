# TP/SL Precedence and Arbitration

Every options desk accumulates threshold conventions. None of them is universal, and the corpus this skill belongs to contains several at once: a credit spread closed at a fraction of its credit, a stop stated as a multiple of that same credit, a covered call bought back at a fraction of the strike width, a debit vertical taken at a multiple of its cost, a long premium position cut at a fraction of its debit — and a calendar that overrules all of them in the last two sessions. **This reference does not supply those numbers.** They belong to `trade-sizing-recovery`'s Canonical Threshold Table, which is their single owner and their tie-breaker. What this file supplies is the *order* in which the rules are consulted, and the arbitration record that results.

## The precedence order

Resolve top-down. **Stop at the first rule that applies.** Never average two thresholds; averaging produces a rule that belongs to no family and cannot be reasoned about later.

| Rank | Rule | Applies when | Owner |
|------|------|--------------|-------|
| 1 | **Desk circuit breaker** | A desk-level breaker condition is declared (correlated unwind, venue failure, extreme dislocation) | The desk's own written conditions |
| 2 | **Calendar / expiry force** | 0–2 DTE, live assignment or pin risk, margin call, expiration processing | `options-risk-engineer` |
| 3 | **Plan-level rung declared at entry** | The trade was opened with a named rung for its own family, and it is no *looser* than that family's loss cut | `trade-sizing-recovery` (the declared number) |
| 4 | **Structure-family threshold** | Nothing above applies | `trade-sizing-recovery` |
| 5 | **Risk-tightening adjustment** | Nothing above applies, and the change **reduces** exposure — an earlier or smaller exit only | The operator, with a grading date |

There is deliberately **no rank that loosens a threshold**. Rank 5 can only ever make the exit *more* conservative: it may cut earlier, trim more, or shrink the position, and it can never widen a rung, extend a deadline, or resurrect an exit that ranks 1–4 have already forced. A number invented after entry to *relax* a rule is a moving goalpost, not a rule — `trade-sizing-recovery` states the same in its own precedence rule, and this skill does not create an exception to it. Rank 5 changes never require a new number for the family row, only a written reason and the date on which the tightening is graded.

## Structure-family thresholds

These rows name **which family a position belongs to** and **why its exit has that shape**. The *values* are not here: every take-profit fraction, stop multiple and DTE force is owned by `trade-sizing-recovery`'s **Canonical Threshold Table**, which is the single tie-breaker for the corpus. Name the row, read it there, and never quote a number from memory — a figure recomputed from the position's own inputs is `[COMPUTED]`; a figure recalled is a defect.

| Structure family | Which row to read (owner: `trade-sizing-recovery`) | Why these shapes |
|------------------|--------------------------------------|------------------|
| Short premium, defined risk (credit spread, iron condor, butterfly) | Credit vertical; iron condor and iron butterfly have **separate rows with separate rung 1s** — a condor and a fly are not one family | A short-premium position collects most of its value early; the second half of the credit is paid for in tail risk. The stop caps the loss at a known multiple of the intended win |
| Debit vertical (call or put spread) | Debit vertical — stated as a share of **max profit**, with the backstop stated against the debit paid | The payoff is bounded, so the rung is a fraction of the profit the spread can still make, and the backstop is a fraction of the debit it cost; the winner must clear the debit by enough to matter |
| Long single option / LEAP | Long call / put; LEAPS / PMCC | Long premium has an unbounded upper tail and a fixed cost; scaling out converts the middle of the distribution into a booked win while keeping the tail |
| Short naked or covered call | CSP / covered call. For the covered call the row's preference is assignment-or-net-credit, not a premium multiple | The position is short gamma and short assignment risk; the stop must respect the event calendar and the stock leg, not just the P&L |
| Calendar / diagonal | Calendar / diagonal — stated against the **debit paid** | A calendar's net P&L hides which leg is doing the work; the rung belongs on the near leg's extrinsic, which is why the row is stated in debit rather than in % of max |
| Ratio structure (1:2, 2:3) | The defined-risk side's row, measured in the risk unit | The risk lives in the ratio, so the stop must be expressed in the width of the narrow spread, not in the net credit |

### Why the short-premium rung sits where it does

A credit position that has given back most of its maximum profit is being paid the remainder for a risk that has not shrunk with it. The tail is the same size; the reward is a fraction of what it was. Closing at the owner's rung converts a favourable risk/reward into a booked one and frees the capital for a fresh decision.

### Why the stop is stated in the same unit as the target

The stop is expressed in the same unit as the take-profit so that the reward-to-risk ratio is fixed by construction — and so that both numbers come from one row of one table. Moving the stop to a smaller multiple changes the trade's expectancy without changing its name; moving it *by hand, after entry*, is the moving-goalpost failure that `trade-sizing-recovery` names explicitly and that rank 5 below is written never to permit.

## Worked arbitration examples

### Example 1 — credit spread where TP, stop and calendar disagree

```text
Position: put credit spread, 1 contract
  credit received:      $1.20  = $120 total
  width:                $5.00 wide -> max loss $380 total
                        [COMPUTED: (5.00 - 1.20) x 100]
  family row:           trade-sizing-recovery -> credit vertical
  current mark:         $1.75 (debit to close)  -> unrealised -$55
  DTE:                  4
  short strike:         2% below spot, closing basis breached yesterday

Rules that apply:
  [family]  that row's TP rung 1 = buy back at $0.60
            [COMPUTED: 0.5 x $1.20]        -> not reached (mark is $1.75)
  [family]  the same row's credit-multiple stop = close at $2.40
            [COMPUTED: 2 x $1.20]          -> not reached
  [calendar] 4 DTE, short strike breached on the close = calendar force
  [thesis]  invalidation level breached            = rank 3 (plan rung) / ACT

Resolution: rank 3 (the declared level) outranks the family bands, and the calendar
force at rank 2 confirms it. The position is closed. The stop never fires because the
decision is not P&L-driven.
Loss booked: roughly $55 plus the exit spread  [COMPUTED] from the fill, not the mark.
```

The lesson: **the stop-loss was never the binding rule.** The level was. Traders who only have a stop watch a position pass through their mental stop and "give it room"; traders who have a level do not have that argument available.

### Example 2 — debit vertical with a plan rung

```text
Position: call debit spread, 3 contracts, $5.00 wide
  debit paid:           $1.80 = $180 per spread  -> $540 total
  family row:           trade-sizing-recovery -> debit vertical
  family TP rung 1:     50% of max profit = $1.80 + 0.5 x ($5.00 - $1.80)
                        = $3.40  [COMPUTED]
  declared at entry:    "take half at 2.00x, trail the rest"   <- plan-level rung
                        = $3.60  [COMPUTED: 2.00 x the $1.80 debit]
  current mark:         $3.05

Rules that apply:
  [family] the row's rung 1 = $3.40 -> not yet reached at the mark of $3.05
  [plan]   the declared rung = $3.60 -> not yet reached either

Resolution: both readings agree that nothing has fired, but the binding number
going forward is the declared rung at $3.60, not the family default at $3.40,
because rank 3 outranks rank 4. A rung declared at entry may sit *looser* than the
family's take-profit -- the constraint is that it may never sit looser than that
family's loss cut. The trade was taken accepting a lower hit rate for a larger
average win; that choice was recorded at entry, so it is the rule now.
```

**Caveat.** A plan-level rung overrides only when it was declared *at entry*. A rung invented mid-trade, after the family threshold has already been crossed, is **not** an override and cannot reopen the position: a post-entry change may only *tighten* — cut earlier, trim more, or shrink — and even that needs a written reason and a grading date. Loosening a threshold after entry is a moving goalpost, which is the failure `trade-sizing-recovery` names in its own precedence rule 2.

### Example 3 — covered call ahead of an ex-dividend date

```text
Position: 100 shares + 1 short call, 6 DTE
  call: short strike 2% OTM, currently ITM on the ask
  credit received:      $0.95 = $95
  family row:           trade-sizing-recovery -> CSP / covered call
  family stop:          3x credit = $2.85 to close  [COMPUTED: 3 x $0.95]
                        (for a covered call the row's first preference is
                         assignment, or an up-and-out roll for a net credit
                         of at least $0.05; the credit-multiple stop is the CSP leg)
  current ask:          $2.10  -> below the credit multiple, so the premium band has
                        NOT fired -- and it is not the rule that decides this position
  event:                ex-dividend in 3 sessions; the dividend exceeds the remaining
                        extrinsic, which is the classic early-assignment setup

Resolution: rank 2 (calendar force) applies before rank 4, and here rank 4 was never
breached in the first place. The decision is not "the stop has not fired, so hold" --
it is "assignment is likely and imminent; decide the stock leg now". Two valid outcomes:
  (a) close the call and keep the shares, paying ~$2.10 versus the $0.95 collected;
  (b) accept assignment and write the stock leg's exit contract before the shares land.
What is NOT valid: holding by default because the premium band is quiet. The event, not
the P&L, is the question that has to be answered today.
```

### Example 4 — long single where the level and the debit band conflict

```text
Position: long call, 20 DTE, debit paid $4.00 per contract = $400
  family row:  trade-sizing-recovery -> long call / put
  family cut:  the row's premium backstop, 40% of the debit
               -> close at $2.40 (a $160 loss)  [COMPUTED: 0.40 x $4.00]
  declared level: "close below 118" -- the level is at a price that implies a
                  $0.90 option mark (a $310 loss)

Rules that apply:
  [family] debit backstop at $2.40
  [rank 3] the declared level

Resolution: rank 3 applies, BUT the level's implied loss ($310) is far outside the
family backstop ($160). That is a conflict between two rules that BOTH have standing,
and it is resolved by the tighter one: the family backstop binds at $2.40, because the
plan's level was set at a distance the position size never justified and a rank-3 rung
may never be looser than its family's loss cut. Record the mismatch and fix the entry
process: the level and the backstop must imply losses of the same order.
```

This fourth case is the one worth internalising. A level that implies a loss several times the size band is not a stop; it is a hope with a price attached.

## The arbitration record

Every conflict produces a record. The record is what makes the precedence table improvable.

```text
conflict:        <short description>
rules_standing:  <rank 3 level at 118 | rank 4 family band at $2.40>
winner:          <rank and rule>
reason:          <one or two sentences>
loser_note:      <what the loser would have done, and why it lost>
graded_on:       <date>
outcome:         <at plan | worse than plan | better than plan>
lesson:          <one line>
```

After a month of records, look for a pattern: if a family threshold keeps losing to a level, either the level should become the default for that family, or the level is being set badly at entry. The record tells you which.

## Circuit breakers

A circuit breaker is the one rule that overrides everything, which means it has to be defined before it is needed. It is not "I feel bad about the book." A usable breaker has:

- **A named condition**, observable and unambiguous (for example: two consecutive sessions where realised volatility on the underlying is above a stated level, or the venue's market status is abnormal, or a correlated group of positions all breach their stops in one session).
- **A named action** — flatten to a stated risk limit, or reduce-only, or no new risk.
- **A named exit condition** — what has to be true for the breaker to come off.
- **A named owner** — who declares it, and whether they can declare it unilaterally.

A breaker without all four of these is a mood, and a mood that overrides a stop is worse than no breaker at all.

## Precedence anti-patterns

| ❌ | ✅ |
|----|-----|
| Averaging two thresholds ("let's split the difference at 1.5×") | Apply the precedence table; the answer is one of the two, not the midpoint |
| Using the family threshold as the only rule and never declaring a level | A level is step 1 of the health check; a position without one cannot reach ACT on its merits |
| Declaring a plan rung after the family threshold was hit | That is not a rank-3 rung and not an override; a post-entry change may only *tighten* risk, and it must be written down and graded |
| Treating the calendar force as an excuse to ignore the level | Rank 2 fires *first*; the level's failure is still recorded and still escalates |
| Letting the breaker become a permanent "risk-off" state | Breakers have exit conditions; without one you have a regime, not a breaker |

## Where the numbers come from

- **The threshold values are not in this file.** Every fraction, multiple and DTE force lives in `trade-sizing-recovery`'s Canonical Threshold Table; name the row, read it there. Those rows are conventions derived from the shape of each payoff and calibrated against the loss bands, not measured constants [ESTIMATED] — which is exactly why they are owned in one place instead of restated in every skill that uses them.
- The worked arithmetic in this reference is deterministic: every figure is reproducible from the position's own credit, debit and width, and is marked `[COMPUTED]`.
- Wing-width and spread-margin conventions trace to the published strategy-based margin material of the options exchanges [VERIFIED] Cboe margin manual; the rules of the clearing house govern expiration and exercise-by-exception [VERIFIED] OCC expiration processing.
- Expiry-day timing conventions (the 15:45 ET decision deadline) reflect how closing-auction handling and late-day liquidity actually behave; verify against your venue's session schedule, which changes on half-days.
- Past performance is not a guarantee. A threshold that produced a good average last quarter can still be the wrong threshold for the structure in front of you today.
