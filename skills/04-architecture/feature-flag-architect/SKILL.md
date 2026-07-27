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

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

**Architect, implement, and maintain feature flag systems from a developer's perspective.** This skill bridges the gap between the operations-focused flag management in `release-manager` and `shipping-and-launch` and the day-to-day development concerns of flag-driven development, SDK integration, testing, and flag debt elimination.

---
<!-- QUICK: 30s -->

## Anti-Hallucination
<!-- STANDARD: 3min -->

* Admit uncertainty. If you cannot determine the correct approach, ask — do not guess.
* Flag your knowledge cutoff. If this project uses tools or patterns you have not seen, state your assumptions.
* Never guess security. If work touches auth, payments, or PII, route to security-reviewer.
* [VERIFIED] before any production guidance: Verify assumptions. Verify compatibility. Verify correctness.

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

**G1: Never deploy without a kill switch for every new feature.** Every feature that ships behind a flag must have a runtime kill switch — no deploy required to disable. If a flag's kill switch requires a deploy, the architecture is broken.

**G2: Flags are code paths, not configuration flags.** Treat every branch guarded by a feature flag as a production code path that needs full test coverage. Both branches (flag ON, flag OFF) must be tested independently before the flag reaches any environment beyond development.

**G3: The testing matrix grows exponentially with flags.** N binary flags = 2^N combinations. Without mitigation, 5 flags = 32 test scenarios. Apply pairwise testing, test at flag boundaries, and never combine untested flag states in production. At the first sign of combinatorial explosion, stop and reduce the flag interaction surface.

**G4: Flag removal is not technical debt cleanup — it's a feature.** Flag removal tickets must be created at flag creation, assigned to the flag owner with a hard deadline (60 days post-100% rollout). CI must fail if a flag at 100% for > 30 days has an open removal ticket.

**G5: Mobile apps have one flag evaluation per app launch against the store.** Unlike web/backend, mobile flags can't be updated instantly — app store review creates a 1-14 day delay. Design for stale flag states. Every mobile flag must have a default value that is safe for the entire review window.

**G6: Log every flag evaluation with trace context.** Every flag evaluation must produce a structured log line containing `flag_name`, `evaluation_result`, `evaluation_reason` (targeting match, default, override, error), `correlation_id`, and `evaluation_latency_ms`. Without these logs, flag-related incidents become undebuggable — you can't answer "who saw what and when" during a kill-switch event. Use the SDK's built-in evaluation logger; never hand-roll.

**G7: Flag context must never contain PII, credentials, or secrets.** Flag evaluation context (user attributes, targeting rules, custom properties) flows through the flag evaluation pipeline and appears in debug logs, audit trails, and analytics exports. Never pass `email`, `phone`, `password`, `token`, `ssn`, `credit_card`, `full_name`, or `date_of_birth` as flag context attributes. Use opaque identifiers (`user_id`, `session_id`) and derive targeting attributes server-side. A flag context with `{"email": "user@example.com"}` will end up in Datadog, Segment, and every analytics warehouse.

**G8: Debug flag resolution locally before any environment promotion.** Every flag must be debuggable in a local environment with the exact same evaluation logic as production. The flag SDK's local evaluation mode (offline mode, local override file) is mandatory — if you can't reproduce a flag state on your machine, you can't debug a production incident. Run through all targeting rules locally before opening a PR.

---

## The Expert's Mindset
<!-- STANDARD: 3min -->

### Mental Models

1. **The Flag is a Temporary Fork.** A feature flag is a code fork with a known merge date. Treat it like a feature branch: the longer it lives, the more painful the merge. The merge IS the flag removal — schedule it.

2. **Two Truths, One Flag.** At any moment, the flag evaluates to exactly one state. But the code must maintain two divergent realities until the flag is removed. Both realities must compile, pass tests, and be safe in production.

3. **Flags Don't Retire Themselves.** No flag ever removed itself. The only force that removes flags is a developer writing a PR. Automate the pressure to remove them: CI failures, sprint-level reminders, flag-age dashboards.

4. **The Store is an Adversary.** Mobile app stores inject 1-14 days of flag evaluation lag. A flag disabled on the server can remain active on 100,000 installed apps for two weeks. Design for the worst-case lag.

5. **Every Flag Creates a Dependency.** When service A checks flag X and service B checks flag X, they become coupled through the flag state. A flag toggle can create distributed consistency problems that didn't exist before.

### Cognitive Biases to Guard Against

