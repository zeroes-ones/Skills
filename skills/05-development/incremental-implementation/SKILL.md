---
name: incremental-implementation
description: >
  Use when building features incrementally with thin vertical slices instead of big-bang
  delivery; when each slice must be independently shippable and testable; when implementing
  behind feature flags with safe defaults; when every commit must leave the codebase in a
  deployable state; or when migrating from waterfall-style delivery to continuous delivery.
  Handles vertical slice decomposition, feature flag lifecycle management, atomic commit
  discipline, safe default patterns, rollout sequencing, and kill-switch patterns. Do NOT
  use for architecture design (route to system-architect), debugging production issues
  (route to debugging-and-error-recovery), or one-shot prototypes (route to prototype).
license: MIT
tags:
  - incremental-delivery
  - vertical-slices
  - feature-flags
  - continuous-delivery
  - atomic-commits
  - safe-defaults
author: Sandeep Kumar Penchala
type: development
status: stable
version: 1.0.0
updated: 2026-07-27
token_budget: 3500
chain:
  consumes_from:
    - feature-flag-architect
    - ci-cd-builder
    - tdd-guide
    - debugging-and-error-recovery
  feeds_into:
    - shipping-and-launch
    - release-manager
    - qa-engineer
    - observability-engineer
---

# Incremental Implementation

> **Portability target:** Works in Claude Code, Copilot CLI, Cursor, Codex, and Gemini CLI. No agent-specific features required.

## Anti-Hallucination

* Admit uncertainty. If you cannot determine the correct vertical slice boundary, ask — do not guess.
* Flag your knowledge cutoff. If this project uses a feature flag system you have not seen, state your assumptions.
* Never guess security. If a slice touches auth, payments, or PII, recommend routing to security-reviewer.
* [VERIFIED] before any production guidance: Verify flag infrastructure exists. Verify CI/CD passes. Verify backward compatibility.

## Ground Rules

| # | Rule | Mechanical Trigger | Violation Response |
|---|------|-------------------|-------------------|
| 1 | Every commit is deployable. Tests must pass after each commit | Pre-commit hook runs tests. Non-zero exit blocks commit | Reject commit. Fix tests before retrying |
| 2 | No PR merges a partial vertical. Slice goes UI to API to DB to back | PR description must list checked boxes for UI, API, Data, Test layers | Any unchecked box means reject PR |
| 3 | Feature flags wrap all new behavior. Default is OLD behavior | Grep for new function or route name. Must appear inside flag check block | Reject PR. Wrap new code in feature flag check |
| 4 | Kill switches ship with the flag | Flag config must have kill_switch, auto_off_metric, and cleanup_after keys | Reject flag config. Add missing keys |
| 5 | Commit messages name the slice | Commit message lacks feat or fix with slice-name pattern | Reject until amended |

## Route the Request

This is a map, not a recipe. Start at the top and follow the matching branch.

    INCOMING TASK: Build feature X
    |
    +-- Is X large enough to require more than 1 PR?
    |   +-- YES -> DECOMPOSE into vertical slices
    |   +-- NO  -> Is it a HOTFIX?
    |              +-- YES -> Route to debugging-and-error-recovery
    |              +-- NO  -> Single commit, single flag. Ship.
    |
    +-- SLICE DECOMPOSITION
    |   |
    |   +-- Start with: What is the smallest unit of X that is independently useful?
    |   |
    |   +-- Each slice MUST:
    |   |   +-- Change at most 3 files in UI layer
    |   |   +-- Change at most 2 files in API or backend layer
    |   |   +-- Change at most 1 migration or data layer file
    |   |   +-- Add at least 1 test file
    |   |
    |   +-- Slice ordering:
    |   |   +-- VS-0: Scaffold plus feature flag plus no-op route
    |   |   +-- VS-1: Happy path with minimum viable data
    |   |   +-- VS-2: Edge case handling: errors, empty states, validation
    |   |   +-- VS-3: Integration: connects X to other systems
    |   |   +-- VS-N: Polish: performance, accessibility, analytics
    |   |
    |   +-- Each VS has its own feature flag
    |
    +-- Do you have feature flag infrastructure?
    |   +-- NO  -> Route to feature-flag-architect FIRST
    |   +-- YES -> Proceed
    |
    +-- Is X touching a payment, auth, or compliance path?
        +-- YES -> Route to security-reviewer first
        +-- NO  -> Start building

## When to Use

