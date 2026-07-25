---
name: hipaa-technical-implementation
description: >
  Use when implementing HIPAA-compliant technical infrastructure, designing PHI
  audit trail schemas, configuring encryption for ePHI at rest and in transit,
  building breach notification pipelines, or managing BAA workflows with
  sub-processors. Handles PHI access logging architectures, data deletion
  cascades, minimum necessary access patterns, and HIPAA Security Rule
  technical controls. Do NOT use for GDPR compliance, general security
  hardening unrelated to PHI, HIPAA policy/legal analysis, or non-healthcare
  data protection.
license: MIT
author: Sandeep Kumar Penchala
type: health-clinical
status: stable
version: 1.1.0
updated: 2026-07-23
tags:
- hipaa-technical-implementation
- hipaa
- privacy
- compliance
- healthcare
- phi
- security
chain:
  consumes_from:
  - backend-developer
  - compliance-officer
  - gdpr-privacy
  - legal-advisor
  - privacy-engineer
  - security-engineer
  feeds_into:
  - backend-developer
  - compliance-officer
  - devops-engineer
  - legal-advisor
  - security-engineer
token_budget: 4200
---
# HIPAA Technical Implementation
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Concrete implementation patterns for HIPAA compliance: PHI audit table schemas, encryption configurations, BAA management, breach notification pipelines, and patient data deletion workflows. This is the code-level companion to `compliance-officer`'s regulatory framework.

## Route the Request

<!-- QUICK: 30s — auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*", "PHI\|ePHI\|protected.health\|HIPAA.*compliance\|covered.entity")` AND `file_contains("*.sql", "audit_log\|access_log\|phi")` | This is your skill. Jump to **Core Workflow** — Phase 2 (PHI Audit Tables). |
| A2 | `file_contains("*", "encrypt\|KMS\|key.rotation\|AES.256\|TLS")` AND `file_exists("terraform/\|cloudformation/\|pulumi/")` | Jump to **Core Workflow** — Phase 3 (Encryption & Key Management). |
| A3 | `file_contains("*", "BAA\|business.associate\|sub.processor\|vendor.*PHI")` | Jump to **Core Workflow** — Phase 4 (BAA Workflow). |
| A4 | `file_contains("*", "delete\|purge\|right.to.be.forgotten\|data.deletion\|cascade")` AND `file_contains("*", "patient\|PHI\|HIPAA")` | Jump to **Core Workflow** — Phase 5 (Data Deletion). |
| A5 | `file_contains("*", "breach\|notification\|OCR\|60.day\|affected.individuals")` AND `file_contains("*", "HIPAA\|PHI")` | Jump to **Core Workflow** — Phase 6 (Breach Notification). |
| A6 | `file_contains("*", "HL7\|FHIR\|CDA\|X12\|EDI")` AND `file_contains("*", "interoperability\|integration")` | Invoke **networking-engineer** or **api-designer** instead. This is health data exchange architecture. |
| A7 | `file_contains("*", "de.identif\|Safe.Harbor\|expert.determination\|anonymiz")` | Jump to **Decision Trees** — De-identification Standards. |
| A8 | `file_contains("*", "minimum.necessary\|purpose.based\|access.control\|RBAC.*PHI")` | Jump to **Best Practices** — Minimum Necessary Access. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
Request: "Make this HIPAA compliant..."
├── ...for a database schema? → Jump to Phase 2 (PHI Audit Tables)
├── ...for cloud infrastructure? → Jump to Phase 3 (Encryption & Key Management)
├── ...involving a new vendor/sub-processor? → Jump to Phase 4 (BAA Workflow)
├── ...for a patient data deletion request? → Jump to Phase 5 (Data Deletion)
├── ...after a suspected breach? → Jump to Phase 6 (Breach Notification)
└── Not sure where to start?
    → Run: inventory your PHI. Where is patient data stored, transmitted, and processed?
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to implement HIPAA controls without a PHI inventory.** You cannot protect what you haven't inventoried. Map every data store that contains PHI before writing a single control. | Trigger: generated code contains `audit_log\|encrypt\|access.control` AND `grep -rn "PHI.inventory\|data.flow\|data.map" --include="*.md" --include="*.csv"` returns 0 results | STOP. Respond: "I need a PHI inventory first. Map every data store containing patient data: database tables, file storage, caches, logs, backups, third-party services. List what PHI fields exist in each. I won't write HIPAA controls against an unknown data landscape." |
| **R2** | **REFUSE to store encryption keys in environment variables or source code.** Environment variables appear in crash dumps, child process inheritance, and debug logs. Use a KMS with automatic key rotation. | Trigger: generated code contains `process\.env\.ENCRYPTION_KEY\|ENCRYPTION_KEY=\|API_KEY=\|SECRET_KEY=` in any config file | STOP. Respond: "Encryption keys must use a KMS (AWS KMS, GCP Cloud KMS, Azure Key Vault) with automatic rotation. Environment variables leak into crash dumps, logs, and child processes. Replace: `process.env.ENCRYPTION_KEY` with `kms.decrypt(ciphertextBlob)` using the KMS SDK." |
| **R3** | **REFUSE to send PHI to third-party services without a signed BAA.** This includes error trackers, analytics, CDNs, and AI APIs. No PHI leaves your infrastructure without a signed Business Associate Agreement. | Trigger: generated code contains `Sentry\|DataDog\|Google.Analytics\|Mixpanel\|LogRocket\|OpenAI` AND `file_contains("*", "PHI\|ePHI\|patient")` AND `grep -rn "BAA\|business.associate"` returns 0 results | STOP. Respond: "This code sends data to [service] which may contain PHI. Either: (1) sign a BAA with the vendor (enterprise tier typically required), or (2) scrub PHI from data before sending using `beforeSend` hooks. PHI must not leave your infrastructure without a signed BAA. This is a HIPAA requirement (45 CFR § 164.502(e))." |
| **R4** | **REFUSE to soft-delete only for patient data deletion requests.** Soft-delete satisfies the application but NOT the right to request deletion. PHI must be purged from caches, indexes, backups, and logs. | Trigger: generated deletion code contains `deleted = true\|is_deleted\|deleted_at` AND NOT `cascade\|cache.*delete\|index.*delete\|backup\|log.*purge` within 30 lines | STOP. Respond: "Soft-delete (`deleted = true`) is not HIPAA-compliant deletion. Patient data must be purged from: (1) primary database, (2) all caches, (3) search indexes, (4) backup rotation (exclude deleted users from restores), (5) log archives. Add cascade deletion pipeline and 30-day verification step." |
| **R5** | **DETECT and WARN about TLS without certificate verification.** `sslmode=require` enables TLS but doesn't prevent MITM attacks. Use `sslmode=verify-full` with CA certificate. | Trigger: generated code contains `sslmode=require\|ssl=true\|?ssl=true` without `verify-full\|verify-ca\|rejectUnauthorized` in database connection strings | WARN: "Database connection uses TLS but doesn't verify the certificate chain. Change `sslmode=require` to `sslmode=verify-full` with the CA certificate path. TLS without certificate verification is encryption theater — vulnerable to MITM attacks with forged certificates." |
| **R6** | **DETECT and WARN about breach notification pipeline depending on the same infrastructure it monitors.** If your monitoring system goes down, breach notification must still work. | Trigger: generated breach notification code AND `file_contains("*", "same.account\|same.cluster\|same.region\|same.provider")` for notification infrastructure | WARN: "The breach notification pipeline shares infrastructure with the systems it monitors. If the primary stack is compromised, notification may fail. Separate breach notification code and contact lists into an independent system (separate cloud account, separate provider, or offline backup)." |
| **R7** | **DETECT and WARN about 'just an email address — it's not PHI' assumption.** Email + health app context = PHI. When combined with any health data or the fact that someone uses a health app, an email address is PHI. | Trigger: generated code treats email as non-PHI (`email NOT in PHI_fields\|exclude email from audit\|email is not PHI`) | WARN: "An email address in a health app context IS PHI under HIPAA. The fact that someone uses a health app, combined with their email, is protected health information. Apply the same protections (audit logging, encryption, minimum necessary access) to email as to any other PHI field." |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

