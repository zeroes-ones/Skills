#!/usr/bin/env bash
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
SKILL_MD="$SKILL_DIR/SKILL.md"
REF_DIR="$SKILL_DIR/reference"

PASS=0
FAIL=0
ERRORS=()
WARNINGS=()

green() { printf '\033[0;32m%s\033[0m\n' "$1"; }
red()   { printf '\033[0;31m%s\033[0m\n' "$1"; }
yellow(){ printf '\033[0;33m%s\033[0m\n' "$1"; }
bold()  { printf '\033[1m%s\033[0m\n' "$1"; }

check() {
    local desc="$1"; shift
    local rc=0
    "$@" >/dev/null 2>&1 || rc=$?
    if [ "$rc" -eq 0 ]; then
        ((PASS++))
        green "  ✓ $desc"
    else
        ((FAIL++))
        red "  ✗ $desc"
        ERRORS+=("$desc")
    fi
}

warn() {
    local desc="$1"; shift
    local rc=0
    "$@" >/dev/null 2>&1 || rc=$?
    if [ "$rc" -eq 0 ]; then
        ((PASS++))
        green "  ✓ $desc"
    else
        yellow "  ⚠ $desc (warning)"
        WARNINGS+=("$desc")
    fi
}

echo ""
bold "═══════════════════════════════════════════════════════"
bold "  Desktop Architecture Patterns — Skill Verification"
bold "═══════════════════════════════════════════════════════"
echo ""

bold "── SKILL.md Checks ──"

check "SKILL.md exists" [ -f "$SKILL_MD" ]

SKILL_LINES=$(wc -l < "$SKILL_MD" | tr -d ' ')
check "SKILL.md is 500-600 lines (actual: $SKILL_LINES)" [ "$SKILL_LINES" -ge 500 ] && [ "$SKILL_LINES" -le 600 ]

check "SKILL.md has opening frontmatter" grep -q '^---$' "$SKILL_MD"
check "SKILL.md has name in frontmatter" grep -q 'name: desktop-architecture-patterns' "$SKILL_MD"
check "SKILL.md has description" grep -q 'description:' "$SKILL_MD"
check "SKILL.md has author" grep -q 'author: Sandeep Kumar Penchala' "$SKILL_MD"
check "SKILL.md has license" grep -q 'license: MIT' "$SKILL_MD"
check "SKILL.md has version" grep -q 'version: 1.0.0' "$SKILL_MD"
check "SKILL.md has updated date" grep -q 'updated: 2026-07-24' "$SKILL_MD"
check "SKILL.md has tags" grep -q 'tags:' "$SKILL_MD"
check "SKILL.md has token_budget" grep -q 'token_budget: 4500' "$SKILL_MD"
check "SKILL.md has consumes_from" grep -q 'consumes_from:' "$SKILL_MD"
check "SKILL.md has feeds_into" grep -q 'feeds_into:' "$SKILL_MD"
check "SKILL.md portability target" grep -q 'Portability target.*Spec-level' "$SKILL_MD"

bold "── Section Checks ──"

check "Section 1: Ground Rules" grep -q '## 1. Ground Rules' "$SKILL_MD"
check "Section 2: Decision Trees" grep -q '## 2. Decision Trees' "$SKILL_MD"
check "Section 3: Gotchas" grep -q '## 3. Gotchas' "$SKILL_MD"
check "Section 4: Anti-Rationalization" grep -q '## 4. Anti-Rationalization' "$SKILL_MD"
check "Section 5: Core Architecture Patterns" grep -q '## 5. Core Desktop Architecture Patterns' "$SKILL_MD"
check "Section 6: Multi-Window" grep -q '## 6. Multi-Window Architecture' "$SKILL_MD"
check "Section 7: IPC Architecture" grep -q '## 7. IPC Architecture' "$SKILL_MD"
check "Section 8: System Tray" grep -q '## 8. System Tray' "$SKILL_MD"
check "Section 9: Auto-Update" grep -q '## 9. Auto-Update' "$SKILL_MD"
check "Section 10: Security" grep -q '## 10. Desktop Security Architecture' "$SKILL_MD"
check "Section 11: Cross-Platform" grep -q '## 11. Cross-Platform Desktop Strategies' "$SKILL_MD"
check "Section 12: State Management" grep -q '## 12. Desktop State Management' "$SKILL_MD"
check "Section 13: Performance" grep -q '## 13. Performance Architecture' "$SKILL_MD"
check "Section 14: Installer" grep -q '## 14. Installer' "$SKILL_MD"
check "Section 15: Testing" grep -q '## 15. Testing Architecture' "$SKILL_MD"

