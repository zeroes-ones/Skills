---
name: smart-contract-auditor
description: "Use when auditing Solidity/Vyper smart contracts for security vulnerabilities, evaluating DeFi protocol attack surfaces, configuring automated analysis pipelines (Slither + Echidna + Manticore + Foundry), performing formal verification with Certora Prover, or writing audit reports with Trail of Bits severity classification. Handles 13 vulnerability types (reentrancy, integer overflow, access control, frontrunning, oracle manipulation, MEV, flash loan attacks, logic errors, unchecked returns, DoS, timestamp dependence, short address, storage collision), automated analysis workflow (Slither static, Echidna fuzzing, Manticore symbolic, manual review), Foundry test suite (forge test, invariant testing, differential testing), gas optimization with adversarial considerations, DeFi-specific attack surfaces (lending pool manipulation, AMM curve exploitation, bridge message verification, liquid staking derivatives), and audit report standards (Critical/High/Medium/Low/Informational severity with CVSS-aligned scoring). Do NOT use for general smart contract development (use solidity-developer), protocol design (use system-architect), economic modeling (use quantitative-analyst), or web frontend security (use security-reviewer)."
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: specialized
status: stable
version: "1.0.0"
updated: 2026-07-24
tags: [smart-contract, solidity, auditing, defi-security, evm, foundry, formal-verification, slither, echidna]
token_budget: 3500
dependencies:
  tools: [slither, echidna, manticore, foundry, certora, forge]
  packages: []
  permissions: [evm-node-access, etherscan-api]
output:
  type: "audit-report, fix-recommendations"
  path_hint: "smart-contract-auditor/"
chain:
  consumes_from:
    - security-engineer
    - backend-developer
    - system-architect
  feeds_into:
    - cryptographic-engineer
    - zkp-engineer
    - devops-engineer
    - incident-responder
  alternatives:
    - solidity-developer
    - security-reviewer
---
> **Portability target:** Spec-level (runs on Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI). No vendor-specific frontmatter fields.

<!-- QUICK: 30s -->
## Route the Request

```
What needs auditing?
├── NEW smart contract (pre-deployment)
│   └── Core Workflow Phase 1-5 (Full Audit)
├── EXISTING deployed contract (post-deployment review)
│   ├─ Was there an exploit? → Decision Trees → Root Cause Analysis
│   └─ No exploit, due diligence → Vulnerability Detection + Manual Review
├── DEFI protocol (lending/AMM/bridge/staking)
│   └─ Decision Trees → DeFi Attack Surface
├── UPGRADEABLE contract (UUPS/Transparent/Beacon)
│   └─ Decision Trees → Proxy Audit
├── GAS OPTIMIZATION with security review
│   └─ Decision Trees → Gas vs Security Trade-off
├── AUDIT REPORT only (template or finalization)
│   └─ Decision Trees → Audit Report
├── FORMAL VERIFICATION (Certora/KEVM)
│   └─ Core Workflow → Phase 4 (Formal Verification)
└── Token standard compliance (ERC-20/ERC-721/ERC-1155)
   └─ Decision Trees → Token Standards
```

<!-- STANDARD: 3min -->
## Ground Rules -- Read Before Anything Else

1. **REFUSE to skip Slither before manual review.** Automated scanners catch 60-80% of vulnerabilities. Skipping them wastes auditor time and misses obvious findings. Always run `slither . --print human-summary` first.

2. **DETECT -- every external call is a reentrancy vector.** Assume all external calls are malicious until proven safe via Checks-Effects-Interactions (CEI) or ReentrancyGuard. grep for `.call{` and verify state is updated before the external call.

3. **STOP -- unchecked arithmetic in Solidity <0.8.0 is a critical vulnerability.** Integer overflow/underflow can drain pools and mint infinite tokens. Require upgrade to ^0.8.0 or verified SafeMath/OpenZeppelin Math library.

4. **REFUSE to approve audit without fuzzing invariants.** Static analysis alone misses state-dependent bugs. Echidna or Foundry fuzz with 100K+ sequences is mandatory for any protocol holding value.

