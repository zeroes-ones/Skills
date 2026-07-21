## Dependency Management

### Hoisting Strategies

| Strategy | Package Manager | Behavior | Phantom Deps? | Disk Usage |
|----------|----------------|----------|---------------|------------|
| **Strict** | pnpm | Content-addressable store, nested `node_modules` via symlinks | ❌ No | Lowest |
| **Hoisted** | npm, Yarn Classic | All deps flat in root `node_modules` | ✅ Yes | Highest |
| **Flexible** | Yarn Berry (PnP) | Virtual filesystem via `.pnp.cjs` | ❌ No (configurable) | Low |

**Phantom dependencies** — when a package can import a dependency it didn't declare. pnpm's strict mode prevents this entirely. Example:

```bash
# This works in npm/Yarn Classic but breaks in pnpm — BAD!
# apps/web/src/api.ts
import { something } from 'dep-only-in-ui-package';  // works in npm, breaks in pnpm
```

**Always use pnpm for new monorepos.** The phantom dependency protection alone is worth the switch.

### Version Consistency Tooling

#### syncpack Configuration

```jsonc
// .syncpackrc.json
{
  "versionGroups": [
    {
      "label": "React must be 18.x across all packages",
      "packages": ["**"],
      "dependencies": ["react", "react-dom"],
      "pinVersion": "^18.2.0"
    },
    {
      "label": "TypeScript must be 5.x",
      "packages": ["**"],
      "dependencies": ["typescript"],
      "pinVersion": "^5.3.0"
    },
    {
      "label": "Internal packages must use workspace protocol",
      "packages": ["**"],
      "dependencies": ["@myorg/**"],
      "dependencyTypes": ["dev", "prod"],
      "isBanned": true,
      "banMessage": "Use workspace:* for @myorg internal dependencies"
    }
  ],
  "semverGroups": [
    {
      "label": "All React ecosystem must use same range type",
      "packages": ["**"],
      "dependencyTypes": ["prod"],
      "range": "^"
    }
  ]
}
```

```bash
# Check for version mismatches
pnpm syncpack list-mismatches

# Fix mismatches automatically
pnpm syncpack fix-mismatches

# In CI: lint only, don't auto-fix
pnpm syncpack lint
```

#### manypkg — Lightweight Alternative

```bash
# Install
pnpm add -Dw @manypkg/cli

# In package.json
{
  "scripts": {
    "lint:repro": "manypkg check"
  }
}
```

#### pnpm Overrides

```jsonc
// root package.json
{
  "pnpm": {
    "overrides": {
      "react": "^18.2.0",
      "next": "^14.0.0",
      // Force a single version of a transitive dependency
      "semver": "^7.5.4"
    },
    "peerDependencyRules": {
      "allowedVersions": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0"
      }
    }
  }
}
```

### Peer Dependency Resolution

```jsonc
// packages/ui/package.json — DECLARE PEER DEPS!
{
  "name": "@myorg/ui",
  "peerDependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "devDependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
```

With pnpm, enable strict peer dep checking:
```yaml
# .npmrc
strict-peer-dependencies=true
auto-install-peers=true
```

### Dependency Audit Commands

```bash
# Why does this package depend on X?
pnpm why react
pnpm why --recursive typescript

# List dependency tree with depth limit
pnpm list --depth=3 --filter=@myorg/web

# Find duplicate versions
pnpm list -r --depth=1 | grep "react@" | sort | uniq -c

# Visualize dependency graph (requires graphviz)
pnpm list --depth=5 --json | pnpx dependency-tree --output graph.html

# Check for outdated dependencies across all packages
pnpm outdated -r

# Find packages that depend on a specific internal package
pnpm ls -r --filter=@myorg/utils --depth=0
```

## Code Sharing & Package Boundaries

### Barrel Exports Pattern

```typescript
// packages/ui/src/index.ts — PUBLIC API
export { Button } from './button/Button';
export { Card, CardHeader, CardBody } from './card';
export { useTheme } from './theme/hooks';

// packages/ui/src/button/index.ts — internal barrel
export { Button } from './Button';
export type { ButtonProps } from './types';
```

