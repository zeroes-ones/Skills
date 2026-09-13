# Error Decoder — Long Form

<!-- DEEP: 5+min -- the symptom catalogue in long form, with causes and fixes -->

The compressed table lives in `SKILL.md`. This file carries the full diagnosis: the symptom as
it actually appears, the mechanism, the fix, and what to change so it cannot recur.

## 1. The page rewraps when the webfont loads

**Symptom:** on a cold load, text visibly reflows a moment after first paint. Lighthouse
reports CLS 0.08–0.25 on mobile. The layout is stable on the developer's machine.

**Mechanism:** the fallback and the webfont have different average advance widths and vertical
metrics, so every line that was laid out with the fallback re-wraps when the real face arrives.
Desktop with a warm cache never sees it because the font is already there.

**Diagnosis:**

```js
new PerformanceObserver((l) => {
  for (const e of l.getEntries()) {
    if (!e.hadRecentInput) console.log(e.value, (e.sources||[]).map(s=>s.node?.nodeName));
  }
}).observe({type:"layout-shift", buffered:true});
```

If the shift sources are text nodes within a few hundred milliseconds of load, and the font
request completes in that window, this is the cause.

**Fix:** derive a metric-matched fallback from the two faces' actual metrics (see
`references/font-loading-and-cls.md`), then re-measure on a throttled profile with the cache
disabled. Report both numbers.

**Recurrence guard:** the fallback `@font-face` is a required deliverable of the type system,
not a follow-up ticket. A new face without one is not mergeable (R1).

## 2. Text will not enlarge

**Symptom:** a user raises their browser's font-size setting and the site does not change. On
iOS, text scaled up in Accessibility settings does not enlarge the page's text.

**Mechanism:** `font-size` in `px` is an absolute unit that ignores the root font-size
preference. The user's setting changes the root; `px` text does not care.

**Diagnosis:**

```bash
grep -rn 'font-size:.*px' src/ | grep -viE 'hairline|border'
```

Any hit on a text role is a diagnosis.

**Fix:** re-author in `rem`. Set `html { font-size: 100% }` and keep it — a habit of setting
`62.5%` to make arithmetic easier reintroduces the problem by overriding the user's setting
with a fraction of it.

**Recurrence guard:** the `px` grep runs in CI and fails on text roles (R2).

## 3. Arabic or Devanagari text renders with broken joins

**Symptom:** Arabic words appear as separated letterforms rather than connected script.
Devanagari conjuncts render as stacked or detached glyphs. Fluent readers describe it as
"wrong" immediately; a non-reader sees nothing amiss.

**Mechanism:** one of three causes, in order of likelihood:

1. **`letter-spacing` inherited from a global selector.** Tracking inserts space between
   glyphs and breaks joining — the shaper cannot connect across the inserted space.
2. **A subset that dropped presentation forms.** The base codepoints are present but the
   contextual forms the shaper needs are not, so it falls back to isolated forms.
3. **A face that never had shaping forms** for that script (a Latin-only family with partial
   Arabic coverage).

**Diagnosis:**

```bash
# Cause 1 — is tracking inherited from a broad selector?
grep -rn 'letter-spacing' src/ | grep -E ':\s*(\*|body|html)'

# Cause 2 — does the shipped subset contain presentation forms?
python3 - <<'PY'
from fontTools.ttLib import TTFont
f = TTFont("public/fonts/subset.woff2")
cps = {cp for t in f["cmap"].tables for cp in t.cmap}
forms = [c for c in range(0xFE70, 0xFF00) if c in cps]   # Arabic presentation forms
print("presentation forms present:", len(forms))
PY
```

**Fix:** remove tracking from joined scripts (R5); re-subset preserving shaping forms; verify
by rendering on a device with the product's real CSS.

**Recurrence guard:** a rendering test in the visual regression suite for every joined-script
locale, and the `* { letter-spacing }` grep in CI.

## 4. Tofu boxes for some users

**Symptom:** a small proportion of users in a locale see `□` where characters should be.
Support tickets arrive with screenshots. Developers cannot reproduce it.

**Mechanism:** coverage was assumed from the family name. The shipped file — usually a subset —
lacks some characters. The characters that trigger it are the ones not present in the design
mockups: unusual diacritics, locale-specific punctuation, Arabic-Indic digits, or
user-generated input.

**Diagnosis:** compare every character the content can produce against the shipped file's cmap
(see `references/script-coverage.md` §2). Include the user-input path.

**Fix:** extend the subset; add a per-script family to the fallback chain.

**Recurrence guard:** coverage is a test in CI, run against the shipped files, derived from the
content — re-run whenever the content model or the font version changes (R5).

## 5. Content clipped under text-spacing overrides

**Symptom:** a user with a spacing override (or an auditing tool applying 1.4.12) sees labels
cut off at the bottom, button text truncated, or table rows overlapping.

