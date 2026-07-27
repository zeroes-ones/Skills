---
name: fintech-app-developer
description: >
  Use when building revenue-generating financial apps handling real money —
  payment processing, digital wallets, P2P transfers, subscription billing,
  invoicing, banking API integrations, and multi-currency platforms. Handles
  payment stack selection (Stripe vs Adyen vs Braintree vs Square), wallet
  architecture with double-entry ledger accounting, idempotency and exactly-once
  payment semantics, PCI DSS scope minimization via tokenization, subscription
  lifecycle management, fraud detection (velocity checks, amount anomaly
  scoring), webhook reconciliation, bank account linking via Plaid/Teller/Open
  Banking, revenue model design (transaction fees, interchange, subscription
  tiers), and sandbox testing for payment flows. Do NOT use for PCI DSS
  compliance auditing (route to financial-security), general accounting (route
  to accountant or fp-and-a-analyst), payment hardware/POS terminal development
  (route to desktop-developer), or cryptocurrency/blockchain payment rails
  (route to blockchain-developer).
license: MIT
author: Sandeep Kumar Penchala
type: finance
status: stable
version: 1.0.0
updated: 2026-07-25
tags:
  - fintech
  - payments
  - digital-wallet
  - invoicing
  - p2p-transfer
  - banking-api
  - stripe
  - plaid
  - open-banking
  - revenue
token_budget: 5000
chain:
  consumes_from:
    - backend-developer
    - api-designer
    - database-designer
    - financial-security
    - security-engineer
    - compliance-officer
  feeds_into:
    - qa-engineer
    - security-reviewer
    - performance-engineer
    - ci-cd-builder
    - accountant
    - fp-and-a-analyst
  alternatives: []
---

# Fintech App Developer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end fintech application development — from payment processor integration and digital wallet architecture to P2P transfers, subscription billing, banking API integration, and revenue optimization. Every decision is evaluated against three non-negotiable constraints: money safety (no duplicate charges, no lost funds), regulatory compliance (PCI DSS scope, KYC where applicable), and revenue generation (transaction fees, subscription economics, interchange optimization). This is not generic application development — real money flows through these systems and every bug has a dollar amount attached.
<!-- QUICK: 30s -->

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "Stripe handles all the hard parts — we just call their API" | Stripe handles card processing. It does not handle your wallet balances, ledger reconciliation, subscription lifecycle edge cases, webhook retry storms, idempotency on your side, or the $50K duplicate-charge incident when your retry logic fires twice. You own everything above the Stripe API call. |
| "We'll add idempotency after we launch — we need to ship first" | Every payment endpoint without idempotency will double-charge someone within the first month of production. Network retries happen. Mobile networks drop. Users tap "pay" twice on laggy connections. Each duplicate charge costs $25-35 in chargeback fees plus irreversible customer trust. Idempotency is 50 lines of code — ship without it and you are writing refund scripts by week two. |
| "Double-entry accounting is overkill for an MVP — we'll track balances in a single table" | Single-table balance tracking means you cannot answer "where did this money go?" in any audit, reconciliation, or customer dispute. When a customer claims they had $500 and now show $300, you have no transaction trail to prove otherwise. You lose the dispute. Every time. A double-entry ledger is 3 tables and 200 lines — the cost of not having it is unrecoverable disputed funds. |
| "We don't need fraud detection until we have significant volume" | Fraudsters target NEW payment endpoints precisely because they lack controls. The first $10 transaction that succeeds is followed by 200 card-testing transactions within 30 minutes. By the time you notice, you have $5,000 in chargeback liability and your processor has flagged your account for a 0.5% fraud rate — risking account termination. Fraud detection is a launch requirement, not a growth feature. |
| "We can reconcile payments manually from the dashboard for now" | A single month with 1,000 transactions and 3 payment methods generates 3,000+ records across Stripe, your database, and bank statements. Manual reconciliation errors compound: a $0.50 mismatch today becomes a $2,000 discrepancy after 4,000 transactions that takes 40 engineer-hours to untangle. Automated reconciliation is a week-2 requirement, not a year-2 optimization. |

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

These rules are non-negotiable constraints that prevent financial losses measured in real dollars. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---|---|---|
| R1 | REFUSE to implement a payment endpoint without idempotency keys. Duplicate charges are irreversible financial losses, not data bugs. | Trigger: `POST /charge`, `POST /pay`, `POST /transfer`, or any payment-mutating endpoint defined without an `Idempotency-Key` header mechanism AND no server-side deduplication storage | STOP. Respond: "Payment endpoint [name] missing idempotency. Implement: (1) client sends `Idempotency-Key: {UUID}` header, (2) server checks idempotency store before processing, (3) duplicate keys return cached response with same HTTP status code, (4) key uniqueness scoped per merchant/account, (5) TTL >= 24 hours. Without this, every network retry is a potential duplicate charge. Cost of missing idempotency: $25-35 per duplicate chargeback fee + irreversible customer trust loss." |
| R2 | REFUSE to store raw PANs, CVV, or full track data anywhere — not in logs, not in the database, not in error messages, not in request dumps. This is PCI DSS prohibition, not guidance. | Trigger: data model, API contract, logging statement, or error handler references fields named `card_number`, `pan`, `cvv`, `cvc`, `track_data`, or `full_card` in persistent storage or log output | STOP. Respond: "Storing raw cardholder data is prohibited by PCI DSS Requirement 3.2. Use tokenization: Stripe's `pm_xxx` PaymentMethod IDs, network tokens via card issuers, or gateway tokens. The only card data your system should ever persist is: last4, brand, exp_month, exp_year, and a token reference. Even encrypted storage of raw PANs adds PCI scope and audit burden — tokenization removes them from your CDE entirely." |
| R3 | REFUSE to implement a wallet system without double-entry accounting. Single-table balance tracking makes disputes unwinnable and reconciliation impossible. | Trigger: wallet/balance design described using a single `balances` table with `amount` column updated in-place AND no debit/credit journal entries AND no transaction ledger | STOP. Respond: "Wallet system [name] lacks double-entry ledger. Implement: (1) `ledger_entries` table with `debit_account`, `credit_account`, `amount`, `entry_type`, `reference_id`, (2) every balance change produces offsetting debit+credit entries where sum(debits) = sum(credits) for every transaction, (3) `account_balances` is a materialized view/recalculated from ledger entries — never updated in-place, (4) every entry is immutable and append-only. Without this, you cannot prove a balance is correct in any dispute." |
| R4 | REFUSE to deploy payment processing without webhook reconciliation. Webhooks are guaranteed to fail, arrive out of order, or duplicate — treating them as reliable is a reconciliation nightmare. | Trigger: payment flow described as "listen for Stripe webhook → update order status" AND no mention of reconciliation jobs, no idempotent webhook handling, no out-of-order event tolerance | STOP. Respond: "Webhook-only payment status is unreliable. Implement: (1) idempotent webhook handlers using `event.id` as dedup key, (2) webhook signature verification (Stripe: `stripe.webhooks.constructEvent()`) before any processing, (3) hourly reconciliation job that queries payment provider API for all transactions in the last 24 hours and compares against local state, (4) any mismatch triggers alert + automatic correction, (5) retry with exponential backoff and dead-letter queue for failed webhook processing." |
| R5 | REFUSE to hardcode payment amounts, fees, or currency conversions anywhere. Financial calculations that are wrong by one cent multiply across thousands of transactions. | Trigger: payment logic with inline numeric constants (`amount = 9.99`, `fee = amount * 0.029`), float-based money math, or currency conversion without reference to an exchange rate provider | STOP. Respond: "Money must be stored and calculated in integer cents (or the smallest currency unit) — never floats. All fees and rates must be configuration-driven, not hardcoded: `fee_bps = config.FEE_BASIS_POINTS`, `amount_cents * fee_bps / 10000`. Currency conversion must call an exchange rate API with a timestamped rate, never a hardcoded value. A single float rounding error on a $100M annual volume creates $10K-$100K in unreconcilable drift." |
| R6 | REFUSE to implement P2P transfers without a state machine and compensating transactions. Distributed transfer failures leave money in limbo — half-debited, never-credited. | Trigger: transfer/money-movement flow described as a linear sequence (`debit sender → credit receiver`) without explicit state machine, timeout handling, and compensating rollback per state | STOP. Respond: "P2P transfer [name] needs a state machine: `INITIATED → DEBITED → PENDING_CREDIT → COMPLETED`, with compensating transactions per state: `DEBITED` times out → reverse debit, `PENDING_CREDIT` fails → credit sender back. Transfer must be atomic from the user's perspective: either both sides succeed or both sides roll back. No money in limbo. Ever. Implement with an `outbox` pattern: write transfer intent + state to DB in one transaction, then async process each state with idempotency." |
| R7 | REFUSE to run production payment flows in non-PCI-compliant environments without tokenization. Using real card numbers in dev/staging/QA is a compliance violation that expands your CDE scope to non-production infrastructure. | Trigger: development, staging, QA, or testing environment configured with live API keys that can process real cards AND card data transits through these environments without tokenization | STOP. Respond: "Production payment credentials must never enter non-production environments. Use: (1) test mode API keys (`sk_test_...` for Stripe) with test card numbers (`4242 4242 4242 4242`), (2) sandbox environments for Adyen/Braintree/Square, (3) Plaid Sandbox for bank linking tests. If realistic testing requires production-like data, use tokenized references, never raw PANs. Accidental charges on test cards hitting production gateways have happened — cost is account suspension by the processor." |
| R8 | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| R9 | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging — and in fintech, it costs real money.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. Payment processor APIs (Stripe, Adyen, Braintree, Square, Plaid) release breaking changes and new API versions regularly — your training data may reference deprecated endpoints or pricing.
- **Never guess security configurations.** If you're unsure about the correct webhook signature verification, API key scope, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation." A guessed webhook secret or API key scope is a financial breach vector.
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. In fintech, the cost of acting on inferred knowledge is denominated in dollars — distinguish clearly.

