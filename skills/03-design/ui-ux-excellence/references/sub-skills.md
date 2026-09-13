# Sub-Skills

<!-- QUICK: 30s -- when to split into a narrower session -->

| Sub-skill | When to use it | Where it lives |
|---|---|---|
| `heuristic-evaluation` | A flow or product needs scoring and findings | `references/heuristics.md`, `references/scorecard.md` |
| `state-coverage` | Screens are missing states, or a state audit is wanted | `references/state-coverage.md` — R2 |
| `error-experience` | Errors read badly, or prevention is the question | `references/error-experience.md` — Decision Tree 1 |
| `empty-states` | First-run, no-results or permission states need design | `references/empty-states.md` |
| `perceived-performance` | The product feels slow with healthy server metrics | `references/perceived-performance.md` — R4 |
| `motion-discipline` | Transitions feel wrong, or motion needs a budget | `references/motion-discipline.md` — R3 |
| `forms-feedback` | Validation timing, input ergonomics, submit behaviour | `references/forms-and-feedback.md` |
| `cognitive-load` | Decision count, choice architecture, recall | `references/cognitive-load.md` |
| `measurement` | HEART, SUS, task success, instrumentation | `references/measurement.md` — R5 |

## Split when

- **One class dominates.** "Our errors are unhelpful" is `error-experience`; it does not need a
  full heuristic scorecard.
- **The request is a single state audit.** Enumerating missing states across screens is its own
  bounded session (Decision Tree 2).
- **Measurement is the blocker.** If no baseline exists, define and instrument it before changing
  anything (R5) — a separate session.
- **A finding needs user data to resolve.** Stop and route to `ux-researcher`; a heuristic
  evaluation cannot establish what users want.

## Stay whole when

- **"Is this good enough to ship?"** That question needs the task list, the heuristic scoring,
  the state gate and the measurement plan together; any subset gives a misleading verdict.
- **A product is being prepared for a launch.** Run the full workflow; a partial pass leaves the
  launch gates (states, errors, waits) unverified.

## Adjacent skills, and the boundary

| Neighbour | They own | This skill owns |
|---|---|---|
| `ui-ux-designer` | The design system, tokens and component specs | Whether the resulting interface is usable, and the evidence for it |
| `ux-researcher` | Study design, recruitment, and the data from users | Converting research findings into scored, prioritised interface defects |
| `ux-writer` | Interface copy as a discipline | Flagging that copy is failing, and the criteria it fails |
| `typography-designer` | The type system and its conformance | Reading-comfort findings that are not typographic defects |
| `platform-hig-architect` | Which platform convention governs | Craft quality within a platform-correct interface |
| `accessibility-auditor` | WCAG conformance and legal exposure | Usability defects, which overlap but are a separate standard |
| `inclusive-design-engineer` | Accessible implementation | The usability half of the same fix |
| `product-analyst` | The data model, dashboards and analysis | The metric definitions the analysis must serve |
| `product-manager` | Priority and product goals | The evidence that makes priority arguable |

The pattern: `ui-ux-designer` builds the interface; this skill judges it, with evidence, and
converts the judgement into measurable outcomes with owners.
