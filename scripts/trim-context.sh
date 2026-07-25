#!/usr/bin/env bash
# ==============================================================================
# trim-context.sh — Dynamic Token Trimmer for Context Window Pressure
# ==============================================================================
# Intelligently strips lower-priority sections when context window pressure
# exceeds target budget. Uses semantic section classification — keeps ground
# rules, verification guardrails, and error recovery intact while dropping
# or compacting practice exercises, verbose examples, and routing maps.
#
# Priority Tiers:
#   Tier 1 (NEVER strip): Ground Rules, Verification, Error Recovery
#   Tier 2 (compact under pressure): Deliberate Practice, L4-L5, routing maps
#   Tier 3 (drop first): Extended examples, verbose refs, anti-patterns
#
# Usage:
#   trim-context.sh --file skill.md --budget 3000 [--json] [--quiet]
#   cat skill.md | trim-context.sh --stdin --budget 2500
# ==============================================================================
set -euo pipefail

INPUT_FILE=""
STDIN=false
BUDGET=3000
JSON=false
QUIET=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --file) INPUT_FILE="$2"; shift 2 ;;
        --stdin) STDIN=true; shift ;;
        --budget) BUDGET="$2"; shift 2 ;;
        --json) JSON=true; shift ;;
        --quiet) QUIET=true; shift ;;
        -h|--help) 
            sed -n '2,30p' "$0" | grep -v '^#' | head -20
            exit 0 ;;
        *) echo "ERROR: $1"; exit 1 ;;
    esac
done

# Read content
if $STDIN; then CONTENT=$(cat); else CONTENT=$(cat "$INPUT_FILE"); fi

INPUT_CHARS=$(echo "$CONTENT" | wc -c | tr -d ' ')
INPUT_LINES=$(echo "$CONTENT" | wc -l | tr -d ' ')
EST_TOKENS=$((INPUT_CHARS / 4))

# ─── Section classification ──────────────────────────────────────────────────
# Single-pass awk: classify each ## section and decide keep/compact/drop

TIER1="Ground Rules|Verification|Error Recovery|Anti-Hallucination"
TIER3="References|Anti-Patterns|Changelog|Appendix|Footnotes|Glossary|See Also|Further Reading"

TRIM_LEVEL=0
if [[ $EST_TOKENS -gt $BUDGET ]]; then
    # Determine how aggressively to trim
    OVERAGE=$((EST_TOKENS - BUDGET))
    OVERAGE_PCT=$((OVERAGE * 100 / EST_TOKENS))
    if [[ $OVERAGE_PCT -le 20 ]]; then TRIM_LEVEL=1
    elif [[ $OVERAGE_PCT -le 50 ]]; then TRIM_LEVEL=2
    else TRIM_LEVEL=3; fi
fi

# ─── Trimming engine (awk) ───────────────────────────────────────────────────
# awk classifies each section at ## heading boundaries and applies trim rules

