# Mobile State Management — Reference

> Patterns for managing UI state from 1 to 200+ screens. Single source of truth, immutable state, and predictable state transitions.

---

## State Categories

| Category | Examples | Storage | Lifetime |
|---|---|---|---|
| **Transient UI state** | Scroll position, text field input, animation progress | `@State` / `remember` | Screen lifecycle |
| **Screen state** | Current view data, loading/error flags | ViewModel / Store | Screen + process death |
| **Session state** | Auth token, user preferences, cart | Repository / DataStore | App session |
| **Persistent state** | Saved posts, user settings, cached data | Database / UserDefaults | Indefinite |
| **Global app state** | Theme, locale, connectivity status | Singleton + Flow/Combine | App lifetime |

---

## Scale 1: Single Screen (SwiftUI + @StateObject)

```swift
// Simple: one ViewModel per screen, no cross-screen state sharing
@MainActor
final class FeedbackViewModel: ObservableObject {
    @Published var rating: Int = 0
    @Published var comment: String = ""
    @Published var isSubmitting: Bool = false
    @Published var submitError: String?

    private let submitFeedback: SubmitFeedbackUseCase

    func submit() async {
        guard rating > 0 else {
            submitError = "Please select a rating"
            return
        }
        isSubmitting = true
        do {
            try await submitFeedback.execute(rating: rating, comment: comment)
            // Reset after success
            rating = 0
            comment = ""
        } catch {
            submitError = error.localizedDescription
        }
        isSubmitting = false
    }
}
```

---

## Scale 2: Shared State Across Screens (iOS — EnvironmentObject)

```swift
// Shared auth state — accessed by any child view
@MainActor
final class SessionStore: ObservableObject {
    @Published var currentUser: User?
    @Published var isAuthenticated: Bool = false
    @Published var authToken: String?

    func signIn(email: String, password: String) async throws {
        let response = try await authService.signIn(email: email, password: password)
        currentUser = response.user
        authToken = response.token
        isAuthenticated = true
    }

    func signOut() {
        currentUser = nil
        authToken = nil
        isAuthenticated = false
    }
}

// In App entry point
@main
struct MyApp: App {
    @StateObject private var session = SessionStore()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(session)
        }
    }
}

// Any child view can access
struct ProfileHeader: View {
    @EnvironmentObject var session: SessionStore

    var body: some View {
        if let user = session.currentUser {
            Text(user.displayName)
        }
    }
}
```

---

## Scale 3: Feature-Scoped State with DI Scopes (Android — Hilt)

```kotlin
// Scoped to a navigation graph / feature
@Module
@InstallIn(ViewModelComponent::class)
object CheckoutModule {
    @Provides
    @ViewModelScoped
    fun provideCartRepository(
        cartDao: CartDao,
        cartApi: CartApi
    ): CartRepository = CartRepositoryImpl(cartDao, cartApi)
}

// ViewModels within checkout feature share the same CartRepository
// When user leaves checkout, ViewModelScope is cleared, CartRepository is freed

@HiltViewModel
class CartViewModel @Inject constructor(
    private val cartRepository: CartRepository
) : ViewModel() {
    private val _cart = MutableStateFlow(CartState())
    val cart: StateFlow<CartState> = _cart.asStateFlow()

    fun addItem(productId: String) {
        viewModelScope.launch {
            cartRepository.addItem(productId)
            _cart.update { it.copy(items = cartRepository.getItems()) }
        }
    }
}

@HiltViewModel
class CheckoutViewModel @Inject constructor(
    private val cartRepository: CartRepository, // SAME instance as CartViewModel
    private val paymentService: PaymentService
) : ViewModel() {
    // Reads cart from the same CartRepository
    val cartItems: StateFlow<List<CartItem>> = cartRepository.observeItems()

    fun checkout() {
        viewModelScope.launch {
            paymentService.processPayment(cartRepository.getTotal())
            cartRepository.clear()
        }
    }
}
```

---

## Scale 4: Multi-Module with Event Bus (Android)

```kotlin
// Shared event bus for cross-module communication without direct dependencies
// Events flow through :core:events module

// core/events/src/main/kotlin/AppEvents.kt
sealed class AppEvent {
    data class UserLoggedIn(val userId: String) : AppEvent()
    data class UserLoggedOut : AppEvent()
    data class CartUpdated(val itemCount: Int) : AppEvent()
    data class LanguageChanged(val locale: Locale) : AppEvent()
}

@Singleton
class AppEventBus @Inject constructor() {
    private val _events = MutableSharedFlow<AppEvent>(
        replay = 0,
        extraBufferCapacity = 64,
        onBufferOverflow = BufferOverflow.DROP_OLDEST
    )
    val events: SharedFlow<AppEvent> = _events.asSharedFlow()

    fun emit(event: AppEvent) {
        _events.tryEmit(event)
    }
}

// feature/cart listens for login events
@HiltViewModel
class CartViewModel @Inject constructor(
    private val eventBus: AppEventBus
) : ViewModel() {
    init {
        viewModelScope.launch {
            eventBus.events.collect { event ->
                when (event) {
                    is AppEvent.UserLoggedIn -> mergeGuestCart(event.userId)
                    is AppEvent.UserLoggedOut -> clearCart()
                    else -> {}
                }
            }
        }
    }
}
```

