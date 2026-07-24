---
title: "Android Architecture Patterns — MVVM, MVI, Clean Architecture"
author: Sandeep Kumar Penchala
date: 2026-07-24
---

## Architecture Decision Framework

Choosing the right architecture for an Android app depends on complexity, team size, and long-term maintainability requirements. This guide covers the three proven patterns for Android: MVVM (Google-recommended default), MVI (Unidirectional Data Flow), and Clean Architecture (domain-centric, multi-module).

| Factor | MVVM | MVI | Clean Architecture |
|--------|------|-----|--------------------|
| Learning curve | Low (Android teams know this) | Medium (requires UDF discipline) | High (abstraction overhead) |
| State management | ViewModel + StateFlow | Reducer + StateFlow + Intent Channel | UseCase + Repository + ViewModel |
| Side-effect handling | Manual (Channel events) | Built-in (sealed Effect class) | Manual with UseCase boundaries |
| Testability | Good (ViewModel unit tests) | Excellent (pure reducer functions) | Excellent (every layer isolated) |
| Multi-module friendly | Yes (feature modules) | Yes (feature modules) | Yes (domain/data/presentation layers) |
| Suitable for | CRUD, list-detail, forms | Complex state machines, wizards | Enterprise, multi-team, 5+ year lifespan |

## MVVM (Model-View-ViewModel)

Google's recommended architecture. The ViewModel exposes state via `StateFlow` (or `LiveData` for legacy). The View observes state and renders UI. The ViewModel handles business logic and communicates with data sources.

### Layer Responsibilities

```
┌─────────────────────────────────────────────────┐
│ View (Activity/Fragment/Composable)             │
│ - Observes StateFlow from ViewModel             │
│ - Renders UI based on state                     │
│ - Forwards user events to ViewModel             │
│ - Zero business logic                           │
└────────────────┬────────────────────────────────┘
                 │ StateFlow<UiState>  ↑ events
┌────────────────▼────────────────────────────────┐
│ ViewModel                                       │
│ - Holds UI state as StateFlow<UiState>          │
│ - Processes user events                         │
│ - Calls Repository / UseCase                    │
│ - Maps domain data to UiState                   │
│ - Survives configuration changes                │
└────────────────┬────────────────────────────────┘
                 │ suspend fun / Flow<T>
┌────────────────▼────────────────────────────────┐
│ Repository                                      │
│ - Single source of truth                        │
│ - Coordinates local + remote data sources       │
│ - Implements caching strategy                   │
│ - Exposes Flow<T> for observable data           │
└──────┬─────────────────────────┬────────────────┘
       │                         │
┌──────▼────────┐      ┌─────────▼─────────┐
│ Local Data    │      │ Remote Data       │
│ Source        │      │ Source            │
│ (Room,        │      │ (Retrofit, Ktor)  │
│  DataStore)   │      │                   │
└───────────────┘      └───────────────────┘
```

### Complete MVVM Implementation

```kotlin
// data/model/User.kt
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey val id: String,
    val name: String,
    val email: String,
    val avatarUrl: String
)

// data/remote/UserApi.kt
interface UserApi {
    @GET("users/{id}")
    suspend fun getUser(@Path("id") userId: String): UserDto
}

// data/remote/UserDto.kt
data class UserDto(val id: String, val name: String, val email: String, val avatar_url: String)

fun UserDto.toEntity() = UserEntity(id, name, email, avatar_url)

// data/local/UserDao.kt
@Dao
interface UserDao {
    @Query("SELECT * FROM users WHERE id = :userId")
    fun observeUser(userId: String): Flow<UserEntity?>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: UserEntity)
}

// data/repository/UserRepository.kt
class UserRepository @Inject constructor(
    private val api: UserApi,
    private val dao: UserDao
) {
    fun observeUser(userId: String): Flow<UserEntity?> = dao.observeUser(userId)

    suspend fun refreshUser(userId: String): Result<UserEntity> = runCatching {
        val dto = api.getUser(userId)
        val entity = dto.toEntity()
        dao.insertUser(entity)
        entity
    }
}

// ui/user/UserUiState.kt
sealed class UserUiState {
    data object Loading : UserUiState()
    data class Success(val user: UserEntity) : UserUiState()
    data class Error(val message: String, val retry: () -> Unit) : UserUiState()
}

// ui/user/UserViewModel.kt
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository,
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {
    private val userId: String = savedStateHandle["userId"]!!

    val uiState: StateFlow<UserUiState> = repository.observeUser(userId)
        .map { entity -> if (entity != null) UserUiState.Success(entity) else UserUiState.Loading }
        .catch { e -> emit(UserUiState.Error(e.message ?: "Error", ::refresh)) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), UserUiState.Loading)

    fun refresh() {
        viewModelScope.launch {
            repository.refreshUser(userId)
        }
    }
}

// ui/user/UserScreen.kt
@Composable
fun UserScreen(
    viewModel: UserViewModel = hiltViewModel(),
    onBack: () -> Unit
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    Scaffold(topBar = { TopAppBar(title = { Text("Profile") }, navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Default.ArrowBack, "Back") } }) }) { padding ->
        Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
            when (val state = uiState) {
                is UserUiState.Loading -> CircularProgressIndicator()
                is UserUiState.Error -> Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(state.message); Button(onClick = state.retry) { Text("Retry") }
                }
                is UserUiState.Success -> UserContent(state.user)
            }
        }
    }
}
```

