# Model Theft & Adversarial ML Defense — Reference

## Overview

Model theft and adversarial ML attacks target the confidentiality and integrity
of machine learning models. Defenders must address both extraction (stealing the
model) and evasion (fooling the model) threats across the model lifecycle.

## Attack Vectors

| Vector | Technique | Defense |
|--------|-----------|---------|
| API Extraction | Query API to train a clone model | Rate limiting, output rounding, query auditing |
| Membership Inference | Determine if a sample was in training data | Differential privacy (ε < 8), output perturbation |
| Model Inversion | Reconstruct training data from gradients | Gradient clipping, secure aggregation, DP-SGD |
| Gradient Leakage | Extract private data from shared gradients in FL | Homomorphic encryption, secure multi-party computation |

## Evasion & Poisoning Defenses

- **Adversarial training:** Augment training data with adversarial examples (PGD, FGSM)
- **Input sanitization:** Feature squeezing, JPEG compression, spatial smoothing
- **Certified robustness:** Randomized smoothing with provable L2/L∞ radius guarantees
- **Backdoor detection:** Neural cleanse, activation clustering, spectral signatures
- **Label flipping resistance:** Robust aggregation (median, trimmed mean) in federated settings

## Operational Controls

- Query fingerprinting and anomaly detection on prediction API patterns
- Differential privacy accounting with per-query ε budget tracking
- Model watermarking for ownership verification post-extraction
- Canary gradients for detecting unauthorized fine-tuning
