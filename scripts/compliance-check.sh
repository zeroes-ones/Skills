#!/usr/bin/env bash
# =============================================================================
# Executable Compliance Scripts — extract Anti-Pattern triggers into
# grep-based lint rules that can be run against codebases.
#
# Usage:
#   ./scripts/compliance-check.sh                    # All categories
#   ./scripts/compliance-check.sh --category dev      # Development skills only
#   ./scripts/compliance-check.sh --target repos/myrepo  # Scan target codebase
#
# This extracts anti-pattern descriptions from SKILL.md files and converts
# them into machine-readable grep patterns for automated compliance checking.
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

CATEGORY=""
TARGET=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --category) CATEGORY="$2"; shift 2 ;;
        --target) TARGET="$2"; shift 2 ;;
        *) echo "Unknown: $1"; exit 1 ;;
    esac
done

# ---------------------------------------------------------------------------
# Pattern Library — extracted from Anti-Patterns sections across skills
# ---------------------------------------------------------------------------
# Format: "pattern_name|grep_regex|severity|category"
# These are derived from the negative constraints in each skill's description
# and Anti-Patterns sections.

# Pattern registry stored as parallel arrays (bash 3.x compatible)
PATTERN_NAMES=()
PATTERN_REGEX=()
PATTERN_SEVERITY=()
PATTERN_CATEGORY=()

_register_pattern() {
    PATTERN_NAMES+=("$1")
    PATTERN_REGEX+=("$2")
    PATTERN_SEVERITY+=("$3")
    PATTERN_CATEGORY+=("$4")
}

# --- Security Anti-Patterns ---
_register_pattern "plaintext-secrets" "(password|secret|api_key|token)[[:space:]]*=[[:space:]]*['\"][^'\"]{8,}['\"]" "CRITICAL" "security"
_register_pattern "unsafe-deserialization" "pickle\.loads|yaml\.load\(|eval\(|exec\(" "CRITICAL" "security"
_register_pattern "raw-sql-concatenation" "SELECT.*\+|\\$\{.*SELECT" "HIGH" "security"

# ---------------------------------------------------------------------------
# Scan target directory (or validate skill definitions only)
# ---------------------------------------------------------------------------

if [[ -z "$TARGET" ]]; then
    echo "=== Compliance: Skill Definition Audit ==="
    echo "Scanning SKILL.md files for anti-pattern definitions..."
    echo ""

    total_skills=0
    skills_with_anti_patterns=0
    skills_with_gotchas=0

    for skill in "$SKILLS_DIR"/*/*/SKILL.md; do
        skill_dir=$(dirname "$skill")
        skill_name=$(basename "$skill_dir")
        total_skills=$((total_skills + 1))

        has_anti=0
        has_gotchas=0
        grep -q "^## Anti-Patterns" "$skill" && has_anti=1 || true
        grep -q "^## Gotchas" "$skill" && has_gotchas=1 || true

        if [[ $has_anti -eq 1 ]]; then
            skills_with_anti_patterns=$((skills_with_anti_patterns + 1))
            count=$(grep -c "^- \*\*" "$skill" 2>/dev/null || echo 0)
            echo -e "  ${GREEN}[$skill_name]${NC} $count anti-patterns"
        fi
        if [[ $has_gotchas -eq 1 ]]; then
            skills_with_gotchas=$((skills_with_gotchas + 1))
        fi

        # Report skills missing BOTH
        if [[ $has_anti -eq 0 && $has_gotchas -eq 0 ]]; then
            echo -e "  ${YELLOW}[$skill_name]${NC} MISSING: no Anti-Patterns or Gotchas section"
        fi
    done

    echo ""
    echo "--- Summary ---"
    echo -e "Total skills:                    $total_skills"
    echo -e "With Anti-Patterns section:      ${GREEN}$skills_with_anti_patterns${NC}"
    echo -e "With Gotchas section:            ${GREEN}$skills_with_gotchas${NC}"
    skills_missing=$((total_skills - skills_with_anti_patterns - skills_with_gotchas))
    if [[ $skills_with_anti_patterns -gt 0 && $skills_with_gotchas -gt 0 ]]; then
        # Skills with both are double-counted; count unique
        skills_with_either=$(grep -rl "^## Anti-Patterns\|^## Gotchas" "$SKILLS_DIR"/*/*/SKILL.md 2>/dev/null | sort -u | wc -l | tr -d ' ')
        skills_missing=$((total_skills - skills_with_either))
    fi
    echo -e "Missing defensive sections:      ${YELLOW}$skills_missing${NC}"

    if [[ $skills_missing -eq 0 ]]; then
        echo -e "${GREEN}All skills have defensive sections (Anti-Patterns or Gotchas).${NC}"
    fi

else
    # --- Target mode: run anti-pattern checks against a codebase ---
    echo "=== Compliance: Codebase Scan ==="
    echo "Target: $TARGET"
    echo ""

    if [[ ! -d "$TARGET" ]]; then
        echo "ERROR: Target directory not found: $TARGET"
        exit 1
    fi

    findings=0
    total_checks=${#PATTERN_NAMES[@]}

    for ((i=0; i<${#PATTERN_NAMES[@]}; i++)); do
        pattern_name="${PATTERN_NAMES[$i]}"
        regex="${PATTERN_REGEX[$i]}"
        severity="${PATTERN_SEVERITY[$i]}"

        matches=$(grep -rnE "$regex" "$TARGET" --include='*.py' --include='*.js' --include='*.ts' --include='*.jsx' --include='*.tsx' --include='*.go' 2>/dev/null | head -20 || true)

        if [[ -n "$matches" ]]; then
            findings=$((findings + 1))
            echo -e "  ${RED}[$severity] $pattern_name${NC}"
            echo "$matches" | while read line; do echo "    $line"; done
            echo ""
        fi
    done

    echo "--- Scan Summary ---"
    echo "Checks run:  $total_checks"
    echo -e "Findings:    ${RED}$findings${NC}"
    if [[ $findings -gt 0 ]]; then
        echo -e "${RED}FAIL: $findings anti-pattern(s) detected.${NC}"
        exit 1
    else
        echo -e "${GREEN}PASS: No anti-patterns detected.${NC}"
    fi
fi
