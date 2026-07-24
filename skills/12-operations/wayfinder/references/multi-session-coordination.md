# Multi-Session Coordination

## The Wayfinder + Handoff Pattern

Wayfinder creates investigation tickets. Handoff preserves progress between sessions that resolve those tickets. Together they enable multi-session investigation without context loss.

## Session Start Protocol

At the start of each investigation session:

1. **Read handoff ledger:** `.handoff/ledger.md` for session state
2. **Query ticket status:** Which tickets are active? Which are done since last session?
3. **Recompute frontier:** Which tickets are now ready?
4. **Select active tickets:** Pick up to 3 from frontier
5. **Update ledger:** Set DOING: to current active ticket

## Session End Protocol

At the end of each investigation session:

1. **Update ticket status:** Mark completed tickets as done, update findings
2. **Update ledger:** Move completed items to DONE:, update DOING: with exact state
3. **Set next session's frontier:** Which tickets should be picked up next?
4. **Produce session handoff:** `.handoff/handoff-YYYYMMDD-HHMM.md`

## Ticket State Machine

```
pending → active → done
              ↓
           blocked → active (when unblocked)
              ↓
           unknowable (terminal)
```

A ticket can transition from active to blocked if investigation reveals an unexpected dependency. A ticket can transition to unknowable if investigation proves the question cannot be answered with current constraints.

## Coordination Artifacts

| Artifact | Owner | Location |
|----------|-------|----------|
| Investigation tickets | Wayfinder | tickets/*.md |
| Knowledge artifacts | Wayfinder | tickets/artifacts/* |
| Session state | Handoff | .handoff/ledger.md |
| Handoff snapshots | Handoff | .handoff/handoff-*.md |

## Conflict Resolution

If two sessions produce conflicting findings:
1. Check timestamps — most recent investigation takes precedence
2. Check methodology — more rigorous method wins
3. If equal rigor, flag as CONFLICT and escalate to a dedicated reconciliation ticket
