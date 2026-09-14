# Failure Narratives

<!-- DEEP: 10+min — the production defects behind each rule, with what each one cost and how it was found -->

Each narrative below is a real defect from a shipped multi-platform product. The **Found by** column
is the point of the table: it is what makes visible that review found none of them.

## The discovery ratio

> 8 defects found by compilers, 2 more by decoding real data, 1 by reading — and **zero of 22 found
> by careful review**.

Every rule in this skill is downstream of that ratio. Where a design-system defect is described
below, the "Found by" entry is usually a *new gate*, not a person.

## The narratives

### N1 — every colour on a flow was a raw palette swatch

**Symptom.** The entire signed-out flow — several screens — rendered permanently dark and ignored the
user's appearance setting.

**Root cause.** The screens referenced the raw primitive ramp rather than the generated adaptive
roles. On a device set to dark it rendered correctly, so nothing looked wrong.

**Why every signal was silent.** The compiler saw a valid colour. The literal guard looked for hex
and hand-built colours, not for a wrong-but-real token. No test asserted colour, because colour is not
behaviour. The reviewer's phone was dark. No gate covered colour *roles*.

**Fix.** Eight files migrated to the adaptive roles. `DeeplyTokens` already contained the correct
roles — they were simply not used.

**Found by.** A review triggered by reading the requirement, not by a tool.

**Lesson.** When a defect is invisible to every existing signal, the answer is a new signal — not
more care. A rule enforced by nothing is advice, and advice loses to a plausible-looking shortcut.

### N2 — the theme gate

**What it checks.** A reference to a raw palette entry outside the design system, and a hand-built
colour in a screen. It reads the palette keys **from the generated token artifact**, so it cannot
disagree with what the compiler sees.

**Deliberate exemption.** A clinical severity ramp — identical in every appearance, so not an
appearance-dependent role. Exempt by name, with the reason in the script.

**How it was trusted.** Shown failing on a deliberately reintroduced violation before being relied on,
because the same project had already shipped a gate that reported clean while two compilers failed.

### N3 — the same control, dressed differently on each platform

**Symptom.** Eight controls rendered at different sizes on the two platforms. A button label was
20sp on one and 16pt on the other; a navigation bar title differed by 41%; a form field was ~44pt on
one platform with the label above the box and 56dp on the other with a floating label, so the same
form looked like two products.

**Worse.** On one platform the button-label step mapped to a rendered size **smaller** than the body
step below it — an inverted ladder — while the other platform rendered it larger than body copy.

**Root cause.** Each platform named its own vocabulary for the same control: one a brand scale
member, the other a vendor type slot. Both were valid in their own language.

**Why every signal was silent.** The literal guard only flags bare literals; every value here came
from a token or a slot. The theme guard covers colour only. The reuse guard covers a primitive
declared twice within one platform. Each platform looked correct read alone.

**Fix.** One role vocabulary both platforms must name, with the rendered size of each role resolved
per platform and asserted within a declared tolerance. The generator now refuses a non-monotonic
mapping outright.

**Found by.** A side-by-side reading of two files in two languages — and then, permanently, a gate.

**Lesson.** Parity is not "both build"; it is "both were checked for the thing that differs."

### N4 — a dimension on the gap scale

**Symptom.** A provider mark inside a button rendered 48pt on one platform and 20dp on the other.

**Root cause.** The other platform used a **spacing** step for a **size**. `DeeplySpacing.lg` was 20;
the correct value was a size token of 48. A spacing step is a gap and a size token is a dimension, and
swapping one for the other is undetectable at the call site because both are numbers from real scales.

**Fix.** A size token for the mark, matching the design's own specification exactly, read by both
platforms.

**Found by.** The parity gate written for N3, as a separate rule class.

**Lesson.** The axis is part of the value's meaning. A gap and a dimension that coincide numerically
are one rhythm change away from diverging.

### N5 — a form field height unified by adopting one platform's spec

**Symptom.** The same form looked like two different products on the two platforms.

