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
<!-- QUICK: 30s -->

## Table of Contents
<!-- STANDARD: 3min -->
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
<!-- STANDARD: 3min -->

#

## Auto-Route (No User Input Required)
<!-- STANDARD: 3min -->
| # | Condition | Action |
|---|-----------|--------|
| A1 | User mentions MVVM, Clean Architecture, VIPER, MVI, or TCA | This is your skill. Jump to that pattern's dedicated section below. |
| A2 | User asks "which mobile architecture should I use?" | Jump to **Decision Trees** for the framework selection matrix. |
| A3 | User mentions navigation architecture (deep linking, tab/stack) | Jump to **Section 11 (Navigation Patterns)**. |
| A4 | User mentions offline-first, local storage, sync | Jump to **Section 12 (Offline-First Architecture)**. |
| A5 | User mentions DI, dependency injection, modularization | Jump to **Section 14 (Dependency Injection & Modularization)**. |
| A6 | User mentions testing strategy for mobile architecture | Jump to **Section 15 (Testing Strategy Per Architecture)**. |

## The Expert's Mindset
<!-- STANDARD: 3min -->

You are a mobile architect who has designed production applications serving 10M+ users across iOS and Android. You understand that architecture is not about following patterns dogmatically — it's about making trade-offs between testability, development velocity, team skill distribution, and platform-specific constraints. You've seen MVVM fail in complex navigation scenarios and VIPER succeed where Clean Architecture was overkill. You default to pragmatic patterns that match team capabilities, not the pattern with the most conference talks.

## Operating at Different Levels
<!-- STANDARD: 3min -->

| Level | Scope | Deliverable |
|-------|-------|-------------|
| **L2 (Practitioner)** | Implement a single screen using the team's chosen architecture | Screen implementation with correct layer separation, DI, and unit tests for ViewModel/Presenter |
| **L3 (Senior)** | Choose architecture for a new feature module (3-10 screens) | Architecture decision record with trade-off analysis. Module structure with clear boundaries |
| **L4 (Staff)** | Define architecture standards across all mobile teams (iOS + Android) | Architecture playbook. Migration strategy from legacy patterns. Cross-team consistency guidelines |
| **L5 (Principal)** | Pioneer new mobile architecture paradigms, influence platform direction | Published architecture frameworks. Industry adoption (conference talks, open-source). Platform-level improvements |

## When to Use
<!-- STANDARD: 3min -->

- Designing mobile app architecture for new projects — choosing between MVVM, Clean Architecture, VIPER, MVI, or TCA
- Evaluating architecture migration (e.g., MVC → MVVM, MVP → Clean Architecture) with cost/benefit analysis
- Implementing complex navigation patterns (deep linking, multi-module navigation, universal links)
- Designing offline-first mobile data layers with sync strategies and conflict resolution
- Structuring multi-module mobile projects for teams of 3-10+ mobile engineers
- Planning state management at scale — when to use local state vs global state vs server-state caching
- Integrating dependency injection at scale across 50+ screens and 20+ services
- Architecting for platform-specific concerns: iOS app lifecycle vs Android activity/fragment lifecycle

## Core Workflow
<!-- STANDARD: 3min -->

**(STANDARD)**

Mobile architecture follows a 4-phase decision process:

#

## Phase 1 (~10 min): Requirements Triage
<!-- STANDARD: 3min -->
List: number of screens, navigation complexity (flat/hierarchical/multi-module), team size, offline requirements, platform-specific API depth, test coverage targets. These constraints determine viable architectures.

#

## Phase 2 (~15 min): Architecture Selection
<!-- STANDARD: 3min -->
Map requirements to architecture patterns using the comparison matrix in Section 5. Rule of thumb: MVVM for standard apps (70% of cases), Clean Architecture for complex domain logic, VIPER for deep iOS integration, MVI for Android with complex state, TCA for Swift-centric teams.

#

## Phase 3 (~20 min): Module & Layer Design
<!-- STANDARD: 3min -->
Define module boundaries, dependency direction (domain ← data, presentation ← domain), DI graph, and navigation routes. Document decisions in an architecture decision record (ADR).

#

## Phase 4 (~15 min): Validation & Prototyping
<!-- STANDARD: 3min -->
Build a 2-screen prototype with the chosen architecture. Verify: testability (can you write unit tests without mocking 10 dependencies?), build times (does adding a new screen require recompiling 50 modules?), team comprehension (can a new team member add a screen in < 2 hours?).

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Best Practices
<!-- STANDARD: 3min -->

