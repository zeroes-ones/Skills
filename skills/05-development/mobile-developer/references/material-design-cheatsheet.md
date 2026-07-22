---
title: "Material Design 3: Complete Reference"
author: Sandeep Kumar Penchala
date: 2026-07-21
---

## Type Scale

Material Design 3 defines 15 type tokens across 5 categories. All sizes in `sp`, line-height in `sp`, letter-spacing in `em`. Default font: **Roboto**. **Google Sans** reserved for Display only (brand moments), never body text.

| Token | Size | Line Height | Letter Spacing | Weight | Use Case |
|-------|------|-------------|----------------|--------|----------|
| `displayLarge` | 57 | 64 | -0.25 | 400 | Hero screens, splash, one-word headlines |
| `displayMedium` | 45 | 52 | 0 | 400 | Secondary hero text |
| `displaySmall` | 36 | 44 | 0 | 400 | Section openers, onboarding |
| `headlineLarge` | 32 | 40 | 0 | 400 | Page titles, article headings |
| `headlineMedium` | 28 | 36 | 0 | 400 | Sub-page titles, card headers |
| `headlineSmall` | 24 | 32 | 0 | 400 | List section headers, dialog titles |
| `titleLarge` | 22 | 28 | 0 | 400 | App bar title, bottom sheet title |
| `titleMedium` | 16 | 24 | 0.15 | 500 | List group labels, tab labels |
| `titleSmall` | 14 | 20 | 0.1 | 500 | Button text, chip labels, small section labels |
| `bodyLarge` | 16 | 24 | 0.5 | 400 | Long-form body text, paragraphs |
| `bodyMedium` | 14 | 20 | 0.25 | 400 | Secondary body, list body text |
| `bodySmall` | 12 | 16 | 0.4 | 400 | Captions, timestamps, helper text |
| `labelLarge` | 14 | 20 | 0.1 | 500 | Button labels, tab labels |
| `labelMedium` | 12 | 16 | 0.5 | 500 | Chip labels, badge text |
| `labelSmall` | 11 | 16 | 0.5 | 500 | Overline, small badges above content |

### Semantic Usage Rules

- **Display**: Brand moments only — splash screens, onboarding hero, empty states with a single large word. Never in scrolling lists.
- **Headline**: Page-level hierarchy. One `headlineLarge` per screen maximum. Use `headlineSmall` for cards and dialogs.
- **Title**: UI element labels. `titleLarge` for top app bar. `titleMedium` for lists and navigation. `titleSmall` for buttons and chips.
- **Body**: Content text. `bodyLarge` for paragraphs (16sp minimum for accessibility). `bodyMedium` for inline text. `bodySmall` strictly for captions — never truncate with smaller body.
- **Label**: All-caps in design, not code (set via `textAllCaps` or CSS `text-transform`). Use for buttons, chips, badges, overlines.

### Platform Mapping

| Token | Android XML | Compose | iOS UIFont | CSS |
|-------|-------------|---------|------------|-----|
| `displayLarge` | `textAppearanceDisplayLarge` | `MaterialTheme.typography.displayLarge` | `.largeTitle` | `font-size: 57px; letter-spacing: -0.25px` |
| `headlineSmall` | `textAppearanceHeadlineSmall` | `MaterialTheme.typography.headlineSmall` | `.title3` | `font-size: 24px` |
| `bodyLarge` | `textAppearanceBodyLarge` | `MaterialTheme.typography.bodyLarge` | `.body` | `font-size: 16px; letter-spacing: 0.5px` |

---

## Color System (M3 Color Roles)

### Core Palette Roles

| Role | Meaning | When Used |
|------|---------|-----------|
| `primary` | Brand color | FAB, prominent buttons, active icons, progress |
| `onPrimary` | Content on primary | Text/icons on primary surfaces — must meet 4.5:1 contrast |
| `primaryContainer` | Tinted version of primary | Less-emphasis containers, highlighted list items |
| `onPrimaryContainer` | Content on primaryContainer | Text/icons inside primary containers |
| `secondary` | Complementary color | Filter chips, secondary buttons, selection controls |
| `onSecondary` | Content on secondary | Text/icons on secondary surfaces |
| `secondaryContainer` | Tinted version of secondary | Input fields, less-prominent containers |
| `onSecondaryContainer` | Content on secondaryContainer | Labels inside secondary containers |
| `tertiary` | Accent / contrast color | Accent elements needing distinction from primary+secondary |
| `onTertiary` | Content on tertiary | Text/icons on tertiary surfaces |
| `tertiaryContainer` | Tinted version of tertiary | Accent backgrounds, highlights |
| `onTertiaryContainer` | Content on tertiaryContainer | Labels inside tertiary containers |
| `error` | Error indication | Error icon, destructive action, error text |
| `onError` | Content on error | Text/icons on error backgrounds |
| `errorContainer` | Tinted error | Error banners, error input backgrounds |
| `onErrorContainer` | Content on errorContainer | Error message text inside error container |

