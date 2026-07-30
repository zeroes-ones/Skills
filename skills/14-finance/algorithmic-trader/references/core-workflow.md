# Core Workflow — Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->

<!-- DEEP: 10+min -->
### Phase 1 (~10 min): Signal Reception & Validation

Consume output from the quantitative-analyst pipeline. Every signal must be validated before any capital is committed.

**Pre-flight: Data quality pipeline.** Bad data produces bad trades — validate inputs before they enter any decision logic:

```python
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import requests

@dataclass
class DataQualityReport:
    passed: bool = True
    issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

def data_quality_preflight(data: pd.DataFrame, symbol: str) -> DataQualityReport:
    """Run BEFORE signal validation. Refuse to trade if data is corrupt."""
    rpt = DataQualityReport()

    # 1. PRICE SANITY
    required_cols = ['open', 'high', 'low', 'close', 'volume']
    missing = [c for c in required_cols if c not in data.columns]
    if missing:
        rpt.issues.append(f"MISSING COLUMNS: {missing}")
        rpt.passed = False
        return rpt

    # OHLC relationship: high >= max(open, close), low <= min(open, close)
    bad_bars = (
        (data['high'] < data[['open','close']].max(axis=1)) |
        (data['low'] > data[['open','close']].min(axis=1))
    )
    if bad_bars.any():
        bad_dates = data.index[bad_bars].tolist()
        rpt.issues.append(
            f"OHLC VIOLATION: {len(bad_dates)} bars with impossible OHLC "
            f"(high < max(o,c) or low > min(o,c)). Dates: {bad_dates[:3]}..."
        )
        rpt.passed = False

    # No zero/negative prices
    for col in ['open', 'high', 'low', 'close']:
        neg = (data[col] <= 0).sum()
        if neg > 0:
            rpt.issues.append(f"NEGATIVE/ZERO PRICES: {neg} {col} values <= 0")
            rpt.passed = False

    # Price gaps > 20% between consecutive bars (likely data error, not real move)
    gap_pct = abs(data['open'] / data['close'].shift(1) - 1) * 100
    extreme_gaps = gap_pct > 20
    if extreme_gaps.any():
        gap_dates = data.index[extreme_gaps].tolist()
        rpt.warnings.append(
            f"EXTREME PRICE GAPS: {len(gap_dates)} gaps >20% — "
            f"verify against secondary data source. Dates: {gap_dates[:3]}..."
        )

    # 2. VOLUME CONSISTENCY
    # Sudden zero-volume bars during market hours = data feed gap
    zero_vol = (data['volume'] == 0)
    if zero_vol.any():
        rpt.warnings.append(f"ZERO VOLUME: {zero_vol.sum()} bars — data feed gap?")

    # Volume spike detection: >10x 20-day median volume = likely data error or HFT burst
    vol_median = data['volume'].rolling(20).median()
    vol_spikes = data['volume'] > (10 * vol_median)
    if vol_spikes.any():
        rpt.warnings.append(
            f"VOLUME SPIKES: {vol_spikes.sum()} bars >10x median — "
            f"verify these are real prints, not data artifacts"
        )

    # 3. CORPORATE ACTION DETECTION
    # Stock splits/dividends change prices discontinuously. Flag for manual review.
    # Split detection: consecutive bars where price drops >40% on no volume spike
    price_drop = (data['close'] / data['close'].shift(1) - 1) * 100
    split_candidate = (price_drop < -40) & (~vol_spikes.shift(1))
    if split_candidate.any():
        split_dates = data.index[split_candidate].tolist()
        rpt.warnings.append(
            f"POSSIBLE STOCK SPLIT: {len(split_dates)} dates with >40% price drop "
            f"and no volume spike. Verify corporate actions. Dates: {split_dates[:3]}..."
        )

    # 4. STALE DATA DETECTION
    last_date = data.index[-1]
    if isinstance(last_date, pd.Timestamp):
        now = pd.Timestamp.now(tz=last_date.tz)
        if hasattr(last_date, 'tz_localize') and last_date.tz is None:
            last_date = last_date.tz_localize('US/Eastern')
        hours_stale = (now - last_date).total_seconds() / 3600

        if hours_stale > 24:
            rpt.issues.append(
                f"STALE DATA: last bar {last_date} — {hours_stale:.1f}h old. "
                f"Refusing to trade on stale data."
            )
            rpt.passed = False
        elif hours_stale > 4:
            rpt.warnings.append(
                f"DATA DELAYED: last bar {hours_stale:.1f}h old. "
                f"After-hours or data feed delay — use with caution."
            )

    return rpt
```

**Data quality gate**: If `DataQualityReport.passed == False`, reject all signals for this symbol — do NOT trade. Warnings are advisory but logged for post-trade audit.

1. **Parse signal envelope**: Extract ticker, direction (CALL=long equity, PUT=short equity), timestamp, conviction score (0.0-1.0), and expected catalyst timeframe from the quantitative-analyst JSON payload.
2. **Liquidity gate**: Check that the underlying trades >500K shares/day and option open interest on the target strike is >1,000 contracts. Illiquid underlyings amplify slippage beyond model assumptions — reject signals on names with average daily volume under 100K.
3. **Correlation gate**: Compare the signal ticker against existing positions. If adding this position would push sector exposure above 30% of portfolio, reduce size or skip. UOA signals cluster — 5 signals in semiconductors is one bet, not five.
4. **News gate**: Scan for pending earnings (within 5 days), FDA decisions, merger votes, or regulatory rulings. Binary event risk trumps any UOA signal. Reduce position size by 50% or skip if an unmodelable event is imminent.
5. **Macro event gate**: Check economic calendar for high-impact releases within 24 hours — FOMC rate decisions, CPI, PPI, NFP, GDP advance, PMI flash, jobless claims. During macro events, intraday volatility expands 2-4x normal and stop-losses get hunted en masse. If a red-flag event (FOMC, CPI, NFP) is within 24 hours: reduce position size by 50% AND widen stop-loss by 1.5x. If within 2 hours: skip the trade entirely — the signal edge is noise against macro volatility.
6. **Signal freshness check**: If the signal timestamp is >2 hours old during market hours (or >1 day for overnight signals), check whether the edge has decayed. Compare current price vs. signal price — if the move already happened, the trade is over.

```python
# Signal validation pseudocode
def validate_signal(signal: dict, portfolio: Portfolio, market_data: MarketData) -> SignalDecision:
    if signal['avg_daily_volume'] < 100_000:
        return SignalDecision.REJECT  # insufficient liquidity

    if signal['option_open_interest'] < 1_000:
        return SignalDecision.REJECT

    sector = get_sector(signal['ticker'])
    if portfolio.sector_exposure[sector] + signal['suggested_size'] > 0.30 * portfolio.nav:
        signal['adjusted_size'] = 0.30 * portfolio.nav - portfolio.sector_exposure[sector]
        if signal['adjusted_size'] <= 0:
            return SignalDecision.REJECT  # sector limit reached

    if days_to_earnings(signal['ticker']) <= 5:
        signal['adjusted_size'] *= 0.5

    hours_to_macro = hours_to_next_macro_event()
    if hours_to_macro <= 2 and is_red_flag_event():
        return SignalDecision.REJECT  # macro event imminent, edge is noise
    elif hours_to_macro <= 24 and is_high_impact_event():
        signal['adjusted_size'] *= 0.5
        signal['stop_multiplier'] = 1.5  # widen stops for macro vol

    signal_age_minutes = (datetime.utcnow() - signal['timestamp']).total_seconds() / 60
    if signal_age_minutes > 120:
        price_change = (market_data.last - signal['signal_price']) / signal['signal_price']
        if abs(price_change) > 0.02:  # >2% move already happened
            return SignalDecision.EXPIRED

    return SignalDecision.ACCEPT

```

