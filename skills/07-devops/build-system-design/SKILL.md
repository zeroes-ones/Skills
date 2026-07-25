---
name: build-system-design
description: >
  Use when build times exceed 5 minutes for incremental builds or 30 minutes for
  clean builds; when evaluating build system options (Bazel, Buck2, Pants, Nx,
  Turborepo, Make) for a codebase; when planning a build system migration or
  modernization; when designing build infrastructure for a monorepo with 50+
  engineers; when build flakiness or non-determinism is causing CI failures;
  when build caching benefits are under investigation; or when scaling build
  infrastructure for remote execution. Handles build system taxonomy and
  selection (task-based vs artifact-based vs convention-based), hermetic build
  design for deterministic caching and reproducibility, incremental build
  optimization (dependency tracking, content-addressable caching, remote caching
  with Bazel REAPI/BuildBarn/BuildBuddy), remote execution architecture for
  large monorepos, build graph analysis (critical path, parallelism tuning, test
  sharding), multi-language build coordination (cross-compilation, protobuf,
  FFI), build rule authoring (Starlark for Bazel, plugin design for
  Pants/Buck2), migration planning to artifact-based systems (cost estimation,
  timeline, tooling: Kythe/buildifier), and anti-pattern recognition (when Bazel
  is overkill and Make is correct). Do NOT use for monorepo tooling selection
  (route to monorepo-manager), CI/CD pipeline optimization (route to
  ci-cd-builder), compiler optimization (route to performance-engineer), or task
  runner configuration within an existing build system.
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: devops
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - build-systems
  - bazel
  - buck2
  - pants
  - make
  - ninja
  - nx
  - turborepo
  - hermetic-builds
  - remote-execution
  - monorepo
  - build-performance
  - caching
  - starlark
token_budget: 4500
chain:
  consumes_from:
    - monorepo-manager
    - ci-cd-builder
    - performance-engineer
  feeds_into:
    - ci-cd-builder
    - monorepo-manager
    - platform-engineer
  alternatives: []
---
# Build System Design

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end build system architecture and engineering — from taxonomy and selection through hermetic design, remote execution, and large-scale migration. Covers the full build system design space: task-based (Make, Just), artifact-based (Bazel, Buck2, Pants), and convention-based (Cargo, Go) systems. Focus on engineering tradeoffs, measurable ROI, and operational excellence — not religious tool debates.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that detect dangerous build advice before it is given. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to recommend Bazel for teams under 10 engineers without extraordinary justification. Bazel's maintenance burden (~0.5-1 FTE for BUILD file hygiene, toolchain upgrades, Starlark rule maintenance) outweighs benefits at small scale. | Trigger: response recommends Bazel/Buck2/Pants AND team size < 10 AND no mention of maintenance cost | STOP. Respond: "Artifact-based build systems (Bazel, Buck2, Pants) require ~0.5-1 dedicated FTE for ongoing maintenance beyond initial migration. At your team size, this represents 5-10% of total engineering capacity. Consider whether Make/Ninja with a caching layer meets your needs, or whether Nx/Turborepo (for JavaScript/TypeScript) provides sufficient incremental benefits at 10x lower maintenance cost." |
| R2 | REFUSE to recommend build system migration without quantifying current pain. Build migrations cost $50K-$500K+ in engineering time. | Trigger: response recommends migration AND no quantification of current build pain (time wasted waiting, CI cost, flakiness rate) | STOP. Respond: "Build migration is a $50K-$500K+ investment. Before recommending migration, quantify current pain: (1) Average incremental build time, (2) Average clean build time, (3) CI build cost per month, (4) Flakiness rate (% of builds that fail for non-code reasons), (5) Engineer-hours lost per week. Only proceed if quantified savings exceed migration cost within 18 months." |
| R3 | REFUSE to design non-hermetic builds for any system where caching or remote execution matters. Non-hermetic builds produce non-deterministic outputs that break caching and enable supply chain attacks. | Trigger: response describes build that accesses network during compilation OR depends on system-installed tools without version pinning | STOP. Respond: "Non-hermetic builds are non-deterministic by definition. They break content-addressable caching (different outputs for same inputs), disable remote execution (workers may have different environments), and create supply chain risks (network access during build). Every build target must declare all inputs explicitly. Use sandboxed execution (Bazel --spawn_strategy=sandboxed, Docker containers for Make) and pin all toolchain versions." |
| R4 | REFUSE to recommend remote execution without first mastering local caching. Remote execution amplifies configuration problems — not solves them. | Trigger: response recommends remote execution (BuildBarn, BuildBuddy, REAPI) AND no mention of local caching maturity | STOP. Respond: "Remote execution amplifies every build configuration problem. If your local cache hit rate is below 80%, remote execution will be slower and more expensive than local builds (network transfer overhead, cold worker environments). First: achieve >90% local cache hit rate with hermetic builds, optimize dependency granularity, remove unnecessary dependencies. Then evaluate remote execution." |
| R5 | DETECT when build graph optimization is suggested without profiling. Guessing the critical path wastes engineering time. | Trigger: response recommends parallelism tuning, test sharding changes, or dependency refactoring AND no mention of build profiling data | STOP. Respond: "Build optimization without profiling data is guessing. Generate a build trace first: `bazel build --profile=profile.json`, then analyze with chrome://tracing or Bazel's analyzer. Identify: (1) Critical path duration, (2) Top 5 longest actions, (3) Cache hit rates per target, (4) Test shard execution time variance. Only optimize after profiling confirms the bottleneck." |
| R6 | REFUSE to recommend "we'll just write a custom build system." Build systems are harder than they look — Google spent 10+ years evolving Blaze/Bazel. | Trigger: response suggests writing a custom build system from scratch | STOP. Respond: "Custom build systems are almost always a mistake. Google's Blaze (now open-sourced as Bazel) took 10+ years to mature. Facebook's Buck took 5+ years. You will rediscover every footgun: incremental correctness bugs, caching invalidation edge cases, cross-platform toolchain hell, Starlark/extension design mistakes. If no existing system fits, extend Bazel with custom rules (Starlark) or adapt Pants with plugins. The extension APIs exist precisely to avoid custom build systems." |
| R7 | DETECT when "let's just add caching" is proposed without addressing build correctness. Caching an incorrect build makes it faster to produce wrong answers. | Trigger: response recommends remote caching, shared caches, or cache infrastructure AND no verification that builds are hermetic and deterministic | STOP. Respond: "Caching a non-deterministic build is dangerous. A shared cache propagates non-reproducible outputs across the entire team — one engineer's environment leak (homebrew library path, different compiler version) poisons the cache for everyone. Before adding caching: verify build determinism by running the same build twice on different machines, comparing output hashes. Only when outputs are bit-for-bit identical is caching safe." |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

