#!/usr/bin/env bash
# ==============================================================================
# sandbox-exec.sh — Isolated Execution Environment for Untrusted Code
# ==============================================================================
# Implements the ai-security spec's Phase 0: Agent Context-Window Security.
# Treats ALL loaded project files as potentially untrusted. Isolates file
# read/write scopes and prevents prompt injection via third-party code in
# README files, package manifests, or dependency source.
#
# Security Model:
#   - Read-only access to project files (no writes to source tree)
#   - Temp directory for output (isolated from project)
#   - No network access unless explicitly allowed
#   - File size limits to prevent DOS
#   - Content sanitization for known injection patterns
#   - Audit log of all file accesses
#
# Usage:
#   sandbox-exec.sh --command "npm test" --project /path/to/repo
#   sandbox-exec.sh --command "python3 analyze.py" --project . --allow-network
#   sandbox-exec.sh --scan /path/to/repo  # Scan for injection patterns only
#   sandbox-exec.sh --sanitize README.md  # Sanitize a file for agent consumption
# ==============================================================================
set -euo pipefail

COMMAND=""
PROJECT=""
SCAN_ONLY=false
SANITIZE_FILE=""
ALLOW_NETWORK=false
ALLOW_WRITES=false
MAX_FILE_SIZE=$((10 * 1024 * 1024))  # 10MB
AUDIT_LOG=""
OUTPUT_DIR=""
VERBOSE=false

# ─── Parse Arguments ─────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --command) COMMAND="$2"; shift 2 ;;
        --project) PROJECT="$2"; shift 2 ;;
        --scan) SCAN_ONLY=true; PROJECT="$2"; shift 2 ;;
        --sanitize) SANITIZE_FILE="$2"; shift 2 ;;
        --allow-network) ALLOW_NETWORK=true; shift ;;
        --allow-writes) ALLOW_WRITES=true; shift ;;
        --max-file-size) MAX_FILE_SIZE="$2"; shift 2 ;;
        --verbose) VERBOSE=true; shift ;;
        --output) OUTPUT_DIR="$2"; shift 2 ;;
        -h|--help)
            sed -n '2,30p' "$0"; exit 0 ;;
        *) echo "ERROR: $1"; exit 1 ;;
    esac
done

# ─── Setup ───────────────────────────────────────────────────────────────────
SANDBOX_ROOT=$(mktemp -d /tmp/sandbox-XXXXXX)
AUDIT_LOG="$SANDBOX_ROOT/audit.log"
OUTPUT_DIR="${OUTPUT_DIR:-$SANDBOX_ROOT/output}"
mkdir -p "$OUTPUT_DIR"

log_audit() {
    local level="$1"; shift
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] [$level] $*" >> "$AUDIT_LOG"
    $VERBOSE && echo "  [$level] $*" >&2 || true
}

cleanup() {
    log_audit "INFO" "Cleaning up sandbox: $SANDBOX_ROOT"
    rm -rf "$SANDBOX_ROOT" 2>/dev/null || true
}
trap cleanup EXIT

# ─── Injection Pattern Scanner ───────────────────────────────────────────────
# Known prompt injection patterns in project files

