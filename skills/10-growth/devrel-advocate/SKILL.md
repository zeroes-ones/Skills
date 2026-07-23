---
name: devrel-advocate
description: >
  Use when building developer relations strategy, creating developer content (tutorials/samples/talks),
  designing hackathons, running champion programs, optimizing developer onboarding (TTC), measuring
  developer NPS, or evangelizing APIs. Handles community strategy, content creation at scale, developer
  feedback loops, and metrics that connect DevRel to business outcomes. Do NOT use for technical
  documentation authoring, product management, paid marketing campaigns, or internal developer tools.
license: MIT
tags:
- devrel
- developer-relations
- community
- advocacy
- hackathons
- developer-content
- api-evangelism
author: Sandeep Kumar Penchala
type: growth
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
chain:
  consumes_from:
  - backend-developer
  - content-strategist
  - documentation-engineer
  - frontend-developer
  - technical-writer
  feeds_into:
  - content-strategist
  - documentation-engineer
  - growth-engineer
  - marketing-manager
---

# Developer Relations / Developer Advocate
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Design and execute developer relations programs that turn developers into champions, products into platforms, and documentation into onboarding. This skill covers community strategy, content creation at scale, sample application architecture, developer feedback loops, and metrics that connect DevRel to business outcomes. Everything ties back to one metric: Time to First API Call (TTC) — how fast a developer goes from "I should check this out" to a working integration.

