---
title: "Android Performance Optimization — Cold Start, Scroll, Memory, APK Size"
author: Sandeep Kumar Penchala
date: 2026-07-24
---

## Performance Pillars

Android performance has four pillars that directly impact user experience and Play Store visibility:

| Pillar | Android Vitals Metric | Bad Threshold | Good Target |
|--------|----------------------|---------------|-------------|
| Startup | Cold start time | > 5s | < 1.5s |
| Rendering | Slow frames (jank) | > 15% of sessions | < 8% |
| Stability | Crash rate | > 1.09% | < 0.47% |
| Memory | ANR rate | > 0.47% | < 0.08% |

## Cold Start Optimization

Cold start is the most impactful performance metric. Users judge your app in the first 2 seconds. Google's research shows that 53% of users abandon apps that take longer than 3 seconds to launch.

### What Happens During Cold Start

```
System Process: Fork Zygote → Create new Linux process
    ↓
App Process: Application.onCreate()
    ↓
Activity: MainActivity.onCreate() → setContent {} → first frame drawn
    ↓
User sees: Initial display → fully interactive
```

### Measuring Cold Start

```bash
# Via command line
adb shell am start -W com.example.app/.MainActivity
# Output: TotalTime: 1842ms ← This is your cold start time

# Repeat 5 times, restarting the app process between each:
adb shell am force-stop com.example.app
adb shell am start -W com.example.app/.MainActivity  # Repeat 5x
```

### Macrobenchmark — Automated Measurement

```kotlin
@RunWith(AndroidJUnit4::class)
class StartupBenchmark {
    @get:Rule val benchmarkRule = MacrobenchmarkRule()

    @Test
    fun startup() = benchmarkRule.measureRepeated(
        packageName = "com.example.app",
        metrics = listOf(StartupTimingMetric()),
        iterations = 10,
        startupMode = StartupMode.COLD
    ) {
        pressHome()
        val intent = Intent(Intent.ACTION_MAIN).apply {
            addCategory(Intent.CATEGORY_LAUNCHER)
            setPackage("com.example.app")
        }
        startActivityAndWait(intent)
    }
}
```

### Startup Optimization Strategies

```kotlin
// BAD: Heavy initialization in Application.onCreate()
class MyApp : Application() {
    override fun onCreate() {
        super.onCreate()
        // These all block the main thread during cold start:
        initializeCrashlytics()
        initializeAnalytics()
        initializeImageLoader()
        initializeRoomDatabase()  // Database creation is expensive
        initializeRemoteConfig()  // Network call on startup thread
    }
}

// GOOD: Lazy and deferred initialization
class MyApp : Application() {
    override fun onCreate() {
        super.onCreate()
        // Only critical init here (crash reporting)
        initializeCrashlytics()  // Must be first — catch startup crashes

        // Defer non-critical init to background thread
        CoroutineScope(Dispatchers.IO).launch {
            initializeAnalytics()
            initializeImageLoader()
        }
    }
}

// Use AndroidX Startup library for declarative init
// Instead of Application.onCreate(), declare initializers:

class AnalyticsInitializer : Initializer<Unit> {
    override fun create(context: Context) {
        // Runs on background thread automatically
        initializeAnalytics()
    }
    override fun dependencies(): List<Class<out Initializer<*>>> = listOf(CrashlyticsInitializer::class.java)
}

// AndroidManifest.xml — register your initializers
// <provider
//     android:name="androidx.startup.InitializationProvider"
//     android:authorities="${applicationId}.androidx-startup">
//     <meta-data android:name="com.example.AnalyticsInitializer" android:value="androidx.startup" />
// </provider>
```

### Splash Screen API

```kotlin
// Use the platform SplashScreen API (Android 12+) — zero-cost splash
// themes.xml
<style name="Theme.App.Starting" parent="Theme.SplashScreen">
    <item name="windowSplashScreenBackground">@color/white</item>
    <item name="windowSplashScreenAnimatedIcon">@drawable/ic_splash</item>
    <item name="postSplashScreenTheme">@style/Theme.App</item>
</style>

// MainActivity.kt
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        installSplashScreen()  // Must be before super.onCreate()
        super.onCreate(savedInstanceState)
        setContent { App() }
    }
}
```

## Scroll Performance & Jank Prevention

### The Frame Budget

At 60fps, each frame has **16.67ms** to render. At 90fps: **11ms**. At 120fps: **8ms**. Every millisecond your code takes beyond the budget = a dropped frame = jank.

### LazyColumn Performance Rules

