# Performance Optimization — Cold Start, Size, 60fps

## The Three Budgets

| Budget | Target | Measured how |
|--------|--------|--------------|
| Cold start | < 2s to interactive | Xcode Instruments / Android Studio Profiler, cold launch |
| App size | Within store budget (250MB universal) and product budget | `npx react-native bundle --dev false` size report + native binary size |
| Scroll frame rate | 60fps (16ms/frame budget) | React DevTools Profiler + Reanimated profiler / Systrace |

## Cold Start Levers (in order of ROI)

1. **Hermes bytecode** — faster parse and smaller bundle; keep enabled (default).
2. **Bundle preloading** — preload the JS bundle on the native side at splash; `expo-splash-screen` with `preventAutoHideAsync`.
3. **Lazy TurboModules** — defer non-critical native SDKs; init them after first frame.
4. **Trim the initial route graph** — lazy routes (`React.lazy`/Expo Router `Suspense`); don't mount the whole tab stack at launch.
5. **Reduce native init work** — move analytics/ads/crash SDK init off the critical path.

## Size Levers

1. **Audit with Metro size reports** — find the heaviest modules; replace or lazy-load.
2. **Remove unused native deps** — every pod/gradle module adds binary size; `expo install` only what you use.
3. **Compress assets** — images to WebP, audio/video to compressed formats; serve heavy media from a CDN, not the bundle.
4. **Hermes bytecode + minification** — enable `production` Metro config (minify, bytecode).

## 60fps Levers

1. **FlashList for lists** — recycling + viewability; FlatList re-renders off-screen rows.
2. **Reanimated worklets on the UI thread** — never JS `useState`-driven animation in a scroll path.
3. **`memo` + selectors** — stop re-rendering list rows on parent state changes.
4. **InteractionManager / `requestAnimationFrame`** — defer non-critical work past the first frame.
5. **Profile, don't guess** — React DevTools Profiler for renders; Instruments/Profiler for native.

## The Scroll Test (Release Gate)

A 1000-row list, scroll programmatically for 30s, measure dropped frames. Regression above 2% dropped frames blocks release (Best Practice 9).

## Profiler Protocol

- Cold start: 5 runs, take the median, same device/OS, release build, no debugger.
- Frame rate: same device, 30s scroll, record fps + dropped frames.
- Size: report JS bundle (dev false) + native binary (ipa/app size) per platform.
