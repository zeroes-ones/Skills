# Forms and Validation

<!-- STANDARD: 3min -- labels, error association, announcement and submit states -->

## The four obligations of an accessible form

1. Every field has a **persistent, programmatic label**.
2. Every error is **associated with its field** and **announced**.
3. No error is communicated by **colour alone**.
4. The user's **input survives** every failure path.

A form that meets all four is accessible in the ways that matter most; a form that misses any one
fails a real user in a real situation.

## Labels

```html
<!-- ✅ A real label, programmatically associated -->
<label for="email">Email address</label>
<input id="email" type="email" autocomplete="email" />

<!-- ❌ Placeholder as the label — vanishes exactly when the user needs it -->
<input type="email" placeholder="Email address" />
```

| Requirement | Detail |
|---|---|
| Persistent label | Visible after the user begins typing |
| Programmatic association | `for`/`id`, or the control wrapped by the label |
| The label is the field's *name* | Not a description — descriptions go in helper text |
| Required/optional stated | Marked in the label, not only by colour or an asterisk alone |
| Group labels for related controls | `fieldset` + `legend` for radio and checkbox groups |
| Instructions before the field | Not after, and not in a placeholder |

**The asterisk problem:** an asterisk alone is not perceivable everywhere and is not announced. State
"required" in the label or helper text.

## Error association

```html
<label for="email">Email address</label>
<input id="email" type="email" aria-invalid="true"
       aria-describedby="email-error" autocomplete="email" />
<p id="email-error" class="error">
  <span aria-hidden="true">⚠</span> That email address is already in use.
</p>
```

The four parts, all required:

| Part | What it does |
|---|---|
| `aria-invalid="true"` | Marks the field as invalid |
| `aria-describedby` pointing at the message | Associates the message with the field |
| An icon plus text | Communicates the error without relying on colour |
| The message itself | Names the problem in the user's terms with the remedy |

The message text does the real work. "Invalid input" is not a message; "That email address is
already in use — sign in, or use a different address" is.

## Announcement

Association makes the message *reachable*; announcement makes it *noticed*.

| Approach | Behaviour |
|---|---|
| The error summary receives focus on failed submit | The user is placed at the problem list — the strongest signal |
| A live region announces the summary | The user hears the count and the first message |
| The associated message plus invalid state | Announced when the user returns to the field |

The best practice for a failed submit: move focus to an **error summary** at the top of the form,
listing each error as a link to its field, and announce the summary politely. This is why the user
knows both that it failed and where to go.

## Validation timing

| Timing | Effect | Use |
|---|---|---|
| On every keystroke | Announces errors while typing | Never for validity |
| On blur | The fix is possible immediately | Field-level validity |
| On submit | All errors at once, late | Only what cannot run earlier, plus re-validated live |

For screen-reader users the timing matters more than for anyone: an error announced mid-word
interrupts the reading of what the user is typing and is actively harmful.

The exception: **positive** validation (availability, strength) may run earlier; it is welcome while
typing.

## The submit control

| Requirement | Detail |
|---|---|
| Does not move or disappear during submission | The user's next action must land where they expect |
| State is communicated | In-flight indicator, announced, without moving the control |
| Double submission prevented | An in-flight state plus idempotency; not a disabled button alone |
| Disabled state, if used, is explained | A disabled submit with no reason leaves the user stuck |

Prefer an enabled submit that reveals the first error. A disabled submit with no explanation is one
of the most common — and most frustrating — form defects.

## Multi-step forms

| Requirement | Detail |
|---|---|
| Step count and position announced | The user knows the commitment |
| Step change announced | A polite live region on entering each step |
| Error location announced | Which step holds the error, and a link to it |
| Back preserves input | Progress must not cost the user's work |
| The step heading receives focus on change | Places the user at the new content |

## Grouping

```html
<fieldset>
  <legend>Notification preference</legend>
  <label><input type="radio" name="notify" value="all" /> All activity</label>
  <label><input type="radio" name="notify" value="mentions" /> Mentions only</label>
  <label><input type="radio" name="notify" value="none" /> Nothing</label>
</fieldset>
```

The `legend` is announced as the group's name, which is what makes a radio group comprehensible. A
`div` with a styled heading does not provide this.

## Target size and spacing

Every interactive control needs a target large enough to activate reliably — for touch users, for
users with motor impairments, and for anyone using the interface on a small screen. Space controls
generously; the platform requirement exists because a too-small target is a real barrier, not a
polish issue.

## The forms checklist

- [ ] Every field has a persistent, programmatically associated label (CR9)
- [ ] No placeholder is used as the only label
- [ ] Related controls are grouped with `fieldset`/`legend`
- [ ] Required/optional is stated in text, not by colour or asterisk alone
- [ ] Every error is associated with its field and marks it invalid (CR8)
- [ ] Every error is communicated by more than colour
- [ ] Failures place focus on an error summary that links to each field
- [ ] Validation runs on blur, not on every keystroke
- [ ] Submit does not move or disappear; in-flight state is announced
- [ ] Double submission is prevented by state plus idempotency
- [ ] Multi-step forms announce the step, the position and the error location
- [ ] Back navigation preserves entered input
- [ ] Target sizes are generous enough for reliable activation
- [ ] Verified end-to-end with a named screen reader, and recorded (R2)
