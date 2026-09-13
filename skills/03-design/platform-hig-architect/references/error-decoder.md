# Error Decoder — Long Form

<!-- DEEP: 5+min -- the symptom catalogue in long form, with causes and fixes -->

The compressed table lives in `SKILL.md`. This file carries the full diagnosis.

## 1. Users miss the back affordance on one platform

**Symptom:** analytics or session recordings show users stuck on inner screens; on one platform
specifically. Support hears "I can't get out of the settings page".
**Mechanism:** a phone navigation model was ported to a platform whose back convention differs —
either a back control where a gesture is expected, or a gesture where the system back should
operate.
**Diagnosis:** perform the platform's own back action from three depths and observe.

```text
Depth 1 → does it return to the parent?
Depth 2 → does it walk the stack, or jump to root?
Depth 3 → does it exit the app from an inner screen (Android interception gap)?
```

**Fix:** adopt the platform's back behaviour per screen, and handle the full history rather than
the top of the stack.
**Recurrence guard:** the conformance audit's navigation dimension is scored from a recording,
not from the design (CR7).

## 2. The tablet layout breaks in split view

**Symptom:** the app is fine full-screen on a tablet, and visibly broken when another app shares
the screen. Elements overlap; a region collapses to nothing.
**Mechanism:** the layout was designed at a device width, not to the available size. Split view
produces a *narrower* region than a phone in landscape — the case never designed (R2).
**Diagnosis:** put the app in the smallest split the platform allows and screenshot.

**Fix:** design against size classes and verify at the smallest multitasking size; add
container-query handling so components respond to their own region, not the window.
**Recurrence guard:** split-view verification is a checklist item, not an afterthought (CR6).

## 3. The TV app is unusable with a remote

**Symptom:** focus is invisible or jumps unpredictably; some screens cannot be exited; the user
gives up.
**Mechanism:** touch and hover assumptions carried to a remote-driven surface, where focus *is*
the pointer. Without a spatial focus model, traversal is arbitrary (Decision Tree 4).
**Diagnosis:** navigate the whole app with only the directional pad, logging focus position.

**Fix:** a persistent, high-contrast focus indicator; a focus graph matching the layout's
geometry; explicit focus entry points; no traps.
**Recurrence guard:** every TV screen is navigable with the remote alone before it is accepted.

## 4. Platform review rejects the build

**Symptom:** a release is blocked by platform review, usually citing convention or system
integration issues.
**Mechanism:** a system affordance was reimplemented (a permission prompt or share sheet), or a
core navigation convention was overridden without justification.
**Diagnosis:** compare each system-integration flow to the platform's own behaviour.

**Fix:** restore system affordances; record any remaining deviation with its rationale — review
teams generally accept a justified deviation and reject an unexplained one.
**Recurrence guard:** the system-affordance check in Verification is a release gate.

## 5. Text ignores the platform's size setting

**Symptom:** a user raises the system text size and the app's text does not change, or changes
and clips.
**Mechanism:** a custom font applied without scaling plumbing; the platform's text style carries
the user's preference and the custom face does not (R5).
**Diagnosis:** set the platform text size to its maximum and inspect.

**Fix:** use the platform's text styles, or reproduce the scaling; then verify the layout at the
maximum size, which is where clipping appears.
**Recurrence guard:** resize verification at the maximum setting per surface (CR11).

## 6. The watch app is unused after the first day

**Symptom:** the wearable app ships; engagement collapses. Users describe it as "too much".
**Mechanism:** phone information density moved to a glance surface. The attention budget, not the
screen size, was the constraint (R2, Decision Tree 4).
**Diagnosis:** count the tasks per screen and the navigation depth.

```text
1 task per screen  → correct
>1 task per screen → crammed
depth > 2          → the hierarchy must flatten
```

**Fix:** one task per screen; escalate detail to the phone; the watch signals, the phone does the
work.
**Recurrence guard:** the reduced-surface checklist gates every wearable screen (CR14).

## 7. Keyboard and pointer users cannot complete the task

**Symptom:** a keyboard user tabs into the app and cannot reach the primary action, or focus
disappears entirely.
**Mechanism:** focus order undefined and the focus indicator removed or never styled (R4).
**Diagnosis:** unplug the pointer; complete the primary task with the keyboard alone.

**Fix:** define focus order explicitly; make focus visible at the platform's expected strength;
restore focus after overlays close.
**Recurrence guard:** the input-modality pass is a checklist item (CR8, CR9).

## 8. The Android build uses iOS navigation (or vice versa)

**Symptom:** after a framework upgrade, one platform's build adopts another platform's
navigation or controls.
**Mechanism:** the framework's default widget set was relied upon, and the default is one
platform's convention (or the framework's own) rather than each platform's (Decision Tree 2).
**Diagnosis:** compare navigation structure and control behaviour per platform build.

**Fix:** adopt per-platform component libraries, or record the shared-UI trade explicitly.
**Recurrence guard:** the fidelity audit runs per platform before release.

## 9. The app "feels foreign"

**Symptom:** reviews and retention indicate the app is disliked without a specific defect being
found; a common phrasing is "it doesn't feel like an app".
**Mechanism:** brand applied uniformly with no convention mapping — every surface identical, so
no surface feels native (R1, R3).
**Diagnosis:** walk the app on each platform and ask, per element, "what would this platform do?"
Count the mismatches.

**Fix:** build the convention matrix; take the platform's behaviour and express brand in the
surface.
**Recurrence guard:** the matrix is reviewed as one artefact, so cross-platform conflicts are
visible (CR2).

## 10. Deep link opens a dead end

**Symptom:** a link into a nested screen leaves back exiting the app.
**Mechanism:** only the link's leaf was resolved; the parent hierarchy was not reconstructed.
**Diagnosis:** open a deep link to a three-level screen and press back.

**Fix:** reconstruct the parent stack from the link; never disable back to hide the symptom.
**Recurrence guard:** deep-link verification is part of the navigation checklist (CR7).

## 11. Hover-only information is invisible on touch

**Symptom:** touch users never see information that pointer users get on hover.
**Mechanism:** a pointer-centric design shared across input modalities (R4).
**Diagnosis:** enumerate every hover/tooltip affordance and check for a non-hover path.

**Fix:** hover is an enhancement; make the information reachable by tap or permanently visible.
**Recurrence guard:** the input pass explicitly checks that hover carries nothing required.

## 12. Workspace arrangement resets every session

**Symptom:** on desktop or spatial surfaces, the user's window/workspace arrangement is lost on
restart.
**Mechanism:** state restoration covers content but not layout — position, size, arrangement.
**Diagnosis:** arrange windows, restart, observe.

**Fix:** persist and restore the arrangement; multi-window and spatial placement are conventions,
not extras.
**Recurrence guard:** state restoration is part of the desktop and spatial checklists.

## The triage rule

Four of these symptoms — wrong back, split-view breakage, invisible focus, and text-size
ignorance — are detectable in minutes with a device or a keyboard, and they account for most
platform-conformance defects reported in the wild. Run the conformance audit's navigation, form
factor, input and typography dimensions first; escalate to the deeper diagnosis above only when
those are clean.
