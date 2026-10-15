#!/usr/bin/env bash
# ============================================================================
# verify-skill.sh — self-verification for options-trading-playbook
# ============================================================================
# Structural, provenance, gate, arithmetic, determinism and reference-integrity
# checks for this skill. Bash 3.2 compatible, no third-party dependencies, no
# network. Exits 0 when every check passes, 1 otherwise.
#
# The three checks that make this script more than a lint:
#   (a) it runs payoff_check.py on every documented card and asserts the values
#       DOCUMENTED IN THIS SKILL AND IN examples/checks/, so the documented
#       arithmetic and the shipped code cannot drift apart;
#   (b) it asserts the checker is DETERMINISTIC by running it twice per command
#       and diffing text, JSON and CSV;
#   (c) it FAILS on an orphaned reference file — a references/*.md that is not
#       linked from SKILL.md.
#
# Usage: bash scripts/verify-skill.sh
# ============================================================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
SKILL_NAME="$(basename "$SKILL_DIR")"
REF_DIR="$SKILL_DIR/references"
EX_DIR="$SKILL_DIR/examples"
CHECK_DIR="$EX_DIR/checks"
LOG_DIR="$EX_DIR/logs"
ENGINE="$SKILL_DIR/scripts/payoff_check.py"
GEN="$LOG_DIR/generate_synthetic_log.py"
SYN_LOG="$LOG_DIR/synthetic-options-log.csv"

# python3 is not guaranteed on PATH on every host; py -3 is the Windows launcher.
PY=""
for cand in python3 py; do
  if command -v "$cand" >/dev/null 2>&1; then
    if [[ "$cand" == "py" ]]; then
      if py -3 -c 'import sys' >/dev/null 2>&1; then PY="py -3"; break; fi
    else
      if "$cand" -c 'import sys' >/dev/null 2>&1; then PY="$cand"; break; fi
    fi
  fi
done
if [[ -z "$PY" ]]; then
  echo "FAIL: no working Python 3 interpreter found (tried python3, py -3)"
  exit 1
fi

export PYTHONIOENCODING=utf-8
TMP="$(mktemp -d 2>/dev/null || mktemp -d -t optplay)"
trap 'rm -rf "$TMP"' EXIT

FAILURES=0
CHECKS=0

pass() { echo "  [PASS] $1"; CHECKS=$((CHECKS + 1)); }
fail() { echo "  [FAIL] $1"; CHECKS=$((CHECKS + 1)); FAILURES=$((FAILURES + 1)); }

count_matches() {
  # $1 = extended regex, $2 = file, $3 = optional -i
  local n
  if [[ "${3:-}" == "-i" ]]; then
    n=$(grep -oiE "$1" "$2" 2>/dev/null | wc -l | tr -d ' ')
  else
    n=$(grep -oE "$1" "$2" 2>/dev/null | wc -l | tr -d ' ')
  fi
  echo "${n:-0}"
}

count_lines() { wc -l < "$1" | tr -d ' '; }

check_section() {
  if grep -q "^## $1\$" "$SKILL_MD" 2>/dev/null; then
    pass "Section: $1"
  else
    fail "Section: $1 — MISSING or not an exact level-2 heading"
  fi
}

check_ge() {
  if [[ "$2" -ge "$3" ]] 2>/dev/null; then
    pass "$1: $2 (minimum $3)"
  else
    fail "$1: $2 (need at least $3)"
  fi
}

# assert_engine_value <label> <output-file> <exact-token-that-must-appear>
assert_engine_value() {
  local label="$1" file="$2" token="$3"
  if grep -qF -- "$token" "$file" 2>/dev/null; then
    pass "arith: $label"
  else
    fail "arith MISSING from engine output: $label (looked for: $token)"
  fi
}

# assert_no_value <label> <output-file> <token-that-must-NOT-appear>
assert_no_value() {
  local label="$1" file="$2" token="$3"
  if grep -qF -- "$token" "$file" 2>/dev/null; then
    fail "negative control FAILED: $label (token present: $token)"
  else
    pass "negative control: $label"
  fi
}

# assert_json_field <label> <json-file> <dotted-path> <expected> [tolerance]
# Reads one scalar out of the engine's --json payload by dotted path so a value
# is asserted by NAME rather than by its column position in a padded table.
assert_json_field() {
  local label="$1" file="$2" path="$3" expect="$4" tol="${5:-0.0000005}"
  local got
  got=$($PY - "$file" "$path" <<'PYEOF'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as fh:
    node = json.load(fh)
for part in sys.argv[2].split("."):
    if node is None:
        break
    if isinstance(node, list):
        try:
            node = node[int(part)]
        except (ValueError, IndexError):
            node = None
    elif isinstance(node, dict):
        node = node.get(part)
    else:
        node = None
if node is None:
    print("n/a")
elif isinstance(node, bool):
    print("yes" if node else "no")
else:
    print(node)
PYEOF
)
  if [[ "$got" == "$expect" ]]; then
    pass "arith: $label"
    return 0
  fi
  if [[ "$got" =~ ^-?[0-9] && "$expect" =~ ^-?[0-9] ]]; then
    if awk -v a="$got" -v b="$expect" -v t="$tol" 'BEGIN{d=a-b; if(d<0)d=-d; exit !(d<=t)}'; then
      pass "arith: $label"
      return 0
    fi
  fi
  fail "arith FAILED: $label (wanted $path = $expect, got $got)"
}

echo "=== Verifying $SKILL_NAME ==="
echo "  interpreter: $PY"
echo ""

# ── Block A: File existence ───────────────────────────────────────────────
echo "--- File Existence ---"
[[ -f "$SKILL_MD" ]] && pass "SKILL.md exists" || { fail "SKILL.md not found"; exit 1; }
[[ -d "$REF_DIR" ]] && pass "references/ directory exists" || fail "references/ directory MISSING"
[[ -d "$EX_DIR" ]] && pass "examples/ directory exists" || fail "examples/ directory MISSING"
[[ -d "$CHECK_DIR" ]] && pass "examples/checks/ directory exists" || fail "examples/checks/ MISSING"
[[ -d "$LOG_DIR" ]] && pass "examples/logs/ directory exists" || fail "examples/logs/ MISSING"
[[ -f "$ENGINE" ]] && pass "checker exists: scripts/payoff_check.py" || fail "checker MISSING: scripts/payoff_check.py"
[[ -f "$GEN" ]] && pass "seeded generator exists" || fail "seeded generator MISSING"
[[ -f "$SYN_LOG" ]] && pass "SYNTHETIC log exists" || fail "SYNTHETIC log MISSING"
[[ -f "$EX_DIR/strategy-cards.md" ]] && pass "examples/strategy-cards.md exists" || fail "examples/strategy-cards.md MISSING"
[[ -f "$EX_DIR/README.md" ]] && pass "examples/README.md exists" || fail "examples/README.md MISSING"
[[ -f "$EX_DIR/run-output.txt" ]] && pass "examples/run-output.txt exists" || fail "examples/run-output.txt MISSING"
[[ -x "$SKILL_DIR/scripts/verify-skill.sh" ]] && pass "verify-skill.sh is executable" || fail "verify-skill.sh is NOT executable (chmod +x)"

