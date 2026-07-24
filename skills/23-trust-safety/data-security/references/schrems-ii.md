# Schrems II — CJEU C-311/18 Data Transfer Ruling

## Overview
Court of Justice of the European Union ruling (July 16, 2020) invalidating the EU-US Privacy Shield and imposing additional requirements on Standard Contractual Clauses (SCCs).

## Key Holdings
1. **Privacy Shield invalidated**: No longer a valid transfer mechanism
2. **SCCs remain valid** but require case-by-case assessment
3. **Supplementary measures required** when destination country law impinges on EU-level protection
4. **DPAs must suspend/ban transfers** if SCCs cannot be complied with

## Transfer Impact Assessment (TIA)
Required for each cross-border data flow:
1. Map data flows and processing activities
2. Assess destination country's legal framework (surveillance laws, government access)
3. Evaluate SCC effectiveness in destination
4. Identify and implement supplementary measures
5. Document and review annually

## Supplementary Technical Measures
- **Encryption**: CMK/HYOK so provider cannot access plaintext
- **Pseudonymization**: Split identifiers from payload across jurisdictions
- **Split processing**: Data processed in EU, only tokens transferred
- **Client-side encryption**: Provider has no decryption capability

## Post-Schrems Enforcement
- Meta fined EUR 1.2 billion (Ireland DPC, 2023) for unlawful EU-US transfers

## References
- CJEU C-311/18: Data Protection Commissioner v Facebook Ireland and Maximillian Schrems
