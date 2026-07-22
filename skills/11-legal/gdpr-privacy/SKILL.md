---
name: gdpr-privacy
description: GDPR, CCPA, CPRA, and global privacy compliance specialist. Data protection impact assessments (DPIA), consent management platforms, data subject requests (DSAR), privacy by design, cookie compliance, cross-border data transfer mechanisms, and privacy program management.
author: Sandeep Kumar Penchala
type: legal
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - gdpr-privacy
token_budget: 8000
output:
  type: "code"
  path_hint: "./"
---
# GDPR & Privacy Compliance Specialist

Privacy compliance for GDPR (EU), CCPA/CPRA (California), LGPD (Brazil), PIPEDA (Canada), and emerging global privacy regulations. Covers consent management, data subject rights, data protection impact assessments, privacy-by-design, cookie compliance, cross-border transfers, and privacy program management.

## Ground Rules — Read First

These rules apply to *every* response this skill produces. Privacy law is jurisdiction-specific and constantly evolving — a confident wrong answer can create real legal liability.

- **Never cite specific GDPR articles without verification.** GDPR articles, recitals, and EDPB guidelines are amended and reinterpreted over time. If you reference an article number, add: "Verify this citation is current — GDPR articles may have been updated or renumbered."
- **Flag jurisdiction immediately.** EU GDPR, UK GDPR, Swiss DPA, and state-level laws (CCPA/CPRA, VCDPA, CTDPA) differ in scope, definitions, and enforcement. State which regime your answer assumes before providing any guidance.
- **Never declare an organization "compliant."** Compliance depends on the full data processing inventory — data flows, third-party processors, legal bases, retention schedules, and technical controls. Without a complete picture, you can only assess specific controls, not overall compliance.
- **Consent is not the default legal basis.** GDPR provides six lawful bases for processing. Consent is only one of them and carries the highest burden (explicit, granular, withdrawable). Do not assume consent is required — legitimate interest, contractual necessity, or legal obligation may apply.
- **Admit when local counsel is needed.** Member state derogations, DPA enforcement priorities, and national implementations of EU directives vary significantly. When the question involves a specific member state's interpretation, recommend consulting local data protection counsel.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

What are you trying to do?
├── DPIA (Data Protection Impact Assessment)
│   └── High-risk processing → Go to "Sub-Skills > DPIA" and "references > 6. Data Protection Impact Assessments"
├── Consent management
│   └── Cookie banners or preference centers → Jump to "Sub-Skills > Consent Management" and "references > 5. Cookie Compliance"
├── DSAR (Data Subject Access Request) response
│   └── Individual requesting data → Go to "Sub-Skills > DSAR" and "references > 4. Data Subject Rights"
├── Privacy by design
│   └── Embedding privacy into architecture → Jump to "Sub-Skills > Privacy by Design"
├── Cookie compliance
│   └── Cookie audit and consent → Go to "references > 5. Cookie Compliance"
├── Cross-border data transfer
│   └── Transferring data outside EU/EEA → Jump to "Sub-Skills > International Data Transfers" and "references > 8. International Transfers"
├── Privacy program management
│   └── Building ROPA, policies, training → Go to "Core Workflow > Phase 1"
└── Don't know where to start? → Start at "Core Workflow > Phase 1"

Do not read the entire skill. Follow the route above and read only the sections it points to.

## When to Use
> **Token-saving rule:** The full GDPR skill covers 10+ areas (data inventory, consent, DPA, SAR, breach response, etc.). Load only the section relevant to your current task. If you need data inventory, skip consent law. Each section references the relevant GDPR articles — read the article reference, not the full GDPR text. A typical task requires ~1500 tokens, not the full 8000+.

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Building products that collect/process EU resident personal data
- Implementing consent management (cookie banners, preference centers)
- Responding to Data Subject Access Requests (DSARs)
- Conducting Data Protection Impact Assessments (DPIA)
- Setting up cross-border data transfer mechanisms (SCCs, BCRs)
- Establishing a privacy program (policies, training, vendor assessments)
- Preparing for CCPA/CPRA compliance (California consumer rights)
- Evaluating data processors and sub-processors
- Designing privacy-by-design into product architecture

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Legal Basis Selection
```
                     ┌──────────────────────────┐
                     │ START: Which GDPR legal    │
                     │ basis for processing?      │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Processing necessary to     │
                    │ deliver contracted service? │
                    └────┬──────────────────┬───┘
                         │ YES              │ NO
                    ┌────▼──────┐    ┌──────▼──────────┐
                    │ Contractual│    │ Processing for   │
                    │ Necessity │    │ analytics,       │
                    │ (Art. 6    │    │ marketing, or    │
                    │ 1(b))     │    │ product improve? │
                    └───────────┘    └──┬──────────┬────┘
                                       │YES       │NO
                                  ┌────▼────┐ ┌───▼──────────┐
                                  │ Need to  │ │Public         │
                                  │ email    │ │interest or    │
                                  │ marketing│ │legal          │
                                  │ or set   │ │obligation?    │
                                  │ cookies? │ └──┬───────┬────┘
                                  └──┬───┬───┘    │YES   │NO
                                     │YES│NO   ┌──▼──┐ ┌─▼────────┐
                                ┌────▼──┐┌▼─────┐│Public│ │Vital     │
                                │Consent ││Legit. ││Interest│ │Interests│
                                │(Art.6  ││Interest││(Art.6 │ │(Art.6   │
                                │1(a))  ││+ LIA  ││1(e)) │ │1(d))    │
                                └───────┘└──────┘└──────┘ └─────────┘
```
**When to choose Contractual Necessity:** Processing essential to provide the paid service — storing user data to deliver their account, processing payment, shipping order. Cannot be used for analytics or marketing.
**When to choose Consent:** Email marketing, non-essential cookies, sensitive data — must be freely given, specific, informed, unambiguous, and withdrawable. Document proof.
**When to choose Legitimate Interest:** Analytics, product improvement, fraud prevention — must pass 3-part balancing test (LIA documented), user has right to object (Art. 21).

### DPIA Trigger Assessment
```
                     ┌──────────────────────────────┐
                     │ START: Is DPIA required?       │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Processing special category     │
                    │ data (health, biometrics,       │
                    │ political, religion, etc.)?     │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────┐    ┌──────────▼──────────┐
                    │ DPIA      │    │ Systematic automated │
                    │ REQUIRED  │    │ decision-making with │
                    │ (Art. 35  │    │ legal/significant    │
                    │ mandatory)│    │ effects (profiling,  │
                    └───────────┘    │ credit scoring)?     │
                                     └──┬──────────────┬────┘
                                        │YES          │NO
                                   ┌────▼────┐ ┌──────▼─────────┐
                                   │DPIA     │ │Large-scale     │
                                   │REQUIRED │ │processing of   │
                                   └─────────┘ │publicly        │
                                               │accessible data?│
                                               └──┬─────────┬────┘
                                                  │YES     │NO
                                             ┌────▼──┐ ┌──▼──────────┐
                                             │DPIA   │ │Likely not   │
                                             │REQUIRED│ │required —   │
                                             └────────┘ │assess      │
                                                        │residual     │
                                                        │risk (Art. 35│
                                                        │lists)       │
                                                        └────────────┘
```
**When DPIA is mandatory:** Special category data, automated decisions with significant effects, large-scale monitoring of public areas, systematic profiling, large-scale processing of criminal data.
**When DPIA may be needed:** New technology with high risk, processing vulnerable person data, combining datasets in unexpected ways. Check your DPA's Art. 35 list.
**When DPIA not required:** Low-risk processing, no special categories, small scale, no automated decisions. Document the decision not to do a DPIA.

### Data Breach Response
```
                     ┌──────────────────────────────┐
                     │ START: Data breach detected    │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Personal data breach likely to │
                    │ result in risk to individuals? │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Notify DPA    │    │ No notification  │
                    │ within 72 hrs │    │ required.        │
                    │ (Art. 33)     │    │ Document internal│
                    │               │    │ assessment +     │
                    │ Is risk HIGH? │    │ reasoning.       │
                    └──┬────────┬───┘    └─────────────────┘
                       │YES     │NO
                  ┌────▼───┐ ┌─▼──────────┐
                  │Notify  │ │DPA notified,│
                  │affected│ │no individual │
                  │data    │ │notification │
                  │subjects│ │required     │
                  │(Art.34)│ └─────────────┘
                  └────────┘
```
**When to notify DPA:** Any breach likely to cause risk to individuals (identity theft, financial loss, reputational damage, loss of confidentiality) — 72-hour clock, explain delay.
**When to notify individuals:** High risk to rights and freedoms — must be done without undue delay, clear and plain language, describe likely consequences, mitigation steps taken.
**When no notification needed:** Breach unlikely to result in risk (encrypted data, keys safe), or no personal data was actually exposed. Document reasoning thoroughly.

### International Transfer Safeguard Selection
```
                     ┌──────────────────────────────┐
                     │ START: Transferring personal   │
                     │ data outside EU/EEA?           │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Destination has EU adequacy     │
                    │ decision (currently: Andorra,   │
                    │ Argentina, Canada, Japan,       │
                    │ Korea, Switzerland, UK, etc.)?  │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Free transfer │    │ Transfer to US   │
                    │ — rely on     │    │ vendor?          │
                    │ adequacy      │    └──┬──────────┬────┘
                    │ decision      │       │YES       │NO
                    └───────────────┘  ┌────▼────┐ ┌───▼──────────┐
                                       │SCCs +   │ │ Intra-group? │
                                       │DPF cert │ └──┬───────┬────┘
                                       │(EU-US   │    │YES   │NO
                                       │DPF) +   │┌───▼──┐ ┌─▼──────────┐
                                       │TIA      ││BCRs  │ │SCCs + local│
                                       └─────────┘│      │ │law analysis│
                                                   └──────┘ └────────────┘
```
**When to rely on Adequacy Decision:** Transfer to EU-recognized adequate country — simplest path, no additional safeguards needed, but periodically verify status remains valid.
**When to use SCCs + DPF:** Transfer to US — EU-US Data Privacy Framework certification + Standard Contractual Clauses + Transfer Impact Assessment (TIA).
**When to use BCRs:** Intra-group transfers across multiple jurisdictions — Binding Corporate Rules approved by lead DPA, costly and slow to set up but durable.

