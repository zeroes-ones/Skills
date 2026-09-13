# Variable Fonts

<!-- STANDARD: 3min -- axis selection, optical sizing, static fallbacks -->

## What they change

A variable font is one file containing a *design space*. Instead of shipping Regular, Medium,
SemiBold and Bold as four files, one file interpolates between them. The trade:

| Gain | Cost |
|---|---|
| One payload instead of N | That payload is larger than any single static cut |
| Continuous weights — 450 is possible, not just 400/500 | Continuous values make it possible to invent 37 weights; discipline is required |
| `opsz` can adapt typography to size | Support caveats across older engines and PDF/print pipelines |
| Fewer requests on the critical path | Subsetting is harder (you cannot subset an axis away) |

## Registered axes

| Axis | Tag | Range typical | Use |
|---|---|---|---|
| Weight | `wght` | 100–900 | the axis almost every product needs |
| Width | `wdth` | 75–125 | condensed/expanded for dense layouts |
| Optical size | `opsz` | 6–144 | adapts stroke contrast and spacing to size |
| Slant | `slnt` | −15–0 | oblique without a separate file |
| Italic | `ital` | 0–1 | a true italic, not a slant |
| Grade | `GRAD` | −200–150 | changes weight **without** changing width — for dark-mode compensation |
| Custom | any 4-char | varies | e.g. `CASL`, `MONO` in some display faces |

**Unregistered/custom axes are the risk.** They are supported inconsistently by older engines,
by PDF export, and by design tooling. If an axis is custom, verify the whole pipeline renders
it before committing to it.

## Decision: which axes to keep

```text
Do you need more than one weight?
├── No → a static cut; skip variable entirely
└── Yes → is the weight change continuous (e.g. 450, 550) or discrete (400, 700)?
    ├── Discrete → static cuts may be cheaper and simpler
    └── Continuous → variable with `wght` only
        Does the same face span body and display sizes?
        ├── Yes → add `opsz` and enable `font-optical-sizing: auto`
        └── No  → keep `wght` only
        Need dark-mode compensation without reflow?
        ├── Yes → add `GRAD`
        └── No  → do not add it
Finally: verify every retained axis renders in every target engine, including PDF/print
```

Each retained axis increases file size and multiplies the QA surface. Retain the axes you
actually use; a font with eight axes that uses two is paying for six it never exercises.

## Optical sizing

`opsz` is the axis that separates a text cut from a display cut. At small sizes, optical
sizing typically increases spacing and stroke weight so the letterforms survive; at large
sizes it tightens spacing and sharpens stroke contrast.

```css
body  { font-optical-sizing: auto; }        /* the engine sets opsz from the rendered size */
.hero { font-optical-sizing: none; }        /* pin it if the automatic value is wrong */
```

Automatic optical sizing is the correct default. Override only when you have looked at the
result and the automatic value is wrong for the context — for example a large-size marketing
headline where you want the text cut's generosity deliberately.

## The weight-inflation trap

Continuous weights make it trivially easy to produce an inconsistent system:

```css
/* ❌ eleven weights across the product, none of them a decision */
.title  { font-weight: 640; }
.label  { font-weight: 520; }
.caption{ font-weight: 415; }
```

```css
/* ✅ a small declared set, mapped to roles */
:root {
  --weight-regular: 400;
  --weight-medium:  520;
  --weight-semibold:620;
  --weight-bold:    700;
}
```

Rule: decide the weight set **before** the variable font arrives, and map roles to it. The
font's capability is not an instruction to use all of it (R3's discipline applies to weights
as much as to sizes).

## Dark-mode compensation with `GRAD`

On dark backgrounds, light text appears heavier (irradiation) than dark text on light
backgrounds. The conventional fix is to reduce the weight on dark surfaces. Doing that with
`wght` changes the glyph *width*, so text reflows when the theme toggles — which is a layout
shift caused by a colour change.

`GRAD` exists for this: it changes apparent weight without changing advance widths, so the
line breaks stay identical.

```css
@media (prefers-color-scheme: dark) {
  :root { --font-grade: -25; }             /* slightly lighter, same widths */
}
body { font-variation-settings: "GRAD" var(--font-grade, 0); }
```

If the face has no `GRAD` axis, accept the slightly heavier appearance rather than trading it
for a theme-toggle reflow.

## Setting axes

Two syntaxes, and they behave differently:

```css
/* High-level properties — preferred; they animate and map to inheritance properly */
.headline { font-weight: 700; font-stretch: 90%; font-style: italic; }

/* Low-level — resets other axes to their defaults, so use sparingly and completely */
.headline { font-variation-settings: "wght" 700, "wdth" 90, "opsz" 48; }
```

**The `font-variation-settings` reset hazard:** setting it replaces the whole axis set. A rule
that sets `"wght" 700` will silently reset `opsz` and `wdth` to defaults, overriding an
inherited `font-optical-sizing: auto`. Prefer the high-level properties; if you must use the
low-level form, specify every axis you mean to control.

## Static fallbacks

Variable fonts are widely supported, but not universally, and not in every export pipeline.
The pragmatic position:

| Context | Approach |
|---|---|
| Modern web, evergreen browsers | variable font directly; no fallback needed |
| Web with a long-tail browser requirement | ship a static Regular + Bold, and treat the variable file as progressive enhancement |
| Native mobile | variable-font support is current on both platforms; verify the OS-version floor |
| Server-side PDF or print export | verify the pipeline renders axes; many export tools flatten to a default instance |
| Email | assume static only; variable support is not dependable |

**The failure mode to guard against** is a variable font loading where the engine does not
support it and rendering at the default instance silently — so the design's 700 weight looks
identical to 400. Test with the variable support disabled, not just enabled.

## Verifying a variable font

```python
# Which axes does this file actually contain, and what are their ranges?
from fontTools.ttLib import TTFont

f = TTFont("fonts/inter-var.woff2")
fvar = f.get("fvar")
if not fvar:
    print("not a variable font")
else:
    for axis in fvar.axes:
        print(f"{axis.axisTag:6s} {axis.minValue:>7.1f} .. {axis.maxValue:<7.1f} "
              f"default {axis.defaultValue:.1f}  ({axis.axisNameID})")
```

Checklist on receipt of a variable font:

- [ ] Axis tags and ranges read from the file, not from the marketing page
- [ ] Every axis you intend to use confirmed to render in each target engine
- [ ] The default instance identified (`fvar` default values) — that is what renders if axes are unsupported
- [ ] Subsetting verified to preserve the axes and any required shaping forms
- [ ] Payload compared against shipping equivalent static cuts, to confirm the trade is worth it
- [ ] For joined scripts, shaping re-verified after subsetting

## Payload comparison

The variable-font decision should be arithmetic, not preference:

```text
static option:  4 files × 28 KB  = 112 KB, 4 requests
variable option: 1 file  × 34 KB  =  34 KB, 1 request
                                    ────────────────
saving: 78 KB and 3 requests on the critical path
```

This is the case where the variable font clearly wins. The case where it does not:

```text
static option:  2 files × 22 KB = 44 KB, 2 requests   (Regular + Bold is all the design uses)
variable option: 1 file × 40 KB = 40 KB, 1 request
```

The saving is 4 KB and one request, and you have taken on axis-support QA across every engine
and export path. If the design uses two discrete weights, take the static cuts.
