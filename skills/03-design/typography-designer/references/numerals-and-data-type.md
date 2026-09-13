# Numerals and Data Type

<!-- STANDARD: 3min -- figure styles, disambiguation, data-table typography -->

## Why figures are a separate decision

The same typeface usually ships several figure styles, and choosing the wrong one for a
context produces a defect that is easy to see and hard to name: columns that never align, or
prose that jitters. Figure style is a semantic decision about the text's *job*.

## The styles

| Style | CSS | Character | Use |
|---|---|---|---|
| Proportional lining | `proportional-nums lining-nums` | even colour in prose; digits vary in width | body text, headings, labels |
| Tabular lining | `tabular-nums lining-nums` | uniform width; columns align | tables, metrics, pricing, spreadsheets |
| Proportional oldstyle | `proportional-nums oldstyle-nums` | digits with ascenders and descenders; blends into text | prose in an editorial face that has a true oldstyle cut |
| Tabular oldstyle | `tabular-nums oldstyle-nums` | uniform width with text figures | rare; oldstyle tables in editorial contexts |
| Diagonal fractions | `diagonal-fractions` | 1/2 rendered as a true fraction | recipes, measurements |
| Stacked fractions | `stacked-fractions` | vertical fraction | mathematics, limited contexts |
| Ordinals | `ordinals` | 1st, 2nd with a proper ordinal marker | English editorial; not applicable to most locales |
| Slashed zero | `slashed-zero` | 0 with a slash | identifiers, codes, financial data |

```css
/* Column context — align */
.table td, .metric-value, .price { font-variant-numeric: tabular-nums lining-nums; }

/* Prose context — even colour */
.prose, .card-title { font-variant-numeric: proportional-nums; }

/* Identifiers — disambiguate */
.serial, .iban, .account { font-variant-numeric: slashed-zero tabular-nums; }
```

## The alignment problem in one picture

```text
Proportional:                   Tabular:
┌────────────┐                  ┌────────────┐
│ Revenue     │                  │ Revenue     │
│ 1,111.00    │                  │ 1,111.00    │
│ 999.00      │  ← ragged        │   999.00    │  ← aligned
│ 12,345.67   │                  │ 12,345.67   │
└────────────┘                  └────────────┘
```

A column of proportional figures cannot be scanned vertically, because the eye has no fixed
reference for the digit positions. In a table whose entire purpose is comparison, that is a
functional defect, not a cosmetic one.

## Disambiguation

| Confusion | Cause | Fix |
|---|---|---|
| `0` vs `O` | rounded zero in many geometric faces | `slashed-zero`, or a face with a distinguishable zero |
| `1` vs `l` vs `I` | similar stems | choose a face whose `1` has a base serif or flag; use a mono for identifiers |
| `5` vs `S`, `8` vs `B` | uncommon but real in condensed faces | verify visually in the chosen face |
| decimal separator vs thousands separator | locale convention (`.`, `,`, narrow no-break space) | never format in CSS; use the locale's number formatter |

The disambiguation requirement is driven by the *content*: account numbers, licence keys,
serials and IBANs need a face that separates these glyphs. A marketing headline does not.

## Locale number formatting

Typography does not decide separators — the locale does. Never hard-code them.

```js
// Use the platform formatter; do not hand-roll separators
new Intl.NumberFormat("de-DE").format(1234567.89);   // "1.234.567,89"
new Intl.NumberFormat("en-US").format(1234567.89);   // "1,234,567.89"
new Intl.NumberFormat("fr-FR").format(1234567.89);   // "1 234 567,89" (narrow nbsp)
new Intl.NumberFormat("ar-EG", { numberingSystem: "arab" }).format(1234567.89); // Arabic-Indic digits
```

Two typographic consequences:

1. **The narrow no-break space** used by fr-FR and some locales is a real character that must
   be in the font subset, and must not be broken across lines in a number (it is
   non-breaking by definition — verify the font has it, or it substitutes).
2. **Arabic-Indic and other non-Latin digit sets** are separate codepoints. A font subset for
   `ar` that includes Arabic letters but not Arabic-Indic digits produces tofu exactly where
   the numbers are — which is usually in the most important cell of the table.

## Data-table typography

A table is the densest typographic artefact in most products. The rules:

| Element | Treatment | Why |
|---|---|---|
| Body cells | tabular figures, base step, `leading-snug` | alignment and row density |
| Header row | label role, weight 500–600, no tracking unless all-caps | distinguishable without a size change |
| Numeric columns | right-aligned (or decimal-aligned where supported) | comparison |
| Text columns | left-aligned | scanning |
| Units | in the header, not repeated per cell | removes repetition and shortens cells |
| Negative values | consistent treatment (minus sign or parentheses), colour as a secondary cue | colour alone fails contrast requirements |
| Totals row | weight and a top border, not a size change | hierarchy without inflation |
| Dense mode | one step down for body cells, leading reduced, never below 12px | legibility floor |

```css
/* Decimal alignment where the platform supports it */
.numeric-col { font-variant-numeric: tabular-nums; text-align: end; }
@supports (font-variant-numeric: decimal) {
  .numeric-col { font-variant-numeric: decimal tabular-nums; }
}
```

## Chart and axis typography

| Element | Treatment |
|---|---|
| Axis labels | caption step, tabular figures so tick values align |
| Value labels on bars | tabular figures; ensure contrast against the bar fill |
| Legends | label step; never tracked all-caps at small sizes |
| Tooltips | body step; ensure the tooltip's own contrast passes |
| Unit symbol | attach to the axis title, not every tick |

The typographic requirement specific to charts: **numbers in a chart must be tabular**, or the
tick labels themselves misalign and the reader cannot judge relative magnitude by position.

## Common defects

| Defect | Cause | Fix |
|---|---|---|
| Columns jitter | proportional figures in a table | `tabular-nums` (Decision Tree 4) |
| `0` read as `O` in an account number | no slashed zero | `slashed-zero` or a different face |
| `1,5` shown in an English UI | separator hard-coded, or the locale formatter not applied | use `Intl.NumberFormat` with the locale |
| Numbers tofu in an Arabic UI | subset lacks Arabic-Indic digits | extend the subset to the digit sets the locale produces |
| Fraction shows as `1/2` where `½` is intended | no fraction feature applied | `diagonal-fractions`, or use the precomposed character |
| Percentage sign separated from its number by a line break | no non-breaking space | bind the unit to the number with a non-breaking space |
| Currency symbol on the wrong side for the locale | symbol placement hard-coded | use the locale formatter, which places it correctly |

## Checklist

- [ ] Every column context uses tabular figures
- [ ] Prose and headings use proportional figures
- [ ] Identifier contexts use a slashed zero or a disambiguating face
- [ ] Number formatting delegated to the locale formatter, never hand-rolled
- [ ] Digit sets for every shipping locale present in the subset (including Arabic-Indic)
- [ ] Narrow no-break space present where the locale uses it
- [ ] Units in headers, not repeated per cell
- [ ] Negative-value treatment does not rely on colour alone
- [ ] Dense mode never drops below the legibility floor
- [ ] Chart tick labels use tabular figures
