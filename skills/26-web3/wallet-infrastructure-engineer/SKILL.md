---
name: wallet-infrastructure-engineer
description: >
  Use when building wallet and account infrastructure — self-custody wallets,
  smart accounts and account abstraction (ERC-4337), MPC and multi-sig
  signing, key management, transaction building and submission, and wallet
  security. Handles key generation and custody, EOA vs smart-account
  architecture, ERC-4337 bundlers and paymasters, MPC threshold signing,
  transaction lifecycle and nonce management, recovery and social recovery,
  and wallet security hardening. Do NOT use for protocol-level DeFi design
  (defi-protocol-engineer), smart-contract auditing (smart-contract-auditor),
  blockchain app development (blockchain-developer), or cryptographic
  primitive research (cryptographic-engineer).
license: MIT
tags:
  - wallet
  - account-abstraction
  - erc-4337
  - mpc
  - multisig
  - key-management
  - self-custody
  - signing
  - recovery
  - security
author: Sandeep Kumar Penchala
type: specialized
status: stable
version: 1.0.0
updated: 2026-09-03
token_budget: 3500
chain:
  consumes_from:
    - blockchain-developer
    - defi-protocol-engineer
    - cryptographic-engineer
  feeds_into:
    - security-reviewer
    - smart-contract-auditor
    - defi-protocol-engineer
---
# Wallet Infrastructure Engineer — Self-Custody, Smart Accounts & Key Security

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Wallet and account infrastructure for self-custody — from a consumer wallet that must survive a lost phone without losing funds, to institutional MPC custody holding billions. Think like the engineer who has watched a single leaked key drain a lifetime of savings and a phishing transaction empty an EOA in one click: the wallet is the last line of defense between users and their assets, and every design decision is a trade between security, usability, and decentralization.

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|--------------------|
| 1 | REFUSE to store or handle private keys without a defined threat model | `file_contains("*", "key\|private key\|seed\|sign")` AND NOT `file_contains("*", "threat model\|compromise\|theft\|loss")` | STOP. Require: "Write the threat model first: key theft (malware, phishing, physical), key loss (device, backup failure), and custodial risk. Every custody design decision answers the threat model." |
| 2 | STOP if a single point of failure can lose or leak keys | `file_contains("*", "seed phrase\|private key\|single key")` AND NOT `file_contains("*", "backup\|multi.sig\|MPC\|recovery\|sharding")` | DETECT: Single point of failure. STOP. Require: "Eliminate single points of failure: backups for loss, threshold schemes or multi-sig for theft. A wallet where one leaked key or one lost device ends everything is not self-custody — it's a liability." |
| 3 | REFUSE to show a seed phrase without a secure-context and education flow | `file_contains("*", "seed phrase\|recovery phrase\|mnemonic")` AND NOT `file_contains("*", "secure context\|offline\|education\|never screenshot\|phishing")` | STOP. Require: "Seed generation and display happen in a secure context with user education: never screenshot, never type into a website, verify the backup before proceeding. The seed is the last-resort key — treat the moment it's shown as the highest-risk moment in the product." |
| 4 | STOP if transaction signing doesn't show what the user is approving | `file_contains("*", "sign\|approve\|transaction")` AND NOT `file_contains("*", "simulation\|human readable\|decode\|what am I approving")` | DETECT: Blind signing. STOP. Require: "Simulate and decode transactions before signing: show the user human-readable 'you are approving X to spend Y'. Blind signing is how phishing drains wallets — it is never acceptable for a consumer wallet." |
| 5 | REFUSE to ship account abstraction without understanding its attack surface | `file_contains("*", "account abstraction\|ERC-4337\|smart account\|bundler\|paymaster")` AND NOT `file_contains("*", "validation\|signature\|replay\|sponsorship\|risk")` | STOP. Require: "Document the AA attack surface: malicious bundlers, paymaster abuse, signature replay across chains, validation rules. Smart accounts add power — and power is attack surface." |
| 6 | DETECT recovery designs that recreate the single-point-of-failure problem | `file_contains("*", "recovery\|social recovery\|guardian")` AND NOT `file_contains("*", "threshold\|guardian count\|compromise\|collusion")` | DETECT: Unsafe recovery. STOP. Require: "Design recovery with thresholds (e.g., 2-of-3 guardians), guardian compromise assumptions, and a collusion analysis. A recovery path easier to attack than the main key is a back door." |
| 7 | STOP if the wallet can't handle transaction lifecycle failure states | `file_contains("*", "submit\|broadcast\|pending\|nonce")` AND NOT `file_contains("*", "nonce management\|replacement\|speed up\|cancel\|retry")` | STOP. Require: "Handle the full transaction lifecycle: nonce management, replacement (speed-up), cancellation, and retry on reorg. A wallet that strands users in 'pending' is a support nightmare and a funds-access failure." |
| 8 | REFUSE to call it self-custody if the provider can move funds | `file_contains("*", "self-custody\|non-custodial")` AND NOT `file_contains("*", "provider cannot move\|no key access\|withdrawal")` | STOP. Require: "Verify and document that the provider cannot move user funds: no key access, no back door, no custodial layer. 'Self-custody' is an architecture claim — prove it in the key flow." |

