# Access Modifiers — Backend (Java, Python, Go, Node)

> Full model: `access-modifiers` → `references/language-models.md` and the per-language files.

The backend is where all four models appear in one estate, and where two of them are mistaken for
boundaries they are not. This file is the working checklist per language.

## Java

**Package-private is the default** (no keyword), and there are two member modifiers beyond it.

| Level | Visible to |
|---|---|
| `public` | everywhere |
| `protected` | **subclasses, and every class in the same package** |
| *(none)* package-private | the package |
| `private` | the declaring class |

**The `protected` misreading is the most common Java visibility error.** It is *at least* as wide as
package-private, because it adds subclass access on top. If the intent is "subclasses only", Java
cannot express it for members — prefer composition, or a public final method delegating to a private
hook.

**Package-private is not a deployment boundary.** A package is a namespace; JARs bundle many, and a
package split across JARs still shares access at compile time. So splitting a package for clarity can
silently **widen** the visibility graph. Review a restructure as a visibility change.

**Where modularised, `exports` in `module-info.java` is the explicit public surface** the language
otherwise lacks — a `public` class in a non-exported package is unreachable from other modules. That
is a stronger boundary than the modifiers give.

**Java's own guidance is this skill's R1 and R3**: *"Use the most restrictive access level that makes
sense for a particular member. Use `private` unless you have a good reason not to"* and *"Avoid
`public` fields except for constants."*

## Python

**There is no private.** The tutorial states it plainly: private instance variables that cannot be
accessed from outside do not exist. What exists is a convention and a mangling rule.

| Form | Meaning | Enforced |
|---|---|---|
| `name` | public | n/a |
| `_name` | "non-public; subject to change without notice" | convention only |
| `__name` | mangled to `_Class__name` to avoid subclass clashes | renamed, not hidden |

**`__name` is not privacy.** Its documented purpose is avoiding name collisions with subclass
attributes — `C()._C__x` reads it fine.

**`__all__` is the closest thing to an explicit surface** and governs star-imports. It is a
declaration of intent, which is the honest level of enforcement available.

**`@property` is the R3 answer**, and it is idiomatic and strong: the representation stays private
while the interface is stable, and the setter has a home for invariants. Prefer it to a bare public
attribute wherever an invariant or a representation matters. For immutability, `frozen=True`
dataclasses.

**Never treat an underscore as a security control.** A value that must genuinely not be read belongs
behind a process boundary, a secret store, or an API design that never ships it. A type checker
(`mypy`, `pyright`) turns the convention into a review finding — useful, and still not a boundary.

## Go

**Two levels: exported and unexported**, decided by capitalisation. The default is closed, which is
the safe direction.

```go
func Visible() { }        // exported
func invisible() { }      // this package only
```

**There is no subtree mechanism**, so a helper shared by two packages must be **exported** and becomes
globally reachable. The remedy is structural, not syntactic:

- put both packages in one package, or
- use the **`internal/` directory**, which the toolchain enforces as importable only within the tree.

**Unexported fields plus an exported constructor** is the R3 and invariant answer:

```go
type Server struct {
    addr string                 // unexported — representation is ours
}

func NewServer(addr string) (*Server, error) {
    if addr == "" { return nil, errors.New("addr required") }
    return &Server{addr: addr}, nil
}
```

**A struct with all-exported fields is a public data shape** — right for a wire DTO, wrong for
anything with an invariant.

**The interface nuance worth using:** Go's implicit interfaces let you define a small *unexported*
interface as an internal seam, without publishing a type — the opposite of Java, where an interface is
inevitably a public surface.

**Tests need no widening:** `package foo` in `foo_test.go` reaches unexported identifiers. Prefer
`package foo_test` (external) where it works, because it tests what a consumer sees.

## Node / TypeScript services

**`private` is erased.** A token on a class field is readable by any code in the process — including a
transitive dependency — once compiled. Use `#field` where it must hold.

```ts
class Client {
  #apiKey: string;              // enforced at runtime
}
```

**Module privacy is «not exporting»**, and the exported set is the surface. Avoid `export *` in a
package entry point: it re-publishes everything the module imports and defeats surface review.

**Structural typing means exported *types* are part of the surface**, not only exported values. Prefer
an explicit exported `interface` to an inferred return type, which publishes whatever the
implementation happens to produce.

## The backend checklist

- [ ] Java: most restrictive level; `private` by default (the vendor's own guidance)
- [ ] Java: `protected`'s real scope (includes the package) understood before use
- [ ] Java: package restructures reviewed as visibility changes
- [ ] Java: `exports` treated as the explicit surface where modularised
- [ ] Python: `_name` treated as a convention; no secret relies on it
- [ ] Python: `__all__` declares the package surface; `@property` used for invariants
- [ ] Go: exported only when another package needs it; `internal/` for shared implementation
- [ ] Go: unexported fields plus an exported constructor where an invariant exists
- [ ] TypeScript: `#field` for anything sensitive; no `export *` in entry points
- [ ] Every language: no declaration widened to public so a test could reach it
