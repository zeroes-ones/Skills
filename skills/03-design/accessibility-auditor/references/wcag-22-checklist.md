---
author: Sandeep Kumar Penchala
type: reference
domain: accessibility
version: "1.0"
last_updated: 2026-07-21
---

# WCAG 2.2 Compliance Checklist

Complete success criteria checklist with testing methodology and implementation guidance per criterion. Organized by the four POUR principles: Perceivable, Operable, Understandable, Robust.

## How to Use This Checklist

For each criterion, the table provides:
- **Level**: A (minimum), AA (standard target), AAA (stretch)
- **Test Method**: Auto (automated tools), Manual (visual/manual review), SR (screen reader), KB (keyboard-only)
- **Priority**: P0 (blocker/legal risk), P1 (high impact), P2 (moderate), P3 (enhancement)

---

## Principle 1: Perceivable

Information and user interface components must be presentable to users in ways they can perceive.

### 1.1 Text Alternatives

Provide text alternatives for any non-text content.

| # | Success Criterion | Level | Test Method | Priority | Implementation Guidance |
|---|-------------------|-------|-------------|----------|------------------------|
| 1.1.1 | **Non-text Content** — All non-text content has a text alternative serving the equivalent purpose | A | Auto + Manual | P0 | **Images**: Meaningful images need descriptive `alt` text conveying purpose, not appearance. Decorative images use `alt=""`. Complex images (charts, diagrams) need both short `alt` and long description via `aria-describedby` or adjacent text. **Controls**: Input type="image" needs `alt` describing function. **CAPTCHA**: Must provide multiple modalities (audio + visual) and a contact option for human assistance. **Testing**: Run axe-core for missing alt detection; manually verify alt quality — "photo" is not equivalent. |

### 1.2 Time-based Media

Provide alternatives for time-based media (audio, video).

| # | Success Criterion | Level | Test Method | Priority | Implementation Guidance |
|---|-------------------|-------|-------------|----------|------------------------|
| 1.2.1 | **Audio-only and Video-only (Prerecorded)** — Audio-only: transcript. Video-only: transcript or audio track conveying same info | A | Manual | P1 | Audio podcasts need full transcripts (speaker labels, sound descriptions). Silent video tutorials need text or audio description of the visual actions. |
| 1.2.2 | **Captions (Prerecorded)** — Captions for all prerecorded audio in synchronized media | A | Manual | P0 | Use WebVTT format. Captions must identify speakers, include sound effects in [brackets], sync within 100ms of audio. Auto-generated captions must be reviewed by a human — raw auto-captions do not satisfy this criterion. |
| 1.2.3 | **Audio Description or Media Alternative (Prerecorded)** — Video content has audio description or full text alternative | A | Manual | P1 | Audio description narrates key visual information during natural pauses. Alternative: provide a transcript that includes both dialogue and visual descriptions. |
| 1.2.4 | **Captions (Live)** — Captions for live synchronized media | AA | Manual | P2 | Live streams need real-time captions (CART or automated + human review). Requires captioning service integration. |
| 1.2.5 | **Audio Description (Prerecorded)** — Audio description for prerecorded video | AA | Manual | P1 | Same as 1.2.3 but audio description is REQUIRED (not optional with transcript alternative). |
| 1.2.6 | **Sign Language (Prerecorded)** — Sign language interpretation for prerecorded audio | AAA | Manual | P3 | Provide a sign language overlay or separate video. Requires professional interpretation. |
| 1.2.7 | **Extended Audio Description (Prerecorded)** — Extended description when pauses insufficient | AAA | Manual | P3 | If natural pauses are too short, pause the video to insert extended description. |
| 1.2.8 | **Media Alternative (Prerecorded)** — Full text alternative for all prerecorded synchronized media | AAA | Manual | P3 | Complete transcript combining dialogue, actions, and visual descriptions in reading order. |
| 1.2.9 | **Audio-only (Live)** — Live audio-only content has a text alternative | AAA | Manual | P3 | Live radio/podcast needs real-time text stream. |

### 1.3 Adaptable

Create content that can be presented in different ways without losing information or structure.

