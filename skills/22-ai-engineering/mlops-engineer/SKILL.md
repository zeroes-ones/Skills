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
chain:
  consumes_from:
    - ml-ai-engineer
    - devops-engineer
    - data-engineer
    - llm-engineer
  feeds_into:
    - llm-engineer
    - ai-safety-engineer
    - ml-ai-engineer
    - observability-engineer
---
# MLOps Engineer

Production machine learning operations — from model deployment through continuous monitoring and automated retraining. Covers serving infrastructure (Triton, vLLM, Ray Serve), observability with drift detection (PSI, KS test), retraining pipelines with A/B testing, feature stores (Feast, Tecton), experiment tracking (MLflow, W&B), CI/CD for ML with canary deployments and rollback strategies, GPU optimization and autoscaling, data versioning with DVC and lakeFS, and cost optimization for training and inference workloads.

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

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

## When to Use
<!-- QUICK: 30s — five reasons to invoke this skill -->

- **Putting your first ML model into production** — Your data scientist has a trained model in a notebook and you need to deploy it as a reliable, monitored service with proper infrastructure, model versioning, and rollback capability.
- **Model performance degrading in production** — Your deployed model's accuracy has dropped significantly (training-serving skew, data drift, concept drift). You need drift detection, retraining triggers, and a rollback strategy.
- **Optimizing ML infrastructure costs** — Your GPU bill is larger than your compute bill. You need GPU utilization optimization, multi-model serving, autoscaling, and cost allocation tagging per model/team.
- **Setting up ML CI/CD for the first time** — You're deploying models manually or with ad-hoc scripts. You need a proper pipeline: data validation → training → evaluation → staging → canary → production, all automated and gated.
- **Building a feature store for consistency across training and serving** — Your data scientists compute features one way in notebooks and your serving pipeline computes them differently. You need a feature store (Feast/Tecton) with point-in-time correctness and low-latency serving.

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

<!-- NEIGHBORS: MLOps bridges model development and production operations — coordinate on infrastructure, data, and serving -->

| Upstream Skill | What You Receive | Decision Gate |
|---|---|---|
| `ml-ai-engineer` | Model artifacts, training code, evaluation metrics, feature engineering logic | Validate model is production-ready before deploying; gate on reproducibility checks |
| `devops-engineer` | Infrastructure provisioning, Kubernetes clusters, CI/CD pipelines, networking and security | Align on infrastructure requirements before model deployment; coordinate autoscaling policies |
| `data-engineer` | Data pipelines, feature computation jobs, data warehouse schemas, data freshness SLAs | Ensure feature pipeline latency meets serving SLAs before productionizing |
| `llm-engineer` | LLM serving requirements (latency targets, throughput, GPU type), prompt pipeline specs | Right-size GPU infrastructure for LLM inference; validate streaming performance |

| Downstream Skill | What You Provide | Artifacts |
|---|---|---|
| `llm-engineer` | Model serving endpoints, GPU-optimized inference, autoscaling configs, latency dashboards | Serving URLs, GPU allocation specs, scaling policies, performance benchmarks |
| `ai-safety-engineer` | Model monitoring data (drift metrics, performance degradation, data quality alerts) | Drift dashboards, model performance reports, data quality incident logs |
| `ml-ai-engineer` | Production performance feedback, retraining triggers, A/B test results, infrastructure constraints | Retraining recommendations, production metric dashboards, infrastructure capacity reports |
| `observability-engineer` | Model-specific metrics (inference latency, prediction distribution, feature drift), alerting rules | Model health dashboards, drift alert configurations, SLA monitoring |

**Coordination cadence:**
- **Pre-deployment:** Infrastructure review with `devops-engineer` on GPU provisioning and networking
- **Daily:** Monitoring sync — review drift alerts and model performance dashboards
- **Weekly:** Sync with `llm-engineer` on serving performance and cost optimization
- **Bi-weekly:** Retraining review with `ml-ai-engineer` on model refresh candidates
- **Monthly:** Capacity planning with `data-engineer` and `devops-engineer` on growth projections

