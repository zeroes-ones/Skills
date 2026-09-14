# Discovery Ratio — why mechanical detection beats review, and what it cannot see

> The organising statistic of this skill: across the source corpus, **8 defects were found by
> compilers, 2 more by decoding real data, 1 by reading**. Zero of the twenty-two in the first batch
> were found by careful review.

---

## The evidence

The source project recorded, for each defect, the instrument that found it. The "found by" column is
the point of the table — it is what converts a war story into a budget argument.

| Instrument | Defects found | Examples of the class |
|-----------|--------------|----------------------|
| **Compilers / type checkers** | 8 | A missing declared enum; a `data class` field with no `val`; Java's `Void` used as Kotlin's void; a type name declared under two different spellings |
| **Decoding real captured data** | 2 | A nullable union widened to an opaque type; a `$ref` dereferenced before its name was read (~80 fields lost their real types) |
| **Gates and validators** | several | A one-way spec gap check silently at 41 documented paths against 114 served; 28 false positives from a whitelist missing a builtin |
| **Inspection of a built artefact** | 4 | A configured URL key never reaching the bundle; localisation files never bundled; an entitlement signature carrying an empty dict; a package name in the merged manifest |
| **Comparison of two implementations** | 2 | One platform rendering stub data while the other rendered live data |
| **Careful reading** | **1** | — |

The ratio in the second batch (entry-flow work) was the same shape and the document says so
explicitly: *every defect below was found by a compiler, a test, or a gate. None was found by
reading.*

---

## Why reading is the weakest signal, structurally

Reading is not a weak instrument because readers are careless. It is weak for three structural
reasons:

| Reason | Mechanism |
|--------|-----------|
| **It shares the author's model** | A defect where both sides are individually correct (`WelcomeView` declared twice, both plausible; a domain type and a generated type sharing a name) reads as correct in isolation. The reader has no access to the collision unless they hold both files at once. |
| **It has no execution** | A comment that describes the intended code is not evidence the code does it. In one instance a comment read "EMAIL BEFORE DISPLAY NAME on submit order, matching the visual order" while the fields rendered display-name-first — on all three platforms. |
| **Its cost does not scale** | Reading a 200k-word codebase for a defect class is not a budget anyone can fund. A gate costs once and runs forever. |

The single defect found by reading in the corpus is instructive in the other direction: it was found
by **reviewing against the platform**, not by reviewing the code — checking the app against a store
requirement (a privacy manifest) that no local tool checked. That is reading *against an external
standard*, which is a different and stronger act than reading the code for internal consistency.

---

## What each instrument costs and covers

A gate set is a portfolio. The table below is the one to reason with when deciding where to spend.

| Instrument | Setup cost | Per-run cost | Catches | Cannot catch |
|-----------|-----------|--------------|---------|--------------|
| Compiler / type checker | Near zero — it exists | Compile time | Syntax, undefined types, wrong spelling, missing dependencies, conformance | Semantic type loss (a wider type that still compiles) |
| Decode real captured data | Low (capture a fixture) | Fast | Opaque types, nullability mismatch, reference mishandling, wire-format drift | Drift over time; mapping decisions |
| Drift / freshness check in CI | Medium (wire it) | Fast | A source change the artefact has not picked up | Wrong mapping decisions; a generator that never ran |
| Purpose-built lint rule | Medium | Fast | One named defect class, at scale, forever | Anything outside the pattern; the class's rare spellings |
| Runtime/boot smoke test | Medium | Slow | A configuration that parses but crashes, a missing bundle resource | Anything in a path the smoke test does not exercise |
| Cross-implementation comparison | High | Slow | Divergence between two implementations of one rule | Anything both implementations get wrong identically |
| Review | Low per instance | High | Novel classes, external-standard mismatches, intent | Anything requiring two files held at once; anything invisible to the reader's environment |

Two rows deserve emphasis:

**"Decode real captured data" cannot be replaced by a hand-written sample.** A hand-written fixture
encodes the same assumptions as the generator that produced the code under test, so it validates
the assumption rather than the wire format. The fixture must be captured from the live source.

