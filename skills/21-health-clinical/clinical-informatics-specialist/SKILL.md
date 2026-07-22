---
name: clinical-informatics-specialist
description: FHIR (HL7) standards R4/R5 with resource types, profiles, extensions, and operations. EHR integration patterns for Epic/MyChart, Cerner, Argonaut, USCDI, and SMART on FHIR. Health data exchange
  via HIE networks, TEFCA, Direct Secure Messaging, XDR/XDM. Hemophilia Treatment Center (HTC) data exchange workflows for rare disease registries. Patient-reported outcome (PRO) data standards including
  PROMIS, PRO-CTCAE, and electronic PRO (ePRO). Clinical terminology with SNOMED CT, LOINC, ICD-10-CM, RxNorm, MedDRA. Data mapping pipelines from source systems to FHIR resources to internal data models.
  Consent management for patient data sharing with granular HIE consent. Real-world evidence (RWE) data pipelines for pharma partnerships. Triggered by FHIR, HL7, EHR integration, health data exchange,
  clinical terminology, PRO, HTC, RWE, consent management.
author: Sandeep Kumar Penchala
type: health-clinical
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- clinical-informatics
- fhir
- hl7
- ehr
- healthcare-interoperability
- hemophilia
- patient-reported-outcomes
- real-world-evidence
token_budget: 4000
output:
  type: code
  path_hint: ./
chain:
  consumes_from:
  - backend-developer
  - compliance-officer
  - patient-experience-researcher
  - regulatory-specialist
  feeds_into:
  - ai-safety-health-reviewer
  - data-engineer
  - medical-content-reviewer
  - patient-experience-researcher
  - patient-health-educator
  - product-manager
---
# Clinical Informatics Specialist

