#!/usr/bin/env bash
# Verification harness for cost-accounting
#
# Asserts this skill's domain INVARIANTS — not just that section headings exist,
# but that the skill actually encodes the rules it claims (ground rules R1-R6,
# the three separate axes, the ABI-breaking-change list, the unload reality,
# the update model, and the reference depth G14 requires).
#
# Run: bash scripts/verify-skill.sh
set -euo pipefail

echo "=== Verifying cost-accounting ==="
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
check "name matches directory" grep -q '^name: cost-accounting$' "$S"

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

# ── Anti-hallucination guardrails ────────────────────────────────────────────
check "guardrail: Admit uncertainty" grep -q 'Admit uncertainty' "$S"
check "guardrail: Flag your knowledge cutoff" grep -q 'Flag your knowledge cutoff' "$S"
check "guardrail: Never guess security" grep -q 'Never guess security' "$S"
check "guardrail: [VERIFIED] provenance" grep -q '\[VERIFIED\]' "$S"

# ── Ground rules ─────────────────────────────────────────────────────────────
for r in R1 R2 R3 R4 R5 R6; do
    check "ground rule $r present" grep -q "\*\*$r\*\*" "$S"
done
check "Ground Rules has Mechanical Trigger column" grep -q 'Mechanical Trigger' "$S"
check "Ground Rules has Violation Response column" grep -q 'Violation Response' "$S"
check "ground rules use REFUSE (blocking language)" grep -q 'REFUSE' "$S"

# ── Invariant assertions: the domain claims the skill must actually encode ──
check "asserts measured vs unmeasured (R1)" grep -qi 'unmeasured' "$S"
check "asserts unmeasured is not zero" grep -qi 'silence' "$S"
check "refuses quoting an untagged figure (R1)" grep -qi 'measurement status' "$S"
check "asserts proxies must be labelled (R2)" grep -qi 'proxy' "$S"
check "asserts proxy drift" grep -qi 'drift' "$S"
check "asserts cost per SUCCESS not per call (R3)" grep -qi 'cost per successful outcome\|cost-per-success' "$S"
check "asserts pairing cost with outcome" grep -qi 'success rate' "$S"
check "asserts budget enforcement (R4)" grep -qi 'enforc' "$S"
check "asserts a recorded increase path (R4)" grep -qi 'increase path' "$S"
check "asserts attribution by node (R5)" grep -qi 'attribut' "$S"
check "asserts phase attribution (retry/escalation)" grep -qi 'retry\|escalation' "$S"
check "asserts a total is not a cause" grep -qi 'total' "$S"
check "asserts forecast from measured units (R6)" grep -qi 'forecast' "$S"
check "asserts scale multiplies" grep -qi 'multipl' "$S"
check "asserts reconciliation against the invoice" grep -qi 'invoice' "$S"
check "asserts the loop is the multiplier" grep -qi 'loop' "$S"
check "asserts showback before chargeback" grep -qi 'showback' "$S"
check "never trades a security control for a saving" grep -qi 'security' "$S"
check "names the run-level vs per-request lever split" grep -qi 'run-level' "$S"
check "asserts the price source is dated" grep -qi 'price' "$S"
check "asserts an accepted variance band" grep -qi 'band\|variance' "$S"
check "cites the repo's own cost plumbing" grep -qi 'max_cost_usd\|measured' "$S"

# ── Decision trees: >= 3 with Yes/No branches ────────────────────────────────
DT_SECTION="$(sed -n '/^## Decision Trees/,/^## Core Workflow/p' "$S")"
dt_count=$(printf '%s\n' "$DT_SECTION" | grep -c '^### ' || true)
if [ "${dt_count:-0}" -ge 3 ]; then
    echo "  PASS decision trees (${dt_count}, min 3)"
    PASS=$((PASS + 1))
else
    echo "  FAIL decision trees (${dt_count}, need >= 3)"
    FAIL=$((FAIL + 1))
fi
check "decision trees branch" grep -q '→' <<<"$DT_SECTION"

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
