#!/usr/bin/env bash
# ==============================================================================
# G13: Skill Example Validation — Real-World Backtest-Verified Examples
# ==============================================================================
# Validates that every non-framework skill has at least one real-world backtest-
# verified example. Checks YAML frontmatter chain.examples field, verifies
# example directories exist, and confirms backtest files contain verified data.
#
# Usage:
#   validate-skill-examples.sh --all          # Check ALL non-framework skills
#   validate-skill-examples.sh --changed      # Only staged/committed SKILL.md
#   validate-skill-examples.sh --errors-only  # Suppress warnings (PASS lines)
#   validate-skill-examples.sh --no-color      # No ANSI color codes
#
# Exit codes:
#   0 — All skills pass
#   1 — Blocking errors (new skill missing examples)
#   2 — Warnings only (existing skills with issues)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# ── Parse flags ──────────────────────────────────────────────────────────────
CHANGED_ONLY=false
ALL_SKILLS=false
NO_COLOR=false
ERRORS_ONLY=false

for arg in "$@"; do
    case "$arg" in
        --changed)    CHANGED_ONLY=true ;;
        --all)        ALL_SKILLS=true ;;
        --no-color)   NO_COLOR=true ;;
        --errors-only) ERRORS_ONLY=true ;;
        *)
            echo "Usage: $0 [--changed|--all] [--no-color] [--errors-only]" >&2
            exit 3
            ;;
    esac
done

# ── Color helpers ────────────────────────────────────────────────────────────
if $NO_COLOR; then
    RED=''; GREEN=''; YELLOW=''; NC=''; BOLD=''
else
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    NC='\033[0m'
    BOLD='\033[1m'
fi

# ── Output helpers ───────────────────────────────────────────────────────────
fail_line()  { echo -e "  ${RED}✗${NC} $1"; }
pass_line()  { echo -e "  ${GREEN}✓${NC} $1"; }
warn_line()  { echo -e "  ${YELLOW}⚠${NC} $1"; }

errors=0
warnings=0
blocking=0

# ── Gather SKILL.md paths ───────────────────────────────────────────────────
SKILL_FILES=""

if $CHANGED_ONLY; then
    # Git staged + last commit diff
    if git rev-parse --git-dir >/dev/null 2>&1; then
        SKILL_FILES=$( (
            git diff --cached --name-only --diff-filter=ACM 2>/dev/null || true
            git diff --name-only --diff-filter=ACM HEAD 2>/dev/null || true
        ) | grep '/SKILL.md$' | sort -u || true)
    fi
    if [ -z "$SKILL_FILES" ]; then
        echo "No changed SKILL.md files to check."
        exit 0
    fi
elif $ALL_SKILLS; then
    SKILL_FILES=$(find "$REPO_ROOT/skills" -name 'SKILL.md' -not -path '*/00-framework/*' | sort || true)
else
    echo "ERROR: Must specify --changed or --all" >&2
    exit 3
fi

if [ -z "$SKILL_FILES" ]; then
    echo "No SKILL.md files found."
    exit 0
fi

# ── Helper: Extract chain.examples from YAML frontmatter ────────────────────
# Returns space-separated example paths, or empty string.
# Uses the repository's yaml_shim fallback when PyYAML is absent, matching the other checks:
# a missing third-party module must not silently turn this gate into "every skill lacks examples".
extract_examples() {
    local skill_file="$1"
    local scripts_dir="$SCRIPT_DIR/.."
    # `python3 -c` matches this repo's established pattern (see scripts/validate-skills.sh) and is
    # recognised by lint-shell's non-shell-context detection, unlike a heredoc with a trailing
    # redirect. The shim fallback keeps this gate working without PyYAML installed.
    python3 -c "
import sys
sys.path.insert(0, '$scripts_dir')
try:
    import yaml
except ImportError:
    import yaml_shim as yaml
try:
    with open('$skill_file') as fh:
        content = fh.read()
    # Anchor on the delimiter LINES: a bare split('---') also splits on every horizontal rule in
    # the body (some skills have ~170), so the wrong slice would be parsed as frontmatter.
    if not content.startswith('---'):
        sys.exit(1)
    end = content.find('\n---', 3)
    if end == -1:
        sys.exit(1)
    fm = yaml.safe_load(content[3:end]) or {}
    chain = fm.get('chain', {}) or {}
    for ex in (chain.get('examples', []) or []):
        print(ex)
except Exception:
    sys.exit(1)
" 2>/dev/null || true
}

