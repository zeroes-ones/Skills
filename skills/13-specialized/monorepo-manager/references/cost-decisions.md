# Cost-Effective Decision Table

| Decision | Free/Cheap Option | Paid Upgrade | When to Upgrade |
|----------|------------------|--------------|-----------------|
| Package manager | pnpm workspaces (free) | — | pnpm is already the best free option |
| Build orchestration | Turborepo (free OSS) | Nx Cloud or Turborepo Remote Cache ($200-$500/mo) | >5 developers, >10 packages, CI times >15 min |
| Remote cache | Local-only or S3 bucket ($1-5/mo) | Vercel Remote Cache or Nx Cloud ($200/mo+) | >5 developers sharing cache or distributed CI |
| Dependency management | Renovate (free OSS) + syncpack (free) | — | Free options are sufficient for most teams |
| Code generation | Plop or Hygen (free OSS) | Nx generators (included) | Already using Nx; otherwise Plop is fine |
| CI parallelization | GitHub Actions matrix (free for public) | BuildJet ($0.004/min) or Nx Cloud agents | Private repos with >10 min CI or need distributed execution |
| Dependency graph visualization | `nx graph` or `turbo run build --graph` (free) | Nx Cloud dependency insights | Need historical trend data or team-level views |

**Annual monorepo tool budget:** MVP: $0 (don't use one). Growth: $0-3K (CI minutes). Scale: $5K-30K (remote cache + CI).
