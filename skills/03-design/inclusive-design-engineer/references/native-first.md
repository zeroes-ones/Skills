# Native First

<!-- STANDARD: 3min -- choosing between native elements, adapted elements and ARIA -->

## The hierarchy

Every semantic need has three possible solutions, in descending order of correctness:

| Rank | Solution | What you get free | What you must build |
|---|---|---|---|
| 1 | **Native element** | Semantics, keyboard behaviour, focus handling, platform AT integration, high-contrast support | Nothing |
| 2 | **Adapted native element** | All of the above, preserved | Only the added behaviour |
| 3 | **Custom widget with ARIA** | Nothing | Everything: semantics, keyboard, focus, announcements, AT quirks |

Rank 1 and 2 are almost always available. Rank 3 is for the cases where no element expresses
what you are building — and even then, a hidden native control (rank 2 by another route) often
solves it better.

## The element map

| You need | Use | Not |
|---|---|---|
| An action | `button` | `div`/`span` with a click handler |
| Navigation | `a href` | `div` with a click handler |
| A form submit | `button type="submit"` | a styled `div` |
| A text input | `input type="text"` (and the right `type`) | a contenteditable `div` |
| A multi-line input | `textarea` | a contenteditable `div` |
| A choice among few, all visible | `input type="radio"` in a `fieldset` with a `legend` | styled `div`s with ARIA |
| A choice among many | `select` | a custom listbox, unless the design requires more |
| Independent toggles | `input type="checkbox"` | ARIA switches |
| A single on/off setting that acts immediately | `button` with `aria-pressed`, or a native control | a styled `div` with a role |
| Grouping of related controls | `fieldset` + `legend` | a `div` with `role="group"` |
| A section of a form | the same | — |
| A disclosure | `button` + `aria-expanded` + the panel | a `div` with a click handler |
| A dialog | `dialog` or the established dialog pattern | a `div` with `role="dialog"` and no focus handling |
| A live status | an existing, pre-created live region | a new element created with the message |
| A summary/detail | `details` + `summary` | a hand-built accordion |
| A progress indicator | `progress` | a `div` with a width |
| A date | `input type="date"` (with an accessible fallback where needed) | a custom calendar with no keyboard model |

## Why the native element is not merely "easier"

The native element is *better*, not just cheaper:

1. **The keyboard model is complete and correct.** A `button` activates on Enter and Space, and
   not on other keys. A `div` with a click handler activates on neither.
2. **Focus behaviour is correct.** Native elements are focusable in the right order, are skipped
   when disabled, and participate in the tab sequence correctly.
3. **The AT integration is the platform's.** Screen readers have first-class handling for native
   elements, including announcement of state, role and name in the user's locale.
4. **Forced-colours and high-contrast modes work.** A native control adapts to the user's
   contrast preference; a `div` styled with fixed colours does not.
5. **Form semantics work.** Native inputs participate in form submission, validation and
   autofill; a contenteditable `div` does not.

Each of these is a thing you would have to reimplement, and would reimplement less well.

## The adapted element

Extend without replacing. The pattern: keep the native element as the real control and add only
the state the native element does not express.

```html
<!-- A disclosure: the button is real; ARIA carries the added state -->
<button type="button" aria-expanded="false" aria-controls="panel-1">
  Shipping options
</button>
<div id="panel-1" hidden>...</div>
```

```html
<!-- A toggle button: the native button, with a pressed state -->
<button type="button" aria-pressed="false">Bold</button>
```

Rules for adaptation:

- **Add only the state the element cannot express.** Do not restate what the element already
  conveys.
- **Never override the element's own behaviour.** A `button` that does not respond to Space is a
  broken button, not a custom control.
- **Keep the accessible name on the control**, not on a wrapper.

## The hidden native control

A powerful middle path: use the native element as the real control, and hide it *visually* while
it remains in the accessibility tree.

```html
<label class="switch">
  <input type="checkbox" class="switch__input" />
  <span class="switch__track" aria-hidden="true"></span>
  <span class="switch__thumb" aria-hidden="true"></span>
</label>
```

The checkbox is real, focusable, keyboard-operable and announced. The visual layer is decoration
and is hidden from AT. This gives a fully custom appearance with none of the custom-widget risk.

Two cautions:

- Hide the native control **visually only** — never with `display: none` or `visibility: hidden`,
  which would remove it from the accessibility tree.
- Keep focus styling on the visible layer, driven by the input's focus state
  (`:focus-visible + .switch__track`).

## When a custom widget is genuinely required

Only when no element expresses the semantic *and* the hidden-control approach cannot carry the
behaviour. The realistic cases: a combobox with custom filtering and multi-select, a tree view, a
grid with cell navigation, a rich text editor, a drag-and-drop reorder with keyboard alternative.

When you build one, you owe the user five things:

| Obligation | Detail |
|---|---|
| Roles and states | Exactly the ones the pattern specifies, no extras |
| The complete keyboard model | Every key, every outcome, documented |
| Focus management | Entry, movement within, dismissal, restoration |
| What is announced, when | Names, states, counts, and the live-region behaviour |
| The verification | Which AT, platform and browser, and what was observed |

And you follow the established pattern rather than inventing one — the pattern's value is that
users of assistive technology already know it.

## The ARIA rules to apply mechanically

| Rule | Check |
|---|---|
| Do not use ARIA where a native element exists | Search the markup for `role=` on semantic elements |
| Do not change native semantics | `role="heading"` on a `button`, `role="link"` on a `div` |
| All interactive ARIA controls must be keyboard operable | Every `role` with a click handler has a key handler |
| Do not use `role="presentation"`/`none` on a focusable element | It removes the semantics while focus remains |
| Every interactive element must have an accessible name | Check icon-only controls first |
| Every `aria-*` attribute must be valid for its role | An attribute on the wrong role is silently ignored |

The mechanical version is a grep, and it catches the majority of ARIA misuse:

```bash
# ARIA on elements that already have semantics — usually unnecessary
grep -rnE '<(button|a|input|select|textarea)[^>]*role=' src/

# Click handlers on non-interactive elements — missing semantics and keyboard path
grep -rnE '<(div|span)[^>]*onClick' src/

# ARIA attributes whose behaviour is not implemented
grep -rn 'aria-expanded\|aria-pressed\|aria-selected\|aria-checked' src/ \
  | grep -v 'onKeyDown\|onClick\|setState\|useState'
```

## The decision, restated

```text
Does a native element express this semantic AND its behaviour?
├── Yes → use it. Stop.
└── No → can the native element be extended, or hidden as the real control?
    ├── Yes → do that. Add only the missing state.
    └── No → build the custom widget to the established pattern,
              document the full contract, and verify with a named AT.
```
