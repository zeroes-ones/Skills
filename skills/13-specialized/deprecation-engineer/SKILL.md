---
name: deprecation-engineer
description: >
  Use when planning to deprecate APIs, endpoints, SDK versions, database schemas,
  feature flags past their sunset date, or entire services. Handles the full
  deprecation lifecycle: advisory vs. compulsory deprecation, migration patterns
  (Strangler Fig, Adapter, Feature Flag, Expand-Contract), zombie code detection
  and dead code removal, deprecation communication (timelines, migration guides,
  sunset dates), user migration sequencing, backward compatibility windows, and
  breaking change management. "Code is a liability" mindset -- every line you
  delete is a line that cannot cause a bug, incur a cost, or need maintenance.
  Do NOT use for incident response during a live outage (route to
  incident-responder), greenfield API design (route to api-designer), database
  migrations without deprecation context (route to database-designer), or
  monorepo-wide refactors without deprecation planning (route to monorepo-manager).
author: Sandeep Kumar Penchala
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
license: MIT
type: specialized
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - deprecation
  - migration
  - api-lifecycle
  - strangler-fig
  - dead-code
  - backward-compatibility
  - breaking-changes
  - sunset
token_budget: 4000
chain:
  consumes_from:
    - api-designer
    - backend-developer
    - database-designer
    - fullstack-developer
    - migration-architect
  feeds_into:
    - api-designer
    - migration-architect
    - documentation-engineer
    - release-manager
  alternatives: []
---

# Deprecation and Migration

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end deprecation and migration engineering: removing dead code, sunsetting APIs, migrating users off deprecated surfaces, and managing breaking changes with minimal user pain. "Code is a liability" -- every line you maintain costs money in bugs, build time, cognitive load, and security surface area. The best code is the code you never wrote; the second best is the code you successfully deleted. This skill covers the full lifecycle from detection through communication, migration, and final removal.

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to deprecate without a migration path. Deprecation without migration leaves users stranded and erodes trust. | Trigger: deprecation announcement is drafted AND no migration guide or replacement API exists | STOP. "Cannot announce deprecation without a documented migration path. Provide: (a) replacement API/feature, (b) step-by-step migration guide with code examples, (c) estimated migration effort for typical users. Announce only when all three are ready." |
| R2 | DETECT when deprecation timeline is shorter than user migration window. Forcing migration faster than users can move causes churn and production incidents. | Trigger: sunset date minus announcement date is less than 2x the estimated migration effort for the slowest-migrating cohort | STOP. "Deprecation timeline of [N] days is insufficient. Slowest-migrating users need [X] days based on their usage patterns. Minimum timeline: max(90 days, 2x slowest cohort migration time). Extend sunset date or provide exceptional support for slow migrators." |
| R3 | REFUSE to remove code without verifying zero production traffic. Deleted code that is still called in production causes immediate outages. | Trigger: code removal PR is opened AND no evidence of zero traffic for at least 30 days (logs, metrics, or analytics) | STOP. "Cannot verify zero traffic for [endpoint/feature/flag]. Instrument the code path with a counter metric, monitor for 30 days, and only proceed with removal after confirming zero invocations for the full observation period." |
| R4 | DETECT zombie code: code that is reachable but never executed in production. Zombie code accumulates maintenance burden with zero value. | Trigger: code exists in the codebase AND has no corresponding production traffic for 90+ days AND is not a cold path (disaster recovery, license activation, account deletion) | STOP. "Zombie code detected: [file:function]. This code has had zero production invocations for 90+ days. Flag for deprecation: add deprecation warning in the next release, remove in the following release. Exception: cold paths that must work when rarely needed (DR, legal holds, compliance)." |
| R5 | REFUSE to make breaking changes without a breaking change window. Surprise breaking changes destroy developer trust and cause cascading failures. | Trigger: change is marked BREAKING AND no breaking change window is scheduled AND consumers have not been notified at least 30 days in advance | STOP. "Breaking change cannot ship without a scheduled window and advance notice. Requirements: (a) announce breaking change 30+ days before the window, (b) schedule a specific breaking change release, (c) provide migration tooling where possible, (d) coordinate with all known consumers." |
| R6 | DETECT when deprecated API version still has paying or contracted customers. Removing an API that customers depend on breaches SLAs and contracts. | Trigger: API version is scheduled for removal AND active API keys or contractually obligated customers still call it | STOP. "Active customers still depend on [API version]: [count] customers, [volume] requests/day. Cannot remove until all customers have migrated or contracts have been renegotiated. Engage customer success for direct outreach to remaining users." |
| R7 | REFUSE to leave deprecated code with just a comment saying "TODO: remove". Undead code -- deprecated but never removed -- is worse than never deprecating. | Trigger: codebase has `@deprecated` annotations or `Deprecated:` comments older than 6 months without a removal ticket | STOP. "Deprecated code found: [location], annotated [date]. Create a removal ticket with a deadline (within 2 sprints). Track deprecated code count as a metric -- it should trend to zero after each deprecation cycle." |