5. **DETECT -- `tx.origin` is NEVER for authentication.** It bypasses all intermediate contract permission checks and is phishable via any intermediate contract call. Require replacement with `msg.sender`.

6. **STOP -- `delegatecall` to untrusted addresses is a full contract takeover.** The caller's storage is fully controlled by the callee. Verify the target is immutable, audited, and from a known address.

7. **REFUSE -- Oracles must have manipulation resistance.** TWAP with <30 min window, spot price from single DEX, or unverified Chainlink feeds are all attack vectors. Require TWAP >= 30 min, Chainlink with staleness check, or dual-oracle medianizer.

8. **STOP -- signature replay attacks across chains.** If chainId is not in the EIP-712 domain separator, signatures can be replayed on any EVM chain. Verify `block.chainid` is included in all EIP-712 typed data signatures.

9. **Admit uncertainty -- never fabricate exploit PoCs.** If uncertain about exploit feasibility, say so explicitly. A hallucinated PoC that doesn't work wastes more time than admitting uncertainty. Provide a theoretical attack path with explicit caveats.

10. **Flag knowledge cutoff.** Solidity, Foundry, and DeFi patterns evolve rapidly. If training data predates the latest compiler version, Foundry release, or known exploit, state this and recommend verifying against current documentation.

<!-- QUICK: 30s -->
## When to Use

- Pre-deployment security audit of a new DeFi protocol or smart contract system
- Post-incident root cause analysis and fix verification after an exploit or close-call
- Upgradeable contract deployment (UUPS, Transparent, Beacon proxy patterns) -- verify storage layout and access control
- Third-party protocol integration review -- composition risk multiplies attack surface
- Token standard compliance audit (ERC-20, ERC-721, ERC-1155, ERC-4626)
- Gas optimization review with adversarial security analysis (not just cost reduction)
- Formal verification request for mission-critical invariants with Certora Prover or KEVM
- Cross-chain bridge or L2 contract audit -- bridge exploits account for 70% of DeFi exploit value
- Continuous audit program for protocols with frequent upgrades -- CI-integrated fuzzing pipeline

<!-- STANDARD: 3min -->
## Decision Trees

### Tree 1: Vulnerability Detection Funnel

```
Slither static analysis
├─ Finding detected → Categorize severity
│  ├─ Critical (direct exploit, no conditions) → Immediate fix → Re-scan
│  ├─ High (exploitable with conditions) → Write PoC → Fix → Verify
│  └─ Medium (best practice violation) → Document → Schedule fix
├─ No finding → Echidna fuzzing (100K+ sequences)
│  ├─ Invariant broken → Trace to source → Fix → Re-fuzz
│  └─ All invariants hold → Manticore symbolic execution
│     ├─ Reachable exploit path → Write PoC → Fix → Verify
│     └─ No path found → Manual review
└─ Manual review complete → Write audit report with PoCs
```

### Tree 2: Reentrancy Defense

```
External call detected (.call{, transfer, send)
├─ Before all state changes? → Violates CEI → Critical
│  └─ Apply CEI: update balance → external call OR add ReentrancyGuard
├─ After state changes? → CEI compliant ✓
│  └─ Check ERC-777/ERC-721 callback risk
├─ Cross-function reentrancy?
│  └─ ReentrancyGuard modifier + verify no unlocked read-only reentrancy
└─ Cross-contract reentrancy via shared state?
   └─ Pull payment pattern or epoch-based accounting
```

### Tree 3: Oracle Manipulation Prevention

```
Price oracle used for collateral/liquidation/trading
├─ Chainlink price feed?
│  ├─ latestRoundData() with answeredInRound check? → Verify staleness < 1hr
│  └─ No answeredInRound check → Vulnerable to stale price → Add check
├─ TWAP (Uniswap V2/V3)?
│  ├─ Window >= 30 minutes → Acceptable for most protocols
│  └─ Window < 30 minutes → Manipulatable with flash loan → Extend window
├─ Dual oracle (Chainlink + TWAP medianizer)?
│  └─ Best practice if deviation threshold triggers circuit breaker
└─ Single DEX spot price without TWAP?
   └─ CRITICAL: Flash loan can manipulate spot price. Replace with TWAP or Chainlink.
```