## MVI (Model-View-Intent)

MVI is a strict Unidirectional Data Flow (UDF) pattern. User actions are modeled as `Intent`s, processed by a reducer that produces a new `State`, and rendered as UI. Side effects are modeled as a separate `Effect` channel.

```
Intent → ViewModel.processIntent(Intent) → reduce(State, Intent) → new State → UI
                                                           ↓
                                                     Side Effect → Channel → UI (one-shot)
```

### Complete MVI Implementation

```kotlin
// ui/search/SearchContract.kt
data class SearchState(
    val query: String = "",
    val results: List<SearchResult> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
)

sealed class SearchIntent {
    data class QueryChanged(val query: String) : SearchIntent()
    data object Search : SearchIntent()
    data class ResultClicked(val result: SearchResult) : SearchIntent()
    data object ClearError : SearchIntent()
}

sealed class SearchEffect {
    data class NavigateToDetail(val id: String) : SearchEffect()
    data class ShowSnackbar(val message: String) : SearchEffect()
}

// ui/search/SearchViewModel.kt
@HiltViewModel
class SearchViewModel @Inject constructor(
    private val searchRepository: SearchRepository
) : ViewModel() {
    private val _state = MutableStateFlow(SearchState())
    val state: StateFlow<SearchState> = _state.asStateFlow()

    private val _effect = Channel<SearchEffect>(Channel.BUFFERED)
    val effect: Flow<SearchEffect> = _effect.receiveAsFlow()

    fun processIntent(intent: SearchIntent) {
        when (intent) {
            is SearchIntent.QueryChanged -> {
                _state.update { it.copy(query = intent.query, error = null) }
            }
            is SearchIntent.Search -> {
                viewModelScope.launch {
                    _state.update { it.copy(isLoading = true, error = null) }
                    searchRepository.search(_state.value.query)
                        .onSuccess { results -> _state.update { it.copy(isLoading = false, results = results) } }
                        .onFailure { e -> _state.update { it.copy(isLoading = false, error = e.message) } }
                }
            }
            is SearchIntent.ResultClicked -> {
                viewModelScope.launch { _effect.send(SearchEffect.NavigateToDetail(intent.result.id)) }
            }
            is SearchIntent.ClearError -> {
                _state.update { it.copy(error = null) }
            }
        }
    }
}

// ui/search/SearchScreen.kt
@Composable
fun SearchScreen(
    viewModel: SearchViewModel = hiltViewModel(),
    onNavigateToDetail: (String) -> Unit
) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    val snackbarHostState = remember { SnackbarHostState() }

    LaunchedEffect(Unit) {
        viewModel.effect.collect { effect ->
            when (effect) {
                is SearchEffect.NavigateToDetail -> onNavigateToDetail(effect.id)
                is SearchEffect.ShowSnackbar -> snackbarHostState.showSnackbar(effect.message)
            }
        }
    }

    Scaffold(snackbarHost = { SnackbarHost(snackbarHostState) }) { padding ->
        Column(Modifier.padding(padding)) {
            OutlinedTextField(
                value = state.query,
                onValueChange = { viewModel.processIntent(SearchIntent.QueryChanged(it)) },
                label = { Text("Search") },
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                keyboardActions = KeyboardActions(onSearch = { viewModel.processIntent(SearchIntent.Search) })
            )
            if (state.isLoading) LinearProgressIndicator(Modifier.fillMaxWidth())
            state.error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
            LazyColumn {
                items(state.results, key = { it.id }) { result ->
                    Text(result.title, Modifier.clickable { viewModel.processIntent(SearchIntent.ResultClicked(result)) })
                }
            }
        }
    }
}
```

