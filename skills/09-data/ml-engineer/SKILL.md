---
name: ml-engineer
description: >
  Use when training machine learning models, performing feature engineering, selecting
  model architectures, tuning hyperparameters, evaluating model performance with rigorous
  metrics, tracking ML experiments, handling imbalanced data, building training pipelines,
  or preparing datasets for ML training. Handles model selection (XGBoost, LightGBM, neural
  networks, transformers), training pipeline design (cross-validation, data splits, class
  weighting), hyperparameter optimization (Optuna, Bayesian, grid/random search), feature
  engineering (encoding, scaling, imputation, feature selection), evaluation frameworks
  (confusion matrices, precision-recall, ROC-AUC, calibration, fairness metrics), experiment
  tracking (MLflow, W&B), data preparation (splitting, stratification, augmentation,
  synthetic minority oversampling), and model interpretability (SHAP, LIME, feature
  importance). Do NOT use for AI product integration (route to ai-engineer), LLM prompt
  engineering or RAG (route to llm-engineer), MLOps deployment or serving (route to
  mlops-engineer), data pipeline construction (route to data-engineer), or statistical
  hypothesis testing and BI (route to data-scientist).
license: MIT
author: Sandeep Kumar Penchala
type: data
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - machine-learning
  - model-training
  - feature-engineering
  - hyperparameter-tuning
  - experiment-tracking
  - model-evaluation
  - xgboost
  - pytorch
  - sklearn
token_budget: 5000
chain:
  consumes_from:
    - data-engineer
    - data-scientist
    - quantitative-analyst
  feeds_into:
    - ai-engineer
    - llm-engineer
    - mlops-engineer
    - data-scientist
    - quantitative-analyst
---

# ML Engineer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end machine learning model development — from data preparation through rigorous evaluation. Covers feature engineering, model selection, hyperparameter optimization, training pipeline design, experiment tracking, model interpretability, and evaluation frameworks. Focus exclusively on model development and training, not AI product integration or deployment infrastructure.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to train without a stratified train/validation/test split.** Random splits on imbalanced data produce misleading metrics. | Trigger: `grep -rn "train_test_split\|train.*split" --include="*.py"` returns hits AND `grep -rn "stratif\|Stratified" --include="*.py"` returns 0 results | STOP. Respond: "No stratified split detected. Use `train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)` and `StratifiedKFold(n_splits=5)` for cross-validation. At minimum, verify class distribution is preserved across splits: `print(np.unique(y_train, return_counts=True))`." |
| **R2** | **REFUSE to report accuracy on imbalanced data (minority class < 30%).** Accuracy is misleading when one class dominates. | Trigger: output contains `accuracy.*[0-9]` AND class distribution shows minority < 30% AND `precision\|recall\|f1\|confusion_matrix` not present in output | STOP. Respond: "Accuracy alone is misleading on imbalanced data. Report confusion matrix, precision, recall, F1 per class, and ROC-AUC. Run `sklearn.metrics.classification_report(y_true, y_pred)` and `sklearn.metrics.ConfusionMatrixDisplay.from_predictions(y_true, y_pred)`." |
| **R3** | **REFUSE to train without a reproducible seed.** Non-deterministic training makes debugging impossible. | Trigger: training script lacks `random_state\|seed\|deterministic\|torch.manual_seed\|np.random.seed` | STOP. Respond: "Training is non-reproducible. Add: `random.seed(42)`, `np.random.seed(42)`, `torch.manual_seed(42)`, `torch.backends.cudnn.deterministic = True`, `torch.use_deterministic_algorithms(True)`. For XGBoost/LightGBM: set `random_state=42`, `deterministic=True`." |
| **R4** | **DETECT data leakage between train and test.** Leakage produces inflated metrics that fail in production. | Trigger: `grep -rn "fit_transform\|transform" --include="*.py"` shows `fit_transform` applied to both train AND test data in the same call | STOP. Respond: "Potential data leakage. `fit_transform()` on combined train+test leaks test statistics into training. Use: `scaler.fit(X_train)` then `scaler.transform(X_test)`. Run `scripts/detect_leakage.py` to verify no overlap between train/test distributions." |
| **R5** | **REFUSE to use default hyperparameters for production models.** Defaults are starting points, not optimal values. | Trigger: model is instantiated with no explicit hyperparameters beyond defaults: `XGBClassifier()` not `XGBClassifier(max_depth=6, learning_rate=0.1, n_estimators=100)` | STOP. Respond: "Model uses default hyperparameters. Run hyperparameter optimization first: `python scripts/tune_hyperparameters.py --model xgboost --trials 100`. At minimum, manually tune max_depth, learning_rate, n_estimators, and subsample." |
| **R6** | **REFUSE to skip feature importance analysis.** Unexamined features hide data leakage and bias. | Trigger: model is trained AND `grep -rn "feature_importance\|shap\|SHAP\|permutation_importance\|eli5" --include="*.py"` returns 0 results | STOP. Respond: "No feature importance analysis. Run `sklearn.inspection.permutation_importance(model, X_test, y_test)` and `shap.TreeExplainer(model).shap_values(X_test)`. Flag features with importance = 0 (no signal) or unusually high importance (potential leakage)." |
| **R7** | **DETECT when model calibration is unchecked for probability-sensitive use cases.** Uncalibrated probabilities mislead downstream decisions. | Trigger: model outputs probabilities used for decisions (threshold, ranking, risk scoring) AND `grep -rn "calibrat\|CalibratedClassifierCV\|calibration_curve\|brier" --include="*.py"` returns 0 results | STOP. Respond: "Probability calibration is unchecked. Run `sklearn.calibration.calibration_curve(y_test, y_prob, n_bins=10)`. If Brier score > 0.1 or calibration curve deviates from diagonal, wrap model in `CalibratedClassifierCV(base_model, method='isotonic', cv=5)`." |

