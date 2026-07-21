# ML Workflow Guide

> **Author:** Sandeep Kumar Penchala

End-to-end machine learning workflow patterns covering project lifecycle, model selection, feature engineering, experiment tracking, evaluation metrics, deployment patterns, and production monitoring. These practices support the data-scientist skill's ML project lifecycle.

## ML Project Lifecycle

```
Problem Framing → Data Collection → Exploratory Data Analysis → Feature Engineering
→ Modeling → Evaluation → Deployment → Monitoring → (Iterate)
```

### Phase Checklist

```markdown
## Problem Framing
- [ ] Business objective defined (increase conversion by X%)
- [ ] ML is the right tool (not a heuristic or rule-based system)
- [ ] Success metrics agreed with stakeholders
- [ ] Baseline established (current performance without ML)
- [ ] Data availability confirmed; access granted

## Data Collection
- [ ] Sources identified (DB, API, logs, third-party)
- [ ] Data pipeline built (ETL/ELT)
- [ ] Data quality assessed (missing %, outliers, distributions)
- [ ] Volume sufficient for chosen model complexity
- [ ] Labels available (or labeling strategy defined)
- [ ] Train/validation/test split strategy defined (time-based for temporal data)
```

## Model Selection Framework

```
Problem type?
├── Classification (discrete output: yes/no, category)
│   ├── < 100K rows, tabular data        → XGBoost / LightGBM
│   ├── > 100K rows, tabular data        → XGBoost → Neural Network if needed
│   ├── Image                             → CNN (ResNet, EfficientNet); ViT for large data
│   └── Text                              → BERT / RoBERTa → fine-tune
├── Regression (continuous output: price, score)
│   ├── Linear relationships              → Linear/Logistic Regression, Ridge, Lasso
│   ├── Non-linear, tabular               → XGBoost / LightGBM / CatBoost
│   └── Deep, complex interactions        → Neural Networks (MLP, TabNet)
├── Clustering (unsupervised grouping)
│   ├── Known cluster count               → K-Means
│   ├── Unknown cluster count             → DBSCAN, HDBSCAN
│   └── High-dimensional                  → PCA → K-Means or UMAP → HDBSCAN
└── Time Series (forecasting)
    ├── Univariate, simple patterns       → ARIMA / SARIMA
    ├── Multivariate, complex             → Prophet, LightGBM with lags
    └── Deep learning, huge data          → TFT (Temporal Fusion Transformer), N-BEATS
```

### Interpretability vs Performance Tradeoff

```
High interpretability needed (regulated, healthcare, credit)?
├── Linear/Logistic Regression, Decision Trees (shallow)
└── Use SHAP/LIME to explain black-box models

Performance trumps interpretability?
├── Gradient Boosted Trees (XGBoost/LightGBM/CatBoost)
└── Deep Learning (if data volume justifies it)
```

## Feature Engineering Patterns

### Encoding Categorical Variables

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# One-Hot Encoding — low cardinality (< 15 categories)
df = pd.get_dummies(df, columns=['country', 'device_type'], drop_first=True)

# Target Encoding — high cardinality (50+ categories), prevents leakage
# Use cross-validated target encoding to avoid data leakage
from category_encoders import TargetEncoder
encoder = TargetEncoder(cols=['zip_code'], smoothing=10)
df_train['zip_code_encoded'] = encoder.fit_transform(df_train['zip_code'], df_train['target'])

# Embedding — very high cardinality (1000+ categories, NLP-like)
# Use Entity Embeddings via neural network embedding layer
```

### Scaling Numerical Features

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# Standard (z-score) — most algorithms, assumes ~normal distribution
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Min-Max [0, 1] — neural networks, distance-based algorithms
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Robust — when outliers are present (uses median/IQR)
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)
```

### Missing Value Strategies

```python
# Strategy depends on missing mechanism (MCAR, MAR, MNAR)
import numpy as np

# 1. Simple imputation
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='median')   # Numerical: median/mean
imputer = SimpleImputer(strategy='most_frequent')  # Categorical: mode
imputer = SimpleImputer(strategy='constant', fill_value='MISSING')

# 2. Add missing indicator (tells model "this value was missing")
df['age_missing'] = df['age'].isna().astype(int)

# 3. Model-based imputation (KNN, MICE)
from sklearn.impute import KNNImputer
imputer = KNNImputer(n_neighbors=5)

# 4. Tree-based models (XGBoost/LightGBM) handle missing natively
# No imputation needed — the model learns optimal split for NaN
```

## Experiment Tracking

### MLflow Structure

