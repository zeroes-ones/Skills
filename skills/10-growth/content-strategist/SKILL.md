---
name: content-strategist
description: >
  Use when planning content strategy, designing editorial calendars, auditing content inventories,
  architecting topic clusters, defining tone-of-voice guidelines, measuring content ROI, or building
  content marketing funnels. Handles content operations, repurposing workflows, audience persona
  development, and data-driven content iteration. Do NOT use for SEO keyword research, social media
  management, paid advertising strategy, or developer documentation authoring.
license: MIT
tags:
- content-strategy
- editorial
- content-marketing
- topic-clusters
- tone-of-voice
- content-audit
- content-operations
author: Sandeep Kumar Penchala
type: growth
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
chain:
  consumes_from:
  - devrel-advocate
  - product-manager
  - seo-specialist
  - ux-writer
  feeds_into:
  - devrel-advocate
  - marketing-manager
  - seo-specialist
---

# Content Strategist
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end content strategy system covering planning, creation, governance, and measurement. Designed for product-led and SaaS organizations building authority through topical depth, structured content operations, and data-driven iteration.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("editorial-calendar.*", "publish_date\|assigned_to")` OR `file_exists("content-calendar.csv")` | Editorial calendar is active. Jump to **Sub-Skills > Editorial Calendar Design**. |
| A2 | `file_exists("content-inventory.csv")` OR `file_contains("content-inventory.*", "page_url\|traffic\|status")` | Content inventory detected. Jump to **Sub-Skills > Content Audit & Inventory**. |
| A3 | `file_exists("tone-of-voice.md")` OR `file_exists(".vale.ini")` | Tone-of-voice guidelines exist. Jump to **Sub-Skills > Tone-of-Voice & Style Guidelines**. |
| A4 | `file_contains("topic-cluster.*", "pillar_page\|cluster_page")` OR `file_exists("keyword-map.*")` | Topic cluster architecture in play. Jump to **Sub-Skills > Topic Cluster Architecture**. |
| A5 | `file_exists("content-brief-template.md")` OR `file_contains("content-brief.*", "target_audience\|conversion_goal")` | Content production pipeline active. Jump to **Core Workflow > Phase 1**. |
| A6 | `file_contains("dashboard.*", "content_pipeline\|traffic_by_page")` OR `file_exists("content-performance-dashboard.*")` | Performance tracking active. Jump to **Sub-Skills > Content ROI Measurement**. |
| A7 | `file_exists("repurposing-workflow.md")` OR `file_contains(".*", "repurpos.*workflow\|format_adaptation")` | Repurposing workflow exists. Jump to **Sub-Skills > Content Repurposing**. |
| A8 | `file_exists("cms-config.*")` OR `file_contains("cms.*", "content_model\|publish_workflow")` | CMS/content ops infrastructure detected. Jump to **Core Workflow > Phase 2**. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:
```
What are you trying to do?
├── Content planning (pillars, personas, workflows)
│   ├── New content program → Start at "Core Workflow > Phase 1"
│   └── Existing program refresh → Go to "Core Workflow > Phase 2"
├── Editorial calendar design
│   └── Multi-writer coordination → Jump to "Sub-Skills > Editorial Calendar Design"
├── Content audit (inventory, categorization)
│   └── Traffic declining or content bloat → Go to "Sub-Skills > Content Audit & Inventory"
├── Content marketing funnel
│   └── Mapping content to buyer journey → Go to "Core Workflow > Phase 1"
├── Topic clusters & pillar strategy
│   └── Building SEO authority → Go to "Sub-Skills > Topic Cluster Architecture"
├── Content repurposing
│   └── Maximizing existing content ROI → Go to "Sub-Skills > Content Repurposing"
├── Tone of voice guidelines
│   └── Inconsistent brand voice → Go to "Sub-Skills > Tone-of-Voice & Style Guidelines"
├── Cross-skill: Coordinate content-keyword strategy with `seo-specialist` → Open that skill
├── Cross-skill: Involve `devrel-advocate` for developer tutorials → Open that skill
├── Cross-skill: Align campaign content with `marketing-manager` → Open that skill
└── Not sure? → Describe the problem in plain language and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to recommend content without audience persona evidence** | Trigger: User says "what content should we create?" or "build a content plan" without attaching persona doc, ICP definition, or audience research | STOP. Respond: "I need audience research before recommending content direction. Share your persona document or ICP definition — who is the target reader and what job do they need done? I'll help you build personas first if needed." |
| **R2** | **REFUSE to add items to editorial calendar without writer capacity estimate** | Trigger: User says "schedule this" or "add to calendar" without providing `estimated_hours` or `assigned_to` | STOP. Respond: "What's the estimated writer/editor capacity for this piece? A calendar without hours-per-piece is a wish list. I need `assigned_to` and `estimated_hours` before scheduling." |
| **R3** | **REFUSE to enforce tone-of-voice against aspirational brand values that contradict observed writing** | Trigger: User provides brand values (e.g., "bold, innovative") but writing samples show opposite style (formal, cautious) | DETECT. Respond: "These brand values don't match the writing samples. 'Bold' and 'innovative' aren't visible in the actual copy. Let's either update the values to match reality or rewrite the samples before we enforce guidelines the team can't follow." |
| **R4** | **REFUSE to cite "best practice" as sole justification without performance data** | Trigger: User asks "what's best practice for blog frequency/CTAs/headline length?" without sharing their own data | DETECT. Respond: "Instead of generic best practice, I'd rather anchor recommendations to your data. Share your content performance dashboard or analytics and I'll prescribe based on what's working for your specific audience." |
| **R5** | **STOP if >30% of recommended content in a plan has no conversion goal mapped** | Trigger: Content plan has 10+ pieces but fewer than 7 have `journey_stage` or `conversion_goal` fields populated | STOP. Respond: "I count {n} pieces without a conversion goal in this plan. Every content piece must map to a funnel stage (TOFU/MOFU/BOFU) and a measurable outcome. Let me add conversion goals before we finalize — content without an outcome is noise." |
| **R6** | **DETECT content debt >20% of inventory and block net-new creation** | Trigger: Content audit reveals >20% of published pages driving zero organic traffic for 6+ consecutive months | DETECT. Flag loudly: "Your inventory has {n} zombie pages ({pct}% of total) generating zero traffic for 6+ months. Schedule a cleanup sprint — merge, refresh, or deprecate — before creating anything new. Dead content drags down your site's overall quality signal." |
| **R7** | **REFUSE to publish content without a documented target keyword cluster** | Trigger: Content brief submitted for review without `keyword_cluster` or `primary_keyword` field populated | STOP. Respond: "This content piece has no keyword target. Every piece must map to a documented keyword cluster — otherwise it's competing blind. Share the keyword research before I review the content." |

