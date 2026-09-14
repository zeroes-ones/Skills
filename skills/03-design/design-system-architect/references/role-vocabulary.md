# Role Vocabulary

<!-- STANDARD: 3min — naming roles by intent, per-platform spellings, generation-time collisions -->

## Why roles exist at all

Two platforms can read *the same scale* and render *different sizes*, and both compile. Each spells
its own name for the same control — one a scale member, the other a vendor type slot — and each
name is valid in its own language. Nothing reports the difference; only reading two files in two
languages side by side reveals it.

A **role** is the one name for the size a control uses. `buttonLabel` is the button label's size on
every platform. The role aliases a scale step, so there is still exactly one set of numbers.

## Name after intent, never after value

| Good role name | Bad role name | Why |
|---|---|---|
| `barTitle` | `titleLarge` | the first names the slot, the second names a scale position that will move |
| `fieldHelper` | `helperTextSmall` | "small" is a value claim; the next scale change makes it a lie |
| `chipLabel` | `bodyMedium` | a vendor slot name is the vendor's vocabulary, not this product's |
| `primary` | `amber` | a role whose name describes its colour is wrong after the next identity change |

A role name that describes its colour or its size will be wrong the first time either changes, and
nobody renames it — so the name becomes a small permanent untruth that new contributors learn.

## Two spellings, one declaration

Each platform shortens a role in its own idiom so a call site stays readable. Both forms name the
same role and resolve to the same size.

| Platform | Short form | Long form (still valid) |
|---|---|---|
| A language with leading-dot member resolution | `.font(.buttonLabel)` | `.font(Role.buttonLabel)` |
| A language without it | a member import, then `style = buttonLabel` | `style = Role.buttonLabel` |
| A scripted language or web | `typeRole.buttonLabel` | — |

**Critical implementation note.** The short form usually works because the generator emits the role
as a static member on the platform's own font type, so a leading dot resolves it exactly the way
the platform's built-in styles do. The type that holds the roles must therefore be a **type alias**
for that platform font type, **not a second copy** of the roles. An enum with its own constants per
role declares every role twice — which is the very drift the roles exist to prevent.

## Two generation-time refusals

Both must happen in the generator, not in review, because both produce failures elsewhere:

1. **A role name that collides with the platform's own vocabulary must be refused.** A platform
   with a built-in style called `body` plus a generated role called `body` gives an extension that
   silently shadows a system style. The failure lands at a call site one language away from the file
   that caused it.
2. **A role whose target is not a scale key must be refused.** A typo emits a constant pointing at
   nothing. Where the platform resolves it through a conditional, it may not fail to compile at
   all — it silently falls to a default, which is the worst outcome available.

## Roles do not fix a wrongly-sized system

Roles prevent the two platforms from **disagreeing**. They do not stop both from being **wrong
together**. Three shared roles can each be a step larger than the platform's own convention for the
control they name, and both platforms will move together into the same wrong size.

The audit that catches this is separate: for each role, name the platform's own convention for that
control (its documented label size, row-title size, secondary-line size) and compare. A role change
is a single edit that fixes every consumer at once, which is the reason to resolve sizes at the role
level rather than per screen.

## When one role must not be reused

The strongest argument for a distinct role is that the **meaning** differs, not the size:

* A provider's call-to-action label inside a third-party row is body copy on a neutral surface, not
  this product's action label — reusing the button's role makes a partner row read as a primary
  action.
* A chip's label is a tappable label, not an action button. Reusing the button role makes a
  five-option chip row read as five primary buttons.
* A helper line below a field is support text; reusing the label role makes it read as a second label.

A role exists to encode which control it belongs to. Two controls that happen to share a size today
and differ in meaning tomorrow should already have two roles.
