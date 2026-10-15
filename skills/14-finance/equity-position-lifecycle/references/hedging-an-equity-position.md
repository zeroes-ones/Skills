# Hedging an Equity Position

A hedge protects a position you do not want to sell. It is a real action with a real cost, and it is frequently proposed for the wrong reason — as a way of *not deciding*. This file decides **whether** to hedge. It never chooses the structure.

**Portability target:** spec-level. Structure selection, strikes and expiries belong to `options-strategist` (and `advanced-options-structures` for non-standard combinations). Premium and sizing arithmetic belong to `trade-sizing-recovery`.

## When a hedge is the right rung

A hedge is **rung 4** of the action router. It fires only when all three are true:

1. **The thesis is intact** at the level. If the level broke, the route is CUT — a hedge on a broken thesis is a broken thesis with an extra leg and an extra cost.
2. **The tax clock argues against realizing now** — typically the long-term anniversary is close enough that the rate difference is worth structuring around, and no higher rung has fired.
3. **A defined structure exists** that protects the position without selling it, and its cost is acceptable against the risk it removes.

If any of the three fails, the hedge is not the answer. In particular, a hedge is **never** a substitute for the decision that rung 2 requires.

## The forbidden versions

| Forbidden | Why it fails |
|---|---|
| "I'll hedge instead of deciding" | The decision was already required by rung 2; hedging delays execution, it does not defer the level |
| "The hedge makes it risk-free" | Every equity hedge has a floor: a put's protection is bounded by its strike, a collar's by the short call, and both cost money |
| "I'll collar it and forget it" | A collar caps the upside, and the cap is a decision about the same position |
| "I'll write calls against the whole position" | Contract granularity means 100 shares per contract; a 300-share position is at most one-third covered by one contract |
| "The hedge is tax-neutral" | Hedging interacts with the holding-period rules. The rule is owned by `equity-tax-lot-and-exit-management` and is **flagged before the order**, never assumed |

## Granularity: the 100-share problem

Equity options deliver in units of 100 shares. That single fact reshapes every hedging decision:

- A **500-share** position can be hedged in 100-share increments: 1, 2, 3, 4 or 5 contracts. Partial protection is available and its fraction is exact.
- A **250-share** position can be hedged by at most 2 contracts (200 shares), leaving 50 shares uncovered. There is no way to protect the last 50 shares with a standard contract.
- A **90-share** position **cannot be hedged at all** with standard listed contracts, no matter how strong the thesis.

This means the hedge ratio is not a free parameter. It is a whole number of contracts divided by the share count, and the residual is exposure you are accepting by construction. Write the residual down: *"2 contracts cover 200 of 250 shares; 50 shares uncovered."*

## Cost arithmetic

A hedge's cost is what it removes from the position's future, expressed as a percentage of the protection it buys.

- **Protective put.** Cost = premium plus the exit spread you will pay on the put itself. The position pays this whether or not the protection is used.
- **Collar.** Cost or credit = put premium less call premium received. A credit collar is not free: the credit is the price of the capped upside.
- **Covered call against part of the position.** Credit received, and upside above the strike given away — plus the tax interaction flag.

A useful comparison, stated in the same units every time:

```text
protection_cost_as_pct_of_position    = hedge_cost ÷ position_value
protection_floor_as_pct_of_position   = (strike − current_price) ÷ current_price
break_even_move_needed_for_the_hedge_to_pay_for_itself
```

The third line is the one that decides most cases: a hedge that only pays for itself if the stock falls more than it has fallen in the last two years is not protection, it is a bet.

## Worked shape, with the numbers labelled

A 300-share position at $60.00, basis $52.00, thesis intact, anniversary 25 sessions away.

| Item | Value | Formula / owner |
|---|---|---|
| Position value | **$18,000** | 300 × 60.00 = 18,000 [COMPUTED] |
| Contract granularity | 3 contracts maximum | 300 ÷ 100 = 3 [COMPUTED] |
| Partial hedge — 1 contract | 100 shares, 33% of the position | 100 ÷ 300 = 33.3% [COMPUTED] |
| Residual exposure at 1 contract | 200 shares | 300 − 100 = 200 [COMPUTED] |
| Unrealized gain | **$2,400** | 300 × (60.00 − 52.00) = 2,400 [COMPUTED] |
| Rate difference at stake | **$408** | 2,400 × (0.408 − 0.238) = 408 [COMPUTED]; rates per [VERIFIED] — IRC §1(h) and §1411 |
| Friction to exit outright instead | ≈ **$408 + $54** | 408 + (18,000 × 0.003 = 54) [ESTIMATED] the 0.3% round-trip band is an operating assumption, not a measured cost |

