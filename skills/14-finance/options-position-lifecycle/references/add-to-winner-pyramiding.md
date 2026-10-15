# Adding to a Winner — Pyramiding

Adding to a position is the only action in this router that *increases* risk. That single fact justifies a stricter gate than anything else in the skill: five preconditions, all of them mechanical, none of them negotiable. This reference defines the rungs, the re-underwrite, the arithmetic, and the version of "add" that is actually a forbidden average-down wearing a friendlier name.

## The one-line rule

> You may add to a position that has already **paid you something**, that is still inside its band after the add, and whose thesis you have re-underwritten from scratch in writing. Anything else is not an add.

## Rung definitions

Rungs are the position's own milestones. They come from the take-profit ladder, and they are what makes "paid you something" a fact rather than a feeling.

| Rung | Definition | What it entitles you to |
|------|------------|-------------------------|
| Rung 0 | Position open, nothing booked | Nothing. No add. No exception |
| Rung 1 | First trim executed (typically 1/3 of units) | Consider an ADD, subject to the five preconditions |
| Rung 2 | Second trim executed | Consider a *second* ADD, subject to the same five preconditions plus a band check on the enlarged position |
| Runner | Remainder with a written trailing rule | No further adds. The runner is the tail; you do not add to a tail |

The **trim comes before the add**, always. This ordering is the whole trick: the booked profit is what makes the added risk financed rather than borrowed. An add on a rung-0 position is a size increase justified by an unrealised number, which is exactly the pattern this skill exists to prevent.

## The five preconditions

### 1. The structure is at or above rung 1

Check the ledger, not your memory. "It's up a lot" is not a rung; a booked trim is a rung.

### 2. The underlying is at a fresh level test

Fresh means **a different structural moment from the one the original position was based on**. Examples:

- Original position opened on a break of resistance at 112; the stock has run to 130 and pulled back to retest 112 from above → not fresh, it is the same level.
- Original position opened at 112; the stock consolidates at 130 for three weeks and now breaks 130 → fresh.
- Original position opened on a trendline; the stock builds a higher base and breaks a new swing high → fresh.

Why it matters: a level test is a decision point. Adding mid-trend without a decision point is adding at a moment with no defined invalidation nearby, which makes the new contracts un-stoppable.

### 3. The thesis has been re-underwritten in writing

Re-underwrite means: state the reason to own it *today*, as if the position did not exist and you were considering it fresh. If the re-underwrite reads like a justification of the existing position, the add is refused. A useful test: would a colleague reading the paragraph, knowing nothing about the position, think it described a good trade? If the paragraph mentions the existing position's P&L, it fails.

### 4. Blended cost and buying-power impact are recomputed

Never estimate. See the arithmetic section below.

### 5. The add leaves the structure inside its band

The enlarged position's **max loss** must be ≤ the band for this name. This is the hard stop, and it is deliberately the last check because it is the one people argue with. The band is not a suggestion about the original trade; it is a property of the account.

If the add breaches the band, the add is refused, and the correct action is usually TRIM (book more of the existing position) rather than ADD.

## The arithmetic

Three numbers are required before an add is taken. All three are `[COMPUTED]` from the position's own inputs.

### Blended cost

```text
blended_cost = (contracts_1 x cost_1 + contracts_2 x cost_2) / (contracts_1 + contracts_2)
```

Worked example — a debit vertical:

```text
leg 1: 2 spreads at $1.80  = $360
leg 2: 1 spread  at $3.30  = $330
blended_cost = ($360 + $330) / 3 = $230 per spread   [COMPUTED]
```

### New break-even

For a spread, break-even on the underlying is the short strike adjusted by the blended cost:

```text
breakeven (call debit spread) = long_strike + blended_cost
breakeven (put  debit spread) = long_strike - blended_cost
```

```text
leg 1 opened with a $100 long strike and $1.80 cost    -> breakeven 101.80
add executed at $3 marks the blended cost at $2.30    -> breakeven 102.30
```

The add **moved the break-even against you by $0.50** even though the position is winning. That is not an argument against adding; it is an argument for *knowing* it. An add to a winner always worsens the blended break-even; the compensation is that the position is closer to the target.

### New max loss, against the band

