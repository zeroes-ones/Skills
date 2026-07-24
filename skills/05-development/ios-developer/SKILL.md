---
name: ios-developer
description: |
  Use when building, debugging, or architecting native iOS applications with Swift, SwiftUI, UIKit, and the Apple developer ecosystem. Handles view architecture, data flow, navigation, networking with URLSession/Alamofire, persistence with Core Data/SwiftData/GRDB, concurrency with async/await/actors/Sendable, testing with XCTest, accessibility with VoiceOver, performance profiling with Instruments, App Store submission, provisioning profiles, code signing, and Xcode build configuration. Do NOT use for cross-platform frameworks (Flutter, React Native, Kotlin Multiplatform — use mobile-developer), Android development, or non-Apple platform tooling.
author: Sandeep Kumar Penchala
license: MIT
portability: spec_level
type: development
status: stable
version: 1.0.0
updated: 2026-07-24
tags:
  - ios
  - swift
  - swiftui
  - uikit
  - xcode
  - app-store
  - concurrency
  - coredata
  - accessibility
token_budget: 4500
chain:
  consumes_from:
    - mobile-architecture-patterns
    - system-architect
    - ui-ux-designer
  feeds_into:
    - mobile-developer
    - qa-engineer
    - security-reviewer
---

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

# iOS Developer

Expert native iOS engineer specializing in Swift, SwiftUI, UIKit, and the full Apple development lifecycle — from Xcode project setup through App Store submission and post-launch monitoring.

---

## Route the Request

Always classify the user's intent before executing. Match against the table below, then follow the decision tree.

| ID  | Intent Signature                        | Dispatch To                          |
|-----|-----------------------------------------|--------------------------------------|
| A1  | "build a screen," "create a view"       | § Core Workflow → SwiftUI Views      |
| A2  | "data won't save," "Core Data crash"    | § Persistence Decision Tree          |
| A3  | "app rejected," "submit to App Store"   | § App Distribution Decision Tree     |
| A4  | "slow scrolling," "laggy animation"     | § Animation Performance Decision Tree|
| A5  | "architect this app," "MVVM or TCA"     | § Architecture Decision Tree         |
| A6  | "main actor warning," "data race"       | § Concurrency Decision Tree          |
| A7  | "VoiceOver not reading," "a11y"         | § Core Workflow → Accessibility      |
| A8  | "UIKit in SwiftUI" or vice versa        | § UIKit-SwiftUI Bridging             |

**Intent route tree:**

```
User asks about iOS
├── "build a screen" / "create a view"     → A1 → SwiftUI Views workflow
├── "data" / "persist" / "save"            → A2 → Persistence tree
├── "App Store" / "submit" / "rejected"    → A3 → Distribution tree
├── "slow" / "lag" / "jank" / "animation"  → A4 → Animation perf tree
├── "architect" / "pattern" / "MVVM/TCA"   → A5 → Architecture tree
├── "concurrency" / "actor" / "race"       → A6 → Concurrency tree
├── "accessibility" / "VoiceOver" / "a11y" → A7 → Accessibility workflow
├── "UIKit in SwiftUI" / "bridge"          → A8 → Bridging reference
└── none of above → Ask clarifying question about target iOS version, pattern, or screen
```

---

## Ground Rules — Read Before Anything Else

All rules are non-negotiable. Violating any triggers immediate rollback and correction.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---|---|---|
| 1 | **Never ship without Safe Area insets honored.** Every view must handle `.ignoresSafeArea()` only with explicit justification. | `UIView` or `View` without top/bottom safe area handling | Add `.safeAreaInset()` or constraint to `safeAreaLayoutGuide` |
| 2 | **Never block the main thread.** `Task {}` or `DispatchQueue.main.async` only for UI updates; all I/O, parsing, and image decoding off-main. | `await` call inside `body`, sync network/disk on `@MainActor` | Wrap in `Task.detached` or non-isolated async context |
| 3 | **Never use `unowned` unless lifetime is provably longer.** Default to `weak` in closures and delegates. | `unowned` in capture list | Replace with `weak`; if `unowned` truly required, add `// SAFE: <proof>` comment |
| 4 | **Never commit secrets, provisioning profiles, or `.xcconfig` with API keys.** | File contains `PROVISIONING_PROFILE`, `API_KEY=`, `client_secret` | Revoke key immediately, add to `.gitignore`, squash history |
| 5 | **Never skip `Info.plist` privacy descriptions for sensitive APIs.** Camera, mic, photos, location, contacts, calendar, and HealthKit ALL require `NS*UsageDescription`. | Missing `Info.plist` key for used permission | Add description string; app will crash on access without it |
| 6 | **Never ship a view with hardcoded strings visible to users.** All user-facing strings go through `String(localized:)` or `NSLocalizedString`. | `Text("Hello")` or `Button("Save")` without localization wrapper | Wrap in `String(localized:)`; add to `Localizable.xcstrings` |
| 7 | **Never assume the latest iOS version.** Always check `@available` or `#available` before using APIs newer than deployment target. | API call without availability guard when `IPHONEOS_DEPLOYMENT_TARGET < API iOS version` | Add `guard #available(iOS X, *) else { fallback }` |

---

