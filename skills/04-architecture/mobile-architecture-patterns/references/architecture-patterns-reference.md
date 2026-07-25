## 5. Architecture Overview & Comparison Matrix

Mobile architecture solves three problems simultaneously: managing state across a disconnected, resource-constrained device; structuring code so 5+ developers can work without conflicts; and surviving the OS killing your process at any moment. No server-side pattern addresses all three.

#

## Comparison Matrix

| Pattern | State Management | Testability | Boilerplate | Learning Curve | Best For |
|---|---|---|---|---|---|
| **MVVM** | ViewModel + bindings | High (VM unit tests) | Low-Medium | Low | Single-platform, <8 devs |
| **Clean Architecture** | UseCases → Repositories → DataSources | Maximum | High | High | Multi-platform, 8+ devs |
| **VIPER** | Interactor → Presenter → View | Maximum (every component) | Very High | High | iOS-only, max testability |
| **MVI** | Unidirectional: Intent → Model → View | High (reducer tests) | Medium | Medium | Android/Compose, predictable state |
| **TCA** | Store + Reducer + Environment | High (test store) | Medium | High | SwiftUI, state-driven apps |

#

## Platform Mapping

| Scenario | iOS Recommendation | Android Recommendation |
|---|---|---|
| Greenfield, small team | MVVM + SwiftUI + Combine | MVVM + Jetpack Compose + StateFlow |
| Greenfield, large team | Clean Architecture + SwiftUI | Clean Architecture + Compose |
| Maximum test coverage | VIPER or TCA | Clean Architecture + MVI |
| Kotlin Multiplatform | Clean Arch shared domain | Clean Arch shared domain |
| Legacy UIKit/XML migration | MVVM + Coordinators | MVVM + LiveData → StateFlow |

---

## 6. MVVM Pattern
<!-- COMPRESSED: Full 92 lines extracted to references/6-mvvm-pattern.md -->

**Model-View-ViewModel** is the entry-level architecture for structured mobile apps. Its core insight: the View should never contain an `if` statement about business logic.

#

## Structure

```
...
> 📎 **Full content (92 lines):** [references/6-mvvm-pattern.md](references/6-mvvm-pattern.md)

## 7. Clean Architecture on Mobile
<!-- Full 30 lines extracted to references/7-clean-architecture-on-mobile.md -->

Clean Architecture on mobile adds domain and data layers around the presentation layer. The key constraint: **dependencies point inward.** Domain knows nothing about data sources. Presentation knows nothing about APIs.
#

## Layer Diagram
┌─────────────────────────────────────────────────────┐
│  PRESENTATION (iOS: SwiftUI/UIKit, Android: Compose) │
...
> 📎 **[references/7-clean-architecture-on-mobile.md](references/7-clean-architecture-on-mobile.md)** — 30 lines of detailed guidance

## 8. VIPER Architecture (iOS)

VIPER splits ViewController responsibilities into five distinct roles. It is the most testable iOS architecture at the cost of the most boilerplate.

#

## Components

| Component | Responsibility | Test With |
|---|---|---|
| **View** | Display data, forward user events to Presenter | View tests (snapshot) |
| **Interactor** | Business logic, data operations | Unit tests (mock presenter) |
| **Presenter** | Format data for display, handle navigation requests | Unit tests (mock view, router) |
| **Entity** | Data models (same as domain models) | Unit tests |
| **Router** | Navigation, module assembly | Integration tests |

Full implementation in `references/viper-architecture-ios.md`.

---

## 9. MVI Pattern (Android)

Model-View-Intent enforces unidirectional data flow through a state reducer. It is the natural pattern for Jetpack Compose and eliminates state inconsistency bugs.

#

## Core Loop

```
User Action → Intent → ViewModel → Reducer → New State → View renders
```

**Immutable state** is the foundation. State is a single data class. Every user action produces a new state instance. Enables time-travel debugging and deterministic testing.

Full implementation in `references/mvi-android-patterns.md`.

---

## 10. TCA — The Composable Architecture

TCA (pointfree.co) brings Redux-like architecture to SwiftUI with first-class support for composition, side effects, and testing. It is ideal for SwiftUI apps with complex, interconnected state.

#

## Core Types

- **State:** A struct describing all data the feature needs
- **Action:** An enum of everything that can happen (user actions, side effect results)
- **Reducer:** A pure function `(inout State, Action) -> Effect<Action>`
- **Store:** Runtime that holds state and runs reducers
- **Effect:** Describes side effects (network, DB) that produce actions

Full implementation in `references/tca-composable-architecture.md`.

---

## 11. Navigation Patterns

Mobile navigation is architecture, not UI. Poor navigation design makes deep linking, state restoration, and multi-module apps impossible.

#

## Coordinator Pattern (iOS + Android)

```swift
protocol Coordinator: AnyObject {
    var childCoordinators: [Coordinator] { get set }
    var navigationController: UINavigationController { get }
    func start()
}

