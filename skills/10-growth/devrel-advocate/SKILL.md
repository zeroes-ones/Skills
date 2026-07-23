---
name: devrel-advocate
description: 'Developer relations strategy, community building, content creation (blogs/tutorials/videos/talks), sample apps, conference speaking, hackathon design, developer onboarding (TTC), developer
  NPS, champion programs, and API evangelism. Trigger: DevRel, developer relations, developer advocate, developer evangelism, community building, developer community, open source community, API evangelist,
  technical community manager. Works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI.'
author: Sandeep Kumar Penchala
type: growth
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- devrel-advocate
token_budget: 4000
output:
  type: code
  path_hint: ./
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

3. **Quickstart Optimization**: A developer should go from zero to a working API call in < 5 minutes.
   Remove every step that isn't absolutely necessary. Pre-fill API keys in the quickstart if possible.
   Use CodeSandbox/Replit/StackBlitz embeds for zero-install try-it-now experiences.
   - **Output**: Quickstart flow optimized. TTC measured and improving sprint over sprint.

4. **Conference & Event Strategy**: Identify 3-5 conferences where your target developers gather.
   Submit CFPs 6 months ahead. Prepare: 1 keynote-level talk, 2 technical deep dives, 1 workshop.
   Booth strategy: live demos > swag > brochures. Staff booths with engineers, not salespeople.
   - **Output**: Conference calendar. Talk abstracts submitted. Workshop materials prepared.

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): Community Building — Turn Users into Champions

1. **Champion Program Design**: Identify top 1% of community members (answer questions without being asked,
   build integrations unprompted, speak about your product publicly). Formalize with: early access to features,
   private Slack/Discord channel, swag, speaker opportunities, contributor recognition in docs.
   Never pay champions directly — it destroys authenticity. Reward with access, recognition, and impact.
   - **Output**: Champion program live. 5-20 champions identified and onboarded.

2. **Developer Feedback Loop**: Every week, bring top developer feedback to product and engineering.
   Format: "Developer problem → Proposed solution → How many developers affected → Revenue/reputation impact."
   Close the loop: when product ships a developer-requested feature, personally notify the developers
   who requested it. Publicly credit them.
   - **Output**: Weekly developer voice report. Feature request tracker with public status.

3. **Office Hours & Developer Support**: Run weekly public office hours (livestream or Discord voice).
   Answer questions live. Record and publish. This scales 1:many instead of 1:1.
   For enterprise developers: quarterly roadmap reviews, monthly check-ins, dedicated Slack channel.
   - **Output**: Office hours schedule published. Recordings available. Support SLAs defined.

4. **Moderation & Community Health**: Weekly: review flagged content, check community sentiment,
   look for unanswered questions (>24 hours old). Monthly: review moderation actions, update guidelines
   if needed. Quarterly: community health survey (safety, belonging, value).
   - **Output**: Community health dashboard. Moderation log. Quarterly health report.

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): Measurement & Iteration

1. **Developer NPS (dNPS)**: Survey developers quarterly. "How likely are you to recommend our
   product to another developer?" Segment by persona, tenure, and usage level.
   - **Output**: dNPS score and trends. Segmented analysis.

2. **Attribution Modeling**: Track how developers found you: organic search, social media, conference,
   referral, docs, sample app. Attribute downstream conversions (signup, first API call, paid conversion)
   to acquisition source. This is hard to do perfectly — aim for directional accuracy.
   - **Output**: Attribution dashboard. Channel ROI analysis.

3. **DevRel Quarterly Business Review**: Present to leadership: developer growth, engagement metrics,
   product feedback shipped, community health, dNPS, pipeline influenced. Always connect DevRel activities
   to revenue or product improvement. Never report "we published 12 blog posts" without "which drove 300
   developer signups and 15 qualified leads."
   - **Output**: QBR deck. Action items for next quarter.

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

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 developers)
- **What changes**: You are the DevRel. Blog posts written by you (or founding engineers). 1:1 developer support via email/DM. No community platform — GitHub Issues + email is enough. Sample apps: 1-2, updated when you remember. No conferences yet — guest on podcasts instead.
- **What's overkill**: Community platform, hackathons, champion program, dNPS surveys, DevRel metrics dashboard, conference sponsorships, swag, dedicated sample app maintenance.
- **Coordination**: You talk to developers directly. Feedback goes straight into your own product decisions.
- **Cost**: $0-1K/yr (domain, maybe a podcast mic).
- **Transition trigger**: You can't personally respond to every developer within 48 hours.

