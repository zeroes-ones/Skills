---
name: mobile-developer
description: 'Cross-platform mobile development with React Native and Flutter, navigation
  patterns, state management, offline-first architecture, push notifications, platform-specific
  patterns, and app store deployment. Trigger: mobile, React Native, Flutter, navigation,
  offline-first, push notifications, app store, iOS, Android.'
author: Sandeep Kumar Penchala
type: development
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- mobile-developer
token_budget: 4000
output:
  type: code
  path_hint: ./
chain:
  consumes_from:
  - accessibility-testing
  - api-designer
  - backend-developer
  - localization-engineer
  - tdd-guide
  - ui-ux-designer
  feeds_into:
  - localization-engineer
  - qa-engineer
  - security-reviewer
  - translation-manager
---
# Mobile Developer

Build production mobile applications — spanning native (Swift/Kotlin), React Native (Expo), and Flutter — with deep expertise across the full development lifecycle. This skill covers decision frameworks for choosing the right technology, architecture patterns, platform-specific design systems (iOS HIG, Material Design 3), offline-first data synchronization, performance optimization to 60fps, security hardening, CI/CD pipeline design, and App Store/Google Play deployment.

## Route the Request
<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("package.json", "\"react-native\"\|\"expo\"\|\"flutter\"")` OR `file_exists("ios/\|android/\|App.tsx\|pubspec.yaml")` | This is your skill. Jump to **Core Workflow** — Phase 2 (UI Implementation). |
| A2 | `file_contains("*", "NSPhotoLibrary\|NSCamera\|Info.plist\|AndroidManifest.*permission")` AND `file_contains("*", "permission.*denied\|permission.*blocked\|shouldShowRequest")` | Jump to **Core Workflow** — Phase 3 (Permissions). |
| A3 | `file_contains("*", "SQLite\|WatermelonDB\|Realm\|MMKV\|AsyncStorage\|local.*database")` AND `file_contains("*", "offline\|sync\|conflict\|reconcile")` | Jump to **Decision Trees** — Offline-First Strategy. |
| A4 | `file_contains("*", "APNs\|FCM\|firebase.*messaging\|push.*notification\|content-available")` AND `file_contains("*", "token.*refresh\|onTokenRefresh\|registerForRemote")` | Jump to **Core Workflow** — Phase 4 (Push Notifications). |
| A5 | `file_contains("*", "FaceID\|TouchID\|biometric\|LAContext\|BiometricPrompt")` OR `file_contains("*", "LAError\|biometryLockout\|BIOMETRIC_ERROR")` | Jump to **Error Decoder** — biometric section. |
| A6 | `file_contains("*", "deeplink\|deep-link\|universal.*link\|apple-app-site\|assetlinks")` OR `file_contains("*", "getInitialURL\|Linking\.openURL\|onNewIntent")` | Jump to **Production Checklist** — S2 (Navigation & Deep Links). |
| A7 | `file_contains("*", "Fastlane\|TestFlight\|Play.*Console\|store.*review\|screenshots")` OR `file_contains("*", "provisioning\|signing\|certificate\|keystore")` | Jump to **Production Checklist** — S13 (Store Metadata). |
| A8 | `file_contains("*", "jest\|detox\|maestro\|appium\|XCTest")` AND `file_contains("*", "e2e\|integration.*test\|snapshot.*test")` | Invoke **qa-engineer** instead. This is mobile testing strategy. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Choose a mobile tech stack → Start at "Decision Trees" — Native vs React Native vs Flutter vs PWA
├── Build a specific screen or UI flow → Jump to "Core Workflow > Phase 2 (UI Implementation)"
├── Implement offline storage (SQLite, MMKV, WatermelonDB) → Go to "Decision Trees > Offline-First Strategy" then Phase 3
├── Set up push notifications (FCM/APNs) → Jump to "Core Workflow > Phase 4 (Push Notifications)"
├── Integrate a native feature (camera, biometrics, GPS) → Go to "references/native-module-guide.md"
├── Optimize performance (60fps, cold start, memory) → Jump to "Core Workflow > Phase 5 (Performance)"
├── Submit to App Store or Google Play → Go to "Production Checklist > App Store Submission"
├── Cross-platform from scratch (React Native/Flutter) → Start at "Decision Trees" then follow Core Workflow
├── Need API contract for mobile → Invoke api-designer skill instead
├── Need backend API for mobile → Invoke backend-developer skill instead
├── Need mobile UI/UX design → Invoke ui-ux-designer skill instead
├── Need security review of mobile → Invoke security-reviewer skill instead
├── Need QA for mobile testing → Invoke qa-engineer skill instead
├── Need localization for mobile → Invoke localization-engineer skill instead
└── Don't know where to start? → Describe your app idea and platform targets and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never assume network connectivity.** Every screen should render something useful offline. Do not show a blank screen or spinner when the network is unavailable — use cached data, offline queues, and graceful degradation.
- **Always handle background/foreground transitions.** Apps can be killed, suspended, or resumed at any time. Save state in `onPause`/`onBackground`, restore in `onResume`/`onForeground`. Do not assume the app starts fresh every time.
- **Test on low-end devices, not just the latest flagship.** Your app must work on a 3-year-old mid-range phone with 4GB RAM and a slow network. Do not optimize only for iPhone 16 Pro or Pixel 9.
- **Always request permissions at the point of need.** Explain why the permission is needed before the system dialog. Do not request all permissions at app launch — it reduces trust and acceptance rates.
- **Admit what you don't know.** Platform-specific APIs (HealthKit, Credential Manager, ARKit) evolve rapidly. If you're not current on the latest SDK version, say so and point to Apple/Google docs.

## The Expert's Mindset
<!-- DEEP: 10+min — how masters think, not just what they do -->

### The Mental Model Shift
Competent mobile developers build apps that work on their test device. Masters build experiences that **work on a $200 Android phone in rural connectivity, in direct sunlight, with 15% battery.** The shift: your iPhone 16 Pro on office WiFi is not representative. The median global user has a mid-range Android device, intermittent connectivity, and pays for data by the megabyte. Design for constraints first — enhance for abundance.

### Cognitive Biases That Kill Mobile Experiences
| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **iOS-first myopia** | Designing and testing exclusively on iOS, then "porting" to Android — Material Design feels alien, back button breaks, permissions model differs | Design for both platforms simultaneously. Every feature spec must include Android behavior before implementation starts. |
| **Flagship device blindness** | Testing only on the latest Pixel or iPhone Pro — missing the 4GB RAM device where your app is killed in the background every 30 seconds | Maintain a device lab: latest flagship + 3-year-old budget device for each platform. Budget device is your primary test target. |
| **Over-engineering offline** | Building CRDT-based sync and conflict resolution for an app that's used 95% online — 6 months of engineering for an edge case | Offline support is a spectrum: cache-last-known-state (2 days) → optimistic writes with retry (2 weeks) → full offline with sync (2 months). Match the engineering investment to the user's actual offline duration. |

### What Mobile Masters Know That Others Don't
- **Battery is a shared resource.** Every network request, GPS poll, and background wake costs battery. A user who uninstalls your app because it's draining their battery is gone forever. Use `WorkManager` (Android) and `BGTaskScheduler` (iOS) — never roll your own background polling.
- **App Store review is a deployment pipeline with a 24-72 hour SLA you don't control.** Structure your app so critical fixes can ship via OTA update (JS bundle, server config, feature flags). The native binary should change rarely. Every native change that requires review is a risk.
- **Memory is a hard ceiling, not a budget.** iOS kills your app when it exceeds the memory limit — no warning, no callback. Android's `onTrimMemory()` is a courtesy, not a guarantee. Profile memory under worst case: largest screen, most content, longest session. If you're within 20% of the limit, you're one image-heavy screen from a crash.
- **Every refactor must remove dead code — not just reorganize it.** When you refactor a screen or module, delete unused assets, dead navigation routes, stale feature flags, and abandoned native modules. Each unused asset bloats the binary; each dead native module risks App Store rejection for unused permissions.

### When to Break Your Own Rules
- **Ship a native module for a single critical feature.** The cross-platform abstraction tax isn't always worth it. If AR, Bluetooth, or advanced camera is your core differentiator, go native for that module. Wrap it in a cross-platform interface for the rest of the app.
- **Use WebView for content that changes daily.** Terms of service, help center, marketing pages — content that changes faster than your app review cycle belongs in a WebView, not in native code.

## Operating at Different Levels

Mobile development spans platform-specific concerns (app stores, device capabilities, offline) that manifest differently at each level.

| Level | Mobile Output Characteristics |
|---|---|
| **L1 — Apprentice** | Implements screens from design specs. Learns navigation patterns, platform conventions, and the build pipeline. |
| **L2 — Practitioner** | Delivers complete features with offline support, error states, and platform-appropriate UX. Independent shipping. |
| **L3 — Senior** | Architecture decisions: navigation design, state management strategy, native vs. cross-platform trade-offs. Platform-specific optimizations. |
| **L4 — Staff** | Mobile platform strategy for the org: shared component architecture, CI/CD for mobile, OTA update strategy, App Store governance. |
| **L5 — Principal** | Novel mobile patterns or frameworks adopted across the industry. "Here's a new approach to offline sync / navigation / cross-platform architecture." |

**Usage**: Say "as an L3 mobile developer, design the navigation architecture for..." Default: **L2** (production-ready, independent execution).

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
<!-- DEEP: 10+min -->

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


**What good looks like:** App builds and runs on both iOS and Android from a single codebase commit. All screens render correctly on the smallest and largest supported device sizes (iPhone SE to Pro Max, Pixel to Galaxy Ultra). No red boxes, crash logs, or ANR reports in the last 100 test sessions. App store review passes on first submission — no guideline violations. Launch-to-interaction time < 2s on a mid-range device (Pixel 6 / iPhone 12).

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

**Production-grade sync queue — priority levels, backoff, and dead letters:**

The simple FIFO queue above works for demos. Production needs priority ordering, exponential backoff with jitter, and a dead letter queue for permanently failed operations.

```typescript
type SyncPriority = 'critical' | 'high' | 'normal' | 'background';
type SyncStatus = 'pending' | 'in_flight' | 'completed' | 'dead_letter';

