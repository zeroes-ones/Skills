# Right to Access & Deletion

SAR (Subject Access Request) and RTBF (Right to Be Forgotten)
implementation patterns with deletion cascade and SLA tracking.

## Subject Access Request (SAR) — GDPR Article 15

### Request Intake
- Dedicated SAR intake: web form, email (privacy@), postal
- Auto-acknowledge within 24 hours
- Identity verification: email verification (low sensitivity), government
  ID (high sensitivity), knowledge-based (medium sensitivity)
- Rule: do NOT collect more data to verify identity than you normally hold
- Log request in SAR tracking system with unique ID

### Data Collection from Data Inventory Graph
The data inventory graph maps subject_id to all data stores:
```
SELECT data_category, storage_location, retention_until
FROM data_inventory_graph
WHERE subject_id = :subject_id
AND is_deleted = FALSE
```

### Response Format
- Structured, machine-readable (JSON preferred for portability)
- Organized by data category with source and purpose annotations
- Include third-party recipients (names) and transfer countries
- State retention period per category
- Explain any redactions (legal privilege, third-party data)

## Right to Erasure (RTBF) — GDPR Article 17

### Grounds for Erasure (at least one must apply)
1. Data no longer necessary for original purpose
2. Consent withdrawn (and no other lawful basis)
3. Objection to processing upheld (no overriding legitimate grounds)
4. Data unlawfully processed
5. Legal obligation to erase
6. Data collected from child (information society service)

### Deletion Cascade Pattern

```
Phase 1: SOFT-DELETE (immediate, recoverable)
  For each store in deletion_sequence (topological sort of dependency graph):
    UPDATE {store} SET is_deleted = TRUE, deleted_at = NOW()
    WHERE subject_id = :subject_id
  Log: {deletion_id, subject_id, store, rows_affected, timestamp, status='soft_deleted'}

Phase 2: HARD-DELETE (after soft-delete window, e.g., 30 days)
  For each store:
    DELETE FROM {store} WHERE is_deleted = TRUE AND deleted_at < NOW() - INTERVAL '30 days'
  Log: {deletion_id, subject_id, store, status='hard_deleted'}

Phase 3: PROCESSOR NOTIFICATION
  For each downstream processor with data:
    Send deletion request with subject_id and data categories
    Track acknowledgment and completion
    Escalate if no response within 7 days

Phase 4: BACKUP DECLARATION
  Document: "Backups retain data for up to 90 days. Hard-deleted records
  will not be restored. Backup restoration processes check is_deleted flag."
```

### Deletion Exceptions
- Legal obligation: retain for tax/employment/regulatory period
- Legal claims: retain while litigation is ongoing or reasonably anticipated
- Archiving: public interest, scientific/historical research, statistical
  (with appropriate safeguards — anonymization or pseudonymization)
- Freedom of expression: journalistic, academic, artistic purposes
- Litigation hold: system flag preventing deletion when legal hold active

## SLA Tracking

| Milestone | Deadline | Escalation Trigger |
|-----------|----------|-------------------|
| Acknowledge SAR | 24 hours | Auto-alert if unacknowledged at 12 hours |
| Identity verified | 5 days | Escalate if no response to verification request |
| Data collected | 20 days | Warn if data inventory query fails for any store |
| Response delivered | 30 days | Escalate to DPO at day 25 |
| Extend to 60 days | Notify within 30 | Must document reason for extension |
| Deletion complete (all phases) | 30 days + backup window | Reconciliation job detects partial deletions |
