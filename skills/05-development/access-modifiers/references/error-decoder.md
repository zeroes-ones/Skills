# Error Decoder — Long Form

<!-- DEEP: 5+min -- the symptom catalogue in long form, with causes and fixes -->

The compressed table lives in `SKILL.md`. This file carries the full diagnosis.

## 1. A refactor breaks external consumers who used an internal helper

**Symptom:** a rename or restructure produces compile errors or runtime failures in code you do not own.
**Mechanism:** the helper was public by default (or package-private in a package someone else imports), so a consumer built on it. Nothing defined the surface, so its consumers did (R2).
**Diagnosis:** compare the declared public surface against the documented one. The gap is the accidental surface.

**Fix:** publish an explicit surface list; narrow the helper; deprecate with a window before removing.
**Recurrence guard:** the surface list is generated and diffed in review (CR4, CR5).

## 2. A sensitive value is readable at runtime despite `private`

**Symptom:** a token, key or credential present in a compiled bundle is reachable by a runtime caller.
**Mechanism:** TypeScript's `private` is erased at compile time — the emitted JavaScript has an ordinary public property. The modifier documented intent; nothing enforced it (R4).
**Diagnosis:** grep for `private` on sensitive names in TypeScript sources.

**Fix:** `#field` for anything whose secrecy matters. Where the language has no enforcing mechanism, move the value behind a boundary that does enforce one.
**Recurrence guard:** every erasure-based modifier on a sensitive value is flagged (CR8).

## 3. A Java caller reaches a Kotlin `internal` API

**Symptom:** code outside the Kotlin module calls an `internal` declaration; the intended boundary did not hold.
**Mechanism:** `internal` is a Kotlin-compiler concept. At the JVM level the symbol is public, so Java on the same classpath reaches it (R4).
**Diagnosis:** search for Java callers of mangled Kotlin internal names.

**Fix:** restrict at the JVM boundary — a module Java cannot depend on, a separate artifact, or an opaque accessor. Document the limitation where it cannot be closed.
**Recurrence guard:** Kotlin `internal` on the JVM is flagged as permeable (CR8).

## 4. Changing a field breaks callers

**Symptom:** renaming, retyping or removing a field breaks consumers, even when the class is otherwise unchanged.
**Mechanism:** a public mutable field published the representation, so the field *is* the contract (R3).
**Diagnosis:** find public non-final fields.

**Fix:** private field plus an accessor; or the read-only idiom (`internal(set)`, `private set`, a getter).
**Recurrence guard:** no public mutable field outside constants and documented transparent data types (CR6).

## 5. Every class is public in an app with one module

**Symptom:** a single-module application where everything is public.
**Mechanism:** the default modifier was never questioned. In a single module there is no public surface, so `public` means nothing and promises nothing (R1).
**Diagnosis:** count `public` declarations in a project with one module.

**Fix:** `internal` throughout; `private` within types. A `public` declaration there should be removed or explained.
**Recurrence guard:** the consumer analysis finds declarations with no consumer and narrows them (CR2).

## 6. A subclass in another module breaks on an upgrade

**Symptom:** a third party's subclass fails after your release, with no signature change on your side.
**Mechanism:** subclassability was granted, deliberately or by default, without an extension contract. Every change to the base now risks the subclass (R6).
**Diagnosis:** is every publicly subclassable class an intended extension point, documented and tested?

**Fix:** document the extension contract and test a subclass path; or close the class (`final` / `sealed` / `public`-not-`open`) and offer an interface instead.
**Recurrence guard:** subclassability is decided separately from visibility (CR11).

## 7. Test-only widening leaks to consumers

**Symptom:** a declaration is public, and its only external reference is a test.
**Mechanism:** `public` was used where the ecosystem has a test-visibility mechanism (R5).
**Diagnosis:** find public declarations referenced only from test files.

**Fix:** `@testable`, `InternalsVisibleTo`, the test source set, same-package tests, or `#[cfg(test)]`.
**Recurrence guard:** no declaration is public solely for tests (CR9, CR10).

