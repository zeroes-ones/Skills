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
## BAA Tracker (maintain this in your security docs)

| Vendor | Service | BAA Signed? | BAA Date | Renewal | PHI Scope |
|--------|---------|------------|----------|---------|-----------|
| AWS | Infrastructure | ✅ | 2026-01-15 | N/A (standing) | All hosted PHI |
| Vercel | Hosting | ⚠️ Enterprise only | - | Annual | CDN only |
| Sentry | Error tracking | ⚠️ Business plan | - | Annual | IP addresses |
| SendGrid | Email | ✅ | 2026-01-20 | Annual | Email + name |
| OpenAI | AI features | ❌ Not available | N/A | N/A | De-identify ONLY |

## Before signing a new vendor:
1. Does this vendor touch PHI in ANY way? (logs, IP, email, name?)
2. Do they offer a BAA? → If NO, can you de-identify before sending?
3. Does their BAA cover ALL sub-processors they use?
4. What is their breach notification SLA? (HIPAA requires ≤60 days; contract should require ≤30)
5. What happens to PHI on contract termination? (must be returned or destroyed)
```

### Phase 5: Patient Data Deletion (~3 hours)

```python
# app/services/data_deletion.py
# Implement cascading deletion that covers: primary DB, backups, logs, caches, search indexes

async def execute_deletion_request(db: AsyncSession, user_id: UUID, scope: str):
    """
    HIPAA right to request deletion + state law requirements.
    scope: 'full' | 'partial' | 'anonymize'
    """
    if scope == "full":
        # 1. Soft-delete in primary DB (preserve audit trail)
        await db.execute("UPDATE profiles SET deleted_at = now() WHERE user_id = :uid", {"uid": user_id})
        await db.execute("UPDATE users SET deleted_at = now() WHERE id = :uid", {"uid": user_id})

        # 2. Hard-delete from caches
        await redis.delete(f"user:{user_id}:*")
        await redis.delete(f"session:{user_id}:*")

        # 3. Queue deletion from search indexes
        await celery.send_task("search.delete_user", args=[str(user_id)])

        # 4. Queue deletion from backups (next backup cycle excludes soft-deleted)
        await celery.send_task("backup.exclude_user", args=[str(user_id)])

        # 5. Log the deletion request
        await audit_service.log_disclosure(db, user_id=user_id, action="deletion_requested")

        # 6. Queue 30-day verification (did cascading deletion complete?)
        await celery.send_task("compliance.verify_deletion", args=[str(user_id)],
                               countdown=30 * 86400)  # 30 days

    elif scope == "anonymize":
        # Replace PHI with synthetic data, preserve analytics value
        await db.execute("""
            UPDATE profiles SET
                first_name = CONCAT('Deleted_User_', SUBSTR(gen_random_uuid()::text, 1, 8)),
                last_name = '',
                email = NULL,
                phone = NULL,
                date_of_birth = NULL,
                address = NULL
            WHERE user_id = :uid
        """, {"uid": user_id})
    else:
        raise ValueError(f"Unknown deletion scope: {scope}")
```

### Phase 6: Breach Notification Pipeline (~2 hours)

```python
# app/services/breach_notification.py
from datetime import datetime, timedelta

