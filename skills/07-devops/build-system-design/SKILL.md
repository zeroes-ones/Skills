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

### Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("BUILD" OR "BUILD.bazel" OR "WORKSPACE" OR "MODULE.bazel")` | Bazel project detected -> Go to **Core Workflow: Phase 1 — Build System Audit** |
| A2 | `file_exists("BUCK" OR "BUCK2" OR ".buckconfig")` | Buck2 project detected -> Go to **Core Workflow: Phase 1 — Build System Audit** |
| A3 | `file_exists("pants.toml" OR "BUILD.pants")` | Pants project detected -> Go to **Core Workflow: Phase 1 — Build System Audit** |
| A4 | `file_exists("Makefile" OR "GNUmakefile")` AND `! file_exists("BUILD")` | Make-based project -> Go to **Decision Trees: Migration Readiness Assessment** |
| A5 | `file_exists("nx.json" OR "turbo.json")` | JavaScript/TypeScript monorepo -> Route to monorepo-manager, offer build-system-design for Nx/Turborepo build optimization |
| A6 | `file_contains("*.gradle", "build.gradle")` OR `file_exists("pom.xml")` | JVM project -> Go to **Decision Trees: JVM Build Migration** |
| A7 | No build system files detected | New project or exploratory -> Go to **Decision Trees: Build System Selection** |

### Intent Route (Ask the User)

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

## Core Workflow

### Phase 1: Build System Audit

Execute in order. Do not skip steps.

```
1. CAPTURE BASELINE METRICS
   |-- Incremental build time (change one file, rebuild): _____ seconds
   |-- Clean build time (full rebuild from scratch): _____ minutes
   |-- CI build time (including test execution): _____ minutes
   |-- Cache hit rate (local): _____%
   |-- Build flakiness rate (non-code failures / total builds): _____%
   |-- Engineer-hours lost per week = (builds/day × wait_time × engineers × 5) / 60
   |-- Monthly CI spend: $_____
   |-- Benchmark: incremental < 30s excellent, < 2min acceptable, > 5min needs investigation
   |-- Benchmark: clean < 5min excellent, < 15min acceptable, > 30min needs investigation

2. PROFILING — IDENTIFY THE BOTTLENECK
   |-- Generate build trace:
   |   |-- Bazel: bazel build //... --profile=profile.json.gz
   |   |-- Buck2: buck2 build //... --profile profile.json
   |   |-- Make: make -j$(nproc) 2>&1 | ts -s
   |   |-- Nx: nx build --profile profile.json
   |-- Analyze with chrome://tracing or Bazel's analyzer:
   |   |-- Critical path: longest sequential chain of dependencies
   |   |-- Top 10 longest actions (compilation, linking, codegen, test)
   |   |-- Cache hit/miss ratio per target (which targets miss cache and why)
   |   |-- Idle time: when workers are waiting for dependencies
   |-- Identify the binding constraint:
   |   |-- CPU-bound (all cores saturated) -> add parallelism or optimize heavy targets
   |   |-- I/O-bound (disk or network) -> add caching, faster storage
   |   |-- Dependency-bound (long critical path) -> restructure dependencies, split targets
   |   |-- Test-bound (slow tests on critical path) -> shard tests, move to separate phase

3. HERMETICITY AUDIT
   |-- Check for network access during build: bazel build --sandbox_block_network ...
   |-- Check for system tool dependencies: ldd or otool on build outputs
   |-- Check for environment variable leaks: compare build outputs with different PATH, HOME
   |-- Check for timestamp embedding: build twice, compare binary hashes
   |-- Findings: _____ targets are non-hermetic (___% of build graph)
```

### Phase 2: Hermetic Build Design

