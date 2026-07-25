## Core Workflow

<!-- QUICK: 30s — scan phase titles to understand the process -->
<!-- DEEP: 10+min -->

### Phase 1 (~20 min): HITRUST CSF Scoping and Control Mapping

1. Determine HITRUST assessment type: e1 (essentials, 44 controls), i1 (implemented, 182 controls), or r2 (risk-based, validated assessment with ~300-500 controls depending on scoping factors).
2. Define organizational, system, and regulatory scoping factors: HIPAA, HITECH, state breach notification laws, FDA cybersecurity requirements.
3. Map HIPAA Security Rule controls (45 CFR § 164.308-312) to HITRUST CSF control categories: Administrative Safeguards → 0x policies/procedures, Physical Safeguards → 0x facility controls, Technical Safeguards → 0x technical controls.
4. Identify gaps: controls not implemented, partially implemented, or implemented but not documented. HITRUST requires documented evidence, not just operational controls.
5. Create remediation roadmap: prioritize by HITRUST maturity scoring (Policy → Procedure → Implemented → Measured → Managed) and regulatory risk.

### Phase 2 (~15 min): PHI Data Flow Mapping

1. Inventory every data store containing PHI: databases (patient records, billing, scheduling), file storage (medical images, scanned documents, reports), caches (Redis session data, CDN edge caches), logs (application logs, access logs, audit logs), backups (database dumps, snapshot copies, offsite archives), third-party services (error trackers, analytics, AI APIs, email delivery).
2. For each data store, document: PHI fields present, encryption status (at rest, in transit, application-level), access controls, retention period, BAA coverage, de-identification status.
3. Classify each PHI data flow: direct identifiers (name, MRN, SSN, email + health context), indirect identifiers (ZIP+DOB+gender combinations, rare diagnoses), de-identified (documented Safe Harbor or Expert Determination method).
4. Output: PHI data flow diagram (DFD) with trust boundaries, external entities, data stores, and processing nodes labeled with encryption and BAA status.

### Phase 3 (~25 min): Encryption Architecture for PHI

```yaml
# Encryption architecture — implement each layer:

# ── AT REST ─────────────────────────────────────
# Database:
#   AWS RDS: encryption enabled at creation (cannot retrofit)
#   PostgreSQL: pgcrypto for column-level encryption of high-sensitivity fields (SSN, MRN)
#   Key management: AWS KMS CMK with automatic annual rotation
#   GCP: Cloud SQL with CMEK; Azure: SQL DB with TDE + BYOK

# Object storage (S3, Blob Storage, GCS):
#   Default encryption: SSE-KMS with CMK (not SSE-S3 default key)
#   Bucket policy: DENY if s3:x-amz-server-side-encryption != aws:kms
#   S3 Object Lock: Governance mode for audit log buckets (immutability)

# Backups:
#   RDS automated backups inherit source encryption
#   Manual snapshots: encrypted with same KMS key
#   Cross-account/cross-region: KMS key sharing with grant constraints

# ── IN TRANSPORT ────────────────────────────────────
# TLS 1.2 minimum; TLS 1.3 preferred
# HSTS: max-age=31536000; includeSubDomains; preload
# Database: sslmode=verify-full (NOT require — verify-full validates certificate chain)
# mTLS: For service-to-service PHI transfer between microservices
# DICOM TLS: For medical imaging transport (DICOM C-STORE/C-FIND over TLS)

# ── APPLICATION-LEVEL ─────────────────────────────
# Field-level encryption for high-risk PHI:
#   AWS KMS envelope encryption pattern
#   Data key generated per record (not per field)
#   Encrypted data key stored alongside ciphertext
#   Key rotation: Decrypt data key with old CMK, re-encrypt with new CMK

# ── KEY MANAGEMENT ─────────────────────────────
# Separation of duties: Key admins ≠ data admins
# HSM for root of trust (AWS CloudHSM, Azure Dedicated HSM)
# Automatic key rotation: 365-day rotation periods
# Key deletion: 7-day minimum waiting period with recovery window
# Audit: All key usage logged to CloudTrail/audit logs
```

### Phase 4 (~20 min): BAA Architecture and Vendor Governance

1. Build and maintain a BAA registry: every vendor processing PHI, BAA execution date, renewal date, sub-processor list reviewed date, security assessment date, PHI scope.
2. For each cloud service in the architecture, verify: does the service touch PHI data? Is there a signed BAA covering that specific service? Do sub-processors of that service also have flow-down BAAs?
3. High-risk vendor categories requiring enhanced due diligence: AI/LLM APIs (data retention risk), error/performance monitoring (PHI in crash reports), CDN/edge (request logging containing PHI), email delivery (PHI in subject lines and bodies), analytics (user behavior = PHI in health context).
4. BAA non-renewal workflow: 30-day notice → data export from vendor → verification of complete deletion → certificate of destruction → removal from BAA registry.

