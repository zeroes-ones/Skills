# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Frame before you analyze** — Write down the hypothesis, null, alternative, and decision criteria before opening the dataset. Prevents p-hacking and confirmation bias.
- **Always report effect size + confidence interval** — A p-value alone is insufficient. "Statistically significant" with 0.01% lift on a $10 test is useless.
- **CUPED by default** — Pre-experiment covariates reduce variance 10-30%, cutting required sample size proportionally. The single highest-ROI experiment technique.
- **SRM check is non-negotiable** — Sample Ratio Mismatch invalidates an experiment. Automate this check; never skip it.
- **Peek, but peek correctly** — Continuous monitoring with unadjusted p-values inflates false positives 5-20x. Use sequential testing or alpha-spending.
- **One primary metric per experiment** — Multiple primary metrics require multiple comparison correction (Bonferroni). Use secondary and guardrail metrics instead.
- **Chronological splits for time series** — Random train/test split leaks future into past. Always split by time. Always backtest on expanding or rolling windows.
- **Interpretability is not optional** — If your model affects humans (loans, hiring, healthcare), you MUST explain predictions. Use SHAP for global + local explanations.
- **Simpson's paradox is lurking** — Always check if aggregated trends reverse within subgroups. Analyze both overall and segmented.
- **Communicate uncertainty visually** — Error bars, confidence bands, prediction intervals. Point estimates alone mislead decision-makers.
