# Symbol Visibility

<!-- STANDARD: 3min -- visibility control, explicit export lists, and collision testing -->

## The problem in one sentence

By default, most toolchains export **everything**, so the boundary you intended does not exist —
which means anything can collide, and anything can become load-bearing for a consumer by accident.

This is R5, and it is the cheapest rule in this skill to apply and the most expensive to skip.

## Why broad export hurts

| Consequence | Mechanism |
|---|---|
| **Collision** | two libraries export the same name; the loader binds one, and the other's callers get it |
| **Interposition** | another library's symbol silently overrides yours, or yours overrides theirs |
| **Frozen surface** | an internal symbol becomes used by a consumer, so removing it breaks someone |
| **Larger symbol table** | the dynamic symbol table grows, with a small load-time cost |
| **Weaker optimisation** | exported functions cannot be inlined or elided as freely |

**Collision is the serious one**, because the failure mode is a *wrong-function call*, not an error.
The program runs, and does the wrong thing.

## The mechanism

Default to hidden; export explicitly.

```c
/* Compile with hidden visibility by default, and export explicitly. */
/* GCC/Clang:   -fvisibility=hidden                                    */
/* MSVC:        /LD with an explicit .def, or __declspec(dllexport)    */

/* Define API_EXPORT once, per platform, as dllexport (Windows)
   or __attribute__((visibility("default"))) (GCC/Clang). */

API_EXPORT int  foo_open(const char *path);   /* exported */
API_EXPORT void foo_close(int handle);        /* exported */

int foo_internal_helper(void);                /* NOT exported — hidden */
```

The result: the exported set is exactly the list of `API_EXPORT` declarations, which is a thing you
can audit, diff and test.

**Language specifics, same principle:**

| Ecosystem | Mechanism |
|---|---|
| C/C++ | `-fvisibility=hidden` plus explicit visibility attributes; a version script or `.def` file |
| Rust | `#[no_mangle] pub extern "C"` with `cdylib`; only `pub` items with the right attributes are exported |
| Go | `//export` directives in `cgo`; `buildmode=c-shared` exports only annotated functions |
| C# | explicit `public` on the assembly's API surface; `InternalsVisibleTo` for tests only |
| Swift | `@_cdecl` for C entry points; other symbols are not exported by default |
| Java/JNI | `JNIEXPORT` on the entry points; everything else stays local |

## The export list is the contract

The single most valuable artefact this skill produces is a **file listing the exported symbols**,
committed and diffed:

```text
# exported-symbols.txt — the public ABI surface. Diffed per release.
foo_open
foo_close
foo_version
foo_last_error
```

Three uses:

1. **It is the contract.** Anything not in it is private, and privateness is enforceable.
2. **It detects removal.** A symbol disappearing from the list is a breaking change, caught in the
   pipeline rather than by a consumer.
3. **It detects accidental addition.** A new symbol appearing means someone exported something
   without deciding to — which is how a private helper becomes a frozen public surface.

## Generic names, and how they collide

The highest-risk exports are the short, generic, `extern "C"` names — precisely because other
libraries like them too.

| Name | Risk |
|---|---|
| `init`, `open`, `close`, `read`, `write` | extremely high — collide with libc, other libraries, other plugins |
| `create`, `destroy`, `get`, `set`, `put` | high — generic verbs |
| `error`, `version`, `config` | high — common nouns |
| `foo_open`, `foo_close` (prefixed) | low — namespacing solves it |
| C++ names | medium — mangled, so less likely to collide, but not portable across toolchains |

**The rule: prefix every exported symbol with the library's name.** It costs nothing and removes an
entire failure class. For a plugin boundary, prefix with the host and the plugin's identity.

## Testing for collisions

A collision test loads the **real co-load set** — the libraries that actually end up in one process
together — and fails on a duplicate exported symbol.

```python
# Shape of the test: collect exported symbols from every library in the host's load set,
# and fail if any name is exported by more than one.
import subprocess, collections, glob

def exported(path):
    out = subprocess.run(["nm", "-D", "--defined-only", path],
                         capture_output=True, text=True).stdout
    return {line.split()[-1] for line in out.splitlines() if line.split()}

seen = collections.defaultdict(list)
for lib in glob.glob("dist/native/**/*.so", recursive=True) + glob.glob("system-libs/*.so"):
    for sym in exported(lib):
        seen[sym].append(lib)

clashes = {s: libs for s, libs in seen.items() if len(libs) > 1}
for sym, libs in sorted(clashes.items()):
    print(f"COLLISION: {sym} exported by {libs}")
raise SystemExit(1 if clashes else 0)
```

**What to include in the co-load set:** your own libraries, every system library the process links,
and every vendored or bundled library. Use `LD_DEBUG=libs` (Linux) or the platform's equivalent to
discover what actually loads, rather than guessing from the build graph.

**Why a real test beats review:** collisions are invisible in source, invisible in the build log, and
invisible at load. They become visible when the wrong function runs.

## Namespacing beyond visibility

Three further techniques when visibility alone is not enough:

| Technique | Use |
|---|---|
| **Symbol versioning** | one library exports multiple versions; the loader picks per consumer |
| **Linker namespaces** | partition libraries so their symbols cannot see one another (available on some platforms) |
| **`RTLD_LOCAL`** | load a library without publishing its symbols to later loads — the default in most implementations |
| **Process isolation** | a sidecar process removes the shared-namespace problem entirely |

`RTLD_LOCAL` deserves a note: `dlopen` documentation states that with this flag (the default),
"Symbols defined in this shared object are not made available to resolve references in subsequently
loaded shared objects." That is the correct default for plugins — and it means one plugin cannot
accidentally satisfy another's unresolved symbol.

## The visibility checklist

- [ ] Hidden visibility is the default at compile time
- [ ] Every exported symbol is declared explicitly, with a documented mechanism
- [ ] The exported set is written to a committed, diffed file
- [ ] Every exported symbol is prefixed with the library or host name
- [ ] A collision test loads the real co-load set and fails on a duplicate
- [ ] Nothing is exported that a consumer has not been told about
- [ ] Internal helpers cannot become load-bearing by accident
- [ ] Plugins load with local (non-publishing) symbol scope
- [ ] The export list is reviewed on every release, not only when something breaks