| Bias | Manifestation | Antidote | Mechanical Trigger (detect before executing) | Violation Response |
|------|---------------|----------|---|
| **Temporary Thing Permanence** | "We'll remove this flag next sprint" → flag survives 18 months | Removal ticket created with flag creation, hard deadline | | |

| **Happy Path Blindness** | Testing only flag=ON, assuming flag=OFF "just works" | CI requires both paths tested before merge | | |

| **Flag Proliferation Drift** | "One more flag won't hurt" → 47 flags, untestable matrix | Flag budget per service; new flag requires retiring an old one | | |

| **Store Optimism** | "Users always update their apps" → 30% on version from 18 months ago | Design for the installed base, not the latest release | | |

| **Kill Switch Complacency** | "We've never needed the kill switch" → kill switch rots, fails when needed | Quarterly kill-switch drills in production | | |

| **Copy-Paste Flag Pattern** | Copied flag wiring from service A to service B without adapting evaluation context | Flag context is service-specific; always review evaluation point | | |

--- | |

## Operating at Different Levels
<!-- STANDARD: 3min -->

| Level | Scope | Autonomy | Key Capability |
|-------|-------|----------|----------------|
| **L1: Flag Consumer** | Uses flags created by others; adds `if (flag.isEnabled("checkout_v2"))` | Follows team flag conventions | Reads flag evaluation docs; adds flags to code following existing patterns |
| **L2: Flag Implementer** | Designs flags for a single service; manages flag lifecycle for owned features | Independently creates and cleans up flags | Chooses flag type (release/experiment/ops/permission); writes flag-aware tests; removes flags on schedule |
| **L3: Flag Architect** | Designs flag systems for a platform; selects SDKs; defines flag conventions across teams | Makes SDK decisions; sets flag policies | SDK evaluation and selection; flag type taxonomy; cross-service flag coordination; CI enforcement |
| **L4: Organizational Flag Strategist** | Multi-platform flag strategy; flag governance across 50+ services; flag cost modeling | Sets org-wide flag policies | Flag budget allocation; multi-platform flag SDK unification; flag-driven development workflow design; flag cost attribution |
| **L5: Industry Flag Thought Leader** | Advances flag technology; contributes to OpenFeature spec; invents flag patterns | Defines industry best practices | OpenFeature contribution; flag safety proofs; flag-driven architecture patterns for previously unsolved problems |

---

## Decision Trees
<!-- STANDARD: 3min -->

**(QUICK)**

### Decision Tree 1: How Do I Choose a Flag Type?

        ┌── INPUT: New feature needs flagging
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
Release toggle     Experiment flag    Operational
(trunk-based dev)  (A/B test)         (kill switch)
   │                 │                  │
   ▼                 ▼                  ▼
Short-lived;        Medium-lived;      Long-lived;
remove within       remove after       permanent;
2 sprints;          experiment         control infra
branch by           concludes;         behavior; rarely
abstraction         track metrics      removed
   │                 │                  │
   ▼                 ▼                  ▼
Lifespan: days      Lifespan: weeks    Lifespan: months
to weeks            to months          to permanent

### Decision Tree 2: How Do I Select a Feature Flag SDK?

        ┌── INPUT: Platform and requirements for flags
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
Need instant        Need offline        Self-hosted
flag updates        flag evaluation     required
(mobile apps)       (no network)        (compliance)
   │                 │                  │
   ▼                 ▼                  ▼
LaunchDarkly/       Firebase Remote     Unleash/
Flagsmith with      Config or local     Flagsmith
streaming or SSE    config with         self-hosted
   │                 │                  │
   ▼                 ▼                  ▼
Cost: $$ per MAU    Cost: $ or free     Cost: infra ops

### Decision Tree 3: How Do I Manage Flag Technical Debt?

        ┌── INPUT: Flag inventory has grown; need cleanup
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
Flag >90 days       Flag has 0%        Flag controls
since rollout       traffic in         deprecated code
completed           production         path
   │                 │                  │
   ▼                 ▼                  ▼
Schedule removal    Remove ASAP;       Remove flag AND
in current sprint;  flag has been      dead code path;
automate expiry     dead for weeks     don't leave stubs
   │                 │                  │
   ▼                 ▼                  ▼
Add expiry date     Auto-cleanup CI    Full removal:
to flag config;     job that flags     flag definition +
CI warns on         zero-traffic       all conditional
expired flags       flags weekly       branches

## Core Workflow
<!-- STANDARD: 3min -->

### Mode 1: Design a Feature Flag System

**Trigger:** "I need to add feature flags to our [platform] app" or "Which feature flag SDK should we use?"

