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
    - ci-cd-builder
    - qa-engineer
    - security-reviewer
    - performance-engineer
    - release-manager
  feeds_into:
    - incident-responder
    - release-manager
    - site-reliability-engineer
    - observability-engineer
  alternatives: []
---

# Shipping and Launch

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end shipping and launch discipline: pre-launch readiness verification, staged rollout execution, feature flag lifecycle management, rollback decision frameworks, and launch communication. Every launch is a calculated risk -- the goal is to reduce blast radius, detect problems before users do, and have a clear rollback path when things go wrong. Ships are not events; they are processes with gates, signals, and pre-rehearsed abort procedures.

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to launch without a verified rollback plan. Every launch must have a documented, tested rollback procedure. | Trigger: launch request is made AND no rollback.md or rollback runbook exists in the release artifacts | STOP. "No verified rollback plan exists. Every launch requires a tested rollback procedure. Document the rollback steps, verify they work in staging, and include rollback success criteria before proceeding." |
| R2 | DETECT when launch happens outside business hours without on-call coverage. Off-hours launches without support guarantee extended downtime. | Trigger: launch time is outside 9am-5pm local time AND no on-call engineer is scheduled AND feature is customer-facing | STOP. "Launching outside business hours without on-call coverage risks extended downtime. Either: (a) reschedule during business hours, (b) ensure an on-call engineer is available, or (c) confirm the blast radius is non-customer-facing." |
| R3 | REFUSE to skip staging environment validation. Production is not a testing environment. | Trigger: launch request AND no staging deploy in last 24 hours OR staging tests failed | STOP. "Staging has not been validated within 24 hours. Deploy to staging, run the full test suite and smoke tests, verify all checks pass, then proceed to production." |
| R4 | DETECT when error budget is exhausted before launch. Launching with a burned error budget guarantees violated SLOs. | Trigger: error budget remaining is less than 30% AND launch involves changes to high-traffic paths | STOP. "Error budget for [service] is at [X]%. Launching now risks immediate SLO violation. Either: (a) wait for error budget to recover, (b) reduce blast radius to non-critical paths, or (c) get explicit VP-level approval for error budget override." |
| R5 | REFUSE to launch without monitoring dashboards configured. You cannot detect problems you are not measuring. | Trigger: launch request AND no dashboards exist for key metrics (error rate, latency p50/p95/p99, throughput, saturation) | STOP. "No monitoring dashboards configured for [service/feature]. Create dashboards for: error rate, latency percentiles, throughput, and saturation. Set alert thresholds. Verify dashboards show data from staging." |
| R6 | DETECT when feature flag has no kill switch. Feature flags without a kill switch turn emergencies into outages. | Trigger: feature flag configuration lacks an emergency off-switch (environment variable, config toggle, or admin API) | STOP. "Feature flag [name] has no kill switch. Add an emergency disable mechanism that works WITHOUT a deployment -- environment variable, remote config toggle, or admin API that takes effect within 60 seconds." |
| R7 | REFUSE to launch when dependent services are unhealthy. A healthy service depending on an unhealthy downstream will fail. | Trigger: launch request AND any critical downstream dependency has degraded status on the health dashboard | STOP. "Dependent service [name] is currently degraded ([status]). Launching now couples your launch risk to their ongoing incident. Wait for dependency to recover or implement a circuit breaker that gracefully degrades when downstream fails." |

## The Expert's Mindset

- **Ships are processes, not events.** A launch is not the moment you click deploy. It is the weeks of preparation, the staged rollout, the monitoring vigil, the go/no-go decision, and the post-launch retro. Treat the deploy button as step 7 of 20, not the finish line.
- **Blast radius is everything.** The difference between a bad launch and a catastrophe is blast radius. Start with 1% of traffic, then 5%, then 25%. At each stage, let the metrics stabilize for at least 15 minutes before expanding. A bug affecting 1% of users is a ticket; a bug affecting 100% is a SEV-1.
- **Feature flags are safety belts, not just feature toggles.** Every flag should have: a kill switch, an owner, a sunset date, and a monitoring dashboard. A flag without these four things is a time bomb disguised as a feature toggle.
- **Go/no-go decisions are data-driven, not calendar-driven.** "It is Tuesday, so we must ship" is how you cause incidents. If the metrics are red, the answer is no-go regardless of the calendar. Ship when it is safe, not when it is scheduled.
- **Rollback is a feature, not a failure.** Designing for rollback (feature flags, backward-compatible schemas, blue-green deploys) is engineering excellence. If you cannot rollback in under 5 minutes, your launch is under-prepared.

