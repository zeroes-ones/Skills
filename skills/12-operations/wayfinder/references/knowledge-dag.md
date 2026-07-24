# Knowledge DAG

## The Dependency Graph

The knowledge DAG (Directed Acyclic Graph) models what must be known before what. Each node is an investigation ticket. Each directed edge A → B means "ticket A must be resolved before ticket B can be investigated."

## Building the DAG

1. List all tickets (nodes)
2. For each pair (A, B), ask: "To investigate B, must we first know the answer to A?"
3. If yes, add edge A → B
4. Validate: topological sort must succeed (no cycles)

## Example DAG

```
DB-001 (Query patterns) ──→ DB-002 (PG benchmark)
                         ──→ DB-003 (TCO comparison)
                                    │
DB-004 (Team skills) ──────────────→ DB-005 (Final recommendation)
```

Frontier (ready to work): DB-001, DB-004
After DB-001 done → frontier becomes: DB-002, DB-003, DB-004
After DB-002 + DB-003 + DB-004 done → frontier becomes: DB-005

## Dependency Types

| Edge Type | Meaning | When to Use |
|-----------|---------|-------------|
| DATA | B needs data from A's artifact | A produces a dataset B analyzes |
| DECISION | B's investigation scope depends on A's conclusion | A chooses technology X; B investigates X specifically |
| METHOD | B's investigation method requires A's output | A builds a benchmark harness; B runs the benchmark |
| UNDERSTANDING | B's question only makes sense after A is answered | A defines query patterns; B asks if DB can handle them |

## Cycle Detection and Resolution

If A → B and B → A:
1. Merge A and B into one larger ticket AB
2. Or split one ticket to remove the circular dependency
3. Or recognize that the cycle indicates both tickets are the same investigation

## DAG Maintenance

- After each ticket completion, check if new unknowns were discovered → add tickets
- If a dependency turned out to be false → remove edge
- If a completed ticket's findings invalidate another ticket → mark invalidated ticket as obsolete
- Re-compute frontier after every status change
