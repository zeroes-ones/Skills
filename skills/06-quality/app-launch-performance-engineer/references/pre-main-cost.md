# Pre-Main Cost

<!-- STANDARD: 3min -- loader work, relocations, static initializers and framework init -->

## Why this phase is the one that hides

Phase 1 runs **before the app's own code**. That has three consequences:

1. **The app cannot instrument it from inside the app.** By the time your first line runs, the cost is
   already spent. You need a loader-level trace or ablation.
2. **Its failure mode is not a logic error.** A slow initializer is a delay; a broken one is a rare,
   environment-dependent launch failure.
3. **It scales with what you link, not with what you wrote.** Adding a dependency adds code that runs
   before yours.

## The four components

### 1. Loader work

The loader maps the executable and its dependencies, resolves their relationships and hands control
over. Apple's documentation describes the sequence: the kernel loads the app's code and data, then
loads the dynamic loader, which "then loads the app's dependent libraries. These are the dynamic
libraries the app was linked with." *(Source: Apple, "Overview of Dynamic Libraries".)*

| Driver | Effect |
|---|---|
| Number of dynamic libraries | each adds mapping, resolution and initialisation |
| Library size | more pages to map and (potentially) fault in |
| Search-path complexity | resolution attempts before a hit |
| Preloading | shifts work earlier, does not remove it |

**Lever:** fewer libraries. Merge, or move optional units to on-demand loading. This is the linkage
decision → `library-linkage-architect`.

### 2. Relocations and binding

Every reference that needs an address at runtime is a relocation. Whether they are processed at load
or at first use is the binding-mode decision.

| Mode | Cost lands |
|---|---|
| Eager (`RTLD_NOW`, bind-now at link) | at load — a predictable block in Phase 1 |
| Lazy (`RTLD_LAZY`) | at first call — spread into Phases 2, 3 and later |

**Lever:** choose the binding mode deliberately; measure both. A large Phase 1 with a small total
suggests eager binding doing work you could defer; a small Phase 1 with a poor TTFD suggests lazy
binding moving cost into the user's first interaction.

### 3. Static initializers

Code that runs before `main`: C++ constructors for globals, `__attribute__((constructor))`, Objective-C
`+load`, Swift initializers, `static { }` blocks in JVM languages, module-level side effects.

| Why they are expensive | Why they are dangerous |
|---|---|
| they run unconditionally, whether used or not | cross-unit order is unspecified |
| they often do I/O or allocate | a failure is environment-dependent and rare |
| they cannot be instrumented from app code | they are invisible in the app's own profiler output |

**Lever:** make initialisation explicit and lazy. See `static-initializers.md`.

### 4. Framework and system initialisation

The framework runs its own start-up: runtime setup, system-service connection, theming, and in some
frameworks a substantial amount of one-time work. You control less here, but not nothing.

| Lever | Effect |
|---|---|
| framework version | newer versions often reduce init cost — measure, do not assume |
| framework configuration | options that pre-load or pre-warm cost; options that defer save |
| disabled subsystems | services you do not use should not initialise |
| system-service wait | partly outside control; identify whether it is bounded |

## Measuring Phase 1

### Loader-level trace

| Platform | Mechanism |
|---|---|
| Linux | `LD_DEBUG=statistics,reloc,libs` reports relocation and resolution counts and the libraries loaded |
| Apple | the launch instrument shows pre-main time and the libraries loaded |
| Android | macrobenchmark and the platform's startup tooling separate pre-main from the total |
| Any | an ablation of the library set gives a coarse but reliable number |

### Ablation of the library and initializer set

```text
1. Baseline: cold start, median device, ≥10 runs, median recorded.
2. Remove or defer ONE library or ONE initializer.
3. Re-measure identically.
4. Record the delta.
5. Restore and re-measure the control (guards against device drift).
```

**What ablation reliably finds:** one or two dependencies responsible for the majority of pre-main
cost. It is common for a single SDK to outcost everything else combined, and it is almost never the
one the team expected.

## The third-party problem

Dependencies often initialise themselves, which puts their cost on your critical path without your
deciding it.

| Mechanism | Platform | Consequence |
|---|---|---|
| Content providers declared in the manifest | Android | initialisers run before the app's own `onCreate` |
| Class-level initialisation on first reference | JVM | cost lands at the first touch |
| Module side effects at import | Python/Node | cost lands at import time |
| `+load` / linker-added constructors | Apple | cost lands before `main` |
| Auto-configuration | framework-specific | cost lands at start-up, sometimes for features unused |

**The Android case is documented.** App Startup exists so components "share a single content
provider… This can significantly improve app startup time", and its guidance warns: "If you previously
used content providers to initialize components in your app, make sure that you remove those content
providers when you use App Startup." *(Source: Android, App Startup library.)*

**The general lesson:** an inventory of what *self-initialises* is more useful than an inventory of
what you wrote, because self-initialisation is where the unowned cost lives.

## Fix order within Phase 1

```
1. Remove what is not needed at all           (unused library, unused subsystem)
2. Defer what is needed but not at start     (lazy init, on-demand load)
3. Consolidate what must initialise          (one init path, not N providers)
4. Reduce the linkage cost of what remains    (fewer libraries, deliberate binding mode)
5. Only then micro-optimise the initialiser   (rarely where the money is)
```

Steps 1 and 2 are where the wins are. Step 5 is where teams start, because it is the visible work.

## Checklist

- [ ] Phase 1 is measured with a loader trace or ablation, not inferred
- [ ] The library count and its contribution are known
- [ ] Every static initializer has been inventoried, including its dependencies'
- [ ] Self-initialising dependencies (providers, auto-config, module side effects) are inventoried
- [ ] The binding mode is a deliberate choice, and both modes have been measured
- [ ] Framework init cost is known, and unused subsystems are confirmed disabled
- [ ] Fix order starts with removal and deferral, not micro-optimisation
- [ ] The Phase 1 result is handed to `library-linkage-architect` where it reflects a linkage cost
