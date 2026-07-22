# Monorepo Tool Comparison — Deep Reference

> A veteran's deep-dive comparing every major monorepo tool for JavaScript/TypeScript and polyglot codebases. Covers Turborepo, Nx, pnpm workspaces, Bazel, Lerna/Lerna-Lite, and Rush across every dimension that matters.

---

## 1. Overview

| Tool | Creator | First Released | License | Primary Language | Philosophy |
|------|---------|---------------|---------|-----------------|------------|
| **Turborepo** | Vercel (acquired from Jared Palmer) | 2021 | MIT | TypeScript | "Incremental builds, zero config" — minimal config, maximum cache |
| **Nx** | Nrwl (Victor Savkin, Jeff Cross) | 2017 | MIT | TypeScript | "Smart monorepo, fast CI" — full ecosystem with generators, graph, boundaries |
| **pnpm workspaces** | Zoltan Kochan | 2016 (workspaces: 2019) | MIT | TypeScript | "Fast, disk-space efficient package manager" — strict, content-addressable |
| **Bazel** | Google (open-sourced 2015) | 2015 | Apache 2.0 | Java (Starlark config) | "Build and test software of any size, quickly and reliably" — hermetic, reproducible |
| **Lerna** | Kip | 2016 | MIT | TypeScript | "A tool for managing JavaScript projects with multiple packages" — legacy but evolving |
| **Rush** | Microsoft | 2018 | MIT | TypeScript | "A scalable monorepo manager for the web" — policy-heavy, enterprise |

---

## 2. Comparison Matrix

| Dimension | Turborepo | Nx | pnpm Workspaces | Bazel | Lerna | Rush |
|-----------|-----------|-----|-----------------|-------|-------|------|
| **Task Orchestration** | Auto via `dependsOn` (`^` / `$` / none) | Explicit + implicit DAG; target dependencies | None (`pnpm -r` runs in order but no DAG) | Full Bazel DAG (BUILD files) | Basic (`--since`, `--scope`) | Custom via Rush plugins + Heft |
| **Caching (Local)** | `node_modules/.cache/turbo` — SHA-256 | `.nx/cache` — content hash | None | Built-in (hermetic incremental) | None | Built-in (phasered) |
| **Caching (Remote)** | Vercel, S3 (custom server), GH Cache | Nx Cloud, custom runners | None | Remote Cache + Remote Execution | None | Rush Cloud (phased commands) |
| **Build Speed** | Very fast (parallel + cache) | Fast (parallel + cache + distributed) | N/A (no build system) | Fastest (hermetic + RE + granular) | Slow (serial, no cache) | Fast (phased, parallel) |
| **Plugin Ecosystem** | Minimal (growing: Turborepo generators) | Extensive (200+ Nx plugins) | pnpm plugins | Large (rules_go, rules_ts, rules_docker, etc.) | Minimal (legacy) | Moderate (Rush plugins from community) |
| **Learning Curve** | 3/10 | 6/10 | 2/10 | 9/10 | 3/10 | 7/10 |
| **Community** | 45k+ GitHub stars, Vercel ecosystem | 22k+ GitHub stars, Nrwl ecosystem | 28k+ GitHub stars | 22k+ GitHub stars, Google-backed | 35k+ stars (legacy but large) | 5k+ stars, MS-backed |
| **Enterprise Features** | Remote cache, RBAC (Vercel) | DTE, graph, boundaries, generators, code ownership | None | RE, RBE, multi-language, strict hermeticity | None | Policy enforcement, phased builds, lockfile management |
| **Best For** | JS/TS monorepos wanting fast + simple | Large JS/TS monorepos needing full toolkit | Small repos where pnpm alone suffices | Polyglot repos at massive scale | Publishing/changelogs (paired with Turborepo/Nx) | Enterprise .NET/TS monorepos |
| **Node Version** | Node 18+ | Node 18+ | Node 18+ (pnpm 9+) | Any (hermetic) | Node 18+ | Node 18+ |
| **Active Development** | ✅ Very active (Vercel team) | ✅ Very active (Nrwl team) | ✅ Very active | ✅ Active (Google) | ⚠️ Slow (community maintained) | ✅ Active (Microsoft) |

---

## 3. Deep Dive per Tool

### 3.1 Turborepo

#### Key Features

- **Zero-config pipeline**: define `dependsOn` and Turborepo figures out the execution order
- **Content-aware caching**: SHA-256 hash of inputs, outputs stored locally + remotely
- **Parallel execution**: runs independent tasks concurrently, respects concurrency limits
- **Incremental builds**: only rebuild changed packages + their consumers
- **Dry-run mode**: see the execution plan without running
- **Filter syntax**: `--filter` for packages, dependents, dependencies, git-changed
- **Monorepo generator (experimental)**: `npx create-turbo` scaffolds a monorepo with shared configs

#### Pipeline Configuration Example

