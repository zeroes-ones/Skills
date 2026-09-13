# Adaptive Layout

<!-- STANDARD: 3min -- size classes, container queries, foldables and multitasking -->

> **Verification note.** Size-class APIs and window-management behaviour differ per platform and
> version. Confirm the specific APIs against the targeted SDK's documentation.

## The governing principle

**Design against available size and input, never against device names.** Device-name breakpoints
("iPad", "phone") break the moment a form factor changes — and form factors now change at
runtime. Foldables unfold, tablets enter split view, windows resize, and a phone gains a
keyboard. The layout must respond to the size it actually has.

The failure this prevents is R2: a tablet layout that is a stretched phone, or a split-view
layout that breaks at the smallest split because it was designed at the largest screen.

## The axes of adaptation

Layout responds to four independent things:

| Axis | Varies with | Affects |
|---|---|---|
| Available width | Window/screen size, split view | Number of regions, columns, measure |
| Available height | Orientation, keyboard presence | Vertical density, scrolled vs. fixed regions |
| Input | Pointer, keyboard, remote, gaze | Focus model, hover, hit targets, shortcuts |
| Multitasking | Split view, stage manager, free-form windows | The *smallest* size the layout must survive |

The fourth axis is the one teams forget. A tablet in split view is narrower than a phone in
landscape; a layout designed at full-screen tablet width must still work there.

## Size classes

Most platforms express available space as a coarse class rather than a device identity.

| Configuration | Typical class | Layout |
|---|---|---|
| Phone portrait | Compact width | Single column; primary action thumb-reachable |
| Phone landscape | Compact height, regular width | Single column, reduced vertical chrome |
| Small tablet / large phone | Regular width | Two regions or a wider measure |
| Tablet / desktop | Regular both | Multi-region: sidebar + detail, or grid |
| Split view (narrow half) | Compact width on a tablet | **Must fall back to the phone layout** |
| Foldable, folded | Compact | Phone layout |
| Foldable, unfolded | Regular | Tablet layout, at runtime |

The split-view row is the crucial one: the same device produces two different size classes, so
device-name breakpoints cannot work. Design the transitions, not the endpoints.

## Region patterns

| Available width | Pattern | Notes |
|---|---|---|
| Narrow | Single column, stack navigation | Detail replaces list |
| Medium | Wide single column, or list + collapsed detail | Increase measure rather than adding a region prematurely |
| Wide | Sidebar/rail + list + detail | Persistent parent; detail never replaces context |
| Very wide | Add a supplementary region or cap the measure | Do not stretch body text to 200 characters |

The "very wide" row matters for web and desktop: the correct response to more width is not always
more text per line. Cap the reading measure (see `typography-designer`) and use the extra width
for structure.

## Container queries versus media queries

| Mechanism | Responds to | Use for |
|---|---|---|
| Media query | Viewport/window | Page-level structure |
| Container query | The component's own container | Component layout independent of where it sits |

A component that must look right in a sidebar, a modal and a full page cannot use media queries —
its viewport says nothing about its own width. Container queries make components genuinely
reusable across regions, which is what multi-region layouts require.

The practical rule: **page structure uses viewport queries; components use container queries.**
A component using viewport queries is coupled to its page, and will break the first time it is
reused in a different region.

## Multitasking and window management

| Surface | Behaviour to handle |
|---|---|
| Tablet split view | Two apps side by side; either half can be narrow |
| Slide-over | The app can be temporarily narrowed further |
| Foldable | Runtime size change across the fold; continuity of state |
| Desktop windows | Free resize, snap, maximise, multi-window, state restore |
| Web | Browser resize, zoom, print/screen-reader reflow |

Rules:

1. **Verify at the smallest supported size, not the largest.** The layout that fails is always
   the narrow one.
2. **Preserve state across a size change.** A foldable unfolding, a window resizing, or a tablet
   entering split view must not reset scroll position, selection or in-progress input.
3. **Never lock orientation to avoid the problem.** Locking landscape on a tablet prevents the
   app from being used alongside another, which is a convention violation.
4. **Test on hardware.** An emulated split view with a mouse does not reveal the layout failure
   a real split reveals.

## Density and the wide case

More width does not mean more content per line or more content per row. The knobs:

| Knob | Narrow | Wide |
|---|---|---|
| Columns | 1 | 2–3 for cards/grids; 1 for prose |
| Reading measure | Full width | Capped (about 45–75 characters) |
| Region count | 1 | 2–3 with persistent parents |
| Row density | Comfortable | Can increase, never below the legibility floor |
| Navigation | Replacement (push) | Persistent (sidebar/rail) |

The most common wide-layout defect is uncapped prose: a 1600px window with a single text column
that is 200 characters wide is unreadable regardless of how much space it "uses".

## The adaptive layout checklist

- [ ] Layout responds to available size and input, not device identity (R2)
- [ ] Both size classes designed, plus the transitions between them
- [ ] Verified at the smallest multitasking size, not the largest screen
- [ ] Split view, slide-over, folded and unfolded states all verified
- [ ] State preserved across size changes (scroll, selection, input)
- [ ] Page structure uses viewport queries; components use container queries
- [ ] Prose measure capped on wide layouts
- [ ] Pointer and keyboard affordances appear when input supports them
- [ ] Orientation not locked to avoid adaptation
- [ ] Tested on real hardware, including a real split view
