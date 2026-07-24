# Blocker Documentation

## The Anatomy of an Actionable Blocker

A blocker without a resolution condition, ETA, and escalation path is not a blocker — it's an abandonment note.

## Required Fields

```markdown
BLOCKED: [one-line description of what's blocked]
Dependency: [what external factor must change]
RESOLUTION: [exact command or condition that verifies the block is lifted]
ETA: [date by which resolution is expected]
ESCALATION: [trigger condition + contact + channel]
Impact: [what cannot proceed until this is resolved]
Workaround: [anything we can do in parallel, or nothing]
```

## Resolution Conditions by Type

| Blocker Type | Example Resolution Condition |
|-------------|------------------------------|
| API endpoint needed | `curl -s https://api.staging.example.com/v2/users \| jq '.items[0].id'` returns non-null |
| PR review needed | PR #42 merged to main, `git log --oneline main \| head -1` shows merge commit |
| Infrastructure provisioned | `aws rds describe-db-instances --db-instance-identifier staging-db` returns `Available` |
| Design decision needed | Decision recorded in `docs/adr/0014-caching-strategy.md` |
| Data available | `SELECT count(*) FROM analytics.events WHERE date >= '2026-07-01'` returns > 0 |

## Escalation Path Template

```
ESCALATION:
  T+0: Blocker identified, documented in ledger
  T+24h: Ping primary contact in [channel]
  T+48h: Escalate to [team lead/manager] in [channel]
  T+72h: Escalate to [skip-level/director] with impact statement
  T+120h: Re-evaluate: is this work still viable? Consider alternative approach.
```

## Blocker Lifecycle States

```
IDENTIFIED → DOCUMENTED → IN_FLIGHT → RESOLVED
                                  ↓
                            STALE (past ETA)
                                  ↓
                            ESCALATED
                                  ↓
                            RE-EVALUATED (cancel work or find alternative)
```

## Common Blocker Anti-Patterns

* "Blocked on API team" — Who? When? What endpoint? How to verify?
* "Waiting for review" — Which PR? From whom? ETA?
* "Can't proceed without X" — What CAN proceed in parallel? Document the workaround.
* Blocker with no ETA — Becomes a black hole; set even a rough ETA and escalate when past it.
