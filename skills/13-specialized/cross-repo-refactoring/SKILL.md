---
name: cross-repo-refactoring
description: >
  Use when planning a breaking API change that affects consumers in other
  repositories; when migrating consumers of a deprecated API across 5+ repos;
  when designing a deprecation and removal strategy for a shared library or
  service; when estimating the blast radius and timeline for a cross-repo
  refactoring; when building automated migration tooling (codemods, automated
  PRs) for cross-repo changes; or when establishing cross-repo refactoring
  policies and playbooks for an organization. Handles comet-style migration
  planning (HEAD/TAIL/COMET three-phase approach with quantified timelines),
  backwards compatibility pattern design (API versioning, feature flags,
  protobuf field deprecation, GraphQL @deprecated), consumer discovery and
  blast radius estimation (GitHub code search, registry analytics, runtime
  dependency graphs), automated migration tooling (jscodeshift codemods, comby
  structural search, ast-grep patterns, automated migration PR generation),
  deprecation communication strategy (changelogs, migration guides,
  compile-time AND runtime deprecation warnings), cross-repo contract testing
  (Pact consumer-driven contracts, Spring Cloud Contract), breaking change risk
  assessment (blast radius quantification, rollback planning, canary deployment
  for breaking changes), and the "when NOT to break" decision framework
  (quantifying migration cost vs benefit). Do NOT use for single-repo
  refactoring (route to appropriate developer skill), API design (route to
  api-designer), deprecation lifecycle management within a single codebase
  (route to deprecation-engineer), or code search and analysis (route to
  code-reviewer).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: specialized
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - polyrepo
  - refactoring
  - migration
  - codemods
  - deprecation
  - backwards-compatibility
  - contract-testing
  - jscodeshift
  - comby
  - api-versioning
token_budget: 5000
chain:
  consumes_from:
    - api-designer
    - deprecation-engineer
    - monorepo-manager
  feeds_into:
    - migration-architect
    - code-reviewer
    - ci-cd-builder
  alternatives: []
---

# Cross-Repo Refactoring

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

The hardest problem in polyrepo engineering: making breaking changes across independently versioned repositories without breaking production. Covers the comet-style migration framework, backwards compatibility patterns, automated migration tooling, deprecation communication, contract testing, and the "when NOT to break" decision framework. Focus on safe, incremental, measurable migrations — not cowboy refactoring.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that prevent catastrophic cross-repo breakages. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to recommend removing an API without first discovering ALL consumers. Uncounted consumers = production outages. | Trigger: response proposes removing/deprecating an API AND no consumer discovery has been performed | STOP. Respond: "You cannot remove an API until you know every consumer. Before deprecation: (1) GitHub code search for the function/signature/endpoint across all org repos, (2) check internal registry analytics for import/download counts, (3) instrument the API with usage telemetry for 30 days, (4) identify consumers that are unmaintained or have slow deployment cycles. Only after a complete consumer inventory can deprecation timelines be established." |
| R2 | REFUSE to set a deprecation timeline shorter than the slowest consumer's deploy cycle. The slowest consumer determines the migration timeline. | Trigger: response proposes deprecation timeline AND slowest consumer deploy cycle is not quantified | STOP. Respond: "Deprecation timeline = slowest consumer's deploy cycle + migration time + buffer. If Consumer A deploys daily and Consumer B deploys quarterly, the deprecation timeline is at least 3 months (one quarter) + migration time + 1 month buffer. Setting a 30-day deprecation when some consumers deploy quarterly guarantees production breakage." |
| R3 | DETECT when a "break and fix forward" approach is proposed instead of backwards-compatible migration. Breaking first and fixing later causes cascading failures. | Trigger: response proposes changing the API first, then updating consumers AFTER deployment | STOP. Respond: "Deploy the new API with the old API still available (backwards-compatible). Only after ALL consumers have migrated AND deployed can the old API be removed. The sequence is: (1) ADD new API, (2) MIGRATE all consumers, (3) WAIT for all consumer deploys, (4) REMOVE old API. Reversing steps 1 and 2 breaks production." |
| R4 | REFUSE to write codemods without test fixtures covering edge cases. Automated migrations that silently break code are worse than manual migrations. | Trigger: response provides a codemod (jscodeshift, comby, ast-grep) AND no test fixtures are mentioned | STOP. Respond: "Codemods must be tested before running across repos. Create test fixtures: (1) the exact pattern to transform, (2) variants (different import styles, argument orders, nesting), (3) negative cases (code that LOOKS similar but should NOT be transformed). Run the codemod against fixtures first. Verify: no false positives, no false negatives. Only then run against real code." |
| R5 | REFUSE to estimate migration effort without quantifying the number of call sites. "Just change the function signature" could mean 5 changes or 5,000. | Trigger: response estimates migration effort/time AND call site count is not quantified | STOP. Respond: "Quantify the blast radius before estimating: (1) how many repos depend on this API? (2) how many call sites per repo? (3) are call sites in tests or production code? (4) how many different patterns need transformation? A 5-line function signature change with 3,000 call sites across 15 repos is a multi-month project, not a quick fix." |
| R6 | DETECT when deprecation warnings are compile-time only without runtime warnings. Compile-time warnings miss already-deployed services. | Trigger: response describes deprecation strategy with only compile-time mechanisms (@deprecated annotation, deprecation comment) AND services consume the API at runtime | STOP. Respond: "Compile-time deprecation only reaches consumers when they rebuild. Deployed services may not rebuild for months. Add runtime deprecation warnings: (1) log a WARN on first use per process lifetime, (2) emit a metric/counter for deprecated API usage, (3) return a Deprecation header in HTTP responses, (4) increment a deprecation counter in your observability dashboard. Without runtime signals, you are flying blind." |
| R7 | REFUSE to execute automated migration PRs without human review gates. Automated PRs at scale can cause widespread breakage. | Trigger: response proposes automated PR creation across 10+ repos AND no review/merge gate is described | STOP. Respond: "Automated migration PRs at scale need safety gates: (1) CI must pass on every PR, (2) batch size limit (max 5 simultaneous PRs until pattern validated), (3) human approval required on first 3 PRs, (4) rollback plan if a merged PR causes issues, (5) monitoring on production after each merge. Without these gates, a bug in the codemod propagates to every repo simultaneously." |

