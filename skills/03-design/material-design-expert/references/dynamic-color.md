# Dynamic Color (Material You / Monet)
<!-- YAML-style: title: Dynamic Color — Material You (Monet), date: 2026-07-26 -->

## Overview

Dynamic Color (Monet) is Material Design 3's wallpaper-based theming system, available on Android 12+. It extracts a seed color from the user's wallpaper and generates a full tonal palette in the HCT color space, assigning each tone to a Material Design color role. The system guarantees WCAG 2.2 AA contrast (4.5:1) for all text-on-surface combinations out of the box.

---

## How Monet Works (Pipeline)

```
Wallpaper → Seed Color → HCT Color Space → Tonal Palette → Role Assignment
    │            │              │                │               │
    │      Extracted via   Hue (H): 0-360°    5-6 tones       Primary, Secondary,
    │      quantization    Chroma (C): 0-120   per color       Tertiary, Error,
    │      algorithm       Tone (T): 0-100     generated       Surface, Background,
    │                                                     OnPrimary, OnSecondary...
```

### Step 1: Wallpaper Extraction
System samples dominant and accent colors from the current wallpaper using the `WallpaperColors` API. Users can also manually select a theme color from 4 extracted options in the system wallpaper picker.

### Step 2: Seed Color
A single ARGB integer representing the dominant extracted color. This seed drives all palette generation.

### Step 3: HCT Color Space
**HCT (Hue, Chroma, Tone)** is a perceptually uniform color space designed for Material You. Unlike HSL or HSV (which are not perceptually uniform — equal numerical steps do not produce equal perceived changes), HCT enables automatic contrast guarantees.

| Component | Range | Description |
|-----------|-------|-------------|
| **Hue (H)** | 0°–360° | The "color" — red, blue, green, etc. Matches HSL hue. |
| **Chroma (C)** | 0–120+ | Color intensity / saturation. 0 = gray, 120+ = maximum vividness. |
| **Tone (T)** | 0–100 | Perceived lightness. 0 = pure black, 100 = pure white, 50 = middle gray. This is what maps to MD3 color roles. |

### Step 4: Tonal Palette Generation
For each key color (Primary, Secondary, Tertiary, Error, Neutral, Neutral Variant), the system generates a full tonal palette — colors at tones 0, 10, 20, ..., 90, 95, 98, 99, 100. Algorithms used:
- `TonalPalette.fromHueAndChroma(hue, chroma)` — generates the palette
- `SchemeTonalSpot` — default MD3 scheme, prioritizes tonal variety
- `SchemeContent` — higher chroma, vibrant accent-heavy scheme
- `SchemeVibrant` — even higher chroma, saturated look
- `SchemeExpressive` — maximal chroma, colorful UI
- `SchemeNeutral` — low chroma, muted
- `SchemeMonochrome` — grayscale
- `SchemeFidelity` — closest to seed color

### Step 5: Role Assignment
Each MD3 color role maps to a specific tone in the generated palette. See the role-to-tone table below.

---

## Tonal Palette: Complete Role-to-Tone Mapping

### Light Theme

| Color Role | Tone | Usage |
|-----------|------|-------|
| **Primary** | 40 | Key brand color. FAB, active navigation, primary buttons, switches, sliders. |
| **On Primary** | 100 | Text/icons on Primary surfaces. |
| **Primary Container** | 90 | Subtle primary-tinted container (chips, cards with primary association). |
| **On Primary Container** | 10 | Text/icons on Primary Container. |
| **Secondary** | 40 | Less prominent accent. Filter chips, toggle buttons, secondary actions. |
| **On Secondary** | 100 | Text/icons on Secondary surfaces. |
| **Secondary Container** | 90 | Tinted surface for secondary emphasis. |
| **On Secondary Container** | 10 | Text/icons on Secondary Container. |
| **Tertiary** | 40 | Complementary accent (teal/cyan if primary is blue). Date picker selection, input field focus. |
| **On Tertiary** | 100 | Text/icons on Tertiary surfaces. |
| **Tertiary Container** | 90 | Complementary tinted container. |
| **On Tertiary Container** | 10 | Text/icons on Tertiary Container. |
| **Error** | 40 | Error messages, destructive actions, red indicators. |
| **On Error** | 100 | Text/icons on Error surfaces. |
| **Error Container** | 90 | Error message background, subtle error state. |
| **On Error Container** | 10 | Text/icons on Error Container. |
| **Surface Dim** | 87 | Lowest elevation surface (behind all content). |
| **Surface** | 98 | Default background surface. Cards, sheets, dialogs. |
| **Surface Bright** | 98 | Brightest surface (highest elevation). |
| **Surface Container Lowest** | 100 | Resting state container. |
| **Surface Container Low** | 96 | Subtly elevated container. |
| **Surface Container** | 94 | Default elevated surface. Navigation drawers, side sheets. |
| **Surface Container High** | 92 | Further elevated (modals, dialogs). |
| **Surface Container Highest** | 90 | Most elevated (overlays). |
| **On Surface** | 10 | Primary text on all surfaces. |
| **On Surface Variant** | 30 | Secondary text, captions, metadata. |
| **Outline** | 50 | Borders, dividers, text field outlines. |
| **Outline Variant** | 80 | Subtle dividers, decorative borders. |
| **Inverse Surface** | 20 | Surface for elements that need dark background in light theme (tooltips, snackbar). |
| **Inverse On Surface** | 95 | Text on Inverse Surface. |
| **Inverse Primary** | 80 | Primary color that works on Inverse Surface (snackbar action). |
| **Scrim** | #000000 + opacity | Modal scrim / backdrop overlay. |
| **Shadow** | #000000 + opacity | Elevation shadow. |

