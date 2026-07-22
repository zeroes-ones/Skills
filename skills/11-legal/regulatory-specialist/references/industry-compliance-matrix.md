# Industry-Compliance Matrix

A comprehensive mapping of every major industry to its compliance requirements, regulations, and frameworks. Use this matrix to identify applicable regulations, understand scope, and prioritize compliance investments.

**All information is for guidance only — always verify with qualified legal and regulatory counsel.**

---
author: Sandeep Kumar Penchala
---

## Healthcare & Life Sciences

### HIPAA (Health Insurance Portability and Accountability Act) — United States

| Component | Scope | Key Requirements | Penalty for Non-Compliance |
|-----------|-------|-----------------|---------------------------|
| **Privacy Rule** | All PHI (Protected Health Information) in any form | Patient rights (access, amendment, accounting of disclosures), minimum necessary standard, Notice of Privacy Practices, authorization for marketing/sale of PHI | $127–$63,973 per violation; $127K–$1.92M/year tier |
| **Security Rule** | Electronic PHI (ePHI) only | Administrative safeguards (risk analysis, workforce training, contingency plan), physical safeguards (facility access, workstation security), technical safeguards (access control, audit controls, integrity controls, transmission security) | Same tiered civil penalties; criminal penalties up to $250K + 10 years imprisonment |
| **Breach Notification Rule** | Unsecured PHI breach | Notify affected individuals within 60 days; notify HHS within 60 days (<500 affected = annual log; >500 = immediate + media + OCR website); notify media if >500 in a state/jurisdiction | Per-violation penalties + reputational damage |
| **Omnibus Rule (2013)** | Business Associates | BAs directly liable for HIPAA violations; BAA mandatory; subcontractors of BAs also covered | Extends liability to BAs; Anthem BA breach = $16M settlement (2018) |
| **Enforcement** | OCR (HHS Office for Civil Rights) | Investigations triggered by breach reports, complaints, media reports, proactive audits | Anthem $16M (2018), Premera $6.85M (2020), CHSPSC $2.3M (2020) |

**Real fines:** Advocate Health Care $5.55M (2016, largest single-entity HIPAA settlement at the time); MD Anderson $4.3M (2018, encryption failures); Excellus Health Plan $5.1M (2021).

### HITECH Act — United States

- **Meaningful Use (now "Promoting Interoperability"):** EHR incentive programs; certified EHR technology required; interoperability and patient access standards
- **Breach notification expansion:** HITECH extended HIPAA breach notification to Business Associates directly
- **Enhanced enforcement:** State AGs empowered to bring civil actions; increased penalty tiers
- **Breach Notification:** <500 individuals = annual log to OCR; >500 = notification within 60 days + OCR website posting + prominent media notice
- **Willful neglect penalties:** Mandatory investigation + CMPs; no 30-day cure period

### FDA Regulations — Software as Medical Device (SaMD)

| Regulation/Guidance | Scope | Key Requirements | Time/Cost Estimate |
|--------------------|-------|-----------------|-------------------|
| **21 CFR Part 820 (QSR)** | Quality System Regulation for medical devices (transitioning to QMSR aligned with ISO 13485:2016) | Design controls (820.30), document controls (820.40), CAPA (820.100), production controls (820.70), complaint files (820.198) | QMS implementation: 12-24 months, $100K-$500K |
| **510(k) Premarket Notification** | Class II devices (moderate risk) | Prove substantial equivalence to predicate device; device description, intended use, technological characteristics, performance testing | $50K-$100K consulting; 3-6 months preparation; 90-day FDA review |
| **De Novo Classification** | Novel Class I/II devices without predicate | Risk-based classification; safety and effectiveness demonstration; special controls may be established | $80K-$150K; 150-day FDA review (goal) |
| **PMA (Premarket Approval)** | Class III devices (high risk, life-sustaining) | Clinical data required (IDE if US studies); manufacturing information; labeling; post-approval requirements | $2M-$10M+; 2-4 year timeline; 180-day FDA review |
| **IEC 62304** | Software lifecycle processes for medical device software | Safety classification (A/B/C); documentation per IEC 62304 Annex; software development plan, requirements, architecture, detailed design, unit testing, integration testing, system testing, release | Depends on safety class; Class C = full SDLC documentation |
| **ISO 14971** | Risk management for medical devices | Hazard identification, risk estimation (severity × probability), risk evaluation, risk control, residual risk, risk/benefit analysis, risk management report | Integrated into design controls; ongoing |
| **21 CFR Part 11** | Electronic records and electronic signatures | Validation, audit trails, authority checks, device checks, e-signatures (unique, non-reusable, two-component), system documentation | Part 11 gap assessment: $10K-$30K; remediation: $50K-$200K |

**GxP (Good Practice) framework:**
- **GCP** (Good Clinical Practice): Clinical trial conduct per ICH E6(R3); informed consent, IRB oversight, data integrity, monitoring, source data verification
- **GLP** (Good Laboratory Practice): Non-clinical lab studies per 21 CFR Part 58; SOPs, equipment calibration, QA unit, study director, raw data retention
- **GMP** (Good Manufacturing Practice): Manufacturing per 21 CFR Parts 210/211; Quality control, batch records, validation, deviation management, annual product reviews

### EU Medical Device Regulation (MDR 2017/745)

| Class | Risk Level | Examples | Conformity Route | Notified Body Required? | Clinical Evidence |
|-------|-----------|----------|-----------------|------------------------|-------------------|
| Class I | Lowest | Medical image storage, appointment reminder apps | Self-declaration per Annex II/III | No (except Class Is, Im, Ir) | Clinical evaluation report (CER); literature-based may suffice |
| Class IIa | Low-medium | Diagnostic software with clinician confirmation, blood pressure monitors | Annex IX (QMS) or Annex XI (production QA) + Annex II/III tech docs | Yes | CER; may include clinical investigation data |
| Class IIb | Medium-high | Radiotherapy planning software, insulin dose calculators | Annex IX + Annex X/XI | Yes | CER; clinical investigation typically required |
| Class III | Highest | Software that directly diagnoses/treats life-threatening conditions autonomously | Annex IX + Annex X/XI + Annex II/III | Yes | Clinical investigation mandatory |

**MDR Rule 11 (Software-specific):** Software intended to provide information for diagnostic/therapeutic decisions (Class IIa), that may cause serious deterioration (Class IIb), or death/irreversible deterioration (Class III).

**Key MDR requirements:**
- **GSPR (General Safety and Performance Requirements) — Annex I:** 23 requirements; cybersecurity for devices with electronic systems
- **Clinical Evaluation Report (CER):** Per MEDDEV 2.7/1 Rev.4; literature review, clinical investigation data, equivalence justification, risk/benefit, PMCF plan
- **Post-Market Surveillance (PMS):** PMS Plan, PMS Report (Class I) or PSUR (IIa+), PMCF
- **UDI (Unique Device Identification):** UDI-DI + UDI-PI; registered in EUDAMED
- **Person Responsible for Regulatory Compliance (PRRC):** Article 15; manufacturer must have at least one PRRC
- **Implant Cards:** Required for implantable devices

**Transition timelines:** MDR fully applicable from May 26, 2021; MDD certificates valid until max Dec 31, 2028 (per Regulation 2023/607 extensions); legacy devices can be placed on market until respective deadlines.

### NHS DSP Toolkit — United Kingdom

- **Purpose:** Data Security and Protection for health and care organizations
- **Scope:** All organizations with access to NHS patient data or systems
- **10 Data Security Standards:** Under 3 leadership obligations — people (staff training, responsibilities), process (risk assessment, incident response), technology (access controls, audit, continuity)
- **Assessment:** Annual self-assessment via online toolkit; published for transparency
- **Evidence items:** 150+ evidence assertions mapped to NDG (National Data Guardian) standards
- **Relation to GDPR:** Complements UK GDPR; toolkit evidences GDPR Article 32 security compliance

### Other Health Data Regulations — Global

| Regulation | Country | Scope | Key Points |
|-----------|---------|-------|------------|
| **PIPEDA (Health)** | Canada | Health information custodians in provinces without substantially similar laws (Ontario = PHIPA, BC = PIPA, Alberta = HIA, Quebec = Law 25) | Consent-based; provincial health laws may supersede |
| **My Health Records Act 2012** | Australia | My Health Record system | Opt-out model (since 2019); healthcare provider access; patient-controlled privacy settings |
| **HSPA (Health Insurance Portability)** | Japan | Anonymized medical data for research | Next-Generation Medical Infrastructure Act; certified data anonymization |
| **DiGAV/DiGA** | Germany | Digital health applications (apps on prescription) | BfArM listing; must prove positive care effects; provisional listing (1 year) then permanent (requires evidence); reimbursable by statutory insurance |
| **HITRUST CSF** | United States (private) | Certifiable security framework for healthcare | Maps to HIPAA, NIST, ISO, PCI; 19 domains, 156 controls; HITRUST r2 validated assessment required by many payers |

---

## Financial Services & FinTech

### PCI DSS 4.0 — Payment Card Industry Data Security Standard

| SAQ Type | Scope | Requirements | Typical Business |
|----------|-------|-------------|-----------------|
| **SAQ A** | Card-not-present merchants; fully outsourced payment processing (hosted payment page, iframe); no electronic storage/processing/transmission of cardholder data on merchant systems | ~22 requirements; eligibility criteria strict — NO merchant system touches card data in any form | E-commerce sites using Stripe Checkout, PayPal standard redirect |
| **SAQ A-EP** | E-commerce merchants partially outsourcing but with website elements that could affect payment page (e.g., embedded payment iframe) | ~191 requirements; includes requirements 6 (secure development), 7 (access control), 9 (physical security) | Sites using Stripe Elements, Braintree drop-in UI (JS on page) |
| **SAQ B** | Imprint-only or standalone terminal merchants (dial-out only, no internet) | ~41 requirements; standalone terminals only | Retail with standalone POS terminals |
| **SAQ B-IP** | Merchants with IP-connected PTS-approved payment terminals (no electronic cardholder data storage) | ~84 requirements; includes network segmentation, vulnerability management | Retail with IP-connected terminals |
| **SAQ C** | Payment application systems connected to internet (no electronic storage) | ~160 requirements; includes firewall, secure config, vulnerability management | Small merchants with POS systems |
| **SAQ C-VT** | Virtual terminal (web-based) merchants (manual entry, no electronic storage) | ~82 requirements; manually entered transactions only | Mail/telephone order businesses |
| **SAQ D (Merchant)** | All other merchants; any electronic storage of cardholder data | ~329 requirements; full PCI DSS scope | Merchants storing, processing, or transmitting cardholder data on their own systems |
| **SAQ D (Service Provider)** | Service providers who store/process/transmit cardholder data or could impact CDE security | ~329 requirements + service provider-specific additions; ROC (Report on Compliance) required, not just SAQ | Payment processors, gateways, hosting providers with access to cardholder environment |

