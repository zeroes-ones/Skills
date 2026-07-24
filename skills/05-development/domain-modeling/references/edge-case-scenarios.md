# Edge-Case Scenarios

Invent adversarial scenarios that stress-test domain definitions until they break — then fix the definitions.

## Scenario Generation Heuristics
- **Temporal**: What if X happens before Y completes?
- **Deletion**: What if the parent entity is deleted while the child is still processing?
- **Concurrency**: What if two users act on the same entity simultaneously?
- **Boundary**: What happens at midnight? At the end of a billing cycle?
- **Null-state**: What if a required field is absent from the legacy system?

## Example Scenarios
- "A customer deletes their account while an order is in fulfillment"
- "A payment succeeds but the inventory allocation fails"
- "A subscription renews during a system migration window"

## Outcome
Each scenario either validates the domain model or exposes a gap. Log both in CONTEXT.md under "Edge Cases."
