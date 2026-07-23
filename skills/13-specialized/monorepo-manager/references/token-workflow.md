# Token-Efficient Workflow

```
# Step 1: Monorepo health check
python3 scripts/monorepo_health.py --root . --output json
# Returns: {"packages": 12, "circular_deps": 0, "orphans": 1,
#           "avg_dep_depth": 2.1, "packages_no_tests": 3, "build_time_cold": 180}

# Step 2: Decision tree
# circular_deps > 0 → FIX IMMEDIATELY. This breaks builds.
# orphans > 0 → Identify and remove or document intentionally unused packages.
# avg_dep_depth > 3 → Refactor. Deep dependency chains slow builds and increase blast radius.
# build_time_cold > 300 → Invest in remote caching.

# Step 3: Quick fix — check what's affected by current change
npx turbo run build --filter=[main...HEAD] --dry-run=json | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'Packages to build: {len(data[\"packages\"])}')
"

# Step 4: Verify cache hit rate
npx turbo run build --verbosity=1 2>&1 | grep -c "cache hit"
# Track: cache hit % should be >80% for developers after first build
```

**Principle:** `monorepo_health.py` analyzes package.json files and dependency graph, outputs JSON. Agent reads structured data, follows decision tree. Affected detection verified via Turborepo dry-run (exit code + JSON). Never reads individual package.json files into context.
