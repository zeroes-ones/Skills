# Access Modifiers — macOS (Swift, app and framework targets)

> Full model: `access-modifiers` → `references/swift.md`. Grounded in *The Swift Programming
> Language*, "Access Control".

macOS is where Swift's level distinction earns its keep, because a macOS project routinely builds
**both** an app target and one or more frameworks. That makes `public` a real decision rather than a
formality — the opposite of an iOS app target, where it usually buys nothing.

## The decision that differs from iOS

| Target | Correct default | Why |
|---|---|---|
| macOS **app** target | `internal` | nothing imports it; `public` buys nothing |
| macOS **framework** target | `public` at the surface, `internal` for everything else | the framework *is* imported — and its surface is a product |
| **App extension** (share, widget, Finder) | `internal` within the extension; `public` only at a shared framework boundary | extensions are separate targets |
| **XPC service** | `public` at the service's message-handling surface only | the boundary is the message interface, not the code |

**The XPC point is the one most often missed:** an XPC service's exported surface is its message
protocol. Marking internal code `public` does not expose it across the process boundary, and marking
a message handler `private` does not hide it from a client that sends the right message. The message
protocol *is* the interface, and it needs its own review.

## Guidance specific to macOS

**1. A framework's surface is a product — publish it as an explicit list.** A macOS framework shipped
to other teams (or to customers) has a compatibility promise per public declaration. Generate the
surface (a symbol dump or an API report) and diff it, so an accidental `public` shows up in review.

**2. `open` is rare in a macOS framework, and expensive when granted.** Third parties subclassing your
NSView or controller means every future change must preserve the subclass contract. Prefer `public`
plus a protocol, or a `public` final method delegating to a private hook.

**3. `internal(set)` is the right shape for framework-owned mutable state.** A published value the
framework updates internally:

```swift
public struct DocumentState {
    public let id: String
    public internal(set) var isDirty: Bool    // clients read; the framework writes
}
```

That is the substitute for a public mutable property in every case where there is no accessor logic.

**4. Sandboxing and entitlements are a different layer — do not confuse them with visibility.** A
`public` declaration in a sandboxed app is reachable by any code in the process; the sandbox
constrains what the *process* may do, not what code within it may call. If a capability must be
unreachable, the mechanism is a helper process (XPC) or a separate framework, not a modifier.

**5. `@testable` works the same way as on iOS**, and the same rule applies: it needs a testing build,
so it cannot reach a release configuration, and it does not reach `private` or `fileprivate`.

## The macOS checklist

- [ ] App target: `internal` by default; `public` only at a deliberate boundary
- [ ] Framework target: an explicit, generated, diffed public surface
- [ ] `open` granted rarely, with a documented contract and a subclass test
- [ ] `internal(set)` used for framework-owned mutable state
- [ ] An XPC service's **message protocol** reviewed as its real interface
- [ ] Sandbox entitlements not mistaken for a code-visibility boundary
- [ ] `package` used where several targets in one package need a shared internal API
- [ ] Tests use `@testable`; nothing widened to `public` for them
- [ ] No `public` signature returns or accepts a less-visible type
