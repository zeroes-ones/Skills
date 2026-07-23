# Build System & CI/CD

Deep dives on task orchestration, caching architecture, and CI/CD pipelines are in **[references/monorepo-tooling.md](references/monorepo-tooling.md)**:

| Section | What's Covered |
|---------|---------------|
| **Task Orchestration** | Turborepo pipeline config, Nx task executor, pnpm workspace protocols, parallel vs sequential execution strategies |
| **Caching Architecture** | Local + remote caching (Nx Cloud, Turborepo Remote Cache), hash computation (inputs/outputs), cache invalidation rules, what to cache/not cache |
| **CI/CD** | Affected detection (build only what changed), GitHub Actions pipeline with remote caching, remote cache strategies (S3, GCS), CI cache optimization, parallel pipeline strategies (fan-out per package) |

**Quick Reference:**
- **Local dev:** `turbo dev --filter=@myorg/web` — runs only web + dependencies
- **CI affected:** `turbo build --filter=[origin/main...HEAD]` — builds only changed packages
- **Remote cache:** Cut CI times 60-90% with shared read/write cache across CI runs