**Process:**

1. **Assess the platform and requirements.** Determine: target platforms (mobile, web, backend, desktop), evaluation latency requirements, offline behavior needs, team size, compliance constraints, budget.
   * Output: Platform Matrix showing flag evaluation points and constraints per platform.

2. **Classify flag types needed.** Release toggles (temporary), experiment toggles (A/B test), ops toggles (kill switches, circuit breakers), permission toggles (premium features, beta access).
   * Output: Flag Type Map matching each planned flag to its type and lifecycle.

3. **Select evaluation architecture.** Choose between: server-side evaluation (backend, zero client latency), client-side evaluation (mobile/web, works offline), or hybrid (evaluate server-side, sync to client).
   * Output: Evaluation Architecture Diagram per platform.

4. **Evaluate SDKs against requirements.** Matrix: LaunchDarkly (enterprise, multi-platform), Flagsmith (open-source option), Unleash (self-hosted), Firebase Remote Config (mobile-first, free), OpenFeature (vendor-neutral abstraction), homegrown (full control, high maintenance).
   * Output: SDK Recommendation with trade-off analysis.

5. **Define flag conventions.** Naming: `[team].[feature].[variant]` (e.g., `checkout.new_flow.v2`). Default values: OFF for release toggles, control for experiments, ON for ops toggles. Expiry: max 60 days post-100% for release toggles.
   * Output: Flag Convention Guide for all teams.

6. **Build the flag cleanup pipeline.** CI checks: (a) flag at 100% > 30 days with open removal ticket → CI FAIL, (b) flag referenced in code but not in flag registry → CI WARN, (c) flag in registry but never evaluated → CI WARN.
   * Output: CI configuration and removal workflow.

**Completion criteria:** SDK recommendation delivered with trade-off matrix, flag conventions documented, CI enforcement configured, removal workflow tested with a dummy flag.

### Mode 2: Implement Feature Flags in Code

**Trigger:** "I need to add a feature flag for [feature]" or "Help me wrap this new feature behind a flag."

**Process:**

1. **Identify flag type.** Release toggle (temporary, removed after rollout), experiment toggle (A/B, removed after experiment ends), ops toggle (permanent, kill switch), permission toggle (permanent, gated access).
   * Decision: Use the type that matches the flag's purpose and expected lifetime.

2. **Choose the abstraction pattern.**
   * **Branching by Abstraction** (recommended for new features): Create interface/strategy, implement old and new, select via flag.
   * **Simple If/Else** (acceptable for small changes): `if (flags.isEnabled("checkout_v2")) { ... } else { ... }`.
   * **Dependency Injection** (recommended for DI frameworks): Bind implementation based on flag state at composition root.
   * **Decorator/Proxy** (recommended for adding behavior): Wrap existing service, add behavior when flag ON.
   * Output: Architecture sketch showing the abstraction boundary.

3. **Implement both paths.** Write the flag-ON path and flag-OFF path. Both must compile and pass tests. Never delete the old code path until the flag is removed — the kill switch depends on it.
   * Per-platform considerations in `references/per-platform-patterns.md`.

4. **Write flag-aware tests.** Test both paths independently. Add integration tests that verify: (a) flag OFF → old behavior, (b) flag ON → new behavior, (c) flag toggles at runtime without restart, (d) kill switch works within target latency.
   * See `references/testing-strategies.md` for combinatorial explosion mitigation.

5. **Register the flag with metadata.** Owner, removal date (max 60 days post-100%), rollout plan (5% → 25% → 50% → 100%), kill switch verified, monitoring dashboard linked.
   * Use the flag registration template in `templates/flag-registration.yaml`.

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
<!-- STANDARD: 3min -->

| Type | Purpose | Lifetime | Default | Example |
|------|---------|----------|---------|---------|
| **Release Toggle** | Ship code dark, enable later | Temporary (≤60 days post-100%) | OFF | `checkout.new_flow.v2` |
| **Experiment Toggle** | A/B test | Temporary (≤experiment duration + 14 days) | Control bucket | `checkout.button_color_test` |
| **Ops Toggle** | Kill switch, circuit breaker | Permanent (operational necessity) | ON (feature works) | `checkout.payment_provider_fallback` |
| **Permission Toggle** | Premium feature, beta access | Permanent (product feature) | OFF (not granted) | `checkout.express_checkout_premium` |

**Release toggles are the only type that MUST be temporary.** Ops and permission toggles are permanent but must be tested for both states regularly.

---

## Per-Platform Flag Architecture
<!-- STANDARD: 3min -->

