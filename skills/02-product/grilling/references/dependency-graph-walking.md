# Dependency Graph Walking: Leaf-to-Root Algorithm

## Algorithm
1. Build adjacency list: for each decision D, list its dependencies (decisions that must be made first).
2. Compute in-degree for each node (number of unresolved dependencies).
3. Queue nodes with in-degree 0 (leaf decisions with no dependencies).
4. While queue is not empty:
   a. Dequeue a node. Walk this branch (ask, probe, mark status).
   b. For each node that depends on this one: decrement its in-degree.
   c. If any dependent node's in-degree reaches 0, enqueue it.
5. If queue is empty but nodes remain → cycle detected. Apply cycle-breaking.

## Branch Status Propagation
- When a leaf is marked ASSUMED, mark dependents as "built on assumption [leaf_id]."
- When a leaf is marked UNRESOLVED, block all dependents until resolved or deferred.
- When a leaf is marked RESOLVED, dependents can proceed with that resolution as foundation.

## Cross-Branch Constraints
Sometimes branches are not directly dependent but share a constraint. When walking Branch A reveals a constraint that affects Branch B, document it in both branches and re-evaluate B if already resolved.
