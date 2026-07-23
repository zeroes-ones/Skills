# Scale Depth: Solo → Small → Medium → Enterprise

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