## The Expert's Mindset

You are a polyrepo migration architect who has orchestrated hundreds of breaking changes across dozens of repos without a single production incident. Your mental model:

* **The slowest consumer sets the pace.** You cannot deprecate faster than the slowest-deploying consumer. A mobile app that releases quarterly dominates your timeline. A critical service that deploys daily is irrelevant if a legacy monolith deploys twice a year.
* **Adding is safe. Removing is dangerous. Changing is in between.** Adding a new API endpoint cannot break anything. Removing an existing one can break everything. Renaming is removing AND adding — treat it as a two-phase migration.
* **Observability is non-negotiable.** If you cannot measure deprecated API usage in production, you are making decisions blind. Every deprecation must be instrumented with runtime counters. Zero on the counter for 30 days is the only safe signal for removal.
* **Codemods are code that modifies code — treat them as production software.** A bug in a codemod that runs across 50 repos is a bug deployed to 50 codebases simultaneously. Test fixtures, CI validation, rollback plans — the same rigor as any production change.
* **Not every refactor is worth it.** A cross-repo refactoring costs $50K-$500K+ in aggregate engineering time. The benefit must exceed the cost by at least 2x. If the benefit is "cleaner code," it is not worth it. If the benefit is "$200K/year in reduced incidents," it might be.

## Operating at Different Levels

* **Quick scan (30s):** Identify the API surface to change. Count consumers via org-wide code search. Estimate call site count. Check if consumers have active maintainers. Flag any consumers with slow deploy cycles.
* **Triage (1 hour):** Full blast radius analysis: consumer repo count, call site count, test vs production split, maintainer contact list. Draft migration sequence. Estimate timeline based on slowest deploy cycle.
* **Deep migration (full session):** Complete comet-style migration plan: HEAD deployment, COMET traversal strategy per consumer, TAIL removal criteria. Codemod authoring with fixtures. Deprecation communication plan. Contract testing setup. Rollback planning.
* **Crisis mode (migration breaks production):** Identify which consumer broke and why. Rollback the breaking change OR the consumer. If rollback is not possible, deploy compatibility shim. Root cause: did consumer discovery miss something? Did codemod have a bug? Were deploy cycles underestimated?

## When to Use

Use cross-repo-refactoring when a code change in one repository requires coordinated changes across independently versioned and deployed repositories — the focus is on safe, incremental, measurable migration at organizational scale.

* Planning a breaking API change: function rename, parameter reorder, return type change, endpoint deprecation
* Migrating consumers off a deprecated API: library function, REST endpoint, GraphQL field, gRPC method
* Designing deprecation strategy: timeline, communication, monitoring, removal criteria
* Building automated migration tooling: codemods, structural search-and-replace, automated PR creation
* Estimating blast radius: consumer count, call site count, deploy cycle analysis, risk assessment
* Setting up contract testing: consumer-driven contracts, Pact, Spring Cloud Contract
* Establishing organizational cross-repo refactoring policy: deprecation windows, migration playbooks, escalation paths
* Evaluating "should we even do this?": cost-benefit analysis of breaking change vs living with the current API

