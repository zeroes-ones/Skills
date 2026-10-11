# Sizing Bands — Full Table

Companion to `SKILL.md` Decision Tree 1.

## Per-idea risk bands by setup class × DTE

| Setup class | DTE 2–7d | DTE 8–14d | DTE 15–45d | DTE 45d+ |
|---|---|---|---|---|
| Momentum fly / butterfly (defined risk) | 0.5% · 1 lot | 1.0% · 1–2 lots | 1.5% · 1–2 lots | n/a (use LEAP band) |
| Debit spread / vertical | — | 1.0% · 1 lot | 1.5% · 1–2 lots | 1.5% · 1–2 lots |
| Single directional call/put (naked long) | AVOID | 0.75% · 1 lot | 1.0% · 1 lot | 2.0% max · 1–2 lots (liquid names only) |
| Calendar / diagonal | — | 1.0% · 1 lot | 1.5% · 1 lot | — |
| Hedge (protective) | sized by exposure, not expectancy | | | |

**Hard caps (always):**
- Single idea max loss ≤ $300–600 (≈1.5% of a typical retail trading account).
- Total open risk across the whole book ≤ 10% of trading capital.
- Concurrent short-dated (≤45d) ideas ≤ 5.
- Correlated names (same theme/sector/underlying driver) count as ONE idea against both caps.

## What the band means in dollars

| Trading capital | 0.5% | 0.75% | 1.0% | 1.5% | 2.0% |
|---|---|---|---|---|---|
| $5,000 | $25 | $37 | $50 | $75 | $100 |
| $10,000 | $50 | $75 | $100 | $150 | $200 |
| $25,000 | $125 | $187 | $250 | $375 | $500 |
| $50,000 | $250 | $375 | $500 | $750 | $1,000 |
| $100,000 | $500 | $750 | $1,000 | $1,500 | $2,000 |

**Contracts = floor(band $ ÷ max-loss per contract).** If the floor is 0, the structure is too big for the account — pick a narrower/cheaper structure or skip. Never round up "because it's close".

## Contract-count honesty checks

- A "1-lot cap" on a $2,000-debit structure is a $2,000 risk — if that exceeds the band, the cap is meaningless; cut the structure, not the count.
- Width-driven risk (spreads) is fixed at width × 100 − credit; premium-driven risk (longs) moves with entry price. Re-check after every re-quote.
- Add the exit spread: a thin book can add 20–30% to the real risk on a naked long.
