# Component Specification Template

<!-- STANDARD: 3min — the eight-part spec that makes a component reviewable and implementable -->

A component belongs to the design system when it has a written specification. The spec has eight
parts, and each part exists because omitting it produced a specific class of defect.

## The eight parts

| Part | Contains | Omitting it causes |
|---|---|---|
| **Purpose** | one sentence: what job this control does, and where it is used | two controls that do the same job, or one used where another belongs |
| **Anatomy** | an ASCII diagram of the parts, with each named | implementers invent parts the designer did not intend |
| **Variants** | every named variant, and what changes between them | a variant implemented as a hand-tuned copy |
| **Sizes** | the size tokens the component reads, and which axis each is on | a dimension borrowed from the spacing scale |
| **States** | a table: state → visual treatment, every role named | an unreviewed state (error, disabled, loading) that fails contrast or loses the action |
| **Accessibility** | the **literal** announced strings, roles, and the hit target | a screen-reader label written per screen, so it drifts |
| **Props** | the interface, typed, defaulted, and exhaustive | untyped or undocumented props, and a second near-duplicate component |
| **Edge cases** | long text, missing data, offline, RTL, huge text scale | a component that is correct only at its design size in English |

## Purpose

One sentence, in the product's vocabulary. It must distinguish this control from its near neighbours —
a chip's purpose ("a compact single-select option in a row") is what stops it being implemented as a
button with one option.

## Anatomy

```
┌──────────────────────────────────┐
│  [leading]  label       [trailing]│
│              └ helper / error line│
└──────────────────────────────────┘
```

Name every part. An unnamed part is one an implementer has to invent, and the invention is where the
component's identity leaks.

## Variants

| Variant | Difference from the base | What must NOT differ |
|---|---|---|

The second column is the useful one. Every variant of an action shares the same shape and material and
differs on one axis — typically the fill. When two variants differ on more than one axis, the
hierarchy the variants were meant to express is gone, and a user has to read labels to find the way
forward.

## Sizes

List the size tokens the component reads. This is where the size-versus-spacing rule bites:

* a minimum height is a **dimension** and reads a size token;
* a gap between the label and the helper line is **spacing** and reads a spacing token;
* a corner radius is its own axis.

State the axis for each value in the table, so a reader cannot borrow the wrong one. Where a size is a
published platform minimum, name the platform and the guideline.

## States

| State | Visual treatment | Tokens / roles read |
|---|---|---|
| default | … | `surface`, `onSurface`, `outline` |
| pressed | … | … |
| focused | … | the focus ring reads a specific role, paired with what it sits against |
| disabled | … | … |
| loading | … | the spinner keeps the control's `on` role, not the page's |
| error | … | the error role pair; a control that draws its own border must suppress **every** border colour, including the error one |

A state table is also the accessibility checklist: every state must be distinguishable not only by
colour.

## Accessibility

Write the **literal** strings the component announces, not a description of them:

* the control's role, and the announced label;
* each state's announcement, including the disabled and loading states;
* the hit target token it reads, per platform;
* the text-scaling behaviour: which role it reads, and what happens at the largest scale.

Writing the literal string is what makes it reviewable. A description ("an appropriate label") is
implemented differently on every screen and drifts.

## Props

```text
interface ComponentProps {
  variant: 'primary' | 'secondary' | 'ghost';   // the variant axis, from the Variants table
  size?: SizeToken;
  label: string;
  leading?: ReactNode;
  onPress: () => void;
  disabled?: boolean;
  loading?: boolean;
}
```

Three rules:

* the variant union matches the Variants table exactly — a variant in one and not the other is a defect;
* every optional prop has a stated default, and the default is the safe one;
* no prop takes a raw colour, a raw size, or a raw radius. A component whose API accepts a literal
  cannot be gated.

## Edge cases

| Case | Expected behaviour |
|---|---|
| label longer than the container | truncation rule, and whether the full text is announced |
| label in a longer-script locale or a right-to-left locale | layout mirroring; the leading/trailing parts swap |
| largest text-scaling setting | which parts wrap, which truncate, and whether the hit target holds |
| loading with a label | whether the label stays announced while the spinner shows |
| offline | whether the action is disabled, and what it announces if so |

## When a component should be promoted

A component earns a place in the system when it has **more than one consumer**. One instance is a
screen's local view; two instances are two copies that will diverge. The trigger to promote is the
second consumer, not a stylistic judgement — and a reuse gate can enforce it by warning on a
primitive declared per-screen while a promoted copy exists.
