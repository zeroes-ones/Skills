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

echo "--- Frontmatter ---"
if grep -q "author: Sandeep Kumar Penchala" "$SKILL_MD"; then
  echo "  [PASS] Author: Sandeep Kumar Penchala"
else
  echo "  [FAIL] Author field missing or incorrect"
  FAILURES=$((FAILURES + 1))
fi

if grep -q "license: MIT" "$SKILL_MD"; then
  echo "  [PASS] License: MIT"
else
  echo "  [FAIL] License field missing or incorrect"
  FAILURES=$((FAILURES + 1))
fi

echo "--- Em-Dash in Ground Rules Heading ---"
if grep -q '^## Ground Rules.*—.*Read Before Anything Else' "$SKILL_MD"; then
  echo "  [PASS] Em-dash present in Ground Rules heading"
else
  echo "  [FAIL] Em-dash missing in Ground Rules heading"
  FAILURES=$((FAILURES + 1))
fi

echo "--- Portability Target ---"
if grep -q '> \*\*Portability target:\*\*' "$SKILL_MD"; then
  echo "  [PASS] Portability target line present"
else
  echo "  [FAIL] Portability target line missing"
  FAILURES=$((FAILURES + 1))
fi

echo "--- Core Workflow Exact Heading ---"
if grep -q '^## Core Workflow$' "$SKILL_MD"; then
  echo "  [PASS] Core Workflow heading present"
else
  echo "  [FAIL] Core Workflow heading missing or malformed"
  FAILURES=$((FAILURES + 1))
fi

echo "--- Description Keywords ---"
DESC=$(sed -n '/^description:/,/^license:/p' "$SKILL_MD" | sed '$d')
if echo "$DESC" | grep -q "Use when" && echo "$DESC" | grep -q "Handles" && echo "$DESC" | grep -q "Do NOT use"; then
  echo "  [PASS] Description contains Use when, Handles, Do NOT use"
else
  echo "  [FAIL] Description missing required keywords"
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
