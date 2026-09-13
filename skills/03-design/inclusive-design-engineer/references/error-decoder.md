# Error Decoder — Long Form

<!-- DEEP: 5+min -- the symptom catalogue in long form, with causes and fixes -->

The compressed table lives in `SKILL.md`. This file carries the full diagnosis.

## 1. Screen reader announces a control with no name

**Symptom:** an icon-only control is announced as "button" with nothing further. The user cannot tell what it does.
**Mechanism:** the control has a visual icon but no accessible name. The icon is decorative to the developer and invisible to the AT (R1).
**Diagnosis:** in the platform inspector, read the node's name. Empty means unnamed.

**Fix:** give the control an accessible name via `aria-label` or visually-hidden text, matching the visible label where one exists. Hide decorative icons from AT.
**Recurrence guard:** a guard asserting every interactive element has a non-empty name.

## 2. Dialog opens and the screen reader reads the page behind it

**Symptom:** the user opens a modal and continues to hear the underlying page.
**Mechanism:** a visual overlay does not modify the accessibility tree. `aria-modal` was absent, or present without actual inertness (Decision Tree 2).
**Diagnosis:** open the dialog; attempt to read the page behind it with the AT.

**Fix:** make the background inert with the platform's modal mechanism or explicit inert marking, and move focus into the dialog.
**Recurrence guard:** a guard asserting focus lands inside the overlay on open.

## 3. Focus disappears after a dialog closes

**Symptom:** the user closes an overlay and lands at the top of the page.
**Mechanism:** the invoking element was not stored before opening, so focus fell to the document body (Decision Tree 2).
**Diagnosis:** note the focused element, open an overlay, close it, and observe where focus is.

**Fix:** store the invoker and restore focus on close; if the invoker no longer exists, move focus to a sensible neighbour, never to the body.
**Recurrence guard:** a guard asserting focus position after close.

## 4. The status message is shown but never announced

**Symptom:** "Saved successfully" appears visually and is silent to a screen reader.
**Mechanism:** the live region was created together with its content, so nothing *changed* from the AT's perspective (R4).
**Diagnosis:** inspect whether the region exists in the DOM before the message, or only with it.

**Fix:** render the region empty at the app root; populate it on change; clear then set so repeated messages re-announce.
**Recurrence guard:** a guard asserting the region exists before the update.

## 5. The screen reader never finishes a sentence

**Symptom:** announcements interrupt each other constantly; the interface is unusable with the AT.
**Mechanism:** `assertive` (or `role="alert"`) used for routine messages, causing each to interrupt the previous (R4).
**Diagnosis:** count assertive regions and alerts against the genuinely urgent cases.

**Fix:** `polite` by default; one assertive region reserved for urgent, blocking information.
**Recurrence guard:** a review item requiring a justification per assertive use.

## 6. Autocomplete cannot be navigated

**Symptom:** arrow keys do nothing, or move focus out of the field and stop filtering.
**Mechanism:** a partial combobox pattern — focus moved into the listbox instead of being retained on the input (Decision Tree 2).
**Diagnosis:** type in the field and press Down; observe whether focus leaves the input.

**Fix:** keep focus on the input, reference the active option, and announce the expanded state and the result count.
**Recurrence guard:** a guard asserting focus remains on the input while the list is open.

## 7. Form errors are not heard

**Symptom:** a screen-reader user submits, nothing is announced, and they submit again.
**Mechanism:** the message is visual only — not associated with the field, not marked invalid, not announced (Decision Tree 3).
**Diagnosis:** submit an invalid form with a screen reader and listen.

**Fix:** associate the message, set the invalid state, move focus to an error summary listing the errors, and announce it politely.
**Recurrence guard:** a guard asserting invalid state and message association per validated field.

## 8. Text is unreadable in one theme

**Symptom:** secondary text or a focus ring is illegible in dark mode.
**Mechanism:** one palette for both themes, or a secondary tone lighter than the passing threshold (R6).
**Diagnosis:** compute the ratio for every text/surface pair in both themes.

