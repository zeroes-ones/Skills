# handoff-out.md — Handoff Payload Writer (Node Exit)

**Boundary:** DECIDE(DONE) → next node (WORKFLOW-SYSTEM.md §5, payload registry)
**Used by:** `iterative-task-execution` (upstream agent at node completion)
**Reads:** node results, decisions, artifacts, verification_evidence from the verify step.

## Behavior rules

Write the terminal output of the node as the handoff payload. Every required key is populated with
content — an empty string or an empty list where real content is expected is a failure, not a value.

```
status: done | blocked | needs_review | skipped
summary: ≤200 words — what was done and the headline result
artifacts:
  - name: <artifact name>
    path: <path>
    sha: <sha256 first 12>
    type: <doc | code | test-report | config | other>
decisions:            # may be [] ONLY if truly none
  - at: <node id>
    what: <decision>
    by: <node id>
open_questions: []    # may be [] ONLY if truly none — a resolved question is a decision, log it
verification_evidence:
  <criterion>: <evidence ref>     # empty map = NOT done
context:
  files_read: [...]
  assumptions: [...]
  tried_and_failed: [...]
budget:
  tokens: <used>
  steps: <used>
  iterations: <used>
next: <suggested downstream skill / action>   # optional
```

## Hard rules

- `verification_evidence` with zero entries means you are describing a claim, not a completion.
  Go back to verify-node.md.
- `artifacts` entries must resolve to files that exist; hashes are computed, not remembered.
- The payload IS the handoff. No separate prose handoff paragraph — prose drifts, the registry
  doesn't. If you feel the need to write prose, the payload schema is missing a field; that is a
  schema problem, not a prose solution.
- Partial work goes out as `status: needs_review` with the gaps in `open_questions` — never as a
  fake `done`.
- Hand off structured state, not transcripts. Raw conversation history belongs nowhere in this
  payload.