| Platform | Evaluation Point | Latency | Offline Behavior | SDK Candidates |
|----------|-----------------|---------|------------------|----------------|
| **Backend (Go/Node/Python/Java)** | Server-side, per-request | < 10ms (local cache) | N/A (always online) | LaunchDarkly, Flagsmith, Unleash, OpenFeature |
| **Web (React/Vue/Svelte)** | Client-side via CDN or SSR | < 50ms (CDN edge) | Stale flag state from last fetch | LaunchDarkly, Flagsmith, GrowthBook, PostHog |
| **iOS (Swift/SwiftUI)** | Firebase Remote Config or SDK | < 100ms (local cache) | Last-fetched flag state (may be days old) | Firebase Remote Config, LaunchDarkly, Flagsmith |
| **Android (Kotlin/Compose)** | Firebase Remote Config or SDK | < 100ms (local cache) | Last-fetched flag state | Firebase Remote Config (12h default cache), LaunchDarkly |
| **Desktop (Electron/Tauri/Native)** | Client-side SDK or remote config | < 50ms (local cache) | Last-fetched; no store review delay | LaunchDarkly, Flagsmith, homegrown |

**Mobile-specific:** Firebase Remote Config has a 12-hour default cache. Force fetch on app launch if flags are time-sensitive, but respect rate limits. App store review means flags can't be updated for 1-14 days — design default values that are safe for the entire review window.

---

## Best Practices
<!-- STANDARD: 3min -->

1. **Do create a flag removal ticket at the moment of flag creation** — Every feature flag must have a planned death. Assign removal to the flag owner with a hard deadline of 60 days post-100% rollout. Configure CI to fail if any flag at 100% rollout for >30 days still has an open removal ticket. Flags that outlive their purpose become zombie code paths — the old code rots, tests bit-rot, and when the flag is finally removed, it causes an incident nobody remembers how to fix. Each zombie flag costs $2K-$10K in incident response when it eventually breaks.
2. **Prefer flag configuration as code over runtime admin UI toggles** — Flag config stored in the same repo and deployment pipeline as application code ensures atomic rollouts where flag state matches deployed code. Admin UI toggles create split-brain states: the code deploys expecting one flag state, but the toggle changes independently through a different path. Storing flags as code with environment-specific overrides in version control eliminates the "flag was toggled but code hadn't deployed" class of production incidents.
3. **Always implement a kill switch as an emergency brake, not just a feature toggle** — A kill switch must disable the feature at runtime without requiring a deploy. If turning a flag off takes a full CI/CD pipeline cycle (15-30 minutes), you've built a feature toggle, not a kill switch. During a production incident with 1,000 requests/second, a 30-minute deploy cycle for a kill switch means 1.8 million requests hitting the broken code path. The cost difference between toggle and kill switch is measured in outage duration.
4. **Never put PII, credentials, or secrets in flag evaluation context** — Flag context attributes flow through the SDK evaluation pipeline and appear in debug logs, audit trails, analytics exports, and monitoring dashboards. An email or phone number in flag context will surface in Datadog, Segment, and every data warehouse. One PII leak via flag context triggers GDPR/CCPA notification obligations — fines start at $2,500 per violation under CCPA and can reach 4% of global revenue under GDPR for systematic exposure.
5. **Measure flag debt score as a continuous health metric** — Track (flags at 100% rollout for >30 days) / (total active flags). Target: 0. A non-zero flag debt score means zombie flags are accumulating. Each zombie adds 2^n complexity to the test matrix (where n is zombie count) and creates an incident vector that compounds over time. Flag debt is like credit card debt: 5 zombie flags today become 10 next quarter if cleanup discipline slips even once. Set a dashboard alert when score exceeds 0.

## Production Checklist
<!-- STANDARD: 3min -->

Before deploying or delivering work from this skill, verify:

