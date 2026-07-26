# Threshold Key Resharing — Committee Rotation, Proactive Security

## Proactive Security Model

Threshold cryptography with static shares is vulnerable to **mobile adversary**: attacker compromises parties over time, eventually collecting `t` shares to reconstruct the key.

**Proactive security:** Periodically refresh shares so old shares become useless.

## Herzberg Dynamic Proactive Scheme (CRYPTO 1995)

### Protocol

```
Setup: Group secret s, threshold t, committee size n

Epoch transition (old committee → new committee):
  1. Each old holder i (with share s_i^old):
     a. Generate random polynomial f_i of degree (t-1) with f_i(0) = s_i^old
     b. Send sub-share f_i(j) to new holder j (via secure channel)

  2. Each new holder j:
     a. Collect sub-shares from at least t old holders
     b. Compute new share: s_j^new = sum(Lambda_i * f_i(j)) mod q
        where Lambda_i is Lagrange coefficient for old holders

  3. Verification:
     a. New holders verify shares against public commitments
     b. Old shares s_i^old are securely deleted

  Result: Same group secret s, new committee with fresh shares
```

### Security Properties
- **Secrecy:** t-1 compromised shares in one epoch + t-1 in another < t total
- **Correctness:** New shares reconstruct same secret s
- **Liveness:** Requires t honest old holders to participate

### Implementation Considerations

```python
def verify_reshare(new_shares: dict[int, int], old_commitments: list[int],
                   group_pk: int) -> bool:
    """Verify that new shares reconstruct to the same group public key."""
    # Verify against old commitments
    for j, share in new_shares.items():
        lhs = pow(G, share, P)
        rhs = 1
        for i, commit in enumerate(old_commitments):
            lagrange = lagrange_coefficient_at_x(list(range(1, len(old_commitments)+1)), j, i)
            rhs = (rhs * pow(commit, lagrange, P)) % P
        if lhs != rhs:
            return False

    # Verify group public key unchanged
    reconstructed = reconstruct(list(new_shares.items())[:len(new_shares)-1])
    return pow(G, reconstructed, P) == group_pk
```

## Distributed Key Generation (DKG)

For initial setup without trusted dealer, use DKG:
- Each party runs a VSS of a random secret
- Group secret = sum of all secrets (unknown to any single party)
- Shares = sum of individual VSS shares

### GJKR DKG (Gennaro et al., 1999)
- Extends Feldman VSS to distributed setting
- Public key computed from all party contributions
- Resistant to up to t-1 malicious parties

## Committee Rotation Cadence

| System Type | Rotation Period | Rationale |
|------------|----------------|-----------|
| High-value custody ($100M+) | 7-30 days | Minimize compromise window |
| Exchange hot wallet | 30-90 days | Balance security vs operational complexity |
| Protocol bridge/oracle | 90-180 days | Lower frequency, on-chain governance |
| Enterprise CA | 90-365 days | Operational overhead of certificate replacement |

## Monitoring & Alerting
- **Share freshness:** Track share creation time; alert if > rotation period
- **Committee liveness:** Monitor participation in resharing; alert if < t responsive
- **Public key stability:** Verify group PK unchanged after each rotation
