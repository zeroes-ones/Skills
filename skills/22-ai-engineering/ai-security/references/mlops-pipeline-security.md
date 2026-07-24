# MLOps Pipeline Security — Reference

## Training Pipeline Hardening

### Data Ingestion Security

- Validate all training data sources: provenance tracking from origin to training set
- Scan for PII (email, phone, SSN, credit card) before data enters pipeline
- Scan for secrets (API keys, tokens, passwords) in training data
- Content filtering: remove toxic, harmful, or illegal content
- Immutable provenance log: every data point's source, timestamp, preprocessing steps, hash

### Training Infrastructure Security

- Training runs in isolated environment (dedicated VPC/subnet, no production access)
- Training jobs run as non-root, minimal filesystem access
- GPU/TPU resources have network restrictions (no outbound internet unless necessary)
- Checkpoint integrity: SHA-256 hash on every checkpoint, signed by training infra
- Differential privacy (if training on sensitive data): ε-budget tracking, DP-SGD

## Model Registry Security

- Access control: separate roles for upload, review, approve, deploy
- Model signing: cryptographic signature on model artifacts (weights, config, tokenizer)
- Immutable registry: once published, version cannot be modified — new versions only
- Vulnerability scanning: automated dependency scan on every model artifact upload
- Provenance chain: training data → training run → checkpoint → registry → deployment

## CI/CD for ML Security

Every model deployment pipeline must include:

1. **Static analysis:** Scan model loading code for pickle usage, known-vulnerable deps
2. **Adversarial testing:** garak/PyRIT automated test suite against staging deployment
3. **Guardrails audit:** Verify all guardrails are present and configured fail-closed
4. **SBOM generation:** Create model bill of materials for every deployment artifact
5. **Policy gate:** Block deployment if any security finding above MEDIUM severity

## Deployment Security

- Model server runs as non-root with minimal capabilities (seccomp/AppArmor profile)
- Network: model server has no outbound internet access (fetch dependencies at build time)
- Resource limits: CPU/memory/GPU caps prevent DoS via resource exhaustion
- Rate limiting: per-user, per-IP, per-token quota at API gateway
- Authentication: all inference endpoints require authentication (API key, OAuth, mTLS)
