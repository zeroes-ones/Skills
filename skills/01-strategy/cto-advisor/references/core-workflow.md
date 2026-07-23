# Core Workflow — Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Technology Strategy

**Build vs Buy Framework:**

```
Can this be a competitive differentiator?
├── YES → Does building give us a moat that buying doesn't?
│   ├── YES → BUILD (invest heavily)
│   └── NO  → Can we customize an off-the-shelf solution?
│       └── YES → BUY + customize
│
└── NO → Is there a mature, well-supported solution available?
    ├── YES → BUY (don't reinvent the wheel)
    └── NO  → Is the market nascent but strategically adjacent?
        ├── YES → BUILD (first-mover advantage possible)
        └── NO  → WAIT (let the market mature, then buy)
```


**What good looks like:** Technology radar document published and reviewed with the engineering team — every major dependency has a clear Adopt/Trial/Assess/Hold rating with written rationale. The last 3 build-vs-buy decisions are documented with 5-year TCO, alternatives considered, and accepted tradeoffs. A new CTO can read the radar and understand why every technology choice was made within an afternoon.

**Build-vs-buy cost comparison (5-year TCO):**

| Cost Factor               | Build                     | Buy (SaaS)          |
|----------------------------|---------------------------|---------------------|
| Initial build              | 3–6 engineers × 6–12 mo  | 0                   |
| Annual maintenance         | 2–3 engineers ongoing    | Annual license      |
| Infrastructure              | Cloud + ops               | Included            |
| Opportunity cost            | Engineers NOT on product  | 0                   |
| Integration cost            | Designed for your stack   | May need adapters   |
| Upgrade/migration cost      | You own it                | Vendor-driven       |
| Vendor lock-in              | None                      | High                |
| Customization flexibility   | Unlimited                 | Limited by API/config|
| **Rule of thumb**           | Build if it IS the product| Buy everything else |

**Technology Radar:**

Maintain a living document that classifies technologies into four rings:
- **Adopt**: proven, safe, widely used — default choice (e.g., PostgreSQL, React, AWS)
- **Trial**: promising, used in production by some teams — actively evaluate (e.g., Rust for perf-critical, Temporal for workflows)
- **Assess**: worth exploring, not yet production-ready in your context — spike/experiment (e.g., WebAssembly, DuckDB)
- **Hold**: proceed with caution — legacy, deprecated, or over-hyped (e.g., MongoDB for relational data, hand-rolled auth)

**Tech Debt Quantification:**

```
Tech Debt Score = (Principal × Interest Rate) / Developer Velocity

Principal = effort to fix the debt (person-days)
Interest Rate = how much it slows down new feature development (hours/week wasted)
Developer Velocity = features shipped per sprint

Prioritization: Fix debt when Interest Rate > 5% of team velocity
                AND fixing it unblocks >20% throughput improvement

NOT all debt should be paid down. Debt that doesn't generate interest
(touch it once a year) is cheaper to carry than pay off.
```

### Phase 2 (~30 min): Engineering Org Design

**Team Topologies — four fundamental team types:**

| Team Type             | Purpose                                   | Interacts With           | Anti-Pattern               |
|-----------------------|-------------------------------------------|--------------------------|----------------------------|
| Stream-Aligned        | Deliver user value end-to-end             | Customers, other teams   | Too many dependencies      |
| Enabling              | Help stream teams overcome obstacles      | Stream-aligned teams     | Becomes ivory-tower        |
| Complicated-Subsystem | Build/maintain systems requiring deep expertise | Stream-aligned teams| Becomes bottleneck         |
| Platform              | Provide self-service infrastructure/platform | Stream-aligned teams  | Becomes ticket-driven      |

**Team size rule:** 5–9 engineers per stream-aligned team. <5: fragile. >9: coordination overhead dominates.
**Conway's Law in practice:** If you want a microservices architecture, organize as stream-aligned teams.
If you organize by function (frontend team, backend team, DB team), your architecture will reflect that.

**Engineering org scaling:**

```
1–10 engineers:  CTO writes code, no managers needed. Flat structure.
10–30:           CTO still technical; 1–2 tech leads emerge. Weekly 1:1s.
30–60:           CTO manages managers. First engineering managers (EMs).
                 Teams of 5–8. CTO spends 50% on strategy/people.
60–150:          Director/VPs emerge. CTO is 80%+ strategy, hiring, culture.
                 EMs manage teams; Directors manage EMs.
150+:            Multiple org layers. CTO is executive function.
                 Key challenge: maintaining technical coherence across orgs.
```

**Span of control:**
- Engineering Manager: 5–8 direct reports (IC engineers)
- Director: 3–5 EMs (15–40 total through chain)
- VP: 3–5 Directors
- CTO: leadership team + architecture group

**Career ladder — dual track:**

```
IC Track                     Management Track
─────────────────────────────────────────────────────
Junior Engineer              —
Engineer                     —
Senior Engineer              Engineering Manager
Staff Engineer               Senior EM
Principal Engineer           Director of Engineering
Distinguished Engineer       VP of Engineering
Fellow                       CTO / CPO
```

Both tracks must extend equally far with equivalent compensation. The worst
org design mistake: forcing engineers into management to advance.

### Phase 3 (~20 min): Architecture Governance

**RFC (Request for Comments) Process:**

```
1. Problem Statement   — What problem? Why now? What happens if we do nothing?
2. Proposed Solution   — Architecture decision with rationale.
3. Alternatives Considered — What else did you evaluate? Why rejected?
4. Trade-offs           — What do we gain? What do we lose? (Performance, complexity, cost, velocity)
5. Migration Plan       — How do we get from here to there? Rollback plan?
6. Open Questions       — What's still uncertain?

Review:
- Author circulates RFC → 5 business day comment period
- Architecture review meeting: author presents, stakeholders discuss
- Decision: Accepted / Accepted with modifications / Rejected / Needs more exploration
- Decisions documented in Architecture Decision Records (ADRs)
```

**ADR (Architecture Decision Record) template:**

```markdown
# ADR-042: Use PostgreSQL as Primary Relational Database