```kotlin
@Composable
fun FeedScreen(posts: List<Post>) {
    LazyColumn {
        items(
            items = posts,
            key = { post -> post.id }  // RULE 1: Stable keys — prevents item recomposition shuffle
        ) { post ->
            // RULE 2: Expensive calculations outside LazyColumn items
            // These run once — not per item
            val formatter = remember { SimpleDateFormat("MMM dd, yyyy") }

            // RULE 3: Avoid object allocation in item composable
            PostItem(
                post = post,
                formattedDate = formatter.format(post.createdAt),  // Pre-computed
                onClick = { /* stable reference */ }
            )
        }
    }
}
```

### Stable + Immutable for Skippable Recompositions

```kotlin
@Stable
data class PostUiItem(
    val id: String,
    val title: String,
    val authorAvatar: Bitmap? = null,  // Bitmap is not @Stable by default
    val timestamp: Long
)

// Custom stability for types Compose doesn't know about
@Stable
class StableBitmapHolder(val bitmap: Bitmap) {
    // Compose uses equals() to check stability — Bitmap.equals() doesn't work
    // Workaround: wrap in a class and implement equals by generation ID
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is StableBitmapHolder) return false
        return this.bitmap.generationId == other.bitmap.generationId
    }
    override fun hashCode(): Int = bitmap.generationId
}
```

### Animation Performance

```kotlin
// Modifier.offset is cheaper than Modifier.padding for animations
// Avoid layout-affecting animations in scrollable lists

@Composable
fun SwipeableItem() {
    var offsetX by remember { mutableFloatStateOf(0f) }
    Box(
        modifier = Modifier
            .offset { IntOffset(offsetX.roundToInt(), 0) }  // Graphics layer only — no layout remeasurement
            .pointerInput(Unit) { detectHorizontalDragGestures { _, dragAmount -> offsetX = dragAmount } }
    )
}
```

## Memory Optimization

### Memory Budget by Device

| Device Tier | RAM | Memory Limit (per process) | Your Max Budget |
|-------------|-----|---------------------------|-----------------|
| Android Go | 1-2GB | ~128-256MB | 100MB |
| Budget | 3-4GB | ~256-512MB | 200MB |
| Mid-range | 6-8GB | ~512MB-1GB | 350MB |
| Flagship | 12-16GB | ~1-2GB | 500MB |

### Memory Profiling with Android Studio

```
Android Studio → Profiler → Memory → Record allocations
1. Navigate through your app's key screens
2. Trigger all major features
3. Look for:
   - Memory not decreasing after returning to previous screen
   - Repeated allocation without deallocation (class count increasing)
   - Large byte[] or Bitmap allocations
```

### Bitmap Memory Management

```kotlin
// WRONG: Full-resolution bitmap decode
val bitmap = BitmapFactory.decodeFile(photoPath)
// 12MP photo: 4000 × 3000 × 4 bytes/pixel = 48MB ← exceeds many device limits

// RIGHT: Downsample to display size
fun decodeSampledBitmap(path: String, reqWidth: Int, reqHeight: Int): Bitmap {
    val options = BitmapFactory.Options().apply { inJustDecodeBounds = true }
    BitmapFactory.decodeFile(path, options)
    // Raw dimensions: options.outWidth, options.outHeight

    options.inSampleSize = calculateInSampleSize(options, reqWidth, reqHeight)
    options.inJustDecodeBounds = false
    return BitmapFactory.decodeFile(path, options)
}

fun calculateInSampleSize(options: BitmapFactory.Options, reqWidth: Int, reqHeight: Int): Int {
    val (height, width) = options.outHeight to options.outWidth
    var inSampleSize = 1
    if (height > reqHeight || width > reqWidth) {
        val halfHeight = height / 2
        val halfWidth = width / 2
        while ((halfHeight / inSampleSize) >= reqHeight && (halfWidth / inSampleSize) >= reqWidth) {
            inSampleSize *= 2
        }
    }
    return inSampleSize
}
```

### Glide/Coil Integration

```kotlin
// Glide — always override to display size
Glide.with(context)
    .load(url)
    .override(targetWidth, targetHeight)  // Downsample to actual View size
    .centerCrop()
    .into(imageView)

// Coil (Compose native) — automatic sizing based on composable layout
AsyncImage(
    model = url,
    contentDescription = "Post image",
    contentScale = ContentScale.Crop,
    modifier = Modifier.size(300.dp)
)
// Coil automatically downsamples to the composable's pixel size
```

### Memory Leak Detection with LeakCanary

