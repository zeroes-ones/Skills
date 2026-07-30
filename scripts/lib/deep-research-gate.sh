#!/usr/bin/env bash
# ============================================================================
# G14: Deep Research Gate — Superior Decision Quality Enforcement
# ============================================================================
# This gate runs BEFORE any trading/finance skill change is committed.
# It enforces research depth, data provenance, regime awareness, and 
# anti-hallucination guardrails. This is NOT a lint check — it's a 
# THINKING QUALITY check. If you can't prove you researched it, you 
# can't commit it.
#
# Architecture: G14 runs after G0-G13. G0-G13 check structure.
# G14 checks DEPTH. A structurally valid skill that fails G14 is 
# a skill that hasn't been properly researched.
#
# Research quality dimensions checked:
#   RQ1: DATA PROVENANCE — Every number must have a source tag
#   RQ2: REGIME COVERAGE — Every strategy must address all market regimes
#   RQ3: PATTERN RECOGNITION — Pattern engine must be consulted
#   RQ4: CROSS-SKILL WIRING — Upstream/downstream references complete 
#   RQ5: FAILURE MODES — What breaks this strategy must be documented
#   RQ6: DOLLAR QUANTIFICATION — Risk/reward in dollars, not just %
#   RQ7: ANTI-HALLUCINATION — Limitations explicitly stated
#   RQ8: RESEARCH CITATIONS — Specific data sources, not general knowledge
#
# Usage:
#   scripts/lib/deep-research-gate.sh [--skill-dir PATH] [--all] [--changed] [--strict]
#
# Exit codes:
#   0 = PASS (research depth sufficient)
#   1 = BLOCK (critical research gaps — cannot commit)
#   2 = WARN (research adequate but improvable — warn but don't block)
# ============================================================================

set -euo pipefail

# --- Configuration ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
MODE="changed"  # --all, --changed, --skill-dir
TARGET_DIR=""
STRICT=false
ERRORS_ONLY=false
NO_COLOR=false

# --- Color Setup ---
if [[ -t 1 ]] && [[ "$NO_COLOR" != "true" ]]; then
  RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
  BOLD='\033[1m'; NC='\033[0m'; CYAN='\033[0;36m'
else
  RED=''; GREEN=''; YELLOW=''; BOLD=''; NC=''; CYAN=''
fi

PASS=0; BLOCK=0; WARN=0; TOTAL=0

# --- Research Quality Thresholds (data-derived, see get_thresholds()) ---
MIN_PROVENANCE_TAGS=2
MIN_REGIME_REFERENCES=1
MIN_DOLLAR_EXAMPLES=1
MIN_FAILURE_MODES=4
MIN_RESEARCH_CITATIONS=8
MIN_REFERENCE_FILES=9

# --- Helper Functions ---
pass_msg()  { echo -e "  ${GREEN}[PASS]${NC} $1"; PASS=$((PASS + 1)); }
block_msg() { echo -e "  ${RED}[BLOCK]${NC} $1"; BLOCK=$((BLOCK + 1)); }
warn_msg()  { echo -e "  ${YELLOW}[WARN]${NC} $1"; WARN=$((WARN + 1)); }
info_msg()  { echo -e "  ${CYAN}[INFO]${NC} $1"; }
total_msg() { TOTAL=$((TOTAL + 1)); }

# --- Check if a file is a skill ---
# ALL skills are subject to deep research quality checks.
# Different domains have different minimum thresholds.
is_skill() {
  local dir="$1"
  [[ -f "$dir/SKILL.md" ]] || return 1
  return 0
}

