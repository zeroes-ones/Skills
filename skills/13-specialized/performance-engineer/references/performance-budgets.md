# Performance Budgets

### Time Budgets

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | < 2.5s | 2.5s - 4.0s | > 4.0s |
| TBT | < 200ms | 200ms - 600ms | > 600ms |
| FID / INP | < 100ms / < 200ms | 100-300ms / 200-500ms | > 300ms / > 500ms |
| CLS | < 0.1 | 0.1 - 0.25 | > 0.25 |

### Size Budgets

| Resource | Budget (compressed) |
|----------|---------------------|
| JavaScript (critical path) | < 200KB |
| CSS (critical path) | < 50KB |
| Hero images (LCP) | < 500KB |
| Total page weight | < 1.5MB |

### Quantity Budgets

| Metric | Budget |
|--------|--------|
| HTTP requests per page | < 25 |
| DOM nodes | < 1500 |
| Render-blocking resources | < 5 |
| Third-party origins | < 5 |

### CI Enforcement

- **Lighthouse CI**: Run Lighthouse in CI, assert scores against budgets. Fail the PR build if thresholds are exceeded.
- **bundlesize**: Configure per-chunk size limits. Fail if a chunk exceeds its budget.
- **Custom checks**: `webpack-stats-plugin` + GitHub Action that compares bundle sizes against a baseline and posts a comment on the PR.
- **Perf budget notification**: Comment on PRs with before/after comparison tables for bundle size, LCP, and TBT.
