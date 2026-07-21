---
name: content-strategist
description: Content planning, editorial calendars, content audits, content marketing funnel, topic clusters, content repurposing, tone of voice guidelines, content metrics.
author: Sandeep Kumar Penchala
type: growth
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - content-strategist
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
---
# Content Strategist

End-to-end content strategy system covering planning, creation, governance, and measurement. Designed for product-led and SaaS organizations building authority through topical depth, structured content operations, and data-driven iteration.

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
### Phase 1 (~15 min): Strategy Foundation

1. **Audience & Persona Research** — Define primary and secondary personas including: job titles, pain points, goals, information needs by funnel stage, preferred content formats, and channels. Validate with customer interviews, sales call recordings, and support ticket analysis.
2. **Content Mission Statement** — Articulate who the content serves, what unique value it provides, and how it differentiates from competitors. Example: "We help backend engineers transition from monolith to microservices with production-tested patterns."
3. **Topic Cluster Architecture** — Identify 3–5 pillar topics (broad, high-volume). For each pillar, map 15–30 cluster topics (specific, long-tail). Define internal linking strategy: every cluster post links to its pillar; pillar links to all clusters. This signals topical authority to search engines.
4. **Competitive Content Audit** — Analyze top 5 competitors: content formats, publishing cadence, average word count, content depth scores, backlink profiles, social engagement. Identify whitespace — topics they under-serve or formats they ignore.
5. **Deliverable: Content Strategy Brief** — A document including persona cards, topic cluster map, competitive analysis, content funnel mapping, and KPIs per funnel stage.

### Phase 2 (~30 min): Content Operations

1. **Editorial Calendar Setup** — Build a quarterly calendar with: working titles, target keywords, funnel stage, assigned writer, draft deadline, review deadline, publish date, distribution channels. Use Notion/Airtable/Asana with calendar and Kanban views.
2. **Content Brief Template** — Standardize briefs with: target persona, funnel stage, primary/secondary keywords, search intent (informational/commercial/transactional/navigational), target word count, outline with H2/H3 structure, internal links to include, competitor URLs to beat, CTAs.
3. **Tone of Voice Guidelines** — Define 3–4 brand voice attributes (e.g., "authoritative but approachable"). For each attribute: do/don't examples, vocabulary preferences, sentence structure guidance. Include grammar and formatting rules: Oxford comma usage, heading capitalization style, code snippet formatting.
4. **Review & Approval Workflow** — Define stages: outline review → first draft → peer review → SEO review → final edit → stakeholder approval (if needed) → publish. Set SLAs per stage. Use Google Docs "suggesting" mode or a collaborative CMS.
5. **Content Governance** — Establish content ownership (who updates what), refresh cadence (quarterly for high-traffic, annually for evergreen), deprecation criteria (outdated, low traffic for 12+ months, brand misalignment). Maintain a content inventory with status, owner, last-updated, and performance fields.

### Phase 3 (~20 min): Measurement & Optimization

1. **Content Metrics Framework** — Map metrics to funnel stages:
   - **Awareness**: organic sessions, impressions, new users, social shares, backlinks acquired
   - **Consideration**: time on page, scroll depth, newsletter sign-ups, gated asset downloads
   - **Conversion**: demo requests, free trial starts, contact sales form submissions, pipeline influenced
   - **Retention**: returning visitor rate, help doc satisfaction scores, churn reduction from educational content
2. **Content Performance Dashboard** — Build in Looker Studio/Tableau. Track: top 20 pages by traffic, top 20 by conversions, pages with highest growth/decline month-over-month, pages with high traffic but low conversion (optimization candidates), pages ranking positions 4–15 (quick-win targets).
3. **Content Refresh Program** — Quarterly: identify pages with declining traffic, update with current data/examples, improve depth, expand keyword coverage, re-publish with new date. Track uplift 30/60/90 days post-refresh.
4. **Repurposing Engine** — From each high-performing long-form piece, generate: Twitter thread, LinkedIn carousel, email newsletter version, podcast talking points, YouTube script, infographic. Maximize ROI per research investment.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- Always write for search intent first, search engines second. Google rewards content that satisfies user needs.
- Use the "inverted pyramid" structure: key takeaway first, supporting details next, background last.
- Every piece of content should have exactly one primary CTA. Too many choices reduce conversion.
- Maintain a content debt backlog alongside the editorial calendar — schedule at least one refresh per sprint.
- Interview subject matter experts before writing technical content; record and transcribe to capture nuance.
- Repurpose content based on data, not hunches — only promote pieces that have already validated with the target audience.
- Use the "skyscraper technique" for competitive topics: find the best existing content, make something 10x better, then promote it.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Content strategy sits between marketing, product, SEO, and brand. Content produced in silos underperforms; coordination amplifies reach and relevance.

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

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
Founder or solo marketer writing everything. Content strategy = a Notion doc. Publish 1-2 posts/week on company blog. Distribution: Twitter/LinkedIn + email to small list. SEO: basic keyword research (free tools), no cluster strategy. No editorial calendar beyond Google Calendar. Measure: page views + email signups. Cost: $0-200/month (CMS hosting, email tool free tier). Overkill: content agency, topic cluster tools, T-shaped writers, multi-channel attribution.

