# Contrast and Colour

<!-- STANDARD: 3min -- ratio computation, non-text contrast and colour-independence -->

## Contrast is a design decision, fixed in tokens

Contrast is decided when the palette is chosen, not when a review happens. This is R6, and the
reason is arithmetic: a palette pairing that fails will fail in every component that uses it, so a
per-component fix guarantees the defect returns with the next component.

Fix it once, in the tokens, with a contrast-safe variant per surface.

## The computation

Relative luminance and contrast ratio, both computed from the sRGB values:

```python
def _channel(c):
    c = c / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def luminance(rgb):
    r, g, b = (_channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(fg, bg):
    l1, l2 = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

# Examples
print(round(contrast((0x76, 0x76, 0x76), (0xFF, 0xFF, 0xFF)), 2))   # grey on white
print(round(contrast((0x00, 0x30, 0x6B), (0xFF, 0xFF, 0xFF)), 2))   # navy on white
```

The ratio is symmetric: `contrast(a, b) == contrast(b, a)`. Only the two colours matter, not which
is text and which is background.

## The thresholds

| Content | Minimum | Where it applies |
|---|---|---|
| Normal text | 4.5:1 | Below the large-text size threshold |
| Large text | 3:1 | At or above the large-text threshold (size or bold-size) |
| Non-text: icons, borders, focus indicators, chart elements | 3:1 | Against the adjacent colour |
| Focus indicator | 3:1 against **both** the component and the page | The indicator must be visible wherever it appears |
| Decorative / inactive | exempt | But "inactive" is not a licence for invisible |

The specific size thresholds for "large text" are defined in the conformance criterion — confirm the
current figures rather than recalling them, since the definition has varied between versions.

## What actually fails, in practice

| Element | Why it fails | Frequency |
|---|---|---|
| Placeholder text | Styled lightest by convention | Very high |
| Caption / helper text | Treated as secondary, so made faint | Very high |
| Disabled controls | Exempt, but frequently invisible | High |
| Text over an image | Background assumed, not measured | High |
| Focus rings on dark surfaces | One ring colour for all surfaces | High |
| Chart labels and gridlines | Treated as decoration | High |
| Hover and visited states | Only the default state was checked | Medium |
| Text on a coloured badge/chip | Brand colour chosen for the surface, not the text | Medium |
| Borders that convey a control's boundary | Treated as decoration | Medium |

The pattern: contrast failures cluster in the **secondary** roles. The primary text is checked; the
helper text, placeholder and disabled state are not.

## Text over images

The background is not a colour; it is a photograph whose brightness varies.

| Solution | Effect |
|---|---|
| A scrim with a known opacity over the image | Produces a measurable background |
| A solid overlay band behind the text | Deterministic |
| A gradient scrim behind the text region | Works if the darkest point still passes |
| Measuring the worst-case pixel under the text | The rigorous approach |

What does not work: choosing a text colour that happens to look fine on the sample image. The
background must be *derived*, not assumed.

## Colour-independence

Colour must never be the only carrier of meaning.

| Meaning | Colour alone | Colour plus |
|---|---|---|
| Error | Red | Red text, an icon, and a border/marker |
| Success | Green | Green text, an icon, and a label |
| Status | A coloured dot | A dot plus a text label |
| Chart series | A colour per series | Distinct line styles or point shapes, plus a legend |
| Required field | An asterisk in a colour | The word "required" |
| Link in prose | A colour | An underline, or an obvious non-colour affordance |

Verify with a colour-blindness simulation across the common types. The test is simple: render the
interface in greyscale — is any meaning lost?

## Accessible palette construction

```text
1. Start from the brand's hues (do not fight the brand; derive from it).
2. For each surface (light, dark, elevated, high-contrast), define:
     - a text colour that passes 4.5:1 against it
     - a secondary text colour that passes 4.5:1 (NOT lighter than passing)
     - a non-text/border colour that passes 3:1
     - a focus indicator that passes 3:1 against both the surface and the component
3. Name the tokens by MEANING, not by value (--text-on-surface, --border-strong).
4. Compute and record the ratio for each text/surface pair in the token file.
5. Re-verify when the palette changes (R6).
```

Step 4 is what makes it durable: a recorded ratio is checkable, and a change that breaks it is
visible in review.

## The contrast test, automated

```js
// Walk every text node against its computed background (see ui-ux-excellence for the full script)
// Cover: default, hover, focus, active, disabled, visited, placeholder, and text over images.
// Report the lowest ratio per text role, not a pass/fail count.
```

Reporting the **lowest ratio per role** is more useful than a count of failures: it shows which role
is closest to the boundary and therefore which will break first when the design changes.

## The colour checklist

- [ ] Every text/surface pair meets 4.5:1 (normal) or 3:1 (large), in every theme (CR10)
- [ ] Every non-text pair (icons, borders, focus rings) meets 3:1
- [ ] Focus indicators are visible against both the component and the page, on every surface
- [ ] Placeholder, caption, helper and disabled roles are checked — not just primary text
- [ ] All states are checked: default, hover, focus, active, disabled, visited
- [ ] Text over images uses a derived, measurable background
- [ ] No meaning depends on colour alone; greyscale loses nothing
- [ ] Contrast-safe variants exist per surface, in the tokens
- [ ] Ratios are recorded in the token file, so a palette change is verifiable
- [ ] The palette is re-verified whenever it changes
