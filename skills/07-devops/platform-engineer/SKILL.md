---
name: platform-engineer
description: Internal Developer Platform (IDP) design, golden paths, Backstage, self-service infrastructure, developer portals, scaffolding, developer experience (DX), platform as product. Works with Claude
  Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI.
author: Sandeep Kumar Penchala
type: devops
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- platform-engineer
token_budget: 3525
chain:
  consumes_from:
  - cloud-architect
  - devops-engineer
  - docker-kubernetes
  - observability-engineer
  feeds_into:
  - backend-developer
  - devops-engineer
  - frontend-developer
  - observability-engineer
output:
  type: code
  path_hint: ./
---
# Platform Engineer / Developer Experience (DX)

Design and operate an Internal Developer Platform that transforms infrastructure into a product.
Covers IDP architecture, golden path templates, self-service IaC modules, developer portal
implementation (Backstage, Port, Cortex), scaffolding toolchains, ephemeral environments, platform
APIs, service catalogs, scorecards, and the platform-as-product operating model.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Design an Internal Developer Platform (IDP) → Jump to "Core Workflow > Phase 1" (IDP Architecture)
│   ├── Platform as product → Go to "Best Practices > Platform as Product"
│   └── Build vs buy decision → See "Decision Trees > Build vs Buy"
├── Create golden paths / paved roads → Jump to "Core Workflow > Phase 2" (Golden Path Design)
│   ├── Service template/scaffolding → Go to "Sub-Skills > scaffolding-toolchains"
│   └── Self-service IaC modules → Go to "Sub-Skills > self-service-infrastructure"
├── Set up Backstage (or Port/Cortex) → Go to "Core Workflow > Phase 3" (Developer Portal)
├── Build self-service infrastructure → Go to "Sub-Skills > self-service-infrastructure" and "Core Workflow > Phase 4"
├── Design a developer portal → Jump to "Core Workflow > Phase 3" (Developer Portal)
├── Set up scaffolding / project templates → Go to "Sub-Skills > scaffolding-toolchains"
├── Need infrastructure building blocks → Invoke `devops-engineer` skill instead
├── Need container orchestration → Invoke `docker-kubernetes` skill instead
├── Need cloud architecture guidance → Invoke `cloud-architect` skill instead
├── Need observability for platform → Invoke `observability-engineer` skill instead
└── Not sure where to start? → "Decision Trees > Platform Maturity Assessment" — understand current state before building
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never build platform features without developer input.** The platform exists to serve developers, not to satisfy platform engineers' architectural ambitions. Validate every feature with real users before building.
- **Golden paths must be the easiest path, not the only path.** Teams must be able to escape the paved road when they have legitimate needs the platform doesn't cover. The platform reduces cognitive load, not removes choice.
- **Platform adoption is earned, not mandated.** If developers are forced to use your platform, you've already failed. Build something so useful they choose it voluntarily.
- **Self-service means zero tickets.** If a developer needs to open a Jira ticket and wait 3 days to provision a database, you don't have a platform — you have a bottleneck with a portal in front of it.
- **Always measure developer experience (DX).** Track time-to-first-deploy, time-to-provision, platform NPS, and ticket volume. Platform success is measured in developer productivity, not platform feature count.
- **Admit what you don't know.** If you haven't interviewed the developers who will use this platform, say so. Recommendations without user research are guesses.

## When to Use

- Your organization has 3+ teams and developers are spending >30% of their time on infrastructure setup
- You are designing a developer portal (Backstage, Port, Cortex) with a service catalog and scorecards
- You need to create golden path templates that provision infrastructure, CI/CD, and monitoring from a single scaffold
- You are building self-service IaC modules so teams can provision databases, queues, and environments without a ticket
- You need to implement ephemeral preview environments that spin up per pull request and tear down on merge
- You are defining platform APIs that abstract cloud complexity behind a simple developer-facing interface
- You are evaluating build vs. buy vs. assemble for platform components (CI, CD, monitoring, secrets management)
- You need to measure developer experience (DX) with metrics like time-to-first-deploy, DORA metrics, and developer NPS

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### 1. Should This Be a Golden Path or Let Teams Choose?
```
Is this capability required for ALL services?
├─ YES → Golden path (mandatory template)
│   └─ Examples: logging, monitoring, CI/CD pipeline, containerization
├─ NO → Is this a frequent request from teams?
│   ├─ YES (>3 teams asked) → Golden path (recommended, not forced)
│   │   └─ Examples: feature flags, secrets management, DB provisioning
│   └─ NO → Let teams own it; revisit at next platform review
└─ Exception: Compliance/security mandate → Golden path regardless of demand
```