interface SyncItem {
  id: string;
  type: 'CREATE' | 'UPDATE' | 'DELETE';
  entity: string;           // table or collection name
  payload: Record<string, unknown>;
  priority: SyncPriority;
  retries: number;          // 0–5
  maxRetries: number;       // default 5
  lastError?: string;
  createdAt: number;        // epoch ms
  nextRetryAt: number;      // epoch ms
  status: SyncStatus;
  localVersion: number;     // monotonic counter for conflict detection
}

class SyncQueue {
  private queue: SyncItem[] = [];
  private processing = false;

  /** Enqueue with priority-based insertion. Critical items (life-saving data
   *  like bleed logs) jump to the front. Background items (analytics) wait. */
  async enqueue(item: Omit<SyncItem, 'id' | 'retries' | 'status' | 'localVersion'>): Promise<void> {
    const syncItem: SyncItem = {
      ...item,
      id: uuid(),
      retries: 0,
      status: 'pending',
      localVersion: await this.getLocalVersion(item.entity),
      nextRetryAt: Date.now(),
    };
    // Insert at correct priority position
    const priorities: SyncPriority[] = ['critical', 'high', 'normal', 'background'];
    const insertIdx = this.queue.findIndex(
      q => priorities.indexOf(q.priority) > priorities.indexOf(syncItem.priority)
    );
    if (insertIdx === -1) this.queue.push(syncItem);
    else this.queue.splice(insertIdx, 0, syncItem);

    await this.persist(); // save queue to MMKV — survives app kill
  }

  /** Process queue with exponential backoff + jitter. Called when online. */
  async processAll(): Promise<void> {
    if (this.processing) return;
    this.processing = true;

    while (this.queue.some(q => q.status === 'pending' && q.nextRetryAt <= Date.now())) {
      const item = this.queue.find(q => q.status === 'pending' && q.nextRetryAt <= Date.now())!;
      item.status = 'in_flight';

      try {
        await this.dispatch(item);
        item.status = 'completed';
        this.queue = this.queue.filter(q => q.id !== item.id);
      } catch (error) {
        item.retries++;
        item.lastError = String(error);

        if (item.retries >= item.maxRetries) {
          // Dead letter — permanently failed. Alert the user for critical items.
          item.status = 'dead_letter';
          if (item.priority === 'critical') {
            this.notifyUser('Sync failed', `Could not save ${item.entity}`);
          }
        } else {
          // Exponential backoff: 2^n * base_delay with 20% jitter
          const baseDelay = item.priority === 'critical' ? 1_000 : 5_000;
          const delay = Math.min(
            Math.pow(2, item.retries) * baseDelay * (0.8 + Math.random() * 0.4),
            5 * 60 * 1000  // cap at 5 minutes
          );
          item.nextRetryAt = Date.now() + delay;
          item.status = 'pending';
        }
      }
      await this.persist();
    }
    this.processing = false;
  }
}
```

**Conflict resolution — three-way merge for offline mutations:**

```typescript
interface ConflictResolution<T> {
  /** Three-way merge using base (last known server state), local, and remote versions.
   *  This is the industry standard — Git uses the same algorithm. */
  resolve(params: {
    baseVersion: T;      // what the server had when we last synced
    localVersion: T;     // what we changed offline
    remoteVersion: T;    // what the server now has (someone else's change)
    strategy: 'last-write-wins' | 'client-wins' | 'server-wins' | 'field-merge';
    fieldRules?: Record<string, 'client' | 'server'>;  // per-field authority for field-merge
  }): T;
}

// Health app example: bleed log entry
function resolveBleedLogConflict(params: {
  baseVersion: BleedLogEntry;
  localVersion: BleedLogEntry;
  remoteVersion: BleedLogEntry;
}): BleedLogEntry {
  const { base, local, remote } = params;

  // If remote hasn't changed since base → use local (no conflict)
  if (remote.updatedAt === base.updatedAt) return local;

  // If local hasn't changed since base → use remote (no conflict)
  if (local.updatedAt === base.updatedAt) return remote;

  // Both changed → field-level merge based on medical safety rules
  return {
    ...remote,
    // User's symptom report always wins (subjective, can't be overridden)
    symptoms: local.symptoms,
    // Severity: take the higher value (safety-first — never downgrade severity)
    severity: Math.max(local.severity, remote.severity),
    // Treatment notes: merge both (don't lose information)
    treatmentNotes: `${remote.treatmentNotes}\n---Additional entry---\n${local.treatmentNotes}`,
    // Administrative fields: server wins (timestamps, flags set by backend)
    updatedAt: remote.updatedAt,
    reviewedBy: remote.reviewedBy,
  };
}
```

**Offline mutations — temporary IDs and sync ordering:**

When creating records offline, generate a temporary client-side ID. On first successful sync, the server returns the permanent ID. All child records must reference the parent by its temporary ID until the parent is synced.

```typescript
// 1. Create parent (bleed log entry) — temporary ID
const tempBleedId = `temp_${uuid()}`;
await localDB.insert('bleed_logs', { id: tempBleedId, ...data, _synced: false });
await syncQueue.enqueue({ type: 'CREATE', entity: 'bleed_logs', payload: { id: tempBleedId, ...data }, priority: 'critical' });

