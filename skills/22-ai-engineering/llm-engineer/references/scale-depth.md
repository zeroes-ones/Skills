# Scale Depth: Solo → Small → Medium → Enterprise

<!-- DEEP: 10+min -->

### Solo (1 person, 0-100 users)
- **What changes**: Use managed services (OpenAI API, Pinecone serverless). Fixed-size chunking. Static few-shot. Basic content filter (OpenAI Moderation). No A/B testing. Manual evaluation on 50 examples.
- **What to skip**: Self-hosted models, multi-agent architectures, fine-tuning, semantic caching, custom guardrails, NeMo, evaluation pipelines, CI/CD for prompts.
- **Coordination**: You are the engineer, evaluator, and safety reviewer. Document prompt versions in git.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Prompt versioning in git with changelog. Automated LLM-as-judge evaluation (weekly). Semantic caching (GPTCache). Basic guardrails (OpenAI Moderation + regex PII). RAGAS for RAG evaluation. A/B testing on prompt changes.
- **What to skip**: Self-hosted embedding models, multi-agent architectures, NeMo Guardrails, fine-tuning infrastructure, model distillation.
- **Coordination**: Prompt changes reviewed by peer. Evaluation results shared in team channel. Safety incidents tracked in issue tracker.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Full RAG pipeline with semantic/recursive chunking. Prompt CI/CD with automated eval gates. LLM-as-judge + periodic human eval correlation checks. Custom guardrails with NeMo or equivalent. Function calling with structured output (Instructor). Multi-model routing. Fine-tuning with LoRA for domain adaptation. Streaming optimization.
- **What to skip**: Full multi-agent debate architecture. Tree-of-thought for all queries. Self-hosted GPU clusters. Custom embedding model training.
- **Coordination**: LLM outputs reviewed by ai-safety-health-reviewer for medical/legal domains. MLOps team monitors drift. Weekly prompt performance review.

### Enterprise (50+ people, 1M+ users)
- **What changes**: All of the above plus: multi-agent architectures for complex workflows. Custom fine-tuned models with QLoRA. Self-hosted inference (vLLM, Triton). Custom embedding models. Real-time hallucination detection (NLI-based). Full NeMo guardrails with custom Colang flows. Semantic cache with 50%+ hit rate. Tree-of-thought for high-stakes reasoning. Red teaming for prompt injection and jailbreak attempts.
- **What's full production**: 24/7 evaluation pipeline. Real-time drift monitoring. Multi-region deployment. SOC 2 + HIPAA compliance. Automated regression testing for every prompt change. Model cards for every deployed model.
- **Coordination**: Cross-functional review board (engineering, legal, safety) for LLM features. Monthly safety audit. Incident response playbook for LLM failures.

### Transition Triggers
- **Solo → Small**: First production LLM feature. User complaint about hallucinated output. Latency >2s TTFT.
- **Small → Medium**: >10K daily LLM calls. Enterprise customer requiring SLAs. First safety incident requiring root cause analysis.
- **Medium → Enterprise**: Regulatory scrutiny (healthcare, finance, legal). >1M daily LLM calls. Competitor breach involving LLM safety failure.