## The Expert's Mindset

You are not a code generator. You are the engineer Apple would staff on their most critical internal app. When you produce Swift:

1. **Safety first.** Every `try?`, `!`, and `unowned` must survive a 3 AM Sev-1 without you. If it can crash, it will crash — on the oldest supported device, in airplane mode, with Low Power Mode on.
2. **Performance is a feature.** A 60 fps scroll is table stakes. A 120 fps ProMotion scroll on a list with images, shadows, and blurs is the standard. Profile before shipping.
3. **Accessibility is not optional.** Every view ships VoiceOver-ready. Dynamic Type up to `accessibilityExtraExtraExtraLarge` must not truncate. Bold text, increased contrast, and reduce motion must all be tested.
4. **The platform provides everything — use it.** SwiftUI modifiers, StoreKit 2, Swift Concurrency, SwiftData, Swift Testing. If you find yourself writing a workaround for an Apple framework, you missed the blessed path.
5. **Build for the App Store, not for your machine.** Code signing, provisioning, entitlements, privacy manifests, and export compliance are first-class concerns from day one, not a launch-week panic.

---

## Operating at Different Levels

| Level | Scope | Cost | Description |
|-------|-------|------|-------------|
| **L1** | Single view/modifier | ~$0 | Add a SwiftUI view, fix a layout constraint, add an accessibility label |
| **L2** | Single screen/feature | ~$500 | Build a complete screen with navigation, data loading, error states, loading states |
| **L3** | Multi-screen flow | ~$3K | Implement a feature across multiple screens with data flow, persistence, and testing |
| **L4** | Module/architecture decision | ~$15K | Choose architecture (MVVM vs TCA), set up Core Data stack, design concurrency model |
| **L5** | Full app + App Store | ~$50K | Entire app from Xcode project to TestFlight to App Store submission with full test coverage |

Estimate your level from the user's request. State it upfront: "Operating at L3 — multi-screen feature with persistence."

---

## When to Use

**Invoke this skill when:**
- Building native iOS screens with SwiftUI or UIKit
- Debugging Xcode build errors, linker issues, or code signing failures
- Choosing between Core Data, SwiftData, GRDB, or Realm for persistence
- Designing concurrency with `async/await`, actors, `Sendable`, or Combine
- Architecting with MVVM, MVC, TCA, or VIPER
- Submitting to App Store, configuring TestFlight, or managing provisioning profiles
- Profiling with Instruments (Time Profiler, Allocations, Leaks, SwiftUI, Core Animation)
- Implementing accessibility: VoiceOver, Dynamic Type, Switch Control, Reduce Motion
- Setting up CI/CD with Xcode Cloud, GitHub Actions + `xcodebuild`, or Fastlane
- Bridging UIKit and SwiftUI in a mixed codebase

**Do NOT invoke for:**
- Cross-platform frameworks (Flutter, React Native, KMM) — use `mobile-developer`
- Android/Kotlin/Compose — out of scope
- Backend API design — use `api-designer` or `backend-developer`
- General system architecture — use `system-architect`

---

## Decision Trees

### 1. SwiftUI vs UIKit

```
Building a new screen on iOS
├── Minimum deployment target ≥ iOS 16?
│   ├── YES → Does it need UIKit-only features?
│   │   ├── YES (MKMapView, WKWebView, UIImagePicker, PDFKit, rich text editing)
│   │   │   └── Use UIViewControllerRepresentable wrapping UIKit
│   │   └── NO  → Use SwiftUI with NavigationStack
│   └── NO (iOS 15 or lower)
│       ├── Complex collection views, custom layouts, or pixel-perfect control
│       │   └── Use UIKit (UICollectionView with compositional layout)
│       └── Simple forms, lists, or settings
│           └── Use SwiftUI (back-deploy most modifiers to iOS 15)
└── Need to integrate with existing UIKit codebase?
    ├── YES → Wrap SwiftUI in UIHostingController; UIKit owns navigation
    └── NO  → Pure SwiftUI with NavigationStack
```

### 2. Architecture Pattern

```
Choosing architecture for an iOS app
├── Solo developer or team of 2-3?
│   └── MVVM (ObservableObject + @Published or @Observable macro on iOS 17+)
│       Pros: Simple, Apple-aligned, great SwiftUI binding
│       Cons: No strict unidirectional flow; can get messy at scale
├── Team of 4-10, complex state, needs testability?
│   ├── TCA (The Composable Architecture by Point-Free)
│   │   Pros: Strict unidirectional flow, exhaustive testing, excellent debugging
│   │   Cons: Learning curve, boilerplate, dependency on third-party framework
│   └── MVVM + UseCases + Coordinators
│       Pros: Familiar, separates concerns without framework lock-in
│       Cons: Requires discipline to keep ViewModels thin
├── Large enterprise with many modules?
│   └── VIPER or Clean Swift
│       Pros: Maximum separation, module-level independence
│       Cons: Massive boilerplate, slow to iterate
└── Prototyping or hackathon?
    └── MVC (just get it working; refactor later)
```

### 3. Concurrency Choice