**Root cause.** One platform rendered a bare text field with 12 points of padding (about 44) and its
label **above** the box; the other rendered the platform's own outlined field at 56 with a floating
label.

**Fix.** One size token at 56, **adopted from the platform that specifies that floor for its own
outlined field**, read by both. 56 exceeds the other platform's 44-point floor, so it is compliant on
both.

**Lesson.** Adopting a published platform specification as the shared value is principled; inventing a
compromise is not. The two produce the same number here and a different argument for it.

### N6 — a hit target below the platform's own minimum

**Symptom.** A control shipped with a hit area below the platform's published minimum.

**Root cause.** A single hit-target token carrying one platform's floor was reused on the other.
Unifying the two floors read as tidiness; it was in fact a decision to under-serve one platform's
specified requirement.

**Fix.** Two tokens — one per platform — each naming the guideline it satisfies. The second is
required because the two platforms' specified floors genuinely differ, not because a design choice
differed.

**Found by.** Reading the platform's own documentation against the token source.

**Lesson.** An accessibility floor is a requirement, not a brand variable. Declaring two values is
correct; a per-platform value is drift only when a call site picks it silently.

### N7 — a document that taught an abandoned palette

**Symptom.** A contributor following the project's own design documents would implement a brand
colour the product had never shipped.

**Root cause.** Three design documents were hand-written; one was generated. The hand-written ones
were four months stale, and the live one had already superseded an earlier palette.

**Why nothing caught it.** There is no gate that compares prose to a product, and there cannot be one
for hand-written prose.

**Fix.** The machine-readable source became the only writable artifact; the human document is
generated from it; a drift check fails CI on divergence.

**Found by.** A person noticing that two documents disagreed.

**Lesson.** A document that restates the source will lie, and the lie is undetectable. Removing the
second writable copy is the fix; discipline is not.

### N8 — a gate that reported clean while two compilers failed

**Symptom.** A stability gate reported a clean run while two compilers were failing.

**Root cause.** It compared referenced type names against declared names, using the **raw** names on
both sides — so it validated a mismatch as consistent. Its first run had also produced 28 false
positives, all legitimate builtins.

**Compound failure.** A gate that cries wolf gets ignored, and an ignored gate is worse than no gate
because it manufactures confidence.

**Fix.** Compare **final emitted identifiers** rather than the pre-transform names the checker has in
common with the generator. Its whitelist was made real, and its findings triaged.

**Lesson.** A check that shares an assumption with the code it validates cannot catch a bug in that
assumption. A gate is not finished when it runs; it is finished when its findings are triaged and it
has been shown failing on a real violation.

### N9 — a rule that was silently a no-op in one direction

**Symptom.** A consistency check ran in both directions, but the reverse direction was a deliberate
no-op. The specification fell to 41 documented paths while the API served 114.

**Root cause.** A one-way check reads as complete and is half a check.

**Lesson.** For every consistency rule, ask which direction it does not check — that is where the
drift accumulates. One-way freshness checks are the common case of this defect.

### N10 — a generator backend that had never been executed

**Symptom.** A generated language target did not parse at all: raw serialised data appended to a
preamble with no declarations.

**Root cause.** The file was untracked, imported by nothing, and that backend had never been run —
only another backend had.

**Lesson.** A backend that has never executed is not "working", it is unexercised. `N files written`
is not success. Every generated target is either committed and consumed, or gitignored and not shipped.

## What each narrative justifies

| Narrative | Rule it establishes |
|---|---|
| N1, N2 | R1 — no screen reads a primitive; the gate reads its vocabulary from the generated artifact |
| N3 | R2 — one role vocabulary, rank-asserted, with a declared tolerance |
| N4 | R3 — dimensions on the size axis, gaps on the spacing axis |
| N5, N6 | R4 — per-platform floors declared with their sources |
| N7 | R5 — documents generated from the source, with a drift gate |
| N8, N9 | R6 and the gate-calibration discipline — vocabulary from the source, proven to fire, both directions |
| N10 | Every generated target consumed or ignored, never untracked-and-unused |