### Small (2-10 people, 100-10K users)
Hire 1-2 content writers or a fractional editor. Editorial calendar in Airtable/Notion. Publish 2-4 pieces/week. SEO: keyword research (Ahrefs/Semrush), topic clusters, pillar pages. Content refresh cycle established. Distribution: newsletter, social scheduling (Buffer/Hootsuite), syndication. Basic attribution: UTM + CRM tracking. Cost: $3K-10K/month. Overkill: in-house video production, dedicated content operations role.

### Medium (10-50 people, 10K-1M users)
Content team (3-5): editor, writers, content strategist, freelance pool. CMS with workflows and approvals. SEO: advanced (enterprise Ahrefs, Clearscope/MarketMuse). Content Ops: content management platform (Contentful/Sanity). Multi-channel: blog, newsletter, podcast, webinars, gated assets. Attribution: multi-touch, pipeline influence modeling. A/B test headlines, CTAs, formats. Cost: $15K-50K/month.

### Enterprise (50+ people, 1M+ users)
Content department (10+): specialists per channel, content ops manager, managing editor. Multi-language, multi-region content operations. AI-assisted content creation + human editorial review. Content supply chain: request → brief → draft → review → publish → distribute → measure. Full attribution: content-sourced vs content-influenced pipeline. Brand-level editorial standards. Cost: $100K-500K+/month.

### Transition Triggers
| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | >2 posts/week consistently for 3 months, or content requests > 1/day | Hire fractional writer/editor; add SEO tool (Ahrefs/Semrush); implement editorial calendar |
| Small → Medium | >4 posts/week, 3+ content channels active, or content ROI > $50K/month | Build in-house team; implement CMS workflows; add attribution model |
| Medium → Enterprise | Multi-language needs, >10 content creators, or content influences >$1M pipeline/month | Dedicate content ops; invest in AI tools; build content supply chain |


### Cross-skills Integration
The preceding skill in the chain documents output format requirements. The following skill in the chain expects that format. Run them sequentially:
```bash
#[previous-skill] && #[this-skill] && #[next-skill]
```
Document the output contract explicitly so consuming skills know what to expect.

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| **Content Audit & Inventory** | Traffic declining or content bloat >100 pieces | Screaming Frog, Google Analytics, GSC — categorize: keep/refresh/consolidate/delete |
| **Topic Cluster Architecture** | Building SEO authority for a new or competitive niche | Pillar + cluster model, keyword mapping, internal linking structure — Ahrefs, Semrush |
| **Editorial Calendar Design** | >2 writers contributing, multiple deadlines/week | Airtable, Notion, CoSchedule — align with product launches, campaigns, events |
| **Tone-of-Voice & Style Guidelines** | Multi-writer team, inconsistent brand voice across channels | Brand voice charter, style guide, writing templates, editorial review process |
| **Content Repurposing** | High-performing long-form content exists; want to maximize ROI | Blog → social threads, video scripts, newsletter, slides, infographics, podcast episodes |
| **Content ROI Measurement** | Justifying content budget or optimizing content investment | Multi-touch attribution, pipeline influence, content scoring — tools: Google Analytics, HubSpot, Salesforce |
| **B2B vs B2C Content Strategy** | Differentiating approach by audience type | B2B: case studies, whitepapers, webinars, LinkedIn. B2C: blog, video, social, email nurture |
| **AI-Assisted Content Production** | Scaling output while maintaining quality and brand voice | ChatGPT, Claude, Jasper — draft, research, summarize; human editing for accuracy + voice |


### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Organic traffic drops sharply | Algorithm update or technical SEO issue | Check GSC for manual actions, verify crawlability, check Core Web Vitals. Rollback recent structural changes. |
| Content ranks but doesn't convert | Content targets top-of-funnel only | Map content to buyer journey: awareness → consideration → decision. Every content piece has a next step CTA. |
| A/B test shows no winner | Sample size too small or test duration too short | Minimum 1 full business cycle per variant. Use sequential testing — don't peek at results. |
| Viral loop doesn't activate | Invite flow has friction | Cut invite flow to 3 taps max. Show invite value before asking. Track invite-to-signup conversion rate. |
| Developer community is silent | No low-friction contribution path | Start with issues labeled "good first issue." Respond within 24h. Celebrate first PR with public thank-you. |
| Paid acquisition CPA too high | Targeting too broad or creative not differentiated | Narrow to lookalike audiences. Test 5+ creative angles per audience segment. Kill underperformers after $500 spend. |
| Activation rate < 10% | Onboarding doesn't demonstrate core value in first session | Force "aha moment" within first 5 minutes. Cut all non-essential onboarding steps. Show value before asking for commitment. |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Content mission statement is documented and visible to all content creators
- [ ] **[S2]**  Topic cluster map exists with pillar pages and cluster relationships defined
- [ ] **[S3]**  Editorial calendar covers next 90 days with assignments, deadlines, and distribution plan
- [ ] **[S4]**  Content brief template is standardized and used for every assigned piece
- [ ] **[S5]**  Tone of voice guidelines are published and include do/don't examples for each voice attribute
- [ ] **[S6]**  Review workflow is defined with SLAs per stage and tracked
- [ ] **[S7]**  Content inventory is maintained with status, owner, last-updated, and performance data
- [ ] **[S8]**  Quarterly content audit process is in place — identifies gaps, refreshes, consolidations, and deletions
- [ ] **[S9]**  Content performance dashboard shows funnel-stage metrics and month-over-month trends
- [ ] **[S10]**  Keyword cannibalization is monitored and addressed within each content cluster
- [ ] **[S11]**  All published content has structured data (Article, HowTo, or FAQ schema as applicable)
- [ ] **[S12]**  Internal linking strategy is enforced — every new post links to pillar page and 3+ relevant cluster posts
- [ ] **[S13]**  Accessibility baseline met: proper heading hierarchy, alt text, sufficient color contrast in embedded graphics
- [ ] **[S14]**  Content refresh triggers are automated: pages dropping >20% traffic over 90 days flagged for review

## MVP vs Growth vs Scale

| Phase | Team Size | Content Volume | Priority | Content Approach |
|-------|-----------|---------------|----------|-----------------|
| **MVP (0→1)** | 1-3 devs, no content hire | 3-5 foundational pages | Educate early adopters | 1 long-form pillar post + 3 cluster posts + blog. Write in-house (founders or engineers). No calendar. Google Docs → publish. |
| **Growth (1→10)** | 3-10 devs, 1 content strategist + 1-2 writers | 2-4 posts/week | Build organic pipeline | Topic clusters, editorial calendar, content briefs, freelance writers. CMS (Ghost/WordPress). Quarterly audits. |
| **Scale (10→N)** | 10+ devs, content team (3-8) | 5-10 posts/week + programmatic | Defend authority, expand TAM | Multi-format (blog, video, podcast, newsletter, social). Content ops platform. Programmatic SEO. Editorial governance. |

**MVP content rule:** Write the 3 pieces your top competitor has that you don't. Make them 2x better. Ship in 2 weeks. Done.

## Cost-Effective Decision Table

| Decision | Free/Cheap Option | Paid Upgrade | When to Upgrade |
|----------|------------------|--------------|-----------------|
| CMS / publishing | Ghost (self-hosted, $9/mo VPS) or GitHub Pages + Markdown | WordPress VIP ($2K+/mo) or Contentful ($489/mo) | Need multi-author workflows, localization, or non-dev editors |
| Keyword research | Google autocomplete + AlsoAsked.com (free tier) | Ahrefs ($99/mo) or SEMrush ($129/mo) | Publishing >4 posts/month with strategic keyword targeting |
| Content optimization | Manual SERP analysis (look at top 10 yourself) | Clearscope ($170/mo) or MarketMuse ($149/mo) | >8 posts/month and need data-driven briefs at scale |
| Editorial calendar | Notion / Airtable (free) | CoSchedule ($29/mo) or Asana Premium | Team >4 writers needing calendar + assignment management |
| Freelance writers | Upwork / personal network ($0.10-0.30/word) | Content agency or in-house hire ($60K-120K/yr) | >8 posts/month or need deep domain expertise |
| Content analytics | Google Analytics 4 + Looker Studio (free) | ChartMogul + Mixpanel or Amplitude | Need attribution to pipeline/revenue, not just traffic |

