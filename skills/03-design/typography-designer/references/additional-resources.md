# Additional Resources — typography-designer

> Deep knowledge loaded on demand. `SKILL.md` stays lean; extended material lives here and in
> the sibling reference files.

## Reference file map

| File | Covers |
|---|---|
| `core-workflow.md` | The ten phases as a runnable procedure with the arithmetic worked through |
| `type-scales.md` | Modular ratios, ladder generation, `clamp()` derivation, measure, leading, tracking, per-locale bases |
| `font-loading-and-cls.md` | Metric matching, `size-adjust` derivation, `font-display` decision, subsetting, preload, CLS measurement |
| `script-coverage.md` | Per-script requirements (Arabic, Indic, Hebrew, Thai, CJK, Latin) and the coverage test procedure |
| `variable-fonts.md` | Registered axes, optical sizing, the weight-inflation trap, `GRAD` for dark mode, payload comparison |
| `type-accessibility.md` | WCAG 1.4.3, 1.4.4, 1.4.10, 1.4.12, 3.1.1 applied to type, with the two-minute audit |
| `font-licensing.md` | Licence families, the contexts that matter, the register format, the CI gate |
| `pairing-and-hierarchy.md` | Pairing strategies, contrast axes, hierarchy without size inflation |
| `numerals-and-data-type.md` | Figure styles, disambiguation, locale number formatting, table and chart typography |
| `metrics-and-measurement.md` | The metric set, measurement scripts, the budget worksheet |
| `anti-patterns.md` | Fourteen patterns with detection heuristics and the sweep script |
| `error-decoder.md` | Twelve symptoms in long form: mechanism, diagnosis, fix, recurrence guard |
| `sub-skills.md` | When to split the session, and the boundary with adjacent skills |

## Extended example

`examples/backtest/README.md` runs a full type-system remediation against a stated scenario and
computes the cost of each failure mode arithmetically, with provenance tags.

## Source material

Primary standards and references this skill draws on. Verify against the current version before
citing a specific clause — standards and fonts both change (see the Anti-Hallucination section).

| Source | What it governs |
|---|---|
| WCAG 2.2 — Success Criteria 1.4.3, 1.4.4, 1.4.10, 1.4.12, 3.1.1 | Text contrast, resize, reflow, spacing overrides, language |
| W3C Internationalization (i18n) articles on script-specific typography | Per-script constraints: shaping, line breaking, spacing |
| CSS Fonts Module Level 4 | `size-adjust`, `ascent-override`, `descent-override`, `line-gap-override`, `font-optical-sizing` |
| CSS Fonts Module Level 5 / `font-variant-numeric` | Figure styles and numeric features |
| CSS Values: `clamp()`, `ch`, viewport units | Fluid scale derivation and measure |
| SIL Open Font License 1.1 text | The Reserved Font Name and redistribution conditions |
| OpenType `fvar` / `STAT` specifications | Variable-font axes and their naming |
| `fontTools` documentation | Reading metrics and cmap coverage programmatically |
| Bringhurst, *The Elements of Typographic Style* | Measure as characters per line; the 45–75 band |
| Web Vitals documentation (`layout-shift`) | CLS attribution and thresholds |

## Verification harness

`scripts/verify-skill.sh` asserts this skill's own invariants: that the scale is generated from a
declared base and ratio, that every webfont has a metric-matched fallback, that every locale has a
coverage test, that every face has a licence record, that no text is sized in `px` alone, and that
the resize and spacing conformance tests are declared. Run it before relying on the skill's output.
