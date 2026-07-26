# mlops-pipeline

Reference documentation for the automation-engineer skill — end-to-end MLOps automation: data validation, feature stores, experiment tracking, training pipelines, hyperparameter tuning, model evaluation, model registry, serving, canary deployments, model monitoring, orchestration, and CI/CD for ML.

## Data Validation

### Great Expectations

Expectation suites define data quality contracts, data docs render validation results, and CI integration gates pipelines on suite passes.

```yaml
# great_expectations.yml — project config
expectations_store_name: expectations_store
validations_store_name: validations_store
data_docs_sites:
  local_site:
    class_name: SiteBuilder
    store_backend:
      class_name: TupleFilesystemStoreBackend
      base_directory: uncommitted/data_docs/local_site/
```

```python
# Define an Expectation Suite programmatically
import great_expectations as gx

context = gx.get_context()
validator = context.sources.pandas_default.read_csv("data/training.csv")

validator.expect_column_values_to_not_be_null("customer_id")
validator.expect_column_values_to_be_between("age", min_value=0, max_value=120)
validator.expect_column_distinct_values_to_be_in_set(
    "status", value_set=["active", "inactive", "churned"]
)
validator.expect_column_kl_divergence_to_be_less_than(
    "prediction_score", partition_object=None, threshold=0.1
)

validator.save_expectation_suite(
    expectation_suite_name="production_training_suite",
    discard_failed_expectations=False,
)
```

```bash
# Run validation checkpoint from CI
great_expectations checkpoint run training_data_checkpoint
```

### TensorFlow Data Validation (TFDV)

Schema inference from existing data, drift detection between training/serving splits, and skew detection across environments.

```python
import tensorflow_data_validation as tfdv

# Infer schema from training data
train_stats = tfdv.generate_statistics_from_csv("data/train.csv")
schema = tfdv.infer_schema(train_stats)
tfdv.write_schema_text(schema, "schema.pbtxt")

# Compare serving data against baseline
serving_stats = tfdv.generate_statistics_from_csv("data/serving_sample.csv")
drift_anomalies = tfdv.validate_statistics(
    statistics=serving_stats,
    schema=schema,
    serving_statistics=train_stats,
    environment="SERVING",
)
tfdv.display_anomalies(drift_anomalies)

# Numeric drift: Jensen-Shannon divergence > 0.1 triggers alert
# Categorical drift: L-infinity distance between distributions
```

## Feature Store

### Feast (Open Source)

Online serving at <10ms latency, offline training dataset retrieval via point-in-time joins, and feature freshness monitoring.

```yaml
# feature_store.yaml
project: customer_churn
registry: gs://my-bucket/registry.db
provider: gcp
online_store:
  type: datastore
offline_store:
  type: bigquery
entity_key_serialization_version: 2
```

```python
# Define a feature view
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64
from datetime import timedelta

customer = Entity(name="customer", join_keys=["customer_id"])

customer_stats_source = FileSource(
    path="gs://my-bucket/customer_stats.parquet",
    timestamp_field="event_timestamp",
)

customer_stats_fv = FeatureView(
    name="customer_stats",
    entities=[customer],
    ttl=timedelta(days=30),
    schema=[
        Field(name="total_orders_90d", dtype=Int64),
        Field(name="avg_order_value_90d", dtype=Float32),
    ],
    source=customer_stats_source,
)

# Fetch online features (sub-10ms)
from feast import FeatureStore
store = FeatureStore(repo_path=".")
feature_vector = store.get_online_features(
    features=["customer_stats:total_orders_90d", "customer_stats:avg_order_value_90d"],
    entity_rows=[{"customer_id": 1001}, {"customer_id": 1002}],
).to_dict()

# Fetch historical features for training with point-in-time correctness
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=["customer_stats:total_orders_90d"],
).to_df()
```

```bash
feast apply                    # deploy feature views
feast materialize 2026-01-01T00:00:00 2026-07-01T00:00:00  # backfill
```

### Tecton (Managed)

