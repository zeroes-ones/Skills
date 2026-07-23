# Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: You are the CTO + every engineer. Build-vs-buy = buy everything (Auth0, Supabase, Vercel). Tech debt is intentional — ship fast. No governance needed. Hiring = none yet.
- **What to skip**: Architecture review boards. RFC processes. Technology radars. Tech due diligence. Vendor scorecards (just use what works).
- **Coordination**: You talk to yourself. Document decisions in a `decisions.md` file.

### Small Team (2-10 people, 100-10K users)
- **What changes**: First engineering hires (generalists). Start build-vs-buy analysis for core infra. Lightweight ADRs for key decisions. Quarterly tech debt assessment. Simple tech radar (Adopt/Hold). Vendor evaluation for 2-3 critical services.
- **What to skip**: Formal ARB. Dual-track career ladder (too early). Platform team (stream-aligned teams are enough). Innovation funnel (just do hackathons).
- **Coordination**: Weekly eng sync (30 min). Monthly tech strategy review with CEO. Bi-weekly 1:1s. ADRs in shared repo.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: VP Engineering hired. Team Topologies emerge (stream-aligned + platform). Formal ARB with monthly cadence. RFC process for cross-cutting decisions. Technology radar reviewed quarterly. Dual-track career ladder. Innovation time (10-20% Fridays). Tech due diligence for enterprise deals.
- **What to skip**: Dedicated innovation team (embed in streams). Multi-year technology roadmaps (6-month rolling is enough). Full-time developer experience team.
- **Coordination**: ARB monthly. RFCs async in shared repo. Quarterly tech strategy review with board. Monthly skip-level 1:1s.

### Enterprise (50+ people, 1M+ users)
- **What changes**: CTO + VPs for each pillar. Multiple platform teams. ARB with formal voting. Enterprise architecture function. Compliance-driven governance (SOC 2, FedRAMP). Technology radar + lifecycle management. Dedicated DevEx team. M&A technical due diligence capability. Patent/IP strategy.
- **What's full production**: Architecture governance board with cross-BU representation. Annual technology strategy with board sign-off. Formal build-vs-buy with procurement partnership. Innovation lab + corporate venture arm.
- **Coordination**: ARB bi-weekly. Quarterly CTO council. Annual architecture summit. Board technology committee.

### Transition Triggers
- **Solo → Small**: You can't ship fast enough alone. First eng hire needed to maintain velocity. >100 active users.
- **Small → Medium**: Coordination overhead between 3+ teams becomes painful without process. First enterprise customer asks about architecture governance.
- **Medium → Enterprise**: Multiple business units need technology alignment. IPO or large M&A on horizon. SOC 2/ISO 27001 audit required.


### War Story 1 — The Kubernetes Migration That Consumed a Year
**Symptom:** A 15-engineer startup decided to migrate from Heroku to Kubernetes to "prepare for scale." The migration took 12 months instead of the planned 3. During that time, zero new features shipped. Two competitors launched and captured market share.
**Root cause:** The CTO chose a "modern" infrastructure stack without assessing team readiness. No one had production K8s experience. The team spent 6 months learning K8s, 4 months fighting YAML drift, and 2 months debugging networking issues.
**Fix:** Adopted a "simplest infrastructure that works" policy: use managed services (Railway, Render, or single-region ECS) until the team has dedicated DevOps headcount and >10K RPS per service. K8s only when you have 3+ engineers with K8s production experience.
**Lesson:** Infrastructure decisions are team-readiness decisions, not architecture decisions. The cost of complexity isn't just the migration — it's the opportunity cost of every feature not shipped during the migration.

### War Story 2 — The Build-Vs-Buy Decision That Cost $2M
**Symptom:** A Series B company decided to build its own identity and authorization system because "auth is core to our product." Eighteen months and 6 engineers later, the system still had gaps (no SSO, flaky MFA, no audit logging) and was blocking enterprise deals.
**Root cause:** The "build vs buy" analysis compared license cost ($120K/yr for Auth0) against 6 months of engineering time ($540K). But it ignored ongoing maintenance, security compliance, and the opportunity cost of not having enterprise features.
**Fix:** Adopted a strict triage: build only what creates competitive advantage. Auth, payments, monitoring, and CI/CD are always buy. The engineering time "saved" by buying pays for itself in faster feature delivery.
**Lesson:** Build-vs-buy analysis must include 5-year TCO, maintenance burden, security compliance cost, and opportunity cost of delayed features. If it's not a competitive differentiator, buy it.

### War Story 3 — The Database That Became the Single Point of Failure
**Symptom:** A team built their entire product on MongoDB because "schemas are flexible and it's faster to iterate." At 50K users, queries that took 5ms became 5-second nightmares. Data inconsistencies caused customer-facing bugs weekly.
**Root cause:** The CTO chose MongoDB for its developer experience without understanding the data access patterns. The product was deeply relational (users, orders, payments, subscriptions) — exactly what MongoDB was not designed for.
**Fix:** Migrated to PostgreSQL using a carefully planned backfill strategy. The 6-month migration was painful, but query performance improved 100x and data consistency issues disappeared entirely.
**Lesson:** Choose your database based on data access patterns, not developer convenience. Relational data belongs in PostgreSQL. The cost of migrating databases in production is 10-100x the cost of choosing right the first time.
