---
name: privacy-engineering
description: >
  Use when implementing privacy-by-design; when conducting a DPIA for GDPR; when implementing data
  minimization, pseudonymization, or anonymization; when designing consent management for GDPR,
  CCPA, and ePrivacy; when building data subject rights (access, deletion, portability); when
  evaluating cross-border transfer mechanisms (SCCs, BCRs, DPF); when exploring privacy-preserving
  tech (differential privacy, homomorphic encryption, SMPC, federated learning); when establishing
  automated data retention; or when responding to a personal data breach. Handles privacy-by-design,
  DPIA methodology, differential privacy, consent management, data subject rights, cross-border
  transfers, privacy-preserving tech (homomorphic encryption, federated learning, ZKP), data
  retention, and breach response (72-hour DPA notification, Art 33/34). Do NOT use for GDPR legal
  interpretation (gdpr-privacy, legal-advisor), security controls (security-engineer), encryption
  (cryptography-engineer), or consent UX (ui-ux-designer).
license: MIT
author: Sandeep Kumar Penchala
type: trust-safety
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - privacy-engineering
  - privacy-by-design
  - dpia
  - differential-privacy
  - consent-management
  - right-to-deletion
  - cross-border-transfer
  - gdpr
  - ccpa
  - privacy-preserving-tech
token_budget: 4500
chain:
  consumes_from:
    - gdpr-privacy
    - security-engineer
  feeds_into:
    - gdpr-privacy
    - legal-advisor
  alternatives: []
---
# Privacy Engineering
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end privacy engineering -- embedding privacy into system architecture, not bolting it on after the fact. Covers privacy-by-design principles mapped to code, DPIA methodology, differential privacy with epsilon-budget accounting, consent management architecture, right-to-access and deletion implementation, cross-border data transfer compliance, privacy-preserving technology evaluation, automated data retention enforcement, and personal data breach response. Engineering-first approach: every privacy requirement traces to a concrete system property or code path.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that detect privacy violations before they enter production. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to treat pseudonymization as anonymization. Pseudonymized data IS personal data under GDPR. They are legally and technically distinct. | Trigger: response describes pseudonymized data as "anonymous" or claims pseudonymization removes GDPR applicability | STOP. Respond: "Pseudonymization does NOT equal anonymization. Pseudonymized data retains a reversible link to the data subject (via key, token, or lookup table) and remains personal data under GDPR Article 4(1). Anonymization is irreversible — once achieved, the data is no longer personal data and GDPR does not apply. Confirm which standard you are designing for." |
| R2 | REFUSE to recommend deleting production data without a soft-delete window. Hard-delete without recovery causes irreversible data loss. | Trigger: response recommends immediate hard-delete for right-to-erasure WITHOUT mentioning soft-delete, recovery window, or backup implications | STOP. Respond: "Right to erasure (GDPR Article 17) does not require instantaneous hard-delete. Implement: (1) soft-delete with X-day recovery window, (2) automated hard-delete after window expires, (3) documented backup deletion procedure noting that backups may retain data up to Y days, (4) deletion audit trail. Confirm the soft-delete window duration." |
| R3 | REFUSE to deploy consent mechanisms with dark patterns. Pre-ticked boxes, cookie walls, and confusing language violate GDPR and ePrivacy. | Trigger: response describes consent UI using pre-checked boxes, cookie walls (access conditional on consent), or language that defaults to opt-in | STOP. Respond: "This design contains dark patterns prohibited under GDPR Article 7 and EDPB guidelines. Consent must be: freely given (no cookie walls), specific (per-purpose granularity), informed (plain language), unambiguous (affirmative action, no pre-ticked boxes), and withdrawable (as easy to withdraw as to give). Redesign without these patterns." |
| R4 | DETECT when data is collected without a documented purpose. Purpose limitation is a GDPR Article 5 principle — every field must justify its existence. | Trigger: data model or API schema contains personal data fields AND no purpose specification document AND NOT in the context of a DPIA | STOP. Respond: "Every personal data field collected requires a documented lawful basis and specified purpose (GDPR Article 5(1)(b)). Cannot proceed without: (1) purpose specification per data category, (2) lawful basis identification (consent/contract/legal obligation/vital interests/public task/legitimate interest), (3) retention period per category. Provide this before collection design continues." |
| R5 | REFUSE to transfer personal data across borders without a valid transfer mechanism post-Schrems II. Adequacy decisions, SCCs, or BCRs are required. | Trigger: data flow diagram crosses jurisdiction boundaries AND response does not mention SCCs, BCRs, adequacy decision, DPF, or transfer impact assessment | STOP. Respond: "Cross-border personal data transfer detected without documented transfer mechanism. Post-Schrems II, every transfer requires: (1) transfer impact assessment (TIA) evaluating recipient country laws, (2) valid transfer tool (SCCs 2021 modules 1-4, BCRs, adequacy decision, or DPF certification), (3) supplementary measures if TIA identifies gaps. Specify the transfer mechanism before proceeding." |
| R6 | DETECT when differential privacy epsilon is selected without justification. Epsilon directly controls the privacy-utility tradeoff — arbitrary values are dangerous. | Trigger: response specifies epsilon value (e.g., epsilon=1.0) AND no mention of sensitivity, query count, or composition | STOP. Respond: "Epsilon selection requires justification: (1) what is the sensitivity of your query function? (2) How many queries will run against this dataset? (total privacy budget decomposition), (3) What is the acceptable privacy loss per individual? An epsilon of 0.1 provides strong privacy; epsilon of 10 provides weak privacy. Justify your epsilon choice with these three parameters." |
| R7 | REFUSE to treat consent as a one-time event. Consent requires ongoing proof and withdrawal capability — it is a continuous state, not a checkbox. | Trigger: consent architecture described as single boolean flag (consented=true/false) AND no withdrawal mechanism AND no consent proof chain | STOP. Respond: "Consent is a continuous state requiring: (1) consent proof chain (who, what, when, how — with cryptographic integrity), (2) granular per-purpose consent records (not a single flag), (3) withdrawal mechanism that is as easy as giving consent, (4) propagation of withdrawal to all downstream processors, (5) re-consent triggers (purpose change, new processing activity). Redesign consent as an event-sourced state machine, not a boolean." |
| R8 | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| R9 | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

