---
name: fintech-ui-designer
description: >
  Use when designing user interfaces for financial applications — trading platforms,
  banking dashboards, investment portfolios, payment flows, cryptocurrency exchanges,
  insurance portals, and personal finance tools. Handles real-time data display
  patterns, high-density information layouts, compliance-driven UI (KYC, audit trails,
  regulatory disclosures), financial data visualization (candlestick charts, order
  books, portfolio allocation), and accessibility for financial data (screen-reader
  tables, color-independent gain/loss indicators). Do NOT use for general dashboards
  (use data-visualization-engineer), backend financial systems, or non-financial
  data displays.
license: MIT
allowed-tools: Read Grep Glob
tags:
  - fintech
  - finance
  - trading
  - banking
  - dashboard
  - data-visualization
  - compliance
  - accessibility
author: Sandeep Kumar Penchala
type: design
status: stable
version: 1.0.0
updated: 2026-07-26
token_budget: 3200
chain:
  consumes_from:
    - ui-ux-designer
    - data-visualization-engineer
    - accessibility-auditor
  feeds_into:
    - frontend-developer
    - mobile-developer
    - data-visualization-engineer
---
# Fintech UI Designer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

Design interfaces for financial applications where **precision, trust, and speed** are paramount. Financial UI carries legal weight — a misplaced decimal point, a confusing fee disclosure, or an inaccessible gain/loss indicator can cost real money and trigger regulatory action.
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

| Loop | When It Fires | What Re-research Validates | Fee transparency must come BEFORE confirmation — lost trust never fully returns. |
|------|--------------|---------------------------| Color is a decoration, not a signal — always pair it with shape, text, and icons. |
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations | Never format money with floating-point math — integer cents prevent display errors. |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? | Real-time data that freezes under load is worse than delayed data — throttle, don't frame-drop. |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? | Fee transparency must come BEFORE confirmation — lost trust never fully returns. |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? | Color is a decoration, not a signal — always pair it with shape, text, and icons. |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.



## Route the Request
<!-- STANDARD: 3min -->

### Auto-Route

| # | Condition | Action | Never format money with floating-point math — integer cents prevent display errors. |
|---|-----------|-------- Real-time data that freezes under load is worse than delayed data — throttle, don't frame-drop. |
| A1 | `file_contains("*.tsx", "candlestick|orderbook|tradingview")` | Trading platform detected. Jump to **Trading Interfaces**. |
| A2 | `file_contains("*.css", "dashboard")` AND `file_contains("*.tsx", "balance|transaction|account")` | Banking dashboard. Jump to **Core Workflow → Banking UX**. |
| A3 | `file_exists("*.csv")` AND `file_contains("*.csv", "price|volume|ticker")` | Financial data feed. Jump to **Data Display Patterns**. |

### Intent Route

