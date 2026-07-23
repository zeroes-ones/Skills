# Dependency Management & Package Architecture

Deep dives on dependency strategies, package boundaries, versioning, and migration are in **[references/monorepo-patterns.md](references/monorepo-patterns.md)**:

| Section | What's Covered |
|---------|---------------|
| **Dependency Management** | Hoisting strategies (auto vs strict), version consistency tools (syncpack, manypkg), peer dependency resolution, depcheck/audit commands |
| **Code Sharing & Boundaries** | Barrel exports pattern, package boundary enforcement (ESLint import rules, module tags), circular dependency detection (madge, dpdm) |
| **Version Management** | Independent vs fixed versioning, Changesets workflow with CLI commands, semantic-release in monorepos, release pipeline summary |
| **Migration Path** | Polyrepo→monorepo strategy, big-bang (subtree merge), gradual adoption step-by-step, git history preservation, risk mitigation |
| **Developer Experience** | Local dev setup, shared ESLint/TS config, VSCode workspace config, Git hooks (Husky + lint-staged), editor integration |

**Quick Reference:**
- **Hoisting:** `"hoist": true` in `.npmrc` unless you have conflicting peer deps
- **Version sync:** `syncpack list-mismatches` in CI — fail on any discrepancy
- **Circular deps:** `madge --circular packages/` — zero tolerance policy
- **New package:** `pnpm exec changeset` → describe change → commit → CI auto-opens Release PR
### Git Hooks — Husky + lint-staged

```bash
# Install
pnpm add -Dw husky lint-staged
pnpm exec husky init

# .husky/pre-commit
pnpm exec lint-staged

# .husky/commit-msg
pnpm exec -- commitlint --edit $1

# package.json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yaml}": [
      "prettier --write"
    ]
  }
}

# commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'scope-enum': [2, 'always', ['web', 'api', 'ui', 'utils', 'types', 'tools', 'release']],
  },
};
```


**What good looks like:** `npm run build -- --filter=[changed]` completes in under 3 minutes. Remote cache hit rate > 70%. CI pipeline runs only affected projects. Developer onboarding to add a new package is documented and takes < 30 minutes.
