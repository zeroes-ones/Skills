# API Security Observability — Reference

## Structured Audit Logging Schema

Every authenticated API request should produce one audit log entry with these fields:

```json
{
  "timestamp": "2026-07-23T14:32:17.421Z",
  "request_id": "req_9f7a3b2c1d4e",
  "event_type": "api.access",
  "actor": {
    "user_id": "usr_abc123",
    "client_id": "cli_xyz789",
    "role": "editor",
    "tenant_id": "tenant_01",
    "source_ip": "203.0.113.42",
    "user_agent": "Mozilla/5.0..."
  },
  "action": {
    "method": "GET",
    "path": "/api/v1/users/456/documents",
    "query_params": {"page": "1", "limit": "50"},
    "graphql_operation": null
  },
  "resource": {
    "type": "document",
    "id": "doc_789",
    "owner_id": "usr_def456",
    "tenant_id": "tenant_01"
  },
  "result": {
    "status_code": 200,
    "response_time_ms": 42,
    "error_code": null,
    "items_returned": 50
  },
  "security": {
    "auth_method": "jwt",
    "token_id": "jti_123",
    "mfa_verified": true,
    "policy_decision": "allow",
    "policy_id": "document.read"
  }
}
```

## Critical Fields for Incident Response

In a security incident, these fields answer the key questions:
- **Who:** `actor.user_id`, `actor.client_id`, `actor.tenant_id`
- **What:** `action.method`, `action.path`, `resource.type`, `resource.id`
- **When:** `timestamp`
- **From where:** `actor.source_ip`, `actor.user_agent`
- **Result:** `result.status_code`, `result.error_code`, `security.policy_decision`
- **Correlation:** `request_id` (same ID across all services in the request chain)

## Credential Stuffing Detection via Rate Anomaly

### Detection Rules

| Rule | Condition | Severity | Response |
|------|-----------|----------|----------|
| Global auth spike | > 50 failed logins/sec across all accounts | CRITICAL | Block top offending IPs, enable CAPTCHA |
| Per-account burst | > 10 failed logins for single account in 5 min | HIGH | Lock account for 15 min, notify user |
| Geographic anomaly | Login attempts from > 3 countries for same account in 24h | HIGH | Require MFA, flag account for review |
| Known credential list | Login with email from recent breach database | MEDIUM | Force password reset, notify user |
| Success rate anomaly | > 30% of auth attempts succeed from new IP range | LOW | Monitor — potentially valid new traffic |

### Implementation Pattern
```sql
-- Detect credential stuffing in real-time (evaluated every 60 seconds)
SELECT 
    source_ip,
    COUNT(*) as attempts,
    COUNT(DISTINCT user_id) as unique_accounts,
    SUM(CASE WHEN status_code = 401 THEN 1 ELSE 0 END) as failures,
    SUM(CASE WHEN status_code = 200 THEN 1 ELSE 0 END) as successes
FROM api_audit_log
WHERE 
    event_type = 'auth.login'
    AND timestamp > NOW() - INTERVAL '5 minutes'
GROUP BY source_ip
HAVING 
    failures > 20 
    OR unique_accounts > 50
    OR (failures > 0 AND successes > 0 AND attempts > 10); -- Mixed success/failure from one IP
```

## API Honeytokens (Canary Endpoints)

Honeytokens are decoy API endpoints/resources that legitimate users should never access:

```javascript
// Honeytoken endpoint — no real user should call this
app.get('/api/v1/internal/admin/debug/users', (req, res) => {
    // 🚨 IMMEDIATE ALERT: Someone is probing internal endpoints
    auditLog.alert({
        severity: 'CRITICAL',
        alert_type: 'honeytoken_accessed',
        actor: extractActor(req),
        honeytoken: 'admin_debug_users',
        action: 'Auto-block source IP, rotate all API keys for tenant',
    });
    
    // Return fake data to delay the attacker
    res.json({ users: [{ id: 'honeytoken_001', role: 'admin_trap' }] });
});
```

### Honeytoken Design Principles
1. **Place in URLs that only appear in source code or configs** — not linked from any UI
2. **Use realistic names** — `/admin/debug/users`, `/_internal/config`, `/api/v2/deprecated/export`
3. **Alert immediately** — no threshold, no rate limit, any access = incident
4. **Fake response** — return plausible data to keep attacker engaged while investigation proceeds
5. **Rotate periodically** — change honeytoken URLs every quarter to catch repeat scanners

## Monitoring Dashboard Design

### Critical Dashboards

1. **Auth Overview:** Login success rate, failure rate, MFA usage, token issuance rate, refresh rate
2. **Rate Limiting:** 429 response rate per endpoint tier, top rate-limited users/IPs
3. **Error Distribution:** 4xx vs 5xx rate, top error codes, error rate by endpoint
4. **API Abuse Detection:** Honeytoken hits, credential stuffing alerts, geographic anomalies
5. **Token Health:** Active tokens count, expired tokens, revoked tokens, refresh token reuse events

### Alert Thresholds

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| Auth failure rate | > 15% | > 30% | Investigate credential stuffing |
| 429 rate | > 5% of requests | > 15% | Check for abuse or misconfigured clients |
| 5xx rate | > 1% | > 5% | Incident response — service degradation |
| Honeytoken hits | N/A | ANY | Immediate incident — attacker inside perimeter |
| Token revocation rate | > 10/min | > 100/min | Investigate mass token theft or bug |
| Average response time | > 500ms | > 2000ms | Check DoS or resource exhaustion |

## Log Retention Requirements
- **Security audit logs:** 90 days minimum, 1 year for compliance (GDPR, PCI DSS, SOC 2)
- **Debug logs:** 7-30 days (lower retention, lower sensitivity)
- **Log integrity:** Write-once storage, hash chain for tamper detection
- **PII in logs:** Hash or tokenize PII fields; never log full tokens or passwords