* Building a feature that requires more than one PR to complete
* Migrating from big-bang releases to continuous delivery
* Working in a codebase where broken commits block the entire team
* Introducing new behavior that must be gated behind configuration
* Reducing deployment risk through incremental rollout
* Coordinating multi-service feature delivery

> If you catch yourself rationalizing, stop. The rationalizations below are traps.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| It is faster to build the whole thing at once | Partial slices reveal integration problems on day 1, not month 3 |
| Feature flags add complexity we do not need | Feature flags are the cheapest insurance policy against bad deploys |
| I will make it atomic later once it works | Non-atomic commits are irreversible technical debt |
| We can skip the slice if it is trivial | Forty percent of trivial slices hide a dependency trap |
| Safe defaults are for production, not dev | Without practice in dev, safe defaults will be forgotten in production |

## The Expert's Mindset

1. **Slices, not layers.** Build a thin piece of every layer, not a complete backend before frontend. This is the most important mental shift from waterfall to incremental.
2. **Flags are surgical instruments.** Each has a lifecycle: zero percent to ten percent to fifty percent to one hundred percent to flag removal. Track lifecycle in a dashboard.
3. **Safe defaults eliminate rollbacks.** A bad deploy with default equals OFF is not a rollback — it is a config change. Thirty-minute rollbacks become thirty-second config toggles.
4. **Atomic commits make blame useful.** When git bisect lands on your commit, it should tell a complete story: one slice, one flag, one test.

## Operating at Different Levels

### Level 1: Quick (Single Slice)
- Decompose into VS-0 through VS-3 using the template below
- Create the feature flag config file
- Commit VS-0: scaffold plus flag plus passing test
- Push and open draft PR with remaining slices as TODOs
- **Complete when:** VS-0 merged, flag at zero percent, CI passes, team acknowledges workflow

### Level 2: Standard (Multi-Slice Feature)
- Run full decomposition with file-level estimates
- Create feature flag lifecycle dashboard entry
- Implement VS-0 through VS-2 as separate PRs
- Run qa-engineer for cross-slice integration tests
- Incremental flag rollout: zero to one to ten to fifty to one hundred percent
- Remove each flag after seven days at one hundred percent
- **Complete when:** All slices merged, all flags at one hundred percent, cleanup scheduled

### Level 3: Deep (Team-Wide Rollout)
- Run brainstorming to validate slice decomposition with stakeholders
- Design flag lifecycle tooling with dashboard, auto-off metrics, cleanup automation
- Write runbook for canary analysis per slice
- Run observability-engineer to instrument per-flag metrics
- Run release-manager for multi-service flag coordination
- Schedule flag removal sprints every two weeks
- **Complete when:** Automation in place, runbooks tested, team trained, dashboards operational

### Level 4: Exploration (Brownfield Migration)
- Run brownfield-adoption-planner to select monolith extraction targets
- Apply Strangler Fig pattern: new behavior to slice, old behavior to monolith
- Run code-simplification on each extracted slice
- **Complete when:** First monolith slice extracted and running in production

## Core Workflow

### Phase 1: Decompose into Vertical Slices

| Slice | Description | Files Changed | LoC | Test File | Flag |
|-------|-------------|---------------|-----|-----------|------|
| VS-0  | Empty route plus flag scaffold | routes.ts, flags.yaml | ~15 | vs0.test.ts | feature_x_vs0 |
| VS-1  | Happy path: create resource | handler.ts, model.ts, migration | ~80 | vs1.test.ts | feature_x_vs1 |
| VS-2  | Error handling: validation, 422, 404 | handler.ts, errors.ts | ~40 | vs2.test.ts | feature_x_vs2 |
| VS-3  | Integration: webhook to service Y | client.ts, webhook.ts | ~60 | vs3.test.ts | feature_x_vs3 |

**Slice sizing rules:** VS-0 at most thirty lines. VS-1 through VS-N at most one hundred lines each.

### Phase 2: Implement in Sequence

1. Checkout fresh branch: git checkout -b feat/x-vs0
2. Create flag in flags.yaml with default: false, kill_switch: true
3. Wrap new code behind flag: if flags.isEnabled feature_x_vs0 then new else old
4. Write tests covering both ON and OFF states
5. Commit: feat x-vs0 scaffold route and feature flag
6. Push and open PR with layer checkmarks

### Phase 3: Ship and Monitor

1. Merge VS-0 at zero percent — no users see it
2. Enable internally, then one percent of users
3. Monitor four hours: error rate, latency, business metric
4. Clean: ten to fifty to one hundred percent over two to three days
5. Not clean: flip flag OFF — no deploy needed

