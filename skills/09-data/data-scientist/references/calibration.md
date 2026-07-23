# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can run `model.fit()` and report accuracy but can't explain when accuracy is a misleading metric — or name 3 alternatives | You can design an experiment end-to-end: power analysis with business-justified MDE, sequential testing with pre-registered analysis plan, and results reported as effect size + CI | A product manager describes a messy business question in 5 minutes and within 15 minutes you can specify the exact statistical test, sample size, decision rule, and the 3 ways the analysis could go wrong |
| You apply a t-test to every A/B test without checking whether the data meets the assumptions (normality, independence, equal variance) | You select the appropriate test based on data characteristics (Mann-Whitney for skewed metrics, delta method for ratio metrics, CUPED for variance reduction) and verify assumptions before running | You can look at a published academic study or industry white paper and identify the fatal statistical flaw (p-hacking, leakage, confounding, selection bias) within 10 minutes |
| You see a "statistically significant p=0.04" result and recommend shipping without looking at the sample size, effect size, or confidence interval | You refuse to report a p-value without the accompanying effect size, 95% CI, and a statement about practical significance in business terms | The CEO asks "Should we bet $10M on this recommendation?" and you give a calibrated probability — "65% chance the effect is real and ≥2%" — and 12 months later your forecast was correct |

**The Litmus Test:** Someone hands you a dataset and says "find insights." Can you produce a report that includes: (a) data quality issues that would invalidate any analysis, (b) the right statistical framework for each research question, (c) effect sizes with uncertainty, and (d) a clear "here's what we know, here's what we don't know" conclusion? If your report says "the data shows X" without caveats, you're not L3 yet.
