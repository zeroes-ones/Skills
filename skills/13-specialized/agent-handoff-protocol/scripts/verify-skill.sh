#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_FILE="$SKILL_DIR/SKILL.md"
REFERENCES_DIR="$SKILL_DIR/references"
ERRORS=0
WARNINGS=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_pass() { echo -e "  ${GREEN}[PASS]${NC} $1"; }
log_fail() { echo -e "  ${RED}[FAIL]${NC} $1"; ERRORS=$((ERRORS + 1)); }
log_warn() { echo -e "  ${YELLOW}[WARN]${NC} $1"; WARNINGS=$((WARNINGS + 1)); }

echo "================================================"
echo "Verifying: agent-handoff-protocol SKILL.md"
echo "================================================"

# --- 1. File existence ---
echo ""
echo "[1] File existence checks..."

if [[ -f "$SKILL_FILE" ]]; then
    log_pass "SKILL.md exists"
else
    log_fail "SKILL.md not found at $SKILL_FILE"
fi

if [[ -d "$REFERENCES_DIR" ]]; then
    log_pass "references/ directory exists"
else
    log_fail "references/ directory not found"
fi

if [[ -f "$SKILL_DIR/scripts/verify-skill.sh" ]]; then
    log_pass "scripts/verify-skill.sh exists"
else
    log_fail "scripts/verify-skill.sh not found"
fi

# --- 2. Frontmatter checks ---
echo ""
echo "[2] Frontmatter checks..."

check_frontmatter_field() {
    local field_name="$1"
    if grep -q "^${field_name}:" "$SKILL_FILE"; then
        log_pass "Frontmatter has '${field_name}'"
    else
        log_fail "Frontmatter missing '${field_name}'"
    fi
}

check_frontmatter_field "name"
check_frontmatter_field "description"
check_frontmatter_field "author"
check_frontmatter_field "license"
check_frontmatter_field "portability"
check_frontmatter_field "type"
check_frontmatter_field "status"
check_frontmatter_field "version"
check_frontmatter_field "updated"
check_frontmatter_field "tags"
check_frontmatter_field "token_budget"
check_frontmatter_field "chain"

# --- 3. Required 14 section headings ---
echo ""
echo "[3] Required section headings..."

REQUIRED_SECTIONS=(
    "## Route the Request"
    "## Ground Rules"
    "## The Expert's Mindset"
    "## Operating at Different Levels"
    "## When to Use"
    "## Core Workflow"
    "## Decision Trees"
    "## Cross-Skill Coordination"
    "## Proactive Triggers"
    "## What Good Looks Like"
    "## Deliberate Practice"
    "## Gotchas"
    "## Verification"
    "## References"
)

for section in "${REQUIRED_SECTIONS[@]}"; do
    if grep -Fq "$section" "$SKILL_FILE"; then
        log_pass "Section found: '${section}'"
    else
        log_fail "Section missing: '${section}'"
    fi
done

# --- 4. Additional required sections ---
echo ""
echo "[4] Additional required sections..."

if grep -q "^## Anti-Rationalization" "$SKILL_FILE"; then
    log_pass "Section found: '## Anti-Rationalization'"
else
    log_fail "Section missing: '## Anti-Rationalization — No Excuses'"
fi

if grep -q "Portability target:" "$SKILL_FILE"; then
    log_pass "Portability target line found"
else
    log_fail "Portability target line missing"
fi

# --- 5. Decision trees (minimum 5) ---
echo ""
echo "[5] Decision tree checks..."

TREE_COUNT=$(grep -c "^### Decision Tree [0-9]" "$SKILL_FILE" || true)
if [[ "$TREE_COUNT" -ge 5 ]]; then
    log_pass "Found $TREE_COUNT decision trees (minimum 5 required)"
else
    log_fail "Only $TREE_COUNT decision trees found (minimum 5 required)"
fi

