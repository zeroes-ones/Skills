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

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---:|
| "It works on my iPhone 16 Pro — we'll test on older devices before launch." | The median global user has a $200 Android phone with 4GB RAM on intermittent connectivity. Your flagship-device testing is testing for 5% of your users. A crash on a budget device isn't a bug — it's a 1-star review and an uninstall. Budget device is your primary test target, not an afterthought. |
| "Offline support is an edge case — 95% of users have connectivity." | Every user loses connectivity — elevators, subways, tunnels, rural roads. A blank screen or infinite spinner on connection loss looks like a crash. Users don't blame the network — they blame your app. Cache-last-known-state is 2 days of work. A 1-star review lasts forever. |
| "This API key is embedded in the app, but nobody's going to decompile it." | `strings app.apk | grep apiKey` takes 3 seconds. Every secret in your binary is public. One exposed API key costs real money in abuse charges and forces an emergency rotation that breaks every installed app version. Keystore/Keychain + server-side proxy is the only safe path. |
| "Full-resolution images look better — downsampling degrades quality." | A 12MP photo decoded at full resolution consumes ~36MB of RAM — enough to OOM-crash a device with 4GB. Users can't see the difference between a 12MP and a viewport-sized image on a 6-inch screen, but they absolutely notice when your app crashes scrolling through photos. Downsample to display size. |
| "We only support iOS 17+/Android 14+ — nobody's on older versions anyway." | iOS adoption rates are high, but Android fragmentation is real. 25%+ of Android users are on versions older than your target. One unguarded API call on an older device = instant crash = 1-star review. A `@available` check costs two lines of code. A crash costs a user permanently. |

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

