# Best Practices — Agent Evaluation Pipeline

## 1. Design the Test Pyramid Before Writing Agent Code
The eval harness is not an afterthought — it's the specification. Write 50 scenarios before implementing the first tool. Each scenario defines expected behavior. The agent is "done" when it passes all scenarios.

## 2. Use Continuous Scoring, Never Binary
Every evaluation dimension uses a 0.0-1.0 scale with behavioral rubric anchors. Binary pass/fail masks regression. A score of 0.87 → 0.84 is a real degradation even if both "pass" a binary threshold.

## 3. Calibrate Judges Against Human Raters
Run LLM judges on 100+ human-annotated examples. Compute Cohen's kappa. If kappa < 0.7, iterate the rubric. Recalibrate every 3 months — human expectations drift.

## 4. Mitigate Position Bias
For pairwise comparisons, evaluate (A, B) and (B, A). Average scores. Position bias flips 65% of decisions in uncalibrated judges.

## 5. Use Statistical Testing
SPRT sequential testing detects regressions 3-5x faster than fixed-sample. It stops early when the result is clear. Configure α=0.05, β=0.20, δ=MDE.

## 6. Containerize Eval
Docker ensures eval runs identically in dev and CI. Mock all external dependencies. If eval doesn't pass in Docker locally, it won't pass in CI.

## 7. Make Eval Reproducible
Temperature=0 for all LLM calls in eval. Seed all RNG. Pin model versions. Lock dependencies. Three consecutive runs must produce identical scores.

## 8. Tier Eval by Model Cost
GPT-4o-mini for pre-merge (95% of runs, $0.03/run). GPT-4o for nightly (full suite, $0.50/run). GPT-4o/Opus for release gates ($2.00/run). Track eval cost alongside quality.

## 9. Include Gotcha Scenarios
Ambiguous instructions, prompt injection, conflicting tools, malformed output, resource exhaustion. A happy-path-only suite misses 80% of production failures.

## 10. Track False-Positive Rate
Monthly report: how many PRs were blocked by eval? How many blocks were false positives? Target <2%. If higher, loosen thresholds or increase sample size.