```
What are you building?
├── Trading platform (order books, charts, price ladders) → Trading Interfaces
├── Banking dashboard (accounts, transactions, transfers) → Banking UX
├── Investment portfolio (holdings, allocation, performance) → Portfolio Design
├── Payment flow (checkout, wallet, P2P transfer) → Payment UX
├── KYC/onboarding flow → Compliance-Driven UI
├── Cryptocurrency exchange → Crypto-Specific Patterns
├── Insurance portal → Insurance UX
├── Personal finance tool (budgeting, tracking, goals) → Personal Finance UX
└── Not sure → Describe the financial domain and primary user action
```

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|--------------------|
| G1 | Never display financial data without a timestamp — "last updated" is as important as the number | `file_contains(output, "$|USD|price|balance")` AND NOT `file_contains(output, "as of|updated|timestamp|delay")` | REFUSE. "Financial data is time-sensitive. Every price, balance, or rate must show 'As of [timestamp]' or 'Delayed [N] minutes.'" |
| G2 | Never convey gain/loss by color alone (red/green) — always include +/− sign and percentage text | `file_contains(output, "green|red")` AND NOT `file_contains(output, "\\+|\\-|arrow.up|arrow.down|increase|decrease")` | DETECT. "Color-only indicators fail for colorblind users and grayscale displays. Always include +/− signs, arrow icons, and text percentage." |
| G3 | Never show a confirmatory action (buy, sell, transfer) without a review step showing all fees, totals, and irreversible consequences | `file_contains(output, "confirm|submit|buy|sell|transfer")` AND NOT `file_contains(output, "fee|total|review|are you sure|irreversible")` | REFUSE. "Financial transactions require a review step. Show: breakdown of fees, total amount, delivery time, and a clear 'This action cannot be undone' warning." |
| G4 | Never abbreviate large numbers without a consistent legend and tooltip with full precision | `file_contains(output, "K|M|B|T")` AND NOT `file_contains(output, "legend|tooltip|exact")` | STOP. "Abbreviated numbers must show full precision on hover/tap. '$1.2M' must reveal '$1,234,567.89' with the abbreviation legend visible." |
| G5 | Never display user financial data without end-to-end encryption indicators (lock icon, "Secured by" label) | `file_contains(output, "account|balance|portfolio")` AND NOT `file_contains(output, "secure|encrypt|lock|256-bit|SSL|TLS")` | DETECT. "Financial applications must display security assurance indicators. Show lock icon + encryption status in persistent chrome." |
| G6 | Never specify UI telemetry, analytics, or error logging that could capture financial credentials, account numbers, or PII in plaintext | `file_contains(spec, "log|analytics|telemetry|track")` AND NOT `file_contains(spec, "redact|sanitize|mask|PII|never.log|no.sensitive")` | REFUSE. "UI telemetry and logging must never capture financial data in plaintext. Specify: all account numbers masked to last 4 digits, all PII redacted at the logging pipeline, zero credentials in any log. Reference PCI DSS Requirement 3.4 for data masking standards." |
| G7 | Never specify animations that delay data visibility or misrepresent financial values — every animation must complete in ≤200ms and never interpolate prices | `file_contains(spec, "animate|transition|motion|spring|tween")` AND NOT `file_contains(spec, "duration.*ms|200ms|prefers-reduced-motion|no.interpolation")` | REFUSE. "Financial UI animations must never delay data visibility or distort values. Rules: (1) price animations ≤200ms — faster is better, (2) NEVER interpolate between prices — a price change flash communicates the fact of change, not a fake 'tween' from old to new, (3) transaction confirmations: checkmark animation + haptic, (4) every animation must have a `prefers-reduced-motion: reduce` fallback to instant. A 400ms price 'count-up' animation showing $97.34 → $103.21 is showing the user WRONG numbers for 400ms." |

## The Expert's Mindset
<!-- STANDARD: 3min -->

Financial UI is **high-stakes information design**. Users don't browse financial data — they scan for anomalies, make decisions with real consequences, and need absolute trust in what they see. Every element must answer: "If I act on this information, will I lose money?"

### Mental Models

| Model | Description |
|---|---|
| **Trust through transparency** | Hidden fees, unclear totals, or ambiguous statuses destroy trust permanently. Show everything: fee breakdowns, processing times, exchange rates used, and where every cent goes. |
| **Precision over aesthetics** | A beautiful chart that misrepresents data is worse than an ugly chart that's accurate. Financial data must be mathematically correct before it can be visually polished. |
| **Scanning patterns for financial data** | Users scan portfolios in Z-pattern (top-left → top-right → bottom-left → bottom-right). Users scan transactions in F-pattern (left column → right column, top to bottom). Place critical data on the scan path. |
| **Anxiety-aware design** | People check their finances when stressed. Design for the anxious user: clear labels, confirmations before destructive actions, easy undo paths, and no dark patterns. |

### Cognitive Biases in Fintech UI

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Anchoring** | Users fixate on the first price they see, even if it's outdated or wrong | Always show percentage change alongside absolute value. Show "since purchase" and "today" side by side. |
| **Loss aversion** | Users feel losses 2x more than gains — red numbers trigger panic | Use measured language. Never show "YOU LOST $500!" — show "Portfolio changed −2.3% today." Context matters. |
| **Overconfidence** | Users overestimate their understanding of complex financial products | Every complex product needs a one-sentence plain-English summary. "This option gives you the right, but not the obligation, to buy 100 shares at $X." |
| **Choice overload** | Too many investment options cause decision paralysis | Default to sensible options. Offer "Recommended" or "Popular" filters. Never dump 5,000 mutual funds into a dropdown. |

### What Masters Know

- **Latency IS the UX.** A trading interface that updates in 500ms feels broken. Target <100ms for price updates, <50ms for order confirmations. Show loading states that acknowledge the delay: "Fetching latest price..." not just a spinner.
- **The order matters more than you think.** In a transaction list, most recent first is obvious. In a portfolio, largest position first is better. In a market watchlist, user-chosen order is best. Default sort order is a design decision.
- **Financial data has seasons.** Tax season, earnings season, end-of-quarter — design for these high-stress periods. Users will be emotional. Your UI must be calm.

