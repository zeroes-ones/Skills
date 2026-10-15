# Cut and Rotation Decision

Two actions, one file, because they are the same exit question asked from two directions. **CUT** asks "should I leave this position?" **ROTATE** asks "should I leave this position *in order to own a different one*?" Rotation is the only action in the router with no options analogue, and it is the one least often taken.

**Portability target:** spec-level. Every figure here is supplied by a tax or sizing owner; this file owns the decision.

## CUT — the level, not the percentage

The trigger for a cut is a **breached invalidation level** or a **broken thesis**. It is never a P&L percentage.

The reason is structural. An option has a clock that can be relied upon to force resolution; a stock does not. If the cut rule is "down 15%", the rule has no anchor in the security itself — it has an anchor in the basis, and the basis is not a fact about the company. Worse, a percentage rule moves: a holder who has already accepted −15% finds −20% easy to accept the second time.

A **level** is a price at which the thesis stops being true. It has three properties a percentage lacks:

1. It is written before the position is opened, so it cannot be fitted to the price afterwards.
2. It is checkable against a close, so two people agree on whether it fired.
3. It survives a change of basis, which a percentage does not.

If no level exists, the position fails step 2 of the health check, is frozen, and the level is written before anything else is decided.

## Execution of a cut

| Situation | First action | If that fails | Last resort |
|---|---|---|---|
| The level broke on a **close**, market gapped overnight | Do not chase the opening print; queue the exit for the first 30 minutes of regular hours | Use a limit at a level you can defend and accept a partial fill | Accept the fill and re-underwrite what remains; never average down a gapped loss |
| The level broke **intraday** on a wick | Require a close, not a wick, before treating the level as breached | If the thesis depends on the intraday level, define it as such in advance | Re-arm the review and treat the wick as a data point, not a trigger |
| The name is **thin** and the exit will not fill at size | Reclassify as a WRITE-OFF candidate and stop monitoring it weekly | Leave a resting order at a level you would genuinely accept | Hold it out of the attention set; the lesson is what was paid for |
| A **forced action** forced the exit | Execute inside the window the firm gave you; the firm need give no advance notice [VERIFIED — 12 CFR 220.4(d)] | Reduce rather than close, if the firm's window allows it | Accept the liquidation and rebuild the account's floors before trading again |

**The write-off classification is an exit, not a failure.** A position in a name that cannot be exited at size is still consuming attention every week. Marking it a write-off removes it from the attention set permanently — which is the only resource it was still costing you.

## ROTATE — the first-class action

Rotation is the explicit comparison between the position you hold and the best alternative use of the same capital. It is not impatience, and it is not disloyalty to a thesis. It is the answer to a question no clock will ever ask on its own: a stock never expires, so a position that is merely *adequate* will occupy its capital forever.

**When rotation is the right action:**

- The capital is needed for a better idea that has already been sized.
- The current thesis is intact but **fully expressed** — the market now believes what you believed, and the remaining upside no longer compensates for the remaining risk.
- The position is a permanently small holding that cannot be trimmed, cannot be sized up, and consumes attention.

**When rotation is the wrong action:**

- The replacement idea has not been sized. A rotation into an unsized idea is two decisions in one order.
- The current position's thesis broke. That is a CUT; the replacement is a separate decision with its own gate.
- The current position realises a loss inside a wash-sale window in the replacement name. That is a void harvest, and it is invisible until the tax year closes.

## The rotation arithmetic, in dollars

The friction must be computed before the comparison, not after.

Position: 700 shares at $57.00, basis $51.28 (a $4,000 gain).

| Item | Value | Formula |
|---|---|---|
| Position value | **$39,900** | 700 × 57.00 = 39,900 [COMPUTED] |
| Gain to realise | **$4,000** | 700 × (57.00 − 51.28) = 4,004; use 4,000 for the arithmetic [COMPUTED] |
| Tax at a 23.8% long-term rate (an assumed rate) | **$952** | 4,000 × 0.238 = 952 [COMPUTED]; the 23.8% rate is [ESTIMATED] — substitute your own bracket — while the statutory rates it derives from are [VERIFIED] — IRC §1(h) and §1411 |
| Round-trip commission and spread | **$120** | 39,900 × 0.003 = 120 [ESTIMATED] — a 0.3% operating band for a liquid large-cap name, not a measured cost |
| **Total friction** | **$1,072** | 952 + 120 = 1,072 [COMPUTED] |
| Friction as a share of the position | **2.7%** | 1,072 ÷ 39,900 = 2.69% [COMPUTED] |

