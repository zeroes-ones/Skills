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

## Gotchas

- **HIPAA "minimum necessary" rule** applies to access controls, not data storage. Storing all patient data in one table is HIPAA-compliant IF role-based access controls limit what each user can query. But a developer with `SELECT` on that entire table violates minimum necessary — access must be column-level or view-level.
- **BAAs don't cover sub-processors** by default. If your cloud provider (who signed your BAA) uses a sub-processor for a specific service (e.g., AWS using a third party for text-to-speech), that PHI flow may not be covered. Audit sub-processor lists quarterly.
- **PHI in logs** is the #1 source of reportable breaches. `logger.info(f"Patient {patient_id} diagnosed with {condition}")` writes PHI to logs. Logs are replicated, backed up, shipped to observability platforms — each copy is a data store that needs encryption, access control, and retention policy.
- **Email is NOT HIPAA-compliant** by default. SMTP is unencrypted text. Office 365/Google Workspace with BAA cover the inbox, but CC'ing an external address, forwarding to personal email, or sending unencrypted attachments all breach HIPAA.
- **De-identification safe harbor** requires removing 18 specific identifiers, but ZIP codes with populations < 20,000 count as an identifier. A dataset with ZIP+DOB+gender re-identifies 87% of the US population (Sweeney study). True de-identification is harder than it looks — use expert determination, not safe harbor.


## References

Detailed reference material loaded on demand:

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)