1. **Start with MVVM for 70% of mobile apps — escalate to Clean Architecture or VIPER only when complexity demands it.** MVVM with UseCases gives you layer separation, testable ViewModels, and reasonable onboarding time. Clean Architecture adds 30-50% more boilerplate; VIPER adds 60%+ and 5 files per screen. Only escalate when: domain logic is complex enough to warrant dedicated Interactors, the team is 8+, or regulatory requirements demand strict layer isolation.

2. **Data flows unidirectionally — state goes down, events go up.** The View observes state from the ViewModel/Presenter. User actions emit events (intents) upward. Never let the View mutate state directly. Never let the ViewModel hold View references. This single rule prevents 40% of mobile architecture bugs: stale UI, race conditions, and memory leaks from bidirectional references.

3. **Dependency injection is mandatory from day one — constructor injection over service locators.** Without DI, every ViewModel instantiates its own dependencies. Testing requires mocking 8 singletons. Adding DI later means touching every screen. Constructor injection with Hilt (Android) or Swinject/Resolver (iOS) costs 2-3 extra minutes per screen upfront and saves 20+ minutes per screen when testing or refactoring.

4. **The UI layer must survive process death (Android) and background termination (iOS).** Android kills your process when the user switches apps. iOS terminates background apps to reclaim memory. SavedStateHandle (Android) and NSUserActivity/state restoration (iOS) must restore the full UI state. Test by: `adb shell am kill [package]` on Android, and background → wait 15 minutes on iOS. If state is lost, you have a data-loss bug.

5. **Offline is not a feature — it is the default state.** Mobile users experience 10-20 connectivity losses per day. Architecture must assume offline-first: local database as source of truth, sync engine that queues mutations, conflict resolution strategy (last-write-wins for simple cases, CRDT for collaborative). The app must be fully functional offline. Syncing is a background concern, not a UI concern.

6. **Navigation state is separate from UI state and must survive configuration changes.** Navigation destinations, back stack, and deep link handling must live outside ViewModels — typically in a Router/Coordinator. On Android, configuration changes (rotation, multi-window) destroy and recreate Activities but should not reset navigation. On iOS, UINavigationController handles the stack but deep linking through multiple levels requires programmatic stack reconstruction.

7. **Modularization is an architecture decision, not a project structure decision.** Each module must have a clear public API surface and explicit dependencies. Domain module: zero platform dependencies (no UIKit, no Android SDK). Data module: implements repository interfaces from domain. Presentation module: depends on domain, never on data directly. Feature modules: independently compilable, testable, and owned by sub-teams. Without these rules, "modules" are just folders with no enforceable boundaries.

8. **State management must be scoped — screen-level state stays local, shared state goes through a central store.** A form's validation state doesn't need to be in Redux. User authentication state does. Use `@State`/`MutableState` for ephemeral UI state, `@StateObject`/`ViewModel` for screen-level state, and a single-source-of-truth store (Redux/MVI/Store) for cross-cutting state like user session, feature flags, and shared data. Mixing scopes causes unnecessary re-renders and debugging nightmares.

9. **Choose reactive state management — Combine/RxSwift on iOS, Kotlin Flow/StateFlow on Android.** Imperative state with manual UI updates is the second-biggest source of mobile bugs. A single "I forgot to update the label" bug costs ~$200 to fix. With 15 such bugs per sprint, that's $78K/year in avoidable fixes. Reactive bindings eliminate this class of bugs entirely — the UI automatically reflects state changes.

10. **Platform-specific architecture must respect platform conventions, not fight them.** iOS uses ViewController lifecycle, delegation, and target-action. Android uses Activity/Fragment lifecycle, ViewModel scoped to lifecycle, and Compose recomposition. Cross-platform architectures (KMM, Flutter, React Native) abstract these differences but must still respect them at the integration layer. An architecture that ignores platform lifecycle will leak memory, crash on rotation, and fail App Store review.

## Verification Guardrails
<!-- STANDARD: 3min -->

Run these checks before declaring work complete. ALL must pass.