TRIMMED=$(echo "$CONTENT" | awk -v tier1="$TIER1" -v tier3="$TIER3" -v trim="$TRIM_LEVEL" '
BEGIN { 
    in_section=0; section_tier=2; section_lines=0; section=""; heading="";
    kept=0; compacted=0; dropped=0; output="";
}
function classify(h) {
    if (h ~ tier1) return 1;
    if (h ~ tier3) return 3;
    return 2;
}
function flush_section() {
    if (heading == "") { output = output section; return; }
    tier = classify(heading);
    
    if (tier == 1) {
        # Tier 1: Keep (or compact at trim level 3)
        if (trim >= 3 && heading !~ /Ground Rules|Error Recovery/) {
            # Ultra-compact: heading + first 2 non-empty lines
            output = output heading "\n";
            lines = split(section, arr, "\n");
            added = 0;
            for (i = 2; i <= lines && added < 3; i++) {
                if (arr[i] !~ /^[[:space:]]*$/) {
                    output = output arr[i] "\n"; added++;
                }
            }
            output = output "<!-- Trimmed L3 -->\n\n";
            compacted++;
        } else {
            output = output section;
            kept++;
        }
    } else if (tier == 3) {
        # Tier 3: Drop at trim level 1+, keep heading only
        if (trim >= 1) {
            output = output heading "\n<!-- Trimmed: see full SKILL.md -->\n\n";
            dropped++;
        } else {
            output = output section;
            kept++;
        }
    } else {
        # Tier 2: Compact at trim level 2+, drop body at 3
        if (trim >= 3) {
            output = output heading "\n<!-- Trimmed L3 -->\n\n";
            dropped++;
        } else if (trim >= 2) {
            output = output heading "\n";
            lines = split(section, arr, "\n");
            added = 0;
            for (i = 2; i <= lines && added < 2; i++) {
                if (arr[i] !~ /^[[:space:]]*$/ && arr[i] !~ /^<!--/) {
                    output = output arr[i] "\n"; added++;
                }
            }
            output = output "<!-- Trimmed L2 -->\n\n";
            compacted++;
        } else {
            output = output section;
            kept++;
        }
    }
    section = ""; heading = ""; section_lines = 0;
}
/^## [A-Z]/ {
    flush_section();
    heading = $0;
    section = $0 "\n";
    in_section = 1; section_lines = 1;
    next;
}
{
    if (in_section) { section = section $0 "\n"; section_lines++; }
    else { section = section $0 "\n"; }
}
END {
    flush_section();
    print output;
    # Stats to stderr
    printf("trim_level=%d kept=%d compacted=%d dropped=%d\n", trim, kept, compacted, dropped) > "/dev/stderr";
}
')

# ─── Calculate savings ───────────────────────────────────────────────────────
FINAL_CHARS=$(echo "$TRIMMED" | wc -c | tr -d ' ')
FINAL_TOKENS=$((FINAL_CHARS / 4))
SAVED=$((EST_TOKENS - FINAL_TOKENS))
SAVED_PCT=0
[[ $EST_TOKENS -gt 0 ]] && SAVED_PCT=$((SAVED * 100 / EST_TOKENS))

# Read awk stats
STATS=$(echo "$TRIMMED" 2>&1 >/dev/null; echo "")

# ─── Output ──────────────────────────────────────────────────────────────────
if $JSON; then
    echo "{\"original_tokens\":$EST_TOKENS,\"final_tokens\":$FINAL_TOKENS,\"saved\":$SAVED,\"saved_pct\":$SAVED_PCT,\"trim_level\":$TRIM_LEVEL,\"within_budget\":$([[ $FINAL_TOKENS -le $BUDGET ]] && echo true || echo false)}"
else
    if ! $QUIET; then
        echo "╔══════════════════════════════════════════════════════════╗" >&2
        echo "║          CONTEXT WINDOW TRIM AUDIT                      ║" >&2
        echo "╚══════════════════════════════════════════════════════════╝" >&2
        echo "" >&2
        echo "📊 TOKEN BUDGET" >&2
        echo "   Original: ~${EST_TOKENS}t  (${INPUT_LINES} lines)" >&2
        echo "   Target:   ${BUDGET}t" >&2
        echo "   Final:    ~${FINAL_TOKENS}t  (saved ${SAVED}t, ${SAVED_PCT}%)" >&2
        echo "   Level:    ${TRIM_LEVEL} (1=drop refs, 2=compact Tier2, 3=ultra-compact)" >&2
        if [[ $FINAL_TOKENS -gt $BUDGET ]]; then
            echo "   ⚠️  Still over by ~$((FINAL_TOKENS - BUDGET))t — consider splitting skill" >&2
        else
            echo "   ✅ Within budget" >&2
        fi
        echo "" >&2
    fi
    echo "$TRIMMED"
fi

[[ $FINAL_TOKENS -le $BUDGET ]] && exit 0 || exit 1
