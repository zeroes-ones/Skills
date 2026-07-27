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

## Route the Request

### Auto-Route

| # | Condition | Action |
|---|-----------|--------|
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

## Ground Rules

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|--------------------|
| G1 | Never display financial data without a timestamp — "last updated" is as important as the number | `file_contains(output, "$|USD|price|balance")` AND NOT `file_contains(output, "as of|updated|timestamp|delay")` | REFUSE. "Financial data is time-sensitive. Every price, balance, or rate must show 'As of [timestamp]' or 'Delayed [N] minutes.'" |
| G2 | Never convey gain/loss by color alone (red/green) — always include +/− sign and percentage text | `file_contains(output, "green|red")` AND NOT `file_contains(output, "\\+|\\-|arrow.up|arrow.down|increase|decrease")` | DETECT. "Color-only indicators fail for colorblind users and grayscale displays. Always include +/− signs, arrow icons, and text percentage." |
| G3 | Never show a confirmatory action (buy, sell, transfer) without a review step showing all fees, totals, and irreversible consequences | `file_contains(output, "confirm|submit|buy|sell|transfer")` AND NOT `file_contains(output, "fee|total|review|are you sure|irreversible")` | REFUSE. "Financial transactions require a review step. Show: breakdown of fees, total amount, delivery time, and a clear 'This action cannot be undone' warning." |
| G4 | Never abbreviate large numbers without a consistent legend and tooltip with full precision | `file_contains(output, "K|M|B|T")` AND NOT `file_contains(output, "legend|tooltip|exact")` | STOP. "Abbreviated numbers must show full precision on hover/tap. '$1.2M' must reveal '$1,234,567.89' with the abbreviation legend visible." |
| G5 | Never display user financial data without end-to-end encryption indicators (lock icon, "Secured by" label) | `file_contains(output, "account|balance|portfolio")` AND NOT `file_contains(output, "secure|encrypt|lock|256-bit|SSL|TLS")` | DETECT. "Financial applications must display security assurance indicators. Show lock icon + encryption status in persistent chrome." |

## The Expert's Mindset

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

| Level | User | Scope | What Changes |
|-------|------|-------|-------------|
| **L1 — Apprentice** | Junior designer building a simple budget tracker | Single account view with balance and transactions | Learn financial data display: currency formatting, date handling, gain/loss indicators. |
| **L2 — Solo** | Startup building a fintech MVP | Multi-account dashboard, basic transactions | Add security indicators, KYC flow, fee disclosures. Test with colorblind simulation. |
| **L3 — Small Team** | Growing fintech with real users | Trading, portfolios, compliance flows | Real-time WebSocket data. Multi-currency support. Audit trail in UI. Regulatory disclosures per jurisdiction. |
| **L4 — Medium** | Established fintech, multiple products | Multi-product platform with shared design system | Design system with financial component library. Accessibility at WCAG 2.2 AA minimum. Multi-region compliance. Performance monitoring on data feeds. |
| **L5 — Enterprise** | Bank, exchange, or major fintech | White-label platform, institutional + retail | Institutional-grade data density. Customizable dashboards per user role. SOC 2, PCI-DSS, GDPR compliance built into UI components. Audit-every-click tracking. |

## Core Workflow

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

## Trading Interfaces

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

| Trigger | Action | Why |
|---------|--------|-----|
| Transaction confirmation without fee breakdown | Flag: "Show all fees before confirming. Users must see: subtotal, fees, total, and delivery time." | Hidden fees are the #1 cause of fintech user complaints and regulatory action. |
| Gain/loss shown only as red/green color | Flag: "Add +/− signs and percentage text. 8% of males are colorblind — they can't distinguish red from green." | Color-only indicators fail accessibility and cause trading errors. |
| Numbers without consistent decimal places | Flag: "Standardize to 2 decimal places for currency. Inconsistent formatting erodes trust." | Users notice formatting inconsistencies and interpret them as errors. |
| Real-time data without connection status | Flag: "Add connection indicator (green/yellow/red dot). User must know if prices are live or stale." | Trading on stale data causes financial loss. |
| "Submit" or "Confirm" on destructive financial action | Flag: "Add review step with: amount, fees, delivery time, and 'This cannot be undone' warning." | Accidental transactions are irreversible in many financial systems. |

## What Good Looks Like

> The dashboard loads in under 2 seconds with skeleton screens for every data region. Prices update via WebSocket with a green connection dot. Every gain/loss has +/− sign, arrow icon, and color (checked with colorblind simulation). The order entry form shows estimated total with fee breakdown before the review step. The review step shows a clear "This order cannot be undone" warning. All tables are navigable by screen reader with proper ARIA roles. Currency is formatted consistently to 2 decimal places across every screen. The "last updated" timestamp is visible in the persistent header. Security indicators (lock icon, "256-bit TLS encryption") appear in the footer or status bar.

## Error Recovery

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Users complain about "hidden fees" | Fee breakdown only shown after confirmation, not before | Move fee disclosure BEFORE the confirm button. Show line items. Never use "estimated total" without itemization. |
| Colorblind users can't tell if they're up or down | Red/green-only gain/loss indicators | Add +/− signs, up/down arrows, and percentage text. Test with colorblind simulators. |
| Prices showing as "$0.000000" | Floating-point precision error in display | Format all currency to 2 decimal places. Use integer cents internally, format for display. |
| Real-time chart freezes during volatility | Too many re-renders per second | Throttle updates to 100ms batches. Drop intermediate ticks; show final price for each batch. |

## Anti-Hallucination

- [VERIFIED] — Standard financial UI pattern (used by major brokerages/banks)
- [COMMON-PRACTICE] — Widely adopted in fintech startups and products
- [INFERRED] — Reasonable extrapolation from financial UX principles
- [UNKNOWN] — Requires verification against specific regulations or jurisdictions
