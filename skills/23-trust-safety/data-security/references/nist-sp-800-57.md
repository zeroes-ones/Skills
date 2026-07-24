# NIST SP 800-57 — Key Management Recommendations

## Overview
NIST SP 800-57 provides cryptographic key management guidance, covering key lifecycle from generation through destruction.

## Key States
1. **Pre-activation**: Generated but not yet available for use
2. **Active**: Available for cryptographic operations
3. **Deactivated**: Not available for operations, retained for decryption only
4. **Compromised**: Key material may have been exposed
5. **Destroyed**: All key material securely destroyed

## Cryptoperiod Recommendations
- **Symmetric data encryption keys**: Maximum 3 years
- **Private signature keys**: 1-3 years
- **Master keys (KMS root)**: Maximum 1 year (rotate frequently)
- **TLS session keys**: Single session
- **Data at rest keys (DEK)**: Rotate annually minimum; 90 days for RESTRICTED data

## Protection Requirements
- Keys must be protected at the same or higher level as the data they protect
- Master keys require HSM (FIPS 140-2 Level 3+)
- Split knowledge and dual control for root key operations
- Automated rotation with version tracking

## References
- NIST SP 800-57 Part 1 Rev 5: https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev/5/final
