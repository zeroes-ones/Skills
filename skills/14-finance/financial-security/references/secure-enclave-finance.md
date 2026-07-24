# Secure Enclaves & Confidential Computing for Finance

AWS Nitro Enclaves, Azure confidential computing, and GCP Confidential
VMs for payment processing, KYC data protection, and proprietary algorithm
isolation in regulated financial environments.

## Why Confidential Computing for Finance?

Financial services process uniquely sensitive data:
- **KYC data**: PII that must not be accessible to cloud operators
- **Payment processing**: cardholder data requiring PCI DSS isolation
- **AML/transaction monitoring**: compliance algorithms considered IP
- **Proprietary trading models**: algorithmic edge that must be protected

Confidential computing provides hardware-level encryption for data in-use
(not just at rest or in transit), preventing even the hypervisor/Ops team
from accessing workloads.

## AWS Nitro Enclaves

### Architecture
```
+-----------------------------------+
| Parent EC2 Instance               |
|  +-----------------------------+  |
|  | Application (payment API)   |  |
|  |    ↓ vsock (local socket)   |  |
|  | Nitro Enclave               |  |
|  |  +-----------------------+  |  |
|  |  | Payment Processing     |  |  |
|  |  | (encrypted memory,    |  |  |
|  |  |  no persistent disk,  |  |  |
|  |  |  no external network, |  |  |
|  |  |  no interactive access)|  |  |
|  |  +-----------------------+  |  |
|  +-----------------------------+  |
+-----------------------------------+
           ↓ Cryptographic Attestation
    AWS Nitro Hypervisor verifies enclave is running approved code
```

### Use Case: PCI DSS Payment Processing

```python
# Parent application (EC2) — receives encrypted card data from client
card_data_ciphertext = receive_payment_from_client(session_key_encrypted_payload)

# Send to enclave via vsock (local, encrypted channel)
enclave_result = vsock_send(ENCLAVE_CID, {
    "operation": "authorize",
    "encrypted_payload": card_data_ciphertext,
    "merchant_id": merchant.id
})

# Enclave decrypts card data, processes payment, returns auth code
# Card data NEVER in plaintext on parent instance
auth_code = enclave_result["auth_code"]
```

### Attestation Flow
1. Enclave boots → Nitro hypervisor measures (PCRs) all code/data initialized
2. Enclave generates attestation document signed by Nitro's root of trust
3. Parent application or external service validates attestation document
4. Only then does parent send sensitive data to enclave
5. Attestation proves: running approved code, on real AWS Nitro, no modifications

## Azure Confidential Computing

### Options
| Service | Protection Level | Use When |
|---------|-----------------|----------|
| Azure DCsv3 VMs (Intel SGX) | Application-level enclave + encrypted memory | Legacy SGX apps, granular secrets |
| Azure DCasv5/DCadsv5 (AMD SEV-SNP) | Full VM encryption, no code changes | Lift-and-shift workloads |
| Azure Confidential AKS | Container-level, encrypted node pools | Kubernetes-native finance apps |
| Azure SQL Always Encrypted with Secure Enclaves | Query on encrypted data | KYC database with searchable encryption |

### AMD SEV-SNP VM Encryption (Easiest Path)
- Full VM memory encrypted with hardware key (AMD EPYC processor)
- Hypervisor cannot read guest memory — prevents cloud admin data access
- No application changes: ordinary Linux VM, fully encrypted at hardware level
- Attestation via Azure Attestation Service: verify VM identity and platform integrity
- Use for: lift-and-shift of existing financial workloads requiring data-in-use protection

### Intel SGX (Fine-Grained — Requires Application Changes)
- Define trusted code regions via SGX SDK (OpenEnclave, Gramine)
- Only code within enclave can access enclave memory
- Protected from: OS, hypervisor, BIOS, SMM, DMA
- Attestation: Intel IAS or DCAP verifies enclave code identity
- Use for: protecting a specific secret (not the entire application)

## GCP Confidential VMs

### AMD SEV and SEV-ES
- Memory encryption: AMD Secure Encrypted Virtualization
- Transparent: run standard Linux VM images without modification
- Not compatible with: live migration between hosts (SEV-ES)

### Key Management
- Cryptographic keys generated per-VM, managed by AMD secure processor
- GCP handles attestation via Shielded VM integration
- Attestation reports verifiable by Google Attestation Service

### Finance-Specific Patterns
```yaml
AML Workload:
  VM: GCP Confidential VM (AMD SEV), Shielded Boot, vTPM
  Data: encrypted GCS bucket (CSEK — Customer-Supplied Encryption Key)
  Processing: confidential computing for ML model + KYC data
  Output: encrypted results to customer-controlled key

Payment Processing:
  Enclave: AWS Nitro for PCI DSS scope reduction
  Attestation: verify enclave identity before sending card data
  Key material: injected via attestation-verified channel
  Logging: censored — no PAN, CVV, full track in logs
```

## Hardware-Based Attestation for Financial Algorithms

### The Pattern
1. Financial institution has proprietary trading/risk model (binary + weights)
2. Model runs in confidential computing environment (Nitro Enclave, SGX, SEV)
3. Before model is loaded, cloud provider attests environment is genuine:
   - Boot measurement (PCR0): firmware hash
   - Kernel measurement (PCR1): kernel + initrd hash  
   - Application measurement (PCR2): container/enclave image hash
4. Institution only releases model weights if attestation passes
5. Enclave processes data, returns results, never exposes model or raw data

### Audit Trail
```
Every enclave launch generates:
- Attestation document (cryptographically signed by hardware root of trust)
- PCR values: cryptographic hashes of boot chain
- Timestamp from Nitro/SEV attestation service
- These are logged immutably for regulatory audit

Regulator can cryptographically verify:
1. Enclave was real hardware (not emulated/simulated)
2. Enclave ran approved code (PCR matches known-good hash)
3. No modification occurred after attestation
```
