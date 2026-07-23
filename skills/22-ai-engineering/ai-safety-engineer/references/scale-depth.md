# Scale Depth

<!-- DEEP: 10+min -->

### Solo (0-10 users, 1 person)
**Description:** Manual review of AI outputs, ad-hoc safety checks
**When to use:** Don't ship dangerous outputs
**Approach:** Developer spot-checks responses; no formal safety process; gut-feel judgments

### Small Team (10-100 users, 2-5 people)
**Description:** Automated guardrails (input/output), safety test suite, red-teaming
**When to use:** Build safety into the product, catch regressions
**Approach:** Content filters + prompt injection detection; automated test suite; periodic red-teaming

### Medium Team (100-10K users, 5-20 people)
**Description:** Safety platform (real-time monitoring, bias detection, incident response)
**When to use:** Proactive safety, systematic risk management
**Approach:** Real-time guardrail dashboard; bias evaluation pipeline; incident response playbook; safety SLAs

### Enterprise (10K+ users, 20+ people)
**Description:** Dedicated safety org, compliance framework, external audits
**When to use:** Enterprise trust, regulatory readiness
**Approach:** Safety VP + team; NIST AI RMF alignment; third-party audits; safety case documentation; EU AI Act compliance

### Transition Triggers
- Move from Solo to Small Team when: Manual spot-checks miss safety issues; need for automated guardrails becomes clear; product usage increases beyond what manual review can handle
- Move from Small Team to Medium Team when: Need for real-time monitoring and systematic risk management; incident response requires formal playbook; bias evaluation becomes important
- Move from Medium Team to Enterprise when: Regulatory compliance requirements (EU AI Act, NIST AI RMF) apply; external audits needed; dedicated safety organization required for enterprise trust
