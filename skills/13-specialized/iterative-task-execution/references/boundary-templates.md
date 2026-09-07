# Boundary Templates — When and How to Apply Each One

Deep-dive companion to `iterative-task-execution`. The six templates live in
`workflow/templates/` and are shared by this skill and `workflow-graph-authoring`. Templates are
prompts: they do not replace judgment, they force the judgment to happen at the right moment in a
stable format.

## The six templates at a glance

| Template | Fires | Reads | Must output |
|----------|-------|-------|-------------|
| `handoff-in.md` | Phase 0 Intake | Incoming payload, run-state | Received / owed / open acknowledgment; refusal reason if artifacts missing |
| `verify-node.md` | Phase 2 Verify | Completion criteria + artifacts | Criterion → evidence map; list of unmet criteria |
| `revise-iteration.md` | Phase 3 REVISE | Diagnostics from last pass | Root cause, ONE approach change, what stays the same |
| `handoff-out.md` | Phase 3 DONE | Node results + registry | Payload with all nine registry keys populated |
| `escalate.md` | Exhaustion / blocked | Attempt history | tried / evidence / blocker / recommended next |
| `loop-reflect.md` | Phase 4 / run end | Expected vs. actual | Efficiency note + ledgered learning |

## Applying `handoff-in.md` (Intake)

Ask and answer three questions before touching the work:

1. **What did I receive?** — list the payload's artifacts and the state fields relevant to this
   node. Confirm the paths exist and the hashes match.
2. **What do I owe?** — restate this node's outputs from the manifest or the skill's contract.
3. **What did upstream leave open?** — enumerate `open_questions`; every one is either resolved
   (and logged as a decision) or carried forward. None may silently vanish.

Refusal rule: if an artifact named in the payload does not exist, or the handoff hash mismatches,
do NOT start. Report the corruption and request replay from the last verified checkpoint. Starting
anyway bakes the corruption into your output.

## Applying `verify-node.md` (Verify)

Mechanical sequence:

- Enumerate the criteria (from the `workflow:` block; in default mode, from the skill's
  Verification / Production Checklist tables plus the explicit request).
- For each criterion name the evidence: artifact path + sha, command output, checklist, or a
  named reasoning trace (for judgment criteria). Manual evidence must carry rationale.
- Produce the map as the verify marker. If any cell is empty, the criterion is unmet — full stop.

Anti-pattern to resist: mapping a criterion to *your intention* ("the code is clean") instead of
*an artifact* ("tests/run.sh exits 0; output in artifacts/test-output.txt"). If you cannot name a
file or an output, you have not verified.

## Applying `revise-iteration.md` (Revise)

Before writing the next pass, fill in three fields:

- **Root cause** of the last failure (from diagnostics — if you cannot name one, you are not ready
  to revise).
- **What changes** this pass (approach, inputs, or scope — exactly one primary lever).
- **What stays the same** (so you can attribute the outcome).

Hard rule: if the only thing you can change is the wording of "try harder", you are at ESCALATE.
The revise marker should read `[DECIDE: REVISE #2 — root cause: X; approach change: Y]`.

## Applying `handoff-out.md` (Done)

Terminal output of a completed node is the payload:

```
status: done
summary: ≤200 words — what was done, headline result
artifacts: [{name, path, sha, type}]
decisions: [{at, what, by}]            # may be []
open_questions: [...]                  # may be []
verification_evidence: {criterion: evidence}   # empty map = not done
context: files read, assumptions, things tried and failed
budget: {tokens, steps, iterations}
next: suggested downstream skill / action       # optional
```

If `verification_evidence` is empty, you are describing a claim, not a completion — go back to
Verify. The payload IS the handoff: no separate prose handoff paragraph needed (and none wanted —
prose handoffs drift; the registry doesn't).

## Applying `escalate.md` (Escalate)

Escalation is a product, not an apology. It contains, in order:

- What was tried: one line per pass, with the evidence ref for each attempt.
- The blocker or the unmet criteria with the evidence that they are unmet.
- Why the budget is the right place to stop (or why the blocker is external).
- The recommended next action: who/what should take it, and what they need.

Escalation without context forces the recipient to re-derive everything — that is the failure mode
`escalate.md` exists to kill. If your escalation does not contain a recommended next action, write
one before sending.

## Applying `loop-reflect.md` (Reflect)

At every exit (done, escalated, run end), compare expected vs. actual:

- Efficiency: passes used vs. passes allowed.
- What the diagnostics taught that the plan did not predict.
- The one learning worth writing to the decision ledger (and, for library authors, into the
  relevant skill's Gotchas).

Two minutes here compounds: it is how loop behavior stops being a mystery and becomes a pattern
library.
