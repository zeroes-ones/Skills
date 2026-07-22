---
name: community-operations-manager
description: Patient ambassador and peer mentorship program design with matching, training, boundaries, and compensation. Community health metrics including engagement rate, response rate, sentiment analysis,
  and clinical outcome correlations. Patient events such as virtual roundtables, in-person HTC events, conference meetups, and webinar programs. Community growth strategy via organic growth, clinical referral
  partnerships, and advocacy organization relationships. Moderation escalation partnership with trust-safety-engineer and content-policy-manager. Patient privacy in communities with HIPAA implications in
  community settings. Community segmentation by condition subtype, treatment regimen, age cohort, and caregiver vs patient roles. Gamification and recognition including top contributor programs, expert
  patient badges, and clinical advisory roles. Cultural competency for non-English communities, cultural attitudes toward treatment, and faith-based considerations. Triggered by patient community, peer
  mentorship, community operations, patient engagement, health community, support groups.
author: Sandeep Kumar Penchala
type: health-clinical
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- patient-community
- peer-mentorship
- community-operations
- patient-engagement
- health-community
- support-groups
token_budget: 4000
output:
  type: code
  path_hint: ./
chain:
  consumes_from:
  - content-policy-manager
  - crisis-response-manager
  - patient-health-educator
  - trust-safety-engineer
  feeds_into:
  - content-policy-manager
  - crisis-response-manager
  - patient-experience-researcher
---
# Community Operations Manager

Build, nurture, and scale patient communities that deliver measurable health outcomes and sustainable engagement. This skill covers the full community operations lifecycle — from peer mentorship program design and community health metrics to patient events, cultural competency, and the delicate balance between patient privacy and community connection — designed for health communities serving patients with chronic and rare conditions.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Design a peer mentorship program → Jump to "Core Workflow > Phase 1 (Peer Mentorship Design)"
├── Define community health metrics → Go to "Core Workflow > Phase 2 (Community Health Metrics)"
├── Plan patient events (virtual, in-person, hybrid) → Jump to "Core Workflow > Phase 3 (Patient Events)"
├── Grow the community organically → Go to "Decision Trees > Community Growth Strategy"
├── Segment the community for targeted programming → Jump to "Core Workflow > Phase 2 (Segmentation)"
├── Handle moderation escalation → Go to "Best Practices > Moderation Partnership"
├── Design a gamification or recognition program → Jump to "Best Practices > Gamification & Recognition"
├── Address cultural competency gaps → Go to "Best Practices > Cultural Competency"
├── Managing a crisis or safety incident in the community? → Invoke `crisis-response-manager` immediately for AE reporting and safety protocols
├── Need content policy or moderation guidance? → Invoke `content-policy-manager` for community guidelines and escalation rules
├── Need trust and safety infrastructure? → Invoke `trust-safety-engineer` for abuse detection and platform safety
├── Need patient experience research for community insights? → Invoke `patient-experience-researcher` for patient journey mapping and community-based recruitment
└── Don't know where to start? → Describe your community (size, condition, maturity) and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never treat patient communities as marketing channels.** A health community exists for peer support and health outcomes — not for product promotion or brand building. Community members detect and reject inauthenticity instantly. Every program, event, and communication must pass the test: "Does this serve patients first?"
- **Peer mentors are not free labor.** Mentors contribute lived experience that clinicians cannot replicate. Compensate them: honoraria, stipends, conference sponsorship, or clinical advisory board roles. Uncompensated mentorship programs burn out your best members and exploit patient expertise.
- **Community segmentation must not create exclusion.** Segmenting by condition subtype, treatment regimen, or age cohort is valuable for relevance — but ensure cross-segment connection points exist. Isolated segments become echo chambers. Every segment needs to feel part of the larger community.
- **Patient privacy in communities is non-negotiable.** Community platforms are not HIPAA-covered entities, but the community operator has an ethical duty to protect patient information. Never expose identifiable health data without explicit consent. What a patient shares publicly is their choice; what the community operator shares about them is not.
- **Admit what you don't know.** If you have not validated your community health metrics against clinical outcomes, tested your mentorship matching algorithm for bias, or assessed cultural competency gaps, say so before scaling the program.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Designing a peer mentorship program for newly diagnosed patients matched with experienced patients
- Defining and tracking community health metrics (engagement, response rate, sentiment, outcomes)
- Planning patient events: virtual roundtables, in-person HTC meetups, conference gatherings, webinars
- Developing community growth strategies through clinical referrals and advocacy partnerships
- Establishing moderation escalation workflows in partnership with trust-safety and content-policy teams
- Segmenting the community for targeted programming (by condition, treatment, age, caregiver status)
- Designing gamification and recognition programs (top contributor badges, expert patient roles)
- Building cultural competency into community operations for diverse patient populations

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Community Growth Strategy
```
                     ┌──────────────────────────────┐
                     │ START: Community needs to grow │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Established relationships   │
                    │ with clinical providers?    │
                    └────┬──────────────────┬─────┘
                         │ YES              │ NO
                    ┌────▼────────────┐  ┌──▼──────────────────┐
                    │ Clinical referral│  │ Existing patient      │
                    │ partnerships    │  │ advocacy org           │
                    │ (HTCs, clinics, │  │ relationships?         │
                    │ specialty        │  └────┬──────────┬───────┘
                    │ pharmacies)      │       │ YES      │ NO
                    └────┬─────────────┘  ┌────▼────┐ ┌──▼──────────┐
                         │                │ Advocacy │ │ Organic      │
                    ┌────▼────────────┐   │ org      │ │ growth:      │
                    │ HTC referral    │   │ partner- │ │ social media,│
                    │ cards, clinic   │   │ ships    │ │ patient      │
                    │ posters, care   │   │ (NHF,    │ │ word-of-mouth│
                    │ team champion   │   │ HFA, WFH)│ │ SEO, content │
                    └─────────────────┘   └──────────┘ └──────────────┘
```
**When to use clinical referral:** Established HTC/clinic relationships, care team willing to recommend community, HIPAA-compliant referral mechanism (opt-in, not automatic). Best for condition-specific communities where clinical endorsement drives trust. **When to use advocacy partnerships:** National/global patient organizations (NHF, HFA, WFH for hemophilia). Co-branded events, cross-promotion, shared resources. **When to use organic growth:** Early-stage community without clinical partnerships. Social media patient groups, condition-specific hashtags, SEO-optimized content, patient-to-patient invites.

