---
name: release-manager
description: Release management, release train, deployment calendar, go/no-go, release coordination, version management, launch readiness, rollback, canary deployment, feature flags. Works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI.
author: Sandeep Kumar Penchala
type: devops
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - release-manager
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
---
# Release Manager

Orchestrate the safe, predictable delivery of software to production. Design release trains,
facilitate go/no-go decisions, manage deployment calendars across teams, coordinate rollbacks,
automate release notes, coordinate feature flag dark launches, and run post-release verification.
Covers the full release lifecycle from branch strategy through production verification and
retrospective.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Plan a release (schedule, scope, dependencies) → Jump to "Core Workflow > Phase 1" (Release Planning)
│   ├── Establish release cadence → Go to "Decision Trees > Release Cadence"
│   └── Coordinate across teams → Go to "Best Practices > Cross-Team Coordination"
├── Coordinate a deployment → Jump to "Core Workflow > Phase 2" (Deployment Coordination)
│   ├── Canary deployment → Go to "Decision Trees > Deployment Strategy Selection"
│   └── Feature flag management → Jump to "Core Workflow > Phase 2" (Feature Flag Dark Launch)
├── Run a go/no-go decision → Jump to "Core Workflow > Phase 3" (Go/No-Go Decision)
├── Plan a rollback → Go to "Core Workflow > Phase 4" (Rollback Planning) and "Best Practices > Rollback"
├── Set up a canary deployment → Jump to "Decision Trees > Deployment Strategy Selection" and "Core Workflow > Phase 2"
├── Manage feature flags for release → Go to "Sub-Skills > feature-flag-management"
└── Not sure where to start? → "Decision Trees > Release Strategy" — match your release frequency to team maturity
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never deploy without a verified rollback plan.** Every deployment must have a documented, tested rollback procedure that takes less time than the deployment itself. If you can't roll back in <5 minutes, don't deploy.
- **Go/no-go decisions need objective criteria, not gut feel.** Use a checklist: test pass rate, coverage, performance benchmarks, security scan results, change failure rate. "Feels ready" is not a criterion.
- **Every release needs a communication plan.** Stakeholders, support teams, and on-call engineers must know: what's deploying, when, what changes, what to watch, and who to contact if something breaks.
- **Feature flags need owners and expiry dates.** Every flag must have a named owner and a removal date (within 1-2 sprints). Flags without expiry dates are technical debt that will cause incidents.
- **Always verify in production after deploy.** Smoke tests, canary metrics, and real-user monitoring before declaring the release complete. The deploy isn't done when the binary is live — it's done when you've confirmed it works.
- **Admit what you don't know.** If you don't have visibility into a dependent team's readiness or a downstream system's state, flag it as a risk — don't assume.

## When to Use

- Your team is shipping too infrequently (or too chaotically) and you need to establish a release cadence
- You need to decide on a release strategy — continuous deployment, daily, weekly train, or sprint-based
- You are running a go/no-go meeting and need a structured readiness checklist to evaluate release risk
- You need to coordinate a release across 3+ teams with interdependent changes and shared deployment windows
- You are designing a canary deployment or blue-green rollout with automated metric comparison and rollback triggers
- You need to set up feature flag dark launches so features can ship disabled and activate safely in production
- You are automating release notes, changelog generation, and version bumping from conventional commits
- You need a rollback playbook — how to detect a bad deploy, who to notify, and how to revert safely

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### 1. Release Cadence Selection
```
What release cadence fits your risk tolerance and team capacity?
├─ Continuous deployment (multiple/day)?
│   └─ PREREQUISITES: feature flags, automated canary + rollback, < 1% change failure rate, DORA Elite level
│       └─ Not ready? → Choose a slower cadence and invest in prerequisites
├─ Daily releases?
│   └─ PREREQUISITES: automated CI/CD, staging environment, automated smoke tests, on-call coverage
│       └─ Good for: web apps, SaaS, internal tools — where rollback is cheap and fast
├─ Weekly release train?
│   └─ PREREQUISITES: release branch, QA regression suite (< 4 hours), go/no-go meeting
│       └─ Good for: cross-team coordination, mobile apps (app store review), regulated environments
├─ Bi-weekly / Sprint-based?
│   └─ PREREQUISITES: sprint planning alignment, feature freeze 2 days before, dedicated QA window
│       └─ Good for: enterprise software, on-prem deployments, customer-managed upgrades
├─ Monthly / Quarterly?
│   └─ Only acceptable for: on-prem software with customer upgrade friction, embedded systems
│       └─ WARNING: > 2 week cycles create merge hell and deferred risk accumulation
└─ Decision rule: if you do quarterly, the INTERNAL cadence should be weekly (via release branches)
```

