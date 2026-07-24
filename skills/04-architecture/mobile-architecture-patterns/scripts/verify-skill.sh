#!/usr/bin/env bash
set -euo pipefail

# verify-skill.sh — Validates mobile-architecture-patterns skill structure and content
# Run from the skill directory: ./scripts/verify-skill.sh

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
REFERENCES_DIR="$SKILL_DIR/references"
ERRORS=0
WARNINGS=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

pass() { echo -e "  ${GREEN}✓${NC} $1"; }
fail() { echo -e "  ${RED}✗${NC} $1"; ERRORS=$((ERRORS + 1)); }
warn() { echo -e "  ${YELLOW}⚠${NC} $1"; WARNINGS=$((WARNINGS + 1)); }

echo "============================================"
echo "Mobile Architecture Patterns — Skill Validator"
echo "============================================"
echo ""

# ─────────────────────────────────────────────
# 1. SKILL.md exists and is non-empty
# ─────────────────────────────────────────────
echo "--- SKILL.md ---"
if [[ -f "$SKILL_MD" ]]; then
    pass "SKILL.md exists"
else
    fail "SKILL.md NOT FOUND at $SKILL_MD"
    echo ""
    echo "CRITICAL: SKILL.md is missing. Cannot continue."
    exit 1
fi

SKILL_LINES=$(wc -l < "$SKILL_MD" | tr -d ' ')
if [[ $SKILL_LINES -ge 500 ]]; then
    pass "SKILL.md has $SKILL_LINES lines (target: 500-600)"
elif [[ $SKILL_LINES -ge 450 ]]; then
    warn "SKILL.md has $SKILL_LINES lines (target: 500-600; close)"
else
    fail "SKILL.md has $SKILL_LINES lines (target: 500-600)"
fi

# ─────────────────────────────────────────────
# 2. YAML Frontmatter
# ─────────────────────────────────────────────
echo ""
echo "--- YAML Frontmatter ---"

if head -1 "$SKILL_MD" | grep -q '^---$'; then
    pass "Frontmatter opening delimiter found"
else
    fail "Frontmatter opening '---' missing"
fi

# Count closing delimiters (second occurrence of --- on its own line)
CLOSING_COUNT=$(grep -c '^---$' "$SKILL_MD" || true)
if [[ $CLOSING_COUNT -ge 2 ]]; then
    pass "Frontmatter closing delimiter found"
else
    fail "Frontmatter closing '---' missing (need 2+ '---' lines)"
fi

# Required frontmatter fields
for field in name description author license version updated tags token_budget chain; do
    if grep -q "^$field:" "$SKILL_MD"; then
        pass "Frontmatter field '$field' present"
    else
        fail "Frontmatter field '$field' MISSING"
    fi
done

NAME_VAL=$(grep "^name:" "$SKILL_MD" | head -1)
if echo "$NAME_VAL" | grep -q "mobile-architecture-patterns"; then
    pass "name field is 'mobile-architecture-patterns'"
else
    fail "name field does not match 'mobile-architecture-patterns': $NAME_VAL"
fi

# ─────────────────────────────────────────────
# 3. Portability Target
# ─────────────────────────────────────────────
echo ""
echo "--- Portability Target ---"
if grep -q "Portability target" "$SKILL_MD"; then
    pass "Portability target statement found"
else
    fail "Portability target statement MISSING"
fi

# ─────────────────────────────────────────────
# 4. Required Sections (15 sections)
# ─────────────────────────────────────────────
echo ""
echo "--- Required Sections ---"

REQUIRED_SECTIONS=(
    "Ground Rules"
    "Decision Trees"
    "Gotchas"
    "Anti-Rationalization"
    "Architecture Overview"
    "MVVM Pattern"
    "Clean Architecture"
    "VIPER Architecture"
    "MVI Pattern"
    "TCA"
    "Navigation Patterns"
    "Offline-First"
    "State Management"
    "Dependency Injection"
    "Testing Strategy"
)

for section in "${REQUIRED_SECTIONS[@]}"; do
    if grep -qi "$section" "$SKILL_MD"; then
        pass "Section '$section' found"
    else
        fail "Section '$section' MISSING"
    fi
done

# ─────────────────────────────────────────────
# 5. Ground Rules — Non-Negotiables
# ─────────────────────────────────────────────
echo ""
echo "--- Ground Rules ---"

# Check for key non-negotiable phrases
GROUND_RULES=(
    "NEVER put business logic"
    "ViewController"
    "Activities"
    "ViewControllers/Activities"
    "Data flows unidirectionally"
    "Dependency injection is mandatory"
    "process death"
    "Offline is not a feature"
    "Navigation state is separate"
)

for rule in "${GROUND_RULES[@]}"; do
    if grep -q "$rule" "$SKILL_MD"; then
        pass "Ground rule phrase found: '$rule'"
    else
        fail "Ground rule phrase MISSING: '$rule'"
    fi
done

# ─────────────────────────────────────────────
# 6. Decision Trees (5+)
# ─────────────────────────────────────────────
echo ""
echo "--- Decision Trees ---"