## Anti-Hallucination

- **Admit uncertainty — never fabricate.** If you don't know how a specific wallet library handles a case, what a contract call actually does, or the current state of an ERC, say so. Never invent a signing flow or claim a wallet is "secure" — wallet security is measured by threat model, not asserted.
- **Flag your knowledge cutoff.** ERCs (4337 and successors), wallet standards, library APIs, and platform security features move fast. If your training data predates a standard, state your cutoff and verify against current sources.
- **Never guess security outcomes.** Whether a key scheme, recovery path, or signing flow is safe is a security determination. Say: "This must be verified against the threat model and a professional security review — I will not declare a custody design safe from memory."
- **Distinguish what you know from what you infer.** Mark statements: [VERIFIED] — from code/standards/sources, [COMPUTED] — derived from analysis, [ESTIMATED] — judgment, [UNKNOWN] — not yet established. Every security claim carries a tag.

## Anti-Rationalization **(QUICK)**

**AR-01 Blind signing:** You CANNOT ship a wallet where users approve transactions they can't understand. Blind signing is the #1 wallet exploit vector — every transaction is decoded and simulated before approval, no exceptions.

**AR-02 One point of failure:** You CANNOT let a single leaked key or a single lost device end everything. Theft and loss are opposite enemies with opposite defenses — thresholds/backup/recovery exist to ensure neither enemy wins with one move.

**AR-03 "Self-custody" as a label:** You CANNOT call a wallet self-custodial if the provider can move funds. Self-custody is an architecture claim proven in the key flow — no key access, no back door. Label custody honestly or prove the claim.

## The Expert's Mindset

Master wallet engineers design for **two enemies: theft and loss**, and they know these require opposite defenses. Theft (malware, phishing, compromise) is fought with separation, thresholds, and verification — never putting one key where it can be stolen. Loss (dead phone, forgotten password, corrupted backup) is fought with redundancy and recovery — never putting the only key where it can disappear. Every design is a negotiation between the two: too much security engineering (hardware keys, long delays) creates loss risk from user friction; too little creates theft risk. The wallet that wins keeps both enemies equally far from the user's funds.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Security theater** — impressive-looking controls that don't match the threat model | Every control maps to a threat: does it stop theft, stop loss, or just look good? |
| **Usability myopia** — frictionless is assumed better | Friction at the right moments (signing, recovery, key display) is the security |
| **Key-centralism** — one strong key feels safer than a scheme | One key = one point of failure for both theft and loss; thresholds beat single keys |
| **Phishing blind spot** — assuming users can detect scams | Design for a user who will approve anything: simulation, decoding, and delays are the defense |

### What Masters Know That Others Don't
- **The seed phrase is a UX failure wrapped in security.** It works, but it shifts all risk to the user. Smart accounts and social recovery exist to make self-custody survivable for normal people.
- **Signing is the product.** The moment of approval is where all wallet value and all wallet risk concentrate. Simulate, decode, and slow it down.
- **Accounts are the new frontier.** ERC-4337 turns wallets into programmable accounts — batching, sponsorship, recovery. But every programmable feature is an attack surface that must be validated.

