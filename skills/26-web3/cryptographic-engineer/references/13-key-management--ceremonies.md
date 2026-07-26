## 13. Key Management & Ceremonies

### 13.1 HSM Integration via PKCS#11

```python
# PKCS#11: Hardware Security Module integration
# Uses SoftHSM2 for development, production HSM (Thales/Gemalto/Utimaco)
from PyKCS11 import PyKCS11

pkcs11 = PyKCS11.PyKCS11Lib()
pkcs11.load("/usr/lib/softhsm/libsofthsm2.so")  # Production: vendor .so
pkcs11.initialize()

slots = pkcs11.getSlotList(tokenPresent=True)
session = pkcs11.openSession(slots[0])

# Authenticate to HSM (split-knowledge in production: two officers enter PIN halves)
session.login("1234")  # Production: dual-control PIN entry

# Generate RSA-4096 key inside HSM (key never leaves hardware)
pub_template = [
    (PyKCS11.CKA_CLASS, PyKCS11.CKO_PUBLIC_KEY),
    (PyKCS11.CKA_TOKEN, True),
    (PyKCS11.CKA_MODULUS_BITS, 4096),
    (PyKCS11.CKA_PUBLIC_EXPONENT, (0x01, 0x00, 0x01)),
    (PyKCS11.CKA_LABEL, "Root-CA-2026"),
]
priv_template = [
    (PyKCS11.CKA_CLASS, PyKCS11.CKO_PRIVATE_KEY),
    (PyKCS11.CKA_TOKEN, True),
    (PyKCS11.CKA_PRIVATE, True),
    (PyKCS11.CKA_SENSITIVE, True),      # Cannot be extracted
    (PyKCS11.CKA_EXTRACTABLE, False),   # ⚠ CRITICAL: Prevent export
    (PyKCS11.CKA_SIGN, True),
    (PyKCS11.CKA_LABEL, "Root-CA-2026"),
]
(pub_key, priv_key) = session.generateKeyPair(pub_template, priv_template)

# Sign operation inside HSM
mechanism = PyKCS11.Mechanism(PyKCS11.CKM_SHA256_RSA_PKCS)
signature = session.sign(priv_key, data_to_sign, mechanism)

session.logout()
session.closeSession()
```

### 13.2 Entropy Sourcing & Health Monitoring

```python
# Multi-source entropy mixing for key ceremonies
# NEVER trust a single entropy source — mix multiple independent sources
import os, time, hashlib
from struct import pack

def ceremony_entropy(num_bytes: int = 64) -> bytes:
    """Mix entropy from hardware RNG + timing jitter + CPU RDRAND"""
    sources = []

    # Source 1: OS CSPRNG (getrandom syscall)
    sources.append(os.urandom(num_bytes))

    # Source 2: CPU RDRAND (Intel/AMD hardware RNG)
    # Each RDRAND instruction: 64 bits of hardware entropy
    rdrand_bytes = b""
    for _ in range(num_bytes // 8):
        rdrand_bytes += pack("<Q", rdrand64())  # CPU intrinsic
    sources.append(rdrand_bytes)

    # Source 3: Timing jitter (clock jitter entropy, SP 800-90B)
    jitter = b""
    for _ in range(num_bytes * 8):
        t1 = time.perf_counter_ns()
        time.sleep(0)  # Yield — measurement noise from scheduler
        t2 = time.perf_counter_ns()
        jitter += pack("<Q", t2 - t1)
    sources.append(hashlib.sha512(jitter).digest()[:num_bytes])

    # Mix via HKDF: entropy = HKDF-Extract(source1 || source2 || source3)
    mixed = hashlib.sha512(b"".join(sources)).digest()
    return mixed[:num_bytes]

# ⚠ Continuous entropy health monitoring (SP 800-90B):
# - Monitor entropy source statistics (min-entropy estimate)
# - Alert if source produces repeat outputs or fails statistical tests
# - Fail closed: refuse key generation if entropy quality < threshold
```

---