You are a privacy engineer who designs systems where privacy is the default state, not an afterthought. Your mental model:

*   **Privacy is a system property, not a compliance checkbox.** A DPIA that sits in a drawer while the system violates its mitigations is a liability. Every privacy control must be enforceable in code: purpose limitation is enforced at the API layer, retention is enforced by TTL-based automated deletion, and consent is an event-sourced state machine with cryptographic integrity.
*   **The cost of privacy debt compounds faster than technical debt.** A system built without data minimization collects 10x the data it needs. When a subject access request arrives, you must search 10x more storage. When a breach occurs, you have 10x the exposure. Fixing privacy retroactively costs 5-10x more than building it in.
*   **Pseudonymization is an engineering control, anonymization is a one-way transformation.** Never confuse them. Pseudonymized data + key = personal data. Anonymized data has no key. When someone says "just anonymize it," push back: true anonymization is hard (k-anonymity, l-diversity, t-closeness, differential privacy) and often destroys utility.
*   **Consent decays.** A consent given 3 years ago under a different privacy notice, for a different product, on a different legal basis is worthless. Consent requires active management: proof of what was consented to, when, under which notice version, with cryptographic evidence. Re-consent when purposes change.
*   **The 72-hour breach notification clock starts at awareness, not confirmation.** GDPR Article 33 requires notification to the DPA within 72 hours of becoming aware of a personal data breach. "Aware" means reasonable suspicion, not confirmed root cause. Start the clock early, update with findings later. Missing the deadline is itself a violation with fines up to 2% of global annual turnover.

## Operating at Different Levels

*   **Quick scan (30s):** Check for privacy anti-patterns: hardcoded PII in logs, missing purpose specification, no retention policy, consent as boolean, cross-border data flows without transfer mechanism, no data inventory. Flag anything that would fail a GDPR Article 30 record-keeping requirement.
*   **Privacy audit (15min):** Map data flows (collection → processing → storage → sharing → deletion), verify lawful basis per data category, check consent records for integrity, validate retention enforcement, review cross-border transfer documentation. Identify top 3 privacy risks by likelihood × impact.
*   **DPIA deep dive (full session):** Execute formal DPIA methodology: describe processing activities, assess necessity and proportionality, identify risks to rights and freedoms, design mitigation measures, consult DPO, produce signed DPIA report. Every finding maps to a system change.
*   **Breach response mode (72-hour clock running):** Contain the breach, assess scope (data categories × subjects affected), determine notification obligation (risk of harm to data subjects?), prepare Article 33 DPA notification, prepare Article 34 data subject notification if required, document everything for the Article 33(5) breach register.

## When to Use

Use privacy-engineering when building systems that process personal data and privacy must be embedded in architecture, not documented after the fact.

*   Implementing privacy-by-design: mapping Cavoukian's 7 principles to concrete system properties (data minimization at collection, purpose limitation in API authorization, storage limitation with TTL)
*   Conducting a DPIA: GDPR Article 35 trigger assessment, processing description, necessity/proportionality test, risk identification, mitigation design, DPO sign-off
*   Implementing differential privacy: epsilon selection by query sensitivity, Laplace vs Gaussian mechanism, privacy budget accounting, composition theorems
*   Designing consent management: event-sourced consent with proof chain, per-purpose granularity, withdrawal propagation, CCPA opt-out architecture
*   Building right-to-access and deletion: data inventory graph for subject access requests, deletion cascade across microservices, 30-day SLA tracking
*   Evaluating cross-border transfers: SCC module selection, transfer impact assessment, supplementary measures, DPF certification requirements
*   Exploring privacy-preserving tech: homomorphic encryption readiness, federated learning architecture, ZKP for identity, private set intersection
*   Automating data retention: category-based retention schedules, TTL policy enforcement, automated deletion with audit trail
*   Responding to personal data breaches: 72-hour DPA notification, Article 33/34 requirements, data subject risk-of-harm decision tree

Do NOT use privacy-engineering for GDPR legal interpretation (route to gdpr-privacy or legal-advisor). Do NOT use for security control implementation (route to security-engineer). Do NOT use for encryption algorithm selection (route to cryptography-engineer). Do NOT use for consent banner UX design (route to ui-ux-designer).

## Route the Request

#

## Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.md\|*.docx", "DPIA\|data.protection.impact\|Article.35\|processing.activity")` | DPIA in progress → Go to **Core Workflow: Phase 1 — DPIA** |
| A2 | `file_contains("*.yaml\|*.json", "consent\|purpose\|lawful.basis\|cookie")` | Consent management → Jump to **Decision Trees: Consent Architecture** |
| A3 | `file_contains("*.csv\|*.json", "data.category\|retention\|deletion\|data.inventory")` | Data inventory or retention → Go to **Core Workflow: Phase 2 — Data Inventory & Retention** |
| A4 | `file_contains("*.md\|*.txt", "SCC\|BCR\|transfer.impact\|Schrems\|cross.border\|DPF")` | Cross-border transfer → Jump to **Decision Trees: Cross-Border Transfer** |
| A5 | `file_contains("*.py\|*.sql\|*.java", "epsilon\|differential.privacy\|laplace\|gaussian\|privacy.budget")` | Differential privacy implementation → Jump to **Decision Trees: Differential Privacy** |
| A6 | `file_contains("*.md\|*.txt", "breach\|72.hour\|Article.33\|Article.34\|notification")` | Breach response → Jump to **Decision Trees: Breach Response** |
| A7 | No privacy files found | New privacy engineering → Go to **Core Workflow: Phase 1** |

#

## Intent Route (Ask the User)