## 8. A public function returns a type that is less visible

**Symptom:** a compile error about accessibility, or a type made public to satisfy one.
**Mechanism:** visibility propagates through signatures — every language enforces it (Swift states it as the guiding principle).
**Diagnosis:** check whether the type was widened to satisfy the signature. If it was, the fix went the wrong way.

**Fix:** ask whether the function should be public at all. Narrowing the function is usually correct; widening the type publishes it permanently.
**Recurrence guard:** no public signature references a less-visible type (CR12).

## 9. `protected` was assumed to mean "subclasses only"

**Symptom:** unrelated classes in the same package call a `protected` member.
**Mechanism:** Java's `protected` includes the whole package. In TypeScript a subclass can also widen it to public.
**Diagnosis:** verify the language's real `protected` scope before relying on it.

**Fix:** use composition or a private hook behind a public final method where "subclasses only" is intended.
**Recurrence guard:** `protected`'s scope is confirmed where it is used (CR13).

## 10. Removing a public declaration breaks a consumer nobody knew about

**Symptom:** a downstream project fails after a release, having depended on something you considered unused.
**Mechanism:** no consumer registry existed, so removal was blind (R2).
**Diagnosis:** is there any record of who depends on the surface?

**Fix:** deprecate first — announce, warn, window, then remove at the announced version.
**Recurrence guard:** deprecation precedes removal (CR14).

## 11. A ported design has different boundaries than the original

**Symptom:** a design moved from Kotlin to Swift (or any pair) exposes or hides more than intended.
**Mechanism:** the modifier was translated literally. `internal` means a compilation unit in Kotlin and a framework target in Swift; neither matches Go's package or C#'s assembly (R4-adjacent).
**Diagnosis:** compare the units and defaults of the two languages.

**Fix:** map by promise, not by keyword (see `language-models.md`).
**Recurrence guard:** a cross-language port is mapped, not translated (CR15).

## 12. A package split silently widens access

**Symptom:** after restructuring packages, code that was unreachable becomes reachable — or the reverse.
**Mechanism:** package-private access was relied on across what is now a boundary, and splitting one package into two *widens* the code that can reach each.
**Diagnosis:** diff the visibility graph before and after the restructure.

**Fix:** treat a package restructure as a visibility change, and review it as one.
**Recurrence guard:** package splits are reviewed for visibility effects (CR13-adjacent).

## 13. Blanket re-export publishes the module

**Symptom:** the surface includes declarations nobody intended to publish.
**Mechanism:** `export *` (or a blanket `pub use`) re-publishes everything a barrel file imports (R2).
**Diagnosis:** grep for `export *` / `pub use *`.

**Fix:** name each export explicitly.
**Recurrence guard:** the surface list is generated, so a blanket export shows up in the diff (CR5).

## 14. A test grant ships

**Symptom:** `InternalsVisibleTo` (or a similar grant) is present in a release artifact.
**Mechanism:** the attribute was added without checking the build configuration (R5).
**Diagnosis:** inspect the release build for the attribute or the named assembly.

**Fix:** exclude it from release builds; name one assembly rather than a wildcard; never treat it as a security boundary.
**Recurrence guard:** the test mechanism is verified absent from release (CR10).

## 15. A public field was fine until behaviour was added

**Symptom:** a data type with public fields needed an invariant, and now every setter bypasses it.
**Mechanism:** the type was a transparent data shape, which was legitimate; adding behaviour made the exposed representation a defect (the documented edge case).
**Diagnosis:** does the type now have invariants or behaviour? Then the public fields are the defect.

**Fix:** migrate to a private field plus an accessor, with a deprecation window for the field.
**Recurrence guard:** a transparent data type's intent is recorded, so adding behaviour triggers a review.

## The triage rule

Three findings — **a public surface defined by exclusion**, **an erasure-based or permeable modifier on a sensitive value**, and **a public mutable field** — are detectable with the sweep in `anti-patterns.md` and account for most visibility defects. Check those three first: the first means the contract is accidental, the second means a boundary does not exist, and the third means the representation is already published.