Do NOT use cross-repo-refactoring for single-repo refactoring (route to backend-developer or frontend-developer). Do NOT use for API design (route to api-designer). Do NOT use for deprecation within a single codebase (route to deprecation-engineer). Do NOT use for code search (route to code-reviewer).

## Route the Request

### Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | User provides function/class/endpoint name + "deprecate" or "remove" or "breaking change" | Deprecation planning -> Go to **Core Workflow: Phase 1 — Blast Radius** |
| A2 | `file_exists(".github/workflows/migration.yml")` OR `file_exists("scripts/codemod/")` | Active migration tooling -> Go to **Core Workflow: Phase 3 — Codemod Execution** |
| A3 | `file_exists("pact/")` OR `file_contains("package.json", "pact")` OR `file_contains("pom.xml", "pact")` | Contract testing setup -> Jump to **Decision Trees: Contract Testing** |
| A4 | `file_contains("CHANGELOG.md", "Deprecated" OR "BREAKING")` | Active deprecation -> Go to **Core Workflow: Phase 1 — Blast Radius** |
| A5 | User mentions "5+ repos" or "10+ consumers" or "multi-repo migration" | Cross-repo migration planning -> Go to **Core Workflow: Phase 1** |
| A6 | User mentions "jscodeshift" or "comby" or "ast-grep" or "codemod" | Codemod authoring -> Go to **Core Workflow: Phase 3** |
| A7 | No specific artifact, general "how do I..." question | New migration planning -> Go to **Core Workflow: Phase 1** |

### Intent Route (Ask the User)

```
What cross-repo refactoring task are you working on?
|-- Planning a breaking change across multiple repos -> Go to "Core Workflow: Phase 1 — Blast Radius"
|-- Writing a codemod to migrate consumers -> Go to "Core Workflow: Phase 3 — Codemod Authoring"
|-- Designing backwards compatibility for a new API version -> Jump to "Decision Trees: Backwards Compatibility"
|-- Setting up contract tests across repos -> Jump to "Decision Trees: Contract Testing"
|-- Communicating deprecation to consumer teams -> Go to "Core Workflow: Phase 4 — Communication"
|-- Deciding whether this breaking change is worth it -> Jump to "Decision Trees: When NOT to Break"
|-- Recovering from a migration that broke production -> Go to "Core Workflow: Crisis Mode"
```

## Core Workflow

### Phase 1: Blast Radius Analysis

Execute in order. Do not skip steps.

```
1. CONSUMER DISCOVERY
   |-- GitHub org-wide code search:
   |   |-- Search for function name: org:my-org import { oldFunction } from
   |   |-- Search for endpoint path: org:my-org /api/v1/deprecated-endpoint
   |   |-- Search for class/type: org:my-org extends OldBaseClass
   |   |-- Search in code AND issues AND pull requests AND discussions
   |-- Registry analytics (if using npm/maven/pypi):
   |   |-- Download count per version, dependency graph
   |   |-- Identify repos still on old versions
   |-- Runtime telemetry (if instrumented):
   |   |-- API usage counters per consumer (service name, version)
   |   |-- Deprecated endpoint call volume over last 30 days
   |-- Output: complete consumer inventory — repo name, maintainer, call site count, deploy cadence

2. CALL SITE CLASSIFICATION
   |-- For each consumer repo, classify every call site:
   |   |-- Production code vs test code (test-only = lower risk)
   |   |-- Direct call vs wrapper (wrapper = single migration point)
   |   |-- Static vs dynamic usage (dynamic = codemod may miss)
   |   |-- Critical path vs non-critical (critical = higher blast radius)
   |-- Count: total call sites = _____, test sites = _____, production sites = _____

3. DEPLOY CYCLE ANALYSIS
   |-- For each consumer, determine:
   |   |-- Typical deploy frequency: daily / weekly / biweekly / monthly / quarterly
   |   |-- Last deploy date (is the repo actively maintained?)
   |   |-- CI pipeline duration (how long from merge to production?)
   |   |-- Canary/gradual rollout vs instant deploy
   |-- Identify the SLOWEST consumer deploy cycle = _____
   |-- This is your MINIMUM deprecation window

4. MAINTAINER CONTACT LIST
   |-- For each consumer repo: primary maintainer, team, Slack channel, on-call rotation
   |-- Flag: unmaintained repos (no commits in 6+ months) — these need special handling
   |-- Flag: external consumers (outside your org) — these need public deprecation process

5. BLAST RADIUS REPORT
   |-- Total consumers: _____ repos
   |-- Total call sites: _____  (production: _____, test: _____)
   |-- Slowest deploy cycle: _____ days
   |-- Unmaintained consumers: _____ repos
   |-- External consumers: _____
   |-- Estimated migration timeline: _____ to _____ weeks
```

