---
author: Sandeep Kumar Penchala
type: reference
domain: fundraising
version: "1.0"
last_updated: 2026-07-21
parent_skill: ceo-strategist
---

# Fundraising Playbook — From Prep to Close

> **Author:** Sandeep Kumar Penchala

A step-by-step guide to raising venture capital. Covers instrument selection, deck construction, investor pipeline management, term sheet negotiation, data room preparation, and timeline management. Use alongside the CEO Strategist skill's equity and cap table guidance.

---

## 1. SAFE vs Priced Round — Decision Framework

| Factor | SAFE | Priced Round (Series Seed/A) |
|--------|------|------------------------------|
| **Speed** | Days to weeks | 6–12 weeks |
| **Legal cost** | $2K–$5K | $30K–$80K |
| **Valuation** | Valuation cap (not priced) | Priced valuation set |
| **Board seat** | No board rights | Typically 1 investor director |
| **Investor rights** | No information/pro-rata by default | Full suite of rights negotiated |
| **Best for** | Pre-seed, Seed, bridge rounds | Series A+ |
| **Dilution clarity** | Deferred — converts at next priced round | Immediate — known ownership % |

**Decision heuristic:**
```
if company_stage == "pre-seed" or round_size < $2M → SAFE
if company_stage == "seed" and lead_investor_committed → SAFE (MFN) or Priced Seed
if company_stage == "series-a" and revenue > $1M ARR → Priced Round
if timeline_urgent → SAFE with valuation cap
```

**SAFE variants to know:**
- **Cap, no discount** — simplest, most founder-friendly
- **Cap + discount** — most common; discount applies if next round < cap
- **MFN (Most Favored Nation)** — no cap/discount set now; matches best later terms
- **Y Combinator Post-Money SAFE** — cap is post-money (simpler dilution math)

---

## 2. Pitch Deck Structure — 10–12 Slides with Key Metrics

| Slide | Title | Key Data Points |
|-------|-------|----------------|
| 1 | **Title** | Logo, tagline, presenter name, contact |
| 2 | **Problem** | TAM/SAM/SOM in $, pain quantification, current solutions fail why |
| 3 | **Solution** | Product screenshot/GIF, core value prop, why *now* |
| 4 | **Market Size** | TAM, growth rate (CAGR %), market tailwinds |
| 5 | **Product** | Demo video/GIF, architecture differentiator, key tech moat |
| 6 | **Traction** | Revenue (MRR/ARR), growth rate (MoM %), logos, NPS > 40, churn < 5% |
| 7 | **Business Model** | Pricing tiers, ACV, LTV:CAC > 3:1, gross margin % |
| 8 | **Competition** | 2×2 matrix or feature comparison, defensible moat |
| 9 | **Team** | Founders with relevant exits/experience, key advisors |
| 10 | **Financials** | 3-year projection: revenue, burn, headcount, break-even month |
| 11 | **The Ask** | Amount raising, instrument, use of funds (pie chart), runway extension |
| 12 | **Appendix** (optional) | Detailed financials, cap table, customer references |

**Metrics investors will drill into:**
- **Seed:** MoM growth rate > 15%, engagement (DAU/MAU > 40%), qualitative customer love
- **Series A:** ARR > $1M, net revenue retention > 100%, CAC payback < 12 months
- **Series B:** ARR > $5M, multiple revenue streams, scalable GTM engine

---

## 3. Investor Pipeline Management

### CRM Template (spreadsheet columns)

```
| Company | Contact | Role | Stage | Last Touch | Next Step | Warmth | Notes |
|---------|---------|------|-------|------------|-----------|--------|-------|
| Sequoia | Jane D.  | GP   | Pitch sent | 07/15 | Partner meeting 07/22 | 🔥 | Likes team |
```

### Pipeline stages
1. **Research** — identify target funds (stage fit, sector fit, check size)
2. **Warm intro** — via mutual connection, portfolio founder, or accelerator
3. **Initial meeting** — 30 min, deck walkthrough, no deep dive
4. **Partner meeting** — full team, product demo, Q&A
5. **Deep dive** — metrics review, customer references, technical diligence
6. **Term sheet** — received, reviewed with counsel
7. **Due diligence** — data room opened, legal/financial review
8. **Close** — docs signed, wire received

### Follow-up cadence after pitch
```
Day 0:      Send deck + 3-sentence recap within 2 hours
Day 3:      Follow-up with one new data point (customer win, metric milestone)
Day 7:      Share team update or product launch (keep top of mind)
Day 14:     Gentle nudge — "Closing round by [date], would love your thoughts"
Day 21:     Final check-in — "Wrapping up, last chance to participate"
```

### Parallel tracking rule
> Run 15–20 investor conversations in parallel. Expect 20% conversion to term sheet. Never go exclusive with one fund until you have a term sheet you'd sign.

---

## 4. Term Sheet Negotiation — Key Terms Explained