// 2. Create child (treatment) — references temp parent ID
await localDB.insert('treatments', { id: `temp_${uuid()}`, bleedLogId: tempBleedId, ...treatmentData, _synced: false });
await syncQueue.enqueue({ type: 'CREATE', entity: 'treatments', payload: { bleedLogId: tempBleedId, ...treatmentData }, priority: 'critical' });

// 3. Sync worker enforces ordering: CREATE parents before children
// On successful parent sync, remap temp IDs to real IDs:
const idMapping = new Map<string, string>(); // tempId → realId
idMapping.set(tempBleedId, serverResponse.id);
// Update all queued child items referencing tempBleedId
for (const item of syncQueue.getByParent(tempBleedId)) {
  item.payload.bleedLogId = serverResponse.id;
}
```

**Network state machine — graceful degradation by connection quality:**

```typescript
type NetworkState = 'online-fast' | 'online-slow' | 'online-metered' | 'offline';
type NetworkStrategy = 'sync-all' | 'sync-critical-only' | 'queue-only' | 'read-cache-only';

const strategyForState: Record<NetworkState, NetworkStrategy> = {
  'online-fast': 'sync-all',            // full sync, fetch fresh data, upload all
  'online-slow': 'sync-critical-only',  // only bleed logs + meds, defer analytics/images
  'online-metered': 'queue-only',       // don't download images/video, queue writes
  'offline': 'read-cache-only',         // local DB only, show stale-data banner
};

// Connectivity detection with quality assessment
const useNetworkMonitor = () => {
  const [state, setState] = useState<NetworkState>('offline');

  useEffect(() => {
    const check = async () => {
      const netInfo = await NetInfo.fetch();
      if (!netInfo.isConnected) return setState('offline');
      if (netInfo.details?.isConnectionExpensive) return setState('online-metered');

      // Measure latency with a HEAD request to health endpoint
      const start = Date.now();
      try {
        await fetch(`${API_BASE}/health`, { method: 'HEAD' });
        const latency = Date.now() - start;
        setState(latency < 500 ? 'online-fast' : 'online-slow');
      } catch {
        setState('offline');
      }
    };
    check();
    return NetInfo.addEventListener(check);
  }, []);

  return state;
};
```

**Delta sync with sequence numbers — minimize transferred data:**

```typescript
interface DeltaSyncState {
  lastSequence: number;       // last server sequence number we've seen
  lastFullSync: number;       // epoch ms of last complete sync
}

async function deltaSync(state: DeltaSyncState): Promise<DeltaSyncState> {
  // 1. Pull: ask server for changes since our last known sequence
  const response = await apiClient.get('/sync/pull', {
    params: { since: state.lastSequence, limit: 500 }
  });
  // Server returns: { changes: [...], newSequence: 1042, hasMore: false }

  // 2. Apply server changes to local DB in order
  for (const change of response.changes) {
    await applyChangeToLocalDB(change);
    state.lastSequence = Math.max(state.lastSequence, change.sequence);
  }

  // 3. Push: send our pending changes to server
  const pendingLocal = await syncQueue.getPending();
  const pushResponse = await apiClient.post('/sync/push', {
    changes: pendingLocal,
    baseSequence: state.lastSequence,  // server checks for conflicts
  });

  // 4. Handle push conflicts
  for (const conflict of pushResponse.conflicts) {
    const resolved = resolveConflict(conflict);
    await localDB.update(conflict.entity, resolved);
  }

  // 5. Periodically do a full reconciliation (e.g., every 24h or on WiFi)
  if (Date.now() - state.lastFullSync > 24 * 60 * 60 * 1000) {
    const fullData = await apiClient.get('/sync/full');
    await localDB.replaceAll(fullData);
    state.lastFullSync = Date.now();
    state.lastSequence = fullData.sequence;
  }

  return state;
}
```

**TTL-based cache invalidation policy by data type:**

| Data Type | Cache TTL | Stale-While-Revalidate | Strategy |
|-----------|-----------|----------------------|----------|
| User profile | 1 hour | Yes (show cached, refresh bg) | `staleTime: 60 * 60 * 1000` |
| Forum posts list | 5 min | Yes | Invalidate on pull-to-refresh |
| Forum post detail | 30 sec | No (show loader for fresh data) | Real-time via WebSocket push |
| Bleed log entries | Immediate | No (health data — never stale) | `staleTime: 0, cacheTime: 0` |
| Medication list | 1 hour | Yes | Invalidate on user edit |
| Notification preferences | 24 hours | Yes | User rarely changes these |
| Static content (FAQs) | 7 days | Yes | Hard reload on app update |
| Pod/condition data | 1 hour | Yes | Invalidate on pod membership change |

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

**APNS device token lifecycle — the full picture:**
- **Registration**: On app launch, call `registerForRemoteNotifications()`. iOS returns a device token via `application(_:didRegisterForRemoteNotificationsWithDeviceToken:)`. This token is unique to the device + app combination and changes across reinstalls, device restores, and major OS updates.
- **Refresh detection**: iOS may issue a new token without user interaction. Always compare the received token against the last stored token. If different, send to backend immediately — old token will fail silently, causing undelivered notifications.
- **Invalidation**: The delegate method `application(_:didFailToRegisterForRemoteNotificationsWithError:)` fires when registration fails. Common causes: no network, no provisioning profile entitlement, simulator (push doesn't work on simulator — test on device).
- **Multi-device handling**: A user with iPhone + iPad + Apple Watch gets different APNs tokens per device. Your backend must store an array of `{ deviceId, platform, token, lastActive }` per user. When sending, broadcast to all or target by last-active device.
- **APNs auth**: Use token-based authentication (JWT with p8 key) — it never expires, unlike certificate-based auth which requires annual renewal. One p8 key covers all your team's apps.

**Notification Service Extension (iOS) — modify push before display:**

```swift
// NotificationService.swift — runs in a separate process, ~30s execution window
// Use cases: decrypt end-to-end encrypted push payload, download rich media attachment
class NotificationService: UNNotificationServiceExtension {
    override func didReceive(_ request: UNNotificationRequest,
        withContentHandler contentHandler: @escaping (UNNotificationContent) -> Void) {

        guard let bestAttempt = request.content.mutableCopy() as? UNMutableNotificationContent else {
            contentHandler(request.content); return
        }

        // 1. Decrypt E2E-encrypted payload (e.g., chat message body)
        if let encryptedBody = bestAttempt.userInfo["encrypted_body"] as? String {
            bestAttempt.body = decryptPayload(encryptedBody) ?? "New message"
        }

        // 2. Download rich media attachment (image, video thumbnail)
        if let imageUrl = bestAttempt.userInfo["image_url"] as? String {
            downloadAttachment(from: imageUrl) { attachment in
                if let attachment = attachment {
                    bestAttempt.attachments = [attachment]
                }
                contentHandler(bestAttempt)
            }
        } else {
            contentHandler(bestAttempt)
        }
    }
}
```

**Notification Content Extension (iOS) — custom notification UI:**
- Provides a custom `UIViewController` displayed when the user 3D-touches or long-presses a notification. Use for: interactive charts, message threads, calendar event previews. Not for: replacing standard notification look entirely (Apple rejects this).
- Register in Info.plist with `UNNotificationExtensionCategory` matching the notification category identifier.
- Limited interaction — no keyboard input, no scrolling `UITableView`. Use `UNNotificationContentExtension` protocol methods for media playback controls or quick action buttons.

**Android notification channels deep-dive:**

```kotlin
// Create channel on app startup — Android 8.0+ requires channels for ALL notifications
// If no channel matches, notification is silently dropped on API 26+
val channel = NotificationChannel(
    "chat_messages",            // id: immutable once created
    "Chat Messages",            // name: user-visible in system settings
    NotificationManager.IMPORTANCE_HIGH // importance: controls sound, heads-up, interruption
).apply {
    description = "Incoming chat messages from your conversations"
    enableVibration(true)
    vibrationPattern = longArrayOf(0, 200, 100, 200) // custom pattern
    setShowBadge(true)          // show dot on app icon
    lockscreenVisibility = Notification.VISIBILITY_PRIVATE // hide content on lock screen
}

