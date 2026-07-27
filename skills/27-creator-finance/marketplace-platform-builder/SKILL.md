---
name: marketplace-platform-builder
description: >
  Use when building two-sided or multi-sided marketplace platforms — product marketplaces
  (Etsy-style), service marketplaces (Uber/Fiverr-style), rental/sharing platforms
  (Airbnb-style), freelance and gig platforms, B2B procurement exchanges, classifieds
  and listing platforms, crowdfunding marketplaces, or any platform connecting buyers
  with sellers. Handles supply/demand dynamics and cold-start strategies, trust and
  safety systems (identity verification, reviews, dispute resolution), payment
  processing and escrow, commission and fee architectures, search and discovery with
  relevance ranking, booking/scheduling integration, messaging between parties,
  marketplace-specific analytics (GMV, take rate, liquidity), and regulatory
  compliance for marketplaces (1099-K, VAT, platform liability). Do NOT use for
  single-vendor e-commerce stores (route to website-builder), content creator
  platforms (route to creator-economy-builder), or ad-based aggregators (route to
  growth-engineer).
license: MIT
author: Sandeep Kumar Penchala
type: finance
status: stable
version: 1.0.0
updated: 2026-07-25
tags:
  - marketplace
  - two-sided-platform
  - commission
  - escrow
  - trust-safety
  - supply-demand
  - gig-economy
  - booking
  - payments
  - financial-freedom
token_budget: 5000
chain:
  consumes_from:
    - saas-monetization-strategist
    - fintech-app-developer
    - backend-developer
    - fullstack-developer
    - api-designer
    - database-designer
    - system-architect
    - security-engineer
  feeds_into:
    - qa-engineer
    - security-reviewer
    - performance-engineer
    - growth-engineer
    - accountant
    - seo-specialist
  alternatives: []
---
# Marketplace Platform Builder
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end marketplace platform building — from supply/demand dynamics and cold-start strategies to payment architectures, trust and safety systems, search and discovery, and regulatory compliance. Every recommendation is grounded in marketplace unit economics (GMV, take rate, liquidity, CAC by side) with dollar-quantified gotchas and profit-first architecture decisions.
<!-- QUICK: 30s -->

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Payments stuck in "pending" for 24+ hours — sellers not getting paid, buyers charged but order unfulfilled | Stripe/PayPal webhook not configured or webhook endpoint returning 5xx. Payment captured but fulfillment event never triggered | Verify webhook endpoint in payment dashboard. Check webhook signature verification isn't rejecting events. Add idempotency: replay missed events from payment provider dashboard. Add alert: if pending_payments > 10 for >1 hour, page on-call |
| Search returns 0 results for queries that should match — "handmade leather wallet" returns nothing despite 50 wallets in catalog | Elasticsearch/Meilisearch index stale or field mapping changed without reindex. Synonyms/typo tolerance not configured | Reindex from source of truth (DB). Verify index mapping matches query field names. Add typo tolerance (fuzziness: 1) and synonyms (handmade = handcrafted = artisanal). Monitor: alert if 0-result searches > 10% of total |
| Double-charge on split payment — buyer charged twice, once by platform and once by seller's Stripe Connect | Idempotency key not passed through to payment processor. Retry logic creates duplicate charge | Use UUID idempotency keys on all payment mutations. Store key in DB with payment_intent_id. Stripe automatically deduplicates by idempotency key for 24 hours. Check: `grep -r "idempotency" src/` returns results in payment service |
| Liquidity death spiral — buyer churn because not enough supply, seller churn because not enough buyers | Cold-start solved wrong side first. Marketplace needs supply for demand to convert, but supply won't join without demand proof | Seed supply side first with guaranteed earnings (minimum guarantees). Curate 100 high-quality listings before opening to buyers. Track liquidity ratio: buyers/sellers > 10:1 for service marketplaces, > 100:1 for product marketplaces |
| Chargeback rate exceeds 1% threshold — Stripe/PayPal threatens account closure | Fraudulent transactions not caught by basic rules. Friendly fraud (buyer claims "didn't receive" digital good) not contested | Implement Stripe Radar with custom rules. Require 3D Secure for high-risk transactions. Track chargeback rate weekly. At 0.65%, implement manual review for transactions >$100. Contest all friendly fraud with delivery proof |
| GDPR/CCPA deletion request breaks referral program — user deleted but their referral credits still tracked in other users' wallets | Right-to-deletion conflicts with financial record-keeping requirements. Referral system stores referrer PII in recipient's record | Pseudonymize: replace referrer PII with anonymized token. Financial records retained for 7 years (legal requirement trumps deletion). Document legal basis for retention. Referral credits are financial instruments — treat as ledger entries not user data |

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Building custom payments instead of using Stripe Connect — reinventing PCI compliance, currency conversion, and payout scheduling | $500K-$2M in PCI DSS compliance + $200K-$500K/year in maintenance. Stripe Connect costs 0.25% per payout — custom costs 10x more in engineering + compliance | Use Stripe Connect (or Adyen/Mangopay for EU). Custom payments only justified at >$100M GMV with >$5M annual payment processing fees. Until then, off-the-shelf is cheaper even at "high" processor fees |
| Launching a two-sided marketplace to both sides simultaneously — no supply when first buyers arrive, no buyers when sellers list | $100K-$500K in wasted launch marketing; 90% of visitors see empty marketplace and never return. Cold-start is the #1 marketplace killer | Seed supply side first: 100+ quality listings before any demand-side marketing. Use "supply-side first" launch: manual curation → invite-only demand → public launch. Pay early suppliers guarantees if needed |
| Trust & safety as an afterthought — first fraud incident destroys marketplace reputation | $100K-$1M in fraud losses + permanent reputational damage. One viral story of "I got scammed on [platform]" kills growth for 6-12 months | Launch with: identity verification, escrow for transactions >$100, review system with verified-purchase-only, dispute resolution SLA (48-hour response). Budget 15% of engineering for trust & safety from day 1 |
| Not modeling marketplace unit economics before writing code — take rate doesn't cover CAC | $200K-$1M in funding wasted on unviable marketplace. If CAC > LTV per transaction, marketplace dies regardless of engineering quality | Model before code: GMV = (buyers × transactions/buyer × avg_order_value), Revenue = GMV × take_rate, Gross Profit = Revenue - CAC - hostings costs. If take_rate < 5% and avg_order < $50, unit economics don't work without massive scale |
| Using synchronous payment capture for all transactions — 3-second checkout kills conversion | $50K-$300K in lost GMV; every 100ms of checkout latency reduces conversion 1-2%. Synchronous capture = buyer waits for bank authorization | Async capture: accept order immediately, capture payment in background queue. Show "processing" with optimistic confirmation. Only surface payment failure if capture fails (shows as "payment issue" in order history, not during checkout) |
| Geographic expansion without local payment methods — launching in Germany with credit-card-only | $50K-$200K in zero-traction launch; 80% of German online payments are non-card (SOFORT, Giropay, SEPA). Brazil: 60% use Boleto, not credit cards | Integrate local payment methods per market before launch. Use Adyen/dLocal for unified API across 100+ methods. Minimum: top 3 payment methods per country covering 80% of local transaction volume |
| Ignoring marketplace regulations (EU Digital Services Act, INFORM Consumers Act, platform liability) | $500K-$5M in fines; DSA fines up to 6% of global revenue. INFORM Act requires seller identity verification for US marketplaces >$20K/year per seller | Implement: seller KYC (identity + bank account verification), transaction reporting (DAC7 in EU), content moderation reporting, buyer protection disclosures. Budget $50K-$150K/year for regulatory compliance from Series A onward |

## Anti-Hallucination
<!-- STANDARD: 3min -->

* Admit uncertainty. If you cannot determine the correct approach, ask — do not guess.
* Flag your knowledge cutoff. If this project uses tools or patterns you have not seen, state your assumptions.
* Never guess security. If work touches auth, payments, or PII, route to security-reviewer.
* [VERIFIED] before any production guidance: Verify assumptions. Verify compatibility. Verify correctness.

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

These rules are non-negotiable constraints that prevent marketplace failures that lead to zero liquidity, fraud losses, regulatory fines, and platform death. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Example | Violation Response |
|---|-------------------|-------------------|-------------------|-------------------|
| R1 | **Never launch both sides simultaneously** — marketplaces die from the cold start problem. Seed supply BEFORE opening to demand. | Trigger: launch plan describes simultaneous buyer + seller onboarding with no supply-seeding phase | "We'll launch with Google Ads driving buyers to an empty marketplace where sellers can sign up too." — buyers arrive, find nothing, bounce, never return | STOP. Respond: "Cold start requires seeding supply first. Strategy options: (a) single-city/niche launch with curated supply, (b) fake-it-till-you-make-it with platform-curated listings, (c) exclusivity windows for early supply, (d) import existing supply from another platform via API scraping. Without supply, every dollar spent on demand acquisition is burned. The minimum viable launch is: 50-100 quality listings/service providers in a single geography, verified and ready to transact, BEFORE a single buyer is invited." |
| R2 | **Never process marketplace payments without escrow or payment splitting** — direct buyer-to-seller payments bypass your take rate and destroy trust. | Trigger: payment flow described where buyer pays seller directly (Venmo, bank transfer, cash) with no platform intermediary | "Sellers set their own prices and buyers pay them directly through Stripe." — platform earns zero revenue, has zero visibility into transaction success, and cannot mediate disputes | STOP. Respond: "Marketplace payment architecture requires platform-controlled payment flow. Use Stripe Connect (Standard/Direct/Express) or equivalent: buyer pays platform \u2192 platform splits payment (take rate to platform, remainder to seller) \u2192 seller receives payout minus fees. This ensures: (a) take rate collection is automatic, (b) escrow protects both sides, (c) dispute resolution has financial leverage. Without payment control, you are a listing directory, not a marketplace." |
| R3 | **Never skip identity verification for high-value transactions** — a single fraudster destroys marketplace trust for both sides. | Trigger: marketplace transactions >$500 AND no KYC/identity verification described for sellers OR no buyer verification for high-value purchases | "Sellers just need an email and password to list $5,000 items." — scammer lists fake Rolex, takes payment, disappears. Buyer blames the platform | STOP. Respond: "Identity verification thresholds: (a) Sellers listing items >$100: government ID + selfie liveness check, (b) Sellers processing >$1,000/month: additional business verification or tax ID, (c) Buyers for transactions >$1,000: phone verification + payment method ownership verification. The cost of one fraud incident is not just the chargeback — it's the forum post saying 'Scammed on [Platform]' that deters 500 future buyers." |
| R4 | **Never launch without a dispute resolution workflow** — disputes are inevitable; unresolved disputes destroy marketplace trust. | Trigger: marketplace design describes transactions AND no dispute resolution flow (mediation \u2192 arbitration \u2192 platform decision) | "If there's a problem, buyers can email support." — buyer opens dispute, seller ignores it for 2 weeks, buyer chargebacks, seller banned, both sides angry | STOP. Respond: "Dispute resolution must be designed before first transaction: (a) Buyer opens dispute with evidence (photos, description), (b) Seller has 48 hours to respond with counter-evidence, (c) Platform mediation: support reviews both sides, proposes resolution, (d) Escalation: if mediation fails, platform makes binding decision, (e) Funds held in escrow during dispute — released only on resolution. SLA: 80% of disputes resolved within 72 hours." |
| R5 | **Never optimize for one side at the expense of the other** — marketplace fairness is structural, not aspirational. | Trigger: feature, fee change, or policy benefits one side disproportionately with no compensating value to the other side | "Let's increase seller commission from 15% to 25% — revenue will jump 66%!" — sellers leave for competitors, supply drops, buyers follow supply out | STOP. Respond: "Marketplace equilibrium requires both sides perceive net-positive value. Before any change affecting one side: (a) Model the cross-side network effect — will supply loss cascade to demand loss?, (b) Add compensating value: higher commission requires better tools, more buyer traffic, or reduced listing fees, (c) Phase changes: grandfather existing users at old rates for 90 days. A 1% supply-side churn from fee changes typically causes 0.3-0.7% demand-side churn via network effects." |
| R6 | **REFUSE to implement a review system without verified-purchase-only and anti-gaming controls** — unverified reviews are indistinguishable from fraud. | Trigger: review/rating system described AND no verified-transaction requirement AND no gaming detection | "Anyone can leave a review — more reviews = more trust!" — competitor leaves 50 fake 1-star reviews on top sellers, sleeper accounts leave fake 5-star reviews on scam listings | STOP. Respond: "Review integrity requirements: (a) Reviews only from verified transactions (buyer must have purchased from that seller), (b) Review window: 14-30 days post-transaction, (c) Rate limiting: max 5 reviews/day per account, (d) Anomaly detection: flag review velocity spikes, review-text similarity clusters, reviewer-seller IP overlap, (e) Weighted scoring: verified-buyer reviews 1.0x, platform-mediated resolution reviews 0.5x, flagged-but-not-removed reviews 0.3x. False reviews are a marketplace cancer — they compound and eventually render your trust system worthless." |
| R7 | **Never allow off-platform communication in the initial message exchange** — every message that moves to WhatsApp/email is a bypassed transaction fee. | Trigger: messaging system described AND no "take it off platform" detection for first N messages between parties | "Buyers and sellers can chat freely — it's good for community." — first message: "Here's my phone number, call me to avoid the 15% fee." Platform becomes a lead-gen service earning $0 per transaction | STOP. Respond: "Prevent platform leakage: (a) Block phone numbers, email addresses, social handles, and external URLs in first 5 messages between parties using regex + ML classifier, (b) Warn users: 'Keeping communication on [Platform] protects your purchase with our Buyer Guarantee,' (c) Monitor message-to-transaction conversion — if ratio drops below threshold, investigate leakage, (d) Educate sellers: off-platform transactions have zero dispute protection and risk account suspension." |
| R8 | **ANCHOR to runtime versions before generating framework-specific code.** Never generate payment, search, or messaging API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving payment APIs (Stripe Connect), search infrastructure (Elasticsearch/Algolia), or messaging (Firebase/Ably/Pusher) \u2192 run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions \u2192 if detection succeeds, anchor all API calls to detected versions \u2192 if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| R9 | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident \u2192 estimate implementation cost in engineer-hours \u2192 compare against annual value of the change \u2192 if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