You are a build system engineer who has lived through migrations, debugged non-deterministic failures at 2 AM, and watched build times silently destroy engineering velocity. Your mental model:

* **Build time is wasted engineering time.** An engineer waiting 10 minutes for a build 15 times per day loses 2.5 hours. At $150/hour fully loaded, that is $375/day per engineer. Across 50 engineers, that is $18,750/day. Build optimization has direct, measurable ROI.
* **Correctness enables speed, not the reverse.** A fast incorrect build is worse than a slow correct one. Non-deterministic builds produce "works on my machine" bugs that waste orders of magnitude more time than the build itself saved.
* **The build graph is the single source of truth.** If the dependency graph is wrong, everything downstream is wrong — caching, incrementality, remote execution, test selection. Invest in graph correctness first, optimization second.
* **Every build system has a complexity budget.** Adding features (code generation, multi-language, cross-compilation) consumes this budget. When exceeded, the build system becomes the bottleneck. Know when the complexity cost exceeds the feature benefit.
* **Simple systems scale down. Complex systems scale up. Neither scales both.** Make scales down to personal projects. Bazel scales up to Google's monorepo. Nx scales across the middle. Choose based on your trajectory, not your current state.

## Operating at Different Levels

* **Quick scan (30s):** Profile build times — incremental and clean. Check cache hit rate. Check for non-hermetic patterns (network access, system tools, unversioned dependencies). Identify the build system in use and whether it matches the team's scale.
* **Triage (10min):** Generate build trace, analyze critical path. Identify top 5 slowest targets. Calculate engineer-hours lost to build waiting. Check if caching is configured. Assess hermeticity.
* **Deep design (full session):** Full build system evaluation: taxonomy assessment, migration cost/benefit analysis, BUILD file architecture, remote execution design, custom rule authoring, CI integration plan, migration roadmap with milestones.
* **Crisis mode (build broken, CI red, release blocked):** Triage build failure. Check for non-determinism (run same build 3 times — does it fail consistently?). Isolate to specific target with `--noshow_progress` + `--test_filter`. Rollback to last green commit immediately, debug offline.

### Scale Depth

#### Solo (1-5 engineers, single language)
Use the language-native build tool: Cargo for Rust, Go modules for Go, Poetry for Python. Add a Makefile for convenience targets (build, test, lint). No need for Bazel — the overhead exceeds the benefit below 50K LOC.

#### Small Team (5-20 engineers, 1-2 languages)
Adopt a task-based build system with caching: Gradle (JVM), Bazel with `rules_*` for Python/Go, or Nx/Turborepo (JavaScript). Implement local build caching. Benchmark incremental build times monthly: target < 30 seconds for a single-file change. **Transition trigger:** When clean build exceeds 5 minutes, invest in remote caching.

#### Medium Org (20-200 engineers, polyglot)
Artifact-based build system (Bazel, Buck2, Pants). Remote cache deployed. Hermetic builds enforced in CI. Build graph optimization: dependency pruning, critical path analysis, test sharding with shard count tuned per target. Build cop rotation established. **Transition trigger:** When CI build time exceeds 15 minutes with caching, evaluate remote execution.

#### Enterprise (200+ engineers, multi-team monorepo)
Remote execution deployed (BuildBarn, BuildBuddy, custom REAPI workers). Custom Starlark rules for org-specific build patterns. Build artifact signing and provenance attestation. Build health dashboard with SLOs: p95 incremental build < 30s, p95 CI build < 10 min, flakiness < 0.1%. BUILD file semantic validation in CI beyond buildifier. Annual build system health review with migration evaluation (is Bazel still the right choice?). **Transition trigger:** When the build team becomes a bottleneck for feature teams, invest in self-service build infrastructure and BUILD file ownership per team.

## When to Use

Use build-system-design when making build infrastructure decisions that affect the entire engineering organization — the focus is on system-level architecture, not individual build file maintenance.

* Evaluating build systems: Bazel vs Buck2 vs Pants vs Make vs Nx vs Turborepo for your specific codebase characteristics
* Diagnosing slow builds: incremental build > 5 minutes or clean build > 30 minutes
* Planning a migration: from Maven/Gradle/CMake/Make to an artifact-based system
* Designing hermetic builds: sandboxing, deterministic outputs, no network access during compilation
* Implementing caching: local disk cache, remote shared cache (Bazel, sccache), content-addressable storage
* Scaling to remote execution: BuildBarn, BuildBuddy, custom REAPI workers — when local builds are insufficient
* Authoring custom build rules: Starlark (Bazel), Pants plugins, Buck2 rule definitions
* Optimizing build graphs: dependency pruning, parallelism tuning, test sharding, critical path analysis
* Multi-language builds: coordinating C++, Java, Python, Go, Protobuf generation in one build graph
* Training teams: BUILD file hygiene, buildifier, build cop rotation, build health dashboards