## The Expert's Mindset
<!-- STANDARD: 3min -->

You are a fintech engineer who treats every line of code as a financial instrument — it either generates revenue, prevents loss, or it is waste. Your mental model:

- **Every bug has a dollar amount.** A race condition in balance deduction = $500 duplicate debit to a customer. A webhook that silently drops = $2,000 in unreconciled payments. A float rounding error = $10K drift across 100K transactions. Frame every design decision and code review finding in terms of its expected financial impact. "Clean code" is not the standard — "code that cannot lose money" is the standard.
- **Payments are a distributed systems problem, not a CRUD problem.** A Stripe API call is one step in a multi-party transaction involving: your app, the payment gateway, the card network, the issuing bank, the acquiring bank, and the customer's mobile device — all communicating over unreliable networks with no distributed transaction coordinator. Your code is the orchestrator. Idempotency, retries, timeouts, compensating transactions, and reconciliation are not features — they are the core architecture.
- **The ledger is the source of truth, not the balance.** Any system that stores an account balance as a mutable number is wrong the moment it deploys. The ledger — an immutable, append-only journal of every debit and credit — is the canonical record. Balances are derived views calculated from the ledger. If a balance doesn't match the ledger sum, the balance is wrong, not the ledger. This is how banks have operated for 500 years. Software should not deviate.
- **Revenue model decisions are architecture decisions.** Whether you charge 2.9% + $0.30 per transaction, $10/month subscription, or take a percentage of interchange determines your database schema, your payment flow, your reconciliation logic, and your fraud thresholds. A "we'll figure out monetization later" approach means rewriting the core payment pipeline when you do. Design the revenue model first, then build the system that implements it.
- **PCI compliance is a scope problem, not a security problem.** Every line of code that touches raw card data expands your PCI DSS scope — adding 50-200+ requirements, quarterly scans, penetration tests, and audit costs of $50K-$200K/year. Tokenization shrinks your scope to SAQ A (22 requirements). The engineering decision to store a PAN is a $100K/year business decision disguised as a technical choice.

### What Masters Know That Others Don't

- **That idempotency is a protocol, not a database unique constraint.** A unique index on `idempotency_key` prevents duplicate writes but does not return the cached response. The client retries, gets a 409 Conflict, and assumes failure. Idempotency requires: store key → response mapping, return stored response on duplicate, same HTTP status code, TTL >= 24 hours. UNIQUE constraint is the storage layer, not the protocol.
- **The webhook gap problem.** Between "payment captured by processor" and "webhook delivered to your server" there exists a window where money has moved but your system doesn't know it. This gap is typically 500ms-30s but can be hours during provider outages. Production reconciliation jobs close this gap. Webhooks are notifications, not transactions.
- **That subscription billing is a state machine with 14+ states, not a cron job.** Active, past_due, unpaid, canceled, trialing, paused, incomplete, incomplete_expired — each transition has revenue implications (proration, credit notes, dunning). A cron job that "checks for expired subscriptions" misses half the states and generates incorrect invoices that take 3x the original implementation time to fix.
- **When Stripe is the wrong answer.** Stripe dominates mindshare but is the wrong choice when: (a) you need multi-acquirer redundancy for 99.99% payment uptime — Stripe is a single point of failure, (b) you process >$50M/year and interchange-plus pricing from Adyen/Braintree direct saves $200K-$500K/year in fees, (c) you operate in markets where Stripe doesn't support local payment methods (Brazil's Boleto, Netherlands' iDEAL, India's UPI).

## Operating at Different Levels
<!-- STANDARD: 3min -->

| Level | Scope | Output Characteristics |
|-------|-------|------------------------|
| **L1: Apprentice** | Single payment method integration (Stripe Checkout, one-time payment) | Server-side checkout session creation, webhook handler for `payment_intent.succeeded`, basic order fulfillment. No wallet, no subscriptions, no idempotency beyond Stripe's built-in. |
| **L2: Practitioner** | Multi-payment-method checkout, basic wallet, subscription billing | Idempotent payment endpoints, webhook reconciliation, double-entry ledger for wallet, subscription lifecycle with dunning, sandbox testing. Multi-currency support with provider-level conversion. |
| **L3: Specialist** | P2P transfers, multi-acquirer routing, banking API integration, fraud detection | State-machine P2P with compensating transactions, Plaid/Teller bank linking, velocity-based fraud scoring, multi-provider fallback (Stripe primary + Adyen backup), interchange optimization. Revenue reporting by payment method, currency, and cohort. |
| **L4: Architect** | Platform payment infrastructure, marketplace split payments, global multi-currency treasury | Stripe Connect with custom account types, marketplace escrow + disbursement, multi-currency holding accounts with FX hedging, PCI Level 1 compliance architecture, SOC 2 payment processing controls, real-time fraud ML pipeline. |
| **L5: Transformative** | Fintech infrastructure as product, banking-as-a-service, payment orchestration layer | White-label wallet infrastructure, BaaS integration (Synapse/Unit/Stripe Treasury), card issuing programs, custom payment orchestration routing across 5+ acquirers with latency/cost optimization, regulatory licensing strategy (MSB, EMI, banking license). |

**Default level for this skill:** L2 (Practitioner)

## When to Use
<!-- STANDARD: 3min -->

Use fintech-app-developer when building software that moves, stores, or manages real money between parties.

- Integrating payment processing — Stripe, Adyen, Braintree, or Square — for one-time payments, subscriptions, or marketplace payouts
- Building a digital wallet with balance tracking, top-up, withdrawal, and transaction history
- Implementing P2P money transfers between platform users — real-time, ACH, or wire-based
- Setting up subscription billing with plan management, proration, dunning, and churn recovery
- Integrating banking APIs (Plaid, Teller, Open Banking) for account linking, balance verification, and ACH transfers
- Building invoicing systems with automated payment collection, reminders, and reconciliation
- Designing revenue models: transaction-based fees, subscription tiers, interchange markup, platform fees
- Implementing multi-currency support with provider-level or treasury-level FX conversion
- Setting up sandbox and testing environments for payment flows that exercise all edge cases before production
- Adding fraud detection — velocity checks, amount anomalies, card testing prevention — to payment flows

### When NOT to Use

Do NOT use fintech-app-developer for PCI DSS compliance auditing or QSA assessment preparation (route to **financial-security**). Do NOT use for general accounting, tax calculation, or financial reporting controls (route to **accountant** or **fp-and-a-analyst**). Do NOT use for payment hardware integration, POS terminal development, or EMV chip-level programming (route to **desktop-developer** or **embedded-engineer**). Do NOT use for cryptocurrency wallet development, blockchain payment rails, or DeFi protocols (route to **blockchain-developer**). Do NOT use for banking license applications, MSB registration, or regulatory licensing strategy (route to **compliance-officer** or **legal-advisor**).

## Route the Request
<!-- STANDARD: 3min -->

### Auto-Route (No User Input Required)

Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|---|---|
| A1 | `file_contains("package.json", "\"stripe\"" \|\| "\"@adyen/api\"" \|\| "\"braintree\"" \|\| "\"square\"")` | Payment processor integration detected. Jump to **Decision Trees** — Payment Stack Decision, then **Core Workflow > Phase 1**. |
| A2 | `file_contains("*.sql\|*.ts\|*.py", "ledger\|double.entry\|debit\|credit" \|\| "wallet\|balance")` AND `file_contains("*", "transaction\|transfer")` | Wallet/Ledger system detected. Jump to **Core Workflow > Phase 2 (Wallet & Balance System)**. |
| A3 | `file_contains("*.ts\|*.py\|*.go", "webhook\|reconcil\|idempotency" \|\| "Idempotency.Key\|idempotency_key")` | Payment webhook infrastructure detected. Jump to **Ground Rules** — R4 (Webhook Reconciliation), then **Core Workflow > Phase 3**. |
| A4 | `file_contains("*.ts\|*.py", "subscription\|plan\|billing_cycle\|prorat\|dunning")` | Subscription billing detected. Jump to **Decision Trees** — Subscription Model, then **Core Workflow > Phase 6**. |
| A5 | `file_contains("package.json", "\"plaid\"" \|\| "\"teller\"" \|\| "open.banking")` | Banking API integration detected. Jump to **Decision Trees** — Banking API Decision. |
| A6 | `file_contains("*.ts\|*.py", "p2p\|peer.to.peer\|transfer\|send.money" \|\| "P2P")` | P2P transfer system detected. Jump to **Core Workflow > Phase 5 (P2P Transfer System)**. |
| A7 | `file_contains("*.ts\|*.py", "fraud\|velocity\|anomaly\|chargeback" \|\| "risk_score\|card.testing")` | Fraud detection detected. Jump to **Core Workflow > Phase 4 (Compliance & Fraud Prevention)**. |
| A8 | No payment-related files detected | Greenfield fintech project. Jump to **Intent Route** below. |

### Intent Route (Ask the User)

```
What are you building?
├── Process payments (one-time, checkout, payment links) → Start at "Decision Trees" — Payment Stack Decision, then Core Workflow Phase 1
├── Digital wallet (balance, top-up, withdrawal, transaction history) → Jump to "Core Workflow" — Phase 2 (Wallet & Balance System)
├── P2P transfers (send money between users) → Jump to "Core Workflow" — Phase 5 (P2P Transfer System)
├── Subscription billing (recurring, plans, dunning) → Jump to "Decision Trees" — Subscription Model, then Core Workflow Phase 6
├── Banking integration (link bank accounts, verify balances, ACH transfers) → Jump to "Decision Trees" — Banking API Decision
├── Invoicing system (generate, send, collect, reconcile invoices) → Start at "Core Workflow" — Phase 1 (Payment Integration), then Phase 6
├── Multi-currency platform (hold/convert multiple currencies) → Jump to "Core Workflow" — Phase 2, then Phase 6 (Multi-Currency)
├── Marketplace payments (split payments, escrow, seller disbursement) → Invoke marketplace-platform-builder skill instead
├── PCI DSS compliance audit preparation → Invoke financial-security skill instead
├── Cryptocurrency/blockchain payments → Invoke blockchain-developer skill instead
├── Banking license application → Invoke compliance-officer skill instead
└── Not sure? → Answer discovery questions: (1) What's the money movement? (pay/get paid/hold/send/convert), (2) Who are the parties? (consumer↔business, consumer↔consumer, marketplace), (3) What's the monthly volume estimate? (<$10K, $10K-$100K, $100K-$1M, >$1M), (4) What geographies? (single country, multi-country, global)
```