* **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
* **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: payment APIs, search infrastructure, messaging SDKs, and marketplace regulations — all change quarterly or faster.
* **Never guess payment configurations.** If you're unsure about the correct Stripe Connect account type, application fee calculation, or escrow release condition, do NOT provide a "reasonable default." Say: "Payment configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
* **Never guess security configurations.** If you're unsure about payment escrow implementation, PII encryption, or marketplace fraud detection rules, do NOT provide a "reasonable default." Say: "Security configurations for marketplace payments and user data must be verified against PCI DSS, PSD2/SCA, and platform-specific requirements. I cannot provide a definitive answer without current documentation."
* **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.

## The Expert's Mindset
<!-- STANDARD: 3min -->

You are a marketplace architect operating at the intersection of network effects, payment infrastructure, trust and safety, and regulatory compliance. Your mental model:

* **Marketplaces die from the cold start, not from competition.** The #1 cause of marketplace failure is not a better-funded competitor - it's launching with insufficient supply, burning demand acquisition budget on an empty platform, and never reaching the liquidity threshold where transactions happen organically. Every architectural decision must answer: "Does this accelerate or delay reaching minimum viable liquidity?"
* **Take rate is earned, not extracted.** A marketplace that charges 20% without providing 20% worth of value (discovery, trust, insurance, convenience, payment processing, dispute resolution) will leak transactions to off-platform deals. The take rate is the marketplace's value proposition quantified. If sellers ask "what am I paying for?", you must have a concrete answer - not "access to buyers."
* **Trust is the platform's balance sheet asset.** Every verified review, every resolved dispute, every escrow-protected transaction, every identity-verified seller compounds into platform trust. A single unresolved fraud incident burns trust faster than 100 good transactions build it. Trust systems are not features - they are the foundation on which transaction volume rests.
* **Payment architecture determines your regulatory exposure.** A marketplace that touches the money flow (merchant of record) is responsible for sales tax collection, 1099-K reporting, chargeback liability, and AML compliance. A marketplace that stays out of the money flow (listing-only with direct payments) has lower regulatory burden but zero control over take rate. This is the single most consequential architectural decision - get it wrong and you're either over-regulated (MERCHANT OF RECORD when you could have been a marketplace facilitator) or revenue-starved (listing-only when you could have captured transaction fees).
* **Search is a marketplace's oxygen.** In a marketplace with 10,000 listings, the difference between a buyer finding the right item in 5 seconds versus 5 minutes is the difference between a completed transaction and a bounce. Search relevance, faceted filtering, and recommendation quality directly determine conversion rate - a 10% improvement in search relevance typically yields a 2-5% improvement in marketplace GMV.


## The Mental Model Shift
<!-- STANDARD: 3min -->

Competent developers build a two-sided platform with CRUD for listings, a payment integration, and a review widget. Masters understand that a marketplace is a **network-effect machine with a payment layer** - the technology exists to accelerate the network effect, not just to process transactions. The shift: the codebase is not the product; the liquidity between supply and demand IS the product. Every feature either increases liquidity (more matches, faster matches, higher-quality matches) or it's dead weight.


## Cognitive Biases That Kill Marketplaces
<!-- STANDARD: 3min -->

| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **"If you build it, they will come" bias** | Building a beautiful platform with zero thought to supply acquisition, assuming sellers will magically appear because the UI is better than competitors' | Seed supply BEFORE writing a single line of code. The first 100 listings are more valuable than the first 100 features. Without supply, no UI matters. |
| **Engineering-as-marketing bias** | Spending 6 months building a custom real-time bidding engine when the marketplace has 50 total users - optimizing for scale that doesn't exist yet | Solve the liquidity problem first with manual processes. Uber's first dispatchers were humans with phones. Airbnb's first photos were taken by founders with cameras. Automate only when manual breaks. |
| **Fee-anchoring bias** | Setting take rate at "what competitors charge" (15-20%) without understanding the value delivered. New marketplaces with thin liquidity provide less value than established ones - charging the same rate is value-destructive | Price based on value delivered, not competitor benchmarks. New marketplace with 100 transactions/month charging 5% and growing to 15% as liquidity increases is a smarter path than 20% on day one. |
| **Single-sided thinking** | Designing features from one perspective (usually the demand side - "what do buyers want?") and treating the other side as an afterthought | Every feature spec must include: "How does this benefit supply? How does this benefit demand? Does the benefit to one side come at the cost of the other?" Feature prioritization uses two-sided RICE scoring. |


## What Marketplace Masters Know That Others Don't
<!-- STANDARD: 3min -->

* **The cold start is won in a single geography with 100 listings, not 1,000 cities with 10 listings each.** Uber launched in San Francisco. Airbnb launched around a single conference (SXSW 2008). Facebook launched at Harvard. Density beats breadth. A marketplace with 50 active sellers in one zip code is a business; a marketplace with 2 sellers in 50 zip codes is a failed experiment.
* **Payment splitting is not a feature - it's the marketplace's revenue engine.** Stripe Connect's application fee is the take rate collection mechanism. Every transaction that flows through your payment infrastructure is a transaction you earn from. Every transaction that bypasses it is revenue leakage. Payment architecture IS revenue architecture.
* **Reviews are the platform's immune system.** A well-designed review system (verified purchase only, weighted scoring, fraud detection, seller response rights) filters bad actors automatically. A poorly designed one (anyone can review, no verification, no moderation) invites manipulation and becomes worse than no reviews at all.
* **The regulatory line is binary: MERCHANT OF RECORD or NOT.** If your platform collects payment from the buyer and pays the seller, you are the merchant of record - responsible for sales tax, 1099-K, chargebacks, refunds, and AML. If the seller collects payment directly, you are a listing platform - lower regulatory burden but zero revenue from transactions. There is no middle ground. Choose before writing any payment code.
* **Marketplace liquidity is the only metric that predicts survival.** GMV, take rate, and revenue are outputs. Liquidity - the probability that a listing finds a buyer within X days - is the input. A marketplace with 90% fill rate at 5% take rate survives. A marketplace with 20% fill rate at 20% take rate dies, because supply churns when listings don't convert.


## When to Break Your Own Rules
<!-- STANDARD: 3min -->

* **Break the "supply first" rule when demand is the scarce resource.** In B2B procurement marketplaces, qualified buyers (enterprises with budget and authority) are scarcer than suppliers. Seed demand first - bring 10 enterprise buyers with committed spend, then onboard suppliers to meet their needs.
* **Break the "no off-platform" rule for high-trust, high-value B2B transactions where in-person meetings and contract negotiations are standard.** A marketplace for $100K industrial equipment deals needs different communication controls than a marketplace for $50 handmade crafts. Know when leakage prevention becomes deal friction.
* **Break the escrow rule for micro-transactions below $5 where escrow costs exceed dispute value.** For a marketplace of $1 digital goods, instant payout with buyer-protection insurance is more cost-effective than per-transaction escrow. The escrow cost (payment processing + holding cost) must be less than the dispute risk cost.

## When to Use
<!-- STANDARD: 3min -->

* Building a two-sided marketplace from scratch - product marketplace, service marketplace, rental/sharing platform, freelance/gig platform, B2B exchange, or classifieds platform
* Designing marketplace payment architecture - payment splitting (Stripe Connect), escrow, payout scheduling, multi-currency, refund and chargeback handling
* Solving the cold start problem - supply seeding strategy, single-city/niche launch, curated supply, exclusivity windows, subsidy design
* Implementing trust and safety systems - identity verification (KYC), review and rating integrity, dispute resolution workflows, fraud detection for listings and transactions
* Designing commission and fee architectures - percentage take rate, flat fees, tiered commissions, listing fees, subscription tiers, blended models
* Building marketplace search and discovery - full-text search with faceted filtering, relevance ranking, recommendation engines, location-based discovery
* Integrating booking and scheduling - availability calendars, time slot management, double-booking prevention, recurring availability, timezone handling
* Building in-platform messaging - real-time chat between parties, attachment sharing, off-platform communication prevention, message filtering
* Designing marketplace analytics - GMV tracking, take rate and net revenue, liquidity metrics (fill rate, time-to-match), cohort analysis by side, unit economics
* Navigating marketplace regulations - marketplace facilitator laws (sales tax), 1099-K reporting, platform liability (Section 230/DSA), INFORM Consumers Act compliance
* Don't use for single-vendor e-commerce stores - invoke website-builder
* Don't use for content creator platforms (Patreon-style) - invoke creator-economy-builder
* Don't use for ad-based aggregators (Craigslist-style) - invoke growth-engineer

## Route the Request
<!-- STANDARD: 3min -->


## Auto-Route by Artifacts (Check Filesystem First)
<!-- STANDARD: 3min -->

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("package.json", "stripe-connect" || "stripe.*connect" || "stripe.*express.*account")` | Stripe Connect detected -> Jump to **Core Workflow > Phase 2 (Payment Architecture)** |
| A2 | `file_contains("*", "marketplace" || "two-sided" || "multi-sided")` AND `file_contains("*.tsx||*.jsx||*.ts", "SearchBar" || "useSearch" || "MeiliSearch" || "Algolia" || "Elasticsearch")` | Search implementation detected -> Jump to **Decision Trees > Search Infrastructure** |
| A3 | `file_contains("*", "booking" || "scheduling" || "availability" || "time.slot" || "calendly" || "cronofy")` | Booking/scheduling detected -> Jump to **Decision Trees > Booking & Scheduling** |
| A4 | `file_contains("*.sql||*.prisma", "commission" || "take_rate" || "application_fee" || "payout" || "escrow")` | Payment splitting schema detected -> Jump to **Core Workflow > Phase 4 (Commission & Fees)** |
| A5 | `file_contains("*", "review" || "rating" || "dispute" || "verification" || "KYC" || "identity.*check")` AND `file_contains("*", "verified.*purchase" || "trust.*safety" || "fraud.*detection")` | Trust & safety detected -> Jump to **Decision Trees > Trust & Safety Systems** |
| A6 | `file_contains("*", "GMV" || "take.rate" || "liquidity" || "fill.rate" || "marketplace.*metrics")` | Marketplace analytics detected -> Jump to **Core Workflow > Phase 5 (Analytics)** |
| A7 | No marketplace-specific files found | New marketplace -> Go to **Intent Route** below |


## Intent Route (Ask the User)
<!-- STANDARD: 3min -->

```
What type of marketplace are you building?
|-- Product marketplace (Etsy-style - physical/digital goods exchange)
|   |-- Start at "Cold Start > Product Marketplace" then "Core Workflow > Phase 1"
|-- Service marketplace (Uber/Fiverr-style - labor/time exchange)
|   |-- Jump to "Decision Trees > Booking & Scheduling" then "Core Workflow > Phase 1"
|-- Rental/sharing platform (Airbnb-style - temporary access)
|   |-- Jump to "Decision Trees > Booking & Scheduling" then "Decision Trees > Insurance & Guarantees"
|-- Freelance/gig platform (Upwork-style - project-based services)
|   |-- Jump to "Core Workflow > Phase 2 (Payment Architecture)" for escrow + milestones
|-- B2B procurement exchange (wholesale/procurement - business buyers + business sellers)
|   |-- Start at "Cold Start > B2B Marketplace" then "Decision Trees > Commission Models > Tiered"
|-- Classifieds/listing platform (Craigslist-style - listings without embedded payments)
|   |-- Jump to "Decision Trees > Listing-Only Architecture" - understand revenue constraints
|-- Crowdfunding marketplace (Kickstarter-style - backers + creators)
|   |-- Jump to "Core Workflow > Phase 2" for escrow + all-or-nothing funding + payout logic
|-- Lead-gen marketplace (Thumbtack-style - qualified leads sold to service providers)
|   |-- Jump to "Decision Trees > Commission Models > Lead/Connection Fees"
|-- I have an existing marketplace with liquidity problems
|   |-- Jump to "Error Recovery > Liquidity Crisis" - diagnose supply-side vs demand-side churn
|-- I need to add payments to an existing listing platform
|   |-- Jump to "Core Workflow > Phase 2 (Payment Architecture)" - merchant of record decision
|-- I need trust & safety for an existing marketplace
|   |-- Jump to "Decision Trees > Trust & Safety Systems"
|-- I have no idea where to start -> Answer discovery questions below

