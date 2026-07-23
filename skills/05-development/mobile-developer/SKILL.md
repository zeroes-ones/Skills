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
<!-- QUICK: 30s -- pick your path, skip the rest -->
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

These are the patterns that cause production incidents, battery drain, and app store rejections. Recognize them early.

| ❌ Anti-Pattern | ✅ Do This Instead |
|-----------------|--------------------|
| **Persistent WebSocket in background** — keeping a WebSocket open when the app enters background, hoping the OS will maintain it. iOS kills it within ~30s; Android within minutes. Battery drain: 20-30%/hour | Close WebSocket in `AppState` background handler. Use silent push (`content-available: 1`) to wake the app when there's new data. Re-establish WebSocket in foreground handler. The user won't notice the 50ms reconnection delay |
| **Storing APNs/FCM tokens as permanent** — registering for push once on first launch and never refreshing. Tokens change on reinstall, device restore, OS update, and sometimes silently | Register for remote notifications on EVERY app launch. Compare received token against stored; if different, sync to backend immediately. Store `lastUpdated` timestamp alongside token. Implement a push test endpoint to verify the pipeline end-to-end |
| **One-size-fits-all push payloads** — sending identical notification payloads to iOS and Android, ignoring platform-specific capabilities. Leads to missing rich media on one platform, broken deep links on another | Send platform-adapted payloads: iOS gets `apns-priority`, `apns-push-type`, `mutable-content`; Android gets `priority`, `channel_id`, `collapse_key`. Use per-platform payload fields in your backend push service |
| **Blocking splash screen on network calls** — fetching config, auth tokens, or feature flags on the splash screen with no timeout. User stares at splash for 10+ seconds in poor connectivity | Native splash screen (not JS/Flutter splash). Start app immediately with cached config/tokens. Validate in background. Timeout at 3s maximum — show the app with degraded state rather than blocking. A frozen splash screen looks like a crash |
| **Caching API responses indefinitely** — setting `Cache-Control: max-age=31536000` or never invalidating TanStack Query caches. Users see stale data days after the server updated | Set reasonable cache TTLs: 30-60s for real-time data, 5-15min for content feeds, 24h for static reference data. Always provide a pull-to-refresh mechanism. Show a "last updated" timestamp so users know data freshness. stale-while-revalidate pattern: serve cached data immediately, update in background |
| **Hiding scroll indicators on long lists** — removing `showsVerticalScrollIndicator={false}` or setting it globally. Users have no idea how far through a 500-item list they are | Always show scroll indicators on content lists. The indicator provides navigation context — "am I 10% or 90% through this feed?" Disable only for full-screen immersive experiences (media player, game). This is an accessibility concern too |
| **Requesting all permissions on first launch** — a permission barrage dialog for camera, location, contacts, notifications, and microphone before the user has seen any value. Opt-in rates drop 60-80% | Request each permission at the point of need with a rationale dialog. Show the permission reason in-app before the system dialog. Use provisional notification auth on iOS (delivers silently first). Respect denial — show a disabled state with Settings link, never re-prompt aggressively |

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| App Store rejected the build — "Your app collects user data without disclosure" | Background location collection was enabled but the privacy nutrition label on App Store Connect didn't list location data. Apple flagged the mismatch during review | Update privacy nutrition labels in App Store Connect to match all data collected. Add a privacy manifest (iOS 17+) that declares all data collection reasons. Run a privacy diff scan before each submission | **App Store privacy labels must match what your code actually does.** Apple's automated scanning checks APIs used vs. privacy labels declared. A mismatch means rejection. Maintain a privacy data inventory and scan it against your app binary before every release |
| App crashed immediately on iOS 18 beta — 100% crash rate for beta testers | Native module used `UIPasteboard` API that was deprecated and removed in iOS 18 beta without a replacement fallback | Check iOS 18 API diffs before beta season. Use `#available(iOS 18, *)` checks with fallback paths. Add beta OS testing to the CI matrix (iOS 18 beta + Android 15 beta). Maintain a `PlatformCompatibility.md` file with known breaking changes per OS version | **Beta OS versions WILL break your native modules.** Apple and Google deprecate APIs aggressively. Add beta OS testing to your CI before the public release. Always have a fallback path for every platform-specific API call. A 100% crash rate on day 1 of a new OS release is a fire drill you shouldn't have |
| User edited a todo on their phone while offline — the edit was silently lost when connectivity returned | Offline sync used last-write-wins without conflict resolution. The user's offline edit was overwritten by the server's stale version when sync ran | Implement CRDT-based conflict resolution or version vector tracking. Show the user a "sync pending" indicator during offline. If conflict is detected, show both versions and let the user choose. Test offline scenarios with the network link conditioner | **Offline without conflict resolution is silent data loss.** Last-write-wins assumes the server always has the latest data — wrong for offline edits. Every offline-first app needs a conflict resolution strategy (CRDT, version vectors, or user-facing merge UI) |
| Push notifications stopped working after app update — no errors logged | APNs token changed after the update (iOS rotates tokens on reinstall and sometimes on updates) but the app didn't re-register for push notifications on launch | Always register for remote notifications on every app launch, not just on first install. Store the most recent token and sync it to the backend. Implement a push notification test endpoint that sends a silent notification to verify the pipeline | **Push notification tokens are ephemeral — never cache them as permanent.** Register for push on every app launch. iOS can rotate APNs tokens silently. A test endpoint that sends a silent notification is the only way to verify the push pipeline end-to-end |
| Biometric auth was bypassed — user could access the app without Face ID after a force quit | Biometric auth was gating the app on resume but not on cold start. After killing and reopening the app, the gate was skipped | Implement biometric auth check on BOTH cold start AND app resume (foreground). Use `AppState` listener in React Native or `applicationWillEnterForeground` in iOS to re-prompt. Test: kill app → reopen → should see biometric prompt | **Auth gates must fire on every entry point, not just backgrounding.** Cold start bypass of biometric auth is a common oversight. Test all app launch paths: fresh install, force quit, background → foreground, and notification tap. One path without auth = data accessible without authentication |
| WebSocket reconnecting in a tight loop — battery drained to zero in 2 hours | `onclose` handler calls `connect()` immediately with no backoff. Even worse: `ws.close()` triggers `onclose` → calls `connect()` → gets open → immediately calls `close()` for cleanup → infinite loop | Implement exponential backoff with jitter in the `onclose` handler: `base = min(1000 * 2^retries, 30000) + random(0, 1000)`. Add a guard: if `ws.close()` was called intentionally, set a `shouldReconnect = false` flag to prevent the reconnect loop. Profile with Xcode Energy Log to verify radio activity settles when app is idle | **Exponential backoff with jitter is mandatory for any reconnect loop.** Without it, a brief server outage triggers a reconnection storm across all devices simultaneously — this is the "thundering herd" problem. Jitter spreads reconnection attempts across a time window, preventing the server from being overwhelmed on recovery |
| Deep link opens app but shows home screen — notification tap leads to wrong destination | The deep-link path `/product/123` resolves in the URL handler but the navigation stack isn't properly restored. If a tab navigator wraps a stack navigator, the deep link must first switch to the correct tab, THEN push onto that tab's stack | Implement a two-phase deep-link handler: (1) navigate to the root destination (tab), (2) in the `navigationReady` callback, push the detail screen with params. Test every deep-link path with the app in every possible state: fresh install, backgrounded, killed, on a different tab. Use `linking.getInitialURL()` for cold-start deep links and `linking.addEventListener('url', ...)` for warm-start | **Deep links must handle every app lifecycle state.** A deep link that works when the app is backgrounded may fail on cold start because the navigation tree hasn't mounted yet. Cold start deep links need explicit handling — `getInitialURL()` + deferred navigation until the root navigator reports `isReady` |
| Background fetch works in development but never fires in production | iOS delivers background fetch at its discretion based on the user's usage patterns. If the user rarely opens the app, iOS deprioritizes it. Android's WorkManager similarly defers work based on battery optimization and Doze mode | Don't rely on background fetch for time-critical operations. Use silent push (`content-available: 1`) for reliable wake — Apple limits rate but guarantees delivery order. On Android, use high-priority FCM data messages. Set `BGTaskScheduler` minimum fetch interval to `15 * 60` (15 minutes) and expect actual delivery to be much less frequent. Log every background fetch invocation to measure real-world delivery rate | **Background fetch is opportunistic, not guaranteed.** Apple and Google control when background tasks run to preserve battery. Silent push is more reliable for time-sensitive wake-ups. If you need guaranteed background execution (e.g., uploading photos), use a background URLSession (iOS) or foreground service (Android) |
| Notification permission dialog shown but user never sees it — dialog dismissed instantly | The permission dialog was triggered before the app's `UIWindow` was fully presented, or the app called `requestAuthorization` inside `applicationDidFinishLaunching` before the root view controller appeared. iOS silently dismisses early permission prompts | Delay permission request until the root view controller's `viewDidAppear` has fired. In React Native, request in a `useEffect` with a 500ms delay after mount — never in the module's top-level code. On Android 13+, use `POST_NOTIFICATIONS` at point of need, not in `Application.onCreate()`. Test permission flow after a fresh install (delete app, reinstall, verify dialog appears and is tappable) | **Permission dialogs presented before the app's window is ready are silently discarded by iOS.** The user never sees the dialog, your code receives `.denied` as the authorization status, and you have no way to re-prompt. This is one of the hardest bugs to detect because the dialog simply never appears |
| Face ID / Touch ID fails with `LAError.biometryLockout` — user locked out of app | Too many failed biometric attempts. iOS locks biometric auth after 5 consecutive failures (Face ID) or 3 (Touch ID). The app doesn't fall back to device passcode, leaving the user stuck at the biometric prompt forever | Handle `LAError.biometryLockout` explicitly: present the system device passcode dialog (`LAPolicy.deviceOwnerAuthentication`) as a fallback. This lets the user unlock with their passcode, which also re-enables biometrics. If passcode fails too, show the app's own credential-based login as a last resort. Never leave the user with only a biometric gate — Face ID can fail for many reasons (face covering, lighting, angle, wet fingers for Touch ID) | **Biometric auth is a convenience, not a gate.** Always have a fallback to device passcode, then to app credentials. `biometryLockout` is common — it happens every time a user hands their phone to a child or wears a face mask. Without a fallback, the user is permanently locked out until they manually go to Settings → Face ID & Passcode |
| FCM token invalidated on server but app still sends with old token — push silently fails for this device | The FCM token was refreshed (device restored, app data cleared, Google Play Services updated) and the server received the new token via `onTokenRefresh`, but the server's old-token cleanup failed due to a race condition. The app's local cache still holds the stale token, and the server doesn't reject it explicitly — FCM just silently drops messages for unregistered tokens | On every app launch: register for FCM token, compare with locally stored token. If different, send to backend with `previousToken` for server-side dedup and old-token cleanup. Implement a `/push/unregister` endpoint that removes tokens explicitly. Monitor FCM response codes: `NotRegistered` means the token was invalidated — trigger a client-side re-registration. Never assume an FCM token stored in SharedPreferences/MMKV is still valid | **FCM token invalidation is silent — no error on the client, no error on the server, just undelivered messages.** The only hint is FCM's `NotRegistered` error in the send response, which many backends ignore. Always send old token alongside new token so the server can clean up. A token validation endpoint (send silent test push, confirm receipt in 5 seconds) is the only way to know if a token is still live |

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