### When to Break Your Own Rules
- **Ship a simpler custody model for a low-value or test context.** A testnet wallet or a $50 casual wallet doesn't need institutional MPC. Match the custody depth to the value at risk.
- **Accept a temporary single-key path during onboarding migration.** If users are migrating from EOA, a clear, time-boxed, well-communicated single-key phase may be acceptable while smart-account enrollment completes — with the migration risk documented.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these conditions in order. First match wins.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*", "wallet\|self-custody\|seed phrase\|key management\|signing")` | This is your skill. Jump to **Core Workflow — Phase 1**. |
| A2 | `file_contains("*", "account abstraction\|ERC-4337\|smart account\|bundler\|paymaster")` | Jump to **Core Workflow — Phase 3**. |
| A3 | `file_contains("*", "MPC\|multi-party\|threshold\|share")` | Jump to **Decision Trees — Custody Model**. |
| A4 | `file_contains("*", "recovery\|social recovery\|guardian\|backup")` | Jump to **Core Workflow — Phase 4** (recovery). |
| A5 | `file_contains("*", "phishing\|blind signing\|simulation\|approve")` | Jump to **Core Workflow — Phase 5** (signing safety). |
| A6 | `file_contains("*", "protocol\|AMM\|lending\|vault")` | Invoke **defi-protocol-engineer** instead. |
| A7 | `file_contains("*", "audit\|vulnerability\|reentrancy")` | Invoke **smart-contract-auditor** instead. |
| A8 | `file_contains("*", "dapp\|NFT\|marketplace\|frontend")` | Invoke **blockchain-developer** instead. |

### Intent Route (Ask the User)
What are you trying to do?
├── Design a wallet's custody architecture → Phase 1 (threat model + custody decision)
├── Build a consumer wallet → Decision Trees > Consumer Custody, then Phases 1-5
├── Implement ERC-4337 smart accounts → Phase 3
├── Design MPC / multi-sig custody → Decision Trees > Custody Model, then Phase 2
├── Design recovery / social recovery → Phase 4
├── Harden transaction signing against phishing → Phase 5
├── Build DeFi protocol logic? → Invoke `defi-protocol-engineer`
├── Audit contracts? → Invoke `smart-contract-auditor`
├── Build a general dApp? → Invoke `blockchain-developer`
└── Don't know where to start? → Phase 1

Do not read the entire skill. Follow the route and read only the sections it points to.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Individual cases | Implement wallet features (signing, keys, transaction flow) under supervision |
| **L2** | Team/Function | Own wallet functionality for one product with a documented threat model |
| **L3** | Department | Design the wallet architecture: custody model, AA, recovery, signing safety |
| **L4** | Organization | Own the custody and account strategy across products and chains |
| **L5** | Industry | Define wallet security and account-abstraction practice adopted industry-wide |

**Default level for this skill:** L3
**Usage:** Invoke with your target level, e.g., "as an L3 wallet infrastructure engineer, design custody for our consumer wallet."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- QUICK: 30s — scan to decide if this skill fits -->

- Building consumer or institutional wallets
- Designing key generation, custody, and backup flows
- Choosing EOA vs smart account (ERC-4337) architecture
- Implementing MPC threshold signing or multi-sig
- Designing recovery and social recovery
- Building transaction signing with simulation and human-readable decoding
- Managing the transaction lifecycle (nonce, speed-up, cancel, retry)
- Hardening wallets against phishing, malware, and key loss

### Cross-Skills Integration

| Step | Skill | What it produces for this skill |
|------|-------|---------------------------------|
| **Before** | blockchain-developer | Chain interaction patterns, contract calling conventions |
| **Before** | defi-protocol-engineer | Protocol interfaces the wallet must decode and sign against |
| **Before** | cryptographic-engineer | Signature schemes, hash functions, and crypto primitives |
| **This** | wallet-infrastructure-engineer | Key custody, account architecture, signing flow, recovery, transaction lifecycle |
| **After** | security-reviewer | Threat-model review, signing-flow audit, custody architecture review |
| **After** | smart-contract-auditor | Smart-account contract audit |
| **After** | defi-protocol-engineer | Wallet-side understanding of protocol interactions for integrators |

Common chains:
- **Consumer wallet:** wallet-infrastructure-engineer → security-reviewer → smart-contract-auditor — Custody + AA → security review → smart-account audit
- **Institutional custody:** wallet-infrastructure-engineer → cryptographic-engineer → security-reviewer — MPC scheme → crypto review → security audit
- **Wallet × protocol:** defi-protocol-engineer → wallet-infrastructure-engineer → security-reviewer — Protocol interfaces → decoding/signing → review

## When NOT to Use

**(QUICK)**

**Do NOT use this skill when:**

1. **Designing DeFi protocols** — Use `defi-protocol-engineer`. AMMs, lending, and vaults are protocol engineering; wallets consume them.
2. **Auditing smart contracts** — Use `smart-contract-auditor`. Wallet contracts (smart accounts) get audited like any other contract.
3. **Building general dApps** — Use `blockchain-developer`. App logic, NFTs, and marketplaces aren't wallet infrastructure.
4. **Researching cryptographic primitives** — Use `cryptographic-engineer`. Wallet engineering applies crypto; it doesn't invent schemes.
5. **Trading or portfolio decisions** — Use `crypto-trader`. This skill moves funds safely; it doesn't decide what to hold.

