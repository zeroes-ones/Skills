# Platform-Specific Material Design Patterns
<!-- YAML-style: title: Platform-Specific Material Design Patterns, date: 2026-07-26 -->

## Android Phone (Compact)

### Navigation
- **Bottom Navigation Bar**: 3-5 top-level destinations. Always visible at screen bottom. Destinations have icon + label (3-4 items) or icon-only (5 items — label shown on active item only). Badge support for notifications. Each destination preserves its own back stack via nested `NavHost`.
- **Top App Bar**: Title, optional navigation icon (hamburger or back arrow), overflow menu (max 3-4 actions before collapsing). Collapsing/lifting variants for scroll-aware behavior.
- **FAB (Floating Action Button)**: Primary action on screen. Position: bottom-end by default (56dp from bottom, 16dp from end). Extended FAB for labeled actions. Mini FAB for secondary related actions.

### Ergonomic Zones (Thumb-Reach Heat Map)

| Zone | Screen Region | Reach Difficulty | What Goes Here |
|------|--------------|-----------------|----------------|
| Natural (Green) | Bottom 1/3 | Easiest — natural thumb arc | Navigation bar, FAB, primary CTAs, bottom sheets |
| Stretch (Yellow) | Middle 1/3 | Moderate — requires thumb extension | Core content, secondary actions, lists |
| Reach (Orange) | Top 1/4 | Stretch — requires hand adjustment | Titles, search bar, profile, overflow |
| Overhead (Red) | Top edge, corners | Hardest — two-handed on large phones | Branding, rarely-used settings |

### Safe Areas & System Bars

| System Bar | Height | Behavior |
|-----------|--------|----------|
| Status Bar | `24dp` (default), `28dp+` with cutout | Draw behind with `WindowInsetsCompat`. Use `fitsSystemWindows` or insets padding. |
| Navigation Bar | `48dp` (gesture nav) or `48dp` (3-button) | Edge-to-edge content. Transparency behind gesture bar. Never place interactive elements behind nav bar. |
| Cutout / Notch | Varies by device | Query `displayCutout` via `WindowInsets`. Never place interactive elements in cutout zone. Extend immersive content (video, maps) into cutout; keep critical UI clear. |

```kotlin
// Edge-to-edge with inset handling
ViewCompat.setOnApplyWindowInsetsListener(rootView) { v, insets ->
    val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
    v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
    WindowInsetsCompat.CONSUMED
}
```

### Back Gesture (Android 14+)
- **Edge-to-edge gesture**: Swipe inward from left or right edge.
- **Predictive back animation**: System handles animation; app integrates via `OnBackPressedCallback` or `BackHandler` in Compose. Shows peek of destination behind.
- **Override rules**: Rarely override system back. Only for in-app transitions (e.g., dismissing a sheet) — and even then, use `PredictiveBackLayout` to match system animation.

### System Share Sheet
- Invoke via `Intent.ACTION_SEND` or `Intent.ACTION_SEND_MULTIPLE`.
- Direct share targets (contacts, frequent apps) appear at top — set `Intent.EXTRA_CHOOSER_TARGETS`.
- Custom preview: `Intent.EXTRA_TITLE` and `ClipData` for rich share previews.
- Do NOT build custom share sheets — users rely on consistency.

---

## Tablet / Foldable (Medium/Expanded)

### Navigation

| Orientation | Pattern | Details |
|------------|---------|---------|
| Portrait | Navigation Rail | Left-edge column of icons + labels. 3-7 destinations. FAB can float within rail or content area. |
| Landscape | Permanent Navigation Drawer | Always-visible side panel with `ModalNavigationDrawer` closed by default, but openable as permanent. |
| Both | Top App Bar (optional) | May be omitted when rail/drawer handles navigation. |

### Canonical Layouts

| Layout | Width Split | Use Case |
|--------|------------|----------|
| **List-Detail** | 1/3 list + 2/3 detail | Email, contacts, settings. `ListDetailPaneScaffold` in Compose. |
| **Supporting Pane** | 2/3 main + 1/3 contextual | Document editing + comments, map + POI details, code + file browser. |
| **Feed** | 2-3 column grid | Photos, news, product catalog. `LazyVerticalStaggeredGrid` with dynamic column count. |

