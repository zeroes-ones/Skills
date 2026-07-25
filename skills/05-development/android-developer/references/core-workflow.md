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