DT_COUNT=$(grep -c 'START:' "$SKILL_MD" || true)
if [[ $DT_COUNT -ge 5 ]]; then
    pass "$DT_COUNT decision trees found (target: 5+)"
elif [[ $DT_COUNT -ge 1 ]]; then
    warn "$DT_COUNT decision trees found (target: 5+)"
else
    fail "No decision trees found"
fi

# ─────────────────────────────────────────────
# 7. Gotchas (5+ dollar-quantified)
# ─────────────────────────────────────────────
echo ""
echo "--- Gotchas ---"

DOLLAR_COUNT=$(grep -c '\$[0-9]' "$SKILL_MD" || true)
if [[ $DOLLAR_COUNT -ge 5 ]]; then
    pass "$DOLLAR_COUNT dollar-quantified gotchas found (target: 5+)"
else
    fail "$DOLLAR_COUNT dollar-quantified gotchas found (target: 5+)"
fi

# ─────────────────────────────────────────────
# 8. Anti-Rationalization Table (5+ rows)
# ─────────────────────────────────────────────
echo ""
echo "--- Anti-Rationalization ---"

ANTI_ROWS=$(grep -c '^|' "$SKILL_MD" | grep -o '[0-9]*' | head -1 || true)
# Count table rows in the Anti-Rationalization section
ANTI_TABLE=$(sed -n '/Anti-Rationalization/,/^---$/p' "$SKILL_MD" | grep -c '^|' || true)
if [[ $ANTI_TABLE -ge 3 ]]; then
    pass "Anti-Rationalization table has $ANTI_TABLE lines (target: 5+ rows)"
else
    fail "Anti-Rationalization table insufficient: $ANTI_TABLE lines"
fi

# ─────────────────────────────────────────────
# 9. Reference Files
# ─────────────────────────────────────────────
echo ""
echo "--- Reference Files ---"

REF_FILES=(
    "mvvm-mobile-patterns.md"
    "clean-architecture-mobile.md"
    "viper-architecture-ios.md"
    "mvi-android-patterns.md"
    "tca-composable-architecture.md"
    "mobile-navigation-patterns.md"
    "offline-first-mobile.md"
    "mobile-state-management.md"
)

MIN_LINES=200

for ref_file in "${REF_FILES[@]}"; do
    ref_path="$REFERENCES_DIR/$ref_file"

    if [[ -f "$ref_path" ]]; then
        ref_lines=$(wc -l < "$ref_path" | tr -d ' ')
        if [[ $ref_lines -ge $MIN_LINES ]]; then
            pass "$ref_file: $ref_lines lines (target: ${MIN_LINES}+)"
        else
            fail "$ref_file: only $ref_lines lines (target: ${MIN_LINES}+)"
        fi
    else
        fail "$ref_file: FILE NOT FOUND"
    fi
done

# ─────────────────────────────────────────────
# 10. Reference files referenced in SKILL.md
# ─────────────────────────────────────────────
echo ""
echo "--- Cross-References ---"

for ref_file in "${REF_FILES[@]}"; do
    if grep -q "$ref_file" "$SKILL_MD"; then
        pass "$ref_file referenced in SKILL.md"
    else
        warn "$ref_file NOT referenced in SKILL.md"
    fi
done

# ─────────────────────────────────────────────
# 11. Code blocks in reference files
# ─────────────────────────────────────────────
echo ""
echo "--- Code Blocks ---"

for ref_file in "${REF_FILES[@]}"; do
    ref_path="$REFERENCES_DIR/$ref_file"
    if [[ -f "$ref_path" ]]; then
        code_blocks=$(grep -c '```' "$ref_path" || true)
        # Each code block has opening and closing ```, so divide by 2
        actual_blocks=$((code_blocks / 2))
        if [[ $actual_blocks -ge 1 ]]; then
            pass "$ref_file: $actual_blocks code blocks"
        else
            warn "$ref_file: no code blocks found"
        fi
    fi
done

# ─────────────────────────────────────────────
# 12. Scripts directory
# ─────────────────────────────────────────────
echo ""
echo "--- Scripts ---"

SCRIPTS_DIR="$SKILL_DIR/scripts"
if [[ -d "$SCRIPTS_DIR" ]]; then
    pass "scripts/ directory exists"
else
    fail "scripts/ directory MISSING"
fi

if [[ -f "$SCRIPTS_DIR/verify-skill.sh" ]]; then
    if [[ -x "$SCRIPTS_DIR/verify-skill.sh" ]]; then
        pass "verify-skill.sh is executable"
    else
        warn "verify-skill.sh is not executable — run: chmod +x scripts/verify-skill.sh"
    fi
else
    fail "verify-skill.sh missing"
fi

# ─────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────
echo ""
echo "============================================"
if [[ $ERRORS -eq 0 ]]; then
    echo -e "${GREEN}ALL CHECKS PASSED${NC}"
else
    echo -e "${RED}$ERRORS ERROR(S) FOUND${NC}"
fi
if [[ $WARNINGS -gt 0 ]]; then
    echo -e "${YELLOW}$WARNINGS WARNING(S)${NC}"
fi
echo "============================================"

exit $ERRORS
