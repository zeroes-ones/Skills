#!/usr/bin/env bash
set -euo pipefail
# ==============================================================================
# lint.sh — Master Lint Runner for Skills Repository
# ==============================================================================
# Orchestrates all four linters (markdown, YAML, shell, file format) with
# consistent CLI interface. Zero external dependencies beyond Python 3.
#
# Usage:
#   ./scripts/lint.sh                          # Lint all changed files
#   ./scripts/lint.sh --all                    # Lint entire repo
#   ./scripts/lint.sh --changed                # Lint git-changed files only
#   ./scripts/lint.sh skills/07-devops/automation-engineer/SKILL.md  # Specific files
#   ./scripts/lint.sh --category markdown      # Only markdown lints
#   ./scripts/lint.sh --category yaml,shell    # Only YAML + shell lints
#   ./scripts/lint.sh --fix                    # Auto-fix formatting issues
#   ./scripts/lint.sh --json                   # Machine-readable JSON output
#   ./scripts/lint.sh --errors-only            # Only show errors, not warnings
#   ./scripts/lint.sh --ci                     # CI mode: --all --errors-only --json
#
# Exit codes: 0=clean, 1=errors found, 2=linter crashed
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── Configuration ──────────────────────────────────────────────────────────
CATEGORIES=("markdown" "yaml" "shell" "files" "template")
ALL_FLAG=false
CHANGED_FLAG=false
FIX_FLAG=false
JSON_FLAG=false
ERRORS_ONLY_FLAG=false
CI_FLAG=false
SELECTED_CATEGORIES=()
POSITIONAL_ARGS=()

# ── Color Setup ────────────────────────────────────────────────────────────
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BOLD='\033[1m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' BOLD='' NC=''
fi

# ── Parse Arguments ────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --all|-a)
            ALL_FLAG=true
            shift ;;
        --changed|-c)
            CHANGED_FLAG=true
            shift ;;
        --fix|-f)
            FIX_FLAG=true
            shift ;;
        --json|-j)
            JSON_FLAG=true
            shift ;;
        --errors-only|-e)
            ERRORS_ONLY_FLAG=true
            shift ;;
        --ci)
            CI_FLAG=true
            ALL_FLAG=true
            ERRORS_ONLY_FLAG=true
            JSON_FLAG=true
            shift ;;
        --category)
            IFS=',' read -ra cats <<< "$2"
            for cat in "${cats[@]}"; do
                cat=$(echo "$cat" | xargs)
                if [[ " ${CATEGORIES[*]} " =~ " ${cat} " ]]; then
                    SELECTED_CATEGORIES+=("$cat")
                else
                    echo -e "${RED}Unknown category: $cat${NC}" >&2
                    echo "Valid categories: ${CATEGORIES[*]}" >&2
                    exit 2
                fi
            done
            shift 2 ;;
        --help|-h)
            echo "Usage: lint.sh [OPTIONS] [FILES...]"
            echo ""
            echo "Options:"
            echo "  --all, -a         Lint entire repository"
            echo "  --changed, -c     Lint git-changed files only"
            echo "  --fix, -f         Auto-fix formatting where possible"
            echo "  --json, -j        Machine-readable JSON output"
            echo "  --errors-only, -e Only show errors (not warnings)"
            echo "  --ci              CI mode (equivalent to --all --errors-only --json)"
            echo "  --category CATS   Comma-separated categories: markdown,yaml,shell,files"
            echo "  --help, -h        Show this help"
            echo ""
            echo "Lint Categories:"
            echo "  markdown  — Heading consistency, whitespace, code blocks, URLs (MD001-MD051)"
            echo "  yaml      — Frontmatter validation, description length, chain references (YML001-YML010)"
            echo "  shell     — Shebang, strict mode, quoting, best practices (SHL001-SHL010)"
            echo "  files     — UTF-8 encoding, line endings, trailing whitespace (FMT001-FMT007)"
            echo ""
            echo "Examples:"
            echo "  ./scripts/lint.sh --all                    # Full repo lint"
            echo "  ./scripts/lint.sh --changed --category yaml # YAML lint on changes"
            echo "  ./scripts/lint.sh --fix                     # Auto-fix formatting"
            echo "  ./scripts/lint.sh skills/07-devops/automation-engineer/SKILL.md"
            exit 0 ;;
        --*)
            echo -e "${RED}Unknown option: $1${NC}" >&2
            echo "Use --help for usage." >&2
            exit 2 ;;
        *)
            POSITIONAL_ARGS+=("$1")
            shift ;;
    esac