### Small Team (2-10 people, 100-1K developers)
- **What changes**: 1 full-time DevRel. Blog: 1 post/week. Community: Discord or Discourse. Sample apps: 3-5, updated per release. Conferences: 2-3/year (regional). Champion program: informal (you know the top 10 developers by name). Office hours: bi-weekly. dNPS: annual survey.
- **What's overkill**: Multiple DevRel hires, global conference circuit, certification program, dedicated developer success team, sophisticated attribution model, internal DevRel tools team.
- **Coordination**: Weekly sync with product and engineering. Monthly developer feedback report.
- **Cost**: $150K-250K/yr (salary + events + tools + swag).
- **Transition trigger**: 1000+ active developers OR developer support volume >20 hours/week OR revenue from developer ecosystem >$500K ARR.

### Medium Team (10-50 people, 1K-10K developers)
- **What changes**: DevRel team of 3-5 (content lead, community manager, developer advocate × 2-3). Blog: 2-3 posts/week. Video: 1/week. Community: Discord + Discourse + Stack Overflow. Sample apps: 10+, CI-tested. Conferences: 8-12/year (global). Champion program: structured with tiers. Hackathons: 2-3/year (online + in-person). dNPS: quarterly. Office hours: weekly. Developer feedback loop: formalized with product triage. Swag: strategic (champions, events, new signups).
- **What's overkill**: Regional DevRel teams, certification program, developer university, dedicated developer success function, internal sample app/SDK platform team.
- **Coordination**: Bi-weekly DevRel-product sync. Monthly stakeholder review. Quarterly developer advisory board.
- **Cost**: $500K-1.5M/yr.
- **Transition trigger**: 10K+ developers OR developer ecosystem revenue >$5M ARR OR international expansion requiring regional DevRel presence.

### Enterprise (50+ people, 10K+ developers)
- **What changes**: DevRel organization (10-30 people). Regional DevRel teams (NA, EMEA, APAC, LATAM). Roles: developer advocates, community engineers, developer success managers, DevRel operations, internal tools engineers for SDKs and sample apps. Certification program. Developer university (self-paced courses). Global conference circuit (20+ events/year). Multiple hackathons per quarter. Dedicated moderation team. Developer advisory board (meets quarterly). dNPS: continuous (in-product surveys). Attribution: multi-touch with CRM integration. Swag: global logistics. Internal advocacy: DevRel has a seat at the product strategy table.
- **What's full production**: Developer ecosystem platform (developer portal, unified docs, community, SDK downloads, status page). Developer success with SLAs. Paid developer support tiers. M&A developer ecosystem integration. Developer fund or startup program. Annual developer conference (owned event, 1000+ attendees).
- **Coordination**: Weekly DevRel leadership meeting. Monthly cross-functional review with product, engineering, marketing, sales. Quarterly executive review. Dedicated DevRel ops function for tools, metrics, and budget.
- **Cost**: $2M-10M+/yr.
- **Transition trigger**: 10K+ active developers OR developer ecosystem is primary growth channel OR IPO/acquisition requires mature developer ecosystem metrics.

## What Good Looks Like

