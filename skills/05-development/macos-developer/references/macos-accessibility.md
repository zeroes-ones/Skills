# macOS Accessibility — VoiceOver, Keyboard, and Inclusive Design

<!-- STANDARD: 3min -- WCAG 2.2 and macOS accessibility compliance -->

## The macOS Accessibility Stack

macOS has the most mature accessibility architecture of any desktop OS. The Accessibility API (`NSAccessibility`) has been refined over 20 years. Every standard AppKit control (NSButton, NSTextField, NSTableView, NSSlider) is accessible by default. Custom views are where accessibility breaks down.

| Component | What It Provides |
|---|---|
| **VoiceOver** | Screen reader: ⌘F5 to toggle. Reads UI hierarchy, labels, values, and changes. |
| **Full Keyboard Access** | Navigate ALL controls via Tab/Shift-Tab. Space to activate, Escape to dismiss. System Settings → Accessibility → Keyboard. |
| **Reduce Motion** | Disables animations. `NSWorkspace.shared.accessibilityDisplayShouldReduceMotion` |
| **Increase Contrast** | High-contrast rendering. `NSWorkspace.shared.accessibilityDisplayShouldIncreaseContrast` |
| **Reduce Transparency** | Disables vibrancy/blur. `NSWorkspace.shared.accessibilityDisplayShouldReduceTransparency` |
| **Voice Control** | Voice commands to control the UI. No special implementation needed — uses accessibility hierarchy. |
| **Switch Control** | Adaptive switch hardware. Traverses accessibility hierarchy sequentially. |

---

## Making Custom Views Accessible

### The Four Required Overrides

Every custom `NSView` subclass that handles mouse events or displays information MUST override these four methods:

```swift
import AppKit

final class CustomControl: NSView {
    // 1. Tell the accessibility system this view is an interactive element
    override func isAccessibilityElement() -> Bool {
        return true
    }

    // 2. Tell the system what ROLE this element plays
    override func accessibilityRole() -> NSAccessibility.Role? {
        return .button  // or .slider, .checkBox, .textField, .image, etc.
    }

    // 3. Provide a human-readable label
    override func accessibilityLabel() -> String? {
        return "Play"  // VoiceOver reads this
    }

    // 4. (Optional but important) Provide the current value
    override func accessibilityValue() -> Any? {
        return nil  // For buttons; for sliders, return the percentage
    }
}
```

### Common NSAccessibility.Role Values

| Role | When to Use |
|---|---|
| `.button` | Clickable elements that perform an action |
| `.checkBox` | Toggleable on/off elements |
| `.radioButton` | Mutually exclusive selection |
| `.slider` | Continuous value adjustment |
| `.textField` | Editable text |
| `.staticText` | Read-only text display |
| `.image` | Decorative or informational images |
| `.table` | Grid/table data |
| `.outline` | Hierarchical tree data |
| `.popUpButton` | Dropdown menu |
| `.group` | Logical grouping of related controls |
| `.window` | Top-level windows |
| `.toolbar` | Toolbar items |
| `.menuBar` | The menu bar |

---

## Keyboard Accessibility

### Make Every Control Keyboard-Reachable

```swift
// In custom NSView subclass:
override var acceptsFirstResponder: Bool { true }

override func becomeFirstResponder() -> Bool {
    needsDisplay = true  // Show focus ring
    return super.becomeFirstResponder()
}

override func resignFirstResponder() -> Bool {
    needsDisplay = true  // Hide focus ring
    return super.resignFirstResponder()
}

override func keyDown(with event: NSEvent) {
    switch event.keyCode {
    case 49: // Space
        performAction()
    case 36: // Return
        performAction()
    default:
        super.keyDown(with: event)
    }
}

// Draw focus ring when first responder
override func drawFocusRingMask() {
    bounds.fill()
}

override var focusRingMaskBounds: NSRect {
    return bounds
}
```

### Full Keyboard Access — System-Wide

When Full Keyboard Access is enabled in System Settings, the user can Tab between ALL controls, including those that are normally mouse-only. Your toolbar buttons, custom controls, and status bar items MUST be in the tab loop.

```swift
// Toolbar items need to be in the tab loop
toolbarItem.isNavigable = true  // macOS 14+

// Explicitly set the next/previous responder
yourView.nextKeyView = nextControl
```

---

## Responding to System Accessibility Settings

