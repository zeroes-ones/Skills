# Scale Depth: Solo → Small → Medium → Enterprise

<!-- DEEP: 10+min -->

### Solo (1 person, 0-100 users)
- **What changes**: Manual review of all AI-generated health content before publication. Basic disclaimer on every output. Content filtering via keyword blocklist. No FDA pathway yet (pre-market). Report clinical accuracy on 50 vignettes.
- **What to skip**: Formal clinical accuracy benchmarking, inter-rater reliability studies, FDA PCCP, red teaming program, bias audits, automated hallucination detection, formal safety incident protocols.
- **Coordination**: You are the safety reviewer. Review every output. Document all safety decisions.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Automated hallucination detection (NLI-based). 100-vignette clinical accuracy test. Basic demographic bias audit. Content filtering with allowed/disallowed categories. Pre-launch red team (200 prompts). Formal disclaimers by content type. Incident response playbook.
- **What to skip**: Full FDA regulatory submission, formal inter-rater reliability study, continuous red teaming, clinician panel, independent safety audit.
- **Coordination**: Clinician advisor reviews accuracy benchmarks. Legal reviews disclaimers. Safety incidents tracked in issue tracker.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Formal clinical accuracy study with ≥3 board-certified clinicians. Inter-rater reliability reported (Cohen's kappa). Full demographic bias audit published. FDA pre-submission meeting. PCCP drafted. Monthly red teaming. Automated content filtering with ML classifiers. Crisis response integration (988 Lifeline). SHAP/LIME explainability for flagged outputs.
- **What to skip**: FDA clearance (in process but not complete), PMA-level clinical trials, independent safety monitoring board, published peer-reviewed validation.
- **Coordination**: Clinical advisory board (3+ physicians). Regulatory affairs consultant. Weekly safety review meeting. Incident response team on call.

### Enterprise (50+ people, 1M+ users)
- **What changes**: FDA clearance obtained (510(k) or De Novo). Published clinical validation study. Continuous red teaming program. Independent safety monitoring board. Real-time hallucination detection. Multi-language bias audits. Explainability dashboards for clinicians. Integration with EHR systems (FHIR). Adverse event reporting system (FDA MedWatch). SOC 2 + HIPAA + HITRUST certified.
- **What's full production**: 24/7 safety monitoring. Automated adverse event detection. Quarterly safety reports to FDA (if cleared). Published transparency reports. Patient safety organization (PSO) participation.
- **Coordination**: Chief Medical Officer. Regulatory affairs team. Clinical safety officer. External advisory board. FDA liaison. Patient advocacy group engagement.

### Transition Triggers
- **Solo → Small**: First 100 users. User reports potentially harmful output. Preparing for pilot with healthcare partner.
- **Small → Medium**: FDA pre-submission meeting scheduled. >10K users. Healthcare enterprise customer requiring clinical validation.
- **Medium → Enterprise**: FDA clearance obtained. >1M users. Integration with clinical workflows.