## Operating at Different Levels

- **Quick scan (30s):** Check launch checklist status, verify staging is green, confirm on-call schedule, check error budgets, review the kill switch for the primary feature flag.
- **Standard engagement (10min):** Review pre-launch checklist completion, verify monitoring dashboards show staging data, confirm rollback procedure is documented and tested, validate go/no-go criteria against current metrics.
- **Deep dive (full session):** Full launch readiness audit: run through every checklist item with evidence, review staged rollout percentages and stabilization periods, validate feature flag lifecycle (creation through deprecation), dry-run rollback in staging, draft launch communication for stakeholders and users.
- **Crisis mode (launch going badly):** Execute rollback immediately if any go/no-go threshold is breached. Do not debug in production. Rollback first, investigate in staging later. Communicate status to stakeholders within 5 minutes of rollback decision.

## When to Use

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

## Core Workflow

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

## Decision Trees

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

## Cross-Skill Coordination

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

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | Launch checklist has unverified items within 1 hour of scheduled launch | [ALERT] Unverified checklist items: [list]. Resolve or reschedule launch. |
| P2 | Error budget below 50% and launch is high-risk | [WARN] Error budget at [X]%. Consider reducing blast radius or waiting for budget recovery. |
| P3 | Feature flag older than 60 days found in codebase | [ALERT] Flag [name] has exceeded its sunset date. Schedule removal within 2 weeks or extend with justification. |
| P4 | No staging deploy in last 48 hours before production launch | [ALERT] Staging has not been validated recently. Deploy and run smoke tests before production launch. |
| P5 | Go/no-go criteria document references metrics without dashboards | [WARN] No dashboard found for metric [name]. Create dashboard before relying on it for go/no-go decisions. |

## What Good Looks Like

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

1. **Checklist Gap Analysis:** Take the last 3 production incidents from your team's post-mortems. For each incident, identify which pre-launch checklist item would have caught it. If none would have, add a new checklist item. Run the updated checklist against the next launch.

2. **Rollback Dry Run:** Schedule a "fire drill" during business hours. Deploy a canary with a deliberate performance degradation (artificial sleep in an endpoint). Time how long it takes from alert firing to full rollback. Target: under 5 minutes for feature flag rollback, under 15 minutes for deploy rollback.

3. **Feature Flag Cleanup Sprint:** Audit your codebase for feature flags older than 60 days. For each: either schedule removal within 2 weeks (with code cleanup) or document the business justification for keeping it. Track flag count over time -- it should be a sawtooth pattern, not monotonic growth.

4. **Go/No-Go Simulation:** Build a table-top exercise with your team. Present a launch scenario with mixed signals (one metric red, others green). Have each team member vote go/no-go with justification. Discuss disagreements. Align on decision-making principles.

5. **Launch Communication Template:** Draft a launch communication for a fictional major outage during a launch. Include: what happened, user impact, current status, estimated resolution, workaround, next update time. Practice delivering it in under 3 minutes. Then draft the post-launch retro summary.

## Gotchas

- **Launching on Friday at 5pm guarantees a weekend incident.** A team deploys a major feature Friday afternoon and leaves for the weekend. A latent bug surfaces Saturday morning when traffic patterns differ from weekday testing. No one is monitoring, and the first alert comes from a customer tweet 8 hours later. **Total cost: $15,000-$50,000 in weekend emergency response, customer trust damage, and potential SLA credits.** Fix: Launch Tuesday-Thursday before 2pm. Never launch on Friday without explicit executive approval and 24/7 on-call coverage.

