# Forms and Feedback

<!-- STANDARD: 3min -- validation timing, inline feedback and input ergonomics -->

## Validation timing

Validation timing is the single highest-leverage form decision, and it is usually wrong by default.
The common implementation — validate everything on submit — delays every correction to the moment
the user has least patience.

| Timing | Effect | Use for |
|---|---|---|
| On input, per keystroke | Feeds errors while typing | Never for validity; only for positive signals (strength, availability) |
| On blur (leaving the field) | The fix is possible immediately | Field-level validity, format, uniqueness |
| On submit | All errors at once, late | Only the checks that cannot run earlier |
| On submit, re-validated live | Errors clear as fixed | The submit-time errors, once shown |

The rule: **validate at the moment the fix is possible.** A format error should appear when the
user leaves the field, not after they have completed eleven others.

Two exceptions:

- **Do not show an error before the user has finished typing.** An error on the second character of
  an email address is noise, not help. Blur is the earliest defensible moment for a format error.
- **Positive validation is welcome earlier.** "Username available" as the user types is helpful;
  "Username invalid" as they type is not.

## Input ergonomics

| Requirement | Reason |
|---|---|
| Correct input type and `inputmode` | Brings the right keyboard on touch devices |
| Autocomplete tokens for known fields (`email`, `tel`, `one-time-code`) | System autofill fills correctly |
| Label present and persistent | Placeholder-only labels vanish once typing starts |
| The label is the field's name, not a description | Assistive technology reads it as the name |
| Generous target size and spacing | Mis-taps on touch; a motor-accessibility requirement too |
| One column on narrow widths | Two-column forms cause skipped fields and mis-ordered entry |
| Required/optional marked once, consistently | Marking every field "required" is noise |
| No redundant fields the system can infer | Each field costs completion (Heuristic 8) |

**The placeholder trap.** A placeholder used as the label disappears when the user types, so the
user loses the field's meaning exactly when they need it — while filling it in. This is both a
usability defect (Heuristic 6) and an accessibility defect.

## Feedback and state communication

| Situation | Feedback | Timing |
|---|---|---|
| Field is valid | Subtle positive indication | On blur |
| Field is invalid | Message adjacent to the field, tied to it | On blur, cleared live once fixed |
| Field is being checked | Inline activity on that field only | Immediately |
| Form is submitting | Button state change; the button does not move | Immediately |
| Submit failed | Preserve input, name the failure, offer the retry | Immediately |
| Submit succeeded | Explicit confirmation | Immediately |

## The submit button

Three defects, all common:

1. **The button moves or disappears during submit.** The user's next tap lands elsewhere.
2. **The button is disabled until the form is "valid".** A disabled button gives no reason, so the
   user cannot tell what is missing. Prefer an enabled button that reveals the first error.
3. **No double-submit protection.** The user taps twice; two records are created. Prevent with an
   in-flight state and idempotency, not with a disabled button alone.

Rule: on submit, the button changes its *state* (in-flight indicator) but not its *position*.

## Error presentation in forms

| Scope | Presentation |
|---|---|
| One field | Next to the field, associated programmatically, with the field visibly marked |
| Several fields | All marked; a summary at the top **as well as** per-field messages, with links |
| Form-level | At the form level, naming the condition and the remedy |

Two rules:

- **Never communicate an error by colour alone.** Add an icon and text; colour is not perceivable
  by everyone and is not announced.
- **Announce errors to assistive technology.** A visually displayed message that is not announced
  is invisible to a screen-reader user, who will then re-submit the same failing form.

## Progress in multi-step forms

| Requirement | Reason |
|---|---|
| Show the total number of steps | The user needs to know the commitment |
| Show the current position | Progress is a status (Heuristic 1) |
| Name each step | Titles set expectations and allow orientation |
| Allow back without losing input | Forward progress must not cost the user's work |
| Allow save-and-resume for long forms | Abandonment is otherwise permanent |
| Request hard information late | Put the effort after the user is invested |

The classic multi-step defect: the user reaches step 4 of 5 and hits a wall requiring a document
they do not have, with no way to save. That is a preventable abandonment.

## Sensitive and irreversible inputs

| Situation | Requirement |
|---|---|
| Destructive action | Confirm with the specific consequence named, or offer undo |
| Irreversible submission | A review step before the point of no return |
| Payment/personal data | Never pre-fill where that would be surprising; never lose it on failure |
| Sensitive values | Masked where appropriate, with an explicit reveal control |

## The forms checklist

- [ ] Field-level validation fires on blur, not only on submit
- [ ] No error is shown mid-typing, before the user has finished
- [ ] Positive signals may appear earlier than negative ones
- [ ] Every field has a persistent label; no placeholder-as-label
- [ ] Input types and autocomplete tokens are set for system autofill
- [ ] Required/optional is marked consistently, not on every field
- [ ] Fields the system can infer are removed
- [ ] The submit button does not move or disappear during submit
- [ ] Double submission is prevented by an in-flight state plus idempotency
- [ ] Errors are presented adjacent to their field and associated programmatically
- [ ] Errors are never communicated by colour alone
- [ ] Errors are announced to assistive technology
- [ ] Multi-step forms show total steps, position, and step names
- [ ] Back navigation preserves entered input
- [ ] Long forms allow save-and-resume
- [ ] Irreversible submissions have a review step
