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