### Phase 2: Comet-Style Migration Planning

```
THE COMET METAPHOR:
  HEAD = New API (the future state)
  TAIL = Old API (the current state, to be removed)
  COMET = Consumers migrating from TAIL to HEAD

PHASE 1: COMET CREATION (Deploy HEAD alongside TAIL)
  1. Add new API (HEAD) to the library/service
     |-- New function name, new endpoint, new type — whatever the target state is
     |-- Old API (TAIL) remains fully functional
     |-- Deploy: HEAD and TAIL coexist in the same release
  2. Verify backwards compatibility
     |-- All existing consumers continue working with TAIL
     |-- New consumers can use HEAD immediately
  3. Instrument TAIL with deprecation counter
     |-- Increment metric on every TAIL usage
     |-- Dashboard: TAIL usage by consumer, by version, over time
  4. Announce deprecation
     |-- CHANGELOG: mark TAIL as @Deprecated (compile-time) + log WARN (runtime)
     |-- Migration guide: HEAD usage examples, before/after
     |-- Timeline: when TAIL will be removed (based on slowest deploy cycle)
     |-- Communication: email, Slack, team meetings for top 5 consumers

PHASE 2: COMET TRAVERSAL (Migrate consumers from TAIL to HEAD)
  1. Prioritize consumers: highest-volume first (reduces TAIL metric fastest)
  2. For each consumer:
     |-- Write codemod if pattern is repetitive (see Phase 3)
     |-- OR manual migration if < 10 call sites
     |-- Open PR with changes
     |-- CI passes (tests + lint + build)
     |-- Merge and deploy consumer
     |-- Verify: TAIL metric from this consumer drops to zero
  3. Track progress: % consumers migrated, % call sites migrated
  4. Gate: TAIL usage below threshold (e.g., < 5% of original) for 30 consecutive days

PHASE 3: COMET REMOVAL (Remove TAIL)
  1. Confirm: TAIL metric = 0 for 30 days across ALL consumers
  2. Remove TAIL code from library/service
  3. Bump MAJOR version (semver: breaking change)
  4. Deploy new version
  5. Monitor: any unexpected errors from straggler consumers?
  6. If errors detected: revert deployment, investigate missed consumer, extend timeline
```

### Phase 3: Codemod Authoring

```
1. SELECT THE RIGHT TOOL
   |-- jscodeshift: JavaScript/TypeScript AST transforms. Best for JS/TS repos.
   |-- comby: Structural search-and-replace across any language. No AST needed.
   |-- ast-grep: Structural search with AST awareness. Good for multi-language.
   |-- semgrep: Pattern-based, security-focused. Good for finding patterns to migrate.
   |-- Custom script (Python/Bash): Regex-based. USE ONLY as last resort (regex misses context).

2. WRITE THE CODEMOD
   |-- Define the transform: OldPattern -> NewPattern
   |-- jscodeshift example:
   |   |-- export default function transformer(file, api) {
   |   |   const j = api.jscodeshift;
   |   |   return j(file.source)
   |   |     .find(j.CallExpression, {callee: {name: 'oldFunction'}})
   |   |     .replaceWith(path => j.callExpression(
   |   |       j.identifier('newFunction'),
   |   |       path.node.arguments  // preserve arguments
   |   |     ))
   |   |     .toSource();
   |   | }
   |-- comby example: comby 'oldFunction(:[args])' 'newFunction(:[args])' -in-place
   |-- Handle edge cases: different argument orders, named vs positional, nested calls

3. TEST THE CODEMOD
   |-- Create test fixtures in __testfixtures__/ directory:
   |   |-- input.js: code BEFORE codemod (diverse patterns: simple, nested, edge cases)
   |   |-- output.js: expected code AFTER codemod
   |   |-- negative.js: code that looks similar but should NOT change
   |-- Run: jscodeshift -t transform.js __testfixtures__/input.js
   |-- Diff output against output.js — must match exactly
   |-- Verify negative.js is unchanged
   |-- Add more fixtures as edge cases are discovered

4. DEPLOY THE CODEMOD
   |-- Phase A — Manual validation: run on 2-3 repos, manually review diffs
   |-- Phase B — Automated PRs: generate PRs for the next 5 repos
   |   |-- Script: for repo in repos; do git clone, run codemod, create PR; done
   |   |-- Each PR: CI must pass, 1 human approval required
   |-- Phase C — Batch rollout: process remaining repos in batches of 5-10
   |   |-- Monitor: any CI failures? any pattern missed?
   |-- Phase D — Stragglers: manual outreach for repos where PRs went stale
```

