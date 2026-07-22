---
name: privacy-engineer
description: >-
  Privacy engineering for health platforms — BAA implementation with sub-processors (BAA checklist, sub-processor inventory, annual review, breach notification requirements), data minimization architecture (collection minimization, retention policies, purpose limitation enforcement, data flow mapping and data lineage), DSAR (Data Subject Access Request) automation (intake portal, identity verification, data discovery across systems, response generation, 30-day SLA tracking), consent management infrastructure (granular consent for treatment types, research, and marketing, consent withdrawal propagation, age verification, parental consent), audit logging (access logs for who viewed what PHI, change logs, purpose-of-access recording, tamper-proof storage, retention), patient data deletion workflows (hard delete vs soft delete, cascade deletion across systems, backup handling, third-party deletion propagation), privacy-by-design review process (privacy impact assessments PIA, data protection impact assessments DPIA, pre-launch privacy review checklist), de-identification (HIPAA Safe Harbor method, expert determination, re-identification risk assessment, k-anonymity and l-diversity), and cookie and tracking consent (GDPR cookie consent, CCPA opt-out, health data-specific tracking restrictions). Triggered by privacy engineering, DSAR, consent management, data minimization, audit logging, de-identification, HIPAA BAA, privacy by design, cookie consent.
author: Sandeep Kumar Penchala
type: security
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - privacy-engineering
  - dsar
  - consent-management
  - data-minimization
  - audit-logging
  - de-identification
  - hipaa-baa
  - privacy-by-design
token_budget: 8000
dependencies:
  tools: []
  packages: []
  permissions: []
output:
  type: "code"
  path_hint: "./"
chain:
  consumes_from: ["gdpr-privacy", "compliance-officer", "security-engineer", "backend-developer"]
  feeds_into: ["security-engineer", "backend-developer", "gdpr-privacy", "legal-advisor"]
---

# Privacy Engineer (Technical)

Implement privacy controls at the infrastructure, application, and data layers. This skill covers the technical implementation of privacy requirements — BAAs, data minimization, DSAR automation, consent management, audit logging, data deletion, privacy-by-design reviews, de-identification, and cookie consent. Privacy engineering is the bridge between legal requirements and working code. A privacy policy is aspirational; a privacy architecture is enforceable.

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

These rules apply to *every* response this skill produces. Privacy engineering decisions have compounding effects — a data retention mistake today becomes a DSAR nightmare in two years.

- **Never assume what data you have — always map first.** Before implementing any privacy control, you must know what data exists, where it lives, who accesses it, and why. Privacy controls built on assumptions about data inventory will miss critical data stores. Always start with a data flow mapping exercise.
- **Soft delete is not delete.** Marking a record `deleted = true` in a database is not deletion — it is a visibility filter. GDPR and CCPA define deletion as the irreversible destruction of data. If a database restore, log replay, or backup recovery can bring the data back, it has not been deleted. Always be precise about deletion semantics.
- **Consent is not a one-time checkbox.** Consent can be withdrawn at any time, and the withdrawal must be as easy as the grant. If consent was collected via a single checkbox, withdrawal must be a single click. Consent changes must propagate to all downstream systems that rely on that consent — a consent withdrawal that only updates the primary database but not the analytics pipeline is a violation.
- **De-identification is not a binary state.** There is no such thing as "fully anonymized" data — only data with varying degrees of re-identification risk. HIPAA Safe Harbor removes 18 identifiers, but combination with external datasets can still enable re-identification. Always describe de-identification in terms of risk level and the specific method applied, not as a guarantee.
- **Admit when the architecture makes a privacy requirement infeasible.** Some privacy requirements — "delete all copies of this user's data everywhere" — may be architecturally impossible without a full system rebuild. Be honest about what is achievable, what requires architectural changes, and what the residual risk is. Promising compliance that the infrastructure cannot deliver is worse than acknowledging the gap.

## Route the Request

<!-- QUICK: 30s — pick your path, skip the rest -->

```
What are you trying to do?
├── Implement a BAA with sub-processors → Jump to "Core Workflow — Phase 1 (BAA Implementation)"
├── Design data minimization architecture → Jump to "Core Workflow — Phase 2 (Data Minimization)"
├── Build DSAR automation → Jump to "Core Workflow — Phase 3 (DSAR Automation)"
├── Set up consent management infrastructure → Jump to "Core Workflow — Phase 4 (Consent Management)"
├── Implement audit logging → Jump to "Core Workflow — Phase 5 (Audit Logging)"
├── Design patient data deletion workflows → Jump to "Core Workflow — Phase 6 (Data Deletion)"
├── Run a privacy-by-design review → Jump to "Core Workflow — Phase 7 (Privacy-by-Design)"
├── De-identify a dataset → Jump to "Core Workflow — Phase 8 (De-identification)"
├── Implement cookie and tracking consent → Jump to "Core Workflow — Phase 9 (Cookie Consent)"
├── Need legal interpretation of GDPR/HIPAA → Invoke gdpr-privacy or legal-advisor skill instead
├── Need HIPAA compliance program design → Invoke compliance-officer skill instead
└── Not sure? → Start at "Core Workflow — Phase 1" and follow sequentially
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Decision Trees
<!-- STANDARD: 3min -->

### DSAR Response: Automated vs Manual vs Legal Review

```
DSAR received and identity verified → Determine response path:

