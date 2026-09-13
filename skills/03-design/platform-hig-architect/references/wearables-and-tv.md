# Wearables and TV

<!-- STANDARD: 3min -- reduced surfaces, attention budgets and focus models -->

> **Verification note.** Wearable and TV platform guidance changes with each release. Confirm
> specific dimension and control guidance against the targeted SDK's documentation.

## Why reduced surfaces are a different problem

A watch and a TV are not small and large phones. They are different *contexts*:

| Surface | Physical situation | Attention budget | Input | Typical duration |
|---|---|---|---|---|
| Watch | On the wrist, often mid-activity | **Seconds** | Dial, swipe, voice, taps | A glance to a few seconds |
| TV | Across the room, lean-back | Minutes, but low intensity | Remote, gamepad, voice | A session |
| Phone | In hand | Minutes | Touch, keyboard | A session |
| Headset | Worn, immersed | Minutes, high intensity | Gaze, hands, voice | A session |

The attention budget, not the screen size, is the design constraint. A watch screen with a
phone's information density is unusable at any size (R2, Decision Tree 4).

## Wearables

### The rules for a wearable

1. **One task per screen.** Not one *idea* — one *task*. A glance surface shows a single answer
   and perhaps a single action.
2. **No deep hierarchy.** One or two levels maximum. A three-level hierarchy on a watch is a
   design failure, not a limitation to work around.
3. **Escalate detail to the phone.** The watch surfaces *the alert or the answer*; the phone
   handles the manipulation. Handing off is the correct design, not a cop-out.
4. **No dense tables or long forms.** A form on a watch should be a single confirmation, not
   data entry.
5. **Design for the input set.** Dial/crown for scroll and precise adjustment, swipe for
   navigation, voice for entry, taps for selection.

### What fits on a watch

| Fits | Does not fit |
|---|---|
| A current metric with a trend | A dashboard of metrics |
| One notification with one action | A notification centre with management |
| A single confirmation | A multi-field form |
| A complication/glance | A multi-step workflow |
| A short timer or control | A settings screen with many options |

### The handoff pattern

```text
Watch shows:  "Order #4412 shipped"  + [Track]
                                     [Open on phone]
Phone shows:  full order detail, tracking map, change address, contact support
```

The watch is the *signal*; the phone is the *workbench*. Designing the watch as a compressed
phone produces an interface nobody uses twice.

## TV

### The rules for TV

1. **Focus is the navigation.** There is no pointer. The focus indicator *is* the cursor, and it
   must be persistent, high-contrast and always visible from 10 feet.
2. **The focus graph should match the layout's geometry.** A grid focuses as a grid. When the
   focus graph and the visual structure disagree, traversal feels arbitrary.
3. **No focus traps, no dead ends.** Every screen must be escapable with the remote.
4. **Ten-foot legibility.** Type is larger, contrast is higher, and spacing is more generous
   than on any other surface. A design that is legible on a monitor will not be legible on a TV.
5. **Restrained motion.** Transitions are slower and less frequent; motion reads as instability
   at a distance.
6. **No hover, no small targets, no dense text.** Each of these has no TV equivalent.

### The TV focus model

| Requirement | Failure if absent |
|---|---|
| Persistent, high-contrast focus indicator | The user loses their place; navigation becomes guesswork |
| Predictable directional traversal | Arrow keys land somewhere unexpected |
| Focus anchored against content updates | Focus lands on the wrong element after a data load |
| Explicit focus entry point per screen | Focus starts nowhere, or in a random region |
| Focus visible after any scroll | Focus scrolls off-screen and disappears |

### The TV layout pattern

```text
┌─────────────────────────────────────────────────┐
│  Row 1: hero / continue watching                │  ← focus enters here
├─────────────────────────────────────────────────┤
│  Row 2: [card] [card] [card] →                  │  ← horizontal, wraps to next row
├─────────────────────────────────────────────────┤
│  Row 3: [card] [card] [card] →                  │
└─────────────────────────────────────────────────┘
   ↑ Down/Up moves between rows; Left/Right within a row.
   ↑ Geometry and focus graph agree, so traversal is predictable.
```

## Shared rules across reduced surfaces

| Rule | Applies to |
|---|---|
| One task per screen | Wearable, TV (per screen), spatial (per window) |
| Focus/attention model designed explicitly | TV, wearable (dial), spatial (gaze) |
| Detail escalates to a richer surface | Wearable → phone; TV → nothing (design it in) |
| No convention borrowed from the phone | Both |
| Legibility verified on the real display at real distance | Both |
| Motion restrained, comfort preferences honoured | Both |
| Input set enumerated and each path tested | Both |

## The reduced-surface checklist

- [ ] Task count per screen is one (wearable, TV screen)
- [ ] Navigation depth within budget (wearable 1–2, TV 2–3)
- [ ] Detail escalates to a richer surface rather than being crammed
- [ ] Every input the surface supports is exercised (dial, remote, voice, gaze)
- [ ] Focus/attention model is explicit; focus indicator visible at real distance
- [ ] Focus graph matches layout geometry (TV)
- [ ] No focus traps; every screen escapable with the surface's input
- [ ] Legibility verified on the real display at the real viewing distance
- [ ] Motion restrained; comfort/reduced-motion preferences honoured
- [ ] No phone convention (hover, dense tables, bottom tabs) carried over
