# Platform Floors

<!-- STANDARD: 3min — published minimums, declaring rather than unifying, and fixed control dimensions -->

## The rule

A minimum tappable control size is a **published platform requirement**, not a brand choice. Its
consequence for a token system is direct: when two platforms publish different minimums, the correct
representation is **two tokens**, each naming the guideline it comes from.

## The failure that produces this rule

A single hit-target token carrying one platform's floor was applied to both. On the platform whose
published minimum is smaller, that was correct. On the other, the control shipped **below its own
platform's minimum** — an accessibility regression produced by tidiness.

The reasoning that produced it is entirely reasonable: one product, one design system, one floor.
The reasoning is wrong because the floor is not the product's to set.

## Declaring versus unifying

| Situation | Correct representation | Why |
|---|---|---|
| Two platforms publish different minimums | two tokens, each naming its guideline | each platform meets its own spec |
| One platform publishes a minimum, the other does not | a token on the platform that does, and a documented rationale on the other | the absence of a published floor is not a licence to go below the practical one |
| A control is fixed for product reasons | one cross-platform size token with the reason recorded | the constraint is the product's, so a shared token is honest |

A per-platform value is **not** drift when the token source declares it and states why. Drift is a
call site silently picking one platform's number for both — which is exactly what the conformance
gate forbids.

## What the token must carry

Every floor token should name, in the source:

* the platform it applies to;
* the guideline it satisfies;
* the fact that it is a requirement rather than a preference, so the next person does not "round it
  to the grid";
* where a second value exists on another platform, a note that the two differ by design.

An unexplained pair of near-identical tokens reads as an accident; an explained pair reads as a
requirement. The explanation is what stops a future contributor unifying them again.

## Fixed control dimensions that are not floors

Not every fixed dimension is an accessibility requirement. The recurring kinds:

| Kind | Character | Belongs on |
|---|---|---|
| interaction floor | a published minimum; never reduced | the size axis, per platform |
| form field height | adopted from a platform's own field spec so a form is the same shape everywhere | the size axis, shared, with the source named |
| a mark or icon inside a button | sized to match a design's own specification | the size axis, shared |
| a readout gauge | fixed so it cannot stretch to compete with adjacent text | the size axis, shared, with the reason |
| a hero or confirm target | the size *is* the meaning | the size axis, shared, with the ratio to a base dimension recorded |
| a photo badge | the size of one element over another fixed element | the size axis, shared, even when a spacing step happens to equal it |

Two patterns worth reusing:

* **A form's field height adopted from one platform's own field specification** is what stops the
  same form looking like two different products — a bare text field with a label above it on one
  platform, and a bordered field with a floating label on the other. 56 of a scalable unit exceeds a
  44-point floor, so it is compliant on both.
* **A standalone element's size expressed as a ratio to a base dimension** (1.5×, 2×) is how a
  preview and a hero stay related without either being a spacing step.

## A deliberately tight affordance

A jump rail, a scrub strip, or a dense index can be legitimately tighter than the platform floor,
provided:

1. the **hit area is the whole strip**, not each row;
2. the reason is recorded where the token lives;
3. both platforms read the same token, so the strip occupies the same area on each.

Without all three, the next accessibility audit finds a number below the floor and cannot distinguish
a deliberate affordance from a regression.

## Review questions for this section

1. Does every interaction floor token name its platform and its guideline?
2. Is any single floor token applied to platforms with different published minimums?
3. Does every fixed dimension record why it is fixed?
4. Does any affordance below the floor record what its real hit area is?
5. Does each fixed dimension live on the size axis rather than the spacing axis?
