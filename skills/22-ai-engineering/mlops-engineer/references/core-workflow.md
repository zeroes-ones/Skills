# Core Workflow — Full Implementation

<!-- STANDARD: 3min -->

### Phase 1 (~30 min): Model Deployment Patterns

#### Real-Time Inference

1. **NVIDIA Triton Inference Server** — multi-framework, multi-model serving:
   - Dynamic batching: accumulates requests into optimal batch sizes for GPU throughput
   - Concurrent model execution: run multiple models on same GPU
   - Model ensembles: chain models (preprocessing → inference → postprocessing) as a pipeline
   - **Best for**: heterogeneous model serving, GPU-intensive workloads, NVIDIA ecosystem

2. **vLLM** — optimized for LLM serving:
   - PagedAttention: manages KV cache in non-contiguous memory blocks, reducing waste
   - Continuous batching: dynamically adds/removes requests from running batches
   - **Throughput**: 10–20× higher than vanilla Hugging Face Transformers serving
   - **Best for**: LLM inference at scale, OpenAI-compatible API

3. **Ray Serve** — general-purpose model serving on Ray:
   - Python-native, supports arbitrary Python code in serving pipeline
   - Autoscaling per-deployment with configurable min/max replicas
   - **Best for**: complex serving logic, multi-model orchestration, Python-heavy workflows

#### Batch Inference

- **Use case**: nightly scoring, backfills, report generation
- **Frameworks**: Spark ML, Ray Data, SageMaker Batch Transform
- **Pattern**: read from data lake → preprocess → inference → write predictions back
- **Cost optimization**: use spot/preemptible instances; batch inference is fault-tolerant

#### Edge Deployment

- **ONNX Runtime**: cross-platform inference, optimized for CPU/edge, model quantization support
- **TensorFlow Lite**: mobile and IoT, 8-bit quantization, hardware acceleration delegates
- **Core ML (Apple)**: iOS/macOS, hardware-optimized, model encryption
- **Key consideration**: model size vs accuracy tradeoff; quantize aggressively for edge

#### Deployment Strategy Selection Matrix

| Requirement | Recommended Framework | Why |
|-------------|----------------------|-----|
| LLM serving, high throughput | vLLM | PagedAttention, continuous batching |
| Multi-model, GPU optimized | Triton | Model ensembles, dynamic batching |
| Complex Python pipelines | Ray Serve | Python-native, flexible orchestration |
| Edge/mobile | ONNX Runtime / TFLite | Cross-platform, quantized, small footprint |
| Simple API, low traffic (<10 QPS) | FastAPI + Transformers | Simple, well-understood, easy to debug |

### Phase 2 (~30 min): Monitoring and Observability

#### Prediction Drift Detection

1. **Population Stability Index (PSI)** — measures distribution shift between reference and production:
   - PSI < 0.1: no significant drift
   - PSI 0.1–0.2: moderate drift (investigate)
   - PSI > 0.2: significant drift (alert, consider retraining)
   - **Formula**: PSI = Σ (P_prod − P_ref) × ln(P_prod / P_ref) across bins

2. **Kolmogorov-Smirnov (KS) test** — statistical test for distribution drift:
   - Non-parametric, works on continuous and discrete features
   - KS statistic: maximum difference between CDFs of reference and production
   - Threshold: reject null hypothesis (no drift) at p < 0.01

3. **Monitoring dimensions:**
   - **Prediction drift**: shift in model output distribution (classification probabilities, regression values)
   - **Feature drift**: shift in input feature distributions (individual features, joint distributions)
   - **Data quality**: schema violations, missing values, out-of-range values, type mismatches
   - **Performance degradation**: if ground truth labels arrive later (delayed feedback), track accuracy/F1 over time

#### Monitoring Dashboard Requirements

```
┌────────────────────────────────────────────────────────┐
│ Model Monitoring Dashboard                              │
├──────────────┬──────────────┬───────────────────────────┤
│ Metric        │ Current       │ Trend (7d)               │
├──────────────┼──────────────┼───────────────────────────┤
│ Prediction PSI│ 0.08          │ ─→ stable                │
│ Feature PSI   │ 0.15 ⚠️       │ ↗ rising (feature_3)     │
│ Data quality  │ 99.7%         │ ─→ stable                │
│ Latency p99   │ 120ms         │ ↘ improving              │
│ Error rate    │ 0.02%         │ ─→ stable                │
│ Throughput    │ 450 QPS       │ ↗ rising (organic)       │
└──────────────┴──────────────┴───────────────────────────┘
```

