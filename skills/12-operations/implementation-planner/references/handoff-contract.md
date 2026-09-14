# Handoff Contract

What the consuming skill or engineer needs in order to start work without asking a question.

## Minimum viable plan

| Field | Why the consumer needs it |
|---|---|
| Task id + title | Stable reference for status and edges |
| Single deliverable | So "done" is unambiguous |
| Acceptance criteria | So done can be judged without the author |
| Verification command | So done can be checked mechanically |
| `blocked_by` | So the consumer knows what must finish first |
| Wave | So scheduling is mechanical |
| Collision surface | So parallel safety is preserved downstream |

## The no-questions test

A plan is complete when the receiver can start **the first task** without asking anything. If they
must ask "what does done look like?" or "can I start this?", the plan is not finished.

## Handing off to different consumers

- **`iterative-task-execution`** needs tasks ordered and each independently verifiable.
- **`project-manager`** needs waves, the critical path, and sizes.
- **`scrum-master`** needs right-sized items with acceptance criteria.
- **`technical-program-manager`** needs cross-team edges made explicit.

## Failure modes of handoff

- **Prose instead of structure.** The plan reads well but cannot be scheduled or automated.
- **Missing edges.** The consumer re-discovers ordering the hard way, mid-sprint.
- **Criteria left implicit.** "Done" becomes the author's opinion, and the author has moved on.
- **No first task identified.** The receiver stalls on day one.
