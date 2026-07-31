# Error Decoder

<!-- DEEP: 5min -- each entry includes a diagnostic grep pattern and step-by-step recovery loop for automation -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Offer acceptance rate < 60% -- candidates receiving offers but declining. Company is winning interviews but losing at the close. | Comp below market, process too slow, or weak closing strategy. Competitors offer more, move faster, or close better. | **Detect:** `grep -ri "offer.*acceptance.*<.*60\|acceptance rate.*below\|< 60%.*accept\|low.*close rate" --include="*.md"`

**Fix:** Benchmark comp against Pave/Levels.fyi for stage + geo. Compress loop to < 14 days. Pre-wire approval flex. HM calls within 2 hours of offer. Document closing strategy before every offer.

**Auto-recovery:** (a) Benchmark all offers against current market, (b) Compress timeline to < 14 days, (c) Pre-wire comp flex for +5-10%, (d) HM calls within 2 hours of offer, (e) Document closing strategy. Target: >80% acceptance. | A low acceptance rate means you are winning interviews but losing the close. The detection pattern catches close rate issues and the auto-recovery loop addresses comp, speed, and process gaps. |
| Candidates dropping out after onsite interviews -- invested significant time then disengaged. | Long decision time after onsite or ghosting. Candidate assumes rejection when they hear nothing. Competitor moves faster with an offer. | **Detect:** `grep -ri "dropping.*out.*after.*onsite\|candidate.*withdrew\|pulled out\|no longer.*interested" --include="*.md"`

**Fix:** Decide within 24 hours of debrief. If yes: HM calls immediately. If no: recruiter calls within 48 hours with feedback. Never leave candidates in limbo.

**Auto-recovery:** (a) Schedule debrief within 24 hours of final interview, (b) HM calls candidate same day if yes, (c) Recruiter delivers specific feedback within 48 hours if no. Every silence day increases drop-off risk by 3-5%. | Every day of silence after an onsite increases drop-off risk by 3-5%. The detection pattern catches candidate withdrawal and the auto-recovery loop enforces rapid decision-making. |
| Low-quality inbound applicants -- volume is there but candidates do not match the role. | JD lists requirements, not outcomes. Filters out strong candidates who would thrive but self-select out. Attracts keyword-matchers. | **Detect:** `grep -ri "low.*quality.*applicant\|bad.*candidates\|unqualified.*inbound\|weak.*pipeline" --include="*.md"`

**Fix:** Rewrite JD: 3 outcomes for first 6 months. Remove "years of experience" requirements. Add comp range. Add "Why this role exists now" section.

**Auto-recovery:** (a) Delete all "X+ years" and degree requirements, (b) Replace with 3 specific 6-month outcomes, (c) Add compensation range, (d) Add "Why this role exists now" section, (e) Republish and monitor quality metric for 30 days. | Job descriptions that list requirements attract keyword-matchers. The detection pattern catches low-quality applicant flow and the auto-recovery loop rewrites JDs to attract the right candidates. |
| Interviewers disagree on scores by >1.5 points -- panel produces conflicting signals. Hiring decision becomes subjective. | No calibration or vague rubric. Each interviewer evaluates differently because the rubric lacks behavioral anchors. | **Detect:** `grep -ri "interviewers.*disagree\|scores.*differ.*by.*[2-9]\|variance.*>.*1" --include="*.md"`

**Fix:** Run calibration session before first interview. Each score must have 3 behavioral anchors. Recalibrate monthly until variance < 0.5 points.

**Auto-recovery:** (a) Pause the loop -- do not interview more candidates, (b) Run calibration with all panelists on same mock candidate, (c) Hard-code 3 behavioral anchors per score level (1-4), (d) Score independently then discuss until variance < 0.5. | Uncalibrated interview panels produce subjective hiring decisions. The detection pattern catches score variance and the auto-recovery loop enforces calibration before proceeding. |
| New hire fails within 6 months -- passed interviews with strong scores but could not perform in the role. | Hired for skills, not for attributes that predict success in your environment. Scorecard missing adaptability, collaboration, decision-making assessment. | **Detect:** `grep -ri "new hire.*failed\|did not.*work.*out\|let.*go.*after.*months\|terminated.*probation\|< 6 months" --include="*.md"`

**Fix:** Audit scorecard for adaptability, collaboration style, and decision-making approach. Add values-based behavioral round. Reference checks with specific scenario questions.

**Auto-recovery:** (a) Audit last 3 failed hires for missing attributes, (b) Add those attributes to every scorecard, (c) Create scenario questions testing each attribute, (d) Add attribute-specific questions to reference checks. | Scorecards designed for screening fail at retention. The detection pattern catches early-stage failure and the auto-recovery loop redesigns the scorecard to test predictors of success in your environment. |
| Referral program produces few or no hires -- employees do not see value in referring. | Bonus too low, payout too slow, or no internal promotion of the program. Employees do not know what roles are open or what the bonus is. | **Detect:** `grep -ri "referral.*few\|referral.*low\|no referrals\|referral program.*dead\|nobody.*refers" --include="*.md"`

**Fix:** Raise bonus to $3K-10K based on role. Pay within 30 days of start. Feature referral stories in company meetings. Send quarterly "What we are hiring" digest to all employees.

**Auto-recovery:** (a) Raise bonus ($3K-5K IC, $5K-10K senior/leadership), (b) Pay within 30 days, (c) Share referral success stories in all-hands, (d) Send quarterly hiring digest. Target: >30% referral hires. | A referral program that nobody uses has a design problem, not an awareness problem. The detection pattern catches underperformance and the auto-recovery loop addresses bonus, payout speed, and visibility. |
| Pay equity complaint or lawsuit -- disparity in offers or compensation by demographic group discovered. | Compensation not audited for bias. Offers made without band anchoring. No offer review process for equity. | **Detect:** `grep -ri "pay.*equity.*complaint\|comp.*discrimination\|offer.*gap.*gender\|offer.*gap.*race\|salary.*disparity" --include="*.md"`

**Fix:** Run annual pay equity audit by gender, race, and tenure. Adjust salaries to correct disparities. Publish compensation band ranges internally. Review every offer for equity before it goes out.

**Auto-recovery:** (a) Review last 12 months of offers by gender and race, (b) Flag statistically significant disparities, (c) Adjust current offers to correct, (d) Implement offer equity review step before approval, (e) Annual pay equity audit automated. | Offer equity is a process problem, not an intent problem. The detection pattern catches pay disparity signals and the auto-recovery loop establishes a systematic offer equity review. |
