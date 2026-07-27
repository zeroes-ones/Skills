# SwiftUI HIG Patterns

Quick-reference for implementing HIG-compliant SwiftUI code.

## Semantic Colors in SwiftUI

```swift
// Text colors
Text("Primary").foregroundColor(.primary)
Text("Secondary").foregroundColor(.secondary)
// .primary and .secondary map to .label and .secondaryLabel

// Background colors
Color(.systemBackground)
Color(.secondarySystemBackground)
Color(.systemGroupedBackground)

// Fill colors for overlays
Color(.systemFill)
Color(.secondarySystemFill)
```

## Touch Target Compliance

```swift
// ❌ Wrong: tight frame on small icon
Image(systemName: "xmark")
    .frame(width: 16, height: 16)
    .onTapGesture { /* close */ }

// ✅ Correct: expand hit target with contentShape
Image(systemName: "xmark")
    .frame(width: 16, height: 16)
    .contentShape(Rectangle().size(width: 44, height: 44))
    .onTapGesture { /* close */ }

// ✅ Alternative: padding then negative padding for visual
Image(systemName: "xmark")
    .frame(width: 16, height: 16)
    .padding(14) // 16 + 28 = 44
    .contentShape(Rectangle())
    .onTapGesture { /* close */ }
```

## Platform-Adaptive Design

```swift
// iOS Tab Bar
TabView {
    ContentView().tabItem { Label("Home", systemImage: "house") }
    SettingsView().tabItem { Label("Settings", systemImage: "gear") }
}

// macOS Sidebar
NavigationSplitView {
    List(selection: $selection) {
        Label("Home", systemImage: "house")
        Label("Settings", systemImage: "gear")
    }
} detail: {
    DetailView(selection: selection)
}

// Platform-conditional navigation
#if os(iOS)
TabView { /* tab bar */ }
#elseif os(macOS)
NavigationSplitView { /* sidebar */ }
#endif
```

## Dynamic Type Implementation

```swift
// System fonts auto-scale
Text("Hello").font(.body)    // ✅ Scales automatically
Text("Hello").font(.title)   // ✅ Scales automatically

// Fixed-size fonts DO NOT scale — use only for icons
Image(systemName: "star").font(.system(size: 24)) // OK for SF Symbols

// Scaled metrics for padding
@ScaledMetric var padding = 16.0
Text("Hello").padding(padding)

// Minimum scale factor to prevent clipping
Text("Very long text")
    .font(.headline)
    .minimumScaleFactor(0.7)
    .lineLimit(2)
```

## Liquid Glass Implementation

```swift
// Basic glass effect
content
    .glassEffect(.regular)

// Material variants
content.glassEffect(.thin)       // Most transparent
content.glassEffect(.regular)    // Default
content.glassEffect(.thick)      // Less transparent
content.glassEffect(.ultraThick) // Nearly opaque

// With Reduce Transparency fallback
@Environment(\.accessibilityReduceTransparency) var reduceTransparency

@ViewBuilder
func glassBackground<Content: View>(_ content: Content) -> some View {
    if reduceTransparency {
        content.background(.regularMaterial)
    } else {
        content.glassEffect(.regular)
    }
}
```

## Accessibility Modifiers

```swift
// Label for interactive elements
Button("Delete", systemImage: "trash") { }
    .accessibilityLabel("Delete this item")

// Combine elements
VStack {
    Text("John Doe")
    Text("john@example.com")
}
.accessibilityElement(children: .combine)

// Hide decorative elements
Image("decorative-pattern")
    .accessibilityHidden(true)

// Custom actions
.accessibilityAction(named: "Share") { /* share */ }
.accessibilityAction(named: "Delete") { /* delete */ }

// Sort priority
.accessibilitySortPriority(1) // Higher = read first

// Input labels for text fields
TextField("Email", text: $email)
    .accessibilityLabel("Email address")

// Value descriptions for progress/state
ProgressView(value: 0.7)
    .accessibilityValue("70% complete")
```

## Safe Area Handling

```swift
// Extend background through safe area (maps, images)
Color.blue
    .ignoresSafeArea()

// Respect safe area for content
ScrollView {
    VStack {
        // Content automatically respects safe area
    }
}

// Custom safe area inset
Color.blue
    .ignoresSafeArea()
    .safeAreaInset(edge: .bottom) {
        Button("Continue") { }
            .padding()
            .background(.regularMaterial)
    }
```

## Haptics

```swift
// Impact feedback
let generator = UIImpactFeedbackGenerator(style: .medium)
generator.impactOccurred()

// Selection feedback (picker changes, toggle)
let generator = UISelectionFeedbackGenerator()
generator.selectionChanged()

// Notification feedback (success, warning, error)
let generator = UINotificationFeedbackGenerator()
generator.notificationOccurred(.success)

// SwiftUI sensory feedback (iOS 17+)
Button("Save") { }
    .sensoryFeedback(.success, trigger: saveSuccess)
```

## Common Violations & Fixes

| Violation | Detection | Fix |
|-----------|-----------|-----|
| Hardcoded color | `Color(hex: "#3C3C43")` | `.foregroundColor(.secondaryLabel)` |
| Sub-44pt target | `.frame(width: 32, height: 32)` | `.contentShape(Rectangle().size(width: 44, height: 44))` |
| Missing VoiceOver label | `Image("icon").onTapGesture { }` | `.accessibilityLabel("Close")` |
| No Dynamic Type | `.font(.system(size: 14))` | `.font(.body)` or `.font(.system(.body))` |
| No reduced-motion fallback | `withAnimation(.spring())` | `withAnimation(reduceMotion ? nil : .spring())` |
| Glass without fallback | `.glassEffect(.regular)` alone | Wrap with `reduceTransparency` check |
| Tab content at screen bottom | Content near home indicator | Add safe area padding, move actions up |
