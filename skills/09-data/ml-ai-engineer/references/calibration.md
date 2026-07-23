# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can fine-tune a model in a Jupyter notebook and get great validation metrics but don't know what happens when 1,000 users hit it simultaneously | You can deploy a model with CI/CD (data validation → training → evaluation → canary → rollback), drift monitoring, and automated retraining — and you've run a live traffic cutover | You can look at an ML system in production for 10 minutes and identify whether the next failure will be data drift, serving infrastructure, or model degradation — then fix it before it happens |
| You train a model, export `model.pkl`, and email it to the backend team with "just load this and call `.predict()`" | You've shipped a model to production with a feature store, online/offline consistency checks, shadow scoring, and a rollback plan that was actually tested | You design the ML platform for a 50-person data science org — and 12 months later, 30 models are in production, model deployments happen in <1 hour, and no model caused a P0 incident |
| You've never run a red-team exercise and you think safety testing is "the compliance team's job" | You've red-teamed a model before launch, documented the failure modes, and implemented guardrails (input filtering, output filtering, topic classifiers) | A regulator asks "How do you know this model is safe?" and you can show them the red-team report, the guardrail architecture, the monitoring dashboard, and 6 months of safety metrics — and they're satisfied |

**The Litmus Test:** Can you take a model from a Jupyter notebook to production — feature pipeline, training pipeline, model registry, A/B evaluation, serving infrastructure, monitoring, rollback plan — entirely on your own? If any step requires another person or team, and you can't do it yourself, you're not L3 yet.