**PCI DSS 4.0 key changes (effective March 2025):**
- Customized implementation approach (alternative to defined approach)
- Expanded multi-factor authentication (MFA) for all access into CDE (not just admin)
- Enhanced password requirements (min 12 characters, no group/shared accounts)
- Targeted risk analysis requirement for certain controls (flexibility with justification)
- Continuous monitoring replaces point-in-time validation mindset
- Service provider mandatory requirements increased (incident response testing, penetration testing frequency)

**Validation levels:**
- **Level 1:** >6M transactions/year → Annual ROC by QSA + quarterly ASV scans + penetration testing
- **Level 2:** 1M-6M transactions/year → SAQ or ROC (acquirer discretion) + quarterly ASV scans
- **Level 3:** 20K-1M e-commerce transactions/year → SAQ + quarterly ASV scans
- **Level 4:** <20K e-commerce or <1M total transactions/year → SAQ + ASV scans (acquirer discretion)

**Real fines & costs:** Target $18.5M settlement (2017, multistate AG); Equifax $575M+ FTC/CFPB/AG settlement (2019, though primarily non-PCI); Cost of breach for Level 1 merchant: avg $3-5M in forensic investigation, remediation, fines, and brand impact.

### SOX (Sarbanes-Oxley Act) — United States

| Section | Focus | IT Implications |
|---------|-------|----------------|
| **Section 302** | CEO/CFO certification of financial reports and internal controls | Executives must attest to effectiveness of disclosure controls and internal controls over financial reporting (ICFR) |
| **Section 404(a)** | Management assessment of internal controls | Management reports on effectiveness of ICFR; requires ITGC (IT General Controls) assessment |
| **Section 404(b)** | External auditor attestation | Independent auditor attests to management's ICFR assessment; accelerated/large accelerated filers only |
| **Section 409** | Real-time disclosure | Systems must support rapid material change disclosure (4 business days for 8-K) |
| **Section 802** | Criminal penalties for document destruction | Records retention policies; data cannot be destroyed when investigation is foreseeable |

**ITGC (IT General Controls) — the IT backbone of SOX compliance:**
1. **Access Control:** User provisioning/de-provisioning, access reviews (quarterly), SOD (separation of duties), privileged access monitoring, password policies
2. **Change Management:** SDLC controls, approval workflows, segregation of dev/test/prod, emergency change procedures, post-implementation review
3. **IT Operations:** Backup/recovery, job scheduling, incident management, capacity planning, monitoring/alerting
4. **Program Development:** SDLC methodology, testing, data migration, documentation standards

**Application Controls (automated controls within financial systems):**
- Input controls (validation, edit checks, authorization)
- Processing controls (matching, batch totals, sequence checks)
- Output controls (reconciliation, review, distribution)
- Interface controls (data transfer validation, reconciliation between systems)
- **Key reports:** IPE (Information Provided by Entity) — any report used in a control must be validated for completeness and accuracy

**SOD (Segregation of Duties) — critical conflict matrix:**
- Cannot: create vendor + approve vendor payments
- Cannot: enter journal entries + approve journal entries
- Cannot: set up users + process transactions
- Cannot: develop code + deploy to production
- Mitigating controls when SOD conflicts unavoidable: compensating controls (review, monitor, log) with documented evidence

**SOX compliance timeline for IPO:**
- Year 0 (filing): Materiality assessment, scoping, control design, walkthroughs
- Year 1 (post-IPO): Operating effectiveness testing begins; 404(a) management report (accelerated/large accelerated filers get 404(b) phased in)
- Year 2+: Full 404(b) external auditor attestation

### GLBA (Gramm-Leach-Bliley Act) — United States

| Rule | Scope | Requirements |
|------|-------|-------------|
| **Financial Privacy Rule** | All "financial institutions" (broadly defined — includes fintech, mortgage brokers, tax preparers, check cashers, payday lenders, even some auto dealers) | Initial privacy notice at account opening; annual privacy notice (unless exception applies); opt-out right for sharing with non-affiliated third parties; opt-out before sharing account numbers for marketing |
| **Safeguards Rule** | Financial institutions' customer information security | Designate coordinator; risk assessment; implement safeguards (access controls, encryption, MFA, audit trails, secure disposal, change management); monitor and test; service provider oversight; incident response |
| **FTC Safeguards Rule 2023 Amendments** | Enhanced security requirements | Mandatory encryption of customer info at rest and in transit; MFA for anyone accessing customer info; annual penetration testing; continuous monitoring; written incident response plan; board-level reporting (qualified individual must report to board) |
| **Pretexting Protection** | Protection against social engineering | Prevent unauthorized access to customer info via false pretenses; employee training on social engineering |

**Who is a "financial institution" under GLBA?** The FTC defines this broadly — any business "significantly engaged" in financial activities. Includes: fintech lenders, mortgage brokers, investment advisors, check cashers, payday lenders, debt collectors, tax preparers, real estate settlement services, and even auto dealers that lease/finance.

### PSD2/PSD3 — Payment Services Directive (EU)

| Component | PSD2 (2018) | PSD3 (proposed, expected ~2026) |
|-----------|------------|-------------------------------|
| **Open Banking** | ASPSPs must provide third-party access via APIs (no screen scraping) | Mandatory dedicated interfaces; improved API performance requirements; standardized API specifications |
| **SCA (Strong Customer Authentication)** | Two of three: knowledge (password/PIN), possession (device/token), inherence (biometric); exemptions: low-value (<€30), low-risk (TRA), trusted beneficiaries, recurring, corporate payments | Refined exemptions; mandatory SCA for certain high-risk transactions |
| **PISP (Payment Initiation Service Provider)** | Licensed to initiate payments on behalf of user; must identify to ASPSP; ASPSP must treat PISP-initiated payments same as direct | Enhanced liability framework for unauthorized transactions |
| **AISP (Account Information Service Provider)** | Licensed to access account data; must have consent; data access dashboard | Expanded data access scope; premium APIs |
| **IBAN discrimination** | Merchants must accept payments from any EU IBAN | Strengthened |

**SCA technical requirements per EBA RTS:**
- Transaction monitoring for fraud (real-time risk analysis = TRA exemption)
- Dynamic linking: authentication code must be specific to amount and payee
- Authentication code cannot be reused
- Inactivity timeout: max 5 minutes
- Block after 5 failed attempts (or max 5 within certain time)
- Secure communication between PSU, PSP, and PISP/AISP
- eIDAS certificates for PISP/AISP identification

### FINRA (Financial Industry Regulatory Authority) — United States

| Rule | Requirement |
|------|------------|
| **4511 (Books & Records)** | Electronic communications must be retained (3+ years, 2 years readily accessible); supervisory review of communications |
| **3110 (Supervisory System)** | Written supervisory procedures (WSPs); designated principals; annual testing/verification; heighten supervision for high-risk activities |
| **4370 (Business Continuity)** | BCP including data backup, mission-critical systems recovery, communication plan, alternate location; annual review and update |
| **Cybersecurity Guidelines** | Risk assessment; access management; vendor management; incident response; staff training; information sharing (FS-ISAC); penetration testing |
| **CAT (Consolidated Audit Trail)** | Requires reporting of all equity/options order events lifecycle: order origination, routing, modification, cancellation, execution, allocation; customer and account identifying info |

**Electronic Communications Retention:**
- Must capture: email, instant messaging, chat, SMS (if used for business), social media, collaboration tools (Slack, Teams)
- Retention: 3 years minimum; 2 years immediately accessible
- Supervisory review: documented, sampling methodology, evidence of review and escalation
- **JPMorgan fines:** $200M (2021) for failure to preserve staff communications on personal devices and WhatsApp — watershed enforcement moment

### MAS TRM (Technology Risk Management) — Singapore

- **Scope:** All financial institutions regulated by Monetary Authority of Singapore
- **Key requirements:** Technology risk governance (board/management oversight), IT outsourcing (cloud concentration risk, exit strategy), data center resilience (max 4-hour unscheduled downtime per incident), system resilience (penetration testing, resilience testing), cybersecurity (threat-led penetration testing, red teaming), access controls, cryptography
- **Notable:** MAS Notice 644 (cyber hygiene for all FIs) — MFA, system security patch management, network perimeter defense, anti-malware, baseline security standards
- **Cyber Incident Reporting:** Notify MAS within 1 hour of discovery of relevant IT incident; root cause analysis within 14 days

### FCA Handbook (Financial Conduct Authority) — United Kingdom

| Section | Focus | Key Points |
|---------|-------|------------|
| **SYSC (Senior Managers and Certification Regime)** | Individual accountability | Senior Managers: defined responsibilities, duty of responsibility; Certification Regime: annual fitness assessment; Conduct Rules: individual and senior manager tiers |
| **Operational Resilience** | March 2022 policy | Identify Important Business Services (IBSs); set impact tolerances (max tolerable disruption); map resources (people, tech, facilities, data, 3rd parties); scenario testing; lessons learned; board self-assessment |
| **Consumer Duty** | July 2023 | Cross-cutting rules (good faith, avoid foreseeable harm, support consumer pursuit of objectives); 4 outcomes (product governance, price/value, consumer understanding, consumer support) |
| **PRIN (Principles for Businesses)** | 11 principles | Integrity, skill/care, management/control, financial prudence, market conduct, customer interests, communications, conflicts, suitability, client assets, relations with regulators |

### Basel III/IV — Operational Risk Capital

- **SMA (Standardized Measurement Approach):** Replaces AMA (Advanced Measurement Approach); BIC (Business Indicator Component) × ILM (Internal Loss Multiplier)
- **Operational Risk categories:** Internal fraud, external fraud, employment practices, clients/products/business practices, damage to physical assets, business disruption/systems failures, execution/delivery/process management
- **Operational resilience overlay:** PRA (UK) SS1/21 — firms must demonstrate ability to remain within impact tolerance for IBSs during severe but plausible scenarios; link between operational risk and operational resilience

