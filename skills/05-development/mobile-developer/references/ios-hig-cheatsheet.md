---
author: Sandeep Kumar Penchala
title: "iOS Human Interface Guidelines: Complete Reference"
date: 2026-07-21
---

## Typography Scale

### SF Pro Text (for sizes <20pt) — primary UI font

| Style | Size (pt) | Weight | Leading (pt) | Tracking (pt) | UIFontTextStyle |
|---|---|---|---|---|---|
| Caption 2 | 11 | Regular | 13 | 0.07 | `.caption2` |
| Caption 1 | 12 | Regular | 16 | 0 | `.caption1` |
| Footnote | 13 | Regular | 18 | -0.08 | `.footnote` |
| Subheadline | 15 | Regular | 20 | -0.24 | `.subheadline` |
| Callout | 16 | Regular | 21 | -0.2 | `.callout` |
| Body | 17 | Regular | 22 | -0.41 | `.body` |
| Headline | 17 | Semibold | 22 | -0.41 | `.headline` |

### SF Pro Display (for sizes ≥20pt) — headings & large UI

| Style | Size (pt) | Weight | Leading (pt) | Tracking (pt) | UIFontTextStyle |
|---|---|---|---|---|---|
| Title 3 | 20 | Regular | 24 | 0.38 | `.title3` |
| Title 2 | 22 | Regular | 28 | 0.35 | `.title2` |
| Title 1 | 28 | Regular | 34 | 0.36 | `.title1` |
| Large Title | 34 | Regular | 41 | 0.37 | `.largeTitle` |

### Additional Styles

| Style | Size | Weight | Leading | Tracking | UIFontTextStyle |
|---|---|---|---|---|---|
| Extra Large Title | 36 | Regular | 43 | 0.37 | `.extraLargeTitle` |
| Extra Large Title 2 | 40 | Regular | 48 | 0.36 | `.extraLargeTitle2` |

### SF Pro Rounded
Use for: **widgets, complications, watchOS interfaces**. Available in same weight scale as SF Pro (Ultralight through Black). Do NOT use as the body font in standard iOS apps — it's primarily for Watch and widget surfaces.

### SF Mono
Use for: **code blocks, terminal output, fixed-width data display**. Available weights: Light through Heavy (6 weights). Scale: SF Mono uses the same size table as SF Pro but with monospaced glyphs (all glyphs occupy identical advance width). Do NOT use for proportional text — the fixed-width spacing looks mechanical in prose.

### Dynamic Type

**How it works**: Users set a preferred content size category in Settings → Display & Text Size → Larger Text. UIKit/SwiftUI automatically scales fonts that use `UIFont.preferredFont(forTextStyle:)` or `.font(.body)`.

**Scale factors** (relative to Large/default):

| Category | Scale Factor | Body becomes |
|---|---|---|
| xSmall | 0.82× | 14pt |
| Small | 0.88× | 15pt |
| Medium | 0.95× | 16pt |
| **Large** (default) | **1.00×** | **17pt** |
| Extra Large | 1.12× | 19pt |
| XXL | 1.24× | 21pt |
| XXXL | 1.36× | 23pt |
| AX1 | 1.53× | 26pt |
| AX2 | 1.76× | 30pt |
| AX3 | 2.06× | 35pt |
| AX4 | 2.41× | 41pt |
| AX5 | 2.82× | 48pt |

**Styles that scale the most**: Body, Headline, Subheadline scale aggressively. **Styles that scale the least**: Caption 1/2 — these stay compact even at AX sizes. Large Title may truncate at AX3+ — test with `.adjustsFontSizeToFitWidth` or `.minimumScaleFactor(0.5)`.

**Testing Dynamic Type**: 
- Simulator: Features → Toggle Increased (⌘+shift+= for larger, ⌘+shift+- for smaller)
- Device: Settings → Control Center → Add "Text Size" control
- Environment override in code: `UIApplication.shared.preferredContentSizeCategory = .accessibilityExtraExtraLarge`