# ── Helper: Check if file contains backtest verification tags ────────────────
has_verification_tags() {
    local dir_path="$1"
    grep -rqE '\[VERIFIED\]|\[COMPUTED\]|\[ESTIMATED|\[BROKER-VERIFIED\]' "$dir_path" 2>/dev/null && return 0 || return 1
}

# ── Helper: Check if file contains dollar-quantified P&L ─────────────────────
has_dollar_pnl() {
    local dir_path="$1"
    grep -rqE '\$[0-9,]+' "$dir_path" 2>/dev/null && return 0 || return 1
}

# ── Helper: Check if content covers best/worst/learnings ─────────────────────
has_scenarios_content() {
    local dir_path="$1"
    # Check for best case, worst case, and learnings content
    local has_best=false has_worst=false has_learnings=false
    if grep -riqE 'best.case|best outcome|optimal outcome|best scenario' "$dir_path" 2>/dev/null; then
        has_best=true
    fi
    if grep -riqE 'worst.case|worst outcome|worst scenario|worst historical' "$dir_path" 2>/dev/null; then
        has_worst=true
    fi
    if grep -riqE 'learning|lesson learned|key takeaway|actionable lesson|what.*learned' "$dir_path" 2>/dev/null; then
        has_learnings=true
    fi
    if $has_best && $has_worst && $has_learnings; then
        return 0
    fi
    return 1
}

# ── Helper: Determine if a skill is "new" (added relative to the base revision) ─
# The base ref is resolved rather than hardcoded: `origin/main` may not exist (a fresh clone
# without a remote, a detached checkout, CI), in which case the old code fell through to
# "not on origin/main" and classified EVERY skill as new — which made every missing-examples
# warning a blocking error. Preference order: an explicit $BASE_REF, then origin/main,
# then main, then the empty tree (everything is new) only as a last resort.
resolve_base_ref() {
    if [ -n "${BASE_REF:-}" ] && git rev-parse --verify --quiet "$BASE_REF" >/dev/null 2>&1; then
        printf '%s' "$BASE_REF"; return 0
    fi
    local candidate
    for candidate in origin/main main origin/HEAD; do
        if git rev-parse --verify --quiet "$candidate" >/dev/null 2>&1; then
            printf '%s' "$candidate"; return 0
        fi
    done
    printf '%s' ""; return 0
}

is_new_skill() {
    local skill_file="$1"
    if ! git rev-parse --git-dir >/dev/null 2>&1; then
        return 1
    fi
    # Paths arrive repo-relative ("./a/b", "a/b") or absolute ("/repo/a/b"), depending on whether
    # the caller used `git diff` or `find`. Resolve the repo root and strip it, so `git show` gets
    # the `<rev>:<path>` form it expects. Getting this wrong silently reclassifies every skill as
    # new, which is what made every missing-examples warning a blocking error.
    local repo_root rel
    repo_root="$(git rev-parse --show-toplevel 2>/dev/null)"
    rel="${skill_file#./}"
    if [ -n "$repo_root" ]; then
        rel="${rel#"$repo_root"/}"
        # Tolerate a symlinked root (e.g. /tmp -> /private/tmp on macOS).
        rel="${rel#"$(cd "$repo_root" && pwd -P 2>/dev/null)"/}"
    fi
    local base
    base="$(resolve_base_ref)"
    if [ -z "$base" ]; then
        # No base to compare against: cannot prove the skill is new, so do not claim it is.
        return 1
    fi
    # Added (not merely modified) between the base and HEAD?
    if git log --diff-filter=A --name-only --pretty=format: "$base..HEAD" 2>/dev/null | grep -qxF "$rel"; then
        return 0
    fi
    # Still absent from the base revision => new.
    if ! git show "$base:$rel" >/dev/null 2>&1; then
        return 0
    fi
    return 1
}

