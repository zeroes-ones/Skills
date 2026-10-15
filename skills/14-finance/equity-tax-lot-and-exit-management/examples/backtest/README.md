# Backtest / Evidence Format — equity-tax-lot-and-exit-management

> **This file defines a FORMAT. It contains no measured results.**
> Everything numeric below is either a column definition, an arithmetic example explicitly
> marked `[COMPUTED]` from stated `[ESTIMATED]` inputs, or a placeholder. The desk has not
> published measured outcomes here, and none are invented. Where a real number would go, a
> placeholder is shown instead.

## Why this format exists

A lot decision can only be justified against the alternative of letting the broker's default
do it. That comparison cannot be made from memory, so every sale is recorded in a fixed shape
that makes the comparison mechanical later. **The format is the deliverable; the numbers
arrive when the book is scored.**

## The unit of record: one sale

One row per sale. A position exited across four rungs produces four rows, and the rows for one
position are read together.

| # | Column | Type | Definition |
|---|---|---|---|
| 1 | `decision_id` | string | Stable id, e.g. `ETL-<symbol>-<seq>` |
| 2 | `tag` | enum | One of `LS` `HL` `WB` `HP` `YE` `LR` `DC` `PS` `SC` — exactly one |
| 3 | `trade_date` | date | The **trade** date of the sale, never the settlement date |
| 4 | `symbol` | string | The security |
| 5 | `account` | string | The account, because lot sets and wash-sale boxes are per holder, not per account |
| 6 | `lots_consumed` | array | Per lot: `{acquired, qty_consumed, basis_per_share, qty_remaining}` |
| 7 | `relief_method` | enum | `specific-id` / `default-fifo` / `default-average` / `default-other` — what actually applied |
| 8 | `instruction_written` | boolean | Was a lot instruction written before the order? |
| 9 | `confirmation_format` | string | What evidence exists that the instruction was applied |
| 10 | `gross_proceeds_usd` | decimal | Sale price × shares, before tax |
| 11 | `realized_gain_usd` | decimal | Per lot and in total, signed |
| 12 | `character` | enum | `short-term` / `long-term` / `mixed` — per lot |
| 13 | `days_held` | integer | Per lot, from the acquisition trade date to the sale trade date |
| 14 | `rate_pair` | object | `{short: 0.xxx, long: 0.xxx, as_of: date, source: "..."}` |
| 15 | `tax_usd` | decimal | Signed: a loss is negative. `realized_gain × rate(character)` |
| 16 | `after_tax_proceeds_usd` | decimal | `gross_proceeds − tax` |
| 17 | `fifo_counterfactual_usd` | decimal | After-tax proceeds if the default lot had been consumed, at the same price and date |
| 18 | `delta_usd` | decimal | **`after_tax_actual − after_tax_fifo`** — the score |
| 19 | `box_start` / `box_end` | dates | The 61-day wash-sale window around this sale, if it realized a loss |
| 20 | `reentry_date` | date | First safe re-entry: box end + 1 day, or "no re-entry" |
| 21 | `disallowed_loss_usd` | decimal | If contaminated: the disallowed amount, with replacement shares and basis added |
| 22 | `non_tax_reason` | string | The reason this position was held at all, written **before** the tax reasoning |
| 23 | `provenance` | object | Per figure: `[COMPUTED]` `[ESTIMATED]` `[VERIFIED]` `[BROKER-VERIFIED]` `[COMMON-PRACTICE]` |
| 24 | `validity_condition` | string | The condition under which this decision remains right |
| 25 | `scoring_date` | date | When the row's outcome is revisited |

`[COMMON-PRACTICE]` This column set is the desk's evidence convention. It is not prescribed by
any regulator, exchange or tax authority.

## The comparison that gives the format its purpose

```text
   actual     =  after_tax_proceeds actually realized on the sale
                 + after-tax proceeds of any LATER rungs of the same exit, at the same
                   scoring date

   fifo       =  after-tax proceeds that would have resulted if the broker's default lot
                 relief had consumed the shares instead, at the SAME price and the SAME date

   delta      =  actual − fifo

   verdict    =  delta > 0  →  the lot choice added after-tax value; keep the rule
                 delta = 0  →  neutral; keep the rule only if it also reduced a risk
                                that was actually carried
                 delta < 0  →  the lot choice destroyed after-tax value; retire the rule
```

**Worked arithmetic for the counterfactual column only.** Four 100-share lots, price
**$120.00** `[ESTIMATED]`, rate pair 40.8% short-term / 23.8% long-term `[ESTIMATED]`.