```text
max_loss = contracts_total x blended_debit x 100               [for a DEBIT spread]
max_loss = contracts_total x (width - net_credit_blended) x 100 [for a CREDIT spread]
```

> **Debit and credit are not the same formula, and the subtraction is the tell.** A credit structure's worst case is the width it must pay out minus the credit it already took in: `width − credit`. A debit structure's worst case is simply the debit it paid — the width caps the *profit*, not the loss, so `width − debit` is the maximum **profit** by construction. The two expressions coincide only when the debit happens to be half the width: below that the credit formula overstates the risk, above it understates it, and in both cases it is answering the wrong question. Credit structures keep `width − credit`; debit structures use the debit paid.

```text
3 spreads, width $5, blended debit $2.30
max_loss = 3 x $2.30 x 100 = 3 x $230 = $690   [COMPUTED]
max_profit (not the risk) = 3 x ($5.00 - $2.30) x 100 = $810
```

Then compare to the band. If the band for this name at this DTE is, say, $600, the third spread is refused even though it is "financed" by a winner.

### Position-level capital check

Also check with `options-risk-engineer`:

- Buying power consumed by the enlarged position.
- Aggregate Greek change (the add almost always increases delta exposure more than it appears to).
- Whether the enlarged position changes the pin or assignment profile near expiry.
- Whether the name's total exposure across structures is now over its allocation.

## Choosing what to add

When the gate passes, the *shape* of the add still matters:

| Add shapes | When it is reasonable | Where it goes wrong |
|------------|----------------------|---------------------|
| Same structure, same strikes, later expiry (roll the winner forward) | The thesis is slow and DTE headroom is short | Paying up in extrinsic for time you may not need |
| Same structure, strikes rolled to the new level test | The level moved and the structure should move with it | Creating an accidental diagonal if only one leg moves |
| Same structure, larger width (up-sizing the spread) | More room for the thesis with proportional risk | Max loss grows faster than the credit does |
| Different structure expressing the same fresh level | The original structure's payoff no longer fits | Turns an add into a second, unmanaged position |

Rule of thumb: **the add should look like the position, aimed at the new level.** If it does not, it is a new trade, and new trades go through `options-strategist` and `trade-sizing-recovery` from the start.

## Forbidden versions

Each of these is called an "add" by the person doing it and is refused by this skill.

1. **Adding to a rung-0 position because it is "working".** Unrealised profit is not a rung. Book first, then add.
2. **Adding to a loser to improve the average.** That is average-down; the only legal form is the defined-risk restructure gate.
3. **Adding at the same level the position was opened at.** No fresh decision point, no defined invalidation, un-stoppable contracts.
4. **Adding to "use up" the remaining buying power.** Buying power is not a deadline.
5. **Adding because the last three adds worked.** The number of consecutive wins is not an input to this gate; the five preconditions are.
6. **Adding into an event window.** If an earnings print or a macro decision sits inside the window, the add waits. This is a size-zero condition, not a judgement call.
7. **Adding after a trim of a *different* position.** Rungs are per position. Profit booked elsewhere does not entitle this name to more risk.
8. **Adding with the intention of trimming back "if it goes wrong".** That is not a plan; it is a hope with an exit clause written in the passive voice.

## Add-versus-trim: the common confusion

It is a common instinct to respond to strength by adding. The router says something different:

```text
Position is at rung 1 with the underlying at a fresh level test
├─ Are the five preconditions all satisfied?
│   ├─ NO  → TRIM on the existing ladder. Book profit; do not increase risk.
│   └─ YES → ADD, sized so that total max loss stays inside the band
└─ Either way: re-run the 7-step health check on the resulting position today
```

Note the asymmetry: trimming is the default response to strength, and adding is the exception that must pass a gate. That asymmetry is deliberate. Trimming is reversible in effect (you can add later, on a fresh decision); an add is not, because it changes the position you will be managing.

## Worked full example

