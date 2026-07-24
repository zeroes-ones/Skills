# VIPER Architecture — iOS Reference

> Full VIPER implementation with module templates, wireframe assembly, and protocol-driven contracts for maximum testability.

---

## VIPER Component Responsibilities

```
┌─────────────────────────────────────────────────────────────────┐
│ VIEW                   PRESENTER              INTERACTOR         │
│ (UIViewController/     (Formatting,           (Business logic,   │
│  SwiftUI View)         navigation)            data ops)          │
│                                                                │
│ - Displays formatted   - Receives events       - Fetches data     │
│   data from Presenter    from View              from Entity/DTOs  │
│ - Forwards user        - Formats data for      - Returns results  │
│   events to Presenter    View display            to Presenter     │
│ - NO logic             - Asks Router to        - Contains ALL     │
│                          navigate               business rules   │
│                                    │                            │
│                         ENTITY     │           ROUTER            │
│                         (Model     │           (Navigation,      │
│                          objects)  │            assembly)        │
│                                    │                            │
│                         - Plain    │           - Creates module  │
│                           structs/ │           - Pushes/presents │
│                           classes  │             new modules     │
│                         - No       │           - Owns UINavCtrl  │
│                           business │                            │
│                           logic    │                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Module Contracts

Define one protocol file per component so each piece is independently testable.

```swift
// MARK: - View Contract

protocol ProfileViewProtocol: AnyObject {
    var presenter: ProfilePresenterProtocol? { get set }
    func displayProfile(_ profile: ProfileDisplayModel)
    func displayError(_ message: String)
    func showLoading()
    func hideLoading()
}

// MARK: - Interactor Contract

protocol ProfileInteractorProtocol: AnyObject {
    var presenter: ProfileInteractorOutputProtocol? { get set }
    func fetchProfile(userId: String)
    func updateProfile(_ profile: Profile)
}

protocol ProfileInteractorOutputProtocol: AnyObject {
    func didFetchProfile(_ profile: Profile)
    func didFailToFetchProfile(_ error: Error)
    func didUpdateProfile(_ profile: Profile)
}

// MARK: - Presenter Contract

protocol ProfilePresenterProtocol: AnyObject {
    var view: ProfileViewProtocol? { get set }
    var interactor: ProfileInteractorProtocol? { get set }
    var router: ProfileRouterProtocol? { get set }
    func viewDidLoad()
    func didTapSave(name: String, email: String)
    func didTapBack()
}

// MARK: - Router Contract

protocol ProfileRouterProtocol: AnyObject {
    static func createModule(userId: String) -> UIViewController
    func navigateBack()
    func navigateToSettings(userId: String)
}

// MARK: - Contract References (weak to avoid retain cycles)

// Presenter has weak references to View and InteractorOutput
// View has strong reference to Presenter
// Interactor has strong reference to InteractorOutput
// Router is held strongly by Presenter
```

---

## Entity

```swift
struct Profile: Equatable {
    let id: String
    let name: String
    let email: String
    let bio: String
    let avatarURL: URL?
    let followerCount: Int
    let followingCount: Int

    var displayName: String {
        name.isEmpty ? "Unknown User" : name
    }

    var followerText: String {
        "\(followerCount) followers"
    }
}

struct ProfileDisplayModel: Equatable {
    let name: String
    let email: String
    let bio: String
    let avatarURL: URL?
    let statsText: String

    init(from profile: Profile) {
        self.name = profile.displayName
        self.email = profile.email
        self.bio = profile.bio
        self.avatarURL = profile.avatarURL
        self.statsText = "\(profile.followerText) · \(profile.followingCount) following"
    }
}
```

---

## Interactor Implementation

```swift
final class ProfileInteractor: ProfileInteractorProtocol {
    weak var presenter: ProfileInteractorOutputProtocol?
    private let profileService: ProfileServiceProtocol
    private let cacheManager: CacheManagerProtocol

    init(profileService: ProfileServiceProtocol, cacheManager: CacheManagerProtocol) {
        self.profileService = profileService
        self.cacheManager = cacheManager
    }

    func fetchProfile(userId: String) {
        // Check cache first
        if let cached = cacheManager.getCachedProfile(userId: userId) {
            presenter?.didFetchProfile(cached)
        }

        // Then fetch fresh data
        profileService.fetchProfile(userId: userId) { [weak self] result in
            switch result {
            case .success(let profile):
                self?.cacheManager.cacheProfile(profile)
                self?.presenter?.didFetchProfile(profile)
            case .failure(let error):
                self?.presenter?.didFailToFetchProfile(error)
            }
        }
    }

    func updateProfile(_ profile: Profile) {
        profileService.updateProfile(profile) { [weak self] result in
            switch result {
            case .success(let updated):
                self?.cacheManager.cacheProfile(updated)
                self?.presenter?.didUpdateProfile(updated)
            case .failure(let error):
                self?.presenter?.didFailToFetchProfile(error)
            }
        }
    }
}
```

---

## Presenter Implementation

```swift
final class ProfilePresenter: ProfilePresenterProtocol {
    weak var view: ProfileViewProtocol?
    var interactor: ProfileInteractorProtocol?
    var router: ProfileRouterProtocol?

    private let userId: String

    init(userId: String) {
        self.userId = userId
    }

    func viewDidLoad() {
        view?.showLoading()
        interactor?.fetchProfile(userId: userId)
    }

    func didTapSave(name: String, email: String) {
        guard !name.trimmingCharacters(in: .whitespaces).isEmpty else {
            view?.displayError("Name cannot be empty")
            return
        }
        // Presenter formats data before passing to Interactor
        let profile = Profile(id: userId, name: name, email: email,
                              bio: "", avatarURL: nil,
                              followerCount: 0, followingCount: 0)
        interactor?.updateProfile(profile)
    }

