# Additional Resources — wallet-infrastructure-engineer

> Deep knowledge loaded on demand. Custody patterns, signing safety, and reference material.

## Custody Model Comparison

| Model | Theft defense | Loss defense | Best for | Watch-outs |
|-------|---------------|--------------|----------|-----------|
| EOA + seed | Seed is single point (weak) | Seed backup (weak if single) | Dev/advanced users | Blind signing risk; no recovery |
| EOA + hardware key | Key never leaves device | Device loss = key loss (no recovery) | Power users | Recovery gap; hardware cost |
| Smart account (ERC-4337) | Spending limits, session keys, simulation | Social recovery, guardians | Consumer self-custody | AA attack surface; bundler/paymaster risk |
| Multi-sig (Safe-style) | Quorum (e.g., 2-of-3) | Signer loss manageable | DAOs/institutions | Coordination friction |
| MPC threshold custody | Shares in separate environments | Threshold survives share loss | Institutions/high value | Complex ops; provider trust |

## Threat Model Template (one page)

| Column | Content |
|--------|---------|
| Assets | What the wallet protects (tokens, NFTs, keys, data) + value range |
| Adversaries | Malware, phishing, physical theft, insider, platform compromise, social engineering |
| Theft scenarios | Compromised device, leaked seed, blind-signed approval, malicious recovery |
| Loss scenarios | Dead/lost device, deleted app, lost backup, forgotten credentials |
| Defenses by scenario | For each: the control that stops it (separation, threshold, recovery, delay, simulation) |
| Residual risks | Accepted risks with rationale (e.g., platform secure-enclave dependency) |

## Signing-Safety Flow (must-haves)

1. **Decode:** translate the raw calldata into human-readable action ("approve USDC spend of 1,000 to Uniswap Router").
2. **Simulate:** dry-run the transaction against current state; show the outcome (balance changes, approvals created, what the contract can do).
3. **Warn:** flag new/suspicious addresses, unlimited approvals, unverified contracts, high value, unusual patterns.
4. **Confirm:** require explicit confirmation showing the risk level; no bare "Sign" for contract interactions.
5. **Batch transparency:** for smart-account batches, show every operation; highlight risky items.

## Recovery Design Checklist

- [ ] Loss scenario defined (device dead, app deleted, phone stolen)
- [ ] Recovery path per scenario (guardian-based, backup-based, or hybrid)
- [ ] Guardian threshold set (e.g., 2-of-3) with compromise + collusion assumptions
- [ ] Guardian diversity (different people/devices/contact methods)
- [ ] Recovery delay + owner notification + veto path
- [ ] Attack-surface analysis: can an attacker trigger or intercept recovery?
- [ ] End-to-end verification of every path (simulated loss → recovered funds)
- [ ] UX tested under stress (real users, simulated loss)

## War Stories

- **The blind-sign drain:** A user approved a "reward claim" that was actually an unlimited approval; the contract drained the wallet over weeks. The wallet showed raw hex and a confirm button. Fix: simulation + human-readable decode + spending limits. Lesson: if the user can't understand what they're approving, the wallet has failed — blind signing is the #1 vector.
- **The lost-phone total loss:** A user's only copy of a seed was in the notes app on the same phone that died. No backup, no recovery — total loss. Fix: enforced backup verification before real funds; social recovery as the default. Lesson: loss is a design outcome; if the wallet never verified a backup, it shipped a loss trap.
- **The "self-custody" back door:** An app labeled non-custodial had a cloud key backup "for support" that let the provider move funds. When discovered, trust collapsed. Fix: prove in the key flow the provider cannot move funds; label honestly. Lesson: custody is an architecture claim — the back door voids it regardless of intent.
- **The single-guardian recovery:** A recovery design used one guardian (a friend's email). The attacker phished that email and triggered recovery. Fix: 2-of-3 diverse guardians + recovery delay + owner notification/veto. Lesson: a recovery path easier to attack than the main key is a back door with a nice name.

## Reference Material

- ERC-4337 spec — account abstraction: EntryPoint, UserOperation, bundlers, paymaster
- Safe (Gnosis Safe) docs — multi-sig account patterns
- Web3Auth / Lit / Turnkey docs — MPC and threshold-signature custody patterns (verify currency)
- Platform security docs — Secure Enclave (iOS), StrongBox/TEE (Android), WebAuthn/passkeys
- Wallet security frameworks (e.g., WalletConnect / CAIP standards, EIP-712 typed data) — structured signing