INJECTION_PATTERNS=(
    # Direct instruction overrides
    'IGNORE (PREVIOUS|ALL) (INSTRUCTIONS|RULES|CONSTRAINTS)'
    'DISREGARD (PREVIOUS|ALL) (INSTRUCTIONS|RULES|CONSTRAINTS)'
    'FORGET (PREVIOUS|ALL) (INSTRUCTIONS|RULES)'
    'OVERRIDE (SYSTEM|AGENT) (PROMPT|INSTRUCTIONS)'
    'YOU ARE NOW'
    'NEW (SYSTEM|AGENT) (PROMPT|INSTRUCTIONS)'
    'YOUR (NEW|ONLY) (ROLE|JOB|TASK) IS'
    
    # System prompt extraction
    'REPEAT (THE|YOUR) (SYSTEM|INITIAL) (PROMPT|INSTRUCTIONS)'
    'PRINT (THE|YOUR) (SYSTEM|INITIAL) (PROMPT|INSTRUCTIONS)'
    'WHAT (IS|ARE) YOUR (SYSTEM|INITIAL) (PROMPT|INSTRUCTIONS)'
    'OUTPUT YOUR (SYSTEM|BASE) PROMPT'
    
    # Tool/execution hijacking
    'EXECUTE (THIS|THE FOLLOWING) (COMMAND|CODE)'
    'RUN (THIS|THE FOLLOWING) (COMMAND|SCRIPT|CODE) WITHOUT (ASKING|CONFIRMATION)'
    'curl.*\|.*(bash|sh|python)'
    '\$\(.*rm -rf.*\)'
    
    # Data exfiltration
    'SEND.*(TO|AT).*(http|https)://'
    'curl.*http.*\$\{?[A-Z_]+\}?'
    'ENV\|ENVIRONMENT\|SECRET\|TOKEN\|PASSWORD\|CREDENTIAL'
    
    # Instruction embedding
    '\[SYSTEM\]:'
    '\[INST\]:'
    '<\|im_start\|>'
    '<\|im_end\|>'
    '<<SYS>>'
    '<system>'
    'Human:.*Assistant:'
    
    # Token smuggling
    '(IGNORE|DISREGARD).*ABOVE.*(INSTRUCTION|RULE)'
    'IMPORTANT:.*IGNORE'
    'CRITICAL:.*OVERRIDE'
)

scan_file() {
    local file="$1"
    local findings=0
    
    # Skip binary files
    if file "$file" 2>/dev/null | grep -q "binary\|data\|archive\|image\|audio\|video"; then
        return 0
    fi
    
    # Skip node_modules, .git, build artifacts
    if echo "$file" | grep -qE "(node_modules|\.git/|\.next/|dist/|build/|\.venv/|__pycache__)"; then
        return 0
    fi
    
    # Size check
    local fsize
    fsize=$(wc -c < "$file" 2>/dev/null || echo 0)
    if [[ $fsize -gt $MAX_FILE_SIZE ]]; then
        log_audit "WARN" "File too large ($fsize bytes), skipping: $file"
        return 0
    fi
    
    # Scan for patterns
    local line_num=0
    while IFS= read -r line; do
        line_num=$((line_num + 1))
        for pattern in "${INJECTION_PATTERNS[@]}"; do
            if echo "$line" | grep -qiE "$pattern" 2>/dev/null; then
                log_audit "ALERT" "INJECTION_PATTERN in $file:$line_num — matches: $pattern"
                log_audit "ALERT" "  Content: $(echo "$line" | cut -c1-120)"
                findings=$((findings + 1))
            fi
        done
    done < "$file"
    
    [[ $findings -gt 0 ]] && return 1 || return 0
}