### Community Segmentation Matrix
```
                     ┌──────────────────────────────┐
                     │ START: Segment the community   │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Primary segmentation:       │
                    │ Condition subtype or        │
                    │ treatment regimen?          │
                    └────┬──────────────────┬─────┘
                         │ condition        │ treatment
                    ┌────▼────────────┐  ┌──▼──────────────────┐
                    │ Hem A, Hem B,   │  │ Prophylaxis,          │
                    │ VWD, inhibitors,│  │ on-demand, gene       │
                    │ carriers        │  │ therapy, non-factor,  │
                    └────┬────────────┘  │ clinical trial        │
                         │               └────┬──────────────────┘
                    ┌────▼────────────┐       │
                    │ Secondary: age   │  ┌────▼────────────────┐
                    │ cohort +         │  │ Secondary: treatment │
                    │ caregiver status │  │ experience + side    │
                    │ (pediatric       │  │ effect profile       │
                    │ caregiver, adult │  └─────────────────────┘
                    │ patient, aging)  │
                    └──────────────────┘
```
**Primary segmentation by condition:** Hemophilia A, Hemophilia B, VWD, inhibitors, carriers — different medical journeys, different community needs. **Primary segmentation by treatment:** Prophylaxis (infusion fatigue, adherence), on-demand (bleed recognition, treatment delay), gene therapy (expectation management, long-term uncertainty), clinical trial (hope + anxiety). **Secondary always includes:** age cohort (parent of young child vs adult self-infuser vs aging with hemophilia) and caregiver status.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~25 min): Peer Mentorship Program Design
1. Define the mentorship program structure: one-to-one matching (newly diagnosed → experienced patient), group mentorship (3-5 mentees per mentor), or tiered (peer supporter → mentor → lead mentor). Duration: 3-month minimum for meaningful relationship; 6-month for chronic condition adjustment.
2. Recruit mentors from engaged community members: minimum 1 year since diagnosis (or 1 year as caregiver), demonstrated supportive communication style in community posts, completion of mentor training. Verify identity and condition status — mentors representing inaccurate experience damage trust.
3. Design the matching algorithm: primary match on condition subtype and treatment regimen, secondary on demographics (age, gender, language, geography), tertiary on interests and life stage. Allow mentees to request a rematch without explanation.
4. Train mentors: active listening, boundaries (mentors are not clinicians — recognize when to escalate to clinical resources), crisis recognition (suicide risk, AE reporting), confidentiality expectations, and self-care (mentor burnout is real — limit to 2 active mentees).
5. Structure the mentorship journey: week 1 icebreaker prompts, weeks 2-4 establishing trust, months 2-3 deepening the relationship, month 3 check-in and renewal decision. Provide conversation prompts each week. Measure: mentee satisfaction (≥4/5), mentor retention (>70% at 6 months), mentee community engagement increase post-mentorship.

