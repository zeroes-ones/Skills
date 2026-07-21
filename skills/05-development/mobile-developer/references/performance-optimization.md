---
title: "Mobile Performance Optimization: The Complete Playbook"
author: Sandeep Kumar Penchala
date: 2026-07-21
---

## Startup Time

**Target**: Cold start < 1.5 seconds on a low-end device (iPhone SE, Samsung A-series). Not warm start. Not on a flagship.

### The Startup Timeline

```
┌───────────── PRE-MAIN ─────────────┐── MAIN ────────────┐── POST-RENDER ──┐
│ dyld load → static init → +load    │ UI setup → 1st frame│ data → hydrate  │
│ 0ms                         400ms  │ 400ms        800ms  │ 800ms   1500ms  │
└────────────────────────────────────┴─────────────────────┴─────────────────┘
```

### iOS: Pre-Main Optimization

**What happens before `main()`:**
1. `dyld` (dynamic linker) loads all dylibs — each dylib adds ~20ms on a cold start
2. Rebase/bind: fix up pointers across dylibs (~100ms baseline)
3. ObjC runtime: register classes, categories, selectors
4. `+load` methods: every `+load` blocks the main thread during startup

**Optimizations:**
- **Reduce dylib count**: Merge frameworks. Each dylib costs. Target < 6 dynamic frameworks in your app. Use static linking for internal frameworks (`MACH_O_TYPE = staticlib`).
- **Audit `+load`**: Replace with `+initialize` (lazy, called on first use) or `dispatch_once`. Run `otool -oV <binary> | grep "_class_ro_t"` to list all classes with `+load`.
- **No static initializers**: In Swift, global/static `let` with complex initializers run at startup. Audit with `__attribute__((constructor))` detection: `nm -gU <binary> | grep "mod_init_func"`.
- **Dyld3 closure**: iOS 13+ pre-computes dyld info. Ensure bitcode-like pre-warming by shipping from App Store (not ad-hoc distribution).
- **Measure**: Set `DYLD_PRINT_STATISTICS=1` env var in Xcode scheme → logs exact pre-main time breakdown.

### Android: Application.onCreate Minimization

**What happens before first frame:**
1. `Application.attachBaseContext()`
2. `ContentProvider.onCreate()` — **all of them**, across your app and all SDKs
3. `Application.onCreate()`
4. First Activity `onCreate()` → `onStart()` → `onResume()` → first draw

**Optimizations:**
- **Lazy ContentProviders**: Use `androidx.startup` (App Startup library). Set `<provider android:initOrder="-1" />` to deprioritize non-critical providers. Never initialize analytics, crash reporters, or ad SDKs in a ContentProvider.
- **Minimize `Application.onCreate()`**: Defer to background thread:
  ```kotlin
  override fun onCreate() {
      super.onCreate()
      // Only UI-critical init here
      if (Process.isApplicationCrashedRecently(this)) return  // skip if crash loop
      CoroutineScope(Dispatchers.Default).launch {
          initializeNonCriticalSdks()
      }
  }
  ```
- **Lazy init stable libraries**: Firebase, WorkManager, etc. should be initialized on demand, not in `Application.onCreate()`. Firebase itself does this — don't subclass and force eager init.
- **ReportFullyDrawn()**: Call `activity.reportFullyDrawn()` after async data loads so startup trace captures real TTI (Time To Interactive), not just first blank frame.
- **Baseline Profile**: Ship `baseline-prof.txt` alongside AAB. Cloud profiles (Play Store) optimize further. Generated from macrobenchmark:
  ```kotlin
  @Test
  fun generateBaselineProfile() {
      rule.collect(packageName = "com.example.app") {
          pressHome(); startActivityAndWait(); device.wait(Until.foreground(), 5000)
      }
  }
  ```

### React Native: Startup

| Engine | Startup | Bundle Size | Notes |
|--------|---------|-------------|-------|
| **Hermes** | 30-50% faster cold start vs JSC | Smaller (precompiled bytecode) | Default since RN 0.70. Always use for production. |
| **JSC (JavaScriptCore)** | Slower parse + compile | Larger (text JS) | Deprecated for production. |

**Specific optimizations:**
- **Inline requires**: `require()` at call site, not top of file. Metro bundles on-demand instead of all at startup.
  ```js
  // ❌ 250ms penalty: all modules loaded upfront
  import { HeavyModule } from './HeavyModule';
  // ✅ Loaded only when screen opens
  const HeavyModule = require('./HeavyModule');
  ```