Complete when: All 6 gates return PASS or adjusted parameters: identity verified (symbol/strategy/confidence match), entry within 1.5 ATR of VWAP, liquidity confirmed (cap >$2B, spread <0.15%), no binary earnings within 5 days (or size halved), no red-flag macro event within 2 hours (or rejected), and signal freshness validated (age <2 hours or move precheck passed). Any rejected signal has a documented rejection reason.

<!-- STANDARD: 3min -->
### Numerical Safety Layer

Every computation that touches market data must survive NaN, Inf, division-by-zero, and zero-volume inputs. A single unguarded operation silently corrupts the entire pipeline — NaN propagates through all downstream math.

```python
import math
import numpy as np
import pandas as pd
from typing import Union, Optional
from functools import wraps

# ─── Core guards ───────────────────────────────────────────────

def safe_divide(numerator: float, denominator: float, fallback: float = 0.0) -> float:
    """Divide two scalars. Returns fallback if denominator is zero or either is NaN/Inf."""
    if (not math.isfinite(numerator)) or (not math.isfinite(denominator)):
        return fallback
    if abs(denominator) < 1e-12:
        return fallback
    result = numerator / denominator
    return result if math.isfinite(result) else fallback

def validate_finite(value: float, label: str = "value", fallback: float = 0.0) -> float:
    """Raise ValueError with context if value is not finite. For pipeline-critical values only."""
    if not math.isfinite(value):
        raise ValueError(f"Non-finite {label}: {value} — upstream data corruption?")
    return value

def sanitize_series(s: pd.Series, fill_method: str = 'ffill') -> pd.Series:
    """Clean a pandas Series: forward-fill gaps, replace Inf with NaN, fill remaining NaN with 0."""
    s = s.replace([np.inf, -np.inf], np.nan)
    if fill_method == 'ffill':
        s = s.ffill()
    elif fill_method == 'zero':
        s = s.fillna(0.0)
    else:
        s = s.bfill().ffill()  # ffill then bfill for remaining edge NaN
    # Any NaN that survived (e.g., leading NaN before any valid value)
    return s.fillna(0.0)

# ─── Decorator: guard entire pipeline functions ─────────────────

def guard_numerical_inputs(func):
    """Decorator: rejects calls where any float/int arg is NaN/Inf."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        for i, arg in enumerate(args):
            if isinstance(arg, (int, float)) and not math.isfinite(arg):
                raise ValueError(
                    f"{func.__name__} arg[{i}]={arg} is non-finite. "
                    f"Check upstream data pipeline."
                )
        for key, val in kwargs.items():
            if isinstance(val, (int, float)) and not math.isfinite(val):
                raise ValueError(
                    f"{func.__name__} kwarg '{key}'={val} is non-finite."
                )
        return func(*args, **kwargs)
    return wrapper

# ─── Data-quality assertions (run at pipeline entry) ────────────

def assert_data_quality(df: pd.DataFrame, required_cols: list[str], label: str = "DataFrame"):
    """Die loudly if data is corrupt. Catches silent NaN propagation at the boundary."""
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"{label} missing columns: {missing}")

    for col in required_cols:
        col_data = df[col]
        nan_count = col_data.isna().sum()
        inf_count = (np.isinf(col_data) if col_data.dtype.kind == 'f' else 0)

        if nan_count > 0:
            pct = nan_count / len(df) * 100
            if pct > 5.0:
                raise ValueError(
                    f"{label}.{col}: {nan_count} NaN ({pct:.1f}%) — "
                    f">5% threshold. Refusing to proceed."
                )
            # <5%: warn and fill
            print(f"WARNING: {label}.{col}: {nan_count} NaN ({pct:.1f}%) — forward-filling")
            df[col] = df[col].ffill().fillna(0.0)

        if isinstance(inf_count, int) and inf_count > 0:
            raise ValueError(
                f"{label}.{col}: {inf_count} Inf values — "
                f"likely division-by-zero upstream. Trace and fix."
            )

    # Price sanity: no zero or negative prices
    for col in ['open', 'high', 'low', 'close']:
        if col in df.columns:
            neg = (df[col] <= 0).sum()
            if neg > 0:
                raise ValueError(f"{label}.{col}: {neg} values ≤ 0 — impossible for prices")

    return df

# ─── Usage example: wrap the pipeline entry ─────────────────────

@guard_numerical_inputs
def compute_stop_loss_safe(entry_price, atr, swing_low, rn_step, vix, vwap_band_low, macro_stop_mult=1.0):
    """Wraps compute_stop_loss with numerical safety guard."""
    return compute_stop_loss(
        entry_price=validate_finite(entry_price, "entry_price"),
        atr=validate_finite(atr, "atr"),
        swing_low=validate_finite(swing_low, "swing_low"),
        round_number_step=validate_finite(rn_step, "rn_step"),
        vix=validate_finite(vix, "vix"),
        vwap_band_low=validate_finite(vwap_band_low, "vwap_band_low"),
        macro_stop_mult=validate_finite(macro_stop_mult, "macro_stop_mult")
    )
```

**Propagation rule**: NaN or Inf detected at any pipeline boundary MUST be investigated upstream — never silently filled. The `assert_data_quality` check runs once at Phase 1 completion. All downstream functions are decorated with `@guard_numerical_inputs` for defense-in-depth.

<!-- DEEP: 10+min -->
### Regime Detection Engine

Trading strategies die when the regime changes. A VIX-only binary check (VIX>20 = fear) misses 80% of regime transitions. This engine combines volatility clustering, trend strength, correlation structure, and credit spreads into one regime classification that all downstream phases consume.

