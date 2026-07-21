---
name: mobile-developer
description: Cross-platform mobile development with React Native and Flutter, navigation patterns, state management, offline-first architecture, push notifications, platform-specific patterns, and app store deployment. Trigger: mobile, React Native, Flutter, navigation, offline-first, push notifications, app store, iOS, Android.
author: Sandeep Kumar Penchala
type: development
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - mobile-developer
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
---
# Mobile Developer

Build production mobile applications — spanning native (Swift/Kotlin), React Native (Expo), and Flutter — with deep expertise across the full development lifecycle. This skill covers decision frameworks for choosing the right technology, architecture patterns, platform-specific design systems (iOS HIG, Material Design 3), offline-first data synchronization, performance optimization to 60fps, security hardening, CI/CD pipeline design, and App Store/Google Play deployment.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Choosing between native (Swift/Kotlin), React Native, Flutter, or PWA for a new mobile project
- Designing navigation architecture (stack, tab, drawer, deep linking, universal links, deferred deep links)
- Implementing state management (Zustand, TanStack Query, Riverpod, BLoC) and local persistence layers
- Building offline-first applications with conflict resolution (CRDT, last-write-wins, operational transform)
- Integrating push notifications (FCM, APNs, Expo Push) with deep-link routing and rich media attachments
- Handling platform-specific design conventions, permissions, biometrics, and hardware APIs
- Profiling and optimizing cold start time, scroll performance (60fps), memory usage, and binary size
- Setting up CI/CD pipelines for TestFlight, App Store, Google Play, and over-the-air updates
- Setting up CI/CD pipelines for TestFlight, App Store, Google Play, and over-the-air updates
- Implementing security: certificate pinning, secure storage, code obfuscation, root/jailbreak detection

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Offline-First Strategy
```
                     ┌──────────────────────────────┐
                     │ START: Offline support level?│
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Is real-time data critical (chat,       │
              │ live tracking, trading)?                │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ Online-first:    │    │ Can users create/     │
        │ Cache for speed, │    │ edit data offline?   │
        │ not availability.│    └──┬───────────────┬───┘
        │ Show stale data  │       │ YES           │ NO
        │ with indicator.  │       ▼               ▼
        └──────────────────┘ ┌────────────┐  ┌───────────┐
                             │ Full       │  │ Read-only │
                             │ offline-   │  │ offline:  │
                             │ first with │  │ cache API │
                             │ local DB + │  │ responses │
                             │ sync queue │  │ + assets  │
                             └────────────┘  └───────────┘
```
**When full offline-first:** Field workers, travelers, areas with unreliable connectivity. Users must create/edit data offline. Conflict resolution needed.  
**When read-only offline:** Content consumption app (news, docs, media). Users don't create data. Pre-cache on WiFi, serve from local when offline.

### Navigation Architecture
```
                     ┌──────────────────────────────┐
                     │ START: Navigation pattern?   │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ App has 5+ main sections with deep     │
              │ linking to detail screens?             │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ Tab navigator    │    │ Simple stack or      │
        │ with nested      │    │ single-screen flow   │
        │ stacks per tab.  │    │ (< 4 screens)?      │
        │ React Navigation │    └──┬───────────────┬───┘
        │ or GoRouter.     │       │ YES           │ NO
        └──────────────────┘       ▼               ▼
                            ┌────────────┐  ┌──────────────┐
                            │ Stack      │  │ Tab + Stack  │
                            │ navigator  │  │ + Drawer.    │
                            │ with deep  │  │ Full deep    │
                            │ linking    │  │ link support │
                            └────────────┘  └──────────────┘
```
**When Tab + Stack:** Instagram/YouTube pattern. 3-5 top-level sections. Each tab has its own navigation history. Deep linking into nested screens required.  
**When Stack only:** Linear flows (onboarding, checkout wizard, setup). No persistent bottom navigation. Each screen leads to the next or back.

### Push Notification Strategy
```
                     ┌───────────────────────────────┐
                     │ START: Notification approach? │
                     └──────────────┬────────────────┘
                                    │
              ┌─────────────────────▼─────────────────────┐
              │ Is this a real-time messaging app         │
              │ (chat, live events)?                      │
              └────┬──────────────────────┬───────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌────────────────────────┐
        │ FCM/APNs data-   │    │ Notifications are      │
        │ only payload +   │    │ marketing or re-       │
        │ in-app WebSocket │    │ engagement triggers?   │
        │ for actual data. │    └──┬─────────────────┬───┘
        │ Decouple push    │       │ YES             │ NO
        │ from content.    │       ▼                 ▼
        └──────────────────┘ ┌────────────┐  ┌──────────────┐
                             │ FCM/APNs   │  │ Local        │
                             │ with deep  │  │ notifications│
                             │ link +     │  │ only.        │
                             │ rich media │  │ Scheduled    │
                             │ + analytics│  │ reminders.   │
                             └────────────┘  └──────────────┘
```
**When data-only + WebSocket:** Real-time chat/messaging. Push delivers wake-up signal; actual content fetched via persistent connection. Avoids 4KB APNs limit.  
**When FCM/APNs with deep link:** Transactional alerts, marketing. Notification tappable → deep link to relevant screen. Rich media (images, video thumbnails) for engagement.