### Dark Theme

| Color Role | Tone | Usage |
|-----------|------|-------|
| **Primary** | 80 | Key brand color in dark theme. |
| **On Primary** | 20 | Text/icons on Primary surfaces. |
| **Primary Container** | 30 | Subtle primary container. |
| **On Primary Container** | 90 | Text/icons on Primary Container. |
| **Secondary** | 80 | Accent in dark theme. |
| **On Secondary** | 20 | Text/icons on Secondary. |
| **Secondary Container** | 30 | Secondary tinted container. |
| **On Secondary Container** | 90 | Text/icons on Secondary Container. |
| **Tertiary** | 80 | Complementary accent. |
| **On Tertiary** | 20 | Text/icons on Tertiary. |
| **Tertiary Container** | 30 | Tertiary tinted container. |
| **On Tertiary Container** | 90 | Text/icons on Tertiary Container. |
| **Error** | 80 | Error states in dark. |
| **On Error** | 20 | Text/icons on Error. |
| **Error Container** | 30 | Error background. |
| **On Error Container** | 90 | Text on error container. |
| **Surface Dim** | 6 | Lowest dark surface. |
| **Surface** | 6 | Default dark background. |
| **Surface Bright** | 24 | Brighter surface in dark (cards, sheets). |
| **Surface Container Lowest** | 4 | Darkest container. |
| **Surface Container Low** | 10 | Slightly elevated container. |
| **Surface Container** | 12 | Default elevated surface. |
| **Surface Container High** | 17 | Elevated container. |
| **Surface Container Highest** | 22 | Most elevated container. |
| **On Surface** | 90 | Primary text on dark surfaces. |
| **On Surface Variant** | 80 | Secondary text. |
| **Outline** | 60 | Borders and dividers. |
| **Outline Variant** | 30 | Subtle dividers. |
| **Inverse Surface** | 90 | Light surface for inverse elements. |
| **Inverse On Surface** | 20 | Text on Inverse Surface. |
| **Inverse Primary** | 40 | Primary color on Inverse Surface. |
| **Scrim** | #000000 + opacity | Modal overlay. |
| **Shadow** | #000000 (no shadow in dark) | Shadows invisible in dark theme — use Surface elevation tones instead. |

---

## Contrast Guarantees

### Automatic AA (4.5:1) Contrast
Dynamic Color guarantees WCAG 2.2 Level AA for all text-on-surface color pairs:
- `onSurface` on `surface` (tone 10 on 98 = 4.5:1+ guaranteed)
- `onPrimaryContainer` on `primaryContainer` (tone 10 on 90 = 4.5:1+ guaranteed)
- Same for Secondary, Tertiary, Error variants

The HCT color space enables this automatically — Tone maps directly to perceived lightness, so contrast ratios are deterministic.

### AAA (7:1) Contrast
The `SchemeTonalSpot` constructor accepts a `contrastLevel` parameter:

| Contrast Level | Minimum Ratio | When to Use |
|---------------|---------------|-------------|
| `0.0` (default) | 4.5:1 (AA) | Standard use. |
| `0.5` | ~7:1 | Higher contrast for readability. |
| `1.0` | ~10:1 | Maximum contrast. Accessibility-focused. |
| `-1.0` (reduced) | ~3:1 | Expressive, low-contrast aesthetic. Use with caution — not accessibility-compliant. |

```kotlin
val hct = Hct.fromInt(seedColorArgb)
val highContrastScheme = SchemeTonalSpot(hct, isDark = false, contrastLevel = 0.5)
```

---

## Implementation Patterns