Design, implement, and govern health data interoperability systems that bridge clinical workflows, EHR platforms, and research pipelines. This skill covers the full clinical informatics lifecycle — from FHIR resource modeling and EHR integration to real-world evidence data pipelines and patient consent management — with specialized depth in rare disease registries and patient-reported outcomes.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Design FHIR resources or profiles → Start at "Decision Trees > FHIR Resource Selection"
├── Integrate with an EHR system (Epic, Cerner) → Jump to "Decision Trees > EHR Integration Path"
├── Set up health data exchange (HIE, TEFCA) → Go to "Decision Trees > Data Standard Selection"
├── Build a patient-reported outcome (PRO) pipeline → Jump to "Core Workflow > Phase 2 (PRO Data Standards)"
├── Map clinical terminology (SNOMED, LOINC, ICD-10) → Go to "Core Workflow > Phase 3 (Terminology Mapping)"
├── Design consent management flows → Jump to "Core Workflow > Phase 4 (Consent & Governance)"
├── Build an RWE pipeline for pharma → Go to "Best Practices > Real-World Evidence Pipelines"
├── Need HIPAA compliance or regulatory guidance → Invoke `compliance-officer` skill instead
├── Need medical content clinical accuracy review? → Invoke `medical-content-reviewer` for evidence-based content validation
├── Need patient experience research or PROM validation? → Invoke `patient-experience-researcher` for patient journey mapping and PRO instrument selection
├── Need regulatory/safety review of clinical data flows? → Invoke `regulatory-specialist` for FDA/EU regulatory pathway guidance
├── Need AI safety validation for health content? → Invoke `ai-safety-health-reviewer` for clinical AI guardrail testing
├── Need backend integration for FHIR server? → Invoke `backend-developer` for FHIR API implementation
└── Don't know where to start? → Describe the clinical data source and target system and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never design FHIR resources without understanding the clinical workflow.** A FHIR resource models a real clinical interaction — a MedicationRequest without knowing the prescribing context (inpatient vs outpatient, specialty pharmacy, prior auth) is a data skeleton, not a clinical asset. Always ask: "What clinical workflow does this data support?"
- **EHR integration requires explicit patient consent mapping.** Every data exchange must trace to a valid consent artifact. Do not assume consent — verify the consent directive exists, its scope (treatment/payment/operations vs research), and its granularity (all records vs specific encounters vs specific data categories). Missing consent mapping is a HIPAA violation.
- **Terminology codes are never "close enough."** A SNOMED CT code for "bleeding disorder" (64779008) is not interchangeable with "hemophilia A" (28293008). A LOINC code for "bleeding severity" is not the same as "joint bleed count." Always validate codes against the ValueSet authority and the use case — mapping errors cascade into clinical decision support failures.
- **PRO measures must be validated for the target population.** A PROMIS-29 instrument validated in adults with osteoarthritis does not automatically apply to adolescents with hemophilia. Always verify the validation study population, language, and literacy level before recommending a PRO instrument. Do not deploy unvalidated PRO measures in production.
- **Admit what you don't know.** If you haven't confirmed the EHR vendor version, the clinical terminology edition, the consent framework jurisdiction, or the PRO validation population, say so and ask before designing the pipeline.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Designing FHIR R4/R5 resource profiles for clinical data exchange
- Integrating with EHR systems (Epic/MyChart, Cerner) via FHIR APIs, HL7v2, or proprietary interfaces
- Building health data exchange pipelines (HIE networks, TEFCA, Direct Secure Messaging)
- Mapping clinical data from source systems to FHIR resources and internal data models
- Implementing patient-reported outcome (PRO) data collection with PROMIS or PRO-CTCAE
- Designing consent management workflows for granular patient data sharing
- Building real-world evidence (RWE) data pipelines for pharma and research partnerships
- Modeling rare disease registry data (e.g., Hemophilia Treatment Center workflows)
- Standardizing clinical terminology across SNOMED CT, LOINC, ICD-10-CM, RxNorm, and MedDRA

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### EHR Integration Path
```
                     ┌──────────────────────────────┐
                     │ START: EHR integration needed  │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Is the target an Epic or   │
                    │ Cerner instance?           │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────────┐
                    │ Use vendor-  │   │ Does the EHR expose │
                    │ specific     │   │ a FHIR R4 endpoint? │
                    │ FHIR APIs +  │   └────┬──────────┬─────┘
                    │ Epic App      │        │ YES      │ NO
                    │ Orchard /     │   ┌────▼────┐ ┌──▼────────┐
                    │ Cerner        │   │ SMART on │ │ HL7v2 or  │
                    │ Millennium    │   │ FHIR +   │ │ custom API│
                    │ APIs          │   │ USCDI    │ │ with      │
                    └───────────────┘   │ profiles │ │ mapping   │
                                        └──────────┘ └───────────┘
```
**When to use vendor-specific APIs:** Epic (App Orchard, MyChart Bedside, Epic FHIR) or Cerner (Millennium FHIR, PowerChart). >80% of US hospital EHR market. Leverage vendor-specific extensions for scheduling, medications, and provider directories that FHIR base resources don't cover. **When to use SMART on FHIR:** EHR-agnostic integration, single sign-on via OAuth2/OIDC, app launch from within EHR. Required for ONC Health IT Certification. **When to use HL7v2:** Legacy EHR systems without FHIR support, lab results (ORU^R01), ADT feeds (ADT^A01-A08). Map to FHIR as an intermediate normalization layer.

