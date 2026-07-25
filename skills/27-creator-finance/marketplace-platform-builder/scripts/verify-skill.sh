#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
SKILL_NAME="$(basename "$SKILL_DIR")"
FAILURES=0

check_section() {
  local pattern="$1"
  local label="$2"
  if grep -q "$pattern" "$SKILL_MD"; then
    echo "  [PASS] Section: $label"
  else
    echo "  [FAIL] Section: $label — MISSING"
    FAILURES=$((FAILURES + 1))
  fi
}

echo "=== Verifying $SKILL_NAME ==="

[ ! -f "$SKILL_MD" ] && echo "[FAIL] SKILL.md not found" && exit 1

echo "--- Required Sections ---"
# Use grep patterns that match the actual section headings (with suffixes like **(STANDARD)**)
check_section "^## Ground Rules" "Ground Rules"
check_section "^## The Expert.s Mindset" "The Expert's Mindset"
check_section "^## Operating at Different Levels" "Operating at Different Levels"
check_section "^## When to Use" "When to Use"
check_section "^## Route the Request" "Route the Request"
check_section "^## Core Workflow" "Core Workflow"
check_section "^## Decision Trees" "Decision Trees"
check_section "^## Cross-Skill Coordination" "Cross-Skill Coordination"
check_section "^## Proactive Triggers" "Proactive Triggers"
check_section "^## What Good Looks Like" "What Good Looks Like"
check_section "^## Deliberate Practice" "Deliberate Practice"

# Check for Error Decoder (actual section name) instead of the non-existent "Gotchas"
if grep -qE "^## (Error Decoder|Gotchas)" "$SKILL_MD"; then
  echo "  [PASS] Section: Error Decoder"
else
  echo "  [FAIL] Section: Error Decoder — MISSING"
  FAILURES=$((FAILURES + 1))
fi

# Accept both "Verification" and "Verification Guardrails"
check_section "^## Verification" "Verification"
check_section "^## References" "References"
check_section "^## State Log" "State Log"
check_section "^## Error Recovery" "Error Recovery"

echo "--- Decision Trees ---"
DT_COUNT=$(sed -n '/^## Decision Trees/,/^## Error Decoder/p' "$SKILL_MD" | grep -c '^###')
if [ "$DT_COUNT" -ge 2 ]; then
  echo "  [PASS] Decision trees: $DT_COUNT (minimum 2)"
else
  echo "  [FAIL] Decision trees: $DT_COUNT (need at least 2)"
  FAILURES=$((FAILURES + 1))
fi

echo "--- Ground Rules ---"
if grep -q "Mechanical Trigger" "$SKILL_MD" && grep -q "Violation Response" "$SKILL_MD"; then
  echo "  [PASS] Ground rules have Mechanical Trigger and Violation Response columns"
else
  echo "  [FAIL] Ground rules missing required columns"
  FAILURES=$((FAILURES + 1))
fi

echo "--- Reference Directory ---"
REF_DIR="$SKILL_DIR/references"
if [ -d "$REF_DIR" ]; then
  echo "  [PASS] references/ directory exists"
else
  echo "  [FAIL] references/ directory missing"
  FAILURES=$((FAILURES + 1))
fi

echo ""
if [ "$FAILURES" -eq 0 ]; then
  echo "\u2705 $SKILL_NAME: ALL CHECKS PASSED"
  exit 0
else
  echo "\u274c $SKILL_NAME: $FAILURES check(s) FAILED"
  exit 1
fi