### Window Size Classes

| Class | Breakpoint (dp) | Typical Devices | Layout Guidance |
|-------|----------------|-----------------|-----------------|
| **Compact** | < 600dp width | Phone (portrait), foldable folded | Single pane, bottom nav |
| **Medium** | 600–840dp width | Tablet (portrait), foldable unfolded (inner screen), phone landscape | List-detail, navigation rail |
| **Expanded** | > 840dp width | Tablet (landscape), desktop, ChromeOS | Multi-pane, permanent drawer |

```kotlin
// Compose adaptive layout
val windowSizeClass = currentWindowAdaptiveInfo().windowSizeClass

when (windowSizeClass.windowWidthSizeClass) {
    WindowWidthSizeClass.COMPACT -> CompactLayout()
    WindowWidthSizeClass.MEDIUM -> MediumLayout()
    WindowWidthSizeClass.EXPANDED -> ExpandedLayout()
}
```

### Multi-Window
- **Split-screen**: Drag divider to resize. Both activities remain in `onResume` state. Handle configuration changes without data loss.
- **Freeform (ChromeOS/Samsung DeX)**: Resizable, freely-positioned windows. Support multi-instance (multiple activities of the same app).
- **Drag and drop**: Between apps via `OnDragListener` or `Modifier.dragAndDropSource`/`Modifier.dragAndDropTarget` in Compose. Support `ClipData` for text, images, URIs.

### Foldable-Specific
- **Hinge-aware layouts**: Avoid placing text, buttons, or interactive elements across the hinge zone (center crease). Use hinge as natural separator.
- **Posture API**: `Jetpack WindowManager` exposes `FoldingFeature` — query hinge position and orientation.
- **Tabletop mode**: Content above hinge, controls below (like a mini laptop).

---

## Wear OS

### Navigation
- **Swipe-to-dismiss**: Pages dismiss with horizontal swipe. `SwipeDismissFrameLayout` wraps content.
- **RSB (Rotary Side Button)**: Press opens app launcher. Long-press opens Google Assistant. Double-press opens most recent app (configurable).
- **Back gesture**: Swipe right from left edge (or left from right edge) dismisses current screen.
- **Deep links limited**: Each screen should be self-contained — avoid deep, nested navigation.

### Complications

| Type | Max Dimensions | Description |
|------|---------------|-------------|
| `SHORT_TEXT` | 48×48dp icon | Short text string (temperature, step count, battery). |
| `LONG_TEXT` | ~48×48dp | Multi-line text (calendar event title + time). 2 lines max. |
| `RANGED_VALUE` | ~48×48dp | Progress arc with min/max/current values (heart rate, UV index). |
| `ICON` | 48×48dp | Single icon (weather condition, notification dot). |
| `SMALL_IMAGE` | 48×48dp | Small photo or graphic (album art, contact photo). |
| `LARGE_IMAGE` | Varies by slot | Full-bleed photo background. |
| `MONOCHROMATIC_IMAGE` | 48×48dp | Single-color icon tinted to accent. |

### Glance Time
- **< 2 seconds** to read critical information.
- Content above the fold (no scrolling for key data). Tappable elements must be immediately identifiable.
- Use large, bold typography with high contrast on always-on-display (AOD) mode.

### Input

| Input Method | Usage |
|-------------|-------|
| Physical bezel (rotary input) | Scroll lists, adjust sliders, zoom. Detect via `RotaryEvent`. Not available on all devices — always provide touch fallback. |
| RSB press | App launcher (single), Assistant (long), Recents (double). |
| Touch (swipe/tap) | Primary navigation and interaction. |
| Voice | Google Assistant for commands, dictation for text input. |

### Tiles
- Swipe-left carousel of glanceable views from watch face.
- **Max 5-7 tiles** per app (system limits). Each tile renders a single-purpose, read-only data snapshot.
- `TileService` extends `androidx.wear.tiles.TileService`. State-driven refresh via `TileData`.
- Composable tiles available with `wear-tiles` library.

