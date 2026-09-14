# Proving a Check Fires — fire cases, silent cases, and the probe

> The core discipline of this skill: a check is not verified until its failure has been observed.
> Everything in this file is the "how", with worked examples drawn from real gate defects.

---

## The four states that produce one output

A check emits `0 problems`. That single line is produced by four structurally different states, and
their remedies have nothing in common:

| State | What is happening | How it looks from outside |
|-------|-------------------|---------------------------|
| Working | The rule evaluated the input and found nothing | `0 problems` |
| Blind | The file glob matched no files, or the working directory was wrong | `0 problems` |
| Disabled | The rule was commented out, renamed, or its config key moved | `0 problems` |
| Wrong | The rule evaluates the wrong two things, consistently | `0 problems` |

The first is the only state you want, and the output is identical in all four. This is why a clean
run is evidence that a process executed, never evidence that an assertion holds.

**The negative control exists to discriminate state 1 from state 2.** Injecting a violation
discriminates state 1 from states 3 and 4. You need both operations, and they are cheap.

---

## Fire case

A fire case is an **injected defect of exactly the class the check claims**, plus the captured
non-zero exit and the finding text.

```
Fire case anatomy:
  1. The defect            — an instance of the class, injected deliberately
  2. The command           — the exact invocation, with its scope flags
  3. The observed result   — non-zero exit, and the finding text it printed
  4. The restoration       — how the injected defect was removed
  5. The fixture           — the case kept in the suite so the proof is repeatable
```

Step 5 is what separates a gate from an anecdote. A gate proven once by hand, in an interactive
terminal, on a machine with a different file set, with a manual `rm` afterwards, is a gate whose
proof expires at the end of the session.

### The restoration is not optional

An injected defect that is not removed is a defect. Real instances of this failure:

* A deliberate `// deliberate drift` injection left in place would be committed as drift.
* A two-struct probe file left in the tree becomes a compilation unit.
* A test that asserts the gate fails on bad input, then leaves the bad input in the fixture
  directory, becomes the case the gate fails on by default in the next run.

Keep injections inside a dedicated fixture directory, or generate them and remove them in the same
script with a `trap`.

### The fire case must match the violation's common spelling

The most instructive single failure in the source material: a motion gate matched
`slideInHorizontally(`. Kotlin's trailing-lambda form — `slideInHorizontally { width -> width }` —
is the *more likely* way to hand-roll the same slide, and it passed straight through the gate. The
gate was correct in form and blind in practice.

> The gate was found by writing a probe and watching it stay silent, which is the only way to know
> a gate fires. A probe is an input you construct *for the purpose of being caught*.

**Probe construction rule:** write the input the way a developer would actually write the violation,
not the way the rule's author would. If the rule was written by reading the linter's own pattern,
the probe will inherit the same assumption.

---

## Silent case

A silent case is input that is **legitimate** and that the check must leave alone. It exists to
catch the opposite failure: a rule broad enough to flag correct code.

Without a silent case, a rule's false-positive rate is discovered in the corpus, after it has been
shipped, by a team whose trust in the gate is the thing being spent.

### What belongs in a silent case set

| Input kind | Why it belongs |
|-----------|----------------|
| The canonical correct form | The rule must not fire on the thing it is protecting |
| The nearest legitimate neighbour | The rule's boundary is exactly here; the neighbour is where over-reach shows |
| A documented exemption | Proves the allowlist actually suppresses; an unproven allowlist is a hope |
| A file the rule's scope should exclude | Proves the scope glob works — this is the negative control as well |
| Empty / trivially small input | Catches rules that fire on absence rather than on violation |

### The asymmetry that causes most rule deletions

Rules are typically tested only in the failing direction: "does it catch the bad thing?" The
question never asked is "does it stay quiet on the good thing?" — and that is the direction whose
failure gets a rule deleted, because the cost of a false positive lands on the person who has to
explain it at 2am.

```
A rule that fires only on real defects              → believed, kept
A rule that fires on 20% legitimate code            → triaged, then `continue-on-error`
A rule that fires on 80% legitimate code            → deleted, and the defect class reopens
```

The last transition is the expensive one, because the deletion removes the coverage that the rule
*badly* provided, and nothing replaces it.

---

## Negative control

A negative control answers one question: **was the check reading anything at all?**

Three ways to build one, in ascending order of confidence:

1. **Break the input.** Introduce a syntax error into the file the check parses. A checker that
   reads it will error or report differently; one that reads nothing is unchanged.
2. **Break the scope.** Rename the directory the glob points at, or run from a different working
   directory. A scope-correct check reports zero files; a scope-blind check reports `0 problems`
   as though the tree were clean.
3. **Break the check itself.** Change one pattern in the checker to something impossible. If the
   output does not change, the pattern was never being evaluated.

Option 3 is the one that catches the most severe class: a check whose rules are parsed but whose
result is aggregated incorrectly, so the findings are discarded between the rule and the exit code.

> A compiler run must be preceded by a negative control when the result is "0 errors" — otherwise
> the check may be vacuous. A deliberate type error proved the type checker was genuinely reading
> the files.

---

## The idempotency-plus-detection pair

For any check that compares a generated artefact against its source (a drift check, a freshness
gate, a `--check` mode), two separate assertions are required and they are often conflated:

| Assertion | Statement | Failure it catches |
|-----------|-----------|-------------------|
| **Idempotency** | Two consecutive runs report no drift | A generator with nondeterministic ordering, timestamps, or map iteration |
| **Detection** | An injected change produces a non-zero exit | A `--check` that computes a diff and then exits zero regardless |

A drift check that always reports drift is as useless as one that never fires: the first trains the
team to ignore the output, the second provides no coverage. Both were verified in the source corpus
by injecting a deliberate drift marker and confirming a non-zero exit.

```
# Idempotency: run twice, diff the outputs
$ gen --check && echo "pass 1 clean"
$ gen --check && echo "pass 2 clean"

# Detection: inject and observe the failure
$ printf '// deliberate drift\n' >> artifacts/generated.ts
$ gen --check; echo "exit=$?"     # MUST be non-zero
$ git checkout -- artifacts/generated.ts
```

---

## Worked example: two gates that had never fired

Both of these are real, from the repository this skill's pattern came from. They are the argument
for the whole discipline.

### Gate A — grep instead of exit code

A gate shelled out to a tool, captured its output, and then grepped the output for a failure
substring rather than trusting the exit code. The tool's failure mode changed its message text;
the substring stopped matching; the gate reported success while the tool was failing. The exit
code had been correct the entire time.

**Design lesson:** the tool's exit code is the contract. Message text is presentation. A gate that
parses presentation to infer status is coupled to the least stable part of the interface.

### Gate B — counting headings instead of checking for trees

A gate verified that a document contained at least three decision trees by counting `###` headings
inside the section. Eighteen documents shipped with `### Decision Tree N:` headings, zero branch
characters, and no diagram — a compliance paragraph wearing a tree's heading.

**Design lesson:** a structural check must assert the property that makes the artefact useful, not
a proxy that correlates with it. "Has three sub-headings" and "contains a branching diagram" are
different assertions, and only the second is the one the rule was written to protect.

Both gates passed for months. Neither could have been caught by reading the gate, because reading
confirms what the code says, and both codes said what their authors intended. What catches this
class is injecting the defect the gate is supposed to fail on and watching it stay green.

---

## The probe-first discipline, condensed

1. Write the violation the way a developer would write it.
2. Write the legitimate neighbour.
3. Run the check on both.
4. If the first is not caught or the second is caught — fix the check, not the fixture.
5. Keep both as fixtures so the proof survives the next refactor of the check.
