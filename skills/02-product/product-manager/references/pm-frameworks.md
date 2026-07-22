---
author: Sandeep Kumar Penchala
type: reference
domain: product-management
version: "1.0"
last_updated: 2026-07-21
parent_skill: product-manager
---

# Product Management Frameworks

> **Author:** Sandeep Kumar Penchala

A comprehensive reference of prioritization, scoping, measurement, and communication frameworks for product managers. Covers RICE, Kano, MoSCoW, opportunity scoring, metrics hierarchies, OKRs, and stakeholder communication templates. Use alongside the Product Manager skill's discovery and delivery workflows.

---

## 1. RICE Prioritization

RICE scores features across four dimensions to produce a single, comparable score.

```
RICE Score = (Reach × Impact × Confidence) ÷ Effort
```

### Scoring guide

| Score | Reach | Impact | Confidence | Effort |
|-------|-------|--------|------------|--------|
| **1** | < 10 users | Minimal — barely noticeable | Wild guess, no data | 1 person-week |
| **2** | 10–100 users | Low — nice to have | Anecdotal evidence | 2 person-weeks |
| **3** | 100–1K users | Medium — users will notice | Qualitative data (interviews) | 1 person-month |
| **4** | 1K–10K users | High — measurable behavior change | Quantitative data (analytics) | 2 person-months |
| **5** | 10K+ users | Massive — changes the game | A/B tested, proven | 3+ person-months |

### RICE scoring template (spreadsheet)

```
| Feature        | Reach | Impact | Confidence | Effort | RICE Score |
|----------------|-------|--------|------------|--------|------------|
| Dark mode      | 4     | 2      | 4          | 3      | 10.7       |
| CSV export     | 3     | 3      | 5          | 2      | 22.5       |
| SSO (SAML)     | 2     | 5      | 4          | 5      | 8.0        |
| Onboarding v2  | 5     | 4      | 3          | 4      | 15.0       |
```

### When RICE works best
- Quarterly roadmap planning with 10+ candidate features
- Cross-team prioritization where stakeholders disagree
- When you need a defensible, data-informed rank — not a precise prediction

### RICE limitations
- Impact and confidence scoring is subjective; calibrate as a team
- Doesn't capture dependencies or sequencing constraints
- Doesn't account for strategic necessity (compliance, platform health)

---

## 2. Kano Model

Classifies features by how they affect customer satisfaction.

```
SATISFACTION
    ▲
    │         DELIGHTERS          │         PERFORMANCE
    │    (unexpected joy,         │    (more = more satisfied)
    │     no penalty if absent)   │   ╱
    │      *                      │  ╱
    │         *              ╱─────╱
    │            *          ╱
    │               *      ╱
    ├────────────────────╱──────────────────► FEATURE INVESTMENT
    │                   ╱
    │                  ╱  MUST-HAVE / BASIC
    │                 ╱   (dissatisfied if absent,
    │                ╱    but more doesn't increase satisfaction)
    │               ╱
    ▼
```

### Kano survey question template

For each feature, ask TWO questions:

```
Functional (if you HAD this feature):
"How would you feel if the app had [feature]?"
  1. I like it
  2. I expect it
  3. I'm neutral
  4. I can tolerate it
  5. I dislike it

Dysfunctional (if you did NOT have this feature):
"How would you feel if the app did NOT have [feature]?"
  1. I like it
  2. I expect it
  3. I'm neutral
  4. I can tolerate it
  5. I dislike it
```

### Classification matrix

```
                    |      DYSFUNCTIONAL (without feature)      |
                    | Like | Expect | Neutral | Tolerate | Dislike |
F  | Like          |   Q  |   A    |    A    |    A     |    O    |
U  | Expect        |   R  |   I    |    I    |    I     |    M    |
N  | Neutral       |   R  |   I    |    I    |    I     |    M    |
C  | Tolerate      |   R  |   I    |    I    |    I     |    M    |
T  | Dislike       |   R  |   R    |    R    |    R     |    Q    |

A = Attractive (Delighter)
M = Must-be (Basic)
O = One-dimensional (Performance)
I = Indifferent
R = Reverse (opposite of expected)
Q = Questionable (invalid response)
```

