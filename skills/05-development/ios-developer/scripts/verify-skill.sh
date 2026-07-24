#!/usr/bin/env bash
set -euo pipefail

# verify-skill.sh — Validates the iOS Developer SKILL.md completeness and reference integrity
# Usage: bash scripts/verify-skill.sh [--strict]

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
STRICT=false
[[ "${1:-}" == "--strict" ]] && STRICT=true

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
pass=0; fail=0

check() {
    local desc="$1"; shift
    if "$@"; then
        echo -e "${GREEN}[PASS]${NC} $desc"; ((pass++))
    else
        echo -e "${RED}[FAIL]${NC} $desc"; ((fail++))
    fi
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

echo "=== iOS Developer SKILL.md Verification ==="
echo "SKILL_DIR: $SKILL_DIR"
echo ""

# File existence
check "SKILL.md exists"             test -f "$SKILL_MD"

# Frontmatter checks
check "Has frontmatter name"        grep -q '^name:' "$SKILL_MD" 2>/dev/null
check "Has frontmatter description" grep -q '^description:' "$SKILL_MD" 2>/dev/null
check "Has author field"            grep -q 'author:' "$SKILL_MD" 2>/dev/null
check "Has license field"           grep -q 'license:' "$SKILL_MD" 2>/dev/null
check "Has portability field"       grep -q 'portability:' "$SKILL_MD" 2>/dev/null
check "Has version field"           grep -q 'version:' "$SKILL_MD" 2>/dev/null

# Structure
check "Has Ground Rules section"    grep -q 'Ground Rules' "$SKILL_MD" 2>/dev/null
check "Has Decision Trees section"  grep -q 'Decision Tree' "$SKILL_MD" 2>/dev/null
check "Has Core Workflow section"   grep -q 'Core Workflow' "$SKILL_MD" 2>/dev/null
check "Has Gotchas section"         grep -q 'Gotchas' "$SKILL_MD" 2>/dev/null
check "Has Scale Depth section"     grep -q 'Scale Depth' "$SKILL_MD" 2>/dev/null
check "Has Production Checklist"    grep -q 'Production Checklist' "$SKILL_MD" 2>/dev/null
check "Has Anti-Rationalization"    grep -q 'Anti-Rationalization' "$SKILL_MD" 2>/dev/null
check "Has Deliberate Practice"     grep -q 'Deliberate Practice' "$SKILL_MD" 2>/dev/null

# References
for ref in swiftui-view-architecture uikit-swiftui-bridging coredata-swiftdata-guide \
           concurrency-actors app-store-submission accessibility-voiceover \
           instruments-profiling xcode-build-settings; do
    check "Reference: references/${ref}.md" test -f "$SKILL_DIR/references/${ref}.md"
done

# Script itself
check "verify-skill.sh is executable" test -x "$SKILL_DIR/scripts/verify-skill.sh"

# Line count
lines=$(wc -l < "$SKILL_MD" | tr -d ' ')
if [ "$lines" -ge 650 ]; then
    check "SKILL.md is >= 650 lines ($lines lines)" true
else
    warn "SKILL.md is $lines lines (target: 650-800)"
    if $STRICT; then ((fail++)); fi
fi

# Summary
echo ""
echo "=== Results: $pass passed, $fail failed ==="
if [ "$fail" -gt 0 ]; then
    echo -e "${RED}Some checks failed.${NC}"
    exit 1
else
    echo -e "${GREEN}All checks passed.${NC}"
fi
