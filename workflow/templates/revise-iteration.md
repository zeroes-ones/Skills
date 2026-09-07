# revise-iteration.md — Revision Prompt for the Next Pass

**Boundary:** VERIFY(fail) → REVISE (node protocol Phase 3)
**Used by:** `iterative-task-execution` (agent preparing the next attempt)
**Reads:** diagnostics from the last pass (failure output, unmet criteria, root-cause notes) +
run-state (iteration count, budget remaining).

## Behavior rules

1. Read the last pass's diagnostics. If you cannot name the root cause of the failure, you are not
   ready to revise — escalate instead (escalate.md).
2. Fill in exactly three fields:
   - **Root cause** of the last failure (from evidence, not from mood).
   - **What changes** this pass — approach, inputs, or scope. Pick ONE primary lever.
   - **What stays the same** — so the outcome of this pass can be attributed.
3. Check the budget: iterations used vs. max_iterations; steps used vs. max_steps. If this pass
   would be the last allowed and your change is speculative, prefer escalating with the
   not-quite-ready context over spending the final pass.
4. Classify the root cause:
   - In your control (logic, inputs, method) ⇒ REVISE.
   - External (missing credentials, missing upstream artifact, ambiguous requirement) ⇒ ESCALATE.
     Retrying an external blocker is not a strategy.
5. Write the revision marker, then execute the changed approach.

## Output markers

```
[DECIDE: REVISE #<n>]
  root cause: <one line, evidence-backed>
  change: <approach | inputs | scope — the ONE lever>
  stays same: <what is unchanged>
  budget: <iterations used/max>, <steps used/max>
```

## Hard rules

- Never repeat an identical action. If the only difference from the last pass is effort or luck,
  you are at ESCALATE, not REVISE.
- Never revise without a root cause. "It failed, trying again" is budget burning with extra steps.
- Never loop past the budget. At `iterations == max_iterations` the exhaustion path fires; the
  revise marker is not an override.
- Change one lever per pass. Changing everything means the next failure teaches you nothing.
