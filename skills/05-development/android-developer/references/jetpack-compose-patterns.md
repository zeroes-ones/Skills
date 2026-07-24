# Jetpack Compose Patterns — Android Developer Reference

> **Parent skill:** [android-developer](../SKILL.md) | **Load condition:** When implementing Compose UI or debugging recomposition issues

## State Hoisting Pattern

State flows down, events flow up. The composable that writes state is the composable that owns it.

```kotlin
// Stateless composable — receives state, emits events
@Composable
fun SearchBar(
    query: String,
    onQueryChange: (String) -> Unit,
    onSearch: () -> Unit,
    modifier: Modifier = Modifier,
) {
    TextField(
        value = query,
        onValueChange = onQueryChange,
        modifier = modifier.testTag("search_input"),
        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
        keyboardActions = KeyboardActions(onSearch = { onSearch() }),
    )
}

// Stateful parent — owns state, delegates rendering
@Composable
fun SearchScreen(viewModel: SearchViewModel = hiltViewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    SearchBar(
        query = uiState.query,
        onQueryChange = viewModel::onQueryChanged,
        onSearch = viewModel::onSearch,
    )
}
```

## ViewModel + StateFlow + Sealed UiState

The canonical Compose state pattern. ViewModel holds `StateFlow<UiState>`, Composable collects with `collectAsStateWithLifecycle()`.

```kotlin
// Sealed interface — one type per screen state
sealed interface FeedUiState {
    data object Loading : FeedUiState
    data class Success(val posts: List<Post>, val isRefreshing: Boolean = false) : FeedUiState
    data class Error(val message: String, val retry: () -> Unit) : FeedUiState
    data object Empty : FeedUiState
}

@HiltViewModel
class FeedViewModel @Inject constructor(
    private val repository: FeedRepository,
) : ViewModel() {

    private val _uiState = MutableStateFlow<FeedUiState>(FeedUiState.Loading)
    val uiState: StateFlow<FeedUiState> = _uiState.asStateFlow()

    init { loadFeed() }

    fun loadFeed() {
        viewModelScope.launch {
            _uiState.value = FeedUiState.Loading
            repository.getFeed()
                .catch { e -> _uiState.value = FeedUiState.Error(e.message ?: "Unknown error", ::loadFeed) }
                .collect { posts ->
                    _uiState.value = if (posts.isEmpty()) FeedUiState.Empty
                    else FeedUiState.Success(posts)
                }
        }
    }
}

@Composable
fun FeedScreen(viewModel: FeedViewModel = hiltViewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    when (val state = uiState) {
        is FeedUiState.Loading -> CircularProgressIndicator()
        is FeedUiState.Empty -> EmptyState()
        is FeedUiState.Error -> ErrorState(state.message, state.retry)
        is FeedUiState.Success -> FeedContent(state.posts, state.isRefreshing)
    }
}
```

## Scaffold Pattern — All Slots

```kotlin
@Composable
fun MainScreen() {
    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()
    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)

    ModalNavigationDrawer(
        drawerState = drawerState,
        drawerContent = { ModalDrawerSheet { /* Drawer items */ } }
    ) {
        Scaffold(
            topBar = { TopAppBar(title = { Text("App") }, navigationIcon = {
                IconButton(onClick = { scope.launch { drawerState.open() } }) {
                    Icon(Icons.Default.Menu, contentDescription = "Open menu")
                }
            })},
            bottomBar = { NavigationBar { /* Bottom nav items */ } },
            floatingActionButton = {
                FloatingActionButton(onClick = { /* FAB action */ }) {
                    Icon(Icons.Default.Add, contentDescription = "Create")
                }
            },
            snackbarHost = { SnackbarHost(snackbarHostState) },
        ) { innerPadding ->
            // Content with scaffold-aware padding
            Box(modifier = Modifier.padding(innerPadding)) { /* Screen content */ }
        }
    }
}
```

## LazyColumn Patterns

```kotlin
@Composable
fun PostList(posts: List<Post>, onPostClick: (String) -> Unit) {
    LazyColumn(
        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        // Sticky header
        stickyHeader { Text("Today", style = MaterialTheme.typography.titleSmall) }

        items(
            items = posts,
            key = { it.id },  // CRITICAL: stable key prevents identity confusion
            contentType = { "post_item" },  // Enables view type recycling
        ) { post ->
            PostCard(
                post = post,
                modifier = Modifier.animateItem(),
                onClick = { onPostClick(post.id) },
            )
        }

        // Loading indicator as footer
        item { if (isLoading) CircularProgressIndicator(modifier = Modifier.fillMaxWidth()) }

        // Auto-load more when reaching end
        val shouldLoadMore by remember {
            derivedStateOf {
                val lastVisible = listState.layoutInfo.visibleItemsInfo.lastOrNull()?.index ?: 0
                lastVisible >= listState.layoutInfo.totalItemsCount - 3 && !isLoading
            }
        }
        LaunchedEffect(shouldLoadMore) {
            if (shouldLoadMore) onLoadMore()
        }
    }
}
```