    func didTapBack() {
        router?.navigateBack()
    }
}

// MARK: - Interactor Output

extension ProfilePresenter: ProfileInteractorOutputProtocol {
    func didFetchProfile(_ profile: Profile) {
        view?.hideLoading()
        let displayModel = ProfileDisplayModel(from: profile)
        view?.displayProfile(displayModel)
    }

    func didFailToFetchProfile(_ error: Error) {
        view?.hideLoading()
        view?.displayError(error.localizedDescription)
    }

    func didUpdateProfile(_ profile: Profile) {
        let displayModel = ProfileDisplayModel(from: profile)
        view?.displayProfile(displayModel)
        router?.navigateBack()
    }
}
```

---

## View Implementation (UIKit)

```swift
final class ProfileViewController: UIViewController, ProfileViewProtocol {
    var presenter: ProfilePresenterProtocol?

    private let nameLabel = UILabel()
    private let emailLabel = UILabel()
    private let activityIndicator = UIActivityIndicatorView(style: .large)
    private let errorLabel = UILabel()

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        presenter?.viewDidLoad()
    }

    private func setupUI() {
        view.backgroundColor = .systemBackground
        // Layout omitted for brevity
    }

    func displayProfile(_ profile: ProfileDisplayModel) {
        nameLabel.text = profile.name
        emailLabel.text = profile.email
        errorLabel.isHidden = true
    }

    func displayError(_ message: String) {
        errorLabel.text = message
        errorLabel.isHidden = false
    }

    func showLoading() {
        activityIndicator.startAnimating()
    }

    func hideLoading() {
        activityIndicator.stopAnimating()
    }
}
```

---

## Router / Wireframe

```swift
final class ProfileRouter: ProfileRouterProtocol {
    weak var viewController: UIViewController?

    static func createModule(userId: String) -> UIViewController {
        let view = ProfileViewController()
        let interactor = ProfileInteractor(
            profileService: ServiceLocator.profileService,
            cacheManager: ServiceLocator.cacheManager
        )
        let presenter = ProfilePresenter(userId: userId)
        let router = ProfileRouter()

        view.presenter = presenter
        presenter.view = view
        presenter.interactor = interactor
        presenter.router = router
        interactor.presenter = presenter
        router.viewController = view

        return view
    }

    func navigateBack() {
        viewController?.navigationController?.popViewController(animated: true)
    }

    func navigateToSettings(userId: String) {
        let settingsVC = SettingsRouter.createModule(userId: userId)
        viewController?.navigationController?.pushViewController(settingsVC, animated: true)
    }
}
```

---

## Unit Testing VIPER

```swift
final class ProfilePresenterTests: XCTestCase {
    private var sut: ProfilePresenter!
    private var mockView: MockProfileView!
    private var mockInteractor: MockProfileInteractor!
    private var mockRouter: MockProfileRouter!

    override func setUp() {
        super.setUp()
        sut = ProfilePresenter(userId: "test-123")
        mockView = MockProfileView()
        mockInteractor = MockProfileInteractor()
        mockRouter = MockProfileRouter()
        sut.view = mockView
        sut.interactor = mockInteractor
        sut.router = mockRouter
    }

    func test_viewDidLoad_showsLoadingAndFetchesProfile() {
        sut.viewDidLoad()

        XCTAssertTrue(mockView.showLoadingCalled)
        XCTAssertTrue(mockInteractor.fetchProfileCalled)
        XCTAssertEqual(mockInteractor.lastFetchedUserId, "test-123")
    }

    func test_didFetchProfile_hidesLoadingAndDisplaysData() {
        let profile = Profile(id: "test-123", name: "Alice",
                              email: "alice@test.com", bio: "",
                              avatarURL: nil, followerCount: 42, followingCount: 10)

        sut.didFetchProfile(profile)

        XCTAssertTrue(mockView.hideLoadingCalled)
        XCTAssertTrue(mockView.displayProfileCalled)
        XCTAssertEqual(mockView.lastDisplayedProfile?.name, "Alice")
    }

    func test_didTapSave_withEmptyName_showsError() {
        sut.didTapSave(name: "   ", email: "alice@test.com")

        XCTAssertTrue(mockView.displayErrorCalled)
        XCTAssertEqual(mockView.lastErrorMessage, "Name cannot be empty")
        XCTAssertFalse(mockInteractor.updateProfileCalled)
    }
}
```

---

## When VIPER Is the Right Choice

| Situation | Verdict |
|---|---|
| Enterprise iOS app, 10+ developers, 50+ screens, 3+ years expected lifespan | **YES** |
| Startup MVP, 2 developers, <10 screens | **NO** — Use MVVM |
| App requiring 90%+ code coverage for compliance (healthcare, finance) | **YES** — VIPER's component isolation makes this achievable |
| Team unfamiliar with protocol-heavy architectures | **NO** — Productivity loss outweighs benefit |
| Mix of UIKit and SwiftUI in migration | **YES** — Presenter bridges both UI paradigms |

### VIPER Anti-Patterns

1. **Massive Presenter:** If your Presenter exceeds 200 lines, push logic to Interactor. The Presenter formats data and routes. Nothing more.
2. **Router does DI assembly manually for every module:** Use a DI container alongside. The Router calls the container, not `init` directly.
3. **View holds a strong reference to anything except Presenter:** View should own exactly one thing — the Presenter. All other references belong elsewhere.
4. **Interactor calls View directly:** Never. Interactor only talks to Presenter via the output protocol.