**Large Content Viewer**: For tab bar items and toolbar buttons that rely on icons only — users with Dynamic Type ≥ AX can long-press to see a large text label. Enable via `largeContentSizeImage` + `largeContentSizeTitle` on `UIBarItem` subclasses, or `.accessibilityShowsLargeContentViewer()` in SwiftUI.

### Custom Fonts
- **When acceptable**: Brand identity fonts for headings, logo lockups, or if your design system requires a specific typeface not covered by SF Pro
- **Licensing pitfalls**: Every custom font requires a distribution license. SIL Open Font License (OFL) is safest. Commercial fonts (e.g., Helvetica Neue, Gotham) require per-app or per-company licensing. Embedding a font without a license = legal risk and possible App Store rejection
- **Fallback strategy**: Register custom font for `UIFontTextStyle` via `UIFontMetrics` to preserve Dynamic Type scaling:
  ```swift
  let customFont = UIFont(name: "BrandSans-Regular", size: 17)!
  let metrics = UIFontMetrics(forTextStyle: .body)
  label.font = metrics.scaledFont(for: customFont)
  ```
- If custom font lacks a glyph (e.g., emoji, CJK, Arabic), Core Text cascades to the system font. Verify with `CTFontCopyCharacterSet`. Never assume full Unicode coverage.

---

## Layout

### Safe Area Insets

| Device Class | Top (pt) | Bottom (pt) | Notes |
|---|---|---|---|
| iPhone SE (2nd/3rd gen) | 20 (status bar) | 0 | No notch, no home indicator |
| iPhone 8/8 Plus | 20 | 0 | Classic bezel, no safe area bottom |
| iPhone X/11 Pro/12 mini/13 mini | 44 | 34 | Notch + home indicator |
| iPhone 12/13/14 | 47 | 34 | Notch + home indicator |
| iPhone 14 Pro/15 Pro/16 Pro | 59 (dynamic island) | 34 | Dynamic island extends into top safe area |
| iPhone 14 Pro Max → 16 Pro Max | 59 | 34 | Larger dynamic island |
| iPad (all gen) | 20 (status bar) | 20 (home indicator on Face ID iPads) | On pre-Face ID iPads, bottom = 0 |
| iPad with Stage Manager | 20 (status bar) + 28 (window chrome) | 20 | Window chrome adds extra top inset |

**Getting safe area values programmatically**: Use `view.safeAreaInsets` (not `safeAreaLayoutGuide.owningView`). Values are 0 until `viewDidLayoutSubviews`. For SwiftUI, use `GeometryReader { proxy in proxy.safeAreaInsets }`.

### Layout Margins

- **Default**: 16pt on iPhone, 20pt on iPad (horizontal). `view.layoutMargins` yields `UIEdgeInsets(top: 8, left: 16, bottom: 8, right: 16)` on iPhone.
- **Readable content guide**: Maximum width = 672pt on iPad in regular-width size class. Use `view.readableContentGuide` for text-heavy views. This prevents lines from being too long for comfortable reading (>75 chars per line).
- **Respecting margins**: In UIKit, `view.layoutMarginsGuide` anchors content. In SwiftUI, `.padding()` defaults to system margins.
- **Directional layout margins**: Use `directionalLayoutMargins` (`.leading`/`.trailing`) instead of `.left`/`.right` to respect RTL languages.

### Touch Targets

- **Minimum**: 44×44pt (as per Apple HIG). This applies to buttons, table view cells, annotation callouts, and any tappable element.
- **Exceptions**:
  - Inline links within text bodies: 44pt height enforced by `UITextView` link detection region; width = glyph width
  - Segmented controls: each segment must be ≥44pt wide, height fixed at 28pt (compact) or 32pt (regular)
  - Navigation bar items: system enforces 44pt tap area even if visual icon is smaller (extra hit area added automatically for `UIBarButtonItem`)
  - Tab bar items: system-provided 44×48pt tap region centered on icon