**Fix:** contrast-safe variants per surface and theme, recorded in the token file.
**Recurrence guard:** the token-level contrast guard, which fails when a pairing drops below threshold.

## 9. A fixed defect returns in a new component

**Symptom:** the same finding appears on a new screen built from the same component.
**Mechanism:** the fix was applied to one instance; the shared source still carries the defect (Phase 7).
**Diagnosis:** locate the fix — in the shared component, or in a screen?

**Fix:** move the fix into the shared component or token, then re-verify its other consumers.
**Recurrence guard:** a structural guard on the shared source.

## 10. Keyboard user lands on a nameless element

**Symptom:** tabbing reaches an element the AT cannot describe.
**Mechanism:** `aria-hidden="true"` on content that remained focusable — removed from the tree but still reachable by keyboard.
**Diagnosis:** grep for `aria-hidden` near focusable markup; confirm with the inspector.

**Fix:** remove `aria-hidden` from focusable content, or remove the content from the tab order properly.
**Recurrence guard:** the structural grep for `aria-hidden` on focusable content.

## 11. No focus indicator at all

**Symptom:** the keyboard user cannot see where they are anywhere in the product.
**Mechanism:** a global `outline: none` in a CSS reset, with no replacement (R3).
**Diagnosis:** the `outline: none` grep, excluding legitimate `:focus-visible` replacements.

**Fix:** a visible indicator using `:focus-visible`, verified on every surface and theme.
**Recurrence guard:** the focus-outline grep in the pipeline.

## 12. Animations cause discomfort and cannot be disabled

**Symptom:** a user with a vestibular disorder cannot use the product; the motion cannot be turned off.
**Mechanism:** `prefers-reduced-motion` is not honoured.
**Diagnosis:** enable the preference and observe whether anything changes.

**Fix:** substitute an instant or opacity change; keep necessary feedback.
**Recurrence guard:** a guard asserting the substitution applies under the preference.

## 13. The framework says accessible; the AT disagrees

**Symptom:** the framework's semantics debug view is green, and the screen reader sees nothing.
**Mechanism:** the framework's semantics bridge maps only partially to the platform's accessibility tree. This is specific to cross-platform frameworks.
**Diagnosis:** inspect the platform's own accessibility tree, not the framework's view.

**Fix:** verify on the platform inspector; add platform-level properties where the bridge is incomplete.
**Recurrence guard:** platform-inspector verification recorded per component.

## 14. Widget is one tab stop too many

**Symptom:** the keyboard user presses Tab repeatedly to pass a single widget.
**Mechanism:** a composite widget implemented as separate tab stops instead of one stop with arrow navigation (roving tabindex).
**Diagnosis:** count the Tab presses required to pass the widget.

**Fix:** one tab stop, arrows inside; adopt the roving tabindex or activedescendant model.
**Recurrence guard:** a keyboard walkthrough item in the checklist.

## 15. A fix is reported complete and reappears next audit

**Symptom:** the finding is marked resolved and appears again in the next cycle.
**Mechanism:** the fix was asserted rather than verified with an AT, on a named platform and browser (R2).
**Diagnosis:** does the record name the AT, platform, browser and observed outcome?

**Fix:** run the verification protocol; mark unverified combinations as unverified.
**Recurrence guard:** the verification record is a completion criterion.

## 16. High-contrast and forced-colours users see a broken interface

**Symptom:** in the user's forced-colours mode, controls lose their boundaries or text becomes invisible.
**Mechanism:** fixed colours that fight the user's palette, and boundaries conveyed only by colour.
**Diagnosis:** enable forced colours / high-contrast mode and complete the primary task.

**Fix:** avoid fixed colours where the user's palette should win; convey boundaries with more than colour.
**Recurrence guard:** forced-colours mode is a recorded test case.

## The triage rule

Four of these symptoms — unnamed controls, non-modal dialogs, silent live regions, and unassociated
errors — account for most accessibility defects found in shipped products, and all four are
detectable in minutes with the platform inspector plus one AT session. Inspect first (fast, cheap),
then verify with the AT (slow, decisive), then guard. In that order.