**Complete when:** All slices merged, dashboard at one hundred percent, cleanup scheduled, zero incidents.

## Decision Trees

### Decision Tree 1: Slice vs. Monolith

    Feature request received
    |
    +-- Can a user get value from a partial implementation?
        +-- YES -> DECOMPOSE into vertical slices
        +-- NO  -> Is it infrastructure-only?
                   +-- YES -> Single change, no flag needed
                   +-- NO  -> Re-examine — almost everything decomposes

### Decision Tree 2: When to Flip the Flag

    VS-N merged and all tests pass
    |
    +-- Is this the first slice (VS-0)?
    |   +-- YES -> Flip to INTERNAL ONLY (QA team, zero percent users)
    |   +-- NO  -> Previous slice stable for more than four hours?
    |              +-- YES -> Increment: one to ten to fifty to one hundred percent
    |              +-- NO  -> WAIT. Investigate errors.

### Decision Tree 3: When to Remove a Flag

    Feature flag at one hundred percent for more than seven days
    |
    +-- Is the flag referenced in any dashboard or alert?
    |   +-- YES -> Update dashboards to remove flag dependency first
    |   +-- NO  -> Proceed with removal
    |
    +-- Is there a cleanup_after date set?
        +-- YES and date has passed -> REMOVE flag and all gating logic
        +-- NO  -> Set cleanup_after to today plus seven days. Retry then.

## Verification

| Complete When | Evidence |
|---|---|
| Complete when VS-0 merged | PR merged, flag config visible in flags.yaml |
| Complete when all slices have feature flags with default: false | Search flags.yaml for each VS flag name |
| Complete when tests pass for both flag ON and OFF states | Test suite run with both flag configurations |
| Complete when no destructive schema changes | Migration diff: only ADD COLUMN, no DROP or ALTER |
| Complete when commit messages reference vertical slice | git log shows feat domain-vsN pattern |
| Complete when flag dashboard entry created | URL to dashboard tile showing flag status |
| Complete when kill switch configured | flags.yaml has kill_switch: true and auto_off_metric |
| Complete when flag removal PR open (flag >7 days at 100 percent) | Flag removal PR linked to flag name |
| Complete when backward compatibility verified | Old API endpoints still respond with 200 |
| Complete when rollback plan documented | Document listing which flags to flip, in what order |

## Best Practices

1. **Slice by user value, not by layer.** User can create a draft post is a slice. Build the Post table is not.
2. **Flags named feature_domain_vsN.** Consistent naming enables instant searching.
3. **Every flag has an owner in CODEOWNERS.** Someone else can kill the flag if you leave.
4. **Tests cover both flag states.** Testing only the ON state is incomplete.
5. **VS-0 ships first, even if it seems useless.** Proves plumbing works: routing, auth, flag infra, CI/CD.
6. **Latency SLIs are per-flag.** A fifty-millisecond regression is visible at flag granularity.
7. **Commit-per-slice reduces review friction.** Fifty-line commits get real reviews in ten minutes.
8. **Flag removal is part of Definition of Done.** Remove after one hundred percent plus seven days.
9. **Backward-compatible schema changes only.** Add columns, never remove or retype.
10. **If a slice breaks, only that slice is rolled back.** The fundamental advantage of incremental delivery.

## Anti-Patterns

| Pattern | Correction |
|---|---|
| Slicing by layer: VS-1 Backend, VS-2 Frontend | Slice by value: VS-1 User can log in, VS-2 User sees dashboard |
| Building all slices on one branch | One branch per slice, merge as each stabilizes |
| Feature flags wrapping entire files | Flags wrap code paths, not files |
| Tests deferred to VS-3 | Test the slice in the slice |
| Flag cleanup deferred to later sprint | Flag removal in same sprint as one hundred percent rollout |
| Kill switches requiring code deploy | Configuration toggle, not code change |

## Gotchas

1. **Flag explosion:** Forty-seven active flags means no cleanup. Cost: $5,000 to $15,000 in test matrix explosion. **Fix:** Flag removal sprint every two weeks.
2. **VS-0 skipping:** Skipping the hello-world slice. Cost: $2,000 to $8,000 — discover infrastructure bugs on VS-3. **Fix:** Never skip VS-0.
3. **Default equals ON:** New behavior for everyone immediately. Cost: $10,000 to $50,000 — bad deploy hits all users. **Fix:** Every new flag defaults to OFF.
4. **Schema migration in slice:** NOT NULL without default breaks old code. Cost: $5,000 to $25,000 in production outage. **Fix:** Nullable with default. Remove nullability later.
5. **Flag dependency chains:** X depends on Y; Y removed, X breaks. Cost: $3,000 to $10,000 cascading failure. **Fix:** Document dependencies in flags.yaml.

