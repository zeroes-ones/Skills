#!/usr/bin/env bash
# Verification harness for platform-hig-architect
#
# Asserts this skill's domain INVARIANTS — not just that section headings exist,
# but that the skill actually encodes the rules it claims (ground rules R1-R6,
# the decision trees, the measurable budget, and the reference depth G14 requires).
#
# Run: bash scripts/verify-skill.sh
set -euo pipefail

echo "=== Verifying platform-hig-architect ==="
echo ""

PASS=0
FAIL=0

check() {
    local name="$1"; shift
    if "$@" >/dev/null 2>&1; then
        echo "  PASS $name"
        PASS=$((PASS + 1))
    else
        echo "  FAIL $name"
        FAIL=$((FAIL + 1))
    fi
}

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
S="$SKILL_DIR/SKILL.md"

# ── Structural ───────────────────────────────────────────────────────────────
check "SKILL.md exists" test -f "$S"
check "references/ directory exists" test -d "$SKILL_DIR/references"
check "scripts/ directory exists" test -d "$SKILL_DIR/scripts"
check "examples/backtest present" test -f "$SKILL_DIR/examples/backtest/README.md"
check "frontmatter delimiters" grep -q '^---$' "$S"
check "token_budget declared" grep -q '^token_budget:' "$S"
check "chain block present" grep -q '^chain:' "$S"
check "chain.examples declared" grep -q 'examples:' "$S"
check "name matches directory" grep -q '^name: platform-hig-architect$' "$S"