| # | Check | Verify |
|---|-------|--------|
| ☐ | Every flag has both ON and OFF code paths tested independently: at least one test per path per flag; both paths covered before flag reaches staging | `grep -c "flag.*=.*true\|flag.*=.*false"` in test files confirms every flag name appears in both ON and OFF test scenarios |
| ☐ | Kill switch verified in staging: toggling flag OFF restores old code path within target latency SLA with zero errors in logs | Toggle flag OFF while monitoring production-like traffic in staging → old path activates within SLA; error rate remains at baseline |
| ☐ | Default flag values safe for all failure modes: SDK unreachable, uninitialized SDK, or SDK returning error — app continues without crash | Simulate SDK outage by blocking flag evaluation endpoint → verify app operates with documented defaults; no feature gates on unavailable flags |
| ☐ | Flag removal ticket created at flag creation: linked to flag registration, assigned to owner, hard deadline ≤60 days post-100% rollout | Verify ticket exists in issue tracker; CI fails if flag at 100% >30 days with open removal ticket (per Ground Rule G4 enforcement) |
| ☐ | Every flag evaluation logged with all required fields: flag_name, evaluation_result, evaluation_reason, correlation_id, evaluation_latency_ms | Inspect structured logs from a flag evaluation call; all 5 fields present, populated, and queryable in log aggregation system |
| ☐ | Flag context verified PII-free: zero email, phone, token, SSN, credit_card, full_name, or date_of_birth in any flag context attribute | Scan/grep flag evaluation codebase → context attributes are only opaque identifiers (user_id, session_id) and server-side derived attributes |
| ☐ | Mobile flags safe for app store review window: default values handle 14-day flag fetch staleness; no core functionality gated on real-time flag updates | Verify all mobile flag defaults produce fully functional app behavior when flag service is unreachable for 14 days |
| ☐ | Rollback plan is documented and tested | Kill switch verified in staging within last 30 days; all flag owners identified with contact info in runbook; flag removal cleanup verified to leave zero code/config/documentation references |

## Verification
<!-- STANDARD: 3min -->

| # | Complete when... | Verify |
|---|---|---|
| ☐ | Complete when every feature flag has both ON and OFF code paths tested independently with at least one test per path | Verify via `grep -c "flag.*=.*true\|flag.*=.*false"` in test files; every flag name must appear in both ON and OFF test scenarios |
| ☐ | Complete when kill switch is verified in test environment — disabling the flag restores old code path within target latency (typically < 100ms) | Verify by toggling flag OFF in test environment while monitoring traffic; old path must activate within latency SLA without errors |
| ☐ | Complete when default flag value is documented and safe for all scenarios: SDK unreachable, uninitialized, or returning an error | Verify default value documentation exists; simulate SDK outage → app must continue with documented default without crashing or blocking |
| ☐ | Complete when flag removal ticket is created at flag creation, linked to flag registration, assigned to owner, with hard deadline ≤ 60 days post-100% rollout | Verify ticket exists in issue tracker; check that CI fails if flag at 100% for > 30 days has open removal ticket (Ground Rule G4) |
| ☐ | Complete when every flag evaluation produces a structured log containing: flag_name, evaluation_result, evaluation_reason, correlation_id, evaluation_latency_ms | Verify by inspecting structured logs from a flag evaluation call; all five fields must be present and populated |
| ☐ | Complete when flag context never contains PII, credentials, or secrets — only opaque identifiers (user_id, session_id) and derived server-side attributes | Verify via grep/scan of flag evaluation code; no email, phone, token, SSN, credit_card, full_name, or date_of_birth in context attributes |
| ☐ | Complete when mobile flags have default values safe for the entire app store review window (1-14 days) with no dependency on real-time flag updates | Verify default value logic handles 14-day staleness; app must remain fully functional with all safe defaults — no feature gates on un-fetchable flags |
| ☐ | Complete when combinatorial explosion is mitigated: for N flags, test matrix uses pairwise testing rather than 2^N exhaustive; flag interaction budget is declared | Verify test plan uses pairwise/t-way strategy; if flags > 5, confirm that interaction analysis has identified dependent flag pairs |
| ☐ | Complete when flag config is stored as code (in the same repo and deployment pipeline as application code) with environment-specific overrides tracked in version control | Verify flag configuration files exist in repo; deployment pipeline applies flag config atomically with application code deploy |
| ☐ | Complete when flag cleanup removes the old code path entirely (not commented out, not behind another flag), deletes flag registration, and closes the removal ticket | Verify via `grep -r "FLAG_NAME"` that zero references remain in code, config, or documentation after cleanup deploy |

## Verification Guardrails
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