```jsonc
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [".env", "tsconfig.json"],
  "globalEnv": ["NODE_ENV", "VERCEL_ENV"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["src/**/*.ts", "src/**/*.tsx", "package.json", "tsconfig.json"],
      "outputs": ["dist/**", ".next/**"],
      "env": ["NODE_ENV"],
      "concurrency": 8
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "concurrency": 4
    },
    "lint": {
      "dependsOn": [],
      "outputs": [],
      "inputs": [".eslintrc.js"]
    },
    "dev": {
      "cache": false,
      "persistent": true,
      "dependsOn": ["^build"]
    }
  }
}
```

#### Caching Architecture

```
Cache Key = SHA256(
  all files matched by task `inputs` globs +
  all `globalDependencies` file contents +
  all `globalEnv` values +
  `turbo.json` content
)

Cache Location:
  Local:    node_modules/.cache/turbo/<package>.<task>.hash
  Remote:   Vercel infra or custom S3/GCS bucket

Cache Hit → restore outputs (dist/, .next/, coverage/)
Cache Miss → execute task, store outputs
```

#### When to Choose Turborepo

- Your codebase is 100% JavaScript/TypeScript
- You want the fastest possible setup — from `npm init` to cached builds in 5 minutes
- You're already in the Vercel ecosystem (remote cache works seamlessly)
- You don't need code generation, module boundaries, or distributed task execution
- **Rule of thumb**: If 80% of your monorepo needs can be solved with `dependsOn` + cache, choose Turborepo.

#### Limitations

- No built-in code generation (use `create-turbo` or Plop)
- No module boundary enforcement (use ESLint plugins)
- No dependency graph visualization beyond `--graph`
- No distributed task execution across agents (single-agent parallel only)
- Less granular input controls than Nx (no `namedInputs`, no `targetDefaults` inheritance)
- No TypeScript project references integration
- No affected command for "apps that depend on this package" — use `--filter=...@myorg/ui` (trailing dots)

---

### 3.2 Nx

#### Key Features

- **Code generation**: `nx generate @nx/react:component --name=button --project=ui`
- **Dependency graph**: `nx graph` — interactive visualization with affected, focused, and group views
- **Affected commands**: `nx affected:build --base=main` — runs tasks only on affected projects
- **Module boundaries**: `@nx/enforce-module-boundaries` — tag-based dependency constraints
- **Distributed Task Execution (DTE)**: `nx-cloud start-ci-run` — split tasks across multiple agents
- **`namedInputs`**: reusable input sets for fine-grained cache key control
- **Nx plugins for every framework**: Next.js, React, Angular, Node, Nest, Express, Vue, Svelte
- **Project graph plugins**: extending the graph with custom nodes and edges
- **Task orchestration across machine boundaries**: not just within one machine

#### Code Generation

```bash
# Create a new React library
nx g @nx/react:lib ui --directory=packages/ui --bundler=vite --unit-test-runner=vitest

# Create a new Next.js app
nx g @nx/next:app web --directory=apps/web --e2e-test-runner=playwright

# Generate a component in an existing library
nx g @nx/react:component Button --project=ui --export

# When not using Nx plugins, use Plop for lightweight code generation
pnpm add -Dw plop
# plopfile.js with package/component generators
```

#### Dependency Graph

```bash
# Interactive graph (opens in browser)
nx graph

# Focus on a single project + its dependencies
nx graph --focus=@myorg/ui

# Show affected projects
nx affected:graph --base=main

# Export as JSON for custom analysis
nx graph --file=graph.json

# Find all paths between two projects
nx graph --focus=@myorg/web --groupByFolder=false
```

#### Affected Commands

```bash
# Core affected pattern
nx affected:build --base=origin/main --head=HEAD --parallel=5 --configuration=production

# Run only on projects that have explicit test changes
nx affected --target=test --base=main --head=HEAD \
  --exclude='!packages/**/src/**/*.spec.ts'

# Run tasks on all projects that depend on a changed lib
nx affected:build --base=main --with-deps

# Run tasks only on libs (skip apps)
nx affected:test --base=main --exclude='apps/*'
```

#### Distributed Task Execution

```yaml
# .github/workflows/ci.yml — Nx DTE
jobs:
  main:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npx nx-cloud start-ci-run --stop-agents-after=build
      - run: npx nx affected:build --base=main --parallel=3
      - run: npx nx affected:test --base=main --parallel=2

  agent:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        agent: [1, 2, 3]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npx nx-cloud start-agent
```

#### Named Inputs — Fine-Grained Cache Control

```jsonc
// nx.json
{
  "namedInputs": {
    "sharedGlobals": [
      "{workspaceRoot}/tsconfig.base.json",
      "{workspaceRoot}/.eslintrc.json",
      "{workspaceRoot}/nx.json"
    ],
    "production": [
      "{projectRoot}/src/**/*",
      "!{projectRoot}/src/**/*.test.ts",
      "!{projectRoot}/src/**/*.spec.ts",
      "!{projectRoot}/src/test-setup.ts"
    ],
    "buildOutputs": ["{projectRoot}/dist", "{projectRoot}/build"]
  },
  "targetDefaults": {
    "build": {
      "inputs": ["production", "^production", "sharedGlobals"],
      "outputs": ["{projectRoot}/dist", "{projectRoot}/.next"]
    },
    "test": {
      "inputs": ["default", "^production", "sharedGlobals"]
    }
  }
}
```

