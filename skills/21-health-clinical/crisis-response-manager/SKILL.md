---
name: crisis-response-manager
description: Adverse event (AE) reporting to FDA MedWatch, EudraVigilance, and manufacturer systems with 24-hour/7-day/15-day timelines. Suicide prevention escalation using Columbia-Suicide Severity Rating
  Scale (C-SSRS) with warm handoff to crisis lines. Public health emergency response for disease outbreak alerts and recall notifications in patient communities. Safety incident taxonomy with severity levels
  S1-S5, response SLAs, and escalation matrix. Crisis communication templates for patient notification, regulatory disclosure, and internal communications. Pharmacovigilance signal detection in community
  data with automated AE mention detection. Mental health crisis protocols for self-harm or harm-to-others indicators. Medical device adverse event reporting (MDR) for connected devices. Post-crisis review
  with root cause analysis, timeline reconstruction, and corrective action plans. Triggered by adverse event, crisis, pharmacovigilance, suicide prevention, safety incident, recall, medical device report,
  public health emergency.
author: Sandeep Kumar Penchala
type: health-clinical
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- crisis-response
- adverse-event-reporting
- pharmacovigilance
- suicide-prevention
- patient-safety
- medical-misinformation
- health-emergency
token_budget: 4000
output:
  type: code
  path_hint: ./
chain:
  consumes_from:
  - community-operations-manager
  - content-policy-manager
  - legal-advisor
  - trust-safety-engineer
  feeds_into:
  - community-operations-manager
  - content-policy-manager
  - incident-responder
---
# Crisis Response Manager

