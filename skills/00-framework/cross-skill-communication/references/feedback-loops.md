# Feedback Loop Mechanics

## Loop Closure Requirements

A feedback loop is CLOSED when all 4 stages complete:

```

1. DELIVERY: Consumer sends feedback message to producer
2. ACKNOWLEDGMENT: Producer acknowledges receipt within 24 hours
3. ACTION: Producer completes `producer_action` by `producer_action_deadline`
4. VERIFICATION: Consumer verifies action addressed the issue

```

## Producer Action Catalog

| Action | When to Use | Success Criteria | Typical Deadline |
|--------|------------|-----------------|------------------|
| `recalibrate` | Confidence consistently off by >15% | Historical accuracy within 10% of reported confidence | 14 days |
| `re_score` | Single output was wrong | Updated output with corrected analysis | 48 hours |
| `methodology_update` | Systemic issue in analysis approach | Updated methodology documented and versioned | 30 days |
| `deprecate` | Output type fundamentally unreliable | Deprecation notice published, consumers migrated | 60 days |
| `escalate` | Issue requires human judgment | Human review completed, decision documented | 7 days |

## Calibration Drift Detection

Track `quality_score` over time per producer-consumer pair:

```

If 10-period moving average of quality_score drops below 0.6:
  FLAG: "Calibration drift detected for {producer}.
         Historical avg: {x}, Current avg: {y}"
  ACTION: Producer should recalibrate within 14 days

```

## Resolution Rate Tracking

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Feedback acknowledgment rate | >95% within 24h | <90% |
| Producer action completion rate | >80% by deadline | <70% |
| Consumer verification pass rate | >90% | <80% |
| Recurring issue rate (same issue >3x) | 0% | >0% (escalate immediately) |

## Escalation Matrix

| Condition | Escalate To | Urgency |
|-----------|------------|---------|
| Producer doesn't acknowledge feedback in 48h | Skill owner + wayfinder | Medium |
| Producer misses action deadline | Skill owner + project-manager | High |
| Same issue recurs 3+ times after "resolved" | Skill owner + engineering-manager | Critical |
| Quality score drops below 0.3 | Skill owner + deprecation review | Critical |
