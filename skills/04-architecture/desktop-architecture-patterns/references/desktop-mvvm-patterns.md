# Desktop MVVM Patterns — Deep Dive

## Overview

Model-View-ViewModel (MVVM) is the dominant architectural pattern for desktop frameworks with native data binding support. It enforces strict separation of concerns: the View is purely declarative, the ViewModel exposes observable state and commands, and the Model contains domain logic with zero UI knowledge.

---

## Pattern Fundamentals

### The Three Layers

```
┌─────────────────────────────────────────────────────────┐
│                        VIEW                              │
│  • Declarative markup (XAML, SwiftUI, HTML)              │
│  • Zero business logic — only property/event wiring      │
│  • DataContext/BindingContext → ViewModel reference      │
│  • NEVER imports Model or Service namespaces             │
├─────────────────────────────────────────────────────────┤
│                     VIEWMODEL                            │
│  • Exposes ObservableObject / INotifyPropertyChanged     │
│  • ICommand / RelayCommand for actions                   │
│  • Transforms Model data for View consumption            │
│  • Never holds a reference to View                       │
│  • Testable without UI framework (pure C#/Swift/TS)      │
├─────────────────────────────────────────────────────────┤
│                       MODEL                              │
│  • Domain entities, validation rules, business logic     │
│  • Data access (repositories, services)                  │
│  • Zero knowledge of View or ViewModel                   │
│  • Pure — no framework dependencies                      │
└─────────────────────────────────────────────────────────┘
```

---

## Platform Implementations

### WPF / WinUI 3 (C#)

```csharp
// ViewModel — no UI dependencies
public class CustomerViewModel : INotifyPropertyChanged
{
    private readonly ICustomerRepository _repo;
    private Customer? _selectedCustomer;

    public ObservableCollection<Customer> Customers { get; } = new();
    public ICommand LoadCommand { get; }
    public ICommand SaveCommand { get; }

    public Customer? SelectedCustomer
    {
        get => _selectedCustomer;
        set { _selectedCustomer = value; OnPropertyChanged(); }
    }

    public CustomerViewModel(ICustomerRepository repo)
    {
        _repo = repo;
        LoadCommand = new RelayCommand(async () =>
        {
            var customers = await _repo.GetAllAsync();
            Customers.Clear();
            foreach (var c in customers) Customers.Add(c);
        });
        SaveCommand = new RelayCommand(
            async () => await _repo.SaveAsync(SelectedCustomer),
            () => SelectedCustomer != null);
    }

    public event PropertyChangedEventHandler? PropertyChanged;
    protected void OnPropertyChanged([CallerMemberName] string? name = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
}
```

```xml
<!-- View — XAML, zero logic -->
<Window x:Class="MyApp.Views.CustomerView"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation">
    <Grid>
        <ListBox ItemsSource="{Binding Customers}"
                 SelectedItem="{Binding SelectedCustomer}" />
        <Button Command="{Binding LoadCommand}" Content="Load" />
        <Button Command="{Binding SaveCommand}" Content="Save" />
    </Grid>
</Window>
```

**Key WPF concerns:**
- `Dispatcher.InvokeAsync` for UI thread marshaling from async operations
- `ObservableCollection<T>` for list binding (batched updates with `AddRange` extensions)
- `RelayCommand` with `CanExecute` for automatic button enable/disable
- Dependency injection via constructor — test ViewModels with mock repositories

### SwiftUI (macOS)

