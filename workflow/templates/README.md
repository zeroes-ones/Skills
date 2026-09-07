# workflow/templates — Boundary Prompt Templates

Shared prompt fragments for the L2 node protocol (WORKFLOW-SYSTEM.md §7). They are consumed by
`iterative-task-execution` (agent running a node) and referenced by `workflow-graph-authoring`
(authors designing loops/handoffs). Each template states its boundary, its inputs, its behavior
rules, and the output markers the runner/log expect.

| File | Boundary | Encodes |
|------|----------|---------|
| `handoff-in.md` | INTAKE | Received / owed / open acknowledgment; refuse on missing artifacts or hash mismatch |
| `verify-node.md` | EXECUTE → VERIFY | Criterion ↔ evidence mapping; no evidence = not done |
| `revise-iteration.md` | VERIFY → REVISE | Root cause + ONE change + what stays same; change-or-escalate |
| `handoff-out.md` | DONE | Payload registry block (status/summary/artifacts/decisions/open_questions/verification_evidence/context/budget[/next]) |
| `escalate.md` | exhaustion / blocked | tried / evidence / blocker / recommended next |
| `loop-reflect.md` | loop complete / run end | expected vs. actual + calibration learning |

The two anti-patterns the set exists to kill:

- **Premature done** — claiming completion without artifact-level evidence. Defeated by
  `verify-node.md` (evidence map mandatory) + `handoff-out.md` (empty verification_evidence = not
  done).
- **Refinement death spiral** — passes that repeat identical actions or polish past the exit
  condition. Defeated by `revise-iteration.md` (change-or-escalate) + the code-level stagnation
  detector in the runner.

Templates are prompts, not substitutes for judgment: they force the judgment to happen at the right
moment in a stable format. Output markers keep behavior observable for evals and the decision
ledger.