### Phase 4: Deprecation Communication

```
1. CHANGELOG ANNOUNCEMENT
   |-- Format: ## [MAJOR.MINOR.PATCH] - YYYY-MM-DD
   |-- ### Deprecated: `oldFunction()` is deprecated. Use `newFunction()` instead.
   |-- ### Migration guide: [link to migration doc with code examples]
   |-- ### Removal timeline: Will be removed in vX.0.0 (estimate: Q3 2026)

2. MIGRATION GUIDE
   |-- Before/After code examples for all common usage patterns
   |-- Breaking changes explained: "The return type changed from X to Y because..."
   |-- FAQ: common issues during migration and solutions
   |-- Link to codemod: "Run this to automate the migration: npx @org/codemod-old-to-new"

3. RUNTIME DEPRECATION WARNINGS
   |-- Log: WARN [DEPRECATED] oldFunction() called by service=payment-service. Use newFunction(). Will be removed in v3.0.0.
   |-- Metrics: increment deprecated_api_usage{api="oldFunction",consumer="payment-service"}
   |-- HTTP header: Deprecation: true, Sunset: Sat, 01 Nov 2026 00:00:00 GMT
   |-- GraphQL: add @deprecated(reason: "Use newField instead", removalVersion: "3.0.0")

4. CONSUMER OUTREACH
   |-- Week 1: Announce deprecation (changelog, email, Slack #general)
   |-- Week 2: Direct message top 5 consumer teams with migration guide + codemod link
   |-- Week 4: Check-in: any blockers? any questions?
   |-- Month 2: Public dashboard of migration progress (% consumers migrated)
   |-- Month 3: Final reminder email — TAIL will be removed in 30 days
   |-- Removal date: TAIL removed. Post-removal monitoring for 1 week.
```

## Decision Trees

### Backwards Compatibility Patterns

```
How to introduce a breaking change without breaking consumers?
|-- Pattern 1: Add-Deprecate-Remove (Comet)
|   |-- Step 1: Add newFunction(args) alongside oldFunction(args)
|   |-- Step 2: Mark oldFunction as @Deprecated (compile-time + runtime warning)
|   |-- Step 3: Wait for all consumers to migrate (monitor with runtime counter)
|   |-- Step 4: Remove oldFunction once counter = 0 for 30 days
|   |-- Best for: function/class renames, parameter changes, return type changes
|   |-- Timeline: 4-12 months depending on consumer deploy cycles

|-- Pattern 2: API Versioning (URL path or header-based)
|   |-- Deploy /api/v2/new-endpoint alongside /api/v1/old-endpoint
|   |-- Consumers opt in to v2 by changing their request path or Accept header
|   |-- Deprecate v1 with Sunset header (HTTP date when v1 goes away)
|   |-- Remove v1 when telemetry shows zero traffic for 30 days
|   |-- Best for: REST APIs with many external consumers
|   |-- Timeline: 6-18 months (external consumers move slowly)

|-- Pattern 3: Feature Flags for API Changes
|   |-- Wrap new behavior behind feature flag: if (featureFlag('new-api')) { newBehavior() } else { oldBehavior() }
|   |-- Enable flag for specific consumers first (canary)
|   |-- Gradually increase: 1% -> 10% -> 50% -> 100%
|   |-- Remove old behavior code after 100% on new for 30 days
|   |-- Best for: behavioral changes where API surface stays the same
|   |-- Timeline: 2-8 weeks per flag rollout

|-- Pattern 4: Protocol Buffer Field Deprecation
|   |-- Add new field (never change field number or type of existing field)
|   |-- Mark old field with [deprecated = true]
|   |-- Reserve old field number after removal: reserved 5;
|   |-- Protobuf backwards compatibility: new servers read old messages, old servers read new messages
|   |-- Best for: gRPC services, protobuf-based message formats
|   |-- Timeline: 3-6 months per field deprecation

|-- Pattern 5: GraphQL @deprecated
|   |-- Add newField to schema alongside oldField
|   |-- Mark oldField: @deprecated(reason: "Use newField instead. Removal: 2026-12-31")
|   |-- GraphQL clients see deprecation in IDE and schema introspection
|   |-- Track oldField usage via resolver instrumentation
|   |-- Remove oldField when usage = 0 for 30 days
|   |-- Best for: GraphQL APIs
|   |-- Timeline: 2-6 months
```

### When NOT to Break

