# After-Tax Versus Gross P&L — the objective function

## The claim

**Two sales of the same 100 shares at the same price on the same day are not the same trade.**
They differ by which lots they consume, and therefore by the tax they create. Gross P&L cannot
see the difference. Percentage gain cannot see the difference. Only after-tax proceeds can.

This is the whole reason a lot-selection ladder exists. If gross P&L were the objective
function, FIFO would be as good as any other answer.

## The formula

```text
   realized_gain_or_loss = (sale_price − basis_per_share) × shares_consumed_from_lot

   tax_on_sale = realized_gain_or_loss × rate(character)
                     where character ∈ {short-term, long-term}
                     and a loss is a negative tax — an offset or a carry-forward

   after_tax_proceeds = gross_proceeds − tax_on_sale
```

And for comparing two candidate lots at the same price and date:

```text
   after_tax_delta = after_tax_proceeds(lot A) − after_tax_proceeds(lot B)
```

Nothing in that expression mentions the account's average cost. It cannot: the average is not
a quantity any sale consumes.

## The same position, four answers

Four lots of 100 shares, price **$120.00** `[ESTIMATED]`, rates `[ESTIMATED]` 40.8% short-term
and 23.8% long-term.

| Lot | Basis/sh | Character | Gain/(loss) | Tax | After-tax proceeds from $12,000 gross |
|---|---|---|---|---|---|
| L1 | $50 | long-term | **$7,000 gain** `[COMPUTED]` | `0.238 × 7,000` = **$1,666 cost** `[COMPUTED]` | **$10,334** `[COMPUTED]` |
| L2 | $90 | short-term | **$3,000 gain** `[COMPUTED]` | `0.408 × 3,000` = **$1,224 cost** `[COMPUTED]` | **$10,776** `[COMPUTED]` |
| L3 | $140 | short-term | **$2,000 loss** `[COMPUTED]` | `0.408 × 2,000` = **$816 saved** `[COMPUTED]` | **$12,816** `[COMPUTED]` |
| L4 | $95 | short-term | **$2,500 gain** `[COMPUTED]` | `0.408 × 2,500` = **$1,020 cost** `[COMPUTED]` | **$10,980** `[COMPUTED]`: 12,000 − 1,020 |

The gross figure is **$12,000** in every row `[COMPUTED]`. Every proceeds cell is `12,000 −
tax`, with the loss row adding instead of subtracting: `12,000 − 1,666` = **$10,334**
`[COMPUTED]`; `12,000 − 1,224` = **$10,776** `[COMPUTED]`; `12,000 + 816` = **$12,816**
`[COMPUTED]`; `12,000 − 1,020` = **$10,980** `[COMPUTED]`. The after-tax spread across the four
rows is `12,816 − 10,334` = **$2,482** `[COMPUTED]` — on one sale, of one position, at one price,
on one day. (That spread is a difference in **after-tax proceeds**. It is the same number as,
but a different quantity from, the **$2,482 tax-liability difference** between FIFO and the loss
lot quoted in `(references/partial-scale-out-lot-ordering.md)`; do not read one for the other.)

**The FIFO default selects L1.** It is the largest after-tax cost of the four. That is the
entire argument for this skill.

## Why 11 months and 13 months are different assets

A lot held 11 months and a lot held 13 months may have identical quantities, identical prices
and identical forward business prospects. They are not the same asset to their owner, because
selling them produces different after-tax cash.

Worked `[ESTIMATED]`: one lot, 100 shares, basis **$0.00** (an extreme illustration so the
numbers are clean), price **$120.00**, so the entire **$12,000 value** `[COMPUTED]` is gain.

| Sale date | Character | Tax | After-tax proceeds |
|---|---|---|---|
| Held 11 months | short-term | `0.408 × 12,000` = **$4,896 cost** `[COMPUTED]` | **$7,104** `[COMPUTED]` |
| Held 13 months | long-term | `0.238 × 12,000` = **$2,856 cost** `[COMPUTED]` | **$9,144** `[COMPUTED]` |