## Operating at Different Levels
<!-- STANDARD: 3min -->

| Level | User | Scope | What Changes |
|-------|------|-------|-------------|
| **L1 — Apprentice** | Junior designer building a simple budget tracker | Single account view with balance and transactions | Learn financial data display: currency formatting, date handling, gain/loss indicators. |
| **L2 — Solo** | Startup building a fintech MVP | Multi-account dashboard, basic transactions | Add security indicators, KYC flow, fee disclosures. Test with colorblind simulation. |
| **L3 — Small Team** | Growing fintech with real users | Trading, portfolios, compliance flows | Real-time WebSocket data. Multi-currency support. Audit trail in UI. Regulatory disclosures per jurisdiction. |
| **L4 — Medium** | Established fintech, multiple products | Multi-product platform with shared design system | Design system with financial component library. Accessibility at WCAG 2.2 AA minimum. Multi-region compliance. Performance monitoring on data feeds. |
| **L5 — Enterprise** | Bank, exchange, or major fintech | White-label platform, institutional + retail | Institutional-grade data density. Customizable dashboards per user role. SOC 2, PCI-DSS, GDPR compliance built into UI components. Audit-every-click tracking. |

## Decision Trees
<!-- STANDARD: 3min -->

### Decision Tree 1: Real-Time Data Strategy

        ┌── INPUT: How fresh does the data need to be?
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
[Real-Time <1s]   [Near-RT 1-15s]   [Delayed >15s]
Trading,          Portfolio         Statements,
order books,      balances,         reports,
live pricing      positions         history
   │                 │                  │
   ▼                 ▼                  ▼
WebSocket with    Polling with      REST fetch
delta updates     cache headers     on-demand
→ show staleness  → show last       → show timestamp
indicator         updated time      of generation

### Decision Tree 2: Compliance Disclosure Placement

        ┌── INPUT: What type of disclosure?
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
[Transactional]   [Informational]    [Consent]
Fee breakdown,    Risk warnings,     KYC/AML,
exchange rate     terms updates      data sharing
   │                 │                  │
   ▼                 ▼                  ▼
Inline,           Persistent         Modal or
pre-confirmation  banner/footer      dedicated
before submit     (non-dismissible   screen before
                  for regulatory)    account access

### Decision Tree 3: Data Density Calibration

        ┌── INPUT: Who is the primary user?
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
[Retail Consumer] [Pro Trader]       [Institutional]
Casual investor,  Day trader,        Portfolio
banking customer  analyst            manager
   │                 │                  │
   ▼                 ▼                  ▼
Low density:      High density:      Extreme density:
cards, simple     tables, candles,   multi-panel,
charts, single    order books,       customizable
metric per view   multiple metrics   layouts, API
                  per row            data grids

## Core Workflow
<!-- STANDARD: 3min -->

### Phase 1: Domain Discovery (10 min)

1. **Identify the financial domain**: trading, banking, investing, payments, insurance, crypto, personal finance
2. **Identify the primary user action**: monitor (passive), trade (active, time-sensitive), transfer (one-time), analyze (research), budget (ongoing)
3. **Identify regulatory requirements**: KYC/AML, GDPR/CCPA, PCI-DSS, SOC 2, MiFID II, SEC/FCA disclosures
4. **Identify data freshness requirements**: real-time (<1s delay), near-real-time (1-15 min), daily, monthly

### Phase 2: Information Architecture (15 min)

**Dashboard layout by domain:**

| Domain | Primary Metric (Top-Left) | Secondary (Top-Right) | Detail Area (Center) | Action Bar (Bottom) |
|--------|--------------------------|----------------------|---------------------|---------------------|
| Banking | Total balance | Pending transactions | Recent transactions | Transfer, Deposit, Pay |
| Trading | Portfolio value + P&L | Buying power | Chart + order book | Buy, Sell, Order history |
| Investing | Total invested + return | Asset allocation pie | Holdings table | Buy, Sell, Research |
| Payments | Amount to send/pay | Recipient | Payment method + fees | Confirm, Cancel |
| Insurance | Policy status | Next premium due | Coverage details | File claim, Update |
| Crypto | Portfolio value | 24h change | Price chart + order book | Buy, Sell, Send, Receive |
| Personal Finance | Monthly spend vs budget | Top spending category | Transaction list | Add transaction, Set goal |

### Phase 3: Data Display Patterns (10 min)

