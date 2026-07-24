# SwiftUI vs AppKit vs Catalyst — macOS UI Framework Selection Guide

<!-- STANDARD: 3min -- definitive framework selection for macOS UI -->

## The Short Answer

| If You Need... | Use... |
|---|---|
| A standard macOS app with sidebar, toolbar, settings, menus | **SwiftUI** (macOS 13+) |
| High-performance data grids (10K+ rows, cell reuse) | **AppKit** `NSTableView` |
| Custom drawing, Metal interop, Core Animation wizardry | **AppKit** `NSView` + `CALayer` |
| Porting an existing iPad app to Mac | **Catalyst** (Mac Catalyst) |
| Menu Bar / status bar app | **SwiftUI** `MenuBarExtra` (macOS 13+) or **AppKit** `NSStatusBar` |
| Access to C APIs: CGEvent, Accessibility, IOKit | **AppKit** (bridging required) |
| A dialog/quick utility (NOT a full app) | **SwiftUI** `WindowGroup` |

**The Default**: SwiftUI for new apps. Bridge to AppKit for the 20% SwiftUI can't handle. Use Catalyst only when sharing an iPad codebase.

---

## Framework Deep Dive

### SwiftUI on macOS — Strengths

| Strength | Detail |
|---|---|
| **Rapid development** | 60% less code than AppKit equivalents. A `Settings` scene in 20 lines vs 200. |
| **Declarative syntax** | State drives UI. No manual `reloadData()`, no delegate/datasource boilerplate. |
| **Cross-platform shared logic** | Share models, ViewModels, and networking with iOS/watchOS. UI layer differs. |
| **Built-in Dark Mode** | `@Environment(\.colorScheme)` updates automatically. Asset catalog handles variants. |
| **`commands` modifier** | Add menu items declaratively. `CommandMenu`, `CommandGroup`, `ToolbarCommands`. |
| **`Settings` scene** | Preferences window with zero boilerplate: `Settings { SettingsView() }`. |
| **`DocumentGroup`** | Document-based apps with autosave, versions, and recent files — all automatic. |
| **`Table` (macOS 12+)** | Sortable, selectable, multi-column data tables with `@State` binding. |
| **`NavigationSplitView`** | Three-column sidebar layout: sidebar → content → detail. Standard macOS pattern. |

### SwiftUI on macOS — Limitations

| Limitation | Workaround |
|---|---|
| **No `NSTableView` cell reuse** | `Table`/`List` virtualizes but lacks `NSTableView`'s cell reuse efficiency for 50K+ rows. Switch to AppKit for this case. |
| **No `NSToolbar` custom view items** | `ToolbarItem` is limited. For custom toolbar items (search fields, segmented controls that resize), use `NSToolbar` via `NSViewRepresentable`. |
| **No `NSSplitView` auto-save** | `NavigationSplitView` doesn't persist sidebar width. Use `NSUserDefaults` + `@SceneStorage`. |
| **No `NSResponder` chain customization** | SwiftUI doesn't expose the AppKit responder chain. For custom key event handling, subclass `NSApplication` and override `sendEvent(_:)`. |
| **`NSOpenPanel`/`NSSavePanel` require AppKit bridging** | Wrap in `NSViewRepresentable` or call from an `AppDelegate` method. |
| **No `NSPopover` detached mode** | SwiftUI popovers are transient. For persistent detached panels, use `NSPopover` with `behavior = .transient`. |

---

### AppKit — Strengths

| Strength | Detail |
|---|---|
| **`NSTableView`** | Cell reuse, `viewBased` or `cellBased`, `rowView` customization, variable row heights, `NSTableRowView` subclassing. Handles 1M+ rows. |
| **`NSToolbar`** | Full customization: `NSToolbarItem` with arbitrary `NSView`, `NSSearchToolbarItem`, `NSToolbarItemGroup`, `allowsUserCustomization`. |
| **`NSSplitView`** | Persistent divider positions via `autosaveName`. Programmatic collapse/expand of panes. |
| **`NSWindow`** | Full control: `titlebarAppearsTransparent`, `titleVisibility`, `toolbarStyle`, `subtitle`, custom `titlebarAccessoryViewControllers`. |
| **Responder chain** | Explicit control over key event propagation, validation of menu items via `validateUserInterfaceItem(_:)`. |
| **`NSDocument`** | Mature document architecture: autosave, versions, duplicate, revert, iCloud Drive integration. |
| **`NSTextView`** | Full text system: `NSTextStorage`, `NSLayoutManager`, `NSTextContainer`. Custom text rendering, syntax highlighting, and inline attachments. |
| **`NSCollectionView`** | Flow, grid, and custom layouts. Item reuse. Drag-and-drop reordering. |

### AppKit — When to Avoid

- **Simple CRUD apps**: AppKit requires 200+ lines for a settings window that SwiftUI does in 30.
- **Rapid prototyping**: SwiftUI's preview canvas (Xcode Previews) is 10x faster than build-and-run for AppKit iteration.
- **New developers on the team**: SwiftUI's learning curve is gentler. AppKit requires understanding delegates, datasources, responder chain, run loop, cell reuse, Auto Layout, and `NSViewController` lifecycle.

---

## Catalyst — The iPad-to-Mac Bridge

### Strengths
| Aspect | Detail |
|---|---|
| **Code sharing** | 80-90% of iPad code compiles for Mac. `UIDocument` maps to `NSDocument`. |
| **Mac idiom** | `UIScene` adapts: `UIMacIdiom` provides native menu bar, toolbar, and Touch Bar. |
| **SwiftUI in Catalyst** | iPad SwiftUI code runs unmodified on Mac via Catalyst. Add `commands` modifier for menu bar. |
| **Plugin support** | AppKit bundle plugins can extend Catalyst apps for Mac-specific features. |