class BreachResponse:
    """HIPAA breach notification: 60-day clock from discovery."""

    def assess_notification_requirement(self, incident: dict) -> str:
        """
        4-factor risk assessment per 45 CFR § 164.402.
        Returns: 'notify' | 'no_notify' | 'escalate_to_legal'
        """
        score = 0
        # Factor 1: Nature and extent of PHI
        if any(k in str(incident.get('data_types', [])) for k in ['diagnosis', 'treatment', 'hiv', 'mental_health']):
            score += 3  # clinical data = high risk
        elif any(k in str(incident.get('data_types', [])) for k in ['name', 'email']):
            score += 1  # demographic only = lower risk

        # Factor 2: Who received it
        if incident.get('recipient_is_covered_entity'):
            score -= 2  # another covered entity under BAA
        if incident.get('publicly_posted'):
            score += 3  # public exposure

        # Factor 3: Was PHI actually acquired?
        if incident.get('confirmed_exfiltration'):
            score += 3
        if incident.get('viewed_only'):
            score += 1

        # Factor 4: Mitigation
        if incident.get('data_encrypted'):
            score -= 3  # encrypted data = low probability of compromise

        if score <= 2:
            return 'no_notify'  # Low probability — document and move on
        elif score <= 5:
            return 'notify'  # Notify individuals and HHS
        else:
            return 'escalate_to_legal'  # High severity, potential media notification

    async def send_notifications(self, incident: dict, affected_count: int):
        """Execute notification pipeline."""
        # 1. Notify individuals within 60 days
        # 2. Notify HHS (simultaneously if >500 affected, annually if <500)
        # 3. Notify media if >500 affected in a single state/jurisdiction
        # 4. Log all notification attempts (required for compliance audit)

        for user in incident.get('affected_users', []):
            await self.notify_individual(user, incident)

        if affected_count > 500:
            await self.notify_hhs_immediate(incident, affected_count)
            await self.notify_prominent_media(incident, affected_count)
        else:
            await self.schedule_hhs_annual_report(incident, affected_count)