```text
Setting: call debit spread on a name at 118, opened 25 days ago.

Original trade
  long 120 call, short 125 call, 2 spreads, debit $1.80  = $360 total
  max loss $360 (the debit paid); band for this name = $600
  width $5.00 -> max profit per spread = $5.00 - $1.80 = $3.20  [COMPUTED]
  rung 1 = $1.80 + (0.50 x $3.20) = $3.40   [COMPUTED -- debit-vertical row]
  rung 2 = $1.80 + (0.75 x $3.20) = $4.20   [COMPUTED -- same row]
  invalidation: closing basis under 114

Review at day 25 (today)
  underlying now 131, testing 131 after consolidating 128-131 for two weeks
  mark $3.40  -> 1.89x cost -> the debit-vertical TP rung 1 ($3.40) reached -> TRIM
  TRIM: sell 1 of the 2 spreads at $3.40  -> books $160 profit  [COMPUTED:
    (3.40 - 1.80) x 100] on that spread
  remaining: 1 spread, rung 1 achieved

ADD evaluation
  preconditions
    1 rung 1 achieved .................................... PASS (1 spread trimmed)
    2 fresh level test: the 128-131 base is a new structure, not the
      original level ..................................... PASS
    3 re-underwrite: written from scratch, no mention of P&L .. PASS
    4 blended cost: ($180 + $340) / 2 = $260  [COMPUTED] ..... computed
    5 band: 2 spreads x $2.60 blended debit x 100 = $520  [COMPUTED]
      $520 <= $600 ..................................... PASS
  decision: ADD 1 spread at $3.40, rolling the strikes up to 133/138

Resulting position
  2 spreads, blended cost $2.60, max loss $520
    [COMPUTED: 2 x $2.60 x 100 -- a debit spread's max loss is the debit paid],
    new breakeven 135.60 = 133.00 long strike + $2.60  [COMPUTED]
  invalidation restated: closing basis under 130 (the base)
  new rungs: 1/3-equivalents do not apply at 2 units -> next trim closes 1 unit
              at the same row's rung 2 on the rolled structure:
              $2.60 + (0.75 x ($5.00 - $2.60)) = $4.40  [COMPUTED]
  grade on: the date the invalidation is next tested, or 45 DTE, whichever first

What would have failed the gate
  - if the band were $400, the add is refused and the action is TRIM (sell the
    second spread and be done)
  - if the stock were merely retesting the original 118 level, precondition 2
    fails and the action is TRIM
  - if earnings were inside the window, the add waits
```

## Post-add obligations

1. **Re-run the seven-step health check today.** The position is new; step 2 in particular must be re-verified because the strikes moved.
2. **Rewrite the exit contract**: new level, new rungs, new improve-by date, refreshed event list.
3. **Record the add in the review log** with its expectation and a grading date — an add is an action above HOLD and R8 applies to it.
4. **Tell the book.** `options-risk-engineer` needs the new exposure, and `portfolio-signal-manager` needs to know the name's weight changed.

## Failure modes of pyramiding

| Failure mode | What goes wrong | Countermeasure |
|--------------|-----------------|----------------|
| The gate is applied to the story, not the ledger | "It's basically at rung 1" — no trim was ever booked | Rung is read from the record; no record, no rung |
| Band check done on the original size | Max loss recomputed for the *original* contracts, not the enlarged position | Always multiply by the *total* contract count, every time |
| The fresh level is fresh-looking | A pullback to a level visited weeks ago is called a new test | Name the previous structure and confirm it is different |
| Add size chosen by "how much can I afford" | Buying power becomes the sizing input | Size from the band, then check buying power — never the reverse |
| Add executed but the brackets are not updated | The attached TP/SL still reflects the old structure and size | Post-add obligations are part of the action, not a follow-up |
| The add is forgotten in the aggregate | Portfolio Greeks and exposure quietly change shape | Every add is reported downstream on the same session |

## Provenance

- The rung-before-add ordering and the band check follow the sizing doctrine of `trade-sizing-recovery` and are stated here as the position-management side of the same rule [COMMON-PRACTICE].
- The arithmetic shown is deterministic and reproducible from the position's own debit, credit and width; every figure is marked `[COMPUTED]`.
- Band percentages and the structure-family rungs are operating conventions derived from the shape of the payoff rather than measured constants [ESTIMATED], and they are owned by `trade-sizing-recovery`'s Canonical Threshold Table — this reference states the add gate, not the levels. Past performance is not a guarantee of future results, and a gate that passes is a permission, not a prediction.
- Margin and assignment consequences of an enlarged position are not computed here; they belong to `options-risk-engineer` and to your broker's published margin schedule, which you should read directly and tag `[BROKER-VERIFIED]`.