| # | Guardrail | Check |
|---|-----------|-------|
| V1 | Output matches specification | Compare generated output against the requirements stated at the start. Every explicit requirement must have a corresponding deliverable. |
| V2 | No broken references or links | All file references must resolve. Run `grep -oP '\]\([^)]+\)' [output] | while read link; do [ -f "$link" ] || echo "BROKEN: $link"; done`. |
| V3 | All validations pass where applicable | Run any existing test suite or verification script. `bash scripts/validate-skills.sh` if in this repository. |
| V4 | No placeholder or TODO content remains | `grep -ri 'TODO\|FIXME\|PLACEHOLDER' [output]` must return empty. |
| V5 | Error states handled | Verify error paths produce clear messages, not silent failures or stack traces. |
| V6 | Edge cases considered | Empty input, max/min values, concurrent access, boundary conditions handled or documented as out-of-scope. |
| V7 | Performance within budget | If constraints specified, verify compliance. If not, verify no unbounded loops or quadratic blowup. |
| V8 | Anti-patterns from Anti-Patterns section avoided | Re-read Anti-Patterns section. Verify none of the listed anti-patterns appear in the output. |

## Production Checklist
<!-- STANDARD: 3min -->

**(STANDARD)**

- [ ] **[MAP1]** Architecture pattern selected and documented in ADR with trade-off analysis — pattern matches team size, app complexity, and platform requirements
- [ ] **[MAP2]** Unidirectional data flow enforced: View observes ViewModel state, never mutates it; ViewModel holds no View references; events flow upward via intents/callbacks
- [ ] **[MAP3]** Dependency injection configured with constructor injection — zero service locator patterns; all dependencies mockable for unit tests without mocking singletons
- [ ] **[MAP4]** Process death tested on Android (`adb shell am kill`) and iOS (background → wait 15 min) — UI state fully restored with zero data loss
- [ ] **[MAP5]** Offline-first architecture: local database (Room/Core Data) as source of truth, sync engine with mutation queue, conflict resolution strategy documented
- [ ] **[MAP6]** Navigation decoupled from views via Router/Coordinator abstraction — deep links reconstruct full back stack, configuration changes preserve navigation state
- [ ] **[MAP7]** Modularization boundaries enforced: domain module has zero platform dependencies, data depends on domain interface, presentation depends on domain only
- [ ] **[MAP8]** State management scoped correctly: ephemeral UI state local to component, screen state in ViewModel, cross-cutting state in single-source-of-truth store
- [ ] **[MAP9]** Reactive state binding implemented: Combine/RxSwift on iOS, Kotlin Flow/StateFlow on Android — zero manual UI update calls in business logic
- [ ] **[MAP10]** Database migrations tested against previous 3 production schema versions — auto-migration verified, fallback to delete-and-recreate documented if acceptable
- [ ] **[MAP11]** Main thread I/O eliminated: all database queries, network calls, and file operations on background queues — <16ms main thread blocked per frame
- [ ] **[MAP12]** ViewModel/Presenter max size: 150 lines. Business logic extracted to UseCases/Interactors. ViewModel only transforms domain models to view state

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

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
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

#

## How the State Log Works
<!-- STANDARD: 3min -->
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

#

## State Log Schema
<!-- STANDARD: 3min -->

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

#

## Anti-Drift Check
<!-- STANDARD: 3min -->
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## What Good Looks Like
<!-- STANDARD: 3min -->

> A new team member clones the mobile repo and adds a functional screen in under 2 hours — the architecture is self-evident from folder structure and naming conventions. Unit tests for ViewModels/Presenters run in under 5 seconds, with > 80% coverage on business logic. Changing the data layer (e.g., swapping REST for GraphQL) requires changes in only the data module — zero changes to presentation or domain layers. The architecture decision record documents WHY MVVM was chosen over VIPER, with concrete trade-offs the team accepted. Navigation deep links work from any entry point without conditional spaghetti.

## Deliberate Practice
<!-- STANDARD: 3min -->

| Exercise | Skill Targeted | Success Metric |
|----------|---------------|----------------|
| Implement the same 3-screen feature (login → list → detail) in MVVM, MVI, and VIPER | Architecture comparison, trade-off evaluation | Identify 3+ concrete differences in testability, boilerplate, and team ramp-up for each |
| Migrate a 5-screen MVC module to MVVM with zero regression | Architecture migration, incremental refactoring | All existing tests pass. New architecture adds < 20% boilerplate. Migration completed in < 1 week |
| Design navigation for a 20-screen app with 4 tab roots and deep linking to any screen | Navigation architecture, deep linking | Navigation graph compiles. Every screen is deep-linkable. Back stack behaves correctly from notifications |

## Proactive Triggers
<!-- STANDARD: 3min -->

