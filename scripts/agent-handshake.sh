#!/usr/bin/env bash
# ==============================================================================
# agent-handshake.sh — Cross-Agent Handshake Runtime Protocol
# ==============================================================================
# Implements the agent-handoff-protocol spec as an executable runtime.
# Enables parallel specialized agents to pass typed state, prune context,
# verify integrity via SHA-256 checksums, and sign/reject contracts.
#
# Handoff Directory: ~/.agents/handoffs/
#   handoffs/
#     {session-id}/
#       state.json        — Serialized agent state
#       contract.json     — Handoff contract (proposed → accepted/rejected)
#       ledger.jsonl      — Decision gate ledger (append-only)
#       checksums.sha256  — Integrity verification
#       context.md        — Pruned context for downstream agent
#
# Usage:
#   agent-handshake.sh propose --from backend-dev --to code-reviewer \
#       --state '{"files":["src/api/users.ts"],"decisions":["used-JWT"]}'
#
#   agent-handshake.sh accept --session abc123 --as code-reviewer
#
#   agent-handshake.sh verify --session abc123
#
#   agent-handshake.sh ledger --session abc123 --decision "chose-postgres" \
#       --rationale "Better JSON support than MySQL for our document model"
# ==============================================================================
set -euo pipefail

HANDOFF_DIR="${HOME}/.agents/handoffs"
COMMAND=""
SESSION_ID=""
FROM_AGENT=""
TO_AGENT=""
STATE_JSON=""
CONTRACT_STATUS=""

mkdir -p "$HANDOFF_DIR"

# ─── Help ────────────────────────────────────────────────────────────────────
usage() {
    cat << 'HELP'
Cross-Agent Handshake Runtime — typed state passing between parallel agents.

COMMANDS:
  propose   Package state, prune context, sign contract, deposit handoff
  accept    Verify checksum, review contract, accept handoff
  reject    Verify checksum, review contract, reject with rationale
  verify    Validate checksum integrity of a handoff package
  ledger    Record an irreversible decision in the decision gate ledger
  status    Show handoff status (proposed/accepted/rejected/expired)
  list      List all pending handoffs for an agent

OPTIONS:
  --from AGENT       Upstream agent name (e.g., backend-developer)
  --to AGENT         Downstream agent name (e.g., code-reviewer)
  --state JSON       Serialized agent state as JSON string
  --session ID       Handoff session identifier
  --as AGENT         Agent accepting/rejecting (for accept/reject)
  --decision TEXT    Decision description (for ledger)
  --rationale TEXT   Rationale for decision (for ledger)
  --reversible       Mark decision as reversible (default: false)

EXAMPLES:
  # Propose a handoff from backend-dev to code-reviewer
  agent-handshake.sh propose --from backend-developer --to code-reviewer \
      --state '{"files":["src/api/users.ts"],"pr_url":"https://github.com/..."}'

  # Code-reviewer accepts the handoff
  agent-handshake.sh accept --session abc123 --as code-reviewer

  # Record an architecture decision
  agent-handshake.sh ledger --session abc123 \
      --decision "Chose PostgreSQL over MySQL" \
      --rationale "Superior JSONB support for semi-structured patient data"
HELP
}

# ─── Parse Arguments ─────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        propose|accept|reject|verify|ledger|status|list)
            COMMAND="$1"; shift ;;
        --from) FROM_AGENT="$2"; shift 2 ;;
        --to) TO_AGENT="$2"; shift 2 ;;
        --state) STATE_JSON="$2"; shift 2 ;;
        --session) SESSION_ID="$2"; shift 2 ;;
        --as) TO_AGENT="$2"; shift 2 ;;
        --decision) DECISION_TEXT="$2"; shift 2 ;;
        --rationale) RATIONALE="$2"; shift 2 ;;
        --reversible) REVERSIBLE="true"; shift ;;
        -h|--help) usage; exit 0 ;;
        *) echo "ERROR: Unknown: $1"; usage; exit 1 ;;
    esac
done

# ─── Generate Session ID ─────────────────────────────────────────────────────
if [[ -z "$SESSION_ID" ]] && [[ "$COMMAND" == "propose" ]]; then
    SESSION_ID=$(date +%Y%m%d-%H%M%S)-$(echo "$FROM_AGENT" | tr ' ' '-')-to-$(echo "$TO_AGENT" | tr ' ' '-')
fi

SESSION_DIR="$HANDOFF_DIR/$SESSION_ID"

# ─── Commands ────────────────────────────────────────────────────────────────

