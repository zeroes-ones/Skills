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
| R8 | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| R9 | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
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

## Core Workflow **(STANDARD)**

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

## Decision Trees **(QUICK)**

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


## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| API endpoint deprecated with 90-day notice — on day 91 the endpoint is removed and 14 downstream services fail because "we never saw the deprecation notice" | The deprecation was announced via a changelog blog post and a `Deprecation: true` HTTP header. The downstream teams (3 different companies, 14 internal services) consume the API but don't read the vendor's changelog. The header was added but no one monitors it. The 90-day timer started when the notice was published, not when consumers acknowledged it | Add a `Sunset` HTTP header (RFC 8594) with the exact date. Send direct emails to registered API consumer contacts at 90d, 60d, 30d, 14d, 7d, 1d before sunset. Instrument: count requests that send the `Deprecation` header and create a dashboard showing % of traffic still on the deprecated endpoint. Do not remove until traffic is <1% of peak for 30 consecutive days | Deprecation notices are a delivery problem, not a publication problem. Publishing a notice is necessary but insufficient — you must confirm receipt. A `Sunset` header is machine-readable; a blog post is not. The removal trigger is `traffic < 1% for 30 days`, not `90 calendar days have elapsed`. |
| "Nobody uses that endpoint" — endpoint removed, payment pipeline breaks, $50K in lost transactions in 4 hours | A developer ran `grep` on the access logs for the last 7 days and found zero hits for the endpoint. But the endpoint is called by a batch job that runs every 30 days (month-end billing). The 7-day window missed the monthly cycle. The endpoint was removed on day 8 of the month — the batch job runs on day 1 | Instrument with a runtime counter (Prometheus `api_calls_total{endpoint="/v1/legacy-payment"}`) and monitor for at LEAST 2 full business cycles (60 days for monthly batch jobs, 90 days for quarterly). Check access logs with a window that covers the longest expected call interval × 3. Never delete based on a 7-day sample | Usage sampling windows must exceed the maximum call interval. Monthly batch jobs are invisible to 7-day access log scans. The only reliable signal is a counter monitored across multiple business cycles. "Nobody uses it" in 7 days means "nobody uses it daily" — not "nobody uses it." |
| Deprecation of `v1/search` announced with a migration guide to `v2/search` — but `v2/search` doesn't support the `include_deleted=true` parameter that 40% of v1 callers depend on | The v2 endpoint was designed for the "90% use case" and omitted the edge-case parameters that v1 accumulated over 5 years. The migration guide said "switch to v2" without addressing the parameter gap. 40% of callers couldn't migrate because v2 lacked equivalent functionality — they stayed on v1 until it was forcibly removed | Before announcing deprecation: run a parameter coverage analysis: `SELECT params, count(*) FROM api_logs WHERE endpoint = '/v1/search' GROUP BY params ORDER BY count(*) DESC`. Every parameter with >1% usage must have a documented equivalent in v2. Publish a migration compatibility matrix — if any cell is red, the deprecation is blocked until it's green | Deprecation without feature parity is forced regression. The v2 endpoint must support every v1 use case that has meaningful usage. "90% feature parity" means "10% of your users can't migrate." Parameter-level coverage analysis identifies the gaps before the announcement. |
| Feature flag removed after being ON at 100% for 8 months — the removal PR deleted the flag check and the code inside `if (featureFlag) { ... }` but the ELSE branch had been silently dead for 8 months and contained a critical bug | The flag had been ON at 100% for so long that the OFF code path (`else` branch) was never tested. The removal PR deleted BOTH the flag check AND the OFF code — assuming the OFF code was unused. But another feature had been silently depending on the OFF code's side effect (a cache invalidation that ran in both branches via a shared function call) | Before removing: trace the full call graph of BOTH branches. Run the test suite with the flag OFF — if any test fails, the OFF code is reachable and must be understood. Audit for shared side effects: any function called from both branches that modifies state. Never delete code you haven't seen execute — instrument both branches with counters for 30 days before removal | Feature flags create dead code branches. After 8 months at 100% ON, the OFF branch is untested and possibly broken — but it may still have side effects that other code depends on. The removal diff must be a NOP: the system behavior after removal must be identical to the system behavior with the flag at 100%. |
| Deprecation communication goes to the `api-announcements@` mailing list — but the list has 400 subscribers, 300 of whom left the company. The actual API consumers (12 engineering teams at 3 client companies) are not on the list | The mailing list was created 5 years ago and never audited. Internal users subscribed with personal emails that bounced. External API consumers registered at onboarding with a single contact email — that person left 2 years ago. The deprecation notice reached exactly 0 of the 12 teams actively consuming the API | Audit the communication list before every deprecation: verify each contact is (a) still at the company, (b) responsible for the integration, (c) has acknowledged receipt. Require a response: "Reply CONFIRMED to acknowledge this deprecation timeline." Escalate non-responders at 60d and 30d — involve account managers for external consumers | Deprecation communication lists rot at the rate of team turnover. A 5-year-old mailing list has 75% stale contacts. Every deprecation must start with a communication audit — confirm that the people receiving the notice are the people maintaining the integration. Require acknowledgment; silence is not consent. |
| Dead code removal deletes `LegacyReportGenerator.java` — 3 weeks later, a quarterly regulatory report fails to generate, and the company misses a compliance filing deadline | The class was never called from application code — it was invoked by a cron job on a server that wasn't in the CI inventory. The cron job's existence was documented in a wiki page last updated in 2019. The dead code analysis tool (static call-graph) correctly reported zero callers — because the caller wasn't in the codebase | Before removing any "dead" code: search all cron configurations (`crontab -l` on every host, Kubernetes CronJob resources, Airflow DAGs, Jenkins jobs). Search all runbooks and operational docs for references to the class/method name. Add a runtime counter for 60 days — even a single invocation means the code is alive, regardless of what static analysis says | Dead code detection by static analysis is incomplete. Cron jobs, one-off scripts, operational runbooks, and external orchestration systems invoke code that has zero in-code references. Always pair static analysis with runtime instrumentation — a counter that logs every invocation is the only authority on whether code is truly dead. |