### State Management
```
                     ┌──────────────────────────┐
                     │ START: State solution?   │
                     └───────────┬──────────────┘
                                 │
              ┌──────────────────▼──────────────────┐
              │ Does state come from an API?        │
              └────┬────────────────────┬───────────┘
                   │ YES                │ NO
                   ▼                    ▼
        ┌──────────────────┐  ┌──────────────────────┐
        │ TanStack Query / │  │ Shared across        │
        │ Riverpod Future  │  │ screens (auth,       │
        │ for server-state │  │ theme, prefs)?       │
        │ caching + refetch│  └──┬───────────────┬───┘
        └──────────────────┘     │ YES           │ NO
                                 ▼               ▼
                          ┌────────────┐  ┌──────────────┐
                          │ Zustand /  │  │ Local state: │
                          │ Riverpod   │  │ useState /   │
                          │ (global)   │  │ BLoC /       │
                          │            │  │ Provider     │
                          └────────────┘  └──────────────┘
```
**When TanStack Query:** API-driven data that needs caching, pagination, and optimistic updates. Server is source of truth. Background refetch on focus.  
**When Zustand/Riverpod:** Client-only global state (auth token, theme mode, feature flags). Cross-screen persistence without API round-trip. Lightweight (< 5KB).

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 0 (~15 min): Native vs Cross-Platform Decision Framework

Before writing a single line of code, select the right technology for the job. The wrong choice can cost months of rework.

**Choose Native (Swift/SwiftUI + Kotlin/Jetpack Compose) when:**
- GPU-intensive rendering is required (games, AR/VR, real-time video processing, Metal/Vulkan access)
- Complex, chained animations must run at 60fps on low-end devices — cross-platform animation bridges add 2-8ms overhead per frame
- Heavy hardware integration: Bluetooth LE peripheral mode, NFC with custom APDUs, Camera2/Core Image pipelines, Core Motion sensor fusion at 100Hz+
- Platform-specific UX is a competitive advantage (e.g., fitness app using HealthKit, banking app needing per-platform trust signals)
- Team has dedicated iOS and Android engineers — dual-platform codebases diverge naturally; fighting a cross-platform abstraction layer adds friction, not velocity

**Choose React Native when:**
- App is content-heavy with standard UI patterns: feeds, lists, forms, CRUD, dashboards
- Team has React/TypeScript expertise — reuse 60-80% of code; the remaining 20-40% is platform-specific (navigation feel, haptics, permissions, native modules)
- Time-to-market is critical: single codebase for MVP, prove product-market fit, then optimize native modules incrementally
- OTA updates are needed: CodePush/expo-updates let you ship JS bundle changes without app store review (Apple allows this for non-native changes per guideline 4.7)
- Anti-pattern: Don't use React Native for apps requiring complex gesture handling (3+ simultaneous gesture recognizers), background audio processing, or per-frame video manipulation — the JS-Native bridge bottleneck still applies even with JSI/Fabric

**Choose Flutter when:**
- Pixel-perfect custom UI that must look identical on iOS and Android — Flutter's Skia/Impeller rendering engine draws every pixel; no platform UI component mapping
- Complex custom animations: Flutter's animation framework provides 60fps out of the box with no bridge overhead (all rendering is on the GPU thread)
- Team lacks web/React background — Dart is easier to learn than React's hooks/JSX paradigm for developers coming from Java/Kotlin/Swift
- Target includes desktop (macOS, Windows, Linux) or web alongside mobile — single Flutter codebase for all four platforms
- Anti-pattern: Avoid Flutter for apps that must feel deeply "platform-native" (heavy OS integration, complex share sheets, platform-specific text selection behavior) — Flutter's custom rendering means platform conventions must be manually recreated

**Performance comparison (real-world benchmarks on mid-range device, iPhone 12 / Pixel 6 equivalent):**

| Metric | Native (Swift/Kotlin) | React Native (Fabric) | Flutter (Impeller) | PWA |
|--------|----------------------|----------------------|--------------------|-----|
| Cold start (ms) | 300-600 | 800-1500 | 600-1000 | 1500-3000 |
| 60fps scrolling | Guaranteed | OK with FlatList/FlashList | Guaranteed | Variable |
| Binary size (MB) | 15-30 | 20-40 (Expo: +10) | 15-25 | 0 (browser) |
| Memory baseline (MB) | 30-60 | 60-120 | 40-80 | 50-150 |
| Native API access | Complete | Via native modules | Via platform channels | Limited |

### Phase 1 (~15 min): Project Scaffolding & Architecture

**Clean Architecture Layers (applies to all frameworks):**
- **Presentation layer**: Screens, widgets, UI components. Depends on Domain layer. Contains no business logic — only UI state transformation and event delegation.
- **Domain layer**: Use cases, entities, repository interfaces. Pure Dart/Swift/Kotlin/TypeScript — zero framework imports. This layer is the source of truth for what the app *does*.
- **Data layer**: Repository implementations, data sources (remote API, local DB, cache), DTOs with mappers to domain entities. Handles serialization, error mapping, pagination.

