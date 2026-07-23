# Production Checklist

<!-- QUICK: 30s -- binary pass/fail with validation commands and auto-fix -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|----------------|--------------------|----------|
| IR1 | Data room built with all 14 folders populated and counsel-reviewed | `test -d data-room/ && test -f data-room/00-index.md && ls data-room/ | wc -l | awk '{exit $1<14}'` | Generate missing folder structure from 14-folder template. |
| IR2 | Pitch deck finalized: 12 slides, no slide >5 bullets | `test -f pitch-deck.pptx && python -c "from pptx import Presentation; p=Presentation('pitch-deck.pptx'); assert len(p.slides)==12"` | Trim to 12 slides. Flag slides with >5 bullets for reduction. |
| IR3 | Financial model with best/base/worst case scenarios, 24-month projections | `grep -l "best case\|base case\|worst case" *.xlsx && grep -c "202[6-9]" financial-model.csv` | Auto-generate scenario tabs and extend projections to 24 months. |
| IR4 | Target investor list: 30-50 firms, tiered, warm intro path mapped | `test -f investor-target-list.csv && wc -l < investor-target-list.csv | awk '{exit $1<30}'` | Generate investor-scoring template. Populate from Crunchbase/Pitchbook CSV export. |
| IR5 | Investor CRM set up with pipeline stages | `test -f pipeline-tracker.* && grep -q "stage\|status\|contacted\|responded\|meeting\|term sheet" pipeline-tracker.*` | Generate pipeline tracker template with standard stages. |
| IR6 | Reference customers identified (5-8), pre-briefed | `grep -c "reference\|9\/10\|NPS.*[89]" reference-customers.md | awk '{exit $1<5}'` | Generate reference survey script. Auto-score customers from NPS data. |
| IR7 | Term sheet comparison matrix completed for competing offers | `test -f term-sheet-comparison.md && grep -q "liquidation\|participation\|board\|anti-dilution" term-sheet-comparison.md` | Generate comparison matrix template with all 8 standard terms. |
| IR8 | Cap table modeled in 4 scenarios: base, down round, exit waterfall, acquisition | `test -d cap-table-scenarios/ && ls cap-table-scenarios/ | wc -l | awk '{exit $1<4}'` | Auto-generate 4 scenario tabs from current cap table. |
| IR9 | Cap table reconciled and counsel-audited within 30 days | `test -f cap-table-audit*.pdf && find cap-table-audit*.pdf -mtime -30 | grep -q .` | Alert: schedule counsel audit. Generate reconciliation workbook. |
| IR10 | First investor update sent or schedule set | `find . -name "investor-update*.md" -mtime -30 | grep -q .` | Auto-generate monthly update from CRM pipeline and financial milestones. |
| IR11 | Background check disclosures prepared upfront | `test -f background-disclosures.md && wc -l < background-disclosures.md | awk '{exit $1<5}'` | Generate disclosure checklist: litigation, regulatory, credential items. |
| IR12 | All material customer contracts (>$100K) collected and redacted | `find data-room/05-commercial/ -name "*.pdf" | wc -l | awk '{exit $1<1}'` | Generate contract collection checklist. Flag missing contracts. |
| IR13 | Competitive differentiation matrix with evidence | `test -f competitive-differentiation.md && grep -q "win.rate\|customer.quote\|benchmark\|evidence" competitive-differentiation.md` | Generate differentiation matrix template. Auto-extract win rates from CRM. |
| IR14 | Fundraising FAQ answering top 20 diligence questions | `test -f fundraising-faq.md && grep -c "^### " fundraising-faq.md | awk '{exit $1<20}'` | Auto-generate FAQ from data room content. Flag unanswered questions. |
| IR15 | No-shop diligence response SLA: 4h acknowledge, 24h fulfill | `grep "SLA\|acknowledge.*4.*hour\|fulfill.*24.*hour" diligence-process.md` | Generate SLA tracker template. Auto-log response times. |