## Best Practices

1. **Never delete based on intuition — instrument with counters first.** "Nobody uses that endpoint anymore" is a production outage waiting to happen. Add a runtime counter, monitor for 30+ days across all environments, and only delete after confirming zero invocations. Intuition-based deletion cascades through payment pipelines and costs $25K-$150K in downtime and SLA credits.
2. **Replacement-first deprecation.** Never deprecate without a working, feature-complete replacement available on day one of the announcement. A "coming soon" v2 that's 6 months late drives enterprise customers with 12-month integration cycles to competitors. Cost: $100K-$1M in churned ARR. The replacement must be at least as capable as what it replaces.
3. **Expand-Contract for every breaking schema change.** Phase 1: add new column/table alongside old. Phase 2: dual-write to both. Phase 3: migrate existing data. Phase 4: remove old after verification. Each phase deploys independently. Skipping Expand-Contract forces coordinated deploys across 8 services — one missed deploy window corrupts downstream analytics.
4. **Communication cadence scales with deprecation severity.** Advisory deprecation: 90-180 days notice with migration guide. Compulsory deprecation: minimum 90 days from announcement to sunset. Send reminders at 60d, 30d, 14d, 7d, 1d before sunset. The sunset date should be `max(engineering_estimate × 3, slowest_customer_migration_time × 1.5, 90 days)`.
5. **Migration tooling is the highest-ROI deprecation investment.** Automated codemods, lint rules with auto-fix, and compatibility shims reduce migration time by 80-95%. A 2-hour codemod script handles 2,000 call sites with zero human error. Manual migration of the same scope takes 40+ hours and misses 10-25% of call sites. Invest in tooling before announcing the deprecation.
6. **Every feature flag needs a sunset date.** Flags ON at 100% for 60+ days are no longer flags — they're dead code masquerading as configuration. Track flag count as an engineering metric with a target ceiling. A codebase with 200+ flags where 80% are ON permanently creates a 2^200 combinatorial testing matrix that consumes 40% of QA time.
7. **Zombie code hunts are recurring engineering work, not one-time cleanups.** Run `knip`, `vulture`, `deadcode`, or `ts-prune` quarterly. Instrument suspect paths with counters for 30-90 days. 12% dead code in a hot-path microservice wastes 1.2 servers continuously — $30K-$100K/year in unnecessary compute. Track zombie code percentage as a code health metric with a target of < 3%.
8. **Direct consumer notification for every deprecation.** Automated announcements in changelogs are not enough. Direct-message every known consumer maintainer. For enterprise customers, dedicated migration support reduces churn risk. A deprecation that surprises a customer who built their business on your API destroys trust that takes years to rebuild.
9. **Return 410 Gone with migration link, never 500.** When the sunset date arrives, return HTTP 410 Gone with the migration guide URL in the response body. A 500 error sends consumers debugging their own code. A 410 is explicit: "This endpoint was intentionally removed. Here's where to go instead." Include a 7-day grace period of 410 responses before removing the code.
10. **Retro after every deprecation.** What went smoothly? What surprised us? Were migration tools adequate? Was the timeline realistic? Document lessons learned. Each retro improves the next deprecation. A deprecation without a retro repeats the same mistakes — timelines set by engineering convenience that force customer churn, zombie code that nobody instrumented, and breaking changes shipped without Expand-Contract.

