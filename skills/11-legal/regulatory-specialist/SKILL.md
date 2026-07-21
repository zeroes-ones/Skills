---
name: regulatory-specialist
description: FDA 21 CFR Part 11, ISO 13485, MDR, HIPAA compliance, GxP validation, audit trail requirements, medical device software (SaMD), quality management systems.
author: Sandeep Kumar Penchala
type: legal
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - regulatory-specialist
token_budget: 3983
output:
  type: "code"
  path_hint: "./"
---
# Regulatory Specialist

Regulatory compliance framework for medical device software (SaMD), health tech, and life sciences. Covers FDA regulations, EU MDR, HIPAA, GxP validation, and quality management systems with emphasis on software-specific implementation.

## Ground Rules — Read First

These rules apply to *every* response this skill produces. Regulatory pathways are product-specific and guidance changes — a wrong classification or approval path can delay market entry by years.

- **Never claim an FDA/CE/MDR approval pathway without knowing the device classification.** FDA Class I, II, III and EU MDR Class I, IIa, IIb, III have fundamentally different requirements. A 510(k) recommendation for a Class III device is dangerously wrong. Always confirm the intended use and classification first.
- **Regulatory requirements change — verify current guidance documents.** FDA guidance documents, EU MEDDEV/MDCG documents, and IMDRF technical documents are updated regularly. If you reference a specific guidance, add: "Confirm this is the current version at [fda.gov](https://www.fda.gov) or [ec.europa.eu](https://ec.europa.eu)."
- **GxP validation is context-dependent.** GAMP5 categories, validation depth, and risk assessment depend on the system's intended use, patient safety impact, and data integrity requirements. Do not prescribe a specific validation approach without understanding the GxP context (GLP, GCP, GMP, GDP).
- **Never state a compliance deadline without checking enforcement discretion.** FDA and EU competent authorities routinely publish enforcement discretion policies, transition periods, and exceptions. A "must comply by" date may have been extended. Verify current timelines before making deadline claims.
- **Admit when you need the actual regulation text.** Guidance documents summarize and interpret regulations — they are not the law. When the answer hinges on precise regulatory language, state that the user should consult the actual regulation text (21 CFR, EU MDR 2017/745, IVDR 2017/746, etc.) through their regulatory affairs team or notified body.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Classifying a Software as a Medical Device (SaMD) under FDA risk categories (Class I, II, III) or EU MDR (Class I, IIa, IIb, III)
- Preparing a 510(k) premarket submission, De Novo request, or CE marking technical documentation
- Implementing 21 CFR Part 11 compliant electronic records and electronic signatures (ER/ES)
- Establishing a Quality Management System (QMS) aligned with ISO 13485:2016 and 21 CFR Part 820 (QSR)
- Conducting GxP (GAMP5) computer system validation for manufacturing, clinical, or laboratory systems
- Building HIPAA-compliant infrastructure: administrative, physical, and technical safeguards
- Designing audit trail and data integrity controls compliant with FDA ALCOA+ principles
- Preparing for FDA inspection or notified body audit — mock audit, CAPA review, documentation readiness

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### SaMD Classification (FDA)
```
                     ┌──────────────────────────────┐
                     │ START: FDA SaMD risk class?    │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Device drives or informs        │
                    │ clinical management where       │
                    │ error could cause serious       │
                    │ injury or death?                │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Class III     │    │ Device informs    │
                    │ PMA required  │    │ clinical mgmt     │
                    │ (highest risk)│    │ where error could │
                    │ e.g., AI for  │    │ cause non-serious │
                    │ stroke        │    │ injury?           │
                    │ diagnosis     │    └──┬──────────┬────┘
                    └───────────────┘       │YES       │NO
                                       ┌────▼────┐ ┌───▼──────────┐
                                       │Class II │ │Class I (lowest│
                                       │510(k) or│ │risk): General │
                                       │De Novo  │ │controls only. │
                                       │e.g.,    │ │e.g., medical  │
                                       │imaging  │ │calculator,    │
                                       │CADt     │ │medication     │
                                       └─────────┘ │reminder app  │
                                                    └──────────────┘
```
**When Class III (PMA):** Life-sustaining/life-supporting, or failure could cause serious injury/death — AI stroke detection, closed-loop insulin delivery, cardiac monitoring. PMA required.
**When Class II (510(k)/De Novo):** Moderate risk — imaging CADt, diagnostic decision support, clinical calculators with significant output. Clearance via substantial equivalence or novel De Novo.
**When Class I (General Controls):** Low risk — medication reminders, general wellness, simple calculators, educational tools. No premarket submission; register + list + QSR compliance.