- **Turbo Modules (Fabric)**: Native modules initialized lazily on first JS call, not eagerly on app start. Migrate from `NativeModules` to Turbo Native Modules.
- **Hermes GC tuning**: In `android/app/build.gradle`:
  ```groovy
  project.ext.react = [
      hermesFlags: ["-O", "-output-source-map", "-max-diagnostic-width=80"]
  ]
  ```

### Flutter: Startup

- **Dart AOT**: Compiles to native ARM/x86 — no JIT warmup. Already fast, but `main()` can still block.
- **Minimize `main()`**: Move non-critical initialization to post-frame callback:
  ```dart
  void main() {
      runApp(const MyApp());
      WidgetsBinding.instance.addPostFrameCallback((_) {
          initializeAnalytics(); // after first frame
      });
  }
  ```
- **Deferred components**: Split large features into deferred libraries loaded on demand (~30% startup reduction for large apps):
  ```dart
  import 'heavy_screen.dart' deferred as heavy;
  // Later: await heavy.loadLibrary(); heavy.HeavyWidget()
  ```

### Measurement

- **Real device only**: Simulators/emulators are misleading. iPhone SE (2nd gen) for iOS. Samsung A14 or Pixel 4a for Android.
- **Cold start**: Force-kill app, clear memory, wait 5 seconds, launch. Measure 10 runs, discard top/bottom 2, average the middle 6.
- **Tooling**: Xcode Organizer (launch time dashboard → 90th percentile). Android Vitals in Play Console (cold start P90).
- **Instrumentation**: `os_signpost` (iOS), `Trace.beginSection` (Android), custom spans in Firebase Performance.

---

## Frame Rate & Jank Prevention

**Target**: 60fps with < 5% dropped frames. 120fps on ProMotion/120Hz devices with < 10% dropped frames.

### Frame Budget

| Refresh Rate | Frame Budget |
|-------------|-------------|
| 60Hz | 16.67ms |
| 90Hz | 11.11ms |
| 120Hz | 8.33ms |

Within that budget: measure → layout → draw → composite → display. If any step exceeds budget, frame drops (jank).

### The Rendering Pipeline

```
[VSYNC] → Input → Animation → Measure → Layout → Draw → Composite → [SWAP]
                                                                    ↑
                                              If > budget → JANK ←─┘
```

### Common Jank Sources (Platform-Agnostic)

1. **Layout thrashing**: Read layout property → write style → read again → forces synchronous re-layout in the same frame. Batch reads then writes.
2. **Overdraw**: Pixels drawn multiple times per frame (background → card → text → shadow). Each layer adds GPU cost.
3. **GC pauses**: JVM/ART/Dart VM garbage collection stops all threads. Avoid allocation in `onDraw()`/`build()`.
4. **Main thread I/O**: SharedPreferences, UserDefaults, SQLite, file reads on main thread. Always async.
5. **Expensive view inflation**: Deep view hierarchies. Flatten with `<merge>`, `<ConstraintLayout>`, or Compose.

### iOS: Jank Debugging

- **Core Animation instrument**: Enable "Color Blended Layers" to find transparent overlays. Enable "Color Offscreen-Rendered" (yellow = GPU offscreen render). Green is good, red/yellow is bad.
- **Offscreen rendering triggers** (each costs 2-3ms per frame):
  - `cornerRadius` + `layer.masksToBounds` — compositor must rasterize to a separate buffer.
  - Fix: use `layer.shouldRasterize = true` for static content, or `CAShapeLayer` for masks.
  - `layer.shadowPath` missing — without it, Core Animation computes shadow from layer alpha every frame. Always set:
    ```swift
    layer.shadowPath = UIBezierPath(roundedRect: bounds, cornerRadius: cornerRadius).cgPath
    ```
  - `layer.mask` — forces offscreen pass. Prefer `CALayer` compositing tricks.

- **Hitches metric**: Xcode Organizer → "Hitches/min". Target < 2 hitches/min. Each hitch = frame > 10ms late.

### Android: Jank Debugging

- **GPU Overdraw Visualization**: Developer Options → Debug GPU Overdraw → Show overdraw areas.
  - True color (no overdraw) → Blue (1x) → Green (2x) → Pink (3x) → Red (4x+). Target: < 2x everywhere.
  - Fix: remove redundant backgrounds. `android:background="@null"` when parent provides background.