### Always-On Display (AOD)
- **Burn-in protection required**. Shift pixels every 60 seconds.
- Use `AmbientMode` in Compose or `AmbientModeSupport` in Views.
- AOD design rules:
  - Remove all white/light backgrounds (< 15% of pixels ON at any time).
  - Outline-only icons, no filled shapes.
  - Text should be thin/outlined weight.
  - No animations in AOD mode.

```kotlin
// Compose AOD handling
AmbientAware(ambientModeController) { ambientState ->
    if (ambientState.isAmbient) {
        // Burn-in safe: dark background, minimal white pixels
        Box(Modifier.background(Color.Black).ambientMode())
    } else {
        // Interactive mode: full color
        Box(Modifier.background(MaterialTheme.colorScheme.surface))
    }
}
```

---

## Android TV (10-Foot UI)

### Viewing Distance & Sizing

| Metric | Value |
|--------|-------|
| Typical viewing distance | 10 feet (3 meters) |
| Minimum touch target equivalent | 48dp on screen ≈ 1.5 inches physical |
| Minimum text size | 16sp for body, 24sp for titles |
| Default spacing | 16dp between elements |

### Navigation: D-Pad Focus
- **Directional navigation**: Up/Down/Left/Right only. No swipe, no drag, no pinch.
- **Focus management** is the #1 TV design priority. Every screen must have a clear, predictable focus path.
- Use `FocusRequester` in Compose TV or `focusable="true"` + `nextFocus[Direction]` in Views.
- Grid layouts: focus wraps within rows horizontally, jumps between rows vertically.

### Focus States (Required)

| State | Visual Treatment |
|-------|-----------------|
| Default (unfocused) | Standard appearance. No elevation. |
| Focused | Bright border/outline (2-3dp). Scale animation to `105-110%`. Color accent highlights. Text may increase weight. |
| Pressed | Brief scale-down to `95%` during D-pad center press. |
| Disabled | Dimmed to 40% opacity. Cannot receive focus. |

**Crucial rules:**
- **No hover-only states** — TV has no mouse/cursor. Everything must work via focus.
- Focus indicator must be clearly visible from 10 feet.
- Animate focus transitions smoothly (`animateItemPlacement`, `AnimatedVisibility`).

### Content Hierarchy (Leanback Patterns)

```
┌──────────────────────────────────────────┐
│  Hero Row (top)                          │
│  ┌──────────────────────────────────────┐│
│  │   Full-width, large poster/video    ││
│  └──────────────────────────────────────┘│
│  Category Row 1: "Continue Watching"     │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐     │
│  │card│ │card│ │card│ │card│ │card│ →   │
│  └────┘ └────┘ └────┘ └────┘ └────┘     │
│  Category Row 2: "Trending Now"          │
│  ...                                     │
└──────────────────────────────────────────┘
```

Key Leanback classes:
- `BrowseSupportFragment`: Main browsing layout with rows
- `PlaybackOverlayFragment`: Video playback with transport controls
- `DetailsSupportFragment`: Content detail view with actions

### Search
- **On-screen keyboard**: Alphabetical layout (ABCDEF...), NOT QWERTY. Users navigate with D-pad — alphabetical is faster for directional input.
- **Voice-first preferred**: Trigger Google Assistant for search — "Search for comedies."
- `SearchSupportFragment`: Leanback search with voice input integrated.

### Input (What's Available)
- **D-pad + Game Controller**: Primary. Directional + select + back.
- **Remote with microphone**: Voice search supported.
- **NOT touch**: Never assume touch. No swipe gestures, no drag-to-reorder, no pinch-to-zoom.
- **NOT mouse/keyboard** (in most cases): Unless targeting ChromeOS TV overlays specifically.

---

## Android Auto

### Distraction Optimization

| Constraint | Limit | Rationale |
|-----------|-------|-----------|
| Max taps per task | 6 taps | NHTSA guidelines. Any task exceeding 6 taps is a driving hazard. |
| Glance duration | < 2 seconds | Total eyes-off-road time per interaction. |
| Text size minimum | 42sp for primary | Must be readable at arm's length in motion. |
| List scroll depth | Max 6 items | Reduce browsing while driving. Offer search/voice instead. |

