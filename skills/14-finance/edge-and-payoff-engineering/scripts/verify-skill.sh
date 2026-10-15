#!/usr/bin/env bash
# ============================================================================
# verify-skill.sh — self-verification for edge-and-payoff-engineering
# ============================================================================
# Structural, provenance, gate, arithmetic and determinism checks for this
# skill. Bash 3.2 compatible, no third-party dependencies, no network.
# Exits 0 when every check passes, 1 otherwise.
#
# The three checks that make this script more than a lint:
#   (a) it runs the engine on the ten-trade hand-check ledger and asserts the
#       expected values WRITTEN IN THAT FILE'S OWN HEADER, so the documented
#       arithmetic and the shipped code cannot drift apart;
#   (b) it asserts the engine is DETERMINISTIC by running it twice on both
#       ledgers and diffing text and JSON;
#   (c) it asserts the shipped illustrative ledger still carries the four
#       constructed cohort verdicts (KEEP / KILL / INSUFFICIENT / KILL).
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
ENGINE="$SKILL_DIR/scripts/edge_engine.py"
HAND_LOG="$LOG_DIR/hand-check-synthetic.csv"
ILL_LOG="$LOG_DIR/illustrative-cohorts-synthetic.csv"
GEN="$LOG_DIR/generate_synthetic.py"

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
TMP="$(mktemp -d 2>/dev/null || mktemp -d -t edgeengine)"
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
    pass "$label"
  else
    fail "MISSING from engine output: $label (looked for: $token)"
  fi
}

# assert_field <label> <fields-file> <bucket> <field> <expected> [tolerance]
# Reads the flat "bucket<TAB>field<TAB>value" dump, so a value is asserted by
# NAME rather than by its column position in a padded table.
assert_field() {
  local label="$1" file="$2" bucket="$3" field="$4" expect="$5" tol="${6:-0.0000005}"
  local row
  row="$(awk -F'\t' -v b="$bucket" -v f="$field" '$1==b && $2==f {print $3; exit}' "$file")"
  if [[ "$row" == "$expect" ]]; then
    pass "$label"
    return 0
  fi
  if [[ "$row" =~ ^-?[0-9] && "$expect" =~ ^-?[0-9] ]]; then
    if awk -v a="$row" -v b="$expect" -v t="$tol" 'BEGIN{d=a-b; if(d<0)d=-d; exit !(d<=t)}'; then
      pass "$label"
      return 0
    fi
  fi
  fail "FAILED: $label (wanted $bucket.$field = $expect, got ${row:-<absent>})"
}

# assert_contains <label> <file> <substring>
assert_contains() {
  local label="$1" file="$2" token="$3"
  if grep -qF -- "$token" "$file" 2>/dev/null; then
    pass "$label"
  else
    fail "FAILED: $label (looked for: $token)"
  fi
}

# dump_fields <json-file> <out-file> -> "bucket<TAB>field<TAB>value" per line
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


for k in ("units_mode", "r_dollars"):
    emit("meta", k, data.get(k))
for k, v in sorted(data.get("cost", {}).items()):
    emit("cost", k, v)
for k, v in sorted(data.get("multiple_testing", {}).items()):
    emit("mt", k, v)
for k, v in sorted(data.get("pooled", {}).items()):
    if isinstance(v, (list, dict)):
        continue
    emit("pooled", k, v)
for c in data.get("cohorts", []):
    b = "coh:%s:%s" % (c["dimension"], c["cohort"])
    for k in sorted(c):
        v = c[k]
        if isinstance(v, (list, dict)):
            continue
        emit(b, k, v)
for lv in data.get("levers", []):
    sys.stdout.write("lever\t%s\t%s\n" % (lv["lever"], lv["delta_E_net"]))
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
if [[ -f "$ENGINE" ]]; then pass "engine exists: scripts/edge_engine.py"; else fail "engine MISSING: scripts/edge_engine.py"; fi
if [[ -f "$HAND_LOG" ]]; then pass "hand-check ledger exists"; else fail "hand-check ledger MISSING"; fi
if [[ -f "$ILL_LOG" ]]; then pass "illustrative ledger exists"; else fail "illustrative ledger MISSING"; fi
if [[ -f "$GEN" ]]; then pass "seeded generator exists"; else fail "seeded generator MISSING"; fi
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
if grep -q 'consumes_from: \[timeframe-performance-statistics, trade-performance-analyst\]' "$SKILL_MD" 2>/dev/null; then
  pass "chain.consumes_from is exactly [timeframe-performance-statistics, trade-performance-analyst]"
