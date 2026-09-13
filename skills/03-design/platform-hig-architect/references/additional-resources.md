# Additional Resources — platform-hig-architect

> Deep knowledge loaded on demand. `SKILL.md` stays lean; extended material lives here and in
> the sibling reference files.

## Reference file map

| File | Covers |
|---|---|
| `convention-matrix.md` | The element-category × platform matrix, the filling procedure and the reviewer's check |
| `platform-families.md` | Apple, Android, Windows, web and cross-platform families: what is governed vs. product-controlled |
| `navigation-conventions.md` | Navigation models, back affordances, depth budgets and deep-link behaviour |
| `gestures-and-input.md` | Gesture vocabulary, WCAG 2.5.1 constraints, and input-modality expectations per surface |
| `adaptive-layout.md` | Size classes, region patterns, container queries, multitasking and density |
| `wearables-and-tv.md` | Reduced surfaces, attention budgets, handoff patterns and the TV focus model |
| `spatial-computing.md` | Headset conventions: placement, gaze, comfort and workspace persistence |
| `platform-accessibility.md` | The platform integration layer beyond WCAG: labels, roles, order, text sizing |
| `cross-platform-strategy.md` | Native vs. adaptive vs. shared, the shared/native boundary, framework caveats, fidelity audit |
| `conformance-audit.md` | The 11-dimension audit, scoring, evidence requirements and report format |
| `deviations.md` | The deviation log format, worked examples, and how to judge a deviation |
| `anti-patterns.md` | Thirteen platform anti-patterns with detection heuristics and a sweep script |
| `error-decoder.md` | Twelve symptoms in long form: mechanism, diagnosis, fix, recurrence guard |
| `sub-skills.md` | When to split the session, and the boundary with adjacent skills |

## Extended example

`examples/backtest/README.md` runs a multi-platform conformance remediation against a stated
scenario and computes the cost of each failure mode arithmetically, with provenance tags.

## Source material

Guidelines change on the platform's release cycle, not on yours — verify the current version
before citing a specific clause or dimension.

| Source | What it governs |
|---|---|
| Apple Human Interface Guidelines | Apple platform conventions, size classes, system affordances, form factors |
| Material Design 3 documentation | Android component, token, navigation and theming guidance |
| Android developer documentation | Back handling, intents, permissions, form-factor adaptation |
| Windows app design guidance | Navigation, pointer/keyboard conventions, window management |
| Platform spatial-computing design guidance | Gaze, placement, depth and comfort conventions |
| Cross-platform framework documentation (Flutter, React Native, Kotlin Multiplatform, .NET MAUI) | Rendering defaults, platform fidelity, navigation handling |
| Platform accessibility documentation (per vendor) | The integration layer: accessibility APIs and expectations |
| CSS Media Queries and Containment specifications | Responsive and container-query behaviour on the web |
| WCAG 2.2 Success Criteria 2.4.7, 2.4.11, 2.5.1, 2.5.8 | Focus visibility, focus appearance, gesture alternatives, target size |

## Verification harness

`scripts/verify-skill.sh` asserts this skill's own invariants: that all six ground rules are
present with their enforcement columns, that the convention matrix and deviation concepts are
encoded, that every form factor in the decision trees has a governing convention, that the
input-modality and system-affordance rules are stated, and that the failure modes and citations
G14 requires are present. Run it before relying on the skill's output.
