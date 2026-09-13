# State Coverage

<!-- STANDARD: 3min -- the full state taxonomy with patterns per state -->

## The governing rule

Every asynchronous surface has more than one state, and the state the designer drew is the least
common one. R2 requires the enumeration: **loading, empty, error, partial** — plus content
extremes and first-run.

Most shipped defects live in the states nobody designed. A review that only looks at the success
path cannot see them, which is why this is a gate and not a score.

## The taxonomy

| State | When it occurs | The defect if absent |
|---|---|---|
| **First-run / onboarding-empty** | The user has no data yet, by definition | The first impression is a dead screen |
| **Loading (initial)** | Before the first data arrives | Blank screen reads as broken |
| **Loading (subsequent/refresh)** | Data exists; it is being updated | Full-screen spinner destroys context |
| **Empty (no results)** | Valid query, zero matches | User cannot tell "no results" from "broken" |
| **Empty (nothing yet)** | The feature is unused, not failing | User cannot tell "nothing here" from "not loaded" |
| **Error (retryable)** | Transient failure | No route forward; user abandons |
| **Error (permanent)** | Unrecoverable for this user/session | User retries against a wall |
| **Partial** | Some data loaded, some failed | The whole screen blanks, losing the working part |
| **Stale** | Data present but old | The user trusts outdated information |
| **Offline** | No connectivity | Confusing errors instead of an honest state |
| **Permission-denied** | The user cannot see this | A silent or scary failure |
| **Extreme content** | Longest, shortest, zero | Layout breaks, text overflows, the row collapses |
| **Success confirmation** | The action worked | The user repeats the action |

## Patterns per state

### First-run / onboarding empty

```
┌─────────────────────────────────┐
│  ▢  (illustration of the thing) │
│                                 │
│  No projects yet                │  ← name the concrete noun, not "items"
│  Projects hold your team's work │  ← one line on what this surface is for
│                                 │
│  [ Create your first project ]  │  ← exactly one primary action
│  Or import an existing one      │  ← secondary path, subordinate
└─────────────────────────────────┘
```

Rules: teach what the surface is for, offer one primary action, never apologise, never show an
error-looking state for a normal condition.

### Empty (no results)

```
No results for "quarterly report"          ← echo the query
[ Clear filters ]  [ Search all projects ] ← ways out, not just information
```

Rules: distinguish no-results from nothing-yet; echo the input that produced the empty set; always
offer a way back to a non-empty state.

### Loading (initial)

```
┌─────────────────────────────────┐
│  ▒▒▒▒▒▒▒▒▒▒▒▒  (skeleton)        │  ← matches the FINAL layout
│  ▒▒▒▒▒▒▒▒                        │
│  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒         │
└─────────────────────────────────┘
```

Rules: the skeleton must have the final layout's shape, or the arrival of data causes reflow; keep
the page chrome stable; never show a skeleton where the layout is unknown — use progress instead
(Decision Tree 4).

### Loading (subsequent)

Keep the existing content and indicate activity on the region being updated. The full-screen
spinner for a refresh is a defect: it destroys context and makes a working screen look broken.

### Error (retryable) — inline, regional

```
┌─────────────────────────────────┐
│  Projects                       │
│  ─────────────────────────────  │
│  ⚠ Couldn't load your projects  │  ← what failed, in the user's terms
│  Your work is safe.             │  ← preservation, if true
│  [ Try again ]                  │  ← the next action
└─────────────────────────────────┘
```

Rules: name the failure in user terms; state preservation; offer the retry; scope it to the region
that failed, not the whole screen.

### Error (permanent)

State what cannot happen and what the user's options actually are. Do not offer a retry that will
fail again — that erodes trust faster than the original failure.

### Partial

```
┌─────────────────────────────────┐
│  ┌──────────┐  ┌──────────┐     │
│  │ Project  │  │ Project  │     │  ← the data that loaded
│  └──────────┘  └──────────┘     │
│  ⚠ 2 projects couldn't load     │  ← the part that did not, marked
│  [ Retry failed ]               │
└─────────────────────────────────┘
```

Rule: never blank the screen because part of it failed. Render the working part.

### Stale

Show the age ("Updated 4 minutes ago") and refresh in place. Do not clear content to refresh it.

### Offline

An explicit offline state with what is and is not available, plus queueing where the product
supports it. Silent failure is worse than a stated limitation.

### Permission-denied

Name the permission and who can grant it, with the request path. Never present it as an error.

### Extreme content

| Extreme | Requirement |
|---|---|
| Longest plausible string | Wrapping or truncation policy defined; truncation must not hide the discriminator |
| Shortest (one character) | Layout does not collapse; label still associated |
| Zero/blank | Renders as the empty value, not as a broken element |
| Numeric extremes | Very large and very small values render without overflow |
| Mixed direction/script | RTL and mixed-script content renders without reordering |

### Success confirmation

For actions whose result is not visible, confirm explicitly — and for destructive actions,
confirm the reversal window if one exists ("Undo"). Silent success causes repeat actions.

## The state matrix template

| Screen | First-run | Loading | Empty(no results) | Empty(nothing yet) | Error(retry) | Error(perm) | Partial | Stale | Offline | Permission | Extremes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Project list | | | | | | | | | | | |
| Project detail | | | | | | | | | | | |
| Search | | | | | | | | | | | |
| Settings | | | | | | | | | | | |

Mark each cell: `designed`, `n/a` (with the reason), or **`MISSING`**. The `MISSING` cells are the
work, and they are usually visible in the matrix long before they are visible to a user.

## Reviewer's quick pass

```text
For each screen that fetches anything:
  1. Disconnect the network before it loads       → is there an honest error state?
  2. Return an empty collection                    → is there an empty state with a way forward?
  3. Throttle to a slow profile                    → is there a skeleton or legible progress?
  4. Fail one of two requests                      → is there a partial state, or a blank screen?
  5. Sign out mid-session and act                  → is there a permission or session-expiry state?
  6. Paste a 200-character value                   → does the layout survive?
  7. Try the screen as a brand-new user            → is the first-run state a teaching surface?
```

Seven steps, a few minutes per screen, and it finds the majority of state defects before users do.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Only the success state designed | Every other user is in an undefined state |
| "No data" as the empty state | Says nothing about what the surface is for or what to do |
| Full-screen spinner on refresh | Destroys working context |
| Blanking on partial failure | Loses the user's working portion |
| Skeleton with the wrong shape | Causes the reflow the skeleton was meant to prevent |
| Error text with no remedy | Abandonment (Heuristic 9) |
| Treating offline as an error | It is a state with defined capabilities |
| Truncation that hides the discriminator | All rows look identical; the user cannot choose |
| State coverage as a score | These are per-screen gates, not an average |
