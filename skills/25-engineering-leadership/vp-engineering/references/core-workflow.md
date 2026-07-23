# Core Workflow — Full Implementation

<!-- STANDARD: 3min -->

### Phase 1: Engineering Strategy

**Multi-Year Technical Vision.**
Strategy isn't a roadmap — it's a set of choices about where to invest and, more importantly, where NOT to invest.

- **Platform vs Product Investment.** What percentage of engineering goes to platform/infrastructure vs customer-facing features? This ratio is your most important resource allocation decision. Usually 20-30% platform for a scaling company.
- **Technical Debt Strategy.** Not all tech debt is bad. Categorize as: strategic (took on intentionally for speed), accidental (unintended from growth), and bitrot (aging dependencies). Assign business impact to each category. Only fix what's slowing you down measurably.
- **Build vs Buy at Scale.** Same framework as the decision tree, but applied across the portfolio: CI/CD, monitoring, auth, payments, CMS, analytics. Review annually — vendors improve, your needs evolve.
- **Innovation Allocation.** Carve out explicit innovation capacity (10-15%). This isn't 20% time — it's directed exploration of specific bets that could become the next product line or platform capability.

**Output:** Annual engineering strategy document (5-8 pages), socialized with ELT and board. Updated quarterly.

### Phase 2: Organizational Architecture

**Designing the Organization for Scale.**
Org design is your most powerful (and dangerous) lever. Wrong boundaries create more problems than wrong code.

- **Engineering Org Structure.** The classic trade-offs: functional teams (mobile, web, backend), product-aligned squads, matrix (functional leads + product leads), or platform + product split. Most companies at scale converge on product-aligned squads with platform teams.
- **Director+ Hiring.** Every director hire is a bet on a sub-organization. Your hiring bar for directors must be higher than for any IC. Look for: managed managers before, navigated a reorg, has a philosophy of management (not just tactics), and cultural fit.
- **Span of Control.** Ideal: 4-7 direct reports for directors and senior EMs. Below 4: overhead waste. Above 7: attention fragmentation. Adjust for experience level — new directors need closer span.
- **Location Strategy.** Remote-first, hybrid, or office-centric? This isn't preference — it's a talent strategy decision. Remote widens the funnel, office deepens collaboration. Choose explicitly; don't drift into a default.
- **M&A Technical Integration.** Playbook for acquiring companies: technical due diligence checklist, integration options (absorb, keep separate, hybrid), cultural integration timeline, system migration plan. One bad M&A integration can destroy both companies' engineering cultures.

**Output:** Org chart with charters, succession plan for every director+ role, location strategy document.

### Phase 3: Executive Leadership

**Operating at the Executive Level.**
The VP Eng role is fundamentally different from Director. You're no longer an engineering representative to the business — you're a business leader who runs engineering.

- **ELT Participation.** Your voice at the executive table must be about the company, not just engineering. Advocate for engineering's perspective on company strategy, but also advocate for the business within engineering. If product and engineering are at war, the CEO loses confidence in both.
- **Board Presentations.** Board decks from engineering must answer three questions: Are we delivering? Are we building the right thing? Is the team healthy and growing? Use DORA metrics for delivery, OKR progress for direction, and engagement/attrition/diversity for health. Never present a metric without trend and context.
- **Budgeting and Headcount.** Annual planning: translate company goals into engineering capacity needs. Use a bottom-up team-based model (not top-down ratio math). Defend headcount with data: what would we NOT deliver if we had 20% fewer people? What would accelerate with 20% more?
- **Investor Updates.** For investors: frame engineering as competitive advantage, not cost center. Show velocity trends, architectural decisions that create moats, talent brand metrics, and engineering-driven product innovation.

**Output:** Board deck template, annual budget model, quarterly investor engineering update.

### Phase 4: Engineering Culture

**Culture at Scale.**
Culture is what you tolerate, what you celebrate, and what you model. At VP level, everything you do — or don't do — sends a cultural signal.

- **Values Definition and Reinforcement.** Company values are often too generic for engineering. Define engineering-specific values: "We ship on Fridays," "Incidents are learning opportunities," "Design docs before code for anything cross-team." Reinforce through rituals, recognition, and your own behavior.
- **Career Ladder Design.** Dual-track (IC + management) with clear, objective level definitions. Compensation parity between tracks. Promotion criteria that reward impact, not hours. Calibration sessions across teams to ensure fairness.
- **Compensation Philosophy.** Market percentile target (e.g., 65th for base, 75th for total comp). Equity refresh strategy. Geo-adjustment policy. Transparency level (ranges visible to all, or on request). Get this wrong and you'll lose people to competitors in weeks, not months.
- **DEI Strategy.** Diversity isn't a pipeline problem alone — it's an inclusion and retention problem. Measure: hiring funnel at every stage by demographic, promotion rates, attrition rates, engagement scores. Act on the data.
- **Engineering Brand.** External blog, conference talks, open source contributions, engineering Twitter/LinkedIn presence. Your engineering brand determines who applies. The best engineers join companies whose engineering culture they already respect.

**Output:** Engineering values doc, career ladder, compensation bands, DEI dashboard, engineering brand calendar.