### Data Standard Selection
```
                     ┌──────────────────────────────┐
                     │ START: Health data exchange    │
                     │ standard selection             │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Nationwide interoperability │
                    │ required (US)?              │
                    └────┬──────────────────┬─────┘
                         │ YES              │ NO
                    ┌────▼────────────┐  ┌──▼──────────────────┐
                    │ TEFCA + USCDI   │  │ Direct data exchange │
                    │ v4 (qualified   │  │ between known         │
                    │ health info      │  │ organizations?        │
                    │ networks)        │  └──┬───────────────┬────┘
                    └─────────────────┘     │ YES           │ NO
                                       ┌────▼────────┐ ┌───▼──────────┐
                                       │ Direct       │ │ HIE network  │
                                       │ Secure       │ │ (regional/   │
                                       │ Messaging    │ │ state-level) │
                                       │ (XDR/XDM)    │ │ via IHE       │
                                       └──────────────┘ │ profiles      │
                                                        └──────────────┘
```
**When to choose TEFCA:** National-scale interoperability, multi-network health data exchange, ONC compliance for Qualified Health Information Networks (QHINs). Use USCDI v4 data classes for minimum required data elements. **When to choose Direct Secure Messaging:** Point-to-point provider communication, transition of care (CCDA documents), known recipient endpoints. Simpler than HIE but doesn't scale to population health. **When to choose HIE network:** Regional or state-level data exchange, existing HIE infrastructure, population health analytics. Use IHE profiles (XCA, XDS.b, XCPD) for document query and patient discovery.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~25 min): FHIR Resource Design and Profiling
1. Identify the clinical use case and map it to FHIR resource types: Patient, Encounter, Observation, Condition, MedicationRequest, Procedure, CarePlan, Questionnaire/QuestionnaireResponse for PRO data.
2. Select FHIR version: R4 for broad EHR compatibility (Epic, Cerner support R4), R5 for new projects (improved Questionnaire, Subscription, Evidence-based medicine resources). R4 is production-safe; R5 is forward-looking.
3. Profile resources using FHIR StructureDefinition: constrain cardinality (0..1 → 1..1 for mandatory fields), bind ValueSets to coded elements (e.g., Condition.code bound to US Core Condition Codes), define extensions for custom data elements not in base resources.
4. Validate profiles against base FHIR specification using the FHIR validator (`org.hl7.fhir.validator`). Run `StructureDefinition.snapshot` generation to ensure differential constraints produce valid snapshots.
5. Document each profile with: clinical context, ValueSet bindings with OIDs, example instances, and mapping to source EHR fields. Share profiles via a FHIR ImplementationGuide on a public registry (Simplifier.net or local FHIR server).

### Phase 2 (~25 min): PRO Data Standards and ePRO Implementation
1. Select the appropriate PRO instrument for the clinical context: PROMIS (generic + domain-specific banks for physical function, pain, fatigue, depression), PRO-CTCAE (symptomatic adverse events in clinical trials), disease-specific instruments (e.g., Haem-A-QoL for hemophilia, HAL for hemophilia activities).
2. Model PRO instruments as FHIR Questionnaires: each item → Questionnaire.item, response options → answerValueSet, scoring logic → extension for scoring algorithm. Map responses to FHIR QuestionnaireResponse resources.
3. For electronic PRO (ePRO): design the administration schedule (daily diary, weekly assessment, pre-visit, post-treatment), configure reminders and adherence tracking, set up alert thresholds for clinician review (e.g., pain score >7 triggers nurse notification).
4. Validate the PRO instrument in the target population: check the validation study's sample size, demographics, language, literacy level, and condition match. Document the validation evidence with the instrument selection rationale.
5. Build the data flow: ePRO app → FHIR QuestionnaireResponse → FHIR server → Observation resources (scored items) → analytics pipeline. Ensure each scored item maps to a LOINC code for interoperability.

### Phase 3 (~30 min): Clinical Terminology Mapping and Normalization
1. Inventory all coded clinical data elements in the source system and identify the target terminology for each: diagnoses → SNOMED CT (or ICD-10-CM for billing), lab results → LOINC, medications → RxNorm, adverse events → MedDRA, procedures → SNOMED CT or CPT.
2. Build terminology maps using standard resources: UMLS Metathesaurus for cross-terminology mapping, NIH Value Set Authority Center (VSAC) for regulated ValueSets, FHIR ConceptMap resources for reusable mappings.
3. Handle code system versioning: each code must include the system URI (e.g., `http://snomed.info/sct`), code, and display. Track terminology version (e.g., SNOMED CT US Edition 2024-09-01) — codes can be retired, renamed, or reclassified across versions.
4. Implement terminology validation: all coded fields must validate against the declared ValueSet. Reject or quarantine data with codes outside the ValueSet. Log unmapped codes for manual curation.
5. For rare disease terminologies (hemophilia): supplement standard terminologies with Orphanet codes, HTC-specific extensions, and World Federation of Hemophilia (WFH) bleeding assessment tools mapped to SNOMED CT concepts.