### EU MDR Classification
```
                     ┌──────────────────────────────┐
                     │ START: EU MDR classification?  │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Is it an active device (relies │
                    │ on energy source beyond human  │
                    │ body/gravity)?                 │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────────────────▼────┐
                    │ Active therapeutic or           │
                    │ diagnostic?                     │
                    └──────────────────┬─────────────┘
                                       │
                    ┌──────────────────▼──────────────────┐
                    │ Intended to administer/remove         │
                    │ medicinal products, or for clinical   │
                    │ intervention on central circulatory   │
                    │ or nervous system?                    │
                    └────┬─────────────────────────────┬───┘
                         │ YES                         │ NO
                    ┌────▼──────┐    ┌─────────────────▼──────┐
                    │Class III  │    │Diagnosis of life-       │
                    │(highest)  │    │threatening state?       │
                    │Rule 9/10  │    └──┬──────────────────┬───┘
                    └───────────┘       │YES              │NO
                                   ┌────▼────┐    ┌───────▼──────┐
                                   │Class IIb│    │Monitor vital │
                                   │Rule 10a │    │parameters    │
                                   └─────────┘    │where         │
                                                  │deterioration │
                                                  │is immediate  │
                                                  │risk?         │
                                                  └──┬───────┬───┘
                                                     │YES   │NO
                                                ┌────▼──┐ ┌─▼──────┐
                                                │Class  │ │Class IIa│
                                                │IIb    │ │or lower │
                                                └───────┘ └────────┘
```
**When Class III:** Highest risk — active therapeutic with critical function, central circulatory/nervous system, or Rule 21 software driving clinical decisions where death/irreversible deterioration possible.
**When Class IIb:** Medium-high risk — active diagnostic for life-threatening conditions (Rule 10a), monitoring vital parameters where immediate danger (Rule 10b).
**When Class IIa:** Medium-low risk — diagnostic support, treatment planning, patient monitoring without immediate risk. Most clinical decision support software.
**When Class I:** Low risk — software with no direct patient impact or wellness/administrative purposes.

### HIPAA Compliance: Business Associate Status
```
                     ┌──────────────────────────────┐
                     │ START: Is your company a       │
                     │ Business Associate?            │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Create, receive, maintain, or   │
                    │ transmit PHI on behalf of a     │
                    │ Covered Entity?                 │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ BA Agreement  │    │ Process PHI at   │
                    │ REQUIRED with │    │ direction of     │
                    │ Covered Entity│    │ customer but no  │
                    │ Implement:    │    │ CE relationship? │
                    │ - Admin       │    └──┬──────────┬────┘
                    │   safeguards  │       │YES       │NO
                    │ - Physical    │  ┌────▼────┐ ┌──▼──────────┐
                    │   safeguards  │  │Sub-     │ │Not a BA —   │
                    │ - Technical   │  │contractor│ │HIPAA likely │
                    │   safeguards  │  │BA +     │ │not directly │
                    │ - Breach      │  │upstream │ │applicable.  │
                    │   notification│  │BA agree-│ │Still follow │
                    │ - BA policy & │  │ment req.│ │security best │
                    │   training    │  └─────────┘ │practices.   │
                    └───────────────┘              └──────────────┘
```
**When you ARE a BA:** SaaS handling PHI for hospitals, clinics, insurers — BAA required with each CE customer, implement 45 CFR §164 Subpart C safeguards.
**When you are a Subcontractor BA:** Process PHI on behalf of another BA (cloud hosting, analytics provider) — need BA agreement with upstream BA, same safeguards apply.
**When you are NOT a BA:** No PHI touching your systems, or merely a conduit (mail carrier, ISP transmitting but not storing PHI). HIPAA not applicable but security best practices encouraged.

### Validation Approach (GxP/GAMP 5)
```
                     ┌──────────────────────────────┐
                     │ START: Computer system          │
                     │ validation approach?            │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ System is commercial off-the-   │
                    │ shelf (COTS) with no            │
                    │ customization?                  │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │GAMP Category │    │ Configured COTS  │
                    │3: Leverage    │    │ (config not code)│
                    │supplier QMS + │    │?                │
                    │vendor audit.  │    └──┬──────────┬────┘
                    │Validate       │       │YES       │NO
                    │config only.   │  ┌────▼────┐ ┌──▼──────────┐
                    └───────────────┘  │GAMP Cat │ │GAMP Category│
                                       │4:      │ │5: Custom /  │
                                       │Validate│ │bespoke      │
                                       │configured│ │development  │
                                       │workflows│ │Full SDLC    │
                                       │+ reports│ │validation   │
                                       └─────────┘ └─────────────┘
```
**When GAMP Category 3:** Off-the-shelf, no customization — MS Office, standard OS, commercial DB. Leverage vendor QMS; validate that it works in your environment.
**When GAMP Category 4:** Configured COTS (ERP, LIMS, MES) — validate configurations, workflows, reports, interfaces. Test that configs meet requirements.
**When GAMP Category 5:** Custom-built — full SDLC validation: URS → FS → DS → IQ → OQ → PQ. Traceability matrix, code review, unit testing, integration testing.

