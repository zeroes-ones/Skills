# Go

<!-- STANDARD: 3min -- capitalisation export, and the absence of a subtree mechanism -->

> Grounded in *The Go Programming Language Specification*, "Exported identifiers".

## The rule, verbatim

> An identifier is exported to permit access to it from another package. An identifier is exported if both:
> - the first character of the identifier's name is a Unicode uppercase letter (Unicode character category Lu); and
> - the identifier is declared in the package block or it is a field name or method name.
>
> All other identifiers are not exported.

There are **two levels**: exported and not. No modifier keywords, no third option.

```go
package foo

func Visible()    { }      // exported — callable from other packages
func invisible()  { }      // unexported — this package only

type Client struct {
    Name   string          // exported field
    secret string          // unexported field
}
```

**Export is the deliberate act**, like Rust's `pub` — the default is closed, which is the safe direction.

## The structural constraint that shapes Go

**There is no "internal to this subtree" mechanism at the syntax level.** A helper shared by two packages must be *exported*, and is therefore reachable by every package that imports either — which is often wider than intended.

This is not a gap to work around with a trick; it is a design constraint that drives Go's package layout:

| Situation | The Go-idiomatic answer |
|---|---|
| A helper needed by two packages | put both in **one package**, or duplicate for clarity |
| Internal implementation shared across a project | use the **`internal/` directory** convention |
| A type that should not be constructible | unexported field + an exported constructor |
| A method only for internal callers | unexported method |
| A package's surface that must stay narrow | make the package do less |

## The `internal/` directory convention

Go's one structural boundary beyond capitalisation:

```
myproject/
├── internal/          ← anything under internal/ is importable only within myproject
│   └── config/
├── api/               ← public
└── cmd/
```

The toolchain enforces it: a package under `internal/` **cannot be imported** from outside the tree rooted at `internal/`'s parent. That is the closest Go gets to `pub(crate)`, and it is the right home for implementation that several packages share but no consumer should see.

**Use it deliberately:** `internal/` is a real boundary, so it is preferable to exporting a helper merely because two packages need it.

## Unexported fields and constructors

Go's answer to R3 and to invariant protection:

```go
type Server struct {
    addr     string        // unexported — representation is ours
    timeout  time.Duration
}

func NewServer(addr string) (*Server, error) {   // the only way to build one
    if addr == "" {
        return nil, errors.New("addr required")
    }
    return &Server{addr: addr, timeout: 30 * time.Second}, nil
}
```

The unexported field plus an exported constructor is the idiom, and it gives you three things at once: a hidden representation, a validated construction path, and a surface you can change.

**A struct with all-exported fields is a public data shape** — fine for a wire DTO, a defect for anything with an invariant to protect (R3).

## Methods, embedding and interfaces

| Construct | Visibility rule |
|---|---|
| method | exported iff capitalised |
| interface | a set of method signatures; implementation is implicit — **an interface itself can be unexported while its methods are exported** |
| embedded type | promotes its exported members; embedded unexported types promote only within the package |
| struct field | exported iff capitalised, independently of the type's own visibility |

**The interface nuance is worth knowing:** Go's implicit interfaces mean you can define a small *unexported* interface in your package and accept it, without publishing a type at all. That is a genuine way to keep a seam internal — and it is the opposite of Java, where an interface is inevitably a public surface.

```go
type store interface {                 // unexported interface — an internal seam
    get(key string) ([]byte, error)
}

func NewHandler(s store) *Handler { … }   // callers pass anything satisfying it, without naming it
```

## Testing (R5)

Go's test rules do the right thing by default:

- `package foo` in `foo_test.go` → the test can reach unexported identifiers (an *internal* test).
- `package foo_test` → the test sees only the exported surface (an *external* test).

**Prefer the external form where it works** — it tests the surface a consumer sees — and use the internal form when you must reach inside. Neither requires widening anything, which is why Go needs no `InternalsVisibleTo`.

## The Go checklist

- [ ] Export is deliberate; unexported is the default for anything not consumed elsewhere
- [ ] `internal/` used for implementation shared across packages (the one real subtree boundary)
- [ ] A helper exported only so another package can use it — challenged, and probably moved instead
- [ ] Unexported fields with an exported constructor where an invariant exists (R3)
- [ ] Structs with all-exported fields confined to transparent data types
- [ ] Small unexported interfaces used as internal seams where appropriate
- [ ] `package foo_test` used for external tests; the internal form only when necessary (R5)
- [ ] Embedded unexported types' promotion behaviour understood before relying on it
