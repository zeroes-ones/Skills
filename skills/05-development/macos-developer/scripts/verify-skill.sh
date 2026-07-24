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
for s in "Ground Rules" "The Expert's Mindset" "Operating at Different Levels" \
        "When to Use" "Route the Request" "Core Workflow" "Decision Trees" \
        "Cross-Skill Coordination" "Proactive Triggers" "What Good Looks Like" \
        "Deliberate Practice" "Gotchas" "Anti-Rationalization" "Verification" "References"; do
  check_section "$s"
done

echo "--- Decision Trees ---"
DT_COUNT=$(sed -n '/^## Decision Trees/,/^## Cross-Skill/p' "$SKILL_MD" | grep -c '^###')
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

echo "--- Anti-Rationalization Table ---"
AR_COUNT=$(sed -n '/^## Anti-Rationalization/,/^## Verification/p' "$SKILL_MD" | grep -c '^|.*|.*|$')
if [ "$AR_COUNT" -ge 5 ]; then
  echo "  [PASS] Anti-rationalization rows: $AR_COUNT (minimum 5)"
else
  echo "  [FAIL] Anti-rationalization rows: $AR_COUNT (need at least 5)"
  FAILURES=$((FAILURES + 1))
fi

echo "--- Reference Links ---"
BROKEN=0
REF_DIR="$SKILL_DIR/references"
if [ -d "$REF_DIR" ]; then
  for ref in $(grep -ohP '(?<=references/)[^)]*\.md' "$SKILL_MD" 2>/dev/null || true); do
    if [ ! -f "$REF_DIR/$ref" ]; then
      echo "  [FAIL] Broken reference: references/$ref"
      BROKEN=$((BROKEN + 1))
    fi
  done
fi
[ "$BROKEN" -eq 0 ] && echo "  [PASS] All reference links resolve" || FAILURES=$((FAILURES + BROKEN))

echo "--- Frontmatter ---"
if grep -q "^name: macos-developer" "$SKILL_MD" && \
   grep -q "^token_budget:" "$SKILL_MD" && \
   grep -q "^chain:" "$SKILL_MD" && \
   grep -q "consumes_from:" "$SKILL_MD" && \
   grep -q "feeds_into:" "$SKILL_MD" && \
   grep -q "Portability target:" "$SKILL_MD"; then
  echo "  [PASS] Frontmatter contains name, token_budget, chain, and portability target"
else
  echo "  [FAIL] Frontmatter incomplete — missing required YAML fields or portability line"
  FAILURES=$((FAILURES + 1))
fi

echo "--- Reference File Quality ---"
LOW_LINE_COUNT=0
for ref in "$REF_DIR"/*.md; do
  REF_LINES=$(wc -l < "$ref")
  REF_NAME=$(basename "$ref")
  if [ "$REF_LINES" -lt 200 ]; then
    echo "  [WARN] $REF_NAME: $REF_LINES lines (target: 200+)"
    LOW_LINE_COUNT=$((LOW_LINE_COUNT + 1))
  fi
done
[ "$LOW_LINE_COUNT" -eq 0 ] && echo "  [PASS] All reference files meet 200-line minimum"

echo ""
if [ "$FAILURES" -eq 0 ]; then
  echo "✅ $SKILL_NAME: ALL CHECKS PASSED"
  exit 0
else
  echo "❌ $SKILL_NAME: $FAILURES check(s) FAILED"
  exit 1
fi