### AML/CFT (Anti-Money Laundering / Counter-Financing of Terrorism)

| Requirement | USBank Secrecy Act (BSA) | EU AMLD6 (6th AML Directive) | FATF Recommendations |
|-------------|--------------------------|------------------------------|----------------------|
| **KYC/CDD** | CIP (Customer Identification Program): name, DOB, address, ID number (verification within reasonable time); CDD (Customer Due Diligence) | Verify identity of customer and beneficial owner; ongoing monitoring; PEP screening | Recommendation 10: CDD for all customers |
| **EDD (Enhanced Due Diligence)** | Required for high-risk customers (PEPs, foreign banks, private banking, correspondent accounts); must understand source of funds/wealth | Enhanced for high-risk countries, complex/unusual transactions, PEPs | Recommendation 10.12: EDD for higher-risk categories |
| **SAR (Suspicious Activity Report)** | File within 30 days (60 if need to identify suspect); $5K threshold for insider abuse; confidentiality — cannot disclose SAR filing to subject | File STR (Suspicious Transaction Report) with national FIU (Financial Intelligence Unit) | Recommendation 20: Mandatory STR reporting |
| **CTR (Currency Transaction Report)** | Transactions >$10K in cash in one business day; multiple transactions by/for same person aggregated | N/A (EU equivalent varies by member state) | Recommendation 29: FIUs |
| **OFAC Sanctions** | SDN (Specially Designated Nationals) list; sectoral sanctions (SSI); screening required at onboarding, transaction, and ongoing | EU Consolidated Sanctions List; screening at same cadence | Recommendation 6: Targeted financial sanctions |
| **AML Program** | 5 pillars: internal controls, designated BSA officer, ongoing training, independent testing (annual), CDD/Risk-based procedures | Risk assessment, policies/procedures, MLRO appointment, training, audit | Recommendation 18: Internal controls |
| **Beneficial Ownership** | CTA (Corporate Transparency Act) — FinCEN BOI reporting; identify 25%+ beneficial owners; FinCEN CDD Rule | AMLD5 (5AMLD): UBO registers (public for companies, accessible for trusts with legitimate interest) | Recommendation 24: Transparency of beneficial ownership |

**AML fines — real world:**
- Goldman Sachs $2.9B (2020, 1MDB scandal)
- Danske Bank €2B+ (2018-2022, Estonia branch)
- Capital One $390M (2021, for willful BSA violations)
- USAA $140M (2022, BSA/AML program failures)
- Binance $4.3B (2023, BSA violations + OFAC sanctions)
- TD Bank $3.09B (2024, BSA/AML failures + record FinCEN penalty $1.8B)

### FinTech-Specific Compliance

| Area | Applicable Regulations | Startup Guidance |
|------|----------------------|-----------------|
| **BaaS (Banking-as-a-Service) / Sponsor Bank Model** | BSA/AML, GLBA, Reg E, UDAAP | Sponsor bank is primary regulator; fintech is service provider; examiner focus on fintech oversight, consumer protection, and compliance management system |
| **Crypto/Digital Assets** | BSA/AML (MSB registration with FinCEN if money transmitter), state money transmitter licenses (MTLs), SEC (if security — Howey test), CFTC (if commodity), IRS (tax treatment) | MSB registration required even for non-custodial? (FinCEN guidance evolving); MTLs: 53 jurisdictions × $100K-2M+ bonding; state-by-state compliance is largest operational burden |
| **Lending (Consumer)** | TILA/Reg Z, ECOA/Reg B, FCRA, FDCPA, state usury laws, state licensing | Rate exportation vs state-by-state licensing; "true lender" challenge; SCRA compliance; UDAAP |
| **BNPL (Buy Now, Pay Later)** | CFPB interpretive rule (2024): BNPL = "credit cards" under Reg Z; must provide billing dispute rights, refunds for returns, billing statements | CFPB enforcement priority; state-by-state scrutiny increasing |
| **InsurTech** | State-by-state insurance regulations; producer licensing; rate/form filing; surplus lines; reinsurance | 50-state compliance framework; navigating MGA vs carrier vs producer definitions; embedded insurance compliance |


## Technology & SaaS

### SOC 2 — System and Organization Controls

| Type | Scope | Report Content | Typical Timeline & Cost |
|------|-------|---------------|------------------------|
| **SOC 2 Type I** | Design of controls at a point in time | Description of system, management's assertion, service auditor's opinion on design suitability and implementation | 3-6 months; $15K-$50K |
| **SOC 2 Type II** | Operating effectiveness over a period (min 6 months, typically 12 months) | Type I content + detailed testing results (samples, exceptions), operating effectiveness opinion | 12-15 months (6 months observation + 3 months audit); $30K-$80K |

**Trust Services Criteria (TSC) — all 5 categories:**
1. **Security (Common Criteria — required):** Logical and physical access controls, system operations, change management, risk mitigation. CC1-CC9 series: COSO Principle mapping.
2. **Availability (optional):** System uptime, disaster recovery, business continuity, incident management.
3. **Confidentiality (optional):** Protection of confidential information per agreements/regulations; identification, classification, encryption, disposal.
4. **Processing Integrity (optional):** System processing is complete, valid, accurate, timely, and authorized; input/processing/output controls; error correction.
5. **Privacy (optional):** GAPP (Generally Accepted Privacy Principles): notice, choice/consent, collection, use/retention/disposal, access, disclosure, quality, monitoring/enforcement. Maps to GDPR/CCPA.

**SOC 2 Readiness Assessment:** Gap analysis against selected TSCs (typically 4-8 weeks, $10K-$30K). Key output: prioritized remediation plan before formal audit engagement.

**SOC 2 Bridge Letter:** Covers gap between SOC 2 report end date and current date; limited assurance; used when report is >12 months old.

**SOC 2 vs ISO 27001 vs FedRAMP:**
| Aspect | SOC 2 | ISO 27001 | FedRAMP |
|--------|-------|-----------|---------|
| Geography | Global (US-origin) | Global (EU-origin) | US Federal only |
| Certification | Attestation report (not a "certificate") | Certifiable (3-year cycle) | Authorization (ATO) |
| Auditor | CPA firm (AICPA-licensed) | ANAB-accredited CB | 3PAO (Third-Party Assessment Organization) |
| Control framework | TSC (5 categories) | Annex A (93 controls, 4 themes) | NIST SP 800-53 (1000+ controls) |
| Recertification | Annual report | Surveillance audits (years 1,2) + recertification (year 3) | Annual assessment + continuous monitoring |
| Recognition | Enterprise sales (required by most US enterprise RFPs) | International recognition; EU DPA preferred | Required to sell to US federal agencies |

### ISO 27001:2022 — Information Security Management System

**2022 version key changes (published Oct 2022, transition deadline Oct 2025):**
- Annex A restructured: 114 controls → 93 controls; 14 domains → 4 themes (Organizational, People, Physical, Technological)
- New controls (11): Threat intelligence (5.7), Information security for use of cloud services (5.23), ICT readiness for business continuity (5.29), Physical security monitoring (7.4), Configuration management (8.9), Information deletion (8.10), Data masking (8.11), Data leakage prevention (8.12), Monitoring activities (8.16), Web filtering (8.23), Secure coding (8.28)
- Merged controls: 56 controls consolidated into 24
- No new controls added without existing equivalent

**Certification process:**
1. **Gap Assessment** (4-8 weeks): Map current controls to Annex A; identify gaps
2. **ISMS Design** (8-16 weeks): Scope, policy framework, risk methodology, risk treatment plan, SoA (Statement of Applicability), procedures
3. **ISMS Implementation** (3-6 months): Operate controls, collect evidence, internal audit, management review
4. **Stage 1 Audit** (1-3 days): Documentation review; assess readiness for Stage 2
5. **Stage 2 Audit** (3-10 days): Verify implementation and effectiveness; non-conformities addressed
6. **Certification Decision** (2-8 weeks): Certificate issued (valid 3 years)
7. **Surveillance Audits** (Year 1, Year 2): Partial scope; verify ISMS maintenance
8. **Recertification Audit** (Year 3): Full scope recertification

**Cost estimate:** Stage 1: $5K-15K; Stage 2: $15K-40K; Surveillance: $8K-20K/year; Recertification: $12K-30K. Total 3-year cycle: $40K-85K (audit fees only; internal costs 2-4×).

**ISO 27001:2022 Annex A Themes:**

| Theme | Control Count | Key Controls |
|-------|--------------|--------------|
| **Organizational (5.1-5.37)** | 37 | Policies (5.1), asset management (5.9-5.14), classification (5.12), supplier security (5.19-5.22), cloud services (5.23), incident management (5.24-5.28), ICT readiness (5.29), legal/compliance (5.31-5.36) |
| **People (6.1-6.8)** | 8 | Screening (6.1), terms of employment (6.2), awareness & training (6.3), disciplinary (6.4), post-employment (6.5), confidentiality (6.6), remote work (6.7), reporting (6.8) |
| **Physical (7.1-7.14)** | 14 | Physical perimeters (7.1), entry (7.2), offices/rooms (7.3), monitoring (7.4), environmental threats (7.5), secure areas (7.6), clear desk/screen (7.7), equipment siting (7.8), off-premises assets (7.9), storage media (7.10), utilities (7.11), cabling (7.12), maintenance (7.13), secure disposal (7.14) |
| **Technological (8.1-8.34)** | 34 | Endpoint devices (8.1), privileged access (8.2), access control (8.3-8.5), authentication information (8.5), capacity management (8.6), malware (8.7), vulnerability management (8.8), configuration management (8.9), deletion (8.10), masking (8.11), DLP (8.12), backups (8.13), redundancy (8.14), logging (8.15), monitoring (8.16), clock sync (8.17), privileged utilities (8.18), install restrictions (8.19), network security (8.20-8.22), web filtering (8.23), cryptography (8.24), secure development (8.25-8.28), testing (8.29), outsourcing development (8.30), network segmentation (8.31), change management (8.32), test data (8.33), test environments (8.34) |

### ISO 27701:2019 — Privacy Information Management (PIMS)

