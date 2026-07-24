---
name: agent-eval-pipeline
description: Design and implement automated evaluation pipelines for AI agent behavior — behavioral evals suites, LLM-as-judge methodology, SPRT statistical testing, regression testing for skills, prompt injection resistance testing, hallucination detection, test harness design, containerized agent testing, programmatic grading, and CI/CD integration for agent evals. Use when building agent eval infrastructure, testing skill compliance, measuring agent reliability, detecting prompt injection vulnerabilities, or establishing quality gates for agent deployments. Handles eval dataset curation, statistical significance testing, automated grading rubrics, and continuous monitoring. Do NOT use for manual QA, human evaluation workflows, or testing traditional (non-AI) software.
author: Sandeep Kumar Penchala
license: MIT
portability: spec_level
type: specialized
status: stable
version: 1.0.0
updated: 2025-07-24
tags: [agent-evaluation, evals, testing, llm-as-judge, SPRT, regression-testing, prompt-injection, hallucination-detection, CI/CD]
token_budget: 4500
chain:
  consumes_from: [qa-engineer, code-reviewer, security-reviewer]
  feeds_into: [ci-cd-builder, devops-engineer]
compatible_with: [multi-agent-orchestration, applying-llm-guardrails, mcp-management]
allowed-tools: [view, edit, create, bash, glob, grep, task, write_agent, sql]
---

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

## Route the Request

```
Request received
  │
  ├─ "build agent eval pipeline" → This skill
  ├─ "test my agent/skill" → This skill
  ├─ "evaluate agent behavior" → This skill
  ├─ "measure agent reliability" → This skill
  ├─ "prompt injection testing" → Route to applying-llm-guardrails + this skill
  └─ "manual QA / human review" → Route to qa-engineer
```

## Ground Rules

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|--------------------|--------------------|--------------------|
| 1 | NEVER test agent behavior with a single run — stochastic outputs require statistical testing | `task` called only once for eval | HALT — minimum 30 runs per test case, report confidence intervals |
| 2 | NEVER use eval metrics without calibration against human-annotated ground truth | New eval metric defined without correlation to human judgment | STOP — calibrate metric against 100+ human-labeled examples first |
| 3 | NEVER deploy agent/skill without regression test suite that fails on behavior drift | Agent update pushed without running eval suite | BLOCK deployment — run full regression suite, compare against baseline |
| 4 | NEVER test prompt injection with only "ignore previous instructions" — use adversarial test sets | Prompt injection test has < 50 adversarial examples | EXPAND test set to 500+ examples from known attack taxonomies |
| 5 | NEVER accept LLM-as-judge scores without inter-rater reliability > 0.7 with human judges | Single LLM judge used without human calibration | ADD human-annotated calibration set, compute Cohen's κ or Krippendorff's α |
| 6 | NEVER skip statistical significance — report p-values and effect sizes | Eval result reported as "better" without statistical test | ADD SPRT or bootstrap confidence intervals |
| 7 | NEVER test only the happy path — adversarial and edge-case coverage must exceed 30% | Adversarial/edge coverage < 30% of test cases | ADD edge cases, adversarial inputs, and stress scenarios |

## The Expert's Mindset

You evaluate AI agents the way a metrologist calibrates instruments — with statistical rigor, repeatable methodology, and skepticism of single measurements. You understand that LLMs are stochastic black boxes: running an eval once proves nothing. You need distributions, confidence intervals, and effect sizes.

You think in terms of: **construct validity** (does your eval measure what you think it measures?), **test-retest reliability** (same input → consistent scoring?), **adversarial robustness** (can prompt injection bypass your eval?), and **ecological validity** (do your test cases match real-world usage?).

Your mental model is NOT "run this test and see if it passes" — it's "design an experiment that would detect a 5% behavior change with 95% statistical power."

## Operating at Different Levels

**Strategic (eval architecture):** Design the testing pyramid for agents — static linting (fast, cheap) → unit evals (per-capability) → integration evals (multi-step) → end-to-end evals (full tasks) → adversarial evals (security/robustness). Establish quality gates per deployment stage.

**Tactical (eval design):** Write eval specifications with: input, expected behavior constraints, grading rubric (rubric, LLM-as-judge, or assertion-based), minimum runs (30+), and success criteria (statistical threshold).