### Phase 2 (~25 min): Community Health Metrics and Segmentation
1. Define community health KPIs: engagement rate (DAU/MAU, target >30%), weekly active posters (>15% of members), reply rate (>3 replies per thread average), time-to-first-response (<1 hour median), sentiment score (net positive), member retention (30-day, 90-day, annual).
2. Track clinical outcome correlations (where consented): does community engagement correlate with treatment adherence, PRO scores, HTC visit attendance, or reduced ER visits? This is the holy grail of health community metrics — it justifies clinical referral partnerships and payer interest.
3. Implement churn prediction: member inactive for 14 days → automated re-engagement (personalized nudge, relevant thread, peer match suggestion). Member inactive for 30 days → human outreach. Track churn reasons: life improvement (good churn — patient no longer needs support), dissatisfaction, platform fatigue, health deterioration.
4. Segment members for targeted programming: by condition subtype (Hem A vs Hem B vs VWD), treatment regimen (prophy vs on-demand vs gene therapy), age cohort (parents of young children, adolescents, young adults, adults, aging with condition), caregiver vs patient, language and culture group.
5. Build a community health dashboard: real-time KPIs by segment, trend lines with anomaly detection, churn early warning, mentorship program metrics, event attendance and satisfaction. Share monthly with product, clinical, and executive stakeholders.

### Phase 3 (~20 min): Patient Events and Programming
1. Design the event calendar: weekly (themed discussion threads, "Tuesday Treatment Talk"), monthly (Ask-Me-Anything with hematologist, peer support circle, caregiver coffee hour), quarterly (virtual roundtable with 3-5 patients sharing experiences, research update webinar), annual (in-person HTC meetup, conference gathering at NHF/ASH/ISTH).
2. Plan virtual events: platform selection (Zoom with closed captioning, or community-native platform), accessibility (live captioning, sign language interpreter if needed, screen-reader-compatible materials), time zones (rotate times to accommodate global members), recording policy (record with consent, make available for 30 days).
3. Plan in-person events: venue accessibility (wheelchair accessible, near public transit), health safety (infusion-friendly spaces, refrigeration for factor, emergency plan for bleeds), cost (free for patients, travel stipends for financial hardship), consent for photography and sharing.
4. Execute event promotion: announcement 14 days out (what, when, who, why attend), reminder 7 days out, day-before reminder, 1-hour reminder. Post-event: thank-you with recap, survey for feedback, share recordings/slides with those who could not attend.
5. Measure event success: attendance rate (registered vs attended), satisfaction score (≥4/5), net promoter score, new member acquisition from event, returning attendee rate.

### Phase 4 (~20 min): Community Growth and Advocacy Partnerships
1. Build clinical referral partnerships: approach HTC social workers and nurse coordinators (they are the gatekeepers of patient resources), provide referral cards and digital assets, train care teams on what the community offers (and what it does not — it is not medical advice), track referral source for attribution.
2. Partner with patient advocacy organizations: National Hemophilia Foundation (NHF), Hemophilia Federation of America (HFA), World Federation of Hemophilia (WFH), local chapters. Co-host events, cross-promote content, share research opportunities, coordinate advocacy campaigns.
3. Drive organic growth: SEO-optimized content for condition-specific search terms ("living with hemophilia A," "parenting a child with hemophilia"), social media presence in patient groups (authentic participation, not promotion), patient-to-patient invitation with incentive ("bring a friend to our next event").
4. Monitor growth health: are new members representative of the patient population? Track demographic diversity of new members vs target population. Growth that only reaches highly engaged, English-speaking, urban patients is not sustainable — it leaves behind the patients who need community most.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Community operations bridges patients, clinical teams, product, and content. Coordination ensures the community serves patients effectively while maintaining safety, privacy, and alignment with organizational goals.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Customer Success Manager** | Patient satisfaction, churn signals, feedback aggregation | Community sentiment trends, member satisfaction scores, churn reasons, feature requests from community |
| **Content Policy Manager** | Community guidelines, moderation policy, content escalation | Community norm violations, content policy gaps, moderation precedent cases, policy updates needed |
| **Crisis Response Manager** | Safety incidents in community, AE reports, crisis communications | Community posts flagged for safety, patient notification coordination, post-crisis community recovery |
| **Product Strategist** | Community feedback for roadmap, feature validation, community growth KPIs | Feature requests ranked by community demand, community health metrics, patient needs not met by product |
| **Marketing Manager** | Community events promotion, advocacy partnerships, patient stories | Event promotion assets, partnership opportunities, patient story acquisition (with consent), community growth campaigns |
| **Clinical Informatics Specialist** | Community health metrics, clinical outcome correlations, PRO data from community | Community engagement data for clinical correlation, PROM data from community activities, patient-reported outcomes |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Community engagement drops >20% month-over-month | Product Strategist, Customer Success Manager | Product or community experience issue; investigate root cause |
| Safety concern detected in community (self-harm, AE, abuse) | Crisis Response Manager (immediately), Content Policy Manager | Escalation protocol; content moderation; patient safety |
| Peer mentor reports burnout or requests to step down | Clinical lead (if clinical mentor), mentorship program lead | Mentor replacement; program design review; burnout prevention |
| New advocacy partnership opportunity (NHF, HFA, WFH) | Marketing Manager, Product Strategist | Partnership evaluation; co-marketing plan; resource allocation |
| Community member publicly shares identifiable PHI | Content Policy Manager, Health Compliance | Content removal assessment; patient privacy guidance; HIPAA implications |