## Proactive Triggers
<!-- DEEP: 10+min — when to intervene before someone asks -->

| Trigger | Action | Why |
|---------|--------|-----|
| ML team ships 3 new models in one sprint, each with bespoke deployment scripts | Propose centralized model serving platform (Triton/vLLM) with standardized deployment config; sync with `ml-ai-engineer` on model packaging contract (ONNX/TensorRT) | Bespoke deployment per model creates N × deployment complexity; centralized serving with standardized config reduces deploy time from days to minutes and eliminates per-model infrastructure drift |
| Data science team reports "model works in notebook but not in production" — training-serving skew suspected | Propose feature store (Feast/Tecton) with point-in-time correctness; implement training-serving feature validation in CI/CD; sync with `data-engineer` on feature computation pipeline and `ml-ai-engineer` on feature engineering code | Training-serving skew is the #1 silent ML failure — the model doesn't crash, it just produces wrong predictions; point-in-time feature store ensures training data reflects the world as it was when labels were generated |
| Product team wants to launch a new recommendation model without A/B testing framework | Propose canary deployment pipeline (5% → 25% → 50% → 100%) with automated rollback on guardrail metric degradation; sync with `ml-ai-engineer` on evaluation criteria and `product-manager` on business KPIs | Deploying without A/B means you can't measure impact; a model with better offline metrics can reduce user engagement; automated rollback prevents 3-week degradation windows |
| Backend team reports model serving latency spikes during peak hours, GPU utilization at 15% | Propose dynamic batching with configurable max delay; implement GPU-aware autoscaling (not CPU-based); sync with `backend-developer` on serving API latency SLA and `devops-engineer` on Kubernetes HPA configuration | CPU-based autoscaling for GPU workloads is like monitoring tire pressure to decide when to refuel; dynamic batching can 4× throughput without adding GPUs; GPU utilization should drive scaling decisions |
| CI/CD pipeline deploys model artifacts but no validation between training and production | Propose model CI/CD with automated gates: data validation → training → evaluation → registry → canary → full promotion; sync with `ml-ai-engineer` on evaluation harness and `devops-engineer` on pipeline orchestration | Manual model deployment is the root cause of "which version is serving right now?" incidents; automated CI/CD with gates ensures every production model passed the same validation |
| Monitoring team reports model performance dashboards are empty — no drift detection in place | Propose PSI/KS-test drift monitoring per feature with automated alerting; implement prediction distribution comparison between training and serving; sync with `observability-engineer` on metric pipeline and alert routing | Drift is invisible without monitoring — models silently degrade for weeks before business metrics detect it; per-feature PSI catches which specific input is drifting before aggregate metrics show impact |
| Team manually retrains models when "someone notices accuracy dropped" | Propose automated retraining triggers: scheduled (weekly), performance-based (drift > threshold), and data-volume-based (N new labeled examples); sync with `ml-ai-engineer` on retraining criteria and `data-engineer` on data freshness | Reactive retraining means models serve degraded predictions for days after drift begins; automated triggers close the loop between detection and remediation |
| Model registry is a shared spreadsheet with columns "model_name" and "where_deployed" | Propose MLflow/W&B model registry with stage transitions, approval workflows, metadata (training data hash, code commit, evaluation metrics); sync with `ml-ai-engineer` on registry integration | A spreadsheet model registry cannot answer "which model version is serving?" during an incident; a proper registry with automated stage transitions is the single source of truth for production ML |

## Core Workflow
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

## Cross-Skill Integration
<!-- STANDARD: 3min -->

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

## Decision Trees
<!-- QUICK: 60s -- flowchart-style logic for fork-in-the-road decisions -->

### Model Retrain Trigger: Schedule vs Drift vs Performance Degradation
<!-- Decision tree for choosing the right retraining trigger strategy -->