#### Module Boundaries

```jsonc
// project tags
{
  "@myorg/utils": { "tags": ["scope:shared", "type:util"] },
  "@myorg/ui": { "tags": ["scope:ui", "type:lib"] },
  "@myorg/web": { "tags": ["scope:app", "type:app"] },
  "@myorg/api": { "tags": ["scope:app", "type:app"] },
  "@myorg/internal-tools": { "tags": ["scope:internal", "type:tool"] }
}

// .eslintrc.json
{
  "rules": {
    "@nx/enforce-module-boundaries": [
      "error",
      {
        "depConstraints": [
          { "sourceTag": "scope:shared", "onlyDependOnLibsWithTags": ["scope:shared"] },
          { "sourceTag": "scope:ui", "onlyDependOnLibsWithTags": ["scope:shared", "scope:ui"] },
          { "sourceTag": "scope:app", "onlyDependOnLibsWithTags": ["scope:shared", "scope:ui", "scope:api"] },
          { "sourceTag": "scope:internal", "onlyDependOnLibsWithTags": ["scope:shared", "scope:internal"] },
          { "sourceTag": "type:app", "onlyDependOnLibsWithTags": ["type:lib", "type:util"] }
        ]
      }
    ]
  }
}
```

#### When to Choose Nx

- You have a large monorepo (50+ packages) and need graphs, generators, and boundaries
- You need distributed task execution across multiple CI agents
- Your team values code generation for consistency (scaffolding apps, libs, components)
- You want enforcement of architectural rules programmatically
- You're building a platform that other teams contribute to — boundaries and tags scale
- You have a polyglot codebase (Nx supports Go, Python, Java, Rust, .NET, plus JS/TS)

#### Limitations

- More config than Turborepo — `nx.json`, project `tags`, `namedInputs`, plugin config
- Nx Cloud dependency for full DTE features (vendor lock-in risk)
- Learning curve is moderate — the `enforce-module-boundaries` rule alone takes time to tune
- Generators can produce too much boilerplate for small projects
- Heavier than Turborepo — more dependencies, more abstractions
- Plugin quality varies — some are excellent, others lack documentation

---

### 3.3 pnpm Workspaces

#### Key Features

- **Strict dependency resolution**: no phantom dependencies — packages can only import what they declare
- **Content-addressable storage**: packages are stored once on disk, symlinked into each workspace's node_modules — deduplication by content, not by name
- **Workspace protocol**: `workspace:*` — always resolves to the local workspace version
- **`pnpm --filter`**: powerful filtering syntax for running npm scripts on subsets of packages
- **`pnpm -r`**: run commands recursively across all packages
- **`pnpm deploy`**: deploy a single package with only its production dependencies
- **`pnpm pack`**: create tarball of a package with workspace protocol replaced

#### Workspace Protocol

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
  - "tools/*"
```

```jsonc
// packages/web/package.json
{
  "dependencies": {
    // workspace:* = always use the local version
    "@myorg/ui": "workspace:*",
    "@myorg/utils": "workspace:*",

    // workspace:^1.0.0 = ^1.0.0 on publish, workspace protocol locally
    "@myorg/legacy": "workspace:^1.2.0",

    // workspace:1.2.3 = exactly 1.2.3 on publish
    "@myorg/pinned": "workspace:1.2.3"
  }
}
```

On `pnpm publish`, `workspace:*` is automatically replaced with the actual version from the target package's `package.json`.

#### Filtering Syntax

```bash
# Run in specific package
pnpm --filter=@myorg/ui build

# Run in all packages
pnpm -r build

# Run in a package and its dependents (upward)
pnpm --filter=@myorg/ui... build

# Run in a package and its dependencies (downward)
pnpm --filter=...@myorg/ui build

# Run in all packages changed since main
pnpm --filter=[origin/main...HEAD] build

# Run in all packages except @myorg/internal
pnpm -r --filter=!@myorg/internal lint

# Run in packages matching glob
pnpm --filter="./packages/**" build

# Combined
pnpm --filter="@myorg/ui..." --filter="!@myorg/internal" test
```

#### When pnpm Workspaces Alone Is Enough

- 3–10 packages with shallow dependency graphs
- No cross-package caching needed (each build is fast enough)
- Teams comfortable with full rebuilds on CI
- No need for task orchestration (no DAG of build/test/lint/deploy)
- Use case: Design system monorepo (18 icon/component/theme packages, 6 devs)

**Example: design system monorepo using pnpm alone:**
```yaml
# pnpm-workspace.yaml
packages:
  - "packages/*"
  - "apps/docs"