**React Native + Expo (recommended for 90% of RN projects):**
```bash
npx create-expo-app@latest --template tabs  # expo-router with tab navigation
```
- Use Expo SDK managed workflow. Eject to bare workflow (expo prebuild) ONLY when: you need a native module not in Expo's module ecosystem, custom Metal/Vulkan rendering, or Bluetooth LE peripheral mode.
- TypeScript strict mode: `strict: true` in tsconfig. Zero `any` types in domain/data layers.
- Folder structure (feature-based, scalable to 50+ screens):
  ```
  src/
    app/              # expo-router file-based routes
    features/
      auth/
        screens/      # LoginScreen, SignupScreen, ForgotPasswordScreen
        components/   # AuthForm, SocialLoginButton, BiometricPrompt
        hooks/        # useAuth, useBiometric
        services/     # authService.ts (API calls)
        types.ts      # LoginRequest, AuthToken, User
        __tests__/    # unit + integration
    shared/
      components/     # Button, TextInput, Card, BottomSheet — design system
      hooks/          # useNetworkStatus, useDebounce, useAppState
      utils/          # formatDate, haptics, platformSelect
      types/          # shared domain types
    services/         # apiClient, secureStorage, analytics
  ```

**Flutter (using very_good_cli):**
```bash
very_good create my_app --org com.company --platforms ios,android
```
- Layered architecture: `lib/features/<feature>/` with `data/`, `domain/`, `presentation/` subdirectories
- Dependency injection: use `get_it` + `injectable` (code generation) for a compile-time-safe service locator; avoid `provider` for DI — it's a state management solution, not a DI container
- Environment configuration: `flutter_dotenv` with `.env.development`, `.env.staging`, `.env.production`. Use Dart define flags (`--dart-define=ENVIRONMENT=staging`) for compile-time constants; env files for runtime config only.

**Monorepo structure (when sharing code with web/backend):**
```
packages/
  api-client/        # Shared API types, fetch wrapper, error types
  ui/                # Shared design tokens, if cross-platform component library
  utils/             # Date formatting, validation, constants
apps/
  mobile/            # React Native / Flutter mobile app
  web/               # Next.js web app (if applicable)
```
Use `turborepo` for task orchestration — it caches build outputs and only rebuilds changed packages.

### Phase 2 (~30 min): Navigation & Deep Linking

**Architecture decision: file-based vs programmatic routing**
- **File-based** (expo-router, go_router with ShellRoute): best for standard navigation patterns; co-location of routes with screens; automatic type generation
- **Programmatic** (React Navigation imperative, Navigator 2.0): when navigation depends on complex runtime state (multi-step wizards that branch, role-based navigation trees, deep link handling with conditional redirects)

**Navigation patterns — when to use each:**
| Pattern | Use case | Anti-pattern |
|---------|----------|--------------|
| Tab Bar (bottom) | 3-5 top-level destinations, flat hierarchy | Don't nest tab bars (bottom tabs + top tabs in same flow = confusing) |
| Stack (push/pop) | Hierarchical drill-down, forms, detail screens | Don't go deeper than 5 levels — use modal for sub-flows |
| Drawer | 5+ destinations, secondary navigation, settings | Not for primary navigation on phones; OK on tablets |
| Modal | Focused task, create/edit flows, alerts requiring action | Don't stack modals — max 1 modal deep |

**Deep linking — production-grade configuration:**
```typescript
// expo-router deep link configuration (app.json)
{
  "scheme": "myapp",
  "associatedDomains": ["applinks:myapp.com"],  // iOS universal links
  "intentFilters": [{                            // Android app links
    "action": "VIEW",
    "autoVerify": true,
    "data": [{ "scheme": "https", "host": "myapp.com" }]
  }]
}
```
- Map every route to a URL path: `product/:id` → `myapp://product/123`
- Deferred deep links: use Branch/AppFlyer for install attribution — user clicks link, installs app, opens to target screen on first launch
- Test deep links: `xcrun simctl openurl booted "myapp://product/123"` (iOS), `adb shell am start -W -a android.intent.action.VIEW -d "myapp://product/123"` (Android)

**Authentication flow (zero-flash pattern):**
1. On app launch, show native splash screen (not a JS/Flutter loading screen — uses launch screen storyboard/xib)
2. Check stored auth token while splash is showing
3. If token exists: validate with server (non-blocking), navigate to main app
4. If no token: navigate to auth stack
5. Hide splash ONLY after navigation target is determined — this prevents the "flash of wrong screen"
6. On logout: clear all cached data, navigate to auth stack with `reset` (no back button to main app)

### Phase 3 (~20 min): State Management & Offline-First Data Layer

**State management taxonomy — choose the right tool for each state category:**

| State Type | React Native | Flutter | Characteristics |
|------------|-------------|---------|-----------------|
| Server state | TanStack Query | Riverpod + AsyncValue | Cached, eventually consistent, paginated |
| Client/global | Zustand | Riverpod StateNotifier | Shared across screens, persisted |
| Form state | React Hook Form + Zod | flutter_form_builder + formz | Ephemeral, validation-heavy |
| UI ephemeral | useState/useReducer | StatefulWidget/ValueNotifier | Single component, discarded on unmount |
| Navigation state | expo-router (built-in) | go_router (built-in) | URL-derived, type-safe params |
| Persistent/local DB | WatermelonDB, MMKV | Isar, Drift | Source of truth for offline-first |

**Offline-first architecture — the definitive approach:**