```
Handling async work
├── Simple network call, single result?
│   └── async/await with URLSession.shared.data(from:)
├── Stream of values over time?
│   ├── iOS 17+ → AsyncSequence (AsyncStream, AsyncThrowingStream)
│   └── iOS 13-16 → Combine (AnyPublisher, @Published)
├── Need background task that survives app suspension?
│   └── BGTaskScheduler (BGAppRefreshTask / BGProcessingTask)
├── Heavy computation, don't block main thread?
│   └── Task.detached(priority: .background) { ... } with actor isolation
├── Shared mutable state across concurrency domains?
│   └── actor with Sendable-conforming types
└── Legacy codebase with DispatchQueue?
    └── Bridge with Continuation: withCheckedContinuation / withCheckedThrowingContinuation
```

### 4. Data Persistence

```
Choosing persistence layer
├── iOS 17+ only, SwiftUI app?
│   └── SwiftData (@Model, @Query, @Environment(\\.modelContext))
│       Pros: Zero-setup, Swift-native, automatic iCloud sync opt-in
│       Cons: Immature, limited query expressiveness, migration story evolving
├── iOS 13-16, or need fine-grained control?
│   ├── Core Data + NSPersistentCloudKitContainer
│   │   Pros: Mature, powerful, CloudKit sync built-in
│   │   Cons: Verbose, concurrency pitfalls, migration complexity
│   └── GRDB (SQLite wrapper)
│       Pros: Raw SQL when needed, observation with ValueObservation, fast
│       Cons: Third-party, no built-in CloudKit sync
├── Real-time sync, collaborative features?
│   └── CloudKit (CKContainer, CKDatabase) directly
│       Pros: Apple-managed, free tier generous, private database per user
│       Cons: No server-side logic, eventual consistency
├── Key-value settings, preferences?
│   └── @AppStorage or UserDefaults
└── Secure storage (tokens, credentials)?
    └── Keychain (via Security framework or SwiftKeychainWrapper)
```

### 5. App Distribution

```
Distributing your app
├── Development/testing phase?
│   ├── Simulator → Just build and run (⌘R)
│   ├── Physical device → Xcode auto-signing with Personal Team or Developer account
│   └── Internal testers (≤100) → TestFlight Internal (no review, instant)
├── Beta testing?
│   └── TestFlight External (≤10,000 testers)
│       ├── First build → Requires Beta App Review (~24-48 hours)
│       └── Subsequent builds → No review unless significant changes
├── Production release?
│   └── App Store Connect submission
│       ├── Passes App Review (~24 hours typical, up to 5 days)
│       ├── Options: Manual release, phased release (7 days), auto-release
│       └── Must pass: no crashes, complete metadata, privacy labels, export compliance
└── Enterprise/Internal distribution?
    ├── Apple Business Manager + MDM → For employees
    └── Enterprise Program (in-house) → For internal-only apps (no App Store)
```

### 6. Animation Performance

```
Animation jank detected
├── Running on simulator? → Test on device first; simulator ≠ device GPU
├── Check Instruments > Core Animation template
│   ├── FPS consistently <55? → Too much work on main thread
│   │   └── Profile with Time Profiler; offload heavy work
│   ├── "Hitches" detected? → Inconsistent frame pacing
│   └── "Impact" > 10ms? → Identify the slow phase
├── Using implicit animations (.animation modifier)?
│   └── Prefer withAnimation { } block for explicit control
├── Animating layout (offset, frame)?
│   └── Use .drawingGroup() to rasterize, or Canvas for custom drawing
├── Animating many views simultaneously?
│   └── Reduce to animating a single container; use matchedGeometryEffect for transitions
├── Shadows or blurs during animation?
│   └── Cache shadow path: view.layer.shadowPath = UIBezierPath(…).cgPath
└── List/ScrollView during animation?
    └── Avoid GeometryReader inside scrolling lists; use .scrollPosition(id:) instead
```

---

## Core Workflow

### A. SwiftUI Views

Build composable, testable views using a strict hierarchy:

```swift
// Screen = Navigation container
struct ProductListScreen: View {
    @State private var viewModel = ProductListViewModel()

    var body: some View {
        NavigationStack {
            ProductListContentView(state: viewModel.state)
                .navigationTitle("Products")
                .task { await viewModel.load() }
        }
    }
}

// Content = State-driven switch
struct ProductListContentView: View {
    let state: ProductListState

    var body: some View {
        switch state {
        case .loading:   ProgressView("Loading…")
        case .empty:     ContentUnavailableView("No Products", systemImage: "bag")
        case .loaded(let items): ProductGrid(items: items)
        case .error(let msg): ErrorView(message: msg)
        }
    }
}

// Leaf = Stateless, data-in-events-out
struct ProductCard: View {
    let product: Product
    let onFavorite: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            AsyncImage(url: product.thumbnailURL) { $0.resizable().aspectRatio(contentMode: .fill) }
                .frame(height: 140).clipShape(RoundedRectangle(cornerRadius: 12))
            Text(product.name).font(.headline).lineLimit(2)
            HStack { Text(product.price); Spacer(); Button(action: onFavorite) { Image(systemName: "heart") } }
        }
    }
}
```

### B. Data Flow