- **Edge case testing**: Apple's App Review team uses an automated tap-target checker. Write a UI test with a 44×44pt finger simulator: `XCUIApplication().buttons["myButton"].tap()` — if it fails on a small device, you need more padding.

### Device Size Classes

| Device | Width | Height | Portrait | Landscape |
|---|---|---|---|---|
| iPhone SE – iPhone 15 (non-Plus) | Compact | Compact (except Plus/Max: Regular height) | wC hC → wC hR (Plus/Max) | wC hC |
| iPhone 15 Plus/Pro Max | Compact | Regular (portrait) / Compact (landscape) | wC hR | wR hC |
| iPad (any size) | Regular | Regular | wR hR | wR hR |
| iPad Split View (1/3 width) | Compact | Regular | wC hR | wC hR |
| iPad Slide Over | Compact | Regular | wC hR | — |

**Multitasking changes**: On iPad, sliding another app into Split View changes `traitCollection.horizontalSizeClass` from Regular to Compact in real-time (via `traitCollectionDidChange`). Every layout must handle this transition gracefully — test with all three slide ratios (1/3, 1/2, 2/3).

---

## Navigation Patterns

### Tab Bars
- **3–5 items** max. <3 = use segmented control instead. >5 = add "More" tab (system-generated for overflow). Do NOT scroll tab bar horizontally — it's undiscoverable.
- **Position**: Always at bottom of screen. Never top, never side on iPhone.
- **Icons**: SF Symbols — `.fill` variant for selected tab, outline variant (`.regular`) for unselected. Weight: `.medium` (25×25pt rendered at @2x = 50×50px asset).
- **Badges**: Red circle with white text (single digit) or white "•". Use for actionable counts only (unread messages, pending approvals). Never use as a status indicator.
- **Selection**: Always persist the last selected tab across app restarts (save tab index in `UserDefaults`). On `UITabBarController`, `.moreNavigationController` handles the overflow automatically.

### Hierarchical Navigation (Navigation Bar)
- **Back chevron**: System-provided `<` chevron with the previous screen's title. Override only for brand color (not shape).
- **Large title**: Enabled by default on iOS 11+. Collapses to inline title on scroll (via `UINavigationBar.prefersLargeTitles = true`). Use for top-level screens; disable for drill-down (`.largeTitleDisplayMode = .never`).
- **Search controller**: Attach to `navigationItem.searchController`. Use `.hidesNavigationBarDuringPresentation = true` to maximize results space. Provide scope bar (≤4 scopes) for filtering, not as primary nav.
- **Right bar button items**: Max 2. Give the primary action a filled button style; secondary = plain. Use SF Symbols always. Long-press on a right bar item should never have a hidden action.

### Modal Presentation

| Style | iOS Default | Use Case | Dismiss Gesture |
|---|---|---|---|
| `.pageSheet` (default) | Card from bottom, parent visible behind | Most modals: forms, detail views, compose | Swipe-down (can disable with `isModalInPresentation = true`) |
| `.fullScreen` | Full cover, parent hidden | Immersive content: camera, media player, onboarding | MUST provide clear dismiss button |
| `.formSheet` | Centered card (iPad only) | Settings, login, short forms | Tap outside (iPad) |
| `.popover` | Arrow-anchored bubble (iPad) | Context menus, filter options, info tips | Tap outside |
| `.automatic` | Platform-appropriate default | Let system decide | System-managed |

**Rules**:
- Always provide a clear dismiss affordance — `Cancel`/`Done`/`X` button. Do not rely solely on swipe-to-dismiss.
- If data can be lost on dismiss, set `isModalInPresentation = true` and present an `UIAlertController(.actionSheet)` confirming discard.
- `.fullScreen` without exit button = guaranteed App Store rejection.

