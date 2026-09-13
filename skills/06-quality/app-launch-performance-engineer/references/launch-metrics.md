# Launch Metrics

<!-- STANDARD: 3min -- TTID versus TTFD, what each governs, and how to capture both -->

## The two metrics

Android's documentation defines them precisely:

| Metric | Definition | Reported by |
|---|---|---|
| **TTID** — time to initial display | "the time it takes to display the first frame" | the framework, automatically, for every app |
| **TTFD** — time to full display | "the time it takes for the app to become fully interactive" | the app, explicitly |

The same source explains why both matter: "TTID lets the user know that the app is loading, and TTFD
is when the app is actually usable." *(Source: Android, "App startup time".)*

## Why one number is not enough

They answer different questions, and a good value on one says nothing about the other.

| Metric | The user's question | Consequence of a poor value |
|---|---|---|
| TTID | "Did my tap register?" | perceived unresponsiveness; the user may tap again or leave |
| TTFD | "Can I actually use this?" | the first interaction does nothing, or the screen is visibly incomplete |

**The trap:** TTID can be *fast* while TTFD is poor — a shell or splash renders immediately, and the
screen stays unusable. Optimising only TTID will show a satisfying number while the experience stays
broken. That is why R2 forbids conflating them.

```
Good TTID, poor TTFD:
  0 ms ──frame──▶ 250 ms ──────────usable──────────▶ 3,400 ms
        (looks fast)                                 (user waited 3.4 s)

Poor TTID, good TTFD:
  0 ms ──────────────frame + usable──────────────▶ 900 ms
                     (nothing, then everything at once)
```

The first case is the more dangerous one, because the instrumentation says the launch is fine.

## Capturing TTID

| Platform | Mechanism |
|---|---|
| Android | the framework logs a `Displayed` line with the TTID value; readable from `logcat`, or measured automatically by the platform's macrobenchmark tooling |
| iOS/macOS | the launch instrument trace; first-frame timing relative to process start |
| Web | first contentful paint / first paint, from the browser's performance entries |
| Desktop | first-paint or window-shown timing from the platform's instrument |
| Serverless | not applicable in the same sense; the analogue is time to first response |

The Android documented shape, for reference:

```
ActivityManager: Displayed com.example/.StartupTiming: +3s534ms
```

That line is the TTID. Because the framework reports it, it is available without instrumenting the
app — which makes it the right metric for a *baseline* and for a production alert.

## Capturing TTFD

This one requires the app to say when it is done, because only the app knows.

```text
1. Define "fully interactive" for this screen, concretely.
     - the primary content is rendered
     - the first action the user will take is possible
     - NOT "everything loaded" (that is a different, later milestone)
2. Call the platform's report-fully-drawn equivalent at that moment.
3. Verify the signal fires on every path, including the empty and error states.
```

### Defining "fully interactive" honestly

This is the judgement call that makes TTFD useful or useless.

| Definition | Verdict |
|---|---|
| "The primary content is visible and the first action works" | **correct** |
| "Every network request completed" | wrong — that is a later, unnecessary milestone |
| "All images decoded" | usually wrong |
| "The spinner disappeared" | wrong if a shell is still showing |

**The failure mode:** a TTFD signal fired too early (as soon as a shell renders) makes the metric
meaningless, and it will report success while users wait. Test the signal by timing the first real
interaction, not by trusting the call site.

## The third metric that teams forget

**TTI on the web** — time to interactive — is the web's analogue of TTFD, and it is the metric that
Lighthouse and Web Vitals address. First paint is the web's TTID. *(Source: Chrome/Lighthouse Time to
Interactive guidance; Web Vitals.)*

The practical point: on the web, the same two-metric discipline applies, but the vocabulary differs.
When a web launch complaint arrives, ask which of the two the user means rather than accepting
"slow start".

## What each metric is sensitive to

| TTID sensitive to | TTFD sensitive to |
|---|---|
| process and loader work | deferred main-thread work |
| static initializers | data fetching on the critical path |
| framework/system init | state hydration |
| root layout complexity | code still being verified or JIT-compiled |
| theme and asset inflation | post-frame work moved but not off-thread |

Reading the pair tells you which family of fixes applies — which is why both are captured before any
fix is chosen (R3).

## Reporting shape

```text
Launch measurement — <surface> — <platform> <version> — <date>

Mode:        cold (process killed between runs)
Device:      <median device class>
Cache:       cleared
Runs:        20

TTID   median 1,240 ms   p90 1,690 ms
TTFD   median 3,410 ms   p90 4,120 ms

Interpretation: TTID is within budget; TTFD is 2.2 s beyond it. The gap is
post-first-frame work, not initialisation — so the fix belongs in deferred
main-thread work and data sequencing, not in the pre-main phase.
```

That interpretation is the deliverable: the pair of numbers, and the phase family they point at.

## Checklist

- [ ] Both TTID and TTFD are measured, and reported separately (R2)
- [ ] TTFD is defined concretely for the screen, not as "everything loaded"
- [ ] The TTFD signal is verified to fire when the screen is genuinely usable
- [ ] The TTFD signal fires on empty, error and partial-data paths, not only success
- [ ] The pair is interpreted to a phase family, and that interpretation is recorded
- [ ] The web equivalent (first paint / time to interactive) is used for web surfaces
- [ ] Both metrics are captured on the median device class, cold, with the cache state stated
- [ ] The production metric is the one the platform reports automatically (TTID), with TTFD added by the app
