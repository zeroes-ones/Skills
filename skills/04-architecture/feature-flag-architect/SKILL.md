---
name: feature-flag-architect
description: >
  Use when designing a feature flag system, selecting a feature flag SDK (LaunchDarkly,
  Flagsmith, Unleash, Firebase Remote Config), implementing flag-driven development,
  managing flag technical debt, designing kill switches, or architecting gradual rollout
  from a developer perspective. Handles flag architecture patterns (branching by
  abstraction, strategy pattern, dependency injection), flag type taxonomy (release,
  experiment, ops, permission), per-platform implementation (mobile/backend/web/desktop),
  testing with feature flags (combinatorial explosion mitigation), flag lifecycle
  automation, instant-update patterns for mobile, and flag cleanup discipline. Do NOT
  use for release process coordination (route to release-manager), launch-day monitoring
  setup (route to shipping-and-launch), or A/B test experiment design (route to
  ab-testing-specialist).
license: MIT
allowed-tools: Read Grep Glob Bash
tags:
  - feature-flags
  - feature-toggles
  - architecture
  - gradual-rollout
  - kill-switch
  - remote-config
  - technical-debt
author: Sandeep Kumar Penchala
type: architecture
status: stable
version: 1.0.0
updated: 2026-07-26
token_budget: 2800
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
chain:
  consumes_from:
    - release-manager
    - shipping-and-launch
    - ci-cd-builder
  feeds_into:
    - mobile-developer
    - android-developer
    - ios-developer
    - frontend-developer
    - backend-developer
    - fullstack-developer
    - qa-engineer
    - ab-testing-specialist
---

# Feature Flag Architect

**Architect, implement, and maintain feature flag systems from a developer's perspective.** This skill bridges the gap between the operations-focused flag management in `release-manager` and `shipping-and-launch` and the day-to-day development concerns of flag-driven development, SDK integration, testing, and flag debt elimination.

---

## Ground Rules

**G1: Never deploy without a kill switch for every new feature.** Every feature that ships behind a flag must have a runtime kill switch — no deploy required to disable. If a flag's kill switch requires a deploy, the architecture is broken.

**G2: Flags are code paths, not configuration flags.** Treat every branch guarded by a feature flag as a production code path that needs full test coverage. Both branches (flag ON, flag OFF) must be tested independently before the flag reaches any environment beyond development.

**G3: The testing matrix grows exponentially with flags.** N binary flags = 2^N combinations. Without mitigation, 5 flags = 32 test scenarios. Apply pairwise testing, test at flag boundaries, and never combine untested flag states in production. At the first sign of combinatorial explosion, stop and reduce the flag interaction surface.

**G4: Flag removal is not technical debt cleanup — it's a feature.** Flag removal tickets must be created at flag creation, assigned to the flag owner with a hard deadline (60 days post-100% rollout). CI must fail if a flag at 100% for > 30 days has an open removal ticket.

**G5: Mobile apps have one flag evaluation per app launch against the store.** Unlike web/backend, mobile flags can't be updated instantly — app store review creates a 1-14 day delay. Design for stale flag states. Every mobile flag must have a default value that is safe for the entire review window.

---

## Expert's Mindset

### Mental Models

1. **The Flag is a Temporary Fork.** A feature flag is a code fork with a known merge date. Treat it like a feature branch: the longer it lives, the more painful the merge. The merge IS the flag removal — schedule it.

2. **Two Truths, One Flag.** At any moment, the flag evaluates to exactly one state. But the code must maintain two divergent realities until the flag is removed. Both realities must compile, pass tests, and be safe in production.

3. **Flags Don't Retire Themselves.** No flag ever removed itself. The only force that removes flags is a developer writing a PR. Automate the pressure to remove them: CI failures, sprint-level reminders, flag-age dashboards.

4. **The Store is an Adversary.** Mobile app stores inject 1-14 days of flag evaluation lag. A flag disabled on the server can remain active on 100,000 installed apps for two weeks. Design for the worst-case lag.