else
  fail "chain.consumes_from is not the required exact block"
fi
if grep -q 'feeds_into: \[\]' "$SKILL_MD" 2>/dev/null; then
  pass "chain.feeds_into is exactly []"
else
  fail "chain.feeds_into is not the required exact block"
fi
if grep -q 'skills/14-finance/edge-and-payoff-engineering/examples/logs' "$SKILL_MD" 2>/dev/null; then
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
for phrase in "how do I make money" "why do I keep losing" "my win rate is high" \
              "is my edge real" "what payoff do I need" "which setups should I stop trading" \
              "how many trades before I know" "what should my risk per trade be"; do
  if grep -qF -- "$phrase" "$SKILL_MD"; then
    pass "description triggers on: $phrase"
  else
    fail "description does not trigger on: $phrase"
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
check_ge "Numbered traps with countermeasures" \
  "$(sed -n '/^### The twelve traps/,/^### Regime Table/p' "$SKILL_MD" | grep -cE '^[0-9]+\. \*\*Trap' || true)" 10

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
echo "--- Provenance & Citations (G14 finance thresholds, verified with grep) ---"
PROV_LINES=$(grep -cE '\[VERIFIED|\[COMPUTED|\[ESTIMATED|\[ILLUSTRATIVE|\[COMMON-PRACTICE' "$SKILL_MD" || true)
check_ge "Lines carrying a provenance tag" "${PROV_LINES:-0}" 9

CITE=$(count_matches 'source.*:|data from|verified against|CBOE|Cboe|Yahoo Finance|Bloomberg|published by|exchange rules' "$SKILL_MD" -i)
check_ge "Research citations (source lines and named sources)" "${CITE:-0}" 8

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

if grep -q 'SYNTHETIC' "$SKILL_MD" && grep -q 'ILLUSTRATIVE' "$SKILL_MD"; then
  pass "synthetic ledgers are labelled SYNTHETIC / ILLUSTRATIVE in the doc"
else
  fail "synthetic ledgers are not labelled in SKILL.md"
fi
if grep -qi 'never be quoted as a finding\|not a backtest\|must never be quoted' "$SKILL_MD"; then
  pass "the 'not a result / not market data' disclaimer is present"
else
  fail "the synthetic-data disclaimer is missing"
fi
if grep -qi 'could not be verified\|unverified\|not verifiable\|was not checked' "$SKILL_MD"; then
  pass "unverified claims are labelled as unverified"
else
  fail "no explicit unverified-claim disclosure found"
fi

