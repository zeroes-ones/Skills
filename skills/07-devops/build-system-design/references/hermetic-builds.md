# Hermetic Build Design

## Definition

A hermetic build produces identical outputs given identical inputs, regardless of the environment. No network access, no system tool dependencies, no environment variable leaks, no timestamps in outputs.

## Why Hermeticity Matters

1. **Caching correctness:** Non-deterministic outputs break content-addressable caching. Two builds of the "same" code produce different hashes → cache misses → no speed benefit.
2. **Remote execution:** Build workers have different environments. A build that depends on `/usr/bin/gcc` fails on a worker without GCC installed.
3. **Reproducibility:** Debugging a production issue from 6 months ago. Can you rebuild the exact binary from that commit? Without hermeticity: probably not.
4. **Supply chain security:** Network access during build means a compromised dependency can inject code at build time.

## Hermeticity Checklist

### Eliminate Network Access
- Declare all external dependencies explicitly (WORKSPACE, MODULE.bazel, third_party/)
- Mirror dependencies internally (Artifactory, Nexus)
- Pin with content hashes: `sha256 = "abc123..."`
- Never use `git_repository` with floating branch (`branch = "main"`)
- Verify: `bazel build --sandbox_block_network //...`

### Eliminate System Dependencies
- Use hermetic toolchains: `register_toolchains()` not `/usr/bin/gcc`
- Container-based builds: Docker with pinned toolchain image
- Nix: `nix-shell` with pinned nixpkgs commit
- Verify: `bazel build --incompatible_strict_action_env //...`

### Eliminate Environment Leaks
- `--action_env` to explicitly pass only required env vars
- Never depend on `$HOME`, `$USER`, `$HOSTNAME`
- Set `SOURCE_DATE_EPOCH` for deterministic timestamps
- Verify: build on macOS and Linux CI — outputs must match

### Verify Determinism
```bash
# Build twice, compare
bazel build //...
cp bazel-bin/ build1/
bazel clean && bazel build //...
diff -r build1/ bazel-bin/  # Must produce no differences
```
