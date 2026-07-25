---
name: android-developer
description: Android development with Kotlin, Jetpack Compose, Android SDK, Material Design 3, Gradle, Play Store deployment, and Android-specific architecture. Use when building Android applications, designing Android UI with Jetpack Compose/XML, configuring Gradle build variants, implementing Android-specific features (WorkManager, Room, Navigation), managing Play Store listings, or optimizing Android performance. Handles Android architecture patterns (MVVM, MVI), Kotlin coroutines/Flow, Android testing (JUnit, Espresso, Compose testing), and background processing. Do NOT use for iOS development, cross-platform mobile, or backend API development.
author: Sandeep Kumar Penchala
license: MIT
version: 1.0.0
updated: 2026-07-24
tags: [android, kotlin, jetpack-compose, mobile, play-store, gradle, material-design]
token_budget: 4500
chain:
  consumes_from:
    - mobile-developer
    - mobile-architecture-patterns
    - ui-ux-designer
    - backend-developer
    - accessibility-auditor
  feeds_into:
    - qa-engineer
    - security-reviewer
    - performance-engineer
---

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

# Android Developer — Native Android Application Development

Build production-grade native Android applications with Kotlin and Jetpack Compose. This is the internal playbook for FAANG-level Android engineering — every section contains concrete, actionable implementation patterns, not generic advice. Covers the full development lifecycle: Compose UI architecture with Material Design 3, MVVM and MVI patterns with ViewModel and StateFlow, Kotlin coroutines and Flow for asynchronous data, Room database with migrations and type converters, dependency injection with Hilt (compile-time verified), Gradle build variants with product flavors, background processing with WorkManager and Foreground Services, Play Store deployment with App Bundle signing, Android accessibility with TalkBack and semantic trees, and performance optimization — cold start under 1.5 seconds, locked 60fps scrolling, and under 50MB APK download — all measured on a $150 budget device with 4GB RAM.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("build.gradle.kts", "com.android.application")` OR `file_exists("app/src/main/AndroidManifest.xml")` OR `file_contains("*.kt", "@Composable")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*.kt", "@Database\|@Entity\|@Dao\|RoomDatabase")` OR `file_contains("build.gradle.kts", "androidx.room")` | Jump to **Decision Trees** — Room vs SQLDelight. |
| A3 | `file_contains("*.kt", "@HiltAndroidApp\|@HiltViewModel\|@Module\|@InstallIn")` OR `file_contains("*.kt", "koin\|kodein")` | Jump to **Decision Trees** — DI Strategy. |
| A4 | `file_contains("*.kt", "WorkManager\|PeriodicWorkRequest\|CoroutineWorker")` OR `file_contains("AndroidManifest.xml", "FOREGROUND_SERVICE")` | Jump to **Core Workflow** — Phase 4 (Background Processing). |
| A5 | `file_contains("*.kt", "viewModel\|ViewModel")` AND `file_contains("*.kt", "StateFlow\|MutableStateFlow\|UiState")` | Jump to **Core Workflow** — Phase 3 (ViewModel & State). |
| A6 | `file_contains("*.kt", "ProGuard\|R8\|minifyEnabled\|proguard-rules")` OR `file_contains("*.kt", "CollectingProguard\|proguard")` | Jump to **Decision Trees** — ProGuard/R8 Configuration. |
| A7 | `file_contains("*.xml", "strings.xml\|contentDescription\|accessibility")` OR `file_contains("*.kt", "contentDescription\|semantics\|TalkBack")` | Jump to references/android-accessibility.md. |
| A8 | `file_contains("*.kt", "Glide\|Coil\|BitmapFactory")` AND `file_contains("*.kt", "override(\|resize\|inSampleSize")` | Jump to references/android-performance-optimization.md. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Build a new Android app from scratch → Start at Decision Trees (Architecture), then Core Workflow Phase 1
├── Design a Jetpack Compose screen → Jump to "Core Workflow > Phase 2 (Compose UI)" and references/jetpack-compose-patterns.md
├── Set up navigation (bottom nav, deep links) → Go to "Decision Trees > Navigation Compose vs Fragments"
├── Implement Room database → Go to "Decision Trees > Room vs SQLDelight" then references/room-database-guide.md
├── Set up dependency injection → Go to "Decision Trees > DI Strategy" then Core Workflow Phase 1
├── Configure Gradle build variants → Jump to references/android-build-variants.md
├── Implement background work → Jump to "Core Workflow > Phase 4"
├── Optimize performance → Jump to references/android-performance-optimization.md
├── Make app accessible → Jump to references/android-accessibility.md
├── Prepare for Play Store → Jump to references/play-store-deployment.md
├── Handle coroutines/Flow properly → Jump to references/kotlin-coroutines-flow.md
├── Need iOS counterpart → Invoke mobile-developer skill instead
├── Need cross-platform mobile → Invoke mobile-developer skill instead
├── Need backend API for Android → Invoke backend-developer skill instead
└── Don't know where to start? → Describe your app idea and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| **R1** | **REFUSE main-thread blocking.** No network, file I/O, or heavy computation on the UI thread. | Trigger: `suspend` function or I/O call (`URL.readText()`, `File.readBytes()`, `socket.connect()`) directly in `@Composable` or `onCreate()` without `withContext(Dispatchers.IO)` | STOP. "Main-thread blocking at [file:line]. Android enforces 5s ANR threshold — blocking >5s kills your process. Wrap in `withContext(Dispatchers.IO) { }` or `viewModelScope.launch(Dispatchers.IO)`." |
| **R2** | **DETECT no error state in UI. Every data-loading screen must handle loading, success, AND error.** | Trigger: `collectAsState()` of a `Flow` in `@Composable` that has no `when { is Error -> }` branch, OR network call without `.catch {}` that updates UI | STOP. "Missing error state at [file:line]. Use `sealed class UiState { Loading; Success(data); Error(message, retry) }`. A blank screen on failure looks like a crash." |
| **R3** | **REFUSE hardcoded secrets.** No API keys, tokens, or credentials in Kotlin/Java source, XML resources, or Gradle files. | Trigger: string `apiKey`, `clientSecret`, `privateKey`, `token` with base64 blob ≥ 20 chars in `.kt`/`.xml`/`.gradle` files | STOP. "Hardcoded secret at [file:line]. `strings app.apk \| grep apiKey` extracts this in seconds. Use Android Keystore + server-side proxy." |
| **R4** | **DETECT missing lifecycle-aware coroutine scoping.** Every coroutine must be bound to a scope that cancels on destruction. | Trigger: `launch { }` without `viewModelScope` in ViewModel, or without `lifecycleScope` in Activity/Fragment, OR `GlobalScope.launch` anywhere | STOP. "Unscoped coroutine at [file:line]. Use `viewModelScope.launch { }` in ViewModels, `lifecycleScope.launch { }` in Activities. Never `GlobalScope` in production." |
| **R5** | **REFUSE full-resolution bitmap without downsampling.** Images must be downsampled to viewport dimensions. | Trigger: `BitmapFactory.decodeResource()` without `Options.inSampleSize`, or Glide/Coil call without `override()` on images > 2MB | STOP. "Unsampled bitmap at [file:line]. A 12MP photo consumes ~36MB RAM. Use Glide `.override(w, h)` or Coil `.size(w, h)`. Downsample to 2× display size max." |
| **R6** | **DETECT missing contentDescription on interactive Composables.** Every Image, IconButton, and unlabeled interactive element needs contentDescription for TalkBack. | Trigger: `Image(` or `IconButton(` in `@Composable` lacking `contentDescription` AND no adjacent `Text()` describing the element | STOP. "Missing contentDescription at [file:line]. TalkBack reads 'unlabeled button' — a Play Store pre-launch report violation. Decorative: `contentDescription = null`. Interactive: describe the action." |
| **R7** | **DETECT collectAsState without lifecycle awareness.** Hot Flow collection must pause when lifecycle drops below STARTED. | Trigger: `Flow.collectAsState()` in `@Composable` without `collectAsStateWithLifecycle()` | STOP. "Use `collectAsStateWithLifecycle()` from lifecycle-runtime-compose. Plain `collectAsState()` wastes battery and CPU collecting when the screen is off-screen." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