## The Expert's Mindset

Master content strategists understand that strategy is not about predicting the future — it's about **being less wrong than the competition, faster**.

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
**Usage:** Invoke this skill with your target level, e.g., "as an L3 content strategist, develop..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Building a new content program from scratch — defining pillars, audience personas, and editorial workflows
- Running a content audit to identify gaps, consolidation opportunities, and refresh candidates
- Designing a topic cluster architecture to establish topical authority for SEO
- Creating or updating tone-of-voice and style guidelines across a multi-writer team
- Planning quarterly or annual editorial calendars aligned with product launches and campaigns
- Repurposing high-performing long-form content into derivative formats (social, email, video scripts)
- Measuring content ROI and building dashboards that connect content to pipeline/revenue
- Optimizing a content marketing funnel from awareness through conversion and retention

## Decision Trees

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Content Format Selection
```
                     ┌──────────────────────────┐
                     │ START: Which content      │
                     │ format to create?         │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Target is TOFU (Top of     │
                    │ Funnel — awareness)?       │
                    └────┬──────────────────┬───┘
                         │ YES              │ NO
                    ┌────▼──────┐    ┌──────▼──────────┐
                    │ Best for   │    │ BOFU (Bottom)?    │
                    │ organic    │    └──┬──────────┬────┘
                    │ search?    │       │YES       │NO (MOFU)
                    └──┬───┬─────┘  ┌────▼────┐ ┌───▼──────────┐
                       │YES│NO     │Case study│ │Webinar,      │
                  ┌────▼──┐┌▼──────┐│Comparison│ │Guide,         │
                  │Blog   ││Video, ││ROI calc, │ │Checklist,     │
                  │post,  ││Podcast││Free trial│ │Template —     │
                  │Guide  ││Social │└──────────┘ │POV content    │
                  │(SEO)  ││media  │              └──────────────┘
                  └───────┘└───────┘
```
**When to choose Blog/Guide:** TOFU + organic search focus — invest in SEO, cluster strategy, evergreen content with 6-12 month shelf life.  
**When to choose Video/Podcast:** TOFU + brand building — reach audiences on YouTube, Spotify; high production cost, long payback.  
**When to choose Case Study/Comparison:** BOFU — close deals with social proof; quantifiable ROI metrics required.  
**When to choose Webinar/Template:** MOFU — nurture leads with gated assets; capture email → nurture sequence.