Master hipaa technical implementations carry a dual responsibility: technical excellence AND human impact. Every decision ripples through to patient outcomes, regulatory standing, and clinical trust.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Automation complacency** — over-trusting systems in high-stakes contexts | Every automated output gets a qualified human review before clinical action |
| **False precision** — treating uncertain data as exact because it's in a database | Always report confidence intervals; never present a single number without its range |
| **Normalcy bias** — assuming things will continue as they always have | Build "what if this fails?" scenarios into every rollout plan |
| **Documentation asymmetry** — over-documenting the routine, under-documenting the exceptions | Exceptions are the most valuable documentation; they teach the model, not just the rule |

### What Masters Know That Others Don't
- **The difference between statistical significance and clinical significance** — a p-value is not a treatment decision
- **Where the regulatory landmines are buried** — the 3 things that will trigger an audit versus the 30 things that won't
- **That patient experience and clinical accuracy are not trade-offs** — bad UX causes medical errors; good UX prevents them

### When to Break Your Own Rules
- **Escalate for safety, not for process.** If patient safety is at risk, bypass the chain of command.
- **Simplify for the patient.** Clinical precision means nothing if the patient can't understand or act on it.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single deliverable | Execute defined procedures under supervision; follow protocols exactly |
| **L2** | Feature / study | Own a feature or study component; work within established regulatory frameworks |
| **L3** | System / program | Design systems that balance clinical needs, regulatory requirements, and technical constraints |
| **L4** | Product / therapeutic area | Define regulatory strategy; shape clinical development approach; influence industry guidance |
| **L5** | Industry / public health | Shape regulatory frameworks; define standards of care through evidence generation |

**Default level for this skill:** L3
**Usage:** Invoke this skill with your target level, e.g., "as an L3 hipaa technical implementation, design..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- QUICK: 30s — scan the bullet list to decide -->

- Setting up a new health app backend — implement PHI audit from day one (retrofit costs 3x)
- Adding a third-party service (Sentry, Mixpanel, OpenAI) — verify BAA coverage before integration
- Patient requests data deletion — execute cascading removal across primary DB, backups, logs, caches
- Preparing for SOC 2 + HITRUST — implement technical controls that satisfy both frameworks
- Security incident response — determine if a breach triggers HIPAA notification requirements
- Cloud architecture review — verify encryption at rest, in transit, and access logging coverage
- Onboarding a new developer — establish minimum necessary data access patterns

## Decision Trees
**(QUICK)**

<!-- STANDARD: 3min -->

### Is This PHI?
```
Does the data element...
├── Relate to past, present, or future physical/mental health?
│   └── YES → Is it combined with an identifier?
│       ├── Name, email, IP, device ID, geolocation, dates? → YES → PHI 🔴
│       └── Fully de-identified per 45 CFR § 164.514(b)? → NO → Not PHI 🟢
├── Relate to payment for healthcare?
│   └── YES → Is it combined with an identifier? → YES → PHI 🔴
└── None of the above → Not PHI 🟢
```

### Breach Risk Assessment

```
Was PHI accessed/acquired by an unauthorized party?
├── YES → Perform 4-factor risk assessment:
│   ├── Nature and extent of PHI (diagnosis vs appointment time)
│   ├── Who accessed it (known entity under BAA vs unknown attacker)
│   ├── Was PHI actually acquired or just exposed?
│   └── Extent of mitigation (was data encrypted? was it exfiltrated?)
│   └── Low probability of compromise? → No notification required (document why)
│   └── > Low probability? → NOTIFY: Patients, HHS, media if >500 affected
└── NO → Document incident, no notification required

```

