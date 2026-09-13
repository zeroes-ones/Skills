# Callbacks and Re-entrancy

<!-- DEEP: 5+min -- re-entrancy, guards, queues and callback lifetime -->

> **Verification note.** Guard semantics (a GIL, an event loop, a dispatcher, a single-threaded
> apartment) differ per runtime and version. Confirm the rules for the runtime you are embedding or
> binding against, rather than relying on recall.

## Why callbacks are the hard case

A one-directional call has one set of rules. A callback inverts the direction, and with it:

| Added concern | Why |
|---|---|
| **Which thread** it arrives on | the native side chose the thread, not you |
| **Re-entrancy** | it may arrive while the original call is still on the stack |
| **Guard state** | the runtime's guard may or may not be held |
| **Lifetime** | the callback may outlive the registration, or the caller |
| **Teardown** | it may arrive while the runtime is shutting down |

This is R4, and the failure mode is a deadlock or a use-after-free — both of which reproduce rarely.

## The re-entrancy deadlock, explained

```text
Managed code calls native:
  managed → acquire guard → native_do_work() → ...

native_do_work calls back into managed:
  ... → callback() → acquire guard  ← DEADLOCK. The guard is already held.

The deadlock is on this thread. Nothing crashes. Nothing logs.
It simply never returns.
```

**Three resolutions, in order of preference:**

| Resolution | Mechanism |
|---|---|
| **Queue and return** | the callback enqueues work; the original call returns; the runtime drains the queue |
| **Re-entrant guard** | the runtime's guard permits re-entry (a recursive lock, or a re-entrancy-permitted state) |
| **Release, call back, re-acquire** | only safe if the managed state is valid without the guard — usually not |

**Queueing is the general answer.** The native side hands work to the runtime's event loop or work queue,
and the runtime executes it on its own terms. It converts a re-entrancy problem into an ordering problem,
which is far easier to reason about.

## The rules, stated for a boundary

Every callback needs these five statements:

| Statement | Example |
|---|---|
| **Arrival thread** | "the runtime's main thread" / "a native worker thread" / "any thread" |
| **Guard state on arrival** | "arrives with the guard acquired" / "the callee must acquire it" |
| **Re-entrancy permitted?** | "not permitted; the native side must queue" |
| **Lifetime bound** | "valid until `cancel_callback()` returns, and the native side must drain" |
| **Error handling** | "an exception in the callback must be caught by the runtime's mechanism" |

**"Any thread" is a warning, not a statement.** It means the caller must marshal, and that must be said.

## Threads created by the native side

A native-created thread calling into a managed runtime is a defect unless the thread is attached.

```text
Native spawns a thread ──▶ calls managed code
                          │
                          ├── NOT attached  → undefined behaviour, intermittent crash
                          └── attached first → defined behaviour
```

| Runtime | Attachment mechanism |
|---|---|
| JVM | `AttachCurrentThread` / `AttachCurrentThreadAsDaemon`; detach before thread exit |
| CPython | `PyGILState_Ensure` / `PyGILState_Release` for the thread's duration |
| Node | use an async work item, or `napi_threadsafe_function` for cross-thread calls |
| .NET | the runtime's thread attachment for interop |

**The defect signature:** an intermittent crash that only occurs when the native side is under load —
because the load is what makes the native side spawn or use extra threads.

## Guard disciplines, by runtime family

| Runtime family | Guard | The two opposite defects |
|---|---|---|
| CPython | the GIL | never releasing it around long native work (everything serialises); releasing it and touching Python objects before re-acquiring (corruption) |
| JVM | no GIL, but a safepoint model and thread attachment | attaching threads wrongly; retaining local references across a safepoint |
| Node | the event loop, single-threaded for JS | touching JS values off the main thread without the threadsafe mechanism |
| .NET | the runtime's own threading | calling into the runtime from an unattached native thread |
| Embedded interpreters | usually a single-threaded or explicit-lock model | re-entering while the interpreter is mid-operation |