These rules are non-negotiable constraints that detect mobile development mistakes before they are given. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE main-thread blocking operations | Trigger: Synchronous network call, file I/O, database query, or JSON parsing running on the UI thread — grep for `DispatchQueue.main` (iOS) wrapping async work, `suspend` functions called without `withContext(Dispatchers.IO)` (Android), or `URLSession.data` with `DispatchSemaphore.wait()` | STOP. Respond: "Main-thread blocking at [file:line]. UI-thread I/O causes ANR dialogs (Android, 5s threshold) or watchdog termination (iOS, crash in <1s on launch). Move to background: `withContext(Dispatchers.IO) { }` (Kotlin) or `Task { await }` on a background actor (Swift). Never `.wait()` on the main thread." |
| R2 | DETECT no offline or error state — blank screen on connectivity loss | Trigger: Network call (`fetch`, `URLSession.dataTask`, `Retrofit.enqueue`) has no `.catch()` / `onError` / `Result.failure` handler AND has no cached-data fallback — silent failure renders a blank screen or infinite spinner | STOP. Respond: "No offline/error fallback at [file:line]. Every network call must handle three states: loading, success, AND failure. On failure: show cached data if available, a retry button, AND a human-readable error message. Never show a blank screen or unending spinner — those look like app crashes to users." |
| R3 | REFUSE hardcoded API keys, tokens, or secrets in client binary | Trigger: String literal matching `apiKey`, `clientSecret`, `token`, `password`, `privateKey`, or base64-encoded blob ≥ 20 chars embedded in client-side source (`.swift`, `.kt`, `.tsx`, `.dart`) — these are extractable via `strings` command or decompilation | STOP. Respond: "Hardcoded credential at [file:line]. Secrets in client binaries are extracted trivially — `strings app.apk | grep apiKey` takes seconds. Use: Android Keystore / iOS Keychain for on-device secrets, OAuth PKCE for auth tokens, and a server-side proxy for third-party API keys. Rotate any exposed credential immediately." |
| R4 | DETECT missing lifecycle-aware subscription management | Trigger: View/ViewController/Composable subscribes to a data stream (Flow, Publisher, Observable, Combine pipeline) but does NOT cancel/dispose in `onPause`+`onDestroy` (Android) or `viewDidDisappear`+`deinit` (iOS) — subscription outlives the view, accumulating in memory | STOP. Respond: "Leaked subscription at [file:line]. Subscriptions that outlive their view cause memory leaks and stale-data bugs. Android: collect in `repeatOnLifecycle(Lifecycle.State.STARTED)` or cancel in `onStop()`. iOS: store in `Set<AnyCancellable>` and cancel in `viewDidDisappear`. Every subscription must have a bound lifecycle." |
| R5 | DETECT full-resolution image loaded without downsampling | Trigger: Image loading call (`Glide.load()`, `Picasso.load()`, `AsyncImage`, `Image(uiImage:)`) with source > 2MB and no `override()`, `resize()`, or `downsampling` option — full bitmap decoded into memory | STOP. Respond: "Unsampled image at [file:line]. A 12MP photo decoded at full resolution consumes ~36MB of RAM — enough to OOM-crash a device with 4GB RAM. Add downsampling: `Glide.with(context).load(url).override(targetWidth, targetHeight).centerCrop()` or `Image(uiImage: downsampledImage)`. Never decode more pixels than the viewport displays." |
| R6 | REFUSE permission request without rationale or purpose string | Trigger: `requestPermission()` / `requestAuthorization()` called without a preceding rationale UI (Android `shouldShowRequestPermissionRationale` flow) or without a `NSCameraUsageDescription` / Info.plist purpose string (iOS) | STOP. Respond: "Permission requested without rationale at [file:line]. Apple rejects apps missing purpose strings in Info.plist (binary reject, 3-day review reset). Android users deny unexplained requests at 2x the rate. Show a rationale dialog BEFORE the system prompt explaining why the permission is needed and what value it delivers to the user." |
| R7 | DETECT platform API call without version guard | Trigger: API symbol requires iOS 17+ or Android 14+ (API 34) but is called with no `@available(iOS 17, *)` check (Swift) or `if (Build.VERSION.SDK_INT >= 34)` guard (Kotlin), AND `deploymentTarget`/`minSdkVersion` is set lower — will crash on older devices | STOP. Respond: "Unguarded API at [file:line]. `[symbol]` requires [platform] [version]+ but your deployment target is lower. Wrap with: `if #available(iOS 17, *) { ... } else { /* graceful fallback */ }` or `if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE)`. Crash on older devices = 1-star review + uninstall."
| R8 | **ANCHOR to runtime versions before generating platform-specific code.** Never generate SwiftUI/UIKit/Jetpack Compose/React Native/Flutter API calls from training data alone — platform SDKs change with every OS release and Expo/Flutter versions introduce breaking API changes. | Trigger: skill receives code-generation task involving platform-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect React Native/Expo/Flutter versions → for native iOS/Android, check `ios/Podfile.lock` and `android/build.gradle` for SDK versions → anchor all API calls to detected versions | STOP. Respond: "Detected: {platform} SDK {version}. Anchoring all API calls to this version. I will flag any APIs that may have changed in more recent OS releases with // VERIFY: comments. See `scripts/references/source-of-truth-anchoring.md`." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
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

### Solo Developer
- React Native or Flutter for cross-platform — single codebase for both stores
- Expo managed workflow for zero-config builds, OTA updates via EAS Update
- SQLite (WatermelonDB or drift) for local persistence with sync queue
- Firebase Authentication + Firestore for backend-less MVPs
- TestFlight Internal + Google Play Internal Testing for distribution
- Manual store submission — no CI/CD pipeline yet

### Small Team (2-5)
- React Native CLI or Flutter with platform-specific native modules as needed
- TanStack Query + Zustand for state management, SQLite + MMKV for storage
- GitHub Actions or Codemagic for CI/CD: lint → test → build → deploy to TestFlight/Play Console
- Feature flags via Firebase Remote Config or LaunchDarkly for phased rollout
- Maestro or Detox for E2E testing on both platforms
- Device lab: top 5 devices by market share, automated perf tests on lowest-spec device

### Medium Team (5-20)
- Native modules for performance-critical features (camera, AR, Bluetooth LE)
- Shared business logic in Kotlin Multiplatform (KMM) or C++ for truly cross-platform logic
- Design system with platform-adaptive components (iOS HIG + Material Design 3)
- Over-the-air updates with CodePush or EAS Update for JS bundle changes
- Automated store submission with Fastlane: screenshots, metadata, phased rollout
- Performance regression CI gate: cold start, scroll FPS, memory on low-end device

