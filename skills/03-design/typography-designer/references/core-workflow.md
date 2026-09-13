# Core Workflow — Type System Design

<!-- STANDARD: 3min -- the ten phases as a runnable procedure -->

The workflow in `SKILL.md` as a sequence you can run start to finish. Each phase has an
input, an action, and a check you can actually perform.

## Phase 1 — Content roles (20 min)

**Input:** the product's real screens, copy deck, or components.
**Action:** list every distinct text role the product renders. Not every size — every
*role*. Typical role set for an application:

```text
display      marketing hero, one per page at most
title-1      page title
title-2      section title
title-3      card or panel title
body         default reading text
body-strong  emphasised body, lead paragraphs
label        form labels, control text, table headers
caption      helper text, metadata, timestamps
code         monospaced identifiers and snippets
```

**Check:** for each role, you can state where it appears and why it is distinct from its
neighbour. If two roles always appear together and never differ in purpose, they are one
role.

**Record the extremes now** — they drive the measure and coverage tests later:

| Extreme | Example | Why it matters |
|---|---|---|
| Longest real string | a 78-character German compound or a 120-character product name | drives measure and truncation decisions |
| Shortest | a single character or an empty cell | a scale of one character is where letter-spacing reads as broken |
| Numeric | `1,234,567.89` in a table | drives figure style (Decision Tree 4) |
| Mixed script | a Latin brand name inside Arabic prose | drives the fallback chain |
| User-generated | names, addresses, emoji | drives coverage beyond the designed set |

## Phase 2 — Coverage matrix (20 min)

For each shipping locale, name the script and the requirements it imposes.

| Locale | Script | Direction | Joining | Word spaces | Coverage requirement |
|---|---|---|---|---|---|
| en-US | Latin | LTR | no | yes | ASCII + Latin-1 + typographic punctuation |
| de-DE | Latin | LTR | no | yes | as above + ß, umlauts; long compounds |
| ar-SA | Arabic | RTL | yes | yes | Arabic presentation forms for shaping |
| hi-IN | Devanagari | LTR | conjuncts | yes | consonants, matras, conjunct forms |
| th-TH | Thai | LTR | no | **no** | Thai block; no space-based breaking |
| ja-JP | CJK | LTR | no | no | kana, kanji, full-width punctuation |

**Check:** every shipping locale appears, and every requirement in the "coverage
requirement" column will be tested against the shipped file in Phase 6.

## Phase 3 — Licence check (15 min) — do this BEFORE design

Eliminate faces you cannot legally ship. See `references/font-licensing.md`.

| Question | Why it decides the face |
|---|---|
| Which licence? | OFL, Apache-2.0, commercial, proprietary — different grants |
| Web embedding allowed? | A desktop licence typically does not grant web use |
| App embedding allowed? | Separate grant; some licences forbid bundling in mobile binaries |
| Server-side rendering allowed? | Some licences scope use by rendering location |
| Subsetting and modification allowed? | Some licences forbid modification (which subsetting is) |
| Attribution required? | Drives a UI or documentation obligation, not just a file |
| Redistribution allowed? | Determines whether the file may sit in the repository |

**Check:** each remaining candidate is permitted for its actual shipping context, with the
grant written down. Do not proceed to Phase 4 with an unknown.

## Phase 4 — Scale (20 min)

Declare the base and the ratio, then generate. Arithmetic, not taste.

```text
base  = 16px (1rem) — the browser default; do not change it
ratio = 1.2 (application UI) or 1.25–1.333 (editorial)

step(n) = base × ratio^n        # n = 0 is the base step
```

For `base = 16` and `ratio = 1.2`:

| n | raw px | rounded px | rem | typical role |
|---|---|---|---|---|
| −2 | 11.11 | 11 | 0.6875 | caption (small) |
| −1 | 13.33 | 13 | 0.8125 | caption, label |
| 0 | 16.00 | 16 | 1.0 | body, label, table |
| 1 | 19.20 | 19 | 1.1875 | title-3 |
| 2 | 23.04 | 23 | 1.4375 | title-2 |
| 3 | 27.65 | 28 | 1.75 | title-1 |
| 4 | 33.18 | 33 | 2.0625 | display (UI) |

Two rules when rounding:

1. **Round to whole `px` for the rem conversion**, then express exactly in `rem`. A
   non-integer `rem` produces fractional device pixels and inconsistent stem weights.
2. **Never let two steps land within 2px of each other.** If they do, the ratio is too
   shallow for the step count — widen the ratio or drop a step (R3).

For a fluid step, derive `clamp()` from two design widths rather than guessing:

```text
Given: size is S1 at viewport W1, and S2 at viewport W2 (W1 < W2)
slope     = (S2 − S1) / (W2 − W1)                 # px per px of viewport
intercept = S1 − slope × W1                       # px at zero viewport
preferred = intercept + slope × 100vw             # expressed in vw units

clamp(min, preferred, max)
  min = S1 rounded down to the previous step
  max = S2 rounded up to the next step
```

Worked example, body 16px at 320px viewport growing to 18px at 1280px:

```text
slope     = (18 − 16) / (1280 − 320) = 2/960 = 0.0020833 px/px
intercept = 16 − 0.0020833 × 320      = 16 − 0.6667 = 15.3333px
preferred = 15.3333px + 2.0833vw
CSS       = clamp(1rem, 0.9583rem + 2.0833vw, 1.125rem)
```

