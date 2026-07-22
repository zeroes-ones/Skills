---
name: mlops-engineer
description: >-
  MLOps Engineer covering model deployment patterns (real-time inference with Triton/vLLM/Ray Serve, batch inference, edge deployment), monitoring and observability (prediction drift via PSI/KS test, feature drift, data quality monitoring, model performance degradation), retraining pipelines (trigger strategies, A/B testing for model updates), feature stores (Feast, Tecton, offline/online serving, point-in-time correctness), experiment tracking (MLflow, Weights & Biases, model registry, lineage tracking), CI/CD for ML (model validation gates, canary deployments, shadow mode, rollback strategies), infrastructure (GPU optimization, model serving frameworks, autoscaling, cold start mitigation), data versioning (DVC, lakeFS, reproducible training pipelines), and cost optimization (spot instances, model compilation, token caching). Triggered by MLOps, model deployment, model monitoring, feature store, experiment tracking, retraining, GPU optimization.
author: Sandeep Kumar Penchala
type: ai-engineering
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - mlops
  - model-deployment
  - model-monitoring
  - feature-store
  - experiment-tracking
  - retraining
  - gpu-optimization
token_budget: 5000
output:
  type: "code"
  path_hint: "./"
---
# MLOps Engineer

Production machine learning operations — from model deployment through continuous monitoring and automated retraining. Covers serving infrastructure (Triton, vLLM, Ray Serve), observability with drift detection (PSI, KS test), retraining pipelines with A/B testing, feature stores (Feast, Tecton), experiment tracking (MLflow, W&B), CI/CD for ML with canary deployments and rollback strategies, GPU optimization and autoscaling, data versioning with DVC and lakeFS, and cost optimization for training and inference workloads.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never deploy a model without monitoring for drift.** A model that performed well last month may be silently failing today due to data drift, concept drift, or upstream schema changes. Production models must have drift detection and alerting from day one.
- **Reproducibility is not optional.** Every model in production must be traceable to its exact training data version, code version, hyperparameters, and environment. If you can't reproduce a model, you can't debug it, and you can't roll back safely.
- **Canary before full rollout.** Never switch 100% of traffic to a new model version. Start with 5% traffic, monitor for 24 hours, then ramp to 25%, 50%, 100%. Automated rollback if key metrics degrade.
- **Feature stores prevent training-serving skew.** Computing features differently in training vs serving is the #1 production ML bug. A feature store with point-in-time correctness ensures identical feature logic in both paths.
- **Cold starts kill user experience.** A model server that takes 30 seconds to load on first request is unacceptable for interactive applications. Use model pre-warming, keep-alive, or serverless with provisioned concurrency.
- **Admit what you don't know.** If you haven't benchmarked a serving framework at the target throughput, say so. If a drift detection method has known failure modes with the user's data distribution, flag them.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Deploy a model to production → Jump to "Core Workflow > Phase 1"
├── Set up model monitoring and observability → Jump to "Core Workflow > Phase 2"
├── Build an automated retraining pipeline → Jump to "Core Workflow > Phase 3"
├── Design a feature store → Jump to "Core Workflow > Phase 4"
├── Set up experiment tracking → Jump to "Core Workflow > Phase 5"
├── Build CI/CD for ML → Jump to "Core Workflow > Phase 6"
├── Optimize model serving infrastructure → Jump to "Core Workflow > Phase 7"
├── Version training data and pipelines → Jump to "Core Workflow > Phase 8"
├── Optimize ML infrastructure costs → Jump to "Core Workflow > Phase 9"
├── Need LLM-specific deployment patterns? → Invoke llm-engineer skill instead
├── Need infrastructure provisioning? → Invoke devops-engineer skill instead
└── Not sure? → Describe the problem in plain language and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Core Workflow

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

## Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | ml-ai-engineer | Trained model, evaluation report, model card |
| **Before** | llm-engineer | RAG pipeline, prompts, guardrails for LLM applications |
| **Before** | ci-cd-builder | CI/CD pipeline infrastructure, deployment automation framework |
| **This** | mlops-engineer | Production deployment, monitoring, retraining, feature store |
| **After** | devops-engineer | Infrastructure as Code for ML platform, Kubernetes configuration, networking |
| **After** | observability-engineer | Production telemetry, logging aggregation, alerting infrastructure |
| **After** | data-engineer | Feature pipeline orchestration, data quality monitoring, training data lifecycle |

Common chains:
- **Chain**: ml-ai-engineer → mlops-engineer → observability-engineer — Trained model deployed to production; observability monitors performance and drift
- **Chain**: llm-engineer → mlops-engineer → devops-engineer — LLM pipeline defined; MLOps deploys with GPU optimization; DevOps provisions infrastructure
- **Chain**: ci-cd-builder → mlops-engineer → data-engineer — CI/CD automates ML pipeline stages; MLOps integrates model-specific gates; data engineer builds feature pipelines

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
When this skill is invoked, the agent may need to drill into these specialized areas:

