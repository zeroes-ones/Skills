# Accessibility & VoiceOver Reference

## Minimum Viable Accessibility

```swift
struct AccessibleButton: View {
    let label: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(label)
        }
        .accessibilityLabel(label)
        .accessibilityHint("Double-tap to activate")
        .accessibilityAddTraits(.isButton)
    }
}
```

## Dynamic Type Support

```swift
Text("Welcome back, \(user.name)")
    .font(.body)  // Scales with Dynamic Type automatically
    .lineLimit(nil)  // Allow wrapping; never truncate

// Custom scaling
Text("42")
    .font(.system(size: 34, weight: .bold, design: .rounded))
    .minimumScaleFactor(0.5)  // Shrink down to 50% if needed
```

## VoiceOver Rotor for Custom Views

```swift
ScrollView {
    LazyVStack {
        ForEach(products) { product in
            ProductRow(product: product)
                .accessibilityElement(children: .combine)
                .accessibilityRotor("Products") {
                    // Custom rotor entry for quick navigation
                    AccessibilityRotorEntry(product.name, id: product.id)
                }
        }
    }
}
```

## Audit Commands

```bash
# Run Accessibility Inspector from CLI
xcrun accessibility-inspector

# In Xcode: Product > Profile > Accessibility Inspector template
# Or use the Accessibility Inspector app directly
open -a "Accessibility Inspector"
```