**Number formatting rules:**
- **Currency**: Always show currency symbol + 2 decimal places. `$1,234.56` not `$1234.567`
- **Large numbers**: Abbreviate with legend. `$1.2M` → tooltip shows `$1,234,567.89`
- **Percentages**: Always show sign + 2 decimal places. `+12.34%` / `−5.67%`
- **Changes**: Green up/red down with arrow icons AND +/− sign. Never color alone.
- **Zero values**: Show `$0.00` not `$0` or `—`. Consistency builds trust.
- **Negative values**: Parentheses or minus sign, chosen consistently. `($500.00)` or `−$500.00`

**Table patterns for financial data:**

```
| Symbol  | Price      | Change      | % Change  | Volume    |
|---------|------------|-------------|-----------|-----------|
| AAPL    | $234.56 ▲  | +$2.34 ▲    | +1.01% ▲  | 45.2M     |
| GOOGL   | $189.23 ▼  | −$1.45 ▼    | −0.76% ▼  | 23.1M     |
```

### Phase 4: Real-Time Data UX (5 min)

- **WebSocket indicators**: Green dot = connected, yellow = reconnecting, red = disconnected
- **Stale data warning**: Gray out prices older than threshold. Banner: "Prices delayed by 15 minutes."
- **Update animations**: Flash changed values briefly (200ms) — not jarring, just noticeable
- **Throttle extreme updates**: During market volatility, don't re-render on every tick. Batch at 100-200ms.

**Animation patterns for financial UI (by context):**

| Context | Animation | Duration | Easing | Reduced Motion | Notes |
|---|---|---|---|---|---|
| Price change (up) | Green flash + arrow | 150-200ms | ease-out | Static green + arrow icon | Never interpolate price number — show the change, not a fake tween |
| Price change (down) | Red flash + arrow | 150-200ms | ease-out | Static red + arrow icon | Same as up but red — consistency matters |
| Order confirmed | Checkmark draw + subtle scale | 300ms | ease-out-back | Static checkmark | Pair with haptic (light) on mobile |
| Transfer initiated | Progress indicator fill | Variable | linear | Static "% complete" text | Shows real progress, not indeterminate spinner |
| New data arrived (WebSocket) | Gentle highlight in/out | 100ms in, 500ms fade | ease-in-out | Instant replace | Subtle — user's eye should catch the change naturally |
| Error / rejection | Red border pulse (1 pulse) | 150ms | ease-out | Static red border | Single pulse only. Never loop — anxiety-inducing in financial context |
| Value crossed threshold (alert) | Amber highlight + gentle pulse (2x) | 150ms × 2 | ease-in-out | Static amber badge | 2 pulse maximum. Pair with sound if user-enabled alerts |

**Performance constraints for financial animations:**
- Animations must not add latency to data display — render the number FIRST, animate the decoration AFTER
- On a ticker with 50+ symbols updating simultaneously, batch DOM updates via `requestAnimationFrame` — never animate each individually
- Mobile: reduce animation complexity on low-power mode. Detect via `navigator.hardwareConcurrency` and battery API

## Trading Interfaces
<!-- STANDARD: 3min -->

### Order Entry Form

```
Buy AAPL — Apple Inc.
├── Order Type: [Market ▼] [Limit ▼] [Stop ▼]
├── Quantity: [___ shares]
├── Price: $_____ (hidden for Market orders)
├── ─────────────────────
├── Estimated Total: $_____
├── Commission: $0.00
├── ─────────────────────
├── Buying Power: $10,000.00
├── After Order: $_____
├── ─────────────────────
├── [Review Order] ← never just "Submit"
└── ─────────────────────
    After Review:
    ├── Order Summary (read-only)
    ├── "This order will execute immediately at the best available price."
    └── [Confirm] [Cancel]
```

### Order Book (Bid/Ask Ladder)
- Bid (buy) on left, Ask (sell) on right — or green/red vertically stacked
- Depth visualization: background bar proportional to volume at each price level
- Spread clearly labeled: "Spread: $0.12 (0.05%)"
- Last traded price highlighted, centered, and large

### Chart Patterns
- **Candlestick**: Price over time. Green up, red down (with pattern/text backup).
- **Line chart**: Simplified price. Good for mobile, long timeframes.
- **Volume bars**: Below price chart. Correlated but separate axis.
- **Timeframe selector**: 1D, 1W, 1M, 3M, 1Y, 5Y, ALL — always visible.

## Banking UX
<!-- STANDARD: 3min -->

