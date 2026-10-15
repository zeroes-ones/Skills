#!/usr/bin/env bash
# ============================================================================
# verify-skill.sh — self-verification for equity-trading-playbook
# ============================================================================
# Structural, provenance, gate, arithmetic and determinism checks for this
# skill. Bash 3.2 compatible, no third-party dependencies, no network.
# Exits 0 when every check passes, 1 otherwise.
#
# The three checks that make this script more than a lint:
#   (a) it runs payoff_check.py on cards whose expected values are DOCUMENTED
#       IN examples/checks/*.md, and asserts the tool reproduces them -- so the
#       documented arithmetic and the shipped code cannot drift apart;
#   (b) it asserts the checker is DETERMINISTIC by running each card twice and
#       diffing both the text output and the --json output;
#   (c) it FAILS on an ORPHANED reference file -- a references/*.md that no
#       `(references/<file>.md)` link in SKILL.md resolves to.
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
LEDGER="$LOG_DIR/equity-book-synthetic.csv"

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
TMP="$(mktemp -d 2>/dev/null || mktemp -d -t payoffcheck)"
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
    fail "Section: $1 -- MISSING or not an exact level-2 heading"
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
    pass "card arithmetic: $label"
  else
    fail "card arithmetic MISSING from checker output: $label (looked for: $token)"
  fi
}

# assert_field <label> <fields-file> <field> <expected> [tolerance]
# Reads the flat "field<TAB>value" dump produced by dump_card from --json, so a
# value is asserted BY NAME rather than by its position in padded text output.
assert_field() {
  local label="$1" file="$2" field="$3" expect="$4" tol="${5:-0.0005}"
  local row
  row="$(awk -F'\t' -v f="$field" '$1==f {print $2; exit}' "$file")"
  if [[ "$row" == "$expect" ]]; then
    pass "card arithmetic: $label"
    return 0
  fi
  if [[ "$row" =~ ^-?[0-9] && "$expect" =~ ^-?[0-9] ]]; then
    if awk -v a="$row" -v b="$expect" -v t="$tol" 'BEGIN{d=a-b; if(d<0)d=-d; exit !(d<=t)}'; then
      pass "card arithmetic: $label"
      return 0
    fi
  fi
  fail "card arithmetic FAILED: $label (wanted $field = $expect, got '${row:-<absent>}')"
}

# assert_cohort <label> <ledger-file> <entity> <field> <expected> [tolerance]
# Reads the "entity<TAB>field<TAB>value" dump produced by dump_ledger below.
assert_cohort() {
  local label="$1" file="$2" entity="$3" field="$4" expect="$5" tol="${6:-0.0005}"
  local row
  row="$(awk -F'	' -v e="$entity" -v f="$field" '$1==e && $2==f {print $3; exit}' "$file")"
  if [[ "$row" == "$expect" ]]; then
    pass "ledger arithmetic: $label"
    return 0
  fi
  if [[ "$row" =~ ^-?[0-9] && "$expect" =~ ^-?[0-9] ]]; then
    if awk -v a="$row" -v b="$expect" -v t="$tol" 'BEGIN{d=a-b; if(d<0)d=-d; exit !(d<=t)}'; then
      pass "ledger arithmetic: $label"
      return 0
    fi
  fi
  fail "ledger arithmetic FAILED: $label (wanted $entity.$field = $expect, got '${row:-<absent>}')"
}

# dump_card <card-json-file> <out-file>  ->  "field<TAB>value" per line
dump_card() {
  $PY - "$1" > "$2" <<'PYEOF'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as fh:
    data = json.load(fh)

card = data.get("card") or {}
for k in sorted(card):
    v = card[k]
    if v is None:
        v = "n/a"
    elif isinstance(v, bool):
        v = "yes" if v else "no"
    elif isinstance(v, float):
        v = repr(round(v, 6))
    sys.stdout.write("%s\t%s\n" % (k, v))
PYEOF
}

# run_card <name> <args...>  -> writes $TMP/<name>.txt and $TMP/<name>.fields.tsv
run_card() {
  local name="$1"; shift
  if ! $PY "$ENGINE" "$@" > "$TMP/$name.txt" 2>&1; then
    fail "checker exited non-zero on card '$name': $*"
    return 1
  fi
  $PY "$ENGINE" "$@" --json > "$TMP/$name.json" 2>&1 || true
  dump_card "$TMP/$name.json" "$TMP/$name.fields.tsv"
  return 0
}

echo "=== Verifying $SKILL_NAME ==="
echo "  interpreter: $PY"
echo ""