notificationManager.createNotificationChannel(channel)
```

**Importance levels — pick the right one:**

| Level | Behavior | Use Case |
|-------|----------|----------|
| `IMPORTANCE_HIGH` | Heads-up popup, sound, vibration | Chat messages, ride arrival, security alerts |
| `IMPORTANCE_DEFAULT` | Sound, no popup | Social updates, content alerts |
| `IMPORTANCE_LOW` | No sound, status bar only | Weather updates, sync status |
| `IMPORTANCE_MIN` | No sound, no visual interruption | Background data sync confirmations |
| `IMPORTANCE_NONE` | Blocked entirely | Deprecated channel migration placeholder |

**Channel groups:** Group related channels so users can manage them together in system settings. E.g., group "Messages" with sub-channels: "Direct Messages" + "Group Messages" + "Message Reactions."

**Silent/background notification best practices:**
- **iOS `content-available: 1`**: Set `apns-priority: 5` (not 10). The payload MUST NOT include `alert`, `sound`, or `badge` — or iOS may throttle it. iOS delivers at most 2-3 silent pushes per hour when the app is not in the foreground, and may coalesce them.
- **Android data payloads**: Omit `notification` key entirely; include only `data`. The app receives the payload in `onMessageReceived` and decides whether to post a local notification. This bypasses the system tray for true background processing.
- **Rate limits**: APNs silently throttles excessive background pushes. FCM collapses messages with the same `collapse_key`. Always include a collapse key for messages that replace previous ones (e.g., "new like on post" — only the latest matters).
- **User-facing rate limit**: More than 4-5 notifications/day from non-messaging apps leads to the user disabling notifications. Respect the user's attention.

**Push notification reliability — detecting and diagnosing failures:**
- **APNs feedback service**: APNs returns status codes (`410 Unregistered` = token invalid, remove it from your database). Poll the feedback service or use the HTTP/2 stream to get real-time delivery failures.
- **FCM delivery diagnostics**: FCM provides delivery receipt via `send_to_device` response (`success`, `failure`, `canonical_ids`). A `NotRegistered` error means the token is stale — delete it. A `canonical_id` in the response means the token was refreshed — update your database.
- **Handling expired tokens**: If a push send returns `410` (APNs) or `NotRegistered` (FCM), remove the token from your database immediately. Sending to invalid tokens wastes quota and may trigger rate limiting by Apple/Google.
- **End-to-end test**: Maintain a backend endpoint that sends a silent notification to a test device on demand. Run this test in CI on every deploy to verify the push pipeline: backend → APNs/FCM → device. A broken push pipeline produces zero user-facing errors — just silently undelivered notifications.

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

### Phase 10 (~25 min): Streaming Clients & Real-Time Data

Real-time data on mobile is a fundamentally different beast from web. iOS and Android aggressively kill persistent connections when the app goes to background. The right pattern is the difference between a chat app that works and one that drains 30% battery per hour.

**Decision matrix — choose the right real-time transport:**

| Use Case | Transport | Why |
|----------|-----------|-----|
| Chat / messaging | WebSocket (primary) + Silent Push (wake) | Bidirectional low-latency; push wakes the app when WebSocket is killed |
| Live feed (sports scores, stock ticker) | SSE (primary) + Polling (fallback) | Server→client unidirectional; simpler than WebSocket; polling as degraded fallback |
| Data sync trigger (new content available) | Silent Push (`content-available: 1` / FCM data-only) | Minimal battery; app wakes briefly, fetches, goes back to sleep |
| Real-time health data (HR monitor, step counter) | BLE / Core Bluetooth | Persistent peripheral connection; not internet-based |
| Collaborative editing | WebSocket + CRDT merge | Bidirectional low-latency + conflict-free merge on reconnect |

**WebSocket client — production-grade implementation:**

```typescript
// Connection state machine: CONNECTING → CONNECTED → RECONNECTING → DISCONNECTED → SUSPENDED
type ConnectionState =
  | 'CONNECTING'
  | 'CONNECTED'
  | 'RECONNECTING'
  | 'DISCONNECTED'
  | 'SUSPENDED'; // app in background, OS killed socket

function useWebSocket(url: string) {
  const [state, setState] = useState<ConnectionState>('DISCONNECTED');
  const wsRef = useRef<WebSocket | null>(null);
  const retryCount = useRef(0);
  const messageQueue = useRef<string[]>([]);

  const connect = useCallback(() => {
    setState('CONNECTING');
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      setState('CONNECTED');
      retryCount.current = 0;
      // Flush queued offline messages
      while (messageQueue.current.length > 0) {
        ws.send(messageQueue.current.shift()!);
      }
    };

    ws.onclose = (e) => {
      if (state === 'SUSPENDED') return; // don't reconnect if suspended
      setState('RECONNECTING');
      // Exponential backoff + jitter: prevents thundering herd
      const base = Math.min(1000 * 2 ** retryCount.current, 30000);
      const jitter = Math.random() * 1000;
      setTimeout(connect, base + jitter);
      retryCount.current++;
    };

    ws.onmessage = (event) => {
      // Dispatch to appropriate handler based on message type
      handleMessage(JSON.parse(event.data));
    };
  }, [url]);

  // Handle app background/foreground transitions
  useEffect(() => {
    const sub = AppState.addEventListener('change', (nextState) => {
      if (nextState === 'active' && wsRef.current?.readyState !== WebSocket.OPEN) {
        setState('RECONNECTING');
        connect();
      } else if (nextState === 'background') {
        setState('SUSPENDED');
        wsRef.current?.close(); // let OS reclaim socket — silent push will wake us
      }
    });
    return () => sub.remove();
  }, [connect]);

  // Offline message queuing: queue when disconnected, flush on reconnect
  const send = useCallback((data: string) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(data);
    } else {
      messageQueue.current.push(data);
    }
  }, []);

  return { state, send };
}
```

**Reconnection backoff reference table:**

| Attempt | Delay (max jitter) | Why |
|---------|-------------------|-----|
| 1st | 1-2s | Quick recovery from transient network flap |
| 2nd | 2-4s | Brief outage (tunnel, elevator) |
| 3rd | 4-8s | Cell tower handoff |
| 4th+ | 8-30s cap | Avoid battery drain; at this point, lean on silent push to wake |

**SSE consumption on mobile:**

```typescript
// EventSource polyfill — React Native lacks native EventSource; use a lib
import EventSource from 'react-native-sse';

