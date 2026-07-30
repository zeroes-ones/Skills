# Trade Journal Schema

## Required Fields
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| trade_id | String/Int | Unique trade identifier | "2026-0115-001" |
| entry_date | Date/DateTime | Entry timestamp | "2026-01-15T09:35:00Z" |
| exit_date | Date/DateTime | Exit timestamp (blank if open) | "2026-01-22T15:58:00Z" |
| symbol | String | Tradeable instrument identifier | "AAPL", "ES", "BTC-USD" |
| asset_class | Enum | Equity/Futures/FX/Crypto/Fixed_Income | "Equity" |
| direction | Enum | LONG/SHORT | "LONG" |
| entry_price | Float | Average fill price | 195.50 |
| exit_price | Float | Average exit price (blank if open) | 201.25 |
| quantity | Float | Number of shares/contracts/units | 100 |
| fees | Float | Total commission + exchange fees | 1.50 |
| slippage | Float | Execution price - signal price (in price units) | 0.05 |

## Recommended Fields
| Field | Type | Description |
|-------|------|-------------|
| strategy_label | String | Which strategy generated this signal |
| conviction_score | Integer (1-5) | Subjective conviction at entry |
| market_regime | Enum | Macro regime at entry (from macro-strategist) |
| entry_signal | String | Technical or fundamental trigger |
| exit_signal | String | What triggered exit (target/stop/discretionary) |
| exit_reason | Free text | Narrative reason if discretionary |
| behavioral_flags | Array[Enum] | Self-reported or auto-detected biases |
| tags | Array[String] | Custom categorization tags |
| notes | Free text | Trade journal commentary |

## Behavioral Tag Taxonomy
| Flag | Definition |
|------|-----------|
| FOMO | Entered because of fear of missing out (chasing) |
| REVENGE | Entered quickly after a loss with increased size |
| ANCHORING | Held because fixated on entry price or recent high |
| OVERTRADING | Excessive frequency without signal quality |
| HESITATION | Failed to enter despite valid signal |
| EARLY_EXIT | Exited before profit target for emotional reasons |
| MOVED_STOP | Widened stop loss beyond plan |
| SIZED_UP | Position size larger than system rules |
| SIZED_DOWN | Position size smaller than system rules |

## File Format Recommendations
- **CSV**: Universal, git-friendly, easy to script against
- **Parquet**: Better for large datasets, preserves types
- **Database**: SQL schema for querying across dimensions

## Provenance
[VERIFIED] Schema design from trading journal best practices
[AS OF 2026-01]