### 2. Go/No-Go Decision Framework
```
At release readiness review, evaluate each criterion:
├─ CRITICAL (any NO = NO-GO):
│   ├─ All automated tests passing? (unit, integration, E2E, smoke)
│   ├─ Security scan clean? (no HIGH/CRITICAL CVEs in dependencies)
│   ├─ Performance regression check passing? (p95 latency < baseline + 10%)
│   ├─ Known P0/P1 bugs? (any open SEV1/SEV2 bugs → NO-GO)
│   └─ Rollback plan tested? (can we revert in < 10 minutes?)
├─ CONDITIONAL (NO = discussion, documented risk acceptance):
│   ├─ All feature flags configured correctly? (new features dark by default?)
│   ├─ Monitoring dashboards and alerts updated for new features?
│   ├─ Release notes drafted and reviewed?
│   ├─ Support/customer-success team briefed?
│   └─ Database migrations tested on production-scale data?
├─ Adjudication:
│   ├─ All CRITICAL pass → GO
│   ├─ Any CRITICAL fail → NO-GO (fix + retest)
│   ├─ > 2 CONDITIONAL fail → NO-GO (unless CTO/VP signs off risk acceptance)
│   └─ Tiebreaker: last releaser says GO/NO-GO if consensus cannot be reached
└─ Decision deadline: 24 hours before deployment window
```

### 3. Rollback Decision Criteria
```
Incident detected during/after deployment:
├─ Is the issue user-visible?
│   ├─ YES → What's the blast radius?
│   │   ├─ > 20% of users impacted → ROLLBACK IMMEDIATELY (< 5 min decision)
│   │   ├─ 5-20% impacted → ROLLBACK (try hotfix first only if fix is < 15 min away)
│   │   └─ < 5% impacted → Investigate; rollback if root cause unclear after 30 min
│   └─ NO (internal/background) → Fix forward; no rollback unless data corruption
├─ Is a hotfix possible in < 15 minutes?
│   ├─ YES + blasts radius < 5% → Hotfix forward
│   └─ NO → ROLLBACK
├─ Data integrity involved? → ROLLBACK + verify data consistency post-revert
└─ ROLLBACK EXECUTION:
    ├─ 1. Activate: incident commander declares rollback (no committee needed)
    ├─ 2. Execute: automated rollback pipeline (target: < 10 min to previous healthy state)
    ├─ 3. Verify: smoke tests pass on rolled-back version; error budget burn stops
    ├─ 4. Communicate: status page update within 5 min; stakeholder Slack within 15 min
    └─ 5. Retro: postmortem within 48h; identify why deploy gates didn't catch the issue
```

### 4. Versioning Strategy Selection
```
What versioning scheme?
├─ Library/API (consumed by other code)?
│   └─ SemVer (MAJOR.MINOR.PATCH)
│       ├─ MAJOR: breaking API changes
│       ├─ MINOR: backward-compatible new functionality
│       └─ PATCH: backward-compatible bug fixes (auto-bump, no human decision)
├─ SaaS/web application (user-facing but not consumed as library)?
│   └─ CalVer (YYYY.MM.PATCH) or date-based tags
│       └─ Benefit: users understand recency; no "MAJOR" anxiety
├─ Internal service (consumed by other services but no external API contract)?
│   └─ Git SHA or build number (semantic tags optional)
│       └─ Benefit: simplicity; deploy-any-commit capability
├─ Mobile app (distributed through app stores)?
│   └─ SemVer for marketing version; build number for technical tracking
│       └─ App stores enforce increasing numbers; coordinate with store review timeline
└─ 0ver (zero-based versioning)?
    └─ Use when: rapid iteration, pre-1.0 product, no stability promise
        └─ Example: 0.47.3 → 0.48.0; MAJOR always 0 until "stable" declaration
```