### Tree 4: Upgradeable Contract Audit

```
Proxy pattern detected
├─ UUPS?
│  └─ Check _authorizeUpgrade() access control -- this is the security boundary
├─ Transparent proxy?
│  └─ Verify admin function does not overlap with user function selectors
├─ Beacon proxy?
│  └─ Check beacon update authority. Single point of compromise.
├─ Storage collision?
│  └─ Run Slither storage-layout check. Verify __gap[] array in all upgradeable contracts.
├─ Initializer protection?
│  └─ _disableInitializers() called in constructor? initialize() has initializer modifier?
└─ Implementation contract selfdestruct?
   └─ CRITICAL: Any function calling selfdestruct in implementation kills all proxies.
```

### Tree 5: Flash Loan Attack Surface

```
Flash loan vector identified
├─ Price oracle manipulation?
│  └─ TWAP >= 30 min + Chainlink with circuit breaker
├─ Governance attack via flash-loaned voting power?
│  └─ Snapshot checkpoint + timelock delay on proposals
├─ Liquidation cascade?
│  └─ Circuit breaker: pause liquidations when collateral price drops > 20% in one block
├─ Collateral ratio manipulation?
│  └─ Recalculate total collateral + total debt atomically after every operation
└─ Rebase token manipulation?
   └─ Block rebasing tokens in collateral. Use fixed-balance wrappers.
```

<!-- STANDARD: 3min -->
## Core Workflow

### Phase 1: Automated Static Analysis (est. 1-2 hours)
1. Run Slither detection suite: `slither . --detect reentrancy-eth,reentrancy-no-eth,reentrancy-benign,reentrancy-events`
2. Print human summary: `slither . --print human-summary`
3. Print call graph: `slither . --print call-graph`
4. Print inheritance graph: `slither . --print inheritance-graph`
5. Categorize findings: Critical (direct exploit) vs High (conditional exploit) vs Medium (best practice)
**Completion criteria:** All Slither findings categorized and documented. Zero Critical or High findings unaccounted for.

### Phase 2: Fuzzing Invariants (est. 4-8 hours)
1. Define 5-10 property invariants (e.g., totalSupply == sum of all balances)
2. Write Echidna test contract with property functions
3. Run `echidna . --test-mode assertion --corpus-dir corpus` for 100K+ sequences
4. Analyze invariant breaks: trace to source code, identify root cause
5. Re-fuzz after fixes to verify invariant restoration
**Completion criteria:** All invariants hold across 100K+ fuzzing sequences. Broken invariants documented with source traces.

### Phase 3: Symbolic Execution (est. 4-8 hours)
1. Run Manticore for bytecode-level path exploration
2. Use Foundry fuzz for Solidity-level symbolic exploration: `forge test` with fuzz runs
3. Verify all branches reachable and state-space coverage
4. Document unreachable branches: are they dead code or are guards missing?
**Completion criteria:** State-space coverage report. All critical paths explored. Unreachable branches documented and justified.

### Phase 4: Formal Verification (est. 8-40 hours, when applicable)
1. Write Certora Verification Language (CVL) rules for mission-critical invariants
2. Run Certora Prover on critical rules: "Total collateral >= total debt at all times"
3. Parametric verification across all function argument combinations
4. Document verified invariants and any unprovable rules
**Completion criteria:** Certora verification report. All critical invariants formally proven or explicitly unprovable with rationale.

### Phase 5: Manual Review & Report (est. 8-16 hours)
1. Business logic review: tokenomics, economic incentives, governance mechanics
2. Composition analysis: integration with external protocols, upgrade paths
3. Write audit report with Trail of Bits severity classification
4. Produce reproducible PoC for every Critical/High finding
5. Include gas analysis with adversarial considerations
6. Provide 30-day remediation timeline with re-audit recommendation
**Completion criteria:** Final audit report. All Critical/High findings have PoCs. Remediation timeline agreed with development team.

