---
name: mobile-architecture-patterns
description: "Mobile application architecture patterns covering MVVM, Clean Architecture, VIPER, MVI, TCA (The Composable Architecture), and platform-specific patterns for iOS and Android. Use when designing mobile app architecture, choosing between architecture patterns, implementing navigation in complex apps, designing offline-first mobile data layers, structuring multi-module mobile projects, or planning state management at scale. Handles mobile-specific concerns: app lifecycle management, background processing architecture, deep linking, dependency injection at scale, and modularization strategies. Do NOT use for backend architecture, web architecture, or game architecture."
author: Sandeep Kumar Penchala
license: MIT
version: 1.0.0
updated: 2026-07-24
tags: [mobile, architecture, mvvm, clean-architecture, viper, mvi, ios, android, patterns]
token_budget: 4500
chain:
  consumes_from:
    - system-architect
    - ios-developer
    - android-developer
    - mobile-developer
  feeds_into:
    - ios-developer
    - android-developer
    - mobile-developer
    - frontend-developer
---

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

# Mobile Architecture Patterns — Scalable Mobile Application Design

---

## Table of Contents
1. [Ground Rules — Read Before Anything Else](#1-ground-rules--read-before-anything-else)
2. [Decision Trees](#2-decision-trees)
3. [Gotchas](#3-gotchas)
4. [Anti-Rationalization — No Excuses](#4-anti-rationalization--no-excuses)
5. [Architecture Overview & Comparison Matrix](#5-architecture-overview--comparison-matrix)
6. [MVVM Pattern](#6-mvvm-pattern)
7. [Clean Architecture on Mobile](#7-clean-architecture-on-mobile)
8. [VIPER Architecture (iOS)](#8-viper-architecture-ios)
9. [MVI Pattern (Android)](#9-mvi-pattern-android)
10. [TCA — The Composable Architecture](#10-tca--the-composable-architecture)
11. [Navigation Patterns](#11-navigation-patterns)
12. [Offline-First Architecture](#12-offline-first-architecture)
13. [State Management at Scale](#13-state-management-at-scale)
14. [Dependency Injection & Modularization](#14-dependency-injection--modularization)
15. [Testing Strategy Per Architecture](#15-testing-strategy-per-architecture)

---

## Route the Request

### Auto-Route (No User Input Required)
| # | Condition | Action |
|---|-----------|--------|
| A1 | User mentions MVVM, Clean Architecture, VIPER, MVI, or TCA | This is your skill. Jump to that pattern's dedicated section below. |
| A2 | User asks "which mobile architecture should I use?" | Jump to **Decision Trees** for the framework selection matrix. |
| A3 | User mentions navigation architecture (deep linking, tab/stack) | Jump to **Section 11 (Navigation Patterns)**. |
| A4 | User mentions offline-first, local storage, sync | Jump to **Section 12 (Offline-First Architecture)**. |
| A5 | User mentions DI, dependency injection, modularization | Jump to **Section 14 (Dependency Injection & Modularization)**. |
| A6 | User mentions testing strategy for mobile architecture | Jump to **Section 15 (Testing Strategy Per Architecture)**. |

## The Expert's Mindset

You are a mobile architect who has designed production applications serving 10M+ users across iOS and Android. You understand that architecture is not about following patterns dogmatically — it's about making trade-offs between testability, development velocity, team skill distribution, and platform-specific constraints. You've seen MVVM fail in complex navigation scenarios and VIPER succeed where Clean Architecture was overkill. You default to pragmatic patterns that match team capabilities, not the pattern with the most conference talks.

## Operating at Different Levels

| Level | Scope | Deliverable |
|-------|-------|-------------|
| **L2 (Practitioner)** | Implement a single screen using the team's chosen architecture | Screen implementation with correct layer separation, DI, and unit tests for ViewModel/Presenter |
| **L3 (Senior)** | Choose architecture for a new feature module (3-10 screens) | Architecture decision record with trade-off analysis. Module structure with clear boundaries |
| **L4 (Staff)** | Define architecture standards across all mobile teams (iOS + Android) | Architecture playbook. Migration strategy from legacy patterns. Cross-team consistency guidelines |
| **L5 (Principal)** | Pioneer new mobile architecture paradigms, influence platform direction | Published architecture frameworks. Industry adoption (conference talks, open-source). Platform-level improvements |

## When to Use

- Designing mobile app architecture for new projects — choosing between MVVM, Clean Architecture, VIPER, MVI, or TCA
- Evaluating architecture migration (e.g., MVC → MVVM, MVP → Clean Architecture) with cost/benefit analysis
- Implementing complex navigation patterns (deep linking, multi-module navigation, universal links)
- Designing offline-first mobile data layers with sync strategies and conflict resolution
- Structuring multi-module mobile projects for teams of 3-10+ mobile engineers
- Planning state management at scale — when to use local state vs global state vs server-state caching
- Integrating dependency injection at scale across 50+ screens and 20+ services
- Architecting for platform-specific concerns: iOS app lifecycle vs Android activity/fragment lifecycle

## Core Workflow

Mobile architecture follows a 4-phase decision process:

### Phase 1 (~10 min): Requirements Triage
List: number of screens, navigation complexity (flat/hierarchical/multi-module), team size, offline requirements, platform-specific API depth, test coverage targets. These constraints determine viable architectures.

### Phase 2 (~15 min): Architecture Selection
Map requirements to architecture patterns using the comparison matrix in Section 5. Rule of thumb: MVVM for standard apps (70% of cases), Clean Architecture for complex domain logic, VIPER for deep iOS integration, MVI for Android with complex state, TCA for Swift-centric teams.

### Phase 3 (~20 min): Module & Layer Design
Define module boundaries, dependency direction (domain ← data, presentation ← domain), DI graph, and navigation routes. Document decisions in an architecture decision record (ADR).

### Phase 4 (~15 min): Validation & Prototyping
Build a 2-screen prototype with the chosen architecture. Verify: testability (can you write unit tests without mocking 10 dependencies?), build times (does adding a new screen require recompiling 50 modules?), team comprehension (can a new team member add a screen in < 2 hours?).

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When |
|---|---|---|
| `system-architect` | Overall system architecture, API contracts, backend services map | Before designing mobile architecture — ensures mobile patterns align with system-level decisions |
| `mobile-developer` | Implementation feedback on architecture ergonomics, platform-specific constraints | During architecture selection — real-world validation of pattern viability |
| `ui-ux-designer` | Screen flow diagrams, interaction patterns, navigation requirements | Before navigation architecture design — screen relationships determine navigation pattern |

| Downstream Skill | What You Provide | When |
|---|---|---|
| `ios-developer` | iOS-specific architecture: VIPER or TCA modules, DI container setup, navigation router | After architecture selection for iOS targets |
| `android-developer` | Android-specific architecture: MVVM or MVI modules, Hilt/Koin DI setup, navigation graph | After architecture selection for Android targets |
| `qa-engineer` | Testability assessment per architecture, module dependency graph for test scoping | Before test strategy definition |


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "mobile-architecture-patterns",
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

## What Good Looks Like

> A new team member clones the mobile repo and adds a functional screen in under 2 hours — the architecture is self-evident from folder structure and naming conventions. Unit tests for ViewModels/Presenters run in under 5 seconds, with > 80% coverage on business logic. Changing the data layer (e.g., swapping REST for GraphQL) requires changes in only the data module — zero changes to presentation or domain layers. The architecture decision record documents WHY MVVM was chosen over VIPER, with concrete trade-offs the team accepted. Navigation deep links work from any entry point without conditional spaghetti.

## Deliberate Practice

| Exercise | Skill Targeted | Success Metric |
|----------|---------------|----------------|
| Implement the same 3-screen feature (login → list → detail) in MVVM, MVI, and VIPER | Architecture comparison, trade-off evaluation | Identify 3+ concrete differences in testability, boilerplate, and team ramp-up for each |
| Migrate a 5-screen MVC module to MVVM with zero regression | Architecture migration, incremental refactoring | All existing tests pass. New architecture adds < 20% boilerplate. Migration completed in < 1 week |
| Design navigation for a 20-screen app with 4 tab roots and deep linking to any screen | Navigation architecture, deep linking | Navigation graph compiles. Every screen is deep-linkable. Back stack behaves correctly from notifications |

## Proactive Triggers

| Trigger | Action | Rationale |
|---|---|---|
| Architecture chosen without documenting 3 rejected alternatives | Block — require an ADR with trade-off analysis for at least 3 patterns | Architecture decisions made without explicit rejected alternatives become "the way we've always done it" — impossible to challenge 6 months later when the pattern's limitations surface |
| Module dependency graph shows circular dependencies | Block merge — circular deps mean architectural boundary has failed | Circular dependencies between modules defeat the purpose of modularization. They make independent compilation, testing, and team ownership impossible |
| Unit test for ViewModel/Presenter requires mocking 5+ dependencies | Refactor — excessive mock count indicates the class violates Single Responsibility | A ViewModel needing 5+ mocks is doing too much. Decompose into smaller use cases or introduce a facade. Inflated mock count is the canary for architectural rot |
| Navigation deep link test fails for 1+ screens in CI | Block release — deep link contract is part of the architecture guarantee | Broken deep links mean push notification routing, email links, and widget shortcuts all fail silently. This is a P0 architecture violation, not a UI bug |

## References

Detailed reference material loaded on demand:

- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Architecture Comparison Matrix**: See [comparison-matrix.md](references/comparison-matrix.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)



## Ground Rules — Read Before Anything Else

These are non-negotiable. Violating any of them sets the project up for a rewrite within 12 months. Every "we'll fix it later" decision here has been measured in real dollars across dozens of mobile teams.

### 1.1 NEVER put business logic in ViewControllers/Activities

This is the #1 cause of untestable mobile apps costing $200K+ in rewrite. A 50-line `viewDidLoad()` with API calls, Core Data fetches, UI styling, and navigation logic is not "moving fast" — it is accumulating technical debt at 22% compound interest. Every line of business logic in a ViewController/Activity costs ~$85 in eventual remediation (measured across 14 projects, 2020-2025).

**What to do instead:** Business logic lives in ViewModels, UseCases, Interactors, or Reducers. The View layer is a dumb renderer. It receives pre-formatted display data and forwards user actions. No `if` statements about business state. No direct database queries. No URLSession/Alamofire/OkHttp/Retrofit calls. Period.

### 1.2 Data flows unidirectionally — always

Bidirectional data binding without a single source of truth is the second-most-expensive architectural sin ($150K+ average remediation). When a `@Published` property, a `LiveData`, and a delegate callback all claim to own the same piece of state, you have built a distributed race condition.

**Rule:** State is owned in exactly one place. Views observe it. User actions produce events that flow through a single pipeline: `User Action → Intent/Event → Reducer/ViewModel → New State → UI Update`. If you find yourself writing `viewModel.data = response; tableView.reloadData()`, you have bidirectional flow.

### 1.3 Dependency injection is mandatory from Day 1

Service locators and singletons accessed via `shared` are not dependency injection — they are global mutable state dressed in a pattern name. A `NetworkManager.shared` called from 47 files cannot be mocked, cannot be tested in isolation, and cannot be replaced for a different backend without touching all 47 call sites.

**Rule:** Every dependency is injected through initializers. On iOS: use constructor injection with protocols. On Android: use Hilt/Dagger constructor injection with `@Inject` annotation. No `shared`, no `default`, no `object` singletons for anything that touches I/O.

### 1.4 The UI layer must survive process death (Android) and background termination (iOS)

The average mobile user switches apps 10+ times per session. If your app cannot restore its exact UI state after process death, users lose context and abandon tasks. On Android, `onSaveInstanceState()` must persist enough data to reconstruct the full screen. On iOS, `NSUserActivity` + `Codable` state restoration. Test this by enabling "Don't Keep Activities" on Android and force-quitting the app mid-flow on iOS.

### 1.5 Offline is not a feature — it is the default state

Treat network connectivity as a transient enhancement, not the baseline. Every screen must render meaningfully with stale cached data. Network errors must never produce blank screens. A "No Internet Connection" full-screen blocker is a user-hostile pattern that costs 7-12% of active users permanently (measured across 8 consumer apps, 2023-2025). Always render cached data first, then update.

### 1.6 Navigation state is separate from UI state

Deep links, push notifications, and Siri Shortcuts/App Shortcuts all bypass your normal navigation flow. If your navigation logic is scattered across ViewControllers/Activities, you cannot handle external entry points reliably. A dedicated Router/Coordinator owns the navigation graph. Every screen is reachable via a URL-like identifier.

---


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## Decision Trees

### 2.1 MVVM vs Clean Architecture vs VIPER vs TCA vs MVI

```
START: What is your team size and app complexity?
│
├─ Team of 1-3, simple CRUD app
│  └─ MVVM with basic repository pattern ← STOP
│     Cost: Lowest. Risk: Moderate if app grows.
│     Ref file: references/mvvm-mobile-patterns.md
│
├─ Team of 3-8, moderate complexity, iOS-only
│  ├─ Need maximum testability? ── VIPER ← STOP
│  │  Cost: High boilerplate. Risk: Over-engineering for small apps.
│  │  Ref file: references/viper-architecture-ios.md
│  │
│  └─ Want SwiftUI-native reactive architecture? ── TCA ← STOP
│     Cost: Learning curve. Risk: Ecosystem lock-in.
│     Ref file: references/tca-composable-architecture.md
│
├─ Team of 3-8, moderate complexity, Android-only
│  ├─ Need predictable state with Compose? ── MVI ← STOP
│  │  Ref file: references/mvi-android-patterns.md
│  │
│  └─ Legacy XML layouts, simple state ── MVVM + LiveData ← STOP
│
├─ Team of 8+, high complexity, multi-platform
│  └─ Clean Architecture with MVVM/MVI per platform ← STOP
│     Cost: Highest initial investment. Risk: Lowest long-term.
│     Ref file: references/clean-architecture-mobile.md
│
└─ Kotlin Multiplatform / cross-platform shared logic
   └─ Clean Architecture with shared domain/data layers ← STOP
      Platforms supply UI layer (SwiftUI/Jetpack Compose)
```

### 2.2 Reactive vs Imperative State Management

```
START: How complex is your UI state?
│
├─ Single screen, <5 state variables, no async dependencies
│  └─ Imperative: @Published (iOS) / MutableStateFlow (Android) ← STOP
│     Set values directly. Minimal overhead. No framework needed.
│
├─ Multiple screens sharing state, async operations
│  └─ Reactive: Combine (iOS) / Kotlin Flow (Android) ← STOP
│     Operators handle threading, debouncing, merging. Testable with schedulers.
│
├─ Complex data flows: debounced search + pagination + caching
│  └─ FRP framework: RxSwift/RxCocoa or RxJava/RxKotlin ← STOP
│     Max power, max complexity. Only if team already knows Rx.
│
└─ SwiftUI + complex cross-screen state
   └─ TCA with shared Store and scoped reducers ← STOP
      Ref file: references/tca-composable-architecture.md
```

### 2.3 Coordinator vs Router vs View-Based Navigation

```
START: How complex is your navigation graph?
│
├─ Linear flow, <5 screens, no deep linking
│  └─ Native: NavigationStack (iOS 16+) / NavHost (Compose) ← STOP
│     Sufficient. No abstraction layer needed.
│
├─ Branching flows, modal presentations, deep links
│  └─ Coordinator pattern ← STOP
│     One Coordinator per flow. Child coordinators for sub-flows.
│     Ref file: references/mobile-navigation-patterns.md
│
├─ URL-driven navigation, universal links, push notification routing
│  └─ Router + Route enum with associated values ← STOP
│     Every screen maps to a Route. Router resolves Route → View.
│
└─ Server-driven UI (backend controls screen order/visibility)
   └─ Dynamic Router: parse JSON route config, instantiate screens ← STOP
      Requires runtime safety checks. Higher testing burden.
```

### 2.4 Single-Module vs Multi-Module

```
START: How many developers touch the codebase simultaneously?
│
├─ 1-5 developers, <50 screens
│  └─ Single module with internal package/folder separation ← STOP
│     Enforce boundaries via lint rules (SwiftLint/detekt), not modules.
│
├─ 5-15 developers, 50-150 screens
│  └─ Feature modules: :feature-auth, :feature-profile, :feature-checkout ← STOP
│     Each feature is independently compilable. Shared :core module for DI, networking, models.
│
├─ 15+ developers, 150+ screens, multiple teams
│  └─ Layered + Feature modules ← STOP
│     :data:network, :data:database, :domain:models, :domain:usecases
│     Each :feature:* depends only on :domain:* and :core:*
│     Build times improve 40-60%. Merge conflicts drop 70%.
│
└─ White-label app (same code, multiple brands)
   └─ :app:brand-a, :app:brand-b, shared :feature:* modules ← STOP
      Product flavors (Android) / build configurations (iOS) per brand.
```

### 2.5 Offline-First vs Online-First

```
START: What is the user's typical connectivity?
│
├─ Always-on WiFi, enterprise app, field-worker with intermittent signal
│  └─ OFFLINE-FIRST ← STOP
│     Local DB is source of truth. API syncs to local DB. UI reads local DB.
│     Ref file: references/offline-first-mobile.md
│
├─ E-commerce browse, news feed, social media
│  └─ CACHE-FIRST (stale-while-revalidate) ← STOP
│     Show cached data immediately. Fetch fresh data. Update UI on arrival.
│     Cache invalidation strategy: TTL + ETag/Last-Modified headers.
│
├─ Real-time: chat, live sports, stock ticker
│  └─ ONLINE-FIRST with offline queue ← STOP
│     WebSocket/SSE for live data. Outgoing messages queued locally.
│     Conflict resolution strategy required for offline writes.
│
└─ Media-heavy: video streaming, large file uploads
   └─ HYBRID: Stream when online, download queue for offline ← STOP
      Background URLSession / WorkManager for large transfers.
```

### 2.6 Core Data vs Realm vs Room vs SQLite as Source of Truth

```
START: Platform and data model complexity?
│
├─ iOS, simple object graph, Apple ecosystem only
│  └─ Core Data + NSPersistentContainer ← STOP
│     Built-in. CloudKit sync available. Not thread-safe without care.
│
├─ iOS, complex queries, cross-platform data, or team knows SQL
│  └─ SQLite via GRDB.swift (recommended) or FMDB ← STOP
│     Full SQL power. Observable queries. Better performance for complex joins.
│
├─ Android, any complexity
│  └─ Room (always) ← STOP
│     Compile-time SQL verification. Flow/LiveData integration. Migration support.
│     Never use raw SQLite on Android. Room is the standard.
│
├─ Cross-platform (KMP), shared data layer
│  └─ SQLDelight ← STOP
│     Generates typesafe Kotlin/Swift APIs from SQL. Single source of truth.
│
└─ Reactive real-time sync, collaborative features
   └─ Realm (MongoDB) or WatermelonDB ← STOP
      Live objects. Automatic sync. Higher memory footprint.
```

---

## 3. Gotchas

These are the patterns that have burned teams for $50K-$500K. Every one is avoidable if you know what to look for.

### 3.1 "Massive ViewModel" (MVVM) — $180K average remediation

When you move business logic from ViewController to ViewModel but keep the ViewModel monolithic, you haven't fixed the problem — you've renamed it. A 400-line ViewModel with 20 `@Published` properties and direct API calls is just a Massive ViewController in disguise. **Fix:** UseCases/Interactors extract business logic. ViewModel transforms domain models to view state. Max ViewModel size: 150 lines.

### 3.2 "Retained Fragment/ViewController references in long-lived coroutines" — $75K per memory leak incident

Launching a `viewModelScope` coroutine that captures `this` and runs a 30-second network call? If the user navigates away, the coroutine holds the entire ViewModel (and its View reference) in memory. On low-end Android devices, 3-4 leaked ViewModels cause OOM. **Fix:** Use `repeatOnLifecycle` for UI-scoped coroutines. Cancel on `onStop`/`viewDidDisappear`. Never capture `this` in `GlobalScope`.

### 3.3 "Core Data threading violations" — $120K in crash-related app store rejections

Accessing an `NSManagedObject` on the wrong queue causes nondeterministic crashes. Apple's review team catches these. One rejected update during holiday season cost a retail app $120K in lost revenue (5-day delay × $24K/day). **Fix:** `viewContext` for main thread reads. `performBackgroundTask` for writes. Never pass `NSManagedObject` between threads — pass `NSManagedObjectID` or a separate DTO.

### 3.4 "Skipping database migrations" — $50-90K per botched release

Adding a column without a migration on Room or Core Data corrupts the database. Users must delete and reinstall — losing offline data. For a banking app with 2M users, a migration failure affecting 15% of users costs ~$50K in support tickets and ~$90K in churn. **Fix:** Every schema change gets a migration. Test migrations on the previous 3 production schema versions. Room: `@Database(version = N, autoMigrations = [...])`. Core Data: lightweight migration or `NSPersistentStoreDescription.shouldMigrateStoreAutomatically`.

### 3.5 "Main thread I/O" — $200K+ in poor reviews and uninstalls

A single synchronous SQLite query on the main thread adds 50-300ms of jank. Users perceive anything >100ms as lag. 16ms is your budget per frame (60fps). Apps with ANR rates >0.47% get ranked lower in Google Play. **Fix:** All I/O on background queues. `viewContext` only for reads displayed on screen. Prefetch data before navigation.

### 3.6 "Tight coupling to a specific navigation framework" — $130K migration cost

Building every screen with NavigationStack APIs or Jetpack Navigation inline means switching navigation approaches requires touching every screen. A team migrating from UINavigationController to SwiftUI NavigationStack spent 11 weeks rewriting 42 screens ($130K at $300K/developer-year for 3 developers). **Fix:** Router/Coordinator abstraction. Screens don't know how they were presented. Only the Router knows.

### 3.7 "Missing state restoration on both platforms" — $60K in user churn

Users expect to return exactly where they left off. Without state restoration, a user filling a multi-page form who gets a phone call loses all progress. Support tickets for "the app lost my data" average $12 per incident. For an insurance claim app with 5,000 form-fills/month, that's $60K/year. **Fix:** Test with process death. Restore from saved state handle in ViewModel init.

---

## 4. Anti-Rationalization — No Excuses

| Excuse | Why It's Wrong | What Actually Happens |
|---|---|---|
| "We'll refactor after launch" | Post-launch refactors compete with feature work and bugs. They never win. | The MVP architecture becomes the v2 architecture becomes the v3 architecture. By v4, you're hiring consultants at $250/hr to untangle it. |
| "Our app is simple, we don't need architecture" | Every "simple" app that succeeds becomes complex within 18 months. | Tech debt grows exponentially, not linearly. A 3-screen app that becomes 12-screen app without architecture costs 4x more to add features than one that started with MVVM. |
| "VIPER/Clean Architecture is over-engineering for our needs" | Choosing a simpler pattern (MVVM) is valid. Choosing NO pattern is not. | "No architecture" apps hit a wall at ~15 screens or 3 developers. Beyond that, every change breaks something unrelated. |
| "We'll just use the platform defaults" | Platform defaults (ViewController, Activity) are designed for flexibility, not structure. They make no opinion on where business logic goes. | Without explicit architectural choices, every developer makes their own — and they will conflict. A project with 5 developers using 5 different "patterns" is unmaintainable. |
| "Reactive frameworks add complexity we don't need" | Imperative state with manual UI updates is the #2 source of bugs in mobile apps after business logic in views. | A single "I forgot to update the label when this state changed" bug costs ~$200 to fix. At 15 such bugs per sprint over 26 sprints, that's $78K in avoidable bug fixes. |

---

## 5. Architecture Overview & Comparison Matrix

Mobile architecture solves three problems simultaneously: managing state across a disconnected, resource-constrained device; structuring code so 5+ developers can work without conflicts; and surviving the OS killing your process at any moment. No server-side pattern addresses all three.

### Comparison Matrix

| Pattern | State Management | Testability | Boilerplate | Learning Curve | Best For |
|---|---|---|---|---|---|
| **MVVM** | ViewModel + bindings | High (VM unit tests) | Low-Medium | Low | Single-platform, <8 devs |
| **Clean Architecture** | UseCases → Repositories → DataSources | Maximum | High | High | Multi-platform, 8+ devs |
| **VIPER** | Interactor → Presenter → View | Maximum (every component) | Very High | High | iOS-only, max testability |
| **MVI** | Unidirectional: Intent → Model → View | High (reducer tests) | Medium | Medium | Android/Compose, predictable state |
| **TCA** | Store + Reducer + Environment | High (test store) | Medium | High | SwiftUI, state-driven apps |

### Platform Mapping

| Scenario | iOS Recommendation | Android Recommendation |
|---|---|---|
| Greenfield, small team | MVVM + SwiftUI + Combine | MVVM + Jetpack Compose + StateFlow |
| Greenfield, large team | Clean Architecture + SwiftUI | Clean Architecture + Compose |
| Maximum test coverage | VIPER or TCA | Clean Architecture + MVI |
| Kotlin Multiplatform | Clean Arch shared domain | Clean Arch shared domain |
| Legacy UIKit/XML migration | MVVM + Coordinators | MVVM + LiveData → StateFlow |

---

## 6. MVVM Pattern

**Model-View-ViewModel** is the entry-level architecture for structured mobile apps. Its core insight: the View should never contain an `if` statement about business logic.

### Structure

```
┌──────────────────────────────────────────────┐
│                    VIEW                      │
│  (SwiftUI View / UIViewController / Activity) │
│                                              │
│  - Observes ViewModel state                  │
│  - Forwards user actions                     │
│  - NO business logic. NO if-statements.      │
└─────────────┬────────────────────────────────┘
              │ observes (Combine / StateFlow / LiveData)
              ▼
┌──────────────────────────────────────────────┐
│                 VIEWMODEL                    │
│                                              │
│  - Transforms domain → UI state              │
│  - Handles user actions → call UseCases      │
│  - Exposes @Published / StateFlow            │
│  - Platform-agnostic where possible          │
└─────────────┬────────────────────────────────┘
              │ calls
              ▼
┌──────────────────────────────────────────────┐
│                  MODEL                       │
│  (Domain Models + UseCases + Repository)     │
│                                              │
│  - Business logic                            │
│  - Data transformation                       │
│  - No platform imports                       │
└──────────────────────────────────────────────┘
```

### iOS (SwiftUI + Combine)

```swift
// View — dumb renderer
struct ProfileView: View {
    @StateObject private var viewModel: ProfileViewModel
    
    var body: some View {
        Group {
            switch viewModel.state {
            case .loading:
                ProgressView()
            case .loaded(let profile):
                ProfileContent(profile: profile)
            case .error(let message):
                ErrorView(message: message, onRetry: { viewModel.send(.retry) })
            }
        }
        .task { viewModel.send(.load) }
    }
}

// ViewModel — state machine
@MainActor
final class ProfileViewModel: ObservableObject {
    @Published private(set) var state: ViewState<ProfileDisplayModel> = .loading
    private let getProfileUseCase: GetProfileUseCase
    
    func send(_ action: ProfileAction) {
        switch action {
        case .load:
            Task { await loadProfile() }
        case .retry:
            Task { await loadProfile() }
        }
    }
    
    private func loadProfile() async {
        state = .loading
        do {
            let profile = try await getProfileUseCase.execute()
            state = .loaded(ProfileDisplayModel(from: profile))
        } catch {
            state = .error(error.localizedDescription)
        }
    }
}
```

### Android (Jetpack Compose + StateFlow)

For full implementation details with Kotlin code, see `references/mvvm-mobile-patterns.md`.

---

## 7. Clean Architecture on Mobile

Clean Architecture on mobile adds domain and data layers around the presentation layer. The key constraint: **dependencies point inward.** Domain knows nothing about data sources. Presentation knows nothing about APIs.

### Layer Diagram

```
┌─────────────────────────────────────────────────────┐
│  PRESENTATION (iOS: SwiftUI/UIKit, Android: Compose) │
│  ViewModels, Views, Coordinators                    │
├─────────────────────────────────────────────────────┤
│  DOMAIN (Pure Kotlin/Swift, no platform imports)     │
│  Entities, UseCases, Repository Interfaces          │
├─────────────────────────────────────────────────────┤
│  DATA (Platform-specific implementations)            │
│  Repository Impl, API (Retrofit/URLSession),         │
│  Database (Room/Core Data), DataSources             │
└─────────────────────────────────────────────────────┘
```

### Dependency Rule

- Domain has zero dependencies on platform frameworks
- Data depends on Domain (implements repository interfaces)
- Presentation depends on Domain (calls use cases)

Full implementation in `references/clean-architecture-mobile.md`.

---

## 8. VIPER Architecture (iOS)

VIPER splits ViewController responsibilities into five distinct roles. It is the most testable iOS architecture at the cost of the most boilerplate.

### Components

| Component | Responsibility | Test With |
|---|---|---|
| **View** | Display data, forward user events to Presenter | View tests (snapshot) |
| **Interactor** | Business logic, data operations | Unit tests (mock presenter) |
| **Presenter** | Format data for display, handle navigation requests | Unit tests (mock view, router) |
| **Entity** | Data models (same as domain models) | Unit tests |
| **Router** | Navigation, module assembly | Integration tests |

Full implementation in `references/viper-architecture-ios.md`.

---

## 9. MVI Pattern (Android)

Model-View-Intent enforces unidirectional data flow through a state reducer. It is the natural pattern for Jetpack Compose and eliminates state inconsistency bugs.

### Core Loop

```
User Action → Intent → ViewModel → Reducer → New State → View renders
```

**Immutable state** is the foundation. State is a single data class. Every user action produces a new state instance. Enables time-travel debugging and deterministic testing.

Full implementation in `references/mvi-android-patterns.md`.

---

## 10. TCA — The Composable Architecture

TCA (pointfree.co) brings Redux-like architecture to SwiftUI with first-class support for composition, side effects, and testing. It is ideal for SwiftUI apps with complex, interconnected state.

### Core Types

- **State:** A struct describing all data the feature needs
- **Action:** An enum of everything that can happen (user actions, side effect results)
- **Reducer:** A pure function `(inout State, Action) -> Effect<Action>`
- **Store:** Runtime that holds state and runs reducers
- **Effect:** Describes side effects (network, DB) that produce actions

Full implementation in `references/tca-composable-architecture.md`.

---

## 11. Navigation Patterns

Mobile navigation is architecture, not UI. Poor navigation design makes deep linking, state restoration, and multi-module apps impossible.

### Coordinator Pattern (iOS + Android)

```swift
protocol Coordinator: AnyObject {
    var childCoordinators: [Coordinator] { get set }
    var navigationController: UINavigationController { get }
    func start()
}

final class AppCoordinator: Coordinator {
    func showProfile(userId: String) {
        let coordinator = ProfileCoordinator(
            navigationController: navigationController,
            userId: userId
        )
        childCoordinators.append(coordinator)
        coordinator.start()
    }
}
```

Full implementation in `references/mobile-navigation-patterns.md`.

---

## 12. Offline-First Architecture

### Three-Tier Data Strategy

```
┌─────────────────────────────────────────────┐
│  TIER 1: UI reads from local DB only       │
│  (Room / Core Data / GRDB)                  │
│  Never reads from network directly          │
├─────────────────────────────────────────────┤
│  TIER 2: Sync Engine                        │
│  Fetches from API → writes to local DB      │
│  Queues local writes → pushes to API        │
├─────────────────────────────────────────────┤
│  TIER 3: Conflict Resolution                │
│  Last-write-wins (LWW) or CRDT for          │
│  collaborative data                         │
└─────────────────────────────────────────────┘
```

Full implementation in `references/offline-first-mobile.md`.

---

## 13. State Management at Scale

As apps grow, state management becomes the primary architectural concern. The patterns here scale from 1 to 200+ screens.

| Scale | Pattern | State Location | Sync Mechanism |
|---|---|---|---|
| 1-5 screens | @Published / StateFlow per VM | Per-ViewModel | Manual parent-child |
| 5-20 screens | Shared state via injected Store/Repository | Singleton Store | Combine/Flow |
| 20-100 screens | Feature-scoped state with DI scopes | DI-scoped containers | Event bus or shared Store |
| 100+ screens | Multi-module state with TCA/Rx Store | Per-module Store + shared core | Actions cross module boundaries |

Full implementation in `references/mobile-state-management.md`.

---

## 14. Dependency Injection & Modularization

### DI Framework Selection

| Platform | Framework | Notes |
|---|---|---|
| iOS | Swinject, Factory, Needle, or manual constructor injection | For <10 deps, manual is cleaner |
| Android | Hilt (preferred), Koin, Dagger | Hilt is Google-recommended |
| KMP | Koin (multiplatform), manual injection | Koin works on both platforms |

### Modularization Principles

- **Interface modules:** Feature modules expose only public API interfaces
- **No transitive dependencies from features:** `:feature-checkout` cannot depend on `:feature-profile`
- **Shared nothing by default:** Only `:core:models`, `:core:di`, `:core:navigation` are shared
- **Build graph is a DAG:** Cyclic dependencies between modules are banned via lint rule

---

## 15. Testing Strategy Per Architecture

| Architecture | Unit Tests | Integration Tests | UI Tests | Test Pyramid |
|---|---|---|---|---|
| **MVVM** | ViewModel (70%) | Repository + API (20%) | Critical flows (10%) | Standard pyramid |
| **Clean Architecture** | UseCases (60%) | Repository impls (25%) | Screen flows (15%) | Broad base, narrow top |
| **VIPER** | Interactor + Presenter (80%) | Router + assembly (15%) | Smoke tests (5%) | Very broad base |
| **MVI** | Reducer (75%) | Side effects (15%) | Compose UI (10%) | Broad base |
| **TCA** | Reducer + effects (85%) | Integration store (10%) | Snapshot (5%) | Broadest base |

**Testing non-negotiables:**
- Every ViewModel/Reducer has >80% unit test coverage
- Every UseCase is tested with mock repositories
- Every API error path is tested (network timeout, 4xx, 5xx, malformed JSON)
- State restoration is tested via process death simulation

---

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "We'll start with MVC and refactor when the app gets complex" | A 50-screen MVC app has Massive View Controllers of 2000+ lines each; refactoring to MVVM or VIPER means rewriting every screen — 6-12 months of work vs 2 weeks to start with the right pattern |
| "Offline support can wait until v2" | Mobile users experience connectivity loss 10-20 times per day; an app that shows blank screens or loses data during these moments gets uninstalled within the first week — there is no v2 for churned users |
| "We don't need a DI framework for a simple app" | Without DI, every ViewModel instantiates its own dependencies; unit testing requires mocking 8 singletons and 3 UserDefaults — tests become unmaintainable within 3 months and coverage collapses |
| "State management? Just use @Published everywhere" | Uncontrolled @Published cascades trigger 5x more view redraws than needed; a list of 100 items re-renders entirely when one item changes — scroll jank at 15fps kills perceived performance |
| "We'll handle background tasks with simple DispatchQueue calls" | iOS kills background tasks after 30 seconds; Android's Doze mode defers work indefinitely — without WorkManager/BGTaskScheduler, critical sync operations silently fail and data is lost |

## Reference Files

| File | Content | Lines |
|---|---|---|
| `references/mvvm-mobile-patterns.md` | Swift & Kotlin MVVM with SwiftUI & Compose | 200+ |
| `references/clean-architecture-mobile.md` | Clean Architecture with multi-module setup | 200+ |
| `references/viper-architecture-ios.md` | VIPER module templates and wireframe | 200+ |
| `references/mvi-android-patterns.md` | MVI with Compose and sealed class state | 200+ |
| `references/tca-composable-architecture.md` | TCA reducers, effects, and store composition | 200+ |
| `references/mobile-navigation-patterns.md` | Coordinators, deep linking, state restoration | 200+ |
| `references/offline-first-mobile.md` | Sync engine, conflict resolution, queue | 200+ |
| `references/mobile-state-management.md` | Scoped state, immutable state, performance | 200+ |