**Annual content budget by phase:** MVP: $0-1K (time only). Growth: $15K-60K (freelancers + tools). Scale: $120K-500K+ (team + tools + multimedia).

## Scalability Decision Tree

```
Do you have >50 unoptimized posts that drive no traffic?
├── YES → Content audit first. Categorize: keep/refresh/consolidate/delete. Don't write new.
└── NO → Good. Proceed.

Is your publishing cadence causing quality issues (rushed, thin content)?
├── YES → Cut cadence by 50%. Double quality. 1 deep post > 4 shallow posts for SEO.
└── NO → Cadence is fine.

Are you ranking page 2 (positions 11-20) for 15+ target keywords?
├── YES → "Quick-win" refresh sprint: update those pages with fresher data, better depth, more internal links.
└── NO → Focus on new content in underserved topic areas.

Is keyword cannibalization visible (2+ pages ranking for same keyword, neither in top 3)?
├── YES → Merge cannibalized pages into one comprehensive page. 301 redirect the weaker one.
└── NO → Good targeting discipline.

Are you producing content in 1 format only (all blog posts)?
├── YES → Repurpose top 3 performers: blog → LinkedIn post → email newsletter → Twitter thread. Zero new research cost.
└── NO → Already multi-format. Focus on format that drives most conversions.
```


**What good looks like:** Content calendar published for the next 30 days with topics, authors, and distribution channels. Topic cluster map covers all primary keywords. Every content piece has a CTA linked to a measurable outcome. Content audit completed within the last 90 days.

## When NOT to Use This Skill (Overkill)

- **Product hasn't launched yet**: Content strategy before you know who your users are is writing blind. Wait until you have 50+ paying/users customers and can interview them.
- **Organic isn't your primary channel**: If you're a sales-led enterprise company closing 5 deals/year, content marketing won't move the needle. Invest in sales enablement docs instead.
- **You have 1 writer (and it's you)**: A 12-month editorial calendar, content brief template system, and quarterly audit process are overkill. Write 1 good post per week. Publish. Learn. Iterate.
- **Your topic is ultra-niche (TAM <10K people)**: Content strategy at scale assumes a large addressable market. If your audience is 500 CTOs at Fortune 500, do 1:1 outreach, not content marketing.
- **You're in a regulated industry where all content needs legal review (pharma, finance)**: Standard content velocity advice doesn't apply. Plan for 2-4 week legal review cycles and lower cadence.

## Token-Efficient Workflow

```
# Step 1: Quick audit — which content to refresh first?
# Run a script that queries GA4/GSC API, outputs prioritized list as JSON
python3 scripts/content_audit.py --site example.com --min-age 180 --output json
# Returns: [{"url":"/blog/x","traffic_change":-40,"priority":"high"}, ...]

# Step 2: Decision tree → pick action
# Traffic drop >30% + age >6 months → REFRESH (update data, expand, republish)
# Ranking position 4-15 → QUICK WIN (improve title, meta, internal links)
# Traffic <10 visits/month + age >12 months → DELETE or CONSOLIDATE

# Step 3: Execute the single action. Verify with exit codes.
# Check if a page has proper heading structure
curl -s https://example.com/blog/x | python3 -c "
import sys, re
html = sys.stdin.read()
h1 = len(re.findall(r'<h1[^>]*>', html))
h2 = len(re.findall(r'<h2[^>]*>', html))
print(f'H1:{h1} H2:{h2}')
sys.exit(0 if h1 == 1 else 1)
"

# Step 4: Verify impact — re-run audit after 30 days
python3 scripts/content_audit.py --site example.com --url /blog/x --compare-30d
```

**Principle:** Automated audit scripts output JSON. Agent reads structured data, not prose. Decision tree maps every audit finding to exactly one action. No deliberation loops.

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Content Marketing Institute — B2B Content Marketing Benchmarks](https://contentmarketinginstitute.com/)
- [HubSpot — Topic Clusters and Pillar Pages](https://blog.hubspot.com/marketing/topic-clusters-seo)
- [Backlinko — Skyscraper Technique](https://backlinko.com/skyscraper-technique)
- [Google — Search Quality Evaluator Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)
- [Clearscope — Content Optimization](https://www.clearscope.io/)
- [Animalz — Content Strategy Blog](https://www.animalz.co/blog/)