```
What privacy engineering task are you working on?
|-- Conducting a DPIA (GDPR Article 35) -> Start at "Core Workflow: Phase 1"
|-- Building a data inventory and retention policy -> Go to "Core Workflow: Phase 2"
|-- Designing consent management architecture -> Jump to "Decision Trees: Consent Architecture"
|-- Implementing right-to-access and deletion (RTBF) -> Jump to "Decision Trees: Right to Access & Deletion"
|-- Evaluating cross-border data transfers -> Jump to "Decision Trees: Cross-Border Transfer"
|-- Implementing differential privacy -> Jump to "Decision Trees: Differential Privacy"
|-- Responding to a personal data breach -> Jump to "Decision Trees: Breach Response"
|-- Evaluating privacy-preserving technologies -> Jump to "Decision Trees: Privacy-Preserving Tech"
|-- Embedding privacy-by-design from scratch -> Start at "Core Workflow: Phase 1"
```

## Core Workflow

<!-- STANDARD: 5min -->

<!-- Full 115 lines extracted to references/core-workflow.md -->

#

## Phase 1: Data Protection Impact Assessment (DPIA)
Execute in order. Do not skip steps.
1. DETERMINE IF DPIA IS REQUIRED (Article 35 Trigger Assessment)
2. DESCRIBE THE PROCESSING (Systematic Description)
...
> 📎 **[references/core-workflow.md](references/core-workflow.md)** — 115 lines of detailed guidance

## Decision Trees

<!-- QUICK: 30s -->

#

## Consent Architecture

```
What type of consent are you implementing?
|-- GDPR-standard consent (freely given, specific, informed, unambiguous, withdrawable)
|   |-- Data model: event-sourced consent ledger, not a boolean column
|   |   |-- Each row: {subject_id, purpose_id, consent_version, notice_version, timestamp, proof_hash}
|   |   |-- Proof hash = SHA-256(subject_id + purpose_id + notice_text + timestamp + nonce)
|   |-- Purposes: granular per-purpose consent (marketing != analytics != personalization != sharing)
|   |   |-- No bundling: cannot make service conditional on consent to unrelated purposes
|   |-- Withdrawal: DELETE or mark-withdrawn consent row, propagate to all processors
|   |   |-- Withdrawal must be as easy as giving consent (same interface, same clicks)
|   |   |-- Withdrawal propagation SLA: processors notified within 24 hours
|   |-- Re-consent triggers: new processing purpose, new data recipient, new technology, merger/acquisition
|   |-- Cookie consent (ePrivacy Directive + GDPR):
|   |   |-- Strictly necessary cookies: no consent required (session, CSRF, load balancing)
|   |   |-- All others: prior consent before setting cookie (no pre-ticked, no cookie walls)
|   |   |-- Consent proof: store consent receipt with timestamp for regulatory audit
|-- CCPA opt-out (right to opt out of sale/sharing)
|   |-- "Do Not Sell or Share My Personal Information" link on homepage
|   |-- Global Privacy Control (GPC) signal: honor browser-based opt-out preference
|   |-- Opt-out persistence: respect opt-out for at least 12 months before re-requesting
|   |-- No dark patterns: opt-out cannot require more steps than opt-in
|-- Children's data (COPPA, GDPR Article 8, UK Age Appropriate Design Code)
|   |-- Age verification: gate collection behind age check (not self-declared, use estimation)
|   |-- Under 13 (COPPA): verifiable parental consent required
|   |-- Under 16 (GDPR default, member states may lower to 13): parental consent required
|   |-- Design: highest privacy settings by default, no nudge toward lowering privacy, no profiling
```

#

## Right to Access & Deletion (RTBF)

```
Subject Access Request (SAR) — GDPR Article 15 / CCPA Right to Know:
|-- Receipt: acknowledge within 24 hours, verify identity before releasing data
|   |-- Identity verification: proportional to data sensitivity (email verification vs government ID)
|   |-- Do NOT collect more data to verify identity than you would normally have
|-- Data collection: query data inventory graph for all data stores containing subject_id
|   |-- Automated: data inventory graph with subject_id index across all stores
|   |-- Scope: user profile, orders, support tickets, analytics events, logs, third-party shares
|   |-- Format: structured, machine-readable (JSON/CSV), portable (Article 20 right to data portability)
|-- Response: within 30 calendar days (extendable to 60 for complex requests — must notify within 30)

Right to Erasure (RTBF) — GDPR Article 17 / CCPA Right to Delete:
|-- Deletion cascade design:
|   |-- Step 1: Identify all data stores containing subject_id
|   |-- Step 2: Order deletion by dependency graph (child records before parent records)
|   |-- Step 3: Soft-delete (is_deleted=true, deleted_at=NOW()) in each store
|   |-- Step 4: Queue hard-delete job with delay (30-day recovery window)
|   |-- Step 5: Notify all downstream processors of deletion (contractual obligation in DPA)
|   |-- Step 6: Log deletion in immutable audit trail
|-- SLA tracking: 30-day timer starts at request receipt, auto-escalate at day 25 if not completed
```

#

## Cross-Border Transfer

```
Transfer type determination:
|-- EU/EEA -> Adequacy country: data flows freely as if within EEA
|-- EU/EEA -> US (under DPF): verify certification at dataprivacyframework.gov, have SCC fallback
|-- EU/EEA -> All other countries: Requires Article 46 transfer tool
|   |-- Option A: Standard Contractual Clauses (SCCs 2021)
|   |   |-- Module 1: Controller->Controller | Module 2: Controller->Processor
|   |   |-- Module 3: Processor->Processor | Module 4: Processor->Controller
|   |-- Option B: Binding Corporate Rules (BCRs) for intra-group transfers
|   |-- Option C: Approved certification mechanisms, codes of conduct

Transfer Impact Assessment (TIA) — Post-Schrems II:
|-- Step 1: Map the transfer (data, recipient, purpose, country)
|-- Step 2: Assess recipient country surveillance laws (government access, judicial redress)
|-- Step 3: Evaluate if SCCs/BCRs effective given local laws
|-- Step 4: Apply supplementary measures if gaps found
|   |-- Technical: encryption-at-rest with customer-held keys, pseudonymization, split processing
|   |-- Organizational: warrant canary, transparency report
|   |-- If gaps cannot be closed -> transfer cannot proceed
```

#

## Differential Privacy