Manage health-related crises in patient-facing communities and digital health products — from adverse event detection and regulatory reporting to suicide prevention escalation and public health emergency response. This skill covers the full crisis lifecycle with regulatory timelines, safety taxonomies, communication templates, and post-crisis review protocols designed for FDA-regulated, patient-safety-critical environments.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Handle an adverse event (AE) report from a patient → Jump to "Core Workflow > Phase 1 (AE Detection & Reporting)"
├── Respond to a suicide risk or self-harm post → Go to "Decision Trees > Mental Health Crisis Escalation"
├── Classify a safety incident severity → Jump to "Decision Trees > Safety Incident Classification"
├── Draft crisis communications (patient, regulatory, internal) → Go to "Core Workflow > Phase 3 (Crisis Communication)"
├── Set up pharmacovigilance signal detection → Jump to "Core Workflow > Phase 4 (PV Signal Detection)"
├── Manage a product recall or public health alert → Go to "Core Workflow > Phase 2 (Public Health Emergency Response)"
├── Report a medical device adverse event (MDR) → Jump to "Core Workflow > Phase 1 (MDR reporting)"
├── Conduct a post-crisis review → Go to "Best Practices > Post-Crisis Review"
├── Need community operations coordination for patient communication? → Invoke `community-operations-manager` for patient notification and community recovery
├── Need content policy enforcement during crisis? → Invoke `content-policy-manager` for misinformation containment and policy updates
├── Need legal review of crisis communications or regulatory disclosures? → Invoke `legal-advisor` for liability assessment and regulatory review
├── Need incident response for data breach involving PHI? → Invoke `incident-responder` for forensic investigation and containment
└── Active crisis in progress? → Start at "Decision Trees > Crisis Activation" then follow escalation matrix
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never delay an AE report for investigation.** FDA MedWatch requires serious, unexpected AEs reported within 15 days (7 days for death or life-threatening). The clock starts when ANY employee becomes aware — not when the investigation concludes. Report first, investigate in parallel. Delayed reporting is a regulatory violation regardless of the investigation outcome.
- **Suicide risk posts require immediate human escalation — never automated-only response.** If a patient post indicates suicidal ideation with plan or intent, an automated "here's a crisis line number" response is insufficient. A trained human must assess using C-SSRS and perform a warm handoff to a crisis service. Do not leave a patient alone with an automated message.
- **Never minimize or dismiss a patient's safety concern.** "That's probably nothing" or "just a bruise, not a bleed" from community staff can discourage AE reporting. Every potential safety signal is treated seriously until triaged by a qualified safety professional (pharmacovigilance, clinical, or regulatory).
- **Crisis communications must be approved by Legal and Regulatory before release.** Patient notification of a safety issue, product recall, or data breach has legal and regulatory implications. Do not draft and send without Legal and Regulatory review — even for "minor" communications.
- **Admit what you don't know.** If you're unsure whether an event is reportable, the timeline applies, or which regulatory body has jurisdiction, escalate to Health Compliance and Legal Advisor immediately. Guessing wrong has regulatory consequences.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Detecting, triaging, and reporting adverse events (AEs) from patient community posts, app feedback, or support tickets
- Escalating suicide risk or self-harm indicators using C-SSRS assessment and warm handoff protocols
- Managing public health emergency communications (disease outbreaks, product recalls, safety alerts)
- Classifying safety incidents by severity (S1-S5) with defined response SLAs and escalation paths
- Drafting crisis communication templates for patients, regulators, and internal stakeholders
- Implementing pharmacovigilance signal detection in community and social listening data
- Reporting medical device adverse events (MDR) per FDA 21 CFR Part 803
- Conducting post-crisis reviews with root cause analysis and corrective action plans

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Safety Incident Classification
```
                     ┌──────────────────────────────┐
                     │ START: Safety incident detected│
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Involves death or           │
                    │ life-threatening injury?    │
                    └────┬──────────────────┬─────┘
                         │ YES              │ NO
                    ┌────▼────────────┐  ┌──▼──────────────────┐
                    │ S1 — Critical    │  │ Requires medical     │
                    │ Activate crisis  │  │ intervention or      │
                    │ team within      │  │ hospitalization?     │
                    │ 15 minutes.      │  └────┬──────────┬──────┘
                    │ Notify CEO,      │       │ YES      │ NO
                    │ Legal, Reg.      │  ┌────▼────┐ ┌──▼──────────┐
                    └──────────────────┘  │ S2 —     │ │ Affects >10  │
                                          │ Severe   │ │ patients or  │
                                          │ Activate │ │ has media    │
                                          │ within 1 │ │ potential?   │
                                          │ hour.    │ └──┬───────┬───┘
                                          │ Notify    │    │ YES   │ NO
                                          │ VP level. │ ┌──▼────┐ ┌──▼────┐
                                          └───────────┘ │ S3 —  │ │ S4 —  │
                                                        │ High  │ │ Medium│
                                                        │ Within│ │ Within│
                                                        │ 4 hrs │ │ 24 hrs│
                                                        └───────┘ └───────┘
```
**S1 — Critical:** Death, life-threatening event, or immediate threat to patient population. Activate crisis team within 15 minutes. CEO, Legal Advisor, Health Compliance, Regulatory notified. **S2 — Severe:** Requires medical intervention or hospitalization. No death. Activate within 1 hour. VP-level notification. **S3 — High:** Affects >10 patients or has media/social media potential. Within 4 hours. Director-level. **S4 — Medium:** Isolated event, no media risk, affect <10 patients. Within 24 hours. **S5 — Low:** Near-miss, potential concern, no patient impact. Within 72 hours. Standard review.

