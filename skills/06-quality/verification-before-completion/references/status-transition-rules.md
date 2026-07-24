# Status Transition Rules

## Purpose
Define exactly when an issue or task can move from "in progress" to "done" or "closed." These rules are gates, not guidelines.

## Transition Criteria

### Bug Fix: Open → Closed
1. Reproduction case executed and documented (BEFORE evidence)
2. Fix applied and verified against reproduction case (AFTER evidence)
3. Regression test suite executed with 0 failures
4. All evidence attached to the issue closing comment
5. High-stakes changes (auth, payment, data): Peer review sign-off obtained

### Feature: In Progress → Done
1. Every acceptance criterion mapped to a verification action
2. Each verification action executed and passing
3. Feature test suite passing (unit + integration)
4. Evidence of each acceptance criterion met, attached to the task

### Hotfix: Open → Closed
1. Fix verified to stop the active incident
2. Post-incident verification ticket filed with 24-hour SLA
3. Full verification (reproduction + regression) completed in the follow-up ticket

## Anti-Patterns (Block Transition)
- **"Fixed in spirit"**: The original bug is fixed but the fix changed behavior for other scenarios
- **"Good enough"**: Output is close to expected but not exact
- **"Works in dev"**: Verified only in the development environment, not staging
- **"Tests pass but..."**: Tests pass but there's an unexplained warning or error in the output
- **"Should be fine"**: No verification done; relying on intuition

## Enforcement
Any team member can challenge a status transition by asking: "Show me the verification evidence." If the evidence doesn't exist, the transition is reversed.
