# Azure Key Vault — Secrets, Keys, and Certificates

## Overview
Azure Key Vault provides secure storage and management of secrets (API keys, passwords, connection strings), cryptographic keys, and TLS/SSL certificates with HSM backing.

## Service Tiers
- **Standard**: Software-protected keys (FIPS 140-2 Level 2)
- **Premium**: HSM-protected keys (FIPS 140-2 Level 3)

## Key Management
- **Software-protected**: Keys generated and stored in software
- **HSM-protected**: Keys generated and stored in dedicated HSM (Premium only)
- **BYOK**: Import keys from on-premises HSM
- **Key rotation**: Manual or automated via Azure Automation + Event Grid

## Data Protection Patterns
- **Column-level encryption**: Azure SQL Always Encrypted with Key Vault
- **TDE**: Azure SQL TDE with Key Vault (BYOK)
- **Storage encryption**: Azure Storage Service Encryption with CMK
- **VM disk encryption**: Azure Disk Encryption with Key Vault (BitLocker/DM-Crypt)

## Access Control
- **RBAC**: Azure RBAC on management plane (who can manage vault)
- **Access Policy**: Data plane permissions (who can read keys/secrets)
- **Network**: VNet service endpoints, Private Link, IP firewall

## References
- Azure Key Vault: https://learn.microsoft.com/en-us/azure/key-vault/
