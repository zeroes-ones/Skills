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