```
1. ELIMINATE NETWORK ACCESS
   |-- Declare all external dependencies explicitly (WORKSPACE, MODULE.bazel, third_party/)
   |-- Mirror dependencies internally (artifact registry: Artifactory, Nexus, Bazel Central Registry)
   |-- Pin versions with content hashes (never use floating tags like "latest")
   |-- Use --sandbox_block_network to verify no target accesses network

2. ELIMINATE SYSTEM DEPENDENCIES
   |-- Replace system-installed tools with hermetic toolchains:
   |   |-- Bazel: register_toolchains() with pre-built binaries, not /usr/bin/gcc
   |   |-- Container-based: run build in Docker with pinned toolchain image
   |   |-- Nix: nix-shell with pinned nixpkgs commit
   |-- Pin compiler version: rules_go, rules_rust, rules_python all support hermetic toolchains
   |-- For Make: wrap in Docker with --volume mounts for source only

3. ELIMINATE ENVIRONMENT LEAKS
   |-- Use --action_env to explicitly pass only required environment variables
   |-- Never depend on $HOME, $USER, $HOSTNAME in build rules
   |-- Use fixed timestamps for reproducibility: SOURCE_DATE_EPOCH for deterministic builds
   |-- Verify: build on macOS CI and Linux CI — outputs must be identical

4. VERIFY DETERMINISM
   |-- Build twice on same machine: diff outputs (must be bit-identical)
   |-- Build on two different machines: diff outputs (must be bit-identical)
   |-- Build with and without cache: cached output must match uncached output
   |-- If outputs differ: use diffoscope, Bazel's --experimental_execution_log_file to find source
```

### Phase 3: Caching & Incrementality

```
1. LOCAL CACHING FIRST
   |-- Disk cache: --disk_cache=/some/persistent/path (Bazel), ccache/sccache (Make)
   |-- Target: >90% local cache hit rate before considering remote caching
   |-- Cache size management: set max cache size, LRU eviction
   |-- Benchmark: second build after cache warm should be <10% of first build

2. REMOTE CACHING
   |-- Options: Bazel Remote Cache API (nginx, BuildBarn CAS, BuildBuddy, bazel-remote)
   |-- Decision: shared CI cache vs team-wide cache
   |   |-- CI-only: simplest, no cross-machine poisoning risk
   |   |-- Team-wide: faster for everyone, requires strict hermeticity
   |-- Network cost: cache upload/download bandwidth. 100MB output × 1000 builds/day = 100GB.
   |-- Cache poisoning recovery: ability to invalidate by target, by user, by time range

3. INCREMENTAL BUILD OPTIMIZATION
   |-- Dependency granularity: split large targets into smaller ones
   |   |-- Single 50K line cc_library -> 10 libraries of 5K lines each
   |   |-- Benefit: changing one file rebuilds 1/10th the code
   |   |-- Cost: more BUILD files to maintain, marginally slower graph resolution
   |-- Header hygiene (C/C++): include-what-you-use, forward declarations, precompiled headers
   |-- Unnecessary dependency pruning: bazel query 'deps(//target)' and remove unused edges
   |-- Test-only changes: --test_filter to run only affected tests, not full suite
```

### Phase 4: Build Graph Optimization

```
1. CRITICAL PATH ANALYSIS
   |-- Identify the critical path from build trace (longest dependency chain)
   |-- For each target on critical path:
   |   |-- Can it be parallelized? (split into smaller targets)
   |   |-- Can it be cached? (deterministic inputs, pre-built artifacts)
   |   |-- Can it be deferred? (move to optional/lazy evaluation)
   |-- Goal: reduce critical path to < 20% of total build time

2. PARALLELISM TUNING
   |-- CPU parallelism: --local_ram_resources, --local_cpu_resources (Bazel)
   |-- Job server: Make's -j flag, load-average limiting (-l)
   |-- Rule of thumb: set parallel jobs to (RAM / peak_per_action_RAM), not (CPU cores)
   |   |-- Example: 64GB RAM, 2GB per compile action = 32 parallel jobs, even with 16 cores
   |-- I/O parallelism: action_local_resources to prevent disk thrashing

3. TEST SHARDING
   |-- Divide large test targets into shards: --test_sharding_strategy=external
   |-- Optimal shard count: total_test_time / target_test_time = number of shards
   |-- Avoid over-sharding: setup/teardown overhead exceeds benefit below ~10 sec/shard
   |-- Flaky test isolation: move flaky tests to separate target, do not block critical path
```

## Decision Trees

### Build System Selection

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

### Migration Readiness Assessment

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

### Remote Execution Readiness

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

### Build System Anti-Patterns

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

