#!/usr/bin/env bash
# Verify multi-agent-orchestration SKILL.md completeness
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
REFS_DIR="$SKILL_DIR/references"
ERRORS=0

red() { printf '\033[31m%s\033[0m\n' "$*"; }
green() { printf '\033[32m%s\033[0m\n' "$*"; }
yellow() { printf '\033[33m%s\033[0m\n' "$*"; }

check() {
    local label="$1" condition="$2"
    if eval "$condition"; then
        green "  PASS: $label"
    else
        red "  FAIL: $label"
        ERRORS=$((ERRORS + 1))
    fi
}

echo "=== Multi-Agent Orchestration Skill Verification ==="
echo ""

# 1. File existence
echo "--- File Existence ---"
check "SKILL.md exists" '[ -f "$SKILL_MD" ]'
check "verify-skill.sh exists" '[ -f "$SKILL_DIR/scripts/verify-skill.sh" ]'
check "references/ directory exists" '[ -d "$REFS_DIR" ]'

# 2. Line count
echo ""
echo "--- Line Count ---"
LINES=$(wc -l < "$SKILL_MD" | tr -d ' ')
check "SKILL.md has 600+ lines ($LINES)" '[ "$LINES" -ge 600 ]'
check "SKILL.md has <= 800 lines ($LINES)" '[ "$LINES" -le 800 ]'

# 3. Frontmatter
echo ""
echo "--- Frontmatter ---"
check "Has name: multi-agent-orchestration" 'grep -q "^name: multi-agent-orchestration" "$SKILL_MD"'
check "Has author: Sandeep Kumar Penchala" 'grep -q "^author: Sandeep Kumar Penchala" "$SKILL_MD"'
check "Has license" 'grep -q "^license:" "$SKILL_MD"'
check "Has portability target" 'grep -q "^portability:" "$SKILL_MD"'
check "Has version" 'grep -q "^version:" "$SKILL_MD"'
check "Has token_budget" 'grep -q "^token_budget:" "$SKILL_MD"'
check "Has chain consumes_from" 'grep -q "consumes_from:" "$SKILL_MD"'
check "Has chain feeds_into" 'grep -q "feeds_into:" "$SKILL_MD"'

# 4. Required sections
echo ""
echo "--- Required Sections ---"
check "Section: Problem Statement" 'grep -q "^## 1. Problem Statement" "$SKILL_MD"'
check "Section: Quick Reference" 'grep -q "^## 2. Quick Reference" "$SKILL_MD"'
check "Section: Topology Patterns" 'grep -q "^## 3. Five Agent Topology" "$SKILL_MD"'
check "Section: Typed Shared State" 'grep -q "^## 4. Typed Shared State" "$SKILL_MD"'
check "Section: Delegation Protocol" 'grep -q "^## 5. Agent Delegation" "$SKILL_MD"'
check "Section: State Sync" 'grep -q "^## 6. State Synchronization" "$SKILL_MD"'
check "Section: Conflict Resolution" 'grep -q "^## 7. Conflict Resolution" "$SKILL_MD"'
check "Section: Observability" 'grep -q "^## 8. Observability" "$SKILL_MD"'
check "Section: Failure Modes" 'grep -q "^## 9. Failure Modes" "$SKILL_MD"'
check "Section: Cost Optimization" 'grep -q "^## 10. Cost Optimization" "$SKILL_MD"'
check "Section: Decision Trees" 'grep -q "^## 11. Decision Trees" "$SKILL_MD"'
check "Section: Ground Rules" 'grep -q "^## 12. Ground Rules" "$SKILL_MD"'
check "Section: Gotchas" 'grep -q "^## 13. Gotchas" "$SKILL_MD"'
check "Section: Quick Start" 'grep -q "^## 14. Quick Start" "$SKILL_MD"'
check "Section: Anti-Rationalization" 'grep -q "^## Anti-Rationalization" "$SKILL_MD"'

# 5. Decision trees
echo ""
echo "--- Decision Trees ---"
TREE_COUNT=$(grep -c "Decision Tree\|decision tree" "$SKILL_MD" || true)
check "At least 5 decision trees ($TREE_COUNT found)" '[ "$TREE_COUNT" -ge 5 ]'

ASCII_COUNT=$(grep -c '[├└│]' "$SKILL_MD" || true)
check "ASCII tree chars present ($ASCII_COUNT occurrences)" '[ "$ASCII_COUNT" -ge 20 ]'

