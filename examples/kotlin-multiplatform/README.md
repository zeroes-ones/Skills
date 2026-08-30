# Kotlin Multiplatform — Worked Example: Shared Auth + Data Layer

> **Example type:** Real-world KMP adoption case study (synthetic but production-plausible). Figures tagged `[VERIFIED]` (facts 2026-08), `[COMPUTED]` (derived from measurements), or `[ESTIMATED]` (projected).

## Scenario

A company with two mobile apps (Android, iOS) that duplicate auth, validation, and the profile data layer. Two separate codebases drift — a password rule change ships to Android and not iOS; the iOS team re-implements what Android already did. Decision: adopt KMP with a shared module for auth + profile data.

## Baseline `[COMPUTED]`

| Metric | Value |
|--------|-------|
| Duplicated business logic | ~11,500 lines (auth + validation + DTOs + repository) |
| Duplicate-bug incidents (12 months) | 7 (a fix shipped to one platform, not the other) |
| Estimated duplicate-implementation cost | 2 devs × ~6 weeks/year ≈ $36,000/year |
| iOS integration method | CocoaPods (legacy) |

## What Was Shared

1. **Auth domain** — models, token storage contract (expect), login/logout/refresh use cases.
2. **Validation** — password rules, email format, profile-field rules (pure logic).
3. **Data layer** — Ktor client + kotlinx.serialization DTOs + SQLDelight profile cache.

## Applied Changes `[VERIFIED]`

- Shared module with hierarchy template; 4 expect declarations (KeychainStore, network-status, device-id, date-provider).
- commonTest suite for auth flows and validation; run on both targets.
- iOS integration migrated CocoaPods → Swift Package Manager; CI builds the iOS consumer with a Swift smoke call.
- Concurrency: token store confined to a single dispatcher; Mutex-guarded refresh.

## Results After 2 Quarters `[COMPUTED]`

| Metric | Before | After | Delta |
|--------|-------:|------:|------:|
| Duplicated logic | 11,500 lines | ~900 lines (platform actuals + UI glue) | -92% |
| Duplicate-bug incidents | 7/year | 1 (UI-only) | -86% |
| Shared-test coverage | 0 | 320 commonTest cases on both targets | +320 |
| iOS binary size delta | — | +1.4MB | within budget |
| New-auth-feature delivery | ~2 weeks/platform | ~4 days (one implementation) | -70% |

## Financial Impact `[COMPUTED]`

- **Duplicate-logic retirement:** 2 devs × 6 weeks/year ≈ **$36,000/year** of re-implementation avoided.
- **Duplicate-bug prevention:** 6 fewer incidents/year × ~$4,000 avg remediation ≈ **$24,000/year**.
- **Feature velocity:** auth features land in days, not weeks — estimated **$18,000/year** in earlier release value.
- **Total ≈ $78,000/year** against ~8 dev-weeks of adoption effort (~$48K loaded) → **~1.6× ROI in year one, ~3.2× year two**.

## Best Case `[ESTIMATED]`

Extending the shared module to the payments domain and onboarding flow, plus Compose Multiplatform for two shared screens → **$160K/year** combined, with the iOS integration fully automated in CI.

## Worst Case

If the iOS export had been left unverified (no CI iOS build), the first Kotlin upgrade would have broken the framework link for the whole team — a **$12K-$18K outage**. If the token store had been shared without confinement, a concurrency crash would have hit both platforms — a **$20K incident** class. The adoption would have looked like a cost, not a saving.

## Lessons Learned & Key Takeaways

- **Key takeaway — bounded sharing wins:** sharing domains that change at a similar rate (auth, validation, data) retired real cost; forcing a UI rewrite would have failed.
- **Lesson learned — the iOS export is the fragile seam:** CI verification of the export + a Swift smoke call turned the riskiest part into a routine gate.
- **Lesson learned — expect surfaces stay small:** 4 deliberate expects instead of 20 convenience ones kept both platforms cheap to maintain.
- **Learning — measure the value:** share %, size delta, and duplicate-bug count turned "KMP is good" into a board-ready ROI number.
- **Lesson learned — concurrency is explicit now:** confining the token store and Mutex-guarding refresh prevented the new-memory-model crash class entirely.

## Repro

```bash
# From the KMP project root, anchor versions first:
bash skills/05-development/kotlin-multiplatform/scripts/version-anchor.sh .
# Run shared tests on both targets:
./gradlew :shared:testDebugUnitTest
./gradlew :shared:iosSimulatorArm64Test
# Verify the iOS export + smoke call in CI, then compare binary size per platform.
```