- **A feature flag without a kill switch turns a 1-minute fix into a 30-minute deploy.** A feature causes a 5x latency spike. The engineer tries to disable the flag but discovers it was hardcoded as a build-time constant, not a runtime toggle. They must cut a new build, wait for CI (25 minutes), and deploy before users see relief. **Total cost: $3,000-$8,000 in degraded user experience and emergency engineering time per incident.** Fix: Every feature flag must have a runtime kill switch (env var, remote config, or admin API) that takes effect within 60 seconds without a deploy.

- **Skipping dark launch causes data corruption at scale.** A new data pipeline writes malformed records to the primary database. Without dark launch (mirroring traffic without persisting), the bug writes 2 million bad records to production before detection. Recovery requires 8 hours of point-in-time restore and data reconciliation. **Total cost: $20,000-$100,000 in engineering time, data recovery, and potential customer-facing data issues.** Fix: Dark launch every data-mutating change. Mirror write traffic to a shadow table for 24-48 hours. Validate data integrity before enabling real writes.

- **Staged rollout percentages that skip from 1% to 100% defeat the purpose.** A team enables a feature for 1% of users, sees no issues for 10 minutes, and jumps to 100%. A database connection pool leak that only manifests under sustained load (needing 15+ minutes at scale) is missed. The pool exhausts at 100% traffic, causing a complete outage. **Total cost: $10,000-$30,000 in outage impact and remediation.** Fix: Each rollout stage must run long enough to observe steady-state behavior. Minimum stabilization periods: 5% for 30min, 25% for 2h, 50% for 4h, 100% with flag as kill switch for 2 weeks.

- **Monitoring dashboards set up on launch day show no historical baseline.** An engineer creates dashboards 30 minutes before launch. When metrics show 200 errors/minute after rollout, there is no baseline to compare against. The team wastes 45 minutes debating whether 200 errors/minute is normal (it was 10/minute before the launch). **Total cost: $2,000-$5,000 in delayed detection and wasted diagnosis time.** Fix: Create monitoring dashboards at least 1 week before launch. Establish baseline metrics from staging and production (pre-feature). Annotate the launch event on all dashboards.

- **Rollback runbook that has never been tested fails when needed.** The documented rollback procedure says "run rollback.sh". On launch day, the engineer discovers rollback.sh requires a specific Python version not installed on the production jump host. The 3-minute procedure takes 25 minutes while they find the right environment. **Total cost: $8,000-$25,000 in extended incident duration.** Fix: Dry-run the rollback procedure in a production-like environment within 7 days of launch. Time it. Document the exact environment prerequisites. The runbook should work from a fresh terminal with no local state.

- **Launch communication that blames "a routine deployment" erodes trust.** After a launch causes a 30-minute partial outage affecting 15% of users, the status page says "We performed routine maintenance." Users who could not access the service know this is false. Social media erupts with "routine maintenance = we broke something." **Total cost: Hard to quantify but significant -- customer churn, reputation damage, reduced feature adoption.** Fix: Be honest in launch communication. "We deployed [feature] and encountered an unexpected issue with [component]. We rolled back within [N] minutes. Full post-mortem will be published within 5 business days."

## Verification

- [ ] Pre-launch checklist: all 6 gates (Code Quality, Security, Performance, Accessibility, Infrastructure, Documentation) show GREEN
- [ ] Rollback procedure: tested in staging within last 7 days, timed at under 5 minutes for feature flag and under 15 minutes for deploy rollback
- [ ] Monitoring: dashboards exist for error rate, latency (p50/p95/p99), throughput, saturation, and business metrics, with at least 24 hours of baseline data
- [ ] Feature flags: every flag has an owner, a sunset date, a kill switch verified to work, and a linked monitoring dashboard
- [ ] Staged rollout plan: defined percentages with minimum stabilization periods, automatic rollback thresholds documented
- [ ] Go/no-go criteria: documented with specific metric thresholds, signed off by engineering lead and product manager
- [ ] Communication: stakeholder email sent, support team briefed, status page template prepared, launch timeline published
- [ ] On-call coverage: engineer scheduled and available for full launch window plus 2 hours after final expansion

## References

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