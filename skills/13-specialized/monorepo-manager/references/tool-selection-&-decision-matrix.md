# Tool Selection & Decision Matrix

### Comparison Across 8 Dimensions

| Tool | Build Speed | Caching Capability | Task Graph | Plugin Ecosystem | Learning Curve (1–10) | Community Size | Enterprise Readiness | Best For |
|------|-------------|-------------------|------------|------------------|-----------------------|----------------|---------------------|----------|
| **Turborepo** | Very Fast | Local + Remote (Vercel, S3) | Auto via `dependsOn` | Minimal (growing) | 3 | Very Large | Good | JS/TS teams wanting fast setup + remote cache |
| **Nx** | Fast | Local + Remote (Nx Cloud) | Advanced (explicit + implicit) | Extensive (200+) | 6 | Large | Excellent | Large monorepos needing generators, boundaries, DTE |
| **pnpm workspaces** | N/A (install only) | None (no build cache) | None (no orchestrator) | N/A | 2 | Very Large | Partial | Package management only; pair with Turborepo/Nx |
| **Bazel** | Fastest (hermetic) | Local + Remote + RE | Full DAG | Polyglot (Java, Go, TS, etc.) | 9 | Medium | Excellent | Polyglot repos, large scale, strict hermeticity |
| **Lerna** | Slow (legacy) | None (native) | Basic (`--since`) | Minimal | 3 | Large (legacy) | Low | Publishing + changelogs when paired with Turborepo/Nx |
| **Rush** | Fast | Local + Remote (Rush Cloud) | Custom (Rush plugins) | Moderate | 7 | Medium | Excellent | Enterprise .NET/TS monorepos needing policy enforcement |

### Decision Tree

```
Is your codebase 100% JavaScript/TypeScript?
├── Yes
│   ├── Fewer than 10 packages, simple dependency graph?
│   │   ├── Yes → pnpm workspaces alone (no build orchestrator needed)
│   │   └── No → Want the simplest setup with fast caching?
│   │       ├── Yes → Turborepo + pnpm workspaces
│   │       └── No → Need code generation, module boundaries, distributed builds?
│   │           ├── Yes → Nx + pnpm workspaces
│   │           └── No → Vercel ecosystem? → Turborepo
│   └── No (polyglot: Java + Go + TS + Python)
│       ├── Need hermetic builds and remote execution?
│       │   ├── Yes → Bazel
│       │   └── No → Nx (supports multiple languages via executors)
│
Is your org > 500 engineers, strict dependency governance required?
├── Yes → Rush (Microsoft-scale policy enforcement)
└── No → Use Turborepo or Nx

Are you migrating from Lerna?
├── Keep Lerna for publish/changelog, add Turborepo for builds
└── Full migration → Remove Lerna, use Turborepo + changesets
```

### When pnpm Workspaces Alone Is Enough

- **Small monorepos** (3–8 packages) with shallow dependency graphs
- **No need for caching** — build times are already < 30 seconds
- **No CI optimization needed** — full rebuilds are fast enough
- **Simple run scripts** — `pnpm --filter` and `pnpm -r` suffice
- **Example**: design system monorepo with 6 icon/component/theme packages

### When You Need More Than pnpm Workspaces

- Build times > 2 minutes locally or > 10 minutes in CI
- Packages share dependencies that cause rebuild cascades
- Need remote caching so CI and devs don't duplicate builds
- Need task orchestration (build deps before consumers, parallel tests)
- Need code generation for packages, components, configs
- Need dependency boundary enforcement (apps → libs, not libs → apps)
- **Rule of thumb**: if you're writing shell scripts to orchestrate build order, you need Turborepo or Nx.
