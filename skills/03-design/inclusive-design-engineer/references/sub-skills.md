# Sub-Skills

<!-- QUICK: 30s -- when to split into a narrower session -->

| Sub-skill | When to use it | Where it lives |
|---|---|---|
| `semantics` | Choosing between native, adapted and ARIA | `references/native-first.md` — Decision Tree 1, R1 |
| `widget-patterns` | Implementing or fixing a dialog, menu, combobox, tabs | `references/aria-patterns.md`, `references/overlays-and-menus.md` |
| `focus` | Focus order, containment, restoration, visibility | `references/focus-management.md` — R3 |
| `keyboard` | A component's keyboard contract | `references/keyboard-interaction.md` — R5 |
| `announcements` | Status messages, errors and progress not being heard | `references/live-regions.md` — R4 |
| `forms` | Labels, error association, submit states | `references/forms-and-validation.md` |
| `contrast` | Palette and token contrast decisions | `references/contrast-and-colour.md` — R6 |
| `preferences` | Reduced motion, contrast, colour scheme, text scaling | `references/user-preferences.md` |
| `verification` | Recording AT verification properly | `references/verification-with-at.md` — R2 |
| `guards` | Making a fix durable | `references/regression-guards.md` |

## Split when

- **One component is the whole problem.** "Our dialog is broken" is `widget-patterns` plus
  `focus`; it does not need a library-wide pass.
- **The finding is a single class.** A contrast finding is `contrast`; do not re-litigate the
  whole palette in the same session.
- **Verification is the blocker.** If no AT is available, resolve that first (R2) — a session spent
  fixing without the ability to verify produces unverifiable work.
- **The fix turns out to be a design-system change.** Move to `ui-ux-designer` for the component
  architecture, then return to implement.

## Stay whole when

- **A component library is being made accessible by construction.** Semantics, patterns, focus,
  keyboard, announcements, contrast and guards are one coherent piece of engineering; splitting
  them produces a library that is accessible on one axis and broken on another.
- **An audit's findings are being remediated as a batch.** The triage, the shared-source fixes and
  the guards interact — a per-finding approach misses that most findings share one or two causes.

## Adjacent skills, and the boundary

| Neighbour | They own | This skill owns |
|---|---|---|
| `accessibility-auditor` | Finding violations, severity, legal exposure | Fixing them, and proving the fix |
| `accessibility-testing` | The automated gates and CI integration | What the guards should assert |
| `access-tech-developer` | Assistive technology itself | Making the product work with existing AT |
| `ui-ux-designer` | Component architecture and design-system structure | The accessible implementation of that structure |
| `ui-ux-excellence` | General interaction quality and craft | The accessibility half of the same defects |
| `typography-designer` | Type tokens and resize conformance | Accessible text rendering within those tokens |
| `platform-hig-architect` | The platform's accessibility contract per surface | Implementing that contract in components |
| `frontend-developer` | Application implementation | The accessible patterns the implementation follows |

The pattern this skill exists to close: `accessibility-auditor` identifies the violation and
explicitly does not implement the fix. This skill is the owner of the fix — and of the proof and the
guard that keep it fixed.