> A developer discovers the product through a conference talk or tutorial, finds a well-maintained sample app that builds on their first try, and gets their question answered in the community forum within hours. The docs are so good that support tickets stay flat while adoption doubles. Product teams ship features with developer feedback already incorporated because the DevRel team runs a tight feedback loop, and the community champions mentor newcomers before the DevRel team even sees the question. Developer NPS trends upward every quarter.

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

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|---|---|---|
| `community-strategy` | Building or restructuring a developer community | Platform selection, moderation, code of conduct, community health, growth tactics |
| `content-creation` | Planning or executing developer content | Blog posts, tutorials, video scripts, talk abstracts, content calendar, distribution |
| `sample-app-development` | Building reference applications | Architecture, maintenance, CI testing, framework coverage, realistic use cases |
| `developer-onboarding` | Optimizing time-to-first-API-call | Quickstart design, signup flow, SDK ergonomics, zero-install demos (CodeSandbox) |
| `conference-speaking` | Preparing for a talk or workshop | CFP strategy, talk structure, slide design, live demos, audience engagement |
| `hackathon-design` | Planning a hackathon | Theme, prizes, judging criteria, platform, promotion, sponsor management |
| `champion-program` | Formalizing top contributor recognition | Tiers, benefits, selection criteria, renewal, community governance |
| `developer-feedback-loop` | Systematizing dev feedback to product | Collection, triage, product advocacy, closing the loop, feature request tracking |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Developer experience is the product**: Developers choose APIs based on DX — clear docs, fast TTC, helpful error messages, consistent SDKs. A 10% improvement in TTC beats a 10% improvement in API performance for adoption. Measure both.
- **Answer questions in public — always**: If one developer asks, 10 others have the same question silently. Answer in a forum, Stack Overflow, or GitHub Discussion. The SEO value compounds for years.
- **Never pay community champions directly**: It destroys authenticity and creates perverse incentives. Reward with access (early features, private channels), recognition (spotlight, swag, speaker ops), and impact (their feedback shapes the product).
- **Keep sample apps alive**: A stale sample app that doesn't compile is worse than no sample app. CI-test every sample app on every API release. Pin dependencies. Update within 1 week of a breaking change.
- **Show, don't tell**: A 5-minute video of a working integration converts better than a 2000-word blog post. A live demo converts better than a video. An interactive sandbox converts better than a live demo. Push toward interactivity.
- **Hire for empathy, not charisma**: The best developer advocates aren't the most extroverted — they're the ones who feel genuine frustration when developers struggle and genuine joy when they succeed. Nurture this trait.
- **Treat your community's time as sacred**: Every email, every event, every tutorial must respect the developer's time. If your workshop takes 2 hours but could be a 15-minute video, you've stolen 1 hour and 45 minutes from every attendee.
- **Metrics must connect to business outcomes**: "We have 5,000 Discord members" means nothing. "Discord community members convert to paid at 3× the rate of non-members" means everything. Always tie DevRel metrics to revenue or product impact.
- **Close the feedback loop publicly**: When a developer-requested feature ships, credit them by name (with permission). This is the single highest-ROI trust-building activity in DevRel.
- **Enforce the code of conduct consistently — especially for VIPs**: The moment your community sees you protect a high-profile contributor from consequences, trust evaporates. Your strongest enforcement should be on your strongest contributors.


## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Launching a community platform (Discord/Discourse) before you have 100+ active developers | Use GitHub Issues + email for 1:1 support until critical mass; launch platform only when developers are asking for it | `grep -r "Discord\|Discourse\|Slack community" --include="*.md"` in project docs — flag any community-platform recommendation without `file_contains("README.md", "active developers")` check | Pre-commit hook: block PRs adding `Discord` or `Discourse` URLs if `wc -l < active-developers.txt` < 100 |
| Staffing conference booths with salespeople who can't do live demos or answer technical questions | Staff developer booths with engineers; follow up within 24 hours; track conversions to first API call | `grep -r "conference booth\|booth staff\|sales.*booth" --include="*.md"` — flag if booth staff list contains no `github.com/` contributor URLs | Conference planning template: require `engineer_count >= sales_count` and list GitHub handles for every booth staffer; block submission if ratio violated |
| Selecting community champions by activity volume (posts made) instead of helpfulness (answers given, PRs reviewed) | Weight helpfulness over volume; champions represent your brand — selecting by activity selects for noise, not signal | `grep -r "champion.*select\|champion.*criteria" --include="*.md"` — flag if `posts_made` appears without `answers_given` or `prs_reviewed` | Champion nomination form: require `helpfulness_ratio = answers / posts` field; auto-reject nominees with ratio < 0.3 |
| Building quickstarts that require reading docs, installing SDK, creating account, generating API key — each on a separate page | Build single-page quickstart with pre-filled keys, one-click code copy, and CodeSandbox/Replit embed — target < 5 minutes to first API call | `grep -rn "step\|Step" quickstart/ --include="*.md" \| wc -l` — flag if step count > 5; `grep -r "CodeSandbox\|Replit\|one-click" quickstart/` — flag if embed is missing | Lint rule: `quickstart-steps` CI check fails if any quickstart has > 5 numbered steps or lacks a CodeSandbox/Replit link |
| Paying community champions directly for contributions | Reward with access (early features, private channels), recognition (spotlight, speaker ops), and impact (feedback shapes product) — direct payment destroys authenticity | `grep -r "pay.*champion\|stipend.*champion\|champion.*payment" --include="*.md"` — flag any monetary reward structure for champions | Champion agreement template: `payment` field locked to `none`; only `access`, `recognition`, `impact` tiers accepted in config |
| Shipping sample apps without CI — they silently break on the next API change | CI-test every sample app on every API release; pin dependencies; update within 1 week of a breaking change | `grep -rn "sample\|example\|demo" .github/workflows/ --include="*.yml"` — flag if no workflow references sample directories; `grep -r "build\|test\|compile" .github/workflows/` — verify sample CI exists | CI gate: every `api-release` workflow MUST trigger downstream `sample-apps-verify` job; merge blocked if sample app CI is red |
| Measuring DevRel success by vanity metrics: "5,000 Discord members" with no connection to business outcomes | Tie every metric to revenue or product impact: "Discord members convert to paid at 3× the rate of non-members" | `grep -r "member count\|follower count\|star count\|download count" --include="*.md"` in reports — flag any vanity metric without `conversion rate` or `pipeline` tie-in | DevRel dashboard template: require `conversion_to_paid` and `pipeline_influenced` columns; reject dashboards with only `count` metrics |
| Letting developer feedback accumulate without closing the loop — features ship, requesters never hear about it | Personally notify every requester when their feature ships; credit by name; close the loop publicly — single highest-ROI trust activity | `grep -r "shipped\|released" CHANGELOG.md` then `grep -rn "reported by\|requested by\|credit" CHANGELOG.md` — flag if shipped features lack reporter attribution | Release template: `CHANGELOG.md` entries require `Reported by: @github_handle` field; CI blocks merges where shipped features lack requester credit |
## Error Decoder

