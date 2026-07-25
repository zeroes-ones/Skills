---
name: smart-contract-auditor
description: >
  Use when auditing Solidity/Vyper smart contracts for security vulnerabilities, evaluating DeFi protocol
  attack surfaces, configuring automated analysis pipelines (Slither + Echidna + Manticore + Foundry),
  performing formal verification with Certora Prover, or writing audit reports with Trail of Bits severity
  classification. Handles 13 vulnerability types (reentrancy, integer overflow, access control, frontrunning,
  oracle manipulation, MEV sandwich/arbitrage/liquidation, flash loan attacks, logic errors, unchecked
  returns, DoS, timestamp dependence, short address, storage collision), automated analysis workflow
  (Slither static → Echidna fuzzing → Manticore symbolic → Manual review), Foundry test suite (forge test,
  invariant testing with handlers, differential testing against reference), gas optimization with adversarial
  considerations (storage packing, unchecked blocks, assembly), DeFi-specific attack surfaces (lending pool
  manipulation, AMM curve exploitation, bridge message verification, liquid staking derivatives), and audit
  report standards (Critical/High/Medium/Low/Informational severity with CVSS-aligned scoring). Do NOT use
  for general smart contract development (use solidity-developer), protocol design (use system-architect),
  economic modeling (use quantitative-analyst), or web frontend security (use security-reviewer).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: security
status: stable
version: 1.0.0
updated: 2026-07-24
tags: [smart-contract, solidity, auditing, defi-security, evm, foundry, formal-verification, slither, echidna]
token_budget: 4500
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
---

# Smart Contract Auditor — Portability Target

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Adversarial security audit of EVM-compatible smart contracts using Trail of Bits methodology:
automated analysis → fuzzing → symbolic execution → manual review.

## Route the Request

| # | Detect Condition | Route To |
|---|-----------------|----------|
| A1 | `.sol` or `.vy` files with `transfer`, `delegatecall`, `selfdestruct` | Core Workflow → Phase 1 (Static Analysis) |
| A2 | DeFi protocol files: lending, AMM, bridge, staking | Decision Trees → DeFi Attack Surface |
| A3 | Upgradeable contract patterns: UUPS, Transparent, Beacon | Decision Trees → Proxy Audit |
| A4 | Files with `require`, `assert`, `revert` under `if` conditions | Decision Trees → Vulnerability Detection |
| A5 | MEV-sensitive patterns: `block.timestamp`, `tx.origin`, `gasprice` | Decision Trees → MEV Mitigation |
| A6 | Formal verification request: Certora, KEVM, Dafny | Core Workflow → Phase 4 (Formal Verification) |
| A7 | Audit report template request | Decision Trees → Audit Report |
| A8 | Gas optimization with `assembly` blocks | Gotchas → G7 Storage Collision |

### Intent Route Tree

```
What are you auditing?
├── NEW smart contract → Core Workflow Phase 1-5 (Full Audit)
├── EXISTING deployed contract → Decision Trees → Vulnerability Detection + Manual Review
├── DEFI protocol (lending/AMM/bridge) → Decision Trees → DeFi Attack Surface
├── UPGRADEABLE contract → Decision Trees → Proxy Audit
├── GAS OPTIMIZATION → Decision Trees → Gas vs Security Trade-off
└── AUDIT REPORT only → Decision Trees → Audit Report
```

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|--------------------|--------------------|
| R1 | **REFUSE to skip Slither before manual review.** Automated scanners catch 60-80% of vulnerabilities. Skipping them wastes auditor time. | Trigger: Manual review requested with no Slither output in context | REFUSE. "Run Slither first: `slither . --print human-summary`. Share the output, then proceed to manual review." |
| R2 | **DETECT — Every external call is a reentrancy vector.** Assume all external calls are malicious until proven safe via CEI or ReentrancyGuard. | Trigger: grep for `.call{` or `transfer` followed by state mutation | WARN: "External call detected before state update. Verify Checks-Effects-Interactions pattern or add ReentrancyGuard." |
| R3 | **STOP — Unchecked arithmetic in Solidity <0.8.0 is a critical vulnerability.** Integer overflow/underflow can drain pools and mint infinite tokens. | Trigger: Solidity pragma < 0.8.0 with no SafeMath | STOP: "Unchecked arithmetic detected. Upgrade to ^0.8.0 or add SafeMath/OppenZeppelin Math library." |
| R4 | **REFUSE to approve audit without fuzzing invariants.** Static analysis alone misses state-dependent bugs. Echidna or Foundry fuzz is mandatory. | Trigger: Audit report without fuzzing output | REFUSE: "No fuzzing evidence provided. Run Echidna with property invariants or Foundry `forge test` with fuzz cases before finalizing." |
| R5 | **DETECT — `tx.origin` is NEVER for authentication.** It bypasses all intermediate contract permission checks. | Trigger: grep for `tx.origin` in `.sol` files | WARN: "tx.origin used for auth — replace with msg.sender. This is phishable via any intermediate contract call." |
| R6 | **STOP — `delegatecall` to untrusted addresses is a full contract takeover.** The caller's storage is fully controlled by the callee. | Trigger: grep for `delegatecall` with dynamic address | STOP: "delegatecall to untrusted address detected. This grants full storage write access. Verify the target is immutable and audited." |
| R7 | **REFUSE — Oracles must have manipulation resistance.** TWAP with <30 min window, spot price from single DEX, or unverified Chainlink feeds are all attack vectors. | Trigger: Oracle pattern with no manipulation protection | REFUSE: "Oracle manipulation vulnerable. Use TWAP ≥ 30 min, Chainlink with staleness check, or dual-oracle medianizer." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

