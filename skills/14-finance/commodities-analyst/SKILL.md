---
name: commodities-analyst
description: >
  Use when analyzing physical commodities (energy, metals, agriculture),
  supply-demand balances, inventory cycles, contango/backwardation in futures
  curves, commodity super-cycles, processing spreads (crack, crush, spark),
  or cross-commodity relative value. Handles fundamental supply-demand modeling,
  futures curve structure, seasonality, geopolitical supply risk, and
  commodity-equity nexus. Do NOT use for commodity futures execution (route
  to futures-trader), FX trading (route to forex-trader), or equity valuation
  (route to quantitative-analyst).
token_budget: 5500
chain: symmetric
consumes_from: [macro-strategist, market-data-engineer, futures-trader]
provides_to: [portfolio-signal-manager, algorithmic-trader]
---

# Commodities Analyst

> **Portability target:** Spec-level. Runs on Claude Code, Copilot CLI, Cursor, Codex, Gemini CLI.

## Route the Request

### Auto-Route

| # | Condition | Action |
|---|-----------|--------|
| A1 | Query mentions crude oil, natural gas, gasoline, heating oil, Brent, WTI | Jump to **Phase 0: Energy Complex** |
| A2 | Query mentions gold, silver, copper, platinum, palladium, base metals, precious | Jump to **Phase 1: Metals** |
| A3 | Query mentions corn, wheat, soybeans, coffee, sugar, cotton, livestock | Jump to **Phase 2: Agricultural** |
| A4 | Query mentions contango, backwardation, futures curve, calendar spread | Jump to **Phase 3: Curve Structure** |
| A5 | Query mentions crack spread, crush spread, spark spread, processing margin | Jump to **Phase 4: Processing Spreads** |
| A6 | Query mentions super-cycle, commodity cycle, secular demand, supply shock | Jump to **Phase 5: Macro Commodity** |

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to quote commodity prices from training data. Commodities move on weather, geopolitics, and inventory reports — intraday. Every price must be [VERIFIED] or [AS OF YYYY-MM-DD]. | Trigger: response contains a commodity price without [VERIFIED] or [AS OF] tag | STOP. "Commodity price unverified. Physical commodity prices change on EIA reports, USDA WASDE, weather models, OPEC+ decisions. All prices must carry provenance." |
| R2 | REFUSE to recommend a commodity trade without inventory analysis. Commodities are NOT financial assets — supply and inventory are THE price drivers. A long oil trade without knowing crude inventories, SPR levels, and spare capacity is not a trade — it's gambling. | Trigger: commodity trade recommended without inventory data (EIA, USDA, LME, COMEX warehouse) | STOP. "Inventory analysis missing. Commodity price = f(supply, demand, inventory, spare capacity). State current inventory levels, days of supply, and 5-year average before any trade recommendation." |
| R3 | REFUSE to analyze a commodity spread without specifying physical delivery dynamics. Processing spreads (crack, crush, spark) involve physical inputs and outputs. A crack spread is not a financial spread — it represents the margin of refining crude into products. | Trigger: spread analysis without physical throughput, capacity utilization, or seasonal product demand | STOP. "Physical delivery context missing for processing spread. State: refinery utilization, product demand season, and input/output price relationship before spread analysis." |
| R4 | REFUSE to compare commodity "yields" across different commodities. Gold has no yield. Copper has no coupon. A commodity's return comes from price appreciation, roll yield, and collateral yield. Comparing "carry" across metals and energies without this decomposition is meaningless. | Trigger: commodity returns compared using yield/carry without decomposing into price return, roll return, and collateral return | STOP. "Commodity return components un-decomposed. Total Return = Spot Return + Roll Return + Collateral Return. Decompose all three before comparing." |
| R5 | REFUSE to ignore seasonality in agricultural and energy commodities. Natural gas demand triples in winter. Gasoline demand peaks in summer. Corn planting is April-May, harvest September-October. Ignoring seasonality misses the single largest predictable price pattern in commodities. | Trigger: agricultural or energy commodity analysis without seasonal demand/supply calendar reference | STOP. "Seasonality omitted. Agricultural and energy commodities have strong seasonal patterns. State current seasonal position, typical seasonal price behavior, and any anomalies." |

## Verification
<!-- STANDARD: 3min -->

