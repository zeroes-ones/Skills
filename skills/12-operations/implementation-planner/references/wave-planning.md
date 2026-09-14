# Wave Planning

A wave is a set of tasks that can run concurrently. Waves exist only after the collision check.

## Building waves

- **Wave 0** = every task with no unresolved predecessor (the unblocked set).
- **Wave N** = every task whose predecessors are all in waves < N.
- Two tasks may share a wave only if their collision surfaces do not intersect.

## The collision check

For every pair in a wave, compare: files touched, tables/schema, deploy targets, queues, API
quotas, feature flags.

| Overlap | Verdict |
|---|---|
| Same file | Serialise, or assign one owner |
| Same table, one writes schema | Order the schema change first |
| Same external resource | Serialise or add a lock task |
| One produces what the other consumes | That is an edge, not parallelism |
| None of the above | Parallel OK — record "none (checked)" |

## Recording the surface

The surface must be **written down**, not remembered. "None (checked)" is a valid and useful entry;
silence is not.

## Failure modes of wave planning

- **Parallelising by feature.** "Different features" is not a collision analysis; the shared config file does not know about features.
- **Unrecorded surface.** Nobody can tell later whether the check was done.
- **Waves that ignore the critical path.** Maximising parallelism on off-path work while the path starves.
- **Treating a collision as a dependency.** Adding a false edge instead of serialising wastes a wave.
