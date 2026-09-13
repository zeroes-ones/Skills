# Launch Modes

<!-- STANDARD: 3min -- the cold/warm/hot taxonomy, what each pays for, and how to measure each -->

## The three modes, as the platform defines them

Android's launch-time documentation defines exactly three states. These definitions are the working
vocabulary, and they are authoritative rather than invented:

| Mode | Definition | What has to happen |
|---|---|---|
| **Cold** | "an app's starting from scratch… the system's process creates the app's process" | process creation, loader, relocations, initializers, framework/system init, first frame |
| **Warm** | "encompasses a subset of the operations that take place during a cold start" | less: some state survives, the process may exist |
| **Hot** | "the system brings your app's host activity to the foreground" | restoration and re-layout; if the UI is still resident, "the app can avoid repeating object initialization, UI initialization, and rendering" |

Cold start "presents the greatest challenge" in minimising start-up time, per the same
documentation. *(Source: Android, "App startup time".)*

## Why the distinction decides the work

The modes do not merely differ in degree — they differ in **cause**.

| Mode | Dominant cost | Optimising the wrong thing looks like this |
|---|---|---|
| Cold | loader work, relocations, static initializers, framework init, first frame | "we made resume faster" against a cold-launch complaint |
| Warm | a subset of cold init, plus whatever state did not survive | "we shrank the binary" against a warm complaint caused by a data refetch |
| Hot | state restoration, re-layout, a refresh on resume | "we deferred initializers" against a hot complaint caused by a synchronous refresh |

This is R6: the modes are not interchangeable, and work aimed at the wrong one produces no measured
improvement — which is indistinguishable from doing nothing.

## Measuring each mode correctly

The measurement *is* the mode. Getting the mode right is mostly about controlling process state.

### Cold start

```text
Requirement: the process must not exist before the run.

Android:   force-stop the app between runs (or kill the process), then launch
           → TTID is reported by the framework in logcat
iOS/macOS: terminate completely; be aware of OS prewarming, which changes the measurement
Desktop:   kill the process; clear any caches you are also testing
Web:       cache disabled, fresh origin, cold CDN
Serverless: force a new instance (no warm capacity), or accept that you are measuring warm

Then: repeat at least 10 times and report MEDIAN and p90 — not the best run.
```

**The prewarming caveat:** some platforms prewarm apps in the background, so a "cold" launch may not
be cold in the sense you assume. State whether prewarming was active, because it changes what the
measurement means.

### Warm start

```text
Requirement: the process may exist, but the app is re-created.

Android:   back out of the app (leaving the process), then relaunch
           → this is the documented warm case
Desktop:   quit the window but keep the process, then reopen
Web:       return to the origin with a warm HTTP cache
```

### Hot start

```text
Requirement: the app is running and is brought to the foreground.

Android:   home button, then relaunch → documented as hot
iOS:       background the app, then foreground it
Desktop:   minimise/hide, then restore the window
```

## Which mode to budget

| Mode | Budget it when |
|---|---|
| Cold | **always** — it is the mode with the largest cost, and the one most complaints describe |
| Warm | when users hit it often (an app the OS kills frequently, or a workflow that backs out and returns) |
| Hot | when resume has real work to do (a large document, a live session, a data refresh) |

**The published excessive thresholds are per mode**, which is the clearest possible signal that a
single "launch time" target is wrong. Android marks start-up excessive at cold ≥ 5 s, warm ≥ 2 s and
hot ≥ 1.5 s, measured as TTID. *(Source: Android vitals launch-time guidance.)*

## The mismatch that motivates this whole skill

```
Complaints are about   →  COLD (first launch, after an update, after the OS killed the app)
Developers test        →  HOT  (app already open, warm caches, flagship device)
```

The two modes are optimised by different changes, so the mismatch means effort lands where nobody
felt the problem. **Name the mode from the complaint before measuring anything** (R1, R6).

## What each mode can and cannot tell you

| Mode | Tells you | Cannot tell you |
|---|---|---|
| Cold | the total init budget; the cost of everything that runs before the UI | the steady-state application behaviour |
| Warm | what did not survive or what must be recomputed | the cost of process and loader work |
| Hot | the cost of restoration and re-layout | anything about initialisation |

Use all three where you can, but **attribute causes using the mode that shows them**. A hot-start
measurement cannot see a static initializer, because in hot start the process never restarted.

## Mode selection, condensed

```text
Complaint: "the app takes ages to open"          → COLD (almost always)
Complaint: "returning to the app is slow"        → HOT (restoration)
Complaint: "after I back out and reopen, slow"   → WARM
Complaint: "slow the first time I open a screen" → NOT a launch mode (first-use cost)
```

The last row is the one teams mis-file. First-use cost — lazy symbol binding, lazy initialization, a
cold cache on first access — belongs to `library-linkage-architect` (binding mode) and
`performance-engineer`, not here.

## Checklist

- [ ] The failing mode is named, and it matches the complaint's wording (R1, R6)
- [ ] The measurement actually reproduces that mode (process state controlled)
- [ ] Prewarming or platform-specific pre-start behaviour is accounted for and stated
- [ ] At least 10 runs, reporting median and p90 rather than best
- [ ] The device class is named, and it is the median rather than the fastest
- [ ] The cache state is stated (cold/warm, cleared/retained)
- [ ] Both display and interactive metrics are captured for the mode, not just one
- [ ] The method is written down before the baseline, so the comparison can hold it constant (R5)