### Transaction List
- Grouped by date: "Today," "Yesterday," "This Week," "February 2026"
- Each transaction: merchant logo + name, category icon, amount (right-aligned)
- Pending transactions: grayed out with "Pending" badge
- Tap/hover: transaction detail with date, time, reference number, category

### Transfer Flow
1. Select from account → Select to account → Enter amount → Review → Confirm → Success
2. Show available balance at each step
3. Warn if transfer exceeds available balance
4. Show estimated arrival time (instant, same-day, 1-3 business days)
5. Fee disclosure: "Transfer fee: $0.00" or "Wire transfer fee: $25.00"

## Compliance-Driven UI
<!-- STANDARD: 3min -->

### KYC/Onboarding Flow
- Progress indicator: "Step 2 of 5"
- Document upload with camera integration
- Clear error states: "Photo too blurry. Retake?"
- Time expectations: "This usually takes 2 minutes"
- Verification status: pending, approved, rejected (with reason and next steps)

### Regulatory Disclosures
- Never hide in collapsed sections or tiny footnotes
- Plain-English summary before legal text: "TL;DR: We charge 0.25% per year, deducted monthly."
- Required disclaimers: "Past performance does not guarantee future results."
- Risk warnings: shown before high-risk actions, not after

### Audit Trail UI
- Every user action logged and visible: "You changed your address on Jan 15, 2026 at 3:42 PM"
- Admin view: full audit log with filters by user, action, date
- Export capability: CSV, PDF for compliance reporting

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

| Upstream Skill | What We Need | When |
|---------------|-------------|------|
| `ui-ux-designer` | Design system, component library, responsive patterns | Before building any fintech UI — adapt existing design system |
| `data-visualization-engineer` | Chart libraries, real-time data binding, WebSocket architecture | Before implementing charts and live data |
| `accessibility-auditor` | WCAG 2.2 compliance, screen-reader testing for financial tables | Before launch — financial services are high-risk for accessibility lawsuits |

| Downstream Skill | What We Provide | When |
|-----------------|----------------|------|
| `frontend-developer` | Component specs, data display rules, compliance UI patterns | After design — implement in React/Vue/Next.js |
| `mobile-developer` | Mobile-specific trading/banking UX, touch-optimized order entry | After desktop design — adapt for mobile |
| `data-visualization-engineer` | Chart requirements, data update frequency, precision requirements | During chart design phase |

## Proactive Triggers
<!-- STANDARD: 3min -->

| Trigger | Action | Why |
|---------|--------|-----|
| Transaction confirmation without fee breakdown | Flag: "Show all fees before confirming. Users must see: subtotal, fees, total, and delivery time." | Hidden fees are the #1 cause of fintech user complaints and regulatory action. |
| Gain/loss shown only as red/green color | Flag: "Add +/− signs and percentage text. 8% of males are colorblind — they can't distinguish red from green." | Color-only indicators fail accessibility and cause trading errors. |
| Numbers without consistent decimal places | Flag: "Standardize to 2 decimal places for currency. Inconsistent formatting erodes trust." | Users notice formatting inconsistencies and interpret them as errors. |
| Real-time data without connection status | Flag: "Add connection indicator (green/yellow/red dot). User must know if prices are live or stale." | Trading on stale data causes financial loss. |
| "Submit" or "Confirm" on destructive financial action | Flag: "Add review step with: amount, fees, delivery time, and 'This cannot be undone' warning." | Accidental transactions are irreversible in many financial systems. |

## What Good Looks Like
<!-- STANDARD: 3min -->

> The dashboard loads in under 2 seconds with skeleton screens for every data region. Prices update via WebSocket with a green connection dot. Every gain/loss has +/− sign, arrow icon, and color (checked with colorblind simulation). The order entry form shows estimated total with fee breakdown before the review step. The review step shows a clear "This order cannot be undone" warning. All tables are navigable by screen reader with proper ARIA roles. Currency is formatted consistently to 2 decimal places across every screen. The "last updated" timestamp is visible in the persistent header. Security indicators (lock icon, "256-bit TLS encryption") appear in the footer or status bar.

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|---------|
| Users complain about "hidden fees" | Fee breakdown only shown after confirmation, not before | Move fee disclosure BEFORE the confirm button. Show line items. Never use "estimated total" without itemization. | Fee transparency must come BEFORE confirmation — lost trust never fully returns. |
| Colorblind users can't tell if they're up or down | Red/green-only gain/loss indicators | Add +/− signs, up/down arrows, and percentage text. Test with colorblind simulators. | Color is a decoration, not a signal — always pair it with shape, text, and icons. |
| Prices showing as "$0.000000" | Floating-point precision error in display | Format all currency to 2 decimal places. Use integer cents internally, format for display. | Never format money with floating-point math — integer cents prevent display errors. |
| Real-time chart freezes during volatility | Too many re-renders per second | Throttle updates to 100ms batches. Drop intermediate ticks; show final price for each batch. | Real-time data that freezes under load is worse than delayed data — throttle, don't frame-drop. |