| Failure Mode | Root Cause | Prevention |
|-------------|-----------|------------|
| Kill switch fails because old code path rotted | Flag at 100% for 6+ months; old path refactored away | CI fails on stale flags; both paths tested weekly |
| Mobile flag update takes 14 days (app store review) | Flag default set to unsafe value; no review-window buffer | Default must be safe for 14-day stale window |
| Combinatorial explosion: 10 flags = 1024 test scenarios | No pairwise testing; no interaction analysis | Pairwise testing (t-way); flag interaction budget |
| Flag SDK outage takes down app | Blocking flag evaluation at startup; no timeout | Non-blocking evaluation with safe default; circuit breaker on SDK |
| Wrong flag state in production | Environment-specific flag config mismatch | Flag config as code; same deployment pipeline as application code |
| Flag removal breaks because tests only tested flag=ON | "Flag is always ON in production, why test OFF?" | CI gate: both states tested before merge |
| PII in flag evaluation context leaks to logging/analytics | `user_context = {"email": user.email, "plan": user.plan}` passed to flag SDK | Never pass PII in flag context. Use `user_id` + server-side derived attributes. Audit flag context with `grep -rE 'email\|phone\|name\|dob\|ssn\|token'` |
| Flag state undebuggable in production incident | No structured flag evaluation logs; no correlation ID | G6: structured logging with `flag_name`, `result`, `reason`, `correlation_id` on every evaluation |

---

## Proactive Triggers
<!-- STANDARD: 3min -->

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

## When to Use
<!-- STANDARD: 3min -->

| Condition | Use This Skill | Use Instead |
|-----------|---------------|-------------|
| Designing a flag evaluation architecture (SDK selection, evaluation context, caching strategy) | feature-flag-architect | N/A — this is the core use case |
| Implementing flag-driven development patterns (branching by abstraction, strategy pattern) | feature-flag-architect | backend-developer (general patterns, not flag-specific) |
| Managing flag technical debt (stale flags, untested branches, flag removal) | feature-flag-architect | code-reviewer (code quality, not flag lifecycle) |
| Coordinating release go/no-go decisions | release-manager | Operations concerns, not flag architecture |
| Setting up launch-day monitoring dashboards | shipping-and-launch | Monitoring setup, not flag design |
| Designing A/B test experiments with statistical rigor | ab-testing-specialist | Experiment design, not flag implementation |
| Selecting between LaunchDarkly, Flagsmith, Unleash, Firebase Remote Config | feature-flag-architect | N/A — SDK evaluation is core competency |

## What Good Looks Like
<!-- STANDARD: 3min -->

A feature flag system that meets this standard: (1) Every flag has an owner, removal date, and kill switch wired to a monitoring dashboard — no orphan flags, (2) Flag evaluation is non-blocking with a safe default and <10ms P99 latency — if the SDK is down, the app still works, (3) Both code paths (flag ON + flag OFF) are tested in CI on every commit — flag=OFF paths don't rot, (4) CI fails if a flag at 100% >30 days has no removal ticket — flags expire automatically, (5) Combinatorial explosion is managed: pairwise testing for interaction, budget of 5 active flags per service, (6) Mobile flags have defaults safe for 14-day app store review staleness — no feature gates on un-fetchable flags, (7) Flag config is code in the same deploy pipeline as application code — no environment drift, (8) Flag evaluation context contains zero PII — no email, name, or phone number passed to flag SDK.

## Deliberate Practice
<!-- STANDARD: 3min -->

1. **Flag removal sprint:** Take a legacy codebase with 50+ flags at 100% for >90 days. For each flag: verify both paths still work (ON and OFF), determine which path is the new permanent behavior, remove the flag and the dead code path, and verify tests pass. Track: flags removed per hour. Target: 10 flags/hour after warmup.

2. **Kill switch fire drill:** Simulate a production incident where a feature behind a flag is corrupting data. You have 60 seconds from alert to kill the flag. Measure: time from alert receipt to flag evaluation returning OFF for all users. Practice with streaming SDKs (LaunchDarkly <200ms), polling SDKs (Unleash <30s), and mobile (Firebase Remote Config — can you beat the 12-hour cache?).

3. **SDK migration exercise:** Migrate a service from one flag provider to another (e.g., LaunchDarkly → OpenFeature + Flagsmith). Keep both running in parallel during migration. Verify: zero flag evaluation errors during migration, zero user-visible impact. Key skill: abstraction layer design that makes provider swaps a configuration change, not a code change.

4. **Combinatorial explosion audit:** Take a codebase with N feature flags (N≥8). Build the full 2^N matrix. Identify all flag pairs that interact (flag A changes behavior that flag B depends on). Implement pairwise testing that covers all interacting pairs. Calculate: test count with exhaustive (2^N) vs pairwise (N²). Document the savings.

