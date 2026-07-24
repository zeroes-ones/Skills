# SwiftUI View Architecture Reference

## View Composition Pattern

```swift
// Screen-Level View
struct ProductListView: View {
    @State private var viewModel = ProductListViewModel()

    var body: some View {
        NavigationStack {
            Group {
                switch viewModel.state {
                case .loading: ProgressView("Loading products…")
                case .empty: EmptyStateView(retry: { Task { await viewModel.load() } })
                case .loaded(let products): ProductGrid(products: products)
                case .error(let message): ErrorBanner(message: message)
                }
            }
            .navigationTitle("Products")
        }
        .task { await viewModel.load() }
    }
}

// Reusable Component
struct ProductCard: View {
    let product: Product
    let onTap: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            AsyncImage(url: product.thumbnailURL) { phase in
                phase.image?.resizable().aspectRatio(contentMode: .fill)
                ?? Color.gray.opacity(0.2)
            }
            .frame(height: 160)
            .clipShape(RoundedRectangle(cornerRadius: 12))

            Text(product.name).font(.headline).lineLimit(2)
            Text(product.formattedPrice).font(.subheadline).foregroundStyle(.secondary)
        }
        .onTapGesture(perform: onTap)
    }
}
```

## View Extraction Heuristic
- Extract when a body exceeds ~40 lines
- Extract when a subview has its own @State or @Binding
- Prefer `struct` views over `var` computed properties for identity stability
