# Negative Controls — how to know your check read anything

> A negative control is the cheapest high-value practice in verification design and the one most
> often skipped, because its absence is invisible: a vacuous check produces exactly the output a
> working one produces.

---

## Why "0 problems" is a low-information result

Information is a function of how many states could have produced the output. A check that prints
`0 problems` has at least four producing states (working, blind, disabled, wrong), so the output
narrows the world very little. A check that prints a finding on injected input has two producing
states (it works, or something coincidental failed), which is a large reduction.

The practical consequence: **the first thing to do with a new check is not to run it on the
codebase. It is to make it fail.**

```
run order that produces knowledge:
  inject a defect  → observe non-zero   (proves the check can fail)
  restore          → observe zero       (proves the check is not stuck failing)
  break the scope  → observe noise/error (proves the check reads something)
  run on the tree  → observe 0          (NOW the zero carries information)

run order that produces false confidence:
  run on the tree  → observe 0          (four possible states, one output)
  ship it
```

---

## The three negative controls

### Control 1 — Break the input

Introduce a defect into the file the check parses, then re-run.

| The check's behaviour | What it proves |
|-----------------------|---------------|
| Errors with a parse failure | It reads and parses; a successful parse on clean input is meaningful |
| Reports the injected defect | It reads, parses, and evaluates; the strongest outcome |
| Unchanged `0 problems` | It is not reading this file — investigate the path or the glob |

Choose the defect so that it is *definitely* in scope. Injecting a defect in an excluded path and
observing silence proves nothing; that is the scope working.

### Control 2 — Break the scope

Rename the target directory, or run the command from a different working directory, or pass a
prefix that matches nothing.

A correctly scoped check reports "0 files checked" or errors on a missing path. A check whose scope
is silently empty reports `0 problems` — the same output as a clean tree. Path globs fail in the
quiet direction, which is why this control matters more than it looks.

The real-world variant: a generated artefact is produced by a script whose glob once matched one
file and now must match 138. The generator still ran, the config still listed the artefact, and the
build still succeeded — the configuration was right and the artefact was stale. **A check that
reads the artefact inherits the artefact's staleness**, so scope controls and currentness controls
are two halves of the same question.

### Control 3 — Break the check

Change one rule's pattern to something impossible (a string that cannot appear), keep everything
else the same, and run.

| Result | Interpretation |
|--------|----------------|
| Output changes (the rule stops firing) | The rule was live; the plumbing is honest |
| Output unchanged | The rule's findings were being discarded somewhere between evaluation and exit |

This is the control that catches the aggregation defect: a check that evaluates all rules
correctly and then exits zero because the exit-code branch reads the wrong variable. No amount of
input-breaking finds it, because the findings are never surfaced.

---

## What a negative control is not

**It is not a test of the check's logic.** A control proves the check is wired — that it reads, that
its findings reach the exit code. Whether the *rule* is correct is a separate question, answered by
the fire case and the silent case.

**It is not a substitute for triaging the first run.** A check can be perfectly wired and produce
28 findings that are all false positives. The control passes, the rule is wrong.

**It is not a one-time act.** Controls decay: a refactor moves the check behind a different scope,
a config key is renamed, a dependency's default changes. Re-run controls when the check's
invocation changes, and keep the control as a fixture rather than a memory.

---

## The control matrix

Use this to decide which control a given check needs.

| Check reads | Control 1 (break input) | Control 2 (break scope) | Control 3 (break check) |
|-------------|-------------------------|-------------------------|-------------------------|
| Source files in a tree | Required | Required — globs are the common failure | Required for hand-rolled checkers |
| A config or manifest | Required | Rarely applicable | Required |
| A generated artefact | Required | Required | Required |
| A shipped/installed artefact | Required | Required — and confirm currentness first | Required |
| A network or external service | Required (mock a failure) | Required (point at nothing) | Required |

The "confirm currentness" cell is not optional for built artefacts. In the source corpus, a fix was
implemented correctly and the device still showed the old behaviour, because the installed build
predated the edit. The decisive check was the **shipped resource table**: the installed package
carried 24 entries of a named string family while the source contained 25. An artefact that cannot
render a value the current source names is not the current source.

> **"Wrong" and "stale" look identical from outside.** Both present as "the fix did not work". The
> discriminator is a count of something the current source names, read from the shipped output.

---

## Control design for probabilistic and statistical checks

Not every check is deterministic. Coverage gates, sampling-based scanners, and timing-sensitive
checks have a distribution rather than a value, and the control logic changes:

| Check kind | Control | Note |
|-----------|---------|------|
| Deterministic rule | Inject and observe the exit code | The simple case |
| Sampling / subset scan | Inject into a file guaranteed to be sampled, or force the sample set | The control itself must be deterministic |
| Threshold on a measurement | Move the measurement across the threshold, not the threshold | Moving the threshold tests the comparison; moving the measurement tests the pipeline |
| Timing / flakiness | State the precondition explicitly | A result that depends on *when* it was read is not a fact |

**The flaky-test instance:** UI tests tapped immediately after `launch()`, racing an animated
splash — green in isolation, red in a full run. The fix was not a retry but making the precondition
explicit: wait for the control to exist **and** be hittable. Retries hide the race; an explicit
precondition removes it.

---

## The four states, restated as a decision procedure

```
The check reports 0 problems. Which state is it in?

  Delete the glob / point it at an empty dir and re-run.
  ├── Output changes (0 files, or an error) → scope is live. Continue.
  └── Output unchanged                      → BLIND. Fix the scope first.

  Inject a violation of the claimed class and re-run.
  ├── Non-zero exit with a finding          → the check works. Continue.
  └── Still 0 problems                       → either DISABLED or WRONG.
      ├── Comment out one rule, re-run: does anything change?
      │   ├── No  → DISABLED (rules not evaluated, or findings discarded)
      │   └── Yes → WRONG. The rule evaluates the wrong two things. Go to
      │             Rule 3 in SKILL.md: re-anchor on final emitted identifiers.
```