## The Expert's Mindset

- **Code is a liability, not an asset.** Every line of code you maintain costs money: it must be read, tested, secured, migrated, and debugged. The best line of code is the one you deleted. The second best is the one you never wrote. Measure your impact not by lines added but by lines responsibly removed.
- **Deprecation is a product decision, not just an engineering task.** Users built workflows around your API. Removing it without empathy destroys trust. Treat deprecation as a product launch: communicate clearly, provide migration paths, measure adoption, and support users through the transition.
- **The Strangler Fig beats the Big Bang every time.** Incrementally replacing an old system piece by piece is safer, faster, and less risky than rewriting everything and cutting over. The old and new systems coexist during migration. When the last user migrates off the old system, you delete it with confidence.
- **Zombie code is the silent killer.** Code that runs in production but serves no purpose (abandoned features, dead A/B test branches, deprecated but never removed paths) still consumes CPU, memory, and engineering attention. Hunting zombies is the highest-ROI refactoring activity -- pure cost reduction with zero user impact.
- **Backward compatibility has an expiration date.** Supporting v1 forever is not kindness -- it is technical debt that slows down v2 and v3. Every deprecated API version must have a published sunset date. Users need certainty to plan their migrations.

## Operating at Different Levels

- **Quick scan (30s):** Check deprecation dashboard: count of active deprecations, overdue removals, zombie code percentage, oldest deprecated-but-not-removed artifact.
- **Standard engagement (10min):** Review a specific deprecation: verify migration guide is complete, check adoption metrics for the replacement, confirm traffic to deprecated surface is declining, validate sunset timeline.
- **Deep dive (full session):** Full codebase zombie hunt: instrument suspected dead paths with counters, analyze 90-day traffic patterns, prioritize removal candidates by maintenance cost, draft deprecation announcements with migration guides, plan breaking change windows.
- **Crisis mode (deprecated API causing production issue):** If the deprecated surface has an active incident, accelerate the migration timeline for remaining users with direct outreach. If the replacement has a bug, fix it immediately -- users migrating off the deprecated surface must land on stable ground.

## When to Use

- Planning to deprecate an API version, endpoint, or SDK method
- Removing a feature that has been superseded or has low adoption
- Cleaning up feature flags past their sunset date
- Migrating users from an old system to a new system (Strangler Fig pattern)
- Planning a breaking change release with advance notice and migration tooling
- Hunting zombie code: dead code paths, abandoned experiments, unused abstractions
- Writing deprecation announcements, migration guides, and sunset timelines
- Managing backward compatibility commitments and their expiration

**When NOT to use:** Greenfield API design (api-designer), database schema migrations without user-facing deprecation (database-designer), incident response during active outage (incident-responder), or monorepo-wide refactors without deprecation (monorepo-manager).

## Route the Request

```
What deprecation/migration task are you working on?
|-- Deprecating an API -> Jump to "Decision Trees: API Deprecation"
|-- Removing a feature -> Jump to "Decision Trees: Feature Removal"
|-- Cleaning up feature flags -> Jump to "Decision Trees: Flag Cleanup"
|-- Hunting zombie code -> Jump to "Decision Trees: Zombie Code Detection"
|-- Planning breaking changes -> Jump to "Decision Trees: Breaking Change"
|-- Writing migration guide -> Go to "Core Workflow: Phase 2 - Migration Guide"
|-- Full deprecation audit -> Start at "Core Workflow: Phase 1 - Deprecation Audit"
```

## Core Workflow

### Phase 1: Deprecation Audit