### Enterprise (20+)
- Native iOS (Swift/SwiftUI) and Android (Kotlin/Compose) teams with shared KMM business logic
- Microfeature architecture with SPM (iOS) and Gradle modules (Android)
- Platform team maintaining internal framework, CI templates, and device lab
- Automated accessibility CI gate blocking merges on violations
- SLO-driven reliability: crash-free rate >99.9%, cold start p95 < 2s
- A/B testing framework with feature flags, phased rollout, and automated rollback on crash rate spike

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

## Decision Trees **(QUICK)**

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

## Core Workflow **(STANDARD)**

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


## Best Practices

1. **Design for offline-first from day one, not as a retrofit.** Cache last-known-good data locally using SQLite (React Native), Hive/Isar (Flutter), or Core Data/SwiftData (native). Show cached content with a discreet "offline" indicator — never a white screen or crash. Queue mutations locally and sync when connectivity returns. Test every screen in airplane mode before merge.

2. **Respect the app lifecycle on every platform.** iOS: handle `scenePhase` changes (active → inactive → background). Android: handle `onPause`/`onStop`/`onDestroy` and process death. Save critical state in `onPause` because `onStop` is not guaranteed. React Native: use `AppState` listener but remember it fires `"inactive"` during Control Center pull-down on iOS — don't pause media on inactive, only on background.

3. **Test on the lowest-spec target device, not the flagship on your desk.** If your target is $200 Android devices with 2GB RAM, test on one. Cold start times, scroll FPS, and memory usage on low-end devices are what your real users experience. Gate every release on performance metrics measured on a representative low-end device. A 10-second cold start on a budget phone drives 53% user abandonment.

4. **Minimize wake locks and background processing.** Every background task drains battery. Use `WorkManager` (Android) or `BGTaskScheduler` (iOS) for deferrable work — the OS batches these for optimal battery. Never hold a wake lock longer than necessary. Avoid polling in the background — use push notifications to wake the app. Profile battery impact with Xcode Energy Log or Android Battery Historian.

5. **Design navigation with deep linking from day one.** Every screen should be reachable via a URL scheme or universal link. Push notification payloads must carry deep-link data (`{ screen: "ChatDetail", params: { chatId: "123" } }`). Test deep links from cold start, warm start, and when the app is not installed (deferred deep links via branch.io or Firebase Dynamic Links). Navigation without deep linking locks you out of re-engagement campaigns.

6. **Keep the app bundle under 150MB to avoid cellular download warnings.** iOS and Android both warn users when downloading apps >150MB over cellular — and many abandon. Use App Thinning (on-demand resources, asset catalogs), compress images to WebP/AVIF, remove unused native libraries. Audit bundle size every release with APK Analyzer or `du -sh` on the .ipa.

7. **Implement biometric auth with platform-native APIs, not third-party wrappers.** iOS: LocalAuthentication framework with Face ID/Touch ID. Android: BiometricPrompt API with `BIOMETRIC_STRONG` for crypto-backed auth. Store tokens in Keychain (iOS) or EncryptedSharedPreferences/Keystore (Android) — never in AsyncStorage or plain SharedPreferences. Fall back to device passcode gracefully and never as a first-choice alternative.

8. **Use platform-appropriate navigation patterns.** iOS: hierarchical drill-down with a back swipe gesture, tab bar at bottom. Android: Navigation drawer or bottom navigation with back button (system or in-app). React Native: `react-navigation` with platform-appropriate defaults (`Platform.select`). Flutter: `go_router` or `auto_route` with platform adaptive transitions. Cross-platform UI that ignores platform conventions feels alien in both ecosystems.

9. **Implement certificate pinning for sensitive apps (finance, health, enterprise).** Without pinning, a compromised CA can MITM your app's traffic. Pin against the public key hash (SPKI), not the certificate — certificates expire; public keys can be reused across renewals. Include a backup pin. Test with proxy tools (Charles, mitmproxy) to verify pinning works. OWASP MASVS L2 requires pinning.

10. **Profile scroll performance with platform tools, not just the naked eye.** iOS: Instruments Core Animation tool (Color Blended Layers, Color Offscreen-Rendered). Android: GPU Rendering Profile Bars (ensure each frame is under 16ms). React Native: Flipper performance plugin or `react-native-performance`. Flutter: performance overlay (rebuild counts, raster times). Jank visible to the eye is already >100ms of dropped frames.


