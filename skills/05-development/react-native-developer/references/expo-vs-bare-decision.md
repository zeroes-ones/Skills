# Expo vs Bare React Native — Decision Worksheet

## The Decision Rule

**Default to Expo managed workflow (EAS Build + EAS Update + prebuild). Choose bare React Native only when a concrete native need cannot be expressed with Expo modules or config plugins.**

## Native-Needs Checklist

Fill this for every new app. If all rows are "Expo module/plugin", stay managed:

| Native need | Expo answer | Bare-required? |
|-------------|-------------|----------------|
| Push notifications | `expo-notifications` (FCM/APNs) | No |
| Biometrics / local auth | `expo-local-authentication` | No |
| Camera / image picker | `expo-camera`, `expo-image-picker` | No |
| Background tasks | `expo-background-task` / `expo-task-manager` | Sometimes (custom native bg service) |
| In-app purchases | `react-native-iap` (JS) or StoreKit native | Sometimes (advanced entitlements) |
| Custom native SDKs (payment, hardware, proprietary) | Config plugin may not exist | **Yes — bare or custom dev client module** |
| Existing native code in the repo | — | **Yes — bare** |
| Offline databases | `expo-sqlite`, WatermelonDB, SQLite | No |
| Video / audio playback | `expo-av`, `react-native-video` | No |

## Cost Model `[COMPUTED]`

| Factor | Expo managed | Bare RN |
|--------|-------------|---------|
| Initial setup | ~0.5 day (EAS handles builds/signing) | 2-4 days (native projects, signing, CI) |
| Native dep addition | Config plugin or prebuild | Manual pod/gradle integration + build config |
| RN upgrade | `npx expo install` aligned to SDK | Manual, breakage-prone, per-library |
| CI/CD | EAS Build/Update built-in | Fastlane + custom pipeline |
| Build toil | Low | High (maintainer burden per upgrade) |

**Example:** a 2-engineer team ships 2 apps/year. Bare adds ~5 engineering-days per app plus ~3 days/year upgrade toil per app. At $150/hr: **~$1,800-$2,400 extra per app-year** — typically 5-10× the cost of any Expo limitation.

## When to Go Bare (Documented Reasons)

1. Custom native SDK with no config plugin and no time to write one.
2. Heavy background/foreground services needing custom native lifecycle code.
3. Existing native codebase to integrate.
4. Team mandate for full native control (rare; usually a misdiagnosis).

## Migration Path

- Managed → Prebuild (`npx expo prebuild`) → modify native → keep config plugins where possible.
- Never eject casually: `expo prebuild` + development build keeps most managed benefits.