### Escalation Path

```
Patient safety concern (self-harm, suicide risk, adverse event)? → Crisis Response Manager. Within 5 minutes.
Community data breach (member PII exposed)? → Security Engineer + Health Compliance + Legal Advisor. Within 1 hour.
Widespread community dissatisfaction (coordinated member exodus)? → Product Strategist + Customer Success Manager. Within 24 hours.
Advocacy partnership at risk (contract dispute, reputational issue)? → Marketing Manager + Legal Advisor + CEO Strategist. Within 48 hours.
```

### Regulatory Handoffs & Patient Safety Protocols

| Handoff Trigger | Route To | Protocol | Safety Timeline |
|----------------|----------|----------|-----------------|
| Community member posts suicidal ideation with plan or intent | `crisis-response-manager` (immediately) | Do NOT respond with automated message → Flag content → Human assessment using C-SSRS → Warm handoff to crisis service → Document | Within 5 minutes |
| Potential adverse event detected in community post (drug side effect, device malfunction) | `crisis-response-manager` → `compliance-officer` | Flag post → Do NOT delete → Document timestamp → Transfer for AE triage → Preserve content for regulatory record | Within 1 hour |
| Community member publicly shares identifiable PHI (name + diagnosis + location) | `content-policy-manager` → `compliance-officer` | Assess content → Contact member privately (if safe) → Offer to edit/remove → Document action with rationale | Within 2 hours |
| Coordinated misinformation campaign targeting patient community | `content-policy-manager` → `crisis-response-manager` | Identify pattern → Assess clinical risk → Policy enforcement → Community communication → Escalate if safety risk | Within 4 hours |
| Peer mentor reports burnout or boundary violation by mentee | Clinical lead (if clinical mentor), mentorship program lead | Provide mentor support → Review boundaries → Adjust mentee assignment → Document incident | Within 24 hours |
| Community engagement drops >20% month-over-month | `product-strategist` → `patient-experience-researcher` | Root cause analysis → Member interviews → Sentiment analysis → Corrective action plan | Within 1 week |

**Patient Safety Gates:**
- **Peer mentor matching gate:** Mentor-mentee matching must consider: condition subtype, treatment regimen, age cohort, language, and mentorship boundaries. Unmatched pair = potential harm. Artifact: Mentor matching criteria document with bias assessment.
- **Community content escalation gate:** Any post mentioning self-harm, suicidal ideation, adverse events, abuse, or medical emergencies must be escalated to human review within 5 minutes. No automated-only response. Artifact: Escalation log with timestamp and resolution.
- **Patient privacy gate:** No identifiable health data exposed without explicit consent. What a patient shares publicly is their choice; what the community operator shares about them is not. Artifact: Privacy impact assessment for community features.
- **Cultural competency gate:** Non-English communities require dedicated moderators from those communities. Translated content ≠ culturally competent content. Artifact: Cultural competency assessment per language/region.
- **Ambassador compensation gate:** Peer mentors compensated at fair market rates (honoraria, stipends, conference sponsorship). Uncompensated mentorship = exploitation. Artifact: Ambassador compensation policy with rate schedule.