1. **[Price Provenance]** — Verify every commodity price includes [VERIFIED] or [AS OF YYYY-MM-DD] tag with source (exchange, EIA, USDA, LME, COMEX, ICE).
2. **[Inventory Context]** — Verify any trade thesis includes current inventory levels, days of supply, and 5-year average context.
3. **[Spread Decomposition]** — Verify processing spreads (crack, crush, spark) show their physical input/output price components explicitly.

**Pass criteria:** All checks pass before delivering output.

## Anti-Hallucination

### Provenance Tags
- `[VERIFIED]` — live data from EIA, USDA, LME, COMEX, ICE, CME, or broker terminal
- `[AS OF YYYY-MM-DD]` — historically accurate as of that date
- `[COMPUTED]` — derived from verified inputs using disclosed formula
- `[ESTIMATED]` — model-based estimate with methodology and error bounds
- `[UNVERIFIED — CHECK SOURCE]` — unable to verify; user must confirm with primary source

### Safety Protocol
Before delivering any commodity analysis, the agent MUST:
1. **Admit uncertainty** — commodity supply/demand data is reported with lags (EIA weekly, USDA monthly, OPEC monthly). Current quarter data is often estimated
2. **Flag your knowledge cutoff** — inventory levels, weather forecasts, and geopolitical events change faster than any financial asset class. Stale data in commodities is more dangerous than in equities
3. **Never guess security** — commodity futures contracts have specific delivery months, grades, and locations. WTI ≠ Brent. Hard Red Winter Wheat ≠ Soft Red Winter Wheat. Wrong grade = wrong trade

## Anti-Rationalization

| Rationalization | Reality |
|----------------|---------|
| "Oil is oil — WTI and Brent move together" | WTI-Brent spread has ranged from -$25 (WTI discount) to +$5 (WTI premium). The spread represents transportation bottlenecks, storage dynamics at Cushing, and US export capacity. Trading WTI when you meant Brent is a different trade |
| "Gold goes up when inflation is high" | Gold's relationship with inflation is inconsistent. Gold rallied in 2000-2011 (inflation was 2-3%) and fell in 2013-2015 (inflation was similar). Real yields and USD explain 80% of gold's variance. Inflation alone explains ~20% |
| "Supply disruption = buy" | Supply disruptions are often PRICED IN. The question is: is the disruption larger than what the forward curve already discounts? A 1M bbl/day disruption when the market priced 2M bbl/day means oil should FALL, not rally |
| "The futures curve is in backwardation, so it's a bullish signal" | Backwardation means spot > futures — tight nearby supply. But it ALSO means negative roll return for long positions. You lose money every time you roll. Backwardation is bullish for spot but bearish for futures holders |
| "Copper is Dr. Copper — it predicts the economy" | Copper demand is 50% China property/construction. A copper rally driven by Chinese stimulus ≠ global economic recovery. Copper's predictive power is conditional on the driver, not the price direction |

## Core Workflow

### Phase 0: Energy Complex

```
1. IDENTIFY the energy commodity
   |-- Crude oil: WTI (Cushing, OK), Brent (North Sea, waterborne), Dubai/Oman (Middle East benchmark)
   |-- Natural gas: Henry Hub (US), TTF (Europe), JKM (Asia). DIFFERENT MARKETS — not substitutes
   |-- Refined products: RBOB gasoline, ULSD (diesel/heating oil), jet fuel

2. PULL supply-demand data [VERIFIED from EIA/IEA/OPEC]
   |-- Global production (mb/d), OPEC+ quota compliance, US production (EIA weekly)
   |-- Global demand (mb/d), by region. IEA monthly. China crude imports as proxy
   |-- Implied stock change = Production - Demand (positive = surplus, builds inventory)
   |-- Spare capacity: OPEC effective spare (typically 1-3 mb/d). Below 1 mb/d = tight

3. PULL inventory data [VERIFIED]
   |-- US crude inventories (EIA weekly Wed 10:30 AM ET) — market-moving release
   |-- Cushing OK hub inventories (delivery point for WTI futures)
   |-- SPR (Strategic Petroleum Reserve) — government stockpile, policy-driven
   |-- Product inventories: gasoline, distillate. Seasonal patterns matter

4. COMPUTE curve structure
   |-- Spot vs 12-month forward: contango (futures > spot) or backwardation (spot > futures)
   |-- Contango → positive roll cost for longs. Backwardation → positive roll yield for longs
   |-- Curve steepness: M1-M6 spread, M1-M12 spread. Extreme contango = storage glut

   Complete when: Supply, demand, inventory [VERIFIED]. Curve structure computed.
   Days of forward demand cover: Total_Inventory / Daily_Demand = X days.
```