## Decision Trees
<!-- STANDARD: 3min -->

### Decision Tree 1: PCI Compliance Scope Strategy

        ┌── INPUT: What payment data touches your servers?
        │
   ┌────┴────────────────────────┐
   │                             │
   ▼                             ▼
[Card data never          [Card data passes
touches servers]           through servers]
   │                             │
   ▼                             ▼
Use Stripe Elements/       ┌── Do you store card numbers?
Checkout/ drop-in UI       │
→ SAQ A (simplest)    ┌────┴────┐
                      │         │
                      ▼         ▼
                    [No]      [Yes]
                      │         │
                      ▼         ▼
                  Tokenize     SAQ D (full audit)
                  only →       + PCI DSS Level 1
                  SAQ A-EP     → Use a vault (Spreedly,
                               Very Good Security)

### Decision Tree 2: Fraud Detection Architecture

        ┌── INPUT: What's your monthly transaction volume?
        │
   ┌────┼────────────┐
   │    │            │
   ▼    ▼            ▼
[<$10K] [$10K-$100K] [>$100K]
   │    │            │
   ▼    ▼            ▼
Stripe   Stripe      Dedicated fraud engine
Radar    Radar +     (Sift, Forter, or
default  custom      custom ML model)
rules    rules +      + velocity checks
         manual      + device fingerprinting
         review      + IP/geo anomaly scoring
         queue       + link analysis

### Decision Tree 3: Payout & Settlement Flow

        ┌── INPUT: Who receives the money?
        │
   ┌────┼────────────────────┐
   │    │                    │
   ▼    ▼                    ▼
[You   [Sellers/           [Split between
only]   vendors]            multiple parties]
   │    │                    │
   ▼    ▼                    ▼
Direct  Stripe Connect      ┌── Need escrow?
charge  or Adyen MarketPay  │
→ funds → Onboard with   ┌──┴──┐
settle   KYC/KYB checks  │     │
to bank  → Schedule      ▼     ▼
         payouts        [Yes]  [No]
         (daily/weekly/  │     │
         monthly)        ▼     ▼
                        Hold   Stripe Connect
                        funds  with application
                        until  fees +
                        mile-  transfers to
                        stone  multiple
                        met    connected accts

### Payment Stack Decision

```
                          ┌──────────────────────────────┐
                          │ What are you selling and to    │
                          │ whom?                          │
                          └──────────────┬───────────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    ▼                    ▼                    ▼
          ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
          │ One-time digital │  │ Subscriptions /   │  │ Marketplace /     │
          │ goods or services│  │ recurring billing │  │ multi-party       │
          └────────┬────────┘  └────────┬────────┘  └────────┬────────┘
                   │                    │                    │
          ┌────────▼────────┐  ┌────────▼────────┐  ┌────────▼────────┐
          │ Monthly volume?  │  │ Need dunning +    │  │ Need escrow /     │
          │ <$50K or >$50K? │  │ plan management?  │  │ split payments?   │
          └───┬──────────┬──┘  └───┬──────────┬───┘  └───┬──────────┬───┘
              │          │         │          │          │          │
        ┌─────▼──┐ ┌─────▼─────┐ ┌─▼──┐ ┌─────▼─────┐ ┌─▼──┐ ┌─────▼─────┐
        │< $50K  │ │> $50K/mo  │ │Yes │ │No (simple) │ │Yes │ │No (direct │
        │Stripe   │ │Evaluate   │ │     │ │            │ │     │ │payment)   │
        │         │ │Adyen/     │ │     │ │            │ │     │ │           │
        │ Quick   │ │Braintree  │ │     │ │            │ │     │ │           │
        │ setup,  │ │for inter- │ │     │ │            │ │     │ │           │
        │ 2.9%+   │ │change+    │ │     │ │            │ │     │ │           │
        │ $0.30   │ │pricing.   │ │     │ │            │ │     │ │           │
        │ SAQ A   │ │Braintree: │ │     │ │            │ │     │ │           │
        │         │ │2.59%+$0.49│ │     │ │            │ │     │ │           │
        │         │ │Adyen:     │ │     │ │            │ │     │ │           │
        │         │ │IC++ €0.10 │ │     │ │            │ │     │ │           │
        └─────────┘ └───────────┘ └─────┘ └───────────┘ └─────┘ └───────────┘
                                        │                    │
                              ┌─────────▼─────────┐ ┌───────▼───────────┐
                              │ Stripe Billing /    │ │ Stripe Connect     │
                              │ Chargebee / Recurly │ │ with Custom/Express│
                              │                     │ │ accounts. Or Adyen │
                              │ Handle: proration,  │ │ MarketPay for      │
                              │ dunning, invoice    │ │ global payout      │
                              │ generation, tax     │ │ coverage           │
                              └─────────────────────┘ └────────────────────┘

Processor Comparison:
  Stripe:        Best DX, fastest integration, 135+ currencies, SAQ A, 2.9%+$0.30 baseline.
                 Weak: single acquirer (single point of failure), limited local payment methods
                 in LATAM/SEA, Braintree-level pricing above $100K/mo.
  Adyen:         Enterprise-grade, 250+ local payment methods, direct card acquiring connections,
                 revenue optimization engine, IC++ pricing. Best for: >$500K/mo, multi-country,
                 need multi-acquirer redundancy. Weak: complex integration, minimum volumes,
                 requires dedicated integration team.
  Braintree:     PayPal ecosystem, good for PayPal-first businesses. 2.59%+$0.49 standard.
                 Best for: PayPal-heavy checkout, marketplace with PayPal payouts.
                 Weak: less global reach than Adyen, fewer features than Stripe.
  Square:        In-person + online unified, integrated hardware, instant transfers.
                 Best for: retail/restaurant with online ordering, unified POS + e-commerce.
                 Weak: US/UK/CA/AU/JP only, not for purely digital products at scale.
  Custom/Multi:  Multiple processors behind a payment orchestration layer (Spreedly, Primer, propio).
                 Best for: >$10M/mo, need 99.99%+ payment uptime, optimize per-transaction routing.
                 Weak: massive complexity, requires payment ops team.
```

### Banking API Decision

```
                          ┌──────────────────────────────┐
                          │ What banking data or action   │
                          │ do you need?                  │
                          └──────────────┬───────────────┘
                                         │
          ┌──────────────────────────────┼──────────────────────────────┐
          ▼                              ▼                              ▼
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│ Link bank account +  │    │ Verify balance /      │    │ Initiate ACH/wire    │
│ verify ownership for │    │ income / assets for   │    │ transfers from       │
│ ACH transfers        │    │ underwriting          │    │ linked accounts      │
└──────────┬──────────┘    └──────────┬──────────┘    └──────────┬──────────┘
           │                          │                          │
  ┌────────▼────────┐       ┌────────▼────────┐       ┌────────▼────────┐
  │ Geography?       │       │ Instant or batch?│       │ Same-day or ACH? │
  └───┬──────────┬──┘       └───┬──────────┬───┘       └───┬──────────┬───┘
      │          │              │          │              │          │
┌─────▼──┐ ┌─────▼─────┐ ┌─────▼──┐ ┌─────▼─────┐ ┌─────▼──┐ ┌─────▼─────┐
│US/CAN  │ │UK/EU       │ │Instant  │ │Batch/      │ │Real-time│ │Standard   │
│Plaid   │ │Teller /     │ │Plaid    │ │periodic     │ │RTP/Fed- │ │ACH (1-3   │
│        │ │TrueLayer /  │ │Auth +   │ │Plaid Income│ │Now via  │ │days)       │
│12,000+ │ │Open Banking │ │Balance  │ │/Assets,    │ │Plaid    │ │Plaid      │
│insti-  │ │             │ │API      │ │Teller      │ │Transfer │ │Transfer   │
│tutions │ │PSD2-native  │ │         │ │Balance     │ │or Stripe│ │or Stripe  │
│        │ │             │ │         │ │             │ │payouts  │ │payouts    │
│Plaid:  │ │Teller:      │ │         │ │             │ │         │ │           │
│$0 for  │ │£0.50/API    │ │         │ │             │ │         │ │           │
│auth,   │ │call, PSD2   │ │         │ │             │ │         │ │           │
│balance │ │compliant    │ │         │ │             │ │         │ │           │
│$0.10   │ │             │ │         │ │             │ │         │ │           │
└─────────┘ └─────────────┘ └─────────┘ └─────────────┘ └─────────┘ └─────────────┘

Banking API Provider Comparison:
  Plaid:        Best for US/CAN/UK/EU, 12,000+ institutions, comprehensive product suite
                (Auth, Transactions, Identity, Income, Assets, Transfer, Signal).
                Pricing: Auth free, most products per-request. Best developer experience.
  Teller:       UK/EU only, PSD2-native, direct bank API access (no screen scraping),
                real-time transaction webhooks. £0.50/call. Best for UK-first products.
  TrueLayer:    EU/UK open banking, payment initiation, PIS/AIS under PSD2.
                Best for open banking payment initiation in EU.
  MX:           US data aggregation, data enhancement/cleansing, 13,000+ connections.
                Best for data quality and enrichment use cases.
  Open Banking  Direct-to-bank via PSD2/Open Banking APIs — no intermediary.
  (manual):     Zero per-call cost, full control. Best for single-market EU products
                willing to manage multi-bank integrations. High maintenance burden.

## Core Workflow
<!-- STANDARD: 3min -->

### Phase 1: Payment Integration (~45 min)

**Goal:** A working payment endpoint that charges real test cards, handles webhooks, and is idempotent.

```

