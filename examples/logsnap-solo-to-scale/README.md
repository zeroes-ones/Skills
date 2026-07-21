# LogSnap — Solo Engineer: Idea to MVP to Scale

A practical example of how a solo engineer uses tiered skill activation to go from idea to profitable SaaS — activating skills only when you need them, not all at once. This isn't Orchestra (the big-team, VC-funded, all-56-skills example). This is you, a laptop, and a product you ship this month.

## The Scenario

You're building **LogSnap** — a simple uptime monitoring + status page SaaS. You check URLs every 60 seconds, send alerts when they go down, and give each customer a public status page. Competitors exist (Better Uptime, UptimeRobot, Statuspage) but they're either expensive or clunky.

You're solo. No team. No funding. You want to ship an MVP in 4 weeks and get to $3K MRR in 6 months.

## The Tiered Approach

```
TIME ──────────────────────────────────────────────────────────────►

Month 0-1          Month 2-6           Month 7-18
──SOLO──►          ──GROW──►           ──FULL──►

8 skills           18 skills            56 skills
MVP shipped         $3K MRR              $25K MRR, hiring
1 user (you)        50 customers         500 customers
SQLite + 1 VPS      PostgreSQL + AWS     Multi-region + SOC 2
No CI/CD            GitHub Actions       DORA metrics, SLOs
No monitoring       Basic alerts         Full observability
```

The critical insight: **you don't need 56 skills to ship**. You need 8. Then you add skills as you add complexity. Every skill you skip at the solo stage saves you 2-40 hours. Every skill you add at the grow/full stage prevents a production outage or compliance blocker.

## Phase 1: Solo MVP (8 skills, 4 weeks)

**Activation:** `./scripts/init-project.sh --solo --name logsnap`

### Skill Chain

```
idea-to-spec ──► system-architect ──► backend-developer
     │                                       │
     ▼                                       ▼
frontend-developer ◄── ui-ux-designer ──► code-reviewer
     │
     ▼
qa-engineer ──► docker-kubernetes
```

### What Each Skill Produces

| Skill | Input | Output | Time Saved |
|-------|-------|--------|------------|
| **idea-to-spec** | "I want to build uptime monitoring" | PRD: 3 core features (monitor, alert, status page), out of scope (team plans, SSO, API), success metric: 1st paying customer in 30 days. See [01-solo-mvp/spec.md](01-solo-mvp/spec.md) | 3 days of thrashing on scope |
| **ui-ux-designer** | Spec, competitor screenshots | 6 screens designed (dashboard, monitor list, monitor detail, alert rules, status page, settings). Mobile-first, one color. See [01-solo-mvp/design.md](01-solo-mvp/design.md) | 1 week of redesign |
| **system-architect** | Spec, scale expectations (100 monitors, solo) | ADR: Monolith over microservices (you're solo). PostgreSQL over MongoDB (you'll need joins later). Go for backend (fast, single binary deploy). Next.js for frontend (SSR for status pages). Cron-based checks, not event-driven. See [01-solo-mvp/architecture.md](01-solo-mvp/architecture.md) | 2 weeks of over-engineering |
| **backend-developer** | Architecture, spec | Go monolith: POST /monitors, GET /monitors/:id/checks, POST /alerts/rules, GET /status/:team. SQLite in dev, PostgreSQL in prod. One binary, one command to start. See [01-solo-mvp/backend.md](01-solo-mvp/backend.md) | 1 week of decision paralysis |
| **frontend-developer** | API spec, design | Next.js app: dashboard (monitor list + status), monitor detail (uptime graph, check history), alert rules (threshold + notification), status page (public, branded). Tailwind CSS, no component library. See [01-solo-mvp/frontend.md](01-solo-mvp/frontend.md) | 1 week of CSS hell |
| **code-reviewer** | All code | PR review: 3 issues found (missing input validation on URL field — lets users add `javascript:alert(1)`, SQL injection in monitor search, unhandled promise in check runner). All fixed before ship. | 1 incident in production |
| **qa-engineer** | Feature list, deployed staging | Test cases: 18 (6 happy path, 6 edge case, 6 error), manual for now. Found: monitor check fails silently when timeout > 60s, status page renders blank if no checks exist, alert fires twice when monitor flaps. All fixed. See [01-solo-mvp/qa.md](01-solo-mvp/qa.md) | 2 support tickets from angry users |
| **docker-kubernetes** | Backend + frontend | Dockerfile (multi-stage, Go binary 14MB), docker-compose (app + postgres + redis), deploy to single $20/mo VPS via docker-compose. No Kubernetes yet — that's phase 3. | Zero "works on my machine" |