| 🖥️ Console Match (grep pattern) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `grep '"members": [0-9]' community-metrics.json` returns < 100 AND `grep '"posts_last_30_days": [0-9]'` returns < 10 | Community platform launched but fewer than 10 posts after 6 months — ghost town that scares away new visitors | Platform was set up before there was enough developer adoption | Shut down public community. Use GitHub Issues + email for 1:1 support until critical mass. Re-launch when active developers > 100. | `curl -s https://api.community-platform/stats \| jq '.members'` → if < 100: `echo "COMMUNITY_GHOST_TOWN" >> alerts.log` → run `scripts/archive-community.sh` → redirect users to GitHub Issues → set calendar reminder: check again in 90 days |
| `grep -rn "sample\[" .github/workflows/ --include="*.yml" \| wc -l` returns 0 OR `gh run list --workflow=sample-apps --limit=1 --json conclusion \| grep failure` | Sample app hasn't compiled in 4 months and developers report broken quickstarts | No CI pipeline for sample apps — API changes broke endpoints silently | Add CI pipeline that builds/tests every sample app on every API release. Pin dependency versions. Set automated alerts for broken builds. | `gh workflow run sample-apps-ci.yml` → if fails: `grep "error:.*sample" build.log \| head -5` → `git checkout -b fix/sample-app-$(date +%Y%m%d)` → fix deps → `gh pr create --title "fix: broken sample app CI"` → merge → verify: `gh run watch $(gh run list --workflow=sample-apps --limit=1 --json databaseId -q '.[0].databaseId')` |
| `grep -c "dNPS" quarterly-report.md` returns 0 OR `grep "dNPS: [-][0-9]"` shows drop > 10 | Developer NPS dropped 20 points after champion program launched | Champion program selected by activity volume, not helpfulness — power users spammed the community | Restructure champion criteria: weight helpfulness (answers given, PRs reviewed) over activity (posts made). Add community moderation training. | `python scripts/champion-audit.py --metric=helpfulness` → if top-10-by-activity != top-10-by-helpfulness: flag mismatch → `python scripts/rebalance-champions.py --weight-helpfulness=0.7` → notify flagged champions → re-run dNPS survey in 30 days |
| `grep "event-leads" conference-report.csv \| awk -F',' '{print $5}' \| grep "active" \| wc -l` returns < 10 | Conference booth generated 500 leads but only 3 converted to active developers | Booth staffed by salespeople who promised nonexistent features and collected business cards with no follow-up | Staff developer booths with engineers who can do live demos. Follow up within 24 hours with personalized onboarding link. Track conversions from event to first API call. | `python scripts/event-audit.py --event=last --metric=lead_to_active` → if conversion < 2%: flag as `BOOTH_WASTE` → `python scripts/reassign-booth-staff.py --min-engineer-ratio=0.5` → update event playbook → require `follow_up_sent` column in lead spreadsheet within 24h |
| `curl -s https://quickstart.example.com/health/ttc \| jq '.ttc_seconds'` returns > 300 | Time-to-First-API-Call averages 45 minutes despite having quickstart docs | Quickstart requires reading docs, installing SDK, creating account, generating API key — each on separate pages | Build single-page quickstart with pre-filled API key, one-click code copy, and CodeSandbox/Replit embed that makes the first call in < 5 minutes. | `python scripts/ttc-profiler.py --url=https://quickstart.example.com` → identify >5 steps or >300s TTC → `python scripts/generate-one-page-quickstart.py --template=single-page` → CI deploys to `quickstart/` → verify: `curl -s https://quickstart.example.com/health/ttc \| jq '.ttc_seconds'` < 300 |
| `grep -rn "TODO\|FIXME" CONTRIBUTING.md CHANGELOG.md` returns > 0 items older than 30 days | Developer feedback loop is broken — features ship but requesters are never notified | No automated attribution or feedback close-loop process | Maintain public feature tracker (Canny, GitHub Discussions). Every shipped feature credits the requester by GitHub handle in CHANGELOG. | `python scripts/feedback-audit.py --since=30d` → for each `shipped` issue without `credited_to`: `gh issue comment ISSUE_NUM --body "Shipped in vX.Y! Thanks @reporter"` → update CHANGELOG → verify: `grep "credited" CHANGELOG.md \| wc -l` > 0 |
| `grep -c "sample" Makefile` returns 0 AND `find . -name "Dockerfile" -path "*/sample*" \| wc -l` returns 0 | Developer onboarding page has 60% bounce rate and no one reaches first API call | No working, CI-verified sample app exists — developers must build from scratch to evaluate | Create 3 sample apps in top 3 frameworks. CI-test on every release. Pre-deploy each sample to a public sandbox URL. Link from docs homepage. | `python scripts/bootstrap-sample-apps.py --frameworks=node,python,go` → `gh workflow run sample-apps-ci.yml` → if green: deploy to `sandbox.example.com/samples/{framework}` → add to docs: `gh pr create --title "docs: add sample app links to homepage"` → verify: `curl -s https://sandbox.example.com/samples/node/ \| grep "200 OK"` |