- **Extension of ISO 27001/27002** for privacy management
- **PIMS-specific requirements:** Clause 5 (PIMS-specific requirements referencing ISO 27001), Clause 6 (PIMS-specific guidance referencing ISO 27002)
- **Roles:** PII Controller (Annex A/F — controls and guidance) vs PII Processor (Annex B/G)
- **Maps to:** GDPR (Articles 5, 12-22, 25, 28, 30, 32-36, 44-49), CCPA/CPRA, PIPEDA, LGPD
- **DPIA integration:** ISO 27701 operationalizes DPIA (clause 5.4)
- **DPO:** Requirements align with GDPR Article 37-39
- **Cross-border transfers:** PIMS-specific Annex C (controller) + Annex H (processor)
- **Certification:** Extension to ISO 27001 certification (not standalone); same CB, same cycle
- **Privacy notice:** PIMS-specific control for privacy notice transparency and content

### ISO 27017:2015 — Cloud Security

- **Guidelines for information security controls for cloud services** based on ISO 27002
- **Cloud-specific controls (7 additional):** Shared roles and responsibilities (CLD 6.3.1), monitoring cloud service activities (CLD 8.1.5), alignment of security management for virtual and physical networks (CLD 9.5.x), administrative operations of cloud service (CLD 12.1.5), cloud customer monitoring (CLD 12.4.5), virtual environment hardening (CLD 13.1.4)
- **Cloud roles:** Cloud Service Customer (CSC) vs Cloud Service Provider (CSP)
- **Shared responsibility:** Defines who owns which controls per service model (IaaS/PaaS/SaaS)

### ISO 27018:2019 — PII Protection in Public Cloud

- **Code of practice for protection of PII in public clouds acting as PII processors**
- **Key controls:** No use of PII for advertising/marketing without explicit consent; PII subject to data subject access rights; CSP must inform customer of subpoena/disclosure requests; PII disclosure to law enforcement only when legally required; data retention and disposal at end of contract; logging PII access by CSP staff
- **Aligns with:** GDPR, ISO 29100 (Privacy Framework)
- **Use case:** Public cloud providers handling customer PII (e.g., AWS, Azure, GCP compliance with this standard)

### FedRAMP — Federal Risk and Authorization Management Program

| Authorization Path | Who Authorizes | Scope | Process |
|-------------------|----------------|-------|---------|
| **Agency ATO** | Individual federal agency | Agency-specific use | CSP works with agency; agency's AO issues ATO; FedRAMP PMO reviews for reuse eligibility |
| **JAB (Joint Authorization Board) P-ATO** | JAB (DOD, DHS, GSA) | Government-wide | CSP applies to FedRAMP Connect; JAB prioritizes ~12/year; P-ATO enables agency-wide reuse |
| **Tailored** | Agency | Low Impact — SaaS (LI-SaaS) | 93 controls (vs 325+ for Moderate); self-attestation component; 3PAO assessment |

**Impact Levels (based on FIPS 199):**
- **Low:** Loss of CIA would have limited adverse effect; ~125 controls
- **Moderate:** Loss would have serious adverse effect; ~325 controls; majority of CSPs target this level
- **High:** Loss would have severe/catastrophic adverse effect; ~425 controls; for most sensitive unclassified data

**FedRAMP process (typical timeline: 6-18 months for Moderate):**
1. **FedRAMP Ready:** 3PAO readiness assessment; readiness assessment report (RAR) reviewed by PMO
2. **Full 3PAO Assessment:** Security Assessment Plan (SAP) → Security Assessment Report (SAR)
3. **Authorization:** AO reviews SAR + POA&M; issues ATO (agency) or P-ATO (JAB)
4. **Continuous Monitoring:** Monthly vulnerability scans, annual 3PAO assessment, POA&M management, significant change requests, annual security review

**Cost:** FedRAMP Ready: $50K-100K; Full assessment: $150K-400K; Continuous monitoring: $100K-250K/year. Total first year: $250K-750K+.

### CMMC 2.0 (Cybersecurity Maturity Model Certification)

| Level | Requirements | Assessment Type | Contract Eligibility |
|-------|-------------|----------------|---------------------|
| **Level 1 (Foundational)** | 15 controls (FAR 52.204-21) | Self-assessment; annual affirmation by senior official | FCI (Federal Contract Information); no CUI |
| **Level 2 (Advanced)** | 110 controls (NIST SP 800-171 Rev 2 + some from Rev 3) | Self-assessment for non-prioritized acquisitions; C3PAO assessment for prioritized | CUI (Controlled Unclassified Information) |
| **Level 3 (Expert)** | 110+ controls from NIST SP 800-172 | Government-led assessment (DIBCAC) | High-value CUI; APT (Advanced Persistent Threat) protection |

**Timeline:** CMMC 2.0 rule finalized October 2024; phased implementation beginning mid-2025; all DoD contracts will require CMMC certification by 2028.

### StateRAMP

- **Purpose:** StateRAMP is to state and local governments what FedRAMP is to federal
- **Impact Levels:** Level 1 (low), Level 2 (moderate — most common), Level 3 (high)
- **Statuses:** Ready, Provisional, Authorized (with continuous monitoring)
- **Participating states (growing):** Arizona, California, Colorado, Florida, Georgia, Michigan, New York, Texas, and more adopting StateRAMP verification requirements
- **Assessment:** 3PAO conducts assessment; StateRAMP PMO reviews; participating governments can use StateRAMP authorization in lieu of their own assessment

### FISMA (Federal Information Security Modernization Act)

- **Scope:** Federal agencies and contractors operating federal information systems
- **Key requirements:** Categorize systems (FIPS 199: low/moderate/high), implement NIST SP 800-53 controls, conduct annual security assessments, develop/maintain POA&M, continuous monitoring, annual FISMA report to OMB/Congress
- **Key NIST publications:**
  - NIST SP 800-53 Rev 5: Security and Privacy Controls (~1000+ controls across 20 families)
  - NIST SP 800-37 Rev 2: Risk Management Framework (RMF) — 7 steps: Prepare → Categorize → Select → Implement → Assess → Authorize → Monitor
  - NIST SP 800-30 Rev 1: Guide for Conducting Risk Assessments
  - NIST SP 800-171 Rev 2/3: Protecting CUI in Nonfederal Systems

### NIST CSF 2.0 (Cybersecurity Framework)

**Six Functions (Governance added in 2.0, February 2024):**

| Function | Core Activities | Key Categories |
|----------|---------------|----------------|
| **GOVERN (GV)** | Organization context; risk management strategy; roles/responsibilities; policies; oversight | GV.OC: Organizational Context; GV.RM: Risk Management Strategy; GV.RR: Roles/Responsibilities; GV.PO: Policies; GV.OV: Oversight; GV.SC: Supply Chain |
| **IDENTIFY (ID)** | Asset management; risk assessment; improvement | ID.AM: Asset Management; ID.RA: Risk Assessment; ID.IM: Improvement |
| **PROTECT (PR)** | Access control; awareness/training; data security; platform security; technology resilience | PR.AA: Identity/Authentication; PR.AT: Awareness/Training; PR.DS: Data Security; PR.PS: Platform Security; PR.IR: Technology Resilience |
| **DETECT (DE)** | Continuous monitoring; adverse event analysis | DE.CM: Continuous Monitoring; DE.AE: Adverse Event Analysis |
| **RESPOND (RS)** | Incident management; incident analysis; incident response reporting/mitigation | RS.MA: Incident Management; RS.AN: Incident Analysis; RS.CO: Reporting; RS.MI: Mitigation |
| **RECOVER (RC)** | Incident recovery plan execution; incident recovery communication | RC.RP: Recovery Plan Execution; RC.CO: Recovery Communication |

**Implementation Tiers:** Partial (Tier 1) → Risk-Informed (Tier 2) → Repeatable (Tier 3) → Adaptive (Tier 4)

**NIST CSF Profiles:** Current Profile vs Target Profile; gap analysis between them drives roadmap.

### CSA STAR (Cloud Security Alliance Security, Trust & Assurance Registry)

| Level | Type | Requirements |
|-------|------|-------------|
| **Level 1: Self-Assessment** | CAIQ (Consensus Assessments Initiative Questionnaire) | CSP completes CAIQ (300+ questions); published on CSA STAR Registry; no third-party validation |
| **Level 2: Certification** | CSA STAR Certification | Third-party audit (CSA-certified auditor); based on CCM (Cloud Controls Matrix) + ISO 27001; integrates with ISO 27001 certification |
| **Level 3: Continuous** | CSA STAR Continuous | Continuous monitoring of cloud security posture; automated evidence collection; STAR Watch (threat intelligence) |

**CCM v4:** 17 domains, 197 controls; maps to 50+ regulations/frameworks (ISO 27001, NIST SP 800-53, GDPR, PCI DSS, SOC 2, FedRAMP, HIPAA, C5, etc.).

### EU Cybersecurity Act & Certification Schemes

- **EUCC (EU Common Criteria):** Voluntary EU-wide cybersecurity certification for ICT products based on Common Criteria; assurance levels: Substantial (AVA_VAN.4) and High (AVA_VAN.5)
- **EUCS (EU Cloud Services):** Certification for cloud services (harmonizing national schemes like BSI C5 (Germany), SecNumCloud (France), ENS (Spain)); under development
- **EU5G:** 5G network cybersecurity certification in progress


## Privacy (Cross-Industry)

### GDPR — General Data Protection Regulation (EU/EEA)

**Data Subject Rights (Chapter 3, Articles 12-23):**

| Right | Article | Description | Response Timeline |
|-------|---------|-------------|-------------------|
| Right to be informed | 13-14 | Transparent info about processing at collection | At point of collection (Art 13) / within 1 month (Art 14) |
| Right of access | 15 | Confirmation of processing + copy of personal data + processing details | 1 month (extendable 2 months) |
| Right to rectification | 16 | Correct inaccurate personal data; complete incomplete data | 1 month |
| Right to erasure ("right to be forgotten") | 17 | Erase personal data where no overriding lawful basis | 1 month |
| Right to restriction of processing | 18 | Restrict processing while verification of accuracy, lawfulness, or objection | 1 month |
| Right to data portability | 20 | Receive data in structured/machine-readable format; transmit to another controller | 1 month |
| Right to object | 21 | Object to processing based on legitimate interest, public interest, direct marketing (absolute right for marketing) | At point of first communication (marketing); at any time thereafter |
| Rights re automated decision-making & profiling | 22 | Not subject to decisions based solely on automated processing with legal/significant effects | Subject access + human intervention right |

