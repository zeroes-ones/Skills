# Sub-Skills

<!-- QUICK: 30s -- table of deeper dives by topic -->
When the agent identifies a specific monorepo need, drill into the relevant sub-skill rather than reading the full SKILL.md. Each sub-skill has dedicated references, tooling, and checklists.

| Sub-Skill | What It Covers | Quick Command |
|-----------|---------------|---------------|
| **Workspace Configuration** | pnpm workspaces, Yarn workspaces, npm workspaces — `pnpm-workspace.yaml`, hoisting, `workspace:*` protocol | `pnpm list --depth=0 --recursive` |
| **Build Orchestration** | Turborepo `turbo.json` pipelines, Nx task graph, `dependsOn` topology, parallel execution limits | `npx turbo run build --dry-run=json` |
| **Dependency Governance** | Hoisting strategies, syncpack/manypkg enforcement, `pnpm.overrides`, peer dependency resolution, deduplication | `npx syncpack list-mismatches` |
| **Package Boundary Enforcement** | `@nx/enforce-module-boundaries`, ESLint `import/no-restricted-paths`, TypeScript path aliases, circular dependency detection with `dpdm`/`madge` | `npx dpdm --circular --tree=false src/**/*.ts` |
| **CI/CD for Monorepos** | Affected detection (`--filter=[main...HEAD]`), remote caching (Vercel, S3, Nx Cloud), GitHub Actions matrix builds, cache warm/restore | `npx turbo run build --filter=[main...HEAD]` |
| **Versioning & Release** | Changesets workflow, independent vs fixed versioning, `semantic-release` monorepo setup, changelog generation | `npx changeset version` |
| **Monorepo Migration** | Polyrepo → monorepo strategy, `git filter-repo` for history preservation, `git subtree`, gradual adoption risk mitigation | `git filter-repo --path packages/my-lib --to-subdirectory-filter packages/my-lib` |

> **Token-saving rule:** Load sub-skill references on demand. If <!-- DEEP: 10+min -->
debugging cache misses → only read the build orchestration section. If setting up CI → only read the CI/CD section.
