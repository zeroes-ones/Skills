# TCA — The Composable Architecture Reference

> SwiftUI-native state management with Redux-inspired unidirectional data flow. Built by Point-Free (pointfree.co). First-class composition, testing, and dependency management.

---

## Core Types

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│   ┌─────────┐    Action     ┌──────────┐    Effect    ┌──────┐ │
│   │  VIEW   │ ────────────► │ REDUCER  │ ───────────► │      │ │
│   │         │               │          │              │ STORE│ │
│   │  reads  │ ◄──────────── │ (inout   │ ◄─────────── │      │ │
│   │  STATE  │    State      │  State,  │    Action    │      │ │
│   │         │               │  Action) │              │      │ │
│   └─────────┘               └──────────┘              └──────┘ │
│                                                                │
│   State = Struct of all data the feature needs                │
│   Action = Enum of all events (user + side effect results)     │
│   Reducer = (inout State, Action) -> Effect<Action>            │
│   Effect = Async work that feeds back an Action                │
│   Store = Runtime holding state and running reducers           │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## Installation

```swift
// Package.swift
dependencies: [
    .package(url: "https://github.com/pointfreeco/swift-composable-architecture",
             from: "1.0.0")
],
targets: [
    .target(name: "MyApp", dependencies: [
        .product(name: "ComposableArchitecture", package: "swift-composable-architecture")
    ])
]
```

---

## Complete Feature: Todo List

### Domain + State

```swift
import ComposableArchitecture
import Foundation

// MARK: - State

@Reducer
struct TodoListFeature {
    @ObservableState
    struct State: Equatable {
        var todos: IdentifiedArrayOf<Todo> = []
        var newTodoText: String = ""
        var isLoading: Bool = false
        var filter: Filter = .all
        var alert: AlertState<Action.Alert>? = nil

        enum Filter: Equatable {
            case all, active, completed
        }

        var filteredTodos: IdentifiedArrayOf<Todo> {
            switch filter {
            case .all: return todos
            case .active: return todos.filter { !$0.isCompleted }
            case .completed: return todos.filter { $0.isCompleted }
            }
        }

        var statsText: String {
            let active = todos.filter { !$0.isCompleted }.count
            return "\(active) remaining · \(todos.count) total"
        }
    }

    struct Todo: Equatable, Identifiable {
        let id: UUID
        var title: String
        var isCompleted: Bool
        var createdAt: Date
    }
```

### Actions

```swift
    // MARK: - Action

    enum Action: BindableAction {
        case binding(BindingAction<State>)
        case task
        case todosLoaded(Result<[Todo], Error>)
        case addTodoButtonTapped
        case addTodo
        case deleteTodo(IndexSet)
        case toggleTodo(id: UUID)
        case filterChanged(State.Filter)
        case clearCompletedTapped
        case alert(PresentationAction<Alert>)

        enum Alert: Equatable {
            case confirmClear
            case confirmDelete(UUID)
        }
    }
```

### Reducer

```swift
    // MARK: - Reducer

    @Dependency(\.todoClient) var todoClient
    @Dependency(\.uuid) var uuid
    @Dependency(\.date) var date

    var body: some Reducer<State, Action> {
        BindingReducer()

        Reduce { state, action in
            switch action {

            case .task:
                state.isLoading = true
                return .run { send in
                    await send(.todosLoaded(
                        Result { try await todoClient.fetchAll() }
                    ))
                }

            case .todosLoaded(.success(let todos)):
                state.isLoading = false
                state.todos = IdentifiedArray(uniqueElements: todos)
                return .none

            case .todosLoaded(.failure(let error)):
                state.isLoading = false
                state.alert = AlertState {
                    TextState("Failed to load todos")
                } message: {
                    TextState(error.localizedDescription)
                }
                return .none

            case .addTodoButtonTapped:
                guard !state.newTodoText.trimmingCharacters(in: .whitespaces).isEmpty
                else { return .none }
                return .send(.addTodo)

            case .addTodo:
                let todo = Todo(
                    id: uuid(),
                    title: state.newTodoText.trimmingCharacters(in: .whitespaces),
                    isCompleted: false,
                    createdAt: date.now
                )
                state.todos.insert(todo, at: 0)
                state.newTodoText = ""
                return .run { [todo] _ in
                    try await todoClient.save(todo)
                }

            case .deleteTodo(let indexSet):
                for index in indexSet {
                    let todo = state.todos[index]
                    state.todos.remove(at: index)
                    return .run { _ in
                        try await todoClient.delete(todo.id)
                    }
                }
                return .none

            case .toggleTodo(let id):
                guard var todo = state.todos[id: id] else { return .none }
                todo.isCompleted.toggle()
                state.todos[id: id] = todo
                return .run { [todo] _ in
                    try await todoClient.save(todo)
                }

            case .filterChanged(let filter):
                state.filter = filter
                return .none

            case .clearCompletedTapped:
                state.alert = AlertState {
                    TextState("Clear completed?")
                } actions: {
                    ButtonState(role: .destructive,
                                action: .confirmClear) { TextState("Clear") }
                }
                return .none

            case .alert(.presented(.confirmClear)):
                let completed = state.todos.filter(\.isCompleted)
                state.todos.removeAll(where: \.isCompleted)
                return .run { _ in
                    for todo in completed {
                        try await todoClient.delete(todo.id)
                    }
                }

            case .alert(.presented(.confirmDelete(let id))):
                state.todos.remove(id: id)
                return .run { _ in try await todoClient.delete(id) }

            case .binding, .alert:
                return .none
            }
        }
    }
}
```

