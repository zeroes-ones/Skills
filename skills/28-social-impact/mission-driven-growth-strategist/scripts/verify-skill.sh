#!/usr/bin/env bash
# verify-skill.sh — Verification script for mission-driven-growth-strategist skill
# Runs before delivering any work product from this skill.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_FILE="$SKILL_DIR/SKILL.md"
ERRORS=0

echo "=== Mission-Driven Growth Strategist — Skill Verification ==="

# 1. Verify SKILL.md exists
if [[ ! -f "$SKILL_FILE" ]]; then
    echo "FAIL: SKILL.md not found at $SKILL_FILE"
    exit 1
fi
echo "PASS: SKILL.md exists"

# 2. Verify all 23 required sections
for section in "Route the Request" "Ground Rules" "Anti-Rationalization" "The Expert's Mindset" "Operating at Different Levels" "When to Use" "When NOT to Use" "Decision Trees" "Core Workflow" "Anti-Hallucination" "Error Decoder" "Error Recovery" "Cross-Skill Coordination" "Proactive Triggers" "Deliberate Practice" "State Log" "What Good Looks Like" "Gotchas" "Best Practices" "Anti-Patterns" "Production Checklist" "Verification" "References"; do
    if grep -q "^## $section" "$SKILL_FILE"; then
        echo "PASS: Section '$section' found"
    else
        # Fuzzy match for sections with annotations
        if grep -q "^## $section " "$SKILL_FILE"; then
            echo "PASS: Section '$section' found (with annotation)"
        else
            echo "FAIL: Missing section '$section'"
            ERRORS=$((ERRORS + 1))
        fi
    fi
done

# 3. Verify anti-hallucination phrases
for phrase in "Admit uncertainty" "Flag your knowledge cutoff" "Never guess security" "[VERIFIED]"; do
    if grep -q "$phrase" "$SKILL_FILE"; then
        echo "PASS: Anti-hallucination phrase '$phrase' found"
    else
        echo "FAIL: Missing anti-hallucination phrase '$phrase'"
        ERRORS=$((ERRORS + 1))
    fi
done

# 4. Verify 8 reference files exist
for ref in theory-of-change-guide.md legal-structures.md impact-frameworks.md funding-models.md governance-patterns.md metrics-catalog.md gotchas.md checklist.md; do
    if [[ -f "$SKILL_DIR/references/$ref" ]]; then
        echo "PASS: Reference '$ref' exists"
    else
        echo "FAIL: Missing reference '$ref'"
        ERRORS=$((ERRORS + 1))
    fi
done

# 5. Verify chain connectivity
if grep -q "consumes_from:" "$SKILL_FILE"; then
    echo "PASS: Chain consumes_from present"
else
    echo "FAIL: Missing chain consumes_from"
    ERRORS=$((ERRORS + 1))
fi

if grep -q "feeds_into:" "$SKILL_FILE"; then
    echo "PASS: Chain feeds_into present"
else
    echo "FAIL: Missing chain feeds_into"
    ERRORS=$((ERRORS + 1))
fi

# 6. Verify description format
FLAT_DESC=$(sed -n '/^description:/,/^[a-z]/p' "$SKILL_FILE" | tr '\n' ' ')
if echo "$FLAT_DESC" | grep -q "Use when" && \
   echo "$FLAT_DESC" | grep -q "Handles" && \
   echo "$FLAT_DESC" | grep -qE "Do\s+NOT\s+use"; then
    echo "PASS: Description follows 'Use when / Handles / Do NOT use' format"
else
    echo "FAIL: Description missing required trigger phrases"
    ERRORS=$((ERRORS + 1))
fi

# 7. Verify gotchas are dollar-quantified (5+)
DOLLAR_COUNT=$(grep -c '\$[0-9]' "$SKILL_FILE" || true)
if [[ "$DOLLAR_COUNT" -ge 5 ]]; then
    echo "PASS: $DOLLAR_COUNT dollar-quantified references (minimum 5)"
else
    echo "FAIL: Only $DOLLAR_COUNT dollar-quantified references (minimum 5)"
    ERRORS=$((ERRORS + 1))
fi

# 8. Verify decision trees (3+)
TREE_COUNT=$(sed -n '/^## Decision Trees/,/^## /p' "$SKILL_FILE" | grep -c '^### ' || true)
if [[ "$TREE_COUNT" -ge 3 ]]; then
    echo "PASS: $TREE_COUNT decision trees (minimum 3)"
else
    echo "FAIL: Only $TREE_COUNT decision trees (minimum 3)"
    ERRORS=$((ERRORS + 1))
fi

# 9. Verify "Complete when" statements (8+)
COMPLETE_COUNT=$(grep -c "Complete when" "$SKILL_FILE" || true)
if [[ "$COMPLETE_COUNT" -ge 8 ]]; then
    echo "PASS: $COMPLETE_COUNT 'Complete when' statements (minimum 8)"
else
    echo "FAIL: Only $COMPLETE_COUNT 'Complete when' statements (minimum 8)"
    ERRORS=$((ERRORS + 1))
fi

echo ""
if [[ "$ERRORS" -eq 0 ]]; then
    echo "=== ALL CHECKS PASSED ==="
    exit 0
else
    echo "=== $ERRORS CHECK(S) FAILED ==="
    exit 1
fi
