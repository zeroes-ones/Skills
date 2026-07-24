---
title: "Kotlin Coroutines & Flow — Full Android Guide"
author: Sandeep Kumar Penchala
date: 2026-07-24
---

## Core Concepts

Kotlin coroutines provide structured concurrency for Android — they're lightweight threads that don't block the calling thread. Combined with Flow (a cold asynchronous stream), they form the backbone of all modern Android data handling.

### The Mental Model

```
suspend fun = function that can pause and resume without blocking a thread
CoroutineScope = defines the lifecycle boundary for coroutines
Flow<T> = cold stream that emits values over time
StateFlow<T> = hot stream that always has a current value (replaces LiveData)
SharedFlow<T> = hot stream for broadcasting events to multiple collectors
Channel<T> = hot stream for communicating between coroutines (one-shot events)
```

## Dispatchers — Choosing the Right Thread

| Dispatcher | Uses | Never Use For |
|------------|------|---------------|
| `Dispatchers.Main` | UI updates, Compose state writes, `collectAsState` | Network calls, file I/O, database queries, JSON parsing |
| `Dispatchers.IO` | Network (Retrofit, Ktor), file I/O, Room database, bitmap decode | CPU-intensive computation (it has an elastic thread pool — too many parallel computations create thread contention) |
| `Dispatchers.Default` | CPU-intensive: sorting, filtering, parsing, encryption, image processing | I/O operations (it has a fixed thread pool = CPU cores — I/O would block compute threads) |
| `Dispatchers.Unconfined` | Testing only (`runTest`) | Production code — unpredictable thread, no structured concurrency guarantees |

### Correct Dispatcher Usage

```kotlin
@HiltViewModel
class FeedViewModel @Inject constructor(
    private val repository: PostRepository
) : ViewModel() {
    fun loadPosts() {
        viewModelScope.launch { // Main thread by default (viewModelScope dispatcher)
            _uiState.value = UiState.Loading
            val result = withContext(Dispatchers.IO) { // Switch to IO for network
                repository.fetchPosts() // retrofit suspend fun
            }
            // Back on Main — safe to update UI state
            result.onSuccess { posts -> _uiState.value = UiState.Success(posts) }
                  .onFailure { e -> _uiState.value = UiState.Error(e.message) }
        }
    }
}
```

## Structured Concurrency

All coroutines must be launched within a scope that controls their lifecycle. Android provides three built-in scopes:

```kotlin
// ViewModel — auto-cancels on ViewModel clear
viewModelScope.launch { /* ... */ }

// Activity/Fragment — auto-cancels on destroy
lifecycleScope.launch { /* ... */ }

// Lifecycle-aware: launches when STARTED, cancels when STOPPED
lifecycleScope.launchWhenStarted { /* deprecated — use repeatOnLifecycle */ }

// Correct way for lifecycle-aware collection
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.uiState.collect { state -> /* safe — paused when stopped */ }
    }
}
```

### The GlobalScope Trap

```kotlin
// NEVER do this in production:
GlobalScope.launch { /* leaks forever — never cancelled */ }

// NEVER scope to application lifecycle for data-loading coroutines:
ProcessLifecycleOwner.get().lifecycleScope.launch { /* only for analytics/ logging */ }
```

## Exception Handling

### try/catch in Coroutines

```kotlin
viewModelScope.launch {
    try {
        val data = withContext(Dispatchers.IO) { repository.fetchData() }
        _state.value = UiState.Success(data)
    } catch (e: IOException) {
        _state.value = UiState.Error("Network error: ${e.message}")
    } catch (e: Exception) {
        _state.value = UiState.Error("Unexpected error: ${e.message}")
    }
}
```

### CoroutineExceptionHandler (Top-Level)

```kotlin
val exceptionHandler = CoroutineExceptionHandler { _, throwable ->
    Log.e("AppCrash", "Uncaught coroutine exception", throwable)
    // Log to Crashlytics, show user-friendly message
}

viewModelScope.launch(exceptionHandler) {
    // If this throws and isn't caught, exceptionHandler catches it
    riskyOperation()
}
```