Streaming features with sub-second freshness, managed infrastructure, and declarative feature definitions.

```python
from tecton import Entity, FeatureService, batch_feature_view, stream_feature_view
from tecton.types import Float64, Timestamp, String

@stream_feature_view(
    source=KafkaSource(topic="transactions"),
    entities=[Entity(name="user", join_keys=["user_id"])],
    schema=[Field("txn_count_5m", Float64)],
    ttl="5m",
    online=True,
    offline=True,
)
def user_txn_count_5m(transactions):
    return transactions.groupby("user_id").agg(txn_count_5m=F.count("*"))
```

## Experiment Tracking

### MLflow Tracking

```bash
mlflow server \
  --backend-store-uri postgresql://user:pass@host/mlflow \
  --default-artifact-root s3://mlflow-artifacts \
  --host 0.0.0.0 --port 5000
```

```python
import mlflow

mlflow.set_tracking_uri("http://mlflow-server:5000")
mlflow.set_experiment("churn-prediction-v2")

with mlflow.start_run(run_name="xgboost-baseline"):
    mlflow.log_params({"max_depth": 6, "learning_rate": 0.1, "n_estimators": 200})
    mlflow.log_metrics({"accuracy": 0.89, "f1": 0.85, "roc_auc": 0.93})
    mlflow.log_artifact("confusion_matrix.png")
    mlflow.sklearn.log_model(model, "model")
```

```python
# Search and compare runs
runs = mlflow.search_runs(
    experiment_ids=["1"],
    filter_string="metrics.f1 > 0.8 and params.learning_rate < 0.2",
    order_by=["metrics.f1 DESC"],
)
```

### Weights & Biases

```python
import wandb

wandb.init(project="churn-prediction", config={"lr": 0.01, "epochs": 50})

for epoch in range(wandb.config["epochs"]):
    loss = train_one_epoch()
    wandb.log({"loss": loss, "epoch": epoch, "lr": scheduler.get_last_lr()[0]})

wandb.log_artifact("model.onnx", type="model")
wandb.finish()
```

## Model Training Pipelines

### Kubeflow Pipelines (KFP v2)

```python
from kfp import dsl, compiler

@dsl.component(packages_to_install=["pandas", "scikit-learn"])
def validate_data(input_csv: str) -> str:
    import pandas as pd
    df = pd.read_csv(input_csv)
    assert df.isnull().sum().sum() == 0, "Null values detected"
    return input_csv

@dsl.component(packages_to_install=["scikit-learn", "mlflow"])
def train_model(data_path: str, max_depth: int) -> dsl.Model:
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(max_depth=max_depth)
    # ... training logic
    return dsl.Model(uri="s3://models/churn-model", name="churn")

@dsl.pipeline(name="churn-training", description="Churn prediction pipeline")
def churn_pipeline(input_csv: str = "gs://data/training.csv"):
    validate_task = validate_data(input_csv=input_csv)
    train_task = train_model(data_path=validate_task.output, max_depth=10)
    train_task.after(validate_task)

compiler.Compiler().compile(churn_pipeline, "churn_pipeline.yaml")
```

### SageMaker Pipelines

```python
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.sklearn.processing import SKLearnProcessor

processor = SKLearnProcessor(
    framework_version="1.2-1", role=role, instance_type="ml.m5.xlarge", instance_count=1
)

processing_step = ProcessingStep(
    name="DataProcessing",
    processor=processor,
    inputs=[ProcessingInput(source="s3://bucket/raw/", destination="/opt/ml/processing/input")],
    outputs=[ProcessingOutput(source="/opt/ml/processing/output")],
    code="preprocessing.py",
)

pipeline = Pipeline(
    name="churn-pipeline",
    steps=[processing_step],
    sagemaker_session=sagemaker_session,
)
pipeline.upsert(role_arn=role)
execution = pipeline.start()
```

### MLflow Projects