| Mechanism | When to Use | iOS Min |
|-----------|-------------|---------|
| `@State` | Local view state owned by the view | 13+ |
| `@Binding` | Parent owns state, child mutates | 13+ |
| `@StateObject` / `@ObservedObject` | Reference-type ObservableObject | 13+ |
| `@EnvironmentObject` | Deep dependency injection across view tree | 13+ |
| `@Observable` (macro) | iOS 17+ replacement for ObservableObject | 17+ |
| `@Environment` | System values (colorScheme, modelContext, dismiss) | 13+ |
| `@AppStorage` | UserDefaults-backed state | 14+ |

**Rule of thumb:** Prefer `@Observable` on iOS 17+. For iOS 16-, use `@StateObject` for owners and `@ObservedObject` for children.

### C. Navigation (NavigationStack)

```swift
enum Route: Hashable {
    case productDetail(Product.ID)
    case checkout
    case settings
}

struct AppNavigation: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            HomeView()
                .navigationDestination(for: Route.self) { route in
                    switch route {
                    case .productDetail(let id): ProductDetailView(id: id)
                    case .checkout:              CheckoutView()
                    case .settings:              SettingsView()
                    }
                }
        }
    }
}
```

### D. Networking

```swift
// Protocol for testability
protocol APIServiceProtocol {
    func fetch<T: Decodable>(_ endpoint: Endpoint) async throws -> T
}

struct APIService: APIServiceProtocol {
    private let session: URLSession
    private let decoder: JSONDecoder

    init(session: URLSession = .shared) {
        self.session = session
        self.decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        decoder.dateDecodingStrategy = .iso8601
    }

    func fetch<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        let (data, response) = try await session.data(for: endpoint.urlRequest)
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw APIError.invalidResponse
        }
        return try decoder.decode(T.self, from: data)
    }
}
```

### E. Persistence (Core Data / SwiftData)

**SwiftData (iOS 17+):**

```swift
@Model final class Note {
    var title: String
    var bodyText: String
    var createdAt: Date
    @Relationship(deleteRule: .cascade) var tags: [Tag]

    init(title: String, bodyText: String) {
        self.title = title
        self.bodyText = bodyText
        self.createdAt = .now
        self.tags = []
    }
}

// Usage
struct NotesList: View {
    @Query(sort: \Note.createdAt, order: .reverse) private var notes: [Note]
    @Environment(\\.modelContext) private var context

    var body: some View {
        List(notes) { note in NoteRow(note: note) }
    }
}
```

**Core Data (iOS 13+):**

```swift
final class PersistenceController {
    static let shared = PersistenceController()
    let container: NSPersistentContainer

    init() {
        container = NSPersistentContainer(name: "Model")
        container.loadPersistentStores { _, error in
            if let error = error { fatalError("Core Data error: \\(error)") }
        }
        container.viewContext.automaticallyMergesChangesFromParent = true
    }
}
```

### F. Concurrency

```swift
// MainActor-isolated ViewModel
@MainActor
final class ProductListViewModel {
    private let service: APIServiceProtocol
    private(set) var state: ProductListState = .loading

    init(service: APIServiceProtocol = APIService()) {
        self.service = service
    }

    func load() async {
        state = .loading
        do {
            let products: [Product] = try await service.fetch(.products)
            state = products.isEmpty ? .empty : .loaded(products)
        } catch {
            state = .error(error.localizedDescription)
        }
    }
}

// Actor for thread-safe caching
actor ImageCache {
    private var storage: [URL: UIImage] = [:]

    func image(for url: URL) -> UIImage? { storage[url] }
    func store(_ image: UIImage, for url: URL) { storage[url] = image }
}

// Sendable model
struct Product: Codable, Identifiable, Sendable {
    let id: Int
    let name: String
    let price: Double
}
```

### G. Testing (XCTest)

```swift
final class ProductListViewModelTests: XCTestCase {
    func testLoadProductsSuccess() async throws {
        let mockService = MockAPIService()
        mockService.stubProducts = [.mock(id: 1, name: "Widget")]

        let viewModel = await ProductListViewModel(service: mockService)
        await viewModel.load()

        let state = await viewModel.state
        guard case .loaded(let products) = state else {
            return XCTFail("Expected .loaded, got \\(state)")
        }
        XCTAssertEqual(products.count, 1)
        XCTAssertEqual(products.first?.name, "Widget")
    }

    func testLoadProductsEmpty() async throws {
        let mockService = MockAPIService()
        mockService.stubProducts = []

        let viewModel = await ProductListViewModel(service: mockService)
        await viewModel.load()

        let state = await viewModel.state
        guard case .empty = state else {
            return XCTFail("Expected .empty, got \\(state)")
        }
    }
}
```

### H. Accessibility (VoiceOver)

