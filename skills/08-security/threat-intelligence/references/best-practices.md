# Best Practices

- **Intelligence-led detection**: every SIEM detection rule is mapped to a specific threat actor TTP from your intelligence database, not a generic "suspicious activity" pattern.
- **Pyramid of Pain prioritization**: invest detection engineering effort at the TTP level (top of pyramid), not at hash/IP level (bottom). TTP-based detections survive adversary tool changes.
- **Confidence scoring discipline**: every intelligence assertion has a confidence score based on source reliability and corroboration — never publish "confirmed" without 3+ independent sources.
- **STIX-native tooling**: adopt OpenCTI or MISP as your CTI platform of record; export all intelligence in STIX 2.1; consume via TAXII 2.1.
- **Threat actor dossier maintenance**: every tracked actor has a living dossier updated at least quarterly with latest TTPs, targeting, and infrastructure changes.
- **Intelligence requirements management**: use Priority Intelligence Requirements (PIRs) to focus collection — never collect "everything." Every feed must answer a specific PIR.
- **Automated IOC lifecycle**: IOCs auto-expire based on last-seen + decay curve; manual review required for IOCs persisting beyond 90 days.
