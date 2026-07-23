# Core Workflow — Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Problem Framing & Hypothesis Generation

1. **Translate business question into statistical question**
   - Input: Stakeholder asks "Why is churn increasing?"
   - Output: "Is churn rate significantly higher in cohort Q2 vs Q1? What features predict churn?"
   - Frame as falsifiable hypothesis: H₀: churn_rate_Q2 = churn_rate_Q1 vs Hₐ: churn_rate_Q2 > churn_rate_Q1

2. **Define success metrics before touching data**
   - Primary metric: the one KPI the experiment/model must move
   - Guardrail metrics: metrics that must NOT degrade (e.g., revenue, latency, CSAT)
   - Diagnostic metrics: metrics to explain why (e.g., feature adoption, error rates)

3. **Map data requirements**
   - Identify all data sources, granularity, time range, completeness
   - Document known biases: selection bias, survivorship bias, measurement error
   - Determine if existing data can answer the question or if new data collection is needed

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): Exploratory Data Analysis (EDA)

4. **Univariate analysis** — One variable at a time
   - Continuous: distribution (histogram, boxplot), central tendency (mean/median), spread (std/IQR), skew, outliers
   - Categorical: frequency counts, proportions, cardinality
   - Input: raw dataset. Output: summary statistics table + distribution plots

5. **Bivariate analysis** — Relationships between pairs
   - Continuous-Continuous: scatter plot, Pearson/Spearman correlation, hexbin for dense data
   - Continuous-Categorical: grouped boxplots, violin plots, aggregated statistics by category
   - Categorical-Categorical: contingency table, mosaic plot, Cramér's V
   - Input: EDA dataset. Output: correlation matrix, cross-tabulations, initial hypotheses validated/rejected

6. **Missing data assessment** — NOT just "drop NA"
   - Is missingness MCAR, MAR, or MNAR? (Little's MCAR test)
   - Decision: MNAR → flag as feature; MAR → impute (KNN, MICE, iterative); MCAR → drop if <5%
   - Input: dataset with missing values. Output: missingness report + imputation strategy

7. **Data quality checks**
   - Impossible values (age = 300, negative revenue)
   - Timestamp consistency (events in the future, out of business hours)
   - Duplicate records, near-duplicates
   - Input: dataset. Output: data quality issues log with remediation actions

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): Statistical Testing & Experimentation

8. **Check test assumptions before running the test**
   - Normality: Shapiro-Wilk (n < 2000) or Kolmogorov-Smirnov (n > 2000), Q-Q plot visual inspection
   - Equal variance: Levene's test or Bartlett's test
   - Independence: Durbin-Watson for time series, design review for clustering
   - If assumptions violated: use non-parametric alternative or transform data

9. **Design the experiment with statistical power**
   - Effect size: what's the Minimum Detectable Effect (MDE) in business terms?
   - Power analysis: α = 0.05, β = 0.20 (power = 80%), compute required sample size N
   - Duration estimate: N / daily_traffic with buffer for seasonality, holidays, ramp-up
   - Use: `statsmodels.stats.power` or online calculators

10. **Run and monitor the experiment**
    - SRM check (Sample Ratio Mismatch): χ² test that observed assignment matches expected
    - Peeking correction: sequential testing (always valid p-values) or spend α across interim looks
    - CUPED (variance reduction): use pre-experiment covariates to reduce variance 10-30%

11. **Analyze results — go beyond the p-value**
    - Report: effect size + confidence interval + practical significance
    - Subgroup analysis: was the effect consistent across segments?
    - Multiple comparison correction: Bonferroni or Benjamini-Hochberg if testing many metrics
    - Input: experiment data. Output: decision (ship/iterate/kill) with evidence memo

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): Predictive Modeling

12. **Feature engineering** — more impactful than model choice
    - Transformations: log for skewed targets, Box-Cox for normality, one-hot/label/target encoding
    - Interactions: create cross-features from domain knowledge (e.g., price × promotion_flag)
    - Temporal: lag features, rolling windows (7d, 30d), day-of-week, holiday indicators
    - Input: cleaned dataset. Output: feature matrix + feature importance ranking

13. **Model selection and training**
    - Split: chronological for time series (NEVER random), stratified for imbalanced classification
    - Cross-validation: k-fold for IID, time-series split for temporal, group k-fold for clustered
    - Hyperparameter tuning: Bayesian optimization (Optuna) over grid search for >3 params
    - Baseline: always compare to a simple model (mean, linear regression, previous period)

14. **Model evaluation — context-dependent metrics**
    - Classification: accuracy (balanced only), precision/recall/F1 (imbalanced), ROC-AUC, PR-AUC
    - Regression: RMSE (sensitive to outliers), MAE (robust), MAPE (interpretable, biased at zero)
    - Time series: MAE, sMAPE, MASE (scale-independent); backtesting with expanding window

15. **Model interpretability** — mandatory for any model affecting humans
    - Global: feature importance (SHAP summary, permutation), partial dependence plots
    - Local: SHAP waterfall for individual predictions, LIME for text/image
    - Input: trained model + holdout set. Output: interpretability report

<!-- DEEP: 10+min -->
### Phase 5 (~25 min): Communication

16. **Craft the narrative — not the methodology**
    - Lead with the decision: "We should ship variant B — +3.2% conversion [95% CI: +1.8%, +4.6%]"
    - Show uncertainty: always include confidence intervals, not just point estimates
    - Visualization: bar charts for comparisons, line charts for trends, waterfall for decomposition
    - Anticipate objections: "But what about segment X?" — pre-compute subgroup results

17. **Write the decision memo**
    - Structure: TL;DR → Business context → Methodology (appendix) → Results → Decision → Risks
    - Input: all analysis outputs. Output: 1-2 page memo + appendix with technical details