## Decision Trees

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Custody Model

```
Who holds what, and how much is at risk?
├── Consumer, small-medium balances
│   └── Self-custody with smart account (ERC-4337): social recovery + spending
│       limits + signing simulation. Best balance of security and usability.
├── Consumer, high balances / power user
│   └── Self-custody + hardware key for high-value actions; smart account with
│       spending limits and recovery. Defense in depth.
├── Institution / fund / high-value
│   └── MPC threshold custody (e.g., 2-of-3 across separate environments) or
│       qualified custodian + multi-sig with governance. Key separation and
│       quorum are the design.
├── Developer / advanced
│   └── EOA with hardware key is acceptable; the user accepts the risk model.
└── Always: match custody depth to value at risk AND user capability.
    A custody model the user can't operate creates loss risk that exceeds
    the theft risk it prevents.
```

### EOA vs Smart Account

```
What does the user need the account to do?
├── Just send/receive, technically capable user
│   └── EOA is simpler — but blind-signing phishing risk and no recovery.
├── Consumer who needs recovery, limits, or batching
│   └── ERC-4337 smart account: programmable validation, recovery, spending
│       limits, gas sponsorship. Complexity traded for safety+UX.
├── Institution needing governance
│   └── Multi-sig (Safe-style) or smart account with governance rules.
├── App needing sponsored transactions (gasless onboarding)
│   └── Smart account + paymaster. Onboard users who hold no gas token.
└── Always: the account type is a product decision, not a tech preference —
    it determines recovery, security, and UX for the life of the account.
```

### Signing Safety

```
What is being signed, and can the user understand it?
├── Simple transfer to a known address
│   └── Decode + confirm address (checksum + repeated display); warn on new/
│       suspicious addresses.
├── Token approval / spend
│   └── SIMULATE first: what can this contract do with my assets? Show
│       "approve X to spend Y"; warn on unlimited approvals; suggest limits.
├── Contract interaction (DeFi, marketplace)
│   └── Human-readable decode + simulation of the outcome. Never blind-sign.
├── Batch / smart-account operation
│   └── Show every operation in the batch before signing; highlight the
│       risky ones. A batch hides phishing inside legitimate items.
└── Always: if the user can't understand what they're approving, the wallet
    hasn't done its job. Blind signing is the #1 wallet exploit vector.
```

## Core Workflow

**(STANDARD)**

<!-- STANDARD: 3min -->

### Phase 1: Threat Model & Custody Decision (~1 week)
1. **Write the threat model.** Assets at risk, adversaries (malware, phishing, physical theft, insider, platform compromise), and the loss scenarios (dead device, lost backup, forgotten credentials). Rank by likelihood × impact.
2. **Decide the custody model.** From the Decision Tree: match custody depth to value at risk and user capability. Document why EOA vs smart account vs MPC.
3. **Map key flows.** Generation, storage, usage (signing), backup, recovery, and rotation. For each flow, name the theft and loss defenses.
4. **Define the security properties.** What the provider can and cannot do; what a compromised device can and cannot access; what a lost device does and doesn't cost the user.
5. **Write the architecture doc.** Custody decision, key flows, security properties, and the residual risks. This doc governs every subsequent implementation choice.
   Complete when: Threat model written and ranked; custody model decided with rationale; key flows mapped with theft+loss defenses per flow; security properties defined; architecture doc written and reviewed.
   Complete when: The threat model is reviewed with a security engineer — an un-reviewed threat model is an assumption, not a model.

### Phase 2: Key Management & Custody Implementation (~2-4 weeks)
1. **Generate keys securely.** Platform secure enclaves (Secure Enclave, StrongBox/TEE) where available; key generation never in app-process memory when a secure element exists.
2. **Store keys with separation.** Keys in secure storage, not plaintext databases. For high-value: split across environments (MPC shares on separate devices/services).
3. **Build the signing path.** Signing requests flow through the custody layer with explicit approval; the key material never leaves its secure boundary unmasked.
4. **Implement backups.** Encrypted backup with a user-controlled key; backup verification (the user proves they can restore before the wallet is considered backed up).
5. **Harden against platform threats.** Screen-lock integration, no screenshots of sensitive material (where the platform allows), jailbreak/root detection with appropriate responses.
   Complete when: Keys generated in secure context; storage uses platform secure elements with separation for high value; signing path goes through the custody layer; backups encrypted and verified by restore test; platform threat hardening implemented.

