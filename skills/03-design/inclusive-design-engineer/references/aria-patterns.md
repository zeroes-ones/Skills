# ARIA Patterns

<!-- STANDARD: 3min -- per-widget roles, states, keyboard contracts and focus rules -->

> **Verification note.** ARIA roles, permitted attributes and the authoring patterns are
> specified and revised by the W3C. Confirm the current role/attribute pairing and the current
> pattern against the WAI-ARIA specification and the ARIA Authoring Practices Guide for the
> version you are targeting, rather than relying on recall.

## The rule that governs all of them

**Every role is a contract.** Announcing `role="dialog"` tells the user (and their AT) that a
dialog behaviour exists: focus moves in, focus is contained, Escape dismisses, focus returns on
close. If the behaviour is not implemented, the role is a false promise and the component is
*worse* than one with no role at all — because the user now expects a contract that will not be
honoured (R1).

The test for any role: **name the behaviour it promises, then find where you implemented it.**

## The patterns, with their contracts

### Dialog / modal

| Aspect | Contract |
|---|---|
| Roles | `role="dialog"` (or `alertdialog` for a confirming interruption); `aria-modal="true"` |
| Name | `aria-labelledby` pointing at the title, or `aria-label` |
| Focus on open | Moves to the first meaningful element (or the dialog itself for a simple one) |
| Focus while open | Contained — Tab and Shift+Tab cycle within the dialog |
| Background | Inert to AT and to focus while open |
| Dismissal | Escape, plus a visible close control; Escape may be suppressed only for a genuinely irreversible interruption |
| Focus on close | Returns to the element that invoked the dialog |
| Scroll | The page behind does not scroll |

The two most common failures: focus is not moved in (so the AT reads the page behind it), and
focus is not returned on close (so the user is dropped at the document body).

### Alert dialog

Same as dialog, with two differences: it interrupts (`role="alertdialog"`), and the focus goes to
the least destructive action. Use it only where a response is genuinely required.

### Menu / menubar

| Aspect | Contract |
|---|---|
| Roles | `role="menu"`, children `role="menuitem"` (or `menuitemcheckbox`/`menuitemradio`) |
| Focus model | Roving `tabindex`, or `aria-activedescendant` |
| Keys | Up/Down move, Home/End jump, Escape closes and returns focus to the trigger, Enter/Space activate |
| Typeahead | Required for longer menus — typing moves to the matching item |
| First and last | Wrap, in the established pattern |
| On open | Focus moves to the first item |

Note: a `role="menu"` is for *application menus*. A list of links or a navigation list is not a
menu, and using the role adds a keyboard contract users do not expect there.

### Combobox / autocomplete

| Aspect | Contract |
|---|---|
| Roles | `role="combobox"` on the input; the popup is a listbox with options |
| Expanded state | `aria-expanded` on the input |
| Active option | `aria-activedescendant` on the input (the input keeps focus, not the option) |
| Keys | Down opens/moves into the list, Up/Down move, Enter selects, Escape closes without clearing |
| Announcement | The expanded state, the active option, and the result count |
| Filtering | Announced, or the count changes audibly — silence after typing is the common defect |

The classic defect: focus moves into the listbox. In the standard pattern the input retains focus
and points at the active option; moving focus breaks typing.

### Tabs

| Aspect | Contract |
|---|---|
| Roles | `role="tablist"`, `role="tab"`, `role="tabpanel"` |
| Selection | `aria-selected` on the active tab |
| Keys | Left/Right move between tabs; Home/End jump; Tab moves into the panel (not to the next tab) |
| Activation | Selection follows focus in the standard pattern |
| Association | Each tab references its panel; each panel references its tab |

### Disclosure / accordion

| Aspect | Contract |
|---|---|
| Element | A real `button` |
| State | `aria-expanded` reflects the panel's visibility |
| Association | `aria-controls` points at the panel |
| Keys | Enter and Space toggle (native button behaviour) |

### Tooltip

| Aspect | Contract |
|---|---|
| Association | The trigger references the tooltip as its description, not its name |
| Trigger | Shown on hover **and** on focus — never hover only |
| Dismissal | Escape dismisses |
| Content | Non-essential only; a tooltip must not be the only source of needed information |
| Announcement | Described, not announced as a live update |

### Toast / status message

| Aspect | Contract |
|---|---|
| Live region | Must exist **before** the message (R4) |
| Politeness | `polite` for routine status; `assertive` only for urgent, interrupting information |
| Role | `status` for routine, `alert` for urgent |
| Content | Update the region's content; do not recreate the region |
| Persistence | Dismissible, and not the only way to learn something important |

### Alert / error summary

| Aspect | Contract |
|---|---|
| Role | `alert` if it must interrupt; otherwise an associated message |
| Focus | An error summary receives focus, so the user is placed at the problem list |
| Links | Each entry links to its field |

## The state attributes, and where they belong

| Attribute | Belongs on | Do not put it on |
|---|---|---|
| `aria-expanded` | The control that expands something | The panel |
| `aria-selected` | The selected item in a set | The container |
| `aria-checked` | A checkbox/switch/menuitemcheckbox | The label |
| `aria-pressed` | A toggle button | A checkbox (use `checked`) |
| `aria-current` | The current item in a set (page, step, location) | Every item |
| `aria-disabled` | A control that is disabled but must stay focusable | — prefer the real `disabled` where it is appropriate |
| `aria-invalid` | The field with the error | The form |
| `aria-describedby` | The control being described | The description |
| `aria-labelledby` | The control being named | The label |
| `aria-hidden="true"` | Decorative elements only | Anything focusable, or anything containing focusable content |

**`aria-hidden` on focusable content is a defect**: the element is removed from the accessibility
tree but remains reachable by keyboard, so a keyboard user lands on an element with no name and no
role.

## Accessible names

Every interactive element and every meaningful image needs a name. In priority order:

1. Visible text content.
2. `aria-labelledby` pointing at visible text (preferred over `aria-label`, because it stays in
   sync with the visible string).
3. `aria-label` when no visible text exists.
4. `title` — last resort, inconsistently exposed.

| Case | Solution |
|---|---|
| Icon-only button | `aria-label` with the action's name, or visually-hidden text |
| Decorative icon inside a labelled button | `aria-hidden="true"` on the icon |
| Meaningful image | `alt` describing its purpose in context |
| Decorative image | `alt=""` |
| Image that is also a link | `alt` describes the destination, not the image |
| An icon that duplicates adjacent text | Hide the icon from AT |

The name must match the visible label where one exists. A control labelled "Save" visually and
"Submit form" to the AT breaks voice control ("click Save" fails).

## The pattern checklist

- [ ] Every role's promised behaviour is implemented somewhere, and you can point to it
- [ ] Every interactive element has an accessible name matching its visible label
- [ ] Every custom widget implements the established pattern's keyboard contract
- [ ] Focus moves in, is contained, and is restored for every overlay
- [ ] The input keeps focus in a combobox; the active option is referenced, not focused
- [ ] No `aria-hidden` on anything focusable
- [ ] Every state attribute is on the right element and is valid for its role
- [ ] ARIA is absent where native semantics already provide the meaning (R1)
- [ ] The widget is verified with a named AT, and the verification is recorded (R2)
