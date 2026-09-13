# Sources — provenance for the claims in this skill

> Every claim in SKILL.md and these reference files traces to a source below, tagged by strength.
Estimated figures are marked as such and must not be quoted as measured.

---

## Sources

The claims in SKILL.md and this file trace to the following. Where a source is weaker (essay,
practice report), it is marked. The mechanisms are well-established; any specific rate or
percentage in a given system must be measured on that system.

| Claim | Source | Strength |
|-------|--------|----------|
| A producer evaluating its own output inherits its own errors; execution and verification must be separate roles | Standard software-assurance practice (separation of duties); reproduced directly in agent literature (`doubt-driven-development` in this library applies a fresh-context adversarial variant) | Established practice |
| Optimising a proxy erodes the intent the proxy stood for | Goodhart's Law and the surrogate-metric literature in economics and ML safety; the "specification gaming" catalogue from DeepMind's *Specification Gaming: The Flip Side of AI Ingenuity* | Established; widely reproduced |
| A validator given the producer's reasoning adopts it | Code-review practice — reviewing an explanation rather than an artifact; anchor bias in review | Established practice |
| LLM judges must be calibrated against human raters on held-out examples | LLM-as-judge literature; this library's own `agent-eval-pipeline` encodes calibration and inter-rater reliability (Cohen's kappa) | Peer-reviewed / established |
| Evaluator-optimizer with independent evaluation outperforms self-critique | Anthropic, "Building Effective Agents" — the evaluator-optimizer pattern and the workflows-versus-agents distinction | Primary vendor engineering |
| A check whose rejection rate is unmeasured provides no signal | Measurement theory; the base-rate and sensitivity/specificity framing | Foundational |
| Aggregating a rate hides the class that matters | Standard observability practice; the same argument the library makes for cache hit rate by key class (`caching-architect`) | Established practice |
| Silent failures (recall failures) cost more than loud ones | Reliability practice; silent wrong data is the expensive class in incident literature | Established practice |
| Incident-cost ranges quoted in SKILL.md ($5k–$50k, $10k–$75k, $25k–$150k, $50k–$500k, $100k–$1M+) | Directional estimates synthesised from incident-response cost reporting | **Estimated** — order-of-magnitude, not audited; never quote as measured |

**Explicitly not claimed.** That independence guarantees correctness (it bounds shared error, it does
not eliminate error), that a specific rejection rate is "right", or that any harm metric fully
captures an intent. The aim is that a verdict carries *signal* and a metric carries a *guard*, not
that either is complete.

---
