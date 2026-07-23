---
name: gdpr-privacy
description: >
  Use when implementing GDPR, CCPA/CPRA, or global privacy compliance programs,
  conducting data protection impact assessments (DPIAs), designing consent management,
  handling data subject requests (DSARs), or establishing cross-border data transfer
  mechanisms. Handles GDPR, CCPA, LGPD, and PIPEDA compliance frameworks,
  privacy-by-design implementation, cookie compliance, data protection impact
  assessments, consent management platforms, and privacy program management. Do NOT
  use for security engineering, compliance auditing for non-privacy frameworks
  (SOC 2, ISO 27001), or legal contract drafting.
license: MIT
allowed-tools: Read Grep Glob
tags:
- gdpr
- ccpa
- privacy
- dpia
- consent
- dsar
- data-protection
- compliance
author: Sandeep Kumar Penchala
type: legal
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 8000
chain:
  consumes_from:
  - compliance-officer
  - legal-advisor
  - privacy-engineer
  feeds_into:
  - compliance-officer
  - hipaa-technical-implementation
  - privacy-engineer
  - security-engineer
---

# GDPR & Privacy Compliance Specialist
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Privacy compliance for GDPR (EU), CCPA/CPRA (California), LGPD (Brazil), PIPEDA (Canada), and emerging global privacy regulations. Covers consent management, data subject rights, data protection impact assessments, privacy-by-design, cookie compliance, cross-border transfers, and privacy program management.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to cite specific GDPR articles without verification marker.** GDPR articles, recitals, and EDPB guidelines are amended and reinterpreted — article numbers may become stale | Trigger: response mentions "Art. [0-9]+" or "Article [0-9]+" without appending "Verify this citation is current — GDPR articles may have been updated or renumbered" | STOP. Append to response: "Verify this citation is current — GDPR articles and EDPB guidelines may have been updated or renumbered since this was written. Check [gdpr-info.eu](https://gdpr-info.eu/) for the current text." |
| **R2** | **REFUSE to answer without flagging jurisdiction.** EU GDPR, UK GDPR, Swiss DPA, CCPA/CPRA, VCDPA, CTDPA, LGPD, PIPEDA differ in scope, definitions, and enforcement | Trigger: response provides privacy guidance but `grep -c "jurisdiction\|applies under\|assuming.*law\|this answer assumes"` < 1 in the response | STOP. Prefix response: "This answer assumes [JURISDICTION]. If your processing involves users in [other jurisdictions], different rules apply. Confirm your applicable regulatory regime before proceeding." |
| **R3** | **REFUSE to declare an organization "compliant."** Compliance depends on the full data processing inventory — data flows, third-party processors, legal bases, retention schedules, and technical controls | Trigger: response contains "are compliant\|is compliant\|fully compliant\|GDPR.compliant\|CCPA.compliant" | STOP. Rephrase: "Based on the controls reviewed, [specific controls] align with [specific regulatory requirement] requirements. However, overall compliance cannot be determined without a complete data processing inventory including all data flows, third-party processors, and legal bases." |
| **R4** | **REFUSE to default to consent as the lawful basis.** GDPR provides six lawful bases — consent carries the highest burden (explicit, granular, withdrawable) and is not always required | Trigger: response recommends "get consent" or "add consent" without evaluating legitimate interest, contractual necessity, legal obligation, vital interests, or public task first | STOP. Respond: "Consent is only one of six lawful bases under Art. 6 GDPR and carries the highest compliance burden. Evaluate: (1) Is processing necessary for contract performance? (2) Is there a legal obligation? (3) Does legitimate interest apply (with LIA)? Only if none apply should consent be the basis." |
| **R5** | **STOP and ASK when local member state interpretation is needed.** Member state derogations, DPA enforcement priorities, and national implementations vary significantly | Trigger: question involves specific member state (e.g., "in Germany," "French DPA says," "under Spanish law") or national derogation under Art. 23, Art. 49, or national data protection acts | STOP. Ask: "This question involves member-state-specific interpretation. EU member states have national derogations and their DPAs have distinct enforcement priorities. I recommend consulting local data protection counsel in [MEMBER STATE]. May I proceed with the general EU GDPR framework analysis while noting where member state variations may apply?" |
| **R6** | **DETECT and WARN about cookie walls and non-compliant consent patterns.** Making service access conditional on accepting non-essential cookies is not valid consent — EDPB and multiple DPAs have confirmed this | Trigger: `grep -rn "cookie.wall\|accept.all.*required\|must.accept\|cannot.access.without" cookie-consent/ CMP-config/ privacy-center/` or user describes a consent flow where rejecting cookies blocks service access | WARN: "Cookie walls — making service access conditional on accepting non-essential cookies — are not valid consent under GDPR. Every cookie category beyond strictly necessary must have a separate, freely given opt-in. The 'Reject All' option must be as prominent as 'Accept All.' If your CMP doesn't support this, switch to a compliant provider." |
| **R7** | **DETECT and WARN about pre-GDPR consent being used for new processing purposes.** Consent obtained for one purpose cannot be repurposed; bundled consent is not valid; repurposing requires new consent or new lawful basis | Trigger: `grep -rn "consent.*20[0-1][0-9]" privacy-policy/ consent-records/` → consent dates before May 2018 (GDPR enforcement) or consent language references outdated purposes. Also: user mentions "we already have their consent" for new feature | WARN: "Pre-GDPR consent or consent from a different processing purpose is not valid for new processing under Art. 6(1)(a) and Art. 7. Consent must be specific, granular, and informed per purpose. Obtain fresh consent for each distinct processing purpose or establish a new lawful basis under Art. 6." |