| Cognitive Bias | How It Manifests | Antidote |
|---|---|---|
| **Code-is-law fallacy** — "The code does what it says" | Auditor assumes intended behavior equals actual behavior | Fuzz every invariant. Code does what it's told, not what you meant. |
| **Test-passing bias** — "Tests pass, so it's secure" | Passing unit tests confused with security verification | Unit tests verify functionality, not absence of bugs. Fuzzing and formal verification test the state space, not happy paths. |
| **Familiarity bias** — "I've seen this pattern before" | Skipping analysis of "standard" OpenZeppelin patterns | Even audited libraries have bugs in integration. Audit the composition, not just components. |
| **Complexity blindness** — "This is too complex to exploit" | Dismissing multi-step attack chains as "theoretical" | Every major DeFi hack was a multi-step chain dismissed as impractical. Map all state transitions. |
| **Tool trust** — "Slither found nothing, so it's clean" | Treating automated tools as comprehensive | Slither finds 60-80%. The remaining 20-40% require human reasoning about business logic, tokenomics, and composition. |

## Operating at Different Levels

| Level | Scope | Tools | Budget | Timeline |
|-------|-------|-------|--------|----------|
| L1 — Quick Review | Single contract, <500 LOC | Slither, manual read | $2K-$5K | 1-2 days |
| L2 — Standard Audit | Protocol with 3-8 contracts | Slither + Echidna + Manual | $15K-$50K | 1-2 weeks |
| L3 — Full Audit | DeFi protocol, 10-30 contracts | L2 + Manticore + Foundry fuzz | $80K-$200K | 3-6 weeks |
| L4 — Formal Verification | Mission-critical: bridge, L2 | L3 + Certora Prover | $200K-$500K | 6-12 weeks |
| L5 — Continuous Audit | Protocol with frequent upgrades | L4 + CI-integrated fuzzing | $500K+/year | Ongoing |

## When to Use

| Trigger | Action |
|---------|--------|
| Pre-deployment audit of new protocol | Core Workflow Phase 1-5, full audit |
| Post-incident review after exploit | Decision Trees → Vulnerability Detection → Root cause |
| Upgradeable contract deployment | Decision Trees → Proxy Audit |
| Integration with external protocol | Core Workflow Phase 3 (Integration Surface) |
| Token standard compliance check | Decision Trees → Token Standards |
| Gas optimization review | Gotchas G7 + Decision Trees → Gas vs Security |
| Regulatory compliance (MiCA, SEC guidance) | References → compliance-mapping.md |

## Core Workflow

### Phase 1: Automated Static Analysis (Slither)
```bash
slither . --print human-summary
slither . --detect reentrancy-eth,reentrancy-no-eth,reentrancy-benign,reentrancy-events
slither . --print call-graph
slither . --print inheritance-graph
```
Categorize findings: Critical (exploitable now) vs High (exploitable with conditions) vs Medium (best practice violation).

### Phase 2: Fuzzing Invariants (Echidna)
```solidity
// echidna: testInvariant_totalSupply_equals_balanceSum
function echidna_totalSupply() public view returns (bool) {
    return totalSupply == balanceSum();
}
```
Define 5-10 property invariants. Run `echidna . --test-mode assertion --corpus-dir corpus`.

### Phase 3: Symbolic Execution (Manticore/Foundry)
Focus on complex state paths. Manticore for bytecode-level, Foundry for Solidity-level. Verify all branches reachable.

### Phase 4: Formal Verification (Certora)
Write CVL rules for critical invariants. "Total collateral ≥ total debt at all times." Parametric verification.

### Phase 5: Manual Review & Report
Business logic review, tokenomics audit, composition analysis. Produce report with PoCs for Critical/High findings.

## Decision Trees

