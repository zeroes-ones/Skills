---
name: ml-ai-engineer
description: >
  Use when training ML models, building RAG pipelines, fine-tuning LLMs, deploying models to production,
  designing MLOps infrastructure, monitoring drift, or implementing responsible AI guardrails. Handles
  model selection, training pipelines, LLM integration patterns, serving at scale, evaluation frameworks,
  and AI safety. Do NOT use for statistical hypothesis testing, data pipeline construction, BI dashboard
  creation, or pure data engineering.
license: MIT
tags:
- machine-learning
- llm
- rag
- mlops
- model-serving
- fine-tuning
- embeddings
- ai-safety
author: Sandeep Kumar Penchala
type: data
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 5000
chain:
  consumes_from:
  - data-engineer
  - data-scientist
  - mlops-engineer
  - quantitative-analyst
  feeds_into:
  - data-scientist
  - llm-engineer
  - mlops-engineer
  - quantitative-analyst
  - trust-safety-engineer
---
# ML & AI Engineer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end machine learning and AI engineering — from problem framing through production monitoring.
Covers the full ML lifecycle, model selection, data preparation, training, MLOps infrastructure,
LLM integration patterns, RAG architectures, model serving at scale, evaluation frameworks,
drift monitoring, and responsible AI guardrails.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to deploy a model without drift monitoring.** Production models degrade silently. | Trigger: `grep -L "drift\|PSI\|KS-test\|evidently\|whylogs\|nannyml" requirements.txt deploy.py serve.py Dockerfile 2>/dev/null` returns non-empty → no drift monitoring configured. | STOP. Respond: "This deployment has no drift monitoring. Run `pip install evidently && python -c 'import evidently'` to bootstrap drift detection. Every production model needs data drift (PSI/KS) and concept drift alerts before serving traffic." |
| **R2** | **REFUSE to report accuracy without confusion matrix, precision, recall, and per-class F1.** | Trigger: output text contains `accuracy.*[0-9]+\.[0-9]+%` and does NOT contain `confusion_matrix\|classification_report\|precision\|recall\|f1` → misleading metric. | STOP. Respond: "Accuracy alone is meaningless for imbalanced data. Run `sklearn.metrics.classification_report(y_true, y_pred)` and `sklearn.metrics.confusion_matrix(y_true, y_pred)` before reporting results." |
| **R3** | **REFUSE to fine-tune an LLM without first evaluating the base model on the target task.** | Trigger: `grep -r "fine.tun\|LoRA\|QLoRA" . --include="*.py"` returns hits AND `grep -r "baseline.*eval\|base.*model.*metric\|zero.shot" . --include="*.py"` returns empty → no baseline established. | STOP. Respond: "Before fine-tuning, run the base model on your evaluation set first: `python eval.py --model base --dataset your_data`. You must prove fine-tuning helps before spending compute. Baseline delta must be ≥ 5% improvement before fine-tuning is justified." |
| **R4** | **DETECT training-serving skew.** Feature engineering MUST be a single source of truth shared between training and serving. | Trigger: `diff <(grep -h "def.*transform\|def.*feature" train.py | sort) <(grep -h "def.*transform\|def.*feature" serve.py | sort)` returns non-empty → duplicated feature logic. | STOP. Respond: "Feature engineering is duplicated in training and serving. Extract into `features.py` shared library, add `test_feature_parity.py` that runs 1,000 examples through both pipelines and asserts identical output within 1e-6 tolerance." |
| **R5** | **REFUSE to serve LLM output to users without retrieval verification or factual grounding check.** | Trigger: code imports `langchain\|llama_index\|openai` and lacks `verify\|grounding\|hallucination\|guardrail\|safety` in same file → no output verification. | STOP. Respond: "LLM output is reaching users unverified. Add retrieval verification: confirm retrieved chunks contain entities in the answer. Add LLM-as-judge factual grounding check. Every RAG pipeline needs a 'did we actually retrieve this?' gate before user-facing output." |
| **R6** | **DETECT unversioned experiment artifacts.** Every training run must be reproducible. | Trigger: `grep -L "seed\|random_state\|set_seed\|deterministic" train.py` returns non-empty OR `grep -L "requirements.*\.txt\|pyproject\.toml" Makefile *.sh 2>/dev/null` returns non-empty → non-reproducible. | STOP. Respond: "Experiments are not reproducible. Pin all random seeds (`random.seed(42)`, `np.random.seed(42)`, `torch.manual_seed(42)`, `torch.backends.cudnn.deterministic = True`), pin dependencies (`pip freeze > requirements.txt`), and version datasets with DVC or lakeFS." |
| **R7** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R8** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

