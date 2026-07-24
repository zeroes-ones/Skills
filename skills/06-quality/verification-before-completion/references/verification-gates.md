# Verification Gates

## Purpose
Define pass/fail criteria for each verification phase. A gate is not a suggestion — it blocks progress until met.

## Gate Definitions

### Gate 1: Reproduction Gate (Phase 1 → Phase 2)
- **Pass**: Bug reproduced using exact reporter steps. Failure evidence captured.
- **Fail**: Cannot reproduce. Steps are incomplete, environment mismatch, or bug is intermittent.
- **Fail Action**: Request clarification from reporter. Do not proceed.

### Gate 2: Fix Verification Gate (Phase 3 → Phase 4)
- **Pass**: Reproduction case now produces expected output. Output matches acceptance criteria.
- **Fail**: Reproduction case still fails, OR passes but with wrong output, OR passes for wrong reason.
- **Fail Action**: Re-examine the fix. Check if the correct code path was modified.

### Gate 3: Regression Gate (Phase 4 → Phase 5)
- **Pass**: All existing tests pass. No new warnings or errors. Dependent module tests pass.
- **Fail**: Any test fails. Any new warning appears. Any dependent module test fails.
- **Fail Action**: Investigate and fix regressions. Re-run from Phase 3 after fix.

### Gate 4: Evidence Gate (Phase 5 → Done)
- **Pass**: Before evidence, after evidence, and test suite results attached to issue/PR.
- **Fail**: Missing any piece of evidence. Evidence doesn't match reproduction case. Links are broken.
- **Fail Action**: Collect missing evidence. Do not close without it.

### Gate 5: Status Transition Gate (Done column)
- **Pass**: All four gates above passed. Anti-rationalization check passed. Peer review sign-off (if high-stakes).
- **Fail**: Any prior gate failed. Rationalization detected. No peer review for high-stakes change.
- **Fail Action**: Return to the failed gate. Do not move the card.