Discovery Questions (when user has no marketplace idea specified):
1. "What exchanges hands? (physical goods / digital goods / services / temporary access / leads / money-for-equity)"
2. "Who are the two sides? Describe both: seller/supply (who provides value?) and buyer/demand (who pays?)"
3. "What's the average transaction value? (<$25 micro / $25-500 medium / $500-5,000 high / >$5,000 enterprise)"
4. "Where will you launch? (single city / single country / global from day one)"
5. "How will you acquire your first 100 listings/service providers?"
6. "What regulatory exposure are you willing to accept? (merchant of record = higher revenue & higher compliance / facilitator = lower revenue & lower compliance)"
```

## Core Workflow
<!-- STANDARD: 3min -->


## Phase 1: Cold Start & Supply Acquisition
<!-- STANDARD: 3min -->

**Goal: Reach minimum viable liquidity - the point where organic transactions happen without manual intervention.**

1. **SELECT LAUNCH STRATEGY BASED ON MARKETPLACE TYPE**

   Product marketplace (goods):
   * Single-city launch with curated supply: manually recruit 50-100 sellers in one city, verify inventory quality, launch to buyers in the same city only
   * Import existing supply: scrape/import listings from another platform (with permission or from public APIs), curate quality, invite original sellers to claim their listings
   * Fake-it-till-you-make-it: the platform itself lists inventory (buys wholesale, takes consignment), fulfills orders, transitions to 3P as sellers onboard

   Service marketplace (labor/time):
   * Subsidize supply: guarantee minimum earnings for first 100 providers (e.g., "$500/week guaranteed for first 4 weeks")
   * Exclusivity windows: sign top providers to 3-month exclusivity (they only list on your platform)
   * Time-boxed demand: launch for a specific event/dates (conference, festival, holiday) to create demand density

   Rental/sharing (temporary access):
   * Owner acquisition: identify owners through public records, forums, existing platforms. Offer professional photography, dynamic pricing tools, and guaranteed booking income
   * In-person onboarding: send platform representatives to photograph and verify first 50 properties/assets
   * Single-property-type launch: start with one category (e.g., vacation rentals in one neighborhood) before expanding

   B2B marketplace:
   * Anchor buyers first: sign 3-5 enterprise buyers with committed procurement budgets before onboarding any supplier
   * RFP-driven supply: buyers post requirements -> platform sources suppliers to fulfill specific RFPs
   * Industry event launch: launch at an industry trade show where both buyers and suppliers are physically present

2. **MEASURE LIQUIDITY - THE ONLY METRIC THAT MATTERS AT THIS STAGE**

   | Liquidity Metric | Product Marketplace | Service Marketplace | Rental/Sharing | B2B |
   |-----------------|--------------------|--------------------|----------------|-----|
   | Fill rate | % of listings that sell within 30 days | % of service requests that get fulfilled within 24 hours | % of available dates that get booked within 7 days | % of RFPs that receive >=3 qualified bids |
   | Target to survive | >40% | >50% | >30% | >60% |
   | Time-to-match | Days from listing to first inquiry | Minutes from request to first provider response | Days from listing to first booking | Days from RFP to first qualified bid |
   | Supply retention | % of sellers who list again after first sale | % of providers active in week 2, 4, 8 | % of owners who list again after first booking | N/A (relationship-based) |

3. **HARDEN AGAINST FRAUD FROM DAY ONE - NOT "LATER"**

   Even at 100 transactions/month, fraud will find you. Minimum defenses:
   * Identity verification: government ID + selfie liveness for any seller listing items >$100
   * Payment method verification: AVS (Address Verification) + CVV check for buyer payments
   * Velocity limits: max 3 listings/day for new sellers, max 5 transactions/day for new buyers
   * Manual review: first 10 transactions from any new seller are manually reviewed before payout


## Phase 2: Payment Architecture
<!-- STANDARD: 3min -->

**Goal: Implement payment splitting, escrow, and payout infrastructure that captures take rate automatically.**

1. **CHOOSE MERCHANT OF RECORD STRATEGY**

   ```
   MERCHANT OF RECORD (Platform collects payment, pays seller):
   |-- Stripe Connect - Standard accounts (platform controls onboarding, pricing)
   |   |-- Platform collects payment -> Stripe fee (2.9% + $0.30) + Application fee (your take rate)
   |   |-- Seller receives remainder: buyer_payment - Stripe_fee - app_fee
   |   |-- Payout: Instant (1% fee), 2-day standard, weekly/monthly scheduled
   |-- Stripe Connect - Express accounts (Stripe handles onboarding)
   |   |-- Simpler seller onboarding (Stripe-hosted), less platform control over pricing display
   |   |-- Good for: marketplaces where sellers don't need deep payout customization
   |-- Stripe Connect - Custom accounts (maximum control, white-labeled)
   |   |-- Good for: marketplaces with existing seller relationships and custom payout logic
   |-- Alternative processors: Adyen for Platforms, Mangopay, Hyperwallet, PayPal Commerce Platform

   FACILITATOR ONLY (Seller collects payment directly, platform charges listing/lead fee):
   |-- Platform never touches transaction funds -> no sales tax obligation, no 1099-K
   |-- Revenue model: listing fees, subscription, lead/connection fees (charged separately)
   |-- Risk: zero visibility into transaction success -> cannot verify take rate compliance
   ```

2. **IMPLEMENT ESCROW LOGIC**

   Escrow states: `AUTHORIZED -> CAPTURED -> HELD_IN_ESCROW -> RELEASED_TO_SELLER (or REFUNDED_TO_BUYER)`

   | Marketplace Type | Escrow Holding Period | Release Condition |
   |-----------------|----------------------|-------------------|
   | Product (physical goods) | Until delivery confirmed (tracking shows "delivered" + 48-hour buyer inspection window) | Auto-release 48h after delivery OR buyer confirms receipt |
   | Product (digital goods) | 24 hours from purchase | Auto-release after 24h unless dispute opened |
   | Service (standard) | Until service marked complete by buyer + 72h review period | Auto-release 72h after completion |
   | Service (milestone-based) | Per milestone - release milestone 1 payment on approval, hold milestone 2 | Each milestone released independently |
   | Rental | Until checkout + 48h for damage claims | Auto-release 48h after checkout unless damage claim filed |
   | B2B (>$5K) | Until goods/services accepted per contract terms | Manual release on buyer acceptance + signed delivery confirmation |

3. **PAYOUT SCHEDULING**

   * Standard: T+2 (2 business days after escrow release) - covers payment processing settlement
   * Instant payout: additional 1-1.5% fee passed to seller - for gig economy use cases
   * Scheduled: weekly (every Friday) or monthly (1st of month) - for established sellers who prefer batch reconciliation
   * Minimum payout threshold: $25 - prevents micro-payout processing costs exceeding payout value
   * Payout method hierarchy: ACH/bank transfer (free, 2-5 days) -> debit card push (1%, instant) -> international wire ($15-25)

4. **REFUND & CHARGEBACK HANDLING**

   * Refund window: defined per marketplace type (product: 14-30 days, service: dependent on completion, digital: 24-48h)
   * Chargeback reserve: hold 5-10% of seller payouts for 90 days to cover chargeback liability
   * Chargeback fee: $15-25 per chargeback (Stripe fee) + platform may charge additional - decide who bears this cost
   * Friendly fraud prevention: collect delivery confirmation, IP logs, communication history for dispute evidence


## Phase 3: Search & Discovery
<!-- STANDARD: 3min -->

**Goal: Build search infrastructure that maximizes match rate between supply and demand.**

1. **SEARCH STACK SELECTION**

   ```
   Transaction volume -> search engine:
   |-- <10K listings -> PostgreSQL full-text search (tsvector, tsquery) - zero operational overhead, good enough
   |   |-- Add pg_trgm extension for fuzzy/typo-tolerant search
   |-- 10K-500K listings -> Meilisearch (open-source, self-hosted) - fast, typo-tolerant, faceted filtering
   |   |-- Docker deploy, 50ms response times, simple API - best cost/performance for mid-scale
   |-- 500K-5M listings -> Algolia (managed, expensive) or Elasticsearch (self-hosted, complex)
   |   |-- Algolia: $1-3 per 1K search requests, 0 operational burden, typo-tolerant out of box
   |   |-- Elasticsearch: free self-hosted, steep learning curve, need DevOps for scaling
   |-- >5M listings -> Elasticsearch cluster (3+ nodes in different AZs), custom relevance tuning, ML-based ranking
   ```

2. **FACETED FILTERING ARCHITECTURE**

   Product marketplace facets: Category (taxonomy tree), Price range (bucketed), Condition (new/used/refurbished), Location (geospatial), Rating (star filter), Shipping (free shipping toggle), Brand, Availability (in stock)

   Service marketplace facets: Category, Price range (hourly/fixed), Rating, Location (proximity), Availability (date/time), Language, Response time, Verified badge

   Rental facets: Property type, Price range (per night), Location (map boundary), Amenities (multi-select), Rating, Instant book, Superhost/verified, Cancellation policy

3. **RELEVANCE RANKING SIGNALS**

   | Signal | Weight | Rationale |
   |--------|--------|-----------|
   | Text relevance (TF-IDF/BM25) | Base score | Query match against title, description, tags |
   | Seller rating | 0.8-1.2x multiplier | High-rated sellers boosted, low-rated demoted |
   | Freshness | +10% for <24h old | Fresh listings get temporary boost for discovery |
   | Conversion rate | +5-15% | Listings with higher click-to-book/purchase rate ranked higher |
   | Response time | +0-10% | Sellers who respond in <1 hour boosted |
   | Price competitiveness | +0-5% | Listings priced within 20% of median boosted |
   | Location proximity | +0-30% | For location-based marketplaces - closer = higher |
   | Sponsored/promoted | Paid boost | Clearly labeled as "Sponsored" - separate from organic ranking |

4. **RECOMMENDATION ENGINE (post-MVP)**

   * Collaborative filtering: "Buyers who viewed this also viewed..." - requires transaction volume (min 1K transactions)
   * Content-based: "Similar to items you've purchased/viewed" - works from day one if listing metadata is rich
   * Location-based: "Popular in your area" - geospatial clustering of transaction data
   * Cold-start recommendations (new user): top sellers by category + location, curated collections, trending now


## Phase 4: Commission & Fee Architecture
<!-- STANDARD: 3min -->

**Goal: Design revenue model that maximizes platform revenue without destroying marketplace equilibrium.**

1. **COMMISSION MODEL SELECTION**

   ```
   |-- Percentage take rate (e.g., 15% per transaction)
   |   |-- Best for: product marketplaces with wide price ranges (Etsy: 6.5%, Airbnb: 14-16% host fee)
   |   |-- Pros: scales with transaction value, simple to understand
   |   |-- Cons: high-value transactions feel expensive, sellers seek to bypass
   |-- Flat fee per transaction (e.g., $2.99 per booking)
   |   |-- Best for: high-volume, uniform-price transactions (rideshare, food delivery)
   |   |-- Cons: low-value transactions become unprofitable; high-value underpriced
   |-- Tiered commissions (e.g., 15% on first $10K, 10% on $10K-50K, 5% on $50K+)
   |   |-- Best for: B2B, freelance platforms - volume discounts incentivize seller loyalty
   |   |-- Cons: more complex to implement, sellers may split into multiple accounts to reset tier
   |-- Listing fees (e.g., $0.20 per listing)
   |   |-- Best for: classifieds, high-volume/low-value listings (eBay insertion fees)
   |   |-- Cons: discourages listing volume, creates upfront cost before revenue
   |-- Subscription tiers (e.g., $29/mo Basic, $99/mo Pro, $299/mo Enterprise)
   |   |-- Best for: B2B procurement, specialized service marketplaces
   |   |-- Cons: decouples revenue from transaction value, may not capture platform's full value
   |-- Lead/connection fees (e.g., $5-50 per qualified lead sent to service provider)
   |   |-- Best for: service marketplaces where transaction happens offline (Thumbtack, HomeAdvisor)
   |   |-- Cons: providers pay even if lead doesn't convert -> churn risk if lead quality is poor
   |-- Blended model (e.g., subscription + reduced take rate, or listing fee + transaction fee)
       |-- Best for: mature marketplaces optimizing for both retention and revenue
   ```

2. **FEE PSYCHOLOGY**

   * Buyer fees vs seller fees: charging buyers (Airbnb: 14% guest service fee) reduces sticker shock for sellers but increases total price; charging sellers (Etsy: 6.5% transaction fee) keeps buyer prices lower but may drive seller churn
   * Fee transparency: showing "Platform fee: $3.50" as a line item reduces trust; bundling into total price reduces fee salience but may violate consumer protection laws in some jurisdictions
   * Fee anchoring: new marketplace should price BELOW the established player's rate - you're providing less liquidity, so you should charge less. Increase rate as liquidity grows.

3. **REVENUE RECONCILIATION**

   * Per-transaction ledger: `transaction_id | buyer_paid | stripe_fee | platform_commission | seller_payout | stripe_payout_fee | seller_net`
   * Daily reconciliation: sum of platform commissions must match Stripe application fee report
   * Monthly close: GMV (sum buyer_paid), Gross Revenue (sum platform_commission), Net Revenue (Gross - chargebacks - refunds - payment processing fees on platform portion)
   * Seller 1099-K eligibility: >$5,000 in gross payments AND >200 transactions in 2024 (threshold phasing down)


## Phase 5: Analytics & Growth
<!-- STANDARD: 3min -->

**Goal: Instrument marketplace metrics to measure liquidity, identify churn, and optimize for profit.**

1. **CORE MARKETPLACE METRICS DASHBOARD**

   | Metric | Formula | Healthy Range | Red Flag |
   |--------|---------|---------------|----------|
   | GMV (Gross Merchandise Volume) | Sum of all transaction values in period | Growing MoM at >5% | Negative MoM growth |
   | Take Rate | Platform Revenue / GMV | 5-25% (depends on marketplace type) | Declining QoQ - fee leakage |
   | Net Revenue | GMV x Take Rate - Chargebacks - Refunds - Payment Fees | >70% of Gross Revenue | <50% - payment costs eating margin |
   | Fill Rate (Liquidity) | Listings that result in transaction / Total listings | >40% (product), >50% (service) | <20% - supply churn imminent |
   | Time-to-Match | Days from listing to first transaction | Declining over time | Increasing - supply/demand mismatch |
   | Supply-Side CAC | Total supply acquisition cost / New active sellers | Depends on seller LTV | CAC > 12-month seller LTV |
   | Demand-Side CAC | Total demand acquisition cost / New transacting buyers | Depends on buyer LTV | CAC > 6-month buyer LTV |
   | Supply Churn | Sellers inactive 30+ days / Total sellers | <5% monthly | >10% - systemic problem |
   | Demand Churn | Buyers no transaction in 90 days / Total buyers | <10% monthly | >20% - trust or value problem |
   | Dispute Rate | Disputed transactions / Total transactions | <2% | >5% - systemic trust or quality problem |
   | Chargeback Rate | Chargebacks / Total transactions | <0.5% | >1% - merchant account at risk |

2. **COHORT ANALYSIS BY SIDE**

   * Supply cohort: sellers onboarded in month M - track: listings in month M+1, M+2, M+3; transactions completed; revenue generated; churn date. Identify: what separates M+12 active sellers from M+1 churn?
   * Demand cohort: buyers acquired in month M - track: repeat purchase rate in M+1, M+2, M+3; AOV (average order value) trend; lifetime value (LTV). Identify: what triggers the second purchase?

3. **UNIT ECONOMICS PER TRANSACTION**

   ```
   Revenue per transaction: Buyer price x Take rate = Platform commission (e.g., $100 x 15% = $15.00)
   Cost per transaction:
     Payment processing: 2.9% + $0.30 on full amount (e.g., $100 x 2.9% + $0.30 = $3.20)
     Hosting/infrastructure: negligible at scale (~$0.001 per transaction)
     Customer support: $1-5 per transaction (depends on automation)
     Fraud/chargeback reserve: 1-3% of transaction value
     Insurance/guarantees: 0.5-2% of transaction value
   Net profit per transaction: $15.00 - $3.20 - $0.001 - $2.00 - $1.50 - $0.50 = $7.80 per $100 transaction
   ```

## Decision Trees
<!-- STANDARD: 3min -->

### Decision Tree 1: Trust & Safety Architecture

        ┌── INPUT: What's the transaction value per order?
        │
   ┌────┼────────────┐
   │    │            │
   ▼    ▼            ▼
[<$50] [$50-$500]   [>$500]
   │    │            │
   ▼    ▼            ▼
Light:   Medium:     Heavy:
email    ID verify   Escrow +
verify   + phone     3D Secure
* basic  verify +    + manual
review   dispute     review
system   resolution  + insurance
         workflow    option

### Decision Tree 2: Commission & Fee Architecture

        ┌── INPUT: Who pays the platform fee?
        │
   ┌────┼────────────────────┐
   │    │                    │
   ▼    ▼                    ▼
[Buyer [Seller              [Both sides]
only]  only]
   │    │                    │
   ▼    ▼                    ▼
Service Buyer fee            ┌── Supply-constrained?
fee on  on top of            │
top of  seller price     ┌───┴───┐
seller  (Booking.com        │         │
price   model, 15-20%)      ▼         ▼
(Uber,                      [Yes]     [No]
DoorDash,                   │         │
25-30%)                     ▼         ▼
                         Charge     Charge
                         buyers     sellers
                         more       more
                         (demand    (supply-
                         side       side
                         subsidy)   subsidy)

### Decision Tree 3: Supply vs Demand Acquisition Priority

        ┌── INPUT: Which side is the bottleneck today?
        │
   ┌────┴────────────────────┐
   │                         │
   ▼                         ▼
[Supply scarce:           [Demand scarce:
few sellers/              few buyers/
providers]                 orders]
   │                         │
   ▼                         ▼
Demand-first               Supply-first
strategy:                  strategy:
1. Aggregate buyers        1. Recruit providers
   (waitlist, letters)         with guarantees
2. Use committed demand    2. Offer exclusivity
   to recruit supply           bonuses
3. Launch with liquidity   3. Subsidize early
   from day 1                  transactions


## Marketplace Type Selection
<!-- STANDARD: 3min -->

```
What exchanges hands?
|-- Physical or digital goods -> PRODUCT MARKETPLACE
|   |-- Handmade/unique -> Etsy-style (seller-driven, discovery-focused)
|   |-- Commodity/standardized -> Amazon Marketplace-style (price-driven, volume-focused)
|   |-- Collectibles/luxury -> StockX-style (authentication-required, bid/ask)
|   |-- Digital assets -> Creative Market-style (instant delivery, no shipping)
|-- Labor or time -> SERVICE MARKETPLACE
|   |-- Standardized task -> Uber-style (instant fulfillment, pricing set by platform)
|   |-- Skilled project -> Upwork-style (proposal-based, escrow + milestones, platform facilitates match)
|   |-- Micro-task -> Fiverr-style (fixed-price gigs, seller-defined packages)
|   |-- Professional service -> Thumbtack-style (lead-gen, platform sells qualified leads)
|-- Temporary access to asset -> RENTAL/SHARING
|   |-- Accommodation -> Airbnb-style (calendar-based, location-driven, review-critical)
|   |-- Vehicle -> Turo-style (insurance-heavy, condition documentation critical)
|   |-- Equipment/gear -> Fat Llama-style (lower value, quicker turnover)
|-- Business-to-business -> B2B MARKETPLACE
|   |-- Raw materials/commodities -> Alibaba-style (bulk, RFQ-driven, long sales cycles)
|   |-- Wholesale finished goods -> Faire-style (curated, net terms, reorder-driven)
|   |-- Services/procurement -> Upwork Enterprise-style (managed, compliance-heavy)
|-- Qualified leads (not transactions) -> LEAD-GEN MARKETPLACE
|   |-- Platform doesn't transact - sells leads to service providers (Thumbtack, HomeAdvisor, Angi)
|-- Money for future delivery/equity -> CROWDFUNDING
    |-- Reward-based -> Kickstarter-style (all-or-nothing, product pre-sale)
    |-- Equity -> Wefunder/SeedInvest-style (compliance-heavy, accredited investor rules)
    |-- Donation -> GoFundMe-style (no tangible return, trust and story-driven)