final class AppCoordinator: Coordinator {
    func showProfile(userId: String) {
        let coordinator = ProfileCoordinator(
            navigationController: navigationController,
            userId: userId
        )
        childCoordinators.append(coordinator)
        coordinator.start()
    }
}
```

Full implementation in `references/mobile-navigation-patterns.md`.

---

## 12. Offline-First Architecture

#

## Three-Tier Data Strategy

```
┌─────────────────────────────────────────────┐
│  TIER 1: UI reads from local DB only       │
│  (Room / Core Data / GRDB)                  │
│  Never reads from network directly          │
├─────────────────────────────────────────────┤
│  TIER 2: Sync Engine                        │
│  Fetches from API → writes to local DB      │
│  Queues local writes → pushes to API        │
├─────────────────────────────────────────────┤
│  TIER 3: Conflict Resolution                │
│  Last-write-wins (LWW) or CRDT for          │
│  collaborative data                         │
└─────────────────────────────────────────────┘
```

Full implementation in `references/offline-first-mobile.md`.

---

## 13. State Management at Scale

As apps grow, state management becomes the primary architectural concern. The patterns here scale from 1 to 200+ screens.

| Scale | Pattern | State Location | Sync Mechanism |
|---|---|---|---|
| 1-5 screens | @Published / StateFlow per VM | Per-ViewModel | Manual parent-child |
| 5-20 screens | Shared state via injected Store/Repository | Singleton Store | Combine/Flow |
| 20-100 screens | Feature-scoped state with DI scopes | DI-scoped containers | Event bus or shared Store |
| 100+ screens | Multi-module state with TCA/Rx Store | Per-module Store + shared core | Actions cross module boundaries |

Full implementation in `references/mobile-state-management.md`.

---

## 14. Dependency Injection & Modularization

#

## DI Framework Selection

| Platform | Framework | Notes |
|---|---|---|
| iOS | Swinject, Factory, Needle, or manual constructor injection | For <10 deps, manual is cleaner |
| Android | Hilt (preferred), Koin, Dagger | Hilt is Google-recommended |
| KMP | Koin (multiplatform), manual injection | Koin works on both platforms |

#

## Modularization Principles

- **Interface modules:** Feature modules expose only public API interfaces
- **No transitive dependencies from features:** `:feature-checkout` cannot depend on `:feature-profile`
- **Shared nothing by default:** Only `:core:models`, `:core:di`, `:core:navigation` are shared
- **Build graph is a DAG:** Cyclic dependencies between modules are banned via lint rule

---

## 15. Testing Strategy Per Architecture

| Architecture | Unit Tests | Integration Tests | UI Tests | Test Pyramid |
|---|---|---|---|---|
| **MVVM** | ViewModel (70%) | Repository + API (20%) | Critical flows (10%) | Standard pyramid |
| **Clean Architecture** | UseCases (60%) | Repository impls (25%) | Screen flows (15%) | Broad base, narrow top |
| **VIPER** | Interactor + Presenter (80%) | Router + assembly (15%) | Smoke tests (5%) | Very broad base |
| **MVI** | Reducer (75%) | Side effects (15%) | Compose UI (10%) | Broad base |
| **TCA** | Reducer + effects (85%) | Integration store (10%) | Snapshot (5%) | Broadest base |

**Testing non-negotiables:**
- Every ViewModel/Reducer has >80% unit test coverage
- Every UseCase is tested with mock repositories
- Every API error path is tested (network timeout, 4xx, 5xx, malformed JSON)
- State restoration is tested via process death simulation

---
