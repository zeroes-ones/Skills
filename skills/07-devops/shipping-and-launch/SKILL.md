---
name: shipping-and-launch
description: >
  Use when preparing a software release for production, designing staged rollout
  strategies, managing feature flags through their lifecycle, setting up launch-day
  monitoring, or making go/no-go decisions. Handles pre-launch checklists spanning
  code quality, security, performance, accessibility, infrastructure, and
  documentation, staged rollout sequences (5%-25%-50%-100%), feature flag lifecycle
  management (dark launch through deprecation), rollback decision thresholds based
  on error rates and latency, launch-day monitoring setup, go/no-go criteria
  frameworks, and launch communication templates for stakeholders and users. Do NOT
  use for CI/CD pipeline design (route to ci-cd-builder), release coordination
  calendars (route to release-manager), incident response during a live incident
  (route to incident-responder), or performance benchmarking (route to
  performance-engineer).
author: Sandeep Kumar Penchala
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
license: MIT
type: devops
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - shipping
  - launch
  - feature-flags
  - staged-rollout
  - go-no-go
  - release-management
  - monitoring
  - rollback
token_budget: 4000
chain:
  consumes_from:
  - automation-engineer
  - ci-cd-builder
  - qa-engineer
  - security-reviewer
  - performance-engineer
  - release-manager
  feeds_into:
  - automation-engineer
  - incident-responder
  - release-manager
  - site-reliability-engineer
  - observability-engineer
  alternatives: []