Do NOT use build-system-design for monorepo tooling and workspace management (route to monorepo-manager). Do NOT use for CI/CD pipeline design (route to ci-cd-builder). Do NOT use for compiler flag optimization (route to performance-engineer). Do NOT use for task runner configuration (e.g., how to write a package.json script).

## Route the Request

#

## Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("BUILD" OR "BUILD.bazel" OR "WORKSPACE" OR "MODULE.bazel")` | Bazel project detected -> Go to **Core Workflow: Phase 1 — Build System Audit** |
| A2 | `file_exists("BUCK" OR "BUCK2" OR ".buckconfig")` | Buck2 project detected -> Go to **Core Workflow: Phase 1 — Build System Audit** |
| A3 | `file_exists("pants.toml" OR "BUILD.pants")` | Pants project detected -> Go to **Core Workflow: Phase 1 — Build System Audit** |
| A4 | `file_exists("Makefile" OR "GNUmakefile")` AND `! file_exists("BUILD")` | Make-based project -> Go to **Decision Trees: Migration Readiness Assessment** |
| A5 | `file_exists("nx.json" OR "turbo.json")` | JavaScript/TypeScript monorepo -> Route to monorepo-manager, offer build-system-design for Nx/Turborepo build optimization |
| A6 | `file_contains("*.gradle", "build.gradle")` OR `file_exists("pom.xml")` | JVM project -> Go to **Decision Trees: JVM Build Migration** |
| A7 | No build system files detected | New project or exploratory -> Go to **Decision Trees: Build System Selection** |

#

## Intent Route (Ask the User)

```
What build system task are you working on?
|-- Evaluating build systems for a new/existing project -> Jump to "Decision Trees: Build System Selection"
|-- Diagnosing slow build times -> Go to "Core Workflow: Phase 1 — Build System Audit"
|-- Planning a migration (Make -> Bazel, Gradle -> Bazel, etc.) -> Jump to "Decision Trees: Migration Readiness"
|-- Designing incremental/hermetic builds -> Go to "Core Workflow: Phase 2 — Hermetic Build Design"
|-- Setting up remote execution -> Jump to "Decision Trees: Remote Execution Readiness"
|-- Authoring custom build rules -> Go to "Core Workflow: Phase 3 — Custom Rules"
|-- Optimizing build graph (critical path, parallelism) -> Go to "Core Workflow: Phase 4 — Graph Optimization"
|-- Multi-language build coordination -> Jump to "Decision Trees: Multi-Language Strategy"
|-- Emergency: build broken, CI red -> Go to "Core Workflow: Crisis Mode"
```

## Core Workflow **(STANDARD)**
<!-- Full 125 lines extracted to references/core-workflow.md -->

#

## Phase 1: Build System Audit
Execute in order. Do not skip steps.
1. CAPTURE BASELINE METRICS
2. PROFILING — IDENTIFY THE BOTTLENECK
...
> 📎 **[references/core-workflow.md](references/core-workflow.md)** — 125 lines of detailed guidance

## Decision Trees **(QUICK)**

#

## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| `bazel build //...` takes 12 minutes locally but 90 minutes in CI — every target rebuilds from scratch on every CI run | The CI runner doesn't persist the Bazel disk cache between runs. Each CI job starts with a clean workspace, so Bazel has no cached action results and rebuilds everything. | Configure `--disk_cache=/mnt/bazel-cache` pointing to a persistent volume. Or use `--remote_cache=grpc://buildcache:9092` with a remote cache service (bazel-remote, Buildbarn). Verify with `bazel clean && bazel build //...` — second build should be instant. | Build system caching is CI infrastructure, not a build config file. If your CI runner doesn't survive between jobs, your build cache doesn't either. |
| Full `pnpm install` adds 30 seconds to every PR — 400 developers × 15 PRs/week × 30s = 50 hours/week of CI time wasted on dependency installs | The CI pipeline runs `pnpm install` unconditionally before every job, even when `pnpm-lock.yaml` hasn't changed since the last run. | Use Nx/Turborepo affected detection: `nx affected:test --base=main` with compute hashing. Cache `node_modules` keyed on lockfile hash. When the lockfile hasn't changed, the install step completes in 1 second from cache. | Every second of CI time multiplied by team size × PR frequency is real money. The build system's job is to skip work that's already been done. |
| Bazel remote execution shows `DEADLINE_EXCEEDED` for all actions — 0 build progress after 10 minutes | The remote execution cluster was scaled to 0 by an autoscaler that didn't understand build traffic patterns. No RE workers available, so every action queues indefinitely. | Configure minimum instance count on the RE worker pool to 1 during business hours. Add a health check endpoint that the build system probes before starting: `bazel build --remote_executor=grpc://re-cluster:8980 --remote_timeout=30`. A 30-second timeout with a clear error beats infinite hang. | Autoscalers are designed for web traffic — request-response patterns with 100ms latencies. Build remote execution has 10-60 second action runtimes. Autoscalers will always get this wrong unless you add minimums. |
| Migrating from Make to Bazel — 6 weeks in, half the team writes `genrule` wrappers around the old Makefile instead of writing BUILD files | The migration plan didn't include a "stop the clock" rule: new targets must be Bazel-native, no genrule escapes. Engineers defaulted to what they knew under deadline pressure. | Enforce a Bazel lint rule: `bazel_skylib` `genrule` check that blocks PRs with `genrule` that wraps `make`. Provide a one-pager per language: "How to Bazel-build a Go binary" / "How to Bazel-build a Python wheel." A template beats a blank page every time. | Migration strategy is more important than build system selection. The best build system in the world won't help if engineers route around it with escape hatches. |
| Nx affected graph shows every project as affected — `nx affected:lint` lints all 200 projects even when only 3 files changed | The `nx.json` implicit dependencies list is empty. Nx can't know that `package.json` changes in the root affect all projects, so it defaults to "everything is affected" as a safe fallback. | Define `targetDefaults` in `nx.json` with `dependsOn` chains. Run `nx graph` to visualize the dependency graph — verify that changing one file only highlights the projects that actually depend on it. | An overly safe affected graph is indistinguishable from no affected graph at all. The system that runs everything "just in case" is the system that gets ignored. |