# ── Block B: Required level-2 sections (23 + Anti-Hallucination) ───────────
echo ""
echo "--- Required Sections (23 + Anti-Hallucination) ---"
check_section "Route the Request"
check_section "Anti-Rationalization"
check_section "Ground Rules"
check_section "The Expert's Mindset"
check_section "Deliberate Practice"
check_section "Operating at Different Levels"
check_section "When to Use"
check_section "When NOT to Use"
check_section "Decision Trees"
check_section "Core Workflow"
check_section "Best Practices"
check_section "Error Decoder"
check_section "Error Recovery"
check_section "Cross-Skill Coordination"
check_section "Proactive Triggers"
check_section "Anti-Patterns"
check_section "State Log"
check_section "Production Checklist"
check_section "What Good Looks Like"
check_section "Verification Guardrails"
check_section "References"
check_section "Gotchas"
check_section "Anti-Hallucination"

# ── Block C: Frontmatter ───────────────────────────────────────────────────
echo ""
echo "--- YAML Frontmatter ---"
NAME_FIELD=$(grep -m1 '^name:' "$SKILL_MD" 2>/dev/null | awk '{print $2}' || true)
if [[ "$NAME_FIELD" == "$SKILL_NAME" ]]; then
  pass "name '$NAME_FIELD' matches directory '$SKILL_NAME'"
else
  fail "name '$NAME_FIELD' does not match directory '$SKILL_NAME'"
fi
for field in description license author type status version updated token_budget tags; do
  if grep -q "^$field:" "$SKILL_MD" 2>/dev/null; then
    pass "frontmatter field: $field"
  else
    fail "frontmatter field missing: $field"
  fi
done
for field in consumes_from feeds_into examples; do
  if grep -q "$field" "$SKILL_MD" 2>/dev/null; then
    pass "chain.$field present"
  else
    fail "chain.$field MISSING"
  fi
done
if grep -q 'consumes_from: \[options-strategist, trade-sizing-recovery, edge-and-payoff-engineering\]' "$SKILL_MD" 2>/dev/null; then
  pass "chain.consumes_from is exactly the required block"
else
  fail "chain.consumes_from is not the required exact block"
fi
if grep -q 'feeds_into: \[options-position-lifecycle\]' "$SKILL_MD" 2>/dev/null; then
  pass "chain.feeds_into is exactly [options-position-lifecycle]"
else
  fail "chain.feeds_into is not the required exact block"
fi
if grep -q 'skills/14-finance/options-trading-playbook/examples/checks' "$SKILL_MD" 2>/dev/null; then
  pass "chain.examples path points at this skill's checks directory"
else
  fail "chain.examples path missing or wrong"
fi
DESC_LEN=$($PY - "$SKILL_MD" <<'PYEOF'
import re, sys
with open(sys.argv[1], encoding="utf-8") as fh:
    text = fh.read()
parts = re.split(r'^---\s*$', text, maxsplit=2, flags=re.MULTILINE)
fm = parts[1]
m = re.search(r'^description:\s*>?\s*\n((?:[ \t]+.*\n)+)', fm, re.MULTILINE)
if not m:
    m = re.search(r'^description:\s*(.+)$', fm, re.MULTILINE)
    print(len(m.group(1).strip()) if m else 0)
else:
    print(len(" ".join(l.strip() for l in m.group(1).splitlines() if l.strip())))
PYEOF
)
if [[ "${DESC_LEN:-0}" -gt 0 && "${DESC_LEN:-0}" -le 1024 ]]; then
  pass "description length ${DESC_LEN} chars (limit 1024)"
else
  fail "description length ${DESC_LEN} chars — must be 1..1024"
fi
for trigger in 'Use when' 'Handles' 'Do NOT use'; do
  if grep -q "$trigger" "$SKILL_MD" 2>/dev/null; then
    pass "description carries the '$trigger' trigger phrase"
  else
    fail "description missing the '$trigger' trigger phrase"
  fi
done
for word in 'credit spreads' 'selling premium' 'win rate do I need' 'buy or sell options' 'profitable' 'book is flat' 'options-strategist'; do
  if grep -qi "$word" "$SKILL_MD" 2>/dev/null; then
    pass "description triggers on the owner's words: $word"
  else
    fail "description does not trigger on: $word"
  fi
done

# ── Block D: Structure and quality gates ───────────────────────────────────
echo ""
echo "--- Content Quality ---"

DT_COUNT=$(sed -n '/^## Decision Trees/,/^## Core Workflow/p' "$SKILL_MD" | grep -c '^### ' || true)
check_ge "Decision tree sub-headings" "${DT_COUNT:-0}" 3

DT_GLYPHS=$(sed -n '/^## Decision Trees/,/^## Core Workflow/p' "$SKILL_MD" | grep -oE '├|└|│|┌|→|▼' | wc -l | tr -d ' ')
check_ge "Decision tree branch glyphs" "${DT_GLYPHS:-0}" 8

DT_FENCES=$(sed -n '/^## Decision Trees/,/^## Core Workflow/p' "$SKILL_MD" | grep -c '^```' || true)
check_ge "Decision tree code fences" "${DT_FENCES:-0}" 2

check_ge "Dollar figures" "$(count_matches '\$[0-9][0-9,]*' "$SKILL_MD")" 5
check_ge "QUICK markers" "$(count_matches 'QUICK: 30s' "$SKILL_MD")" 3
check_ge "STANDARD markers" "$(count_matches 'STANDARD: 3min' "$SKILL_MD")" 1
check_ge "DEEP markers" "$(count_matches 'DEEP: 10' "$SKILL_MD")" 1
check_ge "'Complete when' statements" "$(count_matches 'Complete when' "$SKILL_MD")" 8

