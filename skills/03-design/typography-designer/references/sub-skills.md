# Sub-Skills

<!-- QUICK: 30s -- when to split into a narrower session -->

Typography is broad enough that a single session often cannot do all of it well. Split when the
work is clearly one of these, and stay in the main skill when the task genuinely spans several.

| Sub-skill | When to use it | Where it lives |
|---|---|---|
| `type-scale` | A ladder must be created, audited or replaced | `references/type-scales.md` — Decision Tree 1, ratio arithmetic |
| `font-selection` | Faces must be chosen, paired, or replaced | `references/pairing-and-hierarchy.md`, R4 licence gate first |
| `font-loading` | Swap shift, payload or a loading strategy is the problem | `references/font-loading-and-cls.md` — Decision Tree 2 |
| `variable-fonts` | Axes, optical sizing, static fallback decisions | `references/variable-fonts.md` |
| `script-coverage` | A locale's script must be made to render | `references/script-coverage.md` — Decision Tree 3 |
| `type-accessibility` | Resize, spacing, contrast or reflow is failing | `references/type-accessibility.md` — R2, R6 |
| `font-licensing` | Any question about whether a face may ship | `references/font-licensing.md` — R4 |
| `data-typography` | Tables, metrics, identifiers, charts | `references/numerals-and-data-type.md` — Decision Tree 4 |
| `type-measurement` | A budget must be established or a claim verified | `references/metrics-and-measurement.md` |

## Split when

- **One concern dominates.** "Make Arabic render" is `script-coverage`. Loading a Latin-only
  page is `font-loading`. Keep the session narrow and finish it.
- **The investigation needs a measurement harness** that does not exist yet. Build the harness
  in one session, apply it in the next.
- **The licence is unknown.** Nothing else can proceed (R4) — resolve that alone, then return.
- **The ladder is fragmented across hundreds of files.** Migrating a legacy scale is its own
  multi-session project; do not attempt it inside a design task.

## Stay whole when

- **The task is "set up the type system for a new product / locale set".** That genuinely spans
  scale, loading, coverage, licensing and conformance, and splitting it produces a scale with
  no loading strategy and a loading strategy with no coverage test.
- **A launch is imminent and the work is a conformance pass.** Run the sweep in
  `references/anti-patterns.md` plus the two-minute audit in
  `references/type-accessibility.md`; do not restructure the scale days before release.

## Adjacent skills, and the boundary

| Neighbour | They own | This skill owns |
|---|---|---|
| `brand-guidelines` | the brand's typographic *direction*, logo, identity system | the type system that expresses it in product |
| `ui-ux-designer` | design tokens and component architecture | the type token *family* within that system |
| `ui-ux-excellence` | interaction craft, heuristics, perceived quality | how type is measured and specified |
| `accessibility-auditor` | the whole-product WCAG audit and legal exposure | typographic conformance and its remediation |
| `localization-engineer` | i18n architecture, message pipeline, locale detection | the script and typography requirements those locales impose |
| `translation-manager` | TMS, MT quality, translation QA | nothing — a different discipline |
| `platform-hig-architect` | which platform convention wins where | the type roles, independent of platform |
| `performance-engineer` | the whole performance budget | the font payload and shift contribution within it |

The pattern: neighbours own the *system* and the *process*; this skill owns *type* — its
selection, its measurement, and its conformance.
