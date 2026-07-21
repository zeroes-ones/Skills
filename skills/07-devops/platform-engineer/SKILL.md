---
name: platform-engineer
description: Internal Developer Platform (IDP) design, golden paths, Backstage, self-service infrastructure, developer portals, scaffolding, developer experience (DX), platform as product. Works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI.
author: Sandeep Kumar Penchala
---

# Platform Engineer / Developer Experience (DX)

Design and operate an Internal Developer Platform that transforms infrastructure into a product.
Covers IDP architecture, golden path templates, self-service IaC modules, developer portal
implementation (Backstage, Port, Cortex), scaffolding toolchains, ephemeral environments, platform
APIs, service catalogs, scorecards, and the platform-as-product operating model.

## Decision Trees

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
```

## Core Workflow

### Phase 1: Platform Discovery and Strategy
1. **Map the developer journey**: from laptop setup → first commit → deploy → monitor → incident response.
   - Output: Developer journey map with pain points, time-to-X metrics per phase.
2. **Identify top 3 friction points**: survey developers, measure DORA metrics, time-to-10th-pr.
   - Input: Developer experience survey (NPS + qualitative), pipeline data, onboarding logs.
   - Output: Prioritized backlog ranked by developer-hours-saved per sprint.
3. **Define platform North Star metrics**: time-to-first-deploy, deployment frequency, onboarding time, platform NPS.
   - Output: Dashboard with baseline measurements, 6-month targets.
4. **Select platform team model**: embedded, consulting, enabling, or product — based on org size (see Decision Tree #4).
   - Output: Team charter with mission, operating model, and stakeholder map.

### Phase 2: Golden Path Design
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

### Phase 3: Developer Portal
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

### Phase 4: Environment-as-a-Service
1. **Design ephemeral environment lifecycle**: per-PR namespace, provision on PR open, tear down on merge/close.
   - Output: Architecture for namespace isolation, DNS routing, data seeding.
2. **Implement provisioning automation**: Terraform/Tilt/Garden Garden that spins up a full stack per PR.
   - Input: Service dependency graph, infrastructure module catalog.
   - Output: `pr-<number>.dev.example.com` fully functional within 5 minutes of PR open.
3. **Add cost controls**: TTL-based auto-cleanup (default 48h), per-team budget caps, idle detection.
   - Output: Dashboard showing ephemeral environment spend per team per month.

### Phase 5: Platform as Product Operations
1. **Establish platform SLAs**: availability (99.9%), template freshness (< 30 days behind), support response (< 4h during business hours).
   - Output: Published SLA page visible to all developers.
2. **Run quarterly developer NPS survey**: measure satisfaction, collect feature requests, identify deprecation candidates.
   - Output: NPS score trend, top-5 feature requests, bottom-3 pain points.
3. **Maintain platform changelog**: every change communicated via portal, Slack, and office hours.
   - Output: Changelog page, #platform-announcements channel, weekly office hours.
4. **Deprecation process**: announce → deprecation warning in tooling → migration guide → removal (minimum 90 days).
   - Output: Deprecation tracker with migration status per team.

## Cross-Skill Coordination

| Coordinate With | When | What to Share/Ask |
|---|---|---|
| **DevOps Engineer** | Infrastructure module design, CI/CD template creation | Golden path requirements, module API contracts, pipeline template needs |
| **Cloud Architect** | Landing zone integration, network topology for platform | Platform requirements for account isolation, VPC design, IAM guardrails |
| **CI/CD Builder** | Pipeline template design, reusable workflow authoring | Developer UX expectations, caching patterns, quality gate standards |
| **SRE** | Platform SLA definition, observability integration, incident response | Platform reliability targets, SLO definitions, on-call rotation design |
| **Security Engineer** | Policy guardrails, secret management, compliance automation | Least-privilege templates, vulnerability scanning in golden paths, audit requirements |
| **Backend Developer** | Design-partner feedback, template validation, friction discovery | Developer journey pain points, template usability feedback, feature requests |
| **Frontend Developer** | Portal UX design, scaffolding tooling, developer CLI | Portal usability, CLI ergonomics, onboarding experience feedback |
| **Technical Writer** | Golden path documentation, runbooks, portal content | Documentation structure, runbook templates, onboarding guide content |
| **Release Manager** | Deployment window coordination, feature flag integration | Platform deploy schedule, environment promotion workflow |
| **FinOps Engineer** | Cost allocation tags, ephemeral environment budgets, RI coverage | Resource tagging in templates, cost visibility for self-service resources |

### Escalation Path
```
Platform adoption blocked by team resistance? → Engineering Manager → CTO
Platform outage blocking all deploys? → SRE Incident Commander → CTO
Security finding in golden path template? → Security Engineer → Compliance Officer
Platform cost exceeding budget? → FinOps Engineer → CTO
Architecture deadlock on platform direction? → Cloud Architect → CTO Advisor
```

## Scale Depth

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

## Sub-Skills

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

## Production Checklist

- [ ] Golden path template produces a deployable service in < 1 hour from scaffold
- [ ] Service catalog auto-discovers 100% of production services with owner and on-call metadata
- [ ] Self-service infrastructure modules covered: compute, database, cache, queue, object storage, secrets
- [ ] CI/CD pipeline template enforces lint → test → build → security scan → deploy with quality gates
- [ ] Platform availability SLA published and monitored (target: 99.9% during business hours)
- [ ] Ephemeral environments auto-provision on PR open and auto-destroy within 48 hours of merge/close
- [ ] Cost tags applied automatically by all golden path templates (`Environment`, `Service`, `Team`, `CostCenter`)
- [ ] Platform changelog updated with every release; breaking changes communicated 30+ days in advance
- [ ] Quarterly developer NPS survey completed with action items tracked to resolution
- [ ] Scorecard health metrics defined and visible: CI status, dependency freshness, coverage, SLO compliance, security scans
- [ ] Platform on-call rotation established with runbooks for common incidents (portal down, template failure, module error)
- [ ] Onboarding guide reduces time-to-first-deploy to < 1 day for new engineers
- [ ] Deprecation tracker shows migration status for all deprecated features
- [ ] Brownfield migration playbook exists for services not yet on golden paths

## References

- [Team Topologies](https://teamtopologies.com/) — Conway's Law, stream-aligned teams, enabling teams, platform as product
- [Backstage](https://backstage.io/) — Spotify's open-source developer portal
- [Port](https://www.getport.io/) — Developer portal SaaS with self-service actions
- [Humanitec Platform Engineering](https://platformengineering.org/) — Reference architectures and maturity model
- [DORA Metrics](https://dora.dev/) — Deployment frequency, lead time, MTTR, change failure rate
- [Cookiecutter](https://github.com/cookiecutter/cookiecutter) — Project templating for any language
- Internal: [../../domain/references/platform-engineering-patterns.md](../../domain/references/) — Detailed patterns for IDP components
