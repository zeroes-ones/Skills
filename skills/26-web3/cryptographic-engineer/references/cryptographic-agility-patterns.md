# Cryptographic Agility Patterns — Migration, Inventory, Negotiation

## Algorithm Lifecycle Management

```
                    ┌─────────┐
                    │ ACTIVE  │ ← New deployments use these algorithms
                    └────┬────┘
                         │ Deprecation announced (e.g., 2yr notice)
                    ┌────▼───────┐
                    │ DEPRECATED │ ← Accept existing, reject new
                    └────┬───────┘
                         │ Migration window closed
                    ┌────▼────┐
                    │ LEGACY  │ ← Verify only, migration mandatory
                    └────┬────┘
                         │ Cryptographic irrelevance
                    ┌────▼──────┐
                    │ FORBIDDEN │ ← Reject outright (SHA-1, RSA-1024)
                    └───────────┘
```

## Centralized Crypto Registry

Single source of truth for what algorithms are permitted:

```python
class CryptoRegistry:
    """Controls all cryptographic algorithm selection and negotiation."""
    
    def __init__(self):
        self.algorithms = {}
        self.policies = {}  # Per-category policies
    
    def register(self, algo: AlgorithmProto):
        """Register algorithm with metadata and implementation."""
        self.algorithms[algo.id] = algo
    
    def negotiate(self, peer_offers: list[str], category: str):
        """Select best mutually-supported algorithm.
        
        Priority: PQC-first > ACTIVE classical > DEPRECATED (warn) > reject
        """
        ours = [a for a in self.algorithms.values() 
                if a.category == category and a.status == ACTIVE]
        ours.sort(key=lambda a: (0 if a.is_pqc else 1, -a.security_level))
        
        for algo in ours:
            if algo.id in peer_offers:
                return algo
        
        # No common active algorithm — fail closed
        return None
```

## Hybrid Middleware Pattern

Transparent dual-computation for migration:

```
Input Data
    │
    ├──► Classical KEM (X25519 ECDH) ──► ss_classical ──┐
    │                                                     │
    ├──► PQC KEM (ML-KEM-768) ──► ss_pqc ────────────────┤
    │                                                     │
    └──────────── KDF(ss_classical || ss_pqc) ────────────┘
                              │
                         Final Key (256-bit)
```

**Fail-closed:** If either KEM fails, the entire operation fails. Never fall back to single-KEM security.

## Protocol Negotiation Downgrade Prevention

```
Client → Server: ["ECDHE-X25519", "ML-KEM-768", "RSA-2048"]
                                        ↑
Server sorts by priority:               │
  1. ML-KEM-768 (PQC, highest pri) ─────┘  ← Selected
  2. ECDHE-X25519 (DEPRECATED, skip)
  3. RSA-2048 (LEGACY, skip)

Server → Client: ML-KEM-768 (only option — single-value response prevents downgrade)
```

## Inventory Automation

```bash
# Scan all TLS endpoints for crypto inventory
nmap --script ssl-enum-ciphers -p 443 production-hosts.txt \
  | tee crypto-inventory-$(date +%Y%m%d).log

# Classify endpoints by PQC readiness
# 1. PQC-ready: ML-KEM-768 or ML-DSA-44 in cipher suite
# 2. Hybrid-ready: ECDHE + ML-KEM in same suite
# 3. Classical-only: ECDHE or DHE without PQC
# 4. Vulnerable: RSA key exchange, TLS < 1.2, weak ciphers
```