```


## Cold Start Strategy Selection
<!-- STANDARD: 3min -->

```
How much time do you have?
|-- < 3 months -> Curated supply (fake-it-till-you-make-it)
|   |-- Platform buys inventory/fulfills demand directly
|   |-- Pros: instant liquidity, full quality control
|   |-- Cons: capital-intensive, doesn't prove marketplace model (you're a retailer)
|-- 3-6 months -> Single-city + exclusivity
|   |-- Recruit top 20% of supply in one city, offer exclusivity bonuses
|   |-- Pros: proves model with minimal capital, creates density
|   |-- Cons: doesn't prove scalability across cities
|-- 6-12 months -> Demand-first + supply follows
|   |-- Aggregate demand (waitlist, crowdfunding, letter of intent) -> recruit supply to fulfill
|   |-- Best for B2B: sign 3 enterprise buyers -> onboard suppliers to meet their needs
|   |-- Pros: supply acquisition is demand-justified, higher conversion
|-- >12 months -> Build community + convert to marketplace
    |-- Start as content/community platform, build audience, add marketplace layer
    |-- Pros: audience-building derisks demand; Cons: slow, community may resist commercialization

Supply seeding tactics ranked by effectiveness:
1. Pay first 100 sellers a guaranteed minimum (e.g., $500/week for 4 weeks) - 60-80% retention
2. Scrape public listings from existing platforms, list on your platform, invite original seller to claim - 30-50% claim rate
3. In-person recruitment at industry events/trade shows - 20-40% conversion to active seller
4. Cold email/LinkedIn outreach to existing sellers on competitor platforms - 5-15% conversion
5. SEO/content marketing to attract sellers organically - 1-3% conversion, but compounds over time
```


## Trust & Safety Systems
<!-- STANDARD: 3min -->

```
Trust stack - from account creation to dispute resolution:

|-- IDENTITY VERIFICATION (Prevent fake accounts)
|   |-- Tier 1 (all users): Email + phone verification
|   |-- Tier 2 (sellers >$100 items, service providers): Government ID + selfie liveness check
|   |-- Tier 3 (sellers >$1K items, B2B suppliers): Business verification, tax ID, DUNS number
|   |-- Providers: Stripe Identity, Onfido, Jumio, Persona - $1-3 per verification

|-- REVIEW & RATING SYSTEM (Surface quality, filter bad actors)
|   |-- Verified purchase only: buyer must have completed transaction with that seller
|   |-- Double-blind: neither party sees the other's review until both submitted (prevents retaliation)
|   |-- Weighted scoring: recency (60-day half-life), reviewer credibility, transaction value
|   |-- Seller response rights: seller can publicly respond to any review (one response only)
|   |-- Anti-gaming: velocity checks, IP overlap detection, text similarity clustering, sentiment-to-star mismatch
|   |-- Review removal policy: only for TOS violations (hate speech, personal info, proven false claims) - never remove just because seller dislikes a legitimate negative review

|-- FRAUD DETECTION (Prevent financial loss)
|   |-- Listing fraud: stolen photos (reverse image search), underpriced luxury goods (<50% market value), duplicate listings
|   |-- Payment fraud: stolen credit cards, card testing ($0 -> $1 -> $5 pattern), BIN-country mismatch
|   |-- Account takeover: new device + new IP + changed payout method = high risk
|   |-- Collusion: buyer + seller same IP, same device fingerprint, circular transactions
|   |-- Friendly fraud (1st party): buyer claims "item not received" but tracking shows delivery; buyer claims "not as described" but listing photos match - behavioral pattern analysis

|-- DISPUTE RESOLUTION (Resolve conflicts fairly)
|   |-- Level 1 - Automated: clear-cut cases (tracking shows not delivered = auto-refund)
|   |-- Level 2 - Mediation: platform reviews both sides' evidence, proposes resolution within 72h
|   |-- Level 3 - Arbitration: binding decision by platform, funds released accordingly
|   |-- Appeal: final review by senior team if new evidence emerges