### Economics
| Term | Founder-friendly | Investor-friendly | Notes |
|------|-----------------|-------------------|-------|
| **Liquidation preference** | 1x non-participating | 2x+ participating | 1x non-part = investor gets money back OR converts. Participating = double-dip |
| **Anti-dilution** | Weighted average (broad-based) | Full ratchet | Broad-based = fair; full ratchet = brutal later |
| **Dividends** | Non-cumulative, when declared | Cumulative, 8%+ | Cumulative dividends accrue and add to liquidation stack |
| **Valuation** | Higher, fewer rights | Lower, more rights | Price is one variable; don't optimize in isolation |

### Control
| Term | Founder-friendly | Investor-friendly | Notes |
|------|-----------------|-------------------|-------|
| **Board composition** | 2 founders, 1 investor, 1 independent | 1 founder, 2 investors, 1 independent | Founders should hold majority until Series B |
| **Protective provisions** | Narrow: amend charter, liquidate, incur debt > $X | Broad: hire/fire execs, budget approval, new financing | Push provisions to board-level, not investor-class |
| **Founder vesting** | 4-year with 1-year cliff, acceleration on double-trigger | Same but single-trigger or no acceleration | Double-trigger = acquisition + termination |

### Pro-rata rights
- **Standard:** investor maintains % ownership in future rounds
- **Super pro-rata:** investor can increase % ownership (rare, Series A leads only)
- **When to grant:** only to lead investors; avoid blanket pro-rata for small checks

---

## 5. Data Room Checklist — 20+ Items Organized by Category

### Corporate (Folder: `/corporate`)
- [ ] Certificate of incorporation + amendments
- [ ] Bylaws / operating agreement
- [ ] Cap table (fully diluted, including option pool)
- [ ] Board meeting minutes (last 12 months)
- [ ] Stockholder consents and voting agreements
- [ ] Employee option plan + grant ledger
- [ ] Founders' stock purchase agreements (83(b) filings)

### Commercial (Folder: `/commercial`)
- [ ] Customer list: ARR per customer, contract dates, churn history
- [ ] Top 10 customer contracts (redacted OK)
- [ ] Pipeline report: qualified opportunities, avg. deal size, close rate
- [ ] Pricing page / rate card
- [ ] Win/loss analysis (last 20 deals)
- [ ] Partner/reseller agreements

### Product & Tech (Folder: `/product`)
- [ ] Architecture diagram
- [ ] Product roadmap (next 12 months)
- [ ] Security: SOC 2 / ISO 27001 report or equivalent
- [ ] Uptime SLA history (last 12 months)
- [ ] Open-source licenses inventory
- [ ] Third-party vendor/subprocessor list

### Financials (Folder: `/financials`)
- [ ] P&L (monthly, last 24 months)
- [ ] Balance sheet (quarterly)
- [ ] Budget vs actuals
- [ ] Tax returns (last 2 years)
- [ ] Revenue recognition policy
- [ ] 3-year financial forecast with assumptions

### IP & Legal (Folder: `/legal`)
- [ ] Patent/trademark filings
- [ ] IP assignment agreements (all founders + employees)
- [ ] Material contracts (vendor > $50K, lease, loan)
- [ ] Pending or threatened litigation disclosure
- [ ] GDPR / CCPA / privacy compliance documentation

### Team (Folder: `/team`)
- [ ] Org chart
- [ ] Key employee offer letters
- [ ] Hiring plan (next 12 months)
- [ ] Compensation bands by level

---

## 6. Fundraising Timeline — Month-by-Month

```
MONTH 1: PREPARATION
├── Week 1-2: Build financial model, update pitch deck, prepare data room
├── Week 3:   Practice pitch, get feedback from 5+ trusted advisors
└── Week 4:   Target list: identify 30-50 funds, get warm intros queued

MONTH 2: FIRST MEETINGS
├── Week 5-6: 15-20 initial pitches (3-4 per day, Tue-Thu)
├── Week 7:   Follow-ups, send data room to interested funds
└── Week 8:   Partner meetings with top 8-10 funds

MONTH 3: DEEP DIVE & TERM SHEET
├── Week 9-10: Due diligence: customer calls, tech review, financial audit
├── Week 11:   Receive term sheets (target: 2-3), negotiate with counsel
└── Week 12:   Select lead, sign term sheet, announce (optional)

MONTH 4: CLOSE
├── Week 13-14: Legal documentation (definitive agreements)
├── Week 15:   Closing: signatures, wire transfer, board update
└── Week 16:   Post-close: investor onboarding, press/PR, hiring sprint
```

**Reality check:** Seed rounds close in 4–8 weeks. Series A takes 8–16 weeks. Always add 4 weeks buffer to your plan. Runway should be 6+ months when you start fundraising — never less than 3.

---

## 7. Red Flags Investors Watch For

1. **No technical co-founder** — solvable but harder; bring strong CTO advisor
2. **Co-founder conflict** — unresolved tension kills deals
3. **Full ratchet anti-dilution** on existing cap table — signals poor prior counsel
4. **Revenue concentration** — one customer > 30% of revenue
5. **Founder selling secondary** — pre-Series B, signals low conviction
6. **Over-optimistic projections** — hockey stick without credible GTM plan
7. **Burn rate out of alignment** — high burn with low growth; inefficient capital use

---

See also: CEO Strategist skill for cap table modeling, equity split frameworks, and post-raise governance.
