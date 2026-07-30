# 6 Communication Patterns — Detailed Specification

## Pattern 1: Request-Response

**State Machine:**

```

IDLE → REQUESTING → WAITING → PROCESSED
                    ↓          ↓
                 TIMEOUT    REJECTED
                    ↓
                DEGRADED

```

**Implementation Requirements:**
- Sender must set response_expected_by in payload
- Receiver must acknowledge within 5s or sender starts timeout clock
- Sender must implement exponential backoff for retries: 1s, 5s, 25s
- After 3 retries → circuit breaker increment

## Pattern 2: Publish-Subscribe

**Subscription Registry:**

```json
{
  "event_type": "corporateAction",
  "subscribers": ["technical-signals-engineer", "fundamental-analyst", "portfolio-signal-manager"],
  "delivery_semantics": "at-most-once | at-least-once",
  "retention_period": "ISO8601 duration"
}

```

**Event Taxonomy Categories:**
- `data.*` — data pipeline events (fresh, stale, corrected, corporateAction)
- `signal.*` — signal lifecycle events (generated, expired, recalibrated)
- `regime.*` — market/context regime changes
- `quality.*` — data quality events (degraded, restored, anomaly)
- `lifecycle.*` — skill lifecycle (deprecated, upgraded, recalibrated)

## Pattern 3: Handoff

**State Bundle Checklist:**
- [ ] decisions: What was decided and why
- [ ] constraints: What limits exist (budget, time, tech, regulatory)
- [ ] open_questions: What's still unresolved
- [ ] ruled_out: What approaches were eliminated (include elimination rationale)
- [ ] artifacts: File paths, data, models created or modified
- [ ] assumptions: Explicit assumptions made during work
- [ ] calibration: Parameter settings and methodology versions used

## Pattern 4: Feedback Loop

**Producer Action Types:**
- `recalibrate` — Adjust confidence/scoring model
- `re_score` — Re-run analysis with different parameters
- `methodology_update` — Change how analysis is performed
- `deprecate` — Mark output type as unreliable
- `escalate` — Human review required
- `no_action` — Feedback acknowledged but no change needed (requires justification)

## Pattern 5: Conflict Resolution

**Calibration Methods:**
1. Historical Accuracy: `calibration_factor = actual_accuracy / average_confidence`
2. Cross-Validation: Compare against known outcomes in test set
3. Expert Bayesian: Prior from expert judgment, updated with observed accuracy
4. Consensus Distance: Weight by how far each source is from consensus

## Pattern 6: Orchestration

**Merge Quality Checklist:**
- [ ] De-duplication: Same finding from multiple sources = 1 finding
- [ ] Severity normalization: Map each source's scale to canonical scale
- [ ] Conflict flagging: Disputed severities escalated with both viewpoints
- [ ] Completeness: Each source marked as contributed/degraded/missed
- [ ] Actionability: Every finding has a recommended action
