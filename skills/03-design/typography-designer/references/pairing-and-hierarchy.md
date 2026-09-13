# Pairing and Hierarchy

<!-- STANDARD: 3min -- pairing logic and hierarchy without size inflation -->

## Pairing is a decision about difference, not about taste

The question is never "which two fonts look nice together". It is: **what must differ, and by
how much, for the hierarchy to read?** Two faces that differ subtly create ambiguity; two that
differ wildly create noise. The pairing is chosen to make *roles* distinguishable.

## The three strategies

| Strategy | Description | Risk | Use when |
|---|---|---|---|
| **One family, many weights** | a single superfamily across all roles | risk of flatness; low risk of clash | most application UIs — the safest and fastest choice |
| **Two families, contrasting roles** | one for display/headings, one for body/UI | needs deliberate pairing; can clash | marketing-led products, editorial, brand-forward surfaces |
| **Superfamily** | a family designed with a matching sans/serif/mono set | none (that is its purpose) | systems needing serif + sans + mono coherence |

The most common production mistake is reaching for strategy 2 when strategy 1 would have been
correct. A well-built variable family with a real weight range gives a whole product its
hierarchy with one file and no pairing risk.

## Choosing a contrast axis when pairing

Pick **one** axis of difference and hold the others close. Multiple simultaneous differences
are what produce clash.

| Axis | Example pairing | Reads as |
|---|---|---|
| Serif ↔ sans | Source Serif ↔ Inter | editorial / authority |
| Geometric ↔ humanist | Poppins ↔ Lato | modern / friendly |
| Wide ↔ condensed | any ↔ condensed grotesque | editorial / data density |
| High contrast ↔ low contrast | Didone ↔ grotesque | luxury / utility |
| Monospace ↔ proportional | JetBrains Mono ↔ Inter | technical / code-led |

Hold constant wherever possible: **x-height, stroke weight, and overall optical texture.** Two
faces with very different x-heights will not sit on the same baseline comfortably, regardless
of how well their styles contrast.

## The practical pairing checklist

- [ ] **Same or compatible x-height.** Compare the two at the same nominal size; a large
      x-height difference makes the body text look smaller than it is.
- [ ] **Compatible stroke contrast.** A high-contrast display face next to a low-contrast text
      face works; two different high-contrast faces fight.
- [ ] **Licence coverage for both.** Two faces means two licences (R4).
- [ ] **Both cover the required scripts**, or the fallback chain is declared per role
      (Decision Tree 3).
- [ ] **Weight ranges overlap sensibly.** If the display face lacks a 400 and the body face
      lacks a 700, the roles cannot be met without synthesising weights (which looks wrong).
- [ ] **Figure styles compatible**, if numerals appear in both (Decision Tree 4).
- [ ] **Neither face is doing double duty badly.** A display face used for 14px body text is
      the most common pairing error.

## Hierarchy without size inflation

Size is the loudest hierarchy signal and the most destructive one to overuse. A product that
expresses every level purely with size ends up with eleven sizes and a page that shouts
uniformly.

The four signals, in order of subtlety:

| Signal | Strength | Cost |
|---|---|---|
| Size | loud | fragments the ladder; largest sizes consume layout |
| Weight | medium | safe, provided the weight set is declared |
| Colour / opacity | medium | risks contrast conformance (1.4.3) |
| Space (margin, leading) | quiet, most powerful | free; does not require a new size |

The expert move is **size for the top two levels, then weight and space for everything
below.** A card title differs from body text by weight and margin far more often than it needs
a new step.

```css
/* ❌ hierarchy by size alone — five sizes, no rhythm */
.card-title { font-size: 20px; font-weight: 400; margin: 0; }
.card-body  { font-size: 16px; font-weight: 400; margin: 0; }

/* ✅ size for the level, weight and space for the rhythm */
.card-title { font-size: var(--step-1); font-weight: var(--weight-semibold);
              line-height: var(--leading-snug); margin-block-end: var(--space-2); }
.card-body  { font-size: var(--step-0); font-weight: var(--weight-regular);
              line-height: var(--leading-body); }
```

## Role-to-style map

| Role | Size signal | Weight | Space | Tracking |
|---|---|---|---|---|
| display | +4 | 600–700 | generous above, tight below | negative |
| title-1 | +3 | 600 | generous above | negative |
| title-2 | +2 | 600 | standard above | 0 |
| title-3 | +1 | 500–600 | standard above | 0 |
| body | 0 | 400 | standard below | 0 |
| body-strong | 0 | 500–600 | as body | 0 |
| label | 0 | 500 | tight | 0 |
| caption | −1 | 400 | tight | 0 (contrast is the risk) |
| all-caps label | −1 | 500 | tight | **positive** |
| code | −1 | 400 | as body | 0 |

Note the pattern: only display through title-3 use size as the primary signal. Everything at
or below body relies on weight, space and colour. This is what keeps the ladder small.

## All-caps and small-caps

```css
.label-caps {
  font-variant-caps: all-small-caps;   /* or: text-transform: uppercase + tracking */
  letter-spacing: 0.06em;              /* caps need opening to read as a word */
  font-size: var(--step--1);
}
```

- **Never set all-caps with a negative or zero tracking** — caps read as an unbroken block
  without opening.
- **Never apply all-caps to text that came from the content layer** (user names, product
  titles, non-Latin scripts). Uppercasing is a Latin-only concept; applied to Arabic, Hebrew or
  CJK it does nothing or corrupts. Apply caps as a *display style to a known-Latin label*.
- **`text-transform` is presentational; screen readers may read the underlying text.** If the
  casing carries meaning, it belongs in the content, not the CSS.

## When the brand face cannot do the job

A brand display face frequently lacks a genuine text cut, real italics, or a weight range big
enough for UI. Three acceptable resolutions:

1. **Brand face for display roles only; a harmonised companion for text roles.** Declare the
   pairing and the contrast axis.
2. **Commission or license a text cut** from the same superfamily.
3. **Use the brand face at display sizes and accept a system face for body**, declared
   honestly rather than shipping a display cut strained to 14px.

What is not acceptable is stretching a display face to body sizes because it keeps the file
count down. The cost appears as reduced reading speed and increased fatigue across the whole
product, which is the most expensive place to pay it.

## Recording the pairing decision

In the State Log, record:

| Field | Example |
|---|---|
| Strategy | one family, many weights |
| Contrast axis | n/a (single family) |
| x-height match | n/a |
| Face(s) and licence | Inter, OFL-1.1 |
| Weight set | 400 / 520 / 620 / 700 |
| Roles on which face | all roles |
| Residual risk | brand headline face deferred to a later brand project |
