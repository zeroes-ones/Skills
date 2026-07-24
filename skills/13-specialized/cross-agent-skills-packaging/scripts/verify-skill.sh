#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
SKILL_NAME="$(basename "$SKILL_DIR")"
FAILURES=0

check_section() {
  if grep -q "^## $1" "$SKILL_MD"; then
    echo "  [PASS] Section: $1"
  else
    echo "  [FAIL] Section: $1 — MISSING"
    FAILURES=$((FAILURES + 1))
  fi
}

echo "=== Verifying $SKILL_NAME ==="

[ ! -f "$SKILL_MD" ] && echo "[FAIL] SKILL.md not found" && exit 1

echo "--- Required Sections ---"
for s in "Ground Rules" "The Expert's Mindset" "Operating at Different Levels" "When to Use" "Route the Request" "Core Workflow" "Decision Trees" "Cross-Skill Coordination" "Proactive Triggers" "What Good Looks Like" "Deliberate Practice" "Gotchas" "Verification" "References"; do
  check_section "$s"
done

echo "--- Anti-Rationalization ---"
if grep -q "^## Anti-Rationalization" "$SKILL_MD"; then
  echo "  [PASS] Section: Anti-Rationalization"
else
  echo "  [FAIL] Section: Anti-Rationalization — MISSING"
  FAILURES=$((FAILURES + 1))
fi

echo "--- Decision Trees ---"
DT_COUNT=$(sed -n '/^## Decision Trees/,/^## Cross-Skill Coordination/p' "$SKILL_MD" | grep -c '^###')
if [ "$DT_COUNT" -ge 5 ]; then
  echo "  [PASS] Decision trees: $DT_COUNT (minimum 5)"
else
  echo "  [FAIL] Decision trees: $DT_COUNT (need at least 5)"
  FAILURES=$((FAILURES + 1))
fi

echo "--- Gotchas ---"
GOTCHA_COUNT=$(grep -c '\$[0-9]' "$SKILL_MD" || echo 0)
if [ "$GOTCHA_COUNT" -ge 5 ]; then
  echo "  [PASS] Dollar-quantified gotchas: $GOTCHA_COUNT (minimum 5)"
else
  echo "  [FAIL] Dollar-quantified gotchas: $GOTCHA_COUNT (need at least 5)"
  FAILURES=$((FAILURES + 1))
fi

echo "--- Ground Rules ---"
if grep -q "Mechanical Trigger" "$SKILL_MD" && grep -q "Violation Response" "$SKILL_MD"; then
  echo "  [PASS] Ground rules have Mechanical Trigger and Violation Response columns"
else
  echo "  [FAIL] Ground rules missing required columns"
  FAILURES=$((FAILURES + 1))
fi

echo "--- Portability Target ---"
if grep -q "Portability target" "$SKILL_MD"; then
  echo "  [PASS] Portability target declared"
else
  echo "  [FAIL] Portability target NOT declared"
  FAILURES=$((FAILURES + 1))
fi

echo "--- Reference Links ---"
BROKEN=0
REF_DIR="$SKILL_DIR/references"
if [ -d "$REF_DIR" ]; then
  for ref in $(grep -oh '(references/[^)]*\.md)' "$SKILL_MD" 2>/dev/null | sed 's|(references/||;s|)||'); do
    if [ ! -f "$REF_DIR/$ref" ]; then
      echo "  [FAIL] Broken reference: references/$ref"
      BROKEN=$((BROKEN + 1))
    fi
  done
fi
[ "$BROKEN" -eq 0 ] && echo "  [PASS] All reference links resolve" || FAILURES=$((FAILURES + BROKEN))

echo "--- Reference File Count ---"
REF_COUNT=$(find "$REF_DIR" -maxdepth 1 -name "*.md" | wc -l | tr -d ' ')
if [ "$REF_COUNT" -ge 8 ]; then
  echo "  [PASS] Reference files: $REF_COUNT (minimum 8)"
else
  echo "  [FAIL] Reference files: $REF_COUNT (need at least 8)"
  FAILURES=$((FAILURES + 1))
fi

echo "--- Frontmatter Fields ---"
for field in "name:" "description:" "author:" "license:" "portability:" "type:" "status:" "version:" "updated:" "tags:" "token_budget:" "chain:"; do
  if grep -q "^${field}" "$SKILL_MD"; then
    echo "  [PASS] Frontmatter field: ${field%:}"
  else
    echo "  [WARN] Frontmatter field missing: ${field%:}"
  fi
done

echo ""
if [ "$FAILURES" -eq 0 ]; then
  echo "✅ $SKILL_NAME: ALL CHECKS PASSED"
  exit 0
else
  echo "❌ $SKILL_NAME: $FAILURES check(s) FAILED"
  exit 1
fi
