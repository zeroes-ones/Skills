# Error Decoder — Long Form

<!-- DEEP: 5+min -- the symptom catalogue in long form, with causes and fixes -->

The compressed table lives in `SKILL.md`. This file carries the full diagnosis.

## 1. An extension update breaks dozens of integrations at once

**Symptom:** a host release ships and integrations fail across the ecosystem, publicly and simultaneously.
**Mechanism:** there was no stability tier and no version-negotiation rule, so every extension had been
written against an unstated contract — and the host changed it as an internal change.
**Diagnosis:** is there a published tier table? Does every extension declare a target range?

**Fix:** declare tiers, require a declaration, define every mismatch outcome, and give a deprecation
window. Rehearse the break with a real extension before shipping it.
**Recurrence guard:** the version matrix is tested, including the degradation case (R2).

## 2. A malicious extension exfiltrates user data

**Symptom:** an extension that never requested network capability is found sending user data outward.
**Mechanism:** capabilities were declared in the manifest and documented, but nothing checked them. A
declared permission with no enforcement point is not a control (R3).
**Diagnosis:** trace the operation from extension code to the primitive. Does anything refuse?

**Fix:** a single enforcement chokepoint, default deny, typed refusals, and an audit log. Verify by
building an extension that lacks the capability and confirming the attempt fails.
**Recurrence guard:** the hostile-extension test suite runs per class (R3).

## 3. A third-party defect takes down the host

**Symptom:** the product becomes unavailable and the cause is an extension's crash or infinite loop.
**Mechanism:** untrusted code ran in-process with no isolation, so the extension's failure was the host's
failure (R5).
**Diagnosis:** is there a timeout on host-to-extension calls? Is a crash contained?

**Fix:** isolate by a named mechanism — a sandboxed runtime for untrusted code, a separate process where
crash containment matters — and put a timeout on every call.
**Recurrence guard:** failure containment is tested per class by deliberately causing each failure.

## 4. The platform cannot remove a compromised extension

**Symptom:** a supply-chain compromise is identified and there is no mechanism to disable it at scale.
**Mechanism:** no disable, rollback or revocation state; removal means uninstalling or shipping a host
release (R4).
**Diagnosis:** walk the lifecycle. Can you disable it? Roll it back? Revoke it remotely?

**Fix:** disable, rollback and revocation as first-class states, with the offline behaviour defined and a
publisher appeal path.
**Recurrence guard:** the lifecycle is exercised end to end in a rehearsal (Phase 9).

## 5. Extension authors abandon the platform

**Symptom:** the launch announcement produced a handful of extensions and no momentum.
**Mechanism:** no scaffold, no local host, no test harness — so the first hour was too slow and the
developers left before anything worked (R6).
**Diagnosis:** time a real developer from start to a working extension.

**Fix:** scaffold, local host, test harness, structured errors, one-command packaging. Measure
time-to-first-working-extension against a stated budget.
**Recurrence guard:** the DX budget is tracked and re-measured each quarter.

## 6. Every host release requires an ecosystem-wide migration

**Symptom:** each host release has an associated migration project for every integration.
**Mechanism:** extension points exposed host internals, so every internal change was a public break (R1).
**Diagnosis:** do any published extension points reference host-internal types or structures?

**Fix:** replace internals with intent-level abstractions and opaque handles; move the rest to an
experimental tier.
**Recurrence guard:** every new extension point is reviewed against the abstraction test.

## 7. Silent capability expansion

**Symptom:** users discover after the fact that an update gained access to their content.
**Mechanism:** the update path granted new capabilities without a consent event, which is
indistinguishable from an attack from the user's perspective.
**Diagnosis:** does an update that adds a capability require re-consent?

**Fix:** expansion is a consent event. Declining keeps the old grants and the old version, or updates
degraded, per design.
**Recurrence guard:** the capability-expansion rule is enforced by the update path, not by policy.

## 8. A plugin update needs a host restart for every user