Masters of ml ai engineer don't just build — they build **the right thing, at the right time, with the right trade-offs**. They think in systems, not tasks.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Shiny object syndrome** — chasing new tools without evaluating fit | Before adopting any new tool, write the "why this over the incumbent" justification |
| **Over-engineering** — building for hypothetical scale | Default to simplest solution; add complexity only when the current solution actually breaks |
| **Not-invented-here** — preferring to build rather than compose | Always evaluate 2 existing solutions before building custom |
| **Sunk cost fallacy** — sticking with a technology because you already invested in it | Re-evaluate tech choices every quarter; migration cost vs. staying cost |

### What Masters Know That Others Don't
- The **failure modes** of every component in their stack — not just the happy path
- When **not** to use their favorite tool (every tool has a misuse zone)
- That **data/model quality decays over time** — monitoring is not optional, it's foundational

### When to Break Your Own Rules
- **Move fast on reversible decisions.** Data format? Hard to change. Dashboard layout? Easy. Know the difference.
- **Skip the abstraction until the third use case.** Two is coincidence, three is a pattern.

## Route the Request

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("train.py", "model.fit\|.train()\|Trainer")` OR `file_contains("train.py", "LGBMClassifier\|XGBClassifier\|RandomForest")` | Training classical ML model → Jump to "Core Workflow" — Phase 2 (Training) |
| A2 | `file_contains("*.py", "@app.post.*predict\|FastAPI.*predict\|model.predict")` OR `file_contains("*.py", "bentoml\|mlflow.deploy\|sagemaker\|triton")` | Deploying a model → Jump to "Core Workflow" — Phase 4 (MLOps & Serving) |
| A3 | `file_contains("*.py", "langchain\|llama_index\|chromadb\|pinecone\|weaviate\|qdrant\|faiss")` OR `file_exists("rag.py")` OR `file_exists("retrieval.py")` | Building RAG pipeline → Jump to "Core Workflow" — Phase 3 (RAG Architecture) |
| A4 | `file_contains("*.py", "evidently\|whylogs\|nannyml\|great_expectations\|drift")` OR `file_contains("*.py", "classification_report\|confusion_matrix\|roc_auc")` | Evaluating model or detecting drift → Jump to "Core Workflow" — Phase 5 (Evaluation & Monitoring) |
| A5 | `file_contains("*.py", "peft\|LoRA\|QLoRA\|SFTTrainer\|prepare_model_for_kbit")` OR `file_contains("*.py", "trl\|DPOTrainer\|RewardTrainer")` | Fine-tuning an existing model → Jump to "Core Workflow" — Phase 2 (Fine-tuning) |
| A6 | `file_contains("*.py", "pandas\|pyspark\|polars\|feature_engine")` AND `file_exists("dbt_project.yml")` OR `file_contains("*.py", "Airflow\|Prefect\|Dagster")` | Training data pipeline needed → Invoke `data-engineer` skill |
| A7 | `file_contains("*.py", "torch.cuda\|nvml\|GPU\|CUDA")` AND `file_contains("*.py", "k8s\|kubernetes\|helm\|docker-compose")` | MLOps infrastructure needed → Invoke `mlops-engineer` skill |
| A8 | `file_contains("*.py", "scipy\.stats\|statistical\|hypothesis\|p_value\|t_test\|chi2")` | Statistical analysis needed → Invoke `data-scientist` skill |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Train a new model (classical ML or deep learning) → Jump to "Core Workflow" — Phase 2 (Training)
├── Deploy a model to production → Jump to "Core Workflow" — Phase 4 (MLOps & Serving)
├── Build a RAG pipeline with LLMs → Jump to "Core Workflow" — Phase 3 (RAG Architecture)
├── Evaluate model performance or detect drift → Jump to "Core Workflow" — Phase 5 (Evaluation & Monitoring)
├── Fine-tune an existing model (LoRA, QLoRA) → Jump to "Core Workflow" — Phase 2 (Fine-tuning)
├── Need data pipelines for training data → Invoke `data-engineer` skill
├── Need to deploy LLM with safety guardrails → Jump to "Best Practices" — responsible AI
├── Need statistical analysis → Invoke `data-scientist` skill
├── Need MLOps infrastructure → Invoke `mlops-engineer` skill
├── Need LLM-specific patterns → Invoke `llm-engineer` skill
└── Not sure? → Describe the problem in plain language and I'll route you

```

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single component/module | Implement a well-defined piece following established patterns |
| **L2** | Feature or service | Design and build a complete feature; make tech choices within team conventions |
| **L3** | System or product area | Define architecture for a product area; set team tech standards; mentor L1-L2 |
| **L4** | Multiple systems / platform | Define org-wide architecture patterns; make build-vs-buy decisions; influence industry practice |
| **L5** | Industry / ecosystem | Create new architectural patterns adopted across the industry; redefine what's possible |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L3 ml ai engineer, design..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Framing a business problem as an ML task and selecting the right approach
- Building end-to-end ML pipelines: data ingestion → feature engineering → training → serving
- Training classical ML models (XGBoost, LightGBM, scikit-learn) or deep learning (PyTorch, JAX)
- Designing MLOps infrastructure: experiment tracking, feature store, model registry, CI/CD for ML
- Building RAG applications with LLMs, embedding models, and vector databases
- Fine-tuning open-source LLMs (Llama, Mistral, Gemma, Qwen) with LoRA/QLoRA
- Deploying models: real-time APIs, batch scoring, streaming inference, edge deployment
- Evaluating models comprehensively: offline metrics, slicing, fairness, calibration, A/B testing
- Monitoring production models: data drift, concept drift, performance degradation
- Implementing AI safety: guardrails, red-teaming, hallucination detection, content filtering