**DPIA Triggers (Article 35 — mandatory when processing is "likely to result in high risk"):**
1. Systematic and extensive profiling with significant effects
2. Large-scale processing of special categories of data (Article 9) or criminal conviction data (Article 10)
3. Systematic monitoring of publicly accessible areas on a large scale
4. **New technologies** — any processing involving new technologies where risk is uncertain
5. Processing that would prevent data subjects from exercising a right or using a service/contract
6. **EDPB/DPA lists:** Each DPA publishes its own list of processing requiring DPIA (e.g., ICO list: 12 criteria; CNIL: 8 categories; German DSK: blacklist + whitelist)

**DPO Requirements (Articles 37-39):**
- **Mandatory when:** (a) processing by public authority/body (except courts); (b) core activities consist of regular and systematic large-scale monitoring; (c) core activities consist of large-scale processing of special categories or criminal conviction data
- **Group DPO:** Single DPO for group of undertakings
- **DPO requirements:** Expert knowledge of data protection law and practices; independence; direct report to highest management; no conflict of interest; contactable by data subjects and DPAs
- **DPO duties:** Inform/advise, monitor compliance, advise on DPIA, cooperate with DPA, act as DPA contact point

**Cross-Border Transfer Mechanisms (Chapter 5, Articles 44-50):**

| Mechanism | Legal Basis | When to Use | Requirements |
|-----------|------------|-------------|-------------|
| Adequacy Decision (Art 45) | EU Commission decision that country ensures adequate level of protection | Transfer to: Andorra, Argentina, Canada (commercial), Faroe Islands, Guernsey, Israel, Isle of Man, Japan, Jersey, New Zealand, Republic of Korea, Switzerland, UK, Uruguay, US (DPF certified entities only) | Confirm recipient is within adequacy scope (e.g., DPF requires certification to specific framework) |
| Standard Contractual Clauses — SCCs (Art 46(2)(c)) | EC-approved model contract clauses | Most common mechanism for controller-processor and controller-controller transfers | Execute SCCs (2021 version); conduct TIA (Transfer Impact Assessment); implement supplementary measures if needed |
| Binding Corporate Rules — BCRs (Art 47) | DPA-approved intra-group rules | Multinational corporate groups for intra-group transfers | Apply to lead DPA; demonstrate BCRs are legally binding; 12-18 month approval process; 80+ BCRs approved EU-wide |
| Codes of Conduct / Certifications (Art 46(2)(e)/(f)) | DPA-approved codes or certification mechanisms | Emerging mechanisms | Currently limited uptake; GDPR certification under development per Art 42 |
| Derogations (Art 49) | Specific situations (not for repetitive transfers) | One-off/occasional transfers only: explicit consent, contract necessity, important public interest, legal claims, vital interests | Cannot be used for routine/structural transfers; DPA guidance: narrow interpretation |

**Schrems II Ruling (C-311/18, July 2020):**
- Invalidated Privacy Shield (predecessor to DPF) as adequacy mechanism for US transfers
- Upheld SCCs but required case-by-case assessment: "supplementary measures" required where SCCs alone insufficient
- Key concern: US surveillance laws (FISA Section 702, EO 12333) allow disproportionate government access to EU data
- **Transfer Impact Assessment (TIA)** now required: assess (1) SCCs executed? (2) local laws of destination country? (3) can SCCs be honored in practice? (4) supplementary measures implemented?

**Schrems II Supplementary Measures (EDPB Recommendations 01/2020):**

| Step | Action | When |
|------|--------|------|
| 1. Know your transfers | Map all data flows to third countries | All transfers |
| 2. Verify transfer tool | Confirm SCCs/BCRs/adequacy in place | All transfers |
| 3. Assess third country law | Does local law impinge on SCC effectiveness? Focus: government access (surveillance), data subject rights, judicial redress | All non-adequate countries |
| 4. Adopt supplementary measures | If laws impinge: technical (encryption with keys outside destination, pseudonymization, split processing), organizational (policies, transparency reports), contractual (warrant canary, challenge process) | When law impairs SCCs |
| 5. Procedural steps | If no supplementary measure possible: suspend transfer or notify DPA | Last resort |
| 6. Re-evaluate | Ongoing duty; periodic reassessment | At appropriate intervals |

**DPA Registration & Fees:**
- Many EU member states require controllers/processors to register with their DPA
- Some charge annual fees: UK ICO: £40-£2,900/year (tiered by size/turnover); France CNIL: no fee; Germany: varies by Land (€0-€2,000+); Ireland DPC: no fee
- DPO must also be registered with relevant DPA(s)

**Breach Notification (Articles 33-34):**

| Step | Timeline | Who | What |
|------|---------|-----|------|
| Detection | Immediate | Incident response team | Contain, preserve evidence, assess scope |
| Internal assessment | 0-24 hours | DPO + legal + security | Determine: categories/data subjects affected, approximate number, likely consequences, measures taken/proposed |
| Supervisory authority notification | **Within 72 hours** | Controller (processor must notify controller "without undue delay") | Nature of breach, categories/numbers, DPO contact, consequences, measures taken. If >72 hours: must provide reasons for delay. |
| Data subject notification | **Without undue delay** (if high risk) | Controller | Nature of breach, DPO contact, likely consequences, measures taken, recommendations to mitigate |
| Documentation | Permanent obligation | Controller + Processor | Document ALL breaches (even non-notifiable): facts, effects, remedial action; available for DPA inspection |

### ePrivacy Directive (2002/58/EC) — "Cookie Law"

- **Lex specialis** to GDPR: particularizes GDPR for electronic communications
- **Cookie consent (Art 5(3)):** Storing/accessing info on user's device requires consent — except for "strictly necessary" for service explicitly requested by user
- **ePrivacy Regulation (ePR):** Proposed replacement (stalled since 2017); would harmonize across EU; latest council text ~2024 but timeline uncertain
- **Strictly necessary exemption is NARROW:** Covers: session cookies, load-balancing cookies, authentication cookies, shopping cart, payment, security, user-input cookies (session only). Does NOT cover: analytics (even GA4), A/B testing, personalization, advertising, social media plugins.
- **Consent per ePrivacy:** Must meet GDPR consent standard (freely given, specific, informed, unambiguous). Cookie walls = non-compliant per EDPB when access is conditional on accepting non-essential cookies.
- **Cookie consent validity:** No fixed expiry in law. CNIL guidance: 6 months; ICO: "appropriate"; IAB TCF: 13 months; common practice: refresh every 6-13 months.

### CCPA/CPRA — California Consumer Privacy Act / California Privacy Rights Act

| Right | CCPA (2020) | CPRA (2023+) |
|-------|------------|-------------|
| Right to Know | Access personal information collected (12-month lookback) | Access beyond 12 months (unless impossible/disproportionate); expanded categories |
| Right to Delete | Delete PI subject to exceptions | Expanded; service provider/procurement deletion obligations |
| Right to Opt-Out of Sale | Sale of PI to third parties | Expanded to "sale or sharing" (cross-context behavioral advertising = "sharing") |
| Right to Opt-Out of Sharing | N/A | New; opt-out of cross-context behavioral advertising |
| Right to Correct | N/A | New; correct inaccurate PI |
| Right to Limit Use of Sensitive PI | N/A | New; limit use to necessary purposes (service/product delivery) |
| Right to Non-Discrimination | Cannot discriminate for exercising rights | Strengthened; no financial incentive programs that are unjust/unreasonable/coercive |
| Right to Access Automated Decision-Making | N/A | Access to logic and likely outcomes of ADM; opt-out option |

**CPRA thresholds (expanded from CCPA):**
- Buy, sell, or share PI of 100,000+ consumers/households (CCPA was 50,000)
- OR derive 50%+ annual revenue from selling/sharing PI
- B2B and employee exemptions ended Jan 1, 2023

**CPPA (California Privacy Protection Agency):** New dedicated enforcement agency per CPRA; rulemaking authority; administrative enforcement; can levy fines up to $7,500 per intentional violation.

**Enforcement:** AG civil penalties: $2,500 per violation (unintentional), $7,500 per violation (intentional) or per CPPA; private right of action only for data breaches (statutory damages $100-$750 per consumer per incident).

**Real enforcements:** Sephora $1.2M (2022, first CCPA enforcement — failure to disclose sale of PI, failure to honor GPC); DoorDash (2024, CPPA enforcement for selling PI without notice).

### US State Comprehensive Privacy Laws — Comparison

| Feature | California (CCPA/CPRA) | Virginia (VCDPA) | Colorado (CPA) | Connecticut (CTDPA) | Utah (UCPA) | Texas (TDPSA) | Oregon (OCPA) | Delaware (DPDPA) | Iowa (ICDPA) | Montana (MTCDPA) |
|---------|----------------------|------------------|----------------|---------------------|------------|---------------|---------------|------------------|-------------|------------------|
| **Effective** | 2020/2023 | Jan 1, 2023 | July 1, 2023 | July 1, 2023 | Dec 31, 2023 | July 1, 2024 | July 1, 2024 | Jan 1, 2025 | Jan 1, 2025 | Oct 1, 2024 |
| **Applicability threshold** | $25M+ revenue OR 100K consumers/households OR 50%+ revenue from PI sales | 100K consumers OR 50%+ revenue from PI sales (no revenue threshold) | Same as Virginia | Same as Virginia | $25M+ AND 100K+ consumers | No threshold (substantive applicability) | 100K consumers OR 25K consumers + % revenue | 35K consumers OR 10K + 20%+ revenue | 100K consumers OR 50%+ revenue | 50K consumers OR 50%+ revenue |
| **Opt-in for sensitive data** | Limit use right | Opt-in | Opt-in | Opt-in | Opt-in (child+precise geo only) | Opt-in | Opt-in | Opt-in | N/A (no sensitive data recognition) | Opt-in |
| **Global opt-out (GPC)** | Required | Not required | Required by July 2024 | Required by Jan 2025 | Not required | Not required | Required by Jan 2026 | Required by Jan 2026 | Not required | Not required |
| **DPIA required** | Risk assessment (sale/sharing, sensitive, ADM) | DPIA (targeted ads, sale, sensitive, ADM, profiling risk) | DPIA (same + processing PI for profiling with foreseeable risk) | DPIA (same as Colorado) | None (no DPIA requirement) | DPIA (similar to Colorado) | DPIA | DPIA | None | DPIA |
| **Data minimization** | Purpose-limited | Required | Required | Required | Not required | Required | Required | Required | Not required | Required |
| **Cure period** | No cure (post-CPRA) | 30-day cure (sunset Dec 2025) | 60-day cure (sunset Jan 2025) | 60-day cure (sunset Dec 2024) | 30-day cure (permanent) | 30-day cure (permanent) | 30-day cure (sunset Jan 2026) | 60-day cure (sunset Dec 2025) | 90-day cure (permanent) | 60-day cure (sunset Apr 2026) |
| **Private right of action** | Data breach only | No | No | No | No | No | No | No | No | No |
| **Enforcement** | AG + CPPA | AG | AG + DA | AG | AG | AG | AG | AG (DOJ) | AG | AG |