### Limitations
| Limitation | Detail |
|---|---|
| **No Menu Bar apps** | Catalyst apps must be regular windowed apps. `NSStatusBar` is unavailable. |
| **Sandbox required** | Catalyst apps distributed through the App Store must be sandboxed. |
| **UIKit baggage** | `UINavigationController`, `UITabBarController` feel foreign on Mac. Users expect sidebar navigation. |
| **No `NSDocument`** | Use `UIDocument`. Works but lacks macOS-specific features like proxy icon and vers |
| **Mac-specific APIs unavailable** | `NSWorkspace`, `NSPasteboard` (fully), `CGEvent`, `IOKit`, `NSXPCConnection` are inaccessible. |
| **Scaled rendering** | Catalyst renders at 77% scale by default. Can disable for pixel-perfect rendering at the cost of element sizes feeling slightly off. |

### When to Use Catalyst
- The primary platform is iPad, and Mac is an additional target
- The app doesn't need macOS-only features (menu bar app, system extensions, XPC)
- The team has deep UIKit expertise and no AppKit/SwiftUI experience
- Time-to-market for a Mac version is the priority over Mac-native feel

### When NOT to Use Catalyst
- The app's primary platform is Mac
- You need menu bar integration, system services, or drag-and-drop that feels native
- Users will compare your app to native Mac apps (pro tools, creative software)
- You need Metal rendering inside views (Catalyst's `MTKView` has limitations)

---

## The Bridging Pattern: SwiftUI + AppKit Together

The most common macOS architecture in 2026: **SwiftUI as the shell, AppKit for power features.**

### `NSViewRepresentable` — Wrapping AppKit Views in SwiftUI

```swift
import SwiftUI
import AppKit

struct CustomTableView: NSViewRepresentable {
    @Binding var data: [RowData]
    var onSelect: (RowData) -> Void

    func makeNSView(context: Context) -> NSScrollView {
        let scrollView = NSScrollView()
        let tableView = NSTableView()
        tableView.delegate = context.coordinator
        tableView.dataSource = context.coordinator
        tableView.addTableColumn(NSTableColumn(identifier: NSUserInterfaceItemIdentifier("main")))
        scrollView.documentView = tableView
        return scrollView
    }

    func updateNSView(_ nsView: NSScrollView, context: Context) {
        guard let tableView = nsView.documentView as? NSTableView else { return }
        tableView.reloadData()
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(data: data, onSelect: onSelect)
    }

    class Coordinator: NSObject, NSTableViewDelegate, NSTableViewDataSource {
        var data: [RowData]
        var onSelect: (RowData) -> Void

        init(data: [RowData], onSelect: @escaping (RowData) -> Void) {
            self.data = data
            self.onSelect = onSelect
        }

        func numberOfRows(in tableView: NSTableView) -> Int {
            data.count
        }

        func tableView(_ tableView: NSTableView, viewFor tableColumn: NSTableColumn?, row: Int) -> NSView? {
            let view = tableView.makeView(withIdentifier: NSUserInterfaceItemIdentifier("cell"), owner: nil) as? NSTableCellView
                ?? NSTableCellView()
            view.textField?.stringValue = data[row].title
            return view
        }

        func tableViewSelectionDidChange(_ notification: Notification) {
            guard let tableView = notification.object as? NSTableView,
                  tableView.selectedRow >= 0 else { return }
            onSelect(data[tableView.selectedRow])
        }
    }
}
```

### `NSViewControllerRepresentable` — Hosting AppKit View Controllers

```swift
import SwiftUI
import AppKit

struct AppKitSettingsPane: NSViewControllerRepresentable {
    typealias NSViewControllerType = SettingsViewController

    func makeNSViewController(context: Context) -> SettingsViewController {
        SettingsViewController()
    }

    func updateNSViewController(_ nsViewController: SettingsViewController, context: Context) {
        // Push data updates
    }
}
```

---

## Decision Matrix

| Scenario | SwiftUI | AppKit | Catalyst | Recommendation |
|---|---|---|---|---|
| New macOS-only app, standard UI | ✅ Best | ⚠️ Overkill | ❌ Wrong tool | **SwiftUI** |
| New macOS-only app, custom drawing/Metal | ⚠️ Limited | ✅ Best | ❌ Broken | **AppKit** or SwiftUI + Metal bridge |
| Existing iPad app → Mac port | ⚠️ Rewrite | ❌ Rewrite | ✅ Best | **Catalyst** |
| iPad + Mac from scratch | ✅ Shared models | ❌ Two codebases | ⚠️ Limited | **SwiftUI** with platform `#if os(macOS)` |
| Menu bar / status bar app | ✅ `MenuBarExtra` | ✅ `NSStatusBar` | ❌ Unavailable | **SwiftUI** (macOS 13+), **AppKit** (macOS 12-) |
| Document-based app with complex editing | ⚠️ Growing | ✅ Mature | ⚠️ `UIDocument` | **AppKit** or SwiftUI `DocumentGroup` |
| Video/audio professional tool | ⚠️ Performance | ✅ Metal+AVFoundation | ❌ Performance | **AppKit** with Metal views |
| Internal enterprise tool (simple forms) | ✅ Fast | ⚠️ Slow | ❌ iPad-not-Mac | **SwiftUI** |
| Accessibility-first app | ✅ Growing | ✅ Best | ⚠️ UIKit a11y | **AppKit** (most mature a11y API) |