### Surface Roles

| Role | Meaning |
|------|---------|
| `surface` | Default background for cards, sheets, dialogs, menus |
| `onSurface` | Default text/icon color on surface |
| `surfaceVariant` | Alternative surface (e.g., side panels, app drawer) |
| `onSurfaceVariant` | Text/icon on surfaceVariant — often used for subtitles, captions |
| `surfaceTint` | Elevation overlay color — tints surfaces at higher elevations |
| `inverseSurface` | Opposite of surface (e.g., dark tooltip on light theme) |
| `inverseOnSurface` | Content on inverseSurface |
| `background` | App window background (often same as `surface` in M3) |
| `onBackground` | Content on background |

**Surface vs Background**: In M3, `surface` replaces `background` for most use cases. Use `background` only for the root window. Cards, sheets, dialogs all use `surface`. The elevation overlay system automatically tints `surface` using `surfaceTint` at higher DP levels.

### Outline Roles

| Role | Meaning |
|------|---------|
| `outline` | Borders: text fields, dividers, card strokes |
| `outlineVariant` | Weaker borders: thin dividers, decorative strokes |

### Elevation Overlay System

In M3, elevation is expressed through **surface tint** overlays, not heavy shadows (M2 approach). At each elevation level, `surfaceTint` is blended onto `surface` at increasing opacity:

| Elevation (dp) | Light Theme Opacity | Dark Theme Opacity |
|----------------|---------------------|---------------------|
| 0 | 0% | 0% |
| 1 | 5% | 8% |
| 2 | 8% | 12% |
| 3 | 11% | 16% |
| 4 | 12% | 18% |
| 5 | 14% | 20% |

In dark theme, overlay is more prominent because dark surfaces need more tonal separation.

---

## Dynamic Color (Material You / Monet)

### How It Works

1. **Wallpaper extraction**: Android extracts a source (seed) color from the user's wallpaper using quantized color analysis.
2. **Tonal palette generation**: The seed color runs through the HCT (Hue-Chroma-Tone) color space to generate a full tonal palette (tones 0-100). Each role maps to a specific tone.
3. **Role assignment**: Roles are assigned from the palette — e.g., primary uses tone 40, primaryContainer tone 90, onPrimary tone 100.

### Implementation

**Android 12+ (automatic)** — add to `themes.xml`:
```xml
<style name="Theme.MyApp" parent="Theme.Material3.DynamicColors.DayNight">
    <!-- Everything auto-derived from wallpaper -->
</style>
```

Or programmatic override:
```kotlin
DynamicColors.applyToActivityIfAvailable(this)
```

**Manual palette with `material-color-utilities`** (Jetpack Compose / custom seed):
```kotlin
val hct = Hct.fromInt(seedColorArgb)
val scheme = SchemeTonalSpot(hct, isDark = false, contrastLevel = 0.0)
// scheme.primary, scheme.onPrimary, etc. are all computed
```

### When to Use Dynamic Color

| ✅ Use Dynamic | ❌ Avoid Dynamic |
|---------------|------------------|
| Utility apps, tools, communication | Brand-heavy apps (Spotify, Netflix) |
| Apps where personalization matters | Games |
| Android-first apps | Cross-platform apps needing consistent brand |
| When you have no strong brand color | When brand recognition is critical |

### Overriding Specific Roles

Keep dynamic colors but override specific roles:
```kotlin
val dynamicScheme = /* from wallpaper */
MaterialTheme(
    colorScheme = dynamicScheme.copy(
        primary = BrandColors.PRIMARY,  // override brand
        // all other roles remain dynamic
    )
)
```

---

## Elevation & Shadows

### M3 Elevation Levels

M3 reduces M2's 24 elevation levels to **5 levels (0-5)**, plus arbitrary custom values.