| # | Success Criterion | Level | Test Method | Priority | Implementation Guidance |
|---|-------------------|-------|-------------|----------|------------------------|
| 1.3.1 | **Info and Relationships** — Information, structure, and relationships conveyed through presentation are programmatically determinable | A | Auto + Manual + SR | P0 | Use semantic HTML: `<header>`, `<nav>`, `<main>`, `<footer>`, `<article>`, `<aside>`. Tables use `<th>` with `scope="col/row"`. Forms use `<fieldset>` + `<legend>` for groups, `<label>` (explicit via `for` or implicit via wrapping) for every input. Headings form a logical outline without skipped levels. Lists use `<ul>/<ol>/<dl>`. **Common failures**: Using `<div>` styled as a heading; placeholder-only form labels; tables without header cells. **Testing**: Disable CSS — does structure remain clear? Walk page with screen reader — is the heading hierarchy logical? |
| 1.3.2 | **Meaningful Sequence** — When the sequence affects meaning, the reading order is programmatically determinable | A | Manual + SR | P0 | DOM order must match visual reading order. Do not use CSS `order`, `flex-direction: row-reverse`, or absolute positioning to reorder content in a way that changes meaning. **Testing**: Remove CSS — does the content order still make sense? |
| 1.3.3 | **Sensory Characteristics** — Instructions do not rely solely on sensory characteristics (shape, color, size, location, sound) | A | Manual | P1 | "Click the red button" fails. "Click the 'Submit' button" passes. "Press the round button on the left" fails — name it. Icons alone without labels fail. **Testing**: Search instructions for color/shape/position references. |
| 1.3.4 | **Orientation** — Content is not restricted to portrait or landscape unless essential | AA | Auto + Manual | P1 | Do not use `screen` media query with orientation lock. If orientation lock is essential (piano app), provide a message. **Testing**: Rotate device or use responsive design mode. |
| 1.3.5 | **Identify Input Purpose** — The purpose of each input field collecting user information is programmatically determinable | AA | Auto | P1 | Use `autocomplete` attribute with valid WCAG 2.2 values: `name`, `email`, `tel`, `address-line1`, `bday`, `organization`, `cc-number`, etc. **Testing**: axe-core has an autocomplete rule. |
| 1.3.6 | **Identify Purpose** — In content using markup languages, the purpose of UI components, icons, and regions is programmatically determinable | AAA | Manual + SR | P3 | Use ARIA landmarks with labels (`aria-label` or `aria-labelledby`). Icons need `aria-label`. |

### 1.4 Distinguishable

Make it easier for users to see and hear content including separating foreground from background.

| # | Success Criterion | Level | Test Method | Priority | Implementation Guidance |
|---|-------------------|-------|-------------|----------|------------------------|
| 1.4.1 | **Use of Color** — Color is not the only visual means of conveying information | A | Manual | P0 | Error states need icon + text, not just red border. Links must be underlined (or have 3:1 contrast + non-color indicator on hover/focus). Charts need patterns or labels in addition to color. **Testing**: View page in grayscale (or use a color blindness simulator). |
| 1.4.2 | **Audio Control** — Auto-playing audio > 3 seconds has pause/stop or volume control | A | Manual | P1 | Provide pause/stop button. Do NOT auto-play music or video with audio. If unavoidable, place controls first in tab order. |
| 1.4.3 | **Contrast (Minimum)** — Text has 4.5:1 contrast (3:1 for large text) against background | AA | Auto | P0 | Large text = 18px+ bold or 24px+ regular. Test with axe-core or Colour Contrast Analyser. Text over images/gradients needs careful testing — sample multiple points. Logotypes and inactive UI components are exempt. |
| 1.4.4 | **Resize Text** — Text can be resized up to 200% without loss of content or function | AA | Manual | P1 | Use relative units (`em`, `rem`, `%`) for text sizes. Test at 200% browser zoom. Content must not overlap, truncate, or scroll horizontally. **Testing**: Set browser zoom to 200%, verify all content is accessible. |
| 1.4.5 | **Images of Text** — Use text rather than images of text except for logos and essential cases | AA | Manual + Auto | P1 | Infographics, charts, and logos can use images of text but need alt text. Buttons and headings must never be images of text. **Testing**: Inspect for `<img>` containing text that should be real text. |
| 1.4.6 | **Contrast (Enhanced)** — Text has 7:1 contrast (4.5:1 for large text) | AAA | Auto | P3 | This is the AAA-enhanced threshold. Required only when targeting AAA. |
| 1.4.7 | **Low or No Background Audio** — Audio content has low/no background sounds or can be turned off | AAA | Manual | P3 | Foreground audio must be 20dB louder than background. |
| 1.4.8 | **Visual Presentation** — User can customize foreground/background colors, text spacing, and line length | AAA | Manual | P3 | Provide user stylesheet support. Line length max 80 characters. No text justification. |
| 1.4.9 | **Images of Text (No Exception)** — Only use images of text for pure decoration or logo | AAA | Manual | P3 | Stricter than 1.4.5 — no exception for essential images of text. |
| 1.4.10 | **Reflow** — Content reflows without requiring horizontal scrolling at 320px width with 400% zoom | AA | Manual | P1 | Equivalent to 1280px viewport at 400% zoom = 320 CSS px wide. No bidirectional scrolling. Exceptions: data tables, maps, toolbars. **Testing**: Set viewport to 320px wide, verify no horizontal scroll. |
| 1.4.11 | **Non-text Contrast** — UI components and graphical objects have 3:1 contrast against adjacent colors | AA | Auto + Manual | P0 | Covered: input borders, button boundaries, focus indicators, icons (unless decorative), chart segments. Not covered: disabled states (if truly disabled), decorative elements, logos. **Testing**: Use Colour Contrast Analyser on component edges. |
| 1.4.12 | **Text Spacing** — Content supports user text spacing overrides without loss | AA | Manual | P1 | Must handle: line-height 1.5×, letter-spacing 0.12em, word-spacing 0.16em, paragraph spacing 2×. Do not use `!important` or fixed-height containers. **Testing**: Apply a text-spacing bookmarklet or use browser dev tools to override styles. |
| 1.4.13 | **Content on Hover or Focus** — Dismissible, hoverable, and persistent tooltip/toolbar content | AA | Manual + KB | P1 | Hover-triggered content must be: dismissible without moving pointer (Esc), hoverable (can move pointer to the content without it disappearing), persistent until dismissed (not auto-dismissed by timeout). **Testing**: Trigger a tooltip, move pointer to it, press Esc. |