<!-- STANDARD: 3min -->
## Best Practices

| # | Domain | Best Practice |
|---|--------|---------------|
| 1 | Reentrancy | Every external call (.call, transfer, send) must follow Checks-Effects-Interactions pattern. State updates BEFORE external calls, not after. ReentrancyGuard is defense-in-depth, not a replacement for CEI. |
| 2 | Access Control | Use OpenZeppelin's AccessControl (Ownable is insufficient for multi-signer protocols). Never use tx.origin for authentication. Audit every onlyOwner/admin function as a potential centralization risk. |
| 3 | Oracle Safety | Never use single-DEX spot price. Chainlink feeds must have staleness checks (answeredInRound). TWAP windows must be >= 30 min. Dual oracles with medianizer for high-value protocols. |
| 4 | Arithmetic Safety | Solidity >= 0.8.0 for built-in overflow checking. For <0.8.0, verify SafeMath or OpenZeppelin Math is used. Check for unchecked blocks that might intentionally bypass overflow protection. |
| 5 | Flash Loan Resistance | Collateral ratios must be recalculated atomically within each transaction. Flash loan + oracle manipulation is the most common exploit pattern -- TWAP and circuit breakers are mandatory. |
| 6 | Upgrade Safety | Implement _disableInitializers() in implementation constructor. Use __gap array for storage buffer. Verify storage layout diff on every upgrade. ERC-7201 namespaced storage for complex protocols. |
| 7 | Signature Verification | Include block.chainid in EIP-712 domain separator. Validate deadline/expiry timestamps. Use nonces to prevent replay. Verify signer address is not address(0). |
| 8 | Bridge Security | Validate message authenticity (not just origin). Include chainId in cross-chain messages. Verify adapter/relayer integrity. Monitor for message delays that indicate censorship. |
| 9 | Gas Optimization Security | Assembly blocks must be carefully audited for storage slot correctness. Shortcut optimizations (unchecked math, unsafe casting) can introduce critical vulnerabilities. Gas optimization must never compromise safety. |
| 10 | Timelock & Governance | Governance proposals need timelock delay (48h+ minimum). Flash loan governance attacks can pass malicious proposals. Use Snapshot for voting weight checkpointing. |
| 11 | Fallback Functions | Receive() and fallback() functions can be called by anyone. Verify they don't perform state-changing operations or accept arbitrary calls. |
| 12 | Event Emissions | Critical state changes must emit events for off-chain monitoring. Slither can detect missing events. Events are also used for reorg protection -- verify event ordering. |

<!-- DEEP: 10+min -->
## Error Decoder

### War Story 1: The DAO Reentrancy ($60M)

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| Attacker drains ETH from The DAO smart contract recursively. Each withdrawal call re-enters the withdraw function before the balance is updated, allowing unlimited ETH extraction. | The withdraw function updated the user's balance AFTER sending ETH via call(). The fallback function at the attacker's contract re-called withdraw(), which checked the still-unupdated balance and sent ETH again. This loop continued until the contract was drained. | Apply Checks-Effects-Interactions: update balance BEFORE making the external call. Use ReentrancyGuard modifier as defense-in-depth. For pull payments, let users claim their balance rather than having the contract push it. | Never update state after an external call. CEI (Checks-Effects-Interactions) is not a style preference -- it is existential security. Every .call{} introduces reentrancy risk. ERC-777 tokens make this worse with callback hooks. Assume ALL external calls are malicious. |

