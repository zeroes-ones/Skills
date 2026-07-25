#!/usr/bin/env bash
# ==============================================================================
# verify-script-integrity.sh — CI/CD Security Gate
# ==============================================================================
# Validates that all executable scripts match their SHA256 manifest entries.
# Designed as a blocking CI gate — any tampered script fails the pipeline.
#
# Usage:
#   ./scripts/verify-script-integrity.sh              # Check all scripts
#   ./scripts/verify-script-integrity.sh --json        # JSON output for CI
#   ./scripts/verify-script-integrity.sh --strict      # Fail on untracked scripts
#   ./scripts/verify-script-integrity.sh --gpg          # Also verify GPG signature
#
# Exit codes: 0=clean, 1=tampered/missing, 2=manifest missing, 3=signature invalid
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFEST_FILE="$REPO_ROOT/scripts/.sha256manifest"
SIG_FILE="$MANIFEST_FILE.asc"

OUTPUT_MODE="text"
STRICT_MODE=false
VERIFY_GPG=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --json)   OUTPUT_MODE="json"; shift ;;
        --strict) STRICT_MODE=true; shift ;;
        --gpg)    VERIFY_GPG=true; shift ;;
        --help|-h)
            echo "Usage: verify-script-integrity.sh [--json] [--strict] [--gpg]"
            exit 0 ;;
        *) echo "Unknown: $1"; exit 1 ;;
    esac
done

if [[ ! -f "$MANIFEST_FILE" ]]; then
    if [[ "$OUTPUT_MODE" == "json" ]]; then
        echo '{"status":"error","reason":"manifest missing"}'
    else
        echo "ERROR: No manifest found. Run: ./scripts/generate-sha256-manifest.sh"
    fi
    exit 2
fi

# GPG signature verification
if $VERIFY_GPG; then
    if [[ ! -f "$SIG_FILE" ]]; then
        if [[ "$OUTPUT_MODE" == "json" ]]; then
            echo '{"status":"error","reason":"signature file missing"}'
        else
            echo "ERROR: No GPG signature found at $SIG_FILE"
        fi
        exit 3
    fi
    if gpg --verify "$SIG_FILE" "$MANIFEST_FILE" 2>/dev/null; then
        [[ "$OUTPUT_MODE" == "text" ]] && echo "[OK] GPG signature valid"
    else
        [[ "$OUTPUT_MODE" == "text" ]] && echo "[FAIL] GPG signature INVALID"
        exit 3
    fi
fi

# Parse manifest (bash 3.x compatible — use temp files instead of associative arrays)
MANIFEST_TMP=$(mktemp -d)
trap 'rm -rf "$MANIFEST_TMP"' EXIT