```yaml
# MLproject
name: churn-training
conda_env: conda.yaml
entry_points:
  main:
    parameters:
      max_depth: {type: int, default: 10}
      lr: {type: float, default: 0.01}
    command: "python train.py --max-depth {max_depth} --lr {lr}"
```

```bash
mlflow run . -P max_depth=12 -P lr=0.05 --experiment-name churn-v3
mlflow run git@github.com:myorg/ml-project.git --version v2.0 --backend kubernetes
```

## Hyperparameter Tuning

### Optuna (Define-by-Run)

```python
import optuna

def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 50, 500),
        "max_depth": trial.suggest_int("max_depth", 3, 15),
        "learning_rate": trial.suggest_float("learning_rate", 1e-4, 1e-1, log=True),
        "subsample": trial.suggest_float("subsample", 0.5, 1.0),
    }
    score = cross_val_score(X_train, y_train, params)
    trial.report(score, step=0)
    if trial.should_prune():
        raise optuna.TrialPruned()
    return score

study = optuna.create_study(direction="maximize", pruner=optuna.pruners.MedianPruner())
study.optimize(objective, n_trials=100)
print(f"Best params: {study.best_params}")
print(f"Best value: {study.best_value}")
```

### Ray Tune

```python
from ray import tune, air
from ray.tune.schedulers import ASHAScheduler

tuner = tune.Tuner(
    train_fn,
    param_space={
        "lr": tune.loguniform(1e-4, 1e-1),
        "batch_size": tune.choice([32, 64, 128]),
        "layers": tune.randint(2, 6),
    },
    tune_config=tune.TuneConfig(
        num_samples=50,
        scheduler=ASHAScheduler(max_t=100, grace_period=10),
        metric="val_loss",
        mode="min",
    ),
)
results = tuner.fit()
```

## Model Evaluation

### Core Metrics and Baseline Gating

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def evaluate_model(model, X_test, y_test, baseline_metrics: dict) -> dict:
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
    }

    # Block deploy if ANY metric regresses below baseline
    for name, value in metrics.items():
        if value < baseline_metrics[name] - 0.02:  # 2% tolerance
            raise ValueError(f"Metric {name}: {value:.3f} below baseline {baseline_metrics[name]:.3f}")

    return metrics
```

### Fairness & Bias

```python
# Aequitas: bias audit
from aequitas import Audit
import pandas as pd

audit_df = pd.DataFrame({
    "score": y_proba, "label_value": y_test,
    "race": X_test["race"], "gender": X_test["gender"],
})
audit = Audit(audit_df)
audit.run()
audit.disparity_plot(attribute="race", metrics=["fpr", "fnr", "ppr"])

# Fairlearn: mitigate bias via threshold adjustment
from fairlearn.postprocessing import ThresholdOptimizer

adjuster = ThresholdOptimizer(
    estimator=model,
    constraints="equalized_odds",
    objective="balanced_accuracy_score",
)
adjuster.fit(X_train, y_train, sensitive_features=X_train["race"])
y_pred_adjusted = adjuster.predict(X_test, sensitive_features=X_test["race"])
```

## Model Registry

### MLflow Model Registry

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Register a model
model_uri = f"runs:/{run_id}/model"
result = client.create_model_version(name="churn-predictor", source=model_uri, run_id=run_id)

# Stage transitions with description
client.transition_model_version_stage(
    name="churn-predictor", version=result.version,
    stage="Staging", archive_existing_versions=False,
)

# Promote to production
client.transition_model_version_stage(
    name="churn-predictor", version=result.version,
    stage="Production", archive_existing_versions=True,
)
```

```python
# Webhook trigger on stage transition — POST to CI/CD pipeline
# MLflow UI → Model Registry → Settings → Webhooks
# Configure to POST to: https://ci.example.com/api/trigger-deploy
# Payload: {"model_name": "churn-predictor", "version": "3", "stage": "Production"}
```

### SageMaker Model Registry

