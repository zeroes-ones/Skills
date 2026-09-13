# Plugin ABI

<!-- STANDARD: 3min -- ABI shape for extension points, across-compiler hazards, WASM as a boundary -->

## What makes a plugin ABI harder than a library ABI

A library ABI is between *you* and *you* — the same toolchain, the same release process. A plugin ABI
is between you and **third parties using unknown toolchains**, on unknown platforms, on their own
release schedule. That difference drives everything below.

| Dimension | Library ABI | Plugin ABI |
|---|---|---|
| Who builds the consumer | you | third parties, unknown compilers |
| Toolchain agreement | assumed | must be designed away |
| Version skew | controlled by you | guaranteed to happen |
| Failure containment | in-process crash | must be bounded, ideally sandboxed |
| Lifecycle | load | load, version-negotiate, use, maybe replace |

The full extension-platform design belongs to `plugin-ecosystem-architect`. **This file owns the ABI
shape** — the contract itself.

## The ABI options

| Option | Portability | Isolation | Cost |
|---|---|---|---|
| **C ABI** (opaque handles + function pointers) | high | none | lowest marshalling; no language features cross |
| **C++ ABI** | **low** | none | fails across compilers or versions |
| **COM-like interface table** | high | none | a vtable of function pointers plus a query mechanism |
| **WASM** | high | **strong** | marshalling; different toolchain; capability model |
| **Sidecar process** | high | **strong** | IPC; serialisation; process management |
| **Scripting host** (embedded interpreter) | high | partial | a runtime in-process; language-specific |

**The default for a native plugin boundary is the C ABI.** It is the only thing every toolchain on
every platform agrees on.

## Why the C++ ABI fails

Passing C++ types across a plugin boundary fails on four independent things, any one of which breaks
at the next compiler upgrade:

| Hazard | Why it breaks |
|---|---|
| **Name mangling** | the scheme is not standardised; the same signature mangles differently |
| **Standard-library layout** | `std::string`, `std::vector`, `std::map` sizes and internal layouts differ between implementations and versions |
| **Exception ABI** | throwing across a boundary built with a different exception model is undefined |
| **Vtable layout** | base-class layout and RTTI structures are implementation-defined |
| **Allocator ownership** | memory allocated in one module and freed in another with a different allocator |

**The rule:** if the boundary must be portable, only C types cross it. Opaque pointers, integer and
float primitives, C strings you own explicitly, and function pointers. Everything else stays inside.

**The exception:** if every participant is guaranteed to use the *same* toolchain version and you
control all of them, a C++ boundary is workable. That is a private-plugin situation, not a public
one — state which you have.

## The minimum viable plugin ABI

```c
/* ── Version first. Nothing is called before this. ───────────────────── */
int         plugin_abi_version(void);          /* returns the ABI revision */

/* ── Identity, for diagnostics and conflict detection ───────────────── */
const char *plugin_name(void);
const char *plugin_version(void);

/* ── Lifecycle. Explicit, not implicit in static initializers ────────── */
int  plugin_init(const plugin_host_api *host);   /* 0 = ok */
void plugin_shutdown(void);

/* ── The actual capability, via opaque handles ──────────────────────── */
```

Four properties worth noting:

1. **Version is the first call**, so an incompatible plugin is refused before anything else runs.
2. **Identity is exposed**, so a collision or a stale plugin is diagnosable.
3. **Lifecycle is explicit**, so initialisation is not hidden in a static constructor — which is both
   a load-order hazard and unobservable failure.
4. **Opaque handles only**, so the plugin's internal layout can change without an ABI break.

## The host API, passed in rather than linked

A plugin should receive the host's services as a **function table**, not link against the host.

```c
typedef struct {
    int   abi_version;
    void *(*alloc)(size_t);
    void  (*free)(void *);
    int   (*log)(int level, const char *msg);
    /* ...capabilities, each added by extending the table with a version bump... */
} plugin_host_api;
```

Why this beats linking against the host:

| Benefit | Reason |
|---|---|
| No host symbols to resolve | the plugin has no undefined host symbols, so no collision and no load order |
| Capability is explicit | the plugin can only do what the table offers — a capability boundary |
| The table can be extended | append fields and bump the version; old plugins ignore the tail |
| Memory ownership is clear | allocation and deallocation go through the host's allocator |

**The allocator point is not theoretical:** memory allocated by one module and freed by another with
a different allocator corrupts the heap. Routing allocation through the host's table removes the
class.

## Memory ownership across the boundary

State it explicitly, in the ABI documentation, for every pointer that crosses:

| Direction | Who allocates | Who frees |
|---|---|---|
| Host passes a buffer to the plugin | host | host (plugin must not free it) |
| Plugin returns a buffer to the host | plugin, or via the host's allocator | whichever the ABI says — and it must say |
| Handle returned by the plugin | plugin | the plugin, via its own release function |
| String returned by the plugin | plugin's static or plugin-allocated | documented; never freed by the host unless the ABI permits it |

The defect this prevents: an `A`-allocated pointer freed by `B` with a different allocator. It works
in testing and corrupts in production, because the allocators happen to be compatible in one build.

## Version negotiation

```text
1. Host loads the plugin.
2. Host calls plugin_abi_version() FIRST.
   ├── Symbol missing      → too old; refuse with a clear message
   ├── Older than expected → is it within the supported range? yes → proceed; no → refuse
   └── Newer than the host → refuse; the host cannot know the new contract
3. Host passes its own host_api table, including the host's ABI version.
4. Plugin checks the host's version and refuses if it needs a newer host.
5. Only now does the plugin initialise.
```

Both directions must check. A host that never asks, and a plugin that never verifies, means
incompatibility is discovered by calling something.

## WASM as a plugin boundary

Choose WASM when the plugins are **untrusted** or must be **provably isolated** — the documented use
cases include "server-side compute of untrusted code" and "portable and secure" distribution
*(Source: webassembly.org use-cases)*.

| Advantage | Cost |
|---|---|
| Strong isolation — no ambient host access | everything crosses an explicit, marshalled boundary |
| Portable across platforms and toolchains | a different toolchain and build pipeline |
| Deterministic capability model (imports only) | host functions must be designed intentionally |
| No native ABI problem at all | less library availability; some workloads unsuited |

**The decision rule:** native C ABI for trusted, performance-critical plugins; WASM when plugins are
untrusted or the sandbox is the requirement. State the trade rather than presenting one as the
default.

## The plugin ABI checklist

- [ ] The boundary uses a compiler-portable ABI (C, COM-like, or WASM) — not a C++ ABI
- [ ] `plugin_abi_version()` is called first, before any other symbol (R3)
- [ ] The host's capability table is passed in, not linked against
- [ ] Memory ownership is documented for every pointer crossing the boundary
- [ ] Allocation routes through the host's allocator where the plugin allocates for the host
- [ ] Both host and plugin verify the other's version
- [ ] Lifecycle is explicit functions, not static initialisation
- [ ] Handles are opaque; no internal layout crosses
- [ ] An incompatible plugin fails with a clear, versioned message, not a crash
- [ ] The load requirement (and any unload requirement) is stated (R4)