## Decision Trees
**(QUICK)**

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### ML vs Heuristic vs LLM

```
                     ┌───────────────────────────────┐
                     │ START: Should this be ML?       │
                     └────────────┬──────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Can a deterministic heuristic  │
                    │ solve it with acceptable       │
                    │ accuracy?                      │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼────────┐  ┌──────────▼───────────┐
                    │ Heuristic   │  │ Need reasoning over   │
                    │ Ship in 1d  │  │ unstructured text?    │
                    └─────────────┘  └──┬───────────────┬────┘
                                       │YES            │NO
                                  ┌────▼────────┐ ┌───▼──────────┐
                                  │ Have >1K    │ │ Structured/   │
                                  │ labeled     │ │ tabular data? │
                                  │ examples?   │ └──┬────────┬───┘
                                  └──┬──────┬───┘    │YES     │NO
                                     │YES   │NO   ┌──▼──┐ ┌──▼──────┐
                                ┌────▼──┐ ┌─▼─────┐│XGBoost││Re-evaluate│
                                │Fine-tune│ │RAG +  ││LightGBM││problem   │
                                │LoRA/QLoRA│ │Few-shot││CatBoost││framing   │
                                └────────┘ └──────┘└───────┘└─────────┘
```
**When to choose Heuristic:** Simple rules cover 90%+ of cases, error tolerance is high, shipping speed beats marginal accuracy improvement.  
**When to choose Classical ML:** Structured tabular data, 1K-10K labeled examples, interpretability matters (SHAP values).  
**When to choose RAG:** No labeled data, knowledge is in documents, answer must be grounded in specific context with citations.  
**When to choose Fine-tuned LLM:** Need specific style/tone/task adaptation, have 100-1K high-quality examples, latency budget allows inference.

### Real-time vs Batch vs Streaming Inference

```
                     ┌──────────────────────────┐
                     │ START: Serving pattern    │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ P99 latency requirement?   │
                    └────┬──────────────────┬───┘
                         │ <100ms           │ >1 minute
                    ┌────▼──────┐    ┌──────▼──────────┐
                    │ User-facing│    │ Scheduled/nightly│
                    │ prediction?│    │ scoring?         │
                    └──┬────┬────┘    └──┬──────────┬────┘
                       │YES │NO        │YES       │NO
                  ┌────▼──┐ ┌▼───────┐ ┌▼────┐ ┌───▼──────┐
                  │Real-time│ │Embedded│ │Batch│ │Streaming │
                  │REST/gRPC│ │in DB  │ │Spark│ │Kafka +   │
                  │10-200ms │ │<1ms   │ │daily│ │<100ms    │
                  └─────────┘ └───────┘ └─────┘ └──────────┘
```
**When to choose Real-time API:** User-facing features (search, recommendations, chat), P99 < 200ms, use FastAPI/Triton with auto-scaling.  
**When to choose Batch:** Nightly reports, risk scoring, ETL enrichment — run Spark jobs, cost-efficient, millions/day.  
**When to choose Streaming:** Fraud detection, real-time personalization — Kafka + Flink, <100ms processing, sub-second freshness.  
**When to choose Embedded:** Scoring within SQL queries — ONNX Runtime in PostgreSQL, <1ms, no network overhead.

### RAG vs Fine-tuning vs Prompt Engineering

```
                     ┌──────────────────────────┐
                     │ START: LLM approach       │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Need model to learn new    │
                    │ style/tone/format/task?    │
                    └────┬──────────────────┬───┘
                         │ YES              │ NO
                    ┌────▼──────┐    ┌──────▼──────────┐
                    │ Have 100+  │    │ Need domain      │
                    │ high-quality│    │ knowledge from   │
                    │ examples?  │    │ documents?       │
                    └──┬────┬────┘    └──┬──────────┬────┘
                       │YES │NO        │YES       │NO
                  ┌────▼──┐ ┌▼────────┐┌─▼───┐ ┌───▼──────┐
                  │Fine-tune│ │Few-shot ││RAG  │ │Zero-shot │
                  │LoRA on │ │prompting││+ Vec│ │prompt    │
                  │1K+ exs │ │5-50 exs ││ DB  │ │only      │
                  └────────┘ └─────────┘└─────┘ └──────────┘
```
**When to choose RAG:** Knowledge changes faster than retraining, need citations/attribution, zero labeled data — Pinecone/Weaviate + embedding model.  
**When to choose Fine-tuning:** Teach a specific task/format persistently, have 100-1K high-quality examples, want cost reduction vs long prompts.  
**When to choose Few-shot:** 5-50 examples in prompt, model already capable but needs guidance, no training infrastructure.  
**When to choose Zero-shot:** Simple tasks with capable models (GPT-4, Claude), no examples needed, fastest path.