function useLiveFeed(feedUrl: string) {
  const [events, setEvents] = useState<FeedEvent[]>([]);

  useEffect(() => {
    const es = new EventSource(feedUrl, {
      headers: { Authorization: `Bearer ${token}` },
      // Reconnect with backoff built into the polyfill; tune for mobile
      reconnectOnError: true,
      maxReconnectInterval: 15000,
    });

    es.addEventListener('update', (e) => {
      if (e.data) setEvents((prev) => [...prev, JSON.parse(e.data)]);
    });

    es.addEventListener('error', () => {
      // SSE connection lost — fall back to polling if persistent failure
      if (consecutiveFailures > 3) switchToPolling(feedUrl);
    });

    return () => es.close();
  }, [feedUrl]);
}
```

**Battery-efficient real-time — the golden rules:**

1. **Push-triggered fetch beats persistent WebSocket for most apps.** If your data updates every 30+ seconds, use silent push to tell the app "there's new data" and fetch on demand. A persistent WebSocket keeps the radio active — 10-20× more battery than an occasional push + fetch cycle.
2. **WebSocket only for sub-second latency requirements.** Chat, live trading, real-time collaboration. If 2-5 second delay is acceptable, silent push + fetch is always cheaper.
3. **Never hold a WebSocket open in the background.** iOS kills it within ~30 seconds; Android within a few minutes. Both platforms throttle background network. Close the WebSocket in `onBackground`, re-establish in `onForeground`. Use silent push to wake the app for important messages while in background.
4. **Batch and coalesce:** Don't send 50 individual WebSocket messages when the app returns from background — send one "sync since timestamp X" message and process the batch.

**Background modes — what survives and what doesn't:**

| Platform | Persistent connections | Silent push | Background fetch | BLE |
|----------|----------------------|-------------|-----------------|-----|
| iOS (foreground) | Yes | Yes | N/A | Yes |
| iOS (background, < 30s) | Yes (brief grace period) | Yes | Yes (opportunistic) | Yes (with capability) |
| iOS (background, > 30s) | Killed by OS | Yes (limited rate) | Yes (opportunistic, OS decides) | Yes (with capability) |
| Android (foreground) | Yes | Yes | N/A | Yes |
| Android (background) | Minutes, then killed | Yes (high-priority FCM) | Yes (WorkManager) | Yes (with foreground service) |

**What to remember:** iOS kills WebSocket connections aggressively — plan for it. Silent push is your reliable background wake mechanism on both platforms. For real-time data that must work in the background (fitness tracking, navigation), use platform-native background modes (BLE, location updates, audio) with a foreground service (Android) or capability entitlement (iOS).

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `api-designer` | OpenAPI 3.1 spec optimized for mobile (response size budgets, delta updates, partial responses), auth scheme | Before building API-consuming screens; contract-first approach |
| `ui-ux-designer` | iOS HIG vs Material Design 3 guidance, screen mockups, gesture design, platform-specific interaction patterns | Before implementing UI; platform convention compliance |
| `backend-developer` | API implementation with mobile-specific concerns, push notification payloads, batch endpoints | Before integrating with backend; ensures mobile-specific optimizations exist |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `qa-engineer` | Device coverage plan (low-end + high-end), Maestro/Detox configuration, offline/connectivity test scenarios | QA can't test without the mobile build and test harness |
| `security-reviewer` | Biometric auth implementation, Keychain/Keystore patterns, certificate pinning, jailbreak/root detection | Security review can't assess mobile-specific threats without implementation |
| `localization-engineer` | Platform-specific locale files, App Store/Play Store metadata, mobile formatting constraints | Localization pipeline can't process mobile strings in isolation |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| API version deprecation announced | Backend Developer | Retire old API surface; update mobile client with migration window |
| New push notification type added | Backend, Product Strategist | Payload design, deep-link routing, opt-in/opt-out UX |
| App Store review rejection | DevOps, Legal Advisor | Policy compliance fix, resubmission timeline |
| New permission required (camera, location, health) | Security Engineer, UI/UX Designer | Permission rationale dialog, denial handling, privacy review |
| Critical crash rate spike (>1% sessions) | QA Engineer, Observability | Immediate investigation, potential hotfix release |

### Escalation Path

```
App Store rejection? → DevOps Engineer → Legal Advisor
Security vulnerability? → Security Engineer → Compliance Officer
API breaking change? → Backend Developer lead → System Architect
Critical performance regression? → Observability Engineer → CTO Advisor
Cross-platform inconsistency? → UI/UX Designer → Product Strategist
```

## Proactive Triggers

These are signals that should trigger the mobile developer to investigate — no one needs to tag you; you should be watching for these.

| Trigger | Immediate Action |
|---------|-----------------|
| "APNs tokens failing — push notifications not delivered" | Run token rotation check: verify backend stores per-device token arrays, confirm token refresh runs on every app launch, check APNs feedback service for `410` responses. A single stale token blocks delivery to that device silently — no error on the device, just missing notifications |
| "WebSocket reconnecting in a tight loop — battery drain" | Audit reconnection logic: exponential backoff with jitter must be in place. Check that `onclose` handler isn't calling `connect()` immediately (common substring-matching bug where `ws.close()` triggers `onclose` → reconnect → close → infinite loop). Verify WebSocket is proactively closed in `AppState` background handler, not left dangling for OS kill |
| "Notification tapped but wrong screen opens" | Deep-link routing verification: trace the notification payload's deep-link URL through every routing layer. Test `myapp://product/123` resolves to `ProductScreen(id: 123)`. Check nested navigator state restoration — if a tab navigator contains a stack navigator, the deep link must activate both the tab AND push onto the correct stack |
| "App using 30% battery/hour — streaming connection never sleeps" | Background mode audit: verify WebSocket/SSE connections close on background event. Check if silent push is being used instead of persistent connections for non-latency-critical data. Profile with Xcode Energy Log / Android Battery Historian — identify which component keeps the radio active. A single unclosed WebSocket in background = 20-30% battery/hour |
| "Biometric auth prompts on every app resume — users annoyed" | Auth gate frequency audit: biometric should gate on cold start, not every foreground transition. Check `AppState` listener — ensure it tracks a session timeout (e.g., 5 minutes in background before re-prompting) rather than prompting on every resume. Over-prompting trains users to disable biometric auth |
| "Push notification permission dialog shown at app launch — 80% deny rate" | Permission timing audit: move push permission request to point of value (e.g., after user enables a notification-dependent feature). Use iOS provisional authorization (`UNAuthorizationOptionProvisional`) — delivers notifications silently to Notification Center without a dialog, then prompt later when user has seen the value. First-launch permission barrage is the #1 cause of low opt-in rates |
| "App Store rejected — 'Your app declares support for background modes but doesn't use them'" | Capability audit: remove unused `UIBackgroundModes` from Info.plist. Apple's static analyzer checks if declared background modes match actual API usage. `fetch`, `remote-notification`, `processing`, `bluetooth-central` — only declare what your code actually calls. Remove stale capabilities from old experiments |
| "Crash rate spikes on iOS major version release day" | OS compatibility audit: run your test suite against the iOS beta 2 months before public release. Check all native modules for deprecated APIs (`#available` guards). Maintain a `PlatformCompatibility.md` with per-OS-version breaking changes. iOS major version releases are predictable — the crash shouldn't be a surprise |

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

## What Good Looks Like

> The app launches cold in under 1.5 seconds, scrolls at a locked 60fps, and stays under 50MB of memory on low-end devices. Every screen renders correctly across iOS and Android — safe areas respected, Dynamic Type and font scaling honored, Dark Mode toggled seamlessly. Offline mode degrades gracefully: data syncs via CRDT-backed queues when connectivity returns, and the user never sees a frozen spinner. Push notifications route to the right screen with deep links intact. App store submissions pass review on the first attempt — privacy labels are accurate, screenshots are localized, and the binary is signed, obfuscated, and ready for phased rollout.

### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | ui-ux-designer | Design system, screen mockups, interaction patterns, platform guidelines |
| **This** | mobile-developer | Native/cross-platform implementation, navigation, offline storage, push notifications, performance optimization |
| **After** | qa-engineer | Tests on real devices, verifies offline behavior, validates platform-specific edge cases |

Common chains:
- **Design to app store**: ui-ux-designer → mobile-developer → qa-engineer — Designer defines the look and feel, mobile builds it for iOS/Android, QA validates before submission
- **API-driven mobile**: api-designer → mobile-developer → release-manager — API contract defines data, mobile builds the client experience, release manager handles app store submission

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

## Anti-Patterns
<!-- DEEP: 5min -- each anti-pattern includes machine-detectable patterns -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Persistent WebSocket in background — iOS kills it ~30s, Android within minutes. Battery drain: 20-30%/hour | Close WebSocket in `AppState` background handler. Use silent push (`content-available: 1`) to wake. Re-establish in foreground. | `grep -rn "WebSocket\|ws\.connect\|new WebSocket" src/ --include="*.ts" --include="*.tsx" \| grep -v "close\|disconnect\|AppState"` → finds WS creation without lifecycle handling | eslint rule: require `AppState.addEventListener('change')` when `WebSocket` is instantiated. CI: find WS constructors without matching `removeEventListener` |
| Storing APNs/FCM tokens as permanent — tokens change on reinstall, restore, OS update, sometimes silently | Register for push on EVERY app launch. Compare received token against stored; if different, sync to backend with `previousToken`. | `grep -rn "registerForRemoteNotifications\|getToken\|onTokenRefresh" src/ --include="*.ts" \| grep -v "AppState\|componentDidMount\|useEffect"` → finds token registration not in launch path | CI: verify `messaging().getToken()` or `registerForRemoteNotifications()` is called in `AppDelegate.m` / `MainApplication.java` on cold start |
| One-size-fits-all push payloads — ignores `mutable-content` on iOS, `channel_id` on Android | Send platform-adapted payloads: iOS gets `apns-priority`, `mutable-content`; Android gets `priority`, `channel_id`, `collapse_key` | `grep -rn "apns\|\"aps\"\|notification.*body" server/ --include="*.ts" \| grep -v "mutable-content\|apns-priority\|channel_id"` → finds push payloads without platform-specific fields | Server-side: validate push payload schema per platform before send. Fail CI if `apns.mutable-content` field missing for rich notification feature |
| Blocking splash screen on network calls — user stares at white screen for 10+ seconds in poor connectivity | Native splash screen (not JS). Start app immediately with cached config/tokens. Validate in background. Timeout at 3s — show degraded state. | `grep -rn "SplashScreen\|splash.*screen\|keep.*splash" src/ --include="*.tsx" \| grep -v "hide\|\\.preventAutoHide\|native"` → finds JS-managed splash that blocks on network | eslint rule: require `SplashScreen.hide()` to be called synchronously in root component, before any `await`. CI: Lighthouse mobile audit — fail if LCP > 2.5s |
| Caching API responses indefinitely — `max-age: 31536000`, users see stale data for days | Reasonable TTLs: 30-60s real-time, 5-15min feeds, 24h static. Pull-to-refresh. Show "last updated" timestamp. stale-while-revalidate. | `grep -rn "max-age=31536000\|cacheTime.*Infinity\|staleTime.*Infinity\|max-age.*86400" src/ --include="*.ts"` → finds infinite or day+ cache settings | TanStack Query: set `staleTime: 30_000` (30s) default. Override per-query. CI: lint check that no `staleTime > 86_400_000` unless explicitly documented |
| Hiding scroll indicators on long lists — users lose navigation context in 500-item feeds | Always show scroll indicators on content lists. Disable only for full-screen immersive (media player, game). Accessibility concern. | `grep -rn "showsVerticalScrollIndicator=\{false\}\|showsHorizontalScrollIndicator=\{false\}" src/ --include="*.tsx"` → finds hidden indicators | eslint rule: warn when `showsVerticalScrollIndicator={false}` on `FlatList`/`ScrollView` without `accessibilityRole="list"` |
| Requesting all permissions on first launch — opt-in drops 60-80% with barrage dialog | Request at point of need with rationale dialog. Show reason in-app before system dialog. Provisional notification on iOS. Respect denial. | `grep -rn "requestPermission\|requestAuthorization\|PERMISSIONS\.request" src/ --include="*.ts" \| grep -v "useEffect\|componentDidMount\|onPress\|onPress"` → finds permission requests not tied to user action | eslint rule: `requestPermission()` must be called inside an event handler (onPress/onChange/onSubmit), never in module scope or `componentDidMount` |

## Error Decoder
<!-- QUICK: 15s -- grep the console, match → fix, auto-recover -->

| 🖥️ Console Match | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `grep "LAError.*biometryLockout\|Error Domain=com.apple.LocalAuthentication.*-8"` | Face ID / Touch ID fails — user locked out of app after 5 failed biometric attempts | iOS locks biometric auth after 5 consecutive Face ID failures (3 for Touch ID). App doesn't fall back to device passcode. | Handle `LAError.biometryLockout`: present `LAPolicy.deviceOwnerAuthentication` (device passcode) as fallback. If passcode fails, show app credential login. | 1. Detect `biometryLockout` in auth handler 2. Call `context.evaluatePolicy(.deviceOwnerAuthentication, ...)` — this prompts system passcode 3. On success, biometrics auto-re-enable 4. On failure, fall back to username/password login |
| `grep "SQLITE_CORRUPT\|sqlite3_open_v2\|Database corruption detected"` | App crashes on launch — white screen, `Room` database initialization throws unhandled exception | SQLite WAL file corrupted by concurrent writes across multiple threads without WAL mode. Torn page in database file. | Enable `PRAGMA journal_mode=WAL;` after DB creation. Use single serial queue for all writes (Room auto-handles this). `PRAGMA integrity_check;` on cold launch. | 1. `PRAGMA integrity_check;` on launch 2. If failed: move corrupt DB to backup path 3. Recreate DB from schema migration 4. Restore from server in background 5. Log corruption event to crash reporter |
| `grep "NotRegistered\|FCM.*token.*invalid\|Token.*not.*registered"` | Push notifications silently stop — FCM drops messages for unregistered token | FCM token invalidated (device restore, Play Services update). Server still sends to old token. FCM returns `NotRegistered` but many backends ignore it. | On every launch: register FCM token, compare with stored. If different, send to backend with `previousToken`. Monitor `NotRegistered` in FCM send response. | 1. Detect `NotRegistered` in push send log 2. Trigger silent re-registration on client: `messaging().deleteToken()` → `messaging().getToken()` 3. Send new token to backend with old token for cleanup 4. Verify via `/push/test` endpoint: send silent push, assert receipt in 5s |
| `grep "NSPhotoLibraryUsageDescription\|Missing.*privacy.*usage.*description"` | App Store rejected — missing privacy usage description in `Info.plist` | `Info.plist` missing `NSPhotoLibraryUsageDescription` or overwritten by Expo prebuild. Simulator doesn't enforce privacy descriptions — passes locally. | Add all required privacy keys. Run `plutil -p Info.plist \| grep -E 'NS.*UsageDescription'` in CI. Test on physical device — never simulator-only for permissions. | 1. `plutil -p Info.plist \| grep -E 'NS(Camera\|PhotoLibrary\|Location\|Microphone)UsageDescription'` 2. Assert all required keys present in CI 3. Use pre-build script: `node scripts/validate-privacy-keys.js` 4. Test on physical device before submission |
| `grep "StackOverflowError\|EXC_BAD_ACCESS.*deep.*link\|deep.*link.*loop"` | Deep link opens login screen in infinite loop — app crashes after ~150 iterations, battery drains 80%→12% in 40 min | Deep link intent never consumed. Login screen's `onResume()` re-processes `intent.data` with expired auth token. Loop: deep link → auth expired → login → onResume → deep link... | Always consume deep link after processing: `intent.data = null` (Android), clear `connectionOptions` (iOS). Add loop detection: track last 5 processed links + timestamps. | 1. After processing deep link: `intent.removeExtra("deep_link")` or set `intent.data = null` 2. Store last 5 deep link URLs + timestamps in memory 3. If same link processed > 3 times in 10 seconds → break loop, show home screen 4. Test: manually revoke auth token, click deep link notification |
| `grep "BarcodeReader.*returned null\|ZXing.*no.*barcode\|MLKit.*no.*barcode"` | QR scanner shows viewfinder but never detects barcodes — silent failure, no errors | JPEG compression at quality <60 destroyed QR finder patterns (blocking artifacts blur sharp edges). ZXing tolerance is ~15% deviation; JPEG quality 30 introduces 30-40%. | Feed raw YUV/NV21 frames directly to detector (ZXing/ML Kit accept YUV natively). Only compress AFTER successful detection. Minimum quality 85 if compression is unavoidable. | 1. Verify CameraX/Metal output is YUV_420_888 or NV21 (not JPEG) 2. `grep -rn "Bitmap\.compress\|CompressFormat\.JPEG" src/ --include="*.ts" --include="*.java" --include="*.kt"` 3. If compress exists before barcode detection → remove it 4. Test: capture 50 known QR codes (varying sizes, lighting), assert all detected |