## The Expert's Mindset

Master gdpr privacys understand that strategy is not about predicting the future — it's about **being less wrong than the competition, faster**.

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

## Route the Request

<!-- Machine-executable routing: 8 file_contains/file_exists rows A1-A8 + Intent Route fallback -->

| # | Detect Condition | Route To | Intent Route Fallback |
|---|-----------------|----------|----------------------|
| **A1** | `file_contains("privacy-policy*.md", "DPIA\|data.protection.impact")` or `file_exists("dpias/")` | Sub-Skills → DPIA | "I detect DPIA infrastructure — routing to Data Protection Impact Assessment workflow." |
| **A2** | `file_contains("cookie-consent/", "onetrust\|cookiebot\|cookieyes\|cmp")` or `file_contains("*.html", "cookie.banner\|cookie.consent")` | Sub-Skills → Consent Management | "I detect CMP/cookie consent integration — routing to Consent Management and Cookie Compliance." |
| **A3** | `file_exists("dsar/")` or `file_contains("privacy-policy*.md", "subject.access\|DSAR\|data.subject.right")` | Sub-Skills → DSAR | "I detect DSAR process artifacts — routing to Data Subject Access Request workflow." |
| **A4** | `file_contains("privacy-policy*.md", "cross.border\|international.transfer\|SCC\|standard.contractual")` or `file_exists("sccs/")` | Sub-Skills → International Data Transfers | "I detect cross-border transfer mechanisms — routing to International Data Transfers workflow." |
| **A5** | `file_exists("ropa/")` or `file_contains("privacy-policy*.md", "records.of.processing\|ROPA\|data.inventory")` | Core Workflow → Phase 1 (Privacy Program Assessment) | "I detect privacy program artifacts (ROPA/data inventory) — routing to Phase 1 for completeness assessment." |
| **A6** | `file_contains("*.md\|*.yml", "privacy.by.design\|PbD\|data.minimization\|privacy.engineering")` | Sub-Skills → Privacy by Design | "I detect privacy-by-design patterns — routing to Privacy by Design sub-skill." |
| **A7** | `file_exists(".github/workflows/privacy*.yml")` or `file_contains(".github/workflows/", "privacy.check\|cookie.scan\|dsar")` | Core Workflow → Phase 1 (Pipeline Verification) | "I detect automated privacy CI checks — routing to Phase 1 for pipeline coverage verification." |
| **A8** | `file_contains("README.md", "privacy\|GDPR\|CCPA\|data.protection")` or `file_exists("PRIVACY.md")` | Core Workflow → Phase 1 (Privacy Assessment) | "I detect privacy documentation — routing to Phase 1 for privacy program completeness assessment." |

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Initiative | Execute a defined strategic initiative with clear metrics |
| **L2** | Product line / function | Define strategy for a product line; own outcomes |
| **L3** | Business unit | Set multi-year strategy for a business unit; allocate resources across competing priorities |
| **L4** | Company | Define company-wide strategy; make existential trade-off decisions |
| **L5** | Industry | Shape industry dynamics; create new market categories |

