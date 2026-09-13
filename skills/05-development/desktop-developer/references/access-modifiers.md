# Access Modifiers — Desktop (C#, Swift, and Electron/TypeScript)

> Full model: `access-modifiers` → `references/language-models.md`, `references/csharp.md`,
> `references/typescript.md`.

Desktop spans two very different models in one product: a **compiled** side (C# or Swift) where the
modifier is enforced by the compiler or runtime, and a **JavaScript/TypeScript** side where two of
the modifiers are not enforced at all. The desktop-specific risk is that the same feature is written
in both.

## The compiled side (C# / Swift)

| Concern | C# | Swift |
|---|---|---|
| unit | **assembly** (a real deployment unit) | module (framework/target) |
| member default | `private` | internal |
| top-level type default | `internal` | internal |
| read-only idiom | a property with a private setter | `internal(set)` / `private(set)` |
| test mechanism | `InternalsVisibleTo` | `@testable` |

**C#'s `internal` is a sound boundary** because an assembly is a real unit — better than Java's
package-private. Use it as the default for anything not meant to be public.

**Read the two two-word modifiers as set operations**, because they read alike and scope oppositely:

| Modifier | Logic | Scope |
|---|---|---|
| `protected internal` | **OR** | same assembly, or a derived class anywhere — **wider** |
| `private protected` | **AND** | same assembly, and a derived class — **narrower** |

**Seal library classes by default.** Microsoft's Framework Design Guidelines favour `sealed` for
library classes, because an unsealed public class is an extension contract whether you intended it
or not.

## The TypeScript side (Electron, Tauri front-ends, Tauri/Rust hosts)

**The erasure trap is the desktop-specific hazard**, because desktop apps ship their JavaScript.

```ts
class Settings {
  private apiToken = "…";        // erased at runtime; any renderer reads it
}
```

In Electron the consequence is concrete: **a `private` field is readable by any code in any
renderer**, and by anything the renderer loads — including a compromised dependency. `contextIsolation`
and a preload bridge do not change that, because the field was never private at runtime.

Use `#field` for anything that must actually hold:

```ts
class Settings {
  #apiToken = "…";               // enforced by the JS engine; unreachable
}
```

**Module privacy is achieved by not exporting**, and the exported set is the surface. Avoid
`export *` in a main-process or preload entry point, because it re-publishes everything the module
happens to import.

## The layer that is easy to miss: the IPC bridge

On desktop, a natively `private` or `internal` method exposed through an IPC bridge or a preload
`contextBridge` **becomes callable from the other side**, whatever the modifier says:

```ts
// preload.ts — whatever is listed here is the real surface, regardless of native modifiers
contextBridge.exposeInMainWorld("api", {
  readFile: (p: string) => ipcRenderer.invoke("read-file", p),
});
```

So the bridge's exposed list is a surface that needs the same review as a public API — and it is
frequently the widest surface in the product, because it was assembled by convenience.

## The desktop checklist

- [ ] C#: `internal` as the default for non-public types; `sealed` for library classes
- [ ] C#: `protected internal` and `private protected` read as OR and AND, never as synonyms
- [ ] C#: no public mutable fields; properties with non-public setters
- [ ] Swift: `internal` by default; `public` only at a framework boundary
- [ ] TypeScript: `#field` for anything that must hold at runtime; `private` treated as a hint only
- [ ] TypeScript: module privacy by not exporting; no `export *` in entry points
- [ ] The **IPC bridge / `contextBridge` exposed list** reviewed as a real surface
- [ ] No secret relies on a TypeScript `private`, a bridge, or `contextIsolation` for privacy
- [ ] Tests use `InternalsVisibleTo` / `@testable`; nothing widened to `public` for them
