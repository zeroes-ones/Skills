## 5. Decision Tree: TEE Platform Selection

```
┌── TEE Platform Selection ───────────────────────────────────────┐
│                                                                  │
│  Workload characterization:                                      │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Application-level enclave (isolated process within VM)?     │  │
│  │  ├─ Intel SGX (TDX for full VM) — 256MB EPC, DCAP v4       │  │
│  │  └─ AWS Nitro Enclaves — full Linux VM, vsock comms        │  │
│  │                                                             │  │
│  │ Full VM confidential computing (lift-and-shift)?            │  │
│  │  ├─ AMD SEV-SNP — encrypted VM state, VCEK attestation     │  │
│  │  ├─ Intel TDX — full VM TEE, MRTD measurement, 1TB max     │  │
│  │  └─ ARM CCA Realm — hardware-enforced, RMM firmware        │  │
│  │                                                             │  │
│  │ Multi-cloud portability requirement?                        │  │
│  │  └─ Enarx (Wasm-based), K8s Confidential Containers (CoCo) │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Platform comparison:                                            │
│  ┌──────────┬──────────┬────────────┬──────────┬─────────────┐   │
│  │ Platform │ Enclave  │ Attestation│ Memory   │ Cloud       │   │
│  ├──────────┼──────────┼────────────┼──────────┼─────────────┤   │
│  │ SGX DCAP │ Process  │ ECDSA/DCAP │ 256MB    │ Azure/Ali   │   │
│  │ SEV-SNP  │ Full VM  │ VCEK cert  │ 4TB+     │ AWS/GCP/Az  │   │
│  │ Nitro    │ VM (nop) │ PCR-based  │ Config   │ AWS only    │   │
│  │ TDX      │ Full VM  │ DCAP ext   │ 1TB      │ Azure/GCP   │   │
│  │ ARM CCA  │ VM Realm │ CCA token  │ Config   │ Emerging    │   │
│  └──────────┴──────────┴────────────┴──────────┴─────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

**AWS Nitro Enclaves attestation (Rust):**
```rust
// Nitro Secure Module (NSM) API for cryptographic attestation
use nsm_lib::{Request, Response, Digest};

let request = Request::Attestation {
    public_key: Some(&signing_key.public_bytes()),
    user_data: Some(pcr_binding_hash),   // Bind to specific PCR values
    nonce: Some(&random_nonce),           // Prevents replay attacks
};

let nsm_fd = nsm_lib::nsm_lib_init();
let response = nsm_lib::nsm_send_request(nsm_fd, &request)
    .expect("NSM attestation failed");

// Verify: Document -> AWS Public Cert -> AWS Root CA
let attestation_doc = parse_cbor(&response.attestation_document);
verify_aws_certificate_chain(&attestation_doc.cabundle)
    .map_err(|_| "CRITICAL: Chain validation skipped")?;

assert_eq!(attestation_doc.pcrs[0], expected_enclave_image_hash);
```

**Intel SGX DCAP quote verification (C++):**
```cpp
// SGX DCAP v4: Quote verification with collateral
sgx_ql_qe_report_info_t qve_report_info;
sgx_quote3_t *p_quote = (sgx_quote3_t *)quote_buffer;

// Get PCK cert chain, TCB info, QE identity
tee_supplicant_get_collateral(&p_quote->certification_data, &collateral);

quote3_error_t ret = sgx_qv_verify_quote(
    p_quote, quote_size, &collateral, current_time,
    &verification_result,
    supplemental_data_size > 0  // LVI/MMIO mitigation status
);

// Non-trivial: must check isv_enclave_report_status != QV_RESULT_OK
if (verification_result.isv_enclave_report_status != SGX_QL_QV_RESULT_OK) {
    report_error("Enclave identity mismatch or revoked TCB");
}
```

---
