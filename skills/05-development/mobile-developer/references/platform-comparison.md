---
author: Sandeep Kumar Penchala
title: "Native vs Cross-Platform: The Definitive Comparison"
date: 2026-07-21
---

## Decision Matrix (Score 1-5)

| Criterion | Native (Swift/Kotlin) | React Native (Fabric) | Flutter (Impeller) | PWA |
|---|---|---|---|---|
| **Cold start time** | 5 (<500ms) | 3 (1–2s) | 4 (500ms–1s) | 2 (2–3s URL load) |
| **60fps animation** | 5 (framework primitives) | 4 (Fabric direct mount) | 5 (Impeller pre-compiles shaders) | 3 (CSS/WAAPI, jank risk) |
| **Binary/install size** | 2 (~40MB+) | 3 (~15–25MB) | 3 (~15–20MB) | 5 (~0MB install) |
| **Memory baseline** | 4 (ARC, low idle) | 3 (JS VM overhead) | 3 (Dart VM + engine) | 2 (browser engine) |
| **Native API depth** | 5 (no abstraction) | 4 (TurboModules/NitroModules) | 4 (Platform Channels/FFI) | 1 (Web APIs only) |
| **Learning curve** | 2 (two languages, two SDKs) | 4 (JS/TS, one codebase) | 3 (Dart, one codebase) | 5 (standard web stack) |
| **Community maturity** | 5 (decades) | 5 (Meta-backed, large) | 4 (Google-backed, growing) | 5 (web ecosystem) |
| **Hiring pool size** | 4 (large, expensive) | 5 (JS devs abundant) | 3 (Dart niche, growing) | 5 (ubiquitous) |
| **Code sharing** | 1 (none across platforms) | 4 (~80% shared) | 4 (~85% shared) | 5 (~95% shared) |
| **OTA updates** | 1 (App Store only) | 2 (CodePush deprecated; EAS Updates) | 2 (shorebird/patrol) | 5 (instant deploy) |

### Composite Scores by App Type

#### GPU-Intensive Game
Weights: cold-start=0.05, animation=0.45, binary-size=0.10, memory=0.10, native-api=0.20, learning=0.02, community=0.02, hiring=0.02, sharing=0.02, ota=0.02

| Platform | Composite |
|---|---|
| **Native** | **4.65** (Metal/Vulkan direct access) |
| React Native | 3.75 (not designed for GPU workloads) |
| Flutter | 4.55 (Impeller compiles to Vulkan/Metal, no shader jank) |
| PWA | 2.10 (WebGL ceiling, no low-level GPU) |

#### Content-Heavy Social App
Weights: cold-start=0.20, animation=0.10, binary-size=0.05, memory=0.20, native-api=0.05, learning=0.10, community=0.10, hiring=0.10, sharing=0.08, ota=0.02

| Platform | Composite |
|---|---|
| Native | 4.02 (best perf, two teams cost) |
| **React Native** | **4.12** (strong list perf with FlatList/Fabric, JS hiring pool) |
| **Flutter** | **4.02** (same score, different tradeoffs) |
| PWA | 3.28 (service worker caching helps) |

#### Internal Enterprise Tool
Weights: cold-start=0.05, animation=0.02, binary-size=0.05, memory=0.05, native-api=0.05, learning=0.20, community=0.15, hiring=0.15, sharing=0.20, ota=0.08

| Platform | Composite |
|---|---|
| Native | 2.67 (overkill, expensive) |
| React Native | 3.85 (good JS ecosystem) |
| **Flutter** | **3.88** (fast UI iteration, one codebase) |
| **PWA** | **3.70** (zero install, instant deploy; if offline auth not needed) |

#### E-Commerce with Custom Animations
Weights: cold-start=0.15, animation=0.25, binary-size=0.05, memory=0.10, native-api=0.10, learning=0.10, community=0.10, hiring=0.05, sharing=0.05, ota=0.05

| Platform | Composite |
|---|---|
| Native | 4.45 (no animation ceiling) |
| React Native | 3.90 (Reanimated 3 + Fabric mitigates bridge) |
| **Flutter** | **4.35** (Impeller, no bridge, widget-level compositing) |
| PWA | 2.65 (scroll-linked animations unreliable) |

#### IoT Companion App
Weights: cold-start=0.10, animation=0.02, binary-size=0.05, memory=0.10, native-api=0.45, learning=0.08, community=0.05, hiring=0.05, sharing=0.05, ota=0.05