<!-- DEEP: 10+min — how masters think, not just what they do -->

### The Mental Model Shift
Competent Android developers build apps that work on their Pixel 9 Pro. Masters build experiences that **work on a $150 Samsung Galaxy A14 with 4GB RAM, on 3G connectivity, at 10% battery.** Your flagship device on office WiFi represents 5% of global Android users. Design for constraints first — enhance for abundance.

### Cognitive Biases That Kill Android Experiences
| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **Flagship device blindness** | Testing exclusively on latest Pixel — missing the 4GB RAM device where your app is killed every 30 seconds | Maintain a device lab: latest flagship + 3-year-old budget device. Budget is primary test target. |
| **iOS pattern cargo-culting** | Swipe-to-delete without confirmation, center-aligned titles, no back button handling | Android users expect system back, bottom sheets, FABs, long-press menus. Platform conventions = user trust. |
| **Coroutine over-engineering** | Building Channel/actor pipelines for simple data loading | A `StateFlow` with `map`/`combine` handles 95% of cases. Channels are for one-shot events only. |
| **Premature DI abstraction** | Adding Koin or manual factories "to keep it simple" — then fighting lifecycle bugs | Hilt costs 3 annotation lines per class. Compile-time verification prevents runtime DI crashes. |

### What Android Masters Know
- **The Activity lifecycle is a contract, not a suggestion.** Test every screen with "Don't keep activities" enabled in Developer Options. If your app crashes or loses form input after process death and recreation, it's not production-ready. `SavedStateHandle` in ViewModel and `rememberSaveable` in Compose are mandatory, not optional.
- **`LazyColumn` performance is 90% about `onBindViewHolder` cost.** The difference between buttery 60fps and janky 30fps is the cost of each item binding. Avoid object allocation, complex layout inflation, and bitmap decoding in item composables. Always provide stable `key = { it.id }` for correct recomposition on list mutations. Use `DiffUtil`-equivalent `key` tracking to prevent item identity confusion.
- **R8/ProGuard rules are a liability, not a safety net.** Every `-keep` rule you write increases APK size and reduces optimization potential. The goal is zero custom keep rules in `proguard-rules.pro`. AndroidX, Retrofit, Gson/Moshi, Room, Glide/Coil all ship their own consumer ProGuard rules — R8 picks them up automatically from AAR manifests. If you need a custom `-keep`, you've found a reflection pattern that should be made explicit with `@Keep` annotations.
- **Every refactor must remove dead code — not just reorganize it.** When you refactor a screen or module, actively hunt for unused resources, dead navigation routes, stale feature flags, and abandoned Gradle dependencies. Each unused drawable bloats the APK. Each unused string clutters translation files. Each unused dependency increases build time and ProGuard complexity. A refactor's diff should be net-negative in lines.
- **Baseline profiles are not optional for release.** A generated baseline profile pre-compiles critical code paths during install (AOT compilation), reducing JIT warmup by 30-40%. Without one, your app interprets bytecode on first launch after install — producing jank and slow startup for every new user. Generate via Macrobenchmark's `BaselineProfileRule.collect()` and include in your AAB. Every release should audit the baseline profile delta for regressions.

