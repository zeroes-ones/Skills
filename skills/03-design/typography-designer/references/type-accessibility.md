# Type Accessibility

<!-- STANDARD: 3min -- WCAG criteria that apply to type -->

Typography is the highest-leverage accessibility surface in most products, because most of
what a user reads is text. Five criteria apply directly, and two of them — 1.4.4 and
1.4.12 — are the ones a type system usually fails.

## The five criteria

| Criterion | Level | What it requires of type |
|---|---|---|
| 1.4.3 Contrast (Minimum) | AA | text/background ≥ 4.5:1 normal, ≥ 3:1 large |
| 1.4.4 Resize Text | AA | text resizable to 200% without loss of content or functionality |
| 1.4.10 Reflow | AA | no two-dimensional scrolling at 320 CSS px width (≈ 400% zoom) |
| 1.4.12 Text Spacing | AA | no loss of content when the user overrides line, paragraph, letter and word spacing |
| 3.1.1 Language of Page | A | the language of the text is declared, so the reader and the shaper behave correctly |

## 1.4.4 Resize Text — the `px` trap

Text sized in `px` does not respond to the reader's font-size preference. This is the single
most common typographic conformance failure.

```css
/* ❌ ignores the reader's preference entirely */
body { font-size: 16px; }
h1   { font-size: 28px; }

/* ✅ anchored to the root, which the reader controls */
html { font-size: 100%; }      /* keep the default — do not set 62.5% just for arithmetic */
body { font-size: 1rem; }
h1   { font-size: 1.75rem; }
```

The companion failure is blocking zoom:

```html
<!-- ❌ fails 1.4.4 outright -->
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">

<!-- ✅ zoom allowed -->
<meta name="viewport" content="width=device-width, initial-scale=1">
```

`user-scalable=no` exists to suppress accidental double-tap zoom on a control. The correct fix
for that problem is `touch-action: manipulation` on the control, not disabling zoom for
everyone.

**The test.** Zoom the browser to 200%, and separately raise the root font size, then:

- No text is clipped by a fixed-height container.
- No text is truncated by `overflow: hidden`.
- No horizontal scrolling is introduced for text (1.4.10).
- No control becomes unreachable or overlapping.
- Fixed `px` widths on text containers are the usual culprit — use `ch`, `rem`, or `max-inline-size`.

## 1.4.12 Text Spacing — the fixed-height trap

The criterion specifies four overrides a user may apply, and requires that nothing is lost:

```css
/* The conformance test — apply all four at once */
* {
  line-height: 1.5 !important;
  letter-spacing: 0.12em !important;
  word-spacing: 0.16em !important;
}
p { margin-bottom: 2em !important; }
```

What breaks under these overrides, and the fix:

| Breakage | Cause | Fix |
|---|---|---|
| Label text clipped at the bottom | fixed container height sized to the original line-height | remove the fixed height; let height come from content |
| Button text cut off | `height` on the button rather than `min-height` plus padding | `min-height` + padding |
| Table rows overlap | fixed row `height` | `min-height` or content-driven rows |
| Card text overflows into the next card | fixed card height | `min-height`; allow growth |
| Truncation with no way to see the rest | `overflow: hidden` with `text-overflow: ellipsis` on essential text | allow wrapping, or provide the full text on focus/tap |
| Icons overlap adjacent text | fixed icon container interacting with the larger line box | space the icon with padding, not a fixed offset |

**Note the interaction with joined scripts:** the `letter-spacing: 0.12em` override breaks
Arabic and Indic rendering. This is a known tension in the criterion — the user's need to
override spacing versus the script's need to join. The correct engineering response is to
ensure the *layout* survives the override (nothing clipped or lost) even while the glyph
shaping degrades, and to keep the user's ability to turn the override off. Do not suppress the
override.

## 1.4.3 Contrast

Contrast is a type property because it depends on the rendered size and weight:

| Text | Threshold |
|---|---|
| normal text (below 18pt / 24px, or below 14pt / 18.66px bold) | 4.5:1 |
| large text (≥ 18pt / 24px, or ≥ 14pt / 18.66px bold) | 3:1 |
| incidental text (decorative, inactive) | exempt |
| the same text in `:hover`, `:focus`, `:active`, `:disabled` states | must also pass |

The typographic risks:

- **Caption and placeholder text** are usually the lightest grey and the most likely to fail.
  Placeholders in particular are frequently below 4.5:1.
- **Text over an image** needs a measurable background, not an assumed one. Use a scrim with
  a known contrast, not a gradient that happens to look fine.
- **Thin weights at small sizes** fail perceptually even at 4.5:1. At 300 weight under 14px,
  raise the threshold in your own standard — the criterion's floor is not a quality target.
- **Disabled states** are exempt from the criterion but must still be perceivable; a disabled
  label that is invisible is a usability defect regardless of conformance.

## 1.4.10 Reflow

At 320 CSS px viewport width (roughly 400% zoom on a desktop viewport), content must reflow to
one column without horizontal scrolling for text. Typographic contributors:

- long unbreakable strings (URLs, identifiers, long compounds) need `overflow-wrap: anywhere`
  on the containing text role;
- fixed `px` widths on text containers must become `max-inline-size` in relative units;
- tables of text must reflow or provide an accessible alternative, not scroll horizontally.

## 3.1.1 Language of page

```html
<html lang="ar">                            <!-- the page language -->
<p>Some English <span lang="en">inline text</span> here.</p>   <!-- inline language changes -->
```

Why typography cares: the language declaration drives hyphenation, line breaking, font
selection from the chain, and the correct shaping behaviour. An undeclared language is why
some products hyphenate German correctly and break Thai badly — the engine never knew.

For joined scripts, an undeclared `lang` on an inline Arabic run can cause the wrong shaping
form to be selected. Declare language at every boundary where the script changes.

## The typographic accessibility checklist

- [ ] No text size declared in `px` — all in `rem`
- [ ] `user-scalable=no` and `maximum-scale=1` absent
- [ ] 200% zoom: no clipped, truncated or overlapped text
- [ ] Root font-size increase: layout intact, no horizontal scroll for text
- [ ] All four 1.4.12 overrides applied simultaneously: nothing lost
- [ ] No fixed `height` on any text container (use `min-height` + padding)
- [ ] No `overflow: hidden` on essential text
- [ ] Every text/background pair checked at the rendered size and weight, including states
- [ ] Captions, placeholders and helper text checked — these fail most often
- [ ] Text over images uses a measurable scrim
- [ ] `overflow-wrap` set on user-generated and identifier text roles
- [ ] `lang` declared on the page and at every script-change boundary
- [ ] Joined scripts verified to render shaped joins with the product's real CSS applied

## The two-minute audit

Run this before any release that touched type:

```text
1. Search the codebase for `font-size:` with `px`            → every hit is a defect (R2)
2. Search for `user-scalable=no` and `maximum-scale`         → every hit is a defect (R2)
3. Search for fixed `height` on text containers              → likely 1.4.12 failure (R6)
4. Zoom one dense screen to 200%                             → look for clipping
5. Apply the four overrides to the same screen               → look for loss
6. Check the three lightest text colours against their surfaces
```

Steps 1, 2 and 3 are greps. They catch most typographic accessibility failures in seconds,
before an audit ever runs.