---
# Shipping and Launch

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end shipping and launch discipline: pre-launch readiness verification, staged rollout execution, feature flag lifecycle management, rollback decision frameworks, and launch communication. Every launch is a calculated risk -- the goal is to reduce blast radius, detect problems before users do, and have a clear rollback path when things go wrong. Ships are not events; they are processes with gates, signals, and pre-rehearsed abort procedures.
<!-- QUICK: 30s -->
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated advice breaks real systems. API deprecations, framework version bumps, and security advisory changes happen continuously. Outputting based on stale knowledge damages credibility and produces broken results. | Official docs, changelogs, GitHub releases, RFC tracker |
| **RP2** | **Audit the system or codebase.** Read relevant files. Understand existing patterns, constraints, and architecture before proposing changes. | [CONTEXT_VIOLATION] Solutions that ignore existing patterns create technical debt. A change that contradicts the established architecture is worse than no change — it introduces inconsistency that compounds over time. | Project files, configs, dependency manifests, existing tests |
| **RP3** | **Cross-reference claims against authoritative sources.** Every factual assertion needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] Claims without sources are indistinguishable from hallucinations. The #1 cause of incorrect output is treating assumptions as facts. Source tagging prevents this. | Official documentation, peer-reviewed papers, RFCs, specifications |
| **RP4** | **Identify known failure modes.** Before recommending, list what commonly breaks. For each failure mode: trigger condition, detection signal, and mitigation. | [FAILURE_BLINDNESS] Every domain has known failure patterns. Output that doesn't address them is dangerously incomplete. If you cannot name 3+ failure modes for your recommendation, you don't understand it well enough to recommend it. | Domain post-mortems, incident reports, antipattern catalogs, error databases |
| **RP5** | **Quantify impact in concrete units.** Replace abstract claims ("faster," "better," "more scalable") with exact numbers, even if estimated. | [VAGUENESS_PENALTY] "Faster" is unverifiable. "Reduces p95 latency from 340ms to 120ms (±15ms)" is verifiable. Abstract adjectives hide ignorance behind confidence. Concrete numbers expose gaps. | Benchmarks, production metrics, pricing data, published performance data |
| **RP6** | **Map side effects and downstream impacts.** What else breaks? Which dependencies are affected? Which downstream consumers need updating? | [CASCADE_BLINDNESS] Changes to one component ripple outward. A fix in module A can break module B that depends on A's old behavior. Map the blast radius before acting. | Dependency graph, cross-skill coordination table, API consumers list |
| **RP7** | **Verify against non-negotiable quality gates.** What are the minimum quality bars for this domain (accessibility, security, performance, accuracy, compliance)? | [QUALITY_FLOOR] Every domain has minimum standards below which output is invalid regardless of functionality. Missing WCAG AA = broken. Leaking credentials = broken. Silent data loss = broken. | Domain standards, compliance frameworks, security baselines, accessibility guidelines |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? What are the known boundaries? What scenarios are explicitly out of scope? | [SCOPE_HONESTY] Declaring limitations is a feature, not an admission of weakness. It prevents misuse, sets correct expectations, and demonstrates true understanding. Every solution has boundaries — naming them is professional. | This SKILL.md, domain literature, edge case databases |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks systems, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Domain verified against changelog v2.4. No breaking changes since cutoff.]`. Partial research = partial quality. Zero research = zero credibility.



### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.



## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to launch without a verified rollback plan. Every launch must have a documented, tested rollback procedure. | Trigger: launch request is made AND no rollback.md or rollback runbook exists in the release artifacts | STOP. "No verified rollback plan exists. Every launch requires a tested rollback procedure. Document the rollback steps, verify they work in staging, and include rollback success criteria before proceeding." |
| R2 | DETECT when launch happens outside business hours without on-call coverage. Off-hours launches without support guarantee extended downtime. | Trigger: launch time is outside 9am-5pm local time AND no on-call engineer is scheduled AND feature is customer-facing | STOP. "Launching outside business hours without on-call coverage risks extended downtime. Either: (a) reschedule during business hours, (b) ensure an on-call engineer is available, or (c) confirm the blast radius is non-customer-facing." |
| R3 | REFUSE to skip staging environment validation. Production is not a testing environment. | Trigger: launch request AND no staging deploy in last 24 hours OR staging tests failed | STOP. "Staging has not been validated within 24 hours. Deploy to staging, run the full test suite and smoke tests, verify all checks pass, then proceed to production." |
| R4 | DETECT when error budget is exhausted before launch. Launching with a burned error budget guarantees violated SLOs. | Trigger: error budget remaining is less than 30% AND launch involves changes to high-traffic paths | STOP. "Error budget for [service] is at [X]%. Launching now risks immediate SLO violation. Either: (a) wait for error budget to recover, (b) reduce blast radius to non-critical paths, or (c) get explicit VP-level approval for error budget override." |
| R5 | REFUSE to launch without monitoring dashboards configured. You cannot detect problems you are not measuring. | Trigger: launch request AND no dashboards exist for key metrics (error rate, latency p50/p95/p99, throughput, saturation) | STOP. "No monitoring dashboards configured for [service/feature]. Create dashboards for: error rate, latency percentiles, throughput, and saturation. Set alert thresholds. Verify dashboards show data from staging." |
| R6 | DETECT when feature flag has no kill switch. Feature flags without a kill switch turn emergencies into outages. | Trigger: feature flag configuration lacks an emergency off-switch (environment variable, config toggle, or admin API) | STOP. "Feature flag [name] has no kill switch. Add an emergency disable mechanism that works WITHOUT a deployment -- environment variable, remote config toggle, or admin API that takes effect within 60 seconds." |
| R7 | REFUSE to launch when dependent services are unhealthy. A healthy service depending on an unhealthy downstream will fail. | Trigger: launch request AND any critical downstream dependency has degraded status on the health dashboard | STOP. "Dependent service [name] is currently degraded ([status]). Launching now couples your launch risk to their ongoing incident. Wait for dependency to recover or implement a circuit breaker that gracefully degrades when downstream fails." |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset
<!-- STANDARD: 3min -->

- **Ships are processes, not events.** A launch is not the moment you click deploy. It is the weeks of preparation, the staged rollout, the monitoring vigil, the go/no-go decision, and the post-launch retro. Treat the deploy button as step 7 of 20, not the finish line.
- **Blast radius is everything.** The difference between a bad launch and a catastrophe is blast radius. Start with 1% of traffic, then 5%, then 25%. At each stage, let the metrics stabilize for at least 15 minutes before expanding. A bug affecting 1% of users is a ticket; a bug affecting 100% is a SEV-1.
- **Feature flags are safety belts, not just feature toggles.** Every flag should have: a kill switch, an owner, a sunset date, and a monitoring dashboard. A flag without these four things is a time bomb disguised as a feature toggle.
- **Go/no-go decisions are data-driven, not calendar-driven.** "It is Tuesday, so we must ship" is how you cause incidents. If the metrics are red, the answer is no-go regardless of the calendar. Ship when it is safe, not when it is scheduled.
- **Rollback is a feature, not a failure.** Designing for rollback (feature flags, backward-compatible schemas, blue-green deploys) is engineering excellence. If you cannot rollback in under 5 minutes, your launch is under-prepared.

## Operating at Different Levels
<!-- STANDARD: 3min -->

- **Quick scan (30s):** Check launch checklist status, verify staging is green, confirm on-call schedule, check error budgets, review the kill switch for the primary feature flag.
- **Standard engagement (10min):** Review pre-launch checklist completion, verify monitoring dashboards show staging data, confirm rollback procedure is documented and tested, validate go/no-go criteria against current metrics.
- **Deep dive (full session):** Full launch readiness audit: run through every checklist item with evidence, review staged rollout percentages and stabilization periods, validate feature flag lifecycle (creation through deprecation), dry-run rollback in staging, draft launch communication for stakeholders and users.
- **Crisis mode (launch going badly):** Execute rollback immediately if any go/no-go threshold is breached. Do not debug in production. Rollback first, investigate in staging later. Communicate status to stakeholders within 5 minutes of rollback decision.

## When to Use
<!-- STANDARD: 3min -->

- Preparing a new feature or service for production launch
- Designing a staged rollout strategy with defined percentages and stabilization periods
- Setting up feature flags with proper lifecycle management (dark launch, beta, GA, deprecate, remove)
- Creating pre-launch checklists covering code quality, security, performance, accessibility, infrastructure, and documentation
- Defining go/no-go criteria with specific metric thresholds
- Setting up launch-day monitoring dashboards and alert thresholds
- Writing launch communication templates for stakeholders, support teams, and users
- Planning rollback procedures and verifying they work before launch

**When NOT to use:** CI/CD pipeline automation (ci-cd-builder), release calendar management (release-manager), live incident response (incident-responder), or performance optimization (performance-engineer).

## Route the Request
<!-- STANDARD: 3min -->

```
What launch activity are you working on?
|-- Building a pre-launch checklist -> Start at "Core Workflow: Phase 1 - Pre-Launch Checklist"
|-- Designing staged rollout -> Jump to "Decision Trees: Staged Rollout"
|-- Setting up feature flags -> Jump to "Decision Trees: Feature Flag Lifecycle"
|-- Defining go/no-go criteria -> Jump to "Decision Trees: Go/No-Go Criteria"
|-- Planning rollback -> Jump to "Decision Trees: Rollback Strategy"
|-- Launch day monitoring -> Jump to "Decision Trees: Launch Monitoring"
|-- Writing launch communication -> Go to "Core Workflow: Phase 3 - Launch Communication"
|-- Full launch readiness audit -> Start at "Core Workflow: Phase 1"
```

## Core Workflow **(STANDARD)**
<!-- STANDARD: 3min -->

### Phase 1: Pre-Launch Checklist

```
1. CODE QUALITY GATE
   |-- All PRs reviewed and approved by at least 2 engineers
   |-- No outstanding "blocking" review comments
   |-- All tests passing (unit, integration, e2e) on the release commit
   |-- Code coverage meets project threshold (>80% for critical paths)
   |-- No TODOs or FIXMEs in changed files without tracking tickets
   |-- Linting and formatting checks pass with zero warnings
   |-- Dependency audit: no known CVEs in direct or transitive dependencies

2. SECURITY GATE
   |-- Security review completed for auth, data access, and input validation
   |-- No secrets in code, config, or environment variables
   |-- API endpoints have appropriate rate limiting
   |-- New data stores have encryption at rest enabled
   |-- PII handling reviewed: data minimization, retention policy, access controls
   |-- OWASP Top 10 checks: injection, broken auth, sensitive data exposure, XXE, access control

3. PERFORMANCE GATE
   |-- Load test results: target RPS achieved with p95 latency under SLO
   |-- Memory profile: no leaks under sustained load (>1 hour)
   |-- Database query plans reviewed for new queries, indexes confirmed
   |-- Cold start time (if serverless) under acceptable threshold
   |-- Bundle size (if frontend): no regression vs baseline, lazy loading verified