## Best Practices

1. **Do show every fee, total, and consequence before a confirmatory action** — Hidden fees destroy trust permanently in financial products. A user who discovers a $25 wire fee after confirming a transfer will never fully trust your platform again. The review screen must show: fee breakdown, total amount, delivery time estimate, and an explicit "This action cannot be undone" warning. Trust-repair cost after a hidden-fee incident: $50,000-$200,000 in churn and support burden.
2. **Prefer amber/orange for warnings over red** — In financial contexts, red means emergency, error, or critical alert. Overusing red causes alarm fatigue — when everything is red, nothing is. Reserve red for irreversible loss events (trade rejected, transfer failed, account frozen). Use amber for warnings (approaching margin limit, unusual activity), blue for informational (new feature, market update). A dashboard where 40% of elements are red desensitizes users within 2 weeks.
3. **Always pair color indicators (green/red) with +/− signs, arrow icons, and percentage text** — Approximately 8% of males have color vision deficiency. A gain/loss display using only red/green is invisible to protanopes and deuteranopes. Test every financial data view in grayscale — if any gain/loss state becomes ambiguous without color, add shape/icon/text differentiation. An inaccessible portfolio view costs $250,000+ in ADA litigation exposure.
4. **Never abbreviate financial numbers without a visible legend and full-precision tooltip** — "$1.2M" must reveal "$1,234,567.89" on hover/tap. Users making decisions based on abbreviated numbers without knowing the rounding direction (floor, ceiling, nearest) can make costly errors. A trader seeing "$1.2M" for a position worth $1,249,999 acts on different information than one worth $1,200,001. Missing tooltip on abbreviated values has caused $10,000+ trading errors.
5. **Measure time-to-confirmation for common financial tasks** — How many seconds from intent to confirmed completion for a transfer, trade, or bill pay? Target: under 15 seconds for frequent tasks (balance check, recent transactions), under 60 seconds for complex tasks (multi-leg trade, wire transfer). Every additional 10 seconds of friction increases abandon rate by 7% in financial flows. Track via RUM (Real User Monitoring) segmented by task type.

## Production Checklist

Before deploying or delivering work from this skill, verify:

| # | Check | Verify |
|---|-------|--------|
| ☐ | Every price, balance, or rate display includes a visible timestamp — "As of [HH:MM:SS]" or "Delayed [N] minutes" adjacent to the value | Audit all financial data screens: every monetary value must have a timestamp within 50px; missing timestamps trigger Ground Rule G1 |
| ☐ | Gain/loss indicators use +/− sign + arrow icon + percentage text — never color alone; verify in grayscale mode | Toggle device grayscale; confirm all gain/loss states remain unambiguously distinguishable without any color channel |
| ☐ | Every buy/sell/transfer flow has a review step showing: fee breakdown, total amount, delivery time, and irreversible warning before final confirm | Walk through each transactional flow end-to-end; pre-confirmation screen must render all four elements before the final submit button |
| ☐ | All abbreviated numbers (K/M/B/T) show full precision (2 decimal places) on hover/tap with a visible abbreviation legend | Hover/tap every abbreviated value in chart legends, table cells, and summary cards; tooltip must reveal the exact number |
| ☐ | Security indicators (lock icon + "Secured by 256-bit TLS") visible in persistent chrome on every screen displaying user financial data | Verify lock icon and encryption label render in a consistent position (e.g., footer or header) across all account, balance, and portfolio views |
| ☐ | All UI telemetry, analytics, and error logging redact account numbers to last 4 digits and strip PII at the pipeline | Inspect log output at DEBUG level: no full account numbers, email addresses, tokens, passwords, or SSN appear in any log statement |
| ☐ | Price update animations complete in ≤ 200ms and never interpolate between price values — no "count-up" animations showing intermediate fake numbers | Time a price update animation via performance profiler: render-to-completion must be under 200ms; confirm the new price replaces the old instantly — only a flash/color change communicates the fact of change |
| ☐ | Rollback plan is documented and tested | Verify: canary deploy to 1% of users; monitor error rate and transaction confirmation rate for 15 minutes; kill switch reverts to previous UI version without data loss |

