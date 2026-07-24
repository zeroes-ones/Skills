# Healthcare Security Footguns — Dollar-Quantified

## HIPAA Violations
1. **Unencrypted laptop with PHI stolen** — $50K per record up to $1.5M/year. Average breach: $4.24M (IBM 2024)
2. **No BAA with cloud provider storing PHI** — $50K-$1.5M per violation category
3. **Patient portal accessible without MFA** — OCR settlement: $100K-$1M depending on patient count
4. **Employee accessing ex-spouse medical records** — $250K fine + mandatory corrective action plan + 3 years OCR monitoring

## Technical Footguns
1. **FHIR `_format=xml` enabled on production** — XML external entity injection exposes patient data ($500K+)
2. **Elasticsearch with PHI and no authentication** — exposed to internet, discoverable via Shodan ($2.5M+)
3. **MySQL `general_log` containing PHI queries** — PHI in plaintext log files, audit finding ($100K+)
4. **DICOM images with burned-in PHI shared for research** — de-identification failure, research study suspended ($500K+)

## Real-World Costs
- Anthem breach (2015): $16M OCR settlement, 78.8M records
- Premera Blue Cross (2020): $6.85M, 10.4M records
- Advocate Health Care (2016): $5.55M, 4M records — unencrypted laptops