4. ACCESSIBILITY GATE
   |-- Automated a11y audit: zero critical or serious violations (axe-core)
   |-- Keyboard navigation verified for all new interactive elements
   |-- Screen reader testing completed for critical user flows
   |-- Color contrast meets WCAG 2.2 AA minimum (4.5:1 for text)
   |-- Focus management verified for modal dialogs, route changes, and dynamic content

5. INFRASTRUCTURE GATE
   |-- Infrastructure as Code (IaC) changes reviewed and applied
   |-- Resource limits and autoscaling configured for expected traffic
   |-- Circuit breakers and retry policies configured for downstream calls
   |-- Health check endpoints defined and responding correctly
   |-- DNS, TLS certificates, and load balancer configuration verified
   |-- Database migrations tested with production-scale data volume

6. DOCUMENTATION GATE
   |-- API documentation updated with new/changed endpoints
   |-- Runbook updated with new alerts and troubleshooting steps
   |-- Architecture Decision Records (ADRs) created for significant decisions
   |-- Changelog entry written for user-facing changes
   |-- Internal wiki updated: onboarding, setup, common issues
```

  Complete when: all 6 gates (code quality, security, performance, accessibility, infrastructure, documentation) have zero failing CRITICAL items signed off by the release commander.

### Phase 2: Staged Rollout

```
1. DARK LAUNCH (0% USERS, 100% TRAFFIC MIRRORED)
   |-- Deploy to production with feature flag OFF
   |-- Mirror a percentage of production traffic to new code path
   |-- Compare responses: new vs old for correctness
   |-- Duration: 24 hours minimum
   |-- Success criteria: zero discrepancies in mirrored responses

2. CANARY (1-5% USERS)
   |-- Enable feature flag for 5% of users
   |-- Monitor: error rate, latency, business metrics for 30 minutes
   |-- Compare canary cohort vs control cohort on all metrics
   |-- Automatic rollback if: error rate >2x baseline OR p95 latency >3x baseline
   |-- Duration: 2-4 hours minimum before expanding

3. BETA ROLLOUT (25% USERS)
   |-- Expand to 25% of users
   |-- Monitor for 2 hours minimum, watching for delayed failures
   |-- Check: database load, cache hit rates, queue depths, CPU/memory
   |-- Support team briefed on new feature, known issues documented
   |-- Success criteria: all metrics within 20% of baseline for 1 hour

4. MAJORITY ROLLOUT (50% USERS)
   |-- Expand to 50% of users
   |-- Monitor for 4 hours, covering at least one peak traffic period
   |-- Validate: billing, data integrity, external integrations
   |-- Success criteria: zero SEV-3+ incidents, all SLOs met

5. GENERAL AVAILABILITY (100% USERS)
   |-- Expand to 100% of users
   |-- Keep feature flag as kill switch for 2 weeks minimum
   |-- Schedule flag removal ticket for 2-4 weeks post-launch
   |-- Post-launch retro scheduled within 1 week
```

  Complete when: canary metrics are within baseline for error rate and latency at each stage, dark launch shows zero discrepancies in mirrored responses, and the feature flag kill switch is confirmed operational.

### Phase 3: Launch Communication

```
1. PRE-LAUNCH (24-48 HOURS BEFORE)
   |-- Stakeholder email: launch date, feature summary, rollback plan, POC
   |-- Support team: training on new feature, FAQ, known limitations, escalation path
   |-- Marketing/blog: draft announcement, screenshots, user benefits
   |-- Sales: pricing changes, competitive positioning, demo script

2. LAUNCH DAY
   |-- Status page updated: scheduled maintenance window (if applicable)
   |-- Internal Slack/Teams: launch commencing, link to dashboard, escalation POC
   |-- Real-time updates at each rollout stage (5% complete, 25% complete, etc.)
   |-- Go/no-go call at each stage transition

3. POST-LAUNCH (WITHIN 24 HOURS)
   |-- Launch summary: metrics, incidents, user feedback, lessons learned
   |-- Retro scheduled: what went well, what did not, action items with owners
   |-- Support handoff: known issues, workarounds, escalation criteria
   |-- Feature flag cleanup ticket created with owner and deadline
```

  Complete when: stakeholder email is sent, support team is trained with FAQ and escalation path, launch day communication template is ready, and feature flag cleanup ticket is assigned with a deadline.
  Complete when: Pipeline runs end-to-end in under 15 minutes with parallelized stages.
  Complete when: Rollback tested — can revert to previous version within 5 minutes of detection.
  Complete when: Secrets scan runs in CI and blocks merge on any detected credential.
  Complete when: Infrastructure drift detection enabled — Terraform plan shows zero unmanaged changes.
  Complete when: Runbook documented and tested via game day exercise with < 3 action items.

## Decision Trees **(QUICK)**
<!-- STANDARD: 3min -->

### Staged Rollout

```
What is the risk profile of this change?
|-- LOW RISK: Config change, copy update, CSS-only visual tweak
|   |-- 50% canary for 15 minutes -> 100%
|   |-- Rollback: revert config or deploy previous version
|   |-- Minimal monitoring: error rate, page load time
|-- MEDIUM RISK: New API endpoint, backend refactor, new UI component
|   |-- Dark launch 24h -> 5% for 2h -> 25% for 4h -> 100%
|   |-- Rollback: feature flag off
|   |-- Full monitoring suite: error rate, latency, throughput, business metrics
|-- HIGH RISK: Database migration, auth change, payment flow, data model change
|   |-- Dark launch 48h -> 1% for 4h -> 5% for 8h -> 25% for 24h -> 100%
|   |-- Rollback: feature flag off + backward-compatible schema
|   |-- Extended monitoring: data integrity checks, reconciliation jobs, customer support volume
|-- CRITICAL RISK: Multi-service rewrite, identity system change, compliance-related
|   |-- Dark launch 1 week -> 0.1% for 24h -> 1% for 2d -> 5% for 1 week -> 25% for 1 week -> 100%
|   |-- Rollback: full blue-green deployment with traffic shifting
|   |-- War room staffed for first 24 hours of each expansion phase
```

### Feature Flag Lifecycle

```
Phase 1: CREATION
|-- Flag created in feature flag system (LaunchDarkly, Split, Unleash, custom)
|-- Default: OFF for all users
|-- Owner assigned, sunset date set (default: 60 days from creation)
|-- Kill switch mechanism verified: env var or admin API
|-- Monitoring dashboard linked to flag