## Clean Architecture

Clean Architecture separates code into layers with strict dependency rules: inner layers know nothing about outer layers. Dependencies point inward. The domain layer is pure Kotlin with zero Android dependencies.

```
Presentation (Compose + ViewModel + Hilt)
    ↓ depends on
Domain (UseCase + Repository interface + Entity)
    ↑ implemented by
Data (Repository impl + Room + Retrofit)
```

### Multi-Module Setup

```
app/                           ← application module, wires everything
├── feature/feed/              ← presentation + domain for feed
├── feature/auth/              ← presentation + domain for auth
├── core/network/              ← Retrofit, OkHttp, interceptors
├── core/database/             ← Room, DAOs, entities
├── core/model/                ← shared domain entities, UseCase base
└── core/ui/                   ← shared Compose components, theme
```

### Domain Layer (Pure Kotlin, No Android Deps)

```kotlin
// core/model/src/main/kotlin/com/app/model/Post.kt
data class Post(val id: String, val title: String, val body: String, val authorName: String)

// feature/feed/domain/src/main/kotlin/com/app/feed/domain/PostRepository.kt
interface PostRepository {
    fun observePosts(): Flow<List<Post>>
    suspend fun refreshPosts(): Result<Unit>
    suspend fun createPost(title: String, body: String): Result<Post>
}

// feature/feed/domain/src/main/kotlin/com/app/feed/domain/GetFeedUseCase.kt
class GetFeedUseCase @Inject constructor(private val repository: PostRepository) {
    operator fun invoke(): Flow<List<Post>> = repository.observePosts()
}
```

### Data Layer (Implements Domain Interfaces)

```kotlin
// core/database/src/main/kotlin/com/app/database/PostEntity.kt
@Entity(tableName = "posts")
data class PostEntity(@PrimaryKey val id: String, val title: String, val body: String, val authorName: String)

fun PostEntity.toDomain() = Post(id, title, body, authorName)
fun Post.toEntity() = PostEntity(id, title, body, authorName)

// core/database/src/main/kotlin/com/app/database/PostDao.kt
@Dao
interface PostDao {
    @Query("SELECT * FROM posts ORDER BY id DESC")
    fun observeAll(): Flow<List<PostEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(posts: List<PostEntity>)
}

// feature/feed/data/src/main/kotlin/com/app/feed/data/PostRepositoryImpl.kt
class PostRepositoryImpl @Inject constructor(
    private val api: PostApi,
    private val dao: PostDao
) : PostRepository {
    override fun observePosts(): Flow<List<Post>> = dao.observeAll().map { list -> list.map { it.toDomain() } }
    override suspend fun refreshPosts(): Result<Unit> = runCatching {
        val dtos = api.getPosts()
        dao.insertAll(dtos.map { it.toEntity() })
    }
    override suspend fun createPost(title: String, body: String): Result<Post> = runCatching {
        val dto = api.createPost(CreatePostRequest(title, body))
        val entity = dto.toEntity()
        dao.insertAll(listOf(entity))
        entity.toDomain()
    }
}
```

### Presentation Layer (Compose + ViewModel)

```kotlin
@HiltViewModel
class FeedViewModel @Inject constructor(
    private val getFeedUseCase: GetFeedUseCase,
    private val refreshPostsUseCase: RefreshPostsUseCase
) : ViewModel() {
    val posts: StateFlow<List<Post>> = getFeedUseCase()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    fun refresh() { viewModelScope.launch { refreshPostsUseCase() } }
}
```

## When NOT to Use Clean Architecture

Clean Architecture adds significant boilerplate: interfaces, implementations, mappers, and modularization overhead. Avoid it for:
- Apps with < 5 screens and < 3 data sources
- Prototypes and MVPs where speed-to-feedback trumps maintainability
- Solo-developer projects where the abstraction tax exceeds the isolation benefit
- Apps where the data layer is trivial (single API, no local storage)

Start with MVVM. Extract Clean Architecture layers only when you have multiple data sources, multiple developers, and a measured need for layer isolation.