**"Cross-implementation comparison" is weaker than it looks.** One platform passing is not evidence
about the other when the passing one bypasses the shared contract. In the corpus, iOS passed a
session-persistence requirement because it wrote the keychain directly and only read through the
port; Android implemented the port faithfully and never persisted anything. The port declared
`hasSession` and `clear` but no `save`.

---

## The classes mechanical detection cannot reach

Honesty about the blind spot is what makes the ratio usable instead of overclaimed. Five classes
that no gate in the corpus caught, and the reason:

| Class | Why no gate reaches it | The replacement signal |
|-------|----------------------|----------------------|
| **The platform's own default** | Android's edge-to-edge is the app-level default, so each screen must opt *in*; iOS's safe area is automatic, so a view must opt *out*. The same structural code is correct on one platform and puts a button under the gesture bar on the other. No compiler reports it; a bar-less emulator screenshot looks fine | A parity probe: "which platform gets this by default, and what does the other have to remember?" |
| **A missing write on an interface** | An interface that cannot express an operation cannot be tested for it. Every fake mirrored the omission, so 214 tests agreed with the bug | The question **"who WRITES this?"**, asked of every piece of state something else reads |
| **Duplicate use of one constant** | A navigation bar and a content heading both used the same title key, so the string appeared twice on one screen. Every file that defines it is correct | A UI assertion counting occurrences, not checking presence |
| **A movement's direction** | A transition with one hardcoded direction tells the user the opposite of what happened. Both directions compile from identical-looking code, and a screenshot is still | Two further reasons it survived: the transition lived in a screen rather than the shared primitives, and it was duplicated across platforms so each copy looked correct alone. The direction is knowable only by the code that *changed* the state, so it is domain data, not view state |
| **A store that reads but cannot write** | The same shape as the missing-write case, named separately because it is a *naming* defect: a thing called `SessionStore` implied ownership of the value and only had ownership of the question | Ask of any name what the thing must be able to do to deserve it |

The pattern across all five: **the defect is in a seam between two things that are each individually
correct.** Mechanical detection is strong inside a single artefact and weak at seams. That is the
residual that review and structured probes cover — and it is why the ratio is a budget argument, not
a claim that reading is worthless.

---

## Using the ratio as a budget

The ratio answers one question well: *given a defect class that keeps escaping, what should we
build?*

```
A defect class escaped into production.
├── Is it expressible as a rule over a single artefact?
│   ├── Yes → build the rule. Fire case, silent case, negative control, calibrated severity.
│   └── No ↓
│       Is it expressible as a comparison between two artefacts?
│       ├── Yes → build the comparison, and check BOTH directions.
│       └── No ↓
│           Is it a seam between two individually-correct things?
│           ├── Yes → the signal is a PROBE, not a rule: a question asked of every instance
│           │         ("who writes this?", "which platform defaults here?",
│           │          "does the bar already say this?"). Make the probe a checklist item.
│           └── Yes, and the probe is already on the checklist and still failed →
│               the checklist item is not mechanical enough. Convert it into a test that
│               renders or executes, because a stated rule enforced by nothing is advice.
```

The last branch is the important one, and it is where the corpus's strongest lesson lives:

> **When a defect is invisible to every existing signal, the answer is a new signal — not more
> care.** "Be careful" loses to a plausible-looking shortcut every time; a gate does not.

---

## Reporting it honestly

Two habits from the source project worth copying, because they are what keep the ratio from being
misread:

1. **Report what was NOT verified.** The project's self-assessment has an explicit unverified
   section and reports "P0 gates closed: 0 of 85" without softening. A gate set reported without its
   gaps becomes a guarantee in the reader's mind.
2. **Use "Not built yet" rather than a mock.** A placeholder that looks real is worse than a visible
   gap, because the gap is the information.

Applied to a check: publish, for every gate, the **"does NOT catch" column**. A gate's coverage
claim without its blind spot is a liability, and the blind spot is the part that has to be written
by the person who built it, because the next reader will not be able to derive it.