### 2. Build vs. Buy vs. Assemble for Platform Components
```
Is this a differentiating capability for your business?
├─ YES → Build custom (your competitive advantage lives here)
│   └─ Examples: custom deployment orchestration, proprietary scaling logic
├─ NO → Is there a well-maintained open-source or SaaS option?
│   ├─ YES → Buy/Assemble (Backstage for portal, Terraform for IaC, ArgoCD for GitOps)
│   │   └─ Decision criteria: community size > 5K stars, > 3 committers, > 1 year age
│   └─ NO → Is the domain complex and evolving?
│       ├─ YES → Buy SaaS (let vendor absorb complexity)
│       │   └─ Examples: Port for catalog if Backstage plugin maintenance is too heavy
│       └─ NO → Build thin wrapper; keep surface area small
```

### 3. When to Enforce Platform Adoption vs. Encourage It
```
Adoption approach decision:
├─ Compliance-mandated capability (security, audit, data residency)?
│   └─ ENFORCE: platform policy gates block non-compliant deploys
├─ Productivity-blessed capability (CI templates, scaffolding)?
│   └─ ENCOURAGE: teams choose; measure adoption rate as KPI
├─ New capability being validated?
│   └─ PULL: build with 1-2 design partners, let word-of-mouth drive adoption
└─ Legacy migration path?
    └─ INCENTIVIZE: migration sprints, brownfield co-investment from platform team
```

### 4. Platform Team Topology Decision
```
How many teams and what operating model?
├─ Organization < 50 engineers?
│   └─ Single enabling team (4-6 platform engineers)
│       └─ Model: consulting + self-service tooling
├─ Organization 50-200 engineers?
│   └─ Platform product team + enabling squad
│       └─ Model: product-managed backlog, dedicated support rotation
├─ Organization 200-500 engineers?
│   └─ 2-3 stream-aligned platform teams
│       └─ Model: each owns a domain (CI/CD, infrastructure, observability)
└─ Organization 500+ engineers?
    └─ Platform org with product managers, dedicated SRE, developer relations
        └─ Model: internal product lines with SLAs and NPS tracking
```

### 5. IDP Maturity Model: Where Are You?
```
Level 1 (Ad-hoc): Teams provision manually, no shared tooling
  → Pain: onboarding takes 2+ weeks, every service looks different
Level 2 (Standardized): Shared IaC modules, documented patterns
  → Pain: modules drift, docs rot, platform team is bottleneck
Level 3 (Self-Service): Portal with click-to-create, policy-guarded templates
  → Pain: portal maintenance overhead, plugin ecosystem fragmentation
Level 4 (Productized): Platform has PM, roadmap, SLAs, NPS measurement
  → Pain: balancing innovation with stability, avoiding "platform as bottleneck"
Level 5 (Ecosystem): External contributors, plugin marketplace, multi-team ownership
  → Trigger: >500 engineers, multiple business units with divergent needs

**What good looks like:** The output opens correctly in the target tool. All validations pass. No placeholder content remains.

```

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Platform Discovery and Strategy
1. **Map the developer journey**: from laptop setup → first commit → deploy → monitor → incident response.
   - Output: Developer journey map with pain points, time-to-X metrics per phase.
2. **Identify top 3 friction points**: survey developers, measure DORA metrics, time-to-10th-pr.
   - Input: Developer experience survey (NPS + qualitative), pipeline data, onboarding logs.
   - Output: Prioritized backlog ranked by developer-hours-saved per sprint.
