# Access Modifiers — Kotlin

> Full model: `access-modifiers` → `references/kotlin.md`. Grounded in the Kotlin
> documentation, "Visibility modifiers".

## The four levels, and the default

| Level | Visible in | Default |
|---|---|---|
| `public` | everywhere | **yes — the default** |
| `internal` | the same **module** | no |
| `protected` | the class and its subclasses (class members only) | no |
| `private` | the file (top level) or the class | no |

**`public` is the default, so over-exposure in Kotlin happens by omission.** Narrowing is the
deliberate act — the opposite of Swift, and worth remembering when moving between the two.

## The Android-specific guidance

**1. `internal` means module, and the module is the Gradle source set.** Not the package, and not
necessarily the artifact. So `internal` is generally wider than Java's package-private and narrower
than `public` — and it is not the same unit as any other language's "internal".

**2. The Java permeability trap — the highest-severity Kotlin visibility issue.** `internal` is
enforced by the Kotlin compiler, **not the JVM**. Java code on the same classpath reaches it:

```kotlin
// module "core"
internal fun apiKey(): String = "…"
```

```java
// Java, same classpath — compiles and calls it
CoreKt.apiKey();
```

So `internal` is a boundary against Kotlin consumers and **not** a boundary against Java, reflection,
or bytecode. Where the intent is JVM-wide privacy: keep the declaration in a module Java cannot
depend on, split the artifact, or accept and document that it is Kotlin-internal only.

**3. `private set` instead of a `var`.** The idiomatic answer to encapsulation:

```kotlin
class Profile {
    var name: String = ""
        private set                       // readable everywhere; writable inside the class
    val id: String = ""                   // `val` — immutable, no setter at all
}
```

Prefer `val` for anything that does not change, and `private set` for anything the outside may read
but not write. A public `var` publishes the representation and is the R3 defect.

**4. Classes are `final` by default — which is the right default.** Do not add `open` unless
subclassing is intended. Where it is, the `open` member is a contract: document what a subclass may
rely on, and test the subclass path rather than only the base class.

**5. `protected` is illegal at the top level** — it applies to class members only. A top-level
declaration gets `private` (file-scoped) or `internal` (module-scoped).

**6. Tests reach `internal` through the test source set**, never by widening to `public`:

```kotlin
// src/test/kotlin — same module, so internal is visible
```

That is the mechanism; making a declaration public for a test leaks it to every consumer.

## The Android checklist

- [ ] `public` is a choice, not a default — narrowing is deliberate in Kotlin
- [ ] `internal` understood as module-scoped, not package- or JVM-scoped
- [ ] No `internal` declaration assumes Java cannot reach it; sensitive ones moved off the shared classpath
- [ ] `val` for immutable state; `private set` for read-only-from-outside properties
- [ ] No public `var` publishing the representation
- [ ] Classes left `final` unless subclassing is intended; `open` documented and tested
- [ ] `protected` used only on class members
- [ ] Tests use the test source set; nothing widened to `public` for them
- [ ] In KMP, `expect`/`actual` visibility is consistent and `internal` is the shared-module boundary