### Phase 4 (~25 min): Consent Management and Data Governance
1. Model patient consent using FHIR Consent resources: define scope (treatment, payment, operations, research), actor (patient, legal guardian, authorized representative), provision (allow/deny by data type, purpose, recipient, time period).
2. Implement granular consent for HIE data sharing: patient can consent to share all records, specific encounter types only, exclude sensitive categories (mental health, substance use, HIV status, genetic data), or opt out entirely.
3. Integrate consent decisions into data access enforcement: every data access request checks the active Consent resource before returning data. Cache consent decisions for performance but invalidate on consent change.
4. For research and RWE use cases: ensure consent covers secondary use of data. De-identification (Safe Harbor or Expert Determination under HIPAA) may be required even with research consent. Document the legal basis for data use (consent, IRB waiver, HIPAA authorization).
5. Design consent revocation workflows: patient revokes consent → all downstream consumers notified → data access revoked within SLA (24 hours for HIE, immediate for EHR portal). Maintain an audit trail of consent changes.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Clinical informatics sits at the intersection of clinical workflows, data engineering, and regulatory compliance. Coordination ensures FHIR resources reflect clinical reality, data pipelines preserve semantic meaning, and consent frameworks meet legal requirements.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Health Compliance** | Consent design, HIPAA compliance, data sharing agreements | Consent model, data use purposes, HIPAA minimum necessary standard, BAAs with data recipients |
| **API Designer** | FHIR API design, SMART on FHIR endpoints, authentication | FHIR resource profiles, search parameters, operations ($validate, $match, $everything), OAuth2 scopes |
| **Database Designer** | Source-to-FHIR data mapping, terminology storage, audit trails | Source system schemas, terminology table design, consent storage model, audit log schema |
| **Data Engineer** | ETL pipelines for clinical data, FHIR server ingestion, RWE pipelines | FHIR resource schemas, mapping logic, terminology codes, data quality rules, refresh frequency |
| **Analytics Engineer** | Clinical data models for analytics, PRO score aggregation, RWE cohorts | FHIR-to-analytics mapping, PRO scoring algorithms, cohort definitions, terminology codes for filters |
| **Security Engineer** | Data access controls, encryption, audit logging | Patient data classification, consent-based access rules, de-identification requirements, audit trail retention |
| **UX Researcher** | ePRO instrument usability, patient portal experience, consent UX | PRO instrument design, consent flow usability, patient-facing terminology, health literacy considerations |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| FHIR resource schema change (new required field, breaking cardinality change) | Data Engineer, Analytics Engineer, API Designer | Downstream pipeline breakage; API version update |
| New terminology version released (SNOMED CT, LOINC, ICD-10-CM) | Data Engineer, Analytics Engineer | Remap codes; re-validate existing data; update ValueSets |
| Consent framework change (new regulation, updated policy) | Health Compliance, Security Engineer | Update Consent resources; re-validate access controls |
| PRO instrument change (new version, updated scoring) | Analytics Engineer, UX Researcher | Update scoring pipeline; re-validate patient-facing instruments |
| EHR vendor API deprecation | API Designer, Data Engineer | Migration timeline; alternative integration path |

### Escalation Path

```
Data sharing violation (unauthorized data release)? → Health Compliance → Legal Advisor → CEO
Interoperability failure (data exchange down > SLA)? → Data Engineer → System Architect → CTO
Clinical terminology mapping error (wrong code → wrong decision support)? → Clinical lead → Health Compliance
Patient consent system failure (consent not enforced)? → Security Engineer → Health Compliance → Legal Advisor
```

### Regulatory Handoffs & Clinical Validation Gates

