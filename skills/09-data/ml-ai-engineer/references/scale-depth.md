# Scale Depth

<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
One data scientist/ML engineer handling end-to-end. Use notebook for exploration, scikit-learn/XGBoost for training, pickle for serialization, Flask endpoint for serving. No feature store, no experiment tracking beyond CSV, no CI/CD for models. Batch predictions only. Stick to tabular models; avoid deep learning unless you have a pretrained model. Cost: $0-300/month (Colab Pro, small GPU VM). Overkill: Kubernetes, model registry, drift monitoring, feature stores, distributed training.

### Small (2-10 people, 100-10K users)
Dedicated ML engineer. MLflow for experiment tracking (self-hosted Docker). Model registry with staging/production gates. Start using feature store (Feast) when >10 models share features. Deep learning with single GPU (RTX 4090 or T4). W&B or TensorBoard. CI/CD: GitHub Actions with minimal test suite. A/B testing framework for deployment validation. Basic drift monitoring (prediction distribution). Cost: $1K-5K/month. Overkill: Kubeflow, Airflow for ML pipelines, multi-GPU training, real-time feature serving.

### Medium (10-50 people, 10K-1M users)
ML platform team (2-3). Kubeflow/MLflow Pipelines for orchestration. Feature store with online serving (Redis/DynamoDB). Real-time inference with auto-scaling (Kubernetes + HPA). Comprehensive monitoring: PSI, concept drift via NannyML/Evidently. Model cards for all production models. CI/CD pipeline: data validation → training → eval → registry → canary → full promotion. Multi-GPU training for CV/NLP. A/B + multi-armed bandits. Cost: $10K-50K/month. Overkill: full MLOps platform team (save that for enterprise), distributed training across >8 GPUs.

### Enterprise (50+ people, 1M+ users)
ML platform team (5-10). Multi-tenant feature store. Distributed training (FSDP, DeepSpeed, Ray). GPU cluster with job scheduler (SLURM, Kubernetes + GPU operator). LLM fine-tuning pipeline with LoRA/QLoRA. Comprehensive MLOps: automated retraining triggers, shadow deployments, chaos testing for ML. Federated governance: model risk scoring, bias audits, regulatory compliance (EU AI Act). FinOps: GPU utilization tracking, spot instance orchestration, chargeback. Cost: $100K-1M+/month.

### Transition Triggers
| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | 3+ models in production or >2 team members collaborating | Add MLflow for experiment tracking; implement A/B testing |
| Small → Medium | 10+ models, real-time inference needed, or >5 ML engineers | Add feature store (Feast); implement drift monitoring (NannyML); build ML platform |
| Medium → Enterprise | Per-model cost >$50K/month, distributed training needed, regulatory audits required | Build ML platform team; implement federated governance; add compliance infrastructure |