## Production Checklist
<!-- AUDIT: every item has an executable validation command -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|----------------|--------------------|----------|
| S1 | Technology selection documented: native vs cross-platform with rationale, team skills, performance requirements | `grep -rn "react-native\|flutter\|native\|swift\|kotlin" README.md ADR*.md -l \| wc -l` → must be > 0 with decision rationale | Create `docs/ADR-001-platform-choice.md` with decision matrix (performance, team skills, time-to-market, maintenance cost) |
| S2 | Navigation: deep links map to every shareable screen; universal links + app links configured | `curl -s https://example.com/.well-known/apple-app-site-association \| jq '.applinks.details[].paths'` AND `curl -s https://example.com/.well-known/assetlinks.json \| jq '.statements[].relation'` → both must return valid config | `npx uri-scheme test myapp://product/123` — assert navigation lands on ProductDetail screen |
| S3 | Auth flow: zero-flash launch (splash → resolved auth → correct screen); token refresh with retry queue; logout clears all data | `npx react-native run-ios --simulator="iPhone SE" && instrument -s "cold_launch" -t 1.5` — must show resolved screen in <1.5s, no auth-state flash | Cache auth token in Keychain/Keystore (not AsyncStorage). On launch: read token, validate synchronously, render correct screen immediately |
| S4 | Offline-first: local DB is source of truth; sync queue FIFO with conflict resolution; stale data flagged | `npx detox test --specs e2e/offline.spec.ts --device "iPhone SE"` → toggle airplane mode, perform CRUD, restore connectivity, assert sync | Implement `SyncQueue` with states: `pending → uploading → confirmed`. On `expirationHandler`: revert `uploading` to `pending` |
| S5 | Push notifications: FCM + APNs tokens registered/refreshed on each launch; deep-link routing tested per notification type | `npx react-native log-android \| grep "FCM token"` AND `npx react-native log-ios \| grep "APNs token"` — must show token refresh on each cold launch | `messaging().getToken()` in `App.tsx useEffect`, compare with MMKV-stored token, sync if changed with `previousToken` |
| S6 | Platform design: touch targets ≥ 44pt (iOS) / 48dp (Android); Dynamic Type + font scaling; Dark Mode; Safe Area | `npx eslint --rule '{"react-native/no-inline-styles": "warn"}' src/ \| grep "width\|height\|minWidth"` → review for hardcoded touch target sizes | Replace hardcoded sizes with `Platform.select({ ios: 44, android: 48 })`. Use `Pressable` with `hitSlop` for small icons |
| S7 | Permissions: requested at point of need with rationale; denial gracefully handled with settings deep link | `grep -rn "requestPermission\|requestAuthorization" src/ --include="*.ts" \| grep -v "useEffect\|onPress\|onPress"` → must be empty (permission requests must be user-initiated) | Wrap permission requests in `Alert.alert("Camera needed", "To scan QR codes", [...]) → Linking.openSettings()` on denial |
| S8 | Biometric auth: implemented with device credential fallback; sensitive data re-validated server-side | `grep -rn "deviceOwnerAuthentication\|BIOMETRIC_WEAK\|setUserAuthenticationRequired" src/ --include="*.ts" \| wc -l` → must be > 0 | Handle `biometryLockout`: present `deviceOwnerAuthentication` (passcode). Fall back to username/password if passcode fails too |
| S9 | Performance: cold start < 1.5s (low-end device); 60fps scrolling on 1000+ items; memory < 50MB on 2GB RAM | `npx react-native perf-test --scenario coldStart --device "iPhone SE" --assert-duration 1500` AND `--scenario scrollList --items 1000 --assert-fps 60` | Profile with Xcode Instruments (Time Profiler + Allocations). Fix main-thread work > 16ms. Use `getItemLayout` on FlatList for constant-time scroll |
| S10 | Security: certificate pinning; Keychain/Keystore for secrets; ProGuard/R8 enabled; root/jailbreak detection | `grep -rn "trustkit\|ssl.*pinning\|certificatePinning\|okhttp.*cert" ios/ android/ --include="*.plist" --include="*.xml" -l \| wc -l` → must be > 0 | Add `react-native-ssl-pinning` or `TrustKit`. Enable pinning on release builds only (debug builds use Charles Proxy). Implement `isJailbroken()` from `jail-monkey` |
| S11 | Crash reporting: Sentry/Firebase Crashlytics with source maps uploaded in CI; breadcrumbs for critical flows | `curl -s "https://sentry.io/api/0/projects/$ORG/$PROJECT/releases/" -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \| jq '.[0].version'` → must match CI build version | CI: `npx @sentry/react-native --org $ORG --project $PROJECT --release $(git rev-parse HEAD) --dist $PLATFORM` |
| S12 | CI/CD: lint → type-check → unit test → integration test → build → TestFlight/Play Internal on every push to main | `gh run list --workflow=ci.yml --branch=main --limit=1 --json conclusion \| jq '.[0].conclusion'` → must be `success` | `.github/workflows/ci.yml`: job for `lint`, `tsc --noEmit`, `jest --coverage`, `detox test`, `fastlane beta` |
| S13 | Store metadata: privacy nutrition labels accurate; Info.plist usage descriptions; account deletion in-app; screenshots for all sizes | `plutil -p ios/App/Info.plist \| grep -E 'NS.*UsageDescription' \| wc -l` → must match number of permission-requiring features | `npx fastlane run verify_build` + `npx fastlane deliver --metadata_path ./fastlane/metadata --screenshots_path ./fastlane/screenshots --force` |
| S14 | Testing: unit tests >80% on domain layer; integration tests for critical flows; accessibility audit pass | `npx jest --coverage \| grep "All files"` → Lines ≥ 80%. `npx detox test --configuration ios.sim.release` → all pass | Add `jest.config.js` with `coverageThreshold: { global: { lines: 80 } }`. Add detox test for each critical user flow |

