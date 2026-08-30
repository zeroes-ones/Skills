# iOS Interop — Framework Export, CocoaPods/SPM, Swift Bridging

> `[VERIFIED 2026-08]` — JetBrains recommends Swift Package Manager as the modern integration; verify against the installed Kotlin version (RP1).

## Three Integration Methods

| Method | When | How |
|--------|------|-----|
| **Swift Package Manager** | Modern, CI-friendly | Export a framework via the SPM integration; add it as a local package dependency in Xcode |
| **CocoaPods** | CocoaPods already in the project | `podspec` + Gradle sync (`./gradlew syncFramework`); `pod install` after sync |
| **Direct framework** | Full control | `linkDebugFrameworkIosSimulatorArm64` etc.; embed via an Xcode build phase |

## The Export Contract

1. The framework must **export** (`./gradlew :shared:linkDebugFrameworkIosSimulatorArm64` and device variants).
2. The iOS app must **link** the framework.
3. A **smoke Swift call** must compile and run (one shared function, one shared model).
4. CI verifies all three on every change — never discovered at release.

## Swift Bridging Rules

- **Nullability** — Kotlin nullable types map to Swift optionals; non-null maps to non-optional. Mismatches crash at runtime.
- **Callbacks** — suspend functions export as completion-handler/async functions; understand the generated signature.
- **Error mapping** — Kotlin exceptions cross as `NSError`/`Error`; map them deliberately on the Swift side.
- **Threading** — shared calls return on their own dispatcher; bridge to the main thread in Swift when updating UI.
- **Models** — Kotlin data classes export as Swift structs/classes; keep the surface stable (see source-set-design.md).

## Common Failures

| Failure | Fix |
|---------|-----|
| "framework not found" | Sync order: Gradle export before `pod install`/SPM resolution; clean both |
| Min-version mismatch | Align the iOS deployment target in Gradle and Xcode |
| Nullability crash | Fix the Kotlin nullability annotation / Swift optional handling |
| Missing bitcode/architectures | Export all needed architectures (device + simulator for CI) |
| CocoaPods name conflict | Rename the framework; check other pods for the same name |

## Migration Path

CocoaPods → SPM: create the SPM integration, verify the smoke call, remove the podspec, update CI. Do it in a dedicated PR with the iOS consumer build in CI.
