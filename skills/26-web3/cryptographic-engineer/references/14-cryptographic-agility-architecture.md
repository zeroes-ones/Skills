## 14. Cryptographic Agility Architecture

### 14.1 Algorithm Inventory & Registration

```python
# Cryptographic algorithm registry with agility support
# Central registry to manage migration and deprecation
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, Dict, Optional

class AlgorithmStatus(Enum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"    # Accept existing, don't create new
    LEGACY = "legacy"            # Verify only, migration required
    FORBIDDEN = "forbidden"      # Reject outright (e.g., SHA-1, RSA-1024)

@dataclass
class CryptoAlgorithm:
    name: str
    category: str            # "kex", "signature", "encryption", "hash"
    status: AlgorithmStatus
    deprecation_date: Optional[datetime]
    migration_target: Optional[str]
    impl: Callable

class CryptoRegistry:
    """Central algorithm registry — single source of truth for crypto policy"""
    def __init__(self):
        self._algos: Dict[str, CryptoAlgorithm] = {}
    
    def register(self, algo: CryptoAlgorithm):
        self._algos[algo.name] = algo
    
    def get_active(self, category: str) -> list[CryptoAlgorithm]:
        """Get active algorithms for a category (used for selection)"""
        return [a for a in self._algos.values()
                if a.category == category and a.status == AlgorithmStatus.ACTIVE]
    
    def negotiate(self, peer_algos: list[str], category: str) -> Optional[CryptoAlgorithm]:
        """Protocol negotiation with downgrade prevention.
        
        Sorts by preference: PQC-first, then classical.
        ⚠ Never selects DEPRECATED or FORBIDDEN algorithms.
        """
        our_preferred = self.get_active(category)
        our_preferred.sort(key=lambda a: 0 if "ml-" in a.name else 1)  # PQC first
        
        for algo in our_preferred:
            if algo.name in peer_algos and algo.status == AlgorithmStatus.ACTIVE:
                return algo  # Selected best mutually-supported algorithm
        
        return None  # No common algorithm — fail closed, refuse connection

# Example: TLS-like negotiation
registry = CryptoRegistry()
registry.register(CryptoAlgorithm("ECDHE-X25519", "kex", AlgorithmStatus.DEPRECATED,
    deprecation_date=datetime.now() + timedelta(days=730), migration_target="ML-KEM-768"))
registry.register(CryptoAlgorithm("ML-KEM-768", "kex", AlgorithmStatus.ACTIVE))
registry.register(CryptoAlgorithm("RSA-2048", "kex", AlgorithmStatus.LEGACY))

# Attacker tries downgrade: offers only RSA-2048
selected = registry.negotiate(["RSA-2048"], "kex")
assert selected is None  # ⚠ RSA-2048 is LEGACY, negotiation MUST fail

# Proper negotiation: offers classical + PQC
selected = registry.negotiate(["ECDHE-X25519", "ML-KEM-768"], "kex")
assert selected.name == "ML-KEM-768"  # PQC preferred
```

### 14.2 Hybrid Scheme Middleware

```python
# Transparent hybrid layer: classical + PQC dual computation
class HybridKEM:
    """Dual KEM: produces key_material = KDF(classical_ss || pqc_ss)
    
    Both key exchanges MUST complete successfully.
    Single failure = reject connection (downgrade prevention).
    """
    def __init__(self, classical: str = "X25519", pqc: str = "ML-KEM-768"):
        self.classical_kem = ClassicalKEM(classical)
        self.pqc_kem = PQKEM(pqc)
    
    def encapsulate(self, classical_pk: bytes, pqc_pk: bytes) -> tuple:
        ct_classical, ss_classical = self.classical_kem.encap(classical_pk)
        ct_pqc, ss_pqc = self.pqc_kem.encap(pqc_pk)
        
        # Both MUST succeed — fail closed
        if not ss_classical or not ss_pqc:
            raise DowngradePreventionError("Refusing to fall back to single KEM")
        
        # Key derivation: KDF(ss_classical || ss_pqc)
        combined_key = HKDF_SHA256(ss_classical + ss_pqc, salt=None, info=b"hybrid-kem")
        return (ct_classical + ct_pqc), combined_key
```

---