### supervisorScope — Failure Isolation

```kotlin
viewModelScope.launch {
    supervisorScope {
        // Child 1 failure doesn't cancel child 2
        launch { fetchPosts() }  // fails — logged
        launch { fetchUsers() }  // still runs
    }
}
```

## Flow — Cold Streams

Flow is a cold asynchronous stream — it only emits when collected. Each collector triggers a fresh execution.

```kotlin
fun fetchPostsFlow(): Flow<List<Post>> = flow {
    while (true) {
        val posts = api.getPosts() // suspend
        emit(posts)
        delay(30_000) // Poll every 30s
    }
}.flowOn(Dispatchers.IO) // upstream runs on IO
  .catch { e -> emit(emptyList()) } // error → emit fallback
  .retry(3) { e -> e is IOException } // retry on network errors
```

### Flow Operators Cheat Sheet

| Operator | Purpose | Example |
|----------|---------|---------|
| `map` | Transform each value | `flowOf(1,2,3).map { it * 2 }` → `2, 4, 6` |
| `filter` | Keep matching values | `flowOf(1,2,3).filter { it > 1 }` → `2, 3` |
| `flatMapLatest` | Switch to latest inner flow | Search debounce: query changes → cancel previous search, start new |
| `combine` | Combine latest from two flows | `combine(userFlow, settingsFlow) { u, s -> ... }` |
| `catch` | Handle upstream errors | `.catch { e -> emit(fallback) }` |
| `retry` | Retry on error | `.retry(3) { it is IOException }` |
| `onStart` | Emit before first value | `.onStart { emit(cachedValue) }` |
| `onEach` | Side-effect per emission | `.onEach { value -> logger.log(value) }` |
| `debounce` | Drop rapid emissions | `.debounce(300)` — wait 300ms of silence before emitting |
| `distinctUntilChanged` | Drop duplicate consecutive values | `.distinctUntilChanged()` |

## StateFlow — Hot Stream with Current Value

StateFlow is a hot stream that always has a current value. It's the replacement for `LiveData` in modern Android.

```kotlin
class UserRepository @Inject constructor(private val dao: UserDao) {
    // Room Flow → StateFlow with SharingStarted
    fun observeUsers(): StateFlow<List<User>> = dao.observeAll()
        .map { entities -> entities.map { it.toDomain() } }
        .stateIn(
            scope = CoroutineScope(Dispatchers.IO + SupervisorJob()), // or application scope
            started = SharingStarted.WhileSubscribed(5000), // stop upstream when no subscribers for 5s
            initialValue = emptyList()
        )
}
```

### SharingStarted Strategies

| Strategy | Behavior | Use Case |
|----------|----------|----------|
| `Eagerly` | Start immediately, never stop | App-wide data (auth state, theme) |
| `Lazily` | Start on first subscriber, never stop | Rare, simple cases |
| `WhileSubscribed(stopTimeoutMillis)` | Start on first subscriber, stop after `stopTimeout` ms with zero subscribers | **Default for ViewModels.** Stops waste when screen is gone |

### collectAsStateWithLifecycle vs collectAsState

```kotlin
// WRONG — collects even when app is in background (STOPPED)
val state by viewModel.uiState.collectAsState()

// RIGHT — pauses collection when lifecycle drops below STARTED
val state by viewModel.uiState.collectAsStateWithLifecycle()
// Requires: implementation("androidx.lifecycle:lifecycle-runtime-compose:x.y.z")
```

## SharedFlow — Hot Stream for Events

SharedFlow is for broadcasting events to multiple collectors. Unlike StateFlow, it doesn't hold a current value.

```kotlin
private val _errorEvents = MutableSharedFlow<String>(extraBufferCapacity = 10)
val errorEvents: SharedFlow<String> = _errorEvents.asSharedFlow()

// Emitting
_errorEvents.emit("Network timeout") // suspend — waits if buffer full
_errorEvents.tryEmit("Quick error") // non-suspend — drops if buffer full
```

## Channel — Coroutine-to-Coroutine Communication

Channel is for one-shot events between coroutines. Fits the "single consumer" pattern (navigation events, dialog triggers).

