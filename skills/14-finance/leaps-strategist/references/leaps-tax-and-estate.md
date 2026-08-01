# LEAPS Tax & Estate Planning

> **Portability target:** Spec-level. Tax concepts reference US tax code — adapt for non-US jurisdictions. This is NOT tax advice. Consult a tax professional.

## The Tax Reality

LEAPS create tax situations that short-dated options don't. Most LEAPS traders ignore taxes until April — then discover they owe $5K on trades that "felt profitable" after commissions but weren't after taxes.

## LEAPS vs. Shares: Tax Comparison

| Feature | Shares | LEAPS |
|---------|--------|-------|
| Long-term capital gains (LTCG) | After 1 year holding | After 1 year holding (for equity LEAPS) |
| Qualified dividends | Taxed at LTCG rate (0-20%) | No dividends received — no qualified dividend benefit |
| Short-term gains (STCG) | Sold < 1 year = ordinary income | Closed < 1 year = ordinary income |
| Section 1256 treatment | No | Only index LEAPS (SPX, NDX, RUT): 60% LTCG / 40% STCG regardless of holding period |
| Wash sale applicability | Yes — 30-day window | Yes — different strike or expiration IS "substantially identical" per IRS |
| Straddle rules | No | Yes — if you hold offsetting positions in the same underlying |

## Section 1256: The Index LEAPS Advantage

Index options (SPX, NDX, RUT) are Section 1256 contracts. This is a massive tax advantage:

| Holding Period | Equity LEAPS Tax | SPX LEAPS Tax |
|---------------|-----------------|---------------|
| < 1 year | Ordinary income (up to 37%) | 60% LTCG + 40% STCG (blended ~26.8% at top bracket) |
| > 1 year | LTCG (up to 20%) | 60% LTCG + 40% STCG (same — 1256 overrides holding period) |

**Bottom line:** SPX LEAPS settled in < 1 year save ~10% in taxes vs. equity LEAPS. SPX DITM calls for stock replacement are tax-superior to AAPL DITM calls if your holding period may be < 1 year.

## Wash Sale Traps

The IRS considers options with different strikes or expirations on the same underlying as "substantially identical." Standard LEAPS transactions that trigger wash sales:

| Scenario | Wash Sale? | Consequence |
|----------|-----------|------------|
| Sell LEAPS at loss, buy same-strike LEAPS within 30 days | YES | Loss disallowed, added to new position basis |
| Sell LEAPS at loss, buy different-strike LEAPS on same stock within 30 days | YES | IRS position: different strike = substantially identical for options |
| Sell LEAPS at loss, buy shares within 30 days | YES | Options → shares can trigger wash sale |
| Sell LEAPS at loss in taxable account, buy in IRA within 30 days | YES | IRA purchase triggers wash sale — AND the loss is permanently disallowed (not just deferred) |
| Sell Jan 2027 LEAPS at loss, buy Jan 2028 LEAPS within 30 days | YES | Different expiration does NOT avoid wash sale |

**Rule:** If selling a LEAPS at a loss, wait 31 days before re-entering any position (option or stock) in the same underlying. The 30-day wash window applies bidirectionally.

## PMCC Tax Nuances

The Poor Man's Covered Call creates recurring short-term gains:

- Short call premium: ALWAYS short-term capital gain (regardless of holding period)
- LEAPS sale (if assigned or closed): Holding period determines LTCG vs STCG
- Assignment: If short call is assigned, the LEAPS is typically sold to cover — realizing gain/loss at that point

**PMCC tax drag:** Even if the LEAPS qualifies for LTCG (held > 1 year), the short calls generate STCG every 30-45 days. At top bracket, this is 37% vs. 20%. Over 12 short-call cycles, the tax drag is $800-$2,000/year per PMCC position.

## Estate Planning with LEAPS

LEAPS have one estate planning advantage: the stepped-up basis.

- **Shares:** Upon death, heirs receive stepped-up basis to FMV at date of death. All unrealized gains eliminated.
- **LEAPS:** Same stepped-up basis treatment. LEAPS held until death receive basis step-up.

**Strategy:** For highly appreciated positions with large unrealized gains, rolling to long-dated LEAPS (while managing the tax impact of the initial sale) can preserve exposure while planning for eventual step-up.

## Record-Keeping Requirements

- [ ] Every LEAPS purchase: date, strike, expiration, premium paid, extrinsic at entry
- [ ] Every LEAPS sale/close: date, proceeds, gain/loss, holding period, tax lot
- [ ] Every short call (PMCC): date, strike, expiration, premium received, gain/loss
- [ ] Every roll: both legs recorded separately with reason for roll
- [ ] Year-end: realized gain/loss summary, unrealized positions with acquisition dates
