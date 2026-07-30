# Session Liquidity Guide

## Global FX Sessions (Times in GMT/UTC)

| Session | Hours (GMT) | Hours (ET) | Key Centers | Characteristics |
|---|---|---|---|---|
| Asia-Pacific | 00:00 - 09:00 | 19:00 - 04:00 | Tokyo, Sydney, Singapore, Hong Kong | JPY, AUD, NZD active. Other pairs thin. Spreads 2-4× wider. Risk: gap opens on weekend. |
| London | 08:00 - 17:00 | 03:00 - 12:00 | London, Frankfurt, Zurich | Highest volume session. All European pairs active. EUR, GBP, CHF dominant. Tightest spreads. |
| London/NY Overlap | 13:00 - 17:00 | 08:00 - 12:00 | London + New York | HIGHEST liquidity of the day. All majors at tightest spreads. 70% of daily FX volume in these 4 hours. BEST TIME TO TRADE. |
| New York Only | 17:00 - 22:00 | 12:00 - 17:00 | New York, Toronto | USD, CAD active. European desks closing. Volume declining. US economic data releases 8:30 AM - 10:00 AM ET. |
| Post-NY / Pre-Asia | 22:00 - 00:00 | 17:00 - 19:00 | Wellington opens | Lowest liquidity. DO NOT trade. Spreads can be 5-10× normal. Rollover at 5 PM ET (22:00 GMT). |

## Pair-Session Matching Matrix

| Pair | Best Session | Acceptable Session | Avoid | Spread (Best) | Spread (Avoid) |
|---|---|---|---|---|---|
| EUR/USD | London/NY Overlap | London | Asia (00-08 GMT) | 0.1-0.3 pips | 1-2 pips |
| GBP/USD | London/NY Overlap | London | Asia (00-08 GMT) | 0.3-0.8 pips | 2-5 pips |
| USD/JPY | London/NY Overlap | Asia (Tokyo hours) | Post-NY (22-00 GMT) | 0.2-0.5 pips | 2-4 pips |
| USD/CHF | London/NY Overlap | London | Asia (00-08 GMT) | 0.3-0.8 pips | 2-5 pips |
| AUD/USD | Asia (Sydney/Tokyo) | London/NY Overlap | Post-NY (22-00 GMT) | 0.5-1.0 pips | 3-5 pips |
| NZD/USD | Asia (Wellington open) | Asia | London early | 0.5-1.5 pips | 3-7 pips |
| USD/CAD | NY Only (US data) | London/NY Overlap | Asia | 0.5-1.5 pips | 3-6 pips |
| EUR/JPY | London/NY Overlap | Asia (Tokyo) | Post-NY | 0.5-1.5 pips | 3-8 pips |
| GBP/JPY | London/NY Overlap | London | Asia | 0.8-2.0 pips | 4-10 pips |
| EUR/GBP | London | London/NY Overlap | Asia | 0.2-0.5 pips | 1-3 pips |

## Economic Data Release Windows (ET)

| Time (ET) | Typical Releases | Currency Impact | Trading Rule |
|---|---|---|---|
| 8:30 AM | NFP, CPI, PPI, Retail Sales, GDP, Trade Balance | USD, sometimes CAD | Wait 5 minutes after release. First move is usually wrong (algos fighting). Trade the second move or fade the spike |
| 9:45 AM | PMI (flash/final) | USD | Lower impact unless >5pt deviation from consensus |
| 10:00 AM | ISM Manufacturing/Services, Consumer Sentiment, New Home Sales | USD | ISM has higher impact than PMI. Watch employment sub-index |
| 2:00 PM | FOMC minutes, Fed Beige Book | USD | Often causes reversals of post-FOMC moves |
| 4:30 AM | UK CPI, GDP, employment | GBP | GBP can move 100+ pips on CPI surprise |
| 5:00 AM | Eurozone GDP, German ZEW, Ifo | EUR | German data dominates. ZEW is expectations — leading |

## Spread Widening Events

When spreads WIDEN 3× or more:
- Immediately cancel all market orders
- Switch pending entries to limit orders ONLY
- Widen stop-losses by 50% (the spread will eat tight stops)
- Common causes: news surprise, thin session, weekend open, bank holiday in one major center (e.g., London closed but NY open = EUR thin)