```python
# Create model package group
sagemaker_client.create_model_package_group(
    ModelPackageGroupName="churn-predictor",
    ModelPackageGroupDescription="Churn prediction models",
)

# Register model version with approval workflow
model_package = sagemaker_client.create_model_package(
    ModelPackageGroupName="churn-predictor",
    ModelApprovalStatus="PendingManualApproval",
    InferenceSpecification={...},
)
# After review: sagemaker_client.update_model_package(ModelPackageArn=..., ModelApprovalStatus="Approved")
```

## Model Serving

### TensorFlow Serving

```bash
# REST API predict
curl -X POST http://localhost:8501/v1/models/churn:predict \
  -H "Content-Type: application/json" \
  -d '{"instances": [{"feature_a": 1.0, "feature_b": "active"}]}'

# gRPC predict
tensorflow_model_server --port=8500 --rest_api_port=8501 \
  --model_name=churn --model_base_path=/models/churn \
  --enable_batching=true --batching_parameters_file=batching_config.txt
```

```
# assets.extra/tf_serving_warmup_requests.txt — model warmup
# Warmup requests prevent cold-start latency on first prediction
requests {
  model_warmup {
    name: "warmup"
    batch_size: 16
    inputs {
      key: "feature_a"
      value { dtype: DT_FLOAT  tensor_shape { dim { size: 16 } } }
    }
  }
}
```

### Triton Inference Server

```protobuf
# config.pbtxt — model configuration
name: "churn_ensemble"
platform: "ensemble"
max_batch_size: 128
input [{ name: "features"  data_type: TYPE_FP32  dims: [20] }]
output [{ name: "prediction"  data_type: TYPE_FP32  dims: [1] }]
ensemble_scheduling {
  step [{ model_name: "preprocessing", model_version: 1, input_map { key: "raw" value: "features" } output_map { key: "processed" value: "processed_features" } }]
  step [{ model_name: "xgboost_model", model_version: 1, input_map { key: "input" value: "processed_features" } output_map { key: "output" value: "prediction" } }]
}
dynamic_batching { max_queue_delay_microseconds: 100 }
```

### BentoML

```python
import bentoml

@bentoml.service
class ChurnPredictor:
    @bentoml.on_startup
    def load_model(self):
        self.model = bentoml.sklearn.load_model("churn_model:latest")

    @bentoml.api
    def predict(self, features: np.ndarray) -> np.ndarray:
        return self.model.predict(features)
```

```bash
bentoml build                  # creates bentofile
bentoml containerize churn_predictor:latest  # Docker image
bentoml deploy --platform aws-sagemaker
```

### SageMaker Multi-Model Endpoints

```python
# Multi-model endpoint: one endpoint serves multiple models from S3
sagemaker_client.create_endpoint_config(
    EndpointConfigName="multi-model-churn",
    ProductionVariants=[{
        "VariantName": "AllTraffic", "ModelName": "churn-multi",
        "InstanceType": "ml.m5.xlarge", "InitialInstanceCount": 1,
    }],
)

# A/B testing with production variants
ProductionVariants=[
    {"VariantName": "variant-a", "ModelName": "churn-v3", "InitialVariantWeight": 90},
    {"VariantName": "variant-b", "ModelName": "churn-v4", "InitialVariantWeight": 10},
]
```

## Canary Model Deployment

### Traffic Splitting Strategy

```yaml
# Istio VirtualService — canary rollout
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: churn-model
spec:
  hosts: ["churn-predictor.default.svc.cluster.local"]
  http:
  - route:
    - destination:
        host: churn-v3
      weight: 95
    - destination:
        host: churn-v4
      weight: 5
```

```python
# Automated canary progression with metric guard
def canary_rollout(new_version: str):
    stages = [
        ("shadow", 0),     # Log predictions only, no response
        ("5%", 5), ("25%", 25), ("50%", 50), ("100%", 100),
    ]
    for stage_name, traffic_pct in stages:
        set_traffic_split(stable="churn-v3", canary=new_version, canary_pct=traffic_pct)
        monitor_metrics(window_minutes=10)
        if detect_regression(new_version):
            print(f"Rollback triggered at {stage_name}")
            set_traffic_split(stable="churn-v3", canary=new_version, canary_pct=0)
            raise Exception("Canary failed — rollback complete")
```

