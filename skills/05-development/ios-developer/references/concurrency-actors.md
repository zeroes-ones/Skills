# Concurrency & Actors Reference

## async/await Basics

```swift
func fetchProducts() async throws -> [Product] {
    let url = URL(string: "https://api.example.com/products")!
    let (data, response) = try await URLSession.shared.data(from: url)
    guard let httpResponse = response as? HTTPURLResponse,
          (200...299).contains(httpResponse.statusCode) else {
        throw APIError.invalidResponse
    }
    return try JSONDecoder().decode([Product].self, from: data)
}
```

## Actor Isolation

```swift
actor ImageCache {
    private var cache: [URL: UIImage] = [:]

    func image(for url: URL) -> UIImage? { cache[url] }

    func insert(_ image: UIImage, for url: URL) { cache[url] = image }
}

// Usage
let cache = ImageCache()
Task {
    await cache.insert(thumbnail, for: url)
    let cached = await cache.image(for: url)
}
```

## @MainActor

```swift
@MainActor
final class ProductViewModel: ObservableObject {
    @Published var products: [Product] = []

    func load() async {
        do {
            let fetched = try await APIService.fetchProducts()
            self.products = fetched  // Safe: on MainActor
        } catch {
            // handle error on MainActor
        }
    }
}
```

## Task Groups for Parallelism

```swift
func loadDashboard() async throws -> Dashboard {
    try await withThrowingTaskGroup(of: DashboardComponent.self) { group in
        group.addTask { try await fetchProducts() }
        group.addTask { try await fetchOrders() }
        group.addTask { try await fetchAnalytics() }
        return try await group.reduce(into: Dashboard()) { $0.add($1) }
    }
}
```