### Data Integrity Issue Response (ALCOA+)
```
                     ┌──────────────────────────────┐
                     │ START: Data integrity issue     │
                     │ detected — what action?         │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Data was modified, deleted, or  │
                    │ fabricated deliberately?        │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO (accidental)
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │Immediately    │    │ System error or  │
                    │halt GxP       │    │ user mistake?    │
                    │operations     │    └──┬──────────┬────┘
                    │involved.      │       │YES       │NO
                    │Engage QA +    │  ┌────▼────┐ ┌──▼──────────┐
                    │Legal. Consider│  │CAPA:    │ │Investigate  │
                    │FDA disclosure │  │root cause│ │further —    │
                    │if data used in│  │analysis │ │possibly data │
                    │regulatory     │  │+ technical│ │integrity    │
                    │submission.    │  │control   │ │non-issue or │
                    └───────────────┘  │fix       │ │edge case    │
                                       └──────────┘ └─────────────┘
```
**When to halt operations + engage Legal:** Deliberate fabrication/deletion of GxP data — possible criminal liability (FDA 704(a)(3) authority), regulatory disclosure may be required.
**When to initiate CAPA:** Accidental data loss from system error — fix root cause (audit trail gaps, missing backups, insufficient access controls), document corrective action.
**When to invest more:** Unexplained issue — could be one-off or systemic. Deep-dive investigation; may reveal systemic ALCOA+ violations needing comprehensive remediation.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Product Classification & Regulatory Pathway

1. **SaMD Classification** —
   - **FDA (per IMDRF framework)**:
     - Class I: low risk (e.g., medical image storage, appointment reminders). General Controls. Most are 510(k) exempt.
     - Class II: moderate risk (e.g., diagnostic imaging software, clinical decision support with qualified clinician review). 510(k) Premarket Notification — demonstrate substantial equivalence to predicate device.
     - Class III: high risk (e.g., software that directly diagnoses or treats life-threatening conditions without clinician intervention). PMA (Premarket Approval) — clinical evidence of safety and effectiveness.
   - **EU MDR (Annex VIII)**:
     - Classification rules: Rule 11 specifically for software. Class I (lowest) to Class III (highest).
     - Class I: self-declaration. Classes IIa-IIb-III: require Notified Body involvement.
     - Class IIb and III require Clinical Evaluation Report (CER) per MEDDEV 2.7/1 Rev.4.
2. **Regulatory Pathway Selection**:
   - **510(k)** — Traditional, Special, or Abbreviated. Identify predicate device(s). Map substantial equivalence: intended use, technological characteristics, performance data.
   - **De Novo** — For novel Class I/II devices without a predicate. Includes risk-benefit analysis.
   - **PMA** — Most stringent. Requires clinical investigation data (IDE), manufacturing information, labeling.
   - **CE Marking under MDR** — Technical Documentation (Annex II and III), Clinical Evaluation, Risk Management per ISO 14971, QMS per ISO 13485.
3. **HIPAA Applicability Determination** — If handling Protected Health Information (PHI):
   - Are you a Covered Entity (healthcare provider, health plan, clearinghouse) or Business Associate (vendor handling PHI for a covered entity)?
   - If Business Associate, enter into Business Associate Agreement (BAA) with covered entity.
   - Map the Privacy Rule (uses and disclosures), Security Rule (administrative/physical/technical safeguards), and Breach Notification Rule.
4. **Deliverable: Regulatory Strategy Document** — Classification rationale, regulatory pathway with timeline and estimated costs, predicate device analysis (for 510(k)), applicable standards list, gap assessment against each standard.

### Phase 2 (~30 min): Quality Management System (QMS)

1. **QMS Design (ISO 13485 + 21 CFR Part 820)** — Core subsystems:
   - **Document Control** (820.40 / 13485 §4.2): Document hierarchy (Quality Manual → SOPs → Work Instructions → Forms/Records). Approval workflow, version control, periodic review, obsolescence management. eQMS tooling: Greenlight Guru, Qualio, MasterControl.
   - **Design Controls** (820.30 / 13485 §7.3): Design and Development Plan → Design Inputs (user needs → design requirements) → Design Outputs (specifications, drawings, source code) → Design Review → Design Verification (did we build it right?) → Design Validation (did we build the right thing?) → Design Transfer → Design Changes. Maintain a Design History File (DHF) — the story of how the device was developed.
   - **Risk Management per ISO 14971**: Hazard identification → risk estimation (severity × probability) → risk evaluation → risk control → residual risk evaluation → risk/benefit analysis → Risk Management Report. Maintain a Hazard Traceability Matrix linking hazards to risks to controls to verifications.
   - **CAPA** (Corrective and Preventive Action): Issue identification → investigation and root cause analysis (5 Whys, fishbone) → action plan → implementation → effectiveness verification → closure. CAPA is the most-cited area in FDA inspections — ensure timely closure.
   - **Complaint Handling & Adverse Event Reporting**: MDR (Medical Device Reporting) for FDA — report deaths/serious injuries within 30 days. Vigilance reporting under MDR — serious incidents within 15 days. Implement complaint triage: is it an MDR-reportable event?
   - **Supplier Management**: Supplier qualification, approved supplier list, supplier audits, incoming inspection. Critical for software suppliers (cloud providers, API vendors, open-source components).
   - **Management Review**: Quarterly review of QMS health — quality policy, quality objectives, audit results, CAPA metrics, complaints, regulatory changes.
