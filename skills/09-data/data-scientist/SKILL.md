---
name: data-scientist
description: Scientific method applied to data — hypothesis testing, A/B testing, causal inference, predictive modeling, EDA, time series analysis, statistical modeling, and experiment design. Triggered by data science, statistical analysis, hypothesis testing, experimentation, A/B test, causal inference, predictive modeling, EDA, statistical modeling, time series.
author: Sandeep Kumar Penchala
type: data
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - data-scientist
token_budget: 4500
output:
  type: "code"
  path_hint: "./"
---
# Data Scientist

Apply the scientific method to data problems — frame questions as testable hypotheses, design rigorous
experiments, perform exploratory data analysis, build and validate statistical models, and communicate
results to drive business decisions. This skill covers the full data science lifecycle: problem framing,
EDA methodology, statistical testing (t-test, chi-square, ANOVA, non-parametric), A/B testing design
(sample size, power analysis, MDE, SRM, peeking corrections), causal inference (DID, RDD, IV, propensity
scores), regression analysis, time series forecasting, survival analysis, feature engineering, model
interpretability (SHAP, LIME, partial dependence), Bayesian approaches, and ethical data science.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Hypothesis testing → Jump to "Sub-Skills > statistical-testing"
├── Design an A/B test → Go to "Sub-Skills > experiment-design"
├── Causal inference → Jump to "Sub-Skills > causal-inference"
├── Build a predictive model → Go to "Sub-Skills > predictive-modeling"
├── Exploratory data analysis → Jump to "Sub-Skills > eda-methodology"
├── Time series forecasting → Go to "Sub-Skills > time-series-forecasting"
├── Interpret a model → Jump to "Sub-Skills > model-interpretability"
├── Need data to analyze first → Invoke data-engineer skill instead
└── Don't know where to start? → Start at "Best Practices" — frame before you analyze
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never report results without p-values, confidence intervals, and sample sizes.** A naked "the treatment lifted conversion by 2.3%" without statistical context is misleading. Always include the CI and the sample size.
- **Correlation is not causation — say it explicitly.** When working with observational data, every finding must include a disclaimer about confounding variables. "X correlates with Y (r=0.74, p<0.001), but we cannot establish causation from this data alone."
- **Model performance on training data means nothing.** Report holdout/test set performance. Better yet, report performance on a time-based split that simulates production. A 99% AUC on training data is a red flag, not a victory.
- **Always check for data leakage before celebrating results.** The most common cause of "too good to be true" model performance is target leakage through feature engineering. Check every feature's relationship to the target temporally and logically.
- **Admit what you don't know.** If the data can't answer the question, say so. If a p-value of 0.051 vs 0.049 changes your conclusion, your conclusion isn't robust.

## When to Use

- You need to choose the right statistical test (t-test, chi-square, ANOVA, non-parametric) for a hypothesis
- You are designing an A/B test — sample size calculation, minimum detectable effect, peeking corrections
- You need to run exploratory data analysis (EDA) on a new dataset to surface patterns and anomalies
- You are building a predictive model (regression, classification, time series) for a business forecast
- You need to apply causal inference (difference-in-differences, RDD, instrumental variables) to observational data
- You are interpreting a black-box model using SHAP values, LIME explanations, or partial dependence plots
- You need to analyze time-to-event data with survival analysis or customer churn models
- You are setting up an experiment design with proper randomization, control groups, and statistical power

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Choosing the Right Statistical Test

```
Outcome variable type?
├── Continuous (numeric)
│   ├── 2 groups, independent        → Independent t-test (Welch's if unequal variance)
│   ├── 2 groups, paired              → Paired t-test
│   ├── 3+ groups, independent        → One-way ANOVA → Tukey HSD post-hoc
│   ├── 3+ groups, repeated measures  → Repeated measures ANOVA → Bonferroni post-hoc
│   └── Non-normal / ordinal          → Mann-Whitney U (2 groups) or Kruskal-Wallis (3+)
│
├── Categorical (yes/no, A/B/C)
│   ├── 2 categories, 1 sample        → Binomial test or one-proportion z-test
│   ├── 2 categories, 2+ samples      → Chi-square test of independence
│   ├── Small expected counts (<5)    → Fisher's exact test
│   └── Ordinal categories            → Cochran-Armitage trend test
│
├── Time-to-event (survival)
│   ├── Compare 2+ groups             → Log-rank test
│   └── Cox model with covariates     → Cox proportional hazards
│
└── Relationship between 2+ variables
    ├── Linear relationship           → Pearson correlation
    ├── Monotonic (non-linear)        → Spearman rank correlation
    └── Predict Y from X1..Xn          → Linear/logistic regression
```