### 1. Vulnerability Detection Funnel
```
Slither static analysis
├─ Finding detected → Categorize severity
│  ├─ Critical (direct exploit) → Immediate fix → Re-scan
│  ├─ High (conditional exploit) → Write PoC → Fix → Verify
│  └─ Medium (best practice) → Document → Schedule fix
├─ No finding → Echidna fuzzing
│  ├─ Invariant broken → Trace to source → Fix → Re-fuzz
│  └─ All invariants hold → Manticore symbolic
│     ├─ Reachable exploit path → Write PoC → Fix → Re-verify
│     └─ No path found → Manual review
└─ Manual review complete → Write audit report
```

### 2. Reentrancy Defense
```
External call detected
├─ Before state changes? → Checks-Effects-Interactions (CEI) ✓
├─ After state changes? → Add ReentrancyGuard
│  ├─ Single function → nonReentrant modifier
│  ├─ Cross-function → ReentrancyGuard + CEI
│  └─ Cross-contract → Pull payment pattern
└─ ERC-777/ERC-721 callback? → ReentrancyGuard + block reentrant tokens
```

### 3. Oracle Manipulation Prevention
```
Price oracle used
├─ Chainlink → Check staleness + circuit breaker
│  ├─ latestRoundData() with answeredInRound check
│  └─ Circuit breaker: pause if deviation > X%
├─ TWAP → 30 min minimum window
│  └─ Uniswap V2/V3 TWAP via observe()
├─ Dual oracle → Medianizer
│  └─ Chainlink + TWAP median
└─ Single DEX spot price → VULNERABLE → Replace immediately
```

### 4. Upgradeable Contract Audit
```
Proxy pattern detected
├─ UUPS → Check _authorizeUpgrade() access control
├─ Transparent → Verify admin ≠ user interaction paths
├─ Beacon → Check beacon update authority
├─ Storage gaps → Verify __gap array in all contracts
├─ Initializer → Check _disableInitializers() called in constructor
│  └─ initialize() must have initializer modifier
└─ Storage collision → Slither check for layout conflicts
```

### 5. MEV Mitigation
```
MEV-sensitive operation
├─ DEX swap → Sandwich attack risk
│  └─ Mitigation: slippage protection + Flashbots bundle
├─ Liquidation → Frontrunning risk
│  └─ Mitigation: commit-reveal or MEV auction
├─ Oracle update → Oracle manipulation risk
│  └─ Mitigation: TWAP + delay + circuit breaker
└─ Arbitrage → Backrunning acceptable
   └─ Mitigation: tolerance threshold
```

### 6. Flash Loan Attack Surface
```
Flash loan vector
├─ Price oracle manipulation → Use TWAP + Chainlink
├─ Governance attack via flash-loaned voting power → Snapshot + timelock
├─ Liquidation cascade via manipulated price → Circuit breaker
├─ Collateral ratio manipulation → Recalculate after every operation
└─ Token minting via rebase manipulation → Block rebasing tokens in collateral
```

## Cross-Skill Coordination

| Direction | Skill | Handoff |
|-----------|-------|---------|
| Upstream | security-engineer | Threat model, asset inventory, trust boundaries |
| Upstream | system-architect | Protocol architecture, tokenomics, governance design |
| Upstream | backend-developer | Off-chain components, API security, key management |
| Downstream | cryptographic-engineer | ZKP circuit verification, signature scheme audit |
| Downstream | devops-engineer | Deployment script audit, multisig config, monitoring |
| Downstream | incident-responder | Exploit detection rules, circuit breakers, pause mechanisms |

## Proactive Triggers

| Trigger | Why It Matters | If Ignored |
|---------|---------------|------------|
| New DeFi protocol deployment | 90% of exploited protocols had unaudited code paths | $10M-$600M exploit within first 3 months |
| Upgradeable proxy deployment | Proxy bugs are the #2 source of major DeFi exploits | $11.4M Parity-style selfdestruct or storage corruption |
| Cross-chain bridge launch | Bridges account for 70% of all DeFi exploit value | $100M-$600M bridge exploit (Wormhole, Ronin, Nomad scale) |
| Oracle integration | Price manipulation is the most common flash loan attack vector | $100M+ per protocol (Mango Markets, Cream Finance) |
| Governance token launch | Flash loan governance attacks can drain treasuries | $50M+ treasury theft via malicious proposal |
| Third-party protocol integration | Composition risk multiplies attack surface exponentially | Cascade failure across integrated protocols |


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "smart-contract-auditor",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

### State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

### Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## What Good Looks Like

| Excellent (10/10) | Mediocre (5/10) | Unacceptable (0/10) |
|---|---|---|
| Slither + Echidna + Manticore + Certora + Manual | Slither only + Manual review | No automated analysis, copy-paste audit |
| All invariants formalized and verified | Some invariants checked, no formal verification | No invariants defined |
| PoC exploit for every Critical/High finding | Severity labels without reproduction steps | "Code looks good" without evidence |
| 30-day remediation timeline with re-audit | Fix list without timeline or verification | No follow-up after initial report |
| Gas analysis with adversarial considerations | Gas report without security implications | Gas ignored or blindly optimized |
| Upgrade path verified with storage layout check | Upgrade tested without storage analysis | No upgrade testing |