2. **Design History File (DHF) Structure** — For software: User Needs Document → Software Requirements Specification (SRS) → Software Architecture Document (SAD) → Software Design Specification (SDS) → Source Code (with traceability) → Unit/Integration/System Test Protocols and Reports → Software V&V Report → Risk Management File → Labeling → Release to Production record.
3. **Software Development Life Cycle (IEC 62304)** — Software safety classification (A: no harm, B: non-serious injury, C: death or serious injury). Documentation requirements scale with class. Key deliverables: Software Development Plan, Software Requirements, Architecture Design, Detailed Design, Unit Implementation & Verification, Integration & Integration Testing, System Testing, Software Release.

### Phase 3 (~20 min): Validation & Part 11 Compliance

1. **21 CFR Part 11 (Electronic Records / Electronic Signatures)** — Requirements for systems that create, modify, maintain, or transmit electronic records used in regulated activities:
   - **Validation**: Validate systems to ensure accuracy, reliability, and consistent intended performance.
   - **Audit Trails**: Secure, computer-generated, time-stamped audit trails recording operator entries and actions that create/modify/delete electronic records. Changes shall not obscure previously recorded information. Retain audit trails for at least the period required for the subject electronic records.
   - **Authority Checks**: Ensure only authorized individuals can use the system, electronically sign records, and access/alter records.
   - **Device Checks**: Determine validity of data input and operational instructions.
   - **Electronic Signatures**: Unique to one individual; not reused or reassigned. Must include printed name, date/time of signing, and meaning (author, reviewer, approval). Biometric or two-component (ID + password) signature required — two-component signatures require periodic password changes and lockout after failed attempts.
   - **System Documentation**: Maintain documentation of system validation, user access policies, and controls.
2. **GAMP5 Computer System Validation (CSV)** — Category-based approach:
   - Category 1 (Infrastructure Software): OS, databases, middleware. Document version, configuration, and controls.
   - Category 3 (Non-Configured COTS): Off-the-shelf, no customization (e.g., basic lab equipment). Verify correct installation and vendor assessment.
   - Category 4 (Configured COTS): Configured off-the-shelf (e.g., configured QMS, ERP). Risk-based validation: focus on configured workflows and reports.
   - Category 5 (Custom/Bespoke): Custom-developed. Full validation: User Requirements → Functional Specification → Design Specification → Code Review → Unit/Integration/Acceptance Testing → Traceability Matrix.
   - Validation lifecycle: Validation Plan → User Requirements Specification (URS) → Functional Risk Assessment → IQ (Installation Qualification) → OQ (Operational Qualification) → PQ (Performance Qualification) → Validation Summary Report → Ongoing change control and periodic review.
3. **Data Integrity — ALCOA+ Principles**:
   - **A**ttributable: who did it, when?
   - **L**egible: readable, permanent
   - **C**ontemporaneous: recorded at the time of activity
   - **O**riginal: original record or certified copy
   - **A**ccurate: error-free, complete, truthful
   - **+** Complete, Consistent, Enduring, Available
   - For software: implement audit trails per ALCOA+. Never allow direct database edits in production. All changes go through the application layer with full audit trail.

### Phase 4 (~15 min): Submission & Ongoing Compliance

1. **Premarket Submission Preparation**:
   - **510(k)**: Cover letter, 510(k) summary, Truthful and Accurate statement, Indications for Use, 510(k) Summary or Statement, Standards Data Report, Financial Certification, Device Description, Substantial Equivalence Discussion, Software documentation (per FDA Guidance on Content of Premarket Submissions for Software), Biocompatibility, Sterilization, Electromagnetic Compatibility, Performance Testing (bench, animal, clinical).
   - **CE Marking (MDR)**: Technical Documentation (device description, design/manufacturing info, GSPRs checklist per Annex I, risk/benefit analysis, clinical evaluation), Declaration of Conformity, Notified Body review for IIa+ devices.
