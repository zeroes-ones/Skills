# Build Graph Optimization

## Critical Path Analysis

The critical path is the longest sequential chain of dependencies in the build. It determines the minimum possible build time — no amount of parallelism can make a build faster than its critical path.

### Generating a Build Trace
```bash
# Bazel
bazel build //... --profile=profile.json.gz
# Open profile.json.gz in chrome://tracing

# Buck2
buck2 build //... --profile profile.json
# Use buck2 profile analyze
```

### Analyzing the Trace
1. Identify the critical path (longest dependency chain)
2. For each target on critical path:
   - Can it be split into smaller targets?
   - Can it be cached?
   - Can it be deferred?
3. Goal: critical path < 20% of total sequential build time

## Parallelism Tuning

Rule of thumb: set parallelism based on RAM, not CPU cores.

```
MAX_JOBS = min(
  CPU_CORES,
  AVAILABLE_RAM_GB / PEAK_PER_ACTION_RAM_GB
)

Example: 64GB RAM, 2GB/action, 16 cores
  CPU-bound: 16 parallel actions
  RAM-bound: 32 parallel actions
  Correct: min(16, 32) = 16 parallel actions
  If actions use 1GB: min(16, 64) = 16
  If actions use 4GB: min(16, 16) = 16
```

```bash
# Bazel
bazel build --local_ram_resources=HOST_RAM*0.75 --local_cpu_resources=HOST_CPUS

# Make
make -j$(nproc) -l$(nproc)
```

## Test Sharding

Divide large test targets into independently executable shards.

```bash
# Bazel
bazel test //large:test --test_sharding_strategy=external --test_arg=--shard_count=4

# Optimal shard count
shard_count = ceil(total_test_time / target_test_time)
```

Avoid over-sharding: shard overhead (setup/teardown) exceeds benefit below ~10 seconds per shard.

## Common Anti-Patterns

- Circular dependencies: `a -> b -> a` causes infinite loops or incorrect builds
- Overspecified deps: `deps = ["//a:b", "//c:d"]` when only `//a:b` is needed
- globs: `srcs = glob(["**/*.java"])` causes rebuilds on any file change
- Monolithic targets: one target doing compilation, codegen, test all at once
