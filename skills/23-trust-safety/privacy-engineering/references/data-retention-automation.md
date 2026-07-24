# Data Retention Automation

TTL-based deletion policies, retention schedule templates, automated
enforcement, and audit trails for GDPR Article 5(1)(e) storage
limitation compliance.

## Retention Schedule Template

| Data Category | Retention Period | Justification | Legal Basis | Deletion Method |
|--------------|-----------------|---------------|-------------|-----------------|
| User account data | Account lifetime + 30 days | Contractual necessity, user expectations | GDPR Art 6(1)(b) | Soft-delete → 30d → hard-delete |
| Payment transaction records | 7 years | Tax law requirement (varies by jurisdiction) | Legal obligation Art 6(1)(c) | Archive after 2y, delete at 7y |
| Customer support tickets | 3 years | Reasonable warranty/claim period | Legitimate interest Art 6(1)(f) | Auto-delete 3y after closure |
| Analytics events (raw) | 90 days | Anonymize/aggregate for long-term | Legitimate interest | Aggregate, delete raw at 90d |
| Marketing consent records | Consent lifetime + 2 years | Proof of compliance post-withdrawal | Legal obligation | Retain proof, delete PII |
| Login/IP logs | 90 days | Security incident investigation | Legitimate interest | Auto-delete after 90d |
| Email tracking (opens/clicks) | 30 days | Campaign measurement, then aggregate | Legitimate interest | Aggregate after 30d, delete raw |
| Abandoned carts | 30 days | Recovery window, then delete | Legitimate interest | Auto-delete 30d after abandoned |

## TTL Implementation Patterns

### Pattern 1: Database-Level TTL
```
ALTER TABLE users ADD COLUMN expires_at TIMESTAMP;
ALTER TABLE orders ADD COLUMN expires_at TIMESTAMP;

-- Daily cron: DELETE WHERE expires_at < NOW()
-- Partition by expires_at month for efficient bulk deletes
```

### Pattern 2: Application-Level TTL with Soft Delete
```python
def soft_delete_expired():
    cutoff = datetime.now() - timedelta(days=30)
    for table in personal_data_tables:
        table.update({is_deleted: True, deleted_at: datetime.now()})
              .where(table.expires_at < cutoff, table.is_deleted == False)
```

### Pattern 3: Event-Based Deletion
Consent withdrawal → publish event → all services consume and delete
within SLA. Track completion per service. Reconcile daily.

## Deletion Audit Trail

```
Table: deletion_log (immutable, append-only)
  deletion_id: UUID PK
  subject_id: STRING
  data_category: STRING
  storage_location: STRING (table, S3 path, log stream)
  record_count: INTEGER
  deletion_reason: ENUM ('rtbf_request', 'consent_withdrawal', 'ttl_expired',
                          'account_deletion', 'legal_hold_release')
  deletion_type: ENUM ('soft_delete', 'hard_delete')
  initiated_by: STRING (user_id or 'system')
  initiated_at: TIMESTAMP
  completed_at: TIMESTAMP
  status: ENUM ('pending', 'completed', 'failed')
  error_message: TEXT (nullable)
```

## Retention Policy Enforcement Verification

Quarterly audit checklist:
- [ ] All personal data tables have expires_at or equivalent TTL column
- [ ] Deletion cron job ran successfully in last 24 hours
- [ ] No expired records older than (TTL + 7 days grace) remain in any store
- [ ] Backup retention policy documented and enforced
- [ ] Deletion audit trail shows all expected deletions
- [ ] Known exceptions documented: legal holds, archival with pseudonymization
- [ ] Retention periods reviewed against current legal requirements
- [ ] No new data category added without retention period assignment

## Handling Exceptions

### Backup Retention
Backups retain deleted data for the backup window (e.g., 90 days
rolling). This is acceptable if documented. Requirements:
1. Backup restoration process checks is_deleted flag
2. Backup retention policy is disclosed in privacy notice
3. Backup window is minimized (not indefinite "we keep backups forever")

### Log Retention
Logs containing personal data (IP addresses, user IDs in URL params,
email addresses in error messages) must have justified retention:
- Security logs: retain for incident investigation window (30-180 days)
- Debug logs: minimize PII presence, scrub before retention
- Access logs: 90-365 days typical, document justification

### Legal Holds
Litigation hold overrides normal retention policy:
- Flag records with hold_id, prevent TTL-based deletion
- Document hold scope, duration, legal basis
- Release hold when legal matter concludes → normal TTL resumes
