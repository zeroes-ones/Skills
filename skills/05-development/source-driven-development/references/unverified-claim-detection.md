# Unverified Claim Detection

## Pattern Catalog

Claims in code, PR descriptions, and comments that lack official source backing.

### Pattern 1: Anecdotal Assertions

```
Indicators: "I think...", "I believe...", "pretty sure...", "IIRC...", "AFAIK..."
Detection: grep -rn "\bI think\b\|\bIIRC\b\|\bAFAIK\b\|\bpretty sure\b" src/
```

### Pattern 2: Community Consensus

```
Indicators: "everyone uses...", "standard practice is...", "the community prefers...", "best practice is..."
Detection: grep -rn "\beveryone uses\b\|\bstandard practice\b\|\bbest practice\b" src/
Flag: No source. "Best practice" without citation is opinion.
```

### Pattern 3: Version Assumptions

```
Indicators: "this works since v3...", "compatible with...", "should work with..."
Detection: grep -rn "\bsince v\|compatible with\b\|\bshould work\b" src/
Required: Link to release notes or compat table confirming the version claim.
```

### Pattern 4: Behavioral Assumptions

```
Indicators: "this runs synchronously", "middleware fires before...", "the cache invalidates on..."
Detection: grep -rn "\bruns\|fires\|invalidates\|triggers\|calls back\b" src/ | grep -v "Source:"
Required: Link to docs section describing the exact behavior under specified conditions.
```

### Pattern 5: Deprecation Denial

```
Indicators: "@deprecated" in IDE but no migration, "// eslint-disable-next-line" near framework call
Detection: grep -rn "@deprecated\|eslint-disable-next-line" src/ | grep -v "Source:"
Required: Link to deprecation notice in changelog AND migration path to replacement API.
```

### Pattern 6: Config by Convention

```
Indicators: Config values without comments, magic numbers in framework options
Detection: grep -rn "{ [a-z].*: [0-9]" src/ | grep -v "Source:" | grep -v "//"
Required: Every config value traced to a doc section describing that option's valid range and default.
```

## Risk Classification

| Risk Level | Condition | Example |
|---|---|---|
| LOW | Claim is about optional/UI behavior with fallback | "This color should be accessible" |
| MEDIUM | Claim affects data display or non-critical logic | "This query should be cached for 5 minutes" |
| HIGH | Claim affects data integrity, auth, or payments | "This transaction is atomic" |
| CRITICAL | Claim about security, privacy, or financial logic | "This endpoint is rate-limited by the framework" |

## Mechanical Verification Script

```bash
#!/bin/bash
# Find all framework imports and check for corresponding citations
IMPORTS=$(grep -rn "^import\|^from" src/ --include="*.{ts,js,py,go}" | grep -v "Source:" | grep -v "^import.*from '\.\|^from \.")
if [ -n "$IMPORTS" ]; then
  echo "⚠️ UNCITED IMPORTS FOUND:"
  echo "$IMPORTS"
  echo "Each must have a [Source: ...] citation."
fi
```