### BAA Decision Matrix

```
Service type...
├── Cloud provider (AWS, Azure, GCP) → BAA available on standard terms. Execute before use.
├── Error tracking (Sentry, DataDog) → Some offer BAAs on enterprise plans. Verify coverage.
├── Analytics (Mixpanel, Amplitude) → Most do NOT offer BAAs. Use self-hosted or avoid PHI.
├── AI/LLM APIs (OpenAI, Anthropic) → Zero retained-data BAAs emerging. Check latest status.
│   → If no BAA: de-identify before sending, or use self-hosted model.
├── Email (SendGrid, SES) → BAAs available on paid tiers. Verify TLS enforcement.
└── CDN (Cloudflare, Vercel) → BAAs available on enterprise plans. Disable request logging.
```

## Core Workflow
**(STANDARD)**

<!-- STANDARD: 5min -->

### Phase 1: PHI Data Inventory (~2 hours)

Before writing code, map every place PHI exists:

```bash
# Data flow mapping — run for each feature
# 1. Where is patient data collected?
grep -rn "email\|dob\|diagnosis\|treatment\|medication" src/ --include="*.tsx"

# 2. Where is it stored?
grep -rn "INSERT\|UPDATE" app/models/ --include="*.py"

# 3. Where is it transmitted?
grep -rn "requests.post\|fetch\|axios" src/ --include="*.ts"

# 4. Where does it appear in logs?
grep -rn "console.log\|print\|logger.info" src/ app/ --include="*.ts" --include="*.py"
```

Output: A PHI inventory spreadsheet with columns: Data Element, Storage Location, Transmission Path, Access Pattern, Retention Period, BAA Required.

### Phase 2: PHI Audit Tables (~4 hours)

Every table containing PHI needs a corresponding audit table:

```sql
-- Create audit schema alongside application schema
CREATE SCHEMA IF NOT EXISTS audit;

-- Audit table mirrors source + adds audit metadata
CREATE TABLE audit.profiles (
    audit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    operation CHAR(1) NOT NULL,  -- 'C'reate, 'R'ead, 'U'pdate, 'D'elete
    operation_timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
    operated_by UUID NOT NULL,    -- user_id or system process ID
    operated_from INET,            -- IP address of the request
    record_id UUID NOT NULL,       -- PK of the changed record
    table_name TEXT NOT NULL DEFAULT 'profiles',
    old_values JSONB,              -- previous state (NULL for CREATE)
    new_values JSONB,              -- new state (NULL for DELETE)
    change_reason TEXT              -- e.g., 'patient_request', 'admin_correction'
);

-- Index for fast lookups by patient, operation, time
CREATE INDEX idx_audit_profiles_record ON audit.profiles(record_id, operation_timestamp);
CREATE INDEX idx_audit_profiles_operator ON audit.profiles(operated_by);
CREATE INDEX idx_audit_profiles_timestamp ON audit.profiles(operation_timestamp);

-- Application-level trigger via SQLAlchemy (preferred to DB triggers for logic)
-- See Phase 2a for SQLAlchemy implementation

```

**SQLAlchemy implementation (Python/FastAPI):**

```python
# app/models/audit.py
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from app.database import Base
import uuid

class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = {"schema": "audit"}

    audit_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operation = Column(String(1), nullable=False)
    operation_timestamp = Column(DateTime(timezone=True), nullable=False, server_default="now()")
    operated_by = Column(UUID(as_uuid=True), nullable=False)
    operated_from = Column(INET)
    record_id = Column(UUID(as_uuid=True), nullable=False)
    table_name = Column(String(255), nullable=False)
    old_values = Column(JSONB)
    new_values = Column(JSONB)
    change_reason = Column(Text)

# app/services/audit.py
from app.models.audit import AuditLog
from sqlalchemy.ext.asyncio import AsyncSession

async def log_access(db: AsyncSession, *, user_id, ip_address, record_id, table, reason="access"):
    """Log every PHI access. HIPAA requires accounting of disclosures."""
    audit = AuditLog(
        operation="R",
        operated_by=user_id,
        operated_from=ip_address,
        record_id=record_id,
        table_name=table,
        change_reason=reason,
    )
    db.add(audit)
    await db.commit()

async def log_modification(db: AsyncSession, *, user_id, ip_address, record_id, table, old_vals, new_vals, reason):
    """Log every PHI modification with before/after snapshots."""
    audit = AuditLog(
        operation="U", operated_by=user_id, operated_from=ip_address,
        record_id=record_id, table_name=table,
        old_values=old_vals, new_values=new_vals, change_reason=reason,
    )
    db.add(audit)
    await db.commit()
```

### Phase 3: Encryption at Rest and in Transit (~3 hours)

```yaml
# Encryption checklist — implement each:  

# ── AT REST ─────────────────────────────────────
# PostgreSQL: 
#   ALTER SYSTEM SET ssl = on;
#   CREATE EXTENSION pgcrypto;  -- for column-level encryption if needed
#   AWS RDS: enable encryption at creation (cannot retrofit)

# File uploads (S3):
#   Default server-side encryption: AES-256
aws s3api put-bucket-encryption --bucket lantern-uploads \
  --server-side-encryption-configuration '{
    "Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]
  }'

# Backups:
#   RDS automated backups inherit encryption from source
#   S3 bucket versioning + encryption for backup files

# ── IN TRANSIT ────────────────────────────────────
# API: Enforce HTTPS
# nginx.conf or Cloudflare:
#   Strict-Transport-Security: max-age=31536000; includeSubDomains; preload

# Database connection:
# DATABASE_URL=postgresql+asyncpg://user:pass@host/db?ssl=require

# Redis (if storing PHI-adjacent data):
#   requirepass <strong-password>
#   tls-port 6380 with valid certificate

# ── APPLICATION-LEVEL ─────────────────────────────
# Field-level encryption for sensitive fields:
from cryptography.fernet import Fernet

class EncryptionService:
    """Wrap field-level encryption. NEVER store keys in code."""
    def __init__(self, key: bytes):
        self._fernet = Fernet(key)

    def encrypt_field(self, value: str) -> bytes:
        return self._fernet.encrypt(value.encode())

    def decrypt_field(self, token: bytes) -> str:
        return self._fernet.decrypt(token).decode()

# Key rotation: Use AWS KMS / GCP Cloud KMS with automatic rotation
# aws kms create-key --description "PHI field encryption" --rotation-period 365
```