```
```jsonc
// package.json
{
  "scripts": {
    "build": "pnpm -r --filter=!./apps/docs build",
    "build:docs": "pnpm --filter=./apps/docs build",
    "build:all": "pnpm -r build",
    "test": "pnpm -r test",
    "lint": "pnpm -r lint",
    "storybook": "pnpm --filter=./apps/docs storybook",
    "changeset": "changeset",
    "release": "changeset publish"
  }
}
```

#### Limitations

- **No build caching**: every build runs from scratch. No cache-hit restores. No incremental builds.
- **No task graph**: `pnpm -r` runs commands sequentially (or parallel with `--parallel` but no DAG coordination)
- **No dependency graph analysis**: no built-in `nx graph` or `turbo run build --graph`
- **No code generation**: no scaffolding tools for new packages/components
- **No module boundaries**: can't enforce `apps/` can't import from other `apps/` at the tool level
- **No remote caching**: every CI run and every dev machine builds from scratch
- **pnpm's content store can grow large**: periodic `pnpm store prune` needed

---

### 3.4 Bazel

#### Key Features

- **Hermetic builds**: builds run in a sandbox — no network access, no access to anything not declared in BUILD files. Reproducible every time.
- **Remote execution (RBE)**: build actions execute on Google/AWS/in-cluster workers. Scale horizontally.
- **Remote caching**: share build artifacts across all developers and CI.
- **Multi-language**: native support for Java, C++, Python, Go, Rust, TypeScript (via rules_ts), Docker (via rules_docker), Kubernetes.
- **Granular incremental builds**: Bazel tracks every individual file — not per-package modules. A single function change rebuilds only the compilation units that depend on it.
- **`BUILD` files**: every package declares its own build targets and dependencies.
- **`bazel query` / `bazel cquery`**: ask questions about the build graph ("what depends on this target?").

#### BUILD File Example

```python
# packages/ui/BUILD.bazel
load("@npm//:defs.bzl", "npm_link_all_packages")
load("@aspect_rules_ts//ts:defs.bzl", "ts_project")
load("@aspect_rules_js//js:defs.bzl", "js_library")

npm_link_all_packages(name = "node_modules")

ts_project(
    name = "ui",
    srcs = glob(["src/**/*.ts", "src/**/*.tsx"]),
    deps = [
        "//packages/utils",  # dependency on another Bazel target
        ":node_modules/react",
        ":node_modules/react-dom",
    ],
    tsconfig = "//:tsconfig",
    out_dir = "dist",
    declaration = True,
)

js_library(
    name = "dist",
    srcs = [":ui"],
    visibility = ["//apps:__subpackages__"],
)
```

#### Caching and Remote Execution

```
bazel build //packages/ui

  Phase 1: Analyze BUILD files → build DAG of actions
  Phase 2: Execute actions in topological order
    Each action: compute hash of inputs (source files + toolchain + env)
      → Check local cache
        → Check remote cache (if configured)
          → Execute locally or via RBE
            → Store outputs in cache

Cache key = SHA256(
  source file contents +
  toolchain version +
  BUILD file contents +
  action configuration
)
```

```bash
# Build with remote caching
bazel build //packages/ui --remote_cache=grpc://cache.example.com:9092

# Build with remote execution
bazel build //packages/ui --remote_executor=grpc://rbe.example.com:9092

# Build with debug output
bazel build //packages/ui --explain=build.log --verbose_explanations

# Query the build graph
bazel query "deps(//packages/ui)" --output=graph

# Find all targets that depend on a package
bazel cquery "rdeps(//..., //packages/utils)"
```

#### When It's Worth the Investment

- **Polyglot monorepo**: Java backend + Python ML pipeline + TypeScript frontend + Go CLI tools
- **Massive scale**: 1000+ engineers, millions of lines of code
- **Strict reproducibility**: compliance requirements, deterministic builds
- **Remote execution**: local builds are too slow for your codebase size
- **Fine-grained incremental builds**: you need action-level (not package-level) caching

#### Limitations

- **Steep learning curve**: Bazel's Starlark language, hermeticity requirements, and BUILD semantics take weeks to learn
- **Toolchain maintenance**: rules for each language need maintenance as language toolchains evolve
- **Overhead for small repos**: Bazel's analysis phase alone can take longer than a simple `tsc` build on a small codebase
- **Node.js ecosystem friction**: rules_ts, rules_js, and aspect_rules_js are third-party and change frequently
- **Windows support**: historically weak (improving but not first-class)
- **CI infrastructure**: RBE requires significant infrastructure investment (or paying Google Cloud/AWS for it)
- **Migration cost**: converting existing packages to Bazel BUILD files is expensive

---

### 3.5 Lerna / Lerna-Lite

#### Legacy Role

Lerna was the original monorepo tool for JavaScript (2016). Before Turborepo and Nx existed, Lerna was the only game in town. Its original features:

- `lerna bootstrap`: symlink packages together
- `lerna run`: run npm scripts across all packages
- `lerna publish`: version and publish packages
- `lerna import`: migrate git histories
- `lerna changed`: list changed packages since last release

After `lerna bootstrap` became obsolete (pnpm/Yarn/npm workspaces handle symlinking), and task orchestration moved to Turborepo/Nx, Lerna's role shrank to basically just publishing.

#### Current State

- **Lerna 8**: rewrote to use Nx under the hood for task orchestration. So when you run `lerna run build`, it actually uses Nx's task runner.
- **Lerna-Lite**: a lighter fork of Lerna focused only on publishing and versioning. Maintained by ghiscoding. Removes all the task-running code (delegates to Turborepo or Nx).

#### When Lerna Still Makes Sense

**Option A: Lerna + Turborepo** — use Lerna for publishing/changelogs, Turborepo for builds:
```bash
# Install both
pnpm add -Dw lerna turbo

