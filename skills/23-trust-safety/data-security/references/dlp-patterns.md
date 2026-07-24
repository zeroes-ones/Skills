# Data Loss Prevention (DLP) Patterns

## DLP Architecture Layers

| Layer | Scope | Detection Methods | Example Tools |
|-------|-------|------------------|---------------|
| **Endpoint DLP** | Laptops, workstations, servers | File content inspection, clipboard monitoring, USB control, print monitoring | Microsoft Purview Endpoint DLP, Forcepoint, Digital Guardian |
| **Network DLP** | Network egress points, email, web traffic | Deep packet inspection, protocol analysis, email content scanning | Symantec DLP, Proofpoint, Zscaler DLP |
| **Cloud DLP** | SaaS apps, cloud storage, CASB | API-based inspection, real-time policy enforcement, sharing controls | Netskope CASB, Microsoft Defender for Cloud Apps, GCP DLP API |

## Detection Methods (ranked by false-positive rate)

| Method | FP Rate | Best For | Limitations |
|--------|---------|----------|-------------|
| **Exact Data Match (EDM)** | Very Low | Structured PII (SSN, credit card, employee ID) | Requires fingerprint database; misses derived/transformed data |
| **Indexed Document Matching (IDM)** | Low | Source code, legal contracts, design documents | Requires indexing corpus; misses paraphrased content |
| **Regular Expressions** | Medium | Credit card numbers, SSN, email, phone | High false positives without validation (Luhn check, context) |
| **ML Classification** | Low-Medium | Unstructured text, images, general sensitive content | Requires training; may miss novel patterns |
| **Keyword/Pattern Matching** | High | Quick initial filtering | Produces many false positives; use as first-pass filter only |

## DLP Policy Design Framework

1. **Define protected data types**: What exactly are you protecting? (PII: name+SSN, PHI: diagnosis+patient ID, PCI: PAN+expiry, IP: source code+design docs)
2. **Set thresholds**: Single SSN? Alert. 50 SSNs in one file? Block and quarantine.
3. **Define channels**: Email? Web upload? USB? Cloud sharing? API calls?
4. **Choose response actions**: Alert only → Block and notify user → Block and quarantine → Block and escalate to security
5. **Tune false positives**: Start in monitor-only mode for 30 days. Tune patterns. Then enforce.

## False Positive Tuning Workflow

- Week 1-2: Monitor mode — collect all alerts, classify true vs false positives
- Week 3: Identify top false-positive patterns, adjust regex/keywords/thresholds
- Week 4: Re-test with adjusted rules, verify FP rate < 5%
- Go-live: Enforce blocking for high-confidence rules, alert-only for medium-confidence