bold "── Content Quality ──"

NONNEG=$(grep -c 'NEVER\|ALWAYS' "$SKILL_MD" 2>/dev/null || echo 0)
check "5+ non-negotiable rules (found: $NONNEG)" [ "$NONNEG" -ge 5 ]

DOLLAR=$(grep -c '\$[0-9]' "$SKILL_MD" 2>/dev/null || echo 0)
check "Dollar-quantified gotchas (found: $DOLLAR)" [ "$DOLLAR" -ge 4 ]

TREES=$(grep -c '├──\|└──' "$SKILL_MD" 2>/dev/null || echo 0)
check "Decision tree branches (found: $TREES)" [ "$TREES" -ge 10 ]

ANTI=$(grep -c '^| \*"' "$SKILL_MD" 2>/dev/null || echo 0)
check "Anti-rationalization rows (found: $ANTI)" [ "$ANTI" -ge 5 ]

check "Links to mvvm-patterns" grep -q 'desktop-mvvm-patterns.md' "$SKILL_MD"
check "Links to multi-window" grep -q 'multi-window-architecture.md' "$SKILL_MD"
check "Links to ipc-architecture" grep -q 'desktop-ipc-architecture.md' "$SKILL_MD"
check "Links to system-tray" grep -q 'system-tray-background-services.md' "$SKILL_MD"
check "Links to auto-update" grep -q 'desktop-auto-update-patterns.md' "$SKILL_MD"
check "Links to state-management" grep -q 'desktop-state-management.md' "$SKILL_MD"
check "Links to cross-platform" grep -q 'cross-platform-desktop-strategies.md' "$SKILL_MD"
check "Links to security" grep -q 'desktop-security-architecture.md' "$SKILL_MD"

bold "── Reference Files ──"

for f in \
    desktop-mvvm-patterns.md \
    multi-window-architecture.md \
    desktop-ipc-architecture.md \
    system-tray-background-services.md \
    desktop-auto-update-patterns.md \
    desktop-state-management.md \
    cross-platform-desktop-strategies.md \
    desktop-security-architecture.md
do
    ref="$REF_DIR/$f"
    check "exists: $f" [ -f "$ref" ]
    if [ -f "$ref" ]; then
        lines=$(wc -l < "$ref" | tr -d ' ')
        check "$f: 200+ lines ($lines)" [ "$lines" -ge 200 ]
        check "$f: <=400 lines ($lines)" [ "$lines" -le 400 ]
        check "$f: has headings" grep -q '^#' "$ref"
        warn "$f: has code blocks" grep -q '```' "$ref"
    fi
done

bold "── Self Check ──"
check "verify-skill.sh exists" [ -f "$SCRIPT_DIR/verify-skill.sh" ]
check "verify-skill.sh is executable" [ -x "$SCRIPT_DIR/verify-skill.sh" ]

echo ""
bold "═══════════════════════════════════════════════════════"
bold "  Summary"
bold "═══════════════════════════════════════════════════════"
echo ""
green "  Passed:  $PASS"
[ "$FAIL" -gt 0 ] && red "  Failed:  $FAIL" || green "  Failed:  $FAIL"
[ "${#WARNINGS[@]}" -gt 0 ] && yellow "  Warnings: ${#WARNINGS[@]}"
echo ""

if [ "${#ERRORS[@]}" -gt 0 ]; then
    red "Failed checks:"
    for e in "${ERRORS[@]}"; do red "  ✗ $e"; done
    echo ""
fi
if [ "${#WARNINGS[@]}" -gt 0 ]; then
    yellow "Warnings:"
    for w in "${WARNINGS[@]}"; do yellow "  ⚠ $w"; done
    echo ""
fi

if [ "$FAIL" -eq 0 ]; then
    green "✓ All checks passed!"
    echo ""
    exit 0
else
    red "✗ $FAIL check(s) failed."
    echo ""
    exit 1
fi
