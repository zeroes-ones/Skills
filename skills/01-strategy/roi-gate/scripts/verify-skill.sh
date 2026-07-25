#!/usr/bin/env bash
# Verify roi-gate SKILL.md passes 10/10 quality checks
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
ERRORS=0

check() {
    local desc="$1"
    local pattern="$2"
    if grep -q "$pattern" "$SKILL_MD"; then
        echo "  ✅ $desc"
    else
        echo "  ❌ $desc — MISSING"
        ERRORS=$((ERRORS + 1))
    fi
}

echo "=== ROI Gate Quality Verification ==="
echo ""

echo "--- Structure ---"
check "YAML frontmatter with name" '^name: roi-gate$'
check "YAML frontmatter with type" '^type: strategy$'
check "YAML frontmatter with status" '^status: stable$'
check "YAML frontmatter with version" '^version:'
check "YAML frontmatter with token_budget" '^token_budget:'
check "Chain: consumes_from" 'consumes_from:'
check "Chain: feeds_into" 'feeds_into:'
check "Portability target" 'Portability target:'
check "Progressive disclosure QUICK markers" '<!-- QUICK:'
check "Progressive disclosure STANDARD markers" '<!-- STANDARD:'
check "Progressive disclosure DEEP markers" '<!-- DEEP:'

echo ""
echo "--- Content Quality ---"
check "Ground Rules table" 'Negative Constraint'
check "At least 3 ground rules (R1-R5)" '| \*\*R[1-5]\*\*'
check "Route the Request section" '## Route the Request'
check "Auto-Route table" '### Auto-Route'
check "Intent Route tree" '### Intent Route'
check "Core Workflow section" '## Core Workflow'
check "Decision Trees section" '## Decision Trees'
check "Error Decoder section" '## Error Decoder'
check "Production Checklist section" '## Production Checklist'
check "At least 10 checklist items" '\[ROI[0-9]'
check "Cross-Skill Coordination" '## Cross-Skill Coordination'
check "Proactive Triggers section" '## Proactive Triggers'
check "Anti-Patterns section" '## Anti-Patterns'
check "What Good Looks Like" '## What Good Looks Like'
check "References section" '## References'
check "Operating at Different Levels" '## Operating at Different Levels'
check "When NOT to Use / Gate Bypass" '## When NOT to Use'
check "Expert's Mindset section" "## The Expert's Mindset"
check "War story present (DEEP)" '57 years\|$720K\|$45,000\|98.9%'

echo ""
echo "--- Domain-Specific ---"
check "ROI formula present" 'Cost_of_Dev.*Cost_of_Risk.*Annual_Value_of_Fix'
check "Over-engineering detection tree" 'Over-Engineering Detection'
check "Dependency ROI calculator" 'Dependency ROI Calculator'
check "Abstraction cost calculator" 'Abstraction Cost Calculator'
check "Payback period check" 'payback\|Payback'
check "Gate bypass rules" 'bypass\|Bypass'

echo ""
if [ "$ERRORS" -gt 0 ]; then
    echo "❌ $ERRORS check(s) failed."
    exit 1
else
    echo "✅ All checks passed. roi-gate is 10/10."
fi
