# Flutter — Worked Example: Jank, Startup, and Channel Fix

> **Example type:** Real-world Flutter app optimization case study (synthetic but production-plausible). Figures tagged `[VERIFIED]` (facts 2026-08), `[COMPUTED]` (derived from measurements), or `[ESTIMATED]` (projected).

## Scenario

A field-service dispatch app (Flutter, 3.x stable / Dart 3.x, Riverpod, Bloc for the dispatch module) with 90K MAU on iOS + Android. Complaints: scroll jank on the jobs list, 3.2s cold start, and intermittent login crashes on Android.

## Baseline Measurement `[COMPUTED]`

DevTools profiling on a mid-range Android device (release build, median of 5):

| Metric | Value |
|--------|-------|
| Jank (dropped frames, 30s scroll) | 14% |
| Cold start (to first frame) | 3.2s |
| APK size | 68MB |
| Crash-free sessions | 97.1% |

## Root Causes Found

1. **Heavy build() in the jobs list `[COMPUTED]`** — a 300-line row widget rebuilt eagerly; no const; eager `ListView` children.
2. **Blocking JSON parse on the UI isolate `[COMPUTED]`** — 3MB of job data parsed synchronously in a provider's initializer at startup.
3. **Untyped MethodChannel for login `[VERIFIED]`** — hand-rolled channel with a channel-name mismatch on the Android side → intermittent `MissingPluginException`.

## Applied Fixes

1. **Cheap widgets** — split the row into small const widgets, `ListView.builder`, `RepaintBoundary` around the map thumbnail.
2. **Isolate offload** — `Isolate.run` for the job-data parse; skeleton loading state while parsing.
3. **Pigeon contract for login** — generated typed interface for the auth channel; error paths; thread-correct native side.

## Results After Release `[COMPUTED]`

| Metric | Before | After | Delta |
|--------|-------:|------:|------:|
| Jank (dropped frames) | 14% | 0.9% | -13.1 pts |
| Cold start | 3.2s | 1.4s | -56% |
| APK size | 68MB | 51MB (split-per-abi + tree-shake) | -25% |
| Crash-free sessions | 97.1% | 99.6% | +2.5 pts |

## Financial Impact `[COMPUTED]`

- **Retention:** jank fix + faster start typically adds +3-5% next-day retention for a field workforce app. At 90K MAU and ~$1.10 ARPU/month, +4% ≈ **$3,960/month ≈ $47,500/year**.
- **Crash fix:** the login crash (~2.9% crash rate) cost ~2,600 churned users/year at ~$12 LTV ≈ **$31,000/year**.
- **Total estimated impact ≈ $78K/year** against ~2.5 weeks of effort (~$30K loaded) → **~2.6× ROI in year one**.

## Best Case `[ESTIMATED]`

Applying the same playbook (cheap widgets, isolate offload, typed channels) across the org's 4 Flutter apps → **$210K/year** combined, with untyped-channel incidents eliminated entirely.

## Worst Case

If the login channel had shipped untyped again, the `MissingPluginException` crash class would persist — another **$9K/incident** plus rating decay. If the isolate offload had been skipped, cold start would have stayed ~3s and the retention win would shrink by ~60%.

## Lessons Learned & Key Takeaways

- **Key takeaway — jank is a build problem, not a device problem:** the profiler named the row widget; const + lazy lists fixed the frames. No device upgrade would have.
- **Lesson learned — parse off the UI isolate:** a 3MB JSON parse on the UI isolate froze startup on slow devices; `Isolate.run` cut cold start by more than half.
- **Lesson learned — typed channels are the fix for the crash class:** pigeon eliminated the channel-name typo that crashed login; error paths turned a crash into a handled message.
- **Learning — measure with DevTools, not feelings:** every claim here is median-of-5 on the same device; without that, the team would have argued about jank for a sprint.
- **Lesson learned — release gates prevent regressions:** adding jank and startup checks to CI stops silent regressions from shipping.

## Repro

```bash
# From the app root, anchor versions first:
bash skills/05-development/flutter-developer/scripts/version-anchor.sh .
flutter pub outdated
# Profile frames with the Performance overlay (release build, same device, 30s scroll).
# Startup: 5 runs, median cold start to first frame.
# Size:
flutter build apk --release --split-per-abi --tree-shake-icons --report-sizes
```