**Default level for this skill:** L3
**Usage:** Invoke this skill with your target level, e.g., "as an L3 gdpr privacy, develop..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

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
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Data Mapping & Discovery

1. **Data inventory**: Catalog ALL personal data collected — what, why, where stored, who accesses, retention period
2. **Data flow diagrams**: Map data flows between systems, third parties, and jurisdictions
3. **Legal basis mapping**: For each data category, identify the lawful basis (consent, legitimate interest, contract, legal obligation)
4. **Cross-border transfer assessment**: Identify data flows crossing EU/adequate country borders
5. **Processor inventory**: List all third-party data processors and sub-processors with DPA status

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): Gap Analysis & Remediation

1. **Consent mechanism audit**: Is consent freely given, specific, informed, unambiguous? Granular opt-in with equal prominence for accept/decline?
2. **Privacy notice review**: Does the privacy policy meet transparency requirements (Art. 13-14 GDPR)?
3. **Data subject rights workflow**: Can you handle access, rectification, erasure, portability, objection requests within legal timelines (30 days)?
4. **Data retention audit**: Are retention periods defined and enforced? Is data deleted/anonymized after purpose fulfillment?
5. **Security measures**: Appropriate technical and organizational measures (encryption, pseudonymization, access controls)

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): Implementation & Documentation

1. **Cookie consent banner**: IAB TCF 2.2 framework, prior consent model, granular per-purpose controls
2. **Consent management platform (CMP)**: Cookiebot, OneTrust, or CookieYes deployment
3. **DSAR portal**: Self-service DSAR form, identity verification, secure response delivery
4. **Privacy policy updates**: Layered notice, plain language, specific disclosures per CCPA categories
5. **DPIA templates**: Systematic description, necessity/proportionality assessment, risk assessment, mitigation measures
6. **Data Processing Agreements (DPAs)**: Signed with all processors, SCCs incorporated

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): Ongoing Compliance & Monitoring

1. **Annual privacy review**: Re-assess data inventory, processor list, privacy notices
2. **Privacy training**: Role-based (engineering: privacy-by-design, marketing: consent rules, support: DSAR handling)
3. **Incident response**: 72-hour breach notification workflow under Art. 33-34 GDPR
4. **Vendor assessment**: Standardized privacy review for new vendors/tools
5. **Regulatory monitoring**: Track new regulations (EU AI Act, Digital Services Act, state-level US privacy laws)

## Cross-Skill Coordination

<!-- QUICK: 30s -- table of who to talk to when -->
Privacy compliance is everyone's responsibility — not just legal. Engineering, product, security, and marketing decisions create the data flows that determine compliance.

### Decision Gates & Artifacts

| Decision Gate | Trigger | Artifact / Deliverable |
|---------------|---------|------------------------|
| DPIA required | New processing of high-risk personal data (Art. 35 GDPR) | Data Protection Impact Assessment report |
| Consent mechanism valid | Cookie banner or preference center implemented | Consent audit log demonstrating freely given, specific, informed, unambiguous consent |
| Cross-border transfer lawful | Data leaving EEA to non-adequate country | Transfer Impact Assessment + signed Standard Contractual Clauses (SCCs) |
| Data subject request handleable | DSAR received from data subject | Identity verification + data extraction from all systems + response within 30 days |
| Breach notifiable | Personal data breach causing risk to individuals | Breach notification to supervisory authority (72 hours) + affected data subjects if high risk |
| Vendor passes privacy review | New vendor/tool processes personal data | Signed Data Processing Agreement (DPA) + vendor privacy assessment |

### Route to Other Skills

