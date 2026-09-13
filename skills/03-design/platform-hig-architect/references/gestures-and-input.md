# Gestures and Input

<!-- STANDARD: 3min -- gesture grammar and input-modality expectations -->

> **Verification note.** Gesture semantics can change with platform releases (predictive back is
> a recent example). Confirm specific gesture APIs against the targeted SDK's current
> documentation before implementing.

## Gestures are the platform's grammar

A gesture is not a shortcut; it is a word in a language the user already speaks. Swipe-from-edge
means back on one platform and a drawer on another. Swipe-on-a-row means delete in one context
and archive in another. Pull-down means refresh in one place and reveal in another.

The consequences:

- **Reassigning a gesture is a dialect.** The user must learn it, and they will get it wrong
  first. Justify it and record it (R3).
- **A gesture must not be the only path to a function.** Gesture-only interactions exclude
  users who cannot perform them and are unreachable by keyboard, remote or assistive input. If
  a function is only reachable by a gesture, it is inaccessible (R4, and WCAG 2.5.1).
- **The same gesture may carry different meanings per surface**, and that is correct — the
  platforms differ.

## The gesture vocabulary

| Gesture | Common meaning | Notes |
|---|---|---|
| Swipe from edge | Back (one platform), drawer (another) | Platform-governed; do not reassign casually |
| Swipe on a row/item | Delete, archive, reveal actions | Must be accompanied by a non-gesture path |
| Long press | Context menu, selection, drag initiation | Universal; meaning varies by context |
| Pinch | Zoom | Should also be reachable by controls or keyboard |
| Drag | Reorder, move, share | Needs a keyboard/assistive equivalent |
| Pull to refresh | Refresh content | Convention-specific; not universal |
| Double tap | Zoom, like, focus | Meaning is app-specific; keep it discoverable |
| Rotate/dial | Scroll, zoom, adjust (wearables) | Primary input on watch and some wearables |

## The accessibility constraint on every gesture

WCAG 2.5.1 requires that any function operated by a multipoint or path-based gesture is also
operable with a single pointer without a path — unless the gesture is essential. Practical
implications:

| Gesture | Required alternative |
|---|---|
| Swipe to delete | A delete action in a context menu, edit mode, or an explicit control |
| Pinch to zoom | Zoom controls, or keyboard zoom |
| Drag to reorder | Move commands, or a reorder mode with buttons |
| Path/drawing gesture | A non-path equivalent, unless the path *is* the function |

This is the single most-skipped rule in gesture-heavy interfaces, and it is a conformance
failure, not a preference.

## Input modalities by surface

Enumerating the modalities is R4. The table is the working list.

| Surface | Modalities to support | Often forgotten |
|---|---|---|
| Phone | Touch, assistive touch, voice control, switch | Screen-reader gesture set, switch access |
| Tablet | Touch, pointer, hardware keyboard, stylus | Pointer hover states, keyboard shortcuts, stylus pressure |
| Foldable | Touch, pointer, keyboard; resizing | Layout across a runtime size change |
| Desktop | Pointer, keyboard, trackpad gestures | Full keyboard coverage, context menus, focus visibility |
| Web | Pointer, keyboard, screen reader | Keyboard nav of custom widgets, focus order |
| TV | Remote/directional pad, gamepad, voice | Focus order and a persistent focus indicator |
| Watch | Dial/crown, swipe, voice, taps | Dial as a scroll/zoom mechanism |
| Spatial | Gaze, hand gesture, voice | Gaze as a pointer; comfort and dwell behaviour |

## Focus is the navigation on non-touch surfaces

On TV, desktop and any keyboard-driven surface, there is no touch target — **focus is the
pointer**. That makes three properties mandatory:

1. **A visible focus indicator, always.** Invisible focus is not a compromise; it is the
   equivalent of hiding the cursor.
2. **A deterministic focus order.** The order must be predictable from the layout, and must not
   jump between regions or trap.
3. **Focus restoration.** When a modal, sheet or overlay closes, focus returns to the element
   that opened it — not to the top of the document.

```text
Focus order quality test:
  1. Start at the first interactive element.
  2. Advance through the whole screen without a pointer.
  3. Every element reachable? Every element's purpose visible when focused?
  4. Can you complete the primary task?
  5. Close any overlay — does focus return where it came from?
```

If step 3 or 5 fails, the surface is broken for every keyboard, remote and assistive-input user.

## Spatial focus (TV) specifics

The TV focus model is spatial, not linear, and it is the most common TV defect.

| Requirement | Why | Failure symptom |
|---|---|---|
| A persistent, high-contrast focus indicator | On a 10-foot display, a subtle indicator is invisible | The user does not know where they are |
| A planar focus graph, or explicit anchors | Focus that jumps between regions disorients | Unpredictable traversal |
| No focus traps | Users get stuck with no way out | Dead-end screens |
| Focus anchored to content changes | When content loads, focus must not move silently | Focus lands on the wrong element after a load |
| A visible scroll/focus relationship | Focus moving off-screen must scroll predictably | Focus disappears below the fold |

The design rule that prevents most of these: **make the layout's spatial structure match the
focus graph.** A grid focuses as a grid; a rail focuses as a rail. When they disagree, focus
feels arbitrary.

## Stylus and pointer specifics

| Input | Conventions to honour |
|---|---|
| Stylus | Pressure/tilt support where the task benefits; palm rejection; hover preview |
| Pointer | Hover states (non-essential enhancement only), cursor changes for affordance, right-click/context menu, drag and drop |
| Trackpad | Two-finger scroll, pinch zoom; do not hijack system gestures |

Two rules:

- **Hover must never carry required information.** A pointer user may hover, but a touch user
  cannot; anything revealed only on hover is unavailable to half the audience. Hover is an
  enhancement.
- **Do not hijack system gestures.** Overriding trackpad or system-level gestures causes
  surprising behaviour outside the app.

## The input checklist

- [ ] Every supported modality is enumerated for the surface (R4)
- [ ] Each modality can complete the primary task
- [ ] Every gesture has a non-gesture, single-pointer alternative, or is declared essential (2.5.1)
- [ ] Focus order is deterministic and tested without a pointer
- [ ] Focus indicator is visible at the platform's expected strength
- [ ] Focus is restored after overlays and modals close
- [ ] No focus traps; every region is escapable
- [ ] Hover carries no required information
- [ ] System gestures are not hijacked
- [ ] Assistive input (switch, voice, screen reader) can complete the primary task
