#!/usr/bin/env bash
# verify-skill.sh — Verification script for nonprofit-fundraising-engineer
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_FILE="$SKILL_DIR/SKILL.md"
ERRORS=0

echo "=== Nonprofit Fundraising Engineer — Skill Verification ==="

[[ -f "$SKILL_FILE" ]] && echo "PASS: SKILL.md exists" || { echo "FAIL: SKILL.md not found"; exit 1; }

# Required sections
for section in "Route the Request" "Ground Rules" "Anti-Rationalization" "The Expert's Mindset" "Operating at Different Levels" "When to Use" "When NOT to Use" "Decision Trees" "Core Workflow" "Anti-Hallucination" "Error Decoder" "Error Recovery" "Cross-Skill Coordination" "Proactive Triggers" "Deliberate Practice" "State Log" "What Good Looks Like" "Gotchas" "Best Practices" "Anti-Patterns" "Production Checklist" "Verification" "References"; do
    if grep -q "^## $section" "$SKILL_FILE" || grep -q "^## $section " "$SKILL_FILE"; then
        echo "PASS: Section '$section' found"
    else
        echo "FAIL: Missing section '$section'"
        ERRORS=$((ERRORS + 1))
    fi
done

# Anti-hallucination phrases
for phrase in "Admit uncertainty" "Flag your knowledge cutoff" "Never guess security" "\[VERIFIED\]"; do
    grep -q "$phrase" "$SKILL_FILE" && echo "PASS: AH phrase '$phrase' found" || { echo "FAIL: Missing AH phrase '$phrase'"; ERRORS=$((ERRORS + 1)); }
done

# Reference files
for ref in donation-form-patterns.md recurring-giving-architecture.md crm-integration-playbook.md payment-gateway-nonprofit.md tax-receipt-compliance.md p2p-fraud-prevention.md matching-gift-integration.md donor-analytics.md; do
    [[ -f "$SKILL_DIR/references/$ref" ]] && echo "PASS: Reference '$ref' exists" || { echo "FAIL: Missing reference '$ref'"; ERRORS=$((ERRORS + 1)); }
done

# Chain connectivity
grep -q "consumes_from:" "$SKILL_FILE" && echo "PASS: Chain consumes_from present" || { echo "FAIL: Missing consumes_from"; ERRORS=$((ERRORS + 1)); }
grep -q "feeds_into:" "$SKILL_FILE" && echo "PASS: Chain feeds_into present" || { echo "FAIL: Missing feeds_into"; ERRORS=$((ERRORS + 1)); }

# Description format
FLAT_DESC=$(sed -n '/^description:/,/^[a-z]/p' "$SKILL_FILE" | tr '\n' ' ')
if echo "$FLAT_DESC" | grep -q "Use when" && echo "$FLAT_DESC" | grep -q "Handles" && echo "$FLAT_DESC" | grep -qE "Do\s+NOT\s+use"; then
    echo "PASS: Description 'Use when / Handles / Do NOT use' format"
else
    echo "FAIL: Description format incorrect"
    ERRORS=$((ERRORS + 1))
fi

# Dollar-quantified gotchas
DOLLAR_COUNT=$(grep -c '\$[0-9]' "$SKILL_FILE" || true)
[[ "$DOLLAR_COUNT" -ge 5 ]] && echo "PASS: $DOLLAR_COUNT dollar-quantified references" || { echo "FAIL: Only $DOLLAR_COUNT dollar refs (need 5+)"; ERRORS=$((ERRORS + 1)); }

# Decision trees
TREE_COUNT=$(sed -n '/^## Decision Trees/,/^## /p' "$SKILL_FILE" | grep -c '^### ' || true)
[[ "$TREE_COUNT" -ge 3 ]] && echo "PASS: $TREE_COUNT decision trees" || { echo "FAIL: Only $TREE_COUNT trees (need 3+)"; ERRORS=$((ERRORS + 1)); }

# Complete when
COMPLETE_COUNT=$(grep -ci "Complete when" "$SKILL_FILE" || true)
[[ "$COMPLETE_COUNT" -ge 8 ]] && echo "PASS: $COMPLETE_COUNT 'Complete when' statements" || { echo "FAIL: $COMPLETE_COUNT (need 8+)"; ERRORS=$((ERRORS + 1)); }

echo ""
[[ "$ERRORS" -eq 0 ]] && echo "=== ALL CHECKS PASSED ===" && exit 0 || { echo "=== $ERRORS CHECK(S) FAILED ==="; exit 1; }
