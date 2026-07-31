# Error Decoder

<!-- DEEP: 5min -- each entry includes a diagnostic grep pattern and step-by-step recovery loop for automation -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Onboarding NPS < 30 -- new hires report unstructured experience, no buddy, no 30-day check-in, "I had to figure everything out myself" | No structure, no buddy assignment, no 30/60/90 day milestones. Onboarding treated as an administrative task, not a strategic program. | **Detect:** `grep -ri "onboarding.*NPS.*<.*30\|NPS.*below.*30\|onboarding NPS" --include="*.md"`

**Fix:** Implement buddy program. Ship laptop + accounts before day 1. Manager 30/60/90 day check-ins with written goals. Measure NPS at day 90. Structured onboarding is the highest-ROI people ops investment.

**Auto-recovery:** (a) Assign buddy before day 1, (b) Write 30/60/90 day milestones, (c) Schedule manager check-ins at weeks 1, 2, 4, 8, 12, (d) Send day-90 NPS survey. Target NPS > 50. | Onboarding is the highest-ROI people ops investment. The detection pattern catches negative NPS scores and the auto-recovery loop provides a complete onboarding rescue program. |
| Performance ratings inflated -- 40%+ rated "Exceeds Expectations." System measures manager comfort with difficult conversations, not performance. | No calibration sessions. No forced distribution targets. Managers avoid difficult feedback conversations -- they rate everyone high to avoid conflict. | **Detect:** `grep -ri "40.*%.*Exceeds\|ratings inflated\|leniency bias\|ratings.*too high\|grade inflation" --include="*.md"`

**Fix:** Implement calibration sessions. Set forced distribution targets (5-10% Exceptional). Train managers on giving honest, specific feedback. Review ratings by manager -- flag outlier managers who rate entire team as exceptional.

**Auto-recovery:** (a) Schedule calibration session within 2 weeks, (b) Set forced distribution targets, (c) Train all managers on honest feedback, (d) Identify managers who rated entire team exceptional -- they need coaching. | Rating inflation measures manager discomfort with difficult conversations, not performance. The detection pattern catches inflated distributions and the auto-recovery loop forces calibration rigor. |
| High-performers leaving for 15-20% raises elsewhere. Company caught off guard -- no warning signs detected. | Comp bands stale or below market. No equity refresh program. No stay interview program to detect flight risk. Retention is reactive -- counteroffers only after resignation. | **Detect:** `grep -ri "high.*performer.*left\|top talent.*quit\|key.*employee.*resign\|flight risk" --include="*.md" \| grep -v "stay interview\|retention risk\|engagement score\|pulse"`

**Fix:** Re-benchmark against Pave/Levels.fyi quarterly. Implement annual equity refreshers. Proactive retention conversations for top 20% with comp adjustments. Stay interviews catch flight risk before exit interviews can.

**Auto-recovery:** (a) Benchmark all comp bands against current market data, (b) Implement quarterly stay interviews for top 20% performers, (c) Flag engagement score drops >20 points, (d) Proactive comp adjustments before they interview elsewhere. | Retention is always cheaper than replacement. The detection pattern catches reactive retention and the auto-recovery loop builds a proactive stay interview program. |
| Engagement survey participation < 50%. Employees do not trust anonymity or do not believe action will be taken. | Past surveys collected data with no visible follow-up. Trust in anonymity compromised. Questions asked that leadership had no intention of acting on. | **Detect:** `grep -ri "survey.*participation.*<.*50\|low.*survey.*response\|nobody.*fills.*survey\|survey.*fatigue" --include="*.md"`

**Fix:** Use third-party survey tool with anonymity guarantee. Share results transparently within 2 weeks. Commit to specific action items and report progress. Remove questions you will not act on.

