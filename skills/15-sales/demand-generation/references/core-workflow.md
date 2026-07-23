# Core Workflow — Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->

<!-- DEEP: 10+min -->

### Phase 1 (~20 min): Pipeline Modeling & Target Setting

Build a reverse funnel from revenue target: Revenue target → Pipeline needed (at close rate X) → SQLs needed (at SQL→Opp rate Y) → MQLs needed (at MQL→SQL rate Z) → Leads needed (at Lead→MQL rate W). Example: $2M quarterly revenue target. Avg deal size $50K = 40 closed deals. Close rate 25% = 160 opportunities. SQL→Opp rate 60% = 267 SQLs. MQL→SQL rate 15% = 1,780 MQLs. Lead→MQL rate 10% = 17,800 leads. Now allocate across channels: organic %, paid %, email %, events %, partner %. Track actuals vs. plan weekly. Reforecast monthly.

<!-- DEEP: 10+min -->

### Phase 2 (~60 min): Marketing Operations Setup

Marketing ops is the infrastructure: choose your platform (HubSpot for SMB/mid-market, Marketo for enterprise, Pardot if Salesforce-native required). Set up: (1) Tracking — UTM parameters enforced on every outbound link, form submissions captured with source data, cookie-based tracking for anonymous visitors, first-touch and last-touch fields populated at conversion, (2) Lead lifecycle stages — Visitor → Lead → MQL → SQL → Opportunity → Customer → Evangelist, with automated stage transitions based on scoring and actions, (3) Email automation — nurture sequences triggered by behavior (content download → related nurture track, pricing page visit → sales outreach alert), (4) List hygiene — bounce management, unsubscribe compliance, deduplication, suppression lists, (5) Attribution — U-shaped model as default, campaign influence tracking, ROI dashboards by channel, (6) Reporting — weekly pipeline dashboard: leads by channel, MQL volume, MQL→SQL rate, SQL→Opp rate, pipeline created, CAC by channel, LTV:CAC ratio.

<!-- DEEP: 10+min -->

### Phase 3 (~45 min): Email Marketing & Nurture

Design nurture sequences, not email blasts. Architecture: (1) Welcome sequence (3 emails over 7 days) — triggered on first conversion. Email 1: deliver the asset. Email 2: social proof + case study. Email 3: soft CTA (demo, trial, assessment), (2) Behavioral triggers — pricing page visit → case study email within 1 hour, feature page visit → product demo video, high engagement → sales alert, inactivity (30 days no click) → re-engagement drip (subject: "Still interested?"), (3) Newsletter (bi-weekly) — curated content, product updates, customer stories. Segment by persona so CTOs don't get end-user content, (4) Re-engagement — 3-email sequence for dormant leads. Email 1: "We miss you" + value. Email 2: "Last chance" + offer. Email 3: "Confirm you want to stay" — no click = unsubscribe. Always run a 10% holdout group on nurture sequences. Measure: open rate >20%, CTR >3%, unsubscribe <0.5% per send, conversion rate from nurture >5%.

<!-- DEEP: 10+min -->

### Phase 4 (~30 min): CAC Optimization

Calculate CAC per channel: total channel spend / customers acquired from that channel (using your chosen attribution model). Benchmark: LTV:CAC ratio > 3:1, CAC payback < 12 months. Optimization levers: (1) Creative — test 5+ ad variants per platform, kill underperformers after $500 spend, scale winners, (2) Targeting — narrow by job title, company size, industry, intent signals (G2 category page visits, competitor brand searches), use lookalike audiences from your best customers, (3) Landing page CRO — A/B test headline, hero image, CTA copy, form length, social proof placement, (4) Offer — test ebook vs. benchmark report vs. assessment vs. demo. High-intent offers (demo, trial, assessment) produce fewer leads but higher conversion to SQL, (5) Channel mix — shift spend toward channels with lowest CAC and highest LTV, not just lowest CPL. A $200 CPL channel that converts 20% to SQL beats a $50 CPL channel that converts 2%.

<!-- DEEP: 10+min -->

### Phase 5 (~45 min): ABM + Webinar Programs

**ABM (Account-Based Marketing):** Identify 50-500 target accounts (named list, not segments). Tier them: Tier 1 (1:1, 10-50 accounts — personalized gifts, executive outreach, custom content), Tier 2 (1:few, 50-200 accounts — industry-specific content, direct mail, semi-personalized ads), Tier 3 (1:many, 200-500 accounts — programmatic ads, email sequences, personalized landing pages by industry). For each tier: define the account plan (key contacts, engagement plan, content assets, success metrics). Measure: account engagement score, pipeline created from target accounts, deal velocity for ABM-sourced vs. non-ABM, average deal size uplift. Target: ABM accounts should have 2x pipeline velocity and 30% higher ACV than non-ABM.

**Webinar/Virtual Event Playbook:** (1) Topic selection — solve a specific pain, not a product pitch. "How [Role] at [Company Type] Reduced [Metric] by [X]%." (2) Speaker — customer + your expert. Customer stories convert 3x better than vendor-only. (3) Promotion — email to your list 3x: 2 weeks before, 1 week before, day before. LinkedIn ads targeting job title + industry for net-new. Partner co-promotion for reach extension. (4) During — polls every 10 minutes (engagement + data capture), Q&A throughout (not just at end), demo in last 10 minutes only, (5) Post-webinar — send recording + slides within 24 hours. No-show sequence: "We missed you — here's the recording." Attendee sequence: "Thanks for attending — here's the next step" (case study, trial, assessment). Measure: registration rate, attendance rate (>35% is good), on-demand views, pipeline created within 30 days.
