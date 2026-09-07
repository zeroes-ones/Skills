# Workflow Payload Registry — Reference

Canonical handoff payload for workflow manifests (WORKFLOW-SYSTEM.md Section 5). This file is the
agent-handoff-protocol lens on the registry: where each key maps to this skill's existing contract
concepts, and how manifests enforce it.

## The nine keys

| Key | Required | Contents | agent-handoff-protocol anchor |
|-----|----------|----------|-------------------------------|
| `status` | yes | `done` \| `blocked` \| `needs_review` \| `skipped` | Handoff contract lifecycle state |
| `summary` | yes | ≤ 200 words: what was done, headline result | Pruned context — the distilled state |
| `artifacts` | yes | `[{name, path, sha, type}]` | State serialization: artifact manifest |
| `decisions` | yes | Decisions with rationale (`[]` allowed) | Decision Gate Ledger entries |
| `open_questions` | yes | What the next node must resolve (`[]` allowed) | Open questions accumulation (proactive trigger 5) |
| `verification_evidence` | yes | Criterion → evidence map; empty = not done | Completion claims must be checkable |
| `context` | yes | Files read, assumptions, things tried and failed | Context pass-through protocol elements |
| `budget` | yes | Tokens / steps / iterations used by this node | Token-usage accounting across handoffs |
| `next` | optional | Suggested downstream skill / action | Recommended routing |

Together these preserve the five context elements that must survive any delegation (original
problem, what was tried, log/error output, file paths with line numbers, hypothesized root cause):
they live in `summary` + `context`, with file paths under `artifacts`.

## Writing discipline (handoff-out)

- Artifact entries must resolve to real files; `sha` is computed, not remembered.
- An empty `verification_evidence` map means the node is describing a claim, not a completion —
  go back to verify-node before writing the payload.
- `open_questions` may be empty only when truly none exist; a resolved question is a `decisions`
  entry, not silence.
- Hand off structured state, never raw transcripts.

## Reading discipline (handoff-in)

- Confirm artifact paths exist and hashes match before starting. Mismatch ⇒ report corruption;
  request replay from the last verified checkpoint. Never start on an unverifiable payload.
- Enumerate upstream `open_questions`; each is resolved (logged as a decision) or carried forward.
  None may silently vanish.
- If `summary` disagrees with the artifacts received, trust the artifacts and flag the disagreement.

## Enforcement layers

| Layer | What it checks | Where |
|-------|----------------|-------|
| Manifest authoring | Registered payload keys ⊆ canonical registry; edge payload names resolve | `scripts/validate-workflows.py` (V8) |
| Node execution | Payload keys populated at handoff; empty evidence = not done | `workflow/templates/handoff-out.md`, `verify-node.md` |
| Boundary integrity | Handoff hash verified on receipt; mismatch aborts | `scripts/workflow-runner.py` + run-state rules R1-R6 |
| Behavior | Evals assert payload completeness across handoffs | `evals/tier3-behavioral/` loop-graph scenarios |

## Registry drift

If a flow needs a key beyond these nine, that is a registry change, not a one-off payload extension.
Propose the key, update `workflow/schema/` + this reference + the validator's canonical set, then
adopt. Ad-hoc keys are how handoffs stop being contracts.
