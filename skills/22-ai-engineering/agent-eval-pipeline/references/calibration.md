# Calibration — Agent Evaluation Pipeline

## How to Know Your Level

### Novice
You can write eval scenarios for a single-tool agent and run them with binary pass/fail. You understand the difference between unit, integration, and E2E testing in the agent context. You've scaffolded an eval harness from a template.

**Signs you're here:** You ask "how do I test an agent?" You've never calibrated an LLM judge. You use `assertEqual` for agent output comparison.

**Path to Competent:** Calibrate one LLM judge against human raters. Write 50 scenarios with continuous scoring rubrics. Run SPRT for the first time.

### Competent
You can design a complete test pyramid for a multi-turn agent. You've calibrated an LLM judge with kappa ≥ 0.7. You understand SPRT, bootstrap CI, and when to use each. You've configured a CI eval gate.

**Signs you're here:** You ask "is my judge calibrated?" You track false-positive rate. You can explain position bias and how to mitigate it.

**Path to Expert:** Design a gotcha suite with 50+ scenarios. Implement drift detection with embeddings. Run a silent regression fire drill and measure detection time.

### Expert
You can design evaluation pipelines for 10-phase agent workflows. You've implemented multi-judge ensembles, categorical SPRT for defect classification, and cost-tiered evaluation. You've debugged a production regression that score-based eval missed and added embedding-based detection.

**Signs you're here:** You ask "what's our cost per detected regression?" You optimize the eval pipeline itself. You've onboarded another team onto your eval infrastructure.

**Path to Master:** Build eval-as-a-service. Design self-service scenario authoring. Measure time-to-detection across teams. Publish eval health metrics to the organization.

### Master
You've built evaluation infrastructure used by 5+ agent teams. Your eval platform detects regressions within 4 hours at <2% false-positive rate. You've contributed methodology improvements back to the field (AgentAssay extensions, novel drift detection, calibration automation).

**Signs you're here:** You ask "how do we make eval a platform capability?" Teams ask you to review their eval design. You write about eval methodology for the broader community.