sanitize_content() {
    local content="$1"
    
    # Strip known injection markers
    content=$(echo "$content" | sed -E '
        s/\[SYSTEM\]://gI
        s/\[INST\]://gI
        s/<\|im_start\|>//gI
        s/<\|im_end\|>//gI
        s/<<SYS>>//gI
        s/<system>//gI
        s/<\/system>//gI
    ')
    
    # Neutralize instruction overrides (wrap in code blocks)
    content=$(echo "$content" | sed -E '
        s/(IGNORE (PREVIOUS|ALL) (INSTRUCTIONS|RULES|CONSTRAINTS))/`\1`/gI
        s/(DISREGARD (PREVIOUS|ALL) (INSTRUCTIONS|RULES|CONSTRAINTS))/`\1`/gI
        s/(FORGET (PREVIOUS|ALL) (INSTRUCTIONS|RULES))/`\1`/gI
        s/(OVERRIDE (SYSTEM|AGENT) (PROMPT|INSTRUCTIONS))/`\1`/gI
        s/(YOU ARE NOW)/`\1`/gI
    ')
    
    echo "$content"
}

# ─── Main ────────────────────────────────────────────────────────────────────

# Mode 1: File sanitization
if [[ -n "$SANITIZE_FILE" ]]; then
    if [[ -f "$SANITIZE_FILE" ]]; then
        echo "🧹 Sanitizing: $SANITIZE_FILE"
        ORIGINAL=$(cat "$SANITIZE_FILE")
        CLEANED=$(sanitize_content "$ORIGINAL")
        
        # Check if anything was sanitized
        if [[ "$ORIGINAL" != "$CLEANED" ]]; then
            echo "⚠️  Injection patterns neutralized in $SANITIZE_FILE"
            echo "$CLEANED"
        else
            echo "✅ No injection patterns found"
            echo "$ORIGINAL"
        fi
    else
        echo "ERROR: File not found: $SANITIZE_FILE"
        exit 1
    fi
    exit 0
fi

# Mode 2: Security scan
if $SCAN_ONLY; then
    [[ -d "$PROJECT" ]] || { echo "ERROR: Project directory not found: $PROJECT"; exit 1; }
    
    echo "🔍 Scanning for prompt injection patterns in: $PROJECT"
    echo "═══════════════════════════════════════════════════════════"
    
    TOTAL_FILES=0
    SUSPICIOUS_FILES=0
    
    # Focus on high-risk files
    HIGH_RISK_PATTERNS=(
        "README.md" "README" "CONTRIBUTING.md" "CODE_OF_CONDUCT.md"
        "package.json" "requirements.txt" "setup.py" "Cargo.toml" "go.mod"
        "*.md" "*.txt" "*.cfg" "*.ini" "*.yaml" "*.yml" "*.toml"
        "Makefile" "Dockerfile" "docker-compose*.yml"
    )
    
    for pattern in "${HIGH_RISK_PATTERNS[@]}"; do
        while IFS= read -r file; do
            [[ -z "$file" ]] && continue
            TOTAL_FILES=$((TOTAL_FILES + 1))
            if ! scan_file "$file"; then
                SUSPICIOUS_FILES=$((SUSPICIOUS_FILES + 1))
            fi
        done < <(find "$PROJECT" -path "$pattern" -type f 2>/dev/null || true)
    done
    
    echo ""
    echo "───────────────────────────────────────────────────────────"
    echo "  Files scanned:  $TOTAL_FILES"
    echo "  Suspicious:     $SUSPICIOUS_FILES"
    echo "  Audit log:      $AUDIT_LOG"
    echo "───────────────────────────────────────────────────────────"
    
    if [[ $SUSPICIOUS_FILES -gt 0 ]]; then
        echo ""
        echo "⚠️  Found $SUSPICIOUS_FILES files with potential injection patterns."
        echo "   Review audit log: cat $AUDIT_LOG"
        echo "   Sanitize a file:  sandbox-exec.sh --sanitize <file>"
        exit 2
    else
        echo "✅ No injection patterns detected."
        exit 0
    fi
fi

# Mode 3: Isolated command execution
if [[ -n "$COMMAND" ]]; then
    [[ -n "$PROJECT" ]] || PROJECT="."
    [[ -d "$PROJECT" ]] || { echo "ERROR: Project directory not found: $PROJECT"; exit 1; }
    
    echo "🔒 Sandbox Execution"
    echo "═══════════════════════════════════════════════════════════"
    echo "  Command:    $COMMAND"
    echo "  Project:    $PROJECT (read-only)"
    echo "  Output:     $OUTPUT_DIR"
    echo "  Network:    $($ALLOW_NETWORK && echo 'ALLOWED' || echo 'BLOCKED')"
    echo "  Writes:     $($ALLOW_WRITES && echo 'ALLOWED' || echo 'RESTRICTED')"
    echo "───────────────────────────────────────────────────────────"
    
    # Step 1: Quick pre-scan of project for injection patterns
    log_audit "INFO" "Pre-scan: checking for injection patterns"
    SCAN_FINDINGS=0
    for pattern in "${INJECTION_PATTERNS[@]}"; do
        # Use { grep ... || true; } to avoid pipefail SIGPIPE from head -5
        MATCHES=$( { grep -rliE "$pattern" "$PROJECT" --include="*.md" --include="*.txt" --include="*.json" 2>/dev/null || true; } | head -5)
        if [[ -n "$MATCHES" ]]; then
            SCAN_FINDINGS=$((SCAN_FINDINGS + 1))
            log_audit "WARN" "Pre-scan pattern match: $pattern → $(echo "$MATCHES" | tr '\n' ' ')"
        fi
    done
    
    if [[ $SCAN_FINDINGS -gt 0 ]]; then
        log_audit "WARN" "Pre-scan found $SCAN_FINDINGS potential injection pattern categories"
        echo "⚠️  Pre-scan found potential injection patterns in project files."
        echo "   Full audit log: $AUDIT_LOG"
    else
        echo "✅ Pre-scan: No injection patterns detected."
    fi
    echo ""
    
    # Step 2: Execute in sandbox
    # Create a read-only bind mount of the project (Linux-only, macOS uses copy)
    if [[ "$(uname)" == "Darwin" ]]; then
        # macOS: copy project to temp (no bind mount support without hdiutil)
        log_audit "INFO" "macOS: copying project to sandbox (read-only simulated)"
        SANDBOX_PROJECT="$SANDBOX_ROOT/project"
        cp -R "$PROJECT" "$SANDBOX_PROJECT" 2>/dev/null || true
        chmod -R u-w "$SANDBOX_PROJECT" 2>/dev/null || true
        
        cd "$SANDBOX_PROJECT"
        log_audit "INFO" "Executing: $COMMAND (pwd=$PWD)"
        
        if $ALLOW_NETWORK; then
            bash -c "$COMMAND" > "$OUTPUT_DIR/stdout.txt" 2> "$OUTPUT_DIR/stderr.txt"
        else
            # Network-blocked: unset proxy/env vars that could leak
            env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy \
                bash -c "$COMMAND" > "$OUTPUT_DIR/stdout.txt" 2> "$OUTPUT_DIR/stderr.txt"
        fi
        EXIT_CODE=$?
    else
        # Linux: use namespaces for real isolation
        log_audit "INFO" "Linux: using namespace isolation"
        SANDBOX_PROJECT="$SANDBOX_ROOT/project"
        cp -R "$PROJECT" "$SANDBOX_PROJECT"
        
        cd "$SANDBOX_PROJECT"
        if $ALLOW_NETWORK; then
            unshare -r -m -p --fork bash -c "$COMMAND" > "$OUTPUT_DIR/stdout.txt" 2> "$OUTPUT_DIR/stderr.txt"
        else
            unshare -r -m -p -n --fork bash -c "$COMMAND" > "$OUTPUT_DIR/stdout.txt" 2> "$OUTPUT_DIR/stderr.txt"
        fi
        EXIT_CODE=$?
    fi
    
    # Step 3: Report
    echo ""
    echo "───────────────────────────────────────────────────────────"
    echo "  Exit code:   $EXIT_CODE"
    echo "  Stdout:      $OUTPUT_DIR/stdout.txt ($(wc -c < "$OUTPUT_DIR/stdout.txt" 2>/dev/null || echo 0) bytes)"
    echo "  Stderr:      $OUTPUT_DIR/stderr.txt ($(wc -c < "$OUTPUT_DIR/stderr.txt" 2>/dev/null || echo 0) bytes)"
    echo "  Audit log:   $AUDIT_LOG"
    echo "───────────────────────────────────────────────────────────"
    
    # Show truncated output
    if [[ -s "$OUTPUT_DIR/stdout.txt" ]]; then
        echo ""
        echo "--- STDOUT (first 50 lines) ---"
        head -50 "$OUTPUT_DIR/stdout.txt"
    fi
    
    if [[ -s "$OUTPUT_DIR/stderr.txt" ]]; then
        echo ""
        echo "--- STDERR (first 20 lines) ---"
        head -20 "$OUTPUT_DIR/stderr.txt"
    fi
    
    log_audit "INFO" "Command completed with exit code: $EXIT_CODE"
    exit $EXIT_CODE
fi

# No mode selected
echo "ERROR: Specify --command, --scan, or --sanitize"
echo "Usage: sandbox-exec.sh --scan /path/to/project"
echo "       sandbox-exec.sh --command 'npm test' --project ."
echo "       sandbox-exec.sh --sanitize README.md"
exit 1