### Phase 5 (~30 min): EHR, FHIR, and DICOM Security Hardening

1. **EHR Integration (Epic, Cerner):**
   - OAuth 2.0 with SMART on FHIR app launch framework
   - Patient-scoped access tokens (patient/ user/ system scopes)
   - PKCE for public clients; client secret + JWT assertion for confidential clients
   - EHR audit log integration: all API access logged with user, patient, resource, timestamp, purpose of use
   - Break-glass access with mandatory justification and post-hoc review

2. **FHIR API Security:**
   - SMART on FHIR authorization: standalone launch (patient app) and EHR launch (provider app)
   - FHIR resource-level access control: Condition, Observation, MedicationRequest = clinical; Coverage, ExplanationOfBenefit = payment — different access scopes
   - FHIR Bundle security: SearchSet Bundles must filter to authorized resources only. Never return resources from other patients via `_include` or `_revinclude`.
   - Cures Act information blocking: Cannot restrict patient access to their own EHI (electronic health information). API must be open to patient-facing apps or face penalties up to $1M per violation.

3. **DICOM Medical Imaging Security:**
   - DICOM TLS: Encrypt C-STORE, C-FIND, C-MOVE operations between modalities and PACS
   - DICOMweb: STOW-RS, QIDO-RS, WADO-RS over HTTPS with OAuth 2.0
   - DICOM header PHI: Patient Name (0010,0010), Patient ID (0010,0020), Patient Birth Date (0010,0030), Accession Number (0008,0050) — strip for research datasets per Safe Harbor
   - PACS access control: Radiologist vs. referring physician vs. researcher — different image access scopes
   - DICOM de-identification: DICOM PS 3.15 Annex E defines a profile for de-identification of DICOM objects

4. **Telemedicine Platform Security:**
   - Platform BAA required. Patient-facing app with waiting room authentication.
   - End-to-end encryption for video sessions. No server-side recording without patient consent + BAA.
   - Session authentication: unique meeting ID per encounter, not reusable. Waiting room enabled.
   - PHI in chat: If platform allows text chat during session, that chat is a medical record — must be stored in EHR.
   - Device security: Patient device not managed. Assume untrusted client.

5. **Patient Portal Security:**
   - MFA mandatory for patient portal access
   - Rate limiting on login: 5 attempts per 15 minutes → lockout
   - Session timeout: 15 minutes idle, 2 hours absolute max
   - Patient identity verification: Knowledge-based verification (KBA) at enrollment
   - Proxy access controls: Parent/guardian access to minor, caregiver access to adult — age-based rules, expiration dates
   - Cures Act compliance: All EHI available via patient portal API. No withholding test results, clinical notes, or imaging reports.

### Phase 6 (~30 min): Medical Ransomware Response and Breach Notification

1. **Immediate Containment (0-4 hours):**
   - Isolate affected clinical VLANs. Do NOT shut down medical devices without clinical engineering assessment — shutting down a ventilator has life-safety consequences.
   - Activate clinical downtime procedures: paper charting, phone-based order entry, manual medication administration records.
   - Preserve forensic evidence: memory dumps from affected systems, network flow logs, firewall logs, endpoint telemetry. Time sync all evidence sources.
   - Engage incident response retainer if available. Notify cyber insurance carrier.

2. **Breach Determination (4-48 hours):**
   - Was PHI accessed or acquired? Perform 4-factor risk assessment (see Breach Notification Decision Tree).
   - If encrypted + key NOT compromised → no notification (safe harbor).
   - If PHI accessed/acquired AND > low probability of compromise → start 60-day clock.
   - Document the specific date and time of "discovery" — this is when the clock starts, not when investigation completes.

3. **Notification Pipeline (within 60 days):**
   - Affected individuals: First-class mail (or email if patient has consented to electronic notice). Content: brief description of breach, types of PHI involved, steps to protect themselves, what the organization is doing, contact information.
   - HHS Secretary: Via OCR breach portal. < 500 individuals: annual log. ≥ 500: simultaneous with individual notice.
   - Media: If > 500 residents of any state/jurisdiction are affected, prominent media outlet in that area.
   - State Attorneys General: Varies by state — some require immediate notification regardless of federal timeline.

4. **Recovery and Post-Incident:**
   - Restore from known-clean backups. Verify backup integrity before restoration.
   - Re-image clinical endpoints. Do NOT restore compromised systems.
   - Conduct root cause analysis: How did the attacker get in? Which vulnerability? Which device?
   - Update security architecture to prevent recurrence: Network segmentation review, unpatched device remediation, MFA expansion.
   - Tabletop exercise within 90 days: Rehearse the updated incident response plan with clinical and IT stakeholders.
