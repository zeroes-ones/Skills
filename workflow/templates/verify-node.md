# verify-node.md — Completion Verification Prompt

**Boundary:** EXECUTE → VERIFY (node protocol Phase 2, WORKFLOW-SYSTEM.md §4.2)
**Used by:** `iterative-task-execution` (agent running a node)
**Reads:** completion criteria (skill `workflow:` block, or the skill's Verification /
Production Checklist tables in default mode) + the artifacts/outputs produced in EXECUTE.

## Behavior rules

1. Enumerate every completion criterion as its own line. Do not merge, drop, or "summarize"
   criteria — a criterion that disappears is a decision made by accident.
2. For each criterion, name the evidence that proves it:
   - Machine evidence: artifact path + sha, command output, test result, filled checklist.
   - Judgment evidence (design taste, trade-offs): a named reasoning trace with the limitation
     declared — never a bare checkbox.
3. Produce the criterion → evidence map as your output.
4. Verdict: every criterion met with evidence ⇒ `verify: pass`. Any empty evidence cell ⇒
   `verify: fail` with the list of unmet criteria. An all-empty evidence list ⇒ `verify: fail` —
   you have not verified anything.

## Output markers

```
[VERIFY: k/n criteria met]
  criterion: <text of the criterion>
  evidence: <artifact path + sha | command output | named reasoning trace>
  ...
  unmet: <criterion> (no evidence)
[VERIFY RESULT: pass|fail]
```

## Hard rules

- No criterion without evidence is met — ever. "The code is clean" is not evidence; "lint exits 0
  with the attached output" is.
- If you did not run the check, you do not have the evidence. Run it or mark the criterion unmet.
- If the request's explicit requirements are not all represented among the criteria, add them to
  the criteria list before verifying — the contract is the request + the skill, not the skill alone.
- Never fabricate: a fabricated evidence line is worse than an honest unmet criterion, because it
  looks like completion to every downstream consumer.
