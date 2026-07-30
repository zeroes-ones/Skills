---
name: smart-contract-auditor
description: >
  Use when auditing Solidity/Vyper smart contracts for security vulnerabilities, evaluating DeFi
  protocol attack surfaces, configuring automated analysis pipelines (Slither, Echidna, Manticore,
  Foundry), assessing upgradeable contract patterns for storage collision and proxy risks, reviewing
  cross-chain bridge and oracle security, or conducting economic attack simulations. Handles
  automated analysis (Slither, Aderyn, Mythril), fuzzing (Echidna, Foundry invariant), formal
  verification (Certora Prover, Halmos, Manticore), vulnerability taxonomy (reentrancy,
  over/underflow, access control, front-running, oracle manipulation, flash loans, storage
  collision, delegatecall), DeFi attack surfaces (lending, AMM/DEX, yield, liquid staking),
  cross-chain security (bridges, message verification, replay protection), and upgradeable contracts
  (Transparent vs UUPS, Beacon proxy). Do NOT use for smart contract development
  (blockchain-developer), protocol design (blockchain-developer), or security testing
  (security-reviewer).
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
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated advice breaks real systems. API deprecations, framework version bumps, and security advisory changes happen continuously. Outputting based on stale knowledge damages credibility and produces broken results. | Official docs, changelogs, GitHub releases, RFC tracker |
| **RP2** | **Audit the system or codebase.** Read relevant files. Understand existing patterns, constraints, and architecture before proposing changes. | [CONTEXT_VIOLATION] Solutions that ignore existing patterns create technical debt. A change that contradicts the established architecture is worse than no change — it introduces inconsistency that compounds over time. | Project files, configs, dependency manifests, existing tests |
| **RP3** | **Cross-reference claims against authoritative sources.** Every factual assertion needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] Claims without sources are indistinguishable from hallucinations. The #1 cause of incorrect output is treating assumptions as facts. Source tagging prevents this. | Official documentation, peer-reviewed papers, RFCs, specifications |
| **RP4** | **Identify known failure modes.** Before recommending, list what commonly breaks. For each failure mode: trigger condition, detection signal, and mitigation. | [FAILURE_BLINDNESS] Every domain has known failure patterns. Output that doesn't address them is dangerously incomplete. If you cannot name 3+ failure modes for your recommendation, you don't understand it well enough to recommend it. | Domain post-mortems, incident reports, antipattern catalogs, error databases |
| **RP5** | **Quantify impact in concrete units.** Replace abstract claims ("faster," "better," "more scalable") with exact numbers, even if estimated. | [VAGUENESS_PENALTY] "Faster" is unverifiable. "Reduces p95 latency from 340ms to 120ms (±15ms)" is verifiable. Abstract adjectives hide ignorance behind confidence. Concrete numbers expose gaps. | Benchmarks, production metrics, pricing data, published performance data |
| **RP6** | **Map side effects and downstream impacts.** What else breaks? Which dependencies are affected? Which downstream consumers need updating? | [CASCADE_BLINDNESS] Changes to one component ripple outward. A fix in module A can break module B that depends on A's old behavior. Map the blast radius before acting. | Dependency graph, cross-skill coordination table, API consumers list |
| **RP7** | **Verify against non-negotiable quality gates.** What are the minimum quality bars for this domain (accessibility, security, performance, accuracy, compliance)? | [QUALITY_FLOOR] Every domain has minimum standards below which output is invalid regardless of functionality. Missing WCAG AA = broken. Leaking credentials = broken. Silent data loss = broken. | Domain standards, compliance frameworks, security baselines, accessibility guidelines |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? What are the known boundaries? What scenarios are explicitly out of scope? | [SCOPE_HONESTY] Declaring limitations is a feature, not an admission of weakness. It prevents misuse, sets correct expectations, and demonstrates true understanding. Every solution has boundaries — naming them is professional. | This SKILL.md, domain literature, edge case databases |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks systems, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Domain verified against changelog v2.4. No breaking changes since cutoff.]`. Partial research = partial quality. Zero research = zero credibility.



### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.


## Anti-Hallucination

* Admit uncertainty. If you cannot determine the correct approach, ask — do not guess.
* Flag your knowledge cutoff. If this project uses tools or patterns you have not seen, state your assumptions.
* Never guess security. If work touches auth, payments, or PII, route to security-reviewer.
* [VERIFIED] before any production guidance: Verify assumptions. Verify compatibility. Verify correctness.

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
## Ground Rules — Read Before Anything Else

* **Flag your knowledge cutoff.** Cryptographic standards, ZK proof systems, and smart contract platforms evolve rapidly. If your training data predates the latest FIPS/NIST publication, protocol upgrade, or EVM fork, state your cutoff date and recommend verifying against current documentation.
* **Never guess security parameters.** If you're unsure about the correct key size, curve selection, proof system parameter, or gas optimization, do NOT provide a "reasonable default." Say: "Security parameters must be verified against current best practices. I cannot provide a definitive answer without current documentation."
* **Distinguish between what you know and what you infer.** Mark statements as: [VERIFIED] — from official docs/standards, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure.

1. **REFUSE to skip Slither before manual review.** Automated scanners catch 60-80% of vulnerabilities. Skipping them wastes auditor time and misses obvious findings. Always run `slither . --print human-summary` first.

2. **DETECT -- every external call is a reentrancy vector.** Assume all external calls are malicious until proven safe via Checks-Effects-Interactions (CEI) or ReentrancyGuard. grep for `.call{` and verify state is updated before the external call.

3. **STOP -- unchecked arithmetic in Solidity <0.8.0 is a critical vulnerability.** Integer overflow/underflow can drain pools and mint infinite tokens. Require upgrade to ^0.8.0 or verified SafeMath/OpenZeppelin Math library.

4. **REFUSE to approve audit without fuzzing invariants.** Static analysis alone misses state-dependent bugs. Echidna or Foundry fuzz with 100K+ sequences is mandatory for any protocol holding value.

5. **DETECT -- `tx.origin` is NEVER for authentication.** It bypasses all intermediate contract permission checks and is phishable via any intermediate contract call. Require replacement with `msg.sender`.

6. **STOP -- `delegatecall` to untrusted addresses is a full contract takeover.** The caller's storage is fully controlled by the callee. Verify the target is immutable, audited, and from a known address.

7. **REFUSE -- Oracles must have manipulation resistance.** TWAP with <30 min window, spot price from single DEX, or unverified Chainlink feeds are all attack vectors. Require TWAP >= 30 min, Chainlink with staleness check, or dual-oracle medianizer.

8. **STOP -- signature replay attacks across chains.** If chainId is not in the EIP-712 domain separator, signatures can be replayed on any EVM chain. Verify `block.chainid` is included in all EIP-712 typed data signatures.

9. **Admit uncertainty -- never fabricate exploit PoCs.** If uncertain about exploit feasibility, say so explicitly. A hallucinated PoC that doesn't work wastes more time than admitting uncertainty. Provide a theoretical attack path with explicit caveats.
10. **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. Before writing framework-specific code, run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions. If detection succeeds, anchor all API calls to detected versions. If detection fails, request version info from user. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff."
11. **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. Estimate implementation cost in engineer-hours and compare against annual value of the change. If cost > value, gate fails. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula."

10. **Flag knowledge cutoff.** Solidity, Foundry, and DeFi patterns evolve rapidly. If training data predates the latest compiler version, Foundry release, or known exploit, state this and recommend verifying against current documentation.

<!-- QUICK: 30s -->
## The Expert's Mindset

The smart contract auditor's job is not to find bugs — it's to **think like an adversary, model economic incentives, and identify the gap between what the code says and what it actually allows**. The output is not a vulnerability list; it's a security argument that the contract is safe under a defined threat model.

### Mental Models

| Model | Description | Mechanical Trigger (detect before executing) | Violation Response |
|---|---|---|
| **The attacker thinks in compose, not isolate** | A vulnerability in Contract A + a permission in Contract B + a flash loan from Contract C = an exploit that no single-contract audit would catch. Audit the integration surface, not just the individual contracts. | | |

| **Economic security is security** | A technically correct contract can still be economically exploited if incentives align for attackers. If profit > cost-of-attack, assume an attack will occur. | | |

| **Upgradeability is a double-edged sword** | Upgradeable contracts fix bugs but introduce governance risk. An upgradeable contract with a compromised admin key is equivalent to a non-upgradeable contract with a backdoor. | | |

| **Every external call is a re-entrancy opportunity** | Even if your contract follows checks-effects-interactions, the contract you're calling might not. Cross-contract re-entrancy via read-only re-entrancy and view-function manipulation is real. | | |

### What Masters Know | |

* **The best auditors don't find more bugs — they find the bugs that matter.** A Medium-severity finding that prevents a $50M exploit is worth more than 50 Low-severity findings. Severity classification is a skill, not a formula. | |

* **business logic vulnerabilities outnumber technical vulnerabilities in production exploits.** Flash loan attacks, oracle manipulation, and governance attacks exploit correct code operating in unexpected economic conditions. Read the whitepaper before reading the code. | |

* **Every protocol has at least one Critical-severity bug at launch.** The question is whether your audit finds it or the attacker finds it first. Audit with the assumption that you're racing against an adversary who's also reading the code. | |

## When to Use

* Pre-deployment security audit of a new DeFi protocol or smart contract system
* Post-incident root cause analysis and fix verification after an exploit or close-call
* Upgradeable contract deployment (UUPS, Transparent, Beacon proxy patterns) -- verify storage layout and access control
* Third-party protocol integration review -- composition risk multiplies attack surface
* Token standard compliance audit (ERC-20, ERC-721, ERC-1155, ERC-4626)
* Gas optimization review with adversarial security analysis (not just cost reduction)
* Formal verification request for mission-critical invariants with Certora Prover or KEVM
* Cross-chain bridge or L2 contract audit -- bridge exploits account for 70% of DeFi exploit value
* Continuous audit program for protocols with frequent upgrades -- CI-integrated fuzzing pipeline

<!-- STANDARD: 3min -->
## Decision Trees **(QUICK)**

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
## Core Workflow **(STANDARD)**

### Phase 1: Automated Static Analysis (est. 1-2 hours)
1. Run Slither detection suite: `slither . --detect reentrancy-eth,reentrancy-no-eth,reentrancy-benign,reentrancy-events`
2. Print human summary: `slither . --print human-summary`
3. Print call graph: `slither . --print call-graph`
4. Print inheritance graph: `slither . --print inheritance-graph`
5. Categorize findings: Critical (direct exploit) vs High (conditional exploit) vs Medium (best practice)
**Completion criteria:** All Slither findings categorized and documented. Zero Critical or High findings unaccounted for.
Complete when: Slither detection suite run with all relevant detectors enabled. Findings categorized by severity (Critical/High/Medium) with triage notes. Human-readable summary, call graph, and inheritance graph generated and reviewed.

### Phase 2: Fuzzing Invariants (est. 4-8 hours)
1. Define 5-10 property invariants (e.g., totalSupply == sum of all balances)
2. Write Echidna test contract with property functions
3. Run `echidna . --test-mode assertion --corpus-dir corpus` for 100K+ sequences
4. Analyze invariant breaks: trace to source code, identify root cause
5. Re-fuzz after fixes to verify invariant restoration
**Completion criteria:** All invariants hold across 100K+ fuzzing sequences. Broken invariants documented with source traces.
Complete when: 5-10 property invariants defined and implemented as Echidna test contracts. Fuzzing completed with 100K+ sequences and zero invariant breaks. Any broken invariants traced to root cause with source code references and fix verification.

### Phase 3: Symbolic Execution (est. 4-8 hours)
1. Run Manticore for bytecode-level path exploration
2. Use Foundry fuzz for Solidity-level symbolic exploration: `forge test` with fuzz runs
3. Verify all branches reachable and state-space coverage
4. Document unreachable branches: are they dead code or are guards missing?
**Completion criteria:** State-space coverage report. All critical paths explored. Unreachable branches documented and justified.
Complete when: Symbolic execution completed with Manticore/Foundry fuzz exploring all reachable paths. State-space coverage report generated showing percentage of branches exercised. Unreachable branches documented with justification (dead code or missing guards).

### Phase 4: Formal Verification (est. 8-40 hours, when applicable)
1. Write Certora Verification Language (CVL) rules for mission-critical invariants
2. Run Certora Prover on critical rules: "Total collateral >= total debt at all times"
3. Parametric verification across all function argument combinations
4. Document verified invariants and any unprovable rules
**Completion criteria:** Certora verification report. All critical invariants formally proven or explicitly unprovable with rationale.
Complete when: CVL rules written for all mission-critical invariants. Certora Prover run with parametric verification across all function argument combinations. Verification report documenting proven invariants and any unprovable rules with explicit rationale.

### Phase 5: Manual Review & Report (est. 8-16 hours)
1. Business logic review: tokenomics, economic incentives, governance mechanics
2. Composition analysis: integration with external protocols, upgrade paths
3. Write audit report with Trail of Bits severity classification
4. Produce reproducible PoC for every Critical/High finding
5. Include gas analysis with adversarial considerations
6. Provide 30-day remediation timeline with re-audit recommendation
**Completion criteria:** Final audit report. All Critical/High findings have PoCs. Remediation timeline agreed with development team.
Complete when: Business logic review completed covering tokenomics, incentives, and governance mechanics. Audit report produced with Trail of Bits severity classification. Reproducible PoCs for every Critical/High finding. Gas analysis with adversarial considerations included. 30-day remediation timeline with re-audit recommendation agreed.
Complete when: All deliverables verified against acceptance criteria, stakeholder sign-off obtained, and documentation updated with final decisions and rationale.
Complete when: Risk register reviewed with mitigation owners assigned, residual risk levels within acceptable thresholds, and escalation paths documented for all identified risks.
Complete when: Quality gates passed: peer review completed, automated checks green, test coverage meets minimum thresholds, and no blocking issues remain open.

<!-- STANDARD: 3min -->
## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| Relying solely on automated tools (Slither, Mythril) without manual business logic review — automated scanners find surface-level bugs but miss protocol-specific logic flaws that cause 80% of exploits | $1M-$100M per missed logic vulnerability | Use automated tools as a first-pass triage, not the final audit. Every finding requires manual verification. Allocate 60%+ of audit time to manual code review of business logic, access control, and economic invariants. Write custom detectors for protocol-specific properties. |
| Oracle manipulation via flash loans — using a single-DEX spot price as an oracle allows attackers to manipulate the price in one transaction and drain the protocol | $5M-$500M depending on protocol TVL | Never use single-DEX spot price as oracle. Use TWAP with ≥30 min window or Chainlink with staleness checks (`answeredInRound`) and deviation circuit breakers. For high-value protocols, use dual oracles with a medianizer. |
| Upgrade proxy storage collisions — adding state variables to an upgradeable contract without managing storage layout gaps causes silent corruption of existing storage slots | $10M-$100M in corrupted funds or locked contracts | Use `_disableInitializers()` in implementation contract constructors. Maintain `__gap` storage arrays for future variables. Run storage layout diffs on every upgrade. Follow OpenZeppelin's upgradeable patterns strictly. Remove `selfdestruct` from all implementation contracts. |

## Best Practices

1. **Every external call must follow Checks-Effects-Interactions.** Update state before making external calls. ReentrancyGuard is defense-in-depth, not a replacement for correct CEI ordering. ERC-777 and ERC-721 callbacks introduce reentrancy hooks on token transfers — assume ALL external calls are malicious.
2. **Never use tx.origin for authentication.** Use `msg.sender` with OpenZeppelin's AccessControl for multi-role authorization. `tx.origin` bypasses all proxy and wallet contract protections, effectively delegating all user authority to any contract they interact with.
3. **Never use single-DEX spot price as oracle.** Spot prices are manipulatable with flash loans in a single transaction. Use TWAP (>=30 min window) or Chainlink with staleness checks (answeredInRound) and deviation circuit breakers. Dual oracles with medianizer for high-value protocols.
4. **Use Solidity >=0.8.x for built-in overflow protection.** For <0.8.0 codebases, verify SafeMath is applied to every arithmetic operation. Audit every `unchecked` block as a potential overflow vector — intentional bypass of overflow checks must be documented with rationale.
5. **Collateral ratios must be recalculated atomically within each transaction.** Flash loans can manipulate collateral values between operations. Never cache collateral ratios or debt positions across external calls. Recalculate total collateral and total debt after every state-changing operation.
6. **Upgradeable contracts need `_disableInitializers()` in the constructor.** Without it, anyone can call `initialize()` on the implementation contract and seize control. Verify `__gap` storage arrays for future variables. Run storage layout diffs on every upgrade. Remove `selfdestruct` from all implementation contracts.
7. **Signatures require EIP-712 domain separators with chainId.** Include `block.chainid`, verifying contract address, deadline timestamps, and nonces in every signature payload. Verify signer is not `address(0)`. Structured data via EIP-712 prevents cross-contract replay and blind signing.
8. **Governance proposals need timelock delays (48h+ minimum).** Flash loan governance attacks can pass malicious proposals in a single block by borrowing voting power. Use snapshot-based voting weight checkpointing. Timelock gives the community time to exit or block malicious proposals.
9. **Bridge messages must be explicitly marked as processed before execution.** Cross-chain message replay can drain entire bridges if the processed flag is never checked. Include `chainId` in message hashes. Add rate limiting on message processing per block. Verify message authenticity at every layer of the bridge stack.
10. **Delegatecall targets must be immutable or governance-controlled with timelock.** `delegatecall` to an attacker-controlled address grants full storage write access. Hardcode library addresses or store in immutable variables. If dynamic targets are required, maintain a whitelist managed by governance with timelock and verify target code hash before executing.

<!-- STANDARD: 3min -->
## Error Recovery

If a cryptographic implementation, verification, or deployment fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Implementation fails test vectors | Verify test vector source is authoritative. Check endianness, encoding, and parameter selection | Re-implement using a different verified library. Diff outputs byte-by-byte | Flag as potential library bug. File issue with maintainer with reproducible test case |
| Constant-time verification failure | Check for compiler optimizations that reintroduced branches. Use `volatile` or inline asm barriers | Rewrite the critical section using verified constant-time primitives | Accept the timing leak if below network jitter noise floor. Document residual risk |
| Dependency publishes a security advisory | Evaluate CVSS score and exploitability within 48 hours. If >= 7.0, initiate emergency patch cycle | Find an alternative library or implement a workaround | Document risk acceptance with a hard remediation deadline |
| Production deployment fails validation | Check the validation failure logs. Fix the specific validation error and re-run | Roll back to the last known-good version. Deploy incrementally | Escalate to security-engineer for expert review |

**Hard failure boundary:** If 3 independent approaches all fail, STOP. Log what was tried, capture error output, and report the blocking issue with full context.

<!-- DEEP: 10+min -->
## Error Decoder **(STANDARD)**

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
## Operating at Different Levels

| Level | Auditor Output Characteristics |
|---|---|
| **L1 — Automated scanner** | Runs Slither, Mythril, and static analysis tools. Identifies SWC-registry patterns. Produces automated finding reports. |
| **L2 — Manual code reviewer** | Reads code line-by-line. Finds logic bugs, access control issues, and integration vulnerabilities. Writes PoC exploits for findings. |
| **L3 — Protocol security engineer** | Audits full protocol architecture including tokenomics and governance. Uses Echidna/Foundry fuzzing with handcrafted invariants. Applies Trail of Bits severity classification. |
| **L4 — Economic security auditor** | Models MEV extraction, oracle manipulation, and governance attacks. Combines code audit with game-theoretic analysis of economic incentives. |
| **L5 — Research auditor** | Publishes new vulnerability classes (read-only re-entrancy, cross-chain MEV). Contributes to formal verification tooling. Expert witness for major exploits and legal cases. |

**Usage**: Say "at L3, audit this lending protocol..." or calibrate by protocol complexity. Default: **L3** (protocol-level audit).

## Production Readiness Checklist **(STANDARD)**

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

| Upstream Skill | What You Receive | When to Involve |
|-----------|-------|---------|
| **Upstream:** | `security-engineer` | Threat model, asset inventory, trust boundaries, protocol architecture review |
| **Upstream:** | `system-architect` | Protocol architecture, tokenomics, governance design, upgrade strategy |
| **Upstream:** | `backend-developer` | Off-chain components, API security, key management, relayer infrastructure |
| **Downstream** | `cryptographic-engineer` | ZKP circuit verification requirements, signature scheme audit needs |
| **Downstream** | `devops-engineer` | Deployment script audit, multisig configuration, monitoring dashboards, CI-integrated fuzzing |
| **Downstream** | `incident-responder` | Exploit detection rules, circuit breakers, pause mechanisms, monitoring alerts |

<!-- QUICK: 30s -->
## Deliberate Practice

| Level | Practice Routine | Frequency |
|---|---|---|
| **Novice** | Audit intentionally vulnerable contracts (Damn Vulnerable DeFi, Ethernaut, Capture the Ether). Write PoCs for all challenges | Weekly |
| **Competent** | Participate in audit contests (Code4rena, Sherlock, Cantina). Compare your findings with winning reports | Monthly |
| **Expert** | Audit a live mainnet protocol (with permission). Publish findings with responsible disclosure. Lead an audit contest judging | Quarterly |
| **Master** | Discover and responsibly disclose a novel vulnerability class in a production protocol. Publish detection patterns for automated scanners | Annually |

**The One Highest-Leverage Activity:** Find a past major exploit (Euler $200M, Ronin $625M, Wormhole $326M), study the post-mortem, then audit the vulnerable contract BEFORE reading the exploit details. Write down what you would have found. Then compare with the actual root cause.

## State Log

This skill maintains a **decision ledger** to prevent context drift across audit engagements.

### How the State Log Works

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for prior findings and methodology decisions.
2. **After each major decision:** Append to the ledger:

   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "smart-contract-auditor",
     "phase": "Phase 3: Manual Review",
     "decision": "Severity classification for finding F-42",
     "rationale": "CVSS score, exploitability, impact on TVL",
     "finding_id": "F-42",
     "severity": "Critical",
     "constraints": ["Must be exploitable with <$1M capital"],
     "alternatives_considered": ["Medium (team dispute)", "High (CVSS 8.7)"]
   }

   ```

3. **Before completing work:** Verify all findings, severity classifications, and methodology decisions are recorded.
4. **On context recovery:** Read the last 5 entries before proposing changes.

### Anti-Drift Check

Before beginning a new phase:
* [ ] Have I read the state log from the previous session?
* [ ] Do any prior findings constrain what I'm about to audit?
* [ ] Is my methodology consistent with prior audit decisions?
* [ ] If I'm contradicting a prior finding, have I documented WHY?

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| New DeFi protocol launches on mainnet without a public audit | Flag for security-conscious users. Track TVL growth — high TVL + no audit = high-value target | Unaudited protocols with significant TVL are the most attractive targets for blackhats |
| Major exploit occurs in a protocol using the same patterns as your audited contracts | Within 24 hours: assess if the exploit vector applies to your protocols | Exploit patterns are copy-pasteable across protocols with similar logic |
| Audit contest results published for a protocol you're about to audit | Review the winning findings before starting your audit to calibrate severity baseline | Independent auditors converge on the same Critical findings ~80% of the time |
| Solidity/EVM upgrade introduces new opcodes or changes gas schedule | Test all audited contracts against the new EVM version | Gas schedule changes can break economic assumptions in liquidation and auction logic |
| Governance proposal submitted to upgrade audited contracts | Audit the proposed upgrade code diff within 48 hours | Every upgrade invalidates the prior audit for the changed code paths |

## Anti-Patterns

### Anti-Pattern: Spot Price Oracle
**What it looks like:** Using `getReserves()` from a single Uniswap pair as the price oracle for collateral valuation, liquidation thresholds, or trading.
**Why it fails:** Anyone can flash-swap to manipulate the reserve ratio, artificially inflating or deflating the spot price within a single transaction. The manipulated price is then used to borrow against inflated collateral or trigger unfair liquidations. This is the most common DeFi exploit pattern.
**Do this instead:** Use TWAP with >=30 min window. Add Chainlink price feed as secondary oracle with deviation check. Implement circuit breaker that pauses operations when oracle deviation exceeds 15%. Use medianizer for multi-oracle feeds.

### Anti-Pattern: CEI Violation
**What it looks like:** Making an external call (`.call`, `.transfer`, `.send`) before updating internal state, then updating state after the call returns.
**Why it fails:** The external call can re-enter the same function (or any function sharing state) before the state update. The re-entered call sees the old state and can withdraw funds repeatedly (The DAO, $60M). ERC-777 and ERC-721 callbacks make this worse by introducing reentrancy hooks on token transfers.
**Do this instead:** Follow Checks-Effects-Interactions: validate inputs (Checks), update all state variables (Effects), then make external calls (Interactions). Add ReentrancyGuard modifier as defense-in-depth. Prefer pull payment patterns where users withdraw rather than the contract pushing funds.

### Anti-Pattern: `tx.origin` Authentication
**What it looks like:** `require(tx.origin == owner)` to authorize privileged operations or verify caller identity.
**Why it fails:** `tx.origin` is always the original EOA that initiated the transaction, not the immediate caller. If a user's wallet interacts with a malicious contract, that contract can call the victim's authorized functions and bypass `msg.sender` checks. This effectively delegates all user authority to any contract they interact with.
**Do this instead:** Use `msg.sender` with OpenZeppelin AccessControl for role-based authorization. For multi-sig, use a proper multi-sig wallet (Safe). Never use `tx.origin` for any authentication or authorization decision.

### Anti-Pattern: Uninitialized Proxy Implementation
**What it looks like:** Deploying an upgradeable contract where the implementation has an `initialize()` function but no `_disableInitializers()` call in the constructor.
**Why it fails:** Anyone can call `initialize()` directly on the implementation contract, setting themselves as owner/admin. They can then call `selfdestruct` (if present) to brick all proxies, or upgrade to a malicious implementation. The Parity multi-sig freeze froze $300M+ from this exact pattern.
**Do this instead:** Call `_disableInitializers()` in the implementation contract's constructor. Use OpenZeppelin's Initializable with the reinitializer guard. Remove `selfdestruct` from all upgradeable contracts. Add `__gap[50]` storage arrays for future variables. Verify storage layout compatibility on every upgrade.

### Anti-Pattern: No Range Check on User Inputs
**What it looks like:** Accepting user-supplied values (collateral ratios, fees, token amounts, slippage) without verifying they fall within expected bounds.
**Why it fails:** An attacker can supply extreme values — a 0% collateral ratio, a 100% fee, or an arbitrarily large token amount — that bypass protocol invariants. Integer overflow in older Solidity versions can also wrap values around to bypass checks. Missing range checks on exchange rate inputs have caused $100M+ oracle manipulation exploits.
**Do this instead:** Add explicit range checks: `require(value >= MIN && value <= MAX, "Out of range")`. Use Solidity >=0.8.x for built-in overflow checks. Never trust user-supplied parameters without bounds validation. Add circuit breakers that revert when parameters deviate from expected norms.

### Anti-Pattern: `delegatecall` to Untrusted Address
**What it looks like:** Using `delegatecall` with a user-supplied or dynamically-resolved target address in a proxy, library, or plugin pattern.
**Why it fails:** `delegatecall` executes the target contract's code in the caller's storage context. An attacker-controlled target can modify any storage slot, including owner, balances, and implementation address. This gives an attacker full control over the contract's entire state.
**Do this instead:** Hardcode `delegatecall` targets or store them in immutable variables. If dynamic targets are required, maintain a whitelist managed by governance with timelock. Verify the target contract's code hash before `delegatecall`. Prefer storage-collision-free patterns like ERC-7201 namespaced storage.

## What Good Looks Like

An excellent smart contract audit produces:

* **Comprehensive automated analysis:** Slither + Echidna + Manticore + Foundry all run and documented
* **Formalized invariants:** All property invariants written, verified (fuzzing or formal), with source code trace
* **Reproducible PoCs:** Every Critical/High finding has a standalone PoC exploit that demonstrates the vulnerability
* **Clear severity classification:** Trail of Bits standards with CVSS-aligned scoring, not subjective labels
* **Business logic analysis:** Tokenomics, economic incentives, and governance mechanics reviewed beyond code correctness
* **Actionable remediation:** 30-day fix timeline with verification, clear before/after code for each finding
* **Upgrade safety:** Storage layout diff, initializer verification, proxy pattern analysis
* **Gas analysis:** Adversarial considerations included (not just optimization), assembly blocks verified

Results are measured in findings caught before deployment, not post-exploit.

<!-- STANDARD: 3min -->
## Production Checklist

Before deploying or delivering work from this skill, verify:

| # | Check | Verify |
|---|-------|--------|
| ☐ | Automated analysis complete on final commit hash | `slither . --print human-summary` returns zero High/Critical; `echidna . --test-limit 100000` or `forge test --fuzz-runs 100000` passes all invariants |
| ☐ | Every external call follows CEI pattern with ReentrancyGuard | `grep -rn "\.call{" contracts/` and verify state updates precede each external call; cross-contract read-only reentrancy assessed |
| ☐ | All state-changing functions have access control — no unprotected proxy upgrades, no `tx.origin` auth | `grep -rn "onlyOwner\|onlyRole\|require(msg.sender" contracts/` on every non-view function; zero `tx.origin` references |
| ☐ | Oracle manipulation resistance verified — TWAP ≥ 30 min or Chainlink with staleness check | No spot-price-only oracles; `latestRoundData()` includes `answeredInRound` and staleness threshold; no single-DEX price feeds |
| ☐ | Upgrade safety verified — storage gap, initializer protection, no selfdestruct in implementation | Storage layout diff between versions shows no collisions; `initializer` modifier present; `selfdestruct` absent from implementation contract |
| ☐ | Every Critical/High finding has a reproducible Foundry/Hardhat PoC exploit script | Audit report appendix contains standalone `Exploit.t.sol` or `exploit.js` for each Critical/High; all PoCs verified to succeed against audited commit |
| ☐ | Audit report delivers severity methodology, finding details with before/after code, and 30-day fix timeline | Trail of Bits or CVSS-aligned severity classification; each finding has `Before:`/`After:` code blocks; remediation timeline with milestone dates |
| ☐ | Rollback plan: upgrade pause mechanism tested; emergency shutdown path documented and testnet-verified | Proxy admin can pause new upgrades; `pauseUpgrades()` tested on testnet; emergency withdrawal/shutdown script verified against forked mainnet |

## Verification Guardrails

* [ ] Automated analysis complete: Slither, Mythril, and at least one fuzzer (Echidna/Foundry) run without errors
* [ ] Every external call checked for re-entrancy (CEI pattern, re-entrancy guards, read-only re-entrancy)
* [ ] Access control: every state-changing function has appropriate modifiers/guards; no unauthorized proxy upgrades
* [ ] Integer overflow/underflow checked (Solidity >=0.8 has built-in checks; verify assembly blocks manually)
* [ ] Oracle/manipulation risk assessed: every price oracle has a manipulation threshold and fallback
* [ ] Upgrade safety verified: storage layout compatible, initializer protected, no selfdestruct in implementation
* [ ] Every Critical/High finding has a reproducible PoC exploit (Foundry test or Hardhat script)
* [ ] Audit report includes: severity methodology, finding details with PoCs, remediation guidance with before/after code
* [ ] All findings recorded in State Log with severity classification rationale

## References

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