### Mental Health Crisis Escalation
```
                     ┌──────────────────────────────┐
                     │ START: Community post or       │
                     │ message indicates self-harm    │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Suicidal ideation with      │
                    │ plan, intent, or means?     │
                    └────┬──────────────────┬─────┘
                         │ YES              │ NO
                    ┌────▼────────────┐  ┌──▼──────────────────┐
                    │ IMMEDIATE        │  │ Suicidal ideation    │
                    │ ESCALATION       │  │ without plan or      │
                    │ 1. Call 988/     │  │ intent (wish to die, │
                    │    crisis line   │  │ passive ideation)?   │
                    │ 2. Contact       │  └────┬──────────┬──────┘
                    │    patient via   │       │ YES      │ NO
                    │    phone if      │  ┌────▼────────┐ ┌──▼──────┐
                    │    possible      │  │ Moderate     │ │ Low risk│
                    │ 3. Notify        │  │ risk.        │ │ Self-   │
                    │    clinical lead │  │ Administer   │ │ harm not│
                    │    within 5 min  │  │ C-SSRS.      │ │ indicated│
                    │ 4. Document      │  │ Warm handoff │ │ Document│
                    │    everything    │  │ to crisis    │ │ and      │
                    └──────────────────┘  │ line within  │ │ monitor. │
                                          │ 30 min.      │ │ Follow up│
                                          │ Follow up    │ │ in 24 hrs│
                                          │ in 24 hrs.   │ └──────────┘
                                          └──────────────┘
```
**Immediate escalation (plan/intent/means):** Call 988 Suicide & Crisis Lifeline (US) or local crisis service. If patient identifiable, contact them by phone if safe. Notify clinical lead within 5 minutes. Do NOT leave patient with only an automated message. **Moderate risk (ideation without plan):** Administer C-SSRS screening. Provide warm handoff to crisis resources within 30 minutes. Follow up in 24 hours. **Low risk:** Document concern. Monitor. Follow up in 24 hours. If any escalation in language, move to moderate risk.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~25 min): Adverse Event Detection and Regulatory Reporting
1. Detect potential AEs from all patient-facing channels: community posts, app feedback, support tickets, social media, clinical study data. Implement keyword/phrase detection (drug names + adverse event terminology from MedDRA) with human triage for flagged content.
2. Triage the event: is it a valid AE? Four elements required: (1) identifiable patient, (2) identifiable reporter, (3) a suspect product (drug, device, biologic), (4) an adverse event or fatal outcome. If all four present, it is reportable.
3. Determine seriousness: results in death, life-threatening, requires hospitalization or prolongs existing hospitalization, results in persistent or significant disability/incapacity, is a congenital anomaly/birth defect, or requires intervention to prevent permanent impairment/damage. Serious + unexpected = expedited reporting (15 days, or 7 days for death/life-threatening).
4. Report to the appropriate authority: FDA MedWatch (Form 3500 for voluntary, 3500A for mandatory), EudraVigilance (EU), manufacturer pharmacovigilance system (if involving their product). Use the correct form and timeline for the jurisdiction.
5. Document internally: create an incident record with timeline, reporter details, patient details, product details, event description, seriousness assessment, expectedness assessment, reporting timeline, and confirmation of submission. Retain per regulatory recordkeeping requirements (typically 10 years for FDA).

### Phase 2 (~20 min): Public Health Emergency Response
1. Detect the emergency signal: disease outbreak in patient community, product recall notification from manufacturer or FDA, safety alert from CDC/WHO/health authority, or data suggesting a cluster of serious AEs.
2. Activate the crisis team: Crisis Response Manager (lead), Health Compliance, Legal Advisor, Clinical Lead, CEO/designee (for S1-S2), Community Operations Manager (if patient-facing comms), Communications/PR (if media potential).
3. Verify the facts: confirm the source (manufacturer, regulator, clinical data), assess the scope (which patients, products, geographies are affected), determine the urgency (ongoing exposure vs retrospective concern).
4. Issue patient notification: what happened, what products/geographies are affected, what patients should do (stop use, contact HCP, seek medical attention), where to get more information (hotline, website), and what the company is doing about it. Legal/Regulatory review required before release.
5. Monitor and update: track patient inquiries, media coverage, social media sentiment. Issue updates as new information becomes available. Do not go silent — even "we are still investigating" updates maintain trust.

