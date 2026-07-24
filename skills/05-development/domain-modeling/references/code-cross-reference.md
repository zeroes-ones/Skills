# Code Cross-Reference

Verify that code implements domain rules correctly — and flag contradictions.

## Cross-Reference Protocol
1. Extract every domain rule from CONTEXT.md
2. For each rule, locate the code that enforces it
3. Document the file path and line range in CONTEXT.md
4. Flag rules that exist only in code (no documentation) or only in docs (no enforcement)

## Automated Checks
- `grep` for aggregation logic (e.g., `SUM`, `COUNT`, `reduce`) — verify invariants match domain rules
- `grep` for validation logic — ensure it aligns with documented constraints
- `grep` for state transitions — verify the finite state machine matches the documented lifecycle

## Red Flags
- A domain rule enforced by a regex buried in a controller 4 layers deep
- Two different code paths implementing the same business rule differently
- A "TODO: validate per business rules" comment from 18 months ago