# ── Block A: File existence ───────────────────────────────────────────────
echo "--- File Existence ---"
if [[ -f "$SKILL_MD" ]]; then pass "SKILL.md exists"; else fail "SKILL.md not found"; exit 1; fi
if [[ -d "$REF_DIR" ]]; then pass "references/ directory exists"; else fail "references/ directory MISSING"; fi
if [[ -d "$EX_DIR" ]]; then pass "examples/ directory exists"; else fail "examples/ directory MISSING"; fi
if [[ -d "$CHECK_DIR" ]]; then pass "examples/checks/ directory exists"; else fail "examples/checks/ directory MISSING"; fi
if [[ -d "$LOG_DIR" ]]; then pass "examples/logs/ directory exists"; else fail "examples/logs/ directory MISSING"; fi
if [[ -f "$ENGINE" ]]; then pass "checker exists: scripts/payoff_check.py"; else fail "checker MISSING: scripts/payoff_check.py"; fi
if [[ -f "$LEDGER" ]]; then pass "synthetic ledger exists"; else fail "synthetic ledger MISSING"; fi
if [[ -f "$EX_DIR/README.md" ]]; then pass "examples/README.md exists"; else fail "examples/README.md MISSING"; fi
if [[ -f "$EX_DIR/strategy-cards.md" ]]; then pass "examples/strategy-cards.md exists"; else fail "examples/strategy-cards.md MISSING"; fi
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
if grep -q 'consumes_from: \[equity-position-lifecycle, equity-risk-and-capital-engineer, edge-and-payoff-engineering\]' "$SKILL_MD" 2>/dev/null; then
  pass "chain.consumes_from is the required exact block"
else
  fail "chain.consumes_from is not the required exact block"
fi
if grep -q 'feeds_into: \[equity-position-lifecycle\]' "$SKILL_MD" 2>/dev/null; then
  pass "chain.feeds_into is the required exact block"
else
  fail "chain.feeds_into is not the required exact block"
fi
if grep -q 'skills/14-finance/equity-trading-playbook/examples/checks' "$SKILL_MD" 2>/dev/null; then
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
  fail "description length ${DESC_LEN} chars -- must be 1..1024"
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
PROV_LINES=$(grep -cE '\[VERIFIED|\[COMPUTED|\[ESTIMATED|\[ILLUSTRATIVE|\[COMMON-PRACTICE|\[BROKER-VERIFIED' "$SKILL_MD" || true)
check_ge "Lines carrying a provenance tag" "${PROV_LINES:-0}" 9

CITE=$(count_matches 'source.*:|data from|verified against|CBOE|Cboe|Yahoo Finance|Bloomberg|published by|exchange rules' "$SKILL_MD" -i)
check_ge "Research citations (source lines and named sources)" "${CITE:-0}" 8

if grep -q 'ILLUSTRATIVE' "$SKILL_MD" && grep -q 'SYNTHETIC' "$SKILL_MD"; then
  pass "synthetic fixtures are labelled SYNTHETIC / ILLUSTRATIVE in the doc"
else
  fail "synthetic fixtures are not labelled in SKILL.md"
fi
if grep -qi 'not a backtest\|never be quoted as one\|carries no market information\|carries no market information whatsoever' "$SKILL_MD"; then
  pass "the 'not a result / not market data' disclaimer is present"
else
  fail "the synthetic-data disclaimer is missing"
fi
if grep -qi 'could not be verified\|unverified\|cannot verify' "$SKILL_MD"; then
  pass "unverified claims are labelled as unverified"
else
  fail "no explicit unverified-claim disclosure found"
fi
if grep -qi 'does not promise a profit\|not a prediction, a guarantee or advice\|never claim or imply that a strategy is profitable' "$SKILL_MD"; then
  pass "no-profit / not-advice honesty clause present"
else
  fail "the no-profit honesty clause is missing"
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

if grep -qi 'exit condition\|exit plan\|stop-loss\|stop loss' "$SKILL_MD"; then
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

