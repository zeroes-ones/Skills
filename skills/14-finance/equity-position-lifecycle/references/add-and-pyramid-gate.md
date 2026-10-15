# Add and Pyramid Gate

Adding to a position that is already working is the least understood action in an equity book. It is not the same action as averaging down with a happy sign, and it is not a reward for a stock having gone up. It is a **new entry in the same name**, with a new entry's obligations, executed against a position that already carries risk.

**Portability target:** spec-level. All numbers are supplied by the sizing owner; this file owns the decision and its preconditions.

## The five preconditions

All five, in writing, or the add does not happen.

| # | Precondition | What "pass" looks like | Who owns the number |
|---|---|---|---|
| 1 | Already above rung 1 | The position has banked at least the first plan rung | Plan rungs from the sizing/plan owner |
| 2 | A fresh level test | Price is at a level that means something — support, a prior breakout, a moving average the plan named | `technical-signals-engineer` |
| 3 | Thesis re-underwritten **at the higher price** | A written sentence that is about the business, not about the chart | `fundamental-analyst` |
| 4 | Blended cost and blended break-even recomputed | Both numbers on the page, before the order | Sizing owner |
| 5 | Enlarged position **inside the per-idea band** | The post-add percentage of the book is shown, with its arithmetic | `portfolio-signal-manager` |

Precondition 3 is the one that gets skipped, and it is the one that matters. A thesis that was underwritten at $80 is not automatically a thesis at $110. If the re-underwrite does not produce a *new* invalidation level for the enlarged position, it did not happen.

## The gate supplied by the trading engine

The library's algorithmic-trading skill publishes a pyramid gate; this skill defers to it rather than restating it in its own numbers. Its preconditions are: the position must be a **confirmed winner** (gain above 5% of entry), the add must have **volume confirmation**, the add must be on a **pullback to support rather than at highs**, **trend structure intact**, the add **no larger than 50% of the original size**, **only one pyramid add per position**, and the **blended stop after the add tighter than the original** [VERIFIED — the pyramid gate published in `algorithmic-trader` SKILL.md, rule R13]. The **10%-of-NAV cap** on the enlarged position is *not* part of R13; it is the portfolio constraint published separately in `algorithmic-trader/references/core-workflow.md` — "Max single position: 10% of NAV (absolute hard cap)", restated there as "Total position never exceeds 10% NAV" [VERIFIED — `algorithmic-trader/references/core-workflow.md`].

Read that list against the five preconditions above and the overlap is deliberate: the engine's version is expressed in measurable fields, and this file's version is expressed in decisions. Where they disagree, the stricter one wins.

## The forbidden versions

| Forbidden | Why it fails | What it looks like in the record |
|---|---|---|
| The add at all-time highs with no level under it | There is no level to invalidate against, so the enlarged position has no stop | "add on strength" with no price written |
| The second and third add | The gate is one add per position; more than one is a position build-out disguised as pyramiding | two or more add rows on the same name |
| The add sized by conviction | Size is a formula with caps, never a feeling about the name | no sizing method named |
| The add that breaches the band | The moment a position becomes oversized is not permitted to be an add's side effect | post-add percentage above the cap |
| The add to a position whose level just broke | That is not an add, it is an average down with worse timing | level breached on the close in the same review |

## Worked arithmetic

A winner above rung 1, at $66.00, 500 shares, basis $60.00.

- Position value: **$33,000** [COMPUTED]: 500 sh × $66.00 = 33,000.
- Unrealized gain: **$3,000** [COMPUTED]: 500 × ($66.00 − $60.00) = 500 × $6.00 = 3,000. Against the original cost of 500 × $60.00 = **$30,000** [COMPUTED], that gain is **10.0% of basis** [COMPUTED]: 3,000 ÷ 30,000 = 10.0%. Against the position's current value of **$33,000** [COMPUTED], the same gain is **9.1% of current value** [COMPUTED]: 3,000 ÷ 33,000 = 9.1%. Label which denominator you are quoting — an unqualified "gain %" is two different numbers.
- Permitted add size, per the engine's cap of 50% of the original: 250 shares [COMPUTED]: 500 × 0.50 = 250.
- Blended basis after adding 250 shares at $66.00: **$62.00** [COMPUTED]: (30,000 + 16,500) ÷ 750 = 62.00.