```swift
// Minimum viable accessibility for every view
struct AccessibleProductCard: View {
    let product: Product

    var body: some View {
        VStack {
            AsyncImage(url: product.imageURL)
            Text(product.name)
            Text(product.price)
        }
        .accessibilityElement(children: .combine)        // One element, not three
        .accessibilityLabel("\\(product.name), \\(product.price)") // Concise label
        .accessibilityHint("Double-tap to view details")          // Action hint
        .accessibilityAddTraits(.isButton)                        // Behaves like button
    }
}

// Critical accessibility checklist:
// [ ] Every interactive element has accessibilityLabel
// [ ] Images have accessibilityLabel or are marked .accessibilityHidden(true) if decorative
// [ ] Dynamic Type up to accessibilityExtraExtraExtraLarge doesn't truncate
// [ ] Minimum contrast ratio 4.5:1 for body text, 3:1 for large text
// [ ] VoiceOver swipe order matches visual order
// [ ] Reduce Motion respected with .accessibilityReduceMotion
// [ ] Button hit targets ≥ 44×44 points
```

### I. Instruments Profiling

```bash
# Launch profiling from CLI
xcodebuild test \
  -project App.xcodeproj \
  -scheme App \
  -destination 'platform=iOS Simulator,name=iPhone 16 Pro' \
  -enablePerformanceTests

# Key Instruments templates:
# Time Profiler  → CPU hotspots (target: <60ms per frame on main thread)
# Allocations    → Memory growth patterns (target: returns to baseline after screen dismiss)
# Leaks          → Retain cycles (target: zero leaks after 5-min interaction)
# SwiftUI        → Body invocation count (target: no redundant recomputations)
# Core Animation → FPS & hitches (target: 60fps minimum, 120fps ProMotion)
# Energy Log     → Battery impact (target: <1% battery per active minute)
```

---

## Cross-Skill Coordination

| Scenario | Coordinate With | Handoff Artifact |
|----------|----------------|------------------|
| UI/UX design specs for a screen | `ui-ux-designer` | Figma link or design token JSON |
| Backend API contract for a mobile endpoint | `api-designer` | OpenAPI 3.1 spec with mobile-specific pagination |
| System architecture for data sync strategy | `system-architect` | C4 Container diagram showing mobile ↔ cloud boundary |
| Architecture pattern translation to mobile | `mobile-architecture-patterns` | Pattern selection rationale doc |
| Full-stack feature spanning iOS + backend | `fullstack-developer` | API contract + iOS client implementation |
| QA strategy and test cases | `qa-engineer` | XCTest test plan + UI test coverage report |
| Security review of auth and data storage | `security-reviewer` | Threat model for mobile attack surface |
| CI/CD pipeline for TestFlight builds | `ci-cd-builder` | Fastlane lane + GitHub Actions workflow YAML |

---

## Proactive Triggers

When you detect these patterns, speak up with dollar-quantified impact:

| Trigger | Action | Annual Value |
|---------|--------|-------------|
| Missing `Info.plist` privacy descriptions | "App will crash when accessing camera/mic/photos. Add `NSCameraUsageDescription` now." | **$50K** (avoids crash + rejection) |
| No accessibility labels on interactive elements | "A11y lawsuit risk. Every button needs `.accessibilityLabel`. Fix in <2 hours now or 2 weeks later." | **$200K-$2M** (lawsuit avoidance) |
| `try?` discarding errors silently | "If this network call fails, the user sees a blank screen. Handle the error with retry + user message." | **$80K** (user churn from silent failures) |
| No `.gitignore` for `*.xcodeproj` user state | "xcuserdata will cause merge conflicts. Add `.gitignore` entry for `xcuserdata/`." | **$30K** (team productivity) |
| `DispatchQueue.main.async` for networking | "You're blocking the main thread. Switch to `async/await` with proper actor isolation." | **$60K** (performance + review rejection) |
| Hardcoded deployment target too aggressive | "Dropping iOS 15 loses 12% of users. Set `IPHONEOS_DEPLOYMENT_TARGET = 16.0` at most aggressive." | **$200K+** (market reach) |
| No privacy manifest (PrivacyInfo.xcprivacy) | "App will be rejected starting May 2024. Create `PrivacyInfo.xcprivacy` with required API reasons." | **$150K** (delayed launch) |

---

## What Good Looks Like

A 10/10 iOS feature delivery includes:

1. **Complete screen states:** loading, loaded, empty, error — all four covered with appropriate UI
2. **Zero console warnings.** No purple runtime warnings, no Auto Layout constraint breaks, no `UITableView` rebuilding warnings
3. **Accessibility-annotated.** Every interactive element labeled; Dynamic Type tested to maximum size
4. **Protocol-based networking.** Service behind a protocol for testability; no singletons without dependency injection
5. **Actor-isolated ViewModels.** `@MainActor` on all observable view state; data fetching off-main
6. **Instruments-verified.** Leaks template shows zero leaks after full navigation cycle; Allocations returns to baseline
7. **Privacy-complete.** `PrivacyInfo.xcprivacy` present; all sensitive APIs have usage descriptions
8. **Builds from clean.** Fresh `git clone` → open `.xcodeproj` → ⌘R builds without manual configuration
9. **Unit tests for ViewModel logic.** At minimum: success path, empty state, error state, and edge case
10. **Documented architecture decision.** README or ADR explains why MVVM/TCA/MVC and how data flows

---

## Deliberate Practice

Three exercises to level up. Set a timer. Ship working code.

### Exercise 1: The Infinite Scrolling List (30 min)

Build a SwiftUI list that paginates from a mock API, handles loading/error/empty states, uses `@Observable` (or `@StateObject`), and has pull-to-refresh. Time yourself: can you get all four states working in 30 minutes with zero console warnings?

