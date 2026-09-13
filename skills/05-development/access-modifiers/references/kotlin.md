# Kotlin

<!-- STANDARD: 3min -- internal module semantics, private set, open/final, Java permeability -->

> Grounded in the Kotlin documentation, "Visibility modifiers".

## The four levels

| Level | Visible in | Default |
|---|---|---|
| `public` | everywhere | **yes — this is the default** |
| `internal` | the same **module** | no |
| `protected` | the class and its subclasses | no |
| `private` | the file (top level) or the class | no |

**Two facts that shape Kotlin practice:**

1. **`public` is the default**, so over-exposure happens by omission, not by choice. Narrowing is the deliberate act.
2. **`protected` is not available for top-level declarations** — it applies to class members only.

The documentation is precise that `private` at the top level means *file*-visible, while `private` inside a class means class-visible:

```kotlin
// example.kt
private fun f() { }            // visible inside example.kt only
internal val baz = 6           // visible everywhere in the module
public var bar: Int = 5
    private set                 // property readable everywhere; setter visible in example.kt
```

Note the last form: **`private set` is Kotlin's `internal(set)`**, and it is the idiomatic replacement for a getter over a private field (R3).

## `internal` means module — and the module is not the package

A Kotlin *module* is a compilation unit: a Gradle source set, a Maven module, an IntelliJ module, an Ant task. It is **not** a package, and not a deployment unit necessarily.

| Concept | Scope |
|---|---|
| package | a namespace; not an access boundary in Kotlin |
| module | the access boundary for `internal` |
| artifact/JAR | may contain many modules or one |

So `internal` is generally *wider* than Java's package-private and *narrower* than `public` — and it is not the same unit as any other language's "internal".

## The Java permeability trap (R4)

**Kotlin's `internal` is visible to Java code on the same classpath.**

```kotlin
// module "core"
internal fun apiKey(): String = "…"
```

```java
// Java, same classpath — compiles and runs
CoreKt.apiKey();
```

At the JVM level the declaration is public with a name-mangled suffix; `internal` is enforced by the Kotlin compiler, not the JVM. So:

- **Against Kotlin consumers**: the boundary holds.
- **Against Java consumers**: there is no boundary.
- **Against reflection**: never a boundary.

Where the intent is JVM-wide privacy, `internal` is not the mechanism. Options: keep it in a module that Java cannot depend on, split the artifact, or accept and document that it is Kotlin-internal only.

**This is the highest-severity Kotlin visibility issue**, and it is why R4 flags it rather than treating it as style.

## `open` / `final` — subclassability, decided separately (R6)

**Classes and members are `final` by default.** This is the opposite default from Java, and it is the better one: subclassability is opt-in.

```kotlin
class Closed { }                 // final — cannot be subclassed
open class Extensible {          // explicitly subclassable
    open fun hook() { }          // explicitly overridable
    fun sealedStep() { }         // callable, not overridable
}
```

Practice:

- Leave classes final unless an extension point is intended.
- A public class is *not* automatically subclassable — Kotlin already separates visibility from extension, which is the R6 requirement.
- Every `open` member is a contract: document what a subclass may rely on, and test the subclass path.
- In a shared library, prefer `final` + a documented interface/trait over an `open` base class.

## Compiler-wide concerns worth knowing

| Concern | Effect on visibility |
|---|---|
| `@JvmName` / JVM name mangling of `internal` | produces a public JVM symbol |
| `private` on a top-level member | file-scoped, not package- or module-scoped |
| Companion object members | `private` in a companion is visible to the enclosing class |
| `protected` in an interface | not permitted |
| `internal` in a Multiplatform shared module | shared-module-scoped, then per-target |

## Kotlin Multiplatform

In a shared module, `internal` is scoped to the **shared module**, and `expect`/`actual` declarations must have matching visibility across the shared and platform sides. Practical guidance:

- Prefer `internal` in the shared module; promote only what each platform genuinely needs.
- Keep `actual` declarations no *more* visible than their `expect` counterpart where the language requires it.
- Treat the shared module as the boundary: `internal` there is the natural default for implementation.

## The Kotlin checklist

- [ ] `public` was chosen, not defaulted — narrowing is deliberate in Kotlin (R1)
- [ ] `internal` understood as module-scoped, not package- or JVM-scoped
- [ ] No `internal` declaration assumes Java cannot reach it (R4)
- [ ] `private set` used instead of a public mutable property (R3)
- [ ] Classes left `final` unless subclassing is intended
- [ ] `open` members documented as contracts and tested via a subclass (R6)
- [ ] `protected` used only on class members (it is illegal at top level)
- [ ] Tests reach `internal` via the test source set, not via making it public (R5)
- [ ] In KMP, `expect`/`actual` visibility is consistent, and `internal` is the shared-module boundary