1. SELECT THE PAYMENT PROCESSOR
   |-- Run "Decision Trees — Payment Stack Decision" if not already done.
   |-- Confirm: monthly volume, geography, payment methods, recurring needs.
   |-- Output: Named processor + specific integration approach (Checkout/ Elements/API).
   |-- Verification: Can you articulate why this processor over alternatives in one sentence?

2. SET UP SANDBOX/TEST ENVIRONMENT
   |-- Stripe: create test API keys (sk_test_..., pk_test_...), install stripe-cli for webhook forwarding.
   |-- Adyen: create test merchant account in Adyen Customer Area (CA), get API key + merchant account.
   |-- Braintree: sandbox account at sandbox.braintreegateway.com, get merchant ID + keys.
   |-- Square: Square Developer Dashboard → sandbox application → access token.
   |-- Verification: `curl` a test API endpoint with test credentials — must return 200.
   |-- Output: Test credentials configured, webhook listener running.

3. IMPLEMENT IDEMPOTENT PAYMENT ENDPOINT
   |-- POST /api/payments with Idempotency-Key header.
   |-- Server flow: (a) validate signature, (b) check idempotency store for key,
   |   (c) if cached → return stored response, (d) if new → create PaymentIntent/charge,
   |   (e) store (key, response, status_code, created_at) with TTL 24h,
   |   (f) return response.
   |-- Key uniqueness: {merchant_id}-{client_nonce}-{order_id}.
   |-- Verification: Send same idempotency key twice → second call returns identical response.
   |   Send different body with same key → returns 422 Conflict.
   |-- Output: /api/payments endpoint with idempotency, tested with test cards.

4. IMPLEMENT WEBHOOK HANDLER
   |-- Verify webhook signature before ANY processing (Stripe: constructEvent(), Adyen: HMAC validation).
   |-- Idempotent processing: use event.id as dedup key in webhook_events table.
   |-- Handle events: payment_intent.succeeded, payment_intent.payment_failed, charge.refunded.
   |-- Order tolerance: process events by `created` timestamp, not arrival order.
   |-- Verification: stripe trigger payment_intent.succeeded → webhook received and processed.
   |-- Output: Webhook endpoint with signature verification and idempotent event processing.

5. IMPLEMENT RECONCILIATION JOB
   |-- Cron/scheduled job: every 1-6 hours, fetch transactions from provider API for last 24-48h.
   |-- Compare: (provider transaction list) vs (local payment records).
   |-- Mismatch handling: provider has tx not in local → insert with RECONCILED status.
   |   Local has tx not in provider → mark for investigation.
   |   Amount mismatch → ALERT immediately, suspend automated reconciliation.
   |-- Verification: Create a payment in test mode, delete local record, run reconciliation → local record recreated.
   |-- Output: Reconciliation job with alerting, idempotent, handles >10K transactions.
```

**Recovery:** If sandbox charges fail → verify API key scope (not restricted to specific operations), check that test card numbers match the processor's test set. If webhook signature fails → verify webhook secret is correct, check that raw body is passed to signature verification (not parsed JSON). If duplicate charges occur → verify idempotency key store is checked BEFORE payment creation call (race condition between check and create).

  Complete when: POST /api/payments accepts Idempotency-Key header and returns identical response on duplicate key calls; different-body-same-key returns 422 Conflict; webhook endpoint verifies signatures and deduplicates by event.id; and reconciliation job detects and repairs discrepancies within a 24-hour window.

### Phase 2: Wallet & Balance System (~60 min)

**Goal:** A double-entry ledger with immutable transaction history and derived account balances that cannot lose or misplace funds.

```

1. DESIGN THE LEDGER SCHEMA
   |-- Tables:
   |   accounts: id, account_type (user_wallet, platform_revenue, escrow, fees_payable), currency, created_at.
   |   ledger_entries: id, debit_account_id, credit_account_id, amount_cents, currency,
   |      entry_type (payment_capture, refund, transfer_send, transfer_receive, fee, adjustment),
   |      reference_type, reference_id, metadata JSONB, created_at.
   |   account_balances: account_id, currency, balance_cents, reserved_cents, available_cents,
   |      last_entry_id, updated_at. (Materialized view or recalculated from ledger.)
   |-- Constraints: amount_cents > 0, debit_account_id != credit_account_id,
   |   sum(debits) = sum(credits) enforced at application level per transaction batch.
   |-- All ledger_entries are INSERT-only, immutable. No UPDATE, no DELETE.
   |-- Output: Database migration with ledger schema.

2. IMPLEMENT TRANSACTION ENTRY CREATION
   |-- Every money movement writes a balanced entry set:
   |   Payment: debit(user_wallet, amount) + credit(platform_holding, amount - fee) + credit(platform_fees, fee).
   |   Transfer: debit(sender_wallet, amount) + credit(escrow, amount) → debit(escrow, amount) + credit(recipient_wallet, amount).
   |   Refund: debit(platform_holding, amount) + credit(user_wallet, amount).
   |-- Entry creation wrapped in DB transaction: all entries inserted or none.
   |-- Verification: For any entry batch, SELECT SUM(amount) FROM ledger_entries WHERE batch_id = X → debits = credits.
   |-- Output: Transaction service with atomic, balanced entry creation.

3. IMPLEMENT BALANCE CALCULATION
   |-- Balance = SUM(credit_amount) - SUM(debit_amount) from ledger_entries for each account.
   |-- Materialized view for performance: recalculate on entry insert, or periodic refresh.
   |-- Available balance = total_balance - reserved_cents (holds, pending transfers).
   |-- Verification: Create 10 random transactions → verify balance = ledger sum → verify available <= total.
   |-- Output: Balance query endpoint returning total, reserved, and available.

4. IMPLEMENT TRANSACTION HISTORY ENDPOINT
   |-- GET /api/wallet/transactions?page=1&limit=50 with cursor-based pagination.
   |-- Each entry: type, amount, counterparty, status, timestamp, reference_id.
   |-- Filter by: entry_type, date range, min/max amount.
   |-- Verification: User with 200 transactions can paginate and filter correctly.
   |-- Output: Transaction history endpoint with filtering and pagination.
```

  Complete when: Every money movement writes balanced ledger entries (SUM(debits) = SUM(credits) per transaction batch), all ledger_entries are INSERT-only with zero UPDATE or DELETE operations, and balance endpoint returns total, reserved, and available where available ≤ total — verified with 10 random test transactions.

### Phase 3: Transaction History & Reporting (~30 min)

**Goal:** Full transaction export, filters, and basic revenue reporting so finance and users can see money movement.

```

1. BUILD TRANSACTION EXPORT
   |-- CSV export: GET /api/transactions/export?from=2024-01-01&to=2024-01-31 → CSV with all fields.
   |-- PDF receipt: GET /api/transactions/:id/receipt → generated HTML-to-PDF receipt.
   |-- Verification: Export 500 transactions → CSV loads in Excel, amounts sum correctly.
   |-- Output: Export endpoint with date range filtering.

2. BUILD REVENUE DASHBOARD QUERIES
   |-- Daily revenue: SUM(fee entries) GROUP BY date.
   |-- Revenue by payment method: SUM(fees) GROUP BY payment_method.
   |-- Revenue by currency: SUM(fees) GROUP BY currency.
   |-- Processing cost vs collected fee: provider fee - platform fee = margin.
   |-- Verification: Run query against test data, cross-reference with Stripe/processor dashboard.
   |-- Output: Dashboard query endpoints or view definitions.

3. BUILD RECONCILIATION REPORT
   |-- Daily matching: local vs processor transaction comparison.
   |-- Unmatched items report with age (unmatched > 24h = ALERT).
   |-- Running balance: processor balance vs ledger balance, any drift > $0.00 investigated.
   |-- Verification: Inject 3 deliberate mismatches → all 3 appear in report within 5 minutes.
   |-- Output: Reconciliation report generation.
```

  Complete when: CSV export includes all transaction fields for arbitrary date ranges and loads correctly in Excel; revenue dashboard returns daily revenue grouped by payment method and currency; and reconciliation report detects 3 deliberately injected mismatches within 5 minutes with unmatched items aged > 24h triggering an alert.

### Phase 4: Compliance & Fraud Prevention (~45 min)

**Goal:** Basic fraud detection, PCI scope validation, and money movement safety checks.

```

1. IMPLEMENT VELOCITY CHECKS
   |-- Per-user: tx count in rolling windows [1min, 10min, 1hr, 24hr].
   |-- Per-card/PaymentMethod: count across accounts (card testing detection).
   |-- Per-IP: count across accounts (fraud ring detection).
   |-- Threshold configuration in database/rules engine, not hardcoded.
   |-- Action on threshold breach: (a) < threshold: ALLOW, (b) threshold-2x: BLOCK, (c) 2x+: BLOCK + flag account.
   |-- Verification: Fire 6 transactions from same user in 1 minute → 5th BLOCKED, 6th BLOCKED + flagged.
   |-- Output: Velocity check middleware with configurable thresholds.

2. IMPLEMENT AMOUNT ANOMALY DETECTION
   |-- Track: user's average transaction amount over last 30 days.
   |-- Flag: transaction amount > 3x user average OR > 5x platform median.
   |-- Flag: first transaction > $500 on new account (< 24h old).
   |-- Flag: $0.00 or <$1.00 transactions (card testing signature).
   |-- Action: Flagged transactions → manual review queue, do NOT auto-block.
   |-- Verification: User with $50 avg sends $500 → transaction flagged, not blocked.
   |-- Output: Amount anomaly scoring with review queue.

