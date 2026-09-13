# Test Visibility

<!-- STANDARD: 3min -- every ecosystem's test mechanism, and why public is wrong -->

## The rule

**Tests are a consumer, but a special one with a dedicated mechanism.** Widening to `public` so a test can reach a declaration leaks that declaration to every real consumer — and the test was never the consumer you had to satisfy (R5).

## The mechanisms, by ecosystem

| Ecosystem | Mechanism | Reaches | Ships? |
|---|---|---|---|
| **Swift** | `@testable import` | `internal` (not `private`/`fileprivate`) | no — needs a testing build |
| **Kotlin/Java** | the test source set / same package | `internal` / package-private | no |
| **C#** | `[assembly: InternalsVisibleTo("Tests")]` | `internal` | compile-time attribute; verify it is excluded from release |
| **Rust** | `#[cfg(test)] mod tests` in the module | everything, including private | no — compiled out |
| **Rust** | a `tests/` integration dir | the public surface only | no |
| **Go** | `package foo` in `foo_test.go` | unexported | no |
| **Go** | `package foo_test` in `foo_test.go` | the exported surface only | no |
| **Python** | same module/package path | `_name` (convention) | n/a |
| **TypeScript** | same path; no friend mechanism | `export`ed only | n/a |
| **Dart** | same library (`part`), or the public surface | `_name` only within the library | n/a |
| **C++** | `friend` declarations, or `FRIEND_TEST` | private members | n/a |
| **Kotlin Multiplatform** | the common test source set | `internal` in the shared module | no |

**The pattern:** mature ecosystems give tests a first-class path to internals that does **not** change the shipped surface. Where that path is absent (Dart, TypeScript), the honest answer is to test the public behaviour — not to widen.

## Why `public` is the wrong mechanism

```text
Widened for tests:
  class Helper {                     // now public, for the test
      public void internalStep() { } // every consumer may call it
  }
  → the consumer surface grew by one, permanently
  → the test now constrains it: changing it breaks the test
  → and the "consumer" it was widened for does not ship
```

Three harms at once:

1. **The surface grows.** A promise made to nobody who ships.
2. **The test constrains the design.** Testing a private step couples the test to the implementation, so a refactor breaks the test even when behaviour is unchanged.
3. **The widening is permanent.** Narrowing it later is a breaking change, even though the only consumer was a test.

## Testing internals honestly

| What you want to test | The right approach |
|---|---|
| The public behaviour | test it as a consumer does — the strongest test |
| An internal member's behaviour | the ecosystem's mechanism (`@testable`, `InternalsVisibleTo`, same-package test) |
| A private helper | **do not test it directly** — test the behaviour that uses it |
| A private field | test through the accessor or the observable effect |
| A seam for dependency injection | make the seam `internal`/package-private and inject through it |

**The third row is the important one.** Testing a private helper directly is a design smell in two directions: it means the behaviour is not observable through the public surface (so the design may be wrong), and it means the test will break on any refactor.

**If a private helper has interesting logic, that logic wants its own type** — with its own visibility, its own tests, and a place in the design. That is the refactor the test is pointing at.

## Verifying the mechanism does not ship

Every test-visibility mechanism must be absent from a release artifact. Verify, do not assume:

| Mechanism | Check |
|---|---|
| `@testable` | the release configuration compiles without testing enabled |
| `InternalsVisibleTo` | the attribute is excluded from release builds, or names an assembly that does not ship |
| `#[cfg(test)]` | the release build has no test code — trivially true, and worth confirming |
| a test source set | the test target is not packaged into the artifact |
| Go's internal test package | `_test.go` files are never compiled into a binary |

**The C# case warrants the most care**, because `InternalsVisibleTo` is a source attribute and can reach a shipped assembly if the build configuration does not exclude it — and it is not a security boundary even when it is correct, since the check is name-based.

## The friend mechanism (C++)

C++ is the outlier: `friend` grants a *specific* class or function access to private members, and `FRIEND_TEST(Class, Test)` is the test-specific form.

```cpp
class Engine {
    friend class EngineTest;              // one named friend
    friend class Engine_InternalLogic_Test;  // via FRIEND_TEST
  private:
    int state_ = 0;
};
```

Two cautions:

- **`friend` is not inherited and not transitive** — granting it does not spread, which is good, but it also means each test fixture needs its own grant.
- **It is compile-time only**, like every other mechanism here; it changes what compiles, not what ships.
- **Too many friends is a design signal:** if many classes need access, the class is doing too much, or the representation wants to be a small type with its own surface.

## The test-visibility checklist

- [ ] No declaration is `public` (or wider) solely for tests (R5)
- [ ] The ecosystem's mechanism is used: `@testable`, `InternalsVisibleTo`, test source set, `#[cfg(test)]`, same-package tests, `friend`
- [ ] Tests of public behaviour go through the public surface, not around it
- [ ] Private helpers are tested through the behaviour that uses them, not directly
- [ ] A private helper with interesting logic was refactored into its own type rather than tested in place
- [ ] The mechanism is verified absent from the release artifact
- [ ] `InternalsVisibleTo` names one assembly, not a wildcard, and is not treated as a security boundary
- [ ] Where no mechanism exists (Dart, TypeScript), the limitation is stated rather than worked around by widening