Phase 2: DARK LAUNCH
|-- Code deployed to production with flag OFF
|-- Internal testing: team members, QA, product
|-- No user-facing impact
|-- Duration: until internal sign-off complete

Phase 3: BETA / STAGED ROLLOUT
|-- Flag enabled for percentage or targeted user segments
|-- Monitoring: flag-specific dashboard showing flag-on vs flag-off cohorts
|-- Feedback loop: support tickets, user interviews, analytics
|-- Duration: 1-4 weeks depending on risk

Phase 4: GENERAL AVAILABILITY
|-- Flag ON for 100% of users
|-- Flag remains as kill switch (emergency off-ramp)
|-- Duration: 2-4 weeks minimum before considering removal

Phase 5: DEPRECATION
|-- Flag removal ticket created with deadline
|-- Code cleanup: remove flag checks, dead code paths
|-- Tests updated: remove flag-specific test cases
|-- Duration: 1-2 weeks after GA stabilization

Phase 6: REMOVAL
|-- Flag deleted from feature flag system
|-- All flag-checking code removed from codebase
|-- Monitoring dashboards archived or removed
|-- Sunset complete
```

### Go/No-Go Criteria

```
Technical Criteria (ALL must be GREEN):
|-- All automated tests passing on release commit
|-- Staging environment healthy with production-like data
|-- No critical or high-severity CVEs in dependencies
|-- Load test: target RPS achieved with p95 < SLO
|-- No known P0/P1 bugs in the release

Operational Criteria:
|-- Error budget remaining: >50% for high-risk, >20% for medium-risk
|-- On-call engineer scheduled and available during launch window
|-- Rollback procedure tested in staging within last 7 days
|-- All feature flags have verified kill switches
|-- Monitoring dashboards show staging data (not empty)

Business Criteria:
|-- Support team trained and briefed on new feature
|-- Documentation published (API docs, help center, FAQs)
|-- Legal/compliance approval obtained (if applicable)
|-- Marketing/sales materials ready for external launch
|-- No conflicting launches or maintenance windows scheduled

Go/No-Go Decision Matrix:
| Condition | Status | Action |
|-----------|--------|--------|
| Any Technical RED | NO-GO | Fix issues, re-run checklist from failed item |
| Any Operational RED | NO-GO (unless VP approval) | Address gaps or escalate |
| All GREEN | GO | Proceed to Phase 2: Staged Rollout |
```

### Rollback Strategy

```
Rollback Decision Triggers (any ONE = ROLLBACK):
|-- Error rate exceeds 2x baseline for more than 5 minutes
|-- p95 latency exceeds 3x baseline for more than 5 minutes
|-- Business metric drops >10% (conversion, checkout, signups)
|-- Customer-reported SEV-2 incident related to the launch
|-- Data integrity issue detected (wrong data written, duplicates)
|-- Security vulnerability discovered in production

Rollback Methods (fastest to slowest):
|-- FEATURE FLAG OFF: Instant (seconds). Best for feature-gated changes.
|   |-- flip flag to OFF in feature flag dashboard
|   |-- No deploy needed, takes effect on next evaluation (usually <60s)
|   |-- Verify: error rate returns to baseline
|-- REVERT DEPLOY: 5-15 minutes. Best for non-flagged changes.
|   |-- Deploy previous known-good version
|   |-- git revert <bad-commit> && deploy
|   |-- Verify: health checks pass, metrics return to baseline
|-- BLUE-GREEN TRAFFIC SHIFT: 1-5 minutes. Best for infrastructure changes.
|   |-- Shift 100% traffic back to green (old) environment
|   |-- Blue (new) environment kept for debugging
|   |-- Verify: traffic serving from green, metrics normal
|-- DATABASE ROLLBACK: 30min-2hours. Last resort.
|   |-- Restore from pre-migration snapshot
|   |-- Replay any legitimate transactions during migration window
|   |-- Verify: data integrity checks pass

Rollback Runbook Template:
  1. Decision: [trigger that caused rollback]
  2. Time of decision: [timestamp]
  3. Method: [feature flag / revert deploy / blue-green / DB rollback]
  4. Executor: [name of engineer executing rollback]
  5. Verification: [metrics checked, values observed]
  6. Communication: [who was notified, channels used]
  7. Post-mortem: [ticket link for root cause analysis]
```

### Launch Monitoring

```
Essential Dashboards (create BEFORE launch):
|-- ERROR RATE: 5xx count / total requests, per endpoint, per status code
|   |-- Alert: >2x baseline for 5 minutes
|-- LATENCY: p50, p95, p99 per endpoint
|   |-- Alert: p95 >3x baseline for 5 minutes
|-- THROUGHPUT: requests per second, per endpoint
|   |-- Alert: >50% drop (indicates routing/load balancer issue)
|-- SATURATION: CPU, memory, connection pool, thread pool, queue depth
|   |-- Alert: CPU >80%, connection pool >90%, queue depth >1000
|-- BUSINESS METRICS: signups, purchases, API calls, feature adoption
|   |-- Alert: >10% drop from baseline
|-- FEATURE FLAG METRICS: flag evaluation count, flag-on vs flag-off cohort comparison
|   |-- Alert: flag evaluation errors >1%