### Experiment Design Decision

```
What question are you answering?
├── "Does X cause Y?" (Causal)
│   ├── Can randomize? → A/B test (RCT)
│   │   ├── Single treatment vs control      → Simple A/B, t-test
│   │   ├── Multiple variants                 → Multi-arm test, ANOVA + Tukey
│   │   ├── Continuous optimization           → Multi-arm bandit (Thompson sampling)
│   │   └── Network effects / interference    → Switchback or cluster randomization
│   │
│   └── Cannot randomize? → Quasi-experimental
│       ├── Before/after with control group   → Difference-in-Differences (DID)
│       ├── Clear eligibility cutoff          → Regression Discontinuity (RDD)
│       ├── Instrument available              → Instrumental Variables (IV/2SLS)
│       └── Observational, many covariates    → Propensity score matching
│
├── "What will Y be?" (Prediction)
│   ├── Structured/tabular data → XGBoost, LightGBM, CatBoost
│   ├── Time series → ARIMA, Prophet, Temporal Fusion Transformer
│   └── Rare events → SMOTE + balanced ensemble or anomaly detection
│
└── "How do X and Y relate?" (Association/Exploration)
    ├── Which features matter? → SHAP values, permutation importance
    ├── Non-linear patterns? → GAMs, splines, partial dependence plots
    └── Segments behave differently? → Interaction terms, stratified analysis

**What good looks like:** The output opens correctly in the target tool. All validations pass. No placeholder content remains.

```

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
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

### Phase 5 (~25 min): Communication

16. **Craft the narrative — not the methodology**
    - Lead with the decision: "We should ship variant B — +3.2% conversion [95% CI: +1.8%, +4.6%]"
    - Show uncertainty: always include confidence intervals, not just point estimates
    - Visualization: bar charts for comparisons, line charts for trends, waterfall for decomposition
    - Anticipate objections: "But what about segment X?" — pre-compute subgroup results

17. **Write the decision memo**
    - Structure: TL;DR → Business context → Methodology (appendix) → Results → Decision → Risks
    - Input: all analysis outputs. Output: 1-2 page memo + appendix with technical details

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Data scientists translate raw data into business decisions. They coordinate downstream (with ML engineers
for model productionization) and upstream (with data engineers for pipeline reliability). They also
coordinate cross-functionally (with product managers on experiment design, with business strategists on
strategic insights).

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Data Engineer** | Data availability, pipeline freshness, new data sources | Data schema documentation, SLAs for freshness, backfill capabilities, quality checks |
| **Analytics Engineer** | Metric definitions, curated datasets, dbt model design | Metric calculation logic, experiment metric implementation, data model for analysis datasets |
| **ML/AI Engineer** | Model productionization, feature store population, online serving | Model artifacts, feature engineering code, inference pipeline requirements, monitoring thresholds |
| **Product Manager** | Experiment design, hypothesis prioritization, result interpretation | Experiment proposal (hypothesis, MDE, duration), results brief, recommendation with tradeoffs |
| **Business Strategist** | Strategic questions (market sizing, segmentation), long-term trends | Strategic analysis outputs, market opportunity sizing, customer segmentation frameworks |
| **UX Researcher** | Qualitative + quantitative triangulation, survey design | Share quantitative findings for qualitative probing; receive user behavior hypotheses to test quantitatively |
| **Growth Engineer** | A/B test instrumentation, growth experiment design | Experiment tracking setup, metric calculation in growth tools, statistical significance implementation |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| Experiment result is statistically and practically significant | Product Manager, Growth Engineer | Decision to ship/hold; update roadmap |
| Data quality issue discovered during EDA | Data Engineer, Analytics Engineer | Fix pipeline or update quality checks; may invalidate prior analyses |
| Model shows significant bias (demographic disparity) | Product Manager, Compliance Officer | Ethical review; may require model adjustment or decommission |
| Analysis requires data not currently collected | Data Engineer, Product Manager | Instrumentation request; cost/effort tradeoff |
| SRM detected in running experiment | Product Manager, Growth Engineer | Bug in randomization; experiment validity compromised |

