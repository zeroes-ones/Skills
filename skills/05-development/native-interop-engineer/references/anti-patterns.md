# Anti-Patterns

<!-- STANDARD: 3min -- the interop anti-pattern catalogue with detection heuristics -->

## 1. The unowned pointer

**Symptom:** a leak in long-running processes, or heap corruption that only appears in some builds.
**Cause:** a pointer crosses with no stated allocator or freer (R1).
**Detection:** for every pointer at the boundary, ask who allocates and who frees. Silence is the finding.

**Fix:** an ownership-matrix row per pointer; free on the allocating side or provide the deallocator.

## 2. The mismatched allocator

**Symptom:** corruption in release builds, fine in debug; or fine on one platform, broken on another.
**Cause:** allocation on one side, free on the other, with different allocators (R1).
**Detection:** grep for `free(` / `delete` on pointers that were allocated on the other side.

**Fix:** one allocator for the whole boundary, or a caller-provided allocator, or an arena.

## 3. The cross-frame unwind

**Symptom:** a process abort with no message, immediately after a foreign call.
**Cause:** a panic or exception unwound into a foreign frame (R3).
**Detection:** is there a `catch_unwind` / `try`/`catch` at the outermost boundary function?

**Fix:** contain at the boundary; convert to a result; never let it cross.

## 4. The sentinel collision

**Symptom:** a failure reported as success; silent data corruption.
**Cause:** an error sentinel that is also a legitimate value (R3).
**Detection:** for every sentinel, ask "can this value be legitimate?" If yes, it is a bug.

**Fix:** an explicit out-parameter or result type.

## 5. The unchecked return code

**Symptom:** failures that never surface; the same error repeating silently.
**Cause:** callers ignore the status code.
**Detection:** count the calls and the checks. A gap is the finding.

**Fix:** a one-line conversion helper per language so checking is idiomatic, and error codes that map to the
language's error type.

## 6. The guard re-entrancy deadlock

**Symptom:** a deadlock under load, never single-threaded.
**Cause:** a callback invoked while the runtime's guard is held (R4).
**Detection:** does any native code call back into the runtime during a call it received from it?

**Fix:** queue and return; never call back while holding the guard.

## 7. The unattached thread

**Symptom:** an intermittent crash under load that never reproduces in tests.
**Cause:** a native-created thread called into the runtime without attaching (R4).
**Detection:** does every native thread that touches the runtime attach first?

**Fix:** attach before the first call; detach before exit; or marshal to the runtime's thread.

## 8. The unbounded callback lifetime

**Symptom:** a use-after-free at teardown, or after cancellation.
**Cause:** the callback outlived its registration (R4).
**Detection:** does unregister block until in-flight invocations complete?

**Fix:** a blocking unregister, a registration-held reference, and a defined teardown order.

## 9. The per-element crossing

**Symptom:** cost grows linearly with collection size, far above the actual work.
**Cause:** crossing once per element instead of once per collection (R2).
**Detection:** count crossings per operation.

**Fix:** bulk transfer, or an iterator handle.

## 10. Serialise-everything

**Symptom:** the boundary dominates the profile; each call costs microseconds of encode/decode.
**Cause:** JSON/serialised payloads chosen for simplicity, never measured (R2).
**Detection:** measure the per-crossing cost; compare against a handle-based shape.

**Fix:** a handle for objects; serialisation only where the data is genuinely an object graph.

## 11. The guard held for the whole call

**Symptom:** throughput collapses under concurrency; the runtime serialises.
**Cause:** the guard was never released around the long native work (R4).
**Detection:** is the guard released around the work, or held throughout?

**Fix:** acquire, take what is needed, release, work, re-acquire, publish.

## 12. The `unsafe` region with no review

**Symptom:** a memory-safety defect that may be a security issue.
**Cause:** the invariants the region relies on were assumed (Anti-Hallucination).
**Detection:** is every `unsafe` block documented with its invariants and reviewed?

**Fix:** document the invariants, add bounds/validity checks, or wrap it in a safe abstraction.

## 13. The layout assumption

**Symptom:** corruption after a compiler, platform or version change.
**Cause:** a struct passed by layout with no static assertion (Decision Tree 2).
**Detection:** is there a `_Static_assert` / `sizeof` assertion for every public struct?

**Fix:** assert the layout at build time, or use accessors.

## 14. The unmeasured performance justification

**Symptom:** the FFI version is slower than the pure-language version.
**Cause:** FFI chosen for anticipated speed, never measured (R2, R6).
**Detection:** is there a harness with the empty crossing and the crossing count?

**Fix:** measure before committing; reconsider the boundary if it loses.

## 15. The toolchain that only builds on one machine

**Symptom:** a build break discovered days before release, on one platform.
**Cause:** the second toolchain was never added to every target's pipeline.
**Detection:** is the boundary build in CI for every shipping platform?

**Fix:** add it; a second toolchain is a second maintenance surface, and CI is where that is contained.

## 16. The binding library treated as a contract

**Symptom:** unexpected ownership, threading or error behaviour.
**Cause:** the wrapper's guarantees were assumed rather than read (R5).
**Detection:** can you state what the wrapper guarantees and what it leaves to you?

**Fix:** enumerate both; implement what it leaves; document the guarantees relied upon.

## Detection sweep

```bash
SRC="${1:-src}"

echo "== unsafe blocks (each needs a reviewed invariant) =="
grep -rnE '\bunsafe\b' "$SRC" 2>/dev/null | wc -l | xargs echo "  count:"

echo "== boundary entry points and whether they contain failures =="
grep -rnE 'extern "C"|JNIEXPORT|#\[no_mangle\]|DllImport|LibraryImport|napi_' "$SRC" 2>/dev/null | head -10

echo "== catch/contain at the boundary =="
grep -rnE 'catch_unwind|catch\s*\(|PyErr_SetString|napi_throw' "$SRC" 2>/dev/null | head -5 \
  || echo "  NONE — check whether failures can unwind across"

echo "== allocator mismatch risk: allocation and free on different sides =="
grep -rnE '\b(malloc|calloc|new )\b' "$SRC" 2>/dev/null | head -5
grep -rnE '\b(free|delete)\s*\(' "$SRC" 2>/dev/null | head -5

echo "== ownership documentation =="
find . -iname '*ownership*' -o -iname '*interop*contract*' 2>/dev/null | head || echo "  NONE"

echo "== layout assertions for public structs =="
grep -rnE '_Static_assert|static_assert' "$SRC" 2>/dev/null | head -3 || echo "  NONE"

echo "== sentinel error returns (check for collision with valid values) =="
grep -rnE 'return -1;|return NULL;|return nullptr;' "$SRC" 2>/dev/null | head -5

echo "== thread attachment before runtime calls =="
grep -rnE 'AttachCurrentThread|PyGILState_Ensure|napi_threadsafe_function' "$SRC" 2>/dev/null | head -3 \
  || echo "  NONE — check whether native threads call into the runtime"

echo "== sanitizers in CI =="
grep -rnE 'asan|address.?sanitizer|tsan|thread.?sanitizer|miri|valgrind' .github/workflows/ 2>/dev/null | head \
  || echo "  NONE — memory defects will not be caught in CI"
```

Interpretation: **no containment** at the boundary plus a `catch`-free codebase is a cross-frame unwind
waiting to happen. **No ownership documentation** means the contract is implicit and will be violated.
**No sanitizers in CI** means every memory defect on this list is discovered by users.