## Build System Selection

```
How large is your team and codebase?
|-- < 10 engineers, < 100K LOC, single language
|   |-- C/C++: Make or CMake + Ninja. Simple, fast, universally understood.
|   |-- Go: Go build. Convention-based, zero config. Do not over-engineer.
|   |-- Rust: Cargo. Convention-based. Build scripts handle native deps.
|   |-- Python: setuptools/poetry/uv. No build graph complexity needed.
|   |-- JavaScript/TypeScript: package.json scripts + tsc/esbuild. Nx only if monorepo.
|   |-- JVM: Gradle or Maven. Mature, well-supported, IDE integration.
|   |-- DO NOT use Bazel/Buck2/Pants at this scale unless you have a specific reason.
|
|-- 10-50 engineers, 100K-1M LOC, polyglot or growing monorepo
|   |-- JavaScript/TypeScript monorepo: Nx or Turborepo. Task-based, fast adoption, excellent DX.
|   |-- Mixed-language growing toward monorepo: Start evaluating Bazel or Pants.
|   |   |-- If C++/Python/Go/Java mix: Bazel has best multi-language support.
|   |   |-- If Python-heavy: Pants has best Python support, simpler than Bazel.
|   |   |-- If JVM-heavy: Bazel rules_jvm_external, or Pants JVM support.
|   |-- Decision gate: do you have 1+ engineer who can own build system health? If no, stick with current system.
|
|-- 50-200 engineers, >1M LOC, polyglot monorepo
|   |-- Strong case for artifact-based system (Bazel, Buck2, Pants)
|   |-- Bazel: best ecosystem (rules_go, rules_python, rules_rust, rules_js), largest community
|   |-- Buck2: performance-focused, Rust-based, uses Starlark. Meta-scale proven.
|   |-- Pants: simpler than Bazel, strong Python and JVM, growing community
|   |-- Key decision factors:
|   |   |-- Language mix priority (which language is primary?)
|   |   |-- Remote execution needs (all three support REAPI)
|   |   |-- Team familiarity with Starlark (all three use it for rules)
|   |   |-- Existing migration tooling (Bazel has Kythe, buildifier, migration guides)
|
|-- 200+ engineers, multi-million LOC
|   |-- Bazel is the safe choice: Google-scale proven, extensive ecosystem
|   |-- Buck2 if Meta-scale performance requirements: Rust daemon, materialized vs virtual files
|   |-- Custom extensions layer over either (not custom build system)
|   |-- Requires dedicated build team (3-5 engineers minimum)
|   |-- Remote execution is mandatory at this scale
```

#

## Migration Readiness Assessment

```
Is your team ready for a build system migration?
|-- Phase 0: Quantify the pain
|   |-- Current incremental build time: _____ seconds
|   |-- Current clean build time: _____ minutes
|   |-- Hours lost per engineer per week: _____
|   |-- Build flakiness rate: _____%
|   |-- Is the pain > $100K/year in lost productivity? (50 engineers × 2 hours/week × $100/hr × 50 weeks)
|   |-- If NO: do not migrate. The migration will cost more than the pain.
|   |-- If YES: proceed to Phase 1.
|
|-- Phase 1: Migration cost estimation
|   |-- Initial conversion: 1-3 months × 2-4 engineers (BUILD files, toolchain setup)
|   |-- Build file maintenance: ongoing ~0.5 FTE minimum
|   |-- CI/CD rework: 2-4 weeks
|   |-- Training: 1-2 weeks for team ramp-up
|   |-- Productivity dip during migration: 20-40% for 2-3 months
|   |-- Total estimated cost: $_____ (include opportunity cost of features not shipped)
|
|-- Phase 2: ROI calculation
|   |-- Expected incremental build time improvement: ___% (typical: 50-80%)
|   |-- Expected CI time improvement: ___% (typical: 40-70% with caching)
|   |-- Expected flakiness reduction: ___% (typical: 80-95% with hermetic builds)
|   |-- Annual savings: (hours saved × hourly cost) + (CI cost reduction)
|   |-- ROI timeline: total cost / annual savings = _____ years
|   |-- PROCEED only if: ROI < 18 months AND team has dedicated build owner
|
|-- Phase 3: Migration strategy selection
|   |-- Big Bang: Convert entire repo at once. Fastest to benefits, highest risk.
|   |   |-- Best for: small repos (<50K LOC), strong leadership support, dedicated migration window
|   |-- Strangler Fig: Convert module by module, both systems coexist.
|   |   |-- Best for: large repos, risk-averse orgs, ongoing feature development
|   |-- Tooling: Kythe for cross-reference, buildifier for BUILD file formatting, Buildozer for bulk edits
```

#

## Remote Execution Readiness