- **Systrace / Perfetto**: `systrace.py gfx view wm am res dalvik freq idle sched -b 32768 -t 5 -o trace.html`
  - Look for gaps between VSYNC lines → jank. Red frames = >16ms.
  - `Choreographer#doFrame` section shows where time went.
- **Profile GPU Rendering**: Developer Options → Profile GPU Rendering → On screen as bars. Each bar = one frame. Blue = draw, orange = prepare, red = process, purple = execute. Any bar crossing the green line (16ms) = jank.

### React Native: Thread Model & Jank

Three threads: **JS thread** (business logic), **Shadow thread** (yoga layout), **UI thread** (native rendering).

- **Bridge bottleneck** (old architecture): Every JS↔native call is serialized JSON across the bridge. Batching helps but large payloads block.
- **Fabric (new architecture)**: JS thread communicates directly with native via JSI (C++). No bridge serialization. Shadow tree computed on a separate thread.
- **Run heavy JS off the main thread**: `InteractionManager.runAfterInteractions(() => { heavyWork(); })` defers until animations finish.
- **`useMemo` / `React.memo`**: Prevent re-render cascades that block the JS thread for multiple frames.

### Flutter: Thread Model & Jank

Three threads: **UI thread** (Dart, builds widgets), **Raster thread** (GPU, composites layers), **Platform thread** (main, receives events).

- **Raster jank**: UI thread finishes on time but GPU can't rasterize in time. Cause: complex shaders, too many layers, saveLayer calls.
  - Fix: `RepaintBoundary` around independently animating widgets. Profile with `debugProfilePaintsEnabled = true`.
- **UI jank**: `build()` method too expensive. Symptom: `Widget build()` called more than once per frame.
  - Fix: `const` constructors everywhere. Extract expensive widgets into separate `StatelessWidget` subclasses (const can be cached). Use `AnimatedBuilder` with narrow rebuild scope.
- **Isolate for heavy compute**: JSON parsing, image decoding, encryption:
  ```dart
  final result = await compute(heavyFunction, inputData);
  ```

### List Performance

| Platform | High-Performance List | Prefetch Distance | Key Feature |
|----------|----------------------|-------------------|-------------|
| **React Native** | `FlashList` (Shopify) | `estimatedItemSize` + 2 screens | RecyclerViews under the hood. 5-10x faster than FlatList |
| **Flutter** | `ListView.builder` | `cacheExtent: 500` | Only builds visible + cached items |
| **Android** | `RecyclerView` | `setItemViewCacheSize(20)` + `RecycledViewPool` | View recycling + prefetch via `GapWorker` |
| **iOS** | `UICollectionView` / `LazyVStack` | `prefetchDataSource` | Cell reuse queue + `UICollectionViewDiffableDataSource` for no-reload updates |

**Universal list rules:**
- **Stable keys**: `keyExtractor` (RN), `key:` (Flutter/Compose), `diffableDataSource` (iOS). Re-rendering everything on data change is the #1 list jank cause.
- **Constant item height**: If every item is the same height, the list engine doesn't need to measure — it math-computes positions. 40-60% faster scroll.
- **Avoid inline functions in render**: New closure every render = new props = child re-render. Extract to `useCallback` or class method.

---

## Memory Management

**Target**: < 50MB on a 2GB device after initial load (not after extended use), < 200MB peak on a 6GB device.

### Memory Classes

| Class | Contents | Growth Pattern |
|-------|----------|---------------|
| **Heap** | Object allocations (your code) | Grows with usage, GC collects |
| **Anonymous VM** | `mmap` without file backing, large allocations | Spikes on image decode, large buffers |
| **Graphics** | GPU textures, framebuffers | Spikes on screens with many images |
| **Code** | Loaded libraries, JIT caches | Fixed at startup, grows slightly |

### iOS Memory Limits

No hard documented limit — app is killed (jetsam) when system needs memory:

| Device | RAM | Approximate Jetsam Limit |
|--------|-----|--------------------------|
| iPhone SE (2nd gen) | 3GB | ~600MB |
| iPhone 13 | 4GB | ~800MB |
| iPhone 15 Pro | 8GB | ~1.5GB |
| iPad (10th gen) | 4GB | ~1.2GB |

iOS sends `didReceiveMemoryWarning` before jetsam. **Always implement**:
```swift
override func didReceiveMemoryWarning() {
    super.didReceiveMemoryWarning()
    imageCache.removeAllObjects()
    URLCache.shared.removeAllCachedResponses()
}
```

### Android Memory Limits