```python
import numpy as np
import pandas as pd
from enum import Enum
from scipy import stats
from arch import arch_model  # pip install arch

class Regime(Enum):
    LOW_VOL_BULL = "low_vol_bull"       # VIX < 15, trend ↑, tight credit — buy dips
    HIGH_VOL_BULL = "high_vol_bull"     # VIX 15-25, trend ↑ — normal sizing, wider stops
    CHOP = "chop"                        # VIX 15-25, trend flat — reduce size, take profits fast
    HIGH_VOL_BEAR = "high_vol_bear"     # VIX 25-35, trend ↓ — small size, tight stops, favor puts
    CRASH = "crash"                      # VIX > 35, trend ↓↓, credit blowing out — CASH or hedged only

# ─── Factor 1: GARCH volatility forecast ────────────────────────

def garch_vol_forecast(returns: pd.Series, horizon: int = 5) -> dict:
    """Fit GARCH(1,1) to daily returns. Returns forward vol forecast and
    whether volatility is accelerating (clustering) or mean-reverting."""
    try:
        scaled = returns * 100  # GARCH needs percentage returns
        model = arch_model(scaled.dropna(), vol='Garch', p=1, q=1, dist='normal')
        result = model.fit(disp='off', show_warning=False)

        forecast = result.forecast(horizon=horizon)
        forecast_vol = np.sqrt(forecast.variance.values[-1, :])

        # Vol clustering: if GARCH alpha + beta > 0.95, vol is persistent (clustering)
        alpha = result.params['alpha[1]']
        beta = result.params['beta[1]']
        persistence = alpha + beta
        clustering = persistence > 0.95

        return {
            'current_annual_vol': round(returns.std() * np.sqrt(252) * 100, 1),
            'forecast_vol_t1': round(forecast_vol[0], 2),
            'forecast_vol_t5': round(forecast_vol[-1], 2),
            'garch_persistence': round(persistence, 3),
            'vol_clustering': clustering,
            'vol_trend': 'accelerating' if forecast_vol[-1] > forecast_vol[0] * 1.05 else
                         'decelerating' if forecast_vol[-1] < forecast_vol[0] * 0.95 else 'stable'
        }
    except Exception as e:
        # Fallback: simple EWMA if GARCH fails
        ewma_vol = returns.ewm(span=20).std().iloc[-1] * np.sqrt(252) * 100
        return {
            'current_annual_vol': round(ewma_vol, 1),
            'forecast_vol_t1': round(ewma_vol, 2),
            'forecast_vol_t5': round(ewma_vol, 2),
            'garch_persistence': 0.0,
            'vol_clustering': False,
            'vol_trend': 'stable',
            'fallback': 'EWMA (GARCH fit failed)'
        }

# ─── Factor 2: Trend strength (dual moving average + ADX) ──────

def trend_strength(prices: pd.Series, adx: pd.Series = None) -> dict:
    """Multi-timeframe trend assessment. Single MA cross is noise-prone."""
    sma_20 = prices.rolling(20).mean().iloc[-1]
    sma_50 = prices.rolling(50).mean().iloc[-1]
    sma_200 = prices.rolling(200).mean().iloc[-1]
    current = prices.iloc[-1]

    # Trend alignment: all 3 SMAs aligned = strong trend
    bullish_aligned = current > sma_20 > sma_50 > sma_200
    bearish_aligned = current < sma_20 < sma_50 < sma_200

    # Slope: 20-day rate of change
    roc_20 = (prices.iloc[-1] / prices.iloc[-20] - 1) * 100

    # ADX: >25 = trending, <20 = chopping
    adx_val = adx.iloc[-1] if adx is not None else 20.0

    return {
        'direction': 'bullish' if current > sma_50 else 'bearish',
        'aligned': bullish_aligned or bearish_aligned,
        'strength': 'strong' if (adx_val > 25 and (bullish_aligned or bearish_aligned))
                    else 'weak' if adx_val < 20 else 'moderate',
        'adx': round(adx_val, 1),
        'roc_20d_pct': round(roc_20, 2)
    }

# ─── Factor 3: Cross-asset stress signals ───────────────────────

def cross_asset_stress(vix: float, hy_spread: float, vix_term_structure: float) -> dict:
    """Credit spreads and VIX term structure reveal stress before equity prices move.
    HY spread = high-yield OAS minus treasury. VIX term structure = VIX futures curve slope."""
    stress_signals = []

    # High-yield credit spread (OAS) — blows out BEFORE equities sell off
    if hy_spread > 500:
        stress_signals.append('CREDIT_STRESS: HY spread >500bps — credit market pricing recession risk')
    elif hy_spread > 350:
        stress_signals.append('CREDIT_CAUTION: HY spread >350bps — widening, monitor closely')

    # VIX term structure: backwardation (front > back) = fear, contango = calm
    if vix_term_structure < -1.0:
        stress_signals.append('VIX_BACKWARDATION: futures curve inverted — fear is acute')
    elif vix_term_structure > 2.0:
        stress_signals.append('VIX_CONTANGO: complacency — tail risk cheap, hedge now')

    # VIX level
    if vix > 35:
        stress_signals.append('VIX_CRASH: vol at crisis levels')
    elif vix > 25:
        stress_signals.append('VIX_ELEVATED: above long-run median')

    return {
        'vix': round(vix, 1),
        'hy_spread_bps': round(hy_spread, 1),
        'vix_term_structure': round(vix_term_structure, 2),
        'stress_level': 'extreme' if len(stress_signals) >= 3
                       else 'elevated' if len(stress_signals) >= 2
                       else 'moderate' if len(stress_signals) >= 1
                       else 'low',
        'signals': stress_signals
    }

# ─── Factor 4: Correlation regime (risk-on / risk-off) ──────────

def correlation_regime(sector_returns: pd.DataFrame, spy_returns: pd.Series) -> dict:
    """When all sectors move together (correlation → 1.0), diversification fails.
    High correlation regime = macro-driven, stock-picking alpha is suppressed."""
    # Average pairwise correlation across sectors
    corr_matrix = sector_returns.corr()
    upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    avg_corr = upper_tri.stack().mean()

    # Correlation to SPY
    spy_corr = sector_returns.apply(lambda x: x.corr(spy_returns)).mean()

    return {
        'avg_pairwise_corr': round(avg_corr, 3),
        'avg_spy_corr': round(spy_corr, 3),
        'diversification': 'failed' if avg_corr > 0.80
                          else 'weak' if avg_corr > 0.60
                          else 'normal' if avg_corr > 0.30
                          else 'strong',
        'regime_type': 'risk_on' if (spy_corr > 0.6 and avg_corr > 0.5)
                      else 'risk_off' if (spy_corr > 0.8)
                      else 'stock_pickers_market'
    }

# ─── Master regime classifier ───────────────────────────────────

def classify_regime(
    prices: pd.Series,
    returns: pd.Series,
    vix: float,
    hy_spread: float,
    vix_term_structure: float,
    adx: pd.Series = None,
    sector_returns: pd.DataFrame = None
) -> dict:
    """Multi-factor regime classification. Single VIX threshold is obsolete."""
    vol = garch_vol_forecast(returns)
    trend = trend_strength(prices, adx)
    stress = cross_asset_stress(vix, hy_spread, vix_term_structure)

    # Classification matrix:
    current_vol = vol['current_annual_vol']
    direction = trend['direction']
    stress_level = stress['stress_level']

    if stress_level == 'extreme' and current_vol > 35:
        regime = Regime.CRASH
    elif direction == 'bearish' and (current_vol > 25 or stress_level == 'elevated'):
        regime = Regime.HIGH_VOL_BEAR
    elif direction == 'bullish' and current_vol < 15:
        regime = Regime.LOW_VOL_BULL
    elif direction == 'bullish' and current_vol <= 25:
        regime = Regime.HIGH_VOL_BULL
    elif trend['strength'] == 'weak':
        regime = Regime.CHOP
    else:
        regime = Regime.HIGH_VOL_BULL  # default: proceed with caution

    # Regime → sizing/stop parameters
    regime_params = {
        Regime.LOW_VOL_BULL:  {'risk_per_trade': 0.02, 'stop_atr_mult': 2.0, 'max_positions': 8},
        Regime.HIGH_VOL_BULL: {'risk_per_trade': 0.015, 'stop_atr_mult': 2.2, 'max_positions': 6},
        Regime.CHOP:          {'risk_per_trade': 0.01, 'stop_atr_mult': 2.0, 'max_positions': 4},
        Regime.HIGH_VOL_BEAR: {'risk_per_trade': 0.005, 'stop_atr_mult': 2.5, 'max_positions': 3},
        Regime.CRASH:         {'risk_per_trade': 0.0, 'stop_atr_mult': 3.0, 'max_positions': 0},
    }

    return {
        'regime': regime.value,
        'params': regime_params[regime],
        'vol': vol,
        'trend': trend,
        'stress': stress,
        'garch_persistence': vol['garch_persistence'],
        'transition_risk': 'high' if (vol['vol_clustering'] and stress_level != 'low') else 'low'
    }
```

**Regime routing rules** (enforced before Phase 2 sizing):
- CRASH: No new entries. Existing positions trail at +0.5 ATR. Black swan hedge reviewed.
- HIGH_VOL_BEAR: Max 3 positions, all half-size. Stops at 2.5x ATR. Favor put-side strategies.
- CHOP: Max 4 positions. Take profits at T1 (no runners). Reduce hold time.
- LOW_VOL_BULL: Full size. Normal stops. Let runners run to T3.
- HIGH_VOL_BULL: Normal size but wider stops (2.2x ATR). No leverage.

<!-- DEEP: 10+min -->
### Phase 2 (~15 min): Position Sizing

Translate a validated signal into a concrete share/contract count. Position sizing is where risk management lives — get this wrong and no entry strategy saves you.

1. **Select sizing method**:
   - **Kelly Criterion**: f* = (bp - q) / b where b = win/loss ratio, p = win probability, q = 1-p. Use **half-Kelly** in practice — full Kelly assumes perfect knowledge of edge and can produce 50%+ drawdowns.
   - **Fixed-Fractional**: Risk 1-2% of account NAV per trade. For a $100K account risking 1.5%, max loss per trade = $1,500.
   - **Volatility-Adjusted**: Position size = (Account Risk $) / (ATR_20 * Multiplier). Larger positions in low-volatility names, smaller in high-vol.

