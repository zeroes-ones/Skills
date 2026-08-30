#!/usr/bin/env bash
# Verification harness for flutter-developer
# Run: bash scripts/verify-skill.sh
set -euo pipefail

echo "=== Verifying flutter-developer ==="
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

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Structural checks
check "SKILL.md exists" test -f "$SKILL_DIR/SKILL.md"
check "references/ directory exists" test -d "$SKILL_DIR/references"
check "scripts/ directory exists" test -d "$SKILL_DIR/scripts"
check "evals/ directory exists" test -d "$SKILL_DIR/evals"

# Content checks
check "SKILL.md has frontmatter" grep -q "^---$" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "SKILL.md has token_budget" grep -q "token_budget:" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "SKILL.md has chain" grep -q "chain:" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "SKILL.md has Use when / Handles / Do NOT use description" grep -q "Use when" "$SKILL_DIR/SKILL.md" && grep -q "Handles" "$SKILL_DIR/SKILL.md" && grep -q "Do NOT use" "$SKILL_DIR/SKILL.md"

# Section checks
check "Has Route the Request" grep -q "Route the Request" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Ground Rules" grep -q "Ground Rules" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Anti-Rationalization" grep -q "Anti-Rationalization" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Decision Trees" grep -q "Decision Trees" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Core Workflow" grep -q "Core Workflow" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Error Decoder" grep -q "Error Decoder" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Best Practices" grep -q "Best Practices" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Production Checklist" grep -q "Production Checklist" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Cross-Skill Coordination" grep -q "Cross-Skill Coordination" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Operating at Different Levels" grep -q "Operating at Different Levels" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Anti-Patterns" grep -q "Anti-Patterns" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has References" grep -q "## References" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "Has Skill Creation on Handoff" grep -q "Skill Creation on Handoff" "$SKILL_DIR/SKILL.md" 2>/dev/null

# Reference integrity: every references/*.md linked in SKILL.md must exist
check "All reference links resolve" bash -c "
  cd \"$SKILL_DIR\" && for ref in \$(grep -o '(references/[^)]*\.md)' SKILL.md | tr -d '()' | sed 's|references/||' | sort -u); do
    test -f \"references/\$ref\" || exit 1
  done"

echo ""
echo "========================================"
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
echo "========================================"

if [ $FAIL -gt 0 ]; then
    exit 1
fi