**Why barrels matter in monorepos**: They define the public contract. If `packages/utils` exports `{ add, subtract }` from `index.ts`, consumers import from `@myorg/utils` — never from `@myorg/utils/src/math/add`. Internal refactoring (renaming files, splitting modules) doesn't break consumers.

### Enforcing Package Boundaries

#### Nx `enforce-module-boundaries`

```jsonc
// .eslintrc.json (root)
{
  "rules": {
    "@nx/enforce-module-boundaries": [
      "error",
      {
        "enforceBuildableLibDependency": true,
        "allow": [],
        "depConstraints": [
          {
            "sourceTag": "scope:shared",
            "onlyDependOnLibsWithTags": ["scope:shared"]
          },
          {
            "sourceTag": "scope:ui",
            "onlyDependOnLibsWithTags": ["scope:shared", "scope:ui"]
          },
          {
            "sourceTag": "scope:app",
            "onlyDependOnLibsWithTags": ["scope:shared", "scope:ui", "scope:api"]
          }
        ]
      }
    ]
  }
}
```

Tag each package:
```jsonc
// packages/ui/package.json { "nx": { "tags": ["scope:ui"] } }
// apps/web/package.json { "nx": { "tags": ["scope:app"] } }
// packages/utils/package.json { "nx": { "tags": ["scope:shared"] } }
```

#### ESLint `import/no-restricted-paths`

```jsonc
// apps/web/.eslintrc.json
{
  "rules": {
    "import/no-restricted-paths": [
      "error",
      {
        "zones": [
          // apps/web cannot import from other apps
          { "target": "./src", "from": "../apps", "message": "Apps cannot import from other apps" },
          // apps/web cannot import from packages/internal
          { "target": "./src", "from": "../packages/internal", "message": "Apps cannot import internal packages" }
        ]
      }
    ]
  }
}
```

#### TypeScript Path Restrictions

```jsonc
// packages/ui/tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "@myorg/utils": ["../../packages/utils/src"],  // allowed
      "@myorg/apps/*": []  // not accessible (empty array = no resolution)
    }
  }
}
```

### Circular Dependency Detection

```bash
# dpdm — Dependency graph with cycle detection
pnpm add -Dw dpdm
dpdm --circular packages/ui/src/index.ts

# Madge — Visual circular dependency detection
pnpm add -Dw madge
madge --circular --extensions ts,tsx packages/
madge --image graph.png packages/ui/src/

# Nx — Built-in circular dependency check
nx graph --focus=@myorg/ui
# Look for cycles in the interactive graph

# Turborepo — check with graph output
turbo run build --graph=graph.html
# Open graph.html and look for cycles
```

**Rule**: A package should NEVER import from a package that imports from it, directly or transitively. Caught early, circular deps are easy to fix. Caught late, they require major refactors.

## CI/CD for Monorepos

### Affected Detection

```bash
# Turborepo — build only what changed vs main
turbo build --filter=[main...HEAD]

# Turborepo — filter by specific package + dependents
turbo build --filter=@myorg/utils...  # includes dependents
turbo build --filter=...@myorg/utils  # includes dependencies

# Nx — affected commands
nx affected:build --base=main
nx affected:test --base=main
nx affected:lint --base=main

# Nx — graph affected tasks
nx affected:graph --base=main

# pnpm — manual affected (no cache, but works)
pnpm --filter=[origin/main...HEAD] run build
```

### Complete CI Pipeline — GitHub Actions

```yaml
# .github/workflows/ci.yml
name: Monorepo CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true

env:
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  TURBO_TEAM: ${{ vars.TURBO_TEAM }}
  TURBO_REMOTE_CACHE: true

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Required for affected detection

      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      # Lint only affected packages
      - run: pnpm lint --filter=[main...HEAD]

      # Type-check only affected packages
      - run: pnpm type-check --filter=[main...HEAD]

      # Build affected packages + dependents
      - run: pnpm build --filter=[main...HEAD]...

  test:
    runs-on: ubuntu-latest
    needs: quality
    strategy:
      fail-fast: false
      matrix:
        # Split CI into parallel test jobs per app/package
        package:
          - --filter=@myorg/web
          - --filter=@myorg/api
          - --filter=@myorg/ui
          - --filter=@myorg/utils
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm test ${{ matrix.package }}

  e2e:
    runs-on: ubuntu-latest
    needs: [quality, test]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm e2e --filter=[main...HEAD]...

  size-limit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm build --filter=@myorg/affected...
      - run: pnpm size-limit
```