5. **Every Flag Creates a Dependency.** When service A checks flag X and service B checks flag X, they become coupled through the flag state. A flag toggle can create distributed consistency problems that didn't exist before.

### Cognitive Biases to Guard Against

| Bias | Manifestation | Antidote |
|------|---------------|----------|
| **Temporary Thing Permanence** | "We'll remove this flag next sprint" → flag survives 18 months | Removal ticket created with flag creation, hard deadline |
| **Happy Path Blindness** | Testing only flag=ON, assuming flag=OFF "just works" | CI requires both paths tested before merge |
| **Flag Proliferation Drift** | "One more flag won't hurt" → 47 flags, untestable matrix | Flag budget per service; new flag requires retiring an old one |
| **Store Optimism** | "Users always update their apps" → 30% on version from 18 months ago | Design for the installed base, not the latest release |
| **Kill Switch Complacency** | "We've never needed the kill switch" → kill switch rots, fails when needed | Quarterly kill-switch drills in production |
| **Copy-Paste Flag Pattern** | Copied flag wiring from service A to service B without adapting evaluation context | Flag context is service-specific; always review evaluation point |

---

## Operating Levels

| Level | Scope | Autonomy | Key Capability |
|-------|-------|----------|----------------|
| **L1: Flag Consumer** | Uses flags created by others; adds `if (flag.isEnabled("checkout_v2"))` | Follows team flag conventions | Reads flag evaluation docs; adds flags to code following existing patterns |
| **L2: Flag Implementer** | Designs flags for a single service; manages flag lifecycle for owned features | Independently creates and cleans up flags | Chooses flag type (release/experiment/ops/permission); writes flag-aware tests; removes flags on schedule |
| **L3: Flag Architect** | Designs flag systems for a platform; selects SDKs; defines flag conventions across teams | Makes SDK decisions; sets flag policies | SDK evaluation and selection; flag type taxonomy; cross-service flag coordination; CI enforcement |
| **L4: Organizational Flag Strategist** | Multi-platform flag strategy; flag governance across 50+ services; flag cost modeling | Sets org-wide flag policies | Flag budget allocation; multi-platform flag SDK unification; flag-driven development workflow design; flag cost attribution |
| **L5: Industry Flag Thought Leader** | Advances flag technology; contributes to OpenFeature spec; invents flag patterns | Defines industry best practices | OpenFeature contribution; flag safety proofs; flag-driven architecture patterns for previously unsolved problems |

---

## Core Workflows

### Mode 1: Design a Feature Flag System

**Trigger:** "I need to add feature flags to our [platform] app" or "Which feature flag SDK should we use?"

**Process:**

1. **Assess the platform and requirements.** Determine: target platforms (mobile, web, backend, desktop), evaluation latency requirements, offline behavior needs, team size, compliance constraints, budget.
   - Output: Platform Matrix showing flag evaluation points and constraints per platform.

2. **Classify flag types needed.** Release toggles (temporary), experiment toggles (A/B test), ops toggles (kill switches, circuit breakers), permission toggles (premium features, beta access).
   - Output: Flag Type Map matching each planned flag to its type and lifecycle.

3. **Select evaluation architecture.** Choose between: server-side evaluation (backend, zero client latency), client-side evaluation (mobile/web, works offline), or hybrid (evaluate server-side, sync to client).
   - Output: Evaluation Architecture Diagram per platform.

4. **Evaluate SDKs against requirements.** Matrix: LaunchDarkly (enterprise, multi-platform), Flagsmith (open-source option), Unleash (self-hosted), Firebase Remote Config (mobile-first, free), OpenFeature (vendor-neutral abstraction), homegrown (full control, high maintenance).
   - Output: SDK Recommendation with trade-off analysis.

5. **Define flag conventions.** Naming: `[team].[feature].[variant]` (e.g., `checkout.new_flow.v2`). Default values: OFF for release toggles, control for experiments, ON for ops toggles. Expiry: max 60 days post-100% for release toggles.
   - Output: Flag Convention Guide for all teams.