```
Is this cross-repo breaking change actually worth it?
|-- QUANTIFY THE COST:
|   |-- Consumer count: _____ repos
|   |-- Call site count: _____
|   |-- Migration time per consumer: _____ hours × _____ repos = _____ hours total
|   |-- Automated? Codemod possible? __% automatable (savings: _____ hours)
|   |-- Total engineering cost: _____ hours × $150/hr = $_____
|   |-- Opportunity cost: features NOT built during migration = $_____
|   |-- Risk cost: probability of production incident × impact per incident = $_____

|-- QUANTIFY THE BENEFIT:
|   |-- Performance improvement: $_____/year in reduced compute
|   |-- Incident reduction: $_____/year in fewer on-call pages
|   |-- Developer velocity: $_____/year in faster feature development
|   |-- Security improvement: $_____/year in reduced vulnerability surface
|   |-- Maintenance reduction: $_____/year in reduced code to maintain
|   |-- Total annual benefit: $_____

|-- DECISION GATE:
|   |-- If benefit / cost > 3: PROCEED (strong ROI)
|   |-- If benefit / cost 1.5-3: PROCEED with caution, strict timeline enforcement
|   |-- If benefit / cost 1-1.5: QUESTION — is there a cheaper way to achieve the benefit?
|   |-- If benefit / cost < 1: DO NOT BREAK — live with the current API

|-- RED FLAGS (any one = reconsider):
|   |-- 3+ unmaintained consumer repos (nobody to do the migration)
|   |-- External consumers outside your org (you cannot force them to migrate)
|   |-- Migration touches authentication/authorization code (high blast radius)
|   |-- Consumer deploy cycle > 3 months (timeline stretches beyond 1 year)
|   |-- Primary benefit is "cleaner code" (subjective, unquantifiable)
```

### Contract Testing Strategy

```
Should you implement consumer-driven contract tests across repos?
|-- WHEN CONTRACT TESTING IS WORTH IT:
|   |-- 5+ consumers of the same API
|   |-- Consumers are maintained by different teams
|   |-- Breaking changes have caused 2+ production incidents
|   |-- API changes at least quarterly

|-- PACT WORKFLOW (Consumer-Driven Contracts):
|   |-- Step 1: Consumer defines expectations in a Pact test:
|   |   |-- "When I call GET /api/users/123, I expect {id: 123, name: 'Alice'}"
|   |   |-- This generates a Pact contract file (JSON)
|   |-- Step 2: Consumer publishes contract to Pact Broker
|   |-- Step 3: Provider verifies all consumer contracts in CI:
|   |   |-- "Can I satisfy all consumer expectations with my current implementation?"
|   |   |-- If verification fails, provider CANNOT deploy — it would break consumers
|   |-- Step 4: Provider can see which consumers depend on which fields
|   |   |-- "Consumer A only uses id and name. Consumer B uses id and email."
|   |   |-- Provider knows: can I change the address field without breaking anyone?

|-- SPRING CLOUD CONTRACT (Provider-Driven):
|   |-- Provider defines contracts (Groovy DSL or YAML)
|   |-- Consumer-side: generated tests verify consumer code against contracts
|   |-- Best for: JVM ecosystem, provider-controlled API evolution

|-- LIGHTWEIGHT ALTERNATIVES:
|   |-- Schema registry + CI schema compatibility check (e.g., Avro, Protobuf)
|   |-- CI job that runs consumer test suites against provider staging
|   |-- Shared API client library with versioned releases
|   |-- OpenAPI spec validation in CI: does the new spec break consumers?
```

## Cross-Skill Coordination

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| Designing the new API that replaces the old one | api-designer | API design for HEAD, backwards compatibility patterns |
| Managing deprecation lifecycle within a single service | deprecation-engineer | @Deprecated annotations, runtime warnings, removal gates |
| Polyrepo architecture decisions affecting migration | monorepo-manager | Should you even be in polyrepo? Would monorepo simplify this? |
| CI/CD for automated migration PRs | ci-cd-builder | Automated PR CI, canary deployments for breaking changes |
| Cross-repo search and analysis for consumer discovery | code-reviewer | GitHub code search patterns, structural search with comby/ast-grep |
| Full repo migration (not just API change) | migration-architect | Framework migration, language version upgrades, architecture changes |
| Observability for deprecation tracking | observability-engineer | Deprecated API usage dashboards, runtime counter metrics, alerting |
| Security implications of deprecation | security-reviewer | Old API may have vulnerabilities — removal is also a security improvement |

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | Function marked @Deprecated but no runtime deprecation counter | [ALERT] Deprecation without observability is blind. Add a runtime counter to track usage before setting a removal date. |
| P2 | Deprecation announced with removal date < 90 days away AND consumers exist with quarterly deploy cycle | [ALERT] Timeline too aggressive. Consumers on quarterly deploy won't even see the deprecation before removal. Extend to 6+ months. |
| P3 | Migration plan lacks consumer contact list | [WARN] Who will do the migration in each consumer repo? Identify maintainers before setting timelines. |
| P4 | Codemod deployed to 5+ repos simultaneously without validation on first 2-3 | [WARN] Batch size too large. Validate on 2-3 repos first, then scale up. A codemod bug at scale is painful to undo. |
| P5 | Deprecated API removal date has passed but TAIL code still exists | [ALERT] Removal date was missed. Reassess: is there still usage? Extend or enforce removal. Indefinite deprecation creates confusion. |
| P6 | Breaking change in library/service that has public/external consumers | [ALERT] External consumers cannot be forced to migrate. API versioning (v1/v2) is the only safe path for public APIs. |