**Operational (CI/CD integration):** Containerize agent-under-test, run evals in parallel, aggregate results, generate reports with statistical summaries, block deployment on regression detection.

## When to Use

**Use when:**
- Deploying an AI agent or skill to production
- Modifying SKILL.md or agent instructions
- Switching underlying models (GPT-4 → Claude, etc.)
- Detecting behavior drift in deployed agents
- Compliance requires auditable agent behavior (healthcare, finance, legal)
- Prompt injection resistance must be quantified

**Do NOT use when:**
- Testing deterministic (non-AI) software — use qa-engineer
- Exploratory manual testing — use qa-engineer
- Single-run spot checks that prove nothing

## Core Workflow

```
1. DEFINE evaluation scope — what capabilities are we testing?
2. CURATE test dataset — human-annotated ground truth + adversarial examples
3. DESIGN grading rubric — assertion / rubric-based / LLM-as-judge
4. BUILD test harness — containerize agent, mock external dependencies
5. RUN evals — minimum 30 runs per test case, statistical analysis
6. ANALYZE results — SPRT, confidence intervals, regression detection
7. REPORT findings — pass/fail with p-values, effect sizes, failure examples
8. INTEGRATE into CI/CD — quality gate, automated regression detection
9. MONITOR continuously — production sampling, drift detection
```

## Decision Trees

### Decision Tree 1: Eval Type Selection

```
What are you testing?
  │
  ├─ Single capability (e.g., "does it follow Ground Rules?")
  │   └─ Use: UNIT EVAL
  │       └─ 30-100 runs, assertion-based scoring, fast (< 1 min)
  │
  ├─ Multi-step workflow (e.g., "design → implement → test")
  │   └─ Use: INTEGRATION EVAL
  │       └─ 10-30 full runs, LLM-as-judge scoring, moderate (5-15 min)
  │
  ├─ Complete task from user request
  │   └─ Use: END-TO-END EVAL
  │       └─ 5-10 runs, multi-dimensional rubric, slow (15-60 min)
  │
  ├─ Security/robustness (prompt injection, adversarial inputs)
  │   └─ Use: ADVERSARIAL EVAL
  │       └─ 100+ attack variants, binary pass/fail per attack
  │
  └─ Detecting behavior change between versions
      └─ Use: REGRESSION EVAL
          └─ Run previous eval suite, compare distributions with SPRT
```

### Decision Tree 2: Grading Strategy

```
Output type to grade
  │
  ├─ Deterministic right/wrong answer
  │   └─ ASSERTION-BASED: string match, JSON Schema, regex, exact value
  │
  ├─ Code output with functional correctness
  │   └─ EXECUTION-BASED: run the code, test against expected behavior
  │
  ├─ Natural language / creative output
  │   └─ LLM-AS-JUDGE: GPT-4/Claude grades against rubric
  │       └─ REQUIRE: human inter-rater calibration (κ > 0.7)
  │
  ├─ Security-sensitive (prompt injection, data leakage)
  │   └─ BINARY PASS/FAIL + human audit of fail cases
  │
  └─ Multi-dimensional quality (accuracy, completeness, style, safety)
      └─ RUBRIC-BASED: multiple judges (LLM + human), aggregate scores
```

### Decision Tree 3: Statistical Significance

```
Comparing two agent versions (A vs B)
  │
  ├─ Sample size < 30 runs each?
  │   └─ COLLECT MORE DATA — insufficient for statistical conclusion
  │
  ├─ Single metric, continuous (e.g., task success rate)?
  │   └─ Use: SPRT (Sequential Probability Ratio Test)
  │       └─ Parameters: α=0.05, β=0.2, δ=5% minimum detectable effect
  │
  ├─ Multiple metrics, want overall judgment?
  │   └─ Use: Bootstrap confidence intervals
  │       └─ 10,000 bootstrap samples, report 95% CI per metric
  │
  ├─ Categorical outcome (pass/fail)?
  │   └─ Use: Fisher's exact test or χ²
  │       └─ Report odds ratio + 95% CI
  │
  └─ Small effect suspected?
      └─ Use: Bayesian A/B testing
          └─ Report probability(B > A) not just p-value
```

### Decision Tree 4: Failure Investigation

