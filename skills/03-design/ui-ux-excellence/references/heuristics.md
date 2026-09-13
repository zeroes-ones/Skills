# Heuristics

<!-- STANDARD: 3min -- the ten heuristics with scoring criteria and evidence requirements -->

## How to use these

Each heuristic below carries: what it means, the failure it predicts, the evidence a score
requires, and the common false positive. Score 0–4. **A score below 3 is a blocking finding and
requires a reproduction step** (R6).

The heuristic set is Nielsen's ten usability heuristics; the clause wording is the standard's,
the scoring criteria and evidence requirements here are this skill's working method.

## The scoring scale

| Score | Meaning |
|---|---|
| 0 | Heuristic violated, users blocked or misled |
| 1 | Violated; workaround exists but users must discover it |
| 2 | Partly honoured; some screens/flow segments violate it |
| 3 | Honoured; any exception is deliberate and recorded |
| 4 | Honoured and actively reinforced by the interface's own patterns |

## Heuristic 1 — Visibility of system status

**Means:** the interface keeps the user informed about what is happening, in reasonable time.

**Failure it predicts:** users repeat actions, abandon, or lose confidence, because nothing told
them anything happened.

**Evidence required:** a screen, a step, and what the user does *not* learn within the patience
threshold. Screenshot or recording of the un-signalled state.

**Common false positive:** a fast operation with no indicator is correct — an indicator that
appears for a fraction of a second is a flicker, not status. Only flag when the wait is
perceivable (Decision Tree 4).

## Heuristic 2 — Match between system and the real world

**Means:** the interface speaks the user's language — their terms, their order, their mental
model — rather than the system's internals.

**Failure it predicts:** users cannot map the interface to their goal, so they avoid it or
guess.

**Evidence required:** the exact string, the user-facing concept it should have named, and where
the user's vocabulary differs. Quote the copy.

**Common false positive:** a technical audience may legitimately prefer precise internal terms.
State the audience assumption rather than "fixing" domain language.

## Heuristic 3 — User control and freedom

**Means:** users can undo, exit, and back out. Emergencies have a well-marked exit.

**Failure it predicts:** users feel trapped and abandon rather than navigate.

**Evidence required:** the flow segment where no exit exists — an unrecoverable action, a modal
with no dismiss, a state the user cannot leave except by restarting.

**Common false positive:** a deliberate commitment point (payment) is not a control failure, as
long as it is reversible or clearly framed.

## Heuristic 4 — Consistency and standards

**Means:** the interface follows its own conventions and the platform's, so users do not have to
wonder whether different words or situations mean the same thing.

**Failure it predicts:** users transfer a learned behaviour to a place where it does not apply.

**Evidence required:** two concrete places that disagree (same action, different label or
position), or a platform convention departed from without a recorded rationale.

**Common false positive:** deliberate platform divergence is correct. Check
`platform-hig-architect` before flagging a convention difference.

## Heuristic 5 — Error prevention

**Means:** the design prevents problems before they occur, rather than reporting them after.

**Failure it predicts:** avoidable errors — wrong input, accidental irreversible actions,
mis-set options.

**Evidence required:** the input or action, the foreseeable mistake, and the absence of a
constraint, default, confirmation or undo.

**Common false positive:** not every error is preventable; external-state errors belong to
recovery (Decision Tree 1), not prevention.

## Heuristic 6 — Recognition rather than recall

**Means:** the interface makes options, actions and information visible, so the user does not
have to remember across screens or states.

**Failure it predicts:** users forget a value, re-navigate to check something, or guess.

**Evidence required:** the step where the user must hold information from elsewhere — a value
from a previous screen, a code they must re-enter, a state they cannot see.

**Common false positive:** an expert tool may legitimately rely on trained recall. State the
audience.

## Heuristic 7 — Flexibility and efficiency of use

**Means:** the interface serves both the novice and the experienced user — accelerators that the
novice never sees but the expert can use.

**Failure it predicts:** experienced users are slowed to the novice's pace and route around the
product.

