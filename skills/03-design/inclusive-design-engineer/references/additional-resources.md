# Additional Resources — inclusive-design-engineer

> Deep knowledge loaded on demand. `SKILL.md` stays lean; extended material lives here and in the
> sibling reference files.

## Reference file map

| File | Covers |
|---|---|
| `native-first.md` | The native → adapted → hidden-control → ARIA hierarchy, the element map, and the mechanical ARIA rules |
| `aria-patterns.md` | Per-widget contracts: dialog, menu, combobox, tabs, disclosure, tooltip, toast, and where each state attribute belongs |
| `focus-management.md` | Focus visibility, focus order, roving tabindex, containment, restoration, and route changes |
| `keyboard-interaction.md` | Universal key expectations, the two focus models, per-widget key contracts, traps, and shortcuts |
| `live-regions.md` | The create-with-content trap, politeness, atomicity, over-announcement, and progress |
| `forms-and-validation.md` | Labels, error association, announcement, validation timing, and submit behaviour |
| `overlays-and-menus.md` | The four-part overlay contract and each overlay component's specific defects |
| `contrast-and-colour.md` | Ratio computation, thresholds, what actually fails, text over images, and colour-independence |
| `user-preferences.md` | Reduced motion, increased contrast, colour scheme, text scaling, and the preference test matrix |
| `verification-with-at.md` | The combination set, the verification protocol, what to record, and honest "unverified" |
| `regression-guards.md` | Outcome-versus-implementation assertions, the token guard, and proving a guard fails |
| `anti-patterns.md` | Eighteen implementation anti-patterns with detection heuristics and a sweep script |
| `error-decoder.md` | Sixteen symptoms in long form: mechanism, diagnosis, fix, recurrence guard |
| `sub-skills.md` | When to split the session, and the boundary with adjacent skills |

## Extended example

`examples/backtest/README.md` runs a remediation programme against a stated scenario and computes the
cost of each failure mode arithmetically, with provenance tags.

## Source material

Standards and specifications this skill implements. Confirm the current version before citing a
specific clause, role or attribute pairing.

| Source | What it governs |
|---|---|
| WAI-ARIA specification | Roles, states, properties, live regions, and permitted attribute pairings |
| ARIA Authoring Practices Guide (APG) | Per-widget keyboard contracts, focus rules and implementation patterns |
| WCAG 2.2 | Conformance criteria: contrast, focus appearance, target size, error handling, resize, reflow |
| HTML Living Standard (semantics, form elements) | The native elements and behaviours this skill prefers |
| `prefers-reduced-motion` media query | Honouring the motion-comfort preference |
| `prefers-contrast` media query | Honouring the contrast preference |
| `prefers-color-scheme` media query | Respecting the user's theme choice |
| Platform accessibility API documentation | Accessible names, roles, states and focus in native components |
| `inert` attribute / modal element specifications | Making background content unreachable to keyboard and AT |
| Assistive-technology vendor documentation | AT/browser support differences, per version |

## Verification harness

`scripts/verify-skill.sh` asserts this skill's own invariants: that all six ground rules are present
with enforcement columns, that native-first and the four-part overlay contract are encoded, that
focus containment/restoration, live-region timing, error association, colour-independence and
contrast-in-tokens are stated, that user preferences and text scaling are covered, and that the AT
verification protocol and the guard-proving procedure are present. Run it before relying on the
skill's output.