```
1. INVENTORY DEPRECATED SURFACES
   |-- Scan codebase for deprecation markers:
   |   |-- @Deprecated annotations (Java, Kotlin, Swift)
   |   |-- @deprecated JSDoc tags
   |   |-- DeprecationWarning in Python
   |   |-- [Obsolete] attribute in C#
   |   |-- // DEPRECATED: comments
   |-- Scan feature flag system for flags past sunset date
   |-- Scan API gateway for versioned endpoints (v1, v2, etc.)
   |-- Output: list of all deprecated surfaces with dates and owners

2. MEASURE TRAFFIC PER SURFACE (LAST 90 DAYS)
   |-- Instrument each deprecated surface with a counter
   |-- Collect 90-day traffic data: request count, unique callers, error rate
   |-- Categorize:
   |   |-- ZERO TRAFFIC: safe to remove immediately (with PR review)
   |   |-- DECLINING: traffic is dropping, migration is in progress
   |   |-- STABLE: users have not migrated, need intervention
   |   |-- GROWING: new users adopting deprecated surface -- CRITICAL issue

3. IDENTIFY ZOMBIE CODE
   |-- Code reachable by static analysis but zero production invocations
   |-- Feature flags permanently ON (no off path exercised)
   |-- A/B test branches where experiment ended 90+ days ago
   |-- Error handling for conditions that never occur in production
   |-- Dead code percentage = (zombie LOC / total LOC) * 100
   |-- Target: zombie code under 3% of codebase

4. PRIORITIZE REMOVAL ORDER
   |-- Tier 1 (Remove Now): Zero traffic + no cold-path risk
   |-- Tier 2 (Remove This Sprint): Declining traffic + migration guide exists
   |-- Tier 3 (Plan Removal): Stable traffic + replacement available
   |-- Tier 4 (Intervention Needed): Growing traffic on deprecated surface
   |-- Tier 5 (Contract-Bound): Paying customers, cannot remove unilaterally
```

### Phase 2: Migration Guide

```
1. WRITE THE GUIDE (FOR YOUR USERS, NOT FOR YOU)
   |-- Title: "Migrating from [OLD] to [NEW]"
   |-- Section 1: WHY migrate (benefits of new API, risks of staying on old)
   |-- Section 2: WHEN to migrate (timeline, sunset date, breaking change windows)
   |-- Section 3: HOW to migrate (step-by-step with code examples)
   |   |-- Before/after code snippets for every endpoint/method
   |   |-- Common pitfalls and how to avoid them
   |   |-- Handling edge cases that differ between old and new
   |-- Section 4: VERIFY migration (how to test, what to check)
   |-- Section 5: GET HELP (support channels, escalation path, office hours)

2. PROVIDE MIGRATION TOOLING (WHEN POSSIBLE)
   |-- Automated codemods (jscodeshift, comby, semgrep)
   |-- SDK compatibility shims during transition period
   |-- Linting rules that flag deprecated usage (eslint-plugin-deprecation)
   |-- Runtime warnings with migration instructions in the message
   |-- Self-service migration dashboard showing progress

3. MEASURE MIGRATION PROGRESS
   |-- Track: % of users on old vs new surface over time
   |-- Target migration curve: 25% at 30d, 50% at 60d, 90% at 90d
   |-- Identify slow migrators for direct outreach
   |-- Celebrate migration milestones to maintain momentum
```

### Phase 3: Removal Execution

```
1. CONFIRM pre-removal checklist
   |-- Traffic to deprecated surface: ZERO for 30+ days
   |-- All known consumers migrated or contractually released
   |-- Migration guide published and accessible
   |-- Support team briefed on deprecation and migration path
   |-- Removal PR reviewed by at least 2 engineers
   |-- Breaking change window scheduled (if applicable)

2. EXECUTE removal
   |-- Delete the code (celebrate the deletion!)
   |-- Remove feature flag from flag management system
   |-- Update API documentation to remove deprecated endpoints
   |-- Archive monitoring dashboards for the removed surface
   |-- Update CI to remove tests specific to the deprecated code

3. VERIFY post-removal
   |-- Monitor for 48 hours: any errors from callers still hitting removed surface?
   |-- Check support tickets: any users reporting breakage?
   |-- Update deprecation audit: remove from inventory
   |-- Announce removal completion to stakeholders
   |-- Retro: was the deprecation smooth? What could be improved?
```

## Decision Trees

### API Deprecation