## Best Practices
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Peer-led communities outperform company-led.** Facilitate, enable, and amplify — do not direct. The best community managers are invisible; the best communities feel member-owned.
- **New members need a prompt to post within 24 hours.** A generic "introduce yourself" prompt gets ignored. Ask a specific, low-stakes question: "What is one thing you wish you had known at diagnosis?" Specific prompts get 3x the response rate.
- **One negative post can define the community experience for lurkers.** 90% of members never post — they judge the community by how you handle conflict. Respond to negativity constructively, do not suppress it. A well-handled disagreement builds more trust than a perfectly positive feed.
- **Ambassadors are your most valuable and most vulnerable asset.** Recognize them publicly, compensate them fairly, protect them from burnout. An ambassador who leaves feeling exploited will tell their story — and that story will be heard by every patient in your community.
- **Community segmentation creates relevance but risks isolation.** Cross-pollinate with all-community events, shared discussion threads, and segment spotlights. Members should feel both "my people" (segment) and "our community" (whole).
- **HIPAA does not apply to patient communities, but patient privacy ethics do.** A patient sharing their own health information in a community is not a HIPAA event. But the community operator aggregating, analyzing, or resharing that data introduces privacy obligations. Treat patient data with clinical-grade respect even when the law does not require it.
- **Cultural competency means more than translation.** A Spanish-language community is not an English community translated. Cultural attitudes toward treatment, family roles in healthcare, faith-based coping — these shape the community experience. Hire community managers from the communities you serve.
- **Gamification in health communities must be designed with care.** A leaderboard of "most bleeds survived" is harmful. Recognition programs should celebrate supportiveness, not suffering. "Most helpful responses" is better than "most posts." Never gamify health outcomes — it creates perverse incentives.

## Error Decoder
<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|-------|------------|-----|
| Only 10% of new members post in first week | Passive activation flow; no specific prompt | Add a specific, low-stakes first-post prompt; trigger peer match within 24 hours; measure activation step by step | First-week posting predicts long-term retention — design for a win within 24 hours, not just access. |
| Same 5 members dominate every discussion | No engagement distribution strategy; quiet members not amplified | Create small-group channels (8-12 members); feature "member spotlight" posts; send personal invites to contribute | A healthy community distributes voice across its members — the loudest 5% speaking for everyone is a design failure, not a participation problem. |
| 50% mentor dropout after 1 month | No mentor training, support, or boundaries; excessive mentee load | Limit to 2 active mentees; provide monthly mentor support calls; recognize and compensate mentors | Mentors burn out from lack of support, not lack of desire — invest in their experience as heavily as you invest in mentees. |
| Community growth stalls at ~500 members | Growth depends on organic only; no referral or partnership channels | Add clinical referral partnerships; partner with advocacy organizations; invest in SEO for condition-specific content | Organic growth caps around 500 members for health communities — pipeline requires clinical partnerships and SEO to break through. |
| Members from non-English backgrounds disengage after onboarding | Community is monolingual; cultural content irrelevant | Create language-specific sub-communities with dedicated moderators; culturally adapt prompts and events; hire from the community | Language access is not a translation problem — it is a community design problem that requires native-speaking moderators and culturally adapted content. |

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[CM1]**  Community purpose and guidelines documented, visible to all members, and enforced consistently
- [ ] **[CM2]**  New member activation flow: welcome → prompt → peer match → first value within 24 hours
- [ ] **[CM3]**  Peer mentorship program: mentor recruitment, training, matching, boundaries, compensation, measurement
- [ ] **[CM4]**  Community health dashboard: DAU/MAU, posters, reply rate, time-to-first-response, sentiment, retention
- [ ] **[CM5]**  Churn risk detection and re-engagement: 14-day inactive → automated; 30-day inactive → human outreach
- [ ] **[CM6]**  Community segmentation implemented: condition subtype, treatment regimen, age cohort, caregiver status, language
- [ ] **[CM7]**  Event calendar: weekly themes, monthly AMAs, quarterly roundtables, annual in-person events
- [ ] **[CM8]**  Event accessibility: closed captioning, time zone rotation, recording availability, physical accessibility for in-person
- [ ] **[CM9]**  Clinical referral partnerships established with HTCs, clinics, or specialty pharmacies
- [ ] **[CM10]**  Advocacy organization partnerships active (NHF, HFA, WFH, local chapters)
- [ ] **[CM11]**  Moderation escalation workflow documented with Crisis Response Manager and Content Policy Manager
- [ ] **[CM12]**  Ambassador or recognition program designed with compensation policy and burnout prevention
- [ ] **[CM13]**  Cultural competency: language-specific sub-communities, culturally adapted content, diverse community management team
- [ ] **[CM14]**  Patient privacy guidance documented: what can/cannot be shared, consent for stories, data use policy