| Handoff Trigger | Route To | Protocol | Regulatory Timeline |
|----------------|----------|----------|---------------------|
| New FHIR profile created for clinical data exchange | `compliance-officer` → `security-engineer` | Profile validation → HIPAA minimum necessary review → Data use purpose alignment → Consent mapping | Before profile deployment to production |
| Terminology mapping error discovered (wrong code → wrong clinical decision) | `medical-content-reviewer` → clinical lead | Quarantine affected data → Correct mapping → Re-validate downstream systems → Notify impacted analytics | Within 24 hours of discovery |
| EHR integration endpoint returns PHI without proper authorization | `security-engineer` → `compliance-officer` → `legal-advisor` | Halt data flow → Audit access logs → Patient notification assessment → Corrective action | Within 4 hours |
| Consent framework update required (new regulation, policy change) | `compliance-officer` → `legal-advisor` | Review regulatory requirement → Update Consent resource definitions → Re-validate existing consents → Deploy | Per regulatory deadline |
| PRO instrument changed (new version, updated scoring algorithm) | `patient-experience-researcher` → `data-engineer` | Validate new scoring → Update pipeline → Backfill historical scores → Notify analytics consumers | Before next data collection cycle |
| Real-world evidence (RWE) data sharing with pharma partner | `compliance-officer` → `legal-advisor` | De-identification verification → Data use agreement review → Patient consent scope validation → Audit trail setup | Before first data transfer |

**Clinical Validation Gates:**
- **FHIR profile validation gate:** Every FHIR StructureDefinition must pass FHIR validator before any integration code is written. Validated profile catches 80% of interoperability issues at design time. Artifact: FHIR validation report.
- **Terminology code accuracy gate:** All SNOMED CT, LOINC, ICD-10-CM codes validated against ValueSet authority for the target use case. "Close enough" code = clinical decision support failure. Artifact: Terminology mapping validation report.
- **Consent enforcement gate:** Every data exchange must trace to a valid, unexpired Consent resource with matching purpose-of-use and data scope. Missing consent = HIPAA violation. Artifact: Consent validation log per data exchange.
- **PRO instrument validation gate:** PRO instrument must be validated for target population (condition, age, language, literacy level). Unvalidated instrument = unreliable data. Artifact: PRO validation evidence summary.
- **De-identification verification gate:** Expert Determination or Safe Harbor verification before any data leaves the clinical environment. Re-identification risk must be certified as "very small." Artifact: De-identification certification.

## Best Practices
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Profile before you implement.** Write the FHIR StructureDefinition and validate it against the FHIR validator before writing any integration code. A validated profile catches 80% of interoperability issues at design time.
- **Use USCDI as your minimum data baseline.** USCDI v4 defines the minimum data classes required for nationwide interoperability. Start there, then extend with domain-specific profiles (e.g., Hemophilia IG, mCODE for oncology).
- **Map once, use everywhere.** Build a centralized terminology service with canonical mappings (SNOMED ↔ ICD-10-CM ↔ local codes). Every downstream system queries the terminology service — never duplicate mapping logic.
- **Consent is not a checkbox.** Consent is a FHIR Consent resource with computable provisions that downstream systems enforce programmatically. A checkbox in a UI without a backend Consent resource is a compliance gap.
- **PRO measures degrade without monitoring.** Track PRO completion rates, floor/ceiling effects, and response patterns. A PRO instrument with <60% completion rate or >20% ceiling effect is not producing valid data.
- **De-identification is not anonymous re-identification.** Expert Determination under HIPAA requires a qualified statistician to certify re-identification risk is very small. Safe Harbor (18 identifiers removed) is safer but may strip clinically useful data. Choose method based on use case.
- **Test with real clinical data shapes, not synthetic data.** Synthetic FHIR data misses edge cases — missing required fields, codes outside ValueSets, contradictory clinical statements. Use de-identified real data for integration testing.
- **Version everything.** FHIR profiles, terminology ValueSets, consent policies, PRO instruments, mapping tables — all versioned. A pipeline processing data from 2024 with 2026 terminology codes produces garbage.

