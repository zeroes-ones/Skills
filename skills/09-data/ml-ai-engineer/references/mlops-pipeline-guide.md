---
name: mlops-pipeline-guide
description: Deep-dive on MLOps pipelines: feature stores, experiment tracking, model registry, CI/CD for ML, A/B testing, and shadow deployment.
author: Sandeep Kumar Penchala
---

# MLOps Pipeline Guide

Production ML infrastructure from feature store to continuous delivery. Not theory — concrete
patterns, tool configurations, and operational practices that work at scale.

## 1. Feature Store Architecture

### 1.1 Why Feature Stores Exist

The core problem: features computed offline for training must be IDENTICAL to features computed
online for inference. Without a feature store, teams inevitably duplicate logic in training
pipelines and serving code, creating training-serving skew — the #1 cause of silent model degradation.

### 1.2 Core Components

```
┌──────────────────────────────────────────────────────┐
│                  Feature Registry                     │
│  (metadata: feature definitions, owners, SLAs, docs)  │
└──────────┬───────────────────────┬───────────────────┘
           │                       │
┌──────────▼──────────┐   ┌────────▼──────────────────┐
│   Offline Store      │   │    Online Store            │
│   (Data Warehouse,   │   │    (Redis, DynamoDB,       │
│    Parquet, Delta)   │   │     Cassandra, Bigtable)   │
│                      │   │                            │
│  • Batch, high-vol   │   │  • <10ms P99 latency       │
│  • Historical values │   │  • Latest values only      │
│  • Point-in-time     │   │  • High availability       │
│  • Used for training │   │  • Used for inference      │
└──────────────────────┘   └────────────────────────────┘
```

### 1.3 Point-in-Time Correct Joins

The hardest problem in feature engineering: when you train a model, you need feature values
AS THEY WERE at the time of the label, not as they are now.

**Example of what goes wrong:**
- User placed order on Jan 15 (label event)
- You compute "user_total_orders_last_30_days" using current data
- On Jan 15, they had 3 orders; today they have 7
- Your model trains on the wrong feature value — learns an impossible relationship

**Fix:** Timestamp each feature value. When joining features to labels, use `as_of_time` =
label timestamp. Feast and Tecton handle this automatically.

### 1.4 Feature Engineering Patterns

**Batch features (pre-computed, stored in offline store):**
- Aggregations over time windows: `avg_order_value_7d`, `login_count_30d`
- Embeddings: user embedding, item embedding, content embedding
- Text features: TF-IDF vectors, sentiment scores, entity extraction results

**Real-time features (computed on-the-fly for inference):**
- Current session context: items in cart, page currently viewing, time on site
- Device/geo: IP → geolocation, browser, OS, screen size
- Fresh features from event stream: "purchase made in last 5 minutes"

**Streaming features (Kafka → feature store):**
- Flink/Kafka Streams compute windowed aggregations and push to online store
- Sub-second freshness for features that change rapidly (bidding, fraud detection)

### 1.5 Feature Validation

Every feature pipeline should validate:
- Schema: expected dtypes, no unexpected columns
- Completeness: null rate < threshold (e.g., <5%)
- Range: values within expected bounds (negative age? impossible)
- Distribution: KS test vs previous run; alert if drift > threshold
- Freshness: `MAX(timestamp)` is within expected window

Tools: Great Expectations, TFX Data Validation, Deeque (Spark)

## 2. Experiment Tracking

### 2.1 What Must Be Logged

| Category          | Fields                                                                 |
|-------------------|------------------------------------------------------------------------|
| Code              | git commit hash, branch, diff (optional), entry point script            |
| Data              | dataset version/hash, split configuration, preprocessing params        |
| Model             | architecture, hyperparameters, random seeds, framework version         |
| Training          | loss curves (per-epoch), learning rate schedule, training duration     |
| Evaluation        | all metrics per split, confusion matrix, calibration plot              |
| Environment        | requirements.txt or conda-lock.yml, Docker image tag, hardware specs  |
| Artifacts         | model checkpoint, feature importance plot, SHAP summary plot           |

### 2.2 MLflow Project Structure

```python
import mlflow

mlflow.set_experiment("customer-churn-v2")

with mlflow.start_run(run_name="xgboost_baseline_2024-07-21"):
    # Log parameters
    mlflow.log_params({
        "model_type": "xgboost",
        "max_depth": 6,
        "learning_rate": 0.1,
        "n_estimators": 200,
        "subsample": 0.8,
    })

    # Log metrics
    mlflow.log_metrics({
        "val_accuracy": 0.873,
        "val_precision": 0.821,
        "val_recall": 0.794,
        "val_f1": 0.807,
        "val_roc_auc": 0.912,
    })

    # Log tags
    mlflow.set_tags({
        "git_commit": "a1b2c3d",
        "dataset_version": "v3.2",
        "status": "baseline",
    })

    # Log model
    mlflow.xgboost.log_model(model, "model")

    # Log artifacts
    mlflow.log_artifact("confusion_matrix.png")
    mlflow.log_artifact("feature_importance.csv")
```

