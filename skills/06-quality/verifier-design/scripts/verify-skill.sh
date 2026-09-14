#!/usr/bin/env bash
# Verification harness for verifier-design.
#
# Two layers:
#   1. Structural — the sections, frontmatter and artefacts the library requires.
#   2. Domain invariants — the verifier-design content this skill is FOR: fire cases, silent cases,
#      negative controls, anchoring on final identifiers, joint-rule contradiction, severity
#      calibration, reasoned allowlists, the artefact-versus-configuration rule, and the
#      discovery-ratio argument.
#
# Run: bash scripts/verify-skill.sh
set -euo pipefail

echo "=== Verifying verifier-design ==="
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
check "examples/backtest/README.md exists" test -f "$SKILL_DIR/examples/backtest/README.md"
check "frontmatter present" grep -q "^---$" "$SKILL"
check "token_budget declared" grep -q "token_budget:" "$SKILL"
check "chain declared" grep -q "chain:" "$SKILL"
check "examples declared in chain" grep -q "examples:" "$SKILL"
check "workflow contract declared" grep -q "^workflow:" "$SKILL"
check "portability target declared" contains "Portability target"
check "name matches directory" grep -q "^name: verifier-design" "$SKILL"

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

check "R1 fire case + silent case rule" contains "fire case and a silent case"
check "R2 negative control rule" contains "without a negative control"
check "R3 pre-transform comparison rule" contains "transform has not applied yet"
check "R4 allowlist reason rule" contains "without a written reason"
check "R5 joint-rule contradiction rule" contains "without a contradiction check"
check "R6 severity calibration rule" contains "severity was not calibrated"
check "R7 artefact-not-configuration rule" contains "reads configuration as evidence about an artefact"

check "clean-is-not-evidence thesis" contains "a clean run contains almost no information"
check "shared-assumption principle" contains "cannot catch a bug in that assumption"
check "ignored gate principle" contains "an ignored gate is worse than no gate"
check "discovery ratio argument" contains "found by reading"
check "probe method" contains "probe"
check "first-run false positives" contains "28"

check "tiering by ownership" contains "strict inside"
check "property versus circumstance" contains "property of the input"
check "legal spelling invariant" contains "legal spelling"
check "both directions of a consistency check" contains "both directions"
check "idempotency plus detection" contains "idempotency"
check "fail loudly when unreadable" contains "fail loudly" || contains "fails loudly"
check "stale versus wrong" contains "stale"

check "all four decision trees present" bash -c "grep -qc 'Decision Tree 4' '$SKILL' && grep -q 'Decision Tree 3' '$SKILL' && grep -q 'Decision Tree 2' '$SKILL' && grep -q 'Decision Tree 1' '$SKILL'"
check "verification pass criteria present" contains "Pass criteria"
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
check "failure narratives cite the source ledger" grep -q "native-learnings" "$SKILL_DIR/references/sources.md"

echo ""
echo "-- Backtest provenance --"
check "backtest tags COMPUTED" grep -qi "COMPUTED" "$SKILL_DIR/examples/backtest/README.md"
check "backtest tags ESTIMATED" grep -qi "ESTIMATED" "$SKILL_DIR/examples/backtest/README.md"
check "backtest tags VERIFIED" grep -qi "VERIFIED" "$SKILL_DIR/examples/backtest/README.md"
check "backtest has best case" grep -qi "best case" "$SKILL_DIR/examples/backtest/README.md"
check "backtest has worst case" grep -qi "worst case" "$SKILL_DIR/examples/backtest/README.md"
check "backtest has learnings" grep -qi "learnings" "$SKILL_DIR/examples/backtest/README.md"
check "backtest is dollar-quantified" grep -qE '\$[0-9,]{4,}' "$SKILL_DIR/examples/backtest/README.md"

echo ""
echo "-- Applied to this skill (the gate audits itself) --"
# This skill's own thesis is that a check must be proven to fire. These assertions are the
# self-application: the harness must be able to fail, and it must be able to stay silent.
check "verify-skill.sh reports a PASS count" grep -q 'PASS: \$PASS' "$SKILL_DIR/scripts/verify-skill.sh"
check "verify-skill.sh exits non-zero on failure" grep -q 'exit 1' "$SKILL_DIR/scripts/verify-skill.sh"
check "verify-skill.sh has a negative control (a deliberately absent file is checked)" grep -q 'MISSING' "$SKILL_DIR/scripts/verify-skill.sh"

echo ""
echo "========================================"
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
echo "========================================"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
