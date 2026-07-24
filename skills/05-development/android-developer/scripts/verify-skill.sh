#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="android-developer"
ERRORS=0
WARNINGS=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_pass() { echo -e "${GREEN}[PASS]${NC} $1"; }
log_fail() { echo -e "${RED}[FAIL]${NC} $1"; ERRORS=$((ERRORS + 1)); }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; WARNINGS=$((WARNINGS + 1)); }

echo "========================================="
echo " Verifying skill: $SKILL_NAME"
echo " Directory: $SKILL_DIR"
echo "========================================="
echo ""

# --- 1. SKILL.md exists ---
echo "--- SKILL.md ---"
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    log_pass "SKILL.md exists"
else
    log_fail "SKILL.md is missing"
fi

# --- 2. Frontmatter validation ---
if grep -q "^---$" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
    log_pass "YAML frontmatter delimiters found"
else
    log_fail "Missing YAML frontmatter delimiters (---)"
fi

for field in name description author license version updated tags token_budget chain; do
    if grep -q "^${field}:" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
        log_pass "Frontmatter field '${field}' present"
    else
        log_fail "Missing frontmatter field: ${field}"
    fi
done

if grep -q "consumes_from:" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
    log_pass "chain.consumes_from present"
else
    log_fail "Missing chain.consumes_from in frontmatter"
fi

if grep -q "feeds_into:" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
    log_pass "chain.feeds_into present"
else
    log_fail "Missing chain.feeds_into in frontmatter"
fi

# --- 3. Portability target ---
if grep -q "Portability target:" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
    log_pass "Portability target declaration found"
else
    log_fail "Missing portability target declaration"
fi

# --- 4. Title ---
if grep -q "^# Android Developer.*Native Android" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
    log_pass "Title matches: # Android Developer — Native Android Application Development"
else
    log_warn "Title may not match expected format"
fi

# --- 5. Required sections ---
REQUIRED_SECTIONS=(
    "Route the Request"
    "Ground Rules"
    "The Expert's Mindset"
    "Operating at Different Levels"
    "When to Use"
    "Core Workflow"
    "Decision Trees"
    "Cross-Skill Coordination"
    "Proactive Triggers"
    "What Good Looks Like"
    "Deliberate Practice"
    "Gotchas"
    "Anti-Rationalization"
    "Verification"
    "References"
)

for section in "${REQUIRED_SECTIONS[@]}"; do
    if grep -q "^## ${section}" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
        log_pass "Section '${section}' found"
    else
        log_fail "Missing required section: ${section}"
    fi
done

# --- 6. Ground Rules table has 5+ rows ---
GROUND_RULE_COUNT=$(grep -c '| \*\*R[0-9]\*\*' "$SKILL_DIR/SKILL.md" 2>/dev/null || true)
GR_COUNT=$(echo "$GROUND_RULE_COUNT" | tr -d '[:space:]')
if [ -n "$GR_COUNT" ] && [ "$GR_COUNT" -ge 5 ] 2>/dev/null; then
    log_pass "Ground Rules table has ${GR_COUNT} rules (minimum 5)"
else
    log_fail "Ground Rules table has only ${GR_COUNT:-0} rules (need >= 5)"
fi

# --- 7. Decision Trees count ---
DECISION_TREE_COUNT=$(grep -c '^### .* vs \|^### .*Configuration' "$SKILL_DIR/SKILL.md" 2>/dev/null || true)
DT_COUNT=$(echo "$DECISION_TREE_COUNT" | tr -d '[:space:]')
if [ -n "$DT_COUNT" ] && [ "$DT_COUNT" -ge 5 ] 2>/dev/null; then
    log_pass "Decision Trees section has ${DT_COUNT} trees (minimum 5)"
else
    log_fail "Decision Trees section has only ${DT_COUNT:-0} trees (need >= 5)"
fi

# --- 8. Anti-Rationalization table has 5+ rows ---
ANTI_RAT_SECTION=$(sed -n '/^## Anti-Rationalization/,/^## /p' "$SKILL_DIR/SKILL.md" 2>/dev/null || true)
ANTI_RAT_ROW_COUNT=$(echo "$ANTI_RAT_SECTION" | grep -c '^| "' || true)
AR_COUNT=$(echo "$ANTI_RAT_ROW_COUNT" | tr -d '[:space:]')
if [ -n "$AR_COUNT" ] && [ "$AR_COUNT" -ge 5 ] 2>/dev/null; then
    log_pass "Anti-Rationalization table has ${AR_COUNT} rows (minimum 5)"
