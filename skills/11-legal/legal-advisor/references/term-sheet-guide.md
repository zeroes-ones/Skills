# Term Sheet Guide

> **Author:** Sandeep Kumar Penchala

A practical guide to understanding and negotiating venture capital term sheets. Companion to the [Legal Advisor SKILL.md](../SKILL.md).

---

## 1. Term Sheet Anatomy

Term sheets divide into two categories: **economics** (how proceeds are split) and **control** (who decides what).

```
┌─────────────────────────────────────────────────────────────┐
│                    TERM SHEET STRUCTURE                     │
├──────────────────────────┬──────────────────────────────────┤
│       ECONOMICS          │            CONTROL               │
├──────────────────────────┼──────────────────────────────────┤
│ • Pre-money valuation    │ • Board composition              │
│ • Option pool            │ • Protective provisions          │
│ • Liquidation preference │ • Anti-dilution protection       │
│ • Dividend policy        │ • Redemption rights              │
│ • Conversion rights      │ • Drag-along rights              │
│ • Anti-dilution (split)  │ • Information rights             │
│ • Founder vesting        │ • Right of first refusal/co-sale │
│ • Employee pool refresh  │ • Voting agreement               │
└──────────────────────────┴──────────────────────────────────┘
```

---

## 2. Liquidation Preference

Determines payout order on exit, acquisition, or dissolution.

### Non-Participating Preferred (Standard, "1x non-participating")
Investor chooses: (a) receive 1x their investment back, OR (b) convert to common and get their pro-rata %.
- **Example:** Invest $5M at 20% ownership. Exit at $20M. Investor picks (a) $5M or (b) $4M (20% × $20M). Picks (a). Remainder $15M goes to common.

### Participating Preferred ("Double dipping")
Investor gets 1x back **plus** pro-rata share of remainder.
- **Example:** Invest $5M at 20%. Exit at $20M. Investor gets $5M + 20% × ($20M – $5M) = $5M + $3M = $8M. Common gets $12M.

### Capped Participation
Participating, but capped at 2–3x investment.
- **Example:** Invest $5M, 3x cap. Exit at $50M. Without cap: $5M + $9M = $14M. With cap: min($14M, 3 × $5M = $15M) = $14M. At $100M exit, cap creates meaningful difference.

### Exit Scenario Comparison ($5M invested, 20% ownership)

| Exit Value | Non-Participating | Participating (no cap) | Participating (3x cap) |
|---|---|---|---|
| $10M | $5M (50%) | $6M (60%) | $6M (60%) |
| $25M | $5M (20%) | $9M (36%) | $9M (36%) |
| $50M | $10M (20%) | $14M (28%) | $14M (28%) |
| $100M | $20M (20%) | $24M (24%) | $15M (15%) — cap hits |

> **Founder's note:** Push for non-participating or high-cap participation. Uncapped participation destroys founder returns at modest exits.

---

## 3. Anti-Dilution Protection

Protects investors from down rounds by adjusting their conversion price.

### Full Ratchet
Conversion price reduced to new round price, regardless of shares issued.
- **Example:** Series A at $10/share, Series B at $5/share. Investor's 1M shares convert at $5 (now 2M shares equivalent). **Extreme dilution to founders.**

### Weighted Average — Broad-Based (Standard, "Founder-friendly")
New conversion price accounts for both price and number of shares:

```
CP2 = CP1 × (CSO + NewMoney) / (CSO + SharesIssued)

Where:
CP1 = Original conversion price
CP2 = New conversion price
CSO = Common Stock Outstanding (fully diluted, including options + warrants)
NewMoney = Amount raised at new price / CP1
SharesIssued = Shares actually issued in new round
```

### Weighted Average — Narrow-Based
Same formula, but CSO = common outstanding only (excludes options, warrants). **More punitive** than broad-based.

### Dilution Comparison: $10/share → $5/share down round

| Protection Type | New Conversion Price | Investor Shares After | Founder Dilution |
|---|---|---|---|
| Full Ratchet | $5.00 | 2,000,000 | Severe |
| Narrow-Based WA | ~$6.67 | ~1,500,000 | Moderate |
| Broad-Based WA | ~$8.33 | ~1,200,000 | Minimal |