## Route the Request

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately to the indicated section.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("README.md", "content calendar")` OR `file_exists("content-calendar.md")` | Developer content strategy — Jump to "Core Workflow > Phase 2" |
| A2 | `file_contains("package.json", "\"sample\"")` OR `file_exists("quickstart/")` OR `file_exists("examples/")` | Sample app & quickstart work — Jump to "Sub-Skills > developer-onboarding" |
| A3 | `file_exists("CODE_OF_CONDUCT.md")` AND `file_exists("CONTRIBUTING.md")` | Community governance & moderation — Go to "Core Workflow > Phase 3" |
| A4 | `file_contains("README.md", "hackathon")` OR `file_exists("hackathon/")` | Hackathon design & execution — Jump to "Sub-Skills > hackathon-design" |
| A5 | `file_contains("README.md", "cfp")` OR `file_exists(".github/speaking/")` | Conference & speaking strategy — Jump to "Sub-Skills > conference-speaking" |
| A6 | `file_contains("README.md", "feedback")` OR `file_exists(".github/ISSUE_TEMPLATE/")` | Developer feedback loop — Go to "Sub-Skills > developer-feedback-loop" |
| A7 | `file_contains("README.md", "champion")` OR `file_exists("champions/")` | Champion/MVP program design — Go to "Core Workflow > Phase 3" |
| A8 | `file_contains("README.md", "docs")` OR `file_exists("docs/quickstart")` | Documentation & developer onboarding — Jump to "Core Workflow > Phase 1" |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Developer advocacy strategy
│   ├── New DevRel program → Start at "Core Workflow > Phase 1"
│   └── Refining existing strategy → Go to "Core Workflow > Phase 4"
├── Content creation (blogs, tutorials, videos)
│   └── Scaling developer education → Jump to "Core Workflow > Phase 2"
├── Community building & champion programs
│   └── Growing developer ecosystem → Go to "Core Workflow > Phase 3"
├── Speaking & events (CFP, conferences, webinars)
│   └── Conference strategy → Jump to "Sub-Skills > conference-speaking"
├── Documentation & sample code
│   └── Reducing time-to-first-API-call → Go to "Sub-Skills > developer-onboarding"
├── Hackathon design
│   └── Planning a developer event → Go to "Sub-Skills > hackathon-design"
├── Developer feedback loops
│   └── Systematizing dev input to product → Go to "Sub-Skills > developer-feedback-loop"
├── Cross-skill: Align content calendar with `content-strategist` → Open that skill
├── Cross-skill: Coordinate onboarding experiments with `growth-engineer` → Open that skill
├── Cross-skill: Sync developer content SEO with `seo-specialist` → Open that skill
└── Not sure? → Start at "Core Workflow > Phase 1"
```

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to recommend DevRel strategy without validated developer personas.** Never prescribe tactics when persona data (stack, workflow, pain points) is absent or fabricated. | Trigger: Output contains "persona" AND no `file_contains` check for persona docs has been run OR `file_exists("personas/")` returns false. | STOP. Respond: "I cannot recommend a DevRel strategy without validated developer personas. First: run 10+ developer interviews, document 3-5 personas at `personas/`, then re-invoke this skill." |
| **R2** | **DETECT and BLOCK trust-destroying tactics.** Bait-and-switch content, fake engagement, undisclosed sponsorships, or paid but unlabeled promotion — any tactic that would erode developer trust. | Trigger: Output contains any of ["bait-and-switch", "fake", "astroturf", "pay for stars", "undisclosed", "sock puppet"] OR recommends sponsoring content without `#ad` or `#sponsored` disclosure. | STOP. Respond: "This tactic violates developer trust — and developer trust, once lost, is not regained. The tactic has been blocked. Consider: transparent sponsorships with clear disclosure, or authentic community engagement instead." |
| **R3** | **STOP if measuring vanity metrics as success.** Never present stars, followers, or member counts as DevRel KPIs without tying them to business outcomes (TTC, retention, pipeline, conversion). | Trigger: Output contains "DevRel success" or "DevRel KPI" AND lists [stars, followers, Discord members, subscribers] as primary metrics without conversion/pipeline tie-in. | STOP. Respond: "Vanity metrics detected. DevRel success is measured by: Time-to-First-API-Call (TTC), developer-to-paid conversion rate, dNPS segmented by cohort, and pipeline influenced. Replace vanity metrics with these before proceeding." |
| **R4** | **REFUSE to launch a community platform below critical mass.** Never recommend Discord/Discourse/Slack community when active developer count < 100. | Trigger: Output recommends "community platform" or ["Discord", "Discourse", "Slack community"] AND no prior validation that active developers > 100 (via `file_contains` check or explicit confirmation). | STOP. Respond: "Community platform blocked: you need 100+ active developers before a dedicated platform generates value. Before 100 devs, use GitHub Issues + email for 1:1 support. Re-invoke when you've crossed the threshold." |
| **R5** | **DETECT stale sample code before recommending it.** Never point developers to sample apps or quickstarts that haven't been validated as compiling/running. | Trigger: Output references "sample app" or "quickstart" AND no `file_contains(".github/workflows", "sample")` CI check has been verified OR CI last ran > 7 days ago. | STOP. Respond: "Sample app CI validation required before routing developers. Run: `gh run list --workflow=sample-apps --limit=1 --json status,conclusion` to verify CI is green. If failing, fix the sample apps before recommending them." |

## The Expert's Mindset

Master devrel advocates understand that strategy is not about predicting the future — it's about **being less wrong than the competition, faster**.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Survivorship bias** — studying only winners, ignoring the graveyard | Study 3 failures for every success; what killed them? |
| **Narrative fallacy** — creating clean stories for messy realities | Write the "strategy could be wrong because..." section first |
| **Confirmation bias** — seeking data that supports your thesis | Assign a team member to build the best case AGAINST your strategy |
| **Short-termism** — optimizing this quarter at the expense of next year | Every decision gets a "6-month" and "3-year" impact column |

### What Masters Know That Others Don't
- **The bottleneck is always one thing.** Find it. Fix it. Then find the next one.
- **Strategy = what you say NO to.** If your strategy doesn't exclude anything, it's not a strategy.
- **Timing beats brilliance.** The best strategy at the wrong time loses to a mediocre strategy at the right time.

### When to Break Your Own Rules
- **Bet the company when the asymmetry is right.** If downside = $1M and upside = $1B, the math doesn't care about your process.
- **Ignore the data when you're creating a new category.** By definition, there's no data for something that doesn't exist yet.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Initiative | Execute a defined strategic initiative with clear metrics |
| **L2** | Product line / function | Define strategy for a product line; own outcomes |
| **L3** | Business unit | Set multi-year strategy for a business unit; allocate resources across competing priorities |
| **L4** | Company | Define company-wide strategy; make existential trade-off decisions |
| **L5** | Industry | Shape industry dynamics; create new market categories |