```
Phase 1: ASSESS
|-- Is there a replacement API?
|   |-- Yes -> Proceed to Phase 2
|   |-- No -> HALT. Cannot deprecate without a replacement. Build v2 first.
|-- What is the traffic volume?
|   |-- Zero traffic for 30+ days -> Expedited removal (no announcement needed)
|   |-- Low traffic (<1% of total) -> Standard deprecation (90-day notice)
|   |-- Medium traffic (1-10%) -> Extended deprecation (180-day notice + active migration support)
|   |-- High traffic (>10%) -> Do not deprecate yet. Invest in migration tooling and incentives first.

Phase 2: ANNOUNCE
|-- Advisory deprecation: API still works but is discouraged
|   |-- Add deprecation header (Sunset: Sat, 31 Dec 2026 23:59:59 GMT)
|   |-- Add runtime warning with migration link
|   |-- Publish migration guide
|   |-- Timeline: 90-180 days before compulsory
|-- Compulsory deprecation: API will stop working on sunset date
|   |-- All advisory steps PLUS:
|   |-- Direct outreach to all known consumers
|   |-- Breaking change window scheduled
|   |-- Timeline: minimum 90 days from compulsory announcement to sunset

Phase 3: ENFORCE
|-- Pre-sunset reminders: 60d, 30d, 14d, 7d, 1d before sunset
|-- Sunset day: API returns 410 Gone with migration link in body
|-- Grace period: 7 days of 410 (not 500!) to make failure explicit
|-- Post-sunset: remove code, archive docs, close related tickets
```

### Feature Removal

```
Phase 1: DETECT low-adoption features
|-- Query analytics: feature usage over last 90 days
|-- Threshold: features used by <1% of users AND not required for compliance/legal
|-- Flag candidates for removal review

Phase 2: VALIDATE removal safety
|-- Is the feature gated by a feature flag?
|   |-- Yes -> Turn flag OFF for 30 days. Any complaints?
|   |-- No -> Add a kill switch, turn off, monitor for 30 days
|-- Are there paying customers who depend on this feature?
|   |-- Yes -> Cannot remove unilaterally. Offer migration to alternative or contract renegotiation.
|   |-- No -> Proceed to Phase 3
|-- Is there a regulatory/compliance requirement?
|   |-- Yes -> Cannot remove. Document the requirement and close the removal ticket.
|   |-- No -> Proceed to Phase 3

Phase 3: REMOVE
|-- Announce removal 30 days in advance
|-- Provide alternative workflow or replacement feature
|-- Remove feature flag, UI, backend code, tests, documentation
|-- Monitor support channels for 30 days post-removal
```

### Flag Cleanup

```
Phase 1: AUDIT
|-- List all feature flags with creation date
|-- Categorize by status:
|   |-- ACTIVE: flag is used in production, has a purpose
|   |-- DARK: flag exists but is OFF everywhere (never launched or rolled back)
|   |-- PERMANENT: flag has been ON (100%) for 60+ days -- it is no longer a flag, it is the default
|   |-- ORPHANED: flag owner has left the team/company
|   |-- EXPIRED: flag past its sunset date

Phase 2: CLEANUP per category
|-- PERMANENT flags (ON 100% for 60+ days):
|   |-- Remove flag check, keep the ON-path code
|   |-- Delete the OFF-path code (it has not run in 60+ days)
|   |-- Remove flag from flag management system
|-- DARK flags (OFF everywhere):
|   |-- If never launching: delete flag and all gated code
|   |-- If launching soon: set a hard launch date, convert to ACTIVE
|-- ORPHANED flags:
|   |-- Assign new owner or escalate to engineering manager
|   |-- If no owner within 1 sprint, treat as EXPIRED
|-- EXPIRED flags:
|   |-- Immediate removal if ON 100% or OFF everywhere
|   |-- If partially rolled out, decide: launch to 100% or kill

Phase 3: PREVENT recurrence
|-- Every new flag: owner, sunset date, kill switch
|-- Automated flag expiration: system warns at 30/60/90 days
|-- Flag count tracked as engineering metric -- should be sawtooth, not monotonic
```

### Zombie Code Detection

