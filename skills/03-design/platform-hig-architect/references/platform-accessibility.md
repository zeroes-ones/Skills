# Platform Accessibility

<!-- STANDARD: 3min -- per-platform accessibility expectations beyond WCAG -->

> **Verification note.** Accessibility APIs and their expected use change with platform releases.
> Confirm specific API names and behaviours against the targeted SDK's documentation and the
> platform's current accessibility guidance.

## Two layers, not one

WCAG is the *interface* layer: contrast, reflow, text spacing, target size, keyboard access.
Each platform adds an **integration layer**: the API surface through which its assistive
technologies reach your UI. A product can pass a WCAG audit and still be unusable with a screen
reader, because the platform's accessibility tree was never populated.

This skill handles the platform contract. WCAG conformance auditing belongs to
`accessibility-auditor`; implementation belongs to `inclusive-design-engineer`.

## The integration layer, per family

| Family | Integration mechanism | What the app must do |
|---|---|---|
| Apple | Accessibility API on views (labels, traits, values, hints) | Give every element a meaningful label, correct traits, and a deliberate order |
| Android | Accessibility node info, content descriptions, semantics | Provide content descriptions, roles, and grouped semantics for composites |
| Web | ARIA and native semantics | Use native elements first; ARIA for what HTML cannot express |
| Windows | UI Automation properties | Expose name, role, value and patterns; support keyboard and screen reader |
| TV | Focus + accessibility tree | Make focus traversal match the accessibility order |
| Spatial | Platform accessibility equivalents for gaze/gesture | Provide non-gesture alternatives and label every element |
| Cross-platform | Framework semantics bridging to the platform API | Verify the bridge emits the platform's properties, not just the framework's |

The cross-platform row is the frequent failure: a framework's `semantics` or `accessibilityLabel`
may map only partially to the platform API, so a framework-level audit passes while the platform
tree is empty. **Verify on the platform's own inspector, not in the framework's debug view.**

## The properties that must be set

| Property | Purpose | Skipped symptom |
|---|---|---|
| Name / label | What the element is | Screen reader reads "button" with no purpose |
| Role / trait | What kind of thing it is | A toggle announced as a button |
| Value | Its current state | A slider with no position |
| Hint / description | What activating it does | The user knows what it is but not what it does |
| Order | Reading and focus sequence | Content read in a nonsensical order |
| Grouping | Composite elements | A card read as eleven unrelated fragments |
| State | Selected, expanded, busy, disabled | Silent state changes |

## Platform text sizing

Every platform lets the user raise the text size globally, and each exposes it differently.

| Requirement | Why |
|---|---|
| Body text uses the platform's text styles, or reproduces their scaling | The user's setting is a platform property; ignoring it fails the requirement (R5) |
| Verified at the platform's largest accessibility size | The failure appears only at the extreme |
| Layout survives the largest size | Fixed containers clip; the largest size is where it breaks |
| Custom fonts declare their scaling | A custom face without scaling opts out of the setting |

This is the platform-level counterpart of WCAG 1.4.4, and it fails for the same reason: `px`-like
absolute sizing that ignores the user's preference.

## Gestures, motion and comfort

| Expectation | Applies to |
|---|---|
| Non-gesture alternatives for gesture-only functions | All touch surfaces (WCAG 2.5.1) |
| Reduced-motion honoured | All surfaces |
| Platform comfort settings honoured | Spatial especially |
| Flash/threshold limits honoured | All surfaces |
| Assistive input (switch, voice control) can complete the primary task | All surfaces |

## Per-surface summary

| Surface | Most-missed expectation |
|---|---|
| Phone | Screen-reader labels on icon-only controls; the assistive gesture set |
| Tablet | Split view with a screen reader; keyboard navigation of custom controls |
| Web | Keyboard access to custom widgets; focus management in SPAs |
| Desktop | Full keyboard coverage; menu and context-menu parity |
| TV | Focus order matches the accessibility order; focus announced |
| Watch | Labels on complication/glance content |
| Spatial | Non-gesture alternatives; every gaze target labelled |
| Cross-platform | Verifying the platform tree, not the framework's semantics |

## The platform accessibility checklist

- [ ] Every interactive element has a name, a role and (where applicable) a value
- [ ] Composite elements are grouped so they are not read as fragments
- [ ] Reading/focus order is deliberate, not source order by accident
- [ ] State changes are announced, not silent
- [ ] Body text honours the platform's text-size setting; verified at the largest size
- [ ] Layout survives the largest text size without clipping
- [ ] Every gesture-only function has a non-gesture alternative (2.5.1)
- [ ] Reduced-motion and comfort preferences honoured
- [ ] Assistive input (switch, voice) can complete the primary task
- [ ] Verified with the platform's own inspector and its screen reader, on the real device
- [ ] For cross-platform: verified on each platform's tree, not the framework's semantics view
