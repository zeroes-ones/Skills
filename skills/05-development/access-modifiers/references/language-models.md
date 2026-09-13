# Language Models

<!-- DEEP: 5+min -- the per-language model comparison with defaults and traps -->

> **Verification note.** Access rules, interop boundaries and module systems change between
> compiler versions — Java modules, Swift packages, C# `private protected`, and Kotlin/Java
> interop have all changed materially. Confirm a specific rule against the installed
> compiler's documentation before relying on it.

## The comparison

| Language | Levels | Member default | Unit | Erasure / permeability |
|---|---|---|---|---|
| **Swift** | 6 (`private`, `fileprivate`, `internal`, `package`, `public`, `open`) | internal | module (framework/target) | `@testable` for tests; no runtime erasure |
| **Kotlin** | 4 (`private`, `protected`, `internal`, `public`) | **public** | **module** (compilation unit) | `internal` is visible to **Java** callers on the same classpath |
| **Java** | 4 (package-private, `private`, `protected`, `public`) | package-private | package | `protected` also includes the package |
| **C#** | 6 (`private`, `private protected`, `protected`, `protected internal`, `internal`, `public`) + `file` | `private` (members), `internal` (top-level) | assembly | two two-word modifiers that read alike |
| **Rust** | `private`, `pub`, `pub(crate)`, `pub(super)`, `pub(self)`, `pub(in path)` | **private** | crate | none; enforced by the compiler |
| **Go** | 2 (exported / unexported) | unexported | package | none — but no subtree mechanism either |
| **Python** | convention (`_x`), mangling (`__x`) | public | module | **nothing is enforced** except mangling |
| **TypeScript** | `public`, `protected`, `private`, `#field` | `public` | module | **`private` is erased at runtime** |
| **Dart** | `_` prefix (library-private) | public | **library** | none; the underscore is a library rule |

## The traps, ranked by severity

### 1. TypeScript `private` is erased at runtime

```ts
class Api {
  private token = "s3cret";     // compile-time only
}
const a = new Api() as any;
console.log(a.token);           // "s3cret" — readable by any JS caller
```

The modifier exists only for the type checker. Once compiled, the field is an ordinary property. **`#field` is the runtime-enforced form** and is the correct choice wherever privacy has to hold.

Severity: **security**, when the field holds a secret. This is why R4 flags it rather than treating it as style.

### 2. Kotlin `internal` is visible to Java

```kotlin
// module A
internal fun apiKey() = "…"
```

```java
// Java code on the same classpath — compiles and calls it
ModuleAKt.apiKey();
```

`internal` is a Kotlin-module concept. On the JVM, the generated method is public with a mangled name, so Java callers reach it. **The boundary is Kotlin-wide, not JVM-wide.**

Severity: **security/coupling**, where the API is meant to be unreachable from Java.

### 3. Java `protected` includes the package

Java's `protected` grants access to subclasses **and to every class in the same package**. Teams use it intending "subclasses only" and silently get package-wide exposure.

Severity: **coupling**, occasionally security where the package is shared.

### 4. Python enforces nothing

The tutorial is explicit: *"Private" instance variables that cannot be accessed except from inside an object don't exist in Python.* The underscore is a convention; `__name` triggers **name mangling** — documented as a mechanism to avoid name clashes with subclasses, not to hide anything.

```python
class C:
    def __init__(self):
        self._internal = 1        # convention: do not touch
        self.__mangled = 2        # becomes _C__mangled — still reachable
print(C()._C__mangled)            # 2
```

Severity: **documentation**, not a boundary. Never a security control.

### 5. C#'s two two-word modifiers

| Modifier | Means |
|---|---|
| `protected internal` | same assembly **OR** a derived class **in another assembly** (a union — *wider*) |
| `private protected` | same assembly **AND** a derived class (an intersection — *narrower*) |

They read alike and mean nearly opposite things in scope. Read them as set operations, not as words.

Severity: **correctness**, and a frequent review miss.

### 6. Go has no subtree mechanism

Export is capitalisation: *"An identifier is exported if… the first character of the identifier's name is a Unicode uppercase letter."* There is no "visible to this subtree", so a helper shared by two packages must be **exported** — and becomes globally reachable. The remedy is structural (put it in the right package), not syntactic.

Severity: **design constraint**, and it drives Go's package layout.

### 7. Swift `open` vs `public`

The most useful distinction in any language, and the clearest statement of the visibility/extension split:

| | Visible across modules | Subclassable across modules |
|---|---|---|
| `public` | yes | **no** |
| `open` | yes | **yes** |

Marking a class `open` is documented as an explicit acknowledgement that external subclassing has been considered. Use `public` unless you mean the extension contract.

Severity: **API contract**, permanent.

### 8. Swift's guiding principle

*"No entity can be defined in terms of another entity that has a lower (more restrictive) access level."*

A `public` function cannot return a `private` type. Language-neutral in spirit: **visibility propagates through signatures**, so a leaky signature forces you either to widen the type or narrow the function. Widen the type only after asking whether the function should be public at all.

Severity: **compile-time**, so it is caught — but the fix is where people over-widen.

## The mapping table (porting a surface design)

| Concern | Swift | Kotlin | Java | C# | Rust | Go |
|---|---|---|---|---|---|---|
| this file only | `private` / `fileprivate` | `private` | `private` | `private` / `file` | `pub(self)` | unexported |
| this unit only | `internal` | `internal` | package-private | `internal` | `pub(crate)` | unexported (same package) |
| this unit + tests | `@testable` | test source set | same package test | `InternalsVisibleTo` | `#[cfg(test)]` | same-package `_test.go` |
| subclasses | (no direct equivalent) | `protected` | `protected` (also package) | `protected` | public trait | n/a |
| anyone | `public` | `public` | `public` | `public` | `pub` | **Capitalised** |
| anyone + extend | `open` | `open` | non-`final` public | non-`sealed` public | public trait | n/a |

**The porting rule:** map by *promise*, not by keyword. `internal` (Kotlin, module) does not always map to `internal` (C#, assembly) if the deployment units differ — and it never maps to Go's unexported, which is package-scoped.

## The decision, per language

```text
Which language? → apply its default posture, then narrow:
  Rust      → private by default; add pub(crate)/pub deliberately
  Swift     → internal by default; public only at the framework surface; open only for plugins
  Kotlin    → public by default, so narrow aggressively; internal for module; watch Java
  Java      → package-private by default; remember protected includes the package
  C#        → private members; internal top-level; read the two two-word modifiers as sets
  Go        → unexported unless capitalised; export is the deliberate act
  Python    → convention only; never a boundary; use name mangling for collisions, not privacy
  TypeScript→ private is a hint; #field where it must hold
  Dart      → _ is library-scoped; the library is the unit
```

## Checklist

- [ ] The target language's level set and default are confirmed for the compiler version
- [ ] The unit boundary is identified (module / package / crate / assembly / library)
- [ ] Every erasure-based or permeable modifier is flagged (R4)
- [ ] `protected`'s real scope is confirmed before relying on it
- [ ] Two-word modifiers are read as set operations
- [ ] A ported design was mapped by promise, not by keyword
- [ ] Where the language enforces nothing (Python), the intent is documented rather than assumed