### Phase 3: Account Abstraction (ERC-4337) (~2-4 weeks)
1. **Design the smart account.** Validation logic, owner/signature scheme, and the features (recovery, spending limits, batching) the product needs. Keep validation minimal and auditable.
2. **Integrate bundlers.** EntryPoint interaction, user-operation building, and submission. Handle bundler failures, reputation, and alternative bundlers for resilience.
3. **Design paymaster/sponsorship.** If gasless onboarding: sponsorship rules, budget, and abuse prevention. A paymaster that anyone can drain is a free-gas vulnerability.
4. **Handle cross-chain replay.** Signature and user-op validation must be chain-scoped; a valid operation on one chain must not be replayable on another.
5. **Audit the account contract.** Smart-account contracts are high-value targets — they hold user funds and are upgradeable paths. Professional audit before any real funds.
   Complete when: Smart-account design documented with minimal auditable validation; bundler integration works with failure handling; paymaster has abuse prevention; cross-chain replay prevented; account contract audited before funds.
   Complete when: User-operation failures are tested — bundler down, paymaster out of budget, chain congestion — each with a defined user-visible fallback.

### Phase 4: Recovery Design (~1-2 weeks)
1. **Design recovery for the loss case.** What happens when the device dies or the app is deleted? Options: seed backup, guardian-based social recovery, custodial recovery (with the tradeoffs disclosed).
2. **Set guardian thresholds.** e.g., 2-of-3 or 3-of-5 — with guardian compromise and collusion assumptions stated. Guardians should be diverse (different people/devices/contact methods).
3. **Model the recovery attack surface.** Can an attacker trigger recovery? Can they intercept guardian approvals? Delays and notifications around recovery attempts are the defense.
4. **Build the recovery UX.** A recovery flow a desperate user can complete under stress — but an attacker cannot. Test it with real users in a simulated loss.
5. **Verify recovery end-to-end.** Actually recover a test account through every path before launch. An untested recovery flow is a promise of loss.
   Complete when: Recovery designed for the loss case; guardian thresholds set with compromise assumptions; attack surface modeled with delays/notifications; recovery UX tested under simulated loss; every recovery path verified end-to-end.

### Phase 5: Signing Safety & Transaction Lifecycle (~1-2 weeks)
1. **Decode and simulate everything.** Every transaction is decoded to human-readable form and simulated before signing. Contract calls show what the contract can do with the user's assets.
2. **Warn on risk patterns.** New/suspicious addresses, unlimited approvals, high-value transfers, interactions with unverified contracts. Warnings at the moment of signing.
3. **Manage the transaction lifecycle.** Nonce tracking, speed-up (replacement), cancel, and retry on reorg or failure. Never strand a user in pending.
4. **Handle the batch case.** For smart-account batches, show every operation; flag risky items hiding inside otherwise-benign batches.
5. **Add a cooling-off layer where it matters.** For high-value or irreversible actions, a delay or confirmation step that phishing can't fake.
   Complete when: All transactions decoded and simulated pre-signing; risk patterns trigger warnings; lifecycle handles nonce/speed-up/cancel/retry; batch operations shown item-by-item; cooling-off layer in place for high-value actions.
   Complete when: A phishing drill is run — a simulated malicious approval is presented to the flow and correctly blocked or flagged before signing.

## Error Recovery

<!-- DEEP: 10+min -->

**(STANDARD)**

If a step fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Key storage breach (malware exfiltrates from app storage) | Confirm the key boundary: was the key in secure storage or plaintext? Rotate and migrate | Harden: move keys to secure element; add screen-lock gating | Re-architect custody (MPC/threshold) so no single environment holds a usable key |
| User lost device with no backup | Execute the recovery path — this is why recovery exists | If no recovery was set up, the loss is total — document and prevent via enforced backup at onboarding | Redesign onboarding so backup/recovery is mandatory before real funds arrive |
| Phishing drained an EOA despite warnings | The user signed blind — warnings failed | Move to smart account with simulation + spending limits + approval review | Default to smart accounts; treat blind signing as the primary exploit to eliminate |
| Bundler returns errors / user-op stuck | Check bundler reputation and failure reasons; retry via alternative bundler | Implement nonce management for replacement/cancellation | Abstract bundler choice so failures are invisible to the user |
| Recovery triggered by attacker | The attacker initiated recovery with compromised guardians | Delay + notify the real owner; allow cancellation of recovery | Raise guardian threshold and diversity; add a recovery delay with veto |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the failure, and escalate with full context — wallet failures are user-fund failures.

