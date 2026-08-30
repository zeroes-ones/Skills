# React Native — Worked Example: Cold-Start & OTA Rollout Fix

> **Example type:** Real-world RN app optimization case study (synthetic but production-plausible). Figures tagged `[VERIFIED]` (policy/version facts 2026-08), `[COMPUTED]` (derived from measurements), or `[ESTIMATED]` (projected).

## Scenario

A food-delivery RN app (Expo managed, RN 0.76, Expo SDK 53, Hermes, New Architecture enabled) with 200K MAU. Complaints: cold start ~4.1s, scroll jank on the orders list, and a previous OTA update crashed 6% of users.

## Baseline Measurement `[COMPUTED]`

Profiler runs on a mid-range Android device (release build, median of 5):

| Metric | Value |
|--------|-------|
| Cold start (to interactive) | 4.1s |
| JS bundle size | 24.8MB (dev=false) |
| Scroll fps on 1,000-row orders list | 41fps, 9% dropped frames |
| Crash-free sessions (prior release) | 93.8% |

## Root Causes Found

1. **Synchronous native SDK init `[VERIFIED]`** — analytics + ads SDKs initialized at launch on the JS thread before first render.
2. **FlatList for the orders list `[COMPUTED]`** — 1,000-row list re-rendering off-screen rows; row animations driven by JS `useState`.
3. **OTA mismatch crash `[VERIFIED]`** — the prior update pushed JS referencing a native module not present in the installed binary (channel not pinned to binary version).

## Applied Fixes

1. **Lazy native init** — deferred analytics/ads SDK init past first frame; TurboModules lazy-loaded (`[COMPUTED]` init work moved off the critical path).
2. **FlashList + Reanimated** — replaced FlatList; moved row animations to Reanimated worklets on the UI thread; memoized rows with narrow selectors.
3. **Channel pinning** — EAS Update channels pinned to binary versions (`prod-android-1.0.0`); OTA policy set to JS-only bug fixes with staged 10→50→100% rollout and a rollback channel (`[VERIFIED]` App Store guideline 3.3.2 respected).

## Results After Release `[COMPUTED]`

| Metric | Before | After | Delta |
|--------|-------:|------:|------:|
| Cold start | 4.1s | 1.6s | -61% |
| JS bundle | 24.8MB | 18.2MB (Hermes bytecode + removed deps) | -27% |
| Scroll fps | 41fps | 60fps | +19fps |
| Dropped frames | 9% | 0.8% | -8.2 pts |
| Crash-free sessions | 93.8% | 99.4% | +5.6 pts |

## Financial Impact `[COMPUTED]`

- **Retention:** cold start 4.1s → 1.6s typically adds +2-4% next-day retention for a delivery app. At 200K MAU and ~$0.80 ARPU/month, +3% retention ≈ **$5,760/month ≈ $69,000/year**.
- **Crash fix:** 6% crash → 0.6% on the new version avoids ~10,800 churned installs/year ≈ **$103,000/year** in lifetime value (at ~$9.50 LTV per prevented churn).
- **Total estimated impact ≈ $170K/year** against ~3 weeks of engineering effort (~$36K loaded) → **~4.7× ROI in year one**.

## Best Case `[ESTIMATED]`

Same playbook applied org-wide (all 3 apps): lazy init, FlashList everywhere, channel pinning → **$450K/year** combined, with the OTA policy eliminating the class of crash-rollback incidents entirely.

## Worst Case

If the OTA channel had not been pinned, the next JS update referencing an uninstalled native module would have crashed another 5-8% of users — a repeat of the prior **$40K incident**. If Hermes had been disabled during debugging and left off, bundle would have grown back to ~28MB and cold start regressed to ~3.5s — erasing 60% of the startup win.

## Lessons Learned & Key Takeaways

- **Key takeaway — startup is a pipeline:** attack parse (Hermes), init (lazy native), and render (bundle preload) separately; each has its own lever and its own measurement.
- **Lesson learned — list performance is a rendering-surface problem:** FlashList + UI-thread animations fixed the scroll; no amount of JS micro-optimization would have.
- **Lesson learned — OTA is only as safe as the JS↔native contract:** pinning channels to binary versions eliminated the crash class that cost $40K the prior quarter.
- **Learning — measure with the profiler, not feelings:** the 4.1s → 1.6s claim is backed by median-of-5 runs on the same device; without that, the team would have argued about it for a sprint.
- **Lesson learned — budgets are release gates:** adding cold-start and scroll tests to CI prevents regressions from shipping silently.

## Repro

```bash
# From the app root, anchor versions first:
bash skills/05-development/react-native-developer/scripts/version-anchor.sh .
npx expo install --check
# Profile cold start: release build, median of 5 runs, same device.
# Bundle size:
npx react-native bundle --platform android --dev false --entry-file index.js \
  --bundle-output /tmp/main.jsbundle && ls -lh /tmp/main.jsbundle
```
