# Data Retention Automation

## Retention Policy Framework

| Regulation | Data Type | Minimum Retention | Maximum Retention | Trigger for Deletion |
|-----------|-----------|-------------------|-------------------|---------------------|
| **GDPR** | Personal data | As long as purpose requires | Purpose expiry + 30 days | Purpose fulfilled, consent withdrawn, erasure request |
| **HIPAA** | PHI | 6 years from creation or last effective date | 6 years (federal), longer by state law | Retention period expired |
| **PCI DSS** | Cardholder data | As long as business need requires | Minimize — no business need = delete | Business need expired, quarterly purge required (Req 3.1) |
| **SOX** | Financial records | 7 years | 7 years | Retention period expired |
| **CCPA/CPRA** | Personal information | As long as disclosed at collection | Purpose limitation | Purpose fulfilled, deletion request received |

## Automated Deletion Strategies

### TTL-Based Deletion
```
S3 object lifecycle policy:
  - Transition to Glacier after 90 days
  - Delete after 365 days (with legal hold override check)
```

### Event-Based Purging
```
Trigger: Customer deletion request received
  1. Identify all data stores containing customer data (catalog lookup)
  2. Delete/overwrite records in each store (within 30-day GDPR window)
  3. Verify deletion across all stores
  4. Log deletion audit trail (what was deleted, when, by whom, under what policy)
```

### Legal Hold Override
```
Legal hold flag → suspends all retention-based deletion
  - Only authorized legal team members can set/remove legal hold
  - All deletion jobs check legal hold database before executing
  - Expired holds auto-escalate to legal for review
```

## Backup Exception Documentation

Backups are exempt from immediate deletion because:
1. Restoring and selectively deleting from backup is technically infeasible
2. Backups are encrypted, access-controlled, and time-limited
3. Document: backup retention period, encryption key management, access controls

## NIST SP 800-88 Media Sanitization

| Method | Data Type | Effectiveness |
|--------|-----------|---------------|
| **Clear** | Logical overwrite | Protects against simple non-invasive recovery |
| **Purge** | Cryptographic erase (delete KEK) or block-level overwrite | Protects against laboratory-grade recovery |
| **Destroy** | Physical destruction (shred, incinerate, degauss) | Highest assurance — media unrecoverable |