### Remote Caching Strategies

| Storage | Turborepo | Nx | Cost | Best For |
|---------|-----------|-----|------|----------|
| **Vercel Remote Cache** | Built-in | — | Free tier + paid | Vercel users |
| **Nx Cloud** | — | Built-in | Free tier + paid | Nx users |
| **S3 / GCS** | Custom server | Custom runner | Storage costs | Self-hosted/air-gapped |
| **GitHub Actions Cache** | turborepo-remote-cache action | community actions | Free (GH plan) | GH-only teams |

Self-hosted S3 remote cache for Turborepo:
```bash
# Using turborepo-remote-cache server
# https://github.com/ducktors/turborepo-remote-cache
docker run -d \
  -e STORAGE_PROVIDER=s3 \
  -e AWS_ACCESS_KEY_ID=... \
  -e AWS_SECRET_ACCESS_KEY=... \
  -e S3_BUCKET=my-turbo-cache \
  ducktors/turborepo-remote-cache

# Point turbo.json at it
TURBO_API=https://turbo-cache.myorg.com
TURBO_TOKEN=cache-token
```

### CI Cache Optimization

```yaml
# GitHub Actions — restore turbo/nx cache
- name: Restore Turborepo Cache
  uses: actions/cache@v3
  with:
    path: node_modules/.cache/turbo
    key: turbo-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}
    restore-keys: |
      turbo-${{ runner.os }}-

- name: Restore Nx Cache
  uses: actions/cache@v3
  with:
    path: .nx/cache
    key: nx-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}
    restore-keys: |
      nx-${{ runner.os }}-
```

### Parallel Pipeline Strategies

**Strategy 1: Single agent, parallel tasks (fast for < 50 packages)**
```bash
turbo build test lint --parallel --concurrency=6
```

**Strategy 2: Matrix CI (scales to 100+ packages)**
```yaml
matrix:
  package:
    - --filter=@myorg/web...
    - --filter=@myorg/api...
    - --filter=@myorg/ui...
    - --filter=@myorg/utils...
```
Each job runs independently, failures are isolated, retries are per-package.

**Strategy 3: Nx Distributed Task Execution (1000+ packages)**
```bash
# Agent 1 (coordinator)
nx-cloud start-ci-run --stop-agents-after=build
nx affected:build --base=main

# Agents 2-N
nx-cloud start-agent
```

## Version Management

### Independent vs Fixed Versioning

| Aspect | Fixed/Locked | Independent |
|--------|-------------|-------------|
| **Version** | All packages share one version (e.g., `1.2.3`) | Each package has its own (e.g., `utils@1.0.0`, `ui@2.1.3`) |
| **Bump** | Release bumps everything | Bump only changed packages |
| **Changelog** | Single changelog | Per-package changelogs |
| **Best for** | Tightly coupled packages, single delivery | Loosely coupled, independent release cycles |
| **Tooling** | `standard-version`, `semantic-release` | Changesets |
| **Example** | React, Vue core monorepos | Design systems, utility libraries |

**Recommendation**: Use **Changesets with independent versioning** for most monorepos. Fixed versioning creates unnecessary version bumps for packages that haven't changed, and consumers of individual packages end up with confusing version gaps.

### Changesets — Complete Workflow

```bash
# 1. Developer adds a changeset
npx changeset
# Interactive: select changed packages, choose bump type, write summary

# 2. Changeset file created at .changeset/<random-name>.md
# Contents:
# ---
# "@myorg/ui": minor
# "@myorg/utils": patch
# ---
#
# Add new Button variants and fix utility edge case

# 3. Commit the changeset alongside code changes
git add packages/ui/ packages/utils/ .changeset/
git commit -m "feat(ui): add new Button variants"
```

#### Changeset Config

```jsonc
// .changeset/config.json
{
  "$schema": "https://unpkg.com/@changesets/config@3.0.0/schema.json",
  "changelog": ["@changesets/changelog-github", { "repo": "myorg/repo" }],
  "commit": false,
  "fixed": [],
  "linked": [],
  "access": "public",
  "baseBranch": "main",
  "updateInternalDependencies": "patch",
  "ignore": ["@myorg/internal-tooling"]
}
```