├── Request type is "Access" or "Portability"?
│   ├── Data scope is account-level only (profile, preferences, basic activity)?
│   │   └── → Automated response. Fetch from primary database + search indexes.
│   │       Format per user's selection (JSON, PDF). Deliver via secure portal.
│   │
│   ├── Data scope includes clinical/PHI data?
│   │   └── → Automated discovery + manual review before release.
│   │       Verify: no third-party PHI in results, no data from other patients in
│   │       message threads, no clinical interpretations that could cause distress
│   │       if delivered without clinical context.
│   │
│   └── Data scope crosses 5+ systems or includes third-party sub-processor data?
│       └── → Automated discovery + legal review of third-party data sharing obligations.
│           Confirm sub-processor contracts allow sharing data back to data subject.
│
├── Request type is "Deletion" (Right to be Forgotten)?
│   ├── Data is non-clinical, consent was sole legal basis?
│   │   └── → Automated hard delete cascade. Verify across all systems within 30 days.
│   │
│   ├── Data includes clinical records within regulatory retention period?
│   │   └── → Manual review. Apply soft delete with compliance hold.
│   │       Notify requester: data restricted from processing but retained for
│   │       regulatory compliance period (specify period and legal basis).
│   │
│   └── Data is under active legal hold?
│       └── → Legal review. Do not delete. Notify requester that data is subject to
│           legal preservation obligation. Release hold → re-process deletion.
│
└── Request type is "Rectification" or "Restriction"?
    ├── Correction to factual data (name, contact, payment)?
    │   └── → Automated update with audit trail (before/after values).
    ├── Correction to clinical data (diagnosis, treatment, lab results)?
    │   └── → Manual review. Clinical data corrections may require provider verification.
    │       Do not alter clinical records without confirmation from originating provider.
    └── Restriction of processing?
        └── → Manual review. Flag data in all systems as "restricted" — retain but
            do not process. Add restriction metadata: reason, scope, expiration.
```

### Data Deletion: Hard Delete vs Soft Delete vs Archive

```
Deletion request validated → Choose deletion method:

├── Legal basis for processing has been withdrawn?
│   ├── Consent was sole legal basis and consent has been withdrawn?
│   │   └── → HARD DELETE. Data was only held by consent — no consent = no basis.
│   │       Cryptographic erasure (key deletion) or overwrite + TRIM.
│   │
│   └── Consent was one of multiple legal bases (e.g., legitimate interest + consent)?
│       └── → SOFT DELETE if legitimate interest still applies.
│           Restrict processing to the remaining legal basis. Update privacy notice.
│
├── Data is subject to regulatory retention obligation?
│   ├── HIPAA clinical records (< 6-7 years from last encounter)?
│   │   └── → SOFT DELETE. Mark as deleted, restrict access to compliance/legal roles.
│   │       Auto-purge when retention period expires.
│   │
│   ├── Financial/billing records (< 7 years)?
│   │   └── → SOFT DELETE. Retain for tax/audit purposes. Restricted access.
│   │
│   └── Retention period has expired?
│       └── → HARD DELETE. No basis for continued retention.
│
├── Data is under legal hold?
│   │   └── → ARCHIVE (freeze). Preserve data in current state. Do not modify or delete.
│   │       Resume deletion workflow when hold is released.
│   │
└── Data includes backups?
    └── → NOT IMMEDIATELY DELETABLE. Flag in deletion registry.
        Backups rotate out per retention schedule. Restore procedures must
        check deletion registry and exclude deleted users from restoration.
        Document: "Data will be fully purged from all systems by [backup rotation date]."
