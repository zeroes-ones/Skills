# Type Scales

<!-- STANDARD: 3min -- modular ratios, fluid derivation, per-locale adjustments -->

## Why a declared ratio

A ladder generated from a ratio has a rule. A ladder chosen step by step does not, which is
why products accumulate near-identical sizes: each new screen adds "just one more" heading
size because there is no rule to appeal to. The ratio is not a matter of taste — it is what
makes the tenth screen consistent with the first.

## Common ratios and when they fit

| Ratio | Name | Character | Fits |
|---|---|---|---|
| 1.067 | Minor second | Very tight | Dense data UIs needing many steps in a narrow range |
| 1.125 | Major second | Tight | Application UI, dashboards |
| 1.200 | Minor third | Balanced | Application UI, product marketing |
| 1.250 | Major third | Comfortable | Marketing, editorial |
| 1.333 | Perfect fourth | Expressive | Editorial, presentation |
| 1.414 | Augmented fourth | Strong | Magazine, hero-led pages |
| 1.500 | Perfect fifth | Dramatic | Display-led sites |
| 1.618 | Golden ratio | Extreme | Rarely usable beyond 4–5 steps |

Practical guidance: an application UI usually wants 1.125–1.2 with 6–8 steps. An editorial
product usually wants 1.25–1.333. A ratio above 1.5 creates steps so far apart that the role
between them has nowhere to live.

## Generating the ladder

```text
step(n) = base × ratio^n
```

For `base = 16`, the first eight steps:

| n | ratio 1.125 | ratio 1.2 | ratio 1.25 | ratio 1.333 |
|---|---|---|---|---|
| −2 | 12.6 | 11.1 | 10.2 | 9.0 |
| −1 | 14.2 | 13.3 | 12.8 | 12.0 |
| 0 | 16.0 | 16.0 | 16.0 | 16.0 |
| 1 | 18.0 | 19.2 | 20.0 | 21.3 |
| 2 | 20.3 | 23.0 | 25.0 | 28.4 |
| 3 | 22.8 | 27.6 | 31.3 | 37.9 |
| 4 | 25.6 | 33.2 | 39.1 | 50.6 |
| 5 | 28.8 | 39.8 | 48.8 | 67.4 |

Note how quickly 1.333 leaves the useful band: by step 4 the size is 50.6px, which is a
display size, not a title. This is the arithmetic reason high ratios need fewer steps.

## Rounding

Round the `px` value, then state the exact `rem`:

```text
raw  = base × ratio^n
px   = round(raw)
rem  = px / 16
```

Do not round to a "nicer" number. Adjusting 23px to 24px because 24 feels better is how a
ladder acquires an unstated second rule.

**Collision rule:** if two adjacent steps differ by less than 2px, the ratio is too shallow
for the step count. Either widen the ratio or delete a step. Two roles that differ by 1px are
not a hierarchy; they are noise that will be "fixed" differently on every screen.

## Fluid scales

Stepped ladders are correct when the design must be predictable. Fluid ladders are correct
when one design must serve a continuous range of widths without a breakpoint-specific size.

Derivation from two design points:

```text
slope     = (S2 − S1) / (W2 − W1)
intercept = S1 − slope × W1
preferred = intercept + slope × 100vw
```

Worked example — a title-1 that is 28px at 375px and 40px at 1440px:

```text
slope     = (40 − 28) / (1440 − 375) = 12/1065 = 0.011268 px/px
intercept = 28 − 0.011268 × 375      = 28 − 4.2254 = 23.7746px
preferred = 23.7746px + 1.1268vw
clamp     = clamp(1.75rem, 1.486rem + 1.127vw, 2.5rem)
```

Verify at three widths, not two: the two derivation points, plus one outside the range
(320px) to confirm the clamp floors correctly.

**The common fluid mistake** is using a viewport-relative term with no clamp bounds. Then
the text shrinks without limit on a narrow window and grows without limit on an ultrawide
one. Every fluid step needs both bounds, and the floor must not fall below the step's
stepped minimum (R2).

## Per-locale base adjustments

One scale for all locales is a Latin-centric assumption. Density differs by script:

| Script | Typical adjustment | Why |
|---|---|---|
| Latin | baseline | reference |
| Cyrillic, Greek | +0 to 1 step | similar x-height and density |
| Devanagari, Bengali, Tamil | +1 to 2 steps | matras and conjuncts sit above and below; the nominal size must be larger for equal legibility |
| Arabic, Persian, Urdu | +1 step | joined forms and diacritics reduce apparent size |
| Thai | +1 step | ascenders and descenders occupy more vertical space |
| CJK | +1 to 2 steps | glyphs are drawn to fill an em box; small sizes are dense |

Implement as a per-locale multiplier on the base, not a second global ladder:

```css
:root { --type-base: 1rem; }
:root:lang(ar), :root:lang(fa), :root:lang(ur) { --type-base: 1.0625rem; }
:root:lang(hi), :root:lang(bn), :root:lang(ta) { --type-base: 1.125rem; }
:root:lang(ja), :root:lang(ko), :root:lang(zh) { --type-base: 1.125rem; }
```

This keeps one ladder and one set of roles — the divergence is declared, bounded and
auditable rather than a parallel system. Record it in the State Log as a deliberate
divergence.

## Measure (line length)

Measure governs readability more than the typeface. It is a character count, not a pixel
width. Source: Bringhurst, *The Elements of Typographic Style*, frames measure as characters
per line with a comfortable band of roughly 45–75 for single-column body text.

```css
.prose { max-inline-size: 65ch; }
```

`ch` is the width of the `0` glyph in the current font, so it tracks the face automatically.
Verify against the longest real string, not placeholder text — a 78-character compound will
overflow a 65ch measure and needs a hyphenation or wrapping decision.

## Leading

Leading is a ratio, expressed unitless, so it inherits proportionally:

| Context | `line-height` | Reason |
|---|---|---|
| Display, titles | 1.1–1.2 | large type needs proportionally less |
| Labels, UI, table cells | 1.3–1.4 | single-line mostly; keeps tight rhythm |
| Body text | 1.5–1.65 | the readability band |
| CJK body | 1.7–1.9 | denser glyphs need more air |
| Code | 1.5 | align with body for mixed content |

A fixed `line-height` in `px` or `%` breaks the moment a nested element changes size, because
it no longer scales with the font. Unitless only, on every text role (R2).

## Tracking (letter-spacing)

| Context | Tracking | Note |
|---|---|---|
| Large display type | −0.01em to −0.02em | large type looks loose at default tracking |
| Body | 0 | do not track body text |
| Small caps, all-caps labels | +0.05em to +0.1em | caps need opening to read as a word |
| Joined scripts (Arabic, Indic, connected forms) | **0 — never track** | tracking breaks the joins (R5) |
| Monospaced code | 0 | the face is already tracked |

## Putting it together

```css
:root {
  --type-base: 1rem;
  --type-ratio: 1.2;
  --step--2: 0.6875rem;
  --step--1: 0.8125rem;
  --step-0:  1rem;
  --step-1:  1.1875rem;
  --step-2:  1.4375rem;
  --step-3:  1.75rem;
  --step-4:  2.0625rem;
}
```

Every role in the product references a `--step-*` token. No component declares a raw size.
That is the whole discipline: the ladder is generated, the roles are mapped, and nothing
downstream invents a number.