**Default level for this skill:** L3
**Usage:** Invoke this skill with your target level, e.g., "as an L3 devrel advocate, develop..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

- Your company is launching a developer-facing API or SDK and you need to build an onboarding funnel
- You need to decide whether (and when) to hire a DevRel team based on your developer ecosystem size
- You are choosing a community platform — GitHub Discussions, Discord, Discourse, or Slack — for your developer community
- You need to create a content strategy (blogs, tutorials, videos, conference talks) that drives developer adoption
- You are designing a sample application or quickstart that demonstrates your API's value in under 5 minutes
- You need to measure developer experience — Time to First API Call (TTC), developer NPS, retention cohorts
- You are planning a hackathon or developer contest with clear judging criteria, prizes, and project scaffolding
- You need to build a developer champion or MVP program that rewards and amplifies your most active community members

## Decision Trees

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
```
DEVREL STRATEGY — Should we hire a DevRel or not?
├── Product requires API integration by external developers?
│   └── YES → You need DevRel. Question is when, not if.
├── <100 active external developers today?
│   └── Start with a founding engineer doing DevRel 20% time.
│       Blog posts + 1:1 developer support. No full-time hire yet.
├── 100-1000 active developers?
│   └── Hire 1 full-time DevRel (community + content focus).
│       Budget: salary + $50K-100K/yr (events, swag, tools, travel).
├── 1000-10000 active developers?
│   └── DevRel team of 3-5 (content, community, events). Budget: $500K-1.5M/yr.
├── 10000+ active developers?
│   └── DevRel organization: regional advocates, dedicated community engineers,
│       developer success team, internal tools team for samples/SDKs.
└── Product is internal-only or no external developer ecosystem?
    └── Do NOT hire DevRel. An internal developer experience (IDX) role is different.

COMMUNITY PLATFORM — Where should the developer community live?
├── Open source project on GitHub?
│   └── GitHub Discussions (built-in, no fragmentation) + Discord for real-time chat.
│       GitHub is non-negotiable for OSS. Discord is supplemental, not primary.
├── SaaS API product (commercial, not OSS)?
│   └── Discord or Slack Connect for real-time. Discourse for async/long-form.
│       Forum for SEO-indexable Q&A. Avoid Slack free tier (history disappears).
├── Enterprise B2B with < 500 developer accounts?
│   └── Private Slack Connect channels per customer + a shared forum.
│       Don't build a public community for a private product — it's a ghost town.
├── Mobile/SDK product with high volume of integration questions?
│   └── Stack Overflow tag (official) + Discord for quick help.
│       Stack Overflow is SEO-magnetic — your answers help future developers silently.
└── Chinese market specifically?
    └── WeChat groups + CSDN + SegmentFault. Western platforms don't reach Chinese devs.

CONTENT STRATEGY — What content format drives the most developer adoption?
├── Pre-launch / developer preview?
│   └── 1 "why we built this" blog + 1 interactive quickstart (CodeSandbox/Replit) + 1 talk.
├── Launch week?
│   └── 1 hero blog post + 3 tutorials by use case + 1 video walkthrough (<10 min) +
│       1 live stream/AMA + sample apps for top 3 frameworks + docs site launch.
├── Post-launch (growth phase)?
│   └── 1 tutorial/week + 1 case study/month + 2 guest posts/quarter + 1 conf talk/month.
│       Tutorials drive acquisition. Case studies drive conversion. Talks drive trust.
├── Mature product (100K+ developers)?
│   └── 1 deep-dive technical article/week + video series + podcast + university curriculum +
│       certification program. Shift from "how to use" to "how to master."
└── Developer tool with strong competition?
    └── Migration guides FROM competitors. Comparison pages (fair, not FUD). Performance
        benchmarks (reproducible). These convert better than feature lists.

HACKATHON DESIGN — Run one or not?
├── < 100 community members?
│   └── Don't run a hackathon. You'll get 5 submissions and it'll feel empty.
│       Do a "build with us" livestream instead — more intimate, higher quality.
├── 100-1000 community members?
│   └── Online hackathon, 2-4 weeks, pre-seeded with starter templates.
│       Budget: $5K-15K (prizes, platform, promotion). Goal: 30-50 submissions.
├── 1000-10000 community members?
│   └── Themed hackathon (e.g., "AI Hackathon," "Mobile Hackathon"). 2-4 weeks.
│       Budget: $15K-50K. In-person option for finals. Sponsor booths optional.
├── 10000+ community members?
│   └── In-person hackathon (200-500 attendees). 24-48 hours. Major sponsors.
│       Budget: $50K-200K (venue, food, prizes, staffing, AV).
└── Enterprise/B2B?
    └── Internal hackathon for customer's engineering team. 1-2 days onsite.
        Your DevRel + their engineers build a working integration together.
        Highest-converting "event" per dollar. Budget: travel + 2 days.

TOXIC BEHAVIOR — What to do when a community member turns hostile?
├── First offense, mild (passive-aggressive, unhelpful)?
│   └── Private DM: "Hey, that comment came across differently than you might
│       have intended. We want to keep things constructive." Document it.
├── Second offense or public personal attack?
│   └── Public response: "Let's keep the discussion focused on the technical
│       issue. Personal comments aren't helpful." + private DM with clear boundary.
├── Repeated pattern or harassment, threats, bigotry?
│   └── Immediate 30-day ban. Public note: "This user has been temporarily removed
│       for violating our code of conduct." Appeal process available. No negotiation
│       on harassment — zero tolerance means zero tolerance.
└── High-profile community member (champion, open source contributor)?
    └── Same rules. Apply them faster. If anything, be MORE public about it.
        If you protect VIPs, you lose the community's trust permanently.

**What good looks like:** The output opens correctly in the target tool. All validations pass. No placeholder content remains.

```

