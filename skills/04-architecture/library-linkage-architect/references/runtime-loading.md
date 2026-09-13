# Runtime Loading

<!-- STANDARD: 3min -- dlopen semantics, the unload reality, and load-failure design -->

## What runtime loading is for

Runtime loading (`dlopen`, `LoadLibrary`, `dlsym`, `Library.load`) means the program decides at
runtime which code to bring into its address space. Four legitimate reasons, and one illegitimate
one:

| Reason | Legitimate? |
|---|---|
| Ship optional functionality without shipping it to everyone | **Yes** |
| Platform forces it (plugin host, driver, extension point) | **Yes** |
| Language or licence mismatch (load a library written elsewhere) | **Yes** |
| Isolation or capability separation | **Yes** |
| "It's faster" | **No** — measure it, or the claim is unfounded |
| "To avoid a build dependency or break a cycle" | **Usually no** — that hides an architecture defect |

## Load semantics that matter

From `dlopen(3)`, the properties that change how you must design:

| Property | Consequence |
|---|---|
| Loading is **recursive** — dependencies load too | a single load can pull in an unknown number of libraries |
| `RTLD_LAZY` binds function references on first use, variables immediately | mixed binding behaviour within one library |
| `RTLD_NOW` resolves everything before `dlopen` returns, or errors | failures are load-time and explicit |
| `RTLD_LOCAL` (default) does **not** publish symbols to later loads | plugins cannot accidentally resolve each other's symbols |
| `RTLD_GLOBAL` **does** publish them | needed for some interposition, and a collision risk |
| `RTLD_NODELETE` prevents unload and re-initialisation | the escape hatch when unload is unsafe |
| Loading a symbol requires the exact name, including mangling | C++ symbol names are compiler-specific |

*(Source: `dlopen(3)`, Linux man-pages.)*

## The unload reality

**Unload is not a mechanism you can rely on.** The documented conditions:

> the object is unloaded "if the object's reference count drops to zero and no symbols in this object
> are required by other objects… (Symbols in this object might be required in another object because
> this object was opened with the `RTLD_GLOBAL` flag and one of its symbols satisfied a relocation in
> another object.)"

And the escape hatch exists precisely because unload is hazardous:

> `RTLD_NODELETE` — "Do not unload the shared object during `dlclose()`. Consequently, the object's
> static and global variables are not reinitialized if the object is reloaded with `dlopen()` at a
> later time."

*(Source: `dlopen(3)`, Linux man-pages.)*

Three consequences for design:

1. **You cannot assume the library leaves memory.** Anything holding its pointers, registering its
   callbacks, or depending on its thread-local storage keeps it resident.
2. **Reload does not imply re-initialisation.** Global and static state may persist; a "fresh" load
   may not be fresh.
3. **Thread-local storage and destructors complicate unload.** A registered destructor, a TLS block,
   or an atexit handler can prevent clean teardown, and the failure is time-dependent.

**The design that avoids all of it: version the unit and load a new path.**

```text
Instead of:  unload v1 → load v2        (unreliable)
Do:          load v2 alongside v1       (reliable)
             route new work to v2
             keep v1 until nothing uses it, and accept it may stay resident
```

This trades a bounded amount of resident memory for a lifecycle that actually works — and it is why
plugin hosts that support updates usually accept multiple resident versions.

## Failure design

Every runtime load has four failure cases, and each needs a designed state rather than an error:

| Case | What must happen |
|---|---|
| **Absent** | the capability is unavailable; the product degrades or hides it — not a crash |
| **Corrupt or truncated** | the load fails; report it at the right severity and do not retry indefinitely |
| **Wrong version** | detect the mismatch via a version symbol and refuse to use it — do not call optimistically |
| **Loads but misbehaves** | the host's problem; isolate where possible (sidecar), and bound the damage |

**The version-probe pattern** — the cheapest way to prevent calling an incompatible library:

```c
/* The library exports exactly this, plus its API. Check it before anything else. */
int foo_abi_version(void);          /* returns e.g. 3 */

typedef int (*version_fn)(void);
version_fn v = (version_fn)dlsym(handle, "foo_abi_version");
if (!v) { /* too old to even report a version */ return LOAD_INCOMPATIBLE; }
if (v() != FOO_ABI_EXPECTED) { /* incompatible */ return LOAD_INCOMPATIBLE; }
```

Every plugin ABI should have an equivalent. Without it, an incompatible library is discovered by
calling it, which is a crash rather than an error.

## Choosing the binding mode for a load

| Situation | Choose |
|---|---|
| Optional functionality, rarely used | `RTLD_LAZY` — do not resolve what you may not call |
| A missing symbol must be caught early | `RTLD_NOW` — fail at load, not mid-operation |
| A plugin that must not pollute the namespace | `RTLD_LOCAL` (the default — do not switch to global) |
| A library that must not unload | `RTLD_NODELETE` — and accept the memory |
| Testing whether something is already resident | `RTLD_NOLOAD` — probe without loading |

## What must not be loaded at runtime

| Not this | Why |
|---|---|
| Security-critical primitives, fetched at runtime | a load path is an attack surface; the code should ship in the signed binary |
| A library the product cannot function without | that is a link-time dependency, not an optional load |
| Anything fetched from a path a user or attacker can write | that is code execution, not configuration |
| A unit whose absence is unhandled | the failure is a crash on a code path nobody tested |

**The rule:** runtime loading is for *optional capability*. Anything mandatory, security-relevant or
untrusted-in-origin belongs at link time, or behind a sandbox boundary (WASM, sidecar).

## Checklist

- [ ] Every runtime load has a stated reason from the legitimate list
- [ ] The load's recursive dependencies are known, not assumed
- [ ] A version probe exists, and an incompatible unit is refused before any call
- [ ] All four failure cases (absent, corrupt, wrong version, misbehaving) have designed states
- [ ] Binding mode is chosen per load site and recorded
- [ ] Symbol scope stays local; global loading is justified where used
- [ ] The unload requirement is stated; if unload is load-bearing, the risk is recorded (R4)
- [ ] Versioned loads are used instead of unload-and-reload where updates are needed
- [ ] No security-critical or mandatory code is loaded from a runtime-writable path
- [ ] Every load site is exercised in a test, including the absent and wrong-version cases