Varies by device. Query at runtime:
```kotlin
val am = getSystemService(ACTIVITY_SERVICE) as ActivityManager
val memoryClassMB = am.memoryClass        // heap limit in MB (16-512)
val largeMemoryClassMB = am.largeMemoryClass // with largeHeap=true (not recommended)
```

| Screen Density | Typical Memory Class |
|---------------|---------------------|
| ldpi / mdpi | 16-32MB |
| hdpi | 32-64MB |
| xhdpi | 64-128MB |
| xxhdpi+ | 128-512MB |

**`largeHeap="true"`**: Only for camera, photo editor, or games. Adds 2-4x heap but reduces available memory for other processes. Do not use as a leak band-aid.

### Memory Leak Patterns (Cross-Platform)

1. **Retain cycles (closures capturing self):**
   ```swift
   // ❌ Leak: closure holds self, self holds closure
   fetchData { data in self.updateUI(data) }
   // ✅ Weak capture
   fetchData { [weak self] data in self?.updateUI(data) }
   ```

2. **Unregistered observers:**
   - `NotificationCenter.addObserver` without matching `removeObserver` (iOS)
   - `LiveData.observe` with wrong `LifecycleOwner` (Android)
   - `EventEmitter.addListener` without `removeListener` (RN)

3. **Singletons holding Activity/Context:**
   ```kotlin
   // ❌ Leaks entire Activity on rotation
   object Analytics {
       var context: Context? = null  // never hold Activity context
   }
   // ✅ Application context only
   object Analytics {
       lateinit var appContext: Context  // applicationContext, not Activity
   }
   ```

4. **Animation not cancelled:**
   - iOS: `UIView.animate` with completion block referencing released objects
   - Android: `Animator` not cancelled in `onDestroy()`
   - Flutter: `AnimationController` not disposed

### Detection Tools

| Platform | Tool | What It Finds |
|----------|------|---------------|
| **iOS** | Xcode Memory Graph Debugger | Retain cycles, abandoned memory (Runtime issue navigator) |
| **iOS** | Instruments → Leaks | Real-time leak detection |
| **iOS** | Instruments → Allocations | Heap growth over time; "Generations" mode to find incremental leaks |
| **Android** | LeakCanary | Automatic leak detection in debug builds. Ship `leakcanary-android-no-op` in release. |
| **Android** | Android Studio Memory Profiler | Heap dump, allocation tracking, GC event timeline |
| **RN** | Hermes Heap Snapshots | `global.HermesInternal.getInstrumentedStats()` in Chrome DevTools |
| **Flutter** | Dart DevTools → Memory | Heap snapshot, allocation tracking per isolate |

### Image Memory: The Silent Killer

**Formula**: Decoded bitmap memory = `width × height × 4 bytes` (RGBA, 8 bits per channel).

| Resolution | Memory |
|-----------|--------|
| 4000×3000 (12MP photo) | **48MB** |
| 1920×1080 (Full HD) | **8.3MB** |
| 1125×2436 (iPhone X screenshot) | **11MB** |
| 750×1334 (thumbnail) | **4MB** |

A list of 20 thumbnails = **80MB** just in decoded images.

**Strategies:**
1. **Downscale before decode**: Load at display size, not original resolution.
   - Android: `BitmapFactory.Options.inSampleSize = 4` (decodes at ¼ resolution = 1/16 memory)
   - iOS: `UIImage(data: data, scale: 2.0)` loads at 0.5x resolution
   - React Native: `Image.resizeMode` + use CDN with `?w=300` query param
   - Flutter: `cacheWidth: 300` / `cacheHeight: 300` on `Image.network`
2. **LRU cache**: `LruCache` (Android, ⅛ of available memory), `NSCache` (iOS, auto-evicts under pressure).
3. **Dispose off-screen images**: In lists, dispose images that are scrolled far off-screen. Use `evictsObjectsWithDiscardedContent = true` on iOS.

---

## Bundle Size

**Targets:**
| Platform | Max Download | Max Installed |
|----------|-------------|---------------|
| iOS | 200MB (cellular) / unlimited (WiFi) | < 30MB compressed IPA |
| Android | 150MB compressed AAB | < 15MB base APK per density |

### iOS: App Thinning

| Technique | What It Does | Status |
|-----------|-------------|--------|
| **Slicing** | App Store delivers only assets for target device (e.g., @2x for iPhone SE, @3x for Pro) | ✅ Active |
| **On-Demand Resources** | Assets downloaded after install. Tag with `NSBundleResourceRequest`. Good for: game levels, tutorial videos, AR assets. | ✅ Active |
| **Bitcode** | App Store recompiles for target architecture | ❌ Deprecated (Xcode 14+) |

