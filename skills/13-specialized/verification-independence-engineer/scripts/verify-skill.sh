#!/usr/bin/env bash
# Verification harness for verification-independence-engineer.
#
# Two layers:
#   1. Structural — the skill file has the sections and frontmatter the library requires.
#   2. Domain invariants — the verification-independence content this skill is *for* actually
#      exists: the six ground rules, the four independence properties, the metric-pair rule,
#      the calibration requirement, and the cost/benefit framing.
#
# Run: bash scripts/verify-skill.sh
set -euo pipefail

echo "=== Verifying verification-independence-engineer ==="
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

# Case-insensitive content check, kept separate so patterns may contain spaces safely.
contains() {
    grep -qi -- "$1" "$SKILL"
}

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL="$SKILL_DIR/SKILL.md"

echo "-- Structural --"
check "SKILL.md exists" test -f "$SKILL"
check "references/ directory exists" test -d "$SKILL_DIR/references"
check "scripts/ directory exists" test -d "$SKILL_DIR/scripts"
check "examples/backtest exists" test -f "$SKILL_DIR/examples/backtest/README.md"
check "evals/evals.json exists" test -f "$SKILL_DIR/evals/evals.json"
check "references/additional-resources.md exists" test -f "$SKILL_DIR/references/additional-resources.md"
check "frontmatter present" grep -q "^---$" "$SKILL"
check "token_budget declared" grep -q "token_budget:" "$SKILL"
check "chain declared" grep -q "chain:" "$SKILL"
check "workflow contract declared" grep -q "^workflow:" "$SKILL"
check "portability target declared" contains "Portability target"
check "name matches directory" grep -q "^name: verification-independence-engineer" "$SKILL"

echo ""
echo "-- Required sections --"
for section in \
    "Route the Request" \
    "Ground Rules" \
    "The Expert's Mindset" \
    "Operating at Different Levels" \
    "When to Use" \
    "When NOT to Use" \
    "Decision Trees" \
    "Core Workflow" \
    "Best Practices" \
    "Error Decoder" \
    "Cross-Skill Coordination" \
    "Proactive Triggers" \
    "What Good Looks Like" \
    "Deliberate Practice" \
    "References" \
    "Gotchas" \
    "Anti-Patterns" \
    "Verification" \
    "Error Recovery" \
    "State Log" \
    "Production Checklist" \
    "Anti-Rationalization"
do
    check "Has $section" contains "$section"
done

echo ""
echo "-- Domain invariants (what this skill is FOR) --"

# The six ground rules are the skill's non-negotiables; each must survive an edit.
check "R1 no-self-verification rule present" contains "REFUSE to let a producer verify its own output"
check "R2 information-boundary rule present" contains "REFUSE to give a validator the producer's chain of thought"
check "R3 shared-blind-spot rule present" contains "REFUSE to call two agents independent"
check "R4 no-bare-target rule present" contains "REFUSE to optimise a metric that has no paired harm metric"
check "R5 rubber-stamp rule present" contains "REFUSE to trust a validator that has never rejected anything"
check "R6 stated-properties rule present" contains "REFUSE to claim independence without stating and verifying the properties"

# The four independence properties — the core mental model.
check "independence property: model" contains "Model independence"
check "independence property: context" contains "Context independence"
check "independence property: information" contains "Information independence"

# The athlete/referee diagnosis the skill exists to apply.
check "producer/referee framing present" contains "referee"
check "self-verification named as a draft" contains "draft, not a verification"

# Goal blindness / metric betrayal — the second half of the discipline.
check "goal blindness named" contains "goal blindness"
check "proxy/intent distinction present" contains "stand for"

# Calibration is what makes a verdict evidence.
check "known-bad set required" contains "known-bad set"
check "rejection rate is the signal" contains "rejection rate"
check "calibration invalidated by model change" contains "re-calibration trigger"

# Verification must be runnable, not aspirational.
check "verification pass criteria present" contains "Pass criteria"
check "hiding test described" contains "Hide the producer's reasoning"
check "four decision trees present" test "$(grep -c '^### Decision Tree' "$SKILL")" -ge 4
check "dollar-quantified gotchas present" grep -qE '\$[0-9,]{4,}' "$SKILL"

echo ""
echo "-- Backtest provenance --"
check "backtest tags COMPUTED" grep -qi "COMPUTED" "$SKILL_DIR/examples/backtest/README.md"
check "backtest tags ESTIMATED" grep -qi "ESTIMATED" "$SKILL_DIR/examples/backtest/README.md"

echo ""
echo "-- Reference depth --"
check "reference file is not a stub" bash -c "! grep -q '\[Add detailed examples' '$SKILL_DIR/references/additional-resources.md'"
# The metric-leak catalogue and the sources table live in their own focused files, indexed
# from additional-resources.md — check each where it is actually owned.
check "metric-leak catalogue present" grep -qi "metric-leak catalogue\|Harm metric that guards" "$SKILL_DIR/references/metric-leak-catalogue.md"
check "sources table present" grep -qi "^## Sources" "$SKILL_DIR/references/sources.md"

echo ""
echo "-- Eval coverage --"
check "evals.json declares this skill" grep -q '"skill": "verification-independence-engineer"' "$SKILL_DIR/evals/evals.json"
check "eval has a negative-trigger case" grep -q "negative_trigger" "$SKILL_DIR/evals/evals.json"
check "eval covers each ground rule R1-R6" bash -c "for r in r1 r2 r3 r4 r5 r6; do grep -q \"ground-rule-\$r\" '$SKILL_DIR/evals/evals.json' || exit 1; done"

echo ""
echo "========================================"
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
echo "========================================"

if [ $FAIL -gt 0 ]; then
    exit 1
fi
