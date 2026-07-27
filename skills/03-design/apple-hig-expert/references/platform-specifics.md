# Platform-Specific HIG Patterns

## iOS

### Navigation Paradigms
- **Tab Bar**: 3-5 top-level destinations, always visible at screen bottom. Badge for notifications. Each tab preserves its own navigation stack.
- **Hierarchical (NavigationStack)**: Drill-down navigation with back button. Title animates into navigation bar on scroll.
- **Modal (Sheet)**: Interrupting task or focused content. Full-screen or detent-based sheets. Swipe to dismiss.

### Ergonomic Zones
- **Bottom reach zone**: Bottom 1/3 of screen — primary actions, tab bar, toolbars. Thumb-reachable.
- **Top zone**: Titles, navigation, search. Requires hand adjustment on larger phones.
- **Dynamic Island / Notch**: Never place critical interactive elements here. Extend backgrounds through safe area.

### Safe Areas
- Use `safeAreaInsets` with `ignoresSafeAreaEdges` only for background content (images, videos, maps).
- Home indicator: never overlap with interactive elements. Add padding ≥ 16pt above home indicator.

### Typography
- **Font**: SF Pro (system default)
- **Semantic styles**: `.largeTitle`, `.title`, `.title2`, `.title3`, `.headline`, `.subheadline`, `.body`, `.callout`, `.footnote`, `.caption`, `.caption2`
- **Dynamic Type**: All text styles automatically scale. Test at smallest and largest sizes.

---

## macOS

### Navigation Paradigms
- **Sidebar + Detail**: Primary navigation pattern. Sidebar with collapsible sections. Detail view updates on selection.
- **Single Window / Utility**: Simple apps (calculator, notes, smaller tools). No sidebar needed.
- **Tabbed Windows**: Multiple tabs within a window. System-provided tab bar.
- **Inspector Panels**: Right-side detail inspection. Toggleable.

### Menu Bar & Commands
- Every macOS app needs: App menu, File, Edit, View, Window, Help (minimum).
- All actions should have keyboard shortcuts where reasonable.
- Use `commands` modifier group for standard operations.

### Window Management
- **Default size**: Content-appropriate, not maximized
- **Minimum size**: Define reasonable minimums (≥ 480×270 for smallest utility)
- **Window restoration**: Restore window position and state on relaunch
- **Full screen**: Support native full-screen mode

### Typography
- **Font**: SF Pro (system default)
- **Size**: Typically 13pt for body text, 11pt for captions

---

## watchOS

### Navigation Paradigms
- **Page-based**: Swipe horizontally between pages. Each page is independent content.
- **Hierarchical**: Tap to drill in, swipe left edge to go back. For list-based content.
- **Modal sheets**: Interrupting or focused tasks. Swipe down to dismiss.

### Ergonomic Constraints
- **Screen**: Extremely limited real estate (41-49mm cases)
- **Glance-based interaction**: Average interaction < 5 seconds
- **Crown**: Use Digital Crown for scrolling, zooming, precision adjustments
- **Force Touch**: Deprecated in watchOS 7+ — use long-press or context menus instead

### Typography
- **Font**: SF Compact (designed for small screens)
- **Minimum readable size**: Never smaller than 11pt

### Key Patterns
- **Complications**: Small data displays on the watch face. Update frequently.
- **Notifications**: Short-Look (summary) → Long-Look (detail) on wrist raise.
- **Now Playing / Workout**: Full-screen immersive experiences.

---

## visionOS

### Navigation Paradigms
- **Gaze + Pinch**: Primary interaction. Look at element, pinch fingers to select.
- **Ornaments**: UI elements that float near the content they relate to. Don't obscure.
- **Tab View**: Ornament-based tab bar, typically at bottom of window.
- **Volumes**: 3D content in bounded space. Use `.volumetric` window style.

### Spatial Design Principles
- **Content is the UI**: Minimize chrome. Let content occupy the space.
- **Depth and scale**: Objects have physical presence. Respect scale — don't make tiny buttons.
- **Lighting**: UI adapts to environment lighting. Avoid pure white backgrounds in dark rooms.

### Typography
- **Font**: SF Pro
- **Size**: Larger than iOS — user is further from the "screen"
- **Vibrancy**: System automatically applies vibrancy for readability in passthrough

### Key Patterns
- **Window management**: Free-form window placement. User resizes and repositions.
- **Immersive spaces**: Full-environment experiences. Transition with user consent.
- **SharePlay**: Spatial Personas for shared experiences.
