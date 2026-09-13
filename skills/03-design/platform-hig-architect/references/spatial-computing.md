# Spatial Computing

<!-- DEEP: 5+min -- headset conventions, gaze, depth and comfort -->

> **Verification note.** Spatial-computing platforms are the newest and the fastest-changing,
> and their guidance is revised frequently. Confirm every specific convention, dimension and API
> against the targeted SDK's current documentation before designing against it (see the
> Anti-Hallucination section of `SKILL.md`). Treat this file as a reasoning framework, not a
> source of current dimensions.

## Why spatial is a genuinely different medium

Every other surface is a rectangle the user looks at. A headset is a *space* the user occupies.
That changes four things at once:

| Property | Screen surfaces | Spatial |
|---|---|---|
| Viewport | Fixed rectangle | Open space; content is placed, not fitted |
| Primary pointer | Touch or mouse | **Gaze** — the eyes are the pointer |
| Depth | Simulated | Real; content has a position in space |
| Body | Stationary | Head and hand motion are inputs; comfort is a design constraint |

The most common failure is treating the headset as a large screen: a 2D layout stretched across
the field of view, with no placement, no depth, and no comfort consideration.

## The conventions that follow

### 1. Content is placed, not stretched

| Screen instinct | Spatial equivalent |
|---|---|
| Fill the viewport | Place a window at a comfortable distance and size |
| Fixed layout | Arrangement in space, with a sensible default and user repositioning |
| Responsive breakpoints | Distance, scale and placement relative to the user |
| Z-index | Depth layering with real occlusion |

### 2. Gaze is the pointer

| Screen convention | Spatial convention |
|---|---|
| Hover to preview | Gaze to highlight, with dwell or an explicit commit |
| Click to select | Gaze + pinch/gesture, or gaze + voice |
| Focus ring | A gaze highlight that is legible without being distracting |
| Cursor position | Gaze position, with smoothing to avoid jitter |

Consequences:

- **Gaze-driven selection needs a commit gesture.** Selecting on gaze alone produces accidental
  activations, because users look at things they do not intend to choose.
- **Targets must tolerate gaze precision.** Gaze is less precise than a pointer; targets need
  generous size and spacing, and a dwell/hover state before commitment.
- **The gaze highlight must not obscure.** It indicates, it does not decorate.

### 3. Comfort is a hard requirement, not polish

| Comfort factor | Design response |
|---|---|
| Sustained neck rotation | Keep primary content within a comfortable field; avoid extremes |
| Vergence/accommodation mismatch | Place content at comfortable distances; avoid extremes of near/far |
| Vection and motion sickness | Avoid large-field motion, especially camera-relative movement; provide a stable reference frame |
| Unexpected motion | Never move the user's viewpoint without their input |
| Duration | Long sessions need breaks and stable reference points |

**Never move the user.** Moving the viewpoint without user input is the fastest route to
discomfort, and it is the spatial equivalent of a layout shift — except the user feels it.

### 4. Honour the platform's comfort preferences

The platform exposes user comfort and accessibility settings (motion reduction, comfort
parameters). Honouring them is R6's spatial case, and ignoring them makes the app unusable for
the users who set them.

## Input model

| Input | Role | Requirement |
|---|---|---|
| Gaze | Pointer, highlighting | Smoothed; never the sole trigger for an action |
| Hand gesture | Selection, manipulation | Discoverable; must have a non-gesture equivalent (2.5.1) |
| Voice | Entry, commands | Available as an alternative for entry-heavy tasks |
| Physical input | Precise manipulation, text | Supported where the platform provides it |

The modality enumeration (R4) is essential here, because a spatial app with no voice or physical
input path excludes users who cannot gesture. See `references/gestures-and-input.md`.

## Windows and arrangement

| Concept | Screen | Spatial |
|---|---|---|
| Window | A rectangle in a viewport | A placed surface with a position and a size |
| Fullscreen | Fill the viewport | Immersive mode, entered deliberately |
| Multi-window | Tiled in a viewport | Arranged in space; the user's arrangement must persist |
| State restoration | Restore the layout | Restore position, size, *and* spatial arrangement |

The restoration requirement is easy to miss: a user who arranges their workspace in space expects
that arrangement to survive a session. Resetting it is the spatial equivalent of clearing a
desktop each launch.

## What carries over from other surfaces

| Carries over | Does not carry over |
|---|---|
| Information architecture | Viewport-filling layouts |
| Task models | Fixed-size assumptions |
| Content and copy | Hover-only interactions |
| Brand identity | Dense text at small sizes |
| Accessibility intent (labels, focus order, alternatives) | Pointer-precision targets |

## The spatial checklist

- [ ] Content is placed in space with a sensible default, not stretched to fill
- [ ] Gaze is treated as the pointer, with a commit gesture for selection
- [ ] Gaze targets are sized for gaze precision, with a highlight before commitment
- [ ] The gaze highlight indicates without obscuring
- [ ] Primary content is within a comfortable field; extremes avoided
- [ ] No unprompted viewpoint movement, ever
- [ ] Large-field motion is avoided; a stable reference frame exists
- [ ] Platform comfort and motion preferences are honoured
- [ ] Every action has a non-gesture equivalent where a gesture would otherwise be the only path
- [ ] Voice and physical input supported for entry-heavy tasks
- [ ] Window/workspace arrangement persists across sessions
- [ ] Legibility and target size verified at the platform's comfortable distances