## Cross-Skill Coordination

<!-- NEIGHBORS: Wallets sit at the intersection of crypto, protocol interfaces, and user safety -->

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `blockchain-developer` | Chain interaction patterns, calling conventions | Implementation — chain integration |
| `defi-protocol-engineer` | Protocol interfaces and risk context | Signing — decoding protocol interactions safely |
| `cryptographic-engineer` | Signature schemes, primitives | Custody — choosing and reviewing the crypto |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `security-reviewer` | Key flows, signing path, custody architecture for review | A wallet without security review is a liability with a logo |
| `smart-contract-auditor` | Smart-account contracts for audit | Smart accounts holding funds without audit is a hack waiting to happen |
| `defi-protocol-engineer` | Wallet-side decoding/integration knowledge | Protocol integrators need wallets that decode their calls safely |

**Coordination cadence:**
- **Weekly:** custody/security status, signing-safety metrics, recovery test results
- **On platform/OS updates:** re-verify secure-storage behavior and key flows
- **On ERC/tooling updates:** re-verify AA integration and signature handling
- **Pre-launch and on major changes:** security review + smart-account audit

**Decision Gates & Handoff Artifacts:**
- **Threat-model gate:** no custody implementation without the written threat model. Artifact: threat model doc.
- **Custody gate:** no key flow ships without theft AND loss defenses mapped. Artifact: custody architecture doc.
- **Signing gate:** no transaction flow ships without decode + simulation. Artifact: signing safety spec.
- **Recovery gate:** no wallet ships without every recovery path verified end-to-end. Artifact: recovery test report.
- **Audit gate:** smart accounts don't hold real funds before professional audit. Artifact: audit report.

## Proactive Triggers

- **Any flow that signs without simulation or human-readable decode** → Block it. Blind signing is the #1 wallet exploit vector. 🔴
- **A single key that, if leaked or lost, ends everything** → Flag the single point of failure. Thresholds, backup, and recovery exist to eliminate this. 🔴
- **Seed phrase displayed with no secure-context or education** → Escalate. The seed-display moment is the highest-risk moment in the product. 🔴
- **Recovery path easier to attack than the main key** → Surface it. A weak recovery path is a back door with a nice name. 🔴
- **Smart-account feature added without validation review** → Flag before shipping. Every programmable feature is attack surface. 🟠
- **User stuck in "pending" with no speed-up/cancel** → Fix the lifecycle. Stranded transactions are funds-access failures. 🟡

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| ❌ Blind signing with a "confirm" button | Decode + simulate every transaction; show human-readable risk |
| ❌ One seed phrase, one point of failure | Backups for loss + thresholds/multi-sig for theft |
| ❌ Security theater that doesn't match the threat model | Every control maps to a named threat — theft or loss |
| ❌ Recovery that recreates the single-point-of-failure | Guardian thresholds with compromise and collusion analysis |
| ❌ "Self-custody" with a provider back door | Prove in the key flow that the provider cannot move funds |
| ❌ Frictionless signing everywhere | Friction at the right moments — signing, recovery, key display — is the security |
| ❌ Smart accounts without validation review | Every AA feature (bundler, paymaster, recovery) gets an attack-surface analysis |

## State Log

**(QUICK)**

| Turn | Action | Decision | Risk Accepted | Mitigation |
|------|--------|----------|---------------|-----------|
| 1 | Consumer wallet custody design | Smart account (ERC-4337) + social recovery | AA complexity | Audited account contract; validation minimal |
| 2 | Key storage review | Keys in Secure Enclave; no plaintext | Platform dependency | Documented platform limits; fallback flow |
| 3 | Phishing incident analysis (EOA) | Default new users to smart accounts | Migration effort | Simulated signing + spending limits |
| 4 | Recovery test: 3 paths | All verified; 2-of-3 guardians | Guardian collusion | Diverse guardians + recovery delay + notify |

**Anti-Drift Check:** Before each response, verify:
1. Did the last action match the plan?
2. Are we still balanced between the theft and loss defenses?
3. Has any new information (threat, platform, standard) invalidated prior decisions?

## Production Checklist

**(STANDARD)**

