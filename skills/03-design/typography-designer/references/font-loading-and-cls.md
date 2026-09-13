# Font Loading and CLS

<!-- STANDARD: 3min -- fallback metric matching, subsetting, CLS measurement -->

## The problem in one sentence

A webfont and its fallback have different metrics, so when the webfont arrives every line
that was laid out with the fallback rewraps — and that rewrap is measurable layout shift
(CLS), which is a Core Web Vital with a ranking and user-experience consequence.

## The three-part fix

1. **Declare a metric-matched fallback** whose box metrics are adjusted to the webfont.
2. **Choose a `font-display` strategy** deliberately, per face.
3. **Measure the residual shift** on a named profile and record it.

You cannot skip step 1 — it is the only one that removes the shift rather than hiding it.

## Metric matching

```css
@font-face {
  font-family: "Inter var";
  src: url("/fonts/inter-var.woff2") format("woff2-variations");
  font-weight: 100 900;
  font-display: swap;
}

@font-face {
  font-family: "Inter Fallback";
  src: local("Arial");
  size-adjust: 107.12%;
  ascent-override: 90.2%;
  descent-override: 22.48%;
  line-gap-override: 0%;
}
```

Each descriptor has a job:

| Descriptor | What it does | Derived from |
|---|---|---|
| `size-adjust` | scales the fallback's glyphs so average advance width matches | ratio of the two fonts' average advance widths (or `unitsPerEm`-normalised `xAvgCharWidth`) |
| `ascent-override` | matches the line box's ascent | the webfont's `hhea.ascent` / `unitsPerEm` as a percentage |
| `descent-override` | matches the descent | the webfont's `hhea.descent` / `unitsPerEm` |
| `line-gap-override` | matches the gap some fonts add | the webfont's `hhea.lineGap` / `unitsPerEm` |

**Derivation, not eyeballing.** Read both fonts' metrics and compute the ratios:

```python
# Derive the overrides from the two fonts' actual metrics (R1)
from fontTools.ttLib import TTFont

def metrics(path):
    f = TTFont(path)
    upm = f["head"].unitsPerEm
    hhea = f["hhea"]
    return {
        "upm": upm,
        "ascent": hhea.ascent / upm,
        "descent": abs(hhea.descent) / upm,
        "lineGap": hhea.lineGap / upm,
        "avgWidth": f["hhea"].advanceWidthMax / upm,  # or OS/2 xAvgCharWidth
    }

web = metrics("fonts/inter-var.woff2")
fb  = metrics("/System/Library/Fonts/Supplemental/Arial.ttf")

print("size-adjust:",        f"{web['avgWidth'] / fb['avgWidth'] * 100:.2f}%")
print("ascent-override:",    f"{web['ascent'] / fb['ascent'] * 100:.2f}%")
print("descent-override:",   f"{web['descent'] / fb['descent'] * 100:.2f}%")
print("line-gap-override:",  f"{web['lineGap'] / fb['lineGap'] * 100:.2f}%" if fb['lineGap'] else "0%")
```

`advanceWidthMax` is a rough proxy for width. For a tighter match, compute the mean advance
width over a representative string (the first 200 Latin lowercase letters plus a space) in
both fonts, and take the ratio of those means. `adjustFontFallback` in Next.js and
`fontaine`/`nuxt-font-metrics` in other stacks automate exactly this.

## `font-display` decision

| Value | Block period | Swap period | Use when |
|---|---|---|---|
| `auto` | browser default | — | avoid; behaviour varies |
| `block` | ~3s invisible | infinite | never for body text — invisible text is worse than shifted text |
| `swap` | ~0s (fallback shown) | infinite | **above-the-fold text with a metric-matched fallback** |
| `fallback` | ~100ms | ~3s | text that must not shift after first paint |
| `optional` | ~100ms | ~0s | large payloads, non-critical text; the face is a cache-only enhancement |

The decision rule: **if the text is above the fold and you have done the metric matching, use
`swap`.** If you have not done the metric matching, `swap` converts an invisible-text problem
into a layout-shift problem — which is why R1 requires the fallback before the strategy.

## Subsetting

Subsetting reduces payload. It also creates a coverage hazard: if the subset omits a
character the content can produce, users see tofu (R5).

```css
/* One file per script block, so a Latin-only page never downloads CJK */
@font-face {
  font-family: "Noto Sans";
  src: url("/fonts/noto-latin.woff2") format("woff2");
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+2000-206F, U+2190-21BB, U+2212, U+2215;
}
@font-face {
  font-family: "Noto Sans";
  src: url("/fonts/noto-arabic.woff2") format("woff2");
  unicode-range: U+0600-06FF, U+0750-077F, U+FB50-FDFF, U+FE70-FEFF;
}
```

**Rule:** derive the subset from the union of every character the content can produce, not
from the design mockups. User-generated content and locale-specific punctuation are the
usual omissions. Re-derive when the content model changes.

**Shaping caution.** For joined scripts, subsetting must preserve the presentation forms the
shaper uses. A subset that keeps only base codepoints can render Arabic unjoined. Test
shaping after subsetting, not just codepoint coverage.

## Preloading

```html
<link rel="preload" as="font" type="font/woff2"
      href="/fonts/inter-var.woff2" crossorigin>
```

- Preload **only** the faces used above the fold, and only the exact file. Each preload is a
  connection the critical path must wait for.
- `crossorigin` is required even for same-origin fonts, because font fetches are CORS.
  Without it the browser downloads the font twice.
- Do not preload every subset. Preloading the CJK subset on a Latin page wastes the budget.

## Measuring the shift

Do not assert zero shift. Measure it, on a named profile.

```js
// Layout Shift entries attributable to font swap
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.hadRecentInput) continue;
    for (const source of entry.sources || []) {
      const el = source.node;
      // Flag shifts on text nodes — font swap is the common cause
      console.log("shift", entry.value, el?.nodeName, el?.textContent?.slice(0, 40));
    }
  }
}).observe({ type: "layout-shift", buffered: true });
```

Procedure:

1. Throttle to a named profile (for example "Slow 4G, 4× CPU slowdown") and record it.
2. Clear the font cache so the webfont genuinely arrives late.
3. Reload and capture the CLS value with the font-swap window open.
4. Compare before and after the metric-matched fallback. Record both numbers.
5. Repeat for each script subset that a shipping locale can trigger.

Target: font-attributable CLS approximately 0. A value above roughly 0.02 that traces to font
swap means the fallback is not matched for the face or the size that shifted.

## Payload budget

| Scope | Target | Why |
|---|---|---|
| All font requests, cold first view | ≤ 100 KB | beyond this the font competes with critical resources |
| Single variable font, Latin | 20–40 KB woff2 | typical for a variable Latin face with limited axes |
| Per script subset | ≤ 100 KB woff2 | CJK faces are large; subset by block and preload only what is used |
| Number of distinct faces above the fold | ≤ 2 (one text, one display) | each is a separate blocking resource |

## Ordering the decisions

```text
1. Choose the face and confirm the licence                    (R4, before design)
2. Derive the ladder                                         (R3)
3. Decide static vs variable                                 (Decision Tree 2)
4. Derive the metric-matched fallback                        (R1)
5. Choose font-display per face                              (this file)
6. Subset by unicode-range, derived from content             (R5)
7. Preload only the above-the-fold exact files
8. Measure the residual shift on a named profile             (R1)
```

Steps 4 and 8 are the ones teams skip, and they are the two that decide whether the shift is
fixed or merely hidden.