```

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

## Best Practices
<!-- STANDARD: 3min -->

1. **Audit from day one.** Retrofitting PHI audit trails costs 3x more than building them upfront. Every table with PHI gets an audit shadow table from the first migration.
2. **Encrypt at the application layer for high-sensitivity fields.** Database-level encryption protects against stolen disks, not compromised database credentials. Use Fernet/AES-256-GCM for fields like SSN, diagnosis codes, genetic data.
3. **Minimum necessary is a query-level constraint.** Every API endpoint documents: "Returns: name, email, last_login (minimum for password reset flow)." Not "Returns: user object."
4. **BAA registry is living documentation.** Update it in the same PR that adds a new vendor dependency. Stale BAA registries are worse than none — they create false confidence.
5. **Breach response is rehearsed.** Run a tabletop exercise quarterly. The worst time to discover your notification pipeline is broken is during an actual breach.
6. **Deletion is cascading and verified.** A deletion request must cascade through: primary DB → read replicas → caches → search indexes → backups → logs. Verify with a 30-day follow-up task.
7. **Access logs answer "who saw what when."** Every PHI read is logged with user, timestamp, IP, and purpose. This is required for the HIPAA accounting of disclosures (45 CFR § 164.528).
8. **Never log PHI.** Configure your logger to redact known PHI patterns (emails, SSNs, dates of birth). Use structured logging with PHI-safe fields only.

## Anti-Patterns
<!-- MACHINE-EXECUTABLE: Each row has a grep/lint pattern for detection and auto-prevention -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep/lint) | 🛡️ Auto-Prevent |
|---|---|---|---|
| "We'll add audit logs later — let's ship first" | Audit tables are part of the initial migration. Retrofitting costs 3x and requires backfill scripts that are error-prone. | `grep -rn "audit.*later\|todo.*audit\|FIXME.*audit\|ship.*first.*without.*audit" migrations/ src/` → matches = block | **Audit migration lint**: CI rule: `npx validate-schema --require-audit-tables`. For every table with `patient_id\|mrn\|phi`, require `audit_user`, `audit_timestamp`, `audit_action` columns in same migration. |
| Storing encryption keys in environment variables | Use a KMS (AWS KMS, GCP Cloud KMS, Azure Key Vault) with automatic key rotation. Environment variables appear in crash dumps, logs, and child process inheritance. | `grep -rn "process\\.env\\.(ENCRYPTION_KEY\|SECRET\|API_KEY)\|export.*_KEY=\|ENCRYPTION_KEY=" src/ infra/ -l` → matches = block | **Key storage lint**: `npx detect-env-keys --forbid "ENCRYPTION_KEY\|SECRET_KEY\|API_KEY" --require-kms`. CI rule: auto-fail build if encryption material detected in environment. Pre-commit hook: `git-secrets --scan`. |
| Sending PHI to Sentry/DataDog without a BAA | Either sign a BAA with the vendor (enterprise tier) OR scrub PHI from error context before sending. Use `beforeSend` hooks to redact. | `grep -rn "Sentry\|DataDog\|LogRocket\|Mixpanel\|Amplitude\|FullStory" package.json \| xargs grep -rn "patient\|phi\|ePHI\|mrn" src/ -l \| xargs grep -rn "BAA\|business.associate" . -L` → matches = block | **Third-party PHI lint**: CI rule: `npx validate-vendor-phi --require-baa`. For every vendor in `package.json`, verify BAA on file. Auto-redact PHI patterns in `beforeSend` hooks: `/(\d{3}-\d{2}-\d{4}\|[A-Z]{2}\d{6}\|[^@]+@[^@]+\.\w+)/g`. |
| Soft-delete only for patient data deletion | Soft-delete satisfies the application but NOT HIPAA's right to request deletion. Must also purge from caches, search indexes, backups, and logs. | `grep -rn "deleted.*=.*true\|is_deleted\|deleted_at\|soft.delete" src/ \| grep -v "cascade\|cache.*delete\|index.*delete\|backup\|log.*purge"` → matches = block | **Deletion pipeline lint**: CI rule: `npx validate-deletion-pipeline --require-cascade`. Required pipeline stages: `["primary_db", "read_replicas", "caches", "search_indexes", "log_archives"]`. Add `--verify-after-30-days` job. |
| "It's just an email address — it's not PHI" | Email + health app context = PHI. When combined with any health data or the fact that someone uses a health app, an email is PHI. | `grep -rn "not.PHI\|not.*protected\|exclude.*from.*audit\|(email.*isn't\|email.*is.not)" src/ docs/` → matches = flag | **PHI scope lint**: CI rule: `npx validate-phi-classification --health-context`. Auto-classify `email`, `phone`, `address`, `date_of_birth` as PHI when `app_type = "health"`. Add `@PHI` comment annotation requirement. |
| Breach notification pipeline that depends on the same infrastructure it monitors | Keep breach notification code and contact lists in a separate, highly-available system (separate AWS account, separate provider). | `grep -rn "same.account\|same.cluster\|same.vpc\|same.region" breach_response/ infra/ \| xargs grep -rn "monitor\|alert\|notif" -` → matches = flag | **Notification isolation lint**: CI rule: `npx validate-breach-response --require-separate-account`. Verify `breach_notify_infra.account_id != primary_infra.account_id`. Require offline backup of notification contacts. |
| Hardcoded access control: "admins see everything" | Implement purpose-based access: "Dr. Smith sees her patients' bleed logs; Dr. Jones cannot." Minimum necessary access is per-user, per-purpose. | `grep -rn "role.*=.*admin.*select.*\*\|admin.*can.*see.*all\|superuser.*all.*access" src/` → matches = block | **Access control lint**: CI rule: `npx validate-access-control --forbid-admin-all --require-row-level-security`. Enable RLS on all PHI tables. Auto-reject `SELECT *` on PHI tables without `WHERE provider_id = current_user_id`. |
| Assuming cloud provider encryption is sufficient | AWS RDS encryption protects at rest on disk. It does NOT protect against SQL injection, compromised credentials, or application-level leaks. Layer defenses. | `grep -rn "RDS.encrypt\|at.rest.*enough\|provider.*handles.*encrypt\|sufficient.*because.*cloud" architecture.md` → matches = flag | **Encryption depth lint**: CI rule: `npx validate-encryption-depth --require-app-layer`. Required: `["TLS 1.3 transit", "KMS at-rest", "App-layer AES-256-GCM for PHI fields"]`. Auto-fail if only provider-managed encryption. |

## Error Decoder
<!-- MACHINE-EXECUTABLE: First column is exact grep regex for console/log matching -->

| 🖥️ Console Match (grep regex) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `grep -cP "audit.*size.*GB\|audit.*growing.*fast\|audit.*bloat" db_monitor.log` → size > 50GB | Audit table size grows 10GB/week | Every API call logs full request/response bodies. Unnecessary detail for HIPAA compliance — logs capture payloads, not access records. | Audit only: who accessed what record, when, from where, and why (purpose). Don't log payload contents — those go in application logs with PHI redacted. | **1.** Measure: `npx audit-size-analysis --table audit_log --sample 1000` → identify top payload columns by size. **2.** Trim: `npx audit-trim-schema --remove-columns "request_body,response_body,headers" --keep-columns "user_id,timestamp,ip,action,record_id,purpose"`. **3.** Apply migration: `npx audit-migrate-schema --dry-run` → verify, then `--apply`. **4.** Configure retention: `npx audit-set-retention --days 365 --archive-older-to-s3`. **5.** Monitor: `npx audit-size-alert --threshold-gb 10 --check-daily`. |
| `grep -rn "deleted.*true\|is_deleted\|deleted_at" src/ \| grep -v "cascade\|cache\|index\|backup\|log" \| wc -l` → count > 0 | Patient deletion marked complete but data found in search index 3 months later | Deletion pipeline missed Elasticsearch/Meilisearch index. CDC pipeline created hidden PHI replica. Cascading deletion wasn't verified. | Add verification step: 30 days after deletion, search for user_id in EVERY data store. Alert if found. Build pipeline from runtime data flow, not ORM schema. | **1.** Cross-system search: `npx phi-sweep --patient-id $PATIENT_ID --stores "pg,redis,elasticsearch,s3,analytics_wh,backups"`. **2.** If any store returns hits: `npx phi-purge --patient-id $PATIENT_ID --store $STORE --force`. **3.** Add to cascade: `npx deletion-pipeline-add --store $STORE --phase purge`. **4.** Re-run sweep at day 30: `npx phi-sweep-verify --patient-id $PATIENT_ID --schedule 30d` → must return zero results. **5.** Quarterly audit: `npx deletion-pipeline-audit --sample 50 --verify-cross-system`. |
| `grep -cP "bounce\|undeliverable\|invalid.email\|40%.*bounced" breach_notify.log` → bounce_rate > 0.20 | Breach notification sent but 40% bounced | Contact information was from application database, which had stale email addresses. Notification pipeline depends on potentially compromised data. | Maintain separate notification contact store updated independently. Test quarterly with a drill. | **1.** Audit: `npx breach-contact-audit --source application_db --sample 100` → identify stale rate. **2.** Create independent store: `npx breach-contact-migrate --source application_db --target breach_notify_contacts --verify-independently`. **3.** Schedule refresh: `npx breach-contact-sync --frequency monthly --verify-each`. **4.** Test quarterly: `npx breach-drill --scenario notification --verify-deliverability`. **5.** Monitor: `npx breach-contact-health --check-bounces --alert-above 0.05`. |
| `grep -cP "sslmode=require\|\\?ssl=true\|ssl=true" database.yml .env terraform/ -r` → `grep -v "verify-full\|verify-ca"` → count > 0 | "Unencrypted" finding in audit despite enabling TLS | Database connection string had `?ssl=require` but certificate wasn't verified. `sslmode=require` encrypts but doesn't prevent MITM. | Use `sslmode=verify-full` with CA certificate. `require` = TLS without cert verification = vulnerable to MITM with forged certificates. | **1.** Find: `npx db-connection-audit --pattern "sslmode=require\|ssl=true" --exclude "verify"` → list all non-verified connections. **2.** Generate fix: `npx db-generate-verify-full --env $ENV --ca-cert-path /etc/ssl/certs/rds-ca.pem`. **3.** Test: `npx db-verify-tls --connection "$(npx db-get-connection $ENV)" --require-full-chain`. **4.** If test passes: apply to config. If test fails: `npx db-diagnose-tls`. **5.** Add CI test: `npx db-tls-ci-check --environment all --require-verify-full`. |

## Production Checklist
<!-- MACHINE-EXECUTABLE: Every item has an exact CLI validation command and auto-fix path -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|---------|
| **HI1** | PHI inventory spreadsheet completed — every data store mapped | `grep -rn "PHI\|ePHI\|patient.*data" phi_inventory.csv \| wc -l` must be `>= 1` AND `wc -l phi_inventory.csv` must be `>= 3` | `npx phi-inventory-scan --output phi_inventory.csv --scan "pg,s3,redis,elasticsearch,analytics,logs,backups"` |
| **HI2** | Audit tables created for all PHI-containing database tables | `npx audit-table-check --all-tables` → every table flagged as `contains_phi: true` must have matching `audit_*` table | `npx audit-table-bootstrap --all-phi-tables --output-dir migrations/` |
| **HI3** | Audit logging middleware active — every PHI read/write logged with user, IP, timestamp, purpose | `curl -s "https://api.example/health/audit" \| jq '.active'` must be `true` AND `grep -rn "audit.log\|audit.middleware" app_config.yaml` must exist | `npx audit-middleware-init --log-fields "user_id,ip,timestamp,action,record_id,purpose"` |
| **HI4** | Encryption at rest verified: DB, S3, backups all encrypted with AES-256 | `npx encryption-audit --scope "rds,s3,backups"` → every resource must report `encryption: AES-256` and `key_managed: true` | `npx encryption-enforce --scope "rds,s3,backups" --algorithm AES-256 --require-kms` |
| **HI5** | Encryption in transit: HSTS, TLS 1.2+, cert verification on all connections | `curl -sI https://app.example \| grep -q "Strict-Transport-Security"` AND `npx tls-audit --all-connections` → all `>= TLS 1.2` with `verify: full` | `npx tls-enforce --hsts --min-version 1.2 --require-verify-full` |
| **HI6** | BAA registry current — all vendors touching PHI have signed BAAs | `npx baa-audit --check-all-vendors` → every vendor with `phi_access: true` must have `baa_signed: true` AND `baa_expires` in future | `npx baa-registry-init --scan-package-json --auto-flag-phi-vendors --alert-expiring 30d` |
| **HI7** | Minimum necessary access — no `SELECT *` endpoints, purpose-based filtering | `grep -rn "SELECT \*\|select \*" src/ \| grep -v "test\|spec\|mock" \| wc -l` must be `0` AND `grep -rn "row.level.security\|purpose.based" src/ \| wc -l` must be `>= 2` | `npx min-access-audit --fix-select-star --enable-rls --require-purpose-field` |
| **HI8** | Patient data deletion pipeline: cascading across DB → caches → indexes → backups → logs | `grep -rn "cascade\|delete.*pipeline\|purge" src/deletion/` must have stages for: `["primary_db", "caches", "search_indexes", "backups", "log_archives"]` | `npx deletion-pipeline-init --stages "primary_db,read_replicas,caches,search_indexes,backups,log_archives" --verify-after 30d` |
| **HI9** | Deletion verification task scheduled (30-day follow-up) | `grep -rn "30.day\|thirty.day\|verification.*task\|deletion.*verify" deletion_workflow.yaml \| wc -l` must be `>= 2` | `npx deletion-verify-init --delay-days 30 --cross-system-sweep --alert-on-find` |
| **HI10** | Breach notification pipeline tested with quarterly tabletop exercise | `grep -rn "tabletop\|drill\|quarterly.*test\|notification.*test" training_log.md \| wc -l` must be `>= 1` AND date within 90 days | `npx breach-drill-scheduler --frequency quarterly --output training_log.md` |
| **HI11** | Breach notification contact list stored independently from primary infrastructure | `npx breach-contact-isolation-check` → `same_account` must be `false` AND `same_provider` must be `false` | `npx breach-contact-migrate --target-account breach_notify_prod --offline-backup --verify-quarterly` |
| **HI12** | PHI logging blocked: log redaction patterns active for emails, SSNs, DOBs | `grep -rn "phi.*redact\|pii.*filter\|log.*scrub\|redact.*email\|redact.*ssn" logger_config.yaml \| wc -l` must be `>= 3` | `npx phi-log-filter-init --patterns "email,ssn,dob,mrn,phone,address" --action redact` |
| **HI13** | KMS key rotation enabled — automatic 365-day rotation for field encryption keys | `npx kms-audit --check-rotation` → every key must have `rotation_enabled: true` AND `rotation_period_days <= 365` | `npx kms-rotation-enable --all-keys --period-days 365` |
| **HI14** | Database connection uses `sslmode=verify-full` with valid CA certificate | `grep -rn "sslmode=verify-full\|sslrootcert\|ca-cert" database.yml terraform/ -r \| wc -l` must be `>= 1` per environment | `npx db-connection-fix --target verify-full --ca-cert /etc/ssl/certs/rds-ca.pem --all-environments` |
| **HI15** | Access review process: quarterly review of who has access to what PHI | `grep -rn "quarterly.*review\|access.*review\|entitlement.*review" compliance_calendar.yaml` must exist | `npx access-review-init --frequency quarterly --auto-generate-report --alert-unreviewed 45d` |

