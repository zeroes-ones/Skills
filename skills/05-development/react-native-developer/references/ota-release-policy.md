# OTA and Release Policy — EAS Update, CodePush, App Store Compliance

## The Policy in One Line

**OTA ships JS-only bug fixes and metadata. Native dependencies and significant feature changes ship through store review.**

## Why (App Store Guideline 3.3.2) `[VERIFIED 2026-08]`

Apple restricts apps from downloading or installing executable code. JS-only updates via EAS Update/CodePush-style mechanisms are tolerated in practice for bug fixes, but pushing a visible feature change or anything that alters the app's primary behavior risks rejection, removal, and a review ban.

## Channel Architecture

Pin OTA channels to native build versions:

```
channel "prod-ios-1.0.0"  → binary version 1.0.0
channel "prod-android-1.0.0" → binary version 1.0.0
```

**Never push JS that depends on native code not in the installed binary** — that mismatch is the #1 OTA crash cause (Error Decoder row 1).

## Staged Rollout

1. **10%** → monitor crash-free sessions, E2E smoke, and the top-5 screens.
2. **50%** → monitor again for 12-24h.
3. **100%** → full rollout; keep the rollback channel live.
4. **Rollback** — one command to point the channel back to the previous bundle.

## What Goes Where

| Change | Channel |
|--------|---------|
| JS-only bug fix (no native dep, no visible feature change) | OTA (staged) |
| New native dependency | Store review (both platforms) |
| Visible feature change | Store review |
| Design/metadata tweaks | OTA (metadata is not executable behavior) |
| Crash hotfix while store review is pending | OTA (documented, minimal) |

## Code Signing & Distribution (EAS/Fastlane)

- **EAS Build** — managed builds + signing with credentials stored in EAS; `eas build --profile production`.
- **Fastlane (bare)** — `match` for certificates/provisioning; store upload via `fastlane deliver`/`pilot`.
- Secrets never in the repo — use EAS secrets or CI secret store.
- Both stores need: app icon/splash (from config), privacy policy URL, test accounts for review.

## Monitoring After Release

- Crash-free sessions per version (Sentry/BugSnag/Firebase Crashlytics).
- OTA update success rate per channel.
- Rollout health gates: crash delta > 0.5% → pause and roll back.
