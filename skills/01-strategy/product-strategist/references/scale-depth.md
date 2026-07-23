# Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Product strategy = your gut + 5 customer conversations. Roadmap = a prioritized TODO list. "PMF" = people are paying and not churning. No OKRs, no North Star metric, no prioritization framework.
- **What to skip**: Formal OKRs. RICE/CD3 scoring. Win/loss analysis. NPS surveys. Retention cohort analysis.
- **Coordination**: You are product + engineering + design. Talk to customers weekly.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Product vision written down. Simple roadmap (Now/Next/Later). North Star metric identified. Basic OKRs (1-2 objectives per quarter). Customer feedback loop (interviews + NPS). PMF assessed with Sean Ellis test. Prioritization = value vs effort matrix.
- **What to skip**: Full RICE/CD3 (value vs effort is enough). Competitive win/loss program. Formal product ops. Product council.
- **Coordination**: Weekly product sync with engineering lead. Monthly roadmap review. Quarterly OKR planning. Customer interview debriefs.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Product vision + strategy doc. Theme-based roadmap with outcomes. Structured OKRs (company → team). RICE or CD3 prioritization. Win/loss analysis program. NPS + CSAT + retention cohorts. Dedicated PM per product area. Product ops function emerges. Beta program management.
- **What to skip**: Product portfolio management (unless multi-product). Formal product council (peer review is enough). Full-time product ops (shared with eng ops).
- **Coordination**: Bi-weekly product review. Monthly roadmap review with stakeholders. Quarterly OKR review. Product council monthly.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Multi-product portfolio strategy. Product line management with P&L ownership. Full product ops function. Product council with formal gates. Advanced analytics (product-qualified leads, expansion revenue). Competitive intelligence team. Pricing science. Product-led growth team. M&A product integration playbook.
- **What's full production**: Annual product strategy cycle. Quarterly business review (QBR). Product portfolio review monthly. Product council bi-weekly. Win/loss continuous. Beta → GA lifecycle management.
- **Coordination**: QBR with exec team. Monthly product portfolio review. Bi-weekly product council. Weekly PLG metrics review.

### Transition Triggers
- **Solo → Small**: You need dedicated PM because you can't talk to customers + write specs + manage eng. >500 users.
- **Small → Medium**: Single PM can't cover all product areas. Need specialization. >10K users or second product line.
- **Medium → Enterprise**: Multiple product lines with P&L. IPO or acquisition requires formal product governance. >100K users.


### War Story 1 — The Feature That Shipped to Nobody
**Symptom:** A product team spent 3 quarters building a "collaborative editing" feature for their project management tool. At launch, only 2% of users tried it. After 6 months, adoption was still under 5%. It was eventually deprecated.
**Root cause:** The feature was prioritized based on a single enterprise customer's request and competitive pressure (Notion had it). No user research was done. The actual user need was "know when teammates are viewing the same document" — read-only presence, not real-time editing.
**Fix:** Adopted a "customer problem, not customer request" prioritization rule. Before any feature: run 5 discovery interviews to validate the underlying problem, not the proposed solution. The result: a much smaller "presence indicator" shipped in 3 weeks and hit 80% activation.
**Lesson:** Building what customers ask for is the most expensive way to discover what they actually need. Invest in problem discovery before solution design. A $5K research sprint can save $500K of engineering.

### War Story 2 — The Roadmap Driven by the Loudest Voice
**Symptom:** The VP of Sales brought a "must-have" feature request from a $500K enterprise prospect. The CEO approved it as top priority. The product shipped it in 2 quarters. The prospect went with a competitor anyway. Meanwhile, 3 core features were delayed, and NPS dropped 15 points.
**Root cause:** The roadmap was driven by the highest-value sales opportunity, not data. User feedback from the broader customer base was invisible because there was no systematic feedback collection. The company built for one customer and alienated hundreds.
**Fix:** Implemented RICE scoring with a mandatory step: any feature must reach >10% of the user base to qualify for top priority unless the deal is >20% of ARR. Sales-driven features without broad reach go into a "sponsor-funded" queue.
**Lesson:** The loudest stakeholder is rarely the most representative one. A systematic prioritization framework protects the roadmap from the highest-paid person's opinion.

### War Story 3 — The Pricing Page That Left Millions on the Table
**Symptom:** A B2B SaaS company charged $49/mo for their Pro plan because "that's what competitors charge." The CEO discovered at a board meeting that customers who negotiated custom pricing were paying $200-500/mo. The self-serve pricing was leaving 4x on the table.
**Root cause:** The pricing was set by competitive benchmarking, not willingness-to-pay research. No value metric analysis was done. Customers were willing to pay based on number of seats, not a flat fee.
**Fix:** Moved from per-user flat pricing to usage-based + tiered model: Free ($0), Starter ($29/seat), Business ($99/seat), Enterprise (custom). Tested with 20 customers before launch. ARR increased 300% in 6 months without adding a single new feature.
**Lesson:** Pricing is the most leveraged growth lever. A 10% price increase drops straight to profit. Test pricing changes like product changes — with experiments, cohorts, and statistical significance.
