# Web Hydration

<!-- STANDARD: 3min -- hydration cost and time-to-interactive, with the chunk boundary -->

> **Scope note.** This file owns the *launch phase* view of the web: what hydration costs and how it
> maps to Phase 3. Chunk mechanics — code splitting, tree shaking, bundle analysis — belong to
> `frontend-developer`. Do not duplicate that work here; hand it over with the attribution.

## Hydration is the web's cold start

A server-rendered page has two lives:

```
Life 1 (server):  HTML is generated and delivered → the browser paints it fast → TTID (first paint)
Life 2 (client):  the framework re-executes the component tree, attaches listeners,
                  re-creates state → the page becomes interactive → TTI (time to interactive)
```

The gap between them is the web's Phase 3, and it is where the user experience usually breaks: the
page *looks* ready while taps do nothing.

```
0 ms ────first paint────▶ 400 ms ──────────interactive──────────▶ 3,200 ms
         (looks done)                  (taps did nothing for 2.8 s)
```

This is the same metric-conflation trap as mobile: first paint is TTID, time to interactive is TTFD,
and a fast first paint says nothing about the second.

## Why hydration costs what it does

| Cost driver | Mechanism |
|---|---|
| The component tree's size | every component that hydrates must be re-executed |
| Main-thread blocking | hydration is largely synchronous; it blocks input handling |
| Data re-fetching | a naive implementation fetches on the client what the server already had |
| State re-creation | state is built twice: once on the server, once on the client |
| Framework runtime size | the runtime must be parsed, compiled and executed before hydration starts |
| Mismatch handling | server/client output differing triggers a re-render, doubling the work |

The third and fourth rows are the ones that surprise teams: a server-rendered page that re-fetches and
re-creates everything has paid for rendering twice and gained only the first paint.

## The strategies, in order of ambition

| Strategy | What it reduces | Cost |
|---|---|---|
| **Smaller interactive root** | less of the tree hydrates | requires separating static from interactive |
| **Islands / partial hydration** | only flagged regions hydrate | architectural; framework support varies |
| **Progressive hydration** | hydration is time-sliced | still hydrates everything, eventually |
| **Server components / zero-JS regions** | static regions ship no JS at all | framework-specific |
| **Deferred hydration** | below-fold content hydrates on demand | complexity; care needed for a11y |

**The direction of travel: hydrate less of the page.** Islands exist precisely because the standard
model — hydrate the whole tree — makes the entire page's interactivity hostage to the largest
component.

## Measuring it

| Metric | What it captures |
|---|---|
| First paint / first contentful paint | the web's TTID |
| Time to interactive | the web's TTFD — when input actually works |
| Total blocking time | how long the main thread was unavailable |
| Long tasks after first paint | the hydration work itself |
| Interaction-to-next-paint on the first real interaction | the user-perceived consequence |

**The measurement discipline is identical to mobile** (R1, R2, R5): cold cache, a named device class,
repeated runs, median rather than best, and the same method for before and after. Browser profiler
traces give the phase breakdown; the long-task list after first paint is usually where hydration shows
up.

## The web phase model

```
PHASE 1 (pre-main analogue)   the JS runtime and framework must load and parse before
                              anything can hydrate — network + parse + compile
PHASE 2 (first frame)          HTML/CSS paint → first contentful paint
PHASE 3 (to-interactive)      hydration: re-execution, listener attachment, state creation
                              → time to interactive
```

The Phase 1 analogue matters on the web more than on native, because the runtime itself is shipped:
a large framework bundle *is* pre-main cost, transferred rather than executed locally.

## Attributing on the web

```text
1. First paint measured → Phase 2 bound.
2. Time to interactive measured → the total to Phase 3.
3. Long tasks between the two → the hydration work.
4. Per-component attribution: disable or defer one region and re-measure.
   (This is the web's ablation, and it works the same way — one change, control re-measured.)
```

**The usual finding:** one or two components account for most of the hydration cost, and they are
rarely the ones the team suspects. The ablation tells you which.

## The boundary with `frontend-developer`

| This file owns | `frontend-developer` owns |
|---|---|
| Hydration as a Phase 3 cost, and its attribution | Code splitting and chunk strategy |
| Time-to-interactive as the launch metric | Tree shaking and dead-code elimination |
| The interactive-root decision (architectural) | Bundle size analysis and optimisation tooling |
| The launch budget for the web surface | Asset pipeline and image optimisation |

**Hand over the attribution, not the whole task.** "Hydration is 2.4 s of a 3.2 s time-to-interactive,
concentrated in two components" is a finding `frontend-developer` can act on. "Make the site faster"
is not.

## The re-fetch trap

The most common hydration defect, and the easiest to fix:

```
Server:  fetch data → render HTML → send HTML
Client:  hydrate → fetch the SAME data again → re-render
```

The user sees the page twice-rendered, and the second fetch is on the critical path for interactivity.
Fix by serialising the server's data into the payload and seeding the client from it. The saving is
usually large and mechanical.

## Checklist

- [ ] First paint and time to interactive are measured and reported separately (R2)
- [ ] Long tasks after first paint are captured, to bound the hydration work
- [ ] Per-component attribution is done by ablation, with the control re-measured
- [ ] Server-fetched data is serialised into the payload rather than re-fetched on the client
- [ ] The interactive root is as small as the design allows
- [ ] Islands / partial hydration is considered where the framework supports it
- [ ] The measurement is cold-cache, named device class, repeated, median (R1)
- [ ] The chunk-level fix list is handed to `frontend-developer` with the attribution attached
- [ ] A time-to-interactive budget exists for the web surface, with a gate
