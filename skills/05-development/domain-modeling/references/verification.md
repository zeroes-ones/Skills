## Verification

Run these checks to confirm the domain model is healthy.

```bash
# Check CONTEXT.md freshness (should be < 30 days old)
find . -name "CONTEXT.md" -mtime +30 -exec echo "STALE: {}" \;

# Find domain terms used in class names but missing from CONTEXT.md
grep -rn "class [A-Z]" --include="*.ts" --include="*.java" --include="*.py" --include="*.go" . | \
  grep -v node_modules | grep -v vendor | \
  while read line; do echo "$line"; done

# Detect terms used in multiple modules with potentially different meanings
grep -rn "\bAccount\b\|\bOrder\b\|\bUser\b\|\bCustomer\b" --include="*.ts" . | \
  awk -F: '{print $3}' | sort | uniq -c | sort -rn | head -20

# Find domain rules in comments that aren't in CONTEXT.md
grep -rn "MUST\|MUST NOT\|SHALL\|SHALL NOT\|business rule\|domain rule\|invariant" \
  --include="*.ts" --include="*.java" --include="*.go" . | \
  grep -v node_modules | grep -v vendor

# Verify all ADRs pass the three-part test
for adr in adr/*.md doc/adr/*.md; do
  echo "=== $adr ==="
  grep -c "hard.to.reverse\|surprising\|tradeoff\|alternative" "$adr" 2>/dev/null || echo "  WARNING: no tradeoff signals found"
done

# Check for undocumented bounded contexts
grep -rn "bounded.context\|context.map\|ACL\|anti.corruption" --include="*.md" . | \
  grep -v node_modules

# Cross-reference: find CONTEXT.md rules without code enforcement
# (requires manual review of output)
grep "Rule ID" CONTEXT.md | while read rule; do
  rule_id=$(echo "$rule" | awk '{print $NF}')
  echo "Rule: $rule_id — verify code enforcement exists"
done
```
