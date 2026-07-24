# Error Decoder — Agent Evaluation Pipeline

## Common Eval Failures and Their Root Causes

### "Eval scores fluctuate ±5% between identical runs"
**Root cause:** Non-reproducible eval pipeline. Temperature > 0 on LLM calls, unseeded RNG, or unpinned model versions.
**Fix:** Set temperature=0. Seed all RNG. Pin model versions with date tags. Lock dependency hashes. Verify 3-run score stability.

### "Judge scores don't correlate with human judgment"
**Root cause:** Uncalibrated judge. Position bias, length bias, or self-enhancement bias dominating scores.
**Fix:** Calibrate against 3+ human raters on 100+ examples. Mitigate position bias with symmetric evaluation. Check correlation of scores with response length.

### "CI eval gate blocks 20% of PRs but all are false positives"
**Root cause:** Gate threshold too strict relative to score variance. Single-run eval with ±3% noise and a ±2% threshold.
**Fix:** Require 3 consecutive failures to block. Set threshold at baseline - 2σ (not -1σ). Use SPRT statistical significance.

### "Eval passes locally but fails in CI"
**Root cause:** Environment coupling. Eval depends on `.env` variables, local database, or cached files not present in CI.
**Fix:** Containerize eval with Docker. Mock all external dependencies. Run `docker build && docker run` locally before pushing.

### "Agent scores keep improving but users report it's getting worse"
**Root cause:** Metric-reward hacking. Agent optimizes for the measured dimension (e.g., verbosity) at the expense of unmeasured dimensions (accuracy).
**Fix:** Track 5+ dimensions. Weight them in final score. Use embedding similarity to detect style drift. Run adversarial eval.

### "Gotcha scenarios all pass but agent fails on real edge cases"
**Root cause:** Gotcha scenarios are too narrow. They test specific known patterns rather than generating novel edge cases.
**Fix:** Generate gotchas programmatically with variation. Rotate 30% monthly. Use adversarial generation (LLM-as-attacker finds weaknesses).

### "Nightly eval takes 4+ hours and times out"
**Root cause:** Unoptimized eval pipeline. Full suite running sequentially on expensive judge.
**Fix:** Parallelize scenarios across N containers. Stratified sampling for nightly (200/500 scenarios). Cache unchanged scenarios. Use cheaper judge model.

### "SPRT runs 500+ iterations without reaching a decision"
**Root cause:** Effect size smaller than MDE (δ). Trying to detect a 1% change with δ=0.05.
**Fix:** Reduce δ to match expected effect size. Or accept that the effect is too small to matter — increase δ and move on.
