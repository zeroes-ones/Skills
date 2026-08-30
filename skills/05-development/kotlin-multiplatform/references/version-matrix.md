# Version Matrix Reference — Kotlin/Gradle/kotlinx Compatibility

> `[VERIFIED 2026-08]` — verify against the installed toolchain at research time (RP1). Kotlin releases ~every 6 months; kotlinx libraries track it.

## The Compatibility Contract

- **Kotlin ↔ kotlinx libraries** — kotlinx (coroutines, serialization, datetime) releases align with Kotlin versions; a mismatch breaks compilation.
- **Kotlin ↔ Gradle** — the Kotlin Gradle plugin requires a minimum Gradle version; check the compatibility table.
- **Kotlin/Native ↔ Xcode** — Kotlin/Native supports a range of Xcode versions; an unsupported Xcode breaks the iOS export.
- **KMP ↔ libraries** — Ktor, SQLDelight, and others pin Kotlin versions; check each library's compatibility.

## Commands That Anchor You

```bash
./gradlew --version                 # Gradle + JVM
./gradlew :shared:kotlinToolchainVersion   # Kotlin toolchain
./gradlew :shared:dependencies      # dependency tree + versions
# Version catalog:
cat gradle/libs.versions.toml
```

## Upgrade Protocol

1. Read the Kotlin release notes + migration guide for the target version.
2. Check kotlinx/library compatibility (version catalog + each library's docs).
3. Verify the iOS export still builds (Xcode compat) BEFORE merging.
4. Upgrade the toolchain + libraries as one unit; run the full test matrix on all targets.
5. Rollback path: keep previous versions pinned; a failed upgrade reverts cleanly.

## Rules That Save Builds

- **Version catalog is the single source of truth** — no ad-hoc versions in build files.
- **Pin everything** — Kotlin, Gradle wrapper, Xcode, JDK; CI matches local.
- **Never mix Kotlin majors** — a Kotlin 1.x and 2.x dependency mix breaks compilation.
- **Verify after any change** — a new kotlinx library must match the installed Kotlin.

## The Fragile Seam

The iOS export is the most version-sensitive part: Kotlin/Native, Xcode, and the export config must align. Any version change gets an iOS CI build before merge (Ground Rule R5).