## Verification
<!-- STANDARD: 3min -->

| # | Complete when... | Verify |
|---|---|---|
| ☐ | Complete when every price, balance, or rate display includes a timestamp showing "As of [timestamp]" or "Delayed [N] minutes" adjacent to the value | Verify every financial data point on screen has a visible timestamp; missing timestamps trigger Ground Rule G1 violation |
| ☐ | Complete when gain/loss indicators use at minimum: +/− sign prefix, arrow icon (up/down), and percentage text — never color alone | Verify by viewing in grayscale; all gain/loss states remain distinguishable without any color channel |
| ☐ | Complete when every confirmatory action (buy, sell, transfer) shows a review step with: fee breakdown, total amount, delivery time estimate, and irreversible warning | Verify pre-confirmation review screen renders all four elements before the final submit button; missing any element triggers G3 |
| ☐ | Complete when abbreviated large numbers (K/M/B/T) show full precision on hover/tap with the abbreviation legend visible in chart or table footers | Verify tooltip/hover on any abbreviated value reveals full number to 2 decimal places; legend maps abbreviations to scale |
| ☐ | Complete when security indicators (lock icon, "Secured by 256-bit TLS" label) are visible in persistent chrome on every screen displaying user financial data | Verify lock icon and encryption label render in a consistent position across all account, balance, and portfolio views |
| ☐ | Complete when all UI telemetry and logging redacts account numbers to last 4 digits, strips PII at the pipeline, and never captures credentials in any log level | Verify by inspecting log output at DEBUG level; no full account numbers, emails, tokens, or passwords appear in any log statement |
| ☐ | Complete when financial UI animations complete in ≤ 200ms, never interpolate between price values, and have `prefers-reduced-motion: reduce` fallbacks to instant | Verify every animation duration via inspection; price change indicators flash the new value instantly — no count-up or tween from old to new |
| ☐ | Complete when candlestick/OHLC charts use colorblind-safe palettes (blue-orange or equivalent) with pattern fills as secondary encoding for up/down candles | Verify charts with colorblind simulator; hollow/filled candle distinction or pattern overlay provides redundancy beyond red/green |
| ☐ | Complete when order book and trade tape update via throttled batches (≤ 100ms intervals) with final price for each batch, never dropping ticks during volatility | Verify by stress-testing with rapid price feed; UI must not freeze, and displayed prices must match the last tick in each batch |
| ☐ | Complete when all KYC/onboarding flows include: progress indicator, save-and-resume, clear error recovery on validation failure, and estimated completion time | Verify progress bar advances correctly through each step; form data persists across navigation; validation errors point to specific fields with fix instructions |

## When to Use
<!-- STANDARD: 3min -->

| Condition | Use This Skill | Use Instead |
|-----------|---------------|-------------|
| Designing trading platform UI (order books, charts, price ladders) | ✅ Apply real-time data display patterns, candlestick charts | — |
| Building banking dashboard (accounts, transactions, transfers) | ✅ High-density information layouts, compliance-driven UI | — |
| Designing payment flow (checkout, wallet, P2P transfer) | ✅ Review step, fee breakdown, irreversible action warnings | — |
| Building KYC/onboarding flow | ✅ Compliance-driven UI patterns with progress tracking | — |
| General analytics dashboard (non-financial) | ❌ | `data-visualization-engineer` |
| Backend financial system architecture | ❌ | `backend-developer` or `financial-security` |
| Cryptocurrency exchange UI | ✅ Real-time order book, trade tape, wallet integration | — |
| Insurance portal design | ✅ Claims flow, policy management, document upload patterns | — |

## Deliberate Practice
<!-- STANDARD: 3min -->