## Error Decoder
<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|-------|------------|-----|
| FHIR validator rejects resource with `Unknown extension` | Unregistered extension URL | Register extension in StructureDefinition or IG; ensure canonical URL resolves | Every FHIR extension needs a registered StructureDefinition — validate profiles before resources, not after. |
| EHR API returns `401 Unauthorized` for SMART on FHIR request | Expired or mis-scoped OAuth2 token | Refresh token; verify scopes include requested FHIR resource type; check EHR app registration | Token scopes and EHR registration are set once but tested every deployment — automate token validation in your CI pipeline. |
| Terminology service returns `Code not found in ValueSet` | Code from newer/older terminology edition than ValueSet | Update ValueSet to current edition; add mapping for deprecated codes; quarantine unmapped data | Terminology drift is a chronic data quality problem — version-pin every ValueSet and audit code system updates quarterly. |
| PRO data has 0% completion for a specific item | Item is unclear, embarrassing, or technically broken in ePRO app | Review item wording with UX Researcher; check ePRO rendering on target devices; run patient debrief | Zero completion is almost never a patient problem — it is always a design or technical problem. |
| Consent resource prevents expected data access | Consent provision scope too narrow or expired | Review Consent.provision with Health Compliance; check consent date range and purpose-of-use codes | Computable consent is powerful but dangerous — one overly narrow provision can silently block critical data access for years. |

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[CL1]**  FHIR profiles (StructureDefinitions) created, validated, and published in an ImplementationGuide
- [ ] **[CL2]**  All coded elements bound to ValueSets with canonical URIs and version tracking
- [ ] **[CL3]**  EHR integration endpoint documented: vendor, FHIR version, authentication method, rate limits
- [ ] **[CL4]**  SMART on FHIR app registered with EHR vendor; OAuth2/OIDC scopes defined per resource type
- [ ] **[CL5]**  USCDI v4 data classes mapped and supported for all patient-facing data exchange
- [ ] **[CL6]**  Terminology service deployed with canonical mappings: SNOMED CT, LOINC, ICD-10-CM, RxNorm, MedDRA
- [ ] **[CL7]**  PRO instruments modeled as FHIR Questionnaires; scoring algorithms documented and validated
- [ ] **[CL8]**  Consent resources modeled with computable provisions; consent decisions enforced at data access layer
- [ ] **[CL9]**  Consent revocation workflow tested end-to-end; SLA met for downstream notification
- [ ] **[CL10]**  Data mapping pipeline documented: source system → FHIR resource → internal data model
- [ ] **[CL11]**  De-identification method documented (Safe Harbor or Expert Determination); re-identification risk assessed
- [ ] **[CL12]**  HIE/TEFCA connection configured with patient discovery and document query tested
- [ ] **[CL13]**  RWE pipeline data quality checks passing: completeness, plausibility, conformance, temporal consistency
- [ ] **[CL14]**  Audit trail for all data access, consent changes, and terminology updates operational

## Scale Depth: Solo → Small → Medium → Enterprise
<!-- DEEP: 10+min -->

### Solo (1 person, 0-100 patients)
- **What changes**: Use open-source FHIR server (HAPI FHIR, Microsoft FHIR Server OSS). Map to USCDI v4 minimum data classes only. Terminology: manual SNOMED CT and LOINC lookups via UMLS browser. Consent: paper or simple electronic consent (no granular provisions). PRO: Google Forms or REDCap with manual FHIR mapping. No HIE connection.
- **What to skip**: Custom FHIR profiles beyond US Core. SMART on FHIR app registration (unless required by EHR). Automated terminology validation. TEFCA connection. RWE pipelines. Granular consent.
- **Coordination**: You are the informaticist + developer + data mapper. Document mappings in a spreadsheet.

