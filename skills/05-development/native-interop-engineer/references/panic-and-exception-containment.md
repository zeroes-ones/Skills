# Panic and Exception Containment

<!-- STANDARD: 3min -- containing a foreign frame's failure -->

## The rule

**A failure must not unwind into a foreign frame.** In most runtimes, unwinding through a frame that does
not expect it is undefined behaviour: the result ranges from a clean abort to silently corrupted state.
Containment is not a nicety; it is the precondition for calling across the boundary at all.

This belongs to R3 (error propagation) and is enforced in Phase 8 of the workflow.

## What "containment" means at each boundary

| Boundary | The failure | Where it is caught |
|---|---|---|
| Rust `extern "C"` | a panic | `catch_unwind` inside the extern function |
| C++ across a C ABI | an exception | `try`/`catch` inside the `extern "C"` wrapper |
| JNI native method | a pending Java exception | the native method checks and clears; or the JVM's check APIs |
| CPython extension | a Python error indicator | the extension returns a failure indicator and sets the error |
| N-API | a JS exception | the runtime's exception propagation helpers |
| .NET P/Invoke | a managed exception | it must not cross into native; catch on the managed side |
| WASM module | a trap | the host's trap handling |

**The pattern in every row:** catch *inside* the boundary function, and convert to a value the other side
understands.

## The wrapper pattern

Put the containment in one place, at the boundary, rather than scattering it:

```rust
// The ONLY place a panic may be caught. Everything else is inside.
// (The real code also carries the no_mangle attribute, noted in prose above.)
pub extern "C" fn api_process(in_ptr: *const Input, out: *mut Output) -> i32 {
    // catch_unwind prevents the panic from crossing the extern "C" frame
    match std::panic::catch_unwind(AssertUnwindSafe(|| {
        let input = unsafe { &*in_ptr };   // validated above, in the real version
        process(input)                     // may panic internally
    })) {
        Ok(Ok(value))  => { unsafe { (*out) = value; } STATUS_OK }
        Ok(Err(err))   => err.status_code(),
        Err(_panic)    => STATUS_INTERNAL,   // caught, converted, logged
    }
}
```

Properties worth naming:

| Property | Why |
|---|---|
| The `extern "C"` signature | unwinding is not permitted to cross it |
| `catch_unwind` inside | the panic is caught before the frame boundary |
| A stable panic→code mapping | the caller gets a typed failure, not an abort |
| The detail logged, not exposed | internal state is not leaked across the boundary |
| `AssertUnwindSafe` used deliberately | the safety argument is made explicitly, not assumed |

**The C++ equivalent** is a `try`/`catch(...)` inside an `extern "C"` wrapper function, converting to a
return code. The same shape: the catch is the outermost statement of the boundary function.

## The `unsafe` interaction

Catching a panic does not make the *state* safe. A panic may have left a value inconsistent, so:

| Requirement | Detail |
|---|---|
| State the invariant | what must be true for the unwind to be safe to absorb |
| Prefer abort to corrupt state | where the invariant cannot hold, an abort is the honest choice |
| Validate before use | arguments are validated before the fallible work, not after |
| Do not catch and continue blindly | a caught panic that corrupted shared state must not be ignored |

**The honest position:** `catch_unwind` converts a *process abort* into a *reported error*, which is
strictly better for the caller. It does not repair the state, and claiming that it does is a safety
fiction.

## Containment at the process boundary

Some failures cannot be contained in-process:

| Failure | Reality | Response |
|---|---|---|
| A segmentation fault | process-fatal | isolate the boundary in a subprocess |
| An `abort()` in a third-party library | process-fatal | isolate, or replace the library |
| A stack overflow | process-fatal | bound recursion at the boundary |
| A hang | the caller waits forever | a timeout where the mechanism allows, or a subprocess |
| An out-of-memory in a native allocator | often unrecoverable | report if possible; isolate where it matters |

**The design response is isolation, not a return code.** A boundary that can die cannot be protected by an
error mechanism; it must be run somewhere its death is survivable. That is one of the strongest arguments
for a subprocess or a sandboxed runtime for untrusted or fragile native code.

## Where to catch, and where not to

| Catch here | Do not catch here |
|---|---|
| The boundary function, at its outermost statement | Deep inside, where the state is unknown |
| Around the call into foreign code | Around your own internal logic (let it propagate internally) |
| Where a conversion to an error code is required | Everywhere, "just in case" |

**Catching too eagerly is its own defect:** it hides defects inside your own code by converting them into
errors that look like expected failures.

## Testing containment

```text
1. Force a panic/exception in the foreign code path.
     → the caller receives an error code; the process survives
2. Force a panic during a callback.
     → contained at the callback boundary; the host survives
3. Force a panic after partial state mutation.
     → the documented invariant holds, or the failure is escalated rather than absorbed
4. Force an out-of-bounds access (where a sanitizer is available).
     → the sanitizer catches it; the test asserts the boundary's validation
5. Confirm no abort appears in the logs for cases 1 and 2.
```

Test 1 and 2 are the mandatory pair. Test 3 is where the honest limits of containment are documented.

## Checklist

- [ ] Every boundary function contains foreign failures at its outermost statement (R3)
- [ ] No exception or panic can unwind into a foreign frame
- [ ] A stable mapping from the failure to an error code exists, and the detail is logged not exposed
- [ ] The state invariant required for absorption is stated, or an abort is preferred
- [ ] Containment is not used to hide defects in your own code
- [ ] Process-fatal failures are handled by isolation, not by a return code
- [ ] Containment is tested by forcing a failure, and the process is asserted to survive
- [ ] A callback's failure is contained at the callback boundary