## Core Workflow

<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Foundation — Know Your Developers

1. **Developer Persona Research**: Identify 3-5 developer personas. For each: job title, tech stack, pain points,
   where they learn (Reddit, Stack Overflow, YouTube, conferences), what "success" looks like with your product.
   Validate with 10+ developer interviews (not just your fans — talk to churned developers, too).
   - **Output**: Developer persona cards. Shared with product, marketing, and engineering.

2. **Developer Journey Mapping**: Map the developer's path from discovery to champion.
   Discovery → Signup → First API call (TTC) → First working integration → First production deploy → Evangelism.
   Measure time and drop-off at each stage. Identify the #1 friction point.
   - **Output**: Developer journey map with conversion rates per stage. TTC baseline measured.

3. **Define DevRel KPIs**: Connect DevRel activities to business outcomes.
   - Level 1 (Output): blog posts published, talks given, community members joined
   - Level 2 (Engagement): tutorial completions, sample app clones, docs page views, community messages
   - Level 3 (Product): TTC, API call volume, SDK downloads, active developer accounts
   - Level 4 (Business): developer-sourced pipeline, developer-to-paid conversion, developer NPS, churn
   - **Output**: KPI dashboard. Monthly DevRel report template.

4. **Community Platform Setup**: Choose and configure community platforms. Set up code of conduct
   (use Contributor Covenant as base). Define moderation guidelines. Onboard first 10 community members
   personally — welcome DMs, intro posts, pair them with a buddy.
   - **Output**: Community platform(s) live. Code of conduct published. Moderation guide documented.

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): Content Engine — Educate at Scale

1. **Content Calendar**: Plan next 90 days. Mix: tutorials (50%), reference/API docs (20%), thought leadership (15%),
   case studies (10%), community stories (5%). Each piece has: target persona, funnel stage, distribution channels,
   and a CTA (try the quickstart, join Discord, attend a workshop).
   - **Output**: 90-day content calendar with assignments, deadlines, and distribution plan.