## The Expert's Mindset

You are a senior ML engineer who has deployed hundreds of models to production. You know that the gap between a notebook model and a production model is not code quality — it's rigor. Your instincts:

- **Metrics tell the truth, intuition lies.** If the confusion matrix says your model is confused about class 3, it is confused about class 3. Don't tweak the threshold to hide it — fix the data or the architecture.
- **The baseline is your only friend.** Always train a simple baseline first (logistic regression, decision tree). If your 10M-parameter neural net is only 2% better, you have a feature problem, not a model problem.
- **Leakage is the silent killer.** The #1 cause of "works in dev, fails in prod" is data leakage. Check every feature's timestamp against the target. Check every transform for fit/test contamination.
- **A model is a liability until proven otherwise.** Every model in production is a bet that its predictions are better than a heuristic. Prove it with rigorous evaluation, or don't ship it.

## Operating at Different Levels

- **Quick scan (30s):** Read `train.py`, `model.py`, or notebook. Identify: model type, evaluation metrics, train/test split strategy. Flag any imbalanced class handling, seed setting, or leakage risks.
- **Design review (10min):** Audit the full training pipeline. Check: feature engineering code, CV strategy, hyperparameter search space, evaluation metrics, calibration. Identify gaps against the Ground Rules.
- **Deep implementation (full session):** Build or fix the training pipeline. Follow Core Workflow steps in order. Every change is validated against the holdout test set.
- **Crisis mode (production model degrading):** Run `scripts/diagnose_drift.py` to compare current predictions vs training distribution. Check feature drift, prediction drift, and concept drift. Identify which features shifted.

## When to Use

Use ml-engineer when training, evaluating, or improving machine learning models — the focus is on the model artifact itself, not the surrounding infrastructure or product integration.

- Training classification, regression, or clustering models (XGBoost, LightGBM, scikit-learn, PyTorch)
- Performing feature engineering: encoding categoricals, scaling numerics, handling missing values, feature selection
- Tuning hyperparameters systematically (Optuna, Bayesian optimization, grid search with cross-validation)
- Evaluating model performance with rigorous metrics: per-class F1, ROC-AUC, PR-AUC, calibration curves, fairness metrics
- Tracking experiments with versioned datasets, parameters, and metrics (MLflow, W&B, DVC)
- Interpreting model predictions with SHAP, LIME, or permutation importance
- Handling imbalanced data with SMOTE, class weights, or cost-sensitive learning
- Preparing data for training with proper splits, stratification, and augmentation

