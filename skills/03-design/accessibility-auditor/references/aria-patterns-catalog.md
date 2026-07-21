---
author: Sandeep Kumar Penchala
type: reference
domain: accessibility
version: "1.0"
last_updated: 2026-07-21
---

# ARIA Patterns Catalog

Complete catalog of ARIA design patterns: landmarks, composite widgets, live regions, and relationship attributes. Each pattern includes the correct ARIA roles, states, keyboard interaction model, and common misuse/fix pairs.

## First Rule of ARIA

> If you can use a native HTML element or attribute with the semantics and behavior you need already built in, instead of re-purposing an element and adding an ARIA role, state or property to make it accessible, **then do so**.

In other words: **No ARIA is better than bad ARIA.** Before reaching for ARIA, exhaust all native HTML solutions.

---

## Landmark Patterns

Landmarks allow screen reader users to navigate directly to major page sections.

| Landmark | HTML Equivalent | ARIA Role | Usage | Common Mistakes |
|----------|----------------|-----------|-------|-----------------|
| **Banner** | `<header>` (when top-level) | `role="banner"` | One per page. Site-wide header with logo, primary nav, search. | Multiple banners on one page. Placing `<header>` inside `<article>` — that's not a banner. |
| **Navigation** | `<nav>` | `role="navigation"` | Primary, secondary, breadcrumb, and footer navigation groups. | Not labeling multiple navs (use `aria-label` for each). Wrapping every link list in a nav. |
| **Main** | `<main>` | `role="main"` | One per page. The primary content area. | Multiple main elements. Placing main inside another landmark. |
| **Complementary** | `<aside>` | `role="complementary"` | Content tangential to main content (sidebar, related links). | Using for ads (use ad role instead if needed). |
| **Contentinfo** | `<footer>` (when top-level) | `role="contentinfo"` | One per page. Site-wide footer with copyright, legal links. | Multiple contentinfo landmarks. Footer inside article is not contentinfo. |
| **Search** | — (no native element) | `role="search"` | The search form/region. | Not labeling when multiple search regions exist. |
| **Form** | `<form>` (with accessible name) | `role="form"` | A form region (only when form has no accessible name via `<form aria-label="...">`). | Wrapping every `<form>` in role="form" — only needed if native form lacks accessible name. |
| **Region** | `<section>` (with accessible name) | `role="region"` | Generic landmark for named sections. | Overusing — prefer specific landmarks. Not providing accessible name. |

### Landmark Best Practices
- Every page must have at minimum: `<header>` (banner), `<nav>`, `<main>`, `<footer>` (contentinfo).
- Label every landmark that has multiple instances: `<nav aria-label="Primary">`, `<nav aria-label="Breadcrumb">`.
- Landmarks should contain all page content — no orphan content outside landmarks.
- **Testing**: Use screen reader rotor/menu to list all landmarks. Verify navigation between them makes sense.

---

## Widget Patterns

### Accordion

**When to use**: Collapsible sections where only one or multiple panels can be open at a time.

```html
<!-- Accordion container -->
<div role="region" aria-labelledby="accordion-heading">
  <h2 id="accordion-heading">FAQs</h2>
  
  <!-- Accordion header/trigger -->
  <h3>
    <button id="accordion-trigger-1"
            aria-expanded="true"
            aria-controls="accordion-panel-1">
      What is your return policy?
      <span aria-hidden="true" class="icon">▼</span>
    </button>
  </h3>
  
  <!-- Accordion panel -->
  <div id="accordion-panel-1"
       role="region"
       aria-labelledby="accordion-trigger-1"
       hidden="until-found">
    Returns accepted within 30 days...
  </div>
</div>
```

**Keyboard**: Enter/Space toggles panel. Optional: Arrow keys navigate between headers (recommended for accordions with many items).

**Common Misuse**:
- ❌ Using `<div onclick>` instead of `<button>` — loses keyboard and role
- ❌ Toggling `aria-expanded` but forgetting to show/hide the panel
- ❌ Using `aria-hidden` on the panel instead of the `hidden` attribute — focusable children stay in tab order

---

### Dialog (Modal)

**When to use**: A window overlaid on the page requiring user interaction before returning to the underlying content.

