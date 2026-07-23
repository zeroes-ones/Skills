# Core Workflow — Full Implementation

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


**What good looks like:** ML pipeline reproducible from raw data to deployed model. Feature store serves consistent features for training and inference. Model monitoring tracks prediction drift, data drift, and performance metrics. A/B test framework compares model versions. Training pipeline completes in under 2 hours.

4. **Data requirements by approach:**
   | Approach                     | Minimum Labeled Data | Notes                                    |
   |------------------------------|---------------------|------------------------------------------|
   | Heuristic / rules            | 0                   | Baseline; often surprisingly good        |
   | Classical ML (XGBoost)       | 1K–10K              | Great with well-engineered features      |
   | Fine-tune BERT/RoBERTa       | 1K–10K              | Use SetFit for <100 examples per class   |
   | Fine-tune LLM (LoRA)         | 100–1K              | High-quality examples matter most        |
   | RAG (no fine-tuning)         | 0 labeled, docs needed | Embed documents, retrieve, prompt     |
   | Few-shot LLM prompt          | 5–50                | In-context examples in the prompt        |
   | Zero-shot LLM prompt         | 0                   | Relies entirely on model's pre-training  |

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): Data Preparation

1. **Data collection and labeling:**
   - Audit data sources: transactional DBs, event streams, logs, third-party APIs, human labelers
   - Establish labeling guidelines with edge cases; inter-annotator agreement (Cohen's κ > 0.7)
   - Use weak supervision (Snorkel) or active learning when labels are expensive
   - For LLM fine-tuning: curate diverse, high-quality examples; quality >> quantity

2. **Exploratory Data Analysis (EDA):**
   - Univariate: distributions, missing rates, cardinality, skew, outliers
   - Bivariate: correlations, mutual information, feature interactions
   - Target analysis: class imbalance, distribution shape, temporal patterns
   - **CRITICAL**: check for target leakage — any feature that contains information about the target unavailable at prediction time (e.g., using `days_since_last_purchase` to predict churn when your label is "churned on day X")

3. **Feature engineering patterns:**
   | Data Type           | Encoding Strategy                                                        |
   |---------------------|--------------------------------------------------------------------------|
   | Numeric              | StandardScaler (normal dist), RobustScaler (outliers), QuantileTransformer |
   | High-cardinality cat | Target encoding (with smoothing), CatBoost built-in                      |
   | Low-cardinality cat  | One-hot (≤10 categories), Ordinal (ordered), Binary (2 categories)       |
   | Text                 | TF-IDF (classic ML), embeddings (deep learning), count vectorizer        |
   | Datetime             | Cyclical encoding (sin/cos of hour, day, month), lag features, rolling stats |
   | Geo                  | Geohash, H3 hex, distance to POI, cluster assignment                   |

4. **Handling missing data — in order of preference:**
   1. Understand WHY data is missing (MCAR, MAR, MNAR) — this determines the fix
   2. Delete: if column >60% missing and not critical, drop it
   3. Impute: median (skewed), mean (normal), mode (categorical), KNN, MICE, or model-based
   4. Add indicator flag: create `feature_is_missing` binary column — the absence itself can be signal
   5. Use models that handle missing natively: XGBoost, LightGBM, CatBoost

5. **Train / Validation / Test split — do NOT get this wrong:**
   - **Time-based split**: for time-series or any data with temporal dependency, split chronologically (train on past, test on future) — random split leaks future into training
   - **Group-based split**: if observations share a group (user, session, hospital), keep all of a group in ONE split — cross-group contamination inflates metrics
   - **Stratified split**: maintain class distribution across splits for imbalanced problems
   - **Standard split ratio**: 70/15/15 or 80/10/10 for datasets >10K; 60/20/20 for small datasets
   - **Never tune hyperparameters on the test set** — test set is touched exactly once at the very end

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): Model Development and Training

1. **Start with a strong baseline before complex models:**
   - Simple heuristic: "always predict the majority class", "predict yesterday's value"
   - Linear/logistic regression with basic features
   - LightGBM with default hyperparameters
   - **Rule**: if your complex model doesn't beat a simple baseline by >5%, fix your data or reframe the problem

2. **Hyperparameter tuning strategy:**
   ```
   Stage 1: Coarse grid search (3-5 values per param) → find promising region
   Stage 2: Bayesian optimization (Optuna, Hyperopt) in the promising region
   Stage 3: Manual fine-tuning on the most sensitive parameters
   
   Priority order (most impactful first):
   - Learning rate
   - Model complexity (max_depth, n_estimators, num_layers)
   - Regularization (lambda, alpha, dropout, weight_decay)
   - Batch size (affects convergence, not final quality)
   ```