# ── Reference depth (G14 blocks below 9) ─────────────────────────────────────
ref_count=$(ls "$SKILL_DIR/references"/*.md 2>/dev/null | wc -l | tr -d ' ')
if [ "${ref_count:-0}" -ge 9 ]; then
    echo "  PASS reference depth (${ref_count} files, G14 min 9)"
    PASS=$((PASS + 1))
else
    echo "  FAIL reference depth (${ref_count} files, G14 needs >= 9)"
    FAIL=$((FAIL + 1))
fi

# ── Required sections ────────────────────────────────────────────────────────
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
    "Error Recovery" \
    "Cross-Skill Coordination" \
    "Proactive Triggers" \
    "Anti-Patterns" \
    "State Log" \
    "Production Checklist" \
    "What Good Looks Like" \
    "Verification" \
    "Verification Guardrails" \
    "References" \
    "Gotchas" \
    "Deliberate Practice" \
    "Anti-Rationalization" \
    "Anti-Hallucination"
do
    check "section: $section" grep -q "^## .*$section" "$S"
done

# ── Anti-hallucination guardrails (exact phrases the governance suite greps) ──
check "guardrail: Admit uncertainty" grep -q 'Admit uncertainty' "$S"
check "guardrail: Flag your knowledge cutoff" grep -q 'Flag your knowledge cutoff' "$S"
check "guardrail: Never guess security" grep -q 'Never guess security' "$S"
check "guardrail: [VERIFIED] provenance" grep -q '\[VERIFIED\]' "$S"

# ── Ground rules: all six with mechanical trigger + violation response ───────
for r in R1 R2 R3 R4 R5 R6; do
    check "ground rule $r present" grep -q "\*\*$r\*\*" "$S"
done
check "Ground Rules has Mechanical Trigger column" grep -q 'Mechanical Trigger' "$S"
check "Ground Rules has Violation Response column" grep -q 'Violation Response' "$S"
check "ground rules use REFUSE (blocking language)" grep -q 'REFUSE' "$S"

# ── Invariant assertions: the domain claims the skill must actually encode ──
check "asserts convention matrix before UI (R1)" grep -qi 'convention matrix' "$S"
check "asserts form factor is not a scaled copy (R2)" grep -qi 'scaled copy\|scaled version\|stretched' "$S"
check "asserts documented deviations (R3)" grep -qi 'deviation' "$S"
check "asserts input modalities beyond touch (R4)" grep -qi 'modality\|modalities' "$S"
check "asserts platform text-size setting (R5)" grep -qi 'text-size setting\|text size setting' "$S"
check "asserts platform accessibility contract (R6)" grep -qi 'accessibility contract' "$S"
check "names Apple platforms" grep -q 'iOS' "$S"
check "names watchOS" grep -q 'watchOS' "$S"
check "names visionOS" grep -q 'visionOS' "$S"
check "names tvOS" grep -q 'tvOS' "$S"
check "names Android form factors" grep -qi 'Wear\|foldable' "$S"
check "names web platform" grep -q 'web' "$S"
check "names Windows" grep -q 'Windows' "$S"
check "names Flutter" grep -q 'Flutter' "$S"
check "names React Native" grep -q 'React Native' "$S"
check "names Kotlin Multiplatform" grep -qi 'kotlin-multiplatform\|Kotlin Multiplatform\|Multiplatform' "$S"
check "names .NET MAUI" grep -q 'MAUI' "$S"
check "forbids reimplementing system affordances" grep -qi 'system affordance' "$S"
check "asserts focus model on non-touch surfaces (R4)" grep -qi 'focus order\|focus model' "$S"
check "asserts size classes over device names" grep -qi 'size class' "$S"
check "asserts split view / multitasking verification" grep -qi 'split view' "$S"
check "asserts deep-link back stack" grep -qi 'deep link' "$S"
check "asserts reduced-motion honoured" grep -qi 'motion preference\|reduced-motion\|reduced motion' "$S"
check "carries the versioning caveat (no recalled dimensions)" grep -qi 'release cycle\|SDK version\|version.*verif' "$S"

# ── Decision trees: >= 3 with YES/NO branches ────────────────────────────────
DT_SECTION="$(sed -n '/^## Decision Trees/,/^## Core Workflow/p' "$S")"
dt_count=$(printf '%s\n' "$DT_SECTION" | grep -c '^### ' || true)
if [ "${dt_count:-0}" -ge 3 ]; then
    echo "  PASS decision trees (${dt_count}, min 3)"
    PASS=$((PASS + 1))
else
    echo "  FAIL decision trees (${dt_count}, need >= 3)"
    FAIL=$((FAIL + 1))
fi
check "decision trees branch on Yes" grep -q 'Yes' <<<"$DT_SECTION"
check "decision trees branch on No" grep -q 'No' <<<"$DT_SECTION"

# ── Completion criteria: >= 8 "Complete when" ────────────────────────────────
cw=$(grep -c 'Complete when' "$S" || true)
if [ "${cw:-0}" -ge 8 ]; then
    echo "  PASS completion criteria (${cw} 'Complete when', min 8)"
    PASS=$((PASS + 1))
else
    echo "  FAIL completion criteria (${cw}, need >= 8)"
    FAIL=$((FAIL + 1))
fi

# ── Dollar-quantified gotchas: >= 5 ──────────────────────────────────────────
dollars=$(grep -oE '\$[0-9,]+' "$S" | wc -l | tr -d ' ')
if [ "${dollars:-0}" -ge 5 ]; then
    echo "  PASS dollar-quantified costs (${dollars}, min 5)"
    PASS=$((PASS + 1))
else
    echo "  FAIL dollar-quantified costs (${dollars}, need >= 5)"
    FAIL=$((FAIL + 1))
fi

# ── Progressive disclosure: >= 3 QUICK markers ───────────────────────────────
quick=$(grep -c '\*\*(QUICK' "$S" || true)
if [ "${quick:-0}" -ge 3 ]; then
    echo "  PASS progressive disclosure (${quick} QUICK markers, min 3)"
    PASS=$((PASS + 1))
else
    echo "  FAIL progressive disclosure (${quick}, need >= 3)"
    FAIL=$((FAIL + 1))
fi

# ── Cross-skill coordination tables ──────────────────────────────────────────
check "upstream table present" grep -q '| Upstream Skill' "$S"
check "downstream table present" grep -q '| Downstream Skill' "$S"

# ── Production checklist: >= 10 CR items ─────────────────────────────────────
cr=$(sed -n '/^## Production Checklist/,/^## What Good Looks Like/p' "$S" | grep -c 'CR[0-9]' || true)
if [ "${cr:-0}" -ge 10 ]; then
    echo "  PASS production checklist (${cr} CR items, min 10)"
    PASS=$((PASS + 1))
else
    echo "  FAIL production checklist (${cr}, need >= 10)"
    FAIL=$((FAIL + 1))
fi

# ── All referenced files actually resolve ────────────────────────────────────
broken=0
while IFS= read -r ref; do
    [ -z "$ref" ] && continue
    [ -f "$SKILL_DIR/references/$ref" ] || { echo "  BROKEN references/$ref"; broken=$((broken + 1)); }
done < <(grep -oE '\(references/[^)]+\.md\)' "$S" | sed 's|(references/||; s|)$||' | sort -u)
if [ "$broken" -eq 0 ]; then
    echo "  PASS reference links resolve"
    PASS=$((PASS + 1))
else
    echo "  FAIL $broken broken reference link(s)"
    FAIL=$((FAIL + 1))
fi

# ── Backtest example carries provenance and dollar figures (G13) ─────────────
EX="$SKILL_DIR/examples/backtest/README.md"
check "example has provenance tags" grep -qE '\[VERIFIED\]|\[COMPUTED\]|\[ESTIMATED' "$EX"
check "example has dollar figures" grep -qE '\$[0-9]' "$EX"
check "example covers best case" grep -qiE 'best.case|best outcome|best scenario' "$EX"
check "example covers worst case" grep -qiE 'worst.case|worst outcome|worst scenario' "$EX"
check "example records learnings" grep -qiE 'learning|lesson' "$EX"

echo ""
echo "========================================"
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
echo "========================================"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
