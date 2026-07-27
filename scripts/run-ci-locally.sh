#!/usr/bin/env bash
# =============================================================================
# run-ci-locally.sh — Mirrors GitHub CI workflow locally
#
# Runs the exact same 3 jobs as .github/workflows/validate.yml:
#   Job 1: validate  — validate-skills.sh + chain symmetry + token budget
#   Job 2: hooks     — verify hooks installable
#   Job 3: lint      — markdownlint + reference link integrity
#
# Usage:
#   ./scripts/run-ci-locally.sh           # Full CI mirror (all 3 jobs)
#   ./scripts/run-ci-locally.sh --quick   # Skip slow checks (markdownlint)
#   ./scripts/run-ci-locally.sh --job lint # Run a single job
#
# Exit codes match CI: 0 = all pass, 1 = at least one job failed
# =============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

QUICK_MODE=false
SINGLE_JOB=""

# ── Parse args ──────────────────────────────────────────────────────────
for arg in "$@"; do
    case "$arg" in
        --quick) QUICK_MODE=true ;;
        --job) SINGLE_JOB="${2:-}"; shift ;;
        --job=*) SINGLE_JOB="${arg#--job=}" ;;
        -h|--help)
            echo "Usage: $0 [--quick] [--job validate|hooks|lint]"
            echo ""
            echo "Mirrors GitHub CI workflow (.github/workflows/validate.yml) locally."
            echo ""
            echo "Options:"
            echo "  --quick        Skip slow checks (markdownlint over all 214 skills)"
            echo "  --job NAME     Run a single job: validate, hooks, or lint"
            echo "  -h, --help     Show this help"
            exit 0
            ;;
    esac
done

FAILURES=0
PASSES=0
TOTAL=0

section_header() {
    echo ""
    echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}${BOLD}  $1${NC}"
    echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
}

step_pass() {
    echo -e "  ${GREEN}✓${NC} $1"
    PASSES=$((PASSES + 1))
    TOTAL=$((TOTAL + 1))
}

step_fail() {
    echo -e "  ${RED}✗${NC} $1"
    FAILURES=$((FAILURES + 1))
    TOTAL=$((TOTAL + 1))
}

step_warn() {
    echo -e "  ${YELLOW}⚠${NC} $1 (advisory — non-blocking)"
    PASSES=$((PASSES + 1))
    TOTAL=$((TOTAL + 1))
}

step_skip() {
    echo -e "  ${YELLOW}⊘${NC} $1 (skipped — tool not available)"
}

# ── Job 1: Validate ─────────────────────────────────────────────────────
run_validate_job() {
    section_header "Job 1/3: Validate (skills + chains + budget)"

    # 1a. Full skills validation
    echo "  [1a] Skills validation suite (validate-skills.sh)..."
    if bash "$REPO_ROOT/scripts/validate-skills.sh"; then
        step_pass "Skills validation suite"
    else
        step_fail "Skills validation suite"
    fi

    # 1b. Chain symmetry
    echo ""
    echo "  [1b] Chain symmetry (validate_chains.py)..."
    if python3 "$REPO_ROOT/scripts/validate_chains.py" 2>&1; then
        step_pass "Chain symmetry"
    else
        # Chain symmetry is continue-on-error in CI
        step_warn "Chain symmetry (advisory — 817 pre-existing gaps)"
    fi

    # 1c. Token budget report
    echo ""
    echo "  [1c] Token budget report..."
    python3 -c "
import os, re
over_budget = 0
total = 0
for root, _, files in os.walk('skills'):
    for f in files:
        if f == 'SKILL.md':
            path = os.path.join(root, f)
            total += 1
            with open(path) as fh:
                content = fh.read()
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) < 3:
                continue
            words = len(parts[2].split())
            if words > 5000:
                over_budget += 1
                print(f'    ⚠️  {words:>5} words — {path}')
print(f'    {total} skills checked, {over_budget} over 5000-word budget')
" 2>/dev/null
    step_pass "Token budget report"
}

