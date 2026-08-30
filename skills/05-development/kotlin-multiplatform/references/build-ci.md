# Build & CI — Gradle Config, Targets, Size Control

## The Shared Module Gradle Config (Shape)

```kotlin
kotlin {
    androidTarget()
    listOf(iosArm64(), iosSimulatorArm64(), iosX64()).forEach {
        it.binaries.framework { baseName = "Shared"; isStatic = true }
    }
    sourceSets { ... }
}
```

- **Targets:** declare only what you ship. Every target adds compile + CI cost and binary size surface.
- **Framework:** `isStatic = true` (static framework) is the common choice; dynamic when needed.
- **Version catalog** (`libs.versions.toml`) is the source of truth for Kotlin/Gradle/library versions.

## CI Matrix (Minimum)

| Job | Covers |
|-----|--------|
| Android compile + unit tests | `./gradlew :shared:testDebugUnitTest` |
| iOS targets compile | `linkDebugFrameworkIosSimulatorArm64` + device variant |
| commonTest on all targets | `./gradlew :shared:allTests` (or per-target test tasks) |
| iOS consumer build | `xcodebuild` of the iOS app (smoke interop) |
| Size delta report | Compare binary size per platform against the baseline |

Pin CI to the exact Kotlin/Gradle/Xcode versions (Gradle wrapper, toolchain, Xcode). "Works locally, fails in CI" is a version-mismatch symptom.

## Size Control

- **Trim targets** — fewer targets = less surface.
- **Link options** — Kotlin/Native dead-code elimination; `isStatic` vs dynamic framework.
- **Library discipline** — each kotlinx/library adds size; audit what you actually use.
- **Measure per module** — record the size delta when adding a shared module; keep the tax within budget.

## Common Build Failures

| Failure | Fix |
|---------|-----|
| "Unresolved reference" after a version change | `./gradlew clean` + sync; check the version catalog |
| iOS target not found | Check the declared targets; regenerate the export |
| CI and local disagree | Pin Gradle wrapper + Xcode; use the same JDK/toolchain |
| Binary size regression | Audit targets + libraries; size delta gate in CI |
