# Core Workflow — Full Implementation

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

### Phase 5 (~30 min): FHIR Implementation Patterns

FHIR is a specification, not a recipe. These patterns translate the spec into working code for the most common clinical integration scenarios.

**Epic/Cerner FHIR Endpoint Patterns:**

```python
# Epic FHIR R4 base URL convention
EPIC_BASE = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4"
# Cerner Millennium FHIR R4
CERNER_BASE = "https://fhir-ehr-code.cerner.com/r4/{tenant_id}"

# SMART on FHIR endpoint discovery via .well-known
# GET https://{ehr_base}/.well-known/smart-configuration
# Returns: authorization_endpoint, token_endpoint, scopes_supported, capabilities

# Patient-specific endpoints
def patient_endpoint(base_url: str, patient_id: str, resource: str) -> str:
    """Build patient-scoped FHIR endpoint."""
    return f"{base_url}/{resource}?patient={patient_id}"

# Example: all observations for a patient
# GET /Observation?patient=12345&category=laboratory&_lastUpdated=ge2024-01-01
```

**SMART on FHIR Authentication Flow:**

```python
# Standalone Launch (patient-facing apps)
# 1. Register app with EHR vendor → get client_id, client_secret
# 2. Redirect to EHR authorization endpoint
standalone_params = {
    "response_type": "code",
    "client_id": "{registered_client_id}",
    "redirect_uri": "https://myapp.com/callback",
    "scope": "launch/patient openid fhirUser patient/Observation.rs "
            "patient/MedicationRequest.rs patient/Condition.rs "
            "offline_access",  # for refresh tokens
    "aud": "{ehr_fhir_base_url}",
    "state": "{csrf_token}"
}
# 3. Exchange authorization code for access token
# POST /token → access_token + patient context (patient ID)

# EHR Launch (clinician-facing, launched from within EHR)
ehr_launch_params = {
    "response_type": "code",
    "client_id": "{registered_client_id}",
    "redirect_uri": "https://myapp.com/callback",
    "scope": "launch openid fhirUser patient/Observation.rs "
            "patient/MedicationRequest.rs user/Observation.rs",
    "aud": "{ehr_fhir_base_url}",
    "launch": "{launch_token_from_ehr}",
    "state": "{csrf_token}"
}
# EHR passes launch token — context includes current patient + user
```

**CDA/CCDA Generation from FHIR Composition:**

```python
# CCDA generation pipeline: FHIR Composition → CCDA XML
# Step 1: Fetch the Composition with all referenced resources
# GET /Composition/{id}?_include=*&_revinclude=*

# Step 2: Transform Composition sections to CCDA structured body
# Composition.section mapping:
CCDA_SECTION_MAP = {
    "allergies":   "2.16.840.1.113883.10.20.22.2.6",   # Allergies
    "medications": "2.16.840.1.113883.10.20.22.2.1",   # Medications
    "problems":    "2.16.840.1.113883.10.20.22.2.5.1", # Problem List
    "results":     "2.16.840.1.113883.10.20.22.2.3.1", # Results
    "vitals":      "2.16.840.1.113883.10.20.22.2.4.1", # Vital Signs
}

# Step 3: Use FHIR to CCDA transformation (e.g., XSLT or FHIRPath-based)
# Validate CCDA output against ONC 2015 Edition Cures Update schematron
# Run: schematron validate -s ccda.sch -d output.xml
```

**Bulk FHIR Export ($export):**

```python
# Bulk FHIR Export — population-level data export
# Step 1: Kick off export (async operation)
# GET /Patient/$export
# Or Group-level export for a defined cohort:
# GET /Group/{cohort_id}/$export
# Parameters: _type=Patient,Observation,Condition,MedicationRequest
#             _since=2024-01-01T00:00:00Z

# Step 2: Poll status endpoint from Content-Location header
# GET /_operations/export/{job_id}
# Response: { "transactionTime": "...", "request": "...",
#             "requiresAccessToken": true, "output": [...] }

# Step 3: Download NDJSON files
# Each output entry: { "url": "https://.../Patient.ndjson", "type": "Patient" }
# Download → validate format → process incrementally

# Step 4: NDJSON handling pattern
import ndjson
def process_bulk_export(file_url: str, access_token: str):
    """Stream NDJSON output from bulk export."""
    with requests.get(file_url, headers={
        "Authorization": f"Bearer {access_token}"
    }, stream=True) as r:
        for line in r.iter_lines():
            resource = ndjson.loads(line)
            yield resource  # process one resource at a time
```

**FHIR Resource Validation Against US Core Profiles:**

```python
# US Core profile conformance validation
# Option A: FHIR $validate operation against server
# POST /Observation/$validate
# Body: Observation resource
# Returns: OperationOutcome with issues[]

# Option B: Validate using FHIR Validator CLI (HAPI-based)
# java -jar org.hl7.fhir.validator.jar resource.json
#   -ig hl7.fhir.us.core#6.1.0
#   -profile http://hl7.org/fhir/us/core/StructureDefinition/us-core-observation-lab

# Option C: FHIRPath-based validation for specific constraints
fhirpath_checks = [
    # US Core Lab Observation: must have category of "laboratory"
    "Observation.category.where(coding.system='http://terminology.hl7.org/CodeSystem/"
    "observation-category' and coding.code='laboratory').exists()",

    # US Core Patient: must have identifier with system and value
    "Patient.identifier.where(system.exists() and value.exists()).exists()",

    # US Core Vital Signs: must have a numeric valueQuantity
    "Observation.value.ofType(Quantity).exists()",

    # US Core Condition: clinicalStatus is required
    "Condition.clinicalStatus.exists()",

    # MustSupport validation: check all MS elements are present
    "conformsTo('http://hl7.org/fhir/us/core/StructureDefinition/"
    "us-core-patient')"
]
```

**Key takeaway:** FHIR endpoints are predictable (`.well-known/smart-configuration`), authentication follows OAuth2 patterns, CCDA generation maps Composition sections to template OIDs, bulk export is async with NDJSON output, and US Core profile validation can be done server-side or client-side. Validate early — a resource that fails US Core conformance will break every downstream consumer.