### Split Views
- **Primary column** (sidebar/list): ~320pt on iPad, collapses on iPhone
- **Secondary column** (detail): fills remaining width
- **Supplementary column**: optional third column for iPad (e.g., Mail: mailboxes → message list → message content)
- **Collapse behavior**: On compact width (iPhone), the split view collapses to a single navigation stack. Use `splitViewController(_:collapseSecondary:onto:)` to decide which view controller shows first. Return `true` to keep primary; `false` to show secondary first (if detail content exists).
- **Style**: `.tripleColumn` (iOS 14+), `.doubleColumn` (iOS 14+). Older apps use `UISplitViewController.Style`.

---

## Components & Controls

### Buttons

| Style | API | Use Case | Visual |
|---|---|---|---|
| **Filled** (primary) | `.borderedProminent` | Primary action per screen — exactly 1 per view | Filled tint color, white label |
| **Tinted** (secondary) | `.bordered` | Secondary actions, alternatives to primary | Tinted border + text, transparent fill |
| **Gray** | `.bordered` + gray tint | Tertiary, low-emphasis | Gray border + gray text |
| **Plain** | `.plain` | Inline actions, link-like behavior | No background, tint color text only |
| **Destructive** | `.borderedProminent` + `.destructive` role | Delete, sign out, irreversible actions | Red fill, white label |

**Sizes**: `.large` (height ~50pt, prominent actions), `.medium` (default, ~36pt), `.small` (~28pt). Use large only for the single most important action on screen.

**Rules**: One filled button per screen maximum. Use Tinted/Gray for supporting actions. Never nest a button inside a button. Never use buttons as links in body text — use `UITextView` link detection instead.

### Lists

| Style | `.plain` | `.grouped` | `.insetGrouped` (iOS 13+) |
|---|---|---|---|
| Background | White/systemBackground | Light gray/grouped | Inset from edges, rounded corners |
| Separators | Full-width, inset | Full-width between groups | Hidden (cards auto-separate) |
| Use case | Drill-down menus, long lists | Settings screens | Settings (modern), forms |
| Cell style | `.default`, `.subtitle`, `.value1`, `.value2` | Same | Same |

**Swipe actions**: `UIContextualAction` or SwiftUI `.swipeActions(edge:)`. Max 2 actions per side. Style: `.destructive` (red, trailing) or `.normal` (gray, leading). Always provide both a title AND an SF Symbol — the symbol is what shows during the swipe; the title only shows when fully swiped.

**Context menus**: Long-press on a cell → preview (optional) + action list. Available via `UIContextMenuInteraction` or `.contextMenu` in SwiftUI. Include ≤5 actions. Use `.displayInline` for destructive actions. Never hide primary actions behind a context menu — they must also be accessible via tap + swipe.

### Bars

| Bar | Position | Show | Hide |
|---|---|---|---|
| **Status Bar** | Top | `.default` (always visible) | `.none` (fullscreen: camera, media, game) |
| **Navigation Bar** | Below status bar | `isNavigationBarHidden = false` | Fullscreen scroll, camera, immersive |
| **Toolbar** | Bottom (above tab bar if present) | `isToolbarHidden = false` | Default hidden — only for action sets |
| **Tab Bar** | Absolute bottom | Always visible in tab-based apps | Fullscreen browsing (Safari-style translucent) |

**Status bar style**: `.default` (dark content) for light backgrounds, `.lightContent` for dark backgrounds, `.darkContent` (iOS 13+) for light backgrounds. Override per-view-controller via `preferredStatusBarStyle`.

### Alerts vs Action Sheets

| Attribute | Alert (`.alert`) | Action Sheet (`.actionSheet`) |
|---|---|---|
| **Position** | Centered | Bottom (iPhone), popover (iPad) |
| **Max actions** | 2–3 | 3–5+ |
| **Cancel style** | No dedicated cancel button (use `.cancel` style) | `.cancel` style action (always last) |
| **Destructive** | `.destructive` style (red) | `.destructive` style (red) |
| **Use for** | Confirmation, errors, "Are you sure?" | Choice from a list: share target, sort order, delete vs archive |
| **Anti-pattern** | Advertising, upsells, "rate our app" on alert | Single-choice (use action sheet, not alert) |

