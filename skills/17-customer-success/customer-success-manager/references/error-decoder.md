# Error Decoder

<!-- DEEP: 5min -- each entry includes a diagnostic grep pattern and step-by-step recovery loop for automation -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Health score says green but customer churns | Score overweights lagging indicators (NPS, payment) and underweights leading indicators (login decline, feature abandonment) | **Detect:** `grep "health_score" account.csv \| awk -F, "{if ($2 > 70 && $3 == "churned") print}"` returns matches

**Fix:** Add 60-day trend weights. Implement momentum scoring: score_trend = (current - score_60_days_ago) / score_60_days_ago.

**Auto-recovery:** 1. Detect churned accounts with health_score > 70. 2. Diagnose by comparing lagging vs leading indicator weights. 3. Auto-rebalance to >=60% leading indicators. 4. Validate weight distribution. | A health score that misses churn is worse than no score -- it creates false confidence. The detection pattern catches green-score churners and the auto-recovery loop rebalances toward leading indicators. |
| NPS response rate below 15% | Survey fatigue, wrong channel (email to people who live in Slack), survey too long | **Detect:** `grep "NPS" survey_response.csv \| awk -F, "{count++; if ($2 != "") responded++} END {print responded/count * 100}"` returns < 15

**Fix:** Switch to in-app micro-surveys (1 question). Email only for relationship NPS (quarterly). Offer incentive for relationship survey. Target: >30% response rate.

**Auto-recovery:** 1. Detect response_rate < 15%. 2. Auto-switch to in-app micro-survey template. 3. Inject incentive option. 4. Validate: retest after 1 cycle. If still <15%, escalate to UX researcher. | Low survey response is a channel and length problem, not a disinterest problem. The detection pattern catches low response rates and the auto-recovery loop adapts the survey approach. |
| Onboarding time is excellent but churn is still high | Onboarding measured by task completion, not value realization | **Detect:** `grep "onboarding_complete" account.csv \| awk -F, "{if ($2 == "yes" && $3 == "churned" && $4 < 90) print}"` returns matches

**Fix:** Redefine "onboarding complete" gate as: customer primary use case is live AND end users active AND customer confirms value.

**Auto-recovery:** 1. Detect accounts with onboarding_complete but churned < 90 days. 2. Check if value-realization gate was used vs task-completion gate. 3. Replace task-completion criteria with value-realization criteria. 4. Validate gates. | Task completion is not the same as value realization. The detection pattern catches quick-churn despite completed onboarding and the auto-recovery loop redefines the completion gate. |
| Save offers not working (<20% save rate) | Offer is generic (discount) not specific to churn reason. Customer churning because product does not solve their problem. | **Detect:** `grep "save_offer" intervention_log.csv \| awk -F, "{if ($3 < 20) count++} END {print count/NR * 100}"` returns > 80

**Fix:** Root-cause the churn reason first. If missing feature: free beta access + dedicated support. If too expensive: tier downgrade.

**Auto-recovery:** 1. Detect save_rate < 20%. 2. Diagnose: check if root cause preceded offer. 3. Auto-block: require churn_root_cause populated before any save offer. 4. Retest save_rate after 1 quarter. | A generic discount does not fix a product gap. The detection pattern catches low save rates and the auto-recovery loop enforces root-cause diagnosis before any save offer. |
| QBR attendance declining below 50% of invited | QBRs are one-way product pitches, not joint business reviews. Customers see them as a waste of time. | **Detect:** `grep "QBR" attendance_log.csv \| awk -F, "{if ($3 < $4 * 0.5) print}"` returns matches

**Fix:** Restructure: 80% customer business goals, 20% your product. Pre-read sent 48h before. Confirm attendee list includes decision-maker.

**Auto-recovery:** 1. Detect attendance_rate < 50%. 2. Audit QBR decks for KPI vs demo content ratio. 3. Auto-restructure deck with KPI-first format. 4. Validate: retest attendance_rate after 1 cycle. | A QBR that is a product demo is a waste of the customer time. The detection pattern catches declining attendance and the auto-recovery loop restructures the QBR around customer goals. |
| >20% of churn is unclassified | Churn categories not enforced. Mixing reasons hides actionable patterns. | **Detect:** `grep "unclassified\|N/A\|other" churn_log.csv \| wc -l` > `grep -c "." churn_log.csv` * 0.2

**Fix:** Classify every churned account >$10K as fixable or unavoidable. Track separately. Only fixable churn drives product and process improvements.

**Auto-recovery:** 1. Detect unclassified churn > 20%. 2. Auto-require mandatory churn_category field. 3. Backfill classification prompts. 4. Validate: unclassified count == 0. | Unclassified churn is invisible churn. The detection pattern catches high unclassified rates and the auto-recovery loop enforces mandatory categorization. |
| NRR >130% -- suspiciously high | New logo ARR likely included in NRR numerator. Inflates CS performance with sales results. | **Detect:** `grep "NRR" metric_report.md \| grep -oP "\d+\.?\d*" \| head -1` > 130

**Fix:** Recalculate: NRR = (starting ARR + expansion - contraction - churn) / starting ARR. Exclude new logo ARR.

**Auto-recovery:** 1. Detect reported NRR > 130%. 2. Audit for new logo ARR in calculation. 3. Auto-correct: remove new_logo_arr from numerator. 4. Recalculate and annotate as [CORRECTED: new logo ARR excluded]. | NRR inflated by new logo ARR measures sales, not customer success. The detection pattern catches suspiciously high NRR and the auto-recovery loop recalculates correctly. |