3. **Define platform North Star metrics**: time-to-first-deploy, deployment frequency, onboarding time, platform NPS.
   - Output: Dashboard with baseline measurements, 6-month targets.
4. **Select platform team model**: embedded, consulting, enabling, or product — based on org size (see Decision Tree #4).
   - Output: Team charter with mission, operating model, and stakeholder map.

### Phase 2 (~30 min): Golden Path Design
1. **Define the minimum service template**: language runtime, container, health checks, CI pipeline, observability, secrets.
   - Output: Reference implementation that deploys to production in < 1 hour from scaffold.
2. **Create scaffolding tool**: Cookiecutter/Yeoman template or CLI (`platform create service`) that generates the golden path.
   - Input: Golden path decisions from Phase 2.1.
   - Output: `platform create` command that produces a deployable service skeleton.
3. **Design self-service infrastructure modules**: Terraform/Pulumi/Crossplane compositions for RDS, S3, Redis, Kafka.
   - Output: Catalog of 8-12 infrastructure modules with input schemas and policy guards.
4. **Implement CI/CD pipeline template**: reusable workflow or pipeline-as-code that teams inherit.
   - Output: `.github/workflows/deploy.yml` (or equivalent) that any service can consume via 5 lines of config.
5. **Write "day 2" operations runbooks**: common tasks (scale up, rotate secrets, restore backup) as self-service workflows.
   - Output: 10-15 runbook entries in the developer portal.

### Phase 3 (~20 min): Developer Portal
1. **Select and deploy portal**: Backstage (oss), Port (SaaS), Cortex (SaaS), or custom.
   - Decision matrix: Backstage for customization + budget; Port/Cortex for time-to-value (< 2 weeks).
2. **Implement service catalog**: auto-register services from git repos, Kubernetes, or cloud providers.
   - Output: Every service has an owner, on-call rotation, docs link, and health score.
3. **Build software templates**: Backstage scaffolder actions or Port blueprints for "Create New Service".
   - Output: 3-5 templates covering 80% of service types (API, worker, cron, frontend, data pipeline).
4. **Integrate tech docs**: TechDocs (Backstage) or embedded README rendering from repos.
   - Output: Documentation auto-published on every merge to main.
5. **Add scorecards**: define 8-12 tech health checks (CI passing, dependency freshness, coverage %, SLO compliance).
   - Output: Scorecard dashboard showing red/amber/green per service.

### Phase 4 (~15 min): Environment-as-a-Service
1. **Design ephemeral environment lifecycle**: per-PR namespace, provision on PR open, tear down on merge/close.
   - Output: Architecture for namespace isolation, DNS routing, data seeding.
2. **Implement provisioning automation**: Terraform/Tilt/Garden Garden that spins up a full stack per PR.
   - Input: Service dependency graph, infrastructure module catalog.
   - Output: `pr-<number>.dev.example.com` fully functional within 5 minutes of PR open.
3. **Add cost controls**: TTL-based auto-cleanup (default 48h), per-team budget caps, idle detection.
   - Output: Dashboard showing ephemeral environment spend per team per month.

### Phase 5 (~25 min): Platform as Product Operations
1. **Establish platform SLAs**: availability (99.9%), template freshness (< 30 days behind), support response (< 4h during business hours).
   - Output: Published SLA page visible to all developers.
2. **Run quarterly developer NPS survey**: measure satisfaction, collect feature requests, identify deprecation candidates.
   - Output: NPS score trend, top-5 feature requests, bottom-3 pain points.
3. **Maintain platform changelog**: every change communicated via portal, Slack, and office hours.
   - Output: Changelog page, #platform-announcements channel, weekly office hours.
4. **Deprecation process**: announce → deprecation warning in tooling → migration guide → removal (minimum 90 days).
   - Output: Deprecation tracker with migration status per team.

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `devops-engineer` | Infrastructure building blocks, IaC modules, cluster templates, CI/CD pipeline design | Before building golden paths or self-service infrastructure APIs |
| `docker-kubernetes` | Containerized workloads deployable via golden paths, Helm chart standards, ingress patterns | Before designing deployment workflows or container defaults |
| `cloud-architect` | Landing zone integration, network topology, IAM guardrails for self-service | Before enforcing cloud governance in platform templates |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `backend-developer` | Golden path templates, self-service infrastructure, scaffolding tooling, developer CLI | Developers can't provision services — productivity blocked |
| `frontend-developer` | Portal UX, developer CLI ergonomics, onboarding experience, preview environments | Frontend teams can't self-serve — deployment friction |
| `devops-engineer` | Platform APIs, module contracts, golden path requirements, pipeline template needs | Infrastructure teams build without platform guidance — fragmentation risk |
| `observability-engineer` | Standard observability integration across all services, self-service dashboards | No consistent monitoring — every service reinvents observability |

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| Developer onboarding takes > 1 day from laptop to first production deploy | Propose golden path template: scaffold → local dev → CI/CD → staging → production in < 1 hour; eliminate manual setup steps | Onboarding friction is the canary for platform health; every day of onboarding delay is a day of lost productivity multiplied by every new hire |
| CI/CD pipelines are copy-pasted between repos — 50 slightly different `.github/workflows/deploy.yml` files | Propose reusable pipeline templates: organization-level workflow with parameterized inputs; one source of truth for lint → test → build → scan → deploy | Copy-paste pipelines create a maintenance nightmare; a single security fix must propagate to 50 repos; reusable templates centralize best practices |
| Security requirements documented in wiki but not enforced — teams skip them under delivery pressure | Propose policy-as-code integration: OPA/Rego or Sentinel policies in golden path templates; pipeline blocks deploy on policy violation; security is automatic, not aspirational | Documented security without enforcement is security theater; policy-as-code in the golden path makes compliance the default, not the exception |
| Teams provision infrastructure via tickets to platform team — 2-week wait for a database | Propose self-service infrastructure catalog: Terraform modules with JSON Schema validation, automated provisioning, policy guardrails; target < 15 minutes from request to provisioned | Ticket-based infrastructure provisioning is the #1 platform team bottleneck; self-service with guardrails is faster AND more secure |
| Developer portal (Backstage/Port) shows stale data — service catalog 3 months out of date | Propose automated catalog discovery: Kubernetes entity provider, GitHub org scanner, PagerDuty integration; catalog auto-updates, not manual curation | A stale service catalog is worse than no catalog — it trains developers that the platform is unreliable; auto-discovery keeps it current |
| Golden path templates are 12 months old — new services start with known vulnerabilities and deprecated APIs | Propose template lifecycle: assign owner per template, run Dependabot/Renovate on templates, test quarterly against security baseline, version templates with migration guides | A stale golden path is worse than no golden path — it gives false confidence while shipping known vulnerabilities |
| Platform team has no product manager — roadmap is a Jira backlog sorted by who shouts loudest | Propose platform-as-product: hire or designate a platform PM, run developer NPS survey, maintain public roadmap, prioritize by developer-hours-saved | A platform without product management is an infrastructure team that takes tickets; PM turns reactive ops into strategic product development |
| No ephemeral environments — every PR waits for a shared staging environment, merge conflicts in staging | Propose per-PR ephemeral environments: namespace isolation, automated DNS, data seeding, TTL auto-cleanup; PR gets its own full-stack environment | Shared staging is a bottleneck; ephemeral environments eliminate "works on my machine" and staging merge conflicts simultaneously |

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
- **What changes**: No IDP needed. Document patterns in a README. Single Terraform repo. Manual onboarding.
- **Overkill**: Backstage, scaffolding tools, ephemeral environments, platform APIs, scorecards.
- **Coordination**: You are the platform. No coordination overhead.
- **Cost**: $0 beyond cloud infrastructure costs.
- **Transition trigger**: Second developer joins; onboarding friction becomes visible (> 1 week to first deploy).

### Small (2-10 people, 100-10K users)
- **What changes**: Shared Terraform modules in a monorepo. Templated CI/CD (reusable workflows). `cookiecutter` scaffolding for new services. One shared dev AWS account. Runbooks in a wiki.
- **Overkill**: Developer portal, Backstage, platform APIs, formal SLAs, NPS surveys, ephemeral per-PR environments (use shared staging).
- **Coordination**: Platform changes via PR review. Monthly platform sync (30 min). Shared Slack channel.
- **Cost**: ~$200-500/month for shared dev infrastructure. Platform engineer is part-time role (20% of senior engineer).
- **Transition trigger**: 3+ services with divergent patterns emerge; onboarding > 3 days; first "I didn't know that existed" moment.

### Medium (10-50 people, 10K-1M users)
- **What changes**: Dedicated platform team (2-4 engineers). Backstage or Port deployed. Golden path templates with policy guards. Ephemeral per-PR environments for key services. Platform CLI. Scorecards with tech health metrics. Self-service infrastructure catalog (Terraform modules with JSON schema validation).
- **Overkill**: Full platform-as-product with PM, multi-platform-team topology, formal deprecation SLAs, plugin marketplace.
- **Coordination**: Platform team runs weekly office hours. Quarterly developer NPS survey. Cross-team platform RFCs for major changes. Monthly platform review with engineering leadership.
- **Cost**: $300-500K/year (2-4 engineers). Backstage hosting ~$500-1,000/month. Ephemeral env cloud costs ~$2-5K/month.
- **Transition trigger**: >50 engineers, multiple business units, compliance audit requirements; platform team becomes bottleneck.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Multiple platform teams (2-3) with PMs. Platform Product Manager with roadmap. Published platform SLAs (99.9% availability). Developer Relations function. Plugin marketplace for internal tools. Automated compliance in golden paths. Multi-cloud platform support. Dedicated platform SRE rotation. Brownfield migration service offering.
- **What's full production**: Platform NPS dashboard, adoption rate metrics, cost-per-developer tracking, quarterly platform summit, internal conference talks.
- **Coordination**: Platform PM runs quarterly planning. Monthly stakeholder review. Weekly platform team standups. Bi-weekly cross-platform-team sync. Developer advisory board (quarterly).
- **Cost**: $1.5-3M/year (6-12 engineers + PM + DevRel). Portal hosting $5-15K/month. Ephemeral env costs $20-50K/month. Tooling licenses $50-100K/year.
- **Transition trigger**: Platform team becomes bottleneck for >20% of requests; >3 business units with divergent platform needs; developer NPS declining.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | devops-engineer | Infrastructure building blocks (IaC modules, clusters) |
| **This** | platform-engineer | IDP, golden paths, developer portal, self-service APIs |
| **After** | docker-kubernetes | Containerized workloads deployed via platform golden paths |

Common chains:
- **Chain**: devops-engineer → platform-engineer → docker-kubernetes — Infrastructure primitives become self-service; developers deploy containers through golden paths
- **Chain**: cloud-architect → platform-engineer → observability-engineer — Cloud architecture informs platform design; platform provides standard observability across all services

## What Good Looks Like

> Developers self-serve infrastructure through golden paths and never open a ticket for routine tasks like provisioning a service, adding a database, or deploying to staging. The platform enforces security, compliance, and reliability standards automatically — a service that passes the golden path is production-ready by default. Documentation is discoverable, up-to-date, and written at the level of the developer who needs it. Platform adoption grows because the internal developer experience rivals the best SaaS products, and the platform team's backlog is driven by developer feedback, not guesswork.

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|---|---|---|
| `golden-path-design` | Designing the standard path from code to production for new services | What to include, what to leave configurable, policy guard placement |
| `developer-portal` | Implementing Backstage, Port, or Cortex as the developer-facing UI | Service catalog, software templates, tech docs, scorecards, plugin ecosystem |
| `scaffolding-toolchain` | Automating project generation with Cookiecutter, Yeoman, or custom CLI | Template structure, post-generation hooks, template versioning strategy |
| `self-service-infrastructure` | Building Terraform/Pulumi/Crossplane modules teams can consume without platform team | Module design, input validation, policy-as-code (OPA/Sentinel), versioning |
| `ephemeral-environments` | Per-PR, per-branch full-stack environments with automated lifecycle | Namespace isolation, DNS, data seeding, TTL, cost controls, preview URLs |
| `platform-as-product` | Shifting from infrastructure team to product team with roadmap and SLAs | NPS measurement, stakeholder management, deprecation policy, platform marketing |
| `developer-cli` | Building a CLI that wraps platform capabilities into a unified developer experience | CLI framework selection, command design, output formatting, auth, plugin architecture |
| `brownfield-onboarding` | Migrating existing services onto golden paths without disrupting delivery | Migration playbooks, co-investment model, compatibility layers, incremental migration |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -->
- **Platform as product, not project**: maintain a public roadmap, collect NPS, prioritize based on developer-hours-saved. The platform competes for adoption — make it the path of least resistance.
- **Golden paths cover 80%, not 100%**: build paved roads for common patterns; teams can leave the path for specialized needs but own the consequences.
- **Thinnest viable platform**: ship the smallest thing that removes developer toil. A 10-line reusable workflow deployed today beats a full portal launched in 6 months.
- **Self-service by default, concierge for emergencies**: every capability must be consumable without a ticket. Reserve human interaction for design reviews and incidents.
- **Dogfood your own platform**: the platform team deploys the platform using the platform. If the golden path is painful for you, it's unbearable for others.
- **Policy at the platform layer, not in documentation**: enforce security, compliance, and cost controls in templates and pipelines — docs are aspirational; gates are real.
- **Measure what matters**: time-to-first-deploy, deployment frequency, platform NPS, and template adoption rate. Not vanity metrics like "number of templates created."
- **Deprecate with empathy**: minimum 90 days notice, automated migration tooling where possible, and a human to help stuck teams. Killing features builds trust if done well.
- **Platform is a product — staff it like one**: a platform team without a PM is an infrastructure team that takes tickets. Add PM, UX, and DevRel as you scale.
- **Avoid the "platform team as bottleneck" trap**: if every deploy requires platform team approval, you've built a gate, not a platform. Self-service means no human in the loop.


## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|---|---|
| Platform team approves every deploy — 50 deploys/day queue behind 2 platform engineers | Self-service by default: golden paths automate approval; human review reserved for architecture changes and incidents; platform enforces policy, not gates every deploy |
| Golden path covers every edge case — template has 40 parameters, developers afraid to use it | Golden path covers the 80% use case; leave escape hatches for specialized needs; teams that leave the path own their consequences; thinnest viable template wins |
| Platform built in isolation for 12 months — launched to find it solves problems nobody has | Ship the thinnest viable platform in weeks, not months; validate every feature with 3-5 developer design partners; NPS survey before building, not after launching |
| Developer portal is a static wiki — "documentation-driven platform" with no automation | Portal must be the interface to automation: click-to-provision, self-service catalog, automated workflows; documentation tells you what to do; the portal does it for you |
| Platform team has no PM, no roadmap, no NPS — priorities set by whoever shouts loudest in Slack | Platform-as-product: hire or designate a PM, maintain public roadmap, measure NPS quarterly, prioritize by developer-hours-saved; platform competes for adoption |
| Ephemeral environments never get cleaned up — $15K/month in zombie preview environments | Enforce TTL on all ephemeral environments (default 72 hours); automated cleanup after PR merge/close; cost dashboard shows per-PR environment cost |
| Platform deprecation is "we removed the old API, good luck" — 12 teams broken, 0 days notice | Deprecation policy: announce 90 days before, emit warnings at 60 days, sunset at 0; automated migration tooling where possible; human support for stuck teams |
| Template versioning is "copy the latest" — every service runs a different version of the golden path | Version golden path templates with semver; auto-update dependencies via Renovate; publish migration guides between major versions; track adoption by template version |

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Platform migration broke all teams' deployments for 3 days | Migration was planned as a "big bang" cutover with no backward compatibility layer. All teams had to migrate simultaneously or be left behind. | Plan platform changes as a gradual migration with backward compatibility. Run old and new systems in parallel during the transition period. Allow teams to migrate at their own pace within a defined window. Test the migration path with one early-adopter team before rolling out to all teams. | A platform migration without a parallel run is a deployment blockade. Always provide a migration path, not a migration deadline. |
| Shared development cluster becomes unusable during peak hours | All teams share a single Kubernetes cluster with no resource quotas or namespace limits. One team's CI pipeline consumes all available CPU, blocking everyone else. | Implement resource quotas (ResourceQuota) per namespace. Use cluster autoscaling to add nodes on demand. Isolate CI workloads to a separate cluster or dedicated node pool. Implement priority classes so production workloads always preempt batch jobs. | Shared infrastructure without isolation guarantees contention. Every team should have a resource budget that no other team can consume. |
| API deprecation broke 12 downstream services — no notice was sent | Platform team removed an internal API without notifying consumers. There was no deprecation tracking system or consumer registry. | Maintain a service catalog that tracks API consumers. Implement a deprecation policy: announce (90 days before), warn in API responses (60 days), sunset (0 days). Send deprecation notices through the developer portal, Slack, and email — never rely on a single channel. | The platform team knows when APIs change; downstream teams don't. Deprecation without notification is unilateral system breakage. |
| Golden path template is 8 months out of date — all new services start with security vulnerabilities | Template was created once and never updated. New frameworks, libraries, and security practices were never backported. | Treat golden path templates as living software products, not static documents. Assign ownership for each template. Run automated dependency updates on templates. Version templates and test them quarterly against the latest security baseline. | A stale golden path is worse than no golden path — it gives false confidence while shipping known vulnerabilities. |
| Developer NPS dropped from 45 to -12 after platform portal launch | Platform team spent 6 months building a full Backstage portal without any developer input. The portal was slow, had confusing navigation, and didn't solve developers' actual pain points. | Validate every platform feature with real developers before building. Run design sprints with 3-5 developer design partners. Ship the thinnest viable version — a 10-line reusable workflow deployed today beats a full portal launched in 6 months. | The biggest platform risk is building the wrong thing for 6 months. Validate with users before investing in implementation. |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Golden path template produces a deployable service in < 1 hour from scaffold
- [ ] **[S2]**  Service catalog auto-discovers 100% of production services with owner and on-call metadata
- [ ] **[S3]**  Self-service infrastructure modules covered: compute, database, cache, queue, object storage, secrets
- [ ] **[S4]**  CI/CD pipeline template enforces lint → test → build → security scan → deploy with quality gates
- [ ] **[S5]**  Platform availability SLA published and monitored (target: 99.9% during business hours)
- [ ] **[S6]**  Ephemeral environments auto-provision on PR open and auto-destroy within 48 hours of merge/close
- [ ] **[S7]**  Cost tags applied automatically by all golden path templates (`Environment`, `Service`, `Team`, `CostCenter`)
- [ ] **[S8]**  Platform changelog updated with every release; breaking changes communicated 30+ days in advance
- [ ] **[S9]**  Quarterly developer NPS survey completed with action items tracked to resolution
- [ ] **[S10]**  Scorecard health metrics defined and visible: CI status, dependency freshness, coverage, SLO compliance, security scans
- [ ] **[S11]**  Platform on-call rotation established with runbooks for common incidents (portal down, template failure, module error)
- [ ] **[S12]**  Onboarding guide reduces time-to-first-deploy to < 1 day for new engineers
- [ ] **[S13]**  Deprecation tracker shows migration status for all deprecated features
- [ ] **[S14]**  Brownfield migration playbook exists for services not yet on golden paths

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Team Topologies](https://teamtopologies.com/) — Conway's Law, stream-aligned teams, enabling teams, platform as product
- [Backstage](https://backstage.io/) — Spotify's open-source developer portal
- [Port](https://www.getport.io/) — Developer portal SaaS with self-service actions
- [Humanitec Platform Engineering](https://platformengineering.org/) — Reference architectures and maturity model
- [DORA Metrics](https://dora.dev/) — Deployment frequency, lead time, MTTR, change failure rate
- [Cookiecutter](https://github.com/cookiecutter/cookiecutter) — Project templating for any language
- Internal: [../../domain/references/platform-engineering-patterns.md](../../domain/references/) — Detailed patterns for IDP components
