# The Ladder

<!-- DEEP: 5+min -- the six visibility levels, language-neutral, and what each promises -->

## The universal ladder

Every language implements a subset of the same six levels. The names differ; the *promises* do not.

| Level | Who may use it | The promise it makes | Cost to change |
|---|---|---|---|
| **1. Private** | the enclosing declaration (and its same-file extensions) | none — it is yours | free |
| **2. File-private** | anything in the same source file | none beyond the file | free |
| **3. Package / module-internal** | the package or module | we may change it, but only as a unit | needs a unit-wide review |
| **4. Protected** | subclasses (and, in Java, the package) | subclasses may depend on it | constrains every subclass |
| **5. Public** | any consumer that can import the module | a compatibility promise with a lifetime | breaking change to narrow |
| **6. Open / overridable** | any consumer, and it may be **extended** | a subclass contract, permanently | the strongest promise of all |

**The rule is the asymmetry.** Widening costs one word and promises something; narrowing is a breaking change. That is why the default is the narrowest level that compiles, and why every widening is a decision rather than a convenience.

## Why the levels are not a single axis

Two different things are being promised at different levels:

```
Levels 1–3 : VISIBILITY   — who may call this
Levels 4–6 : EXTENSION    — who may build on this
```

`protected` and `open` are not "more public" than `public` in a meaningful ranking sense — they grant a *different* thing. A `public` non-overridable method is callable by everyone and changeable by you. A `protected` one is callable by fewer and changeable by you *only if you preserve the subclass contract*.

This is why Decision Tree 3 asks about subclassability separately, and why R6 refuses to treat it as a side effect of visibility.

## The levels in prose

### Private — the default you should reach for first

The declaration is an implementation detail. Nothing outside may depend on it, so it can be renamed, restructured or deleted at will. **Zero cost to change** is the whole value, and it is the reason to prefer it.

**Not the same as encapsulation.** A private *field* reached through a public getter is encapsulated. A private field read by a public *field* is not — the representation leaked.

### File-private — a Swift-specific extra rung

Useful where a file-scoped extension needs a member that no other file should see:

```swift
private func helper() {}          // this type, plus same-file extensions
fileprivate func helper2() {}     // anywhere in this file
```

The distinction matters because Swift's `private` is *type*-scoped, not file-scoped, so a second type in the same file cannot see it.

### Package / module-internal — the unit boundary

The declaration is internal to a unit: a Java package, a Kotlin module, a C# assembly, a Rust crate, a Dart library. External consumers cannot use it; the unit's own code can, freely.

**This is the level most often conflated across languages**, because "package" and "module" mean different things in each. Kotlin's `internal` is *module*-scoped, not package-scoped. Rust's `pub(crate)` is crate-scoped. Java's package-private is package-scoped — and a package is not a deployment unit. See `references/language-models.md`.

### Protected — subclassable, and wider than you think

The declaration is available to subclasses. In **Java it is also available to the whole package**, which is a common misreading: teams use `protected` intending "subclasses only" and get package-wide exposure.

`protected` is the first level that constrains your future changes: a subclass may depend on it, so changing it is a breaking change in a way that changing a private member is not.

### Public — the compatibility promise

Any consumer that can import the module may use it. This is where the promise acquires a *lifetime*: narrowing a public declaration is a breaking change, and consumers you cannot enumerate may depend on it.

**Public is where the API surface begins.** Below it, you are free. At it, you are committed.

### Open / overridable — the extension contract

The declaration is public *and* may be extended: subclassed, overridden, or (in Rust's analogue) implemented against a public trait.

This is the strongest and most expensive promise in the ladder. Every future change must:
- preserve the subclass contract,
- keep overridable members overridable,
- avoid the fragile-base-class traps (calling overridable methods from the constructor, changing invariants subclasses relied on),
- and be tested against a subclass, not only against the base class.

Swift makes this distinction explicit and is the clearest teacher of it: a `public` class is visible across modules but **not subclassable** outside its own; `open` grants both, and marking a class `open` is documented as an explicit statement that the impact of external subclassing has been considered.

## The language-neutral decision

```text
For each declaration:
  1. Who consumes it?          → the level this selects
  2. Could anyone else?        → if "maybe", stay narrow (R1)
  3. Does the promise survive a rename or restructure?
     ├── Yes → it is a private/internal detail; keep it narrow
     └── No  → it is a promise; record it, and treat changing it as breaking
  4. Is subclassability needed, in addition to visibility? → level 6, deliberately (R6)
```

## The defaults, and which philosophy each encodes

| Language | Default for a member | The philosophy |
|---|---|---|
| **Rust** | **private** | the safe default; `pub` is the deliberate act |
| **Swift** | internal (module) | module is the natural unit |
| **Kotlin** | **public** | convenience; narrowing is deliberate |
| **Java** | package-private | the package is the unit |
| **C#** | `private` for members, `internal` for top-level types | mixed, and worth knowing |
| **Go** | unexported (lowercase) | export is deliberate via capitalisation |
| **Python** | public | nothing is enforced; convention only |
| **TypeScript** | `public` | compile-time only; `#field` is the real private |

**The Rust default is the shape to imitate**, whatever the language: private unless deliberate.

## Checklist

- [ ] Every declaration is at the narrowest level that compiles (R1)
- [ ] Visibility and subclassability were decided separately (R6)
- [ ] Widening is recorded as a promise, with its consumer named
- [ ] `protected`'s real scope in the target language was confirmed
- [ ] The unit boundary (package vs module vs crate vs assembly) is understood for this language
- [ ] Nothing is public only because another public declaration returns it
- [ ] The public surface is an explicit list, not "not private"