2. **FDA Inspection Readiness** — QSIT (Quality System Inspection Technique) focuses on 4 major subsystems: Management Controls, Design Controls, CAPA, Production and Process Controls. Preparation: mock inspection, back-room/front-room team training, SME assignments, document retrieval system. Post-inspection: respond to 483 observations within 15 business days with corrective action plan.
3. **Post-Market Surveillance** — FDA: MDR reporting, annual post-market reports for high-risk devices, post-approval studies (for PMA). EU: Post-Market Surveillance (PMS) Plan, Periodic Safety Update Report (PSUR), Post-Market Clinical Follow-up (PMCF).
4. **Software Updates & Change Control** — Assess impact of every software change on safety and effectiveness. Document in Change Control per QMS. Determine whether change requires a new 510(k) (FDA guidance: changes that significantly affect safety or effectiveness — new indication, new algorithm, new risk profile). For MDR: assess whether change requires notified body re-approval.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- In a software context, "validation" does NOT mean testing the software works — it means producing documented evidence that the software meets user needs and intended uses in a production-equivalent environment.
- Build your QMS to be audit-ready at all times, not just when an inspection is announced. An auditor should find the evidence they need without anyone hunting for it.
- Every design output must trace back to a design input, and every design input must trace forward to verification. Maintain this traceability matrix from day one — retrofitting it is painful.
- Start the risk management process during requirements gathering, not after implementation. Hazards identified late require expensive redesigns.
- Part 11 audit trails must be tamper-resistant — store them in append-only tables or immutable logs. The audit trail itself must be auditable.
- Never validate a production system with production data that contains PHI — use synthetic or de-identified test data.
- The Predicate Device analysis for 510(k) is the single most scrutinized part of your submission — invest the time to make the substantial equivalence argument airtight.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Regulatory compliance in healthcare, finance, and safety-critical domains requires deep cross-functional coordination. Engineering, quality, and legal all own pieces of the compliance puzzle.

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Legal Advisor** | Regulatory interpretation, enforcement response, contracts | Regulatory applicability analysis, enforcement risk, contract compliance terms |
| **CTO Advisor** | System architecture for compliance (audit trails, validation) | Technical controls for Part 11, data integrity architecture, validation strategy |
| **System Architect** | QMS integration, validated system design, electronic records | System boundaries, data flows, electronic signature implementation |
| **QA / Validation Engineer** | IQ/OQ/PQ, GxP validation, test strategy | Validation protocols, traceability matrix, acceptance criteria |
| **Security Reviewer** | Access controls, audit trails, data integrity | HIPAA Security Rule controls, FDA cybersecurity guidance, IEC 62304 security requirements |
| **GDPR/Privacy Specialist** | Patient data, PHI, clinical trial data | HIPAA Privacy Rule vs GDPR intersection, data subject rights in healthcare context |
| **Backend Developer** | Audit trail implementation, electronic signatures, data integrity | Part 11 requirements for audit trails, timestamp synchronization, non-repudiation |
| **DevOps** | Validated environment management, change control, deployment | GxP change control process, environment segregation (DEV/VAL/PROD), deployment validation |
| **Product Strategist** | SaMD classification, intended use statements, 510(k) strategy | Regulatory pathway determination, labeling requirements, clinical evidence strategy |
| **Project Manager** | Submission timelines, regulatory milestones, resource planning | FDA/notified body submission calendar, review cycles, approval dependencies |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Intended use change for SaMD/SiMD product | Legal Advisor, Product Strategist, CTO Advisor | May change FDA classification (Class I→II→III) or require new 510(k) |
| Adverse event or device malfunction reported | Legal Advisor, QA, CEO Strategist | MDR vigilance reporting (15-30 day deadlines); potential field safety corrective action |
| FDA Form 483 or Warning Letter received | Legal Advisor, QA, CEO Strategist, External Regulatory Counsel | Enforcement action; response required within 15 business days |
| Change to QMS or validated system architecture | QA, System Architect, CTO Advisor | Re-validation may be required; change control board review |
| New data integrity issue discovered (ALCOA+ violation) | QA, CTO Advisor, Legal Advisor | Part 11/GxP violation; potential data invalidation and regulatory disclosure |
| Cybersecurity vulnerability in medical device software | Security Reviewer, CTO Advisor, Legal Advisor | FDA cybersecurity guidance requirements; potential recall or field action |
| Audit finding (internal or external) rated Critical or Major | QA, Project Manager, Legal Advisor | CAPA required; may delay certification or regulatory submission |
| Regulatory submission (510(k), PMA, CE marking technical file) filed | Project Manager, Product Strategist, CEO Strategist | Clock starts on review timeline; commercial launch dependent on clearance |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| FDA Warning Letter or consent decree | **External FDA Counsel** + CEO Strategist + Board | Corporate existential risk; specialized regulatory defense required |
| Class I recall decision (reasonable probability of serious harm/death) | **CEO Strategist** + External Regulatory Counsel + PR/Comms | Public health risk; immediate regulatory and public notification |
| Clinical trial serious adverse event (SAE) with potential product liability | **External Counsel** + CEO Strategist + IRB/Ethics Committee | Multi-jurisdiction reporting; litigation preparation |
| ISO 13485 / MDR certification at risk (major nonconformity) | **Notified Body** + CEO Strategist + QA Lead | CE marking at risk; EU market access may be suspended |
| Whistleblower allegation of data integrity fraud (GxP) | **External Counsel** + Board + FDA (if required) | Criminal liability potential; DOJ/FDA investigation risk |

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
Regulatory compliance by founder reading FDA guidance docs. No QMS, no validation, no regulatory submissions. Class I self-declaration only. HIPAA: BAA templates from legal marketplace. No CE marking. Operate as "not a medical device" if defensible. Risk: must have regulatory strategy documented before first pilot. Cost: $0-500/month. Overkill: ISO 13485 certification, QMS software, 510(k) preparation, external regulatory counsel.