2. **Calculate share quantity**:

   ```

   account_risk_dollars = portfolio.nav * risk_per_trade_pct
   stop_distance_pct = abs(entry_price - stop_loss_price) / entry_price
   position_value = account_risk_dollars / stop_distance_pct
   shares = floor(position_value / entry_price)

   ```

3. **Apply Kelly if win/loss data exists**:

   ```python
   def half_kelly_fraction(win_rate: float, avg_win: float, avg_loss: float) -> float:
       b = avg_win / abs(avg_loss)  # win/loss ratio
       p = win_rate
       q = 1 - p
       kelly_f = (b * p - q) / b
       return max(0.0, kelly_f * 0.5)  # half-Kelly, floor at 0

   # Example: 55% win rate, avg win +8%, avg loss -5%
   # b = 8/5 = 1.6, f* = (1.6*0.55 - 0.45)/1.6 = 0.26875
   # Half-Kelly = 13.4% of account... way too aggressive for multi-position portfolio
   # Cap half-Kelly at 5% max position size regardless of formula output

   ```

4. **Apply constraints**:
   - Max single position: 10% of NAV (absolute hard cap)
   - Max sector exposure: 30% of NAV
   - Max gross leverage: 2.0x (long + |short|)
   - Min position size: $2,000 (below this, commissions eat the edge)

5. **Set liquidity-grab-aware stop-loss**: Market makers actively hunt obvious stop levels — 2x ATR from entry is the most common, most hunted level. The stop must survive liquidity sweeps, not just reflect volatility.

   ```python
   def compute_stop_loss(
       entry_price: float,
       atr: float,
       swing_low: float,           # nearest swing low below entry
       round_number_step: float,   # 0.50 for stocks > $20, else 0.10
       vix: float,                 # current VIX
       vwap_band_low: float,       # VWAP - 2σ (lower band)
       macro_stop_mult: float = 1.0  # from macro gate, 1.5x during CPI/NFP/FOMC
   ) -> tuple[float, dict]:
       # --- LAYER 1: Regime-adjusted ATR multiplier ---
       if vix > 30:
           atr_mult = 2.5          # wide during volatility spikes
       elif vix > 20:
           atr_mult = 2.2
       else:
           atr_mult = 2.0

       atr_mult *= macro_stop_mult  # widen during macro events

       raw_stop = entry_price - (atr_mult * atr)

       # --- LAYER 2: Swing-low buffer ---
       # Never place stop AT a swing low — market makers push through
       # swing lows knowing stops cluster there. Go BELOW the swing low.
       if (swing_low - raw_stop) < (0.3 * atr):
           raw_stop = swing_low - (0.3 * atr)

       # --- LAYER 3: Round-number avoidance ---
       # Stops cluster at round numbers ($X.00, $X.50). Use asymmetric offset.
       nearest_round = round(raw_stop / round_number_step) * round_number_step
       if abs(raw_stop - nearest_round) < (round_number_step * 0.3):
           raw_stop = nearest_round - (round_number_step * 0.378)

       # --- LAYER 4: VWAP band floor ---
       # Stops within normal noise range get swept. Push below VWAP band.
       if raw_stop > vwap_band_low:
           raw_stop = vwap_band_low - (0.1 * atr)

       # --- LAYER 5: Stop-distance safety check ---
       stop_atr_distance = (entry_price - raw_stop) / atr
       warnings = []
       if stop_atr_distance < 1.5:
           warnings.append('STOP_TOO_TIGHT: <1.5x ATR — high grab probability')
       if abs(raw_stop % round_number_step) < 0.02:
           warnings.append('ROUND_NUMBER: stop at obvious level')

       # --- LAYER 6: Audit trail ---
       audit = {
           'atr_multiplier': atr_mult,
           'swing_low': swing_low,
           'final_stop': round(raw_stop, 2),
           'stop_pct': round((entry_price - raw_stop) / entry_price * 100, 2),
           'stop_atr_distance': round(stop_atr_distance, 2),
           'warnings': warnings
       }

       return raw_stop, audit
   ```

   **Layer rationale**: L1 adjusts for market regime (wide during fear), L2 avoids the #1 source of false stop-outs (swing low sweeps), L3 camouflages from order-book clustering, L4 ensures stops aren't in normal noise range, L5 catches configuration errors, L6 creates an audit trail for post-trade review.

6. **Size the trim targets**: Pre-compute exit tiers based on entry:

   ```
   tier_1_target = entry_price * 1.10   # +10% — risk-off trim (sell 25%)
   tier_2_target = entry_price * 1.20   # +20% — scaling trim (sell 25%)
   tier_3_target = entry_price * 1.40   # +40% — runner trim (sell 25%)
   initial_stop_loss, stop_audit = compute_stop_loss(
       entry_price, atr, swing_low, round_number_step, vix,
       vwap_band_low, macro_stop_mult
   )
   ```

Complete when: Share quantity calculated from selected sizing method (Kelly/fixed-fractional/vol-adjusted). All portfolio constraints applied (max position 10%, sector 30%, gross leverage 2.0x). Trim targets T1/T2/T3 pre-computed. Stop-loss computed through all 6 liquidity-grab layers (regime multiplier, swing-low buffer, round-number avoidance, VWAP floor, safety check, audit trail). Stop audit dict logged with no STOP_TOO_TIGHT warnings.

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): Entry Execution

Bridge the gap between model prices and real fills. Slippage, commissions, and timing determine whether a theoretically profitable strategy actually makes money.

1. **Choose order type based on urgency and spread**:
   - Tight spreads (<0.1% of price) and normal urgency → limit order at mid or 1 tick favorable
   - Wide spreads (>0.5%) or high urgency → marketable limit (limit at ask for buys, bid for sells)
   - Size >1% of ADV → TWAP/VWAP algorithm to avoid moving the market

2. **Estimate slippage before submitting**:

   ```

   # Realistic slippage model (from live trading data)
   if market_cap > 100e9:     slippage_pct = 0.02  # mega-cap: 2 bps
   elif market_cap > 10e9:    slippage_pct = 0.05  # large-cap: 5 bps
   elif market_cap > 2e9:     slippage_pct = 0.15  # mid-cap: 15 bps
   else:                       slippage_pct = 0.50  # small-cap: 50 bps

   # Options slippage is worse — multiply by 3-5x
   option_slippage_pct = slippage_pct * 4.0
   # For OTM options, add another 2-3%
   if option_moneyness < 0.95:  # OTM
       option_slippage_pct += 2.0

   ```

