## Error Decoder

| Error Message / Situation | Root Cause | Fix | Lesson |
|--------------------------|------------|-----|--------|
| "Test showed +10% lift but launched and saw 0%" | Novelty effect — users react to change, not improvement. | Run tests minimum 2 full weeks (capture weekday + weekend). Exclude first-time users from analysis. | Novelty effects decay in 7-14 days. Short tests overestimate true effect. |
| "p<0.05 but the CI includes zero" | Impossible — check your math. Likely using one-tailed test p-value with two-tailed CI. | Use consistent tails: two-tailed test + two-tailed CI, or one-tailed test + one-tailed bound. | Two-tailed is standard unless you have a strong directional prior. |
| "Retention improved but DAU flat" | Simpson's paradox: new cohorts retain better but are smaller. Old large cohorts churning masks the improvement. | Report cohort-level retention, not aggregate. Forecast: as old cohorts age out, DAU will rise. | Aggregate metrics lag cohort improvements by months. Lead with cohort data. |
| "Sample size calculator says 50K users, we only have 5K" | MDE too small or baseline too variable. | Increase MDE (test bigger changes). Use CUPED/stratification to reduce variance. Consider quasi-experiment (pre/post with control). | Small traffic = test big ideas. A 1% lift that needs 500K users is not testable at your scale. |
| "Funnel shows 50% drop at step 3 but no clue why" | Quantitative funnel tells you WHERE, not WHY. | Add qualitative: session recordings (Hotjar, FullStory), user interviews, exit surveys at funnel step. | Funnels + recordings + interviews = complete picture. Funnels alone = half the answer. |
| "Dashboard shows metrics but nobody looks at it" | Dashboard measures activity, not outcomes. | Redesign: every tile answers "should we do X?" Add annotations (launches, incidents). Weekly review ritual. | Dashboards without decisions are decoration. Kill or redesign them quarterly. |
