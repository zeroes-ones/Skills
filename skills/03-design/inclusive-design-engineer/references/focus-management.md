# Focus Management

<!-- STANDARD: 3min -- focus order, containment, restoration and visibility -->

## Focus is a single-owner resource

At any moment exactly one element has focus, and its position is the user's location in the
interface. Everything in this file follows from that: focus must be *somewhere sensible*, must be
*movable deliberately*, and must be *visible*.

For a keyboard user, focus is the pointer. For a screen-reader user, it is the reading cursor. A
focus defect is therefore not a cosmetic issue — it is the equivalent of hiding the cursor and
hoping the user guesses where they are.

## R3: focus visibility

The most common accessibility regression in modern CSS is the focus ring removed for aesthetic
reasons:

```css
/* ❌ Removes the pointer for every keyboard user */
*:focus { outline: none; }
button:focus { outline: none; }
```

```css
/* ✅ A visible indicator, drawn to the brand */
:focus-visible {
  outline: 3px solid var(--focus-ring);
  outline-offset: 2px;
  border-radius: 2px;
}
```

Requirements for the indicator:

| Requirement | Why |
|---|---|
| Visible against **every** background it can appear on | A ring invisible on a dark surface is not a ring |
| Sufficient area to be perceived | A hairline is not visible at a glance |
| Present on every focusable element | Including links, custom controls, and elements inside dark panels |
| Distinguishable from the selected/hover state | Focus and selection are different concepts |
| Drawn for both light and dark themes | A single colour rarely works on both |

Use `:focus-visible` rather than `:focus` so a pointer click does not draw the ring, while keyboard
navigation always does. This is the mechanism that makes it possible to remove the ring on click
without removing it for keyboard users — the problem `outline: none` was trying to solve.

**The two-surface test:** focus an element that sits on a coloured background, then one on the
page background, then one inside a dark panel. If any of the three is hard to see, the indicator
fails.

## Focus order

Focus order is the sequence of destinations. It should follow the reading order and the task order.

| Rule | Detail |
|---|---|
| DOM order is focus order | Do not use positive `tabindex` to reorder; fix the DOM |
| Focus order matches visual order | Otherwise the user jumps around the page |
| One tab stop per composite widget | A list of ten items is one stop with arrow keys inside, not ten stops |
| No tab stop on non-interactive content | A heading is not a destination |
| Focusable elements are visible | A focusable element hidden visually is a trap |

```bash
# Positive tabindex is almost always a defect — it breaks the natural order
grep -rn 'tabindex="[1-9]' src/
```

**The keyboard walkthrough test:** unplug the pointer, press Tab from the top of the page, and
confirm (a) every interactive element is reachable, (b) the order matches the visual order, (c) the
indicator is visible at every stop, (d) you can complete the primary task without a pointer.

## Roving tabindex

Composite widgets (tabs, menus, toolbars, grids) use one tab stop with internal arrow-key
navigation. This is the **roving tabindex** pattern:

```text
Tab      → moves into the widget (lands on the active/selected item)
Arrows   → move between items within the widget
Tab      → moves out of the widget (to the next control after it)
```

The alternative is `aria-activedescendant`, where the container keeps focus and points at the
active child. Both are correct; the combobox pattern specifically requires the
`activedescendant` form because the input must keep focus to accept typing.

Implementing a widget as ten separate tab stops is the common defect: the keyboard user must press
Tab ten times to pass one widget, which makes the interface unusable in practice.

## Focus containment

A modal overlay must contain focus while it is open, so the user cannot tab into the page behind
it.

| Requirement | Detail |
|---|---|
| Move focus in on open | To the first meaningful element, or the dialog itself |
| Keep focus inside | Tab and Shift+Tab cycle within the dialog |
| Make the background inert | Not just visually covered — unreachable and unannounced |
| Restore on close | Focus returns to the invoking element, not the document body |

**The background-inert problem:** a visual overlay does not, by itself, prevent a screen reader from
reading the page behind it, nor a keyboard user from tabbing into it. The dialog must make the
background inert — via the platform's mechanism, a modal element, or explicit inert marking —
otherwise the "modal" is only modal to the mouse.

The most common failure after containment is restoration: the dialog closes, and focus is dropped
at the document body, so the user must navigate from the top of the page again.

## Focus restoration

```text
Opened from  →  focus moves to the overlay
Closed       →  focus returns to THE ELEMENT THAT OPENED IT
```

Store the invoking element when opening, and restore it on close. This applies to dialogs, drawers,
popovers, menus, tooltips and inline expansions.

Where the invoking element no longer exists (the row was deleted, for example), move focus to the
nearest sensible neighbour — a sibling row, the list, or the enclosing region — and never to the
document body.

## Focus management for route and view changes

In single-page applications, a route change does not move focus, so the AT user stays where they
were while the content changes beneath them.

| Change | Focus should |
|---|---|
| New page/view | Move to the page heading or the main region, once |
| In-page tab/panel switch | Move to the panel, or leave focus on the tab (per the pattern) |
| Content added | Generally not move — announce it instead (live region) |
| Content removed | Move to the nearest remaining element |
| An error blocks submission | Move to the error summary |

## What must never happen

| Never | Why |
|---|---|
| `outline: none` with no replacement | Removes the keyboard user's pointer (R3) |
| Focus lost to the document body after an overlay closes | The user must start over |
| Focus moved on page load to a random element | Disorients, especially in a screen reader |
| Positive `tabindex` reordering | Breaks the natural order elsewhere |
| Focusable element inside `aria-hidden` | Reachable but nameless — the worst of both |
| `display: none` used to "hide" a control that must be focusable | Removes it from the tree entirely |
| A modal that does not contain focus | Equivalent to having no modal |
| Autofocus on a destructive control | One keystroke from an accident |

## The focus checklist

- [ ] A visible focus indicator on every focusable element, on every surface (R3)
- [ ] `:focus-visible` used, so the ring is not drawn on pointer clicks
- [ ] Focus order matches DOM order and visual order; no positive `tabindex`
- [ ] One tab stop per composite widget, with arrow keys inside
- [ ] Overlays move focus in, contain it, and make the background inert
- [ ] Focus is restored to the invoking element on close
- [ ] Route changes move focus to the new view's heading or main region
- [ ] No focusable element is inside `aria-hidden` content
- [ ] Focus is never lost to the document body
- [ ] Verified by a keyboard-only walkthrough completing the primary task