### Cookie Consent Strategy
```
                     ┌──────────────────────────────┐
                     │ START: Cookie compliance       │
                     │ strategy?                      │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Do you use any non-essential    │
                    │ cookies (analytics, marketing,  │
                    │ social media, tracking)?        │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO (only essential)
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Must have     │    │ No consent       │
                    │ cookie banner │    │ required.        │
                    │ with:         │    │ Inform users     │
                    │ - Reject all  │    │ about essential  │
                    │   button      │    │ cookies in       │
                    │ - Granular    │    │ privacy policy.  │
                    │   controls    │    │ Still need cookie│
                    │ - Prior       │    │ notice per ePD.  │
                    │   consent     │    └─────────────────┘
                    │ - Withdrawal  │
                    │   mechanism   │
                    │ - Consent log │
                    └───────────────┘
```
**When full consent banner needed:** Any non-essential cookies — analytics (GA4 without consent mode), marketing pixels (Meta, LinkedIn), social widgets, advertising.
**When notice-only sufficient:** Only strictly necessary cookies (session, CSRF, load balancing, shopping cart) — no consent required but must inform users.
**When to use Consent Mode:** Google services (GA4, Ads) — signals consent state without cookies, enables modeled data for non-consenting users, reduces gap.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Data Mapping & Discovery

1. **Data inventory**: Catalog ALL personal data collected — what, why, where stored, who accesses, retention period
2. **Data flow diagrams**: Map data flows between systems, third parties, and jurisdictions
3. **Legal basis mapping**: For each data category, identify the lawful basis (consent, legitimate interest, contract, legal obligation)
4. **Cross-border transfer assessment**: Identify data flows crossing EU/adequate country borders
5. **Processor inventory**: List all third-party data processors and sub-processors with DPA status

### Phase 2 (~30 min): Gap Analysis & Remediation

1. **Consent mechanism audit**: Is consent freely given, specific, informed, unambiguous? Granular opt-in with equal prominence for accept/decline?
2. **Privacy notice review**: Does the privacy policy meet transparency requirements (Art. 13-14 GDPR)?
3. **Data subject rights workflow**: Can you handle access, rectification, erasure, portability, objection requests within legal timelines (30 days)?
4. **Data retention audit**: Are retention periods defined and enforced? Is data deleted/anonymized after purpose fulfillment?
5. **Security measures**: Appropriate technical and organizational measures (encryption, pseudonymization, access controls)

### Phase 3 (~20 min): Implementation & Documentation

1. **Cookie consent banner**: IAB TCF 2.2 framework, prior consent model, granular per-purpose controls
2. **Consent management platform (CMP)**: Cookiebot, OneTrust, or CookieYes deployment
3. **DSAR portal**: Self-service DSAR form, identity verification, secure response delivery
4. **Privacy policy updates**: Layered notice, plain language, specific disclosures per CCPA categories
5. **DPIA templates**: Systematic description, necessity/proportionality assessment, risk assessment, mitigation measures
6. **Data Processing Agreements (DPAs)**: Signed with all processors, SCCs incorporated

### Phase 4 (~15 min): Ongoing Compliance & Monitoring

1. **Annual privacy review**: Re-assess data inventory, processor list, privacy notices
2. **Privacy training**: Role-based (engineering: privacy-by-design, marketing: consent rules, support: DSAR handling)
3. **Incident response**: 72-hour breach notification workflow under Art. 33-34 GDPR
4. **Vendor assessment**: Standardized privacy review for new vendors/tools
5. **Regulatory monitoring**: Track new regulations (EU AI Act, Digital Services Act, state-level US privacy laws)

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Privacy compliance is everyone's responsibility — not just legal. Engineering, product, security, and marketing decisions create the data flows that determine compliance.

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **CTO Advisor** | Data architecture, encryption, data minimization | Data flow diagrams, encryption standards, pseudonymization implementation |
| **Security Reviewer / CISO** | Breach response, security measures, access controls | Incident response plan, technical measures adequacy, vulnerability impact on PII |
| **Legal Advisor** | Privacy policy, DPAs, regulatory interpretation | Policy language, contract terms, legal basis assessment |
| **Regulatory Specialist** | Industry-specific privacy (HIPAA, COPPA, GLBA) | Overlapping regulatory frameworks, sectoral privacy requirements |
| **Product Strategist** | Feature design, data collection purpose limitation | Purpose specification, data minimization in product requirements |
| **All Frontend Developers** | Cookie consent implementation, data collection forms | Consent banner technical spec, granular opt-in/opt-out, consent logging |
| **All Backend Developers** | Data storage, retention, deletion, DSAR automation | Retention logic, automated deletion jobs, DSAR data extraction APIs |
| **UX Designer** | Consent UX, privacy settings, preference centers | Consent must be as easy to withdraw as to give; dark patterns prohibited |
| **Growth Engineer** | A/B tests involving personal data, analytics tracking | Lawful basis for experimentation data, consent scope, data subject rights during tests |
| **Marketing** | Email marketing, analytics, cookie usage on landing pages | Consent requirements for marketing, legitimate interest boundaries, unsubscribe mechanisms |
| **DevOps/Infrastructure** | Cross-border data storage, data residency, backups | Data location controls, SCCs for cloud providers, backup retention alignment |
| **Data/Analytics** | Event tracking taxonomy, PII in analytics, data warehouse governance | PII classification of events, pseudonymization, analytics data retention |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Personal data breach (confirmed or suspected) | CTO Advisor, Security Reviewer, Legal Advisor, CEO Strategist | 72-hour supervisory authority notification clock starts immediately |
| New vendor/tool proposed that processes personal data | Legal Advisor, Security Reviewer | DPA required before data sharing; vendor privacy assessment needed |
| Data subject access request (DSAR) received | Legal Advisor, Engineering Lead (backend) | 30-day response deadline; data extraction from all systems required |
| New product feature collecting new category of personal data | Product Strategist, Legal Advisor, CTO Advisor | DPIA trigger; lawful basis must be established pre-launch |
| Cross-border data transfer to non-adequate country planned | Legal Advisor, CTO Advisor, DevOps | SCCs required; transfer impact assessment needed |
| Cookie consent mechanism change (new CMP, update to banner) | UX Designer, Frontend Dev, Marketing | IAB TCF compliance; consent logging continuity |
| Regulatory inquiry or complaint from DPA | Legal Advisor, CEO Strategist | Privileged response strategy; potential enforcement action |
| Data retention period reached — automated deletion about to execute | CTO Advisor, Backend Dev, Data/Analytics | Verify no legal hold or legitimate purpose overrides deletion |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Supervisory authority (DPA) investigation or enforcement action | **External Privacy Counsel** + CEO Strategist + Legal Advisor | Privileged, specialized defense; potential fines up to 4% global revenue |
| Large-scale data breach affecting >1,000 data subjects | **External Breach Counsel** + CISO + CEO Strategist + PR/Comms | Multi-jurisdiction notification; regulatory + reputational crisis |
| DPIA identifies high residual risk that cannot be mitigated | **Supervisory Authority** (prior consultation) + Legal Advisor | Art. 36 GDPR obligation; regulator may prohibit processing |
| EU representative or DPO identifies systematic non-compliance | **Board/Audit Committee** + CEO Strategist | Governance failure; personal liability risk for executives |
| Cross-border transfer mechanism invalidated (e.g., Privacy Shield successor struck down) | **External Privacy Counsel** + CTO Advisor + Legal Advisor | All international data flows may need restructuring |

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
Minimal viable compliance. Privacy policy: free template (Termly/Iubenda). Cookie consent: CookieYes free plan (<25K pageviews). DSAR: manual email template. No DPO, no DPIA, no ROPA, no vendor assessments. If no EU users, block EU traffic. Key: have a privacy policy, basic cookie notice, and know your data flows. Cost: $0-50/month. Overkill: OneTrust, automated DSAR portal, BCRs, external privacy counsel retainer, ISO 27701.

### Small (2-10 people, 100-10K users)
Fractional DPO (2-4 hours/month) or privacy counsel retainer. Cookie consent: Cookiebot or OneTrust ($50-300/month). DSAR: automated portal (Mine PrivacyOps free tier). DPIA for any high-risk processing. Signed DPAs with all vendors processing personal data. ROPA maintained (Google Sheets at minimum). Privacy training for all staff. Cost: $500-3K/month. Overkill: dedicated in-house DPO, enterprise privacy management platform, BCRs.

### Medium (10-50 people, 10K-1M users)
In-house privacy lead or fractional DPO (10+ hours/week). OneTrust/TrustArc privacy platform. Automated data discovery and classification. Privacy by design integrated into SDLC (DPIA template, review gates). Comprehensive vendor risk assessments. ISO 27001 or SOC 2 for security foundation. Regular privacy training with completion tracking. Incident response plan tested annually. Cost: $5K-20K/month. Overkill: full ISO 27701 certification, AI governance program unless AI is core product.

### Enterprise (50+ people, 1M+ users)
In-house DPO + privacy team (2-5). OneTrust Enterprise / BigID. Automated data mapping, DSAR processing, vendor assessments. ISO 27701 certification (PIMS). Binding Corporate Rules for cross-border transfers. AI governance program (EU AI Act ready). Dedicated privacy engineering function: PETs, data minimization at architecture level. Board-level privacy reporting. Regulatory engagement strategy. Cost: $50K-500K+/month.

### Transition Triggers
| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | >5 DSARs/month, >20 vendors processing personal data, or first DPIA required | Hire fractional DPO; implement automated DSAR portal; execute DPAs with all vendors |
| Small → Medium | >20 DSARs/month, >50 vendors, or launched in 3+ EU markets | Purchase privacy management platform; hire privacy lead; integrate privacy into SDLC |
| Medium → Enterprise | 1M+ data subjects, regulatory investigation, or M&A activity | Hire in-house DPO team; pursue ISO 27701; implement BCRs; add AI governance |


