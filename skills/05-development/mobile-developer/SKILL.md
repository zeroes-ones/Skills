---
name: mobile-developer
description: >
  Use when building cross-platform mobile applications with React Native or Flutter,
  implementing offline-first architecture, configuring push notifications, or preparing
  app store deployments. Handles navigation patterns, state management, platform-specific
  design systems, biometric authentication, and deep linking. Do NOT use for web
  frontend development, backend API design, DevOps infrastructure, or desktop
  application development.
author: Sandeep Kumar Penchala
license: MIT
type: development
status: stable
version: 1.1.0
updated: 2026-07-23
tags:
- react-native
- flutter
- ios
- android
- offline-first
- push-notifications
- app-store
token_budget: 4000
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
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

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

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.

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

## What Good Looks Like

> The app launches cold in under 1.5 seconds, scrolls at a locked 60fps, and stays under 50MB of memory on low-end devices.

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | ui-ux-designer | Design system, screen mockups, interaction patterns, platform guidelines |
| **This** | mobile-developer | Native/cross-platform implementation, navigation, offline storage, push notifications, performance optimization |
| **After** | qa-engineer | Tests on real devices, verifies offline behavior, validates platform-specific edge cases |

Common chains:
- **Design to app store**: ui-ux-designer → mobile-developer → qa-engineer — Designer defines the look and feel, mobile builds it for iOS/Android, QA validates before submission
- **API-driven mobile**: api-designer → mobile-developer → release-manager — API contract defines data, mobile builds the client experience, release manager handles app store submission

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

## Gotchas

- **App store rejection at launch.** Apple and Google reject apps for common violations: using private APIs, missing privacy labels, incomplete permission descriptions, or placeholder content. Each rejection adds 1-3 days to the review queue. At launch, every day of delay costs revenue, marketing spend (ads already running with no product), and team morale. **Total cost: $10K-$50K per rejection in delayed revenue, wasted marketing spend, and rework by the engineering team racing to fix and resubmit.** Fix: submit for review 2 weeks before launch date. Run through the full App Store Review Guidelines checklist before submission. Budget for at least one rejection in your launch timeline.
- **No offline mode.** Apps that show a white screen or crash when connectivity drops get 1-star reviews mentioning "doesn't work on the subway/plane." These reviews persist forever and directly reduce conversion from search results. Apps with no offline support see 25-40% lower ratings in regions with patchy connectivity (emerging markets, rural areas). **Total cost: $15K-$50K in lost downloads from negative reviews — a 0.5-star rating drop can reduce install conversion by 30%.** Fix: implement a local-first architecture. Cache last-known-good data. Show cached content with a "you're offline" banner instead of errors. Test every screen in airplane mode.
- **App bundle size above 150MB (cellular download limit).** Both Apple and Google show a warning when users try to download apps over 150MB (iOS) or 150MB (Android Play Store) via cellular. Users on metered connections — the majority in many markets — abandon the install. **Total cost: $20K-$100K in lost installs. App install conversion drops 1% for every 6MB over 100MB (Google internal data).** Fix: use App Thinning/Slicing (on-demand resources, asset catalogs). Compress images to WebP/AVIF. Remove unused native libraries. Audit bundle with `npm run bundle-analyzer` or Android Studio's APK Analyzer every release.
- **Missing accessibility on mobile.** The ADA and Section 508 apply to mobile apps — not just websites. A lawsuit or DOJ demand letter over an inaccessible app costs $10K-$50K to settle (legal fees + remediation), plus mandated accessibility fixes under court order. **Total cost: $10K-$50K in settlements and remediation per complaint, before accounting for lost users (15% of the population has a disability).** Fix: enable TalkBack/VoiceOver and navigate your entire app. Set `accessibilityLabel` on every interactive element. Maintain minimum 4.5:1 contrast ratio. Test with Accessibility Scanner (Android) and Accessibility Inspector (iOS) before every release.

- **React Native's `console.log`** in production builds on iOS appears in the device logs — it doesn't get stripped. Sensitive data logged during development ships to production if not behind `__DEV__` guards.
- **`AsyncStorage`** has a 6MB limit on Android (varies by device). Large JSON blobs silently fail with no error callback. Chunk data over 1MB or use SQLite for structured storage.
- **iOS Simulator networking** uses the host Mac's network directly. `localhost` works. Android Emulator uses a virtual router at `10.0.2.2` to reach host `localhost`. Code that works in iOS sim will silently fail on Android em.
- **Keyboard avoidance**: `KeyboardAvoidingView` with `behavior="padding"` works on iOS but not Android (Android adjusts the window size automatically). Using `padding` on Android double-shifts the content.
- **`Image.prefetch()`** has a 50MB disk cache on iOS and no disk cache on Android (Android clears on app close). Don't rely on prefetch for offline image availability on Android.
- **App State (`AppState.currentState`)** on iOS reports `"inactive"` during Control Center pull-down. If you pause video on `"background"` only, your video keeps playing when the user opens Control Center.

## Verification

- [ ] Run `npm test` / `flutter test` / XCTest — all tests pass
- [ ] Build for both platforms: `npx react-native run-ios` AND `npx react-native run-android` (or Flutter equivalents) — both build without error
- [ ] Test on physical device (not just simulator): touch interactions, scroll performance, keyboard behavior
- [ ] Test offline: enable airplane mode — app shows cached data, not crash/white screen
- [ ] Test permissions: deny camera/location/notifications — app degrades gracefully with explanation
- [ ] Verify app size: `du -sh` the built .ipa/.apk — within budget (< 20% increase from baseline)

## References

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Negative Constraints**: See [negative-constraints.md](references/negative-constraints.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)

