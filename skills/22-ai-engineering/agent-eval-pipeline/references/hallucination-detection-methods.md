# Hallucination Detection Methods

## Detection Categories

### Factual Grounding
- Cross-reference outputs against provided context
- Flag claims not supported by input documents
- Use NLI (Natural Language Inference) models

### Self-Consistency
- Run agent N times (N ≥ 5)
- Compare outputs for factual consistency
- High variance on factual claims → likely hallucination

### Source Attribution
- Require agent to cite sources for factual claims
- Verify citations resolve to actual content
- Flag unsourced claims as unverified

### Uncertainty Expression
- Track hedging language ("might", "possibly", "I think")
- Sudden shift from uncertain → certain without new evidence = red flag
- Encourage calibrated confidence: "I'm 90% confident that..."

## Metrics
- Hallucination rate: % of runs with at least one hallucination
- Factual precision: % of factual claims that are correct
- Source fidelity: % of citations that match source content