**Audit with**: `xcrun assetutil --info Payload/App.app` → shows which assets are tagged for slicing.

### Android: App Bundle (AAB)

- **Automated splitting**: Google Play generates split APKs per density (`drawable-mdpi`), ABI (`arm64-v8a`), and language (`values-fr`).
- **Play Feature Delivery**: Split features by module. Users download only modules they actually use.
  ```gradle
  // build.gradle (dynamic feature module)
  plugins { id("com.android.dynamic-feature") }
  ```
- **On-demand modules**: Install mid-session via `SplitInstallManager`.

**Audit with**: `bundletool build-apks --bundle=app.aab --output=out.apks` → `bundletool get-size total --apks=out.apks` → shows per-device size.

### React Native: Bundle Optimization

**Audit**:
```bash
npx react-native-bundle-visualizer --platform ios --dev false
```

**Optimizations:**
- **Hermes precompiled bytecode**: Run `npx react-native bundle --minify true --bundle-output ...` with Hermes. Bytecode is 30-40% smaller than JS text + parse time eliminated.
- **Metro config pruning**: Exclude test files, Flow types, dev tools:
  ```js
  // metro.config.js
  transformer: {
      minifierPath: 'metro-minify-terser',
      minifierConfig: { compress: { drop_console: true } }
  }
  ```
- **Dead code elimination**: `babel-plugin-transform-remove-console` for production.

### Flutter: Bundle Optimization

- **`--split-debug-info`**: Moves debug symbols out of the binary (~10-20% reduction).
  ```bash
  flutter build apk --split-debug-info=build/debug-info
  ```
- **Icon tree shaking**: Flutter strips unused Material/Cupertino icons automatically.
- **Deferred components**: (Android only) Split large features. Requires Gradle dynamic feature modules.
- **ProGuard/D8/R8** already run on Android `flutter build`. Enable on iOS via `--obfuscate`.

### Common Bloat Sources (Audit These First)

| Bloat Source | Typical Waste | Fix |
|-------------|--------------|-----|
| **Duplicate .so files** | 5-15MB | Check `jniLibs` — ensure no duplicate architectures |
| **Uncompressed assets** | 2-10MB | Compress JSON/CSV. Use WebP instead of PNG (35% smaller). |
| **Debug symbols in release** | 3-8MB | Strip with `strip -S` (iOS), `minifyEnabled true` (Android) |
| **Unused fonts** | 1-5MB per font | Remove font weights you don't render (e.g., Light, Black variants) |
| **Maps SDK + tiles** | 15-40MB | Use on-demand feature delivery for maps module |
| **Firebase/GoogleServices plist/json** | Negligible | Ensure `GoogleService-Info.plist` and `google-services.json` not duplicated |

---

## Network Performance

**Target**: Critical API response < 200ms on 4G (p50), < 500ms on 3G (p90).

### HTTP Caching

**ETag / If-None-Match** — server sends hash of response. Client sends it back. Server responds `304 Not Modified` (no body, ~200 bytes). Saves 90%+ transfer for unchanged data.

```swift
// iOS: URLCache handles this automatically
let config = URLSessionConfiguration.default
config.requestCachePolicy = .reloadRevalidatingCacheData

// Android: OkHttp handles this automatically with CacheControl
val cache = Cache(File(context.cacheDir, "http"), 10 * 1024 * 1024)
val client = OkHttpClient.Builder().cache(cache).build()
```

**Cache-Control header strategy:**
- Immutable assets (images, fonts): `Cache-Control: public, max-age=31536000, immutable`
- API lists (inbox): `Cache-Control: private, max-age=60, stale-while-revalidate=300`
- Real-time data (stock price): `Cache-Control: no-store`

### Payload Optimization

| Technique | Typical Savings | Effort |
|-----------|----------------|--------|
| **Gzip/Brotli** (text responses) | 60-80% | Server config only |
| **JSON field pruning** (`?fields=id,name,avatar`) | 40-70% | GraphQL or custom server filter |
| **GraphQL** (replace REST) | 30-50% | Schema migration |
| **Protobuf** (replace JSON) | 20-40% vs gzipped JSON | Schema + codegen |
| **WebP/AVIF images** (replace PNG/JPEG) | 25-50% | CDN transformation |
| **Incremental delta updates** | 80-95% on subsequent fetches | Server-side diffing |

