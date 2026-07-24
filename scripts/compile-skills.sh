#!/usr/bin/env bash
# ==============================================================================
# compile-skills.sh — Dual-Representation Build System
# ==============================================================================
# Compiles human-readable SKILL.md files into minified XML optimized for LLM
# execution, achieving 35-50% token reduction.
#
# Usage:
#   ./scripts/compile-skills.sh skills/02-product/product-manager/   # single
#   ./scripts/compile-skills.sh --all                                 # all skills
#   ./scripts/compile-skills.sh --verify                              # verify
#   ./scripts/compile-skills.sh --clean                               # clean output
#
# Exit codes: 0=success, 1=compilation error, 2=XML malformation
# ==============================================================================

set -euo pipefail

# ─── Configuration ───────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="${REPO_ROOT}/.skills-compiled"
SKILLS_DIR="${REPO_ROOT}/skills"
PY_COMPILER="${SCRIPT_DIR}/_compile_skill.py"

# Color output (auto-detect terminal)
if [[ -t 1 ]]; then
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
    CYAN='\033[0;36m'; NC='\033[0m'
else
    RED=''; GREEN=''; YELLOW=''; CYAN=''; NC=''
fi

# ─── Logging ─────────────────────────────────────────────────────────────────
log_info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
log_err()   { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# ─── Stats tracking (aggregated via temp file to avoid subshell issues) ──────
STATS_FILE="${OUTPUT_DIR}/.compile_stats"
init_stats() {
    mkdir -p "$OUTPUT_DIR"
    echo "0 0 0 0 0" > "$STATS_FILE"
}
read_stats() { cat "$STATS_FILE" 2>/dev/null || echo "0 0 0 0 0"; }
write_stats() { echo "$1 $2 $3 $4 $5" > "$STATS_FILE"; }

# ─── Compile a single skill ──────────────────────────────────────────────────
compile_one() {
    local skill_dir="${1%/}"
    local skill_name
    skill_name="$(basename "$skill_dir")"

    if [[ ! -f "$skill_dir/SKILL.md" ]]; then
        log_err "No SKILL.md found in $skill_dir"
        return 1
    fi

    local result
    if ! result=$(python3 "$PY_COMPILER" compile "$skill_dir" "$OUTPUT_DIR" 2>&1); then
        log_err "Failed to compile $skill_name"
        echo "$result" >&2
        return 1
    fi

    # Parse JSON summary from Python output (save to file to avoid re-parsing)
    local tmp_json="${OUTPUT_DIR}/.tmp_result.json"
    echo "$result" > "$tmp_json"

    local name orig comp red
    name=$(python3 -c "import json; d=json.load(open('$tmp_json')); print(d['name'])" 2>/dev/null || echo "$skill_name")
    orig=$(python3 -c "import json; d=json.load(open('$tmp_json')); print(d['original'])" 2>/dev/null || echo "0")
    comp=$(python3 -c "import json; d=json.load(open('$tmp_json')); print(d['compiled'])" 2>/dev/null || echo "0")
    red=$(python3 -c "import json; d=json.load(open('$tmp_json')); print(d['reduction'])" 2>/dev/null || echo "0")
    rm -f "$tmp_json"

    # Update aggregate stats (only when compiling all)
    read -r _total _sorig _scomp _sfail _swarn < <(read_stats) 2>/dev/null || true
    _total=${_total:-0}; _sorig=${_sorig:-0}; _scomp=${_scomp:-0}; _sfail=${_sfail:-0}; _swarn=${_swarn:-0}
    local new_total=$((_total + 1))
    local new_sorig=$((_sorig + orig))
    local new_scomp=$((_scomp + comp))
    local new_sfail=$_sfail
    local new_swarn=$_swarn
    write_stats "$new_total" "$new_sorig" "$new_scomp" "$new_sfail" "$new_swarn"

    log_ok "$name: ${orig} → ${comp} tokens (${red}% reduction)"
    return 0
}

# ─── Compile all skills ──────────────────────────────────────────────────────
compile_all() {
    local start_time
    start_time=$(date +%s)

    log_info "Compiling all skills from $SKILLS_DIR..."
    echo ""

    mkdir -p "$OUTPUT_DIR"

    # Collect all skill dirs
    local skill_dirs=()
    while IFS= read -r -d '' md_file; do
        skill_dirs+=("$(dirname "$md_file")")
    done < <(find "$SKILLS_DIR" -name "SKILL.md" -print0 | sort -z)

    local total=${#skill_dirs[@]}
    log_info "Found $total skills. Compiling in parallel..."

    # Determine parallel jobs (use nproc or fallback to 4)
    local jobs=${NPROC:-4}
    if command -v nproc &>/dev/null; then
        jobs=$(nproc)
    elif [[ "$(uname)" == "Darwin" ]]; then
        jobs=$(sysctl -n hw.ncpu 2>/dev/null || echo 4)
    fi
    # Cap at 8 to avoid I/O thrashing
    [[ "$jobs" -gt 8 ]] && jobs=8

    # Process in parallel using background jobs
    local completed=0 failed=0
    local tmp_dir="${OUTPUT_DIR}/.tmp_jobs"
    mkdir -p "$tmp_dir"

    local running=0
    for skill_dir in "${skill_dirs[@]}"; do
        # Wait if at max jobs
        while [[ $running -ge $jobs ]]; do
            wait -n 2>/dev/null || true
            ((running--)) || true
        done

        local skill_name
        skill_name="$(basename "$skill_dir")"

        # Compile in background
        (
            if python3 "$PY_COMPILER" compile "$skill_dir" "$OUTPUT_DIR" > "$tmp_dir/${skill_name}.json" 2>/dev/null; then
                echo "OK" > "$tmp_dir/${skill_name}.status"
            else
                echo "FAIL" > "$tmp_dir/${skill_name}.status"
            fi
        ) &
        ((running++))
    done

    # Wait for remaining jobs
    wait

    # Collect results
    local total_orig=0 total_comp=0
    for skill_dir in "${skill_dirs[@]}"; do
        local skill_name
        skill_name="$(basename "$skill_dir")"
        local status_file="$tmp_dir/${skill_name}.status"
        local json_file="$tmp_dir/${skill_name}.json"

        if [[ -f "$status_file" ]] && [[ "$(cat "$status_file")" == "OK" ]]; then
            ((completed++))
            if [[ -f "$json_file" ]]; then
                local orig comp red
                orig=$(python3 -c "import json; print(json.load(open('$json_file')).get('original', 0))" 2>/dev/null || echo "0")
                comp=$(python3 -c "import json; print(json.load(open('$json_file')).get('compiled', 0))" 2>/dev/null || echo "0")
                red=$(python3 -c "import json; print(json.load(open('$json_file')).get('reduction', 0))" 2>/dev/null || echo "0")
                total_orig=$((total_orig + orig))
                total_comp=$((total_comp + comp))
                log_ok "$skill_name: ${orig} → ${comp} tokens (${red}% reduction)"
            fi
        else
            ((failed++))
            log_err "Failed: $skill_name"
        fi
    done

    # Clean up
    rm -rf "$tmp_dir"
    rm -f "$STATS_FILE"

    local end_time elapsed
    end_time=$(date +%s)
    elapsed=$((end_time - start_time))

    local avg_red=0
    if [[ "$total_orig" -gt 0 ]]; then
        avg_red=$(python3 -c "print(round((1 - $total_comp / $total_orig) * 100, 1))")
    fi

    echo ""
    log_info "──────────────────────────────────────────────────────────"
    log_ok   "Compilation complete: $completed skills compiled"
    if [[ "$failed" -gt 0 ]]; then
        log_warn "  $failed failures"
    fi
    log_info "  Total original tokens: $total_orig"
    log_info "  Total compiled tokens: $total_comp"
    log_info "  Average reduction:     ${avg_red}%"
    log_info "  Time:                  ${elapsed}s"
    log_info "  Output:                $OUTPUT_DIR"
    log_info "──────────────────────────────────────────────────────────"
}

# ─── Verify compiled output ──────────────────────────────────────────────────
verify_all() {
    log_info "Verifying compiled output..."

    if [[ ! -d "$OUTPUT_DIR" ]]; then
        log_err "No compiled output found at $OUTPUT_DIR. Run with --all first."
        return 1
    fi

    python3 "$PY_COMPILER" verify "$OUTPUT_DIR"
    return $?
}

# ─── Clean compiled output ───────────────────────────────────────────────────
clean_output() {
    if [[ -d "$OUTPUT_DIR" ]]; then
        log_info "Removing $OUTPUT_DIR ..."
        rm -rf "$OUTPUT_DIR"
        log_ok "Cleaned compiled output"
    else
        log_info "Nothing to clean (no $OUTPUT_DIR)"
    fi
}

# ─── Ensure .gitignore has .skills-compiled/ entry ──────────────────────────
ensure_gitignore() {
    local gitignore="$REPO_ROOT/.gitignore"
    local entry=".skills-compiled/"

    if [[ -f "$gitignore" ]]; then
        if ! grep -qF "$entry" "$gitignore"; then
            echo "" >> "$gitignore"
            echo "# Compiled skill XML output" >> "$gitignore"
            echo "$entry" >> "$gitignore"
            log_ok "Added '.skills-compiled/' to .gitignore"
        fi
    else
        {
            echo "# Compiled skill XML output"
            echo "$entry"
        } > "$gitignore"
        log_ok "Created .gitignore with '.skills-compiled/' entry"
    fi
}

# ─── Show usage ──────────────────────────────────────────────────────────────
show_usage() {
    cat << 'USAGE'
compile-skills.sh — Dual-Representation Build System

Compiles human-readable SKILL.md files into minified XML optimized for
LLM execution, achieving 35-50% token reduction.

Usage:
  ./scripts/compile-skills.sh <skill-dir>   Compile a single skill
  ./scripts/compile-skills.sh --all          Compile all skills
  ./scripts/compile-skills.sh --verify       Verify compiled output
  ./scripts/compile-skills.sh --clean        Remove compiled output

Examples:
  ./scripts/compile-skills.sh skills/02-product/product-manager/
  ./scripts/compile-skills.sh --all
  ./scripts/compile-skills.sh --verify

Output structure:
  .skills-compiled/
    product-manager/
      skill.xml         Minified XML for LLM execution
      metadata.json     Token stats, compilation info
    system-architect/
      skill.xml
      metadata.json
    ...

Exit codes:
  0  Success
  1  Compilation error (invalid markdown, missing file)
  2  XML malformation (detected during --verify)
  3  Token budget exceeded
USAGE
}

# ─── Main ────────────────────────────────────────────────────────────────────
main() {
    if [[ $# -eq 0 ]]; then
        show_usage
        exit 0
    fi

    # Verify Python compiler exists
    if [[ ! -f "$PY_COMPILER" ]]; then
        log_err "Python compiler not found: $PY_COMPILER"
        exit 1
    fi

    case "${1:-}" in
        --all)
            ensure_gitignore
            compile_all
            ;;
        --verify)
            verify_all
            ;;
        --clean)
            clean_output
            ;;
        --help|-h)
            show_usage
            ;;
        -*)
            log_err "Unknown flag: $1"
            show_usage
            exit 1
            ;;
        *)
            # Single skill directory
            ensure_gitignore
            local skill_dir="${1%/}"
            if [[ ! -d "$skill_dir" ]]; then
                log_err "Directory not found: $skill_dir"
                exit 1
            fi
            local skill_name
            skill_name="$(basename "$skill_dir")"
            log_info "Compiling single skill: $skill_name"
            mkdir -p "$OUTPUT_DIR"
            if compile_one "$skill_dir"; then
                echo ""
                log_ok "Compilation complete → $OUTPUT_DIR/$skill_name/"
            else
                exit 1
            fi
            ;;
    esac
}

main "$@"