```
START: Determine when and why to retrain a production model
  │
  ├─ Is the model's performance directly measurable in production within 24 hours (labels available, ground truth observable)?
  │    ├─ YES → PERFORMANCE-BASED trigger. Retrain when accuracy/precision/recall drops below threshold.
  │    └─ NO → Continue
  │
  ├─ Does the input data distribution shift seasonally, cyclically, or due to external factors (market conditions, user behavior changes, new product features)?
  │    ├─ YES → DRIFT-BASED trigger. Retrain when PSI/KS statistic exceeds threshold on feature distributions.
  │    └─ NO → Continue
  │
  ├─ Is there a regulatory or compliance requirement for periodic retraining (FDA, fair lending, model risk management)?
  │    ├─ YES → SCHEDULE-BASED trigger (with performance/drift as additional triggers). Regulatory minimum frequency.
  │    └─ NO → Continue
  │
  ├─ Is the model a low-risk, slowly-changing problem where manual retraining every 1-3 months has been sufficient?
  │    ├─ YES → SCHEDULE-BASED (monthly/quarterly) with drift monitoring as a safety net. Don't over-engineer.
  │    └─ NO → Continue
  │
  └─ Do you have both observable labels AND feature drift monitoring?
       ├─ YES → HYBRID. Performance degradation triggers immediate retrain. Drift triggers investigation. Schedule is fallback.
       └─ NO → Start with schedule, add drift monitoring, graduate to performance-based when labels are available.
```

### Feature Store vs Feature Pipeline
<!-- Decision tree for choosing between a managed feature store and ad-hoc feature pipelines -->

```
START: You need to serve features for model training and inference
  │
  ├─ Are the same features used by more than one model, team, or use case?
  │    ├─ YES → FEATURE STORE. Shared features need point-in-time correctness and a registry.
  │    └─ NO → Continue
  │
  ├─ Do you need point-in-time correct historical feature values for training (e.g., "what was the user's 30-day transaction count as of March 15, not today")?
  │    ├─ YES → FEATURE STORE. Feature pipelines without point-in-time logic create training-serving skew.
  │    └─ NO → Continue
  │
  ├─ Is online inference latency requirement <10ms and you need pre-computed features at request time?
  │    ├─ YES → FEATURE STORE with online serving layer. Computing features at request time will violate latency SLA.
  │    └─ NO → Continue
  │
  ├─ Are you building a single model, with ≤5 features, from a single data source, in a prototype phase?
  │    ├─ YES → FEATURE PIPELINE. Simple ETL into training data. Don't introduce feature store overhead for a prototype.
  │    └─ NO → Continue
  │
  ├─ Is feature engineering logic complex (windowed aggregations, multi-source joins, entity embeddings) and must be identical between training and serving?
  │    ├─ YES → FEATURE STORE. Duplicating complex logic in training and serving code guarantees divergence.
  │    └─ NO → Continue
  │
  └─ Are you serving <100 QPS with batch inference (not real-time)?
       ├─ YES → FEATURE PIPELINE with batch feature computation. Feature store online serving is overkill for batch.
       └─ NO → FEATURE STORE. At production scale, the governance, reuse, and consistency benefits justify the infrastructure cost.
```

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

## Best Practices
<!-- DEEP: 10+min -->

1. **Design the feature store for point-in-time correctness from day one**: The most common source of training-serving skew is using "current" feature values when training on historical labels. If you train a churn model on January data but join with customer features as they exist in July, you're training on the future. Feast/Tecton point-in-time joins ensure training data reflects the world as it was when the label was generated. Validate with a simple test: train on historical data, then check if feature values match what would have been served at that time.

2. **Treat the model registry as the single source of truth, not a nice-to-have**: Every model in production must have a registry entry with stage (staging/production/archived), owner, training data version, evaluation metrics, and approval trail. The registry answers "which model version is serving right now?" in an incident — a question that should never require searching through Kubernetes configs or Slack threads. Automate stage transitions: a model graduates from staging to production only through the CI/CD pipeline, never manually.

3. **Design A/B testing infrastructure to measure business outcomes, not just model metrics**: A model with 2% higher AUC that reduces user engagement by 5% is a worse model. A/B tests must track guardrail metrics (latency, error rate, cost per prediction) alongside business KPIs. Pre-register success criteria before the test starts. Run tests long enough to reach statistical significance — a 2-hour A/B test on a model serving 10 QPS proves nothing.

