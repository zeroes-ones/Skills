#!/usr/bin/env bash
set -uo pipefail

# verify-skill.sh — Validation script for applying-llm-guardrails skill
# Run from: skills/23-trust-safety/applying-llm-guardrails/

SKILL_FILE="SKILL.md"
REF_DIR="references"
PASS=0
FAIL=0
WARN=0

green()  { echo -e "\033[32m[PASS]\033[0m $*"; ((PASS += 1)); }
red()    { echo -e "\033[31m[FAIL]\033[0m $*"; ((FAIL += 1)); }
yellow() { echo -e "\033[33m[WARN]\033[0m $*"; ((WARN += 1)); }

echo "============================================"
echo " Verifying: applying-llm-guardrails skill"
echo "============================================"
echo ""

# ─────────────────────────────────────────────────
# 1. File existence
# ─────────────────────────────────────────────────
echo "--- File Existence ---"

if [[ -f "$SKILL_FILE" ]]; then
    green "SKILL.md exists"
else
    red "SKILL.md missing"
fi

if [[ -d "$REF_DIR" ]]; then
    green "references/ directory exists"
else
    red "references/ directory missing"
fi

# ─────────────────────────────────────────────────
# 2. Frontmatter validation
# ─────────────────────────────────────────────────
echo ""
echo "--- Frontmatter ---"

FRONTMATTER=$(head -50 "$SKILL_FILE")

if echo "$FRONTMATTER" | grep -q "^---$"; then
    green "Frontmatter opening delimiter present"
else
    red "Frontmatter opening delimiter missing"
fi

if echo "$FRONTMATTER" | grep -q "^name: applying-llm-guardrails"; then
    green "name: applying-llm-guardrails"
else
    red "name field incorrect or missing"
fi

if echo "$FRONTMATTER" | grep -q "^author: Sandeep Kumar Penchala"; then
    green "author: Sandeep Kumar Penchala"
else
    red "author field incorrect or missing"
fi

if echo "$FRONTMATTER" | grep -q "^portability:"; then
    green "portability field present"
else
    red "portability field missing"
fi

if echo "$FRONTMATTER" | grep -q "^type: security"; then
    green "type: security"
else
    red "type field incorrect or missing"
fi

if echo "$FRONTMATTER" | grep -q "^token_budget:"; then
    green "token_budget field present"
else
    red "token_budget field missing"
fi

if echo "$FRONTMATTER" | grep -q "consumes_from:"; then
    green "chain.consumes_from present"
else
    red "chain.consumes_from missing"
fi

if echo "$FRONTMATTER" | grep -q "feeds_into:"; then
    green "chain.feeds_into present"
else
    red "chain.feeds_into missing"
fi

# ─────────────────────────────────────────────────
# 3. Required section headings
# ─────────────────────────────────────────────────
echo ""
echo "--- Required Sections (14 + Anti-Rationalization) ---"

declare -a REQUIRED_SECTIONS=(
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
    "## Anti-Rationalization"
)

for section in "${REQUIRED_SECTIONS[@]}"; do
    if grep -Fq "$section" "$SKILL_FILE"; then
        green "Section: $section"
    else
        red "MISSING section: $section"
    fi
done

# ─────────────────────────────────────────────────
# 4. Portability target line at end
# ─────────────────────────────────────────────────
echo ""
echo "--- Portability Target ---"

if tail -5 "$SKILL_FILE" | grep -q "Portability.*works with"; then
    green "Portability target line at file end"
else
    yellow "Portability target line not in last 5 lines"
fi

# ─────────────────────────────────────────────────
# 5. Ground Rules count (minimum 7)
# ─────────────────────────────────────────────────
echo ""
echo "--- Ground Rules Count ---"

GROUND_RULES=$(grep -c "^[0-9]\+\. \*\*[A-Z]" "$SKILL_FILE" || true)
if [[ "$GROUND_RULES" -ge 7 ]]; then
    green "Ground rules: $GROUND_RULES (minimum 7)"
elif [[ "$GROUND_RULES" -ge 1 ]]; then
    yellow "Ground rules: $GROUND_RULES (under 7)"
else
    red "No ground rules found"
fi

# ─────────────────────────────────────────────────
# 6. Decision Trees (minimum 5)
# ─────────────────────────────────────────────────
echo ""
echo "--- Decision Trees ---"

# Count ASCII trees by counting "├─" or "└─" patterns in code blocks
TREE_COUNT=$(grep -c "### [0-9]\+\. " "$SKILL_FILE" || true)
if [[ "$TREE_COUNT" -ge 5 ]]; then
    green "Decision trees: $TREE_COUNT (minimum 5)"
elif [[ "$TREE_COUNT" -ge 1 ]]; then
    yellow "Decision trees: $TREE_COUNT (under 5)"
else
    red "No decision trees found"
fi

# ─────────────────────────────────────────────────
# 7. Gotchas count (minimum 5)
# ─────────────────────────────────────────────────
echo ""
echo "--- Gotchas Count ---"