**Evidence required:** the repeated task, the number of steps, and the absence of a shortcut,
recent-items list, or bulk action.

**Common false positive:** this is the heuristic most legitimately traded away for a small or
single-purpose product. Record the trade rather than forcing accelerators.

## Heuristic 8 — Aesthetic and minimalist design

**Means:** the interface shows what is relevant and needed, not more.

**Failure it predicts:** the signal is drowned by noise; the user cannot find the relevant thing.

**Evidence required:** a **count** — how many equally-weighted items compete at a given step, or
how much of the screen carries no task-relevant information. This is the heuristic most often
scored by taste; the count is what makes it evidence (R1).

**Common false positive:** information density is correct for expert tools. The defect is
competition for the primary task, not density per se.

## Heuristic 9 — Help users recognise, diagnose, and recover from errors

**Means:** error messages are expressed in plain language, state the problem precisely, and
suggest a constructive solution.

**Failure it predicts:** users cannot fix the problem and abandon, or repeat the failing action.

**Evidence required:** the exact message, the user situation it fails to name, and the missing
next action. Three checks: does it name the problem? Does it name the remedy? Is the user's work
preserved?

**Common false positive:** none worth tolerating. This is the most-neglected heuristic and the
one where trust is decided.

## Heuristic 10 — Help and documentation

**Means:** help is available, findable, focused on the user's task, and concise.

**Failure it predicts:** users cannot complete a task they would otherwise finish, and contact
support instead.

**Evidence required:** the task, the point of confusion, and where help should have been
available (in context, not in a documentation site).

**Common false positive:** a genuinely self-evident interaction needs no help. Absence of help
is only a defect where a real user stalls.

## The scorecard

| # | Heuristic | Score (0-4) | Evidence (screen + step) | Observed behaviour | Finding |
|---|---|---|---|---|---|
| 1 | Visibility of system status | | | | |
| 2 | Match to the real world | | | | |
| 3 | User control and freedom | | | | |
| 4 | Consistency and standards | | | | |
| 5 | Error prevention | | | | |
| 6 | Recognition over recall | | | | |
| 7 | Flexibility and efficiency | | | | |
| 8 | Aesthetic and minimalist design | | | | |
| 9 | Error recognition and recovery | | | | |
| 10 | Help and documentation | | | | |

**A row with a score and no evidence column filled is not a score.** That is R6, and it is the
line between an evaluation and an opinion.

## Which heuristics fail most often

Observed pattern across evaluations of shipped products, in rough order of frequency:

| Rank | Heuristic | Why it fails |
|---|---|---|
| 1 | 9 — Error recovery | Errors are written by the system's author, in the system's terms, with no remedy |
| 2 | 1 — System status | States were never designed; the wait was never considered |
| 3 | 5 — Error prevention | Prevention requires anticipating a mistake, which requires the task model |
| 4 | 6 — Recognition over recall | Values are held across screens because nobody counted the memory load |
| 5 | 3 — User control | Exits and undo arrive late, after the flow is built |

The pattern is instructive: the four most-failed heuristics are all about the *unhappy* paths.
Interfaces are designed for the happy path and reviewed on the happy path, so every defect lives
where nobody looked.

## Reporting

For each finding:

```markdown
### H9-01 — Error after failed save names the system, not the situation
- **Heuristic:** 9 — Error recognition and recovery
- **Score:** 1
- **Screen / step:** Invoice editor → Save with a stale session
- **Reproduce:** open two tabs, sign out in one, save in the other
- **Observed:** "Error 401: Unauthorized". The draft remains in the editor but nothing says so.
- **Consequence:** the user cannot tell whether their work survived, so they retype it; measured
  retry rate on this path is 41% [ESTIMATED].
- **Fix:** name the situation ("Your session expired"), state that the draft is preserved, and
  offer "Sign in and save".
- **Metric:** retry-without-retype rate; owner: checkout team; review: next release.
```

Every field is required. The `Reproduce` line is what makes the finding disputable and fixable
rather than a matter of opinion.