### Phase 3 (~20 min): Crisis Communication Templates
1. **Patient Notification Template:** (a) What happened — clear, factual, no speculation. (b) Who is affected — specific products, lot numbers, date ranges. (c) What patients should do — actionable instructions. (d) What we are doing — investigation status, corrective actions. (e) Contact information — hotline, website, HCP resources. Health literacy checked: ≤8th grade reading level.
2. **Regulatory Disclosure Template:** (a) Event description with date/time of first awareness. (b) Product identification (name, lot, NDC/UDI). (c) Patient impact summary (number affected, outcomes). (d) Root cause analysis status. (e) Corrective and preventive actions (CAPA). (f) Regulatory timeline compliance confirmation. Submit through formal regulatory channels, not email.
3. **Internal Communications Template:** (a) Situation summary (one paragraph). (b) What we know and what we do not know. (c) Current response status. (d) What employees should do if contacted by patients, media, or regulators (refer to designated spokesperson). (e) Next update expected.
4. All communications must: be approved by Legal and Regulatory, be consistent across channels, include a date/time stamp, and be archived for regulatory recordkeeping.

### Phase 4 (~25 min): Pharmacovigilance Signal Detection
1. Define the data sources: patient community posts, social media listening, app feedback, support tickets, clinical study data, published literature, regulatory databases (FAERS, EudraVigilance).
2. Implement automated detection: NLP-based keyword/phrase matching (drug names, product names + MedDRA Preferred Terms), sentiment analysis for negative health outcomes, anomaly detection for AE reporting rate spikes. Human triage validates all flagged content.
3. Triage detected signals: is this a new signal (not in the product label/Investigator Brochure), a change in frequency or severity of a known signal, or a known reaction at expected frequency? New signals require expedited assessment.
4. Validate the signal: clinical review by safety physician, causality assessment (Naranjo scale, WHO-UMC criteria), expectedness check against reference safety information, literature and database search for corroborating evidence.
5. Act on validated signals: update product labeling, issue Dear Healthcare Professional letter, update risk management plan (RMP/REMS), report to regulators, and communicate to patients and HCPs as appropriate.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Crisis response is inherently cross-functional. Delays in coordination compound patient risk and regulatory exposure. This table defines exactly who needs to know what and when.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Health Compliance** | Every AE report, every crisis activation | AE reportability determination, regulatory timeline, consent and privacy implications, FDA communication strategy |
| **Legal Advisor** | Crisis communications, regulatory disclosure, liability assessment | Communication review, regulatory submission review, liability exposure assessment, privilege determination |
| **Incident Responder** | Data breaches involving PHI, system failures affecting safety data | Incident severity, containment status, forensic findings, breach notification timeline |
| **Community Operations Manager** | Patient-facing crisis communications, community posts with safety concerns | Patient notification content, community moderation escalation, ambassador communication coordination |
| **CEO Strategist** | S1-S2 incidents, media-facing crises, regulatory enforcement actions | Situation summary, response status, reputational risk, regulatory exposure, media strategy |
| **Compliance Officer** | Regulatory reporting, CAPA tracking, audit preparation | Report submission confirmation, CAPA status, audit trail completeness, inspection readiness |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Potential AE detected in patient community or social media | Health Compliance, Clinical Lead | AE triage within 24 hours; reportability determination |
| Suicide risk with plan or intent detected | Clinical Lead (immediately), Health Compliance (within 1 hour) | Active intervention required; duty to warn; documentation for regulatory |
| Product recall or safety alert received from manufacturer or FDA | CEO Strategist, Legal Advisor, Community Operations Manager | Patient notification planning; regulatory response; media strategy |
| Safety signal validated (new or changed risk) | Health Compliance, Legal Advisor, CEO Strategist | Labeling update; regulatory submission; patient/HCP communication |
| Crisis communication released without Legal/Regulatory approval | Legal Advisor, Health Compliance, CEO Strategist | Damage control; corrective action; regulatory notification if applicable |

### Escalation Path

```
S1 — Critical (death, life-threatening)? → CEO + Legal + Health Compliance + Clinical Lead. War room within 15 minutes.
S2 — Severe (hospitalization, significant disability)? → VP-level + Legal + Health Compliance. Within 1 hour.
Regulatory inspection or enforcement action? → CEO + Legal + Health Compliance + Compliance Officer. Within 2 hours.
Media inquiry about safety incident? → CEO + Legal + Communications/PR. Do not respond before coordination.
```

