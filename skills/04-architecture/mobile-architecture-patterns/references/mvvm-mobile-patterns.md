# MVVM Mobile Patterns — Swift & Kotlin Reference

> Reference implementation of Model-View-ViewModel for iOS (SwiftUI + Combine) and Android (Jetpack Compose + Kotlin Flows).

---

## iOS Implementation (SwiftUI + Combine)

### Complete ViewModel Pattern

```swift
import Combine
import Foundation

// MARK: - State Definition

enum ViewState<T: Equatable>: Equatable {
    case idle
    case loading
    case loaded(T)
    case error(String)

    var isLoading: Bool {
        if case .loading = self { return true }
        return false
    }

    var value: T? {
        if case .loaded(let value) = self { return value }
        return nil
    }
}

// MARK: - ViewModel Protocol

protocol ViewModelProtocol: ObservableObject {
    associatedtype State: Equatable
    associatedtype Action

    var state: State { get }
    func send(_ action: Action)
}

// MARK: - Display Model (separate from Domain Model)

struct ProductDisplayModel: Equatable, Identifiable {
    let id: String
    let title: String
    let formattedPrice: String
    let availabilityBadge: String
    let imageURL: URL?

    init(from domain: Product) {
        self.id = domain.id
        self.title = domain.name
        self.formattedPrice = NumberFormatter.currency.string(
            from: NSNumber(value: domain.price)
        ) ?? "$\(domain.price)"
        self.availabilityBadge = domain.inStock ? "In Stock" : "Out of Stock"
        self.imageURL = URL(string: domain.imagePath)
    }
}

// MARK: - UseCase

protocol GetProductsUseCase {
    func execute(category: String) async throws -> [Product]
}

final class GetProductsUseCaseImpl: GetProductsUseCase {
    private let repository: ProductRepository

    init(repository: ProductRepository) {
        self.repository = repository
    }

    func execute(category: String) async throws -> [Product] {
        let products = try await repository.fetchProducts(category: category)
        guard !products.isEmpty else {
            throw DomainError.emptyResults
        }
        return products.sorted { $0.popularity > $1.popularity }
    }
}

// MARK: - ViewModel Implementation

@MainActor
final class ProductListViewModel: ViewModelProtocol {
    typealias State = ViewState<[ProductDisplayModel]>
    typealias Action = ProductListAction

    @Published private(set) var state: State = .idle

    private let getProductsUseCase: GetProductsUseCase
    private let analyticsTracker: AnalyticsTracker
    private var lastCategory: String?

    init(
        getProductsUseCase: GetProductsUseCase,
        analyticsTracker: AnalyticsTracker
    ) {
        self.getProductsUseCase = getProductsUseCase
        self.analyticsTracker = analyticsTracker
    }

    func send(_ action: Action) {
        switch action {
        case .load(let category):
            Task { await loadProducts(category: category) }
        case .refresh:
            Task { await refreshProducts() }
        case .selectProduct(let id):
            analyticsTracker.track(.productSelected(id: id))
        case .retry:
            Task { await retryLastOperation() }
        }
    }

    private func loadProducts(category: String) async {
        lastCategory = category
        state = .loading
        do {
            let products = try await getProductsUseCase.execute(category: category)
            let displayModels = products.map(ProductDisplayModel.init)
            state = .loaded(displayModels)
        } catch let error as DomainError {
            state = .error(error.userFacingMessage)
        } catch {
            state = .error("Something went wrong. Please try again.")
        }
    }

    private func refreshProducts() async {
        guard let category = lastCategory else { return }
        let products = try? await getProductsUseCase.execute(category: category)
        if let products {
            state = .loaded(products.map(ProductDisplayModel.init))
        }
    }

    private func retryLastOperation() async {
        guard let category = lastCategory else { return }
        await loadProducts(category: category)
    }
}

// MARK: - Actions

enum ProductListAction {
    case load(category: String)
    case refresh
    case selectProduct(id: String)
    case retry
}

// MARK: - View (Dumb Renderer)

struct ProductListView: View {
    @StateObject private var viewModel: ProductListViewModel

    init(viewModel: ProductListViewModel) {
        _viewModel = StateObject(wrappedValue: viewModel)
    }

    var body: some View {
        content
            .navigationTitle("Products")
            .task { viewModel.send(.load(category: "electronics")) }
            .refreshable { viewModel.send(.refresh) }
    }

    @ViewBuilder
    private var content: some View {
        switch viewModel.state {
        case .idle:
            Color.clear
        case .loading:
            ProductListSkeleton()
        case .loaded(let products):
            if products.isEmpty {
                EmptyStateView(message: "No products found")
            } else {
                List(products) { product in
                    ProductRow(product: product)
                        .onTapGesture {
                            viewModel.send(.selectProduct(id: product.id))
                        }
                }
            }
        case .error(let message):
            ErrorStateView(
                message: message,
                retryAction: { viewModel.send(.retry) }
            )
        }
    }
}

// MARK: - Unit Test Example

/*
final class ProductListViewModelTests: XCTestCase {
    func test_loadProducts_setsStateToLoaded() async {
        let mockUseCase = MockGetProductsUseCase()
        mockUseCase.stubbedResult = [Product.mock()]
        let sut = ProductListViewModel(
            getProductsUseCase: mockUseCase,
            analyticsTracker: MockAnalyticsTracker()
        )

        sut.send(.load(category: "electronics"))

        let expectation = expectation(description: "state updated")
        let cancellable = sut.$state.sink { state in
            if case .loaded(let products) = state, !products.isEmpty {
                expectation.fulfill()
            }
        }
        await fulfillment(of: [expectation], timeout: 1.0)

        XCTAssertEqual(mockUseCase.executeCallCount, 1)
        XCTAssertTrue(mockUseCase.lastCategory == "electronics")
    }
}
*/
```