```swift
// ViewModel — @MainActor for UI-bound state
@MainActor
class ProjectViewModel: ObservableObject {
    @Published var projects: [Project] = []
    @Published var selectedProject: Project?
    @Published var isLoading = false
    @Published var errorMessage: String?

    private let service: ProjectService

    init(service: ProjectService) {
        self.service = service
    }

    func loadProjects() async {
        isLoading = true
        defer { isLoading = false }
        do {
            projects = try await service.fetchAll()
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}

// View — declarative, testable via Preview
struct ProjectListView: View {
    @StateObject private var viewModel: ProjectViewModel

    init(viewModel: ProjectViewModel) {
        _viewModel = StateObject(wrappedValue: viewModel)
    }

    var body: some View {
        List(viewModel.projects, selection: $viewModel.selectedProject) { project in
            ProjectRow(project: project)
        }
        .task { await viewModel.loadProjects() }
        .overlay { if viewModel.isLoading { ProgressView() } }
    }
}
```

**Key SwiftUI concerns:**
- `@MainActor` on ViewModel — all `@Published` updates must be on main thread
- `@StateObject` for ViewModel ownership in View — survives redraws
- `@ObservedObject` for injected ViewModels from parent
- `NSManagedObjectContext` integration for CoreData-backed Models
- `AppStorage` for simple preference binding without ViewModel intermediation

### Electron + React + MobX

```typescript
// ViewModel (MobX store) — framework-agnostic, testable
import { makeAutoObservable, runInAction } from 'mobx';

class CustomerStore {
  customers: Customer[] = [];
  selectedCustomer: Customer | null = null;
  isLoading = false;
  error: string | null = null;

  constructor(private repo: CustomerRepository) {
    makeAutoObservable(this);
  }

  async loadCustomers() {
    this.isLoading = true;
    try {
      const result = await this.repo.getAll();
      runInAction(() => {
        this.customers = result;
        this.isLoading = false;
      });
    } catch (e) {
      runInAction(() => {
        this.error = (e as Error).message;
        this.isLoading = false;
      });
    }
  }

  async saveCustomer() {
    if (!this.selectedCustomer) return;
    await this.repo.save(this.selectedCustomer);
  }

  get activeCustomerCount() {
    return this.customers.filter(c => c.isActive).length;
  }
}

// View (React component) — observer pattern
import { observer } from 'mobx-react-lite';

const CustomerList: React.FC<{ store: CustomerStore }> = observer(({ store }) => {
  useEffect(() => { store.loadCustomers(); }, [store]);

  return (
    <div>
      {store.isLoading && <Spinner />}
      {store.error && <ErrorBanner message={store.error} />}
      <ListBox
        items={store.customers}
        selected={store.selectedCustomer}
        onSelect={(c) => store.selectedCustomer = c}
      />
      <Button onClick={() => store.saveCustomer()} disabled={!store.selectedCustomer}>
        Save ({store.activeCustomerCount} active)
      </Button>
    </div>
  );
});
```

**Key Electron + MobX concerns:**
- `makeAutoObservable` for automatic tracking — no manual decorators
- `runInAction` for async boundaries — MobX strict mode enforces this
- Computed properties (`get`) for derived state — automatically memoized
- Store instantiation in preload/contextBridge scope for IPC integration

---

## ViewModel Design Rules

### Command Pattern

| Rule | Why |
|------|-----|
| Commands expose `canExecute` | Buttons auto-disable; no polling |
| Async commands handle loading/error states | User needs feedback; ViewModel owns UI state |
| Commands accept parameters via `CommandParameter` | Reusable commands across multiple buttons |
| Long-running commands show progress | ViewModel exposes `isSaving`, `progress` observables |

### State Exposure

```typescript
// BAD: ViewModel exposes raw Model types
class BadViewModel {
  customers: Customer[] = []; // View can mutate entities directly
}

// GOOD: ViewModel exposes readonly View-friendly types
class GoodViewModel {
  private _customers: Customer[] = [];
  get customerViews(): ReadonlyArray<CustomerView> {
    return this._customers.map(c => ({
      id: c.id,
      displayName: `${c.firstName} ${c.lastName}`,
      statusColor: c.isActive ? 'green' : 'gray'
    }));
  }
}
```

### Threading Model