## Scale Depth: Solo → Small → Medium → Enterprise
<!-- STANDARD: 3min -->

### Solo (1 developer, health app MVP)
**Description:** One developer, one app, cloud-hosted. No dedicated compliance team.
**Approach:** PHI inventory spreadsheet. Audit logging via middleware (not per-endpoint). AWS RDS with encryption enabled (automatic). BAA with AWS only. Deletion: soft-delete in DB only (document limitation). Breach notification: manual process with template.
**Time investment:** ~10 hours for baseline HIPAA technical implementation.

### Small Team (2-10 developers, live product, patients)
**Description:** Growing health app. Real patient data. First compliance audit on horizon.
**Approach:** Full audit table schemas. Application-level encryption for high-sensitivity fields. BAA registry with 5-10 vendors. Cascading deletion with verification. Breach notification pipeline automated. SOC 2 Type II preparation begins.
**Time investment:** ~30 hours initial. ~5 hours/month ongoing.

### Medium Team (10-50 developers, multiple products, HITRUST)
**Description:** Multiple health products. Dedicated security engineer. HITRUST certification target.
**Approach:** KMS with automatic rotation. Per-purpose access control. Audit log aggregation to SIEM. Automated access reviews. Deletion fully automated and verified across all data stores. Breach notification fully rehearsed. HITRUST CSF controls mapped to implementation.
**Time investment:** Dedicated compliance engineering role (0.5 FTE minimum).