The golden rule: **local database is the source of truth; the server is a backup.** Never code as if the network is always available.

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  UI Layer   │ ←──→│ Domain Layer │ ←──→│  Repository │
│ (screens)   │     │ (use cases)  │     │   (facade)  │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                          ┌────┴────┐
                                    ┌─────┴────┐ ┌──┴──────────┐
                                    │ Local DB │ │ Remote API   │
                                    │ (primary)│ │ (secondary)  │
                                    └──────────┘ └──────────────┘
                                          │              │
                                          └── Sync ──────┘
```

**Sync strategy selection:**

| Strategy | When to use | Conflict handling | Example |
|----------|------------|-------------------|---------|
| Last-write-wins (LWW) | Single-user apps, non-collaborative data | Timestamp comparison | Note-taking app, settings sync |
| CRDT (Conflict-free Replicated Data Types) | Multi-user collaboration, offline editing | Automatic merge via CRDT semantics | Google Docs-style editor, shared task lists |
| Operational Transform (OT) | Real-time collaboration with central server | Server-mediated transformation | Google Docs (original), text editors |
| Delta sync | Large datasets, batch updates | Server as authority, client replays missing deltas | Calendar sync, email sync |

**Sync queue implementation pattern (React Native example):**
```typescript
// 1. User performs mutation → written to local DB immediately + queued
async function updateTodo(todo: Todo) {
  await localDB.update('todos', todo);              // optimistic local update
  await syncQueue.enqueue('UPDATE_TODO', todo);     // queue for server
}

