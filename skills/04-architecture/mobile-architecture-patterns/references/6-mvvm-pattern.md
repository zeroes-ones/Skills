## 6. MVVM Pattern

**Model-View-ViewModel** is the entry-level architecture for structured mobile apps. Its core insight: the View should never contain an `if` statement about business logic.

### Structure

```
┌──────────────────────────────────────────────┐
│                    VIEW                      │
│  (SwiftUI View / UIViewController / Activity) │
│                                              │
│  - Observes ViewModel state                  │
│  - Forwards user actions                     │
│  - NO business logic. NO if-statements.      │
└─────────────┬────────────────────────────────┘
              │ observes (Combine / StateFlow / LiveData)
              ▼
┌──────────────────────────────────────────────┐
│                 VIEWMODEL                    │
│                                              │
│  - Transforms domain → UI state              │
│  - Handles user actions → call UseCases      │
│  - Exposes @Published / StateFlow            │
│  - Platform-agnostic where possible          │
└─────────────┬────────────────────────────────┘
              │ calls
              ▼
┌──────────────────────────────────────────────┐
│                  MODEL                       │
│  (Domain Models + UseCases + Repository)     │
│                                              │
│  - Business logic                            │
│  - Data transformation                       │
│  - No platform imports                       │
└──────────────────────────────────────────────┘
```

### iOS (SwiftUI + Combine)

```swift
// View — dumb renderer
struct ProfileView: View {
    @StateObject private var viewModel: ProfileViewModel

    var body: some View {
        Group {
            switch viewModel.state {
            case .loading:
                ProgressView()
            case .loaded(let profile):
                ProfileContent(profile: profile)
            case .error(let message):
                ErrorView(message: message, onRetry: { viewModel.send(.retry) })
            }
        }
        .task { viewModel.send(.load) }
    }
}

// ViewModel — state machine
@MainActor
final class ProfileViewModel: ObservableObject {
    @Published private(set) var state: ViewState<ProfileDisplayModel> = .loading
    private let getProfileUseCase: GetProfileUseCase

    func send(_ action: ProfileAction) {
        switch action {
        case .load:
            Task { await loadProfile() }
        case .retry:
            Task { await loadProfile() }
        }
    }

    private func loadProfile() async {
        state = .loading
        do {
            let profile = try await getProfileUseCase.execute()
            state = .loaded(ProfileDisplayModel(from: profile))
        } catch {
            state = .error(error.localizedDescription)
        }
    }
}
```

### Android (Jetpack Compose + StateFlow)

For full implementation details with Kotlin code, see `references/mvvm-mobile-patterns.md`.

---