| Level | DP | Visual | Use |
|-------|-----|--------|-----|
| 0 | 0 | Flat, no elevation | Body content, full-screen surfaces |
| 1 | 1 | Subtle surface tint only | Cards (resting), list items, chips |
| 2 | 3 | Light tint | FAB (resting), menu, bottom sheet |
| 3 | 6 | Medium tint | FAB (pressed), dialog, drawer |
| 4 | 8 | Pronounced tint | Navigation drawer (over other content) |
| 5 | 12 | Strong tint | Modal dialogs, time pickers |

### Shadow vs Tint

- **M2**: relied on shadow `elevation` for depth perception.
- **M3**: uses `surfaceTint` color overlay at increasing opacity. Shadows are secondary, softer, and applied via `spotShadowColor` (ambient) — not the primary depth cue.

On Android, set via `tonalElevation` (M3) instead of `elevation` (M2):
```kotlin
Card(elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)) // M3 tonal
```

---

## Component Specifications

### Buttons

| Variant | Height | Corner Radius | Horizontal Padding | Icon Size | Use |
|---------|--------|---------------|---------------------|-----------|-----|
| **Filled** | 40dp | 20dp (full pill) | 24dp | 18dp | Primary action per screen |
| **Filled Tonal** | 40dp | 20dp | 24dp | 18dp | Secondary prominence |
| **Outlined** | 40dp | 20dp | 24dp | 18dp | Medium emphasis, forms |
| **Text** | 40dp | 20dp | 12dp | 18dp | Low emphasis, card actions |
| **Elevated** | 40dp | 20dp | 24dp | 18dp | When button needs to sit above scroll content |

**FAB (Floating Action Button)**:

| Variant | Container Size | Icon Size | Corner | Note |
|---------|---------------|-----------|--------|------|
| Regular FAB | 56×56dp | 24dp | 16dp | Default |
| Small FAB | 40×40dp | 24dp | 12dp | When regular FAB is too dominant |
| Large FAB | 96×96dp | 36dp | 28dp | Promotional, onboarding |
| Extended FAB | 48dp height | 24dp | 16dp | Has text label (16dp padding each side) |

**Button states** (all variants): enabled, hovered, focused, pressed, disabled. Opacity at disabled: 38% (content), 12% (container if filled).

### Navigation Bar

- **Height**: 80dp (70dp without bottom system inset)
- **Destinations**: 3-5 (never fewer than 3, never more than 5)
- **Active indicator**: 32×16dp pill, centered behind icon
- **Icon**: 24×24dp
- **Label**: 12sp, below icon, `labelMedium` token
- **Badge**: 16dp diameter above icon, max 2 digits (shows "9+" above)

### Navigation Rail

- **Width**: 80dp
- **Icon containers**: 56×32dp pill (active), 32×32dp (inactive)
- **Icon**: 24dp
- **Destinations**: 4-7 (ideal for tablet/desktop)
- **FAB position**: centered above the rail or as a menu item

**Breakpoint Decision**:
| Window Width | Navigation |
|--------------|------------|
| < 600dp (Compact) | Bottom Navigation Bar |
| 600-840dp (Medium) | Navigation Rail |
| > 840dp (Expanded) | Navigation Drawer (permanent) |

### Top App Bar

| Variant | Height | Scroll Behavior |
|---------|--------|-----------------|
| Center-aligned | 64dp | Pin (stays), Collapse (hides on scroll). Use `TopAppBarScrollBehavior` |
| Small | 64dp | EnterAlways (reappears on upward scroll) |
| Medium | 112dp | Collapses to 64dp on scroll |
| Large | 152dp | Collapses to 64dp. Title transitions from `headlineMedium` to `titleLarge` |

- **Leading icon**: 24dp, 48dp touch target
- **Headline**: `titleLarge` (22sp)
- **Trailing icons**: max 3, each 24dp in 48dp touch target

### Cards

| Variant | Elevation | Corner Radius | Content Padding |
|---------|-----------|---------------|-----------------|
| Elevated | 1dp | 12dp | 16dp |
| Filled | 0 | 12dp | 16dp |
| Outlined | 0 | 12dp | 16dp |

- **Rich media**: extend image to card edges (top corners only), then content below
- **Actions**: text buttons at bottom, left-aligned; primary action rightmost
- **Swipe dismiss**: use `SwipeToDismissBox` with background reveal