# ── ORPHAN CHECK: every references/*.md must be linked from SKILL.md ────────
ORPHANS=0
for f in "$REF_DIR"/*.md; do
  [[ -f "$f" ]] || continue
  base="$(basename "$f")"
  if ! grep -qF "(references/$base)" "$SKILL_MD" 2>/dev/null; then
    fail "ORPHANED reference file: references/$base is not linked from SKILL.md"
    ORPHANS=$((ORPHANS + 1))
  fi
done
if [[ "$ORPHANS" -eq 0 ]]; then
  pass "no orphaned reference files ($REF_COUNT on disk, all linked)"
fi

# ── Block I: The checker runs, and is deterministic ────────────────────────
echo ""
echo "--- Checker: runs and is deterministic ---"
if $PY "$ENGINE" --version >"$TMP/version.txt" 2>&1; then
  pass "checker --version runs: $(cat "$TMP/version.txt")"
else
  fail "checker --version failed"
fi

CARDS=(
  "c1|--tp|3.0|--sl|1.0|--p|0.40"
  "c2|--tp|1.0|--sl|1.0|--p|0.45"
  "c3|--tp|0.5|--sl|1.5|--p|0.62|--cost-r|0.02"
  "c4|--tp|2.0|--sl|1.0|--p|0.45|--cost-bps|5|--stop-pct|0.10"
  "c5|--tp|0.75|--sl|1.0|--p|0.65"
)

for spec in "${CARDS[@]}"; do
  IFS='|' read -r -a argv <<< "$spec"
  name="${argv[0]}"
  args=("${argv[@]:1}")
  if $PY "$ENGINE" "${args[@]}" >"$TMP/$name.1.txt" 2>&1; then
    pass "checker runs on card '$name'"
  else
    fail "checker FAILED on card '$name'"
    continue
  fi
  $PY "$ENGINE" "${args[@]}" >"$TMP/$name.2.txt" 2>&1
  if diff -q "$TMP/$name.1.txt" "$TMP/$name.2.txt" >/dev/null 2>&1; then
    pass "card '$name' text output is byte-identical across two runs"
  else
    fail "card '$name' text output is NOT deterministic"
  fi
  $PY "$ENGINE" "${args[@]}" --json >"$TMP/$name.1.json" 2>&1
  $PY "$ENGINE" "${args[@]}" --json >"$TMP/$name.2.json" 2>&1
  if diff -q "$TMP/$name.1.json" "$TMP/$name.2.json" >/dev/null 2>&1; then
    pass "card '$name' JSON output is byte-identical across two runs"
  else
    fail "card '$name' JSON output is NOT deterministic"
  fi
done

# The ledger run must be deterministic too, including its cohort table.
if $PY "$ENGINE" --from-log "$LEDGER" >"$TMP/log.1.txt" 2>&1; then
  pass "checker runs on the synthetic ledger via --from-log"
else
  fail "checker FAILED on the synthetic ledger"
fi
$PY "$ENGINE" --from-log "$LEDGER" >"$TMP/log.2.txt" 2>&1
if diff -q "$TMP/log.1.txt" "$TMP/log.2.txt" >/dev/null 2>&1; then
  pass "ledger output is byte-identical across two runs"
else
  fail "ledger output is NOT deterministic"
fi
$PY "$ENGINE" --from-log "$LEDGER" --json >"$TMP/log.1.json" 2>&1
$PY "$ENGINE" --from-log "$LEDGER" --json >"$TMP/log.2.json" 2>&1
if diff -q "$TMP/log.1.json" "$TMP/log.2.json" >/dev/null 2>&1; then
  pass "ledger JSON output is byte-identical across two runs"
else
  fail "ledger JSON output is NOT deterministic"
fi

# ── Block J: The card arithmetic ───────────────────────────────────────────
# Every value asserted below is written in examples/checks/*.md as the expected
# value, computed BY HAND in that file. If the checker and the documented hand
# arithmetic ever diverge, this block fails.
echo ""
echo "--- Card Arithmetic (checker vs the hand arithmetic in examples/checks/) ---"

# Card 1: b=3, p=0.40 -> E=+0.600000R, p*=0.250000, b*=1.500000,
# sd=1.959592, n_req=42.667, L=10.809, R_max=1.2336%, POSITIVE.
if run_card c1 --tp 3.0 --sl 1.0 --p 0.40; then
  assert_field "c1 b = 3.000000"                    "$TMP/c1.fields.tsv" "b"           "3.0"
  assert_field "c1 E = +0.600000R"                  "$TMP/c1.fields.tsv" "E"           "0.6"
  assert_field "c1 E_net = +0.600000R"              "$TMP/c1.fields.tsv" "E_net"       "0.6"
  assert_field "c1 b* = 1.500000"                   "$TMP/c1.fields.tsv" "b_star"      "1.5"
  assert_field "c1 p* = 0.250000"                   "$TMP/c1.fields.tsv" "p_star"      "0.25"
  assert_field "c1 Kelly f* = +0.200000"            "$TMP/c1.fields.tsv" "kelly"       "0.2"
  assert_field "c1 sd = 1.959592"                   "$TMP/c1.fields.tsv" "sd"          "1.959592"
  assert_field "c1 n_req = 42.667"                  "$TMP/c1.fields.tsv" "n_req"       "42.666667" 0.001
  assert_field "c1 L = 10.809"                      "$TMP/c1.fields.tsv" "L"           "10.808896" 0.001
  assert_field "c1 R_max = 1.2336%"                 "$TMP/c1.fields.tsv" "R_max_pct"   "1.233552" 0.0001
  assert_field "c1 c_R* = E = 0.600000"             "$TMP/c1.fields.tsv" "cost_breakeven_R" "0.6"
  assert_engine_value "c1 verdict POSITIVE"         "$TMP/c1.txt" "VERDICT: POSITIVE"
  assert_engine_value "c1 sd formula printed"       "$TMP/c1.txt" "0.400000*5.760000 + 0.600000*2.560000 = 3.840000"
  assert_engine_value "c1 n_req formula printed"    "$TMP/c1.txt" "4*(1.959592/0.600000)^2 = 42.667 trades"
  assert_engine_value "c1 L formula printed"        "$TMP/c1.txt" "ln(250.0)/ln(1.666667) = 5.521461/0.510826 = 10.809"
  assert_engine_value "c1 R_max formula printed"    "$TMP/c1.txt" "20.0000%/(10.809*1.50) = 1.2336%"
fi

# Card 2: b=1, p=0.45 -> E=-0.100000R, p*=0.500000, b*=1.222222,
# sd=0.994987, n_req=n/a (E<0), L=9.236, R_max=1.4437%, NEGATIVE.
if run_card c2 --tp 1.0 --sl 1.0 --p 0.45; then
  assert_field "c2 b = 1.000000"                    "$TMP/c2.fields.tsv" "b"           "1.0"
  assert_field "c2 E = -0.100000R"                  "$TMP/c2.fields.tsv" "E"           "-0.1"
  assert_field "c2 b* = 1.222222"                   "$TMP/c2.fields.tsv" "b_star"      "1.222222"
  assert_field "c2 p* = 0.500000"                   "$TMP/c2.fields.tsv" "p_star"      "0.5"
  assert_field "c2 sd = 0.994987"                   "$TMP/c2.fields.tsv" "sd"          "0.994987"
  assert_field "c2 n_req = n/a (E < 0)"             "$TMP/c2.fields.tsv" "n_req"       "n/a"
  assert_field "c2 L = 9.236"                       "$TMP/c2.fields.tsv" "L"           "9.235730" 0.001
  assert_field "c2 R_max = 1.4437%"                 "$TMP/c2.fields.tsv" "R_max_pct"   "1.443669" 0.0001
  assert_engine_value "c2 verdict NEGATIVE"         "$TMP/c2.txt" "VERDICT: NEGATIVE"
  assert_engine_value "c2 n_req refusal reason"     "$TMP/c2.txt" "E_net = -0.100000R is not positive"
  assert_engine_value "c2 Kelly negative reason"    "$TMP/c2.txt" "NEGATIVE: no fraction of the bankroll"
fi

# Card 3 (THE DISPOSITION TRAP): b=1/3, p=0.62 -> p*=0.750000, E=-0.173333R,
# E_net=-0.193333R, sd=0.647182, n_req=n/a, L=5.706, R_max=2.3365%, NEGATIVE.
if run_card c3 --tp 0.5 --sl 1.5 --p 0.62 --cost-r 0.02; then
  assert_field "c3 b = 0.333333"                    "$TMP/c3.fields.tsv" "b"           "0.333333" 0.000001
  assert_field "c3 p* = 0.750000 (the trap)"        "$TMP/c3.fields.tsv" "p_star"      "0.75"
  assert_field "c3 E = -0.173333R"                  "$TMP/c3.fields.tsv" "E"           "-0.173333" 0.000001
  assert_field "c3 E_net = -0.193333R"              "$TMP/c3.fields.tsv" "E_net"       "-0.193333" 0.000001
  assert_field "c3 b* = 0.612903"                   "$TMP/c3.fields.tsv" "b_star"      "0.612903" 0.000001
  assert_field "c3 Kelly f* = -0.520000"            "$TMP/c3.fields.tsv" "kelly"       "-0.52"
  assert_field "c3 sd = 0.647182"                   "$TMP/c3.fields.tsv" "sd"          "0.647182"
  assert_field "c3 n_req = n/a (E < 0)"             "$TMP/c3.fields.tsv" "n_req"       "n/a"
  assert_field "c3 L = 5.706"                       "$TMP/c3.fields.tsv" "L"           "5.706437" 0.001
  assert_field "c3 R_max = 2.3365%"                 "$TMP/c3.fields.tsv" "R_max_pct"   "2.336525" 0.0001
  assert_engine_value "c3 verdict NEGATIVE"         "$TMP/c3.txt" "VERDICT: NEGATIVE"
  assert_engine_value "c3 the 0.75 break-even is printed" "$TMP/c3.txt" "1/(1+0.333333) = 0.750000"
  assert_engine_value "c3 p+5pp is still NEGATIVE"  "$TMP/c3.txt" "p + 5pp"
  assert_field "c3 sensitivity p+5pp still negative" "$TMP/c3.fields.tsv" "cost_r" "0.02"
fi

# Card 4 (COST-SENSITIVE TIGHT STOP): b=2, p=0.45, 5 bps at a 0.10% stop.
# c_R = 5/(100*0.10) = 0.500000R, E = +0.350000R -> E_net = -0.150000R.
# The SAME card at a 5.0% stop gives c_R = 0.010000R and E_net = +0.340000R.
if run_card c4 --tp 2.0 --sl 1.0 --p 0.45 --cost-bps 5 --stop-pct 0.10; then
  assert_field "c4 b = 2.000000"                    "$TMP/c4.fields.tsv" "b"           "2.0"
  assert_field "c4 E = +0.350000R"                  "$TMP/c4.fields.tsv" "E"           "0.35"
  assert_field "c4 c_R = 0.500000R (derived)"       "$TMP/c4.fields.tsv" "cost_r"      "0.5"
  assert_field "c4 E_net = -0.150000R"              "$TMP/c4.fields.tsv" "E_net"       "-0.15"
  assert_field "c4 sd = 1.492481"                   "$TMP/c4.fields.tsv" "sd"          "1.492481"
  assert_field "c4 L = 9.236"                       "$TMP/c4.fields.tsv" "L"           "9.235730" 0.001
  assert_field "c4 R_max = 1.4437%"                 "$TMP/c4.fields.tsv" "R_max_pct"   "1.443669" 0.0001
  assert_engine_value "c4 verdict NEGATIVE by cost" "$TMP/c4.txt" "VERDICT: NEGATIVE"
  assert_engine_value "c4 cost-alone reason"        "$TMP/c4.txt" "cost alone consumes the edge"
  assert_engine_value "c4 c_R derivation printed"   "$TMP/c4.txt" "c_R = bps/(100*stop_pct) = 5.0000/(100*0.1000) = 0.500000"
  assert_engine_value "c4 break-even stop S*"       "$TMP/c4.txt" "S* = bps/(100*E) = 5.0000/(100*0.350000) = 0.1429%"
fi
if run_card c4wide --tp 2.0 --sl 1.0 --p 0.45 --cost-bps 5 --stop-pct 5.0; then
  assert_field "c4wide c_R = 0.010000R"             "$TMP/c4wide.fields.tsv" "cost_r"    "0.01"
  assert_field "c4wide E_net = +0.340000R"          "$TMP/c4wide.fields.tsv" "E_net"     "0.34" 0.000001
  assert_field "c4wide n_req = 77.076"              "$TMP/c4wide.fields.tsv" "n_req"     "77.076125" 0.001
  assert_engine_value "c4wide verdict POSITIVE"     "$TMP/c4wide.txt" "VERDICT: POSITIVE"
fi

# Card 5 (MARGINAL): b=0.75, p=0.65 -> E=+0.137500R, p*=0.571429,
# sd=0.834697, n_req=147.405, L=5.259, R_max=2.5351%, MARGINAL.
if run_card c5 --tp 0.75 --sl 1.0 --p 0.65; then
  assert_field "c5 b = 0.750000"                    "$TMP/c5.fields.tsv" "b"           "0.75"
  assert_field "c5 E = +0.137500R"                  "$TMP/c5.fields.tsv" "E"           "0.1375"
  assert_field "c5 p* = 0.571429"                   "$TMP/c5.fields.tsv" "p_star"      "0.571429" 0.000001
  assert_field "c5 b* = 0.538462"                   "$TMP/c5.fields.tsv" "b_star"      "0.538462" 0.000001
  assert_field "c5 sd = 0.834697"                   "$TMP/c5.fields.tsv" "sd"          "0.834697"
  assert_field "c5 n_req = 147.405"                 "$TMP/c5.fields.tsv" "n_req"       "147.404960" 0.001
  assert_field "c5 L = 5.259"                       "$TMP/c5.fields.tsv" "L"           "5.259425" 0.001
  assert_field "c5 R_max = 2.5351%"                 "$TMP/c5.fields.tsv" "R_max_pct"   "2.535125" 0.0001
  assert_field "c5 c_R* = E = 0.137500"             "$TMP/c5.fields.tsv" "cost_breakeven_R" "0.1375"
  assert_engine_value "c5 verdict MARGINAL"         "$TMP/c5.txt" "VERDICT: MARGINAL"
fi

# ── Block K: Guard paths must not crash ────────────────────────────────────
echo ""
echo "--- Guard Paths (degenerate input must be reported, not raised) ---"
guard_case() {
  local label="$1"; shift
  if $PY "$ENGINE" "$@" >"$TMP/guard.txt" 2>&1; then
    pass "guard: $label exits 0"
  else
    fail "guard: $label exited non-zero (must report, not crash)"
  fi
}
guard_case "sl = 0"                --tp 3.0 --sl 0 --p 0.40 --quiet
guard_case "tp = 0"                --tp 0 --sl 1.0 --p 0.40 --quiet
guard_case "p = 0"                 --tp 3.0 --sl 1.0 --p 0 --quiet
guard_case "p = 1"                 --tp 3.0 --sl 1.0 --p 1.0 --quiet
guard_case "cost >= E"             --tp 3.0 --sl 1.0 --p 0.40 --cost-r 0.8 --quiet
guard_case "n = 1"                 --tp 3.0 --sl 1.0 --p 0.40 --n 1 --quiet
guard_case "p out of range (1.5)"  --tp 3.0 --sl 1.0 --p 1.5 --quiet
guard_case "p out of range (-0.2)" --tp 3.0 --sl 1.0 --p -0.2 --quiet

$PY "$ENGINE" --tp 3.0 --sl 0 --p 0.40 --quiet >"$TMP/g1.txt" 2>&1 || true
assert_engine_value "sl = 0 is refused with a reason" "$TMP/g1.txt" "sl = 0.000000 R. A stop of 0R is not a stop"
assert_engine_value "sl = 0 verdict is UNDEFINED"     "$TMP/g1.txt" "VERDICT: UNDEFINED"

$PY "$ENGINE" --tp 3.0 --sl 1.0 --p 1.5 --quiet >"$TMP/g2.txt" 2>&1 || true
assert_engine_value "p > 1 is refused with a reason"  "$TMP/g2.txt" "is outside [0,1]"

$PY "$ENGINE" --tp 3.0 --sl 1.0 --p 0.40 --n 1 --quiet >"$TMP/g3.txt" 2>&1 || true
assert_engine_value "n = 1 reports no streak to size" "$TMP/g3.txt" "there is no streak to size for"

$PY "$ENGINE" --tp 3.0 --sl 1.0 --p 1.0 --quiet >"$TMP/g4.txt" 2>&1 || true
assert_engine_value "p = 1 reports L = 0 with its reason" "$TMP/g4.txt" "L = 0 because p = 1"

# Exit code 2 for a missing required flag and for a missing file.
if $PY "$ENGINE" --tp 3.0 >/dev/null 2>&1; then
  fail "guard: a card without --p should exit 2"
else
  rc=$?
  if [[ "$rc" -eq 2 ]]; then pass "guard: a card without --p exits 2"; else fail "guard: missing --p exited $rc, expected 2"; fi
fi
if $PY "$ENGINE" --from-log "$TMP/does-not-exist.csv" >/dev/null 2>&1; then
  fail "guard: a missing --from-log file should exit 2"
else
  rc=$?
  if [[ "$rc" -eq 2 ]]; then pass "guard: a missing ledger exits 2"; else fail "guard: missing ledger exited $rc, expected 2"; fi
fi

# ── Block L: The synthetic ledger's documented cohort arithmetic ───────────
echo ""
echo "--- Synthetic Ledger (documented cohort arithmetic) ---"
LF="$TMP/ledger.tsv"
$PY - "$TMP/log.1.json" > "$LF" <<'PYEOF'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as fh:
    data = json.load(fh)

log = data["log"]
sys.stdout.write("BOOK\trows\t%s\n" % log["rows"])
for k, v in log["book"].items():
    sys.stdout.write("BOOK\t%s\t%s\n" % (k, v))
for c in log["cohorts"]:
    name = c["setup"]
    for k, v in c.items():
        if k == "setup":
            continue
        sys.stdout.write("%s\t%s\t%s\n" % (name, k, v))
PYEOF

assert_cohort 'ledger rows = 62'                    "$LF" "BOOK" "rows"        "62"
assert_cohort 'ledger pooled mean R = +0.076613'    "$LF" "BOOK" "E_R_sample"  "0.076613" 0.000001
assert_cohort 'ledger pooled c_R = 0.010000'        "$LF" "BOOK" "c_R"         "0.01"
assert_cohort 'ledger pooled E_net = +0.066613'     "$LF" "BOOK" "E_net_R"     "0.066613" 0.000001
assert_cohort 'trend-breakout n = 15'               "$LF" "trend-breakout" "n"         "15"
assert_cohort 'trend-breakout p = 0.400000'         "$LF" "trend-breakout" "p"         "0.4"
assert_cohort 'trend-breakout b_R = 3.000000'       "$LF" "trend-breakout" "b_R"       "3.0"
assert_cohort 'trend-breakout E_net = +0.590000R'   "$LF" "trend-breakout" "E_net_R"   "0.59" 0.000001
assert_cohort 'range-meanrev p = 0.650000'          "$LF" "range-meanrev"  "p"         "0.65"
assert_cohort 'range-meanrev b_R = 0.750000'        "$LF" "range-meanrev"  "b_R"       "0.75"
assert_cohort 'range-meanrev E_net = +0.127500R'    "$LF" "range-meanrev"  "E_net_R"   "0.1275" 0.000001
assert_cohort 'disposition p = 0.625000'            "$LF" "disposition-quick-tp" "p"         "0.625"
assert_cohort 'disposition b_R = 0.333333'          "$LF" "disposition-quick-tp" "b_R"       "0.333333" 0.000001
assert_cohort 'disposition E_net = -0.260000R'      "$LF" "disposition-quick-tp" "E_net_R"   "-0.26" 0.000001
assert_cohort 'sizing-slip b_R = 1.000000'          "$LF" "sizing-slip"    "b_R"       "1.0"
assert_cohort 'sizing-slip b_currency = 10.000000'  "$LF" "sizing-slip"    "b_cur"     "10.0"
assert_cohort 'sizing-slip E_R_ratio = -0.333333'   "$LF" "sizing-slip"    "E_R_ratio" "-0.333333" 0.000001
assert_cohort 'sizing-slip E_currency_ratio = +2.666667' "$LF" "sizing-slip" "E_cur"    "2.666667" 0.000001
assert_engine_value "sizing-slip contamination flagged"  "$TMP/log.1.txt" "CONTAMINATED"
assert_engine_value "sizing-slip currency/R gap reported" "$TMP/log.1.txt" "currency b = 10.0000 against R b = 1.0000"
assert_engine_value "the synthetic label is echoed"       "$TMP/log.1.txt" "SYNTHETIC / ILLUSTRATIVE"

# ── Block L2: --setup and --csv-out (CLI parity with the options playbook) ──
echo ""
echo "--- CLI Parity: --setup and --csv-out ---"
if $PY "$ENGINE" --from-log "$LEDGER" --setup sizing-slip >"$TMP/setup.txt" 2>&1; then
  pass "--setup <tag> runs"
  assert_engine_value "--setup prints the R BASIS filter line"  "$TMP/setup.txt" "R BASIS: --setup sizing-slip -- only this cohort is included"
  assert_engine_value "--setup narrows the row count to 3"      "$TMP/setup.txt" "rows read : 3"
  assert_engine_value "--setup flags that the pooled row is not the book" "$TMP/setup.txt" "only this cohort is included"
else
  fail "--setup <tag> FAILED"
fi
if $PY "$ENGINE" --from-log "$LEDGER" --setup not-a-tag >/dev/null 2>&1; then
  fail "guard: an unknown --setup tag should exit 2"
else
  rc=$?
  if [[ "$rc" -eq 2 ]]; then pass "guard: an unknown --setup tag exits 2"; else fail "guard: unknown --setup exited $rc, expected 2"; fi
fi
if $PY "$ENGINE" --tp 2.0 --p 0.40 --setup x >/dev/null 2>&1; then
  fail "guard: --setup without --from-log should exit 2"
else
  rc=$?
  if [[ "$rc" -eq 2 ]]; then pass "guard: --setup without --from-log exits 2"; else fail "guard: --setup without --from-log exited $rc, expected 2"; fi
fi
if $PY "$ENGINE" --from-log "$LEDGER" --csv-out "$TMP/cohorts.csv" >"$TMP/csvout.txt" 2>&1; then
  if [[ -f "$TMP/cohorts.csv" ]]; then
    CROWS=$(grep -c ',' "$TMP/cohorts.csv" || true)
    if [[ "$CROWS" -eq 5 ]]; then
      pass "--csv-out writes a header plus 4 cohort rows"
    else
      fail "--csv-out wrote $CROWS comma-bearing lines, expected 5 (header + 4 cohorts)"
    fi
    if head -1 "$TMP/cohorts.csv" | grep -q '^setup,n,wins,losses,breakeven,p,r_mode,b_R'; then
      pass "--csv-out header starts with the documented column order"
    else
      fail "--csv-out header is not the documented column order"
    fi
    if grep -q '^sizing-slip,3,1,2,0,0.333333,yes,1.000000' "$TMP/cohorts.csv"; then
      pass "--csv-out carries the sizing-slip cohort row"
    else
      fail "--csv-out is missing the sizing-slip cohort row"
    fi
  else
    fail "--csv-out did not create the file"
  fi
  $PY "$ENGINE" --from-log "$LEDGER" --csv-out "$TMP/cohorts2.csv" >/dev/null 2>&1
  if diff -q "$TMP/cohorts.csv" "$TMP/cohorts2.csv" >/dev/null 2>&1; then
    pass "--csv-out is byte-identical across two runs"
  else
    fail "--csv-out is NOT deterministic"
  fi
else
  fail "--csv-out FAILED"
fi

# ── Block M: The ledger is labelled SYNTHETIC and carries its provenance ────
echo ""
echo "--- Synthetic Ledger Labelling ---"
if grep -q 'SYNTHETIC' "$LEDGER"; then pass "ledger header carries SYNTHETIC"; else fail "ledger header does NOT carry SYNTHETIC"; fi
if grep -q 'NOT market data' "$LEDGER"; then pass "ledger header says it is not market data"; else fail "ledger header missing the not-market-data disclaimer"; fi
if grep -q '^# PROVENANCE:' "$LEDGER"; then pass "ledger carries # PROVENANCE: lines"; else fail "ledger has no # PROVENANCE: lines"; fi
LEDGER_ROWS=$(grep -c '^T[0-9]' "$LEDGER" || true)
check_ge "ledger trade rows" "${LEDGER_ROWS:-0}" 40
for col in setup risk cost symbol; do
  if head -200 "$LEDGER" | grep -m1 '^trade_id,' | grep -q "$col"; then
    pass "ledger schema has a '$col' column"
  else
    fail "ledger schema is missing the '$col' column"
  fi
done

# The sibling ledger read must work too: same schema, no alteration.
SIB="$SKILL_DIR/../edge-and-payoff-engineering/examples/logs/hand-check-synthetic.csv"
if [[ -f "$SIB" ]]; then
  if $PY "$ENGINE" --from-log "$SIB" >"$TMP/sib.txt" 2>&1; then
    pass "checker reads the sibling edge-and-payoff-engineering fixture unchanged"
    assert_engine_value "sibling fixture: 10 rows read"          "$TMP/sib.txt" "rows read : 10"
    assert_engine_value "sibling fixture: p = 0.600000"          "$TMP/sib.txt" "0.600000"
    assert_engine_value "sibling fixture: zero-cost warning fires" "$TMP/sib.txt" "WARNING"
  else
    fail "checker FAILED on the sibling edge-and-payoff-engineering fixture"
  fi
else
  echo "  [SKIP] sibling fixture not present at $SIB"
fi

# ── Block N: The shipped check documents match the checker's real output ───
echo ""
echo "--- examples/checks/ Documents Match Real Output ---"
check_doc() {
  local file="$1" needle="$2"
  if grep -qF -- "$needle" "$CHECK_DIR/$file" 2>/dev/null; then
    pass "doc $(basename "$file") contains: $needle"
  else
    fail "doc $(basename "$file") is MISSING: $needle"
  fi
}
for f in 01-trend-breakout-positive.md 02-one-to-one-negative.md 03-disposition-trap-high-win-rate.md \
         04-cost-sensitive-tight-stop.md 05-marginal-mean-reversion.md 06-atr-sizing-and-ledger.md; do
  if [[ -f "$CHECK_DIR/$f" ]]; then pass "check document exists: $f"; else fail "check document MISSING: $f"; fi
done
check_doc "01-trend-breakout-positive.md"  "  trades to a 2-sigma mean : 42.667"
check_doc "02-one-to-one-negative.md"      "VERDICT: NEGATIVE"
check_doc "03-disposition-trap-high-win-rate.md" "  break-even win rate p*: 0.750000"
check_doc "04-cost-sensitive-tight-stop.md" "  net expectancy E_net  : -0.150000R"
check_doc "04-cost-sensitive-tight-stop.md" "  net expectancy E_net  : +0.340000R"
check_doc "05-marginal-mean-reversion.md"  "VERDICT: MARGINAL"
check_doc '06-atr-sizing-and-ledger.md'    '  share count             = floor($1,233.55/$10.00) = 123 shares'
check_doc '06-atr-sizing-and-ledger.md'    'sizing-slip: CONTAMINATED'

# ── Gate Decision ──────────────────────────────────────────────────────────
echo ""
echo "=== $SKILL_NAME verification: ${CHECKS} checks, ${FAILURES} failed ==="
if [[ "$FAILURES" -gt 0 ]]; then
  echo "FAIL"
  exit 1
fi
echo "PASS"
exit 0