#### Version PR & Publish — GitHub Action

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    branches: [main]

concurrency: ${{ github.workflow }}-${{ github.ref }}

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      # Create/update "Version Packages" PR or publish
      - name: Create Release Pull Request or Publish
        uses: changesets/action@v1
        with:
          version: pnpm changeset version
          publish: pnpm changeset publish
          commit: "chore(release): version packages"
          title: "Version Packages"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Semantic Release in Monorepos

```bash
# Multi-semantic-release — per-package semantic release
pnpm add -Dw multi-semantic-release

# Configure commit message conventions on each package
# package.json > "release" > { "branches": ["main"] }

# Run
pnpm multi-semantic-release
```

Commit convention:
```
feat(ui): add new Button variant    → minor bump for @myorg/ui
fix(utils): correct edge case       → patch bump for @myorg/utils
feat(api)!: change auth flow        → major bump for @myorg/api
docs(readme): update API docs       → no release
```

### Release Pipeline Summary

```
Developer commits code + changeset → PR merged to main
  └─ GitHub Action triggers
      └─ changesets/action:
          ├─ If changesets exist → run "changeset version" → create "Version Packages" PR
          └─ If "Version Packages" PR merged → run "changeset publish"
              ├─ Publish packages to npm (with workspace:* replaced by actual versions)
              ├─ Create GitHub releases per package
              └─ Tag commits (v1.2.3, @myorg/ui@1.2.3, etc.)
```

## Migration Path: Polyrepo → Monorepo

### Strategy Selection

| Strategy | Best For | Risk | Timeline |
|----------|----------|------|----------|
| **Big-bang** | Starting fresh (no legacy), < 10 packages | High | Days |
| **Gradual** | Existing codebase, > 10 packages, multiple teams | Low | Weeks–months |

### Big-Bang Migration

```bash
# 1. Create new monorepo directory
mkdir my-monorepo && cd my-monorepo

# 2. Initialize pnpm workspace
pnpm init
# Create pnpm-workspace.yaml

# 3. Clone each package with history using git filter-repo
git clone --bare https://github.com/myorg/utils.git
cd utils.git
git filter-repo --path-rename :packages/utils/ --force
cd ..
git clone utils.git my-monorepo

# Repeat for each package...

# 4. Merge all histories into one repo
cd my-monorepo
git remote add utils ../utils.git
git fetch utils
git merge --allow-unrelated-histories utils/main
git remote remove utils

# 5. Install dependencies and verify
pnpm install
pnpm build
```

### Gradual Adoption — Step by Step

**Phase 1: Identify candidates (Week 1)**
- Pick 2–3 packages that are tightly coupled (e.g., shared UI lib, utils, types)
- These should have low risk and high cross-dependency value

**Phase 2: Create monorepo shell (Week 1)**
```bash
mkdir my-monorepo
cd my-monorepo
git init
pnpm init
# pnpm-workspace.yaml pointing to packages/*
# Install Turborepo
pnpm add -Dw turbo
# Create turbo.json
turbo init
```

**Phase 3: Migrate packages (Weeks 2–3)**
- Copy each package into `packages/`
- Preserve git history per package (use `git filter-repo` if needed)
- Update all internal imports to use workspace protocol
- Update CI to run from monorepo root

**Phase 4: Expand (Weeks 4+)**
- Add more packages gradually
- Demonstrate value: faster CI (affected builds), atomic cross-package changes
- Document working patterns for teams adopting later

### Preserving Git History

```bash
# git filter-repo — Extract package with full history
brew install git-filter-repo  # macOS

# Create a directory-filtered copy of the repo
git clone --bare https://github.com/myorg/utils.git
cd utils.git
git filter-repo \
  --path src/ \
  --path package.json \
  --path tsconfig.json \
  --path LICENSE \
  --path-rename src/:packages/utils/src/ \
  --force

# git subtree — Simpler but loses history detail
git subtree add --prefix=packages/utils ../utils.git main

# git merge --allow-unrelated-histories — Preserves all history
git remote add utils ../utils.git
git fetch utils
git merge --allow-unrelated-histories utils/main
git remote remove utils
# Then move files to correct location with git mv
```

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| **CI breaks for everyone** | Start with low-risk packages. Gradual adoption keeps other CI pipelines untouched. |
| **Git history loss** | Use `git filter-repo` before merging. Never `rm -rf && cp`. |
| **Dependency conflicts** | Use pnpm's strict resolution. Pin critical shared deps (React, Next). Run `pnpm why` on conflicts. |
| **Build times explode** | Set up affected-only CI immediately. Don't skip caching setup. |
| **Team ownership confusion** | Keep CODEOWNERS per package/directory. Merge freely, but review per team. |