```kotlin
// build.gradle.kts (app) — dev dependency only
dependencies {
    debugImplementation("com.squareup.leakcanary:leakcanary-android:2.13")
}

// Application class
class MyApp : Application() {
    override fun onCreate() {
        super.onCreate()
        // LeakCanary auto-installs in debug builds — no manual configuration needed
    }
}
```

## APK / AAB Size Optimization

### APK Analyzer

Analyze your APK/AAB in Android Studio: **Build → Analyze APK → Select your AAB**

### Size Reduction Strategies

```kotlin
android {
    buildTypes {
        release {
            // 1. R8 Code Shrinking + Obfuscation
            isMinifyEnabled = true
            isShrinkResources = true  // Removes unused resources
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }

    // 2. Limit ABI support (drop x86 for phones, keep arm64-v8a)
    defaultConfig {
        ndk { abiFilters += listOf("arm64-v8a") }
    }

    // 3. Remove non-English resources from libraries
    defaultConfig {
        resConfigs("en")  // Only include English strings from all dependencies
    }

    // 4. Convert images to WebP
    // Run: Android Studio → Refactor → Convert to WebP
    // WebP is 25-35% smaller than PNG, supported on all Android versions

    // 5. Use vector drawables instead of PNG for icons
    // < 200dp icons: vector drawable (XML)
    // > 200dp images: WebP

    // 6. Adaptive icon: foreground (108dp) + background layers
    // Both as vector drawables — zero raster cost

    // 7. App Bundle splits by default
    bundle {
        language { enableSplit = true }
        density { enableSplit = true }
        abi { enableSplit = true }
    }
}
```

### Baseline Profiles

Baseline Profiles pre-compile critical code paths (startup, navigation), reducing JIT warmup time by 30-40% on first launch after install.

```kotlin
// app/src/main/baseline-prof.txt (generated by Macrobenchmark)

// Generate: ./gradlew :app:generateBaselineProfile
// This profile is included in the AAB and used by Play Store to pre-compile
// your app's critical paths during install.

// Macrobenchmark to generate:
@RunWith(AndroidJUnit4::class)
class BaselineProfileGenerator {
    @get:Rule val benchmarkRule = MacrobenchmarkRule()

    @Test
    fun generateBaselineProfile() = benchmarkRule.collectBaselineProfile(
        packageName = "com.example.app",
        iterations = 3  // Multiple runs to cover different code paths
    ) {
        pressHome()
        val intent = Intent(Intent.ACTION_MAIN).apply {
            addCategory(Intent.CATEGORY_LAUNCHER)
            setPackage("com.example.app")
        }
        startActivityAndWait(intent)
        // Navigate through critical user journeys
        device.findObject(By.text("Feed")).click()
        device.waitForIdle()
        device.findObject(By.text("Profile")).click()
        device.waitForIdle()
    }
}
```

## StrictMode — Catch Performance Issues in Development

```kotlin
class MyApp : Application() {
    override fun onCreate() {
        if (BuildConfig.DEBUG) {
            StrictMode.setThreadPolicy(
                StrictMode.ThreadPolicy.Builder()
                    .detectDiskReads()
                    .detectDiskWrites()
                    .detectNetwork()
                    .detectCustomSlowCalls()
                    .penaltyLog()
                    .penaltyFlashScreen()  // Red flash border on violation
                    .build()
            )
            StrictMode.setVmPolicy(
                StrictMode.VmPolicy.Builder()
                    .detectLeakedSqlLiteObjects()
                    .detectLeakedClosableObjects()
                    .detectActivityLeaks()
                    .detectLeakedRegistrationObjects()
                    .penaltyLog()
                    .build()
            )
        }
        super.onCreate()
    }
}
```

## Performance Checklist (Pre-Release)

- [ ] Cold start < 1.5s on budget device (measured via `adb shell am start -W`, averaged over 5 runs)
- [ ] Macrobenchmark cold start shows < 10% regression from previous release
- [ ] LazyColumn scrolls at 60fps (zero dropped frames) on budget device, measured via Profile GPU Rendering
- [ ] Memory usage stays under 200MB on a 4GB device during a 10-minute session (monitored via Memory Profiler)
- [ ] No memory leaks: LeakCanary shows zero retained instances after navigating all screens
- [ ] APK/AAB download size < 30MB (APK Analyzer), install size < 100MB
- [ ] Baseline profile generated and included in AAB
- [ ] ProGuard/R8 enabled in release build, isShrinkResources = true
- [ ] All images loaded via Glide/Coil with explicit `override()` or automatic sizing
- [ ] StrictMode enabled in debug builds — zero violations in logcat
- [ ] Android Vitals on Play Console: no warnings on startup time, slow rendering, or ANR rate