---

## 4. Board Composition

### Standard Early-Stage (3–5 seats)

```
SERIES A BOARD (5 seats)
├── Common Directors (2): CEO + 1 founder/operator
├── Preferred Directors (2): Lead investor + 1 other investor
└── Independent Director (1): Agreed by both parties
```

### Considerations
- **Pre-Series A:** 3 seats (2 common, 1 investor optional)
- **Series B+:** Independent becomes 2 seats; investors may gain majority
- **Never give investors board control pre-Series B.** Maintain founder majority or at least parity.

---

## 5. Protective Provisions (Veto Rights)

### Standard (NCVA/NVCA Model)
- Amend Certificate of Incorporation
- Authorize new class/series of stock
- Redeem or repurchase shares
- Declare dividends
- Change board size
- Liquidate, dissolve, or wind up
- Sell the company or substantially all assets

### Aggressive (Push Back)
- Create subsidiaries
- Incur debt over $X
- Change principal line of business
- Hire/fire C-suite executives
- Approve annual budget
- Enter into material contracts over $X
- Settle litigation over $X

---

## 6. Additional Rights Explained

### Redemption Rights
Investor can force company to repurchase shares after X years (typically 5–7). Rarely exercised but creates balance-sheet liability. **Push for:** no redemption, or redemption only at board discretion.

### Drag-Along Rights
Majority (or supermajority) can force all shareholders to participate in a sale. **Standard:** majority of preferred + board approval. Prevents holdout shareholders from blocking a good exit.

### Tag-Along (Co-Sale) Rights
Minority shareholders can participate pro-rata if a major shareholder sells. Protects founders and early investors from being left behind.

### Registration Rights
- **Demand registration:** Investor can force company to file S-1 (IPO registration)
- **Piggyback registration:** Right to include shares in company-initiated registration
- **S-3/F-3 rights:** Short-form registration once eligible
- **Lock-up period:** 180 days standard; investors agree not to sell post-IPO

---

## 7. Founder Vesting Acceleration

### Single-Trigger Acceleration
Vesting accelerates on acquisition. **Very rare post-Series A.** Seen in founder-friendly deals or acqui-hires.

### Double-Trigger Acceleration (Standard)
Vesting accelerates only if **both** (a) company is acquired **and** (b) founder is terminated without cause or resigns for good reason within 12 months.

### Negotiation Spectrum
```
Single-Trigger ──────── Double Full ──────── Double Partial ──────── No Acceleration
(founder-favored)      (standard)          (50% common)           (investor-favored)
```

### Good Reason Definition (Trigger Events)
- Material reduction in role, title, or responsibilities
- Reduction in base compensation > 10%
- Relocation > 50 miles
- Company's material breach of employment agreement

---

## 8. Key Terms Cheat Sheet

| Term | What to Push For | What to Resist |
|---|---|---|
| **Liquidation preference** | 1x non-participating | >1x, participating, uncapped |
| **Anti-dilution** | Broad-based weighted average | Full ratchet |
| **Board** | Founder majority or parity | Investor majority (pre-Series B) |
| **Protective provisions** | NVCA standard list | Operational vetoes |
| **Vesting** | Standard 4yr/1yr cliff | No cliff, single-trigger acceleration |
| **Dividends** | Non-cumulative, board discretion | Cumulative, compounding |
| **Redemption** | None or board-only | Mandatory redemption |
| **Option pool** | 10–15% pre-money | >20% pre-money (over-dilutes founders) |

---

## 9. Negotiation Mindset

1. **Focus on the nasty scenarios.** Term sheets feel theoretical at $50M+ exit scenarios, but protective provisions and liquidation preferences bite hardest in modest exits or down rounds.
2. **Everything is negotiable.** "Market standard" means "this is my opening position."
3. **Lawyer up, but lead the negotiation yourself.** Investors want to negotiate with founders, not attorneys.
4. **Multiple term sheets = leverage.** Run a process; competitive tension is the founder's best friend.
5. **The relationship matters more than 5% economics.** A supportive investor on your board is worth more than slightly better terms from a bad partner.

---

*This guide is educational, not legal advice. Consult qualified counsel before signing any term sheet.*
