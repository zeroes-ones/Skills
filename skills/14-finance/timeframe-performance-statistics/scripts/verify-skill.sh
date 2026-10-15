#!/usr/bin/env bash
# ============================================================================
# verify-skill.sh — self-verification for timeframe-performance-statistics
# ============================================================================
# Structural, provenance, gate, arithmetic and determinism checks for this
# skill. Bash 3.2 compatible, no third-party dependencies, no network.
# Exits 0 when every check passes, 1 otherwise.
#
# The two checks that make this script more than a lint:
#   (a) it runs the engine on the six-trade hand-check log and asserts the
#       expected values DOCUMENTED IN THAT FILE'S OWN HEADER, so the documented
#       arithmetic and the shipped code cannot drift apart;
#   (b) it asserts the engine is DETERMINISTIC by running it twice on the same
#       input and diffing — text, JSON and CSV-out.
#
# Usage: bash scripts/verify-skill.sh
# ============================================================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
SKILL_NAME="$(basename "$SKILL_DIR")"
REF_DIR="$SKILL_DIR/references"
EX_DIR="$SKILL_DIR/examples"
LOG_DIR="$EX_DIR/logs"
ENGINE="$SKILL_DIR/scripts/timeframe_stats.py"
HAND_LOG="$LOG_DIR/hand-check-synthetic.csv"
YEAR_LOG="$LOG_DIR/illustrative-year-synthetic.csv"

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
TMP="$(mktemp -d 2>/dev/null || mktemp -d -t tfstats)"
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
# Use for un-padded text (CSV rows, sentences). For the engine's right-aligned
# summary table use assert_field, which is whitespace-tolerant.
assert_engine_value() {
  local label="$1" file="$2" token="$3"
  if grep -qF -- "$token" "$file" 2>/dev/null; then
    pass "hand-check: $label"
  else
    fail "hand-check MISSING from engine output: $label (looked for: $token)"
  fi
}

# assert_field <label> <fields-file> <bucket> <field> <expected> [tolerance]
# Reads the flat "bucket<TAB>field<TAB>value" dump produced by dump_fields, so a
# value is asserted by NAME rather than by its column position in a padded table.
assert_field() {
  local label="$1" file="$2" bucket="$3" field="$4" expect="$5" tol="${6:-0.0005}"
  local row
  row="$(awk -F'\t' -v b="$bucket" -v f="$field" '$1==b && $2==f {print $3; exit}' "$file")"
  if [[ "$row" == "$expect" ]]; then
    pass "hand-check: $label"
    return 0
  fi
  if [[ "$row" =~ ^-?[0-9] && "$expect" =~ ^-?[0-9] ]]; then
    if awk -v a="$row" -v b="$expect" -v t="$tol" 'BEGIN{d=a-b; if(d<0)d=-d; exit !(d<=t)}'; then
      pass "hand-check: $label"
      return 0
    fi
  fi
  fail "hand-check FAILED: $label (wanted $bucket.$field = $expect)"
}

# dump_fields <json-file> <out-file>  ->  "bucket<TAB>field<TAB>value" per line,
# with the verdict block flattened under the bucket name VERDICT.
dump_fields() {
  $PY - "$1" > "$2" <<'PYEOF'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as fh:
    data = json.load(fh)


def emit(bucket, key, val):
    if val is None:
        val = "n/a"
    elif isinstance(val, bool):
        val = "yes" if val else "no"
    sys.stdout.write("%s\t%s\t%s\n" % (bucket, key, val))


for b in data["buckets"]:
    for k in sorted(b):
        v = b[k]
        if isinstance(v, (list, dict)):
            continue
        emit(b["bucket"], k, v)
for k in sorted(data["verdict"]):
    v = data["verdict"][k]
    if isinstance(v, (list, dict)):
        continue
    emit("VERDICT", k, v)
PYEOF
}

echo "=== Verifying $SKILL_NAME ==="
echo "  interpreter: $PY"
echo ""