```

## When to Use

<!-- QUICK: 30s — scan the bullet list to decide if this skill fits -->

- Implementing Business Associate Agreements (BAAs) with technical sub-processors
- Designing data minimization architectures with collection, retention, and purpose limitation
- Building automated DSAR intake, verification, discovery, and response pipelines
- Setting up granular consent management with withdrawal propagation
- Implementing tamper-proof audit logging for PHI access
- Designing patient data deletion workflows across systems and backups
- Conducting privacy-by-design reviews (PIA, DPIA) before product launches
- Applying de-identification techniques (Safe Harbor, expert determination, k-anonymity)
- Implementing cookie and tracking consent (GDPR, CCPA, health-data restrictions)

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

<!-- CROSS-SKILL: Privacy engineering consumes and feeds multiple disciplines — use this table to route cross-cutting work -->

### Decision Gates

| When faced with this decision... | Invoke | Key Artifact |
|---|---|---|
| Need regulatory interpretation of DPIA, BAA, or retention rules | `compliance-officer` | BAA inventory, retention schedule, audit scope definition |
| GDPR consent/legitimate interest legal assessment needed | `gdpr-privacy` | DPIA template, LIA documentation, SCCs for cross-border transfers |
| Infrastructure security controls for privacy enforcement | `security-engineer` | Encryption key policies, IAM role definitions, WORM storage configurations |
| Legal hold or deletion request with conflicting obligations | `legal-advisor` | Legal hold notices, jurisdictional retention memos, chain-of-custody logs |
| New data pipeline creates new data flow | `data-engineer` | Data lineage diagrams, pipeline documentation, purpose gate configurations |
| Clinical data model affects retention or de-identification | `clinical-informatics-specialist` | FHIR resource definitions, clinical data dictionaries, consent-to-research mappings |

### Coordination Table

| Skill | Direction | When to Consume / Feed | Shared Artifacts |
|-------|----------|------------------------|------------------|
| `compliance-officer` | Consume | HIPAA compliance program requirements, regulatory interpretation, audit scope definition | BAA inventory, retention schedules, access review reports |
| `compliance-officer` | Feed | Technical evidence of controls (encryption, access logs, deletion certificates) for compliance audits and regulatory filings | Audit log exports, encryption verification reports, deletion certificates |
| `gdpr-privacy` | Consume | GDPR legal interpretation (legitimate interest assessments, DPIA thresholds, cross-border transfer mechanisms) | DPIA templates, SCC documentation, RoPA entries |
| `gdpr-privacy` | Feed | Technical implementation of GDPR requirements (consent plumbing, deletion pipelines, data portability exports) | Consent propagation logs, deletion verification reports, DSAR response artifacts |
| `security-engineer` | Consume | Infrastructure security controls (encryption standards, network segmentation, IAM policies) that privacy controls depend on | Encryption key policies, VPC configurations, IAM role definitions |
| `security-engineer` | Feed | Privacy-specific security requirements (PHI access audit logging, tamper-proof storage, PHI-in-log detection) | Audit log schemas, WORM storage configurations, log scanning rules |
| `legal-advisor` | Consume | Legal interpretation of deletion requests, legal hold scope, regulatory retention periods by jurisdiction | Legal hold notices, retention requirement memos, jurisdictional data maps |
| `legal-advisor` | Feed | Technical feasibility assessments for deletion requests, evidence of deletion for legal proceedings, data inventory for discovery | Deletion feasibility reports, chain-of-custody logs, data catalogs |
| `data-engineer` | Consume | Data pipeline architecture: where data flows, transformation points, ETL schedules — required for data flow mapping | Data lineage diagrams, pipeline documentation, data catalog entries |
| `data-engineer` | Feed | Privacy requirements for data pipelines: purpose limitation enforcement, retention automation, PHI filtering at ingestion | Purpose gate configurations, retention automation scripts, field-level encryption specs |
| `clinical-informatics-specialist` | Consume | Clinical data models, FHIR/HL7 schemas, clinical workflow requirements that affect data collection and retention | FHIR resource definitions, clinical data dictionaries, workflow diagrams |
| `clinical-informatics-specialist` | Feed | Privacy constraints on clinical data use: de-identification requirements for research, consent boundaries for secondary use | De-identified dataset specifications, consent-to-research mappings, data use agreements |

**Coordination Protocol:**
1. Privacy requirements that require legal interpretation → file a request with `compliance-officer` or `gdpr-privacy` (include specific technical context, not open-ended "is this GDPR compliant?")
2. Privacy controls that depend on infrastructure → file a `security-engineer` request with the specific control needed (e.g., "need WORM storage for audit logs with Compliance mode and 6-year retention")
3. New data pipelines or ETL jobs → notify `data-engineer` to register in data catalog BEFORE data flows (retroactive data flow mapping is 10x harder)
4. Legal holds or deletion requests that conflict → escalate to `legal-advisor` with both requirements documented; do not independently resolve conflicts between legal obligations

## Core Workflow
<!-- STANDARD: 3min -->

### Phase 1 — BAA Implementation with Sub-Processors

**Goal:** Ensure every sub-processor handling PHI has a valid, current BAA and meets technical and organizational security requirements.

**BAA Checklist (per sub-processor):**

```
□ BAA executed and signed by both parties (not just clickwrap — documented signature)
□ Sub-processor's SOC 2 Type II or ISO 27001 certification reviewed and current
□ Sub-processor's encryption standards verified: AES-256 at rest, TLS 1.2+ in transit
□ Sub-processor's breach notification timeline confirmed: ≤ 72 hours from discovery
□ Sub-processor's data center locations documented (must not process PHI in prohibited jurisdictions)
□ Sub-processor's sub-sub-processors disclosed and reviewed
□ Data flow diagram for PHI to/from sub-processor documented
□ Minimum necessary PHI fields sent to sub-processor confirmed (data minimization check)
□ Sub-processor's data deletion process verified: 30-day post-termination deletion with certificate
□ Sub-processor's access control model reviewed: RBAC, MFA required, no shared accounts
```

**Sub-Processor Inventory:**
- Centralized registry with fields: sub-processor name, service provided, PHI categories processed, BAA effective date, BAA expiration/review date, data center locations, certification status, risk tier
- Annual review schedule with 90-day, 60-day, and 30-day reminders before BAA expiration
- Risk tier classification: Tier 1 (core clinical data), Tier 2 (supporting data), Tier 3 (ancillary data)

**Breach Notification Requirements:**
- Contractual requirement: sub-processor must notify within 72 hours of discovering a breach
- Notification must include: nature of breach, PHI categories affected, number of individuals affected, remediation actions taken, timeline of events
- Automated monitoring: sub-processor status pages and security bulletins monitored for undisclosed incidents
- Breach simulation: annual tabletop exercise with each Tier 1 sub-processor

### Phase 2 — Data Minimization Architecture

**Goal:** Design systems that collect only necessary data, retain it only as long as needed, and enforce purpose limitations at the technical level.

**Collection Minimization:**
- Field-level justification: every data field collected must have a documented purpose, legal basis, and retention period
- Collection review trigger: new feature PRD must include a "Data Collection Impact" section reviewed by privacy engineering
- Pre-collection filtering: API validation that rejects fields not in the approved schema for that endpoint — do not accept and then filter
- Progressive collection: collect minimal data at registration, request additional data only when needed for specific features

**Retention Policies:**

```
Retention Schedule Example (health platform):
  Clinical records (PHI):                    7 years from last encounter (or state law, whichever longer)
  Account data (email, username):            3 years after account closure
  Audit logs (access, change):               6 years (HIPAA minimum)
  Consent records:                           Duration of processing + 3 years after withdrawal
  Support tickets:                           3 years after resolution
  Analytics events (de-identified):          26 months (GDPR best practice for analytics)
  Marketing consent:                         2 years after last engagement
  Server/application logs (with PHI):        90 days (minimize PHI in logs)
  Backups:                                   30 days (aligned with retention policy, not extended)