Launch War Room Setup (for high/critical risk launches):
|-- Dedicated video call or chat channel
|-- Required attendees: launch engineer, on-call engineer, product manager
|-- Optional: engineering manager, SRE, dependency team POCs
|-- Shared screen: main monitoring dashboard
|-- Timeline document: real-time log of events, decisions, metrics
|-- Communication: status updates every 15 minutes to stakeholders
```

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Launching on a Friday at 5 PM — if something breaks, the on-call engineer is alone, tired, and has no escalation path until Monday morning | $50K-$300K in extended outage over a weekend with no senior engineers available | Schedule launches for Tuesday-Thursday mornings; never launch before a holiday or weekend; ensure at least 2 engineers are available for the first 4 hours post-launch |
| Dark launching with 1% mirrored traffic but never comparing responses — the dark launch runs for 24 hours "successfully" but the new code returns 500s on 3% of mirrored requests because no one checked the comparison | $20K-$100K in deploying broken code that was "verified" by dark launch | Dark launch must include automated response comparison: diff old vs new responses, alert on any discrepancy > 0%; a dark launch without comparison is just warming CPUs |
| Killing a feature flag after 2 weeks without checking if the flag is still referenced in code — removing the flag key crashes the application for users who had it cached | $10K-$50K in production crash from stale flag references | Keep flags as kill switches for minimum 2 weeks post 100% rollout; before removal, grep the entire codebase for the flag key; schedule flag removal as a separate deploy, not bundled with feature work |

## Error Decoder — War Stories from the Trenches
<!-- STANDARD: 3min -->

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Staged rollout at 5% shows green metrics — at 50%, error rate jumps to 12% because the new code path hits a different DB query that was never load tested | The 5% cohort was only 200 users — all in a single geographic region hitting the same read replica. The query plan used the covering index fine. At 50% (20,000 users), the query planner switched to a sequential scan because the index statistics shifted. The 5% test never exercised the query at the scale that triggers the planner change | Add a load-generation step at each rollout stage: 5% users + 95% synthetic traffic to simulate full load. Run `EXPLAIN ANALYZE` on both the old and new query plans with production-scale data volumes. Extend canary bake time to cover peak traffic hours (at least 2 full traffic cycles) | Query planner behavior changes at scale thresholds, not at user-percentage thresholds. A 5% canary on a 1M-user system is still only 50K users — below the threshold where the planner switches from index scan to seq scan. Synthetic load fills the gap between small canary and full production. |
| Feature flag kill switch doesn't work — flipping the flag to OFF still routes 8% of users to the broken code path because of CDN cache | The kill switch is a LaunchDarkly flag evaluated client-side. But the application's CDN caches full-page responses for 5 minutes. After the flag is killed, users with cached pages continue executing the old code for up to 5 minutes. The kill switch "took effect" immediately, but the cached pages don't re-evaluate the flag | Add a `Cache-Control: no-cache` header on pages that evaluate feature flags. Use server-side flag evaluation with edge-level flag delivery (Cloudflare Workers + LaunchDarkly SDK at the edge). Implement a secondary kill mechanism: an S3 object that every page fetch checks — bypasses CDN cache entirely | Kill switches must be faster than your longest cache TTL. A client-side flag behind a CDN with 5-minute caching has a 5-minute kill latency. Server-side evaluation at the edge eliminates the CDN cache dependency. Always have a bypass mechanism — a simple file check that no cache layer can ignore. |
| Pre-launch checklist shows 6 green gates — but the "performance" gate was tested against a staging database with 100 rows, not production's 500M rows | The performance test ran in staging with a database clone from production — but the clone was last refreshed 11 months ago. Since then, production grew from 500K to 500M rows. The query that took 12ms in staging takes 28 seconds in production because the index no longer fits in memory | Enforce a staging data freshness SLA: the staging database clone must be refreshed within 7 days of production for pre-launch testing. Add a row-count comparison check: `SELECT count(*)` in both staging and production — refuse to run performance tests if staging has < 50% of production's row count | Staging environments drift from production at the rate of production data growth. A database clone from 11 months ago tests queries against data volumes 3 orders of magnitude smaller. Pre-launch performance testing is only valid if staging mirrors production data scale. |
| Launch monitoring dashboard shows all green — 2 hours later, error budget is exhausted because the dashboard showed fleet averages, not per-endpoint breakdowns | The dashboard displayed P95 latency and error rate for ALL endpoints combined. The new `/checkout` endpoint had 40% error rate, but `/status` (called 100× more often) had 0% errors. The fleet-wide error rate was 0.4% — below the 1% threshold. The per-endpoint failure was invisible at fleet granularity | Break down launch dashboards by endpoint, not by service. Add a per-endpoint error budget burn alert: `rate(http_requests_total{endpoint="/checkout", status=~"5.."}[5m]) / rate(http_requests_total{endpoint="/checkout"}[5m]) > 0.05`. Display the top-5 error-contributing endpoints on the launch-day dashboard | Fleet-wide metrics hide endpoint-level disasters. A low-traffic endpoint with a 40% error rate is invisible in a fleet average flooded by a high-traffic healthy endpoint. Launch monitoring must slice by endpoint — every endpoint is a separate reliability surface. |
| Rollback completes in 3 minutes but the on-call engineer wakes up at 4 AM to find the database migration wasn't rolled back — the deploy reverted but the schema change persisted | The deploy rollback (`kubectl rollout undo`) reverted the application version. But the release included a database migration that added a `NOT NULL` column. The old application code doesn't know about the new column and INSERTs fail because it doesn't supply a value. The migration was applied forward but never reversed | Every release must include BOTH forward and reverse migration scripts. The reverse migration is tested in staging as part of the rollback drill. For irreversible schema changes (added NOT NULL column), the release is tagged DEPLOY-ROLLBACK-ONLY — the schema change is separated into a follow-up release with its own rollback plan | Application rollback and database rollback are independent operations. `kubectl rollout undo` reverts code; it does not revert schema. Writes that hit new columns with old code fail silently or noisily. Always pair every migration with a tested reverse migration — and if reversal is impossible, the deploy and the schema change must be separate releases. |
| Launch communication goes out on Slack at 10 AM — customers start reporting issues at 10:03 but the support team hasn't been briefed and tells customers "we're investigating" for 2 hours | The launch-day communication plan included stakeholder updates and a status page banner. But the support team wasn't on the distribution list. When customers reported issues, the support team had no context — they didn't know a launch was happening, didn't have the new feature's known-limitations doc, and escalated every ticket to engineering | Add the support team to the launch comms distribution 48 hours before launch. Create a "support brief" document: what's changing, known limitations, troubleshooting steps, escalation path. Run a 15-minute support briefing call 24 hours before launch. During the launch, have an engineering liaison in the #support-escalation channel | Support is the front line of every launch. Customers report issues to support, not to engineering. If support doesn't know a launch is happening, every customer report becomes a SEV1 escalation. Brief support before launch — they're your first responders. |

## Best Practices
<!-- STANDARD: 3min -->

1. **Pre-launch checklist as a non-negotiable gate — not a suggestion.** Six mandatory gates: Code Quality (PRs approved, tests passing, no TODOs), Security (no CVEs, rate limiting, encrypted data), Performance (load tested, no memory leaks, query plans reviewed), Accessibility (zero critical a11y violations, keyboard nav verified), Infrastructure (IaC reviewed, autoscaling configured, health checks defined), Documentation (API docs updated, runbooks current, ADRs created). All six must show GREEN before any user sees the change.

2. **Go/no-go criteria with specific, measurable thresholds — never "it feels ready."** CRITICAL (any NO = NO-GO): all automated tests pass, security scan clean, no known P0/P1 bugs, rollback tested in last 7 days, error budget ≥30% remaining. CONDITIONAL (NO = documented VP-level risk acceptance): feature flags configured with kill switches, monitoring dashboards with ≥24h baseline data, support team briefed, DB migrations tested at scale. Decision deadline: 24 hours before launch.

3. **Rollback automation: one command, under 5 minutes, tested within 7 days of launch.** A feature-flag kill switch takes effect in <60 seconds without a deploy. A deploy rollback (`kubectl rollout undo`, `terraform destroy -target`, blue-green swap) completes in <15 minutes. The runbook must work from a fresh terminal with zero local state. Dry-run in staging and time it. If the runbook fails, the launch is NO-GO.

4. **Launch communication: pre-launch, launch-day, post-launch — three distinct templates.** Pre-launch (24-48h before): stakeholder email with launch date, feature summary, rollback plan, escalation POC. Launch-day: status page update, internal Slack announcements at each rollout stage transition with go/no-go call. Post-launch (within 24h): launch summary with metrics, incident log, lessons learned, retro scheduled. Honesty in communication — never call an outage "routine maintenance."

5. **Post-launch monitoring: 24-72 hours of active vigilance with annotated dashboards.** Watch error rates, latency (p50/p95/p99), throughput, saturation, and business metrics against the 7-day baseline. Dashboards must exist with baseline data at least 1 week before launch — an annotated launch timestamp tells you whether the launch caused the anomaly or inherited it. The launch commander stays on-call for the full monitoring window.

6. **Phased rollouts with minimum stabilization periods per stage.** Dark launch (0% users, 100% mirrored traffic, 24h minimum) for data-mutating changes. Canary (5%, 30-min stabilization) → Beta (25%, 2h stabilization) → Majority (50%, 4h stabilization covering one peak period) → GA (100%, keep flag as kill switch for 2 weeks). Each stage has automatic rollback thresholds: error rate >2x baseline or p95 latency >3x baseline triggers immediate abort.

7. **Dark launch every data-mutating change — never write to production without validating first.** Mirror production traffic to a shadow write path for 24-48 hours. Compare new vs. old responses for correctness. Validate data integrity before enabling real writes. The first time your code touches real data should not be the first time it runs in production. Skipping dark launch on a data pipeline change that writes 2M malformed records costs $20K-$100K in recovery.

8. **Feature flags require four things: owner, sunset date, kill switch, monitoring dashboard.** A flag without an owner is orphaned the moment the creator changes teams. A flag without a sunset date lives forever — 6 months later, the "off" code path has rotted and the kill switch triggers a 2-hour outage. A flag without a kill switch turns a 1-minute fix into a 30-minute deploy. A flag without a dashboard is flying blind.

9. **Error budgets are launch gates, not just SRE abstractions.** If remaining error budget is <30% for a service in the launch blast radius, the launch is NO-GO for that service. Launching into an exhausted error budget guarantees immediate SLO violation. The error budget policy must be documented: ≥50% = normal ops, 20-50% = risky deploys blocked, 5-20% = all deploys blocked, <5% = full freeze.

10. **Post-launch retro within 1 week: small, blame-free, action-oriented.** Three questions: What went well? What went wrong? What do we change for next launch? Produce ≤5 concrete action items with owners and dates. Track retro action item completion rate across launches — the metric that measures whether your launch process is actually improving. A retro without tracked action items is therapy, not engineering.

## Error Recovery **(STANDARD)**
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| CI/CD pipeline for staged rollout | ci-cd-builder | Pipeline must support canary deployment, traffic shifting, and automatic rollback triggers |
| Pre-launch security audit | security-reviewer | OWASP checks, dependency audit, secret scanning, auth review |
| Load testing and performance baseline | performance-engineer | Establish baseline metrics, run soak tests, validate SLO targets |
| Accessibility audit before launch | accessibility-auditor | WCAG 2.2 AA compliance, screen reader testing, keyboard navigation |
| Incident response if launch goes bad | incident-responder | Handoff procedure, escalation path, shared war room |
| Release coordination and calendar | release-manager | Scheduling launch window, avoiding conflicts, stakeholder communication |
| Monitoring and alerting setup | observability-engineer | Dashboard creation, alert thresholds, SLO tracking |
| Feature flag infrastructure | platform-engineer | Flag system availability, kill switch reliability, flag evaluation performance |

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `cloud-architect` | Infrastructure design, networking, IAM, cost model | Before provisioning infrastructure or designing deployment pipelines |
| `ci-cd-builder` | Pipeline design, build optimization, deployment strategies | Before designing CI/CD workflows |
| `automation-engineer` | Launch checklist, rollback plan, comms timeline | Before automating launch delivery pipelines |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|
| `automation-engineer` | Launch checklist, rollback plan, comms timeline | Launch without automation — manual errors |

## Proactive Triggers
<!-- STANDARD: 3min -->

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | Launch checklist has unverified items within 1 hour of scheduled launch | [ALERT] Unverified checklist items: [list]. Resolve or reschedule launch. |
| P2 | Error budget below 50% and launch is high-risk | [WARN] Error budget at [X]%. Consider reducing blast radius or waiting for budget recovery. |
| P3 | Feature flag older than 60 days found in codebase | [ALERT] Flag [name] has exceeded its sunset date. Schedule removal within 2 weeks or extend with justification. |
| P4 | No staging deploy in last 48 hours before production launch | [ALERT] Staging has not been validated recently. Deploy and run smoke tests before production launch. |
| P5 | Go/no-go criteria document references metrics without dashboards | [WARN] No dashboard found for metric [name]. Create dashboard before relying on it for go/no-go decisions. |

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## Production Checklist **(STANDARD)**
<!-- STANDARD: 3min -->

- [ ] **[SHIP1]** Pre-launch checklist: all 6 gates (Code Quality, Security, Performance, Accessibility, Infrastructure, Documentation) show GREEN — no exceptions, no "will fix after launch"
- [ ] **[SHIP2]** Rollback procedure tested in staging within the last 7 days, timed at <5 minutes for feature flag and <15 minutes for deploy rollback — runbook works from a fresh terminal with zero local state
- [ ] **[SHIP3]** Feature flags: every flag has an owner, a sunset date (max 60 days post-GA), a runtime kill switch (<60 second effect, no deploy required), and a linked monitoring dashboard
- [ ] **[SHIP4]** Staged rollout plan documented with percentages and minimum stabilization periods: dark launch (0%, 24h), canary (5%, 30min), beta (25%, 2h), majority (50%, 4h), GA (100%)
- [ ] **[SHIP5]** Automatic rollback thresholds configured: error rate >2x baseline OR p95 latency >3x baseline triggers immediate abort at every rollout stage
- [ ] **[SHIP6]** Monitoring dashboards exist with ≥24 hours of baseline data: error rate, latency (p50/p95/p99), throughput, saturation, business metrics — launch timestamp annotated on all dashboards
- [ ] **[SHIP7]** Go/no-go criteria documented with specific metric thresholds, signed off by engineering lead and product manager — decision deadline 24 hours before deploy window
- [ ] **[SHIP8]** Stakeholder communication: pre-launch email sent 24-48h before, support team briefed with FAQ and escalation path, status page template prepared
- [ ] **[SHIP9]** On-call coverage confirmed: engineer scheduled and available for full launch window plus 2 hours after final expansion — no Friday after 2pm launches without VP approval and 24/7 on-call
- [ ] **[SHIP10]** Dark launch completed for all data-mutating changes: mirrored traffic validated for 24-48 hours, data integrity verified before enabling real writes
- [ ] **[SHIP11]** Error budget check: all services in the launch blast radius have ≥30% remaining error budget — services with exhausted budgets require VP-level risk acceptance
- [ ] **[SHIP12]** Post-launch retro scheduled within 1 week: 3 questions, ≤5 action items with owners and dates, tracked action item completion rate from previous launches
- [ ] **[SHIP13]** Launch timeline published: pre-launch (T-48h), dark launch (T-24h), canary (T+0), beta (T+2h), majority (T+4h), GA (T+8h), monitoring window (T+8h to T+72h)
- [ ] **[SHIP14]** Feature flag cleanup tickets created: one per flag, assigned to flag owner, due within 30 days of 100% rollout — CI enforces cleanup within 60 days

## What Good Looks Like
<!-- STANDARD: 3min -->

```
LAUNCH: Personalized recommendations engine

