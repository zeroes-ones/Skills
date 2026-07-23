# Scale Depth: Solo → Small → Medium → Enterprise

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
