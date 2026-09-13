# Sub-Skills

<!-- QUICK: 30s -- when to split into a narrower session -->

| Sub-skill | When to use it | Where it lives |
|---|---|---|
| `convention-matrix` | A multi-platform product needs its governing conventions decided | `references/convention-matrix.md` — R1 |
| `platform-family` | One family's conventions need reasoning through | `references/platform-families.md` |
| `navigation` | Navigation model or back affordance is the question | `references/navigation-conventions.md` |
| `gestures-input` | Gesture meanings or input modalities need resolution | `references/gestures-and-input.md` — R4 |
| `adaptive-layout` | Size classes, split view, foldables, container queries | `references/adaptive-layout.md` — R2 |
| `reduced-surface` | Watch, TV or spatial conventions | `references/wearables-and-tv.md`, `references/spatial-computing.md` |
| `cross-platform-strategy` | Native vs. adaptive vs. shared, framework caveats | `references/cross-platform-strategy.md` |
| `platform-accessibility` | The platform's accessibility contract | `references/platform-accessibility.md` — R6 |
| `conformance-audit` | Auditing a surface against its platform guidance | `references/conformance-audit.md` |
| `deviation-log` | Recording or reviewing convention departures | `references/deviations.md` — R3 |

## Split when

- **One dimension dominates.** "Make the TV build navigable" is `reduced-surface`; it does not
  need the cross-platform strategy review.
- **A single platform family is in scope** and the question is its conventions, not the mapping.
  Route the depth to `apple-hig-expert` or `material-design-expert` and keep this skill's role to
  the matrix cell.
- **A platform version's guidance is unknown.** Resolve the specific documented value first
  (Anti-Hallucination); do not design on a recalled dimension.
- **The audit is the request.** A conformance audit is its own deliverable; do not restructure
  the UI inside it.

## Stay whole when

- **A product is being prepared for multiple platforms for the first time.** The matrix, the
  adaptivity strategy, the size-class design and the input pass are one coherent piece of work;
  splitting them produces a matrix nobody follows.
- **A platform review has failed.** The finding is usually a convention the product misunderstood,
  which requires the matrix and the deviation log to correct together.

## Adjacent skills, and the boundary

| Neighbour | They own | This skill owns |
|---|---|---|
| `apple-hig-expert` | Deep Apple HIG, Liquid Glass, Apple platform detail | Which Apple conventions bind, and the deviation list |
| `material-design-expert` | Deep Material 3 components and tokens | Which Android conventions bind, and the deviation list |
| `ui-ux-designer` | The design system and component library | How components render and behave per platform |
| `ui-ux-excellence` | Heuristic evaluation and interaction craft, platform-agnostic | The platform-correctness baseline that craft sits on |
| `typography-designer` | The type system and resize conformance | Which platform text styles satisfy the roles |
| `inclusive-design-engineer` | Accessible implementation | The platform accessibility *contract* per surface |
| `accessibility-auditor` | WCAG conformance and legal exposure | Platform-specific expectations beyond WCAG |
| `mobile-developer` | Implementation on mobile | The conventions the implementation must honour |

The pattern: the platform specialists own **depth on one platform**; this skill owns the
**decision of which convention governs**, and the record of where the product departs.