### Phase 4: BAA Management (~2 hours)

```markdown


## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Encryption at rest is "enabled" but database backups are stored unencrypted on an S3 bucket with public-read ACL | The team enabled TDE on the RDS instance but backup snapshots export to S3 where bucket-level encryption was never configured — and a misconfigured IAM policy made it world-readable | Audit the full data lifecycle, not just the primary store. Enable default bucket encryption (SSE-S3 or SSE-KMS). Block public access at the account level with S3 Block Public Access. Run AWS Trusted Advisor or ScoutSuite weekly. | Encryption at rest means encryption at every rest location — database, backups, snapshots, replicas, logs, and exports. One unencrypted copy breaks compliance. |
| Developer's laptop stolen from coffee shop — contains 3 years of de-identified patient data that's trivially re-identifiable | The "de-identification" removed names and MRNs but kept ZIP code + DOB + diagnosis date — the combination re-identifies 87% of patients when cross-referenced with voter registration data | Enforce HIPAA Safe Harbor de-identification: remove all 18 identifiers. For limited data sets, ensure a Data Use Agreement is in place. Never allow production PHI on developer laptops — use synthetic data generators for local development. Require full-disk encryption on all devices. | HIPAA's Safe Harbor de-identification requires removing 18 specific identifiers. ZIP+DOB+diagnosis date is not de-identified — it's a re-identification key. |
| Business Associate sends PHI breach notification 9 months late because their contract has a 72-hour SLA but no enforcement mechanism | The BAA states "BA shall notify CE within 72 hours of breach discovery" but there's no monitoring to verify compliance, no audit rights exercised, and no penalty clause beyond contract termination | Add breach notification verification to the vendor management program: quarterly attestation letters, annual right-to-audit exercises, and financial penalties for late notification (e.g., $10K/day beyond 72 hours). Contract termination is not a sufficient penalty — by then the damage is done. | A contractual obligation without an enforcement mechanism is a suggestion. BAAs need teeth: audit rights you actually exercise and penalties that actually hurt. |
| Production PHI appears in the test environment because someone ran `mysqldump prod | mysql test` to debug a query | The test database has no access controls, no audit logging, and is accessible to all 50 developers and 12 contractors — none of whom have HIPAA training | Never copy production data to non-production environments. Use data masking tools (Delphix, Informatica TDM) or synthetic data generators. If test data with PHI is absolutely required, the test environment must meet the same security controls as production. | The test environment is the most common PHI leak vector nobody audits. One `mysqldump` pipe can undo years of compliance work. |
| Patient requests an accounting of disclosures and the team can't produce it because access logs only go back 90 days | The EHR's default audit log retention is 90 days due to storage costs. HIPAA requires 6 years of disclosure accounting. The access logs exist for 90 days then are permanently deleted. | Configure audit log retention for 7 years minimum. Archive logs to low-cost cold storage (Glacier, archive-tier blob) after 90 days. Test retrieval quarterly — an archive you can't restore from is not an archive. | HIPAA disclosure accounting requires 6 years of records. If your log retention is shorter than your legal obligation, you're non-compliant by design. |
| Penetration test passes but the tester never checked the physical badge reader at the data center back door | The security assessment scope was "network and application only." The data center's back door badge reader has been broken for 4 months and propped open with a cardboard box. | Include physical security in HIPAA security risk assessments. Walk the perimeter. Test badge readers and camera coverage. Check that server racks are locked and only authorized personnel have keys. | HIPAA Security Rule covers physical safeguards too. Your firewall doesn't matter if someone can walk in and unplug the server. |

## Best Practices
**(STANDARD)**

1. **Encrypt ePHI at rest using AES-256 with KMS-managed keys and automatic rotation.** Under the 2024 HIPAA Security Rule proposed update, encryption for ePHI moves from addressable to required. Use CMK (Customer Managed Key), not default service keys, for all PHI data stores — databases, object storage, file systems, backups, and log archives. Enable automatic key rotation (90-day or 365-day depending on data sensitivity). Never store encryption keys in environment variables, source code, or configuration files.

2. **Implement PHI audit logging as a mandatory middleware, not an optional feature.** Every PHI access (create, read, update, delete) must log: who (user_id), what (record_id, table_name, old_values, new_values), when (timestamp with timezone), where (IP address), and why (change_reason). Use a separate audit schema, not application tables. Index by record_id and timestamp for fast accounting of disclosures. HIPAA requires you to produce an accounting of disclosures for the past 6 years within 30-60 days of request.

3. **Apply the minimum necessary principle at the database query level, not the UI level.** Never use `SELECT *` on PHI-containing tables. Implement column-level access controls via database views or API response filtering. A billing clerk needs patient name, MRN, and CPT code — not diagnosis, treatment notes, or lab results. Document the minimum necessary fields for each role and enforce them in the data access layer.

4. **De-identify data using Expert Determination, not Safe Harbor, for any published or shared dataset.** Safe Harbor removal of 18 identifiers is insufficient when ZIP+DOB+gender re-identifies 87% of Americans (Sweeney study). Expert Determination requires a qualified statistician to certify "very small" re-identification risk using documented statistical methods. Apply k-anonymity (k ≥ 5), l-diversity, and t-closeness. Execute a Data Use Agreement prohibiting re-identification attempts.

5. **Never send PHI to any third-party service without a verified, current BAA.** This includes error trackers (Sentry, DataDog), analytics (Google Analytics, Mixpanel), AI/LLM APIs (OpenAI, Anthropic), CDNs, and email delivery services. If the vendor doesn't offer a BAA on your plan tier, either: (a) upgrade to the BAA-offering tier, (b) scrub PHI before sending via `beforeSend` hooks and CSP headers, or (c) switch to a BAA-offering alternative. PHI leakage to non-BAA services is the #2 source of OCR settlements after PHI-in-logs.

6. **Design data deletion as a cascading pipeline with verification, not a soft-delete flag.** A patient data deletion request requires: (1) primary database purge, (2) cache invalidation, (3) search index removal, (4) backup rotation exclusion, (5) log archive purge, and (6) third-party vendor deletion notification. Implement a 30-day verification step that confirms zero residual PHI across all systems. Soft-delete (`deleted=true`) satisfies the application but NOT HIPAA — residual PHI in caches and backups is still regulated data.

7. **Use `sslmode=verify-full` for all database connections, not `sslmode=require`.** `sslmode=require` enables TLS but doesn't verify the server certificate — vulnerable to MITM attacks with forged certificates. `sslmode=verify-full` validates the certificate chain against the CA, ensuring you're connecting to the actual database server. TLS without certificate verification is encryption theater for PHI in transit.

8. **Separate breach notification infrastructure from the systems it monitors.** If your primary infrastructure is compromised (ransomware, account takeover), the notification pipeline must still function. Host notification contact lists, templates, and workflows on a separate cloud account, separate provider, or offline backup. Include printed contact lists for key stakeholders. Test semi-annually: "We've lost access to our primary cloud account — can we still notify patients within 48 hours?"

9. **Treat metadata as PHI when combined with health context.** An IP address + timestamp of a telehealth session reveals the patient's location and appointment time. An email address in a health app context reveals the fact that someone uses a health app. Under OCR's 2024 guidance, online identifiers (IP address, device ID, email) are PHI when related to past, present, or future health status or healthcare provision. Apply the same protections to metadata as to clinical data.

10. **Implement purpose-based access control, not just role-based access.** A provider accessing records for treatment has different access justification than the same provider accessing records for research. FHIR Consent resources with `.provision.purpose` = `TREAT` should not authorize research access. Map every PHI access to a documented purpose-of-use (treatment, payment, operations, research, public health) and enforce it at the authorization layer.

## Error Recovery
**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination

<!-- STANDARD: 3min -->

| Upstream Skill | What to Expect | Communication Trigger |
|---------------|----------------|---------------------|
| `compliance-officer` | HIPAA policy framework, regulatory requirements, covered entity determination | When policy needs technical implementation — this skill provides the code |
| `privacy-engineer` | Data minimization architecture, consent management, DSAR workflows | When implementing deletion cascades or minimum necessary access |
| `security-engineer` | Security architecture, encryption standards, access control models | When setting up encryption at rest/in transit or breach response |
| `backend-developer` | Application architecture, database schemas, API patterns | When adding audit tables or integrating encryption services |
| `legal-advisor` | Breach determination legal analysis, BAA contract review | When assessing whether an incident meets notification threshold |
| `compliance-officer` | Compliance program structure, policies, training requirements | When mapping technical controls to compliance framework |

| Downstream Skill | What to Deliver | Communication Trigger |
|-----------------|-----------------|---------------------|
| `backend-developer` | Audit table schemas, encryption service code, deletion pipelines | When implementing PHI-handling endpoints |
| `devops-engineer` | Infrastructure encryption configs, BAA-managed vendor list | When provisioning HIPAA-compliant cloud infrastructure |
| `security-engineer` | Breach notification code, access logging patterns | When integrating security monitoring with compliance reporting |
| `legal-advisor` | Breach risk assessment output, audit trail evidence | When legal needs technical evidence for breach determination |
| `compliance-officer` | Technical control evidence for compliance audits | When preparing for HITRUST, SOC 2, or OCR audit |

## Proactive Triggers

<!-- STANDARD: 2min — surface these WITHOUT being asked -->

- **PHI in logs** → `console.log(user.email)`, `print(patient_name)`, or unstructured log output containing identifiers. Flag every instance. PHI in logs = breach waiting to happen. 🔴
- **Third-party SDK without BAA** → A new npm/pip package sends data to an external service. Verify BAA coverage BEFORE merging. 🔴
- **Database column without audit** → A new column in a PHI-containing table has no corresponding audit column. Suggest audit schema update. 🟡
- **Backup retention exceeds policy** → Automated backups older than retention period not being purged. Flag the S3 lifecycle policy gap. 🟡
- **Unencrypted database connection** → `DATABASE_URL` without `?ssl=require` in production config. Production data in transit MUST be encrypted. 🔴
- **Missing minimum necessary filter** → An API endpoint returns `SELECT *` from a PHI table. Should return only required columns per the access context. 🟡
- **BAA expiry approaching** → A vendor BAA is expiring within 30 days. Queue renewal or data migration off that vendor. 🟠
- **Patient deletion incomplete after 30 days** → Deletion was requested but verification task found residual data in caches/backups. Escalate for manual cleanup. 🔴


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## What Good Looks Like

<!-- STANDARD: 3min -->

Every PHI access is logged — who, what, when, from where, and why. The audit trail is complete enough to generate a HIPAA accounting of disclosures in under 24 hours. Encryption is layered: database, application, transport — no single key compromise exposes PHI. The BAA registry is current and reviewed quarterly. A patient requesting data deletion sees their data purged from every system within 30 days, verified by an automated follow-up. When a breach occurs, the notification pipeline fires within 48 hours of discovery — not 60 days — because the team has rehearsed it. A new developer joining the team can't accidentally log PHI because the logger redacts it. An auditor can trace any PHI access from API request → audit log → user identity in under 5 minutes.

## Deliberate Practice

```mermaid
graph LR
    A[Design<br/>solution] --> B[Validate with<br/>stakeholders] --> C[Measure<br/>outcomes] --> D[Refine for<br/>safety & UX] --> A

