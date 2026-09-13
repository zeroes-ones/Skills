# Additional Resources — access-modifiers

> Deep knowledge loaded on demand. `SKILL.md` stays lean; extended material lives here and in the
> sibling reference files.

## Reference file map

| File | Covers |
|---|---|
| `the-ladder.md` | The six visibility levels, language-neutral, and the visibility/extension split |
| `language-models.md` | The nine-language comparison, the eight traps ranked by severity, and the porting table |
| `swift.md` | `open` vs `public`, the guiding principle, `package`, `fileprivate`, `internal(set)`, `@testable` |
| `kotlin.md` | `internal`'s module scope and Java permeability, `private set`, `open`/`final`, KMP |
| `java.md` | package-private, `protected`'s real scope, JPMS `exports` as an explicit surface, `final`/`sealed` |
| `csharp.md` | The six levels, `protected internal` vs `private protected` as set operations, `file`, `InternalsVisibleTo` |
| `rust.md` | Private-by-default, `pub(crate)`/`pub(super)`, sealed traits, `pub use` as a curated surface |
| `go.md` | Capitalisation export, `internal/`, unexported fields with constructors, unexported interfaces |
| `python.md` | The underscore convention, name mangling's real purpose, `__all__`, `@property` |
| `typescript.md` | `private`'s erasure, `#field`, structural typing and the exported-type surface |
| `dart-and-mobile.md` | Dart's library-scoped `_`, the analyzer hints, and the mobile cross-platform map |
| `api-surface.md` | Designing the surface as an explicit contract; the five surface layers; deprecation sequencing |
| `test-visibility.md` | Every ecosystem's test mechanism, and why `public` is the wrong answer |
| `anti-patterns.md` | Fifteen visibility anti-patterns with detection heuristics and a sweep script |
| `error-decoder.md` | Fifteen symptoms in long form: mechanism, diagnosis, fix, recurrence guard |
| `sub-skills.md` | When to split the session, and the boundary with adjacent skills |

## Extended example

`examples/backtest/README.md` runs a visibility remediation against a stated scenario, with the
arithmetic shown and every figure provenance-tagged.

## Source material

Access rules, interop boundaries and module systems change between compiler versions. Confirm a
specific rule against the installed toolchain's documentation before relying on it.

| Source | What it governs |
|---|---|
| *The Swift Programming Language*, "Access Control" | The six levels; `open` grants cross-module subclassing and `public` does not; the guiding principle; `@testable` |
| Kotlin documentation, "Visibility modifiers" | The four modifiers; `public` default; `internal` is module-scoped; `private set`; `protected` unavailable at top level |
| Oracle Java Tutorials, "Controlling Access to Members of a Class" | The two top-level and four member levels; package-private is the default; the "most restrictive" recommendation; "avoid public fields except for constants" |
| Microsoft Learn, C# access modifiers and Framework Design Guidelines | The six levels including `protected internal` and `private protected`; the `file` modifier; `InternalsVisibleTo`; the Do/Consider/Avoid/Do-not posture |
| *The Rust Reference*, "Visibility and privacy" | Private by default; `pub(crate)`, `pub(self)`, `pub(super)`, `pub(in path)`; the two privacy rules |
| *The Go Programming Language Specification*, "Exported identifiers" | The capitalisation rule and that all other identifiers are unexported |
| *The Python Tutorial*, "Private Variables" | That private instance variables do not exist; the underscore convention; name mangling's purpose |
| TypeScript Handbook, "Member Visibility" | `public` default; `private`/`protected` are compile-time; `#field` is runtime-enforced; `protected` may be widened by a subclass |
| Dart language documentation | Library-scoped `_` privacy; the `meta` analyzer annotations |

## Verification harness

`scripts/verify-skill.sh` asserts this skill's own invariants: that all six ground rules are present
with enforcement columns, that the restraint ladder and the per-language defaults are encoded, that the
two security traps (TypeScript erasure, Kotlin Java-permeability) are flagged, that test visibility uses
a dedicated mechanism rather than `public`, and that subclassability is treated as a separate decision
from visibility. Run it before relying on the skill's output.