### Overfitting Diagnosis

```
                     ┌──────────────────────────┐
                     │ START: Model not          │
                     │ generalizing?             │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Train acc >> Val acc?      │
                    │ (gap > 5%?)               │
                    └────┬──────────────────┬───┘
                         │ YES              │ NO
                    ┌────▼──────┐    ┌──────▼──────────┐
                    │Overfitting│    │ Train ~= Val?    │
                    └──┬────────┘    └──┬──────────┬────┘
                       │               │YES       │NO (both low)
                  ┌────▼───────┐  ┌────▼────┐ ┌───▼──────────┐
                  │Regularize: │  │Metric   │ │Underfitting: │
                  │L1/L2,drop, │  │mismatch?│ │More capacity, │
                  │early stop, │  └──┬───┬───┘ │better features│
                  │more data   │     │YES│NO    │Reduce regul. │
                  └────────────┘  ┌──▼┐┌─▼────┐└──────────────┘
                                  │Fix││Check │
                                  │eval││data  │
                                  │met││quality│
                                  └───┘└──────┘
```
**When to increase regularization:** Train acc >> Val acc, high variance across CV folds — add L1/L2, dropout, early stopping, data augmentation.  
**When to increase capacity:** Both train and val are low — model too simple, underfitting. Add layers, reduce regularization, engineer better features.  
**When to audit data:** Perfect train, random val — likely data leakage or bad split. Audit time-based/group-based splits.

### Model Monitoring Thresholds

```
                     ┌──────────────────────────────┐
                     │ START: Production model       │
                     │ monitoring alert fired?       │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ PSI > 0.25 on critical feature?│
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼────────────┐  ┌──────▼──────────┐
                    │Data drift:      │  │ P99 latency >    │
                    │Trigger retrain, │  │ 2× SLA?         │
                    │investigate      │  └──┬──────────┬────┘
                    │upstream change  │     │YES       │NO
                    └─────────────────┘  ┌──▼────┐ ┌──▼──────────┐
                                         │Scale  │ │Pred error   │
                                         │up infra│ │rate > 5×    │
                                         │or model│ │baseline?    │
                                         │optimize│ └──┬──────┬───┘
                                         └────────┘    │YES   │NO
                                                   ┌───▼──┐ ┌─▼─────┐
                                                   │Concept│ │No     │
                                                   │drift: │ │action │
                                                   │Rollback│ │needed │
                                                   │+ retrain│ └──────┘
                                                   └───────┘
```
**When to trigger retrain:** PSI > 0.25 on any critical feature — data distribution shifted significantly. Investigate upstream pipeline first.  
**When to rollback:** Prediction error rate > 5× baseline for 15+ min — model performance collapsed. Immediate rollback to last known good.  
**When to scale infra:** P99 latency > 2× SLA — model isn't broken, infrastructure is. Add replicas, optimize model with quantization.

## Core Workflow
**(STANDARD)**

<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Problem Framing and Feasibility

1. **Frame the ML problem** — not every problem needs ML. Ask:
   - Is there a clear input → output mapping with historical examples?
   - Can a heuristic or rule-based system solve it with acceptable accuracy?
   - Is the cost of a wrong prediction acceptable? What's the error tolerance?
   - Do we have (or can we acquire) labeled data? How much? What's the label quality?

2. **Define success criteria before writing code:**
   - **Business metric**: what KPI does this model move? (revenue, retention, cost reduction)
   - **Model metric**: offline proxy for the business metric (precision@K, RMSE, ROC-AUC)
   - **Baseline**: current production performance — heuristic, previous model, or random
   - **Launch bar**: minimum improvement over baseline to justify deployment cost

3. **Decision tree for model selection:**

   ```
   Problem type?
   ├── Structured/tabular data (rows & columns)
   │   ├── Regression (predict number)       → XGBoost, LightGBM, CatBoost, Linear Regression
   │   ├── Binary classification              → XGBoost, LightGBM, Logistic Regression
   │   ├── Multi-class classification         → XGBoost, LightGBM, CatBoost
   │   ├── Time-series forecasting            → Prophet, ARIMA, Temporal Fusion Transformer, DeepAR
   │   └── Recommendation / ranking          → Two-tower models, Matrix Factorization, LightFM
   │
   ├── Unstructured data
   │   ├── Text
   │   │   ├── Classification/extraction     → Fine-tuned BERT/RoBERTa/DeBERTa, SetFit
   │   │   ├── Generation/summarization      → LLM (GPT-4, Claude, Llama, Mistral)
   │   │   ├── Semantic search               → Embeddings + vector DB (RAG)
   │   │   └── Translation                   → NLLB, M2M-100, fine-tuned mT5
   │   │
   │   ├── Images
   │   │   ├── Classification                 → ResNet, EfficientNet, ViT, fine-tune CLIP
   │   │   ├── Object detection               → YOLOv8, DETR, Faster R-CNN
   │   │   ├── Segmentation                   → SAM, Mask R-CNN, U-Net
   │   │   └── Generation                     → Stable Diffusion, DALL-E, Midjourney API
   │   │
   │   ├── Audio
   │   │   ├── Speech-to-text                 → Whisper, DeepSpeech
   │   │   ├── Text-to-speech                 → ElevenLabs, Bark, Tortoise-TTS
   │   │   └── Audio classification           → Wav2Vec2, AST, CLAP
   │   │
   │   └── Video                              → TimeSformer, VideoMAE, ViVit
   │
   └── Multi-modal
       └── Vision + Language                  → GPT-4V, Gemini, LLaVA, CogVLM, Fuyu
   ```

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.