```
Should you invest in remote execution?
|-- Prerequisites (ALL must be true):
|   |-- ☐ Builds are fully hermetic (verified with sandbox_block_network)
|   |-- ☐ Local cache hit rate > 90%
|   |-- ☐ Build graph is correct (no missing dependencies, no over-specified deps)
|   |-- ☐ Remote cache configured and working (cache hit rate > 60%)
|   |-- ☐ Team size > 20 engineers OR build time > 15 min clean
|   |-- If any unchecked: address prerequisites first. Remote execution amplifies problems.
|
|-- Cost-benefit analysis:
|   |-- Option A: Managed (BuildBuddy, EngFlow)
|   |   |-- Cost: $200-$500/engineer/month + compute
|   |   |-- Benefit: zero ops burden, excellent UX, built-in analytics
|   |   |-- Best for: teams without dedicated infra engineers
|   |-- Option B: Self-hosted (BuildBarn, bazel-remote, custom REAPI workers)
|   |   |-- Cost: $50-$150/engineer/month compute + 1-2 FTE ops
|   |   |-- Benefit: full control, no data leaving network, potentially cheaper at scale
|   |   |-- Best for: teams with dedicated infra, privacy/security requirements
|   |-- Option C: Hybrid (managed CAS + self-hosted workers)
|   |   |-- Best for: custom worker requirements (GPU, specialized hardware) with managed caching
|
|-- Scaling milestones:
|   |-- 20-50 engineers: remote caching only (sufficient for most)
|   |-- 50-200 engineers: remote execution for CI, local builds for dev
|   |-- 200+ engineers: remote execution for all (dev + CI)
|   |-- 500+ engineers: dedicated build cluster, BuildBarn/BuildBuddy enterprise
```

#

## Build System Anti-Patterns

```
Common build system mistakes and how to fix them:
|-- Anti-Pattern: Monolithic targets (one BUILD target for entire module)
|   |-- Symptom: changing any file rebuilds everything
|   |-- Fix: split into focused libraries by responsibility
|   |-- Before: cc_library(name="all", srcs=glob(["**/*.cc"])) — 50 files, 1 target
|   |-- After: 10 cc_library targets, 5 files each, focused deps
|   |-- Benefit: 10x reduction in incremental build time

|-- Anti-Pattern: Overly broad visibility (default_visibility = ["//visibility:public"])
|   |-- Symptom: circular dependencies, accidental coupling, impossible to refactor
|   |-- Fix: explicit visibility per target, default to private
|   |-- Rule: new targets default to private. Explicitly grant visibility to known consumers.
|   |-- Benefit: prevents dependency graph rot, enables safe refactoring

|-- Anti-Pattern: genrule abuse (using genrule for code generation, templating, file copy)
|   |-- Symptom: non-hermetic builds, undeclared inputs, impossible to cache
|   |-- Fix: use purpose-built rules (expand_template, http_file, custom Starlark rules)
|   |-- genrule should be the LAST resort, not the first tool
|   |-- Benefit: hermeticity, caching, remote execution compatibility

|-- Anti-Pattern: Floating external dependencies (git_repository with no commit/tag pin)
|   |-- Symptom: builds break spontaneously when upstream changes
|   |-- Fix: pin ALL external deps with commit SHA + sha256 hash
|   |-- WORKS: http_archive(url=..., sha256="abc123...")
|   |-- BROKEN: git_repository(remote=..., branch="main")
|   |-- Benefit: reproducible builds forever

|-- Anti-Pattern: BUILD file copypasta (copy-pasting BUILD rules between targets)
|   |-- Symptom: inconsistent conventions, repeated mistakes at scale
|   |-- Fix: use macros (.bzl functions) for repeated patterns, custom rules for new concepts
|   |-- Write a macro once, use it 100 times. One place to fix bugs.
|   |-- Benefit: consistency, single source of truth for common build patterns
```

#

## Build vs Buy: Custom Rules vs External Tools

```
Should you write a custom build rule or integrate an external build tool?
|-- WRITE A CUSTOM RULE (Starlark/Pants plugin/Buck2 rule) when:
|   |-- The tool generates files consumed by other build targets
|   |-- The tool's inputs are BUILD dependencies (need automatic rebuild on change)
|   |-- The tool needs to participate in the build graph (caching, remote execution)
|   |-- The tool is simple: 1 input → 1 output, no complex configuration
|   |-- Example: protobuf code generation, OpenAPI client generation, asset compilation

|-- WRAP AN EXTERNAL TOOL (genrule with declared inputs/outputs) when:
|   |-- The tool is complex and not worth reimplementing (e.g., webpack, CMake)
|   |-- The tool has its own caching that can't be replicated
|   |-- The tool generates many outputs with complex interdependencies
|   |-- The tool changes rapidly and keeping a custom rule in sync is too expensive

|-- KEEP THE TOOL OUTSIDE THE BUILD SYSTEM (run in CI before/after build) when:
|   |-- The tool does not produce build artifacts (linting, formatting, documentation gen)
|   |-- The tool's output is not consumed by other build targets
|   |-- The tool is slow (>30 seconds) and not on the critical path
|   |-- Example: ESLint, Prettier, documentation generators, Docker image builds

|-- DECISION MATRIX:
|   |-- Tool output consumed by build targets? YES + simple = custom rule. YES + complex = genrule wrapper.
|   |-- Tool output consumed by build targets? NO → run outside build system (CI step, pre-commit hook)
|   |-- Tool needs build cache participation? YES → custom rule (declare inputs/outputs). NO → external.
|   |-- Team has Starlark expertise? YES → custom rule. NO → maintain simpler approach.
```

## Best Practices

1. **Design for incremental builds from day one.** Every target must declare its exact inputs (deps, srcs, data) and outputs. When a single `.cc` file changes, only affected targets rebuild — not the entire project. Incremental build time is the #1 developer experience metric.

2. **Achieve hermetic builds: no network, no system tools, no timestamps.** Run `bazel build --sandbox_block_network //...` and it must pass. Hermetic builds guarantee reproducibility — the same commit builds identically on any machine, any CI runner, 6 months later.

3. **Use content-addressable caching: remote cache before remote execution.** Deploy a remote cache (bazel-remote, BuildBuddy) before investing in remote execution. A 94% cache hit rate on CI saves more money than 200 parallel workers. Remote execution is the scaling lever; remote cache is the efficiency lever.

