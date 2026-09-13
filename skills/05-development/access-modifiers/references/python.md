# Python

<!-- STANDARD: 3min -- the underscore convention, name mangling, and __all__ -->

> Grounded in *The Python Tutorial*, "Private Variables".

## The vendor's own position

The tutorial is unusually direct, and it should be quoted rather than paraphrased:

> "Private" instance variables that cannot be accessed except from inside an object
> don't exist in Python. However, there is a convention that is followed by most Python
> code: a name prefixed with an underscore (e.g. `_spam`) should be treated as a non-public
> part of the API (whether it is a function, a method or a data member). It should be
> considered an implementation detail and subject to change without notice.

So there is **one real level** (public) plus **two conventions**:

| Form | Meaning | Enforced? |
|---|---|---|
| `name` | public | n/a |
| `_name` | "non-public; subject to change without notice" | **convention only** |
| `__name` | name-mangled to `_Class__name` | mechanically renamed, not hidden |
| `__name__` | dunder — reserved for the language | do not invent these |

## Name mangling is not privacy

The tutorial is explicit about its purpose:

> Since there is a valid use-case for class-private members (namely to avoid name clashes
> of names with names defined by subclasses), there is limited support for such a
> mechanism, called name mangling.

Mangling exists to **avoid collisions with subclass attributes**, not to restrict access:

```python
class C:
    def __init__(self):
        self.__x = 1

print(C()._C__x)          # 1 — reachable; the name was rewritten, nothing was hidden
```

So `__x` gives you *"a different attribute name"*, which is why a subclass defining `__x` does not clobber the parent's. It is not a boundary.

## The practical rules

| Intent | Python answer |
|---|---|
| this class only | `_name` (convention) — and a comment if it matters |
| this module only | `_name`, plus `__all__` to control `from m import *` |
| this package only | `_name` in a submodule; a leading-underscore module name where appropriate |
| public | the name, documented |
| prevent construction mistakes | an explicit `__init__` that validates, or a factory function |
| prevent attribute mutation | `@property` with no setter, or frozen dataclasses |
| genuinely secret | **not Python's job** — a process boundary, a secret store, or an API design that never ships the value |

## `__all__` — the closest thing to an explicit surface list

```python
# package/__init__.py
__all__ = ["Client", "connect", "Config"]      # the published surface
```

Three effects:

1. `from package import *` imports only these names (R2's explicit-list practice).
2. Linters read it and will flag a name used but not listed.
3. It documents intent, which is the only enforcement available.

**Note:** `__all__` governs the star-import surface, not reachability. `from package import _internal` still works. It is a declaration of intent, which is precisely the honest level of enforcement Python offers.

## `@property` — encapsulation, achieved

Python's answer to R3 is idiomatic and strong: a private attribute behind a property, so the representation stays yours while the interface is stable.

```python
class Config:
    def __init__(self):
        self._timeout = 30

    @property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, value: int) -> None:
        if value <= 0:
            raise ValueError("timeout must be positive")
        self._timeout = value
```

Two advantages over a bare attribute:

- **The representation can change** without touching callers (rename `_timeout`, compute it, store it elsewhere).
- **An invariant has a home** — the setter validates, so an invalid state cannot be constructed.

For immutability, prefer `@dataclass(frozen=True)` or `NamedTuple` over "please don't mutate `_x`".

## Packages, modules and the actual boundary

Python has no compile-time access control, so the boundaries that exist are structural:

| Boundary | Enforced by |
|---|---|
| module | the import system |
| package (`__init__.py` surface) | `__all__` (convention) |
| published artifact | packaging config |
| process | the OS — the only hard boundary |

**If a value must genuinely not be read by other code, no naming convention achieves it.** Put it behind a process boundary, a service, or do not ship it. R4 exists precisely because `_name` and `__name` are frequently mistaken for controls they are not.

## Type checkers add a hint, not enforcement

`mypy` and `pyright` will flag access to `_name` from outside the module or class **as a warning**, which is genuinely useful in review. It is still static analysis of source that a runtime caller bypasses.

Worth enabling: it turns the convention into a finding. Not worth trusting as a boundary.

## The Python checklist

- [ ] `_name` used for non-public API, and understood as a convention
- [ ] `__name` used only for collision avoidance, never cited as privacy
- [ ] `__all__` declares the package's published surface (R2)
- [ ] No secret relies on an underscore for protection (R4)
- [ ] `@property` (or `frozen=True`) used instead of a bare public attribute where an invariant or representation matters (R3)
- [ ] Validation lives in `__init__` or a factory, not in a convention
- [ ] A type checker is enabled, so the convention produces review findings
- [ ] Genuine privacy is achieved structurally — a process, a store, or not shipping it
