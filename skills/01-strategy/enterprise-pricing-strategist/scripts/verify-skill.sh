#!/bin/bash
# verify-skill.sh — 39-point verification for enterprise-pricing-strategist
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
FAILURES=0

green() { echo -e "\033[0;32m✓\033[0m $1"; }
red()   { echo -e "\033[0;31m✗\033[0m $1"; ((FAILURES++)); }

echo "=== Enterprise Pricing Strategist — Skill Verification ==="
echo ""

# --- EXISTENCE CHECKS ---
echo "[EXISTENCE]"

[ -f "$SKILL_MD" ] && green "SKILL.md exists" || red "SKILL.md MISSING"
[ -d "$SKILL_DIR/references" ] && green "references/ directory exists" || red "references/ MISSING"
[ -d "$SKILL_DIR/scripts" ] && green "scripts/ directory exists" || red "scripts/ MISSING"

# --- YAML FRONTMATTER ---
echo ""
echo "[YAML FRONTMATTER]"

grep -q "^name:" "$SKILL_MD" && green "name field present" || red "name field MISSING"
grep -q "^description:" "$SKILL_MD" && green "description field present" || red "description field MISSING"
grep -q "Do NOT use" "$SKILL_MD" && green "Do NOT use boundary present" || red "Do NOT use boundary MISSING"

CHAIN_COUNT=$(grep -c "consumes_from:\|feeds_into:" "$SKILL_MD" || true)
[ "$CHAIN_COUNT" -ge 2 ] && green "Chain connectivity declared ($CHAIN_COUNT entries)" || red "Chain connectivity INSUFFICIENT ($CHAIN_COUNT)"

# --- REQUIRED SECTIONS ---
echo ""
echo "[REQUIRED SECTIONS]"

REQUIRED_SECTIONS=(
    "Route the Request"
    "When to Use"
    "When NOT to Use"
    "The Expert's Mindset"
    "Operating at Different Levels"
    "Ground Rules"
    "Core Workflow"
    "Decision Trees"
    "Anti-Rationalization"
    "Error Recovery"
    "Error Decoder"
    "Gotchas"
    "Best Practices"
    "Anti-Patterns"
    "Proactive Triggers"
    "Production Checklist"
    "Cross-Skill Coordination"
    "State Log"
    "What Good Looks Like"
    "Anti-Hallucination"
    "Verification"
    "Deliberate Practice"
    "References"
)

for section in "${REQUIRED_SECTIONS[@]}"; do
    grep -q "^## .*${section}" "$SKILL_MD" 2>/dev/null && green "Section: $section" || red "Section MISSING: $section"
done

# --- ANTI-HALLUCINATION ---
echo ""
echo "[ANTI-HALLUCINATION]"

AH_PHRASES=(
    "Admit uncertainty"
    "Flag your knowledge cutoff"
    "Never guess"
    "\[VERIFIED\]"
)

for phrase in "${AH_PHRASES[@]}"; do
    grep -q "$phrase" "$SKILL_MD" 2>/dev/null && green "AH phrase: $phrase" || red "AH phrase MISSING: $phrase"
done

# --- COMPLETION CRITERIA ---
echo ""
echo "[COMPLETION]"

COMPLETE_COUNT=$(grep -ci "Complete when" "$SKILL_MD" || true)
if [ "$COMPLETE_COUNT" -ge 8 ]; then
    green "Complete when: $COMPLETE_COUNT (min 8)"
else
    red "Complete when: $COMPLETE_COUNT (need 8+)"
fi

QUICK_COUNT=$(grep -c "QUICK:" "$SKILL_MD" || true)
if [ "$QUICK_COUNT" -ge 3 ]; then
    green "QUICK markers: $QUICK_COUNT (min 3)"
else
    red "QUICK markers: $QUICK_COUNT (need 3+)"
fi

# --- DECISION TREES ---
echo ""
echo "[DECISION TREES]"

TREE_COUNT=$(grep -c "^###" "$SKILL_MD" | grep -c -E "Decision|Select|Path|Structure" || true)
DT_SUBHEADS=$(grep -c "^### " "$SKILL_MD" || true)
if [ "$DT_SUBHEADS" -ge 10 ]; then
    green "Decision tree sub-sections: $DT_SUBHEADS (ample)"