```html
<!-- Backdrop -->
<div class="dialog-backdrop"></div>

<!-- Dialog -->
<div role="dialog"
     aria-modal="true"
     aria-labelledby="dialog-title"
     aria-describedby="dialog-description"
     tabindex="-1">
  
  <h2 id="dialog-title">Confirm Deletion</h2>
  
  <p id="dialog-description">
    Are you sure you want to delete this item? This action cannot be undone.
  </p>
  
  <button>Cancel</button>
  <button>Delete</button>
  
  <!-- Close button -->
  <button aria-label="Close dialog">✕</button>
</div>
```

**Required State Management (JavaScript)**:
1. On open: Save last focused element. Move focus to dialog (or first focusable element). Trap focus within dialog.
2. On close: Return focus to the saved element.
3. Escape key closes the dialog.

**Keyboard**:
- Tab/Shift+Tab: Cycle focus within dialog (trap focus — Tab from last element goes to first, Shift+Tab from first goes to last)
- Escape: Close dialog (and fire cancel action)
- Enter/Space: Activate focused button

**Common Misuse**:
- ❌ Focus moves to dialog but isn't trapped — user Tabs into background page
- ❌ Focus is not returned on close — user is left at top of page
- ❌ Using `role="alertdialog"` for confirmation dialogs — correct for destructive/blocking actions
- ❌ Missing `aria-modal="true"` — screen reader may read background content
- ❌ Setting `aria-hidden="true"` on the dialog itself instead of the background content

**AlertDialog variant**: Use `role="alertdialog"` only when the dialog's message is critically important (e.g., session timeout, destructive action). Identical keyboard behavior.

---

### Tabs

**When to use**: Content sections displayed one at a time via tab selection.

```html
<div role="region" aria-labelledby="tabs-title">
  <h2 id="tabs-title">Account Settings</h2>
  
  <!-- Tab list -->
  <div role="tablist" aria-label="Account settings tabs">
    <button role="tab"
            id="tab-1"
            aria-selected="true"
            aria-controls="tabpanel-1"
            tabindex="0">
      Profile
    </button>
    <button role="tab"
            id="tab-2"
            aria-selected="false"
            aria-controls="tabpanel-2"
            tabindex="-1">
      Security
    </button>
    <button role="tab"
            id="tab-3"
            aria-selected="false"
            aria-controls="tabpanel-3"
            tabindex="-1">
      Billing
    </button>
  </div>
  
  <!-- Tab panels -->
  <div role="tabpanel"
       id="tabpanel-1"
       aria-labelledby="tab-1"
       tabindex="0">
    Profile settings content...
  </div>
  <div role="tabpanel"
       id="tabpanel-2"
       aria-labelledby="tab-2"
       tabindex="0"
       hidden>
    Security settings content...
  </div>
  <div role="tabpanel"
       id="tabpanel-3"
       aria-labelledby="tab-3"
       tabindex="0"
       hidden>
    Billing settings content...
  </div>
</div>
```

**Keyboard (Automatic Activation — recommended)**:
- Left/Up Arrow: Move focus to previous tab, activate it immediately
- Right/Down Arrow: Move focus to next tab, activate it immediately
- Home: Move focus to first tab, activate
- End: Move focus to last tab, activate

**Keyboard (Manual Activation — for expensive content loads)**:
- Left/Up Arrow: Move focus to previous tab only (activate on Enter/Space)
- Right/Down Arrow: Move focus to next tab only (activate on Enter/Space)
- Home/End: Move focus to first/last tab

**Tab panel receives focus via `tabindex="0"`** so screen reader users can navigate directly to panel content. Roving tabindex on tabs (only the active tab has `tabindex="0"`, others have `tabindex="-1"`).

**Common Misuse**:
- ❌ Using `<a href>` links for tabs — tabs are controls, not navigation
- ❌ Not managing roving tabindex — all tabs get Tab key, creating excessive stops
- ❌ Forgetting `aria-controls` and `aria-labelledby` linking tabs to panels
- ❌ Using same-orientation arrows for both horizontal and vertical tab lists

---

### Menu (Navigation & Application)

**Navigation Menu** (site nav dropdown):

