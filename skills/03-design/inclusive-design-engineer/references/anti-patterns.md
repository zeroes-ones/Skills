# Anti-Patterns

<!-- STANDARD: 3min -- the implementation anti-pattern catalogue with detection heuristics -->

## 1. ARIA as a substitute for behaviour

**Symptom:** a widget announces a role it cannot honour — a `div` with `role="button"` that no key activates.
**Cause:** the role was added to satisfy an audit item (R1).
**Detection:**

```bash
grep -rnE '<(div|span)[^>]*role="(button|checkbox|link|tab|menuitem)"' src/
```

**Fix:** the native element, or the full behaviour the role promises.

## 2. The partial widget pattern

**Symptom:** a dialog that does not contain focus; a combobox with no arrow keys.
**Cause:** the pattern was implemented visually, not contractually (R5).
**Detection:** name each part of the pattern's contract and find its implementation. Any gap is the defect.

**Fix:** implement the contract fully, or ship a simpler correct component.

## 3. Focus ring removal

**Symptom:** keyboard users cannot see where they are.
**Cause:** `outline: none` for aesthetic reasons (R3).
**Detection:**

```bash
grep -rn 'outline:\s*\(none\|0\)' src/ | grep -v -E 'focus-visible|focus-within'
```

**Fix:** a visible indicator on every surface, using `:focus-visible`.

## 4. Focus lost after an overlay closes

**Symptom:** the user is dropped at the document body and must navigate from the top.
**Cause:** the invoking element was not stored and restored.
**Detection:** open an overlay, close it, observe where focus is.

**Fix:** store the invoker; restore on close.

## 5. Modal that is modal only to the mouse

**Symptom:** the screen reader reads the page behind the dialog; the keyboard tabs into it.
**Cause:** a visual overlay with no inertness (Decision Tree 2).
**Detection:** open the dialog, then attempt to tab and to read behind it.

**Fix:** make the background inert — the platform modal mechanism, or explicit inert marking.

## 6. Live region created with its content

**Symptom:** the status message is shown and never announced.
**Cause:** the region and its content render together (R4).
**Detection:**

```bash
grep -rn 'aria-live' src/
# then check whether the region is rendered empty and populated later
```

**Fix:** the region exists first; the update changes its content.

## 7. Assertive by default

**Symptom:** the screen reader never finishes a sentence; the interface is exhausting.
**Cause:** `assertive` (or `role="alert"`) used for routine messages.
**Detection:** count `assertive` and `role="alert"` occurrences against the genuinely urgent cases.

**Fix:** `polite` by default; justify each `assertive`.

## 8. Placeholder as the label

**Symptom:** the field's meaning disappears the moment the user types.
**Cause:** the placeholder was used to save space.
**Detection:** does the field have a real `label`/`for` association?

**Fix:** a persistent, associated label.

## 9. Error not associated with its field

**Symptom:** a screen-reader user cannot tell which field failed or why.
**Cause:** the message is adjacent visually but not programmatically.
**Detection:**

```bash
grep -rn 'aria-invalid\|aria-describedby' src/ | wc -l   # versus the number of validated fields
```

**Fix:** `aria-invalid` plus `aria-describedby` pointing at the message.

## 10. Colour-only meaning

**Symptom:** errors and statuses are invisible to users who cannot perceive the colour.
**Cause:** colour was the only affordance.
**Detection:** render the interface in greyscale; is any meaning lost?

**Fix:** add text, an icon or a shape.

## 11. Contrast fixed per component

**Symptom:** the same contrast failure reappears in each new component.
**Cause:** the fix was applied at the component level, not the token level (R6).
**Detection:** do contrast-safe variants exist per surface in the token file?

**Fix:** contrast-safe tokens, with the ratios recorded.

## 12. Focus indicator invisible on one theme

**Symptom:** focus is visible in light mode and invisible in dark mode.
**Cause:** one indicator colour for all surfaces.
**Detection:** focus an element on each theme and each surface colour.

