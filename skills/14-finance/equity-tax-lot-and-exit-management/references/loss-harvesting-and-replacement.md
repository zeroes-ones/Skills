# Loss Harvesting and Replacement — realising the loss, honestly

## What a harvest is, and what it is not

A harvest is the deliberate realization of a loss in order to offset a gain or to build a
carry-forward. It is a **tax-accounting action inside an economic decision**, not a reason to
own or to sell anything.

It is not:

- a way to make money — the loss is real money that was already lost;
- a way to fix a bad position — the position still exists in its replaced form;
- a way to reduce risk — the substitute carries the risk the original did;
- a reason to sell a position you would not otherwise sell.

If the position is not something the holder wants to own, the answer is to sell it and stay
out, which is also the simplest harvest. If it is, the harvest is a date and a lot choice on a
sale that was going to happen anyway.

## Step 1 — does the harvest have a real offset?

A realized loss is worth something only against something. Establish, in dollars and by
character:

| Offset inventory | What it can absorb |
|---|---|
| Short-term realized gains this year | A short-term loss, dollar for dollar, with no annual limit |
| Long-term realized gains this year | A long-term loss, dollar for dollar |
| No gains, or gains smaller than the loss | Ordinary income, up to the annual capital-loss deduction limit, with the remainder carrying forward |
| A prior-year carry-forward | Consumes the current year's realized items first |

`[COMMON-PRACTICE]` The ordering of losses against gains, and the annual deduction limit
against ordinary income, both have their own rules and neither is modelled here. The point of
the table is not to compute the tax; it is to force the question "what does this loss actually
offset?" before the sale is placed.

**If nothing is available to offset and the deduction limit is already used,** the harvest
produces a carry-forward: real, useful in a later year, and not a current-year benefit. Say so
plainly rather than presenting the harvest as a saving.

## Step 2 — size the harvest

Size the harvest to the offset, not to the loss.

- Offsets of **$4,000** `[ESTIMATED]` and a loss lot of **$9,000 loss** `[ESTIMATED]`: selling
  the whole lot realizes more loss than the year can use, and the excess becomes a
  carry-forward. That may be exactly right — carry-forwards are not worthless — but it should
  be a stated choice, not a surprise.
- Sizing is a lot decision: sell part of the loss lot, or sell it whole and accept the
  carry-forward.

## Step 3 — sweep the 61-day box, both directions

Before anything is placed, list every purchase of the same or a substantially identical
security from 30 days before the intended sale to 30 days after it. Include reinvestment,
employee plans, other accounts and retirement accounts. The window and its arithmetic live in
`(references/wash-sale-window-playbook.md)`.

## Step 4 — choose the re-entry

The four honest options, with their real costs:

| Option | What it does | Cost | When it is right |
|---|---|---|---|
| **Stay out** | Sell the loss lot and hold no substitute for the box and beyond | Full market exposure given up for the period | The position was not wanted. This is the cleanest harvest and the only one with no identity question |
| **Same security on day 31** | Sell, wait out the box, re-buy on day 31 | One month of missed exposure in both directions; possible price gap | The thesis is intact and the holder is prepared to be out |
| **Substitute security** | Sell the loss lot, buy an economically similar but not substantially identical security at once | Basis risk: the substitute will not track the original exactly, and the identity question must be answered | The exposure must be maintained and a defensible substitute exists |
| **Double-up, then sell** | Buy the replacement first, then sell the loss lot — so the replacement is not acquired inside the box relative to the sale | Requires capital for both positions at once; the box still runs 30 days *after* the sale for any further purchase | The holder wants continuity of exposure and has the capital |

### The double-up technique, stated fairly

Buying the replacement **before** the loss sale means the replacement acquisition is outside
the forward half of the box only if it is more than 30 days before the sale — which it is not.
The technique that actually works is: **buy the replacement at least 31 days before the sale**,
or accept that the acquisition dates inside the box are exactly what the rule addresses.
Where a broker or adviser presents "buy first, sell second" as a way around the window, the
dates must be checked against the actual 61-day box, not against the intent.

**The honest version:** there is no costless way to keep continuous exposure and bank a loss
on the same security. Something is given up — exposure, tracking, or the loss itself. Pick
which, in writing.

## Step 5 — the substitute decision, done honestly

