# Wash-Sale Window Playbook — the 61-day box

## The rule, stated exactly

A loss on the sale of stock is disallowed where, within the period beginning 30 days before
the sale and ending 30 days after it, the taxpayer acquires substantially identical stock or
securities. `[VERIFIED — IRC §1091(a)]`

Three consequences follow immediately, and each is a place people lose money:

1. **The window is 61 days long, and it looks BOTH ways.** Thirty days before, the sale day,
   thirty days after. A purchase made *before* the loss sale contaminates it.
2. **The disallowed loss does not vanish — it moves.** Replacement shares generally take a
   basis adjusted by the disallowed amount, and they inherit the old shares' holding period.
   `[VERIFIED — IRC §1223(3)]`
3. **Substantially identical is a facts-and-circumstances question.** Stock of a different
   corporation is "ordinarily" not substantially identical; convertible preferred may be.
   `[VERIFIED — IRS Pub 550]`

## The 61-day box, drawn

```text
        day −30            day 0 (loss sale)            day +30
   ────────┬────────────────────┬───────────────────────────┬────────
           │                    │                           │
      purchases here        LOSS SALE                  purchases here
      contaminate it                                   contaminate it

   safe re-entry is day +31, not day +30.
```

Two dates to write on the ticket, every time: **box start = sale date − 30 days** and
**box end = sale date + 30 days**. The first safe re-entry is the day after the box ends.

## What counts as a purchase

The list is longer than most holders expect, because it is not limited to a deliberate buy
order in the same account.

| Event | Is it a purchase for this purpose? | What usually goes wrong |
|---|---|---|
| A deliberate buy of the same security | Yes | The obvious case — and the one people remember |
| A buy of the same security in **another account** | Yes | The account boundary is invisible to the rule |
| A buy inside a **retirement account**, then a sale in a taxable account | Commonly treated as within the rule | The two accounts are never thought of as one holder |
| Automatic investment plan purchase | Yes | It fires on its own schedule, inside the box, unnoticed |
| Dividend **reinvestment** | Yes | Quarterly, small, and the most common accidental contaminant |
| ESPP purchase period | Yes | The purchase date is set by the plan, not the holder |
| RSU vesting | Yes | Vesting on a fixed date the holder did not choose |
| Option exercise delivering shares | Yes | The acquisition date is the exercise date |
| A spousal purchase | Commonly attributed to the holder | Two people, one tax return |
| Buying back a **short** position | Not a purchase of stock; but the short's own rules apply | Confusing the short-side dividend clock with the wash-sale box |
| A **gift** received | Generally no acquisition by purchase | But the holding period carries over, which changes the character later |
| An **inheritance** | Generally not a purchase | Basis is usually reset, which resets the analysis |

`[COMMON-PRACTICE]` The table is a working checklist for scanning an account history, not a
restatement of the statute. Each row has exceptions, and several depend on facts that have to
be established rather than assumed.

## The two traps that cost the most

### Trap 1 — the December harvest and the January re-buy

The holder sells at a loss on **December 20** to book the loss in this tax year, then re-buys
on **January 5** because "it is a new tax year".

- Box start on the sale: `December 20 − 30` = **November 20** `[COMPUTED]` — **box day 1**.
- Box end: `December 20 + 30` = **January 19** `[COMPUTED]` — **box day 61**.
- January 5 is **box day 47** `[COMPUTED]`, which is **day +16 measured from the sale**.
- The re-buy is **inside the box**. Part or all of the loss is disallowed and moves into the
  January lot's basis.

**Two day numbers, two anchors — never mix them.** This file counts **box days**, with the box
start as day 1: `box day = calendar days elapsed since the box start + 1`, so the 61-day box runs
from box day 1 (November 20) to box day 61 (January 19) and January 5 is box day 47
`[COMPUTED]`. The **sale-relative** count — used in the diagram above, in the pre-sale arithmetic
below, and in `(references/year-end-harvest-calendar.md)` — takes the **sale date as day 0**, so
the box runs day −30 to day +30, the same January 5 is **day +16**, and the first safe re-entry
is **day +31**.

The new tax year has nothing to do with it. The window is counted in days from the sale, not
in calendar years.

### Trap 2 — the purchase made before the sale

The holder buys 100 more shares on **day −11**, then sells 100 shares at a loss on **day 0**
"to harvest".

The 100 shares bought eleven days earlier are replacement shares. The disallowed loss is
sized by the replacement quantity, not by good intentions.

- Loss on the sale: **$5,000 loss** `[ESTIMATED]` on 1,000 shares.
- Replacement shares acquired inside the box: 600.
- Disallowed share: `600 / 1,000` = 60% `[COMPUTED]` → `0.60 × 5,000` = **$3,000 cost** that
  does not reduce this year's income `[COMPUTED]`.
