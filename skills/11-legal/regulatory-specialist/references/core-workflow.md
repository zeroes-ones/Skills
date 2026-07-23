# Core Workflow — Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
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

<!-- DEEP: 10+min -->
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

<!-- DEEP: 10+min -->
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

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): Submission & Ongoing Compliance

1. **Premarket Submission Preparation**:
   - **510(k)**: Cover letter, 510(k) summary, Truthful and Accurate statement, Indications for Use, 510(k) Summary or Statement, Standards Data Report, Financial Certification, Device Description, Substantial Equivalence Discussion, Software documentation (per FDA Guidance on Content of Premarket Submissions for Software), Biocompatibility, Sterilization, Electromagnetic Compatibility, Performance Testing (bench, animal, clinical).
   - **CE Marking (MDR)**: Technical Documentation (device description, design/manufacturing info, GSPRs checklist per Annex I, risk/benefit analysis, clinical evaluation), Declaration of Conformity, Notified Body review for IIa+ devices.
2. **FDA Inspection Readiness** — QSIT (Quality System Inspection Technique) focuses on 4 major subsystems: Management Controls, Design Controls, CAPA, Production and Process Controls. Preparation: mock inspection, back-room/front-room team training, SME assignments, document retrieval system. Post-inspection: respond to 483 observations within 15 business days with corrective action plan.
3. **Post-Market Surveillance** — FDA: MDR reporting, annual post-market reports for high-risk devices, post-approval studies (for PMA). EU: Post-Market Surveillance (PMS) Plan, Periodic Safety Update Report (PSUR), Post-Market Clinical Follow-up (PMCF).
4. **Software Updates & Change Control** — Assess impact of every software change on safety and effectiveness. Document in Change Control per QMS. Determine whether change requires a new 510(k) (FDA guidance: changes that significantly affect safety or effectiveness — new indication, new algorithm, new risk profile). For MDR: assess whether change requires notified body re-approval.
