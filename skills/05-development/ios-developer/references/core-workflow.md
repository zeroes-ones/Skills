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