2. **Sample Application Architecture**: Build and maintain 3-5 reference applications.
   Each demonstrates: auth, core API calls, error handling, and a realistic use case
   (not a TODO app — a mini SaaS, a data dashboard, an integration with another popular API).
   Keep them updated. A stale sample app destroys trust faster than no sample app.
   - **Output**: 3-5 sample apps. CI tests that verify they build and run. Update on every major API change.

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.

## Cross-Skill Coordination

<!-- QUICK: 30s -- table of who to talk to when -->

### Decision Gates & Artifacts

| Gate | Condition | Action |
|------|-----------|--------|
| DevRel ↔ Content | Blog post, tutorial, or educational content series planned | Coordinate with `content-strategist`; align editorial calendar and SEO keywords |
| DevRel ↔ Growth | Developer onboarding optimization or TTC changes | Involve `growth-engineer`; share dNPS data and signup funnel metrics |
| DevRel ↔ Product | Developer feedback prioritization or feature requests | Coordinate with `product-manager`; share structured feedback with user counts |
| DevRel ↔ SEO | Developer docs discoverability or content SEO | Sync with `seo-specialist`; align on developer keyword strategy |
| DevRel ↔ Engineering | Sample app broken or SDK feature request | Involve `backend-developer` or `frontend-developer`; share reproduction steps |

**Artifacts shared across skills:**
- Developer content calendar (shared with `content-strategist`, `seo-specialist`)
- Sample app repositories (shared with `backend-developer`, `frontend-developer`)
- Developer feedback reports (shared with `product-manager`, `backend-developer`)
- dNPS survey results and TTC benchmarks (shared with `product-manager`, `growth-engineer`)

| Coordinate With | When (Trigger) | What Info Flows |
|---|---|---|
| **Product Manager** | Feature prioritization, developer feedback | Developer pain points, feature requests with user count, competitive gaps |
| **Content Strategist** | Blog posts, tutorials, documentation | Technical content briefs, SEO keywords for developer topics, content calendar alignment |
| **Technical Writer** | API docs, quickstarts, sample app READMEs | Docs gaps identified by developers, common support questions that need documenting |
| **API Designer** | API usability feedback, DX improvements | Developer friction in API design, SDK ergonomics, error message quality |
| **Frontend/Backend Developer** | Sample app maintenance, SDK development | Sample app bugs, SDK feature requests, developer-reported issues |
| **Growth Engineer** | Developer onboarding optimization, A/B testing signup flow | TTC data, signup funnel drop-off, experiment ideas for onboarding |
| **UX Researcher** | Developer experience research, usability testing | Developer journey pain points, persona validation, usability study recruitment |
| **Marketing / Demand Gen** | Event promotion, content distribution, paid campaigns | Developer channel strategy, event calendar, content amplification |
| **CEO Strategist** | DevRel strategy, budget, headcount | Developer ecosystem metrics, competitive landscape, ROI of DevRel investment |
| **Legal Advisor** | Code of conduct enforcement, contributor agreements, event liability | Code of conduct review, CLA/DCO strategy, event legal requirements |
| **SEO Specialist** | Developer content SEO, docs SEO, Stack Overflow presence | Developer keyword strategy, docs site architecture, hreflang for localized developer hubs |
| **Customer Success** | Enterprise developer accounts, escalated issues | Developer health scores, churn risks, expansion opportunities |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| TTC increases by >30% month-over-month | Product Manager, Growth Engineer, API Designer | Onboarding regression; urgent investigation |
| Developer NPS drops >10 points in a quarter | Product Manager, CEO Strategist, API Designer | Developer satisfaction crisis; root cause analysis |
| Community Code of Conduct violation by high-profile member | Legal Advisor, CEO Strategist | Reputation risk; consistent enforcement critical |
| Competing product launches significantly better DX | Product Manager, API Designer, CEO Strategist | Competitive threat; DX gap analysis and response |
| Developer-requested feature shipped | Original requesters (personally), community (publicly) | Close the feedback loop; build trust |
| Sample app broken due to API change | API Designer, Backend Developer | Developer trust at risk; fix immediately |
| Conference CFP accepted (major event) | Content Strategist, Marketing | Amplify; prepare talk + booth + side events |
| Community growth stalls (<5% month-over-month for 3 months) | Product Manager, Growth Engineer | Growth program audit; channel diversification |