```kotlin
private val _navigationEvents = Channel<NavigationEvent>(Channel.BUFFERED)
val navigationEvents = _navigationEvents.receiveAsFlow() // Expose as cold Flow for single collector

viewModelScope.launch {
    _navigationEvents.send(NavigationEvent.GoToDetail(id))
}
```

## Room + Flow Integration

Room natively supports Flow and suspend functions. All DAO queries marked as `Flow` are observable — Room re-emits whenever the underlying table changes.

```kotlin
@Dao
interface PostDao {
    // Observable — emits whenever posts table changes
    @Query("SELECT * FROM posts ORDER BY created_at DESC")
    fun observeAllPosts(): Flow<List<PostEntity>>

    // Observable with parameter — re-emits when matching rows change
    @Query("SELECT * FROM posts WHERE author_id = :authorId")
    fun observeAuthorPosts(authorId: String): Flow<List<PostEntity>>

    // One-shot suspend — doesn't observe
    @Query("SELECT * FROM posts WHERE id = :postId")
    suspend fun getPost(postId: String): PostEntity?
}
```

## Testing Coroutines & Flow

### runTest — Standard Coroutine Test

```kotlin
class FeedViewModelTest {
    @Test
    fun `loadPosts emits success state`() = runTest {
        val fakeRepo = FakePostRepository(successPosts = listOf(Post("1", "Title")))
        val vm = FeedViewModel(fakeRepo)

        vm.loadPosts()
        advanceUntilIdle() // Process all pending coroutines

        assertEquals(UiState.Success(listOf(Post("1", "Title"))), vm.uiState.value)
    }
}
```

### Testing StateFlow

```kotlin
@Test
fun `uiState emits loading then success`() = runTest {
    val vm = FeedViewModel(fakeRepo)
    val states = mutableListOf<UiState>()

    val job = launch(UnconfinedTestDispatcher(testScheduler)) {
        vm.uiState.toList(states)
    }

    vm.loadPosts()
    advanceUntilIdle()

    assertEquals(2, states.size)
    assertIs<UiState.Loading>(states[0])
    assertIs<UiState.Success>(states[1])
    job.cancel()
}
```

### Testing with Turbine (Flow Testing Library)

```kotlin
@Test
fun `uiState emits in order`() = runTest {
    val vm = FeedViewModel(fakeRepo)
    vm.uiState.test {
        assertEquals(UiState.Loading, awaitItem())
        vm.loadPosts()
        assertEquals(UiState.Success(testPosts), awaitItem())
        cancelAndIgnoreRemainingEvents()
    }
}
```

## Common Pitfalls

### Pitfall 1: MutableStateFlow with data class — stale recomposition

```kotlin
data class UiState(val posts: List<Post>, val isLoading: Boolean)

// Problem: emitting the same data class value (equal by value) skips recomposition
_state.value = UiState(posts, false) // No recomposition if posts is the same

// Fix: add a nonce for forced recomposition
data class UiState(
    val posts: List<Post>,
    val isLoading: Boolean,
    val refreshId: Long = System.currentTimeMillis()
)
```

### Pitfall 2: Flow.collect() in a new coroutine per screen

```kotlin
// WRONG: new coroutine per recomposition — memory leak + extra collectors
@Composable
fun Screen(vm: ViewModel) {
    LaunchedEffect(Unit) { vm.data.collect { /* ... */ } }
}

// RIGHT: collectAsStateWithLifecycle handles lifecycle
@Composable
fun Screen(vm: ViewModel) {
    val data by vm.data.collectAsStateWithLifecycle()
}
```

### Pitfall 3: combine() emitting whenever any flow emits

```kotlin
// Problem: combine(flow1, flow2) { a, b -> ... } emits when EITHER flow emits
// If flow1 emits every 100ms and flow2 every 500ms, you get 14 emissions per second

// Fix: use sample() or debounce() on the combined output if rapid emissions are wasteful
combine(fastFlow, slowFlow) { a, b -> Pair(a, b) }
    .sample(200) // Emit at most every 200ms
```