### 2.3 Experiment Organization

```
Experiments/
├── customer-churn-v2/
│   ├── Run: xgboost_baseline_2024-07-21 [tags: baseline, v3.2]
│   ├── Run: xgboost_tuned_2024-07-22 [tags: tuned, v3.2, best_candidate]
│   └── Run: lightgbm_baseline_2024-07-23 [tags: baseline, lightgbm]
├── fraud-detection-v1/
└── recommendation-ranking-v3/
```

**Naming conventions:**
- Experiment name: `{problem_name}-v{version}`
- Run name: `{model}_{description}_{YYYY-MM-DD}`
- Always use semantic names, not UUIDs

## 3. Model Registry

### 3.1 Lifecycle Management

```
staging ──(eval gate)──▶ production ──(time)──▶ archived
   ▲                        │
   └──(rollback)────────────┘
```

**Promotion gates:**
1. Offline metrics pass thresholds (defined in experiment config)
2. Slice-based eval: no slice worse than X% below overall
3. Fairness metrics within acceptable bounds
4. Canary/shadow deployment metrics match or exceed production
5. Model owner approval (for high-risk models)

**Registry metadata per model version:**
- Training dataset reference (version, hash, date range)
- Evaluation report link
- Deployment config (instance type, autoscaling, batch size)
- Known limitations and caveats
- Rollback instructions

### 3.2 Multi-Model Registry with MLflow

```bash
# Register a model
mlflow models register-model -m "runs:/abc123/model" --name "churn_predictor"

# Transition to staging
mlflow models transition-stage --name "churn_predictor" --version 3 --stage "staging"

# Add description
mlflow models update-model-version --name "churn_predictor" --version 3 \
  --description "XGBoost with hyperparameter tuning. +3% F1 vs v2."

# Promote to production
mlflow models transition-stage --name "churn_predictor" --version 3 --stage "production"

# Archive old version
mlflow models transition-stage --name "churn_predictor" --version 2 --stage "archived"
```

## 4. CI/CD for ML

### 4.1 The ML CI/CD Pipeline

```
      ┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
      │ Data     │    │ Feature   │    │ Model     │    │ Model    │
Push  │ Validation│───▶│ Pipeline  │───▶│ Training  │───▶│ Eval     │
      └─────────┘    └──────────┘    └──────────┘    └─────┬────┘
                                                            │
                      ┌──────────┐    ┌──────────┐    ┌────▼─────┐
                      │ Monitor  │◀───│ Canary    │◀───│ Registry │
                      │ (ongoing)│    │ Deploy    │    │  Stage   │
                      └──────────┘    └──────────┘    └──────────┘
```

### 4.2 Pipeline Implementation (GitHub Actions Example)

```yaml
name: ML Training Pipeline
on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly retrain on Mondays
  workflow_dispatch:      # Manual trigger
  push:
    paths:
      - 'ml/**'
      - 'features/**'

jobs:
  data-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate Data
        run: |
          great_expectations checkpoint run data_quality_check

  train:
    needs: data-validation
    runs-on: [self-hosted, gpu]
    steps:
      - uses: actions/checkout@v4
      - name: Train Model
        run: |
          python train.py \
            --experiment-name churn-v3 \
            --data-version ${{ github.sha }} \
            --log-to-mlflow

  evaluate:
    needs: train
    runs-on: ubuntu-latest
    steps:
      - name: Evaluate Model
        run: |
          python evaluate.py \
            --run-id ${{ needs.train.outputs.run_id }} \
            --threshold-accuracy 0.85
      - name: Check Fairness
        run: |
          python evaluate_fairness.py \
            --run-id ${{ needs.train.outputs.run_id }}

  register:
    needs: evaluate
    if: success()
    runs-on: ubuntu-latest
    steps:
      - name: Register Model
        run: |
          python register_model.py \
            --run-id ${{ needs.train.outputs.run_id }} \
            --stage staging

  deploy-canary:
    needs: register
    runs-on: ubuntu-latest
    steps:
      - name: Deploy Canary (10% traffic)
        run: |
          python deploy_canary.py \
            --model-version ${{ needs.register.outputs.model_version }} \
            --traffic-percent 10

  monitor-canary:
    needs: deploy-canary
    runs-on: ubuntu-latest
    steps:
      - name: Monitor Canary (wait 4 hours)
        run: |
          python monitor_canary.py \
            --model-version ${{ needs.register.outputs.model_version }} \
            --duration-hours 4

  promote:
    needs: monitor-canary
    if: success()
    runs-on: ubuntu-latest
    steps:
      - name: Promote to Production
        run: |
          python promote_model.py \
            --model-version ${{ needs.register.outputs.model_version }}
```

## 5. Model Deployment Strategies

### 5.1 Shadow Deployment

New model receives a COPY of production traffic; predictions are logged but NOT shown to users.
Compare metrics offline before exposing to users. Zero risk, but requires double infrastructure.

**When to use:** first deployment, high-risk models, no rollback infrastructure yet.

