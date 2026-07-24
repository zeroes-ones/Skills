# Mobile Navigation Patterns — Reference

> Coordinator pattern, deep linking, state restoration, and universal link handling for iOS and Android.

---

## The Coordinator Pattern

Coordinators own the navigation graph. Views never push/present other views directly. This enables deep linking, universal links, push notification routing, and testable navigation.

### iOS Coordinator (UIKit)

```swift
protocol Coordinator: AnyObject {
    var childCoordinators: [Coordinator] { get set }
    var navigationController: UINavigationController { get }
    func start()
}

protocol Coordinatable {
    associatedtype Route
    func navigate(to route: Route)
}

// MARK: - App Coordinator (Root)

final class AppCoordinator: Coordinator {
    var childCoordinators: [Coordinator] = []
    let navigationController: UINavigationController
    private let dependencyContainer: DependencyContainer

    init(navigationController: UINavigationController,
         container: DependencyContainer) {
        self.navigationController = navigationController
        self.dependencyContainer = container
    }

    func start() {
        if dependencyContainer.authService.isAuthenticated {
            showMainFlow()
        } else {
            showAuthFlow()
        }
    }

    func handleDeepLink(_ deepLink: DeepLink) {
        switch deepLink {
        case .product(let id):
            showMainFlow()
            showProductDetail(productId: id)
        case .profile(let userId):
            showMainFlow()
            showProfile(userId: userId)
        case .checkout:
            showMainFlow()
            showCheckout()
        }
    }

    private func showMainFlow() {
        let tabCoordinator = TabCoordinator(
            navigationController: navigationController,
            container: dependencyContainer
        )
        childCoordinators.append(tabCoordinator)
        tabCoordinator.start()
    }

    private func showAuthFlow() {
        let authCoordinator = AuthCoordinator(
            navigationController: navigationController,
            container: dependencyContainer,
            onAuthSuccess: { [weak self] in
                self?.childCoordinators.removeAll()
                self?.showMainFlow()
            }
        )
        childCoordinators.append(authCoordinator)
        authCoordinator.start()
    }

    private func showProductDetail(productId: String) {
        guard let tabCoordinator = childCoordinators
            .compactMap({ $0 as? TabCoordinator }).first else { return }
        tabCoordinator.showProductDetail(productId: productId)
    }

    private func showProfile(userId: String) {
        guard let tabCoordinator = childCoordinators
            .compactMap({ $0 as? TabCoordinator }).first else { return }
        tabCoordinator.showProfile(userId: userId)
    }

    private func showCheckout() {
        guard let tabCoordinator = childCoordinators
            .compactMap({ $0 as? TabCoordinator }).first else { return }
        tabCoordinator.showCheckout()
    }
}
```

### Deep Link Definition

```swift
enum DeepLink {
    case product(id: String)
    case profile(userId: String)
    case checkout

    init?(url: URL) {
        guard let components = URLComponents(url: url, resolvingAgainstBaseURL: true),
              let host = components.host else { return nil }

        switch host {
        case "product":
            guard let id = components.queryItems?
                .first(where: { $0.name == "id" })?.value else { return nil }
            self = .product(id: id)
        case "profile":
            guard let userId = components.queryItems?
                .first(where: { $0.name == "userId" })?.value
            else { return nil }
            self = .profile(userId: userId)
        case "checkout":
            self = .checkout
        default:
            return nil
        }
    }
}

// Info.plist: myapp://product?id=123 → DeepLink.product(id: "123")

// SceneDelegate / AppDelegate
func scene(_ scene: UIScene, openURLContexts URLContexts: Set<UIOpenURLContext>) {
    guard let url = URLContexts.first?.url,
          let deepLink = DeepLink(url: url) else { return }
    appCoordinator?.handleDeepLink(deepLink)
}
```

### SwiftUI Navigation (iOS 16+)