| Lot | Basis/sh | Character | Gain/(loss) | Tax | After-tax proceeds |
|---|---|---|---|---|---|
| L1 (the default's choice) | $50 | long-term | **$7,000 gain** `[COMPUTED]` | `0.238 × 7,000` = **$1,666 cost** `[COMPUTED]` | `12,000 − 1,666` = **$10,334** `[COMPUTED]` |
| L3 (an alternative) | $140 | short-term | **$2,000 loss** `[COMPUTED]` | `0.408 × 2,000` = **$816 saved** `[COMPUTED]` | `12,000 + 816` = **$12,816** `[COMPUTED]` |

`delta_usd` for the L3 sale against the FIFO counterfactual is `12,816 − 10,334` =
**$2,482 credit** `[COMPUTED]`. Those figures are an illustration of the column's arithmetic,
not a recorded outcome.

## Best case, worst case, and the learning line

Every scored row carries three prose fields, because a number alone does not teach anything:

- **Best case.** What the lot choice produced when it worked: the delta, and the condition
  that made it work — for example, "the loss lot was also the weakest forward case, so the tax
  saving and the risk decision agreed".
- **Worst case.** What the lot choice cost when it failed: the delta, and the failure mode it
  fell into — for example, "the loss sale sat inside a 61-day box opened by a reinvestment
  purchase eleven days earlier; the loss was disallowed and became basis in the replacement".
- **Learning / key takeaway.** One sentence, written to be reusable: a rule to keep, a rule to
  retire, or a check to add to the pre-trade list.

A row without all three is an incomplete record, however precise its numbers.

## The placeholder block for a scored sale

```text
   decision_id:            ETL-<SYMBOL>-001
   tag:                    <LS|HL|WB|HP|YE|LR|DC|PS|SC>
   trade_date:             YYYY-MM-DD            # trade date, not settlement
   lots_consumed:          [{acquired, qty, basis_per_share, qty_remaining}, ...]
   relief_method:          specific-id | default-fifo | default-average | default-other
   instruction_written:    true | false
   gross_proceeds_usd:     $0.00                 [COMPUTED | ESTIMATED]
   realized_gain_usd:      $0.00                 [COMPUTED | ESTIMATED]
   character:              short-term | long-term | mixed
   rate_pair:              {short, long, as_of, source}
   tax_usd:                $0.00                 [COMPUTED] from realized_gain × rate
   after_tax_proceeds_usd: $0.00                 [COMPUTED]
   fifo_counterfactual_usd:$0.00                 [COMPUTED]
   delta_usd:              $0.00                 [COMPUTED]  ← the score
   box_start / box_end:    YYYY-MM-DD / YYYY-MM-DD
   reentry_date:           YYYY-MM-DD | none
   disallowed_loss_usd:    $0.00 | 0             [COMPUTED]
   non_tax_reason:         "<written before the tax reasoning>"
   validity_condition:     "<condition under which this stays right>"
   best_case:              "<delta + the condition that made it work>"
   worst_case:             "<delta + the failure mode it fell into>"
   learning:               "<one reusable sentence>"
   scoring_date:           YYYY-MM-DD
```

## What the corpus is for

Two questions only, and the format is designed so both are answerable from the rows:

1. **Does a tag beat the default?** Aggregate `delta_usd` by `tag` across a regime. A tag whose
   delta is zero or negative has bought nothing but an audit trail.
2. **Is a rule regime-dependent?** Aggregate `delta_usd` by `tag` per regime. A rule that wins
   in a correction and loses in an uptrend is not a rule; it is a condition.

**Known limitation of the corpus.** The delta measures the after-tax result of the lot choice
at a point in time. It does not measure whether the position should have been held at all —
that belongs to `equity-position-lifecycle`, and the two questions must be scored separately.
A positive delta on a position that should never have been owned is a correctly measured
mistake.

## Provenance discipline for every figure

| Tag | Meaning here | Requirement |
|---|---|---|
| `[VERIFIED]` | A rule traced to a named public source | The source is written beside the figure |
| `[COMPUTED]` | Arithmetic derived from stated inputs | The formula is shown |
| `[ESTIMATED]` | An assumed input | The assumption is named |
| `[BROKER-VERIFIED]` | True for one broker's published behaviour | The broker and the date are named |
| `[COMMON-PRACTICE]` | Desk convention with no vendor-independent source | Labelled as convention |

An untagged figure in a scored row is treated as unverified and is not aggregated.