## Deliberate Practice

| Exercise | Time | Focus |
|----------|------|-------|
| Audit Damn Vulnerable DeFi challenges 1-15 | 8 hours | Reentrancy, flash loans, oracle, governance |
| Write Echidna invariants for a Uniswap V2 fork | 4 hours | AMM invariants, reserve ratios, fee math |
| Certora CVL for a lending protocol | 6 hours | Collateralization invariants, liquidation rules |
| Manually find a reentrancy in a test contract without tools | 2 hours | Training the eye for CEI violations |
| Reconstruct a past DeFi exploit from post-mortem | 4 hours | Multi-step attack chain analysis |

## Gotchas

| # | Situation | Cost | Fix |
|---|-----------|------|-----|
| G1 | Missing CEI pattern in token withdrawal | $60M (The DAO) — full drain | Reorder: update balance → external call. Or use ReentrancyGuard. |
| G2 | Oracle uses single DEX spot price with flash loan | $100M+ (Mango Markets) — price manipulation | TWAP ≥ 30 min + Chainlink staleness check + circuit breaker |
| G3 | `delegatecall` to user-supplied address | $6M+ — full contract takeover | Only delegatecall to immutable, audited, known addresses |
| G4 | Uninitialized proxy implementation contract | $11.4M (Parity) — frozen funds | `_disableInitializers()` in implementation constructor |
| G5 | Signature replay across chains missing chainId | $5M+ — cross-chain replay attack | Include `block.chainid` in EIP-712 domain separator |
| G6 | Unchecked return value from `transfer`/`send` | $3M+ — silent failure | Use `call{value: amount}("")` or OpenZeppelin Address.sendValue |
| G7 | Storage collision in upgradeable contracts | $10M+ — data corruption | Declare `__gap` array, use namespaced storage (ERC-7201) |
| G8 | Frontrunning `approve` → `transferFrom` race | $1M+ per incident | Use `increaseAllowance`/`decreaseAllowance` pattern |

## Verification

- [ ] Slither output reviewed: zero Critical/High unresolved
- [ ] Echidna fuzzed 100K+ sequences with zero invariant breaks
- [ ] Manticore/Foundry explored all state-space branches
- [ ] All external calls follow CEI or have ReentrancyGuard
- [ ] No `tx.origin` used for authentication
- [ ] Oracle manipulation resistance verified (TWAP ≥ 30min or Chainlink)
- [ ] Upgrade path tested with storage layout diff
- [ ] All Critical/High findings have reproducible PoCs
- [ ] Gas analysis includes adversarial considerations
- [ ] Audit report follows Trail of Bits severity standards
- [ ] Remediation timeline agreed with development team
- [ ] Re-audit scheduled after fixes applied

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|----------------|---------|
| "We used OpenZeppelin, so we're safe." | Libraries are components, not guarantees. Composition bugs, initialization errors, and integration flaws bypass library security. Every DeFi hack involving OpenZeppelin proves this. |
| "Our tests have 100% coverage." | Line coverage is not state coverage. Tests verify expected behavior; exploits verify edge cases. Fuzz 100K+ random sequences to find the state combinations your tests missed. |
| "It's only a small change — no need for re-audit." | Small changes cause the biggest exploits. A one-line oracle change enabled $100M+ Mango Markets manipulation. Every code change touching state or external calls requires re-audit. |
| "The audit firm already reviewed it." | No audit is exhaustive. Audit firms miss bugs (2-5% false negative rate). Treat audits as one layer in a defense-in-depth strategy: Slither + Echidna + Manticore + Certora + manual. |
| "Formal verification is overkill for our project." | "Overkill" means you can afford the exploit. Bridges, lending protocols, and any protocol holding >$10M TVL cannot afford to skip formal verification. Certora has caught critical bugs in audited protocols. |

## References

- [13-vulnerability-taxonomy.md](references/13-vulnerability-taxonomy.md)
- [slither-config-guide.md](references/slither-config-guide.md)
- [echidna-invariant-testing.md](references/echidna-invariant-testing.md)
- [foundry-audit-workflow.md](references/foundry-audit-workflow.md)
- [formal-verification-certora.md](references/formal-verification-certora.md)
- [defi-attack-surfaces.md](references/defi-attack-surfaces.md)
- [upgradeable-contract-audit.md](references/upgradeable-contract-audit.md)
- [mev-mitigation-patterns.md](references/mev-mitigation-patterns.md)
- [audit-report-template.md](references/audit-report-template.md)
- [gas-optimization-security.md](references/gas-optimization-security.md)
