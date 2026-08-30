# Performance Optimization — Frames, Startup, Size

## The Three Budgets

| Budget | Target | Measured how |
|--------|--------|--------------|
| Frame rate | 60fps (16ms/frame), jank < 1% dropped frames | Flutter DevTools Performance overlay, `SchedulerBinding` frame timing |
| Cold start | < 2s to first frame on a mid-range device | `flutter run --profile` / native launch timing |
| App size | Within store limits and product budget | `flutter build apk --release --report-sizes` / IPA size |

## Frame-Time Levers (in order of ROI)

1. **Cheap builds** — const widgets, small focused widgets, no work in build().
2. **Lazy lists** — `ListView.builder`/`SliverList`; never eager 1,000-item lists.
3. **RepaintBoundary** — isolate expensive paints (maps, videos, gradients).
4. **Isolate offload** — heavy computation/parsing to `Isolate.run`.
5. **Avoid `Opacity`/shadows over large areas** — use `Color` with alpha or pre-blurred assets.
6. **Texture/PlatformView judiciously** — they're expensive; batch and bound them.

## Startup Levers

1. **AOT release build** — debug/JIT startup is 3-5× slower; always measure release.
2. **Defer non-critical initialization** — lazy singleton providers, defer analytics/ads init.
3. **Tree-shake icons + slim plugins** — remove unused plugin registrations.
4. **Splash screen strategy** — native splash → first frame; avoid long Flutter-side splash.

## Size Levers

1. **`--split-per-abi`** (Android) — split APKs per ABI; big win on 64-bit-only devices.
2. **Tree-shake icons** — `--tree-shake-icons` removes unused Material icons.
3. **Obfuscation + `--split-debug-info`** — smaller release and separable debug symbols.
4. **Asset hygiene** — compressed images (WebP), no unused assets; serve heavy media from a CDN.
5. **Audit plugins** — each plugin adds native code; remove unused ones.

## The Profiler Protocol

- Same device, same OS, release build, no debugger.
- Frames: 30s of representative scrolling; record fps + dropped frames.
- Startup: 5 runs, median cold start.
- Memory: Memory profiler over a 10-minute session; look for monotonic growth (leaks).

## Release Gate

Jank < 1% dropped frames; cold start within budget; size within limits. A regression blocks release — "we'll fix it next sprint" is not a plan.
