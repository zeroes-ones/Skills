# Walkthrough — One Review-Fix Iteration With the Boundary Templates Applied

This is the prompt-level story of pass 1 of the happy-path run, showing how the boundary templates
(`workflow/templates/`) translate the manifest into what an agent executing the `code-reviewer`
node actually does. The executor (`executors/review_board.py`) is the deterministic stand-in for
the behavior described here.

## Setup (manifest)

`code-reviewer` is a loop member of `review-fix-loop`. Its contract: produce `code-findings`;
verdict `pass` only when its review criteria are met. Loop `exit_when: review-verdict.verdict ==
pass`; budget 3 passes; exhaustion escalates to `release-gate`.

## Pass 1, step by step

### 1. INTAKE — `handoff-in.md`

The reviewer reads run-state and answers the intake contract:

```
[INTAKE: received 0 artifacts (first pass of review-fix-loop, round 1), 0 open questions]
  owe: code-findings field + a verdict for review-verdict to aggregate
  open: none carried forward
[INTAKE RESULT: proceed]
```

The runner has already recorded the handoff bookkeeping for the previous boundary, so the reviewer
knows *who* routed it here (the loop) and what payload contract the edge carries (`handoff-v1`).

### 2. EXECUTE — the skill's own workflow

The agent loads `code-reviewer/SKILL.md` (Route the Request → Ground Rules → review procedure),
reads the changed files, and produces its findings. In the deterministic executor this is the
`code-reviewer` branch: round 1 returns verdict `changes_requested` with
`evidence: ["code-reviewer-review-1"]` and diagnostics naming the issue ("naming and dead code").

### 3. VERIFY — `verify-node.md`

```
[VERIFY: 1/1 criteria evaluated]
  criterion: "Findings are accurate against the diff"
  evidence: code-reviewer-review-1 (files examined, findings recorded)
  unmet: none
[VERIFY RESULT: pass]   # review verdict itself is changes_requested — criteria for the REVIEW were met
```

Note the discipline: the node's own completion criteria (the review is *done*, well-evidenced) are
met even when the review *verdict* is `changes_requested`. The verdict is content; the done-state is
contract. `verify-node.md` exists to keep those two from being conflated.

### 4. DECIDE — node level

The node is done: status `done`, verdict `changes_requested`, evidence recorded. The runner stores
the record and increments the step budget. The reviewer's `fixer` edge is suppressed — this is a
loop member, and the loop owns the transition.

### 5. Aggregate + fixer — same protocol, different content

`security-reviewer` and `qa-engineer` run the identical protocol. Then `review-verdict` aggregates
all three verdicts (join: all). Any `changes_requested` fails the aggregate:

```
[DECIDE: REVISE #1 — root cause: code-reviewer found dead code; security + qa clean]
  change: route findings to fixer
  stays same: reviewers, gatekeeper, exit condition
  budget: 1/3 passes used
```

`fixer` executes with the three findings sets as input, applies changes, and returns
`verdict: fixed` with `evidence: ["fixer-pass-1"]`.

### 6. Loop exit check — the engine's decision

After the pass completes (5 nodes executed), the runner evaluates
`exit_when: review-verdict.verdict == pass` against the pass's aggregate verdict:
`changes_requested` → exit false, passes used 1 < 3 → **iterate**.

## Passes 2-3 and exit

- Pass 2 repeats: verdicts `changes_requested`, fixer applies more changes, aggregate fails →
  iterate (2/3).
- Pass 3: reviewer verdicts turn `pass` (criteria met), aggregate passes. Exit condition true →
  **loop exited**. Now — and only now — the members' outgoing edges fire:
  `fixer.status == done` → `release-gate`, carrying the `handoff-v1` payload with the fix report
  and the aggregate verdict as evidence.

### 7. Gate — human judgment, artifact-fed

`release-gate` requires `fix-report` + `review-verdict` artifacts to exist before it fires (the
`gates:` declaration enforces this). The gate approves; the run completes with a handoff record
`{from: fixer, to: release-gate, payload: handoff-v1, sha: …}`.

### 8. REFLECT — `loop-reflect.md`

```
[REFLECT: review-fix-loop]
  expected: converge by round 2
  actual: converged round 3
  delta: +1 pass (dead-code finding needed two fix rounds)
  learning: reviewer thresholds drift when the diff grows between passes — evidence discipline
            held; calibration: max_iterations 3 was exactly right this time
```

## What the exhaustion path changes

With `REVIEW_SCENARIO=exhaust`, rounds 1-3 all return `changes_requested`. After pass 3 the exit
condition is false and `passes == max_iterations` → **exhaustion**. The runner logs an `escalate`
action and routes directly to the loop's `escalate_to: release-gate` — no edge handoff, no fourth
pass, no silent stop. The escalation report (`escalate.md` structure) would carry per-pass
evidence; in the checkpoint it is visible as the log entry plus the three rounds of
`changes_requested` records.