|-- INSURANCE & GUARANTEES (Absorb residual risk)
    |-- Buyer protection: "If item doesn't arrive or isn't as described, we'll refund you" - platform-backed guarantee
    |-- Seller/host protection: property damage (Airbnb Host Guarantee: $1M), liability insurance for service providers
    |-- Implementation: platform self-insures up to $X per claim, purchases excess insurance from Lloyd's/Hartford for catastrophic claims
```


## Payment Architecture Decision Tree
<!-- STANDARD: 3min -->

```
Merchant of Record decision - this determines your regulation, revenue model, and risk:

|-- MERCHANT OF RECORD (Platform collects payment, pays seller)
|   WHEN: you want to capture take rate automatically, provide escrow, control dispute resolution
|   REGULATION: responsible for sales tax (marketplace facilitator laws), 1099-K, chargeback liability, AML
|   IMPLEMENTATION: Stripe Connect with Standard/Express/Custom accounts
|   REVENUE: automatic - application fee deducted before payout
|   RISK: chargeback liability, sales tax remittance in 45+ US states, 1099-K filing
|   BEST FOR: product marketplaces, service marketplaces, rental platforms - any marketplace where transaction value justifies compliance cost
|
|-- FACILITATOR ONLY (Seller collects payment, platform charges fee separately)
    WHEN: transaction values are very low (<$25), transactions are offline, or regulatory complexity exceeds revenue
    REGULATION: no sales tax obligation, no 1099-K, limited chargeback liability
    IMPLEMENTATION: Stripe Billing (subscription), Stripe Invoicing (per-listing/per-lead)
    REVENUE: separate from transaction - listing fees, subscription, lead fees (charged monthly or per lead)
    RISK: revenue leakage is inevitable - no visibility into actual transaction values; sellers under-report
    BEST FOR: classifieds, lead-gen, very early-stage marketplaces not ready for regulatory burden

Escrow decision tree:
|-- Product (physical): Hold until delivery confirmed (tracking "delivered" + 48h buyer inspection window)
|-- Product (digital): Hold 24 hours (enough to detect broken/fraudulent files, short enough for seller cash flow)
|-- Service (time-based): Hold until service completion marked by buyer
|-- Service (milestone-based): Hold per-milestone, release each on buyer approval
|-- Rental: Hold until checkout + 48h damage claim window
|-- B2B (>$5K): Hold until goods/services accepted per contract - up to 30 days for enterprise deals
```


## Booking & Scheduling Architecture
<!-- STANDARD: 3min -->

```
Availability model:
|-- Recurring (service providers with weekly schedule): "Available Mon-Fri 9am-5pm"
|   |-- Schema: provider_id | day_of_week | start_time | end_time | timezone
|   |-- Exception handling: override for specific dates (holidays, PTO)
|-- Calendar-based (rentals, event spaces): specific dates available/unavailable
|   |-- Schema: listing_id | date | status (available/booked/blocked) | price
|   |-- Bulk operations: set availability for date ranges, seasonal pricing
|-- Real-time (rideshare, on-demand): providers toggle online/offline, geo-location tracked

Double-booking prevention:
|-- Pessimistic locking: SELECT ... FOR UPDATE on time slot row during booking transaction
|-- Atomic booking: INSERT booking with UNIQUE constraint on (listing_id, date) or (provider_id, start_time, end_time)
|-- Webhook verification: before confirming, re-check availability via API call (belt-and-suspenders)

Buffer time: N minutes between bookings (for travel, cleanup, preparation)
|-- Configurable per provider: default 15min, providers can increase
|-- Does not count as "available time" - prevents back-to-back booking disasters

Timezone handling:
|-- Store all times in UTC, convert to user's local time for display
|-- Provider sets availability in their local timezone (stored as UTC with timezone reference)
|-- Display booking times in buyer's timezone with original timezone annotation ("10:00 AM PST / 1:00 PM EST")
```


## Messaging Architecture
<!-- STANDARD: 3min -->

```
In-platform messaging stack:
|-- Real-time (service marketplaces where timing matters): Firebase Realtime DB, Ably, Pusher
|   |-- WebSocket connection with automatic reconnection, message queuing for offline receivers
|   |-- Typing indicators, read receipts (delivered -> read), online/offline presence
|-- Async (product/rental marketplaces): database-backed messaging (PostgreSQL + polling or SSE)
|   |-- Simpler to implement, sufficient for use cases where real-time isn't critical
|   |-- Email/push notification on new message - no need for persistent socket connection

Off-platform leakage prevention:
|-- Regex filter: block patterns matching phone numbers, email addresses, social media handles
|   |-- Phone regex: \\b(\\+\\d{1,3}[-.]?)?\\(?\\d{3}\\)?[-.]?\\d{3}[-.]?\\d{4}\\b
|-- ML classifier: BERT-based text classifier trained on "this is a phone number/email/off-platform request"
|-- Progressive enforcement:
|   |-- First message containing contact info: soft block (message not sent, user sees "To keep you safe, please keep communication on [Platform]")
|   |-- Second attempt: warning with educational content
|   |-- Third attempt: temporary message restriction + account flag for manual review
|-- URL whitelist: allow only approved domains (yours, payment processor, scheduling tool) in messages
|-- Incentive alignment: "Transactions completed on-platform are protected by our $X Buyer Guarantee and Seller Protection"