| Framework | UI Thread | Background Work | Marshaling |
|-----------|-----------|-----------------|------------|
| WPF/WinUI | STA Dispatcher | `Task.Run` + `ConfigureAwait(false)` | `Dispatcher.InvokeAsync` |
| SwiftUI | `@MainActor` | `Task.detached` (background priority) | `await MainActor.run` |
| Electron | Renderer main thread | `worker_threads` / Web Workers | `ipcRenderer.invoke` / `postMessage` |

---

## Testing MVVM

### ViewModel Unit Tests (WPF)

```csharp
[Test]
public async Task LoadCommand_PopulatesCustomers_FromRepository()
{
    var mockRepo = new Mock<ICustomerRepository>();
    mockRepo.Setup(r => r.GetAllAsync()).ReturnsAsync(new[] {
        new Customer { Id = 1, Name = "Acme" }
    });

    var vm = new CustomerViewModel(mockRepo.Object);
    vm.LoadCommand.Execute(null);

    Assert.That(vm.Customers.Count, Is.EqualTo(1));
    Assert.That(vm.Customers[0].Name, Is.EqualTo("Acme"));
}

[Test]
public void SaveCommand_CanExecute_OnlyWhenCustomerSelected()
{
    var vm = new CustomerViewModel(Mock.Of<ICustomerRepository>());
    Assert.That(vm.SaveCommand.CanExecute(null), Is.False);

    vm.SelectedCustomer = new Customer { Id = 1 };
    Assert.That(vm.SaveCommand.CanExecute(null), Is.True);
}
```

### ViewModel Unit Tests (Swift)

```swift
func testLoadProjects_FillsPublishedArray() async {
    let mockService = MockProjectService()
    mockService.stubbedProjects = [Project(id: "1", name: "Test")]

    let vm = await ProjectViewModel(service: mockService)
    await vm.loadProjects()

    XCTAssertEqual(vm.projects.count, 1)
    XCTAssertEqual(vm.projects.first?.name, "Test")
}
```

### ViewModel Unit Tests (MobX + Jest)

```typescript
test('loadCustomers sets state on success', async () => {
  const mockRepo = { getAll: jest.fn().mockResolvedValue([{ id: '1', name: 'Acme' }]) };
  const store = new CustomerStore(mockRepo as any);

  await store.loadCustomers();

  expect(store.customers).toHaveLength(1);
  expect(store.isLoading).toBe(false);
  expect(store.error).toBeNull();
});
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| ViewModel references `Window` or `UserControl` | Cannot unit test, memory leaks from retained View refs | ViewModel exposes events/observables only |
| Model imports `System.Windows` or `SwiftUI` | Domain logic tied to presentation framework | Keep Model in separate, framework-free assembly/target |
| View code-behind with business logic | Logic inaccessible to tests, duplicated across Views | Move logic to ViewModel; View handles only visuals |
| `ObservableCollection` without `SuppressNotification` | Thousands of UI updates for batch operations | Use `BeginInit`/`EndInit` pattern or batched updates |
| Neglecting `IDisposable` on ViewModels | Event handler leaks, timer leaks, subscription leaks | Implement `IDisposable`, clean up in `Unloaded`/`onDisappear` |

---

## Cross-Platform MVVM Frameworks

| Framework | Platforms | Language | Data Binding |
|-----------|-----------|----------|--------------|
| Avalonia UI | Windows, macOS, Linux | C# | XAML + ReactiveUI |
| .NET MAUI | Windows, macOS | C# | XAML + MVVM Toolkit |
| Uno Platform | Windows, macOS, Linux, Web | C# | XAML + WinUI |
| React Native (Desktop) | Windows, macOS | TypeScript | React state + context |

---

## References

- [WPF MVVM Toolkit (Microsoft)](https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/)
- [SwiftUI Data Flow (Apple)](https://developer.apple.com/documentation/swiftui/state-and-data-flow)
- [MobX — Making React Reactive](https://mobx.js.org/)
- See also: [desktop-state-management.md](desktop-state-management.md)