### Route to Other Skills

- **`content-strategist`** — When producing developer blog posts, tutorials, or educational content series that need editorial alignment
- **`growth-engineer`** — When optimizing developer onboarding flows, signup experiments, or TTC metrics
- **`seo-specialist`** — When optimizing developer docs for search or developer content SEO strategy
- **`backend-developer` / `frontend-developer`** — When sample app maintenance or SDK development needs engineering support

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| Time-to-First-API-Call (TTC) increases > 30% month-over-month | Audit quickstart: count steps from "I want to try" to "it worked"; remove friction; test with new developer unfamiliar with product | TTC is the single most important DevRel metric — every added step costs 50% of developers; degradation is a conversion emergency |
| Sample app CI pipeline fails — quickstart no longer compiles | Fix within 24 hours; notify API team if breaking change caused it; add pre-release sample app testing to API deployment pipeline | A stale sample app is worse than no sample app — developers who try and fail are less likely to try again |
| Community Code of Conduct violation by high-profile contributor | Enforce consistently — same consequences as any member; notify Legal Advisor; communicate decision to community | The moment your community sees VIPs protected from consequences, trust evaporates — strongest enforcement on strongest contributors |
| Developer NPS drops > 10 points in a quarter | Run root cause analysis; survey detractors; correlate with product changes, support response times, and community activity | dNPS decline is a lagging indicator — by the time it drops 10 points, developers have been frustrated for months |
| Developer-requested feature shipped after 6+ months of advocacy | Personally notify every developer who requested it; credit by name (with permission); publish community update with before/after | Closing the feedback loop publicly is the single highest-ROI trust-building activity in DevRel |
| Conference CFP accepted at major event (KubeCon, re:Invent, PyCon) | Notify Content Strategist, Marketing; prepare talk + workshop + booth plan; amplify across all channels; schedule follow-up content | A major conference talk is a force multiplier — plan the full content funnel, not just the 45-minute slot |
| Community growth stalls < 5% month-over-month for 3 consecutive months | Audit acquisition channels; review onboarding conversion; survey inactive members; test new content formats or platforms | Community growth stall is a leading indicator of product-market fit issues in the developer segment |
| Champion program members churning > 30% annually | Survey departing champions; review tier benefits; ensure champions feel impact (feedback shapes product) not just recognition (swag, badges) | Champions stay for impact, not perks — if they don't see their feedback in the product roadmap, they leave |

## What Good Looks Like

> The docs are so good that support tickets stay flat while adoption doubles. Product teams ship features with developer feedback already incorporated because the DevRel team runs a tight feedback loop,

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.


### Cross-skills Integration
```mermaid
graph LR
    A[content-strategist] --> B[devrel-advocate]
    B --> C[growth-engineer]
    D[product-manager] --> B
    B --> E[technical-writer]
```
Run skills in the order shown:
```bash
# Chain A: content-strategist → devrel-advocate → growth-engineer
# Chain B: product-manager → devrel-advocate → technical-writer
```

## Deliberate Practice

```mermaid
graph LR
    A[Formulate<br/>thesis] --> B[Test in<br/>market] --> C[Study<br/>outcome] --> D[Refine<br/>mental model] --> A
```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Write a strategy memo for a past business event; compare your reasoning to what actually happened | Monthly |
| **Competent** | Write 3 strategies for the same goal with different constraints; debate which wins | Quarterly |
| **Expert** | Reverse-engineer a competitor's strategy from public information; validate against their next move | Quarterly |
| **Master** | Board-level strategy for a company in a different industry; present to a peer CEO for feedback | Semi-annually |

**The One Highest-Leverage Activity:** Write a pre-mortem for your current strategy: It is 2 years from now. Our strategy failed. Why?

## References

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Scale Depth**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)

