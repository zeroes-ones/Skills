# MVI Patterns — Android Reference

> Model-View-Intent with unidirectional data flow for Jetpack Compose. Immutable state, pure reducer functions, and deterministic UI rendering.

---

## Core MVI Loop

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   User Action ──► Intent ──► ViewModel ──► Reducer ──┐      │
│        ▲                                             │      │
│        │                                             ▼      │
│        └────────── View ◄── New State ◄──────────────┘      │
│                                                              │
│   STATE IS IMMUTABLE. Every action produces a new state.     │
│   State is a SINGLE sealed class/data class, not 10 vars.    │
└──────────────────────────────────────────────────────────────┘
```

---

## Complete Implementation — Search Screen

### State Definition

```kotlin
// Single source of truth for the entire screen
data class SearchState(
    val query: String = "",
    val results: List<SearchResult> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val recentSearches: List<String> = emptyList(),
    val isSearchFocused: Boolean = false,
    val selectedFilter: SearchFilter = SearchFilter.ALL
) {
    val hasResults: Boolean get() = results.isNotEmpty()
    val showEmptyState: Boolean get() = !isLoading && results.isEmpty() && query.isNotEmpty()
}

enum class SearchFilter { ALL, PRODUCTS, ARTICLES, USERS }

data class SearchResult(
    val id: String,
    val title: String,
    val subtitle: String,
    val type: SearchFilter,
    val thumbnailUrl: String?
)
```

### Intents (User Actions)

```kotlin
sealed interface SearchIntent {
    data class UpdateQuery(val query: String) : SearchIntent
    data class SubmitSearch(val query: String) : SearchIntent
    data class SelectResult(val resultId: String) : SearchIntent
    data class SelectFilter(val filter: SearchFilter) : SearchIntent
    data class RemoveRecentSearch(val query: String) : SearchIntent
    data object ClearQuery : SearchIntent
    data object Retry : SearchIntent
}
```

### Side Effects (One-shot events)

```kotlin
sealed interface SearchEffect {
    data class NavigateToDetail(val id: String) : SearchEffect
    data class ShowToast(val message: String) : SearchEffect
}
```

### ViewModel

```kotlin
@HiltViewModel
class SearchViewModel @Inject constructor(
    private val searchUseCase: SearchUseCase,
    private val recentSearchesRepository: RecentSearchesRepository
) : ViewModel() {

    private val _state = MutableStateFlow(SearchState())
    val state: StateFlow<SearchState> = _state.asStateFlow()

    private val _effects = Channel<SearchEffect>(Channel.BUFFERED)
    val effects: Flow<SearchEffect> = _effects.receiveAsFlow()

    private var searchJob: Job? = null

    init {
        viewModelScope.launch {
            _state.update { it.copy(
                recentSearches = recentSearchesRepository.getRecentSearches()
            )}
        }
    }

    fun onIntent(intent: SearchIntent) {
        when (intent) {
            is SearchIntent.UpdateQuery -> updateQuery(intent.query)
            is SearchIntent.SubmitSearch -> submitSearch(intent.query)
            is SearchIntent.SelectResult -> selectResult(intent.resultId)
            is SearchIntent.SelectFilter -> selectFilter(intent.filter)
            is SearchIntent.RemoveRecentSearch -> removeRecentSearch(intent.query)
            is SearchIntent.ClearQuery -> clearQuery()
            is SearchIntent.Retry -> retrySearch()
        }
    }

    private fun updateQuery(query: String) {
        _state.update { it.copy(query = query, error = null) }

        // Debounced search as user types
        searchJob?.cancel()
        if (query.length < 2) {
            _state.update { it.copy(results = emptyList()) }
            return
        }
        searchJob = viewModelScope.launch {
            delay(300) // 300ms debounce
            executeSearch(query)
        }
    }

    private fun submitSearch(query: String) {
        searchJob?.cancel()
        val trimmed = query.trim()
        if (trimmed.isEmpty()) return

        _state.update { it.copy(
            query = trimmed,
            isLoading = true,
            error = null
        )}
        recentSearchesRepository.addRecentSearch(trimmed)
        _state.update { it.copy(
            recentSearches = recentSearchesRepository.getRecentSearches()
        )}
        viewModelScope.launch { executeSearch(trimmed) }
    }

    private suspend fun executeSearch(query: String) {
        _state.update { it.copy(isLoading = true) }
        searchUseCase(query, _state.value.selectedFilter)
            .onSuccess { results ->
                _state.update { it.copy(
                    isLoading = false,
                    results = results,
                    error = null
                )}
            }
            .onFailure { error ->
                _state.update { it.copy(
                    isLoading = false,
                    error = error.message ?: "Search failed"
                )}
            }
    }

    private fun selectResult(resultId: String) {
        viewModelScope.launch {
            _effects.send(SearchEffect.NavigateToDetail(resultId))
        }
    }

    private fun selectFilter(filter: SearchFilter) {
        _state.update { it.copy(selectedFilter = filter) }
        val currentQuery = _state.value.query
        if (currentQuery.isNotEmpty()) {
            viewModelScope.launch { executeSearch(currentQuery) }
        }
    }

    private fun removeRecentSearch(query: String) {
        recentSearchesRepository.removeRecentSearch(query)
        _state.update { it.copy(
            recentSearches = recentSearchesRepository.getRecentSearches()
        )}
    }

    private fun clearQuery() {
        searchJob?.cancel()
        _state.update { it.copy(query = "", results = emptyList(), error = null) }
    }

    private fun retrySearch() {
        val currentQuery = _state.value.query
        if (currentQuery.isNotEmpty()) {
            viewModelScope.launch { executeSearch(currentQuery) }
        }
    }
}
```

### Composable View

```kotlin
@Composable
fun SearchScreen(
    viewModel: SearchViewModel = hiltViewModel(),
    onNavigateToDetail: (String) -> Unit
) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    // Collect one-shot effects
    LaunchedEffect(Unit) {
        viewModel.effects.collect { effect ->
            when (effect) {
                is SearchEffect.NavigateToDetail -> onNavigateToDetail(effect.id)
                is SearchEffect.ShowToast -> { /* Show snackbar */ }
            }
        }
    }

    Scaffold(
        topBar = {
            SearchBar(
                query = state.query,
                onQueryChange = { viewModel.onIntent(SearchIntent.UpdateQuery(it)) },
                onSearch = { viewModel.onIntent(SearchIntent.SubmitSearch(it)) },
                onClear = { viewModel.onIntent(SearchIntent.ClearQuery) },
                isFocused = state.isSearchFocused
            )
        }
    ) { padding ->
        Column(modifier = Modifier.padding(padding)) {
            // Filter chips
            FilterRow(
                selected = state.selectedFilter,
                onFilterSelected = { viewModel.onIntent(SearchIntent.SelectFilter(it)) }
            )

            // Content area
            when {
                state.isLoading -> SearchLoadingState()
                state.error != null -> SearchErrorState(
                    message = state.error!!,
                    onRetry = { viewModel.onIntent(SearchIntent.Retry) }
                )
                state.showEmptyState -> SearchEmptyState(query = state.query)
                state.hasResults -> SearchResultsList(
                    results = state.results,
                    onResultClick = { viewModel.onIntent(SearchIntent.SelectResult(it.id)) }
                )
                state.query.isEmpty() -> RecentSearchesList(
                    searches = state.recentSearches,
                    onSearchClick = { viewModel.onIntent(SearchIntent.SubmitSearch(it)) },
                    onRemoveClick = { viewModel.onIntent(SearchIntent.RemoveRecentSearch(it)) }
                )
            }
        }
    }
}
```

---

## MVI Unit Testing

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class SearchViewModelTest {

    @get:Rule
    val dispatcherRule = MainDispatcherRule()

    private val mockSearchUseCase: SearchUseCase = mock()
    private val mockRecentRepo: RecentSearchesRepository = mock()
    private lateinit var sut: SearchViewModel

    @Before
    fun setup() {
        whenever(mockRecentRepo.getRecentSearches()).thenReturn(emptyList())
        sut = SearchViewModel(mockSearchUseCase, mockRecentRepo)
    }

    @Test
    fun `UpdateQuery with short text clears results`() = runTest {
        sut.onIntent(SearchIntent.UpdateQuery("ab"))
        advanceUntilIdle()

        val state = sut.state.value
        assertThat(state.query).isEqualTo("ab")
        assertThat(state.results).isEmpty()
    }

    @Test
    fun `SubmitSearch with valid query loads results`() = runTest {
        val mockResults = listOf(SearchResult("1", "Test", "", SearchFilter.ALL, null))
        whenever(mockSearchUseCase.invoke(any(), any()))
            .thenReturn(Result.success(mockResults))

        sut.onIntent(SearchIntent.SubmitSearch("test query"))
        advanceUntilIdle()

        val state = sut.state.value
        assertThat(state.isLoading).isFalse()
        assertThat(state.results).hasSize(1)
        assertThat(state.error).isNull()
    }

    @Test
    fun `SubmitSearch failure sets error state`() = runTest {
        whenever(mockSearchUseCase.invoke(any(), any()))
            .thenReturn(Result.failure(RuntimeException("Network error")))

        sut.onIntent(SearchIntent.SubmitSearch("test"))
        advanceUntilIdle()

        val state = sut.state.value
        assertThat(state.error).contains("Network error")
        assertThat(state.isLoading).isFalse()
    }
}
```

---

## MVI vs MVVM — When to Choose

| Concern | MVVM | MVI |
|---|---|---|
| State shape | Multiple `StateFlow`/`LiveData` | Single immutable state class |
| Side effects | Mixed into ViewModel logic | Explicit `Channel<Effect>` |
| Debugging | Harder — state changes scattered | Easier — state is a single snapshot |
| Boilerplate | Lower | Higher (intents, effects, state class) |
| Best for | Simple screens, small teams | Complex screens, Compose, large teams |
| Compose fit | Good | Excellent — designed for it |
