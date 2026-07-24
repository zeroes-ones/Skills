# Anti-Rationalization Table

## Purpose
Catalog the cognitive biases that cause developers to skip verification, with counter-strategies.

## Complete Anti-Rationalization Catalog

| Excuse | Bias | Counter-Strategy | Real-World Cost |
|---|---|---|---|
| "The change is obviously correct" | Overconfidence effect | Run the reproduction case anyway. "Obvious" changes have the highest regression rate. | Production outage from a "trivial" null check |
| "I already tested it manually" | Availability heuristic | Manual testing is not reproducible. If it's not automated, it didn't happen. | Bug resurfaces 3 months later, nobody remembers the fix |
| "The CI will catch issues" | Diffusion of responsibility | CI runs generic tests, not the reporter's exact scenario. | CI passes, production fails on reporter's edge case |
| "It's just a one-line change" | Anchoring on LOC | Blast radius is measured in dependents, not lines. | One-line config change takes down auth service |
| "It works on my machine" | Egocentric bias | The reporter's environment is different. Verify in their context. | Fix works locally, fails in production (different Node version) |
| "I'll verify after the release" | Hyperbolic discounting | Post-release bugs cost 10-100x more. Verify now. | Weekend outage because fix was merged Friday, unchecked |
| "The test coverage is high" | McNamara fallacy | Coverage measures lines executed, not behaviors verified. | 95% coverage, 0% behavior verification |
| "Nobody else verifies this thoroughly" | Social proof (misapplied) | The team that verifies catches regressions others miss. | Competitive advantage from fewer production bugs |

## Detection Heuristics
- Commit messages containing "obviously," "trivial," "just," "should work"
- PR comments with no test output or screenshots
- Issues closed within 1 hour of being assigned (no time to verify)
- "Works for me" without follow-up questions about the reporter's environment
