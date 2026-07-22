## Build System Deep Dive

### Task Orchestration

#### Dependency Graph Construction

Turborepo and Nx both build a dependency graph from your workspace configuration:

```
@myorg/web ──depends-on──> @myorg/ui ──depends-on──> @myorg/utils
@myorg/api ──depends-on──> @myorg/utils
                            @myorg/utils ──depends-on──> (none)
```

Nx's graph is richer — it distinguishes **npm dependencies** (package.json) from **implicit dependencies** (import statements in source code). Turborepo only walks package.json dependencies.

#### Pipeline Configuration — `turbo.json`

```jsonc
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [".env", "tsconfig.json", ".eslintrc.js"],
  "globalEnv": ["NODE_ENV", "API_URL", "VERCEL_ENV"],
  "pipeline": {
    "build": {
      // ^build = build dependencies first (topological order)
      "dependsOn": ["^build"],
      // Files to hash for cache key
      "inputs": ["src/**/*.ts", "src/**/*.tsx", "package.json", "tsconfig.json"],
      // Outputs to cache and restore
      "outputs": ["dist/**", ".next/**"],
      // Environment variables that affect the build output
      "env": ["NODE_ENV"],
      // How many tasks to run in parallel (default: # of CPUs)
      "concurrency": 8
    },
    "test": {
      // $ means "self" — wait for this package's build to finish first
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "inputs": ["src/**/*.test.ts", "src/**/*.spec.ts", "jest.config.ts"],
      "concurrency": 4
    },
    "lint": {
      // No dependsOn — lint can run independently
      "dependsOn": [],
      "outputs": [],
      "inputs": ["src/**/*.ts", "src/**/*.tsx", ".eslintrc.js"]
    },
    "type-check": {
      "dependsOn": ["^build"],
      "outputs": [],
      "inputs": ["src/**/*.ts", "src/**/*.tsx", "tsconfig.json"]
    },
    "dev": {
      "cache": false,  // Don't cache dev servers
      "persistent": true, // Mark as long-running
      "dependsOn": ["^build"]
    }
  }
}
```

#### Turbo DependsOn Notation

| Syntax | Meaning | Example |
|--------|---------|---------|
| `"^build"` | Wait for dependency's `build` to finish | Build UI before web |
| `"build"` | Wait for this package's `build` (self) | Test after build |
| `["^build", "lint"]` | Wait for dep build + this package's lint | |
| `[]` | No dependencies — runs immediately | lint, type-check |
| `"$FOO"` | Await env var `FOO` | Environment-specific builds |

#### Nx Pipeline Configuration

```jsonc
// nx.json
{
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": [
        "{projectRoot}/src/**/*",
        "{projectRoot}/package.json",
        "{projectRoot}/tsconfig.json",
        "!{projectRoot}/src/**/*.test.ts"  // exclude test files from build cache keys
      ],
      "outputs": ["{projectRoot}/dist", "{projectRoot}/.next"]
    },
    "test": {
      "dependsOn": ["build"],
      "inputs": [
        "{projectRoot}/src/**/*",
        "{projectRoot}/jest.config.ts",
        "sharedGlobals"
      ],
      "outputs": ["{projectRoot}/coverage"]
    }
  },
  "namedInputs": {
    "sharedGlobals": ["{workspaceRoot}/tsconfig.json", "{workspaceRoot}/.eslintrc.js"],
    "production": ["{projectRoot}/src/**/*", "!{projectRoot}/src/**/*.test.ts"]
  }
}
```

### Caching Architecture

#### Input Hashing

Turborepo computes a SHA-256 hash from:
- File contents of all `inputs` glob matches
- Contents of `globalDependencies` files
- Values of `globalEnv` variables
- Contents of `turbo.json` itself

Nx does the same concept with `inputs` and `namedInputs` — the hash key includes every file in the input set.

**Cache key = `SHA256(input_files + global_deps + env_vars + task_definition)`**

#### Cache Hit/Miss Debugging

```bash
# Turborepo — verbose cache info
turbo build --verbos e --dry-run

# See what inputs were hashed
turbo build --dry-run=json | jq '.tasks[] | select(.package == "@myorg/web") | .hash'

# Nx — what changed
nx affected:build --base=main --verbose

# Nx — compare cache keys
nx graph --affected --base=main

# Manually verify inputs match
find packages/ui/src -type f -exec md5sum {} \;
```

#### Local Caching

```bash
# Default: local cache at node_modules/.cache/turbo
# Clear local cache
turbo clean

# Nx local cache at .nx/cache
nx reset
```

#### Remote Caching

```bash
# Turborepo — Vercel Remote Cache
npx turbo login
npx turbo link

# Turborepo — Custom S3 Remote Cache
# Set environment variables:
TURBO_API=https://your-cache.example.com
TURBO_TOKEN=your-token
TURBO_TEAM=your-team

# Nx — Nx Cloud
npx nx connect-to-nx-cloud

# Nx — Custom Remote Cache (shareable CLI)
# Configure in nx.json:
"tasksRunnerOptions": {
  "default": {
    "runner": "nx/tasks-runners/default",
    "options": {
      "cacheableOperations": ["build", "test", "lint"],
      "remoteCache": {
        "enabled": true,
        "url": "https://cache.example.com"
      }
    }
  }
}
```

### Incremental Builds

Turborepo and Nx only rebuild packages whose inputs changed PLUS all transitive consumers:

```
Change in @myorg/utils:
  └─ @myorg/utils is rebuilt
     └─ @myorg/ui is rebuilt (depends on utils)
        └─ @myorg/web is rebuilt (depends on ui)
        └─ @myorg/api is rebuilt (depends on utils)

No change in @myorg/types or @myorg/ui own code → they use cache
```

This is the **monorepo superpower** — a change in a utility function doesn't require rebuilding the entire codebase.

### What to Cache / What Not to Cache

| Cache | Don't Cache |
|-------|-------------|
| `dist/` | `node_modules/` (restore from lockfile) |
| `.next/` | `.env` files (secrets) |
| `coverage/` | OS-specific binaries |
| `build/` | Log files |
| `storybook-static/` | PID files |
| Compiled outputs | Lockfile itself |

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