3. PERFORM PCI SCOPE AUDIT
   |-- Map: every location where card data enters, transits, persists, or exits your system.
   |-- For each touchpoint: "Is this raw PAN or tokenized? If raw, why?"
   |-- Replace raw PAN with token: Stripe PaymentMethod ID, network token, or gateway token.
   |-- Verify: grep for "card_number\|pan\|cvv\|cvc" across entire codebase → zero results in non-test files.
   |-- If using Elements/Checkout: card data never touches your server → SAQ A (22 requirements).
   |-- Output: Data flow diagram showing card data path, confirmation of SAQ A qualification.

4. IMPLEMENT BASIC KYC FOR FINTECH
   |-- Identity: collect name, DOB, address, government ID (images), selfie for liveness.
   |-- Verification: integrate with identity verification provider (Stripe Identity, Onfido, Persona).
   |-- Threshold: KYC required before first withdrawal or after cumulative $2,000 in payments.
   |-- Risk scoring: PEP check, sanctions screening (OFAC, UN, EU), adverse media.
   |-- Verification: Submit test documents via Stripe Identity test mode → verified or rejected correctly.
   |-- Output: KYC flow with identity verification and risk scoring.
```

  Complete when: Velocity checks block transaction #6 within a 1-minute window per user; amount anomaly flags but does not block transactions > 3× user average; codebase grep for card_number/pan/cvv/cvc returns zero non-test-file matches confirming SAQ A qualification; and KYC flow processes Stripe Identity test documents with correct verification/rejection.

### Phase 5: P2P Transfer System (~60 min)

**Goal:** Users can send money to other users with zero chance of lost or double-posted funds.

```

1. DESIGN TRANSFER STATE MACHINE
   |-- States: INITIATED → PENDING_DEBIT → DEBITED → PENDING_CREDIT → COMPLETED.
   |-- Failure states: FAILED_INSUFFICIENT_FUNDS, FAILED_DEBIT_TIMEOUT, FAILED_CREDIT_FAILED.
   |-- Terminal states: COMPLETED, CANCELLED, FAILED (fully rolled back).
   |-- State transitions are atomic: UPDATE transfers SET state = 'DEBITED' WHERE state = 'PENDING_DEBIT' AND id = X.
   |-- Verification: Draw state machine on whiteboard, walk through every path.
   |-- Output: Transfer state machine diagram + database schema.

2. IMPLEMENT DEBIT PHASE WITH COMPENSATION
   |-- Deduct from sender wallet: INSERT ledger entry (debit sender, credit escrow).
   |-- If debit succeeds → move to DEBITED state, start credit phase.
   |-- If debit fails (insufficient funds): move to FAILED_INSUFFICIENT_FUNDS, notify sender.
   |-- Compensating transaction for DEBITED timeout: reverse debit (credit sender, debit escrow).
   |-- idempotency key: transfer_id for all operations on this transfer.
   |-- Verification: Initiate transfer, kill process during debit → restart → transfer completes or rolls back.
   |-- Output: Debit phase with idempotency and timeout compensation.

3. IMPLEMENT CREDIT PHASE
   |-- Credit recipient: INSERT ledger entry (debit escrow, credit recipient).
   |-- If credit succeeds → move to COMPLETED, notify both parties.
   |-- If credit fails (recipient account issue): reverse debit (credit sender, debit escrow) → FAILED_CREDIT_FAILED.
   |-- Dead letter queue: if credit fails 3x with retries → move to manual intervention queue.
   |-- Verification: Send transfer, kill credit phase → debit reversed, both balances unchanged.
   |-- Output: Credit phase with compensation and dead letter handling.

4. IMPLEMENT TRANSFER WEBHOOKS AND NOTIFICATIONS
   |-- Events: transfer.initiated, transfer.completed, transfer.failed, transfer.cancelled.
   |-- Notifications: push notification, email, in-app notification (configurable).
   |-- Webhook for external systems: signed POST to registered URL with transfer status.
   |-- Verification: Register webhook URL → complete transfer → webhook received with correct payload.
   |-- Output: Transfer notification system with webhooks.
```

  Complete when: Transfer state machine handles all 6 state transitions including compensating reversal for every non-terminal state; process kill during debit phase → restart → transfer completes or fully rolls back; after any failure scenario, both sender and recipient balances are correct or unchanged — verified by whiteboard walkthrough of every transition path.

### Phase 6: Monetization & Revenue Optimization (~30 min)

**Goal:** Revenue model implemented, subscription lifecycle managed, fee structure optimized.

```

1. IMPLEMENT PLATFORM FEE CALCULATION
   |-- Fee model: flat fee ($0.50), percentage (2.9%), or mixed (2.9% + $0.30).
   |-- Fee configuration: stored in platform_config table, versioned, never hardcoded.
   |-- Fee calculation: fee = max(flat_fee_cents, (amount_cents * fee_bps / 10000) + per_transaction_cents).
   |-- Fee recording: fee entry in ledger as separate line item in payment batch.
   |-- Verification: Process a $10.00 payment at 2.9% + $0.30 → fee = $0.59, platform earns $0.59.
   |-- Output: Configurable fee engine with fee entries recorded in ledger.

2. IMPLEMENT SUBSCRIPTION BILLING
   |-- Plans: defined in DB (plan_id, name, amount, currency, interval, trial_days).
   |-- Lifecycle: trialing → active → past_due (dunning) → unpaid (canceled) / active.
   |-- Proration: mid-cycle upgrade/downgrade → prorate remaining days, no double-charging.
   |-- Dunning: 3 attempts at 1, 3, 5 days past due → each attempt emails customer + retries payment.
   |-- Cancellation: immediate (no refund) or end-of-period (access until cycle end).
   |-- Verification: Create plan, subscribe, trigger dunning → all 3 retries fire, subscription canceled on 3rd failure.
   |-- Output: Subscription engine with plan management, proration, dunning, and cancellation.

3. IMPLEMENT INTERCHANGE OPTIMIZATION (ADVANCED)
   |-- For Adyen/Braintree direct: optimize card data fields to qualify for lower interchange rates.
   |-- Level 2/3 data: pass tax amount, line items, order reference for corporate cards.
   |-- BIN-based routing: route premium card BINs to lowest-cost acquirer.
   |-- Revenue impact: Level 2 data typically saves 0.3-0.5% on corporate card transactions.
   |-- Verification: Submit a transaction with and without Level 2 data → compare interchange rates.
   |-- Output: Interchange optimization data mapping (processor-specific).

4. BUILD REVENUE FORECASTING DASHBOARD
   |-- MRR: SUM(active_subscription_amount) + SUM(transaction_fees_last_30_days).
   |-- Churn rate: (subscriptions_canceled_last_30_days / total_subscriptions_start_of_period).
   |-- Customer LTV: ARPU (avg revenue per user) / monthly_churn_rate.
   |-- Revenue by cohort: group by signup month.
   |-- Verification: Create 100 subscriptions with varying dates → MRR, churn, LTV calculate correctly.
   |-- Output: Revenue dashboard with MRR, churn, cohort LTV.