### Small Team (2-10 people, 100-10K patients)
- **What changes**: FHIR server (HAPI or Azure API for FHIR) with custom profiles for rare disease extensions. EHR integration via SMART on FHIR with 1-2 vendor APIs. Terminology service (Ontoserver or custom) with automated validation. PRO via validated ePRO platform. Consent: FHIR Consent resources with basic provisions. Regional HIE connection.
- **What to skip**: TEFCA QHIN connection. Multi-terminology crosswalk automation. Automated PRO alerting. Granular consent beyond category-level. RWE pipelines for pharma.
- **Coordination**: Weekly clinical informatics review. Monthly terminology update review. Quarterly consent audit.

### Medium Team (10-50 people, 10K-100K patients)
- **What changes**: Enterprise FHIR server (Google Cloud Healthcare API, InterSystems IRIS for Health). Full SMART on FHIR app ecosystem. Multi-EHR integration (Epic + Cerner + athenahealth). Terminology service with UMLS integration and automated crosswalks. PRO platform with automated alerting and clinician dashboard. Consent: granular, computable provisions with auto-enforcement. HIE: TEFCA QHIN connection or multi-HIE federation. RWE: de-identified pipeline for pharma partnerships.
- **What to skip**: Full FHIR R5 migration (unless greenfield). Patient-mediated data exchange (SMART Health Cards). AI-driven terminology mapping.
- **Coordination**: Bi-weekly informatics council. Monthly data quality review. Quarterly RWE pipeline audit. Consent governance board.

### Enterprise (50+ people, 100K+ patients)
- **What changes**: Multi-region FHIR server infrastructure. FHIR R5 for new clinical domains (Evidence-based medicine, genomic reporting). SMART on FHIR with patient-mediated exchange. Terminology service with ML-assisted mapping and real-time code updates. PRO platform integrated with EHR and clinical decision support. Consent: patient-facing consent dashboard with dynamic policy updates. HIE: QHIN participant with national-scale exchange. RWE: FDA-grade real-world evidence pipelines with CDISC standards (SDTM, ADaM).
- **What's full production**: Annual FHIR IG publishing cycle. Continuous terminology update pipeline. PRO instrument lifecycle management (validation → adoption → sunset). Consent policy automation. RWE FDA submission readiness.

### Transition Triggers
- **Solo → Small**: First EHR integration required. >500 patients. Multiple PRO instruments in use.
- **Small → Medium**: Multi-EHR integration. TEFCA connection. Pharma partnership requiring RWE. >10K patients.
- **Medium → Enterprise**: National-scale data exchange. FDA RWE submission. Genomic data integration. >100K patients.

## What Good Looks Like

Clinical data flows seamlessly between EHRs, patient apps, and pharma partners. FHIR APIs are the backbone — not afterthoughts. Clinicians trust the data because mappings are validated and provenance is traceable. Real-world evidence pipelines generate insights without manual data wrangling.

## References
<!-- QUICK: 30s -- links to deeper reading -->
- **api-designer** — for FHIR API design patterns, OAuth2/OIDC, and API versioning
- **database-designer** — for clinical data model design, terminology storage, and audit trail schemas
- **data-engineer** — for ETL pipelines from EHR to FHIR server to analytics
- **analytics-engineer** — for clinical data models, PRO score aggregation, and RWE cohort building
- **security-engineer** — for data access controls, consent enforcement, and de-identification
- [HL7 FHIR R4 Specification](https://hl7.org/fhir/R4/) — Resource definitions, profiling, operations
- [US Core Implementation Guide](https://hl7.org/fhir/us/core/) — USCDI-aligned FHIR profiles
- [SMART on FHIR](https://docs.smarthealthit.org/) — App launch, authorization, EHR integration
- [TEFCA Framework](https://www.healthit.gov/topic/interoperability/trusted-exchange-framework-and-common-agreement) — ONC trusted exchange
- [PROMIS HealthMeasures](https://www.healthmeasures.net/explore-measurement-systems/promis) — Validated PRO instruments
- [SNOMED CT](https://www.snomed.org/) — Clinical terminology standard
- [LOINC](https://loinc.org/) — Lab and clinical observation terminology
