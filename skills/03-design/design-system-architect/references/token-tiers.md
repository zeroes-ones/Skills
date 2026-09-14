# Token Tiers

<!-- STANDARD: 3min — the three tiers, what may read what, and why the middle tier is mandatory -->

## The three tiers

| Tier | Holds | Example shape | May be read by |
|---|---|---|---|
| **Primitive** | A raw value with no meaning beyond itself | a swatch (`#1A1713`), a numeric step (`18px`), an easing curve | semantic roles, design-system primitives. **Never a screen.** |
| **Semantic** | An intent that resolves per appearance | `background`, `onBackground`, `outline`, `primary`, `error` | screens, components, other semantic roles |
| **Component** | A slot inside one component | `buttonLabel`, `fieldHelper`, `rowSubtitle` | that component and its variants |

The tiers are a type system. Their purpose is to make one class of mistake **unwritable** rather
than merely discouraged — because that class of mistake compiles.

## Why the middle tier is not optional

A primitive has exactly one value. A screen needs a **pair** — the surface and the content on it —
and neither member of the pair can be derived from the other without knowing which appearance is
active.

The failure is specific and quiet: a generator exposes the raw ramp so the roles can be built from
it, and that exposure is reachable from a screen. On a device set to dark, reading the primitive
renders **correctly**. In light mode it is unreadable — and the compiler saw a valid colour, the
literal guard saw no hex, the test suites assert behaviour rather than colour, and the reviewer's
own phone was dark.

| Signal | Why it stays silent |
|---|---|
| The compiler | the primitive is a valid value of the right type |
| The literal guard | it looks for `#RRGGBB` and hand-built colours, not for a wrong-but-real token |
| Unit tests | colour is not behaviour, so nothing asserts it |
| A reviewer | they check on their own device, in their own appearance setting |
| The gate set | no gate covers colour *roles* |

When a defect is invisible to every existing signal, the answer is a new signal — not more care.

## What "resolve per appearance" means in the source

A semantic role points at a primitive per appearance:

```text
background:  { light: @cream,    dark: @charcoal }
onBackground:{ light: @charcoal, dark: @cream }
outline:     { light: @lightOutline, dark: @charcoalOutline }
```

Two consequences worth stating explicitly:

* The generator must **emit one adaptive constant per role**, not one constant per primitive. If the
  role is emitted as a compile-time constant of a single value, it cannot adapt, and screens will
  reach for the primitive instead.
* The raw ramp may still be generated — the roles are built from it — but nothing outside the
  design system may reference it. Reachability is not permission.

## A domain scale is the legitimate exception

A clinical or severity ramp is the same colour in every appearance: severity 4 is emergency red on
a dark device and on a light one. It is not an appearance-dependent role, so exempting it is
correct — but the exemption must be:

* **by name**, listing the exact members, never a wildcard over a tier;
* **with the reason written where the rule lives**, because an allow-list entry without a reason
  outlives the decision that justified it and silently permits the next violation of the class.

## What a material is not

A blur or glass effect composites whatever is behind it. There is no value for "sample and blur
what is underneath", so it cannot be a token. Shape, corner radius, and edge width are tokens; the
material is the platform's. Recording that in the source — and in the type — is what stops the next
contributor adding a `glass` colour token, or worse, reaching for a blur modifier that blurs the
content rather than the backdrop and is the opposite of the effect intended.

## Review questions for this section

1. Does every entry in the source sit in exactly one tier, and does its label say why?
2. Can any screen reach a primitive? If yes, what gate prevents it?
3. Is every semantic role emitted as one adaptive constant per platform, or as a fixed value?
4. Does every exemption from the primitive rule name its members and state its reason?
5. Is there any value in the source that is really a platform-owned property? If so, record it as
   non-tokenisable rather than tokenising it.