## Error Recovery **(DEEP)**

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

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| API deprecation affecting external developers | api-designer, devrel-advocate | Design replacement API, communicate to developer community |
| Database schema deprecation | database-designer | Migration scripts, backward-compatible schema transitions, Expand-Contract pattern |
| Feature flag cleanup at scale | platform-engineer | Flag system tooling, automated expiration, flag hygiene metrics |
| Migration affecting multiple services | migration-architect | Cross-service migration sequencing, dependency order, integration testing |
| Deprecation communication and docs | documentation-engineer, technical-writer | Migration guides, API docs updates, changelog entries |
| Contract-bound deprecation for enterprise customers | customer-success-manager, legal-advisor | Customer outreach, contract renegotiation, SLA compliance |
| Security-motivated deprecation (vulnerable dependency) | security-engineer | CVE severity, forced migration timeline, exception process |


| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | System context, integration points, architectural constraints | Before specialized implementation — understand the system it fits into |


## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | Deprecated API still receiving >1% of total traffic 30 days before sunset | [ALERT] [N]% of traffic still on deprecated [API]. Accelerate migration outreach. Consider extending sunset if migration is not possible. |
| P2 | Feature flag ON for 100% of users for >60 days | [WARN] Flag [name] is effectively permanent. Remove flag check and dead code path. |
| P3 | Code path with zero production invocations for 90+ days | [INFO] Potential zombie code: [file:function]. Verify it is not a cold path. If confirmed dead, schedule removal. |
| P4 | @deprecated annotation older than 12 months without removal | [ALERT] Deprecated code [location] has been undead for 12+ months. Schedule removal this sprint or remove the deprecation annotation (if it will never be removed). |
| P5 | Breaking change shipped without a scheduled breaking change window | [ALERT] Breaking change in [PR/commit] shipped outside scheduled window. Verify consumer notification was adequate. Monitor for error rate spikes. |


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
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

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "Nobody uses that endpoint anymore — just delete it." | Intuition is not data. Three critical internal services still call it, and the deletion cascades through the payment pipeline. Cost: **$25K-$150K** in downtime, emergency fixes, and SLA credits. Never delete based on intuition — instrument, monitor for 30+ days, confirm zero invocations. |
| "We can deprecate next quarter — it's not urgent." | Every quarter of delay adds 25% more consumers to the deprecated surface. What was 3 services becomes 8, and the migration grows from a sprint to a multi-quarter program. Cost: **$50K-$200K/year** in compounding deprecation debt that gets exponentially harder to unwind. |
| "One more feature flag won't hurt — it's just a boolean." | The codebase accumulates 200+ flags, 80% ON at 100%. Every new feature must be tested against 2^200 theoretical combinations. QA spends 40% of time managing flag permutations. Cost: **$50K-$200K/year** in wasted QA time and slower release velocity. Every flag needs a sunset date. |
| "Let's just ship the breaking change — consumers can adapt." | Engineering sets a 30-day window because "the migration is simple." Enterprise customers with change control boards need 90-120 days. They can't meet the deadline and escalate to their account executives. Cost: **$50K-$200K** in account management time and potential customer churn. |
| "That dead code isn't costing us anything — it's just sitting there." | 12% dead code in a high-traffic microservice still executes CPU cycles on every request. At 10K req/s, that's 1.2 wasted servers continuously. Across 50 services over a year: **$30K-$100K/year** in unnecessary cloud compute. Dead code is a recurring infrastructure tax. |