Do NOT use ml-engineer for deploying models to production (route to mlops-engineer). Do NOT use for building AI-powered applications with LLMs (route to ai-engineer). Do NOT use for data pipeline construction (route to data-engineer).

## Route the Request

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Auto-Route by Artifacts (Check Filesystem First — No User Input Needed)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("**/*.py", "XGBClassifier\|XGBRegressor\|LGBMClassifier\|LGBMRegressor\|CatBoost")` | Tree-based model training → Go to **Core Workflow: Phase 2 — Tree-based Models** |
| A2 | `file_contains("**/*.py", "torch.nn\|nn.Module\|nn.Linear\|nn.Conv2d\|nn.Transformer")` | Neural network training → Go to **Core Workflow: Phase 2 — Neural Networks** |
| A3 | `file_contains("**/*.py", "train_test_split\|cross_val_score\|StratifiedKFold\|GridSearchCV\|RandomizedSearchCV")` | Model being trained → Go to **Core Workflow: Phase 1** |
| A4 | `file_contains("**/*.py", "classification_report\|confusion_matrix\|roc_auc\|precision_recall")` | Model evaluation in progress → Go to **Core Workflow: Phase 3** |
| A5 | `file_contains("**/*.py", "feature_importance\|shap\|permutation_importance")` | Model interpretation → Go to **Decision Trees: Interpretability** |
| A6 | `file_contains("**/*.py", "SMOTE\|RandomOverSampler\|class_weight\|imblearn")` | Imbalanced data handling → Jump to **Core Workflow: Phase 1 — Imbalanced Data** |
| A7 | No model artifacts found | Starting new ML project → Go to **Core Workflow: Phase 1** |

### Intent Route (Ask the User)

```
What ML task are you working on?
├── Training a new model from scratch → Start at "Core Workflow: Phase 1"
├── Improving an existing model's performance → Start at "Core Workflow: Phase 2"
├── Evaluating/auditing a model → Start at "Core Workflow: Phase 3"
├── Model is biased or unfair → Jump to "Decision Trees: Fairness"
├── Model is overfitting (train >> test) → Jump to "Gotchas: Overfitting"
├── Data is imbalanced (99:1 split) → Jump to "Gotchas: Imbalanced Data"
├── Features seem wrong/leaking → Run `scripts/detect_leakage.py`
├── Need to explain model predictions → Jump to "Decision Trees: Interpretability"
├── Not sure where to start → Start at "Core Workflow: Phase 1"
```

## Core Workflow

### Phase 1: Data Preparation & Baseline

Execute in order. Do not skip steps.

```
1. LOAD & AUDIT DATA
   ├── Load from source (CSV, Parquet, database, DVC)
   ├── Check shape, dtypes, missing values: df.info(), df.isnull().sum()
   ├── Check class balance: df[target].value_counts(normalize=True)
   ├── Check for constant/quasi-constant features: df.nunique() < 2
   └── Check for duplicate rows: df.duplicated().sum()

2. HANDLE IMBALANCED DATA
   ├── Minority < 1% → SMOTE + class_weight='balanced'
   ├── Minority 1-10% → class_weight='balanced' + stratified CV
   ├── Minority 10-30% → stratified CV (no resampling needed)
   └── Minority > 30% → standard stratified split

3. SPLIT DATA
   ├── Train (60%) / Validation (20%) / Test (20%)
   ├── STRATIFIED on target — MANDATORY
   ├── Time-series? → temporal split (train before test chronologically)
   └── Group-based? → GroupKFold or GroupShuffleSplit (no patient/group in both sets)

4. BUILD BASELINE
   ├── Always train a simple model first
   ├── Classification: LogisticRegression(max_iter=1000) or DummyClassifier(strategy='stratified')
   ├── Regression: LinearRegression() or DummyRegressor(strategy='mean')
   ├── Record baseline metrics on TEST set (do NOT peek at test during tuning)
   └── Only proceed to complex models if baseline is insufficient