```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Shadow a clinician or patient for a day; document every moment of friction in their workflow | Quarterly |
| **Competent** | Review a past project that had a safety or compliance issue; map the chain of decisions that led there | Monthly |
| **Expert** | Design a solution under 3 conflicting regulatory regimes (e.g., FDA, EMA, PMDA); identify where they diverge | Quarterly |
| **Master** | Contribute to industry guidelines or regulatory frameworks; move from following rules to shaping them | Annually |

**The One Highest-Leverage Activity:** Every project post-mortem must include a "patient impact" section. If you can't trace your work to a patient outcome, you're building in the dark.

## BAA Tracker (maintain this in your security docs)

| Vendor | Service | BAA Signed? | BAA Date | Renewal | PHI Scope |
|--------|---------|------------|----------|---------|-----------|
| AWS | Infrastructure | ✅ | 2026-01-15 | N/A (standing) | All hosted PHI |
| Vercel | Hosting | ⚠️ Enterprise only | - | Annual | CDN only |
| Sentry | Error tracking | ⚠️ Business plan | - | Annual | IP addresses |
| SendGrid | Email | ✅ | 2026-01-20 | Annual | Email + name |
| OpenAI | AI features | ❌ Not available | N/A | N/A | De-identify ONLY |

## Before signing a new vendor:

> See [references/vendor-due-diligence.md](references/vendor-due-diligence.md) for the full vendor due diligence checklist covering BAA requirements, sub-processor audits, breach notification SLAs, and PHI handling on contract termination.

## Anti-Patterns
**(STANDARD)**

- **HIPAA "minimum necessary" rule** applies to access controls, not data storage. Storing all patient data in one table is HIPAA-compliant IF role-based access controls limit what each user can query. But a developer with `SELECT` on that entire table violates minimum necessary — access must be column-level or view-level. **Total cost: $10,000-$50,000 per violation (Tier 1) to $50,000-$1,919,173 per violation (Tier 4)** in OCR civil monetary penalties, multiplied by the number of affected individuals — a single developer with overbroad access affecting 500 records can trigger penalties up to $1.9M/year.
- **BAAs don't cover sub-processors** by default. If your cloud provider (who signed your BAA) uses a sub-processor for a specific service (e.g., AWS using a third party for text-to-speech), that PHI flow may not be covered. Audit sub-processor lists quarterly. **Total cost: $50,000-$500,000 per year** in compliance gap remediation — discovering an uncovered sub-processor post-audit requires retroactive BAAs, potential breach notification, and 3-6 months of legal remediation at $200-$500/hour.
- **PHI in logs** is the #1 source of reportable breaches. `logger.info(f"Patient {patient_id} diagnosed with {condition}")` writes PHI to logs. Logs are replicated, backed up, shipped to observability platforms — each copy is a data store that needs encryption, access control, and retention policy. **Total cost: $100,000-$1,000,000 per incident** in breach response — a single PHI-in-logs breach affecting 500+ individuals triggers mandatory OCR reporting ($20,000-$50,000 in legal/forensic costs), patient notification ($5-$10 per record), and 2+ years of OCR monitoring.
- **Email is NOT HIPAA-compliant** by default. SMTP is unencrypted text. Office 365/Google Workspace with BAA cover the inbox, but CC'ing an external address, forwarding to personal email, or sending unencrypted attachments all breach HIPAA. **Total cost: $25,000-$250,000 per incident** — a single employee forwarding PHI to personal email triggers a breach investigation, with OCR fines starting at $100 per record for "reasonable cause" violations.
- **De-identification safe harbor** requires removing 18 specific identifiers, but ZIP codes with populations < 20,000 count as an identifier. A dataset with ZIP+DOB+gender re-identifies 87% of the US population (Sweeney study). True de-identification is harder than it looks — use expert determination, not safe harbor. **Total cost: $250,000-$5,000,000 per incident** — releasing "de-identified" data that can be re-identified triggers a breach notification for every individual in the dataset, plus FTC action, civil lawsuits, and permanent reputational damage to research programs.

## Production Checklist
**(STANDARD)**

- [ ] All ePHI data stores encrypted at rest with AES-256 using KMS CMK — key rotation enabled (90-day or 365-day)
- [ ] All database connections use `sslmode=verify-full` with CA certificate — not `sslmode=require`
- [ ] All API endpoints enforce HTTPS with HSTS (max-age=31536000, includeSubDomains, preload)
- [ ] PHI audit tables exist for every table containing PHI — separate audit schema with immutable append-only design
- [ ] Audit log indexed by record_id and operation_timestamp — accounting of disclosures producible within 24 hours
- [ ] Column-level access controls enforced via database views or API response filters — no SELECT * on PHI tables
- [ ] PHI redaction middleware active on all logging pipelines — pre-production log scan returns zero PHI matches
- [ ] Every third-party service receiving any data from the application has a verified, current BAA (or PHI is scrubbed before sending)
- [ ] BAA registry current — all vendors listed with BAA sign date, renewal date, and PHI scope — reviewed quarterly
- [ ] Data deletion pipeline implements cascading purge: primary DB → caches → indexes → backups → logs → third-party vendors
- [ ] Data deletion verification runs 30 days after deletion request — confirms zero residual PHI across all systems
- [ ] Breach notification pipeline hosted on infrastructure independent from clinical systems — tested semi-annually
- [ ] Encryption keys never stored in environment variables, source code, or config files — KMS only
- [ ] Purpose-based access control documented for each role — access justification (TREAT/PAYMENT/OPERATIONS/RESEARCH) required per access
- [ ] De-identification uses Expert Determination with formal statistical certification for all published/shared datasets — Safe Harbor only for internal use with no external sharing

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "We use HTTPS everywhere — that makes us HIPAA compliant." | HTTPS only covers encryption in transit. HIPAA requires administrative (risk assessments, workforce training), physical (facility access controls), and technical (access controls, audit controls, integrity controls) safeguards. HTTPS alone covers ~5% of HIPAA Security Rule requirements. 80% of OCR settlements involve entities that had encryption but lacked access controls or audit logging. |
| "We have a BAA with AWS/Azure/GCP — we're covered." | A BAA makes the cloud provider a business associate for THEIR infrastructure, not yours. If you misconfigure an S3 bucket to public-read, the BAA does not cover you — that's YOUR breach. 53% of healthcare cloud breaches are caused by customer misconfiguration, not provider failure. |
| "Dev and staging environments don't need the same HIPAA controls — there's no real patient data." | 37% of healthcare breaches originate in non-production environments where real PHI was used "temporarily" or production data was copied without de-identification. OCR does not distinguish between prod and non-prod — any system containing PHI is subject to the full Security Rule. $250K+ penalties per non-compliant environment. |
| "It's just metadata — timestamps, IP addresses, and device IDs aren't PHI." | Metadata is PHI when it can identify an individual in a healthcare context. An IP address + timestamp of a telehealth session reveals the patient's location and appointment time — two PHI identifiers. OCR guidance (2024) explicitly includes online identifiers as PHI when related to health services. Metadata-only breaches have triggered $500K+ OCR settlements. |
| "Event logging is optional — it's an 'addressable' specification." | "Addressable" under HIPAA does NOT mean optional. It means you must implement the specification OR document why it's not reasonable and implement an equivalent alternative. No major OCR settlement has accepted "we decided not to" as a valid alternative to audit logging. Implement or document with legal review. |


## Verification

- [ ] Encryption at rest: `aws s3api get-bucket-encryption` — all PHI buckets have encryption enabled
- [ ] Encryption in transit: `curl -I <https://${endpoint}`> — all endpoints return HTTPS (not HTTP) with valid TLS 1.2+
- [ ] Access logging: `aws s3api get-bucket-logging` — all PHI buckets have access logging enabled
- [ ] Audit log: `SELECT * FROM audit_log WHERE timestamp > NOW() - INTERVAL '24 hours'` — all PHI access is logged
- [ ] PHI in logs scan: `grep -E '[0-9]{3}-[0-9]{2}-[0-9]{4}' logs/*.log` — zero SSN patterns in logs
- [ ] BAA audit: all vendors handling PHI have current BAA — zero vendors without BAA
- [ ] Access review: all users with PHI access have documented business justification, reviewed within 90 days