### Connection Optimization

- **HTTP/2 multiplexing**: Single TCP connection, multiple concurrent requests. Eliminates head-of-line blocking. Already default on `URLSession` (iOS) and OkHttp (Android, since 3.x). Verify server supports H2 (`curl -sI --http2 https://api.example.com`).
- **Connection pooling**: `URLSession` and OkHttp pool connections. Keep-alive timeout: server should set to 30-60 seconds. Client should not close after each request.
- **DNS prefetch**: On app launch, warm up DNS for critical domains:
  ```kotlin
  // Android
  CoroutineScope(Dispatchers.IO).launch {
      InetAddress.getByName("api.example.com")
  }
  ```

### Image Delivery

Never serve full-resolution images to mobile. Use an image CDN with URL-based transformations:

```
https://cdn.example.com/photos/beach.jpg?w=375&h=300&fit=crop&fm=webp&q=80
```

| CDN | URL Pattern |
|-----|-------------|
| **imgix** | `?w=375&h=300&fit=crop&fm=webp&auto=compress` |
| **Cloudinary** | `upload/w_375,h_300,c_fill,f_auto,q_auto/beach.jpg` |
| **CloudFront + Lambda@Edge** | Custom `?size=375x300&format=webp` handler |

### Offline-First Strategy

- **Cache-then-network**: Show cached data immediately, fetch fresh in background, reconcile on arrival. Avoids empty states and spinners.
- **Persistent storage**: Room (Android), Core Data / SwiftData (iOS), WatermelonDB (RN), Isar/Hive (Flutter).
- **Sync engine**: Queue mutations when offline, replay when online. Use `WorkManager` (Android) or `BGTaskScheduler` (iOS).

---

## Measurement & CI Enforcement

### Measurement Tools

| Tool | Platform | Metrics |
|------|----------|---------|
| **Xcode Instruments** | iOS | Startup time, memory, CPU, network, energy, frame rate |
| **Android Profiler** | Android | CPU, memory, network, energy |
| **Xcode Organizer** | iOS (App Store) | Launch time, hitches, disk writes, hangs, memory |
| **Android Vitals** | Android (Play Console) | ANR rate, crash rate, startup time, stuck partial wake locks |
| **Firebase Performance** | Cross-platform | Custom traces, HTTP request latency, screen rendering |
| **Sentry Performance** | Cross-platform | Distributed tracing, span waterfall, slowest DB queries |
| **Flipper** | Cross-platform (debug) | Network inspector, layout inspector, shared preferences viewer |
| **Macrobenchmark** | Android | Startup, scroll jank, complex UI frame timing (Jetpack library) |

### CI Performance Gates

Fail the build if any gate is violated:

```yaml
# Sample CI config (platform-agnostic gates)
performance_gates:
  cold_start:
    max: 2000ms              # iPhone SE / Pixel 4a target
    percentile: p90          # Not average! Average hides outliers
    warmup_runs: 3           # Discard first 3 (cache warmup)
    measure_runs: 10         # Run 10, take p90

  memory:
    peak: 80MB               # Peak during standard user flow
    baseline: 45MB           # After initial load, before heavy use
    leak_test_iterations: 10 # Repeat 10x — memory must return to baseline

  bundle_size:
    ios_ipa_compressed: 30MB
    android_base_apk: 15MB

  frame_drops:
    max_percent: 5%          # Max % frames over 16ms during scroll test
    scroll_distance: 10000px # Scroll 10,000px of content
```

### Real User Monitoring (RUM)

Aggregate metrics from production, segmented:

| Segment | Why |
|---------|-----|
| **Device class** | iPhone 15 Pro vs iPhone SE shows 3x perf difference |
| **OS version** | iOS 17 vs iOS 15 — different system behaviors |
| **Network type** | 5G/WiFi (fast), 4G (moderate), 3G/Edge (slow) — affects network-bound startup |
| **App version** | Detect regressions in new releases |
| **Cold vs warm start** | Cold is the real test; warm hides problems |

**Key percentiles**: Track p50 (typical user), p75 (worse-case typical), p95 (edge case). Never track average — it smooths out the tail you need to fix.

### Performance Regression Detection

- **Record baseline** on each release using the same device (or cloud device farm like Firebase Test Lab / Sauce Labs).
- **Flag regression**: if any metric degrades > 10% from baseline, block the release.
- **Bisect**: Git bisect between last good → first bad commit. Macrobenchmark supports bisecting automatically.
