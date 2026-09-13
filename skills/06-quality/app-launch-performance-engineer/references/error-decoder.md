# Error Decoder — Long Form

<!-- DEEP: 5+min -- the symptom catalogue in long form, with causes and fixes -->

The compressed table lives in `SKILL.md`. This file carries the full diagnosis.

## 1. "Cold start is slow on some devices, fine on mine"

**Symptom:** the team cannot reproduce the report. Launch feels instant on the development device.
**Mechanism:** the measurement was taken on the fastest device class, or with a warm process, or both.
The complaint comes from the median device, cold — which is a different machine state entirely.
**Diagnosis:** name the device class you measured on, and confirm the process was killed between runs.

**Fix:** measure cold, on the median device class, ≥10 runs, reporting median and p90.
**Recurrence guard:** the device class and mode are recorded with every launch figure (R1).

## 2. First frame is fast, but the app is unusable for seconds

**Symptom:** the screen appears immediately and looks complete, but taps do nothing for a noticeable
period.
**Mechanism:** TTID was optimised and TTFD was never measured. The deferred work still runs on the
main thread after the first frame.
**Diagnosis:** measure both metrics; a large TTID-to-TTFD gap localises the problem to Phase 3.

**Fix:** move post-frame work off the main thread, or sequence it later; ship a compilation profile
where the runtime supports one.
**Recurrence guard:** TTID and TTFD are both reported, always (R2).

## 3. A regression appeared after adding one dependency

**Symptom:** a launch regression of hundreds of milliseconds, with no obvious code change to blame.
**Mechanism:** the dependency added a static initializer or a self-registration hook, which runs before
the app's own code. Nothing in the app's diff looks expensive.
**Diagnosis:** build the self-initialisation inventory (not the app's own code inventory) and ablate.

**Fix:** defer, consolidate or remove the initialiser; where it self-registers, remove the replaced
hook.
**Recurrence guard:** every dependency addition triggers the init inventory (CR4-adjacent).

## 4. Android cold start exceeds the published excessive threshold

**Symptom:** the platform's own vitals flag start-up as excessive.
**Mechanism:** commonly third-party SDKs declaring content providers, which run before the app's own
`onCreate`. Android's App Startup library exists to consolidate these — and its documentation requires
removing the providers it replaces.
**Diagnosis:** inspect the **merged** manifest, not the source manifest. The providers arrive from
dependency manifest merges and are invisible in your own file.

**Fix:** consolidate the initialisers into one ordered path, remove the old providers, and ship a
compilation profile for the interactive paths.
**Recurrence guard:** the merged manifest is checked for providers on every dependency addition.

## 5. The splash screen keeps getting longer

**Symptom:** the splash's duration grew each release; the app still takes as long to become usable.
**Mechanism:** the splash absorbed growing initialisation work instead of covering a fixed wait. The
underlying cost was never reduced, so the cover grew with it.
**Diagnosis:** is there any measurement of the work behind the splash? Usually not.

**Fix:** measure and reduce the work, then size the splash to the residual. A splash is a cover, not a
cure (R4).
**Recurrence guard:** the Verification step checks whether a splash is being used as the fix.

## 6. A measured improvement disappears in the next build

**Symptom:** a launch improvement was reported and verified, and the next release shows the old number.
**Mechanism:** the before/after comparison changed conditions — a different device, a cleared cache on
one side only, a different instrument, or a different run count.
**Diagnosis:** compare the recorded *methods*, not only the numbers.

**Fix:** re-measure both sides with one method, publish the noise floor, and require the method with
the number.
**Recurrence guard:** the method is part of the deliverable, recorded with the figure (R5).

## 7. Serverless cold start is seconds with a trivial handler

**Symptom:** the handler does almost nothing; the cold start is still measured in seconds.
**Mechanism:** the module graph is the cost. Every module imported at module scope is evaluated on
instance start, before the handler runs.
**Diagnosis:** measure the import graph with the runtime's tooling; rank by **self** time, not
cumulative.

**Fix:** remove module-scope work, defer imports, tree-shake the entry, split a monolithic entry.
**Recurrence guard:** the entry's import graph is measured when the function is next modified.

## 8. A Python CLI takes hundreds of milliseconds before doing anything

**Symptom:** a simple command feels sluggish; the work it performs is trivial.
**Mechanism:** the package's `__init__.py` imports the whole framework so convenience imports work —
paid on every single invocation, because a CLI is cold every time.
**Diagnosis:** `python -X importtime` shows "module name, cumulative time (including nested imports)
and self time (excluding nested imports)" per the Python documentation.

**Fix:** make the package's top-level import lazy, preserving the convenience API via lazy attribute
access.
**Recurrence guard:** CLI latency is measured per invocation in CI, not once at development.

## 9. Optimisation effort produced no measurable change

**Symptom:** weeks of work; the number did not move.
**Mechanism:** the work targeted a mode or a phase that was not the bottleneck — commonly cold-launch
work applied to Phase 1 when Phase 3 dominates, or hot-start work against a cold-launch complaint.
**Diagnosis:** re-read the complaint's mode and the attribution's dominant phase.

**Fix:** re-scope to the dominant phase of the failing mode. Attribution before work (R3, R6).
**Recurrence guard:** the dominant phase is named before a fix is chosen.

## 10. The budget held for two releases, then drifted

**Symptom:** launch slowly increased despite a stated target.
**Mechanism:** the budget was a number with no gate. Each release added a little initialisation and
nothing removed it, because nothing failed.
**Diagnosis:** name the thing that fails when the budget is exceeded. If nothing does, there is no
budget.

**Fix:** a CI benchmark that fails the build, plus a production alert, plus a defined failure response.
**Recurrence guard:** the budget is a gate, and increases require a recorded reason and a re-review
date (R4).

## 11. A first-use stutter that is not a launch problem

**Symptom:** the app launches fine, and the *first* time a specific screen is opened it pauses.
**Mechanism:** lazy binding resolving symbols, or lazy initialisation running, at first use of that
path. The cost was deferred, not removed.
**Diagnosis:** measure first-call latency on that path; compare the first open to the second.

**Fix:** eager binding or pre-warming for that path — a decision belonging to
`library-linkage-architect` (binding mode). Do not file it as a launch regression.
**Recurrence guard:** first-use latency is measured separately from launch.

## 12. The CI runner shows a regression that users do not see

**Symptom:** the gate fails intermittently; production metrics are fine.
**Mechanism:** the CI runner varies between builds (shared hardware, thermal state, noisy neighbours),
so the gate measures the runner as much as the app.
**Diagnosis:** establish the runner's noise floor by measuring the unchanged build twice.

**Fix:** pin the runner, increase the run count, or move the gate to a nightly schedule with a
production alert carrying the per-change signal.
**Recurrence guard:** the noise floor is recorded with the gate, and the gate is not disabled for
flakiness.

## 13. Deep links or restored sessions make launch look slow

**Symptom:** cold start is fine in a plain launch and slow when the app is opened from a link or with a
restored session.
**Mechanism:** the measured "cold start" included restoration work that a plain launch does not
perform. The extra work is real, but it is not initialisation.
**Diagnosis:** separate the launch paths — plain launch, link launch, restored session — and measure
each.

**Fix:** budget and optimise each path separately; do not average them into one number.
**Recurrence guard:** the launch paths are enumerated, and the budget names which one it covers.

## The triage rule

Three of these symptoms — the wrong-device measurement, the TTID/TTFD conflation, and the unattributed
cause — are detectable in under an hour and account for most launch work that produces no result. Run
the mode triage, then the two-metric measurement, then the phase attribution, in that order, before
touching any code.