That last pair is the honest comparison the hedge must beat. A hedge costing more than roughly **$460** to avoid a $408 tax difference has cost more than it saved — and it has done so while leaving part of the position unprotected. Fill the premium column from your own broker's quote; it is not guessed here.

## The tax interaction flag

Hedging is not tax-neutral, and this file does not compute the rule. What it does is require the flag **before** the order:

> *"Proposed: hedge 100 of 300 shares with [structure] expiring [date], while the position is [N] sessions from its long-term anniversary and [M] days into a qualified-dividend window. Does this affect the holding period, and how?"*

Route that to `equity-tax-lot-and-exit-management`. Two specific reasons the flag matters:

- A position held for the qualified-dividend requirement — 61 days inside the 121-day period beginning 60 days before the ex-date [VERIFIED — IRC §1(h)(11), §246(c)] — is a position with a *live* holding-period requirement that a hedge could interact with.
- The long-term anniversary depends on the holding period beginning the day after the buy trade date and ending on the sale trade date [VERIFIED — IRC §1222, IRS Pub 550]; anything that pauses or terminates that period changes the date the holder is planning around.

Writing the flag costs one line. Skipping it risks a tax outcome nobody measured.

## When a hedge is clearly wrong

- **The level broke.** Route to CUT. A hedge on a breached thesis costs premium to protect a position you had already decided to leave.
- **The forced-action rung is live.** A margin call is not managed with a put; it is managed by reducing. The firm need give no advance notice above a $1,000 deficiency [VERIFIED — 12 CFR 220.4(d)].
- **The position is a write-off candidate.** Paying premium to protect an illiquid name is paying for a protection you cannot monetise.
- **The position is inside a wash-sale window and the hedge involves the same name.** The window freezes trading behaviour in the name, 30 days either side of a loss sale [VERIFIED — IRC §1091].
- **The holder cannot state what the hedge is for.** "Downside protection" is not a purpose; "protect the position through an event I do not want to sell into, at a defined cost, until the anniversary" is.

## Recording a hedge

```text
action:            HEDGE
rung:              4
thesis_state:      intact at the level, verified on the close
higher_rungs:      1 clear · 2 clear · 3 clear (no capital needed elsewhere; friction not cleared)
reason:            anniversary in 25 sessions; rate difference at stake 408 [COMPUTED]
shares_protected:  100 of 300          [COMPUTED] 100 ÷ 300 = 33.3%
residual:          200 shares uncovered
structure:         options-strategist — NOT decided here
cost:              from the broker quote, filled in at execution
tax_flag:          issued to equity-tax-lot-and-exit-management on <date>, answer <yes/no + rule>
exit_from_hedge:   the level, the anniversary, or the expiry, whichever comes first
expectation:       "the position survives the window with downside bounded below the strike"
grade_on:          the next review date
```

## Failure modes

1. **The hedge as procrastination.** Countermeasure: the rung-2 test is run first; if the level broke, the route is CUT.
2. **The hedge assumed to be tax-neutral.** Countermeasure: the tax flag is issued and answered before the order.
3. **Granularity ignored.** A 250-share position hedged "fully" with 2 contracts leaves 50 shares naked. Countermeasure: the residual is written in shares.
4. **Cost not stated as a percentage of the position.** Countermeasure: every hedge record carries cost ÷ position value.
5. **The collar's cap treated as free upside given away.** Countermeasure: the cap is recorded as a decision, not as a residual.
6. **Paying premium on a write-off candidate.** Countermeasure: liquidity classification precedes the hedge decision.
7. **Hedging into a wash-sale window.** Countermeasure: the flag from the health check blocks it.
8. **The hedge expiring before the event it was written for.** Countermeasure: the expiry is checked against the event calendar at the review, every review.
9. **Multiple hedges accumulating on one name.** Countermeasure: one hedge per position; a second is a new decision that must pass rungs 1–4 again.
10. **The position becoming unmanaged because the hedge "handles it".** Countermeasure: the contract still needs its level, target, date and event list. A hedge is an overlay, not a plan.

## What good looks like

A hedge that is worth its premium is recognisable: the thesis is intact and written, the level is verified on a close, the rungs above it are cleared in writing, the protected fraction is a whole number of contracts with the residual in shares, the cost is stated as a percentage of the position, the tax flag has been answered, and the position still has its own contract. Every one of those is a line in the record. A hedge that cannot produce those lines is not protection — it is a cost with a story attached.