## Best Practices

1. **Feature store over ad-hoc feature engineering.** Reusable features defined once and served consistently for training and inference prevent training/serving skew — the #1 cause of silent model degradation in production. Feast, Tecton, or a data warehouse-based feature store ensures the model sees the same feature computation path in both environments.

2. **Experiment tracking is non-negotiable — log everything.** Every training run gets a unique ID with: hyperparameters, dataset version, code commit hash, evaluation metrics, and environment. MLflow, Weights & Biases, or Neptune. Without this, you cannot reproduce results or debug production degradation. "I think this model was trained with learning_rate=0.001" is not a production posture.

3. **Model registry with staged lifecycle.** Models progress through: development → staging → production → archived. Each transition requires documented evaluation results and approval. MLflow Model Registry or Vertex AI Model Registry. Rollback to any previous version must be a single API call, not a code deploy.

4. **Training/serving skew detection is a production requirement.** Monitor feature distributions between training and serving data using KS-test, PSI, or Jensen-Shannon divergence. A model trained on summer data fails silently in winter if nobody checks for seasonal drift. Evidently AI, WhyLabs, or NannyML for drift monitoring.

5. **Hyperparameter tuning uses Bayesian optimization, not grid search.** Grid search is exponential in parameters — 5 params × 10 values = 100,000 combinations. Optuna/Hyperopt with TPE or Bayesian optimization converges on optimal values in 10x fewer trials. Reserve 20% of compute budget for the final training run with tuned parameters.

6. **Model cards for every production model.** Document: intended use, out-of-scope use cases, training data characteristics, evaluation results by subgroup, ethical considerations, and limitations. Model cards are a governance requirement under the EU AI Act and build organizational trust. Google's Model Card Toolkit or Hugging Face model cards.

7. **Bias and fairness evaluation before deployment, not after incidents.** Evaluate model performance across demographics (gender, race, age, geography). Disaggregated metrics reveal 95% overall accuracy hiding 70% accuracy for a minority subgroup. Use Fairlearn, AI Fairness 360, or What-If Tool.