# --- Get skill domain for threshold calibration ---
get_skill_domain() {
  local dir="$1"
  if [[ "$dir" == *"/14-finance/"* ]] || grep -q 'type:.*finance\|tags:.*trading\|tags:.*options\|tags:.*quant' "$dir/SKILL.md" 2>/dev/null; then
    echo "finance"
  elif [[ "$dir" == *"/01-strategy/"* ]] || grep -q 'type:.*strategy\|tags:.*business\|tags:.*ceo\|tags:.*cto' "$dir/SKILL.md" 2>/dev/null; then
    echo "strategy"
  elif [[ "$dir" == *"/12-quality/"* ]] || [[ "$dir" == *"/15-devops/"* ]]; then
    echo "engineering"
  else
    echo "general"
  fi
}

# --- Get domain-adjusted thresholds ---
# Thresholds derived from 226-skill ecosystem scan (2026-08-01):
#   Finance: p75-derived (top 25% pass, rest must improve)
#   Strategy: p90-derived (strategic decisions carry outsized risk)
#   Engineering: p75-derived 
#   General: p50-derived (baseline research consciousness)
get_thresholds() {
  local domain="$1"
  case "$domain" in
    finance)
      # p75: provenance=9 regimes=3 failure=9 dollar=0 citations=8 refs=9
      # BLOCK below p75, WARN between p75-p90
      MIN_PROVENANCE_TAGS=9      # p75: only top 3 of 11 finance skills have >=9
      MIN_REGIME_REFERENCES=3    # p75: most cover 3/4 regimes (missing bull regime)
      MIN_DOLLAR_EXAMPLES=2      # stretch: only 1 skill has any today, set at aspirational
      MIN_FAILURE_MODES=9        # p75: every finance skill should think about failure
      MIN_RESEARCH_CITATIONS=8   # p75: data sources must be cited
      MIN_REFERENCE_FILES=9      # p75: depth of research
      ;;
    strategy)
      # p90: provenance=2 regimes=1 failure=3 dollar=0 citations=7 refs=15
      # Strategy skills have smaller distribution — use p90 to push quality up
      MIN_PROVENANCE_TAGS=3      # p90+1: push beyond current max of 2 (median=2)
      MIN_REGIME_REFERENCES=2    # p90: most have 0-1, 2 is aspirational
      MIN_DOLLAR_EXAMPLES=1      # stretch: zero strategy skills have dollar examples today
      MIN_FAILURE_MODES=3        # p75: strategy without failure modes is dangerous
      MIN_RESEARCH_CITATIONS=7   # p90: cite your sources
      MIN_REFERENCE_FILES=15     # p90: strategy requires deep references
      ;;
    engineering)
      # Engineering skills merged into general in scan — use general p75
      MIN_PROVENANCE_TAGS=3      # p75 of general=2, round up
      MIN_REGIME_REFERENCES=1    # most engineering has 1
      MIN_DOLLAR_EXAMPLES=1      # stretch
      MIN_FAILURE_MODES=4        # p75 of general
      MIN_RESEARCH_CITATIONS=8   # p75 of general
      MIN_REFERENCE_FILES=12     # p75 of general
      ;;
    general)
      # p50 (median) as floor — "beyond and precise" means even general skills need rigor
      MIN_PROVENANCE_TAGS=2      # median of 209 skills
      MIN_REGIME_REFERENCES=1    # median
      MIN_DOLLAR_EXAMPLES=1      # stretch — almost no general skills have dollar examples
      MIN_FAILURE_MODES=4        # p75: demand above median for failure thinking
      MIN_RESEARCH_CITATIONS=8   # p75: data source consciousness
      MIN_REFERENCE_FILES=9      # median
      ;;
  esac
}

