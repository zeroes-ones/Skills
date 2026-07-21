---
author: Sandeep Kumar Penchala
type: asset-template
domain: product-management
version: "1.0"
last_updated: 2026-07-21
---

# Product Roadmap Template

A Now/Next/Later roadmap template designed for outcome-driven product management. Avoid date-based commitments beyond the current quarter. Focus on problems, not solutions.

---

## Roadmap Meta

| Field | Value |
|-------|-------|
| **Product / Area** | [Product name or feature area] |
| **Version** | [v1.0] |
| **Last Updated** | [YYYY-MM-DD] |
| **Owner** | [Product Manager name] |
| **Next Review** | [YYYY-MM-DD — at least quarterly] |
| **Stakeholders** | [Names and roles of key stakeholders] |

---

## Product Vision

[2–3 sentences describing the product's purpose and the change it aims to create in users' lives. This stays relatively stable over time.]

> "For [target user] who [problem], [product name] is a [category] that [key benefit]. Unlike [alternatives], our product [key differentiator]."

---

## Strategic Objectives (OKRs)

These objectives define success for the current and upcoming periods.

| Objective | Key Results | Target Date | Status |
|-----------|-------------|-------------|--------|
| [Objective 1] | KR1: [Measurable outcome] | Q[n] 20YY | On Track / At Risk / Blocked |
| | KR2: [Measurable outcome] | | |
| | KR3: [Measurable outcome] | | |
| [Objective 2] | KR1: [Measurable outcome] | Q[n] 20YY | |
| | KR2: [Measurable outcome] | | |

---

## Roadmap

### NOW — Committed (Current Quarter)

Work that is actively in development or fully specced and ready to start within the next 2 weeks.

| Initiative | Problem / Opportunity | Target Outcome | RICE Score | Confidence | Status |
|------------|----------------------|----------------|------------|------------|--------|
| [Initiative 1] | [What user/business problem does this solve?] | [Expected measurable improvement] | [Score] | [%] | 🟢 In Progress |
| [Initiative 2] | [Problem] | [Outcome] | [Score] | [%] | 🟡 Spec Ready |
| [Initiative 3] | [Problem] | [Outcome] | [Score] | [%] | 🟢 In Progress |
| [Initiative 4] | [Problem] | [Outcome] | [Score] | [%] | 🔵 Blocked |

**Capacity**: [X] engineering teams / [Y] engineers available this quarter.

**Status Legend**: 🟢 In Progress · 🟡 Spec Ready (awaiting engineering) · 🔵 Blocked · ⚪ Not Started

---

### NEXT — Discovered & Prioritized (Next 1–2 Quarters)

Work that has been validated (problem is real, solution direction is clear) but hasn't started. This column is a buffer — it changes as priorities shift.

| Initiative | Problem / Opportunity | Target Outcome | RICE Score | Confidence | Est. Effort |
|------------|----------------------|----------------|------------|------------|-------------|
| [Initiative 5] | [Problem] | [Outcome] | [Score] | [%] | [S/M/L/XL] |
| [Initiative 6] | [Problem] | [Outcome] | [Score] | [%] | [S/M/L/XL] |
| [Initiative 7] | [Problem] | [Outcome] | [Score] | [%] | [S/M/L/XL] |
| [Initiative 8] | [Problem] | [Outcome] | [Score] | [%] | [S/M/L/XL] |

**Decision Rule**: When "Now" capacity opens, pull the highest RICE item from "Next" that fits available capacity.

**T-Shirt Size Reference**: S = 1–2 weeks · M = 2–4 weeks · L = 1–2 months · XL = 2–4 months

---

### LATER — Validated Problems (Future Horizons)

Problems we believe are worth solving but haven't committed to a specific solution or timeline. These are validated problems, not feature proposals.

| Problem Statement | Evidence (Data, Research, Requests) | Potential Impact | Discovery Needed |
|-------------------|-------------------------------------|-----------------|------------------|
| [Users struggle to... because...] | [N support tickets/month, churn %, survey feedback, interview quotes] | [Estimated impact on KPIs] | [What we need to learn before committing] |
| [Problem 2] | [Evidence] | [Impact] | [Discovery needed] |
| [Problem 3] | [Evidence] | [Impact] | [Discovery needed] |
| [Problem 4] | [Evidence] | [Impact] | [Discovery needed] |

**Promotion Criteria**: A "Later" item moves to "Next" when:
1. The problem is validated with quantitative AND qualitative evidence
2. A solution approach has been sketched and reviewed by engineering
3. The RICE score has been computed and reviewed with the team
4. The item has a clear success metric

---

## RICE Scoring Reference

| Initiative | Reach | Impact | Confidence | Effort (person-months) | RICE Score |
|------------|-------|--------|------------|------------------------|------------|
| [Name] | [Users/quarter] | [1–5] | [20/50/80/100%] | [N] | [(R×I×C)/E] |
| | | | | | |
| | | | | | |
| | | | | | |

**Scoring Guide**:

**Reach** — How many users will this affect per quarter?
- Use actual numbers where available (analytics, database queries)
- If unknown, estimate conservatively and flag as low confidence
- Consider both direct users and indirectly affected users

**Impact** — How much will this improve the target metric?
- 1 = Minimal improvement (barely measurable)
- 2 = Low improvement (noticeable but small)
- 3 = Medium improvement (meaningful change)
- 4 = High improvement (significant step change)
- 5 = Massive improvement (transformative)

**Confidence** — How certain are we about the reach, impact, and effort estimates?
- 20% = Gut feeling / opinion only
- 50% = Supported by qualitative data (interviews, feedback)
- 80% = Supported by quantitative data (analytics, A/B test, survey)
- 100% = Proven (already measured, A/B tested, or industry standard)

