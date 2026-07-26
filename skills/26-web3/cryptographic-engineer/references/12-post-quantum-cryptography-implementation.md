## 12. Post-Quantum Cryptography Implementation

### 12.1 ML-KEM Key Encapsulation (liboqs)

```python
# OQS Python bindings: ML-KEM-768 (FIPS 203, NIST standard)
import oqs

# Alice: Generate keypair
with oqs.KeyEncapsulation("ML-KEM-768") as alice:
    alice_public = alice.generate_keypair()
    # Encapsulation: Bob creates shared secret + ciphertext
    with oqs.KeyEncapsulation("ML-KEM-768") as bob:
        ciphertext, bob_shared = bob.encap_secret(alice_public)
    # Decapsulation: Alice recovers shared secret
    alice_shared = alice.decap_secret(ciphertext)
    assert bob_shared == alice_shared  # 256-bit shared secret
```

### 12.2 Hybrid X.509 Certificates

```python
# Hybrid certificate: ECDSA P-256 + ML-DSA-44 signatures
# Two independent signatures on the same TBSCertificate
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ec

def create_hybrid_cert(csr: x509.CertificateSigningRequest,
                       ca_ecdsa_key, ca_mldsa_key) -> x509.Certificate:
    """Build X.509 cert with dual signature algorithm"""

    builder = x509.CertificateBuilder()
    builder = builder.subject_name(csr.subject)
    builder = builder.issuer_name(ca_cert.subject)
    builder = builder.public_key(csr.public_key())
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.not_valid_before(datetime.utcnow())
    builder = builder.not_valid_after(datetime.utcnow() + timedelta(days=365))

    # Standard ECDSA signature (classical)
    cert_bytes = builder.sign(ca_ecdsa_key, hashes.SHA256())

    # ML-DSA-44 alternate signature (PQC) in certificate extension
    # OID: 2.16.840.1.101.3.4.3.17 (id-alg-mldsa-44)
    mldsa_sig = sign_mldsa44(cert_bytes.tbs_certificate_bytes, ca_mldsa_key)

    cert = cert_bytes.add_extension(
        x509.UnrecognizedExtension(
            oid=MLDSA44_SIG_OID,
            value=mldsa_sig
        ), critical=False
    )
    return cert

# ⚠ Both signatures MUST validate — single-signature acceptance = downgrade attack
```

### 12.3 Crypto Inventory & Migration Timeline

```python
# Automated crypto inventory via TLS fingerprinting
def inventory_crypto_endpoints(hosts: list[str]) -> dict:
    """Scan endpoints, classify by quantum risk, generate migration plan"""
    results = {}
    for host in hosts:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
            s.connect((host, 443))
            cipher = s.cipher()
            cert_der = s.getpeercert(binary_form=True)
            cert = x509.load_der_x509_certificate(cert_der)

            results[host] = {
                "kex_algorithm": cipher[0],           # e.g., ECDHE-RSA
                "sig_algorithm": cert.signature_algorithm_oid._name,
                "pqc_ready": is_pqc_cipher(cipher),   # False for classical
                "hnld_risk": has_long_lived_data(host),  # Harvest-now-decrypt-later
                "migration_priority": calculate_priority(cipher, cert),
            }
    return results

# Migration timeline:
# Year 0-1: Inventory + hybrid TLS 1.3 deployment
# Year 1-2: PQC-only internal services, hybrid external
# Year 2-3: Deprecate RSA/ECDH, PQC-only for long-lived secrets
# Year 3-5: Remove classical fallback (full PQC migration)
```

---
