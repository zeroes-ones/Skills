# TEE Attestation Workflow — SGX/SEV/Nitro/CCA

## Intel SGX DCAP (Data Center Attestation Primitives)

### Attestation Flow (v4 API)
1. Enclave generates REPORT (hardware-signed, MRENCLAVE + user data)
2. Quoting Enclave (QE) verifies REPORT, generates QUOTE (ECDSA-signed)
3. Verifier fetches collateral from Intel PCS (Provisioning Certification Service):
   - PCK Certificate (Platform Certification Key, per-CPU)
   - TCB Info (Trusted Computing Base version, CPUSVN, ISVSVN)
   - QE Identity (Quoting Enclave signing key)
4. Verifier checks:
   - Quote signature against PCK
   - PCK chain → processor CA → Intel root
   - TCB status: not revoked, meets minimum security version
   - MRENCLAVE matches expected enclave measurement
   - User data matches expected nonce

### TCB Recovery Handling
- Monitor `tcbStatus` in supplemental data
- `UpToDate`, `OutOfDate`, `ConfigurationNeeded`, `Revoked`
- Alert: `OutOfDate` + high-value workload → restart with updated microcode

## AMD SEV-SNP

### Attestation Report Verification
1. Guest requests ATTESATION_REPORT from PSP (Platform Security Processor)
2. PSP generates REPORT signed by VCEK (Versioned Chip Endorsement Key)
3. Verifier fetches VCEK certificate from AMD KDS (Key Distribution Service):
   - URL: `https://kdsintf.amd.com/vcek/v1/{chip_id}`
4. Verify chain: VCEK → SEV-SNP CA → AMD Root CA (ARK/ASK)
5. Validate: MEASUREMENT (launch digest), POLICY (debug disabled), TCB version

### Critical Checks
- POLICY bit 1 (Debug): Must be 0 for production
- POLICY bit 2 (Migration Agent): Must be controlled
- TCB version >= minimum required for workload sensitivity

## AWS Nitro Enclaves

### Attestation via NSM (Nitro Secure Module)
1. Enclave requests attestation document from NSM via vsock
2. NSM signs document with Nitro key (PCR-based measurements)
3. Document includes:
   - PCR0-PRC3 (Platform Configuration Registers)
   - Instance ID, AWS account ID
   - User-provided public key and nonce (for secure channel establishment)
4. Verifier validates:
   - Document signature via AWS Nitro attestation public certificate
   - PCR values match expected enclave image (kernel + init + application)
   - Nonce matches to prevent replay

## ARM CCA (Confidential Compute Architecture)

### Realm Attestation
1. RMM (Realm Management Monitor) provides CCA attestation token
2. Token signed by platform attestation key (CPAK)
3. Verifier validates via DICE certificate chain to CCA root
4. Realm Initial Measurement (RIM) defines expected state

## Common Attestation Failure Modes
1. **Expired collateral:** Intel PCS/AMD KDS certificates expire; cache with refresh
2. **Clock skew:** Attestation includes timestamp; NTP synchronization critical
3. **TCB downgrade attack:** VM migrated to older microcode; check TCB monotonicity
4. **Measurement mismatch:** Container/image update changes MRENCLAVE; update expected values
