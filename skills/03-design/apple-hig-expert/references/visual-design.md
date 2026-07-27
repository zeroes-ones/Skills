# Visual Design: Semantic Colors & Liquid Glass

## Semantic Color System

Apple's semantic color system adapts automatically to:
- **Appearance**: Light Mode, Dark Mode
- **Accessibility**: Increase Contrast, Reduce Transparency
- **Context**: Platform (iOS vs macOS vs watchOS vs visionOS)

### Primary Semantic Colors

| Semantic Color | Usage | Light Value | Dark Value |
|---------------|-------|------------|------------|
| `.label` | Primary text | `#000000` (100% black) | `#FFFFFF` (100% white) |
| `.secondaryLabel` | Secondary text, captions | `#3C3C4399` (60% black) | `#EBEBF599` (60% white) |
| `.tertiaryLabel` | Disabled/placeholder text | `#3C3C432E` (18% black) | `#EBEBF540` (25% white) |
| `.quaternaryLabel` | Watermark text | `#3C3C4318` (10% black) | `#EBEBF529` (16% white) |
| `.systemBackground` | Root view background | `#FFFFFF` (white) | `#000000` (black) |
| `.secondarySystemBackground` | Scrollable content area | `#F2F2F7` (light gray) | `#1C1C1E` (dark gray) |
| `.tertiarySystemBackground` | Floating grouping | `#FFFFFF` (white) | `#2C2C2E` (dark gray) |
| `.systemGroupedBackground` | Grouped table background | `#F2F2F7` | `#000000` |

### Fill Colors (for layers on backgrounds)

| Fill | Usage | Light Opacity | Dark Opacity |
|------|-------|--------------|-------------|
| `.systemFill` | Standard overlay | 20% over gray | 24% over gray |
| `.secondarySystemFill` | Secondary overlay | 16% over gray | 18% over gray |
| `.tertiarySystemFill` | Tertiary overlay | 12% over gray | 12% over gray |
| `.quaternarySystemFill` | Subtle overlay | 8% over gray | 8% over gray |

### Separator Colors

| Separator | Usage |
|-----------|-------|
| `.separator` | Standard separators |
| `.opaqueSeparator` | Non-transparent separators |

### Tint & Accent

- **AccentColor**: App-defined accent. Applied automatically to system controls.
- **Tint**: Override accent for specific views. Use `.tint()` modifier.

### Rule: Never Hardcode
```swift
// ❌ Wrong
Text("Hello").foregroundColor(Color(hex: "#3C3C43"))

// ✅ Correct
Text("Hello").foregroundColor(.secondaryLabel)
```

---

## Liquid Glass Design Language

Announced WWDC25 (June 2025), shipped with iOS 26 / iPadOS 26 / macOS Tahoe / watchOS 26 / tvOS 26 / visionOS 26 (September 2025).

### Core Concept
Translucent material hierarchy that creates depth through progressive translucency. Glass surfaces let light and background content through in controlled amounts, creating a sense of physical layering.

### Material Hierarchy

| Level | Translucency | Usage |
|-------|-------------|-------|
| **Primary Glass** | Most translucent (~85% background visible) | Modal sheets, floating panels, overlaid content |
| **Secondary Glass** | Medium translucent (~60% background visible) | Sidebars, tab bars, toolbars |
| **Tertiary Glass** | Least translucent (~40% background visible) | Navigation bars, headers, status bars |
| **Opaque Surface** | 0% translucency | Content areas, scroll views, text-heavy regions |

### SwiftUI Usage
```swift
// Apply Liquid Glass effect
View()
    .glassEffect(.regular)

// Material variants
.glassEffect(.thin)       // More translucent
.glassEffect(.regular)    // Default
.glassEffect(.thick)      // Less translucent
.glassEffect(.ultraThick) // Nearly opaque
```

### Accessibility: Reduce Transparency
```swift
@Environment(\.accessibilityReduceTransparency) var reduceTransparency

var body: some View {
    if reduceTransparency {
        content
            .background(.regularMaterial) // Fallback to standard material
    } else {
        content
            .glassEffect(.regular) // Liquid Glass
    }
}
```

### Contrast Considerations
- Text over glass must pass 4.5:1 contrast against the **busiest** underlying region
- Test with: photo backgrounds, gradients, scrolling content behind glass
- Dark text on light glass: use `.label` (highest contrast semantic)
- Light text on dark glass: use `.label` and verify on all background conditions
- **Always test with Reduce Transparency ON** — the opaque fallback must also pass contrast

### Anti-Patterns
| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Glass on glass on glass | Depth becomes noise, not signal | Max 2 glass layers deep. Third layer must be opaque. |
| Text directly on glass over photos | Text becomes unreadable where photo is busy | Add a subtle glass tint behind text, or place text on opaque surface inset within glass |
| Glass everywhere | Every element looks like a window — user loses figure/ground | Reserve glass for containers (sheets, sidebars, toolbars). Content goes on opaque surfaces. |

### Platform Differences
- **iOS/iPadOS**: Glass is the default surface treatment. Familiar since iOS 7 blur effects.
- **macOS Tahoe**: Glass replaces traditional title bars and sidebars. Window chrome becomes translucent.
- **watchOS 26**: Subtle glass on notifications and overlays. Content remains maximally readable.
- **visionOS**: Glass already foundational (launched with glass materials). iOS 26 glass aligns visionOS and iOS visual language.