### 5. Hotfix vs. Scheduled Release Decision
```
Critical bug found in production:
├─ User-visible and SEV1/SEV2?
│   └─ HOTFIX: cherry-pick to release branch → accelerated deploy pipeline → verify
│       └─ Process: hotfix branch from release tag → fix + test → merge to release AND main
├─ User-visible but SEV3 (minor, workaround exists)?
│   └─ SCHEDULED: include in next regular release train
├─ Not user-visible?
│   └─ SCHEDULED: fix in main, goes out with next release
└─ HOTFIX process requirements:
    ├─ Hotfix PR must be reviewed by 2+ engineers (same standard as normal PRs)
    ├─ Must pass full test suite (no shortcuts)
    ├─ Must update release notes and changelog
    └─ Post-hotfix: root cause analysis within 48h to prevent recurrence

**What good looks like:** The output opens correctly in the target tool. All validations pass. No placeholder content remains.

```

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Release Planning
1. **Establish release calendar**: define release train schedule (weekly, bi-weekly), deployment windows, and freeze periods.
   - Output: Shared calendar with release dates, code freeze deadlines, QA windows, and deploy windows for next quarter.
2. **Map cross-team dependencies**: identify which services/teams must release together.
   - Input: Service dependency map, architecture docs, team ownership matrix.
   - Output: Release dependency graph with ordering constraints.
3. **Define release scope**: features, bug fixes, infrastructure changes — what's planned for this release.
   - Input: Product roadmap, sprint backlog, engineering work tracker.
   - Output: Release scope document with owner, risk level, and feature flag plan per item.
4. **Assign release roles**: release commander, QA lead, deployment engineer, communications liaison.
   - Output: Release role assignment for each release in the calendar.

### Phase 2 (~30 min): Release Preparation
1. **Create release branch**: branch from main at code freeze; cherry-pick approved changes only after freeze.
   - Output: `release/v2.5.0` branch with frozen scope; `main` continues forward development.
2. **Run full test suite**: unit, integration, E2E, performance, security on release branch.
   - Output: Test results dashboard; any failures must be fixed and re-tested before go/no-go.
3. **Verify feature flag configuration**: all new features behind flags, default OFF for gradual rollout.
   - Output: Feature flag manifest showing flag name, rollout %, and kill-switch availability.
4. **Draft release notes**: auto-generate from conventional commits; add human-written summary, known issues, upgrade notes.
   - Input: Commit history between previous release tag and current release branch.
   - Output: Release notes in changelog format (Keep a Changelog) with breaking change callouts.
5. **Brief stakeholders**: support team, customer success, marketing — provide release summary and expected impact.
   - Output: Stakeholder briefing doc (1-pager) sent 48 hours before deploy window.