GOTCHA_COUNT=$(grep -c "| \*\*.*\*\* — " "$SKILL_FILE" || true)
GOTCHA_COUNT2=$(grep -c "| \*\*.*\*\* " "$SKILL_FILE" || true)
GOTCHA_COUNT=$((GOTCHA_COUNT + GOTCHA_COUNT2))
if [[ "$GOTCHA_COUNT" -ge 5 ]]; then
    green "Gotchas: $GOTCHA_COUNT (minimum 5)"
elif [[ "$GOTCHA_COUNT" -ge 1 ]]; then
    yellow "Gotchas: $GOTCHA_COUNT (under 5)"
else
    red "No gotchas found"
fi

# ─────────────────────────────────────────────────
# 8. Reference files (minimum 8)
# ─────────────────────────────────────────────────
echo ""
echo "--- Reference Files ---"

declare -a EXPECTED_REFS=(
    "llama-guard-3-implementation.md"
    "prompt-guard-deployment.md"
    "nemo-guardrails-config.md"
    "guardrails-ai-patterns.md"
    "presidio-pii-detection.md"
    "four-layer-defense-model.md"
    "guard-model-collapse.md"
    "production-guardrail-metrics.md"
)

ref_count=0
for ref in "${EXPECTED_REFS[@]}"; do
    if [[ -f "$REF_DIR/$ref" ]]; then
        lines=$(wc -l < "$REF_DIR/$ref" | tr -d ' ')
        if [[ "$lines" -ge 30 ]]; then
            green "Reference: $ref ($lines lines)"
            ((ref_count += 1))
        else
            yellow "Reference: $ref ($lines lines — under 30)"
            ((ref_count += 1))
        fi
    else
        red "MISSING reference: $ref"
    fi
done

echo ""
if [[ "$ref_count" -ge 8 ]]; then
    green "Reference files: $ref_count (minimum 8)"
elif [[ "$ref_count" -ge 1 ]]; then
    yellow "Reference files: $ref_count (under 8)"
else
    red "No reference files found"
fi

# ─────────────────────────────────────────────────
# 9. Total SKILL.md line count
# ─────────────────────────────────────────────────
echo ""
echo "--- Line Count ---"

SKILL_LINES=$(wc -l < "$SKILL_FILE" | tr -d ' ')
if [[ "$SKILL_LINES" -ge 650 ]]; then
    green "SKILL.md: $SKILL_LINES lines (target 650-750)"
elif [[ "$SKILL_LINES" -ge 500 ]]; then
    yellow "SKILL.md: $SKILL_LINES lines (below 650 target)"
else
    red "SKILL.md: $SKILL_LINES lines (significantly below target)"
fi

# ─────────────────────────────────────────────────
# 10. Anti-Rationalization table (minimum 5 rows)
# ─────────────────────────────────────────────────
echo ""
echo "--- Anti-Rationalization ---"

ANTI_ROWS=$(grep -c "^| \*\*.*\*\* |" "$SKILL_FILE" || true)
if [[ "$ANTI_ROWS" -ge 5 ]]; then
    green "Anti-rationalization rows: $ANTI_ROWS (minimum 5)"
elif [[ "$ANTI_ROWS" -ge 1 ]]; then
    yellow "Anti-rationalization rows: $ANTI_ROWS (under 5)"
else
    red "No anti-rationalization rows found"
fi

# ─────────────────────────────────────────────────
# 11. Code blocks check
# ─────────────────────────────────────────────────
echo ""
echo "--- Code Blocks ---"

CODE_BLOCKS=$(grep -c '```' "$SKILL_FILE" || true)
CODE_BLOCKS=$((CODE_BLOCKS / 2))  # Each block has opening + closing
if [[ "$CODE_BLOCKS" -ge 3 ]]; then
    green "Code blocks: $CODE_BLOCKS"
elif [[ "$CODE_BLOCKS" -ge 1 ]]; then
    yellow "Code blocks: $CODE_BLOCKS (light on implementation)"
else
    yellow "No code blocks found"
fi

# ─────────────────────────────────────────────────
# 12. Proactive triggers (minimum 5)
# ─────────────────────────────────────────────────
echo ""
echo "--- Proactive Triggers ---"

TRIGGER_COUNT=$(grep -c "^| \*\*.*\*\* |" "$SKILL_FILE" || true)
if [[ "$TRIGGER_COUNT" -ge 5 ]]; then
    green "Proactive triggers: $TRIGGER_COUNT (minimum 5)"
else
    yellow "Proactive triggers: $TRIGGER_COUNT"
fi

# ─────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────
echo ""
echo "============================================"
echo " VERIFICATION COMPLETE"
echo "============================================"
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
echo "  WARN: $WARN"
echo ""

if [[ "$FAIL" -gt 0 ]]; then
    echo "❌ Verification FAILED — $FAIL issue(s) need fixing"
    exit 1
elif [[ "$WARN" -gt 0 ]]; then
    echo "⚠️  Verification PASSED with $WARN warning(s)"
    exit 0
else
    echo "✅ Verification PASSED — all checks green"
    exit 0
fi