### Phase 1: Metals

```
1. CLASSIFY the metal
   |-- Precious: gold, silver, platinum, palladium. Store of value + industrial
   |-- Base/Industrial: copper, aluminum, zinc, nickel, lead, tin. Economic cycle exposure
   |-- Battery/Energy transition: lithium, cobalt, rare earths, graphite
   |-- Steel complex: iron ore, steel, metallurgical coal, scrap

2. PRECIOUS METALS drivers
   |-- Real yields (TIPS): 10yr TIPS yield — single most important gold driver. Higher real yield = lower gold
   |-- USD: DXY index. Stronger dollar = lower gold (gold is priced in USD)
   |-- Central bank buying: quarterly data. 2022-2024: record CB gold purchases
   |-- ETF flows: GLD, IAU holdings. Track weekly for sentiment
   |-- Gold-silver ratio: 80+ = silver cheap relative to gold. <60 = silver expensive

3. BASE METALS drivers
   |-- Exchange inventories: LME, SHFE, COMEX warehouse stocks. Weekly data
   |-- Treatment charges (TC/RCs): copper smelter fees. Falling TCs = concentrate shortage
   |-- China demand: property starts, grid investment, EV production. 50%+ of global copper demand
   |-- Supply disruptions: mine strikes, weather, technical issues. Concentrate market tightening
   |-- Cancelled warrants: metal booked for withdrawal from LME warehouses. Leading indicator

4. COMPUTE curve structure
   |-- LME forward curve: cash-3month spread. Backwardation = tight nearby supply
   |-- Exchange inventory ÷ daily consumption = days of supply
   |-- Below 3 days: critical tightness. Above 10 days: well supplied

   Complete when: Real yields and USD indexed [VERIFIED]. LME/SHFE/COMEX inventory [VERIFIED].
   Curve structure computed. China demand drivers identified.
```

### Phase 2: Agricultural

```
1. IDENTIFY the commodity and current crop year
   |-- Grains: corn, wheat (HRW, SRW, HRS), soybeans, rice
   |-- Softs: coffee (Arabica/Robusta), sugar (#11 raw, #5 white), cocoa, cotton, OJ
   |-- Livestock: live cattle, feeder cattle, lean hogs
   |-- Crop year ≠ calendar year: US corn Sep-Aug, soybeans Sep-Aug, wheat Jun-May, coffee Oct-Sep

2. PULL WASDE/Conab/USDA data [VERIFIED]
   |-- Planted area, harvested area, yield per acre → production estimate
   |-- Domestic use + exports = total demand
   |-- Ending stocks = Beginning stocks + Production - Total demand
   |-- Stocks-to-use ratio: ending stocks / total use. <10% = tight. >20% = ample

3. WEATHER & GROWING CONDITIONS [VERIFIED from NOAA/USDA crop progress]
   |-- Planting progress (% complete vs 5-year average)
   |-- Crop conditions: % good/excellent. Trending down? Drought monitor
   |-- El Niño/La Niña: ENSO phase. El Niño = wetter Brazil/Argentina, drier India/Australia
   |-- Key weather windows: US corn pollination (July), soybean pod-setting (August)

4. COMPUTE seasonality position
   |-- Pre-planting (Feb-Apr): weather risk premium builds
   |-- Growing season (May-Aug): weather is everything. Prices most volatile
   |-- Harvest (Sep-Nov): harvest pressure, seasonal price lows
   |-- Post-harvest (Dec-Jan): demand rationing. Storage economics

   Complete when: WASDE supply-demand table [VERIFIED or AS OF latest report].
   Stocks-to-use ratio computed. Seasonal position identified.
```

### Phase 3: Curve Structure