```swift
@Observable
final class AppRouter {
    var navigationPath = NavigationPath()

    enum Route: Hashable {
        case product(id: String)
        case profile(userId: String)
        case checkout
    }

    func navigate(to route: Route) {
        navigationPath.append(route)
    }

    func popToRoot() {
        navigationPath.removeLast(navigationPath.count)
    }

    func handleDeepLink(_ url: URL) {
        guard let deepLink = DeepLink(url: url) else { return }
        navigationPath.removeLast(navigationPath.count)
        switch deepLink {
        case .product(let id):
            navigationPath.append(Route.product(id: id))
        case .profile(let userId):
            navigationPath.append(Route.profile(userId: userId))
        case .checkout:
            navigationPath.append(Route.checkout)
        }
    }
}

struct AppRootView: View {
    @State private var router = AppRouter()

    var body: some View {
        NavigationStack(path: $router.navigationPath) {
            HomeView(router: router)
                .navigationDestination(for: AppRouter.Route.self) { route in
                    switch route {
                    case .product(let id):
                        ProductDetailView(productId: id)
                    case .profile(let userId):
                        ProfileView(userId: userId)
                    case .checkout:
                        CheckoutView()
                    }
                }
        }
        .onOpenURL { router.handleDeepLink($0) }
    }
}
```

---

## Android Navigation (Jetpack Navigation + Compose)

```kotlin
// Navigation routes as sealed class
sealed class Screen(val route: String) {
    data object Home : Screen("home")
    data object ProductDetail : Screen("product/{productId}") {
        fun createRoute(productId: String) = "product/$productId"
    }
    data object Profile : Screen("profile/{userId}") {
        fun createRoute(userId: String) = "profile/$userId"
    }
    data object Checkout : Screen("checkout")
}

// NavHost setup
@Composable
fun AppNavGraph(
    navController: NavHostController = rememberNavController()
) {
    NavHost(
        navController = navController,
        startDestination = Screen.Home.route
    ) {
        composable(Screen.Home.route) {
            HomeScreen(onProductClick = { id ->
                navController.navigate(Screen.ProductDetail.createRoute(id))
            })
        }
        composable(
            route = Screen.ProductDetail.route,
            arguments = listOf(navArgument("productId") { type = NavType.StringType })
        ) { backStackEntry ->
            val productId = backStackEntry.arguments?.getString("productId") ?: return@composable
            ProductDetailScreen(productId = productId)
        }
        composable(
            route = Screen.Profile.route,
            arguments = listOf(navArgument("userId") { type = NavType.StringType })
        ) { backStackEntry ->
            val userId = backStackEntry.arguments?.getString("userId") ?: return@composable
            ProfileScreen(userId = userId)
        }
        composable(Screen.Checkout.route) {
            CheckoutScreen()
        }
    }
}

// Deep link handling in AndroidManifest.xml
/*
<intent-filter>
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />
    <data android:scheme="myapp" android:host="product" />
</intent-filter>
*/
```

---

## State Restoration

### iOS

```swift
// Scene-based restoration (iOS 13+)
final class ProfileViewController: UIViewController {
    private let userId: String

    override func viewDidLoad() {
        super.viewDidLoad()
        // Restore from userActivity if present
        if let activity = view.window?.windowScene?.userActivity {
            restore(from: activity)
        }
    }

    override func updateUserActivityState(_ activity: NSUserActivity) {
        super.updateUserActivityState(activity)
        activity.addUserInfoEntries(from: ["userId": userId])
    }

    private func restore(from activity: NSUserActivity) {
        guard let userId = activity.userInfo?["userId"] as? String
        else { return }
        // Restore state with userId
    }
}
```

### Android

```kotlin
class ProfileViewModel(
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val userId: String = savedStateHandle["userId"] ?: ""

    fun updateUserId(newId: String) {
        savedStateHandle["userId"] = newId
    }
}

// Compose: rememberSaveable for UI state
@Composable
fun SearchScreen() {
    var query by rememberSaveable { mutableStateOf("") }
    var scrollState = rememberLazyListState()

    // query survives process death, scrollState restored automatically
}
```

---

## Navigation Anti-Patterns

1. **Views pushing views directly:** `navigationController?.pushViewController(vc, animated: true)` inside a ViewController. This makes deep linking impossible.
2. **Navigation logic in ViewModels:** ViewModels should not know about navigation. They emit events. Router/Coordinator responds.
3. **One giant Coordinator:** Split into child coordinators: `AuthCoordinator`, `TabCoordinator`, `OnboardingCoordinator`. Each owns a flow.
4. **Missing back-stack cleanup on logout:** After logout, clear the entire navigation stack. Reset to auth flow root.
5. **No testing for process death:** If you haven't tested that your app restores correctly after `adb shell am kill <package>` (Android) or force-quit (iOS), you haven't tested your app.
