# macOS Menu Bar Apps — Architecture & Patterns

<!-- STANDARD: 3min -- build apps that live in the menu bar -->

## The Two Eras of Menu Bar Development

| Era | API | Minimum macOS | Approach |
|---|---|---|---|
| **Classic (pre-2022)** | `NSStatusBar` + `NSStatusItem` + `NSMenu` | macOS 10.0+ | Create `NSStatusItem`, attach `NSMenu` or custom `NSView` |
| **Modern (2022+)** | SwiftUI `MenuBarExtra` | macOS 13+ | Declarative: `MenuBarExtra("Title", systemImage: "icon") { ... }` |

**Recommendation**: Use `MenuBarExtra` for macOS 13+ targets. Fall back to `NSStatusBar` for macOS 12 support.

---

## SwiftUI `MenuBarExtra` (macOS 13+)

### Minimal Menu Bar App

```swift
import SwiftUI

@main
struct MyMenuBarApp: App {
    var body: some Scene {
        MenuBarExtra("MyApp", systemImage: "hammer") {
            VStack {
                Text("Hello from the menu bar!")
                Divider()
                Button("Do Something") {
                    // Action
                }
                .keyboardShortcut("d")
                Divider()
                Button("Quit") {
                    NSApplication.shared.terminate(nil)
                }
                .keyboardShortcut("q")
            }
            .padding()
        }
        .menuBarExtraStyle(.window) // .menu (default), .window
    }
}
```

### MenuBarExtra Styles

| Style | Behavior |
|---|---|
| `.menu` (default) | Standard dropdown menu. Content presented as `NSMenuItem`-like items. |
| `.window` | Content presented in a floating panel/window. Behaves like a popover. |

### Hiding the Dock Icon

```swift
import SwiftUI

@main
struct MyMenuBarApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    var body: some Scene {
        MenuBarExtra("MyApp", systemImage: "hammer") {
            ContentView()
        }
    }
}

final class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        // Hide from Dock and Command-Tab switcher
        NSApp.setActivationPolicy(.accessory)
    }
}
```

### Appearing Only in Menu Bar

In `Info.plist`, add `Application is agent (UIElement)` → `YES` (or `LSUIElement = YES`). This hides the Dock icon and makes the app menu bar-only.

---

## AppKit `NSStatusBar` (macOS 12 and earlier)

### Full Example

```swift
import AppKit

final class StatusBarController: NSObject {
    private var statusItem: NSStatusItem!
    private var menu: NSMenu!

    override init() {
        super.init()
        setupStatusItem()
    }

    private func setupStatusItem() {
        statusItem = NSStatusBar.system.statusItem(
            withLength: NSStatusItem.variableLength
        )

        if let button = statusItem.button {
            button.image = NSImage(
                systemSymbolName: "hammer",
                accessibilityDescription: "MyApp"
            )
            button.image?.isTemplate = true // Enables Dark Mode auto-invert
            button.action = #selector(toggleMenu)
            button.target = self
        }

        setupMenu()
    }

    private func setupMenu() {
        menu = NSMenu()

        let statusItem = NSMenuItem(
            title: "Status: Running",
            action: nil,
            keyEquivalent: ""
        )
        statusItem.isEnabled = false
        menu.addItem(statusItem)
        menu.addItem(.separator())

        menu.addItem(NSMenuItem(
            title: "Preferences...",
            action: #selector(openPreferences),
            keyEquivalent: ","
        ))

        menu.addItem(.separator())

        menu.addItem(NSMenuItem(
            title: "Quit",
            action: #selector(NSApplication.terminate(_:)),
            keyEquivalent: "q"
        ))
    }

    @objc private func toggleMenu() {
        statusItem.button?.isHighlighted = true
        // Show menu at status item position
        if let button = statusItem.button {
            menu.popUp(
                positioning: nil,
                at: NSPoint(x: 0, y: button.bounds.height),
                in: button
            )
        }
    }

    @objc private func openPreferences() {
        // Open preferences window
        NSApp.setActivationPolicy(.regular)
        NSApp.activate(ignoringOtherApps: true)
        // Show settings window...
    }
}
```

### Custom View in Status Item

```swift
let customView = NSHostingView(rootView: StatusBarCustomView())
customView.frame = NSRect(x: 0, y: 0, width: 100, height: 22)

if let button = statusItem.button {
    button.addSubview(customView)
    button.frame = customView.frame
}
```

---

## Menu Bar Icon Guidelines

| Rule | Detail |
|---|---|
| **PDF template images** | Use PDF vector assets with "Template" rendering mode. macOS automatically inverts for Dark Mode and menu bar highlight. |
| **`isTemplate = true`** | Critical for monochrome icons. Without this, your icon looks wrong in Dark Mode. |
| **22×22 points recommended** | The menu bar is 24pt tall. Icons should be 18-22pt tall. |
| **Multiple sizes in asset catalog** | Provide @1x (22px) and @2x (44px) for Retina displays. |
| **Avoid full-color icons** | Unless your app genuinely needs a color indicator, use template images that integrate with the system appearance. |
| **No animation in menu bar** | Animating the status item icon drains battery and distracts users. Disable timer-driven updates when the menu is open. |

---

## Common Issues

### Icon Not Visible / Wrong Color in Dark Mode
```swift
button.image?.isTemplate = true  // This MUST be set
```

### Menu Doesn't Respond to Clicks
The app's activation policy is `.prohibited`. Change to `.accessory`:
```swift
NSApp.setActivationPolicy(.accessory)
```

### Window Opens Behind Other Windows
```swift
NSApp.activate(ignoringOtherApps: true)
window.makeKeyAndOrderFront(nil)
```

### App Quits When Window Closes
By default, menu bar apps with `LSUIElement = YES` quit when the last window closes. To prevent this:
```swift
// In AppDelegate
func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
    return false
}
```
