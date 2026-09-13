# Rust

<!-- STANDARD: 3min -- private by default, pub(crate), pub(super), pub(in path) -->

> Grounded in *The Rust Reference*, "Visibility and privacy".

## The default is private

> By default, everything is private, with two exceptions: associated items in a `pub` trait are public by default…

This is the safest default in any mainstream language, and it is the shape worth imitating elsewhere by habit: **nothing is published until you say `pub`**.

Rust's own model is two rules:

1. An item is visible to a module if it is public in that module, or if the module is a descendant of the item's module.
2. An item is visible through a path only if every component of the path is visible.

The second rule is why a `pub` item inside a private module is unreachable — **the module chain gates the item**. That is a useful property: you can make an item public while keeping its module private, and it stays unreachable until the module is published.

## The visibility forms

| Form | Visible within |
|---|---|
| *(nothing)* | the enclosing module and its descendants |
| `pub(self)` | the current module — explicit private |
| `pub(super)` | the parent module |
| `pub(crate)` | the whole crate |
| `pub(in path)` | the named ancestor module (`path` must resolve to an ancestor) |
| `pub` | anywhere, subject to the module chain |

`pub(self)` exists mainly for macro hygiene and explicitness; `pub(crate)` and `pub(super)` are the practical forms.

## The two forms you will actually use

### `pub(crate)` — Rust's "internal"

The analogue of C#'s `internal` and Kotlin's module-internal, and the natural choice for anything the crate needs but consumers do not:

```rust
pub(crate) fn validate(input: &str) -> Result<(), Error> { … }
```

Because a crate **is** the unit of distribution, `pub(crate)` is a real boundary — unlike Java's package-private, which is only a namespace. Prefer it over `pub` by default for internal APIs.

### `pub(super)` — the parent, and why it exists

For a child module exposing something only to its parent, which is the idiomatic way to keep a submodule's surface closed while the parent composes it:

```rust
mod engine {
    pub struct Engine { /* private fields */ }
    impl Engine {
        pub(super) fn new_internal() -> Self { … }   // the parent may construct; nobody else
    }
}

pub fn build() -> engine::Engine {
    engine::Engine::new_internal()          // the parent can call it
}
```

**The pattern:** private fields plus a `pub(super)` constructor gives you a type that consumers can use but only its parent can create. That is a genuine encapsulation tool, not a visibility tweak.

## Private fields and construction

Rust gives you the R3 answer for free, if you use it:

```rust
pub struct Config {
    pub(crate) timeout: Duration,      // crate-visible field
    retries: u8,                       // private — the representation is yours
}

impl Config {
    pub fn retries(&self) -> u8 { self.retries }        // accessor
    pub fn set_retries(&mut self, n: u8) { self.retries = n; }   // controlled mutation
}
```

**A `pub` field is a permanent commitment** to the field's name and type, exactly as a public field is elsewhere. Keeping fields private and exposing methods is the default-correct shape.

## Traits and the visibility/extension split

Rust has no inheritance, so the R6 question takes a different form: **is the trait public?** A public trait is an extension point that anyone may implement.

```rust
pub trait StorageEngine {              // third parties may implement — an extension contract
    fn get(&self, key: &[u8]) -> Option<Vec<u8>>;
}

pub(crate) trait InternalHook { }      // crate-only implementation
```

Rust's advantage over class-based languages: **a public trait does not commit you to any implementation**, so an extension point is cheaper to publish than an `open` class or a `protected` method. Where a Rust library would otherwise expose a subclassable base, prefer a public trait plus a sealed-by-default set of implementations.

**The sealed-trait pattern** is the standard way to publish a trait for use but not implementation: a public trait with a private supertrait.

```rust
mod private { pub trait Sealed {} }

pub trait Format: private::Sealed { }        // usable, but not implementable outside the crate
```

That is Rust's `sealed`, and it is exactly the "callable but not extensible" level that Java and C# lack.

## Module chain as a boundary tool

Because a `pub` item is unreachable while its module is private, you can stage publication:

```rust
mod v2 {                       // private module
    pub struct Client { }      // pub, but unreachable from outside
    pub fn connect() { }
}

pub mod api {                  // public module
    pub use crate::v2::Client; // selectively re-export just what is published
}
```

Useful for keeping implementation modules private while publishing a curated surface (`pub use`) — Rust's version of the explicit surface list.

## The Rust checklist

- [ ] Default is private; `pub` is added deliberately (the language already enforces the posture)
- [ ] `pub(crate)` preferred over `pub` for internal APIs
- [ ] `pub(super)` used for parent-only construction
- [ ] Struct fields private unless a `pub` field is genuinely intended (R3)
- [ ] A public trait is treated as an extension contract, or sealed with a private supertrait (R6)
- [ ] `pub use` re-exports used to publish a curated surface, not blanket re-exports
- [ ] Implementation modules kept private where only the surface should be reachable
- [ ] `#[cfg(test)] mod tests` (in-module) used to reach private items, rather than widening (R5)
- [ ] A `pub` item inside a private module recognized as unreachable until the module is published