## Model Monitoring

### Data Drift Detection

```python
# Population Stability Index (PSI) — detect input distribution shift
import numpy as np
from scipy.stats import ks_2samp, wasserstein_distance

def compute_psi(expected, actual, bins=10):
    """PSI < 0.1: no drift; 0.1-0.25: moderate; > 0.25: significant drift."""
    breaks = np.linspace(0, 1, bins + 1)
    expected_ratio = np.histogram(expected, breaks)[0] / len(expected)
    actual_ratio = np.histogram(actual, breaks)[0] / len(actual)
    expected_ratio = np.clip(expected_ratio, 1e-10, None)
    actual_ratio = np.clip(actual_ratio, 1e-10, None)
    return np.sum((actual_ratio - expected_ratio) * np.log(actual_ratio / expected_ratio))

def detect_drift(reference_data, current_data, threshold=0.1):
    psi_value = compute_psi(reference_data, current_data)
    ks_stat, ks_pval = ks_2samp(reference_data, current_data)
    h_dist = wasserstein_distance(reference_data, current_data)

    return {
        "psi": psi_value,
        "ks_statistic": ks_stat,
        "ks_pvalue": ks_pval,
        "hellinger_distance": h_dist,
        "drift_detected": psi_value > threshold or ks_pval < 0.01,
    }
```

### Evidently AI

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset

report = Report(metrics=[DataDriftPreset(), TargetDriftPreset()])
report.run(reference_data=reference_df, current_data=current_df)
report.save_html("drift_report.html")

# Drift alert thresholds
# | Feature  | P-value | Drift Detected |
# |----------|---------|----------------|
# | age      | 0.85    | No             |
# | income   | 0.001   | Yes            |
```

### whylogs

```python
import whylogs as why

profile = why.log(current_df)
profile_view = profile.view()

# Compare against reference profile (uploaded to WhyLabs)
# whylogs monitors distribution, cardinality, missing values, type changes

results = why.log(current_df)
# Profile contains: counts, types, frequent items, cardinality, distribution metrics per column
```

## Pipeline Orchestration

### Airflow DAG

```python
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta

default_args = {"owner": "ml-team", "retries": 1, "retry_delay": timedelta(minutes=10)}

with DAG("churn_ml_pipeline", start_date=datetime(2026, 1, 1),
         schedule_interval="@weekly", catchup=False, default_args=default_args) as dag:

    # Sensor: wait for upstream data pipeline
    wait_for_data = ExternalTaskSensor(
        task_id="wait_for_data_pipeline",
        external_dag_id="etl_customer_features",
        external_task_id="export_features",
        timeout=3600,
    )

    validate = KubernetesPodOperator(
        task_id="validate_data", name="data-validation",
        image="gcr.io/myproject/ml-ops:latest",
        cmds=["python", "-m", "mlops.validate"],
    )

    train = KubernetesPodOperator(
        task_id="train_model", name="training",
        image="gcr.io/myproject/ml-ops:latest",
        cmds=["python", "-m", "mlops.train"],
    )

    wait_for_data >> validate >> train
```

### Prefect

```python
from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner

@task(retries=3, retry_delay_seconds=60)
def validate_data() -> bool:
    return run_great_expectations()

@task
def train_model(valid: bool) -> str:
    return mlflow_train()

@flow(task_runner=ConcurrentTaskRunner(), name="churn-pipeline")
def churn_ml_pipeline():
    valid = validate_data()
    model_uri = train_model(valid, wait_for=[valid])
    evaluate_model(model_uri, wait_for=[model_uri])
```

### Dagster

```python
from dagster import asset, AssetIn, Definitions, AssetExecutionContext

@asset
def raw_customer_data() -> pd.DataFrame:
    return pd.read_csv("s3://data/customers.csv")