### Dependency (todoClient)

```swift
// Dependencies/TodoClient.swift
import Dependencies
import Foundation

struct TodoClient {
    var fetchAll: @Sendable () async throws -> [TodoListFeature.Todo]
    var save: @Sendable (TodoListFeature.Todo) async throws -> Void
    var delete: @Sendable (UUID) async throws -> Void
}

extension TodoClient: DependencyKey {
    static let liveValue = TodoClient(
        fetchAll: { /* API or local DB call */ [] },
        save: { _ in /* Save to API/DB */ },
        delete: { _ in /* Delete from API/DB */ }
    )

    static let testValue = TodoClient(
        fetchAll: { [] },
        save: { _ in },
        delete: { _ in }
    )
}

extension DependencyValues {
    var todoClient: TodoClient {
        get { self[TodoClient.self] }
        set { self[TodoClient.self] = newValue }
    }
}
```

### View

```swift
struct TodoListView: View {
    @Bindable var store: StoreOf<TodoListFeature>

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Input
                HStack {
                    TextField("What needs to be done?",
                              text: $store.newTodoText)
                        .textFieldStyle(.roundedBorder)
                    Button("Add") {
                        store.send(.addTodoButtonTapped)
                    }
                    .disabled(store.newTodoText.trimmingCharacters(
                        in: .whitespaces).isEmpty)
                }
                .padding()

                // Filter
                Picker("Filter", selection: $store.filter.sending(\.filterChanged)) {
                    Text("All").tag(TodoListFeature.State.Filter.all)
                    Text("Active").tag(TodoListFeature.State.Filter.active)
                    Text("Completed").tag(TodoListFeature.State.Filter.completed)
                }
                .pickerStyle(.segmented)
                .padding(.horizontal)

                // List
                if store.isLoading {
                    ProgressView()
                        .frame(maxHeight: .infinity)
                } else {
                    List {
                        ForEach(store.filteredTodos) { todo in
                            HStack {
                                Button {
                                    store.send(.toggleTodo(id: todo.id))
                                } label: {
                                    Image(systemName: todo.isCompleted
                                          ? "checkmark.circle.fill"
                                          : "circle")
                                }
                                Text(todo.title)
                                    .strikethrough(todo.isCompleted)
                            }
                        }
                        .onDelete { store.send(.deleteTodo($0)) }
                    }
                }
            }
            .navigationTitle("Todos")
            .toolbar {
                ToolbarItem(placement: .status) {
                    Text(store.statsText)
                        .font(.caption)
                }
                ToolbarItem(placement: .primaryAction) {
                    Button("Clear") { store.send(.clearCompletedTapped) }
                }
            }
        }
        .alert($store.scope(state: \.alert, action: \.alert))
        .task { await store.send(.task).finish() }
    }
}
```

---

## Composing Features (Parent-Child)

```swift
@Reducer
struct AppFeature {
    @ObservableState
    struct State: Equatable {
        var todoList = TodoListFeature.State()
        var settings = SettingsFeature.State()
        var selectedTab: Tab = .todos

        enum Tab { case todos, settings }
    }

    enum Action {
        case todoList(TodoListFeature.Action)
        case settings(SettingsFeature.Action)
        case tabSelected(State.Tab)
    }

    var body: some Reducer<State, Action> {
        Scope(state: \.todoList, action: \.todoList) {
            TodoListFeature()
        }
        Scope(state: \.settings, action: \.settings) {
            SettingsFeature()
        }

        Reduce { state, action in
            switch action {
            case .tabSelected(let tab):
                state.selectedTab = tab
                return .none
            case .todoList, .settings:
                return .none
            }
        }
    }
}
```

---

## Testing TCA

```swift
@MainActor
func testAddTodo() async {
    let store = TestStore(initialState: TodoListFeature.State()) {
        TodoListFeature()
    } withDependencies: {
        $0.uuid = .incrementing
        $0.date = .constant(Date(timeIntervalSince1970: 0))
    }

    store.state.newTodoText = "Buy groceries"
    await store.send(.addTodoButtonTapped)
    await store.send(.addTodo) {
        $0.todos = [
            TodoListFeature.Todo(
                id: UUID(0),
                title: "Buy groceries",
                isCompleted: false,
                createdAt: Date(timeIntervalSince1970: 0)
            )
        ]
        $0.newTodoText = ""
    }
}

func testToggleTodo() async {
    var todo = TodoListFeature.Todo(
        id: UUID(0), title: "Test", isCompleted: false,
        createdAt: Date()
    )
    let store = TestStore(
        initialState: TodoListFeature.State(todos: [todo])
    ) {
        TodoListFeature()
    }

    await store.send(.toggleTodo(id: UUID(0))) {
        $0.todos[id: UUID(0)]?.isCompleted = true
    }
}
```

---

## When TCA Excels

- Complex cross-screen state that would require massive parent ViewModels in MVVM
- Apps where every screen is a composition of smaller features
- Teams wanting exhaustive test coverage (TCA TestStore is best-in-class)
- SwiftUI-only apps (TCA does not support UIKit directly)
- Apps needing time-travel debugging and state persistence built-in