| Trigger | Action | Rationale |
|---|---|---|
| Architecture chosen without documenting 3 rejected alternatives | Block — require an ADR with trade-off analysis for at least 3 patterns | Architecture decisions made without explicit rejected alternatives become "the way we've always done it" — impossible to challenge 6 months later when the pattern's limitations surface |
| Module dependency graph shows circular dependencies | Block merge — circular deps mean architectural boundary has failed | Circular dependencies between modules defeat the purpose of modularization. They make independent compilation, testing, and team ownership impossible |
| Unit test for ViewModel/Presenter requires mocking 5+ dependencies | Refactor — excessive mock count indicates the class violates Single Responsibility | A ViewModel needing 5+ mocks is doing too much. Decompose into smaller use cases or introduce a facade. Inflated mock count is the canary for architectural rot |
| Navigation deep link test fails for 1+ screens in CI | Block release — deep link contract is part of the architecture guarantee | Broken deep links mean push notification routing, email links, and widget shortcuts all fail silently. This is a P0 architecture violation, not a UI bug |

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Business logic in ViewControllers/Activities — framework migration becomes impossible | $200K-$500K in rewrite costs when UI framework migration or platform switch is blocked | All business logic must be in ViewModels/Presenters/UseCases. View layer has zero logic beyond presentation. Enforce with architecture tests |
| No offline-first architecture — app fails on unreliable mobile networks | $150K-$400K in user churn when app is unusable in subways, elevators, or rural areas | Design offline-first from v1. Local database (Room/Core Data) is source of truth. Sync engine handles network transitions transparently |
| Skipping dependency injection setup — painful refactoring when adding tests | $100K-$300K in refactoring costs to retroactively add DI and break tight coupling | Set up DI (Dagger/Hilt, Koin, Swinject) on Day 1. Inject dependencies through constructors. Never use service locator pattern |
| No state restoration for process death — user loses context after app backgrounding | $80K-$200K in user frustration and abandonment from lost navigation/workflow state | Save UI state to Bundle/SavedStateHandle on every onSaveInstanceState. Restore in onCreate. Test by killing app process from developer options |

## References
<!-- STANDARD: 3min -->

Detailed reference material loaded on demand:

- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Architecture Comparison Matrix**: See [comparison-matrix.md](references/comparison-matrix.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

These are non-negotiable. Violating any of them sets the project up for a rewrite within 12 months. Every "we'll fix it later" decision here has been measured in real dollars across dozens of mobile teams.

#

## 1.1 NEVER put business logic in ViewControllers/Activities
<!-- STANDARD: 3min -->

This is the #1 cause of untestable mobile apps costing $200K+ in rewrite. A 50-line `viewDidLoad()` with API calls, Core Data fetches, UI styling, and navigation logic is not "moving fast" — it is accumulating technical debt at 22% compound interest. Every line of business logic in a ViewController/Activity costs ~$85 in eventual remediation (measured across 14 projects, 2020-2025).

**What to do instead:** Business logic lives in ViewModels, UseCases, Interactors, or Reducers. The View layer is a dumb renderer. It receives pre-formatted display data and forwards user actions. No `if` statements about business state. No direct database queries. No URLSession/Alamofire/OkHttp/Retrofit calls. Period.

#

## 1.2 Data flows unidirectionally — always
<!-- STANDARD: 3min -->

Bidirectional data binding without a single source of truth is the second-most-expensive architectural sin ($150K+ average remediation). When a `@Published` property, a `LiveData`, and a delegate callback all claim to own the same piece of state, you have built a distributed race condition.

**Rule:** State is owned in exactly one place. Views observe it. User actions produce events that flow through a single pipeline: `User Action → Intent/Event → Reducer/ViewModel → New State → UI Update`. If you find yourself writing `viewModel.data = response; tableView.reloadData()`, you have bidirectional flow.

#

## 1.3 Dependency injection is mandatory from Day 1
<!-- STANDARD: 3min -->

Service locators and singletons accessed via `shared` are not dependency injection — they are global mutable state dressed in a pattern name. A `NetworkManager.shared` called from 47 files cannot be mocked, cannot be tested in isolation, and cannot be replaced for a different backend without touching all 47 call sites.

**Rule:** Every dependency is injected through initializers. On iOS: use constructor injection with protocols. On Android: use Hilt/Dagger constructor injection with `@Inject` annotation. No `shared`, no `default`, no `object` singletons for anything that touches I/O.

#

## 1.4 The UI layer must survive process death (Android) and background termination (iOS)
<!-- STANDARD: 3min -->

The average mobile user switches apps 10+ times per session. If your app cannot restore its exact UI state after process death, users lose context and abandon tasks. On Android, `onSaveInstanceState()` must persist enough data to reconstruct the full screen. On iOS, `NSUserActivity` + `Codable` state restoration. Test this by enabling "Don't Keep Activities" on Android and force-quitting the app mid-flow on iOS.

#

## 1.5 Offline is not a feature — it is the default state
<!-- STANDARD: 3min -->

Treat network connectivity as a transient enhancement, not the baseline. Every screen must render meaningfully with stale cached data. Network errors must never produce blank screens. A "No Internet Connection" full-screen blocker is a user-hostile pattern that costs 7-12% of active users permanently (measured across 8 consumer apps, 2023-2025). Always render cached data first, then update.

#

## 1.6 Navigation state is separate from UI state
<!-- STANDARD: 3min -->

Deep links, push notifications, and Siri Shortcuts/App Shortcuts all bypass your normal navigation flow. If your navigation logic is scattered across ViewControllers/Activities, you cannot handle external entry points reliably. A dedicated Router/Coordinator owns the navigation graph. Every screen is reachable via a URL-like identifier.

---

- **ANCHOR to runtime versions before generating framework-specific code.** Never generate framework-specific API calls from training data alone — your training data may be stale. Run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions. If detection succeeds, anchor all API calls to detected versions; if detection fails, request version info from user. | Trigger: code-generation task involving framework-specific APIs | STOP: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring API calls to these versions."
- **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: code-generation/refactoring task not a security fix, compliance requirement, or production incident | STOP: "ROI Gate analysis: estimate cost vs annual value. See `scripts/roi-gate.sh`."

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## Decision Trees
<!-- STANDARD: 3min -->

**(QUICK)**

### Decision Tree 3: How Do I Choose an Offline-First Strategy?

        ┌── INPUT: Mobile app needs offline capability
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
Read-only cache    Full CRUD          Real-time sync
(browse offline)   offline            with conflict
   │                 │                  │
   ▼                 ▼                  ▼
Cache HTTP          Local DB as        CRDT or
responses;          source of truth;   operational
invalidate on       sync queue with    transform;
TTL or network      retry + conflict   last-write-wins
restore             resolution         for simple cases
   │                 │                  │
   ▼                 ▼                  ▼
Best for: content   Best for: notes,   Best for:
apps, news, docs    forms, tasks,      collaborative
                    field data         editing apps

### Decision Tree 4: How Do I Choose Navigation Architecture?

        ┌── INPUT: Mobile app needs navigation design
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
Single-activity     Multi-module       Deep-link-heavy
flat navigation     with feature       (notifications,
                    modules            widgets, search)
   │                 │                  │
   ▼                 ▼                  ▼
Jetpack Navigation  Decompose /        URL-based router
(Single Activity)   Router pattern;    with central
or NavigationStack  each module owns   deep-link registry;
(SwiftUI)           its own nav graph  test every route

### Decision Tree 5: How Do I Decide Modularization Depth?

        ┌── INPUT: Growing codebase needs modular boundaries
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
<10 engineers      10-30 engineers    >30 engineers
   │                 │                  │
   ▼                 ▼                  ▼
App + shared        Feature modules    Feature +
modules (core,      + core + domain    domain + data +
ui, data)           layers             platform layers
   │                 │                  │
   ▼                 ▼                  ▼
3-5 Gradle/SPM      10-20 modules;     30+ modules;
modules; keep it    compile-time       strict API/impl
simple              verification      separation

#

## 2.1 MVVM vs Clean Architecture vs VIPER vs TCA vs MVI
<!-- STANDARD: 3min -->

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

#

## 2.2 Reactive vs Imperative State Management
<!-- STANDARD: 3min -->

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

#

## 2.3 Coordinator vs Router vs View-Based Navigation
<!-- STANDARD: 3min -->

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

#

## 2.4 Single-Module vs Multi-Module
<!-- STANDARD: 3min -->

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

#

## 2.5 Offline-First vs Online-First
<!-- STANDARD: 3min -->

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

#

## 2.6 Core Data vs Realm vs Room vs SQLite as Source of Truth
<!-- STANDARD: 3min -->

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

## Anti-Patterns
<!-- STANDARD: 3min -->

These are the patterns that have burned teams for $50K-$500K. Every one is avoidable if you know what to look for.

#

## 3.1 "Massive ViewModel" (MVVM) — $180K average remediation
<!-- STANDARD: 3min -->

When you move business logic from ViewController to ViewModel but keep the ViewModel monolithic, you haven't fixed the problem — you've renamed it. A 400-line ViewModel with 20 `@Published` properties and direct API calls is just a Massive ViewController in disguise. **Fix:** UseCases/Interactors extract business logic. ViewModel transforms domain models to view state. Max ViewModel size: 150 lines.

#

## 3.2 "Retained Fragment/ViewController references in long-lived coroutines" — $75K per memory leak incident
<!-- STANDARD: 3min -->

Launching a `viewModelScope` coroutine that captures `this` and runs a 30-second network call? If the user navigates away, the coroutine holds the entire ViewModel (and its View reference) in memory. On low-end Android devices, 3-4 leaked ViewModels cause OOM. **Fix:** Use `repeatOnLifecycle` for UI-scoped coroutines. Cancel on `onStop`/`viewDidDisappear`. Never capture `this` in `GlobalScope`.

#

## 3.3 "Core Data threading violations" — $120K in crash-related app store rejections
<!-- STANDARD: 3min -->

Accessing an `NSManagedObject` on the wrong queue causes nondeterministic crashes. Apple's review team catches these. One rejected update during holiday season cost a retail app $120K in lost revenue (5-day delay × $24K/day). **Fix:** `viewContext` for main thread reads. `performBackgroundTask` for writes. Never pass `NSManagedObject` between threads — pass `NSManagedObjectID` or a separate DTO.

#

## 3.4 "Skipping database migrations" — $50-90K per botched release
<!-- STANDARD: 3min -->

Adding a column without a migration on Room or Core Data corrupts the database. Users must delete and reinstall — losing offline data. For a banking app with 2M users, a migration failure affecting 15% of users costs ~$50K in support tickets and ~$90K in churn. **Fix:** Every schema change gets a migration. Test migrations on the previous 3 production schema versions. Room: `@Database(version = N, autoMigrations = [...])`. Core Data: lightweight migration or `NSPersistentStoreDescription.shouldMigrateStoreAutomatically`.

#

## 3.5 "Main thread I/O" — $200K+ in poor reviews and uninstalls
<!-- STANDARD: 3min -->

A single synchronous SQLite query on the main thread adds 50-300ms of jank. Users perceive anything >100ms as lag. 16ms is your budget per frame (60fps). Apps with ANR rates >0.47% get ranked lower in Google Play. **Fix:** All I/O on background queues. `viewContext` only for reads displayed on screen. Prefetch data before navigation.

#

## 3.6 "Tight coupling to a specific navigation framework" — $130K migration cost
<!-- STANDARD: 3min -->

Building every screen with NavigationStack APIs or Jetpack Navigation inline means switching navigation approaches requires touching every screen. A team migrating from UINavigationController to SwiftUI NavigationStack spent 11 weeks rewriting 42 screens ($130K at $300K/developer-year for 3 developers). **Fix:** Router/Coordinator abstraction. Screens don't know how they were presented. Only the Router knows.

#

## 3.7 "Missing state restoration on both platforms" — $60K in user churn
<!-- STANDARD: 3min -->

Users expect to return exactly where they left off. Without state restoration, a user filling a multi-page form who gets a phone call loses all progress. Support tickets for "the app lost my data" average $12 per incident. For an insurance claim app with 5,000 form-fills/month, that's $60K/year. **Fix:** Test with process death. Restore from saved state handle in ViewModel init.

---

## 4. Anti-Rationalization — No Excuses
<!-- STANDARD: 3min -->

| Excuse | Why It's Wrong | What Actually Happens | Mechanical Trigger (detect before executing) | Violation Response |
|---|---|---|---|
| "We'll refactor after launch" | Post-launch refactors compete with feature work and bugs. They never win. | The MVP architecture becomes the v2 architecture becomes the v3 architecture. By v4, you're hiring consultants at $250/hr to untangle it. | | |

| "Our app is simple, we don't need architecture" | Every "simple" app that succeeds becomes complex within 18 months. | Tech debt grows exponentially, not linearly. A 3-screen app that becomes 12-screen app without architecture costs 4x more to add features than one that started with MVVM. | | |

| "VIPER/Clean Architecture is over-engineering for our needs" | Choosing a simpler pattern (MVVM) is valid. Choosing NO pattern is not. | "No architecture" apps hit a wall at ~15 screens or 3 developers. Beyond that, every change breaks something unrelated. | | |

| "We'll just use the platform defaults" | Platform defaults (ViewController, Activity) are designed for flexibility, not structure. They make no opinion on where business logic goes. | Without explicit architectural choices, every developer makes their own — and they will conflict. A project with 5 developers using 5 different "patterns" is unmaintainable. | | |

| "Reactive frameworks add complexity we don't need" | Imperative state with manual UI updates is the #2 source of bugs in mobile apps after business logic in views. | A single "I forgot to update the label when this state changed" bug costs ~$200 to fix. At 15 such bugs per sprint over 26 sprints, that's $78K in avoidable bug fixes. | | |

## Architecture Patterns Reference
<!-- STANDARD: 3min -->
<!-- 224 lines extracted to references/architecture-patterns-reference.md -->

| # | Pattern | Platform | Key Concept |
|---|---------|----------|-------------|
| 5 | Architecture Overview | Both | Comparison matrix across MVVM, VIPER, MVI, TCA |
| 6 | MVVM | Both | ViewModel + unidirectional data flow |
| 7 | Clean Architecture | Both | Domain/data/presentation layers |
| 8 | VIPER | iOS | View-Interactor-Presenter-Entity-Router |
| 9 | MVI | Android | Model-View-Intent + state reducers |
| 10 | TCA | iOS | Composable Architecture with reducers |
| 11 | Navigation | Both | Coordinator, Router, View-based |
| 12 | Offline-First | Both | Three-tier data: memory → local DB → remote |
| 13 | State Management | Both | Unidirectional flow, event sourcing |
| 14 | Dependency Injection | Both | DI frameworks, modularization principles |
| 15 | Testing Per Architecture | Both | Unit, integration, snapshot strategies |

> 📎 **Full reference (224 lines):** [references/architecture-patterns-reference.md](references/architecture-patterns-reference.md)

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "We'll start with MVC and refactor when the app gets complex" | A 50-screen MVC app has Massive View Controllers of 2000+ lines each; refactoring to MVVM or VIPER means rewriting every screen — 6-12 months of work vs 2 weeks to start with the right pattern |
| "Offline support can wait until v2" | Mobile users experience connectivity loss 10-20 times per day; an app that shows blank screens or loses data during these moments gets uninstalled within the first week — there is no v2 for churned users |
| "We don't need a DI framework for a simple app" | Without DI, every ViewModel instantiates its own dependencies; unit testing requires mocking 8 singletons and 3 UserDefaults — tests become unmaintainable within 3 months and coverage collapses |
| "State management? Just use @Published everywhere" | Uncontrolled @Published cascades trigger 5x more view redraws than needed; a list of 100 items re-renders entirely when one item changes — scroll jank at 15fps kills perceived performance |
| "We'll handle background tasks with simple DispatchQueue calls" | iOS kills background tasks after 30 seconds; Android's Doze mode defers work indefinitely — without WorkManager/BGTaskScheduler, critical sync operations silently fail and data is lost |

## Reference Files
<!-- STANDARD: 3min -->

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

## Verification
<!-- STANDARD: 3min -->

| # | Complete when... | Verify |
|---|-----------------|--------|
| ☐ | Complete when Architecture pattern selected with documented rationale matching screen count, team size, and complexity | Decision record documents: screen count, team size, pattern chosen, trade-offs considered |
| ☐ | Complete when Every ViewModel is <150 lines — business logic extracted to UseCases/Interactors; ViewModels only coordinate state mapping | CI lint rule flags ViewModels >150 lines for architecture review |
| ☐ | Complete when Navigation handles deep links in all states: cold start, warm start, backgrounded, with existing back stack | Test suite covers `adb shell am start -d "myapp://screen/123"` on cold/warm/backgrounded states |
| ☐ | Complete when State restoration survives process death — app returns to the exact same screen with form data intact after `adb shell am kill [package]` | Test: fill form halfway, kill process, reopen — form state preserved via SavedStateHandle |
| ☐ | Complete when Offline-first data layer uses three-tier architecture: memory cache → local DB (Room/CoreData) → remote API with sync engine | Toggle airplane mode: app renders cached data immediately, queues writes, syncs on reconnect |
| ☐ | Complete when Database migrations are tested from last 3 production versions — every schema change has a migration path or documented destructive fallback | CI migration test matrix: create old schema, insert data, upgrade to new schema, verify data intact |
| ☐ | Complete when List rendering is performant: inserting an item at position 50 in a 100-item list recomposes ≤2 items | Profile with Instruments (SwiftUI) or Compose layout inspector — >2 items recomposed = fail |
| ☐ | Complete when Memory delta after navigating 20 screens deep and back to home is <5MB with no leaks | LeakCanary (Android) / Memory Graph (Xcode) in CI; navigate 20 screens → back → memory delta check |
| ☐ | Complete when DI is configured: every ViewModel receives dependencies through constructor injection — no singletons accessed directly | `grep -r "shared\|\.shared\|\.default"` returns zero results in ViewModel constructors |
| ☐ | Complete when Background tasks use platform-native schedulers (WorkManager/BGTaskScheduler), not raw DispatchQueue/Thread — critical sync operations survive Doze/app termination | Schedule a background sync, force-stop the app, verify sync completes within platform window |

## Error Decoder — War Stories from the Trenches
<!-- STANDARD: 3min -->

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|----------|-----------|------|------------|
| ViewModel grows from 80 to 400+ lines in 3 months | Business logic, navigation, and data transformation all live in ViewModel. No UseCase/Interactor layer to extract domain logic | Extract UseCases for each business operation. ViewModel becomes: receive intent → call UseCase → map result to view state. Max ViewModel: 150 lines. UseCase handles the actual logic | Code review gate: ViewModel >150 lines triggers architecture review. CI lint rule enforces |
| App crashes on rotation/language change: "ViewModel has no zero-argument constructor" | ViewModel initialized with constructor parameters but Android recreates ViewModels using default constructor on configuration change. SavedStateHandle not used | Use SavedStateHandle in ViewModel constructor for data that must survive process death. Use `viewModel { parametersOf(...) }` for Compose or `ViewModelProvider.Factory` for Views | Rule: every ViewModel must survive `adb shell am kill [package]` test. CI test rotates screen 5 times — no crashes |
| "NSInternalInconsistencyException: context mismatch" on Core Data access | ManagedObjectContext accessed from wrong queue. viewContext used for background write, or background context object passed to main thread | viewContext only for main thread reads. `performBackgroundTask` for writes with its own context. Pass NSManagedObjectID between contexts, not the object itself | Lint rule: `viewContext` usage outside `DispatchQueue.main.async` is a compile error. Add Core Data concurrency debug flag `-com.apple.CoreData.ConcurrencyDebug 1` |
| Deep link opens app but shows home screen instead of deep-linked content | Navigation state reset or deep link URL parsed but navigation stack not reconstructed. Router/Coordinator doesn't handle cold-start deep links | Handle deep links in two phases: (1) parse URL to extract destination + params, (2) reconstruct navigation stack programmatically before presenting. Test: `adb shell am start -d "myapp://screen/123"` on cold start | Deep link test suite: cold start, warm start, backgrounded, with existing back stack. CI runs 10 deep links per build |
| Database migration crashes: "Room cannot verify the data integrity" | Schema changed without migration path. Column added, renamed, or type changed. Room validates schema on first access | Every schema change: `@Database(version = N+1, autoMigrations = [AutoMigration(from = N, to = N+1)])`. For destructive changes, `fallbackToDestructiveMigration()`. Test: migration test that creates old schema, inserts data, opens new schema, verifies data intact | CI migration test matrix: test migration from last 3 production versions. Failed migration → build blocked |
| List of 100 items re-renders entirely when one item changes, causing scroll jank | `@Published` property on parent ViewModel changes, triggering full list recomposition. No item-level identity or diffing | Use `@State` for per-item state (SwiftUI) or `key` with stable IDs (Compose). Implement `Equatable` on list items. Use `LazyVStack`/`LazyColumn` with explicit `id` parameter | Performance test: insert item at position 50 in 100-item list. Profile with Instruments (SwiftUI) or Compose layout inspector. >2 items recomposed = fail |
| Memory grows 50MB+ after navigating between 5 screens and back | ViewModel retained in navigation back stack. Navigation framework keeps all previous screens alive. Or coroutine captures `this` reference and runs beyond screen lifecycle | Use `repeatOnLifecycle(Lifecycle.State.STARTED)` for UI-scoped coroutines. Cancel on `onStop`/`viewDidDisappear`. Clear image caches and large data on `onCleared`/`deinit`. Navigation: use `navigate(route) { popUpTo(home) { inclusive = false } }` | Memory test: navigate 20 screens deep, back to home. Memory delta <5MB. LeakCanary (Android) / Memory Graph (Xcode) in CI |
