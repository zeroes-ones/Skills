# Anti-Patterns

<!-- STANDARD: 3min -- the interaction anti-pattern catalogue with detection heuristics -->

## 1. Taste-as-evidence review

**Symptom:** design review feedback is entirely adjectives — "cluttered", "needs polish", "feels off".
**Cause:** no shared bar, so opinion substitutes for criteria.
**Detection:** count findings with a reproduction step in the review thread. Zero is the signal.

**Fix:** convert to evidence — screen, step, observed behaviour, consequence (R1).

## 2. Success-path-only screens

**Symptom:** blank screens, undefined empties, unnamed errors in support tickets.
**Cause:** only the ideal state was designed (R2).
**Detection:** disconnect the network and load the screen; inspect the empty state as a new user.

**Fix:** enumerate every state per async screen; treat coverage as a gate (Decision Tree 2).

## 3. "No data" empty states

**Symptom:** the first-run experience is a dead screen reading "No data".
**Cause:** the empty state was treated as a placeholder, not as onboarding.
**Detection:** create a new account and visit every surface.

**Fix:** name the concrete noun, state the purpose, offer one primary action (empty-states.md).

## 4. Errors without a remedy

**Symptom:** users cannot complete the task after a failure; support tickets say "unhelpful error".
**Cause:** the message names the system's condition and stops.
**Detection:** every error string in the product, checked for a next action.

**Fix:** name, remedy, preserve — all three (error-experience.md).

## 5. Central indeterminate spinner for everything

**Symptom:** a spinner in the middle of the screen for a multi-second operation, replacing content.
**Cause:** the weakest perceived-performance technique applied uniformly (R4).
**Detection:** every spinner and its operation's plausible duration.

**Fix:** match the technique to the duration band; preserve context (Decision Tree 4).

## 6. Skeleton with the wrong shape

**Symptom:** content jumps when data arrives — the reflow the skeleton should have prevented.
**Cause:** the skeleton was drawn as generic bars, not from the final layout.
**Detection:** throttle and watch whether the layout shifts on arrival.

**Fix:** derive the skeleton from the real final layout.

## 7. Motion that outlasts its cause

**Symptom:** users tap twice because the interface feels slow on a fast operation.
**Cause:** a transition longer than the interaction it accompanies (R3).
**Detection:** time the transitions against the actions they accompany.

**Fix:** shorten below the interaction; animate only context changes.

## 8. Decorative motion in the primary path

**Symptom:** polish added to the most frequent action; the product feels sluggish in daily use.
**Cause:** delight optimised for a demo, not for the thousandth use.
**Detection:** animation present on the most-repeated interactions.

**Fix:** reserve motion for context changes; keep feedback immediate.

## 9. Competing primary actions

**Symptom:** three equally-weighted buttons; users hesitate or tap the wrong one.
**Cause:** decisions were added rather than defaulted.
**Detection:** count the equally-weighted actions at each task step.

**Fix:** one primary per screen per step; default and disclose the rest (cognitive-load.md).

## 10. Validation on submit only

**Symptom:** users complete a long form and are rejected at the end.
**Cause:** validation timing chosen by implementation convenience.
**Detection:** fill a field with a format error and leave it — does anything happen?

**Fix:** validate on blur, at the moment the fix is possible (forms-and-feedback.md).

## 11. Placeholder-as-label

**Symptom:** the field's meaning disappears the moment the user starts typing.
**Cause:** the placeholder was used to save vertical space.
**Detection:** does the label vanish on input?

**Fix:** a persistent label, always.

## 12. The disabled submit button

**Symptom:** a greyed-out submit with no indication of what is missing.
**Cause:** the button was disabled instead of informing.
**Detection:** is the submit disabled, and does the UI say why?

**Fix:** keep it enabled and reveal the first error; prevent double submission with an in-flight state.

## 13. Irreversible action adjacent to a frequent one

**Symptom:** accidental deletion or an irreversible change.
**Cause:** no spatial separation, confirmation, or undo (Decision Tree 1).
**Detection:** measure the distance and adjacency between destructive and routine controls.

**Fix:** separate, confirm with the specific consequence, or offer undo.

## 14. Un-legible long operation

**Symptom:** the screen appears frozen for tens of seconds; users reload or abandon.
**Cause:** no progress signal, and no way to leave (R4).
**Detection:** run the operation on a slow network and observe.

**Fix:** determinate progress with stages, plus the ability to leave.

## 15. Immortal findings

**Symptom:** the same five findings recur every quarter with new wording.
**Cause:** no metric, no owner, no review date (R5).
**Detection:** compare this quarter's findings with the previous two quarters'.

**Fix:** every fix gets a metric, an owner and a review date; report a trend, not a snapshot.

## 16. Improvement claimed without a baseline

**Symptom:** "it's better now" after a redesign, with no number.
**Cause:** no baseline captured before the change (R5).
**Detection:** is there a pre-change measurement of the metric being claimed?

**Fix:** capture the baseline first, or label the claim as a hypothesis.

## 17. Verified only on the designer's machine

**Symptom:** perceived slowness and layout breakage reported by users, invisible in review.
**Cause:** verification on a fast device with a warm cache.
**Detection:** re-run the review on a throttled representative device.

**Fix:** verify on the median device and network.

## 18. Colour-only error indication

**Symptom:** users do not see the error; screen-reader users re-submit the same failing form.
**Cause:** the error was communicated visually by colour alone.
**Detection:** is there text and an icon, and is the message announced?

**Fix:** text plus icon, associated programmatically and announced.

## Detection sweep

```bash
SRC="${1:-src}"

echo "== 'No data' style empty states =="
grep -rniE '"(no data|no results|nothing here|empty)"' "$SRC" 2>/dev/null | head || echo "  none"

echo "== generic error strings with no remedy =="
grep -rniE '"(something went wrong|error occurred|invalid input|an error)"' "$SRC" 2>/dev/null | head || echo "  none"

echo "== transitions present (check durations against interactions) =="
grep -rnE 'transition:|animate' "$SRC" 2>/dev/null | wc -l | xargs echo "  count:"

echo "== reduced-motion handling =="
grep -rn "prefers-reduced-motion" "$SRC" 2>/dev/null | wc -l | xargs echo "  count:"

echo "== skeleton / loading states =="
grep -rniE 'skeleton|loading|shimmer' "$SRC" 2>/dev/null | wc -l | xargs echo "  count:"

echo "== error association for assistive tech =="
grep -rnE 'aria-invalid|aria-describedby|role="alert"|role=.alert' "$SRC" 2>/dev/null | wc -l | xargs echo "  count:"

echo "== placeholder used as a label =="
grep -rnE 'placeholder=' "$SRC" 2>/dev/null | wc -l | xargs echo "  placeholder count (check each has a real label):"
```

Interpretation: a non-zero "No data" count and a zero reduced-motion count are near-certain
findings. A high transition count with no reduced-motion handling is a comfort defect. A zero
skeleton count alongside a spinner count means the perceived-performance technique is uniformly
the weakest one.