# ── Block A: File existence ───────────────────────────────────────────────
echo "--- File Existence ---"
if [[ -f "$SKILL_MD" ]]; then pass "SKILL.md exists"; else fail "SKILL.md not found"; exit 1; fi
if [[ -d "$REF_DIR" ]]; then pass "references/ directory exists"; else fail "references/ directory MISSING"; fi
if [[ -d "$EX_DIR" ]]; then pass "examples/ directory exists"; else fail "examples/ directory MISSING"; fi
if [[ -d "$LOG_DIR" ]]; then pass "examples/logs/ directory exists"; else fail "examples/logs/ directory MISSING"; fi
if [[ -f "$ENGINE" ]]; then pass "engine exists: scripts/timeframe_stats.py"; else fail "engine MISSING: scripts/timeframe_stats.py"; fi
if [[ -f "$HAND_LOG" ]]; then pass "hand-check log exists"; else fail "hand-check log MISSING"; fi
if [[ -f "$YEAR_LOG" ]]; then pass "illustrative log exists"; else fail "illustrative log MISSING"; fi
if [[ -f "$LOG_DIR/generate_synthetic.py" ]]; then pass "seeded generator exists"; else fail "seeded generator MISSING"; fi
if [[ -f "$EX_DIR/run-output.txt" ]]; then pass "examples/run-output.txt exists"; else fail "examples/run-output.txt MISSING"; fi
if [[ -f "$EX_DIR/README.md" ]]; then pass "examples/README.md exists"; else fail "examples/README.md MISSING"; fi
if [[ -x "$SKILL_DIR/scripts/verify-skill.sh" ]]; then pass "verify-skill.sh is executable"; else fail "verify-skill.sh is NOT executable (chmod +x)"; fi

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
for field in description license author type status version updated token_budget; do
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
if grep -q 'consumes_from: \[trade-performance-analyst\]' "$SKILL_MD" 2>/dev/null; then
  pass "chain.consumes_from is exactly [trade-performance-analyst]"
else
  fail "chain.consumes_from is not the required exact block"
fi
if grep -q 'feeds_into: \[\]' "$SKILL_MD" 2>/dev/null; then
  pass "chain.feeds_into is exactly []"
else
  fail "chain.feeds_into is not the required exact block"
fi
if grep -q 'skills/14-finance/timeframe-performance-statistics/examples/logs' "$SKILL_MD" 2>/dev/null; then
  pass "chain.examples path points at this skill's log directory"
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
if grep -q '^\*\*Downstream' "$SKILL_MD" || grep -q '### Downstream' "$SKILL_MD"; then pass "Cross-Skill Coordination: Downstream table present"; else fail "Cross-Skill Coordination: Downstream table missing"; fi
if grep -q "Portability target" "$SKILL_MD"; then pass "Portability target declared"; else fail "Missing Portability target declaration"; fi

BP_COUNT=$(sed -n '/^## Best Practices/,/^## Error Decoder/p' "$SKILL_MD" | grep -cE '^[0-9]+\. ' || true)
check_ge "Best Practices numbered items" "${BP_COUNT:-0}" 10

CR_COUNT=$(sed -n '/^## Production Checklist/,/^## What Good Looks Like/p' "$SKILL_MD" | grep -oE 'CR[0-9]+' | wc -l | tr -d ' ')
check_ge "Production Checklist CR items" "${CR_COUNT:-0}" 10

AP_COUNT=$(sed -n '/^## Anti-Patterns/,/^## State Log/p' "$SKILL_MD" | grep -c '❌' || true)
check_ge "Anti-Patterns entries" "${AP_COUNT:-0}" 5

ED_COLS=$(sed -n '/^## Error Decoder/,/^## Error Recovery/p' "$SKILL_MD" | grep -m1 '^|' | awk -F'|' '{print NF-2}')
check_ge "Error Decoder columns" "${ED_COLS:-0}" 4

# ── Block E: Anti-hallucination guardrails ──────────────────────────────────
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

CITE=$(count_matches 'source.*:|data from|verified against|CBOE|Cboe|Yahoo Finance|Bloomberg|published by|exchange rules' "$SKILL_MD" -i)
check_ge "Research citations (source lines and named sources)" "${CITE:-0}" 8

if grep -q 'ILLUSTRATIVE' "$SKILL_MD" && grep -q 'SYNTHETIC' "$SKILL_MD"; then
  pass "synthetic logs are labelled SYNTHETIC / ILLUSTRATIVE in the doc"
else
  fail "synthetic logs are not labelled in SKILL.md"