```
Phase 1: STATIC DETECTION
|-- Tools to find potentially dead code:
|   |-- knip (JS/TS): finds unused files, dependencies, exports
|   |-- vulture (Python): finds dead code via AST analysis
|   |-- deadcode (Go): finds unused functions and variables
|   |-- ts-prune (TypeScript): finds unused exports
|   |-- Coverage reports: 0% covered code paths are suspects (not proof)
|-- Warning: static analysis has false positives. Entry points, reflection, and dynamic dispatch look dead but are not.

Phase 2: RUNTIME VERIFICATION
|-- Add counter metrics to suspected dead paths
|-- Monitor for 30-90 days (include at least one full business cycle)
|-- Cold paths (DR, compliance, annual reports): may legitimately have zero traffic for 90 days
|-- Distinguish: "never called" vs "called rarely but critically"

Phase 3: SAFE REMOVAL
|-- Zero invocations for 90+ days AND not a cold path -> safe to delete
|-- Replace with explicit error: "This code path was removed on [date]. If you reach this error, contact [team]."
|-- Keep the error for 30 days as a safety net, then remove it too
|-- Track zombie code % as a code health metric
```

### Breaking Change Management

```
Phase 1: JUSTIFY the breaking change
|-- Is the breaking change necessary?
|   |-- Yes (examples): security fix, data integrity bug, compliance requirement, fundamental architecture improvement
|   |-- No (examples): rename for aesthetics, minor API shape preference, "we should have done it differently"
|   |-- If No -> Find a backward-compatible way. Add v2 alongside v1.
|-- Can the breaking change be avoided?
|   |-- Additive change: add new field/method, deprecate old one -> NOT BREAKING
|   |-- Expand-Contract pattern: support both old and new during transition -> NOT BREAKING
|   |-- Default values: new required param with default -> NOT BREAKING (usually)

Phase 2: PLAN the breaking change
|-- Announce: minimum 30 days before breaking change window
|-- Migration tooling: automated codemods, lint rules, compatibility shims
|-- Breaking change window: scheduled release where breaking changes are allowed
|-- Version bump: MAJOR version (SemVer) or new API version (v2, v3)
|-- Consumer coordination: direct outreach to all known consumers

Phase 3: EXECUTE
|-- Release the breaking change during the scheduled window
|-- Monitor: error rate spike from consumers who missed the migration
|-- Support: have migration experts on call during and after the window
|-- Retro: was the advance notice sufficient? Were migration tools adequate?
```

## Cross-Skill Coordination

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| API deprecation affecting external developers | api-designer, devrel-advocate | Design replacement API, communicate to developer community |
| Database schema deprecation | database-designer | Migration scripts, backward-compatible schema transitions, Expand-Contract pattern |
| Feature flag cleanup at scale | platform-engineer | Flag system tooling, automated expiration, flag hygiene metrics |
| Migration affecting multiple services | migration-architect | Cross-service migration sequencing, dependency order, integration testing |
| Deprecation communication and docs | documentation-engineer, technical-writer | Migration guides, API docs updates, changelog entries |
| Contract-bound deprecation for enterprise customers | customer-success-manager, legal-advisor | Customer outreach, contract renegotiation, SLA compliance |
| Security-motivated deprecation (vulnerable dependency) | security-engineer | CVE severity, forced migration timeline, exception process |

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | Deprecated API still receiving >1% of total traffic 30 days before sunset | [ALERT] [N]% of traffic still on deprecated [API]. Accelerate migration outreach. Consider extending sunset if migration is not possible. |
| P2 | Feature flag ON for 100% of users for >60 days | [WARN] Flag [name] is effectively permanent. Remove flag check and dead code path. |
| P3 | Code path with zero production invocations for 90+ days | [INFO] Potential zombie code: [file:function]. Verify it is not a cold path. If confirmed dead, schedule removal. |
| P4 | @deprecated annotation older than 12 months without removal | [ALERT] Deprecated code [location] has been undead for 12+ months. Schedule removal this sprint or remove the deprecation annotation (if it will never be removed). |
| P5 | Breaking change shipped without a scheduled breaking change window | [ALERT] Breaking change in [PR/commit] shipped outside scheduled window. Verify consumer notification was adequate. Monitor for error rate spikes. |

## What Good Looks Like