### What to Keep Separate

- **Secrets and environments** — never merge `.env` files. Use `sops` or vault for secrets.
- **Database schemas** — monorepo the code, not the data.
- **CI configurations for non-migrated repos** — leave them in their original repos until migrated.
- **Heavy binary assets** (ML models, large datasets) — use Git LFS or external artifact storage, not the monorepo.

### What to Bring In First

**Good first candidates:**
- Shared type definitions (`@myorg/types`)
- Shared utility libraries (`@myorg/utils`)
- Shared UI components (`@myorg/ui`)
- Internal tooling / CLI tooling
- Configuration packages

**Bring in later (after proving value):**
- Applications (apps/)
- Full domain packages
- Legacy packages that need refactoring

## Developer Experience

### Local Dev Setup

```bash
# Root package.json scripts
{
  "scripts": {
    "dev": "turbo dev --parallel",
    "dev:web": "turbo dev --filter=@myorg/web",
    "dev:api": "turbo dev --filter=@myorg/api",
    "build": "turbo build",
    "build:ui": "turbo build --filter=@myorg/ui",
    "test": "turbo test",
    "test:affected": "turbo test --filter=[main...HEAD]",
    "lint": "turbo lint",
    "type-check": "turbo type-check",
    "clean": "turbo clean && rm -rf node_modules",
    "format": "prettier --check \"**/*.{ts,tsx,json}\"",
    "format:fix": "prettier --write \"**/*.{ts,tsx,json}\""
  },
  "devDependencies": {
    "turbo": "latest",
    "prettier": "^3.0.0"
  }
}

# Developer workflow
git checkout -b feat/add-button-variant
# ... make changes in packages/ui ...
pnpm dev          # Starts all apps with hot reload
# ... verify in web and api apps ...
pnpm test --filter=@myorg/ui
pnpm build        # Full build to verify nothing is broken
pnpm changeset    # Add changeset
git add -A && git commit -m "feat(ui): add new variant"
git push -u origin HEAD
```

### Shared ESLint Configuration

```javascript
// packages/config/eslint-config/library.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:import/recommended',
    'plugin:import/typescript',
    'prettier',
  ],
  plugins: ['@typescript-eslint', 'import'],
  rules: {
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    'import/no-default-export': 'error',
    'import/order': ['error', {
      groups: ['builtin', 'external', 'internal', 'parent', 'sibling', 'index'],
      'newlines-between': 'always',
    }],
  },
  settings: {
    'import/resolver': {
      typescript: {
        alwaysTryTypes: true,
      },
    },
  },
};
```

### VSCode Workspace Configuration

```jsonc
// my-monorepo.code-workspace
{
  "folders": [
    { "name": "root", "path": "." },
    { "name": "web", "path": "apps/web" },
    { "name": "api", "path": "apps/api" },
    { "name": "ui", "path": "packages/ui" },
    { "name": "utils", "path": "packages/utils" }
  ],
  "settings": {
    "typescript.tsdk": "node_modules/typescript/lib",
    "eslint.workingDirectories": [
      { "mode": "auto" }
    ],
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.codeActionsOnSave": {
      "source.fixAll.eslint": "explicit"
    },
    "npm.packageManager": "pnpm",
    "search.exclude": {
      "**/node_modules": true,
      "**/dist": true,
      "**/.next": true
    },
    "files.exclude": {
      "**/node_modules": true
    }
  },
  "extensions": {
    "recommendations": [
      "dbaeumer.vscode-eslint",
      "esbenp.prettier-vscode",
      "nrwl.angular-console",       // Nx extension
      "mikestead.dotenv",
      "bradlc.vscode-tailwindcss"
    ]
  }
}
```

