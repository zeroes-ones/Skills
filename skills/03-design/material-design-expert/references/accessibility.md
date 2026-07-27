# Material Design Accessibility Patterns
<!-- YAML-style: title: Material Design Accessibility Patterns, date: 2026-07-26 -->

## TalkBack (Screen Reader)

### contentDescription: The #1 Rule
Every meaningful interactive or informational element must have a `contentDescription`:
- **Images, icons, buttons**: `contentDescription = "Add to favorites"` (describe the action, not the visual)
- **Decorative elements**: `contentDescription = null` or `importantForAccessibility = "no"`
- **Data displays**: Describe the data, not the chart type: `"Revenue: $42.8K, up 12% from last month"` not `"Bar chart showing revenue"`

```kotlin
// Compose
Icon(
    imageVector = Icons.Default.Favorite,
    contentDescription = "Add to favorites"
)
Divider() // Automatically ignored by TalkBack

// Views
imageView.contentDescription = "Profile photo of Sandeep Kumar"
imageView.importantForAccessibility = IMPORTANT_FOR_ACCESSIBILITY_NO // decorative
```

### Heading Hierarchy
Material Design requires semantic heading levels for TalkBack navigation. Users can navigate by heading.

```kotlin
// Compose
Text(
    text = "Account Settings",
    modifier = Modifier.semantics { heading() },
    style = MaterialTheme.typography.headlineSmall
)
```

**Rules:**
- Exactly one level-1 heading per screen (the screen title).
- Levels must not skip (no h1 → h3 without h2).
- Use typography styles that map to heading levels: `headlineLarge` → h1, `headlineMedium` → h2, `headlineSmall` → h3.

### Live Regions for Dynamic Content
Announce content changes without moving accessibility focus:

```kotlin
// Compose — live region
var message by remember { mutableStateOf("Loading...") }
Text(
    text = message,
    modifier = Modifier.semantics { liveRegion = LiveRegionMode.Assertive }
)
// When message changes, TalkBack automatically announces it
```

**Modes:**
| Mode | Behavior |
|------|----------|
| `LiveRegionMode.Polite` | Announce after current speech finishes. For non-critical updates. |
| `LiveRegionMode.Assertive` | Interrupt current speech immediately. For errors, completion, critical changes. |

### Custom Accessibility Actions
For complex gestures that TalkBack users can't perform (swipe, drag-and-drop, pinch):

```kotlin
Box(
    modifier = Modifier.semantics {
        customActions = listOf(
            CustomAccessibilityAction("Delete") { onDelete(); true },
            CustomAccessibilityAction("Archive") { onArchive(); true }
        )
    }
)
```

### Grouping Composite Components
Combine child elements into a single accessibility node for cards, list items, etc.

```kotlin
// Compose
Card(
    modifier = Modifier.semantics(mergeDescendants = true) {
        contentDescription = "Message from Alice: See you at 3pm"
    }
) {
    Column {
        Text("Alice")       // Not individually read
        Text("See you at 3pm") // Not individually read
        Icon(Icons.Default.Star, null) // Not individually read
    }
}
```

---

## Touch Target Minimums

### The 48dp Rule
**48dp × 48dp minimum** — Material Design requirement, exceeds WCAG 2.5.5's 44px target.

| Element | Minimum Size | Implementation |
|---------|-------------|----------------|
| Icon button | 48×48dp | `IconButton` handles this automatically |
| Text button | 48dp height | `Button` defaults to 48dp minHeight |
| List item | 48dp height | `ListItem` handles this |
| FAB | 56×56dp (standard), 48×48dp (mini) | Built-in |
| Chip | 32dp height, but touch area padded to 48dp | `AssistChip`, `FilterChip` handle this |
| Checkbox/Radio/Switch | 48×48dp | `Checkbox` + `.size(48.dp)` |
| Slider thumb | 20dp visually, but 48dp touch target | `Slider` handles this automatically |

```kotlin
// When custom clickable — force minimum 48dp
Box(
    modifier = Modifier
        .size(48.dp) // Minimum
        .clickable { onClick() }
)
```

### Expanding Touch Targets
For icons inside containers that are smaller than 48dp, use padding to expand the touch area:

```kotlin
Icon(
    imageVector = Icons.Default.Close,
    contentDescription = "Close",
    modifier = Modifier
        .size(24.dp) // Visual size
        .padding(12.dp) // Expands touch area to 48dp
        .clickable { onClose() }
)
```

---

## Switch Access (Motor Accessibility)

Switch Access allows users with motor impairments to navigate by scanning items sequentially.

### Requirements