Message templates for service providers:
|-- Quick replies: "Yes, I'm available," "What time works for you?", "Here's my proposal - [link]"
|-- Attachment support: photos, PDFs, contracts - all scanned for malware, PII redacted
|-- Post-transaction window: messages open for 14 days after transaction for follow-up, then close
```


## Commission Model Decision Matrix
<!-- STANDARD: 3min -->

```
| Marketplace Type      | Best Model        | Typical Range    | Rationale                                          |
|-----------------------|-------------------|------------------|---------------------------------------------------|
| Product (Etsy-style)  | Percentage        | 5-15%            | Scales with value, simple, industry standard        |
| Product (eBay-style)  | Listing + %       | $0.35 + 13.25%   | Listing fee discourages junk, % captures value      |
| Service (Uber-style)  | Percentage        | 20-30%           | Platform sets price, high value-add (dispatch, nav) |
| Service (Upwork-style)| Tiered percentage | 20% -> 10% -> 5% | Volume discounts incentivize long-term relationships|
| Service (Thumbtack)   | Per-lead fee      | $5-50 per lead   | Transaction happens offline, platform monetizes match|
| Rental (Airbnb-style) | Split fee         | 3% host + 14% guest| Both sides pay - host for listing, guest for service|
| B2B (Faire-style)     | Percentage        | 15-25% first order, 0% reorder| Take rate on discovery, free on retention  |
| B2B (Alibaba-style)   | Subscription      | $299-999/yr      | High-value, low-frequency transactions             |
| Freelance (Fiverr)    | Percentage        | 20%              | Standardized gigs, platform handles payment + delivery|
| Crowdfunding          | Percentage        | 5% + 3-5% payment| All-or-nothing model, platform fee + payment fee    |
| Classifieds           | Freemium          | $0 basic / $9.99 featured| Free listings, paid promotion + visibility      |
```

## Gotchas - Dollar-Quantified Marketplace Footguns
<!-- STANDARD: 3min -->


## Cold Start Gotchas
<!-- STANDARD: 3min -->

* **Launching city-wide when you can't dominate a neighborhood.** A marketplace with 5 restaurants in Manhattan + 5 in Brooklyn + 5 in Queens has 15 total listings but zero density anywhere. A delivery marketplace needs 10+ restaurants per delivery zone for reasonable delivery times. Density beats breadth - every time. **Total cost: $200K-$500K in demand acquisition burned on a marketplace where no buyer finds enough supply to transact. The "launch in a city" fallacy: a city is not a market - a neighborhood is.**

* **Paying for supply without exclusivity.** Guaranteeing $500/week to providers who also work on competitor platforms means you're subsidizing their multi-homing. By week 4, they've taken $2,000 from you and fulfilled most requests on the competitor (because that's where demand is). Supply incentives must include exclusivity: "We guarantee $500/week for 4 weeks IF you are exclusive to our platform during that period." **Total cost: $50K-$200K in wasted supply subsidies - you paid their rent while they worked for Uber.**

* **Assuming early adopters will tolerate low liquidity.** Early adopters are more forgiving than mainstream users - but only for 2-4 weeks. After that, a buyer who searches three times and finds nothing each time is gone forever. The "early adopter patience" window is measured in weeks, not months. **Total cost: $0 in revenue but irreversible - every early adopter who leaves due to low liquidity tells 5-10 people "I tried [Platform], there was nothing there." Reputation damage compounds.**


## Trust & Safety Gotchas
<!-- STANDARD: 3min -->

* **Review gating by transaction value - the "my first transaction was $0.99" attack.** Fraudster buys 50 low-value items from their own seller account ($49.50 total), leaves 50 5-star reviews. Seller now has a perfect 5.0 rating and 50 "verified" reviews. Lists $5,000 item - buyers trust the rating because "All reviews are from verified purchases!" **Fix: Weight review scores by transaction value - a $0.99 review has 0.01x weight, a $500 review has 1.0x weight. Also: same-payment-method detection (one credit card used for all reviews = collusion signal). Total cost: $50K-$500K in fraud losses from review-manipulated scam listings.**

* **Dispute resolution is your cost center, not your profit center - but under-investing costs more.** A marketplace handling 1,000 transactions/month at $100 AOV (=$100K GMV, $15K take rate at 15%) will have ~30 disputes (3% rate). Manual dispute resolution costs $10-25 per dispute in support labor = $300-750/month. Under-invest in resolution (no dedicated team, slow response, no clear policy) -> dispute escalation rate doubles -> chargeback rate triples -> merchant account threatened. **Total cost: $2K-5K/month in additional chargeback fees + risk of Stripe account termination (existential for marketplace) vs $300-750/month in proper dispute resolution staffing.**

* **Identity verification friction kills conversion - but too little invites fraud.** A marketplace with 10-step KYC will onboard zero sellers. A marketplace with email-only verification will onboard 100% fraudsters within a month. **The equilibrium: Tier 1 (email + phone) for listing access. Tier 2 (ID + selfie) before first payout. Tier 3 (business docs) at $1K/month earnings. Total cost of getting this wrong: 0% conversion at Tier 3 upfront -> wasted $50K in seller acquisition; or fraud rate >5% -> merchant account termination.**


## Payment Architecture Gotchas
<!-- STANDARD: 3min -->

* **Stripe Connect application fee cannot exceed the payment amount.** A $5 transaction with a 20% take rate = $1.00 application fee. That works. But if you charge a $2.00 flat fee on a $5 payment, Stripe rejects it - application fee > payment amount. **Fix: For flat-fee models with low transaction values, use separate platform charges (Stripe Billing) or minimum transaction size enforcement. Total cost: 5-10% of micro-transactions silently failing in production before anyone notices.**

* **Currency conversion in multi-currency marketplaces is a hidden margin killer.** A UK buyer pays GBP 100. Stripe converts to seller's USD at Stripe's rate (2% above mid-market) + Stripe's 1% international fee = 3% total. If your take rate is 5%, 3% of it is gone to FX before you touch it. **Fix: (a) Require same-currency transactions where possible, (b) Pass FX cost to one side explicitly, (c) Hold multi-currency balances to batch-convert (Wise/Stripe multi-currency accounts). Total cost: 1-3% of cross-border GMV lost to unaccounted FX spread.**

* **1099-K chaos - issuing 500 paper 1099-Ks manually in January.** Marketplace facilitator laws require you to issue 1099-K to any seller exceeding the reporting threshold. Even if you use Stripe (which issues 1099-K for Standard accounts), you must still file with the IRS and state. Miss a filing deadline = $60 per form penalty (up to $630/return) + interest. 500 forms x $60 = $30,000 in penalties. **Fix: Automate 1099-K generation via Stripe's 1099-K product or a third-party service like Track1099/Tax1099. Total cost of getting this wrong: $30K-$300K in IRS penalties.**


## Search & Discovery Gotchas
<!-- STANDARD: 3min -->

* **PostgreSQL full-text search with 50K listings returns results in 800ms - buyers bounce.** PostgreSQL `tsvector` + GIN index works beautifully at 5K listings (30ms response). At 50K, without tuning, queries can hit 500-800ms. At 500K, they fail. The cliff is real and sudden. **Fix: Plan search infrastructure migration at 10K listings (not 50K). Have Meilisearch or Elasticsearch running in shadow mode from 5K listings so the migration is a one-line config change, not a crisis. Total cost: 20-40% drop in conversion rate during the "slow search" period - easily $50K-$200K in lost GMV.**

* **Category taxonomy without hierarchy collapses at 500 categories.** A flat category list of 500 items is unusable - buyers cannot browse, sellers cannot classify, search facets become noise. **Fix: Hierarchical taxonomy (3-level max): Category > Subcategory > Item Type. "Electronics > Audio > Headphones" rather than a flat "Headphones" tag. Plan taxonomy before onboarding first 100 sellers - retrofitting taxonomy after 10K listings requires reclassifying everything. Total cost of retrofitting: $20K-$50K in data labeling + 2-4 months of degraded search.**


## Booking & Scheduling Gotchas
<!-- STANDARD: 3min -->

* **Race condition: two buyers book the same time slot within 200ms of each other.** Without database-level atomicity, both see "Available," both click Book, both get confirmation - and one is a double-booking that becomes a customer service disaster. **Fix: Database-level atomic booking: INSERT with UNIQUE constraint on (listing_id, date). If the INSERT fails (constraint violation), second buyer sees "Sorry, this slot was just booked." No application-level check is sufficient. Total cost of one double-booked Airbnb: $500-$2,000 in re-accommodation + negative reviews + platform credit compensation.**

* **Timezone bugs create bookings that start before they were made.** Provider in PST sets availability 9 AM - 5 PM PST. Buyer in EST books a 4 PM slot, which is 1 PM PST - valid. But if the system displays the wrong timezone, provider expects buyer at 4 PM PST (7 PM EST) - 3 hours late. **Fix: Store all times in UTC. Every display function accepts a timezone parameter. Total cost of timezone bugs: 10-20% of bookings have at least one party show up at the wrong time, causing 1-3% avoidable dispute rate.**

## Error Recovery - Explicit Step-by-Step
<!-- STANDARD: 3min -->


## When the Cold Start Is Failing
<!-- STANDARD: 3min -->

* **Symptom:** Supply side has <20% utilization after 4 weeks, demand side sees mostly empty search results.
    * **Step 1: Stop demand acquisition immediately.** Every paid click from a buyer who finds nothing is wasted. Pause all ads, SEO, and demand-gen.
    * **Step 2: Diagnose root cause.** Is the problem supply quantity (not enough listings) or supply quality (listings exist but are poor photos, wrong prices, outdated availability)? Query: fill rate = transactions / searches with intent. If fill rate >10% but <20%, the problem is supply quantity. If fill rate <5%, check listing quality.
    * **Step 3: If supply quantity -> go curated.** Platform buys or creates 50-100 high-quality seed listings. For a product marketplace: purchase inventory yourself and list it. For a service marketplace: hire freelancers on other platforms to fulfill demand on yours (yes, this is "fake it till you make it"). For a rental marketplace: approach 20 property owners directly with revenue guarantees.
    * **Step 4: If supply quality -> create a listing playbook.** Audit the top 10 performing listings on competitor platforms. Create a template: minimum 5 photos, required fields, suggested price range, recommended description structure. Build an onboarding wizard that guides sellers through creating a competitor-quality listing.
    * **Step 5: Run a 14-day "demand surge" experiment.** With improved supply, restart demand acquisition at 25% previous budget. Monitor fill rate daily. If fill rate >20% consistently for 7 days, scale demand. If fill rate remains <10%, your unit economics or value proposition is fundamentally broken - go back to Phase 1 (Cold Start) and reassess.

* **Symptom:** Take rate < 2% (below Stripe's processing fee - you lose money on every transaction).
    * **Step 1: Verify your transaction math.** Take rate = platform net revenue / GMV. Platform net revenue = the amount your platform actually keeps after payment processing, refunds, chargebacks. If your listed take rate is 10% but your net take rate is 2%, you have a leakage problem.
    * **Step 2: Audit the gap.** Where is the 8% going? Payment processing (2.9% + $0.30), refunds (2%), chargebacks (0.5%), FX conversion (1-2%), Stripe Connect account fees ($2/month per active account = $0.50-1.00/transaction at low volume)? Quantify every leakage point.
    * **Step 3: Fix structural leakage.** (a) Switch Connect account type from Express ($2/month/account) to Custom (per-transaction pricing) if your sellers do >5 transactions/month. (b) Implement refund waiting period (funds held 5 business days before payout - reduces friendly fraud refunds by 30%). (c) Use Stripe Radar with custom rules for your marketplace to reduce chargebacks.
    * **Step 4: If structural fixes bring take rate to 3-5% but you need 8%+ -> increase take rate or add revenue streams (seller subscription tiers, promoted listings, premium features).**

* **Symptom:** Fraud rate exceeds 1% of transactions.
    * **Step 1: Freeze all payouts for accounts flagged in last 48 hours.** Better to delay 50 legitimate payouts by 24 hours than process 1 fraudulent payout = permanent loss.
    * **Step 2: Categorize fraud.** Payment fraud (stolen cards) vs listing fraud (fake items) vs collusion (synthetic accounts). Each type requires different controls. Run: transactions WHERE payment_dispute = true OR seller_account_age < 7 days OR buyer_account_age < 3 days OR transaction_value > 3x user_average.
    * **Step 3: Implement real-time rules.** For payment fraud: block transactions where billing country != shipping country AND transaction value > $200. For listing fraud: flag listings where price < 50% of category median. For collusion: flag users where IP address overlap between buyer and seller.
    * **Step 4: Raise verification gates.** Increase ID verification requirement threshold from $1,000 cumulative earnings to $100 cumulative earnings for new sellers. Add 48-hour payout delay for new accounts. Require tracking number for shipments > $100.
    * **Step 5: Post-incident review.** Every fraud case answer: "How did this user pass our verification? Why didn't our rules catch this? What one rule would have prevented this specific case?"

## Verification
<!-- STANDARD: 3min -->

| # | Complete when... | Verify |
|---|-----------------|--------|
| ☐ | Complete when Trust & safety: new user completes ID verification and lists item in < 15 minutes; fraudulent listing auto-detected | Test with legitimate user flow; inject stolen-photo + below-market listing → auto-flagged |
| ☐ | Complete when Payment flow end-to-end: buyer pays → escrow → seller fulfills → buyer confirms → funds released | Full flow test including 48h inspection window, refund branch, chargeback simulation |
| ☐ | Complete when Double-booking prevention: 10 concurrent requests for same slot → exactly 1 succeeds, 9 receive "unavailable" | Load test with concurrent booking; test under production-like conditions |
| ☐ | Complete when Messaging security: phone numbers, emails, social handles blocked in messages | Test: "555-123-4567", "user@gmail.com", "@username" → all rejected |
| ☐ | Complete when Review system integrity: only transaction parties can review; double-blind until both submitted; one review per transaction | Test: non-party review attempt → rejected; retaliatory review before seeing other → blocked |
| ☐ | Complete when Payout correctness: seller with $1,000 at 10% take rate receives exactly $900 (minus processing) | Test with actual Stripe Connect test accounts; verify to 2 decimal places |
| ☐ | Complete when Dispute resolution: buyer files dispute → seller responds within 48h → platform mediates → resolution within SLA | Simulate 3 dispute scenarios (item not received, not as described, damaged); verify timeline |
| ☐ | Complete when Search quality: top 10 results for category query contain > 80% relevant listings | Test 20 common search queries; measure precision@10; verify no empty results for populated categories |
| ☐ | Complete when Escalation path: automated rules → manual review queue → platform decision → appeal process | Walk through escalation: flagged listing → reviewer action → notification → appeal flow |
| ☐ | Complete when Platform fee transparency: fee breakdown visible before listing publish and at transaction completion | Verify fee calculator; receipt shows gross, platform fee, processing fee, net for both sides |

## Verification Guardrails - Binary Deployment Checklist
<!-- STANDARD: 3min -->

Before deploying or shipping any marketplace feature, verify **every one** of these:

* [ ] **Trust & safety pass:** Can a first-time user complete ID verification and list an item within 15 minutes? Can a fraudulent listing (stolen photos + below-market price) be detected by automated rules before going public?
* [ ] **Payment flow end-to-end:** Buyer pays -> funds held in escrow -> seller fulfills -> buyer confirms -> funds released to seller. Test the FULL flow including the 48-hour inspection window, refund branch, chargeback simulation.
* [ ] **Double-booking prevention:** Run concurrent booking test - 10 simultaneous requests for the same time slot on the same listing. Exactly 1 should succeed, 9 should receive "Slot unavailable" error. Must be tested under load, not in development.
* [ ] **Messaging security:** Can phone numbers, email addresses, and social media handles be sent in messages? They should be blocked. Test with: "call me at 555-123-4567", "email me at user@gmail.com", "find me on IG @username". All 3 should fail.
* [ ] **Review system integrity:** Can a user review a transaction they were not a party to? No. Can a reviewed user retaliate before seeing the review? No (double-blind). Can a single user leave 10 reviews on the same transaction? No.
* [ ] **Payout correctness:** Seller with $1,000 in completed transactions at 10% take rate should receive exactly $900 (minus payment processing). Test with actual Connect test accounts, not mocked responses.
* [ ] **Search performance:** Query load test with realistic data volume (production scale x 1.5). 95th percentile search response time < 200ms. Faceted filtering with 5 active filters < 300ms.
* [ ] **Timezone integrity:** Create a booking in EST for a provider in PST. Provider's calendar should show booking time in PST. Buyer's confirmation should show in EST. No double-bookings due to timezone conversion bugs.
* [ ] **Sales tax collection:** For US marketplace facilitator states - is tax calculated correctly at checkout? Collected? Remitted? Registration complete in all applicable states?
* [ ] **Cold start readiness:** Does the onboarding flow for new sellers create a listing that matches the quality of the top 25% of existing listings? Does the first-time buyer experience surface at least 10 relevant, high-quality listings within 2 seconds?

## Sub-Skills - When to Use Specialized References
<!-- STANDARD: 3min -->

* **api-designer** - When designing the REST/GraphQL API surface for marketplace operations (listing CRUD, booking endpoints, messaging, payment initiation). The marketplace API has multiple consumer types (buyers, sellers, admins) with different permission models.
* **database-designer** - When designing the schema for listings (semi-structured data across categories), availability calendars (time-series), messaging, and transaction records. Marketplace databases balance relational integrity (payments, users) with flexible schemas (listing attributes across diverse categories).
* **system-architect** - When planning the overall marketplace architecture including search infrastructure, image processing pipeline, notification system, and scaling plan for peak traffic (holiday shopping for product marketplaces, summer for travel marketplaces).
* **security-engineer** - When implementing KYC, identity verification, fraud detection rules, payment security (PCI-DSS), and access control for multi-party data (buyer sees seller's rating but not their real name before booking).
* **backend-developer** or **fullstack-developer** - When implementing the actual marketplace platform code (listings, transactions, messaging, booking, payout scheduling).
* **qa-engineer** - When testing booking race conditions, payment flow edge cases, search with large datasets, and multi-user scenarios (buyer + seller + admin interactions).
* **performance-engineer** - When optimizing search response times under load, image delivery via CDN, and concurrent booking handling at scale.
* **growth-engineer** - When designing supply acquisition funnels, demand generation campaigns, referral programs for both sides, and SEO for listing pages.
* **accountant** - When setting up marketplace facilitator tax collection, 1099-K automation, multi-currency accounting, and revenue recognition for escrowed funds.
* **seo-specialist** - When optimizing listing pages for search engines, building category landing pages, and implementing structured data for products/services.
* **saas-monetization-strategist** - When designing commission models, seller subscription tiers, freemium structures, and upsell paths.
* **accessibility-auditor** - Ensure marketplace UI (listings, booking flows, messaging) is accessible to all users including those with disabilities.

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | Scalability requirements, infrastructure decisions, database selection | During architecture design phase |
| `api-designer` | API contracts, versioning strategy, webhook patterns | Before implementing payment and search APIs |
| `database-designer` | Schema design for multi-tenant marketplace data, indexing for search | During data model design |

## Handoff Protocols
<!-- STANDARD: 3min -->

When routing work to other skills, provide:
* **Marketplace context:** "Product marketplace, 500 sellers / 10K buyers, $75 AOV, 12% take rate, Stripe Connect Express accounts, PostgreSQL + Meilisearch, US-only for now, expanding to EU in 6 months."
* **Current phase:** "Phase 2: Payment Architecture - implementing escrow for high-value items (>$500)."
* **Constraints:** "Must use Stripe Connect (already integrated), cannot add payment processors, seller pays 0.5% platform fee for escrow."

Key interfaces between skills:
* marketplace-platform-builder -> payment: define escrow rules, payout schedules, fee structures, Connect account type requirements
* marketplace-platform-builder -> booking: define availability models, timezone rules, buffer times, double-booking requirements
* marketplace-platform-builder -> trust-safety: provide marketplace-specific rules (what constitutes fraud for this marketplace type, acceptable review behaviors)
* marketplace-platform-builder -> search: define relevance factors (distance vs rating vs price vs freshness tradeoffs), faceted filter requirements, category taxonomy

## Communication Triggers
<!-- STANDARD: 3min -->

If you detect any of these conditions while working on the marketplace, you **must** explicitly call them out to the user:

* **Trust black hole:** The platform design allows a user to transact without any identity trail. Response: "This marketplace has no identity verification for transactions above [threshold]. With no verification gate, expect a fraud rate of 5-10% of transaction volume. At [projected GMV], that's [dollar amount] in fraud losses per month. I recommend adding Tier 2 verification before first payout at minimum."
* **Liquidity death spiral:** Fill rate is below 10% and trending down. Response: "Marketplace liquidity is critically low at [fill rate]%. At this rate, buyers churn within 2-3 visits. You have approximately 4-6 weeks before buyer-side acquisition becomes net-negative - the cost to acquire a buyer exceeds expected lifetime value because they don't find what they need. Options: (a) seed supply manually, (b) narrow geography to increase density, (c) pivot to a single high-demand category."
* **Escrow design gap:** Transactions >$X are being processed without escrow. Response: "Transactions above $500 are direct payouts with no escrow protection. This creates a trust asymmetry - buyers bear 100% of non-delivery risk. The expected chargeback rate for these transactions is 2-4x higher than escrowed transactions. Implementing escrow via Stripe Connect deferred payouts would reduce chargebacks by [estimated] 40-60%."
* **Regulatory blind spot:** Marketplace facilitator tax liability is not being collected. Response: "As a marketplace facilitator with sellers in [states], you are required to collect and remit sales tax. Non-compliance penalties start at $X per transaction and the state can assess back taxes for the entire period of non-compliance. This is not optional - major marketplaces (Etsy, eBay, Amazon) have been complying since 2019-2021 per state laws. Implement via Stripe Tax, TaxJar, or Avalara."
* **Commission model mismatch:** The take rate doesn't cover payment processing costs. Response: "Your net take rate after payment processing is [negative/zero]%. At [projected volume], you are losing [amount] per transaction. You need either: (a) a minimum transaction size to cover fixed processing fees, (b) a different commission model (percentage instead of flat fee), or (c) additional revenue streams (subscription, promoted listings)."
* **Booking race condition risk:** No atomic booking implementation. Response: "The current booking flow uses application-level availability checks without database constraints. Under concurrent load, this allows double-bookings. Even at 100 bookings/day, with 3-second average booking flow time, the probability of a double-booking collision is approximately 3-5 per month. Each double-booking costs $[cost] in re-accommodation. Fix: add UNIQUE constraint on (listing_id, booking_date) and move availability check into the INSERT transaction."

## Proactive Triggers
<!-- STANDARD: 3min -->

These are things you should do automatically, without waiting for the user to ask:

* Always calculate and surface net take rate (not just gross commission). "Your 15% commission = 12.1% net take rate after Stripe 2.9% + $0.30. At $50 AOV, that's $6.05 net per transaction (not $7.50)."
* Always specify which Stripe Connect account type for the use case (Standard for individual sellers, Express for platforms wanting lighter onboarding, Custom for full white-label control).
* Always flag that a marketplace needs a TOS that covers both buyer and seller sides - not just a generic website TOS.
* Always mention the 1099-K threshold and marketplace facilitator responsibilities when designing the payment flow for US-based platforms.
* Always include the cold start strategy for every marketplace design - no marketplace design is complete without a liquidity plan.
* Always recommend starting with a single geography and a single category and expanding only after proving liquidity.
* Always check whether the commission model works at both the lowest and highest expected transaction values ($5 and $5,000 - does the take rate math work at both extremes?).
* When designing messaging, always include off-platform communication prevention. "A marketplace where parties take communication off-platform is a marketplace that leaks revenue."
* When designing reviews, always include "verified transaction only" and "double-blind" mechanisms.

## Operating at Different Levels
<!-- STANDARD: 3min -->


## Level 1 (Apprentice) - For Junior Developers
<!-- STANDARD: 3min -->

Focus: Implementing individual marketplace features correctly.
* Build a listing CRUD with proper validation (required fields by category, image upload with resizing).
* Implement Stripe Connect payment with application fees on Standard accounts.
* Add basic search with PostgreSQL full-text or simple Elasticsearch queries.
* Write booking availability checks with database-level uniqueness.
* Build in-platform messaging that blocks common contact-info patterns.


## Level 2 (Practitioner) - For Mid-Level Developers
<!-- STANDARD: 3min -->

Focus: Connecting marketplace components into a cohesive platform.
* Design the full listing lifecycle: create -> review -> publish -> deactivate -> archive.
* Implement escrow flows: hold funds -> buyer confirmation / timeout -> release or refund.
* Add review system with verified purchase gating and double-blind submission.
* Build admin dashboard: transaction monitoring, dispute queue, payout reconciliation.
* Implement fraud rules: velocity checks, transaction-value-to-user-average ratio, geo-mismatch detection.


## Level 3 (Senior) - For Senior Developers
<!-- STANDARD: 3min -->

Focus: System-level thinking across buyers, sellers, and platform operations.
* Architect the full payment flow including Connect account types, split payments for multi-party transactions, and multi-currency support.
* Design the search infrastructure migration path: PostgreSQL full-text -> Meilisearch -> Elasticsearch based on listing volume.
* Implement supply-demand matching algorithms: relevance scoring with configurable weights, location-based ranking, freshness decay.
* Build marketplace analytics: GMV tracking, take rate calculation (gross and net), liquidity metrics, cohort analysis by acquisition channel.
* Design the notification system: transactional (booking confirmed, payment received) and engagement (new listing matches saved search, price drop alert).


## Level 4 (Staff/Lead) - For Staff Engineers
<!-- STANDARD: 3min -->

Focus: Platform strategy, multi-marketplace patterns, and business impact.
* Design marketplace-in-a-box: a platform that can launch new marketplace verticals without rebuilding core infrastructure (listings, payments, messaging, trust).
* Architect multi-sided marketplace dynamics: when your marketplace has 3+ sides (buyers, sellers, delivery partners, insurers, inspectors).
* Implement advanced trust systems: ML-based fraud detection, network graph analysis for collusion detection, automated dispute resolution for low-value cases.
* Design international expansion: multi-currency, multi-language listings, region-specific compliance (GDPR for EU marketplace, PIPL for China, LGPD for Brazil).
* Build marketplace financial modeling: unit economics per transaction, LTV/CAC by side and cohort, GMV forecasting, take rate optimization models.


## Level 5 (Transformative) - For Principal Engineers
<!-- STANDARD: 3min -->

Focus: Redefining what a marketplace can be.
* Decentralized marketplaces: smart contract escrow, DAO governance for dispute resolution, tokenized reputation that travels across platforms.
* AI-native marketplaces: automated listing creation from photos, AI-powered pricing recommendations, fully automated dispute resolution for >90% of cases, agentic supply/demand matching (buyers don't search - the marketplace proactively matches).
* Cross-platform liquidity protocols: enabling supply and demand to flow across marketplace platforms (imagine a seller listed on your marketplace automatically appearing on 5 partner marketplaces with real-time inventory sync).
* Embedded marketplaces: marketplace-as-API that integrates into other platforms (SaaS platform adds "find a consultant" marketplace natively powered by your infrastructure).

## Best Practices
<!-- STANDARD: 3min -->

* **Measure liquidity obsessively - it is the heartbeat of your marketplace.** Track fill rate (searches that result in a transaction), time-to-match (seconds from search to booking/purchase), and supplier utilization (% of supply-side capacity that is filled). If any of these decline for 2 consecutive weeks, intervene before the death spiral begins.

* **Make the transaction the atomic unit of everything.** Every feature, every metric, every notification should be keyed to the transaction. A marketplace is a transaction engine with a UI - not the other way around. Reviews attach to transactions. Payments attach to transactions. Disputes attach to transactions. Analytics aggregates transactions.

* **Price your take rate based on value captured, not cost-plus.** A marketplace that helps a photographer find clients without any marketing effort captures 20-30% of their marketing budget. Charge based on that value, not 2.9% + a 1% margin. Cost-plus pricing produces unsustainable marketplaces.

* **Control the payment - control the marketplace.** If you don't process the payment, you don't have a marketplace - you have a lead-gen platform. Revenue leakage, trust erosion, and disintermediation are inevitable when payments happen off-platform.

* **Build for the side that is harder to acquire.** In most marketplaces, supply is harder to acquire than demand (sellers must create listings, upload photos, set prices - buyers just need a credit card). Design onboarding, incentives, and retention for the harder side first.

* **Prevent disintermediation by adding more value than the match.** If your only value is the introduction, parties will take future transactions off-platform. Add value post-match: escrow, dispute resolution, insurance, scheduling, analytics, invoice generation. Make the platform essential to the transaction, not just the introduction.

* **Launch with curation, scale with algorithms.** Manual curation of supply (hand-picking the top 100 sellers, reviewing every listing before publish) creates quality that algorithms alone cannot match at launch. As volume grows, use the curated data as training data for automated quality scoring.

* **Tax compliance is not optional and it compounds.** Start collecting sales tax from day one - retroactive compliance is exponentially harder. Stripe Tax or TaxJar costs 0.5% of transaction value - far less than the cost of non-compliance.

## State Log - Tracking Marketplace Build Progress
<!-- STANDARD: 3min -->

When working on a marketplace build, maintain a state tracking block.

**How it works:**
Below each turn's response, append a results block tracking decisions made, components built, and open items. This creates a running log that any future skill/handoff can resume from.

```xml
<state_log>
  <decisions>
    <item id="marketplace-type" status="decided">product | service | rental | b2b | lead-gen | crowdfunding</item>
    <item id="geography" status="decided">single-city: [city] | multi-city | global</item>
    <item id="payment-model" status="decided">Stripe Connect [Standard|Express|Custom] | facilitator-only | hybrid</item>
    <item id="commission-model" status="decided">percentage:[X]% | flat-fee:$[X] | tiered | subscription | freemium | blended</item>
    <item id="escrow-strategy" status="decided">per-transaction | milestone-based | no-escrow | deferred-payout:[N]days</item>
  </decisions>
  <built>
    <item id="listings" status="built | in-progress | not-started"/>
    <item id="search" status="built | in-progress | not-started"/>
    <item id="payments" status="built | in-progress | not-started"/>
    <item id="escrow" status="built | in-progress | not-started"/>
    <item id="messaging" status="built | in-progress | not-started"/>
    <item id="booking" status="built | in-progress | not-started"/>
    <item id="reviews" status="built | in-progress | not-started"/>
    <item id="verification" status="built | in-progress | not-started"/>
    <item id="disputes" status="built | in-progress | not-started"/>
    <item id="analytics" status="built | in-progress | not-started"/>
  </built>
  <open-items>
    <item>[Description of pending decision or issue]</item>
  </open-items>
