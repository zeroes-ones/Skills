# Static vs Dynamic

<!-- STANDARD: 3min -- the trade in size, load, memory and update model, with the measurement method -->

## The trade, as the platform vendors state it

Apple's developer documentation states it directly rather than leaving it to folklore:

> "Using dynamic libraries instead of static libraries reduces the executable file size of an app.
> They also allow apps to delay loading libraries with special functionality only when they're
> needed instead of at launch time. This feature contributes further to reduced launch times and
> efficient memory use."

And the cost of the other direction:

> "Linking many static libraries into an app produces large app executable files. Applications with
> large executables suffer from slow launch times and large memory footprints."

*(Source: Apple, "Overview of Dynamic Libraries", archived developer documentation.)*

So the trade is **size and load flexibility against something** — and the "something" is not speed.
It is per-consumer simplicity at build time, paid for with an update model at remediation time.

## What each side actually costs

| Dimension | Static | Dynamic |
|---|---|---|
| Executable size | larger — code is copied into each binary | smaller — code exists once |
| Load time | grows with executable size | loader work, but code is shared and can be deferred |
| Resident memory | private copy per process | shared text pages across processes; private data still per-process |
| Build complexity | simpler — one artefact | needs version, path and symbol management |
| Update model | rebuild and re-ship every consumer | patch once, if the version boundary holds |
| ABI risk | none across consumers (no boundary) | a real, permanent obligation |
| Startup predictability | high — everything is present | depends on binding mode and loader work |
| Deployability to minimal targets | excellent — no runtime needed | needs the loader and the library present |

**The two rows that matter most:** *update model* and *ABI risk*. They are the asymmetric ones —
static removes an entire class of runtime failure and adds an entire class of remediation cost.

## The update-model asymmetry, in numbers

This is the argument that should drive most decisions, and it is a security argument rather than a
performance one:

```text
Scenario: a critical vulnerability is published in a dependency.

STATIC linkage path per consumer:
  patch the dependency source              → rebuild dependency
  → rebuild every consumer                 → re-run full test suites
  → re-sign / re-package                   → store review or release train
  → staged rollout                         → measure adoption

DYNAMIC linkage path:
  patch the dependency                     → publish the patched library once
  → users (or the platform) update it      → protected without a consumer rebuild
```

The difference is not a constant; it is the difference between *one* remediation and *N*, and it is
paid on the attacker's schedule rather than yours.

**The worked example that made this concrete:** Heartbleed (CVE-2014-0160) affected OpenSSL. Every
consumer that had statically linked OpenSSL needed to rebuild and re-ship; consumers of a
system-provided shared OpenSSL could be patched once at the platform level. CVE-2014-0160 is listed
in CISA's Known Exploited Vulnerabilities catalog (OpenSSL, added 2022-05-04), so the scenario is
not hypothetical. *(Sources: Heartbleed disclosure; CISA KEV catalog.)*

## How to measure the launch side

Do not argue about launch cost from theory. Measure it on the target, and record the method.

```text
For each candidate form, on a representative device and build:

1. Cold start, repeated (process killed between runs)
     → median and p90, not the best run
2. Warm start
3. Binary size (and container/package size if shipped in one)
4. Resident memory after first interaction settles
5. Time spent in the loader, if the platform exposes it
```

Platform-specific notes:

- **iOS/macOS:** the dynamic loader (`dyld`) resolves the dependent libraries before `main` runs;
  instrument with the platform's launch profiler rather than guessing from dylib count.
- **Android:** use the platform's startup measurement (see `app-launch-performance-engineer`), which
  separates time-to-initial-display from time-to-full-display.
- **Linux:** `LD_DEBUG=statistics,reloc` reports relocation and resolution work for a given binary —
  a direct measurement of the dynamic-load cost that static linkage avoids.
- **Any platform:** measuring "a big binary" and "a small binary" is not the same as measuring the
  *same functionality* in both forms. Build both, or the comparison is meaningless.

Report every number with `[VERIFIED]` (measured, tool and device named), `[COMPUTED]` (derived,
formula shown) or `[ESTIMATED]` (assumption written down).

## When static is clearly right

| Situation | Why |
|---|---|
| Minimal container, rescue tool, initramfs | no shared runtime guaranteed on the target |
| Firmware, bootloader, early boot | the library must exist before any loader does |
| Single consumer in lockstep | the ABI obligation buys nothing |
| Hard real-time path where a load failure is unacceptable | everything present and resolved up front |
| A dependency with no security surface | the update-model cost is unrealised |
| Distribution that forbids extra binaries | one self-contained artefact is the only permitted form |

## When dynamic is clearly right

| Situation | Why |
|---|---|
| A security-critical dependency shipped to many consumers | remediation once, not N times |
| Multiple independent consumers | a shared copy, and a stable boundary they can both use |
| Optional functionality that most users never touch | delay the load until needed |
| Plugin/extension boundaries | the whole point is runtime replaceability |
| Platform-provided system libraries with a patch channel | the OS owns remediation |

## The hybrid, done deliberately

Shipping both forms is legitimate — and it is the common answer for a library with mixed consumers.

```
Static build      → for consumers that want a self-contained artefact
Dynamic build     → for consumers that want patchability and share code
```

Three rules that make it honest:

1. **Both forms are built and tested in the pipeline.** An untested second form is a liability that
   fails the day it is needed.
2. **The ABI policy applies to the dynamic form only**, and is documented as such.
3. **The update models differ, and that is stated.** A static consumer still rebuilds for a fix;
   do not let the existence of a dynamic build imply otherwise.

## The decision worksheet

| Question | Static | Dynamic |
|---|---|---|
| How many independently-released consumers? | one | many |
| How must a security fix reach users? | accepts a rebuild | must not require a rebuild |
| What is the launch/memory budget? | size is affordable | size must stay small |
| Must functionality be optional or deferred? | no | yes |
| Does the target have a shared runtime? | no | yes |
| Is there a plugin/extension requirement? | no | yes |
| Is the channel restrictive? | bundled single artefact | permits bundled libraries |

If the answers split, the honest output is *both forms*, with the update models stated separately —
not a preference dressed as a decision.
