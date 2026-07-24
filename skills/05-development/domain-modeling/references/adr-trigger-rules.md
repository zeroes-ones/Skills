# ADR Trigger Rules

Architecture Decision Records are not for every decision. Apply the three-part trigger test before creating an ADR.

## The Three-Part Trigger Test

An ADR is warranted when the decision is ALL THREE:

1. **Hard to reverse** — would require significant refactoring, data migration, or team retraining to undo
2. **Surprising without context** — a new team member reading the code would ask "why did they do it this way?"
3. **Result of a real tradeoff** — there were genuine alternatives with different pros/cons, not just one obvious choice

## Examples That Pass
- Choosing event sourcing over CRUD for the Order aggregate
- Deciding to use a UUID as the Customer aggregate root identifier instead of auto-increment
- Splitting the monolithic "User" concept into Identity vs. Profile bounded contexts

## Examples That Do NOT Pass
- Choosing PostgreSQL (no real tradeoff discussed, team standard)
- Using REST for a simple CRUD API (not surprising, not hard to reverse)
- Adding a field to an entity (easily reversible)
