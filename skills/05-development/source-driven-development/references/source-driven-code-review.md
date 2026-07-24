# Source-Driven Code Review

## Review Objective

Verify that every framework/library touchpoint in a change is traceable to official documentation at the correct version.

## Pre-Review: Reviewer Setup

1. Check out the PR branch
2. Run `npm ls --depth=0` or equivalent to capture exact versions
3. Open the official docs at those versions in browser tabs

## Review Checklist

### Phase 1: Import Audit

- [ ] Every third-party `import`/`require`/`use` has a `[Source: ...]` citation
- [ ] The version in every citation matches the installed version (from lockfile)
- [ ] No imports of deprecated packages (cross-reference with npm deprecation warnings)
- [ ] No imports of packages that don't appear in `dependencies`/`devDependencies`

### Phase 2: API Signature Verification

- [ ] Every method call's parameter order matches the documented signature
- [ ] Keyword/named arguments are used where the docs recommend them
- [ ] Optional parameters are handled (not assumed to have defaults)
- [ ] Return types are used correctly per docs (null checks, error handling patterns)

### Phase 3: Configuration Audit

- [ ] Every config option maps to a documented property in the config schema
- [ ] No undocumented/"magic" options (values that "someone said" work)
- [ ] Default values are explicitly noted if their behavior matters
- [ ] Environment-specific config is documented with source for valid values

### Phase 4: Behavioral Claims

- [ ] Every behavioral assumption ("runs on mount," "invalidates cache," "is atomic") has a doc citation
- [ ] Async/sync execution assumptions are verified against docs
- [ ] Error handling patterns match the documented error types and shapes

### Phase 5: Version Consistency

- [ ] No version mismatch between cited docs and lockfile
- [ ] No mixed version assumptions (e.g., using v4 API with v3 config pattern)
- [ ] Migration guides consulted for any files that touch recently-upgraded packages

## Review Comments Template

### For missing citations:
```
🔴 BLOCKING: Missing source citation for `{imported_package}`.
Add: // [Source: {Framework} Docs, Section: {section}, URL: {url}, Version: {v}]
```

### For unverified claims:
```
🟡 WARNING: Claim "{claim}" is unverified. No official source linked.
Please add citation or flag with ⚠️ UNVERIFIED and risk level.
```

### For version mismatches:
```
🔴 BLOCKING: Citation says Version: v{old} but lockfile has v{new}.
Update citation to current version and verify API compatibility.
```

### For deprecated usage:
```
🔴 BLOCKING: `{method}` is deprecated in v{current}. Migration guide: {url}.
Replace with `{replacement}` per official docs.
```

## Automated Review Helpers

```bash
#!/bin/bash
# Run this in the PR branch before manual review

echo "=== UNCITED IMPORTS ==="
grep -rn "^import\|^from\|require(" src/ --include="*.{ts,js,py,go}" | \
  grep -v "Source:" | grep -v "^\.\/\|^\.\.\/"

echo "=== VERSION MISMATCHES ==="
# Extract cited versions
grep -rohP 'Version:\s*\K[^\]]+' src/ | sort -u > /tmp/cited.txt
# Extract installed versions
npm ls --depth=0 --json 2>/dev/null | jq -r '.dependencies | to_entries[] | "\(.key)@\(.value.version)"' > /tmp/installed.txt || true
diff <(sort /tmp/cited.txt) <(sort /tmp/installed.txt) || echo "Version drift detected"

echo "=== STACK OVERFLOW REFERENCES ==="
grep -rn "stackoverflow\|stackoverflow.com" src/ --include="*.{ts,js,py,go}"
```