## Cross-Skill Coordination

### Upstream (call before implementing)

| Upstream Skill | When to Call |
|---|---|
| feature-flag-architect | No flag infrastructure exists |
| brainstorming | Feature scope unclear or contested |
| security-reviewer | Feature touches auth, payments, or PII |
| system-architect | Feature crosses microservice boundaries |

### Downstream (call after slices ship)

| Downstream Skill | When to Call |
|---|---|
| shipping-and-launch | Ready for staged rollout |
| release-manager | Multi-service coordinated release |
| qa-engineer | Cross-slice integration tests |
| observability-engineer | Flag-level metrics and dashboards |
| code-simplification | Flag cleanup after feature is stable |

## Proactive Triggers

| Trigger | Action | Why |
|---|---|---|
| PR over two hundred lines | Decompose into smaller slices | Review quality drops exponentially |
| Three or more flags in one commit | Split into per-flag commits | Cannot bisect to a single flag |
| Flag at one hundred percent for more than seven days | Open flag-removal PR | Active flags are attack surface |
| Auto-off metric triggered | Page on-call, do not touch the flag | Let system protect itself |
| WIP in commit message | Reject, rewrite with feat domain-vsN | WIP commits break bisect |

## What Good Looks Like

**Correct:**

    PR #142: feat(billing-vs1): add invoice creation endpoint
    - UI: InvoiceForm.tsx (+45)
    - API: POST /api/invoices (+32)
    - Data: invoices migration (+18)
    - Test: vs1-invoice.test.ts (+67)
    Flag: feature_billing_vs1 (default: false, kill_switch: p99 > 1000ms)

**Counter-example (reject):**

    PR #143: added billing stuff (312 lines, no tests, no flag)
    WIP — do not merge yet

## Deliberate Practice

1. **Slice this feature:** Users can upload avatar images. Decompose into VS-0 through VS-3.
2. **Flag removal drill:** Find oldest active flag over thirty days at one hundred percent. Remove in a PR.
3. **Git bisect test:** On a branch with five or more commits, bisect to find a bug-introducing commit.
4. **Safe default audit:** Verify every flag defaults OFF. Flag any defaulting ON.
5. **Slice sizing:** Take last feature PR over two hundred lines. Re-slice into at most one hundred line slices.

## Error Recovery

1. **Flag accidentally ON for all users:** Flip OFF in config — no deploy needed. Investigate. Never delete the flag.
2. **VS-2 merged before VS-1:** Revert VS-2. Merge VS-1 first. Cost: about thirty minutes.
3. **Flag cleanup broke production:** Flag still referenced in dashboard. Re-deploy flag config. Update dashboards. Cost: about one hour.
4. **Migration incompatible with old code:** Rollback migration. Make column nullable. Re-deploy. Cost: about two hours.
5. **Flag infrastructure unavailable:** All flags fail CLOSED. Confirm default OFF. Fix infrastructure. Zero user impact.

## State Log

- [ ] VS-0 decomposed and estimated
- [ ] Feature flag created with default: false
- [ ] VS-0 PR merged
- [ ] VS-1 decomposed and estimated
- [ ] VS-1 PR merged
- [ ] VS-2 decomposed and estimated
- [ ] VS-2 PR merged
- [ ] VS-3 integration decomposed
- [ ] All flags at one hundred percent
- [ ] Flag cleanup scheduled

## References

- [feature-flag-architect](../feature-flag-architect/SKILL.md) — Flag infrastructure design
- [shipping-and-launch](../../07-devops/shipping-and-launch/SKILL.md) — Staged rollout patterns
- [ci-cd-builder](../../07-devops/ci-cd-builder/SKILL.md) — CI/CD pipeline integration
- [tdd-guide](../../06-quality/tdd-guide/SKILL.md) — Test-first discipline per slice
- [brownfield-adoption-planner](../../13-specialized/brownfield-adoption-planner/SKILL.md) — Brownfield adoption
- [Feature Toggles (Martin Fowler)](https://martinfowler.com/articles/feature-toggles.html)
- [Strangler Fig Application (Martin Fowler)](https://martinfowler.com/bliki/StranglerFigApplication.html)
