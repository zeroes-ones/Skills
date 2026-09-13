# Error Experience

<!-- STANDARD: 3min -- error prevention, naming, remedy and preservation patterns -->

## The three obligations

Every error state owes the user three things. A message that provides fewer than three is
incomplete, regardless of how it is styled.

| Obligation | Question it answers | Test |
|---|---|---|
| **Name** | What happened, in my terms? | Does it use the user's vocabulary, not the system's? |
| **Remedy** | What do I do now? | Is there a next action, and is it the right one? |
| **Preservation** | Did I lose anything? | Is the user's work intact, and does the message say so? |

The third is the one most often omitted, and the one that costs the most: a user who does not
know whether their work survived will redo it, which is pure waste.

## Prevention first

Prevention is cheaper than recovery, and it is Heuristic 5. The mechanisms, in order of strength:

| Mechanism | Strength | Example |
|---|---|---|
| Inference | Strongest — the user never acts | Prefill the address from the account |
| Constraint | Strong — invalid input impossible | A date picker instead of a free-text date |
| Sensible default | Strong | The most common choice pre-selected |
| Reversibility | Strong | Undo instead of confirm |
| Confirmation | Medium — adds friction | A confirmation for an irreversible action |
| Validation at the moment of fix | Medium | Inline validation as the field is left |
| Validation on submit only | Weakest | The whole form is rejected at the end |

Use the strongest mechanism the situation allows. Reach for confirmation only where the action
cannot be made reversible.

## Confirmation, used sparingly

Confirmation is the most over-used prevention mechanism, and over-use destroys its value: users
learn to dismiss dialogs reflexively, and then confirm the one that mattered.

Use confirmation only when **all** of these hold:

- the action is irreversible or expensive to reverse,
- the consequence is not visible from the action itself,
- the action is not part of a rapid, deliberate sequence.

Otherwise prefer undo. An undo that works is worth more than a dialog that interrupts.

```text
Reversible   → do it, offer undo
Irreversible → confirm, and name the specific consequence
```

"Naming the specific consequence" means "Delete 14 projects and their 230 files?" — not "Are you
sure?". The number and the noun are what make the dialog do work.

## Naming the problem

| Bad | Why | Better |
|---|---|---|
| "Error 401: Unauthorized" | The system's term for the system's condition | "Your session expired" |
| "Something went wrong" | Names nothing | "We couldn't save your draft" |
| "Invalid input" | Does not say which input or why | "That email address is already in use" |
| "Network error" | The user has no network concept | "You appear to be offline. We'll retry when you reconnect." |
| "Validation failed" | The system's word for a user's mistake | "Passwords need at least 12 characters" |
| "Forbidden" | Hostile and uninformative | "You don't have access to this project. Ask [owner] for access." |

Two rules: **use the user's nouns**, and **state the specific condition**. A message that could
apply to any failure tells the user nothing.

## Providing the remedy

| Error class | The remedy |
|---|---|
| Transient (network, timeout, rate limit) | Retry, with the retry labelled and honest about what it does |
| Input error | The exact fix, next to the offending field |
| Session/permission | Sign in again, or the request path, with who to ask |
| Missing prerequisite | A link to the thing that is missing, in context |
| Permanent | What is not possible, and the available alternatives |
| Conflict (someone else changed it) | Show both versions; let the user choose |
| Quota/limit | The limit, the current value, and the upgrade path |

The most common remedy defect: offering **retry** for a permanent error. A retry that fails again
costs more trust than the original failure.

## Preserving the user's work

| Situation | Obligation |
|---|---|
| Form submission fails | Keep the input in the fields; say so |
| Long-form editor fails to save | Local persistence; state that the draft is kept and where |
| Multi-step flow fails mid-way | Resume at the failed step, not the beginning |
| Upload fails | Retry the upload without re-selecting the file |
| Conflict overwrites | Never silently discard; offer both |
| Session expiry | Preserve and restore after re-authentication |

State the preservation explicitly. The user cannot see your persistence layer; silence reads as
loss, and a user who assumes loss will redo work that already exists.

## Error copy template

```text
[What happened, in the user's terms]  — one sentence, plain, specific
[What it means for them]              — optional, one clause, only if not obvious
[Preservation, if applicable]         — "Your draft is saved."
[The action]                          — one primary action; a secondary only if genuinely useful
```

Length: short enough to read at a glance. A multi-paragraph error is not read; it is dismissed.

## Where errors are presented

| Scope | Presentation |
|---|---|
| One field | Inline, adjacent, tied to the field; never a summary only |
| One region | Inline at the region; the rest of the screen keeps working |
| Whole screen | Full-screen state with a route back |
| Whole app / offline | Persistent, informative, non-blocking |
| Background operation | Notification or status area; never a modal that steals focus |

Rule: **an error is presented at the scope of its cause.** A failed avatar upload must not produce
a full-screen error.

## The error checklist

- [ ] Every error names the condition in the user's vocabulary
- [ ] Every error offers the correct next action (not a retry for a permanent failure)
- [ ] Preservation is stated whenever work is retained
- [ ] Errors appear at the scope of their cause (field / region / screen)
- [ ] Preventable errors are prevented: inferred, constrained, defaulted, or made reversible
- [ ] Confirmation is used only for irreversible actions, and names the specific consequence
- [ ] Undo is preferred where the action is reversible
- [ ] Validation fires at the moment the fix is possible, not only on submit
- [ ] Errors are announced to assistive technology, not merely shown visually
- [ ] A field error is never communicated by colour alone