## Verification Guardrails

Before delivering work, the agent must verify:

- [ ] **Self-check against What Good Looks Like:** All deliverables meet the quality bar defined above
- [ ] **No broken references:** All file paths, URLs, and skill references resolve correctly
- [ ] **Continuity with State Log:** No prior decisions contradicted without documented rationale
- [ ] **Anti-hallucination check:** No fabricated APIs, version numbers, or capabilities asserted
- [ ] **Error Recovery paths exercised:** Failure modes documented and recovery steps tested
- [ ] **Cross-skill dependencies satisfied:** All upstream skill outputs consumed as documented

If any checkbox fails, revise before delivering. When all pass, add to the state log.

### Scale Depth

#### Solo / Seed-Stage Startup
- **Scope:** Single application. Cloud-hosted (AWS/Azure/GCP). PHI in one database. 1-2 vendors with BAAs. No dedicated security team.
- **Architecture:** Cloud provider BAA (standard tier). Database encryption at rest (enable at creation). TLS for all endpoints. PHI audit table in separate schema. Environment-based secrets (never in code). Manual BAA tracking spreadsheet.
- **Constraints:** No compliance budget beyond cloud BAA. Encryption must be enabled at infrastructure creation (retrofit is 3-6 months). Audit logging from day one (retrofit costs 3x).
- **Critical minimum:** Encryption at rest + in transit. PHI audit table. BAA with cloud provider. No PHI in logs. Never store keys in code.