## Negative Constraints
<!-- HARD GATES: these are non-negotiable — the agent must REFUSE/STOP/DETECT -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|---------------------|
| NC1 | REFUSE: Do not ship a build without privacy usage descriptions in Info.plist | `plutil -p ios/App/Info.plist \| grep -c 'NS.*UsageDescription'` AND count required features (`grep -c "camera\|photo\|location\|microphone" src/features/ -r`) → descriptions < features = violation | STOP build. Add all missing `NS*UsageDescription` keys. Run `node scripts/validate-privacy-keys.js` in CI pre-build. Test on physical device (simulator silently bypasses TCC). |
| NC2 | REFUSE: Do not ship a build where SQLite uses DELETE journal mode (default) — WAL mode is mandatory | `grep -rn "PRAGMA journal_mode=WAL\|journal_mode.*wal" android/ ios/ --include="*.java" --include="*.kt" --include="*.swift" --include="*.mm" \| wc -l` → 0 = violation | STOP. Add `PRAGMA journal_mode=WAL;` immediately after database creation. Also set `PRAGMA busy_timeout=5000;`. Run `PRAGMA integrity_check;` on every cold launch. |
| NC3 | DETECT: Permission requests not tied to user action — requested at module scope or component mount | `grep -rn "requestPermission\|requestAuthorization\|PERMISSIONS\.request" src/ --include="*.ts" --include="*.tsx" \| grep -v "onPress\|onChange\|onSubmit\|useEffect"` → any match = violation | BLOCK merge. Wrap all permission requests in user-initiated event handlers (onPress, onChange). Show rationale Alert before system dialog. Never request in `componentDidMount` or module top-level. |
| NC4 | REFUSE: Do not ship a build with certificate pinning disabled in release configuration | `grep -rn "sslPinning.*false\|trustkit.*disabled\|pinning.*disable\|okhttp.*trustAll" ios/ android/ --include="*.plist" --include="*.xml" --include="*.kt" \| grep -v "debug\|test\|\.spec"` → any match in release config = violation | STOP. Enable certificate pinning via TrustKit (iOS) or OkHttp CertificatePinner (Android). Use `if (BuildConfig.DEBUG) { disablePinning() }` pattern — never disable in release. |
| NC5 | DETECT: Deep link intent not consumed after processing — causes infinite navigation loops | `grep -rn "getInitialURL\|onNewIntent\|application.*open.*url" src/ --include="*.ts" --include="*.java" --include="*.kt" --include="*.swift" -A 5 \| grep -v "intent\.data\s*=\s*null\|removeExtra\|handled\|consumed"` → processing without consumption = violation | BLOCK merge. After processing deep link: Android: `intent.data = null` or `intent.removeExtra("deep_link")`. iOS: clear `connectionOptions` in handler. Add loop detection: track last 5 processed links, break if same URL processed > 3 times in 10s. |
| NC6 | REFUSE: Do not use `dangerouslySetInnerHTML` or `WebView.injectJavaScript` for user-generated content in mobile apps | `grep -rn "dangerouslySetInnerHTML\|injectJavaScript\|evaluateJavascript" src/ --include="*.tsx" \| grep -v "test\|\.spec"` → any match in production code = violation | STOP. Replace with `Text` components + sanitized markdown. `WebView` with `injectJavaScript` on UGC is XSS in mobile. Only allow `injectJavaScript` on static, developer-controlled content. |
| NC7 | DETECT: Biometric auth implemented without device passcode fallback — users permanently locked out after biometryLockout | `grep -rn "biometric\|FaceID\|TouchID\|BiometricPrompt" src/ --include="*.ts" -A 10 \| grep -c "deviceOwnerAuthentication\|BIOMETRIC_STRONG\|passcode\|credential"` → fallback count = 0 = violation | BLOCK merge. Add `deviceOwnerAuthentication` (system passcode) fallback. On `biometryLockout`: present passcode → success re-enables biometrics. Final fallback: app credentials login. Never gate app exclusively on biometrics. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can build screens that look good in the simulator but your app crashes after 3 days in the background — you blame "the OS killed it" | Your app survives a 4-hour background session, airplane mode toggle mid-sync, and OS-level force-kill without data loss — verified by automated test | Your app has a 4.8+ star rating on both stores with >100K installs, <0.1% crash-free session rate in Firebase Crashlytics, and you haven't received a "data loss" support ticket in 12 months |
| You treat permissions as a checkbox — add the key to `Info.plist` and move on | You handle every permission state: not-determined (show rationale dialog before requesting), denied (show settings deep-link), restricted (explain parental controls), and authorized (proceed) — plus the "iOS silently discards early prompts" edge case | You onboard a new developer and within their first week, they can add a camera feature with correct permission handling on both platforms without asking you — because your permission abstractions are self-documenting |
| You test on your daily-driver flagship phone and assume "it works everywhere" — your Pixel 8 Pro has 12GB RAM, so everything feels fast | You own a test device farm: a 3-year-old budget Android (2GB RAM), an iPhone SE 2nd gen, and an iPad with split-screen. Every PR is tested on the lowest-spec device in your fleet | You can predict, within 10%, the crash rate of a feature before it ships — based on your knowledge of OS background limits, memory pressure behavior, and the device fragmentation matrix — and you're right >80% of the time |

**The Litmus Test:** Ship an app that survives: (a) no connectivity for 2 hours (airplane mode, local operations queued), (b) an OS-level force-kill mid-sync (swipe-up kill while data is uploading), (c) a biometric lockout (5 failed Face ID attempts → fallback to device passcode → fallback to app credentials), and (d) background termination on a 2GB RAM device with 15 other apps open. After all four scenarios, the app must: reopen to the correct screen, have zero data loss, and show no stale/corrupted state. If you can't prove this with automated tests, you're not L3.

## Deliberate Practice
<!-- DEEP: 10+min — how to improve, not just what you do -->

### The Mobile Improvement Loop
1. **Deploy to the worst device you own** — A 3-year-old budget Android with 4G throttling. Use it as your daily driver for one day.
2. **Find every friction point** — Slow startup? Janky scroll? Background kill? Permission denied with no explanation? Empty state in airplane mode?
3. **Fix the worst offender** — Then redeploy and test again. Did the experience improve for that device class?
4. **Rotate devices monthly** — Different device, different OS version, different network conditions. Your app works differently on all of them.

### Practice Routines
| Skill Level | Practice | Frequency | Expected Result |
|-------------|----------|-----------|-----------------|
| Novice → Competent | Build the same app (camera + list + detail) natively in Swift and Kotlin, then in React Native and Flutter. Compare code, performance, and platform feel | Monthly per platform | Understands the tradeoffs between cross-platform and native from lived experience, not documentation |
| Competent → Expert | Run the Android Strict Mode and iOS Instruments on your app. Fix every violation: disk reads on main thread, overdraw, memory leaks, retain cycles | Quarterly | App is verified clean by platform tooling, not by developer assumption |
| Expert → Master | Ship an app to production on a platform you've never shipped to before. Go through the full store review process | Annually | Understands the platform's review criteria, provisioning, signing, and release management — not just its API surface |

### The One Thing
**Delete your app and reinstall it. On a device you've never used for development. On a slow network. With no account pre-created.** The first-run experience you see is what every new user sees. If it's not delightful, nothing else in the app matters.

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