## Error Recovery **(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

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


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "mobile-developer",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

### State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

### Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## Production Checklist **(STANDARD)**

Before any app store submission or production release, verify ALL of:

1. `npm test` / `flutter test` / XCTest — all tests pass, both platforms
2. Build for both platforms: iOS and Android both compile without error from clean checkout
3. Cold start time under 1.5s on low-end target device (not simulator)
4. Scroll performance: locked 60fps on low-end device, zero dropped frames in GPU profiling
5. Memory: under 50MB baseline, no leaks after navigating core flow 20×
6. Offline test: airplane mode on every screen — cached data shown, no crash/white screen, "offline" indicator visible
7. Bundle size: .ipa < 150MB, .aab < 150MB — audit with APK Analyzer / App Thinning report
8. App Store Review Guidelines checklist completed: no private APIs, privacy labels complete, permission descriptions accurate
9. Accessibility: TalkBack/VoiceOver navigates every screen, all elements have `accessibilityLabel`, minimum 4.5:1 contrast
10. Permissions: deny each permission — app degrades gracefully with explanation, no crash, no infinite spinner
11. Deep links: test every deep link from cold start, warm start, push notification, and universal link
12. Biometric auth: Face ID/Touch ID and fallback to passcode both work; tokens stored in Keychain/Keystore
13. Push notifications: FCM/APNs token registered, deep-link payload routes to correct screen, rich media attachments render
14. Crash reporting: Firebase Crashlytics/Sentry initialized, symbolication working, test crash appears in dashboard
15. Certificate pinning verified (if applicable): proxy tools cannot intercept traffic
16. Release notes, screenshots, and promotional text ready for App Store Connect and Google Play Console

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

## Anti-Patterns

### 1. App Store Rejection at Launch
**What it looks like:** Submitting to review the day before launch. Apple/Google reject for private APIs, missing privacy labels, or placeholder content. Each rejection adds 1-3 days to review queue. Marketing spend burns with no product live.
**Cost:** $10K-$50K per rejection in delayed revenue, wasted marketing, and emergency rework.
**Fix:** Submit 2 weeks before launch. Run through the full App Store Review Guidelines checklist. Budget for at least one rejection in your timeline. Test with TestFlight internal/external before submission.

### 2. No Offline Mode
**What it looks like:** White screen or crash when connectivity drops. 1-star reviews: "doesn't work on the subway." Apps without offline support see 25-40% lower ratings in regions with patchy connectivity.
**Cost:** $15K-$50K in lost downloads from negative reviews. A 0.5-star drop reduces install conversion by 30%.
**Fix:** Local-first architecture. Cache last-known-good data. Show cached content with an offline banner. Queue mutations for retry. Test every screen in airplane mode.

### 3. Bundle Size Over 150MB Cellular Limit
**What it looks like:** App bundle exceeds 150MB. iOS and Android warn users on cellular download — most abandon. Install conversion drops 1% for every 6MB over 100MB.
**Cost:** $20K-$100K in lost installs.
**Fix:** App Thinning/Slicing, on-demand resources. Compress images to WebP/AVIF. Remove unused native libraries. Audit bundle every release with APK Analyzer or `du -sh` on .ipa.

### 4. Missing Mobile Accessibility
**What it looks like:** ADA and Section 508 apply to mobile apps. Inaccessible app invites lawsuit or DOJ demand letter. 15% of the population has a disability — they can't use your app.
**Cost:** $10K-$50K in settlements and remediation per complaint.
**Fix:** Enable TalkBack/VoiceOver, navigate entire app. Set `accessibilityLabel` on every interactive element. Maintain 4.5:1 contrast ratio. Test with Accessibility Scanner (Android) and Accessibility Inspector (iOS) before every release.

### 5. QA Only on Flagship Devices
**What it looks like:** Team tests on iPhone 15 Pro and Pixel 9. 40% of users run $200 devices with 2GB RAM. Features at 60fps on flagships drop to 8fps on low-end. Cold start at 10s drives 53% abandonment.
**Cost:** $20K-$100K in lost installs and rating erosion from untested device tiers.
**Fix:** Device lab covering top 5 devices by market share in target region. Automated performance tests on lowest-spec device. Gate releases on cold-start time, scroll FPS, and memory on representative low-end device.