```

  Complete when: Platform fee is stored in database config (not hardcoded in source), fee change takes effect at effective_date without code deploy; subscription lifecycle handles trialing→active→past_due→unpaid with dunning retries at 1/3/5 days past due; and MRR/churn/LTV dashboard calculates correctly against 100 test subscriptions with varying dates.
  Complete when: Payment flow tested end-to-end — subscription, one-time, and refund scenarios.
  Complete when: Revenue recognition rules verified with accounting — compliant with ASC 606.

## Best Practices
<!-- STANDARD: 3min -->

1. **Store money in integer cents, always.** Every amount in your system — dollar, euro, yen, bitcoin — must be the smallest currency unit as an integer. $10.99 = 1099 cents, ¥500 = 500 yen. Float-based money math accumulates rounding errors: `0.1 + 0.2 = 0.30000000000000004` in IEEE 754. Over 100K transactions, float drift can reach thousands of dollars. Use `DECIMAL(19,4)` in SQL only for multi-currency FX, and even then, convert to integer before ledger entry.

2. **Idempotency keys are a protocol, not a database constraint.** A UNIQUE index prevents duplicate writes but does not return the original response. The full idempotency protocol: (a) client generates key per payment intent, (b) server checks store, (c) if found, return STORED response with SAME HTTP status, (d) if not found, process payment, store response, return. Key collision detection: same key + different body → 422 Conflict. Key TTL: >= 24 hours. Key scope: per merchant/account, not global.

3. **Webhook reconciliation is mandatory, not optional.** Webhooks fail. They arrive out of order. They get duplicated. A payment_captured webhook can arrive AFTER a refund webhook. Run a reconciliation job every 1-6 hours: fetch all transactions from processor API for the last 24 hours, compare against local records, resolve mismatches. Process webhooks by event timestamp, not arrival order. If a webhook for a 3-day-old event arrives, it should still be processed correctly (your order state machine should handle this).

4. **Double-entry ledger from day one.** Not "when we scale." Not "after MVP." The ledger is 3 tables and 200 lines of code. It proves every balance is correct in any dispute. It enables reconciliation. It survives audit. A single balance table that you UPDATE in place is wrong the moment it deploys. Migrating from single-table to double-entry takes 5x longer than starting with it. Every bank since the Medici family has used double-entry for a reason.

5. **Test with real test cards, test webhooks, and deliberate failures.** Use Stripe's test card numbers (`4000 0000 0000 3220` for 3D Secure, `4000 0000 0000 0002` for declines). Test: insufficient funds, card declined, 3D Secure required, network timeout simulation. Use stripe-cli to trigger webhooks locally. Test: idempotency collisions, concurrent transfers, race conditions, reconciliation gaps. A payment system that hasn't been tested against failures will fail in production.

6. **The subscription lifecycle is a state machine, not a cron job.** Trialing → Active → PastDue → Unpaid → Canceled. But also: Paused, Incomplete, IncompleteExpired. Each state transition has financial implications (proration, credit notes, dunning emails, invoice generation). A cron job `UPDATE subscriptions WHERE end_date < NOW()` is wrong because it ignores mid-cycle cancellations, proration, and grace periods. Model it as a state machine with explicit transitions.

7. **Separate payment capture from order fulfillment.** Payment confirmation (webhook) should trigger order fulfillment, not replace it. An `order` table with status `PENDING_PAYMENT → PAID → FULFILLING → FULFILLED → COMPLETED` decouples the two. If Stripe webhooks are delayed 2 hours, orders move to `PAID` when the reconciliation job catches up. Never tie fulfillment directly to webhook arrival.

8. **Use Stripe Elements or Checkout to minimize PCI scope.** Both solutions host card input fields on Stripe's domain — card data never touches your server. This qualifies you for SAQ A (22 requirements) instead of SAQ A-EP (191 requirements) or SAQ D (329 requirements). The engineering cost difference is nil. The compliance cost difference is $50K-$200K/year. There is no technical reason to handle raw card data.

9. **Multi-currency requires explicit exchange rate sourcing.** Store rates from a provider (Open Exchange Rates, ECB, Stripe's forex). Record every rate with timestamp + provider + rate pair. Never use a hardcoded rate. Currencies that differ by 1% compound into significant reconciliation drift. For wallet holding: keep separate balances per currency. For conversion: apply rate at conversion time, record conversion entry in ledger.

10. **Fraud detection is a launch requirement, not a post-launch feature.** Minimum viable fraud detection: (a) velocity checks per user/card/IP, (b) first transaction >$500 on account <24h old = flag, (c) transaction amount > 3x user average = flag, (d) consecutive micro-transactions ($0-5) = card testing block. These are 300 lines of code that prevent 90% of fraud vectors. Launch without them and you're running a honeypot.

11. **Every API call to a payment processor needs a timeout, retry, and circuit breaker.** Stripe's API has 99.95% uptime — which means 4.38 hours of downtime per year. Your code must handle: (a) timeout: 10s for payment creation, (b) retry: 3 attempts with exponential backoff (1s, 2s, 4s) for idempotent operations only, (c) circuit breaker: after 5 consecutive failures, stop calling for 30s, alert on-call. Never retry non-idempotent operations — that's how double charges happen.

12. **Revenue model changes are database migrations.** Shifting from 2.9% + $0.30 to 2.5% + $0.25 requires: (a) new fee configuration version in DB, (b) effective date, (c) all transactions after effective date use new rates, (d) existing subscriptions grandfathered or migrated. Hardcoding a fee change in code means rollback requires a code deploy, not a config change. A "quick config change" that takes 2 days of deploy pipeline is not quick.

## Error Decoder — War Stories from the Trenches
<!-- STANDARD: 3min -->

| Error Message | Root Cause | Fix | Lesson |
|---|---|---|---|
| Customer charged twice for same order — $250 duplicate charge. Refund takes 5 business days, customer disputes both charges | Retry logic without idempotency: mobile client sent POST, network dropped before response, client retried without idempotency key. Server processed both as new charges | (1) Add idempotency key requirement to payment endpoint. (2) Before processing any charge, check idempotency store. (3) Duplicate key → return cached response, not new charge | The cost of missing idempotency is not the duplicate charge — it's the duplicate charge + the $25 chargeback fee + the customer loss + the processor fraud flag. 50 lines of code prevents infinite cost. |
| Webhook processing causes orders stuck in "pending" for 6 hours. 200 orders unfulfilled, support team overwhelmed | Stripe webhook outage: webhooks were delayed 4 hours. During gap, orders created at `PENDING_PAYMENT` and never updated because the system relied solely on webhooks for status updates | (1) Add reconciliation job running hourly. (2) Reconciliation queries Stripe API for all payments in last 24h. (3) Any payment captured but order not updated → update order status. (4) Alert if reconciliation finds >10 mismatches | Webhooks are notifications, not transactions. The reconciliation job is the transaction. During any processor outage, only reconciliation keeps your system consistent. |
| Wallet balance shows $500 but ledger shows $490. Customer demands $10, company pays $50 "goodwill credit" to resolve complaint | Single balance UPDATE instead of ledger insert: a concurrent transfer deducted $10 after the balance was read but before it was written. The UPDATE overwrote the deduction with the stale read value | (1) Never UPDATE balances in place. (2) BALANCE = SUM(ledger_entries). (3) When balance display doesn't match ledger, recalculate from ledger — ledger is always correct | Lost update on a balance field is a class of bug that double-entry ledger eliminates at the architecture level. A balance that can be stale is a balance that will be stale. |
| Subscription billed customer $99 after they canceled — 3 months in a row before anyone noticed | Cancelation was recorded as `status: canceled` but the billing job used `end_date > NOW()` to find active subscriptions. Canceled subscriptions with future end_dates were still picked up | (1) Billing job must check status: WHERE status = 'active' AND next_billing_date <= NOW(). (2) Subscription status is the gate, not dates. (3) Add assertion: after any billing run, verify no subscription with status='canceled' was charged | Boolean decisions in financial code compound. A single missing `WHERE status = 'active'` cost $297 in refunds, 3 months of trust damage, and potential chargeback fees if the customer disputed. |
| P2P transfer deducted sender, never credited receiver. $1,000 in limbo — customer service can't explain where money is | Transfer processed as two separate operations with no atomicity: debit succeeded, credit failed due to a transient DB connection error. No compensating transaction ran because the failure wasn't caught | (1) Wrap debit+credit in a state machine. (2) DEBITED state has a timeout → if no CREDITED within 30s, reverse debit. (3) Use outbox pattern: write transfer intent + state atomically, process states asynchronously. (4) Idempotent state transitions | Financial transactions are distributed systems problems. "Debit then credit" is not atomic — you need compensating transactions and timeouts for every state where money has left one account but not arrived in another. |
| Stripe charges succeeded but local order status stuck at PENDING. 500 orders later, nobody noticed until monthly revenue report showed $50K gap between Stripe and internal numbers | Webhook secret rotation: Stripe dashboard had new webhook signing secret after a security incident. Old secret in env vars. All webhooks were failing signature verification and being silently dropped | (1) Webhook handler must LOG and ALERT on signature failure, never silently drop. (2) Monitor webhook success rate — if it drops below 95%, alert immediately. (3) Webhook secrets should be in a secret manager with audit log for rotations. (4) Reconciliation job caught this 24h later — but should have been 5 minutes later with alerting | Silently dropping webhooks is a data integrity emergency. Every webhook failure must be noisy. Alert thresholds: webhook success rate < 99% in any 5-minute window triggers P1 alert. |

## Production Checklist
<!-- STANDARD: 3min -->

Every item must pass before ANY production deployment that processes real money. Failure on any item blocks deployment.

| # | Check | Verification | Failure Cost |
|---|-------|-------------|--------------|
| [FINTECH1] | Idempotency keys enforced on every POST /payments, POST /transfers, POST /refunds endpoint | Send same idempotency key twice → identical response, no second charge. Send same key + different body → 422. | $25-35/duplicate chargeback + customer loss |
| [FINTECH2] | Double-entry ledger with immutable entries — no UPDATE or DELETE on ledger_entries table | SELECT SUM(amount) FROM ledger_entries WHERE transaction_batch_id = X → debits = credits. DB permissions: ledger_entries table is INSERT-only for application user. | $500-10K/unreconcilable funds + unwinnable disputes |
| [FINTECH3] | Webhook signature verification before processing any event | Send webhook with invalid signature → 401, event NOT processed. Send valid signature → 200, event processed. | $2K-50K in missed payment events per hour of silent failure |
| [FINTECH4] | Automated reconciliation job running at <= 6-hour intervals | Delete a payment record from local DB, run reconciliation → record recreated within 1 cycle. Mismatch > 10 transactions triggers alert. | $100-5K/day in unreconciled transactions |
| [FINTECH5] | Zero raw PAN/CVV/track data in any persistent storage, logs, or error messages | grep -r "card_number\|pan\|cvv\|cvc\|track_data" across codebase → zero results in non-test files. Check production logs for last 24h → no card data in log entries. | $50K-200K PCI fine + mandatory forensic audit |
| [FINTECH6] | Payment test suite exercises ALL failure modes | Test cards: decline (4000...0002), insufficient funds (4000...9995), 3D Secure (4000...3220), expired card, stolen card. Network: simulate timeout, simulate webhook delay. | $500-10K in unhandled edge cases in first month of production |
| [FINTECH7] | Subscription billing state machine handles all lifecycle transitions | Test: trial→active, active→past_due, past_due→active (recovery), past_due→unpaid (3 failed dunning), active→canceled, canceled→reactivated with proration. | $100-500/customer in incorrect billing + manual corrections |
| [FINTECH8] | P2P transfer state machine with compensating transactions for every state | Kill process during debit → transfer rolls back. Kill process during credit → debit reversed, both balances unchanged. After 3 retry failures → moves to dead letter queue with alert. | $100-10K per stuck transfer in limbo |
| [FINTECH9] | Velocity checks active on payment and transfer endpoints | Fire 6 transactions from same user in 1 minute → 5th BLOCKED. Fire 3 transactions from same card across 3 different accounts → all 3 FLAGGED. | $500-5K/card testing attack wave |
| [FINTECH10] | Multi-currency: amounts stored in integer cents, exchange rates timestamped and sourced | Process $10.99 payment → DB has 1099, not 10.99. Exchange rate: check that rate has provider + timestamp + rate pair. | $100-1K/day in float rounding drift |
| [FINTECH11] | All payment processor API calls have timeout (10s), retry (3x with exponential backoff), circuit breaker | Simulate Stripe API timeout → 3 retries fire → circuit breaker opens after 5 consecutive failures. Non-idempotent operations do NOT retry. | $1K-50K in cascading failures during provider outage |
| [FINTECH12] | Platform fees are configuration-driven, not hardcoded | Change fee from 2.9% to 2.5% in platform_config → new payments use 2.5% immediately. No code deploy required. | 2-day deploy cycle for "urgent fee change" during pricing emergency |
| [FINTECH13] | Production API keys are NOT in any non-production environment | Check staging/QA configs → only test mode API keys (sk_test_, test_*, sandbox_). Attempt to use staging keys against production → fails. | Accidental production charges on test data + processor account flag |
| [FINTECH14] | Revenue reporting: MRR, churn, LTV, transaction fees correctly calculated on test data | Create 100 subscriptions with known patterns → MRR matches manual calculation. Cancel 5 subscriptions → churn = 5%. | $10K-100K in incorrect financial reporting leading to bad business decisions |
| [FINTECH15] | Database backups include ledger_entries and are tested with restore drill | Restore latest backup to test environment → run balance verification: all account balances = SUM(ledger_entries). Test restore completes in < 1 hour. | Complete loss of financial transaction history — unrecoverable |

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

| Upstream Skill | What You Receive | Decision Gate |
|---|---|---|
| **backend-developer** | API framework setup, middleware patterns, database connection management, authentication layer | Before Phase 1 — payment endpoints need auth and DB. Confirm: auth middleware, database with transaction support, error handling conventions. |
| **api-designer** | REST/GraphQL API contract for payment, wallet, transfer, and subscription endpoints | Before Phase 1 — OpenAPI spec for payment endpoint includes Idempotency-Key header, error response schema for 422/409/402. Confirm: all payment-mutating endpoints have idempotency in spec. |
| **database-designer** | Ledger schema, balance materialization strategy, transaction isolation requirements | Before Phase 2 — ledger entries table must be INSERT-only, balances are derived views. Confirm: SERIALIZABLE isolation level for ledger entry batches, partial index on idempotency keys, BRIN index on created_at. |
| **financial-security** | PCI scope assessment, tokenization strategy, fraud detection architecture, KYC requirements | Before Phase 4 — SAQ type determined, card data flow mapped, tokenization confirmed. Confirm: zero raw PANs anywhere, fraud rules defined, KYC threshold set. |
| **security-engineer** | API authentication, webhook signature verification, secret management, rate limiting | Before Phase 1 — webhook signing secret rotated, API keys in vault, rate limiting on payment endpoints. Confirm: webhook signature verification code reviewed by security. |
| **compliance-officer** | KYC/AML requirements, transaction monitoring thresholds, SAR filing triggers, regulatory jurisdiction | Before Phase 4 — KYC requirements defined, transaction monitoring rules set, regulatory reporting obligations documented. Confirm: KYC threshold, withdrawal limits, PEP screening integration. |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| **qa-engineer** | Payment test suite with all failure modes, sandbox environment, idempotency test cases, webhook simulation | QA cannot validate payment flows without sandbox + test cards + webhook simulation. Missing test suite → production bugs found by customers. |
| **security-reviewer** | Card data flow diagram, tokenization implementation, webhook handler code, API key management | Security review blocked without understanding where card data transits. Missed tokenization gap → PCI audit finding. |
| **performance-engineer** | Payment endpoint latency targets, concurrent transfer throughput, webhook processing capacity | Performance testing blocked without realistic payment traffic patterns. Under-provisioned → payment timeouts under load. |
| **ci-cd-builder** | Webhook secret injection, test API key rotation, reconciliation job scheduling, database migration order | CI/CD can't deploy without knowing secrets, cron schedules, and migration dependencies. Wrong migration order → ledger corruption. |
| **accountant** | Ledger export format, transaction categorization, fee allocation, reconciliation reports | Accounting can't close books without ledger data in their format. Delayed ledger → delayed financial reporting → compliance risk. |
| **fp-and-a-analyst** | Revenue data: MRR, churn, LTV, transaction fees by payment method, customer cohort revenue | Financial planning can't model without actual revenue data. Delayed revenue data → incorrect forecasts → misallocated budget. |

## Proactive Triggers
<!-- STANDARD: 3min -->

| # | Trigger Condition | Severity | Auto-Response |
|---|---|---|---|
| P1 | Payment endpoint created AND no `Idempotency-Key` header mechanism | 🔴 CRITICAL | [ALERT] Every payment endpoint without idempotency will double-charge customers. Implement idempotency store + key deduplication before allowing any traffic. Cost: $25-35 per duplicate chargeback. |
| P2 | Wallet balance implemented as single UPDATE-able column AND no ledger entries table | 🔴 CRITICAL | [ALERT] Single-table balance tracking makes disputes unwinnable. Implement double-entry ledger with immutable entries. Cost: $500-10K per unreconcilable balance discrepancy. |
| P3 | Webhook handler AND no signature verification | 🔴 CRITICAL | [ALERT] Unsigned webhook processing allows payment forgery. Implement HMAC/RSA signature verification before any event processing. Cost: unlimited fraudulent payment acceptance. |
| P4 | Card data (PAN/CVV) in logs, error messages, or DB schema outside tokenized fields | 🔴 CRITICAL | [ALERT] Raw card data expands PCI scope. Replace with token references (PaymentMethod ID). Cost: $50K-200K PCI fine + audit. |
| P5 | Money math using float/double instead of integer cents | 🟡 HIGH | [WARN] Float-based money accumulates rounding errors. Convert all amounts to integer cents (smallest currency unit). Drift of $0.0003/tx × 100K txs = $30. Scale to $100M = $30K drift. |
| P6 | Transfer/debit-credit logic AND no compensating transaction for intermediate states | 🟡 HIGH | [WARN] Money can get stuck in ESCROW/PENDING state if credit fails after debit succeeds. Implement state machine with timeout-based compensating transactions for each non-terminal state. |
| P7 | Subscription billing AND cron-based renewal without state machine | 🟠 MEDIUM | [WARN] Cron-based billing misses edge cases (proration, dunning, grace period). Implement subscription state machine with explicit transitions. Cost: incorrect charges requiring manual refund. |
| P8 | Multi-currency support AND hardcoded exchange rates | 🟠 MEDIUM | [WARN] Hardcoded FX rates go stale immediately. Use exchange rate API with timestamped rates. Drift of 1% on $1M cross-currency volume = $10K unreconcilable. |

## Anti-Patterns
<!-- STANDARD: 3min -->

| ❌ Anti-Pattern | ✅ Do This Instead |
|---|---|
| **Checking balance with `SELECT balance FROM accounts` and then `UPDATE`-ing it** — the read and write are not atomic. Another transaction deducts money between the SELECT and UPDATE. You overdraw the account. | Balances are derived: `SELECT SUM(credit) - SUM(debit) FROM ledger_entries WHERE account_id = X`. Every money movement INSERTs ledger entries in a SERIALIZABLE transaction. Balance checks happen inside the same transaction as the deduction. |
| **Relying solely on webhooks for order fulfillment** — webhooks are unreliable. They can be delayed hours, arrive out of order, or be dropped entirely during provider outages. | Webhooks update status optimistically. A reconciliation job runs every 1-6 hours: query processor API for all transactions in last 24h, compare against local state, resolve mismatches. Webhooks are notifications, reconciliation is the source of truth. |
| **Using database UNIQUE constraint as idempotency** — prevents duplicate writes but returns a constraint violation error instead of the original response. The client sees an error, assumes failure, and initiates a refund or retry loop. | Full idempotency protocol: (1) check key in idempotency store, (2) if found → return stored response + same HTTP status, (3) if not found → process payment → store response → return. The client always gets the same response for the same key. |
| **Hardcoding payment processor API keys in source code** — keys in code = keys in git history = keys leaked to every developer with repo access = catastrophic when a developer's laptop is compromised. | API keys in environment variables or a secret manager (AWS Secrets Manager, HashiCorp Vault, Doppler). Production keys never in .env files committed to git. Use Stripe restricted API keys with minimum permissions per environment. |
| **Float-based money math:** `amount = 19.99; fee = amount * 0.029;` — IEEE 754 float representation error: `0.1 + 0.2 = 0.30000000000000004`. Over 1M transactions, drift reaches thousands. | Store and calculate in integer cents: `amount_cents = 1999; fee_cents = amount_cents * 29 / 1000;` (29 basis points = 0.29%). For division, use banker's rounding: round half to even to avoid systematic bias. |
| **Single payment processor with no fallback** — Stripe has 99.95% uptime = 4.38 hours/year of downtime. During those 4.38 hours, you process zero payments and lose revenue. | Multi-acquirer routing: Stripe primary + Adyen/Braintree secondary. Payment orchestration layer (Spreedly, Primer) routes to fallback on primary failure. Circuit breaker: after 5 consecutive primary failures, route all traffic to secondary for 5 minutes. |
| **"Process payment → send confirmation email" in the same synchronous request** — email delivery (SMTP) can take 2-10 seconds. The payment appears stuck. The user refreshes, resubmits, creates a duplicate. | Payment processing is synchronous and fast (< 2s). Everything else is async: confirmation email, receipt generation, analytics events, push notifications, webhook dispatch. Use a job queue (BullMQ, SQS, Sidekiq). |
| **"We'll figure out the revenue model after we have users"** — the revenue model determines the payment flow, the database schema, the fee calculation, the reconciliation logic, and the dashboard queries. Changing it later is a rewrite. | Design the revenue model first: (1) how do you charge? (% of tx, flat fee, subscription, interchange markup), (2) who pays? (sender, receiver, both), (3) when do you collect? (per-tx, monthly, threshold). Then build the system that implements it. |

## What Good Looks Like
<!-- STANDARD: 3min -->

```