### Cross-skills Integration
```mermaid
graph LR
    A[legal-advisor] --> B[gdpr-privacy]
    B --> C[compliance-officer]
    D[product-manager] --> B
    B --> E[security-engineer]
```
Run skills in the order shown:
```bash
# Chain A: legal-advisor → gdpr-privacy → compliance-officer
# Chain B: product-manager → gdpr-privacy → security-engineer
```

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| **Consent Management** | Non-essential cookies, marketing emails, or processing sensitive data | CookieYes, Cookiebot, OneTrust — CMP with granular controls, consent logs, withdrawal mechanism |
| **DSAR (Data Subject Access Requests)** | Individuals requesting access, deletion, or portability of their data | Mine PrivacyOps, DataGrail — identity verification, automated data collection, 30-day response window |
| **DPIA (Data Protection Impact Assessment)** | High-risk processing: special category data, profiling, new technology, large-scale monitoring | ICO/CNIL templates, OneTrust — systematic risk assessment, mitigation measures, Art. 35 consultation triggers |
| **International Data Transfers** | Transferring personal data outside EU/EEA, especially to US | SCCs, UK Addendum, EU-US DPF certification, Transfer Impact Assessment (TIA), BCRs |
| **Vendor/Processor Assessment** | Evaluating third-party data processors and sub-processors | DPAs, OneTrust Vendorpedia, Whistic — security review, Schrems II compliance, annual re-assessment |
| **Breach Response** | Security incident involving personal data | 72-hour notification clock, Art. 33 DPA notification, Art. 34 data subject notification, documentation |
| **ROPA (Record of Processing Activities)** | Art. 30 requires ROPA for organizations >250 employees or processing sensitive/risky data | Spreadsheet or privacy platform — controller and processor records, legal basis, retention periods, transfers |
| **Privacy by Design** | Embedding data protection into product architecture from the start | Data minimization, purpose limitation, PETs (differential privacy, pseudonymization), privacy impact assessment at design gates |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Data minimization is the best defense**: Don't collect what you don't need. Every field is a liability.
- **Privacy by design, not privacy by retrofit**: Build data protection into architecture, don't bolt it on after
- **Consent must be as easy to withdraw as to give**: One-click opt-out is a legal requirement, not UX polish
- **Document everything**: If it's not documented, it didn't happen. Regulators expect evidence.
- **Keep data inventory current**: Stale data maps are the #1 compliance gap found in audits
- **Train engineers, not just lawyers**: Engineering decisions create 80% of privacy risks
- **Legitimate interest is not a silver bullet**: Must pass the 3-part balancing test; document your LIAs
- **Cookie walls are not valid consent**: Cannot make service access conditional on accepting non-essential cookies

## MVP vs Growth vs Scale

| Phase | Team Size | Priority | Privacy Approach |
|-------|-----------|----------|-----------------|
| **MVP (0→1)** | 1-5 employees, no DPO | Avoid catastrophic fines. Ship lean. | Privacy policy from template (Termly/iubenda, $0-50). Cookie consent: CookieYes free plan. DSAR: manual email-based (1 request/month max). No DPIA, no ROPA, no vendor assessments. If no EU users, block EU traffic. |
| **Growth (1→10)** | 5-50 employees, fractional DPO or counsel | Systematic compliance program, audit-ready | Cookiebot or OneTrust ($50-300/mo). Automated DSAR portal. DPIA for high-risk processing. Signed DPAs with all vendors. ROPA maintained. Privacy training for all staff. |
| **Scale (10→N)** | 50+ employees, in-house DPO + privacy team | Enterprise privacy program, certifiable | OneTrust Enterprise ($1K-5K/mo). Automated data discovery and classification. Privacy by design integrated into SDLC. ISO 27701 certification (PIMS). Binding Corporate Rules for cross-border transfers. AI governance program (EU AI Act ready). |

## Cost-Effective Decision Table

| Decision | Free/Cheap Option | Paid Upgrade | When to Upgrade |
|----------|------------------|--------------|-----------------|
| Privacy policy | Termly generator (free) or Iubenda ($5.99/mo) | Law firm drafted ($3K-8K one-time) | Revenue >$100K or processing sensitive data at scale |
| Cookie consent | CookieYes (free, <25K pageviews/mo) | OneTrust ($100-500/mo) or Cookiebot ($12/mo) | >25K pageviews, need IAB TCF, or multi-domain |
| DSAR handling | Manual process (email template + identity verification) | Mine PrivacyOps (free tier) or DataGrail | >5 DSARs/month — automation pays for itself |
| DPIA template | ICO/CNIL free templates | Privacy management platform (OneTrust/TrustArc) | >3 DPIAs/year or need workflow approvals |
| Vendor assessments | Google Forms + manual review | OneTrust Vendorpedia or Whistic | >20 vendors or regulatory requirement |
| Privacy training | ICO free training materials + internal wiki | EverFi or MediaPro ($20-50/user) | >50 employees or need completion tracking for audit |
| Data mapping | Excel/Google Sheets | DataGrail, BigID, or OneTrust DataDiscovery | >50 data stores/systems — manual mapping breaks |

**Annual privacy budget by phase:** MVP: $0-500. Growth: $3K-15K (tools + fractional DPO). Scale: $100K-500K (DPO salary + enterprise tools + external counsel).

## Scalability Decision Tree

```
Are you processing EU personal data with >1K data subjects?
├── YES → GDPR applies. Privacy policy + cookie consent + DSAR process = minimum viable compliance.
│   └── Are you processing special category data (health, biometrics, political, etc.)?
│       ├── YES → DPIA REQUIRED before processing. Must have explicit consent or specific legal basis.
│       └── NO → Lawful basis documentation sufficient.
└── NO → Is your target market going to include EU in 12 months?
    ├── YES → Implement privacy-by-design now. Cheaper than retrofitting.
    └── NO → Basic privacy policy sufficient. Revisit if market expands.

Are you using 10+ third-party tools/SaaS that touch user data?
├── YES → Create vendor assessment process. DPA queue > 20 vendors = automation needed.
└── NO → Manual DPA management fine. Google Sheets tracking is sufficient until >20 vendors.

Are you receiving 5+ DSARs per month?
├── YES → Automate with DSAR portal. Manual handling costs ~2-4 hours/request.
└── NO → Manual email process fine. Template response + identity check.

Do you have a security incident response plan?
├── NO → This is priority #1. GDPR Art. 33 requires 72-hour notification.
│   Without a plan, you can't meet this. Write the plan BEFORE an incident.
└── YES → Test the plan annually with tabletop exercises.

Are you transferring data from EU → non-adequate countries (e.g., US)?
├── YES → SCCs required. Execute and document. Review annually (EDPB guidance evolves).
└── NO → No transfer mechanism needed. Document adequacy decision relied upon.
```


**What good looks like:** Data inventory complete and reviewed within 6 months. Lawful basis documented for every processing activity. Consent records include timestamps, version of consent presented, and audit trail. DPO appointed (if required). Data subject request process tested and documented.

## When NOT to Use This Skill (Overkill)

- **No EU users and no plans to launch in EU**: CCPA alone is simpler. GDPR is disproportionately complex for US-only businesses. Don't over-engineer.
- **B2B SaaS with <10 customers, all enterprise contracts handled by legal**: Your enterprise contracts cover data processing terms. Cookie consent on a marketing site with no logins is minimal.
- **Static website with no forms, no analytics, no cookies**: Privacy policy from a template stating "we collect nothing" is sufficient. Consent banners collect nothing — you're asking for consent to collect nothing.
- **Internal tool used by <5 employees with no customer data**: GDPR has a household exemption. Internal tools processing only employee data need basic transparency, not full compliance program.
- **You're pre-revenue and your product changes weekly**: Don't optimize consent flows for features that may not exist next month. Have a privacy policy. Add granular controls when features stabilize.
- **Sole proprietorship processing <100 records**: National small-business exemptions may apply. Check your member state's implementation. Tiered compliance exists for a reason.

## Token-Efficient Workflow

```
# Step 1: Privacy health check
python3 scripts/privacy_check.py --output json
# Returns: {
#   "has_privacy_policy": true, "policy_last_updated": "2024-01-15",
#   "has_cookie_consent": true, "consent_platform": "cookieyes",
#   "has_dpa_with_all_processors": false, "processors_without_dpa": 7,
#   "has_dsar_process": true, "dsar_last_30_days": 2,
#   "has_dpia_for_high_risk": false, "high_risk_activities": 2,
#   "has_ropa": false,
#   "has_data_retention_schedule": true,
#   "has_breach_response_plan": false,
#   "cross_border_transfers_to_non_adequate": true,
#   "sccs_executed": false
# }

# Step 2: Decision tree from JSON
# processors_without_dpa > 0 → Execute DPAs (highest legal risk)
# has_breach_response_plan == false → Write incident response plan
# has_dpia_for_high_risk == false AND high_risk_activities > 0 → Conduct DPIA
# has_ropa == false → Create ROPA (Art. 30 requires it for most businesses)

# Step 3: Quick verification
grep -l "data-protection\|privacy\|gdpr\|CCPA" policies/*.md | wc -l  # Policy coverage count
python3 scripts/check_cookie_banner.py --url https://example.com       # Exit 0 = compliant
python3 scripts/test_dsar_workflow.py                                  # Exit 0 = process works
```

**Principle:** `privacy_check.py` outputs a JSON compliance snapshot. Agent applies decision tree to rank actions by legal risk. No reading privacy policies into agent context (token waste). Cookie banner and DSAR checks use automated scripts returning exit codes.


### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Contract signed with unfavorable terms | Missing redline on key clauses | Never sign first draft. Redline: liability cap, indemnification, termination for convenience, IP ownership, data processing. |
| No BAA with HIPAA-covered vendor | Assumed vendor had one | Verify BAA before sharing any PHI. Retroactive BAA does not cover data already shared. |
| GDPR fine exposure | No data inventory or lawful basis documented | Document every data field, its purpose, lawful basis, retention period, and third-party sharing. |
| Open source license violation | Dependency used in proprietary product | Check license compatibility: GPL/AGPL is not compatible with proprietary distribution. Use only MIT/Apache 2.0/BSD in proprietary products. |
| Employee classification lawsuit | Contractor treated as employee | IRS 20-factor test. If contractor works exclusively, uses company equipment, and has set hours → they're an employee. |
| Privacy policy doesn't match app behavior | Policy written before features built | Policy must reflect actual data collection. Conduct pre-release audit: every permission request maps to a policy disclosure. |
| Jurisdiction conflict for international users | Terms only reference one country | Specify governing law AND dispute resolution. EU users need GDPR compliance regardless of where you're based. |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Data inventory document complete and reviewed within last 6 months
- [ ] **[S2]**  Lawful basis documented for every data processing activity
- [ ] **[S3]**  Privacy notice(s) updated, layered, and accessible from every page
- [ ] **[S4]**  Cookie consent banner deployed with prior consent, granular controls, and consent logging
- [ ] **[S5]**  DSAR workflow tested end-to-end with documented SLA compliance
- [ ] **[S6]**  Data Processing Agreements signed with all processors (including sub-processors)
- [ ] **[S7]**  DPIA completed for all high-risk processing activities
- [ ] **[S8]**  Data retention schedule defined and automated deletion/anonymization implemented
- [ ] **[S9]**  Cross-border transfer impact assessment completed with SCCs executed where required
- [ ] **[S10]**  Data breach response plan documented with 72-hour notification workflow
- [ ] **[S11]**  Privacy training completed by all employees (role-specific)
- [ ] **[S12]**  Vendor privacy assessment process defined and applied to all new tools
- [ ] **[S13]**  Records of processing activities (ROPA) maintained per Art. 30 GDPR
- [ ] **[S14]**  Annual compliance review scheduled with audit trail

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [GDPR Full Text](https://gdpr-info.eu/)
- [ICO Guide to GDPR](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/)
- [EDPB Guidelines](https://edpb.europa.eu/our-work-tools/general-guidance/gdpr-guidelines-recommendations-best-practices_en)
- [CCPA/CPRA Text](https://oag.ca.gov/privacy/ccpa)
- [IAB Transparency & Consent Framework (TCF) 2.2](https://iabeurope.eu/transparency-consent-framework/)
- [NOYB — European Center for Digital Rights](https://noyb.eu/)
- [CNIL Guidelines (France)](https://www.cnil.fr/en/home)
- [NIST Privacy Framework](https://www.nist.gov/privacy-framework)

---
## 3. Legal Basis Decision Framework


## 3. Legal Basis Decision Framework

Choosing the wrong legal basis is one of the most common GDPR violations and one of the hardest to fix retroactively (you cannot switch legal bases mid-stream without a new collection event). This framework walks through each legal basis, when to use it, and how to document it.

### 3.1 Consent (Art. 6(1)(a))

Consent is the most demanding legal basis and the most widely misunderstood.

**Valid consent checklist -- all must be YES:**

| Criterion | Test | Non-compliant example |
|---|---|---|
| **Freely given** | Can the data subject refuse without detriment? Is there a genuine choice? | To use our app, you must agree to marketing emails. (Bundling consent with service access = not freely given.) |
| **Specific** | Is consent granular per purpose? One consent per processing purpose. | A single checkbox: I agree to the Terms and Privacy Policy. (Bundling multiple purposes = not specific.) |
| **Informed** | Has the data subject been told: controller identity, purpose of each processing activity, types of data, right to withdraw, existence of automated decision-making, transfer to third countries and safeguards? | We use cookies to improve your experience. (Not specific enough about what data, which cookies, for what purposes.) |
| **Unambiguous** | Clear affirmative action. No pre-ticked boxes. Silence or inactivity is not consent. | A pre-ticked Sign me up for the newsletter checkbox. |
| **Withdrawable** | Must be as easy to withdraw as to give. At any time. No detriment for withdrawal. | Requiring a phone call to withdraw consent that was given by a single click. |
| **Named parties** | All controllers and processors relying on the consent must be named at the time of collection. | We and our partners -- which partners? What do they do with the data? |
| **Not conditional** | Consent cannot be a condition of service if the processing is not necessary for that service (Art. 7(4), bundling prohibition). | Accept all cookies or leave the site. (Cookie wall -- see Section 5 below.) |

**Consent record requirements (Art. 7(1)):** Must be able to demonstrate consent was given. Store: timestamp, consent text shown at the time, consent string/token, IP address, user agent, banner/notice version, purposes consented to, and withdrawal mechanism.

**When consent is the RIGHT choice:**
- Marketing communications (email, SMS, push notifications)
- Non-essential cookies and trackers (analytics, advertising, personalization)
- Processing special categories of data where no other Art. 9(2) basis applies
- Any processing that the data subject would not reasonably expect

**When consent is the WRONG choice:**
- Employment relationships (power imbalance -- consent is rarely freely given)
- Processing necessary to fulfill a contract (use Art. 6(1)(b) instead)
- Public authorities performing their tasks (use Art. 6(1)(e) instead)

### 3.2 Legitimate Interest (Art. 6(1)(f))

Legitimate interest is the most flexible legal basis -- but it requires a documented balancing exercise, and it is not available to public authorities performing their tasks.

**The Legitimate Interest Assessment (LIA) -- 3-Part Test:**

**Part 1: Purpose Test** -- Is there a legitimate interest?
- The interest must be lawful (not contrary to any law).
- The interest must be sufficiently specific. Commercial interest or business purposes is too vague. Examples of established legitimate interests: fraud prevention, direct marketing (to existing customers about similar products -- soft opt-in under ePrivacy), network and information security, intra-group administrative transfers, whistleblowing schemes (within limits).
- Document: What is the specific interest we are pursuing? Who benefits? How does this align with our business purpose as understood by data subjects?

**Part 2: Necessity Test** -- Is the processing necessary for that interest?
- Necessary means: is there a less intrusive way to achieve the same purpose? If you can achieve the same result with aggregated, anonymized, or pseudonymized data, the processing of personal data is not necessary.
- Document: Can we achieve this purpose without processing personal data? Can we achieve it with less data? Can we achieve it with less intrusive means? What alternatives did we consider and why were they rejected?

**Part 3: Balancing Test** -- Does the individual's interests override the legitimate interest?
- Consider: the nature of the data (is it sensitive? is it publicly available?), the reasonable expectations of the data subject (would they be surprised?), the status of the controller and data subject (is there a power imbalance? is the data subject a child?), the impact on the data subject (could this cause harm, distress, discrimination, loss of control?), the safeguards applied (pseudonymization, opt-out mechanisms, enhanced transparency).
- If the impact outweighs the interest, you cannot use legitimate interest.
- Document the balancing conclusion: The balancing test weighs in favor of [controller/data subject] because [reasoning]. Safeguards applied: [list].

**When legitimate interest is appropriate:**
- Fraud detection and prevention
- IT security monitoring (IDS/IPS, log analysis for threats)
- Direct marketing to existing customers about similar products (with opt-out -- this is the ePrivacy soft opt-in)
- Internal reporting and analytics using pseudonymized data
- Business continuity and disaster recovery (backups containing personal data)

**When legitimate interest is NOT appropriate:**
- Any processing where consent is required by ePrivacy (cookies, electronic marketing to non-customers)
- Processing special categories of data (Art. 9 provides its own exhaustive list of exceptions)
- Processing that would surprise or distress the data subject
- Processing children's data for marketing or profiling

### 3.3 Contract Necessity (Art. 6(1)(b))

This is the most narrowly interpreted legal basis. Necessary for the performance of a contract means: without this processing, the contract cannot be performed. Not helpful for business, not mentioned in the terms, but *strictly necessary*.

**The Contract Necessity Test:**
- Is the processing objectively necessary to deliver the core service the data subject has requested?
- Would the contract be impossible to perform without this processing?
- Is there a less intrusive way to perform the contract?

**Qualifies as contract necessity:**
- Processing a delivery address to ship a purchased item
- Processing payment information to charge for a subscription
- Processing an email address to send a password reset link
- Processing a username to display in a multiplayer game

**Does NOT qualify as contract necessity:**
- Using purchase history to recommend products (this is a separate purpose -- use legitimate interest with opt-out, or consent)
- Sharing email with marketing partners (separate purpose -- requires consent)
- Profiling user behavior to improve the service (this is not necessary to deliver the service the user signed up for -- use legitimate interest or consent)
- Sending promotional emails about service upgrades (marketing -- requires consent or soft opt-in)

**Critical distinction -- services vs. features:** Just because a feature is described in your terms does not make all associated data processing contractually necessary. The test is objective, not contractual. You cannot contract your way into a wider legal basis.

### 3.4 Legal Obligation (Art. 6(1)(c))

Processing that is necessary for compliance with a legal obligation to which the controller is subject.

**Must be:**
- A specific law (EU or Member State law) -- not a general government request or recommendation.
- The obligation must be mandatory, not optional.
- **Examples by industry:**
  - **Financial services:** AML/KYC under 4AMLD/5AMLD -- customer due diligence, transaction monitoring, suspicious activity reporting, record-keeping for 5 years post-relationship.
  - **Employment:** Tax withholding and social security reporting, workplace safety reporting, minimum wage compliance records.
  - **Healthcare:** Medical device adverse event reporting, clinical trial documentation (ICH GCP), prescription records.
  - **Telecommunications:** Data retention under national laws (subject to CJEU case law limitations -- see Tele2 Sverige, La Quadrature du Net).
  - **E-commerce:** Invoice retention (typically 6-10 years depending on Member State), VAT reporting.

### 3.5 Vital Interests (Art. 6(1)(d))

Narrowly limited to processing necessary to protect the vital interests of the data subject or another natural person -- life-or-death situations. Emergency medical treatment, disaster response, humanitarian emergencies. Cannot be used for routine processing. If another legal basis is available (e.g., consent in a medical context), use that instead.

### 3.6 Public Task (Art. 6(1)(e))

Only available to public authorities or private organizations performing a task in the public interest vested by law. Not applicable to most commercial organizations.

### 3.7 Decision Tree: Which Legal Basis?

```
START: Is the processing necessary to comply with a specific, mandatory law?
  |-- YES -> Use Legal Obligation (Art. 6(1)(c))
  |-- NO -> Is it strictly necessary to perform the contract with the data subject?
            |-- YES -> Use Contract Necessity (Art. 6(1)(b))
            |-- NO -> Is the data subject in a life-or-death situation?
                      |-- YES -> Use Vital Interests (Art. 6(1)(d))
                      |-- NO -> Is consent required by ePrivacy or for special category data?
                                |-- YES -> Use Consent (Art. 6(1)(a)) -- must meet all validity criteria
                                |-- NO -> Can you pass the LIA 3-part test?
                                          |-- YES -> Use Legitimate Interest (Art. 6(1)(f)) -- document the LIA
                                          |-- NO -> Use Consent (Art. 6(1)(a))
```

**Switching legal bases:** You cannot switch retroactively. If you collected data under consent and the data subject withdraws, you must stop processing -- you cannot pivot to legitimate interest. If you collected under legitimate interest and the data subject objects successfully, you must stop. Choose carefully at collection time and document your reasoning.

---
## 4. Data Subject Rights (DSAR)

GDPR provides 8 data subject rights. Implementing these at scale requires a centralized DSAR engine -- a request management system that orchestrates identity verification, data collection across all data stores, response assembly, and fulfillment tracking.

For a comprehensive DSAR implementation guide including technical architecture, deletion cascades, portability formats, exemption handling, and quarterly testing protocols, see `references/dsar-implementation-guide.md`.

### 4.1 The 8 Rights at a Glance

| Right | Art. | Summary |
|---|---|---|
| **Access** | 15 | Data subject can obtain confirmation of whether their data is processed, a copy of the data, and metadata (purposes, categories, recipients, retention, rights). |
| **Rectification** | 16 | Correct inaccurate data; complete incomplete data. |
| **Erasure (Right to be Forgotten)** | 17 | Delete data where: no longer necessary, consent withdrawn, objection upheld, unlawful processing, legal obligation. Subject to exemptions (freedom of expression, legal obligation, public health, archiving, legal claims). |
| **Restriction** | 18 | Limit processing while accuracy is contested, processing is unlawful, data is needed for legal claims, or objection is pending. |
| **Portability** | 20 | Receive data in structured, commonly used, machine-readable format (JSON, CSV, XML). Only applies to data provided by the data subject, processed by automated means, based on consent or contract. |
| **Objection** | 21 | Object to processing based on legitimate interest or public task. Absolute right to object to direct marketing. |
| **Automated decision-making** | 22 | Right not to be subject to decisions based solely on automated processing that produce legal or similarly significant effects. Exceptions: contract necessity, authorized by law, explicit consent. |
| **Notification obligation** | 19 | Controllers must communicate rectification, erasure, or restriction to each recipient unless impossible or disproportionate. |

### 4.2 30-Day Response Timeline

- **Clock starts:** Upon receipt of the request. Receipt means the request has been received by the designated DSAR channel and contains sufficient information to identify the data subject and the right being exercised.
- **Standard deadline:** 30 calendar days (not business days).
- **Extensions:** Up to an additional 60 days (total 90) for complex or numerous requests. Must inform the data subject within the first 30 days of the extension and the reasons.
- **ID verification tolling:** The clock pauses while you await identity verification. Start the clock only after identity is confirmed.
- **CCPA comparison:** CCPA allows 45 days (extendable to 90 with notice).

### 4.3 Identity Verification

Use a tiered approach based on the sensitivity of data requested:

| Tier | Risk Level | Methods | When to Use |
|---|---|---|---|
| **Basic** | Low | Email confirmation, logged-in session | Access request for non-sensitive data by authenticated user |
| **Medium** | Moderate | Government ID + selfie match, knowledge-based authentication | Account data including contact details, purchase history |
| **High** | High | Notarized document, in-person verification, multi-factor | Special category data, financial data, deletion requests |

**Critical principle:** Do not request more personal data for verification than necessary. If the data subject is already authenticated in your system, do not demand a passport scan for a simple access request.

### 4.4 Exemptions and Limitations

**Manifestly unfounded (Art. 12(5)):**
- The request is vexatious, harassing, or made in bad faith
- Examples: repetitive requests with no interval for data refresh, requests made to disrupt operations
- Response: refuse or charge a reasonable fee. Must demonstrate why it is manifestly unfounded.

**Excessive (Art. 12(5)):**
- The request overlaps with a recent previous request
- Response: charge a reasonable fee or refuse. The bar is higher than manifestly unfounded -- repetition alone may not qualify if sufficient time has passed.

**Adversely affecting others' rights (Art. 15(4)):**
- Access response cannot include personal data of third parties unless they consent or it is unreasonable to withhold
- Must redact third-party data or split files with joint data subjects

**Other exemptions:** Legal professional privilege, management forecasting, negotiation data, regulatory references, journalistic/academic/artistic purposes (Member State derogations).

### 4.5 Technical Architecture

A centralized DSAR engine should follow this architecture:

1. **Intake Layer:** Web form, email parser, API endpoint. Validates request completeness, creates case in tracking system.
2. **ID Verification Service:** Integrates with auth system, optionally with third-party IDV provider. Returns verified identity token.
3. **Data Store Connectors:** A plugin system -- one connector per data store (PostgreSQL, MongoDB, S3, Salesforce, Zendesk, Stripe, analytics warehouse). Each connector implements: `search(subject_id)`, `retrieve(record_ids)`, `delete(record_ids)`, `export(record_ids, format)`.
4. **Response Assembly Engine:** Aggregates results from all connectors, deduplicates, organizes by category, applies redactions, generates the response package.
5. **Deletion Orchestrator:** Coordinates cascading deletion across all stores. Tracks confirmation from each processor. Implements legal hold checks.
6. **Tracking Dashboard:** See the DSAR implementation guide for dashboard design.


---
## 5. Cookie Compliance

Cookie compliance sits at the intersection of the ePrivacy Directive (2002/58/EC, as amended by 2009/136/EC) and GDPR. The ePrivacy Directive (the lex specialis for electronic communications) requires consent for storing or accessing information on a user's terminal equipment, with a narrow exemption for strictly necessary cookies. GDPR then governs what you do with any personal data collected via those cookies.

### 5.1 ePrivacy Directive + GDPR Interplay

**The rule:** You must obtain prior consent before setting any cookie or tracker that is not strictly necessary (ePrivacy Art. 5(3)). GDPR then provides the standard for what valid consent looks like (freely given, specific, informed, unambiguous -- Art. 4(11) and Art. 7). This means cookie consent must meet ALL the GDPR consent validity criteria.

**Strictly necessary exemption** covers only:
- Session cookies for login state (but not persistent login cookies)
- Shopping cart cookies
- Load-balancing cookies
- Security cookies (CSRF tokens)
- Cookies remembering cookie preferences (ironically)

**The exemption does NOT cover:**
- Analytics cookies (even first-party) -- unless they are essential to providing the service explicitly requested by the user
- A/B testing cookies
- Personalization cookies
- Advertising/targeting cookies
- Social media tracking pixels

### 5.2 Consent Management Platform (CMP) Selection Criteria

When selecting a CMP (OneTrust, Cookiebot, Usercentrics, Cookie Information), evaluate:

| Criterion | Requirement |
|---|---|
| **IAB TCF v2.2 compliance** | Must support the Transparency & Consent Framework for programmatic advertising |
| **Granular consent** | Per-purpose and per-vendor toggles, not just accept all / reject all |
| **Prior blocking** | Must block cookies/scripts before consent -- not just fire and then honor withdrawal |
| **Consent logging** | Records timestamp, consent string, IP, user agent, banner version, purpose list, vendor list |
| **Consent refresh** | Configurable refresh interval (13 months max), re-prompt on material change |
| **Withdrawal mechanism** | Persistent floating button or link; as easy to withdraw as to give |
| **Multi-domain/language** | If you operate across domains and languages |
| **Accessibility** | WCAG 2.1 AA compliant consent interface |
| **API/Webhook** | Programmatic access to consent state for downstream systems |
| **GPC signal** | Honors Global Privacy Control browser signal as opt-out |

### 5.3 Cookie Categorization

| Category | Description | Examples | Consent Required? |
|---|---|---|---|
| **Strictly Necessary** | Essential for the website to function; requested service cannot be provided without them | Session cookies, CSRF tokens, load balancers, shopping cart, cookie preferences | No |
| **Performance / Analytics** | Collect information about how visitors use the site (page views, time on site, error messages) | Google Analytics, Mixpanel, Hotjar heatmaps | Yes |
| **Functional** | Enable enhanced functionality and personalization (remembering preferences, language selection) | Language preference, region selector, video player cookies | Yes |
| **Targeting / Advertising** | Track browsing across sites to build profiles and serve targeted ads | Facebook pixel, Google Ads, retargeting, programmatic ad cookies | Yes (explicit) |

### 5.4 Consent Logs

Per Art. 7(1) accountability, you must be able to demonstrate that consent was given. Log every consent event:

| Field | Example |
|---|---|
| **Consent ID** | `cons_abc123def456` |
| **Timestamp** | `2026-01-15T14:32:17Z` |
| **Consent string** | IAB TCF consent string (e.g., `CO4QHXgO4QHXg...`) |
| **IP address** | `203.0.113.42` (hashed after 30 days) |
| **User agent** | `Mozilla/5.0 ... Chrome/120.0` |
| **Banner version** | `v3.2.1` |
| **Purposes consented** | `[store_and_access_info, create_personalised_ads_profile, measure_ad_performance, ...]` |
| **Purposes rejected** | `[use_limited_data_to_select_content]` |
| **Vendors consented** | `[Google (755), Facebook (89), ...]` |
| **GPC signal honored** | `false` |
| **Consent scope** | Domain(s) covered by this consent |

Store consent logs in an append-only, immutable data store. Retain for the life of the processing plus the statute of limitations for legal claims (typically 3-7 years after the consent expires or is withdrawn).

### 5.5 Consent Refresh

- **Maximum validity:** 13 months from the date consent was given (per IAB TCF policy and advocated by several EU DPAs -- notably CNIL). After 13 months, re-prompt.
- **Material change triggers:** If you add a new purpose, new vendor, new data category, or change how data is used, you must re-obtain consent. The existing consent does not cover the new processing.
- **CNIL guidance:** Recommends 6-month consent validity for advertising cookies specifically.

### 5.6 Cookie Walls Prohibition

A cookie wall is a mechanism that conditions access to a website or service on the user's acceptance of all cookies. The EDPB has stated (Opinion 04/2012, confirmed in post-GDPR guidance) that cookie walls are not valid consent because consent is not freely given when access is conditional. If your only options are "Accept all cookies" or "Leave the site," you do not have valid consent.

**Compliant alternative:** Offer a genuine choice. If the user declines non-essential cookies, they still access the content. You may offer a cookie-free paid alternative (e.g., ad-free subscription), but the free service cannot be contingent on accepting tracking.

---
## 6. Data Protection Impact Assessments (DPIAs)

A DPIA is a process for identifying and minimizing the data protection risks of a project. It is a legal requirement (Art. 35) for processing that is likely to result in a high risk to individuals. The DPIA must be completed *before* the processing begins.

For a comprehensive DPIA template with all sections elaborated, risk matrix, and fillable indicators, see `references/dpia-template-detailed.md`.

### 6.1 When is a DPIA Required?

The EDPB (WP248) established 9 criteria. A DPIA is required if processing meets **2 or more** of these criteria:

1. **Evaluation or scoring** -- including profiling and predicting behavior (credit scoring, performance assessment)
2. **Automated decision-making with legal or similar significant effect** (hiring algorithms, loan decisions)
3. **Systematic monitoring** -- of publicly accessible areas (CCTV, location tracking in apps)
4. **Sensitive data or highly personal data** -- special categories, financial data, location data, communications data
5. **Data processed on a large scale** -- consider number of subjects, volume of data, duration, geographic extent
6. **Matching or combining datasets** -- from multiple sources in a way that exceeds reasonable expectations
7. **Data concerning vulnerable persons** -- children, employees, patients, asylum seekers, mentally ill persons
8. **Innovative use of technological or organizational solutions** -- AI, machine learning, IoT, biometric identification
9. **Preventing data subjects from exercising a right or using a service** -- deny-listing, fraud databases that block access

**Mandatory DPIA triggers (regardless of criteria count):**
- Systematic and extensive profiling with significant effects
- Large-scale processing of special categories of data or criminal conviction data
- Systematic large-scale monitoring of publicly accessible areas

**National DPA lists:** Many EU DPAs publish their own lists of processing activities that require a DPIA. Check your lead DPA's list. The UK ICO, for example, requires DPIAs for: innovative technology, denylisting, biometric/genetic data, data matching, invisible processing, tracking, targeting children, risk of physical harm.

### 6.2 DPIA Methodology

1. **Describe the processing:** What data? How collected? How stored? Who accesses? How long? What systems? Who are the data subjects? (See detailed template for structured questionnaire.)
2. **Assess necessity and proportionality:** For each purpose -- why is this processing necessary? Why can't less data achieve it? Why can't it be done with less intrusive means?
3. **Identify risks:** Using the WP29 risk criteria, enumerate risks to rights and freedoms. Each risk: describe the risk event, the potential impact, and the likelihood.
4. **Identify mitigation measures:** For each risk, specify the measure (technical or organizational) that reduces likelihood or impact.
5. **Assess residual risk:** After mitigation, is the risk low, medium, or high? If high, consultation with the DPA is required before processing.
6. **Document and sign off:** DPO review, stakeholder approvals, version control.
7. **Integrate into project plan:** DPIA outcomes feed into design decisions, not sit on a shelf.

### 6.3 Risk Assessment Matrix

Use a 5x5 likelihood x severity matrix:

| Likelihood \ Severity | 1 (Minimal) | 2 (Limited) | 3 (Significant) | 4 (Severe) | 5 (Maximum) |
|---|---|---|---|---|---|
| **5 (Almost Certain)** | Medium (5) | High (10) | Extreme (15) | Extreme (20) | Extreme (25) |
| **4 (Likely)** | Medium (4) | Medium (8) | High (12) | Extreme (16) | Extreme (20) |
| **3 (Possible)** | Low (3) | Medium (6) | High (9) | High (12) | Extreme (15) |
| **2 (Unlikely)** | Low (2) | Low (4) | Medium (6) | Medium (8) | High (10) |
| **1 (Rare)** | Low (1) | Low (2) | Low (3) | Medium (4) | Medium (5) |

**Risk acceptance thresholds:**
- Low (1-3): Acceptable, document monitoring plan
- Medium (4-6): Acceptable with ongoing monitoring, periodic review
- High (8-12): Requires additional mitigation; if residual risk remains high after mitigation, DPA consultation
- Extreme (15-25): Stop. Redesign. Processing cannot proceed without fundamental changes.

### 6.4 DPA Consultation (Art. 36)

If the DPIA indicates high residual risk and no mitigation can reduce it, you must consult the DPA before processing. The consultation must include: responsibilities of controller/processor, purposes and means of processing, measures and safeguards, DPO contact details, DPIA, and any other information the DPA requests. The DPA has 8 weeks (extendable to 14) to respond. Processing without consultation when required can result in fines and orders to suspend processing.

---
## 7. Data Breach Notification

### 7.1 The 72-Hour Rule (Art. 33)

**When the clock starts:** Upon becoming *aware* of a personal data breach. Awareness means having a reasonable degree of certainty that a breach has occurred -- not necessarily knowing all details, but enough to conclude that personal data may have been compromised.

**What triggers awareness:**
- An alert from your monitoring system
- A report from a processor
- A third-party notification (security researcher, customer)
- Discovery during internal audit or investigation

**What does NOT start the clock:**
- An unconfirmed rumor
- A vague anomaly that could have non-breach explanations
- A suspicion that requires investigation -- but the investigation must happen *immediately*

**The 72-hour timeline is absolute:** 72 hours from awareness, not 3 business days. If the 72nd hour falls on a weekend or holiday, the deadline does not extend. If you miss the window, you can still notify, but must provide reasons for the delay (Art. 33(1)).

**Internal escalation workflow:**
1. **Detection (0-2 hours):** Anyone who detects a potential breach reports to the incident response team via a dedicated channel (Slack, PagerDuty, email to security@).
2. **Triage (0-4 hours):** Incident response team assesses: is personal data involved? What categories? How many data subjects? What is the nature of the breach (confidentiality, integrity, availability)?
3. **Containment (0-4 hours):** Isolate affected systems, revoke compromised credentials, take affected services offline if necessary, preserve logs and forensic evidence.
4. **Risk assessment (4-24 hours):** Determine the risk to individuals. See risk assessment framework below.
5. **DPA notification (0-72 hours):** If risk exists, notify the supervisory authority.
6. **Data subject notification (without undue delay):** If high risk, notify affected individuals.
7. **Post-incident (<30 days):** Root cause analysis, remediation, update DPIA and security measures, tabletop exercise to test improvements.

### 7.2 Breach Risk Assessment

| Risk Level | Criteria | Action |
|---|---|---|
| **Low** | Encrypted data, no potential for harm, data already publicly available | No notification to DPA or data subjects required. Document in internal breach log. |
| **Medium** | Some potential for inconvenience or limited harm (e.g., exposed email addresses only) | Notify DPA within 72 hours. Data subject notification not required. |
| **High** | Identity theft risk, financial loss, special categories exposed, large data set, data can be linked with other data to cause harm | Notify DPA within 72 hours AND notify data subjects without undue delay. |

**Factors that increase risk:** Special categories of data, financial data, credentials (especially if reused), children's data, data volume, data subjects could be identified from the breach, data can enable identity theft or fraud, data can cause reputational harm, discrimination, or loss of confidentiality.

**Factors that decrease risk:** Strong encryption with intact keys, data that is already public, data that cannot be linked to identifiable individuals.

### 7.3 DPA Notification Content (Art. 33(3))

The notification to the supervisory authority must include:

1. Nature of the breach: categories and approximate number of data subjects, categories and approximate number of records
2. DPO contact details or other contact point
3. Likely consequences of the breach
4. Measures taken or proposed to address the breach, including mitigation of adverse effects

If all information is not available, provide it in phases without undue further delay.

### 7.4 Data Subject Notification Content (Art. 34)

When the breach is likely to result in high risk to rights and freedoms, communicate to data subjects without undue delay. The communication must:

1. Describe the nature of the breach in clear and plain language
2. Provide the DPO contact details or other contact point
3. Describe the likely consequences
4. Describe measures taken or proposed to address the breach
5. Describe steps the data subject can take to protect themselves (change passwords, monitor accounts, contact credit bureaus)

**No notification required if:**
- The data was encrypted with strong encryption (and keys were not compromised)
- The controller has taken subsequent measures ensuring high risk is no longer likely
- Notification would involve disproportionate effort (in which case, use a public communication)

### 7.5 Internal Breach Log

Per Art. 33(5), every breach must be documented regardless of whether notification was made. The log must include:

- Date and time of detection
- Date and time of awareness (when 72-hour clock started)
- Description of the breach (what happened, how, what data, how many subjects)
- Risk assessment outcome (low/medium/high) and justification
- Whether DPA was notified and when
- Whether data subjects were notified and when
- Containment and remediation measures
- Root cause
- Corrective actions to prevent recurrence
- Regulatory reference number (if assigned by DPA)

This log must be available for inspection by the supervisory authority.

### 7.6 Tabletop Exercise Format

Conduct at least annually. Format:

1. **Scenario injection:** Present a realistic breach scenario (e.g., S3 bucket misconfigured exposing 50,000 customer records; phishing attack on HR with employee data exfiltrated; rogue employee downloading customer database)
2. **Timed response:** Participants work through the escalation workflow against the clock. Facilitator tracks times.
3. **Decision points:** Force participants to make decisions: Is this notifiable? Who needs to be involved? What do we tell customers? Do we involve law enforcement?
4. **Hot wash:** Debrief immediately after. What worked? What did not? Where were the delays?
5. **After-action report:** Document findings, assign action items, set deadlines. Feed into updated incident response plan.


---
## 8. International Transfers

The GDPR restricts transfers of personal data to third countries (non-EEA) unless specific safeguards are in place. This became significantly more complex after the CJEU Schrems II ruling (July 2020), which invalidated the Privacy Shield and raised the bar for transfer assessments.

For a comprehensive international transfer compliance guide covering adequacy decisions, SCC module selection, Transfer Impact Assessments, BCRs, UK-specific requirements, and the Data Privacy Framework, see `references/international-transfer-guide.md`.

### 8.1 Transfer Identification

A transfer occurs when personal data is sent from the EEA to a third country or international organization (Art. 44). **Remote access from a third country constitutes a transfer** -- if an engineer in India accesses an EU-hosted database, that is a transfer. This makes transfers pervasive for any organization with global operations or remote workforce.

### 8.2 Transfer Safeguards Hierarchy

In order of preference:

1. **Adequacy decision** (Art. 45): The European Commission has determined the country provides an adequate level of protection. Current list includes: Andorra, Argentina, Canada (commercial), Faroe Islands, Guernsey, Israel, Isle of Man, Japan, Jersey, New Zealand, Republic of Korea, Switzerland, UK, Uruguay. **Note:** The US is NOT on the general adequacy list but has the Data Privacy Framework (see below).

2. **Appropriate safeguards** (Art. 46):
   - Standard Contractual Clauses (SCCs) -- 2021 version, the most common mechanism
   - Binding Corporate Rules (BCRs) -- for intra-group transfers
   - Approved codes of conduct (Art. 40) with binding commitments
   - Approved certification mechanisms (Art. 42) with binding commitments
   - Ad hoc contractual clauses authorized by DPA

3. **Data Privacy Framework (DPF):** For transfers to the US, organizations that self-certify under the EU-US DPF, UK Extension, or Swiss-US DPF provide adequate protection. Check the DPF list before relying on this.

4. **Derogations** (Art. 49): Narrow, exceptional situations -- consent (explicit), contract necessity, public interest, legal claims, vital interests, public register. These are NOT suitable for routine, repetitive transfers.

### 8.3 Standard Contractual Clauses (SCCs 2021)

The 2021 SCCs are modular. Choose the correct module(s):
- **Module 1:** Controller to Controller
- **Module 2:** Controller to Processor (most common for SaaS)
- **Module 3:** Processor to Sub-Processor
- **Module 4:** Processor to Controller

**Key obligations:**
- Complete Annex I (parties, description of transfer), Annex II (security measures), Annex III (sub-processors)
- Include the docking clause to allow additional parties to accede
- Conduct a Transfer Impact Assessment (TIA) before executing
- Implement supplementary measures if TIA identifies gaps

### 8.4 Transfer Impact Assessment (TIA)

Per EDPB Recommendations 01/2020, before transferring data under SCCs, you must assess:

1. The laws and practices of the destination country regarding government access to data
2. Whether those laws impinge on the effectiveness of the SCCs
3. Whether supplementary measures can address any gaps

**Specific risk factors for US transfers:**
- FISA Section 702 (surveillance of non-US persons)
- Executive Order 12333 (foreign intelligence gathering)
- Cloud Act (US law enforcement access to data held by US companies)
- Assess whether your data is of the type that might be subject to these authorities

**If gaps exist:** Implement supplementary measures -- encryption with keys held outside the destination country, pseudonymization with no re-identification capability in the destination country, or (if gaps cannot be closed) suspend transfers.

---
## 9. Data Protection Officer (DPO)

### 9.1 When a DPO is Required (Art. 37)

Mandatory if ANY of these apply:
- **Public authorities or bodies** (except courts in their judicial capacity)
- **Core activities consist of processing that requires regular and systematic monitoring of data subjects on a large scale** -- e.g., behavioral advertising, location tracking, health monitoring, CCTV networks
- **Core activities consist of large-scale processing of special categories of data (Art. 9) or criminal conviction data (Art. 10)** -- e.g., hospital processing patient data, insurance company processing health data, background check services

"Core activities" means the key operations necessary to achieve the organization's purpose -- not ancillary functions like payroll. If you are a marketing company, profiling for advertising is a core activity. If you are a furniture manufacturer, the marketing department's cookies are core to marketing but may or may not be core to the organization -- assess both.

**Even if not required:** Voluntary DPO appointment is considered a strong indicator of accountability. If you appoint a DPO, they have all the same protections and obligations as a mandatory DPO.

### 9.2 DPO Responsibilities (Art. 39)

- Inform and advise the controller/processor and employees of their data protection obligations
- Monitor compliance with GDPR and organizational data protection policies
- Advise on DPIAs and monitor their performance
- Cooperate with the supervisory authority
- Act as the contact point for the DPA on processing issues
- Take into account the risk associated with processing operations

### 9.3 Independence and Protections (Art. 38)

- The DPO cannot be dismissed or penalized for performing their tasks
- The DPO reports directly to the highest management level
- The DPO must have adequate resources to perform their tasks
- The DPO cannot receive instructions regarding the exercise of their tasks
- The DPO must not have a conflict of interest (cannot be the person who decides purposes and means of processing -- e.g., CEO, CTO, CMO typically cannot be DPO)
- Contact information must be published and communicated to the supervisory authority

### 9.4 DPO or Not -- Decision Matrix

| Factor | DPO Required? |
|---|---|
| Public authority | Yes, always |
| Core activity: large-scale regular monitoring | Yes |
| Core activity: large-scale special category data | Yes |
| None of the above, but process personal data | No (but recommended) |
| Fewer than 250 employees and occasional processing | No |

---
## 10. Privacy by Design

Privacy by design (Art. 25) requires that data protection be integrated into the processing activities and business practices from the design stage through the entire lifecycle. It is not a feature to add later -- it is a design constraint.

### 10.1 Data Minimization in Architecture

- Design schemas so that personal data and non-personal data are stored in separate, access-controlled tables/collections
- At the API layer, implement field-level access control -- never return more fields than the caller needs
- Use GraphQL or sparse field selectors (e.g., `?fields=id,name,email` in REST) to enforce minimization at read time
- Implement purpose-based access tokens: a service calling the user API for authentication receives only auth-relevant fields; a service calling for analytics receives only pseudonymized data
- Audit database schemas quarterly: any field without a documented purpose and legal basis is flagged for deletion

### 10.2 Pseudonymization Techniques

| Technique | What It Does | When to Use | Key Management |
|---|---|---|---|
| **Tokenization** | Replace identifier with a random token, store mapping in a secure vault | When you need to re-identify later (analytics linking, customer support) | Vault must be isolated with strict access control |
| **Hashing (salted)** | One-way transformation with salt -- cannot reverse, but can link records | Analytics, data warehousing -- when re-identification is not needed but consistency is | Salt must be stored separately, rotated periodically |
| **Encryption** | Reversible with key -- protects confidentiality while retaining utility | Data at rest, application-layer protection for sensitive fields | Key must be in a KMS (AWS KMS, HashiCorp Vault), not in the application code |
| **Aggregation** | Replace individual data with statistical summaries | Reporting, dashboards, public datasets | n/a (no key needed) |

**Critical distinction:** Pseudonymized data is still personal data under GDPR because re-identification is possible (you hold the key/mapping). Anonymized data (truly irreversible) is not personal data. Most organizations never achieve true anonymization -- be honest in your assessments.

### 10.3 Privacy Patterns

| Pattern | Description | Use Case |
|---|---|---|
| **k-anonymity** | Ensure each record is indistinguishable from at least k-1 other records in the dataset | Publishing datasets, analytics exports. Typical: k >= 5 for low-risk, k >= 20 for higher-risk. |
| **l-diversity** | Extension of k-anonymity: within each k-anonymous group, at least l distinct values for sensitive attributes | When k-anonymity alone can leak sensitive attribute values (e.g., all k records share same disease). Typical: l >= 2. |
| **Differential privacy** | Add calibrated noise to query results so the presence or absence of any individual record cannot be determined | Public-facing analytics, API responses with aggregate counts. Epsilon (privacy budget) controls the tradeoff. Typical: epsilon 0.1-1.0. |

### 10.4 Privacy-Enhancing Technologies (PETs)

| Technology | What It Does | Maturity | When to Use |
|---|---|---|---|
| **Homomorphic encryption** | Perform computations on encrypted data without decrypting | Emerging (high overhead) | Financial services, healthcare -- when you need to process data without seeing it |
| **Secure multi-party computation (SMPC)** | Multiple parties compute a function over their private inputs without revealing them | Emerging | Cross-organization analytics, fraud detection consortiums |
| **Zero-knowledge proofs (ZKP)** | Prove a statement is true without revealing the underlying data | Maturing | Age verification (prove age > 18 without revealing birthdate), identity verification |
| **Federated learning** | Train ML models across decentralized data without centralizing raw data | Maturing | Mobile keyboard prediction, healthcare model training across hospitals |

**Implementation guidance for PETs:** These are specialist tools. Do not deploy them without expert input. The error mode for a misconfigured PET is that you think data is private but it is not -- far worse than knowing you have a compliance gap.

---
## 11. CCPA/CPRA Comparison

The California Consumer Privacy Act (CCPA, as amended by the California Privacy Rights Act -- CPRA) is the closest US equivalent to GDPR. Understanding the differences is essential for any organization processing both EU and California resident data.

### 11.1 Applicability Thresholds

An organization must comply with CCPA/CPRA if it does business in California AND meets any ONE of:
- Annual gross revenue exceeds $25 million (globally)
- Buys, sells, or shares personal information of 100,000 or more consumers or households
- Derives 50% or more of annual revenue from selling or sharing consumers' personal information

**Comparison:** GDPR applies to any organization that processes personal data of individuals in the EEA, regardless of revenue or scale (subject to the household exemption for purely personal activities).

### 11.2 Consumer Rights Under CCPA/CPRA

| Right | Description | GDPR Equivalent |
|---|---|---|
| **Right to Know** | Request disclosure of categories and specific pieces of personal information collected, sources, purposes, and third parties shared with | Right of Access (Art. 15) |
| **Right to Delete** | Request deletion of personal information, subject to exceptions | Right to Erasure (Art. 17) |
| **Right to Correct** | Request correction of inaccurate personal information (added by CPRA) | Right to Rectification (Art. 16) |
| **Right to Opt-Out of Sale/Sharing** | Direct businesses to stop selling or sharing personal information for cross-context behavioral advertising | Right to Object (Art. 21) -- but CCPA is opt-OUT, GDPR is opt-IN for some processing |
| **Right to Limit Use of Sensitive PI** | Limit use of sensitive personal information to what is necessary to perform the service (added by CPRA) | Special categories under Art. 9 with explicit consent |
| **Right to Non-Discrimination** | Businesses cannot discriminate against consumers who exercise CCPA rights | No explicit equivalent, but fairness principle (Art. 5(1)(a)) covers this |

### 11.3 Key Differences from GDPR

| Dimension | GDPR | CCPA/CPRA |
|---|---|---|
| **Default consent model** | Opt-in for most processing (consent as legal basis) | Opt-out for sale/sharing (business can process until consumer opts out) |
| **Personal information definition** | Any information relating to an identified or identifiable natural person | Broader: includes household data, inferences drawn from personal information |
| **Sensitive data** | Special categories of personal data (Art. 9) with heightened protections | Sensitive personal information subcategory (SSN, precise geolocation, race, religion, health, biometrics, etc.) with right to limit use |
| **Enforcement** | Supervisory authorities, administrative fines up to 4% global annual turnover or EUR20M | California AG and California Privacy Protection Agency (CPPA); administrative fines; private right of action ONLY for data breaches (not for other violations) |
| **DPO requirement** | Required in specific circumstances | No DPO requirement, but businesses must provide methods for submitting requests |
| **DPIA requirement** | Required for high-risk processing (Art. 35) | Cybersecurity audit and risk assessment required for processing presenting significant risk (CPRA) |
| **Data retention** | Storage limitation principle (Art. 5(1)(e)) | No explicit storage limitation, but must inform consumers of retention period at collection |
| **Cross-border transfers** | Extensive restrictions with adequacy decisions, SCCs, etc. | No cross-border transfer restrictions (US federal system) |

### 11.4 Operational Impact

For organizations subject to both:
- **Do not build parallel systems.** A single DSAR engine that handles both GDPR and CCPA request types, with jurisdiction logic to apply the correct rules (timeline, verification standard, data scope).
- **Unify consent management.** Your CMP should handle GDPR (opt-in, granular) and CCPA (opt-out link, GPC signal) with jurisdiction detection.
- **Privacy notices can be unified** but must clearly differentiate rights available to different jurisdictions.
- **Data mapping is the common foundation** -- both regimes require you to know what data you have and where it lives.

---
## 12. Monitoring & Maintenance

Compliance is not a one-time project. Build these recurring processes:

### 12.1 Consent Audit

- **Quarterly:** Review a sample (10%) of consent records for completeness (all required fields present, consent valid at time of processing). Verify that consent withdrawal propagates to all downstream systems within 30 days.
- **Annually:** Full audit of consent architecture. Test the consent withdrawal flow end-to-end.
- **Consent refresh cadence:** 13-month maximum. Schedule automated re-consent prompts 30 days before expiration.

### 12.2 Data Retention Schedule Enforcement

- **Automated purging scripts:** Cron/scheduled jobs that query for records past retention period. Must run at least monthly.
- **Deletion logs:** Retain evidence of every deletion run -- what was deleted, when, by which job.
- **Legal hold override:** Mechanism to suspend automated deletion. Each hold must have: case identifier, scope (which records), start date, expiry/review date, legal owner.
- **Quarterly verification:** Spot-check 50-100 records across different data categories to confirm deletion has occurred.

### 12.3 Vendor Compliance

- **Annual review:** For every processor -- reconfirm contract currency, SCC version, sub-processor list, security certification status (SOC 2, ISO 27001), and DPA terms.
- **Sub-processor notifications:** When a processor adds a new sub-processor, assess within 30 days. If you object and the processor cannot accommodate, you may need to terminate.
- **Onboarding checklist:** Before sending data to any new vendor -- DPA executed, SCCs attached (if non-EEA), TIA completed, vendor risk tier assigned, privacy team approval.

### 12.4 Privacy Impact Metrics

Track these KPIs monthly. Review quarterly with DPO and management:

| Metric | Target | Escalation Trigger |
|---|---|---|
| DSAR volume | Track trend | >2x normal monthly volume |
| DSAR response time | <30 days (100%) | Any response approaching day 25 |
| DSAR rejection rate | <15% | >20% in any quarter |
| Consent opt-in rate (marketing) | Track trend | <5% -- your consent UX may be coercive or confusing |
| Breach count (total) | 0 | Any breach triggers review |
| High-risk breaches | 0 | Any high-risk breach triggers full investigation |
| Employee training completion | 100% | <95% within 30 days of assignment |
| Vendor DPA currency | 100% | <100% triggers remediation plan |
| ROPA review currency | <12 months since last review per record | Any record >13 months stale |

---
## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S15]**  Records of Processing Activities (ROPA) are complete, accurate, and reviewed within the last 12 months
- [ ] **[S16]**  Legal basis documented for every processing activity with LIAs where legitimate interest is claimed
- [ ] **[S17]**  Consent Management Platform deployed, blocking non-essential cookies/trackers before consent
- [ ] **[S18]**  Consent logs maintain timestamp, consent string, IP, and banner version -- retrievable per user
- [ ] **[S19]**  Consent withdrawal mechanism tested and confirmed to propagate to all downstream systems
- [ ] **[S20]**  Do Not Sell or Share link and mechanism implemented and honoring GPC signal (CCPA/CPRA)
- [ ] **[S21]**  DSAR automation pipeline functional: access, portability, and deletion tested quarterly
- [ ] **[S22]**  DSAR response times tracked and within regulatory SLAs (30 days GDPR, 45 days CCPA)
- [ ] **[S23]**  Deletion cascade confirmed to reach all processors with confirmation tracking
- [ ] **[S24]**  DPIA template integrated into SDLC and completed for all high-risk processing activities
- [ ] **[S25]**  Standard Contractual Clauses (2021 version) executed with all non-EEA processors
- [ ] **[S26]**  Transfer Impact Assessments completed for all third-country transfers
- [ ] **[S27]**  Data breach response plan documented, tested via tabletop exercise within last 12 months
- [ ] **[S28]**  Breach notification templates prepared and ready for rapid deployment
- [ ] **[S29]**  Internal breach log maintained with all incidents regardless of notification obligation
- [ ] **[S30]**  Privacy policy accurately reflects all processing -- updated within last 12 months
- [ ] **[S31]**  Employee privacy training completed for all staff with access to personal data (annual)
- [ ] **[S32]**  Data retention schedule enforced -- automated purging of data past retention period
- [ ] **[S33]**  Legal hold process documented and accessible to legal team
- [ ] **[S34]**  DPO appointed or privacy responsibility formally assigned to a qualified individual
- [ ] **[S35]**  DPO contact information published and communicated to supervisory authority
- [ ] **[S36]**  Vendor DPA inventory current -- all processors have executed DPAs with SCCs where applicable
- [ ] **[S37]**  Vendor sub-processor list current and authorized
- [ ] **[S38]**  Privacy metrics dashboard live and reviewed quarterly
- [ ] **[S39]**  Annual compliance review completed and documented

---
## References
<!-- QUICK: 30s -- links to deeper reading -->
**Primary Legislation:**
- [GDPR Full Text -- EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [CCPA/CPRA -- California AG](https://oag.ca.gov/privacy/ccpa)
- [ePrivacy Directive 2002/58/EC](https://eur-lex.europa.eu/eli/dir/2002/58/oj)

**EDPB / WP29 Guidance:**
- [EDPB Guidelines 4/2019 -- Article 25: Data Protection by Design and by Default](https://edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-42019-article-25-data-protection-design-and_en)
- [EDPB Recommendations 01/2020 -- Supplementary Measures for International Transfers](https://edpb.europa.eu/our-work-tools/our-documents/recommendations/recommendations-012020-measures-supplement-transfer_en)
- [WP248 -- DPIA Guidelines](https://edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-data-protection-impact-assessment-dpia_en)
- [EDPB Guidelines 01/2022 -- Data Subject Rights: Right of Access](https://edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-012022-data-subject-rights-right-access_en)
- [EDPB Guidelines 05/2020 -- Consent](https://edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-052020-consent-under-regulation-2016679_en)

**International Transfers:**
- [European Commission -- Standard Contractual Clauses (SCCs)](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en)
- [Data Privacy Framework Program](https://www.dataprivacyframework.gov/)
- [UK ICO -- International Data Transfer Agreement (IDTA)](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/international-transfers/)

**Cookie Compliance:**
- [IAB Europe -- Transparency & Consent Framework (TCF)](https://iabeurope.eu/transparency-consent-framework/)
- [CNIL -- Cookies and Other Trackers Guidelines](https://www.cnil.fr/en/cookies-and-other-trackers)

**Regulatory Guidance:**
- [ICO -- Guide to the General Data Protection Regulation](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/)
- [EDPB -- Binding Corporate Rules](https://edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-22022-relevant-update-recommendations-12022_en)

**Tools:**
- [OneTrust -- Privacy Management Platform](https://www.onetrust.com/)
- [BigID -- Data Discovery and Intelligence](https://bigid.com/)

---
**Internal Reference Documents:**
- [DSAR Implementation Guide](references/dsar-implementation-guide.md)
- [DPIA Detailed Template](references/dpia-template-detailed.md)
- [International Transfer Compliance Guide](references/international-transfer-guide.md)