**The CPython pair is worth memorising**, because both directions are common and both are severe: holding
the GIL during a long native computation is a performance defect, and releasing it carelessly is a
correctness defect.

## Callback lifetime

The use-after-free at teardown is the other classic:

```text
1. Managed code registers a callback with a native library.
2. Managed object is disposed / collected.
3. The native library invokes the callback.   ← the callback now points at freed state
4. Use-after-free, or a crash during shutdown.
```

**The contract that prevents it:**

| Requirement | Detail |
|---|---|
| Cancellation is explicit | an `unregister` that **blocks until in-flight invocations complete** |
| Registration holds a reference | the managed side keeps the callback target alive while registered |
| Teardown order is defined | drain the native side before releasing the managed runtime |
| A post-cancel invocation is rejected | the native side must not call after a successful unregister |
| The bound is enforced, not documented | a test asserting no invocation after unregister returns |

The key phrase is **blocks until in-flight invocations complete**. A non-blocking unregister returns while
the callback is still executing, and the caller then frees state the callback is using.

## Errors in the callback

An exception thrown in a callback is on the *native* stack, which is a foreign frame — the cross-frame
unwind prohibition applies (see `error-propagation.md`).

| Runtime | Mechanism |
|---|---|
| N-API | exception propagation helpers, or the threadsafe-function error path |
| JNI | the native method must check for a pending exception and clear it before returning |
| CPython | the callback must return a failure indicator and set the error state; the native side must propagate it |
| Rust callbacks into a runtime | catch at the callback boundary |

**"Log and swallow" is a legitimate choice only if it is stated**, because it changes the failure from an
error into an absence.

## Testing callbacks

```text
1. Re-entrancy: invoke the callback WHILE the original call is still on the stack.
     → must not deadlock; must be queued, or re-enter safely
2. Concurrency: invoke from N threads simultaneously.
     → no corruption; the stated safety holds
3. Unattached-thread: invoke from a native thread that was never attached.
     → must be attached by design (this test should pass, not crash)
4. Lifetime: unregister, then invoke.
     → no invocation after unregister returns
5. Teardown: begin shutdown, allow an in-flight invocation, complete shutdown.
     → drains safely; no use-after-free
6. Callback throws/panics.
     → caught at the boundary; converted; the host survives
7. Unregister during an in-flight call.
     → blocks until the invocation completes, then returns
```

Test 1 and test 4 are the two that find the real defects. Test 4 with a *concurrent* invocation is the
one that catches a non-blocking unregister.

## The inverted case: embedding

When native code drives an embedded managed runtime, the re-entrancy rules **invert**:

| Normal (managed drives native) | Embedded (native drives managed) |
|---|---|
| the managed runtime's guard is the constraint | the embedding contract is the constraint |
| callbacks from native must respect the guard | callbacks into managed are the *primary* path |
| the native side must not block the runtime | the embedder must not block the runtime's loop |
| teardown order: drain native, then release managed | teardown order: stop the embedder, then drain managed |

**State which direction the host is**, because applying the wrong convention produces the deadlock the
rules were meant to prevent.

## Checklist

- [ ] Every callback states its arrival thread, guard state, re-entrancy and lifetime (R4)
- [ ] The runtime's guard is never held while calling back (R4)
- [ ] Work is queued rather than re-entered where the guard does not permit re-entry
- [ ] Every native-created thread is attached to the runtime before touching its state
- [ ] Guard discipline is correct in both directions (released around native work; re-acquired before use)
- [ ] Unregister blocks until in-flight invocations complete
- [ ] No invocation occurs after a successful unregister returns
- [ ] Exception handling in the callback is defined and does not unwind across the frame
- [ ] Teardown order is defined and exercised
- [ ] All seven callback tests above are implemented, especially re-entrancy and post-unregister invocation
- [ ] The host direction (managed-drives-native or native-drives-embedded) is stated