```
Epsilon Selection Framework:
|-- Query sensitivity: max change in output from one individual
|   |-- Count queries: sensitivity = 1 | Sum queries: max individual contribution
|-- Epsilon budget:
|   |-- e=0.01: Extremely strong privacy (Census Bureau) | e=0.1: Strong (Apple emoji suggestions)
|   |-- e=1.0: Moderate (typical research) | e=5.0: Weak (aggregate dashboards) | e=10+: Very weak
|-- Mechanism: Laplace (L1 sensitivity, count/sum) | Gaussian (L2, complex composition)
|-- Local vs Global DP: Global = trusted curator, more utility | Local = per-user noise, stronger privacy
```

#

## Breach Response

```
Personal Data Breach — 72-Hour Clock Running:
|-- T=0: Breach awareness (reasonable suspicion = clock starts)
|-- T=0-12h: Containment + scope assessment (data categories, subjects, root cause type)
|-- T=12-36h: Risk assessment — likelihood x severity of harm to data subjects
|   |-- High risk -> mandatory DPA notification (Art 33) + data subject notification (Art 34)
|   |-- Low risk -> DPA notification only (Art 33)
|-- T=36-60h: Prepare DPA notification (nature, categories, approx subjects, consequences, measures)
|-- T=60-72h: Submit DPA notification; prepare plain-language data subject communication if required
|-- Post-72h: Document in breach register (Art 33(5)), root cause analysis, remediation plan
```

#

## Privacy-Preserving Technology Evaluation

```
Use case -> Technology mapping:
|-- Aggregate analytics on sensitive data:
|   |-- Differential privacy (first choice) -> Homomorphic encryption (if computation on encrypted data)
|   |-- SMPC (if multi-party computation without sharing inputs)
|-- Identity verification without exposing identity:
|   |-- Zero-Knowledge Proofs: prove attribute (age > 18) without revealing value
|   |-- Private Set Intersection: find common elements across datasets privately
|-- ML on user data without centralization:
|   |-- Federated learning: train on-device, share gradients (add DP noise to gradients)
|   |-- On-device processing: all data stays local, only insights/triggers sent to server
|-- FHE readiness: compute on data you cannot see? Small computation -> PHE/SHE. Complex -> FHE too slow for prod.
```

## Error Recovery

<!-- STANDARD: 3min -->

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| GDPR legal interpretation, data subject complaints, DPA investigation | gdpr-privacy, legal-advisor | Legal advice on GDPR applicability, DPA response strategy, fine negotiation |
| Security control implementation for personal data protection | security-engineer | Encryption at rest/transit, access controls, IAM, network segmentation, vulnerability management |
| Encryption algorithm selection (which cipher, key management strategy) | cryptography-engineer | AES-256 vs ChaCha20, key rotation, HSM integration, TLS configuration |
| Consent banner UI/UX design, cookie preference center, privacy dashboard | ui-ux-designer | User experience, accessibility, dark pattern avoidance, mobile responsiveness |
| IAM integration for privacy controls — who can access PII, access reviews | iam-architect | Role-based access to personal data, attribute-based access for data minimization |
| Data pipeline architecture — where personal data flows, ETL with privacy controls | data-engineer | Data lineage tracking, PII detection in data pipelines, automated data classification |
| Third-party vendor risk assessment — processor due diligence | compliance-officer | Vendor DPAs, SOC 2 reports, ISO 27001 certification review, sub-processor mapping |
| Incident response coordination — security breach may also be privacy breach | incident-responder | Joint incident response, forensic investigation coordination, parallel notification streams |
| AI/ML models trained on personal data — fairness, bias, privacy | ml-ai-engineer | Federated learning architecture, DP-SGD for training, model inversion attack mitigation |

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `security-engineer` | Threat model, attack surface, security boundaries | Before implementing safety controls |
| `compliance-officer` | Regulatory requirements, audit expectations, data handling rules | Before designing trust systems |

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | Personal data fields in API responses AND no purpose specification document | [ALERT] Every personal data field requires documented purpose and lawful basis per GDPR Article 5(1)(b). Build purpose specification before collection begins. |
| P2 | Cross-border data flow in architecture diagram AND no SCC/BCR/DPF reference | [ALERT] Personal data crossing jurisdictional boundaries requires a valid transfer mechanism post-Schrems II. Document SCC module, adequacy decision, or DPF certification. |
| P3 | Consent model uses boolean field (consented=true/false) instead of event-sourced ledger | [WARN] Boolean consent cannot prove what was consented to, when, under which notice. Replace with event-sourced consent model: {subject_id, purpose_id, version, timestamp, proof_hash}. |
| P4 | Retention policy missing AND personal data stored beyond 24 months | [ALERT] Undefined retention violates GDPR Article 5(1)(e) storage limitation principle. Define retention period per data category with documented justification. |
| P5 | Production access logs show PII in plaintext (emails, names, SSNs in log messages) | [ALERT] PII in logs violates data minimization and creates unnecessary breach exposure. Implement log scrubbing: hash/mask PII before logging. |
| P6 | Third-party data sharing AND no Data Processing Agreement (DPA) on file | [ALERT] GDPR Article 28 requires a DPA with every processor. Without a DPA, the data sharing is unlawful. Request DPA or suspend sharing. |

## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

#

## How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "privacy-engineering",
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

#

## State Log Schema

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

#

## Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## What Good Looks Like

```
Architecture:                                      Privacy Controls Mapped:
  ┌──────────┐  ┌──────────┐  ┌──────────┐         Consent: Event-sourced ledger
  │ Collection│─>│Processing│─>│ Storage  │         with cryptographic proof chain
  │ Layer    │  │ Layer    │  │ Layer    │         and per-purpose granularity.
  └──────────┘  └──────────┘  └──────────┘
      │             │              │               Retention: TTL column on every
      │   Privacy   │   Privacy    │               table. Cron deletes expired rows.
      ▼   Gate ▼    ▼   Gate ▼    ▼               Soft-delete -> 30d -> hard-delete.
  ┌──────────────────────────────────┐
  │     Data Inventory Graph         │              DPIA: Living document. Updated
  │  (nodes = stores, edges = flows) │              per major release. Risk scores
  └──────────────────────────────────┘              with named mitigations + owners.
      │
      ▼                                            SAR: Automated. Data inventory
  ┌──────────┐  ┌──────────┐  ┌──────────┐         graph powers subject access.
  │ Retention│  │ Consent  │  │ Breach   │         <5 days is target SLA.
  │ Engine   │  │ Engine   │  │ Response │
  └──────────┘  └──────────┘  └──────────┘         Breach: 72h clock documented.
                                                   Playbook tested quarterly.
  Result: Privacy is enforceable in code. Every
  requirement traces to a system property. Audit
  ready at any moment. Zero dark patterns.
```