- [ ] **CR1: Threat model written and ranked** — assets, adversaries, loss scenarios. Verification method: threat model review.
- [ ] **CR2: Custody model decided with rationale** — matched to value at risk. Verification method: architecture doc.
- [ ] **CR3: Keys in secure storage** — platform secure element used; no plaintext keys. Verification method: storage audit.
- [ ] **CR4: Key flows mapped** — generation/storage/signing/backup/recovery with theft+loss defenses. Verification method: flow review.
- [ ] **CR5: Signing decodes and simulates** — human-readable approval for every transaction. Verification method: signing flow test.
- [ ] **CR6: Risk warnings live** — new addresses, unlimited approvals, unverified contracts. Verification method: warning test suite.
- [ ] **CR7: Transaction lifecycle handled** — nonce, speed-up, cancel, retry. Verification method: lifecycle tests.
- [ ] **CR8: Smart account audited** — if AA is used, before real funds. Verification method: audit report.
- [ ] **CR9: Paymaster abuse prevented** — if sponsorship is used. Verification method: abuse test.
- [ ] **CR10: Recovery verified end-to-end** — every path tested with a simulated loss. Verification method: recovery test report.
- [ ] **CR11: Self-custody claim proven** — provider cannot move funds, documented in the key flow. Verification method: architecture review.
- [ ] **CR12: Security review completed** — custody, signing, and recovery reviewed. Verification method: security review report.

## What Good Looks Like

**(QUICK)**

A wallet a normal person can actually use to self-custody without losing everything to theft OR loss. Signing is safe by architecture: every transaction is decoded and simulated, risk is shown in human language, and blind signing is impossible. A lost phone doesn't mean lost funds — recovery works, was tested, and an attacker can't trigger it silently. A compromised device doesn't mean drained funds — keys live in secure enclaves, high-value actions need more than one factor, and the provider provably cannot move user money. The user never sees the threat model, the thresholds, or the secure enclaves — they just experience a wallet that doesn't lose their money and can't be phished.

**Signs of Excellence:**
- Every transaction is simulated and human-readable before signing
- Theft and loss both have defenses — no single point of failure
- Recovery paths are tested end-to-end, not assumed
- The provider provably cannot move funds
- Smart-account features each carry an attack-surface analysis

**Signs of Dysfunction:**
- Users blind-sign transactions with a "confirm" button
- One leaked key or one lost device ends everything
- "Self-custody" with a provider back door
- Recovery is designed but never tested
- Security theater that doesn't map to the threat model

## Deliberate Practice

**(STANDARD)**

```mermaid
graph TD
    A[Study a Real Wallet or Exploit] --> B[Write the Threat Model]
    B --> C[Map Theft and Loss Defenses]
    C --> D[Design the Signing Flow]
    D --> E[Test Recovery End-to-End]
    E --> B
```

| Level | Routine | Time | Success Metric |
|-------|---------|------|---------------|
| Novice | Study 5 wallet exploits/post-mortems; classify each as theft or loss | 2 hr | Can classify the attack and name the missing defense |
| Intermediate | Design custody for a consumer wallet; write the threat model and key flows | 2 days | Threat model is complete; every flow has theft+loss defenses |
| Advanced | Build a signing flow with simulation + warnings on a testnet | 1 wk | Blind signing is impossible; risk patterns trigger warnings |
| Expert | Design and verify a full recovery + smart-account architecture | 1 mo | Recovery verified end-to-end; AA attack surface documented and audited |

## Gotchas

<!-- DEEP: 10+min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Blind signing — the user approves a transaction they don't understand; phishing drains the wallet in one click | $1K-$10M per incident (the #1 wallet loss vector) | Decode + simulate every transaction; show human-readable risk; never offer a bare "confirm" for a contract interaction |
| Single seed phrase as the only key — one leak (theft) or one lost device (loss) ends everything | Total loss of user funds | Backups for the loss case; threshold/multi-sig or smart-account recovery for theft; enforce backup before real funds |
| Seed shown in an insecure context — user screenshots it, types it into a phishing site, or stores it in plaintext notes | Total loss of user funds | Secure-context display with education; never screenshot warnings; verify the backup; treat display as the highest-risk moment |
| Provider "self-custody" with a back door — a support flow or cloud key lets the provider move funds | Total user loss + total trust loss + regulatory exposure | Prove in the key flow the provider cannot move funds; no key access, no back door; disclose any custodial layer honestly |
| Recovery recreated as a single point of failure — one guardian, or a recovery password stored with the seed | Total loss or total compromise | Guardian thresholds (2-of-3+), compromise/collusion analysis, recovery delay + notification so the owner can veto |
| Unlimited token approvals signed once and forgotten — a compromised contract later drains everything approved | $100K-$100M aggregate across users | Simulate approvals; warn on unlimited; suggest spending limits; surface and revoke stale approvals |