## What Good Looks Like

```
Ideal cross-repo migration (function rename, 12 consumer repos, 200 call sites):

Month 0: Comet Creation
  Library v2.5.0 ships with newFunction() alongside oldFunction()
  oldFunction() logs WARN + increments counter on every call
  CHANGELOG: "oldFunction() deprecated. Migrate to newFunction(). Removal: v3.0.0 (estimated Jan 2027)"
  Migration guide published with before/after examples

Month 1-2: Codemod + First Consumers
  Codemod transforms oldFunction() -> newFunction() (95% automated, 5% manual edge cases)
  PRs opened for top 5 consumer repos
  3 of 5 merged and deployed
  Dashboard: 40% of call sites migrated

Month 3-4: Remaining Consumers
  PRs opened for remaining 7 repos
  Monthly check-in with consumer teams
  Dashboard: 90% of call sites migrated
  2 repos unresponsive — escalated to engineering manager

Month 5: Cleanup
  Last consumer merges. Dashboard: 100% migrated.
  Runtime counter shows 0 oldFunction() calls for 30 consecutive days.

Month 6: Comet Removal
  Library v3.0.0 ships — oldFunction() removed
  Post-deploy monitoring: zero incidents
  Migration complete. Total cost: ~$75K. Benefit: $120K/year in reduced incidents + maintenance.
```

## Deliberate Practice

```
Phase 1: Consumer discovery
  Take a real function in your codebase. Search GitHub org-wide for all call sites.
  Classify: production vs test, critical vs non-critical, simple vs complex patterns.
  Goal: Understand how far a single function spreads across repos.

Phase 2: Write a simple codemod
  Create a function rename codemod with jscodeshift.
  Write 5 test fixtures (simple, nested, edge cases, negative, async).
  Run against a real repo, review the diff manually.
  Goal: Codemod authoring with confidence.

Phase 3: Design a deprecation timeline
  Pick a function you want to rename. Identify all consumers. Determine their deploy cycles.
  Create a deprecation timeline with specific dates: announcement, first migration, last migration, removal.
  Goal: Realistic timeline estimation.

Phase 4: Build a runtime deprecation counter
  Add a counter to an existing API. Emit it as a metric. Create a dashboard.
  Verify: you can see which consumers call which deprecated APIs in real time.
  Goal: Observability-driven deprecation.

Phase 5: Simulate a failed migration
  Change an API, update only SOME consumers. Observe what breaks.
  Practice rollback. Practice the emergency compatibility shim.
  Goal: Muscle memory for when things go wrong.

Phase 6: Full comet migration (capstone)
  Identify a real candidate. Write the plan. Present the cost-benefit analysis.
  If approved: execute Phases 1-3 (creation, traversal, removal).
  Goal: End-to-end migration experience.
```

## Gotchas

* **A codemod that handles 95% of cases still leaves 5% as manual work — and 5% of 2,000 call sites is 100 manual changes.** Codemod authors consistently underestimate the manual tail. Each manual change requires: reading context, understanding the pattern, applying the fix, testing. At 10 minutes per manual change × 100 sites = 16+ hours of unplanned work. **Total cost: $15K-$50K in manual migration work for the tail end of a codemod that "handles almost everything."**

* **Deprecation warnings in logs that nobody reads are worse than no warnings at all.** If your runtime deprecation counter shows 500 calls/day but nobody has an alert on it, you have a false sense of safety. The counter must trigger a dashboard, which must trigger an alert, which must trigger a ticket. Otherwise you will remove the API while it still has active callers. **Total cost: $30K-$150K per production outage caused by removing a "deprecated but still used" API.**

* **"Just use the latest version" doesn't work for consumers with dependency conflicts.** Consumer A uses `your-lib@2.5` for the new API. But Consumer A also uses `other-lib@1.0` which depends on `your-lib@2.0`. Now Consumer A has a diamond dependency conflict and cannot upgrade until `other-lib` also upgrades. This chains indefinitely. **Total cost: $20K-$80K in blocked migration work across a dependency graph with 3+ levels of transitive dependencies.**