**Check:** every step traces arithmetically to base and ratio; the fluid form is verified at
320px, 1280px and 2560px, and at 200% text resize (R2).

## Phase 5 — Role mapping (15 min)

Assign each role a step, a weight, a leading and a measure. Leading is unitless.

```css
:root {
  --type-base: 1rem;
  --type-ratio: 1.2;
  --leading-tight: 1.15;   /* display and titles */
  --leading-snug:  1.35;   /* labels, UI */
  --leading-body:  1.6;    /* reading text */
  --measure-body:  65ch;   /* characters, not pixels */
}
```

| Role | Step | Weight | Leading | Notes |
|---|---|---|---|---|
| display | +4 | 600 | leading-tight | negative tracking allowed |
| title-1 | +3 | 600 | leading-tight | |
| title-2 | +2 | 600 | leading-tight | |
| title-3 | +1 | 500 | leading-snug | |
| body | 0 | 400 | leading-body | measure-body applies |
| label | 0 | 500 | leading-snug | never tracked |
| caption | −1 | 400 | leading-snug | contrast is the risk here |
| code | −1 | 400 | leading-snug | monospaced; no optical sizing |

**Check:** every role resolves to tokens; no role holds a raw value; no two roles share a
step unless they deliberately differ only by weight or leading.

## Phase 6 — Script coverage (30 min)

Prove coverage against the shipped file. See `references/script-coverage.md`.

```bash
# List every character the content can produce, deduplicated
# (from the message catalogues, not from the design mockups)
python3 - <<'PY'
import glob, json, re, sys
chars = set()
for f in glob.glob("locales/**/*.json", recursive=True):
    chars |= set(re.sub(r"\{[^}]*\}", "", json.load(open(f)).__str__()))
print("".join(sorted(chars)))
PY
```

Then test the shipped font's coverage (any tool that reports cmap coverage works):

```bash
# Example with fonttools — report codepoints the file does not cover
python3 - <<'PY'
from fontTools.ttLib import TTFont
import glob
required = set(open("/tmp/required-chars.txt").read())
for path in glob.glob("public/fonts/*.woff2"):
    f = TTFont(path)
    covered = {chr(c) for t in f["cmap"].tables for c in t.cmap}
    missing = sorted(required - covered)
    print(path, "missing:", "".join(missing) or "none")
PY
```

**Check:** for every locale, zero missing characters from the shipped chain; and for joined
scripts, a visual shaping check confirms the joins render.

## Phase 7 — Loading (25 min)

Run Decision Tree 2. The deliverable is a block per face, like this:

```css
/* The webfont */
@font-face {
  font-family: "Inter var";
  src: url("/fonts/inter-var.woff2") format("woff2-variations");
  font-weight: 100 900;
  font-display: swap;
  unicode-range: U+0000-00FF, U+0131, U+2000-206F, U+2190-21BB, U+2212, U+2215;
}

/* Metric-matched fallback — overrides derived from the two fonts' metrics (R1) */
@font-face {
  font-family: "Inter Fallback";
  src: local("Arial");
  size-adjust: 107.12%;
  ascent-override: 90.2%;
  descent-override: 22.48%;
  line-gap-override: 0%;
}
```

**Check:** shift measured on a named throttled profile and recorded; the metric overrides
come from published metrics, not from eyeballing.

## Phase 8 — Numerals and details (15 min)

Per Decision Tree 4, then set punctuation and optical sizing:

```css
.table-cell   { font-variant-numeric: tabular-nums lining-nums; }
.prose        { font-variant-numeric: proportional-nums; }
.display      { font-optical-sizing: auto; }   /* variable opsz axis */
```

**Check:** every numeric context states its figure style; 0/O and 1/l/I verified in the
chosen face wherever they can be confused.

## Phase 9 — Conformance (30 min)

Test the two typographic WCAG criteria that most type systems fail. See
`references/type-accessibility.md`.

| Test | How | Pass |
|---|---|---|
| 1.4.4 Resize text | Browser zoom to 200%; also raise the root font size | No content lost, no clipped text, no horizontal scrolling for text |
| 1.4.12 Text spacing | Apply all four overrides: `line-height: 1.5`, `margin-bottom: 2em` on paragraphs, `letter-spacing: 0.12em`, `word-spacing: 0.16em` | No content lost, no overlap |
| 1.4.3 Contrast | Check text/background pairs at the actual rendered size and weight | 4.5:1 normal, 3:1 large |
| 1.4.10 Reflow | 320px width, 400% zoom equivalent | No two-dimensional scrolling for text |

**Check:** all four recorded with the tool and the result, not asserted.

## Phase 10 — Budget and record (15 min)

Type has a measurable budget. Record it.

| Metric | How measured | Typical target |
|---|---|---|
| Font payload (first view) | Transfer size of font requests on a cold load | ≤ 100 KB total |
| CLS contribution from fonts | Layout Shift entries attributable to font swap | ≈ 0 |
| Characters per line (body) | `ch` measurement on real content | 45–75 |
| Largest text size in a container at 200% | Overflow check | no clipping |
| Contrast minimum across text roles | Automated pass over all role/surface pairs | ≥ 4.5:1 normal text |

Record every licence and every measured value in the State Log. The next engineer needs the
*why*, and the licence register needs the *what*.