if grep -q "Mechanical Trigger" "$SKILL_MD"; then pass "Ground Rules: Mechanical Trigger column"; else fail "Ground Rules: Missing Mechanical Trigger column"; fi
if grep -q "Violation Response" "$SKILL_MD"; then pass "Ground Rules: Violation Response column"; else fail "Ground Rules: Missing Violation Response column"; fi
if grep -q '^| Upstream Skill |' "$SKILL_MD"; then pass "Cross-Skill Coordination: Upstream table header"; else fail "Cross-Skill Coordination: missing '| Upstream Skill |' table"; fi
if grep -q '^### Downstream' "$SKILL_MD"; then pass "Cross-Skill Coordination: Downstream table present"; else fail "Cross-Skill Coordination: Downstream table missing"; fi
if grep -q "Portability target" "$SKILL_MD"; then pass "Portability target declared"; else fail "Missing Portability target declaration"; fi

BP_COUNT=$(sed -n '/^## Best Practices/,/^## Error Decoder/p' "$SKILL_MD" | grep -cE '^[0-9]+\. ' || true)
check_ge "Best Practices numbered items" "${BP_COUNT:-0}" 10

CR_COUNT=$(sed -n '/^## Production Checklist/,/^## What Good Looks Like/p' "$SKILL_MD" | grep -oE 'CR[0-9]+' | wc -l | tr -d ' ')
check_ge "Production Checklist CR items" "${CR_COUNT:-0}" 10

AP_COUNT=$(sed -n '/^## Anti-Patterns/,/^## State Log/p' "$SKILL_MD" | grep -c '❌' || true)
check_ge "Anti-Patterns entries" "${AP_COUNT:-0}" 5

ED_COLS=$(sed -n '/^## Error Decoder/,/^## Error Recovery/p' "$SKILL_MD" | grep -m1 '^|' | awk -F'|' '{print NF-2}')
check_ge "Error Decoder columns" "${ED_COLS:-0}" 4

# ── Block E: Anti-hallucination guardrails ─────────────────────────────────
echo ""
echo "--- Anti-Hallucination ---"
for phrase in "Admit uncertainty" "Flag your knowledge cutoff" "Never guess security" "\[VERIFIED\]"; do
  if grep -q "$phrase" "$SKILL_MD" 2>/dev/null; then
    pass "guardrail phrase present: $(echo "$phrase" | sed 's/\\//g')"
  else
    fail "guardrail phrase MISSING: $phrase"
  fi
done
if grep -q '^## Anti-Hallucination$' "$SKILL_MD"; then
  pass "Anti-Hallucination is a level-2 heading"
else
  fail "Anti-Hallucination heading must be exactly '## Anti-Hallucination'"
fi
if grep -qi 'knowledge cutoff' "$SKILL_MD"; then pass "knowledge cutoff declared"; else fail "knowledge cutoff not declared"; fi

# ── Block F: Provenance and citation discipline ────────────────────────────
echo ""
echo "--- Provenance & Citations ---"
PROV_LINES=$(grep -cE '\[VERIFIED|\[COMPUTED|\[ESTIMATED|\[ILLUSTRATIVE|\[COMMON-PRACTICE' "$SKILL_MD" || true)
check_ge "Lines carrying a provenance tag" "${PROV_LINES:-0}" 9

CITE=$(count_matches 'source.*:|data from|verified against|CBOE|Cboe|OCC|Yahoo Finance|Bloomberg|published by|exchange rules|exchange fee|contract specifications' "$SKILL_MD" -i)
check_ge "Research citations (source lines and named sources)" "${CITE:-0}" 8

if grep -q 'ILLUSTRATIVE' "$SKILL_MD" && grep -q 'SYNTHETIC' "$SKILL_MD"; then
  pass "the synthetic log is labelled SYNTHETIC / ILLUSTRATIVE in the doc"
else
  fail "the synthetic log is not labelled in SKILL.md"
fi
if grep -qi 'not a backtest' "$SKILL_MD" && grep -qi 'not market data' "$SKILL_MD"; then
  pass "the 'not a result / not market data' disclaimer is present"
else
  fail "the synthetic-data disclaimer is missing"
fi
if grep -qi 'could not be verified\|unverified\|not verifiable' "$SKILL_MD"; then
  pass "unverified claims are labelled as unverified"
else
  fail "no explicit unverified-claim disclosure found"
fi
if grep -qi 'not.*claim.*profit\|does not claim\|never claim' "$SKILL_MD" || grep -qi 'no sentence' "$SKILL_MD"; then
  pass "the skill explicitly disclaims any profitability claim"
else
  fail "no explicit profitability disclaimer found"
fi

# ── Block G: G14 depth gates (finance thresholds, verified with grep) ──────
echo ""
echo "--- G14 Depth (finance thresholds; regexes verified by grep) ---"
BULL=$(count_matches 'bull market|bull regime|uptrend' "$SKILL_MD" -i)
CORR=$(count_matches 'correction|pullback' "$SKILL_MD" -i)
BEAR=$(count_matches 'bear market|downturn|drawdown|recession' "$SKILL_MD" -i)
CRASH=$(count_matches 'crash|tail event|black swan|march 2020|market collapse' "$SKILL_MD" -i)
REGIMES=0
[[ "${BULL:-0}" -gt 0 ]] && REGIMES=$((REGIMES + 1))
[[ "${CORR:-0}" -gt 0 ]] && REGIMES=$((REGIMES + 1))
[[ "${BEAR:-0}" -gt 0 ]] && REGIMES=$((REGIMES + 1))
[[ "${CRASH:-0}" -gt 0 ]] && REGIMES=$((REGIMES + 1))
check_ge "Regime coverage (of 4; bull=$BULL correction=$CORR bear=$BEAR crash=$CRASH)" "$REGIMES" 3

FAILMODE=$(count_matches 'failure[ -]mode|what[ -].*go[ -].*wrong|when[ -].*fails|when[ -].*break|loses[ -].*money|worst[ -]case|exit[ -]condition|stop[ -]loss|close[ -]position|edge[ -]case|known[ -]limitation|what[ -].*break' "$SKILL_MD" -i)
check_ge "Failure-mode matches" "${FAILMODE:-0}" 9

FM_LIST=$(sed -n '/^### Failure Modes/,/^### Regime Table/p' "$SKILL_MD" | grep -cE '^[0-9]+\. \*\*Failure mode' || true)
check_ge "Numbered failure modes under '### Failure Modes'" "${FM_LIST:-0}" 10

if grep -q 'exit condition\|exit rule\|stop-loss\|stop loss\|kill criterion\|kill criteria' "$SKILL_MD"; then
  pass "exit conditions / kill criteria documented"
else
  fail "no exit conditions documented"
fi

