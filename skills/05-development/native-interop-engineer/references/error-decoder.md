# Error Decoder — Long Form

<!-- DEEP: 5+min -- the symptom catalogue in long form, with causes and fixes -->

The compressed table lives in `SKILL.md`. This file carries the full diagnosis.

## 1. A leak that appears only in long-running processes

**Symptom:** memory grows over hours or days; a short test shows nothing.
**Mechanism:** a pointer allocated on one side and never freed on the other. Each crossing leaks a small
amount; the total is invisible until the process has crossed the boundary millions of times.
**Diagnosis:** for each pointer at the boundary, ask who allocates and who frees. Then run a loop that
crosses the boundary repeatedly and watch the heap.

**Fix:** an ownership-matrix row per pointer; free on the allocating side, or provide the deallocator
(`free_string`-style) so the caller cannot get it wrong.
**Recurrence guard:** the ownership contract is reviewed per pointer (R1), not per call site.

## 2. Heap corruption that "works in testing"

**Symptom:** corruption in release builds, or on one platform only; debug builds are fine.
**Mechanism:** allocation on one side, free on the other, with different allocators. They happen to agree
in some builds — a shared runtime, a debug allocator — and diverge in others.
**Diagnosis:** trace the allocation and the free; compare the allocators.

**Fix:** one allocator for the whole boundary, a caller-provided allocator, or the arena pattern.
**Recurrence guard:** sanitizers in CI catch the moment the mismatch happens.

## 3. The process aborts with no message after a foreign call

**Symptom:** an immediate abort, no stack, no log, right after a call across the boundary.
**Mechanism:** a panic or exception unwound into a foreign frame, which is undefined behaviour (R3).
**Diagnosis:** is there containment at the outermost boundary function?

**Fix:** `catch_unwind` / `try`-`catch` at the boundary, converted to a result code, with the detail logged.
**Recurrence guard:** a test that forces a panic in the foreign path and asserts the process survives.

## 4. A call fails and the caller sees success

**Symptom:** silent wrong behaviour or data corruption; no error is ever reported.
**Mechanism:** a sentinel error value that is also a legitimate return — a `-1` count that means both
"unknown" and "error", a `NULL` that means both "absent" and "failed" (R3).
**Diagnosis:** for every sentinel, ask whether the value can be legitimate.

**Fix:** an explicit out-parameter or a result type; the failure must be distinguishable from success on
every path.
**Recurrence guard:** the error contract is tested at every code, including unknown ones.

## 5. Deadlock under load, never in single-threaded tests

**Symptom:** the process hangs, with no crash and no log; only under concurrency.
**Mechanism:** a callback re-entered the runtime while its guard was held. The deadlock is on one thread and
never resolves (R4).
**Diagnosis:** does any native code call back during a call it received from the runtime?

**Fix:** queue the work and return; never call back while holding the guard.
**Recurrence guard:** the re-entrancy test invokes the callback while the original call is on the stack.

## 6. An intermittent crash on a native-created thread

**Symptom:** a crash under load, never in tests.
**Mechanism:** the native side spawned or used a thread that was never attached to the runtime, so the
runtime was called from an unknown thread.
**Diagnosis:** does every native thread attach before touching runtime state?

**Fix:** attach before the first call; detach before exit; or marshal to the runtime's own thread.
**Recurrence guard:** a test that invokes the boundary from a freshly created thread.

## 7. A use-after-free during shutdown

**Symptom:** a crash at teardown, or after cancelling an operation.
**Mechanism:** a callback outlived its registration, or arrived while the runtime was being torn down
(R4).
**Diagnosis:** does unregister block until in-flight invocations complete? Is the teardown order defined?

**Fix:** a blocking unregister, a reference held by the registration, and a drain-before-release teardown
order.
**Recurrence guard:** a test that unregisters and then invokes; no invocation may occur.

## 8. The FFI call is slower than the pure-language version

**Symptom:** the boundary was added for speed and the operation got slower.
**Mechanism:** the per-crossing cost multiplied by the crossing count exceeds the gain from the faster
kernel (R2, R6).
**Diagnosis:** measure the empty crossing, a typical crossing, and the crossing count per operation.

**Fix:** reduce the crossing count structurally (bulk transfer, iterator handle), or reconsider the
boundary.
**Recurrence guard:** the harness from the justification decision is retained and re-run.

## 9. The build breaks on one platform days before release

**Symptom:** the boundary does not build for a target that was never in CI.
**Mechanism:** the second toolchain was added for the development platform only.
**Diagnosis:** is the boundary built in CI for every shipping platform?

**Fix:** add it to every target's pipeline.
**Recurrence guard:** the build matrix includes the boundary for every shipping platform.

## 10. Corrupted strings in one locale

**Symptom:** text looks right in development and wrong for some users.
**Mechanism:** an encoding mismatch — a platform code page interpreted as UTF-8, or a UTF-16 buffer
treated as bytes.
**Diagnosis:** state the encoding on both sides; check whether a conversion happens.

**Fix:** UTF-8 explicitly, with a stated conversion where the runtime differs.
**Recurrence guard:** the string tests include non-ASCII, emoji and both directions.

## 11. A string silently truncated

**Symptom:** data is cut off at a character nobody typed.
**Mechanism:** a bare `char*` used for data that can contain a NUL, so the receiving side stops at the NUL.
**Diagnosis:** is a length passed wherever the data could contain a NUL?

**Fix:** pass an explicit length for any non-plain-text data.
**Recurrence guard:** the embedded-NUL test is in the string suite.

## 12. Corruption after a compiler or version upgrade

**Symptom:** a boundary that worked for a year breaks on a toolchain update.
**Mechanism:** a struct passed by layout with no assertion, so the layout drifted silently.
**Diagnosis:** is there a `_Static_assert` on `sizeof` and key offsets for every public struct?

**Fix:** assert the layout at build time, or move to accessors.
**Recurrence guard:** the assertions are in the header, so drift is a compile error.

## 13. Throughput collapses under concurrency

**Symptom:** adding threads does not add throughput; the runtime serialises.
**Mechanism:** the guard was held for the entire native call, so every thread queues behind it (R4).
**Diagnosis:** is the guard released around the work?

**Fix:** acquire, copy what is needed, release, work, re-acquire, publish.
**Recurrence guard:** a test asserts that other threads make progress during a long native call.

## 14. A memory-safety defect found by a security review

**Symptom:** an out-of-bounds write in an `unsafe` region, potentially an exploit primitive.
**Mechanism:** the region's invariants were assumed rather than checked (Anti-Hallucination).
**Diagnosis:** is every `unsafe` block documented with its invariants and reviewed?

**Fix:** document the invariants, add validation, or wrap it in a checked abstraction.
**Recurrence guard:** every boundary `unsafe` region is a review item.

## 15. Unexplained behaviour after adopting a binding library

**Symptom:** ownership or threading behaviour differs from expectations.
**Mechanism:** the wrapper's guarantees were assumed rather than read (R5).
**Diagnosis:** can you state what the wrapper guarantees and what it leaves to you?

**Fix:** enumerate both; implement what it leaves; record the guarantees relied upon.
**Recurrence guard:** the binding's guarantees are re-checked on upgrade.

## The triage rule

Three findings — an unowned pointer, missing containment at the boundary, and no sanitizers in CI — account
for most interop defects reaching production, and all three are detectable in an afternoon. Check the
ownership contract, the containment wrapper, and the sanitizer pipeline before any deeper interop review.
