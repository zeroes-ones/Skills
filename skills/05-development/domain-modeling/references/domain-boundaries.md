# Domain Boundaries

Identifying where one domain ends and another begins — the hardest part of domain modeling.

## Boundary Signals
- **Language shift**: Different stakeholders use different words for the same concept
- **Rule divergence**: The same entity follows different rules in different parts of the system
- **Ownership**: Different teams are responsible for different aspects of the same concept
- **Lifecycle independence**: Entities are created, modified, and deleted on different schedules
- **Transaction boundaries**: Operations that must be atomic don't span the proposed boundary

## Context Mapping Patterns
- **Partnership**: Two teams cooperate, boundaries are negotiated
- **Shared Kernel**: A small, carefully-maintained shared model
- **Customer-Supplier**: Upstream defines, downstream adapts
- **Conformist**: Downstream accepts upstream's model without translation
- **Anti-Corruption Layer (ACL)**: Downstream builds a translation layer
- **Separate Ways**: No integration — domains are fully independent
