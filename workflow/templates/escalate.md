# escalate.md — Escalation Report Prompt

**Boundary:** exhaustion (budget/stagnation) or external blocker (node protocol Phase 3)
**Used by:** `iterative-task-execution` (agent at ESCALATE)
**Reads:** attempt history with per-pass evidence, current run-state, the exhaustion target
(`escalate_to` in the manifest, or the human gate).

## Behavior rules

Escalation is a product, not an apology. Write it in this order:

```
[ESCALATE: <node id>]
  at: <iterations used/max | steps used/max | stagnation detected at pass N>
  what was tried:        # one line per pass, evidence ref each
    pass 1: <approach> -> <result> (evidence: <ref>)
    pass 2: <approach changed to> -> <result> (evidence: <ref>)
    ...
  blocker / unmet criteria:   # with the evidence they are unmet
    ...
  why here: <budget exhausted | stagnation (no delta across N passes) | external blocker>
  recommended next: <who/what should act, and what they need to act>
```

## Hard rules

- Escalation without context forces the recipient to re-derive everything — that is the failure
  mode this template exists to kill. Tried / evidence / blocker / next are all mandatory.
- Never escalate empty-handed with "help": if you have zero evidence of what was tried, you have
  not earned an escalation — but do not fabricate attempts either; report the honest state.
- Escalation is the correct outcome at the budget boundary. It is not a failure of character; it is
  the designed termination of a bounded loop.
- If `escalate_to` names a target (gate/skill), address the report to that target's decision
  frame: what does a human gate need to approve or reject? What does the fallback skill need to
  take over?
