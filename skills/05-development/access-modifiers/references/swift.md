# Swift

<!-- STANDARD: 3min -- open vs public, package, fileprivate, internal(set), @testable -->

> Grounded in *The Swift Programming Language*, "Access Control".

## The six levels

| Level | Visible in | Subclassable/overridable outside the module |
|---|---|---|
| `open` | any file in any module | **yes** |
| `public` | any file in any module | **no** |
| `package` | any file in the same **package** | no |
| `internal` (default) | any file in the same **module** | no |
| `fileprivate` | the same **source file** | n/a |
| `private` | the enclosing declaration (+ same-file extensions) | n/a |

## `open` vs `public` — the distinction that matters

The clearest teacher of the visibility/extension split in any language:

```swift
public class A { }                 // usable across modules; NOT subclassable outside the module
open  class B { }                  // usable AND subclassable across modules

public class C {
    public func a() { }            // callable everywhere; not overridable outside
    open   func b() { }            // overridable outside the module
}
```

The documentation states that marking a class `open` explicitly indicates the impact of code from other modules using it as a superclass has been considered. **That is R6 in one sentence:** subclassability is a deliberate announcement, not a visibility level.

**Practice:** start at `public`; promote to `open` only when a third party genuinely needs to subclass, and document the extension contract at that moment.

## The guiding principle

> No entity can be defined in terms of another entity that has a lower (more restrictive) access level.

```swift
private struct Detail { }
public func make() -> Detail { }     // ERROR: a public function cannot return a private type
```

The fix is *not* automatically to widen `Detail`. Ask first whether `make()` should be public at all — the compile error is often pointing at an over-wide function, not an over-narrow type.

Same rule for parameters, properties and generic constraints. Visibility propagates through signatures.

## `internal` — the default, and the right one for most code

Module-scoped: the framework or target. For an app this is the natural default, and it is stricter than Kotlin's or Java's, so Swift code starts in a better place.

**Consequence:** in a single-target app, `internal` and `public` differ only if the app ships a framework — so `public` in an app is usually a mistake with no benefit.

## `package` — the multi-module app

Added for apps and frameworks structured into several modules that ship together. Use it when a declaration must cross a module boundary **inside one package** but not beyond.

`internal` is per-module; `package` is per-package. In a multi-module app with a shared internal API, `package` is the level that expresses the intent.

## `fileprivate` — file-scoped, and why `private` is not

`private` is scoped to the *declaration* (plus same-file extensions), not the file. So a second type in the same file cannot see it:

```swift
struct A {
    private func p() { }
    fileprivate func f() { }
}
struct B {                          // same file
    func use(a: A) {
        // a.p()  — not visible: private is type-scoped
        a.f()     // visible: fileprivate is file-scoped
    }
}
```

Reach for `fileprivate` when a file-scoped helper or extension must share a member across types in that file — not as a general-purpose "almost private".

## `internal(set)` — the asymmetric setter

A common API shape: publicly readable, internally writable.

```swift
public struct Model {
    public internal(set) var id: Int      // read everywhere; write only inside the module
    public private(set) var count = 0     // read everywhere; write only inside this type
}
```

This is the idiomatic substitute for a getter over a private field, and it is strictly better than a public mutable property (R3): the representation stays yours.

| Form | Read | Write |
|---|---|---|
| `public var x` | everywhere | everywhere — the coupling R3 refuses |
| `public internal(set) var x` | everywhere | module only |
| `public private(set) var x` | everywhere | type only |
| `private var x` + computed getter | everywhere | type only, with logic |

## `@testable` — the test mechanism (R5)

```swift
@testable import MyModule      // reach any internal entity
```

Requires the module to be compiled with testing enabled, so **it cannot reach a release artifact** — which is exactly why it is the right mechanism and `public` is not.

`@testable` does **not** grant access to `private` or `fileprivate`. Testing those directly is a design smell — test the behaviour that uses them.

## The Swift checklist

- [ ] `public` is used only at a genuine module surface — not in a single-target app
- [ ] `open` appears only where cross-module subclassing is intended and documented (R6)
- [ ] `open` members are tested via a subclass, not only directly
- [ ] `internal(set)` / `private(set)` used instead of public mutable properties (R3)
- [ ] `fileprivate` used for file-scoped sharing, not as a loose `private`
- [ ] No public signature returns or accepts a less-visible type (the guiding principle)
- [ ] `package` used where a multi-module app needs a package-wide API
- [ ] Tests use `@testable`, and no declaration was widened for them (R5)
- [ ] `@testable` does not appear in a release build configuration