The number that matters is the last one. **The new idea must beat the old one by roughly 2.7% in the first year before the rotation is level.** That is the bar. It is a real bar, and it is also a low bar — which is exactly why "it might come back" is not an answer.

Now compare the two ideas' expected returns:

- Held position, expected forward return: X.
- Replacement, expected forward return net of its own entry friction: Y.
- Rotate when **Y − X > 2.7%** over the horizon you actually intend to hold, before considering that the rotation also resets the holding-period clock on the replacement, which is a tax consequence rather than an arithmetic one [VERIFIED — the holding period begins the day after the buy trade date; IRC §1222, IRS Pub 550].

The expected-return inputs belong to `fundamental-analyst` and `portfolio-signal-manager`. This file owns the structure of the comparison and the requirement that the friction be in it.

## Which tax lot leaves, and why it is not decided here

A rotation realises a gain or a loss, and therefore touches lots:

- Selling specific lots changes the realised amount, and therefore the tax — [VERIFIED] the tax owner's decision, not this file's.
- A realised **loss** opens a 61-day wash-sale window in the name, 30 days before through 30 days after, with replacement shares inheriting the old holding period [VERIFIED — IRC §1091, §1223(3)]. Rotating *out of* a name at a loss and back *into* it inside the window is a void harvest.
- A gain realised before the long-term anniversary is short-term; the holding period begins the day after the buy trade date and ends on the sale trade date, so the earliest long-term sale is buy date + 1 year + 1 day [VERIFIED — IRC §1222, IRS Pub 550].

The instruction issued to the tax owner is precise: *"exit the whole position at price P on date D as part of a rotation into NAME — choose the lots, and flag any window this opens."*

## The order of operations

A rotation is executed as **CUT then ADD**, in that order, never as two simultaneous ideas:

```text
1. Size the replacement.            portfolio-signal-manager
2. Compute the friction in dollars. equity-tax-lot-and-exit-management + equity-risk-and-capital-engineer
3. Compare: replacement edge − friction > held position's forward edge?
      NO  → do not rotate. Record "nothing better" as an answer with a date.
      YES → continue
4. Check the wash-sale window on the name being exited, and on the name being entered.
5. Exit first. The exit realises the gain or loss and frees the capital.
6. Size the entry against the actual freed capital, not the assumed amount.
7. Write the new position's contract: level, target, improve-by date, event list.
```

Step 6 is the step that gets skipped. The freed capital is rarely exactly the number assumed before the exit; the entry is sized against what the account actually has.

## The standing rotation question

Rotation is asked on the cadence, not once at purchase:

- **Every held position** is compared against the best idea available for the same money, at the same risk, today.
- **"Nothing better" is a valid answer** — but it is recorded as an answer with a date, because the alternative is a book that has not been examined in years.
- **A rotation that is refused twice for the same reason** is not a refusal; it is a decision that the comparison is not being done honestly.

## Failure modes

1. **The cut rule is a percentage.** Countermeasure: the level is a price, versioned, written before the position existed.
2. **The level restated lower.** Countermeasure: a change to the level requires a written reason and a new grading date.
3. **Cutting into the opening print after a gap.** Countermeasure: first 30 minutes of regular hours, or a limit you can defend.
4. **A thin name carried as if it were tradeable.** Countermeasure: write-off classification at every review where depth fails.
5. **Rotation without friction arithmetic.** Countermeasure: the 2.7% bar is computed and shown, or the rotation is refused for lack of a number.
6. **Rotating into an unsized idea.** Countermeasure: the replacement is sized before the exit, and re-sized against actual freed capital after.
7. **A rotation that voids a harvest.** Countermeasure: the wash-sale window is checked on both names before the exit.
8. **The "it might come back" non-decision.** Countermeasure: the rotation question is asked on the cadence; the answer is recorded; a refusal carries a date.
9. **Selling the winner to keep the loser.** Countermeasure: dispositions are chosen by the level, never by the sign of the P&L.
10. **The rotation that is really a CUT.** If the thesis broke, the route is rung 2 and the replacement is a separate, later decision. Bundling them hides a broken thesis inside a purchase.

## Verification

- **Complete when** the cut trigger is a written price level, not a percentage of entry.
- **Complete when** the mechanism (window, limit, partial-fill handling) is written before the order.
- **Complete when** the rotation's friction is shown in dollars with its formula, and the comparison against the replacement's edge is on the page.
- **Complete when** the lot instruction names the rung, size, price and date, and the tax owner has answered it.
- **Complete when** the wash-sale window has been checked on both the exiting and the entering name.
- **Complete when** the new position has its own contract, or the rotation has not been completed.
