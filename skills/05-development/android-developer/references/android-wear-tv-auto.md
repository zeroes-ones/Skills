# Android Extended Form Factors — Wear OS, Android TV, Android Auto

> Deep-dive reference loaded on demand by `android-developer`. Real users meet your app on
> watches, TVs, and in the car — these form factors share the phone's codebase but each has
> its own design language, hardware constraints, and release channel. Think like an engineer
> who shipped one app to five screens: the phone is the hub, and every other surface is a
> focused, glanceable extension of it.

## 0. Core Mental Model

| Form factor | User context | Design rule | Primary constraint |
|-------------|--------------|-------------|-------------------|
| **Wear OS** | 1-5 second glances, one hand, small wrist | Glanceable: one task per screen, big text, minimal taps | Battery, tiny screen, no keyboard |
| **Android TV** | 10-foot UI, remote (D-pad) navigation, shared screen | Focus-based navigation, 10-foot legibility, no touch | D-pad only, overscan, TV audio |
| **Android Auto** | Driving — eyes on road, hands on wheel | Zero-interaction design; templates do the thinking | Driver distraction (NHTSA guidelines), no video/text |

**Never design the phone app "down" to the watch or "up" to the TV.** Each form factor gets its
own information architecture and interaction model; the shared layer is data, domain logic, and
accounts — not UI.

## 1. Wear OS

### Project setup
- Wear OS apps are a separate module (`:wear`) with `org.jetbrains.kotlin.plugin.compose` +
  Wear Compose (`androidx.wear.compose:compose-material`), **not** phone Material 3.
- Manifest: `<uses-feature android:name="android.hardware.type.watch" />`; target round and
  square screens; `androidx.wear` tiles + complications libs.