### Pickers

| Type | API | Use Case | Notes |
|---|---|---|---|
| **Date Picker** `compact` | `.compact` | Single date, tap to expand calendar | Default on iOS 14+. Uses little space. |
| **Date Picker** `inline` | `.inline` | Calendar always visible | Use only in forms with ample vertical space |
| **Date Picker** `wheels` | `.wheels` | Precise date/time selection | Takes ~216pt vertical space. Classic style. |
| **General Picker** | `UIPickerView` / `Picker` | Selecting from ≤20 options | For >20 options, use a table view with search instead |
| **Color Picker** | `UIColorPickerViewController` / `ColorPicker` | Color selection | System-provided eyedropper + favorites. `.supportsAlpha` flag. |

---

## Gestures

### Standard Gestures (System-Provided)

| Gesture | Recognizer | Standard Usage | Do NOT Override For |
|---|---|---|---|
| **Tap** | `UITapGestureRecognizer` | Button press, selection, dismiss keyboard | — |
| **Drag** | `UIPanGestureRecognizer` | Pull-to-refresh, slider, reorder | Pull to dismiss (system modal dismiss) |
| **Swipe** | `UISwipeGestureRecognizer` | List actions, page curl | Everything except specific directional actions |
| **Pinch** | `UIPinchGestureRecognizer` | Zoom in/out (photos, maps) | — |
| **Rotate** | `UIRotationGestureRecognizer` | Map rotation, image editor | Scrolling (often conflicts with pan) |
| **Long Press** | `UILongPressGestureRecognizer` | Context menus, drag-and-drop initiation, text selection | Standard tap behavior |

### Custom vs System Gestures
- **Use system-provided** for: tap, swipe-to-go-back, pinch-to-zoom, pull-to-refresh. These consistent across the OS and users have muscle memory.
- **Use custom gestures** only for: in-app canvas drawing, game controls, custom transitions between in-app states. Even then, prefer `UIGestureRecognizer` subclasses over raw touch handling.
- **Never override globally**: Screen-edge swipe-back (`UIScreenEdgePanGestureRecognizer`, left edge). This is the universal "go back" gesture. If you override it, users get stuck with no way back except reaching for the top-left back button.

### Swipe-Back (Left Edge)
- Managed by `UINavigationController.interactivePopGestureRecognizer`
- To customize: set your view controller as `gestureRecognizer.delegate` and implement `gestureRecognizerShouldBegin`
- To add to a non-navigation use case: add `UIScreenEdgePanGestureRecognizer` with `.left` edge — but only if you're not inside a `UINavigationController`
- **Absolute rule**: the gesture must always result in navigation backward. Never use left-edge swipe for a custom action — it violates the user's expectation that it means "go back."

### Haptic Feedback

| Style | Intensity | Use Case |
|---|---|---|
| `.light` | Subtle tap | Button press, cell selection, toggle switch |
| `.medium` | Noticeable thud | Drag lift, snap-to-place, confirmation |
| `.heavy` | Strong thud | Successful action, error, destructive confirmation |
| `.soft` | Muted | Notification arrival, background state change |
| `.rigid` | Sharp, stiff | Physical object collision, toggle snap |
| `.selection` | — (auto) | Picker wheel detent |
| `.success/warning/error` | — (patterned) | Task completion, validation failure |

**Generator API**: `UIImpactFeedbackGenerator(style: .medium).impactOccurred()`. Create the generator once and reuse — `prepare()` before use to reduce latency (up to 100ms savings). In SwiftUI, `.sensoryFeedback(.success, trigger: didSave)`.

