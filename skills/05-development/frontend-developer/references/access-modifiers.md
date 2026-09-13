# Access Modifiers — Frontend (TypeScript, and the build boundary)

> Full model: `access-modifiers` → `references/typescript.md`.

Frontend is the ecosystem where **the modifier most often mistaken for a security boundary** is in
daily use, because everything you write ships to the browser or the bundle.

## The erasure trap, and it is the frontend-specific hazard

```ts
class AuthClient {
  private token = "…";          // compile-time only — ERASED
}
```

`private` and `protected` are erased on compile. In the emitted JavaScript the field is an ordinary
public property, reachable by:

- any consumer with `as any`
- `Object.keys` / `for…in` / spread
- a plain JavaScript module in the same bundle
- **any transitive dependency in the bundle**
- the browser console, in a client-side build

So on the frontend the practical consequence is sharper than elsewhere: **the field is in the shipped
artifact and everything in the artifact can read it.** `#field` is the runtime-enforced form:

```ts
class AuthClient {
  #token = "…";                 // enforced by the JS engine
}
```

**The related frontend rule:** a value that must never be readable by the client does not belong in
client code at all — no modifier makes it safe. Server-only secrets stay server-side; that is an
architecture decision, not a visibility one.

## Which modifier

| Situation | Use |
|---|---|
| ordinary encapsulation in a class | `private` — ergonomic and readable; the build enforces it |
| a secret, token, or bypassable invariant | `#field` — enforced at runtime |
| subclasses only | `protected`, noting it is compile-time only **and** a subclass can widen it to public |
| module-internal | **not export** it; TypeScript has no module keyword |
| anything public | `public` written explicitly, so omission is not the signal |

**The `protected` caveat is documented TypeScript behaviour:** a derived class may legitimately expose
a `protected` member more widely as part of a subtype contract. So `protected` is a convention with a
published widening path — the wrong tool for a member that must never be public.

## Module privacy is the exported set

The surface is what the module exports, and nothing else. Two practices make that a decision rather
than an accident:

**1. Avoid `export *` in an entry point.** It re-publishes everything the barrel file happens to
import, so the surface grows with every dependency (R2), and it defeats surface review.

```ts
// ❌ every re-exported symbol becomes public
export * from "./internal/helpers";

// ✅ name the surface
export { Client } from "./client";
export type { ClientOptions } from "./types";
```

**2. Structural typing means exported types are surface too.** An inferred return type publishes
whatever the implementation happens to produce — so prefer an explicit exported `interface`, which is
nameable, documentable and diffable.

```ts
// ❌ publishes the shape the implementation happens to have
export function createClient() { return { … }; }

// ✅ the published contract is named
export interface Client { request(path: string): Promise<Response>; }
export function createClient(): Client { … }
```

## The bundler is not a boundary

A tree-shaken, minified, bundled artifact does not enforce anything: the field is still there unless
it is provably unused, and minification renames rather than hides. **Do not treat "it won't be
included" or "the name is mangled" as privacy.**

The related trap: **an environment variable or a build-time constant is inlined into the bundle** and
is readable in the shipped artifact. That is a build-configuration concern, not a modifier one, and
the correct rule is the same — do not put secrets in client code.

## Testing (R5)

TypeScript has no friend mechanism (no `@testable`, no `InternalsVisibleTo`), so tests reach
internals by:

- living beside the module and importing from it — which means the declaration must be **exported**,
  or the test imports the module path and uses whatever the module exposes;
- testing the **exported** behaviour, which is what a consumer sees and is usually the better test.

**`#field` is unreachable from tests by design.** Test the behaviour that uses it. Never widen to
`public` for a test — in a frontend bundle the widening ships to every user.

## The frontend checklist

- [ ] No secret relies on `private` — `#field` used where the value must hold
- [ ] Nothing sensitive placed in client code on the assumption a modifier protects it
- [ ] `protected` not treated as a guarantee (a subclass can widen it)
- [ ] `export *` avoided in entry points; the surface is named explicitly
- [ ] Exported *types* reviewed as part of the surface; explicit interfaces over inferred shapes
- [ ] Bundling and minification not mistaken for a privacy mechanism
- [ ] Build-time constants and `NEXT_PUBLIC_*`-style values checked for secrets
- [ ] No declaration widened to `public` so a test could reach it
- [ ] `#field` support confirmed against the configured `target` / `useDefineForClassFields`
