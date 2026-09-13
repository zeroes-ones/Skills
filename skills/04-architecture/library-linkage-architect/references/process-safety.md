# Process Safety

<!-- STANDARD: 3min -- fork constraints, load order, and initialisation ordering -->

## Why this belongs in a linkage skill

Loading decisions determine when code runs, and **when code runs is a safety property**. Two classic
categories of production failure live exactly at this boundary: work done at the wrong time relative
to `fork()`, and initialisation that runs in an order nobody controls.

## `fork()` and loaded code

The documented constraint is stark — from `fork(2)`:

> "After a `fork()` in a multithreaded program, the child can safely call only async-signal-safe
> functions (see `signal-safety(7)`) until such time as it calls `execve(2)`."

and:

> "The child process is created with a single thread — the one that called `fork()`. The entire
> virtual address space of the parent is replicated in the child, including the states of mutexes,
> condition variables, and other pthreads objects."

*(Source: `fork(2)`, Linux man-pages.)*

### What that means in practice

| Situation | Result |
|---|---|
| A library loaded before `fork()` holds a lock at fork time | the child inherits the *held* lock with no thread to release it → deadlock |
| The child calls anything non-async-signal-safe before `exec` | undefined behaviour; commonly a hang in `malloc` or a TLS access |
| A library registered an `atexit`/destructor and the child exits early | destructors run in a process that never initialised them properly |
| A library spawned a background thread before `fork()` | the child has no such thread, but state says otherwise |

**The classic case:** a library initialises a memory allocator or a logging subsystem, which takes an
internal lock, and the process forks while that lock is held. In the parent it is fine. In the child
it is a deadlock that appears under load and never in testing.

### The rule

**Do no work before `fork()` that you do not have to.** Then, if the process forks, only
async-signal-safe calls in the child until `exec`.

Two practical measures:

| Measure | Detail |
|---|---|
| Fork before initialising libraries | start the child early, exec quickly; do not load the world first |
| Use `pthread_atfork` handlers where unavoidable | they exist precisely to reset or re-acquire locks around fork — but they are a workaround, not a design |

**The design question this creates for linkage:** a library that *must* be loaded before a fork (for
example, one the parent needs) is a library whose initialisation must be fork-safe. That is a
constraint on the library choice, not just on the call site.

## Initialisation order

Static initialisers run in an order the language does not fully specify. Every language has a version
of this problem.

| Mechanism | The problem |
|---|---|
| **C++ static objects across translation units** | order between TUs is unspecified; one may read another before it exists |
| **Objective-C / Swift `+load`** | runs before `main`, in an order that depends on link order and dyld behaviour |
| **Java/Kotlin static initialisers** | run on class load, in an order driven by the first reference |
| **Go package `init()`** | ordered by import graph, not by intent |
| **Rust** | no static constructors by design; `lazy_static`/`OnceCell` make initialisation explicit — which is why this class of bug is rarer there |
| **Attribute-based registration** (language-specific) | order depends on the linker, and can change when the link order changes |

### The failure shape

A static initialiser touches something that does not exist yet:

```
static Logger logger{"/var/log/app.log"};     // runs before main
// ... later, the filesystem or the environment is not ready
// → works on the developer's machine, fails in 0.1% of launches
```

The low reproduction rate is the point: it is an order-dependent race, not a logic error.

### The fixes

| Fix | Detail |
|---|---|
| **Make initialisation explicit** | a `init()`/`main()`-time call, not a constructor; the runtime cannot control what you do not defer |
| **Avoid global mutable state** | the state is the hazard, not the mechanism |
| **Use lazy, once-guarded access** | initialise at first use, where the environment is known good |
| **Order within a TU is defined; use it deliberately** | and do not rely on cross-TU order at all |
| **Test with a shuffled or restricted environment** | launch with a minimal environment to expose the dependency |
| **Make each initialiser independently valid** | an initialiser that assumes another ran is the defect |

## Load order and symbol resolution

The loader's resolution order decides which definition wins. That is a safety property too.

| Factor | Effect |
|---|---|
| Load order | first-loaded definition can win for subsequent lookups |
| `RTLD_GLOBAL` | makes a library's symbols available to later loads — and therefore able to satisfy them |
| Symbol visibility | hidden symbols cannot participate in resolution at all |
| `LD_LIBRARY_PATH` / search paths | change which version is found |
| `rpath`/`runpath` | pin search paths into the binary itself, removing environment dependence |
| Preloading | shifts the whole resolution order |

**The predictable practice:** set `rpath` to a known location rather than depending on the
environment, keep symbols local, and test the real co-load set (see `symbol-visibility.md`).

## A pre-launch safety checklist

Things that must be true before the process does anything meaningful:

- [ ] No work before `fork()` beyond what is required to set up the exec
- [ ] Any library loaded pre-fork has fork-safe initialisation, or `pthread_atfork` handling
- [ ] Only async-signal-safe calls in a forked child before `exec`
- [ ] No static initialiser depends on another static initialiser across units
- [ ] No static initialiser touches the filesystem, network or environment it does not own
- [ ] Initialisation that could fail is explicit and its failure is handled
- [ ] Load order is pinned (`rpath`), not dependent on the environment
- [ ] Symbol scope is local by default, so one library cannot satisfy another's undefined symbols
- [ ] The real co-load set is tested for symbol collisions
- [ ] A minimal-environment launch is part of the test plan

## Why this is a linkage concern, not just a coding concern

Each item above is decided by *what you load and when*, which is the linkage decision:

| Linkage choice | Safety consequence |
|---|---|
| Static linkage | initialisers are in your binary, so you control when they run — and you carry them |
| Dynamic linkage | initialisers run at load, before `main`, in the loader's order |
| Runtime loading | you choose the moment — which is an opportunity, and a responsibility |
| A library loaded for one function | you still pay its initialisers |
| Fewer libraries | fewer initialisers, fewer order hazards, less to go wrong before `main` |

The last row is the practical headline: **every library you link is code that runs before your code
does.** Reducing the count is a safety measure as well as a launch-cost measure.