```

**Purpose Limitation Enforcement:**
- Data tagging: tag every data store with permitted purposes (treatment, payment, operations, research, marketing)
- Purpose gate: API middleware that checks the purpose of the requesting service against the data store's permitted purposes
- Cross-purpose access requires documented exception approval with expiration (30-day max, renewable with review)
- Regular purpose audit: scan access patterns for purpose drift (e.g., marketing team accessing treatment data)

**Data Flow Mapping (Data Lineage):**
- Automated discovery: scan infrastructure for data stores (databases, object storage, caches, queues, logs)
- Data flow diagrams: document movement of PHI between systems with transfer method and encryption
- Data lineage tracking: for each PHI field, trace origin → transformations → destinations
- Change detection: alert when new data flows are detected (new database connection, new ETL job)

### Phase 3 — DSAR (Data Subject Access Request) Automation

**Goal:** Build an automated pipeline for handling data subject access requests with identity verification, data discovery, response generation, and SLA tracking.

**DSAR Intake Portal:**
- Self-service request form: request type (access, deletion, rectification, portability, restriction), data categories of interest, preferred response format
- Identity verification integrated into the form (see below)
- Request confirmation with tracking ID and expected response date
- Accessibility: WCAG 2.2 AA compliant, available in all supported languages

**Identity Verification:**
- Tiered verification based on data sensitivity:
  - Tier 1 (basic account data): email verification + logged-in session
  - Tier 2 (profile data): email + SMS OTP
  - Tier 3 (PHI, clinical data): email + SMS OTP + knowledge-based verification (account creation date, last login location) + government ID upload (if knowledge-based fails)
- Verification must complete before data discovery begins (do not search for data without verifying identity)
- Failed verification: 3 attempts → manual review; no data returned on failed verification

**Data Discovery Across Systems:**

```
DSAR Data Discovery Pipeline:
  1. Parse request → determine data categories requested
  2. Query data catalog → identify all systems containing requested data categories
  3. Dispatch discovery queries in parallel:
     ├── Primary database (user profile, account, preferences)
     ├── Clinical data store (conditions, treatments, medications)
     ├── Messaging system (DMs, group posts, comments)
     ├── Support ticket system
     ├── Analytics data warehouse
     ├── Search indexes (Elasticsearch/OpenSearch)
     ├── Object storage (uploaded images, documents)
     ├── Audit logs (access and change history for user's data)
     └── Third-party sub-processors (via API)
  4. Aggregate results → deduplicate → format per response specification
```

**Response Generation:**
- Format options: machine-readable JSON, human-readable PDF, portable format for data portability requests
- Response structure: data categories as sections, each with data values, source system, collection date, purpose, and retention period
- PII/PHI redaction: redact data of other individuals that appears in the requester's data (e.g., other participants in a group chat)
- Delivery: secure portal download (not email — PHI in email is a breach risk), access expires after 30 days

**30-Day SLA Tracking:**
- SLA clock starts at identity verification completion (not request submission)
- Automated reminders: 7-day warning, 3-day warning, 1-day warning, overdue escalation
- Extension tracking: 30-day extension available with documented reason (GDPR allows 2-month extension for complex requests)
- SLA dashboard: open requests, average response time, overdue count, extension rate

### Phase 4 — Consent Management Infrastructure

**Goal:** Implement granular consent collection and withdrawal propagation across all systems that rely on consent as a legal basis.

**Granular Consent Model:**

```
Consent Categories:
  Treatment (Essential)
  ├── Core platform functionality
  ├── PHI processing for care coordination
  └── Cannot be withdrawn while account is active

  Research (Optional)
  ├── De-identified data for internal research
  ├── Identifiable data for clinical research
  └── Third-party research collaboration

  Marketing (Optional)
  ├── Product updates and newsletters
  ├── Partner offers and promotions
  └── Behavioral advertising

  Communication (Optional)
  ├── Appointment reminders
  ├── Health tips and educational content
  └── Community engagement notifications
```

**Consent Withdrawal Propagation:**

```
Propagation Pipeline:
  1. User withdraws consent for category X
  2. Update consent record in primary consent store (timestamp, withdrawal method)
  3. Publish consent change event to message bus
  4. All downstream consumers process event:
     ├── Analytics pipeline → stop processing data for category X
     ├── Marketing automation → remove from all campaigns using category X
     ├── Data warehouse → flag data collected under category X for deletion
     ├── Third-party integrations → API call to delete/stop processing
     └── Research databases → flag for exclusion from new studies
  5. Confirmation: each consumer acknowledges processing
  6. Reconciliation: verify all consumers confirmed within 24 hours
  7. Alert on failure: if any consumer fails to acknowledge, escalate
```

**Age Verification:**
- Self-declared age at registration (with clear statement: "You must be [minimum age] to use this service")
- If self-declared age is < 13 (or local digital age of consent): block registration, provide parent/guardian onboarding flow
- Parental consent: verifiable parental consent mechanism (small-dollar credit card charge + void, government ID + video verification, signed consent form)
- Age gating on sensitive features: re-verify age before accessing features with higher risk (direct messaging, video upload)

### Phase 5 — Audit Logging

**Goal:** Implement tamper-proof audit logging that records who accessed what PHI, when, why, and from where.

**Access Logs (PHI Access Monitoring):**

```
Access Log Schema:
  {
    event_id: UUID,
    timestamp: ISO 8601 with timezone (NTP-synchronized),
    actor: {
      user_id: string,
      role: string,
      session_id: string
    },
    action: "view" | "create" | "update" | "delete" | "export" | "download",
    resource: {
      type: "patient_record" | "clinical_note" | "lab_result" | "prescription",
      id: string,
      patient_id: string
    },
    purpose: "treatment" | "payment" | "operations" | "research" | "legal",
    context: {
      ip_address: string,
      user_agent: string,
      device_fingerprint_hash: string
    },
    result: "success" | "denied" | "error"
  }
```

**Change Logs:**
- Record before/after values for every PHI field modification
- Include: who made the change, when, from what old value to what new value, source system
- Immutable: change logs must be append-only — no updates or deletes to log entries

**Purpose-of-Access Recording:**
- Require purpose selection for every PHI access (dropdown: treatment, payment, operations, research, legal)
- Break-glass access: emergency access without purpose selection is allowed but triggers immediate review
- Purpose mismatch alert: if a user's access pattern doesn't match their role (e.g., billing staff accessing clinical notes)

**Tamper-Proof Storage:**
- Write to append-only storage: blockchain-based or WORM (S3 Object Lock with Compliance mode)
- Cryptographic chaining: each log entry includes hash of previous entry (Merkle tree structure for integrity verification)
- Separate storage: audit logs in a separate AWS account/GCP project with different access controls
- Immutability verification: automated daily scan to verify log integrity (recompute hashes, detect gaps)

**Retention:**
- HIPAA minimum: 6 years for audit logs containing PHI access records
- State law may require longer (check jurisdiction)
- Automated purging after retention period with deletion certification

### Phase 6 — Patient Data Deletion Workflows

**Goal:** Implement deletion workflows that satisfy regulatory requirements (GDPR right to erasure, CCPA deletion requests, HIPAA accounting of disclosures) and actually remove data from all systems.

**Hard Delete vs. Soft Delete:**

```
Decision Matrix:
  Hard Delete (irreversible destruction):
    ├── User requests account deletion (GDPR/CCPA right)
    ├── Consent withdrawal where consent was sole legal basis
    ├── Data collected beyond retention period
    └── Method: cryptographic erasure (key deletion) or overwrite with zeros + TRIM

  Soft Delete (retained for compliance):
    ├── Clinical records within HIPAA retention period (6-7 years)
    ├── Financial records (tax, billing — 7+ years)
    ├── Audit logs (6 years minimum)
    ├── Legal hold data (until hold is released)
    └── Method: flag as deleted, restrict access to compliance/legal roles only
```

**Cascade Deletion Across Systems:**

```
Cascade Deletion Pipeline:
  1. Initiation: deletion request validated and approved
  2. Primary store: hard/soft delete in primary database
  3. Cascade to dependent systems (ordered):
     ├── Search indexes: delete document from Elasticsearch/OpenSearch
     ├── Cache layers: invalidate cached user data (Redis, Memcached)
     ├── Object storage: delete uploaded files (S3 with versioning — delete all versions)
     ├── Analytics warehouse: delete/redact user data in data warehouse
     ├── Message queues: purge any queued messages containing user data
     ├── CDN/logs: purge edge caches and CDN-stored content
     └── Third-party sub-processors: API-driven deletion requests
  4. Verification: query each system to confirm data is no longer accessible
  5. Deletion certificate: generate certificate with: user ID, deletion date, systems verified, method used
```

**Backup Handling:**
- Backup exclusion: flag deleted users in deletion registry; restore procedures must check registry and skip deleted users
- Backup rotation: retention policies must align — when backups rotate out, deleted data is permanently gone
- Backup restoration test: quarterly test to verify that deleted user data is not restorable
- Restore-then-delete: if a backup containing deleted user data must be restored (disaster recovery), re-execute deletion on restored data

**Third-Party Deletion Propagation:**
- Contractual requirement: sub-processors must delete data within 30 days of request
- Deletion API: sub-processors must provide a deletion API (not "email us to delete")
- Deletion verification: request deletion confirmation certificate from sub-processor
- Deletion audit: annual audit of sub-processor deletion compliance (spot-check deleted user IDs)

### Phase 7 — Privacy-by-Design Review Process

**Goal:** Embed privacy review into the product development lifecycle so that privacy issues are identified before code is written, not after data is collected.

**Privacy Impact Assessment (PIA):**

```
PIA Trigger Criteria (any one triggers a PIA):
  □ New collection of PHI or personal data
  □ New data sharing with third parties
  □ New use of existing data for a different purpose
  □ New technology with privacy implications (biometrics, AI/ML, location tracking)
  □ Processing of sensitive data (health, children's data, biometric, financial)
  □ Processing at scale (> 10,000 individuals)

PIA Sections:
  1. Project description and data flow summary
  2. Data inventory: what data, from whom, for what purpose, legal basis
  3. Privacy risks identified (use STRIDE-Privacy: Linkability, Identifiability,
     Non-repudiation, Detectability, Information disclosure, Unawareness, Non-compliance)
  4. Risk mitigation measures for each identified risk
  5. Residual risk assessment after mitigation
  6. Stakeholder sign-off: product manager, privacy engineer, legal, DPO
```

**Data Protection Impact Assessment (DPIA):**
- Required under GDPR Article 35 for high-risk processing
- Additional sections beyond PIA: necessity and proportionality assessment, data subject rights impact, consultation with DPO, prior consultation with supervisory authority (if residual risk is high)
- DPIA must be reviewed and updated when processing changes significantly

**Pre-Launch Privacy Review Checklist:**

```
Pre-Launch Privacy Review:
  □ Data inventory updated with new data elements
  □ Legal basis for each data element documented
  □ Consent flow reviewed (if consent-based): granular, withdrawable, not pre-checked
  □ Data retention periods defined for all new data
  □ Data minimization verified: no unnecessary fields collected
  □ Encryption verified: TLS 1.2+ in transit, AES-256 at rest
  □ Access controls: least privilege, role-based, MFA required for PHI access
  □ Audit logging: all PHI access events logged with purpose
  □ DSAR capability: new data discoverable and retrievable via DSAR pipeline
  □ Deletion capability: new data included in cascade deletion workflows
  □ Third-party review: any new sub-processors have valid BAA
  □ Cookie/tracking: new cookies categorized and consent-gated
  □ Privacy notice updated to reflect new processing
  □ DPO approval obtained (if required)
  └── Launch gate: ALL items must be checked; no exceptions
```

### Phase 8 — De-identification

**Goal:** Apply de-identification techniques that satisfy regulatory standards while preserving data utility for research and analytics.

**HIPAA Safe Harbor Method (18 Identifiers to Remove):**

```
Safe Harbor Checklist:
  □ 1. Names
  □ 2. Geographic subdivisions smaller than state (except first 3 digits of ZIP if > 20,000 people)
  □ 3. Dates directly related to individual (except year): birth, admission, discharge, death
  □ 4. Telephone numbers
  □ 5. Fax numbers
  □ 6. Email addresses
  □ 7. Social Security numbers
  □ 8. Medical record numbers
  □ 9. Health plan beneficiary numbers
  □ 10. Account numbers
  □ 11. Certificate/license numbers
  □ 12. Vehicle identifiers and serial numbers
  □ 13. Device identifiers and serial numbers
  □ 14. Web URLs
  □ 15. IP addresses
  □ 16. Biometric identifiers
  □ 17. Full-face photographs and comparable images
  □ 18. Any other unique identifying number, characteristic, or code
```

**Expert Determination Method:**
- A qualified statistician determines that the risk of re-identification is "very small"
- Must document: methods used, justification for the "very small" determination, qualifications of the expert
- Higher data utility than Safe Harbor (keeps more data) but requires expert involvement

**Re-identification Risk Assessment:**
- Prosecutor risk: probability that a specific individual is in the dataset and can be identified
- Journalist risk: probability that ANY individual in the dataset can be identified
- Marketer risk: probability that the dataset can be linked to external datasets at scale
- Risk threshold: re-identification probability < 0.05 (5%) is commonly accepted

**k-Anonymity and l-Diversity:**

```
k-Anonymity:
  For each combination of quasi-identifiers (age, ZIP, gender),
  at least k individuals share the same combination.
  - k=5 means every combination appears at least 5 times
  - Higher k = more privacy, less utility
  - Limitation: does not protect against homogeneity attacks

l-Diversity:
  For each k-anonymous group, at least l "well-represented" values
  exist for each sensitive attribute.
  - l=3 means at least 3 different values for each sensitive field per group
  - Addresses the homogeneity attack limitation of k-anonymity
  - Distinct l-diversity: at least l distinct values
  - Entropy l-diversity: entropy of sensitive values > log(l)
```

### Phase 9 — Cookie and Tracking Consent

**Goal:** Implement cookie consent mechanisms that comply with GDPR, CCPA, and health data-specific restrictions.

**GDPR Cookie Consent:**
- Consent required BEFORE non-essential cookies are set (no "implied consent" or "by using this site you agree")
- Cookie categories: Necessary (always on), Preferences, Statistics, Marketing
- Granular consent: users must be able to accept/reject by category, not just all-or-nothing
- Consent proof: store consent record with timestamp, cookie categories accepted, consent method, IP address
- Consent renewal: re-prompt every 12 months or when cookie usage changes materially
- Cookie wall prohibited: cannot block access to content if user rejects non-essential cookies

**CCPA Opt-Out:**
- "Do Not Sell or Share My Personal Information" link on every page
- Global Privacy Control (GPC) signal must be honored as opt-out
- Opt-out must be processed within 15 business days
- No dark patterns: "Accept All" and "Reject All" must be equally prominent

**Health Data-Specific Tracking Restrictions:**
- No retargeting based on health conditions (e.g., "person viewed diabetes content")
- No lookalike audiences built from health condition data
- No tracking pixels on pages displaying PHI (appointment details, lab results, clinical notes)
- Session replay tools must block recording of pages with PHI
- Analytics on PHI-containing pages: server-side only, no client-side tracking, no full URL capture

## Best Practices
<!-- DEEP: 10+min -->

<!-- BEST PRACTICES: Privacy engineering patterns that prevent the most common failures -->

1. **Data Flow Mapping Before Any Privacy Control.** You cannot protect data you don't know you have. Before implementing any privacy control — access logging, deletion, DSAR — complete a data flow mapping exercise. Identify every system that stores, processes, or transmits PHI. Document the data lineage: origin → transformations → destinations. Automate change detection so new data flows don't go unnoticed. A privacy control built on incomplete data inventory is a compliance gap waiting to be discovered in an audit.

2. **Consent Propagation as Event-Driven Architecture.** Consent is not a database field — it's a distributed state. When a user withdraws consent for a category, every system that relied on that consent must stop processing within a configured timeframe. Design consent changes as events published to a message bus with guaranteed delivery. Every downstream consumer must acknowledge processing. Implement reconciliation: verify all consumers confirmed within 24 hours. A consent withdrawal that updates the primary database but not the analytics pipeline is a violation.

3. **Audit Log Immutability by Design, Not by Policy.** Audit logs must be tamper-proof at the infrastructure level, not just by access control policy. Use WORM storage (S3 Object Lock with Compliance mode), cryptographic chaining (each entry hashes the previous), and separate AWS accounts/GCP projects for log storage. Automated daily integrity verification. If a single admin with database access can modify audit logs, the logs are not forensically sound.

4. **DSAR Automation with Human Review Gates.** Automate the heavy lifting — identity verification, data discovery across systems, response formatting — but insert a human review gate before releasing data that includes PHI or third-party information. A DSAR response that accidentally includes another patient's data in a group chat export is a breach. The automation should flag: (a) content containing other individuals' data, (b) clinical information that may cause distress without clinical context, and (c) data from third-party sub-processors that may have contractual sharing restrictions.

5. **BAA Management as a Living Inventory, Not a Filing Cabinet.** BAAs expire, sub-processors add sub-sub-processors, certifications lapse. Maintain a centralized sub-processor inventory with automated reminders at 90, 60, and 30 days before BAA expiration. Annual review of every sub-processor's SOC 2/ISO 27001 status. Risk-tier classification (Tier 1: core clinical, Tier 2: supporting, Tier 3: ancillary) to prioritize review depth. A BAA that expired 18 months ago but nobody noticed is a compliance finding.

6. **Privacy-by-Design Review in CI/CD, Not as a Pre-Launch Panic.** Integrate privacy review into the development pipeline, not as a gate that blocks launch. Every PRD includes a "Data Collection Impact" section. PIAs are triggered automatically when new PHI fields, new third-party data sharing, or new processing purposes are detected. The pre-launch checklist is the final verification that all gates passed, not the first time anyone thinks about privacy. Privacy review that happens only at launch is too late — the architecture is already fixed.

7. **Cookie Consent UX Optimized for Both Compliance and Performance.** Do not load third-party tracking scripts before consent. Use a tag manager that respects consent signals — scripts in the "Marketing" category must not fire until consent is granted. The consent banner must load synchronously (render-blocking for non-essential scripts). Measure the performance impact: consent management should add < 100ms to page load. A consent banner that's legally compliant but adds 2 seconds to page load will drive users to reject all cookies out of frustration, not informed choice.

8. **Right-to-Be-Forgotten Cascade Testing.** The deletion pipeline is only as strong as its weakest link. Test cascade deletion end-to-end quarterly: submit a test deletion, then verify the data is gone from the primary database, search indexes, caches, object storage, analytics warehouse, CDN, and all third-party sub-processors. Then test backup restoration: restore from the most recent backup and confirm the deleted user's data is excluded. The test should fail if any system still returns the user's data. A deletion pipeline that works in theory but breaks in practice is a regulatory liability.

## Error Decoder
<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| A health platform received a GDPR deletion request and executed a thorough cascade delete across all live systems: primary database, search indexes, analytics warehouse, third-party sub-processors. The deletion certificate was issued. Eighteen months later, a database corruption incident required restoring from backups. The restored backup contained the deleted user's full clinical record — which was then re-indexed into the search system and became queryable again. | The backup rotation policy was 36 months, but the team assumed backups "aged out" after 90 days. The deletion registry existed but the restore procedure didn't check it. The deletion certificate was issued based on live-system verification only. | Investigate the failure mode, document the root cause, update privacy controls, and deploy corrective monitoring. Re-train team on the identified gap. | Backups are part of the deletion scope. Flag deleted users in a deletion registry and enforce that ALL restore procedures check the registry and skip deleted users. Extend retention for the deletion registry to match the longest backup retention period. Test backup restoration quarterly with deleted user IDs. |
| A user withdrew consent for marketing data processing. The consent management system updated the primary consent store and published a consent change event. The analytics pipeline subscribed to consent events but had a bug: it only processed "consent_granted" events, silently dropping "consent_withdrawn" events. For 14 months, the user's behavioral data continued flowing into marketing segmentation and ad targeting — a clear GDPR violation. | The consent propagation pipeline had no reconciliation mechanism. There was no verification that every consumer acknowledged processing the withdrawal event. The bug was discovered during a GDPR audit, not through internal monitoring. | Investigate the failure mode, document the root cause, update privacy controls, and deploy corrective monitoring. Re-train team on the identified gap. | Every consent propagation pipeline needs reconciliation — verify that all consumers confirmed processing within a defined window (24 hours). Alert on any consumer that fails to acknowledge. Test consent withdrawal end-to-end at least monthly: withdraw consent for a test user and verify the user is excluded from every downstream system's processing. |
| A patient submitted a DSAR requesting all their data. The privacy team started a manual discovery process: emailing each system owner asking "do you have data for user X?" System owners took days to respond, some were on vacation, some systems had no clear owner. The 30-day GDPR SLA was missed by 15 days. The supervisory authority was notified and opened an investigation. | There was no data catalog. No automated discovery. The DSAR process relied on humans knowing what systems existed and who owned them — institutional knowledge that changed when people left. | Investigate the failure mode, document the root cause, update privacy controls, and deploy corrective monitoring. Re-train team on the identified gap. | DSAR automation starts with a data catalog. Every system that stores user data must be registered with: data categories stored, API for querying user data, and system owner. The DSAR pipeline queries all registered systems in parallel. A system not in the catalog doesn't exist for DSAR purposes — which is a violation waiting to happen. |
| A health platform published a de-identified dataset for research, applying HIPAA Safe Harbor (removing all 18 identifiers). A researcher cross-referenced the dataset with public voter registration records using ZIP code + date of birth + gender and re-identified 87% of the individuals. The dataset included sensitive diagnoses including HIV status, mental health conditions, and substance use disorder. | Safe Harbor removes ZIP codes smaller than 20,000 people but the dataset used 5-digit ZIP codes for urban areas where even a single ZIP can contain 50,000+ people. Combined with DOB and gender, this trio is a quasi-identifier that uniquely identifies 87% of the US population. The re-identification risk assessment was not performed. | Investigate the failure mode, document the root cause, update privacy controls, and deploy corrective monitoring. Re-train team on the identified gap. | Safe Harbor is a minimum, not a guarantee. Always perform a re-identification risk assessment using the specific dataset and available external datasets. Apply k-anonymity at minimum (k ≥ 5 for each quasi-identifier combination). For sensitive health data, k ≥ 11 is recommended. Consider differential privacy for high-risk datasets. |
| A health platform used a third-party error monitoring service (Sentry/Datadog) to track application errors. A bug in the appointment scheduling feature caused patient names, dates of birth, and appointment reasons to appear in error stack traces — which were sent to the third-party service. The third-party service had no BAA. The error logs were indexed and searchable by the third-party's support team. | Error logging was not included in the data flow mapping. The team assumed error logs only contained technical information. No PHI scanning was applied to outbound log streams. The third-party monitoring service was treated as infrastructure, not as a sub-processor. | Investigate the failure mode, document the root cause, update privacy controls, and deploy corrective monitoring. Re-train team on the identified gap. | All outbound data flows are potential PHI leaks. Scan error logs, debug output, and monitoring data for PHI patterns before they leave the environment. Every third-party service that receives data from your systems — even error logs — needs a BAA if PHI could appear. Redact PHI at the application level before it reaches the logging framework. |

## Production Checklist
<!-- STANDARD: 3min -->

<!-- CHECKLIST: PE1-PE14 reference IDs for Privacy Engineering production readiness -->

- **PE1** — BAA checklist completed for all sub-processors handling PHI; sub-processor inventory current and reviewed within last 12 months
- **PE2** — Sub-processor breach notification pipeline tested: 72-hour detection-to-notification flow verified
- **PE3** — Data minimization: field-level justification documented for all PHI fields; collection review trigger integrated into feature launch process
- **PE4** — Retention policies defined and enforced: automated purging operational for all data categories with retention periods
- **PE5** — Data flow mapping complete: all PHI flows documented, automated change detection operational
- **PE6** — DSAR automation: intake portal, identity verification, data discovery, response generation, and SLA tracking operational for all data categories
- **PE7** — Consent management: granular consent collection deployed, withdrawal propagation pipeline tested across all downstream systems
- **PE8** — Audit logging: access logs, change logs, purpose-of-access recording operational; tamper-proof storage validated; integrity verification automated
- **PE9** — Data deletion: cascade deletion pipeline tested end-to-end; backup exclusion verified; third-party deletion propagation confirmed
- **PE10** — Privacy-by-design: PIA/DPIA process integrated into SDLC; pre-launch privacy review checklist enforced as launch gate
- **PE11** — De-identification: Safe Harbor or expert determination method applied to analytics datasets; re-identification risk assessment completed
- **PE12** — Cookie consent: GDPR-compliant consent banner deployed; granular category selection functional; consent proof stored
- **PE13** — CCPA opt-out: "Do Not Sell or Share" link on all pages; GPC signal honored; opt-out processed within 15 business days
- **PE14** — Health data tracking restrictions: no retargeting on health conditions; no tracking pixels on PHI pages; session replay PHI blocking verified

## Scale Depth
<!-- DEEP: 10+min -->

<!-- SCALE: How privacy engineering evolves as the organization grows -->

### Solo Developer / Early-Stage Startup (1-5 engineers, < 1,000 users)
- Data inventory: a shared document listing the 2-3 databases and services in use
- BAAs: PDF files in a shared drive, annual review is a calendar reminder
- DSAR: manual — privacy contact email, manual database queries, no SLA tracking
- Consent: a single checkbox at registration, no granular categories, no propagation
- Audit logging: application-level logging to stdout, no tamper-proofing
- Deletion: manual SQL DELETE, no cascade, no backup handling
- Privacy review: "does this feel creepy?" gut check before launch
- De-identification: remove names and emails, call it anonymous
- **Key risk:** Everything is manual. One DSAR can consume a day of engineering time. Privacy posture is entirely dependent on the founding team's good intentions.

### Single Product / Small Team (5-20 engineers, 1,000-100,000 users)
- Data inventory: automated discovery script that scans infrastructure, still manually updated
- BAAs: centralized registry in a project management tool, quarterly review reminders
- DSAR: basic automation — intake form + automated primary database query, manual for other systems
- Consent: granular categories (essential, marketing, research), withdrawal updates primary store
- Audit logging: structured logs to separate storage, but still updatable by admins
- Deletion: scripted cascade across known systems, backup handling via deletion registry
- Privacy review: PIA template completed before launch, reviewed by tech lead (not privacy specialist)
- De-identification: Safe Harbor applied manually to analytics exports
- **Key risk:** Privacy is still a part-time responsibility. The engineer doing privacy is also doing feature work. Incomplete data inventory leads to missed systems in DSAR/deletion.

### Multi-Product Platform (20-100 engineers, 100,000-10M users)
- Dedicated privacy engineer (or small privacy engineering team)
- Data inventory: automated discovery + change detection, data catalog with ownership metadata
- BAAs: automated renewal tracking with 90/60/30-day reminders, risk-tiered sub-processor inventory
- DSAR: fully automated pipeline — intake, identity verification, discovery across all systems, response generation
- Consent: event-driven propagation with reconciliation, 24-hour confirmation window, alerting on failure
- Audit logging: WORM storage, cryptographic chaining, automated integrity verification, separate access control
- Deletion: automated cascade across all registered systems, backup exclusion verified, third-party deletion API integration
- Privacy review: PIA/DPIA integrated into SDLC, privacy gate in CI/CD, dedicated privacy review for high-risk features
- De-identification: automated Safe Harbor + k-anonymity assessment, re-identification risk scoring
- **Key risk:** System complexity outpaces privacy automation. New microservices, data pipelines, and third-party integrations are added faster than the privacy catalog is updated.

### Enterprise with Subsidiaries (100+ engineers, 10M+ users)
- Privacy engineering team with specialists (DSAR, consent, de-identification, privacy infrastructure)
- Data inventory: real-time data flow mapping with automated PHI classification and lineage tracking
- BAAs: automated sub-processor risk scoring, continuous certification monitoring, automated breach notification testing
- DSAR: multi-jurisdiction DSAR handling with jurisdiction-specific response templates and legal review routing
- Consent: global consent management with jurisdiction-specific consent models, cross-border transfer controls
- Audit logging: blockchain-verified audit trails, real-time anomaly detection on access patterns, AI-assisted purpose mismatch detection
- Deletion: zero-touch deletion with automated cascade verification, sub-processor deletion audit, backup purge certification
- Privacy review: privacy engineering embedded in every product team, automated PIA triggers from feature flags, privacy budget enforcement
- De-identification: differential privacy for analytics, synthetic data generation for testing, formal re-identification risk assessment with expert determination
- **Key risk:** Regulatory fragmentation across jurisdictions. Privacy requirements in the EU, US (state-by-state), Brazil, India, and others may conflict. Need jurisdiction-specific privacy policy overlays with conflict resolution mechanisms.

## What Good Looks Like
<!-- STANDARD: 3min -->

<!-- OUTCOME: The north star for privacy engineering in health platforms -->

- **Privacy is a feature, not a checkbox.** Users see clear, granular consent options in plain language — not a wall of legalese. They can access, download, and delete their data through self-service tools that work in seconds, not weeks. Privacy controls are visible and build trust, not hidden in settings menus.

- **DSARs are boring.** A data subject request is a routine automated operation that completes within days, not a fire drill that consumes the engineering team. The pipeline handles identity verification, data discovery, third-party coordination, and response generation without manual intervention. The SLA dashboard shows 99%+ on-time completion.

- **Deletion actually deletes.** When a user requests deletion, the cascade pipeline verifiably removes data from every system — primary databases, search indexes, caches, object storage, analytics warehouses, and all sub-processors. Backup restoration procedures exclude deleted users. Quarterly tests confirm that deleted data stays deleted.

- **Audit logs are court-ready.** Access logs are tamper-proof, cryptographically chained, and stored with integrity verification. When a regulator or plaintiff asks "who accessed this patient's record?", the answer is precise, complete, and verifiable. The logs demonstrate a culture of accountability, not a scramble to assemble evidence.

- **Privacy review catches issues before code is written.** The PIA/DPIA process is integrated into the SDLC — privacy risks are identified in the design phase, not the launch checklist. Engineers understand the privacy implications of their architectural choices because privacy engineering has educated the organization, not policed it.

- **Regulators see a mature privacy program, not a reactive scramble.** When a supervisory authority asks for evidence of compliance, the platform produces automated reports: data inventory, retention schedules, DSAR metrics, consent propagation verification, deletion certificates. The audit is a demonstration of operational controls, not a project to create documentation.

## Sub-Skills

<!-- QUICK: lookup specialized workflows -->

### baa-implementation

BAA checklist, sub-processor inventory, annual review, breach notification requirements. See Phase 1.

### data-minimization

Collection minimization, retention policies, purpose limitation enforcement, data flow mapping and lineage. See Phase 2.

### dsar-automation

Intake portal, identity verification, data discovery, response generation, 30-day SLA tracking. See Phase 3.

### consent-management

Granular consent categories, withdrawal propagation, age verification, parental consent. See Phase 4.

### audit-logging

Access logs, change logs, purpose-of-access recording, tamper-proof storage, retention. See Phase 5.

### data-deletion

Hard delete vs soft delete, cascade deletion, backup handling, third-party deletion propagation. See Phase 6.

### privacy-by-design

PIA, DPIA, pre-launch privacy review checklist, stakeholder sign-off. See Phase 7.

### de-identification

Safe Harbor method, expert determination, re-identification risk assessment, k-anonymity, l-diversity. See Phase 8.

### cookie-consent

GDPR cookie consent, CCPA opt-out, health data tracking restrictions. See Phase 9.
