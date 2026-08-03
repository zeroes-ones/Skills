#!/usr/bin/env bash
# Verify network-builder skill integrity
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_FILE="$SKILL_DIR/SKILL.md"

echo "=== Verifying network-builder ==="

# Basic file checks
[ -f "$SKILL_FILE" ] || { echo "FAIL: SKILL.md not found"; exit 1; }
[ -d "$SKILL_DIR/references" ] || { echo "FAIL: references/ directory not found"; exit 1; }

# Template compliance checks
echo "Checking required sections..."
for section in "RESEARCH_PREREQUISITE" "Anti-Hallucination" "Route the Request" \
    "Ground Rules" "The Expert's Mindset" "Operating at Different Levels" \
    "When to Use" "When NOT to Use" "Decision Trees" "Core Workflow" \
    "Error Decoder" "Cross-Skill Coordination" "Proactive Triggers" \
    "What Good Looks Like" "Deliberate Practice" "References" "Gotchas" \
    "Anti-Patterns" "Verification" "Error Recovery" "State Log" \
    "Production Checklist" "Anti-Rationalization" "Complete When"; do
    if ! grep -q "^## $section" "$SKILL_FILE"; then
        echo "  MISSING: $section"
    fi
done

# Anti-hallucination guardrails
for phrase in "Admit uncertainty" "Flag your knowledge cutoff" "Never guess" "[VERIFIED]"; do
    if ! grep -qF "$phrase" "$SKILL_FILE"; then
        echo "  MISSING GUARDRAIL: $phrase"
    fi
done

# Dollar-quantified gotchas
dollar_count=$(grep -c '\$' "$SKILL_FILE" || true)
if [ "$dollar_count" -lt 5 ]; then
    echo "  WARNING: Only $dollar_count dollar-quantified references (need ≥5)"
fi

# Decision trees
dt_count=$(sed -n '/^## Decision Trees/,/^## /p' "$SKILL_FILE" | grep -c '^###' || true)
if [ "$dt_count" -lt 3 ]; then
    echo "  WARNING: Only $dt_count decision trees (need ≥3)"
fi

# Complete when
cw_count=$(grep -ci 'Complete when' "$SKILL_FILE" || true)
if [ "$cw_count" -lt 8 ]; then
    echo "  WARNING: Only $cw_count 'Complete when' criteria (need ≥8)"
fi

echo "=== network-builder verification complete ==="