# lerna.json
{
  "version": "independent",
  "npmClient": "pnpm",
  "command": {
    "publish": {
      "ignoreChanges": ["*.md", "**/test/**"],
      "message": "chore(release): publish"
    }
  }
}

# Use Turbo for builds, Lerna for publish
pnpm lerna publish
```

**Option B: Lerna-Lite** — minimal publish-only tool:
```jsonc
// lerna.json (Lerna-Lite)
{
  "version": "independent",
  "npmClient": "pnpm",
  "packages": ["apps/*", "packages/*"],
  "command": {
    "version": { "allowBranch": "main" },
    "publish": {
      "conventionalCommits": true,
      "createRelease": "github"
    }
  }
}
```

```bash
# Lerna-Lite commands (no bootstrap, no run — those are removed)
pnpm lerna changed
pnpm lerna diff
pnpm lerna version
pnpm lerna publish
```

#### Migration Off Lerna

**To Turborepo:**
1. Remove `lerna run` — replace with `turbo run`
2. Remove `lerna bootstrap` — you already use pnpm workspaces
3. Remove `lerna.json` — add `turbo.json`
4. Keep `lerna publish` or migrate to `changesets`

**To Nx:**
1. Follow Nx migration guide — `nx init` can detect Lerna config
2. Replace `lerna.json` with `nx.json`
3. Migrate `lerna publish` workflow to Nx release or changesets

---

### 3.6 Rush

#### Key Features

- **Lockfile management**: Rush manages its own lockfile for all projects — no relying on pnpm-lock.yaml or yarn.lock alone
- **Phased builds**: builds run in phases (build → test → lint) with explicit orchestration
- **Policy enforcement**: built-in ESLint, Prettier, and custom policies enforced across all projects
- **Heft build system**: Rush includes Heft, a TS/ESBuild-based build system with plugin support
- **Artifact caching and deduplication**: Rush's install approach deduplicates at the project level
- **pnpm-based**: Rush uses pnpm under the hood for package installation
- **Rush plugins**: extensible through plugins for additional commands and policies

#### rush.json Configuration

```jsonc
// rush.json
{
  "npmVersion": "9.6.0",
  "rushVersion": "5.112.0",
  "pnpmVersion": "8.6.0",
  "nodeSupportedVersionRange": ">=18.0.0",
  "projectFolderMinDepth": 2,
  "projectFolderMaxDepth": 2,
  "approvedPackagesPolicy": {
    "reviewCategories": ["production", "development"],
    "ignoredNpmScopes": ["@types"]
  },
  "gitPolicy": {
    "versionBumpCommitMessage": "Bump versions [skip ci]",
    "changeLogPath": "common/changes"
  },
  "repository": {
    "url": "https://github.com/myorg/repo",
    "defaultBranch": "main"
  },
  "projects": [
    {
      "projectFolder": "apps/web",
      "reviewCategory": "production",
      "shouldPublish": true
    },
    {
      "projectFolder": "packages/ui",
      "reviewCategory": "production",
      "shouldPublish": true
    },
    {
      "projectFolder": "packages/utils",
      "reviewCategory": "development",
      "shouldPublish": false
    }
  ]
}
```

#### Phased Build Commands

```bash
# Build in dependency order
rush build

# Build specific projects and their deps
rush build --to @myorg/web

# Build only changed projects
rush build --impacted-by @myorg/utils

# Rebuild (force — no incremental)
rush rebuild

# Run a custom npm script in the project order
rush <script> --to @myorg/web
```

#### Policy Enforcement

Rush's `approvedPackagesPolicy` is unique — it maintains a curated list of approved dependencies across the whole repo:

```bash
# After adding a new dependency, generate the approval
rush update-autoinstaller

# Check if any packages use non-approved deps
rush check

