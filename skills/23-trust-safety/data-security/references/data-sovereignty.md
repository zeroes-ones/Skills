# Data Sovereignty & Cross-Border Transfer

## Overview
Architecting data systems to comply with jurisdictional data protection laws. Data residency (where data is stored) vs sovereignty (whose laws govern access).

## Key Concepts
- **Data Residency:** Data stored in a specific country/region
- **Data Sovereignty:** Data subject to the laws of the country where it resides
- **Data Localization:** Legal requirement that data must remain within borders

## Schrems II Impact (CJEU, July 2020)
Invalidated EU-US Privacy Shield. SCCs remain valid but require:
1. Transfer Impact Assessment (TIA) per EDPB Recommendations 01/2020
2. Technical supplementary measures when destination laws are inadequate
3. Encryption with keys held outside importer jurisdiction
4. Pseudonymization before transfer
5. Split processing across jurisdictions

## EU-US Data Privacy Framework (DPF, 2023)
Replacement for Privacy Shield. Self-certified US companies only.
- Do NOT rely on DPF alone — maintain SCCs as fallback
- DPF faces the same FISA 702 challenge as invalidated Privacy Shield

## Technical Architecture
### Geo-Fenced KMS
Encryption keys stored in jurisdiction-specific KMS. Data cannot be decrypted without access to the jurisdiction's KMS.

### CLOUD Act Defense
US-headquartered cloud providers can be compelled to produce data under CLOUD Act regardless of storage location. Defense: customer-held encryption keys — provider has no access to plaintext.