---

## Principle 2: Operable

User interface components and navigation must be operable.

### 2.1 Keyboard Accessible

Make all functionality available from a keyboard.

| # | Success Criterion | Level | Test Method | Priority | Implementation Guidance |
|---|-------------------|-------|-------------|----------|------------------------|
| 2.1.1 | **Keyboard** — All functionality operable through keyboard interface | A | KB | P0 | Every interactive element must be focusable and actionable via keyboard. No keyboard traps. Custom widgets must implement ARIA Authoring Practices keyboard patterns. **Testing**: Tab through entire interface. Activate everything with Enter/Space. No dead ends. |
| 2.1.2 | **No Keyboard Trap** — Focus can move away from any component using standard keyboard methods | A | KB | P0 | Tab/Shift+Tab must always work. Arrow keys, Escape must work per widget pattern. If non-standard key is required, provide instructions. **Testing**: Enter every modal, dialog, and custom widget — verify you can always Tab/Esc out. |
| 2.1.3 | **Keyboard (No Exception)** — All functionality operable via keyboard without exception | AAA | KB | P3 | Even drawing apps, flight simulators, etc. must provide keyboard equivalents. |
| 2.1.4 | **Character Key Shortcuts** — Single-character shortcuts can be remapped, turned off, or are only active on focus | A | Manual | P2 | Single-letter shortcuts (e.g., press 'S' to search) must be: turn-off-able, remappable, or active only when component has focus. Modifier-key combinations (Ctrl+S) are exempt. **Testing**: Identify all single-key shortcuts. |

### 2.2 Enough Time

Provide users enough time to read and use content.

| # | Success Criterion | Level | Test Method | Priority | Implementation Guidance |
|---|-------------------|-------|-------------|----------|------------------------|
| 2.2.1 | **Timing Adjustable** — Time limits can be turned off, adjusted, or extended | A | Manual | P1 | For any time limit (session timeout, quiz, auction): user must be able to turn off, adjust to 10× default, or extend (with 20s warning at least 20s before expiry). Real-time exceptions: auctions where extension would invalidate the activity. **Testing**: Identify all timeouts. Start a session and verify warning appears and extension works. |
| 2.2.2 | **Pause, Stop, Hide** — Moving, blinking, scrolling, or auto-updating content can be paused, stopped, or hidden | A | Manual | P1 | Auto-advancing carousels need pause button. Auto-updating live feeds need pause. Animations triggered by interaction have no requirement. Pure decoration animations are exempt. **Testing**: Check for any content that moves or updates without user initiation. |
| 2.2.3 | **No Timing** — Timing is not an essential part of the activity (except non-interactive media) | AAA | Manual | P3 | No content time limits at all. Exceptions: real-time events, non-interactive synchronized media. |
| 2.2.4 | **Interruptions** — Interruptions (alerts, updates) can be postponed or suppressed | AAA | Manual | P3 | Non-emergency interruptions must be user-controlled. |
| 2.2.5 | **Re-authenticating** — When session expires, user can continue without data loss | AAA | Manual | P3 | Re-authentication must preserve all data. |
| 2.2.6 | **Timeouts** — Users must be warned about inactivity timeouts causing data loss | AAA | Manual | P3 | Warning at session start, not just before timeout. |