### When to Break Your Own Rules
- **Skip Compose for GPU-intensive custom views.** Real-time audio visualizers, OpenGL maps, per-frame camera processing: use `AndroidView` wrapping a custom `GLSurfaceView`.
- **Use ContentProvider for cross-app data sharing.** Room is for in-app persistence. Inter-app data goes through ContentProvider with a contract URI.

## Operating at Different Levels

| Level | Android Output Characteristics |
|---|---|
| **L1 — Apprentice** | Implements screens from designs. Learns lifecycle, basic ViewModel, Retrofit calls. Step-by-step guidance needed. |
| **L2 — Practitioner** | Delivers features with error/loading states, background work, Material 3 theming. Independent Play Store shipping. |
| **L3 — Senior** | Architecture decisions: MVVM vs MVI, multi-module Gradle, navigation graphs, ProGuard/R8, testing strategy. |
| **L4 — Staff** | Platform strategy: shared component libraries, Gradle convention plugins, CI/CD for Android, app size governance. |
| **L5 — Principal** | Novel patterns adopted industry-wide. Framework contributions. New approaches to Android architecture or performance. |

**Usage**: Say "as an L3 Android developer, design the architecture for..." Default: **L2**.

## When to Use

- Building a new native Android app with Kotlin and Jetpack Compose
- Designing Compose UI: layouts, Material 3 theming, navigation, animation
- Implementing MVVM/MVI with ViewModel, StateFlow, and unidirectional data flow
- Setting up Room database with entities, DAOs, migrations, type converters
- Configuring Hilt DI with lifecycle-scoped components
- Creating Gradle build variants (product flavors, build types, signing configs)
- Implementing background processing with WorkManager and Foreground Services
- Managing coroutines and Flow: structured concurrency, exception handling, testing
- Writing Android tests: JUnit, Espresso, Compose testing
- Preparing Play Store: AAB generation, store listing, managed publishing
- Optimizing performance: cold start, scroll jank, memory, APK size
- Implementing accessibility: TalkBack, content descriptions, touch targets, contrast

## Decision Trees

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Compose vs XML Layout

```
New project, minSdk ≥ 21, team comfortable with declarative UI?
├── YES → Jetpack Compose. Full adoption. 30-40% less code than XML.
└── NO  → Legacy codebase with heavy custom Views (map, camera, video)?
          ├── YES → Compose + AndroidView for legacy interop
          └── NO  → XML + Data Binding + Fragments (migration path)
```

### MVVM vs MVI

```
Complex user-driven state machines (wizard, checkout, multi-step forms)?
├── YES → MVI with sealed Intent + StateFlow + Effect Channel. Explicit state transitions.
└── NO  → Team knows MVVM?
          ├── YES → MVVM: ViewModel + StateFlow + sealed UiState. Covers 85% of use cases.
          └── NO  → Start with MVVM. Graduate to MVI only when state complexity demands it.
```

### Room vs SQLDelight

```
KMP (Kotlin Multiplatform) planned or in use?
├── YES → SQLDelight. Cross-platform SQL generation for Android + iOS.
└── NO  → Need Android ecosystem integration (Paging 3, WorkManager)?
          ├── YES → Room. Full Jetpack integration + compile-time SQL verification.
          └── NO  → Room. It's the default. Google's recommended persistence library.
```

### Hilt vs Koin vs Manual DI

```
Build speed the overwhelming concern AND < 10 ViewModels?
├── YES → Manual DI + AppContainer singleton. Zero annotation processing cost.
└── NO  → Need lifecycle-scoped components (ViewModel, Fragment, Service)?
          ├── YES → Hilt. Compile-time DI graph verification + scope tree. 5-10% build overhead.
          └── NO  → Hilt. Even without scopes, compile-time safety justifies the cost.
```
**Koin**: Prefer if team needs runtime DI with DSL definitions. Risk: runtime crash for missing deps vs Hilt's compile-time error.

### Navigation Compose vs Fragments

```
UI built entirely with Compose (no XML screens)?
├── YES → Navigation Compose. Type-safe routes, NavHost composable, bottom nav support.
└── NO  → Existing deep link infrastructure with Navigation XML?
          ├── YES → Keep Nav XML + Fragments. Incremental Compose interop via AndroidView.
          └── NO  → Migrate new screens to Nav Compose. Interop existing Fragments.
```

### ProGuard/R8 Configuration

```
Using reflection, serialization, or annotation processors requiring class names?
├── YES → Start with default rules. Add @Keep on serialized classes. Custom -keep ONLY after crash in release.
└── NO  → R8 enabled with minifyEnabled true. Zero custom rules in proguard-rules.pro. Libraries ship consumer rules.
```

## Core Workflow

<!-- QUICK: 30s -- scan phase titles -->

### Phase 1 (~15 min): Project Setup & Architecture
1. **Gradle convention plugins** via `buildSrc` — shared `android { }` blocks, no copy-paste
2. **Feature-based modules**: `:feature:auth`, `:feature:feed`, not layer-based `:data`, `:domain`, `:ui`
3. **Hilt**: `@HiltAndroidApp` on Application, `@AndroidEntryPoint` on Activity, `@HiltViewModel` on ViewModels
4. **Theme**: `MaterialTheme` with `dynamicColor` on Android 12+, fallback `lightColorScheme()`/`darkColorScheme()`
5. **Navigation**: Single `NavHost` per Activity. Each feature contributes `NavGraphBuilder` extensions.

