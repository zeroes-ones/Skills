# Binding Modes

<!-- STANDARD: 3min -- eager versus lazy binding, and where each belongs -->

## The distinction

Symbol resolution and binding cost money. The question is **when you pay it**.

| Mode | When symbols resolve | Where the cost lands |
|---|---|---|
| **Eager** | at load, before the program runs | startup — one predictable block |
| **Lazy** | at first reference to each function | the first call of each function — spread across runtime |

The mechanism: with lazy binding, a call site goes through a resolution stub on first use; with
eager binding, every symbol is resolved before the loader hands control over.

## What the documentation says

From `dlopen(3)`:

> `RTLD_LAZY` — "Perform lazy binding. Resolve symbols only as the code that references them is
> executed. If the symbol is never referenced, then it is never resolved. (Lazy binding is performed
> only for function references; references to variables are always immediately bound when the shared
> object is loaded.)"

> `RTLD_NOW` — "If this value is specified… all undefined symbols in the shared object are resolved
> before `dlopen()` returns. If this cannot be done, an error is returned."

And from `ld.so(8)`:

> `LD_BIND_NOW` — "If set to a nonempty string, causes the dynamic linker to resolve all symbols at
> program startup instead of deferring function call resolution to the point when they are first
> referenced."

*(Sources: `dlopen(3)` and `ld.so(8)`, Linux man-pages.)*

**The three facts that matter operationally:**

1. **Lazy defers function resolution only.** Variable references bind immediately — so lazy binding
   never makes a whole library's cost disappear.
2. **Lazy never pays for what is never called.** A library loaded for one function out of two hundred
   resolves one symbol, not two hundred.
3. **`RTLD_NOW` makes failure happen at load.** If a symbol is missing, you learn at load time, not
   at the moment a user triggers the code path.

## Choosing

```text
Is startup latency the dominant constraint?
├── Yes → LAZY, so unused paths cost nothing at launch
│         But: accept that first-call jitter is real, and that a missing symbol
│         fails at first use rather than at load
└── No ↓
    Do you need failures to be discoverable before the code runs?
    ├── Yes → EAGER (RTLD_NOW / bind-now at link time)
    │         Cost: every symbol resolved before use, even unused ones
    └── No ↓
        Is the code path launched from a user-visible interaction?
        ├── Yes → prefer EAGER for that library, so the jitter is not in a tap handler
        └── No  → LAZY is the reasonable default
Finally, always:
  ├── Is the library on the cold-start critical path? → measure both; report the delta
  └── Is a missing symbol possible (optional platform API, version skew)?
      ├── Yes → EAGER, so it fails at load with a clear error rather than mid-operation
      └── No  → the choice above stands
```

## Eager at link time, not just at load

Binding mode can be set when the binary is produced, not only when a library is loaded at runtime:

| Mechanism | Effect |
|---|---|
| `-Wl,-z,now` (or the equivalent bind-now flag) | resolve everything at load, for the whole binary |
| `-Wl,-z,lazy` | keep lazy binding as the default |
| `DF_BIND_NOW` dynamic flag | marks the object to be fully bound at load |
| `LD_BIND_NOW=1` (environment) | forces eager binding for a run — useful for diagnosis |

**Security note:** bind-now is also a hardening measure, because a fully-resolved GOT cannot be
redirected by a later symbol interposition. That is a secondary benefit, not the primary reason to
choose it, but it means the two goals often align.

## The failure mode each mode produces

| Mode | Characteristic failure |
|---|---|
| **Lazy** | First-call latency spikes with no startup cost — "the app stutters the first time you open that screen" |
| **Lazy** | A missing symbol surfaces mid-operation, in the worst place |
| **Eager** | Startup cost grows with the total number of unresolved symbols, even for paths never executed |
| **Eager** | A missing symbol prevents the program starting at all — which is the point, but it must be handled |

Both are legitimate; the defect is choosing one *inadvertently*. The default differs by platform and
toolchain, which is exactly why the choice must be recorded rather than assumed.

## Where the cost is visible

| Symptom | Likely mode | What to measure |
|---|---|---|
| Startup time grows when a new library is linked in | eager | total unresolved symbols, and the loader's relocation work |
| Intermittent multi-millisecond delay on the first use of a feature | lazy | first-call timing on the specific path |
| A crash that occurs only on a rarely-used code path | lazy (missing symbol) | `LD_DEBUG=bindings` or the platform equivalent |
| A crash or clean failure at startup after a dependency update | eager (correctly) | the load-time error message |

`LD_DEBUG=statistics,reloc,bindings` (Linux) reports the actual resolution work, which converts this
from an argument into a measurement.

## Interaction with the launch budget

Binding mode is one term in the launch cost, and it interacts with the linkage decision:

```text
Fewer dynamic dependencies  → less to resolve, either mode
Smaller exported surface    → fewer symbols to resolve
Deferred (optional) loads   → nothing to resolve until needed
Eager binding               → all of it, up front, predictably
Lazy binding                → spread into first use
```

So the levers compose: reduce the dependency count and the exported surface first, then choose the
binding mode for the residual cost. Hand the measurement to `app-launch-performance-engineer`.

## Diagnostics

```bash
# What does the loader actually do for this binary?
LD_DEBUG=statistics ./app            # counts of relocation/resolution operations
LD_DEBUG=reloc ./app                 # which relocations are processed
LD_DEBUG=bindings ./app              # which symbols bind where

# Force eager binding to compare startup
LD_BIND_NOW=1 ./app

# Which libraries does this process actually load?
LD_DEBUG=libs ./app 2>&1 | grep 'calling init'
```

Run each on a representative device, several times, and report median rather than best-case.

## Checklist

- [ ] A binding mode is chosen deliberately, per library, and recorded
- [ ] The platform's default binding mode is known (it differs between toolchains)
- [ ] Startup-critical libraries are measured in both modes on a representative device
- [ ] First-call paths that a user can trigger are not paying uncounted resolution cost
- [ ] Lazy binding is not masking a missing symbol that should fail at load
- [ ] Where hardening is a goal, bind-now is considered and its startup cost measured
- [ ] The measurement is recorded with its tool and device (`[VERIFIED]`), not asserted
