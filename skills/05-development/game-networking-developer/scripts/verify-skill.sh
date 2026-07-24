#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0
WARNINGS=0

pass() { echo -e "  ${GREEN}PASS${NC} $1"; PASSED=$((PASSED + 1)); }
fail() { echo -e "  ${RED}FAIL${NC} $1"; FAILED=$((FAILED + 1)); }
warn() { echo -e "  ${YELLOW}WARN${NC} $1"; WARNINGS=$((WARNINGS + 1)); }

echo "============================================"
echo "Game Networking Developer — Skill Verifier"
echo "============================================"
echo ""

# ─── Check 1: SKILL.md exists ───
echo "[1] Core files"
if [[ -f "$SKILL_DIR/SKILL.md" ]]; then
    pass "SKILL.md exists"
else
    fail "SKILL.md missing"
fi

# ─── Check 2: Reference files exist ───
declare -a REF_FILES=(
    "client-server-architecture-games.md"
    "prediction-reconciliation-patterns.md"
    "lag-compensation-techniques.md"
    "snapshot-interpolation.md"
    "interest-management.md"
    "nat-traversal-relay.md"
    "matchmaking-architecture.md"
    "dedicated-server-infrastructure.md"
)

for rf in "${REF_FILES[@]}"; do
    if [[ -f "$SKILL_DIR/$rf" ]]; then
        pass "Reference file: $rf exists"
    else
        fail "Reference file: $rf MISSING"
    fi
done

# ─── Check 3: Script exists ───
echo ""
echo "[2] Scripts"
if [[ -f "$SKILL_DIR/scripts/verify-skill.sh" ]]; then
    pass "scripts/verify-skill.sh exists"
else
    fail "scripts/verify-skill.sh missing"
fi

# ─── Check 4: YAML Frontmatter ───
echo ""
echo "[3] YAML Frontmatter"
FRONTMATTER=$(head -30 "$SKILL_DIR/SKILL.md")

check_frontmatter() {
    local field="$1"
    local expected="$2"
    if echo "$FRONTMATTER" | grep -q "^${field}:.*${expected}"; then
        pass "Frontmatter field: $field contains '$expected'"
    else
        warn "Frontmatter field: $field — verify contains '$expected'"
    fi
}

check_frontmatter "name" "game-networking-developer"
check_frontmatter "description" "Game networking engineering"
check_frontmatter "author" "Sandeep Kumar Penchala"
check_frontmatter "license" "MIT"
check_frontmatter "version" "1.0.0"
check_frontmatter "tags" "game-networking"

# Check for chain fields
if echo "$FRONTMATTER" | grep -q "consumes_from:"; then
    pass "Frontmatter has consumes_from"
else
    fail "Frontmatter missing consumes_from"
fi

if echo "$FRONTMATTER" | grep -q "feeds_into:"; then
    pass "Frontmatter has feeds_into"
else
    fail "Frontmatter missing feeds_into"
fi

# Check for token_budget
if echo "$FRONTMATTER" | grep -q "token_budget:"; then
    pass "Frontmatter has token_budget"
else
    warn "Frontmatter missing token_budget"
fi

# ─── Check 5: Portability target header ───
echo ""
echo "[4] Portability target"
if grep -q "Portability target:" "$SKILL_DIR/SKILL.md"; then
    pass "Portability target found"
else
    fail "Portability target missing"
fi

# ─── Check 6: Required sections ───
echo ""
echo "[5] Required sections in SKILL.md"

declare -a REQUIRED_SECTIONS=(
    "Ground Rules"
    "Decision Trees"
    "Gotchas"
    "Anti-Rationalization"
    "Core Architecture Models"
    "Protocol Design"
    "Client-Side Prediction"
    "Lag Compensation"
    "Snapshot Interpolation"
    "Interest Management"
    "NAT Traversal"
    "Matchmaking Architecture"
    "Dedicated Server"
    "Security"
    "Debugging"
)

for section in "${REQUIRED_SECTIONS[@]}"; do
    if grep -qi "$section" "$SKILL_DIR/SKILL.md"; then
        pass "Section found: $section"
    else
        fail "Section MISSING: $section"
    fi
done

# ─── Check 7: Ground Rules non-negotiables ───
echo ""
echo "[6] Ground Rules non-negotiables"
NONNEG=$(grep -c "NEVER\|MUST\|mandatory\|Non-Negotiable\|non-negotiable" "$SKILL_DIR/SKILL.md" || true)
if [[ "$NONNEG" -ge 5 ]]; then
    pass "Found $NONNEG non-negotiable indicators (>=5 required)"
else
    fail "Only $NONNEG non-negotiable indicators found (need >=5)"
fi

# ─── Check 8: Decision trees count ───
echo ""
echo "[7] Decision Trees count"
DT_COUNT=$(grep -c "^### Decision Tree" "$SKILL_DIR/SKILL.md" || true)
if [[ "$DT_COUNT" -ge 5 ]]; then
    pass "Found $DT_COUNT decision trees (>=5 required)"
