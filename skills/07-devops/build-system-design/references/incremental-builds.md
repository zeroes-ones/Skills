# Incremental Build Optimization

## The Incremental Build Contract

An incremental build should rebuild ONLY targets affected by the change. If changing `foo.cc` causes `bar_test` to rebuild, the dependency graph is wrong or overly broad.

## Dependency Granularity

```
BAD: Single 50K-line cc_library
  cc_library(name = "all", srcs = glob(["**/*.cc"]))

GOOD: Split into focused libraries
  cc_library(name = "types", srcs = ["types.cc"], hdrs = ["types.h"])
  cc_library(name = "parser", srcs = ["parser.cc"], hdrs = ["parser.h"], deps = [":types"])
  cc_library(name = "compiler", srcs = ["compiler.cc"], hdrs = ["compiler.h"], deps = [":parser"])
```

Benefit: changing `types.h` rebuilds 1 library. Changing `compiler.cc` rebuilds 1 library.
Cost: more BUILD files, slightly slower graph resolution.

## Caching Strategies

### Local Disk Cache
```bash
# Bazel
bazel build --disk_cache=/persistent/cache //...

# ccache (for Make/CMake)
export CCACHE_DIR=/persistent/ccache
ccache --max-size=50G
```

### Remote Shared Cache
```bash
# bazel-remote (NGINX-backed)
bazel build --remote_cache=http://cache.internal:9090 //...
```

Cache hit rate targets:
- Local: >90% (same machine, successive builds)
- Remote CI: >60% (different machines, clean checkout)
- Remote team: >40% (many developers, diverse changes)

## Header Hygiene (C/C++)

- Include What You Use (IWYU): only include what you directly use
- Forward declarations: replace `#include "foo.h"` with `class Foo;` where possible
- Precompiled headers: for large, stable headers (standard library, framework headers)

## Unnecessary Dependency Pruning

```bash
# Find unused dependencies
bazel query 'deps(//path/to:target)' --output=graph

# Remove deps that are not directly used
# Re-run: does the target still build and test?
```
