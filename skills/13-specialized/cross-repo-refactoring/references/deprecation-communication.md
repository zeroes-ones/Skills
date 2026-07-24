# Deprecation Communication Strategy

## Multi-Channel Communication Plan

### Week 1: Announce
- CHANGELOG entry with deprecation notice
- Email to consumer team maintainers
- Slack message in #general and #eng-announcements
- Migration guide published (docs site)

### Week 2: Direct Outreach
- DM top 5 consumer maintainers with personalized migration path
- Office hours: 2 sessions for Q&A
- Link to codemod: `npx @org/codemod-old-to-new`

### Week 4: Check-In
- Dashboard published: % consumers migrated
- Follow-up with teams that have not started
- Identify blockers: dependency conflicts, resource constraints

### Month 2: Escalation
- Engineering manager notified of unresponsive teams
- Public dashboard auto-refreshes daily
- "Last call" reminder — removal in 60 days

### Month 3: Final Warning
- Removal date communicated explicitly
- Contact list verified for emergency rollback
- On-call rotation briefed on potential issues

## Runtime Deprecation Warnings

### Logging
```
WARN [DEPRECATED] oldFunction() called by service=payment-service v2.3.1.
Use newFunction(). Will be removed in v3.0.0 (2026-11-01).
```

### HTTP Response Header
```
Deprecation: true
Sunset: Sat, 01 Nov 2026 00:00:00 GMT
Link: <https://docs.example.com/migration>; rel="deprecation"
```

### OpenMetrics/Prometheus Counter
```
deprecated_api_usage_total{api="oldFunction",consumer="payment-service"} 1523
```