Pre-launch (T-48h):
  - All 6 checklist gates GREEN
  - Staged rollout plan: 5%(2h) -> 25%(4h) -> 50%(8h) -> 100%
  - Rollback: feature flag kill switch (instant)
  - Monitoring: 4 dashboards (error, latency, business, flag-specific)
  - On-call: Alice (primary), Bob (secondary)
  - Communication: stakeholder email sent, support briefed

Launch day:
  09:00 - Deploy to production (flag OFF) -- DARK LAUNCH
  09:05 - Enable for 5% -- metrics nominal
  09:35 - Go decision: expand to 25%
  11:45 - Go decision: expand to 50%
  16:00 - p95 latency spike: 450ms -> 800ms (threshold: 900ms)
  16:05 - Root cause: cold cache for new recommendation model
  16:10 - Cache warmed, latency returns to 480ms
  16:30 - Go decision: expand to 100%
  17:00 - Launch complete. Metrics all green.

Bad alternative (anti-pattern):
  - Deploy at 22:00 Friday (no on-call)
  - 100% rollout immediately (no staged rollout)
  - No kill switch (must revert deploy)
  - No dashboards (discover issues from user complaints)
  - Latency spikes at midnight, SEV-1 called, on-call paged at home
  - Rollback takes 20 minutes because CI pipeline is congested