# Auto-fix dependency version consistency
rush update
```

#### When to Choose Rush

- **Enterprise .NET/TypeScript monorepos** — Rush + Heft works well with TypeScript and ASP.NET patterns
- **Strict approval workflows**: you need approved-package-list enforcement (common in regulated industries)
- **Centralized lockfile management**: you want Rush to manage a single lockfile, not pnpm/yarn directly
- **Large teams needing policy enforcement** — Rush's `approvedPackagesPolicy` and `rush check` catch issues early
- **Phased build orchestration**: you need more control than Turborepo's `dependsOn` but less complexity than Bazel

#### Limitations

- **Rush is opinionated**: it wants to control your build pipeline (Heft, phased commands). Not easy to "just use Turborepo for builds, Rush for packages."
- **pnpm-only**: Rush uses pnpm internally. Can't use yarn or npm.
- **Configuration heavy**: `rush.json`, project registration, autoinstallers, change logs — lots of ceremony.
- **Smaller ecosystem**: fewer plugins, fewer community resources than Nx or Turborepo.
- **Migration cost**: not trivial to adopt Rush for an existing monorepo — the project registration process is manual.
- **Less JS/TS idiomatic**: Rush feels more like a C#/.NET tool that happens to support JS — the configuration style shows its enterprise heritage.

---

## 4. Decision Framework

### Decision Tree (Text)

```
START: What is your primary language?
├── Multiple languages (Java + Go + TS + Python + Rust)
│   └── > 500 engineers, need hermetic builds + remote execution?
│       ├── Yes → Bazel
│       └── No → Nx (polyglot support via executors + plugins)
│
├── 100% JavaScript/TypeScript
│   └── How many packages?
│       ├── < 10 → pnpm workspaces (no build orchestrator)
│       │   └── CI builds > 5 min?
│       │       ├── Yes → Add Turborepo
│       │       └── No → Stay with pnpm alone
│       ├── 10–50 → Turborepo (fastest setup)
│       │   └── Need generators, boundaries, DTE?
│       │       ├── Yes → Nx
│       │       └── No → Turborepo is perfect
│       ├── 50–200 → Nx (graphs, boundaries, DTE)
│       └── > 200 → Nx + DTE or Rush
│
└── Enterprise with strict com pliance
    └── Need approved dependency lists, centralized lockfile management?
        ├── Yes → Rush
        └── No → Nx + syncpack
```

### Cost vs Benefit Analysis

| Tool | Setup Time | Ongoing Maintenance | CI Cost | Migration Cost | Benefit-to-Cost Ratio |
|------|-----------|--------------------|---------|----------------|----------------------|
| **pnpm alone** | 15 min | 0 (none) | Highest (full rebuilds) | None | ∞ (no cost) — until you need more |
| **Turborepo** | 30 min | ~2 hrs/month | Low (cached) | Very low | High |
| **Nx** | 2–4 hrs | ~8 hrs/month | Low (cached + DTE) | Medium | High (at scale) |
| **Bazel** | 2–4 weeks | ~40 hrs/month | Lowest (RBE) | Very high | Only at very large scale |
| **Lerna+Lite** | 15 min (add-on) | ~1 hr/month | Same as underlying | Very low | Low (legacy) |
| **Rush** | 4–8 hrs | ~10 hrs/month | Low | Medium–High | Medium (enterprise) |

### When to Use Multiple Tools Together

- **pnpm + Turborepo** (most common): pnpm for installs, Turborepo for orchestration + caching
- **pnpm + Nx**: pnpm for installs, Nx for full toolkit (generators, graph, boundaries, DTE)
- **pnpm + Turborepo + Lerna**: Turborepo for builds, Lerna for publishing (legacy pattern)
- **pnpm + Turborepo + Changesets**: Turborepo for builds, Changesets for versioning + publishing
- **pnpm + Nx + Changesets**: Nx for everything + Changesets for versioning
- **pnpm + Rush**: Rush manages installs + builds + policy
- **Bazel alone**: Bazel handles everything (install via rules, build, test, deploy)

---

## 5. Migration Paths Between Tools

### Lerna → Turborepo

```bash
# 1. Install Turborepo
pnpm add -Dw turbo