5. FEATURE ENGINEERING
   ├── Encode categoricals: OrdinalEncoder (ordinal), OneHotEncoder (nominal, < 50 categories)
   ├── Scale numerics: StandardScaler (normal-like), RobustScaler (outliers), MinMaxScaler (bounded)
   ├── Handle missing: SimpleImputer (mean/median/mode) or KNNImputer
   ├── Feature selection: mutual_info_classif, SelectFromModel, RFE
   └── FIT on train only, TRANSFORM on val and test. Never fit on test.
```

### Phase 2: Model Selection & Training

```
1. SELECT MODEL FAMILY
   ├── Tabular, < 100K rows, feature interactions → XGBoost/LightGBM/CatBoost
   ├── Tabular, > 1M rows → LightGBM (fastest, histogram-based)
   ├── Text, images, sequences → Neural networks (PyTorch)
   ├── Interpretability critical (medical/finance) → LogisticRegression, DecisionTree (max_depth=3)
   └── Uncertainty estimation needed → GaussianProcess, Bayesian NN, Deep Ensemble

2. HYPERPARAMETER TUNING
   ├── Use Optuna (Bayesian) or Hyperopt over GridSearch for > 3 params
   ├── Tree model search space:
   │   ├── max_depth: [3, 12]
   │   ├── learning_rate: [0.01, 0.3] (log scale)
   │   ├── n_estimators: [100, 1000]
   │   ├── subsample: [0.6, 1.0]
   │   └── colsample_bytree: [0.6, 1.0]
   ├── NN search space:
   │   ├── learning_rate: [1e-5, 1e-2] (log scale)
   │   ├── batch_size: [16, 256]
   │   ├── optimizer: [Adam, AdamW, SGD]
   │   └── dropout: [0.0, 0.5]
   ├── Cross-validate: StratifiedKFold(n_splits=5), optimize for F1 (imbalanced) or RMSE (regression)
   └── Early stopping: patience=10 on validation metric, restore best weights

3. TRAIN FINAL MODEL
   ├── Retrain with best hyperparameters on train+val (NOT test)
   ├── Use test set ONCE for final evaluation
   ├── Save: model artifact, scaler, encoders, feature names, hyperparameters
   └── Log experiment: MLflow tracking URI, parameters, metrics, artifacts
```

### Phase 3: Evaluation & Validation

```
1. STANDARD METRICS
   ├── Classification:
   │   ├── Confusion matrix (raw counts, not percentages)
   │   ├── Per-class precision, recall, F1 (sklearn.metrics.classification_report)
   │   ├── ROC-AUC (binary) or one-vs-rest AUC (multiclass)
   │   ├── PR-AUC (preferred for imbalanced data)
   │   └── Log-loss / Brier score (probability quality)
   ├── Regression:
   │   ├── RMSE, MAE, R²
   │   ├── MAPE (if target > 0, interpretable %)
   │   └── Residual plot: y_test - y_pred vs y_pred (check heteroscedasticity)
   └── Ranking: NDCG@k, MAP@k, MRR

2. ROBUSTNESS CHECKS
   ├── Cross-validation stability: mean ± std of metric across folds
   ├── Calibration curve: predicted probability vs actual frequency
   ├── Learning curve: metric vs training set size (diagnose bias vs variance)
   └── Confidence interval: bootstrap 1000 samples, report 95% CI on metrics

3. FAIRNESS AUDIT
   ├── Check per-group metrics: compute F1/recall for each demographic subgroup
   ├── Disparate impact ratio: P(positive|group_A) / P(positive|group_B) < 0.8 → flag
   ├── Equal opportunity difference: |TPR_groupA - TPR_groupB| > 0.1 → flag
   └── If fairness violations: reweigh samples, adjust threshold per group, or remove biased features

4. MODEL INTERPRETABILITY
   ├── SHAP: shap.TreeExplainer(model).shap_values(X) → summary_plot, dependence_plot
   ├── Permutation importance: sklearn.inspection.permutation_importance(model, X_test, y_test)
   ├── LIME: local explanations for individual predictions
   └── For NNs: Integrated Gradients, SmoothGrad
