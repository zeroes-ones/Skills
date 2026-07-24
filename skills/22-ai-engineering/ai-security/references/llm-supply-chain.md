# Supply Chain Security for LLM Apps — Reference

## Overview

LLM supply chain security extends beyond traditional software supply chain
concerns to include model weights, datasets, fine-tuning pipelines, and the
unique risks of third-party model hubs.

## Model Provenance

- **Hugging Face model cards:** Verify author identity, training methodology,
  and intended use before importing. Prefer models with verified organizations.
- **safetensors vs. pickle:** safetensors is a safe serialization format that
  cannot execute arbitrary code. NEVER load pickle-based model files without
  sandboxed execution — pickle deserialization is arbitrary code execution.
- **SHA256 verification:** Always pin and verify model weight hashes. Model
  weights can be silently replaced on hubs without version changes.
- **Sigstore/cosign:** Sign model artifacts with Sigstore for cryptographic
  provenance chains integrated into CI/CD pipelines.

## Dependency Scanning

- **pip/conda audit:** Scan Python dependencies for known CVEs in your ML stack
- **Container image scanning:** Trivy, Grype for base images (PyTorch, TF, vLLM containers)
- **SBOM for ML:** Generate Software Bill of Materials including model weights,
  datasets, and fine-tuning artifacts alongside traditional dependencies

## Hugging Face Security

- Enable 2FA and organization access controls on model repositories
- Audit model commit history for unexpected changes before pulling
- Use the `trust_remote_code=False` flag unless code review has been performed
- Verify inference API endpoints use HTTPS and authenticate all requests