## Production Checklist

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | Community platform(s) live with published code of conduct and moderation guidelines | `test -f CODE_OF_CONDUCT.md && test -f CONTRIBUTING.md && grep -q "moderation" CODE_OF_CONDUCT.md` | `cp templates/CODE_OF_CONDUCT.md . && cp templates/CONTRIBUTING.md . && echo "✅ S1: Community governance docs created"` |
| **[S2]** | Developer personas documented (3-5) and validated with 10+ developer interviews | `ls personas/*.md 2>/dev/null | wc -l | xargs -I{} test {} -ge 3 && grep -rn "validated" personas/ | wc -l | xargs -I{} test {} -ge 3` | `python scripts/generate-persona-template.py --output=personas/ && echo "✅ S2: Persona templates created; schedule 10 interviews"` |
| **[S3]** | Developer journey mapped from discovery to champion with conversion rates and TTC baseline | `test -f docs/developer-journey.md && grep -q "TTC" docs/developer-journey.md && grep -q "conversion" docs/developer-journey.md` | `python scripts/journey-mapper.py --output=docs/developer-journey.md && echo "✅ S3: Journey map scaffolded"` |
| **[S4]** | Quickstart enables a working API call in < 5 minutes; measured and tracked per release | `curl -s https://quickstart.example.com/health/ttc | jq -e '.ttc_seconds < 300'` | `python scripts/ttc-validator.py --url=https://quickstart.example.com --threshold=300 --alert-on-fail` |
| **[S5]** | 3-5 sample applications maintained and CI-tested on every API change | `gh run list --workflow=sample-apps --limit=1 --json conclusion -q '.[0].conclusion' | grep -q success` | `gh workflow run sample-apps-ci.yml && gh run watch $(gh run list --workflow=sample-apps --limit=1 --json databaseId -q '.[0].databaseId')` |
| **[S6]** | 90-day content calendar published with persona, funnel stage, and distribution channel per piece | `test -f content-calendar.md && grep -q "persona\|funnel stage\|distribution" content-calendar.md` | `python scripts/calendar-generator.py --days=90 --output=content-calendar.md && echo "✅ S6: Content calendar generated"` |
| **[S7]** | Champion program live with 5-20 members; tiers, benefits, and selection criteria defined | `test -f champions/README.md && grep -q "tier\|benefit\|selection" champions/README.md && test $(wc -l < champions/members.csv) -ge 6` | `python scripts/champion-bootstrap.py --min-members=5 --output=champions/ && echo "✅ S7: Champion program scaffolded"` |
| **[S8]** | Developer feedback loop formalized: weekly report to product, feature requests tracked with public status | `test -f .github/ISSUE_TEMPLATE/feature_request.md && gh issue list --label "feedback" --limit 1 --json number -q '. | length > 0'` | `python scripts/feedback-workflow.py --init && gh label create "feedback" --color 0366d6 && echo "✅ S8: Feedback loop initialized"` |
| **[S9]** | Weekly office hours running and recorded; questions answered in public (forum/Stack Overflow) | `python scripts/office-hours-check.py --last-7-days | grep -q "running"` | `python scripts/office-hours-scheduler.py --weekly --platform=Discord --auto-record && echo "✅ S9: Office hours scheduled"` |
| **[S10]** | dNPS measured quarterly; segmented by persona, tenure, and usage level | `grep -rn "dNPS" reports/ --include="*.md" | grep -q "$(date +%Y)"` | `python scripts/dnps-survey.py --trigger=quarterly --segments=persona,tenure,usage && echo "✅ S10: dNPS survey deployed"` |
| **[S11]** | Attribution tracking for developer acquisition sources (organic, social, referral, events, docs) | `grep -rn "utm_source\|referrer\|acquisition_channel" analytics/ --include="*.sql" --include="*.yml" | head -1 | grep -q "."` | `python scripts/attribution-setup.py --sources=organic,social,referral,events,docs --output=analytics/ && echo "✅ S11: Attribution config created"` |
| **[S12]** | Conference/event strategy: CFP calendar, talk abstracts, workshop materials prepared | `test -f events/cfp-calendar.md && grep -q "CFP\|abstract\|workshop" events/cfp-calendar.md` | `python scripts/cfp-scanner.py --output=events/cfp-calendar.md && python scripts/abstract-generator.py --output=events/talks/ && echo "✅ S12: CFP strategy bootstrapped"` |
| **[S13]** | Hackathon playbook documented (if applicable): theme, platform, judging rubric, prize structure | `test -f hackathon/playbook.md && grep -q "theme\|judging\|prize" hackathon/playbook.md` | `python scripts/hackathon-playbook.py --output=hackathon/playbook.md && echo "✅ S13: Hackathon playbook created"` |
| **[S14]** | Swag strategy: champions, event attendees, new signups; inventory managed | `test -f swag/inventory.csv && grep -q "champion\|event\|signup" swag/inventory.csv` | `python scripts/swag-planner.py --output=swag/ && echo "✅ S14: Swag strategy scaffolded"` |
| **[S15]** | Moderation log reviewed weekly; community health survey run quarterly | `python scripts/moderation-audit.py --since=7d | grep -q "reviewed"` | `python scripts/moderation-review.py --auto-flag --output=reports/moderation-$(date +%Y%m%d).md && echo "✅ S15: Weekly moderation review triggered"` |
| **[S16]** | DevRel dashboard tracks: developer growth, engagement, TTC, dNPS, pipeline influenced | `curl -s https://dashboard.internal/api/health | jq -e '.metrics | contains(["growth","engagement","TTC","dNPS","pipeline"])'` | `python scripts/dashboard-generator.py --metrics=growth,engagement,TTC,dNPS,pipeline --deploy && echo "✅ S16: DevRel dashboard deployed"` |
| **[S17]** | Quarterly Business Review (QBR) delivered to leadership with DevRel impact on business outcomes | `test -f reports/QBR-$(date +%Y)-Q*.md && grep -q "pipeline\|revenue\|conversion" reports/QBR-$(date +%Y)-Q*.md` | `python scripts/qbr-generator.py --quarter=current --output=reports/ && echo "✅ S17: QBR template generated"` |