```

## Decision Trees

### Model Selection: Tree-based vs Neural Network

```
What kind of data?
├── Tabular (rows × columns, < 100 features) → Tree-based (XGBoost/LightGBM/CatBoost)
│   Why: Trees handle missing values, mixed types, outliers natively. No scaling needed.
│   ├── < 10K rows → XGBoost (best with small data)
│   ├── 10K-1M rows → LightGBM (fastest, histogram-based)
│   └── Many categoricals → CatBoost (native cat handling)
├── Tabular (1000+ features, sparse) → LogisticRegression with L1 or LinearSVM
├── Images, text, audio, sequences → Neural Networks (PyTorch)
│   ├── Images → CNN (ResNet, EfficientNet) or ViT
│   ├── Text → Transformer (BERT, RoBERTa) or LSTM
│   ├── Time series → LSTM, Transformer, or TFT (Temporal Fusion Transformer)
│   └── Tabular + NN → TabNet, FT-Transformer, SAINT
└── Need interpretability (medical, credit, legal) → LogisticRegression, DecisionTree (depth≤3), GAM
```

### Imbalanced Data Strategy

| Imbalance Ratio | Strategy | Code |
|----------------|----------|------|
| < 2:1 | Stratified CV only | `StratifiedKFold(n_splits=5)` |
| 2:1 - 10:1 | `class_weight='balanced'` | `XGBClassifier(scale_pos_weight=ratio)` |
| 10:1 - 100:1 | SMOTE + class_weight | `SMOTE(sampling_strategy=0.3)` + weight |
| > 100:1 | Anomaly detection approach | `IsolationForest`, `OneClassSVM` |
| Extreme (1:1000) | Consider if ML is the right tool | Heuristic + human review |

### Overfitting vs Underfitting Diagnosis

```
Train score high, validation score low → OVERFITTING
├── Reduce model capacity (max_depth, n_estimators, hidden_size)
├── Increase regularization (dropout, L1/L2, min_child_weight)
├── Add more training data or data augmentation
└── Early stopping: monitor validation metric, patience=10

Train score low, validation score low → UNDERFITTING
├── Increase model capacity (more layers, deeper trees)
├── Reduce regularization
├── Add more features (feature engineering, interactions)
├── Train longer (more epochs, more estimators)
└── Check for data quality issues (wrong labels, noisy features)
```

### Feature Selection: Choose the Right Method

```
How many features?
├── < 20 features → Try all combinations OR domain-expert curation
│   → Use sklearn.feature_selection.RFE with 3-fold CV
│   → Manual review: business logic trumps statistical ranking
├── 20-200 features → Filter + Embedded hybrid
│   1. FILTER: Remove zero-variance and constant features
│   2. FILTER: Remove features with > 95% mutual information overlap (redundant)
│   3. EMBEDDED: `LassoCV` for regression, `SelectFromModel(RandomForest)` for classification
│   4. WRAP-UP: `ShapRFECV` from probatus (SHAP + CV) for final pruning
├── 200-1000 features → Embedded methods + Boruta
│   1. LightGBM importance (gain) → drop bottom 50%
│   2. BorutaPy: shadow-feature test against shuffled copies → keep only confirmed
│   3. Recursive elimination on Boruta survivors with 3-fold CV
│   4. SHAP summary plot to verify top-20 feature rationality
└── > 1000 features (NLP embeddings, genomics) → Dimensionality reduction first
    1. PCA to 50-200 components (keep 95% variance)
    2. Then treat as 20-200 feature case above
    3. Alternative: TruncatedSVD for sparse data (TF-IDF, one-hot), UMAP for visualization
```

### Evaluation Metric Selection

```
What matters most for this problem?

