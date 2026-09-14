# Financial Display Patterns

Numbers in a financial interface are the product. Formatting is not cosmetic.

## The rules

| Concern | Requirement |
|---|---|
| Sign | Never rely on colour alone; pair with `+`/`-` and an arrow or explicit label |
| Precision | Match the instrument — currency to 2dp, rates to 4dp, crypto by convention, never trailing zeros that imply false precision |
| Grouping | Locale-aware separators; never assume comma thousands |
| Alignment | Right-align numeric columns, decimal-align where precision varies |
| Staleness | Timestamp every quote; a stale price shown as live is the most damaging defect in this domain |
| Colour semantics | Fix one convention per product and honour it — in some markets red is up |

## Failure modes

- **Colour-only sign.** Colourblind users lose the direction entirely.
- **False precision.** Showing 8 decimals for a currency implies accuracy that does not exist.
- **Unlabelled staleness.** The user acts on a price that moved minutes ago.
- **Mixed colour conventions.** Region A shows red-as-down, region B red-as-up, and neither is labelled.
- **Layout shift on value change.** Digits that change width move every neighbouring column.
- **Locale-naive parsing.** Inputs accepted in one format are displayed in another, silently changing the value.