**Symptom:** updating an extension requires restarting the product; users lose state.
**Mechanism:** the lifecycle depended on unloading, which is unreliable — a shared object unloads only
when its reference count reaches zero and nothing else references it.
**Diagnosis:** does the design mention unloading as the update mechanism?

**Fix:** version and load alongside; route new work to the new version and accept bounded resident
versions.
**Recurrence guard:** the lifecycle uses versioned loads, not unload (see `library-linkage-architect`).

## 9. Developers cannot diagnose a load failure

**Symptom:** support volume is high for simple problems; forum threads end in workarounds.
**Mechanism:** host errors named the symptom, not the cause or the next action.
**Diagnosis:** read the host's error strings. Do they say what to do?

**Fix:** cause, next action, and a link to the specific fix — implemented at the error site, since a
developer reads the error and not the docs.
**Recurrence guard:** the actionable-error coverage is measured as a percentage.

## 10. An extension works locally and fails at install

**Symptom:** a developer's tested extension fails the moment it is installed for a user.
**Mechanism:** local development granted all capabilities, so the capability model was never exercised
until install time.
**Diagnosis:** does local development enforce the real capability set?

**Fix:** enforce locally. The developer should discover the model in their first hour, not in
production.
**Recurrence guard:** the local host runs with the same capability enforcement as production.

## 11. The ecosystem becomes a monoculture

**Symptom:** two or three extensions hold nearly all installs; the platform has the risk of a platform
with none of the diversity.
**Mechanism:** the platform-versus-partner boundary was never published, so one publisher took the whole
adjacent space, and no one else had an incentive to compete.
**Diagnosis:** what is the concentration metric? Was a boundary published?

**Fix:** publish what the platform will and will not build; honour it. Address the incentive gap for
classes with no commercial value.
**Recurrence guard:** concentration is tracked and reviewed, not assumed healthy.

## 12. The platform ships a feature a partner's extension provided

**Symptom:** the ecosystem's trust collapses after the platform builds a popular extension's feature.
**Mechanism:** the boundary was never published, or was violated for a roadmap reason.
**Diagnosis:** is there a written boundary? Did the roadmap respect it?

**Fix:** publish the boundary, and honour it. A single violation is a permanent signal to every remaining
developer that the line moves against them.
**Recurrence guard:** the platform-versus-partner boundary is a review gate for roadmap items.

## 13. A platform rule invalidates the distribution model

**Symptom:** redistribution or review blocks the designed distribution.
**Mechanism:** the channel's rules were never confirmed before the model was designed.
**Diagnosis:** is there a recorded, dated confirmation per channel?

**Fix:** confirm the rules first — third-party code, bundled runtimes, signing, review, update mechanism.
A forbidden model is not a choice.
**Recurrence guard:** the platform-constraint check precedes the distribution design.

## 14. An extension cannot be identified in support

**Symptom:** a user reports a problem and support cannot tell which extension caused it.
**Mechanism:** the manifest lacks an identity, or it is not surfaced in diagnostics.
**Diagnosis:** is the extension's id and version visible in logs, crash reports and the UI?

**Fix:** require identity in the manifest; surface it in diagnostics, alongside its version and
capabilities.
**Recurrence guard:** identity is a required manifest field.

## 15. Extensions accumulate, and nobody uses them

**Symptom:** many published extensions, most never updated and rarely installed.
**Mechanism:** the incentive exchange does not work — no reach, no revenue, or too much contract
instability for the value on offer.
**Diagnosis:** which classes are alive and which are abandoned? What does the developer get?

**Fix:** reduce friction for low-incentive classes; address reach or revenue for classes with real value;
publish the boundary so developers can assess the risk.
**Recurrence guard:** ecosystem health metrics, including abandonment rate, are reviewed.

## The triage rule

Three findings — capabilities declared but unenforced, no removal path, and no scaffold — are detectable
in an afternoon and predict most platform failures. The first is a security control that does not exist,
the second means harm cannot be remediated, and the third means the ecosystem will not form. Check those
three before any deeper platform review.