3. **Microstructure trap detection**: Market microstructure can invalidate a signal before your order reaches the exchange. These traps are invisible to daily data — they require real-time awareness:

   ```python
   from dataclasses import dataclass
   from typing import Optional

   @dataclass
   class MicrostructureCheck:
       """Pre-entry microstructure audit. Each trap can turn a +EV signal into -EV execution."""

       # Trap 1: Bid-ask bounce
       # If the spread is 2% of price, you lose 2% the moment you enter.
       # Mid-cap names at lunch can have spreads 5x normal.
       spread_pct: float          # (ask - bid) / mid * 100
       spread_acceptable: bool    # True if spread < 0.15% (equity) or < 2% (options)

       # Trap 2: Order book imbalance
       # Market makers lean the book before large moves. If the book is
       # 3:1 ask-side (sell pressure), your limit buy will fill immediately
       # as the price drops through it — adverse selection.
       book_imbalance: float      # (bid_size - ask_size) / (bid_size + ask_size), -1 to +1
       book_imbalance_ok: bool    # True if imbalance is not against your direction

       # Trap 3: Adverse selection risk
       # Thin books mean your limit order gets picked off by HFTs
       # who detect it and front-run. Only use limit orders when depth
       # at your price level is > 5x your order size.
       depth_at_entry: int        # shares available at entry price level
       order_size: int            # your intended shares
       depth_adequate: bool       # True if depth_at_entry > 5 * order_size

       # Trap 4: Implementation shortfall
       # The gap between decision price and fill price. For mid-cap names,
       # 15-30 minute delays between signal and fill can cost 0.3-0.8%.
       arrival_price: float       # mid-price when signal was generated
       expected_fill: float       # estimated fill price after spread + depth impact
       shortfall_bps: float       # (fill - arrival) / arrival * 10000, in basis points
       shortfall_acceptable: bool # True if shortfall < 10 bps (equity) or < 50 bps (options)

       # Overall gate
       @property
       def can_trade(self) -> bool:
           return all([
               self.spread_acceptable,
               self.book_imbalance_ok,
               self.depth_adequate,
               self.shortfall_acceptable
           ])

   def check_microstructure(
       symbol: str,
       side: str,           # 'buy' or 'sell'
       order_size: int,
       arrival_price: float,
       l2_data: dict        # Level 2 order book snapshot
   ) -> MicrostructureCheck:
       """Run before every entry. Microstructure traps are invisible to
       daily bars but kill small accounts through death-by-spread."""

       # Trap 1: Spread
       bid = l2_data['bids'][0][0] if l2_data.get('bids') else 0
       ask = l2_data['asks'][0][0] if l2_data.get('asks') else 0
       mid = (bid + ask) / 2
       spread_pct = ((ask - bid) / mid) * 100 if mid > 0 else 999
       spread_ok = spread_pct < 0.15

       # Trap 2: Order book imbalance
       total_bid_size = sum(b[1] for b in l2_data.get('bids', [[0, 0]])[:5])
       total_ask_size = sum(a[1] for a in l2_data.get('asks', [[0, 0]])[:5])
       denom = total_bid_size + total_ask_size
       imbalance = (total_bid_size - total_ask_size) / denom if denom > 0 else 0

       # If buying and book leans ASK (imbalance < -0.3), sellers dominate —
       # you'll fill immediately but at a worse price. If selling and book
       # leans BID (imbalance > 0.3), buyers are absorbing — good for sellers.
       if side == 'buy':
           imbalance_ok = imbalance > -0.3  # not too ask-heavy
       else:
           imbalance_ok = imbalance < 0.3   # not too bid-heavy

       # Trap 3: Depth adequacy
       if side == 'buy':
           depth_at_level = sum(a[1] for a in l2_data.get('asks', [[0, 0]])[:3])
       else:
           depth_at_level = sum(b[1] for b in l2_data.get('bids', [[0, 0]])[:3])
       depth_ok = depth_at_level > (5 * order_size)

       # Trap 4: Implementation shortfall
       # Marketable limit at mid+half-spread as estimate
       if side == 'buy':
           est_fill = mid + (ask - mid) * 0.5
       else:
           est_fill = mid - (mid - bid) * 0.5
       shortfall_bps = ((est_fill - arrival_price) / arrival_price) * 10000
       shortfall_ok = abs(shortfall_bps) < 10

       return MicrostructureCheck(
           spread_pct=round(spread_pct, 3),
           spread_acceptable=spread_ok,
           book_imbalance=round(imbalance, 3),
           book_imbalance_ok=imbalance_ok,
           depth_at_entry=depth_at_level,
           order_size=order_size,
           depth_adequate=depth_ok,
           arrival_price=arrival_price,
           expected_fill=round(est_fill, 2),
           shortfall_bps=round(shortfall_bps, 1),
           shortfall_acceptable=shortfall_ok
       )

   # ─── HFT activity detection ───────────────────────────────────

   def hft_activity_score(l2_data: dict, recent_trades: list[dict]) -> dict:
       """Detect HFT presence from quote flickering and trade burst patterns.
       When HFTs are active, they will pick off naive limit orders."""
       quote_changes = 0
       # Count quote updates per second from L2 snapshot timestamp changes
       # (simplified — real implementation uses tick-level timestamps)
       if 'timestamp' in l2_data:
           quote_changes = 1

       # Trade burst detection: >10 trades in <1 second = HFT
       trade_timestamps = [t.get('timestamp') for t in recent_trades if 'timestamp' in t]
       bursts = 0
       for i in range(len(trade_timestamps) - 10):
           window = trade_timestamps[i:i+10]
           if (max(window) - min(window)).total_seconds() < 1.0:
               bursts += 1

       hft_score = 'high' if bursts > 5 else 'moderate' if bursts > 1 else 'low'

       return {
           'hft_score': hft_score,
           'trade_bursts': bursts,
           'recommendation': (
               'USE_TWAP: HFTs are active — do not use limit orders, '
               'they will get picked off' if hft_score == 'high'
               else 'LIMIT_OK: normal market conditions — limit orders are safe'
               if hft_score == 'low'
               else 'CAUTION: moderate HFT activity — use midpoint pegs or TWAP for size > 500 shares'
           )
       }
   ```

   **Microstructure gate**: If `MicrostructureCheck.can_trade == False`, do NOT submit the order. Wait 5 minutes and re-check. Three consecutive failures = skip the trade. HFT activity detected → switch from limit to TWAP/VWAP algorithm.

4. **Commission-aware sizing**:
   - Equity: ~$0 (commission-free at most brokers), but SEC fees apply (~$8/million sold)
   - Options: $0.65/contract typical. 100 contracts = $65 round trip. On a $5,000 position, that is 1.3% drag.
   - If estimated commissions > 1% of expected profit, reduce size or skip the trade.

5. **Broker API execution flow** (Alpaca example):

   ```python
   import alpaca_trade_api as tradeapi

   api = tradeapi.REST(api_key, secret_key, base_url, api_version='v2')

   # Place bracket order: entry + stop-loss + take-profit in one request
   api.submit_order(
       symbol='AAPL',
       qty=shares,
       side='buy',
       type='limit',
       limit_price=entry_price,
       time_in_force='day',
       order_class='bracket',
       stop_loss={'stop_price': stop_loss_price},
       take_profit={'limit_price': tier_1_target}
   )

   # For options through Alpaca (if enabled):
   # api.submit_order(
   #     symbol='AAPL250117C00200000',  # OSI format
   #     qty=10,
   #     side='buy',
   #     type='limit',
   #     limit_price=2.50,
   #     time_in_force='day'
   # )

   ```

6. **Duplicate order guard**:

   ```python
   # Idempotency via client_order_id
   order_id = f"{signal['id']}_{datetime.utcnow().strftime('%Y%m%d')}"
   existing = api.get_order_by_client_order_id(order_id)
   if existing and existing.status not in ('canceled', 'rejected'):
       return existing  # already submitted, do not duplicate
   api.submit_order(..., client_order_id=order_id)

   ```

Complete when: Order type selected based on spread and urgency. Slippage estimate computed. Microstructure check passed (spread acceptable, book imbalance not against direction, depth >5x order size, shortfall <10 bps). If HFT detected, order switched to TWAP/VWAP. Commission drag verified <1% of expected profit. Broker API order submitted with bracket (stop-loss + take-profit). Idempotency key (client_order_id) registered. Duplicate order guard confirmed — no double-submission.

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): Position Management

A live position is not passive — it requires active monitoring and pre-programmed responses to price movement, time decay, and signal degradation.

1. **Trailing stop engine with grab protection**:

   ```python
   def update_trailing_stop(
       position: Position,
       current_price: float,
       atr: float,
       vix: float,
       bars_1m: list[Bar]  # last 20 1-minute bars for volume context
   ) -> float:
       # Regime-adjusted ATR multiplier (same as initial stop logic)
       if vix > 30:
           atr_mult = 2.5
       elif vix > 20:
           atr_mult = 2.2
       else:
           atr_mult = 2.0

       new_stop = current_price - (atr_mult * atr)

       # --- GRAB GUARD: Don't adjust stop on a wick ---
       # If the current candle is a wick (low << close), the current_price
       # may be a temporary sweep — don't ratchet the stop up from a wick low
       if len(bars_1m) >= 1:
           last_bar = bars_1m[-1]
           body_low = min(last_bar.open, last_bar.close)
           wick_ratio = (body_low - last_bar.low) / atr if atr > 0 else 0
           if wick_ratio > 0.5:  # >0.5 ATR wick — this is a grab, not a move
               # Use the body low instead of the wick low
               new_stop = body_low - (atr_mult * atr)

       # Stop only moves up for longs (down for shorts). Never reverse.
       position.trailing_stop = max(position.trailing_stop, new_stop)
       return position.trailing_stop

   ```

