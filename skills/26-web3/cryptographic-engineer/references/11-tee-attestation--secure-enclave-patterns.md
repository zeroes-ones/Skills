## 11. TEE Attestation & Secure Enclave Patterns

### 11.1 Remote Attestation Protocol

```
Enclave (Prover)                    Verifier (Relying Party)
     |                                        |
     |--- 1. Request attestation ----------->|
     |<-- 2. Nonce + expected PCR values ----|
     |                                        |
     | 3. Generate Quote (report)             |
     |    - Enclave identity (MRENCLAVE)      |
     |    - TCB level (CPUSVN, ISVSVN)        |
     |    - User data = Hash(nonce, pk)       |
     |                                        |
     |--- 4. Quote + ephemeral PK ---------->|
     |                                        |
     |    5. Verify attestation:              |
     |       a) Quote signature (IAS/DCAP)    |
     |       b) MRENCLAVE matches expected    |
     |       c) TCB level >= minimum          |
     |       d) Nonce matches                 |
     |       e) Certificate chain valid       |
     |                                        |
     |<-- 6. Establish secure channel --------|
     |    (encrypt session key to enclave PK) |
```

### 11.2 Sealing — Persisting State Across Enclave Restarts

```cpp
// SGX: Seal data to enclave identity (MRENCLAVE) or signing identity (MRSIGNER)
sgx_status_t seal_secret(const uint8_t *secret, size_t len,
                         uint8_t *sealed_blob, size_t sealed_len) {
    // Policy: MRENCLAVE — only this exact enclave binary can unseal
    sgx_sealed_data_t *sealed = (sgx_sealed_data_t *)sealed_blob;
    
    // Key policy: bind to enclave identity + TCB
    // KEYPOLICY_MRENCLAVE: exact binary match (secure, breaks on updates)
    // KEYPOLICY_MRSIGNER: any enclave from same developer (flexible)
    uint16_t key_policy = SGX_KEYPOLICY_MRENCLAVE;
    
    sgx_status_t ret = sgx_seal_data(
        0,                    // Additional MAC text
        NULL,                 // No additional text
        len, secret,
        sealed_len, sealed
    );
    
    // ⚠ Store sealed blob on untrusted storage (disk, database)
    // It's encrypted + authenticated with hardware-derived key
    return ret;
}
```

### 11.3 AMD SEV-SNP Attestation Verification

```python
# AMD SEV-SNP: Verify attestation report with VCEK certificate chain
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
import requests

def verify_sev_attestation(report: bytes, expected_measurement: bytes) -> bool:
    """Verify SEV-SNP attestation report against AMD KDS"""
    
    # 1. Parse attestation report
    attestation = parse_sev_report(report)
    
    # 2. Fetch VCEK certificate from AMD KDS (Key Distribution Service)
    chip_id = attestation.chip_id
    vcek_url = f"https://kdsintf.amd.com/vcek/v1/{chip_id}"
    response = requests.get(vcek_url)
    
    chain_pem = f"{response.text}\n{AMD_ROOT_CA_PEM}\n{AMD_SEV_CA_PEM}"
    
    # 3. Verify certificate chain: VCEK -> SEV-CA -> AMD Root
    vcek_cert = x509.load_pem_x509_certificate(response.text.encode())
    ca_cert = x509.load_pem_x509_certificate(AMD_SEV_CA_PEM.encode())
    root_cert = x509.load_pem_x509_certificate(AMD_ROOT_CA_PEM.encode())
    
    verify_cert_chain(vcek_cert, ca_cert, root_cert)
    
    # 4. Verify report signature using VCEK public key
    vcek_pubkey = vcek_cert.public_key()
    verify_report_signature(report, vcek_pubkey)
    
    # 5. Validate measurement and policy
    assert attestation.measurement == expected_measurement  # Launch digest match
    assert attestation.policy & POLICY_DEBUG == 0  # Debug must be disabled
    assert attestation.tcb_version >= MINIMUM_TCB
    
    return True
```

---
