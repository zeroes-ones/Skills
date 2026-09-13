# Navigation Conventions

<!-- STANDARD: 3min -- navigation models, back affordances and information architecture per platform -->

> **Verification note.** Navigation control names and exact behaviours change between platform
> releases. The *models* described here are stable; the specific APIs and control names must be
> confirmed against the targeted SDK's current documentation.

## Why navigation is the highest-stakes convention

Navigation is the one convention users operate without thinking. It is learned once, on the
first app, and expected forever. It is also the most expensive property to change, because it
is structural: changing a navigation model means moving screens, rewiring state, and breaking
every bookmark, deep link and muscle memory built on top of it.

This is why R1 requires the convention matrix *before* screens. A navigation decision made per
screen is a decision made differently on every screen.

## The models

| Model | Shape | Fits | Fails when |
|---|---|---|---|
| Stack | Push/pop a hierarchy | Tasks with a clear drill-down | Used for peer destinations (tabs would be right) |
| Tabs | Peer destinations, flat | A small set of top-level areas | More than about five peers, or when the areas are hierarchical |
| Drawer | Many peers, hidden | Large peer sets, lower-frequency areas | The primary destinations are the ones you hide |
| Sidebar / rail | Peers with persistent context | Tablets, desktop, foldables | On a phone, where it steals the content width |
| Split (list + detail) | Master and detail side by side | Tablets, desktop, wide layouts | At a narrow width without collapsing to a stack |
| Focus rail (TV) | Linear/spatial traversal | Remote-driven surfaces | Any touch or pointer surface |

## The back affordance, per family

| Family | Back is | Violating it means |
|---|---|---|
| Apple | A gesture from the leading edge, plus a control in the navigation bar | Users swipe and nothing happens — a trapped feeling |
| Android | System back (button or gesture), *including predictive back* | The system gesture exits the app instead of navigating |
| Web | The browser's back button, and the address bar | Users lose their place; deep links break |
| Windows | A back control, an Esc/Alt-Left binding, and reliable history | Keyboard users cannot navigate back |
| TV | An explicit back/exit control on the remote | The user cannot leave a screen — a dead end |

Two consequences that catch teams out:

1. **Android's back is not the app's to own.** An app that intercepts the system back gesture
   incompletely causes the OS to close the app from an inner screen. Handle the full history,
   not just the top of the stack.
2. **Web back is also the navigation model.** An SPA that manages state without pushing history
   entries makes back leave the site instead of the view. Push a history entry per view.

## Information architecture across platforms

The *shape* of the information architecture can be shared; the *expression* cannot.

```text
Shared:        Areas → Sections → Detail
iOS:           Tab per Area → Stack per Section      (peer areas as tabs)
Android:       Nav per Area → Stack per Section      (back integrates with the system)
Tablet:        Rail/Sidebar per Area → List + Detail (persistent context)
Web:           Nav per Area → Routes per Section     (addressable, back/forward works)
Desktop:       Menu/window per Area → Shortcuts      (parallel work, multi-window)
TV:            Rail per Area → Linear focus          (no pointer, focus only)
Watch:         Page per Area, shallow                (no deep hierarchy)
```

The information architecture is identical; the expression differs in every row. That is the
answer to "how do we share a design across platforms": share the IA, fork the navigation.

## Navigation depth budgets

Every surface has a depth it tolerates before the user loses the thread:

| Surface | Comfortable depth | Why |
|---|---|---|
| Phone | 3–4 levels | Back affordance is one gesture away; re-orientation is cheap |
| Tablet | 4–5 levels, with a persistent parent | The parent stays visible, so depth is cheaper |
| Web | Any, if addressable | The URL is the context; users can jump |
| Desktop | Any, with multi-window | Parallel windows remove the need to traverse |
| TV | 2–3 levels maximum | Focus traversal is slow and disorienting at depth |
| Watch | 1–2 levels | The attention budget does not support hierarchy |

The watch and TV budgets are the ones most often violated: a team with a working phone app
assumes the hierarchy ports. It does not — it must be flattened, with detail escalated to
another device (Decision Tree 4).

## Modal versus push

| Use a modal when | Use a push when |
|---|---|
| The task is self-contained and must complete or cancel atomically | The task is part of a browsing hierarchy |
| Interrupting is acceptable and expected (payment, auth) | The user should retain their place in the parent |
| The context must be preserved behind it | The parent context is not needed during the task |

Cross-platform caveat: a modal on one platform may read as a push on another, and the dismissal
gesture differs. The *decision* (modal vs. push) can be shared; the *expression* and the
dismissal affordance belong to the platform.

## Deep links and URL state

Deep linking is a navigation contract on every platform, and it is where cross-platform
navigation diverges most visibly.

| Platform | Deep link mechanism | Requirement |
|---|---|---|
| Apple | Universal links, custom schemes | Handle cold start and warm start; restore the full stack, not just the leaf |
| Android | App links, intents | Handle cold/warm start; honour the system back stack afterwards |
| Web | URLs and routes | Every view addressable; back/forward consistent |
| Cross-platform | Framework router over the platform mechanisms | The router must not bypass platform handling |

The classic defect: a deep link opens the target screen with an empty back stack, so back exits
the app instead of returning to the parent. The fix is to reconstruct the parent hierarchy from
the link, not to disable back.

## Reviewer's navigation checklist

- [ ] Every screen answers "how do I go back?" with a platform-correct affordance
- [ ] Peer destinations are peers (tabs/nav), not stack depth
- [ ] Depth is within the surface's budget (watch and TV especially)
- [ ] Deep links reconstruct the parent hierarchy, not just the leaf
- [ ] Android back handles the full history and plays with system/predictive back
- [ ] Web pushes a history entry per view; back/forward behave
- [ ] Desktop has keyboard navigation and reliable history
- [ ] Modals are used for atomic tasks and dismiss the platform's way
- [ ] Navigation is not unified across platforms where the platforms differ
