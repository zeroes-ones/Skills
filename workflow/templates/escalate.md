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

## When the escalation target is a kind: agent gate

A loop's `escalate_to` may name an **identify-agent gate** (`kind: agent`) instead of a human gate.
That is not an escalation to a person — it is a pre-human triage step. Address the report to the
gate's decision frame:

```
[ESCALATE -> identify-agent-gate: <gate id>]
  loop / reason: <loop id> | <max-iterations | stagnation | step-budget | guardrail-block>
  what was tried:        # one line per pass, evidence ref each (same shape as above)
  blocker / unmet criteria:
  channels tried so far: # pool members already led a reroute window (gate.tried)
  recommended channel:   # which pool member should lead the next bounded window, and why
  needs human if:        # the condition under which this gate should escalate to gate.escalate_to
```

The gate reroutes a bounded number of times (`max_reroutes`), each time granting the escalating
loop a fresh window with the identified channel first. Write the report so the identifying agent
can pick a *channel*, not a verdict: name the member whose change of approach would produce new
evidence. If every channel is tried, the end-state stops changing across reroutes, or the reason
is not reroutable (step-budget / guardrail-block), the gate escalates to its terminal `escalate_to`
— a human gate — with this same report attached.

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
