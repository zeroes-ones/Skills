# Core Workflow — Full Implementation

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
