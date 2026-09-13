# Additional Resources — ui-ux-excellence

> Deep knowledge loaded on demand. `SKILL.md` stays lean; extended material lives here and in the
> sibling reference files.

## Reference file map

| File | Covers |
|---|---|
| `heuristics.md` | The ten heuristics with scoring criteria, evidence requirements and common false positives |
| `scorecard.md` | The scorecard template, the impact × frequency severity model, the ship gate, and the trend series |
| `cognitive-load.md` | Decision counting, choice architecture, recognition over recall, and where load hides |
| `state-coverage.md` | The full state taxonomy (13 states) with patterns, the state matrix, and the seven-step review |
| `error-experience.md` | The three obligations (name, remedy, preservation), prevention mechanisms, and error copy |
| `perceived-performance.md` | The duration bands, technique ranking, skeletons, optimistic UI, and context preservation |
| `motion-discipline.md` | What motion is for, what must not animate, budgets, easing, and reduced motion |
| `empty-states.md` | The four kinds of empty, the anatomy of a good one, and variant copy that works |
| `forms-and-feedback.md` | Validation timing, input ergonomics, submit behaviour, and multi-step progress |
| `measurement.md` | HEART, SUS, task success, instrumentation, attribution and reporting |
| `anti-patterns.md` | Eighteen patterns with detection heuristics and a sweep script |
| `error-decoder.md` | Fifteen symptoms in long form: mechanism, diagnosis, fix, recurrence guard |
| `sub-skills.md` | When to split the session, and the boundary with adjacent skills |

## Extended example

`examples/backtest/README.md` runs a quality remediation against a stated scenario and computes the
cost of each failure mode arithmetically, with provenance tags.

## Source material

Standards and references this skill draws on. Thresholds and band guidance are conventions derived
from collected data; verify the current version before citing a specific figure.

| Source | What it governs |
|---|---|
| Nielsen's ten usability heuristics | The heuristic set, clauses and their application |
| ISO 9241-11 | The usability definition: effectiveness, efficiency, satisfaction |
| HEART framework | The signal taxonomy for choosing experience metrics |
| System Usability Scale (Brooke) and interpretation guidance | Perceived-usability measurement and score bands |
| Nielsen Norman Group perceived-performance thresholds | The 0.1s / 1s / 10s responsiveness bands |
| Severity-rating guidance for usability findings | Impact × frequency severity modelling |
| Web Vitals documentation | Interaction responsiveness and layout-shift measurement |
| WCAG 2.2 — 1.4.4, 1.4.10, 1.4.12, 2.3.3, 3.3.1, 3.3.3, 3.3.4 | Resize, reflow, text spacing, motion, and error prevention/recovery/suggestion |
| `prefers-reduced-motion` media query specification | Honouring the motion-comfort preference |
| CSS transitions and compositor-friendly property guidance | Which properties can be animated without jank |

## Verification harness

`scripts/verify-skill.sh` asserts this skill's own invariants: that all six ground rules are present
with enforcement columns, that the ten heuristics are enumerated with evidence requirements, that
the state taxonomy and severity model are encoded, that perceived-performance bands and
reduced-motion handling are stated, and that the measurement instruments and the
evidence-before-opinion discipline are present. Run it before relying on the skill's output.
