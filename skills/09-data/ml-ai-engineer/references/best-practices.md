# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Start with the simplest thing that could possibly work**: heuristic → linear model → XGBoost → deep learning → LLM. Each step must justify the added complexity with measured improvement.
- **Your eval is your spec**: invest heavily in evaluation; a bad eval lets bad models through and blocks good ones. Multi-metric, multi-slice, multi-segment.
- **Training-serving skew is the #1 production ML bug**: identical preprocessing, identical feature logic, identical data distribution expectations. Test for it explicitly in CI.
- **Reproducibility is not optional**: seed everything (`random`, `numpy`, `torch`, `cudnn`), pin dependencies, version datasets, log git hash. You will need to reproduce a 6-month-old run.
- **RAG before fine-tuning**: 80% of LLM use cases are solved with good retrieval. Fine-tune only when you need to teach the model a new style, task, or reasoning pattern.
- **Monitor from day one**: if you can't measure degradation, you can't fix it. At minimum: prediction distribution drift, serving latency, error rate.
- **Labels are your most valuable asset**: invest in labeling quality, consistency, and coverage before investing in model architecture.