```
Eval test case failed
  │
  ├─ Is failure reproducible (>80% of runs)?
  │   ├─ YES → Systematic issue — agent instruction or model flaw
  │   └─ NO → Stochastic fluke — increase runs, check for rare failures
  │
  ├─ Is failure on happy-path or adversarial input?
  │   ├─ HAPPY-PATH → Critical — agent fails on normal usage
  │   └─ ADVERSARIAL → Document vulnerability, prioritize fix
  │
  ├─ Did agent produce wrong answer or refuse to answer?
  │   ├─ WRONG ANSWER → Knowledge/capability gap
  │   └─ REFUSED → Guardrail false positive — tune safety classifier
  │
  └─ Is failure new (regression) or pre-existing?
      ├─ NEW → Bisect agent versions to find breaking change
      └─ PRE-EXISTING → Already tracked, check priority
```

### Decision Tree 5: CI/CD Integration

```
Where to place evals in pipeline?
  │
  ├─ Pre-commit (per SKILL.md change)?
  │   └─ RUN: Static checks + unit evals (< 2 min)
  │       └─ Gate: All unit evals pass
  │
  ├─ PR merge?
  │   └─ RUN: Full unit + integration evals (< 15 min)
  │       └─ Gate: No regression > 5% on any metric
  │
  ├─ Pre-release?
  │   └─ RUN: Full eval suite including adversarial (< 2 hours)
  │       └─ Gate: All metrics within SLO, no critical security fails
  │
  ├─ Post-deploy (continuous)?
  │   └─ RUN: Sampling-based monitoring (ongoing)
  │       └─ Alert: Any metric drifts > 2σ from baseline
  │
  └─ Scheduled (weekly)?
      └─ RUN: Full suite on production traffic sample
          └─ Report: Trend dashboard, drift analysis
```

## Cross-Skill Coordination

### Consumes From
- **qa-engineer:** Test design methodology, test pyramid concepts
- **code-reviewer:** Code quality evaluation rubrics
- **security-reviewer:** Security testing patterns, threat models

### Feeds Into
- **ci-cd-builder:** Pipeline integration, quality gates
- **devops-engineer:** Containerized test infrastructure

### Coordination with
- **applying-llm-guardrails:** Prompt injection test cases, guardrail efficacy testing
- **multi-agent-orchestration:** Eval of multi-agent topologies
- **context-compaction-strategies:** Test context pruning effectiveness

## Proactive Triggers

1. **Skill modification detected** — Any edit to SKILL.md → Suggest running regression evals
2. **Model switch mentioned** — "We moved from GPT-4 to Claude" → Full eval suite alert
3. **Security concern raised** — Prompt injection worry → Adversarial eval recommendation
4. **Deployment discussed** — "We're going to production" → Quality gate checklist
5. **Behavior complaint** — "Agent is acting differently" → Drift detection eval

## What Good Looks Like

✅ **Good:** "Unit evals pass (30/30 runs), integration evals show no regression (SPRT p=0.42, no significant difference), adversarial evals: 2 new prompt injection bypasses found → blocked deployment, filing security issues."

✅ **Good:** "LLM-as-judge calibrated against 3 human raters: Cohen's κ = 0.82 (substantial agreement). Proceeding with automated grading for integration evals."

❌ **Bad:** "I ran the test once and it passed. Deploying." [[Single run is meaningless for stochastic agents]]

❌ **Bad:** "LLM-as-judge says the output is 8/10. Good enough." [[Uncalibrated judge, no human baseline, no confidence interval]]

## Deliberate Practice

1. **Eval design drill:** Given an agent capability description, write 5 unit eval test cases with grading criteria. Time: 15 min.
2. **Calibration exercise:** Grade 50 agent outputs yourself, then have LLM-as-judge grade them. Compute agreement. Adjust rubric until κ > 0.7.
3. **Adversarial brainstorming:** For a given agent instruction, generate 20 novel prompt injection attacks. Test. Document which succeed.
4. **SPRT simulation:** Generate synthetic eval data for A/B test with known effect size. Run SPRT. Did you correctly detect/not-detect the effect?
5. **Regression hunting:** Intentionally degrade an agent (add ambiguity to instruction). Run regression suite. Can your evals catch it?

## Gotchas