### Content Refresh vs. New Creation
```
                     ┌──────────────────────────┐
                     │ START: Publish new or      │
                     │ refresh existing?          │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Existing page ranks #4-15  │
                    │ for target keyword AND     │
                    │ age > 6 months?            │
                    └────┬──────────────────┬───┘
                         │ YES              │ NO
                    ┌────▼──────┐    ┌──────▼──────────┐
                    │ Refresh   │    │ Keyword gap      │
                    │ existing  │    │ not covered at   │
                    │ page —    │    │ all?             │
                    │ update    │    └──┬──────────┬────┘
                    │ stats, add│      │YES       │NO
                    │ new       │ ┌────▼────┐ ┌──▼──────────┐
                    │ section,  │ │Create new│ │Content      │
                    │ republish │ │pillar +  │ │cannibaliz-  │
                    │ with new  │ │cluster   │ │ation risk — │
                    │ date      │ └──────────┘ │consolidate  │
                    └───────────┘               │or de-optimize│
                                                └─────────────┘
```
**When to Refresh:** Existing page ranks #4-15, 6+ months old — update stats, add new sections, republish with fresh date (SEO win in 30-60 days).  
**When to Create New:** Keyword gap uncovered, no existing page within striking distance — build pillar + cluster, target long-tail first.  
**When to Consolidate:** Multiple pages competing for same keyword — merge into one definitive resource, 301 redirects.

### Content Distribution Channel Mix
```
                     ┌──────────────────────────┐
                     │ START: Where to distribute │
                     │ this content?              │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Content drives organic     │
                    │ search traffic (SEO ROI)?  │
                    └────┬──────────────────┬───┘
                         │ YES              │ NO
                    ┌────▼──────┐    ┌──────▼──────────┐
                    │ SEO +     │    │ Content is        │
                    │ owned     │    │ time-sensitive?   │
                    │ channels  │    └──┬──────────┬────┘
                    │ + email   │       │YES       │NO
                    │ nurture   │  ┌────▼────┐ ┌──▼──────────┐
                    └───────────┘  │Social    │ │Gated asset  │
                                   │(real-time)│ │— email      │
                                   │+ push     │ │capture +    │
                                   │notifications│ │retargeting │
                                   └──────────┘ └─────────────┘
```
**When to choose SEO + Owned:** Evergreen content, ROI from organic — invest in keyword research, backlinks, updates. Distribution: blog + newsletter.
**When to choose Social + Push:** News, announcements, time-sensitive — Twitter, LinkedIn, Slack communities, push notifications.  
**When to choose Gated + Retargeting:** High-value lead gen asset — landing page, form, email sequence, retargeting ads.

### Content Audit Decision Matrix
```
                     ┌──────────────────────────────┐
                     │ START: How to handle existing  │
                     │ content piece?                 │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Traffic > 100/month AND        │
                    │ conversion rate > 1%?          │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ KEEP +        │    │ Traffic > 100    │
                    │ OPTIMIZE:     │    │ but < 1% CVR?    │
                    │ Add CTAs,     │    └──┬──────────┬────┘
                    │ update offers,│      │YES       │NO
                    │ internal links│ ┌────▼────┐ ┌──▼──────────┐
                    └───────────────┘ │REFRESH  │ │Traffic < 10 │
                                      │Improve  │ │AND age > 1yr│
                                      │CVR: CTAs,│ └──┬──────┬───┘
                                      │offers,   │   │YES   │NO
                                      │format    │┌──▼──┐┌─▼──────┐
                                      └──────────┘│DELETE││KEEP +  │
                                                   │or 301││MONITOR │
                                                   │redirect││(low   │
                                                   └──────┘│priority)│
                                                           └────────┘
```
**When to Keep + Optimize:** High traffic + high CVR — your best assets. Update CTAs, add related content links, optimize for conversions.  
**When to Refresh:** High traffic, low conversion — content is found but doesn't convert. Improve CTAs, update offers, or fix format/paywall.
**When to Delete/Redirect:** <10 visits/month, >1 year old, no backlinks — prune. 301 redirect to closest relevant page.