```
1. READ the futures curve
   |-- Contango: Futures > Spot. Normal for storable commodities. Futures = Spot + Storage + Interest - Convenience Yield
   |-- Backwardation: Spot > Futures. Tight nearby supply. Convenience yield > storage + interest
   |-- Flat: No term structure. Market in equilibrium

2. DECOMPOSE total return
   |-- Spot Return = (Spot_t1 - Spot_t0) / Spot_t0. Price change of the commodity
   |-- Roll Return = (F_near - F_far) / F_near per roll period. Positive in backwardation, negative in contango
   |-- Collateral Return = risk-free rate on the cash used to collateralize futures
   |-- Total Return ≈ Spot Return + Roll Return + Collateral Return

3. COMPUTE roll yield
   |-- Roll Yield = (F1 - F2) / F1 × (1 / months_between). Annualized.
   |-- Positive roll yield = free carry for longs. Negative = cost for longs
   |-- Example: WTI M1 = $78, M6 = $76. 5-month roll = ($78-$76)/$78 = 2.56% = 6.15% annualized ✓

4. INVENTORY-CURVE RELATIONSHIP
   |-- Inventories low + spot tight → backwardation (positive roll yield, bullish carry)
   |-- Inventories high + spot weak → contango (negative roll yield, bearish carry)
   |-- Super-contango: >10% annualized = storage glut. Buy storage, sell forward
   |-- Super-backwardation: >20% annualized = extreme tightness. Spot premium collapse risk

   Complete when: Curve structure characterized. Roll return computed.
   Inventory level consistent with curve shape (contango should = ample inventory, backwardation = tight).
```

### Phase 4: Processing Spreads

```
1. IDENTIFY the processing spread
   |-- Crack spread: Refinery margin. 3-2-1 crack = 3 crude → 2 gasoline + 1 distillate
   |-- Crush spread: Soybean processing. 1 soybeans → soybean meal + soybean oil
   |-- Spark spread: Gas-fired power generation. Electricity price - (Gas price × Heat Rate + Carbon)
   |-- Hog crush: Pork processing. Pork cutout - hog price

2. COMPUTE the spread
   |-- 3-2-1 Crack = (2 × RBOB + 1 × ULSD - 3 × Crude) / 3 per barrel
   |-- Board crush = (Soybean_Meal × 48lbs/bu + Soybean_Oil × 11lbs/bu - Soybeans) per bushel

3. INTERPRET the spread
   |-- Crack spread ≈ refining margin. $15-25/bbl = normal. <$10 = refinery losing money. >$30 = windfall
   |-- Seasonal: gasoline crack strongest Mar-May (pre-summer), heating oil Oct-Dec (pre-winter)
   |-- Turnarounds: spring/fall refinery maintenance reduces crude demand, tightens products

   Complete when: Spread computed [COMPUTED]. Seasonal position identified.
   Capacity utilization checked [VERIFIED from EIA]. Spread vs 5yr range.
```

### Phase 5: Macro Commodity

```
1. ASSESS commodity cycle position
   |-- Super-cycle (10-30yr): structural demand shift (China 2000s, energy transition 2020s)
   |-- Business cycle (3-7yr): GDP-driven demand across industrial commodities
   |-- Inventory cycle (6-18mo): restocking/destocking. PMI new orders leading indicator
   |-- Seasonality (1-12mo): weather, crop cycles, driving season, heating season

2. CHECK inter-commodity relationships
   |-- Gold/Oil ratio: oz of gold per barrel. 20+ = gold expensive vs oil. <10 = oil expensive vs gold
   |-- Copper/Gold ratio: Dr. Copper vs safe haven. Rising = risk-on. Falling = risk-off
   |-- Bloomberg Commodity Index (BCOM) trend: broad commodity beta
   |-- GSCI roll yield: aggregate roll return across commodity complex

3. CROSS-ASSET signals
   |-- Commodities vs equities: relative performance. Commodities outperform in late cycle, underperform early
   |-- Commodities vs bonds: commodity prices vs breakeven inflation. Rising commodities = rising inflation expectations to some extent
   |-- EM FX vs commodities: AUD, CAD, BRL, ZAR correlated with commodity indices

   Complete when: Cycle position assessed. Key inter-commodity ratios computed.
   Cross-asset regime identified (risk-on/risk-off for commodities).
```

## Decision Trees

### Inventory-Curve Diagnosis

