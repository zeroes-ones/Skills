# C#

<!-- STANDARD: 3min -- the six levels, protected internal vs private protected, file, InternalsVisibleTo -->

> Grounded in Microsoft Learn's C# access-modifier documentation and the Framework Design
> Guidelines.

## The levels

| Modifier | Visible to |
|---|---|
| `public` | any assembly |
| `protected internal` | same assembly **OR** a derived class in another assembly |
| `protected` | the class and derived classes |
| `internal` | the same assembly |
| `private protected` | same assembly **AND** a derived class |
| `private` | the class or struct only |
| `file` | the same source file (top-level types only) |

## The two-word modifiers, read as set operations

They read alike and behave nearly oppositely. Read them as boolean logic, not as words:

| Modifier | Logic | Scope |
|---|---|---|
| `protected internal` | **OR** — same assembly, or a derived class elsewhere | **wider** |
| `private protected` | **AND** — same assembly, and a derived class | **narrower** |

So `protected internal` is the *most permissive* of the two-word forms, and `private protected` the least. A review that treats them as synonyms will mis-scope a member in one direction or the other.

## Defaults

| Declaration | Default |
|---|---|
| top-level type | `internal` |
| class/struct member | `private` |
| interface member | `public` |
| delegate in a namespace | `internal` |
| enum member | `public` |

Two facts from that table worth acting on:

1. **Top-level types default to `internal`** — the assembly boundary. That is a good default: a new type is not published by accident.
2. **Interface members are implicitly `public`** and cannot be narrowed (C# 8+ allows default implementations; accessibility on interface members has narrowed in recent versions, so verify against the target language version).

## `file` — the file-scoped type

```csharp
file sealed class Helper { }      // visible only in this source file
```

Added for source generators and file-local helpers. **It cannot be combined with any access modifier**, and it applies to top-level (non-nested) types only.

This fills the gap left by `private` — which, as in Swift, is *declaration*-scoped, not file-scoped.

## `InternalsVisibleTo` — the test mechanism (R5)

```csharp
[assembly: InternalsVisibleTo("MyProject.Tests")]
```

Grants a named assembly access to this assembly's `internal` declarations. It is a compile-time attribute, so it does not change the shipped surface, and it is the correct way to reach internals from tests.

Three cautions:

- It is **not** a security boundary: any assembly that can convince the compiler it is named can be granted access. Never rely on it to protect a secret.
- It **should not ship** in a release artifact if the test assembly is not shipped — verify the build configuration excludes it.
- Prefer one explicit friend assembly over a wildcard, so the surface of trust is enumerable.

## Assembly boundaries

`internal` in C# means *this assembly* — a stronger and more concrete unit than Java's package:

| Concept | Boundary |
|---|---|
| Java package-private | the package (a namespace, not a unit) |
| C# `internal` | the assembly (a deployment unit) |
| Kotlin `internal` | the module (a compilation unit) |

Because an assembly is a real deployment unit, **`internal` in C# is usually a sound boundary** — better than Java's package-private and comparable to Rust's `pub(crate)`. Use it as the default for anything not meant to be public.

## The Framework Design Guidelines posture

Microsoft's Framework Design Guidelines organize recommendations as **Do / Consider / Avoid / Do not**, and state explicitly that good library design may occasionally require violating them — such cases should be rare, clearly understood, and documented. That posture maps directly onto this skill's rules:

| Guideline posture | This skill's rule |
|---|---|
| Expose the minimum surface | R1, R2 |
| Avoid public fields | R3 |
| Do not expose mutable state | R3 |
| Consider `sealed` for library classes | R6 |

**The `sealed` recommendation is the notable one:** the Guidelines favour sealing library classes by default, because an unsealed public class is an extension contract whether or not it was intended as one. That is R6, stated by the vendor.

## The C# checklist

- [ ] Top-level types are `internal` unless deliberately published (the default, kept)
- [ ] `protected internal` and `private protected` are read as OR and AND, not as synonyms
- [ ] `sealed` used for library classes unless subclassing is intended (R6)
- [ ] No public mutable fields; properties with non-public setters instead (R3)
- [ ] Interface members recognized as public surfaces
- [ ] `file` used for source-generator and file-local helpers, not as a general `private`
- [ ] `InternalsVisibleTo` used for tests, naming one assembly, not a wildcard (R5)
- [ ] `InternalsVisibleTo` excluded from release builds
- [ ] No secret relies on `internal` or `InternalsVisibleTo` for protection
