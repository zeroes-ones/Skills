# Completion Verification Protocol

## Objective Completion Criteria
Completion is binary: every branch has a status. "Feels done" is not a criterion.

### Verification Walk
For each branch in the decision tree:
1. Verify status is RESOLVED, DEFERRED, or ASSUMED. UNEXPLORED is a FAIL.
2. For RESOLVED: verify rationale is documented and references evidence/constraints.
3. For DEFERRED: verify resolution date and responsible person are specified.
4. For ASSUMED: verify validation plan and "if false" contingency are documented.

### Completion Dashboard
```
Total branches: [N]
  RESOLVED: [n1] ([n1/N]%)
  DEFERRED: [n2] ([n2/N]%) — resolution dates: [list]
  ASSUMED:  [n3] ([n3/N]%) — validation plans: [list]
  UNEXPLORED: [n4] — BLOCKING: complete before declaring done
```

## Anti-Pattern: The "Feels Done" Trap
- Sign: "I think we've covered everything" without walking the tree.
- Sign: "We spent enough time on this" without checking branch status.
- Sign: "The big decisions are made" while leaf decisions are unexplored.
- Response: Walk the tree. Show unexplored branches. "Partial grilling creates false confidence."