```python
import mlflow

mlflow.set_experiment("customer-churn-prediction")

with mlflow.start_run(run_name="xgboost-v2"):
    # Log parameters
    mlflow.log_params({
        "model_type": "xgboost",
        "max_depth": 6,
        "learning_rate": 0.05,
        "n_estimators": 500,
        "subsample": 0.8,
    })

    # Train model
    model = xgb.XGBClassifier(**params)
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], early_stopping_rounds=50)

    # Log metrics
    y_pred = model.predict(X_val)
    mlflow.log_metrics({
        "accuracy": accuracy_score(y_val, y_pred),
        "f1": f1_score(y_val, y_pred),
        "auc_roc": roc_auc_score(y_val, y_pred),
    })

    # Log model + feature importance
    mlflow.xgboost.log_model(model, "model")
    mlflow.log_artifact("feature_importance.png")

    # Reproducibility: log git commit + data hash
    mlflow.set_tag("git_commit", "abc1234")
    mlflow.set_tag("data_hash", hash_data(X_train))
```

## Evaluation Metrics by Problem Type

| Problem | Primary Metric | Secondary Metric | When to Use |
|---------|---------------|-----------------|-------------|
| Binary Classification (balanced) | Accuracy | F1, AUC-ROC | Classes roughly equal |
| Binary Classification (imbalanced) | F1 or AUC-PR | AUC-ROC | Fraud, rare disease detection |
| Multi-class Classification | Macro F1 | Accuracy | Equal importance per class |
| Regression (no outliers) | RMSE | MAE | Normal error distribution |
| Regression (with outliers) | MAE | R² | Robust to outliers |
| Ranking | NDCG@k | MAP@k | Search, recommendations |
| Time Series | SMAPE, MASE | RMSE | Forecast accuracy |

## Deployment Patterns

### Batch Inference

```python
# Run daily batch predictions; write results to DB
import pandas as pd
from sqlalchemy import create_engine

def batch_inference():
    # Load features from data warehouse
    df = pd.read_sql("SELECT * FROM features WHERE date = CURRENT_DATE", engine)
    # Load model
    model = mlflow.xgboost.load_model("models:/churn-predictor/production")
    # Predict
    df['churn_probability'] = model.predict_proba(df[feature_cols])[:, 1]
    # Write results
    df[['customer_id', 'churn_probability']].to_sql('churn_predictions', engine, if_exists='append')
```

### Real-Time API

```python
from fastapi import FastAPI
import mlflow, xgboost

app = FastAPI()
model = mlflow.xgboost.load_model("models:/churn-predictor/production")

@app.post("/predict/churn")
async def predict_churn(features: dict):
    df = pd.DataFrame([features])
    proba = model.predict_proba(df)[:, 1][0]
    return {"churn_probability": float(proba), "at_risk": proba > 0.5}
```

### Feature Store Integration

```
Offline (training): Feature Store → Training Dataset → Model Training
Online (serving):  Request → Feature Store (low-latency) → Model → Prediction

Tools: Feast, Tecton, SageMaker Feature Store
```

## Production Monitoring

### Data Drift Detection

```python
from scipy.stats import ks_2samp
import numpy as np

def detect_drift(reference_data: np.ndarray, current_data: np.ndarray, threshold: float = 0.05):
    """Detect distribution shift using Kolmogorov-Smirnov test."""
    statistic, p_value = ks_2samp(reference_data, current_data)
    drifted = p_value < threshold
    return {"drifted": drifted, "p_value": p_value, "statistic": statistic}
```

### Model Monitoring Dashboard

```
Metric                   | Alert When
-------------------------|---------------------------
Prediction distribution  | KL divergence > 0.1 from baseline
Feature drift (PSI)      | Population Stability Index > 0.25
Model staleness          | > 30 days since last retrain
Accuracy degradation     | Online accuracy drops > 5% vs baseline
Inference latency        | P95 > 100ms (real-time) or SLA breach
Data quality             | Missing values > 5% in production features
```

### Drift Types

| Drift Type | Definition | Detection Method |
|-----------|-----------|-----------------|
| Data Drift | P(X) changes — input distribution shifts | PSI, KS test, Jensen-Shannon divergence |
| Concept Drift | P(Y|X) changes — relationship changes | Monitor prediction accuracy over time |
| Label Drift | P(Y) changes — target distribution shifts | Compare P(Y) over time windows |
| Prediction Drift | Model outputs shift | Compare prediction distribution |

### Retraining Triggers

```
Schedule-based: Retrain weekly/monthly regardless of performance
Performance-based: Retrain when accuracy drops below threshold
Data-volume-based: Retrain when N new labeled examples accumulate
Drift-based: Retrain when PSI > 0.25 or KL divergence > 0.1
Hybrid (recommended): Schedule + drift-based trigger
```

This ML workflow guide implements the data-scientist skill's full lifecycle — from problem framing through production monitoring — ensuring models are built systematically, tracked rigorously, and monitored continuously for drift and degradation.
