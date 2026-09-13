# Anti-Patterns

<!-- STANDARD: 3min -- the catalogue with detection heuristics -->

Each entry has a detection heuristic, so the pattern is findable rather than merely
recognisable after the fact.

## 1. The ad-hoc size ladder

**Symptom:** a product with eleven heading sizes, several within 2px of each other.
**Cause:** sizes chosen per screen with no declared base and ratio.
**Detection:** list every distinct `font-size` and look for pairs within 2px.

```bash
grep -rhoE 'font-size:\s*[0-9.]+(px|rem)' src/ | sort -u
```

**Fix:** declare base and ratio; regenerate the ladder; remap roles (R3).

## 2. `px` text sizes

**Symptom:** text does not respond to the browser's font-size preference.
**Cause:** designer-friendly units applied to a reader-controlled property.
**Detection:**

```bash
grep -rn 'font-size:.*px' src/ | grep -v 'hairline\|border'
```

**Fix:** `rem` for every text role; keep `px` only for hairlines and borders (R2).

## 3. Generic font fallback

**Symptom:** visible rewrap and a CLS spike on every cold load.
**Cause:** `font-family: Inter, sans-serif` with no metric-matched fallback.
**Detection:**

```bash
grep -rn 'font-family' src/ | grep -v 'Fallback' | grep -E 'sans-serif|serif|system-ui'
```

**Fix:** a metric-matched `@font-face` with `size-adjust` and ascent/descent overrides, plus a
measured shift (R1).

## 4. Tracking applied globally

**Symptom:** Arabic and Indic text renders with broken joins in some markets.
**Cause:** a `*` or `body` rule applying `letter-spacing`, intended for Latin display type.
**Detection:**

```bash
grep -rn 'letter-spacing' src/ | grep -E '^\S+:\s*(\*|body|html)'
```

**Fix:** remove tracking from global selectors; apply it only to specific display roles (R5).

## 5. Coverage by family name

**Symptom:** tofu for real users in a shipping locale.
**Cause:** "the family covers it" treated as evidence.
**Detection:** no glyph test exists in the repository for any locale.
**Fix:** prove coverage against the shipped file per locale (R5).

## 6. One scale for all locales

**Symptom:** CJK and Indic text reads as too small and dense at the Latin size.
**Cause:** a Latin-derived ladder applied unchanged to every script.
**Detection:** no `:lang()` base adjustment exists anywhere.
**Fix:** per-locale base multipliers, declared and recorded (see `references/type-scales.md`).

## 7. Fixed-height text containers

**Symptom:** content clipped when a reader applies the 1.4.12 overrides.
**Cause:** `height` (not `min-height`) on text containers, sized to the default line-height.
**Detection:**

```bash
grep -rnE 'height:\s*[0-9]+(px|rem)' src/ | grep -iE 'label|title|text|cell|badge'
```

**Fix:** `min-height` plus padding; let height come from content (R6).

## 8. Licence by assumption

**Symptom:** a release blocked by legal review days before launch.
**Cause:** "it is a free font" accepted as the licensing answer.
**Detection:** font binaries present with no adjacent licence record.
**Fix:** a licensing register with a permitted-context row per face (R4).

## 9. Proportional figures in tables

**Symptom:** columns never align; a data table cannot be scanned vertically.
**Cause:** figure style left at the font default for a tabular context.
**Detection:**

```bash
grep -rn 'tabular-nums' src/ | wc -l   # zero hits while tables exist
```

**Fix:** `tabular-nums` on every column context (Decision Tree 4).

## 10. Display cut strained to body sizes

**Symptom:** body text is tiring to read; perceived quality is low despite the "nice" font.
**Cause:** a display face used for 14px body text to keep the file count down.
**Detection:** one family used at both 48px and 14px with no distinct text cut.
**Fix:** a harmonised text companion, or move the display face to display roles only.

## 11. `font-variation-settings` reset

**Symptom:** optical sizing silently stops working after another axis is set.
**Cause:** `font-variation-settings` replaces the whole axis set rather than merging.
**Detection:**

```bash
grep -rn 'font-variation-settings' src/
```

**Fix:** use the high-level properties (`font-weight`, `font-stretch`, `font-style`); if the
low-level form is required, specify every axis meant to be controlled.

## 12. Unbounded fluid type

**Symptom:** text shrinks to illegible on a narrow window and grows without limit on ultrawide.
**Cause:** a viewport-relative term with no `clamp()` bounds.
**Detection:**

```bash
grep -rnE 'font-size:.*vw' src/ | grep -v clamp
```

**Fix:** `clamp(min, preferred, max)` with the floor above the stepped minimum (R2).

## 13. Measure by eye

**Symptom:** body lines that are 110 characters long on wide screens; fatigue in long reads.
**Cause:** a container width chosen visually, with no character-count check.
**Detection:** no `ch` or `max-inline-size` on prose containers.
**Fix:** `max-inline-size` in `ch`; verify on the longest real string.

## 14. Subset that drops a producible character

**Symptom:** tofu on user-generated or locale-specific input.
**Cause:** the subset derived from the design mockups rather than from content.
**Detection:** subset generation script reads from design files, not message catalogues.
**Fix:** derive from the union of every character the content can produce; test the extremes.

## Detection sweep

Run this before any release that touched type:

```bash
# Typographic anti-pattern sweep — cheap greps that catch most defects
set -euo pipefail
SRC="${1:-src}"

echo "== px text sizes (R2) =="
grep -rn 'font-size:.*px' "$SRC" 2>/dev/null | grep -viE 'hairline|border' || echo "  none"

echo "== zoom disablement (R2) =="
grep -rn 'user-scalable\|maximum-scale' . 2>/dev/null | grep -v node_modules || echo "  none"

echo "== global letter-spacing (R5) =="
grep -rn 'letter-spacing' "$SRC" 2>/dev/null \
  | grep -E ':\s*(\*|body|html)' || echo "  none"

echo "== unbounded fluid type (R2) =="
grep -rnE 'font-size:.*vw' "$SRC" 2>/dev/null | grep -v clamp || echo "  none"

echo "== fixed heights on text containers (R6) =="
grep -rnE 'height:\s*[0-9]+(px|rem)' "$SRC" 2>/dev/null \
  | grep -iE 'label|title|text|cell|badge' || echo "  none"

echo "== font binaries without a licence record (R4) =="
find . -type f \( -name '*.woff2' -o -name '*.ttf' -o -name '*.otf' \) \
  -not -path './node_modules/*' 2>/dev/null | while IFS= read -r f; do
    grep -q "$(basename "$f")" design/type-licensing.md 2>/dev/null \
      || echo "  $f — no register entry"
  done
```

Every hit is either a defect or a line worth annotating with why it is an exception. There is
no third category.
