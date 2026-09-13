# Additional Resources — Verification Independence Engineer

> Deep knowledge loaded on demand. SKILL.md holds the decisions and rules (R1-R6, the four
> decision trees). The extended material lives in the focused files below.

| Reference file | What it holds |
|----------------|---------------|
| [`independence-properties.md`](independence-properties.md) | Independence is a set of four properties, not a label. This file holds the detail and the enforcement test for each |
| [`metric-leak-catalogue.md`](metric-leak-catalogue.md) | Every optimised metric is a proxy. This catalogue names, for common metrics, the intent they stand for, the cheapest path that satisfies the number while betraying it, and the harm metric that guards it |
| [`calibration-recipes.md`](calibration-recipes.md) | A verdict is a measurement, so it needs a known-good reference. These recipes build the known-bad set and the four numbers that say whether a validator is awake |
| [`failure-narratives.md`](failure-narratives.md) | Anonymised narratives of verification that reported success while correctness degraded. Each ends with the rule it justifies |
| [`verification-recipes.md`](verification-recipes.md) | The checks in SKILL.md's Verification section, written as runnable procedures rather than aspirations |
| [`sources.md`](sources.md) | Every claim in SKILL.md and these reference files traces to a source below, tagged by strength. |
| [`related-reading.md`](related-reading.md) | The skills this one consumes from and feeds into, and what each relationship is for. |

---

## How to use these files

- Starting an independence audit → `independence-properties.md` (the four axes and the
  hiding test), then `verification-recipes.md` for the runnable checks.
- A green metric with a worsening outcome → `metric-leak-catalogue.md`.
- A validator nobody trusts → `calibration-recipes.md`.
> Provenance for every claim: `sources.md`. Estimated figures are explicitly marked.
