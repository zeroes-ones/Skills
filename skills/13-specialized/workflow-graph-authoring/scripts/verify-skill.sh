#!/usr/bin/env bash
# =============================================================================
# verify-skill.sh — per-skill verification harness for workflow-graph-authoring
# Mirrors the repo-standard harness (e.g. agent-handoff-protocol/scripts/verify-skill.sh):
# existence, frontmatter, required sections, guardrail phrases, quantification,
# progressive disclosure, reference links. Exit 0 = all checks pass.
# =============================================================================
set -euo pipefail

SKILL_NAME="workflow-graph-authoring"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_FILE="$SKILL_DIR/SKILL.md"
REFERENCES_DIR="$SKILL_DIR/references"
ERRORS=0

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
log_pass() { echo -e "  ${GREEN}[PASS]${NC} $1"; }
log_fail() { echo -e "  ${RED}[FAIL]${NC} $1"; ERRORS=$((ERRORS + 1)); }
log_warn() { echo -e "  ${YELLOW}[WARN]${NC} $1"; }

echo "================================================"
echo "Verifying: ${SKILL_NAME} SKILL.md"
echo "================================================"

# --- 1. Existence ---
echo ""
echo "[1] Existence checks..."
[[ -f "$SKILL_FILE" ]] && log_pass "SKILL.md exists" || log_fail "SKILL.md not found"
[[ -d "$REFERENCES_DIR" ]] && log_pass "references/ directory exists" || log_fail "references/ missing"

# --- 2. Frontmatter fields ---
echo ""
echo "[2] Frontmatter checks..."
for field in name description author license portability type status version updated tags \
             token_budget chain; do
    if grep -q "^${field}:" "$SKILL_FILE"; then
        log_pass "Frontmatter has '${field}'"
    else
        log_fail "Frontmatter missing '${field}'"
    fi
done

# --- 3. Required section headings ---
echo ""
echo "[3] Required section headings..."
REQUIRED_SECTIONS=(
    "## Route the Request" "## Ground Rules" "## The Expert's Mindset"
    "## Operating at Different Levels" "## When to Use" "## When NOT to Use"
    "## Core Workflow" "## Decision Trees" "## Error Recovery"
    "## Cross-Skill Coordination" "## Proactive Triggers" "## What Good Looks Like"
    "## Deliberate Practice" "## Gotchas" "## Anti-Hallucination" "## Anti-Patterns"
    "## Best Practices" "## Production Checklist" "## Verification" "## State Log"
    "## References" "## Anti-Rationalization"
)
for sec in "${REQUIRED_SECTIONS[@]}"; do
    if grep -q "^${sec}" "$SKILL_FILE"; then
        log_pass "Section present: ${sec}"
    else
        log_fail "Missing section: ${sec}"
    fi
done

# --- 4. Guardrail phrases + discipline markers ---
echo ""
echo "[4] Content discipline checks..."
for phrase in "Admit uncertainty" "Flag your knowledge cutoff" "Never guess security" \
              "[VERIFIED]" "Mechanical Trigger" "Violation Response" "Complete when" \
              "| Upstream Skill"; do
    if grep -qF "$phrase" "$SKILL_FILE"; then
        log_pass "Contains '${phrase}'"
    else
        log_fail "Missing '${phrase}'"
    fi
done

dollar_count=$(grep -o '\$[0-9,]\+' "$SKILL_FILE" | wc -l | tr -d ' ')
if [ "$dollar_count" -ge 5 ]; then
    log_pass "Dollar-quantified references: ${dollar_count} (>= 5)"
else
    log_fail "Dollar-quantified references: ${dollar_count} (< 5)"
fi

quick_count=$(grep -c 'QUICK' "$SKILL_FILE" || true)
if [ "$quick_count" -ge 3 ]; then
    log_pass "QUICK markers: ${quick_count} (>= 3)"
else
    log_fail "QUICK markers: ${quick_count} (< 3)"
fi

complete_when=$(grep -c 'Complete when' "$SKILL_FILE" || true)
if [ "$complete_when" -ge 8 ]; then
    log_pass "'Complete when' statements: ${complete_when} (>= 8)"
else
    log_fail "'Complete when' statements: ${complete_when} (< 8)"
fi

# --- 5. Reference links resolve ---
echo ""
echo "[5] Reference links..."
broken=0
while IFS= read -r ref; do
    [ -z "$ref" ] && continue
    if [ ! -f "$REFERENCES_DIR/$ref" ]; then
        echo "    BROKEN references/$ref"
        broken=$((broken + 1))
    fi
done < <(grep -oE '\(references/[^)]+\.md' "$SKILL_FILE" | sed 's/^.*references\///' || true)
if [ "$broken" -eq 0 ]; then
    log_pass "All reference links resolve"
else
    log_fail "${broken} broken reference link(s)"
fi

# --- 6. Summary ---
echo ""
echo "================================================"
if [ "$ERRORS" -eq 0 ]; then
    echo -e "  ${GREEN}✅ ${SKILL_NAME} verification PASSED${NC}"
else
    echo -e "  ${RED}❌ ${SKILL_NAME} verification FAILED — ${ERRORS} error(s)${NC}"
fi
echo "================================================"
exit "$ERRORS"
