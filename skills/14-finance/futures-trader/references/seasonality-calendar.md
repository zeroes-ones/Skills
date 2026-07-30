# Seasonality Calendar

> Commodity seasonality tables: bullish/bearish windows per commodity, transition dates, historical reliability scores.

## Seasonality Scorecard

| Commodity | Symbol | Bullish Window | Bearish Window | Transition Dates | Historical Reliability | Primary Driver |
|-----------|--------|---------------|----------------|-----------------|----------------------|----------------|
| Corn | ZC | Mar – Jun | Jul – Sep | Jun 30 (acreage report) | 65% (20yr) | Planting weather, acreage reports |
| Soybeans | ZS | Feb – May | Jun – Aug | Jun 30 (acreage) | 60% (20yr) | SA weather → US growing season |
| Wheat | ZW | Sep – Nov | Mar – May | Dec 1 (winter wheat dormancy) | 55% (20yr) | Northern Hemisphere crop cycle |
| Cotton | CT | Feb – Apr | Jul – Sep | Apr 30 (planting progress) | 60% (20yr) | Planting intentions, weather |
| Coffee | KC | May – Jul | Oct – Dec | Jul 15 (Brazil frost season end) | 58% (20yr) | Brazilian winter (frost risk) |
| Natural Gas | NG | Aug – Oct | Mar – May | Oct 31 (storage peak) | 70% (20yr) | Storage build/draw, weather |
| Crude Oil | CL | Feb – Apr, Jun – Aug | Sep – Nov | Sep 15 (refinery turnaround) | 55% (20yr) | Driving season, refinery maint |
| Heating Oil | HO | Sep – Nov | Mar – May | Nov 15 (heating season start) | 65% (20yr) | Winter heating demand |
| Gasoline | RB | Feb – Apr | Sep – Nov | Apr 15 (summer blend switch) | 60% (20yr) | Driving season, blend changes |
| Gold | GC | Dec – Feb | Jun – Aug | Jan 1 (new year demand) | 55% (20yr) | Jewelry demand, festivals |
| S&P 500 | ES | Nov – Apr | May – Oct | May 1 ("Sell in May") | 62% (50yr) | Tax/calendar effects |
| Treasury Bonds | ZB | Aug – Oct | Mar – May | Sep 15 (FOMC cycle) | 55% (20yr) | Rate expectations, issuance |

## Grain Seasonality Detail

### Corn (ZC)

```
Jan – Feb: Winter doldrums. Low volatility. South American crop developing.
Mar – May: PLANTING WEATHER PREMIUM. Wet spring = delayed planting = bullish.
May – Jun: Weather market peaks. Key reports: WASDE (monthly), Acreage (Jun 30).
Jul – Aug: POLLINATION. Most critical 2-week period (mid-Jul). Heat/drought = price spikes.
Sep – Oct: HARVEST PRESSURE. New crop supply hits. Typically bearish.
Nov – Dec: Post-harvest recovery. Export demand picks up.
```

### Soybeans (ZS)

```
Jan – Feb: South American weather (Brazil/Argentina crop development).
Mar – Apr: US planting intentions. Acreage battle: corn vs soybeans.
May – Jun: US planting. Late planting = shift acres to soybeans (bearish soy vs corn).
Jul – Aug: POD-SETTING. Critical month. Aug WASDE = first survey-based yield estimate.
Sep – Oct: HARVEST PRESSURE. Record crops = price lows.
Nov – Dec: Export demand from China. Post-harvest rally potential.
```

## Energy Seasonality Detail

### Natural Gas (NG)

```
Jan – Feb: PEAK WITHDRAWAL. Coldest months. Storage depletes rapidly.
Mar – May: SHOULDER SEASON. Injection begins. Typically lowest prices of year.
Jun – Aug: COOLING DEMAND. Power generation for AC. Moderate support.
Sep – Oct: HURRICANE SEASON. Gulf of Mexico supply risk. Storage peak approaches.
Nov – Dec: WITHDRAWAL BEGINS. First cold snap = price spike potential.
```

### Crude Oil (CL)

```
Jan – Feb: REFINERY MAINTENANCE. Lower crude demand. Bearish.
Mar – May: PRE-DRIVING SEASON. Refineries restart. Bullish setup.
Jun – Aug: DRIVING SEASON. Peak gasoline demand. Bullish for crude.
Sep – Oct: HURRICANE SEASON. Gulf supply disruption risk.
Nov – Dec: YEAR-END. OPEC meetings. Tax-loss selling. Mixed.
```

## Equity Index Seasonality

### S&P 500 (ES) — The "Sell in May" Pattern

```
Nov – Jan: SANTA CLAUS RALLY. Year-end positioning. Strongest 3-month period historically.
Feb – Apr: EARNINGS SEASON. Q4 earnings + Q1 guidance. Normally positive.
May – Jul: "SELL IN MAY AND GO AWAY." Historically weakest 6-month period (May-Oct).
Aug – Sep: Historically the two worst months for equities. Volatility spikes.
Oct: "OCTOBER EFFECT." Crash month historically (1929, 1987, 2008). Also often a buying opportunity.
```

## Using Seasonality

### Integration Rules

1. Seasonality provides **bias**, not **timing** — always combine with technical analysis
2. Seasonal patterns have **60-70% historical reliability** — 30-40% of years break the pattern
3. **Transition dates** matter more than the window itself — the 2 weeks around transitions see the largest moves
4. The strongest seasonal trades are those where **seasonality + COT + technicals** all align

### Position Sizing by Seasonal Alignment

| Seasonal Alignment | Position Size | Rationale |
|-------------------|--------------|-----------|
| Bullish season + bullish technicals + COT supportive | 100% (full size) | All three aligned |
| Bullish season + neutral technicals | 50-75% | Partial alignment |
| Bullish season + bearish technicals | 25-50% or wait | Seasonality alone is not enough |
| Bearish season + bullish technicals | 25-50% | Counter-seasonal strength = significant |
| Bearish season + bearish technicals + COT supportive | 100% (full short) | All three aligned bearish |
- **Neutral season** | Size purely on technicals and COT | Seasonality provides no edge |

## Key Report Dates

| Date | Report | Impact |
|------|--------|--------|
| 2nd week each month | WASDE (World Agricultural Supply and Demand Estimates) | HIGH for grains |
| Last week each month | EIA Short-Term Energy Outlook | HIGH for energy |
| Jun 30 | USDA Acreage Report | EXTREME for grains |
| Sep 30 | USDA Quarterly Grain Stocks | HIGH for grains |
| 1st week each month | OPEC+ Meeting | HIGH for crude oil |
| Every Thursday | EIA Natural Gas Storage Report | HIGH for NG |

**Always check the USDA, EIA, and CFTC release calendars for exact dates.** Reports routinely move markets 3-5% in minutes.