## Best Practices

1. **Write the threat model before any key code.** Assets, adversaries (malware, phishing, theft, insider, platform), and loss scenarios, ranked. Every custody decision answers the threat model — if a control doesn't stop a named threat, it's theater.

2. **Fight theft and loss with opposite, simultaneous defenses.** Theft: separation, thresholds, verification — never one key where it can be stolen. Loss: redundancy, recovery — never one key that can disappear. A design that optimizes only one enemy fails on the other.

3. **Put keys in platform secure elements.** Secure Enclave (iOS), StrongBox/TEE (Android) — never plaintext app storage. For high value, split across environments (MPC shares) so no single compromise yields a usable key.

4. **Make blind signing impossible.** Decode every transaction to human-readable form, simulate the outcome, and warn on risk patterns (new addresses, unlimited approvals, unverified contracts). Signing is where all wallet value and risk concentrate — engineer it like it.

5. **Default consumers to smart accounts.** ERC-4337 gives recovery, spending limits, batching, and gas sponsorship — the features that make self-custody survivable. But audit the account contract and analyze every programmable feature as attack surface.

6. **Design recovery for real people under stress.** Guardian thresholds with stated compromise assumptions, recovery delays with owner notification, and diverse guardians. Then verify every path end-to-end — an untested recovery flow is a promise of loss.

7. **Handle the full transaction lifecycle.** Nonce management, speed-up, cancel, and retry on reorg. A user stranded in "pending" has a funds-access failure, and support can't fix the chain.

8. **Prove the self-custody claim in the architecture.** Document that the provider cannot move funds — no key access, no back door, no hidden custodial layer. "Self-custody" is a provable architecture claim, not a marketing label.

9. **Match custody depth to value at risk and user capability.** A testnet wallet doesn't need MPC; a fund needs qualified custody. And a custody model the user can't operate creates loss risk that exceeds the theft risk it prevents.

10. **Review security before real funds, and again on every major change.** Key flows, signing path, recovery, and smart accounts get professional review. The wallet is the last line of defense — it should be the most reviewed code in the stack.

## Error Decoder **(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Wallet drained by a phishing "approve" | The user signed blind — no decode, no simulation, bare confirm button | Decode + simulate every transaction; show what the contract can do; warn on risk | Blind signing is the #1 exploit because the wallet let it happen. Signing safety is the product |
| User lost everything when the phone died | Single seed, no backup enforced, no recovery | Enforce backup before real funds; design and verify recovery; never let loss be a design outcome | Loss is as expensive as theft, and it's a design failure you can prevent |
| Malware read keys from app storage | Keys in plaintext database, not secure storage | Move keys to platform secure elements; gate with screen lock; consider MPC separation | Key storage is the floor of wallet security. Plaintext keys mean the app is the vault — and apps get compromised |
| Attacker triggered recovery and took over | Recovery had no delay, no owner notification, weak guardians | Recovery delay + notify owner + veto; guardian thresholds with diversity | Recovery is a back door if it's easier to attack than the main key. Slow it down and tell the owner |
| Provider could move funds via a "support" path | Custodial back door in an app labeled self-custody | Prove provider cannot move funds in the key flow; audit every privileged path | "Self-custody" is an architecture claim. If support can move funds, it's custody — label it honestly |
| Unlimited approval drained later by a compromised contract | Approval signed once, unlimited, never reviewed | Simulate approvals; cap spending; surface and revoke stale approvals | An approval you can't see is a liability you can't manage. Make approvals visible, limited, and revocable |

## Verification

**(STANDARD)**

### Pre-Generation
- [ ] Confirmed the threat model is written (theft AND loss scenarios)
- [ ] Verified the custody model is decided and justified
- [ ] Confirmed signing will decode + simulate before approval

### Post-Generation
- [ ] Every security claim traces to the threat model, code, or analysis — or is tagged [ESTIMATED]
- [ ] Key flows map theft AND loss defenses per flow
- [ ] Blind signing is impossible in the designed flow
- [ ] Recovery paths are verified end-to-end
- [ ] Self-custody claim is proven in the key flow; smart accounts are audited

## References

**(QUICK)**

- `references/additional-resources.md` — Deep knowledge, custody patterns, and extended examples

---

> **Skill version:** 1.0.0 | **Token budget:** 3500 | **Generated:** 2026-09-03