### 5.2 Canary Deployment

Route X% of production traffic to new model; compare metrics (latency, error rate, business
metrics) against old model. Ramp 5% → 25% → 100% if metrics pass at each step.

**Infrastructure:** load balancer or service mesh with traffic splitting (Istio, Linkerd, Envoy).

**Canary duration by risk level:**
- Low risk (cosmetic model): 1–4 hours at each step
- Medium risk (user-facing, non-critical): 4–24 hours
- High risk (financial, health, safety): 24–72 hours minimum

### 5.3 A/B Testing Models

Both models serve real users with randomized assignment. Measure business metric (conversion,
retention, revenue) over the experiment period. Statistical test to determine winner.

**Differences from canary:**
- Canary: compares model-level metrics (latency, errors); technical health check
- A/B: compares business metrics (revenue, engagement); product decision

**Implementation with feature flags:**
```python
# User assignment (consistent per user)
def get_model_version(user_id):
    bucket = hash(user_id) % 100
    if bucket < 10:    return "new_model"    # 10% treatment
    else:              return "production"    # 90% control
```

### 5.4 Multi-Armed Bandit

Dynamically adjust traffic allocation based on real-time performance. Models that perform better
get more traffic automatically. Maximizes reward while minimizing regret.

Tools: AWS Personalize automatically uses bandit; custom with Thompson sampling or UCB.

### 5.5 Rollback Strategy

**Automatic rollback triggers:**
- Error rate > 2× baseline for >5 minutes
- P99 latency > 3× baseline
- Model output distribution completely outside expected range (all predictions = same class)
- Business metric drops below threshold in A/B test

**Rollback procedure:**
1. Route 100% traffic to previous model version (load balancer or feature flag)
2. Stop new model's inference pods (but keep them for investigation)
3. Create incident ticket with model version, time, trigger reason
4. Postmortem: what went wrong? Fix eval, fix monitoring, fix process

## 6. Pipeline Orchestration

### 6.1 Orchestrator Selection

| Tool       | Best For                                                | Key Feature                           |
|------------|---------------------------------------------------------|---------------------------------------|
| Airflow    | Complex DAGs, rich ecosystem, on-prem + cloud           | Python DAGs, extensive operators      |
| Dagster    | Asset-based thinking, data-aware scheduling             | Software-defined assets, I/O managers |
| Prefect    | Dynamic workflows, Python-native, easy to adopt         | Pythonic, great UI, cloud-managed      |
| Kubeflow   | Kubernetes-native ML pipelines                          | Native to K8s, notebook integration    |
| Metaflow   | Data science workflows, AWS-native                      | Built-in data versioning, step functions|

### 6.2 Pipeline Patterns

**Retraining triggers:**
- **Scheduled**: weekly/daily retrain regardless of drift
- **Data-driven**: retrain when new data volume exceeds threshold or drift detected
- **Performance-driven**: retrain when model performance degrades below threshold
- **Code-driven**: retrain when model code or feature definitions change

**Recommended:** Combine scheduled (safety net) + drift-triggered (responsiveness).

## 7. Infrastructure

### 7.1 Training Infrastructure

| Workload        | Recommended Instance       | Notes                                  |
|-----------------|----------------------------|----------------------------------------|
| Tabular ML      | CPU, 8–16 vCPUs, 32GB RAM | XGBoost/LightGBM scale well on CPU     |
| Fine-tune BERT  | GPU: T4 or A10G, 24GB VRAM | 1 GPU sufficient for <1M examples      |
| Fine-tune 7B LLM| GPU: A100 40GB or 2×A10G   | QLoRA on single A10G for 7B            |
| Fine-tune 70B LLM| GPU: 2×A100 80GB or 4×A10G| QLoRA on 2×A100 80GB                   |
| Train from scratch| GPU cluster (8+A100s)    | Distributed: FSDP, DeepSpeed ZeRO-3     |

**Cost optimization:**
- Use spot/preemptible instances: 60–80% cheaper; checkpoint frequently
- Mixed precision (FP16/BF16): 2× faster, half the memory
- Gradient checkpointing: trade 20% slower for 50% less memory
- Gradient accumulation: effective batch size > GPU memory limit

### 7.2 Serving Infrastructure

**Latency targets:**
- Real-time user-facing: P99 < 200ms
- Asynchronous (recommendations feed): P99 < 1s
- Batch (nightly scoring): P99 < time window (e.g., 4 hours)

**Scaling:**
- Horizontal: add more pods; load balancer distributes
- Vertical: bigger instances with more CPUs/GPUs
- GPU sharing: NVIDIA MIG, MPS, or vLLM with multiple model instances on one GPU

## References

- MLflow: https://mlflow.org/
- Feast: https://docs.feast.dev/
- Tecton: https://docs.tecton.ai/
- Weights & Biases: https://docs.wandb.ai/
- Great Expectations: https://docs.greatexpectations.io/
- NVIDIA Triton: https://docs.nvidia.com/deeplearning/triton-inference-server/
- vLLM: https://docs.vllm.ai/
