# Decision Matrix: Submodule vs Subtree vs Package vs Vendoring

## Comparison Framework

When choosing a code-sharing strategy across repositories, evaluate each option across six dimensions. Score each dimension 0-5 and multiply by the weight.

| Dimension | Weight | Submodule | Subtree | Package Registry | Vendoring |
|-----------|--------|-----------|---------|-----------------|-----------|
| Update frequency tolerance | 3 | ⬜ | ⬜ | ⬜ | ⬜ |
| Consumer count scalability | 2 | ⬜ | ⬜ | ⬜ | ⬜ |
| CI simplicity | 2 | ⬜ | ⬜ | ⬜ | ⬜ |
| Local modification capability | 3 | ⬜ | ⬜ | ⬜ | ⬜ |
| History preservation | 1 | ⬜ | ⬜ | ⬜ | ⬜ |
| Security maintenance overhead | 3 | ⬜ | ⬜ | ⬜ | ⬜ |

## Decision Scenarios

### Scenario A: 3 consumers, weekly updates, dedicated owners
Recommendation: Submodules. The consumer count is manageable, and exact version pinning prevents surprise breakages. Configure branch tracking to simplify updates.

### Scenario B: 15 consumers, daily updates, mature CI
Recommendation: Private package registry. The consumer count exceeds submodule scalability limits (7+). Semantic versioning allows independent update cadences.

### Scenario C: Small utility lib, 2 consumers, needs local patches
Recommendation: Vendoring with update tracking. The dependency is small enough to vendor, and local modifications are a first-class requirement. Maintain VENDOR_VERSION file with upstream diff check in CI.