**Other states with enacted legislation (2025-2027 effective):** Tennessee (TIPA, 2025), Indiana (2026), Kentucky (2026), Nebraska (2025), New Hampshire (2025), New Jersey (2025), Maryland (MODPA, 2025), Minnesota (2025), Rhode Island (2026). **More than 20 states** now have comprehensive privacy laws.

**Federal privacy law landscape:** American Privacy Rights Act (APRA) — bipartisan discussion draft 2024 (not passed); preemption of state laws remains key sticking point.

### LGPD — Brazil (Lei Geral de Proteção de Dados)

- **Patterned after GDPR** with Brazilian specifics
- **ANPD (Autoridade Nacional de Proteção de Dados):** Enforcement began 2021; active scrutiny increasing
- **10 legal bases** (vs GDPR's 6): adds "protection of credit," "research," and "protection of life/health" as standalone bases
- **Data mapping** (inventário de dados): ANPD requires comprehensive data mapping for compliance
- **DPO ("Encarregado"):** Mandatory for all controllers (broader than GDPR); must be publicly identified
- **Breach notification:** "Reasonable time frame" (ANPD guidance: 3 business days recommendation, not 72-hour mandate like GDPR)
- **International transfers:** Similar to GDPR structure; adequacy decisions, SCCs, BCRs, specific derogations
- **Sanctions:** Effective Aug 1, 2021; fines up to 2% of Brazil revenue (max 50M reais per violation); daily fines; partial/total suspension of processing/database
- **Enforcement:** 2023 saw first major sanctions; ANPD ramping up from guidance phase to active enforcement

### PIPL — China (Personal Information Protection Law)

| Provision | Key Points |
|-----------|-----------|
| **Data localization** | Critical Information Infrastructure Operators (CIIOs) and processors handling PI reaching CAC thresholds must store PI domestically |
| **Cross-border transfers** | Must pass CAC security assessment (for CIIOs, large-volume PI, or sensitive PI), sign SCCs (CAC-issued), or obtain certification |
| **Consent** | "Separate consent" for: sharing PI with other processors, public disclosure of PI, collection of sensitive PI, cross-border transfer, use of PI in public-facing imagery |
| **Sensitive PI** | Broader than GDPR: includes biometric, religious, medical/health, financial accounts, location tracking; AND PI of minors under 14 (automatically sensitive) |
| **Algorithmic governance** | Transparency obligation; right to opt out of algorithmic recommendations; no differential pricing using algorithms |
| **Enforcement** | Fines up to 50M RMB or 5% of prior year's revenue; personal liability for responsible persons (100K-1M RMB fines + potential ban); business license revocation possible |
| **Effective** | November 1, 2021 |

**CAC (Cyberspace Administration of China):** Primary regulator; aggressive enforcement since mid-2023; cross-border data transfer relaxed slightly in 2024 with new regulations (exemptions for non-sensitive/non-critical data below volume thresholds).

### PIPEDA — Canada

- **PIPEDA:** 10 fair information principles; consent-based (express or implied depending on sensitivity); Bill C-27 (proposed Consumer Privacy Protection Act — CPPA) would replace PIPEDA with GDPR-like framework including tribunal enforcement and administrative monetary penalties
- **Quebec Law 25 (formerly Bill 64):** Sept 2022 + 2023 stages; GDPR-like: mandatory DPO, breach recording, PIAs, right to data portability, right to be forgotten (de-indexing), automated decision transparency, administrative penalties up to CAD $10M or 2% of worldwide turnover, penal fines up to CAD $25M or 4%
- **Provincial health laws:** Alberta PIPA, BC PIPA (substantially similar to PIPEDA); Ontario PHIPA (health-specific); New Brunswick PHIPAA

### Other Global Privacy Laws

| Law | Country/Region | Key Features | Status |
|-----|---------------|-------------|--------|
| **APP (Australian Privacy Principles)** | Australia | 13 APPs; OAIC enforcement; Notifiable Data Breaches (NDB) scheme; CDR (Consumer Data Right) privacy safeguards for open banking/energy/telecom | Privacy Act review: proposed reforms include fair/ reasonable test, direct right of action, tort of serious invasion of privacy |
| **PDPA** | Singapore | 9 obligations (consent, notification, purpose limitation, accuracy, protection, retention, access/correction, transfer, openness); amended 2020 — mandatory data breach notification, expanded deemed consent, data portability (pending), higher financial penalties (max 10% of annual SG turnover or SGD $1M, whichever higher) | Active enforcement; mandatory DNC Registry |
| **PDPB (DPDP Act 2023)** | India | Consent-based with legitimate uses exceptions; consent managers; significant data fiduciaries (SDFs) — additional obligations; Data Protection Board of India; penalties up to ₹250 Cr per violation cross-border data flow default allowance with government blocking power for specified countries | Act passed August 2023; rules under development (expected late 2024/2025); phased implementation |
| **PIPA** | South Korea (amended 2023) | One of the strictest globally; data localization features; right to data portability; right to reject automated decisions; expanded breach notification (within 24 hours to PIPC + 5 days to data subject); fines up to 3% of revenue | Active; vigorously enforced |
| **APPI** | Japan | Amended 2020 + 2022; mandatory breach notification (PPC); cross-border transfer disclosure; expanded data subject rights; PPC enforcement | Japan-EU mutual adequacy; active enforcement |
| **POPIA** | South Africa | Effective July 2021; 8 conditions for lawful processing; Information Regulator; prior authorization for certain processing; fines up to ZAR 10M or imprisonment; cross-border rules | Active enforcement started 2022+ |

### Adequacy Decisions (EU Commission)

| Country/Regime | Adequacy Status | Scope |
|---------------|----------------|-------|
| **Andorra, Argentina, Faroe Islands, Guernsey, Isle of Man, Israel, Jersey, New Zealand, Uruguay** | Adequate | Full adequacy finding |
| **Canada** | Adequate (commercial) | PIPEDA only (not provincial laws beyond those deemed substantially similar) |
| **Japan** | Adequate (mutual) | PPC-covered processing; mutual adequacy arrangement |
| **Republic of Korea** | Adequate | PIPA-covered processing; 2021 adequacy decision |
| **Switzerland** | Adequate | Swiss FADP |
| **United Kingdom** | Adequate (post-Brexit) | UK GDPR; dual adequacy: EU → UK (2021, extended 2025) + UK → EU (2021, ongoing) |
| **United States** | Adequate (limited) | EU-US Data Privacy Framework (DPF) only — certified entities; NOT general adequacy |
| **UK Extension to DPF** | UK-US Data Bridge | UK Extension to EU-US DPF; effective Oct 2023 |
| **Swiss-US DPF** | Effective July 2024 | Swiss-US Data Privacy Framework |

### EU-US Data Privacy Framework (DPF)

- **Replaced:** Privacy Shield (invalidated by Schrems II, July 2020)
- **EU-US DPF:** Adequacy decision July 10, 2023
- **Key safeguards (vs Privacy Shield):**
  - US EO 14086 (Oct 2022): Enhanced safeguards for signals intelligence; necessity and proportionality; two-tier redress mechanism (Civil Liberties Protection Officer + Data Protection Review Court)
  - DPF Principles: Notice, choice, accountability for onward transfer, security, data integrity/purpose limitation, access, recourse/enforcement/liability
  - Self-certification via ITA (Department of Commerce); annual re-certification; published on DPF list
- **Challenges:** NOYB has announced challenge (noyb vs. DPF); Max Schrems predicts it will reach CJEU within 2-3 years; legal uncertainty remains
- **Practical impact:** DPF provides stronger legal basis for US transfers vs SCCs+TIA alone; but long-term viability uncertain


## Industry-Specific Regulatory

### Education (EdTech)

| Regulation | Country | Scope & Key Points |
|-----------|---------|-------------------|
| **FERPA** | US | Protects educational records of students (K-12 + post-secondary); "educational records" = records directly related to a student maintained by educational agency/institution. Parental consent required for disclosure (exceptions: school officials with legitimate educational interest, directory information after opt-out opportunity, transfer, health/safety emergency). **EdTech vendors as "school officials":** Must be under direct control of school regarding use/maintenance of education records; perform institutional service/function; follow same requirements as school employees. Critical: vendor must NOT re-disclose or use PII for any other purpose. |
| **COPPA** | US | Children's Online Privacy Protection Act — applies to operators of websites/online services directed to children under 13 OR knowingly collecting PI from children under 13. Requires: verifiable parental consent before collection, privacy policy, right to review/delete child's information, data retention limitation. **EdTech context:** School can consent in lieu of parent when tool used exclusively for educational purposes (school authorization exception); but strict limitations apply. |
| **PPRA** | US | Protection of Pupil Rights Amendment — surveys collecting certain categories of information (political, religious, income, sexual behavior) require parental consent; right to inspect instructional materials |
| **GDPR — Children (EU)** | EU | Art 8: Children under 16 (member state variation: 13-16) require parental consent for information society services; member state derogations allowed; UK: age 13 |

### Gaming & Gambling

| Jurisdiction | Regulator | Key Requirements |
|-------------|-----------|-----------------|
| **UKGC (United Kingdom)** | UK Gambling Commission | License required; KYC/AML per MLR; age verification (Challenge 25); self-exclusion (GAMSTOP); responsible gambling tools (deposit limits, time-outs, reality checks); financial vulnerability checks; advertising compliance (CAP code) |
| **MGA (Malta)** | Malta Gaming Authority | B2C and B2B licenses; compliance audit; technical system audit; key function roles required; source of wealth/funds checks |
| **Curacao** | Curacao Gaming Control Board (reforms 2024) | Transitioning from master license model to direct licensing; LOK (National Ordinance on Games of Chance) 2024; previously criticized for lax enforcement |
| **Gibraltar** | Gibraltar Gambling Commissioner | License required; substance over form — must have substantive presence in Gibraltar |
| **US (per state)** | NJ DGE, PA PGCB, NV GCB, MI MGCB, etc. | State-by-state licensing; significant investigation cost ($50K-500K+); geolocation verification (within state borders); responsible gaming programs; tax structures vary widely (8.5-51% GGR) |
| **Sweden** | Spelinspektionen | License per vertical (sports betting, casino, etc.); duty of care; SEK 2K deposit cap for casino (temporary measure made potentially permanent); Bonus restrictions (one-time welcome bonus) |

### Telecommunications

| Regulation | Region | Key Provisions |
|-----------|--------|---------------|
| **ePrivacy Directive / ePR** | EU | Confidentiality of communications; traffic/location data handling; cookie consent; direct marketing rules; public directories; caller ID; itemized billing |
| **GDPR + ePrivacy interplay** | EU | GDPR general framework; ePrivacy particularizes for electronic communications sector; consent for cookies (ePrivacy) vs legitimate interest for analytics (controversial — most DPAs say consent required) |
| **Lawful Intercept** | National (varies) | CALEA (US); RIPA/IPA (UK); TKÜV (Germany); telecommunications providers must enable lawful interception per court order/warrant; technical standards for LI interfaces (ETSI LI, 3GPP LI) |
| **Data Retention** | EU (varies) | CJEU invalidated blanket data retention (Tele2/Watson, La Quadrature du Net); member states can require targeted retention for national security; varied implementation across EU |
| **NIS2 — Digital Infrastructure** | EU | Telecommunications providers covered as "essential entities" under NIS2 (Annex I); must implement cybersecurity risk management measures and report significant incidents |

### Automotive & IoT

| Standard/Regulation | Scope | Key Points |
|--------------------|-------|-----------|
| **UN R155** | Cyber Security (vehicle type approval) | Mandatory for new vehicle types in EU from July 2022 (all new vehicles July 2024); CSMS (Cyber Security Management System) certification; covers vehicle lifecycle from design to decommissioning; threat analysis and risk assessment (TARA); vehicle security operations center (VSOC) |
| **UN R156** | Software Updates (vehicle type approval) | SUMS (Software Update Management System) certification; safe and secure software updates; RXSWIN (software identification) documentation; update integrity and authenticity verification |
| **ISO/SAE 21434** | Road vehicles — cybersecurity engineering | Process-based standard: cybersecurity culture, governance, TARA, concept, development, validation, production, operations/maintenance, decommissioning; aligns with UN R155 |
| **GDPR for Connected Vehicles** | EU | EDPB Guidelines 01/2020: vehicle data = personal data (including VIN, location, driver behavior, biometrics); consent required for non-essential processing (infotainment, personalized services, insurance telematics); data minimization; user profiles must be deletable |
| **IoT Cybersecurity** | Global | EU: Cyber Resilience Act (CRA, expected 2024-2025 enforcement) — mandatory cybersecurity requirements for products with digital elements; vulnerability disclosure obligations; CE marking linked to cybersecurity; lifecycle security updates (min 5 years). US: IoT Cybersecurity Improvement Act (2020) — NIST standards for IoT procured by federal government. UK: PSTI Act (2024) — mandatory security requirements for consumer IoT (no default passwords, vulnerability disclosure, update transparency). Singapore: Cybersecurity Labelling Scheme (CLS) for consumer IoT |

### Critical Infrastructure

| Regulation | Region | Key Points |
|-----------|--------|-----------|
| **NIS2 Directive** (2022/2555) | EU | Replaces NIS1; expands scope (essential + important entities in 18 sectors); cybersecurity risk management (all-hazards); incident reporting (significant incidents within 24 hours early warning + 72 hours notification + final report within 1 month); supply chain security; board-level accountability; fines: essential entities: €10M or 2% global turnover (whichever higher); important entities: €7M or 1.4% |
| **DORA (Digital Operational Resilience Act)** | EU (financial sector) | Effective January 2025; ICT risk management, incident reporting, digital operational resilience testing (TLPT — threat-led penetration testing for critical entities), ICT third-party risk (oversight framework for critical ICT providers like cloud), information sharing |
| **CIRCIA (Cyber Incident Reporting for Critical Infrastructure Act)** | US | Signed 2022; CISA rulemaking (NPRM published 2024); covered entities in 16 critical infrastructure sectors must report: covered cyber incidents within 72 hours; ransom payments within 24 hours; $100K+ civil penalties for non-compliance |
| **NERC CIP** | US/Canada (electric grid) | Mandatory reliability standards for bulk electric system; CIP-003 through CIP-014: security management controls, personnel/training, electronic security perimeters, physical security, cyber asset management, incident response, configuration management, vulnerability assessment, supply chain risk, transmission station physical security |
| **TSA Security Directives** | US (pipelines, rail, aviation) | Post-Colonial Pipeline (2021): SD 2021-01/02/03; mandatory incident reporting (within 12 hours to CISA), cybersecurity coordinator, contingency/ recovery planning, vulnerability assessment |

### HR & Employment Technology

| Regulation | Country | Key Points |
|-----------|---------|-----------|
| **FCRA (Fair Credit Reporting Act)** | US | Background checks (employment screening) — must obtain written consent; pre-adverse action process (provide copy of report + Summary of Rights before adverse action); adverse action notice; accuracy requirements for CRAs; 7-year lookback limit for most criminal records (bankruptcy = 10 years) |
| **EEOC Guidance** | US | AI-based hiring tools must not create disparate impact on protected classes; 4/5ths rule; employer liability for vendor AI tools if discriminatory |
| **NYC Local Law 144** | US (New York City) | Automated Employment Decision Tools (AEDT): mandatory bias audit before use; notice to candidates/employees; right to alternative evaluation; effective July 2023 with enforcement beginning July 2024 |
| **GDPR — Employee Data** | EU | Art 88: Member states may provide more specific rules for employment context; generally: consent is problematic (power imbalance — employee cannot freely consent); legitimate interest or legal obligation preferred bases; employee monitoring strictly limited (proportionality); works council involvement (Betriebsrat in Germany, CSE in France); Art 49 derogations NOT for routine HR data transfers |
| **Illinois BIPA (Biometric Information Privacy Act)** | US (Illinois) | Private right of action ($1K negligent, $5K intentional/reckless per violation); written informed consent before collecting biometric data (fingerprints, facial scans); retention/destruction schedule; prohibition on sale of biometric data. White Castle $17B exposure in class action (2023 — $1K × 9,500 employees × 45,000 scans); significant risk for time/attendance systems using fingerprints |

### Cannabis

| Area | Regulatory Landscape |
|------|---------------------|
| **Federal Status (US)** | Schedule I under Controlled Substances Act (CSA) — federally illegal; rescheduling to Schedule III proposed by DEA (2024); would not legalize but would remove 280E tax burden |
| **State-by-State** | 38 states + DC allow medical; 24 states + DC allow adult use; each state has unique licensing, testing, packaging, advertising, and track-and-trace requirements |
| **Seed-to-Sale Tracking** | Metrc (used by ~25 states), BioTrackTHC, Leaf Data Systems; RFID-tagged plants; every transfer logged; diversion prevention |
| **Banking** | SAFER Banking Act (proposed) — would provide safe harbor for financial institutions serving state-legal cannabis businesses; currently most operate cash-only or via state-chartered credit unions |
| **280E (IRS)** | No deduction for ordinary business expenses for Schedule I/II trafficking businesses; effective tax rate 70-80% for cannabis businesses; rescheduling to III would eliminate 280E burden |

### Insurance (InsurTech)

| Regulation | Country/State | Key Points |
|-----------|--------------|-----------|
| **State Insurance Regulation** | US (per state) | McCarran-Ferguson Act (1945) — insurance regulated by states; each state has DOI; licensing (producer, adjuster, MGA, TPA, insurer); rate/form filing; market conduct exams; risk-based capital (RBC) requirements |
| **Model Audit Rule (MAR)** | US (NAIC) | NAIC Annual Financial Reporting Model Regulation (#205); similar to SOX 404; applies to insurers exceeding premium thresholds; internal control over financial reporting (ICFR); management report; external auditor attestation |
| **IRDAI** | India | Insurance Regulatory and Development Authority; licensing; product filing; investment limits; solvency margin; reinsurance; data localization requirement; intermediaries regulation |
| **Consumer Duty** | UK (FCA) | Extends to insurance products; fair value assessment; product governance; consumer understanding/ support standards |
| **GDPR** | EU | Insurance data = special category (health data) for underwriting/claims; explicit consent typically required |

### Real Estate / PropTech

| Regulation | Country | Key Points |
|-----------|---------|-----------|
| **RESPA (Real Estate Settlement Procedures Act)** | US | Prohibition on kickbacks/referral fees for settlement services; affiliated business arrangement (AfBA) disclosure; good faith estimate/loan estimate requirements; HUD-1/closing disclosure |
| **Fair Housing Act** | US | Prohibits discrimination in sale/rental/financing based on race, color, religion, sex, national origin, disability, familial status; AI/algorithmic tenant screening must not create disparate impact |
| **Property Data Privacy** | US (emerging) | GDPR/CCPA apply to property transaction data containing PII; specific real estate privacy concerns: tenant screening data, property ownership records, mortgage application data |
| **PropTech-specific** | Global | Smart home IoT = GDPR + Cyber Resilience Act intersection; tenant behavioral data = sensitive processing; property management platforms = controller/processor determination |

---
## International Standards Mapping

| Standard | Equivalent/Related | Region | Certification Body | Assessment Cycle | Cost Estimate |
|----------|-------------------|--------|-------------------|-----------------|---------------|
| **SOC 2** | ISAE 3402 (International), ISAE 3000 (Attestation) | Global (US-origin) | AICPA-licensed CPA firm | Annual report; Type II = 12-month period | $30K-$80K/year |
| **ISO 27001:2022** | ISMS certification | Global (EU-origin) | ANAB-accredited Certification Body (CB) | 3-year cycle (Stage 1 + Stage 2 + Surveillance year 1 & 2) | $40K-$85K/3-year cycle (external audit only) |
| **PCI DSS 4.0** | PCI Security Standards | Global | QSA (Qualified Security Assessor) for ROC; self-assessment for SAQ | Annual validation | $12K-$80K/year (depending on SAQ type and if QSA required) |
| **FedRAMP** | NIST SP 800-53 | US Federal | 3PAO (Third-Party Assessment Organization) | Annual assessment + continuous monitoring | $250K-$750K+ first year; $100K-$250K/year ongoing |
| **CMMC 2.0** | NIST SP 800-171 + 800-172 | US DoD supply chain | C3PAO (Level 2) / DIBCAC (Level 3) | Triennial assessment (Level 2/3); annual self-affirmation (Level 1) | $15K-$100K+ (Level 1 self-assessment free) |
| **Cyber Essentials / Plus** | IASME Governance | UK | IASME Certification Body | Annual | £300-£500 (Essentials), £1,500-£4,000 (Plus) |
| **BSI IT-Grundschutz** | ISO 27001 basis + German specifics | Germany | BSI-certified auditor | 3-year ISO 27001 cycle + IT-Grundschutz check | €15K-€50K (with ISO 27001) |
| **ENS (Esquema Nacional de Seguridad)** | Security framework for Spanish public sector | Spain | CCN-certified auditor (CCN-STIC) | 2-year certification cycle (low/medium); high = more frequent | €8K-€30K |
| **SecNumCloud** | Enhanced cloud security | France | ANSSI-accredited CB | ISO 27001 + additional SecNumCloud criteria | €50K-€150K+ |
| **C5 (Cloud Computing Compliance Criteria Catalogue)** | Cloud security framework | Germany | BSI / accredited auditor | Based on audit report | €30K-€80K |
| **IRAP (Information Security Registered Assessors Program)** | FedRAMP equivalent for Australian gov | Australia | ASD-certified IRAP assessor | Annual assessment | AUD $40K-$150K |
| **ISMAP (Information System Security Management and Assessment Program)** | FedRAMP equivalent for Japanese gov | Japan | ISMAP-registered auditing body | Registration (valid ~1.5 years); renewal with continuous audit | ¥5M-¥30M |
| **MTCS (Multi-Tier Cloud Security)** | Singapore cloud security | Singapore | MTCS-certified auditing organization | 3-year certification | SGD $15K-$60K |
| **K-ISMS** | Korean ISMS | South Korea | KISA-accredited certification body | 3-year certification | KRW 15M-60M |

### Cross-Framework Control Mapping

| Control Domain | ISO 27001:2022 (Annex A) | SOC 2 (TSC) | NIST SP 800-53 Rev 5 | PCI DSS 4.0 | HIPAA Security Rule |
|---------------|--------------------------|-------------|---------------------|-------------|-------------------|
| Access Control | A.5.15-5.18, A.8.2-8.5 | CC6.1-CC6.3 | AC family (25 controls) | Req 7 | 45 CFR §164.312(a) |
| Asset Management | A.5.9-5.14 | CC6.1 | CM-8 | Req 2.4 | — |
| Cryptography | A.8.24 | CC6.1, CC6.7 | SC-8, SC-12, SC-13 | Req 3, Req 4 | 45 CFR §164.312(e) |
| Incident Response | A.5.24-5.28 | CC7.1-CC7.5 | IR family (10 controls) | Req 12.10 | 45 CFR §164.308(a)(6) |
| Change Management | A.8.32 | CC8.1 | CM-3, CM-4 | Req 6.4 | — |
| Vendor Management | A.5.19-5.22 | CC9.1-CC9.2 | SA family (22 controls) | Req 12.8 | 45 CFR §164.308(b) |
| BCP/DR | A.5.29-5.30 | CC7.5, A1.2 | CP family (13 controls) | Req 12.10 | 45 CFR §164.308(a)(7) |
| Logging & Monitoring | A.8.15-8.17 | CC7.1-CC7.4 | AU family (16 controls) | Req 10 | 45 CFR §164.312(b) |
| Physical Security | A.7.1-7.14 | CC6.4 | PE family (19 controls) | Req 9 | 45 CFR §164.310 |
| HR Security | A.6.1-6.8 | CC1.1-CC1.5 | PS family (10 controls) | Req 12.6-12.7 | 45 CFR §164.308(a)(3) |

---
## Startup Compliance Roadmap by Stage

| Stage | Revenue/Funding | Compliance Priorities | Documentation/Evidence | Cost Range | Timeline |
|-------|----------------|----------------------|----------------------|-----------|----------|
| **Pre-seed** | $0-500K | Privacy policy + ToS, basic security (MFA, encrypted DB), data mapping (spreadsheet), cookie consent (if website with EU/CA users), DMCA agent, determine if regulated product | Privacy policy (Iubenda/Termly), GDPR/CCPA privacy notice, basic data map, info sec policy (1 pager), access control spreadsheet | $500-2K one-time; $20-50/mo ongoing | 1-4 weeks |
| **Seed** | $500K-2M | SOC 2 Type I readiness (if enterprise sales), GDPR gap assessment, security risk assessment, penetration test, vendor review process, open-source license audit | SOC 2 Type I report (optional), pen test report, security risk assessment, third-party vendor list, open-source licenses, DPA template | $10K-30K/year | 2-4 months |
| **Series A** | $2-10M | SOC 2 Type II, ISO 27001 gap assessment, DPO (internal or fractional), formal vendor security reviews, compliance automation tooling (Vanta/Drata/Secureframe), employee security training | SOC 2 Type II report (min 6-month observation), ISO 27001 readiness, DPO appointment, DPIA templates, vendor security questionnaires, automated evidence collection | $50K-150K/year | 6-12 months |
| **Series B** | $10-50M | Full ISO 27001 certification, PCI DSS (if payment processing), FedRAMP (if federal pipeline), dedicated compliance team, multi-framework compliance program, TPRM platform | ISO 27001 certificate, PCI ROC/SAQ, continuous monitoring evidence, compliance dashboards, risk register, incident response tests, TPRM assessments | $200K-500K/year | 12-24 months |
| **Series C+** | $50M+ | Continuous compliance automation, global privacy program (multiple jurisdictions), regulatory affairs team, Board-level compliance reporting, external audit coordination (multiple frameworks), M&A due diligence readiness | Multi-framework continuous monitoring, board reports, global ROPA, regulatory filings, privacy impact assessments, AI governance framework, GRC platform | $500K-2M+/year | Ongoing (program maturity) |

### Seed Stage — When to Start What

| Scenario | Trigger | First Compliance Investment |
|----------|---------|---------------------------|
| **Enterprise deal (>$100K)** in pipeline | Customer security questionnaire received (200+ questions) | SOC 2 Type I readiness + penetration test ($15K-25K) |
| **10K+ EU users** or **first EU enterprise deal** | DPAs being requested; DSARs arriving | GDPR gap assessment + DPA template + privacy consultant ($8K-15K) |
| **Payment processing** (>$1M/year or enterprise payment requirements) | Acquirer/vendor requires PCI compliance evidence | PCI SAQ A or A-EP ($2K-5K) |
| **Healthcare data** (even 1 covered entity customer) | PHI handling | HIPAA risk assessment + BAA template ($10K-15K) |
| **Fundraising in 6-12 months** | DD preparation | Open-source license audit ($2K-5K) + IP assignment review |

### Compliance Program Maturity Model

| Level | Name | Characteristics | Typical Stage |
|-------|------|---------------|---------------|
| **Level 0: Nonexistent** | No awareness; no controls; no documentation | Compliance not on radar | Idea/Pre-product |
| **Level 1: Initial/Ad Hoc** | Reactive; basic privacy policy + ToS; manual processes; spreadsheets | MVP with paying customers | Pre-seed |
| **Level 2: Managed** | Documented policies; formal risk assessment; pen testing; vendor review; SOC 2 Type I | Preparing for/responding to enterprise sales | Seed / Series A |
| **Level 3: Defined** | SOC 2 Type II or ISO 27001 certified; compliance automation; DPO appointed; DPIA process; incident response tested | Enterprise sales accelerating | Series A / B |
| **Level 4: Quantitatively Managed** | Multi-framework certified; continuous monitoring; metrics-driven; board reporting; proactive horizon scanning | Public company or PE-backed scale-up | Series B / C |
| **Level 5: Optimizing** | Continuous improvement; predictive compliance; integrated GRC; compliance as competitive moat | Market leader in regulated industry | Series C+ / Public |

---
## Quick Reference: Industry → Top 3 Regulations

| Industry | Top 3 Regulations (by enforcement risk) |
|----------|--------------------------------------|
| B2B SaaS (general) | GDPR → SOC 2 → ISO 27001 |
| B2C App (consumer) | GDPR → CCPA/state privacy → ePrivacy (cookies) |
| HealthTech / Digital Health | HIPAA → FDA (SaMD) → GDPR (health data) |
| FinTech / Payments | AML/BSA → PCI DSS → GDPR/GLBA (privacy) |
| EdTech | FERPA → COPPA → GDPR (EU schools) |
| AdTech / MarTech | ePrivacy → GDPR → CCPA/state privacy |
| AI / ML / LLM | EU AI Act → GDPR → Copyright (training data) |
| Blockchain / Web3 | AML/BSA → Securities (Howey) → OFAC Sanctions |
| IoT / Connected Devices | Cyber Resilience Act (EU) → UN R155/156 (auto) → PSTI Act (UK consumer IoT) |
| Marketplace / Platform | GDPR → PSD2 (EU payments) → DSA (EU platforms) |
| Government / GovTech | FedRAMP → FISMA → CMMC (if DoD) |
| Critical Infrastructure | NIS2 (EU) → CIRCIA (US) → NERC CIP (energy) |
| Gaming / Gambling | UKGC/MGA/State licensing → AML/KYC → GDPR |
| HR Tech / Employment | FCRA → GDPR (employee) → BIPA (biometric) |
| InsurTech | State DOI → Model Audit Rule → GDPR |
