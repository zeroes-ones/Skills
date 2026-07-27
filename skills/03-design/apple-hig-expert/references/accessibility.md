# Accessibility on Apple Platforms

## Overview

Apple's accessibility infrastructure is baked into the HIG. Every platform provides:
- **VoiceOver**: Screen reader with gesture-based navigation
- **Dynamic Type**: User-controlled text size from xSmall to xxxLarge (+ Accessibility sizes)
- **Reduce Motion**: Disable animations and parallax effects
- **Reduce Transparency**: Replace translucent surfaces with opaque alternatives
- **Increase Contrast**: Higher contrast for text and UI elements
- **Switch Control**: Sequential item navigation for motor accessibility
- **AssistiveTouch**: Custom gestures for physical interaction constraints

## VoiceOver Requirements

### Every Interactive Element Needs a Label
```swift
Button(action: { /* action */ }) {
    Image(systemName: "heart.fill")
}
.accessibilityLabel("Add to favorites")
```

### Group Related Elements
```swift
VStack {
    Text("Sandeep Kumar")
    Text("sandeep@example.com")
}
.accessibilityElement(children: .combine)
.accessibilityLabel("Sandeep Kumar, sandeep@example.com")
```

### Announce Dynamic Changes
```swift
AccessibilityNotification.Announcement("Search complete. 5 results found.").post()
```

### Custom Actions for Complex Controls
```swift
.accessibilityAction(named: "Delete") { /* delete action */ }
.accessibilityAction(named: "Share") { /* share action */ }
```

### Traits
- `.isButton`, `.isHeader`, `.isLink`, `.isSelected`, `.isImage`
- `.isModal` — indicates blocking overlay
- `.updatesFrequently` — for live-updating content

## Dynamic Type

### System Text Styles (Auto-Scale)
```swift
Text("Hello").font(.body)     // Scales automatically
Text("Hello").font(.title)    // Scales automatically
Text("Hello").font(.caption)  // Scales automatically
```

### Custom Fonts with Scaling
```swift
// Relative to Dynamic Type
Text("Hello").font(.system(.body, design: .rounded))

// Custom size that scales
Text("Hello").font(.custom("MyFont", size: 17, relativeTo: .body))
```

### Minimum Scale Factor
```swift
Text("Long content that might wrap")
    .font(.headline)
    .minimumScaleFactor(0.5) // Shrink to 50% before truncating
    .lineLimit(1)
```

### Testing Dynamic Type
- **Smallest**: xSmall — verify no layout breaks from too-small elements
- **Default**: Large (default) — baseline
- **Largest**: xxxLarge — verify no text clipping, no overflow
- **Accessibility Extra Large**: AX1-AX5 — verify critical content still accessible
- Use Xcode's Environment Overrides or `.environment(\.sizeCategory, .accessibilityExtraExtraLarge)` in previews

## Reduce Motion

```swift
@Environment(\.accessibilityReduceMotion) var reduceMotion

// Animate conditionally
withAnimation(reduceMotion ? nil : .spring()) {
    // animation
}

// Or use a simplified animation
withAnimation(reduceMotion ? .none : .spring()) {
    // animation
}
```

### Motion Guidelines
- No autoplaying video backgrounds when Reduce Motion is on
- Parallax effects must be disabled
- Page transitions should become simple fades
- Scroll animations should become instant

## Reduce Transparency

```swift
@Environment(\.accessibilityReduceTransparency) var reduceTransparency

var background: some View {
    if reduceTransparency {
        Color(.systemBackground) // Opaque fallback
    } else {
        Color(.systemBackground).glassEffect(.regular) // Glass when allowed
    }
}
```

### Transparency Guidelines
- All glass/modally-blurred surfaces must have opaque fallback
- Blur radius should adjust: heavier blur (more opaque) is better than removing glass entirely
- Verify all text contrast on both glass and opaque surfaces

## Increase Contrast

```swift
@Environment(\.accessibilityEnabled) var accessibilityEnabled
@Environment(\.legibilityWeight) var legibilityWeight

var strokeWidth: CGFloat {
    legibilityWeight == .bold ? 2.0 : 1.0
}
```

### Contrast Guidelines
- Increase border widths on outlines and separators
- Use heavier font weights (`.bold` vs `.regular`) when Increase Contrast is on
- Secondary text may need to be promoted to primary contrast

## Platform-Specific Accessibility

### iOS
- **VoiceOver Rotor**: Users navigate by headings, links, landmarks. Use `.accessibilityAddTraits(.isHeader)`.
- **Reachability**: Double-tap home indicator to bring top content down. Don't put critical actions only at top.
- **Back Tap**: System-level double/triple tap gesture. Don't override unintentionally.

### macOS
- **Full Keyboard Access**: Navigate entire UI by keyboard. Every control needs a keyboard equivalent where practical.
- **VoiceOver**: Uses keyboard commands (Control+Option). Test tab order.
- **Display Zoom**: Screen zoom up to 200%. Layout should not break.

### watchOS
- **VoiceOver**: Simplified rotor with fewer options. Content must be concise.
- **Zoom**: Digital Crown to zoom. Layout must not break when zoomed.
- **Font size**: Extremely limited screen. Content hierarchy is critical.

### visionOS
- **VoiceOver**: Integrated with gaze. Describes what the user is looking at.
- **Pointer Control**: Alternative to gaze for motor accessibility. Dwell control + head pointer.
- **Audio Descriptions**: For spatial experiences, describe spatial arrangements.