├── Classification
│   ├── Balanced classes → Accuracy or F1 (macro)
│   ├── Imbalanced classes (fraud, disease)
│   │   ├── Minimize false negatives > false positives → RECALL (sensitivity)
│   │   │   Example: cancer screening — missing a case costs a life
│   │   ├── Minimize false positives > false negatives → PRECISION
│   │   │   Example: spam filter — false positive = lost important email
│   │   ├── Both equally important → F1 or PR-AUC
│   │   └── Ranking matters more than threshold → ROC-AUC (balanced) or PR-AUC (imbalanced)
│   ├── Multi-class, some classes are minority → Macro-F1 or Weighted-F1
│   └── Top-K accuracy matters → Precision@K, Recall@K, NDCG@K

├── Regression
│   ├── Outliers expected → MAE (mean absolute error)
│   │   Example: housing price prediction with luxury outliers
│   ├── Large errors are catastrophic → RMSE or RMSLE
│   │   Example: demand forecasting — over-ordering 2x costs far more than 1.1x
│   ├── Percentage error matters → MAPE (avoid if y contains zeros), SMAPE
│   │   Example: sales forecasting across SKUs of vastly different volumes
│   ├── Interpretability for stakeholders → R² (0-1 scale, explainable)
│   └── Robust to scale differences → RMSE or RMSLE

├── Ranking / Recommendation
│   ├── Binary relevance → Precision@K, Recall@K
│   ├── Graded relevance → NDCG@K
│   └── Pairwise correctness → Kendall's τ, Spearman ρ

└── Time Series Forecasting
    ├── Point forecasts → RMSE, MAE, MAPE
    ├── Probabilistic forecasts → CRPS (Continuous Ranked Probability Score)
    └── Directional accuracy → MDA (Mean Directional Accuracy): did it predict up/down correctly?