| Rule | Why |
|------|-----|
| All interactive elements in logical order | Switch Access follows the accessibility tree. Out-of-order elements cause confusion. |
| Group related actions | Combine 3 separate buttons into a single group with custom actions. Speak the group name. |
| No time-dependent interactions | No auto-dismissing dialogs, timed modals, countdown-triggered actions (without accessible alternatives). |
| No drag-only gestures | Every drag operation must have a button-based alternative. |

### Tab Order
```kotlin
// Ensure logical traversal order
Column {
    Button(modifier = Modifier.semantics { isTraversalGroup = true }) { Text("Primary") }
    OutlinedButton(modifier = Modifier.semantics { isTraversalGroup = true }) { Text("Secondary") }
    TextButton(modifier = Modifier.semantics { isTraversalGroup = true }) { Text("Tertiary") }
}
// Traversal: Primary → Secondary → Tertiary (matches visual order)
```

---

## Voice Access

Voice Access assigns numeric labels to interactive elements. Users speak the number to activate it.

### Label Assignment
- Automatically generated for all `clickable`, `focusable`, or `semantics` elements.
- Elements without `contentDescription` show generic labels ("Button 12"). Always provide `contentDescription`.

### Voice Commands

| Command | Action | Implementation Note |
|---------|--------|-------------------|
| "Tap [label]" | Activate element | Label comes from `contentDescription` or auto-assigned number |
| "Scroll down" | Scroll `LazyColumn` | Works automatically |
| "Scroll up" | Scroll reverse | Works automatically |
| "Go back" | Navigate back | System-level, no app change needed |
| "Show labels" | Show all labels on screen | System-level |
| "Hide labels" | Hide labels | System-level |

---

## Contrast Requirements

### MD3 Role Guarantees
When using `MaterialTheme.colorScheme` correctly, contrast is guaranteed:

| Text Role | On Background | Contrast | WCAG Level |
|-----------|--------------|----------|------------|
| `onSurface` (body text) | `surface` (background) | ≥ 4.5:1 | AA |
| `onSurfaceVariant` (secondary text) | `surface` | ≥ 3:1 | Large text AA |
| `onPrimary` (button text) | `primary` (button) | ≥ 4.5:1 | AA |
| `onError` (error text) | `error` | ≥ 4.5:1 | AA |
| `onPrimaryContainer` | `primaryContainer` | ≥ 4.5:1 | AA |

### Custom Color Verification
When using custom colors, verify with `md3_checker.py`:

```python
# md3_checker.py — verify a custom color pair
# Usage: python3 md3_checker.py --fg "#1A1C1E" --bg "#FFFFFF" --size 14sp
# Output: Contrast ratio: 15.9:1 PASS (AA + AAA)
```

### Gradient/Image Backgrounds
For text over gradients or images, check contrast at the **worst point** (lightest pixel behind darkest text, or vice versa). Tool: `md3_checker.py --gradient "image.png" --text "#000000" --bounds-left 0.3`.

### Critical Contrast Rules

| Context | Minimum | Notes |
|---------|---------|-------|
| Body text (< 18pt) | 4.5:1 | `onSurface` on `surface` |
| Large text (≥ 18pt or 14pt bold) | 3:1 | Headlines, titles |
| UI components (buttons, inputs) | 3:1 | Border on background |
| Icons | 3:1 | Same as large text |
| Disabled text | No minimum | But must be distinguishable from enabled |
| Logos | No minimum | Decorative only |

---

## Text Scaling

### System Font Size

| Setting | Scale | Dev System Equivalent |
|---------|-------|----------------------|
| Smallest | 85% | Test at `0.85f` scale factor |
| Default | 100% | Standard |
| Larger | 130% | System max via Display settings |
| Largest Accessibility | 200% | Via Accessibility → Font size → Largest |

### Using `sp` Units (Always)
```kotlin
// CORRECT: scales with system font size
Text(
    text = "Hello",
    fontSize = 16.sp // ✅ Uses sp — scales with system preferences
)

// WRONG: does not scale
Text(
    text = "Hello",
    fontSize = 16.dp // ❌ Uses dp — does NOT scale with system preferences
)
```

### Compose Best Practices
```kotlin
// Typography scales — define in sp
val typography = Typography(
    bodyLarge = TextStyle(fontSize = 16.sp, lineHeight = 24.sp),
    titleLarge = TextStyle(fontSize = 22.sp, lineHeight = 28.sp)
)

// Layout: use weight() and fillMaxWidth() instead of fixed widths
// This prevents text truncation at large font sizes
Text(
    text = longString,
    modifier = Modifier.fillMaxWidth(),
    overflow = TextOverflow.Ellipsis,
    maxLines = 2
)
```