### Phase 2 (~30 min): Compose UI Implementation
1. **Screen = one @Composable**. Extract sub-composables for reuse. Screen receives NavController + ViewModel.
2. **State**: `val uiState by viewModel.uiState.collectAsStateWithLifecycle()`. Sealed `UiState`: Loading, Success, Error, Empty.
3. **LazyColumn**: `key = { it.id }` for stable recomposition. `remember` for expensive calcs inside items.
4. **Scaffold pattern**: `Scaffold` with `topBar`, `bottomBar`, `floatingActionButton`, `snackbarHostState`.
5. **Side effects**: `LaunchedEffect(key)` for one-shot, `DisposableEffect` for cleanup, `rememberCoroutineScope()` for user-triggered suspend calls.
> See [references/jetpack-compose-patterns.md](references/jetpack-compose-patterns.md) for the full catalog.

### Phase 3 (~20 min): ViewModel & State
1. **ViewModel lifecycle**: `@HiltViewModel class VM @Inject constructor(repo: Repo) : ViewModel()`. Survives config changes.
2. **StateFlow exposure**: `private val _uiState = MutableStateFlow(UiState.Loading)` → `val uiState: StateFlow<UiState> = _uiState.asStateFlow()`. Never `LiveData` for new code.
3. **One-shot events**: `Channel<UiEvent>(Channel.BUFFERED)` → `receiveAsFlow()`. For navigation, snackbar, dialog.
4. **Error handling**: `viewModelScope.launch { try { ... } catch (e: Exception) { _uiState.value = UiState.Error(e.message) } }`.
5. **Testing**: `runTest { vm.uiState.test { assertEquals(Loading, awaitItem()); vm.load(); assertEquals(Success(data), awaitItem()) } }`.

### Phase 4 (~20 min): Background Processing
1. **Deferrable work**: `WorkManager` — must complete even if app exits. `CoroutineWorker.doWork()` is suspend.
2. **Constraints**: `NetworkType.UNMETERED`, `BatteryNotLow`. Respect user resources.
3. **Foreground Services**: User-visible tasks (media, navigation, download). Non-dismissible notification within 5s. Android 14+ requires type-specific permission.
4. **Exact alarms**: `AlarmManager.setExactAndAllowWhileIdle()`. Requires `SCHEDULE_EXACT_ALARM`. Fallback to WorkManager.
5. Return `Result.success()`, `Result.failure()`, or `Result.retry()` from `doWork()`.

### Phase 5 (~15 min): Resources & Localization
1. **String resources**: `strings.xml` for all user-facing text. `stringResource()` in Compose. Zero hardcoded strings in Kotlin files.
2. **Dark theme**: `darkColorScheme()` in theme. 4.5:1 contrast minimum. Test with forced night mode.
3. **Image assets**: Vector drawables (icons < 200dp), WebP (photos), adaptive icons (foreground + background layers).
4. **Dynamic color**: `dynamicLightColorScheme(context)` / `dynamicDarkColorScheme(context)` on Android 12+.

### Phase 6 (~30 min): Testing Strategy

**Unit tests with JUnit5 + MockK + Turbine:**

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class FeedViewModelTest {
    @get:Rule val mainDispatcherRule = MainDispatcherRule()
    private val repository: FeedRepository = mockk(relaxed = true)
    private lateinit var viewModel: FeedViewModel

    @Before fun setup() { viewModel = FeedViewModel(repository) }

    @Test fun `emits Loading then Success`() = runTest {
        val posts = listOf(Post("1", "Title", "Body"))
        coEvery { repository.getFeed(any()) } returns flowOf(Resource.Success(posts))
        viewModel.uiState.test {
            assertThat(awaitItem()).isInstanceOf(FeedUiState.Loading::class.java)
            assertThat((awaitItem() as FeedUiState.Success).posts).hasSize(1)
            cancelAndIgnoreRemainingEvents()
        }
    }
}
// testImplementation("io.mockk:mockk:1.13.13")
// testImplementation("app.cash.turbine:turbine:1.2.0")
// testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.9.0")
```

**Compose UI tests with test tags:**

```kotlin
@RunWith(AndroidJUnit4::class)
class FeedScreenTest {
    @get:Rule val composeTestRule = createComposeRule()

    @Test fun `shows error and retry on failure`() {
        composeTestRule.setContent {
            FeedScreen(uiState = FeedUiState.Error("No internet", retryAction = {}), ...)
        }
        composeTestRule.onNodeWithTag("error_retry_button").assertIsDisplayed()
        composeTestRule.onNodeWithTag("error_message").assertTextEquals("No internet")
    }
}
// androidTestImplementation("androidx.compose.ui:ui-test-junit4")
// debugImplementation("androidx.compose.ui:ui-test-manifest")
```

**Room DAO tests with in-memory database:**

```kotlin
@RunWith(AndroidJUnit4::class)
class ProductDaoTest {
    private lateinit var db: AppDatabase
    private lateinit var dao: ProductDao