```html
<button id="menu-button"
        aria-expanded="false"
        aria-haspopup="true"
        aria-controls="menu-list">
  Products
</button>

<ul id="menu-list"
    role="menu"
    aria-labelledby="menu-button"
    hidden>
  <li role="none">
    <a role="menuitem" href="/products/widget" tabindex="-1">Widget</a>
  </li>
  <li role="none">
    <a role="menuitem" href="/products/gadget" tabindex="-1">Gadget</a>
  </li>
  <li role="separator"></li>
  <li role="none">
    <a role="menuitem" href="/products/all" tabindex="-1">View All</a>
  </li>
</ul>
```

**Application Menu** (desktop-like, dropdown with commands):

```html
<button id="app-menu-btn"
        aria-expanded="false"
        aria-haspopup="menu"
        aria-controls="app-menu">
  File
</button>

<ul id="app-menu"
    role="menu"
    aria-labelledby="app-menu-btn"
    hidden>
  <li role="none">
    <button role="menuitem" tabindex="-1">New File</button>
  </li>
  <li role="none">
    <button role="menuitem" tabindex="-1">Open...</button>
  </li>
  <!-- Submenu -->
  <li role="none">
    <button role="menuitem"
            aria-expanded="false"
            aria-haspopup="menu"
            aria-controls="recent-submenu"
            tabindex="-1">
      Recent Files
    </button>
    <ul id="recent-submenu" role="menu" aria-label="Recent Files" hidden>
      <li role="none">
        <button role="menuitem" tabindex="-1">document.md</button>
      </li>
    </ul>
  </li>
</ul>
```

**Keyboard (Navigation Menu, links)**:
- Tab to enter menu
- Up/Down Arrow: Navigate items (roving tabindex)
- Escape: Close menu, return focus to trigger
- Enter/Space: Activate link
- Letter key: Jump to item starting with that letter

**Keyboard (Application Menu, buttons)**:
- Tab to enter menu
- Up/Down Arrow: Navigate items
- Escape: Close menu, return focus to trigger
- Enter/Space: Activate item
- Right Arrow: Open submenu / Left Arrow: Close submenu

**Common Misuse**:
- ❌ Using `aria-haspopup="true"` instead of `aria-haspopup="menu"` — less informative
- ❌ Forgetting `aria-expanded` toggle on the trigger
- ❌ Not closing the menu on Escape
- ❌ Using `role="menu"` for navigation links — that's `role="navigation"`

---

### Combobox (Autocomplete / Select with Filter)

**List autocomplete with manual selection** (most accessible pattern):

```html
<label for="combo-input">Choose a fruit:</label>

<div role="combobox"
     aria-expanded="false"
     aria-owns="combo-listbox"
     aria-haspopup="listbox">
  
  <input id="combo-input"
         type="text"
         role="combobox"
         aria-expanded="false"
         aria-controls="combo-listbox"
         aria-autocomplete="list"
         aria-activedescendant=""
         autocomplete="off">
  
  <ul id="combo-listbox"
      role="listbox"
      aria-label="Fruits"
      hidden>
    <li role="option" id="combo-option-0" aria-selected="true">Apple</li>
    <li role="option" id="combo-option-1">Banana</li>
    <li role="option" id="combo-option-2">Cherry</li>
    <li role="option" id="combo-option-3">Date</li>
    <li role="option" id="combo-option-4">Elderberry</li>
  </ul>
</div>
```

**State Management**:
- `aria-expanded`: true when listbox is visible
- `aria-activedescendant`: ID of the currently highlighted option (instead of moving focus)
- `aria-selected`: true on the currently selected option(s) in the listbox

**Keyboard**:
- Alt+Down / Down Arrow (when closed): Open listbox
- Down/Up Arrow (when open): Move active descendant, announce option via screen reader
- Enter: Select active option, close listbox, populate input
- Escape: Close listbox without selecting
- Type: Filter options, open listbox if closed

**Common Misuse**:
- ❌ Moving focus to listbox instead of using `aria-activedescendant` — breaks typing
- ❌ Not announcing option count ("3 results available")
- ❌ Auto-selecting on arrow navigation (without Enter confirmation)
- ❌ Single-select acting as multi-select or vice versa — be explicit