# ── Job 2: Hooks ────────────────────────────────────────────────────────
run_hooks_job() {
    section_header "Job 2/3: Hooks (install + verify)"

    # 2a. Verify hooks are installable
    echo "  [2a] Hook installation test..."
    if [ -f "$REPO_ROOT/scripts/install-hooks.sh" ]; then
        if bash "$REPO_ROOT/scripts/install-hooks.sh" 2>&1; then
            step_pass "Hook install script runs"
        else
            step_fail "Hook install script failed"
        fi
    else
        step_fail "scripts/install-hooks.sh not found"
    fi

    # 2b. Pre-commit gate runs clean
    echo ""
    echo "  [2b] Pre-commit hook dry-run..."
    if [ -f "$REPO_ROOT/.githooks/pre-commit" ]; then
        if bash "$REPO_ROOT/.githooks/pre-commit" 2>&1; then
            step_pass "Pre-commit hook dry-run"
        else
            step_warn "Pre-commit hook had issues (may fail on changed files only)"
        fi
    else
        step_fail ".githooks/pre-commit not found"
    fi
}

# ── Job 3: Lint ─────────────────────────────────────────────────────────
run_lint_job() {
    section_header "Job 3/3: Lint (markdown + links)"

    # 3a. Markdown lint
    echo "  [3a] Markdown lint (all skills)..."
    if [ "$QUICK_MODE" = true ]; then
        step_skip "Markdown lint (--quick mode)"
    elif command -v npx &>/dev/null; then
        if npx --yes markdownlint-cli2 'skills/**/SKILL.md' --config .markdownlint.json 2>&1; then
            step_pass "Markdown lint — 0 errors"
        else
            step_fail "Markdown lint found errors"
        fi
    else
        step_skip "Markdown lint (npx not available)"
    fi

    # 3b. Reference link integrity
    echo ""
    echo "  [3b] Reference link integrity..."
    errors=0
    while IFS= read -r line; do
        ref_file=$(echo "$line" | grep -oP '(?<=\(\.\/references\/)[^)]+' || true)
        if [ -n "$ref_file" ]; then
            dir=$(echo "$line" | cut -d: -f1 | xargs dirname)
            if [ ! -f "$dir/references/$ref_file" ]; then
                echo "    ❌ BROKEN: $dir/references/$ref_file"
                errors=$((errors + 1))
            fi
        fi
    done < <(grep -roPH '\[.*\]\(\.\/references\/[^)]+\)' skills/ 2>/dev/null || true)
    if [ "$errors" -eq 0 ]; then
        step_pass "Reference links — 0 broken"
    else
        step_fail "Reference links — $errors broken"
    fi
}

# ── Main ────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║  CI Mirror: Local Skills Governance Gate                    ║${NC}"
echo -e "${BOLD}║  Mirrors .github/workflows/validate.yml                     ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"

if [ "$QUICK_MODE" = true ]; then
    echo -e "  ${YELLOW}Mode: --quick (skipping markdownlint)${NC}"
fi

START_TIME=$(date +%s)

case "$SINGLE_JOB" in
    validate) run_validate_job ;;
    hooks)    run_hooks_job ;;
    lint)     run_lint_job ;;
    "")
        run_validate_job
        run_hooks_job
        run_lint_job
        ;;
    *)
        echo -e "${RED}Unknown job: $SINGLE_JOB${NC}"
        echo "Valid jobs: validate, hooks, lint"
        exit 1
        ;;
esac

# ── Summary ─────────────────────────────────────────────────────────────
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}  CI Mirror Summary${NC}"
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  Total steps: ${TOTAL}"
echo -e "  ${GREEN}Passed: ${PASSES}${NC}"
if [ "$FAILURES" -gt 0 ]; then
    echo -e "  ${RED}Failed: ${FAILURES}${NC}"
else
    echo -e "  Failed: 0"
fi
echo -e "  Duration: ${DURATION}s"
echo ""

if [ "$FAILURES" -gt 0 ]; then
    echo -e "${RED}${BOLD}❌ CI Mirror FAILED — ${FAILURES} step(s) failed${NC}"
    echo ""
    echo "  Fix guidance:"
    echo "    • Template issues: ./scripts/lint.sh --fix && python3 scripts/lib/lint-template.py --changed"
    echo "    • Chain issues:    python3 scripts/validate_chains.py --fix --name <skill>"
    echo "    • Markdown issues: npx markdownlint-cli2 --fix 'skills/**/SKILL.md'"
    echo "    • Broken links:    fix reference paths in SKILL.md files"
    echo ""
    exit 1
else
    echo -e "${GREEN}${BOLD}✅ CI Mirror PASSED — all steps green${NC}"
    echo ""
    exit 0
fi