Two months of holding, `9,144 − 7,104` = **$2,040** `[COMPUTED]` of difference, or 17% of the
gross value `[COMPUTED]`.

That is a real and large effect. It is also the effect that produces the single most common
error in this domain, which is the next section.

## The line that must not be crossed

```text
   Tax changes WHEN you sell a position you were going to sell.
   Tax does not change WHETHER the position should exist.
```

The 17% effect above applies to a position the holder was selling anyway. It does not apply to
a position held only because of the number. When a thesis breaks, the position's own downside
is uncapped while the tax differential is bounded by the rate pair — a few percent, as the
cushion computation shows. `[COMPUTED]` The arithmetic of the cushion is therefore also the
arithmetic of the prohibition: the rate is worth about 5.6% of a position on the worked
numbers, and a broken thesis is worth the position.

## Deferred tax is not forgiven tax

The residual-position counter-check, stated properly:

- Sell the loss lot, keep the low-basis lot: **$816 saved** `[COMPUTED]` in the current year,
  and a **$7,000 gain** `[COMPUTED]` of deferred tax now sits in the retained lot.
- Sell the low-basis lot, keep the loss lot: **$1,666 cost** `[COMPUTED]` realized now, and
  the retained lot carries a **$2,000 loss** `[COMPUTED]` of potential future benefit.

Neither is free. The correct comparison includes the retained position's embedded tax
position, which is why the honest counter-check appears beside every worked example in this
skill. It is not a reason to avoid the analysis; it is a reason to finish it.

## What to record, every time

| Field | Why |
|---|---|
| Lots consumed, by acquisition date and basis | The identification, restated |
| Gross proceeds | The number the gross view stops at |
| Realized gain or loss, and its character | The input to the tax figure |
| Rate pair applied, with the date and the `source:` | The assumption the conclusion rests on |
| Tax on the sale, signed (a loss is negative) | The subtrahend |
| After-tax proceeds | The objective function's value |
| FIFO counterfactual, after tax | The default's answer, at the same price and date |
| Delta | **`after_tax_actual − after_tax_fifo`** — the only number that scores the decision |

A ledger row without the delta has recorded a trade, not a decision.

## Failure modes

1. **What goes wrong — the gross comparison.** Two lots compared on gross gain; the more expensive lot looks better because its gross gain is smaller, or vice versa.
2. **What goes wrong — the percentage comparison.** Two lots compared on percentage gain when their gross amounts differ; the comparison is between two different quantities.
3. **Worst case — the rate used to justify a hold.** A 17% effect used as a reason to keep owning something; the cushion is 5.6% of the position and the thesis risk is not bounded.
4. **What goes wrong — the deferred tax ignored.** The retained low-basis lot is treated as carrying no liability, so the harvest appears better than it is.
5. **What goes wrong — the unstated rate pair.** An after-tax figure presented without the rates that produced it, so it cannot be recomputed or challenged.
6. **What goes wrong — the missing delta.** The ledger row records the trade but not its result against the FIFO default, so the rule that chose the lot can never be scored.
7. **Known limitation — state and local tax is out of scope.** Where it applies, it can change the ordering conclusion and it is not in the arithmetic above.
8. **Edge case — the loss in a year with no offset.** A negative tax becomes a carry-forward, not a refund, and the after-tax proceeds figure changes meaning.
9. **Edge case — the basis-adjusted lot.** A wash-sale replacement lot's basis is not its purchase price, so its gain and its tax are not what the purchase record suggests.

## Checklist

- [ ] Every candidate lot expressed as after-tax proceeds, not gross and not percentage.
- [ ] Rate pair stated with its `source:` or labelled `[ESTIMATED]`.
- [ ] Signed tax figure, so a loss appears as a benefit rather than a cost.
- [ ] FIFO counterfactual computed at the same price and date.
- [ ] Delta recorded, signed, in the ledger row.
- [ ] Retained position's embedded deferred tax stated in dollars.
- [ ] Non-tax reason to hold written before the tax comparison, per R5.