Payment Flow:                              Wallet & Ledger:
  Client sends POST /payments               ┌──────────────────────────┐
    with Idempotency-Key: uuid              │ ledger_entries (immutable) │
  ┌─Server checks idempotency store─┐       │ debit_acct | credit_acct   │
  │ Key exists? → Return cached resp│       │   user_123  | platform     │
  │ Key is new:                     │       │   user_123  | fees         │
  │  → Stripe PaymentIntent.create  │       │   platform  | user_456     │
  │  → INSERT ledger (debit,credit) │       │ sum(debits) = sum(credits)│
  │  → Store response in idemp store│       └──────────────────────────┘
  │  → Return 200 + payment result  │       balance = SUM(credits) -
  └─────────────────────────────────┘                 SUM(debits)

  Webhooks:                              P2P Transfer:
  signature verified → event.id dedup'd  INITIATED → PENDING_DEBIT →
  → process event → reconciliation job    DEBITED → PENDING_CREDIT →
  closes gap every hour                   COMPLETED (or ROLLED BACK)

  Result:                                Result:
  Zero duplicate charges.                Zero money in limbo.
  Every cent reconciled.                 Both balances correct or
  SAQ A PCI compliance.                  unchanged. Every time.
  Revenue visible in real-time.          Audit trail for every transfer.