```swift
import AppKit

final class AccessibilityObserver {
    init() {
        // Reduce Motion
        NotificationCenter.default.addObserver(
            forName: NSWorkspace.accessibilityDisplayOptionsDidChangeNotification,
            object: nil,
            queue: .main
        ) { _ in
            let reduceMotion = NSWorkspace.shared
                .accessibilityDisplayShouldReduceMotion
            // Disable or simplify animations
        }

        // Increase Contrast
        let increaseContrast = NSWorkspace.shared
            .accessibilityDisplayShouldIncreaseContrast
        if increaseContrast {
            // Use high-contrast color scheme
        }
    }
}

// SwiftUI equivalent
struct ContentView: View {
    @Environment(\.accessibilityReduceMotion) var reduceMotion
    @Environment(\.accessibilityReduceTransparency) var reduceTransparency
    @Environment(\.accessibilityDifferentiateWithoutColor) var differentiateWithoutColor

    var body: some View {
        VStack {
            if reduceMotion {
                Text("Static") // No animation
            } else {
                AnimatedContent()
            }
        }
    }
}
```

---

## Accessibility Inspector

### Using the Inspector

1. Open Xcode → Open Developer Tool → Accessibility Inspector
2. Select your app as the target
3. Navigate the accessibility hierarchy tree
4. Inspect each element's label, role, value, and actions

### What to Look For
- [ ] Every interactive element has a `label`
- [ ] Every interactive element has a `role`
- [ ] Labels are descriptive: "Delete 'Vacation Photo'" not just "Delete"
- [ ] Values change is announced: sliders, progress bars, status indicators
- [ ] Focus order follows visual layout (left-to-right, top-to-bottom)
- [ ] No "empty group" elements (groups with no accessible children)
- [ ] Images have descriptions (or are marked as decorative via `accessibilityRole(.image)` + empty label for purely decorative)

---

## Announcing State Changes

When a state change happens that isn't triggered by the user's direct interaction (e.g., a download completes, an error occurs), announce it to VoiceOver:

```swift
// AppKit
NSAccessibility.post(
    element: NSApp.mainWindow!,
    notification: .announcementRequested,
    userInfo: [
        .announcement: "Download complete: 3 files saved.",
        .priority: NSAccessibilityPriority.high.rawValue
    ]
)

// SwiftUI
AccessibilityNotification.Announcement("Download complete").post()
```

---

## Accessibility for Custom Controls — Full Example

```swift
final class RatingControl: NSView {
    private var rating: Int = 0 {
        didSet {
            needsDisplay = true
            // Announce value change to VoiceOver
            NSAccessibility.post(
                element: self,
                notification: .valueChanged
            )
        }
    }

    // MARK: - NSAccessibility

    override func isAccessibilityElement() -> Bool { true }

    override func accessibilityRole() -> NSAccessibility.Role? { .slider }

    override func accessibilityLabel() -> String? { "Rating" }

    override func accessibilityValue() -> Any? {
        return "\(rating) out of 5 stars"
    }

    override func accessibilityMinValue() -> Any? { 0 }

    override func accessibilityMaxValue() -> Any? { 5 }

    override func accessibilityPerformIncrement() -> Bool {
        guard rating < 5 else { return false }
        rating += 1
        return true
    }

    override func accessibilityPerformDecrement() -> Bool {
        guard rating > 0 else { return false }
        rating -= 1
        return true
    }

    override func accessibilityHelp() -> String? {
        "Adjust the rating from 0 to 5 stars"
    }
}
```

---

## Common Accessibility Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| `<div onClick>` equivalent: `NSView` with `mouseDown` override, no accessibility overrides | VoiceOver can't see it. Keyboard users can't reach it. | Override all four `accessibility*` methods |
| Custom drawn text instead of `NSTextField` | VoiceOver can't read drawn pixels. Keyboard selection doesn't work. | Use `NSTextField` or implement `NSAccessibilityStaticText` protocol fully |
| Color-only state indicators (red/green dot without label) | Colorblind users and VoiceOver users can't distinguish. | Add `accessibilityLabel`: "Status: Offline" or use shape + color |
| `accessibilityLabel = ""` on interactive elements | VoiceOver skips the element entirely. | Always provide a meaningful label |
| Image-based buttons without labels | VoiceOver reads "image" with no context. | Set `accessibilityLabel` on the `NSImageView` or `NSButton.imagePosition` |
| Custom focus ring drawing that doesn't respond to `accessibilityDisplayShouldIncreaseContrast` | Low-vision users can't see the focus ring. | Respect the system contrast setting |

---

## Testing Accessibility

### Manual Testing
1. **Toggle VoiceOver (⌘F5)**. Navigate your entire app without looking at the screen.
2. **Enable Full Keyboard Access**. Navigate every window using only Tab, Space, Return, Escape.
3. **Enable Reduce Motion**. Verify all animations disable.
4. **Enable Increase Contrast**. Verify all UI elements remain distinct.
5. **Enable Voice Control**. Speak commands to control your app.

### Automated Testing
```swift
func testAccessibilityLabels() {
    let app = XCUIApplication()
    app.launch()

    // Every button must have a label
    for button in app.buttons.allElementsBoundByIndex {
        XCTAssertFalse(
            button.label.isEmpty,
            "Button without accessibility label: \(button.identifier)"
        )
    }
}
```