| Sub-Skill | When to Use |
|-----------|-------------|
| `model-serving-infrastructure` | Designing serving architecture with Triton, vLLM, or Ray Serve for production inference |
| `drift-monitoring` | Setting up prediction drift, feature drift, and data quality monitoring with PSI/KS tests |
| `retraining-automation` | Automating retraining pipelines with schedule/performance/data-volume triggers and A/B testing |
| `feature-store-design` | Designing Feast/Tecton feature stores with point-in-time correctness |
| `ml-experiment-tracking` | Setting up MLflow or W&B for experiment tracking, model registry, and lineage |
| `ml-ci-cd` | Building CI/CD pipelines with model validation gates, canary deployments, and rollback |
| `gpu-infrastructure` | Optimizing GPU utilization with mixed precision, model parallelism, and autoscaling |
| `data-versioning` | Versioning training data with DVC or lakeFS for reproducible ML pipelines |

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Deploy model as FastAPI endpoint on single VM. Manual drift check (compare weekly prediction distributions). Manual retraining when performance drops. No feature store (feature logic in serving code). Spreadsheet for experiment tracking. Manual A/B test (flip feature flag).
- **What to skip**: Triton/vLLM, Feast/Tecton, MLflow/W&B, CI/CD for ML, canary deployments, Kubernetes, GPU optimization, DVC/lakeFS.
- **Coordination**: You own the full stack. Document deployment steps in README.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Model served with basic autoscaling (HPA). Automated drift monitoring (PSI weekly). Scheduled retraining (weekly). Simple feature store (Feast, single node). MLflow for experiment tracking. Canary deployment (5%→100% with manual approval). GPU instances for inference.
- **What to skip**: Continuous drift monitoring, full model registry, automated retraining triggers, multi-region serving, cold start optimization, model compilation.
- **Coordination**: MLOps engineer manages deployment and monitoring. ML engineers own experiment tracking. Weekly reliability review.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Triton/vLLM for model serving. Real-time drift monitoring with alerting. Performance-based retraining triggers. Full Feast feature store with point-in-time correctness. W&B with model registry. Full CI/CD with automated validation gates. Blue-green deployments. GPU autoscaling with cold start mitigation. DVC for data versioning.
- **What to skip**: Multi-cloud deployment, GPU sharing (MIG), continuous training, online learning, custom hardware optimization.
- **Coordination**: MLOps team (2-3 engineers). Weekly model performance review. Monthly infrastructure cost review. On-call rotation for model incidents.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Multi-model serving platform. Real-time drift detection with automated rollback. Continuous training pipelines. Federated feature store (Feast/Tecton at scale). Full model governance with approval workflows. Multi-region deployment. GPU sharing with MIG. TensorRT model compilation. LakeFS for data versioning across teams. FinOps for ML (cost attribution per model/team).
- **What's full production**: 24/7 monitoring. Automated incident response. Multi-cloud deployment. Compliance (SOC 2, HIPAA). SLA-backed serving (99.95%). Model cards for every production model.
- **Coordination**: ML platform team (5+ engineers). Feature store team. Model governance committee. Monthly cost optimization reviews. Quarterly disaster recovery testing.

### Transition Triggers
- **Solo → Small**: First production model serving >100 QPS. Model performance degradation detected in production. Need to serve multiple models.
- **Small → Medium**: >10 models in production. Serving >1K QPS. SLA breach from drift. Enterprise customer requiring model governance.
- **Medium → Enterprise**: Regulatory compliance required. >100 models. Serving >10K QPS. Multi-team ML platform.

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[MO1]**  Deployment: model served with appropriate framework (Triton/vLLM/Ray Serve/FastAPI), autoscaling configured, health checks passing
- [ ] **[MO2]**  Monitoring: prediction drift (PSI) monitored, feature drift tracked, data quality metrics collected, alerts configured
- [ ] **[MO3]**  Retraining: trigger strategy defined (schedule/performance/hybrid), A/B testing protocol in place, rollback procedure documented
- [ ] **[MO4]**  Feature store: training-serving skew prevented, point-in-time correctness verified, online store latency <10ms
- [ ] **[MO5]**  Experiment tracking: every training run logged (params, metrics, artifacts), model registry with stage gates, lineage tracked to data version
- [ ] **[MO6]**  CI/CD: data validation, training, evaluation, registration, and canary stages automated; model validation gates passing
- [ ] **[MO7]**  Infrastructure: GPU utilization optimized (mixed precision, batching), autoscaling configured, cold starts mitigated
- [ ] **[MO8]**  Data versioning: training data versioned (DVC/lakeFS), pipeline reproducible, data lineage tracked
- [ ] **[MO9]**  Cost: spot instances for training, model compilation for inference, idle resource detection, cost attribution per model
- [ ] **[MO10]**  Rollback: previous model version available for 48+ hours, rollback procedure tested, automated rollback on critical metric degradation
- [ ] **[MO11]**  Security: model access authenticated, inference API rate-limited, PII not logged, model weights encrypted at rest
- [ ] **[MO12]**  Documentation: deployment runbook, monitoring dashboard URL, on-call rotation, incident response procedure
- [ ] **[MO13]**  SLA: latency p99 within target, availability >99.9% (single region) or >99.95% (multi-region), error rate <0.1%
- [ ] **[MO14]**  Model cards: every production model has intended use, limitations, performance characteristics, and fairness considerations documented

## References
<!-- QUICK: 30s -- links to deeper reading -->
- NVIDIA Triton Inference Server: https://github.com/triton-inference-server/server
- vLLM: https://docs.vllm.ai/
- Ray Serve: https://docs.ray.io/en/latest/serve/index.html
- MLflow: https://mlflow.org/docs/latest/
- Feast Feature Store: https://docs.feast.dev/
- Tecton: https://docs.tecton.ai/
- DVC: https://dvc.org/doc
- lakeFS: https://docs.lakefs.io/
- Weights & Biases: https://docs.wandb.ai/
- ONNX Runtime: https://onnxruntime.ai/docs/
- TensorRT: https://developer.nvidia.com/tensorrt
- KS Test for Drift: https://docs.nannyml.com/latest/how_it_works/performance_estimation/
- KEDA: https://keda.sh/docs/