# Extract paths and hashes into parallel files
> "$MANIFEST_TMP/paths"
> "$MANIFEST_TMP/hashes"
while IFS= read -r line; do
    [[ "$line" =~ ^# ]] && continue
    [[ -z "$line" ]] && continue
    echo "${line#*  }" >> "$MANIFEST_TMP/paths"
    echo "${line%%  *}" >> "$MANIFEST_TMP/hashes"
done < "$MANIFEST_FILE"

# Check results
> "$MANIFEST_TMP/tampered"
> "$MANIFEST_TMP/missing"
> "$MANIFEST_TMP/untracked"
passed=0

# Build set of manifest paths for fast lookup (line-anchored for exact match)
grep -E '^[a-f0-9]{64}  ' "$MANIFEST_FILE" | awk '{print $2}' | sort > "$MANIFEST_TMP/paths_sorted"

while IFS= read -r path; do
    full_path="$REPO_ROOT/$path"
    # Use exact match: line starts with hash then two spaces then path
    expected=$(grep -E "^[a-f0-9]{64}  ${path}$" "$MANIFEST_FILE" | head -1 | awk '{print $1}')

    if [[ ! -f "$full_path" ]]; then
        echo "$path" >> "$MANIFEST_TMP/missing"
        continue
    fi

    actual=$(shasum -a 256 "$full_path" | awk '{print $1}')

    if [[ "$actual" != "$expected" ]]; then
        echo "$path" >> "$MANIFEST_TMP/tampered"
    else
        passed=$((passed + 1))
    fi
done < "$MANIFEST_TMP/paths"

# Check for scripts not in manifest
find "$REPO_ROOT/scripts" "$REPO_ROOT/skills" "$REPO_ROOT/.githooks" \
    -type f \( -name '*.sh' -o -name '*.py' \) -print0 2>/dev/null | sort -z | \
while IFS= read -r -d '' script_path; do
    rel_path="${script_path#$REPO_ROOT/}"
    # Skip manifest and signature files
    [[ "$rel_path" == "scripts/.sha256manifest"* ]] && continue
    if ! grep -qxF "$rel_path" "$MANIFEST_TMP/paths_sorted" 2>/dev/null; then
        echo "$rel_path" >> "$MANIFEST_TMP/untracked"
    fi
done

tampered_count=$(wc -l < "$MANIFEST_TMP/tampered" | tr -d ' ')
missing_count=$(wc -l < "$MANIFEST_TMP/missing" | tr -d ' ')
untracked_count=$(wc -l < "$MANIFEST_TMP/untracked" | tr -d ' ')

# Output
status_str="pass"
[[ "$tampered_count" -gt 0 ]] || [[ "$missing_count" -gt 0 ]] && status_str="fail"

if [[ "$OUTPUT_MODE" == "json" ]]; then
    tampered_json=$(python3 -c "import json; print(json.dumps([l.strip() for l in open('$MANIFEST_TMP/tampered') if l.strip()]))" 2>/dev/null || echo "[]")
    missing_json=$(python3 -c "import json; print(json.dumps([l.strip() for l in open('$MANIFEST_TMP/missing') if l.strip()]))" 2>/dev/null || echo "[]")
    untracked_json=$(python3 -c "import json; print(json.dumps([l.strip() for l in open('$MANIFEST_TMP/untracked') if l.strip()]))" 2>/dev/null || echo "[]")
    echo "{"
    echo "  \"status\": \"$status_str\","
    echo "  \"passed\": $passed,"
    echo "  \"tampered\": $tampered_count,"
    echo "  \"missing\": $missing_count,"
    echo "  \"untracked\": $untracked_count,"
    echo "  \"tampered_files\": $tampered_json,"
    echo "  \"missing_files\": $missing_json,"
    echo "  \"untracked_files\": $untracked_json"
    echo "}"
else
    echo "=== Script Integrity Verification ==="
    echo ""
    while IFS= read -r path; do
        [[ -z "$path" ]] && continue
        echo -e "  \033[0;31m[MISSING]\033[0m  $path"
    done < "$MANIFEST_TMP/missing"
    while IFS= read -r path; do
        [[ -z "$path" ]] && continue
        echo -e "  \033[0;31m[TAMPERED]\033[0m $path"
    done < "$MANIFEST_TMP/tampered"
    while IFS= read -r path; do
        [[ -z "$path" ]] && continue
        echo -e "  \033[1;33m[UNTRACKED]\033[0m $path"
    done < "$MANIFEST_TMP/untracked"
    echo ""
    echo "──────────────────────────────────────────"
    echo -e "  Verified:  \033[0;32m$passed passed\033[0m"
    if [[ "$tampered_count" -gt 0 ]]; then
        echo -e "  Tampered:  \033[0;31m$tampered_count\033[0m"
    fi
    if [[ "$missing_count" -gt 0 ]]; then
        echo -e "  Missing:   \033[1;33m$missing_count\033[0m"
    fi
    if [[ "$untracked_count" -gt 0 ]]; then
        echo -e "  Untracked: \033[1;33m$untracked_count\033[0m"
    fi
    echo "──────────────────────────────────────────"
fi

# Exit code
if [[ "$tampered_count" -gt 0 ]] || [[ "$missing_count" -gt 0 ]]; then
    exit 1
fi
if $STRICT_MODE && [[ "$untracked_count" -gt 0 ]]; then
    exit 1
fi
exit 0