### Dialogs

| Property | Value |
|----------|-------|
| Corner radius | 28dp |
| Min width | 280dp |
| Max width | 560dp (560dp on tablet) |
| Title | `headlineSmall` (24sp), 24dp padding top |
| Body | `bodyMedium` (14sp), 16dp padding between title and actions |
| Actions | Right-aligned, 8dp gap. Affirmative button rightmost. Max 2 buttons in basic dialog. |

**Full-screen dialog**: Use for complex forms, search. Top app bar with close (X) + optional affirmative action. Content scrollable. 16dp side padding.

### Snackbar

| Variant | Height | Max Lines | Dismiss |
|---------|--------|-----------|---------|
| Single-line | 48dp | 1 line text + 1 action | Auto-dismiss 4s, or swipe |
| Two-line | 68dp | 2 lines text + 1 action | Auto-dismiss 6s, or swipe |

- **Position**: bottom of screen, above navigation bar
- **Action**: `labelLarge`, `primary` color, right-aligned
- **Behavior**: only one visible at a time. New snackbar replaces existing.

### Text Fields

| Variant | Active Indicator | Container |
|---------|-----------------|-----------|
| Filled | Bottom stroke (1dp inactive, 2dp active) | `surfaceVariant` background, 4dp top corner |
| Outlined | Full border (1dp inactive, 2dp active) | Transparent, 4dp corner |

- **Height**: 56dp (single line). `labelSmall` (11sp) floating label at top.
- **Label animation**: label at center when empty → shrinks to top on focus/filled
- **Supporting text**: `bodySmall` (12sp), 4dp below field. Error: `error` color. Character counter: right-aligned.
- **Leading icon**: 24dp, left side. **Trailing icon**: 24dp, right side (clear button, password toggle).
- **Touch target**: 48dp minimum height per tappable area.

### Chips

| Variant | Behavior | When |
|---------|----------|------|
| **Assist** | Acts like a small button | "Add to calendar", "Get directions" |
| **Filter** | Toggle selection. Check icon appears on selected. | Filter lists by category |
| **Input** | Displays data, removable with close icon | Email recipients, tags |
| **Suggestion** | Acts as a quick suggestion | Autocomplete dropdown, search history |

- **Height**: 32dp
- **Corner radius**: 8dp
- **Icon size**: 18dp (leading). 18dp close affordance (trailing, input chips).
- **Label**: `labelLarge` (14sp)
- **Selection state**: Filter chips toggle `primaryContainer` background with check icon.

### Progress Indicators

| Type | Use |
|------|-----|
| **Linear determinate** | Known duration: file upload, download |
| **Linear indeterminate** | Unknown duration: page load, data fetch |
| **Circular determinate** | Known duration, compact space |
| **Circular indeterminate** | Unknown duration, inline (24dp icon) or full screen |

- **Track height**: 4dp (linear)
- **Stroke width**: 4dp (circular, default 48dp diameter)
- **Color**: `primary` for active track, `surfaceVariant` for inactive track

### Sliders

| Property | Continuous | Discrete |
|----------|------------|----------|
| Tick marks | No | Yes, at each step |
| Value display | No (or on thumb press) | Label bubble above thumb |
| When | Volume, brightness | Incremental settings (font size 12-24) |

- **Track**: 4dp height (active: `primary`, inactive: `surfaceVariant`)
- **Thumb**: 20dp diameter, ripple on press
- **Touch target**: 48dp

### Switches, Checkboxes, Radio Buttons

| Component | Touch Target | Icon Area | When |
|-----------|-------------|-----------|------|
| Switch | 48×48dp | 52×32dp (track) | Instant on/off (WiFi, Bluetooth) |
| Checkbox | 48×48dp | 18×18dp (box) | Multi-select in a list |
| Radio | 48×48dp | 20dp (outer circle) | Single-select from options |

- **Selection state colors**: `primary` when selected. `onSurface` at 38% opacity when unselected.
- **Haptic**: light tap on selection.

---

## Adaptive Layout Guidelines

### Window Size Classes

| Class | Width (dp) | Devices |
|-------|------------|---------|
| **Compact** | < 600 | Phone portrait, phone landscape (small) |
| **Medium** | 600 – 840 | Tablet portrait, phone landscape (large), foldable unfolded |
| **Expanded** | > 840 | Tablet landscape, desktop, foldable tablet |

