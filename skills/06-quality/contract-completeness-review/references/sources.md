# Sources

Every claim in this skill traces to one of the sources below, tagged by strength.

| Tag | Meaning |
|---|---|
| `[VERIFIED]` | Observed in a specific file, defect record, or commit in the named source |
| `[COMPUTED]` | Derived arithmetically from stated inputs; the derivation is shown where used |
| `[ESTIMATED]` | Assumed for illustration; the assumption is written down |
| `[COMMON-PRACTICE]` | Widely taught in the field; not tied to a specific source |

## Primary source

**`docs/deeply-health-mining.md`** `[VERIFIED]` — synthesis of an eleven-cluster deep read of
`/Users/sp.vm/Documents/Projects/Deeply-Health`, a production health app (iOS, Android, React
Native, Next.js, Python/FastAPI) with ~320k words of docs, ~207k words of native code, 15 ADRs, and
a live design-token pipeline.

The specific finding this skill is built from is **F4**: an interface that cannot express an
operation cannot be tested for it, ranked in that synthesis as "a genuinely missing diagnostic. It
is not code review, not testing, not architecture. It is contract-completeness review."

## Defect records

**`/Users/sp.vm/Documents/Projects/Deeply-Health/docs/native-learnings.md`** `[VERIFIED]`

| Location | Claim taken |
|---|---|
| Defect 44 (the `SessionStore` case) | The port declared `hasSession` and `clear` but no `save`; Android implemented the interface exactly and never persisted a session; iOS passed because it bypassed the port |
| The four-signal table for Defect 44 | Both compilers, 214 tests, all five gates, and two green builds were each silent, and each for a distinct reason |
| Part 6, rules 35–37 | "Ask who WRITES this"; "when one platform passes and the other fails, check whether one bypasses the shared contract"; "an interface that cannot express an operation cannot be tested for it" |
| Part 4 (the verification ladder) | Four rungs with a "does NOT catch" column; you cannot skip rungs; a 0-error compiler run needs a negative control |
| Defect 1 (spec 41 of 114 paths) | `if not fuzzy_found: pass  # Don't fail on extras` — the reverse direction was a deliberate no-op |
| Defect 22 | A gate reported clean while two compilers were failing, because it compared raw names on both sides — the assumption was shared with the code it validated |
| Defect 22 (28 false positives) | "A gate that cries wolf gets ignored, and an ignored gate is worse than no gate" |
| Part 6, rule 11 | Two right names in one target — the compiler names the consequence, not the collision |
| Part 6, rule 38 | A generated value with no reader; "generation proves a value EXISTS; only a call site proves it is APPLIED" |
| Defect 18 | A view model whose state starts at loading and is never written by anything; found by noticing no timeout fired |
| Part 6, rule 46 | A comment describing the intended code is not evidence the code does it |
| Part 6, rule 47 | A root screen has no back control, whatever the comment claims |
| Part 5b (behaviour-named test table) | Tests named after the behaviour, cross-referenced to the defect each guards |

**`/Users/sp.vm/Documents/Projects/Deeply-Health/docs/native-entry-flow-parity.md`** `[VERIFIED]`

| Location | Claim taken |
|---|---|
| §5 (the launch decision) | "unread" is not "signed out"; completion beats a stale step; neither app hardcodes a destination |
| §7 (not built yet) | A route value that no screen reads is "a trap for the next reader"; two authorities for one fact |
| §8 (how this is enforced) | The rule-to-gate table: every rule that matters has a named gate |
| §9 (platform defaults that differ) | When a platform supplies a default, the other platform is where you look; parity is "both checked for the thing that differs", not "both build" |

**`/Users/sp.vm/Documents/Projects/Deeply-Health/docs/CHANGELOG.md`** `[VERIFIED]` — the fix record for
the session defect: `save` added on both platforms, `NexusAuthRepository.toSession()` made `suspend`
and persisting before it returns, so password login, registration and all three SSO providers store
the session through one function rather than three call sites remembering to.

## Secondary sources

**`/Users/sp.vm/Documents/Projects/Deeply-Health/docs/native-sso-setup.md`** `[VERIFIED]` — the
`SessionStore` interface as declared, the regression test
`a written session is reported, and a cleared one is not`, and the atomicity requirement (Android
writes the token pair in one `commit()` rather than two `apply()` calls).

> The figures in `failure-narratives.md` and the skill's Gotchas table are `[COMPUTED]` from the
> stated defect scope and a blended engineering rate. They are **not** historical accounting for
> this project, whose own documents do not publish per-defect costs. Treat them as order-of-magnitude
> illustrations of the defect class, and substitute your own rates before citing them as a forecast.

## Standards and common practice

* **Ports and adapters / hexagonal architecture** `[COMMON-PRACTICE]` — the seam vocabulary used
  throughout; the skill assumes the reader knows what a port is and does not re-teach it.
* **Structural typing and interface conformance** `[COMMON-PRACTICE]` — Go's implicit interfaces,
  TypeScript's structural typing, Kotlin's explicit `: Interface`, Swift's protocol conformance, and
  Java's `implements` differ in whether an implementation is *declared* to satisfy a contract. This
  matters for the bypass map, which is why this skill states that the exact rule must be confirmed
  against the language reference rather than recalled.
* **Test doubles (Meszaros taxonomy)** `[COMMON-PRACTICE]` — the stub / fake / mock distinction used
  in `mirroring-fakes.md`.

## What this skill deliberately does not cite

* **Per-defect dollar costs for the source project.** Not published in the corpus; every figure here
  is constructed and labelled.
* **The source project's stale design docs.** The synthesis records that three hand-written design
  documents describe a brand colour that never shipped. Their format was mined; their values were
  not.
* **Environment specifics** — JDK versions, sandbox flags, absent SDKs. Recorded in the synthesis as
  explicitly non-transferable.

## Anti-hallucination statement

Every `[VERIFIED]` row above was read in the named file during preparation of this skill. Where a
claim required inference rather than reading — for example, that a given bypass pattern would
recur on a third platform — it is stated as a generalisation and marked `[COMMON-PRACTICE]` or left
as an explicit assumption. No defect is attributed to the source project that its own records do
not state.

**Knowledge cutoff note:** language-level interface semantics change across versions. Confirm the
specific rule for setter requirement, implicit conformance, and default methods against the installed
compiler version rather than against this file.