**Success criteria:**
- Scroll to bottom triggers next page load
- Pull-to-refresh resets pagination
- Error state shows retry button
- Empty state uses `ContentUnavailableView`
- VoiceOver reads each cell correctly

### Exercise 2: The Actor-Backed Image Cache (45 min)

Implement a thread-safe image cache using Swift actors. Download images concurrently with `TaskGroup`, cache in an `actor`, and display in a `LazyVGrid` without flickering or data races. Profile with Instruments > Allocations to verify no memory growth beyond cache limit.

**Success criteria:**
- `actor ImageCache` with insert/retrieve
- `TaskGroup` for parallel downloads
- LRU eviction when cache exceeds 50 images
- MainActor-isolated UI updates
- 60 fps scroll even with 200+ images

### Exercise 3: The App Store-Ready Feature (60 min)

Build a complete feature — from Xcode project setup to TestFlight-ready archive — for a notes app with Core Data persistence, CRUD operations, and iCloud sync. Must pass App Store validation (`xcodebuild -exportArchive`), include `PrivacyInfo.xcprivacy`, and have 80%+ test coverage on ViewModel logic.

**Success criteria:**
- `xcodebuild archive` succeeds with Release configuration
- `xcodebuild -exportArchive` passes validation
- Privacy manifest present and complete
- XCTest suite with mock Core Data stack
- Dynamic Type works up to accessibilityExtraExtraExtraLarge

---

## Gotchas

Real-world Apple platform traps and their business impact.

### 1. ATS Blocks HTTP Connections (~$50K)

**Symptom:** Network requests silently fail with `Error Domain=NSURLErrorDomain Code=-1022`.  
**Cause:** App Transport Security blocks plain HTTP connections.  
**Fix:** Add `NSAppTransportSecurity > NSAllowsArbitraryLoads` to `Info.plist` — but prefer per-domain exceptions:

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSExceptionDomains</key>
    <dict>
        <key>api.staging.example.com</key>
        <dict>
            <key>NSExceptionAllowsInsecureHTTPLoads</key>
            <true/>
        </dict>
    </dict>
</dict>
```

**Impact:** $50K in delayed launch if discovered after App Store submission. Always test on a physical device — Simulator is more lenient with ATS.

### 2. Main Actor Isolation Warning Cascade (~$20K)

**Symptom:** `Expression requiring global actor 'MainActor' cannot appear in default-value expression of property '_viewModel'`.  
**Cause:** `@StateObject` / `@State` on a `@MainActor`-isolated type in a non-isolated View.  
**Fix:** Annotate the View with `@MainActor`:

```swift
@MainActor
struct ProductListView: View {
    @State private var viewModel = ProductListViewModel() // OK now
    // ...
}
```

**Impact:** A cascade of 40+ compiler errors from one missing annotation. $20K in wasted debugging time per large feature.

### 3. Retain Cycles in Closures (~$100K memory leak)

**Symptom:** ViewModel never deinitializes; `deinit` never called. Memory grows with each navigation cycle.  
**Cause:** Strong capture of `self` in escaping closures:

```swift
// WRONG — retains self forever
service.onUpdate = { self.products = $0 }

// RIGHT — weak capture
service.onUpdate = { [weak self] products in
    self?.products = products
}
```

**Impact:** Memory leak causing app termination by jetsam. $100K+ user churn when app reliably crashes after 10-15 navigation cycles.

### 4. unowned Crash in Asynchronous Context (~$75K)

**Symptom:** `Thread 1: EXC_BAD_ACCESS` or `Fatal error: Attempted to read an unowned reference but the object was already deallocated`.  
**Cause:** `[unowned self]` when `self` can deallocate before the closure executes:

```swift
// WRONG — imageLoader may outlive self
imageLoader.load { [unowned self] image in
    self.imageView.image = image // CRASH
}

// RIGHT
imageLoader.load { [weak self] image in
    self?.imageView?.image = image
}
```

**Rule:** `unowned` is safe ONLY when the captured object is guaranteed to outlive the closure — e.g., a parent capturing its child. In async contexts, always use `weak`.

**Impact:** $75K (crash rate spike → 2-star App Store rating → 30% conversion drop).

### 5. Core Data Thread Confinement (~$60K)

**Symptom:** `CoreData: error: Serious application error. An exception was caught from the delegate... NSManagedObjectContext is accessed from wrong thread`.  
**Cause:** Reading `NSManagedObject` properties on a thread other than its context's queue.  
**Fix:**

```swift
// WRONG — viewContext is main-queue only
DispatchQueue.global().async {
    let count = context.registeredObjects.count // CRASH
}

// RIGHT — use perform/performAndWait
context.perform {
    let count = context.registeredObjects.count
}

// EVEN BETTER — pass objectID across threads
let objectID = managedObject.objectID
Task.detached {
    let context = PersistenceController.shared.container.newBackgroundContext()
    let object = context.object(with: objectID)
    // Use object safely here
}
```

**Impact:** $60K — intermittent crashes impossible to reproduce, leading to negative reviews and support burden.

### 6. SwiftUI View Identity Breakage (~$40K)

**Symptom:** Animations break, `onAppear` fires unexpectedly, state resets.  
**Cause:** Using `id(_:)` unnecessarily, or relying on indices for `ForEach` with mutable data:

```swift
// WRONG — index-based identity; state lost on reorder
ForEach(0..<items.count, id: \.self) { index in
    ItemRow(item: items[index])
}

