# Java

<!-- STANDARD: 3min -- package-private, protected's real scope, modules, final vs sealed -->

> Grounded in the Oracle Java Tutorials, "Controlling Access to Members of a Class".

## The levels

| Level | Visible to |
|---|---|
| `public` | every class everywhere |
| `protected` | **subclasses, and every class in the same package** |
| *(no modifier)* — package-private | every class in the same package |
| `private` | the declaring class only |

**At the top level there are only two**: `public`, or package-private. `private` and `protected` are member-level modifiers.

## The vendor's own recommendation

The tutorial states the practice plainly, and it is the same restraint principle this skill follows:

> "Use the most restrictive access level that makes sense for a particular member. Use `private` unless you have a good reason not to."

and

> "Avoid `public` fields except for constants."

So R1 and R3 are not opinions imported from elsewhere — they are Java's own documented guidance.

## The `protected` misreading (the most common Java trap)

Most developers read `protected` as "subclasses only". The real scope includes **the entire package**:

```java
package a;

public class Base {
    protected void hook() { }     // visible to: subclasses anywhere, AND every class in package a
}

package a;

class Sibling {                   // not a subclass, same package
    void use(Base b) {
        b.hook();                 // compiles — package access via protected
    }
}
```

Consequences:

- A `protected` member is **not** a narrow extension-only surface; it is at least as wide as package-private.
- In a large package, `protected` is often wider than `public` in practice, because it adds subclass access on top of package visibility.
- If you want "subclasses only", **Java cannot express it** for members. Prefer composition, or a public final method delegating to a private hook.

## Package-private is the default — and the package is not a unit

Members with no modifier are package-scoped. That is the default, and for internal helpers it is usually the right level.

But note what a package is: **a namespace, not a deployment unit.** JARs bundle many packages; packages split across JARs still share package access at compile time (and at runtime on the classpath, modulo sealing). So:

- Package-private is *not* the same boundary as C#'s `internal` (assembly) or Rust's `pub(crate)`.
- Modularising a large package into smaller ones **does not narrow** package-private access — it can widen it, because formerly-one package becomes several.
- That is why package structure drifts: teams split packages for clarity and silently change the visibility graph.

## Java modules (`module-info.java`, JPMS)

The module system adds a layer *above* packages and is the only mechanism that makes a package boundary real at runtime:

```java
module com.example.core {
    exports com.example.core.api;          // the published surface — an explicit list (R2)
    // everything else is not exported, even if the classes are public
}
```

Two consequences worth internalising:

1. **`exports` is the explicit public surface this skill asks for.** A public class in a non-exported package is unreachable from other modules — so Java modules let you publish a *list*, not a default.
2. **A public class is not automatically reachable.** Without an `exports` directive, `public` is module-internal. That is a stronger and more honest boundary than visibility alone.

Where a project is modularised, treat `exports` as the API contract and everything else as internal, whatever the modifiers say.

## `final` and `sealed` — subclassability, decided separately (R6)

Java defaults to **subclassable**, so extension must be closed deliberately:

| Declare | Effect |
|---|---|
| `final class` | no subclassing |
| `final` method | no overriding |
| `sealed class` (with `permits`) | only the named subclasses may extend |
| `non-sealed` | explicitly re-opens a sealed hierarchy |

`sealed` is Java's strongest expression of an intentional extension contract: the permitted subtypes are named and exhaustive, which is exactly what R6 asks a designer to state.

**Practice:** default new classes to `final` unless extension is intended; use `sealed` when the extension set is known and finite; leave a class open only with a documented contract.

## Interfaces and defaults

- Interface members are **implicitly public** (and `abstract` unless `default`/`static`).
- You cannot narrow an interface member's visibility in Java — so an interface *is* a public surface.
- Consequently: do not use an interface as an internal seam if you intend to keep it internal. Use a package-private abstract class, or a module that does not export the interface's package.
- Nested types in an interface are implicitly public and static.

## The Java checklist

- [ ] Members use the most restrictive level; `private` by default (Java's own guidance, R1)
- [ ] `protected` used with its true scope in mind — it includes the package
- [ ] "Subclasses only" intent expressed by composition or a private hook, not `protected`
- [ ] No public mutable fields; constants excepted (R3)
- [ ] Package boundaries understood as namespaces, not units — and package splits reviewed for visibility changes
- [ ] Where modularised, `exports` is the explicit API list (R2)
- [ ] Classes default to `final`; `sealed` where the extension set is known
- [ ] Interfaces treated as public surfaces (their members cannot be narrowed)
- [ ] Tests live in the same package to reach package-private, rather than widening it (R5)