* **GraphQL deprecations are invisible if consumers don't update their schema introspection.** When you deprecate a GraphQL field, consumers see the deprecation in their IDE — IF they re-run introspection. Many teams run introspection once at project setup and never again. They will discover the deprecation when the field disappears, not when you announce it. **Total cost: $10K-$40K in emergency fixes when GraphQL consumers discover breaking changes at runtime, months after the deprecation announcement.**

* **Feature flags for API changes create a combinatorial testing matrix.** If you have 3 API changes behind 3 feature flags, you have 8 (2^3) possible states. Nobody tests all 8. When flag combination {newAuth: true, newPagination: false, newFormat: true} breaks, the root cause is a flag interaction that was never tested. **Total cost: $25K-$75K in debugging flag-interaction bugs across a service with 5+ simultaneously active API feature flags.**

* **Unmaintained consumer repos are deprecation black holes.** A repo with no active maintainers will never migrate. You have 3 options: (1) migrate it yourself (takes 2-5 days to understand unfamiliar codebase), (2) accept that this consumer will break and deal with the incident, (3) never remove the old API. All three options are expensive. **Total cost: $15K-$40K per unmaintained consumer repo, either in migration labor or production incident cost.**

* **Contract tests prevent regressions but don't prevent design mistakes.** If Consumer A's Pact test says "I expect field `address` to be a string," and you change `address` to an object (breaking change), the Pact test fails — good. But if Consumer A's Pact test was never written, you have no protection. Contract testing works only for the consumers who have actually written tests. **Total cost: $20K-$60K in undiscovered breaking changes for consumers without contract tests, discovered only after production deploy.**

* **Codemods that modify import paths can break barrel exports and tree shaking.** If a codemod changes `import { foo } from './old-module'` to `import { foo } from './new-module'`, but `./new-module` has different barrel re-exports, downstream consumers of the consumer may also break. Codemods operate on single repos — they cannot see transitive effects. **Total cost: $12K-$35K in cascading breakages when a codemod in Repo A causes import errors in Repo B that depends on Repo A.**

## Verification

After planning or executing a cross-repo refactoring, run this sequence. Do not proceed past a failure.

1. **Consumer inventory completeness:** `org:my-org <function-name>` GitHub search returns 0 additional call sites not in the migration plan. Re-run search with variants (different import styles, aliases).
2. **Codemod test fixtures:** All test fixtures pass: output matches expected, negative cases unchanged. Test against 3 real consumer repos — diffs are correct and complete.
3. **Blast radius documentation:** Consumer count, call site count, deploy cycle analysis, maintainer list all documented and current (within 1 week).
4. **Deprecation observability:** Runtime deprecation counter exists, dashboard shows per-consumer usage, alert fires if counter exceeds threshold.
5. **Timeline feasibility:** Deprecation removal date is at least (slowest deploy cycle × 3) days in the future. All consumer maintainers have acknowledged the timeline.
6. **Rollback plan:** Documented rollback procedure for every consumer. Contact list for emergency rollback coordination.
7. **Benefit exceeds cost:** Documented cost-benefit analysis with ratio > 1.5. Decision record with approval.

If any check fails: diagnose from verification item, provide specific actionable fix, restart verification from failed item.

## References

* [jscodeshift Documentation](https://github.com/facebook/jscodeshift) — JavaScript/TypeScript codemod toolkit
* [comby Documentation](https://comby.dev/) — Structural code search and replace
* [ast-grep Documentation](https://ast-grep.github.io/) — AST-based structural search
* [Pact Documentation](https://docs.pact.io/) — Consumer-driven contract testing
* [/references/comet-migration.md](references/comet-migration.md) — HEAD/TAIL/COMET three-phase framework with timelines
* [/references/backwards-compatibility.md](references/backwards-compatibility.md) — API versioning, feature flags, protobuf, GraphQL patterns
* [/references/consumer-discovery.md](references/consumer-discovery.md) — GitHub search, registry analytics, runtime dependency graphs
* [/references/migration-tooling.md](references/migration-tooling.md) — jscodeshift, comby, ast-grep, automated PR generation
* [/references/deprecation-communication.md](references/deprecation-communication.md) — Changelogs, migration guides, runtime warnings
* [/references/contract-testing.md](references/contract-testing.md) — Pact, Spring Cloud Contract, schema compatibility
* [/references/risk-assessment.md](references/risk-assessment.md) — Blast radius quantification, rollback planning
* [/references/when-not-to-break.md](references/when-not-to-break.md) — Cost-benefit analysis framework for breaking changes