---

### Disclosure (Show/Hide)

**Simpler alternative to Accordion** — use when you don't need multiple panels that act as a group.

```html
<button aria-expanded="false" aria-controls="disclosure-content">
  Show advanced settings
</button>

<div id="disclosure-content" hidden>
  Advanced setting fields...
</div>
```

**Difference from Accordion**: Disclosure does not require heading structure, multiple items, or exclusive open. One button, one panel. Simpler keyboard model (Enter/Space toggles; no arrow keys).

---

### Tooltip

**When to use**: Brief, non-interactive descriptive text for an element.

```html
<button aria-describedby="tooltip-save">
  💾
</button>

<div id="tooltip-save"
     role="tooltip"
     hidden>
  Save document (Ctrl+S)
</div>
```

**Important constraints**:
- Tooltips must be hoverable (mouse can move to tooltip without it disappearing)
- Must be dismissible via Escape
- Content must be short (1-2 lines) — for longer content, use a popover or dialog
- Tooltip must not obscure the trigger element
- Do not put interactive elements inside tooltips
- Show on hover AND focus (both `mouseenter`/`focus`), hide on `mouseleave`/`blur`/`Escape` with a 300ms delay

**Common Misuse**:
- ❌ Using `aria-label` AND tooltip together — redundant, tooltip should use `aria-describedby`
- ❌ Tooltips on disabled buttons — disabled buttons can't receive hover/focus
- ❌ Putting links or buttons inside tooltips — use a popover or dialog instead
- ❌ Content that scrolls or requires reading time — use Toggletip (click-triggered, dismissible)

---

## Live Region Patterns

Live regions announce dynamic content changes to screen readers without moving focus.

| Type | ARIA Attribute | When to Use | Example |
|------|---------------|-------------|---------|
| **Polite** | `aria-live="polite"` | Non-urgent updates. Announces after current screen reader utterance completes. | Search result count, "Loading complete," cart item count |
| **Assertive** | `aria-live="assertive"` | Critical updates. Interrupts current utterance. | Session expiring warning, critical error, action-failed alert |
| **Off** | `aria-live="off"` | Default. No announcement. | — |

### Specialized Live Region Roles

| Role | Live Behavior | Atomic | When to Use |
|------|--------------|--------|-------------|
| `role="status"` | `aria-live="polite"` + `aria-atomic="true"` | Yes | General status updates. Does NOT receive focus. |
| `role="alert"` | `aria-live="assertive"` + `aria-atomic="true"` | Yes | Critical alerts requiring immediate attention. |
| `role="log"` | `aria-live="polite"` | No | Streaming logs, chat history, console output. New messages append. |
| `role="marquee"` | `aria-live="off"` by default | No | Auto-scrolling content like tickers. |
| `role="timer"` | `aria-live="off"` | No | Countdown timers, clocks. |
| `role="progressbar"` | — (use `aria-valuenow`) | — | Progress indicators. Update `aria-valuenow` as progress changes. |

### Live Region Implementation Rules

1. The live region element MUST exist in the DOM before content changes are injected.
2. Pre-populate `aria-live` regions with the live attribute on an empty container at page load.
3. `aria-atomic="true"`: announces the entire region on any change. `false`: announces only the changed nodes.
4. Use `aria-relevant="additions removals"` to control what changes are announced (default: additions + text).
5. Be careful with `aria-live="assertive"` — overuse desensitizes users and degrades experience.

```html
<!-- Pre-created live region (DO NOT dynamically create this element) -->
<div id="live-region" aria-live="polite" aria-atomic="true"></div>

<!-- In JavaScript, inject text into existing container -->
<script>
  // Correct: inject into existing live region
  document.getElementById('live-region').textContent = '5 results found';
  
  // Incorrect: dynamically create the live region — may not be detected
  // document.body.insertAdjacentHTML('beforeend', '<div aria-live="polite">5 results found</div>');
</script>
```

### Common Live Region Mistakes
- ❌ Creating the live region element dynamically at the time of the announcement
- ❌ Using `aria-live` without `aria-atomic` — partial updates may be confusing
- ❌ Repeatedly injecting the same text (screen reader ignores duplicate announcements — use a technique to force re-read)
- ❌ Forgetting to clear the live region content after announcement
- ❌ Using `role="alert"` for non-critical messages — desensitizes users

