---
name: hipaa-technical-implementation
description: HIPAA technical implementation — BAA templates, PHI audit table schemas, encryption at rest/in transit patterns, access logging architectures, data deletion cascades, breach notification pipelines, and minimum necessary data access patterns. Use when implementing HIPAA-compliant infrastructure, setting up PHI audit trails, signing BAAs with sub-processors, or building patient data deletion workflows.
author: Sandeep Kumar Penchala
type: health-clinical
status: stable
version: 1.0.0
updated: 2026-07-22
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
output:
  type: code
  path_hint: infrastructure/
---
# HIPAA Technical Implementation

Concrete implementation patterns for HIPAA compliance: PHI audit table schemas, encryption configurations, BAA management, breach notification pipelines, and patient data deletion workflows. This is the code-level companion to `compliance-officer`'s regulatory framework.

## Route the Request
<!-- QUICK: 30s — pick your path, skip the rest -->

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

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

1. **HIPAA is a floor, not a ceiling.** State laws (California CMIA, Texas HB 300, New York SHIELD Act) often impose stricter requirements. Implement to the strictest applicable standard.
2. **PHI = identifiable health data × covered entity status.** Not all health data is PHI. Map your data flows before implementing controls — you can't protect what you haven't inventoried.
3. **Minimum necessary is the default.** Every query, API response, and dashboard must return only the minimum PHI needed for the task. This is not a feature — it's a HIPAA requirement (45 CFR § 164.502(b)).
4. **BAAs before data.** No PHI leaves your infrastructure without a signed Business Associate Agreement. This includes analytics tools, error trackers, CDNs, and AI APIs.
5. **Breach clock starts at discovery.** You have 60 days to notify affected individuals and HHS. The clock starts when ANY employee discovers a breach, not when management decides.

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
<!-- STANDARD: 2min -->

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| "We'll add audit logs later — let's ship first" | Audit tables are part of the initial migration. Retrofitting costs 3x and requires backfill scripts that are error-prone. |
| Storing encryption keys in environment variables | Use a KMS (AWS KMS, GCP Cloud KMS, Azure Key Vault) with automatic key rotation. Environment variables appear in crash dumps, logs, and child process inheritance. |
| Sending PHI to Sentry/DataDog without a BAA | Either sign a BAA with the vendor (enterprise tier) OR scrub PHI from error context before sending. Use `beforeSend` hooks to redact. |
| Soft-delete only for patient data deletion | Soft-delete satisfies the application but NOT HIPAA's right to request deletion. You must also purge from caches, search indexes, backups, and logs. |
| "It's just an email address — it's not PHI" | Email + health app context = PHI. When combined with any health data or even the fact that someone uses a health app, an email address is PHI. |
| Breach notification pipeline that depends on the same infrastructure it monitors | Keep breach notification code and contact lists in a separate, highly-available system (e.g., a separate AWS account with its own alerting). |
| Hardcoded access control: "admins see everything" | Implement purpose-based access: "Dr. Smith sees her patients' bleed logs; Dr. Jones cannot." Minimum necessary access is per-user, per-purpose. |
| Assuming cloud provider encryption is sufficient | AWS RDS encryption protects at rest on disk. It does NOT protect against SQL injection, compromised credentials, or application-level leaks. Layer your defenses. |

## Error Decoder
<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Audit table size grows 10GB/week | Every API call logs full request/response bodies. Unnecessary detail for HIPAA compliance. | Audit only: who accessed what record, when, from where, and why. Don't log payload contents — those go in application logs with PHI redacted. | Audit trails are for compliance, not debugging. Keep them focused on "who saw what when" — not the full HTTP conversation. |
| Patient deletion marked complete but data found in search index 3 months later | Deletion pipeline missed the Elasticsearch/Meilisearch index. Cascading deletion wasn't verified. | Add a verification step: 30 days after deletion, search for the user_id in every data store. Alert if found. | "I deleted it" != "it's gone." Deletion must be verified across every system that could have replicated or cached the data. |
| Breach notification sent but 40% bounced | Contact information was from the application database, which had stale email addresses. | Maintain a separate notification contact store updated independently. Test quarterly with a drill. | The breach notification pipeline must not depend on the same data that may have been compromised or is stale. |
| "Unencrypted" finding in audit despite enabling TLS | Database connection string had `?ssl=require` but the certificate wasn't verified (`sslmode=require` not `verify-full`). | Use `sslmode=verify-full` with the CA certificate. `require` enables TLS but doesn't prevent MITM attacks with forged certificates. | TLS without certificate verification is encryption theater. Always verify the certificate chain in production. |

## Production Checklist
<!-- STANDARD: 3min -->

| ID | Item | Status |
|----|------|--------|
| HI1 | PHI inventory spreadsheet completed — every data store mapped | ☐ |
| HI2 | Audit tables created for all PHI-containing database tables | ☐ |
| HI3 | Audit logging middleware active — every PHI read/write logged with user, IP, timestamp, purpose | ☐ |
| HI4 | Encryption at rest verified: DB, S3, backups all encrypted with AES-256 | ☐ |
| HI5 | Encryption in transit enforced: HSTS, TLS 1.2+, certificate verification on all connections | ☐ |
| HI6 | BAA registry current — all vendors touching PHI have signed BAAs | ☐ |
| HI7 | Minimum necessary access implemented — no `SELECT *` endpoints, purpose-based filtering active | ☐ |
| HI8 | Patient data deletion pipeline: cascading across DB → caches → indexes → backups → logs | ☐ |
| HI9 | Deletion verification task scheduled (30-day follow-up confirms all copies purged) | ☐ |
| HI10 | Breach notification pipeline tested with quarterly tabletop exercise | ☐ |
| HI11 | Breach notification contact list stored independently from primary infrastructure | ☐ |
| HI12 | PHI logging blocked: log redaction patterns active for emails, SSNs, DOBs | ☐ |
| HI13 | KMS key rotation enabled — automatic 365-day rotation for field encryption keys | ☐ |
| HI14 | Database connection uses `sslmode=verify-full` with valid CA certificate in production | ☐ |
| HI15 | Access review process: quarterly review of who has access to what PHI | ☐ |

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

## References
<!-- STANDARD: 3min -->

- **compliance-officer** — HIPAA policy framework and regulatory requirements that drive technical implementation
- **privacy-engineer** — Data minimization architecture and consent management infrastructure
- **security-engineer** — Security architecture, encryption standards, and access control patterns
- **legal-advisor** — Breach determination legal analysis and BAA contract review
- **compliance-officer** — Compliance program structure, audit preparation, and training frameworks
