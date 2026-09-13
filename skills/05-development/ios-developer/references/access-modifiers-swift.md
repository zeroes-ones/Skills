# Access Modifiers — Swift

> Full model: `access-modifiers` → `references/swift.md`. Grounded in *The Swift Programming
> Language*, "Access Control".

## The six levels, and the default

| Level | Visible in | Subclassable outside the module |
|---|---|---|
| `open` | any module | **yes** |
| `public` | any module | **no** |
| `package` | the same package | no |
| `internal` **(default)** | the same module (target/framework) | no |
| `fileprivate` | the same source file | n/a |
| `private` | the enclosing declaration + same-file extensions | n/a |

## The iOS-specific guidance

**1. In an app target, `public` is almost always a mistake.** `internal` is the default and reaches
everything in the target. `public` buys nothing unless the app ships a framework — so treat every
`public` in an app target as either a framework boundary you intended, or a leftover.

**2. `open` is a decision, not a visibility level.** `public` makes a class usable across modules;
it does **not** make it subclassable. Use `public` by default, and promote to `open` only when a
third party genuinely needs to subclass — at which point you owe them a documented contract and a
subclass-path test.

**3. `internal(set)` / `private(set)` instead of mutable public state.** The idiomatic Swift answer
to encapsulation:

```swift
public struct Profile {
    public let id: String                    // immutable — fine to publish
    public internal(set) var name: String    // read everywhere; write inside the module
    public private(set) var score = 0        // read everywhere; write inside this type
}
```

Prefer these to a computed getter over a private field where there is no logic in the accessor.

**4. `fileprivate` is file-scoped; `private` is declaration-scoped.** A second type in the same file
cannot see a `private` member. Reach for `fileprivate` when a file-scoped helper or a same-file
extension must share a member across types in that file — not as a loose "almost private".

**5. The guiding principle catches over-wide functions, not just under-wide types.** "No entity can
be defined in terms of another entity that has a lower (more restrictive) access level." When a
`public` function returns an `internal` type, the error is often pointing at the *function*, not the
type. Ask whether the function should be public before widening the type.

**6. Tests reach `internal` via `@testable`, and `@testable` does not ship.** It requires a testing
build, so it cannot reach a release configuration — which is why it is right and `public` is not. It
does **not** reach `private` or `fileprivate`; testing those directly couples the test to the
implementation.

## The iOS checklist

- [ ] `public` appears only at a genuine framework or package boundary — not in an app target
- [ ] `open` used only where cross-module subclassing is intended, documented and tested
- [ ] `internal(set)` / `private(set)` used instead of mutable public properties
- [ ] `let` for published values that never change
- [ ] `fileprivate` used for file-scoped sharing, not as a general `private`
- [ ] No `public` signature returns or accepts a less-visible type
- [ ] `package` used where a multi-module app needs a package-wide API
- [ ] Tests use `@testable`; nothing was widened to `public` for them
- [ ] `@testable` confirmed absent from the release configuration