</state_log>

```

**Anti-Drift Check:**
At the start of each new conversation about a marketplace build, consult the state log from the previous session. If no state log exists, begin with the discovery questions in the Route the Request section.

## What Good Looks Like
<!-- STANDARD: 3min -->

A marketplace build is considered **production-ready** when:

* A new seller can create a listing from their phone in under 10 minutes and have it published (or in-review) within that time.
* A buyer can search, find, and complete a transaction end-to-end in under 3 minutes from landing on the platform.
* Payment flow handles the full lifecycle: pay -> escrow hold -> fulfillment -> confirmation -> payout -> refund-if-needed, all automated.
* Trust systems prevent the top 5 fraud vectors: stolen payment methods, fake listings, review manipulation, account takeover, and collusion.
* The search returns relevant results (buyer clicks on a top-5 result) for 80%+ of queries, with p95 response time under 200ms.
* Booking system passes concurrent booking test: 10 simultaneous requests, 1 success, zero double-bookings.
* Messaging keeps communication on-platform with automated detection of contact info sharing and appropriate blocking.
* Analytics dashboard tracks GMV, net take rate, liquidity (fill rate, time-to-match), supply/demand side cohort retention, and chargeback rate - all updated daily minimum.
* Tax compliance is automated: sales tax collected at checkout, remitted on schedule, 1099-K forms generated and filed.
* Escrow and dispute resolution have clear policies at every tier (automated, mediation, arbitration), with documented SLAs for each.

## Deliberate Practice - Skill-Building Exercises
<!-- STANDARD: 3min -->

* **Exercise 1: Design the transaction flow.** Take a marketplace you use regularly (Airbnb, Uber, Etsy, Upwork). Diagram the complete transaction flow: listing -> discovery -> booking/purchase -> payment -> escrow -> fulfillment -> confirmation -> review. For each step, identify: what data changes state, what notification fires, what failure modes exist.

* **Exercise 2: Design the cold start for a new marketplace type.** Pick a marketplace type you've never designed before. Design the cold start strategy: which side do you seed first? What incentives do you offer? What geography do you launch in? What's your exclusivity policy? Write the first 90-day plan.

* **Exercise 3: Build a commission model that works at both extremes.** Design a commission model for a marketplace with $5-$5,000 transactions. Show the math at $5, $50, $500, and $5,000. Verify the net take rate is positive at all levels. Adjust the model until it works at all levels without being unfair at any level.

* **Exercise 4: Red-team the trust & safety.** For a marketplace you designed, list every way a bad actor could exploit it. Stolen credit cards? Fake listings? Review manipulation? Collusion? For each vector, write the detection rule and the automated response. Score your own design.

* **Exercise 5: Migrate the search.** Design a search migration plan for a marketplace with 1,000 listings today growing to 100,000 in 12 months. What search technology at each stage (1K, 10K, 50K, 100K)? What are the cutover criteria? What runs in shadow mode before cutover?

* **Exercise 6: Internationalize a US-only marketplace.** Take a US-only marketplace and design the changes needed for EU expansion: GDPR compliance, VAT collection (marketplace rules), multi-currency, multi-language listings, regional payment methods (SEPA, iDEAL, Sofort). Identify every code change, infrastructure change, and operational change.

## Error Decoder - War Stories from the Trenches
<!-- STANDARD: 3min -->

| Symptom | Common Cause | Diagnostic | Fix |
|---|---|---|---|
| Sellers not completing onboarding. 80% drop-off after step 2 of 5. | Too many fields, too early. Asking for tax ID and bank details before seller sees any value. | Check onboarding funnel analytics: which step has the highest drop-off? | Defer all non-essential fields until after first listing is published. Bank details before first payout, not before first listing. |
| Buyers search but never message or book. High search-to-contact ratio (100:1). | Search results are irrelevant. Buyers see poor matches and assume the platform doesn't have what they want. | Review search logs: what queries return 0 results or low-relevance results? | Add synonyms, typo tolerance, and category boosting. If a query for "vintage leather sofa" returns no results, show "vintage leather couch" or just "leather sofa" with messaging about expanding search. |
| Disputes spike 3x in one week. No code changes deployed. | Either: (a) a new seller cohort is low-quality (fake listings, misleading descriptions), or (b) payment fraud wave (stolen cards being tested). | Filter disputes by: seller cohort (new sellers in last 30 days?), buyer cohort (new accounts?), transaction location (specific geography?), category (one category over-represented?). | If seller-cohort-driven: pause new seller onboarding from that channel, review all active listings from that cohort. If payment-fraud-driven: tighten payment verification rules, add velocity checks. |
| Stripe Connect onboarding fails for 40% of sellers. | Wrong Connect account type for the seller demographic. Custom accounts require more fields than Express. Some sellers are in unsupported countries. | Filter failures by: country, account type requested, failure reason code from Stripe. | Switch to Express accounts (simpler onboarding) if sellers are primarily individuals. Pre-filter supported countries before starting onboarding. Provide clear error messages with next steps. |
| "Take rate" in analytics shows 15% but bank account shows 8% of GMV. | Gross take rate conflated with net take rate. Payment processing, refunds, chargebacks, FX fees, and Connect fees are consuming 7% of GMV. | Build a take rate waterfall: GMV -> gross commission -> minus payment processing -> minus refunds -> minus chargebacks -> minus FX fees -> minus Connect account fees = net take rate. Track each step. | Fix the largest leakage points first. Typically: refunds (tighten return policy, improve listing accuracy) and payment processing (negotiate rates at >$1M/month processing volume). |
| Mobile users have 3x lower conversion than desktop. | Non-responsive listing pages, slow image loading on mobile, no mobile-optimized booking/purchase flow, no push notifications for follow-up. | Check mobile page speed (Lighthouse score), image sizes, form UX on 375px wide viewport. | Implement responsive images with srcset, lazy loading, mobile-optimized booking UX (large tap targets, minimal typing), PWA with push notifications for booking confirmations and messages. |

## Production Checklist - Pre-Launch Verification
<!-- STANDARD: 3min -->

Before launching a marketplace to the public, every item in this checklist must be verified:

### Payments & Money Movement
* [ ] Stripe Connect integration tested end-to-end with live test mode accounts (buyer, seller, platform).
* [ ] Application fees calculate correctly: verify for $10, $100, $1,000, $10,000 transactions - at every tier if using tiered commissions.
* [ ] Escrow holds release correctly: on buyer confirmation, on auto-release timeout, on dispute resolution.
* [ ] Refunds return correct amounts: buyer refund = full payment, platform fee refund if refund is platform-initiated.
* [ ] Payout schedule is documented: when does a seller get paid after transaction completion? Same for service providers, rental hosts.
* [ ] Failed payout handling: what happens when a seller's bank account is invalid? Retry logic, notifications, support workflow.
* [ ] Sales tax collection active in all marketplace facilitator states where you have nexus.
* [ ] 1099-K reporting pipeline tested: can you generate a report of all sellers above the reporting threshold?
* [ ] Chargeback response workflow: 7-day response window, pre-built evidence templates (tracking number, delivery confirmation, listing description).
* [ ] Multi-currency: if supported, tested GBP, EUR, CAD, AUD transactions, verified exchange rates applied, verified seller receives correct amount in their currency.

### Trust & Safety
* [ ] Identity verification at appropriate tiers: Tier 1 for all, Tier 2 for threshold-triggered, Tier 3 for high-value.
* [ ] Review system: verified purchase gating, double-blind enforced, weight-by-transaction-value tested.
* [ ] Review manipulation detection: 10+ reviews from same IP, 10+ reviews to same seller in 24h, sentiment-text mismatch.
* [ ] Listing fraud detection: reverse image search for stock photos, price anomaly detection (3 sigma below category median).
* [ ] Payment fraud rules active: billing/shipping country mismatch, rapid small transactions (card testing), high-value first purchase.
* [ ] Dispute resolution workflow: Level 1 (automated) -> Level 2 (mediation) -> Level 3 (arbitration) -> Appeal path defined and tested.
* [ ] Terms of Service for both buyer and seller sides, with platform policies on prohibited items, acceptable use, and liability limits.

### Marketplace Operations
* [ ] Search returns results for top 100 expected queries (test manually with a checklist).
* [ ] Search performance: <200ms p95 with 2x current listing volume, faceted filtering functional.
* [ ] Category taxonomy functional: browse path works (Category > Subcategory > Item Type), filtering by category returns correct results.
* [ ] Booking: concurrent booking test (10 simultaneous), timezone test (buyer and seller in different zones), buffer time enforcement.
* [ ] Messaging: contact info blocked, URL allowlist enforced, attachments scanned.
* [ ] Notification system: transactional emails (booking confirmed, payment received, payout sent) working, push notifications for real-time events.
* [ ] Seller onboarding completion rate >60% (or documented reasons for drop-off with improvement plan).
* [ ] First-time buyer experience: can a new user find and complete a transaction in under 5 minutes?
* [ ] Admin dashboard: can you view all active transactions, disputes, flagged accounts, and platform metrics at a glance?

### Infrastructure
* [ ] Database backups: daily automated backups with point-in-time recovery, verified restore process.
* [ ] CDN for listing images: images served through CDN with proper caching headers, responsive image sizes.
* [ ] Monitoring and alerting: transaction failure rate, search latency, booking error rate, payout failure rate all monitored with alerts.
* [ ] Rate limiting on API endpoints: especially payment initiation, booking creation, message sending.
* [ ] DDoS protection: Cloudflare/AWS Shield or equivalent on all public endpoints.
* [ ] Logging: every state change in a transaction lifecycle is logged (created -> paid -> fulfilled -> confirmed -> paid_out), searchable within 60 seconds of occurrence.

## Deliberate Practice
<!-- STANDARD: 3min -->

The best marketplace builders understand liquidity dynamics, trust mechanics, and multi-sided network effects. Deliberate practice means launching real marketplaces, measuring liquidity metrics, and iterating based on supply/demand data.

| Level | Practice Routine | Frequency |
|---|---|---|
| **Novice** | Build a simple two-sided marketplace (e.g., service booking) with Stripe Connect, basic search, and reviews. Seed supply side with 10 providers. Measure time-to-first-transaction | Monthly |
| **Competent** | Implement escrow/custodial payments, dispute resolution workflow, and fraud detection rules. Run a simulated marketplace with 100+ transactions. Measure dispute rate and resolution time | Quarterly |
| **Advanced** | Build a production marketplace with search/discovery (Elasticsearch/Algolia), messaging, booking/scheduling, and analytics dashboard. Launch with real users on both sides. Track GMV, take rate, liquidity, and retention | Biannually |
| **Expert** | Scale a marketplace to $1M+ GMV. Implement multi-geography support (currencies, languages, compliance), marketplace facilitator tax automation, and ML-powered trust & safety. Publish a case study on liquidity engineering | Annually |

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift. Every major decision (payment architecture, trust/safety strategy, search infrastructure, cold start playbook) must be recorded.

| Decision | Date | Rationale | Alternatives Considered |
|----------|------|-----------|------------------------|
| *Record all critical decisions here* | — | — | — |

## References
<!-- STANDARD: 3min -->

Core marketplace platform references (extracted to.

* **Marketplace Types & Strategies** - Detailed breakdown of each marketplace type, supply/demand dynamics per type, cold start playbooks for each type, and case studies of successful marketplaces that executed each playbook..

* **Payment Architecture Deep Dive** - Complete Stripe Connect integration patterns (Standard vs Express vs Custom), escrow implementation patterns, multi-party payment splitting, marketplace facilitator tax compliance by jurisdiction, 1099-K automation..

* **Trust & Safety Implementation** - Identity verification provider comparison (Stripe Identity, Onfido, Jumio, Persona), fraud detection rule engines, ML-based fraud detection architecture, review system design patterns, dispute resolution workflows..

* **Search & Discovery Architecture** - Search infrastructure comparison (PostgreSQL FTS vs Meilisearch vs Elasticsearch vs Algolia), relevance scoring algorithms for marketplaces, faceted filtering patterns, recommendation engine patterns (collaborative filtering, content-based, hybrid), geospatial search with PostGIS..

* **Analytics & Metrics** - Marketplace-specific analytics schema (GMV, take rate, liquidity, cohort analysis), dashboard implementation patterns, event tracking architecture, marketplace financial modeling..

* **Regulatory Compliance by Region** - US: marketplace facilitator laws by state, 1099-K thresholds, INFORM Consumers Act, Section 230. EU: Digital Services Act, GDPR for marketplaces, VAT One Stop Shop, PSD2/SCA requirements. UK: P2B Regulation..

* **Mobile Marketplace Patterns** - Location services integration, push notification architecture, camera & media handling, offline support for field service marketplaces, mobile payment integration (Apple Pay, Google Pay)..

* **Booking & Scheduling Systems** - Calendar data models, timezone handling patterns, double-booking prevention implementations, recurring availability, buffer time, capacity management..

* **Messaging & Communication** - Real-time messaging architecture, off-platform leakage prevention, message moderation patterns, attachment handling, notification systems..

## External Resources
<!-- STANDARD: 3min -->

* **Stripe Connect Documentation** - https://stripe.com/docs/connect - The definitive reference for marketplace payment architecture. Study the account type comparison (Standard vs Express vs Custom) and application fee patterns.
* **The Marketplace Monetization Map** - https://a16z.com/marketplace-monetization-map/ - a16z framework for marketplace business models and monetization strategies.
* **All about Stripe Connect and payments for marketplaces** - https://stripe.com/guides/marketplaces - Stripe's comprehensive marketplace guide covering payment flows, compliance, and best practices.
* **The Hierarchy of Marketplace Needs** - https://www.nfx.com/post/the-hierarchy-of-marketplace-needs - Sarah Tavel's framework for marketplace success factors: from foundational trust to network effects.
* **Marketplace Liquidity** - https://a16z.com/2018/11/01/everything-you-wanted-to-know-about-marketplace-liquidity/ - a16z deep dive on marketplace liquidity metrics and strategies.
* **1099-K Reporting Requirements** - https://www.irs.gov/businesses/understanding-your-form-1099-k - IRS guidance on marketplace facilitator reporting obligations.
* **Digital Services Act (EU)** - https://commission.europa.eu/strategy-and-policy/priorities-2019-2024/europe-fit-digital-age/digital-services-act_en - EU regulation governing online platforms and marketplaces operating in the EU.
* **INFORM Consumers Act** - https://www.ftc.gov/legal-library/browse/statutes/inform-consumers-act - US law requiring online marketplaces to verify high-volume third-party sellers.
* **All About Doubts**, by Andrew Chen - Essential reading for marketplace builders on cold start problems and network effects.
* **Platform Revolution**, by Geoffrey G. Parker, Marshall W. Van Alstyne, and Sangeet Paul Choudary - Comprehensive framework for platform business models, network effects, and marketplace strategy.
