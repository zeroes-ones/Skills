# Trim and Scale-Out Ladder

A trim is the action that turns an unrealized gain into cash without closing a position you still want to own. It is also the action most likely to be executed badly, for two reasons: equity positions come in whole shares, and shares come in **lots** — and the lot you sell is not a bookkeeping detail, it is a different decision with a different tax outcome.

**Portability target:** spec-level. This file owns the *shape* of the ladder and the decision. The lot choice and the tax arithmetic belong to `equity-tax-lot-and-exit-management`.

## Trigger and precondition

- **Trigger:** the position reaches a plan rung that was defined before the rung was reached, with the level intact.
- **Precondition:** a ladder exists, and a rule exists for whatever remains after each rung. A trim that leaves a runner with no rule is half a plan.
- **Not a precondition:** the position being up a particular percentage. Rungs come from the plan, and the plan came from the sizing owner.

## The whole-share rule

Shares do not divide the way options contracts do. A 900-share position trims cleanly in thirds (300 / 300 / 300); a 1,000-share position does not (333.33 each). The rule is therefore:

1. **Prefer rungs that divide into whole shares.** 900, 1,200, 1,500 shares are ladder-friendly; 1,000 is not.
2. **If the rungs will not divide, trim the whole rung and re-decide the remainder** — do not approximate. A 333-share trim with 1 share of rounding is a real order with a real fill, and the rounding was never a decision.
3. **Never trim a fraction of a share as if it were a fraction of a position.** Fractional-share facilities exist; they are not a licence to make the ladder meaningless.

Why this matters more than it sounds: a trim executed at an arbitrary size is not a rung, it is a sale. Sales have their own tax and behavioural consequences, and the ladder stops being a plan the moment its rungs become approximate.

## The thirds ladder

The default shape, for a position with no other plan:

| Rung | Fraction | Purpose | What remains |
|---|---|---|---|
| 1 | 1/3 of units | Book the first profit; the position must stop being purely theoretical | 2/3 running, with a written rule |
| 2 | 1/3 of the original | Confirm the position has done what it was bought to do | 1/3 running, with a trail |
| 3 | Remainder or an explicit trail | Let the third rung decide itself | Nothing held without a rule |

Two rules make the ladder work:

- **Each rung has a written rule for the remainder.** The most common failure is that rung 1 is executed and the runner is then managed by attention.
- **The ladder is defined before rung 1 is reached.** A ladder invented at rung 1 is a rationalisation of what already happened.

## Worked arithmetic

A 900-share position at $48.00, basis $35.00.

| Rung | Shares | Price | Proceeds | Formula |
|---|---|---|---|---|
| 1 | 300 | $48.00 | **$14,400** | 300 × 48.00 = 14,400 [COMPUTED] |
| 2 | 300 | $54.00 | **$16,200** | 300 × 54.00 = 16,200 [COMPUTED] |
| 3 | 300 | trail from $58.00 | rule-dependent | — |

Remaining exposure after rung 1: 600 shares = **$28,800** at $48.00 [COMPUTED]: 600 × 48.00 = 28,800.

The realised gain at rung 1, against a $35.00 basis: **$3,900** [COMPUTED]: 300 × ($48.00 − $35.00) = 300 × 13.00 = 3,900.

That $3,900 is the number that engages the tax owner: at a 23.8% long-term rate the tax is **$928** [COMPUTED]: 3,900 × 0.238; at a 40.8% short-term rate it is **$1,591** [COMPUTED]: 3,900 × 0.408. Rates per [VERIFIED] — IRC §1(h) and §1411. Substitute your own bracket; the point is that the trim's *tax* is a function of *which lots* are sold, which is why the lot decision is not made here.

## The lot interaction — the part this file refuses to decide

Selling 300 shares of a 900-share position built from three lots of 300 is unambiguous. Selling 300 shares of a 1,000-share position built from nine lots is nine different decisions:

- Which lots are sold determines the realised gain, and therefore the tax.
- Which lots are sold determines whether a **wash-sale** window is opened in the name: a loss realised on the sold lot starts a 61-day window, 30 days before through 30 days after, and replacement shares inherit the old holding period [VERIFIED — IRC §1091, §1223(3)].
- Which lots are sold determines whether remaining shares are near a **long-term anniversary**. The holding period begins the day after the buy trade date and ends on the sale trade date, so the earliest long-term sale is buy date + 1 year + 1 day [VERIFIED — IRC §1222, IRS Pub 550].
- Which lots are sold can interact with a qualified-dividend holding window: 61 days inside the 121-day period beginning 60 days before the ex-date [VERIFIED — IRC §1(h)(11), §246(c)].

**This skill names the interaction and stops.** The instruction to give the tax owner is: *"rung N of the ladder, executed at price P, N shares, on date D — choose the lots."* That is a complete instruction; "sell 300 shares" is not.

## Ladders that are not thirds

The thirds ladder is a default, not a law. Two variants worth knowing:

| Variant | Shape | Best for | Risk |
|---|---|---|---|
| **Front-loaded** | 50% / 30% / 20% | A position whose thesis is already fully expressed at rung 1, in a name you would not re-buy | Gives up the runner; if the name doubles you will remember it |
| **Back-loaded** | 20% / 30% / 50% | A position whose thesis is genuinely long-duration, in a regime that supports it | Keeps most of the exposure through the drawdown that would have funded rung 1 |

Both variants still require a written rule for the remainder, and both still require the ladder to be defined before rung 1.

## Trimming into strength, never into a gap

A trim is a sale by another name, so the same execution discipline applies as to a cut:

- **Do not trim into the opening print after a gap.** The opening minutes are the worst liquidity of the session.
- **Trim into strength on a normal session.** Rungs are price-and-time conditions; you are not obliged to execute on the first tick that touches the rung.
- **Accept a partial fill.** A rung that fills in two pieces is still the rung.

## Re-entry of trimmed shares

A trimmed name often drops afterwards, and the temptation to re-buy arrives fast. Two rules:

1. **Re-entry is a new position.** It needs a thesis, a level, a size inside the band, and a date — the same contract a fresh buy would need.
2. **The wash-sale flag applies if the trim realised a loss.** If the rung was executed below basis, a repurchase inside 61 days is inside the window. Freeze the name.

The most expensive version of this pattern is: trim at rung 1, watch the price fall, re-buy bigger, and then own a position that is larger than the one the plan allowed, at a worse average than the original.

## Recording a trim

```text
action:           TRIM
rung:             1 of 3
shares_before:    900
shares_after:     600
price:            48.00
proceeds:         14,400        [COMPUTED] 300 × 48.00
gain_realised:     3,900        [COMPUTED] 300 × (48.00 − 35.00)
lots:             equity-tax-lot-and-exit-management — instruction issued, not decided here
lot_instruction:  "rung 1, 300 sh, at 48.00, on 2026-10-20 — choose the lots"
remainder_rule:   rung 2 at 54.00, or the trail from 58.00 if rung 2 is not reached
wash_sale_flag:   no loss realised in this name; window not opened
expectation:      "the remainder reaches rung 2 or the trail fires"
grade_on:         the next review date
```

## Failure modes

1. **The fractional trim.** Countermeasure: the whole-share rule, and the ladder is chosen with divisibility in mind from the start.
2. **Rung 1 executed, remainder unmanaged.** Countermeasure: each rung names the rule for what remains.
3. **The ladder invented at rung 1.** Countermeasure: rungs come from the plan that existed before the rung.
4. **The trim that realises a loss without a wash-sale flag.** Countermeasure: the loss case is checked before the order, not after.
5. **Lot choice delegated to a default the holder does not understand.** Countermeasure: the instruction to the tax owner names rung, size, price and date.
6. **Trimming into a gap because "the rung was hit".** Countermeasure: rungs are conditions, not triggers to sell at any price.
7. **Selling winners to fund a loser elsewhere.** That is the disposition error the whole skill exists to prevent; route it to the router, not the ladder.
8. **The trim that leaves a position that cannot be trimmed again.** If the remainder is smaller than one whole rung, decide once: close it or commit to holding it with a rule. A position too small to trim is a position too small to manage.