ASCII_TREE_COUNT=$(grep -c '[├└│─]' "$SKILL_FILE" || true)
if [[ "$ASCII_TREE_COUNT" -ge 10 ]]; then
    log_pass "Found $ASCII_TREE_COUNT ASCII tree characters"
else
    log_warn "Only $ASCII_TREE_COUNT ASCII tree characters — trees may be incomplete"
fi

# --- 6. Dollar-quantified gotchas (minimum 5) ---
echo ""
echo "[6] Gotcha checks..."

DOLLAR_GOTCHA_COUNT=$(grep -c '\$[0-9]' "$SKILL_FILE" || true)
if [[ "$DOLLAR_GOTCHA_COUNT" -ge 5 ]]; then
    log_pass "Found $DOLLAR_GOTCHA_COUNT dollar-quantified gotchas (minimum 5 required)"
else
    log_fail "Only $DOLLAR_GOTCHA_COUNT dollar-quantified gotchas found (minimum 5 required)"
fi

GOTCHA_COUNT=$(grep -c '^| [0-9] |' "$SKILL_FILE" || true)
if [[ "$GOTCHA_COUNT" -ge 5 ]]; then
    log_pass "Found $GOTCHA_COUNT gotcha entries in table"
else
    log_fail "Only $GOTCHA_COUNT gotcha entries found (minimum 5 required)"
fi

# --- 7. Ground Rules with Mechanical Trigger + Violation Response ---
echo ""
echo "[7] Ground Rules checks..."

GROUND_RULES_COUNT=$(sed -n '/^## Ground Rules/,/^## /p' "$SKILL_FILE" | sed '$d' | grep -c '^| [0-9] |' || true)
if [[ "$GROUND_RULES_COUNT" -ge 5 ]]; then
    log_pass "Found $GROUND_RULES_COUNT ground rules (minimum 5 recommended)"
else
    log_warn "Only $GROUND_RULES_COUNT ground rules found"
fi

if grep -q "Mechanical Trigger" "$SKILL_FILE"; then
    log_pass "Ground Rules table has 'Mechanical Trigger' column"
else
    log_fail "Ground Rules table missing 'Mechanical Trigger' column"
fi

if grep -q "Violation Response" "$SKILL_FILE"; then
    log_pass "Ground Rules table has 'Violation Response' column"
else
    log_fail "Ground Rules table missing 'Violation Response' column"
fi

# --- 8. Reference links resolve ---
echo ""
echo "[8] Reference link checks..."

REF_LINKS=$(grep -o 'references/[^)]*' "$SKILL_FILE" || true)
REF_COUNT=$(echo "$REF_LINKS" | grep -c . || true)

if [[ "$REF_COUNT" -ge 5 ]]; then
    log_pass "Found $REF_COUNT reference links"
else
    log_warn "Only $REF_COUNT reference links found (minimum 5 recommended)"
fi

while IFS= read -r ref_path; do
    if [[ -n "$ref_path" ]]; then
        full_path="$SKILL_DIR/$ref_path"
        if [[ -f "$full_path" ]]; then
            log_pass "Reference resolves: $ref_path"
        else
            log_fail "Reference broken: $ref_path (file not found)"
        fi
    fi
done <<< "$REF_LINKS"

# --- 9. Reference file count ---
echo ""
echo "[9] Reference files in references/..."

