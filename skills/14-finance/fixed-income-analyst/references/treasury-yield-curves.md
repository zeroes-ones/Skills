# Treasury Yield Curves

## Curve Benchmark Tenors

| Tenor | Name | CUSIP Prefix | Futures | Typical Use |
|-------|------|-------------|---------|------------|
| 1mo-1yr | Bills | 912796 | N/A | Cash management, Fed policy pricing |
| 2yr | Notes | 91282C | ZT (2yr) | Short end rate expectations |
| 3yr | Notes | 91282C | Z3N (3yr) | Intermediate, less liquid |
| 5yr | Notes | 91282C | ZF (5yr) | Curve belly, mortgage benchmark |
| 7yr | Notes | 91282C | — | Less liquid, interpolated |
| 10yr | Notes | 91282C | ZN (10yr) | Benchmark, most liquid point |
| 20yr | Bonds | 912810 | TWE (20yr) | Pension/insurance duration target |
| 30yr | Bonds | 912810 | ZB (30yr) | Long duration, liability matching |

## On-the-Run vs Off-the-Run

On-the-run = most recently issued at each tenor. Trades at a premium (lower yield) due to liquidity.
Off-the-run = previously issued. Trades at discount (higher yield) due to lower liquidity.

Typical on-the-run premium: 2-10bp (varies with market stress).
During crisis: premium can invert — off-the-runs become more expensive as investors seek specific issues.

## Key Curve Metrics

| Metric | Computation | Current Signal |
|--------|------------|----------------|
| 2s10s Spread | 10yr yield - 2yr yield | Steep > 0, Flat/Inverted < 0 |
| 5s30s Spread | 30yr yield - 5yr yield | Belly steepness |
| 2s5s10s Butterfly | 2×5yr - (2yr + 10yr) | Curvature. Positive = belly rich, negative = belly cheap |
| 3m10y Spread | 10yr yield - 3mo T-bill | Near-term vs long-term expectations. Deepest inversion precedes recession |
| Fed Funds Implied | Fed Funds Futures or OIS | Market pricing of next 1-3 FOMC meetings |

## Curve Shapes and Macro Signals

| Shape | 2s10s | Signal | Historical Context |
|-------|-------|--------|-------------------|
| Steep | >150bp | Growth + rate hike expectations. Long duration risky | Post-GFC QE era |
| Normal | +50 to +150bp | "Normal" — modest growth, moderate inflation | Pre-2008 typical |
| Flat | 0 to +50bp | Late cycle. Market uncertain about growth | Pre-recession signal |
| Inverted | <0bp | Recession forecast. Market prices rate CUTS | 6 of last 7 recessions preceded by inversion |
| Deeply Inverted | <-50bp | Extreme recession fear. Aggressive rate cuts priced | 2023: -108bp deepest since 1981 |

## Curve Data Sources

- **US Treasury:** treasury.gov/resource-center/data-chart-center/interest-rates — Daily Treasury Par Yield Curve
- **Real-time:** Broker/terminal (Bloomberg, Reuters). Treasury.gov is 4 PM ET prior day
- **Fed:** newyorkfed.org — ACM term premium, Treasury term premia estimates
- **Futures-implied:** CME FedWatch for Fed funds path

All yields must be [VERIFIED] from live source or [AS OF date] for historical analysis.