### Long Press → Context Menu (3D Touch Replacement)
- Trigger: `UILongPressGestureRecognizer` with `minimumPressDuration = 0.5` (system default)
- System-provided behavior: preview (peek) + action sheet (pop) on `UIContextMenuInteraction`
- Custom: Use `UIContextMenuConfiguration` with `actionProvider` for dynamic menu items
- Accessibility: All context menu actions MUST also be accessible via a non-long-press path (a button, a swipe action, or VoiceOver rotor action)

---

## Color System

### Semantic Colors (Light/Dark Auto-Adapting)

| Color Name | Light Mode Value | Purpose |
|---|---|---|
| `label` | #000000 (black) | Primary text |
| `secondaryLabel` | #3C3C43 at 60% | Subtitle, description |
| `tertiaryLabel` | #3C3C43 at 30% | Placeholder, disabled text |
| `quaternaryLabel` | #3C3C43 at 18% | Watermark, non-interactive hints |

### Background Colors

| Color | Light Mode | Purpose |
|---|---|---|
| `systemBackground` | #FFFFFF | Root view background |
| `secondarySystemBackground` | #F2F2F7 | Grouped table, secondary surface |
| `tertiarySystemBackground` | #FFFFFF | Nested surface within secondary |

### Grouped Background Colors

| Color | Light Mode | Purpose |
|---|---|---|
| `systemGroupedBackground` | #F2F2F7 | Grouped table background |
| `secondarySystemGroupedBackground` | #FFFFFF | Cell background in grouped table |
| `tertiarySystemGroupedBackground` | #F2F2F7 | Nested cell background |

### Fill Colors

| Color | Opacity | Purpose |
|---|---|---|
| `systemFill` | 20% of `label` | Subtle fill for shapes, SF Symbol backgrounds |
| `secondarySystemFill` | 16% | Softer fill, nested shapes |
| `tertiarySystemFill` | 12% | Very subtle, watermark-like fills |
| `quaternarySystemFill` | 8% | Barely visible fills, hit-area expansion |

### Separator & Link

| Color | Light Mode | Purpose |
|---|---|---|
| `separator` | #3C3C43 at 29% | Table/collection separators |
| `opaqueSeparator` | #C6C6C8 | Opaque alternative for non-blending contexts |
| `link` | #007AFF (system blue) | Hyperlinks, tappable URLs |