4. **Shadow-deploy new models for a full business cycle before cutting over traffic**: Run the candidate model in shadow mode (log predictions without serving them) for at least one full business cycle (week/month/quarter depending on domain). Compare shadow predictions against production predictions on the same traffic. Look for: prediction distribution shifts, unexpected edge case behavior, latency differences, and cost differences. A model that looks great in offline evaluation can behave very differently on production traffic patterns.

5. **Build data validation as a pipeline stage, not a monitoring afterthought**: Validate training data before it reaches the model — schema checks (expected columns and types), range checks (values within expected bounds), freshness checks (data not stale), and distribution checks (no sudden shifts). Use Great Expectations or TFDV with automated blocking: if validation fails, the pipeline stops. A model trained on corrupted data is worse than no model at all.

6. **Version models, data, AND code together for full reproducibility**: A model artifact without the training data version and the training code version is not reproducible. Use DVC or lakeFS to version training data. Use MLflow or W&B to version model artifacts. Use git to version training code. Store the triplet (data hash, code commit, model version) in the model registry. When debugging a production issue, you should be able to exactly reproduce the model that's serving.

7. **Monitor for training-serving skew with statistical tests, not eyeballing**: Compute PSI (Population Stability Index) or KS statistic between training data distribution and production feature distribution. Set automated thresholds (PSI > 0.2 triggers alert). Monitor per-feature, not just aggregate. A model can look fine on aggregate metrics while one critical feature has silently drifted. Run these checks on every prediction log batch, not weekly.

8. **Optimize inference costs as aggressively as you optimize model accuracy**: A 0.5% accuracy improvement that triples inference cost is rarely worth it. Use mixed precision (FP16/INT8), model compilation (TensorRT/ONNX), dynamic batching, and spot instances for batch inference. Profile per-model cost and set budgets. Implement model right-sizing: serve simple models on CPU, complex models on GPU. Track cost-per-prediction as a production metric alongside latency and accuracy.

## Anti-Patterns
<!-- DEEP: 10+min — mistakes that turn production ML into production incidents -->

| ❌ Anti-Pattern | ✅ Do This Instead |
|---|---|
| **Manual model deployment** — SSH into prod server, `scp model.pkl`, restart gunicorn; no rollback plan, no approval trail, no deployment log | Deploy via CI/CD pipeline: model artifact → staging validation → canary (5% traffic, 24h) → automated rollback on metric degradation → full promotion; every deployment logged in model registry with approval trail |
| **No canary or blue-green deployment** — new model replaces old model on 100% of traffic instantly; bad model affects all users simultaneously | Implement canary deployment: 5% → 25% → 50% → 100% with automated rollback if P99 latency, error rate, or business metrics degrade; blue-green for instant rollback (switch traffic back to previous stable deployment) |
| **No feature store** — feature computation logic duplicated in training code (Python/pandas) and serving code (Java/Go); training uses `transaction_amount / 100`, serving uses `transaction_amount / 1000` — silent skew | Centralize feature definitions in feature store (Feast/Tecton); training and serving read from the same feature definition; point-in-time correct joins for training data; sync feature definitions with `data-engineer` and `ml-ai-engineer` |
| **No model registry** — "which model version is serving?" answered by grepping Kubernetes pod env vars during an incident at 3 AM | Every production model registered with stage (staging/production/archived), training data hash, code commit, evaluation metrics, and owner; automated stage transitions via CI/CD; registry is the single source of truth for "what's running where" |
| **No drift monitoring** — model performance degrades silently for 8 weeks until business metrics detect the problem; $340K in losses before anyone notices | Implement per-feature PSI/KS-test monitoring with automated alerting; compare prediction distributions between training baseline and production traffic hourly; automated retraining trigger on drift > threshold; sync with `observability-engineer` on alert routing |
| **Training-serving skew from duplicated feature logic** — `transaction_amount` normalized with min-max in training (Python) but z-score in serving (Java); model receives features on wrong scale, produces confident-but-wrong predictions | Feature transformations defined once in feature store or shared library consumed by both training and serving; validate feature values in CI/CD: sample production features, compare distribution to training baseline, block deployment if KS statistic > 0.1 |
| **GPU overprovisioning without cost optimization** — 4× p3.2xlarge instances at $28K/month, GPU utilization 12%, autoscaling based on CPU (which never exceeds 25%) | Right-size GPU instances: benchmark model with FP16/INT8 quantization; enable dynamic batching; autoscale on GPU utilization + request queue depth; use spot instances for non-production; scheduled downscaling during off-peak hours; sync with `devops-engineer` on infrastructure optimization |
| **Data validation as monitoring afterthought** — schema checks catch missing columns but pass silently when categorical values are semantically swapped ("electronics"→1 becomes "electronics"→2 after Python version migration) | Validate training data before it reaches the model: schema checks + range checks + freshness checks + distributional checks (compare categorical frequencies to baseline); semantic consistency checks (label encoding produces same mapping as previous run); block pipeline if validation fails; sync with `data-engineer` on data quality contracts |

