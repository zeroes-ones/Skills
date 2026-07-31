# Error Decoder

<!-- DEEP: 5min -- each entry includes a diagnostic grep pattern and step-by-step recovery loop for automation -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Fired employee for poor performance but had no written record of feedback, PIPs, or coaching. Employee sued for wrongful termination and won. | Documentation felt confrontational, so the manager avoided it. HR did not audit manager documentation. | **Detect:** `grep -ri "no documentation\|nothing in writing\|verbal only\|no paper trail" --include="*.md"`

**Fix:** Require written documentation for every performance conversation. Audit quarterly. If it is not in writing, the termination cannot happen. Train managers: documentation protects both the employee (they know where they stand) and the company (defensible process).

**Auto-recovery:** 1. grep for termination language. 2. If no PIP/written warning found -> HARD STOP. 3. Issue formal documentation gap warning with: (a) Document all performance issues in writing, (b) Issue formal PIP with measurable goals, (c) Wait PIP period, (d) Re-evaluate only after PIP concludes. | The detection pattern catches missing documentation before termination proceeds. The auto-recovery loop enforces a hard stop when termination lacks required paper trail. Documentation protects both the employee and the company. |
| HR tried to mediate a harassment complaint informally. Behavior escalated. Employee quit and sued. Company settled for seven figures. | Desire to avoid conflict and protect a senior leader overrode proper process. No investigation protocol existed. | **Detect:** `grep -ri "harassment\|inappropriate behavior\|sexual misconduct\|hostile.*environment" --include="*.md" \| grep -i "informal\|off the record\|just talk\|mediate\|handle quietly"`

**Fix:** Harassment complaints never get informal resolution. Every complaint triggers formal investigation: neutral investigator, interviews, evidence collection, findings, corrective action. No "off the record" harassment report -- ever.

**Auto-recovery:** 1. grep for harassment keywords. 2. If "informal" or "mediate" appears -> HARD STOP. 3. Assign neutral investigator, interview all parties, preserve communications, document findings, determine corrective action. No exceptions. | Harassment complaints are never resolved informally. The auto-recovery loop catches "off the record" language and forces formal process. One informal mediation can become a seven-figure settlement. |
| Every employee issue -- interpersonal conflict, work-style friction, minor grievances -- funneled through HR. Managers abdicated all people responsibility. | No manager training on conflict resolution. No expectation that managers handle Level 1 people issues. | **Detect:** `grep -ri "complaint department\|everything comes to HR\|HR bottleneck\|managers not handling" --include="*.md"`

**Fix:** Train every manager on basic conflict resolution and coaching. Create escalation protocol: Level 1 (interpersonal) -> manager handles. Level 2 (pattern/policy) -> manager + HR consult. Level 3 (legal/harassment) -> HR leads. Hold managers accountable -- it is in their performance review.

**Auto-recovery:** Define Level 1 (manager owns, HR not involved), Level 2 (manager + HR consult), Level 3 (HR leads). Add manager accountability to performance reviews. | Managers managing people is not optional. The detection pattern catches HR bottleneck language, and the fix enforces an escalation protocol that keeps Level 1 issues with the manager who owns them. |
| Chose the cheapest health plan -- high deductible, narrow network. Employees could not afford to use it. Top talent left for companies with better benefits. | Benefits selected on cost alone, not employee needs. No employee input. No benchmarking. | **Detect:** `grep -ri "cheapest.*benefits\|lowest.*premium\|save on benefits\|cut health insurance" --include="*.md" \| grep -v "employee survey\|benchmark\|utilization"`

**Fix:** Survey employees before renewal on what they value. Benchmark 3-5 peer companies. Offer at least HDHP+HSA and PPO options. Run utilization reports annually -- if 40%+ on same plan, consider dropping others.

**Auto-recovery:** (a) Survey employees on priorities, (b) Benchmark 3-5 peers, (c) Offer minimum 2 plan options, (d) Run annual utilization analysis. Cost alone drives attrition -- measure ROI of benefits spend vs. replacement cost. | The cheapest benefits plan is the most expensive in the long run. The detection pattern catches cost-only decisions and the auto-recovery loop forces employee input and benchmarking before benefits selection. |
| Company doubled in 6 months. Onboarding was a 30-minute laptop handout. No cultural orientation. Original values became inside jokes. 30% attrition within a year. | Growth prioritized over culture. No deliberate cultural onboarding. Values not reinforced at scale. | **Detect:** `grep -ri "doubled headcount\|hypergrowth\|scaling fast\|grew from.*to.*in.*months" --include="*.md" \| grep -v "onboarding\|culture\|values\|orientation\|people-ops"`

**Fix:** At 50: define values with observable behaviors. At 100: build values into hiring, onboarding (culture session with founder), performance reviews, recognition. At 200+: hire dedicated people-ops or culture role. Culture scales through deliberate systems.

**Auto-recovery:** (a) Define values with specific observable behaviors, (b) Culture session in every new hire first week, (c) Values rating in performance reviews, (d) Recognition program tied to values. Culture does not auto-scale. | Culture does not auto-scale. The detection pattern catches hypergrowth without cultural infrastructure, and the auto-recovery loop provides stage-specific interventions from 50 to 200+ employees. |