### Escalation Path

```
Experiment with revenue risk? → Product Manager → Product Strategist → CEO
Model with fairness/ethical concern? → Compliance Officer → Legal Advisor
Data pipeline blocking analysis? → Data Engineer → DevOps Engineer
Analysis contradicting company strategy? → Business Strategist → CEO Strategist
```

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
- **What changes**: Data scientist = you also do data engineering, analytics, and ML. Focus on fast, directional analyses. Jupyter notebooks are fine. Statistical rigor: report p-values but don't obsess over power analysis. Models are proof-of-concept.
- **What to skip**: Power analysis for every test. Formal experiment documentation. Separate training/serving infrastructure. Model monitoring and drift detection. Multiple comparison corrections for exploratory analyses.
- **Coordination**: Self-contained. Share results as notebook exports or 2-pager memos.
- **Cost**: Free — use Python (scipy, statsmodels, scikit-learn), Jupyter, and Google Colab.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Basic experiment platform (growth tool, feature flag service). Statistical rigor: power analysis before all experiments, SRM checks, CUPED. Peer review of experiment designs before launch. Model versioning with Git. Result documentation in shared knowledge base.
- **What to skip**: Full MLOps pipeline. Experimentation platform (use feature flags + SQL). Causal inference for every question (A/B test when possible).
- **Coordination**: Weekly experiment review. Coordinate with data engineer for pipeline reliability. Share experiment calendar to avoid interaction effects.
- **Cost**: $0-500/month for BI tools. Time: 1-2 days per experiment from design to decision.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Dedicated experimentation platform with automated SRM, sequential testing, CUPED. Full MLOps for production models. Experimentation culture: quarterly planning, experiment review board. Model governance: fairness audits, documentation for compliance. Advanced causal inference for non-randomizable questions.
- **What to skip**: Real-time model serving (batch is fine for most). Custom experimentation platform (use off-the-shelf). Bayesian methods everywhere (frequentist is adequate for most).
- **Coordination**: Bi-weekly experiment review board. Data science guild for methodology standards. Coordinate with compliance for model risk management.
- **Cost**: $2K-10K/month (experimentation platform, compute). Dedicated experimentation PM.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Tiered experimentation (exploratory → canary → holdout → full launch). Model risk management framework. Centralized feature store connecting experiments to production models. Data science platform with shared compute, versioned environments, and reproducibility guarantees. Cross-team experiment interference detection. Federated learning for privacy-sensitive use cases.
- **What's full production**: Experimentation center of excellence. Model cards for all production models. Ethical AI review board. Counterfactual evaluation framework. Data science on-call rotation for critical models.
- **Coordination**: Monthly experiment governance board. Cross-functional model review (legal, compliance, product, engineering). Quarterly methodology audit.
- **Cost**: $50K-200K+/month (platform, compute, dedicated experimentation team, governance).

### Transition Triggers
- **Solo → Small**: Second analyst joins. >100 users making predictive models valuable. First revenue-impacting experiment.
- **Small → Medium**: 5+ parallel experiments. First production model serving customers. Compliance requirements appear.
- **Medium → Enterprise**: 20+ data scientists. Model risk management required by regulation. Cross-team experiment interference observed.

## What Good Looks Like

> Every experiment begins with a pre-registered hypothesis, a power analysis, and a peer-reviewed design before the first user is bucketed. Results include confidence intervals and effect sizes, not just p-values, and the experimentation platform automatically flags SRM violations and peeking issues. Stakeholders make decisions on statistically rigorous evidence within 48 hours of experiment completion, and the experiment knowledge base means no question is tested twice. Models in production have documented performance baselines, and degradation triggers a retrain before any customer notices.