### Content Team Structure Decision
```
                     ┌──────────────────────────────┐
                     │ START: How to staff content?   │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Publishing cadence > 4         │
                    │ long-form pieces/week?         │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ In-house team │    │ Need specialized  │
                    │ + freelance   │    │ domain expertise  │
                    │ pool for      │    │ (SME-level)?     │
                    │ overflow      │    └──┬──────────┬────┘
                    └───────────────┘       │YES       │NO
                                       ┌────▼────┐ ┌──▼──────────┐
                                       │Agency+  │ │Freelance    │
                                       │SME      │ │generalist   │
                                       │external │ │or small     │
                                       │partners │ │in-house team│
                                       └─────────┘ └─────────────┘
```
**When to build in-house team:** >4 pieces/week, need deep product knowledge, fast iteration — hire editor + writers; supplement with freelancers.
**When to use Agency + SME:** Niche domain expertise (legal, medical, financial) — pair agency with subject matter experts for accuracy.  
**When to use Freelance:** <4 pieces/week, general topics — cost-effective, flexible, no benefits overhead.

## Core Workflow

<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Strategy Foundation

1. **Audience & Persona Research** — Define primary and secondary personas including: job titles, pain points, goals, information needs by funnel stage, preferred content formats, and channels. Validate with customer interviews, sales call recordings, and support ticket analysis.
2. **Content Mission Statement** — Articulate who the content serves, what unique value it provides, and how it differentiates from competitors. Example: "We help backend engineers transition from monolith to microservices with production-tested patterns."
3. **Topic Cluster Architecture** — Identify 3–5 pillar topics (broad, high-volume). For each pillar, map 15–30 cluster topics (specific, long-tail). Define internal linking strategy: every cluster post links to its pillar; pillar links to all clusters. This signals topical authority to search engines.
4. **Competitive Content Audit** — Analyze top 5 competitors: content formats, publishing cadence, average word count, content depth scores, backlink profiles, social engagement. Identify whitespace — topics they under-serve or formats they ignore.
5. **Deliverable: Content Strategy Brief** — A document including persona cards, topic cluster map, competitive analysis, content funnel mapping, and KPIs per funnel stage.

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): Content Operations

1. **Editorial Calendar Setup** — Build a quarterly calendar with: working titles, target keywords, funnel stage, assigned writer, draft deadline, review deadline, publish date, distribution channels. Use Notion/Airtable/Asana with calendar and Kanban views.
2. **Content Brief Template** — Standardize briefs with: target persona, funnel stage, primary/secondary keywords, search intent (informational/commercial/transactional/navigational), target word count, outline with H2/H3 structure, internal links to include, competitor URLs to beat, CTAs.
3. **Tone of Voice Guidelines** — Define 3–4 brand voice attributes (e.g., "authoritative but approachable"). For each attribute: do/don't examples, vocabulary preferences, sentence structure guidance. Include grammar and formatting rules: Oxford comma usage, heading capitalization style, code snippet formatting.
4. **Review & Approval Workflow** — Define stages: outline review → first draft → peer review → SEO review → final edit → stakeholder approval (if needed) → publish. Set SLAs per stage. Use Google Docs "suggesting" mode or a collaborative CMS.
5. **Content Governance** — Establish content ownership (who updates what), refresh cadence (quarterly for high-traffic, annually for evergreen), deprecation criteria (outdated, low traffic for 12+ months, brand misalignment). Maintain a content inventory with status, owner, last-updated, and performance fields.

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): Measurement & Optimization

1. **Content Metrics Framework** — Map metrics to funnel stages:
   - **Awareness**: organic sessions, impressions, new users, social shares, backlinks acquired
   - **Consideration**: time on page, scroll depth, newsletter sign-ups, gated asset downloads
   - **Conversion**: demo requests, free trial starts, contact sales form submissions, pipeline influenced
   - **Retention**: returning visitor rate, help doc satisfaction scores, churn reduction from educational content