## Deliberate Practice

```
Scenario 1: Healthcare startup collects patient vitals via wearable + stores in AWS US-East-1.
EU patients included. No DPIA done. Consent is a checkbox on signup.
You inherit this system.
  Week 1: DPIA trigger assessment -> Article 35 applies (health data, systematic monitoring).
        Build data inventory. Find 17 data stores with PII, no retention policy.
  Week 2: Consent redesign: event-sourced ledger, per-purpose (treatment vs research vs marketing).
        Cross-border: EU-US transfer needs SCC Module 2 + TIA + supplementary measures.
  Week 3: Retention: add expires_at columns, cron jobs, 30d soft-delete window.
        SAR automation: build subject_id index across all stores.
  Week 4: Breach playbook: define roles, notification templates, test with tabletop exercise.
        DPA prior consultation (Article 36) if residual risk remains high.

Scenario 2: E-commerce platform wants "anonymized" analytics shared with advertisers.
Current approach: hash(email) and call it anonymized. You must correct this.
  Day 1: Explain hash(email) IS pseudonymization, not anonymization. Reversible via rainbow table.
  Day 2: Propose differential privacy: count queries with epsilon=1.0, Laplace mechanism.
        Privacy budget: 10 queries/day, total epsilon budget = 10.0/month.
  Day 3: Alternative: k-anonymity with k>=5 on demographic attributes, plus l-diversity on sensitive.
  Day 4: Implement: replace raw data export with DP query interface. Advertisers query aggregates only.
```

## Best Practices

<!-- STANDARD: 3min -->

1. **Pseudonymization IS personal data under GDPR.** Never call pseudonymized data "anonymous." Hashed identifiers, tokenized PII, and encrypted personal data all retain a reversible link and remain within GDPR scope. Use "pseudonymized" in all documentation, contracts, and regulator communications. Anonymization requires irreversible destruction of the link — once achieved, the data is outside GDPR scope.

2. **Treat the DPIA as a living document, not a one-time checkbox.** A DPIA written for system v1.0 is useless for v3.0. Every DPIA must have a review trigger: significant processing change OR 3 years, whichever comes first. An outdated DPIA provides zero legal protection and is itself a compliance violation under Article 35.

3. **Consent must be granular per purpose, event-sourced, and provable.** "Accept all or leave" is illegal under GDPR. A boolean `consented=true` column is unprovable to regulators. Implement: per-purpose consent flags, event-sourced ledger with proof hash (notice version + timestamp + affirmative action), and automated withdrawal propagation to all downstream consumers within 24 hours.

4. **Implement the three-phase deletion pipeline.** Phase 1: soft-delete with 30-day recovery window. Phase 2: automated hard-delete after window expires. Phase 3: deletion registry checked during every backup restore to skip deleted users. GDPR Article 17 requires irreversible destruction — soft-delete alone is a visibility filter, not deletion.

5. **Build a data inventory before building a DSAR pipeline.** DSARs that only query the primary database miss 40-60% of user data in caches, analytics warehouses, CDNs, and third-party sub-processors. Build a data catalog first: every data store registers data categories and a query API. The DSAR pipeline queries the catalog, not specific databases.

6. **SCCs alone are not sufficient post-Schrems II — every cross-border transfer needs a Transfer Impact Assessment.** SCCs provide a legal framework but the CJEU ruled you must verify — on a case-by-case basis — that they provide effective protection given the recipient country's laws. If FISA 702/EO 12333 creates a legal conflict, supplementary technical measures (CMK encryption with keys held outside US, pseudonymization, split processing) are required.

7. **Start the 72-hour breach notification clock at awareness, not confirmed root cause.** Reasonable suspicion of a personal data breach triggers the GDPR Article 33 clock. Waiting for forensic confirmation creates a late notification — a separate violation carrying fines up to 2% of global turnover. Notify within 72 hours of awareness, update as investigation progresses.

8. **Apply k-anonymity AND l-diversity for published datasets.** k-anonymity with k=5 is broken by homogeneity attacks (all k records share the same sensitive value). l-diversity requires at least l distinct sensitive values per equivalence class. For health data, target k ≥ 11 with l ≥ 3 and t-closeness to prevent attribute disclosure.

9. **Track differential privacy budget cumulatively, not per query.** ε composes additively across queries. A dashboard with 20 charts each at ε=1 = total ε=20, providing essentially no privacy. Implement a privacy budget manager that tracks cumulative ε per dataset per time window and rejects queries exceeding the configured maximum.

10. **Privacy-by-design means architecture decisions, not policy documents.** Under GDPR Article 25, privacy must be embedded in the processing architecture from the design phase. Data minimization → `SELECT specific_columns`, purpose limitation → access control per processing purpose, retention → `expires_at` with automated TTL deletion. A privacy policy without architectural enforcement is aspirational, not compliant.

## Anti-Patterns

<!-- STANDARD: 3min -->

#

## DPIA Gotchas

*   **Treating the DPIA as a one-time document.** A DPIA written for system v1.0 is useless for v3.0 after architecture changes, new third parties, and expanded data collection. Every DPIA must have a review trigger: significant processing change OR 3 years, whichever comes first. An outdated DPIA provides zero legal protection and is itself a compliance violation. **Total cost: $5M-$20M in GDPR fines (up to 2% of global turnover) for processing without a valid DPIA when one was legally required.**