fi
if grep -qi 'not a backtest\|never be quoted as a finding\|carries no market information' "$SKILL_MD"; then
  pass "the 'not a result / not market data' disclaimer is present"
else
  fail "the synthetic-data disclaimer is missing"
fi
if grep -qi 'could not be verified\|unverified\|not verifiable' "$SKILL_MD"; then
  pass "unverified claims are labelled as unverified"
else
  fail "no explicit unverified-claim disclosure found"
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

if grep -q 'exit condition\|exit plan\|stop-loss\|stop loss' "$SKILL_MD"; then
  pass "exit conditions / exit plan documented"
else
  fail "no exit conditions documented"
fi

FAILMODE_REFS=$(cat "$REF_DIR"/*.md | grep -cE '^[0-9]+\. \*\*' || true)
check_ge "Numbered failure-mode rows across reference files" "${FAILMODE_REFS:-0}" 10

# ── Block H: References ─────────────────────────────────────────────────────
echo ""
echo "--- References ---"
REF_COUNT=$(find "$REF_DIR" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
check_ge "Reference files on disk" "${REF_COUNT:-0}" 9

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

LINKED=$(grep -ohE '\(references/[^)]*\.md\)' "$SKILL_MD" 2>/dev/null | sort -u | wc -l | tr -d ' ')
if [[ "${LINKED:-0}" -ge "${REF_COUNT:-0}" ]]; then
  pass "every reference file is linked from SKILL.md ($LINKED linked, $REF_COUNT on disk)"
else
  fail "unlinked reference files: $(( REF_COUNT - LINKED ))"
fi

# ── Block I: The engine runs, and is deterministic ─────────────────────────
echo ""
echo "--- Engine: runs and is deterministic ---"
if $PY "$ENGINE" --version >"$TMP/version.txt" 2>&1; then
  pass "engine --version runs: $(cat "$TMP/version.txt")"
else
  fail "engine --version failed"
fi

for pair in "$HAND_LOG:hand" "$YEAR_LOG:year"; do
  log="${pair%%:*}"; tag="${pair##*:}"
  if $PY "$ENGINE" --csv "$log" >"$TMP/$tag.1.txt" 2>&1; then
    pass "engine runs on $(basename "$log")"
  else
    fail "engine FAILED on $(basename "$log")"
    continue
  fi
  $PY "$ENGINE" --csv "$log" >"$TMP/$tag.2.txt" 2>&1
  if diff -q "$TMP/$tag.1.txt" "$TMP/$tag.2.txt" >/dev/null 2>&1; then
    pass "engine text output is byte-identical across two runs: $(basename "$log")"
  else
    fail "engine text output is NOT deterministic: $(basename "$log")"
  fi
  $PY "$ENGINE" --json "$log" >"$TMP/$tag.1.json" 2>&1
  $PY "$ENGINE" --json "$log" >"$TMP/$tag.2.json" 2>&1
  if diff -q "$TMP/$tag.1.json" "$TMP/$tag.2.json" >/dev/null 2>&1; then
    pass "engine JSON output is byte-identical across two runs: $(basename "$log")"
  else
    fail "engine JSON output is NOT deterministic: $(basename "$log")"
  fi
  $PY "$ENGINE" --csv-out "$TMP/$tag.1.csv" "$log" >/dev/null 2>&1
  $PY "$ENGINE" --csv-out "$TMP/$tag.2.csv" "$log" >/dev/null 2>&1
  if diff -q "$TMP/$tag.1.csv" "$TMP/$tag.2.csv" >/dev/null 2>&1; then
    pass "engine --csv-out is byte-identical across two runs: $(basename "$log")"
  else
    fail "engine --csv-out is NOT deterministic: $(basename "$log")"
  fi
done

# The generator must be deterministic too: same seed, same bytes.
if $PY "$LOG_DIR/generate_synthetic.py" >"$TMP/gen.log" 2>&1; then
  cp "$YEAR_LOG" "$TMP/gen.1.csv"
  $PY "$LOG_DIR/generate_synthetic.py" >/dev/null 2>&1
  if diff -q "$TMP/gen.1.csv" "$YEAR_LOG" >/dev/null 2>&1; then
    pass "seeded generator is byte-identical on re-run (seed fixed)"
  else
    fail "seeded generator is NOT deterministic — the illustrative log has changed"
  fi
else
  fail "seeded generator failed to run"
fi

# ── Block J: The hand-check arithmetic ─────────────────────────────────────
# Every value asserted below is written in the header of
# examples/logs/hand-check-synthetic.csv as the expected value, computed by
# hand. If the engine and the hand arithmetic ever diverge, this block fails.
# Values are read by NAME from the engine's --json output.
echo ""
echo "--- Hand-Check Arithmetic (engine vs the file's documented expectations) ---"
HB="$TMP/hand.out.txt"
cp "$TMP/hand.1.txt" "$HB" 2>/dev/null || $PY "$ENGINE" --csv "$HAND_LOG" >"$HB" 2>&1
HFD="$TMP/hand.fields.tsv"
$PY "$ENGINE" --json "$HAND_LOG" > "$TMP/hand.json" 2>&1
dump_fields "$TMP/hand.json" "$HFD"

# Coverage: 6 daily periods, 6 weekly periods, 4 two-week periods, 2 monthly.
assert_field "D bucket: 6 periods"                  "$HFD" "D"  "n_periods" "6"
assert_field "W bucket: 6 periods"                  "$HFD" "W"  "n_periods" "6"
assert_field "2W bucket: 4 periods"                 "$HFD" "2W" "n_periods" "4"
assert_field "M bucket: 2 periods"                  "$HFD" "M"  "n_periods" "2"
assert_field "Q bucket: 1 period"                   "$HFD" "Q"  "n_periods" "1"
assert_field "every bucket holds all 6 trades"      "$HFD" "M"  "n_trades" "6"
assert_field "D bucket: 1.000 trades per period"    "$HFD" "D"  "trades_per_period" "1.000"
assert_field "M bucket: 3.000 trades per period"    "$HFD" "M"  "trades_per_period" "3.000"
assert_field "M bucket: 12.000 periods per year"    "$HFD" "M"  "periods_per_year" "12.000"

# Monthly bucket, period-by-period (hand-computed in the CSV header). These two
# rows are asserted as verbatim CSV lines, because they carry every per-period
# field the engine computes for that period.
assert_engine_value "2025-01 period row: net 150.00" "$HB" "M,2025-01,2025-01,3,250.00,100.00,150.00,1,1,1,0.500000,250.00,100.00,2.500000,50.00,2.500000,0.285714,0.214286"
assert_engine_value "2025-02 period row: net 225.00" "$HB" "M,2025-02,2025-02,3,375.00,150.00,225.00,2,1,0,0.666667,187.50,150.00,1.250000,75.00,2.500000,0.444444,0.222222"

# Monthly bucket, across periods: mean 187.5, sd 53.033009, t = 5.0 exactly.
assert_field "M mean_period_pnl = 187.50"           "$HFD" "M" "mean_period_pnl" "187.50" 0.006
assert_field "M median_period_pnl = 187.50"         "$HFD" "M" "median_period_pnl" "187.50" 0.006
assert_field "M sd_period_pnl = 53.033009"          "$HFD" "M" "sd_period_pnl" "53.033009"
assert_field "M t_stat = 5.000000"                  "$HFD" "M" "t_stat" "5.000000"
assert_field "M period_sharpe = 3.535534"           "$HFD" "M" "period_sharpe" "3.535534"
assert_field "M cumulative_pnl = 375.00"            "$HFD" "M" "cumulative_pnl" "375.00" 0.006
assert_field "M max_drawdown = 0.00"                "$HFD" "M" "max_drawdown" "0.00" 0.006
assert_field "M lag1_autocorrelation = n/a (2 periods)" "$HFD" "M" "lag1_autocorrelation" "n/a"
assert_field "M n_eff = n/a (2 periods)"            "$HFD" "M" "n_eff" "n/a"

# Monthly bucket, pooled beat-losses: win_rate .6, payoff 1.666667,
# break-even .375, edge .225, se .219089, 2se .438178 -> FAIL.
assert_field "M win_rate = 0.600000"                "$HFD" "M" "win_rate" "0.600000"
assert_field "M avg_win = 208.333333"               "$HFD" "M" "avg_win" "208.333333" 0.006
assert_field "M avg_loss = 125.00"                  "$HFD" "M" "avg_loss" "125.00" 0.006
assert_field "M payoff_ratio = 1.666667"            "$HFD" "M" "payoff_ratio" "1.666667"
assert_field "M expectancy_per_trade = 62.50"       "$HFD" "M" "expectancy_per_trade" "62.50" 0.006
assert_field "M profit_factor = 2.500000"           "$HFD" "M" "profit_factor" "2.500000"
assert_field "M break_even_win_rate = 0.375000"     "$HFD" "M" "break_even_win_rate" "0.375000"
assert_field "M edge = 0.225000"                    "$HFD" "M" "edge" "0.225000"
assert_field "M se_win_rate = 0.219089"             "$HFD" "M" "se_win_rate" "0.219089"
assert_field "M 2 x se_win_rate = 0.438178"         "$HFD" "M" "_two_se" "0.438178"
assert_field "M edge_test = FAIL"                   "$HFD" "M" "edge_test" "FAIL"

# Daily bucket: series 250,-100,0,300,-150,75 -> mean 62.5,
# sd sqrt(167187.5/5) = 182.859235, t = 0.837218, sharpe 0.341793,
# max_drawdown -150.00, rho -0.614264, n_eff raw 25.109 capped to 6.
assert_field "D mean_period_pnl = 62.50"            "$HFD" "D" "mean_period_pnl" "62.50" 0.006
assert_field "D median_period_pnl = 37.50"          "$HFD" "D" "median_period_pnl" "37.50" 0.006
assert_field "D sd_period_pnl = 182.859235"         "$HFD" "D" "sd_period_pnl" "182.859235"
assert_field "D t_stat = 0.837218"                  "$HFD" "D" "t_stat" "0.837218"
assert_field "D period_sharpe = 0.341793"           "$HFD" "D" "period_sharpe" "0.341793"
assert_field "D max_drawdown = -150.00"             "$HFD" "D" "max_drawdown" "-150.00" 0.006
assert_field "D lag1_autocorrelation = -0.614264"   "$HFD" "D" "lag1_autocorrelation" "-0.614264"
assert_field "D n_eff raw = 25.109366 (capped below)" "$HFD" "D" "n_eff" "25.109366"
assert_field "D n_eff_capped = 6.000 (the trade count)" "$HFD" "D" "n_eff_capped" "6.000"
assert_field "D edge_test = FAIL"                   "$HFD" "D" "edge_test" "FAIL"

# Two-week bucket: series 250,-100,300,-75 -> mean 93.75,
# sd sqrt(132968.75/3) = 210.530085, t = 0.890609, sharpe 0.445305,
# max_drawdown -100.00, rho -0.985453, n_eff raw 545.952 capped to 6.
assert_field "2W mean_period_pnl = 93.75"           "$HFD" "2W" "mean_period_pnl" "93.75" 0.006
assert_field "2W sd_period_pnl = 210.530085"        "$HFD" "2W" "sd_period_pnl" "210.530085"
assert_field "2W t_stat = 0.890609"                 "$HFD" "2W" "t_stat" "0.890609"
assert_field "2W period_sharpe = 0.445305"          "$HFD" "2W" "period_sharpe" "0.445305"
assert_field "2W max_drawdown = -100.00"            "$HFD" "2W" "max_drawdown" "-100.00" 0.006
assert_field "2W lag1_autocorrelation = -0.985453"  "$HFD" "2W" "lag1_autocorrelation" "-0.985453"
assert_field "2W n_eff raw = 545.952 (impossible)"  "$HFD" "2W" "n_eff" "545.952"
assert_field "2W n_eff_capped = 6.000 (the guard fires)" "$HFD" "2W" "n_eff_capped" "6.000"

# Single-period buckets: sd and t_stat are refusals, not zeros.
assert_field "Q (one period) -> sd_period_pnl n/a"  "$HFD" "Q" "sd_period_pnl" "n/a"
assert_field "Q (one period) -> t_stat n/a"         "$HFD" "Q" "t_stat" "n/a"
assert_field "Q (one period) -> period_sharpe n/a"  "$HFD" "Q" "period_sharpe" "n/a"
assert_field "Q (one period) -> lag1 n/a"           "$HFD" "Q" "lag1_autocorrelation" "n/a"
assert_field "Y (one period) -> n_eff n/a"          "$HFD" "Y" "n_eff" "n/a"

# The verdict on a 6-trade, 2-month log must be INSUFFICIENT DATA.
assert_field "verdict bucket = n/a"                 "$HFD" "VERDICT" "bucket" "n/a"
assert_field "verdict status = INSUFFICIENT DATA"   "$HFD" "VERDICT" "status" "INSUFFICIENT DATA"
assert_engine_value "verdict is INSUFFICIENT DATA (text output)" "$HB" "INSUFFICIENT DATA"
assert_engine_value "the failing constraint is named per bucket" "$HB" "n_periods=2 < 12"
assert_engine_value "the dependence caveat is printed"           "$HB" "DEPENDENCE CAVEAT -- these buckets are not independent tests"

# ── Block K: The illustrative log's documented properties ──────────────────
echo ""
echo "--- Illustrative Log (structural properties) ---"
YS="$TMP/year.out.txt"
cp "$TMP/year.1.txt" "$YS" 2>/dev/null || $PY "$ENGINE" --csv "$YEAR_LOG" >"$YS" 2>&1
YFD="$TMP/year.fields.tsv"
$PY "$ENGINE" --json "$YEAR_LOG" > "$TMP/year.json" 2>&1
dump_fields "$TMP/year.json" "$YFD"

assert_engine_value "120 trades in the illustrative log"            "$YS" "trade rows      : 120"
assert_field "every bucket reports all 120 trades"                  "$YFD" "D"  "n_trades" "120"
assert_field "D has 120 periods"                                    "$YFD" "D"  "n_periods" "120"
assert_field "W has 53 periods"                                     "$YFD" "W"  "n_periods" "53"
assert_field "W trades_per_period 2.264 (fails the gate)"           "$YFD" "W"  "trades_per_period" "2.264151"
assert_field "2W has 27 periods"                                    "$YFD" "2W" "n_periods" "27"
assert_field "2W trades_per_period 4.444 (the near miss)"           "$YFD" "2W" "trades_per_period" "4.444444"
assert_field "M has 13 periods"                                     "$YFD" "M"  "n_periods" "13"
assert_field "Q has 5 periods"                                      "$YFD" "Q"  "n_periods" "5"
assert_field "H has 3 periods"                                      "$YFD" "H"  "n_periods" "3"
assert_field "Y has 2 periods"                                      "$YFD" "Y"  "n_periods" "2"
assert_field "verdict bucket is M"                                  "$YFD" "VERDICT" "bucket" "M"
assert_field "verdict status is noise"                              "$YFD" "VERDICT" "status" "NOT DISTINGUISHABLE FROM NOISE"
assert_field "verdict t_stat is 0.948"                              "$YFD" "VERDICT" "t_stat" "0.947858"
assert_field "verdict n_periods is 13, not more"                    "$YFD" "VERDICT" "n_periods" "13"
assert_field "verdict carries n_eff = 10.782"                       "$YFD" "VERDICT" "n_eff" "10.781742"

# The across-period statistics that the skill's prose quotes.
assert_field "D t_stat = 1.293"                                     "$YFD" "D" "t_stat" "1.292616"
assert_field "W t_stat = 1.113"                                     "$YFD" "W" "t_stat" "1.112656"
assert_field "2W t_stat = 1.056"                                    "$YFD" "2W" "t_stat" "1.055792"
assert_field "M t_stat = 0.948"                                     "$YFD" "M" "t_stat" "0.947858"
assert_field "Q t_stat = 0.852"                                     "$YFD" "Q" "t_stat" "0.852410"
assert_field "H t_stat = 0.574"                                     "$YFD" "H" "t_stat" "0.573835"
assert_field "Y t_stat = 2.079 on only 2 periods"                   "$YFD" "Y" "t_stat" "2.079016"
assert_field "D n_eff = 77.894 (loses 35% to clustering)"           "$YFD" "D" "n_eff" "77.893871"
assert_field "W n_eff = 45.866"                                     "$YFD" "W" "n_eff" "45.866199"
assert_field "2W n_eff = 18.079"                                    "$YFD" "2W" "n_eff" "18.078597"
assert_field "M n_eff = 10.782 (below its 13 periods)"              "$YFD" "M" "n_eff" "10.781742"
assert_field "Q n_eff = 4.687"                                      "$YFD" "Q" "n_eff" "4.687261"
assert_field "H rho = -1.000000, refused by the guard"              "$YFD" "H" "lag1_autocorrelation" "-1.000000"
assert_field "H n_eff = n/a (guard fired)"                          "$YFD" "H" "n_eff" "n/a"
assert_field "Y lag1 = n/a (2 periods)"                             "$YFD" "Y" "lag1_autocorrelation" "n/a"
assert_field "D rho = 0.212771"                                     "$YFD" "D" "lag1_autocorrelation" "0.212771"
assert_field "D period_sharpe = 0.118019"                           "$YFD" "D" "period_sharpe" "0.118019"
assert_field "M period_sharpe = 0.262889"                           "$YFD" "M" "period_sharpe" "0.262889"
assert_field "Y period_sharpe = 1.470086"                           "$YFD" "Y" "period_sharpe" "1.470086"

# Drawdown by bucket: the table the skill's prose quotes.
assert_field "D drawdown = -2,007.03 (the real fall)"                "$YFD" "D"  "max_drawdown" "-2007.03" 0.006
assert_field "W drawdown = -1,859.05"                               "$YFD" "W"  "max_drawdown" "-1859.05" 0.006
assert_field "2W drawdown = -1,853.02"                              "$YFD" "2W" "max_drawdown" "-1853.02" 0.006
assert_field "M drawdown = -1,656.33"                               "$YFD" "M"  "max_drawdown" "-1656.33" 0.006
assert_field "Q drawdown = -1,082.85"                               "$YFD" "Q"  "max_drawdown" "-1082.85" 0.006
assert_field "H drawdown = -1,082.85 (same as Q)"                   "$YFD" "H"  "max_drawdown" "-1082.85" 0.006
assert_field "Y drawdown = 0.00 against a real daily fall"           "$YFD" "Y"  "max_drawdown" "0.00" 0.006

# Pooled beat-losses: win_rate .55, payoff 1.045703, break-even .488829,
# edge .061171, se .045415, 2se .090830 -> FAIL. Identical in every bucket.
for bk in D W 2W M Q H Y; do
  assert_field "$bk pooled win_rate = 0.550000"                     "$YFD" "$bk" "win_rate" "0.550000"
  assert_field "$bk pooled edge = 0.061171"                         "$YFD" "$bk" "edge" "0.061171"
done
assert_field "M pool payoff_ratio = 1.045703"                       "$YFD" "M" "payoff_ratio" "1.045703"
assert_field "M pool break_even_win_rate = 0.488829"                "$YFD" "M" "break_even_win_rate" "0.488829"
assert_field "M pool se_win_rate = 0.045415"                        "$YFD" "M" "se_win_rate" "0.045415"
assert_field "M pool 2 x se = 0.090830"                             "$YFD" "M" "_two_se" "0.090830"
assert_field "M beat-losses test FAILs at 120 trades"               "$YFD" "M" "edge_test" "FAIL"
assert_field "pooled gross_profit = 7,851.87"                       "$YFD" "M" "gross_profit" "7851.87" 0.006
assert_field "pooled gross_loss = 6,143.48"                         "$YFD" "M" "gross_loss" "6143.48" 0.006
assert_field "pooled net_pnl = 1,708.39"                            "$YFD" "M" "net_pnl" "1708.39" 0.006
assert_field "pooled cumulative_pnl = 1,708.39"                     "$YFD" "M" "cumulative_pnl" "1708.39" 0.006
assert_field "pooled expectancy_per_trade = 14.24"                  "$YFD" "M" "expectancy_per_trade" "14.236583" 0.006
assert_field "pooled profit_factor = 1.278"                         "$YFD" "M" "profit_factor" "1.278149"
assert_field "pooled avg_win = 118.97"                              "$YFD" "M" "avg_win" "118.967727" 0.006
assert_field "pooled avg_loss = 113.77"                             "$YFD" "M" "avg_loss" "113.768148" 0.006
assert_field "0 break-even trades in the illustrative log"          "$YFD" "M" "breakeven_trades" "0"

# Text-output assertions: the prose the skill cites verbatim.
assert_engine_value "M is the verdict bucket"                       "$YS" "VERDICT: M is the most reliable review timeframe"
assert_engine_value "verdict is capped by dependence"               "$YS" "CONFIDENCE IS CAPPED BY DEPENDENCE"
assert_engine_value "t_stat and n_eff are on the verdict line"      "$YS" "n_periods = 13, n_eff = 10.78 (capped: 10.78)"
assert_engine_value "the dependence caveat is printed unconditionally" "$YS" "DEPENDENCE CAVEAT -- these buckets are not independent tests"
assert_engine_value "the verdict rule is stated in the output"      "$YS" "rank buckets by descending |t_stat|"
assert_engine_value "the near-miss gate failure is named"           "$YS" "2W   : trades_per_period=4.44 < 5"
assert_engine_value "D fails on trades per period, not periods"     "$YS" "D    : trades_per_period=1.00 < 5"
assert_engine_value "Y fails on period count"                       "$YS" "Y    : n_periods=2 < 12"
assert_engine_value "the bucketing-invariance is stated"            "$YS" "this test is bucketing-INVARIANT by construction"
assert_engine_value "the synthetic provenance is echoed into output" "$YS" "SYNTHETIC / ILLUSTRATIVE"
assert_engine_value "the input is labelled not-a-backtest"          "$YS" "NOT a backtest"
assert_engine_value "the engine refuses to annualise Sharpe"        "$YS" "does NOT annualise a"

# ── Block L: Scope discipline / deferrals ──────────────────────────────────
echo ""
echo "--- Scope Discipline ---"
for defer in 'trade-performance-analyst' 'trade-sizing-recovery' 'portfolio-signal-manager' \
             'algorithmic-trader' 'options-position-lifecycle' 'equity-position-lifecycle' \
             'trading-decision-data-catalogue'; do
  if grep -q "$defer" "$SKILL_MD" 2>/dev/null; then
    pass "defers to: $defer"
  else
    fail "no deferral to: $defer"
  fi
done
if grep -qi 'does not redefine\|refuses to redefine\|owned by' "$SKILL_MD"; then
  pass "the metric-definition handoff is stated as a refusal"
else
  fail "the metric-definition handoff is not stated"
fi
if grep -q 'quarter to half\|one-quarter to one-half\|quarter-to-half' "$SKILL_MD"; then
  pass "the cadence rule (quarter-to-half of the holding period) is stated"
else
  fail "the cadence rule is missing from SKILL.md"
fi
if grep -q 'review-cadence-by-dte-zone.md' "$SKILL_MD"; then
  pass "the options-position-lifecycle cadence table is cited"
else
  fail "the options-position-lifecycle cadence table is not cited"
fi
if grep -q 'equity-time-axes-cadence.md\|equity-position-lifecycle' "$SKILL_MD"; then
  pass "the equity-position-lifecycle cadence table is cited"
else
  fail "the equity-position-lifecycle cadence table is not cited"
fi
TRAP_COUNT=$(sed -n '/### The twelve traps/,/### Regime Table/p' "$SKILL_MD" | grep -cE '^[0-9]+\. \*\*Trap' || true)
check_ge "Numbered traps with countermeasures" "${TRAP_COUNT:-0}" 10

# ── Block M: examples/run-output.txt is fresh ──────────────────────────────
echo ""
echo "--- run-output.txt Freshness ---"
if [[ -f "$EX_DIR/run-output.txt" ]]; then
  # Re-run both documented commands and confirm their output is inside the
  # captured file, token by token, so a stale capture fails loudly.
  for token in "VERDICT: M is the most reliable review timeframe" \
               "n_eff_capped" \
               "SYNTHETIC / ILLUSTRATIVE"; do
    if grep -qF -- "$token" "$EX_DIR/run-output.txt"; then
      pass "run-output.txt contains this run's output: $(echo "$token" | cut -c1-46)"
    else
      fail "run-output.txt is STALE — missing: $token"
    fi
  done
  if grep -q 'RUN 1 of 2' "$EX_DIR/run-output.txt" && grep -q 'RUN 2 of 2' "$EX_DIR/run-output.txt"; then
    pass "run-output.txt shows both documented command lines"
  else
    fail "run-output.txt does not show both documented command lines"
  fi
else
  fail "run-output.txt missing"
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
