# Write, Manage, Read

Each phase prevents a specific failure. Skipping any one produces a store that looks like memory and behaves like a log.

| Phase | What it does | Failure if absent |
|---|---|---|
| **Write** | Appends a structured, provenance-carrying entry | Nothing is remembered |
| **Manage** | Bounds, folds, supersedes, evicts | The store rots; signal buries itself |
| **Read** | Retrieves and injects under a trust label | Storage cost with no behavioural change |

## Write

Every entry carries: source, timestamp, workflow, run id, outcome, trust class. A write without provenance produces an entry that can never be aged, audited, or safely dropped.

## Manage

Four operations, all scheduled: **retain** raw within a window, **consolidate** older entries into counts, **supersede** contradicted entries keeping both, **evict** entries that are unageable or never read.

Consolidation counts; it never re-summarises. See `consolidation.md`.

## Read

Retrieval returns entries for injection. The injection point is the security boundary: everything crossing it gets a context-only wrapper.

## Failure modes of the lifecycle

- **Read skipped.** The most common failure — a complete write path, a complete manage job, and nothing that reads. Cost with no return.
- **Manage skipped.** Unbounded growth; the useful entries become unreachable.
- **Write skipped.** Nothing to read; the agent re-derives everything.
- **Read before trust labelling.** A self-built injection path.
