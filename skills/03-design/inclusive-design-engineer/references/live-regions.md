# Live Regions

<!-- DEEP: 5+min -- announcements, politeness, timing and the create-with-content trap -->

## The governing rule

**A live region announces changes to content that occurs after the region exists.** A region
created together with its content announces nothing, because from the AT's perspective nothing
changed — the content was always there (R4).

This single property explains the majority of "we added a live region and it still doesn't
announce" defects.

```html
<!-- ❌ Created with its content — announces nothing -->
<div aria-live="polite">Saved successfully</div>

<!-- ✅ The region exists first; the change announces -->
<div aria-live="polite" id="status"></div>
<!-- later: -->
<script>document.getElementById("status").textContent = "Saved successfully";</script>
```

## Politeness

| Value | Behaviour | Use for |
|---|---|---|
| `polite` | Waits for a pause in the user's activity | Routine status: saved, loaded, added, filtered |
| `assertive` | Interrupts immediately | Urgent, time-sensitive, or blocking information only |
| `off` | Does not announce (the default) | Decorative or duplicated content |

`assertive` interrupts the user mid-sentence. Every use must be justified: an error that blocks the
task, a session about to expire, a destructive action that completed. Using `assertive` for routine
confirmations makes the interface unusable — the AT never finishes a sentence.

Default to `polite`. Justify each `assertive`.

## Roles that imply live behaviour

Some roles carry an implicit politeness, which means adding the role is enough (and adding
`aria-live` on top is redundant):

| Role | Implicit politeness | Use for |
|---|---|---|
| `status` | polite | Routine status messages |
| `alert` | assertive | Urgent messages requiring immediate attention |
| `log` | polite | Append-only logs (chat, activity feeds) |
| `progressbar` | (not live by default) | Progress — announce value changes deliberately |
| `timer` | off | Countdowns — announce only meaningful thresholds |

Prefer the role when it fits: `role="status"` expresses both the semantics and the politeness.

## The atomic and relevant attributes

| Attribute | Effect |
|---|---|
| `aria-atomic="true"` | Announces the whole region on any change, not just the changed node |
| `aria-atomic="false"` | Announces only the changed node (default) |
| `aria-relevant="additions"` | Announces added nodes only |
| `aria-relevant="text"` | Announces text changes |
| `aria-relevant="removals"` | Announces removals (rarely useful alone) |

Use `aria-atomic="true"` when the region's meaning depends on the whole string — a counter, a
status line, a filtered-result count. Otherwise the AT may announce a fragment ("3" instead of
"3 results found").

```html
<div role="status" aria-atomic="true">3 results found</div>
```

## What to announce, and what not to

| Announce | Do not announce |
|---|---|
| A state change the user caused but cannot see | Every keystroke |
| An asynchronous completion ("Saved", "Uploaded") | Decorative or duplicated text |
| A count that changed because of a filter | Content that is already visible and focused |
| An error that blocks progress | A status the user can already perceive ("button pressed") |
| A step change in a multi-step flow | — |

The test: **would the user be unable to proceed without this information?** If not, it does not need
an announcement. Over-announcing is a real defect class — it makes the AT unusable by drowning the
useful signals.

## Timing and debouncing

| Problem | Fix |
|---|---|
| Rapid updates announce every intermediate value | Debounce; announce the settled state |
| A message appears and vanishes before it is read | Keep it long enough, or keep it in the DOM and mark it visually transient |
| Multiple regions announce at once | Use one region for related messages, or sequence them |
| A region announces on first page load | Do not populate the region during initial render — only on genuine change |

The last row is a common surprise: a region that is server-rendered with content may announce on
load, which is usually undesired. Keep the region empty in the initial markup and populate it on
change.

## Progress announcements

| Situation | Approach |
|---|---|
| Short, determinate | A `progressbar` with the value; announce on completion, not on every tick |
| Long, determinate | Announce meaningful thresholds (25%, 50%, 75%) rather than every percent |
| Indeterminate | A status message for start and a separate one for completion |
| Batch work | Announce the completion total, not each item |

Announcing every progress tick is the classic over-announcement defect; it makes the AT unusable
for the duration of the operation.

## Pattern: a status message component

```html
<!-- Rendered once, at app root, empty -->
<div id="app-status" role="status" aria-atomic="true" class="sr-only"></div>

<!-- On change, update the content; clear it after the message has been read -->
<script>
  function announce(message) {
    const el = document.getElementById("app-status");
    el.textContent = "";                 // reset so the same message re-announces
    requestAnimationFrame(() => { el.textContent = message; });
  }
</script>
```

Three details that make it work:

1. **The region is at the app root**, present from the first render.
2. **The content is cleared then set**, so a repeated identical message still announces.
3. **The region is visually hidden but not `display: none`** — a region that is not rendered may
   not announce.

## Visually-hidden, correctly

```css
.sr-only {
  position: absolute;
  width: 1px; height: 1px;
  padding: 0; margin: -1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
  border: 0;
}
```

Never `display: none` or `visibility: hidden` — both remove the element from the accessibility tree,
so it cannot announce.

## The two-region pattern for errors

An assertive region for blocking errors and a polite one for routine status, kept separate so an
urgent message is not queued behind a polite one.

```html
<div id="app-alert"  role="alert"  aria-atomic="true" class="sr-only"></div>
<div id="app-status" role="status" aria-atomic="true" class="sr-only"></div>
```

## The live-region checklist

- [ ] Every live region exists in the DOM before its content changes (R4)
- [ ] No region is created together with its content
- [ ] Politeness matches urgency; every `assertive` is justified
- [ ] Roles with implicit politeness (`status`, `alert`, `log`) used where they fit
- [ ] `aria-atomic="true"` where the whole string is the message
- [ ] Repeated identical messages re-announce (content cleared then set)
- [ ] Progress is announced at thresholds, not on every tick
- [ ] Related rapid updates are debounced
- [ ] Regions are visually hidden without `display: none`
- [ ] No announcement for information the user can already perceive
- [ ] The announcement is verified with a **named** screen reader, and recorded (R2)