# --- RQ1: Data Provenance ---
# Every numerical claim must be tagged with its source
check_provenance() {
  local skill_file="$1"
  local skill_name="$2"
  
  # Count provenance tags
  local verified; verified=$(grep -c '\[VERIFIED\]' "$skill_file" 2>/dev/null) || verified=0
  local computed; computed=$(grep -c '\[COMPUTED\]' "$skill_file" 2>/dev/null) || computed=0
  local estimated; estimated=$(grep -c '\[ESTIMATED' "$skill_file" 2>/dev/null) || estimated=0
  local broker; broker=$(grep -c '\[BROKER-VERIFIED\]' "$skill_file" 2>/dev/null) || broker=0
  local common; common=$(grep -c '\[COMMON-PRACTICE\]' "$skill_file" 2>/dev/null) || common=0
  local total_tags=$((verified + computed + estimated + broker + common))
  
  # Count untagged numbers using python
  local untagged; untagged=$(python3 -c "
import re, sys
with open('$skill_file') as f:
    content = f.read()
matches = re.findall(r'\d+(?:\.\d+)?\s*%', content)
print(len(matches))
" 2>/dev/null) || untagged=0
  local untagged_dollar; untagged_dollar=$(python3 -c "
import re, sys
with open('$skill_file') as f:
    content = f.read()
matches = re.findall(r'\\\$\d[\d,]*\s', content)
print(len(matches))
" 2>/dev/null) || untagged_dollar=0
  
  if [[ $total_tags -lt $MIN_PROVENANCE_TAGS ]]; then
    block_msg "RQ1: Only $total_tags provenance tags (min $MIN_PROVENANCE_TAGS required). [VERIFIED]=$verified [COMPUTED]=$computed [ESTIMATED]=$estimated [BROKER-VERIFIED]=$broker [COMMON-PRACTICE]=$common"
  else
    pass_msg "RQ1: $total_tags provenance tags ([VERIFIED]=$verified [COMPUTED]=$computed [ESTIMATED]=$estimated)"
  fi
  
  # Check for specific anti-hallucination markers
  if grep -q 'Anti-Hallucination\|Anti-Hallucination' "$skill_file" 2>/dev/null; then
    pass_msg "RQ1: Anti-Hallucination section present"
  else
    block_msg "RQ1: Missing Anti-Hallucination section — all trading skills MUST declare limitations"
  fi
  
  # Check for knowledge cutoff
  if grep -qi 'knowledge cutoff\|data.*as of\|verified.*as of\|accurate.*as of' "$skill_file" 2>/dev/null; then
    pass_msg "RQ1: Knowledge cutoff declared"
  else
    warn_msg "RQ1: No knowledge cutoff declared — data may be stale"
  fi
}

# --- RQ2: Regime Coverage ---
# Market regimes only apply to market-dependent domains: finance, strategy, growth, seo, data
# Non-market skills (dev, design, ops, people, legal) are NOT checked for regimes
is_market_domain() {
  local domain="$1"
  case "$domain" in
    finance|strategy|growth) return 0 ;;  # market regimes matter
    *) return 1 ;;  # non-market skills don't need regime coverage
  esac
}