```

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| PCI compliance failures from storing raw card data — a single log statement that prints `req.body.card_number` means card data hits your logs, your monitoring system, and your backups | $50K-$500K in PCI fines ($5K-$100K/month of non-compliance) plus mandatory forensic audit ($20K-$50K) plus merchant account termination (existential for fintech); SAQ A (22 requirements) becomes SAQ D (329 requirements) the moment raw PAN touches your server | Use Stripe Elements/Checkout so card data never touches your server. If you must handle raw PAN (rare), use a PCI-compliant tokenization provider. Run `grep -r "card_number\|pan\|cvv\|cvc" --include="*.{js,ts,py,go,java}"` across the entire codebase before every deploy — zero non-test matches is the only acceptable result. Configure log scrubbers to redact card patterns. |
| Idempotency bugs causing double charges — checking idempotency store AFTER creating the payment instead of before, or a race condition where two concurrent requests both see "key not found" and both create charges | $10K-$200K in refunds, chargeback fees ($15-$25 per dispute), and irreversible trust damage — customers who get double-charged tell 5-10 people and often never return | The idempotency check-and-create must be atomic: use a database transaction with SELECT FOR UPDATE on the idempotency key row, or a Redis SETNX with TTL 24h. The stored response must include the full HTTP status code and body. Test with concurrent duplicate requests (Apache Bench or k6 with same key in multiple threads). If the provider charges $0.30 + 2.9%, a double-charge on a $1,000 transaction costs $1,000 + $29.30 in processing fees — both unrecoverable. |
| Reconciliation drift — webhook delivery failures, out-of-order events, or a reconciliation job that silently stops running for 3 weeks while transactions accumulate mismatches | $5K-$100K/month in unreconciled funds — every day of drift compounds: a 0.1% discrepancy on $1M/month volume = $1,000/day, $30K/month, invisible until an audit or customer complaint surfaces it | Run reconciliation every 1-6 hours, not daily. Alert on ANY reconciliation job failure (if the cron scheduler fails silently, you lose visibility). Implement a heartbeat: reconciliation job writes a `last_reconciliation_at` timestamp, and a separate monitor alerts if it's > 2x the expected interval. Track drift as a metric: `ledger_balance - processor_balance` should be $0.00 — any non-zero value is investigated same-day. |
| Float-based money math — using `double` or `float` for amounts, then wondering why $0.10 + $0.20 = $0.30000000000000004 in IEEE 754 | $1K-$50K in cumulative rounding errors over 100K+ transactions — a 0.01-cent rounding error per transaction compounds to $10 at 100K volume, but in multi-currency scenarios the error amplifies and becomes a reconciliation nightmare | Store every amount as integer cents: $10.99 = 1099. For division (fee calculation), use banker's rounding (round half to even) to avoid systematic bias. `DECIMAL(19,4)` in SQL only for FX rates and intermediate calculations — convert to integer cents before writing to the ledger. Audit: run `SUM(ledger.debits) - SUM(ledger.credits)` daily — any result other than exactly 0 is a bug. |
| Single payment processor with no fallback — Stripe has 99.95% uptime = 4.38 hours/year of downtime, and during those 4.38 hours you process zero payments | $5K-$50K in lost transaction revenue during an outage — for a platform processing $1M/month, a 4-hour outage costs ~$5,500 in lost GMV plus the customers who churn because "their payment didn't go through" | Implement multi-acquirer routing: Stripe primary + Adyen/Braintree secondary behind a payment orchestration layer (Spreedly, Primer). Circuit breaker: after 5 consecutive primary failures, route all traffic to secondary for 5 minutes. This is an L3+ concern — solo developers can use Stripe alone until $50K/month volume, but the architecture should support adding a fallback without rewriting the payment layer. |

## Verification Guardrails
<!-- STANDARD: 3min -->

Before delivering work, self-check against these conditions. If any fail, revise before delivering.

1. **Idempotency verified:** Duplicate idempotency key returns identical response with same HTTP status code. Different body + same key returns 422. Provider API called exactly once per unique key.
2. **Ledger integrity:** For any batch of entries in a single transaction, debits = credits. All entries are INSERT-only — zero UPDATE or DELETE on ledger_entries.
3. **No raw card data:** grep for `card_number`, `pan`, `cvv`, `cvc`, `track_data` across codebase → zero non-test-file matches. Production logs sampled → zero card data.
4. **Webhook security:** Invalid signature → 401. Valid signature → processed. Event ID deduplication working. Reconciliation job tested with deliberate gap.
5. **Failure mode coverage:** Tested: card declined, insufficient funds, 3D Secure required, network timeout, webhook delay, idempotency collision, concurrent transfer race condition.
6. **Money in integer cents:** No float in any amount field. All amounts stored as smallest currency unit. Exchange rates timestamped and sourced.
7. **State machines complete:** Transfer state machine has compensating transactions for every non-terminal state. Subscription state machine handles all lifecycle transitions.
8. **Platform fees configurable:** Fee change is a database config update, not a code deploy. All transactions after effective date use new fee.
9. **Sandbox separation:** Zero production API keys in dev/staging/QA. Test mode confirmed with test card numbers.
10. **Cross-skill continuity:** State log updated with all major decisions. References to financial-security, backend-developer, api-designer are consistent. No contradictions with downstream skill expectations.

## Deliberate Practice
<!-- STANDARD: 3min -->

The best fintech developers treat financial correctness as non-negotiable. Deliberate practice means building payment systems with double-entry accounting, idempotency, and reconciliation from day one.

| Level | Practice Routine | Frequency |
|---|---|---|
| **Novice** | Build a simple payment processing endpoint with Stripe/Plaid integration. Implement idempotency keys and basic error handling. Process 100 test transactions with zero data loss | Monthly |
| **Competent** | Build a complete wallet system with double-entry ledger, transaction history, and balance reconciliation. Implement webhook handling with retry logic. Run 1000+ transactions through reconciliation | Quarterly |
| **Advanced** | Build a P2P transfer system with idempotency, compensating transactions, and real-time fraud detection. Pass a security audit (OWASP Top 10 + PCI DSS checklist). Process 10K+ test transactions | Biannually |
| **Expert** | Design and build a production fintech platform processing real money. Implement SOC 2 controls, KYC/AML integration, and regulatory reporting. Ship to production with 99.99% transaction success rate | Annually |

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift. Every major decision (payment processor, ledger architecture, compliance strategy) must be recorded.

| Decision | Date | Rationale | Alternatives Considered |
|----------|------|-----------|------------------------|
| *Record all critical decisions here* | — | — | — |

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->
**(STANDARD)**

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | `which [tool]`. Install via package manager | Check PATH. Symlink if needed | Use functionally equivalent alternative |
| Payment processing error | Check Stripe/Plaid dashboard. Verify API keys and webhook signature | Review provider error docs. Test in sandbox mode | Contact provider support with request IDs and timestamps |
| Permission denied | Verify API key scopes and environment. Check `ls -la` for files | Refresh credentials. Check token expiration | Use different auth method or environment |
| Command hangs | Kill and re-run with `timeout 30`. Check resources | Add debug flags. Reduce scope | Split work. Exponential backoff retry |
| Data integrity (transactions) | Reconcile against provider dashboard. Compare checksums | Run on subset. Check for race conditions and idempotency | Abort and flag for human review — financial data errors are unacceptable |

**Hard failure boundary:** If 3 approaches fail, STOP. For fintech, data integrity failures are NEVER acceptable to bypass. Log everything and escalate.

## References
<!-- STANDARD: 3min -->

- [Stripe API Reference](https://stripe.com/docs/api) — PaymentIntents, PaymentMethods, SetupIntents, webhooks, idempotency, Connect
- [Stripe: Idempotent Requests](https://stripe.com/docs/idempotency) — Key generation, retry strategy, POST-only idempotency
- [Adyen API Explorer](https://docs.adyen.com/api-explorer/) — /payments, /recurring, /payouts, webhooks, revenue optimization
- [Braintree Developer Docs](https://developer.paypal.com/braintree/docs) — Gateway API, recurring billing, marketplace, dispute handling
- [Square Developer](https://developer.squareup.com/) — Payments API, Orders API, Invoices API, sandbox setup
- [Plaid API](https://plaid.com/docs/api/) — Auth, Transactions, Identity, Income, Assets, Transfer, Signal, Link
- [Teller API](https://teller.io/docs) — Account linking, transaction fetching, real-time webhooks for UK/EU banking
- [PCI SSC: SAQ Types](https://www.pcisecuritystandards.org/document_library/) — SAQ A (22 requirements) vs SAQ A-EP (191) vs SAQ D (329)
- [Stripe: PCI Compliance Guide](https://stripe.com/docs/security) — Elements/Checkout for SAQ A qualification, tokenization best practices
- [Stripe: Subscription Billing](https://stripe.com/docs/billing) — Plans, proration, dunning, invoices, metered billing
- [Stripe Connect](https://stripe.com/docs/connect) — Custom/Express/Standard accounts, marketplace payments, split payouts
- [Plaid: Transfer](https://plaid.com/docs/transfer/) — ACH transfer initiation, balance check, transfer status tracking
- [/scripts/verify-skill.sh](scripts/verify-skill.sh) — Verify all 18 required sections, ground rules, decision trees, best practices
