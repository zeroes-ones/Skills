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
for s in "Anti-Hallucination" "Ground Rules" "The Expert's Mindset" "Operating at Different Levels" "When to Use" "Route the Request" "Core Workflow" "Decision Trees" "Cross-Skill Coordination" "Proactive Triggers" "What Good Looks Like" "Deliberate Practice" "Gotchas" "Error Recovery" "State Log" "Verification" "References"; do
  check_section "$s"
done

echo "--- Decision Trees ---"
DT_COUNT=$(sed -n '/^## Decision Trees/,/^## /p' "$SKILL_MD" | grep -c '^### Decision Tree')
if [ "$DT_COUNT" -ge 3 ]; then
  echo "  [PASS] Decision trees: $DT_COUNT (minimum 3)"
else
  echo "  [FAIL] Decision trees: $DT_COUNT (need at least 3)"
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

echo "--- Completion Criteria ---"
CC_COUNT=$(grep -ci "Complete when" "$SKILL_MD" || echo 0)
if [ "$CC_COUNT" -ge 8 ]; then
  echo "  [PASS] Completion criteria: $CC_COUNT (minimum 8)"
else
  echo "  [FAIL] Completion criteria: $CC_COUNT (need at least 8)"
  FAILURES=$((FAILURES + 1))
fi

echo "--- Anti-Hallucination ---"
if grep -q "Admit uncertainty" "$SKILL_MD" && grep -q "Flag your knowledge cutoff" "$SKILL_MD" && grep -q "Never guess security" "$SKILL_MD"; then
  echo "  [PASS] Anti-hallucination guardrails present"
else
  echo "  [FAIL] Missing anti-hallucination guardrails"
  FAILURES=$((FAILURES + 1))
fi

echo ""
if [ "$FAILURES" -eq 0 ]; then
  echo "✅ $SKILL_NAME: ALL CHECKS PASSED"
  exit 0
else
  echo "❌ $SKILL_NAME: $FAILURES check(s) FAILED"
  exit 1
fi