# 6. Gotchas
echo ""
echo "--- Gotchas ---"
GOTCHA_COUNT=$(grep -c '\$[0-9].*K+' "$SKILL_MD" || true)
check "At least 7 dollar-quantified gotchas ($GOTCHA_COUNT found)" '[ "$GOTCHA_COUNT" -ge 7 ]'

# 7. Ground rules
echo ""
echo "--- Ground Rules ---"
GR_COUNT=$(grep -c "^| [0-9]" "$SKILL_MD" || true)
check "At least 6 ground rules ($GR_COUNT found)" '[ "$GR_COUNT" -ge 6 ]'

# 8. Reference files
echo ""
echo "--- Reference Files ---"
REFS=$(find "$REFS_DIR" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
check "At least 10 reference files ($REFS found)" '[ "$REFS" -ge 10 ]'

# Check each expected reference
for ref in five-agent-topologies.md langgraph-typed-state-patterns.md \
    crewai-pydantic-task-outputs.md agent-delegation-protocol.md \
    state-synchronization-strategies.md conflict-resolution-patterns.md \
    failure-mode-prevention.md observability-multi-agent.md \
    cost-optimization-reference.md swarm-advanced-patterns.md; do
    if [ -f "$REFS_DIR/$ref" ]; then
        REF_LINES=$(wc -l < "$REFS_DIR/$ref" | tr -d ' ')
        if [ "$REF_LINES" -ge 30 ]; then
            green "  PASS: $ref ($REF_LINES lines)"
        else
            yellow "  WARN: $ref ($REF_LINES lines, expected 30+)"
        fi
    else
        red "  FAIL: $ref not found"
        ERRORS=$((ERRORS + 1))
    fi
done

# 9. Reference links resolve
echo ""
echo "--- Reference Link Resolution ---"
LINK_COUNT=$(grep -c "](references/" "$SKILL_MD" || true)
RESOLVED=0
while IFS= read -r link; do
    ref_file=$(echo "$link" | sed 's/.*](references\///' | sed 's/).*//')
    if [ -f "$REFS_DIR/$ref_file" ]; then
        RESOLVED=$((RESOLVED + 1))
    else
        red "  FAIL: Broken link → references/$ref_file"
        ERRORS=$((ERRORS + 1))
    fi
done < <(grep -o '](references/[^)]*' "$SKILL_MD")
check "All reference links resolve ($RESOLVED/$LINK_COUNT)" '[ "$RESOLVED" -eq "$LINK_COUNT" ]'

# 10. Anti-Rationalization table
echo ""
echo "--- Anti-Rationalization ---"
ANTI_COUNT=$(grep -c "| When you think" "$SKILL_MD" || true)
check "Anti-Rationalization table present ($ANTI_COUNT row headers)" '[ "$ANTI_COUNT" -ge 1 ]'
ANTI_ROWS=$(grep -c "^| \"" "$SKILL_MD" || true)
check "At least 5 rationalization rows ($ANTI_ROWS found)" '[ "$ANTI_ROWS" -ge 5 ]'

# 11. Portability
echo ""
echo "--- Portability ---"
check "Mentions Claude Code" 'grep -q "Claude Code" "$SKILL_MD"'
check "Mentions Copilot CLI" 'grep -q "Copilot CLI" "$SKILL_MD"'
check "Mentions Cursor" 'grep -q "Cursor" "$SKILL_MD"'
check "Mentions OpenClaw" 'grep -q "OpenClaw" "$SKILL_MD"'
check "Mentions Gemini CLI" 'grep -q "Gemini CLI" "$SKILL_MD"'

# 12. Code examples
echo ""
echo "--- Code Examples ---"
PY_COUNT=$(grep -c '```python' "$SKILL_MD" || true)
check "Python code blocks present ($PY_COUNT found)" '[ "$PY_COUNT" -ge 5 ]'
YAML_COUNT=$(grep -c '```yaml' "$SKILL_MD" || true)
check "YAML code blocks present ($YAML_COUNT found)" '[ "$YAML_COUNT" -ge 1 ]'

echo ""
echo "========================================="
if [ "$ERRORS" -eq 0 ]; then
    green "ALL CHECKS PASSED — Skill is complete! ✓"
    exit 0
else
    red "VERIFICATION FAILED — $ERRORS error(s) found ✗"
    exit 1
fi
