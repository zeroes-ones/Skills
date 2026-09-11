#!/usr/bin/env bash
# Verification harness for configuration-change-safety.
#
# Two layers:
#   1. Structural — the sections and frontmatter the library requires.
#   2. Domain invariants — the change-safety content this skill is FOR: the six ground rules,
#      reversibility classification, validation gates, blast radius on the dependency graph,
#      drift detection, and flag ownership.
#
# Run: bash scripts/verify-skill.sh
set -euo pipefail

echo "=== Verifying configuration-change-safety ==="
echo ""

PASS=0
FAIL=0

check() {
    local name="$1"; shift
    if "$@"; then
        echo "  PASS $name"
        PASS=$((PASS + 1))
    else
        echo "  FAIL $name"
        FAIL=$((FAIL + 1))
    fi
}

contains() { grep -qi -- "$1" "$SKILL"; }

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL="$SKILL_DIR/SKILL.md"

echo "-- Structural --"
check "SKILL.md exists" test -f "$SKILL"
check "references/ directory exists" test -d "$SKILL_DIR/references"
check "scripts/ directory exists" test -d "$SKILL_DIR/scripts"
check "examples/ backtest exists" test -f "$SKILL_DIR/examples/backtest/README.md"
check "frontmatter present" grep -q "^---$" "$SKILL"
check "token_budget declared" grep -q "token_budget:" "$SKILL"
check "chain declared" grep -q "chain:" "$SKILL"
check "examples declared in chain" grep -q "examples:" "$SKILL"
check "workflow contract declared" grep -q "^workflow:" "$SKILL"
check "portability target declared" contains "Portability target"
check "name matches directory" grep -q "^name: configuration-change-safety" "$SKILL"

echo ""
echo "-- Required sections --"
for section in \
    "Route the Request" "Ground Rules" "The Expert's Mindset" \
    "Operating at Different Levels" "When to Use" "When NOT to Use" \
    "Decision Trees" "Core Workflow" "Best Practices" "Error Decoder" \
    "Cross-Skill Coordination" "Proactive Triggers" "What Good Looks Like" \
    "Deliberate Practice" "References" "Gotchas" "Anti-Patterns" \
    "Verification" "Error Recovery" "State Log" "Production Checklist" \
    "Anti-Rationalization"
do
    check "Has $section" contains "$section"
done

echo ""
echo "-- Domain invariants (what this skill is FOR) --"

check "R1 reversibility classification rule" contains "reversibility has not been classified"
check "R2 schema rule" contains "no schema"
check "R3 no-all-at-once rule" contains "all targets at once"
check "R4 drift detection rule" contains "drift undetected"
check "R5 flag ownership rule" contains "owner and a removal date"
check "R6 config-is-not-lower-risk rule" contains "lower-risk than a code change"

check "reversible vs irreversible classification" contains "irreversible"
check "config as code" contains "config as code"
check "drift detection" contains "drift"
check "blast radius on dependency graph" contains "dependency graph"
check "selector verification" contains "selector"
check "progressive rollout" contains "canary"
check "abort thresholds" contains "abort threshold"
check "feature flag lifecycle" contains "flag"
check "change freeze" contains "freeze"
check "validation before apply" contains "pre-apply"

check "numeric abort threshold example" contains "error_rate > 1%"
check "flag removal window stated" contains "60 days"

check "verification pass criteria present" contains "Pass criteria"
check "rollback rehearsal required" contains "executed once outside production"
check "dollar-quantified gotchas present" grep -qE '\$[0-9,]{4,}' "$SKILL"

echo ""
echo "========================================"
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
echo "========================================"

if [ $FAIL -gt 0 ]; then
    exit 1
fi