```

## Deliberate Practice
<!-- STANDARD: 3min -->

1. **Checklist Gap Analysis:** Take the last 3 production incidents from your team's post-mortems. For each incident, identify which pre-launch checklist item would have caught it. If none would have, add a new checklist item. Run the updated checklist against the next launch.

2. **Rollback Dry Run:** Schedule a "fire drill" during business hours. Deploy a canary with a deliberate performance degradation (artificial sleep in an endpoint). Time how long it takes from alert firing to full rollback. Target: under 5 minutes for feature flag rollback, under 15 minutes for deploy rollback.

3. **Feature Flag Cleanup Sprint:** Audit your codebase for feature flags older than 60 days. For each: either schedule removal within 2 weeks (with code cleanup) or document the business justification for keeping it. Track flag count over time -- it should be a sawtooth pattern, not monotonic growth.

4. **Go/No-Go Simulation:** Build a table-top exercise with your team. Present a launch scenario with mixed signals (one metric red, others green). Have each team member vote go/no-go with justification. Discuss disagreements. Align on decision-making principles.

5. **Launch Communication Template:** Draft a launch communication for a fictional major outage during a launch. Include: what happened, user impact, current status, estimated resolution, workaround, next update time. Practice delivering it in under 3 minutes. Then draft the post-launch retro summary.

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "Friday 5pm deploy — what could go wrong? We'll check it Monday." | Saturday morning traffic patterns differ from weekday testing. A latent bug surfaces, nobody monitors, and the first alert is a customer tweet 8 hours later. $15K-$50K in weekend emergency response, trust damage, and SLA credits. |
| "We'll add the runtime kill switch in the next iteration — the feature works." | Feature causes 5x latency spike. The flag is a build-time constant, not a runtime toggle. Fix requires: new build (25 min CI) + deploy = 30+ minutes of degraded experience. $3K-$8K per incident when a 60-second toggle would have sufficed. |
| "Dark launching is overkill for a small data pipeline change." | New pipeline writes 2M malformed records to the production database before detection. Recovery = 8 hours of point-in-time restore and reconciliation. $20K-$100K in engineering time and potential data integrity issues. |
| "Feature flags are temporary — no need for a removal process." | Flag at 100% for 6 months. 40 commits later, someone refactors the "off" code path. Database migration failure triggers emergency toggle back to 0% — all users hit broken code, 2-hour outage. $50K-$250K per stale-flag incident. |
| "Manual go/no-go based on the team's gut feel is faster than formal process." | A green test suite means "nothing we predicted broke," not "nothing broke." Go/no-go without production canary data is gambling. $50K-$500K in incident response and lost revenue per judgment-error release. |

## Anti-Patterns
<!-- STANDARD: 3min -->

- **Launching on Friday at 5pm guarantees a weekend incident.** A team deploys a major feature Friday afternoon and leaves for the weekend. A latent bug surfaces Saturday morning when traffic patterns differ from weekday testing. No one is monitoring, and the first alert comes from a customer tweet 8 hours later. **Total cost: $15,000-$50,000 in weekend emergency response, customer trust damage, and potential SLA credits.** Fix: Launch Tuesday-Thursday before 2pm. Never launch on Friday without explicit executive approval and 24/7 on-call coverage.

- **A feature flag without a kill switch turns a 1-minute fix into a 30-minute deploy.** A feature causes a 5x latency spike. The engineer tries to disable the flag but discovers it was hardcoded as a build-time constant, not a runtime toggle. They must cut a new build, wait for CI (25 minutes), and deploy before users see relief. **Total cost: $3,000-$8,000 in degraded user experience and emergency engineering time per incident.** Fix: Every feature flag must have a runtime kill switch (env var, remote config, or admin API) that takes effect within 60 seconds without a deploy.

- **Skipping dark launch causes data corruption at scale.** A new data pipeline writes malformed records to the primary database. Without dark launch (mirroring traffic without persisting), the bug writes 2 million bad records to production before detection. Recovery requires 8 hours of point-in-time restore and data reconciliation. **Total cost: $20,000-$100,000 in engineering time, data recovery, and potential customer-facing data issues.** Fix: Dark launch every data-mutating change. Mirror write traffic to a shadow table for 24-48 hours. Validate data integrity before enabling real writes.

- **Staged rollout percentages that skip from 1% to 100% defeat the purpose.** A team enables a feature for 1% of users, sees no issues for 10 minutes, and jumps to 100%. A database connection pool leak that only manifests under sustained load (needing 15+ minutes at scale) is missed. The pool exhausts at 100% traffic, causing a complete outage. **Total cost: $10,000-$30,000 in outage impact and remediation.** Fix: Each rollout stage must run long enough to observe steady-state behavior. Minimum stabilization periods: 5% for 30min, 25% for 2h, 50% for 4h, 100% with flag as kill switch for 2 weeks.

- **Monitoring dashboards set up on launch day show no historical baseline.** An engineer creates dashboards 30 minutes before launch. When metrics show 200 errors/minute after rollout, there is no baseline to compare against. The team wastes 45 minutes debating whether 200 errors/minute is normal (it was 10/minute before the launch). **Total cost: $2,000-$5,000 in delayed detection and wasted diagnosis time.** Fix: Create monitoring dashboards at least 1 week before launch. Establish baseline metrics from staging and production (pre-feature). Annotate the launch event on all dashboards.

- **Rollback runbook that has never been tested fails when needed.** The documented rollback procedure says "run rollback.sh". On launch day, the engineer discovers rollback.sh requires a specific Python version not installed on the production jump host. The 3-minute procedure takes 25 minutes while they find the right environment. **Total cost: $8,000-$25,000 in extended incident duration.** Fix: Dry-run the rollback procedure in a production-like environment within 7 days of launch. Time it. Document the exact environment prerequisites. The runbook should work from a fresh terminal with no local state.

- **Launch communication that blames "a routine deployment" erodes trust.** After a launch causes a 30-minute partial outage affecting 15% of users, the status page says "We performed routine maintenance." Users who could not access the service know this is false. Social media erupts with "routine maintenance = we broke something." **Total cost: Hard to quantify but significant -- customer churn, reputation damage, reduced feature adoption.** Fix: Be honest in launch communication. "We deployed [feature] and encountered an unexpected issue with [component]. We rolled back within [N] minutes. Full post-mortem will be published within 5 business days."

## Verification
<!-- STANDARD: 3min -->

- [ ] Pre-launch checklist: all 6 gates (Code Quality, Security, Performance, Accessibility, Infrastructure, Documentation) show GREEN
- [ ] Rollback procedure: tested in staging within last 7 days, timed at under 5 minutes for feature flag and under 15 minutes for deploy rollback
- [ ] Monitoring: dashboards exist for error rate, latency (p50/p95/p99), throughput, saturation, and business metrics, with at least 24 hours of baseline data
- [ ] Feature flags: every flag has an owner, a sunset date, a kill switch verified to work, and a linked monitoring dashboard
- [ ] Staged rollout plan: defined percentages with minimum stabilization periods, automatic rollback thresholds documented
- [ ] Go/no-go criteria: documented with specific metric thresholds, signed off by engineering lead and product manager
- [ ] Communication: stakeholder email sent, support team briefed, status page template prepared, launch timeline published
- [ ] On-call coverage: engineer scheduled and available for full launch window plus 2 hours after final expansion

## Verification Guardrails
<!-- STANDARD: 3min -->

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## References
<!-- STANDARD: 3min -->

- [LaunchDarkly Feature Flag Best Practices](https://launchdarkly.com/blog/) -- Feature flag management patterns and anti-patterns
- [Google SRE: Managing Risk](https://sre.google/sre-book/managing-risk/) -- Error budgets, SLOs, and risk-based launch decisions
- [Atlassian: Staged Rollout Guide](https://www.atlassian.com/continuous-delivery/principles/canary-deployments) -- Canary deployment strategies and patterns
- [Split.io: Feature Flag Lifecycle](https://www.split.io/blog/feature-flag-lifecycle-management/) -- Managing flags from creation to removal
- [PagerDuty: Incident Communication Templates](https://response.pagerduty.com/) -- Templates for stakeholder and customer communication during incidents
- [Keep a Changelog](https://keepachangelog.com/) -- Human-readable changelog format
- [references/core-workflow.md](references/core-workflow.md) -- Detailed pre-launch checklist and rollout execution guide
- [references/anti-patterns.md](references/anti-patterns.md) -- Launch anti-patterns with real-world case studies
- [references/best-practices.md](references/best-practices.md) -- Staged rollout and launch best practices
- [references/calibration.md](references/calibration.md) -- Risk calibration: how to match rollout strategy to change risk
- [references/checklist.md](references/checklist.md) -- Printable pre-launch checklist with evidence columns
- [references/error-decoder.md](references/error-decoder.md) -- Common launch failures decoded with root causes and fixes
- [references/footguns.md](references/footguns.md) -- Launch footguns: the most expensive mistakes and how to avoid them
- [references/scale-depth.md](references/scale-depth.md) -- Scaling launch discipline from startup to enterprise
