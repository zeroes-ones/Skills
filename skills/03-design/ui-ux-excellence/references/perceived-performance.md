# Perceived Performance

<!-- STANDARD: 3min -- skeletons, optimistic UI, progress legibility -->

## Perception is the metric

The clock is not what the user experiences. A screen that acknowledges instantly and completes
later feels faster than one that is silent and then instantaneous, even when the second is
genuinely quicker. Design for the perception, then optimise the clock.

This is R4: **any operation that can exceed the patience threshold must have a perceivable signal
before it does.**

## The thresholds

| Duration | What the user experiences | Response |
|---|---|---|
| Up to ~0.1s | Instant | No indicator — an indicator would flicker and add noise |
| ~0.1s to ~1s | Perceptible, tolerable | Immediate local feedback (pressed state, optimistic UI); no spinner |
| ~1s to ~10s | Attention drifts | Skeleton matching the final layout, or determinate progress |
| Beyond ~10s | The user switches task | Determinate progress with stages, plus the ability to leave |

Thresholds are approximately these values; confirm against current responsiveness guidance and
measure on your own representative device rather than assuming.

## The techniques, ranked

| Technique | Effect | Cost / risk |
|---|---|---|
| **Instant acknowledgement** | Removes the "did it work?" question | None — always do this |
| **Optimistic UI** | The result appears immediately | Needs a visible, correct rollback |
| **Skeleton** | Compresses perceived wait; prevents reflow | The shape must match the final layout |
| **Local progress for local work** | Keeps the rest of the screen alive | Requires a region-level indicator |
| **Determinate progress** | Honest for long operations | Requires knowing the total |
| **Stage labels** | Explains a long multi-step operation | Requires a real stage model |
| **Backgrounding** | Removes the wait entirely | Requires a notification/return path |
| **Chunked rendering** | Shows useful content sooner | Requires the content to be renderable in parts |

Note the absence of "a spinner in the middle of the screen" from the strong end of that list. A
central indeterminate spinner is the weakest technique available: it says "wait" without saying
how long, and it usually replaces content the user was reading.

## Skeletons

The skeleton is the highest-leverage technique for the 1–10s band, and it fails in two specific
ways.

**Failure 1 — wrong shape.** A skeleton that does not match the final layout causes the reflow it
was supposed to prevent; the content jumps when it arrives.

```
Wrong:  ▒▒▒▒▒▒▒▒▒▒           →  ┌─────┐
        ▒▒▒▒▒▒▒▒▒▒              │ text │    (layout shifts)
                                └─────┘

Right:  ┌─────┐              →  ┌─────┐
        │▒▒▒▒▒│                 │ text │    (no shift)
        └─────┘                 └─────┘
```

**Failure 2 — too long on screen.** A skeleton that appears for a fraction of a second is a
flash. Either raise the delay before showing it, or skip it for genuinely fast operations.

| Rule | Reason |
|---|---|
| Shape matches the final layout | Prevents the shift it exists to prevent |
| Appears only after a short delay | Avoids flashing on fast responses |
| Disappears as content arrives, region by region | Feels incremental rather than all-or-nothing |
| Carries no text | Skeleton text is misread as content |
| Preserves page chrome | Navigation stays usable during load |

## Optimistic UI

Apply the change immediately, assume success, and reconcile when the server responds.

```text
User taps "Send"
  → message appears in the thread immediately, marked as sending
  → on success: mark sent
  → on failure: mark failed, offer retry, keep the text
```

Rules that make it safe:

1. **The action must be very likely to succeed.** Optimistic UI on a flaky operation produces
   frequent rollbacks, which is worse than waiting.
2. **The rollback must be visible and correct.** A silent rollback teaches the user that the app
   lies.
3. **The user's input must survive failure.** Never lose the message the user typed.
4. **Ordering must hold.** Optimistic items must not reorder when the server's truth arrives.

## Progress legibility

| Operation | Signal |
|---|---|
| Upload/download | Determinate percentage, plus a cancel |
| Multi-step save | Stage labels, not a bar with no meaning |
| Search across sources | "Searching 3 of 5 sources" |
| Batch operation | "142 of 400 complete", with a way to leave |
| Unknown duration | Elapsed context ("still working…") plus a way out |

The rule that matters: **a long operation must let the user leave.** Blocking a screen for
minutes is the defect, not the duration.

## Keeping context alive

The most common perceived-performance defect is not slowness — it is destroying context to show
that something is happening.

| Defect | Fix |
|---|---|
| Full-screen spinner on refresh | Refresh in place; keep content visible |
| Blanking a list while filtering | Keep the previous results until the new ones arrive |
| Blocking a modal for a background save | Save in the background with a status indicator |
| Clearing a form to show a loading state | Never — the input is the user's work |
| Removing navigation during load | Keep the chrome; only the content region loads |

## Measuring the perception

| Metric | What it captures |
|---|---|
| Time to first meaningful feedback | How long until the user knows the action registered |
| Perceived-duration proxy (skeleton vs. spinner) | Comparative felt duration on the same operation |
| Interaction-to-next-paint | Responsiveness of the acknowledgement |
| Layout shift during load | Whether the skeleton is preventing the shift it should |
| Abandonment during the wait window | The ultimate perception signal |

Measure on a representative device and network — the median device, not the fastest one. A
perceived-performance finding verified on a developer machine is not verified (see the Error
Decoder's related symptom).

## The perceived-performance checklist

- [ ] Every operation's plausible duration is known, and the signal matches the band
- [ ] Sub-perceptible operations show no indicator (no flashing)
- [ ] Perceptible-but-short operations get instant acknowledgment, not a spinner
- [ ] Multi-second operations get a skeleton matching the final layout, or determinate progress
- [ ] Skeletons appear after a short delay and match the final shape
- [ ] Optimistic UI is used where success is highly likely, with a visible correct rollback
- [ ] Long operations let the user leave
- [ ] Context is preserved: no blanking, no full-screen spinner on refresh
- [ ] The user's input survives every failure path
- [ ] Verified on a representative device and network, not a developer machine