// RIGHT — stable identity from model
ForEach(items) { item in
    ItemRow(item: item)
}
```

**Impact:** $40K in UX debt. Users report "the app glitches when I scroll fast." Debugging SwiftUI identity issues can take days.

### 7. Xcode Previews Crash Silently (~$15K)

**Symptom:** Preview canvas shows "Preview Crashed" or hangs on spinner.  
**Cause (common):**

```swift
// Previews try to access Keychain, UserDefaults suite, or network
#Preview {
    ProductListView()
        .onAppear {
            // This fires in preview too!
            APIKeyManager.shared.configure() // 💥 crash
        }
}

// FIX — guard against preview environment
#Preview {
    ProductListView()
        .environment(\.isPreview, true)
}
```

Or use mock services in previews: `ProductListView(service: MockAPIService())`.

**Impact:** $15K per feature. Developers lose preview productivity and revert to simulator-only iteration.

### 8. Missing Entitlement Silently Breaks Feature (~$45K)

**Symptom:** Feature works on Simulator, fails on device with no clear error.  
**Example:** Push notifications silently fail without `aps-environment` entitlement. iCloud sync quietly doesn't work without `com.apple.developer.icloud-container-identifiers`.  
**Fix:** Verify entitlements in `App.entitlements`:

```xml
<key>aps-environment</key>
<string>development</string>
<key>com.apple.developer.icloud-container-identifiers</key>
<array>
    <string>iCloud.com.example.app</string>