// 2. Sync worker processes queue when online
syncQueue.onConnectivityChange(async (online) => {
  if (online) {
    const pending = await syncQueue.getPending();    // FIFO order
    for (const item of pending) {
      try {
        await apiClient.sync(item);
        await syncQueue.markComplete(item.id);
      } catch (error) {
        if (isConflict(error)) {
          await resolveConflict(item, error.serverVersion);
        } else {
          await syncQueue.markFailed(item.id, error);
        }
      }
    }
  }
});
```

**Local database selection:**
- **WatermelonDB** (React Native): Lazy-loading SQLite. Only loads records when accessed — survives 10,000+ records without memory pressure. Best for relational data.
- **MMKV** (React Native): Synchronous key-value storage, 30x faster than AsyncStorage. Use for tokens, settings, small objects. NOT for relational queries.
- **Isar** (Flutter): NoSQL with links (relationships), full-text search, ACID transactions. Best all-rounder for Flutter local storage.
- **Drift** (Flutter): Type-safe SQLite wrapper with reactive queries. Use when you need complex SQL joins and migrations.

### Phase 4 (~15 min): Push Notifications

**Provider architecture:**
```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Backend │ →──│   FCM    │ →──│  Android  │
│  Server  │    │  (Google)│    │  Device   │
│          │    └──────────┘    └──────────┘
│          │    ┌──────────┐    ┌──────────┐
│          │ →──│   APNs   │ →──│   iOS    │
│          │    │  (Apple) │    │  Device   │
└──────────┘    └──────────┘    └──────────┘
```

**Critical implementation details:**
- APNs tokens rotate. Always register for token updates on each app launch — do NOT assume a stored token is valid. iOS may issue a new token after app reinstall, device restore, or OS update.
- FCM tokens also change. Subscribe to `onTokenRefresh` callback.
- Store the platform and token together: `{ platform: 'ios', token: '...', lastUpdated: Date }`. Backend needs to know which push service to route through.
- Never send sensitive data in the notification payload itself — push services (Apple/Google) log these. Put only a reference ID in `data`, fetch actual content from your API on notification tap.

**Notification priority taxonomy:**
| Priority | Android | iOS | Use case |
|----------|---------|-----|----------|
| High (10) | `priority: high` | `apns-priority: 10` | Time-sensitive: chat messages, OTP codes, ride updates |
| Normal (5) | `priority: normal` | `apns-priority: 5` | Standard: social updates, content alerts, reminders |
| Background | Silent FCM | `content-available: 1` | Data sync trigger, no user-visible notification |

### Phase 5 (~25 min): Platform Design Systems

**iOS Human Interface Guidelines — non-negotiable rules:**
- **Touch targets**: minimum 44×44pt. No exception. Apple rejects apps with tappable elements smaller than this.
- **Safe Areas**: Always respect safe area insets (top notch/island, bottom home indicator). Use `SafeAreaView` (RN) or `SafeArea` (Flutter) — never hardcode padding values.
- **Typography**: Use the system font (SF Pro). Support Dynamic Type — all text must scale when user changes accessibility text size. Test with largest accessibility text size; layouts must not break.
- **Navigation**: Tab bars at bottom for top-level destinations (3-5 items). Use hierarchical navigation with back chevron for drill-down. Modals for focused tasks — always provide clear dismiss action.
- **Gestures**: Standard gestures only unless you have a strong reason. Swipe-back from left edge is sacred on iOS — don't override it globally.
- **Dark Mode**: EVERY screen must support Dark Mode. Use semantic colors (label, secondaryLabel, systemBackground) that adapt automatically.
- **Haptics**: Use `UIImpactFeedbackGenerator` for confirmations, selections, and errors. Tiny detail — massive perceived quality difference. `light` for selection, `medium` for confirmation, `heavy` for errors, `rigid` for toggle switches.

**Android Material Design 3 — non-negotiable rules:**
- **Touch targets**: minimum 48dp. The extra 4dp over iOS accounts for Android's larger default finger size assumption.
- **Edge-to-edge**: Apps MUST draw behind the status bar and navigation bar (Android 15+ enforces this). Use `WindowInsets` APIs — never hardcode status bar height.
- **Material You (Monet)**: Support dynamic color on Android 12+. User-chosen wallpaper colors flow through your app via `android:colorPrimary` and M3 color roles.
- **Predictive back gesture** (Android 14+): Users expect to see a preview of the destination screen during a back swipe. Implement `OnBackPressedCallback` with `setEnabled(false)` to opt into the system back animation.
- **Typography**: Use Material type scale tokens (`displayLarge` through `labelSmall`). Roboto is default; Google Sans for brand moments only.
- **Navigation Bar**: Bottom for phones, Navigation Rail (side) for tablets/landscape. Use `NavigationBar` composable or BottomNavigationView (views).

For complete platform design system details, see `references/ios-hig-cheatsheet.md` and `references/material-design-cheatsheet.md`.

### Phase 6 (~25 min): Performance Optimization

Performance is the #1 reason users delete apps. A 2-second delay in startup increases abandonment by 20%.

**Cold start time target: < 1.5 seconds to interactive (measured from user tap to first frame render + data visible)**

| Optimization | Framework | Impact |
|-------------|-----------|--------|
| Native splash screen (not JS splash) | All | -200-500ms perceived |
| Lazy init non-critical SDKs (analytics after 1s delay) | All | -100-300ms |
| Hermes engine (React Native) | RN | -200-400ms TTI |
| Dart AOT compilation (default in release) | Flutter | Already optimized |
| Minimize main isolate/Dart entry point work | Flutter | -100-200ms |
| Deferred component loading | RN/Flutter | -500KB+ binary |

**List performance — 60fps scrolling is non-negotiable:**
- **React Native**: Use `FlashList` (Shopify) instead of `FlatList` — it's 5-10x faster for large lists by recycling views more aggressively. Estimated item size + `getItemType` for heterogeneous lists.
- **Flutter**: Use `ListView.builder` — never `ListView(children: [...])` for lists over 20 items. `itemExtent` for fixed-height items (avoids layout pass per item).
- **Both**: Paginate with cursor-based pagination. Load 20-30 items per page. Implement `onEndReached` with threshold (0.5 = trigger when half a screen away from end). Guard against double-fires with a loading ref/lock.

**Image optimization:**
- Always resize server-side to exact display dimensions × device pixel ratio. A 4000×3000 photo displayed at 375×250 wastes 99.7% of decoded memory.
- Progressive JPEGs: show low-res (10-20KB) immediately, swap to full-res on load. Prevents white flash.
- Memory cache: 1/4 of available RAM (not disk RAM — runtime memory). Disk cache: 200MB max, LRU eviction.
- Libraries: `expo-image` (React Native, built on Glide/SDWebImage), `cached_network_image` (Flutter).

**Animation performance — never block the UI thread:**
- React Native: Always use `useNativeDriver: true` for `Animated` API. Animations without native driver run on the JS thread — any JS work (state update, API response parsing, navigation transition) causes frame drops.
- Flutter: Most animations are GPU-driven by default. For complex custom painters, use `RepaintBoundary` to isolate repaint areas and avoid full-screen repaints.

For deep performance optimization guides, see `references/performance-optimization.md`.

### Phase 7 (~25 min): Security

Mobile security is defense-in-depth. Assume the device is compromised — never trust the client.

| Layer | Technique | Framework |
|-------|-----------|-----------|
| Transport | Certificate pinning (pinned to leaf or intermediate CA) | react-native-ssl-pinning, flutter_trusted_device |
| Storage | iOS Keychain / Android Keystore for secrets; EncryptedSharedPreferences for tokens | expo-secure-store, flutter_secure_storage |
| Code | ProGuard/R8 (Android), code obfuscation | Built into Android build; react-native-obfuscating-transformer |
| Integrity | Root/jailbreak detection, SafetyNet/Play Integrity | react-native-device-info, flutter_jailbreak_detection |
| Auth | Biometric + device credential fallback; never store PIN | expo-local-authentication, local_auth |
| Network | ATS (App Transport Security) enforced; no HTTP except localhost dev | Info.plist NSAppTransportSecurity (never disable in prod) |

**Hard rules:**
- Never store API keys, client secrets, or symmetric encryption keys in the app binary. Extract strings from any IPA/APK with `strings` command in seconds. Use backend-to-backend communication for secrets.
- Certificate pinning adds ~50KB to binary. Rotate pins every 90 days. Have a backup pin — if you only pin one cert and it expires, your app is bricked until an update is approved (3-7 days for App Store).
- Biometric auth is convenience, not security. Always fall back to server-validated credential after biometric gate. Biometrics can be compelled legally; a password cannot (5th Amendment, US).

### Phase 8 (~30 min): Deployment & CI/CD

**Build pipeline — the gold standard flow:**
```
Push to main → CI triggers:
  1. Lint (ESLint/dart analyze)          ~30s
  2. Type-check (tsc --noEmit)           ~45s
  3. Unit tests (Jest/flutter test)      ~2min
  4. Build dev binary (simulator)        ~5min
  5. Integration tests (Detox/Maestro)   ~8min
  6. Build staging binary                ~10min
  7. Upload to TestFlight/Play Internal  ~3min
  Total: ~30min to staging distribution

