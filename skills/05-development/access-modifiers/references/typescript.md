# TypeScript

<!-- STANDARD: 3min -- private vs protected vs #field, and erase-at-runtime -->

> Grounded in the TypeScript Handbook, "Member Visibility".

## The four forms

| Form | Visible to | Enforced at runtime? |
|---|---|---|
| `public` (default) | everywhere | n/a |
| `protected` | the class and subclasses | **no** |
| `private` | the class only | **no** |
| `#field` (ECMAScript private) | the class only | **yes** — a real runtime boundary |

**The default is `public`**, and the documentation notes that you never *need* to write it — which means over-exposure in TypeScript happens by omission.

## The erasure trap (R4, and it is a security issue)

TypeScript's `private` and `protected` are **compile-time only**. They are erased on compile; the emitted JavaScript has an ordinary public property.

```ts
class Api {
  private token = "s3cret";
}

const api = new Api() as any;
console.log(api.token);            // "s3cret"
```

Any of these reaches it, with no type error at runtime because there is no runtime check:

- `as any` / `as unknown as`
- reflection via `Object.keys` / `for…in`
- a plain JavaScript consumer of the compiled output
- `JSON.stringify`, a debugger, or `console.log`

**So `private` documents intent; it does not enforce it.** Where the privacy has to hold — a token, a credential, an invariant you cannot let be bypassed — use `#field`.

```ts
class Api {
  #token = "s3cret";               // ECMAScript private: enforced by the JS engine
}

const api = new Api() as any;
console.log(api.#token);            // SyntaxError — genuinely unreachable
```

`#field` is not a TypeScript feature; it is a JavaScript one, so it works in any environment supporting it and cannot be erased.

## Which to choose

```text
Does anything outside this class need to read it?
├── No → is it a secret or a security-relevant invariant?
│   ├── Yes → #field (R4)
│   └── No  → `private` is acceptable: it communicates intent and the build enforces it
├── Subclasses only → `protected`, and note that it is compile-time only and can be
│   widened by a subclass making it public (documented TypeScript behaviour)
└── Everyone → public, deliberately
```

**The practical split:** `private` for ordinary encapsulation (it is ergonomic and readable), `#field` wherever the value's secrecy matters.

## `protected` and its documented escape

The Handbook documents that a derived class may legitimately expose a `protected` member more widely as part of a subtype contract. That is a real feature — and it means `protected` is **not** a guarantee: a subclass can publish what the base kept protected.

```ts
class Base { protected m = 10; }
class Derived extends Base { public m = 10; }    // documents as allowed
```

So `protected` is a convention with a documented widening path. If a member must never be public, `protected` is the wrong tool.

## Structural typing and the surface question

TypeScript's type system is **structural**, which changes what "private" means at the type level: two structurally identical types are assignable. Private/protected members participate in assignability (a class with a `private` member is only assignable from the same declaration), but structural matching still means **the shape is the interface** in most cases.

Consequence: **the exported types are the API surface**, not only the exported values. A public function's parameter and return types are published whether or not you intended it — the language-neutral "visibility propagates through signatures" rule, with extra force because the *shape* is the contract.

| Practice | Why |
|---|---|
| Export explicit interfaces, not inferred shapes | an inferred type publishes everything the implementation happens to have |
| Prefer `interface` for a published contract | it is nameable, documentable and diffable |
| Keep internal types unexported | an unexported type cannot be built on even if structurally identical |
| Avoid `export *` | it publishes everything in the module by default (R2) |

## Module-level privacy

TypeScript has no module-internal keyword. Module-level privacy is achieved by **not exporting**:

```ts
// internal.ts — exports nothing; only this module's own code uses it
function helper() { }

export function publicApi() { helper(); }    // the module's surface is what it exports
```

So the surface is `export` — the same "deliberate act" shape as Rust's `pub` and Go's capitalisation, and the opposite of `private`'s accidental widening.

**Avoid `export *`** in a public entry point: it re-publishes everything a barrel file happens to import, which is surface-by-accident (R2) and makes tree-shaking less effective.

## Testing (R5)

TypeScript tests reach internals the way the rest of the ecosystem does:

- **Same module path** — a test file in the same directory can import unexported items only if they are exported; TypeScript has no friend mechanism. So the common pattern is to test the exported surface, or to put the test beside the implementation and accept that it imports the module.
- **`#field` is unreachable from tests by design.** Test the behaviour that uses it, not the field.
- **Never widen to `public` for a test** (R5). If the surface is the only thing testable, the test is testing the surface — which is often the better test anyway.

## The TypeScript checklist

- [ ] `private` is not relied on where secrecy matters — `#field` is used instead (R4)
- [ ] `protected` is not treated as a guarantee (a subclass can widen it)
- [ ] Module privacy is expressed by *not exporting*, and the exported set is the surface (R2)
- [ ] `export *` avoided in public entry points
- [ ] Exported *types* reviewed as part of the surface, not only exported values
- [ ] Explicit interfaces exported rather than inferred shapes
- [ ] `public` written explicitly where it is intended, so omission is not the signal
- [ ] No declaration widened to `public` for tests (R5)
- [ ] `#field` behaviour confirmed against the target runtime (`target`/`useDefineForClassFields`)