```
                     ┌──────────────────────┐
                     │ Commodity curve shape     │
                     └──────────┬───────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
        Backwardation       Contango          Super-Contango
        (F1 > F2)          (F1 < F2)          (F1 << F2, >10% ann)
              │                 │                 │
              ▼                 ▼                 ▼
     ┌────────────────┐ ┌──────────────┐ ┌──────────────┐
     │ Inventories?     │ │ Inventories?   │ │ Storage glut   │
     └──┬─────────┬─────┘ └──┬───────┬─────┘ │ confirmed      │
        │LOW      │HIGH      │HIGH   │LOW     └──┬────────────┘
        ▼         ▼          ▼       ▼          ▼
   ┌─────────┐ ┌─────────┐ ┌─────┐ ┌─────────┐ ┌──────────┐
   │ GENUINE │ │ SUPPLY  │ │NORMAL│ │ SUPPLY  │ │ SELL     │
   │ TIGHT-  │ │ SCARE?  │ │CARRY │ │ BUILD   │ │ futures  │
   │ NESS    │ │   │     │ │COST  │ │ despite │ │ Buy      │
   │ ✓ long  │ │  YES/NO │ │      │ │ curve   │ │ storage  │
   │ futures │ └──┬──┬───┘ │      │ │ signal? │ │ basket   │
   └─────────┘    │  │     └─────┘ └──┬──┬───┘ └──────────┘
               YES   NO              YES  NO
                │     │               │    │
                ▼     ▼               ▼    ▼
           ┌──────┐┌──────────┐ ┌──────┐┌──────────┐
           │SQUEEZE││SELL futures││POTENTIAL││OVERSOLD │
           │DO NOT ││Spot panic ││OVER-   ││Spot floor│
           │SHORT  ││unwinds    ││SUPPLY  ││BUY spot  │
           └──────┘└──────────┘│short fts││sell fwds  │
                               └────────┘└──────────┘
```

### Commodity Type Router

```
                     ┌──────────────────────┐
                     │ "Analyze [commodity]"    │
                     └──────────┬───────────┘
                                │
           ┌────────────────────┼────────────────────┐
           ▼                    ▼                    ▼
    Has storage cost?     Has industrial       Has growing
    vs no storage?        use case?            season?
           │                    │                    │
    ┌──────┴──────┐      ┌──────┴──────┐      ┌──────┴──────┐
    │YES: Energy   │      │YES: Base     │      │YES: Ag      │
    │Metals, some  │      │metals,       │      │Grains,      │
    │ags           │      │energy        │      │softs,       │
    └──────┬───────┘      └──────┬───────┘      │livestock    │
           │                     │              └──────┬───────┘
           ▼                     ▼                     ▼
    ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
    │ FOCUS:          │    │ FOCUS:          │    │ FOCUS:          │
    │ Inventory +     │    │ PMI + China     │    │ WASDE +         │
    │ Curve + EIA     │    │ + exchange      │    │ Weather +       │
    │                 │    │ inventories     │    │ Stocks-to-use   │
    └────────────────┘    └────────────────┘    └───────────────┘
```

## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| Buying oil because "OPEC+ cut production" — but the cut was 1M bbl/day and the market had already priced 1.5M bbl/day. The "cut" was actually a disappointment relative to expectations. Oil drops $3 on the announcement and the trader doesn't understand why | $50K-$500K in "OPEC+ trade" losses. The absolute production cut is irrelevant — only the surprise vs market expectations matters. The forward curve already embeds the expected cut | Check BEFORE the announcement: what does the futures curve imply? Backwardation = tight supply expected. If the curve is already in backwardation, a production cut is partially priced. Compare announced cut to analyst consensus, not to zero |
| Trading natural gas during "shoulder season" (spring/fall) the same way as winter. NG demand: winter heating = 100+ Bcf/day, shoulder = 60 Bcf/day. Storage injections in shoulder = 50-100 Bcf/week. The price dynamics are completely different — shoulder is about storage trajectory, winter is about weather forecasts | $100K-$1M in shoulder-season losses. NG volatility drops 50% in shoulder but mean-reversion increases. Breakout strategies fail. Weather premium is absent but storage surplus/deficit dominates | Switch strategy by season: Winter (Nov-Mar): trade weather forecasts, HDD deviations, storage withdrawals. Summer (Jun-Aug): trade cooling demand, power burn, CDD. Shoulder (Apr-May, Sep-Oct): trade storage injection trajectory. Don't use one playbook year-round |
| Buying gold "as an inflation hedge" when real yields are rising. Gold's primary driver is real yields (TIPS), not CPI. If nominal yields rise faster than inflation (real yields increase), gold goes DOWN despite inflation being high. 2022: CPI 6-9%, gold flat to down — real yields rose from -1.0% to +2.0% | $50K-$500K in gold positions during "inflation that everyone already knows about." Gold priced 2% CPI when real yields were -1%. When real yields went to +1.5%, gold fell DESPITE CPI being 4%. Inflation hedging with gold only works when inflation SURPRISES | Track 10yr TIPS yield as the PRIMARY gold driver. If real yields are rising, do not buy gold regardless of the inflation narrative. The gold/inflation relationship is mediated entirely through real yields and the USD |
| Looking at LME copper inventories without checking cancelled warrants. LME inventory = 150K tonnes. Cancelled warrants = 80K tonnes (53% of total). Metal is booked for withdrawal — inventories are about to drop 80K. The "ample" inventory picture is misleading — actual available metal is only 70K tonnes | $200K-$1M in copper trades based on stale inventory interpretation. Cancelled warrants are a leading indicator — inventory drops follow 1-2 weeks later. Trading on total inventory without netting cancelled warrants = trading on data that's already stale | Always compute: Available Inventory = On-Warrant Inventory (Total - Cancelled). Track the ratio of cancelled/on-warrant. >30% = imminent drawdown. The commodity market already sees this — if you don't, you're trading at an information disadvantage |
| Selling corn in June because "weather has been perfect so far" — ignoring that July pollination is the critical yield-determining period. A 10-day heatwave in July can cut yields 20-30 bushels/acre. The crop is MADE OR BROKEN in July/August, not in the planting/germination phase | $100K-$1M in pre-sold crop that rallies 30% after a July drought. Early-season crop conditions tell you about STAND establishment, not yield potential. The market knows this and prices weather risk premium through July even if current conditions are perfect | Track the crop calendar: pollination (corn) = July, pod-setting (soybeans) = August, grain-fill (wheat) = May-June. The weather during the reproductive phase determines yield. Do not extrapolate vegetative-phase conditions to final yield. The market won't remove weather premium until the crop is made |

