## 5. Core Desktop Architecture Patterns

### 5.1 MVVM (Model-View-ViewModel)

The dominant pattern for data-binding-native frameworks (WPF, WinUI 3, SwiftUI, Avalonia).

```
┌──────────────┐     Data Binding      ┌─────────────────┐
│    VIEW      │◄──────────────────────►│   VIEWMODEL     │
│  (XAML,      │   Commands/Events      │  (Observable     │
│   SwiftUI,   │                        │   Objects,       │
│   HTML/CSS)  │                        │   @Published)    │
└──────────────┘                        └────────┬────────┘
                                                  │
                                         ┌────────▼────────┐
                                         │     MODEL        │
                                         │  (Domain Logic,  │
                                         │   Data Access,   │
                                         │   Validation)    │
                                         └─────────────────┘
```

**Key rules:**
- ViewModel never holds a reference to View — only exposes observables
- Model never imports View/ViewModel namespaces
- Commands encapsulate actions with `canExecute` guards
- Use `INotifyPropertyChanged` (WPF), `@Published` (SwiftUI), or `Observable` (MobX for Electron)

**Anti-patterns:**
- ViewModels that import UI frameworks (`System.Windows`, `SwiftUI`) — testability destroyed
- Models that know about data binding — tight coupling to presentation
- Views with logic beyond simple property/event wiring

See: [reference/desktop-mvvm-patterns.md](reference/desktop-mvvm-patterns.md)

### 5.2 Redux-Style / Unidirectional Data Flow

Best for complex state with undo/redo, time-travel debugging, or multi-window sync.

```
┌──────────┐   dispatch(action)   ┌──────────┐   new state   ┌──────────┐
│  VIEW    │─────────────────────►│ REDUCER  │──────────────►│  STORE   │
│          │                      │(pure fn) │               │(single   │
│          │                      └──────────┘               │ source   │
│          │                                                 │ of truth)│
│          │◄────────────────────────────────────────────────┤          │
└──────────┘              subscribe(state)                   └──────────┘
```

**Desktop-specific concerns:**
- Multiple windows = multiple stores or a single store with scoped selectors
- Main process store + renderer process stores with IPC sync
- Middleware for persistence (redux-persist with SQLite adapter)
- Action serialization for undo stack (keep actions, not snapshots)

See: [reference/desktop-state-management.md](reference/desktop-state-management.md)

### 5.3 MVP (Model-View-Presenter)

Best for frameworks without native data binding, or when you need maximum testability.

```
┌──────────┐   interface   ┌─────────────┐              ┌──────────┐
│  VIEW    │◄──────────────┤  PRESENTER   │─────────────►│  MODEL   │
│ (passive,│               │ (mediator,   │              │          │
│  no logic│               │  testable)   │              │          │
│  at all) │──────────────►│              │              │          │
└──────────┘  user events   └─────────────┘              └──────────┘
```

**Rule:** Presenter has zero knowledge of UI framework. It receives plain data from View interface and returns plain data. Test presenters with mock Views — 100% coverage achievable.

### 5.4 Event-Driven Architecture

For apps with loosely coupled subsystems (notifications, plugins, system tray, menu bar).

```
┌──────────┐  event   ┌──────────────┐  event   ┌──────────┐
│ Producer │─────────►│  Event Bus    │─────────►│ Consumer │
│  (Window │          │  (typed,      │          │  (Tray,  │
│   A)     │          │   centralized)│          │   Menu)  │
└──────────┘          └──────────────┘          └──────────┘
```

**Desktop event bus patterns:**
- Electron: `ipcMain`/`ipcRenderer` for cross-process, `EventEmitter` for intra-process
- Tauri: event system (`listen`/`emit`) with JSON payloads
- Native: OS event loops (NSNotificationCenter on macOS, Windows message pump)

---