### Templates (DHU — Desktop Head Unit)
Android Auto apps are template-driven; you do not design free-form layouts.

| Template | Use Case | Key Elements |
|----------|----------|-------------|
| **Navigation** | Turn-by-turn maps | `NavigationTemplate` with map surface + step info. `MapActionStrip` for ancillary actions (mute, search). |
| **Media** | Audio playback | `MediaTemplate` with large album art, playback controls (play/pause, skip), seek bar. |
| **Messaging** | Read aloud + reply | `MessagingTemplate` — incoming message read aloud via TTS. Reply via voice dictation only. No on-screen keyboard. |
| **Point of Interest (POI)** | Location browsing | `PlaceListNavigationTemplate` — list of nearby destinations. Tap to navigate. |
| **Sign-in / Landing** | Initial setup | `SignInTemplate` — minimal, must complete before driving or defer. |

### Touch Targets

| Element | Minimum Size | Notes |
|---------|-------------|-------|
| Action buttons | 76dp × 76dp | Larger than mobile (48dp) due to vehicle vibration. |
| List items | 84dp height | Extra spacing prevents mis-taps. |
| Seek bar thumb | 32dp | Same as mobile, but surrounding touch area padded to 76dp. |

### Design Constraints
- **Dark theme mandatory**: Light mode is unsafe at night. Must support system dark theme always ON.
- **Voice-first**: Google Assistant integration required. All text input must have voice fallback. On-screen keyboard prohibited during driving.
- **No video**: No video playback, animated GIFs, or distracting motion.
- **No notifications**: Android Auto suppresses standard Android notifications. Use `CarAppExtender` for auto-specific updates.
- **No immersive content**: No full-screen experiences, no games.

---

## Large Screen / ChromeOS / Desktop

### Input Assumptions

| Input Type | Available | Implications |
|-----------|-----------|--------------|
| Keyboard | Yes (physical or on-screen) | Support all standard shortcuts (Ctrl+C/V/Z, Ctrl+N, Ctrl+W). `onKeyEvent` in Compose or `onKeyDown` in Views. |
| Mouse / Trackpad | Yes | Right-click context menus (`DropdownMenu` + `onRightClick`). Hover states, scroll wheel. Cursor changes. |
| Touch | Yes (on convertible Chromebooks) | Still support touch — layering touch + keyboard/mouse. |
| Stylus | Yes (on some devices) | Input region for drawing/signing, pressure sensitivity. |

### Window Management
- **Resizable windows**: All apps must handle free-form resize. Use `WindowSizeClass` to adapt layout.
- **Title bar**: Show window title, window controls (minimize, maximize, close). Customize with `enableEdgeToEdge` + custom title bar or use system default.
- **Multi-instance**: Allow multiple app windows via `android:resizeableActivity="true"` and `launchMode="standard"` (not `singleTask`).

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Z` | Undo |
| `Ctrl+Shift+Z` / `Ctrl+Y` | Redo |
| `Ctrl+C` / `Ctrl+X` / `Ctrl+V` | Copy / Cut / Paste |
| `Ctrl+A` | Select All |
| `Ctrl+N` | New item/window |
| `Ctrl+W` | Close current window/tab |
| `Ctrl+S` | Save |
| `Ctrl+F` | Find/Search within page |
| `Ctrl+P` | Print |
| `Ctrl+Tab` | Switch tabs |
| `Escape` | Dismiss dialog / back navigation |
| `F11` | Toggle fullscreen |

### Context Menus
- Right-click on any interactive element should show a context menu.
- Menu items: relevant actions for that element (Edit, Delete, Share, Open in new window).
- Use `PopupMenu` or `DropdownMenu` attached to click coordinates.

### Desktop-Specific Patterns
- **Drag handles**: Window edges for resize; title bar for move.
- **Notification tray integration**: System notifications via `NotificationManager` appear in ChromeOS system tray.
- **File system access**: `Storage Access Framework` for open/save dialogs.
- **Printing**: `PrintManager` for system print dialog.