#### Alert Thresholds

- **Critical**: PSI > 0.2, error rate > 1%, latency p99 > SLA → page on-call
- **Warning**: PSI 0.1–0.2, missing values > 5%, throughput anomaly → Slack notification
- **Info**: new feature values observed, schema drift, model age > 30 days → weekly report

### Phase 3 (~25 min): Retraining Pipelines

#### Trigger Strategies

1. **Schedule-based**: retrain weekly/daily/hourly regardless of performance
   - Simplest, predictable compute cost
   - **Risk**: retrains unnecessarily, may miss sudden drift between retrains

2. **Performance-based**: trigger retraining when monitored metric degrades below threshold
   - Efficient, only retrains when needed
   - **Risk**: requires ground truth labels with low latency; delayed feedback breaks this

3. **Data-volume-based**: retrain after N new training examples accumulated
   - Good for cold-start, expanding coverage
   - **Risk**: doesn't account for data quality of new examples

4. **Hybrid**: schedule-based as safety net + performance-based as primary trigger
   - **Recommendation**: most production systems should use hybrid

#### A/B Testing for Model Updates

```
┌─────────────────────────────────────────────────────────┐
│ Model Update A/B Testing Protocol                        │
├─────────────────────────────────────────────────────────┤
│ Phase 1: Shadow (0% traffic, evaluation only)            │
│   └── Deploy new model, log predictions, compare offline  │
│ Phase 2: Canary (5% traffic, 24 hours)                   │
│   └── Monitor: predictions, latency, error rate, drift    │
│ Phase 3: Ramp (25% → 50% → 100%)                         │
│   └── 12 hours at each step, monitor at each transition   │
│ Phase 4: Full rollout (100% traffic)                     │
│   └── Keep old model warm for 48 hours for rollback       │
│ Rollback trigger: any critical metric degrades >5%        │
└─────────────────────────────────────────────────────────┘
```

### Phase 4 (~25 min): Feature Stores

#### Feast Architecture

```yaml
# feature_store.yaml
project: patient_risk
registry: gs://bucket/registry.db
provider: gcp
offline_store:
  type: bigquery
online_store:
  type: redis
  connection_string: redis://...

# Feature definition
from feast import FeatureView, Field, Entity
from feast.types import Float32

patient = Entity(name="patient_id", join_keys=["patient_id"])
patient_features = FeatureView(
    name="patient_features",
    entities=[patient],
    schema=[Field(name="age_normalized", dtype=Float32),
            Field(name="prior_admissions_30d", dtype=Float32)],
    source=BigQuerySource(table="features.patient_daily"),
    ttl=timedelta(days=30)
)
```

#### Point-in-Time Correctness

- **Problem**: training uses features from time T, serving uses features from time "now" — if you join wrong, you leak future information into training
- **Solution**: feature store joins features AS OF event timestamp, ensuring training data doesn't contain future information
- **Feast/Teeton**: `get_historical_features(entity_df, features, full_feature_names=True)` — time-travel queries

#### Offline vs Online Serving

| Aspect | Offline | Online |
|--------|---------|--------|
| Purpose | Training data generation | Real-time inference |
| Latency | Minutes to hours | <10ms |
| Storage | Data warehouse / lake | Redis / DynamoDB / Cassandra |
| Freshness | Daily / hourly batch | Real-time streaming |
| Consistency | Eventual | Point-in-time at request |

### Phase 5 (~25 min): Experiment Tracking

#### MLflow

```python
import mlflow

mlflow.set_experiment("patient-readmission-v2")
with mlflow.start_run(run_name="xgboost-baseline"):
    # Log parameters
    mlflow.log_params({"max_depth": 6, "learning_rate": 0.01})
    # Log metrics
    mlflow.log_metrics({"auc": 0.84, "f1": 0.79})
    # Log model with signature
    mlflow.xgboost.log_model(model, "model",
        signature=infer_signature(X_train, model.predict(X_train)))
    # Log artifacts
    mlflow.log_artifact("confusion_matrix.png")
```

#### Model Registry

- **Stages**: None → Staging → Production → Archived
- **Stage transitions require**: automated tests pass (CI gate), manual approval (for Production), performance above threshold
- **Lineage**: every model in registry has git commit, training data version, hyperparameters, metrics, and environment snapshot

#### Weights & Biases

