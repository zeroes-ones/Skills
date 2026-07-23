# Error Decoder

| 🖥️ Console Match (grep pattern) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `grep -rL "openapi\|\.proto\|asyncapi" contracts/ && cat dependency-matrix.* \| grep "api"` — API dependencies exist but no contract files found | Integration between Team A and Team B took 3 months instead of 3 weeks — request/response schemas didn't match at integration | Teams started implementing against verbal API contracts with no machine-readable spec. Each team built against their own interpretation. | Mandate contract-first: define OpenAPI/gRPC/AsyncAPI specs before any implementation. Version the contract. Both teams build against the spec. | `for dep in $(yq '.dependencies[] | select(.type=="api") | .name' dependency-matrix.yaml); do if [ ! -f "contracts/${dep}.yaml" ]; then echo "BLOCKED: missing contract for $dep — freeze implementation, create spec, circulate for 48h review, unlock when approved"; exit 1; fi; done; echo "All API contracts present — proceed with implementation"` |
| `grep -L "sunset.date\|cutover.criteria\|rollback" migration-plan.* program-charter.*` — migration plan missing quantitative exit criteria | Migration program ran 8 months over schedule because dual-run period was indefinite — "we'll switch when confident" with no threshold | Cutover criteria were qualitative ("when we're confident") — no quantitative thresholds for switching traffic. Team kept running both systems indefinitely. | Define specific cutover criteria: latency within 10% of old system, zero data integrity errors for 7 days, error rate <0.1%. Set a hard sunset date with executive sign-off. | `if ! grep -q "sunset.date" program-charter.md; then echo "BLOCKED: add sunset date (ISO date) to program charter — get sponsor sign-off via email within 48h"; fi; if ! grep -q "cutover.criteria" program-charter.md; then echo "BLOCKED: define cutover criteria (latency %, error rate, data integrity) — circulate to all team leads for review"; fi; if grep -q "sunset.date" program-charter.md && grep -q "cutover.criteria" program-charter.md; then echo "Migration plan is gate-ready — proceed to milestone planning"; fi` |
| `grep "owner.*TBD\|owner.*team.*that\|owner: *$" dependency-matrix.*` — dependency with missing or placeholder owner | Critical cross-team dependency had no owner — blocked the program for 3 weeks | Dependency was assigned to "the team that will build it" — no named individual, no committed date. A dependency without a named owner has >90% chance of slipping. | Every dependency must have: named individual owner, owning team, committed date, buffer %. Track in matrix with weekly review. Escalate unowned dependencies >48h to sponsor. | `python3 -c "
import yaml, datetime
with open('dependency-matrix.yaml') as f: deps = yaml.safe_load(f)
for d in deps['dependencies']:
    if not d.get('owner') or d['owner'] in ['TBD', '', 'the team that will build it']:
        print(f'ESCALATE: {d[\"name\"]} has no owner — notify {d[\"owning_team\"]} EM within 24h, sponsor within 48h if still unowned')
    elif not d.get('committed_date'):
        print(f'WARN: {d[\"name\"]} owned by {d[\"owner\"]} but no committed date — request within 24h')
print('All dependencies owned and dated' if all(d.get('owner') and d['owner'] not in ['TBD',''] for d in deps['dependencies']) else '')
"` |
| `grep -P "on track\|looking good\|no issues\|green across" status-report-*.md && grep -v "confidence\|P[0-9]\{2\}" status-report-*.md` — optimistic language without quantitative backing | Exec sponsor found out about a schedule slip at the monthly review — canceled the program | TPM gave optimistic updates ("nearly on track") instead of honest risk reporting. Schedule slipped silently while status reports stayed green. | Report confidence intervals, not gut-feel. "80% confidence: Q3 delivery." Escalate any critical path slip within 48 hours. Bad news ages like milk — report it fresh. | `python3 -c "
import re, datetime
with open('status-report-latest.md') as f: content = f.read()
if re.search(r'on track|looking good|no issues', content, re.I) and not re.search(r'confidence.*\d+%|P\d{2}|AT_RISK|BLOCKED', content):
    print('REJECT: status report uses optimistic language without quantitative confidence — regenerate with milestone %, dependency status, PERT range')
    print('Auto-fix: append "Confidence: P50=[date], P90=[date]. Dependencies: X/Y ON_TRACK, Z AT_RISK. Risk score: [N]/10 (trend: ↓/→/↑)"')
"` |
| `find docs/adr/ -name "*.md" | while read adr; do adr_num=$(basename "$adr" .md | cut -d- -f1); git log --oneline --all | grep -q "$adr_num" && echo "LATE: $adr — ADR accepted after implementation started"; done` — ADR file creation date after first related commit | Program built wrong architecture because no ADR was written for a foundational decision — 4 teams built against incompatible assumptions | Key architecture choice was made in a hallway conversation between two senior engineers. No written record — each team implemented their own interpretation. | Document every significant architecture decision as an ADR BEFORE implementation. Circulate for review. Require system-architect or CTO approval for cross-cutting decisions. | `for adr in docs/adr/*.md; do adr_date=$(git log --diff-filter=A --format=%ai -- "$adr" | tail -1); earliest_commit=$(git log --all --oneline --format=%ai | sort | head -1); if [ "$adr_date" \> "$earliest_commit" ]; then echo "RETROACTIVE ADR: $adr — supersede with true decision ADR that cites this as post-hoc documentation"; else echo "VALID: $adr — decision recorded before implementation"; fi; done` |
| `python3 -c "import datetime, os; m = os.path.getmtime('dependency-matrix.yaml'); days = (datetime.datetime.now() - datetime.datetime.fromtimestamp(m)).days; print(f'STALE: {days}d') if days > 7 else print('FRESH')"` — dependency matrix not updated in 7+ days | Program had a clear dependency map at kickoff but by month 3 it was obsolete — 4 new deps emerged, 2 silently descoped | Dependency tracking treated as one-time artifact, not living process. No weekly review cadence — changes accumulated invisibly. Dependencies decay at ~15%/week without active management. | Institute mandatory 30-min weekly dependency sync. Every dependency: ON_TRACK, AT_RISK (buffer <50%), BLOCKED. Status changes trigger immediate notification. Any dependency unconfirmed in 14 days is AT_RISK by default. | `#!/bin/bash
MATRIX="dependency-matrix.yaml"
DAYS=$(python3 -c "import datetime,os;print((datetime.datetime.now()-datetime.datetime.fromtimestamp(os.path.getmtime('$MATRIX'))).days)")
if [ "$DAYS" -gt 7 ]; then
  echo "ESCALATE: Dependency matrix is ${DAYS}d stale — schedule emergency 30-min dependency sync within 24h"
  for dep in $(yq '.dependencies[] | select(.status=="ON_TRACK") | .name' "$MATRIX"); do
    echo "AUTO-DEMOTE: $dep ON_TRACK→AT_RISK (unconfirmed >7 days)"
  done
  echo "After sync, update matrix and re-run: yq '.dependencies[].status' $MATRIX"
fi` |
| `grep -c "integration.test.*final\|integration.*last.milestone\|integrate.*at.*end" milestone-plan.* program-charter.*` — integration testing scheduled only at final milestone | Cross-team integration testing at final milestone — 12 critical bugs found, adding 6 weeks to timeline | "Integration at the end" is waterfall thinking in an agile program. Teams tested in isolation; contract conformance doesn't catch edge cases. | Schedule integration smoke tests at every milestone. After any team completes a contract-dependent feature, run integration test within 48h. Make "cross-team integration tests passing" an exit criterion for every milestone. | `for ms in $(yq '.milestones[].name' milestone-plan.yaml); do if ! grep -q "integration.test" "milestone-plan.yaml"; then echo "FIX: add integration test gate to milestone '$ms'"; fi; done
echo 'integration_test_gate:
  trigger: "any_contract_dependent_feature_complete"
  deadline: "48h after feature complete"
  check: "run_integration_smoke.sh --teams $(yq .dependent_teams[] contracts/feature.yaml)"
  exit_criteria: "all smoke tests pass, no P0/P1 bugs"'
