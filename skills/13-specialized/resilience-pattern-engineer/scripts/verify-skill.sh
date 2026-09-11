#!/usr/bin/env bash
# Verification harness for resilience-pattern-engineer.
#
# Two layers:
#   1. Structural — the skill file has the sections and frontmatter the library requires.
#   2. Domain invariants — the resilience-specific content this skill is *for* actually exists:
#      the six ground rules, the five failure modes, the pattern set, the sizing formulas, and
#      the requirement that every defence has a test observed to fire.
#
# Run: bash scripts/verify-skill.sh
set -euo pipefail

echo "=== Verifying resilience-pattern-engineer ==="
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
check "frontmatter present" grep -q "^---$" "$SKILL"
check "token_budget declared" grep -q "token_budget:" "$SKILL"
check "chain declared" grep -q "chain:" "$SKILL"
check "workflow contract declared" grep -q "^workflow:" "$SKILL"
check "portability target declared" contains "Portability target"
check "name matches directory" grep -q "^name: resilience-pattern-engineer" "$SKILL"

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
check "R1 retry-jitter rule present" contains "REFUSE to add retries without jitter"
check "R2 deadline-derived timeout rule present" contains "REFUSE to declare a timeout"
check "R3 firing-test rule present" contains "requires a test that proves it fires"
check "R4 no-silent-degradation rule present" contains "Never degrade silently"
check "R5 measured-bulkhead rule present" contains "measured concurrency"
check "R6 worst-case failure-mode rule present" contains "worst for you"

# The five failure modes R6 demands — the whole point of the failure-mode phase.
check "failure mode: slow" contains "slow / hang"
check "failure mode: hang" contains "hang"
check "failure mode: partial" contains "partial"
check "failure mode: wrong-200" contains "wrong-200"
check "failure mode: flapping" contains "flapping"

# Pattern coverage: the defences a reader comes here to find.
check "timeout pattern" contains "timeout"
check "retry with jitter" contains "jitter"
check "circuit breaker pattern" contains "circuit breaker"
check "bulkhead pattern" contains "bulkhead"
check "load shedding pattern" contains "shed"
check "graceful degradation pattern" contains "degradation ladder"

# Quantified guidance, not vibes.
check "jitter formula present" grep -q "random(0, min(cap" "$SKILL"
check "Little's Law sizing present" contains "Little's Law"
check "headroom multiplier stated" contains "1.3 headroom"
check "half-open ramp described" contains "half-open"

# Verification must be runnable, not aspirational.
check "verification pass criteria present" contains "Pass criteria"
check "chaos test required per defence" contains "observed to fire"
check "dollar-quantified gotchas present" grep -qE '\$[0-9,]{4,}' "$SKILL"

echo ""
echo "========================================"
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
echo "========================================"

if [ $FAIL -gt 0 ]; then
    exit 1
fi
