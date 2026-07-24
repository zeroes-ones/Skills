#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_FILE="$SKILL_DIR/SKILL.md"
REFERENCES_DIR="$SKILL_DIR/references"
PASS=0
FAIL=0

check() {
    local desc="$1"
    if eval "$2"; then
        echo "  ✓ $desc"
        PASS=$((PASS + 1))
    else
        echo "  ✗ $desc"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== MCP Management Skill Verification ==="
echo "Skill directory: $SKILL_DIR"
echo ""

# --- File existence ---
echo "[File Structure]"
check "SKILL.md exists" '[ -f "$SKILL_FILE" ]'
check "references/ directory exists" '[ -d "$REFERENCES_DIR" ]'
check "scripts/ directory exists" '[ -d "$SKILL_DIR/scripts" ]'

# --- Frontmatter ---
echo ""
echo "[Frontmatter]"
check "name field present" 'grep -q "^name: mcp-management" "$SKILL_FILE"'
check "description field present" 'grep -q "^description:" "$SKILL_FILE"'
check "author field present" 'grep -q "^author: Sandeep Kumar Penchala" "$SKILL_FILE"'
check "license field present" 'grep -q "^license:" "$SKILL_FILE"'
check "portability field present" 'grep -q "^portability:" "$SKILL_FILE"'
check "type field present" 'grep -q "^type:" "$SKILL_FILE"'
check "status field present" 'grep -q "^status:" "$SKILL_FILE"'
check "version field present" 'grep -q "^version:" "$SKILL_FILE"'
check "updated field present" 'grep -q "^updated:" "$SKILL_FILE"'
check "tags field present" 'grep -q "^tags:" "$SKILL_FILE"'
check "token_budget field present" 'grep -q "^token_budget:" "$SKILL_FILE"'
check "chain section present" 'grep -q "^chain:" "$SKILL_FILE"'
check "consumes_from present" 'grep -q "consumes_from:" "$SKILL_FILE"'
check "feeds_into present" 'grep -q "feeds_into:" "$SKILL_FILE"'

# --- Required headings ---
echo ""
echo "[Required Headings]"
check "## Route the Request" 'grep -q "^## Route the Request" "$SKILL_FILE"'
check "## Ground Rules" 'grep -q "^## Ground Rules" "$SKILL_FILE"'
check "## The Expert'\''s Mindset" 'grep -q "^## The Expert'\''s Mindset" "$SKILL_FILE"'
check "## Operating at Different Levels" 'grep -q "^## Operating at Different Levels" "$SKILL_FILE"'
check "## When to Use" 'grep -q "^## When to Use" "$SKILL_FILE"'
check "## Core Workflow" 'grep -q "^## Core Workflow" "$SKILL_FILE"'
check "## Decision Trees" 'grep -q "^## Decision Trees" "$SKILL_FILE"'
check "## Cross-Skill Coordination" 'grep -q "^## Cross-Skill Coordination" "$SKILL_FILE"'
check "## Proactive Triggers" 'grep -q "^## Proactive Triggers" "$SKILL_FILE"'
check "## What Good Looks Like" 'grep -q "^## What Good Looks Like" "$SKILL_FILE"'
check "## Deliberate Practice" 'grep -q "^## Deliberate Practice" "$SKILL_FILE"'
check "## Gotchas" 'grep -q "^## Gotchas" "$SKILL_FILE"'
check "## Verification" 'grep -q "^## Verification" "$SKILL_FILE"'
check "## References" 'grep -q "^## References" "$SKILL_FILE"'
check "## Anti-Rationalization" 'grep -q "^## Anti-Rationalization" "$SKILL_FILE"'

# --- Content quality checks ---
echo ""
echo "[Content Quality]"
check "Portability target line present" 'grep -q "Portability target:" "$SKILL_FILE"'
check "Mechanical Trigger phrase appears (Ground Rules)" 'grep -q "Mechanical Trigger:" "$SKILL_FILE"'
check "Violation Response phrase appears (Ground Rules)" 'grep -q "Violation Response:" "$SKILL_FILE"'
check "At least 7 ground rules" 'test $(grep -c "^[0-9]\+\. \*\*Mechanical Trigger" "$SKILL_FILE") -ge 7'
check "L1-L5 operating levels" 'grep -q "L1" "$SKILL_FILE" && grep -q "L5" "$SKILL_FILE"'
check "At least 5 decision trees" 'test $(grep -c "^### Decision Tree" "$SKILL_FILE") -ge 5'
check "Dollar-quantified gotchas" 'grep -q "\\$[0-9]" "$SKILL_FILE"'
check "At least 5 dollar-quantified gotchas" 'test $(grep -cF "$" "$SKILL_FILE") -ge 5'
check "MCP spec reference (JSON-RPC 2.0)" 'grep -q "JSON-RPC 2.0" "$SKILL_FILE"'

# --- Reference files ---
echo ""
echo "[Reference Files]"
check "mcp-transport-configs.md" '[ -f "$REFERENCES_DIR/mcp-transport-configs.md" ]'
check "mcp-security-hardening.md" '[ -f "$REFERENCES_DIR/mcp-security-hardening.md" ]'
check "mcp-server-types.md" '[ -f "$REFERENCES_DIR/mcp-server-types.md" ]'
check "mcp-config-schema.md" '[ -f "$REFERENCES_DIR/mcp-config-schema.md" ]'
check "multi-server-routing.md" '[ -f "$REFERENCES_DIR/multi-server-routing.md" ]'
check "mcp-diagnostics.md" '[ -f "$REFERENCES_DIR/mcp-diagnostics.md" ]'
check "claude-code-mcp-integration.md" '[ -f "$REFERENCES_DIR/claude-code-mcp-integration.md" ]'
check "cross-agent-mcp-patterns.md" '[ -f "$REFERENCES_DIR/cross-agent-mcp-patterns.md" ]'

# --- Line count estimates ---
echo ""
echo "[Sizes]"
SKILL_LINES=$(wc -l < "$SKILL_FILE" | tr -d ' ')
echo "  SKILL.md: $SKILL_LINES lines"
for ref in "$REFERENCES_DIR"/*.md; do
    ref_lines=$(wc -l < "$ref" | tr -d ' ')
    ref_name=$(basename "$ref")
    echo "  $ref_name: $ref_lines lines"
done

# --- Summary ---
echo ""
echo "========================================="
echo "Verification complete: $PASS passed, $FAIL failed"
echo "========================================="

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