### MVP Ship Checklist

- [x] Monitor CRUD + 60-second checks working
- [x] Email alert when monitor goes down (via Resend, free tier: 100/day)
- [x] Public status page per team (yourstatus.logsnap.dev/teamname)
- [x] Stripe checkout ($9/mo for 10 monitors, $29/mo for 50)
- [x] SSL via Caddy (auto-renew)
- [x] Daily DB backup to S3 (shell script + cron)
- [x] Error logging to a file (you'll add proper observability in phase 2)

**What you deliberately skip in solo phase:**
- Authentication (everyone gets a magic link via email — you add Google OAuth in phase 2)
- CI/CD (you `git push && ssh deploy` — you add GitHub Actions in phase 2)
- Monitoring (you check the server once a day — you add proper monitoring in phase 2)
- Legal docs (you add ToS + privacy policy in phase 2)
- Multi-tenancy isolation (one DB, team_id column — you fix this in phase 3)
- Automated tests (you test manually — you add tests in phase 2)
- Analytics (you ask customers what they want — you add analytics in phase 2)

**Total time to MVP:** 4 weeks (nights + weekends)
**Total infra cost:** $29/mo ($20 VPS + $9 domain)
**First paying customer:** Day 28 (Product Hunt launch)

## Phase 2: Grow — First Customers to $3K MRR (18 skills, 5 months)

**Activation:** `./scripts/init-project.sh --grow --name logsnap`

### New Skills Activated (+10)

```
──SOLO──► + ──GROW──►

business-strategist ──► growth-engineer ──► seo-specialist
product-manager ──► analytics-engineer
ci-cd-builder ──► observability-engineer
incident-responder
gdpr-privacy ──► legal-advisor
content-strategist ──► technical-writer
```

### What Changed

| Skill | Trigger | What It Produced |
|-------|---------|-----------------|
| **business-strategist** | "Should I raise or bootstrap?" | Decision: bootstrap. $3K MRR growing 15% month, LTV $240 (avg 8-month retention × $30/mo), CAC $15 (content marketing), LTV:CAC 16:1. VC path needs $30M+ TAM — LogSnap's is $2B but fragmented. Bootstrap, keep 100% equity. |
| **product-manager** | 50 customers, feedback piling up | Roadmap: Q1 (team plans, Google OAuth, webhook alerts), Q2 (API, Slack integration, custom domains), Q3 (incident templates, scheduled maintenance). RICE-scored. "Add webhook alerts" wins (RICE: 90). |
| **growth-engineer** | Stuck at 40 customers, conversion flat | A/B test: homepage CTA "Start free trial" (3.1%) vs "Monitor your first URL in 60 seconds" (5.4%), p=0.02, n=600. Shipped. Added onboarding checklist inside product — activation rate from 42% to 68%. |
| **seo-specialist** | Organic traffic at 200 visits/month | Keyword strategy: "uptime monitoring tool" (12K/mo), "free status page" (8K/mo), "website monitoring service" (5K/mo). Built 3 comparison pages (LogSnap vs Better Uptime/Pingdom/UptimeRobot). Traffic: 200 → 1,200/month in 3 months. |
| **analytics-engineer** | "Why do users churn?" | dbt models from PostgreSQL + Stripe. Found: users who set up 3+ monitors in first 48 hours retain at 82% vs 34% for those who don't. Built "Add your 3 most important URLs" onboarding step. Churn dropped from 8% to 4.2%. |
| **ci-cd-builder** | "Deploying manually 3x a day is eating my time" | GitHub Actions: lint → test → build → deploy. 8-minute pipeline. Feature branches auto-deploy to preview environments. Main branch deploys to production. Rollback: `git revert && git push` (5 minutes). |
| **observability-engineer** | Woken up at 3am because the check runner silently died | Prometheus + Grafana (free tier): uptime dashboard, check success rate, alert latency. 3 SLOs: check execution > 99.5% success, alert delivery < 60s p95, status page load < 500ms. Alert: "Check runner not processing for 5 minutes" → PagerDuty. |
| **incident-responder** | First real outage: DB filled up, all monitors stopped for 4 hours | Postmortem: no disk alert, no auto-vacuum, no runbook. Fixes: disk usage alert at 70%, auto-vacuum enabled, runbook written. Incident response plan: severity levels, customer communication template. |
| **gdpr-privacy + legal-advisor** | First EU customer asks for DPA | Privacy policy + ToS (generated, reviewed by attorney), DPA signed, cookie consent banner (no analytics cookies without opt-in), data processing inventory (monitor URLs, check results, email addresses). |
| **content-strategist + technical-writer** | Need scalable customer acquisition | Blog (2x/month): "How we built a status page in 200 lines of Go," "Monitoring vs observability for indie hackers." Changelog. API docs (OpenAPI → Stoplight). Knowledge base (15 articles: getting started, alert configuration, status page customization). |

### Results at End of Phase 2

| Metric | Start | End |
|--------|-------|-----|
| MRR | $120 | $3,100 |
| Customers | 4 | 52 |
| Churn | Unknown | 4.2%/month |
| Infrastructure | $29/mo | $145/mo |
| Time spent on ops | 8 hrs/week | 3 hrs/week (automation) |
| Hours before incident detection | Unknown (user reported) | 5 minutes (automated) |

## Phase 3: Full Scale — $3K to $25K MRR (56 skills, 12 months)

**Activation:** `./scripts/init-project.sh --full --name logsnap`

### New Skills Activated (+38)

All remaining skills from domains: strategy (ceo-strategist, cto-advisor, product-strategist), design (brand-guidelines, accessibility-auditor), architecture (api-designer, database-designer, networking-engineer), development (fullstack-developer, mobile-developer, localization-engineer), quality (security-reviewer), devops (cloud-architect, devops-engineer, finops-engineer, platform-engineer, release-manager, site-reliability-engineer), security (security-engineer, compliance-officer), data (data-engineer, data-scientist, database-reliability-engineer, ml-ai-engineer), growth (devrel-advocate), legal (regulatory-specialist), operations (customer-support-engineer, project-manager, scrum-master, technical-program-manager), specialized (chaos-engineer, documentation-engineer, migration-architect, monorepo-manager, performance-engineer).

### What Changes in Full Scale

| Domain | Trigger | Key Decisions |
|--------|---------|---------------|
| **Strategy** | Growing team (3 engineers, 1 support, 1 sales), considering Series A | ceo-strategist: Don't raise yet — $25K MRR growing 12%/month, profitable ($18K expenses), 10 months to $100K MRR at current rate. CTO-advisor: Hire for scale (distributed systems engineer), migrate to microservices at $50K MRR, not now. |
| **Architecture** | 500 customers, DB is the bottleneck | system-architect: Extract check-runner into separate service. api-designer: Public API with rate limiting + API keys (customers asking for it). database-designer: Read replicas for status pages (they get 50K views/day). networking-engineer: CDN for status pages (CloudFront, 90% cache hit rate). |
| **Security & Compliance** | Enterprise customer asks: "Are you SOC 2 compliant?" | security-engineer: Penetration test (3 medium findings, all fixed). IAM hardening. Secrets rotation. compliance-officer: SOC 2 Type I audit (4 weeks, 32 controls, 3 gaps — fixed within 30 days). |
| **Data** | Need to understand power users vs churn risks | data-engineer: ETL pipeline (PostgreSQL → BigQuery via Airbyte), dbt models for product analytics. data-scientist: Churn prediction model (features: check frequency, alert count, team size — AUC 0.84). ml-ai-engineer: "Smart alerts" — anomaly detection on response times, reduces false positives by 40%. |
| **DevOps** | Deploying 5x/day, one bad deploy took status pages down | cloud-architect: Multi-AZ (finally). devops-engineer: Terraform for everything, GitOps with ArgoCD. release-manager: Canary deploys (10% → 50% → 100%), feature flags. site-reliability-engineer: Error budgets, toil automation (4 automated processes, 12 hrs/week saved). chaos-engineer: GameDay — killed a check-runner instance, system self-healed in 45 seconds. |
| **Operations** | First hire (support engineer), then 3 more engineers | scrum-master: 2-week sprints, retrospectives, velocity tracking. project-manager: RAID log, stakeholder updates. customer-support-engineer: Intercom + knowledge base (75 articles). technical-program-manager: Cross-team initiatives (API launch, SOC 2, multi-region). |
| **Growth** | $25K MRR, targeting $100K | devrel-advocate: Sample integrations on GitHub, "How to monitor your API" workshop. seo-specialist: International SEO (German, French). documentation-engineer: Docs site (Docusaurus), docs-as-code pipeline. monorepo-manager: 3 repos merged (frontend, backend, docs) with Turborepo. performance-engineer: Status page load: 2.3s → 400ms (CDN + Edge Functions + ISR). |

### Full Scale Results

| Metric | Phase 2 End | Phase 3 End |
|--------|------------|------------|
| MRR | $3,100 | $25,000 |
| Customers | 52 | 480 |
| Team | 1 (you) | 6 (3 eng, 1 support, 1 sales, 1 content) |
| Infrastructure | $145/mo | $2,800/mo |
| Uptime | 99.2% (best-effort) | 99.95% (SLO-backed) |
| Deploy frequency | 3/week | 5/day |
| Incident MTTR | 4 hours | 12 minutes |
| SOC 2 | No | Type I (Type II in progress) |
| Churn | 4.2% | 2.8% |

## The Tiered Skill Map

Here's exactly which skills activate at each tier:

```
──SOLO── (8 skills)
├── 02-product: idea-to-spec
├── 03-design: ui-ux-designer
├── 04-architecture: system-architect
├── 05-development: backend-developer
├── 05-development: frontend-developer
├── 06-quality: code-reviewer
├── 06-quality: qa-engineer
└── 07-devops: docker-kubernetes

──GROW── (+10 skills, 18 total)
├── 01-strategy: business-strategist
├── 02-product: product-manager
├── 07-devops: ci-cd-builder
├── 07-devops: observability-engineer
├── 08-security: incident-responder
├── 09-data: analytics-engineer
├── 10-growth: growth-engineer
├── 10-growth: seo-specialist
├── 10-growth: content-strategist
├── 11-legal: gdpr-privacy
├── 11-legal: legal-advisor
└── 12-operations: technical-writer

──FULL── (+38 skills, 56 total)
Everything else — all 13 domains, complete coverage
```

## Key Lessons for Solo Engineers

1. **Start with 8 skills, not 56.** The solo tier exists because shipping something that works is more important than shipping something perfect. Every skill you skip saves 2-40 hours.
2. **Add skills when pain exceeds overhead.** You don't need CI/CD when you deploy once a week. You need it when you deploy 3 times a day. You don't need SLOs with 50 customers. You need them with 500.
3. **The tiered system is a playbook, not a checklist.** Use `--solo` to ship fast. When you hit traction, run `--grow` against your existing project — it'll add what you need without rebuilding what you have.
4. **Security and legal are not optional, even solo.** GDPR applies if you have EU customers, regardless of company size. Your privacy policy doesn't need to be complex, but it needs to exist.
5. **The biggest mistake solo engineers make is over-engineering before product-market fit.** Microservices, Kubernetes, event-driven architecture — these solve problems you don't have yet. A Go monolith on a $20 VPS can serve 10,000 monitors. Start there.

## Running This Example Yourself

```bash
# Starting a new solo project
cd my-saas-idea
/path/to/skills/scripts/init-project.sh --solo --name my-project

# 6 months later, when you have traction
/path/to/skills/scripts/init-project.sh --grow --name my-project

# 18 months later, when you're scaling
/path/to/skills/scripts/init-project.sh --full --name my-project
```

Each activation adds the skills relevant to your current stage without replacing what you already built.

---

*This example demonstrates tiered skill activation — the same approach used by the [zeroes-ones/Skills](https://github.com/zeroes-ones/Skills) library. Compare with [Orchestra Platform](../orchestra-platform/) for the big-team, all-56-skills approach.*