4. **Pin external dependencies with content hashes, not branch references.** `git_repository` pointing to `master` in WORKSPACE is non-reproducible. Use Bzlmod/MODULE.bazel with `integrity = "sha256-..."`. Every external dependency must be pinned to an exact version with a verified hash.

5. **Author custom build rules for repeated patterns, not one-off genrules.** A `genrule` with a 10-line `cmd` that copies boilerplate across 50 targets is a maintenance liability. Write a Starlark rule that declares its interface once: inputs, outputs, toolchain dependencies. Custom rules pay for themselves after the third use.

6. **Test sharding requires test isolation.** Before enabling `--test_sharding`, verify no test shares state (database, temp files, environment variables) with another test. Tests that pass serially and fail under sharding are Heisen-failures — the hardest flakiness to debug.

7. **Keep BUILD files minimal: one target per conceptual unit, not one target per file.** Over-granular BUILD files create phantom rebuilds from over-specified deps. `//foo:bar` when you only need `//foo:bar:types` means changing `bar`'s implementation rebuilds your target unnecessarily. Declare `deps` on the narrowest target that provides what you need.

8. **Validate build graph correctness in CI.** Buildifier formats BUILD files but doesn't validate `deps` completeness, visibility correctness, or glob scope. Add `bazel query 'deps(//...)' --output=graph` to CI to catch missing and unused dependency edges. The linter passing is necessary but not sufficient.

9. **Cross-compile for deployment targets in the build system, not in Dockerfiles.** Define platform toolchains (linux_amd64, linux_arm64) in the build graph. Docker builds become `bazel build //... --platforms=@io_bazel_rules_go//go/toolchain:linux_amd64` — no separate cross-compilation step.

10. **Sign build artifacts at creation time.** Attach a cryptographic signature to every release artifact. The build system (not CI glue scripts) should produce a signed artifact + provenance attestation. An unsigned artifact is indistinguishable from a compromised one.

## Error Recovery **(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| Monorepo with 50+ engineers evaluating Bazel vs Nx | monorepo-manager | Nx handles JS/TS monorepo tooling; if polyglot, Bazel is the architectural choice |
| CI/CD pipeline build stage optimization | ci-cd-builder | CI caching, artifact storage, build matrix strategies |
| Compiler-level performance (LTO, PGO) within build system | performance-engineer | Link-time optimization, profile-guided optimization integration |
| Docker-based build containers and hermetic toolchains | docker-kubernetes | Toolchain container images, CI build environments |
| Build system health dashboards and monitoring | observability-engineer | Build time metrics, cache hit rate dashboards, alerting on build regressions |
| Platform engineering team building internal build service | platform-engineer | Developer portal integration, golden build paths, self-service build infrastructure |
| Cross-compilation for embedded or mobile targets | mobile-developer, firmware-developer | NDK cross-compilation, iOS/macOS universal binaries, ARM/RISC-V targets |
| JVM build migration from Gradle/Maven to Bazel | backend-developer | JVM-specific Bazel rules, dependency management, annotation processing |

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `cloud-architect` | Infrastructure design, networking, IAM, cost model | Before provisioning infrastructure or designing deployment pipelines |
| `ci-cd-builder` | Pipeline design, build optimization, deployment strategies | Before designing CI/CD workflows |

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | BUILD files contain `srcs = glob(["**/*.java"])` (overly broad globs) | [ALERT] Overly broad globs cause unnecessary rebuilds when ANY file in directory changes. Prefer explicit file lists or narrow globs. |
| P2 | Build target has >100 direct dependencies (`deps` list) | [WARN] Large deps lists increase critical path and reduce incrementality. Consider splitting into smaller, focused targets. |
| P3 | `WORKSPACE` file exists but no `MODULE.bazel` (pre-Bazel 7, no Bzlmod) | [INFO] Bzlmod (MODULE.bazel) replaces WORKSPACE in Bazel 7+. Plan migration for better dependency management and reproducible builds. |
| P4 | Cache hit rate < 50% in CI | [ALERT] Low cache hit rate wastes CI minutes and money. Audit: are inputs deterministic? Are cache keys stable? Is cache storage working? |
| P5 | Test target takes >60 seconds with no sharding | [WARN] Consider sharding this test target. A 5-minute test suite with 4 shards can run in 75 seconds on remote execution. |
| P6 | Build contains `genrule` with `cmd = "curl ..."` (network access in build) | [ALERT] genrule with network access breaks hermeticity. Replace with http_file/http_archive or pre-downloaded dependencies. |

## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

#

## How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "build-system-design",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

#

## State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

#

## Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## Production Checklist **(STANDARD)**

- [ ] **[BS1]** Hermeticity verified: `bazel build --sandbox_block_network //...` passes — no network access, no system tool leaks, no timestamp embedding
- [ ] **[BS2]** Determinism verified: two consecutive builds on the same machine produce bit-for-bit identical outputs — diff of `bazel-bin/` is empty
- [ ] **[BS3]** Incremental build time < 10 seconds for a single-file change in a leaf library — only affected targets and their direct dependents rebuild
- [ ] **[BS4]** Remote cache deployed and configured — cache hit rate > 80% for incremental changes, > 90% for clean CI builds
- [ ] **[BS5]** External dependencies pinned with content hashes via Bzlmod/MODULE.bazel (Bazel), no `git_repository` pointing to branches — reproducible builds guaranteed
- [ ] **[BS6]** Build graph validated in CI: `bazel query 'deps(//...)' --output=graph` returns zero missing dependency edges and zero unused deps
- [ ] **[BS7]** Test sharding enabled only after test isolation audit — zero shared-state tests, all tests pass 100% under `--test_sharding`
- [ ] **[BS8]** Custom Starlark rules for repeated patterns — no genrule with >5-line `cmd`, no copy-pasted build logic across targets
- [ ] **[BS9]** Cross-compilation toolchains defined for all deployment platforms — Dockerfiles use `bazel build` output, not separate compilation steps
- [ ] **[BS10]** Build artifacts cryptographically signed at creation time — provenance attestation generated alongside every release artifact
- [ ] **[BS11]** Build dashboard visible to all engineers: cache hit rates, build times per target, flakiness rate, CI build duration trend — reviewed weekly by build cop
- [ ] **[BS12]** Build cop rotation established: 1 engineer/week maintains BUILD file hygiene, toolchain updates, flaky test quarantine — no centralized build team bottleneck
- [ ] **[BS13]** Buildifier and gazelle configured in CI — formatting enforced, but semantic checks (dep completeness, visibility) run separately
- [ ] **[BS14]** Migration readiness (if planning): current pain quantified in $, migration cost estimated, projected ROI timeline < 18 months — all three documented in decision record

## What Good Looks Like

```
Ideal build system state (artifact-based, 200 engineers, polyglot monorepo):

Incremental build:
  Change one .cc file -> build and test affected targets only -> 8 seconds
  (Bazel correctly identifies 3 dependent targets, runs them in parallel)

Clean build with remote execution:
  bazel build //... --config=remote -> 4 minutes (200 workers in parallel)
  (Local clean build would take 45 minutes)

CI integration:
  PR opens -> CI runs `bazel test //...` -> 6 minutes with remote execution
  Cache hit rate: 94% (only changed targets re-execute)

Build health:
  Hermetic: $ bazel build --sandbox_block_network //... -> SUCCESS
  Deterministic: build twice, `diff -r bazel-bin/` -> no differences
  Flakiness: <0.1% (one flaky build per 1,000)

Engineer experience:
  Build cop rotation: 1 engineer/week maintains build health (BUILD file hygiene, toolchain updates)
  Build dashboard: cache hit rates, build times, flakiness—visible to entire org
  Migration complete: no Makefiles, no Gradle scripts, no ad-hoc scripts in CI
```

## Deliberate Practice

```
Phase 1: Single-language repo, no build system
  Makefile -> 3 targets, 5 source files -> 2 second build
  Goal: Understand task-based builds, dependency declaration

Phase 2: Add Bazel to existing C++ project
  10 cc_library targets, 3 cc_binary targets, 5 cc_test targets
  Goal: Learn BUILD file structure, deps declaration, test integration

Phase 3: Break hermeticity, then fix it
  Intentionally add: genrule with curl, system() call, timestamp embedding
  Fix each: http_archive, hermetic toolchain, SOURCE_DATE_EPOCH
  Goal: Internalize why hermeticity matters

Phase 4: Remote caching setup
  Start bazel-remote Docker container, configure --remote_cache
  Build with cache, clear local cache, rebuild from remote
  Goal: Cache hit/miss patterns, cache debugging

Phase 5: Custom Starlark rule
  Write a rule that generates code from protobuf
  Handle: toolchain selection, dependency propagation, output declaration
  Goal: Understand rule authoring API, provider model

Phase 6: Full migration simulation
  Take a real 5K LOC Make project, estimate migration cost
  Write BUILD files, verify hermeticity, benchmark improvement
  Goal: End-to-end migration experience before doing it for real
```

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "We'll migrate to Bazel next quarter — the Makefile still works." | Next quarter becomes next year. 45-minute build times × 20 engineers × $150/hr = $22,500/day in lost productivity. 6 months of delay = $150K+ in wasted engineering time with nothing to show for it. |
| "Remote caching and execution are optimizations — we'll add them later." | Without remote caching, CI compute costs 3-5x what they should. A 50-engineer org burning $15K/month on CI runners can cut that to $4K/month. Delaying 6 months = $66K in unnecessary compute spend. |
| "BUILD file maintenance is the build team's job." | Centralizing BUILD ownership creates a single bottleneck. Feature teams blocked 2-4 hrs/week waiting on build fixes = $50K-$120K/year in idle engineering capacity. Every team owns their own BUILD files. |
| "We'll autogenerate BUILD files later — manual is fine for now." | Manual BUILD files at scale accumulate stale deps, missing visibility, and incorrect globs. Fixing 200+ stale BUILD files after a migration = $40K-$80K in one-time cleanup that could have been automated from day one. |
| "Buildifier makes our BUILD files correct — the linter passes." | Buildifier only formats. It doesn't validate dep completeness, visibility correctness, or glob scope. Teams that trust buildifier alone ship broken builds that "look right" — $15K-$50K in debugging non-obvious failures over 6 months. |

## Anti-Patterns

### Anti-Pattern: Migrating to Bazel Without Training Budget
**What it looks like:** Org decides "we're migrating to Bazel." Engineers get a wiki link and are expected to learn on the job. BUILD files are cargo-culted from existing targets.
**Why it fails:** Engineers take 2-4 weeks to become productive with BUILD files and Starlark. At $150/hr, that's $12K-$24K per engineer in ramp-up cost. Within 6 months, the build graph is worse than before the migration — stale deps, incorrect visibility, overly broad globs. $50K-$150K in build graph cleanup.
**Do this instead:** Budget 2 weeks of dedicated training per engineer before the migration starts. Pair every engineer with a build expert for the first month. Run weekly BUILD file hygiene reviews for 3 months post-migration. Never migrate during a hiring push.

### Anti-Pattern: Trusting Buildifier for Correctness
**What it looks like:** CI runs `buildifier -lint=warn` on BUILD files. The linter passes. Team assumes BUILD files are correct.
**Why it fails:** Buildifier only formats. It does not check deps completeness, visibility correctness, or glob scope. Teams that trust buildifier alone ship broken builds that "look right." $15K-$50K in debugging non-obvious failures over 6 months.
**Do this instead:** Run `buildifier` for formatting AND `bazel query` for semantic validation. Check for missing deps, unused deps, and visibility violations in CI. Buildifier is necessary but not sufficient.

### Anti-Pattern: Enabling Remote Execution Before Fixing Flakiness
**What it looks like:** Team wants faster CI, so they enable remote execution with 200 workers. Tests that "pass almost always" locally now fail regularly due to timing differences.
**Why it fails:** A test that passes 98% locally fails 2% × 200 workers = 4 failures per build on remote execution. Each investigation costs $150-$500. Cumulative cost: $30K-$100K/year in flake investigation.
**Do this instead:** Achieve >99.9% test reliability locally before enabling remote execution. Quarantine flaky tests. Run test suite 100x locally to establish baseline reliability. Only then scale horizontally with remote execution.

### Anti-Pattern: WORKSPACE with Unpinned Git Dependencies
**What it looks like:** `git_repository(name = "some_dep", remote = "...", branch = "master")` in WORKSPACE. Builds rely on whatever HEAD is at the time.
**Why it fails:** Six months later, nobody knows which version was used. The build is non-reproducible. Migrating to Bzlmod/MODULE.bazel requires restructuring the entire dependency graph. $20K-$80K in migration and debugging.
**Do this instead:** Pin every external dependency with a content hash. Use Bzlmod/MODULE.bazel with `integrity = "sha256-..."`. No branch references. No floating tags.

### Anti-Pattern: Over-Specified Deps Causing Phantom Rebuilds
**What it looks like:** `deps = ["//foo:bar"]` when only `//foo:bar:types` is needed. Every change to `bar`'s implementation rebuilds your target.
**Why it fails:** 5 extra deps × 200 targets × 2 min rebuild × 20 changes/day = 6.7 engineer-hours of unnecessary waiting per day. $200K-$500K/year in wasted build time for a 100-engineer org.
**Do this instead:** Declare deps on the narrowest target providing what you need. Use `bazel query 'somepath(//my:target, //foo:bar)'` to identify unnecessary edges. Audit deps quarterly with `unused_deps` in CI.

### Anti-Pattern: Test Sharding Without Isolation Audit
**What it looks like:** Enabling `--test_sharding=4` on a test suite where tests share database state, temp files, or environment variables.
**Why it fails:** Tests pass serially and fail under sharding — the worst kind of flakiness because it's non-deterministic. Finding and fixing shared state across 5,000 tests after sharding is a multi-week effort costing $30K-$75K.
**Do this instead:** Audit test suite for shared state before enabling sharding. Use `--runs_per_test=100` to detect pre-existing flakiness. Each test must be self-contained: no shared database, no temp file collisions, no mutable environment variables.

### Anti-Pattern: ccache as Build System Substitute
**What it looks like:** Builds are slow, so team installs ccache. Build times improve slightly. Team considers the problem solved.
**Why it fails:** ccache operates at the compilation level, not the build graph level. It doesn't help with linking, code generation, or test execution — the parts that dominate build times in large projects. If your Makefile has incorrect dependencies, ccache caches incorrect outputs. $10K-$25K in misdiagnosed build time.
**Do this instead:** ccache is a compiler wrapper, not a build system. Fix the build graph first: correct dependency declarations, fine-grained targets, and artifact-based caching (remote cache). Use ccache as a complementary optimization, not a substitute.

## Verification

After designing or modifying a build system, run this sequence. Do not proceed past a failure.

1. **Hermeticity check:** `bazel build --sandbox_block_network //...` passes with no network access violations. If failures, identify and fix non-hermetic targets.
2. **Determinism check:** Build twice on the same machine, compare output hashes. Build once on two different machines, compare hashes. All outputs must be bit-for-bit identical.
3. **Cache correctness:** Build with remote cache enabled, clear local cache, rebuild. Outputs must match the original. Cache hit rate > 80% for incremental changes.
4. **Incremental build time:** Change one .cc/.java/.py file in a leaf library. Rebuild. Time must be < 10 seconds for an incremental change (single target + direct dependents).
5. **Dependency correctness:** `bazel query 'deps(//...)' --output=graph | grep -c "missing"` returns 0. No missing dependency edges. No unused dependency edges.
6. **Build graph hygiene:** No target has >100 direct deps. No genrule uses network access. All external deps are pinned with content hashes.
7. **Migration readiness:** If planning migration, quantified current pain ($), estimated migration cost ($), and projected ROI timeline (<18 months). All three documented in decision record.

If any check fails: diagnose from verification item, provide specific actionable fix, restart verification from failed item.

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.## References

* [Bazel Official Documentation](https://bazel.build/docs) — Build system, Starlark, remote execution
* [Buck2 Documentation](https://buck2.build/) — Meta's artifact-based build system
* [Pants Build System](https://www.pantsbuild.org/) — Python/JVM-focused build system
* [Bazel Remote Execution API](https://github.com/bazelbuild/remote-apis) — REAPI protocol specification
* [/references/build-system-taxonomy.md](references/build-system-taxonomy.md) — Task-based vs artifact-based vs convention-based comparison matrix
* [/references/hermetic-builds.md](references/hermetic-builds.md) — Hermeticity design patterns, sandboxing, determinism verification
* [/references/incremental-builds.md](references/incremental-builds.md) — Cache strategies, dependency tracking, content-addressable storage
* [/references/remote-execution.md](references/remote-execution.md) — REAPI architecture, managed vs self-hosted, scaling guide
* [/references/build-graph-optimization.md](references/build-graph-optimization.md) — Critical path analysis, parallelism, test sharding
* [/references/multi-language-builds.md](references/multi-language-builds.md) — Cross-compilation, protobuf, FFI coordination
* [/references/build-rules-extensibility.md](references/build-rules-extensibility.md) — Starlark rule authoring, providers, toolchains
* [/references/bazel-migration.md](references/bazel-migration.md) — Migration playbook, cost estimation, tooling