### Action per category
- **Must-be:** Ship to stay competitive. Don't over-invest — diminishing returns after "good enough."
- **Performance:** Invest proportionally — more is better. Good for roadmap differentiation.
- **Delighter:** Ship selectively. They become "must-be" over time (competition copies). Budget 10–20% of capacity.
- **Indifferent:** Don't build. Waste of resources.
- **Reverse:** Opposite of what user wants — investigate misunderstanding.

---

## 3. MoSCoW Method

Scope negotiation for a fixed deadline.

```
| Category | Definition | % of capacity |
|----------|-----------|---------------|
| **Must have** | Critical for launch — product is useless without it | 60% |
| **Should have** | Important but not critical — painful to omit | 20% |
| **Could have** | Nice to have — included if time allows | 20% |
| **Won't have** | Explicitly out of scope for this release | 0% |
```

### MoSCoW rules
1. Must-have is NOT "everything we want." If everything is Must, nothing is.
2. Must-haves total ≤ 60% of estimated capacity. This gives a realistic buffer.
3. Won't-haves are as important as Must-haves — make scope boundaries explicit.
4. Re-evaluate weekly: Should-haves can become Won't-haves if timeline slips.

### Example: Mobile app v1
```
MUST HAVE:
  ✓ Email + password signup/login
  ✓ Core feed (pull-to-refresh, basic posts)
  ✓ Profile (photo, bio)

SHOULD HAVE:
  ✓ Social login (Google, Apple)
  ✓ Push notifications for mentions
  ✓ Search (basic keyword)

COULD HAVE:
  ✓ Dark mode
  ✓ Post drafts (save for later)
  ✓ Share to Instagram/Twitter

WON'T HAVE (v1):
  ✗ Video posts
  ✗ Direct messaging
  ✗ Analytics dashboard
```

---

## 4. Opportunity Scoring

Prioritize based on importance vs satisfaction gap.

### Survey questions (per outcome/need)
1. "How important is [outcome] to you?" (1–5)
2. "How satisfied are you with current solutions for [outcome]?" (1–5)

### Opportunity score calculation
```
Opportunity = Importance + max(Importance − Satisfaction, 0)
```

### Scoring matrix
```
HIGH
  ▲              UNDER-SERVED               TABLE STAKES
  │              (Prime opportunity —        (Important + satisfied —
  │               invest here)               maintain, don't over-invest)
I │              Opportunity > 10            Opp = 8–10
M ├────────────────────────────────────────────────────
P │              LOW PRIORITY                OVER-SERVED
O │              (Ignore — not important,    (Important + over-served —
R │               not a pain point)           reduce investment)
T │              Opp < 8                     Opp = 6–8
  │
  └────────────────────────────────────────────────────►
LOW          SATISFACTION (current solutions)         HIGH
```

---

## 5. Product Metrics Hierarchy

```
                    ┌─────────────────────┐
                    │    NORTH STAR        │  ← One metric that measures core value
                    │  (e.g., Weekly       │
                    │   Active Projects)   │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
    ┌─────────▼────────┐ ┌────▼─────────┐ ┌────▼─────────┐
    │   L1: BUSINESS    │ │  L1: GROWTH  │ │ L1: QUALITY  │ ← Business outcomes
    │   MRR, ARR, NRR   │ │  New users,  │ │  Uptime,      │
    │                   │ │  Activation  │ │  CSAT, NPS    │
    └─────────┬─────────┘ └────┬─────────┘ └────┬─────────┘
              │                │                │
    ┌─────────▼─────────┐ ┌───▼──────────┐ ┌───▼──────────┐
    │  L2: PRODUCT       │ │ L2: ACQ      │ │ L2: RELIAB.  │ ← Product-level
    │  Feature adoption, │ │  Signup rate, │ │  P95 latency, │
    │  Engagement depth  │ │  Trial→Paid  │ │  Error rate   │
    └─────────┬─────────┘ └────┬─────────┘ └────┬─────────┘
              │                │                │
    ┌─────────▼─────────┐ ┌───▼──────────┐ ┌───▼──────────┐
    │  L3: FEATURE       │ │ L3: CHANNEL  │ │ L3: ALERT     │ ← Feature-level
    │  Search usage,     │ │  Organic vs  │ │  Specific      │
    │  Export completions│ │  Paid ratio  │ │  endpoint errs │
    └───────────────────┘ └──────────────┘ └───────────────┘
```