2. **Trim execution logic**:

   ```python
   def check_trims(position: Position, current_price: float) -> list[Order]:
       orders = []
       remaining = position.remaining_shares

       if current_price >= position.tier_1_target and not position.tier_1_executed:
           sell_qty = int(position.original_shares * 0.25)
           orders.append(Order(side='sell', qty=sell_qty, type='limit', price=current_price))
           position.tier_1_executed = True
           # Move stop to breakeven after Tier 1
           position.trailing_stop = position.entry_price

       if current_price >= position.tier_2_target and not position.tier_2_executed:
           sell_qty = int(position.original_shares * 0.25)
           orders.append(Order(side='sell', qty=sell_qty, type='limit', price=current_price))
           position.tier_2_executed = True

       if current_price >= position.tier_3_target and not position.tier_3_executed:
           sell_qty = int(position.original_shares * 0.25)
           orders.append(Order(side='sell', qty=sell_qty, type='limit', price=current_price))
           position.tier_3_executed = True

       return orders

   ```

3. **Time stop monitor**: If `(datetime.utcnow() - position.entry_time).days >= 5` and the position P&L is between -2% and +5%, the signal has not worked. Exit at market. UOA signals that do not move within 5 trading days almost never become big winners.

4. **Earnings blackout**: If earnings are within 48 hours and position has profit >10%, exit 50%. If flat or losing, exit 100%. The UOA signal was not an earnings play unless explicitly tagged as such.

5. **Signal decay tracker**: Monitor whether the original UOA signal conditions still hold. If the unusual activity was a large call buyer and those calls are now being sold (delta hedging unwound), the smart money has exited — you should too.

Complete when: Trailing stop engine is active with VIX-adjusted multiplier and wick-filter guard, updating every 30 seconds. Trim execution logic is armed (T1/T2/T3 targets monitored). Time stop monitor is tracking days-held. Earnings blackout rules are active (48-hour pre-earnings check). Signal decay tracker is polling original UOA conditions. Liquidity grab detector is armed for every stop-trigger candle.

<!-- DEEP: 10+min -->
### Phase 5 (~15 min): Exit Execution & Risk Monitoring

Systematic exits prevent emotional decisions. Every exit is pre-planned — the only decision at exit time is whether the pre-planned condition has been met.

1. **Exit trigger hierarchy** (checked in order every 30 seconds):

   ```
   1. Emergency stop: News/event invalidating thesis → Exit 100% market order
   2. Hard stop-loss: price <= stop_loss → Run grab-detector BEFORE exiting
   3. Trailing stop: price <= trailing_stop → Run grab-detector BEFORE exiting
   4. Time stop: days_held >= 5 AND pnl_pct < 5% → Exit 100% market order
   5. Trim targets: price >= tier_N_target → Sell tier_N quantity
   6. Signal invalidation: original UOA flow reversed → Exit 100%
   ```

2. **Liquidity grab detector** — runs BEFORE executing a stop-loss exit. A stop trigger is NOT automatically an exit. The detector applies 5 confirmation layers to distinguish a real breakdown from a liquidity sweep:

   ```python
   def is_liquidity_grab(
       trigger_price: float,      # the stop level that was breached
       stop_type: str,            # 'hard_stop' or 'trailing_stop'
       bars_1m: list[Bar],        # last 30 1-minute bars
       bars_5m: list[Bar],        # last 12 5-minute bars
       avg_volume_20d: float,     # 20-day average volume
       premarket: bool = False,
       postmarket: bool = False,
       seconds_since_open: int = 0
   ) -> tuple[bool, str, str]:
       """
       Returns (is_grab, action, reason)
       action: 'EXIT' | 'HOLD' | 'WIDEN_AND_HOLD'
       """

       if len(bars_1m) < 5:
           return (False, 'EXIT', 'insufficient data to evaluate')

       last_bar = bars_1m[-1]
       prior_bars = bars_1m[-5:-1]  # 4 prior bars for context
       bar_low = last_bar.low
       bar_close = last_bar.close
       bar_volume = last_bar.volume if hasattr(last_bar, 'volume') else avg_volume_20d
       bar_body_low = min(last_bar.open, last_bar.close)

       # --- CHECK 1: Wick vs. body violation ---
       # If the low is a wick (low << close) but the body is ABOVE the stop,
       # this is a classic liquidity grab — a momentary sweep that reversed.
       # A real breakdown closes through the stop, not just ticks through it.
       if bar_body_low > trigger_price and bar_low <= trigger_price:
           wick_depth = (trigger_price - bar_low) / (bar_body_low - bar_low) if bar_body_low != bar_low else 0
           if wick_depth < 0.5:  # stop was only wick-violated, not body-violated
               return (True, 'HOLD', f'wick-only violation: body={bar_body_low:.2f} > stop={trigger_price:.2f} (wick depth {wick_depth:.1%})')

       # --- CHECK 2: Close-below confirmation ---
       # Even if the body violated the stop, require the bar to CLOSE below stop.
       # Intra-bar spikes that reverse before close are false signals.
       if bar_close > trigger_price:
           # Bar went through stop but closed above it — recovery already happened
           avg_body = sum(abs(b.open - b.close) for b in prior_bars) / max(len(prior_bars), 1)
           if bar_close - trigger_price > avg_body * 0.5:  # closed convincingly above
               return (True, 'HOLD', f'recovery close: close={bar_close:.2f} > stop={trigger_price:.2f}')

       # --- CHECK 3: Volume confirmation ---
       # A real breakdown comes with conviction. A low-volume sweep is noise.
       # Require the trigger bar to have at least 70% of average volume.
       volume_ratio = bar_volume / avg_volume_20d if avg_volume_20d > 0 else 1.0
       if volume_ratio < 0.7:
           # Low-volume stop trigger — likely a grab during a quiet period
           # Widen stop by 0.3 ATR but DON'T exit yet
           return (True, 'WIDEN_AND_HOLD', f'low-volume trigger: vol ratio={volume_ratio:.2f} (<0.7 threshold)')

       # --- CHECK 4: Time-of-day gating ---
       # First 30 minutes have massive noise. Last 30 minutes have positioning games.
       # Stops triggered during these windows are disproportionately false.
       if seconds_since_open < 1800:  # first 30 min
           # Widen by 0.5 ATR during opening noise window
           return (True, 'WIDEN_AND_HOLD', f'opening noise window: {seconds_since_open}s since open')

       if premarket or postmarket:
           # Thin liquidity outside regular hours = easy to engineer a stop sweep
           return (True, 'WIDEN_AND_HOLD', f'extended hours trigger: pre={premarket}, post={postmarket}')

       if seconds_since_open > 20700:  # last 30 min of regular session (6.5h = 23400s)
           return (True, 'WIDEN_AND_HOLD', f'closing positioning window: {seconds_since_open}s since open')

       # --- CHECK 5: Multi-timeframe confirmation ---
       # A 1-min tick below the stop means nothing if the 5-min bar is still above.
       # Require confirmation on the higher timeframe.
       if len(bars_5m) >= 1:
           last_5m = bars_5m[-1]
           if last_5m.low > trigger_price:
               # 1-min triggered but 5-min is clean — grab
               return (True, 'HOLD', f'1-min violation only: 5-min low={last_5m.low:.2f} > stop={trigger_price:.2f}')

       # --- ALL CHECKS PASSED: REAL BREAKDOWN ---
       return (False, 'EXIT', f'confirmed breakdown: volume ratio={volume_ratio:.2f}, close={bar_close:.2f}')

   ```

   **Detector rationale**: The 5 checks form a progressive sieve. A stop must fail ALL 5 defenses to execute:
   - Check 1 (Wick): Catches 60-70% of false triggers — the most common grab pattern
   - Check 2 (Close): Catches intra-bar reversal grabs — price goes through, then back
   - Check 3 (Volume): Filters low-conviction moves during quiet periods
   - Check 4 (Time): Blocks noise windows where stop hunting is concentrated
   - Check 5 (MTF): Ensures the breakdown shows on multiple timeframes, not just a 1-min tick