### Canonical Layouts

1. **List-Detail**: List on left (⅓ width), detail on right (⅔). Compact: separate screens with navigation transitions. Medium+: side by side.
2. **Supporting Pane**: Main content (⅔) + contextual sidebar (⅓). Compact: bottom sheet instead of sidebar.
3. **Feed**: Full-width scrolling list. Compact: single column. Expanded: 2-3 column grid.

### Navigation Changes at Breakpoints

| Window Class | Navigation Pattern |
|--------------|-------------------|
| Compact | Bottom Navigation Bar + Top App Bar |
| Medium | Navigation Rail (left) + content area |
| Expanded | Permanent Navigation Drawer or Rail + Top-level tabs |

### Multi-Column on Tablets

```kotlin
// Jetpack Compose
val windowSizeClass = currentWindowAdaptiveInfo().windowSizeClass
if (windowSizeClass.windowWidthSizeClass == WindowWidthSizeClass.EXPANDED)
    ListDetailLayout()  // side-by-side
else
    SinglePaneLayout()  // stacked
```

---

## Motion

### Duration Tokens

| Token | Range | Use |
|-------|-------|-----|
| **Short** | 50 – 200ms | Button presses, toggle switches, ripple |
| **Medium** | 200 – 400ms | Screen transitions, FAB morph, card expand |
| **Long** | 400 – 700ms | Complex choreography, page enter/exit, onboarding |

### Easing Curves

| Easing | Bezier | Feel | When |
|--------|--------|------|------|
| **Standard** | `cubic-bezier(0.2, 0.0, 0, 1.0)` | Quick start, gentle deceleration | Most transitions, shared elements |
| **Emphasized** | `cubic-bezier(0.2, 0.0, 0, 1.0)` (longer duration) | Expressive deceleration | Hero transitions, full-screen dialogs |
| **Decelerated** | `cubic-bezier(0.0, 0.0, 0, 1.0)` | Fast entry, smooth stop | Elements appearing on screen |
| **Accelerated** | `cubic-bezier(0.2, 0.0, 1, 1.0)` | Quick exit, fast fade | Elements leaving screen |
| **Linear** | `cubic-bezier(0, 0, 1, 1)` | Constant speed | Progress indicators only |

### Transition Patterns

| Pattern | Description | Duration | Easing |
|---------|-------------|----------|--------|
| **Container Transform** | One surface morphs into another (card → detail page) | 300ms | Standard |
| **Fade Through** | Outgoing fades out, incoming fades in | 150ms each, staggered | Decelerated (in), Accelerated (out) |
| **Fade** | Simple crossfade (tab changes) | 200ms | Standard |
| **Slide** | Lateral slide (navigation drawer, bottom sheet) | 250ms | Standard |
| **Shared Axis** | Items move together in same direction (list → detail) | 300ms | Standard |

### Predictive Back Gesture

Android 14+ back gesture shows a preview of the destination before committing. Implement via `OnBackPressedCallback` + `OnBackInvokedDispatcher`:

```kotlin
override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    requireActivity().onBackPressedDispatcher.addCallback(viewLifecycleOwner) {
        // System shows destination peek during gesture
        findNavController().navigateUp()
    }
}
```

### Staggered Children Entrance

Stagger list items by 30-50ms each on screen enter:
```kotlin
// Compose
items.forEachIndexed { index, item ->
    AnimatedVisibility(
        visible = visible,
        enter = fadeIn() + slideInVertically { it / 2 }
            .apply { initialOffsetMillis = index * 50 }
    )
}
```

---

## Quick Reference: Common Mistakes

| ❌ Don't | ✅ Do |
|----------|------|
| Use `displayLarge` for page titles | Use `headlineLarge` for page titles |
| Apply `elevation` in M3 (M2 API) | Use `tonalElevation` in M3 |
| Use background for cards | Use `surface` for cards |
| Put 6+ items in bottom nav | Cap at 5; use a "More" pattern for extras |
| Use corner radius > 28dp on dialogs | Max 28dp corner radius for dialogs |
| Put affirmative button left in dialogs | Affirmative action always rightmost |
| Use `cornerRadius` + `masksToBounds` on iOS | Add `layer.shadowPath` to avoid offscreen render |
| Dynamic color for brand-heavy apps | Override `primary` only, keep dynamics for containers |
