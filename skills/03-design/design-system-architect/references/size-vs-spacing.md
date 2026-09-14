# Size Versus Spacing

<!-- STANDARD: 3min — the axis separation, fixed dimensions, and the cost of a coincidental match -->

## Three axes, one numeric slot

A padding, a frame dimension, and a corner radius all flow into the same numeric type in most
frameworks. That is convenient for the framework and dangerous for the design system, because it
means the axes are interchangeable at the call site:

```text
padding(.rowMinHeight)                 ← a dimension used as a gap; compiles
RoundedRectangle(cornerRadius: .md)    ← a gap used as a radius; compiles
frame(width: .base, height: .base)     ← a gap used as a dimension; compiles
```

Every one of those is a mistake that renders plausibly and is invisible in review, because the
numbers are real numbers from a real scale.

## The definition

| Axis | Answers | Changes when | Token prefix |
|---|---|---|---|
| **Spacing** | how far apart are two things? | the page rhythm or density changes | `spacing` |
| **Size** | how big is this one thing? | an accessibility floor, a design decision, or a control spec changes | `size` |
| **Radius** | how round is this corner? | the shape language changes | `radius` |

A gap is relational — it exists between two elements. A dimension is intrinsic — it exists because
one element is that size.

## Why a coincidental match is the dangerous case

The clearest instance: a camera badge diameter happened to be exactly one of the spacing steps. Two
things follow.

1. **The coupling is invisible today.** Nothing is wrong yet, so nothing is flagged. The value reads
   as a correct use of the design system.
2. **The coupling is wrong tomorrow.** The first time the spacing rhythm is retuned, the badge's
   diameter changes with it — silently, on every screen that draws it. The person retuning the
   rhythm has no reason to look at a badge.

The fix costs one token: move the value to the size scale under a name that says what it sizes. The
size scale can still equal the spacing step numerically; what matters is that the **name** ties the
value to the concern it serves. The name is what makes the coupling visible in a diff and reviewable
in a token file.

## An interaction target is not a design choice

A minimum tappable control size is a **published platform requirement**, not a brand decision. Two
consequences:

* It must never be reduced to "stay on the grid". Shrinking it is an accessibility regression.
* Where two platforms publish different minimums, the correct answer is **two tokens**, each naming
  the guideline it satisfies — not one compromise value.

Unifying them reads as tidiness and is a decision to ship one platform below its own specified floor.
Declaring them separately is not drift when the token file states both with reasons; drift is a call
site silently picking one platform's number for both.

## Fixed control dimensions

Some dimensions are genuinely fixed and should not scale with the surrounding layout:

| Kind | Example | Why fixed |
|---|---|---|
| an interaction floor | a hit target | a published minimum, not a layout outcome |
| a gauge readout | a progress indicator's width | a control that stretched to the title's width would compete with it |
| a rail width | a jump rail or scrub strip | must occupy the same strip on both platforms |
| a hero element | a preview or confirm target | the size *is* the meaning — a preview that grew with its container would not read as the picture being confirmed |
| a badge | an edit affordance over a photo | it is the size of one element, and it sits over another fixed element |

Each of these still belongs on the **size** axis. "It is fixed" is not a reason for it to be a
number in a screen; it is a reason for it to be a named size token with the reason recorded.

## A tight affordance can be deliberately below the floor

A rail row that must fit many buckets into a phone's height is legitimately tight — but only when
its **touch target is the whole strip**, not each row. Record it: the value, the reason, and the
statement that the hit area is the container. Without that note, the next accessibility audit reads
a number below the floor and cannot tell a deliberate affordance from a regression.

## Review questions for this section

1. Does any size token equal a spacing token numerically? If so, is the coupling named or accidental?
2. Does any screen contain a dimension number rather than a size token?
3. Is every per-platform floor declared separately, with its guideline named?
4. Does every "fixed" dimension state why it is fixed?
5. Does any affordance below the platform floor record why, and what its real hit area is?