## Footguns
<!-- DEEP: 10+min — war stories from developer relations and community building -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| Spent $50K sponsoring 4 conferences in one year — developer signups didn't budge because every talk was a product pitch disguised as a technical talk | A DevRel team at an API startup spent $50K on conference sponsorships in 2023: booth fees, swag, travel for 3 team members per event. They gave talks at all 4 conferences. But developer signups from conference attribution were exactly 12 — at a cost of $4,167 per signup. Post-mortem revealed the talks were titled "How Our API Solves Microservices Problems" — developers attended expecting technical content and got a sales pitch. Conference attendees actively warned each other to skip the company's sessions. | The team confused "conference presence" with "developer trust." Conference sponsorships work when you teach something developers value independently of your product. When every talk is a product demo, developers categorize you as a vendor, not a peer — and they tune out. | **Conference talks must pass the "no-product test": if you removed every mention of your product, would the talk still be worth attending?** Acceptable talk: "Scaling WebSocket Connections to 10M Concurrent Users — Lessons from Building in Rust." Unacceptable: "How Our Platform Scales WebSockets — a Demo." Aim for 80% educational, 20% product mention. Better: 0% product mention during the talk, let the booth be where product conversations happen. Track conference ROI as qualified developer signups within 30 days, not booth visitors. |
| Built a Slack community of 5,000 developers — 4,800 never posted, the 200 who did were asking support questions, and community health collapsed because there was no programming or moderation strategy | A DevRel team launched a public Slack community in 2022. Growth was fast — 5,000 members in 8 months through website CTAs and conference signups. But by month 10: 4,800 members had never sent a message, the #general channel was 90% support questions ("my API key doesn't work"), the original 200 active members had gone silent, and the DevRel team was running an unpaid support queue. They shut the Slack down in month 14 because "the community wasn't working." | The community had no programming (regular events, prompts, AMAs, challenges), no moderation strategy, and no onboarding experience. Joining a 5,000-person Slack where nobody posts is like walking into an empty convention center. The platform choice was also wrong — Slack communities collapse without active programming because conversations disappear in the scroll. | **Community platforms need active programming, not just membership.** Launch with a 4-week content calendar before inviting members: weekly AMA with an engineer, biweekly coding challenge, monthly showcase thread ("what did you build this month?"). Every new member gets a DM from a human within 24 hours asking "what are you working on?" Use Discourse or Discord for async communities where content persists and is searchable. Measure community health by weekly active posters (not total members), and hire a community manager before you hit 1,000 members. |
| Hired 3 DevRel engineers who only wrote blog posts — zero community engagement, zero conference talks, zero GitHub activity, and $450K/year of content that the content marketing team could have produced for $120K | A Series B developer-tools company hired 3 DevRel engineers in 2023 at $150K each. Their output over 12 months: 48 blog posts, 12 "guest posts" on partner blogs, and 3 white papers. Zero conference talks. Zero open-source contributions to relevant projects. Zero engagement in developer forums (Stack Overflow, Reddit, Hacker News). Zero community events hosted. The $450K headcount produced content indistinguishable from what a $120K/year content marketing contractor could deliver. | DevRel was defined as "developer content marketing" rather than "developer advocacy." The hires were evaluated on content output (posts written) rather than developer engagement (relationships built, trust earned). The DevRel team had no GitHub activity because "we're not engineers, we're advocates" — but developers trust advocates who code. | **DevRel must include at least 3 of 5 activity types:** (a) content creation (blog, video, docs), (b) community engagement (forums, social, chat), (c) events (conferences, meetups, workshops), (d) open-source contribution (to your product AND adjacent projects), (e) product feedback (closing the loop between developers and product team). Evaluate DevRel engineers on developer trust metrics (GitHub stars, forum reputation, talk ratings, community NPS), not content output alone. A DevRel engineer who gives 1 conference talk that 500 developers love is worth more than one who writes 20 blog posts nobody reads. |
| Promised 12 feature requests to community members with "we'll prioritize this" — product team shipped none of them within 12 months, community trust evaporated, and 3 top contributors publicly quit the community | A DevRel team at a developer-tools startup collected 47 feature requests from community members over 6 months (Q1-Q2 2023). In every interaction, the DevRel response was: "Great idea — I'll share this with the product team and we'll prioritize it." None of the 47 requests were shipped within 12 months. The actual product roadmap was already committed to enterprise customers' requirements. In Q3 2023, 3 of the community's top 10 contributors posted public farewell messages: "I've been told my feedback matters for 18 months — nothing has shipped. I'm moving to [competitor]." | DevRel overpromised to build goodwill without checking whether the product team had capacity or intent to ship the requests. There was no feedback loop — the requests went into a private Slack channel that the product team never checked. The community was treated as a source of goodwill, not a stakeholder whose trust could be depleted. | **Never promise a feature will ship — promise it will be evaluated.** The correct response: "I've logged this in our public feedback tracker (link). You'll see it's now 'Under Review.' Our product team reviews the tracker every 2 weeks — you'll get a status update whether the answer is 'planned,' 'not planned,' or 'we need more input.'" Maintain a public feature request board (Canny, Productboard portal, or GitHub Discussions) where every request gets a public status. Close the loop on every request within 30 days — a "no" with an explanation is better than silence. |
| Measured DevRel success by "developer signups" for 3 years — then discovered 60% of signups never made an API call, meaning the funnel was full of people who signed up for swag at a conference and never intended to build anything | A DevRel team's primary KPI was "developer signups" — and they hit 50,000 in 3 years. The board was impressed until a new CTO asked: "What percentage of those developers made an API call in the first 30 days?" Answer: 40%. "What percentage built a working integration?" Answer: unknown — they'd never tracked it. Investigation revealed 60% of signups were empty accounts: conference swag collectors, students who needed a project screenshot, and developers who tested 1 endpoint and left. The "50K developer community" was really 20K. | The DevRel team optimized for the easiest metric to inflate (signups) rather than the metric that matters (active developers). Signups can be gamed with giveaways, conference booth scanners, and email list imports. Active developers requires product value. | **Measure DevRel by Time-to-Value and developer activation, not signups.** Core metrics: (a) signup-to-first-API-call in minutes (target: <5 minutes with quickstart), (b) activation rate: % of signups who make >10 API calls in first 7 days, (c) dNPS segmented by tenure (are developers happier at month 6 than month 1?), (d) developer-influenced pipeline: deals where a developer champion exists. Report signups for vanity, but make decisions on activation. A 5,000-developer community where 4,000 are active is more valuable than a 50,000-developer community where 20,000 are ghosts. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You report "developer signups" and "community members" to leadership, and you've never calculated what percentage of them are active developers who build with your product | Your Quickstart guide enables a developer to make their first successful API call in under 5 minutes — you've tested it with 10 developers who'd never seen your product, timed them, and iterated until the median time was <5 minutes | You build a DevRel function from scratch at a company with no developer community — and within 18 months, you have >1,000 weekly active developers, a dNPS >60, and a champion program with 20+ members who contribute more documentation than your team writes |
| Your conference talks are product demos with a thin layer of "here's a best practice" — and developer attendees rate your sessions 3/5 or lower | You've killed a conference sponsorship 2 weeks before the event because the talk you planned wouldn't pass the "no-product test" — and you'd rather lose the $12K deposit than damage developer trust with a pitch disguised as a talk | A developer-influenced deal closes with a $500K ACV, and in the win interview the buyer says "your developer community was the reason we chose you — our engineers already trusted your product before we talked to sales" |
| You've told a developer "I'll share your feedback with the product team" and never followed up — and the developer noticed and stopped contributing to your community | You maintain a public feature request board where >90% of requests have a status updated within 30 days — and community members reference the board in conversations because they trust it | Competitors start hiring DevRel teams because your community is visibly driving product adoption — and the playbook they're copying is the one you wrote |

