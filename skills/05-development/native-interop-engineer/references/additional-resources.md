# Additional Resources — native-interop-engineer

> Deep knowledge loaded on demand. `SKILL.md` stays lean; extended material lives here and in the
> sibling reference files.

## Reference file map

| File | Covers |
|---|---|
| `boundary-justification.md` | When to cross a language boundary, the alternatives, and how to measure the performance claim |
| `binding-mechanisms.md` | JNI, CPython C API, N-API, P/Invoke, cgo, Rust FFI — and what each guarantees versus leaves to you |
| `abi-choice.md` | C versus C++ versus sandboxed ABI, fixed-width types, opaque handles, layout assertions, the extensible-struct pattern |
| `memory-ownership.md` | The ownership matrix, allocator mismatch, lifetimes, arenas, handle staleness, reference counting |
| `marshalling.md` | The four data shapes ranked by cost, the cost model, handles, collections, strings, async data |
| `strings-and-encodings.md` | Encoding, explicit length, the embedded-NUL trap, conversion cost, the deallocator-travels-with-the-type pattern |
| `error-propagation.md` | Result codes, result structs, catching at the boundary, the sentinel trap, un-representable failures |
| `panic-and-exception-containment.md` | The containment wrapper per boundary, the `unsafe` interaction, and process-fatal failures |
| `callbacks-and-reentrancy.md` | The re-entrancy deadlock, guard disciplines, thread attachment, callback lifetime and the seven callback tests |
| `threading-and-affinity.md` | Attachment, affinity and thread-safety as three separate properties, and the guard as a threading rule |
| `performance-at-the-boundary.md` | Per-crossing cost, crossing count, the harness, crossing-count reductions, and the reporting shape |
| `anti-patterns.md` | Sixteen interop anti-patterns with detection heuristics and a sweep script |
| `error-decoder.md` | Fifteen symptoms in long form: mechanism, diagnosis, fix, recurrence guard |
| `sub-skills.md` | When to split the session, and the boundary with adjacent skills |

## Extended example

`examples/backtest/README.md` runs an interop remediation against a stated scenario, with the arithmetic
shown and every figure provenance-tagged.

## Source material

Binding mechanisms and their safety guarantees change between runtime and library versions. Confirm the
current version before relying on a guarantee.

| Source | What it governs |
|---|---|
| JNI specification and the JVM's native interface documentation | Reference kinds, exception check APIs, thread attachment |
| CPython C API and extension documentation | Reference counting, the GIL, thread state and attachment |
| Node N-API / node-addon-api documentation | Handle scopes, async work, threadsafe functions, exception propagation |
| .NET interop documentation (`LibraryImport`/`DllImport`, marshalling attributes) | Calling conventions, string marshalling, struct layout |
| cgo documentation | The pointer-passing rules between Go and C, and their rationale |
| Rust FFI documentation and the `catch_unwind` contract | `extern "C"` unwinding prohibition, panic containment, `#[no_mangle]` |
| Platform ABI documentation (per architecture) | Calling conventions, alignment, and struct layout rules |
| `dlopen(3)` and platform loader documentation | Symbol resolution and the shared-object boundary |
| webassembly.org use-cases documentation | Sandboxed boundaries as an interop alternative |

## Verification harness

`scripts/verify-skill.sh` asserts this skill's own invariants: that all six ground rules are present with
enforcement columns, that ownership requires a named allocator and freer per pointer, that no panic or
exception can cross a foreign frame, that sentinel collisions are refused, that callback threading and
lifetime are stated, that the performance justification must be measured, and that the unsafe-region
review is required. Run it before relying on the skill's output.