# ── Main validation loop ─────────────────────────────────────────────────────
echo ""
echo "G13: Skill Example Validation — Real-World Backtest-Verified Examples"
echo ""

skill_count=0
pass_count=0
fail_count=0

while IFS= read -r skill_f; do
    [ -z "$skill_f" ] && continue
    skill_count=$((skill_count + 1))

    # Convert relative path to absolute if needed
    if [[ "$skill_f" != /* ]]; then
        skill_abs="$REPO_ROOT/$skill_f"
    else
        skill_abs="$skill_f"
    fi

    [ ! -f "$skill_abs" ] && continue

    # Get short display name (e.g., "14-finance/options-strategist")
    skill_display=$(echo "$skill_abs" | sed -n 's|.*/skills/\(.*\)/SKILL\.md|\1|p')
    if [ -z "$skill_display" ]; then
        skill_display=$(echo "$skill_abs" | sed -n 's|.*/skills/\(.*/SKILL\.md\)|\1|p')
    fi

    # Extract example paths from YAML frontmatter
    example_paths=$(extract_examples "$skill_abs")

    if [ -z "$example_paths" ]; then
        if is_new_skill "${skill_f#./}"; then
            fail_line "$skill_display: ${BOLD}MISSING examples field - NEW skill requires examples${NC}"
            blocking=$((blocking + 1))
            errors=$((errors + 1))
        else
            fail_line "$skill_display: missing examples field in chain section"
            warnings=$((warnings + 1))
        fi
        fail_count=$((fail_count + 1))
        continue
    fi

    # Validate each example path
    all_ok=true
    while IFS= read -r ex_path; do
        [ -z "$ex_path" ] && continue
        ex_abs="$REPO_ROOT/$ex_path"

        # Check 1: Directory exists
        if [ ! -d "$ex_abs" ]; then
            fail_line "$skill_display: example dir not found: $ex_path"
            all_ok=false
            continue
        fi

        # Check 2: README.md exists
        if [ ! -f "$ex_abs/README.md" ]; then
            fail_line "$skill_display: example dir missing README.md: $ex_path"
            all_ok=false
            continue
        fi

        # Check 3: Verification tags present
        if ! has_verification_tags "$ex_abs"; then
            fail_line "$skill_display: no [VERIFIED]/[COMPUTED]/[ESTIMATED]/[BROKER-VERIFIED] tags in $ex_path"
            all_ok=false
            continue
        fi

        # Check 4: Dollar-quantified P&L present
        if ! has_dollar_pnl "$ex_abs"; then
            fail_line "$skill_display: no dollar-quantified P&L in $ex_path"
            all_ok=false
            continue
        fi

        # Check 5: Best/worst/learnings content present
        if ! has_scenarios_content "$ex_abs"; then
            fail_line "$skill_display: missing best/worst/learnings analysis in $ex_path"
            all_ok=false
            continue
        fi

    done <<< "$example_paths"

    if $all_ok; then
        if ! $ERRORS_ONLY; then
            pass_line "$skill_display: example(s) validated"
        fi
        pass_count=$((pass_count + 1))
    else
        if is_new_skill "${skill_f#./}"; then
            blocking=$((blocking + 1))
        fi
        errors=$((errors + 1))
        fail_count=$((fail_count + 1))
    fi

done <<< "$SKILL_FILES"

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "──────────────────────────────────────────────────────────────────────────"
echo -e "  Skills checked: ${BOLD}$skill_count${NC}"
echo -e "  ${GREEN}Passed: $pass_count${NC}  ${RED}Failed: $fail_count${NC}"
if [ "$warnings" -gt 0 ]; then
    echo -e "  ${YELLOW}Warnings: $warnings (existing skills missing examples)${NC}"
fi
if [ "$blocking" -gt 0 ]; then
    echo -e "  ${RED}Blocking: $blocking (new skills require examples)${NC}"
fi
echo "──────────────────────────────────────────────────────────────────────────"

# ── Exit code logic ──────────────────────────────────────────────────────────
if [ "$blocking" -gt 0 ]; then
    exit 1
elif [ "$warnings" -gt 0 ]; then
    exit 2
fi
exit 0
