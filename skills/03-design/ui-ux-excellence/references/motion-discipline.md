# Motion Discipline

<!-- STANDARD: 3min -- what to animate, budgets, easing and reduced motion -->

## The governing rule

**Motion must explain a change.** A transition should communicate where something came from, what
changed, or that one thing caused another. If it explains nothing, it is latency dressed as
polish.

This is R3, and it is the rule most often broken — not because teams love animation, but because
animation is added by default by component libraries and never questioned.

## What motion is for

| Purpose | Example | Notes |
|---|---|---|
| **Spatial** | A panel slides in from the edge it occupies | Explains where the panel lives |
| **Hierarchical** | A detail view expands from its row | Explains the parent-child relationship |
| **Causal** | An item animates into the cart it was added to | Explains what caused what |
| **Continuity** | A list item persists position across a sort | Preserves identity through change |
| **Feedback** | A pressed state | Confirms the input registered |
| **Attention** | A brief highlight on new content | Must be dismissible and non-blocking |

If a proposed animation maps to none of these, it should not exist.

## What must not be animated

| Never | Why |
|---|---|
| Waiting for a transition to complete before accepting input | The interaction now has a latency floor |
| Decorative motion longer than the interaction it accompanies | Motion must not outlast its cause |
| Motion that repeats indefinitely in view | Draws attention from the task permanently |
| Motion that blocks or delays an action | Friction disguised as delight |
| Motion on a destructive confirmation | Delight is inappropriate at a decision point with consequences |
| Large full-field motion | Comfort risk, and it dominates a screen that should be calm |
| Motion with no reduced-motion alternative | Fails the comfort preference (see below) |

## Budgets

| Property | Guidance | Reason |
|---|---|---|
| Duration — micro-feedback | At the edge of perceptible; effectively immediate | Feedback must feel caused by the input |
| Duration — transition | Shorter than the interaction it accompanies | Longer reads as lag |
| Duration — large surface | Longer, but still brief | A large element moving fast reads as violent |
| Property | Compositor-friendly only (`transform`, `opacity`) | Layout-triggering properties cause jank |
| Simultaneous animations | Few | Attention cannot follow several at once |
| Frequency | Rare | Recurring motion becomes noise within a session |

The absolute numbers vary by platform and change with platform revisions — confirm the current
recommended durations against your target platform's guidance rather than recalling them. The
*relationships* above are the portable part: feedback shorter than transition, transition shorter
than the interaction, and nothing that makes the user wait.

## Easing

| Direction | Easing | Why |
|---|---|---|
| Entering (appearing) | Decelerate | Arrives quickly, settles — matches physical arrival |
| Exiting (disappearing) | Accelerate | Leaves quickly — matches physical departure |
| Moving within the screen | Ease in-out | Smooth both ends |
| Feedback (press) | Immediately linear or near-instant | Must not feel laggy |
| Reordering | Ease, with continuity of identity | Shows the item is the same item |

Linear easing on a spatial transition reads as mechanical and is the most common "something feels
off" cause.

## Reduced motion

The platform exposes a reduced-motion preference, and honouring it is both a conformance
requirement and a comfort necessity for users with vestibular disorders.

```css
@media (prefers-reduced-motion: reduce) {
  /* Replace motion with an instant change, not with nothing */
  .panel        { animation: none; transition: none; }
  .fade-in      { transition: opacity 0.01ms; }   /* opacity is generally acceptable */
  .slide-in     { transform: none; }              /* no spatial movement */
}
```

Two rules:

1. **Replace, do not remove.** Removing a transition can leave the interface in a state it never
   reaches. Substitute an instant state change or an opacity change.
2. **Never use reduced-motion as a reason to remove necessary feedback.** A pressed state and a
   progress indicator are feedback, not decoration; they must remain, just without travel.

The preference is also exposed programmatically in most UI frameworks (a motion-reduction query or
setting). Honour it in native code as well as CSS.

## Implementation rules

| Rule | Reason |
|---|---|
| Animate `transform` and `opacity`, not layout properties | Layout-triggering properties cause reflow and jank mid-animation |
| Respect the input's own timing | A transition must not add a floor to interaction latency |
| Use a transition token, not an inline duration | Consistency, and one place to correct |
| Define motion in the design system | Otherwise every component invents its own timing |
| Test on the median device | Animation jank appears on the slow device, not the fast one |
| Test with reduced motion enabled | The substitution is rarely written the first time |

## Motion anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| "Animate everything for consistency" | Motion without purpose is delay; consistency of decoration is not a virtue |
| Blocking the action on the animation | Adds latency to every interaction |
| Spinner-plus-animation | Competing signals; the user cannot tell what is happening |
| Motion that repeats forever in view | Permanent attention theft |
| Delight on a destructive path | Inappropriate at a consequential decision |
| Reduced motion = no motion at all | Can leave the UI in an unreachable state; substitute instead of deleting |
| Testing only on a fast device | Jank is invisible there |
| Inline durations everywhere | No consistency, no single place to fix |

## The motion checklist

- [ ] Every animation states what it explains (spatial, hierarchical, causal, continuity, feedback, attention)
- [ ] Micro-feedback is effectively immediate
- [ ] Transitions are shorter than the interaction they accompany
- [ ] Only compositor-friendly properties are animated
- [ ] No action is blocked or delayed by a transition
- [ ] Easing matches direction (decelerate in, accelerate out)
- [ ] Durations come from tokens, defined in the design system
- [ ] Reduced motion is honoured, substituting an instant or opacity change
- [ ] Necessary feedback survives reduced motion
- [ ] No indefinite decorative motion in view
- [ ] Verified on the median device, with reduced motion enabled and disabled