5. **Flag evaluation context security review:** Audit 3 production services for PII in flag evaluation context. Search for: email, name, phone, DOB, SSN, token, password in flag context objects. For each violation: redesign the evaluation to use derived attributes (e.g., `user_tier = "enterprise"` instead of `email = "ceo@company.com"`). Verify: after fix, zero PII in flag evaluation logs.

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Feature flag SDK returns 5xx — all flag evaluations fail, app uses defaults | SDK outage or network partition between app and flag service | Verify circuit breaker on SDK client. Check: what is the default when SDK is unreachable? It must be the safe/old behavior. Implement: non-blocking evaluation with timeout (100ms), cached last-known-good state, alert on >1% evaluation failure rate |
| Flag at 100% for 6 months — old code path deleted, kill switch no-ops | Flag removal process didn't verify both paths still exist before declaring flag "done." Dead code elimination removed the fallback | CI gate: before flag removal, test that both states still work. If old code path has been deleted, flag removal is an emergency — re-implement the old path or accept that kill switch is permanently broken |
| Mobile app shows wrong feature state for 12 hours after flag change | Firebase Remote Config default cache is 12 hours. Flag change propagated on server but mobile clients won't fetch for 12 more hours | Set minimum fetch interval based on flag criticality: release toggles = 1 hour, kill switches = real-time (force fetch on app foreground). Implement in-app force refresh mechanism. Default values must be safe for maximum staleness window |
| Flag evaluation returns wrong user segment — enterprise features shown to free users | User attributes used in targeting rules are stale or incorrect. Segment membership computed from cached data | Verify user attribute freshness: when was `user.plan`, `user.team_size`, `user.features` last updated? Implement attribute refresh on login and app foreground. Add debug endpoint: `/debug/flags?user_id=X` shows what flags evaluate to and why |
| Staging and production have different flag configs — feature works in staging, broken in prod | Flag config not deployed atomically with application code. Staging was manually toggled for testing and never reset | Flag config as code in same repo and deployment pipeline. CI gate: compare staging vs production flag config before deploy — any non-rollout differences fail the deploy. Use flag environment synchronization tooling |

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Kill switch rots because old code path deleted while flag was at 100% — the one time you need it, it does nothing | $100K-$2M in extended outage; a bug that could have been killed in 5 seconds takes 2 hours to rollback via full deploy | CI gate: test flag=OFF path on every commit regardless of current rollout %. If flag_OFF test fails → block merge until old path is restored or flag is declared non-reversible |
| Mobile flag defaults set to "show new feature" instead of "show old behavior" — app store review window is 1-14 days of broken behavior | $50K-$500K in forced app store hotfix + 1-14 days of broken production. Emergency app store review costs $0 but the wait costs users | Default must be safe behavior (old path). Assume SDK will be unreachable for 14 days. Test: deploy app with airplane mode ON and verify no broken features. Firebase Remote Config: never use `activate()` with "new" as default |
| Flag SDK evaluated synchronously at app startup with no timeout — SDK outage = app won't start | $200K-$1M in complete app outage; 100% of users can't open app because flag SDK (external dependency) is down | Non-blocking evaluation with timeout (100ms). Cache last-known-good flag state in local storage. Circuit breaker: after 5 consecutive failures, use cache for 5 minutes before retrying |
| PII leaked through flag evaluation context to third-party analytics — user emails in LaunchDarkly audit logs | $500K-$5M in GDPR/CCPA fines; flag evaluation context containing `email`, `name`, `phone` shipped to vendor's servers in another jurisdiction | Audit: `grep -rE 'email|phone|name|dob|ssn|token'` on flag context construction. Use `user_id` + server-side derived attributes only. Never pass raw PII to flag SDK. Add pre-commit hook that blocks PII patterns in flag context files |
| Untested flag=OFF paths rot silently — 6 months of "flag is always ON in prod, why test OFF?" leads to broken kill switches | $50K-$300K in failed kill switch when you need it most; the one safe fallback path crashes because nobody tested it for 6 months | CI requires both states tested on every commit. `test_flag_on()` and `test_flag_off()` must both pass. If flag_OFF test is skipped with `// TODO: test flag off` for >2 weeks, CI blocks merge |
| Combinatorial explosion: 10 feature flags = 1024 test scenarios — test suite takes 8 hours or only tests "all flags ON" | $50K-$200K in untested interactions; 10 flags with untested interactions = 1023 untested production states. One combination crashes | Pairwise testing (t-way) reduces 1024 to ~100 scenarios. Flag interaction budget: max 5 active flags per service. Flag dependency graph: if flag A depends on flag B, declare it — CI tests flagged interactions explicitly |
| Flag removal leaves commented-out code — "just in case we need it back" — 18 months later nobody knows what it does | $10K-$50K in codebase entropy; commented-out flag code accumulates, confuses new developers, and still shows up in full-text search during incident response | Flag removal = delete old code path entirely. No commented-out code, no `// LEGACY: old flag path`. Git history preserves the old code if needed. Removal checklist: delete code, delete flag registration, delete tests, close ticket |
| Flag config drifts between environments — staging has `rollout: 50%`, production has `rollout: 100%` because someone manually toggled | $30K-$150K in staging-prod parity breaks; feature tested at 50% in staging = 50% of test traffic hit different code paths than production | Flag config as code in repo. Deployment pipeline applies config atomically with code. CI gate: `diff staging-flags.json production-flags.json` — only intentional rollout % differences allowed |

