# Version Matrix Reference — Flutter/Dart Compatibility

> `[VERIFIED 2026-08]` — verify against the installed SDK at research time (RP1). Flutter ships stable ~quarterly; Dart majors advance alongside.

## The Compatibility Contract

- **Flutter ↔ Dart** are released together — a Flutter version pins a Dart SDK. Never mix a mismatched pair.
- **Packages** declare SDK constraints in pubspec (`sdk: ^3.x`); `flutter pub outdated` surfaces drift.
- **Plugins** are pinned to Flutter versions; a Flutter upgrade can break plugins with native code.
- **iOS/Android minimums** — Flutter sets minimum OS targets per release; verify the app still covers your supported floor.

## Commands That Anchor You

```bash
flutter --version          # Flutter + Dart versions
flutter doctor             # environment health
flutter pub outdated       # dependency drift
dart pub outdated          # Dart-only deps
flutter analyze            # static analysis gate
```

## Upgrade Protocol

1. Read the release notes / migration guide for the target version (breaking changes, deprecations).
2. Check plugin compatibility (`pub outdated` + pub.dev compat badges).
3. Upgrade Flutter SDK + all packages as one unit; run `flutter pub get`.
4. Run `flutter analyze` + the full test matrix on both platforms.
5. Rollback path: keep the previous SDK/package pins; a failed upgrade reverts cleanly.

## Rules That Save Builds

- **Pin packages** — never unversioned git deps or `any` constraints in production.
- **One source of truth** — pubspec.yaml + pubspec.lock are the contract; never hand-edit `.dart_tool`.
- **Verify after any add** — `flutter pub outdated` after adding a package; a mismatch breaks the build.
- **Pin the CI Flutter version** — CI and local must use the same Flutter SDK (use `fvm` or a pinned Docker image).

## Impeller Note

- Impeller is the default renderer on modern Flutter (replacing Skia). It fixes classic Skia jank but has its own edge cases (certain shaders/effects).
- Verify rendering with the Performance overlay; if a visual regression appears, check Impeller issues before "fixing" app code.