- Allowed share: `5,000 − 3,000` = **$2,000 loss** `[COMPUTED]`, which does reduce it.
- The **$3,000** is added to the basis of the 600 replacement shares, which also inherit the
  original shares' holding period. `[VERIFIED — IRC §1223(3)]`

The holder who assumed a full $5,000 deduction is $3,000 of deduction away from the truth.

## The disallowed-loss arithmetic

```text
   disallowed_loss = (replacement_shares / sold_shares) × realized_loss
   allowed_loss    = realized_loss − disallowed_loss
   new_basis_of_replacement = old_basis_of_replacement + disallowed_loss
   holding_period_of_replacement = holding_period_of_old_shares  (carried over)
```

When replacement shares are fewer than the shares sold, only the matching fraction is
disallowed. When they are more, the whole loss is disallowed and the excess replacement
shares carry the rest of the adjustment forward.

## What the loss becoming basis actually costs

The disallowed loss is not destroyed; it is deferred into replacement shares. The cost is
the deferral itself, and it can be permanent:

- If the replacement shares are held to death or donated, the adjustment may never be
  recovered in the way the holder intended.
- If the replacement shares are sold later at a gain, the disallowed loss has effectively
  reduced that gain — the same money, one tax year later.
- If the replacement shares are sold at a further loss inside *another* box, the analysis
  recurses.

The correct framing: **the loss was not harvested, only moved.** A harvest that does not
actually realize the loss has produced no offset and therefore bought nothing.

## Is a substitute security a way out?

Sometimes. This is one of the few places where an unrelated but economically similar security
is genuinely legitimate rather than an evasion, because the statutory test is **substantial
identity**, not economic exposure. `[VERIFIED — IRS Pub 550]`

| Candidate substitute | Why it might be acceptable | The caution |
|---|---|---|
| A broad market or sector fund instead of one stock | A different issuer, a different set of holdings; stock of a different corporation is "ordinarily" not substantially identical | The judgement is facts and circumstances. Document the reasoning; do not simply assert it |
| A direct competitor | Different issuer, different security, similar economics | Similar economics is not the test, but a regulator or a court may see it differently from you. Verify |
| A convertible preferred of the same issuer | — | Publ. 550 flags convertible preferred as a case that **may** be substantially identical. Treat as unsafe |
| The same security through a different ticker, share class or listing | — | Generally unsafe. Same issuer, same economics |
| An option or contract on the same security | — | Generally unsafe as a replacement |

**The honest instruction:** where the answer cannot be established, stay out of the market
for the remainder of the box. Not buying is free. A contaminated loss is not.

## When the box is already open and the loss is already sold

1. Size the replacement shares precisely; count them, do not estimate.
2. Compute the disallowed fraction and the allowed loss.
3. Record the basis addition on the replacement lot and the inherited holding period.
4. Refresh the lot table — the basis it shows is now wrong.
5. Re-plan the rest of the exit around the lots that actually exist.

Do not place another trade to "fix" it. A second sale cannot undo a disallowed loss.

## Failure modes

1. **What goes wrong — the backwards window.** A purchase eleven days before the loss sale disallows most of it, and the harvest buys almost nothing.
2. **What goes wrong — the dividend reinvestment.** A quarterly DRIP inside the box contaminates a loss in an account the holder believed was separate.
3. **Worst case — the January re-buy.** The loss is deferred into the January lot's basis, which was not the plan, and the offset for the current year is gone.
4. **What goes wrong — the asserted substitute.** A replacement was called "different" without the facts-and-circumstances question being asked.
5. **Worst case — the convertible preferred.** A same-issuer convertible instrument treated as a safe substitute when Publ. 550 flags it as a case that may be substantially identical.
6. **What goes wrong — the retirement-account purchase.** A buy inside an IRA inside the box, in an account that was never considered part of the analysis.
7. **Known limitation — this skill cannot establish substantial identity.** It can only require that the question be asked and the answer written down.
8. **Edge case — partial replacement.** Replacement shares fewer than shares sold produce a partial disallowance, with the rest allowed. Getting the fraction wrong overstates or understates the deduction.
9. **What goes wrong — the missing record.** The disallowed loss was computed once, in a conversation, and never written onto the replacement lot. The basis is wrong forever.
10. **Edge case — the recursive box.** The replacement shares are themselves sold at a loss inside another box, and the analysis repeats.

## Checklist

- [ ] Box start and box end dates written out for every loss sale, both sides.
- [ ] Every purchase of the same or a similar security listed for 30 days either way, every account.
- [ ] Reinvestment, automatic investment, ESPP and vesting dates checked explicitly.
- [ ] Replacement quantity counted, not estimated.
- [ ] Disallowed fraction, disallowed amount and allowed loss all written down.
- [ ] Basis addition recorded on the replacement lot.
- [ ] Inherited holding period recorded on the replacement lot.
- [ ] First safe re-entry date recorded, as a date, not as "31 days later".
- [ ] Substitute decision, if any, recorded with the written answer to the identity question.