### War Story 2: Mango Markets Oracle Manipulation ($100M+)

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| Attacker manipulates the oracle price of MNGO tokens by exploiting a single-DEX spot price feed. They deposit manipulated collateral, borrow all available assets, and drain $100M+ from the protocol. | The protocol used a single-DEX spot price oracle without TWAP. The attacker executed a large swap on that DEX to manipulate the spot price, then immediately used the inflated collateral value to borrow all available funds. The flash loan was used to fund both the swap and the borrow. | Use TWAP with >= 30 min window (not spot price). Add Chainlink price feed as secondary oracle with deviation check. Implement circuit breaker: pause borrows when oracle deviation exceeds threshold. Use medianizer for multi-oracle feeds. | A single-DEX spot price is not an oracle -- it's a price suggestion. Any protocol using spot price without TWAP is one flash loan away from being drained. Oracle design is the most critical security decision in a DeFi lending protocol. |

### War Story 3: Parity Multi-Sig Wallet Freeze ($11.4M)

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| A user accidentally triggers the kill() function on the Parity multi-sig wallet library contract. All wallets using that library become frozen -- their ETH and tokens are permanently locked. | The Parity multi-sig wallet used a library-based architecture where the library contract was initialized and then wallets called into it via delegatecall. The library contract had a selfdestruct function that was callable by anyone. Once selfdestruct was called, all delegatecalls to that library address reverted. | Implement _disableInitializers() in the constructor of implementation contracts. Remove selfdestruct from implementation contracts entirely. Use transparent proxy pattern to separate admin from user functions. Add storage gap __UPGRADABLE__ arrays. | An uninitialized implementation contract is an existential risk. Anyone can call selfdestruct on an implementation contract. Once destroyed, all proxies pointing to it are bricked. Initializer guards and constructor-based disablement are not optional for upgradeable contracts. |

### War Story 4: Wormhole Bridge Exploit ($325M)

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| Attacker mints 120,000 wETH ($325M) on Solana by forging a bridge message. The Solana contract accepts the forged message and releases the wrapped ETH to the attacker without corresponding ETH being locked on Ethereum. | The Wormhole bridge validator logic had a critical bug: the guardian signature verification was bypassed because the contract checked if guardianSetAddress was set, but never validated it was the CURRENT guardian set. An old guardian set (compromised) or zero-address guardian set could pass verification. | Always validate that the verifying entity is the current, active guardian set. Implement epoch-based guardian rotation with explicit deactivation of old sets. Add verify() function that checks (1) active set, (2) threshold signatures from active set, (3) non-replay via message ID tracking. | Bridge security is dominated by message verification logic. The implicit assumption of "current guardian set" being the one that signed is not enough -- you must explicitly check that the signing set is the active one. Cross-chain message verification is the hardest security problem in DeFi, requiring formal verification of the verification logic itself. |

### War Story 5: Cream Finance Flash Loan Attack ($130M)

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| Attacker executes a complex flash loan attack against Cream Finance's lending protocol. They manipulate the price of an LP token through a series of swaps and borrows, ultimately extracting $130M in stolen assets. | The protocol used an LP token (from a DEX pair) as collateral. The LP token price was computed on-chain using the reserve ratio of the underlying DEX pair. An attacker could flash loan manipulate the DEX pair's reserves, artificially inflating the LP token price, then borrow against the inflated collateral. | Never use liquidity-provider tokens as collateral with on-chain price computation. If LP tokens must be accepted, use a TWAP oracle for the LP token price, not spot reserves. Add circuit breakers that pause borrowing when TVL deviates abnormally. Use Chainlink LP token pricing if available. | Any collateral that can be manipulated on-chain is not safe collateral. LP tokens are particularly dangerous because their price is computed from manipulable reserves. On-chain price computation for collateral value is an invitation to flash loan arbitrage. The safest approach is to use off-chain oracles for all collateral pricing. |

