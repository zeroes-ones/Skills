# AI Red-Teaming Methodology — Reference

## Tool Ecosystem

**garak** (garak - LLM Vulnerability Scanner): Python CLI, 80+ probes, 20+ detectors.
Best for automated, broad-coverage scanning in CI/CD. Probes include: prompt injection,
encoding-based attacks, known jailbreaks (DAN, STAN, AIM), divergence attacks, toxicity,
misinformation, and more.

**PyRIT** (Python Risk Identification Tool, Microsoft): Orchestration framework for
multi-turn adversarial attacks. Supports attacker LLM strategies (PAIR — Prompt Automatic
Iterative Refinement, Crescendo), scoring with human-review or LLM-as-judge, and
converters (Base64, ROT13, leetspeak, unicode).

**Gandalf (Lakera):** Gamified prompt injection challenge. 8 levels of increasing
difficulty. Excellent for building red-teaming intuition.

## Test Suite Coverage

| Attack Category | garak Probes | PyRIT Strategies | Custom Needed? |
|-----------------|-------------|------------------|----------------|
| Prompt injection | promptinject.* | direct/indirect injection | Multi-modal injection |
| Jailbreak | dan.*, encoding.* | PAIR, Crescendo | App-specific jailbreaks |
| Data extraction | divergence.* | many-shot extraction | Training data extraction |
| Toxicity | toxicity.* | — | Domain-specific toxicity |
| Model theft | — | API extraction | Architecture probing |

## CI/CD Integration

1.  Trigger: on every model update (weights, system prompt, fine-tuning), every PR that
    touches inference code, and on schedule (weekly for stable models)
2.  Run garak with configured probes against staging endpoint
3.  Parse results: any HIGH severity finding → block deployment
4.  Regression suite: all previously successful attacks must fail (be blocked) to pass
5.  Results dashboard: attack success rate trend, new vulnerability alerts

## Severity Classification

- **CRITICAL:** Successful jailbreak producing harmful content, system prompt extraction,
  PII in output, arbitrary code execution via plugin
- **HIGH:** Partial jailbreak, tool invocation without authorization, data extraction
  beyond intended scope
- **MEDIUM:** Rate limiting bypass, guardrail evasion with low success rate
- **LOW:** Theoretical vulnerabilities, attacks requiring unrealistic conditions