3. **Cross-validation strategy by data type:**
   | Data Characteristic  | CV Strategy                                     |
   |----------------------|--------------------------------------------------|
   | IID (independent)    | 5-fold stratified K-fold                         |
   | Time-series          | TimeSeriesSplit (expanding window) or blocked CV |
   | Grouped              | GroupKFold — groups never split across folds     |
   | Small dataset (<1K)  | Leave-One-Out or 10× repeated 5-fold             |
   | Large dataset (>1M)  | Single holdout validation set is sufficient      |

4. **Detecting and fixing overfitting:**
   | Symptom                         | Fix                                                       |
   |---------------------------------|-----------------------------------------------------------|
   | Train >> Val accuracy           | Add regularization (L1/L2, dropout), reduce model capacity |
   | Val loss increasing, train flat | Early stopping with patience=5-10 epochs                  |
   | Perfect train, random val       | Data leakage — audit your split and features              |
   | High variance across CV folds   | More data, reduce model complexity, ensemble methods      |

5. **Regularization cheat sheet:**
   - **L1 (Lasso)**: feature selection — drives coefficients to exactly zero
   - **L2 (Ridge)**: prevents any single coefficient from dominating
   - **ElasticNet**: combines L1 + L2; best default for linear models
   - **Dropout**: for neural nets; 0.2 input layer, 0.5 hidden layers
   - **Weight decay**: modern alternative to L2 in deep learning
   - **Early stopping**: stop training when validation metric stops improving
   - **Data augmentation**: best regularizer — more (real) data always wins

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): Evaluation