---

## Relationship Attributes Quick Reference

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `aria-labelledby` | Links element to one or more elements as its label (ID references, space-separated) | `<div id="dialog" aria-labelledby="title-el">` |
| `aria-describedby` | Links element to description element(s) | `<input aria-describedby="hint error">` |
| `aria-controls` | Indicates element controls another element | `<button aria-controls="menu-list">` |
| `aria-owns` | Indicates parent-child relationship when not reflected in DOM | `<ul aria-owns="option-external">` |
| `aria-activedescendant` | Points to active descendant in composite widget | `<input aria-activedescendant="option-3">` |
| `aria-details` | Links to extended description (like `<details>`) | `<img aria-details="long-desc">` |
| `aria-errormessage` | Links field to its error message | `<input aria-errormessage="email-error">` |

---

## Common ARIA Misuse Patterns & Fixes

| Misuse | Problem | Fix |
|--------|---------|-----|
| `role="button"` on a `<div>` | Loses native button behavior (form submission, disabled state, Enter/Space) | Use `<button>`. If impossible, implement full keyboard handler and `tabindex="0"` |
| `aria-label="submit"` on a button with text "Save" | Screen reader says "submit" but sighted user sees "Save" → 2.5.3 violation | `aria-label` must include visible text: `aria-label="Save document"` |
| `aria-hidden="true"` on a parent of a focusable element | Focusable children become invisible to screen reader but remain in tab order | Never put focusable elements inside `aria-hidden="true"` |
| `tabindex="0"` on non-interactive elements | Everything becomes a tab stop, overwhelming keyboard users | Only interactive elements should be in tab order |
| `tabindex="1"`, `tabindex="2"`, etc. | Custom tab orders always diverge from visual order and DOM order → 2.4.3 violation | Only use `tabindex="0"` or `tabindex="-1"`. Never positive integers. |
| `aria-live` on `<body>` or large container | Too much content announced at once | Scope live regions to the smallest relevant container |
| `role="navigation"` on every `<ul>` with links | Too many landmarks, confusing navigation | Only on primary/secondary navigation regions |
| Missing `aria-expanded` on toggles | Screen reader can't determine if the controlled content is visible | Always pair with expandable content |
| `role="presentation"` or `role="none"` on focusable element | Removes semantics but element is still in tab order — confusing | Use on layout-only elements. Never on focusable or interactive elements. |
| `aria-disabled="true"` without disabling functionality | Screen reader announces disabled but element is clickable | Either use `disabled` attribute on native elements or fully prevent interaction and style accordingly |

---

## Decision Flowchart

```
Need interactive widget?
  │
  ├─ Is there a native HTML element that does this?
  │   YES → Use it. Done.
  │   NO  ↓
  │
  ├─ Tab panel group? → role="tablist" + role="tab" + role="tabpanel"
  ├─ Expand/collapse section? → <button aria-expanded> + hidden panel
  ├─ Overlay requiring interaction? → role="dialog" + aria-modal + focus trap
  ├─ Dropdown with options/links? → role="menu" / role="listbox" + aria-haspopup
  ├─ Autocomplete input? → role="combobox" + aria-activedescendant + role="listbox"
  ├─ Brief hover text? → role="tooltip" + aria-describedby
  ├─ Tree navigation? → role="tree" + role="treeitem" + aria-expanded
  ├─ Dynamic status update? → role="status" or aria-live="polite"
  ├─ Critical alert? → role="alert"
  └─ None of the above? → Reconsider if ARIA is the right solution, or consult the ARIA Authoring Practices Guide
```

---

## References

- ARIA Authoring Practices Guide (APG): https://www.w3.org/WAI/ARIA/apg/
- ARIA Specification: https://www.w3.org/TR/wai-aria-1.2/
- ARIA in HTML: https://www.w3.org/TR/html-aria/
- MDN ARIA Guide: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA
- Practical ARIA Examples (WAI): https://www.w3.org/WAI/ARIA/apg/example-index/