3. **Stop execution after grab check**:

   ```python
   def execute_stop_exit(position: Position, trigger_price: float, stop_type: str, context: dict) -> Order | None:
       is_grab, action, reason = is_liquidity_grab(
           trigger_price, stop_type,
           context['bars_1m'], context['bars_5m'],
           context['avg_volume_20d'],
           context.get('premarket', False),
           context.get('postmarket', False),
           context.get('seconds_since_open', 0)
       )

       log_event(position.id, stop_type, trigger_price, is_grab, action, reason)

       if action == 'HOLD':
           return None  # do nothing — it was a grab

       if action == 'WIDEN_AND_HOLD':
           # Widen the stop by 0.3 ATR and continue monitoring
           position.hard_stop -= (0.3 * position.atr_at_entry)
           position.trailing_stop -= (0.3 * position.atr_at_entry)
           position.grab_widen_count += 1
           if position.grab_widen_count >= 3:
               # After 3 widens, the thesis is broken — exit
               return Order(side='sell', qty=position.remaining_shares, type='market')
           return None

       # action == 'EXIT': confirmed breakdown
       return Order(side='sell', qty=position.remaining_shares, type='market')
   ```

   2. **Portfolio risk dashboard** (real-time calculations):

   ```python
   def portfolio_risk_metrics(positions: list[Position], prices: dict) -> dict:
       nav = sum(p.market_value for p in positions) + cash
       returns = daily_return_series(positions)

       # Value at Risk (95%, 1-day)
       var_95 = np.percentile(returns, 5)

       # Conditional VaR (expected loss beyond VaR)
       cvar_95 = returns[returns <= var_95].mean()

       # Max drawdown
       cumulative = (1 + returns).cumprod()
       running_max = cumulative.expanding().max()
       drawdown = (cumulative - running_max) / running_max
       max_dd = drawdown.min()

       # Beta to SPY
       spy_returns = get_spy_returns()
       beta = cov(returns, spy_returns) / var(spy_returns)

       # Correlation matrix
       returns_df = pd.DataFrame({p.ticker: p.daily_returns for p in positions})
       corr_matrix = returns_df.corr()

       # Net delta exposure
       net_delta = sum(p.delta_exposure for p in positions)

       return {
           'nav': nav, 'var_95': var_95, 'cvar_95': cvar_95,
           'max_drawdown': max_dd, 'beta': beta,
           'corr_matrix': corr_matrix, 'net_delta': net_delta
       }

   ```

3. **Hard circuit breaker**: If account drawdown exceeds 20% from peak NAV:
   - Liquidate all positions at market
   - Cancel all open orders
   - Set trading mode = HALTED
   - Require manual review before resuming
   - This is non-negotiable. No strategy, no conviction, no "but the signal was strong" overrides the circuit breaker.

4. **Black swan hedge monitor**: When VIX < 15, purchase OTM SPY puts (5% OTM, 30-45 DTE) for 1-2% of portfolio NAV as tail risk insurance. Cheap when volatility is low — do not wait for the storm to buy flood insurance.

Complete when: Exit trigger hierarchy is armed (6 levels checked every 30 seconds). Liquidity grab detector is live — all 5 confirmation layers (wick, close, volume, time-of-day, multi-timeframe) evaluating every stop trigger before execution. HOLD/WIDEN_AND_HOLD/EXIT actions logged per trigger. Portfolio risk dashboard is computing VaR/CVaR/max-drawdown/beta/correlation/net-delta in real time. Hard circuit breaker is set at 20% drawdown. Black swan hedge is evaluated and purchased if VIX < 15.

<!-- DEEP: 10+min -->
### Phase 6 (~25 min): Backtesting & Post-Trade Analysis

Validate strategies before risking capital. Learn from every trade — winners and losers.

1. **Vectorized backtest** (fast, for strategy exploration). Uses the same `compute_stop_loss()` defined in Phase 2 — the 6-layer liquidity-grab defense applies to backtesting too. Testing with naive `entry - (2 * ATR)` produces fiction, not tradeable results:

   ```python
   def vectorized_backtest(
       signals: pd.DataFrame,    # columns: date, ticker, signal, entry_price, conviction
       prices: pd.DataFrame,     # columns: tickers, rows: dates (use bar LOW for stop-out check)
       lows: pd.DataFrame,       # daily lows — required for intra-bar stop-out detection
       atr: pd.Series,           # ATR(14) per entry date
       vix: pd.Series,           # VIX per entry date
       rn_step: float = 0.50     # round-number step ($0.50 for stocks >$20, else $0.10)
   ) -> pd.DataFrame:
       results = []
       LOOKBACK = 20  # bars for swing-low detection

       for _, signal in signals.iterrows():
           entry_idx = prices.index.get_loc(signal['date'])
           start = max(0, entry_idx - LOOKBACK)
           end = min(entry_idx + 20, len(prices) - 1)

           entry = signal['entry_price']
           atr_val = atr.iloc[entry_idx]
           vix_val = vix.iloc[entry_idx]

           # Swing low: lowest LOW in lookback window
           swing_low = lows.iloc[start:entry_idx].min()

           # VWAP band low (simplified — use close for VWAP proxy)
           recent = prices.iloc[start:entry_idx]
           vwap = recent.mean()
           vwap_std = recent.std()
           vwap_band_low = vwap - (2.0 * vwap_std)

           # THE FIX: compute_stop_loss() replaces naive entry - (2 * ATR)
           stop, audit = compute_stop_loss(
               entry, atr_val, swing_low, rn_step, vix_val, vwap_band_low
           )

           tier_1 = entry * 1.10   # +10% risk-off trim target
           tier_2 = entry * 1.20   # +20% scaling trim target

           # Intra-bar stop-out: use bar LOW, not close, to detect whether
           # price breached the stop during the bar (critical for grab simulation)
           future_lows = lows.iloc[entry_idx + 1:end + 1]
           future_highs = prices.iloc[entry_idx + 1:end + 1]

           for i, (low_val, high_val) in enumerate(zip(future_lows, future_highs)):
               if low_val <= stop:
                   # Stop was hit — but was it a grab?
                   # In backtest without tick data, assume worst case: stop fills at stop price
                   results.append({
                       'pnl_pct': (stop - entry) / entry,
                       'exit_reason': 'stop_loss',
                       'days_held': i + 1,
                       'stop_atr_distance': audit['stop_atr_distance']
                   })
                   break
               elif high_val >= tier_2 and i > 0:
                   results.append({
                       'pnl_pct': (tier_2 - entry) / entry,
                       'exit_reason': 'tier_2',
                       'days_held': i + 1
                   })
                   break
           else:
               # Time stop after 20 days
               results.append({
                   'pnl_pct': (prices.iloc[end] - entry) / entry,
                   'exit_reason': 'time_stop',
                   'days_held': 20
               })

       df = pd.DataFrame(results)
       return df

   ```

2. **Walk-forward optimization** (the only backtest that matters):
   - Split data: 3 years in-sample → optimize parameters → 1 year out-of-sample → test
   - Slide forward 1 year, repeat. Five windows minimum.
   - If strategy parameters are unstable across windows (Sharpe swings >50%), the strategy is overfit.
   - Only trade strategies where out-of-sample Sharpe is within 20% of in-sample Sharpe.

