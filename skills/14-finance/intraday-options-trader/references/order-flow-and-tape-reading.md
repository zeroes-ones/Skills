# Order Flow & Tape Reading for Intraday Options

> **Portability target:** Spec-level. Vendor-agnostic concepts — adapt to any broker's time & sales feed.

## When to Use This Reference

Load this when entering intraday momentum/ORB trades using options. Tape reading tells you whether the price move has institutional backing or is noise. Options are more expensive than shares — every trade needs a structural reason from order flow.

## The Core Question

Every intraday options trade must answer: **Is the move real or noise?**

- Real move: Large prints, VWAP support, accumulation/distribution visible in tape
- Noise: Small lot trades, no volume confirmation, spread widening during the move

## Time & Sales Signals

| Signal | Meaning | Options Implication |
|--------|---------|-------------------|
| Large prints (500+ lots, equity) at offer | Institutional buying — real demand | Favor calls, expect continuation |
| Large prints at bid | Institutional selling — real pressure | Favor puts, expect continuation |
| Small prints only (sub-100 lots) | Retail noise — no institutional conviction | Skip or halve size; the edge is coin-flip |
| Block trades at VWAP | Passive rebalancing — not directional | No signal either way — fade moves off blocks |
| Sweep orders clearing multiple levels | Aggressive demand — urgent execution | High probability of continuation; enter momentum |
| Iceberg orders (repeated same-size prints) | Hidden institutional size — stealth accumulation | Strong signal in direction of iceberg prints |
| Tape speed acceleration | Event or news-driven — algo reaction | Wait 30-60 seconds for algos to settle before entering |

## Options-Specific Order Flow

| Flow Type | Signal | When to Fade |
|-----------|--------|-------------|
| Unusual call buying (10× OI, offer-side) | Bullish positioning | If volume dries up within 5 minutes — fade |
| Unusual put buying (10× OI, offer-side) | Bearish positioning | If it's pre-earnings positioning — fade |
| Call selling at bid (large size) | Bearish — overwriting or closing | Confirm with tape — selling could be delta-hedge |
| Sweep of ATM calls + put sales | Synthetic long — extremely bullish | Follow with calls or debit spreads |
| Delta-neutral large flow (balanced) | No directional signal — vol trade | Don't trade directionally off vol flow |

## FalseStopGuard: 4-Layer Exit Confirmation

Adapted from the Trading project's backtest (1,068 trades). Premature exits on noise were the #1 cause of underperformance.

1. **Liquidity check:** Is the pullback on increased volume? If volume < 50% of entry-bar volume, it's noise — hold.
2. **Wick analysis:** Is the pullback candle > 60% wick on the reversal side? If yes, buyers stepped in — hold.
3. **Volume context:** Did volume expand at the pullback OR at the reversal? Volume at reversal = real demand — hold.
4. **Thin-window check:** Is this within 15 minutes of open/close? If yes, liquidity is thin → widen stop by 10%.

**Rule:** Need 2+ layers to confirm before triggering a stop. One layer alone = noise.

## When Tape Reading Fails

- **Low-volume options:** Prints are sparse — no reliable signal from option tape alone. Use equity tape.
- **PFOF routing:** Robinhood/Webull fill data is NOT real market flow. It's internalized. Don't read tape.
- **First and last 5 minutes:** Tape is chaotic. Algos and market makers dominate. No retail edge.
- **Index options (SPX/NDX):** No equity tape. Use futures order flow (ES/NQ) as proxy.

## Checklist: Before Entering on Tape Signal

- [ ] Equity tape confirms: large prints at offer (calls) or bid (puts)
- [ ] NOT entering in first 2 minutes of open
- [ ] NOT entering in final 15 minutes before close
- [ ] Spread < 5% of option price for equity options, < 2% for SPX
- [ ] FalseStopGuard configured: all 4 layers active before stop triggers
- [ ] Size: standard intraday size (no doubling on "conviction" from tape)
