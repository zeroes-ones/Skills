# Handoff Contract Template

## What This Is

A handoff contract is a bilateral agreement between two agents in a pipeline.
The upstream agent promises specific deliverables. The downstream agent commits to
specific actions given those deliverables. Both sides are auditable.

## Template

```markdown
# Handoff Contract: {origin_skill} → {target_skill}

**Contract ID:** `{pipeline_id}:{origin_skill}→{target_skill}:{timestamp}`
**Created:** {ISO8601}
**Protocol Version:** 1.0.0

## 1. What I Deliver (Upstream Commitments)

| # | Deliverable | Type | Path/Location | Acceptance Criteria |
|---|-------------|------|---------------|---------------------|
| 1 | {artifact name} | {adr|spec|config|code} | {path} | {verifiable condition} |
| 2 | ... | | | |

## 2. What I Need From You (Downstream Commitments)

| # | Request | Deadline | Priority | Blocked By |
|---|---------|----------|----------|------------|
| 1 | {action} | {date or SLA} | {P0-P3} | {none or contract ID} |

## 3. Constraints I'm Passing

| # | Constraint | Type | Non-Negotiable | Source |
|---|------------|------|----------------|--------|
| 1 | {constraint} | {type} | {yes|no} | {origin} |

## 4. Open Questions I Couldn't Resolve

| # | Question | Context | Suggested Approach |
|---|----------|---------|-------------------|
| 1 | {question} | {why it matters} | {hint} |

## 5. Acceptance Gate

- [ ] All deliverables in §1 verified by downstream agent
- [ ] All P0 requests in §2 acknowledged within SLA
- [ ] All non-negotiable constraints in §3 preserved
- [ ] Open questions in §4 addressed or escalated

## 6. Sign-Off

**Upstream Agent:** {origin_skill} — {timestamp}
**Downstream Agent:** {target_skill} — {timestamp} (to be filled on receipt)
**Escalation Path:** {who to notify if contract is breached}
```

## Contract Lifecycle States

```
PROPOSED → ACCEPTED → IN_PROGRESS → FULFILLED
                ↓           ↓
             REJECTED    BREACHED
```

## Breach Conditions

1. Deliverable missing or fails acceptance criteria → contract is BREACHED
2. P0 request ignored beyond deadline → contract is BREACHED
3. Non-negotiable constraint violated → pipeline is ABORTED