```text
   Is the replacement SUBSTANTIALLY IDENTICAL to the security sold?
        ├── Same issuer, same security, different ticker/venue/class ──▶ YES. Unsafe.
        ├── Same issuer, convertible preferred or a convertible ──────▶ MAY BE. Unsafe.
        │     (Publ. 550 flags convertible preferred as a case that may be)
        ├── An option or contract on the same security ───────────────▶ Generally unsafe.
        ├── A different issuer, similar industry ─────────────────────▶ Ask the question.
        │     Different corporation is "ordinarily" not substantially identical,
        │     but the test is facts and circumstances. Write the reasoning.
        └── A broad fund whose holdings overlap the original ─────────▶ Ask the question.
              Overlap alone is not the test, but document the analysis.
```

`[VERIFIED — IRS Pub 550]` Stock of a different corporation is "ordinarily" not substantially
identical; convertible preferred may be. The determination is made on facts and circumstances.

**Operational rule:** if the question cannot be answered with a written paragraph, do not use
the substitute. Stay out for the box. Not buying is free.

## Worked harvest, with the arithmetic visible

Inputs `[ESTIMATED]`: lot L3, 100 shares, basis **$140.00/share**, current price **$120.00**.
Realized short-term gains this year: **$3,000 gain** `[ESTIMATED]`. Marginal short-term rate
40.8% `[ESTIMATED]`.

- Realized loss: `(120.00 − 140.00) × 100` = **$2,000 loss** `[COMPUTED]`.
- Offset against the **$3,000 gain** `[COMPUTED]`: the gain becomes `3,000 − 2,000` =
  **$1,000 gain** `[COMPUTED]`.
- Tax effect: `0.408 × 2,000` = **$816 saved** `[COMPUTED]`.
- If instead nothing was available to offset and the annual deduction limit were already
  used, the harvest would produce a carry-forward and **$0 saved** in the current year
  `[COMPUTED]`.
- Box: if L3 is sold on the 15th, the box runs from the 15th of the prior month to the 14th
  of the next month; the first safe re-entry is the 15th of the next month `[COMPUTED]`.

The same 100 shares, the same price, the same day, produce **$816** `[COMPUTED]` of difference
between the "sell the loss lot" answer and the FIFO default's "sell the oldest lot" answer.
That number is the whole reason the lot decision exists.

## Counter-check before placing the harvest

- Is the loss lot also the lot with the **weakest forward outlook**? If not, the harvest is
  realizing a loss on the strongest part of the position to keep the weakest — a tax-driven
  error.
- Is the remaining position's **embedded deferred tax** larger than the realized saving? If
  so, the harvest has swapped a small current benefit for a larger future one.
- Is the **thesis** intact on the remaining position? If not, the harvest is a way of not
  deciding, and the correct action is a full exit.

## Failure modes

1. **What goes wrong — harvesting with nothing to offset.** The loss becomes a carry-forward, real but not a current-year saving, and it was presented as one.
2. **What goes wrong — harvesting the strongest lot.** The lot with the best forward case is sold because it happens to carry the loss, leaving the weakest lot in place.
3. **Worst case — the contaminated harvest.** A reinvestment or an automatic purchase inside the box disallows the loss; the harvest buys nothing and the basis of the replacement is now wrong.
4. **What goes wrong — the asserted substitute.** A replacement called "different" without the identity question being answered in writing.
5. **Worst case — the double-up misread.** "Buy first, sell second" applied outside the 61-day box it was supposed to avoid.
6. **What goes wrong — the exposure gap nobody priced.** Staying out for 31 days in a rising market costs more than the loss was worth. That is a legitimate trade-off, but it must be named before, not after.
7. **What goes wrong — the harvest instead of a decision.** A broken position is harvested rather than exited, because harvesting felt like action.
8. **Known limitation — the carry-forward inventory is out of scope.** This skill cannot tell you what prior-year carry-forwards you have; that comes from the return.
9. **Edge case — the loss lot smaller than the desired harvest.** Selling the whole lot over-realizes; selling part leaves an awkward partial lot that must be carried correctly.
10. **Edge case — the year's offset disappears.** A planned gain is deferred, and the harvest's realized loss now has nothing to offset this year.

## Checklist

- [ ] Offset inventory established in dollars and by character, from the return or the broker's realized report.
- [ ] Harvest sized to the offset, with the carry-forward amount stated if any.
- [ ] 61-day box swept in both directions across every account.
- [ ] Re-entry option chosen from the four, and its cost named.
- [ ] Substitute, if any, cleared by a written answer to the identity question.
- [ ] Loss lot compared against the forward outlook of the lots that remain.
- [ ] Deferred tax on the remaining position stated in dollars.
- [ ] Ledger row created before the order, tagged `HL`, carrying the after-tax delta against FIFO.