### Regulatory Handoffs & Clinical Validation Gates

| Handoff Trigger | Route To | Protocol | Regulatory Timeline |
|----------------|----------|----------|---------------------|
| Serious, unexpected adverse event (SAE) — death or life-threatening | `compliance-officer` → FDA MedWatch | Report with available information → Continue investigation in parallel → Submit follow-up report when complete | **7 calendar days** |
| Serious, unexpected adverse event (SAE) — non-life-threatening | `compliance-officer` → FDA MedWatch | Report with available information → Continue investigation → Submit follow-up | **15 calendar days** |
| Medical device adverse event — death or serious injury | `compliance-officer` → FDA MDR | Submit MDR report → Manufacturer notification → Device investigation | **30 calendar days** |
| Suicide risk post with plan or intent detected | Clinical lead (immediately) → crisis line warm handoff | C-SSRS assessment by trained human → Stay with patient until connected → Document handoff | **Within 5 minutes** |
| Product recall or safety alert received from manufacturer or FDA | `ceo-strategist` → `legal-advisor` → `community-operations-manager` | Assess recall scope → Plan patient notification → Draft regulatory response → Coordinate media strategy | Within 24 hours of receipt |
| Validated safety signal (new or changed risk) | `compliance-officer` → `legal-advisor` → `ceo-strategist` | Signal validation → Labeling update assessment → Regulatory submission → Patient/HCP communication | Per regulatory requirement |
| Crisis communication released without Legal/Regulatory approval | `legal-advisor` → `compliance-officer` → `ceo-strategist` | Damage assessment → Corrective communication → Regulatory notification (if applicable) → Process review | Within 24 hours |

**Patient Safety Validation Gates:**
- **AE reportability gate:** Every potential AE must be triaged within 24 hours of ANY employee awareness. Clock starts at awareness, not at investigation conclusion. Missed timeline = FDA 483/Warning Letter. Artifact: AE triage form with reportability determination.
- **Suicide risk escalation gate:** No automated-only response to suicidal ideation. Trained human must assess using C-SSRS and perform warm handoff. Cold referral ("here's a number") is insufficient. Artifact: C-SSRS assessment documentation with handoff confirmation.
- **Crisis communication approval gate:** All external crisis communications (patient notification, regulatory disclosure, press statement) must receive Legal AND Regulatory approval before release. No exceptions for "minor" communications. Artifact: Communication approval form with sign-offs.
- **Post-crisis review gate:** Every S1-S3 incident requires blameless post-crisis review within 2 weeks. Must include: root cause analysis, timeline reconstruction, what worked, what didn't, corrective actions with owners and deadlines. Artifact: Post-crisis review report with CAPA assignments.
- **Evidence preservation gate:** Never delete or modify crisis-related content. Archive with timestamp and reason. Destroyed evidence = regulatory violation. Artifact: Content preservation log with chain of custody.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Report AEs first, investigate in parallel.** The clock starts when ANY employee becomes aware. A complete investigation is not required before reporting — submit with available information and update with follow-up reports.
- **Practice crisis scenarios quarterly.** Run tabletop exercises for: AE cluster detection, suicide risk post, product recall, data breach involving PHI, and FDA inspection. The first time your team sees a crisis scenario should not be during a real crisis.
- **Pre-draft and pre-approve communication templates.** Patient notification templates, regulatory disclosure templates, and internal communications templates should be drafted, reviewed by Legal and Regulatory, and stored in a crisis toolkit — not written from scratch during a crisis.
- **Maintain a single source of truth for crisis status.** Use a crisis dashboard or shared document that shows: current severity, timeline, actions taken, pending actions, responsible parties, and next update time. Everyone works from the same information.
- **Never delete or modify crisis-related content.** Patient posts, internal communications, investigation notes — all are discoverable. If a post is removed for safety reasons, archive it with a timestamp and reason. Do not destroy evidence.
- **Warm handoff means a live human connection.** For suicide risk, "here is the crisis line number" is a cold referral. A warm handoff means: you stay with the patient while they connect to the crisis service, confirm they are connected, and document the handoff.
- **Post-crisis review is not optional.** Every S1-S3 incident gets a blameless post-crisis review within 2 weeks. Root cause analysis, timeline reconstruction, what worked, what did not, and specific corrective actions with owners and deadlines.
- **Regulatory timelines are non-negotiable.** 7 days for death/life-threatening, 15 days for serious unexpected, 30 days for medical device death/serious injury. These are calendar days, not business days. Missed timelines are cited in FDA 483s and Warning Letters.

## Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| AE not reported within 15-day timeline | Triage delay; unclear who owns reporting; lack of awareness that clock started | Implement AE detection alerts with SLA timer; designate PV responsible person; train all staff that awareness = clock start |
| Community moderator dismissed potential AE as "just a complaint" | Lack of PV training; no clear escalation path | Train all patient-facing staff on AE identification (4 elements); implement flag-for-review button in moderation tools |
| Suicide risk post received automated crisis line response only | No human escalation protocol; after-hours coverage gap | Implement 24/7 on-call for clinical staff; warm handoff protocol with documentation requirements; after-hours escalation path |
| Crisis communication released with incorrect information | Drafted under time pressure without fact verification; bypassed review | Pre-approved templates with fill-in-the-blank format; mandatory Legal/Regulatory review before release; single approver for external comms |
| Post-crisis review findings not implemented (same issue recurs) | CAPA assigned but not tracked to completion; no accountability | Track CAPAs in a system with owners, deadlines, and status; quarterly CAPA review; link CAPAs to post-crisis review records |

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[CR1]**  AE detection and triage process documented with defined SLA from detection to triage decision (≤24 hours)
- [ ] **[CR2]**  AE reporting pathways established: FDA MedWatch, EudraVigilance, manufacturer PV systems
- [ ] **[CR3]**  Regulatory timeline tracker active: 7-day (death/life-threatening), 15-day (serious unexpected), 30-day (MDR)
- [ ] **[CR4]**  Suicide prevention escalation protocol documented with C-SSRS assessment and warm handoff procedures
- [ ] **[CR5]**  24/7 on-call coverage for S1-S2 crisis activation confirmed with contact roster current
- [ ] **[CR6]**  Safety incident taxonomy (S1-S5) documented with response SLAs and escalation matrix
- [ ] **[CR7]**  Crisis communication templates (patient, regulatory, internal) drafted, reviewed by Legal/Regulatory, and stored in crisis toolkit
- [ ] **[CR8]**  Pharmacovigilance signal detection configured for community and social listening data sources
- [ ] **[CR9]**  Medical device adverse event (MDR) reporting process documented per 21 CFR Part 803
- [ ] **[CR10]**  Crisis dashboard or shared status document template ready for immediate activation
- [ ] **[CR11]**  Quarterly crisis tabletop exercise schedule established with after-action reviews
- [ ] **[CR12]**  Post-crisis review process documented with root cause analysis, CAPA tracking, and 2-week completion SLA
- [ ] **[CR13]**  All patient-facing staff trained on AE identification and escalation (annual refresher)
- [ ] **[CR14]**  Crisis records retention policy documented per regulatory requirements (FDA: 10 years; EU: per GVP Module VI)

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 patients)
- **What changes**: AE detection = you reading every post and message. Manual MedWatch 3500 form. No automated signal detection. Crisis response = you + Legal counsel (external). No formal S1-S5 taxonomy — just "urgent" and "not urgent." Suicide protocol = crisis line number and follow-up. No post-crisis review process.
- **What to skip**: Automated PV signal detection. Crisis dashboard. Tabletop exercises. MDR reporting (unless you have a device). EudraVigilance (unless EU).
- **Coordination**: You are the crisis response team. External legal counsel on retainer.