# 2. Create turbo.json
cat > turbo.json << 'EOF'
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": { "dependsOn": ["^build"], "outputs": ["dist/**"] },
    "test": { "dependsOn": ["build"], "outputs": [] },
    "lint": { "outputs": [] }
  }
}
EOF

# 3. Replace lerna run commands
# Before: "build": "lerna run build"
# After:  "build": "turbo run build"
# After:  "test": "turbo run test"
# After:  "lint": "turbo run lint"

# 4. Keep lerna publish if you need it, or migrate to changesets
# lerna.json still works for publish commands

# 5. Verify
turbo run build
turbo run test
```

### Lerna → Nx

```bash
# 1. Run Nx init
npx nx@latest init

# 2. Nx detects lerna.json and offers to migrate
# It will create nx.json, modify package.json scripts

# 3. Or manual:
pnpm add -Dw @nx/workspace
nx g @nx/workspace:init

# 4. Update CI
# Before: lerna run build --since=main
# After:  nx affected:build --base=main
```

### pnpm Workspaces → Turborepo

```bash
# 1. Install Turborepo
pnpm add -Dw turbo

# 2. Create turbo.json with pipeline config

# 3. Replace pnpm -r commands
# Before: "build": "pnpm -r build"
# After:  "build": "turbo run build"

# Before: "test": "pnpm -r --filter=!apps/docs test"
# After:  "test": "turbo run test"

# 4. Leverage --filter for affected
pnpm build --filter=[main...HEAD]

# 5. Set up remote cache (optional but recommended)
npx turbo login && npx turbo link
```

### pnpm → Nx

```bash
# 1. Init Nx
npx nx@latest init

# 2. Nx detects pnpm-workspace.yaml and reads the packages
# It creates nx.json with project configuration

# 3. Add Nx plugins for your frameworks
pnpm add -Dw @nx/next @nx/react @nx/node

# 4. Migrate CI
# Before: pnpm -r build
# After:  nx run-many --target=build
# Or:     nx affected:build --base=main
```

### Turborepo → Nx

```bash
# 1. Install Nx
pnpm add -Dw nx @nx/workspace

# 2. Run Nx init (migrates turbo.json to nx.json)
npx nx init

# 3. Nx reads turbo.json and imports pipeline config
# It creates the equivalent nx.json with targetDefaults

# 4. Optional: add plugins for generators
pnpm add -Dw @nx/react @nx/next

# 5. Update CI commands
# Before: turbo run build --filter=[main...HEAD]
# After:  nx affected:build --base=main
```

### pnpm → Bazel

This is the most complex migration. It's not incremental for individual packages — you need to convert BUILD files for the entire repo.

```bash
# 1. Add Bazelisk (Bazel launcher) to root
brew install bazelisk  # dev machines

# 2. Create root WORKSPACE file
cat > WORKSPACE << 'EOF'
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "aspect_rules_js",
    sha256 = "...",
    strip_prefix = "rules_js-1.33.0",
    url = "https://github.com/aspect-build/rules_js/releases/download/v1.33.0/rules_js-v1.33.0.tar.gz",
)

load("@aspect_rules_js//js:repositories.bzl", "rules_js_dependencies")
rules_js_dependencies()

# Load pnpm workspace support
load("@aspect_rules_js//npm:repositories.bzl", "npm_translate_lock")
npm_translate_lock(
    name = "npm",
    pnpm_lock = "//:pnpm-lock.yaml",
    update_pnpm_lock = True,
)

load("@npm//:repositories.bzl", "npm_repositories")
npm_repositories()
EOF

# 3. Create BUILD.bazel per package (one per package — takes the longest)
# This is the primary migration cost

# 4. Build
bazel build //packages/ui:all

# 5. Remove old scripts from package.json
# Bazel replaces npm scripts entirely
```

**Cost estimate for pnpm → Bazel migration:**
- 10 packages: ~2–4 hours of BUILD file authoring per package
- 50 packages: ~1–2 weeks full-time
- 100+ packages: ~1 month+ including learning curve for rules

---

## 6. Real-World References

### Turborepo Users

| Company | Scale | Use Case |
|---------|-------|----------|
| **Vercel** | Entire frontend ecosystem | Vercel's own SDK, CLI, and internal tooling monorepo |
| **Netflix** | UI platform team | Shared UI components and design system |
| **Stripe** | Several frontend teams | Payment UI components and internal tools |
| **Linear** | ~30 packages | Linear's entire frontend codebase |
| **Yahoo/Jira** | Design system + web apps | Large-scale migration from polyrepo |
| **AWS Amplify** | CLI + Console + UI libs | Full AWS Amplify JS ecosystem |

### Nx Users

| Company | Scale | Use Case |
|---------|-------|----------|
| **Nrwl (creator)** | Dogfooding | Nx itself is a monorepo with Nx |
| **Adobe** | Multiple product teams | Adobe Express and other web apps |
| **Microsoft** | VS Code extensions | Large ecosystem of extensions |
| **Hilton** | Enterprise hotel platform | Reservation system + digital services |
| **PayPal** | Checkout experience team | Checkout flow micro-frontends |
| **Lyft** | Web platform team | Lyft's frontend monorepo |
| **eBay** | Multiple product teams | eBay's web app monorepo |

### pnpm Workspaces (as primary, no orchestrator)

| Company | Scale | Notes |
|---------|-------|-------|
| **Vue.js core team** | ~10 packages | Vue core, compiler, server-renderer |
| **Prisma** | Multiple packages | Prisma CLI, client, engines |
| **Astro** | ~20 packages | Astro core, integrations, adapters |
| **Nuxt** | ~30 packages | Nuxt framework modules |

### Bazel Users

| Company | Scale | Use Case |
|---------|-------|----------|
| **Google** | Entire company monorepo | The origin of Bazel. ~2 billion lines of code. |
| **Uber** | Polyglot monorepo | Go + Android + iOS + Web |
| **Twitter/X** | Monorepo (before migration) | Large JVM + Scala codebase |
| **ASOS** | Polyglot ecommerce | .NET + JS + Python monorepo |
| **SpaceX** | Embedded + web + ML | Starlink dashboard, Dragon software |
| **Etsy** | PHP + JS monorepo | Full ecommerce platform (migrated partly from Bazel back to Nx) |

### Rush Users

| Company | Scale | Use Case |
|---------|-------|----------|
| **Microsoft** | 1ES (1ES Platform) | Large enterprise .NET + TS monorepo |
| **TypeScript compiler** | ~1 package (but uses Rush) | Microsoft uses Rush for various first-party monorepos |
| **Bing** | Search infrastructure | Bing frontend tooling |
| **Selina** | Hospitality platform | Multi-app monorepo across multiple product teams |
| **SAP** | Enterprise cloud | Cloud platform frontend components |

### Lerna (Legacy — Most Have Migrated)

| Company | Past State | Current State |
|---------|-----------|---------------|
| **Babel** | Babel monorepo on Lerna | Migrated to Yarn workspaces + Lerna for publish |
| **React** | React used Lerna | Migrated to custom scripts, then Nx |
| **Jest** | Jest on Lerna | Migrated to pnpm workspaces |
| **WordPress** | Gutenberg on Lerna | Migrated to pnpm + Nx |
| **Angular** | Angular CLI on Lerna | Migrated to Bazel, then Nx |
| **Ember** | Ember.js on Lerna | Migrated to pnpm workspaces |

### Migration Patterns Observed in the Wild

```
2016–2020: Lerna (everyone)
2020–2022: Lerna → pnpm workspaces + Turborepo (mid-size teams)
            Lerna → pnpm workspaces + Nx (larger teams)
2022–2024: pnpm workspaces + Turborepo (most common new setup)
            pnpm workspaces + Nx (growth for large monorepos)
2024+:     pnpm + Turborepo (default Vercel path)
            pnpm + Nx (for full toolkit)
            Bazel (only at very large scale or polyglot)
            Rush (enterprise with strict policy needs)
```

---

## 7. Quick Reference — CLI Commands

```bash
# ── TURBOREPO ──────────────────────────────────────
turbo build                              # Build all
turbo build --filter=@myorg/ui           # Build one package
turbo build --filter=[main...HEAD]       # Build affected
turbo build --filter=@myorg/ui...        # Build package + its consumers
turbo build --filter=...@myorg/ui        # Build package + its dependencies
turbo run build test lint --parallel     # Run multiple tasks
turbo run build --graph                  # Show execution graph
turbo run build --dry-run                # Show execution plan (no execute)
turbo run build --dry-run=json           # JSON execution plan
turbo login && turbo link                # Set up remote cache
turbo clean                              # Clear local cache

# ── NX ──────────────────────────────────────────────
nx build my-app                          # Build one project
nx run-many --target=build               # Build all
nx affected:build --base=main            # Build affected
nx affected:build --base=main --head=HEAD
nx affected:test --base=main
nx graph                                 # Interactive dependency graph
nx graph --focus=@myorg/ui
nx g @nx/react:lib ui                   # Generate React library
nx g @nx/next:app web --directory=apps
nx run @myorg/web:build:production       # Run with configuration
nx migrate latest                        # Update Nx and plugins
nx report                                # Show Nx version info
nx reset                                 # Clear cache
nx connect-to-nx-cloud                   # Set up Nx Cloud

# ── PNPM WORKSPACES ────────────────────────────────
pnpm -r build                            # Run build in all packages (in order)
pnpm --filter=@myorg/ui build            # Run in one package
pnpm --filter=@myorg/ui... build         # Package + consumers
pnpm --filter=...@myorg/ui build         # Package + deps
pnpm --filter=[origin/main...HEAD] build # Changed packages only
pnpm ls --depth=3                        # Dependency tree
pnpm why react                           # Why is react installed?
pnpm outdated -r                         # Outdated deps across all packages
pnpm store prune                         # Clean content-addressable store
pnpm dedupe                              # Deduplicate compatible versions

# ── BAZEL ───────────────────────────────────────────
bazel build //packages/ui:all            # Build UI package
bazel test //packages/ui/...             # Run all tests in UI
bazel query "deps(//packages/ui)"        # Query dependencies
bazel cquery "rdeps(//..., //packages/ui)"  # Reverse deps
bazel clean                              # Clean build outputs
bazel build --explain=log.txt            # Debug build decisions
bazel build --aspects=@aspect_rules_ts//ts:defs.bzl%ts_project_aspect
bazel run @npm//:jest -- packages/ui     # Run tool from Bazel

# ── LERNA ───────────────────────────────────────────
lerna changed                            # List changed packages
lerna diff                               # Show diff since last release
lerna version                            # Version packages
lerna publish                            # Publish packages (from-if-content)
lerna run build --since=main             # Run in changed packages
lerna ls                                 # List packages

# ── LERNA-LITE ──────────────────────────────────────
pnpm lerna changed                       # List changed packages
pnpm lerna version                       # Create version commit + tag
pnpm lerna publish                       # Publish + create GitHub release

# ── RUSH ────────────────────────────────────────────
rush update                              # Install/update dependencies
rush build                               # Build in dependency order
rush build --to @myorg/web               # Build up to web
rush build --impacted-by @myorg/utils    # Rebuild consumers of utils
rush rebuild                             # Force full rebuild
rush check                               # Validate dependency consistency
rush list                                # List projects
rush change                              # Create change log entry
```