## Side-Effect API Decision Matrix

| API | When to Use | Example |
|-----|------------|---------|
| `LaunchedEffect(key)` | Suspend work tied to composition lifecycle | Load data when screen appears |
| `DisposableEffect(key)` | Setup/teardown with composition | Register/unregister listener |
| `SideEffect` | Sync with non-Compose state every recomposition | Update Toolbar title |
| `rememberCoroutineScope()` | User-triggered suspend calls | Button click → network call |
| `snapshotFlow` | Convert SnapshotStateList to Flow | Observe list changes reactively |

### LaunchedEffect — Data Loading on Screen Entry

```kotlin
@Composable
fun ProductDetailScreen(productId: String, viewModel: ProductViewModel = hiltViewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    LaunchedEffect(productId) {
        viewModel.loadProduct(productId)
    }

    // Never: LaunchedEffect(Unit) — it runs once and never re-triggers on param changes
}
```

### DisposableEffect — Observer Lifecycle

```kotlin
@Composable
fun ConnectivityAwareContent(viewModel: MainViewModel = hiltViewModel()) {
    DisposableEffect(Unit) {
        val observer = object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(network: Network) { viewModel.onNetworkAvailable() }
            override fun onLost(network: Network) { viewModel.onNetworkLost() }
        }
        val cm = LocalContext.current.getSystemService<ConnectivityManager>()!!
        cm.registerDefaultNetworkCallback(observer)
        onDispose { cm.unregisterNetworkCallback(observer) }
    }
}
```

### rememberCoroutineScope — User-Triggered Suspend

```kotlin
@Composable
fun SubmitButton(onSubmit: suspend () -> Result) {
    val scope = rememberCoroutineScope()
    var isLoading by remember { mutableStateOf(false) }

    Button(
        onClick = {
            scope.launch {
                isLoading = true
                val result = onSubmit()
                isLoading = false
                // handle result
            }
        },
        enabled = !isLoading,
    ) { Text(if (isLoading) "Submitting..." else "Submit") }
}
```

## @Stable and @Immutable — Recomposition Control

```kotlin
// @Stable: Compose compiler trusts equality check — skips if equals() says same
@Stable
data class UserProfile(
    val id: String,
    val name: String,
    val avatarUrl: String,
)

// @Immutable: values NEVER change after construction — zero recomposition overhead
@Immutable
data class AppConfig(
    val apiBaseUrl: String,
    val enableExperimentalFeatures: Boolean,
)

// External types (java.time.Instant, etc.) are marked unstable by compiler.
// Wrap them in @Stable wrappers:
@Stable
data class StableInstant(val value: Long) {
    constructor(instant: java.time.Instant) : this(instant.toEpochMilli())
}
```

## derivedStateOf — Derived Values That Update Less Often

```kotlin
@Composable
fun FilteredList(items: List<Item>, query: String) {
    // Recalculated only when items or query changes, not on every recomposition
    val filteredItems by remember(items, query) {
        derivedStateOf { items.filter { it.name.contains(query, ignoreCase = true) } }
    }

    // Show active filter count
    val activeFilters by remember { derivedStateOf { filteredItems.size } }

    LazyColumn { items(filteredItems, key = { it.id }) { ItemRow(it) } }
}
```

## Navigation Compose — Type-Safe Routes

```kotlin
@Serializable sealed class Route {
    @Serializable data object Feed : Route()
    @Serializable data class PostDetail(val postId: String) : Route()
    @Serializable data class Profile(val userId: String, val showSettings: Boolean = false) : Route()
}

@Composable
fun AppNavGraph(navController: NavHostController = rememberNavController()) {
    NavHost(navController = navController, startDestination = Route.Feed) {
        composable<Route.Feed> { FeedScreen(onPostClick = { navController.navigate(Route.PostDetail(it)) }) }
        composable<Route.PostDetail> { PostDetailScreen(onProfileClick = { userId -> navController.navigate(Route.Profile(userId)) }) }
        composable<Route.Profile> { backStackEntry ->
            val route: Route.Profile = backStackEntry.toRoute()
            ProfileScreen(userId = route.userId, showSettings = route.showSettings)
        }
    }
}
```

## Material 3 Dynamic Color Theming

