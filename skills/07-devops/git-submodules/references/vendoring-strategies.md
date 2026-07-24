# Vendoring Strategies

## Decision Framework

Vendor when ALL of these conditions are true:
1. Dependency is small (< 5K LOC)
2. Dependency is stable (< 1 release per quarter)
3. You need local modifications that cannot be upstreamed
4. You have automated monitoring for upstream releases
5. You accept maintenance responsibility for this code

## Vendoring Patterns

### Go-Style (vendor/ directory)

```
vendor/
  github.com/
    org/
      lib/
        VENDOR_VERSION  # Contains: v1.2.3, fetched 2026-01-15
        lib.go
```

Managed by `go mod vendor`. Pins exact versions. CI check: `go mod verify`.

### Third-Party Style

```
third_party/
  lib-name/
    README.md          # Upstream: https://github.com/..., Version: v1.2.3
    update.sh          # Script to fetch latest and diff
    lib-name/
      (vendored source)
```

### CI Monitoring

```bash
# Check if vendored code is stale
UPSTREAM_VERSION=$(curl -s https://api.github.com/repos/org/lib/releases/latest | jq -r .tag_name)
VENDORED_VERSION=$(cat vendor/lib/VENDOR_VERSION)
if [ "$UPSTREAM_VERSION" != "$VENDORED_VERSION" ]; then
  echo "WARNING: vendored lib is behind upstream ($VENDORED_VERSION vs $UPSTREAM_VERSION)"
fi
```

## When to Un-Vendor

- More than 4 releases per year → migrate to package registry
- Multiple repos need the same vendored code → extract to shared submodule/package
- Security vulnerability disclosed → patch immediately or un-vendor
