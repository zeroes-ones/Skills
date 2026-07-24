# Data Access Audit

## Audit Log Schema

Every data access must produce an immutable log entry:

```
{
  "event_id": "uuid",
  "timestamp": "ISO 8601 with timezone",
  "actor": {
    "user_id": "authenticated user or service account",
    "ip_address": "source IP",
    "session_id": "session identifier"
  },
  "action": "READ | WRITE | DELETE | EXPORT | GRANT",
  "resource": {
    "data_store": "database/table/column or file path",
    "record_id": "specific record accessed",
    "classification": "data classification tier"
  },
  "result": "ALLOW | DENY | ERROR",
  "context": {
    "application": "application making the request",
    "purpose": "declared access purpose",
    "request_id": "correlation ID for request tracing"
  }
}
```

## Audit Architecture

- **Immutable logs**: Write-once storage (S3 Object Lock, GCP Bucket Lock, append-only ledger)
- **Log integrity**: SHA-256 chain (each log entry references hash of previous entry)
- **Retention**: Minimum 1 year online, 7 years archived (compliance dependent)
- **Tamper detection**: Alert on any log modification or gap in sequence numbers

## SIEM Integration

- Forward all data-access audit events to SIEM in real-time
- Configure correlation rules:
  - Access to Tier 3 (Restricted) data outside business hours → P1 alert
  - Single user accessing > 1000 records in 5 minutes → P2 alert
  - Failed access attempts > 10/minute from single source → P3 alert
  - First-time access to Tier 3 data by any user → P4 notification

## UEBA Anomaly Detection

User and Entity Behavior Analytics detects anomalies in data access patterns:
- **Baseline**: 30 days of normal access patterns per user/role
- **Anomaly triggers**: Access from new location, unusual time, unusual data volume, new data types
- **Response**: Alert with risk score → Investigate → Revoke access if confirmed unauthorized

## Database Activity Monitoring (DAM)

- Deploy at database network layer (proxy/gateway) or via native audit logging
- Monitor: SQL queries, schema changes, permission changes, data exports
- Alert on: `SELECT * FROM users`, `DROP TABLE`, `GRANT ALL`, mass exports
