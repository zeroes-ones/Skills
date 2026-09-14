# Verification Recipes — the eight checks as runnable procedures

> Each recipe has an input, a command shape, an expected observation, and the failure it
> discriminates. Run them in order; do not proceed past a failure.

---

## Recipe 1 — Fire case

**Question:** has this check ever been observed failing?

```
INPUT        an injected defect of the class the check claims

COMMAND      <the check, with its exact scope flags>
             (plus, for a drift check: append a deliberate marker to the artefact first)

OBSERVE      · non-zero exit code
             · the finding text, naming the injected location
             · the restoration step (remove the injection)

DISCRIMINATES  a working check from a disabled, blind, or wrong one

FAILS WHEN   exit is 0, or the finding names nothing, or the exit is non-zero for
             an unrelated reason (check the message, not just the code)
```

Record the fixture, not just the result. A fire case that is not kept in the suite expires at the
end of the session.

---

## Recipe 2 — Silent case

**Question:** does this check stay away from legitimate input?

```
INPUT        · the canonical correct form
             · the nearest legitimate neighbour of the violation
             · a documented exemption (proves the allowlist suppresses)
             · a file the scope should exclude
             · empty or trivially small input

COMMAND      <the check>

OBSERVE      zero findings; and if the check supports it, a count of files evaluated

DISCRIMINATES  a precisely scoped rule from one that flags a family

FAILS WHEN   a legitimate input produces a finding — this is the direction whose
             failure gets the rule deleted, and it is the direction usually untested
```

---

## Recipe 3 — Negative control: input

**Question:** is the check parsing the thing it claims to parse?

```
INPUT        a DELIBERATE SYNTAX ERROR in a file that is definitely in scope

COMMAND      <the check>

OBSERVE      · a parse error, OR
             · a changed finding set, OR
             · any output that differs from the clean run

DISCRIMINATES  a check that reads from one that returns a constant

FAILS WHEN   the output is unchanged — the check is not reading this file
```

Keep the injected file small. The point is to be in scope, not to be realistic.

---

## Recipe 4 — Negative control: scope

**Question:** is the check's glob matching anything?

```
INPUT        rename the target directory, or run from a different working directory,
             or pass a prefix matching nothing

COMMAND      <the check, unchanged>

OBSERVE      "0 files checked", a path error, or an empty file list

DISCRIMINATES  a live scope from a glob that matches nothing

FAILS WHEN   the check reports "0 problems" identically to a clean tree.
             Path globs fail in the quiet direction — this is the control that
             catches it, and it is the one most often skipped
```

After the control, confirm the artefact is **current**, not merely present: a count of something only
the current source names is the cheapest discriminator between "wrong" and "stale".

---

## Recipe 5 — Anchor check

**Question:** does the check compare the level at which the bug lives?

```
INPUT        the check's source, specifically both sides of every comparison

COMMAND      grep for the comparison; ask of each side:
             "has a transform been applied to this value yet?"

OBSERVE      both sides hold FINAL EMITTED IDENTIFIERS — the names the consumer
             resolves, the keys the runtime reads, the fields the bundle carries

DISCRIMINATES  a check that can catch the bug from one that shares the bug's
               assumption with the code it validates

FAILS WHEN   either side is a pre-transform name: a raw reference string, a
             generator's intermediate identifier, a source-level spelling.
             A check that shares an assumption with the code it validates cannot
             catch a bug in that assumption
```

---

## Recipe 6 — Contradiction matrix

**Question:** does every combination of the constrained dimensions have a legal spelling?

```
INPUT        every rule constraining the declaration — including rules in OTHER
             tools, other validators, and other languages

COMMAND      enumerate the product of the dimensions each rule cares about,
             then fill each cell with a spelling satisfying ALL rules

OBSERVE      · every cell has at least one spelling → no contradiction; keep the matrix
             · an empty cell → a rule set defect, filed and narrowed

DISCRIMINATES  a coherent rule set from one whose defect lives in the intersection

FAILS WHEN   you stop at the first empty cell. Enumerate the whole product: the
             second empty cell is usually in a dimension nobody thought to name.

THEN         encode "every <dimension> has a legal spelling in every <other>" as a test
```

---

## Recipe 7 — Severity calibration

**Question:** is this rule's severity chosen from measurement?

```
INPUT        the rule, run on the CURRENT corpus (not the change, not a sample)

COMMAND      <the check> | count findings
             then triage EACH finding as real or spurious — do not estimate

OBSERVE      the pair (N findings, precision = real / N)

DISCRIMINATES  a rule ready to block from one that will be ignored

FAILS WHEN   N is large and precision is low and the rule ships at blocking severity.
             That combination teaches the team to skip gate output, and the lesson
             generalises to every gate
```

| N | precision | Action |
|---|-----------|--------|
| small | high | blocking |
| small | low | narrow the pattern, then blocking |
| large | high | fix the corpus first, then blocking |
| large | low | advisory until tiered by ownership |

---

## Recipe 8 — Wiring check

**Question:** has the check been proven in the configuration where it actually runs?

```
INPUT        the SAME injected defect as Recipe 1, executed through the real path
             (the CI job, the hook, the pipeline stage — not a local shell)

COMMAND      the real invocation, with its real scope, working directory and tool version

OBSERVE      the non-zero exit, propagated to the pipeline verdict

DISCRIMINATES  a gate from a script that has never run

FAILS WHEN   the check passes in CI because:
             · the scope glob is relative to a different working directory
             · the tool version pins a default that differs from local
             · the path is filtered out by a changed-files condition
             · the gate runs but the pipeline ignores its exit code
```

The fourth failure is the expensive one: a gate with `continue-on-error`, or one whose failure is
collected into a report rather than into the exit status, appears in the log and affects nothing.
Re-run the fire case after any change to the wiring, the scope, or the tool version.

---

## The eight checks as a pass/fail table

| # | Check | Passes when | Fails when |
|---|-------|-------------|-----------|
| 1 | Fire case | Non-zero exit observed on injected input | Never observed failing |
| 2 | Silent case | Legitimate input produces nothing | A legitimate input is flagged |
| 3 | Control (input) | Output moves when the input is broken | Output constant |
| 4 | Control (scope) | Empty scope is visible | Empty scope reads as clean |
| 5 | Anchor | Both sides are final identifiers | Either side is pre-transform |
| 6 | Contradiction | Every cell has a legal spelling | An empty cell exists |
| 7 | Calibration | Severity from measured counts | Severity from preference |
| 8 | Wiring | Fire case re-proven in the real path | Proven only by hand |

**Pass criteria:** all eight. A check that passes seven and fails one is not a control; it is a
belief with a script attached.

---

## A minimal gate specification template

Everything a check needs, in the order the eight recipes produce it:

```
CHECK            <name>
DEFECT CLASS     <one sentence>
ESCAPED INSTANCE <a real defect of this class that got past the existing signals, or "none yet">
READS            source | config | built artefact        (artefact preferred — see R7)
FIRE CASE        <input> → exit <code>, finding: <text>  (fixture path)
SILENT CASE      <input> → 0 findings                     (fixture path)
NEGATIVE CONTROL <how the check was shown to read something>
ANCHOR           comparison operands, and why each is a final identifier
CONTRADICTIONS   matrix reference, or "no overlapping rules"
FINDINGS         N on the current corpus, T real, precision T/N
SEVERITY         blocking | advisory — and the tier boundary if tiered
EXEMPTIONS       each: match, property-reason, bound
DOES NOT CATCH   <the blind spots, written down>
WIRED AT         <pipeline stage / hook>, last fire-re-proved <date>
```
