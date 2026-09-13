# Sub-Skills

<!-- QUICK: 30s -- when to split into a narrower session -->

| Sub-skill | When to use it | Where it lives |
|---|---|---|
| `ladder` | Which of the six levels a declaration needs | `references/the-ladder.md` — Decision Tree 1 |
| `language-model` | A specific language's levels, defaults and traps | `references/language-models.md` |
| `swift` | `open` vs `public`, `package`, `internal(set)`, `@testable` | `references/swift.md` |
| `kotlin` | `internal` module semantics, Java permeability, `private set` | `references/kotlin.md` |
| `java` | package-private, `protected`'s real scope, JPMS `exports` | `references/java.md` |
| `csharp` | the six levels and the two two-word modifiers | `references/csharp.md` |
| `rust` | private-by-default, `pub(crate)`, sealed traits | `references/rust.md` |
| `go` | capitalisation export and `internal/` | `references/go.md` |
| `python` | the convention, mangling, `__all__` | `references/python.md` |
| `typescript` | `private` vs `#field`, erased enforcement | `references/typescript.md` |
| `dart` | library-scoped `_`, and the mobile mapping | `references/dart-and-mobile.md` |
| `api-surface` | Designing the surface as an explicit contract | `references/api-surface.md` — R2 |
| `test-visibility` | Reaching internals from tests, per ecosystem | `references/test-visibility.md` — R5 |

## Split when

- **One language is the question.** "How do I express package-internal in Dart?" is a lookup, not a design session.
- **The API surface is being designed** — `api-surface`, and it is bounded.
- **A test cannot reach a declaration** — `test-visibility` alone.
- **A port is being made** — `language-models` plus the two languages' files.
- **A sensitive value needs protection** — the language file plus R4; escalate if it is a security boundary.

## Stay whole when

- **A library's visibility is being established from scratch.** The ladder, the surface list, the extension decisions and the test story are one design; splitting them produces a surface with no contract, or a test story that widened it.
- **A codebase is being de-exposed.** Consumer analysis, narrowing, the surface list and the deprecation path are one piece of work.

## Adjacent skills, and the boundary

| Neighbour | They own | This skill owns |
|---|---|---|
| `codebase-design` | module decomposition, seams, interface depth | the visibility *within* that decomposition |
| `library-linkage-architect` | binary symbol export, ABI, linkage | the source-level modifiers, and the flag when the two disagree |
| `api-designer` | REST/GraphQL contract versioning | source-level promises |
| `iam-architect` | runtime authorization and identity | compile-time visibility |
| `code-reviewer` | the full review | the modifier-change review, as an API change |
| `secure-api-design` | network API security | source-level boundaries, and the erasure/permeability flags |

The pattern: `codebase-design` decides *where the boundaries are*; `library-linkage-architect` decides *what the linker exports*; this skill decides *what the source promises* — and flags when a modifier does not enforce what it appears to.

**The naming caution worth stating:** "access control" means **authorization** in security contexts (`iam-architect`, `secure-api-design`) and **source visibility** here. The two are unrelated, and conflating them in a routing decision sends a security question to a style skill or the reverse.