- Phone and watch apps are separate APKs installed together from one Play listing (wear app
  bundled under the phone's release).

### UI patterns (Wear Compose)
- **Screens:** `Scaffold` with `TimeText` + `PositionIndicator` (scroll), `ScalingLazyColumn`
  for lists — the Wear-native scroll that scales/fades items at edges.
- **One task per screen.** Split a phone form into a wizard of single-choice screens rather
  than one dense form. Watch users tap, they don't type — offer chips and choices.
- **Text sizes:** 12sp minimum body, ~24sp headlines; contrast on OLED. Never rely on color
  alone (watch faces have huge ambient-brightness variance).
- `curvedText` and the curve layout only when it aids glanceability — decoration that costs
  legibility is a bug on a watch.

### Tiles, Complications, Watch Faces
- **Tiles** (swipe-right surface): update via `TileService`; each tile ≤ 3-5 glanceable data
  points; refresh with `Scheduler`/`WorkManager`, never a polling loop.
- **Complications** (data shown on watch faces): implement `ComplicationProviderService`;
  support the 5 types (short text, long text, ranged value, small/large image). Keep the
  update cadence honest — every write wakes the watch face.
- **Watch faces** use `WatchFaceService` + `Canvas`/Compose; watch-face and app complications
  are how users actually keep your data visible. A health/fitness app without a complication
  is invisible on the wrist.

### Connectivity
- **Watch ↔ phone:** `WatchConnectivity` (`MessageClient`, `DataClient`, `CapabilityClient`).
  Prefer `MessageClient` for request/response, `DataClient` for state sync; handle the watch
  being offline (phone out of range) — never block on a phone round-trip.
- **Standalone-first:** modern Wear apps should work without the phone (own network via
  `NetworkRequest` on LTE/Wi-Fi). Design phone-sync as an enhancement, not a requirement.
- Health: `HealthServices` (passive/active data) with permission flows; respect user privacy —
  health data is the most sensitive data on the device.

## 2. Android TV

### Project setup
- TV module with `androidx.leanback` or Jetpack Compose for TV (`androidx.tv` material
  components). Manifest: `<uses-feature android:name="android.software.leanback" android:required="false" />`
  + `android.software.touchscreen` NOT required.
- Banner/icon assets: 320x180 px banner required for Play; launcher icons at TV sizes.

### Interaction model (D-pad / 10-foot)
- **Focus is the cursor.** Every screen must be navigable with D-pad: focus states on every
  card, no hover-dependent actions, no scroll-wheel assumptions.
- `LazyRow`/`LazyColumn` with `Modifier.focusable()`, `rememberSaveable` for focus position;
  `FocusRequester` for initial focus and search.
- **Legibility:** body text ≥ 18-20sp from 10 feet; high contrast; overscan-safe margins
  (Android TV adds its own overscan — keep critical UI inside the safe zone).
- **Audio:** route media through `MediaSession`/`Media3` so the TV remote and system UI
  control playback; respect audio focus.

### Content patterns
- Content discovery is a **browse-and-preview** loop: rows of cards (continue watching,
  recommendations via `WatchNext`), not dense lists. Preview content on focus (hero image +
  trailer/metadata) — this is how people actually decide what to watch.
- Search with voice (`SearchManager`/`RecognizerIntent`); recommendations via
  `Recommendation`/`WatchNextChannel` only if the user opted into them.
- Games/leanback: input via game controller; follow the TV game checklist (no touch, support
  pause, handle controller disconnect).

## 3. Android Auto

### Rules that are not optional
- **Driver distraction is the design constraint.** Use only the approved `Car App Library`
  templates (media, messaging, navigation, parking, IoT, calendar). Custom interactive UI is
  **not permitted** — Auto renders your app inside its own templates.
- **No text entry while driving**, no video, no scrollable lists of text. Messages use the
  template's suggested-reply flow; navigation uses the template's map surface.
- Build for **categories**: media (`MediaBrowserService`/`MediaSession` + `androidx.car.app`
  media templates), messaging (`MessagingService` with reply templates), navigation
  (`NavigationManager` with `Place` + surface callbacks), and IoT (`CarAppService`).

### App structure
- `CarAppService` → `Session` per category; templates render on the head unit. The phone app
  supplies the service; test on a phone with the desktop head unit (DHU) before hitting a car.
- Handle **driving state transitions**: app must function from a stopped state and re-enter
  safely; never resume a video or drop the user mid-navigation when the car moves.
- Keep media playback stable across reconnects (the head unit disconnects/reconnects
  constantly); persist session state, don't rely on the connection.

## 4. Release, Testing & Common Traps

### Release channels
- **Wear OS:** release the wear APK under the phone app's Play listing (same package family);
  test with the Wear emulator + a real device (sensors, battery, ambient mode are real-only).
- **Android TV:** separate Play listing; requires leanback feature, banner, and TV screenshots.
- **Android Auto:** app review category approval — Google reviews the app against the driver
  distraction guidelines before it appears on head units. Budget review time into the release.

### Testing checklist
- [ ] Watch: round + square emulators AND a physical device; ambient mode; complications on 2+
  watch faces; watch offline (no phone) flows.
- [ ] TV: D-pad-only walkthrough of every screen (no touch); focus states; 10-foot legibility;
  overscan-safe margins; remote back/home handling.
- [ ] Auto: DHU (desktop head unit) for every template; driving-state transitions; reconnect
  mid-playback; message reply flow without text entry.

### War stories
- **The phone form on a watch:** An onboarding form rendered "faithfully" on Wear required 14
  scroll-screens and a keyboard. Rebuilt as 3 single-choice screens with chips — completion
  went from 12% to 71%. Lesson: shrink the task, not the layout.
- **The TV app that assumed a mouse:** Cards revealed actions on hover; on a D-pad there is no
  hover, so half the app was unreachable. Lesson: design the focus graph first, then the visuals.
- **The Auto app that failed review:** A media app with custom controls was rejected against
  the driver-distraction guidelines; the rebuild on media templates passed in one round.
  Lesson: read the category templates before writing any UI code.
