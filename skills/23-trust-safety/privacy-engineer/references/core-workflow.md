# Core Workflow — Full Implementation

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