1. **Classification metrics — choose the right one:**
   | Use Case                            | Primary Metric    | Secondary Metric  |
   |-------------------------------------|-------------------|-------------------|
   | Balanced classes                    | Accuracy          | Log-loss          |
   | Imbalanced, care about positives    | Precision-Recall AUC | F1-score       |
   | Imbalanced, care about ranking      | ROC-AUC           | PR-AUC            |
   | Fraud detection (rare positives)    | Precision@K       | Recall@K          |
   | Medical diagnosis (don't miss)      | Recall (sensitivity) | NPV            |
   | Spam detection (don't false-alarm)  | Precision         | FPR               |
   | Multi-class                         | Macro F1          | Weighted F1       |

2. **Regression metrics:**
   | Use Case                | Metric | Interpretation                                   |
   |-------------------------|--------|--------------------------------------------------|
   | General purpose         | RMSE   | Penalizes large errors heavily; in target units  |
   | Outlier-heavy targets   | MAE    | Less sensitive to outliers; in target units      |
   | Scale-invariant         | MAPE   | Percentage error; fails when y=0                 |
   | Understand variance     | R²     | Proportion of variance explained; 1.0 is perfect |

3. **Ranking/Recommendation metrics:**
   - **NDCG@K**: normalized discounted cumulative gain — rewards relevant items at top ranks
   - **MAP@K**: mean average precision — treats ranking as binary relevance at each position
   - **MRR**: mean reciprocal rank — good for "find the one right answer" tasks
   - **Hit Rate@K**: fraction of users with at least one relevant item in top K

4. **Beyond aggregate metrics — slice-based evaluation:**
   - Segment by user demographics, geography, plan tier, device type, acquisition channel
   - Report worst-performing slice alongside overall metric
   - **Rule**: if any slice with >5% of traffic performs significantly worse, fix before launch

5. **LLM-specific evaluation:**
   | Capability         | Eval Framework/Tool          | Example Metric              |
   |--------------------|------------------------------|-----------------------------|
   | Code generation    | HumanEval, MBPP, SWE-bench   | pass@k                      |
   | General knowledge   | MMLU, ARC, HellaSwag         | Accuracy                    |
   | Summarization      | ROUGE, BERTScore, SummEval   | ROUGE-L, BERTScore F1       |
   | RAG quality        | RAGAS, TruLens, DeepEval     | Faithfulness, Relevance     |
   | Safety             | Anthropic eval, custom       | Refusal rate, harm score    |
   - **LLM-as-judge pattern**: use a stronger LLM (GPT-4, Claude Opus) to evaluate outputs of a weaker model
   - Always validate LLM-as-judge against human ratings (correlation >0.7)

<!-- DEEP: 10+min -->
### Phase 5 (~25 min): MLOps Infrastructure

1. **Experiment tracking — log everything:**
   - Tooling: MLflow, Weights & Biases, Neptune, Comet ML
   - Log for every run: git commit hash, dataset version/hash, hyperparameters, metrics (train+val), artifacts (model, plots, config), environment (requirements.txt or conda env export)
   - Naming convention: `{model_name}_{date}_{git_short_hash}_{brief_description}`
   - Tag runs: `baseline`, `best_so_far`, `production_candidate`, `failed`

2. **Feature Store — training/serving parity:**
   - **Offline store**: historical features for training (data warehouse, parquet, Delta Lake) — batch, high-throughput
   - **Online store**: low-latency features for inference (Redis, DynamoDB, Bigtable) — <10ms P99
   - Tools: Feast, Tecton, Hopsworks, or custom with point-in-time correct joins
   - **The cardinal rule**: feature transformation logic is defined ONCE and reused in training and serving — if you write it twice, they WILL diverge

3. **Model Registry — manage the lifecycle:**
   - Stages: `staging` → `production` → `archived`
   - Store: model artifact (pickle, ONNX, saved_model), environment spec, metrics, training dataset reference
   - Promotion requires: passing eval gate, approval from model owner, documented release notes
   - Archive old models; never delete — you need them for rollback and audit

4. **CI/CD for ML — distinct from software CI/CD:**
   ```
   Trigger: new training data available OR scheduled retrain OR code change
   
   Pipeline stages:
   1. Data validation (Great Expectations, TFX Data Validation)  → schema, stats, drift check
   2. Feature computation (point-in-time correct)                → push to offline feature store
   3. Model training (with experiment tracking)                  → log to MLflow/W&B
   4. Model evaluation (offline metrics, slicing, fairness)      → gate: pass/fail
   5. Model registration (if gate passed)                        → registry stage: staging
   6. Shadow/canary deployment                                   → smoke test on live traffic
   7. Full promotion (if shadow metrics OK)                      → registry stage: production
   ```

<!-- DEEP: 10+min -->
### Phase 6 (~25 min): Model Serving

1. **Deployment patterns — choose based on latency and throughput:**
   | Pattern              | Latency    | Throughput   | Best For                             |
   |----------------------|------------|--------------|--------------------------------------|
   | Real-time REST/gRPC  | 10–200ms   | 100–10K QPS  | User-facing predictions              |
   | Batch inference      | Minutes-Hrs| Millions/day | Nightly scoring, report generation   |
   | Streaming            | <100ms     | 100K+ QPS    | Fraud detection, recommendations     |
   | Edge / on-device     | <10ms      | Per-device   | Mobile, IoT, offline-capable         |
   | Embedded in DB       | <1ms       | Query-bound  | Scoring within SQL queries           |

2. **Serving infrastructure:**
   - **Frameworks**: FastAPI (simple), Ray Serve (distributed), Triton Inference Server (high-perf, multi-framework), BentoML (packaging), Seldon Core/KFServing (Kubernetes-native)
   - **GPU serving**: use Triton with dynamic batching, model concurrency, and instance groups; NVIDIA MIG for GPU partitioning
   - **CPU serving**: ONNX Runtime or OpenVINO — 2–10× speedup over native PyTorch/TF; quantized INT8 models
   - **Auto-scaling**: based on request latency (P99 < target) and queue depth; pre-warm on deploy

3. **Model optimization for inference:**
   | Technique          | Speedup | Accuracy Cost | When to Use                          |
   |--------------------|---------|---------------|--------------------------------------|
   | ONNX export         | 1.5–3×  | None          | Always — first step                  |
   | INT8 quantization   | 2–4×    | <1%           | CPU deployment, edge devices         |
   | FP16 inference      | 2×      | Negligible    | GPU deployment (Ampere+)             |
   | Pruning             | 1.5–3×  | 0.5–2%        | Large models, GPU bound              |
   | Knowledge distillation| 2–10× | 1–5%          | Replace large model with small       |
   | Operator fusion     | 1.2–1.5×| None          | Always — part of ONNX/TensorRT       |
   | FlashAttention      | 2–4×    | None          | Transformer inference (GPU)          |

4. **Batching strategies:**
   - **Dynamic batching**: server waits N ms to accumulate requests, processes them as a batch — balances latency vs throughput
   - **Ragged batching**: for variable-length sequences — pad to max in batch, mask attention — as opposed to padding all to model max
   - **Continuous batching** (aka iteration-level scheduling): for LLMs — don't wait for all sequences in a batch to finish before adding new ones; vLLM, TensorRT-LLM

<!-- DEEP: 10+min -->
### Phase 7 (~25 min): LLM Patterns

1. **Prompt engineering — fundamental patterns:**
   - **Zero-shot**: just ask; works for simple tasks with capable models
   - **Few-shot**: provide 3–8 examples in the prompt; format input→output pairs consistently
   - **Chain-of-thought (CoT)**: add "Let's think step by step" — forces the model to reason before answering; 10–30% improvement on reasoning tasks
   - **Tree-of-thought (ToT)**: explore multiple reasoning paths, evaluate each, backtrack — for complex planning
   - **ReAct**: interleave Reasoning and Action — model decides to use a tool, sees result, reasons further
   - **Structured output**: request JSON, XML, or function-call format; constrain with grammar (guidance, outlines, lm-format-enforcer)

2. **RAG Architecture — retrieval-augmented generation:**
   ```
   ┌──────────────┐    ┌───────────────┐    ┌──────────────┐
   │ Document      │───▶│ Chunking       │───▶│ Embedding     │
   │ Ingestion     │    │ Strategy       │    │ Model         │
   └──────────────┘    └───────────────┘    └──────┬───────┘
                                                    │
                                              ┌─────▼───────┐
   ┌──────────────┐    ┌───────────────┐    │ Vector DB    │
   │ User Query    │───▶│ Query          │───▶│ (Pinecone,   │
   │               │    │ Transformation │    │  Weaviate,   │
   └──────────────┘    └───────────────┘    │  pgvector)   │
                                             └──────┬───────┘
   ┌──────────────┐    ┌───────────────┐           │
   │ Final Answer  │◀───│ LLM Generation │◀─────────┘
   │ (with cites)  │    │ + Prompt       │    Retrieved Chunks
   └──────────────┘    └───────────────┘
   ```
   Key decisions:
   - **Chunking**: size 256–1024 tokens; overlap 10–20%; prefer semantic (sentence-boundary-aware) over fixed-length
   - **Embedding model**: `text-embedding-3-large` (OpenAI, 3072d), `embed-english-v3.0` (Cohere, 1024d), `bge-large-en-v1.5` (BGE, 1024d, open-source), `e5-mistral-7b-instruct` (Microsoft, 4096d, SOTA open-source)
   - **Vector DB**: Pinecone (managed, fast, $$), Qdrant (OSS, fast, Rust), Weaviate (OSS, hybrid search built-in), pgvector (PostgreSQL extension, simple), Milvus (OSS, distributed, GPU indexing)
   - **Retrieval**: dense (cosine similarity on embeddings) + sparse (BM25/Splade for keyword match); hybrid with reciprocal rank fusion
   - **Reranking**: cross-encoder (`bge-reranker-v2-m3`, Cohere Rerank v3) scores (query, chunk) pairs — improves recall substantially

3. **Fine-tuning LLMs — when and how:**
   | Scenario                          | Approach                          |
   |-----------------------------------|-----------------------------------|
   | Add knowledge (docs, facts)       | **RAG** — don't fine-tune         |
   | Teach style/tone/format           | **Fine-tune** — 100–1K examples   |
   | Teach a new task/skill            | **Fine-tune** — 1K–10K examples   |
   | Both knowledge + task             | **RAG + fine-tune** — combine     |
   | Hard reasoning, math, code        | **Fine-tune** — need high-quality data |

   **LoRA / QLoRA parameters — starting points:**
   - `r` (rank): 8–64; higher = more capacity but more VRAM; 16 is a safe default
   - `alpha`: usually 2× r; scaling factor for the LoRA weights
   - `target_modules`: all linear layers for best quality; `["q_proj", "v_proj"]` for memory efficiency
   - `lora_dropout`: 0.05–0.1
   - QLoRA: 4-bit NF4 quantization with double quantization — fine-tune 70B models on a single 48GB GPU

4. **Agent patterns:**
   - **ReAct agent**: LLM generates Thought → Action → Observation → Thought → ... → Final Answer
   - **Tool-use / function calling**: LLM outputs structured JSON to invoke tools (search, calculator, DB query, API call)
   - **Plan-and-execute**: LLM first creates a plan (list of steps), then executes each step with tool calls
   - **Multi-agent**: separate LLM instances with different roles (researcher, coder, critic) collaborating
   - **Guardrails**: validate tool inputs, timeouts on tool execution, max iterations, human approval for destructive actions

<!-- DEEP: 10+min -->
### Phase 8 (~30 min): Monitoring and Observability

1. **Drift detection — the silent killer:**
   | Drift Type         | What Changes             | Detection Method                           |
   |--------------------|--------------------------|--------------------------------------------|
   | Data drift         | Input feature distribution | KS test, PSI, Jensen-Shannon distance    |
   | Concept drift      | P(Y|X) relationship      | Monitor prediction error over time         |
   | Prediction drift   | Model output distribution | Compare to training distribution           |
   | Label drift        | Ground truth distribution | Requires delayed labels; monitor after arrival |

   - **Reference window**: last 7 days of training data distribution
   - **Analysis window**: current production data distribution (rolling)
   - **Threshold**: PSI > 0.2 triggers investigation; PSI > 0.25 triggers retrain pipeline
   - Tools: Evidently AI, NannyML, Whylogs, Great Expectations, custom with scipy stats

2. **Performance monitoring:**
   - **Online metrics** (require labels): accuracy, precision, recall, RMSE — computed when ground truth arrives (delayed by hours/days)
   - **Proxy metrics** (no labels needed): prediction distribution stability, % null predictions, avg prediction magnitude, % predictions in valid range
   - **Infrastructure metrics**: latency (P50, P95, P99), throughput (QPS), error rate (4xx, 5xx), GPU utilization, queue depth

3. **Alerting — page on symptoms:**
   - Prediction error rate > 5× baseline for >15 minutes → page on-call
   - Data drift PSI > 0.3 on any critical feature → create ticket
   - Serving latency P99 > 2× SLA for >5 minutes → page on-call
   - % null inputs > 10% (and previously near 0%) → page on-call (likely upstream data pipeline failure)

<!-- DEEP: 10+min -->
### Phase 9 (~20 min): Responsible AI

1. **Fairness metrics — measure before launch:**
   | Metric                    | Definition                                                      |
   |---------------------------|-----------------------------------------------------------------|
   | Demographic parity        | P(positive|group A) = P(positive|group B)                       |
   | Equal opportunity         | TPR same across groups                                          |
   | Equalized odds            | TPR and FPR same across groups                                  |
   | Disparate impact ratio    | ratio of positive rates; <0.8 indicates adverse impact (US legal) |

2. **Explainability:**
   - **SHAP**: game-theoretic feature importance; works for any model; global + local explanations
   - **LIME**: local surrogate models; faster than SHAP, less theoretically grounded
   - **Integrated Gradients**: for neural networks; attribute prediction to input features
   - **Attention visualization**: for transformers — shows which tokens the model attended to
   - **LLM explainability**: ask the model to explain its reasoning; chain-of-thought as explanation

3. **Safety guardrails for LLM applications:**
   - **Input guard**: classify and block harmful inputs (Llama Guard, OpenAI Moderation API, custom classifier)
   - **Output guard**: detect hallucinations (verify claims against retrieved context), filter toxic content, enforce format
   - **Prompt injection defense**: separate instructions from user data (use special delimiters), input sanitization, rate limiting
   - **Red-teaming**: systematically attempt to break safety controls; both automated (Garak, promptfoo) and human
   - **Model cards**: document intended use, limitations, training data, evaluation results, and fairness assessment

4. **Cost optimization:**
   | Layer          | Strategy                                                       | Savings |
   |----------------|----------------------------------------------------------------|---------|
   | Training       | Spot/preemptible instances, mixed precision, gradient accumulation | 40–70% |
   | Serving (GPU)  | Continuous batching (vLLM), quantization (INT8/INT4), model distillation | 50–90% |
   | Serving (CPU)  | ONNX Runtime, quantization, caching frequent responses         | 30–60% |
   | LLM APIs       | Prompt compression, shorter context, tiered models (GPT-4→3.5 for simple tasks), prompt caching | 30–80% |
   | Embeddings     | Cache embeddings; don't re-embed unchanged documents           | 50–90% |
   | Vector DB      | Dimension reduction (PCA), scalar quantization, disk-based index for cold data | 30–60% |


### Cross-skills Integration
```bash
# Statistical models → ML productionization → API integration
/data-scientist && /ml-ai-engineer && /backend-developer
# Data pipelines → ML training → Security review
/data-engineer && /ml-ai-engineer && /security-engineer
# Data scientists develop models. ML engineers productionize and monitor. Backend devs integrate. Security reviews for safety.
```