| Platform | Composite |
|---|---|
| **Native** | **4.65** (BLE/WiFi/NFC direct, background modes reliable) |
| React Native | 3.65 (BLE via `react-native-ble-plx`, background limits) |
| Flutter | 3.75 (Platform Channels for BLE, `flutter_blue_plus`) |
| PWA | 1.80 (Web Bluetooth limited, no Web NFC on iOS, no background) |

---

## Performance Deep Dive

### Cold Start: Frame-by-Frame Breakdown

| Frame | Native | React Native (Fabric) | Flutter (Impeller) | PWA |
|---|---|---|---|---|
| 0–16ms | Dyld loads binary, links @rpath frameworks | JS engine (Hermes) loads bytecode | Dart AOT snapshot mapped into memory | Browser process spawned |
| 16–32ms | +load methods, static initializers | Bridge/TM initialization, Metro bundle parse | Engine (Flutter.framework) initializes rasterizer | HTML parse, CSP check |
| 32–48ms | UIApplicationMain, AppDelegate | Fabric mounts root component, shadow tree build | PlatformView registration | CSSOM + Layout |
| 48–64ms | First UIViewController viewDidLoad | First Yoga layout pass → Fabric mount to native views | First widget build → RenderObject → Layer tree | JS bundle eval |
| 64–100ms | viewWillAppear → viewDidAppear (TTI) | TTI (40–80ms slower than native) | First frame rasterized by Impeller (no shader compile jank) | TTI ~2s (network-dependent) |

**Why native wins**: No VM startup. No bridge. Dyld optimizations (chained fixups, page-in linking) produce sub-400ms cold starts on recent devices. Swift's static dispatch on structs and final classes eliminates vtable overhead.

**What Fabric improves**: Direct mounting bypasses the JS→Native bridge for view operations. Shadow tree mutations apply in C++ (JSI) not JSON serialization. Hermes AOT compilation eliminates parse overhead. Result: ~15–20% faster cold start vs old architecture.

**Impeller architecture**: Pre-compiles shaders at build time (AOT), eliminating runtime shader compilation — the #1 source of Flutter jank on the old Skia pipeline. Uses a single-frame render pass with MSAA resolve. On Metal/iOS, tile-based deferred rendering maps cleanly to Impeller's render graph; on Vulkan/Android, render passes reuse command buffers. Frame budget: raster thread < 6ms typical.

### Animation Pipeline Comparison

```
NATIVE (UIKit/SwiftUI):
  Touch → UIEvent → CADisplayLink (16.67ms tick)
    → UIView.animate / SwiftUI Animation
    → Core Animation (render server, separate process)
    → GPU (RenderMetal, CAMetalLayer)
    → Display
  Key: UI events AND compositing happen on render server — main thread is free.

REACT NATIVE (Fabric):
  Touch → Native driver (Reanimated 3, worklet on UI thread)
    → Animated values flow to shadow tree (C++)
    → Fabric mounts mutated props directly to native views
    → Yoga layout only if dimensions change
    → Core Animation → GPU → Display
  Key: With Reanimated 3 worklets, animations run entirely on UI thread — never cross bridge.
  Without Reanimated: JS thread computes interpolated values → bridge serialization → native apply → jank at >30fps.

FLUTTER (Impeller):
  Touch → GestureArena → AnimationController (Ticker, vsync-bound)
    → Widget rebuild (Dart, on UI thread)
    → Element tree diff → RenderObject.markNeedsPaint
    → Layer tree → Impeller Aiks canvas → DisplayList
    → Impeller renderer (raster thread) → Metal/Vulkan → GPU → Display
  Key: Impeller pre-compiles shaders; raster thread always < 6ms. UI thread jank only if Dart code is heavy.

PWA:
  Touch → requestAnimationFrame → CSS transition/animation / WAAPI
    → Composite on compositor thread (if transform/opacity only)
    → Paint on main thread (if layout-triggering properties)
    → GPU raster → Display
  Key: Only transform & opacity are compositor-only. Any layout-change animation forces main-thread paint → jank.
```

### Garbage Collection Models

