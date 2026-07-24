# Cycle Termination Rules

## The Hard Stop

After 3 doubt cycles on any single claim, the review STOPS. No exceptions. No "just one
more check." No "but what if..." The 3-cycle limit is the core discipline of doubt-driven
development — it separates adversarial review from analysis paralysis.

## Why 3 Cycles?

### The Mathematics of Diminishing Returns

| Cycle | Defect Discovery Rate | Cumulative Cost |
|---|---|---|
| Cycle 1 | 60-70% of all discoverable defects | 15 min/claim |
| Cycle 2 | 20-25% of remaining defects | 10 min/claim |
| Cycle 3 | 5-10% of remaining defects | 10 min/claim |
| Cycle 4 | 1-3% of remaining defects | 10 min/claim + delay cost |
| Cycle 5+ | <1% | Exponential time cost (review fatigue) |

Cycle 4 costs more in engineer time and merge delay than the expected value of defects it
finds. The 3-cycle limit is not arbitrary — it's the economic breakpoint where the cost of
additional doubt exceeds the cost of the remaining risk.

## Stop Criteria Checklist

Before stopping, verify ALL of the following:

- [ ] **Cycle count:** No claim has > 3 doubt cycles in doubt_log.md
- [ ] **CRITICAL resolution:** All CRITICAL severity doubts are RESOLVED (not ACCEPTED, not DEFERRED)
- [ ] **HIGH resolution:** All HIGH severity doubts are RESOLVED or ACCEPTED with monitoring
- [ ] **Reconciliation complete:** Every non-HOLDS doubt has a RECONCILE.md entry
- [ ] **Residual risk cataloged:** Every ACCEPTED doubt has quantified risk + monitoring plan
- [ ] **Cross-model check:** Every CRITICAL cycle-3 doubt has cross-model escalation record
- [ ] **Doubt theater cleared:** All flagged doubt theater has been reformulated or dismissed
- [ ] **Merge decision:** CLEAR TO MERGE, MERGE WITH MONITORING, or DO NOT MERGE

## Residual Doubt Acceptance Framework

### What Residual Doubt IS
Residual doubt is the uncertainty that remains after 3 cycles. It is NOT a failure of the
process — it is an expected outcome. Every non-trivial system has unknowns that cannot be
resolved through review alone.

### What Residual Doubt Is NOT
- "I feel uneasy about this" — feelings are not residual doubt; they're intuition debt
- "We didn't have time to check X" — missed checks are not residual doubt; they're incomplete review
- "Someone should look at this later" — deferred review is not residual doubt; it's a ticket

### Acceptance Criteria
A residual doubt is ACCEPTABLE when:
1. Three cycles have been completed on the claim
2. The probability of the doubt materializing is < 0.3 (unlikely)
3. The impact if it materializes is < HIGH ($10K)
4. A monitoring alert exists that detects if the doubt materializes
5. A runbook exists with response steps if the alert fires
6. A re-evaluation date is set (not "never")

### Acceptance Template
```markdown
## RESIDUAL_RISK-[claim_id]

**Doubt:** [What remains uncertain after 3 cycles]
**Probability:** [0.1-0.3]
**Impact:** [$ amount or severity level]
**Monitoring:** [Alert ID, condition, dashboard link]
**Runbook:** [Link to response procedure]
**Re-evaluation:** [Date — no more than 90 days out]
**Acceptance rationale:** [Why the cost of further cycles exceeds the risk]
```

## When to BREAK the 3-Cycle Rule

Only two exceptions justify a 4th cycle:
1. **New evidence emerged** — A test run after cycle 3 produced unexpected results that
   change the doubt's probability or impact assessment. This is not "one more idea" —
   it's new data.
2. **Regulatory requirement** — FDA, EU AI Act, or equivalent regulation mandates a
   specific verification that was not covered in cycles 1-3. This is compliance, not doubt.

Both exceptions require explicit justification in RECONCILE.md with the tag `CYCLE-4-JUSTIFIED`.