---

## Scale 5: TCA Store Composition (iOS — 100+ screens)

```swift
// Parent feature composes child features
@Reducer
struct AppFeature {
    @ObservableState
    struct State: Equatable {
        var auth = AuthFeature.State()
        var home = HomeFeature.State()
        var settings = SettingsFeature.State()
        var selectedTab: Tab = .home

        // Shared state — any child feature can read via parent
        var currentUser: User?
    }

    enum Action {
        case auth(AuthFeature.Action)
        case home(HomeFeature.Action)
        case settings(SettingsFeature.Action)
        case tabSelected(State.Tab)
        case userUpdated(User)
    }

    var body: some Reducer<State, Action> {
        Scope(state: \.auth, action: \.auth) { AuthFeature() }
        Scope(state: \.home, action: \.home) { HomeFeature() }
        Scope(state: \.settings, action: \.settings) { SettingsFeature() }

        Reduce { state, action in
            switch action {
            case .auth(.loginResponse(.success(let user))):
                state.currentUser = user
                state.selectedTab = .home
                return .none

            case .userUpdated(let user):
                state.currentUser = user
                return .none

            default:
                return .none
            }
        }
    }
}
```

---

## Immutable State Concurrency (Kotlin)

```kotlin
// Thread-safe state updates with atomic operations
@Stable
data class FeedState(
    val posts: List<Post> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val pagination: PaginationState = PaginationState()
) {
    val isEmpty: Boolean get() = posts.isEmpty() && !isLoading
    val showLoadMore: Boolean get() = pagination.hasNextPage && !isLoading
}

data class PaginationState(
    val currentPage: Int = 0,
    val hasNextPage: Boolean = true,
    val isLoadingMore: Boolean = false
)

class FeedViewModel @Inject constructor(
    private val feedRepository: FeedRepository
) : ViewModel() {

    private val _state = MutableStateFlow(FeedState())
    val state: StateFlow<FeedState> = _state.asStateFlow()

    fun loadNextPage() {
        val current = _state.value
        if (current.pagination.isLoadingMore || !current.pagination.hasNextPage) return

        _state.update {
            it.copy(pagination = it.pagination.copy(isLoadingMore = true))
        }

        viewModelScope.launch {
            feedRepository.getFeed(current.pagination.currentPage + 1)
                .onSuccess { page ->
                    _state.update {
                        it.copy(
                            posts = it.posts + page.items,
                            pagination = PaginationState(
                                currentPage = page.number,
                                hasNextPage = page.hasNext,
                                isLoadingMore = false
                            ),
                            isLoading = false
                        )
                    }
                }
                .onFailure { error ->
                    _state.update {
                        it.copy(
                            error = error.message,
                            pagination = it.pagination.copy(isLoadingMore = false)
                        )
                    }
                }
        }
    }
}
```

---

## Performance: Avoiding Recompositions

### iOS

```swift
// BAD: Entire view recomputes when any @Published property changes
@Published var name = ""
@Published var email = ""
@Published var posts: [Post] = []

// GOOD: Use @ObservationIgnored for non-UI state, or split into sub-ViewModels
@Observable
final class ProfileViewModel {
    var name = ""
    var email = ""
    var posts: [Post] = []
    @ObservationIgnored var analyticsId: String = ""
    @ObservationIgnored var lastFetchDate: Date?
}
```

### Android

```kotlin
// BAD: List recomposes on every state change
@Composable
fun FeedScreen(viewModel: FeedViewModel) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    LazyColumn { items(state.posts) { PostCard(it) } }
    // PostCard re-renders when isLoading changes
}

// GOOD: Derive stable keys, use @Immutable models
@Immutable
data class PostModel(val id: String, val title: String, val author: String)

@Composable
fun FeedScreen(viewModel: FeedViewModel) {
    val posts by viewModel.posts.collectAsStateWithLifecycle()
    val isLoading by viewModel.isLoading.collectAsStateWithLifecycle()

    LazyColumn {
        // Only post list recomposes; loading spinner is separate
        items(posts, key = { it.id }) { PostCard(it) }
    }

    if (isLoading) {
        LinearProgressIndicator(modifier = Modifier.fillMaxWidth())
    }
}
```

---

## State Restoration Checklist

| Platform | Mechanism | What to Save |
|---|---|---|
| iOS (UIKit) | `NSUserActivity` + `updateUserActivityState` | Screen identifier + minimal data to reconstruct |
| iOS (SwiftUI) | `@SceneStorage` | Tab selection, scroll position, draft text |
| Android (View) | `onSaveInstanceState` / `SavedStateHandle` | Screen params, form input, scroll position |
| Android (Compose) | `rememberSaveable` | Any `Parcelable`/`Serializable` state |

### Test process death:

```bash
# Android
adb shell am kill com.example.app
# Then reopen app — state should restore

# iOS
# Edit scheme → Run → Options → uncheck "Launch due to background fetch"
# Force quit app, reopen — state should restore
```
