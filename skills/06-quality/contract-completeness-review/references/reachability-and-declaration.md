# Reachability and Declaration

Every contract member makes a claim: *this operation exists and is used*. Two ways the claim can be
false while everything stays green.

| Claim | False when | Failure signal |
|---|---|---|
| **Every declaration is implemented** | An implementation is missing a member | A red compiler or a failing contract test — loud |
| **Every declaration is exercised** | A member has no call site | **None.** An unused member is valid code |
| **Every implementation is declared** | The implementation grew past the declaration | **None**, unless the check runs in both directions |

The bottom two rows are this skill's territory.

## Declared but unused

A contract member with zero call sites is usually read as dead code and scheduled for removal. It is
worth distinguishing three cases first, because they have different fixes:

| Case | Example | Fix |
|---|---|---|
| **Superseded** | An old method kept for compatibility that nothing calls | Remove it, with the compatibility window stated |
| **External contract** | A library or protocol member that consumers outside this repo call | Keep, with a named consumer and a reason. Mark it `[VERIFIED]` external |
| **Generated but unapplied** | A derived value — a token, a config key, a computed field — that exists and is never read | **This is a defect, not dead code.** Add the call site |

The third case is the one that hides. A value can be generated correctly, be present in the built
artefact, pass every gate, and be applied by nothing. The observed instance: an accent derivation
carried the exact border, subtle, and text values from the original implementation and nothing read
them, so a user who selected a teal accent got teal buttons and brand-amber borders. The symptom
read as a brand-consistency issue, not as a bug.

> Generation proves a value EXISTS; only a call site proves it is APPLIED.

The check is one grep per member: `grep -rn "<member>" --include='*.kt' --include='*.swift' | wc -l`.
Count call sites minus declaration sites. Zero is a finding.

## The one-way check

A conformance check that only asks "is everything declared implemented" will never report the
inverse. The observed instance is worth quoting exactly, because its author recorded the cause:

```
if not fuzzy_found:
    pass   # Don't fail on extras
```

That single no-op branch is how a specification silently fell to 41 documented paths while the API
served 114. Nothing was broken. The check ran on every commit, passed on every commit, and would
have passed forever.

The general shape:

| Direction | Question | Typical state |
|---|---|---|
| Declaration → implementation | Is every declared item implemented? | Usually present — it is the obvious check |
| Implementation → declaration | Is every implemented item declared? | **Usually a no-op**, or absent entirely |

The second direction is the one that matters when a service grows faster than its specification,
which is the normal case in any system with more than one team.

## Bidirectionality test

To verify a conformance check actually runs both ways, introduce an implementation that is **ahead**
of the declaration and confirm the check fails:

```
1. Add an operation, endpoint, or field to the implementation.
2. Do NOT add it to the declaration.
3. Run the conformance check.
4. If it passes, the reverse direction is a no-op. Report that as the finding.
5. Remove the addition.
```

Step 4 is the whole test. A check that stays green when reality moves ahead of the declaration is
one-directional regardless of how the code is written or how the author describes it.

## Rules can be locally correct and jointly contradictory

A related failure belongs here because it is also a completeness defect, one level up: the *rules*
are incomplete, not the contract.

A scope had no legal spelling. Combining a module name with an internal visibility modifier failed
one rule that required explicitness and a second rule that banned redundancy. Each rule was correct
in isolation; together they forbade every available form.

The encoded invariant: **every scope must have a legal spelling in every tree.**

The mechanical check is an exhaustive matrix — the cross product of every dimension the rules
constrain — with each combination spelled out and checked for at least one legal form:

```
for each module scope       (n)
  for each visibility        (m)
    for each tree            (k)
      assert at least one legal spelling exists      → n × m × k cells, each with a witness
```

The same reasoning applies to any rule set with two dimensions. The check is cheap; the defect is
not, because an impossible combination is discovered by whoever is trying to use it, usually late.

## Calibration: a gate that cries wolf gets ignored

A related rule from the same source: a design gate policed every raw colour literal and reported 80
violations, most of them legitimate. The resolution was not to add more care — it was two severity
tiers, strict inside the design system and duplication-only elsewhere.

> A gate that cries wolf gets ignored, and an ignored gate is worse than no gate, because it
> manufactures confidence.

Apply the same discipline here. A reachability report that lists every unused member as a defect
produces noise. Split the output into the three cases above, and block on the third only.

## Rules

* **Count call sites per contract member; zero is a finding until classified.** Superseded, external,
  or generated-unapplied.
* **Generated-and-unapplied is a defect, not dead code.** The value is correct and the product is
  wrong.
* **Prove both directions by making reality move ahead of the declaration.** If the check stays
  green, that is the finding.
* **Test the cross product of any two-dimensional rule set.** Every scope must have a legal spelling.
* **Tier the severity before shipping the check.** A noisy gate is worse than no gate.