The blended basis moves up whenever the add is above the original basis. That is the arithmetic cost of pyramiding, and it should be stated before the order rather than discovered after it.

## The band check, in dollars

The per-idea band is 10% of the book and no sector above 25% [VERIFIED — the caps published in `portfolio-signal-manager`].

On a $250,000 account the band is $25,000:

- Before the add: $33,000, which is **13.2%** of the book [COMPUTED]: 33,000 ÷ 250,000 = 13.2%.
- The position is already **$8,000 over** the band [COMPUTED]: 33,000 − 25,000 = 8,000.
- The add is therefore **barred**, not because the trade is unattractive, but because the position was already oversized when the question was asked.

This is the most common real outcome of the gate, and it is not a failure of the gate. It is the gate finding a pre-existing problem one decision earlier than it would otherwise have appeared.

## Worked walkthrough

```text
Position: 500 sh, basis 60.00, now 66.00, above rung 1

Precondition 1  above rung 1 ............................ PASS (rung 1 banked 3 weeks ago)
Precondition 2  fresh level test ........................ PASS (retest of the 64.80 breakout level)
Precondition 3  thesis re-underwritten at 66.00 ........ PASS (written; new invalidation 61.50)
Precondition 4  blended basis ........................... 62.00 [COMPUTED]
Precondition 5  band after the add ...................... FAIL
                 post-add value 250 × 66.00 = 16,500
                 position after 33,000 + 16,500 = 49,500
                 49,500 ÷ 250,000 = 19.8% against a 10% band [COMPUTED]

Result: ADD refused at precondition 5. Queued: the trim that
        would bring the position back inside the band, taken first.
```

The record matters here. "Add refused on clause 5" is a finding about the book, and it feeds the next review; "we decided not to add" is not.

## Recording an add

```text
action:            ADD
preconditions:     1 PASS · 2 PASS · 3 PASS (written, dated) · 4 PASS · 5 PASS
shares_added:      250
basis_before:      60.00
basis_after:       62.00        [COMPUTED] (30,000 + 16,500) ÷ 750
position_pct:      13.2% → 19.8%   [COMPUTED]
new_invalidation:  61.50, written before the order
add_count:         1 of a maximum 1
expectation:       "the retested level holds and the position reaches rung 2"
grade_on:          the next review date, or the level, whichever comes first
```

## Failure modes

1. **The award add.** The add is a reward for the position being up, and no level under the add was identified. Countermeasure: precondition 2 is a level test, and the level is written in the record.
2. **The thesis that was never re-underwritten.** The same sentences are copied forward. Countermeasure: a new invalidation level for the enlarged position is the evidence that the re-underwrite happened.
3. **The band discovered after the fill.** Countermeasure: precondition 5 is computed before the order, with the arithmetic shown.
4. **Pyramiding a position that just had its level breached.** That is an average down — route to rung 7 and the five-clause gate.
5. **The blended break-even misread as a target.** A blended basis is a cost, not a forecast. Countermeasure: the target comes from the plan, not from the blend.
6. **The add count drifting.** Two or three adds on the same name, each individually reasonable. Countermeasure: one add per position, per the engine's published gate.
7. **The tax consequence of the new lot ignored.** The new lot's acquisition date and basis are different from the old ones. Countermeasure: flag the lot interaction to `equity-tax-lot-and-exit-management` before the order.
8. **The add funded by selling a winner elsewhere.** That is a rotation, and it is rung 3, not rung 6. Route it there.

## Exit conditions for the enlarged position

- **Complete when** the enlarged position has its own written invalidation level, distinct from the original position's level.
- **Complete when** the post-add band percentage is on the page with its arithmetic.
- **Complete when** the add count is recorded against a stated maximum.
- **Complete when** the expectation is falsifiable and has a grading date.
- **Complete when** the re-underwritten thesis is filed with the record, dated, so a later review can see what it claimed.