2. **Content Performance Dashboard** — Build in Looker Studio/Tableau. Track: top 20 pages by traffic, top 20 by conversions, pages with highest growth/decline month-over-month, pages with high traffic but low conversion (optimization candidates), pages ranking positions 4–15 (quick-win targets).
3. **Content Refresh Program** — Quarterly: identify pages with declining traffic, update with current data/examples, improve depth, expand keyword coverage, re-publish with new date. Track uplift 30/60/90 days post-refresh.
4. **Repurposing Engine** — From each high-performing long-form piece, generate: Twitter thread, LinkedIn carousel, email newsletter version, podcast talking points, YouTube script, infographic. Maximize ROI per research investment.

## Cross-Skill Coordination

<!-- QUICK: 30s -- table of who to talk to when -->
Content strategy sits between marketing, product, SEO, and brand. Content produced in silos underperforms; coordination amplifies reach and relevance.

### Decision Gates & Artifacts

| Gate | Condition | Action |
|------|-----------|--------|
| Content ↔ SEO | Keyword strategy or topic cluster change | Loop in `seo-specialist`; share keyword targets and SERP intent analysis |
| Content ↔ Product | Feature launch or messaging pivot | Coordinate with `product-manager`; align content calendar with roadmap |
| Content ↔ DevRel | Developer-focused content or tutorial series | Involve `devrel-advocate`; co-author technical content with developer perspective |
| Content ↔ Marketing | Campaign launch or lead magnet creation | Sync with `marketing-manager`; align content funnel to demand gen goals |
| Content ↔ UX Writing | In-product copy or onboarding flow | Coordinate with `ux-writer`; maintain brand voice consistency across surfaces |

**Artifacts shared across skills:**
- Editorial calendar (shared with `marketing-manager`, `seo-specialist`, `devrel-advocate`)
- Content brief templates (shared with `seo-specialist`, `ux-writer`)
- Tone-of-voice guidelines (shared with `ux-writer`, `devrel-advocate`, `marketing-manager`)
- Content performance dashboards (shared with `growth-engineer`, `marketing-manager`, `seo-specialist`)

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **SEO Specialist** | Keyword research, content planning, audits | Keyword targets, SERP intent, content gap analysis, cannibalization risks |
| **Growth Engineer** | Content-led growth experiments, landing pages | Content as experiment variant, conversion copy for A/B tests |
| **UX Writer / Product** | In-product copy, onboarding flows, microcopy | Tone of voice alignment, terminology consistency, user-facing messaging |
| **Marketing/Demand Gen** | Campaign content, lead magnets, email sequences | Content calendar alignment, campaign briefs, distribution channel strategy |
| **Social Media Manager** | Content distribution, repurposing | Social-optimized excerpts, visual assets, engagement data for topic ideation |
| **Technical Writer** | Documentation, knowledge base, blog | Editorial standards for docs, content hierarchy, cross-linking strategy |
| **Data/Analytics** | Content performance, funnel metrics | Content attribution model, engagement metrics, conversion tracking by content piece |
| **Design/Brand** | Visual content, infographics, brand consistency | Brand guidelines, visual asset requirements, content format specifications |
| **Product Strategist** | Product launches, feature announcements | Product roadmap, feature positioning, customer-facing messaging |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Editorial calendar shift >2 weeks | Marketing, Social Media, SEO Specialist | Distribution, promotion, and keyword targeting depend on timing |
| Content underperforming benchmark by >50% after 30 days | SEO Specialist, Growth Engineer, Data | May need SEO refresh, promotion boost, or format change |
| New topic cluster identified (strategy pivot) | SEO Specialist, Marketing, Product Strategist | Realignment of content investment; cross-team buy-in needed |
| Brand voice/tone guidelines updated | UX Writer, Technical Writer, Marketing | Consistency across all public-facing content surfaces |
| Competitor launches major content initiative | SEO Specialist, Product Strategist, Marketing | Competitive response needed; content differentiation strategy |
| Content audit reveals >20% of content is stale/outdated | SEO Specialist, Technical Writer | Refresh or deprecation decisions; 301 redirect planning |
| High-performing content generating leads but not tracked | Data/Analytics, Growth Engineer | Attribution gap; content ROI under-reported |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Content strategy misaligned with product direction | **Product Strategist** + CEO Strategist | Strategic realignment; product-market messaging disconnect |
| >3 months of content investment with zero attributable pipeline | **Growth Engineer** + Marketing Lead | ROI crisis; strategy or distribution fundamentally broken |
| Brand reputation risk from published content | **Legal Advisor** + PR/Comms | Libel, trademark, or regulatory exposure |
| Resource request denied for critical content hire | **CEO Strategist** or CMO | Content under-investment affects all growth channels |
| Content team blocked by engineering (CMS, publishing, tooling) | **CTO Advisor** + Project Manager | Operational bottleneck; needs engineering prioritization |