Tag release → Production build → Store submission
```

**Code signing — the part that breaks most teams:**
- iOS: Use Fastlane Match with a shared GitHub repo for certificates and provisioning profiles. One source of truth; no "it works on my machine" cert issues. Rotate annually (certificates expire after 1 year).
- Android: Generate upload keystore, store it in CI secrets (base64-encoded). Separate upload key (CI signing) from app signing key (Google-managed via Play Signing). Google Play Signing means even if your upload key is compromised, Google holds the actual app signing key.

**Over-the-air updates:**
- React Native: `expo-updates` — instant JS bundle push. Configure `fallbackToCacheTimeout: 0` (never fallback to embedded bundle if update download fails; the user already has a working version). Test OTA updates thoroughly — a bad push can crash ALL users instantly without app store rollback.
- Flutter: Shorebird — pushes Dart code changes. Still evolving; test extensively before production use.

**Store submission pitfalls that cause rejection:**
1. Missing privacy nutrition labels (Apple). List ALL data types your app collects, even if through third-party SDKs.
2. Requesting permissions without usage strings in Info.plist/AndroidManifest.
3. No "Delete Account" option inside the app (Apple requirement for apps with account creation since June 2022).
4. App crashes on launch on iPad if you only tested iPhone (Apple tests on both).
5. Using private APIs (Apple static analysis catches these). No `LSApplicationQueriesSchemes` beyond what you need.

### Phase 9 (~20 min): Testing Strategy

**Testing pyramid for mobile — adapted from web:**
```
        /\
       /E2E\      10% — Critical flows only (signup, checkout, core CRUD)
      /------\
     /  Inte- \    30% — Feature integration (screen with real API + DB)
    / gration  \
   /------------\
  /    Unit      \ 60% — Business logic, reducers, use cases, validators
 /----------------\