8. **Shadow deployment before canary, canary before full rollout.** Deploy the new model in shadow mode (log predictions, don't serve them) for 1-2 weeks. Then canary to 5% of traffic and compare against production baseline. Gradual rollout catches performance regressions before they affect all users.

9. **GPU memory discipline — profile before training.** Use `torch.cuda.memory_summary()` or `nvidia-smi dmon` to profile memory usage. Batch size × sequence length × hidden dim determines memory footprint. OOM mid-training wastes hours of GPU time. Mixed precision (fp16/bf16) cuts memory in half with minimal accuracy loss for most architectures.

10. **LLM-specific: RAG over fine-tuning as the default, not the exception.** For most enterprise use cases, RAG provides grounded, updatable responses at lower cost than fine-tuning. Reserve fine-tuning for domain-specific behavior patterns that RAG cannot capture (tone, format, instruction-following style). Prompt engineering alone works for < 5 examples of desired behavior.

## Error Recovery
**(STANDARD)**
**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `data-engineer` | Feature computation schedules, historical backfill requirements, data quality expectations, schema contracts | Before building training pipelines or feature engineering workflows |
| `data-scientist` | Feature engineering insights, model evaluation metrics, training data quality assessment, statistical validation methods | Before selecting model architecture or designing evaluation harness |
| `mlops-engineer` | Model registry integration, CI/CD pipeline for ML, deployment infrastructure, monitoring stack | Before deploying models to production or setting up drift monitoring |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `data-scientist` | Model artifacts, feature engineering code, inference pipeline requirements, monitoring thresholds | Scientists can't productionize research — models stay in notebooks |
| `mlops-engineer` | Model serving API contract, GPU/CPU resource requirements, canary deployment strategy, drift detection rules | MLOps can't deploy models — no serving infrastructure configured |
| `llm-engineer` | RAG architecture patterns, embedding pipelines, prompt engineering frameworks, model evaluation harness | LLM applications lack foundation — hallucination and quality risks |

## Proactive Triggers

<!-- DEEP: 10+min — when to intervene before someone asks -->

| Trigger | Action | Why |
|---------|--------|-----|
| Data scientist hands off a Jupyter notebook with `model.fit()` and says "this is production-ready" | Propose structured training pipeline: data validation → feature engineering → training → evaluation → model registry; sync with `mlops-engineer` on CI/CD integration and `data-engineer` on feature computation | Notebooks are exploration artifacts, not production artifacts; a training pipeline ensures reproducibility, versioning, and automated validation — the notebook author won't be the one debugging it at 3 AM |
| Team wants to deploy an ML model but has no evaluation framework beyond accuracy | Propose multi-metric evaluation harness: per-class precision/recall, calibration (ECE), fairness metrics per protected group, slice-based evaluation, business simulation; sync with `data-scientist` on evaluation methodology | Accuracy alone hides critical failures: 95% accuracy on imbalanced data (5% positive class) means a "predict negative always" model scores 95%; slice-based evaluation catches "works for segment A, fails for segment B" before production |
| Product asks "can we add ML to predict user churn?" with no labeled data | Propose labeling strategy first: heuristic-based weak labels → active learning for edge cases → human review for quality; sync with `data-engineer` on label pipeline and `product-manager` on labeling budget | Labels are the most valuable ML asset — more impactful than model architecture choice; investing in labeling quality before model selection prevents garbage-in-garbage-out cycles |
| Feature engineering code exists in 3 different places: training script, batch inference, and real-time serving | Propose centralized feature engineering in feature store (Feast) with shared transformation logic; sync with `data-engineer` on feature computation pipeline and `mlops-engineer` on serving integration | Duplicated feature logic is the root cause of training-serving skew; centralized feature definitions with point-in-time correctness ensure identical computation in all environments |
| Team wants to fine-tune an LLM but has only 200 labeled examples | Recommend RAG before fine-tuning: retrieval-augmented generation solves 80% of LLM use cases with zero training; sync with `llm-engineer` on RAG architecture; fine-tune only for teaching new tasks/styles/reasoning patterns | Fine-tuning on 200 examples overfits to noise; RAG with good retrieval provides factually grounded responses without model retraining; fine-tuning is appropriate only when you need the model to learn a fundamentally new capability |
| Backend team needs model serving API but no contract exists for input/output schemas | Propose model serving API contract: input schema (feature names, types, ranges), output schema (prediction format, confidence scores, calibration), error codes; sync with `backend-developer` on API design and `mlops-engineer` on serving infrastructure | Without a serving contract, frontend/backend teams build against assumptions that break when the model changes; a versioned API contract decouples model iteration from consumer changes |
| Bias audit reveals model performs 30% worse for a protected demographic group | Propose bias mitigation pipeline: fairness metrics monitoring (demographic parity, equal opportunity), reweighting/resampling during training, threshold calibration per group; sync with `ai-safety-engineer` on fairness evaluation | A model that performs 30% worse for a protected group is a regulatory and ethical liability; fairness must be measured and mitigated before deployment, not discovered by users |
| Model evaluation shows strong offline metrics but team asks "will this actually work in production?" | Propose A/B testing framework with guardrail metrics: business KPIs (conversion, engagement) alongside model metrics (latency, error rate); shadow deployment before traffic cutover; sync with `mlops-engineer` on canary infrastructure | Offline evaluation measures model quality on historical data; A/B testing measures business impact on live users; a model with better offline metrics can still hurt business outcomes |


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## What Good Looks Like

> Every training run is reproducible: pinned dependencies, versioned datasets, seeded randomness, and a logged git hash.

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

## Deliberate Practice

```mermaid
graph LR
    A[Build] --> B[Measure<br/>failure modes] --> C[Study<br/>post-mortems] --> D[Re-build<br/>with constraints] --> A

```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Rebuild an existing system from scratch, then compare your design with the original | Monthly |
| **Competent** | Add a new constraint (10x data, zero downtime, etc.) to a familiar design and re-architect | Quarterly |
| **Expert** | Design the same system under 3 conflicting constraint sets; write a decision record for each | Quarterly |
| **Master** | Teach a junior to design a system; your role is to ask questions, not give answers | Monthly |

**The One Highest-Leverage Activity:** Every quarter, take a system you built 6+ months ago and redesign it from scratch with what you know now. Write down what changed and why.

## Anti-Patterns

- **Model checkpoint callbacks** trigger on every N steps, but if your training crashes at step 4,999 and checkpoint interval is 5,000 — you lose 4,999 steps of work. Also: `save_best_only=True` with a validation metric prevents saving intermediate checkpoints entirely. The best model may not be the last. **Total cost: $50-$500 per GPU-hour wasted — losing 4,999 steps on an 8×A100 cluster at $30/GPU-hour means $1,200-$12,000 in burned compute with zero recoverable output.**
- **`torch.no_grad()` doesn't mean zero memory** — tensors still accumulate on the computation graph if created inside `with torch.no_grad():` but used outside it with `requires_grad=True`. Inference memory leaks happen silently this way. **Total cost: $10-$100 per GPU-hour in wasted memory overhead — a slow memory leak that OOMs after 48 hours of inference on a $3/GPU-hour instance wastes $144 in compute and requires a restart that delays serving by hours.**
- **Mixed precision (float16) training** can produce NaN gradients when activation values exceed 65,504 (float16 max). Loss scaling (multiplying loss by 1024, dividing gradients) hides underflow but can't fix overflow. Monitor `grad_norm` — NaN gradients after a spike usually mean overflow. **Total cost: $100-$1,000 in wasted GPU time per failed run — a NaN at step 8,000 of a 10,000-step training run on 8×H100s at $25/GPU-hour wastes $4,500 in compute with no usable checkpoint.**
- **Transformer attention masks** — a mask of `0` means "attend to this token" in Hugging Face, but `0` means "ignore this token" in most PyTorch implementations. Mixing libraries silently inverts the attention pattern, producing models that attend to padding tokens instead of real content. **Total cost: $5,000-$50,000 in wasted training runs — a model trained with inverted attention masks converges to garbage, wasting an entire training budget before anyone notices the validation metrics are nonsensical.**
- **GPU memory fragmentation**: `empty_cache()` frees memory but doesn't defragment. After 100 cycles of allocating/deallocating different-sized tensors, you may have 4GB "free" but can't allocate a 2GB contiguous tensor. Restart the process or use `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`. **Total cost: $20-$200 per restart cycle — each fragmentation-induced OOM requires a full process restart on multi-GPU nodes, costing 5-15 minutes of idle GPU time at $20-$200 per node-hour depending on GPU tier.**

## Production Checklist
**(STANDARD)**

Before any model reaches production, verify ALL of:

1. Model card documented: intended use, out-of-scope use cases, training data characteristics, evaluation results by subgroup, ethical considerations, and limitations
2. Experiment tracking configured — every training run has: hyperparameters, dataset version, code commit hash, evaluation metrics, and environment
3. Model registered in model registry with staged lifecycle: development → staging → production → archived, with documented evaluation results at each transition
4. Training/serving skew monitoring deployed: KS-test or PSI on feature distributions between training and inference, alerting on drift
5. Shadow deployment completed for 1-2 weeks before canary: log predictions, compare against production baseline
6. Canary deployment to 5% traffic with automated comparison against production model, auto-rollback on regression
7. Bias and fairness evaluation across demographics completed: gender, race, age, geography — disaggregated metrics documented
8. Feature store serving features identically for training and inference — no duplicate feature computation paths
9. GPU memory profiling completed: batch size × sequence length verified to fit in available memory with headroom for gradients and optimizer states
10. Mixed precision (fp16/bf16) evaluated with loss scaling — NaN gradient monitoring enabled via grad_norm alerts
11. Hyperparameter tuning completed with Bayesian optimization — grid search considered insufficient justification for production
12. Inference latency and throughput benchmarks met: p50, p95, p99 latencies under SLO, throughput supports peak traffic × 1.5
13. Rollback plan verified: single API call to revert to previous model version, end-to-end rollback tested in staging
14. Monitoring dashboards live: prediction distribution, feature drift, latency, error rate, and business KPIs

## Scale Depth

| Scale | Scope & Complexity | Key Considerations |
|---|---|------|
| **Solo** | 1-2 models, personal projects or research | Jupyter notebooks with MLflow for experiment tracking. Single GPU (Colab, Lambda Labs, or local RTX). Manual deployment via Flask/FastAPI. Focus on reproducibility: every notebook cell runs top-to-bottom without modification. |
| **Small Team (2-10)** | 5-20 models, single business domain | MLflow or Weights & Biases for experiment tracking and model registry. Feature store (Feast lightweight). CI/CD pipeline for model training and deployment. Kubernetes or SageMaker for serving. Shadow + canary deployment pattern. |
| **Medium (10-100)** | 50+ models, multiple business domains | Centralized ML platform (Kubeflow, Vertex AI, SageMaker). Automated retraining pipelines triggered by data drift. Feature store with point-in-time correctness (Feast, Tecton). Model monitoring with automated rollback. MLOps maturity: Level 2 (automated CI/CD + continuous training). |
| **Enterprise (100+)** | 500+ models, multi-cloud/hybrid, regulatory compliance | Federated ML platform — central platform team owns infrastructure, domain teams own models. Real-time model monitoring with automated incident response. Model governance board for ethical review. EU AI Act compliance program. GPU cluster management with priority scheduling and cost allocation. |

**Transition Triggers:**
- Solo → Small Team: > 3 models requiring production serving; need for experiment tracking beyond spreadsheet
- Small Team → Medium: > 20 models across > 2 domains; need for shared feature store and automated retraining
- Medium → Enterprise: > 500 models or regulated industry requiring formal model governance and EU AI Act compliance

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| Training loss decreasing but validation loss increasing from epoch 3 | Overfitting — model memorizes training data, won't generalize | Add regularization (dropout, weight decay), reduce model capacity, increase training data, add data augmentation, early stopping with validation patience | The gap between training and validation loss is the generalization gap. A widening gap means your model is memorizing noise. |
| Model performs well in training but fails in production — same metrics, different data | Training/serving skew — feature computation differs between offline training pipeline and online inference pipeline | Audit feature computation code in both paths; implement feature store that serves identical transformations; monitor feature distribution drift (PSI > 0.1 is a warning) | The #1 cause of silent model failure in production. The model didn't degrade — it's solving a different problem than the one it was trained on. |
| GPU OOM during training even though batch_size × seq_len × hidden_dim fits in memory | Memory accounting ignores optimizer states and gradients — Adam stores 2× parameters (m, v), amortized gradients use memory, and activation checkpointing adds overhead | Reduce batch size, enable gradient checkpointing, use mixed precision (fp16 cuts memory ~50%), use DeepSpeed ZeRO or FSDP for distributed training | Allocated memory = model params + gradients + optimizer states + activations. The model parameters are only ~1/4 of total memory: 1× params + 1× gradients + 2× Adam states + N× activations. |
| NaN loss at step 4,500 of training | Gradient explosion or fp16 overflow — activation values > 65,504 exceed float16 max | Enable gradient clipping (max_norm=1.0), switch to bf16 (wider range), add loss scaling, monitor grad_norm and alert on spikes | NaN after thousands of steps usually means a rare input triggered an extreme activation. Log the input batch when NaN occurs for root cause analysis. |
| Model deployed but prediction latency 10x higher than benchmark | Inference was benchmarked on GPU with batch_size=64 but production serves single requests on CPU; different hardware and batching pattern | Benchmark on production hardware with production batch sizes; use ONNX Runtime or TensorRT for optimization; consider model distillation for latency-sensitive deployments | Inference benchmarks must match production conditions. A model that runs in 10ms with batching on A100 can take 200ms for single requests on CPU. |
| Bias audit reveals model is 30% less accurate for minority subgroup | Training data underrepresenting the subgroup; proxy variables (e.g., ZIP code correlating with race) leaking protected attributes | Oversample underrepresented groups, remove proxy variables, apply fairness constraints during training (Fairlearn, AIF360), evaluate disaggregated metrics before deployment | Models learn the biases in your data. A "99% accurate" model that fails for 10% of your users is not ready for production. |
| Experiment tracking shows 50 runs, MLflow server is slow, "which run was production?" | No naming convention, no tagging, no lifecycle status. Every run is named `run_20240315_142432` and nobody knows which is which. | Implement naming convention: `{model}-{dataset_version}-{description}`. Tag every run with status (production, staging, deprecated, experiment). Archive runs > 30 days old with no status tag. | Experiment tracking without naming discipline is worse than no tracking — it creates the illusion of traceability without actually enabling it. |

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "Prompt injection is the user's problem, not our infrastructure" | Prompt injection is the #1 OWASP for LLM apps; every input field — user text, uploaded files, webpage summaries, tool outputs — is an untrusted attack vector that crosses system boundaries |
| "We'll fine-tune a smaller model to match GPT-4 quality and save costs" | Distillation and fine-tuning recover ~70-80% of teacher quality on benchmark tasks but lose emergent reasoning, instruction-following nuance, and safety alignment — the gap widens on out-of-distribution inputs |
| "RAG solves hallucination, we don't need factuality guardrails beyond retrieval" | RAG reduces but doesn't eliminate hallucination; models override retrieved context with parametric knowledge, synthesize across documents incorrectly, and cite sources that contradict their own output |
| "We evaluate on the same metrics the foundation model paper reports, so we're covered" | Foundation model benchmarks (MMLU, HumanEval, GSM8K) measure general capability, not task-specific reliability — your medical Q&A, code generation, or customer-facing app needs domain-grounded evals |
| "Chain-of-thought improves accuracy, so we should always use it" | CoT increases latency 3-10x and cost proportionally; for classification, extraction, and routing tasks it adds no accuracy and wastes compute — reasoning is a tool, not a default |


## Verification

- [ ] Training runs to completion without NaN loss or exploding gradients — monitor `grad_norm` throughout
- [ ] Validation loss plateaus (not decreasing AND not increasing) — no overfitting signal
- [ ] Checkpoint saved and can be loaded: `model = load_from_checkpoint('best.ckpt')` succeeds
- [ ] Inference test: run inference on 100 samples — output shape correct, values in expected range (e.g., probabilities in [0, 1])
- [ ] GPU memory: `nvidia-smi` shows memory usage < 90% of GPU RAM — no OOM risk during peak batch
- [ ] Reproducibility: train twice with same seed — metrics within 1% (GPU non-determinism tolerance)

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## References

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Scale Depth**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)

