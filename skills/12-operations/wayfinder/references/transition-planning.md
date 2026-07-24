# Transition Planning

## When to Transition

Transition from investigation to implementation when:
- All BLOCKING tickets are resolved (status: done)
- Capstone decision document is produced
- Implementation can proceed without guessing at core architectural questions

ORDERING and INDEPENDENT tickets can continue in parallel with implementation if they don't block implementation decisions.

## Capstone Decision Document

The capstone synthesizes all investigation findings into actionable recommendations.

```markdown
# [Project] — Investigation Capstone

## Summary
[2-3 sentences: what was investigated and the key decision]

## Decisions
### Decision 1: [Topic]
- Recommendation: [what we recommend]
- Confidence: [HIGH/MEDIUM/LOW]
- Informed by: [ticket IDs and key findings]
- Alternatives rejected: [what we considered and why not]
- Risks: [what could prove us wrong]

## Open Questions
- [Any remaining unknowns that are not blocking implementation]

## Implementation Ticket List
| ID | Description | Informed By | Priority |
|----|-------------|-------------|----------|
| IMPL-001 | ... | DB-001, DB-005 | P0 |
| IMPL-002 | ... | DB-005 | P1 |

## Risk Register
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| ... | ... | ... | ... |
```

## Handoff to Implementation

The capstone document is the primary handoff artifact to the implementation team (project-manager, system-architect, development team). It should be self-contained — the implementation team should not need to read individual investigation tickets.

## Post-Transition

After transition:
1. Archive investigation tickets to `tickets/archive/`
2. Update `.handoff/index.md` with INVESTIGATION_COMPLETE status
3. Knowledge artifacts remain as living project documentation
4. If new unknowns surface during implementation, re-open wayfinder for targeted investigation

## Transition Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|--------------|
| 100% certainty before transition | Perfectionism — some ORDERING unknowns can be resolved during implementation |
| No capstone document | Implementation team re-investigates the same questions |
| Capstone without recommendations | "Here's what we found" without "here's what we should do" creates decision paralysis |
| Premature transition | BLOCKING unknowns unresolved → implementation built on assumptions |