```

**Tools by layer:**
| Layer | React Native | Flutter |
|-------|-------------|---------|
| Unit | Jest + @testing-library/react-native | flutter test (built-in) |
| Widget/Component | @testing-library/react-native | flutter test with `pumpWidget` |
| Integration | Maestro (recommended — YAML-based, works on both platforms) | integration_test (built-in) |
| E2E | Detox (gray-box, Jest-based) or Maestro | patrol (successor to integration_test, more reliable) |
| Snapshot | jest-image-snapshot | golden_toolkit |
| Performance | React Native Performance Monitor, Flipper | Flutter DevTools timeline |

**Testing rules that prevent production incidents:**
- Every API-dependent screen must have a mock provider test that exercises loading, error, empty, and data states.
- Accessibility tests: run `accessibility()` checks in Maestro or manual VoiceOver/TalkBack pass. Every interactive element must have an accessibility label.
- Performance regression: measure cold start time and scroll FPS in CI. Fail the build if cold start exceeds 2s or average scroll FPS drops below 58.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Mobile development spans platform-specific concerns, API consumption, push infrastructure, and app store compliance. Coordination with backend, design, security, and release management is continuous.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Backend Developer** | API contract design, push notification payloads | Latency constraints on mobile networks, batch endpoints to reduce round trips, payload size limits (4KB APNs) |
| **Frontend Developer** | Cross-platform consistency, shared design tokens | Responsive-to-mobile design mapping, shared component patterns, navigation parity |
| **UI/UX Designer** | Platform conventions, gesture design | iOS HIG vs Material Design 3 differences, safe area requirements, platform-specific interaction patterns |
| **Security Engineer** | Certificate pinning, secure storage, auth | Biometric auth implementation, Keychain/Keystore patterns, token refresh on mobile, jailbreak/root detection |
| **DevOps Engineer** | CI/CD for app stores, OTA updates | Code signing automation, TestFlight/Internal Testing setup, build matrix (iOS + Android), environment configs |
| **QA Engineer** | Device matrix testing, E2E automation | Device coverage plan (low-end + high-end), Maestro/Detox configuration, offline/connectivity test scenarios |
| **Observability Engineer** | Crash reporting, performance monitoring | Crashlytics/Sentry integration, cold start timing, network error tracking, ANR detection thresholds |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| API version deprecation announced | Backend Developer | Retire old API surface; update mobile client with migration window |
| New push notification type added | Backend, Product Strategist | Payload design, deep-link routing, opt-in/opt-out UX |
| App Store review rejection | DevOps, Legal Advisor | Policy compliance fix, resubmission timeline |
| New permission required (camera, location, health) | Security Engineer, UI/UX Designer | Permission rationale dialog, denial handling, privacy review |
| Binary size exceeds App Store limit | Backend (if shared code), DevOps | Asset optimization, code splitting, on-demand resources |
| Critical crash rate spike (>1% sessions) | QA Engineer, Observability | Immediate investigation, potential hotfix release |

### Escalation Path

```
App Store rejection? → DevOps Engineer → Legal Advisor
Security vulnerability? → Security Engineer → Compliance Officer
API breaking change? → Backend Developer lead → System Architect
Critical performance regression? → Observability Engineer → CTO Advisor
Cross-platform inconsistency? → UI/UX Designer → Product Strategist
```

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Mobile = React Native with Expo (managed workflow). No native code. One codebase for iOS + Android. Auth = Firebase Auth or Supabase Auth. Deploy via EAS Build. No CI/CD beyond Expo. Manual testing on one device.
- **What to skip**: Native development (Swift/Kotlin). Custom native modules. Offline-first. Feature flags. CodePush/OTA updates. Performance profiling. Detox/Maestro E2E tests. Multi-device testing.
- **Coordination**: You own mobile + backend. Ship to TestFlight manually.

### Small Team (2-10 people, 100-10K users)
- **What changes**: React Native with Expo (managed or bare). TypeScript. CI/CD with EAS Build. Basic offline support (cached API responses). Push notifications (FCM + APNs). Crash reporting (Sentry). Testing on 2-3 devices (low-end + high-end). Platform-specific styling where needed.
- **What to skip**: Native modules. Offline-first with sync. E2E tests (Detox/Maestro). Performance budgets in CI. Root/jailbreak detection. Certificate pinning.
- **Coordination**: PR review with another mobile dev. API contract sync with backend. Bi-weekly mobile sync.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: React Native with native modules where needed. Offline-first with sync for critical flows. E2E tests (Maestro/Detox) on CI. Performance budgets (cold start < 2s, 60fps). Biometric auth. Secure storage (Keychain/Keystore). Multi-device test matrix (5+ devices). OTA updates (CodePush/EAS Update). Feature flags.
- **What to skip**: Full native development (Swift/Kotlin). Custom rendering engine. Advanced animations library (use Reanimated). Multi-platform beyond iOS + Android.
- **Coordination**: Weekly mobile guild. Bi-weekly design review. Monthly performance audit. Pre-release regression pass.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Native development teams (Swift + Kotlin) + cross-platform team. Full offline-first architecture with conflict resolution. Certificate pinning + root/jailbreak detection + code obfuscation. Performance monitoring (cold start, scroll FPS, memory). Advanced CI/CD with automated store submission. A/B testing. Feature flags for gradual rollout. Accessibility testing (VoiceOver/TalkBack). Internationalization (RTL, locale-specific formats).
- **What's full production**: Mobile platform team. Mobile reliability engineering. Store review management. Beta program (TestFlight + Play Console). Cross-platform component library. App performance observability.
- **Coordination**: Mobile platform team weekly. Cross-platform design system council monthly. App store release coordination. Quarterly mobile strategy review.

### Transition Triggers
- **Solo → Small**: Second mobile developer. User complaints about performance or crashes.
- **Small → Medium**: Offline support needed. Performance becomes critical (cold start > 2s). >10K installs.
- **Medium → Enterprise**: Multi-platform team split. Store review rejections need process. >100K installs.

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `cross-platform-selection` | Choosing between React Native (Expo), Flutter, Swift/Kotlin native, or PWA | Performance requirements, team skills, time-to-market, platform-specific API needs, long-term maintenance cost |
| `navigation-architecture` | Designing tab/stack/drawer navigation with deep linking and universal links | React Navigation/GoRouter, `apple-app-site-association`, `assetlinks.json`, deferred deep links |
| `offline-first` | Building apps for unreliable connectivity, field workers, or data-entry-heavy workflows | WatermelonDB/Isar local DB, sync queue with conflict resolution (CRDT, LWW), network status monitoring |
| `push-notifications` | Implementing FCM/APNs with deep-link routing, rich media, and analytics | Token registration/refresh, notification channels (Android), provisional auth (iOS), foreground handling |
| `mobile-security` | Certificate pinning, Keychain/Keystore, biometric auth, root/jailbreak detection | SSL pinning with TrustKit/okhttp, secure enclave storage, code obfuscation (ProGuard/R8), runtime integrity checks |
| `performance-optimization` | Cold start < 1.5s, 60fps scrolling, memory < 50MB on low-end devices | Hermes engine tuning, FlatList/RecyclerView optimization, image caching tiers, main thread offloading |
| `app-store-deployment` | TestFlight, App Store Connect, Google Play Console, over-the-air updates (CodePush) | Store metadata (privacy labels, screenshots), phased rollout, app review guidelines, EAS Submit |
| `platform-design-compliance` | iOS HIG and Material Design 3 conformance: touch targets, safe areas, typography | 44pt/48dp touch targets, Dynamic Type/font scaling, Dark Mode, SafeArea/WindowInsets, platform-specific gestures |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
1. **Measure performance on low-end devices, not your flagship phone:** Target a $200 Android device (2GB RAM) for baseline. If cold start < 1.5s and scrolling hits 60fps there, it works everywhere. Your iPhone 15 Pro Max is not representative.
2. **Local DB is source of truth; server is the sync target:** In offline-first apps, the local database drives the UI. API calls update the local DB, which triggers reactive UI updates. Never show a spinner waiting for the network when local data exists.
3. **Request permissions at point of need with rationale:** Don't ask for camera access on app launch. Ask when the user taps "Scan QR code." Show a rationale dialog before the system prompt. If denied, show a disabled state with a link to Settings.
4. **Deep-link every shareable screen:** Every screen a user might share, receive as a notification target, or bookmark must have a deep-link URL. Test universal links (iOS) and app links (Android) with `apple-app-site-association` and `assetlinks.json` validators.
5. **Push notifications: token refresh on every launch, silent notification for data sync:** Register for push on each app launch — tokens change. Use silent/background notifications to trigger data sync, not to deliver content. Content notifications should wake the app and fetch fresh data.
6. **Design for platform conventions, not pixel-perfect cross-platform parity:** iOS users expect bottom tab bars, swipe-to-go-back, and SF Symbols. Android users expect Material Design 3, top app bars, and system back button. Delight comes from feeling native, not identical.
7. **Graceful degradation for offline, permissions denied, and low battery:** Every feature should define its degraded experience: offline (stale data with indicator), permissions denied (disabled with explanation), low battery (reduce animation, pause background sync).
8. **Automate store submission, don't manually upload:** CI should build, sign, and upload to TestFlight/Play Console on every merge to main. Manual uploads lead to wrong versions, missing symbols, and late-night App Store Connect panic.
9. **Crash reporting with breadcrumbs, not just stack traces:** Log user actions (screen visited, button tapped, API called) as breadcrumbs before the crash. A stack trace tells you what crashed; breadcrumbs tell you what the user was doing — and how to reproduce it.
10. **Security is defense-in-depth:** Certificate pinning + Keychain/Keystore + ProGuard/R8 + root detection + disable screenshots in app switcher + jailbreak detection. Each layer alone can be bypassed; together they raise the bar from opportunistic to targeted attack.


### Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| `Module not found: Can't resolve '...'` | Missing dependency or incorrect import path | `npm install <package>` or fix import path |
| `TypeError: Cannot read properties of undefined` | Accessing property on null/undefined value | Add optional chaining (`?.`) or null check before access |
| `Connection refused` | Target service not running or wrong host/port | Check service status: `docker ps`; verify environment variables |
| `ECONNREFUSED` | Database server not running | `docker compose up -d db`; check connection string |
| `413 Payload Too Large` | Request body exceeds server limit | Increase `body-parser` limit or paginate the request |
| `port 3000 already in use` | Previous process still bound to port | `lsof -ti:3000 \| xargs kill` or use `PORT=3001` |
| `ETIMEDOUT` | Network connectivity issue or firewall | Check network: `ping <host>`; verify firewall rules |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Technology selection documented: native vs cross-platform decision with rationale, team skills, performance requirements
- [ ] **[S2]**  Navigation architecture: deep links map to every shareable screen; universal links (iOS) + app links (Android) configured and verified with `apple-app-site-association` and `assetlinks.json`
- [ ] **[S3]**  Auth flow: zero-flash launch (splash → resolved auth state → correct screen); token refresh with retry queue; logout clears all cached data
- [ ] **[S4]**  Offline-first data: local DB is source of truth; sync queue processes mutations FIFO with conflict resolution; network status indicator shown during offline; stale data flagged visually
- [ ] **[S5]**  Push notifications: FCM + APNs tokens registered and refreshed on each launch; notification deep-link routing tested for each notification type; foreground notification handling defined
- [ ] **[S6]**  Platform design compliance: all touch targets ≥ 44pt (iOS) / 48dp (Android); Dynamic Type + font scaling tested; Dark Mode supported on every screen; Safe Area / WindowInsets respected
- [ ] **[S7]**  Permissions: requested at point of need with rationale dialog; denial gracefully handled with settings deep link
- [ ] **[S8]**  Biometric auth: implemented with device credential fallback; sensitive data re-validated server-side after biometric gate
- [ ] **[S9]**  Performance: cold start < 1.5s (measured on low-end device); 60fps scrolling on lists with 1000+ items; memory < 50MB on 2GB RAM device; image caching with disk + memory layers
- [ ] **[S10]**  Security: certificate pinning active; Keychain/Keystore for secrets; ProGuard/R8 enabled with keep rules for serialization models; root/jailbreak detection (at minimum, log and alert)
- [ ] **[S11]**  Crash reporting: Sentry/Firebase Crashlytics with source maps uploaded in CI; breadcrumbs for critical user flows
- [ ] **[S12]**  CI/CD: lint → type-check → unit test → integration test → build → TestFlight/Play Internal on every push to main
- [ ] **[S13]**  Store metadata: App Store privacy nutrition labels accurate; all Info.plist usage descriptions included; account deletion flow inside app; screenshots for all required device sizes
- [ ] **[S14]**  Testing: unit tests for all domain logic (>80% coverage on domain layer); integration tests for critical flows; accessibility audit pass

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [references/platform-comparison.md](references/platform-comparison.md) — Detailed native vs cross-platform decision matrix
- [references/ios-hig-cheatsheet.md](references/ios-hig-cheatsheet.md) — Complete iOS Human Interface Guidelines reference
- [references/material-design-cheatsheet.md](references/material-design-cheatsheet.md) — Complete Material Design 3 reference
- [references/performance-optimization.md](references/performance-optimization.md) — Startup, animation, memory, list, and bundle optimization
- [references/offline-first-patterns.md](references/offline-first-patterns.md) — Sync strategies, conflict resolution, local DB selection
- [Expo Documentation](https://docs.expo.dev/)
- [React Native Documentation](https://reactnative.dev/docs/)
- [Flutter Documentation](https://flutter.dev/docs)
- [React Navigation](https://reactnavigation.org/)
- [TanStack Query](https://tanstack.com/query/latest)
- [WatermelonDB](https://watermelondb.dev/)
- [Fastlane](https://fastlane.tools/)
- [Human Interface Guidelines — Apple](https://developer.apple.com/design/human-interface-guidelines/)
- [Material Design 3](https://m3.material.io/)