### Route to Other Skills

- **`seo-specialist`** — When content needs keyword research, SERP analysis, topic cluster architecture, or SEO content briefs
- **`product-manager`** — When content strategy needs product roadmap alignment, feature positioning, or competitive messaging
- **`devrel-advocate`** — When creating developer tutorials, technical blog posts, or community-facing content
- **`marketing-manager`** — When aligning content calendar with campaigns, demand gen, or multi-channel distribution

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| Content audit reveals > 30% of pages are stale or driving zero traffic | Run refresh/consolidate sprint before creating anything new; merge thin posts into comprehensive resources; 301 redirect | Content debt compounds — old thin pages drag down site authority signal; fix debt before adding more |
| High-performing pillar post loses > 20% traffic over 90 days | Flag for immediate refresh: update data, add new sections, improve internal links, check for competitor content that surpassed it | A declining pillar is a compounding loss — each month of decline costs more in lost organic traffic than fixing it costs |
| Competitor publishes definitive content that outranks yours for a core keyword | Analyze competitor piece for depth, freshness, format; plan 10x better version; prioritize over net-new content | Defending existing rankings is cheaper than earning new ones — react within 30 days or cede the position permanently |
| Keyword cannibalization detected — 2+ pages competing for same term, neither in top 3 | Merge cannibalized pages into one comprehensive resource; 301 redirect weaker pages; update internal links | Cannibalization splits your authority — one strong page beats three weak ones on the same keyword |
| Content calendar slip > 3 weeks — multiple deadlines missed | Audit root cause: writer capacity, review bottleneck, unclear briefs; reduce calendar to sustainable cadence; add buffer days | A calendar with constant slips is a wish list — cut volume before stakeholders stop trusting publish dates |
| Attribution gap identified — high-performing content generating leads not tracked in CRM | Implement UTM + CRM tracking; add content attribution to pipeline reporting; close the loop within one month | Content ROI is invisible without attribution — untracked leads are under-reported impact that costs budget justification |
| Content team blocked by CMS or publishing tooling for > 2 weeks | Escalate to engineering/product; request temporary workaround (e.g., publish to staging URL, use alternative CMS); quantify opportunity cost | Blocked publishing is an operational emergency, not a nice-to-have — each week of delay compounds missed traffic and lead generation |
| Brand voice inconsistency flagged in public by audience — "did someone else write this?" | Audit recent content for voice alignment; reinforce tone-of-voice guide with editorial team; add Vale linter to CI | Brand voice inconsistency erodes trust faster than grammatical errors — audience notices before internal review does |

## What Good Looks Like

> 

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.


### Cross-skills Integration
```mermaid
graph LR
    A[product-manager] --> B[content-strategist]
    B --> C[devrel-advocate]
    D[seo-specialist] --> B
    B --> E[technical-writer]
```
Run skills in the order shown:
```bash
# Chain A: product-manager → content-strategist → devrel-advocate
# Chain B: seo-specialist → content-strategist → technical-writer
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

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Cost-Effective Decision Table**: See [cost-decisions.md](references/cost-decisions.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **MVP vs Growth vs Scale**: See [mvp-growth-scale.md](references/mvp-growth-scale.md)
- **Scalability Decision Tree**: See [scalability-tree.md](references/scalability-tree.md)
- **Scale Depth**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)
- **Token-Efficient Workflow**: See [token-workflow.md](references/token-workflow.md)
- **When NOT to Use This Skill (Overkill)**: See [when-not-to-use.md](references/when-not-to-use.md)

