# NIST SP 800-88 — Guidelines for Media Sanitization

## Overview
NIST Special Publication 800-88 Revision 1 provides guidance on securely sanitizing electronic media to prevent unauthorized data recovery.

## Sanitization Categories

### Clear
Logical techniques to sanitize data against non-invasive recovery attempts. Overwrites user-addressable storage with non-sensitive data.

### Purge
Physical or logical techniques rendering data recovery infeasible using state-of-the-art laboratory techniques. Includes:
- Cryptographic Erase (CE): Destroy encryption keys
- Block erase for SSDs
- Degaussing for magnetic media

### Destroy
Renders data recovery infeasible and media unusable:
- Incinerate, shred, pulverize, melt
- Disintegration with 2mm particle size

## Media-Specific Guidance
- **SSD**: Cryptographic erase preferred (wear leveling makes overwrite unreliable)
- **HDD**: Multi-pass overwrite or degaussing
- **Cloud**: Crypto-shredding (delete CMK from KMS)
- **Tape**: Degaussing, shredding

## Verification
- Clear/Purge: Sample-based verification
- Destroy: Witnessed with certificate of destruction

## References
- NIST SP 800-88 Rev 1: https://csrc.nist.gov/publications/detail/sp/800-88/rev-1/final