---

## Android Implementation (Jetpack Compose + Kotlin Flows)

### Complete ViewModel Pattern

```kotlin
package com.example.productlist

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

// MARK: - State Definition

sealed interface ProductListUiState {
    data object Idle : ProductListUiState
    data object Loading : ProductListUiState
    data class Success(val products: List<ProductDisplayModel>) : ProductListUiState
    data class Error(val message: String) : ProductListUiState
}

// MARK: - Display Model

data class ProductDisplayModel(
    val id: String,
    val title: String,
    val formattedPrice: String,
    val availabilityBadge: String,
    val imageUrl: String?
) {
    companion object {
        fun fromDomain(product: Product): ProductDisplayModel = ProductDisplayModel(
            id = product.id,
            title = product.name,
            formattedPrice = "$${String.format("%.2f", product.price)}",
            availabilityBadge = if (product.inStock) "In Stock" else "Out of Stock",
            imageUrl = product.imagePath
        )
    }
}

// MARK: - UI Actions (Intents)

sealed interface ProductListAction {
    data class Load(val category: String) : ProductListAction
    data object Refresh : ProductListAction
    data class SelectProduct(val id: String) : ProductListAction
    data object Retry : ProductListAction
}

// MARK: - UseCase

class GetProductsUseCase @Inject constructor(
    private val repository: ProductRepository
) {
    suspend operator fun invoke(category: String): Result<List<Product>> {
        return try {
            val products = repository.fetchProducts(category)
            if (products.isEmpty()) {
                Result.failure(DomainError.EmptyResults)
            } else {
                Result.success(products.sortedByDescending { it.popularity })
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

// MARK: - ViewModel

@HiltViewModel
class ProductListViewModel @Inject constructor(
    private val getProductsUseCase: GetProductsUseCase,
    private val analyticsTracker: AnalyticsTracker
) : ViewModel() {

    private val _uiState = MutableStateFlow<ProductListUiState>(ProductListUiState.Idle)
    val uiState: StateFlow<ProductListUiState> = _uiState.asStateFlow()

    private var lastCategory: String? = null

    fun onAction(action: ProductListAction) {
        when (action) {
            is ProductListAction.Load -> loadProducts(action.category)
            is ProductListAction.Refresh -> refreshProducts()
            is ProductListAction.SelectProduct ->
                analyticsTracker.track(AnalyticsEvent.ProductSelected(action.id))
            is ProductListAction.Retry -> lastCategory?.let { loadProducts(it) }
        }
    }

    private fun loadProducts(category: String) {
        lastCategory = category
        _uiState.update { ProductListUiState.Loading }

        viewModelScope.launch {
            getProductsUseCase(category)
                .onSuccess { products ->
                    _uiState.update {
                        ProductListUiState.Success(
                            products = products.map(ProductDisplayModel::fromDomain)
                        )
                    }
                }
                .onFailure { error ->
                    _uiState.update {
                        ProductListUiState.Error(
                            when (error) {
                                is DomainError.EmptyResults -> "No products found"
                                is java.net.UnknownHostException -> "No internet connection"
                                else -> "Something went wrong. Please try again."
                            }
                        )
                    }
                }
        }
    }

    private fun refreshProducts() {
        lastCategory?.let { category ->
            viewModelScope.launch {
                getProductsUseCase(category)
                    .onSuccess { products ->
                        _uiState.update {
                            ProductListUiState.Success(
                                products = products.map(ProductDisplayModel::fromDomain)
                            )
                        }
                    }
            }
        }
    }
}

// MARK: - Composable View (Dumb Renderer)

@Composable
fun ProductListScreen(
    viewModel: ProductListViewModel = hiltViewModel(),
    onProductClick: (String) -> Unit
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    LaunchedEffect(Unit) {
        viewModel.onAction(ProductListAction.Load("electronics"))
    }

    Scaffold(topBar = { TopAppBar(title = { Text("Products") }) }) { paddingValues ->
        Box(modifier = Modifier.padding(paddingValues)) {
            when (val state = uiState) {
                is ProductListUiState.Idle -> {}
                is ProductListUiState.Loading -> ProductListSkeleton()
                is ProductListUiState.Success -> {
                    if (state.products.isEmpty()) {
                        EmptyState(message = "No products found")
                    } else {
                        LazyColumn {
                            items(state.products, key = { it.id }) { product ->
                                ProductRow(product = product, onClick = {
                                    viewModel.onAction(ProductListAction.SelectProduct(product.id))
                                    onProductClick(product.id)
                                })
                            }
                        }
                    }
                }
                is ProductListUiState.Error -> {
                    ErrorState(message = state.message) {
                        viewModel.onAction(ProductListAction.Retry)
                    }
                }
            }
        }
    }
}
```

