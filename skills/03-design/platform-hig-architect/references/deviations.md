# Deviations

<!-- STANDARD: 3min -- the deviation log format and worked examples -->

## Why a deviation log exists

A convention override and a defect look identical in a screenshot. Without a log, the next
engineer reads the override as a bug and "fixes" it — removing a deliberate decision — or
preserves a real bug believing it was deliberate. Both failures are common, and both are
prevented by one table.

This is R3. The rule is not "never deviate"; it is "never deviate silently".

## What counts as a deviation

| Counts | Does not count |
|---|---|
| Using a non-platform navigation model | Brand colour on a platform control |
| Reassigning a platform gesture | Custom imagery or illustration |
| A custom control where the platform has one | Custom type within the platform's sizing system |
| Reimplementing a system affordance | Content and information architecture |
| Skipping the platform's feedback pattern | Visual theming that preserves behaviour |
| A different back affordance | Brand voice in copy |

The dividing line: **behaviour deviates, appearance usually does not.** If the user must do
something different from what the platform taught them, it is a deviation.

## The log format

| Field | Content | Why it matters |
|---|---|---|
| ID | `DEV-001` | Referenceable from code comments and reviews |
| Surface | Platform + form factor | Conventions are per surface |
| Category | Navigation / gesture / control / feedback / accessibility | Groups the cost |
| Convention departed from | Name the platform pattern | Makes the deviation falsifiable |
| What we do instead | The actual behaviour | The implementation reference |
| Rationale | Why the cost is worth it | The decision's justification |
| Cost to users | What the user must relearn or lose | Forces the trade to be explicit |
| Preserved behaviour | How the expected outcome is still achievable | Prevents a dead end |
| Reversal trigger | When to revisit | Prevents permanent drift |
| Owner | Who decided | Accountability and future contact |

## Worked examples

### DEV-001 — Custom primary action placement (justified)

| Field | Content |
|---|---|
| Surface | iOS phone |
| Category | Control / primary action |
| Convention departed from | Platform's conventional placement for a primary action |
| What we do instead | A brand-styled primary action in a fixed position, visually distinctive |
| Rationale | The primary action is the product's core loop; discoverability is measured and better in this position for our task |
| Cost to users | The control is not where the platform would put it; the first interaction requires reading |
| Preserved behaviour | Behaviour (activation, feedback, hit target, accessibility) is entirely the platform's; only placement and styling differ |
| Reversal trigger | If measured task-completion drops below the pre-change baseline |
| Owner | Head of design |

This is a *good* deviation: it departs on surface, preserves behaviour, and is measurable.

### DEV-002 — Signature gesture (justified, with an alternative)

| Field | Content |
|---|---|
| Surface | All touch surfaces |
| Category | Gesture |
| Convention departed from | The platform's default meaning for this swipe |
| What we do instead | The swipe triggers the signature feature |
| Rationale | The signature feature is the product; the gesture is its most direct expression |
| Cost to users | The platform default is no longer available on that element; some users will trigger it by accident first |
| Preserved behaviour | A visible control performs the same action, so the feature is not gesture-only (WCAG 2.5.1) |
| Reversal trigger | If accidental-trigger rates exceed a set threshold |
| Owner | Product + design |

The load-bearing field is "preserved behaviour": the gesture is *additional*, never the only path.

### DEV-003 — Custom confirmation dialogue (rejected)

| Field | Content |
|---|---|
| Category | Control / destructive action |
| Convention departed from | The platform's confirmation affordance |
| What we proposed | A branded confirmation sheet for destructive actions |
| Rationale | "It matches our brand" |
| Cost to users | Loses system behaviour (focus handling, accessibility, dismissal); adds a pattern to learn |
| Preserved behaviour | None — it *is* the only path |
| Verdict | **Rejected.** Brand is expressible in the dialogue's content and styling, not by reimplementing the system affordance |

The reject case is instructive: the rationale was aesthetic, the cost was behavioural, and no
behaviour was preserved. That is the signature of an unjustified deviation.

## Judging a deviation

```text
Does the deviation change BEHAVIOUR the platform taught?
├── No (appearance only) → not a deviation; brand is free
└── Yes ↓
    Is there a non-deviating path to the same outcome (a control, a menu, a keyboard equivalent)?
    ├── Yes → deviation may be acceptable (it is additive, not exclusive)
    └── No  → the deviation EXCLUDES users. Require a preserved path before accepting (R4)
    Is the rationale measurable (a metric, a regulation, a platform limit)?
    ├── No (taste, aesthetics) → reject or require a measurable rationale
    └── Yes ↓
        Is the platform affordance being reimplemented rather than supplemented?
        ├── Yes → reject; system affordances are not the product's to own
        └── No  → accept, record, and set a reversal trigger
```

## Reviewing the log

At each release, scan the log for:

- Deviations whose reversal trigger has been met (revert them)
- Deviations that have grown (one screen became five)
- Deviations whose rationale no longer applies (a platform limit was lifted)
- Deviations that duplicate each other (consolidate into one pattern)
- New UI that deviates with no log entry (the log failed — fix the process)

A log that only grows is a sign the review is not happening. A healthy log is small, specific
and occasionally shrinking.

## Deviation checklist

- [ ] Every behavioural departure from a platform convention has a log entry (R3)
- [ ] Each entry names the convention departed from, in falsifiable terms
- [ ] Each entry states the cost to users, not just the benefit
- [ ] Each entry states how the expected outcome is still achievable
- [ ] Each entry has a reversal trigger and an owner
- [ ] Appearance-only differences are not logged (they are not deviations)
- [ ] System affordances are never reimplemented, so never appear as deviations
- [ ] The log is reviewed each release and occasionally shrinks