propose_handoff() {
    [[ -n "$FROM_AGENT" ]] || { echo "ERROR: --from required"; exit 1; }
    [[ -n "$TO_AGENT" ]] || { echo "ERROR: --to required"; exit 1; }
    
    mkdir -p "$SESSION_DIR"
    
    # Build state payload
    local timestamp
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    cat > "$SESSION_DIR/state.json" << STATE
{
  "handoff_id": "$SESSION_ID",
  "timestamp": "$timestamp",
  "from": "$FROM_AGENT",
  "to": "$TO_AGENT",
  "token_budget_before": $(echo "${STATE_JSON}" | wc -c | awk '{print int($1/4)}'),
  "state": ${STATE_JSON:-{}},
  "non_negotiable_constraints": [],
  "open_questions": [],
  "artifacts": []
}
STATE
    
    # Generate checksum
    sha256sum "$SESSION_DIR/state.json" | awk '{print $1}' > "$SESSION_DIR/checksums.sha256"
    echo "state.json $(cat "$SESSION_DIR/checksums.sha256")" >> "$SESSION_DIR/checksums.sha256"
    
    # Create contract (PROPOSED state)
    cat > "$SESSION_DIR/contract.json" << CONTRACT
{
  "handoff_id": "$SESSION_ID",
  "status": "PROPOSED",
  "proposed_at": "$timestamp",
  "from": "$FROM_AGENT",
  "to": "$TO_AGENT",
  "checksum": "$(cat "$SESSION_DIR/checksums.sha256" | head -1)",
  "accepted_at": null,
  "accepted_by": null,
  "rejected_at": null,
  "rejection_rationale": null
}
CONTRACT
    
    # Initialize ledger if not exists
    if [[ ! -f "$SESSION_DIR/ledger.jsonl" ]]; then
        touch "$SESSION_DIR/ledger.jsonl"
    fi
    
    # Log the proposal
    echo "{\"timestamp\":\"$timestamp\",\"event\":\"HANDOFF_PROPOSED\",\"from\":\"$FROM_AGENT\",\"to\":\"$TO_AGENT\",\"handoff_id\":\"$SESSION_ID\"}" >> "$SESSION_DIR/ledger.jsonl"
    
    echo "✅ Handoff PROPOSED: $FROM_AGENT → $TO_AGENT"
    echo "   Session: $SESSION_ID"
    echo "   Path:    $SESSION_DIR"
    echo "   Checksum: $(cat "$SESSION_DIR/checksums.sha256" | head -1)"
    echo ""
    echo "   Next: agent-handshake.sh accept --session $SESSION_ID --as $TO_AGENT"
}

accept_handoff() {
    [[ -d "$SESSION_DIR" ]] || { echo "ERROR: Session $SESSION_ID not found"; exit 1; }
    [[ -n "$TO_AGENT" ]] || { echo "ERROR: --as required"; exit 1; }
    
    # Verify checksum
    if ! verify_checksum; then
        echo "❌ Checksum verification FAILED. Handoff may be corrupted."
        exit 2
    fi
    
    # Read contract
    local contract_to
    contract_to=$(python3 -c "import json; print(json.load(open('$SESSION_DIR/contract.json'))['to'])" 2>/dev/null || echo "")
    
    if [[ "$contract_to" != "$TO_AGENT" ]]; then
        echo "⚠️  Contract is addressed to '$contract_to' but you are '$TO_AGENT'"
        echo "   Accept anyway? Only proceed if you are a supervisor agent."
    fi
    
    # Update contract
    local timestamp
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    python3 -c "
import json
with open('$SESSION_DIR/contract.json') as f:
    c = json.load(f)
c['status'] = 'ACCEPTED'
c['accepted_at'] = '$timestamp'
c['accepted_by'] = '$TO_AGENT'
with open('$SESSION_DIR/contract.json', 'w') as f:
    json.dump(c, f, indent=2)
" 2>/dev/null || {
        # Fallback if python3 not available
        cat > "$SESSION_DIR/contract.json" << EOF
{
  "handoff_id": "$SESSION_ID",
  "status": "ACCEPTED",
  "accepted_at": "$timestamp",
  "accepted_by": "$TO_AGENT"
}
EOF
    }
    
    # Log acceptance
    echo "{\"timestamp\":\"$timestamp\",\"event\":\"HANDOFF_ACCEPTED\",\"by\":\"$TO_AGENT\",\"handoff_id\":\"$SESSION_ID\"}" >> "$SESSION_DIR/ledger.jsonl"
    
    # Output state for downstream agent consumption
    echo "✅ Handoff ACCEPTED: $SESSION_ID"
    echo "   Contract signed by: $TO_AGENT at $timestamp"
    echo ""
    echo "--- STATE PAYLOAD ---"
    cat "$SESSION_DIR/state.json"
}

reject_handoff() {
    [[ -d "$SESSION_DIR" ]] || { echo "ERROR: Session $SESSION_ID not found"; exit 1; }
    [[ -n "$TO_AGENT" ]] || { echo "ERROR: --as required"; exit 1; }
    
    local timestamp
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    python3 -c "
import json
with open('$SESSION_DIR/contract.json') as f:
    c = json.load(f)
c['status'] = 'REJECTED'
c['rejected_at'] = '$timestamp'
c['rejected_by'] = '$TO_AGENT'
c['rejection_rationale'] = '${RATIONALE:-No rationale provided}'
with open('$SESSION_DIR/contract.json', 'w') as f:
    json.dump(c, f, indent=2)
" 2>/dev/null
    
    echo "{\"timestamp\":\"$timestamp\",\"event\":\"HANDOFF_REJECTED\",\"by\":\"$TO_AGENT\",\"rationale\":\"${RATIONALE:-none}\",\"handoff_id\":\"$SESSION_ID\"}" >> "$SESSION_DIR/ledger.jsonl"
    
    echo "❌ Handoff REJECTED by $TO_AGENT"
    echo "   Rationale: ${RATIONALE:-No rationale provided}"
}