check_regime_coverage() {
  local skill_file="$1"
  local skill_name="$2"
  local domain="$3"
  
  # Skip regime check for non-market domains — regime coverage doesn't apply
  if ! is_market_domain "$domain"; then
    pass_msg "RQ2: N/A — non-market domain (regime coverage not applicable)"
    return 0
  fi
  
  local bull; bull=$(python3 -c "
import re, sys
with open('$skill_file') as f:
    content = f.read()
matches = re.findall(r'bull[\s-]market|bull[\s-]regime|bull[\s-]environment|bull[\s-]trend|uptrend', content, re.I)
print(len(matches))
" 2>/dev/null) || bull=0
  local correction; correction=$(python3 -c "
import re, sys
with open('$skill_file') as f:
    content = f.read()
matches = re.findall(r'correction|pullback|decline[\s-].*[5-9]%|[-−][5-9][\s-]?%', content, re.I)
print(len(matches))
" 2>/dev/null) || correction=0
  local bear; bear=$(python3 -c "
import re, sys
with open('$skill_file') as f:
    content = f.read()
matches = re.findall(r'bear[\s-]market|bear[\s-]regime|downturn|drawdown|recession', content, re.I)
print(len(matches))
" 2>/dev/null) || bear=0
  local crash; crash=$(python3 -c "
import re, sys
with open('$skill_file') as f:
    content = f.read()
matches = re.findall(r'crash|[-−][2-3][5-9]%|[-−][4-9][0-9]%|black[\s-]swan|tail[\s-]event|march[\s-]2020|2008[\s-]financial|market[\s-]collapse', content, re.I)
print(len(matches))
" 2>/dev/null) || crash=0
  local total_regimes=$(( (bull > 0) + (correction > 0) + (bear > 0) + (crash > 0) ))
  
  if [[ $total_regimes -ge 4 ]]; then
    pass_msg "RQ2: All 4 regimes covered (bull=$bull, correction=$correction, bear=$bear, crash=$crash)"
  elif [[ $total_regimes -ge 3 ]]; then
    warn_msg "RQ2: $total_regimes/4 regimes covered — missing at least one regime scenario"
  else
    block_msg "RQ2: Only $total_regimes/4 regimes covered. Strategies untested in missing regimes are DANGEROUS. (bull=$bull, correction=$correction, bear=$bear, crash=$crash)"
  fi
}

# --- RQ3: Pattern Recognition Engine Consultation ---
check_pattern_engine() {
  local skill_file="$1"
  local skill_name="$2"
  
  # Check if pattern-recognition-engine.md is referenced
  if grep -q 'pattern-recognition-engine\|pattern.recognition.engine\|Pattern Recognition Engine' "$skill_file" 2>/dev/null; then
    pass_msg "RQ3: Pattern Recognition Engine referenced"
  elif [[ "$skill_name" == "options-strategist" ]] || [[ "$skill_name" == "options-risk-engineer" ]]; then
    block_msg "RQ3: Pattern Recognition Engine NOT referenced — this is mandatory for strategist/risk-engineer skills"
  else
    warn_msg "RQ3: Pattern Recognition Engine not referenced — consider consulting the meta-layer"
  fi
  
  # Check for evidence of data-driven threshold derivation
  local has_derived; has_derived=$(python3 -c "
import re, sys
with open('$skill_file') as f:
    content = f.read()
found = re.search(r'derived[\s-].*threshold|threshold[\s-].*from[\s-].*data|why[\s-].*\d+[\s-].*not[\s-].*\d+|mathematically|crossover[\s-].*point|data[\s-].*backed', content, re.I)
print(1 if found else 0)
" 2>/dev/null) || has_derived=0
  if [[ "$has_derived" == "1" ]]; then
    pass_msg "RQ3: Thresholds appear data-derived (not arbitrary)"
  else
    warn_msg "RQ3: No evidence of data-derived thresholds — are these numbers backed by data or opinion?"
  fi
}

# --- RQ4: Cross-Skill Wiring ---
check_cross_skill() {
  local skill_file="$1"
  local skill_name="$2"
  
  # Check for upstream references in chain
  if grep -q 'consumes_from\|Consumes From\|upstream' "$skill_file" 2>/dev/null; then
    pass_msg "RQ4: Upstream dependencies declared"
  else
    warn_msg "RQ4: No upstream dependencies — is this skill truly standalone?"
  fi
  
  if grep -q 'feeds_into\|Feeds Into\|downstream' "$skill_file" 2>/dev/null; then
    pass_msg "RQ4: Downstream consumers declared"
  else
    warn_msg "RQ4: No downstream consumers — what skills use this output?"
  fi
}

# --- RQ5: Failure Mode Documentation ---
check_failure_modes() {
  local skill_file="$1"
  local skill_name="$2"
  local domain="$3"
  
  local failure_count; failure_count=$(python3 -c "
import re, sys
with open('$skill_file') as f:
    content = f.read()
matches = re.findall(r'failure[\s-]mode|what[\s-].*go[\s-].*wrong|when[\s-].*fails|when[\s-].*break|loses[\s-].*money|worst[\s-]case|exit[\s-]condition|stop[\s-]loss|close[\s-]position|edge[\s-]case|known[\s-]limitation|what[\s-].*break', content, re.I)
print(len(matches))
" 2>/dev/null) || failure_count=0
  
  if [[ $failure_count -ge $MIN_FAILURE_MODES ]]; then
    pass_msg "RQ5: $failure_count failure modes documented (min $MIN_FAILURE_MODES)"
  else
    block_msg "RQ5: Only $failure_count failure modes documented (min $MIN_FAILURE_MODES). Every strategy has failure modes. Document them."
  fi
  
  # Check for stop-loss or exit condition (domain-aware)
  if is_market_domain "$domain"; then
    # Market domains: need explicit stop-loss / exit rules
    local has_exit; has_exit=$(python3 -c "
import re, sys
with open('$skill_file') as f:
    content = f.read()
found = re.search(r'stop[\s-]loss|exit[\s-].*condition|close[\s-].*position[\s-].*when|cut[\s-].*loss|exit[\s-].*plan|exit[\s-].*rule', content, re.I)
print(1 if found else 0)
" 2>/dev/null) || has_exit=0
    if [[ "$has_exit" == "1" ]]; then
      pass_msg "RQ5: Exit conditions / stop-loss documented"
    else
      block_msg "RQ5: No exit conditions or stop-loss rules — every strategy needs an exit"
    fi
  else
    # Non-market domains: need "Complete When" or "when to stop" criteria
    local has_completion; has_completion=$(python3 -c "
import re, sys
with open('$skill_file') as f:
    content = f.read()
found = re.search(r'Complete[\s-]when|completion[\s-]criteria|when[\s-]to[\s-]stop|escalate[\s-]when|stop[\s-]condition|done[\s-]when|success[\s-]criteria', content, re.I)
print(1 if found else 0)
" 2>/dev/null) || has_completion=0
    if [[ "$has_completion" == "1" ]]; then
      pass_msg "RQ5: Completion/exit criteria documented"
    else
      warn_msg "RQ5: Consider documenting when to stop, escalate, or consider the task complete"
    fi
  fi
}

# --- RQ6: Dollar Quantification ---
check_dollar_quantification() {
  local skill_file="$1"
  local skill_name="$2"
  
  local dollar_examples; dollar_examples=$(python3 -c "
import re, sys
with open('$skill_file') as f:
    content = f.read()
matches = re.findall(r'\\\$\d[\d,]*\s*(?:loss|profit|gain|saved|cost|risk|P&L|drawdown|premium|debit|credit|value|worth)', content, re.I)
print(len(matches))
" 2>/dev/null) || dollar_examples=0
  
  if [[ $dollar_examples -ge $MIN_DOLLAR_EXAMPLES ]]; then
    pass_msg "RQ6: $dollar_examples dollar-quantified examples (min $MIN_DOLLAR_EXAMPLES)"
  else
    warn_msg "RQ6: Only $dollar_examples dollar-quantified examples. Abstract percentages don't cut it — show the dollars."
  fi
}

# --- RQ7: Anti-Hallucination Guardrails ---
check_anti_hallucination() {
  local skill_file="$1"
  local skill_name="$2"
  
  # Check for estimation acknowledgment
  local has_uncertainty; has_uncertainty=$(python3 -c "
import re, sys
with open('$skill_file') as f:
    content = f.read()
found = re.search(r'estimated.*\xb1|approximate|not[\s-].*guarantee|past[\s-].*performance|not[\s-].*predict|admit[\s-].*uncertainty|knowledge[\s-].*cutoff|uncertainty', content, re.I)
print(1 if found else 0)
" 2>/dev/null) || has_uncertainty=0
  if [[ "$has_uncertainty" == "1" ]]; then
    pass_msg "RQ7: Uncertainty acknowledged"
  else
    block_msg "RQ7: No uncertainty acknowledgment — trading skills must admit what they don't know"
  fi
  
  # Check for data source citations
  local citations; citations=$(python3 -c "
import re, sys
with open('$skill_file') as f:
    content = f.read()
matches = re.findall(r'source.*\:|data[\s-].*from|verified[\s-].*against|CBOE|Yahoo[\s-]Finance|Bloomberg|published[\s-].*by|exchange[\s-].*rules', content, re.I)
print(len(matches))
" 2>/dev/null) || citations=0
  
  if [[ $citations -ge $MIN_RESEARCH_CITATIONS ]]; then
    pass_msg "RQ7: $citations data source citations (min $MIN_RESEARCH_CITATIONS)"
  else
    warn_msg "RQ7: Only $citations data source citations — where does the data come from?"
  fi
}

# --- RQ8: Research Depth — Reference Coverage ---
check_reference_depth() {
  local skill_dir="$1"
  local skill_name="$2"
  
  local ref_dir="$skill_dir/references"
  if [[ -d "$ref_dir" ]]; then
    local ref_count=$(ls "$ref_dir"/*.md 2>/dev/null | wc -l | tr -d ' ')
    if [[ $ref_count -ge $MIN_REFERENCE_FILES ]]; then
      pass_msg "RQ8: $ref_count reference files (research depth adequate)"
    elif [[ $ref_count -ge $((MIN_REFERENCE_FILES / 2)) ]]; then
      warn_msg "RQ8: $ref_count reference files — consider adding more research depth"
    else
      block_msg "RQ8: Only $ref_count reference files — insufficient research depth (min $MIN_REFERENCE_FILES)"
    fi
  else
    warn_msg "RQ8: No references/ directory — where is the supporting research?"
  fi
  
  # Check example coverage
  local examples_dir="$REPO_ROOT/examples"
  local skill_example_count=$(find "$examples_dir" -name "*.md" -path "*$(echo $skill_name | tr '-' '*')*" 2>/dev/null | wc -l | tr -d ' ')
  if [[ $skill_example_count -ge 2 ]]; then
    pass_msg "RQ8: $skill_example_count example files with backtest data"
  else
    warn_msg "RQ8: Only $skill_example_count examples — backtest validation sparse"
  fi
}

# --- Check single skill ---
check_skill() {
  local skill_dir="$1"
  local skill_file="$skill_dir/SKILL.md"
  local skill_name=$(basename "$skill_dir")
  local domain=$(get_skill_domain "$skill_dir")
  get_thresholds "$domain"
  
  echo ""
  echo -e "${BOLD}${CYAN}═══ Deep Research Gate: $skill_name [$domain] ═══${NC}"
  
  check_provenance "$skill_file" "$skill_name"
  check_regime_coverage "$skill_file" "$skill_name" "$domain"
  check_pattern_engine "$skill_file" "$skill_name"
  check_cross_skill "$skill_file" "$skill_name"
  check_failure_modes "$skill_file" "$skill_name" "$domain"
  check_dollar_quantification "$skill_file" "$skill_name"
  check_anti_hallucination "$skill_file" "$skill_name"
  check_reference_depth "$skill_dir" "$skill_name"
}

# --- Main ---
main() {
  echo -e "${BOLD}G14: DEEP RESEARCH GATE — Superior Decision Quality Enforcement${NC}"
  echo "Research quality requires: data provenance, regime coverage, pattern engine,"
  echo "failure modes, dollar quantification, anti-hallucination, and research depth."
  echo ""
  
  if [[ "$MODE" == "all" ]]; then
    # Check ALL skills across all domains
    local skills_dir="$REPO_ROOT/skills"
    echo -e "${CYAN}Scanning all skills for research quality...${NC}"
    local checked=0
    for skill_dir in "$skills_dir"/*/*/; do
      if is_skill "$skill_dir"; then
        check_skill "$skill_dir"
        checked=$((checked + 1))
      fi
    done
    echo ""
    echo -e "${CYAN}Checked $checked skill(s) across all domains${NC}"
  elif [[ "$MODE" == "changed" ]]; then
    # Check only skills with uncommitted changes
    local changed_files=$(git -C "$REPO_ROOT" diff --name-only HEAD 2>/dev/null | grep 'skills/.*/SKILL.md' || true)
    if [[ -z "$changed_files" ]]; then
      changed_files=$(git -C "$REPO_ROOT" diff --name-only --cached 2>/dev/null | grep 'skills/.*/SKILL.md' || true)
    fi
    
    if [[ -z "$changed_files" ]]; then
      echo -e "  ${GREEN}[PASS]${NC} No skill changes detected — skipping deep research gate"
      return 0
    fi
    
    # Extract unique skill directories
    local skill_dirs=$(echo "$changed_files" | sed 's|/SKILL.md||' | sort -u)
    for dir in $skill_dirs; do
      local full_path="$REPO_ROOT/$dir"
      if [[ -d "$full_path" ]] && is_skill "$full_path"; then
        check_skill "$full_path"
      fi
    done
  elif [[ -n "$TARGET_DIR" ]]; then
    if is_skill "$TARGET_DIR"; then
      check_skill "$TARGET_DIR"
    else
      echo -e "  ${YELLOW}[SKIP]${NC} $TARGET_DIR is not a skill — skipping deep research gate"
      return 0
    fi
  fi
  
  # --- Gate Decision ---
  echo ""
  echo -e "${BOLD}═══ G14 Gate Decision ═══${NC}"
  echo -e "  Checks passed: ${GREEN}$PASS${NC}  Warnings: ${YELLOW}$WARN${NC}  Blocks: ${RED}$BLOCK${NC}"
  
  if [[ $BLOCK -gt 0 ]]; then
    echo ""
    echo -e "${RED}${BOLD}⛔ G14 BLOCKED: $BLOCK critical research gap(s)${NC}"
    echo ""
    echo "  To resolve:"
    echo "  1. Add provenance tags [COMPUTED]/[VERIFIED]/[ESTIMATED] to all numerical claims"
    echo "  2. Address all 4 market regimes (bull, correction, bear, crash)"
    echo "  3. Reference the Pattern Recognition Engine for strategy decisions"
    echo "  4. Document failure modes — what breaks this strategy?"
    echo "  5. Add dollar-quantified examples with real P&L numbers"
    echo "  6. Declare limitations and knowledge cutoff"
    echo "  7. Add data source citations"
    echo ""
    echo "  Deep research is a PREREQUISITE, not an option."
    echo "  If you cannot PROVE you researched it, you cannot commit it."
    exit 1
  elif [[ $STRICT == "true" ]] && [[ $WARN -gt 0 ]]; then
    echo ""
    echo -e "${YELLOW}${BOLD}⚠️  G14 WARNING (strict mode): $WARN research quality warning(s)${NC}"
    echo "  Strict mode treats warnings as blocks. Address the warnings above."
    exit 1
  else
    echo ""
    echo -e "${GREEN}${BOLD}✅ G14 PASSED: Research depth sufficient${NC}"
    if [[ $WARN -gt 0 ]]; then
      echo -e "  ${YELLOW}$WARN warning(s)${NC} — address before production deployment"
    fi
    exit 0
  fi
}

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --all) MODE="all"; shift ;;
    --changed) MODE="changed"; shift ;;
    --skill-dir) MODE="skill-dir"; TARGET_DIR="$2"; shift 2 ;;
    --strict) STRICT=true; shift ;;
    --errors-only) ERRORS_ONLY=true; shift ;;
    --no-color) NO_COLOR=true; shift ;;
    -h|--help)
      echo "Usage: deep-research-gate.sh [OPTIONS]"
      echo "  --all          Check all finance skills"
      echo "  --changed      Check only skills with uncommitted changes (default)"
      echo "  --skill-dir DIR Check a specific skill directory"
      echo "  --strict       Treat warnings as blocks"
      echo "  --errors-only  Show only blocking errors"
      echo "  --no-color     Disable colored output"
      exit 0
      ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

main