| Request Pattern | Route To | Why |
|-----------------|----------|-----|
| Draft/review privacy policy language or DPA terms | `legal-advisor` | Contract language, legal basis interpretation, enforceability |
| HIPAA, COPPA, GLBA, or healthcare-specific privacy | `regulatory-specialist` | Sector-specific privacy frameworks beyond general GDPR/CCPA |
| Security controls, encryption, access management | `security-engineer` | Technical safeguards for data protection (Art. 32 GDPR) |
| Enterprise privacy program governance, board reporting | `compliance-officer` | Program-level governance, audit readiness, regulatory filing coordination |
| Product feature data collection design | `privacy-engineer` | Privacy-by-design implementation, data minimization at architecture level |

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

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| New vendor/tool proposed that processes personal data | Block procurement until DPA signed and vendor privacy assessment completed; add to ROPA; notify Security Reviewer | Processing without DPA is an Art. 28 violation — the contract must exist before data flows, not after integration |
| Personal data breach suspected (laptop stolen, S3 bucket misconfigured, unauthorized access) | Start 72-hour Art. 33 clock; notify DPO within 2 hours; complete risk assessment within 24 hours; prepare DPA notification template | The clock starts at AWARENESS, not confirmation — without a pre-built notification workflow, every breach misses the deadline |
| New product feature collecting new category of personal data | Complete DPIA BEFORE processing begins; identify specific lawful basis; document necessity and proportionality; notify Product Strategist | Processing high-risk data without DPIA is the highest-fine GDPR violation — up to 4% of global annual turnover |
| Data subject access request (DSAR) received | Verify identity within 5 days; search all data stores within 10 days; assemble response; escalate if approaching day 20 of 30-day window | Manual DSAR across 12 systems will miss the deadline — automate before the first request arrives |
| Cross-border data transfer to non-adequate country planned | Execute SCCs (2021 version) before transfer; complete TIA; add transfer to ROPA; notify DPO; implement procurement gate for future transfers | Transfers happen in engineering, not legal — procurement must gate every cloud service and SaaS tool for data residency |
| Cookie consent CMP reports < 80% opt-in rate — users not freely consenting | Audit consent flow: reject-all button equal prominence, no pre-ticked boxes, no cookie wall; compare against EDPB guidelines; fix within 1 week | A CMP designed to maximize consent rather than enable free choice is a CNIL/DPA fine waiting to happen |
| Data retention schedule not enforced — records older than stated policy still in production | Implement automated deletion/anonymization based on retention policy; audit data stores quarterly; escalate to CTO Advisor | Retention violations are systematic — if you keep data longer than your own policy states, the policy is evidence against you |
| Privacy training completion rate drops below 90% across workforce | Escalate to HR and department heads; gate system access on training completion; track per-department compliance | Untrained employees create liability — regulators cite training gaps in every enforcement action; human error is the leading breach cause |

## What Good Looks Like

> When GDPR compliance is fully embedded, every data flow is mapped and lawful, consent mechanisms are transparent and granular, DSARs are fulfilled within 30 days with complete accuracy, DPIAs precede 

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.


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
- **7. Data Breach Notification**: See [breach-notification.md](references/breach-notification.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **11. CCPA/CPRA Comparison**: See [ccpa-cpra.md](references/ccpa-cpra.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **5. Cookie Compliance**: See [cookie-compliance.md](references/cookie-compliance.md)
- **Cost-Effective Decision Table**: See [cost-decisions.md](references/cost-decisions.md)
- **6. Data Protection Impact Assessments (DPIAs)**: See [dpia.md](references/dpia.md)
- **9. Data Protection Officer (DPO)**: See [dpo.md](references/dpo.md)
- **4. Data Subject Rights (DSAR)**: See [dsar.md](references/dsar.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **8. International Transfers**: See [international-transfers.md](references/international-transfers.md)
- **3. Legal Basis Decision Framework**: See [legal-basis.md](references/legal-basis.md)
- **3. Legal Basis Decision Framework**: See [legal-basis.md](references/legal-basis.md)
- **12. Monitoring & Maintenance**: See [monitoring-maintenance.md](references/monitoring-maintenance.md)
- **MVP vs Growth vs Scale**: See [mvp-growth-scale.md](references/mvp-growth-scale.md)
- **10. Privacy by Design**: See [privacy-by-design.md](references/privacy-by-design.md)
- **Scalability Decision Tree**: See [scalability-tree.md](references/scalability-tree.md)
- **Scale Depth**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)
- **Token-Efficient Workflow**: See [token-workflow.md](references/token-workflow.md)
- **When NOT to Use This Skill (Overkill)**: See [when-not-to-use.md](references/when-not-to-use.md)