**The Litmus Test:** You're given a developer product you've never used, a 90-day deadline, and a budget of $30K. Can you: identify 3 developer communities where your target audience already gathers, contribute authentically (answer 50+ questions, publish 2 educational pieces, give 1 meetup talk), and produce 100 qualified developer signups with >40% activation? If you can do this without ever saying "check out our product" in your first 10 community interactions, you understand DevRel.

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
<!-- QUICK: 30s -- links to deeper reading -->
- [Developer Relations: How to Build and Grow a Successful Developer Program](https://www.amazon.com/Developer-Relations-Build-Successful-Program/dp/148427163X/) — Caroline Lewko, James Parton
- [The Business Value of Developer Relations](https://www.amazon.com/Business-Value-Developer-Relations-Community/dp/1484237474/) — Mary Thengvall
- [Community Canvas](https://community-canvas.org/) — Framework for designing communities
- [Contributor Covenant](https://www.contributor-covenant.org/) — Standard open source code of conduct
- [DevRel Collective](https://devrelcollective.fun/) — Community of DevRel professionals
- [Orbit Model](https://orbit.love/model) — Community member engagement framework
- [Measuring Developer Relations](https://devtomanager.com/) — DevRel metrics and ROI
- [SlashData — State of Developer Relations](https://www.slashdata.co/) — Annual industry benchmark report
- [DevRelCon](https://www.devrelcon.com/) — The main DevRel conference
- [references/community-health-survey.md](references/community-health-survey.md) — Template survey questions
- [references/hackathon-playbook.md](references/hackathon-playbook.md) — Step-by-step hackathon execution guide