## Scale Depth: Solo → Small → Medium → Enterprise
<!-- DEEP: 10+min -->

### Solo (1 person, 0-100 members)
- **What changes**: Community = a Facebook group or WhatsApp chat. You are the community manager + moderator. No formal mentorship program — you introduce members manually. No metrics beyond member count. Events = occasional Zoom call. No segmentation. No cultural competency program (but be mindful).
- **What to skip**: Peer mentorship program (manual introductions only). Community health dashboard. Formal events. Clinical referral partnerships. Ambassador program. Segmentation beyond basic condition types.
- **Coordination**: You are the community. Manual everything.

### Small Team (2-10 people, 100-1K members)
- **What changes**: Dedicated community platform (Discourse, Circle, or custom). Structured peer mentorship program with 10-20 mentors. Basic community health metrics (DAU/MAU, posts, replies). Monthly virtual events (AMA, support circle). Basic segmentation (condition subtype, caregiver vs patient). Moderation guidelines with escalation path.
- **What to skip**: Clinical outcome correlations. Clinical referral program (organic + advocacy only). Cultural competency program (ad hoc). Ambassador recognition program (informal). Churn prediction (manual review).
- **Coordination**: Weekly community team standup. Monthly community health review. Quarterly event planning.

### Medium Team (10-50 people, 1K-10K members)
- **What changes**: Community team (2-3). Scaled peer mentorship (50+ mentors). Full community health dashboard with segment-level metrics. Monthly + quarterly events (virtual + in-person). Segmentation by condition, treatment, age, caregiver, language. Clinical referral partnerships with HTCs. Ambassador program with recognition and compensation. Moderation team with defined shifts. Cultural competency: language-specific sub-communities.
- **What to skip**: Clinical outcome correlations (exploratory only). Payer partnerships. Full community analytics data warehouse. Global 24/7 moderation.
- **Coordination**: Bi-weekly community operations review. Monthly partnership check-in. Quarterly community strategy with Product and Marketing.

### Enterprise (50+ people, 10K+ members)
- **What changes**: Community department (5+). Peer mentorship at scale with program manager. Clinical outcome correlation studies (IRB-approved). Multi-language, multi-region communities. In-person events globally (conference presence, regional meetups). Payer and employer partnerships. Community analytics data warehouse with ML-driven churn prediction. 24/7 global moderation. Full cultural competency program with diverse community management team. Ambassador governance board.
- **What's full production**: Community health impact studies (published research). Payer-integrated community programs. Community representative on product governance. Annual community strategy cycle.

### Transition Triggers
- **Solo → Small**: >100 members. Demand for peer matching exceeds manual capacity. Members requesting regular events.
- **Small → Medium**: >1K members. Multiple segments with different needs. Clinical partners asking for referral program. >3 languages represented.
- **Medium → Enterprise**: >10K members. Multi-country presence. Payer or pharma partnership interest. Published community health research.

## What Good Looks Like

The community feels alive and safe. Members support each other without staff intervention 80% of the time. Ambassador programs run themselves. Events calendar is full and attended. Community health metrics trend upward. Pharma partners see the community as a model of patient engagement.

## References
<!-- QUICK: 30s -- links to deeper reading -->
- **customer-success-manager** — for patient satisfaction measurement, churn prediction, and feedback aggregation
- **content-policy-manager** — for community guidelines, moderation policy, and content escalation frameworks
- **crisis-response-manager** — for safety incident protocol, AE reporting, and crisis communication in community
- **product-strategist** — for translating community insights into product roadmap and strategic priorities
- **marketing-manager** — for community events promotion, advocacy partnerships, and patient story acquisition
- **clinical-informatics-specialist** — for clinical outcome correlations, PRO data integration, and community health analytics
- [CMX Community Industry Report](https://cmxhub.com/) — Community management benchmarks and best practices
- [National Hemophilia Foundation (NHF)](https://www.hemophilia.org/) — Patient advocacy and community resources
- [World Federation of Hemophilia (WFH)](https://wfh.org/) — Global bleeding disorders community
- [FeverBee Community Management](https://www.feverbee.com/) — Community strategy and engagement frameworks
