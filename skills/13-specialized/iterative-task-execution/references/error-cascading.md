# Error Cascading — the failure that iteration does not fix

> Retrying is not the same as diagnosing. An error cascade is a loop that varies on every pass
> without ever naming the cause, and it burns the most budget for the least information (G7).

---

## What an error cascade is

The loop has a failure. Instead of asking *why*, the agent changes something and tries again:

```
tool errors  → try a different parameter   → errors
             → try a different flag        → errors
             → try a slightly different order → errors
             → ... ten passes, 40k tokens, mechanism still unnamed
```

Every pass is *different*, so stagnation detection (no delta across passes) does not fire — and that
is what makes this failure worse than an ordinary loop. The output of each pass changes, so the loop
looks alive while the underlying error is completely unfixed. **The signal is not "the pass repeated";
it is "the error repeated while the parameters moved."**

## Two shapes

| Shape | Where it happens | Why it compounds |
|-------|------------------|------------------|
| **Single-chain cascade** | One agent/user loop retrying a failing tool call | The same flawed reasoning evaluates each retry, so it cannot see its own error; failure detection from inside the chain that produced the failure is the hard part |
| **Cross-boundary cascade** | A failure in step A is passed to step B as if it were a valid input | B optimizes for internal consistency with a false premise, so the output is coherent and wrong; the error is now several steps from its cause |

The single-chain shape is a **budget** failure (the loop never converges). The cross-boundary shape is
a **correctness** failure (it converges on something false). The second is the more expensive of the
two, because it can exit "successfully".

## Detection signals

| Signal | Reading |
|--------|---------|
| Parameters differ pass-to-pass, error text does not | Error cascade (G7). Stop varying; diagnose. |
| Same error text, different stack/site each time | You are moving the failure around, not fixing it — the cause is upstream of where it surfaces |
| A downstream artifact is internally consistent but externally false | Cross-boundary cascade: a failed step's output was consumed as input |
| Pass count rises while the *cause* is never written down | You have a sampler, not a loop |
| "It worked this time" with no change to the cause | Flaky symptom, unfixed mechanism; it will return |

## The rule

**Name the mechanism before varying anything (G7).**

```
error occurs
  ├── Can you state the failure mechanism in one sentence?
  │   ├── Yes → change the ONE lever that mechanism implies; a pass that changes
  │   │        anything else is not a response to this error
  │   └── No  → one bounded DIAGNOSTIC pass is allowed: reproduce the error
  │             deliberately, read the full message (not the first line),
  │             inspect the actual state, and name the mechanism.
  │             ├── mechanism named → now you may revise
  │             └── still unnamed     → ESCALATE with the error text. Do not guess again.
  └── Is the error crossing a boundary (A's output → B's input)?
      └── Yes → verify AT the boundary, not only at the end: B checks A's artifact,
                and the check is done by someone other than A
                (a producer verifying itself is a draft, not verification —
                 see `verification-independence-engineer`)
```

## Why the boundary case matters

A self-check cannot catch this class of failure, because the producer's check inherits the producer's
error — the exact mechanism `verification-independence-engineer` names. So the defence against a
cross-boundary cascade is structural: a distinct verifier at the edge, seeing the artifact and its
evidence rather than the producer's reasoning. Within a single node, the same principle applies in
miniature: the *verify* phase must be able to fail the *execute* phase's output, or it is decoration.

## Anti-patterns

| ❌ | ✅ |
|----|----|
| "Try a different value" with no stated cause | Name the mechanism, then change the one lever it implies (G7) |
| Treating a changed error message as progress | Check whether the error *moved* or was *fixed*; moving is not progress |
| Consuming an upstream failure as a valid input | Verify at the boundary, by a verifier other than the producer |
| Escalating with only the last error | Escalate with the error text, the passes tried, and what each was meant to change |