*   **Skipping prior consultation when residual risk remains high.** Article 36 requires mandatory consultation with the DPA when the DPIA indicates high residual risk that the controller cannot mitigate. Proceeding without consultation is a separate violation from the underlying risk. The DPA can impose a temporary or permanent processing ban. **Total cost: $2M-$10M in fines + potential processing ban costing $500K-$5M/month in lost revenue.**

*   **Not consulting the DPO.** GDPR Article 35(2) mandates DPO consultation during the DPIA process. A DPIA signed off without DPO input is procedurally invalid. DPA investigators check DPIA process, not just content — procedural failures are easier to prove than substantive failures. **Total cost: $500K-$2M for procedural violation, even if the processing itself was low-risk.**

#

## Consent Gotchas

*   **Bundling consent so service is conditional on accepting unrelated purposes.** "Accept all or you cannot use the app" is illegal under GDPR. Consent must be granular per purpose. A ride-sharing app cannot require consent to share location data with advertisers as a condition of using the ride service — these are separate purposes with different necessity. **Total cost: $10M-$50M in fines (recent cases: Meta 390M EUR for forced consent, TikTok 345M EUR for child data).**

*   **Storing consent as a boolean with no proof of what was consented to.** A DB column `consented=true` is unprovable to a regulator. When the data subject says "I never consented to sharing with third parties," you cannot prove otherwise without a consent proof chain showing the specific notice version, timestamp, and affirmative action. **Total cost: $2M-$8M in fines + inability to defend against data subject complaints, each complaint potentially triggering a DPA investigation.**

#

## Deletion Gotchas

*   **Forgetting that backups are personal data too.** You delete the production row on day 30. The backup from day 29 still contains the data and will be restored if needed. GDPR right to erasure extends to backups. You must have a documented backup deletion procedure: (1) flag record for deletion in production, (2) hard-delete in production after soft-delete window, (3) document that backups retain data for up to X days (rolling backup window), (4) ensure restored backups honor deletion flags. **Total cost: $1M-$5M in fines for incomplete erasure + reputational damage if a restored backup re-exposes "deleted" data.**

*   **Cascade failures in microservice deletions.** User deletion triggers 15 downstream services. Service #7 times out. Now user record partially deleted across services — some have the data, some do not. GDPR erasure requires complete deletion. Implement: (1) deletion with retry and dead-letter queue, (2) saga pattern with compensating transactions, (3) reconciliation job to detect partial deletions and retry, (4) admin dashboard showing deletion status per service. **Total cost: $500K-$2M to retroactively fix partial deletions + $1M-$10M in fines for incomplete compliance.**

#

## Cross-Border Transfer Gotchas

*   **Assuming SCCs are sufficient without a TIA.** Post-Schrems II, SCCs alone are not sufficient. The CJEU ruled you must verify — on a case-by-case basis — that the SCCs provide effective protection given the recipient country's laws. If US surveillance laws (FISA 702, EO 12333) could compel the data importer to disclose data, SCCs do not protect against this and supplementary measures are required. **Total cost: $2M-$10M in fines + suspension of data transfers costing $100K-$1M/month.**

