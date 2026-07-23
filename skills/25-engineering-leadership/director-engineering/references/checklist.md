# Production Checklist

<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[DE1]** | Org chart documented with team charters for every team — mission, scope, stakeholders, working agreements | `find . -name "*team-charter*" -o -name "*org-chart*" \| wc -l` → must be >= number of teams in org | Template: `templates/team-charter.md` — deploy one per team |
| **[DE2]** | EM:IC ratio between 1:5 and 1:8 for all teams | `scripts/check-em-ic-ratio.sh` → parses org-chart.yaml, flags teams outside 5-8 range | Alert: notify director when any team exceeds 1:8 or falls below 1:5 |
| **[DE3]** | Director:EM ratio between 1:4 and 1:6 | `scripts/check-director-span.sh` → parses org-chart.yaml, flags if span >6 | Alert: suggest hiring additional director or redistributing teams |
| **[DE4]** | Career ladder current and published for all engineering roles | `grep -rn "career ladder\|level guide\|competency" --include="*.md" \| wc -l` → must match >= 1 per role family | Template: `templates/career-ladder.md` |
| **[DE5]** | Annual budget and headcount plan approved by FP&A — 3 scenarios modeled | `grep -c "scenario\|tier\|KTLO\|stretch" budget*.md` → must be >= 3 | Template: `templates/budget-scenarios.md` |
| **[DE6]** | Team health metrics collected quarterly (engagement, psychological safety, eNPS) | `find . -name "*engagement*\|*team-health*\|*pulse*" -mtime -90` → must return files | Cron: `scripts/send-pulse-survey.sh` on quarterly schedule |
| **[DE7]** | Cross-team architecture forum meets bi-weekly or monthly — documented decisions | `grep -rn "architecture forum\|design review\|tech council" --include="*.md" -mtime -30` → must return recent meeting notes | Calendar: recurring invite with `templates/architecture-forum-agenda.md` |
| **[DE8]** | Succession plan documented for each EM role — ready-now name identified | `grep -c "succession\|ready.now\|backup" succession-plan*.md` → must be >= number of EMs | Template: `templates/succession-plan.md` — one row per EM |
| **[DE9]** | Quarterly strategy memo written and presented to exec team — business language, not velocity charts | `grep -rn "executive summary\|quarterly strategy\|Q[1-4].*memo" --include="*.md" -mtime -90` → must return file | Template: `templates/strategy-memo-business.md` |
| **[DE10]** | Stakeholder NPS measured (product, design, dependent teams) — quarterly trend | `grep -rn "stakeholder NPS\|partner satisfaction\|internal NPS" --include="*.md" -mtime -90` → must return data | Cron: `scripts/send-stakeholder-nps.sh` quarterly |
| **[DE11]** | Incident review action items tracked — completion > 90% within 30 days | `scripts/check-postmortem-actions.sh` → calculates (complete / total) × 100, fails if < 90 | Dashboard: `scripts/postmortem-dashboard.sh` — public Slack channel |
| **[DE12]** | Promotion rate audited by demographic — no significant differentials | `scripts/audit-promotion-rates.sh` → chi-squared test, flags p < 0.05 differentials | Quarterly run: `scripts/audit-promotion-rates.sh --report` |
| **[DE13]** | Vendor contract renewals calendar with 90-day review trigger | `grep -rn "renewal\|contract end\|expir" vendor-calendar*.md` → must list all active vendors with dates | Cron: `scripts/vendor-renewal-alert.sh` — 90-day warning to director |
| **[DE14]** | EM peer group meets bi-weekly with documented learnings | `find . -name "*EM-peer*\|*EM-community*\|*manager-roundtable*" -mtime -14` → must return notes | Calendar: recurring invite with `templates/em-peer-agenda.md` |