- **Advantages over MLflow**: better collaboration UI, built-in hyperparameter sweeps, integrated artifacts and reports
- **When to use W&B**: research-heavy teams, hyperparameter optimization, need rich visualization
- **When to use MLflow**: self-hosted requirement, tight integration with Databricks, simpler setup

### Phase 6 (~25 min): CI/CD for ML

#### Pipeline Stages

```
┌──────────┐    ┌───────────┐    ┌──────────┐    ┌────────────┐    ┌───────────┐
│  Data    │───→│  Training  │───→│   Eval    │───→│  Register   │───→│   Deploy   │
│ Validation│   │           │    │           │    │            │    │           │
└──────────┘    └───────────┘    └──────────┘    └────────────┘    └───────────┘
     │               │                │                │                │
     ▼               ▼                ▼                ▼                ▼
  Schema         Experiment       Metrics >        Stage =          Canary
  validation     tracked          baseline         Staging          5%→100%
```

#### Model Validation Gates

- **Data validation**: schema check, statistical profile comparison, data quality tests
- **Training validation**: no NaN loss, convergence within expected steps, no overfitting (train/val gap <5%)
- **Evaluation validation**: primary metric above threshold, all slice metrics above threshold, fairness metrics within bounds
- **Infrastructure validation**: model loads in serving container, latency at target QPS within SLA, memory within limits

#### Canary and Rollback

- **Canary deployment**: deploy new model alongside old, route % traffic via feature flag
- **Shadow mode**: send traffic to new model but only log predictions (no user impact)
- **Rollback**: if critical metric degrades, revert to previous model version within 5 minutes
- **Blue-green**: maintain two identical environments; swap traffic instantly

### Phase 7 (~25 min): Infrastructure

#### GPU Optimization

1. **Mixed precision (FP16/BF16)**: 2× throughput, half memory; BF16 preferred for training stability
2. **Model parallelism**: split model across GPUs (tensor parallelism, pipeline parallelism)
3. **FlashAttention**: memory-efficient attention; 2–4× faster, uses less VRAM
4. **KV cache optimization**: PagedAttention (vLLM), GQA (Grouped Query Attention)
5. **Continuous batching**: dynamically add/remove from batches; 10× throughput improvement for LLMs

#### Autoscaling

- **HPA (Horizontal Pod Autoscaler)**: scale based on CPU/memory or custom metrics (request queue depth)
- **KEDA**: event-driven autoscaling for Kafka/Redis queue depth
- **Cold start mitigation**: keep minimum replicas ≥1; pre-warm models on startup; use provisioned concurrency

#### Cold Start Mitigation

- **Model pre-warming**: send dummy inference request on startup to load model into GPU memory
- **Keep-alive pools**: maintain pool of warm containers; scale ahead of demand based on time-of-day patterns
- **Model caching**: cache model weights on local SSD; reduce download time from minutes to seconds

### Phase 8 (~20 min): Data Versioning

#### DVC (Data Version Control)

```bash
# Track data alongside code
dvc add data/training_data.csv
git add data/training_data.csv.dvc
git commit -m "Add training dataset v1.2"

# Remote storage
dvc remote add -d storage s3://my-bucket/dvc-store
dvc push

# Reproduce pipeline
dvc repro  # runs pipeline stages and caches intermediate results
```

#### lakeFS

- Git-like operations on data lakes: branch, commit, merge, revert
- **Use case**: create branch for model experiment, run on consistent data snapshot, merge if successful
- **Zero-copy branching**: branches don't duplicate data, only metadata

### Phase 9 (~20 min): Cost Optimization

#### Spot/Preemptible Instances

- **Training**: use spot instances for distributed training with checkpointing (resume if interrupted)
- **Batch inference**: spot instances ideal — fault-tolerant, stateless, interruptible
- **Production inference**: avoid spot for latency-sensitive serving; use reserved/committed use discounts

#### Model Compilation

- **ONNX Runtime**: compile PyTorch/TF models to optimized format; 2–5× inference speedup on CPU
- **TensorRT**: NVIDIA's optimizer; 2–3× throughput improvement on GPU
- **OpenVINO**: Intel CPU/VPU optimization; good for edge and CPU inference

#### Token Caching for LLMs

- **KV cache sharing**: reuse KV cache across requests with shared prefixes (system prompts)
- **Speculative decoding**: small draft model generates candidates, large model verifies; 2–3× throughput
- **Prompt caching (Anthropic)**: cache long prompts; 90% cost reduction on cache hits
