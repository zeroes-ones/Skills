# Reconciliation Protocol

## Structured Reconciliation Workflow

Reconciliation is the bridge between finding a doubt and shipping code. Every doubt that
does not resolve to "CLAIM HOLDS" must produce a RECONCILE.md entry with a decision record.

## Decision Record Template

```markdown
## RECONCILE-[claim_id]

| Field | Value |
|---|---|
| **Claim** | [CLAIM-ID]: [one-sentence assertion] |
| **Doubt** | [DOUBT-ID]: [specific failure condition tested] |
| **Severity** | [CRITICAL\|HIGH\|MEDIUM\|LOW] |
| **Cycle** | [1\|2\|3] |
| **Status** | [RESOLVED\|ACCEPTED\|DEFERRED\|ESCALATED] |
| **Resolution** | [What was changed, accepted, or escalated] |
| **Evidence** | [Test result, code change, monitoring config, escalation report] |
| **Residual Risk** | [What risk remains after this decision] |
| **Monitoring** | [Alert ID, dashboard link, runbook reference] |
| **Date** | [YYYY-MM-DD] |
| **Reviewer** | [Name or model identifier] |
```

## Status Definitions

### RESOLVED
The doubt was substantiated and the code was fixed. Resolution must include:
- The code change (PR link or commit hash)
- A regression test that would catch the same doubt in the future
- Verification that the fix doesn't introduce new claims
- Cross-model verification for CRITICAL severity (mandatory)

### ACCEPTED
The doubt is real but the cost of fixing exceeds the cost of the risk. Acceptance requires:
- Quantified risk: probability × impact estimate
- Monitoring plan: specific alert that detects if the risk materializes
- Runbook: documented response procedure if the alert fires
- Review cadence: date for re-evaluation (not "never")
- Second reviewer sign-off for safety-critical paths

### DEFERRED
The doubt requires a fix that exceeds the current sprint's scope. Deferral requires:
- Ticket filed with severity label and sprint target
- Short-term mitigation (rate limit, feature flag, circuit breaker)
- Acceptance that the risk exists until the ticket is resolved
- Escalation trigger: if deferred > 2 sprints, auto-escalate to tech lead

### ESCALATED
The doubt requires a different model or human expert. Escalation requires:
- Cross-model review report (see cross-model-escalation.md)
- Specific question for the escalated reviewer
- Deadline for response (24h for CRITICAL, 72h for HIGH)
- Fallback: if escalated review doesn't respond, ACCEPT with maximum monitoring

## Residual Risk Quantification Framework

For every ACCEPTED doubt, quantify the residual risk:

```
RISK_SCORE = PROBABILITY × IMPACT

PROBABILITY:
  0.9 — Almost certain (will happen within 30 days under normal load)
  0.7 — Likely (will happen within 90 days or under moderate load spike)
  0.5 — Possible (requires specific conditions: load spike, edge input, race window)
  0.3 — Unlikely (requires multiple simultaneous failures)
  0.1 — Rare (requires extraordinary circumstances)

IMPACT (dollars):
  CRITICAL — >$100K (data loss, security breach, regulatory violation, >1h downtime)
  HIGH     — $10K-$100K (degraded service, revenue loss, customer impact)
  MEDIUM   — $1K-$10K (delayed processing, manual intervention required)
  LOW      — <$1K (cosmetic, self-healing, minimal user impact)
```

**Acceptance threshold:** No ACCEPTED doubt with RISK_SCORE > 0.5 × HIGH may be accepted
without director-level approval.

## Reconciliation Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| **Silent Accept** | Reviewer accepts doubt to avoid conflict with senior engineer | Require quantified risk statement — forces engagement |
| **Defer Forever** | Deferred with no sprint target → never fixed | Auto-escalate after 2 sprints |
| **Resolve Without Test** | Code changed, but no regression test → doubt will recur | Gate RESOLVED on test existence |
| **Accept Without Monitor** | Risk accepted but no detection → silent failure in production | Gate ACCEPTED on alert configuration |
| **Escalate and Forget** | Escalated to cross-model but no deadline → lossy handoff | 24h/72h SLA with fallback to ACCEPT |