### Small (2-10 people, 100-10K users)
Regulatory consultant (10-20 hours/month) or fractional RA/QA lead. SaMD classification memo documented. QMS: paper-based or lightweight (Greenlight Guru Essentials). 510(k) or CE marking preparation begins. HIPAA: full BAA process, annual risk assessment, security rule compliance. Part 11: audit trail requirements designed in. Cost: $3K-10K/month. Overkill: full QMS software suite, multiple regulatory submissions in parallel, clinical trials.

### Medium (10-50 people, 10K-1M users)
In-house RA/QA specialist or dedicated consulting firm. QMS: electronic (Greenlight Guru, Qualio, MasterControl). 510(k) submitted or CE marking technical file under review. ISO 13485 certification. HIPAA: annual assessments, breach simulation exercises. Validation: GAMP 5 framework applied. Regulatory affairs capability: EU MDR transition, UKCA, TGA, Health Canada. Cost: $10K-50K/month.

### Enterprise (50+ people, 1M+ users)
RA/QA department (3-10+). QMS: enterprise (Veeva Vault, TrackWise, Sparta). Multiple cleared/approved devices across FDA, EU MDR, and international markets. Post-market surveillance: complaint handling, adverse event reporting (MDR, MEDDEV 2.12). Clinical evaluation reports (CER) per MEDDEV 2.7.1 Rev 4. Design controls integrated with product development. Regulatory intelligence: monitoring global changes. Cost: $100K-500K+/month.

### Transition Triggers
| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | Product confirmed as medical device by regulatory assessment; preparing first regulatory submission | Hire regulatory consultant; document QMS; begin 510(k) or CE Marking technical file |
| Small → Medium | First regulatory submission filed; QMS audit scheduled (FDA/Notified Body) | Implement electronic QMS; hire RA/QA specialist; pursue ISO 13485 |
| Medium → Enterprise | Multiple cleared devices; international expansion (>3 markets); post-market surveillance required | Build RA/QA department; implement Veeva/TrackWise; establish regulatory intelligence; CER/PMS programs |

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| **SaMD Regulatory Classification** | Determining whether software qualifies as a medical device and at what risk class | FDA 21 CFR 862-892, EU MDR Annex VIII, IMDRF risk categorization — classification memo with rationale |
| **510(k) / De Novo Submission** | Seeking FDA clearance for Class II medical device software | Substantial equivalence (510(k)) or novel device (De Novo) — predicate device analysis, performance testing, software documentation per IEC 62304 |
| **CE Marking / EU MDR Technical File** | Placing medical device software on EU market | Technical documentation per Annex II/III, Clinical Evaluation Report (CER) per MEDDEV 2.7.1 Rev 4, Notified Body audit preparation |
| **HIPAA Compliance Program** | Handling PHI as a Covered Entity or Business Associate | 45 CFR §164 — administrative/physical/technical safeguards, BAA management, breach notification, annual risk assessment, workforce training |
| **21 CFR Part 11 / EU Annex 11 Validation** | Electronic records/electronic signatures in regulated GxP environments | Audit trail design, ALCOA+ data integrity, electronic signature controls, CSV per GAMP 5, IQ/OQ/PQ documentation |
| **QMS Implementation (ISO 13485 / 21 CFR 820)** | Building quality management system for medical device development | Greenlight Guru, Qualio, MasterControl, Veeva Vault — document control, CAPA, complaint handling, design controls, management review |
| **FDA Inspection Readiness** | Preparing for FDA pre-approval inspection, routine surveillance, or for-cause inspection | Mock audit, SME preparation, back-room coordination, CAPA evidence, documentation organization, 483 response strategy |
| **Post-Market Surveillance (PMS)** | Ongoing monitoring of device safety and performance after market clearance | Vigilance reporting (MDR, MEDDEV 2.12), complaint trending, PMCF, PSUR, recall/field action management |


### Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| `Permission denied` | Missing file/system permissions | Use `chmod +x` or `sudo`; check user/group ownership |
| `command not found` | Required tool not installed | Install with `apt install`, `brew install`, or `npm install -g` |
| `File exists` | Output file already exists | Use `--force` flag or specify different output path |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  SaMD classification documented with rationale per FDA and EU MDR criteria
- [ ] **[S2]**  Regulatory pathway selected (510(k), De Novo, PMA, CE Marking) with timeline and cost estimates
- [ ] **[S3]**  QMS implements all required subsystems per ISO 13485 and 21 CFR Part 820 — audited within last 12 months
- [ ] **[S4]**  Design History File (DHF) complete for current device version — traceability from user needs to verification
- [ ] **[S5]**  ISO 14971 Risk Management File exists with hazard traceability matrix and risk/benefit analysis
- [ ] **[S6]**  Software development follows IEC 62304 lifecycle with artifacts appropriate for safety classification
- [ ] **[S7]**  21 CFR Part 11 controls implemented for all GxP-regulated electronic records: audit trails, authority checks, e-signatures
- [ ] **[S8]**  Computer System Validation (CSV/GAMP5) performed for all GxP systems with IQ/OQ/PQ documentation
- [ ] **[S9]**  Audit trails are secure, tamper-resistant, time-stamped, and retained per record retention requirements
- [ ] **[S10]**  ALCOA+ data integrity principles embedded in system design and verified through periodic data integrity audits
- [ ] **[S11]**  HIPAA compliance: BAA executed with all covered entities, Security Rule safeguards implemented, Breach Notification procedures in place
- [ ] **[S12]**  CAPA system operational: issues tracked to closure with root cause analysis and effectiveness verification
- [ ] **[S13]**  FDA inspection / Notified Body audit readiness program in place with mock audits conducted
- [ ] **[S14]**  Post-market surveillance programs active: complaint handling, MDR/vigilance reporting, PSUR, PMCF
- [ ] **[S15]**  Change control process includes assessment of regulatory impact (new 510(k) or notified body notification required?)

## MVP vs Growth vs Scale

| Phase | Team Size | Priority | Regulatory Approach |
|-------|-----------|----------|---------------------|
| **MVP (0→1)** | 1-3 devs, no regulatory hire | Classify correctly, don't ship unregulated | Determine if you're a medical device (FDA decision tree). If yes: hire regulatory consultant ($200-400/hr, 20-40 hrs for classification + pathway). If no: document the determination. |
| **Growth (1→10)** | 3-15 devs, part-time regulatory consultant (10-20 hrs/mo) | Build QMS, prepare submission | ISO 13485-aligned QMS (eQMS tool: Greenlight Guru $600/mo or Qualio $1K/mo), design controls, risk management (ISO 14971), software lifecycle (IEC 62304). Regulatory submission prep. |
| **Scale (10→N)** | 15+ devs, in-house regulatory team (2-4) | Maintain compliance, expand markets | Full QMS with continuous improvement, post-market surveillance, multiple-country regulatory, notified body/ FDA relationship management, regulatory intelligence for new markets. |

**MVP regulatory rule:** Classification is everything. One wrong call = you're shipping an unregulated medical device, which is a criminal offense. Hire a regulatory consultant for 20 hours to classify your product. It costs $4K-8K and can save $500K+ in remediation. If you're NOT a medical device, document the decision rationale.

## Cost-Effective Decision Table

| Decision | Free/Cheap Option | Paid Upgrade | When to Upgrade |
|----------|------------------|--------------|-----------------|
| SaMD classification | FDA classification wizard (free) + guidance docs | Regulatory consultant ($4K-8K for classification) | Any ambiguity. Classification error is the #1 most expensive mistake. |
| QMS tooling | Manual: Google Docs + spreadsheets + DocuSign | Greenlight Guru ($600/mo) or Qualio ($1K/mo) | >3 design control documents or preparing for 510(k)/CE marking |
| 510(k) submission | Self-prepare (requires deep regulatory knowledge, 3-6 months) | Regulatory consultant ($50K-100K full submission) | First-time submission or novel device. If you have a clear predicate, self-prep may be viable. |
| CE Marking (MDR) | Self-prepare technical documentation | Notified body + consultant ($80K-150K) | Mandatory for Class IIa+. Not optional. |
| HIPAA compliance | Self-assessment + HHS guidance + BAA templates (free) | HIPAA consultant ($10K-25K engagement) | Processing PHI for covered entities. HIPAA violations are $100-50K per violation. |
| Part 11 compliance | Manual: documented procedures + change-controlled spreadsheets | Validated eQMS + audit trail systems ($1K-3K/mo) | Any GxP-regulated activity. Manual Part 11 is auditable but painful at scale. |
| Clinical evaluation (MDR) | Literature review (requires expertise) | CRO or consultant ($30K-80K) | Class IIb/III devices. Required for CE marking. |
| ISO 13485 certification | Self-implement QMS, hire auditor ($5K-8K for certification audit) | Consultant-led implementation ($30K-60K) | First-time certification or significant QMS gaps |

**Annual regulatory budget by phase:** MVP: $4K-15K (consultant classification + initial guidance). Growth: $50K-200K (QMS + submission + consultant). Scale: $200K-800K+ (team + maintenance + new markets).

## Scalability Decision Tree