## Proactive Triggers

| # | Trigger | Auto-Response |
|---|---------|---------------|
| P1 | `crude_inventory_change > 5_million_barrels AND analyst_consensus < 2_million` | [ALERT] EIA crude build >3M bbls above consensus. Demand weakness or supply surge. Short-term bearish crude |
| P2 | `Cushing_inventory < 20_million_barrels AND declining` | [URGENT] Cushing approaching tank bottoms (~20M minimum operable). WTI backwardation may spike. Front-month squeeze risk |
| P3 | `LME_cancelled_warrants / on_warrant > 0.50` | [ALERT] 50%+ of LME inventory booked for withdrawal. Imminent physical tightness. Backwardation deepening |
| P4 | `NG_storage_surplus / deficit > 300_Bcf vs 5yr_avg AND heating_season_starting` | [INFO] Natural gas entering winter with significant storage surplus. Price upside limited unless extreme cold |
| P5 | `WASDE_stocks_to_use < 0.08 AND growing_weather_forecast == DRY` | [URGENT] Stocks-to-use below 8% WITH adverse weather. Potential price spike. Front-month backwardation |
| P6 | `gold_silver_ratio > 85` | [INFO] Gold/Silver ratio at extreme (>85). Silver significantly undervalued vs gold historically. Silver mean-reversion trade |
| P7 | `BCOM_index < 20_day_MA AND USD_DXY > 50_day_MA AND commodity_positions_open` | [WARN] Broad commodity weakness + strong USD. Check that thesis on each position is intact. Tighten stops |

## Cross-Skill Coordination

### Upstream

| Upstream Skill | What You Receive | Trigger | Your Response |
|---|---|---|---|
| `macro-strategist` | Global GDP forecasts, China macro pulse, USD direction, inflation regime, risk-on/off | **PUSH:** China credit impulse turning. **PUSH:** USD regime change | China impulse up → overweight base metals. USD weakening → long commodities broadly (USD negative for commodities) |
| `futures-trader` | Execution costs, roll costs, margin requirements, contract specifications, CTD analysis | **PUSH:** Roll approaching. **PUSH:** Margin change | Adjust position for roll: determine roll strategy (calendar spread vs legging). Margin increase → reduce size or add collateral |
| `market-data-engineer` | EIA data, WASDE, LME/COMEX inventories, weather data, shipping rates | **PULL:** requestEIAInventory. **PULL:** requestWASDE. **PULL:** requestWeatherModel | Data update → reassess supply-demand balance. Check if data changes the thesis |

### Downstream