    @Before fun setup() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        db = Room.inMemoryDatabaseBuilder(context, AppDatabase::class.java).build()
        dao = db.productDao()
    }
    @After fun teardown() { db.close() }

    @Test fun `upsert inserts or replaces products`() = runTest {
        dao.upsertProducts(listOf(ProductEntity("1", "Test", 999, "", "cat1")))
        assertThat(dao.getProductById("1")).isNotNull()
    }
}
```

### Phase 7 (~30 min): Background Work — WorkManager & Foreground Services

```kotlin
// Period sync with constraints — Android enforces 15 min minimum interval
@HiltWorker
class DataSyncWorker @AssistedInject constructor(
    @Assisted context: Context,
    @Assisted params: WorkerParameters,
    private val syncRepo: SyncRepository,
) : CoroutineWorker(context, params) {
    override suspend fun doWork(): Result {
        setForeground(ForegroundInfo(1001, createSyncNotification()))
        return try {
            syncRepo.syncPendingChanges()
            Result.success()
        } catch (e: IOException) {
            if (runAttemptCount < 3) Result.retry() else Result.failure()
        }
    }
    companion object {
        fun enqueue(ctx: Context) {
            WorkManager.getInstance(ctx).enqueueUniquePeriodicWork(
                "periodic_sync", ExistingPeriodicWorkPolicy.KEEP,
                PeriodicWorkRequestBuilder<DataSyncWorker>(15, TimeUnit.MINUTES)
                    .setConstraints(Constraints.Builder()
                        .setRequiredNetworkType(NetworkType.CONNECTED)
                        .setRequiresBatteryNotLow(true).build())
                    .build()
            )
        }
    }
}
```

```xml
<!-- AndroidManifest.xml foreground service declarations -->
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_DATA_SYNC" />
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
<service android:name=".service.UploadService"
    android:foregroundServiceType="dataSync" android:exported="false" />
```

### Phase 8 (~20 min): Play Store Deployment

```kotlin
// app/build.gradle.kts — signing from CI env, NEVER commit keystore
android {
    signingConfigs {
        create("release") {
            storeFile = rootProject.file("upload-keystore.jks")
            storePassword = System.getenv("KEYSTORE_PASSWORD")
            keyAlias = System.getenv("KEY_ALIAS")
            keyPassword = System.getenv("KEY_PASSWORD")
        }
    }
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            isMinifyEnabled = true; isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
}
```

**Play Console pre-submission checklist:**
1. `targetSdkVersion 35` — required within 1 year of Android 15 release
2. Privacy policy URL in Play Console AND in-app (mandatory for personal data collection)
3. Data safety form: declare ALL data types collected/shared
4. IARC content rating questionnaire completed
5. `android:debuggable="false"` in release manifest (Play rejects debuggable APKs)
6. `ndk { abiFilters += listOf("arm64-v8a", "x86_64") }` if any native code
7. Screenshots: 2 phone (6.5"), 7" tablet, 10" tablet for tablet-supported apps
8. Permissions Declaration Form for background location, `QUERY_ALL_PACKAGES`, `MANAGE_EXTERNAL_STORAGE`
9. Enroll in Play App Signing — verify upload key SHA-1 matches Console
10. Managed publishing enabled for controlled staged rollout (10% → 50% → 100%)

```kotlin
// In-app review API — max once/30 days, Google-enforced, never show custom prompt
// implementation("com.google.android.play:review-ktx:2.0.1")
fun requestInAppReview(activity: Activity) {
    val manager = ReviewManagerFactory.create(activity)
    manager.requestReviewFlow().addOnCompleteListener { request ->
        if (request.isSuccessful) manager.launchReviewFlow(activity, request.result)
    }
}