@asset(ins={"raw": AssetIn("raw_customer_data")})
def validated_data(raw: pd.DataFrame) -> pd.DataFrame:
    assert raw["customer_id"].is_unique
    return raw

@asset(ins={"data": AssetIn("validated_data")})
def trained_model(data: pd.DataFrame) -> str:
    return train_and_log(data)

defs = Definitions(assets=[raw_customer_data, validated_data, trained_model])
```

## CI/CD for ML

### Pipeline Stages

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌───────────┐
│ Validate  │ → │  Train   │ → │ Evaluate │ → │ Registry │ → │   Deploy   │
│  Data     │    │  Model   │    │  Model   │    │  (Stage) │    │ (Staging)  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └─────┬─────┘
                                                                ┌─────▼─────┐
                                                                │ Integration│
                                                                │   Tests    │
                                                                └─────┬─────┘
                                                                ┌─────▼─────┐
                                                                │   Deploy   │
                                                                │(Production)│
                                                                └───────────┘
```

### GitHub Actions ML Workflow

```yaml
name: ML Training Pipeline

on:
  push:
    paths: ["src/**", "data/**", "config/**"]
  schedule:
    - cron: "0 2 * * 1"  # Weekly retrain Monday 2 AM
  workflow_dispatch:
    inputs:
      auto_deploy:
        description: "Auto-deploy to production"
        type: boolean
        default: false

env:
  MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
  AWS_REGION: us-east-1

jobs:
  data-validation:
    runs-on: ubuntu-latest
    outputs:
      validation_passed: ${{ steps.validate.outputs.passed }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install great-expectations pandas pyarrow
      - id: validate
        run: |
          great_expectations checkpoint run training_data_checkpoint
          echo "passed=true" >> "$GITHUB_OUTPUT"

  train:
    needs: data-validation
    if: needs.data-validation.outputs.validation_passed == 'true'
    runs-on: ubuntu-latest
    outputs:
      run_id: ${{ steps.train.outputs.run_id }}
      model_f1: ${{ steps.train.outputs.f1 }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt
      - id: train
        run: |
          python -m mlops.train --output-run-id-file run_id.txt
          echo "run_id=$(cat run_id.txt)" >> "$GITHUB_OUTPUT"
          echo "f1=0.87" >> "$GITHUB_OUTPUT"

  evaluate:
    needs: train
    runs-on: ubuntu-latest
    outputs:
      deploy_decision: ${{ steps.gate.outputs.deploy }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install mlflow scikit-learn evidently fairlearn
      - id: gate
        run: |
          python -m mlops.evaluate --run-id "${{ needs.train.outputs.run_id }}" --min-f1 0.85
          echo "deploy=true" >> "$GITHUB_OUTPUT"

  register-model:
    needs: evaluate
    if: needs.evaluate.outputs.deploy_decision == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install mlflow boto3
      - run: |
          python -m mlops.register \
            --run-id "${{ needs.train.outputs.run_id }}" \
            --model-name churn-predictor \
            --stage Staging

  deploy-staging:
    needs: register-model
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_DEPLOY_ROLE }}
          aws-region: ${{ env.AWS_REGION }}
      - run: |
          aws sagemaker update-endpoint \
            --endpoint-name churn-predictor-staging \
            --endpoint-config-name churn-config-staging-v${{ github.run_number }}

  integration-test:
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install requests
      - run: |
          python -m tests.integration \
            --endpoint https://staging.api.example.com/churn

  deploy-production:
    needs: integration-test
    if: inputs.auto_deploy == true
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_PROD_DEPLOY_ROLE }}
          aws-region: ${{ env.AWS_REGION }}
      - run: |
          aws sagemaker update-endpoint \
            --endpoint-name churn-predictor-prod \
            --endpoint-config-name churn-config-prod-v${{ github.run_number }}
      - name: Promote in registry
        run: |
          python -m mlops.promote \
            --model-name churn-predictor \
            --from-stage Staging --to-stage Production
```