# ── Block G: References ─────────────────────────────────────────────────────
echo ""
echo "--- References ---"
REF_COUNT=$(find "$REF_DIR" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
check_ge "Reference files on disk" "${REF_COUNT:-0}" 10

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
  fail "unlinked reference files (orphans): $(( REF_COUNT - LINKED ))"
fi

# ── Block H: The engine runs, and is deterministic ─────────────────────────
echo ""
echo "--- Engine: runs and is deterministic ---"
if $PY "$ENGINE" --version >"$TMP/version.txt" 2>&1; then
  pass "engine --version runs: $(cat "$TMP/version.txt")"
else
  fail "engine --version failed"
fi

for pair in "$HAND_LOG:hand" "$ILL_LOG:ill"; do
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
done

# The generator must be deterministic too: same seed, same bytes.
if $PY "$GEN" >"$TMP/gen.log" 2>&1; then
  cp "$ILL_LOG" "$TMP/gen.1.csv"
  $PY "$GEN" >/dev/null 2>&1
  if diff -q "$TMP/gen.1.csv" "$ILL_LOG" >/dev/null 2>&1; then
    pass "seeded generator is byte-identical on re-run (seed fixed)"
  else
    fail "seeded generator is NOT deterministic — the illustrative ledger changed"
  fi
else
  fail "seeded generator failed to run"
fi

# ── Block I: Robustness — degenerate ledgers must not crash ────────────────
echo ""
echo "--- Robustness (degenerate ledgers must not crash) ---"
printf 'trade_id,open_date,close_date,pnl,risk,setup\n' > "$TMP/empty.csv"
printf 'trade_id,open_date,close_date,pnl,risk,setup\nW1,2026-01-01,2026-01-02,100,100,A\nW2,2026-01-02,2026-01-03,200,100,A\n' > "$TMP/allwins.csv"
printf 'trade_id,open_date,close_date,pnl,risk,setup\nL1,2026-01-01,2026-01-02,-100,100,A\nL2,2026-01-02,2026-01-03,-50,100,A\n' > "$TMP/allloss.csv"
printf 'trade_id,open_date,close_date,pnl,risk,setup\nS1,2026-01-01,2026-01-02,60,100,A\n' > "$TMP/single.csv"
printf 'trade_id,open_date,close_date,pnl\nN1,2026-01-01,2026-01-02,500\nN2,2026-01-02,2026-01-03,-250\n' > "$TMP/norisk.csv"
printf 'trade_id,open_date,close_date,pnl,risk\nR1,2026-01-01,2026-01-02,500,250\nR2,2026-01-02,2026-01-03,-250,\n' > "$TMP/partial.csv"
for f in empty allwins allloss single norisk partial; do
  if $PY "$ENGINE" "$TMP/$f.csv" >"$TMP/$f.out.txt" 2>&1; then
    pass "engine survives the '$f' ledger (exit 0)"
  else
    fail "engine CRASHED or errored on the '$f' ledger"
  fi
done
if grep -q 'CURRENCY MODE' "$TMP/norisk.out.txt"; then
  pass "a ledger with no risk column drops to CURRENCY MODE and says so"
else
  fail "no risk column did NOT trigger the CURRENCY MODE disclosure"
fi
if grep -q 'partial risk' "$TMP/norisk.out.txt" || grep -q 'no positive risk' "$TMP/partial.out.txt"; then
  pass "a partially blank risk column is refused and the offending line is named"
else
  fail "a partially blank risk column was NOT refused"
fi
if grep -q 'COST IS ZERO' "$TMP/hand.1.txt"; then
  pass "the zero-cost warning fires on the cost-less hand-check ledger"
else
  fail "the zero-cost warning did NOT fire where it is required"
fi
if grep -q 'COST IS ZERO' "$TMP/ill.1.txt"; then
  fail "the zero-cost warning fired on a ledger that HAS a cost column"
else
  pass "the zero-cost warning is silent on a ledger with a cost column"
fi

# ── Block J: The hand-check arithmetic ─────────────────────────────────────
# Every value asserted below is written in the header of
# examples/logs/hand-check-synthetic.csv as a hand-computed expectation. If the
# engine and the documented arithmetic ever diverge, this block fails.
echo ""
echo "--- Hand-Check Arithmetic (engine vs the ledger's own documented expectations) ---"
HB="$TMP/hand.out.txt"
cp "$TMP/hand.1.txt" "$HB" 2>/dev/null || $PY "$ENGINE" --csv "$HAND_LOG" >"$HB" 2>&1
HFD="$TMP/hand.fields.tsv"
dump_fields "$TMP/hand.1.json" "$HFD"

assert_field "mode is R (risk positive on all ten rows)" "$HFD" "meta" "units_mode" "R"
assert_field "n = 10" "$HFD" "pooled" "n" "10"
assert_field "6 wins" "$HFD" "pooled" "wins" "6"
assert_field "4 losses" "$HFD" "pooled" "losses" "4"
assert_field "0 break-even trades" "$HFD" "pooled" "breakeven_trades" "0"
assert_field "p = 0.600000" "$HFD" "pooled" "p" "0.6"
assert_field "avg_win = 1.666667" "$HFD" "pooled" "avg_win" "1.666667" 0.0000005
assert_field "avg_loss = 1.000000" "$HFD" "pooled" "avg_loss" "1.0"
assert_field "b = 1.666667" "$HFD" "pooled" "b" "1.666667" 0.0000005
assert_field "E = 0.600000" "$HFD" "pooled" "E" "0.6"
assert_field "E closed form = 0.600000" "$HFD" "pooled" "E_formula" "0.6"
assert_field "c_R = 0.000000 (no cost column)" "$HFD" "pooled" "c_R" "0.0"
assert_field "E_net = 0.600000" "$HFD" "pooled" "E_net" "0.6"
assert_field "p* = 0.375000" "$HFD" "pooled" "p_star" "0.375" 0.0000005
assert_field "b* = 0.666667" "$HFD" "pooled" "b_star" "0.666667" 0.0000005
assert_field "edge = 0.225000" "$HFD" "pooled" "edge_p" "0.225" 0.0000005
assert_field "Kelly f* = 0.360000" "$HFD" "pooled" "kelly" "0.36"
assert_field "half Kelly = 0.180000" "$HFD" "pooled" "half_kelly" "0.18"
assert_field "sd_R = 1.505545" "$HFD" "pooled" "sd_R" "1.5055453054181622"
assert_field "n_req = 25.185185" "$HFD" "pooled" "n_req" "25.18518518518519"
assert_field "trades_per_year = 57.976190" "$HFD" "pooled" "trades_per_year" "57.976190476190474"
assert_field "years_at_current_pace = 0.434406" "$HFD" "pooled" "years_at_pace" "0.4344056582249602"
assert_field "L formula = 2.512942" "$HFD" "pooled" "L_formula" "2.51294159473206"
assert_field "L simulated = 2.17825" "$HFD" "pooled" "L_sim" "2.17825"
assert_field "R_max_frac = 0.061211 of capital" "$HFD" "pooled" "R_max_frac" "0.06121121695550711"
assert_field "R_max_dollars = 6121.12" "$HFD" "pooled" "R_max_dollars" "6121.121695550711" 0.006
assert_field "verdict is INSUFFICIENT SAMPLE" "$HFD" "pooled" "verdict" "INSUFFICIENT SAMPLE (< n_req trades)"

assert_field "cohort count m = 3 (months only)" "$HFD" "mt" "m_cohorts_tested" "3"
assert_field "Bonferroni alpha = 0.0166667" "$HFD" "mt" "adjusted_alpha" "0.016666666666666666"
assert_field "adjusted z bar = 2.393980" "$HFD" "mt" "z_bar" "2.3939798012415405"
assert_field "0 of 3 cohorts clear the adjusted bar" "$HFD" "mt" "cohorts_clearing_adjusted_bar" "0"

assert_field "2026-01 cohort: n = 4" "$HFD" "coh:month:2026-01" "n" "4"
assert_field "2026-01 cohort: p = 0.75" "$HFD" "coh:month:2026-01" "p" "0.75"
assert_field "2026-01 cohort: E = 1.0" "$HFD" "coh:month:2026-01" "E" "1.0"
assert_field "2026-02 cohort: E = 0.5" "$HFD" "coh:month:2026-02" "E" "0.5"
assert_field "2026-03 cohort: E = 0.0" "$HFD" "coh:month:2026-03" "E" "0.0"
assert_field "2026-03 cohort is INSUFFICIENT" "$HFD" "coh:month:2026-03" "verdict" "INSUFFICIENT (n<30)"

assert_engine_value "text output names the reconciliation row" "$HB" "E (closed form x avg_loss)"
assert_engine_value "text output prints the zero-cost warning" "$HB" "*** COST IS ZERO IN THIS RUN ***"
assert_engine_value "text output prints the streak approximation note" "$HB" "STREAK FORMULA"
assert_engine_value "text output prints the central claim" "$HB" "CENTRAL CLAIM"
assert_engine_value "verdict line printed" "$HB" "VERDICT: INSUFFICIENT SAMPLE (< n_req trades)"
assert_engine_value "the engine echoes the ledger's SYNTHETIC provenance" "$HB" "SYNTHETIC / ILLUSTRATIVE"

# ── Block K: The illustrative ledger's documented cohort structure ─────────
echo ""
echo "--- Illustrative Ledger (the four constructed cohort verdicts) ---"
IS="$TMP/ill.out.txt"
cp "$TMP/ill.1.txt" "$IS" 2>/dev/null || $PY "$ENGINE" --csv "$ILL_LOG" >"$IS" 2>&1
IFD="$TMP/ill.fields.tsv"
dump_fields "$TMP/ill.1.json" "$IFD"

assert_engine_value "200 trades in the illustrative ledger" "$IS" "trade rows      : 200"
assert_field "pooled p = 0.510000" "$IFD" "pooled" "p" "0.51"
assert_field "pooled b = 0.962557" "$IFD" "pooled" "b" "0.9625565823328397"
assert_field "pooled b* = 0.960784" "$IFD" "pooled" "b_star" "0.9607843137254901"
assert_field "pooled E = 0.000941" "$IFD" "pooled" "E" "0.00094053286435547"
assert_field "cost drag c_R = 0.029875" "$IFD" "pooled" "c_R" "0.02987546699875467"
assert_field "pooled E_net = -0.028935" "$IFD" "pooled" "E_net" "-0.0289349341343992"
assert_field "sd_R = 1.072301" "$IFD" "pooled" "sd_R" "1.0723008886275145"
assert_field "n_req = 5199305.93" "$IFD" "pooled" "n_req" "5199305.930354224"
assert_field "years_at_current_pace = 32882.67" "$IFD" "pooled" "years_at_pace" "32882.67405644971"
assert_field "L simulated = 6.80955" "$IFD" "pooled" "L_sim" "6.80955"
assert_field "R_max_frac = 0.019580" "$IFD" "pooled" "R_max_frac" "0.019580344271403156"
assert_field "pooled verdict is NEGATIVE EDGE" "$IFD" "pooled" "verdict" "NEGATIVE EDGE"

assert_field "SETUP-TREND: n = 62" "$IFD" "coh:setup:SETUP-TREND" "n" "62"
assert_field "SETUP-TREND: E_net = +0.244744" "$IFD" "coh:setup:SETUP-TREND" "E_net" "0.2447443685741432"
assert_field "SETUP-TREND verdict KEEP" "$IFD" "coh:setup:SETUP-TREND" "verdict" "KEEP"
assert_field "SETUP-FADE: n = 60" "$IFD" "coh:setup:SETUP-FADE" "n" "60"
assert_field "SETUP-FADE: p = 0.416667" "$IFD" "coh:setup:SETUP-FADE" "p" "0.4166666666666667"
assert_field "SETUP-FADE: E_net = -0.252740" "$IFD" "coh:setup:SETUP-FADE" "E_net" "-0.25273954066729826"
assert_field "SETUP-FADE verdict KILL" "$IFD" "coh:setup:SETUP-FADE" "verdict" "KILL (E_net<=0 with n>=30)"
assert_field "SETUP-EVENT: n = 23 (below the floor)" "$IFD" "coh:setup:SETUP-EVENT" "n" "23"
assert_field "SETUP-EVENT: E_net = -0.001335" "$IFD" "coh:setup:SETUP-EVENT" "E_net" "-0.0013349602580748632"
assert_field "SETUP-EVENT verdict INSUFFICIENT" "$IFD" "coh:setup:SETUP-EVENT" "verdict" "INSUFFICIENT (n<30)"
assert_field "SETUP-CREDIT: n = 55" "$IFD" "coh:setup:SETUP-CREDIT" "n" "55"
assert_field "SETUP-CREDIT: p = 0.618182 (the high win rate)" "$IFD" "coh:setup:SETUP-CREDIT" "p" "0.6181818181818182"
assert_field "SETUP-CREDIT: b = 0.495589 (the bad payoff)" "$IFD" "coh:setup:SETUP-CREDIT" "b" "0.49558912831997437"
assert_field "SETUP-CREDIT: b* = 0.617647" "$IFD" "coh:setup:SETUP-CREDIT" "b_star" "0.6176470588235294"
assert_field "SETUP-CREDIT: E = -0.074962" "$IFD" "coh:setup:SETUP-CREDIT" "E" "-0.07496200850130198"
assert_field "SETUP-CREDIT: E_net = -0.104837" "$IFD" "coh:setup:SETUP-CREDIT" "E_net" "-0.10483747550005665"
assert_field "SETUP-CREDIT verdict KILL (the disposition trap)" "$IFD" "coh:setup:SETUP-CREDIT" "verdict" "KILL (E_net<=0 with n>=30)"

assert_field "m = 35 cohorts tested" "$IFD" "mt" "m_cohorts_tested" "35"
assert_field "adjusted z bar = 3.188815" "$IFD" "mt" "z_bar" "3.1888152561902836"
assert_field "1 of 35 clears the adjusted bar" "$IFD" "mt" "cohorts_clearing_adjusted_bar" "1"
assert_field "2 of 35 clear a naive 1.96" "$IFD" "mt" "cohorts_clearing_naive_1p96" "2"

assert_engine_value "the kill list is printed" "$IS" "KILL LIST (10 cohort(s) with n>=30 and E_net<=0):"
assert_engine_value "the cost-is-binding banner fires" "$IS" "COST IS THE BINDING CONSTRAINT"
assert_engine_value "the multiple-testing note is printed" "$IS" "MULTIPLE TESTING"
assert_engine_value "the adjusted-bar clearer is listed with its n" "$IS" "READ n NEXT TO t"
assert_engine_value "the engine's refusals panel is printed" "$IS" "6. WHAT THE ENGINE CANNOT TELL YOU"

# ── Block L: Scope discipline / deferrals ──────────────────────────────────
echo ""
echo "--- Scope Discipline ---"
for defer in 'trade-performance-analyst' 'timeframe-performance-statistics' \
             'trade-sizing-recovery' 'portfolio-signal-manager' 'algorithmic-trader' \
             'options-position-lifecycle' 'equity-position-lifecycle' \
             'options-strategist' 'trading-decision-data-catalogue'; do
  if grep -q "$defer" "$SKILL_MD" 2>/dev/null; then
    pass "defers to: $defer"
  else
    fail "no deferral to: $defer"
  fi
done
if grep -qi 'does not redefine\|refuses to redefine\|does not define or compute' "$SKILL_MD"; then
  pass "the metric-definition handoff is stated as a refusal"
else
  fail "the metric-definition handoff is not stated"
fi
if grep -q 'close date' "$SKILL_MD"; then
  pass "the close-date bucketing convention is restated (consumed, not re-derived)"
else
  fail "the close-date bucketing convention is missing"
fi

# ── Block M: examples/run-output.txt is fresh ──────────────────────────────
echo ""
echo "--- run-output.txt Freshness ---"
if [[ -f "$EX_DIR/run-output.txt" ]]; then
  for token in "RUN 1 of 2" \
               "RUN 2 of 2" \
               "VERDICT: INSUFFICIENT SAMPLE (< n_req trades)" \
               "VERDICT: NEGATIVE EDGE" \
               "SYNTHETIC / ILLUSTRATIVE" \
               "KILL (E_net<=0 with n>=30)"; do
    if grep -qF -- "$token" "$EX_DIR/run-output.txt"; then
      pass "run-output.txt contains this run's output: $(echo "$token" | cut -c1-44)"
    else
      fail "run-output.txt is STALE — missing: $token"
    fi
  done
else
  fail "run-output.txt missing"
fi

# ── Block N: examples/README.md honesty ────────────────────────────────────
echo ""
echo "--- examples/README.md ---"
if [[ -f "$EX_DIR/README.md" ]]; then
  for token in "synthetic" "SYNTHETIC" "trade_id,open_date,close_date,pnl" "risk" "cost" "setup" \
               "KILL LIST" "n_req" "R_max"; do
    if grep -qi -- "$token" "$EX_DIR/README.md"; then
      pass "README covers: $token"
    else
      fail "README does not cover: $token"
    fi
  done
  if grep -qi 'synthetic' "$EX_DIR/README.md" && grep -qi 'never be quoted\|not a finding\|not a result' "$EX_DIR/README.md"; then
    pass "README states bluntly that the shipped ledgers are synthetic"
  else
    fail "README does not state the synthetic-data disclaimer"
  fi
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
