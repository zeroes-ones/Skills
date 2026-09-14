# The Discovery Ledger

Every contract finding should record **what found it**. The column is small and it changes how a
team spends its verification effort, because it makes visible which class of defect required a
person to ask a question and which class a machine could have caught.

## The column

| Finding | Found by | Root cause |
|---|---|---|
| A spec covered 41 of 114 paths | Running the gap check | Its reverse direction was a deliberate no-op |
| Generated Python failed `py_compile` on line one | `py_compile` | The file header used `//` comments |
| An entitlement file and setting were both correct, but the signature carried an empty dict | `codesign -d --entitlements` on the built app | Entitlements are granted by a provisioning profile, not by a plist |
| A localisation directory was declared but never a build target | Reviewing the build configuration | Translations shipped nowhere; the only defect of the set with no build signal |
| **Android never persisted a session at all** | **Asking "who WRITES the token?"** | The port declared `hasSession` and `clear` but no `save` |

Four of the five were found by a tool. One was found by a question — and it is the most serious
defect in the corpus, because it was invisible to every check the project ran.

## Why the column matters

The source corpus states its own organising ratio:

> **8 defects found by compilers, 2 more by decoding real data, 1 by reading** — zero of 22 found by
> careful review.

That ratio is not an argument against review. It is an argument about **where to spend the next unit
of verification effort**, and it is only visible if each finding records what found it. Without the
column, every finding looks equally discoverable, and the natural conclusion is "be more careful",
which is the strategy the ratio shows to be the weakest one available.

The column produces three decisions:

| If most findings came from… | Then |
|---|---|
| Compilers | The build is doing its job. Add nothing; the rung-2 checks are adequate |
| Tests and gates | Those checks are earning their place. Find whether any of them was proven to fire |
| **Asking a question** | **That question is a candidate for a mechanical check.** This is the signal to act on |

The third row is the point. A question that repeatedly finds defects is a check that has not been
written yet.

## From question to gate

The transferable question in this skill —

> *"who WRITES this?"*, asked of any state something else depends on reading

— was a question first. It found a port with no `save`, on one platform, in a codebase with 214
tests and five gates. Whether it becomes a mechanical check depends on the codebase: if contracts
are declared in a parseable form and state accessors follow a naming convention, the check is a
script. If not, it stays a review question — and then it needs to be in the checklist, not in a
person's head.

The intermediate artefact is the **behaviour-named test table**: one test per named behaviour, each
cross-referenced to the defect it guards. It carries the question forward without pretending it has
been mechanised.

## Honest assessment: name what you have NOT verified

The ledger only works if it is honest about its own blind spots. Three practices make it honest:

1. **An explicit unverified section.** State the checks you did not run, the paths you could not
   reach, and the inventory you could not complete. "Unverified" is a result.
2. **"Not built yet" rather than a stub.** A placeholder that looks finished is worse than an
   admitted gap, because it consumes the attention that the gap should attract.
3. **A count that does not soften.** Reporting "P0 gates closed: 0 of 85" is more useful than
   reporting the shape of the plan. Report the ratio you actually have.

Applied here: if the codebase could not be fully searched for call sites, the operation inventory is
marked INCOMPLETE. If a finding rests on an assumption about behaviour rather than an observed call
site, it is tagged `[ESTIMATED]`. A ledger that rounds its own gaps away is not a ledger.

## Rules

* **Every finding gets a Found by entry.** Include "reading" where that is the honest answer — it is
  the entry that carries the most information.
* **A repeated question is a check waiting to be written.** Track which questions recur; the second
  occurrence is when to automate.
* **Publish the ratio, not a narrative.** "Zero of 22 found by careful review" is actionable.
  "Review caught several issues" is not.
* **Name the unverified.** A list of what was not checked is part of the deliverable.
* **Do not let a stub stand in for a gap.** Admitting the gap is cheaper than the defect the stub
  conceals.
