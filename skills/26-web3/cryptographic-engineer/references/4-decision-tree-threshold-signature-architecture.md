## 4. Decision Tree: Threshold Signature Architecture

```
┌── Threshold Signature Architecture ─────────────────────────────┐
│                                                                 │
│  Requirements analysis:                                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Need non-interactive signing (no co-signer coordination)?  │  │
│  │  └─► BLS Threshold — single-round, aggregatable, but      │  │
│  │     requires pairing-friendly curve (BLS12-381, BN254)     │  │
│  │     ⚠ Keygen requires DKG (distributed key generation)     │  │
│  │                                                           │  │
│  │ Need identifiable aborts (know which party refused)?       │  │
│  │  └─► FROST (Schnorr) — 2-round signing, identifies        │  │
│  │     misbehaving signers, compatible with standard Schnorr  │  │
│  │     ⚠ Interactive: all signers must participate round 1    │  │
│  │                                                           │  │
│  │ Need ECDSA compatibility (Bitcoin/Ethereum)?               │  │
│  │  └─► GG20/GG18/CGGMP — multi-round, supports secp256k1    │  │
│  │     ⚠ 5+ rounds, higher latency, Paillier ZK required      │  │
│  │                                                           │  │
│  │ Need committee rotation without re-keying?                 │  │
│  │  └─► Proactive secret sharing with key resharing          │  │
│  │     (Herzberg dynamic proactive scheme)                    │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Protocol comparison:                                            │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────────┐   │
│  │ Protocol │ Rounds   │ Curve    │ Size     │ Abort ID     │   │
│  ├──────────┼──────────┼──────────┼──────────┼──────────────┤   │
│  │ FROST    │ 2        │ secp256k1│ 64B sig  │ Yes          │   │
│  │ BLS      │ 1 (non-i)│ BLS12-381│ 96B sig  │ No           │   │
│  │ GG20     │ 5-7      │ secp256k1│ 64B sig  │ Yes          │   │
│  │ CGGMP    │ 4-6      │ secp256k1│ 64B sig  │ Yes          │   │
│  └──────────┴──────────┴──────────┴──────────┴──────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**FROST threshold signing (Rust):**
```rust
// frost-secp256k1: t-of-n Schnorr threshold signature
use frost_secp256k1 as frost;
use rand::thread_rng;

// Round 1: Each signer generates nonces and commitments
let mut rng = thread_rng();
let (secret_package, round1_package) = frost::keys::KeyPackage::try_from(participant_secret)
    .unwrap()
    .new_nonce(&mut rng)
    .unwrap();

// Coordinator aggregates commitments
let signing_package = frost::SigningPackage::new(round1_packages, message);

// Round 2: Each signer produces signature share
let signature_share = frost::sign(&signing_package, &secret_package, &round1_package)
    .map_err(|e| IdentifiableAbort::from(e))?;  // ← identifiable abort

// Coordinator aggregates shares into final Schnorr signature
let group_signature = frost::aggregate(&signing_package, &signature_shares, &group_public_key)
    .unwrap();
verify(&group_public_key, message, &group_signature);  // Standard Schnorr verify
```

**BLS threshold aggregation (no signer interaction):**
```python
# Each party signs locally; aggregator combines
from py_ecc.bls import G2ProofOfPossession as bls

# Party i signs with its key share (no coordination needed)
sig_share_i = bls.Sign(sk_share_i, message)

# Aggregator: combine t shares via Lagrange interpolation
aggregated_sig = bls.Aggregate(sig_shares)  # O(n) aggregation, constant-size result

# Verify: PK is group public key (reconstructed from shares)
bls.Verify(group_pk, message, aggregated_sig)  # True if >= t honest signers
```

---