### Build vs Buy: Custom Rules vs External Tools

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

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | BUILD files contain `srcs = glob(["**/*.java"])` (overly broad globs) | [ALERT] Overly broad globs cause unnecessary rebuilds when ANY file in directory changes. Prefer explicit file lists or narrow globs. |
| P2 | Build target has >100 direct dependencies (`deps` list) | [WARN] Large deps lists increase critical path and reduce incrementality. Consider splitting into smaller, focused targets. |
| P3 | `WORKSPACE` file exists but no `MODULE.bazel` (pre-Bazel 7, no Bzlmod) | [INFO] Bzlmod (MODULE.bazel) replaces WORKSPACE in Bazel 7+. Plan migration for better dependency management and reproducible builds. |
| P4 | Cache hit rate < 50% in CI | [ALERT] Low cache hit rate wastes CI minutes and money. Audit: are inputs deterministic? Are cache keys stable? Is cache storage working? |
| P5 | Test target takes >60 seconds with no sharding | [WARN] Consider sharding this test target. A 5-minute test suite with 4 shards can run in 75 seconds on remote execution. |
| P6 | Build contains `genrule` with `cmd = "curl ..."` (network access in build) | [ALERT] genrule with network access breaks hermeticity. Replace with http_file/http_archive or pre-downloaded dependencies. |

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

## Gotchas

* **Bazel's learning curve costs real money.** Engineers take 2-4 weeks to become productive with BUILD files and Starlark. At $150/hr, that is $12,000-$24,000 per engineer in ramp-up cost. Budget for training and expect a 20-30% productivity dip during the first month. **Total cost: $12K-$24K per engineer onboarding.**

* **Buildifier doesn't fix semantics — only formatting.** Running `buildifier` on your BUILD files makes them look correct. It does not check that `deps` are complete, that visibility is correct, or that globs are appropriately scoped. Teams that rely on buildifier alone ship broken builds that "look right." **Total cost: $15K-$50K in debugging non-obvious build failures over 6 months.**

* **Remote execution amplifies flakiness, not fixes it.** A test that passes 98% of the time locally will fail 2% × 200 workers = 4 failures per full build on remote execution. Each failure investigation costs $150-$500 in engineer time. The cumulative effect of 1% flakiness across 500 targets is devastating. **Total cost: $30K-$100K/year in flake investigation for a 200-engineer org.**

* **WORKSPACE dependency hell is real.** A single `git_repository` pointing to `master` in WORKSPACE makes your build non-reproducible. Six months later, nobody knows which version of the dependency was used. The fix (Bzlmod/MODULE.bazel) requires restructuring your entire dependency graph. **Total cost: $20K-$80K in dependency migration and debugging for a mid-size repo.**

* **Over-specified `deps` cause phantom rebuilds.** Adding a dependency on `//foo:bar` when you only need `//foo:bar:types` means changing `bar`'s implementation rebuilds your target. Over time, this cascades: 5 extra deps per target × 200 targets × 2 min rebuild × 20 changes/day = 6.7 engineer-hours of unnecessary waiting per day. **Total cost: $200K-$500K/year in wasted build time for a 100-engineer org with poorly maintained deps.**

* **Test sharding without test isolation creates Heisen-failures.** Tests that share state (database, temp files, environment variables) will pass serially and fail under sharding — the worst kind of flakiness because it is non-deterministic. Finding and fixing shared state across 5,000 tests after sharding is enabled is a multi-week effort. **Total cost: $30K-$75K in test isolation cleanup after enabling sharding on a legacy test suite.**

* **"Just use ccache" doesn't fix your build system.** ccache works at the compilation level, not the build graph level. If your Makefile has incorrect dependencies, ccache will cache incorrect outputs. ccache also doesn't help with linking, code generation, or test execution — the parts that dominate build times in large projects. **Total cost: $10K-$25K in misdiagnosed build time after investing in ccache but not fixing the underlying dependency graph.**

* **Migrating to Bazel during a hiring push causes permanent build hygiene debt.** New engineers who never learned the old system will cargo-cult BUILD files (copy-paste deps, overly broad globs, no visibility rules). Within 6 months, the build graph is worse than before the migration. **Total cost: $50K-$150K in build graph cleanup and re-education if migration isn't paired with mandatory build hygiene training.**

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

## References

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
