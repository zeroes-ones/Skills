# Dependency Discovery

Undeclared order is the single largest source of wasted parallel work. These are the techniques
for finding dependencies that are real rather than assumed.

## Where to look

| Source | What it reveals |
|---|---|
| Import graph (`rg '^import|^from'`) | Module-level prerequisites |
| Database migrations | Schema ordering; which table must exist first |
| Shared config / env files | Files two tasks will both edit — a collision, not a dependency |
| API contracts | Which service must expose an endpoint before another can consume it |
| Feature flags | The flag must exist before code sits behind it |
| Test fixtures | Shared factories create hidden coupling between otherwise separate tasks |

## The three dependency kinds

1. **Artifact** — task B consumes what task A produces. Always a blocking edge.
2. **Ordering** — B must not run before A for correctness (schema before backfill). An edge.
3. **Resource** — B and A both touch one file, table, or deploy target. Not an edge, but a serialisation requirement or an ownership assignment.

Confusing kind 3 with kind 2 is the common error: teams add a false blocking edge when they should
simply serialise.

## Validating the DAG

- Walk each task and ask "what must be true before this starts?" Record every answer.
- A cycle means a hidden shared prerequisite — extract it as one foundation task.
- Every edge must be justifiable in one sentence. "It feels like B should come after A" is not an edge.

## Failure modes of dependency discovery

- **Assumed order.** The plan relies on ordering nobody wrote down; two people start work that conflicts. Known limitation of verbal plans.
- **False edges.** Serialising work that was actually parallel, wasting the parallelism budget.
- **Missing resource edges.** Two tasks pass the artifact check but collide on a shared file at merge.
- **Hidden test coupling.** Shared fixtures make independent tasks fail each other's tests.
