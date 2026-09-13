# Binding Mechanisms

<!-- DEEP: 5+min -- JNI, cgo, PyO3, N-API, P/Invoke and their contracts -->

> **Verification note.** Binding mechanisms and their safety guarantees change between runtime and
> library versions. Confirm a specific API or guarantee against the documentation for the version you are
> building against, rather than relying on recall.

## The mechanisms

| Boundary | Mechanism | Tooling | Note |
|---|---|---|---|
| JVM ↔ native | JNI | javac/javah, or a binding layer (JNA, Panama, a Rust/Python binding crate) | the oldest and most verbose; safety depends on your `unsafe` discipline |
| Python ↔ native | CPython C API | C extension, or PyO3 / cffi / ctypes | the GIL is the central constraint |
| Node.js ↔ native | N-API | node-addon-api, or raw N-API | N-API is ABI-stable across Node versions; raw V8 is not |
| .NET ↔ native | P/Invoke (`LibraryImport`/`DllImport`) | the runtime's marshaler | marshalling attributes are the contract |
| Go ↔ C | cgo | `import "C"` | pointer-passing rules are stricter than they look |
| Rust ↔ C | `extern "C"` + `#[no_mangle]` / `unsafe extern` | cbindgen | Rust's safety ends at the boundary |
| Kotlin Multiplatform ↔ native | platform interop (JNI on Android, cinterop on native) | the KMP toolchain | interop differs per target |
| Any ↔ WASM | the runtime's import/export model | the toolchain's bindings | capability-set-as-imports; sandboxed |

**The single most important property to note per mechanism:** *what it guarantees about memory and
errors*, because that is what you must implement yourself.

## What each mechanism guarantees — and what it leaves to you

| Mechanism | Guarantees | Leaves to you |
|---|---|---|
| JNI | the JVM's object model, reference kinds (local/global/weak), exception check APIs | every native allocation, every local-reference release, every exception check |
| CPython C API | reference counting, GIL acquisition APIs, error indicators | refcount balance, GIL discipline, thread attachment |
| N-API | a stable ABI, handle scope semantics, exception propagation helpers | scope management, buffer lifetimes, thread-safety of your state |
| P/Invoke | marshalling of declared types, some automatic lifetime handling | unmanaged memory ownership, calling conventions, string lifetimes |
| cgo | C-compatible calls, some pointer rules enforced at runtime | thread attachment, the pointer-passing rules (stricter than they appear) |
| `extern "C"` (Rust) | nothing across the boundary | panic containment, every pointer, every safety invariant |
| WASM | sandbox isolation, no ambient authority | marshalling, the capability model, the host imports |

**The pattern:** every mechanism guarantees its *own* runtime's rules and nothing about the memory you
pass. That memory is always yours to manage.

## JNI: the reference kinds

The distinction that causes most JNI leaks:

| Kind | Lifetime | Who frees |
|---|---|---|
| **Local reference** | until the native method returns (or the frame is popped) | the VM, automatically — but there is a limit per frame |
| **Global reference** | until explicitly deleted | you, explicitly |
| **Weak global** | until the object is collected | you, explicitly |

**The classic leak:** creating local references in a loop and hitting the local-reference limit, because
they are not released until the frame ends. The fix is an explicit local frame per iteration, popped
inside the loop.

**The classic over-correction:** promoting everything to a global reference, so nothing is ever
collected. Both extremes are defects.

## CPython: the GIL and threading

The GIL is the central constraint for any Python extension:

| Rule | Consequence of violating it |
|---|---|
| Hold the GIL to touch Python objects | undefined behaviour, corruption |
| Release the GIL around long native work | otherwise the whole process serialises on your call |
| Re-acquire it before touching Python state again | corruption |
| Attach any thread that calls into Python before doing so | undefined behaviour |

**The two opposite defects:** never releasing the GIL (native work blocks every Python thread), and
releasing it and then touching Python objects before re-acquiring (corruption).

## N-API: scopes and stability

| Property | Detail |
|---|---|
| ABI stability | N-API is designed to be stable across Node versions, unlike raw V8 bindings |
| Handle scopes | values are scoped; leaving a scope frees them — the mechanism that prevents leaks |
| Async work | async work items exist for off-thread work; returning into JS must go through them |
| Thread safety | you may not touch JS values off the main thread without the runtime's mechanism |

**The defect this prevents:** returning into JS from a worker thread directly. The runtime provides the
mechanism (an async work item or an equivalent); using it is not optional.

## cgo: the pointer rules

cgo has rules that are stricter than most developers assume, and they exist because Go's garbage
collector may move or collect memory that C retains.

| Rule | Why |
|---|---|
| Go pointers passed to C must not be retained by C after the call | the Go collector is not aware of C's references |
| C must not store a Go pointer | same reason |
| Structures containing Go pointers are subject to additional rules | avoid them at the boundary |
| Long-running C calls that need to call back into Go need the runtime's mechanism | callbacks must be marshalled |

**The practical consequence:** the safe pattern is to copy data across, or to hold the data in C-owned
memory for the duration. Trading a copy for safety is usually correct here.

## P/Invoke: marshalling as the contract

```csharp
// The attributes ARE the contract: calling convention, string encoding, lifetime
[LibraryImport("native", EntryPoint = "process")]
private static partial int Process(
    [MarshalAs(UnmanagedType.LPUTF8Str)] string input,
    out IntPtr result);
```

| Attribute | What it decides |
|---|---|
| `CallingConvention` | how arguments are passed — the most common source of immediate crashes |
| String marshalling | encoding and lifetime of a string crossing the boundary |
| `[In]`/`[Out]` | whether the runtime copies |
| `StructLayout` | layout of a struct crossing unchanged |

**The default you should not trust:** the runtime's default calling convention may not match the
library's. State it explicitly for every import.

## Shared concerns across all mechanisms

Whatever the mechanism, these four things are always yours:

| Concern | Why the mechanism cannot help |
|---|---|
| **Allocation ownership** | the mechanism does not know which side should free |
| **Error semantics** | it can propagate its own errors, not your convention |
| **Thread affinity** | it exposes the runtime's guard, but the policy is yours |
| **Callback lifetime** | it does not know when you are done with a callback |

## Choosing between mechanisms on one boundary

| Situation | Prefer |
|---|---|
| Node addon, long-lived | N-API (ABI-stable) over raw V8 |
| Python extension, performance-critical | a C extension or PyO3 over ctypes (ctypes is slower and less safe) |
| .NET interop, modern runtime | `LibraryImport` (source-generated) over `DllImport` |
| JVM interop, simple calls | a maintained binding layer over hand-written JNI |
| JVM interop, performance-critical | hand-written JNI, with the reference discipline |
| Go ↔ C, data crossing | copy across, per the pointer rules |
| Rust ↔ C, large API surface | `cbindgen`-generated headers, with panic containment |
| Anything untrusted | a sandboxed runtime rather than a native binding |

## Checklist

- [ ] The mechanism is named, with its version
- [ ] What the mechanism guarantees is stated, and what it leaves to you is stated
- [ ] The runtime's reference/handle model is understood (JNI references, N-API scopes, Python refcounts)
- [ ] The runtime's guard discipline is followed (GIL released around native work, re-acquired before use)
- [ ] Threads are attached to the runtime before touching its state
- [ ] Calling conventions and string encodings are declared explicitly, not defaulted
- [ ] cgo pointer rules are respected, or data is copied across
- [ ] The mechanism's error-propagation helpers are used, not bypassed
- [ ] Anything untrusted is sandboxed rather than natively bound