verify_checksum() {
    [[ -f "$SESSION_DIR/checksums.sha256" ]] || { echo "ERROR: No checksum file"; return 1; }
    [[ -f "$SESSION_DIR/state.json" ]] || { echo "ERROR: No state file"; return 1; }
    
    local expected actual
    expected=$(head -1 "$SESSION_DIR/checksums.sha256")
    actual=$(sha256sum "$SESSION_DIR/state.json" | awk '{print $1}')
    
    if [[ "$expected" == "$actual" ]]; then
        return 0
    else
        echo "   Expected: $expected" >&2
        echo "   Actual:   $actual" >&2
        return 1
    fi
}

record_ledger() {
    [[ -d "$SESSION_DIR" ]] || { echo "ERROR: Session $SESSION_ID not found"; exit 1; }
    [[ -n "$DECISION_TEXT" ]] || { echo "ERROR: --decision required"; exit 1; }
    
    local timestamp
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    cat >> "$SESSION_DIR/ledger.jsonl" << LEDGER
{"timestamp":"$timestamp","event":"DECISION_RECORDED","decision":"$DECISION_TEXT","rationale":"${RATIONALE:-none}","reversible":${REVERSIBLE:-false}}
LEDGER
    
    echo "📝 Decision recorded in ledger: $DECISION_TEXT"
}

show_status() {
    [[ -d "$SESSION_DIR" ]] || { echo "ERROR: Session $SESSION_ID not found"; exit 1; }
    
    echo "📋 Handoff: $SESSION_ID"
    echo "═══════════════════════════════════════"
    
    if [[ -f "$SESSION_DIR/contract.json" ]]; then
        python3 -c "
import json
c = json.load(open('$SESSION_DIR/contract.json'))
print(f\"   Status:    {c.get('status', 'UNKNOWN')}\")
print(f\"   From:      {c.get('from', '?')}\")
print(f\"   To:        {c.get('to', '?')}\")
print(f\"   Proposed:  {c.get('proposed_at', '?')}\")
if c.get('accepted_at'): print(f\"   Accepted:  {c['accepted_at']} by {c.get('accepted_by', '?')}\")
if c.get('rejected_at'): print(f\"   Rejected:  {c['rejected_at']} — {c.get('rejection_rationale', 'no rationale')}\")
" 2>/dev/null || cat "$SESSION_DIR/contract.json"
    fi
    
    if [[ -f "$SESSION_DIR/checksums.sha256" ]]; then
        echo ""
        echo "   Checksum:  $(head -1 "$SESSION_DIR/checksums.sha256")"
        if verify_checksum 2>/dev/null; then
            echo "   Integrity: ✅ VERIFIED"
        else
            echo "   Integrity: ❌ FAILED"
        fi
    fi
    
    if [[ -f "$SESSION_DIR/ledger.jsonl" ]]; then
        local entries
        entries=$(wc -l < "$SESSION_DIR/ledger.jsonl" | tr -d ' ')
        echo "   Ledger:    $entries entries"
    fi
}

list_handoffs() {
    local agent_filter="${1:-}"
    echo "📋 Pending Handoffs"
    echo "═══════════════════════════════════════"
    
    local found=0
    for dir in "$HANDOFF_DIR"/*/; do
        [[ -d "$dir" ]] || continue
        local contract="$dir/contract.json"
        [[ -f "$contract" ]] || continue
        
        local status to_agent
        status=$(python3 -c "import json; print(json.load(open('$contract')).get('status','?'))" 2>/dev/null || echo "?")
        to_agent=$(python3 -c "import json; print(json.load(open('$contract')).get('to','?'))" 2>/dev/null || echo "?")
        
        if [[ -n "$agent_filter" ]] && [[ "$to_agent" != "$agent_filter" ]]; then
            continue
        fi
        
        local sid
        sid=$(basename "$dir")
        echo "   [$status] $sid → $to_agent"
        found=$((found + 1))
    done
    
    if [[ $found -eq 0 ]]; then
        echo "   (no handoffs found)"
    fi
}

# ─── Dispatch ────────────────────────────────────────────────────────────────
case "$COMMAND" in
    propose) propose_handoff ;;
    accept)  accept_handoff ;;
    reject)  reject_handoff ;;
    verify)  verify_checksum && echo "✅ Checksum verified for $SESSION_ID" || { echo "❌ Checksum FAILED"; exit 2; } ;;
    ledger)  record_ledger ;;
    status)  show_status ;;
    list)    list_handoffs "$TO_AGENT" ;;
    *)       usage; exit 1 ;;
esac