### 2.3 Seizures and Physical Reactions

Do not design content in a way known to cause seizures or physical reactions.

| # | Success Criterion | Level | Test Method | Priority | Implementation Guidance |
|---|-------------------|-------|-------------|----------|------------------------|
| 2.3.1 | **Three Flashes or Below Threshold** — No content flashes more than 3 times per second | A | Auto | P0 | Flashes that exceed the general flash and red flash thresholds are prohibited. Use Photosensitive Epilepsy Analysis Tool (PEAT). **Testing**: Run PEAT on any animations with flashing elements. |
| 2.3.2 | **Three Flashes** — No content flashes more than 3 times per second | AAA | Auto | P3 | Even lower threshold than 2.3.1. |
| 2.3.3 | **Animation from Interactions** — Motion animation triggered by interaction can be disabled unless essential | AAA | Manual | P3 | Respect `prefers-reduced-motion`. |

### 2.4 Navigable

Provide ways to help users navigate, find content, and determine where they are.

| # | Success Criterion | Level | Test Method | Priority | Implementation Guidance |
|---|-------------------|-------|-------------|----------|------------------------|
| 2.4.1 | **Bypass Blocks** — Mechanism to skip repeated blocks of content | A | KB + SR | P0 | Provide a "Skip to main content" link as the first focusable element. Use landmark regions (`<main>`, `<nav>`) so screen readers can jump. **Testing**: Load page, press Tab — is "Skip to main" the first item? |
| 2.4.2 | **Page Titled** — Web pages have descriptive and unique titles | A | Auto + Manual | P1 | `<title>` must describe the page's purpose/content. Include current step in multi-step flows (e.g., "Checkout — Step 2 of 4: Shipping"). **Testing**: Manually review page titles for uniqueness and descriptiveness. |
| 2.4.3 | **Focus Order** — Focusable components receive focus in a meaningful order | A | KB | P0 | Tab order follows visual reading order (typically DOM order). Do not use `tabindex` > 0. `tabindex="0"` is acceptable. **Testing**: Tab through the page — is the order logical? |
| 2.4.4 | **Link Purpose (In Context)** — Purpose of each link can be determined from link text alone or with programmatic context | A | Auto + Manual | P1 | Avoid "click here", "read more", "learn more". Link text must describe the destination. Context can come from: same sentence, enclosing list item, enclosing paragraph, or `aria-label`/`aria-labelledby`. **Testing**: List all links with a screen reader — each must make sense in isolation. |
| 2.4.5 | **Multiple Ways** — More than one way to locate a page within a set of pages (unless it's a step in a process) | AA | Manual | P2 | Provide at least two: navigation menu, search, sitemap, breadcrumbs, related links. Multi-step processes (checkout, wizard) are exempt. **Testing**: For any non-process page, identify at least two navigation methods. |
| 2.4.6 | **Headings and Labels** — Headings and labels are descriptive and informative | AA | Manual | P1 | Headings must outline the page structure. Labels must describe input purpose. Avoid generic labels like "Enter value." **Testing**: Review heading outline. Verify each label is descriptive. |
| 2.4.7 | **Focus Visible** — Any keyboard-operable UI has a visible focus indicator | AA | Manual + KB | P0 | Focus indicator must be visible on ALL interactive elements. Minimum 2px outline or area change. Must have 3:1 contrast against adjacent colors. **Testing**: Tab through entire interface. Focus indicator must never disappear. Use `:focus-visible` for mouse vs. keyboard differentiation. |
| 2.4.8 | **Location** — Information about the user's location within a set of pages is available | AAA | Manual | P3 | Breadcrumbs, current step indicator, or highlighted navigation item. |
| 2.4.9 | **Link Purpose (Link Only)** — Purpose of each link identified from link text alone | AAA | Auto + Manual | P3 | Stricter than 2.4.4 — no context from surrounding text allowed. |
| 2.4.10 | **Section Headings** — Section headings organize content | AAA | Manual | P3 | All sections of content must have a heading. |
| 2.4.11 | **Focus Not Obscured (Minimum)** — When a UI component receives focus, it is not fully hidden by author-created content | AA | KB + Manual | P1 | Sticky headers/footers must not cover focused elements. Modals must not have content behind them that receives focus. **Testing**: Tab through all elements — verify focused element is at least partially visible. |
| 2.4.12 | **Focus Not Obscured (Enhanced)** — Focused component is entirely visible (not just partially) | AAA | KB + Manual | P3 | Focused element must be 100% visible, not just partially. |
| 2.4.13 | **Focus Appearance** — Focus indicator has minimum area and contrast | AAA | Manual | P3 | 2 CSS px minimum perimeter, or area at least 4 CSS px thick along shortest side. 3:1 contrast minimum from unfocused state, adjacent colors, and same pixels in unfocused state. |

### 2.5 Input Modalities

Make it easier for users to operate functionality through various inputs beyond keyboard.

| # | Success Criterion | Level | Test Method | Priority | Implementation Guidance |
|---|-------------------|-------|-------------|----------|------------------------|
| 2.5.1 | **Pointer Gestures** — Multi-point or path-based gestures have single-pointer alternatives | A | Manual | P1 | Pinch-to-zoom needs +/- buttons. Swipe needs tap/click alternatives. Drawing/signing is exempt. **Testing**: Can every gesture action be performed with a single tap/click? |
| 2.5.2 | **Pointer Cancellation** — Functions triggered by a down-event can be aborted or reversed | A | Manual | P1 | Use up-event (onclick, touchend) not down-event. If you must use down-event, provide: abort by moving pointer away, or undo functionality. Essential activities exempt. **Testing**: Click and hold a button — does it activate on release or press? Can you drag away to cancel? |
| 2.5.3 | **Label in Name** — Visible label text is part of the accessible name | A | Auto + SR | P0 | Accessible name must start with or match visible label text. If button says "Submit", its `aria-label` must include "Submit". **Testing**: With screen reader, does the announced name match or start with what's visually displayed? |
| 2.5.4 | **Motion Actuation** — Functions operated by device motion have UI alternatives | A | Manual | P2 | Shake-to-undo needs a button. Tilt-to-scroll needs scrollbar. **Testing**: Can every motion-activated function be performed with UI controls? |
| 2.5.5 | **Target Size (Minimum)** — Pointer target size is at least 24×24 CSS pixels | AA | Auto + Manual | P1 | Exceptions: inline links, spacing provides equivalent size, target is in a sentence/block, user-agent default, essential presentation. **Testing**: Measure touch targets with browser dev tools. |
| 2.5.6 | **Concurrent Input Mechanisms** — Users can switch between input modalities (mouse, keyboard, touch, stylus, voice) | AAA | Manual | P3 | Do not restrict to a single input type. |
| 2.5.7 | **Dragging Movements** — Dragging has single-pointer alternative | AA | Manual | P1 | Drag-and-drop needs point-and-click alternative. **Testing**: Every drag operation must have a non-drag equivalent. |
| 2.5.8 | **Target Size (Enhanced)** — Target size at least 44×44 CSS pixels | AAA | Auto + Manual | P3 | AAA-level target size. |

---

## Principle 3: Understandable

Information and the operation of the user interface must be understandable.

### 3.1 Readable

Make text content readable and understandable.

| # | Success Criterion | Level | Test Method | Priority | Implementation Guidance |
|---|-------------------|-------|-------------|----------|------------------------|
| 3.1.1 | **Language of Page** — Default human language is programmatically determined | A | Auto | P1 | `<html lang="en">`. Valid BCP 47 language tag. **Testing**: axe-core checks for lang attribute. |
| 3.1.2 | **Language of Parts** — Human language of each passage/phrase is programmatically determined | AA | Auto + Manual | P2 | Use `lang` attribute on elements containing text in a different language. `<blockquote lang="fr">`. Proper names and technical terms in other languages may be exempt. **Testing**: Search for foreign-language content, verify `lang` attribute. |

### 3.2 Predictable

Make Web pages appear and operate in predictable ways.

| # | Success Criterion | Level | Test Method | Priority | Implementation Guidance |
|---|-------------------|-------|-------------|----------|------------------------|
| 3.2.1 | **On Focus** — When a component receives focus, it does not initiate a change of context | A | KB | P1 | Focus must not trigger: form submission, new window, focus change, significant content change. Exceptions: help dialogs triggered by focus. **Testing**: Tab through every element — any unexpected page changes? |
| 3.2.2 | **On Input** — Changing a UI component's setting does not automatically change context unless advised beforehand | A | Manual + KB | P1 | Changing a dropdown/radio must not auto-submit the form or navigate away. Exceptions: a warning was provided; or the change is core behavior (e.g., language selector that changes page language). **Testing**: Change every form control value — any unexpected navigation or submission? |
| 3.2.3 | **Consistent Navigation** — Navigation mechanisms repeated on multiple pages appear in the same relative order | AA | Manual | P2 | Primary nav, breadcrumbs, and footer links must maintain consistent order across pages. **Testing**: Compare navigation order across 5+ pages. |
| 3.2.4 | **Consistent Identification** — Components with same functionality are identified consistently | AA | Manual | P2 | Icons, buttons, and form fields that do the same thing should have the same label. "Search" icon should always be "Search", not alternating with "Find" or "Look up." **Testing**: Audit repeated components for label consistency. |
| 3.2.5 | **Change on Request** — Changes of context are initiated only by user request, or a mechanism is available to turn them off | AAA | Manual | P3 | Auto-refreshing pages need a way to disable auto-refresh. Auto-redirects need user confirmation. |
| 3.2.6 | **Consistent Help** — Help mechanisms are in consistent locations across pages | A | Manual | P2 | Help links, chat widgets, contact info — always in the same relative order. At least one help mechanism within the site. **Testing**: Verify help mechanism location is identical across pages. |

### 3.3 Input Assistance

Help users avoid and correct mistakes.

| # | Success Criterion | Level | Test Method | Priority | Implementation Guidance |
|---|-------------------|-------|-------------|----------|------------------------|
| 3.3.1 | **Error Identification** — When an input error is detected, the error is described in text | A | Manual + SR | P0 | Error messages must be text (not just red border). Associate error with field using `aria-describedby` pointing to error message ID. Error text must describe the problem AND how to fix it. **Testing**: Submit a form with errors — are errors announced by screen reader? Is each error text clear? |
| 3.3.2 | **Labels or Instructions** — Labels or instructions are provided when content requires user input | A | Manual + SR | P0 | Every form field needs a visible label. Required fields marked with text (not just asterisk — or asterisk must be explained at form start). Format expectations must be communicated (e.g., "MM/DD/YYYY"). **Testing**: Review every form — does each field have a label? Are format requirements communicated? |
| 3.3.3 | **Error Suggestion** — When input error is detected, suggestions for correction are provided | AA | Manual | P1 | Beyond just identifying the error — tell the user the correct format or suggest valid values. Exception: would compromise security (password hints). **Testing**: Trigger errors — does each error include a suggestion for how to correct? |
| 3.3.4 | **Error Prevention (Legal, Financial, Data)** — Submissions that cause legal commitments or financial transactions are reversible, checked, or confirmed | AA | Manual | P1 | Checkout, contract signing, data deletion must have: confirmation step, ability to review/edit, or ability to reverse. **Testing**: Does every irreversible action have a confirmation step? |
| 3.3.5 | **Help** — Context-sensitive help is available | AAA | Manual | P3 | Help text, tooltips, or links to documentation next to complex inputs. |
| 3.3.6 | **Error Prevention (All)** — All submissions require confirmation, review, or are reversible | AAA | Manual | P3 | Extends 3.3.4 to ALL form submissions. |
| 3.3.7 | **Accessible Authentication (Minimum)** — Authentication doesn't require cognitive function tests | AA | Manual | P1 | No CAPTCHAs, no puzzle-solving, no memorization or transcription. Alternatives: magic links, OAuth, password managers (autocomplete). Object recognition and personal content are exempt. **Testing**: Can you authenticate without solving a puzzle or remembering/transcribing? |
| 3.3.8 | **Accessible Authentication (No Exception)** — Authentication without all cognitive function tests, no exceptions | AAA | Manual | P3 | Even stronger — no object recognition or personal content tests allowed. |
| 3.3.9 | **Redundant Entry** — Previously entered information is auto-populated or available for selection | A | Manual | P2 | In a multi-step process, previously entered data (same session) must be auto-populated or selectable. Exception: re-entering for security (password), or when essential. **Testing**: In a multi-step form, does step 3 auto-populate data from step 1? |

---

## Principle 4: Robust

Content must be robust enough to be interpreted by a wide variety of user agents, including assistive technologies.

### 4.1 Compatible

Maximize compatibility with current and future user agents, including assistive technologies.

| # | Success Criterion | Level | Test Method | Priority | Implementation Guidance |
|---|-------------------|-------|-------------|----------|------------------------|
| 4.1.1 | **Parsing** — (Deprecated in WCAG 2.2 — removed. Use HTML validator as best practice.) | — | — | — | While formally removed, still good practice: validate HTML with W3C validator. Ensure IDs are unique, elements are closed, attributes use proper syntax. |
| 4.1.2 | **Name, Role, Value** — All UI components have programmatically determined name, role, value, and state | A | Auto + SR | P0 | Native HTML elements have this built-in. Custom widgets (tabs, accordions, sliders) must use ARIA to expose name, role, value, and state changes. Custom checkboxes need `role="checkbox"`, `aria-checked`, and accessible name. **Testing**: Inspect each custom widget with browser accessibility tree. Run axe-core. |
| 4.1.3 | **Status Messages** — Status messages are programmatically determined without receiving focus | AA | Manual + SR | P1 | Dynamic content updates (success toast, search result count, cart update, loading indicator) must use `role="status"`, `role="alert"`, or `aria-live`. Use `aria-live="polite"` for non-urgent updates, `aria-live="assertive"` for critical alerts. **Testing**: Trigger a status update — does screen reader announce it without moving focus? |

---

## Testing Methodology Quick Reference

| Method | Tool | What It Catches | False Positive Rate |
|--------|------|-----------------|---------------------|
| **Automated** | axe-core, Lighthouse, WAVE | ~30-40% of issues: color contrast, missing alt text, missing labels, invalid ARIA, heading structure | Medium — verify all findings manually |
| **Keyboard Only** | Unplug mouse, Tab/Shift+Tab/Enter/Space/Arrows | Focus order, focus visibility, keyboard traps, operability | Low |
| **Screen Reader** | NVDA+Firefox, VoiceOver+Safari, JAWS+Chrome | Name/role/value exposure, reading order, live regions, landmark navigation | Low |
| **Visual Review** | Manual inspection, color filters | Color reliance, content reflow, text spacing, sensory characteristics | Medium |
| **Zoom** | Browser zoom 200%, 400% | Reflow, content loss, text resize | Low |
| **Code Review** | Manual source inspection | Semantic structure, ARIA misuse, autocomplete attributes | Low |

---

## Priority Triage Guide

| Priority | Criteria | Response Timeline |
|----------|----------|-------------------|
| **P0** | Blocks users completely; legal risk; common assistive tech failure | Fix before launch |
| **P1** | Significantly degrades experience; affects many users | Fix within current sprint |
| **P2** | Noticeable but workaround exists; affects some users | Fix within next 2 sprints |
| **P3** | WCAG AAA; enhancement; affects few users | Backlog; address as capacity allows |

---

## WCAG 2.2 New Criteria (Added over 2.1)

The following criteria were added in WCAG 2.2. Ensure these receive extra attention:

- **2.4.11** Focus Not Obscured (Minimum) — AA
- **2.4.12** Focus Not Obscured (Enhanced) — AAA
- **2.4.13** Focus Appearance — AAA
- **2.5.7** Dragging Movements — AA
- **2.5.8** Target Size (Minimum) — AA (updated)
- **3.2.6** Consistent Help — A
- **3.3.7** Accessible Authentication (Minimum) — AA
- **3.3.8** Accessible Authentication (No Exception) — AAA
- **3.3.9** Redundant Entry — A

**Removed in 2.2**: 4.1.1 Parsing (obsolete — handled by HTML spec directly)

---

## References

- WCAG 2.2 Specification: https://www.w3.org/TR/WCAG22/
- Understanding WCAG 2.2: https://www.w3.org/WAI/WCAG22/Understanding/
- How to Meet WCAG 2.2 (Quick Reference): https://www.w3.org/WAI/WCAG22/quickref/
- axe-core Rules: https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md
- WebAIM WCAG Checklist: https://webaim.org/standards/wcag/checklist