### Cross-skills Integration
```bash
# Analytics models → Statistical analysis → ML models
/analytics-engineer && /data-scientist && /ml-ai-engineer
# Clean datasets → Hypothesis testing → Business decisions
/data-engineer && /data-scientist && /product-manager
# Analytics engineers provide clean, modeled data. Data scientists test hypotheses and build models. ML engineers productionize.
```

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `experiment-design` | Designing A/B tests, multi-arm bandits, quasi-experiments | Power analysis, MDE calculation, SRM checks, peeking corrections, CUPED, sequential testing |
| `statistical-testing` | Choosing and running the right statistical test | Test selection decision tree, assumption checking, effect size + CI reporting, multiple comparison corrections |
| `causal-inference` | When randomization is impossible | DID, RDD, IV/2SLS, propensity score matching, synthetic control, DAG-based identification |
| `eda-methodology` | Initial data exploration and quality assessment | Univariate/bivariate analysis, missing data handling (MCAR/MAR/MNAR), outlier detection, data quality checks |
| `predictive-modeling` | Building models to predict outcomes | Feature engineering, model selection (XGBoost, LightGBM), hyperparameter tuning (Optuna), evaluation metrics |
| `time-series-forecasting` | Forecasting metrics over time | ARIMA, Prophet, exponential smoothing, backtesting, trend/seasonality decomposition, changepoint detection |
| `model-interpretability` | Explaining model predictions to stakeholders | SHAP, LIME, partial dependence plots, permutation importance, ICE plots, accumulated local effects |
| `bayesian-methods` | When prior knowledge exists or uncertainty quantification matters | Bayesian A/B testing, hierarchical models, probabilistic programming (PyMC, Stan), credible intervals |

## Best Practices
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


### Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| `Permission denied` | Missing file/system permissions | Use `chmod +x` or `sudo`; check user/group ownership |
| `command not found` | Required tool not installed | Install with `apt install`, `brew install`, or `npm install -g` |
| `File exists` | Output file already exists | Use `--force` flag or specify different output path |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Business question translated to falsifiable statistical hypothesis (H₀ and Hₐ explicitly stated)
- [ ] **[S2]**  Primary metric defined; guardrail metrics identified; diagnostic metrics mapped
- [ ] **[S3]**  EDA completed: univariate distributions, bivariate relationships, missing data characterized (MCAR/MAR/MNAR)
- [ ] **[S4]**  Data quality issues documented: impossible values, timestamp anomalies, duplicates, measurement errors
- [ ] **[S5]**  Experiment: power analysis completed (α=0.05, power≥0.80); MDE justified in business terms
- [ ] **[S6]**  Experiment: SRM check automated and passing before analysis
- [ ] **[S7]**  Experiment: peeking correction in place (sequential testing or alpha-spending)
- [ ] **[S8]**  Experiment: results reported as effect size + 95% CI + practical significance assessment
- [ ] **[S9]**  Model: chronological or grouped split used (no random split leakage)
- [ ] **[S10]**  Model: baseline model comparison included (always compare to simple heuristic)
- [ ] **[S11]**  Model: interpretability analysis completed (SHAP, LIME, or partial dependence)
- [ ] **[S12]**  Model: fairness evaluation across demographic segments (if relevant)
- [ ] **[S13]**  Decision memo written: TL;DR, context, results, recommendation, risks, next steps
- [ ] **[S14]**  Code, data, and results reproducible (pinned dependencies, seed set, data version documented)
- [ ] **[S15]**  Stakeholder communication: 1-page summary with visualization, technical appendix for peer review

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Statistical Testing Field Manual](references/statistical-testing.md) — Test selection, assumption checking, effect sizes, multiple comparisons
- [A/B Testing Design & Analysis Guide](references/ab-testing-guide.md) — Power analysis, SRM, CUPED, sequential testing, multi-arm bandits
- [Causal Inference Cookbook](references/causal-inference.md) — DID, RDD, IV, propensity scores, DAGs, do-calculus
- [Model Interpretability Guide](references/model-interpretability.md) — SHAP, LIME, partial dependence, fairness evaluation
- Trustworthy Online Controlled Experiments (Kohavi, Tang, Xu) — The A/B testing bible
- Causal Inference: The Mixtape (Cunningham) — Accessible causal inference with code examples
- Statistical Rethinking (McElreath) — Bayesian approach to data science
- https://www.evanmiller.org/ — Practical A/B testing calculators and explainers