### War Story 6: Nomad Bridge Replay Attack ($190M)

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| A single legitimate cross-chain message is replayed hundreds of times, draining $190M from the Nomad bridge. Thousands of copycat attackers drain funds in a "run on the bank." | The Nomad bridge's message verification logic had a bug where the first message was verified correctly, but subsequent messages with the same data were accepted because the "processed" flag for the message hash was never checked. In fact, the message hash was computed incorrectly (zero-filling a different field), so no message was ever marked as processed. | Always check and set a processed mapping for message hashes. The message hash computation must include ALL fields. Test that the hash never produces collision or zero values. Add a rate limit on message processing per block. Implement a withdraw delay that allows manual intervention during attacks. | A single unchecked message replay can drain an entire bridge. The missing processed-check is a one-line bug that cost $190M. Message hash computation must be rigorously tested -- a subtle bug in the hash calculation makes the processed mapping useless. Formal verification of message verification logic is mandatory for bridges. |

<!-- STANDARD: 3min -->
## Scale Depth: Solo => Small => Medium => Enterprise

### Solo (0-10 users, individual auditor or single contract)
- **Scope:** Single contract audit, <500 LOC, simple ERC-20/ERC-721 tokens
- **Tools:** Slither static analysis, manual review
- **Fuzzing:** Basic Echidna for simple invariants
- **Formal verification:** Not typically applicable
- **Report format:** Markdown audit summary with severity labels
- **Timeline:** 1-2 days per contract
- **Constraints:** No cross-contract composition analysis, limited economic modeling

### Small Team (10-100 users, audit firm or in-house team, 3-8 contracts)
- **Scope:** Protocol with 3-8 contracts, moderate complexity, some DeFi exposure
- **Tools:** Slither + Echidna + Foundry fuzz
- **Fuzzing:** Property-based fuzzing, 50K+ sequences per invariant
- **Formal verification:** Certora for mission-critical invariants
- **Report format:** Standardized report with PoCs for Critical/High findings
- **Timeline:** 1-2 weeks
- **Constraints:** Manual upgrade analysis, basic economic modeling

### Medium Team (100-10K users, dedicated security firm, 10-30 contracts)
- **Scope:** Full DeFi protocol audit (lending, AMM, bridge, staking), complex compositions
- **Tools:** Slither + Echidna + Manticore + Foundry + Certora Prover
- **Fuzzing:** 100K+ sequences, differential fuzzing, mutation-guided fuzzing
- **Formal verification:** Certora CVL for all invariant types
- **Report format:** Comprehensive report with gas analysis, economic attack modeling
- **Timeline:** 3-6 weeks
- **Constraints:** Formal verification for critical paths, 30-day remediation follow-up

### Enterprise (10K+ users, top-tier audit firm or protocol with >$1B TVL)
- **Scope:** Full protocol suite including bridges, governance, oracles, complex DeFi compositions
- **Tools:** L3 + custom invariant DSL, formal verification across all critical invariants
- **Fuzzing:** Continuous fuzzing (CI-integrated), 1M+ sequences, adversarial fuzzing
- **Formal verification:** Certora + KEVM + Dafny for different abstraction levels
- **Report format:** Formal verification report + standard audit report + remediation verification
- **Timeline:** 6-12 weeks with continuous re-audit cycle
- **Constraints:** Formal proofs for all invariants, regulatory compliance (MiCA, SEC)

### Transition Triggers
- **Solo => Small:** Second contract type introduced; first DeFi integration
- **Small => Medium:** TVL exceeds $10M; first upgradeable contract audit
- **Medium => Enterprise:** TVL exceeds $1B; bridge audit; regulatory mandate

<!-- STANDARD: 3min -->
## Production Readiness Checklist