FAILMODE_REFS=$(cat "$REF_DIR"/*.md | grep -cE '^[0-9]+\. \*\*Failure mode' || true)
check_ge "Numbered failure-mode rows across reference files" "${FAILMODE_REFS:-0}" 10

# ── Block H: References ─────────────────────────────────────────────────────
echo ""
echo "--- References ---"
REF_COUNT=$(find "$REF_DIR" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
check_ge "Reference files on disk" "${REF_COUNT:-0}" 11

THIN=0
for f in "$REF_DIR"/*.md; do
  [[ -f "$f" ]] || continue
  n=$(count_lines "$f")
  if [[ "$n" -lt 80 ]]; then
    fail "Reference file under 80 lines: $(basename "$f") ($n lines)"
    THIN=$((THIN + 1))
  fi
done
if [[ "$THIN" -eq 0 ]]; then pass "every reference file has at least 80 lines of content"; fi

BROKEN=0
for ref in $(grep -ohE '\(references/[^)]*\.md\)' "$SKILL_MD" 2>/dev/null | sed 's|(references/||;s|)||' || true); do
  if [[ -n "$ref" && ! -f "$REF_DIR/$ref" ]]; then
    fail "Broken reference link: references/$ref"
    BROKEN=$((BROKEN + 1))
  fi
done
if [[ "$BROKEN" -eq 0 ]]; then pass "all reference links resolve (0 broken)"; fi

# Orphan check: every references/*.md on disk must be linked from SKILL.md.
ORPHANS=0
for f in "$REF_DIR"/*.md; do
  [[ -f "$f" ]] || continue
  base="$(basename "$f")"
  if ! grep -qF "(references/$base)" "$SKILL_MD" 2>/dev/null; then
    fail "ORPHANED reference file: references/$base is not linked from SKILL.md"
    ORPHANS=$((ORPHANS + 1))
  fi
done
if [[ "$ORPHANS" -eq 0 ]]; then pass "no orphaned reference files ($REF_COUNT on disk, all linked)"; fi

# ── Block I: The checker runs, and is deterministic ────────────────────────
echo ""
echo "--- Checker: runs and is deterministic ---"
if $PY "$ENGINE" --version >"$TMP/version.txt" 2>&1; then
  pass "checker --version runs: $(cat "$TMP/version.txt")"
else
  fail "checker --version failed"
fi

DET_FAILS=0
run_det() {
  # $1 = label, $2.. = engine args
  local label="$1"; shift
  if ! $PY "$ENGINE" "$@" >"$TMP/det1" 2>&1; then
    fail "checker FAILED on: $label"
    DET_FAILS=$((DET_FAILS + 1))
    return
  fi
  $PY "$ENGINE" "$@" >"$TMP/det2" 2>&1
  if diff -q "$TMP/det1" "$TMP/det2" >/dev/null 2>&1; then
    pass "byte-identical across two runs: $label"
  else
    fail "NOT deterministic: $label"
    DET_FAILS=$((DET_FAILS + 1))
  fi
}
run_det "positive card"        --tp 2.5 --sl 1.0 --p 0.35 --cost-r 0.02
run_det "negative card"        --tp 0.5 --sl 2.0 --p 0.70
run_det "credit mode"          --credit 1.00 --width 5.00 --tp-money 50 --sl-money 200 --p 0.80
run_det "scaling check"        --scaling-check --legs 4 --fee-per-contract 0.65 --rung-split 3 --position-value 5.00
run_det "fee derivation"       --tp 2.5 --sl 1.0 --p 0.35 --fee-per-contract 0.65 --legs 4 --r-dollars 15
run_det "from-log"             --from-log "$SYN_LOG"
run_det "from-log --setup"     --from-log "$SYN_LOG" --setup debit-spread-2.5R --tp 2.5 --sl 1.0 --p 0.35
run_det "json output"          --json --tp 0.5 --sl 2.0 --p 0.80
run_det "edge sl=0"            --tp 1 --sl 0 --p 0.5
run_det "edge tp=0"            --tp 0 --sl 1 --p 0.5
run_det "edge p=1"             --tp 1 --sl 1 --p 1.0
run_det "edge p=0"             --tp 1 --sl 1 --p 0.0
run_det "edge n=1"             --tp 2 --sl 1 --p 0.5 --n 1
run_det "edge cost>=E"         --tp 2.5 --sl 1 --p 0.35 --cost-r 0.5

# JSON and CSV-out determinism
$PY "$ENGINE" --json --from-log "$SYN_LOG" >"$TMP/j1" 2>&1
$PY "$ENGINE" --json --from-log "$SYN_LOG" >"$TMP/j2" 2>&1
if diff -q "$TMP/j1" "$TMP/j2" >/dev/null 2>&1; then pass "JSON from-log output is byte-identical across two runs"; else fail "JSON from-log NOT deterministic"; fi
$PY "$ENGINE" --csv-out "$TMP/c1.csv" --from-log "$SYN_LOG" >/dev/null 2>&1
$PY "$ENGINE" --csv-out "$TMP/c2.csv" --from-log "$SYN_LOG" >/dev/null 2>&1
if diff -q "$TMP/c1.csv" "$TMP/c2.csv" >/dev/null 2>&1; then pass "CSV-out is byte-identical across two runs"; else fail "CSV-out NOT deterministic"; fi

# The generator must be deterministic too: same seed, same bytes.
if $PY "$GEN" --print >"$TMP/gen1.csv" 2>&1; then
  $PY "$GEN" --print >"$TMP/gen2.csv" 2>&1
  if diff -q "$TMP/gen1.csv" "$TMP/gen2.csv" >/dev/null 2>&1; then
    pass "seeded generator is byte-identical on re-run (seed fixed)"
  else
    fail "seeded generator is NOT deterministic"
  fi
  if diff -q "$TMP/gen1.csv" "$SYN_LOG" >/dev/null 2>&1; then
    pass "the committed SYNTHETIC log matches the generator byte for byte"
  else
    fail "the committed SYNTHETIC log has DRIFTED from the generator"
  fi
else
  fail "seeded generator failed to run"
fi

# Orphan/robustness: an invalid input must exit non-zero with a message, not crash.
if $PY "$ENGINE" --from-log "$TMP/does-not-exist.csv" >"$TMP/missing.out" 2>&1; then
  fail "a missing log should be a non-zero exit"
else
  if grep -q 'ERROR' "$TMP/missing.out"; then
    pass "a missing log exits non-zero with an ERROR message"
  else
    fail "a missing log exited non-zero without an ERROR message"
  fi
fi
if $PY "$ENGINE" >"$TMP/noargs.out" 2>&1; then
  fail "no arguments should be a non-zero exit"
else
  pass "no arguments exits non-zero with usage guidance"
fi

# ── Block J: The documented arithmetic (engine vs this skill's own numbers) ─
# Every value asserted below is written in SKILL.md and in examples/checks/ as
# the expected value. If the checker and the documentation ever diverge, this
# block fails.
echo ""
echo "--- Hand-Check Arithmetic (engine vs the documented values) ---"

# Card 1 — long premium, 1R stop, 2.5R target @ p = 0.35, c_R = 0.02
$PY "$ENGINE" --tp 2.5 --sl 1.0 --p 0.35 --cost-r 0.02 >"$TMP/c1.txt" 2>&1
assert_engine_value "C1 b = 2.5000"            "$TMP/c1.txt" "b       = tp/sl                  : 2.5000"
assert_engine_value "C1 E = 0.2250 R"          "$TMP/c1.txt" "E       = p*b - (1-p)            : 0.2250 R per trade"
assert_engine_value "C1 E_net = 0.2050 R"      "$TMP/c1.txt" "E_net   = E - c_R                : 0.2050 R per trade"
assert_engine_value "C1 b* = 1.8571"           "$TMP/c1.txt" "b*      = (1-p)/p                : 1.8571"
assert_engine_value "C1 p* = 28.57%"           "$TMP/c1.txt" "p*      = 1/(1+b)                : 28.57%"
assert_engine_value "C1 edge = 6.43%"          "$TMP/c1.txt" "edge    = p - p*                 : 6.43%"
assert_engine_value "C1 f* = 9.00%"            "$TMP/c1.txt" "f*      = E/b                    : 9.00% of capital"
assert_engine_value "C1 half-Kelly = 4.50%"    "$TMP/c1.txt" "half-Kelly                       : 4.50% of capital"
assert_engine_value "C1 sd = 1.6694 R"         "$TMP/c1.txt" "sd      = sqrt(p(b-E)^2+(1-p)(-1-E)^2) : 1.6694 R"
assert_engine_value "C1 se_E = 0.1056 R"       "$TMP/c1.txt" "se_E    = sd/sqrt(n)                   : 0.1056 R"
assert_engine_value "C1 n_req = 220.20"        "$TMP/c1.txt" ": 220.20  (ceil: 221)"
assert_engine_value "C1 years_at_pace = 0.88"  "$TMP/c1.txt" "years_at_pace = n_req / trades_per_year: 0.88 years"
assert_engine_value "C1 L = 13 (raw 12.82)"    "$TMP/c1.txt" ": 13 trades  (raw: 12.82)"
assert_engine_value "C1 R_max = 1.03%"         "$TMP/c1.txt" ": 1.03% of equity per trade"
assert_engine_value "C1 verdict is POSITIVE"   "$TMP/c1.txt" "POSITIVE: E_net = 0.2050 >= se_E = 0.1056"
assert_engine_value "C1 sensitivity E at p-5pp" "$TMP/c1.txt" "p -5pp -> 30.0%                          0.0500       0.0300"
assert_engine_value "C1 sensitivity E at p+5pp" "$TMP/c1.txt" "p +5pp -> 40.0%                          0.4000       0.3800"
assert_engine_value "C1 sensitivity b -0.25"   "$TMP/c1.txt" "b -0.25 -> 2.250                         0.1375       0.1175"
assert_engine_value "C1 sensitivity cost x2"   "$TMP/c1.txt" "cost x2.0 -> 0.0400 R                    0.2250       0.1850"

# Card 2 — credit 50%/2x @ p = 0.70: NEGATIVE
$PY "$ENGINE" --tp 0.5 --sl 2.0 --p 0.70 >"$TMP/c2.txt" 2>&1
assert_engine_value "C2 b = 0.2500"            "$TMP/c2.txt" "b       = tp/sl                  : 0.2500"
assert_engine_value "C2 E = -0.1250 R"         "$TMP/c2.txt" "E       = p*b - (1-p)            : -0.1250 R per trade"
assert_engine_value "C2 b* = 0.4286"           "$TMP/c2.txt" "b*      = (1-p)/p                : 0.4286"
assert_engine_value "C2 p* = 80.00%"           "$TMP/c2.txt" "p*      = 1/(1+b)                : 80.00%"
assert_engine_value "C2 edge = -10.00%"        "$TMP/c2.txt" "edge    = p - p*                 : -10.00%"
assert_engine_value "C2 f* = -50.00%"          "$TMP/c2.txt" "f*      = E/b                    : -50.00% of capital"
assert_engine_value "C2 sd = 0.5728 R"         "$TMP/c2.txt" "sd      = sqrt(p(b-E)^2+(1-p)(-1-E)^2) : 0.5728 R"
assert_engine_value "C2 L = 5 (raw 4.59)"      "$TMP/c2.txt" ": 5 trades  (raw: 4.59)"
assert_engine_value "C2 R_max = 2.67%"         "$TMP/c2.txt" ": 2.67% of equity per trade"
assert_engine_value "C2 n_req refused with a reason" "$TMP/c2.txt" "You cannot see an edge that is not there"
assert_engine_value "C2 negative-Kelly note"   "$TMP/c2.txt" "f* is negative: the Kelly criterion says do not bet"
assert_engine_value "C2 verdict is NEGATIVE"   "$TMP/c2.txt" "NEGATIVE: E_net = -0.1250 <= -se_E = -0.0362"

# Card 3 — the 50%/2x card in credit mode at p = 0.80: EXACTLY break-even
$PY "$ENGINE" --credit 1.00 --width 5.00 --tp-money 50 --sl-money 200 --p 0.80 >"$TMP/c3.txt" 2>&1
assert_engine_value "C3 R basis = max loss 400.00" "$TMP/c3.txt" "1R = the structure's max loss (W - C) x multiplier = 400.00"
assert_engine_value "C3 per-spread credit 100.00"  "$TMP/c3.txt" "per spread      : credit 100.00   width 500.00   max loss (W-C): 400.00"
assert_engine_value "C3 target is 50.00% of credit" "$TMP/c3.txt" "target          : 50.00 (50.00% of credit)   stop: 200.00 (2.00 x credit)"
assert_engine_value "C3 b = 0.2500"            "$TMP/c3.txt" "b       = tp/sl                  : 0.2500"
assert_engine_value "C3 E = 0.0000 R (exact)"  "$TMP/c3.txt" "E       = p*b - (1-p)            : 0.0000 R per trade"
assert_engine_value "C3 b* equals b = 0.2500"  "$TMP/c3.txt" "b*      = (1-p)/p                : 0.2500"
assert_engine_value "C3 p* equals p = 80.00%"  "$TMP/c3.txt" "p*      = 1/(1+b)                : 80.00%"
assert_engine_value "C3 edge = 0.00%"          "$TMP/c3.txt" "edge    = p - p*                 : 0.00%"
assert_engine_value "C3 f* = 0.00%"            "$TMP/c3.txt" "f*      = E/b                    : 0.00% of capital"
assert_engine_value "C3 sd = 0.5000 R"         "$TMP/c3.txt" "sd      = sqrt(p(b-E)^2+(1-p)(-1-E)^2) : 0.5000 R"
assert_engine_value "C3 L = 4 (raw 3.43)"      "$TMP/c3.txt" ": 4 trades  (raw: 3.43)"
assert_engine_value "C3 R_max = 3.33%"         "$TMP/c3.txt" ": 3.33% of equity per trade"
assert_engine_value "C3 n_req refused (E = 0)" "$TMP/c3.txt" "n/a: E = 0.0000 <= 0."
assert_engine_value "C3 verdict is MARGINAL"   "$TMP/c3.txt" "MARGINAL: |E_net| = 0.0000 < se_E = 0.0316"
assert_no_value  "C3 does not emit an astronomical n_req" "$TMP/c3.txt" "324518553658426654725561982648320"

# Card 4 — the multi-rung fee threshold
$PY "$ENGINE" --scaling-check --legs 4 --fee-per-contract 0.65 --rung-split 3 --position-value 5.00 >"$TMP/c4.txt" 2>&1
assert_engine_value "C4 fee_per_rung = 2.60"   "$TMP/c4.txt" "= 4 * 0.65 = 2.60"
assert_engine_value "C4 banked_per_rung = 1.67" "$TMP/c4.txt" "= 5.00 / 3 = 1.67"
assert_engine_value "C4 extra_fee = 5.20"      "$TMP/c4.txt" "= 2 * 4 * 0.65 = 5.20"
assert_engine_value "C4 threshold = 7.80"      "$TMP/c4.txt" "position_value < rung_split * legs * fee_per_contract = 3 * 4 * 0.65 = 7.80"
assert_engine_value "C4 FEE-NEGATIVE at 5.00"  "$TMP/c4.txt" "FEE-NEGATIVE: each rung banks 1.67 and pays 2.60"
assert_engine_value "C4 shortfall 0.93 per rung" "$TMP/c4.txt" "a shortfall of"
$PY "$ENGINE" --scaling-check --legs 4 --fee-per-contract 0.65 --rung-split 3 --position-value 12.00 >"$TMP/c4b.txt" 2>&1
assert_engine_value "C4b FEE-POSITIVE at 12.00" "$TMP/c4b.txt" "FEE-POSITIVE: each rung banks 4.00 and pays 2.60"

# Card 5 — the marginal two-point edge
$PY "$ENGINE" --tp 0.5 --sl 1.0 --p 0.68 >"$TMP/c5.txt" 2>&1
assert_engine_value "C5 b = 0.5000"            "$TMP/c5.txt" "b       = tp/sl                  : 0.5000"
assert_engine_value "C5 E = 0.0200 R"          "$TMP/c5.txt" "E       = p*b - (1-p)            : 0.0200 R per trade"
assert_engine_value "C5 b* = 0.4706"           "$TMP/c5.txt" "b*      = (1-p)/p                : 0.4706"
assert_engine_value "C5 p* = 66.67%"           "$TMP/c5.txt" "p*      = 1/(1+b)                : 66.67%"
assert_engine_value "C5 edge = 1.33%"          "$TMP/c5.txt" "edge    = p - p*                 : 1.33%"
assert_engine_value "C5 sd = 0.6997 R"         "$TMP/c5.txt" "sd      = sqrt(p(b-E)^2+(1-p)(-1-E)^2) : 0.6997 R"
assert_engine_value "C5 se_E = 0.0443 R"       "$TMP/c5.txt" "se_E    = sd/sqrt(n)                   : 0.0443 R"
assert_engine_value "C5 n_req = 4896.00"       "$TMP/c5.txt" ": 4896.00  (ceil: 4896)"
assert_engine_value "C5 years_at_pace = 19.58" "$TMP/c5.txt" ": 19.58 years"
assert_engine_value "C5 L = 5 (raw 4.85)"      "$TMP/c5.txt" ": 5 trades  (raw: 4.85)"
assert_engine_value "C5 verdict is MARGINAL"   "$TMP/c5.txt" "MARGINAL: |E_net| = 0.0200 < se_E = 0.0443"

# Card 6 — the fee derivation turning a positive corner negative
$PY "$ENGINE" --tp 2.5 --sl 1.0 --p 0.35 --fee-per-contract 0.65 --legs 4 --r-dollars 15 >"$TMP/c6.txt" 2>&1
assert_engine_value "C6 cost_per_trade = 5.20" "$TMP/c6.txt" "= 0.65 * 4 * 2 = 5.20"
assert_engine_value "C6 tickets = 8"           "$TMP/c6.txt" "tickets per round trip = legs * 2 = 8"
assert_engine_value "C6 c_R = 0.3467 R"        "$TMP/c6.txt" "= 5.20 / 15.00 = 0.3467 R"
assert_engine_value "C6 E_net = -0.1217 R"     "$TMP/c6.txt" "E_net   = E - c_R                : -0.1217 R per trade"
assert_engine_value "C6 cost note fires"       "$TMP/c6.txt" "cost 0.3467 R >= gross E 0.2250 R"
assert_engine_value "C6 verdict is NEGATIVE"   "$TMP/c6.txt" "NEGATIVE: E_net = -0.1217 <= -se_E = -0.1056"

# The synthetic log's two cohorts — the hand-check values in the CSV header
$PY "$ENGINE" --json --from-log "$SYN_LOG" >"$TMP/syn.json" 2>&1
assert_json_field "SYN log rows = 80"                  "$TMP/syn.json" "from_log.rows" "80"
assert_json_field "SYN r_mode is on"                   "$TMP/syn.json" "from_log.r_mode" "yes"
assert_json_field "SYN condor n = 40"                  "$TMP/syn.json" "from_log.cohorts.0.n" "40"
assert_json_field "SYN condor wins = 31"               "$TMP/syn.json" "from_log.cohorts.0.wins" "31"
assert_json_field "SYN condor losses = 9"              "$TMP/syn.json" "from_log.cohorts.0.losses" "9"
assert_json_field "SYN condor p = 0.7750"              "$TMP/syn.json" "from_log.cohorts.0.p" "0.775"
assert_json_field "SYN condor b = 0.250"               "$TMP/syn.json" "from_log.cohorts.0.b" "0.25"
assert_json_field "SYN condor E = -0.03125"            "$TMP/syn.json" "from_log.cohorts.0.E" "-0.03125"
assert_json_field "SYN condor cost_r = 0.026"          "$TMP/syn.json" "from_log.cohorts.0.cost_r" "0.026"
assert_json_field "SYN condor E_net = -0.05725"        "$TMP/syn.json" "from_log.cohorts.0.E_net" "-0.05725"
assert_json_field "SYN debit n = 40"                   "$TMP/syn.json" "from_log.cohorts.1.n" "40"
assert_json_field "SYN debit wins = 14"                "$TMP/syn.json" "from_log.cohorts.1.wins" "14"
assert_json_field "SYN debit losses = 26"              "$TMP/syn.json" "from_log.cohorts.1.losses" "26"
assert_json_field "SYN debit p = 0.3500"               "$TMP/syn.json" "from_log.cohorts.1.p" "0.35"
assert_json_field "SYN debit avg_win = 2.4700 R"       "$TMP/syn.json" "from_log.cohorts.1.avg_win_R" "2.47"
assert_json_field "SYN debit b = 2.470"                "$TMP/syn.json" "from_log.cohorts.1.b" "2.47"
assert_json_field "SYN debit E = 0.21450 R"            "$TMP/syn.json" "from_log.cohorts.1.E" "0.2145"
assert_json_field "SYN debit cost_r = 0.013"           "$TMP/syn.json" "from_log.cohorts.1.cost_r" "0.013"
assert_json_field "SYN debit E_net = 0.20150 R"        "$TMP/syn.json" "from_log.cohorts.1.E_net" "0.2015"
assert_json_field "SYN pooled n = 80"                  "$TMP/syn.json" "from_log.cohorts.2.n" "80"
assert_json_field "SYN pooled p = 0.5625"              "$TMP/syn.json" "from_log.cohorts.2.p" "0.5625"

# The log's own arithmetic, straight from the CSV: 31 wins at +0.25R and 14 wins
# averaging 2.4700R must produce those two E values.
SYN_CHECK=$($PY - "$SYN_LOG" <<'PYEOF'
import csv, sys

wins_condor = losses_condor = 0
wins_debit = losses_debit = 0
sum_debit_win_r = 0.0
with open(sys.argv[1], encoding="utf-8", newline="") as fh:
    lines = [l for l in fh if not l.lstrip().startswith("#")]
for rec in csv.DictReader(lines):
    pnl = float(rec["pnl"]); risk = float(rec["risk"])
    r = pnl / risk
    if rec["setup"] == "credit-condor-50-2x":
        if pnl > 0: wins_condor += 1
        elif pnl < 0: losses_condor += 1
    else:
        if pnl > 0:
            wins_debit += 1; sum_debit_win_r += r
        elif pnl < 0: losses_debit += 1
p_condor = wins_condor / (wins_condor + losses_condor)
E_condor = p_condor * 0.25 - (1 - p_condor)
avg_win_debit = sum_debit_win_r / wins_debit
p_debit = wins_debit / (wins_debit + losses_debit)
E_debit = p_debit * avg_win_debit - (1 - p_debit)
print("%d %d %.6f %.6f %.6f %.6f %.6f" % (
    wins_condor, wins_debit, p_condor, E_condor,
    avg_win_debit, p_debit, E_debit))
PYEOF
)
if [[ "$SYN_CHECK" == "31 14 0.775000 -0.031250 2.470000 0.350000 0.214500" ]]; then
  pass "SYN log hand-check: 31 wins / 14 wins, E_condor = -0.031250R, E_debit = +0.214500R"
else
  fail "SYN log hand-check FAILED (got: $SYN_CHECK)"
fi

# ── Block K: Robustness / negative controls ────────────────────────────────
echo ""
echo "--- Robustness and Negative Controls ---"
$PY "$ENGINE" --tp 1 --sl 0 --p 0.5 >"$TMP/e1.txt" 2>&1
assert_engine_value "sl=0 -> b is refused with a reason" "$TMP/e1.txt" "a stop of 0R means the loss is unbounded"
$PY "$ENGINE" --tp 0 --sl 1 --p 0.5 >"$TMP/e2.txt" 2>&1
assert_engine_value "tp=0 -> b = 0.0000 is legal"        "$TMP/e2.txt" "b       = tp/sl                  : 0.0000"
assert_engine_value "tp=0 -> E = -0.5000 R"              "$TMP/e2.txt" "E       = p*b - (1-p)            : -0.5000 R per trade"
$PY "$ENGINE" --tp 1 --sl 1 --p 1.0 >"$TMP/e3.txt" 2>&1
assert_engine_value "p=1 -> E = +1.0000 R"               "$TMP/e3.txt" "E       = p*b - (1-p)            : 1.0000 R per trade"
assert_engine_value "p=1 -> L = 0 with a note"           "$TMP/e3.txt" "p = 1: a losing trade cannot occur"
$PY "$ENGINE" --tp 1 --sl 1 --p 0.0 >"$TMP/e4.txt" 2>&1
assert_engine_value "p=0 -> E = -1.0000 R"               "$TMP/e4.txt" "E       = p*b - (1-p)            : -1.0000 R per trade"
assert_engine_value "p=0 -> b* refused with a reason"    "$TMP/e4.txt" "no payoff breaks even at a zero win rate"
$PY "$ENGINE" --tp 2 --sl 1 --p 0.5 --n 1 >"$TMP/e5.txt" 2>&1
assert_engine_value "n=1 -> se_E = sd"                   "$TMP/e5.txt" "se_E    = sd/sqrt(n)                   : 1.5000 R"
$PY "$ENGINE" --tp 2.5 --sl 1 --p 0.35 --cost-r 0.5 >"$TMP/e6.txt" 2>&1
assert_engine_value "cost >= E -> cost note fires"       "$TMP/e6.txt" "cost 0.5000 R >= gross E 0.2250 R"

# Negative controls: tokens that must NOT be present anywhere in the card output
assert_no_value "no 'guaranteed' in the checker output" "$TMP/c1.txt" "guaranteed"
assert_no_value "no 'will make money' claim in output"  "$TMP/c1.txt" "will make money"
assert_no_value "no benchmark claim in output"          "$TMP/c1.txt" "outperform"

# The SYNTHETIC label must be echoed into every from-log output.
$PY "$ENGINE" --from-log "$SYN_LOG" >"$TMP/syn.txt" 2>&1
assert_engine_value "SYNTHETIC label is echoed into the output" "$TMP/syn.txt" "SYNTHETIC / ILLUSTRATIVE"
assert_engine_value "the input is labelled not-a-backtest"      "$TMP/syn.txt" "NOT a backtest"
assert_engine_value "the engine states it is not a forecast"    "$TMP/syn.txt" "NOT a forecast"
assert_engine_value "the cohort tag is what prevents pooling"   "$TMP/syn.txt" "credit-condor-50-2x"
assert_engine_value "the profit corner is reported per cohort"  "$TMP/syn.txt" "debit-spread-2.5R"
assert_engine_value "the condor cohort is negative on this fixture" "$TMP/syn.txt" "-0.0572"

# ── Block L: Scope discipline / deferrals ──────────────────────────────────
echo ""
echo "--- Scope Discipline ---"
for defer in 'options-strategist' 'advanced-options-structures' 'options-position-lifecycle' \
             'options-leg-management' 'trade-sizing-recovery' 'options-risk-engineer' \
             'edge-and-payoff-engineering' 'timeframe-performance-statistics' \
             'options-automation-engineer' 'trading-decision-data-catalogue' \
             'technical-signals-engineer' 'macro-strategist' 'quantitative-analyst'; do
  if grep -q "$defer" "$SKILL_MD" 2>/dev/null; then
    pass "defers to: $defer"
  else
    fail "no deferral to: $defer"
  fi
done
if grep -qi 'never select\|selects no\|never select, recommends or prices\|prices a \*payoff\*' "$SKILL_MD"; then
  pass "the structure-selection handoff is stated as a refusal"
else
  fail "the structure-selection handoff is not stated"
fi
if grep -q 'p\* = 1/(1+b)' "$SKILL_MD"; then
  pass "the break-even win rate formula is stated"
else
  fail "the break-even win rate formula is missing from SKILL.md"
fi
if grep -q '0.0000' "$SKILL_MD" && grep -q '80.00%' "$SKILL_MD"; then
  pass "the 50%/2x break-even identity (p*=80.00%, E=0.0000R) is documented"
else
  fail "the 50%/2x break-even identity is missing"
fi

# ── Block M: examples/run-output.txt is fresh ──────────────────────────────
echo ""
echo "--- run-output.txt Freshness ---"
if [[ -f "$EX_DIR/run-output.txt" ]]; then
  for token in "OPTIONS PAYOFF CHECK" \
               "b       = tp/sl                  : 2.5000" \
               "MARGINAL: |E_net| = 0.0000 < se_E = 0.0316" \
               "FEE-NEGATIVE: each rung banks 1.67 and pays 2.60" \
               "SYNTHETIC / ILLUSTRATIVE" \
               "DIFF (run 1 vs run 2): byte-identical"; do
    if grep -qF -- "$token" "$EX_DIR/run-output.txt"; then
      pass "run-output.txt contains this run's output: $(echo "$token" | cut -c1-46)"
    else
      fail "run-output.txt is STALE — missing: $token"
    fi
  done
  RUNS=$(grep -c '^# COMMAND ' "$EX_DIR/run-output.txt" || true)
  check_ge "run-output.txt documented commands" "${RUNS:-0}" 6
  DIFFS=$(grep -c '^DIFF (run 1 vs run 2): byte-identical' "$EX_DIR/run-output.txt" || true)
  check_ge "run-output.txt determinism diffs shown" "${DIFFS:-0}" 6
else
  fail "run-output.txt missing"
fi

# ── Block N: examples/checks/ freshness ────────────────────────────────────
echo ""
echo "--- examples/checks Freshness ---"
CHECK_FILES=$(find "$CHECK_DIR" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
check_ge "documented check files" "${CHECK_FILES:-0}" 4
if [[ "${CHECK_FILES:-0}" -le 6 ]]; then
  pass "documented check count is within 4-6 ($CHECK_FILES)"
else
  fail "documented check count is $CHECK_FILES (spec says 4-6)"
fi
for token in "b       = tp/sl                  : 2.5000" \
             "POSITIVE: E_net = 0.2050 >= se_E = 0.1056" \
             "NEGATIVE: E_net = -0.1250 <= -se_E = -0.0362" \
             "p*      = 1/(1+b)                : 80.00%" \
             "FEE-NEGATIVE: each rung banks 1.67 and pays 2.60" \
             "MARGINAL: |E_net| = 0.0200 < se_E = 0.0443" \
             "NEGATIVE: E_net = -0.1217 <= -se_E = -0.1056"; do
  if grep -rqF -- "$token" "$CHECK_DIR" 2>/dev/null; then
    pass "checks/ contains verbatim output: $(echo "$token" | cut -c1-46)"
  else
    fail "checks/ is missing verbatim output: $token"
  fi
done
if grep -rqF 'the tool'"'"'s own, captured verbatim' "$CHECK_DIR" 2>/dev/null; then
  pass "every check file states that its output is the tool's own, captured verbatim"
else
  fail "a check file does not state that its output is the tool's own, verbatim"
fi
if grep -rqi 'not.*claim\|does not claim\|not a result\|not market data' "$CHECK_DIR" 2>/dev/null; then
  pass "checks/ carries the not-a-result framing"
else
  fail "checks/ does not carry the not-a-result framing"
fi

# ── Block O: The synthetic fixture is labelled everywhere it appears ───────
echo ""
echo "--- Synthetic Labelling ---"
for f in "$SYN_LOG" "$GEN" "$EX_DIR/README.md" "$SKILL_MD" \
         "$REF_DIR/from-negative-to-positive-walkthrough.md"; do
  if grep -qi 'SYNTHETIC' "$f" 2>/dev/null; then
    pass "SYNTHETIC labelled: $(basename "$f")"
  else
    fail "SYNTHETIC label MISSING from: $(basename "$f")"
  fi
done
if grep -qi 'SYNTHETIC' "$EX_DIR/run-output.txt" 2>/dev/null; then
  pass "SYNTHETIC labelled in run-output.txt"
else
  fail "SYNTHETIC label MISSING from run-output.txt"
fi
# The fixture filename itself must carry the label.
if [[ "$(basename "$SYN_LOG")" == *synthetic* ]]; then
  pass "the fixture filename carries the synthetic label"
else
  fail "the fixture filename does not carry the synthetic label"
fi

# ── Summary ────────────────────────────────────────────────────────────────
echo ""
echo "=============================================="
if [[ "$FAILURES" -eq 0 ]]; then
  echo "OK  $SKILL_NAME: all $CHECKS checks passed"
  exit 0
else
  echo "FAIL $SKILL_NAME: $FAILURES of $CHECKS check(s) failed"
  exit 1
fi