### Small Team (2-10 people, 100-10K patients)
- **What changes**: AE triage process with trained moderators. MedWatch + manufacturer reporting. Basic keyword detection for AE terms. S1-S4 taxonomy with escalation paths. Crisis communication templates. Suicide warm handoff protocol with on-call during business hours. Quarterly crisis review. Post-crisis reviews for S1-S3.
- **What to skip**: 24/7 on-call (use escalation to leadership). Automated signal detection. Full pharmacovigilance system (use manual + keyword). Tabletop exercises. MDR system (unless applicable).
- **Coordination**: Designated Crisis Response Manager. Weekly safety review. Legal on retainer + quarterly check-in.

### Medium Team (10-50 people, 10K-100K patients)
- **What changes**: Dedicated pharmacovigilance or safety function. Automated AE detection with NLP. Full S1-S5 taxonomy with defined SLAs. 24/7 on-call rotation. Crisis communication templates pre-approved by Legal/Regulatory. Signal detection and validation process. Quarterly tabletop exercises. Post-crisis review with CAPA tracking in QMS. MDR reporting system if applicable. Crisis dashboard.
- **What to skip**: Full signal detection automation (semi-automated with human review). Global PV system (US + EU only). Dedicated crisis communications team.
- **Coordination**: Safety committee (bi-weekly). Crisis team roster with quarterly review. Post-crisis review board. Annual regulatory inspection readiness.

### Enterprise (50+ people, 100K+ patients)
- **What changes**: Pharmacovigilance department with qualified person for pharmacovigilance (QPPV) in EU. Fully automated AE detection across all data sources. Global PV system with multi-country reporting. 24/7 global safety coverage. Crisis communications team with dedicated media response. Continuous signal detection with statistical algorithms. Monthly tabletop exercises for different scenarios. CAPA system integrated with enterprise QMS. MDR and vigilance reporting for all device markets.
- **What's full production**: Global safety database. AI-assisted signal detection and validation. Crisis simulation program. Regulatory inspection management system. Board-level safety reporting.

### Transition Triggers
- **Solo → Small**: First serious AE. >500 patients. Community or social media with public visibility.
- **Small → Medium**: FDA-registered product. EU market entry (requires QPPV). >10K patients. First S1 incident.
- **Medium → Enterprise**: Multiple products in multiple markets. FDA inspection or Warning Letter. >100K patients. Public company or IPO track.

## What Good Looks Like

When a crisis hits, the response is swift, coordinated, and compassionate. Adverse events are reported within regulatory timelines. The team knows exactly who does what. Post-crisis reviews lead to concrete improvements. Patients feel protected, not policed.

## References
<!-- QUICK: 30s -- links to deeper reading -->
- **regulatory-specialist** — for AE reportability determination, regulatory timelines, and HIPAA in crisis contexts
- **legal-advisor** — for crisis communication review, liability assessment, and regulatory disclosure strategy
- **incident-responder** — for data breach response, incident command structure, and post-incident review methodology
- **community-operations-manager** — for patient-facing crisis communications and community moderation during crises
- **ceo-strategist** — for S1-S2 incident notification, media strategy, and reputational risk management
- **compliance-officer** — for regulatory reporting, CAPA tracking, and inspection readiness
- [FDA MedWatch](https://www.fda.gov/safety/medwatch-fda-safety-information-and-adverse-event-reporting-program) — AE reporting forms and guidance
- [FDA 21 CFR Part 803 — Medical Device Reporting](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-803) — MDR requirements
- [EudraVigilance](https://www.ema.europa.eu/en/human-regulatory-overview/research-development/pharmacovigilance-research-development/eudravigilance) — EU AE reporting system
- [Columbia-Suicide Severity Rating Scale (C-SSRS)](https://cssrs.columbia.edu/) — Suicide risk assessment tool
- [988 Suicide & Crisis Lifeline](https://988lifeline.org/) — US crisis line
- [ICH E2D — Post-Approval Safety Data Management](https://www.ich.org/page/efficacy-guidelines) — PV signal detection guidance