### Phase 3 (~20 min): Go/No-Go Decision
1. **Run go/no-go checklist**: evaluate all CRITICAL and CONDITIONAL criteria (see Decision Tree #2).
   - Output: Go/No-Go scorecard with pass/fail per criterion.
2. **Conduct go/no-go meeting** (30 min max, day before deploy):
   - Attendees: release commander, QA lead, engineering lead, product owner.
   - Agenda: review checklist, discuss any CONDITIONAL failures, vote GO/NO-GO.
   - Output: GO/NO-GO decision documented in release tracker.
3. **NO-GO resolution**: fix failures, re-run tests, reconvene. Maximum 2 NO-GO attempts before scope reduction.
   - Output: Updated scope (smaller, safer) or new release date.

### Phase 4 (~15 min): Deployment Execution
1. **Pre-deploy verification**: smoke tests on staging, database migration dry-run, load balancer health check.
   - Output: Pre-deploy checklist all green.
2. **Execute deployment strategy**: canary (5% → monitor 10 min → 25% → monitor 10 min → 100%) or blue-green.
   - Input: Deployment strategy decision (canary/blue-green/rolling) based on risk assessment.
   - Output: Deployment progressing through stages with automated metric verification at each gate.
3. **Monitor during deployment**: watch error rate, latency, saturation, and business metrics (signups, checkout success).
   - Output: Real-time deploy dashboard; automated rollback if error budget burn exceeds threshold.
4. **Post-deploy verification**: smoke tests against production, critical user journey validation.
   - Output: Release verification checklist signed off within 30 minutes of 100% rollout.
5. **Feature flag rollout**: enable features gradually over 1-3 days, monitoring each increment.
   - Output: Feature rollout plan with % increments and verification windows.

### Phase 5 (~25 min): Post-Release
1. **Monitor for 24-72 hours**: watch error budgets, performance, user reports, support ticket volume.
   - Output: Post-release monitoring report at T+24h and T+72h.
2. **Finalize release notes**: add any post-release fixes, known issues discovered during rollout.
   - Output: Published release notes on changelog page and internal wiki.
3. **Conduct release retrospective** (within 1 week):
   - What went well? What went wrong? What should we change for next release?
   - Output: Retrospective doc with < 5 action items prioritized.
4. **Archive release artifacts**: release branch, build artifacts, test results, go/no-go decision record.
   - Output: Release archive for audit and future reference.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
| Coordinate With | When | What to Share/Ask |
|---|---|---|
| **CI/CD Builder** | Pipeline design, deployment automation, rollback automation | Release workflow requirements, canary/blue-green configuration, gating criteria |
| **SRE** | Error budget integration, incident response during deploy, post-deploy verification | Release risk assessment, error budget status, deploy freeze requests |
| **QA Engineer** | Test planning, regression suite execution, go/no-go testing criteria | Release scope, test results, quality sign-off requirements |
| **Product Manager** | Release scope definition, feature priority, stakeholder communication | Feature readiness, dark launch plans, customer communication |
| **Backend/Frontend Developers** | Feature completion, merge coordination, bug fixes | Code freeze timeline, cherry-pick requests, merge conflict resolution |
| **Security Engineer** | Security scan results, CVE remediation, compliance verification | Security clearance for release, vulnerability status, compliance gate results |
| **DevOps Engineer** | Infrastructure changes in release, database migrations, environment readiness | Infrastructure change risk, migration rollback plan, environment availability |
| **Platform Engineer** | Golden path integration, self-service release dashboard, template compliance | Release workflow in platform, dashboard requirements, release health metrics |
| **Support/Customer Success** | Release briefing, known issues, customer communication templates | Release summary, expected impact, support escalation path for release issues |
| **Marketing** | Public release announcement, feature highlights, changelog publication | Release notes, feature highlights, timing coordination for external communication |

### Escalation Path
```
Go/No-Go deadlock (cannot reach consensus)? → CTO decides
SEV1 during deployment? → SRE Incident Commander → Rollback → CTO notified
Release repeatedly NO-GO (3+ times)? → CTO + Product (scope renegotiation)
Cross-team dependency blocking release? → Engineering Manager → CTO
Customer-impacting regression found post-release? → SRE → Rollback → Postmortem
```

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
- **What changes**: No formal release process. Merge to main → deploy. Feature flags via env vars. Release notes are git log. Rollback = `git revert` + redeploy.
- **Overkill**: Release trains, go/no-go meetings, release branches, formal versioning, stakeholder briefings, deployment calendars.
- **Coordination**: You decide when to deploy. No coordination needed.
- **Cost**: $0 beyond CI/CD costs.
- **Transition trigger**: First time you break production and can't quickly identify which change caused it. Second person starts deploying.

### Small (2-10 people, 100-10K users)
- **What changes**: Release branches for coordination. Basic go/no-go (tests passing? security scan clean?). Weekly release cadence. Automated release notes (conventional commits + changelog tool). Feature flags for risky changes. Simple versioning (SemVer). Rollback via pipeline.
- **Overkill**: Formal release train with cross-team dependency mapping, stakeholder briefing docs, multi-stage canary with metric verification, release commander role.
- **Coordination**: One person owns the release each week (rotating). Go/no-go checklist in a shared doc. Release notes auto-generated. Brief Slack announcement.
- **Cost**: $0-200/month (changelog tools, feature flag SaaS free tier).
- **Transition trigger**: > 2 teams shipping to same production; merge conflicts during deploy; "who deployed what?" confusion.

### Medium (10-50 people, 10K-1M users)
- **What changes**: Weekly release train with published calendar. Formal go/no-go meeting (30 min, day before). Designated release commander (rotating). Canary deployments with metric verification. Release dashboards. Cross-team dependency tracking. Stakeholder briefing for major releases. Feature flag platform with gradual rollout. Release retrospective every cycle.
- **Overkill**: Full-time release manager, multi-track release trains, deployment window SLAs, formal risk assessment matrix for every release.
- **Coordination**: Release commander coordinates across teams. Go/no-go meeting with QA + engineering leads. Dependency check-in 3 days before freeze. Release retrospective within 1 week.
- **Cost**: ~$20-40K/year (feature flag platform, 10% of senior engineer time for release commander rotation).
- **Transition trigger**: > 5 teams deploying to same production; first customer-reported deployment regression; compliance audit requiring deployment records.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Dedicated release management function (1-2 release managers). Multi-track release trains (fast track for hotfixes, standard track for features). Enterprise feature flag platform with kill switches and audit logging. Automated canary analysis with statistical significance testing. Release risk assessment matrix with scoring. Formal stakeholder communication templates. Deployment window SLAs with business units. Release health scorecards. Regulatory compliance evidence collection per release.
- **What's full production**: Release management platform with automated gating. Progressive delivery with automated promotion/rollback. Release predictability metrics (on-time %). Self-service release dashboard for all teams. Compliance artifact auto-generation per release.
- **Coordination**: Release manager runs release planning weekly. Go/no-go with VP-level visibility for major releases. Cross-team dependency sync daily during freeze week. Monthly release program review with CTO.
- **Cost**: $300-600K/year (1-2 release managers + platform). Feature flag enterprise platform $30-80K/year. Release management tooling $10-30K/year.
- **Transition trigger**: > 10 teams deploying to same production, regulatory environment (SOX, FDA), customer contractual release SLAs, > $100M revenue with release-dependent revenue recognition.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | ci-cd-builder | Build artifacts and deployment pipeline |
| **This** | release-manager | Release plan, go/no-go decision, deployment coordination |
| **After** | site-reliability-engineer | Production reliability monitoring and incident response |

Common chains:
- **Chain**: ci-cd-builder → release-manager → site-reliability-engineer — Pipeline produces deployable artifacts; release manager orchestrates rollout; SRE monitors production health
- **Chain**: qa-engineer → release-manager → incident-responder — QA reports test results; release manager decides go/no-go; incident responder handles any production issues

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|---|---|---|
| `release-train-design` | Designing the release cadence, train tracks, and freeze windows | Cadence selection, train topology, emergency/hotfix track, calendar management |
| `go-no-go-framework` | Establishing go/no-go criteria, checklist, and decision process | Critical vs. conditional criteria, meeting facilitation, risk acceptance documentation |
| `versioning-strategy` | Selecting and implementing SemVer, CalVer, or custom versioning | Version bump automation, changelog generation, breaking change detection |
| `rollback-playbook` | Designing and automating rollback procedures | Decision criteria, execution pipeline, verification, data consistency, communication |
| `release-notes-automation` | Automating changelog generation from conventional commits | Commit conventions, changelog tools, human-written summaries, breaking change callouts |
| `feature-flag-coordination` | Coordinating dark launches and gradual rollouts via feature flags | Flag lifecycle, kill switches, rollout percentages, flag debt cleanup |
| `canary-deployment` | Progressive delivery with canary analysis and automated gating | Canary stages, metric-based promotion, automated rollback triggers, statistical analysis |
| `release-health-dashboard` | Building dashboards for release tracking, health, and predictability | Key metrics, stakeholder views, historical trend analysis, deploy frequency tracking |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Release trains create predictability**: teams know exactly when their code ships. This reduces "is my change in prod?" anxiety and makes planning possible.
- **Code freeze means CODE FREEZE**: only bug fixes and security patches after the freeze deadline. Feature work goes to the next train. No exceptions without release commander + CTO approval.
- **Go/No-Go is not a democracy**: the release commander makes the final call. A clear decision-maker prevents deadlocks. Rotate the role to share risk awareness.
- **Rollback is a feature, not a failure**: if rollback takes > 10 minutes, it's broken. Practice rollbacks monthly. A smooth rollback is better than a heroic hotfix.
- **Feature flags have a lifecycle**: every flag must have an owner and removal date. Flags older than 60 days become technical debt. Use flag removal as a release checklist item.
- **Release notes are for humans, not computers**: auto-generated changelogs are a start. Add a 1-paragraph summary, known issues, and upgrade instructions written by a person.
- **Every release needs a rollback plan**: if you can't describe how to undo a change in < 3 sentences, it shouldn't be in the release.
- **Database migrations are the #1 cause of rollback failures**: always have a downgrade migration tested. If a migration is irreversible, it goes in a separate, carefully planned release.
- **Post-release monitoring is mandatory**: the first 24 hours after deploy is when most regressions surface. Keep the deployer on-call for at least 24 hours post-release.
- **Release retrospectives compound**: each retro should produce < 5 action items. Track them across releases. If the same issue appears in 3 consecutive retros, escalate to engineering leadership.


### Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| `Permission denied` | Missing file/system permissions | Use `chmod +x` or `sudo`; check user/group ownership |
| `command not found` | Required tool not installed | Install with `apt install`, `brew install`, or `npm install -g` |
| `File exists` | Output file already exists | Use `--force` flag or specify different output path |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Release calendar published for current quarter with freeze dates, deploy windows, and release commander assignments
- [ ] **[S2]**  Go/no-go checklist defined with CRITICAL (auto NO-GO if fail) and CONDITIONAL criteria
- [ ] **[S3]**  Release branch strategy documented: branch naming, cherry-pick process, merge-back to main
- [ ] **[S4]**  Rollback pipeline tested within last 30 days; target: < 10 minutes from decision to previous healthy state
- [ ] **[S5]**  All database migrations have tested downgrade scripts; irreversible migrations flagged and planned separately
- [ ] **[S6]**  Feature flag platform in place; all new features behind flags with rollout plan and removal date
- [ ] **[S7]**  Release notes auto-generated from conventional commits with human-written summary and breaking change callouts
- [ ] **[S8]**  Canary deployment pipeline: 5% → monitor → 25% → monitor → 100% with automated metric gates at each stage
- [ ] **[S9]**  Post-release monitoring dashboard active for 72 hours after every deploy
- [ ] **[S10]**  Release retrospective conducted within 1 week of every release; action items tracked
- [ ] **[S11]**  Stakeholder briefing template ready; stakeholders briefed 48 hours before major releases
- [ ] **[S12]**  Release archive maintained: branch, build artifacts, test results, go/no-go decision for audit
- [ ] **[S13]**  Deployment window communicated to all teams; no competing infrastructure changes during window
- [ ] **[S14]**  Support/customer success team has escalation path for release-related issues

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Keep a Changelog](https://keepachangelog.com/) — Standard for human-readable changelogs
- [Semantic Versioning](https://semver.org/) — SemVer specification
- [Conventional Commits](https://www.conventionalcommits.org/) — Commit message convention for automated changelogs
- [LaunchDarkly Feature Flags](https://launchdarkly.com/) — Feature flag management platform
- [DORA Metrics](https://dora.dev/) — Deployment frequency as key release health metric
- [Google SRE: Release Engineering](https://sre.google/sre-book/release-engineering/) — Release engineering chapter from Google SRE book
- Internal: [../../domain/references/release-management-patterns.md](../../domain/references/) — Release strategies and anti-patterns
