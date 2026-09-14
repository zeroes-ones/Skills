# Contrast Pairing

<!-- STANDARD: 3min — role pairs, the partner rule, and the arithmetic of a resolved pair -->

## The partner rule

A contrast ratio is a property of **two** colours. Which two is decided by what paints on what, and
the answer is not "everything on the page background".

* An `on` role is painted on its base role. `onPrimary` sits on `primary`, not on the page.
* A base role is measured against its own `on` role when it carries text.
* A role with no text or icon on it (an outline, a divider) has no pair and no ratio. Recording
  "n/a" is the honest entry, not a number computed against the background.

Comparing every role to the page background produces two failures at once: a meaningless 1.00:1 for
the background itself, and the **wrong** ratio for every `on` role, because the pair never occurs.

## The reusable table

Generate the pairing table from the source, not by hand:

| Role (its partner) | Light | Dark | Contrast (light) | Contrast (dark) |
|---|---|---|---|---|
| `background` (vs `onBackground`) | … | … | … | … |
| `onBackground` (vs `background`) | … | … | … | … |
| `primary` (vs `onPrimary`) | … | … | … | … |
| `onPrimary` (vs `primary`) | … | … | … | … |
| `outline` | … | … | n/a | n/a |

Two things the table buys:

1. **The partner is explicit** in the header, so a reader cannot compute the wrong pair by accident.
2. **Both appearances are side by side**, which is how the asymmetric cases become visible: the
   colour that works on a light surface is frequently too pale or too deep for the dark one, which is
   why a single `error` role is wrong and a per-appearance error pair is right.

## The per-appearance asymmetry

The same semantic intent often needs two different primitives:

```text
error: { light: #8C2F2F, dark: #E8A0A0 }
```

A pale red on a cream surface fails contrast; a deep red on a warm charcoal surface fails it too.
The role is one; the primitive per appearance is two. That is what the middle tier exists for.

## The pairing errors that survive review

| Error | Why it survives | Fix |
|---|---|---|
| An `on` role measured against the page background | the number is real, the pair is wrong | measure against the base role it is painted on |
| Text on an accent fill using the page's text role | it looks plausible on a light accent and fails on a light one; a measured instance can sit near 3.3:1 while every gate reports clean | use the `on` role that pairs with the accent |
| An accent chosen at runtime with a fixed on-colour | a light accent needs dark text and a dark accent needs light text | choose the on-colour by relative luminance against a declared threshold |
| A spinner inside an accent-filled control keeping the page's colour | spinners are not text, so nobody checks them | treat any glyph inside the control as part of the same pair |
| A focus ring or border checked against the surface it sits on rather than the adjacent fill | borders are measured as decoration | measure a focus indicator against the colours adjacent to it |

## Deriving the on-colour for a runtime accent

Because the accent is user-chosen, the on-colour cannot be a constant. Declare the threshold and the
two candidates as parameters:

```text
onAccent = relativeLuminance(accent) > threshold ? darkOnAccent : lightOnAccent
```

The threshold and both candidates belong in the source with the derivation. A hardcoded
"always light text on the accent" is correct for the default accent and wrong for roughly half the
colours a user can pick — and the test for it is a parameter sweep, not a screenshot.

## What a role pairing does not prove

A passing pair proves the *token values* meet the floor. It does not prove the shipped screen meets
it, because:

* content may be composited over a translucent material, changing the effective background;
* an image or camera feed may sit behind the text;
* opacity applied at the call site changes the rendered colour without changing the token.

When the question is "does this shipped screen meet the floor?", escalate to `accessibility-auditor`
for measurement in the rendered artefact. This skill's job is to make the pairs correct and
explicit so that measurement has something well-defined to verify.

## Review questions for this section

1. Does every text or icon role name the role it is painted on?
2. Is any role compared against the page background by default?
3. Does each appearance have its own primitive where the asymmetry requires it?
4. Is the runtime on-colour chosen by a declared luminance threshold rather than hardcoded?
5. Are non-text glyphs inside a filled control included in the pair?