| Framework | Model | Pause time | Memory overhead | Notes |
|---|---|---|---|---|
| **Swift** | ARC (compile-time retain/release) | 0ms (no GC pauses) | ~5% overhead (refcounts) | Cycle detection via `weak`/`unowned`; no tracing, deterministic dealloc |
| **Kotlin/JVM (Android)** | ART concurrent copying GC | <1ms minor, 2–5ms major | ~15–20% overhead | Generational: young (TLAB allocation) + old generation; concurrent mark + compact |
| **Hermes (RN)** | Generational, non-moving, concurrent mark | <2ms (incremental) | ~10% overhead | No stop-the-world full GC; young gen (32KB) collected frequently; old gen mark-sweep concurrent |
| **Dart VM (Flutter)** | Generational, parallel mark, concurrent sweep | <1ms minor, 1–3ms major | ~15% overhead | Two generations: new-space (scavenge, Cheney semi-space) and old-space (mark-sweep); bump-pointer allocation in new-space |
| **V8/WebKit (PWA)** | Orinoco (V8) / Bmalloc (JSC) — concurrent + parallel | 1–5ms | ~20–25% overhead | Full browser overhead includes DOM, CSSOM, layout trees |

### Binary Size Breakdown

```
NATIVE iOS (.ipa, uncompressed):
  ├── Executable (Mach-O):        8–15MB   (Swift stdlib embedded, no ABI stability pre-iOS 12.2)
  ├── Frameworks (embedded):      20–30MB  (3rd-party .frameworks per target)
  ├── Assets.car (compiled):      5–15MB   (images, colors, data)
  ├── Localization (.lproj):      1–3MB
  ├── SwiftUI/Combine overhead:   3–5MB    (if used)
  └── Total: ~40–70MB

REACT NATIVE (.apk/.ipa):
  ├── Hermes bytecode bundle:     2–5MB    (precompiled JS)
  ├── Native libs (.so/.dylib):   8–12MB   (Hermes, Yoga, Fabric, TurboModules)
  ├── JS bundle (Metro):          1–3MB    (minified, not tree-shaken as aggressively)
  ├── Assets:                     2–10MB
  ├── Frame overhead:             3–5MB    (React Native framework)
  └── Total: ~15–35MB

FLUTTER (.ipa/.apk):
  ├── App (.app/.aab):            3–8MB    (Dart AOT compiled)
  ├── Flutter engine:             8–12MB   (libFlutter.so/Flutter.framework, Impeller, ICU, Skia fallback)
  ├── Assets:                     2–8MB
  ├── Platform plugins:           2–5MB    (per native plugin .framework/.so)
  └── Total: ~15–33MB

PWA:
  ├── HTML+CSS+JS (cache):        0.5–3MB  (service worker cached)
  ├── App shell:                  0.2–1MB
  ├── Assets (IDB/cache):         variable
  ├── Install size:               ~0MB (just the URL, no store download)
  └── Total: ~0MB initial, ~2–5MB after full cache
```

---

## When Each Option Fails (Anti-Patterns)

### Native (Swift + Kotlin)
- **Two full teams, two codebases**: If your budget supports only one team, feature drift is inevitable. iOS gets feature X in v2.3; Android gets it in v2.7. Users notice.
- **Iteration speed**: No OTA. Every bug fix = App Store review (24–48h avg). Critical hotfix takes days, not hours.
- **Sharing business logic**: Shared Kotlin Multiplatform layer helps, but networking, models, validation all duplicated unless you invest in KMP/Swift-Kotwin. Adds build complexity.
- **Overkill for**: Simple CRUD apps, internal tools, prototypes, apps with <100K users and no performance-sensitive features.

### React Native
- **Bridge saturation at high throughput**: Even with Fabric's JSI, serializing 100+ events/sec (gyroscope at 100Hz, real-time BLE data streams) can drop frames. Use TurboModules + C++ for hot paths.
- **Complex gesture handling**: Nested gesture responders (pan inside scroll inside swipe) require manual `GestureDetector` + `NativeGesture` composition. Panresponder conflicts are the #1 source of RN gesture bugs.
- **Background processing limits**: iOS background task expiration (30s) applies. No long-running services. Use native modules (`BGTaskScheduler`) for anything beyond a few seconds.
- **Large lists with heterogeneous cells**: Even with `FlashList` or `FlatList` optimization, 500+ complex cells with images will stutter. Virtualization with `recycle` helps but RecyclerView/UICollectionView are still 2–3x more efficient.
- **Anti-pattern**: RN-only shop building a camera app, real-time audio processing, or AR — use native for these surfaces.

