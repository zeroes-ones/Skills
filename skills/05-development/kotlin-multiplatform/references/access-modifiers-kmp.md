# Access Modifiers — Kotlin Multiplatform

> Full model: `access-modifiers` → `references/kotlin.md`. Grounded in the Kotlin
> documentation, "Visibility modifiers".

KMP adds a layer the single-platform Kotlin guidance does not cover: a **shared module** whose
`internal` scope is the shared module, and `expect`/`actual` declarations that must agree on
visibility across the shared and platform sides.

## The unit, in a KMP project

```
shared/                       ← one module for Kotlin purposes
├── commonMain/               ← the shared code
├── androidMain/              ← the Android actual
└── iosMain/                  ← the iOS actual
```

`internal` in `commonMain` is visible throughout the **shared module** — including in the platform
source sets — and not to consumers of the module. That makes `internal` the natural default for shared
implementation, and it is generally the right level.

## Guidance specific to KMP

**1. `internal` in the shared module is the boundary — use it as the default.** Everything the
platform layers need can be `internal`; only what each platform's *consumers* need should be `public`.
The temptation is to make shared code `public` because the platform code must call it, which is
usually a mistake: `internal` already reaches the platform source sets of the same module.

**2. `public` in `commonMain` is a two-platform promise.** A public declaration in a shared module is
part of both the Android and the iOS surface. Any change to it breaks two consumers, and the Android
side carries the Java permeability caveat (below). Publish deliberately and keep the surface short.

**3. `expect`/`actual` visibility must be consistent.** The `actual` declaration cannot be *more*
visible than its `expect` counterpart where the compiler requires matching, so the `expect`
declaration's modifier is the effective ceiling for that member. Set the visibility on the `expect`
side and mirror it on the `actual`.

```kotlin
// commonMain
internal expect fun platformVersion(): String

// androidMain — same visibility
internal actual fun platformVersion(): String = Build.VERSION.RELEASE
```

**4. The Java permeability trap applies to the Android side of the shared module.** An `internal`
declaration in `commonMain` compiles to a public-with-mangled-name JVM symbol on Android, so **Java
code on the same classpath can reach it** — the same issue as single-platform Kotlin, with the extra
consequence that a shared-module internal is exposed on the Android artifact. Where that matters, keep
the declaration out of the Android artifact, or accept and document it.

**5. On the iOS side, the shared module's Kotlin `internal` is not an Objective-C/Swift boundary
either.** What the framework exposes to Swift is decided by the framework export configuration (the
`api`/framework naming rules), not by the Kotlin modifier. So a shared-module `internal` is *not*
automatically hidden from Swift — check the export configuration rather than assuming the modifier
covers both platforms.

## The shared-public decision

```text
Does each platform's CONSUMER need this?
├── No  → internal in commonMain (the default; reaches both platform source sets)
└── Yes → public in commonMain
    ├── it is a promise to BOTH the Android and the iOS surface
    ├── on Android, note the JVM/Java permeability of the compiled symbol
    ├── on iOS, confirm what the framework export configuration actually exposes
    └── add it to the surface list, which is now a two-platform contract
```

## Tests

The shared module's tests live in a test source set, so `internal` is reachable without widening —
`commonTest`, `androidTest`, `iosTest`. That is the mechanism; making a shared declaration `public` for
a test publishes it to both platforms' consumers.

## The KMP checklist

- [ ] `internal` is the default in `commonMain`; `public` is a deliberate, two-platform promise
- [ ] Platform source sets reach shared code via `internal`, not via widened visibility
- [ ] `expect`/`actual` visibility matches, with the ceiling set on the `expect` side
- [ ] Shared `internal` not assumed to be hidden from Java on the Android artifact
- [ ] Framework export configuration checked for what Swift actually sees on iOS
- [ ] The shared public surface published as an explicit list, understood as a two-platform contract
- [ ] Tests live in the test source sets (`commonTest`, `androidTest`, `iosTest`)
- [ ] No shared declaration widened to `public` so a test could reach it