### Enterprise (50+ developers, multi-product, multi-regulation)
**Description:** Global health platform. HIPAA + GDPR + state laws. Dedicated compliance team.
**Approach:** Multi-region encryption with customer-managed keys. Real-time PHI flow monitoring. AI-assisted audit log anomaly detection. Zero-trust architecture for PHI access. Fully automated deletion with cryptographic verification. Breach notification with redundant communication channels. Continuous compliance monitoring.
**Time investment:** Dedicated compliance engineering team (2-3 FTE).

## What Good Looks Like
<!-- STANDARD: 3min -->

Every PHI access is logged — who, what, when, from where, and why. The audit trail is complete enough to generate a HIPAA accounting of disclosures in under 24 hours. Encryption is layered: database, application, transport — no single key compromise exposes PHI. The BAA registry is current and reviewed quarterly. A patient requesting data deletion sees their data purged from every system within 30 days, verified by an automated follow-up. When a breach occurs, the notification pipeline fires within 48 hours of discovery — not 60 days — because the team has rehearsed it. A new developer joining the team can't accidentally log PHI because the logger redacts it. An auditor can trace any PHI access from API request → audit log → user identity in under 5 minutes.

## Footguns
<!-- DEEP: 10+min — war stories from HIPAA technical implementation -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| Analytics tool ingested 18 months of patient emails and MRNs through the app's error tracking SDK — $240K in breach notification costs, 3 months of forensics | A health app integrated Sentry for error tracking. The developer configured Sentry's SDK to capture full request payloads from API errors. Over 18 months, 14,200 error events included patient PII — email addresses, medical record numbers, and in 340 cases, diagnosis codes in API request bodies. Sentry's BAA was signed for basic error metadata, not PHI payload capture. The breach was discovered during a routine data flow audit. Notifications went to 14,200 patients. Forensics cost $240K. Sentry wasn't designed to receive PHI — it has no audit trail for PHI access, no deletion cascade, and their infrastructure wasn't vetted for HIPAA. | The engineering team treated error tracking as an infrastructure concern, not a PHI data flow. Sentry was added to the tech stack without a data flow review. The BAA was signed for a hypothetical integration scope that didn't match reality. | **Every SDK and third-party service that touches your application must be listed in the PHI inventory with the data it actually receives, not the data you think it receives.** After any new SDK integration, run a production sampling test: capture 100 requests from the service's dashboard and manually check for PII. Add PII redaction middleware that strips emails, MRNs, and diagnosis codes from error payloads before they reach any third-party service. |
| BAA signed with AWS covers the main account — but the analytics data warehouse in a sibling AWS account with PHI replicas had no BAA | A health platform used AWS Organizations with separate accounts for production (account A) and analytics (account B). Production PHI data was replicated nightly to account B's Redshift cluster. The BAA was signed for account A only — the legal team assumed the AWS Organizations BAA covered the entire organization. It doesn't. Each AWS account that processes or stores PHI requires its own BAA or explicit inclusion in the master BAA. An OCR HIPAA investigation following a patient complaint discovered the gap. The settlement included a $175K fine and a 3-year corrective action plan with annual audits. | AWS Organizations groups accounts for billing and management, not for HIPAA compliance. Each account is a separate HIPAA covered entity relationship. The legal team applied organizational hierarchy logic to regulatory contracts. | **Map every AWS account, GCP project, or Azure subscription that stores or processes PHI. Verify a BAA exists for each one individually.** If your cloud provider's BAA structure covers sub-accounts, get that in writing from their compliance team. Don't assume organizational hierarchy == BAA coverage. Add BAA verification to your quarterly access review: for each PHI data store, confirm the BAA is current and covers the exact account/project/subscription ID. |
| Patient data deletion request completed — but 3 months later, a full copy of the patient's records was restored from a "deleted before the cutoff" backup during a disaster recovery test | A patient requested complete data deletion per the app's privacy policy. The deletion pipeline successfully purged the patient's records from the production database, caches, search indexes, and analytics warehouse. Verification confirmed zero records. Three months later, a DR test restored a production database backup from 6 months prior — before the deletion request. The restored database contained the patient's full PHI. The backup was supposed to have a 90-day retention, but the backup retention policy was misconfigured to keep monthly snapshots for 12 months. The patient's data was re-created in a test environment accessible to 8 engineers. | The backup retention policy wasn't aligned with the deletion policy. The deletion pipeline didn't scan backups. The DR test process had no PHI check before restoring data to an accessible environment. | **Backup retention must not exceed data deletion guarantees.** If your privacy policy says "data deleted within 30 days," backups must not be retained beyond 30 days either. Alternatively: maintain a deletion manifest — a list of deleted patient IDs with deletion dates. Before any backup restore, check the manifest. Any patient who requested deletion after the backup date must be re-deleted from the restored environment before it becomes accessible. The DR test playbook must include a "PHI re-deletion" step. |
| `sslmode=require` on the PostgreSQL connection — 2 years of production traffic was vulnerable to MITM attacks because certificate verification was disabled | A health platform's PostgreSQL connection string used `sslmode=require` for 2 years. The team believed "require" meant "TLS enforced." It doesn't. `sslmode=require` enables TLS encryption but does NOT verify the server's certificate — meaning any server presenting any certificate (or no valid certificate) can complete the TLS handshake. A sophisticated attacker on the same VPC could intercept database traffic with a forged certificate. The misconfiguration was discovered during a penetration test. The fix — changing to `sslmode=verify-full` with the RDS CA certificate — took 5 minutes. But 2 years of PHI was transmitted without certificate verification. The breach disclosure to patients cited "potential, not confirmed" interception because there was no way to prove traffic wasn't intercepted. | The team confused "TLS enabled" with "TLS properly configured." `sslmode=require` is a common default in development tutorials and ORM quickstarts. Nobody verified the connection security after the initial setup because "it's encrypted" felt sufficient. | **Every database connection string in every environment must use `sslmode=verify-full` with the correct CA certificate path.** Add a configuration test to CI/CD: connect to the database from a test container and verify the TLS handshake validates the full certificate chain. If the connection succeeds with `verify-full` but not with `require` (because of an invalid cert), the test should fail. This catches certificate rotation issues before they become production "fix it by downgrading to require" emergencies. |
| Patient data deletion was marked "complete" in the app — but the Elasticsearch index retained PHI for 14 months because the deletion pipeline didn't include the search index in its scope | An `app.deleteUser()` function cascaded through: PostgreSQL (soft delete → hard delete after 30 days), Redis cache flush, S3 file purge, and analytics warehouse drop. The deletion was marked "complete" with a green verification check. But the app's search functionality used Elasticsearch for patient record search. The Elasticsearch index was synced from PostgreSQL via a CDC pipeline (Debezium) and was not in the deletion cascade. A patient's MRN, diagnosis history, and treatment dates remained searchable in Elasticsearch for 14 months. Discovered when a support agent searched for a deleted patient's name to help another patient and found the records. | The data flow diagram that informed the deletion pipeline was built from the application's ORM models — it didn't include infrastructure services like search indexes. CDC pipelines create hidden PHI replicas that sit outside the application's data model. | **Build the deletion pipeline from a runtime data flow diagram, not the ORM schema.** Trace every system that could ingest, cache, or replicate PHI: databases → caches → search indexes → message queues → CDC pipelines → analytics → backups → logs. The deletion verification step must run a cross-system search: query every data store by patient ID 30 days after deletion and confirm zero results. Any system with a hit becomes part of the deletion cascade. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You know HIPAA requires encryption but can't explain the difference between encryption at rest (AES-256), encryption in transit (TLS 1.2+), and application-level encryption — or which PHI fields need which | You've built a PHI audit trail that logs every read/write with user identity, timestamp, IP, and purpose — and an auditor can trace any PHI access from API request to individual database row in under 5 minutes | An OCR investigator conducts a surprise HIPAA compliance review and concludes: "The technical safeguards exceed the minimum necessary standard" — no findings, no corrective action plan, and they cite your audit trail implementation as an example of best practice |
| Your PHI "inventory" is a mental model — you don't have a documented spreadsheet mapping every data store, every PHI field, and every third-party service with signed BAAs | You've designed a deletion pipeline that cascades through database → cache → search index → backups → logs — and a follow-up verification 30 days later confirms zero PHI across all systems | A patient sues for unauthorized disclosure of PHI. Your legal team requests the accounting of disclosures for that patient. You produce a complete, timestamped audit log of every access to that patient's data in 4 hours — and the case is dismissed because the log proves no unauthorized access occurred |
| You sign BAAs with vendors but haven't verified that the vendor's actual data handling matches the BAA scope — and you can't name which vendors receive PHI vs which receive de-identified data only | You've built a breach notification pipeline that has been tested in a live tabletop exercise, notified simulated patients within 48 hours, and the post-mortem produced 3 process improvements implemented within 30 days | You design the HIPAA technical architecture for a company acquiring 2 health apps with different tech stacks — within 60 days you produce a unified PHI inventory, a consolidated audit trail, a combined deletion pipeline, and a single BAA registry covering all 3 products |

**The Litmus Test:** Your CTO deploys a new microservice that stores patient data in a database you didn't know existed. You find out 6 months later. If your first question is "does the microservice have audit logging, encryption, and BAA coverage?" and you can answer all three definitively within 30 minutes by querying your infrastructure-as-code registry (you have one, right?) — you're L3. If your first reaction is "wait, we have how many databases?" — you're not there yet.

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

## References
<!-- STANDARD: 3min -->

- **compliance-officer** — HIPAA policy framework and regulatory requirements that drive technical implementation
- **privacy-engineer** — Data minimization architecture and consent management infrastructure
- **security-engineer** — Security architecture, encryption standards, and access control patterns
- **legal-advisor** — Breach determination legal analysis and BAA contract review
- **compliance-officer** — Compliance program structure, audit preparation, and training frameworks