### Flutter
- **Platform feel mismatch**: Material widgets on iOS look off. Cupertino widgets cover ~80% of iOS HIG — the remaining 20% (large titles collapsing to inline, search controller behavior, context menus, haptic patterns) need manual `Theme` customization or native Platform Views.
- **Large binary for simple apps**: A "Hello World" Flutter app is ~12MB. For simple utility apps, this is excessive vs a 3MB SwiftUI app.
- **Dart ecosystem smaller than JS**: Fewer libraries. No Express/Fastify equivalent. Server-side Dart is niche. Tooling (linters, code generators) less mature than JS ecosystem.
- **Text editing**: Selection handles, autocorrect, text input delegate behavior — Flutter's custom text field can't perfectly replicate native text interaction. Avoid for document-editing-heavy apps.
- **Anti-pattern**: Apps that need zero platform friction (e.g., an Apple Design Award contender), document editors, or apps with <5 screens where native would take 2 weeks.

### PWA
- **No push notifications on iOS** (as of iOS 18+ Web Push is available but limited: no silent push, no rich media in notification, user must add-to-homescreen first, no notification grouping). Android Web Push works but has lower reliability than FCM.
- **No background sync**: `Background Sync` API not supported on iOS Safari. No periodic background sync. Offline-first is possible (SW caching) but sync-on-reconnect is unreliable.
- **No Bluetooth/NFC**: Web Bluetooth on Chrome only. Web NFC only on Chrome Android. Zero support on iOS Safari for either.
- **Cold start is URL load**: Every cold start = re-fetching the app shell, even with aggressive SW caching. No splash screen API on iOS (can hack with a static image in manifest, but no programmatic control).
- **iOS storage eviction**: iOS may evict IndexedDB and SW cache under storage pressure with no warning. No persistent storage guarantee.
- **Anti-pattern**: Any app needing hardware access (BLE, NFC, AR), background execution, iOS notifications, or a premium "native-feel" experience.

---

## Migration Considerations

### React Native → Native Modules (Fabric / New Architecture)
```
Gradual path:
  1. Enable New Architecture (RCT_NEW_ARCH_ENABLED=1 in Podfile)
  2. Convert JS-native bridges to TurboModules (C++ JSI, no JSON serialization):
     - Implement <ModuleName> spec in JS (NativeModule spec)
     - Generate C++ host object via Codegen
     - Implement ObjC/Kotlin delegate, expose to JSI
  3. Replace `<NativeComponent>` with Fabric Native Components:
     - Define ComponentDescriptor in C++
     - Implement ShadowNode for layout
     - Mount directly via Fabric's SurfaceMountingManager
  4. Migrate animated components to Reanimated 3 worklets
  5. Profile: if a particular screen remains janky → rewrite entirely in native,
     embed via RCTRootView or present as native UIViewController.

Do NOT: rewrite entire app at once. Attack one screen per sprint.
```

### Native → Flutter (Add-to-App)
```
Incremental integration:
  1. Create Flutter module (flutter create --template module flutter_module)
  2. iOS: embed via FlutterViewController presented modally,
     or use FlutterEngine with a FlutterMethodChannel for bi-directional comm
  3. Android: embed via FlutterFragment or FlutterActivity;
     use FlutterEngineGroup for shared engine (reduces memory: one engine, multiple isolates)
  4. Share data: Pigeon codegen for type-safe Platform Channels
  5. Route management: Use a shared Navigator key; native side pushes named routes
     into Flutter via MethodChannel or FlutterEngine's platformDispatcher

When to add native screens to a Flutter app:
  - Camera viewfinder (Platform View or native UIViewController)
  - Map with 1000+ annotations (native MKMapView/Google Maps SDK)
  - Payment sheet (Apple Pay modal, Stripe native SDK)
  - Document scanning (VisionKit/VNDocumentCameraViewController)

When NOT to go add-to-app:
  - App is <10 screens and fully native — just stay native
  - Heavy interop between host and Flutter — each channel call is ~0.1ms;
    1000 calls/frame will blow budget
  - Teams are separate (iOS + Android) → Flutter requires Dart fluency across both
```

### Cross-Platform Fallback Strategy
When a cross-platform framework can't deliver a feature:
1. **Isolate the feature** — build as a native module/screen, not interleaved
2. **Use Platform Views sparingly** — each Platform View creates a new `UIView`/`View` that composites as a texture; >3 Platform Views visible simultaneously degrades scroll performance in both RN and Flutter
3. **Pattern**: Cross-platform for 80% (lists, forms, navigation), native for 20% (camera, maps, BLE, AR, complex animations). This ratio is sustainable; the inverse (80% native, 20% cross-platform) is not — you're fighting the framework.