**Fix:** an indicator verified against both the component and the page, per theme.

## 13. `aria-hidden` on focusable content

**Symptom:** a keyboard user lands on an element with no name and no role.
**Cause:** `aria-hidden` used to hide something visually that remained focusable.
**Detection:**

```bash
grep -rn 'aria-hidden="true"' src/ | grep -iE 'button|link|input|tabindex'
```

**Fix:** never `aria-hidden` on focusable content; hide it properly or remove it from the tab order.

## 14. Keyboard trap

**Symptom:** the user cannot leave a region without a pointer.
**Cause:** Tab prevented, or focus containment without an exit.
**Detection:** tab into every composite widget and confirm you can leave.

**Fix:** never prevent Tab outside a modality with an explicit exit; provide Escape.

## 15. Per-instance fix

**Symptom:** the defect returns in the next screen built from the same component.
**Cause:** the fix was applied to the reported screen, not the source (Phase 7).
**Detection:** locate the fix — is it in the shared component, or in one screen?

**Fix:** fix the shared source, then re-verify its other consumers.

## 16. Unguarded fix

**Symptom:** the defect returns after a refactor.
**Cause:** no regression guard, or a guard that asserts an implementation detail.
**Detection:** revert the fix in a scratch branch — does any test fail?

**Fix:** an outcome-asserting guard, demonstrated to fail.

## 17. Unverified fix reported as complete

**Symptom:** the same finding reappears in the next audit.
**Cause:** the fix was asserted rather than observed with an AT (R2).
**Detection:** does the record name the AT, platform and browser?

**Fix:** the verification protocol, or report the fix as unverified.

## 18. Framework semantics mistaken for the platform tree

**Symptom:** the framework's debug view is green; the screen reader sees nothing.
**Cause:** the framework's semantics bridge maps only partially (platform-accessibility context).
**Detection:** inspect the platform's own accessibility tree, not the framework's view.

**Fix:** verify on the platform inspector and with the platform's AT.

## Detection sweep

```bash
SRC="${1:-src}"

echo "== click handlers on non-interactive elements (R1) =="
grep -rnE '<(div|span)[^>]*onClick' "$SRC" 2>/dev/null | head || echo "  none"

echo "== redundant role on semantic elements (R1) =="
grep -rnE '<(button|a|input|select|textarea)[^>]*role=' "$SRC" 2>/dev/null | head || echo "  none"

echo "== focus outline removed (R3) =="
grep -rn 'outline:\s*\(none\|0\)' "$SRC" 2>/dev/null | grep -v -E 'focus-visible|focus-within' || echo "  none"

echo "== aria-hidden on possibly focusable content =="
grep -rn 'aria-hidden="true"' "$SRC" 2>/dev/null | grep -iE 'button|link|input|tabindex' || echo "  none"

echo "== live regions (check each is populated after render) =="
grep -rn 'aria-live\|role="status"\|role="alert"' "$SRC" 2>/dev/null | wc -l | xargs echo "  count:"

echo "== error association (should be > 0 wherever validation exists) =="
grep -rn 'aria-invalid\|aria-describedby' "$SRC" 2>/dev/null | wc -l | xargs echo "  count:"

echo "== reduced-motion handling (R-preferences) =="
grep -rn 'prefers-reduced-motion' "$SRC" 2>/dev/null | wc -l | xargs echo "  count:"

echo "== positive tabindex (breaks natural order) =="
grep -rn 'tabindex="[1-9]' "$SRC" 2>/dev/null || echo "  none"

echo "== placeholder used as a label =="
grep -rn 'placeholder=' "$SRC" 2>/dev/null | wc -l | xargs echo "  count (verify each has a real label):"
```

Interpretation: a non-zero first, second, third or fourth block is a near-certain finding. A zero
reduced-motion count alongside any animation is a comfort defect. A zero error-association count
alongside validated fields means errors are visual-only.
