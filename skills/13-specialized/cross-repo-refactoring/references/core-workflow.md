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
