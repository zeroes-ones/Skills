# Overlays and Menus

<!-- STANDARD: 3min -- dialogs, drawers, menus, comboboxes, tooltips and popovers -->

## The shared contract

Every overlay component shares the same four-part contract. Missing any part makes the overlay
partially modal, which is worse than not being an overlay at all.

| Part | Requirement |
|---|---|
| **Entry** | Focus moves into the overlay on open |
| **Containment** | Focus stays inside while it is open; the background is inert to AT and to the keyboard |
| **Dismissal** | Escape closes it, plus a visible close control |
| **Restoration** | Focus returns to the invoking element on close |

## Dialog / modal

The most common component to get wrong, and the most damaging, because the failure mode is a screen
reader reading the page behind the dialog while the user believes they are inside it.

```html
<div role="dialog" aria-modal="true" aria-labelledby="dlg-title">
  <h2 id="dlg-title">Delete project</h2>
  <p>This deletes the project and its 14 files. This cannot be undone.</p>
  <button type="button">Cancel</button>
  <button type="button">Delete</button>
</div>
```

| Requirement | Detail |
|---|---|
| `aria-modal="true"` | Announces modality — and *requires* the background to actually be inert |
| Labelled by the title | `aria-labelledby` pointing at the visible heading |
| Focus on open | The dialog itself, or the first meaningful control |
| Focus containment | Tab and Shift+Tab cycle within |
| Background inert | Not merely visually covered |
| Escape | Closes, unless the interruption is genuinely irreversible |
| Focus on close | Returns to the invoker |
| Page scroll | The background does not scroll |

**The ordering of actions:** for destructive dialogs, focus the *least* destructive action. Placing
focus on "Delete" means one keystroke completes the destruction.

## Drawer / side panel

Same contract as a dialog, with one addition: if it is modal (it blocks the page), it must make the
background inert exactly as a dialog does. A drawer that is visually modal but keyboard-transparent
is the same defect as a keyboard-transparent dialog.

If the drawer is *non-modal* (the page remains usable beside it), do not give it dialog semantics —
that would promise modality that does not exist.

## Menu

A menu is an application menu, not a list of links. Using `role="menu"` on navigation adds a
keyboard contract users do not expect in a nav list.

```html
<button type="button" aria-haspopup="true" aria-expanded="false" aria-controls="m1">Actions</button>
<ul id="m1" role="menu" hidden>
  <li role="menuitem" tabindex="-1">Duplicate</li>
  <li role="menuitem" tabindex="-1">Move…</li>
  <li role="menuitem" tabindex="-1">Delete</li>
</ul>
```

| Requirement | Detail |
|---|---|
| Trigger | A real button with `aria-haspopup` and `aria-expanded` |
| Focus on open | The first item, or the item the menu was opened from |
| Keys | Up/Down move, Home/End jump, Enter/Space activate |
| Typeahead | Typing moves to the matching item (required for longer menus) |
| Wrap | First and last wrap, per the pattern |
| Escape | Closes and returns focus to the trigger |
| Selection | Closes the menu and returns focus |

**The roving tabindex defect:** implementing menu items as separate tab stops. The menu should be one
tab stop with arrow navigation inside.

## Combobox / autocomplete

The pattern with the highest defect rate, because the focus model is counter-intuitive: the input
keeps focus and *references* the active option, rather than moving focus into the list.

| Requirement | Detail |
|---|---|
| Input retains focus | `aria-activedescendant` points at the active option — focus does not move |
| Expanded state | `aria-expanded` on the input |
| Association | `aria-controls` points at the listbox |
| Options | The active option carries `aria-selected` |
| Keys | Down opens or moves into the list; Up/Down move; Enter selects; Escape closes without clearing |
| Announcement | Expanded state, active option, and the result count |
| Filtering | The count change is announced — silence after typing is the common defect |

**The classic defect:** moving focus into the listbox on arrow-down, which breaks typing. The user
can no longer refine the query.

## Tooltip

| Requirement | Detail |
|---|---|
| Trigger | Hover **and** focus — never hover only |
| Association | Describes the trigger (`aria-describedby`), does not name it |
| Dismissal | Escape dismisses |
| Content | Non-essential; never the only source of needed information |
| Persistence | Visible long enough to read; not auto-hidden while focused |

A tooltip carrying essential information is an accessibility defect on its own: it is unreachable on
touch and unreadable at leisure.

## Popover

Same contract as a dialog, scaled down. If it is modal to the keyboard, it must contain and restore
focus. If it is dismissible and non-modal, provide Escape and ensure focus is not lost when it
closes.

## Toast

Not an overlay, but often treated as one, and the defect is the same family:

| Requirement | Detail |
|---|---|
| Live region | Present before the message (R4) |
| Not focus-stealing | Toasts must not move focus unless they demand a response |
| Dismissible | Including by keyboard |
| Not the only signal | A toast alone is not how a user should learn something important |
| Persistence | Long enough to read; not removed while focused |

## Overlays and background content

The defect underneath most overlay bugs: a visual overlay does not modify the accessibility tree.
The page behind remains focusable and readable unless made inert.

| Mechanism | Effect |
|---|---|
| Platform modal element / modal API | Handles inertness, focus and dismissal together |
| Explicit inert marking on the background | Removes the background from focus and AT |
| `aria-hidden` on the background | Removes it from AT but **not** from the keyboard — insufficient alone |

`aria-hidden` alone is the most common half-fix: the screen reader stops reading the background, but
a keyboard user still tabs into it.

## The overlay checklist

- [ ] Every overlay moves focus in, contains it, and restores it on close (CR6)
- [ ] The background is inert to both keyboard and AT, not merely visually covered
- [ ] Escape dismisses every overlay, unless the interruption is irreversible and that is justified
- [ ] Every overlay is labelled by its visible heading
- [ ] Destructive dialogs focus the least destructive action
- [ ] Menus are one tab stop with arrow navigation and typeahead
- [ ] Comboboxes keep focus in the input and reference the active option
- [ ] Tooltips appear on focus as well as hover, and never carry essential information only
- [ ] Toasts use a pre-existing live region and do not steal focus
- [ ] `role="menu"` is not used for navigation lists
- [ ] Verified with a keyboard-only walkthrough and a named screen reader (R2)