**Mechanism:** text containers with a fixed `height` sized to the default line-height. When the
line box grows, the container does not.

**Diagnosis:** apply the four overrides and look for clipping.

```css
* { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important; }
p { margin-bottom: 2em !important; }
```

**Fix:** replace `height` with `min-height` on text containers; remove `overflow: hidden` from
essential text; let padding create the space.

**Recurrence guard:** the override test runs on the densest screens before release (R6).

## 6. The heading hierarchy has eleven sizes

**Symptom:** a codebase with `font-size` values 26, 28, 30, 32 for four "different" heading
levels, and no one can explain the difference between `h3` and `.subtitle`.

**Mechanism:** no declared ratio, so every new screen added a size rather than reusing a step.
This compounds: by the time it is noticed, the sizes are load-bearing in hundreds of files.

**Diagnosis:** list distinct sizes and count pairs within 2px.

**Fix:** declare base and ratio; generate the ladder; remap roles to steps; migrate
incrementally by role rather than by find-and-replace.

**Recurrence guard:** no component may declare a raw `font-size`; sizes come from tokens (R3).

## 7. Table figures jitter and columns never align

**Symptom:** a numeric column where the digits do not line up vertically, so the eye cannot
compare magnitudes down the column.

**Mechanism:** the font's default figure style is proportional, which is correct for prose and
wrong for columns.

**Fix:** `font-variant-numeric: tabular-nums lining-nums` on the column context.

**Recurrence guard:** a lint rule or review checklist item: any table cell containing a number
uses tabular figures (Decision Tree 4).

## 8. Legal exposure from a font licence

**Symptom:** legal review blocks a release, or a demand arrives after launch. The font is in
the app binary but the purchased licence covered desktop use only.

**Mechanism:** "it is free" or "we have a licence" conflated the design-phase grant with the
shipping grant. App embedding, server rendering and redistribution are usually separate.

**Diagnosis:** audit every font binary against the licensing register, per shipping context.

**Fix:** obtain the correct grant, or replace the face. Replacement invalidates the scale
metrics and fallback work, which is why it is expensive.

**Recurrence guard:** the register precedes the design (R4); a CI gate fails on any binary
without a permitted-context entry.

## 9. Small text legible on desktop, illegible on device

**Symptom:** a 12px caption is readable in the design tool and on a desktop monitor, and
unreadable on a phone in daylight.

**Mechanism:** verification happened at high DPI with desktop antialiasing, which renders small
text more clearly than a phone's subpixel arrangement. Hinting and stem darkening differ.

**Fix:** test at real sizes, on the real target device, in the real locale. Raise the floor: 12px
is a practical minimum, and caption text below it needs a deliberate justification.

**Recurrence guard:** device testing is a checklist item for any change to the small end of the
ladder.

## 10. Optical sizing silently stops working

**Symptom:** a variable face with an `opsz` axis no longer adapts; display sizes look loose and
body sizes look tight, exactly as if `opsz` were pinned.

**Mechanism:** a later rule set `font-variation-settings: "wght" 600`, which replaces the entire
axis set and resets `opsz` to its default — overriding an inherited
`font-optical-sizing: auto`.

**Diagnosis:**

```bash
grep -rn 'font-variation-settings' src/
```

**Fix:** use the high-level properties; if the low-level form is necessary, list every axis you
mean to control.

**Recurrence guard:** the low-level syntax is banned by convention where an equivalent
high-level property exists.

## 11. Unused weights and axes ship in the payload

**Symptom:** a variable font payload of 90–140 KB where the design uses two weights.

**Mechanism:** the full axis range was retained "in case". Each retained axis increases file
size, and each unused weight is a value someone will eventually apply inconsistently.

**Diagnosis:** compare the declared weight set against the values actually used.

```bash
grep -rhoE 'font-weight:\s*[0-9]+' src/ | sort -u
```

**Fix:** drop unused axes from the file where the toolchain supports instancing; declare a small
weight set and map roles to it.

**Recurrence guard:** payload budget tracked per release; the declared weight set is part of the
type system's documentation.

## 12. Numbers tofu in an Arabic or Devanagari UI

**Symptom:** the table renders correctly except the digits, which show as boxes. Usually the
most important cell.

**Mechanism:** the subset preserved the script's letters but not its digit set. Arabic-Indic
(٠١٢…) and Devanagari digits are distinct codepoints from ASCII digits.

**Fix:** extend the subset to the digit sets the locale's formatter produces; verify with the
content's real numbers.

**Recurrence guard:** coverage tests include the digit sets for every shipping locale
(see `references/numerals-and-data-type.md`).

## The triage rule

Three of these symptoms — rewrap, resize failure, and spacing clipping — are detectable by
grep and a zoom test in under two minutes, and they account for most typographic defects found
in the wild. Run the sweep in `references/anti-patterns.md` first; escalate to the deeper
diagnosis above only when the sweep is clean and the defect persists.
