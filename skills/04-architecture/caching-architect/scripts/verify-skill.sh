#!/usr/bin/env bash
# Verification harness for caching-architect.
#
# Two layers:
#   1. Structural — the sections and frontmatter the library requires.
#   2. Domain invariants — the cache-correctness content this skill is FOR: the six ground rules,
#      invalidation strategies, key-schema discipline, stampede defences, staleness budgets,
#      layer coherence, and hit-rate-by-key-class measurement.
#
# Run: bash scripts/verify-skill.sh
set -euo pipefail

echo "=== Verifying caching-architect ==="
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
check "name matches directory" grep -q "^name: caching-architect" "$SKILL"

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

check "R1 TTL-is-not-invalidation rule" contains "TTL as the only invalidation"
check "R2 key schema rule" contains "key schema"
check "R3 stampede defence rule" contains "stampede defence"
check "R4 staleness budget rule" contains "staleness budget"
check "R5 layer coherence rule" contains "coherence rule between layers"
check "R6 measure-before-tuning rule" contains "measured hit rate"

check "immutable key strategy" contains "immutable key"
check "write-through invalidation" contains "write-through"
check "event-driven invalidation" contains "event-driven"
check "versioned key strategy" contains "versioned key"
check "stale-while-revalidate" contains "stale-while-revalidate"

check "single-flight defence" contains "single-flight"
check "request coalescing" contains "coalescing"
check "probabilistic early expiry" contains "probabilistic early expiry"
check "distributed lock with TTL" contains "lock TTL"

check "tenant/scope separator dimensions" contains "authorization scope"
check "collision test required" contains "collision test"
check "keys are a security boundary" contains "security boundary"

check "layer precedence defined" contains "precedence"
check "propagation order defined" contains "propagation"
check "hit rate by key class" contains "by key class"
check "negative caching policy" contains "negative"

check "verification pass criteria present" contains "Pass criteria"
check "cold-start defended" contains "cold start"
check "dollar-quantified gotchas present" grep -qE '\$[0-9,]{4,}' "$SKILL"

echo ""
echo "-- Reference depth --"
# The extended material lives in focused files indexed from additional-resources.md; assert each
# file the SKILL.md References section names actually exists, so a future edit cannot orphan one.
ref_fail=0
while IFS= read -r ref; do
    [ -z "$ref" ] && continue
    if [ ! -f "$SKILL_DIR/$ref" ]; then
        echo "  MISSING $ref"
        ref_fail=$((ref_fail + 1))
    fi
done < <(grep -oE 'references/[a-z0-9-]+\.md' "$SKILL" | sort -u)
check "every referenced file exists" test "$ref_fail" -eq 0

check "reference count meets corpus standard" bash -c "test \$(ls '$SKILL_DIR/references'/*.md 2>/dev/null | wc -l) -ge 9"
check "index maps the focused files" grep -q "Reference file map" "$SKILL_DIR/references/additional-resources.md"
check "sources file has a sources table" grep -qi "^## Sources" "$SKILL_DIR/references/sources.md"

echo ""
echo "-- Backtest provenance --"
check "backtest tags COMPUTED" grep -qi "COMPUTED" "$SKILL_DIR/examples/backtest/README.md"
check "backtest tags ESTIMATED" grep -qi "ESTIMATED" "$SKILL_DIR/examples/backtest/README.md"

echo ""
echo "-- Eval coverage --"
check "evals.json declares this skill" grep -q '"skill": "caching-architect"' "$SKILL_DIR/evals/evals.json"

echo ""
echo "========================================"
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
echo "========================================"

if [ $FAIL -gt 0 ]; then
    exit 1
fi