**Effort** — Total person-months required (engineering + design + QA + deployment).
- Count ALL contributors, not just engineering
- Include deployment, migration, documentation, and monitoring time

---

## Stakeholder-Specific Views

### Executive Summary (1 page)

**Current Quarter Focus**: [2–3 sentence summary of what we're shipping now and why]

**Key Metrics**:
| Metric | Current | Target | Trend |
|--------|---------|--------|-------|
| [North Star Metric] | [Value] | [Value] | 📈/📉/➡️ |
| [KPI 1] | [Value] | [Value] | |
| [KPI 2] | [Value] | [Value] | |

**Risks & Mitigations**:
- [Risk 1] — [Mitigation plan]
- [Risk 2] — [Mitigation plan]

**Key Decisions Needed**: [List decisions requiring executive input]

---

### Engineering View

**Now — Technical Details**:
| Initiative | Tech Lead | Key Technical Decisions | Dependencies | Migration Required? |
|------------|-----------|------------------------|--------------|---------------------|
| [Name] | [Lead] | [Architecture choices, new services, data changes] | [Other teams, APIs, infrastructure] | Yes/No — [Details] |
| | | | | |

**Next — Technical Pre-work Needed**:
- [Spike/investigation needed for Next items]
- [Infrastructure or platform work needed before Next items can start]

**Tech Debt & Quality**:
- [ ] [Tech debt item 1] — [Effort, Impact]
- [ ] [Tech debt item 2] — [Effort, Impact]

---

### Sales & Marketing View

**Now — What to Communicate**:
| Initiative | Value Proposition | Target Persona | GA Date | Enablement Materials |
|------------|-------------------|---------------|---------|---------------------|
| [Name] | [1-sentence benefit statement] | [Persona] | [Date or Q] | [One-pager / demo / training / blog post] |
| | | | | |

**Key Talking Points**:
1. [Competitive differentiator 1]
2. [Competitive differentiator 2]
3. [Customer success story or quote]

---

### Design View

**Now — Design Status**:
| Initiative | Designer | Design Status | Handoff Status | Key Design Decisions |
|------------|----------|---------------|----------------|---------------------|
| [Name] | [Designer] | 🔴 Not Started / 🟡 In Progress / 🟢 Complete | Not Started / Ready / In Review | [Decisions] |
| | | | | |

**Next — Design Discovery Needed**:
- [UX research or exploration needed for Next items]

**Design System Impact**:
- [New components needed? Existing components modified? New patterns?]

---

## Quarterly Review & Update Process

### Pre-Review Preparation (1 week before)
- [ ] Update all initiative statuses
- [ ] Collect current metrics (North Star + KPIs)
- [ ] Review RICE scores for confidence changes (has new data changed our estimates?)
- [ ] Gather customer feedback and support ticket themes from the quarter
- [ ] Prepare stakeholder-specific summary slides

### Review Meeting Agenda (90 minutes)
1. **Metrics Review** (10 min) — Progress toward OKRs. What moved? What didn't?
2. **Now Review** (20 min) — Status of committed work. Blockers? Scope changes?
3. **Next Promotion** (20 min) — Which Next items move to Now? Any re-prioritization?
4. **Later Scan** (15 min) — Any validated problems ready for discovery? New problems emerged?
5. **Capacity Planning** (15 min) — Team capacity for next quarter. Any changes?
6. **Decisions & Actions** (10 min) — Document decisions. Assign follow-ups.

### Post-Review
- [ ] Update roadmap document within 2 business days
- [ ] Communicate changes to all stakeholders
- [ ] Update project management tool (Jira, Linear, Asana) to reflect roadmap
- [ ] Archive previous version with date stamp

---

## Roadmap Anti-Patterns

| Anti-Pattern | Why It's Harmful | What to Do Instead |
|-------------|------------------|--------------------|
| Date-based roadmap beyond current quarter | Dates beyond 3 months are fiction; they create false certainty and disappointment | Use Now/Next/Later. Commit to dates only for Now. |
| Feature list disguised as roadmap | Stakeholders fixate on specific solutions, not problems | Write the problem, not the solution syntax |
| No success metrics | Can't tell if work had impact | Every initiative has a target outcome with a measurable metric |
| Stakeholders surprised by the roadmap | Erodes trust; invites scope creep | Socialize roadmap async 48h before review meetings |
| "Next" and "Later" items never get revisited | Roadmap becomes stale; opportunities missed | Quarterly review forces re-evaluation |
| Capacity ignored | Committed work exceeds available capacity → inevitable delays | Match Now commitments to actual capacity |
| All items are "high priority" | No real prioritization; everything becomes urgent | Use RICE consistently. If everything is P0, the scoring is broken. |
| Roadmap not visible to the team | Engineers/designers don't understand the "why" behind priorities | Publish roadmap visibly (Notion, Confluence, shared drive) |
| No confidence scoring | Low-confidence items receive equal commitment as proven items | Flag confidence <50% for a spike or time-boxed investigation |
| Roadmap doesn't change quarter to quarter | Reality changes; roadmap that doesn't adapt is a wishlist | Expect 20–30% churn in Next; Later is inherently fluid |

---

## References

- _Escaping the Build Trap_ by Melissa Perri — outcome-driven roadmapping
- _Inspired_ by Marty Cagan — product discovery and roadmap practices
- RICE Prioritization Framework by Sean McBride (Intercom): https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/
- Now/Next/Later Roadmapping by Janna Bastow (ProdPad): https://www.prodpad.com/blog/how-to-build-a-product-roadmap-everyone-understands/
- Shape Up by Ryan Singer (Basecamp) — for shaping bets and time-boxed development
