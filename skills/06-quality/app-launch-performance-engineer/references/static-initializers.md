# Static Initializers

<!-- STANDARD: 3min -- how they hide, why they cannot be instrumented, and how to remove them -->

## What counts

Anything that runs before the app's own entry point, or at first reference, without an explicit call
in the app's code:

| Mechanism | Language/platform | When it runs |
|---|---|---|
| Global object constructors | C++ | before `main`, cross-unit order unspecified |
| `__attribute__((constructor))` | C/C++ (GCC/Clang) | before `main` |
| `+load` | Objective-C | before `main` |
| Swift type initialisers / attributed entry points | Swift | before or at first use, per mechanism |
| `static { ... }` blocks | Java/Kotlin | at class load, on first reference |
| Module-level side effects | Python, Node, Ruby | at import |
| `init()` functions across a package | Go | in import-graph order |
| Auto-configuration / auto-registration | framework-specific | at start-up |

## Why they are the highest-value thing to find

| Property | Consequence |
|---|---|
| They run unconditionally | a feature nobody uses still pays at launch |
| They run before app code | the app's own instrumentation cannot see them |
| Their order is unspecified across units | a dependency between two initializers is a latent, rare failure |
| They often perform I/O | a filesystem, network or environment dependency is a launch-time hazard |
| They are invisible in review | they look like ordinary declarations |

**The economics:** a single static initializer that takes 80 ms is 80 ms on every launch for every
user, forever, and it is usually removable in minutes once found. That ratio is why this is the list
to build first.

## Finding them

### Source-level scan

```bash
SRC="${1:-src}"

echo "== C/C++ global objects with constructors =="
grep -rnE '^(static\s+)?[A-Z][A-Za-z_0-9]*\s+[a-z_][A-Za-z_0-9]*\s*[({]' "$SRC" 2>/dev/null | head

echo "== constructor attributes =="
grep -rnE '__attribute__\s*\(\s*\(\s*constructor' "$SRC" 2>/dev/null | head

echo "== Objective-C +load =="
grep -rnE '^\s*\+\s*\(void\)\s*load' "$SRC" 2>/dev/null | head

echo "== Java/Kotlin static blocks =="
grep -rnE '^\s*static\s*\{|^\s*companion object\s*\{' "$SRC" 2>/dev/null | head

echo "== module-level side effects (Python) =="
grep -rnE '^[a-z_]+\(|^[A-Z_]+\(|^register\(|^setup\(' "$SRC" 2>/dev/null | head
```

A source scan gives candidates. It cannot tell you which ones are *expensive*.

### Binary-level enumeration (more reliable)

```bash
# Which libraries does the process actually load?
LD_DEBUG=libs ./app 2>&1 | grep 'calling init'

# Count them — each one may carry initializers
LD_DEBUG=libs ./app 2>&1 | grep -c 'calling init'
```

Some toolchains or linkers can also emit the initializer list; where that is available it is more
complete than a source scan, because it includes what dependencies added.

### The I/O smell

The dangerous initializers are the ones doing work:

```bash
# Global objects whose constructor arguments suggest I/O or environment access
grep -rnE '^\s*(static\s+)?\w+\s+\w+\s*\(\s*"(/|\./|~)' "$SRC" 2>/dev/null
grep -rnE 'getenv|fopen|open\(|connect\(|readFile|readFileSync|fs\.' "$SRC" 2>/dev/null \
  | grep -vE 'function|def |//' | head
```

An initializer that opens a file, reads an environment variable, or touches the network is a
launch-time hazard *and* a launch-cost item.

## Removing them

### Convert to explicit and lazy

```cpp
// ❌ Runs before main; cost and order are not yours
static Logger g_logger{"/var/log/app.log"};

// ✅ Explicit, at a point where the environment is known good
Logger& logger() {
    static Logger instance{default_log_path()};   // initialised once, at first use
    return instance;
}
```

The two properties that fix it: **explicit** (the app decides when) and **lazy** (only if used).

### Consolidate N into one

Where several dependencies each initialise themselves, consolidate them into a single ordered
initialisation point the app controls. Android's App Startup library exists for exactly this pattern —
one content provider instead of several — and its documentation requires removing the providers it
replaces. *(Source: Android, App Startup library.)*

### Defer past the first frame

An initializer that must happen but need not happen before the first frame should be scheduled after
TTID. Moving work from Phase 1 to Phase 3 is a real improvement *if* it does not lengthen Phase 3
past the budget — measure both.

### Remove the dependency instead

The cheapest initializer is the one you do not link. Before optimising an initializer, ask whether the
dependency is needed at all at start-up.

## Ordering hazards

Cross-unit initialisation order is unspecified. The defects this causes:

| Pattern | Failure |
|---|---|
| Initializer A uses an object defined in initializer B | whichever runs first sees an uninitialised value |
| A initializer registers a callback the framework runs before it is ready | callback fires against partial state |
| An initializer reads a config written by another initializer | race, resolved by luck |
| An initializer touches the filesystem before the container is mounted | rare, environment-dependent failure |

**The fix is structural:** no initializer may depend on another initializer having run. Make each
independently valid, or make the ordering explicit in a single initialisation function that the app
calls.

## Verifying the removal

```text
1. Baseline cold start (median device, ≥10 runs, median recorded).
2. Remove or defer the initializer.
3. Re-measure with the identical method.
4. Confirm the delta is outside the noise (increase runs if not).
5. Confirm no functionality was lost — the initializer still runs, just later.
6. Confirm the later phase did not absorb more than was saved.
7. Check the environment-dependence is gone (launch with a minimal environment).
```

Step 6 is the one skipped: moving 200 ms from Phase 1 to Phase 3 is not an improvement if TTFD grows
by 200 ms or more.

## Checklist

- [ ] Every static initializer is inventoried, including those added by dependencies
- [ ] Each one's cost is measured by ablation, not estimated from its source
- [ ] Initializers doing I/O or reading the environment are treated as hazards, not just costs
- [ ] Initialisation is explicit and lazy where possible
- [ ] Multiple self-initialising components are consolidated into one ordered path
- [ ] Deferred work is scheduled after the first frame, and both phases are re-measured
- [ ] No initializer depends on another having run
- [ ] Removals are verified to have moved cost out of the total, not into Phase 3
- [ ] A minimal-environment launch is part of the test plan