else
    red "Decision tree sub-sections: $DT_SUBHEADS (likely <3 trees)"
fi

# --- REFERENCE FILES ---
echo ""
echo "[REFERENCES]"

REQUIRED_REFS=(
    "pricing-architecture.md"
    "volume-discount-models.md"
    "roi-calculators.md"
    "contract-negotiation.md"
    "procurement-compliance.md"
    "deal-desk-operations.md"
    "gotchas.md"
    "checklist.md"
)

REF_COUNT=0
for ref in "${REQUIRED_REFS[@]}"; do
    if [ -f "$SKILL_DIR/references/$ref" ]; then
        SIZE=$(wc -c < "$SKILL_DIR/references/$ref" || echo 0)
        if [ "$SIZE" -gt 100 ]; then
            green "Reference: $ref (${SIZE} bytes)"
            ((REF_COUNT++))
        else
            red "Reference: $ref — TOO SMALL ($SIZE bytes)"
        fi
    else
        red "Reference MISSING: $ref"
    fi
done

[ "$REF_COUNT" -ge 8 ] && green "Reference count: $REF_COUNT (min 8)" || red "Reference count: $REF_COUNT (need 8)"

# --- DOLLAR COST REFERENCES ---
echo ""
echo "[DOLLAR QUANTIFICATION]"

DOLLAR_COUNT=$(grep -c '\$[0-9]' "$SKILL_MD" || true)
if [ "$DOLLAR_COUNT" -ge 5 ]; then
    green "Dollar-quantified costs: $DOLLAR_COUNT references (min 5)"
else
    red "Dollar-quantified costs: $DOLLAR_COUNT references (need 5+)"
fi

# --- GROUND RULES ---
echo ""
echo "[GROUND RULES]"

GR_COUNT=$(grep -c "^| R[0-9]" "$SKILL_MD" || true)
TRIGGER_COUNT=$(grep -c "Trigger:" "$SKILL_MD" || true)
if [ "$GR_COUNT" -ge 5 ]; then
    green "Ground rules: $GR_COUNT (min 5)"
else
    red "Ground rules: $GR_COUNT (need 5+)"
fi

if [ "$TRIGGER_COUNT" -ge 5 ]; then
    green "Mechanical triggers: $TRIGGER_COUNT"
else
    red "Mechanical triggers: $TRIGGER_COUNT (need 5+)"
fi

# --- CROSS-SKILL COORDINATION ---
echo ""
echo "[CROSS-SKILL]"

grep -q "| Upstream Skill" "$SKILL_MD" && green "Upstream Skill table present" || red "Upstream Skill table MISSING"

# --- ANTI-PATTERNS ---
echo ""
echo "[ANTI-PATTERNS]"

AP_COUNT=$(grep -c "^\\* ❌" "$SKILL_MD" || true)
if [ "$AP_COUNT" -ge 5 ]; then
    green "Anti-patterns: $AP_COUNT (min 5)"
else
    red "Anti-patterns: $AP_COUNT (need 5+)"
fi

# --- PORTABILITY ---
echo ""
echo "[PORTABILITY]"

grep -q "Portability target" "$SKILL_MD" && green "Portability target declared" || red "Portability target MISSING"

# --- TOKEN BUDGET ---
echo ""
echo "[TOKEN BUDGET]"

BODY_LINES=$(awk '/^---$/{fm++; next} fm>=2{count++} END{print count+0}' "$SKILL_MD")
if [ "$BODY_LINES" -le 600 ]; then
    green "Body lines: $BODY_LINES (budget 600)"
else
    red "Body lines: $BODY_LINES (over 600 budget)"
fi

# --- SUMMARY ---
echo ""
echo "================================="
if [ "$FAILURES" -eq 0 ]; then
    echo -e "\033[0;32mALL CHECKS PASSED\033[0m"
else
    echo -e "\033[0;31m$FAILURES FAILURE(S) DETECTED\033[0m"
fi
echo "================================="

exit $FAILURES
