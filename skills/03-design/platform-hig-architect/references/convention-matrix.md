# Convention Matrix

<!-- STANDARD: 3min -- the element-category x platform matrix and how to fill it -->

## What the matrix is for

A multi-platform product makes one decision per element category per surface. Left implicit,
that decision gets made again on every screen — and differently each time, because different
engineers weigh brand, habit and deadline differently. The matrix makes the decision once and
makes it visible.

This is R1. Without it, divergence appears as navigation conflicts and gesture collisions,
which are the most expensive UI properties to change after the fact.

## The categories

| Category | The question it answers |
|---|---|
| Navigation | Tabs, drawer, stack, sidebar — and where the back affordance lives |
| Primary action | Where the dominant action sits on a screen |
| Destructive action | How deletion/removal is confirmed and what gesture triggers it |
| Gestures | What each gesture means (swipe, long-press, pinch, drag, pull) |
| Controls | Which control set renders (system, platform library, custom) |
| Feedback | Progress, toast/snackbar, haptics, inline validation, empty and error states |
| Typography | System text styles vs. brand type, and how resize is honoured |
| Motion | Timing, easing, and reduced-motion behaviour |
| Window/insets | Safe areas, notches, system bars, multi-window behaviour |
| System integration | Permissions, biometrics, share, notifications, deep links, widgets |
| Accessibility | Labels, roles/traits, focus order, gesture alternatives |
| Theming | Light/dark, dynamic colour, platform accent |

## The matrix

Fill one column per shipping surface. "Governed by" names the platform whose convention wins;
"Deviation" records where the product deliberately departs.

| Category | Phone (iOS) | Phone (Android) | Tablet | Web | Desktop | TV | Watch |
|---|---|---|---|---|---|---|---|
| Navigation | Platform tabs + stack | Platform nav + back | Sidebar + detail | Nav bar + breadcrumbs | Menu bar + shortcuts | Focus-based rail | Page-based, shallow |
| Primary action | Platform convention | Platform FAB/action | Region-appropriate | Inline/reflowed | Toolbar/menu | Focused control | Single action |
| Destructive | Swipe + confirm | Long-press + confirm | Same as phone | Explicit confirm | Right-click + confirm | Explicit confirm | Explicit confirm |
| Gestures | Platform set | Platform set | Platform set + pointer | Wheel/keys | Pointer/keys | Remote keys | Crown/swipe |
| Controls | Platform library | Platform library | Platform library | Brand + a11y primitives | Platform library | Platform library | Platform library |
| Feedback | Haptics + toast | Snackbar + haptics | Inline | Inline + toast | Inline | On-screen, focus-anchored | Haptic + minimal |
| Typography | System styles | System styles | System styles | Brand (resize-proven) | System or brand | Larger, 10-foot | System, minimal custom |
| Motion | Platform timing | Platform timing | Platform timing | Brand tokens | Subtle | Restrained | Minimal |
| Window/insets | Safe areas | Insets/edge-to-edge | Split view | Responsive | Resizable | Overscan-safe | Screen bounds |
| System integration | Widgets, deep links | Widgets, intents | Multitasking | PWA/share | Multi-window | Remote, media keys | Complications |
| Accessibility | Platform APIs | Platform APIs | Platform APIs | ARIA + WCAG | Platform APIs | Focus + a11y | Platform APIs |
| Theming | Light/dark + accent | Dynamic colour | Both | CSS + user pref | Both | Both, high contrast | Light/dark |

The content of each cell is the *decision*, not the implementation. It should be short enough
that a reviewer can spot a wrong one at a glance.

## Filling procedure

1. **List surfaces.** One column per shipping surface and form factor. A phone and a tablet for
   the same platform are two columns (R2).
2. **Default each cell to the platform convention.** Start from the platform, not from the brand.
   This inverts the usual instinct and prevents accidental overrides.
3. **Run Decision Tree 1 on the cells where brand presses.** Anywhere the product wants to
   differ, decide deliberately and record it (R3).
4. **Mark system-affordance cells as fixed.** Permissions, biometrics, share and selection are
   never product-controlled; mark them so nobody tries.
5. **Record deviations in the deviation log**, one row per departure, with the cost to learned
   behaviour.
6. **Review the matrix as one artefact.** The value is in seeing all surfaces at once — a
   conflict between two columns is visible here and invisible in separate specs.

## Worked example: a brand-heavy consumer app

The brand team wants a signature gesture and a custom primary action. Filled matrix excerpt:

| Category | iOS | Android | Decision rationale |
|---|---|---|---|
| Navigation | Platform stack + back swipe | Platform stack + system back | **No deviation.** Back is learned; overriding it costs every user on every screen |
| Primary action | Platform convention placement | Platform convention placement | **No deviation.** Placement is muscle memory; the brand expresses itself in the control's styling |
| Gestures — signature | One reserved gesture for the signature feature | Same gesture, platform-consistent trigger | **Deviation, recorded.** Signature feature is the product; documented with the cost that the gesture is no longer available for platform use |
| Destructive | Platform swipe + confirm | Platform long-press + confirm | **No deviation.** Destructive actions must feel the same as the rest of the platform |
| Controls | Brand styling over platform behaviour | Brand styling over platform behaviour | **Partial deviation.** Visual surface is brand; behaviour, hit targets and accessibility come from the platform |

The pattern in the example is the answer to most conflicts: **take the platform's behaviour,
express the brand in the surface.** Behaviour is learned; surfaces are read.

## Anti-patterns in filling the matrix

| Anti-pattern | Why it fails |
|---|---|
| Leaving cells blank | A blank cell is a decision deferred to whoever writes the screen, which is exactly what the matrix prevents |
| Writing implementations instead of decisions | "Uses `NavigationStack`" is an implementation; "platform stack with back swipe" is a decision that survives a framework change |
| Marking brand for every visual cell | Brand everywhere means convention nowhere; the platform's learned affordances must appear somewhere |
| Treating the tablet as the phone column | The tablet has its own conventions and its own multitasking constraints (R2) |
| Not marking system affordances | An engineer will eventually try to style a permission dialogue |
| Building the matrix once | It is a living artefact; a new surface or a platform revision changes it |

## Reviewer's quick check

Before accepting UI work against the matrix, scan for these:

- [ ] Every cell names a convention, not a framework or a control class
- [ ] System-affordance cells are explicitly marked as fixed
- [ ] Every brand-governed cell traces to a Decision Tree 1 outcome
- [ ] Every deviation cell appears in the deviation log with a rationale
- [ ] Each form factor has its own column
- [ ] Navigation conflicts between columns are resolved, not merely noted
