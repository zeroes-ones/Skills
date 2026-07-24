# Question Sequencing: Dependency-Based Interview Order

## Core Principle
Questions are ordered by dependency, not by importance or convenience. If Decision B depends on Decision A, you resolve A before asking about B.

## Topological Sort for Decision Trees
1. Map all branches as nodes in a directed graph.
2. Draw dependency arrows: A → B means "B depends on A."
3. Find nodes with no incoming dependencies (leaf nodes). Start here.
4. After resolving a node, remove it and its outgoing edges. New leaves appear.
5. Repeat until all nodes are resolved.

## Cycle Breaking
When A → B and B → A:
- Treat one side as an assumption. Document: "We are assuming [A] for now. If this changes, we will revisit [B]."
- Choose the assumption that is easiest to verify or has the lowest impact if wrong.
- After resolving the other side, return to the assumed side and verify.

## When to Reorder
- New information during grilling reveals an unstated dependency → add to graph, re-sort.
- A resolved decision changes the premises of an unresolved decision → re-evaluate the unresolved one.