### Pattern 1: Automatic (Android 12+, App-Wide)
```kotlin
// In Activity.onCreate() — simplest integration
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        DynamicColors.applyToActivityIfAvailable(this)
        setContent { App() }
    }
}
```

### Pattern 2: XML Theme (Views)
```xml
<!-- res/values/themes.xml -->
<style name="Theme.MyApp" parent="Theme.Material3.DynamicColors.DayNight">
    <!-- All MD3 roles are automatically populated from wallpaper -->
</style>
```

### Pattern 3: Manual Seed (material-color-utilities)
```kotlin
// Programmatic control — useful for brand override
import com.google.android.material.color.utilities.Hct
import com.google.android.material.color.utilities.SchemeTonalSpot

val seedColor = Color.parseColor("#6750A4") // M3 default purple
val hct = Hct.fromInt(seedColor)
val scheme = SchemeTonalSpot(hct, isDark = false, contrastLevel = 0.0)

val colorScheme = ColorScheme(
    primary = Color(scheme.primary),
    onPrimary = Color(scheme.onPrimary),
    primaryContainer = Color(scheme.primaryContainer),
    // ... map all 24+ roles
)
MaterialTheme(colorScheme = colorScheme) { App() }
```

### Pattern 4: Compose (dynamicColor)
```kotlin
// Jetpack Compose — simplest declarative approach
MaterialTheme(
    colorScheme = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
        dynamicLightColorScheme(LocalContext.current)
    } else {
        lightColorScheme() // Fallback for pre-12
    }
) { App() }
```

---

## When NOT to Use Dynamic Color

| Scenario | Why | Mitigation |
|----------|-----|-----------|
| **Brand-heavy apps** | Dynamic Color can replace brand colors (Spotify green → wallpaper-derived green). Brand recognition lost. | Override `primary` only. Keep other roles dynamic: `colorScheme.copy(primary = brandColor)`. |
| **Games** | Dynamic palettes don't match game aesthetics. Need deliberate mood-setting color design. | Use custom `ColorScheme` with a fixed palette. |
| **Cross-platform apps** | iOS/Web don't have Monet. Inconsistent brand identity across platforms. | Use static `lightColorScheme()` / `darkColorScheme()` with shared brand token values. |
| **Medical / healthcare** | Color carries semantic meaning (red = critical, green = normal). Dynamic Color may reassign these arbitrarily. | Use `SchemeContent` with a fixed brand seed + semantic colors for status indicators. |
| **Enterprise with white-label** | Each client needs their own exact brand palette. | Use `SchemeTonalSpot` with each client's brand seed. Do NOT use `DynamicColors.applyToActivityIfAvailable`. |

---

## Testing Dynamic Color

### Test Matrix (Minimum)
Test with 5+ dramatically different wallpapers to ensure your UI is legible in all scenarios:

| Wallpaper Type | Hue Range | Risk |
|---------------|-----------|------|
| Sunset (warm) | 0–30° (red/orange) | Primary Container may clash with warm-themed content. |
| Forest (cool) | 120–180° (green/teal) | Secondary may become very similar to Primary. |
| Snow (neutral) | Low chroma, near-white | All colors may appear washed out — ensure sufficient chroma for interactive elements. |
| Neon (saturated) | High chroma (80+) | Overly vivid accent colors may overwhelm content. |
| Monochrome (grayscale) | None (achromatic) | System falls back to default M3 palette. Verify fallback is acceptable. |

### Test Per Wallpaper
- [ ] Light theme variant
- [ ] Dark theme variant
- [ ] Contrast check: `md3_checker.py` or Accessibility Scanner on all text-on-surface combinations
- [ ] Component stress test: Cards, FAB, chips, text fields, switches, dialogs — all must be distinguishable
- [ ] Screenshot review: Do brand elements remain identifiable?

### Validation Script
```python
# md3_checker.py — verify contrast for key pairs
# Usage: python3 md3_checker.py --primary #FF6600 --is-dark false
# Output: contrast ratios for all 24+ role pairs
```

---

## Fallback for Pre-Android-12

When `DynamicColors.applyToActivityIfAvailable` is unavailable (API < 31):

```kotlin
// Compose fallback
val colorScheme = when {
    Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> dynamicLightColorScheme(context)
    else -> lightColorScheme(
        primary = Color(0xFF6750A4),       // M3 default purple
        onPrimary = Color(0xFFFFFFFF),
        primaryContainer = Color(0xFFEADDFF),
        onPrimaryContainer = Color(0xFF21005D),
        // ... all roles
    )
}
MaterialTheme(colorScheme = colorScheme) { App() }
```

Alternatively, use `SchemeContent(hct, isDark, contrastLevel)` with a brand seed for a consistent static palette that still follows MD3 tonal logic.