6. **Build the flag cleanup pipeline.** CI checks: (a) flag at 100% > 30 days with open removal ticket → CI FAIL, (b) flag referenced in code but not in flag registry → CI WARN, (c) flag in registry but never evaluated → CI WARN.
   - Output: CI configuration and removal workflow.

**Completion criteria:** SDK recommendation delivered with trade-off matrix, flag conventions documented, CI enforcement configured, removal workflow tested with a dummy flag.

### Mode 2: Implement Feature Flags in Code

**Trigger:** "I need to add a feature flag for [feature]" or "Help me wrap this new feature behind a flag."

**Process:**

1. **Identify flag type.** Release toggle (temporary, removed after rollout), experiment toggle (A/B, removed after experiment ends), ops toggle (permanent, kill switch), permission toggle (permanent, gated access).
   - Decision: Use the type that matches the flag's purpose and expected lifetime.

2. **Choose the abstraction pattern.**
   - **Branching by Abstraction** (recommended for new features): Create interface/strategy, implement old and new, select via flag.
   - **Simple If/Else** (acceptable for small changes): `if (flags.isEnabled("checkout_v2")) { ... } else { ... }`.
   - **Dependency Injection** (recommended for DI frameworks): Bind implementation based on flag state at composition root.
   - **Decorator/Proxy** (recommended for adding behavior): Wrap existing service, add behavior when flag ON.
   - Output: Architecture sketch showing the abstraction boundary.

3. **Implement both paths.** Write the flag-ON path and flag-OFF path. Both must compile and pass tests. Never delete the old code path until the flag is removed — the kill switch depends on it.
   - Per-platform considerations in `references/per-platform-patterns.md`.

4. **Write flag-aware tests.** Test both paths independently. Add integration tests that verify: (a) flag OFF → old behavior, (b) flag ON → new behavior, (c) flag toggles at runtime without restart, (d) kill switch works within target latency.
   - See `references/testing-strategies.md` for combinatorial explosion mitigation.

5. **Register the flag with metadata.** Owner, removal date (max 60 days post-100%), rollout plan (5% → 25% → 50% → 100%), kill switch verified, monitoring dashboard linked.
   - Use the flag registration template in `templates/flag-registration.yaml`.

**Completion criteria:** Both code paths implemented and tested, flag registered with full metadata, kill switch verified, removal ticket created and assigned.

### Mode 3: Diagnose Flag Problems

**Trigger:** "The feature flag isn't working as expected" or "Flag state is inconsistent across services."

**Process:**

1. **Trace evaluation path.** Identify where the flag is evaluated: client-side (mobile/web), server-side (backend), or edge (CDN, API gateway). Check evaluation latency and caching.
2. **Check flag state propagation.** Server-side flags evaluate immediately. Mobile flags may be cached for hours or days. Web flags depend on CDN cache and polling interval.
3. **Verify target rules.** Check that the user/device/session matches the targeting rules. Verify default rule when no targeting matches.
4. **Inspect flag across environments.** Dev, staging, production may have different flag configurations. Verify environment-specific settings.
5. **Check for flag interaction bugs.** Two flags that interact may produce unexpected behavior when combined. Use pairwise testing to narrow down interactions.

---

## Flag Type Taxonomy

| Type | Purpose | Lifetime | Default | Example |
|------|---------|----------|---------|---------|
| **Release Toggle** | Ship code dark, enable later | Temporary (≤60 days post-100%) | OFF | `checkout.new_flow.v2` |
| **Experiment Toggle** | A/B test | Temporary (≤experiment duration + 14 days) | Control bucket | `checkout.button_color_test` |
| **Ops Toggle** | Kill switch, circuit breaker | Permanent (operational necessity) | ON (feature works) | `checkout.payment_provider_fallback` |
| **Permission Toggle** | Premium feature, beta access | Permanent (product feature) | OFF (not granted) | `checkout.express_checkout_premium` |

**Release toggles are the only type that MUST be temporary.** Ops and permission toggles are permanent but must be tested for both states regularly.

---

## Per-Platform Flag Architecture