### Metric design rules
1. Every L2 metric must roll up to an L1 metric
2. Every feature has at least one L3 metric
3. If a metric isn't moving after 2 quarters, remove it
4. Counter-metrics for every metric: e.g., "engagement up" — check "support tickets also up?"

---

## 6. OKR Setting for Product Teams

### OKR format
```
Objective: [Qualitative, aspirational, memorable goal]
Key Result 1: [Measurable outcome — from X to Y by date]
Key Result 2: [Measurable outcome]
Key Result 3: [Measurable outcome]
```

### Example 1: Growth
```
Objective: Become the default starting point for new teams

KR1: Increase weekly trial signups from 500 to 1,200
KR2: Improve trial-to-paid conversion from 12% to 20%
KR3: Achieve NPS ≥ 50 for first-30-day experience
```

### Example 2: Platform
```
Objective: Make our API the most reliable integration in our customers' stack

KR1: Reduce API p95 latency from 800ms to 300ms
KR2: Achieve 99.9% uptime (from 99.5% — max 43 min downtime/month)
KR3: Publish public status page with < 5 min incident detection latency
```

### Example 3: Engagement
```
Objective: Users depend on us daily for their most important workflows

KR1: Increase DAU/MAU from 25% to 40%
KR2: Increase avg. sessions per user per day from 1.2 to 2.5
KR3: Reduce time-to-value for core workflow from 15 min to 3 min
```

### OKR health checks (mid-quarter)
- [ ] Are KRs on track? (Red/Yellow/Green)
- [ ] Are we doing the *right* work to move KRs? (or just shipping features?)
- [ ] Any KR that's already hit 100%? (Set it too low — learn for next quarter)
- [ ] Any KR stuck at 0%? (Blocked? Wrong KR? Unblock or adjust)

---

## 7. Stakeholder Communication Templates

### Weekly Update (Email/Slack)
```markdown
**Subject:** Product Update — Week of [Date]

**🏆 Top wins:**
- [Win 1 — with metric if possible]
- [Win 2]

**🚧 In progress:**
- [Initiative] — [Status: On track / At risk] — ETA: [Date]
- [Initiative] — [Status] — ETA: [Date]

**⚠️ Risks / Blockers:**
- [Risk] — Mitigation: [Plan] — Need: [Ask, if any]

**📊 Key metric:**
[North Star or primary metric] — [Current] vs [Target] — [Trend: ↗️ / ↘️ / ➡️]
```

### Monthly Business Review (Slide deck — 5 slides)
```
Slide 1: North Star + Top 3 Product Metrics — trends, targets, gaps
Slide 2: What We Shipped — features, experiments, wins (with data)
Slide 3: What's Next — top 3 priorities for next month, why, expected impact
Slide 4: User Insights — key learnings from research, support, sales
Slide 5: Asks/Decisions — what do we need from leadership?
```

### Quarterly Roadmap Presentation (10 slides)
```
Slide 1:   Vision & strategy recap (1 sentence each)
Slide 2:   Q accomplishments vs. plan
Slide 3:   North Star + key metrics — quarterly trends
Slide 4:   Market/competitive update (any major shifts?)
Slide 5:   User research themes (top 3 insights this quarter)
Slide 6:   Proposed Q+1 roadmap — initiatives, not features
Slide 7:   Resource & capacity plan
Slide 8:   Risks & mitigation
Slide 9:   Key decisions needed
Slide 10:  Appendix: detailed metrics, feature list, research citations
```

---

See also: Product Manager skill for discovery workflows, stakeholder management, and roadmap planning.