#### Small / Series A (Growth)
- **Scope:** Multiple services. 5-10 vendors with BAAs. PHI in database + file storage + caches. 1-2 engineers with part-time security responsibility.
- **Architecture:** KMS with customer-managed keys + auto-rotation. PHI audit middleware (not manual logging). BAA registry with renewal calendar. Automated PHI redaction in logging pipeline. Column-level access control via database views. Data deletion cascade with 30-day verification. Breach notification pipeline (documented, contact list current).
- **New concerns:** Third-party vendor BAA verification (sub-processor audit). SOC 2 Type II preparation. HITRUST e1/i1 scoping. Penetration test cadence. Backup encryption and restore testing.
- **Critical addition:** PHI audit middleware. BAA registry with renewal tracking. Automated log redaction. Breach notification pipeline documentation.

#### Medium / Series B+ (Scale)
- **Scope:** Microservices architecture. 20+ vendors with BAAs. Multi-region deployment. Dedicated security/compliance engineer.
- **Architecture:** HITRUST i1 certification. Purpose-based access control (not just RBAC). Expert Determination de-identification pipeline. Breach notification pipeline with automated 4-factor risk assessment. Separate breach notification infrastructure (different cloud account). Real-time PHI-in-log detection with alerting. Automated BAA renewal tracking with Slack/email reminders 90/60/30 days before expiry.
- **New concerns:** Multi-jurisdiction data residency (state-level breach laws). Sub-processor audit program. Customer BAA negotiation (enterprise sales). Cyber insurance application with technical evidence. Automated compliance evidence collection for audits.
- **Critical addition:** HITRUST certification. Purpose-based access control. Expert Determination de-identification. Independent breach notification infrastructure.