---

## Key Design Decisions

| Decision | iOS | Android |
|---|---|---|
| State type | `enum ViewState<T>` with associated value | `sealed interface` with data classes |
| Concurrency | `async/await` (Swift 5.5+) main actor | `viewModelScope.launch` |
| Observation | `@Published` + `ObservableObject` | `StateFlow` + `collectAsStateWithLifecycle` |
| Thread safety | `@MainActor` annotation on ViewModel | Dispatchers.Main implicit in Compose |
| DI | Constructor injection via protocol | `@HiltViewModel` + `@Inject constructor` |
| Actions | Enum with associated values | Sealed interface hierarchies |

### Avoid These Anti-Patterns

1. **ViewModel owns View:** Never pass View/Context/UIViewController to ViewModel. Must survive config changes.
2. **Formatting in UI layer:** Currency, dates, plurals belong in ViewModel or DisplayModel, not in `body`/`@Composable`.
3. **Direct API calls from ViewModel:** Always inject UseCase/Repository. Direct calls make ViewModel untestable.
4. **ViewModels observing each other:** Use a shared Repository or parent ViewModel with scoped state — never peer observation.
5. **Mutable state leaking from ViewModel:** Expose immutable snapshots via `private(set)` or `StateFlow`. No external writes to ViewModel state.

### When MVVM is NOT enough

MVVM breaks down when:
- Cross-screen state sharing becomes complex (>5 screens sharing state)
- Side effects (analytics, logging) need systematic handling
- Navigation logic becomes intertwined with business logic
- You find yourself passing the same state down through 4+ screens

At that point, graduate to Clean Architecture or MVI/TCA. See the Decision Trees in SKILL.md.