done

# ── Determine categories to run ────────────────────────────────────────────
if [[ ${#SELECTED_CATEGORIES[@]} -eq 0 ]]; then
    SELECTED_CATEGORIES=("${CATEGORIES[@]}")
fi

# ── Build common flags ─────────────────────────────────────────────────────
COMMON_FLAGS=()
if $JSON_FLAG; then
    COMMON_FLAGS+=("--json")
fi
if $ERRORS_ONLY_FLAG; then
    COMMON_FLAGS+=("--errors-only")
fi
if ! $JSON_FLAG && [[ ! -t 1 ]]; then
    COMMON_FLAGS+=("--no-color")
fi

# ── Determine scope ────────────────────────────────────────────────────────
SCOPE_FLAGS=()
if $ALL_FLAG; then
    SCOPE_FLAGS+=("--all")
elif $CHANGED_FLAG; then
    SCOPE_FLAGS+=("--changed")
fi

# If positional args provided, pass them directly (override scope)
if [[ ${#POSITIONAL_ARGS[@]} -gt 0 ]]; then
    SCOPE_FLAGS=("${POSITIONAL_ARGS[@]}")
fi

# ── Header ─────────────────────────────────────────────────────────────────
if ! $JSON_FLAG; then
    echo ""
    echo -e "${BOLD}━━━ Lint Suite ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "  Categories: ${SELECTED_CATEGORIES[*]}"
    if $ALL_FLAG; then
        echo "  Scope:      entire repository"
    elif $CHANGED_FLAG; then
        echo "  Scope:      git-changed files"
    elif [[ ${#POSITIONAL_ARGS[@]} -gt 0 ]]; then
        echo "  Scope:      ${#POSITIONAL_ARGS[@]} specified file(s)"
    fi
    if $FIX_FLAG; then
        echo -e "  Mode:       ${GREEN}--fix (auto-correct)${NC}"
    fi
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
fi

# ── Run Linters ────────────────────────────────────────────────────────────
OVERALL_EXIT=0
declare -A RESULTS

for category in "${SELECTED_CATEGORIES[@]}"; do
    linter_script="$SCRIPT_DIR/lib/lint-${category}.py"

    if [[ ! -f "$linter_script" ]]; then
        echo -e "${RED}[SKIP]${NC} Linter not found: $linter_script" >&2
        continue
    fi

    if ! $JSON_FLAG; then
        echo -e "${BOLD}[${category}]${NC}"
    fi

    # Build command
    cmd=(python3 "$linter_script" "${SCOPE_FLAGS[@]}" "${COMMON_FLAGS[@]}")

    if $FIX_FLAG && [[ "$category" == "files" ]]; then
        cmd+=(--fix)
    fi

    # Run linter
    set +e
    output=$("${cmd[@]}" 2>&1)
    exit_code=$?
    set -e

    if ! $JSON_FLAG; then
        echo "$output"
        echo ""
    fi

    RESULTS[$category]=$exit_code
    if [[ $exit_code -ne 0 ]]; then
        OVERALL_EXIT=1
    fi
done

# ── Summary ────────────────────────────────────────────────────────────────
if ! $JSON_FLAG; then
    echo -e "${BOLD}━━━ Lint Summary ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    for category in "${SELECTED_CATEGORIES[@]}"; do
        if [[ ${RESULTS[$category]:-2} -eq 0 ]]; then
            echo -e "  ${GREEN}✓${NC} $category"
        else
            echo -e "  ${RED}✗${NC} $category (exit code: ${RESULTS[$category]})"
        fi
    done

    if [[ $OVERALL_EXIT -eq 0 ]]; then
        echo -e "\n  ${GREEN}${BOLD}All lint checks passed.${NC}"
    else
        echo -e "\n  ${RED}${BOLD}Lint errors found. Fix before committing.${NC}"
        echo -e "  ${YELLOW}Tip:${NC} Run '${BOLD}./scripts/lint.sh --fix${NC}' to auto-fix formatting."
    fi
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
fi

exit $OVERALL_EXIT
