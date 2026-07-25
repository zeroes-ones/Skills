#!/usr/bin/env bash
# ==============================================================================
# generate-sha256-manifest.sh — Script Integrity Verification System
# ==============================================================================
# Generates a SHA256 manifest for all executable scripts in the repository.
# This manifest is checked by verify-script-integrity.sh and the pre-commit
# hook to detect unauthorized or malicious modifications to any script.
#
# Usage:
#   ./scripts/generate-sha256-manifest.sh              # Generate new manifest
#   ./scripts/generate-sha256-manifest.sh --check       # Verify against existing
#   ./scripts/generate-sha256-manifest.sh --sign KEY    # Sign with GPG key
#
# Exit codes: 0=success, 1=hash mismatch, 2=missing files, 3=signing error
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFEST_FILE="$REPO_ROOT/scripts/.sha256manifest"
MODE="generate"
GPG_KEY=""
QUIET=false

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

while [[ $# -gt 0 ]]; do
    case "$1" in
        --check) MODE="check"; shift ;;
        --sign) MODE="sign"; GPG_KEY="$2"; shift 2 ;;
        --quiet) QUIET=true; shift ;;
        --help|-h)
            echo "Usage: generate-sha256-manifest.sh [--check|--sign KEY]"
            echo "  (no flag)  Generate new SHA256 manifest"
            echo "  --check    Verify all scripts match existing manifest"
            echo "  --sign KEY Sign manifest with GPG key for tamper-evident distribution"
            exit 0 ;;
        *) echo "Unknown: $1"; exit 1 ;;
    esac
done

# Scripts to include in manifest — core scripts + all verify-skill.sh files
# Excludes the manifest itself and generated files
collect_scripts() {
    # Core scripts (excluding manifest and self)
    find "$REPO_ROOT/scripts" -type f \( -name '*.sh' -o -name '*.py' \) \
        ! -name '.sha256manifest' ! -name '.sha256manifest.sig' \
        ! -name 'generate-sha256-manifest.sh' \
        -print0 2>/dev/null

    # All per-skill scripts (verify-skill.sh + Python tools)
    find "$REPO_ROOT/skills" -type f \( -name '*.sh' -o -name '*.py' \) -print0 2>/dev/null

    # Git hooks
    find "$REPO_ROOT/.githooks" -type f -print0 2>/dev/null
}

generate_manifest() {
    [[ "$QUIET" == "true" ]] || echo -e "${CYAN}[GENERATE]${NC} Computing SHA256 hashes for all scripts..."
    echo "# SHA256 Script Integrity Manifest" > "$MANIFEST_FILE"
    echo "# Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")" >> "$MANIFEST_FILE"
    echo "# Repository: $(cd "$REPO_ROOT" && git remote get-url origin 2>/dev/null || echo 'unknown')" >> "$MANIFEST_FILE"
    echo "# Commit:    $(cd "$REPO_ROOT" && git rev-parse HEAD 2>/dev/null || echo 'unknown')" >> "$MANIFEST_FILE"
    echo "#" >> "$MANIFEST_FILE"
    echo "# Format: SHA256  *relative/path" >> "$MANIFEST_FILE"
    echo "# Verify:  ./scripts/verify-script-integrity.sh" >> "$MANIFEST_FILE"
    echo "" >> "$MANIFEST_FILE"

    local count=0
    while IFS= read -r -d '' script_path; do
        local rel_path="${script_path#$REPO_ROOT/}"
        local hash
        hash=$(shasum -a 256 "$script_path" | awk '{print $1}')
        echo "$hash  $rel_path" >> "$MANIFEST_FILE"
        count=$((count + 1))
    done < <(collect_scripts | sort -z)

    [[ "$QUIET" == "true" ]] || echo -e "${GREEN}[OK]${NC} Manifest generated: $count scripts hashed → $MANIFEST_FILE"
}