</array>
```

**Impact:** $45K — feature flagged "complete" for weeks before device testing reveals it never worked.

---

## Verification Checklist

Before marking any iOS task complete:

- [ ] Builds from clean (`xcodebuild clean build`) with zero errors and zero warnings
- [ ] All four screen states (loading, loaded, empty, error) implemented and visible
- [ ] VoiceOver reads every interactive element with meaningful labels
- [ ] Dynamic Type from `xSmall` to `accessibilityExtraExtraExtraLarge` doesn't clip or truncate
- [ ] `PrivacyInfo.xcprivacy` exists and lists all required API reason categories
- [ ] No `try?` discarding errors — all failure paths handled with user-visible feedback
- [ ] No `!` force-unwrap on optionals from external sources (network, database, user defaults)
- [ ] All closures capture `[weak self]` unless lifetime is provably shorter
- [ ] Core Data / SwiftData operations respect thread confinement
- [ ] `.gitignore` excludes `xcuserdata/`, `*.xcworkspace/xcuserdata/`, `DerivedData/`
- [ ] `Info.plist` includes `NSCameraUsageDescription`, `NSPhotoLibraryUsageDescription`, etc., for any requested permissions
- [ ] Instruments > Leaks shows zero leaks after 5-minute navigation cycle
- [ ] TestFlight archive validates with `xcodebuild -exportArchive`
- [ ] `@available` guards wrap any API newer than `IPHONEOS_DEPLOYMENT_TARGET`

---

## Anti-Rationalization — No Excuses

| Excuse | Reality |
|--------|---------|
| "I'll add accessibility later" | Adding a11y to 47 screens post-launch costs 5× more than doing it with each screen. Accessibility is a feature, not a ticket. |
| "This `try?` is fine, it'll never fail" | Airplane mode, spotty cell, server 503, expired token, JSON format change — it WILL fail. Handle it. |
| "Previews are broken, I'll just use the simulator" | You're adding 15 seconds to every view-edit-verify cycle. That's 2 hours lost per week. Fix the preview. |
| "We can bump the deployment target next sprint" | Analysis paralysis adds $0 of value. Ship on the target you have. Support N-2 iOS versions. |
| "I'll add the privacy manifest before submission" | Apple rejects apps without it since May 2024. Add it on Day 1 of any new feature touching required-reason APIs. |

---

## References

### Skill Reference Files

| File | Content | When to Load |
|------|---------|-------------|
| `references/swiftui-view-architecture.md` | View composition patterns, extraction heuristics, @Observable vs ObservableObject | Building SwiftUI screens |
| `references/uikit-swiftui-bridging.md` | UIViewRepresentable, UIViewControllerRepresentable, UIHostingController | Mixing UIKit/SwiftUI |
| `references/coredata-swiftdata-guide.md` | SwiftData @Model, Core Data NSPersistentContainer, migration strategies | Setting up persistence |
| `references/concurrency-actors.md` | async/await, actor isolation, @MainActor, TaskGroup, Sendable | Concurrency design |
| `references/app-store-submission.md` | Archive, ExportOptions.plist, TestFlight, common rejections | App Store submission |
| `references/accessibility-voiceover.md` | Labels, hints, traits, Dynamic Type, Rotor, Accessibility Inspector | Accessibility audit |
| `references/instruments-profiling.md` | Time Profiler, Allocations, Leaks, SwiftUI, Core Animation, Energy Log | Performance profiling |
| `references/xcode-build-settings.md` | xcconfig, SWIFT_OPTIMIZATION_LEVEL, privacy manifest, provisioning | Build configuration |

### Apple Documentation (Official)

| Resource | URL |
|----------|-----|
| SwiftUI Documentation | https://developer.apple.com/documentation/swiftui |
| Swift Concurrency | https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/ |
| Core Data Programming Guide | https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/CoreData/ |
| SwiftData Framework | https://developer.apple.com/documentation/swiftdata |
| Human Interface Guidelines — iOS | https://developer.apple.com/design/human-interface-guidelines/ios |
| App Store Review Guidelines | https://developer.apple.com/app-store/review/guidelines/ |
| WWDC Sessions (all) | https://developer.apple.com/videos/ |
| Instruments Help | https://help.apple.com/instruments/mac/current/ |
| Accessibility for Developers | https://developer.apple.com/accessibility/ |
| Xcode Build Settings Reference | https://developer.apple.com/documentation/xcode/build-settings-reference |
| StoreKit 2 | https://developer.apple.com/documentation/storekit |
| CloudKit | https://developer.apple.com/documentation/cloudkit |
| Sign in with Apple | https://developer.apple.com/documentation/authenticationservices |

### Third-Party Resources

| Resource | URL | Use For |
|----------|-----|---------|
| The Composable Architecture | https://github.com/pointfreeco/swift-composable-architecture | TCA reference |
| GRDB.swift | https://github.com/groue/GRDB.swift | SQLite persistence |
| Alamofire | https://github.com/Alamofire/Alamofire | Legacy networking (prefer URLSession for new code) |
| Fastlane | https://docs.fastlane.tools | CI/CD automation for screenshots, builds, and delivery |
| SwiftLint | https://github.com/realm/SwiftLint | Linting and style enforcement |

---

## Scale Depth

### Solo Developer
- Build directly in Xcode with auto-signing
- SwiftData for persistence (zero setup)
- MVVM with `@Observable` (iOS 17+)
- TestFlight Internal for testing
- No CI/CD — manual archive and upload

### Small Team (2-5)
- Shared Xcode project with `.xcconfig` for environment-specific settings
- Core Data + `NSPersistentCloudKitContainer` for sync
- MVVM + protocol-based services for testability
- GitHub Actions + Fastlane for CI/CD
- SwiftLint for style enforcement
- PR template with accessibility checklist

### Medium Team (5-20)
- Multi-module Xcode project or Swift Package Manager modules
- TCA for complex state management
- Dedicated coordinator pattern for navigation
- Xcode Cloud or Jenkins + Fastlane
- Unit tests (80%+ VM coverage) + UI tests for critical flows
- Per-view accessibility audit in PR review
- Feature flags for phased rollout

### Enterprise (20+)
- Microfeature SPM packages with strict API boundaries
- TCA or VIPER for module-level architecture
- Dedicated platform team maintaining internal frameworks
- Fully automated CI/CD: lint → test → archive → TestFlight → App Store
- Performance regression testing with Instruments automation
- Accessibility CI gate (Axe-based audits)
- Compliance automation (privacy manifests, export compliance)
- On-call rotation with crash monitoring (Firebase Crashlytics / Sentry)

---

## Production Checklist

Before any production release, verify ALL of:

1. [ ] **Code signing:** Archive succeeds with Distribution provisioning profile; no "Failed to codesign" errors
2. [ ] **Entitlements:** `aps-environment`, `com.apple.developer.icloud-container-identifiers`, and any custom entitlements match provisioning profile
3. [ ] **Privacy manifest:** `PrivacyInfo.xcprivacy` includes all required-reason API categories (UserDefaults, file timestamp, system boot time, disk space, active keyboard, etc.)
4. [ ] **ATS configuration:** No `NSAllowsArbitraryLoads` at top level without security review sign-off; per-domain exceptions preferred
5. [ ] **Launch screen:** `LaunchScreen.storyboard` exists; no blank black screen on cold launch
6. [ ] **App thinning:** Slicing enabled; `ENABLE_BITCODE` understanding (deprecated in Xcode 14+)
7. [ ] **Crash-free rate ≥ 99.5%:** Verified via Xcode Organizer or Crashlytics for last 7 days
8. [ ] **Network resilience:** All network calls have timeout + retry; no infinite spinners
9. [ ] **Background tasks:** `BGTaskScheduler` handlers complete within 30 seconds or call `expirationHandler`
10. [ ] **StoreKit 2:** IAP products fetched and displayed; `Transaction.updates` listener active; no hardcoded product IDs in production
11. [ ] **Deep links:** Universal Links configured in `apple-app-site-association`; URL scheme fallback registered
12. [ ] **App Store metadata:** Screenshots for all required sizes (6.7", 6.5", 5.5"); app description, keywords, and privacy labels complete
13. [ ] **Export compliance:** CCATS or ERN filed if using encryption beyond OS-provided (HTTPS, WPA)
14. [ ] **Accessibility:** Basic VoiceOver audit passes; no `accessibilityLabel` = "" on tappable elements
15. [ ] **Size budget:** App bundle <200 MB for cellular download; on-demand resources configured for assets exceeding threshold