```
DEPRECATION: Payment API v1 -> v2

Timeline:
  Day 0: v2 launched (feature-complete), v1 marked advisory deprecation
  Day 0: Migration guide published with code examples for all 12 endpoints
  Day 30: 45% of traffic migrated to v2 (automated codemod helped)
  Day 60: 78% of traffic migrated, slow-migrators identified (3 enterprise customers)
  Day 75: Direct outreach to enterprise customers, dedicated migration support
  Day 90: v1 marked compulsory deprecation, Sunset header added
  Day 120: v1 returns 410 Gone, 99.8% of traffic on v2
  Day 127: Grace period ends, v1 code removed from codebase
  Day 130: v1 dashboards archived, support tickets closed
  Retro: Migration was smooth. Codemod was the highest-ROI investment.

Bad alternative (anti-pattern):
  Day 0: v2 launched (missing 3 endpoints v1 had)
  Day 1: v1 removed immediately (no deprecation period)
  Day 1-30: 40+ customer complaints, 3 production incidents from unexpected breaking changes
  Day 30: v1 reinstated to stop the bleeding
  Outcome: Trust destroyed, both v1 and v2 maintained for 6 more months
```

## Deliberate Practice

1. **Zombie Hunt:** Take a production codebase and run a static dead code detector (knip, vulture, deadcode). For each finding, classify as: definitely dead, possibly cold-path, or false positive. Add counters to the top 5 "definitely dead" candidates. After 30 days, remove the ones with zero invocations.

2. **Deprecation Roleplay:** Write a deprecation announcement and migration guide for a fictional API. Have a teammate play the role of an angry customer who built their business on the deprecated API. Practice responding with empathy while maintaining the deprecation timeline. Identify gaps in your migration guide from their objections.

3. **Flag Spring Cleaning:** Audit all feature flags in your codebase. For each flag older than 60 days that is ON at 100%, remove it. For each orphaned flag, assign a new owner or escalate. Track flag count before and after. Aim for a 30%+ reduction in active flag count.

4. **Breaking Change Impact Analysis:** Pick a public API method. List all known consumers (internal, external, SDK). For each, estimate the effort to migrate if you changed the method signature. Write a backward-compatible wrapper that supports both old and new signatures. Compare the wrapper approach vs the breaking change approach.

5. **Expand-Contract Pattern Drill:** Take a database schema change that would normally be breaking (rename column, split table). Design an Expand-Contract migration: Phase 1 (Expand): add new column/table alongside old. Phase 2: write to both. Phase 3: read from new, fall back to old. Phase 4 (Contract): remove old column/table. Time each phase and identify the rollback point at each step.

## Gotchas

- **Deleting code that is still called in production causes an immediate outage.** A developer deletes a deprecated endpoint that "nobody uses anymore" based on intuition, not data. Three critical internal services still call it, and the deletion causes a cascade of failures across the payment pipeline. **Total cost: $25,000-$150,000 in downtime, emergency fixes, and SLA credits.** Fix: Never delete based on intuition. Instrument with counters, monitor for at least 30 days across all environments. Only delete after confirming zero invocations.

- **Deprecating an API without a replacement drives customers to competitors.** A SaaS company deprecates their REST API v1 and points users to a "coming soon" v2 that is 6 months late. Enterprises with 12-month integration cycles cannot wait and switch to a competitor. **Total cost: $100,000-$1,000,000 in lost annual recurring revenue from churned enterprise accounts.** Fix: Never deprecate without a working, feature-complete replacement available on day one of the deprecation announcement. The replacement must be at least as capable as what it replaces.

- **Feature flags left ON permanently become a combinatorial testing nightmare.** A codebase accumulates 200+ feature flags, 80% of which are ON for 100% of users. Every new feature must be tested against 2^200 theoretical flag combinations. The QA team spends 40% of their time managing flag permutations instead of testing new features. **Total cost: $50,000-$200,000/year in wasted QA time and slower release velocity.** Fix: Every flag gets a sunset date. Flags ON at 100% for 60+ days are removed (keep ON-path, delete OFF-path). Track flag count as an engineering metric with a target ceiling.

- **Zombie code in hot paths wastes millions in cloud costs.** A high-traffic microservice has 12% dead code paths (abandoned A/B tests, deprecated feature branches) that still execute CPU cycles on every request. At 10,000 requests/second, this wastes the equivalent of 1.2 servers continuously. Over a year, across 50 services, this adds up. **Total cost: $30,000-$100,000/year in unnecessary cloud compute.** Fix: Regular zombie hunts. Instrument suspect paths. Dead code removal should be a recurring engineering sprint item, not a one-time cleanup.

