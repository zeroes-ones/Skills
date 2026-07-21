---
name: gdpr-privacy
description: GDPR, CCPA, CPRA, and global privacy compliance specialist. Data protection impact assessments (DPIA), consent management platforms, data subject requests (DSAR), privacy by design, cookie compliance, cross-border data transfer mechanisms, and privacy program management.
author: Sandeep Kumar Penchala
---

# GDPR & Privacy Compliance Specialist

Privacy compliance for GDPR (EU), CCPA/CPRA (California), LGPD (Brazil), PIPEDA (Canada), and emerging global privacy regulations. Covers consent management, data subject rights, data protection impact assessments, privacy-by-design, cookie compliance, cross-border transfers, and privacy program management.

## When to Use

- Building products that collect/process EU resident personal data
- Implementing consent management (cookie banners, preference centers)
- Responding to Data Subject Access Requests (DSARs)
- Conducting Data Protection Impact Assessments (DPIA)
- Setting up cross-border data transfer mechanisms (SCCs, BCRs)
- Establishing a privacy program (policies, training, vendor assessments)
- Preparing for CCPA/CPRA compliance (California consumer rights)
- Evaluating data processors and sub-processors
- Designing privacy-by-design into product architecture

## Core Workflow

### Phase 1: Data Mapping & Discovery

1. **Data inventory**: Catalog ALL personal data collected — what, why, where stored, who accesses, retention period
2. **Data flow diagrams**: Map data flows between systems, third parties, and jurisdictions
3. **Legal basis mapping**: For each data category, identify the lawful basis (consent, legitimate interest, contract, legal obligation)
4. **Cross-border transfer assessment**: Identify data flows crossing EU/adequate country borders
5. **Processor inventory**: List all third-party data processors and sub-processors with DPA status

### Phase 2: Gap Analysis & Remediation

1. **Consent mechanism audit**: Is consent freely given, specific, informed, unambiguous? Granular opt-in with equal prominence for accept/decline?
2. **Privacy notice review**: Does the privacy policy meet transparency requirements (Art. 13-14 GDPR)?
3. **Data subject rights workflow**: Can you handle access, rectification, erasure, portability, objection requests within legal timelines (30 days)?
4. **Data retention audit**: Are retention periods defined and enforced? Is data deleted/anonymized after purpose fulfillment?
5. **Security measures**: Appropriate technical and organizational measures (encryption, pseudonymization, access controls)

### Phase 3: Implementation & Documentation

1. **Cookie consent banner**: IAB TCF 2.2 framework, prior consent model, granular per-purpose controls
2. **Consent management platform (CMP)**: Cookiebot, OneTrust, or CookieYes deployment
3. **DSAR portal**: Self-service DSAR form, identity verification, secure response delivery
4. **Privacy policy updates**: Layered notice, plain language, specific disclosures per CCPA categories
5. **DPIA templates**: Systematic description, necessity/proportionality assessment, risk assessment, mitigation measures
6. **Data Processing Agreements (DPAs)**: Signed with all processors, SCCs incorporated

### Phase 4: Ongoing Compliance & Monitoring

1. **Annual privacy review**: Re-assess data inventory, processor list, privacy notices
2. **Privacy training**: Role-based (engineering: privacy-by-design, marketing: consent rules, support: DSAR handling)
3. **Incident response**: 72-hour breach notification workflow under Art. 33-34 GDPR
4. **Vendor assessment**: Standardized privacy review for new vendors/tools
5. **Regulatory monitoring**: Track new regulations (EU AI Act, Digital Services Act, state-level US privacy laws)

## Cross-Skill Coordination

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

## Best Practices

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

## Production Checklist

- [ ] Data inventory document complete and reviewed within last 6 months
- [ ] Lawful basis documented for every data processing activity
- [ ] Privacy notice(s) updated, layered, and accessible from every page
- [ ] Cookie consent banner deployed with prior consent, granular controls, and consent logging
- [ ] DSAR workflow tested end-to-end with documented SLA compliance
- [ ] Data Processing Agreements signed with all processors (including sub-processors)
- [ ] DPIA completed for all high-risk processing activities
- [ ] Data retention schedule defined and automated deletion/anonymization implemented
- [ ] Cross-border transfer impact assessment completed with SCCs executed where required
- [ ] Data breach response plan documented with 72-hour notification workflow
- [ ] Privacy training completed by all employees (role-specific)
- [ ] Vendor privacy assessment process defined and applied to all new tools
- [ ] Records of processing activities (ROPA) maintained per Art. 30 GDPR
- [ ] Annual compliance review scheduled with audit trail

## References

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
