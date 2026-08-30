# Compose Multiplatform — Shared UI Strategy

> `[VERIFIED 2026-08]` — Compose Multiplatform is stable for iOS but has a smaller ecosystem than platform-native UI. Verify maturity for your specific needs (RP1).

## When to Use Compose Multiplatform for UI

| Situation | Verdict |
|-----------|---------|
| Shared business logic + shared simple-to-medium UI | Strong fit — one UI codebase for both platforms |
| Pixel-identical custom design | Good — Compose renders its own UI |
| Heavy platform-idiomatic UI (HIG/Material native components, complex platform gestures) | Consider platform UI + shared logic instead |
| Mature ecosystem dependency (native payment sheets, complex maps) | Verify library support before committing |

## Architecture

- **Shared UI in commonMain** — Compose Multiplatform code with the same composable model as Android Jetpack Compose.
- **Platform UI optional** — for apps that keep native UI, share only the logic layer (the default KMP approach).
- **Navigation** — shared navigation (e.g., the multiplatform navigation library or a shared ViewModel + platform navigation).

## Practical Notes

- iOS rendering is Metal-backed via Skia; verify custom effects on device (not just simulator).
- Fonts, text input, and clipboard behave differently per platform — test the real flows.
- Keep platform-specific composables behind expect/actual or platform modules.
- Reuse the shared data layer + coroutines patterns from `shared-data-layer.md` — the ViewModel layer is where Compose and logic meet.

## Migration Path

Start with **shared logic only** (low risk), add Compose Multiplatform for new screens, and migrate screens incrementally — never rewrite the whole UI at once.

## Test Strategy

- commonTest for ViewModels and logic (as in testing-shared-logic.md).
- Compose UI tests in commonTest where the framework supports them; platform tests for platform-specific UI behavior.
- Verify on real devices — simulator rendering can hide iOS-specific issues.