1. **Audit a real trading platform.** Open Robinhood, Coinbase, or Interactive Brokers. Count: how many data points on screen? How is gain/loss communicated? What happens when you tap "Buy" — is there a review step? Find 3 things the platform does well and 3 things that violate best practices.
2. **Design an order confirmation screen.** Create a mockup for a $10,000 stock purchase. Show: ticker + quantity, limit price, estimated total, commission/fees breakdown, settlement time (T+2), and a clear "This order cannot be undone" warning. Test with a colleague — can they understand the full cost in under 5 seconds?
3. **Build a colorblind-safe portfolio view.** Take a portfolio screen showing 5 positions (2 up, 3 down). Redesign so gain/loss is unambiguous without color: +/− signs, arrow icons, percentage text. Verify by viewing in grayscale. Then test all three colorblind types (deuteranopia, protanopia, tritanopia).
4. **Design a KYC flow end-to-end.** Map the full identity verification journey: ID upload → selfie → address verification → review → approval/rejection. Handle every error state: blurry photo, expired ID, address mismatch. Time each step — target under 3 minutes total.
5. **Optimize a real-time data display.** Given a WebSocket stream spitting 100 price updates/second, design a throttled display that updates at 100ms intervals, shows the final price per batch, and has a visible connection status indicator.

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Gain/loss shown only as red/green color — 8% of males are colorblind and cannot distinguish | $50K-$200K in accessibility lawsuit exposure; $15K-$40K in trading errors from misinterpreted signals | Always include +/− signs, up/down arrows, and percentage text. Test with colorblind simulators for all three types |
| Hidden fees only shown after confirmation — #1 cause of fintech user complaints and regulatory fines | $100K-$1M in CFPB/FCA fines for deceptive fee disclosure; 40% churn from first-time users who feel tricked | Show fee breakdown BEFORE confirm button: subtotal, platform fee, network fee, tax, total. Never use "estimated total" without full itemization |
| Real-time prices without connection status indicator — users trade on stale data thinking it's live | $25K-$500K in trade errors from stale price execution; regulatory liability for displaying outdated data as current | Persistent connection dot (green/yellow/red) + "As of [timestamp]" or "Delayed [N] minutes" on every price display |
| Abbreviated numbers (1.2M) without tooltip showing full precision — users misread scale | $10K-$100K in trading mistakes from misreading order size or position value | Hover/tap reveals full number to 2 decimal places. Abbreviation legend visible in chart footer (K=thousands, M=millions, B=billions) |
| Financial data displayed without consistent decimal places — erodes trust in platform | $50K-$200K in lost user trust and abandonment; institutional clients require formatting consistency | Standardize to 2 decimal places for currency. Integer cents internally. Format only at display layer. Zero-pad to consistent width |
| No review step on irreversible financial action (buy, sell, transfer) — accidental transactions | $50K-$5M in liability for irreversible erroneous transactions; regulatory penalties for inadequate confirmation | Mandatory review step with: amount, fees, total, delivery time, "This action cannot be undone" warning. Require explicit confirmation gesture |
| Animations interpolating between price values — shows wrong numbers during transition | $20K-$100K in trading errors from stale interpolated values; violates MiFID II best execution requirements | Flash the new value instantly. Never count-up or tween between prices. Animations ≤200ms with reduced-motion fallback to instant |

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Decision | Status | Timestamp |
|----------|--------|-----------|
| (none yet) | — | — |

## References
<!-- STANDARD: 3min -->

- [PCI DSS v4.0](https://www.pcisecuritystandards.org/document_library/) — Payment Card Industry Data Security Standard for UI compliance
- [WCAG 2.2 Guidelines](https://www.w3.org/TR/WCAG22/) — Web Content Accessibility Guidelines for financial accessibility
- [CFPB Design Guidelines](https://www.consumerfinance.gov/design/) — Consumer Financial Protection Bureau design standards
- `references/trading-interface-patterns.md` — Order book, price ladder, depth chart design patterns
- `references/banking-ux-patterns.md` — Account dashboard, transaction history, transfer flow patterns
- `references/payment-ux-patterns.md` — Checkout flows, wallet design, P2P transfer UX
- `references/compliance-ui-patterns.md` — KYC, audit trails, regulatory disclosure design
- `references/financial-data-visualization.md` — Candlestick charts, portfolio allocation, time-series patterns
- `references/fintech-colorblind-safety.md` — Colorblind-safe palettes for financial data

## Anti-Hallucination
<!-- STANDARD: 3min -->

- Admit uncertainty. If you cannot determine the correct approach, ask — do not guess.
- Flag your knowledge cutoff. If this project uses tools or patterns you have not seen, state your assumptions.
- Never guess security. If work touches auth, payments, or PII, route to security-reviewer.
- [VERIFIED] — Standard financial UI pattern (used by major brokerages/banks)
- [COMMON-PRACTICE] — Widely adopted in fintech startups and products
- [INFERRED] — Reasonable extrapolation from financial UX principles
- [UNKNOWN] — Requires verification against specific regulations or jurisdictions