## Scale Depth: Solo → Small → Medium → Enterprise
<!-- DEEP: 10+min -->

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

## Error Decoder
<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Fraud detection model's precision dropped from 87% to 62% over 8 weeks. The operations team noticed when the manual review queue tripled in size. The model was still serving predictions with high confidence — it was just confidently wrong. $340K in fraudulent transactions were approved during the degradation window. | A data pipeline change modified how `transaction_amount` was normalized in production (changed from min-max to z-score normalization). The training pipeline still used min-max normalization. The model was receiving features on a completely different scale, but the prediction API returned the same confidence scores because the model architecture had no mechanism to detect out-of-distribution inputs. | Added feature distribution comparison between training and serving (KS test per feature, hourly). Implemented schema validation in the serving pipeline that compares incoming feature statistics to training baseline. Added a "prediction confidence" calibration layer that reduces confidence for features outside training distribution. Created a feature transformation registry where all normalization logic is defined once and used by both training and serving. | Training-serving skew is the most dangerous ML failure mode because it's silent. The model doesn't crash, doesn't throw errors, and continues producing predictions with the same confidence scores. The only signal is degraded business outcomes, which can take weeks to detect. Statistical distribution monitoring is not optional. |
| Feature store (Feast online serving) experienced a Redis cluster failure. Within 60 seconds, 23 production models were unable to retrieve features at inference time. Models began serving default values (zeros) for missing features. A pricing model recommended $0.00 for 1,400 transactions before the circuit breaker fired. Total revenue impact: $47K in underpriced transactions. | Models treated feature store unavailability identically to "feature value is zero." No distinction between "feature is legitimately zero" and "feature store timed out." Circuit breakers were per-model, not correlated across the feature store dependency — each model independently detected its own "degradation" without recognizing the shared root cause. The feature store was a single point of failure for the entire ML platform. | Implemented feature-level sentinel values: when feature store is unavailable, serve `NaN` not `0.0`. Models explicitly check for missing features and either refuse to predict (safety-critical) or use a fallback model trained without those features. Deployed cross-model circuit breaker: if >3 models detect feature retrieval failures within 30 seconds, all models using that feature store enter degraded mode simultaneously. Added feature store read-replica with automatic failover. Implemented local feature cache with 5-minute TTL as a buffer against transient outages. | A centralized feature store is a centralized failure domain. Every model that depends on the feature store must handle its unavailability gracefully — and the handling must be coordinated across models, not siloed. Sentinel values that mean "I don't know" are safer than default values that mean "assume zero." |
| Recommendation model was retrained on a weekly schedule. The week-27 retrain produced a model with 11% lower click-through rate than the week-26 model. The degradation was discovered during a monthly business review when the product manager asked "why did recommendations engagement dip in early July?" The worse model had been serving for 3 weeks. | Automated retraining pipeline checked that the new model "trained successfully" (no errors) but did not compare its performance against the currently-serving model. The pipeline replaced the production model because the new model's offline AUC was above a static threshold — but below the incumbent model's offline AUC. No A/B test or canary deployment. No automated rollback on metric degradation. | Added champion/challenger comparison in the retraining pipeline: new model must outperform the currently-serving model on evaluation metrics (not just clear a static threshold). Implemented canary deployment: new model serves 5% of traffic for 24 hours while monitoring business metrics. Automated rollback if canary model underperforms champion by >2% on any guardrail metric. Added "time since last model update" to the monitoring dashboard so stale-model alerts fire even if retraining pipeline is "succeeding." | A retraining pipeline that replaces models without comparing them to the incumbent is an automated downgrade pipeline. "Successfully trained" ≠ "better than current." Canary deployment with business metric validation is the only way to prevent automated quality regression. |
| Inference serving ran on 4× p3.2xlarge instances (single GPU each) at a cost of ~$28K/month. GPU utilization averaged 12%. Load testing showed the service could handle peak traffic on 2 instances, but autoscaling was configured based on CPU utilization (which never exceeded 25%) rather than GPU utilization or request queue depth. | Autoscaling metric (CPU) was not the bottleneck metric (GPU memory bandwidth and request latency). The model used FP32 precision by default with no mixed-precision optimization. Dynamic batching was disabled (each request processed independently). Instances were provisioned for peak capacity 24/7 with no scheduled downscaling during off-peak hours (midnight-6am traffic was 8% of peak). | Changed autoscaling to track GPU utilization, request queue depth, and P99 latency. Enabled FP16 mixed precision (40% throughput improvement, no accuracy loss). Enabled dynamic batching with 10ms max batch delay. Implemented scheduled downscaling to 1 instance during off-peak hours. Switched to spot instances for non-production inference. Migrated to p3.2xlarge → g5.xlarge (better price-performance for the model size). New monthly cost: $8K. Same latency, same accuracy. | GPU infrastructure costs are dominated by what you don't measure. CPU-based autoscaling for GPU workloads is like monitoring tire pressure to decide when to refuel. GPU utilization, batch efficiency, and inference-specific metrics must drive infrastructure decisions. Every dollar spent on unused GPU capacity is a dollar that could fund more model iterations. |
| All data validation checks passed. Schema was correct. Column types matched. Value ranges were within bounds. The model trained successfully and was deployed. Two days later, users reported nonsensical recommendations. Investigation revealed the training data had correct schema and ranges but the `product_category` column values were silently remapped: "electronics" → 1, "books" → 2 became "electronics" → 2, "books" → 1 due to a dictionary key ordering bug in a Python 3.6 → 3.10 migration. | Data validation checked types (int), ranges (1-50 valid), and null rate (0%) — all passed. No semantic validation: checking that the distribution of categories matched the expected distribution. No check that label values still mapped to the same meaning. The validation pipeline validated syntax, not semantics. | Added distributional validation: compare categorical column value frequencies against a known-good baseline. Added semantic consistency checks: verify that label encoding produces the same mapping as the previous training run. Implemented a "smoke test" where a small set of known inputs must produce expected predictions before the model is promoted. Added data profiling snapshots to the model registry for comparison across training runs. | Schema validation catches syntax errors. Distributional validation catches semantic errors. A pipeline that validates that columns exist and have the right types will happily pass data where all categories are swapped. Semantic drift is harder to detect than schema drift — and much more dangerous. |

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

## What Good Looks Like
<!-- QUICK: 30s -- aspirational north star for this skill -->

> MLOps is not about deploying models — it's about building the confidence that every model in production is performing as intended, every minute of every day, and that when it's not, the system knows before the business does. **What good looks like**: model deployments are automated, gated, and reversible in under 5 minutes; training-serving skew is detected within hours, not weeks; feature stores serve point-in-time correct values and survive partial infrastructure failures gracefully; retraining pipelines only replace models that are provably better than the incumbent; GPU infrastructure is right-sized to actual demand with cost attribution per model; every model in production has a documented owner, a rollback plan, and a monitored SLA; and when someone asks "is the model still working?", the answer is a dashboard URL, not a Slack thread of guesses. A platform that can deploy 100 models but can't prove any of them are working correctly is a deployment pipeline, not an MLOps practice.

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