### Testing at Scale
- Test layouts at 85%, 100%, 130%, and 200% font scale.
- Verify no text truncation (no clipped words).
- Verify no overlapping elements.
- Verify `LazyColumn` items don't crowd each other.

---

## Reduce Motion

### Detection
```kotlin
// Check if animations are disabled system-wide
val durationScale = Settings.Global.getFloat(
    contentResolver,
    Settings.Global.ANIMATOR_DURATION_SCALE,
    1.0f
)
val reduceMotion = durationScale == 0.0f
```

### When Reduce Motion is Enabled
| Disable | Replace With |
|---------|-------------|
| Entrance animations (fade in, slide up) | Instant appear |
| Parallax scrolling effects | Static backgrounds |
| Auto-advancing carousels | Static cards or manual navigation |
| Decorative animations (pulsing, bouncing) | Static elements |
| Page transition animations | Instant page swap |

```kotlin
val durationScale = Settings.Global.getFloat(
    LocalContext.current.contentResolver,
    Settings.Global.ANIMATOR_DURATION_SCALE, 1.0f
)
val reduceMotion = durationScale == 0.0f

AnimatedVisibility(
    visible = isVisible,
    enter = if (reduceMotion) EnterTransition.None else fadeIn(),
    exit = if (reduceMotion) ExitTransition.None else fadeOut()
) { Content() }
```

---

## Captions and Audio

### CaptioningManager
Read system caption preferences to auto-apply:

```kotlin
val captioningManager = context.getSystemService(CaptioningManager::class.java)
val fontSize = captioningManager.fontScale // System caption preference
val style = captioningManager.userStyle // Caption appearance
val locale = captioningManager.locale // Preferred caption language
```

### Requirements
- All spoken content in video must have captions.
- Music/ambient audio should have descriptive captions: "[Upbeat jazz playing]", "[Thunder rumbling]".
- Audio ducking during TalkBack: lower media volume when TalkBack is speaking.

---

## Time-Based Accessibility

### Detecting Accessibility Services
```kotlin
val accessibilityManager = context.getSystemService(AccessibilityManager::class.java)
accessibilityManager.addAccessibilityStateChangeListener { enabled ->
    if (enabled) {
        // Any accessibility service is ON
        increaseTimeouts()       // Extend toast/snackbar duration
        disableAutoAdvance()     // Stop carousel auto-rotation
        enableDescriptiveLabels() // Switch from short to descriptive content descriptions
    }
}
```

### Timeout Adjustments

| Element | Default Timeout | Accessibility Timeout |
|---------|----------------|----------------------|
| Snackbar | 4 seconds | 10 seconds |
| Toast | 2 seconds | 6 seconds |
| Auto-dismiss dialog | 3 seconds | Disable — require explicit dismiss only |
| Auto-advancing carousel | 5 seconds | Disable — require manual next/previous buttons |
| Loading indicator timeout | 10 seconds | 30 seconds (some users need more time) |

---

## Testing Tools

### Accessibility Scanner (APK)
Google's official automated checker. Install from Play Store. Scans any screen and reports:
- [ ] Missing `contentDescription`
- [ ] Touch targets < 48dp
- [ ] Contrast failures (< 4.5:1)
- [ ] Unlabeled elements
- [ ] Text scaling issues

### TalkBack (Built-in)
Enable: Settings → Accessibility → TalkBack → ON
Test every screen with TalkBack:
- [ ] Can you navigate to every element?
- [ ] Are the descriptions meaningful?
- [ ] Is the focus order logical?
- [ ] Can you complete every task (sign in, create item, search)?

### Switch Access
Enable: Settings → Accessibility → Switch Access → ON
- [ ] Can you navigate via scanning?
- [ ] Are all interactive elements reachable?
- [ ] Are groups logical?

### Voice Access
Enable: Settings → Accessibility → Voice Access → ON
- [ ] Do all interactive elements have visible labels?
- [ ] Can you say "tap [label]" and get the right element?

### Layout Inspector
Android Studio → View → Tool Windows → Layout Inspector
- [ ] Select "Accessibility Properties" view
- [ ] Verify `contentDescription` on all elements
- [ ] Verify `importantForAccessibility` flags

### Testing on Physical Device (Not Emulator)
Accessibility testing **must** be done on a physical device:
- Emulators cannot simulate Switch Access or Voice Access reliably.
- TalkBack on emulator misses gesture nuances.
- Real device testing reveals real-world interaction issues (thumb reach, vibration, system bar interactions).