### Dark Mode
- All semantic colors auto-adapt — dark mode flips `label` to white (#FFFFFF), `systemBackground` to black (#000000), and adjusts all intermediate colors proportionally
- **Testing**: Simulator → Features → Toggle Appearance (⌘+shift+A). Or in code: `overrideUserInterfaceStyle = .dark`. Or in Settings → Developer → Dark Appearance.
- **Environment override in SwiftUI**: `.preferredColorScheme(.dark)` on any view or `.colorScheme(.dark)` environment value.

### Increased Contrast
- Accessibility setting: Settings → Accessibility → Display & Text Size → Increase Contrast
- `UIColor` provides `accessibilityName` variants that increase opacity when enabled
- Test with `UIAccessibility.isDarkerSystemColorsEnabled` to provide higher-contrast alternatives for custom colors

---

## Iconography (SF Symbols)

### SF Symbols vs Custom Icons

| Factor | SF Symbols | Custom Icons |
|---|---|---|
| Consistency | Matches San Francisco weight & optical size | Must manually match stroke weight, corner radius |
| Dynamic Type | Auto-scales with text | Manual sizing per size class |
| Weight variants | 9 weights (Ultralight → Black) | Must export per weight |
| Rendering modes | Monochrome, Hierarchical, Palette, Multicolor | Single mode |
| Availability | 6000+ symbols (SF Symbols 6) | Unlimited |
| **When to use** | 95% of UI icons: tab bars, nav bars, toolbars, lists, buttons | Brand logos, app icon, unique custom metaphors not in SF Symbols |

### Symbol Scales

| Scale | Use Case | Example Size |
|---|---|---|
| `.small` | Captions, inline with small text | 12–14pt |
| `.medium` | Body text, standard buttons | 17–20pt |
| `.large` | Headlines, prominent buttons | 24–28pt |

### Rendering Modes

| Mode | Behavior | Use Case |
|---|---|---|
| `monochrome` | Single color applied to entire symbol (default) | Tab bars, nav bars — tint color driven by selection state |
| `hierarchical` | Primary color + secondary at 50% opacity | Depth indication: filled section = foreground, lighter = background |
| `palette` | 2–3 explicit colors assigned to symbol layers | Multi-state indicators (e.g., green check + gray circle) |
| `multicolor` | Symbol's baked-in colors (where available) | Weather symbols, folder colors, badge colors |

### Icon Sizes by Context

| Context | Icon Size (pt) | Scale | Asset Size (@3x) |
|---|---|---|---|
| Tab bar | 25×25 | @2x/@3x | 75×75px |
| Navigation bar | 25×25 | @2x/@3x | 75×75px |
| Toolbar | 25×25 | @2x/@3x | 75×75px |
| Home screen quick action | 35×35 | @2x/@3x | 105×105px |
| Table cell (leading) | 29×29 (list) or 40×40 (large) | @2x/@3x | variable |
| Notification/Widget | 60×60 (small), larger for medium/large | @2x/@3x | variable |

### Custom Symbols
- Create in SF Symbols app (available on macOS): import an SVG, set stroke weight, define layer structure for hierarchical/palette rendering
- Export as .svg with annotations → add to Xcode asset catalog as "Symbol Image Set"
- Custom symbols participate in all rendering modes and Dynamic Type scaling if properly annotated

---

## Common App Store Rejections (HIG-Related)

| # | Violation | Fix |
|---|---|---|
| 1 | **Hidden/unclear dismiss on modal flows** | Every modal needs a clear `Cancel`/`Done`/`X` button. Swipe-down alone is not enough — it's undiscoverable for many users. |
| 2 | **Touch targets below 44pt** | Minimum 44×44pt hit area for every interactive element. Use `UIButton.contentEdgeInsets` or `.padding()` to expand invisible hit area without enlarging visual. |
| 3 | **Not respecting safe areas** | Content must not clip under notch, dynamic island, or home indicator. Test on iPhone SE (no safe area bottom) AND iPhone 16 Pro Max (large dynamic island). |
| 4 | **System icons misused** | The share icon (↑) means "share," not "upload." The trash icon means "delete," not "remove from list." The heart icon means "favorite/like," not "health." Misusing system icons = rejection for confusing UX. |
| 5 | **No Dark Mode support** | All screens must be usable in dark mode. If your app has custom colors, provide dark variants via Asset Catalog's "Appearances" setting or `UITraitCollection`-based color resolution. |
| 6 | **Missing/wrong Info.plist usage descriptions** | Every privacy-sensitive API needs a purpose string: `NSCameraUsageDescription`, `NSPhotoLibraryUsageDescription`, `NSBluetoothAlwaysUsageDescription`, `NSLocationWhenInUseUsageDescription`, etc. Description MUST explain WHAT you use it for and WHY — generic text like "This app needs camera access" is rejected. |
| 7 | **Login required before any value** | If your app requires login, show a functional demo/browse mode OR provide demo credentials. Apps that show only a login wall on first launch get rejected under "minimum functionality." |
| 8 | **Placeholder content** | "Lorem ipsum" text, placeholder images, or empty states that say "Coming Soon" without actual content = rejection. Ship real content or hide unfinished features. |
| 9 | **Broken links / dead features** | All buttons must do something. All links must resolve. Every tab must show content. Dead-end screens are rejected. |
| 10 | **Forced rating prompts** | Do NOT use `SKStoreReviewController.requestReview()` on first launch or after every action. iOS limits it to 3× per year per app — use it after positive actions (task completed, level beaten). Never gate functionality behind a rating. |
