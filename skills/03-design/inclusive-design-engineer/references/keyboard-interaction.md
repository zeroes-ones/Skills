# Keyboard Interaction

<!-- STANDARD: 3min -- keyboard models, roving focus, activedescendant, and shortcuts -->

## Why the keyboard model is structure

Keyboard support is not an enhancement layered onto a component; it is part of how the component is
built. A component designed without a keyboard model must be rebuilt to gain one, because focus
movement, activation and dismissal are structural properties (R5).

The practical consequence: **define the keyboard contract when you define the component's props**,
not when someone files a ticket.

## The universal expectations

| Key | Expected behaviour |
|---|---|
| Tab | Move to the next focusable element |
| Shift+Tab | Move to the previous |
| Enter | Activate the focused control (buttons, links) |
| Space | Activate the focused control; scroll the page when nothing is focused |
| Escape | Dismiss the current overlay or cancel the current operation |
| Arrow keys | Move within a composite widget; scroll when nothing is focused |
| Home / End | Jump to the first/last item within a widget; page start/end otherwise |

These are not preferences. A control that does not respond to Enter or Space is broken, regardless
of how it looks.

## The two focus models

| Model | How it works | Use for |
|---|---|---|
| **Roving tabindex** | One item has `tabindex="0"`, the rest `-1`; arrows move the `0` | Menus, tabs, toolbars, grids, radio groups |
| **`aria-activedescendant`** | The container keeps focus and points at the active child | Comboboxes, and any widget where a text input must keep focus |

Roving tabindex moves *real* focus, so the AT follows the focused element. `activedescendant` keeps
focus on the container and describes which child is active; it is required where the user must keep
typing (combobox).

```html
<!-- Roving tabindex: the selected tab is the tab stop -->
<div role="tablist">
  <button role="tab" aria-selected="true"  tabindex="0">Overview</button>
  <button role="tab" aria-selected="false" tabindex="-1">Details</button>
  <button role="tab" aria-selected="false" tabindex="-1">History</button>
</div>
```

```html
<!-- activedescendant: the input keeps focus, the option is referenced -->
<input role="combobox" aria-expanded="true" aria-controls="listbox-1"
       aria-activedescendant="opt-2" />
<ul id="listbox-1" role="listbox">
  <li id="opt-1" role="option">Alpha</li>
  <li id="opt-2" role="option" aria-selected="true">Beta</li>
</ul>
```

## Per-widget key contracts

| Widget | Keys |
|---|---|
| Button | Enter, Space activate. Enter activates on keydown; Space on keyup |
| Link | Enter activates |
| Checkbox | Space toggles |
| Radio group | Arrows move and select; the group is one tab stop |
| Switch | Space toggles |
| Tabs | Left/Right move (selection follows focus); Home/End jump; Tab enters the panel |
| Menu | Up/Down move; Home/End jump; Escape closes and returns focus; typeahead; Enter activates |
| Dialog | Focus contained; Escape closes; Tab cycles inside |
| Combobox | Down opens/moves; Enter selects; Escape closes without clearing; typeahead filters |
| Tree | Up/Down move; Right expands or enters; Left collapses or exits; Home/End jump |
| Grid | Arrow keys move cells; Home/End jump to row ends; Ctrl+Home/End to grid corners |
| Slider | Arrows adjust; Home/End go to the extremes; PageUp/PageDown for larger steps |

If you implement a widget, implement its row completely. A menu with mouse support and no arrow
keys is not a menu.

## Keyboard traps

A keyboard trap is any state where focus cannot leave a region by keyboard. The one legitimate
trap is a modal dialog, and even there Escape provides the exit.

| Trap | Cause | Fix |
|---|---|---|
| Focus cycles forever inside a widget | Containment implemented without an exit | Provide Escape, or a control that moves focus out |
| A custom control consumes Tab | The key handler prevents default on Tab | Never prevent Tab except inside a modality with an explicit exit |
| An iframe or embedded widget captures Tab | Third-party content | Provide a documented way out, and test it |
| A focusable element that is visually hidden | Off-screen positioning without intent | Remove it from the tab order unless it is a skip link |

**Skip links** are the deliberate exception: a link at the start of the page that jumps to the main
content. It must become visible when focused, and it must be the first focusable element.

## Shortcuts

Single-key shortcuts (a bare letter) conflict with AT, which uses letters for navigation. Rules:

| Rule | Detail |
|---|---|
| Prefer modifier-based shortcuts | `Ctrl`/`Cmd` combinations do not collide with AT navigation |
| If single-key, allow it to be turned off, remapped, or scoped to a focused component | The conformance requirement |
| Document the shortcuts somewhere discoverable | Otherwise they are a hidden feature |
| Do not hijack browser or AT shortcuts | `Ctrl+F`, screen-reader keys, and platform shortcuts are not yours |

## Testing the keyboard model

```text
1. Unplug the pointer (or disable the trackpad).
2. Tab from the top of the page:
     - is every interactive element reachable?
     - does the order match the visual order?
     - is the focus indicator visible at every stop?
3. Complete the primary task using only the keyboard.
4. Exercise every composite widget with its arrow keys.
5. Open an overlay; confirm focus moves in, is contained, and returns on close.
6. Confirm Escape exits every overlay.
7. Confirm you never get stuck (no trap).
8. Confirm no single-key shortcut fires while simply typing in a field.
```

Steps 2 and 7 find the majority of keyboard defects. Both take minutes.

## The keyboard checklist

- [ ] Every interactive component is operable with the keyboard alone (CR3)
- [ ] Enter and Space activate controls, per the platform's convention
- [ ] Every composite widget uses one tab stop, with arrows inside
- [ ] The key contract for each widget is documented where the component is defined
- [ ] Escape exits every overlay and cancels every cancellable operation
- [ ] No keyboard trap exists outside a modal, and the modal has Escape
- [ ] A skip link exists, is first in the tab order, and becomes visible on focus
- [ ] Shortcuts are modifier-based, or single-key with a documented way to disable them
- [ ] Browser and AT shortcuts are not hijacked
- [ ] Verified by completing the primary task with the keyboard alone, with the pointer disabled