## References
<!-- STANDARD: 3min -->

* `references/flag-type-taxonomy.md` — Detailed taxonomy: release toggles, experiment toggles, ops toggles, permission toggles with lifecycle and removal strategy per type
* `references/sdk-comparison-matrix.md` — LaunchDarkly vs Flagsmith vs Unleash vs Firebase Remote Config vs OpenFeature across 15 dimensions
* `references/testing-strategies.md` — Combinatorial testing, pairwise/t-way testing, both-state test patterns, flag transition testing
* `references/mobile-flag-architecture.md` — Per-platform mobile architecture: Firebase Remote Config, offline defaults, store review window, force-refresh patterns
* [LaunchDarkly SDK Documentation](https://docs.launchdarkly.com/sdk) — Official SDK docs for all platforms
* [OpenFeature Specification](https://openfeature.dev/specification/) — Vendor-neutral flag evaluation specification
* [Martin Fowler: Feature Toggles](https://martinfowler.com/articles/feature-toggles.html) — Canonical reference on toggle categories and lifecycle

## Route the Request
<!-- STANDARD: 3min -->

| Request Pattern | Action |
|----------------|--------|
| "Set up a feature flag for my new feature" | Route to feature-flag-architect: design flag type (release/ops/experiment/permission), define owner + removal date + kill switch, implement both paths, add both-state tests |
| "We need to release this feature to 10% of users" | Route to feature-flag-architect + release-manager: architect the rollout flag, coordinate release approval, set up monitoring for the 10% cohort |
| "Can we turn off feature X in production?" | Route to feature-flag-architect: verify kill switch still works (both paths tested recently?), execute kill, verify old path activates, create incident ticket |
| "We have 50+ flags and can't tell which ones are still in use" | Route to feature-flag-architect: flag audit — identify flags at 100% >30 days, flags with untested OFF paths, orphan flags with departed owners, schedule removal sprint |
| "Should we use LaunchDarkly or build our own?" | Route to feature-flag-architect: build-vs-buy analysis with TCO over 3 years, vendor risk assessment, OpenFeature abstraction to preserve optionality |

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Decision | Status | Timestamp |
|----------|--------|-----------|
| (none yet) | — | — |

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

### Upstream (Consumes From)

| Upstream Skill | What We Need | When |
|----------------|-------------|------|
| `release-manager` | Ops-level flag lifecycle, release calendars, go/no-go frameworks | When integrating flags into release pipelines — our flag metadata feeds their checklists |
| `shipping-and-launch` | Launch-day monitoring, staged rollout sequences | When designing rollout flag architecture — their dashboards consume our evaluation data |
| `ci-cd-builder` | CI enforcement of flag policies (stale flag detection, both-state test gating) | When implementing CI flag governance — we define checks, they implement them |

### Downstream (Feeds Into)

| Downstream Skill | What We Provide | When |
|-----------------|----------------|------|
| `mobile-developer` | Per-platform flag implementation guidance for mobile | After flag architecture designed — Firebase Remote Config caching, offline defaults |
| `android-developer` | Android-specific: Firebase Remote Config (12h cache), in-app updates for flag fetch | After mobile flag design — Play Store review bypass patterns |
| `ios-developer` | iOS-specific: Firebase Remote Config, App Store review window | After mobile flag design — `NSUserActivity` integration for Handoff flags |
| `frontend-developer` | Web-specific: SSR+client flag hydration, CDN caching | After flag architecture designed — no-flash-of-old-UI patterns |
| `backend-developer` | Server-side evaluation, per-request flag resolution | After flag architecture designed — flag-aware database migrations |
| `qa-engineer` | Flag-aware test strategy: pairwise testing, both-state test generation | After flag system designed — flag transition testing |
| `ab-testing-specialist` | Experiment flag design, statistical validity guidance | When running experiments — sample size integration with flag-based experiments |

---

## Toolbox
<!-- STANDARD: 3min -->

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