```kotlin
@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,  // Material You — Android 12+
    content: @Composable () -> Unit,
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> darkColorScheme()
        else -> lightColorScheme()
    }
    MaterialTheme(
        colorScheme = colorScheme,
        typography = AppTypography,
        shapes = AppShapes,
        content = content,
    )
}
```

## Compose + View Interop — AndroidView

```kotlin
@Composable
fun MapView(
    onMapReady: (GoogleMap) -> Unit,
    modifier: Modifier = Modifier,
) {
    // Wrap legacy View in Compose
    AndroidView(
        factory = { context ->
            MapView(context).apply {
                onCreate(null)
                onResume()
                getMapAsync(onMapReady)
            }
        },
        modifier = modifier.fillMaxSize(),
        update = { mapView -> mapView.onResume() },  // Called on recomposition
    )
}

@Composable
fun ComposeInXml() {
    // Embed Compose inside XML layout
    AndroidViewBinding(FragmentXmlBinding::inflate) {
        // Access binding properties
        ComposeView(context).apply { setContent { MyComposable() } }
    }
}
```

## Modifier Order Matters

```kotlin
// CORRECT: clickable FIRST so padding is inside the tap target
Modifier
    .clickable { }
    .padding(16.dp)
    .fillMaxWidth()

// WRONG: fillMaxWidth first, then padding (spills outside), then clickable on too-small area
Modifier
    .fillMaxWidth()
    .padding(16.dp)
    .clickable { }
```

## AnimatedVisibility

```kotlin
@Composable
fun ExpandableSection(expanded: Boolean, content: @Composable () -> Unit) {
    AnimatedVisibility(
        visible = expanded,
        enter = fadeIn() + expandVertically(),
        exit = fadeOut() + shrinkVertically(),
    ) { content() }
}

// AnimatedContent for state transitions
@Composable
fun StateAwareContent(uiState: UiState) {
    AnimatedContent(targetState = uiState, transitionSpec = {
        fadeIn() togetherWith fadeOut()
    }) { state ->
        when (state) {
            is UiState.Loading -> LoadingContent()
            is UiState.Success -> SuccessContent(state.data)
            is UiState.Error -> ErrorContent(state.message)
        }
    }
}
```

## Pull-to-Refresh with Material 3

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PullToRefreshList(
    isRefreshing: Boolean,
    onRefresh: () -> Unit,
    content: @Composable () -> Unit,
) {
    val pullRefreshState = rememberPullToRefreshState()
    Box(modifier = Modifier.nestedScroll(pullRefreshState.nestedScrollConnection)) {
        content()
        if (pullRefreshState.isRefreshing) {
            LaunchedEffect(true) { onRefresh() }
        }
        PullToRefreshContainer(
            state = pullRefreshState,
            modifier = Modifier.align(Alignment.TopCenter),
        )
    }
    LaunchedEffect(isRefreshing) {
        if (!isRefreshing) pullRefreshState.endRefresh()
    }
}
```

## Testing Patterns

```kotlin
@RunWith(AndroidJUnit4::class)
class FeedScreenTest {
    @get:Rule val composeTestRule = createEmptyComposeRule()

    @Before fun setup() {
        composeTestRule.setContent {
            AppTheme { FeedScreen(viewModel = fakeViewModel) }
        }
    }

    @Test fun `shows error state with retry button`() {
        val errorState = FeedUiState.Error("No internet") {}
        composeTestRule.setContent { FeedScreenContent(uiState = errorState) }
        composeTestRule.onNodeWithTag("error_message").assertTextEquals("No internet")
        composeTestRule.onNodeWithTag("error_retry_button").assertIsDisplayed()
    }

    @Test fun `clicking item navigates to detail`() {
        composeTestRule.onNodeWithTag("post_card_1").performClick()
        composeTestRule.onNodeWithTag("post_detail_screen").assertIsDisplayed()
    }
}
```

## Recomposition Optimization Checklist

- Use `@Stable` / `@Immutable` on data classes passed to Composables
- `key = { it.id }` in `LazyColumn items()` for stable identity
- `remember {}` for expensive calculations inside composition
- `derivedStateOf` for state that changes less frequently than its inputs
- Enable Strong Skipping Mode: `composeCompiler { enableStrongSkippingMode = true }` (Compose 1.7+)
- Check Compose compiler metrics: `build/compose-metrics/` for unstable class detection
- Never pass lambdas inline in Modifier — extract as `remember` references
- Use `contentType` in `LazyColumn items()` for view type recycling
- Profile with Layout Inspector → recomposition counts. Zero recompositions on static screens
- Enable `ComposeCompilerReports` to audit unstable parameters in every @Composable
