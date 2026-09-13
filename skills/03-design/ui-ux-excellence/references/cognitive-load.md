# Cognitive Load

<!-- STANDARD: 3min -- decision cost, choice architecture and recognition over recall -->

## Why count decisions

"Cluttered" is unarguable; "four equally-weighted choices, three of which apply to 8% of users"
is arguable, fixable and measurable. The discipline of this file is to replace adjectives with
counts wherever a count is possible.

The underlying claim: **every decision a user must make costs time, attention, and a chance to
choose wrong.** Reducing the number of necessary decisions improves completion more reliably than
improving the appearance of the decisions themselves.

## The three loads

| Load | What it is | Reduce by |
|---|---|---|
| **Intrinsic** | Inherent to the task | Not reducible — the task is the task |
| **Extraneous** | Added by the interface | **This is the target** — remove it |
| **Germane** | Effort that builds understanding | Preserve and support |

Extraneous load is where interface defects concentrate: choices that did not need to be offered,
information that did not need to be displayed, steps that did not need to exist, and memory the
interface could have carried.

## Counting decisions

For any screen or step, count:

```text
1. Decisions the user must make to proceed       (target: as few as the task requires)
2. Equally-weighted options competing at once    (target: 1 primary)
3. Items of information required from memory     (target: 0)
4. Fields requiring input the system could infer (target: 0)
5. Steps whose purpose is not self-evident       (target: 0)
```

Publish the counts in the finding. They convert "feels heavy" into a change that can be verified.

## Choice architecture

| Pattern | Effect | Use when |
|---|---|---|
| One primary action | Removes the decision | Almost always |
| A sensible default | Removes the decision, retains the option | The choice is usually the same |
| Progressive disclosure | Defers a decision | The option is rare or advanced |
| Recommended option marked | Reduces decision cost without removing choice | There is a defensible default |
| Constrained input | Prevents an invalid choice | The valid set is knowable |
| Inferred input | Removes a decision entirely | The system already knows |

The strongest lever is **inference**: the field the user did not have to fill because the system
already knew. The second strongest is **a default with an escape hatch**.

## Decision cost is not linear

Adding options has three costs that compound:

1. **Time** — each option must be read and evaluated.
2. **Regret** — more options raise the chance the user chose worse than an alternative they did not pick.
3. **Abandonment** — beyond a small set, some users defer or leave.

This is why "let the user choose" is often the *expensive* option rather than the respectful one.
Respect is expressed as a good default plus an obvious way to change it.

## Recognition over recall

Every value the user must hold in their head is a defect opportunity. The interface should carry
the memory.

| Recall defect | Fix |
|---|---|
| Re-entering a value from a previous screen | Carry it forward visibly, or show it in context |
| Remembering which option was chosen earlier | Display the current state at the decision point |
| Copying a code between devices/screens | Paste-friendly field, or a link/deep-link that carries it |
| Knowing which filters are applied | Show active filters as removable chips |
| Remembering a command or shortcut | Offer it in context, with the shortcut shown when used |
| Holding an order of steps | Number the steps and show progress |

**The two-tab test:** if a user must open a second tab or go back to complete the current step,
the interface is requiring recall and should carry the information instead.

## Where load hides

| Hidden load | Detection |
|---|---|
| Unlabelled waits | The user cannot tell work is happening (Heuristic 1) |
| Implicit state the user must infer (unsaved, offline, sync pending) | Ask: could the user be wrong about the current state? If yes, state it |
| Required context from another screen | The two-tab test |
| Irreversible actions adjacent to frequent ones | Count adjacency: how close is the destructive control to the routine one? |
| Ambiguous labels with overlapping meanings | Can two users disagree about what this does? |
| Silent success | Did something happen, and does the user know? |
| Inconsistent placement of the same action | Same action, three different positions across the flow |

## The working procedure

```text
For each task step:
  1. Count decisions, competing options, memory items, inferable fields, unexplained steps.
  2. Record the counts in the finding.
  3. Apply the lowest-cost reduction available: infer > default > disclose > remove.
  4. Re-count after the change.
  5. Confirm the task success metric moved, against the baseline (R5).
```

The re-count is what makes this a method rather than a set of opinions: the numbers before and
after are comparable.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| "Streamline the UI" | Not a change; no count, no target |
| Adding options to satisfy every request | Compounding decision cost instead of adding a default |
| Hiding a necessary option to reduce options | The user who needs it cannot find it; use progressive disclosure instead |
| Reducing visual density to reduce load | Density is not load; the count of decisions is |
| Trusting the designer's fluency | The designer cannot un-know where the settings are; observe cold |
| Treating all users as novices | Expert tools legitimately carry trained recall — state the audience |
