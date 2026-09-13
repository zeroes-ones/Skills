# Anti-Patterns

<!-- STANDARD: 3min -- platform anti-patterns with detection heuristics -->

## 1. The universally identical app

**Symptom:** navigation, controls and gestures are the same on every platform; users on one
platform report the app "feels foreign".
**Cause:** consistency was defined as visual sameness rather than convention conformance.
**Detection:** one navigation implementation, no platform conditionals in the UI layer.

```bash
# Expect per-platform UI divergence; its total absence is the signal
grep -rn "Platform.OS\|isIOS\|android\b" src/ --include=*.ts --include=*.tsx | wc -l
```

**Fix:** build the convention matrix, then fork navigation, gestures and controls (R1).

## 2. The stretched phone

**Symptom:** a tablet or desktop layout that is the phone layout with more whitespace; breaks in
split view.
**Cause:** breakpoints keyed to device names rather than available size (R2).
**Detection:** device-name breakpoints; no size-class handling; no split-view test.

```bash
grep -rnE "iPad|tablet|768|1024" src/ | grep -v "size-class\|sizeClass"
```

**Fix:** design per size class; verify at the smallest multitasking size.

## 3. Touch-only assumptions

**Symptom:** keyboard, pointer, remote and gaze users cannot complete the primary task.
**Cause:** touch was the only modality tested (R4).
**Detection:** no focus management, hover states carrying information, no shortcut definitions.

```bash
grep -rn "tabIndex\|onKeyDown\|focus-visible\|:focus" src/ | wc -l   # zero is the signal
```

**Fix:** enumerate modalities; define focus order and visibility; add shortcuts.

## 4. The reimplemented system affordance

**Symptom:** a custom permission prompt, share sheet or confirmation that behaves subtly
differently; occasionally a platform review rejection.
**Cause:** the system affordance was treated as a styling opportunity.
**Detection:** custom UI in the flow where a system dialogue is expected.

**Fix:** restore the system affordance. It brings behaviour, accessibility and review approval.

## 5. Invisible focus on a non-touch surface

**Symptom:** on TV or desktop, the user cannot tell where they are.
**Cause:** focus was never designed because the design tool has no focus state.
**Detection:** no focus indicator in the design; no focus order diagram.

**Fix:** a persistent, high-contrast focus indicator; a deliberate, tested focus order.

## 6. Gesture-only function

**Symptom:** a function reachable only by a multipoint or path-based gesture.
**Cause:** gestures designed as a shortcut without an alternative path.
**Detection:** a feature whose only entry point is a gesture.

**Fix:** add a single-pointer, non-path alternative (WCAG 2.5.1). The gesture may remain as an
addition.

## 7. Silent text-size ignorance

**Symptom:** the app ignores the platform's text-size setting.
**Cause:** a custom font applied without scaling plumbing (R5).
**Detection:** fixed text sizes; no dynamic-type or text-scaling participation.

```bash
grep -rn "fontSize" src/ | grep -vE "scale|PixelRatio|sp\b" | head
```

**Fix:** platform text styles, or reproduce the scaling; verify at the maximum setting.

## 8. Framework defaults presented as conformance

**Symptom:** a self-drawn widget set shipped to a platform-targeted app, described as native.
**Cause:** the framework's default was treated as the platform's convention.
**Detection:** no platform component library; no record of the trade.

**Fix:** adopt platform components, or record the trade as a trade (R3, Decision Tree 2).

## 9. The unrecorded deviation

**Symptom:** reviewers flag "bugs" that are deliberate, or preserve real bugs believing they were
deliberate.
**Cause:** no deviation log (R3).
**Detection:** behavioural departures with no corresponding log entry.

**Fix:** the deviation log, reviewed each release.

## 10. The crammed reduced surface

**Symptom:** a watch app showing a dashboard; a TV app with small text.
**Cause:** phone information density moved to a surface with a different attention budget (R2).
**Detection:** a reduced-surface screen with more than one task, or dense text.

**Fix:** one task per screen; escalate detail to a richer surface (Decision Tree 4).

## 11. Locked orientation as an adaptation substitute

**Symptom:** the app locks landscape/portrait to avoid handling the other.
**Cause:** adaptation treated as optional.
**Detection:** orientation lock in the manifest/plist.

**Fix:** design both orientations; a lock prevents side-by-side use on tablets.

## 12. Broken deep-link back stack

**Symptom:** a deep link opens a screen and back exits the app.
**Cause:** only the leaf of the link was resolved, not the parent hierarchy.
**Detection:** deep link into a nested screen and press back.

**Fix:** reconstruct the parent stack from the link; never disable back.

## 13. Hover-dependent information

**Symptom:** information revealed only on hover, unavailable to touch users.
**Cause:** a pointer-centric design shared with a touch surface.
**Detection:** tooltips or reveals with no touch/click equivalent.

**Fix:** hover is an enhancement; the information must be reachable without it.

## Detection sweep

```bash
SRC="${1:-src}"

echo "== device-name breakpoints (R2) =="
grep -rnE "iPad|tablet|768px|1024px" "$SRC" 2>/dev/null | grep -v "size-class" || echo "  none"

echo "== missing platform divergence (R1) =="
n=$(grep -rn "Platform.OS\|isIOS\|isAndroid" "$SRC" 2>/dev/null | wc -l | tr -d ' ')
[ "$n" -eq 0 ] && echo "  WARNING: no platform-conditional UI found in a multi-platform app"

echo "== focus handling (R4) =="
f=$(grep -rn "focus-visible\|onKeyDown\|tabIndex" "$SRC" 2>/dev/null | wc -l | tr -d ' ')
[ "$f" -eq 0 ] && echo "  WARNING: no focus handling found"

echo "== orientation lock =="
grep -rn "orientation" *.json *.plist android/app/src/main/AndroidManifest.xml 2>/dev/null \
  | grep -iE "lock|portrait|landscape" || echo "  none"

echo "== deviation log present (R3) =="
find . -iname "*deviation*" -not -path "./node_modules/*" 2>/dev/null | head -3 \
  || echo "  none found"
```

Every warning above is a convention question that has not been answered. The sweep takes
seconds; the rework it prevents is measured in weeks.
