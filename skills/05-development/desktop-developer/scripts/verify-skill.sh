#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
ERRORS=0
WARNINGS=0

green()  { printf '\033[0;32m%s\033[0m\n' "$1"; }
red()    { printf '\033[0;31m%s\033[0m\n' "$1"; ERRORS=$((ERRORS + 1)); }
yellow() { printf '\033[0;33m%s\033[0m\n' "$1"; WARNINGS=$((WARNINGS + 1)); }

echo "=== Desktop Developer Skill Verification ==="
echo ""

# 1. SKILL.md exists and has minimum line count
if [ ! -f "$SKILL_MD" ]; then
    red "❌ SKILL.md not found at $SKILL_MD"
    exit 1
fi

LINES=$(wc -l < "$SKILL_MD" | tr -d ' ')
if [ "$LINES" -lt 600 ]; then
    red "❌ SKILL.md is $LINES lines (need >= 600)"
else
    green "✓ SKILL.md: $LINES lines"
fi

# 2. Frontmatter required fields
for field in "name:" "description:" "author:" "license:" "portability:" "type:" "status:" "version:" "updated:" "tags:" "token_budget:" "chain:"; do
    if grep -q "^$field" "$SKILL_MD"; then
        green "✓ Frontmatter: $field present"
    else
        red "❌ Missing frontmatter field: $field"
    fi
done

# 3. Required sections
for section in \
    "Portability Target" \
    "Route the Request" \
    "Ground Rules" \
    "The Expert.s Mindset" \
    "Operating at Different Levels" \
    "When to Use" \
    "Decision Trees" \
    "Core Workflow" \
    "Cross-Skill Coordination" \
    "Proactive Triggers" \
    "What Good Looks Like" \
    "Deliberate Practice" \
    "Gotchas" \
    "Verification" \
    "Anti-Rationalization" \
    "References" \
    "Scale Depth" \
    "Production Checklist"; do
    if grep -q "## $section" "$SKILL_MD"; then
        green "✓ Section: $section"
    else
        red "❌ Missing section: $section"
    fi
done

# 4. Code snippets present
for lang in "typescript" "rust" "csharp" "json" "xml" "bash"; do
    if grep -q "\`\`\`$lang" "$SKILL_MD"; then
        green "✓ Code block: $lang"
    else
        yellow "⚠ No $lang code block found"
    fi
done

# 5. ASCII decision trees (> 3)
TREE_COUNT=$(grep -c '├──\|└──' "$SKILL_MD" || true)
if [ "$TREE_COUNT" -gt 15 ]; then
    green "✓ Decision trees: $TREE_COUNT branch lines"
else
    yellow "⚠ Only $TREE_COUNT decision tree branch lines (expect > 15)"
fi

# 6. Reference files exist
REFS=(
    "references/electron-architecture-patterns.md"
    "references/tauri-security-model.md"
    "references/desktop-ipc-patterns.md"
    "references/auto-update-strategies.md"
    "references/desktop-installer-packaging.md"
    "references/native-module-integration.md"
    "references/desktop-window-management.md"
    "references/cross-platform-testing.md"
)

for ref in "${REFS[@]}"; do
    REF_PATH="$SKILL_DIR/$ref"
    if [ -f "$REF_PATH" ]; then
        REF_LINES=$(wc -l < "$REF_PATH" | tr -d ' ')
        if [ "$REF_LINES" -ge 20 ]; then
            green "✓ Reference: $ref ($REF_LINES lines)"
        else
            yellow "⚠ Reference short: $ref ($REF_LINES lines, expect >= 20)"
        fi
    else
        red "❌ Missing reference: $ref"
    fi
done

# 7. Gotchas count >= 7
GOTCHA_COUNT=$(grep -c '^| [0-9]' <(sed -n '/^## Gotchas/,/^## Verification/p' "$SKILL_MD") || true)
if [ "$GOTCHA_COUNT" -ge 7 ]; then
    green "✓ Gotchas: $GOTCHA_COUNT entries (>= 7)"
else
    red "❌ Gotchas: only $GOTCHA_COUNT entries (need >= 7)"
fi

# 8. Production checklist >= 12
CHECKLIST_COUNT=$(grep -c '^- \[' <(sed -n '/^## Production Checklist/,$p' "$SKILL_MD") || true)
if [ "$CHECKLIST_COUNT" -ge 12 ]; then
    green "✓ Production Checklist: $CHECKLIST_COUNT items (>= 12)"
else
    red "❌ Production Checklist: only $CHECKLIST_COUNT items (need >= 12)"
fi

# 9. Ground Rules: nodeIntegration check (critical security)
if grep -q "NEVER enable.*nodeIntegration.*true" "$SKILL_MD"; then
    green "✓ Ground Rule: nodeIntegration security rule present"
else
    red "❌ Missing: nodeIntegration security ground rule"
fi

echo ""
echo "=== Summary ==="
echo "Errors:   $ERRORS"
echo "Warnings: $WARNINGS"

if [ "$ERRORS" -gt 0 ]; then
    echo "❌ VERIFICATION FAILED"
    exit 1
else
    echo "✓ VERIFICATION PASSED"
    exit 0
fi