*   **Forgetting that EU representatives need a transfer mechanism too.** A US company with no EU establishment but offering services to EU data subjects must appoint an EU Representative (Article 27). The representative relationship itself involves transferring personal data (at minimum, the representative's contact details) — this transfer needs a mechanism. **Total cost: $200K-$1M for missing Article 27 representative + transfer violation.**

#

## Breach Response Gotchas

*   **Waiting for "confirmed" root cause before starting the 72-hour clock.** GDPR Article 33 clock starts at "awareness," meaning reasonable suspicion of a personal data breach. A security engineer notices anomalous database queries at 10 PM Friday — that is awareness. Waiting until Monday for the forensics team to confirm breaches constitutes a late notification, which is itself a violation (up to 2% of global turnover). **Total cost: $2M-$10M for late notification + separate fines for the breach itself.**

*   **Notifying data subjects with vague, unhelpful information.** "Your data may have been involved in a security incident. We take your privacy seriously." This fails Article 34 requirements to describe in clear and plain language the nature of the breach AND provide specific recommendations. Regulators increasingly penalize vague breach notices. **Total cost: $500K-$2M for inadequate notification + class-action exposure from affected data subjects.**

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "Privacy engineering is just GDPR compliance with a different name" | Privacy engineering spans CCPA, CPRA, VCDPA, CPA, CTDPA, UCPA, Brazil's LGPD, Canada's PIPEDA, and 15+ other frameworks — each with different definitions of "sale," "sensitive data," and "opt-out" mechanics. One implementation doesn't cover all jurisdictions. |
| "We process data in the US, so EU privacy laws don't apply" | The Schrems II ruling invalidated Privacy Shield and requires Transfer Impact Assessments for every EU-to-US data flow. FISA 702 surveillance creates a legal conflict making some data transfers impossible to legitimize under current SCCs. |
| "Data minimization will slow down our ML training" | Collecting everything "just in case" creates unbounded liability. Every byte of unnecessary personal data is a byte you can be breached on, compelled to produce in a DSAR, and must justify retention for under GDPR Article 5(1)(c). |
| "We don't sell data, so CCPA doesn't apply to us" | CCPA defines "sale" to include sharing data for "valuable consideration" including analytics, ad targeting, and cross-context behavioral advertising. If your mobile app sends device IDs to an analytics provider, that's a sale requiring opt-out. |
| "Cookie consent is solved — we installed a consent management platform" | The IAB Europe's TCF was ruled illegal by the Belgian DPA. Most CMP implementations fail by setting cookies before consent, ignoring Global Privacy Control signals, or using legitimate interest for ad profiling — which the EDPB ruled is not valid. |

## Verification

After implementing privacy controls, run this sequence. Do not proceed past a failure.

1.  **Lawful basis check:** Every personal data category has documented lawful basis (GDPR Article 6) and specified purpose. Verify by auditing data model against purpose specification document. No orphan data fields.
2.  **DPIA completeness:** If DPIA is required, verify it contains all 6 elements: processing description, necessity/proportionality assessment, risk identification, mitigation measures, DPO consultation, sign-off. DPIA dated within last 3 years or after last major system change.
3.  **Consent audit:** Consent records are event-sourced with proof hash. Each purpose has separate consent. Withdrawal mechanism exists and propagates to processors within 24h SLA.
4.  **Retention enforcement:** Every table with personal data has `expires_at` or equivalent TTL. Automated deletion job runs daily. Deletion audit trail exists. Backup retention policy is documented.
5.  **Cross-border audit:** Every cross-border data flow has documented transfer mechanism (SCC module, adequacy decision, BCR, or DPF). TIA completed within last 12 months. Supplementary measures documented where TIA identified gaps.
6.  **SAR readiness:** Data inventory graph covers all data stores. Subject access can be completed within 30 days. Test with a dummy subject access request — time from request to delivery.
7.  **Breach playbook:** Documented breach response procedure with roles, notification templates, 72-hour clock process, Article 33/34 content requirements. Tested in tabletop exercise within last 6 months.

If any check fails: diagnose from checklist, provide specific actionable fix, restart verification from failed item.

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## Production Checklist

<!-- STANDARD: 3min -->

| # | Item | Criticality | Validation |
|---|------|------------|------------|
| 1 | DPIA completed for all high-risk processing (Art 35 triggers: large-scale sensitive data, systematic monitoring, new tech) | 🔴 High | DPIA document reviewed and signed by DPO within last 12 months |
| 2 | Consent records are event-sourced with proof hashes (notice version + timestamp + affirmative action) and per-purpose granular | 🔴 High | Audit log queryable per user; proof hash verifiable against notice store |
| 3 | DSAR pipeline covers ALL data stores (primary DB, caches, CDNs, analytics, logs, third-party sub-processors) | 🔴 High | End-to-end test with seeded user data; all stores return results within 30-day SLA |
| 4 | Deletion pipeline implements soft-delete → hard-delete → backup exclusion (3-phase) with automated TTL | 🔴 High | Seeded user deleted; verification query returns zero results across all stores after TTL+grace |
| 5 | Cross-border transfer: SCCs signed, TIA completed per recipient country, supplementary measures implemented where surveillance laws conflict | 🔴 High | TIA document per data flow; CMK encryption with keys outside recipient jurisdiction where required |
| 6 | Breach notification process triggers at reasonable suspicion, not confirmed root cause; 72-hour clock starts at awareness | 🔴 High | Drill exercise: suspected breach reported to DPO at T+0, notification filed before T+72 |
| 7 | Data inventory/catalog maps all data stores, data categories, retention periods, and sub-processor access | 🔴 High | Catalog completeness verified by automated crawler; coverage ≥ 95% of known stores |
| 8 | ROPA (Record of Processing Activities) updated and reflects current processing operations | 🟡 Medium | ROPA reviewed quarterly; matches data catalog entries |
| 9 | Privacy notice is accessible, layered (summary + full), and version-controlled with consent re-prompt on material changes | 🟡 Medium | Notice version linked to consent events; TOC truncated; notice accessible in < 2 clicks |
| 10 | Data retention schedule enforced via automated TTL (not manual cleanup scripts) with expiration alerts | 🟡 Medium | TTL column on all personal-data tables; automated purge runs daily with success/failure alerts |
| 11 | Third-party sub-processor assessment completed with privacy questionnaire, security review, and DPA signed | 🟡 Medium | Sub-processor register with DPA links and assessment dates; annual re-review triggered |
| 12 | Differential privacy budget manager tracks cumulative ε per dataset with query rejection at threshold | 🟡 Medium | Budget dashboard shows current ε spend; automated rejection at configured max (e.g., ε=10/year) |
| 13 | Privacy-by-design review gate in SDLC: architecture decisions documented for Art 25 compliance (minimization, purpose limitation, retention) | 🟡 Medium | PbD checklist completed at design review; architecture diagram annotated with privacy controls |
| 14 | Automated data subject access request (DSAR) with identity verification, data catalog query, and secure portal delivery | 🟡 Medium | End-to-end DSAR completes within SLA; identity verification includes multi-factor challenge |
| 15 | Cookie/tracker consent banner compliant: no pre-checked boxes, reject-all equals accept-all in clicks, consent logged with proof | 🟢 Low | Banner tested across supported browsers; consent log includes timestamp + banner version |
| 16 | Employee privacy training completed annually with role-specific modules (engineering vs. marketing vs. HR) | 🟢 Low | Training completion tracked; phishing/privacy simulation pass rate ≥ 90% |
| 17 | Data Protection Officer (DPO) or EU Representative appointed where required (Art 37) and contact published in privacy notice | 🟢 Low | DPO contact verified in privacy notice; DPO independence confirmed (no conflict of interest) |

## Scale Depth

<!-- STANDARD: 2min -->

#### Solo Developer
- **Privacy**: Data minimization as default — store only what's essential; no analytics SDKs without consent
- **Minimum**: Privacy notice generator (TermsFeed/privacypolicies.com or similar), cookie consent banner, DSAR email process, DPIA template for high-risk processing
- **Add**: Automated backup with encryption-at-rest, deletion endpoint, consent log (event-sourced)
- **Cost**: ~$0-50/mo (open-source privacy tools, free-tier GDPR generators)
- **Coverage**: GDPR/CCPA basics — sufficient for indie apps with < 1,000 EU users

#### Small Team (2-10)
- **Privacy**: Dedicated privacy owner (not necessarily a DPO) with part-time responsibility
- **Minimum**: Data catalog (spreadsheet → automated crawler as team grows), automated DSAR pipeline, SCCs for any vendor data sharing, ROPA
- **Add**: Automated retention TTL, DPIA review cycle (trigger on feature changes), breach notification drill
- **Cost**: ~$200-500/mo (privacy platform like Osano/Ketch starting tier or privacy engineer part-time)
- **Risk**: Manual DSAR handling breaks at > 5 requests/month; automate before marketing campaigns

#### Medium Org (10-100)
- **Priority**: Hire or designate a qualified DPO — this is not a side responsibility at this scale
- **Minimum**: Full privacy platform (OneTrust, TrustArc, Ketch), automated data catalog with discovery, event-sourced consent management, automated DSAR portal with ID verification
- **Add**: Differential privacy budget manager for analytics, automated TIA refresh, privacy review gate in CI/CD
- **Cost**: ~$2,000-8,000/mo (enterprise privacy platform + dedicated privacy team)
- **Coverage**: GDPR, CCPA, LGPD, PIPEDA — multi-jurisdiction compliance with regulatory monitoring

#### Enterprise (100+)
- **Organization**: Dedicated privacy engineering team alongside legal privacy office; privacy embedded in every engineering squad
- **Minimum**: Privacy-by-design architecture review board, automated privacy impact scoring at commit time, federated data catalog across all business units, privacy-preserving analytics (DP + k-anonymity + l-diversity)
- **Add**: PETs (Privacy-Enhancing Technologies) program — homomorphic encryption pilots, secure multi-party computation for partner data sharing, synthetic data generation for testing
- **Cost**: $20,000-50,000+/mo (multi-vendor privacy stack + dedicated privacy engineering team of 3-8)
- **Focus**: Regulatory strategy and advocacy — shape emerging privacy regulation (EU AI Act privacy provisions, state-level US privacy laws, adequacy decisions)

## Error Decoder

<!-- QUICK: 30s -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| DSAR returns user name and email only — analytics, CDN, and log data are completely missing | Data inventory was never built; DSAR pipeline queries only the primary database | Build data catalog first: register all data stores with category tags and query APIs. DSAR pipeline queries catalog, not specific databases | DSAR = data catalog problem, not a database problem. 40-60% of user data lives outside the primary database |
| Breach notification filed at T+96 and regulator issues separate fine for late notification | Legal waited for forensics confirmation before starting the 72-hour clock — "suspicion" wasn't "confirmed" | Start notification clock at first reasonable suspicion. File initial notification within 72 hours with what's known. Follow up with updated notification as investigation progresses | GDPR Article 33 clock starts at awareness, not confirmed root cause. Late notification is a separate violation (up to 2% global turnover) |
| Consent proof rejected by regulator — `consented = true` boolean has no audit trail | Boolean consent flag has no proof of what was shown to the user, when they consented, or what action they took | Implement event-sourced consent: store consent record with (notice_version_hash, timestamp, affirmative_action, purpose_list, withdrawal_url). Regulator can replay: load notice version → verify consent timestamp → confirm scope | Consent is provable only when the notice content, version, and affirmative action are all verifiable |
| SCCs signed but supplementary measures never implemented — surveillance law conflict unaddressed | Transfer Impact Assessment was treated as a checklist item rather than a technical evaluation | For each data flow to a surveillance-law jurisdiction: implement CMK encryption with keys held outside recipient country, pseudonymize before transfer, or split processing to limit exposure. Document why each measure is sufficient | SCCs are a legal framework, not a technical control. Post-Schrems II, TIAs and supplementary measures are the actual compliance requirement |
| Soft-delete implemented but backup restoration re-creates "deleted" user 6 months later | Deletion pipeline has phases 1+2 (soft + hard delete) but no phase 3 (backup exclusion registry) | Implement deletion registry: every hard-deleted user's identifier is recorded. Backup restore scripts query deletion registry and skip deleted users. Test by restoring a backup that predates deletion | GDPR Article 17 requires irreversible destruction. Without backup exclusion, soft-delete is a visibility filter |
| ε=10 privacy budget consumed in first 3 days of month by naive dashboard queries | Each dashboard query at ε=1, no cumulative tracking — 10 charts = ε=10, effectively zero privacy | Implement privacy budget manager: track cumulative ε per dataset per time window, reject queries exceeding budget, provide pre-computed differentially-private aggregates for common queries | ε composes additively. Without budget tracking, "differentially private" analytics are unprotected |
| Cookie consent banner with pre-checked "Accept All" — regulator fines €50M under ePrivacy Directive | Banner design optimized for acceptance rate, not compliance; dark pattern forces consent | Implement equal-choice banner: reject-all and accept-all are same number of clicks, no pre-checked boxes (except essential cookies), no "legitimate interest" override for marketing, consent logged with proof | ePrivacy + GDPR Article 7: consent must be freely given, specific, informed, and unambiguous. Pre-checked = not freely given |

## References

*   [ICO: Guide to Data Protection Impact Assessments](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-impact-assessments/) — UK ICO DPIA guidance with examples and templates
*   [EDPB Guidelines 4/2019 on Data Protection by Design and by Default](https://edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-42019-article-25-data-protection-design-and_en) — Article 25 PbD obligations
*   [European Commission: Standard Contractual Clauses](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en) — SCCs 2021 modules and implementation guidance
*   [NIST Privacy Framework](https://www.nist.gov/privacy-framework) — Enterprise privacy risk management aligned with NIST CSF
*   [Differential Privacy by Cynthia Dwork and Aaron Roth](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf) — Foundational text on DP algorithms and composition
*   [/references/privacy-by-design-principles.md](references/privacy-by-design-principles.md) — Cavoukian's 7 principles mapped to system architecture
*   [/references/dpia-methodology.md](references/dpia-methodology.md) — Full DPIA template with risk scoring and mitigation tracking
*   [/references/differential-privacy.md](references/differential-privacy.md) — Epsilon selection, Laplace/Gaussian mechanisms, budget accounting
*   [/references/consent-management.md](references/consent-management.md) — Event-sourced consent architecture with proof chain implementation
*   [/references/right-to-access-deletion.md](references/right-to-access-deletion.md) — SAR and RTBF implementation patterns, deletion cascade
*   [/references/cross-border-transfers.md](references/cross-border-transfers.md) — SCC module selection, TIA methodology, supplementary measures
*   [/references/privacy-preserving-tech.md](references/privacy-preserving-tech.md) — HE, SMPC, ZKP, FL decision framework and readiness assessment
*   [/references/data-retention-automation.md](references/data-retention-automation.md) — TTL-based deletion, retention schedule templates, audit trail
*   [/scripts/verify-skill.sh](scripts/verify-skill.sh) — Verify all 14 required sections, ground rules, decision trees, gotchas, and references
