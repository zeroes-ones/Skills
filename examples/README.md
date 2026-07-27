# Examples — Skills in Action

Real projects demonstrating how skills chain together. Each example shows a different activation pattern.

---

## LogSnap — Solo Engineer: Idea to $25K MRR

**[`logsnap-solo-to-scale/`](logsnap-solo-to-scale/)**

**Pattern:** Tiered activation — start lean, add skills as you grow.

| Tier | Skills | MRR | What It Demonstrates |
|------|--------|-----|---------------------|
| **Solo** (Month 0-1) | 8 skills | $0 → $120 | MVP shipping: idea-to-spec → backend → frontend → review → deploy. Deliberately skips CI/CD, monitoring, legal, analytics. Ships in 4 weeks on a $20 VPS. |
| **Grow** (Month 2-6) | 18 skills | $120 → $3,100 | Adding what hurts: CI/CD when deploying 3x/day, observability when woken at 3am, SEO when organic traffic stalls, analytics when churn is unknown, GDPR when first EU customer signs. |
| **Full** (Month 7-18) | 56 skills | $3,100 → $25,000 | Scaling to a team: microservices extraction, SOC 2 compliance, multi-region, canary deploys, error budgets, chaos engineering, devrel, international SEO. |

**Key insight:** You don't need 56 skills to ship. You need 8. Add skills when pain exceeds overhead.

**To run it yourself:**
```bash
cd my-saas-idea
skills-init --solo
# ... 6 months later ...
skills-init --grow
# ... 18 months later ...
skills-init --full
```

---

## Orchestra Platform — Full Team, All Skills

**[`orchestra-platform/`](orchestra-platform/)**

**Pattern:** Full activation — all domains from strategy through operations.

A VC-funded team building a collaborative music production platform. Demonstrates:

- **Strategy phase:** CEO-strategist → business-strategist → product-strategist (market sizing, fundraising deck, OKRs)
- **Product phase:** UX researcher → product manager → idea-to-spec (personas, PRD, user stories)
- **Design phase:** UI/UX designer → accessibility auditor → brand guidelines (design system, WCAG 2.2 AA, visual identity)
- **Architecture phase:** System architect → API designer → database designer → networking engineer (C4 diagrams, ADRs, schema design)
- **Development phase:** Backend → frontend → mobile → fullstack (multi-platform, offline-first, localization)
- **Quality phase:** Code reviewer → QA engineer → security reviewer → accessibility testing (6-dimension review, OWASP, a11y gates)
- **DevOps phase:** CI/CD → observability → Docker/K8s → cloud architect → platform engineer → SRE → release manager → FinOps
- **Security phase:** Security engineer → compliance officer → incident responder (SOC 2, ISO 27001, IR runbooks)
- **Legal phase:** Legal advisor → GDPR/privacy → regulatory specialist

**Organized by domain folder** — each domain has its own subdirectory with skill-specific outputs. 30+ files showing real artifacts.

---

## UOA Options Trading — Domain-Specific Pipeline

**[`uoa-options-trading/`](uoa-options-trading/)**

**Pattern:** Domain extension — finance skills + existing data/dev skills.

A solo quant trader building an Unusual Options Activity (UOA) detection and execution system. Demonstrates:

- **Data pipeline:** market-data-engineer → data-engineer → database-reliability-engineer
- **Signal detection:** quantitative-analyst (premium ≥ $1M, mid-cap, ATM/OTM, 7-365 DTE)
- **Trade execution:** algorithmic-trader → backend-developer (Kelly sizing, trailing stops, trim ladders)
- **Monitoring:** frontend-developer → observability-engineer → analytics-engineer (P&L dashboard, Sharpe ratio, drawdown)
- **Risk:** data-scientist (backtesting) → qa-engineer (execution verification) → incident-responder (market hours runbook)

**Key insight:** Domain-specific skills (market-data-engineer, quantitative-analyst, algorithmic-trader) extend the library without duplicating general skills (data-engineer, data-scientist).

---

## Skill Activation by Example

| Example | Skills Used | Best For |
|---------|------------|----------|
| **LogSnap Solo** | 8 | Weekend projects, prototypes, indie hackers |
| **LogSnap Grow** | 18 | Side projects with users, open source, early startups |
| **LogSnap Full** | 56 | Growing SaaS, hiring first employees |
| **Orchestra Platform** | 106+ | Funded startups, enterprise teams, all-domains coverage |
| **UOA Trading** | 15 | Domain-specific pipelines (finance, health, gaming, etc.) |

---

## How to Read an Example

Each example follows this structure:

1. **The Story** — Who is building this? What's their context? Why these skills?
2. **The Chain** — ASCII dependency graph showing which skills feed into which
3. **Per-Skill Outputs** — What each skill actually produced (not theory — concrete artifacts)
4. **Decision Points** — Critical choices made at each skill boundary
5. **Results** — Metrics before and after (MRR, churn, deploy frequency, incident MTTR, etc.)

The artifacts are in domain-specific subdirectories. For instance, `orchestra-platform/04-architecture/system-arch.md` is the actual output the system-architect skill produced for the Orchestra project.

---

*These examples are living documents. As skills evolve, the examples update to reflect new capabilities. Run `skills-update` to get the latest.*