| Downstream Skill | What You Send | Trigger | Expected Response |
|---|---|---|---|
| `portfolio-signal-manager` | Commodity exposure: sector (energy/metals/ag), direction, conviction, risk factors (curve, weather, geopolitics) | **PUSH:** New commodity position. **PUSH:** Curve opportunity (roll yield) | Integrates with equity, FI, FX. Checks for unintended commodity beta in equity positions |
| `algorithmic-trader` | Execution: commodity, contract, direction, lots, order type, roll instructions | **PUSH:** Trade signal. **PUSH:** Roll instruction | Fill report with slippage. Roll executed at calendar spread |

## Error Recovery

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| Natural gas position loses despite correct weather forecast — called for cold, cold happened, NG dropped | The cold was ALREADY PRICED INTO the futures curve. Weather models had shown the cold for 10 days. By the time you traded, the weather premium was in the price. The cold verified → no new information → premium came OUT → price dropped | Check weather model CONSENSUS, not just the forecast. If GFS and ECMWF both showed cold 10 days ago, the NG market already priced it. You need a colder-than-forecast SURPRISE to profit from a long | Weather is the most forecasted variable in commodities. The 10-day forecast is already in the price. Your edge is in seeing what the models DON'T show — faster warming, deeper cold, longer duration — not in trading the public forecast |
| Corn position loses despite drought — drought happened, corn rallied initially, then dropped back | The drought was in the US but Brazil had a RECORD crop, flooding the export market. Global balance sheet matters, not local. US drought + Brazil bumper crop = net neutral global supply. The initial rally was on US headlines; the reversal was on global balance | Always check the GLOBAL supply-demand balance, not just local. Corn, soybeans, wheat are globally traded. US drought + Brazil record crop = Brazilian exports fill the gap. The global S/D balance is what matters, not the US S/D in isolation | Commodity markets are global. A local supply shock that doesn't affect the global balance is a short-term headline, not a structural supply deficit. Always compute: Global Production - Global Demand = Global Stock Change before concluding "supply shock" |
| Crack spread trade impossible to execute — calculated the crack, wanted to buy it, but broker requires 3 separate futures legs with different margins | The crack spread is a PHYSICAL relationship. In futures, it requires 3 separate positions: long 2 RBOB + long 1 ULSD + short 3 crude. Margin: ~$30K for the package vs $10K for a single contract. The margin rules reflect the VOLATILITY of the spread, not just the notional | Check broker margin for multi-leg spreads BEFORE constructing the trade. CME clears crack spreads as pre-defined combos with reduced margin (spread margin = lower than outrights). Use the exchange-recognized spread, not 3 separate orders | Exchange-cleared spreads have lower margin requirements than separate legs. Always check if your spread is a recognized exchange combo. If you leg in separately, you pay full margin AND take execution risk between legs |
| Gold-silver ratio trade doesn't work — bought silver because ratio >85, ratio went to 90 and stayed there for 6 months | The gold-silver ratio has no time limit for mean reversion. It can stay "extreme" for years. The ratio was >80 from 2018-2020 (2+ years). The trade has negative carry (no yield on silver) and the ratio can keep trending | Size for 2+ year mean reversion, not 2 months. The gold-silver ratio is NOT a short-term mean-reversion trade. It's a secular valuation metric. Consider: no carry (precious metals have zero yield), ratio can trend for years, and position must survive until the catalyst arrives | Mean-reverting trades in commodities with no carrying cost have no "clock." Unlike yield curve trades where negative carry forces resolution, the gold-silver ratio can stay extreme indefinitely. You need a CATALYST, not just a valuation extreme |

## What Good Looks Like

```
Commodity: WTI Crude Oil (CL futures, CME)
Price: $78.50/bbl [VERIFIED from CME, timestamp]. M1-M6 spread: -$2.10 (contango, 5.4% annualized) [COMPUTED]

Supply-Demand [VERIFIED from EIA 04/10/2024]:
  Global Production: 102.0 mb/d. OPEC+ compliance: 85% (leakage 0.5 mb/d above quota)
  Global Demand: 102.5 mb/d (IEA estimate). Implied deficit: -0.5 mb/d
  US Production: 13.2 mb/d (record). US Exports: 4.5 mb/d

Inventories [VERIFIED from EIA weekly]:
  US Crude: 445M bbls (-2M vs last week, -15M vs 5yr avg). Cushing: 32M bbls (below 35M comfort)
  Days of forward cover: 25 days (vs 28-day 5yr avg). TIGHTENING.
  SPR: 365M bbls (drawn 220M since 2021, no refill announced)

Curve & Carry:
  Curve: Contango (F1 < F6 < F12). Annualized roll cost: -5.4% for longs
  Interpretation: Market is WELL-SUPPLIED in the forward market despite spot tightness.
  The contango says: "current tightness is temporary, forward supply is adequate."

Trade Implications:
  Spot tightness (Cushing low, global deficit) argues for near-term strength.
  But contango means long futures positions lose 5.4%/year rolling.
  → Best expression: bull calendar spread (long front month, short deferred)
    captures spot tightness without paying roll cost.
```