## Anti-Patterns

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

## Verification Guardrails

Before delivering work, the agent must verify:

- [ ] **Self-check against What Good Looks Like:** All deliverables meet the quality bar defined above
- [ ] **No broken references:** All file paths, URLs, and skill references resolve correctly
- [ ] **Continuity with State Log:** No prior decisions contradicted without documented rationale
- [ ] **Anti-hallucination check:** No fabricated APIs, version numbers, or capabilities asserted
- [ ] **Error Recovery paths exercised:** Failure modes documented and recovery steps tested
- [ ] **Cross-skill dependencies satisfied:** All upstream skill outputs consumed as documented

If any checkbox fails, revise before delivering. When all pass, add to the state log.

## Production Checklist **(DEEP)**

- [ ] **[S1]** Deprecation inventory complete: all deprecated surfaces (APIs, features, flags, libraries, endpoints) cataloged with sunset date, replacement, and migration guide. Audit refreshed within last 30 days.
- [ ] **[S2]** Replacement available and feature-complete: every deprecated surface has a working replacement deployed to production before deprecation announcement. Replacement is at least as capable as what it replaces.
- [ ] **[S3]** Runtime counters active on all deprecated surfaces: per-consumer usage metrics emitting to dashboards. Alert configured for non-zero traffic 14 days before sunset. Zero invocations confirmed for 30+ days before code removal.
- [ ] **[S4]** Migration guides published for every deprecation: before/after code examples, common pitfalls with workarounds, timeline with specific dates, contact for migration support. Guides reviewed by a developer unfamiliar with the old API.
- [ ] **[S5]** Sunset dates set with consumer input: timeline = max(engineering_estimate × 3, slowest_customer_migration_time × 1.5, 90 days). Heaviest users surveyed before setting dates. No deprecation window < 90 days.
- [ ] **[S6]** Communication cadence executed: 60d, 30d, 14d, 7d, 1d reminders sent. Direct outreach to all known consumers. Enterprise customers offered dedicated migration support.
- [ ] **[S7]** Feature flag hygiene maintained: zero flags ON at 100% for >60 days without a removal ticket. Zero orphaned flags. Flag count tracked as engineering metric with target ceiling. Sunset date on every new flag.
- [ ] **[S8]** Zombie code percentage measured and trending downward: target < 3% of codebase. Quarterly zombie hunts scheduled. Instrumented suspect paths confirmed dead by 30+ days of zero-invocation counters.
- [ ] **[S9]** Breaking changes use Expand-Contract: each phase independently deployable and reversible. No coordinated multi-service deploys required. Dual-write verified with diffing system.
- [ ] **[S10]** Breaking change window scheduled and published: minimum 30 days advance notice. Next window date communicated to all teams. Migration experts on call during and after the window.
- [ ] **[S11]** 410 Gone responses configured: sunset date returns HTTP 410 with migration link in body. 7-day grace period of 410 before code removal. No 500 errors returned for intentionally removed endpoints.
- [ ] **[S12]** Rollback plan for every removal: revert path documented (restore from git history, re-deploy). Emergency contact list for unexpected breakage. Post-removal monitoring for 30 days with alert on related error spikes.

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