- **A breaking change shipped without the Expand-Contract pattern forces coordinated deploys.** A team changes a database column type from INT to BIGINT. All 8 services that read this column must deploy simultaneously. One service misses the deploy window, and for 4 hours it writes truncated data that corrupts downstream analytics. **Total cost: $15,000-$50,000 in data corruption remediation and coordinated deploy overhead.** Fix: Use Expand-Contract. Phase 1: add new BIGINT column, write to both. Phase 2: migrate existing data. Phase 3: read from new column. Phase 4: remove old INT column. Each phase is independently deployable and reversible.

- **A deprecation timeline set by engineering convenience, not user reality, forces churn.** Engineering sets a 30-day deprecation window for an API because "the migration is simple -- just change one parameter." Enterprise customers with change control boards, compliance reviews, and QA cycles need 90-120 days minimum. They cannot meet the deadline and escalate to their account executives. **Total cost: $50,000-$200,000 in account management time, contract renegotiations, and potential customer loss.** Fix: Survey your heaviest users before setting deprecation timelines. The sunset date should be: max(engineering_estimate * 3, slowest_customer_migration_time * 1.5, 90 days).

- **Removing error handling for "impossible" conditions creates silent data corruption.** During a zombie hunt, a developer removes error handling for a database constraint violation because "this constraint is enforced at the application layer, so it can never fail in production." Six months later, a race condition in a new feature bypasses the application check, the constraint violation is unhandled, and the transaction silently fails -- corrupting financial data for 2 weeks before detection. **Total cost: $50,000-$500,000 in financial data correction and audit remediation.** Fix: Distinguish between "dead code" (never reached in any execution path) and "error handling for unlikely conditions." Zombie code removal must not remove safety nets. If you remove an error handler, replace it with an explicit assertion that fires an alarm if the impossible happens.

## Verification

- [ ] Deprecation audit: all deprecated surfaces have a sunset date, a replacement, and a migration guide
- [ ] Traffic verification: zero-invocation surfaces confirmed by 30+ days of counter metrics before code removal
- [ ] Feature flag hygiene: no flags ON at 100% for >60 days without a removal ticket; no orphaned flags
- [ ] Zombie code percentage: measured and trending downward, with a target of under 3% of the codebase
- [ ] Breaking change schedule: next breaking change window is published at least 30 days in advance
- [ ] Migration guides: every deprecated surface has a guide with before/after code examples and common pitfalls
- [ ] Consumer notification: all known consumers of deprecated surfaces have been directly notified
- [ ] Rollback plan: for every removal, the revert path is documented (restore from git history, re-deploy)

## References

- [Google Deprecation Policy](https://cloud.google.com/products/deprecation-policy) -- Industry-standard deprecation timeline and communication model
- [Martin Fowler: Strangler Fig Application](https://martinfowler.com/bliki/StranglerFigApplication.html) -- Incremental replacement pattern
- [Stripe API Versioning](https://stripe.com/blog/api-versioning) -- Best-in-class API versioning and deprecation approach
- [GitHub API Versioning](https://docs.github.com/en/rest/overview/api-versions) -- API deprecation with Sunset headers
- [Semantic Versioning 2.0.0](https://semver.org/) -- Breaking change signaling through version numbers
- [Knight Capital Incident (2012)](https://en.wikipedia.org/wiki/Knight_Capital_Group#2012_stock_trading_disruption) -- $440M loss from dead code reactivation during deploy
- [references/core-workflow.md](references/core-workflow.md) -- Detailed deprecation audit and removal execution workflow
- [references/anti-patterns.md](references/anti-patterns.md) -- Deprecation anti-patterns: what not to do
- [references/best-practices.md](references/best-practices.md) -- Migration patterns: Strangler Fig, Adapter, Expand-Contract
- [references/calibration.md](references/calibration.md) -- Deprecation timeline calibration by user cohort and risk level
- [references/checklist.md](references/checklist.md) -- Pre-removal verification checklists
- [references/error-decoder.md](references/error-decoder.md) -- Common removal failures and recovery procedures
- [references/footguns.md](references/footguns.md) -- Deprecation footguns: the most expensive deletion mistakes
- [references/scale-depth.md](references/scale-depth.md) -- Scaling deprecation from single service to platform-wide