| Platform | Evaluation Point | Latency | Offline Behavior | SDK Candidates |
|----------|-----------------|---------|------------------|----------------|
| **Backend (Go/Node/Python/Java)** | Server-side, per-request | < 10ms (local cache) | N/A (always online) | LaunchDarkly, Flagsmith, Unleash, OpenFeature |
| **Web (React/Vue/Svelte)** | Client-side via CDN or SSR | < 50ms (CDN edge) | Stale flag state from last fetch | LaunchDarkly, Flagsmith, GrowthBook, PostHog |
| **iOS (Swift/SwiftUI)** | Firebase Remote Config or SDK | < 100ms (local cache) | Last-fetched flag state (may be days old) | Firebase Remote Config, LaunchDarkly, Flagsmith |
| **Android (Kotlin/Compose)** | Firebase Remote Config or SDK | < 100ms (local cache) | Last-fetched flag state | Firebase Remote Config (12h default cache), LaunchDarkly |
| **Desktop (Electron/Tauri/Native)** | Client-side SDK or remote config | < 50ms (local cache) | Last-fetched; no store review delay | LaunchDarkly, Flagsmith, homegrown |

**Mobile-specific:** Firebase Remote Config has a 12-hour default cache. Force fetch on app launch if flags are time-sensitive, but respect rate limits. App store review means flags can't be updated for 1-14 days — design default values that are safe for the entire review window.

---

## Verification Guardrails

### Before Merging Flag Code
1. **Both paths tested.** At least one test for flag=ON, one for flag=OFF, one for flag transition.
2. **Kill switch verified.** Disable flag in test environment → verify old code path activates within target latency.
3. **Default value documented.** What happens when the flag SDK is unreachable, uninitialized, or returns an error?
4. **Removal ticket created.** Ticket linked to flag registration, assigned to flag owner, deadline set.
5. **Flag registered.** Metadata complete: owner, type, removal date, rollout plan, monitoring link.

### Before Rolling Out a Flag
1. **Rollback plan tested.** Kill switch drill completed in staging.
2. **Monitoring dashboard ready.** Error rate, latency, and business metrics for both flag states.
3. **Both paths healthy.** Flag=ON and flag=OFF code paths verified in production-like load test.
4. **Removal date locked.** No later than 60 days from today.

### At Flag Removal (Flag Cleanup)
1. **Old code path fully deleted.** Not commented out, not behind another flag — deleted.
2. **Tests updated.** Old-path tests removed or merged into new-path tests.
3. **Flag registration deleted.** Remove from flag registry.
4. **Removal ticket closed.** Verify that all references to the flag are gone from code, config, and documentation.
5. **Deploy and verify.** Deploy the cleanup, verify no flag references remain in production.

---

## Failure Modes and Their Costs

| Failure Mode | Root Cause | Prevention |
|-------------|-----------|------------|
| Kill switch fails because old code path rotted | Flag at 100% for 6+ months; old path refactored away | CI fails on stale flags; both paths tested weekly |
| Mobile flag update takes 14 days (app store review) | Flag default set to unsafe value; no review-window buffer | Default must be safe for 14-day stale window |
| Combinatorial explosion: 10 flags = 1024 test scenarios | No pairwise testing; no interaction analysis | Pairwise testing (t-way); flag interaction budget |
| Flag SDK outage takes down app | Blocking flag evaluation at startup; no timeout | Non-blocking evaluation with safe default; circuit breaker on SDK |
| Wrong flag state in production | Environment-specific flag config mismatch | Flag config as code; same deployment pipeline as application code |
| Flag removal breaks because tests only tested flag=ON | "Flag is always ON in production, why test OFF?" | CI gate: both states tested before merge |

---

## Proactive Triggers

Detect these patterns in code and auto-route to this skill:

| Trigger | Pattern | Action |
|---------|---------|--------|
| Raw feature flag evaluation scattered across codebase | `grep -rn "isEnabled\|featureFlag\|FEATURE_" --include="*.ts" --include="*.go"` — more than 5 unique flag names across 3+ files | Propose flag abstraction layer: single evaluation point, typed flag interface |
| Flags at 100% with no removal tickets | `grep -rn "rollout.*100\|percentage.*100"` in flag config | CI gate: stale flag detection; removal sprint allocation |
| Untested flag branches | Coverage gap on `if (flag.isEnabled)` blocks | Both-state test requirement; flag-aware test generation |
| Mobile flags with server-only default values | `grep -rn "defaultValue\|fallback"` in mobile flag config — default references something that requires network | Unsafe default detection; offline-safe default requirement |
| Same flag name in multiple services without coordination | Flag registry: duplicate flag names across service boundaries | Cross-service flag coordination; flag namespace conventions |
| Environment-specific flag config drift | Flag values differ between staging and production beyond intentional rollout % | Flag config as code; drift detection in CI |

---

## Cross-Skill Coordination

| Skill | Relationship | Coordination |
|-------|-------------|--------------|
| `release-manager` | Consumes from | Ops-level flag lifecycle, release calendars, go/no-go frameworks. Our flag metadata feeds their release checklists. |
| `shipping-and-launch` | Consumes from | Launch-day monitoring, staged rollout sequences. Our flag evaluation architecture feeds their rollout dashboards. |
| `ci-cd-builder` | Consumes from | CI enforcement of flag policies (stale flag detection, both-state test gating). We define the checks; they implement them. |
| `mobile-developer` | Feeds into | Per-platform flag implementation for mobile. Firebase Remote Config caching, offline defaults, store review window. |
| `android-developer` | Feeds into | Android-specific: Firebase Remote Config (12h cache), in-app updates for flag fetch, Play Store review bypass patterns. |
| `ios-developer` | Feeds into | iOS-specific: Firebase Remote Config, App Store review window, `NSUserActivity` integration for Handoff flags. |
| `frontend-developer` | Feeds into | Web-specific: SSR+client flag hydration, CDN caching, no-flash-of-old-UI patterns. |
| `backend-developer` | Feeds into | Server-side evaluation, per-request flag resolution, flag-aware database migrations. |
| `qa-engineer` | Feeds into | Flag-aware test strategy: pairwise testing, both-state test generation, flag transition testing. |
| `ab-testing-specialist` | Feeds into | Experiment flag design, statistical validity of flag-based experiments, sample size integration. |

---

## Toolbox

### Flag Evaluation Decision Tree

```
New flag needed?
├── Will this flag exist for more than 60 days?
│   ├── Yes → Is it a kill switch?
│   │   ├── Yes → OPS TOGGLE (permanent, always test both paths)
│   │   └── No → PERMISSION TOGGLE (permanent, gate access)
│   └── No → Is this for an A/B test?
│       ├── Yes → EXPERIMENT TOGGLE (temporary, remove after experiment)
│       └── No → RELEASE TOGGLE (temporary, remove within 60 days of 100%)
└── All toggles require: owner, removal date, kill switch, monitoring dashboard
```

### SDK Evaluation Trade-offs (Quick Reference)

| Factor | LaunchDarkly | Flagsmith | Unleash | Firebase Remote Config | OpenFeature |
|--------|-------------|-----------|---------|------------------------|-------------|
| Self-hosted | No (SaaS only) | Yes (open-source) | Yes (open-source) | No (Google SaaS) | N/A (abstraction layer) |
| Mobile SDK quality | Excellent | Good | Limited | Excellent (Android/iOS native) | Depends on provider |
| Offline support | Yes (mobile) | Yes | Limited | Yes (built-in) | Depends on provider |
| Real-time updates | Streaming (< 200ms) | Polling/SSE | Polling | Fetch (12h default cache) | Depends on provider |
| Targeting rules | Rich (custom attributes, segments) | Good | Good | Limited (user properties, app version) | Minimum-viable (spec-defined) |
| Pricing | Enterprise ($) | Free (OSS) / Paid cloud | Free (OSS) / Paid cloud | Free (with limits) | Free (OSS) |
| Best for | Enterprises, multi-platform | Startups, open-source-first | Self-hosted requirement | Mobile apps, Google ecosystem | Vendor independence |