REF_FILE_COUNT=$(find "$REFERENCES_DIR" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')
if [[ "$REF_FILE_COUNT" -ge 8 ]]; then
    log_pass "Found $REF_FILE_COUNT reference .md files (minimum 8 required)"
else
    log_fail "Only $REF_FILE_COUNT reference .md files found (minimum 8 required)"
fi

# --- 10. Content quality checks ---
echo ""
echo "[10] Content quality checks..."

if grep -q "A1\|A2\|A3\|A4\|A5\|A6\|A7\|A8" "$SKILL_FILE"; then
    log_pass "Auto-route table found (A1-A8 anchors)"
else
    log_warn "Auto-route table may be incomplete"
fi

if grep -q "Intent Route Tree\|intent route tree" "$SKILL_FILE"; then
    log_pass "Intent route tree found"
else
    log_warn "Intent route tree not explicitly labeled"
fi

if grep -q "Completeness Bias\|Recency Bias\|Ownership Bias" "$SKILL_FILE"; then
    log_pass "Cognitive bias table found (at least 3 biases)"
else
    log_warn "Cognitive bias table may be incomplete"
fi

L_LEVEL_COUNT=$(grep -c '| L[1-5] |' "$SKILL_FILE" || true)
if [[ "$L_LEVEL_COUNT" -ge 5 ]]; then
    log_pass "Found $L_LEVEL_COUNT operating levels (L1-L5)"
else
    log_fail "Only $L_LEVEL_COUNT operating levels found (L1-L5 required)"
fi

TRIGGER_COUNT=$(sed -n '/^## Proactive Triggers/,/^## /p' "$SKILL_FILE" | sed '$d' | grep -c '^| [0-9] |' || true)
if [[ "$TRIGGER_COUNT" -ge 5 ]]; then
    log_pass "Found $TRIGGER_COUNT proactive triggers (minimum 5 required)"
else
    log_fail "Only $TRIGGER_COUNT proactive triggers found (minimum 5 required)"
fi

if grep -q "Why It Matters" "$SKILL_FILE"; then
    log_pass "Proactive Triggers has 'Why It Matters' column"
else
    log_fail "Proactive Triggers missing 'Why It Matters' column"
fi

if grep -q "If Ignored" "$SKILL_FILE"; then
    log_pass "Proactive Triggers has 'If Ignored' column"
else
    log_fail "Proactive Triggers missing 'If Ignored' column"
fi

if grep -q "Excellent.*Mediocre.*Unacceptable" "$SKILL_FILE"; then
    log_pass "What Good Looks Like has 3-column format"
else
    log_warn "What Good Looks Like 3-column format not confirmed"
fi

if grep -q "Deliberate Practice" "$SKILL_FILE" && grep -q "What You'll Learn" "$SKILL_FILE"; then
    log_pass "Deliberate Practice table found with expected columns"
else
    log_warn "Deliberate Practice table may be incomplete"
fi

ANTI_COUNT=$(sed -n '/^## Anti-Rationalization/,/^## /p' "$SKILL_FILE" | sed '$d' | grep -c '^| ' || true)
if [[ "$ANTI_COUNT" -ge 6 ]]; then
    log_pass "Found $((ANTI_COUNT - 1)) anti-rationalization rows (minimum 5 required)"
else
    log_fail "Only $((ANTI_COUNT - 1)) anti-rationalization rows found (minimum 5 required)"
fi

if grep -q "Upstream\|Consumes From\|Downstream\|Feeds Into" "$SKILL_FILE"; then
    log_pass "Cross-Skill Coordination has upstream/downstream tables"
else
    log_warn "Cross-Skill Coordination upstream/downstream tables not confirmed"
fi

# --- 11. Line count check ---
echo ""
echo "[11] Size checks..."

LINE_COUNT=$(wc -l < "$SKILL_FILE" | tr -d ' ')
if [[ "$LINE_COUNT" -ge 450 ]] && [[ "$LINE_COUNT" -le 700 ]]; then
    log_pass "SKILL.md is $LINE_COUNT lines (target: 500-600)"
elif [[ "$LINE_COUNT" -lt 450 ]]; then
    log_warn "SKILL.md is $LINE_COUNT lines — shorter than target 500-600"
else
    log_warn "SKILL.md is $LINE_COUNT lines — longer than target 500-600"
fi

# --- Summary ---
echo ""
echo "================================================"
if [[ "$ERRORS" -eq 0 ]]; then
    echo -e "${GREEN}VERIFICATION PASSED${NC} — 0 errors, $WARNINGS warnings"
else
    echo -e "${RED}VERIFICATION FAILED${NC} — $ERRORS errors, $WARNINGS warnings"
fi
echo "================================================"

exit "$ERRORS"