echo "Add the above yaml block to every milestone in milestone-plan.yaml"` |
| `grep -E "[0-9]+ months|[A-Z][a-z]+ [0-9]{4}" status-report-*.md | grep -v "confidence\|P[0-9]\{2\}\|range"` — single-date commitment without confidence interval | Program sponsor demanded "single date" — TPM gave one, missed by 4 months, lost all credibility | TPM collapsed PERT (optimistic: 6mo, likely: 9mo, pessimistic: 14mo) into single "9 months" because "stakeholders don't like ranges." Delivered in 13 months — exactly the P90 scenario. | Never communicate a single date when uncertainty >30%. Use confidence intervals: "80% confidence: Q3-Q4." Explain what changes the range. If forced to give a single date, give the P90. | `python3 -c "
pert = {'optimistic': 6, 'most_likely': 9, 'pessimistic': 14}
expected = (pert['optimistic'] + 4*pert['most_likely'] + pert['pessimistic']) / 6
stddev = (pert['pessimistic'] - pert['optimistic']) / 6
p50 = expected; p90 = expected + 1.28*stddev
print(f'PERT: P50={p50:.1f}mo, P90={p90:.1f}mo, 80% confidence: {expected-0.84*stddev:.1f}-{expected+0.84*stddev:.1f}mo')
print('REPORT: \"80% confidence: delivery in {:.0f}-{:.0f} months. Range narrows as staffing, scope, and external dependencies resolve.\"'.format(expected-0.84*stddev, expected+0.84*stddev))
if pert['pessimistic'] - pert['optimistic'] > pert['most_likely'] * 0.3:
    print('WARN: Uncertainty >30% — single date is a lie. Use confidence intervals only.')
"` |