Every data point tagged. Supply-demand balanced. Inventories in context. Curve structure consistent with inventory signal. Trade expression accounts for curve costs.

## Verification Guardrails

- [ ] **All commodity prices from live source** — EIA, CME, ICE, LME, broker terminal. [VERIFIED] timestamp
- [ ] **Inventory data current** — EIA weekly, LME daily, WASDE monthly. Not stale
- [ ] **Curve structure characterized** — contango or backwardation, roll yield computed
- [ ] **Supply-demand balanced** — production, demand, implied stock change. Days of supply
- [ ] **Seasonality accounted for** — where are we in the seasonal cycle? Weather premium?
- [ ] **Global balance, not local** — US + Brazil + Argentina + EU + Black Sea for grains. Global for oil
- [ ] **Processing spread margins verified** — crack/crush/spark computed with current futures prices
- [ ] **No fabricated inventory numbers or production figures** — if unverified, state as [ESTIMATED]

## Deliberate Practice

### Exercise 1: Inventory Calculus (5 min)
EIA reports: US crude +5M bbls (consensus was -2M). Cushing -1.5M. Gasoline -3M. Distillate -1M. Interpret: is this bearish or bullish? What's the Cushing signal vs the headline?

### Exercise 2: Roll Yield vs Spot (5 min)
WTI spot $78, M6 $76, M12 $73. Compute annualized roll yield for a long futures position rolled every 6 months. Which would you rather hold: spot (via ETF like USO, paying 0.80% expense ratio) or futures (paying roll cost but no expense ratio)?

### Exercise 3: Crack Spread (5 min)
Crude $75/bbl. RBOB $2.50/gal ($105/bbl). ULSD $2.80/gal ($117.60/bbl). Compute 3-2-1 crack spread. Is this above or below the 5-year average of $18/bbl? What seasonal phase are we in?

### Exercise 4: Stocks-to-Use (5 min)
US corn: beginning stocks 2.2B bu, production 15.0B bu, domestic use 12.5B bu, exports 2.5B bu. Compute ending stocks, stocks-to-use ratio. Is this tight (<10%), normal (10-15%), or ample (>15%)?

### Exercise 5: Gold Driver (5 min)
10yr TIPS yield goes from 1.50% to 2.00%. DXY goes from 104 to 106. Gold was at $2,050. Estimate the new gold price using: ΔGold ≈ -100 × ΔReal_Yield - 15 × ΔDXY.

## References
- [energy-complex.md](references/energy-complex.md) — Crude oil benchmarks, natural gas markets, refined products, EIA data guide
- [metals-markets.md](references/metals-markets.md) — Precious metals drivers, base metals supply chains, LME/COMEX/SHFE exchange data
- [agricultural-markets.md](references/agricultural-markets.md) — Grain/oilseed balance sheets, WASDE report guide, growing season calendar, weather models
- [curve-structure-analysis.md](references/curve-structure-analysis.md) — Contango/backwardation, roll yield, total return decomposition, inventory-curve relationship
- [processing-spreads.md](references/processing-spreads.md) — Crack spread, crush spread, spark spread, margin analysis, seasonal patterns
- [commodity-cycles.md](references/commodity-cycles.md) — Super-cycles, inventory cycles, leading indicators, inter-commodity ratios
- [geopolitical-risk.md](references/geopolitical-risk.md) — Strait of Hormuz, Russia/Ukraine grain corridor, OPEC+ politics, sanctions frameworks
- [seasonality-calendar.md](references/seasonality-calendar.md) — Crop calendars, heating/cooling seasons, refinery turnaround schedules, hurricane season
- [error-recovery.md](references/error-recovery.md) — Error recovery: weather premium, global vs local balance, secular mean-reversion, curve misunderstanding