else
    log_fail "Anti-Rationalization table has only ${AR_COUNT:-0} rows (need >= 5)"
fi

# --- 9. Gotchas with dollar-quantified ($X,000+ or $XK+) ---
GOTCHAS_SECTION=$(sed -n '/^## Gotchas/,/^## /p' "$SKILL_DIR/SKILL.md" 2>/dev/null || true)
DOLLAR_GOTCHA_COUNT=$(echo "$GOTCHAS_SECTION" | grep -cE '\$[0-9]+[0-9,K]' || true)
DG_COUNT=$(echo "$DOLLAR_GOTCHA_COUNT" | tr -d '[:space:]')
if [ -n "$DG_COUNT" ] && [ "$DG_COUNT" -ge 5 ] 2>/dev/null; then
    log_pass "Gotchas section has ${DG_COUNT} dollar-quantified entries (minimum 5)"
else
    log_fail "Gotchas section has only ${DG_COUNT:-0} dollar-quantified entries (need >= 5)"
fi

# --- 10. Reference files ---
echo ""
echo "--- Reference Files ---"
REQUIRED_REFS=(
    "jetpack-compose-patterns.md"
    "android-architecture-patterns.md"
    "kotlin-coroutines-flow.md"
    "room-database-guide.md"
    "android-build-variants.md"
    "play-store-deployment.md"
    "android-accessibility.md"
    "android-performance-optimization.md"
)

for ref in "${REQUIRED_REFS[@]}"; do
    REF_PATH="$SKILL_DIR/references/$ref"
    if [ -f "$REF_PATH" ]; then
        LINE_COUNT=$(wc -l < "$REF_PATH" 2>/dev/null | tr -d '[:space:]')
        if [ -n "$LINE_COUNT" ] && [ "$LINE_COUNT" -ge 200 ] 2>/dev/null && [ "$LINE_COUNT" -le 400 ] 2>/dev/null; then
            log_pass "$ref exists (${LINE_COUNT} lines, in 200-400 range)"
        elif [ -n "$LINE_COUNT" ] && [ "$LINE_COUNT" -gt 400 ] 2>/dev/null; then
            log_warn "$ref is ${LINE_COUNT} lines (target: 200-400, slightly over)"
        else
            log_warn "$ref is only ${LINE_COUNT:-0} lines (target: 200-400)"
        fi
    else
        log_fail "Missing reference file: $ref"
    fi
done

# --- 11. Line count for SKILL.md ---
SKILL_LINES=$(wc -l < "$SKILL_DIR/SKILL.md" 2>/dev/null | tr -d '[:space:]')
echo ""
if [ -n "$SKILL_LINES" ] && [ "$SKILL_LINES" -ge 500 ] 2>/dev/null && [ "$SKILL_LINES" -le 600 ] 2>/dev/null; then
    log_pass "SKILL.md is ${SKILL_LINES} lines (target: 500-600)"
elif [ -n "$SKILL_LINES" ] && [ "$SKILL_LINES" -lt 500 ] 2>/dev/null; then
    log_warn "SKILL.md is only ${SKILL_LINES} lines (target: 500-600)"
else
    log_warn "SKILL.md is ${SKILL_LINES:-0} lines (target: 500-600, slightly over)"
fi

# --- 12. Verify script exists ---
if [ -f "$SKILL_DIR/scripts/verify-skill.sh" ]; then
    log_pass "scripts/verify-skill.sh exists"
else
    log_fail "scripts/verify-skill.sh is missing"
fi

# --- Summary ---
echo ""
echo "========================================="
echo " Verification Summary"
echo "========================================="
echo -e "${GREEN}Passed checks${NC}"
echo -e "${RED}Failed: ${ERRORS}${NC}"
echo -e "${YELLOW}Warnings: ${WARNINGS}${NC}"

if [ "$ERRORS" -gt 0 ]; then
    echo ""
    echo -e "${RED}Verification FAILED. Fix ${ERRORS} error(s) above.${NC}"
    exit 1
else
    echo ""
    echo -e "${GREEN}Verification PASSED.${NC}"
    exit 0
fi