#### Enterprise / Public Company
- **Scope:** Multiple product lines. 50+ vendors with BAAs. International data transfers. Dedicated compliance team. Public company SOX + HIPAA alignment.
- **Architecture:** HITRUST r2 validated assessment. Zero-trust architecture for PHI access. Federated authorization with consent directives (FHIR Consent). Continuous compliance monitoring (Drata, Vanta, Secureframe). Automated PHI data flow mapping updated on every deployment. BAA lifecycle management platform. Patient data portability automation (HIPAA Right of Access).
- **New concerns:** Cross-border PHI transfer (EU adequacy, Binding Corporate Rules). M&A compliance integration (acquired company may not have HIPAA controls). SEC cybersecurity disclosure (material breach within 4 business days). Board-level compliance reporting. OCR proactive audit readiness.
- **Critical addition:** Continuous compliance monitoring. Federated authorization. Cross-border transfer compliance. Board-level reporting. M&A compliance integration playbook.

**Transition Triggers:**
- **Solo → Small:** First external vendor beyond cloud provider added → implement BAA registry and vendor due diligence. First customer SOC 2 request → start SOC 2 preparation. PHI found in logs → implement automated redaction middleware.
- **Small → Medium:** Enterprise customer requires HITRUST certification → begin HITRUST i1 assessment. Third-party vendor breach in your industry → implement sub-processor audit program. PHI spans multiple services → implement purpose-based access control and centralized authorization.
- **Medium → Enterprise:** IPO or acquisition on horizon → align with public company compliance requirements. International expansion → implement cross-border transfer compliance. Board requests cybersecurity updates → establish board-level reporting cadence with metrics.

## Error Decoder
**(DEEP)**

| Symptom | Real-World Cause | Diagnostic Steps | Resolution |
|---------|-----------------|------------------|------------|
| Database connection rejected after enabling TLS — `sslmode=verify-full` fails | Server certificate doesn't match connection hostname, CA certificate path is wrong, or self-signed certificate in use. `sslmode=require` was working because it skipped verification. | Check certificate: `openssl s_client -connect host:5432 -showcerts`. Verify CN/SAN matches the connection hostname. Confirm CA certificate file path is correct and accessible to the application process. | Download the correct CA certificate from the database provider (AWS RDS: us-east-1 bundle). Set correct path in connection string. If using self-signed certs in dev, use `sslmode=verify-ca` with the self-signed CA, but NEVER use `sslmode=require` in production. |
| Audit table growing 500GB/month — query performance degrading | Audit logging every row read for every page view — logging "patient list page loaded" generates 50 audit rows per page load. Audit table is in same database as application, competing for resources. | Check audit log volume by operation type: `SELECT operation, count(*) FROM audit.logs GROUP BY operation`. High READ count suggests over-logging. Check if pagination triggers N audit events for N rows displayed. | Implement selective audit: log READ only when a single patient record is viewed in detail, not list views. Move audit tables to separate database instance. Archive audit logs older than 1 year to cold storage (retain for 6 years per HIPAA). Implement log sampling for analytics queries vs individual record access. |
| Patient data deletion verification finds residual PHI 30 days after deletion request | Backup retention policy keeps snapshots for 90 days — deleted records are still in the backup. Search index (Elasticsearch/OpenSearch) wasn't re-indexed after deletion. CDN cache still serves stale patient data. | Query backup catalog for snapshots taken in the 30 days since deletion. Check search index for deleted record IDs. Test CDN cache for patient-specific URLs. Check log archives for PHI in deleted time range. | Exclude deleted patient IDs from backup restoration process (maintain deletion manifest). Re-index search engine with deletion filter. Invalidate CDN cache by patient-specific cache keys. Update deletion pipeline to include backup exclusion, search index removal, CDN purge, and log archive filtering. Re-run verification after pipeline update. |
| BAA registry audit reveals vendor BAA expired 45 days ago — PHI continued flowing | BAA renewal tracking was manual spreadsheet-based. Vendor changed BAA terms (now requires enterprise tier). Nobody noticed the expiration because the vendor relationship "was working fine." | Stop PHI flow to the vendor immediately. Audit all PHI transactions with the vendor since BAA expiration date — each is a potential impermissible disclosure. Assess whether this triggers breach notification. | Halt PHI transmission to vendor. If vendor is critical, execute emergency BAA renewal or migrate to BAA-compliant alternative. Implement automated BAA renewal tracking with alerts at 90/60/30 days. Add quarterly BAA registry review to compliance calendar. This is the most common and most preventable BAA gap. |
| OCR breach investigation finds that encryption was not enabled on PHI database — "it was on the roadmap" | Encryption at rest was deferred to "post-launch optimization." The 2024 HIPAA Security Rule proposed update makes encryption required, not addressable. "We planned to encrypt" is not a defense under the proposed rule. | Check if any breach actually occurred (encryption gap doesn't automatically equal breach). Determine when PHI first entered unencrypted storage. Assess whether any unauthorized access occurred. | Enable encryption immediately (most cloud databases: modify instance to enable encryption — requires downtime for some engines). Document when encryption was enabled. If breach occurred, the "unencrypted PHI" finding increases OCR penalty tier. Prepare for OCR inquiry: show encryption was a planned control that was delayed, not ignored. Retrofit encryption is a 3-6 month project that could have been 1-2 days at creation. |
| Production database contains real PHI in development/staging environment — developer had full access | Production database was copied to staging without de-identification. No data classification policy distinguished prod from non-prod. Developer ran ad-hoc queries on staging with real patient data. | Identify which PHI fields exist in staging. Determine how long real PHI has been in non-production. Audit who accessed staging and what queries they ran. 37% of healthcare breaches originate in non-production environments (OCR data). | De-identify staging data immediately. Implement automated data masking pipeline for all non-production environments. Apply same HIPAA controls to staging as production (encryption, audit logging, access controls, BAA requirements). Train developers: non-production is NOT a HIPAA-free zone. OCR does not distinguish between prod and non-prod. |

## References

Detailed reference material loaded on demand:

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)

