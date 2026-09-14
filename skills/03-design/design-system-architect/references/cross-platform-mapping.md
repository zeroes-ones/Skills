# Cross-Platform Mapping

<!-- DEEP: 10+min — monotonic mapping, rank assertions, tolerances, and the equal-size cases -->

## The problem this solves

A brand type scale is defined in one unit — a design pixel size. Each platform renders it with its
own mechanism:

* A platform with **scaling text styles** maps the brand size to the style whose real point size is
  closest, and gains user text-scaling for free. Those styles are **not** the brand numbers: the
  nearest style to a 16px step is typically 17pt, not 16pt.
* A platform whose text unit **scales and equals the design pixel** can use the exact value.

That asymmetry is the whole problem. The platforms *can never be exactly equal* unless the font
asset is bundled and kept metric-compatible, and the resulting small gap is legitimate. What is not
legitimate is the gap that a naive mapping produces.

## The measured failure

The mapping had drifted so that a **larger** brand step landed on a **smaller** rendered style than
the step below it:

| Role | Source step | Mapped style | Real point size | Rendered on the other platform |
|---|---|---|---|---|
| primary body text | 16px | `.body` | 17pt | 16sp |
| button label | 18px | `.callout` | **16pt** | 20sp |

On one platform a button label rendered **below** its own body copy — an inverted ladder — while on
the other it was 20sp. Every value came from a token or a vendor slot, so the literal guard reported
clean; the theme guard covers colour only; and both platforms look correct read alone.

## The rank assertion

The generator must order the scale by source size and assert, for each adjacent pair, that the
rendered size on the mapped platform is **not smaller** than the pair below it. Two further rules
belong in the same assertion:

1. **An equal rendered size is legitimate only when the weight differs.** A regular 17pt and a
   semibold 17pt are a real pair and a real hierarchy step; two steps sharing both size and weight
   render identically, so the smaller one is pointless on that platform.
2. **The point sizes are facts about the platform, not brand choices.** Record them in the generator
   beside a note saying so: if the platform changes a style's size, the comparison is what needs
   revisiting, not the design.

```text
for (lower, upper) in adjacent(scale ordered by source size):
    assert points(upper.style) >= points(lower.style)
    if points equal: assert upper.weight != lower.weight
```

An assertion of this shape is cheap, runs at generation time, and — unlike review — fires.

## The tolerance, and why it must be declared

A platform that maps to scaling styles cannot hit the brand pixel exactly. The honest contract is a
**declared tolerance** beside the mapping, with its reason written down:

* state the tolerance in the same unit the platform renders in;
* justify it as the smallest value that admits the platform's scaling styles;
* check that it is **tighter than the defect it exists to catch** — a tolerance wider than the
  original gap would have certified the bug it was written for;
* assert the tolerance itself, so a later edit cannot quietly widen it.

A tolerance of about two points is typical where a mapping to system styles is in play; the correct
number for a given system is the one you can justify, not one copied from another product.

## The per-platform resolution table

The reusable artefact is a table that resolves every role on every platform:

| Role | Scale step | Platform A rendered | Platform B rendered | Delta | Within tolerance? |
|---|---|---|---|---|---|

Write this even when both platforms are correct. It is the artefact that makes a *future* drift
visible, because the next person adds a role and the table has an obvious empty row. A role with no
cross-platform resolution is a role that was never checked.

## Do not confuse the role tier with the mapping

A scale member is a size. A role is a control's size. A vendor slot is another platform's name for a
size. The mapping is the table from role to rendered size per platform. Keeping all four concepts
distinct is what lets the gate's message say "this primitive reads a scale member where a role
belongs" rather than "this value is wrong".

## What NOT to do

* **Do not hardcode a fixed size to force equality.** A fixed size does not scale with the user's
  text-scaling setting and fails the text-scaling requirement — the exact accessibility property the
  system-style mapping was chosen to preserve.
* **Do not bundle a font purely to close a two-point gap** unless it is already required for other
  reasons. It changes the glyph identity on that platform, adds an asset to verify, and buys less
  than the tolerance costs.
* **Do not add a per-role fallback branch for a system version no supported device runs.** A
  fallback for an unreachable system is dead code that cannot be verified, and it hides the real
  requirement.

## Verifying the assertion is useful

An assertion that has never failed is not evidence. Inject the inversion — swap two adjacent steps'
mapped styles in the source — regenerate, and confirm the generator refuses with a message naming
both steps and both rendered sizes. Then restore and confirm the generator is silent. Record both
outcomes; the firing run is the evidence, the silent run is the control.

## Mapping a separate non-collapsible scale

Where a domain scale exists for a different audience — an emergency or clinical scale that must stay
larger and never thinner than a given weight — it gets its own mapping table and its own assertion,
and it must **not** be folded into the general ladder. The property that makes it safe (never below
a certain size or weight) is exactly the property a merge destroys, and a merged scale passes every
rank assertion while losing the guarantee.