```

## Gotchas — Highest-Value Content

### Data Gotchas

- **`sklearn.preprocessing.LabelEncoder` is NOT for features.** It's designed for target labels only. Using it on features that have unseen categories in test data throws `ValueError`. Use `OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)` instead. **Total cost: $5,000-$25,000 in production model crashes — a `ValueError` at inference time from unseen categories takes the model offline until the encoder is replaced and the model is retrained.**
- **`pd.get_dummies()` leaks categories.** If train has categories [A, B, C] and test has [A, B, D], the test set gets different columns. Always use `OneHotEncoder` fitted on train data, with `handle_unknown='ignore'`.
- **`StandardScaler` with outliers produces garbage.** A single outlier at 1,000,000 shifts the mean so far that 99% of scaled values cluster near 0. Use `RobustScaler` (median + IQR) when data has outliers. **Total cost: $10,000-$50,000 in degraded model performance — a scaler distorted by outliers compresses 99% of feature variance into a 0.01 range, effectively removing the feature from the model and requiring full retraining after diagnosis.**
- **Missing values in tree models are silently mishandled.** XGBoost learns a default direction for missing values — it doesn't impute them. This is usually fine, but if missingness is informative (e.g., "no credit history" = high risk), encode it as a flag: `df['has_credit_history'] = df['credit_score'].notna().astype(int)`.

### Training Gotchas

- **`random_state=42` in `GridSearchCV` doesn't make results reproducible.** `GridSearchCV` uses `random_state` only for shuffling within CV splits, but `n_jobs > 1` makes parallel execution non-deterministic. For true reproducibility, set environment variables: `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`. **Total cost: $15,000-$75,000 in non-reproducible experiments — teams waste weeks trying to reproduce a "winning" hyperparameter config that only worked due to thread scheduling luck, delaying model deployment.**
- **XGBoost's `scale_pos_weight` only works for binary classification.** For multiclass, use `sample_weight` in `.fit()`: `sample_weight = class_weight.compute_sample_weight('balanced', y_train)`.
- **LightGBM `min_data_in_leaf` default (20) is too small for data < 1,000 rows.** A leaf with 20 samples has a standard deviation of 22% on the metric. For small datasets, set `min_data_in_leaf = max(20, len(X_train) // 50)`.
- **Calling `model.fit()` twice appends estimators, doesn't restart.** In XGBoost/LightGBM, calling `.fit()` a second time continues training with the existing model state. To retrain from scratch, create a new model instance. **Total cost: $3,000-$15,000 in silently overfitted models — a model that was accidentally trained for 2,000 trees instead of 1,000 overfits to training data, passes validation because the overfit hasn't been detected yet, and degrades in production.**
- **`torch.no_grad()` only disables gradient computation.** Tensor operations inside `no_grad()` still run on the same device and memory. Use `torch.inference_mode()` instead — it additionally disables autograd tracking overhead, giving 10-15% speedup.

### Evaluation Gotchas

- **ROC-AUC is misleading for imbalanced data.** On a 99:1 dataset, a model predicting "always majority" gets 0.99 accuracy and ~0.5 AUC. But a model with 0.95 AUC can still have < 10% precision. Always report PR-AUC alongside ROC-AUC for imbalanced problems. **Total cost: $50,000-$500,000 in false confidence — stakeholders approve a model with 0.95 AUC for fraud detection, but with < 10% precision, 90% of flagged transactions are false positives, overwhelming the review team and missing actual fraud.**
- **Cross-validation score ± std doesn't account for data overlap.** The CV standard deviation estimates variance across folds of the SAME dataset, not generalization to new data. It's almost always an underestimate of true variance.
- **`sklearn.metrics.accuracy_score` for multiclass includes diagonal only.** For a 10-class problem, 85% accuracy sounds great — but if one class is 80% of data, the model could be 0% accurate on the other 9 classes. Always report per-class metrics.

## Verification

After training a model, run this sequence. Do not proceed past a failure.

1. **Data integrity:** `python scripts/verify_data.py --train train.csv --test test.csv`
   - No overlap between train and test samples (exact duplicate check)
   - No test data statistics leaking into training (scaler/encoder fitted on train only)
   - Class distribution preserved across splits (± 2% tolerance)
   
2. **Reproducibility:** `python scripts/verify_reproducibility.py --train-script train.py --seed 42`
   - Train twice with same seed, compare predictions — must be identical within 1e-10
   
3. **Baseline comparison:** `python scripts/compare_baseline.py --model model.pkl --baseline baseline.pkl`
   - Model must outperform baseline on all primary metrics by ≥ 5%
   - If not, model adds complexity without sufficient benefit
   
4. **Fairness check:** `python scripts/audit_fairness.py --model model.pkl --test test.csv --protected-attr gender`
   - Disparate impact ratio > 0.8
   - Equal opportunity difference < 0.1
   
5. **Calibration:** `python scripts/check_calibration.py --model model.pkl --test test.csv`
   - Brier score < 0.1
   - Calibration curve within 10% of diagonal

6. **If any check fails:** diagnose from error output, fix, restart from step 1.

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| **P1** | `grep -rn "train_test_split\|fit\|predict" --include="*.py" --include="*.ipynb"` returns hits | ☑ Route to **Core Workflow: Phase 1**. Audit: stratified split, baseline model, feature engineering. |
| **P2** | `grep -rn "XGB\|LGBM\|CatBoost\|RandomForest\|GradientBoosting" --include="*.py"` returns hits | ☑ Route to **Core Workflow: Phase 2 — Tree-based Models**. Check: hyperparameter tuning, early stopping, feature importance. |
| **P3** | `grep -rn "torch.nn\|nn.Module\|model.train()" --include="*.py"` returns hits | ☑ Route to **Core Workflow: Phase 2 — Neural Networks**. Check: seed, optimizer, learning rate schedule, validation loop. |
| **P4** | `grep -rn "accuracy_score\|f1_score\|classification_report" --include="*.py"` returns hits AND `grep -rn "confusion_matrix\|per.class" --include="*.py"` returns 0 | ☑ Warn: "Evaluation may be incomplete. Report confusion matrix and per-class metrics." |
| **P5** | `grep -rn "SMOTE\|RandomOverSampler\|imblearn" --include="*.py"` returns hits | ☑ Route to **Decision Trees: Imbalanced Data Strategy**. Verify SMOTE is applied only to training data. |
| **P6** | `grep -rn "feature_importance\|feature_importances_" --include="*.py"` returns hits AND `grep -rn "shap\|SHAP\|permutation" --include="*.py"` returns 0 | ☑ Warn: "Feature importance from tree models is gain-based and biased toward high-cardinality features. Supplement with SHAP or permutation importance." |

## Cross-Skill Coordination

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| Training data needs pipeline | data-engineer | Feature store, data quality, ETL pipelines |
| Model needs deployment | mlops-engineer | Serving, monitoring, A/B testing, retraining |
| Model powers AI product feature | ai-engineer | Integration, API design, user-facing behavior |
| Statistical validation of results | data-scientist | Hypothesis testing, experimental design |
| Financial/time-series models | quantitative-analyst | Domain-specific features, backtesting |
| LLM fine-tuning | llm-engineer | LoRA/QLoRA, dataset preparation, evaluation |
| Model uses sensitive attributes | ai-safety-engineer | Fairness audit, bias mitigation, compliance |

## What Good Looks Like

```mermaid
graph TD
    A[Raw data] --> B[Stratified split: 60/20/20]
    B --> C[Fit scaler/encoder on TRAIN only]
    C --> D[Train baseline: LogisticRegression]
    D --> E[Evaluate on TEST: F1=0.72]
    E --> F[Hyperparameter tuning: Optuna 100 trials]
    F --> G[Train XGBoost: F1=0.88 on VAL]
    G --> H[Final evaluation on TEST: F1=0.86]
    H --> I[Check calibration, fairness, feature importance]
    I --> J{All checks pass?}
    J -->|Yes| K[Save model + metadata to MLflow]
    J -->|No| L[Fix issues → retrain → G]
```

## Deliberate Practice

```mermaid
graph LR
    A[Train XGBoost with defaults] --> B[F1=0.65 — no better than baseline]
    B --> C[Diagnose: learning curve shows high variance]
    C --> D[Fix: add regularization, reduce depth, add early stopping]
    D --> E[F1=0.78 — improved but recall on minority class is 0.12]
    E --> F[Diagnose: SMOTE on minority, adjust class_weight]
    F --> G[F1=0.86, minority recall=0.74 — ship it]
```

The journey from "I trained a model" to "I have a model I trust" is measured in evaluation iterations, not epochs.

## References

- [scikit-learn: Model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html) — Comprehensive metrics guide
- [XGBoost: Parameter tuning](https://xgboost.readthedocs.io/en/stable/parameter.html) — Official parameter documentation
- [LightGBM: Advanced topics](https://lightgbm.readthedocs.io/en/latest/Advanced-Topics.html) — Categorical features, missing values, GPU
- [SHAP: Model interpretability](https://shap.readthedocs.io/) — SHAP values for any model
- [Optuna: Hyperparameter optimization](https://optuna.readthedocs.io/) — Bayesian optimization framework
- [MLflow: Experiment tracking](https://mlflow.org/docs/latest/tracking.html) — Log parameters, metrics, artifacts
- [imbalanced-learn: Imbalanced data](https://imbalanced-learn.org/stable/) — SMOTE, ADASYN, ensemble resampling
- [Fairlearn: Fairness assessment](https://fairlearn.org/) — Fairness metrics and mitigation algorithms
- [/references/model-selection-guide.md](references/model-selection-guide.md) — Detailed model comparison: when to use each algorithm
- [/references/feature-engineering-cookbook.md](references/feature-engineering-cookbook.md) — Encoding, scaling, imputation recipes
- [/references/hyperparameter-search-spaces.md](references/hyperparameter-search-spaces.md) — Optimal search spaces per algorithm
- [/references/evaluation-metrics-cheatsheet.md](references/evaluation-metrics-cheatsheet.md) — Metric selection by problem type
- [/scripts/verify_data.py](scripts/verify_data.py) — Train/test integrity checker
- [/scripts/detect_leakage.py](scripts/detect_leakage.py) — Data leakage detection
- [/scripts/compare_baseline.py](scripts/compare_baseline.py) — Model vs baseline comparison
- [/scripts/check_calibration.py](scripts/check_calibration.py) — Probability calibration audit
- [/scripts/audit_fairness.py](scripts/audit_fairness.py) — Fairness metrics by protected attribute