else
    fail "Only $DT_COUNT decision trees found (need >=5)"
fi

# ─── Check 9: Gotchas with dollar amounts ───
echo ""
echo "[8] Gotchas with dollar-quantified costs"
GOTCHA_COUNT=$(grep -c "^### Gotcha" "$SKILL_DIR/SKILL.md" || true)
DOLLAR_GOTCHAS=$(grep -c '\$[0-9]' "$SKILL_DIR/SKILL.md" || true)
if [[ "$GOTCHA_COUNT" -ge 5 ]]; then
    pass "Found $GOTCHA_COUNT gotchas (>=5 required)"
else
    fail "Only $GOTCHA_COUNT gotchas found (need >=5)"
fi
if [[ "$DOLLAR_GOTCHAS" -ge 5 ]]; then
    pass "Found $DOLLAR_GOTCHAS dollar-quantified cost references"
else
    warn "Only $DOLLAR_GOTCHAS dollar-quantified references (expect >=5)"
fi

# ─── Check 10: Anti-Rationalization table ───
echo ""
echo "[9] Anti-Rationalization table"
ANTI_ROWS=$(grep -c '^| "' "$SKILL_DIR/SKILL.md" || true)
if [[ "$ANTI_ROWS" -ge 5 ]]; then
    pass "Found $ANTI_ROWS anti-rationalization rows (>=5 required)"
else
    fail "Only $ANTI_ROWS anti-rationalization rows (need >=5)"
fi

# ─── Check 11: Reference file references in SKILL.md ───
echo ""
echo "[10] Reference file cross-references"
for rf in "${REF_FILES[@]}"; do
    if grep -q "$rf" "$SKILL_DIR/SKILL.md"; then
        pass "SKILL.md references $rf"
    else
        warn "SKILL.md may not reference $rf"
    fi
done

# ─── Check 12: Line count ───
echo ""
echo "[11] File size checks"
SKILL_LINES=$(wc -l < "$SKILL_DIR/SKILL.md")
if [[ "$SKILL_LINES" -ge 500 && "$SKILL_LINES" -le 700 ]]; then
    pass "SKILL.md is $SKILL_LINES lines (target: 500-600)"
elif [[ "$SKILL_LINES" -gt 700 ]]; then
    warn "SKILL.md is $SKILL_LINES lines (target: 500-600, slightly over)"
else
    warn "SKILL.md is $SKILL_LINES lines (target: 500-600, slightly under)"
fi

for rf in "${REF_FILES[@]}"; do
    RF_LINES=$(wc -l < "$SKILL_DIR/$rf")
    if [[ "$RF_LINES" -ge 180 && "$RF_LINES" -le 450 ]]; then
        pass "Reference $rf: $RF_LINES lines (target: 200-400)"
    elif [[ "$RF_LINES" -lt 180 ]]; then
        warn "Reference $rf: $RF_LINES lines (target: 200-400, under)"
    else
        warn "Reference $rf: $RF_LINES lines (target: 200-400, slightly over)"
    fi
done

# ─── Check 13: Code blocks for technical depth ───
echo ""
echo "[12] Technical depth indicators"
CODE_BLOCKS=$(grep -c '```' "$SKILL_DIR/SKILL.md" || true)
if [[ "$CODE_BLOCKS" -ge 6 ]]; then
    pass "SKILL.md has $((CODE_BLOCKS / 2)) code blocks"
else
    warn "SKILL.md has few code blocks ($((CODE_BLOCKS / 2))) — may lack technical depth"
fi

# Reference files should have code/architecture content
for rf in "${REF_FILES[@]}"; do
    REF_BLOCKS=$(grep -c '```' "$SKILL_DIR/$rf" || true)
    if [[ "$REF_BLOCKS" -ge 4 ]]; then
        pass "Reference $rf: $((REF_BLOCKS / 2)) code blocks"
    else
        warn "Reference $rf: few code blocks — may lack implementation detail"
    fi
done

# ─── Check 14: External references ───
echo ""
echo "[13] External references"
EXT_REFS=$(grep -cE 'github\.com|rfc-|gdc|valve|gambetta|gaffer|agones|gamelift' "$SKILL_DIR/SKILL.md" || true)
if [[ "$EXT_REFS" -ge 5 ]]; then
    pass "Found $EXT_REFS external reference indicators"
else
    warn "Only $EXT_REFS external references found"
fi

# ─── Summary ───
echo ""
echo "============================================"
echo "VERIFICATION SUMMARY"
echo "============================================"
echo -e "  ${GREEN}Passed: $PASSED${NC}"
echo -e "  ${RED}Failed: $FAILED${NC}"
echo -e "  ${YELLOW}Warnings: $WARNINGS${NC}"
echo ""

if [[ "$FAILED" -gt 0 ]]; then
    echo -e "${RED}VERIFICATION FAILED — $FAILED checks failed.${NC}"
    exit 1
else
    echo -e "${GREEN}VERIFICATION PASSED — All critical checks passed with $WARNINGS warnings.${NC}"
    exit 0
fi