// Billing 7.x — subscriptions and one-time purchases
// implementation("com.android.billingclient:billing-ktx:7.1.1")
// Must acknowledge purchases within 3 days or Google auto-refunds
// Must handle pending purchases (slow payment methods in India, Brazil)
```

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `mobile-developer` | Cross-platform architecture, offline-first patterns, push notification strategy | Before Android-only decisions that should align with iOS |
| `ui-ux-designer` | Material Design 3 spec, screen mockups, interaction patterns, a11y requirements | Before implementing Compose UI |
| `backend-developer` | REST/GraphQL API with Android-specific optimizations, push payloads | Before integrating network layer |
| `api-designer` | OpenAPI 3.1 spec, SDK generation, rate limits | Before writing Retrofit/Ktor interfaces |
| `database-designer` | ERD, Room schema decisions, indexing for mobile queries | Before defining Room @Entity classes |
| `accessibility-auditor` | WCAG 2.2 AA mapped to Android: content descriptions, focus, touch targets | Before release; Play Store pre-launch report |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `qa-engineer` | AAB build, device coverage plan, Espresso/Compose test harness, performance baselines | QA blocked without build and test config |
| `security-reviewer` | R8 mapping, Keystore implementation, cert pinning, root detection | Security review can't assess Android attack surface |
| `performance-engineer` | Profile data, baseline profiles, macrobenchmark results, APK size breakdown | Performance optimization needs instrumented measurement |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| New Gradle dependency with .so libraries | Security, Release Manager | Binary size impact, supply chain security |
| `minSdk` or `targetSdk` change | QA, DevOps | Device coverage change, Play Store requirement |
| New Android permission added | Security, UI/UX Designer | Rationale dialog, privacy review |
| Play Store pre-launch report violation | QA, Accessibility Auditor | Fix before production |
| ProGuard/R8 rule added | Performance, Release Manager | APK size regression, obfuscation verification |

### Escalation Path

```
Play Store rejection? → Release Manager → Legal Advisor
Security vulnerability? → Security Engineer → Compliance Officer
Architecture cross-cut with iOS? → Mobile Developer → System Architect
Critical performance regression? → Performance Engineer → CTO Advisor
Accessibility blockers? → Accessibility Auditor → Compliance Officer
```

## Proactive Triggers

These are signals that should trigger the Android developer to investigate — no one needs to tag you.

| Trigger | Immediate Action |
|---------|-----------------|
| "ANR rate spiked to 0.5%+ in Play Console" | Android Vitals >0.47% ANR triggers bad-behavior badge, deprioritizing search ranking. Audit main-thread blocking: grep for `Thread.sleep()`, `socket.connect()` without timeout, Room queries outside coroutine. Enable `StrictMode.detectAll()` in debug builds (`penaltyDeath()` catches violations instantly). Profile with CPU Profiler — look for >5s blocking on main thread. **Impact: $20K-$50K in lost organic installs from search rank drop.** |
| "Cold start >2s on low-end devices (Android Vitals)" | 20% uninstall rate for apps exceeding 2s cold start. Audit `Application.onCreate()`: move content providers to AndroidX Startup `Initializer<T>` with lazy init. Move heavy I/O to `Dispatchers.Default`. Generate baseline profile via `BaselineProfileRule.collect()` in Macrobenchmark. Profile with `systrace --app=com.example`. **Impact: $15K-$30K in user churn and uninstalls.** |
| "OutOfMemoryError — bitmap-related crashes in production" | Each OOM crash on a low-RAM device = ~8% session abandonment rate. Audit all image loading: Glide `.override(width, height)` or Coil `.size(width, height)` on every load. Profile heap dump: look for `byte[]` allocations >10MB. Set `android:largeHeap="false"` (true masks leaks). Downsample to 2× display at most. **Impact: $8K-$25K per month in lost ARPU from crash-affected cohorts.** |
| "Play Store listing rejected — policy violation" | Background location requires prominent disclosure BEFORE system dialog + in-app video demo. `QUERY_ALL_PACKAGES` needs Play Console declaration. `MANAGE_EXTERNAL_STORAGE` requires file manager/video justification + Google review. Each rejection = 3-7 day re-review delay. **Impact: $5K-$15K per rejection cycle in delayed launch revenue.** |
| "Compose screen recomposes 50+ times on simple scroll" | Users spend 40% less time in janky apps. Layout Inspector recomposition counts: unstable lambdas (inline `Modifier`), non-remembered callbacks, data classes without `@Stable`. Replace `mutableStateOf` in ViewModel with `StateFlow` + `collectAsStateWithLifecycle()`. Enable `composeCompiler { enableStrongSkippingMode = true }` (Compose 1.7+). **Impact: $15K-$30K in reduced engagement and session time.** |
| "App uses 30% battery/hour — WorkManager continuously" | 1★ "battery drain" reviews are the #2 reason for uninstall (after crashes). Verify `PeriodicWorkRequest` interval ≥15 min. Constraints MUST include `NetworkType.UNMETERED` for large transfers. Foreground Service must call `stopForeground()` within 3 min (Android 14+ limit). Profile with Battery Historian. **Impact: $10K-$25K in 1-star review cascade and uninstall rate spike.** |
| "Release APK 3× debug size — R8 not running" | APK size >150MB loses 20% install conversion on cellular. Check `isMinifyEnabled = true` AND `isShrinkResources = true` in release. Run APK Analyzer → sort by raw size. `resConfigs("en")` removes all non-English resources from libraries. Enable `android.enableR8.fullMode=true` in `gradle.properties`. **Impact: $5K-$10K in lost installs + CDN costs for oversized downloads.** |
| "TalkBack reads 'unlabeled button' on half the UI" | ADA Title III lawsuits settle for $10K-$50K. Play Store pre-launch report flags a11y. Every `IconButton`, `FloatingActionButton`, `Image` without adjacent text needs `contentDescription`. Run Accessibility Scanner from Play Store. Group elements with `semantics(mergeDescendants = true)`. **Impact: $10K-$50K in accessibility lawsuit risk + Play Store pre-launch warnings.** |


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "android-developer",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

### State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

### Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## What Good Looks Like

> Every Compose screen handles three states (loading/success/error) as a sealed interface with zero blank screens on failure. Every network call is wrapped in a Repository with offline-first caching via Room — users see cached data instantly, network updates arrive async. Every coroutine is scoped to `viewModelScope` or `lifecycleScope` — zero `GlobalScope` instances. Every `Image`, `IconButton`, and interactive composable has `contentDescription`. Cold start <500ms on Galaxy A14 (4GB RAM, eMMC). Scrolls at locked 60fps in `LazyColumn` with 0 dropped frames in systrace. APK <30MB download.

> `AndroidManifest.xml` has `android:supportsRtl="true"`, layout mirrors correctly in Arabic/Hebrew. Pseudo-localized strings (`en-XA`) pass without truncation. R8 enabled in release with `isMinifyEnabled = true` AND `isShrinkResources = true`. `proguard-rules.pro` contains zero custom `-keep` rules — all libraries ship consumer rules. `app/build.gradle.kts` uses `composeBom` for version management, KSP instead of kapt. Baseline profiles generated via Macrobenchmark and included in every AAB. Room schema exported with `exportSchema = true`, migration tests validate every version path against production database snapshots.

### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | ui-ux-designer | Material Design 3 design system, screen mockups with a11y annotations, interaction patterns, component specs |
| **This** | android-developer | Native Compose implementation: UI, ViewModel, Room, Retrofit, WorkManager, Hilt, Gradle, Play Store AAB |
| **After** | qa-engineer | Compose/Espresso tests, device coverage matrix, performance baselines, accessibility audit pass |

Common chains:
- **Design to Play Store**: ui-ux-designer → android-developer → qa-engineer → release-manager
- **API to Android app**: api-designer → backend-developer → android-developer → security-reviewer
- **Feature delivery**: product-strategist → android-developer → performance-engineer → play-store-deployment

## Deliberate Practice

### The Android Improvement Loop
1. **Install on a $150 Galaxy A14** — 4GB RAM, eMMC storage. Use as daily driver for one day.
2. **Find every friction point** — Slow startup? Jank? OOM? ANR? Permission denied?
3. **Profile and fix** — CPU Profiler, Memory Profiler, Battery Historian. Fix the worst offender.
4. **Repeat monthly** with a different budget device. Your app behaves differently on all of them.

### Practice Routines
| Skill Level | Practice | Frequency | Expected Result |
|-------------|----------|-----------|-----------------|
| Novice → Competent | Build same screen in XML + Compose + Compose MVI. Compare line count, testability, recomposition. | Monthly | Understands when Compose improves vs adds complexity |
| Competent → Expert | Enable StrictMode with penaltyDeath(). Fix every violation: disk reads, network, leaked closeables. | Quarterly | App verified clean by platform tooling |
| Expert → Master | Build feature with only Android framework (no Jetpack, no Retrofit). Then rebuild with Jetpack. | Annually | Understands what Jetpack abstracts and where the real cost is |

### The One Thing
**Preload your app on Android Go edition (1-2GB RAM).** If it launches under 3s and doesn't crash scrolling 100 items, your architecture is solid.

## Gotchas

- **Memory leak from retained Fragment View Binding ($15K-$40K).** `_binding` not nulled in `onDestroyView()` retains old view references across config changes. Multiply by navigation across 5 screens and you've got an OOM chain on 2GB devices. Fix: `private var _binding: FragmentXBinding? = null`; null in `onDestroyView()`; use `binding` property with `checkNotNull` guard.

- **WorkManager periodic runs from start, not completion ($10K-$30K).** `PeriodicWorkRequest(15, MINUTES)` starts the 15-min clock at task *start*. If task takes 10 min, next run is 5 min later. If 20 min, next runs immediately. Produces battery drain and Play Store policy violations. Fix: Use `OneTimeWorkRequest` that enqueues next at end of `doWork()` for gap-from-completion scheduling.

- **R8 strips Retrofit suspend function parameters ($15K-$40K).** R8 removes unused params from `@GET` suspend functions, changing the Retrofit proxy signature. Release-only crash: `IllegalArgumentException: Wrong number of arguments` — debug builds work perfectly. Fix: Add `-keepclasseswithmembers class * { @retrofit2.http.* <methods>; }` or annotate interface methods with `@Keep`. ALWAYS test release builds before Play Store submission.

- **MutableStateFlow + data class stale recomposition ($5K-$15K).** Same `data class` value emitted on `MutableStateFlow` → Compose uses structural equality (`equals()`) and skips recomposition. Pull-to-refresh shows stale data — "refresh doesn't work" bugs that defy debugging. Fix: Add `refreshId: Long = System.currentTimeMillis()` to `UiState` for explicit recomposition triggers, or use `SnapshotMutationPolicy` with `referentialEqualityPolicy()`.

- **Lost upload keystore — app permanently unpublishable ($25K-$100K+).** Play App Signing uses two keys: your upload key (signing AABs submitted to Play) and Google's app signing key (signing distributed APK). Lose the upload key = can never update the app. Google cannot recover it. The listing must be unpublished, a new package name created, losing all installs, ratings, and Play Store search rank. Fix: Store upload keystore in password manager + encrypted backup. Enroll in Play App Signing immediately. Verify SHA-1 fingerprint matches Play Console before first release.

- **Room migration missing — every updater crashes ($20K-$50K).** New `@Entity` column without `Migration(start, end)` → `IllegalStateException: A migration from X to Y was required but not found` on database open. Every user updating from the previous version crashes on launch — crash rate spikes to 100% of updaters. Fix: Every schema change needs `Migration(oldVersion, newVersion) { database.execSQL("ALTER TABLE ...") }`. Export schema JSON with `exportSchema = true` and commit to VCS. Test migrations against production database snapshots.

- **ANR from main-thread network I/O ($30K-$100K).** `URL.readText()` or `socket.connect()` on main thread triggers "App isn't responding. Wait / Close" dialog at 5 seconds. Android Vitals dashboard tracks ANR rate; >0.47% triggers bad-behavior badge that deprioritizes your app in search results. Fix: Enable `StrictMode.setThreadPolicy(ThreadPolicy.Builder().detectAll().penaltyDeath().build())` in debug builds — it crashes INSTANTLY on violation so you catch it in development. Move all I/O to `withContext(Dispatchers.IO) { }`.

- **Compose recomposition from unstable parameters ($30K+ in lost engagement).** Passing a data class from an external library (e.g., `java.time.Instant`) to a `@Composable` function causes recomposition every frame — the Compose compiler marks external types as unstable. Layout Inspector shows recomposition count incrementing on every frame even with static data. Fix: Annotate data classes with `@Stable`, wrap external types in stable wrappers, or enable Strong Skipping Mode: `composeCompiler { enableStrongSkippingMode = true }` (Compose 1.7+). Check compiler metrics in `build/compose-metrics/` for unstable classes.

- **Play Store rejection for background location without prominent disclosure ($5K-$15K per rejection).** Google requires a prominent disclosure dialog BEFORE the system permission dialog explaining WHY background location is essential. Must submit a video demonstrating the feature. Include `android:foregroundServiceType="location"` in the service declaration. Without this: "Prominent disclosure not provided" rejection. Fix: Implement a custom dialog that appears before `requestPermissions()`, explaining the critical use case. Record the flow for Play Console submission. Test on internal track before production submission.

- **Configuration change destroys UI state — no SavedStateHandle ($20K+).** Rotating the device or enabling "Don't keep activities" in Developer Options destroys and recreates the Activity. If state is held in the Activity instead of ViewModel + `SavedStateHandle`, form inputs, scroll position, and navigation state are lost. `android:configChanges="orientation|screenSize"` is NOT a fix — it breaks multi-window, dark theme switching, and locale changes. Fix: All UI state in `ViewModel` + `SavedStateHandle`. Use `rememberSaveable` for Compose-local state. Test by rotating device mid-input on every form screen.

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "It works on my Pixel 9 Pro — we'll test budget devices after the feature freeze." | 95% of global Android users have mid-range or budget devices. A crash on a Galaxy A14 isn't a bug — it's a 1-star review. Budget device is primary test target. |
| "I'll add error handling after the happy path — let's not slow down for edge cases." | A blank screen on network failure looks like a crash. Every screen without error states silently fails in production. Error handling isn't polish — it's the difference between professional and prototype. |
| "We don't need TalkBack — user research didn't flag accessibility." | 15% of population has a disability. Play Store pre-launch report flags a11y. `contentDescription` is 40 characters. A 1-star accessibility review is forever. |
| "API key in local.properties isn't committed, so it's safe." | `BuildConfig` fields are compiled into the APK in plaintext. `strings app.apk` extracts them in seconds. Use Keystore + server proxy. |
| "Hilt adds 15% build time — manual DI is simpler." | Manual DI's cost is runtime: missing dependency crashes, no scope enforcement, no compile-time verification. One null-pointer crash costs more than Hilt's build overhead saves in a year. |

## Verification

- [ ] `./gradlew test` — all unit tests pass, no regressions
- [ ] `./gradlew connectedCheck` — Espresso/Compose tests pass on target device
- [ ] `./gradlew bundleRelease` — zero ProGuard/R8 warnings, no missing keep rules
- [ ] APK/AAB download size < 30MB, install size < 100MB (APK Analyzer)
- [ ] Test on budget device (Galaxy A14, 4GB RAM): cold start < 2s, no ANR, no OOM
- [ ] TalkBack: navigate entire app — every interactive element described, focus logical
- [ ] Airplane mode: every screen shows cached data or error+retry, not blank
- [ ] "Don't keep activities": app restores state after process death
- [ ] Dark mode: all screens pass 4.5:1 contrast, no hardcoded light colors
- [ ] `./gradlew lint` — zero new errors or warnings in release lint
- [ ] Baseline profile generated and included in AAB

## References

Detailed reference material loaded on demand:

- **Jetpack Compose Patterns**: See [references/jetpack-compose-patterns.md](references/jetpack-compose-patterns.md) — 20 patterns: state hoisting, ViewModel+StateFlow, sealed UiState, Scaffold, LazyColumn keys, side effects (LaunchedEffect, DisposableEffect, SideEffect), AndroidView interop, Material 3 theming with dynamic color, type-safe Navigation Compose, recomposition optimization
- **Android Architecture Patterns**: See [references/android-architecture-patterns.md](references/android-architecture-patterns.md) — MVVM with ViewModel+StateFlow+sealed UiState, MVI with Intent+State+Effect Channel, Clean Architecture (domain/data/presentation layers), UseCase pattern, Repository with offline-first caching, DI with Hilt, SavedStateHandle for process death
- **Kotlin Coroutines & Flow**: See [references/kotlin-coroutines-flow.md](references/kotlin-coroutines-flow.md) — Dispatcher selection (Main/IO/Default/Unconfined), structured concurrency, Flow vs StateFlow vs SharedFlow vs Channel, cold vs hot streams, exception handling (try/catch, catch operator, CoroutineExceptionHandler), cancellation, `callbackFlow`, `flowOn`, testing with `runTest` and Turbine
- **Room Database Guide**: See [references/room-database-guide.md](references/room-database-guide.md) — Entity, DAO, Database, embedded types, type converters, FTS (full-text search), SQL queries (raw and generated), multi-table JOINs and @Relation, migrations (Migration, AutoMigration, destructive fallback), exportSchema, testing with in-memory database
- **Android Build Variants**: See [references/android-build-variants.md](references/android-build-variants.md) — Build types (debug/release), product flavors (environment/region), flavor dimensions, signing configs (debug/release/CI env vars), build variants matrix, convention plugins via buildSrc, version catalogs (libs.versions.toml), resourceConfigs, abiFilters, splits (density/ABI)
- **Play Store Deployment**: See [references/play-store-deployment.md](references/play-store-deployment.md) — Play App Signing (upload key vs app signing key), AAB generation, internal/alpha/beta/production tracks, staged rollout (10%→50%→100%), in-app review API, Billing 7.x subscriptions/one-time, pre-launch report, policy compliance, Data safety form, IARC content rating, managed publishing
- **Android Accessibility**: See [references/android-accessibility.md](references/android-accessibility.md) — TalkBack navigation, contentDescription best practices, Compose semantics (semantics, mergeDescendants, invisibleToUser), touch target minimums (48dp), color contrast (4.5:1 text, 3:1 large text), focus order, live regions (AccessibilityLiveRegion), testing with Accessibility Scanner, WCAG 2.2 AA mapped to Android
- **Android Performance Optimization**: See [references/android-performance-optimization.md](references/android-performance-optimization.md) — Cold start optimization (launch themes, lazy content providers, baseline profiles), scroll jank (LazyColumn stable keys, recomposition counts, unstable parameters), memory management (bitmap downsampling, heap dump analysis, leak detection), APK size (R8 full mode, resource shrinking, ABI splits, resConfigs), Macrobenchmark with BaselineProfileRule, systrace/perfetto capture

**External references:**
- Android Developers — App Architecture Guide: <https://developer.android.com/topic/architecture>
- Jetpack Compose Documentation: <https://developer.android.com/develop/ui/compose>
- Now in Android (Google's reference app): <https://github.com/android/nowinandroid>
- Material Design 3 for Android: <https://m3.material.io/develop/android>
- Play Console Help — Policy Center: <https://play.google.com/console/about/policies/>
- Kotlin Coroutines Guide: <https://kotlinlang.org/docs/coroutines-guide.html>
- AndroidX Release Notes: <https://developer.android.com/jetpack/androidx/versions>
- Google Play Academy (Store listing best practices): <https://playacademy.exceedlms.com/>