check_manifest() {
    if [[ ! -f "$MANIFEST_FILE" ]]; then
        echo -e "${RED}[ERROR]${NC} No manifest found at $MANIFEST_FILE"
        echo "Run: ./scripts/generate-sha256-manifest.sh to create one."
        exit 1
    fi

    echo -e "${CYAN}[VERIFY]${NC} Checking script integrity against $MANIFEST_FILE..."
    echo ""

    local total=0 passed=0 failed=0 missing=0 untracked=0
    declare -a manifest_entries
    declare -A manifest_map

    # Parse manifest
    while IFS= read -r line; do
        [[ "$line" =~ ^# ]] && continue
        [[ -z "$line" ]] && continue
        local hash="${line%%  *}"
        local path="${line#*  }"
        manifest_map["$path"]="$hash"
        manifest_entries+=("$path")
    done < "$MANIFEST_FILE"

    # Check each manifest entry exists and matches
    for path in "${manifest_entries[@]}"; do
        local full_path="$REPO_ROOT/$path"
        local expected_hash="${manifest_map[$path]}"

        if [[ ! -f "$full_path" ]]; then
            echo -e "  ${RED}[MISSING]${NC} $path — file no longer exists"
            missing=$((missing + 1))
            continue
        fi

        local actual_hash
        actual_hash=$(shasum -a 256 "$full_path" | awk '{print $1}')

        if [[ "$actual_hash" == "$expected_hash" ]]; then
            echo -e "  ${GREEN}[OK]${NC} $path"
            passed=$((passed + 1))
        else
            echo -e "  ${RED}[TAMPERED]${NC} $path — hash mismatch!"
            echo "    Expected: $expected_hash"
            echo "    Actual:   $actual_hash"
            failed=$((failed + 1))
        fi
        total=$((total + 1))
    done

    # Check for scripts NOT in manifest (potential injection)
    while IFS= read -r -d '' script_path; do
        local rel_path="${script_path#$REPO_ROOT/}"
        if [[ -z "${manifest_map[$rel_path]:-}" ]]; then
            echo -e "  ${YELLOW}[UNTRACKED]${NC} $rel_path — script not in manifest (potential injection vector)"
            untracked=$((untracked + 1))
        fi
    done < <(collect_scripts | sort -z)

    echo ""
    echo "──────────────────────────────────────────"
    echo -e "  Total:     $total"
    echo -e "  ${GREEN}Passed:    $passed${NC}"
    if [[ $failed -gt 0 ]]; then
        echo -e "  ${RED}Tampered:  $failed${NC}"
    fi
    if [[ $missing -gt 0 ]]; then
        echo -e "  ${YELLOW}Missing:   $missing${NC}"
    fi
    if [[ $untracked -gt 0 ]]; then
        echo -e "  ${YELLOW}Untracked: $untracked${NC}"
    fi
    echo "──────────────────────────────────────────"

    if [[ $failed -gt 0 ]] || [[ $missing -gt 0 ]]; then
        echo -e "${RED}[FAIL]${NC} Script integrity check FAILED — do NOT execute untrusted scripts."
        exit 1
    fi

    if [[ $untracked -gt 0 ]]; then
        echo -e "${YELLOW}[WARN]${NC} $untracked untracked scripts found. Run generate-sha256-manifest.sh to update."
        # Non-blocking for untracked (new scripts may be legitimate)
    else
        echo -e "${GREEN}[PASS]${NC} All scripts verified. No tampering detected."
    fi
}

sign_manifest() {
    if [[ -z "$GPG_KEY" ]]; then
        echo -e "${RED}[ERROR]${NC} GPG key required for signing. Use --sign KEYID"
        exit 3
    fi
    if [[ ! -f "$MANIFEST_FILE" ]]; then
        echo -e "${YELLOW}[INFO]${NC} Generating manifest before signing..."
        generate_manifest
    fi
    echo -e "${CYAN}[SIGN]${NC} Signing manifest with GPG key $GPG_KEY..."
    gpg --detach-sign --local-user "$GPG_KEY" --armor "$MANIFEST_FILE"
    echo -e "${GREEN}[OK]${NC} Signature written to $MANIFEST_FILE.asc"
}

case "$MODE" in
    generate) generate_manifest ;;
    check)    check_manifest ;;
    sign)     sign_manifest ;;
esac