```
Is your software intended for medical purposes (diagnosis, treatment, prevention, monitoring)?
├── YES → It's potentially SaMD. Proceed to classification.
│   ├── Is it Class I (low risk, e.g., medical image storage)?
│   │   └── General controls, likely 510(k) exempt. Document decision. Ship.
│   ├── Is it Class II (moderate risk, e.g., diagnostic aid with clinician review)?
│   │   └── 510(k) required. Identify predicate device. Full design controls per 820.30.
│   └── Is it Class III (high risk, e.g., autonomous diagnosis)?
│       └── PMA required. Clinical evidence needed. This is a 2-4 year, $5M+ pathway.
└── NO → Not a medical device under FDA. Document the determination. Ship as general software.

Do you handle Protected Health Information (PHI)?
├── YES → Are you a Covered Entity or Business Associate?
│   ├── Covered Entity → Full HIPAA compliance (Privacy, Security, Breach rules).
│   └── Business Associate → Sign BAA. Implement Security Rule safeguards.
└── NO → HIPAA doesn't apply. Still follow good security practices.

Have you had an FDA inspection or notified body audit in the last 2 years?
├── YES → Were observations (483) or non-conformities issued?
│   ├── YES → CAPA required. Address within timeline. Failure = warning letter.
│   └── NO → Clean audit. Maintain QMS. Schedule next internal audit.
└── NO → Schedule a mock audit within 6 months. Don't wait for the real thing.

Is your software changing (new feature, new algorithm, new intended use)?
├── YES → Does the change significantly affect safety or effectiveness?
│   ├── YES → May need new 510(k) or notified body notification. Assess with consultant.
│   └── NO → Document in change control. No submission needed. Move forward.
└── NO → Maintain. Review annually.
```

## When NOT to Use This Skill (Overkill)

- **You're NOT building medical device software or handling PHI**: This entire skill is overkill for general SaaS. Use security best practices + standard legal docs. The FDA won't knock on your door.
- **You're at concept stage with no prototype**: Regulatory strategy before you've validated the clinical need is premature. Build a prototype. Test with clinicians. Then classify.
- **Wellness/fitness app with explicit "not medical advice" disclaimers**: If you're a step counter or meditation app and you never claim to diagnose or treat, you're likely not SaMD. Get a consultant to confirm, then use standard software practices.
- **You're building on a regulated platform (e.g., Apple HealthKit with FDA-cleared algorithms)**: Your regulatory burden may be lower if the platform handles classification. Still consult — don't assume.
- **Research-only tool (no clinical use)**: IRB oversight may be sufficient. FDA regulations for investigational devices differ from commercial devices.

## Token-Efficient Workflow

```
# Step 1: Classification decision tree (scripted)
python3 scripts/classify_samd.py \
  --intended-use "Software that analyzes retinal images to detect diabetic retinopathy" \
  --clinician-review false --output json
# Returns: {"is_samd": true, "fda_class": "Class II", "pathway": "510(k)", "confidence": "high"}

# Step 2: Decision tree → action per classification
# Class I → Document determination. Ship with general controls.
# Class II → Identify predicate devices. Prepare 510(k). Build QMS.
# Class III → PMA pathway. This is a multi-year commitment. Plan accordingly.

# Step 3: Checklist execution with exit codes
# Verify design controls are in place
python3 scripts/check_design_controls.py --repo . --output json
# Returns: {"design_inputs": true, "design_outputs": true, "traceability": false,
#           "dhf_complete": false, "missing": ["traceability_matrix", "design_review_003"]}
# Exit code 0 = all controls present, 1 = gaps

# Step 4: QMS document status
python3 scripts/qms_status.py --qms-dir docs/qms --output json
# Returns: {"documents": 45, "overdue_review": 3, "next_audit_days": 120}
```

**Principle:** `classify_samd.py` outputs JSON with classification + pathway. Agent follows decision tree to exactly one next action. Document checks verify completeness via exit codes. Never reads regulation text into agent context.

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [FDA — 21 CFR Part 11 (Electronic Records; Electronic Signatures)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [FDA — 21 CFR Part 820 (Quality System Regulation — transitioning to ISO 13485 via QMSR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-820)
- [ISO 13485:2016 — Medical Devices Quality Management Systems](https://www.iso.org/standard/59752.html)
- [ISO 14971:2019 — Medical Devices — Application of Risk Management](https://www.iso.org/standard/72704.html)
- [IEC 62304:2006+AMD1:2015 — Medical Device Software — Life Cycle Processes](https://www.iso.org/standard/64686.html)
- [EU MDR 2017/745 — Full Text](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32017R0745)
- [FDA — Content of Premarket Submissions for Software](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/content-premarket-submissions-management-cybersecurity-medical-devices)
- [IMDRF — SaMD Classification Framework](https://www.imdrf.org/documents/software-medical-device-possible-framework-risk-categorization-and-corresponding-considerations)
- [GAMP5 — A Risk-Based Approach to Compliant GxP Computerized Systems](https://ispe.org/publications/guidance-documents/gamp-5)
- [HIPAA — Security Rule Guidance](https://www.hhs.gov/hipaa/for-professionals/security/index.html)