| # | Item | Ref |
|---|------|-----|
| CR1 | Slither output reviewed: zero Critical/High unresolved findings | [V1] |
| CR2 | Echidna fuzzed 100K+ sequences with zero invariant breaks | [V2] |
| CR3 | Manticore/Foundry explored all state-space branches | [V3] |
| CR4 | All external calls follow CEI or have ReentrancyGuard | [V4] |
| CR5 | No tx.origin used for authentication anywhere in the codebase | [V5] |
| CR6 | Oracle manipulation resistance verified (TWAP >= 30 min or Chainlink with staleness) | [V6] |
| CR7 | Upgrade path tested with storage layout diff (no collision, gaps verified) | [V7] |
| CR8 | All Critical/High findings have reproducible PoCs | [V8] |
| CR9 | Gas analysis includes adversarial considerations (not just optimization) | [V9] |
| CR10 | Audit report follows Trail of Bits severity standards with CVSS scoring | [V10] |
| CR11 | Remediation timeline agreed with development team (30-day max for Critical) | [V11] |
| CR12 | Re-audit scheduled after fixes applied | [V12] |
| CR13 | Signature replay protection verified (chainId in EIP-712 domain, nonces, deadlines) | [V13] |
| CR14 | Selfdestruct removed from all upgradeable implementation contracts | [V14] |
| CR15 | Approve/transferFrom race condition mitigated (increaseAllowance pattern used) | [V15] |
| CR16 | Fallback/receive functions audited for unexpected state changes | [V16] |

<!-- STANDARD: 3min -->
## Cross-Skill Coordination

| Direction | Skill | Handoff |
|-----------|-------|---------|
| **Upstream** | `security-engineer` | Threat model, asset inventory, trust boundaries, protocol architecture review |
| **Upstream** | `system-architect` | Protocol architecture, tokenomics, governance design, upgrade strategy |
| **Upstream** | `backend-developer` | Off-chain components, API security, key management, relayer infrastructure |
| **Downstream** | `cryptographic-engineer` | ZKP circuit verification requirements, signature scheme audit needs |
| **Downstream** | `devops-engineer` | Deployment script audit, multisig configuration, monitoring dashboards, CI-integrated fuzzing |
| **Downstream** | `incident-responder` | Exploit detection rules, circuit breakers, pause mechanisms, monitoring alerts |

<!-- QUICK: 30s -->
## What Good Looks Like

An excellent smart contract audit produces:

- **Comprehensive automated analysis:** Slither + Echidna + Manticore + Foundry all run and documented
- **Formalized invariants:** All property invariants written, verified (fuzzing or formal), with source code trace
- **Reproducible PoCs:** Every Critical/High finding has a standalone PoC exploit that demonstrates the vulnerability
- **Clear severity classification:** Trail of Bits standards with CVSS-aligned scoring, not subjective labels
- **Business logic analysis:** Tokenomics, economic incentives, and governance mechanics reviewed beyond code correctness
- **Actionable remediation:** 30-day fix timeline with verification, clear before/after code for each finding
- **Upgrade safety:** Storage layout diff, initializer verification, proxy pattern analysis
- **Gas analysis:** Adversarial considerations included (not just optimization), assembly blocks verified

Results are measured in findings caught before deployment, not post-exploit.

<!-- STANDARD: 3min -->
## References

### Reference Files

| File | Contents |
|------|----------|
| `references/13-vulnerability-taxonomy.md` | Full 13-type vulnerability classification with detection rules |
| `references/slither-config-guide.md` | Slither configuration, detector selection, custom detectors |
| `references/echidna-invariant-testing.md` | Echidna property testing, corpus management, assertion mode |
| `references/foundry-audit-workflow.md` | Foundry forge fuzz, invariant tests, differential testing |
| `references/formal-verification-certora.md` | Certora CVL rules, parametric verification, prover configuration |
| `references/defi-attack-surfaces.md` | Lending, AMM, bridge, staking specific attack patterns |
| `references/upgradeable-contract-audit.md` | UUPS, Transparent, Beacon proxy audit checklists |
| `references/mev-mitigation-patterns.md` | Sandwich, frontrunning, backrunning defense patterns |
| `references/audit-report-template.md` | Trail of Bits format report template with severity guidelines |
| `references/gas-optimization-security.md` | Gas optimization with adversarial security considerations |

### External Standards

| Standard | Purpose |
|----------|---------|
| Trail of Bits Severity Classification | Industry standard for smart contract vulnerability severity |
| SWC Registry | Smart Contract Weakness Classification and test cases |
| EIP-712 | Typed structured data hashing and signing for signatures |
| ERC-7201 | Namespaced storage layout for upgradeable contracts |
| Certora Verification Language | Formal verification specification language for EVM |