### 6. console.log Shipping to Production (React Native)
**What it looks like:** `console.log` in React Native iOS production builds appears in device logs — it doesn't get stripped. Sensitive data logged during development ships to every user's device.
**Fix:** Wrap all logging behind `__DEV__` guards. Use `react-native-logs` or `babel-plugin-transform-remove-console` in production builds. Never log API responses, user data, or tokens.

### 7. AsyncStorage 6MB Limit on Android
**What it looks like:** `AsyncStorage` has a ~6MB limit on Android (device-dependent). Large JSON blobs silently fail with no error callback. Data is lost without the developer knowing.
**Fix:** Chunk data over 1MB. Use SQLite (WatermelonDB, `expo-sqlite`) for structured storage. Monitor storage usage. Migrate to MMKV for larger key-value needs (react-native-mmkv).

### 8. iOS Simulator vs Android Emulator Networking
**What it looks like:** iOS Simulator uses host Mac's network — `localhost` works directly. Android Emulator uses virtual router at `10.0.2.2` to reach host. Code that works on iOS sim silently fails on Android emulator.
**Fix:** Use `Platform.select({ ios: 'localhost', android: '10.0.2.2' })` for local dev API URLs. Test networking on both platforms before merge. Use actual device testing for final verification.

### 9. Platform-Specific Keyboard Avoidance
**What it looks like:** `KeyboardAvoidingView` with `behavior="padding"` double-shifts content on Android because Android already adjusts window size automatically. iOS needs it; Android breaks with it.
**Fix:** Use `Platform.select` for behavior prop: `behavior={Platform.OS === 'ios' ? 'padding' : undefined}`. Or use `react-native-keyboard-aware-scroll-view` which handles both platforms correctly.

### 10. Image.prefetch() Platform Inconsistency
**What it looks like:** `Image.prefetch()` has 50MB disk cache on iOS, but Android clears its cache entirely on app close. Relying on prefetch for offline image availability silently fails on Android.
**Fix:** Use `react-native-fast-image` with consistent disk caching across platforms. Implement explicit image cache management. Never assume prefetched images survive app restart on Android.

### 11. AppState "inactive" During Control Center
**What it looks like:** `AppState.currentState` on iOS reports `"inactive"` when user pulls down Control Center or Notification Center. Pausing video on `"background"` only means video keeps playing during Control Center interaction.
**Fix:** Listen for `"inactive"` state and handle it explicitly. Pause playback on both `"inactive"` and `"background"`, or check `"active"` explicitly and pause on anything else.

## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When mobile apps go wrong, they go wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| App crashes on 30% of Android devices, works perfectly on iOS — `FragmentManager` crash is the #1 Android-only crash in every crash report | Android fragment lifecycle — backgrounded app's fragment state is destroyed by OS but Activity tries to access null fragment reference. iOS doesn't have fragments so the crash is platform-specific | Add null checks in `onViewCreated()`, use `savedInstanceState` bundle for state restoration, or migrate to Jetpack Compose Navigation which handles this automatically. For React Native, ensure native module lifecycle is bound to React context | Android's aggressive memory management kills fragments without warning. Every fragment access must be null-guarded. Cross-platform frameworks paper over this — until they don't |
| `FlatList` re-renders entire list on every keystroke — typing in a search bar freezes for 500ms as 1000 items re-render | Missing `keyExtractor` prop. React Native falls back to array index as key. When items shift (due to sort, filter, or insert), every item gets a new key and remounts entirely | Always provide `keyExtractor={(item) => item.id.toString()}` with a stable, unique identifier. Use `React.memo` on list item components. Use `getItemLayout` for fixed-height items to skip measurement. Profile with Flipper Performance plugin | Without a keyExtractor, FlatList treats every data change as a complete rebuild. One missing prop turns O(1) scroll performance into O(n) re-render cost |
| Hermes engine incompatible with a native module — app crashes on Android with `TypeError: undefined is not a function`, works on iOS with JSC | Some native modules use JavaScript features that Hermes doesn't support (certain `Proxy` behaviors, `eval`, or `with` statements). Hermes is default on Android, JSC on iOS — the bug is platform-specific and impossible to reproduce on iOS | Check native module compatibility with Hermes before adopting. Add `"jsEngine": "hermes"` to iOS Podfile to use Hermes uniformly. Use `npx react-native info` to audit native module versions. Test on both engines before committing to a module | Hermes and JSC are different JavaScript engines with different feature support. A module that "works" on iOS may crash on Android because it relies on JSC-specific behavior. Engine parity prevents split-brain debugging |
| Deep link opens app but shows home screen instead of target content — user taps notification, expects to see the message, gets dashboard | Deep link is processed before React Native JS bundle is fully loaded. The native layer receives the intent, but the navigation container isn't mounted yet. The link event fires into the void | Use `Linking.getInitialURL()` in the root component's `useEffect` (runs once on mount). For cold starts, the native layer queues the URL — read it after the navigation ref is ready. For warm starts, use `Linking.addEventListener('url', handler)`. Test deep links via `adb shell am start` and `xcrun simctl openurl` from killed state | Cold-start deep-linking is a race condition between the OS delivering the URL and your app's navigation system being ready. The link arrives in <100ms; your JS bundle takes 500ms-2s to load. You must poll for the queued URL, not just listen for events |
| App rejected from App Store — "ITMS-90809: Deprecated API Usage — UIWebView" but the app doesn't use UIWebView | A dependency (typically an old analytics SDK, ad network, or auth library) statically links `UIWebView`. Apple scans the binary for the symbol, not the intent. Even transitive dependencies trigger rejection | Run `grep -r "UIWebView" node_modules/` to find the offending package. Upgrade or replace the dependency. For iOS, use `nm path/to/lib.a | grep UIWebView` to scan static libraries. Add `--no-use-uiwebview` flag to React Native's Podfile | Apple scans compiled binaries, not source code. A dependency you never call can still get your app rejected because its `.a` or `.framework` bundle contains deprecated symbols |
| App works on Wi-Fi, fails on cellular — API calls timeout, images don't load, users on 4G/5G can't use the app | Cellular connections have higher latency (50-200ms RTT), lower bandwidth (especially in rural areas), and aggressive carrier NAT. Timeouts set to 5 seconds work on Wi-Fi (10ms RTT) but fail on cellular. Large images and uncompressed payloads time out on slow connections | Set network timeout to 30 seconds minimum. Use adaptive image loading (thumbnail → full resolution). Test on Network Link Conditioner with "Edge" and "3G" profiles. Monitor `NetInfo.isConnected` and `NetInfo.isInternetReachable` — degrade gracefully when connectivity is poor | "Works on my Wi-Fi" is the mobile equivalent of "works on my machine." Cellular networks are slower, less reliable, and more latent than any development setup. Every network call must survive 200ms+ latency and 500kbps bandwidth |

## Verification

- [ ] Run `npm test` / `flutter test` / XCTest — all tests pass
- [ ] Build for both platforms: `npx react-native run-ios` AND `npx react-native run-android` (or Flutter equivalents) — both build without error
- [ ] Test on physical device (not just simulator): touch interactions, scroll performance, keyboard behavior
- [ ] Test offline: enable airplane mode — app shows cached data, not crash/white screen
- [ ] Test permissions: deny camera/location/notifications — app degrades gracefully with explanation
- [ ] Verify app size: `du -sh` the built .ipa/.apk — within budget (< 20% increase from baseline)

## Verification Guardrails

Before delivering work, the agent must verify:

- [ ] **Self-check against What Good Looks Like:** All deliverables meet the quality bar defined above
- [ ] **No broken references:** All file paths, URLs, and skill references resolve correctly
- [ ] **Continuity with State Log:** No prior decisions contradicted without documented rationale
- [ ] **Anti-hallucination check:** No fabricated APIs, version numbers, or capabilities asserted
- [ ] **Error Recovery paths exercised:** Failure modes documented and recovery steps tested
- [ ] **Cross-skill dependencies satisfied:** All upstream skill outputs consumed as documented

If any checkbox fails, revise before delivering. When all pass, add to the state log.

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