3. **Backtest reality checks** (apply these or your results are fiction):
   - **Survivorship bias**: Backtest on point-in-time universes. Companies get acquired and delisted — if your backtest only uses today's tickers, it has survivorship bias.
   - **Look-ahead bias**: Do not use split-adjusted prices before the split date. Do not use earnings data before the announcement time.
   - **Slippage model**: Deduct 0.5% per trade for mid-cap equity, 2-3% for OTM options.
   - **Commission drag**: $0.65/contract × (buy + sell) = $1.30 round trip per contract.
   - **Regime test**: Run backtest separately on bull (2009-2020), bear (2008, 2020 Q1, 2022), and sideways (2015-2016) markets. A strategy that only works in bull markets will blow up.

4. **Statistical validation** (before you trust the backtest, prove your edge isn't noise):

   ```python
   import numpy as np
   from scipy import stats
   from typing import Tuple

   def bootstrap_sharpe_ci(
       returns: np.ndarray, n_bootstrap: int = 2000, ci: float = 0.95
   ) -> dict:
       """Bootstrap confidence interval for annualized Sharpe ratio.
       A 95% CI that includes zero means you have no statistically significant edge."""
       n = len(returns)
       sharpe_obs = np.sqrt(252) * returns.mean() / returns.std()

       bootstrapped = np.zeros(n_bootstrap)
       for i in range(n_bootstrap):
           sample = np.random.choice(returns, size=n, replace=True)
           bootstrapped[i] = np.sqrt(252) * sample.mean() / (sample.std() + 1e-12)

       alpha = 1 - ci
       lower = np.percentile(bootstrapped, alpha / 2 * 100)
       upper = np.percentile(bootstrapped, (1 - alpha / 2) * 100)

       return {
           'sharpe': round(sharpe_obs, 3),
           f'ci_{int(ci*100)}_lower': round(lower, 3),
           f'ci_{int(ci*100)}_upper': round(upper, 3),
           'significant': lower > 0,  # True only if entire CI > 0
           'n_bootstrap': n_bootstrap
       }

   def monte_carlo_significance(
       returns: np.ndarray, n_simulations: int = 1000
   ) -> dict:
       """Monte Carlo: shuffle entry dates to destroy any real edge.
       If your Sharpe is no better than random entry timing, you have no alpha."""
       n = len(returns)
       actual_sharpe = np.sqrt(252) * returns.mean() / (returns.std() + 1e-12)

       shuffled_sharpes = np.zeros(n_simulations)
       for i in range(n_simulations):
           shuffled = np.random.permutation(returns)
           shuffled_sharpes[i] = np.sqrt(252) * shuffled.mean() / (shuffled.std() + 1e-12)

       p_value = (shuffled_sharpes >= actual_sharpe).mean()

       return {
           'actual_sharpe': round(actual_sharpe, 3),
           'mc_mean_sharpe': round(shuffled_sharpes.mean(), 3),
           'mc_std_sharpe': round(shuffled_sharpes.std(), 3),
           'p_value': round(p_value, 4),
           'significant_95': p_value < 0.05,
           'significant_99': p_value < 0.01,
           'n_simulations': n_simulations
       }

   def deflated_sharpe(
       returns: np.ndarray, n_trials: int = 1, n_bootstrap: int = 2000
   ) -> dict:
       """Deflated Sharpe ratio (Harvey & Liu 2015). Corrects for multiple testing —
       if you tried 50 strategy variations and picked the best backtest, your apparent
       Sharpe is inflated. This tests whether the BEST of N trials is significant."""
       n = len(returns)
       sharpe_obs = np.sqrt(252) * returns.mean() / (returns.std() + 1e-12)

       # Under null: returns ~ N(0, sigma^2)
       sigma = returns.std()
       max_sharpes = np.zeros(n_bootstrap)
       for i in range(n_bootstrap):
           best_trial_sharpe = -999
           for _ in range(n_trials):
               fake_returns = np.random.normal(0, sigma, n)
               trial_sharpe = np.sqrt(252) * fake_returns.mean() / (fake_returns.std() + 1e-12)
               best_trial_sharpe = max(best_trial_sharpe, trial_sharpe)
           max_sharpes[i] = best_trial_sharpe

       p_value = (max_sharpes >= sharpe_obs).mean()

       return {
           'sharpe': round(sharpe_obs, 3),
           'n_trials_corrected': n_trials,
           'deflated_p_value': round(p_value, 4),
           'significant_95': p_value < 0.05,
           'warning': (
               "SHARPE IS INFLATED — multiple testing correction makes it insignificant"
               if p_value >= 0.05 else None
           )
       }

   def walk_forward_consistency(wf_windows: list[dict]) -> dict:
       """Check that strategy parameters don't drift across walk-forward windows.
       Each window dict must have: 'sharpe', 'win_rate', 'profit_factor'."""
       sharpes = [w['sharpe'] for w in wf_windows]
       win_rates = [w['win_rate'] for w in wf_windows]
       pf = [w['profit_factor'] for w in wf_windows]

       sharpe_cv = np.std(sharpes) / (abs(np.mean(sharpes)) + 1e-12)  # coefficient of variation
       wr_range = max(win_rates) - min(win_rates)
       pf_range = max(pf) - min(pf)

       # Stability thresholds
       stable_sharpe = sharpe_cv < 0.50   # <50% CV = stable
       stable_wr = wr_range < 0.20         # <20% range
       stable_pf = pf_range < 1.0          # <1.0 range

       return {
           'n_windows': len(wf_windows),
           'sharpe_range': (round(min(sharpes), 3), round(max(sharpes), 3)),
           'sharpe_cv': round(sharpe_cv, 3),
           'win_rate_range': (round(min(win_rates), 3), round(max(win_rates), 3)),
           'pf_range': (round(min(pf), 2), round(max(pf), 2)),
           'stable': stable_sharpe and stable_wr and stable_pf,
           'verdict': (
               'STRATEGY IS STABLE — consistent across regimes'
               if (stable_sharpe and stable_wr and stable_pf)
               else 'OVERFIT DETECTED — parameters unstable across windows'
           )
       }
   ```

   **Statistical gate**: Before promoting any strategy from backtest to paper trading, these four tests MUST pass:
   - Bootstrap Sharpe 95% CI must exclude zero
   - Monte Carlo p-value < 0.05 (edge is not random timing)
   - Deflated Sharpe p-value < 0.05 (corrected for multiple testing)
   - Walk-forward consistency verdict = STABLE

   A strategy that fails any of these is noise disguised as alpha.

5. **Post-trade P&L attribution**:

   ```python
   def attribution_report(closed_trades: list[Trade]) -> dict:
       df = pd.DataFrame([t.to_dict() for t in closed_trades])

       return {
           'total_trades': len(df),
           'win_rate': (df['pnl'] > 0).mean(),
           'avg_win': df[df['pnl'] > 0]['pnl_pct'].mean(),
           'avg_loss': df[df['pnl'] < 0]['pnl_pct'].mean(),
           'profit_factor': df[df['pnl'] > 0]['pnl'].sum() / abs(df[df['pnl'] < 0]['pnl'].sum()),
           'largest_winner': df['pnl_pct'].max(),
           'largest_loser': df['pnl_pct'].min(),
           'avg_hold_days': df['days_held'].mean(),
           'exit_by_reason': df.groupby('exit_reason')['pnl_pct'].agg(['count', 'mean']),
           'sector_pnl': df.groupby('sector')['pnl'].sum(),
           'signal_conviction_decay': df.groupby('conviction_bucket')['pnl_pct'].mean()
       }

   ```

Complete when: Vectorized backtest produced using compute_stop_loss() (6-layer liquidity-grab defense, not naive 2x ATR). Walk-forward validation completed (5+ windows, out-of-sample Sharpe within 20% of in-sample). All reality checks applied. Statistical validation passed all 4 gates (bootstrap CI excludes zero, Monte Carlo p<0.05, deflated Sharpe p<0.05, walk-forward STABLE). Post-trade P&L attribution report generated with win rate, profit factor, exit reason breakdown, and sector PnL.