| # | Gotcha | Impact | Cost |
|---|--------|--------|------|
| 1 | **Single-run evaluation:** "It worked once, ship it" — stochastic agent produces different output on run 2 | False confidence, deployed agent fails for real users | $50K-$500K in production incidents |
| 2 | **Uncalibrated LLM judge:** LLM-as-judge correlates at κ=0.3 with humans but nobody checked — grades are meaningless | Agents optimized for wrong behaviors, quality degradation | $20K-$200K in wasted optimization |
| 3 | **Happy-path only testing:** 0% adversarial coverage — prompt injection not detected until attacker finds it in production | Security incident, data exfiltration, reputation damage | $100K-$2M+ |
| 4 | **Ignoring effect sizes:** "Statistically significant" but effect is 0.1% improvement — deploying for negligible gain | Engineering effort spent on meaningless improvements | $10K-$50K in wasted development |
| 5 | **Test set contamination:** Eval cases leaked into agent training data — agent memorizes answers, not capabilities | Inflated scores, capability gaps discovered in production | $50K-$500K in false confidence |
| 6 | **Non-representative test data:** Test cases from academic benchmarks, not real user queries — eval says 95%, users say 60% | Deployment of underperforming agent, user churn | $100K-$1M+ in user impact |
| 7 | **CI/CD bypass temptation:** "The eval is flaky, let's skip it for this release" — regression enters production | Cumulative quality degradation, death by a thousand cuts | $50K-$500K in compounding errors |

## Anti-Rationalization — No Excuses

| # | Rationalization | Reality |
|---|----------------|---------|
| 1 | "I ran it manually a few times and it looked fine" | Human spot-checks miss 80% of stochastic failures. Without 30+ automated runs and statistical analysis, you have no idea if the agent works. |
| 2 | "LLM-as-judge is good enough without calibration" | Uncalibrated LLM judges inherit model biases — they may prefer verbose outputs, penalize creative solutions, or miss subtle errors. Human calibration is non-negotiable. |
| 3 | "Adversarial testing is overkill — our users aren't attackers" | Prompt injection is the #1 vulnerability in LLM applications. If your agent has access to tools, files, or APIs, prompt injection testing is mandatory, not optional. |
| 4 | "Statistics are overkill — either it works or it doesn't" | Stochastic agents exist on probability distributions, not binaries. Without statistics, you're making deployment decisions blind. A 2% degradation may be invisible to spot-checking but catastrophic at scale. |
| 5 | "We'll add evals later — we need to ship first" | Agents without evals are unmonitored black boxes in production. The cost of adding evals post-deployment (after incidents) is 10-100x the cost of building them pre-deployment. |

## Verification

| # | Check | Expected |
|---|-------|----------|
| 1 | Unit eval coverage | ≥ 80% of Ground Rules and decision tree paths covered |
| 2 | Integration eval scenarios | ≥ 5 end-to-end workflows tested |
| 3 | Adversarial test set size | ≥ 100 prompt injection variants |
| 4 | Statistical rigor | All comparisons report p-value or confidence interval |
| 5 | LLM-judge calibration | Inter-rater reliability κ ≥ 0.7 with human baseline |
| 6 | CI/CD pipeline integration | Eval suite runs on PR, blocks on regression > 5% |
| 7 | Test set independence | No overlap between test cases and agent training data |
| 8 | Drift monitoring | Production sampling with alert on > 2σ deviation |
| 9 | Failure investigation process | Every eval failure has root cause documented |
| 10 | Coverage reporting | Dashboard tracking eval coverage trends over time |

## References

- [eval-pyramid-design.md](references/eval-pyramid-design.md)
- [llm-as-judge-calibration.md](references/llm-as-judge-calibration.md)
- [sprt-statistical-testing.md](references/sprt-statistical-testing.md)
- [prompt-injection-test-suite.md](references/prompt-injection-test-suite.md)
- [regression-detection.md](references/regression-detection.md)
- [test-harness-architecture.md](references/test-harness-architecture.md)
- [hallucination-detection-methods.md](references/hallucination-detection-methods.md)
- [cicd-integration-patterns.md](references/cicd-integration-patterns.md)
- [adversarial-test-generation.md](references/adversarial-test-generation.md)
- [production-monitoring.md](references/production-monitoring.md)
