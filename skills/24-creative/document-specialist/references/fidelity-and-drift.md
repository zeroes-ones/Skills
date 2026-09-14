# Fidelity and Drift

Every format conversion loses something. The professional move is to know what, check it, and say so.

## What drifts, and how often

| Element | Typical drift | Check |
|---|---|---|
| Pagination | Common | Page count, then visual |
| Fonts | Common (substitution) | Inspect rendered output |
| Table borders/widths | Common | Visual inspection |
| Formulas | Occasional | Recalculate and compare |
| Pivots | Occasional | Refresh and compare |
| Macros | Usually lost | State it explicitly |
| Tracked changes | Sometimes flattened | Decide accept/reject/preserve |
| Links/bookmarks | Often broken | Follow a sample link |
| Alt text/structure | Sometimes dropped | Accessibility check |

## Reporting rule

State what survived and what was lost. Never present a converted file as equivalent to its source
without having checked.

## Failure modes of conversion

- **Trusting the converter.** Drift is discovered by the customer.
- **Assuming macros survive.** A process silently loses its automation.
- **Flattening revisions silently.** A legal or review trail disappears.
- **Broken internal links.** A cross-referenced document no longer navigates.
- **Metadata from the source carried over.** The converted file leaks the original's properties.
