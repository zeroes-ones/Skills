# Scale Depth

<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person) → Small (2-10) → Medium (10-50) → Enterprise (50+)

| Dimension | Solo | Small | Medium | Enterprise |
|-----------|------|-------|--------|------------|
| **Repo Structure** | Single repo, `src/` + `lib/` folders | pnpm workspaces + Turborepo, 3-15 packages | Nx/Turborepo + remote caching, 15-100 packages | Nx/Bazel + distributed CI, 100+ packages |
| **Build System** | No orchestration, just `pnpm build` | Turborepo with local caching | Remote caching (Nx Cloud/S3), affected-only CI | Distributed build agents, multi-region caching |
| **Dependency Mgmt** | Single `package.json` | pnpm + syncpack version enforcement | Renovate + automated dep updates | Custom package registry + dependency governance board |
| **Package Boundaries** | No enforcement needed | ESLint import rules | Nx module tags + lint rules | Automated boundary enforcement + architecture fitness functions |
| **Versioning** | `npm version patch` | Changesets with independent versioning | Automated release PRs + changelogs | Semantic-release per package + multi-channel releases |
| **CI/CD** | Build all on push | Affected-only builds | Remote cache + parallel pipelines | Distributed CI with Nx Cloud agents or BuildJet |
| **Developer Experience** | VS Code, single config | Shared ESLint/TS config | VSCode workspace + git hooks | Automated generator scripts for new packages |

### Transition Triggers

| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | 3+ packages sharing code, cross-package PRs weekly | Adopt pnpm workspaces + Turborepo, set up shared configs |
| Small → Medium | >10 packages, CI >15 min, >5 developers | Remote caching, affected-only CI, module boundary enforcement |
| Medium → Enterprise | >100 packages, multi-team, CI >30 min | Distributed CI, architecture governance, automated package scaffolding |
