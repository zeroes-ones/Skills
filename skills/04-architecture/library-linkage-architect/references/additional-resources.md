# Additional Resources — library-linkage-architect

> Deep knowledge loaded on demand. `SKILL.md` stays lean; extended material lives here and in the
> sibling reference files.

## Reference file map

| File | Covers |
|---|---|
| `linkage-forms.md` | The three axes, the unit-form catalogue, and the four constraints that select a form |
| `static-vs-dynamic.md` | The trade in size, load, memory and update model, with the measurement method and the update-model asymmetry |
| `abi-stability.md` | The breaking-change list, opaque types, reserved space, versioning strategies, and automatic detection |
| `symbol-visibility.md` | Visibility control, export lists, generic-name collisions, and the collision test |
| `binding-modes.md` | Eager versus lazy binding, the documented semantics, and choosing per library |
| `runtime-loading.md` | `dlopen` semantics, the unload reality, version probes, and the four load-failure states |
| `update-model.md` | The five remediation models, the exposure window, blister-radius pairing, and the rehearsal procedure |
| `plugin-abi.md` | C versus C++ versus WASM boundaries, the host capability table, memory ownership, and version negotiation |
| `process-safety.md` | `fork` constraints, static initialisation order, load order, and symbol resolution |
| `platform-constraints.md` | The constraint categories per channel, and how to record their design implications |
| `anti-patterns.md` | Fifteen linkage anti-patterns with detection heuristics and a sweep script |
| `error-decoder.md` | Fourteen symptoms in long form: mechanism, diagnosis, fix, recurrence guard |
| `sub-skills.md` | When to split the session, and the boundary with adjacent skills |

## Extended example

`examples/backtest/README.md` runs a linkage remediation against a stated scenario — a security fix
under static linkage, and a dylib-count launch regression — with the arithmetic shown and every figure
provenance-tagged.

## Source material

Linkage semantics and platform rules change between toolchain, runtime and OS releases. Confirm the
current version before citing a specific clause or behaviour.

| Source | What it governs |
|---|---|
| Apple, "Overview of Dynamic Libraries" (archived developer documentation) | The static-versus-dynamic trade in executable size, launch time and memory footprint |
| `dlopen(3)`, Linux man-pages | `RTLD_LAZY`/`RTLD_NOW` binding, `RTLD_LOCAL`/`RTLD_GLOBAL` scope, `RTLD_NODELETE`, and the unload conditions |
| `ld.so(8)`, Linux man-pages | `LD_BIND_NOW`, library search paths, relocation and symbol-resolution behaviour |
| `fork(2)` and `signal-safety(7)`, Linux man-pages | The async-signal-safe restriction after fork, and inherited pthreads object state |
| CISA Known Exploited Vulnerabilities catalog | The Heartbleed example that motivates the update-model argument |
| GCC wiki, "Visibility"; toolchain documentation per language | Symbol export control and interposition behaviour |
| `ld.so(8)` and platform loader documentation | Soname-based versioning and resolution order |
| webassembly.org use-cases documentation | WASM as a portable, sandboxed boundary for untrusted code |
| Platform distribution and store policy documentation (per channel, current version) | What may be shipped, loaded, signed and updated |

## Verification harness

`scripts/verify-skill.sh` asserts this skill's own invariants: that all six ground rules are present
with enforcement columns, that the three axes are kept separate, that the ABI-breaking-change list and
the unload reality are encoded, that the update model and exposure window are required, that symbol
visibility and collision testing are stated, and that the platform-constraint check is a gate. Run it
before relying on the skill's output.