**Auto-recovery:** (a) Switch to third-party survey tool, (b) Share anonymized results within 2 weeks, (c) Publicly commit to 1-2 action items with owners and deadlines, (d) Report progress before next survey. | Survey participation recovers when employees see action from previous surveys. The detection pattern catches low participation and the auto-recovery loop rebuilds trust through transparency. |
| I-9 audit reveals missing or incorrect forms. No single owner for I-9 process. Forms completed by hiring managers without training. | No I-9 process owner. I-9s handled as an afterthought during onboarding. No regular self-audit. Paper forms lost or stored incorrectly. | **Detect:** `grep -ri "I-9.*audit.*missing\|I-9.*not.*complete\|E-Verify.*failed\|I-9.*error" --include="*.md"`

**Fix:** Assign I-9 ownership to People Ops. E-Verify within 3 business days of hire. Quarterly self-audit on random sample of 10% of I-9s. Use electronic I-9 system.

**Auto-recovery:** (a) Assign single I-9 owner, (b) Audit 100% of active employee I-9s, (c) Set up electronic I-9 system, (d) E-Verify within 3 business days, (e) Quarterly self-audit on 10% random sample. | I-9 compliance is cheap to maintain and expensive to restore. The detection pattern catches audit failure signals and the auto-recovery loop provides a complete compliance rescue. |
| Career ladder exists but no one uses it for promotions. Promotions based on manager advocacy, not documented criteria. | Ladder is aspirational, not operational. No measurable criteria per level. No promotion packet process. No cross-functional review. | **Detect:** `grep -ri "career ladder.*not.*used\|ladder.*ignored\|leveling.*not.*applied\|promotion.*inconsistent" --include="*.md"`

**Fix:** Add behavioral anchors to each level. Require promotion packets with evidence against level criteria. Review by cross-functional panel. Calibrate promotions the same way you calibrate performance ratings.

**Auto-recovery:** (a) Add measurable behavioral anchors per level, (b) Create promotion packet template, (c) Form cross-functional promotion review panel, (d) Schedule quarterly promotion calibration sessions. | A career ladder that no one uses is just a document. The detection pattern catches ladder-not-used language and the auto-recovery loop operationalizes it with measurable anchors and cross-functional review. |
| Top performer quits unexpectedly -- no warning signs. Exit interview reveals issues that were never surfaced. | No retention risk signal detection. No pulse surveys tracking engagement trajectory. No stay interview program. | **Detect:** `grep -ri "top performer.*quit.*unexpected\|blind.*sided.*resign\|shocked.*resign" --include="*.md"`

**Fix:** Implement pulse surveys with eNPS tracking. Flag any employee whose engagement score drops >20 points. Conduct stay interviews asking "what would make you leave?" before they decide.

**Auto-recovery:** (a) Launch pulse surveys (5 questions + eNPS) monthly, (b) Flag any employee with >20 point eNPS drop for stay interview within 48 hours, (c) Quarterly stay interviews for top 20%. | An unexpected resignation means your early warning system failed. The detection pattern catches blindsided language and the auto-recovery loop builds a retention early warning system. |
| Pay equity complaint or lawsuit -- compensation disparities by gender, race, or tenure discovered. | Compensation not audited for bias. No annual pay equity analysis. Bands used inconsistently across demographic groups. | **Detect:** `grep -ri "pay.*equity.*complaint\|pay.*discrimination\|comp.*bias\|salary.*gap.*gender\|salary.*gap.*race" --include="*.md"`

**Fix:** Run annual pay equity audit by gender, race, and tenure. Adjust salaries to correct disparities -- do not wait for a complaint. Publish compensation band ranges internally (transparency reduces bias).

**Auto-recovery:** (a) Run regression analysis across gender and race controlling for role, level, tenure, and location, (b) Adjust any statistically significant disparities, (c) Publish comp band ranges internally, (d) Automate pay equity audit annually. | Pay equity is cheaper to maintain than to restore after a complaint. The detection pattern catches equity complaint signals and the auto-recovery loop forces systematic audit. |
