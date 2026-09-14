# Theming and Roles

<!-- DEEP: 10+min — appearance versus accent, materials that cannot be tokens, chrome, and runtime derivation -->

## Two vocabularies, one screen

The rule that makes a theme enforceable: **the system's appearance governs the canvas, the product's
accent governs selection and identity.** Without that split, every screen makes its own choice and
"theming" becomes a per-screen decision that no gate can check.

| Follows the system appearance | Follows the accent | Is the platform's material |
|---|---|---|
| page and screen background | primary action fill | translucent surfaces |
| card, sheet, input surfaces | selected row or list item | system chrome (bars, sheets, dialogs) |
| body, heading, and muted text | segmented-control selection | the accent hairline *edge* on a container |
| icons and chevrons | badges | |
| dividers and hairlines | borders, focus rings, active indicators | |
| spinners on a surface | progress bars, tab indicators | |

The mental test: if it signals identity or selectedness, it is accent. If it is the canvas or the
content on it, it is system. If it composites what is behind it, it is a material and cannot be a
token.

## The raw-ramp defect, in full

A generator exposes the raw ramp so roles can be built from it. On one platform the raw ramp is
reachable from a screen as a plain colour constant. It **compiles**, renders correctly on a device
set to dark, and is **unreadable in light mode** — it does not adapt to the appearance setting at
all. A whole signed-out flow was written against the raw ramp and shipped permanently dark.

The generated token file **already contained the correct adaptive roles**. They were simply not
used. Five signals stayed silent, each for its own reason (see `token-tiers.md`). The fix was eight
files and one new gate.

What makes the new gate trustworthy is not that it runs:

* it reads the palette keys **from the generated token artifact**, so it cannot disagree with what
  the compiler sees;
* its exemption list is by name with the reason written in the script;
* it was **shown failing** on a deliberately reintroduced violation before it was trusted.

## A runtime accent is a derivation, not a colour

A user-selectable accent cannot be a compile-time constant. What *is* centralised is the **default
and the derivation parameters**: for each derived role, the saturation and lightness to pin, and the
luminance threshold used to choose the on-colour.

```text
border   = hue(accent), saturation 40, lightness 55–58   (per appearance)
subtleBg = hue(accent), saturation 22, lightness 93 / 14 (per appearance)
text     = hue(accent), saturation 45/55, lightness 35/78 (per appearance)
onAccent = relativeLuminance(accent) > 0.179 ? dark : light
```

Three properties make this design reviewable rather than magical:

1. **Hue is preserved, saturation and lightness are pinned.** Every accent the user picks yields a
   family that stays inside the product's tonal range, so the surrounding UI remains harmonious.
2. **The derivation is a pure function over (accent, appearance).** That is what makes it testable —
   a handful of tests covering hue preservation, role distinctness, appearance dependence, the
   luminance-chosen on-colour, and the colour-space round trip.
3. **Computing it inside the theme object makes every one of those tests unreachable.** A derivation
   buried in the theme is only observable by rendering a screen.

The failure this prevents is specific: mapping the accent onto only the primary/secondary/tertiary
roles leaves the derived border, subtle-background, and text roles on the old brand values, so a user
who picks a teal accent gets teal buttons with brand-amber borders — a half-converted app that reads
as "brand consistency" rather than as a bug.

## A material is not a token

Glass and blur composite the content behind them. There is no hex for "sample and blur what is
underneath", so the material cannot be a token:

| Is a token | Is the platform's |
|---|---|
| corner radius | the translucent material itself |
| the edge width of the hairline | how the backdrop is sampled and blurred |
| the shape it clips to | whether the platform provides it at all |

Two traps that exist on only one platform and read as correct in a screenshot:

* **A border call whose shape parameter defaults to a square.** Omit it and the border draws a
  rectangle while a preceding clip cuts the corners off — every surface renders with a border that
  stops short at each corner. Always pass the shape.
* **A control that draws its own border must have every such colour suppressed.** For an outlined
  text field that is the focused, unfocused, **error**, and **disabled** border colours — not just
  the first two. Missing the error one means the framework paints its own error stroke over the
  custom hairline whenever the field is in error: two borders, and the platform's wider one wins.

One mechanism per platform. A second, near-duplicate surface type is two places for a material change
to land, and one of them will be missed.

## Chrome: the platform's material, not a brand fill

A pushed screen's bar is the platform's own material. Painting it with the brand accent put a solid
brand slab directly on top of brand-edged containers below it — the accent used as a **fill**, which
the theming rule permits in exactly one control.

| Platform | The bar is | What is deliberately not done |
|---|---|---|
| one with a system navigation bar | the system material | no forced opaque background; no bar tint |
| one with a composed top bar | the same scheme-aware surface the containers use | no brand container colour; no custom back control |

Rules that generalise:

* **The root screen has no bar.** It is the front door, not a pushed detail; a bar there puts a title
  above a headline that is already the screen's title. Express that as *absent*, not *disabled* — a
  disabled back control still reads as "there is a way back".
* **The title is a localisation key**, and it comes from shared domain data, so the bar and the route
  cannot disagree about which screen is showing.
* **A hand-drawn back control breaks the system gesture.** On a platform without a system chevron in
  its composed bar, wire the visible control to the same callback the hardware back gesture uses, so
  the two cannot disagree.

## What the review must include

1. Page background uses the adaptive background role, not a fixed colour.
2. Text and icons use the `on` role paired with the surface they sit on — text on an accent panel
   needs that panel's on-colour, not the page's.
3. The accent is limited to actions, selection, segmented controls, badges, and borders; the one fill
   is the primary action.
4. Containers carry the material plus an accent edge rather than a flat brand card.
5. The bar is the platform's material, not a brand fill.
6. **Toggle the system appearance with the screen open.** The whole screen should change, not only
   the parts you remembered to make adaptive. This is the one step no tool performs, and it is the
   step that would have caught the raw-ramp defect before it was written.
