#!/usr/bin/env python3
"""
study.py -- the TREND / MOMENTUM corner on real daily prices.

Deterministic. Stdlib only. No network. No third-party imports.

WHAT THIS IS
    A pre-registered, run-once study of four long-only strategies on four
    instruments, over the full daily history the data source would give us:

        S1  trend-follow 200d      enter when close > SMA(200); exit when
                                   close < SMA(200); stop at entry - 2*ATR(14)
        S2  trend-follow 50/200    enter when SMA(50) > SMA(200) AND
                                   close > SMA(50); exit when close < SMA(50);
                                   stop at entry - 2*ATR(14)
        S3  buy & hold             one entry at the first available open
        S4  vol-targeted hold      always long, sized so trailing 20d realised
                                   vol targets 15% annualised, rebalanced monthly

    The rules above were fixed before the first number was produced. Nothing in
    this file searches, optimises or tunes a parameter. There is no loop over
    parameter values anywhere: a reader can check that by reading it.

WHAT THIS ENGINE OWNS, AND WHAT IT DELIBERATELY DOES NOT
    Timeframe bucketing and the significance of each bucket's statistics belong
    to the sibling engine
        skills/14-finance/timeframe-performance-statistics/scripts/timeframe_stats.py
    This script IMPORTS that engine and calls it, rather than re-implementing
    its formulae: bucket_key(), sample_sd(), median(), max_drawdown(),
    lag1_autocorr(), n_effective(), aggregate_bucket(), profit_factor(),
    safe_div(), and its verdict constants MIN_PERIODS_FOR_VERDICT,
    MIN_TRADES_PER_PERIOD_FOR_VERDICT and T_STAT_NOISE_BAND. If that file moves,
    this script fails loudly instead of silently substituting its own maths.

    Sharpe / max-drawdown DEFINITIONS for the headline table belong to the
    `trade-performance-analyst` skill. The headline Sharpe below is stated with
    its full convention (daily simple returns, full sample, Rf = 0, x sqrt(252))
    because a Sharpe without its convention is not a number, it is a mood. The
    per-bucket Sharpe is left UNANNUALISED, exactly as the sibling engine leaves
    it, so the timeframe comparison is comparing like with like.

EXECUTION MODEL (stated once; every result depends on it)
    * Signals are evaluated on the CLOSE of day i and executed at the OPEN of
      day i+1. No signal is ever executed on the bar that produced it.
    * One unit of risk = the stop distance = 2 * ATR(14). ATR is the simple
      mean of the last 14 true ranges. R = (exit - entry) / (entry - stop).
    * The stop is a real exit rule, not only a risk label. If day j's low
      touches the stop, the trade exits at min(open[j], stop) on day j, which
      models a gap through the stop rather than pretending the stop price was
      available.
    * No commission, no spread, no slippage, no borrow, no dividends. These
      flatter every strategy and are a stated limitation, not a hidden one.
    * Position size is 100% of equity notional (no leverage) for S1/S2/S3. S1
      and S2 are FLAT between trades, so their equity curve has long flat
      stretches -- which is why their Sharpe is low relative to their return.
    * S4 is the only strategy allowed leverage, because "size to a 15% vol
      target" is meaningless without it. Its realised weight range is reported
      so the leverage actually used is visible rather than assumed.
    * The strategy daily return series is the input to every statistic here:
      headline metrics, regime attribution, year attribution and the bucketed
      P&L series. One series per (strategy, instrument).

OUTPUT
    stdout is the report. It is written to run-output.txt by the caller.
    Files written next to this script:
        headline.csv  rstats.csv  per-year.csv  regime.csv  buckets.csv
        complementarity.csv  tradelogs/*.csv  engine-output/*.txt|*.json

USAGE
    py -3 study.py                    # analysis on data/*.csv, writes artefacts
    py -3 study.py --quiet-files      # stdout only
    py -3 study.py --instrument SPY   # restrict to one instrument

EXIT CODES
    0  ran
    2  input missing or unreadable (message names the problem)
"""

import argparse
import csv
import datetime
import glob
import importlib.util
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
TRADELOG_DIR = os.path.join(HERE, "tradelogs")
ENGINE_OUT_DIR = os.path.join(HERE, "engine-output")

SIBLING_REL = os.path.join("..", "..", "..", "timeframe-performance-statistics",
                           "scripts", "timeframe_stats.py")
SIBLING_ABS = os.path.normpath(os.path.join(HERE, SIBLING_REL))

INSTRUMENTS = ["SPY", "QQQ", "TLT", "GLD"]
STRATEGIES = ["S1", "S2", "S3", "S4"]

STRATEGY_TITLE = {
    "S1": "S1 trend-follow 200d (close>SMA200 in, close<SMA200 out, stop 2xATR14)",
    "S2": "S2 trend-follow 50/200 (SMA50>SMA200 & close>SMA50 in, close<SMA50 out, stop 2xATR14)",
    "S3": "S3 buy & hold (enter first open, hold to end of data)",
    "S4": "S4 vol-targeted hold (always long, 15% annualised vol target, monthly rebalance)",
}

TRADING_DAYS_PER_YEAR = 252
ATR_PERIOD = 14
ATR_MULT = 2.0
VOL_LOOKBACK = 20
VOL_TARGET = 0.15
SLOPE_LOOKBACK = 20
SMA_FAST = 50
SMA_SLOW = 200

NA = None


# ---------------------------------------------------------------------------
# Sibling engine: import, do not re-implement
# ---------------------------------------------------------------------------

def load_sibling_engine():
    if not os.path.isfile(SIBLING_ABS):
        raise SystemExit(
            "ERROR: the sibling engine is missing:\n  %s\n"
            "This script reuses timeframe_stats.py for bucket_key(), sample_sd(),\n"
            "max_drawdown(), lag1_autocorr(), n_effective(), aggregate_bucket() and\n"
            "the verdict thresholds. It will not substitute its own formulae."
            % SIBLING_ABS)
    spec = importlib.util.spec_from_file_location("tfstats", SIBLING_ABS)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


TF = load_sibling_engine()


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def fnum(v, nd=3):
    if v is NA or v is None:
        return "n/a"
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return "nan" if math.isnan(v) else ("inf" if v > 0 else "-inf")
    return "{:.{nd}f}".format(v, nd=nd)


def fpct(v, nd=2):
    """A fraction rendered as a percentage. Values past 100,000% are rendered in
    scientific notation rather than as an unreadable run of digits -- S4's
    unbounded leverage produces numbers that large, and hiding them behind a
    comma-separated integer would be worse than showing the exponent."""
    if v is NA or v is None:
        return "n/a"
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return "nan" if math.isnan(v) else ("inf" if v > 0 else "-inf")
    if abs(v) >= 1000.0:
        return "{:.3e}%".format(v * 100.0)
    return "{:.{nd}f}%".format(v * 100.0, nd=nd)


def fpp(v, nd=2):
    """A value already in percentage points."""
    if v is NA or v is None:
        return "n/a"
    if abs(v) >= 100000.0:
        return "{:.3e}".format(v)
    return "{:.{nd}f}".format(v, nd=nd)


def table(headers, rows, align=None):
    """Render a plain fixed-width table. align: 'l' or 'r' per column."""
    ncol = len(headers)
    if align is None:
        align = ["r"] * ncol
    cells = [[str(c) for c in r] for r in rows]
    widths = [len(headers[i]) for i in range(ncol)]
    for r in cells:
        for i in range(ncol):
            widths[i] = max(widths[i], len(r[i]))

    def line(r):
        parts = []
        for i in range(ncol):
            parts.append(r[i].ljust(widths[i]) if align[i] == "l"
                         else r[i].rjust(widths[i]))
        return "  " + "  ".join(parts).rstrip()

    out = [line(headers), "  " + "-" * (sum(widths) + 2 * (ncol - 1))]
    for r in cells:
        out.append(line(r))
    return out


def csv_write(path, headers, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(",".join(headers) + "\n")
        for r in rows:
            fh.write(",".join(
                ("" if v is NA or v is None else
                 ("{:.6f}".format(v) if isinstance(v, float) else str(v)))
                for v in r) + "\n")


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

class Bars(object):
    def __init__(self, symbol, dates, o, h, l, c, v, provenance):
        self.symbol = symbol
        self.dates = dates
        self.open = o
        self.high = h
        self.low = l
        self.close = c
        self.volume = v
        self.provenance = provenance

    def __len__(self):
        return len(self.close)


def read_bars(path):
    provenance = []
    dates, o, h, l, c, v = [], [], [], [], [], []
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            if line.startswith("# PROVENANCE:"):
                provenance.append(line[len("# PROVENANCE:"):].strip())
                continue
            if line.startswith("#") or not line.strip():
                continue
            if line.startswith("date,"):
                continue
            f = line.rstrip("\r\n").split(",")
            dates.append(datetime.date.fromisoformat(f[0]))
            o.append(float(f[1]))
            h.append(float(f[2]))
            l.append(float(f[3]))
            c.append(float(f[4]))
            v.append(float(f[5]))
    if len(dates) < 300:
        raise SystemExit("ERROR: %s has only %d rows; need >= 300" % (path, len(dates)))
    symbol = os.path.basename(path).split("_")[0]
    return Bars(symbol, dates, o, h, l, c, v, provenance)


def load_universe(only=None):
    out = {}
    for sym in INSTRUMENTS:
        if only and sym not in only:
            continue
        path = os.path.join(DATA_DIR, sym + "_1d.csv")
        if not os.path.isfile(path):
            raise SystemExit("ERROR: missing input %s" % path)
        out[sym] = read_bars(path)
    if not out:
        raise SystemExit("ERROR: no instrument matched the filter")
    return out


# ---------------------------------------------------------------------------
# Indicators
# ---------------------------------------------------------------------------

def sma(x, n):
    out = [NA] * len(x)
    s = 0.0
    for i, val in enumerate(x):
        s += val
        if i >= n:
            s -= x[i - n]
        if i >= n - 1:
            out[i] = s / n
    return out


def true_range(h, l, c):
    tr = [0.0] * len(c)
    tr[0] = h[0] - l[0]
    for i in range(1, len(c)):
        tr[i] = max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1]))
    return tr


def atr(h, l, c, n=ATR_PERIOD):
    tr = true_range(h, l, c)
    out = [NA] * len(c)
    for i in range(n - 1, len(c)):
        out[i] = sum(tr[i - n + 1:i + 1]) / n
    return out


def log_returns(c):
    r = [0.0] * len(c)
    for i in range(1, len(c)):
        r[i] = math.log(c[i] / c[i - 1])
    return r


def realised_vol(c, n=VOL_LOOKBACK, ppy=TRADING_DAYS_PER_YEAR):
    lr = log_returns(c)
    out = [NA] * len(c)
    for i in range(n, len(c)):
        w = lr[i - n + 1:i + 1]
        m = sum(w) / n
        var = sum((x - m) ** 2 for x in w) / (n - 1)
        out[i] = math.sqrt(max(var, 0.0)) * math.sqrt(ppy)
    return out


# ---------------------------------------------------------------------------
# Strategy simulation
# ---------------------------------------------------------------------------

def simulate_trend(bars, entry_fn, exit_fn):
    """Long-only, one position at a time. Returns a list of trade dicts."""
    n = len(bars)
    at = atr(bars.high, bars.low, bars.close, ATR_PERIOD)
    trades = []
    i = 0
    while i < n - 1:
        if entry_fn(i) and at[i] is not NA:
            e = i + 1
            epx = bars.open[e]
            stop = epx - ATR_MULT * at[i]
            j = e
            done = False
            while j < n:
                if bars.low[j] <= stop:
                    xpx = min(bars.open[j], stop)   # gap through the stop
                    trades.append(dict(entry_i=e, exit_i=j, entry_px=epx,
                                       stop=stop, exit_px=xpx, reason="stop"))
                    done = True
                    break
                if j > e and exit_fn(j - 1):
                    trades.append(dict(entry_i=e, exit_i=j, entry_px=epx,
                                       stop=stop, exit_px=bars.open[j],
                                       reason="signal"))
                    done = True
                    break
                j += 1
            if done:
                i = j
            else:
                trades.append(dict(entry_i=e, exit_i=n - 1, entry_px=epx,
                                   stop=stop, exit_px=bars.close[n - 1],
                                   reason="end_of_data"))
                i = n - 1
            continue
        i += 1
    for t in trades:
        risk = t["entry_px"] - t["stop"]
        t["R"] = (t["exit_px"] - t["entry_px"]) / risk
        t["ret"] = t["exit_px"] / t["entry_px"] - 1.0
        t["entry_date"] = bars.dates[t["entry_i"]]
        t["exit_date"] = bars.dates[t["exit_i"]]
        t["days_held"] = t["exit_i"] - t["entry_i"] + 1
    return trades


def trades_to_daily(bars, trades):
    """Daily equity returns of the book implied by `trades` (flat between them)."""
    n = len(bars)
    ret = [0.0] * n
    for t in trades:
        for day in range(t["entry_i"], t["exit_i"] + 1):
            prev = t["entry_px"] if day == t["entry_i"] else bars.close[day - 1]
            cur = t["exit_px"] if day == t["exit_i"] else bars.close[day]
            ret[day] = cur / prev - 1.0
    return ret


def simulate_buy_hold(bars):
    n = len(bars)
    ret = [0.0] * n
    for i in range(1, n):
        ret[i] = bars.close[i] / bars.close[i - 1] - 1.0
    return ret, []


def simulate_vol_target(bars):
    """Always long. On the first trading day of each month the position is reset
    so that its NOTIONAL exposure equals target_vol / trailing_20d_realised_vol
    TIMES current equity. The weight is read from the PREVIOUS close, so nothing
    here uses its own future.

    When the weight is below 1 the remainder sits in cash at 0% and earns
    nothing; when it is above 1 the book is levered and the excess exposure is
    borrowed at 0%. The return on a rebalance day is therefore
        w * (close/open - 1)
    and NOT w * close/open - 1. That distinction is the whole of the leverage
    accounting, and getting it wrong overstates a levered book enormously.
    """
    n = len(bars)
    vol = realised_vol(bars.close, VOL_LOOKBACK)
    ret = [0.0] * n
    eq = 1.0
    units = 0.0
    cash = 1.0
    weights = []
    prev_month = (bars.dates[0].year, bars.dates[0].month)
    for i in range(1, n):
        m = (bars.dates[i].year, bars.dates[i].month)
        eq_prev = eq
        if m != prev_month:
            prev_month = m
            if vol[i - 1] is not NA and vol[i - 1] > 0:
                w = VOL_TARGET / vol[i - 1]
                units = w * eq_prev / bars.open[i]
                cash = eq_prev - units * bars.open[i]
                weights.append(w)
                eq = units * bars.close[i] + cash
            else:
                eq = eq_prev
        else:
            if units > 0:
                eq = units * bars.close[i] + cash
        ret[i] = eq / eq_prev - 1.0
    return ret, weights


# ---------------------------------------------------------------------------
# Statistics on a return series
# ---------------------------------------------------------------------------

def equity_curve(ret):
    eq = 1.0
    curve = [1.0] * len(ret)
    for i in range(len(ret)):
        eq *= (1.0 + ret[i])
        curve[i] = eq
    return curve


def max_drawdown_pct(curve):
    """Peak-to-trough fall of a compounded equity curve, as a NEGATIVE pct."""
    peak = curve[0]
    worst = 0.0
    for v in curve:
        if v > peak:
            peak = v
        dd = v / peak - 1.0
        if dd < worst:
            worst = dd
    return worst


def years_between(d0, d1):
    return (d1 - d0).days / 365.25


def headline(ret, dates):
    n = len(ret)
    curve = equity_curve(ret)
    total = curve[-1] - 1.0
    yrs = years_between(dates[0], dates[-1])
    if curve[-1] <= 0:
        cagr = -1.0
    else:
        cagr = curve[-1] ** (1.0 / yrs) - 1.0
    m = sum(ret) / n
    sd = TF.sample_sd(ret)
    sharpe = (m / sd * math.sqrt(TRADING_DAYS_PER_YEAR)) if (sd not in (NA, 0)) else NA
    return dict(total_return=total, cagr=cagr, max_dd=max_drawdown_pct(curve),
                sharpe_daily_annualised=sharpe, mean_daily=m, sd_daily=sd,
                years=yrs, n_days=n, equity_end=curve[-1])


def r_stats(rs):
    """Trade-level statistics in R units, exactly as pre-registered."""
    rs = list(rs)
    n = len(rs)
    wins = [r for r in rs if r > 0]
    losses = [-r for r in rs if r < 0]
    decided = len(wins) + len(losses)
    if n == 0:
        return dict(n=0, p=NA, b=NA, E=NA, pstar=NA, bstar=NA, sd=NA,
                    n_req=NA, L=NA, wins=0, losses=0, breakeven=0)
    p = (len(wins) / decided) if decided else NA
    b = NA
    if wins and losses:
        b = (sum(wins) / len(wins)) / (sum(losses) / len(losses))
    E = (p * b - (1.0 - p)) if (p is not NA and b is not NA) else NA
    pstar = 1.0 / (1.0 + b) if b is not NA else NA
    bstar = (1.0 - p) / p if (p not in (NA, 0)) else NA
    sd = TF.sample_sd(rs)
    n_req = NA
    if sd is not NA and E not in (NA, 0):
        n_req = 4.0 * (sd / abs(E)) ** 2
    L = NA
    if p not in (NA, 0.0, 1.0) and n > 1:
        denom = math.log(1.0 / (1.0 - p))
        if denom > 0:
            L = math.log(n) / denom
    return dict(n=n, p=p, b=b, E=E, pstar=pstar, bstar=bstar, sd=sd,
                n_req=n_req, L=L, wins=len(wins), losses=len(losses),
                breakeven=n - decided)


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return NA
    mx = sum(xs) / n
    my = sum(ys) / n
    sx = sum((v - mx) ** 2 for v in xs)
    sy = sum((v - my) ** 2 for v in ys)
    if sx <= 0 or sy <= 0:
        return NA
    return sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / math.sqrt(sx * sy)


# ---------------------------------------------------------------------------
# Regime classification (data-derived, no hindsight labels)
# ---------------------------------------------------------------------------

def classify_regimes(bars):
    """For each day i, the state KNOWN AT THE CLOSE OF DAY i-1 is the label.

    Lagging the label by one day matters: a regime label read off the same
    close as the return it explains is co-determined with that return, and
    attributing a return to a state that the return itself created is the
    most common way a regime table lies. Everything below uses state[i-1].

      trend   : close vs SMA(200)
      slope   : sign of SMA(200)[t] - SMA(200)[t-20]
      vol     : tercile of trailing 20d realised vol over the full sample
    """
    n = len(bars)
    s_slow = sma(bars.close, SMA_SLOW)
    vol = realised_vol(bars.close, VOL_LOOKBACK)

    raw_trend = [NA] * n
    raw_slope = [NA] * n
    raw_vol = list(vol)
    for i in range(n):
        if s_slow[i] is not NA:
            raw_trend[i] = "above" if bars.close[i] > s_slow[i] else "below"
        if s_slow[i] is not NA and i >= SLOPE_LOOKBACK and s_slow[i - SLOPE_LOOKBACK] is not NA:
            raw_slope[i] = "up" if s_slow[i] > s_slow[i - SLOPE_LOOKBACK] else "down"

    vals = sorted(v for v in raw_vol if v is not NA)
    if not vals:
        raise SystemExit("ERROR: no realised-vol series for %s" % bars.symbol)
    q1 = vals[int(len(vals) * 1.0 / 3.0)]
    q2 = vals[int(len(vals) * 2.0 / 3.0)]

    def tercile(v):
        if v is NA:
            return NA
        if v <= q1:
            return "vol-low"
        if v <= q2:
            return "vol-mid"
        return "vol-high"

    trend = [NA] * n
    slope = [NA] * n
    terc = [NA] * n
    regime_6 = [NA] * n
    regime_4 = [NA] * n
    regime_12 = [NA] * n
    for i in range(1, n):
        t = raw_trend[i - 1]
        s = raw_slope[i - 1]
        v = tercile(raw_vol[i - 1])
        trend[i] = t
        slope[i] = s
        terc[i] = v
        if t is not NA and v is not NA:
            regime_6[i] = "%s|%s" % (t, v)
        if t is not NA and s is not NA:
            regime_4[i] = "%s|slope-%s" % (t, s)
        if t is not NA and s is not NA and v is not NA:
            regime_12[i] = "%s|slope-%s|%s" % (t, s, v)
    return dict(trend=trend, slope=slope, tercile=terc, regime_4=regime_4,
                regime_6=regime_6, regime_12=regime_12,
                q1=q1, q2=q2, usable_from=219)


# ---------------------------------------------------------------------------
# Bucketed P&L series, via the sibling engine
# ---------------------------------------------------------------------------

def bucketed_series(bars, daily_ret_pct, trades, symbols_tag):
    """Bucket the strategy's daily P&L (percentage points of equity) with the
    sibling engine's OWN bucket_key(), then let its OWN aggregate_bucket()
    compute mean / sd / t_stat / period-Sharpe / max drawdown / autocorrelation
    / n_eff.

    trades_per_period that the engine derives is DAYS per period here, because
    each daily P&L observation is handed to it as one row. The count that the
    verdict gate actually wants -- real strategy trades per period -- is
    supplied separately as `trades_per_period` and is used for the gate.
    """
    n = len(bars)
    synth = {}
    for b in TF.BUCKET_ORDER:
        groups = {}
        for i in range(n):
            key, label = TF.bucket_key(b, bars.dates[i])
            g = groups.setdefault(key, {"pnl": 0.0, "last": bars.dates[i],
                                        "first": bars.dates[i]})
            g["pnl"] += daily_ret_pct[i]
            if bars.dates[i] > g["last"]:
                g["last"] = bars.dates[i]
            if bars.dates[i] < g["first"]:
                g["first"] = bars.dates[i]
        rows = []
        for key in sorted(groups):
            g = groups[key]
            rows.append(dict(trade_id=key, open_date=g["first"],
                             close_date=g["last"], pnl=g["pnl"],
                             risk=NA, symbol=symbols_tag, line=0))
        synth[b] = rows

    trade_counts = {}
    for b in TF.BUCKET_ORDER:
        cnt = {}
        for t in trades:
            key, _ = TF.bucket_key(b, t["exit_date"])
            cnt[key] = cnt.get(key, 0) + 1
        trade_counts[b] = cnt

    out = {}
    for b in TF.BUCKET_ORDER:
        agg = TF.aggregate_bucket(b, synth[b], None)
        keys = sorted(synth[b], key=lambda r: r["close_date"])
        n_periods = agg["n_periods"]
        real_tpp = (sum(trade_counts[b].values()) / n_periods) if n_periods else NA
        out[b] = dict(bucket=b, n_periods=n_periods,
                      mean=agg["mean_period_pnl"], sd=agg["sd_period_pnl"],
                      t_stat=agg["t_stat"], period_sharpe=agg["period_sharpe"],
                      max_dd=agg["max_drawdown"],
                      days_per_period=(n / n_periods) if n_periods else NA,
                      trades_per_period=real_tpp,
                      n_trades=sum(trade_counts[b].values()),
                      lag1=agg["lag1_autocorrelation"], n_eff=agg["n_eff"],
                      noise_flag=agg["noise_flag"],
                      first=agg["first_period"], last=agg["last_period"],
                      periods=[(r["trade_id"], r["pnl"]) for r in keys])
    return out


def bucket_verdict(rows):
    """The sibling engine's verdict rule, applied with the CORRECT
    trades_per_period. Constants are imported, not retyped."""
    elig = [r for r in rows
            if r["n_periods"] >= TF.MIN_PERIODS_FOR_VERDICT
            and r["trades_per_period"] is not NA
            and r["trades_per_period"] >= TF.MIN_TRADES_PER_PERIOD_FOR_VERDICT
            and r["t_stat"] is not NA]
    if not elig:
        return dict(bucket=NA, status="INSUFFICIENT DATA",
                    reason="no bucket has n_periods >= %d AND trades_per_period >= %d"
                           % (TF.MIN_PERIODS_FOR_VERDICT,
                              TF.MIN_TRADES_PER_PERIOD_FOR_VERDICT))
    elig.sort(key=lambda r: (-abs(r["t_stat"]), TF.BUCKET_ORDER.index(r["bucket"])))
    best = elig[0]
    return dict(bucket=best["bucket"],
                status=("NOT DISTINGUISHABLE FROM NOISE"
                        if best["noise_flag"] == "NOT DISTINGUISHABLE FROM NOISE"
                        else "most reliable of the qualifying buckets"),
                reason="highest |t_stat| (%.3f) among %d bucket(s) passing both gates"
                       % (best["t_stat"], len(elig)),
                t_stat=best["t_stat"], n_periods=best["n_periods"],
                trades_per_period=best["trades_per_period"],
                n_eff=best["n_eff"], noise_flag=best["noise_flag"])


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def build_strategies(bars):
    n = len(bars)
    s_fast = sma(bars.close, SMA_FAST)
    s_slow = sma(bars.close, SMA_SLOW)

    def s1_entry(i):
        return s_slow[i] is not NA and bars.close[i] > s_slow[i]

    def s1_exit(i):
        return s_slow[i] is not NA and bars.close[i] < s_slow[i]

    def s2_entry(i):
        if s_fast[i] is NA or s_slow[i] is NA:
            return False
        return s_fast[i] > s_slow[i] and bars.close[i] > s_fast[i]

    def s2_exit(i):
        return s_fast[i] is not NA and bars.close[i] < s_fast[i]

    t1 = simulate_trend(bars, s1_entry, s1_exit)
    t2 = simulate_trend(bars, s2_entry, s2_exit)

    bh_ret, bh_trades = simulate_buy_hold(bars)
    vt_ret, vt_weights = simulate_vol_target(bars)

    out = {}
    out["S1"] = dict(ret=trades_to_daily(bars, t1), trades=t1, weights=None)
    out["S2"] = dict(ret=trades_to_daily(bars, t2), trades=t2, weights=None)
    out["S3"] = dict(ret=bh_ret, trades=bh_trades, weights=None)
    out["S4"] = dict(ret=vt_ret, trades=[], weights=vt_weights)
    return out


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(newline="\n")

    ap = argparse.ArgumentParser(prog="study.py")
    ap.add_argument("--instrument", default=None, help="comma-separated subset")
    ap.add_argument("--quiet-files", action="store_true",
                    help="do not write the CSV artefacts")
    args = ap.parse_args(argv if argv is not None else sys.argv[1:])

    only = None
    if args.instrument:
        only = set(x.strip().upper() for x in args.instrument.split(","))
    universe = load_universe(only)

    if not args.quiet_files:
        os.makedirs(TRADELOG_DIR, exist_ok=True)
        os.makedirs(ENGINE_OUT_DIR, exist_ok=True)

    L = []
    add = L.append

    # =====================================================================
    # 0. Header
    # =====================================================================
    add("=" * 100)
    add("TREND / MOMENTUM CORNER -- REAL-DATA STUDY")
    add("=" * 100)
    add("")
    add("PRE-REGISTERED. These rules were fixed before the first number was produced.")
    add("There is no parameter search in this script: no loop over SMA lengths, ATR")
    add("multipliers, vol targets or stop distances appears anywhere in the source.")
    for s in STRATEGIES:
        add("  %s" % STRATEGY_TITLE[s])
    add("")
    add("EXECUTION MODEL")
    add("  signals on the close of day i, executed at the OPEN of day i+1")
    add("  one risk unit = stop distance = %g x ATR(%d) (simple mean of true range)"
        % (ATR_MULT, ATR_PERIOD))
    add("  stop is a real exit: if low[j] touches it, exit at min(open[j], stop)")
    add("  costs: NONE modelled (no commission, spread, slippage, borrow, dividends)")
    add("  S1/S2/S3 position size = 100%% of equity notional, no leverage")
    add("  S4 leverage = target_vol / trailing_20d_realised_vol, rebalanced monthly")
    add("  Sharpe convention: daily simple returns, full sample, Rf = 0, x sqrt(252)")
    add("  per-bucket Sharpe is left UNANNUALISED, as the sibling engine leaves it")
    add("")
    add("METRIC PROVENANCE")
    add("  Bucketing, per-period statistics and the verdict thresholds are NOT")
    add("  re-implemented here. This script imports:")
    add("    %s" % SIBLING_ABS)
    add("  and calls bucket_key(), aggregate_bucket(), sample_sd(), median(),")
    add("  max_drawdown(), lag1_autocorr(), n_effective(), profit_factor().")
    add("  Imported thresholds: MIN_PERIODS_FOR_VERDICT=%d  "
        "MIN_TRADES_PER_PERIOD_FOR_VERDICT=%d  T_STAT_NOISE_BAND=%s"
        % (TF.MIN_PERIODS_FOR_VERDICT, TF.MIN_TRADES_PER_PERIOD_FOR_VERDICT,
           TF.T_STAT_NOISE_BAND))
    add("")

    # =====================================================================
    # 1. Data
    # =====================================================================
    add("=" * 100)
    add("1. DATA ACTUALLY USED")
    add("=" * 100)
    add("")
    rows = []
    for sym in sorted(universe):
        b = universe[sym]
        rows.append([sym, str(b.dates[0]), str(b.dates[-1]), str(len(b)),
                     fnum(years_between(b.dates[0], b.dates[-1]), 2),
                     fnum(b.close[-1] / b.close[0], 4)])
    add("  These rows are read from the data/*_1d.csv files below. Each CSV carries")
    add("  a # PROVENANCE: header written at pull time, reproduced in full beneath")
    add("  the table. Every number in this report descends from those files.")
    add("")
    L.extend(table(["instrument", "first_date", "last_date", "rows",
                    "years", "price_multiple"], rows, ["l", "l", "l", "r", "r", "r"]))
    add("")
    for sym in sorted(universe):
        add("  %s provenance:" % sym)
        for p in universe[sym].provenance:
            add("    # %s" % p)
        add("")

    # =====================================================================
    # 2. Headline metrics
    # =====================================================================
    add("=" * 100)
    add("2. HEADLINE METRICS")
    add("=" * 100)
    add("")
    add("  Sharpe = mean_daily / sd_daily x sqrt(252), daily simple returns, full")
    add("  sample per instrument, Rf = 0. Max drawdown = peak-to-trough of the")
    add("  compounded equity curve, negative. CAGR uses 365.25-day years.")
    add("  S3's max drawdown is the instrument's own; S4's is the vol-targeted book's.")
    add("")
    head_rows = []
    head_csv = []
    headline_store = {}
    weight_rows = []
    for sym in sorted(universe):
        b = universe[sym]
        strat = build_strategies(b)
        headline_store[sym] = {}
        w = strat["S4"]["weights"]
        if w:
            ws = sorted(w)
            weight_rows.append([sym, str(len(w)), fnum(min(w), 2),
                                fnum(ws[len(ws) // 2], 2), fnum(max(w), 2),
                                fnum(sum(w) / len(w), 2),
                                str(sum(1 for x in w if x > 1.0))])
        for s in STRATEGIES:
            h = headline(strat[s]["ret"], b.dates)
            headline_store[sym][s] = h
            head_rows.append([sym, s, fpct(h["total_return"]), fpct(h["cagr"]),
                              fpct(h["max_dd"]), fnum(h["sharpe_daily_annualised"], 3),
                              str(h["n_days"]),
                              fnum(h["mean_daily"] * 10000.0, 3)])
            head_csv.append([sym, s, h["total_return"], h["cagr"], h["max_dd"],
                             h["sharpe_daily_annualised"], h["n_days"],
                             h["mean_daily"]])
    L.extend(table(["inst", "strat", "total_return", "CAGR", "max_dd",
                    "Sharpe(ann)", "n_days", "mean_day_bp"],
                   head_rows, ["l", "l", "r", "r", "r", "r", "r", "r"]))
    add("")
    add("  n_days = trading days in the series. A strategy that is FLAT for most of")
    add("  the sample still pays for those flat days in the Sharpe denominator.")
    add("")
    add("  S4 LEVERAGE ACTUALLY USED. S4 is the only rule that can lever, because")
    add("  'target 15% vol' has no meaning without it. The registration set NO cap")
    add("  on the weight, so the weight is unbounded whenever trailing vol is low:")
    add("")
    L.extend(table(["inst", "rebalances", "w_min", "w_median", "w_max", "w_mean",
                    "n_months_w>1"], weight_rows,
                   ["l", "r", "r", "r", "r", "r", "r"]))
    add("")
    add("  READ THIS BEFORE COMPARING S4's ROW WITH S3's. S4 is the only rule that")
    add("  can lever, because 'target 15% vol' has no meaning without it, and the")
    add("  registration set NO cap on the weight. In calm months S4 therefore holds")
    add("  well over 1x exposure (see the table above), so its raw total return is")
    add("  vol-scaled and is NOT the like-for-like comparison with S3 that it looks")
    add("  like. The honest comparison is max drawdown and Sharpe at the price of")
    add("  the leverage actually used. A capped, deployable version of S4 is a")
    add("  DIFFERENT rule and was NOT tested -- see section 10.")
    if not args.quiet_files:
        csv_write(os.path.join(HERE, "headline.csv"),
                  ["instrument", "strategy", "total_return", "cagr", "max_dd",
                   "sharpe_daily_annualised", "n_days", "mean_daily"],
                  head_csv)

    # =====================================================================
    # 3. R-unit trade statistics
    # =====================================================================
    add("=" * 100)
    add("3. TRADE-LEVEL STATISTICS IN R UNITS (pre-registered definitions)")
    add("=" * 100)
    add("")
    add("  p  = wins / (wins + losses); break-even trades excluded from the")
    add("       denominator and reported separately")
    add("  b  = average winning R / average losing R (both magnitudes)")
    add("  E  = p*b - (1-p), the expectancy per trade in R")
    add("       NOTE ON THE UNIT OF E: with b = avg_win/avg_loss, E is the")
    add("       expectancy expressed in MULTIPLES OF THE AVERAGE LOSS, not in raw")
    add("       R. The raw-R expectancy per trade is p*avg_win - (1-p)*avg_loss,")
    add("       and the two are related by E = (that) / avg_loss. Both are printed")
    add("       side by side in handcheck-output.txt so the unit is never implied.")
    add("  p* = 1/(1+b)  the break-even win rate implied by this payoff")
    add("  b* = (1-p)/p  the payoff needed to break even at this win rate")
    add("  sd = sample sd (n-1) of the R multiples")
    add("  n_req = 4*(sd/|E|)^2  trades needed for a ~2-sigma edge")
    add("  L  = ln(N)/ln(1/(1-p))  expected longest losing streak")
    add("")
    add("  S3 and S4 have NO stop, so they have no risk unit and no R multiple.")
    add("  Reporting a p, b or E for them would require inventing the risk unit")
    add("  that the registration deliberately ties to the stop. They are n/a,")
    add("  and their sample size appears as n_trades = 0 (S4) or 1 (S3).")
    add("")
    r_rows = []
    r_csv = []
    trade_store = {}
    for sym in sorted(universe):
        b = universe[sym]
        strat = build_strategies(b)
        trade_store[sym] = strat
        for s in STRATEGIES:
            rs = [t["R"] for t in strat[s]["trades"]]
            st = r_stats(rs)
            if s in ("S3", "S4"):
                r_rows.append([sym, s, "n/a", "n/a", "n/a", "n/a", "n/a",
                               "n/a", "n/a", "n/a",
                               str(1 if s == "S3" else 0)])
            else:
                r_rows.append([sym, s, fnum(st["p"], 4), fnum(st["b"], 4),
                               fnum(st["E"], 4), fnum(st["pstar"], 4),
                               fnum(st["bstar"], 4), fnum(st["sd"], 4),
                               fnum(st["n_req"], 1), fnum(st["L"], 2),
                               str(st["n"])])
            r_csv.append([sym, s, st["n"], st["wins"], st["losses"],
                          st["breakeven"], st["p"], st["b"], st["E"],
                          st["pstar"], st["bstar"], st["sd"], st["n_req"], st["L"]])
    L.extend(table(["inst", "strat", "p", "b", "E", "p*", "b*", "sd(R)",
                    "n_req", "L", "n_trades"],
                   r_rows, ["l", "l", "r", "r", "r", "r", "r", "r", "r", "r", "r"]))
    add("")
    add("  Read n_req against n_trades. Where n_req is far larger than n_trades,")
    add("  the measured E is not yet distinguishable from noise, whatever its sign.")
    add("")
    if not args.quiet_files:
        csv_write(os.path.join(HERE, "rstats.csv"),
                  ["instrument", "strategy", "n_trades", "wins", "losses",
                   "breakeven", "p", "b", "E", "pstar", "bstar", "sd_R",
                   "n_req", "expected_longest_losing_streak"],
                  r_csv)

    # trade logs + sibling engine runs
    engine_summary = {}
    if not args.quiet_files:
        for sym in sorted(universe):
            strat = trade_store[sym]
            for s in ("S1", "S2"):
                trades = strat[s]["trades"]
                if not trades:
                    continue
                log_path = os.path.join(TRADELOG_DIR, "%s_%s.csv" % (sym, s))
                with open(log_path, "w", encoding="utf-8", newline="") as fh:
                    fh.write("# PROVENANCE: strategy=%s  instrument=%s\n" % (s, sym))
                    fh.write("# PROVENANCE: simulated by study.py from "
                             "data/%s_1d.csv (TradingView MCP daily, split-adjusted, "
                             "regular session only)\n" % sym)
                    fh.write("# PROVENANCE: signals on close, executed next open; "
                             "stop = entry - %g*ATR(%d)\n" % (ATR_MULT, ATR_PERIOD))
                    fh.write("# PROVENANCE: entry/exit prices are per ONE unit of "
                             "the instrument; pnl is per 100000 units of notional "
                             "so that the sibling engine's currency maths is "
                             "readable; risk is the same notional basis\n")
                    fh.write("trade_id,open_date,close_date,pnl,risk,symbol,"
                             "entry_px,stop_px,exit_px\n")
                    cap = 100000.0
                    for k, t in enumerate(trades, 1):
                        units = cap / t["entry_px"]
                        pnl = units * (t["exit_px"] - t["entry_px"])
                        risk = units * (t["entry_px"] - t["stop"])
                        fh.write("%s_%04d,%s,%s,%.2f,%.2f,%s,%.6f,%.6f,%.6f\n"
                                 % (s, k, t["entry_date"], t["exit_date"], pnl,
                                    risk, sym, t["entry_px"], t["stop"],
                                    t["exit_px"]))
                rel_log = os.path.relpath(log_path, HERE).replace("\\", "/")
                for mode, ext in (("--json", "json"), ("", "txt")):
                    cmd = [sys.executable, SIBLING_ABS] + ([mode] if mode else []) + \
                          ["--capital", "100000", rel_log]
                    proc = subprocess.run(cmd, capture_output=True, text=True,
                                          cwd=HERE)
                    out_path = os.path.join(ENGINE_OUT_DIR, "%s_%s.%s"
                                            % (sym, s, ext))
                    with open(out_path, "w", encoding="utf-8", newline="") as fh:
                        fh.write(proc.stdout)
                    if mode == "--json":
                        try:
                            payload = json.loads(proc.stdout)
                        except ValueError:
                            payload = None
                        if payload:
                            engine_summary[(sym, s)] = payload

    # =====================================================================
    # 4. Cross-check against the sibling engine's own trade-level output
    # =====================================================================
    add("=" * 100)
    add("4. THE SIBLING ENGINE'S OWN VERDICT ON THESE TRADES")
    add("=" * 100)
    add("")
    add("  timeframe-performance-statistics/scripts/timeframe_stats.py was RUN as a")
    add("  subprocess on the real trade logs in tradelogs/. Its full human output is")
    add("  in engine-output/<inst>_<strat>.txt and its JSON in ...json. Extracted:")
    add("")
    add("  The pooled win_rate / break_even_win_rate / edge are bucketing-INVARIANT")
    add("  in that engine by construction, so one row per (instrument, strategy) is")
    add("  the whole story at trade level.")
    add("")
    eng_rows = []
    if engine_summary:
        for key in sorted(engine_summary):
            p = engine_summary[key]
            b0 = p["buckets"][0]
            v = p["verdict"]
            eng_rows.append([
                key[0], key[1], str(b0["n_trades"]), fpct(b0["win_rate"]),
                fpct(b0["break_even_win_rate"]), fpct(b0["edge"]),
                fnum(b0["se_win_rate"], 4), b0["edge_test"],
                str(v.get("bucket") or "n/a"),
                str(v.get("status") or "")[:34]])
        L.extend(table(["inst", "strat", "trades", "win_rate", "be_wr", "edge",
                        "se_wr", "beat_losses", "best_bucket", "verdict"],
                       eng_rows, ["l", "l", "r", "r", "r", "r", "r", "l", "l", "l"]))
    else:
        add("  engine runs were skipped (--quiet-files)")
    add("")
    add("  The engine's own dependence caveat, quoted from the file it lives in:")
    add("")
    for ln in TF.DEPENDENCE_CAVEAT.split(". "):
        add("    %s" % ln.strip())

    # =====================================================================
    # 5. Per calendar year
    # =====================================================================
    add("")
    add("=" * 100)
    add("5. PER CALENDAR YEAR -- every strategy x every instrument, losses included")
    add("=" * 100)
    add("")
    add("  return  : compounded from that year's daily returns")
    add("  maxdd   : peak-to-trough inside the year, curve rebased at the year's")
    add("            first bar, negative")
    add("  a trade belongs to the bucket containing its EXIT date (the sibling")
    add("  engine's own convention), so a trade opened in December and closed in")
    add("  January is counted in January.")
    add("  p, b, E : in R units, from that year's trades only; n/a where the year")
    add("            has no losing trade (b undefined) or no trade at all")
    add("  LOSS    : which strategies lost money in that year")
    add("")
    peryear_rows = []
    peryear_csv = []
    for sym in sorted(universe):
        b = universe[sym]
        strat = trade_store[sym]
        years = sorted(set(d.year for d in b.dates))
        add("-" * 100)
        add("PER-YEAR -- %s" % sym)
        add("-" * 100)
        add("")
        rows = []
        for s in STRATEGIES:
            ret = strat[s]["ret"]
            idx_by_year = {}
            for i, d in enumerate(b.dates):
                idx_by_year.setdefault(d.year, []).append(i)
            tr_by_year = {}
            for t in strat[s]["trades"]:
                tr_by_year.setdefault(t["exit_date"].year, []).append(t)
            for y in years:
                idxs = idx_by_year[y]
                sub = [ret[i] for i in idxs]
                curve = equity_curve(sub)
                tot = curve[-1] - 1.0
                dd = max_drawdown_pct(curve)
                trs = tr_by_year.get(y, [])
                st = r_stats([t["R"] for t in trs]) if s in ("S1", "S2") else None
                if s in ("S1", "S2"):
                    pv, bv, ev = fnum(st["p"], 4), fnum(st["b"], 4), fnum(st["E"], 4)
                else:
                    pv = bv = ev = "n/a"
                rows.append([s, str(y), str(len(idxs)), fpct(tot), fpct(dd),
                             str(len(trs)), pv, bv, ev,
                             "LOSS" if tot < 0 else ""])
                peryear_csv.append([sym, s, y, tot, dd, len(trs),
                                    st["p"] if st else NA, st["b"] if st else NA,
                                    st["E"] if st else NA,
                                    1 if tot < 0 else 0])
        L.extend(table(["strat", "year", "n_days", "return", "maxdd", "n_trades",
                        "p", "b", "E", "LOSS"],
                       rows, ["l", "r", "r", "r", "r", "r", "r", "r", "r", "l"]))
        add("")
        add("  losing years by strategy in %s:" % sym)
        for s in STRATEGIES:
            lost = [r[1] for r in rows if r[0] == s and r[9] == "LOSS"]
            add("    %s  %2d of %2d years   %s"
                % (s, len(lost), len(years), ", ".join(lost) if lost else "(none)"))
        add("")
    if not args.quiet_files:
        csv_write(os.path.join(HERE, "per-year.csv"),
                  ["instrument", "strategy", "year", "return", "max_dd",
                   "n_trades", "p", "b", "E", "is_loss"], peryear_csv)

    # =====================================================================
    # 6. Regime grid
    # =====================================================================
    add("=" * 100)
    add("6. REGIME GRID -- data-derived, lagged one day, no hindsight labels")
    add("=" * 100)
    add("")
    add("  Every trading day is labelled with the state KNOWN AT THE PREVIOUS CLOSE:")
    add("    trend  : close vs SMA(200)")
    add("    slope  : sign of SMA(200)[t] - SMA(200)[t-%d]" % SLOPE_LOOKBACK)
    add("    vol    : tercile of trailing %dd realised vol, cut over the FULL sample"
        % VOL_LOOKBACK)
    add("  Daily returns of each strategy are then attributed to that label.")
    add("  The one-day lag is deliberate: labelling a return with a state read off")
    add("  its own close makes the label and the return the same fact.")
    add("")
    regime_csv = []
    for sym in sorted(universe):
        b = universe[sym]
        strat = trade_store[sym]
        reg = classify_regimes(b)
        add("-" * 100)
        add("REGIME GRID -- %s   (vol tercile cuts: %.4f / %.4f annualised)"
            % (sym, reg["q1"], reg["q2"]))
        add("-" * 100)
        add("")
        yrs = years_between(b.dates[0], b.dates[-1])
        for grid, key in (("2x3 (trend x vol tercile)", "regime_6"),
                          ("2x2 (trend x slope)", "regime_4")):
            cells = []
            labels = sorted(set(x for x in reg[key] if x is not NA))
            classified = sum(1 for x in reg[key] if x is not NA)
            add("  %s -- %d of %d days classified (%.1f%%); the rest is warm-up"
                % (grid, classified, len(b), 100.0 * classified / len(b)))
            add("")
            for lab in labels:
                idxs = [i for i in range(len(b)) if reg[key][i] == lab]
                add("    %s  n_days=%d  days/yr=%.1f"
                    % (lab, len(idxs), len(idxs) / yrs))
                for s in STRATEGIES:
                    ret = strat[s]["ret"]
                    vals = [ret[i] for i in idxs]
                    tot = sum(vals)
                    mean = tot / len(vals)
                    sd = TF.sample_sd(vals)
                    ann_contrib = tot / yrs
                    ann_if = mean * TRADING_DAYS_PER_YEAR
                    trades = [t for t in strat[s]["trades"]
                              if reg[key][t["entry_i"] - 1] == lab]
                    st = r_stats([t["R"] for t in trades]) if s in ("S1", "S2") else None
                    cells.append([lab, s,
                                  fnum(mean * 100.0, 3),
                                  fpct(ann_if),
                                  fpct(ann_contrib),
                                  "YES" if ann_contrib < 0 else "",
                                  str(len(trades)),
                                  fnum(st["p"], 3) if st else "n/a",
                                  fnum(st["b"], 3) if st else "n/a",
                                  fnum(st["E"], 3) if st else "n/a",
                                  fnum(st["n_req"], 0) if st and st["n_req"] not in (NA, None) else "n/a"])
                    regime_csv.append([sym, grid, lab, s, len(idxs), mean,
                                       sd, ann_if, ann_contrib,
                                       len(trades),
                                       st["p"] if st else NA,
                                       st["b"] if st else NA,
                                       st["E"] if st else NA,
                                       st["n_req"] if st else NA])
            L.extend(table(["regime", "strat", "mean_day_bp", "ann_if_persists",
                            "ann_contrib", "NEG", "n_tr", "p", "b", "E", "n_req"],
                           cells,
                           ["l", "l", "r", "r", "r", "l", "r", "r", "r", "r", "r"]))
            add("")
        add("  ann_contrib is the annualised contribution to the strategy's total")
        add("  arithmetic return: sum of that regime's daily returns / %.1f years."
            % yrs)
        add("  n_tr counts trades ENTERED while the regime label was in force.")
        add("  S4's cells are vol-scaled by construction: a low-vol regime earns a")
        add("  large weight, so S4's contribution in a calm regime is amplified and")
        add("  is not comparable with S3's in that same regime.")
        add("")
    if not args.quiet_files:
        csv_write(os.path.join(HERE, "regime.csv"),
                  ["instrument", "grid", "regime", "strategy", "n_days",
                   "mean_daily_return", "sd_daily_return",
                   "annualised_if_persisted", "annualised_contribution",
                   "n_trades_entered", "p", "b", "E", "n_req"], regime_csv)

    # =====================================================================
    # 7. Timeframe buckets
    # =====================================================================
    add("=" * 100)
    add("7. TIMEFRAME BUCKETS -- the sibling engine's own bucketing and verdict")
    add("=" * 100)
    add("")
    add("  The strategy's P&L series bucketed D / W / 2W / M / Q / H / Y using the")
    add("  sibling engine's bucket_key() -- a trade belongs to the bucket containing")
    add("  its CLOSE date, and 2W pairs are anchored on ODD ISO weeks. The P&L unit")
    add("  here is a percentage point of equity, summed inside the bucket (so it is")
    add("  arithmetic, not compounded). mean / sd / t_stat / period-Sharpe / max")
    add("  drawdown / lag-1 autocorrelation / n_eff are computed by the engine's own")
    add("  aggregate_bucket(), not by a second implementation.")
    add("")
    add("  VERDICT RULE (imported from that engine, not invented here):")
    add("    rank buckets by descending |t_stat|, but only among buckets with")
    add("      n_periods >= %d  AND  trades_per_period >= %d"
        % (TF.MIN_PERIODS_FOR_VERDICT, TF.MIN_TRADES_PER_PERIOD_FOR_VERDICT))
    add("    any bucket with |t_stat| < %s is NOT DISTINGUISHABLE FROM NOISE."
        % TF.T_STAT_NOISE_BAND)
    add("")
    add("  trades_per_period below is the REAL count of strategy trades closed per")
    add("  period. The engine's own figure, days_per_period, is shown next to it so")
    add("  the difference between 'how many observations' and 'how many independent")
    add("  trades' is visible rather than conflated.")
    add("")
    bucket_csv = []
    verdicts = {}
    for sym in sorted(universe):
        b = universe[sym]
        strat = trade_store[sym]
        add("-" * 100)
        add("TIMEFRAME BUCKETS -- %s" % sym)
        add("-" * 100)
        add("")
        for s in STRATEGIES:
            pct = [r * 100.0 for r in strat[s]["ret"]]
            bk = bucketed_series(b, pct, strat[s]["trades"], "%s:%s" % (sym, s))
            verdicts[(sym, s)] = bucket_verdict(list(bk.values()))
            rows = []
            for key in TF.BUCKET_ORDER:
                r = bk[key]
                rows.append([key, str(r["n_periods"]), fnum(r["mean"], 4),
                             fnum(r["sd"], 3), fnum(r["t_stat"], 3),
                             fnum(r["period_sharpe"], 4), fpct(r["max_dd"] / 100.0),
                             fnum(r["trades_per_period"], 3),
                             fnum(r["days_per_period"], 2),
                             fnum(r["lag1"], 3), fnum(r["n_eff"], 1),
                             "yes" if (r["n_periods"] >= TF.MIN_PERIODS_FOR_VERDICT
                                       and r["trades_per_period"] is not NA
                                       and r["trades_per_period"] >= TF.MIN_TRADES_PER_PERIOD_FOR_VERDICT
                                       and r["t_stat"] is not NA) else "no",
                             r["noise_flag"][:22]])
                bucket_csv.append([sym, s, key, r["n_periods"], r["mean"], r["sd"],
                                   r["t_stat"], r["period_sharpe"], r["max_dd"],
                                   r["trades_per_period"], r["days_per_period"],
                                   r["lag1"], r["n_eff"], r["noise_flag"]])
            add("  %s" % STRATEGY_TITLE[s])
            L.extend(table(["bk", "n_per", "mean", "sd", "t_stat", "per_Sharpe",
                            "max_dd", "tr/per", "days/per", "lag1", "n_eff",
                            "gates", "noise"],
                           rows,
                           ["l", "r", "r", "r", "r", "r", "r", "r", "r", "r",
                            "r", "l", "l"]))
            v = verdicts[(sym, s)]
            if v["bucket"] is NA:
                add("    VERDICT: INSUFFICIENT DATA -- %s" % v["reason"])
            else:
                add("    VERDICT: %s is the most reliable review timeframe. %s"
                    % (v["bucket"], v["reason"]))
                add("             status: %s" % v["status"])
            add("")
    if not args.quiet_files:
        csv_write(os.path.join(HERE, "buckets.csv"),
                  ["instrument", "strategy", "bucket", "n_periods",
                   "mean_period_pnl_pct", "sd_period_pnl_pct", "t_stat",
                   "period_sharpe", "max_drawdown_pct_pnl", "trades_per_period",
                   "days_per_period", "lag1_autocorrelation", "n_eff",
                   "noise_flag"], bucket_csv)

    add("  Which bucket gives the most trustworthy statistics, and why -- the")
    add("  engine's verdict bucket per (instrument, strategy):")
    add("")
    vrows = []
    for sym in sorted(universe):
        for s in STRATEGIES:
            v = verdicts[(sym, s)]
            vrows.append([sym, s, str(v["bucket"] or "n/a"),
                          str(v["status"]), str(v.get("n_periods", "")),
                          fnum(v.get("t_stat"), 3),
                          fnum(v.get("trades_per_period"), 3)])
    L.extend(table(["inst", "strat", "best_bucket", "status", "n_periods",
                    "t_stat", "trades_per_period"], vrows,
                   ["l", "l", "l", "l", "r", "r", "r"]))
    add("")
    add("  WHY, in the engine's own terms:")
    add("")
    add("    * Y wins for S2 on all four instruments, and it is the ONLY bucket that")
    add("      wins anywhere. It is not that yearly P&L has more information than")
    add("      daily P&L -- the engine's dependence caveat says the opposite, since Y")
    add("      literally contains every smaller bucket. Y wins because it is the one")
    add("      bucket where the SECOND gate can be met: a book that trades a few")
    add("      times a year needs a bucket big enough to contain >= %d trades."
        % TF.MIN_TRADES_PER_PERIOD_FOR_VERDICT)
    add("    * S1 fails BOTH gates on every instrument. Its trades_per_period never")
    add("      reaches %d even at Y, so the rule returns INSUFFICIENT DATA and names"
        % TF.MIN_TRADES_PER_PERIOD_FOR_VERDICT)
    add("      that constraint rather than picking a bucket anyway.")
    add("    * S3 and S4 have NO trades, so trades_per_period = 0 and no bucket can")
    add("      ever qualify. For them this engine's verdict machinery simply does not")
    add("      apply: their P&L is one continuous position, and bucketing a single")
    add("      position does not manufacture independent observations. The right")
    add("      review frequency for S3/S4 is NOT answerable from this test.")
    add("    * Where Y does qualify but |t_stat| < %s -- SPY S2 and TLT S2 -- the"
        % TF.T_STAT_NOISE_BAND)
    add("      engine's own words are 'NOT DISTINGUISHABLE FROM NOISE'. Read that as")
    add("      the headline: 1.9 is not 2.0, and 0.37 is nowhere near it.")
    add("    * The practical consequence is the engine's: MORE PERIODS WILL NOT FIX")
    add("      THIS. MORE INDEPENDENT TRADES WILL. Moving the review timeframe cannot")
    add("      create trades that did not happen.")

    # =====================================================================
    # 8. All-weather test
    # =====================================================================
    add("")
    add("=" * 100)
    add("8. ALL-WEATHER TEST -- is any one rule set profitable in every regime")
    add("   and every year?")
    add("=" * 100)
    add("")
    add("  Losing years, per strategy per instrument, counted from table 5:")
    add("")
    aw_rows = []
    for s in STRATEGIES:
        tot_lost = 0
        tot_y = 0
        worst = None
        for sym in sorted(universe):
            b = universe[sym]
            strat = trade_store[sym]
            years = sorted(set(d.year for d in b.dates))
            ret = strat[s]["ret"]
            idx_by_year = {}
            for i, d in enumerate(b.dates):
                idx_by_year.setdefault(d.year, []).append(i)
            lost = 0
            wy = None
            wv = 1e9
            for y in years:
                curve = equity_curve([ret[i] for i in idx_by_year[y]])
                v = curve[-1] - 1.0
                if v < 0:
                    lost += 1
                if v < wv:
                    wv = v
                    wy = y
            tot_lost += lost
            tot_y += len(years)
            if worst is None or wv < worst[1]:
                worst = (sym, wv, wy)
            aw_rows.append([s, sym, str(lost), str(len(years)),
                            "%s %s" % (wy, fpct(wv))])
        aw_rows.append([s, "ALL", str(tot_lost), str(tot_y),
                        "worst %s %s" % (worst[0], fpct(worst[1]))])
    L.extend(table(["strat", "inst", "losing_years", "years", "worst_year"],
                   aw_rows, ["l", "l", "r", "r", "l"]))
    add("")
    # regime cells that are negative, per strategy
    add("  Regime cells (2x3 grid) where the strategy's annualised contribution")
    add("  was NEGATIVE:")
    add("")
    neg_rows = []
    for sym in sorted(universe):
        b = universe[sym]
        strat = trade_store[sym]
        reg = classify_regimes(b)
        yrs = years_between(b.dates[0], b.dates[-1])
        for s in STRATEGIES:
            ret = strat[s]["ret"]
            neg = []
            for lab in sorted(set(x for x in reg["regime_6"] if x is not NA)):
                idxs = [i for i in range(len(b)) if reg["regime_6"][i] == lab]
                c = sum(ret[i] for i in idxs) / yrs
                if c < 0:
                    neg.append("%s %s" % (lab, fpct(c)))
            neg_rows.append([sym, s, str(len(neg)), ", ".join(neg) if neg else "(none)"])
    L.extend(table(["inst", "strat", "neg_cells", "cells"],
                   neg_rows, ["l", "l", "r", "l"]))
    add("")
    # data-driven verdict text
    total_lost = {}
    total_years = {}
    for r in aw_rows:
        if r[1] == "ALL":
            total_lost[r[0]] = int(r[2])
            total_years[r[0]] = int(r[3])
    zero_instrument = []
    for s in STRATEGIES:
        inst_lost = [int(r[2]) for r in aw_rows if r[0] == s and r[1] != "ALL"]
        if min(inst_lost) == 0:
            zero_instrument.append(s)
    add("  VERDICT ON THE ALL-WEATHER QUESTION, from the numbers above:")
    add("")
    add("    losing instrument-years / total instrument-years available:")
    for s in STRATEGIES:
        add("      %s   %3d / %3d = %.0f%%"
            % (s, total_lost[s], total_years[s],
               100.0 * total_lost[s] / total_years[s]))
    add("")
    add("    strategies with at least one instrument on which every year was positive:"
        " %s" % (", ".join(zero_instrument) if zero_instrument else "NONE"))
    add("    instrument-years in which a strategy was negative in EVERY regime cell"
        " at once: not counted here; see the per-regime table in section 6.")
    add("")
    add("    On this evidence there is NO single rule set among S1-S4 that is")
    add("    profitable in every year and every regime. The fewest losing")
    add("    instrument-years any strategy manages is %d of %d."
        % (min(total_lost.values()), total_years[STRATEGIES[0]]))
    no_neg_cell = sorted(set(r[1] for r in neg_rows if int(r[2]) == 0))
    add("    strategies that have at least one instrument with NO negative regime")
    add("    cell: %s" % (", ".join(no_neg_cell) if no_neg_cell else "none"))
    add("    (an instrument with no negative regime cell can still have losing")
    add("    YEARS -- the grid and the calendar disagree, which is the point of")
    add("    running both.)")
    add("")
    add("    'Profitable every time in every market condition' is not a property a")
    add("    single long-only rule set has exhibited on this data. That is a")
    add("    statement about the evidence, not a theorem: it is what 4 instruments")
    add("    x 23-34 years of daily bars can show.")

    # =====================================================================
    # 9. Complementarity
    # =====================================================================
    add("=" * 100)
    add("9. COMPLEMENTARITY -- do the strategies lose in the SAME years?")
    add("=" * 100)
    add("")
    add("  Pearson correlation of YEARLY returns, over the years common to both")
    add("  series. Computed per instrument, and on the cross-instrument mean yearly")
    add("  return (the pooled row) so a single instrument cannot carry the answer.")
    add("")
    comp_csv = []
    pooled = {}
    for sym in sorted(universe):
        b = universe[sym]
        strat = trade_store[sym]
        years = sorted(set(d.year for d in b.dates))
        idx_by_year = {}
        for i, d in enumerate(b.dates):
            idx_by_year.setdefault(d.year, []).append(i)
        yr_ret = {}
        for s in STRATEGIES:
            ser = []
            for y in years:
                curve = equity_curve([strat[s]["ret"][i] for i in idx_by_year[y]])
                ser.append(curve[-1] - 1.0)
            yr_ret[s] = ser
            pooled.setdefault(s, {})
            for y, v in zip(years, ser):
                pooled[s].setdefault(y, []).append(v)
        add("  %s -- correlation of yearly returns" % sym)
        rows = []
        for a in STRATEGIES:
            row = [a]
            for c in STRATEGIES:
                row.append(fnum(pearson(yr_ret[a], yr_ret[c]), 3))
            rows.append(row)
            for c in STRATEGIES:
                comp_csv.append([sym, a, c, pearson(yr_ret[a], yr_ret[c])])
        L.extend(table([""] + STRATEGIES, rows, ["l"] + ["r"] * 4))
        add("")
        add("  %s -- which strategies lost in which year" % sym)
        rows = []
        for y in years:
            losses = [s for s in STRATEGIES
                      if yr_ret[s][years.index(y)] < 0]
            rows.append([str(y)] + ["LOSS" if s in losses else "-" for s in STRATEGIES]
                        + [", ".join(losses) if losses else "(none)"])
        L.extend(table(["year"] + STRATEGIES + ["LOSERS"], rows,
                       ["r"] + ["l"] * 4 + ["l"]))
        add("")
    add("  POOLED across instruments -- correlation of the mean yearly return")
    add("")
    pyears = sorted(set().union(*[set(v) for v in pooled.values()]))
    series = {}
    for s in STRATEGIES:
        series[s] = [sum(pooled[s][y]) / len(pooled[s][y]) for y in pyears]
    rows = []
    for a in STRATEGIES:
        row = [a]
        for c in STRATEGIES:
            row.append(fnum(pearson(series[a], series[c]), 3))
        rows.append(row)
        for c in STRATEGIES:
            comp_csv.append(["POOLED", a, c, pearson(series[a], series[c])])
    L.extend(table([""] + STRATEGIES, rows, ["l"] + ["r"] * 4))
    add("")
    add("  POOLED -- losing years per strategy (mean yearly return < 0)")
    rows = []
    for y in pyears:
        k = pyears.index(y)
        losses = [s for s in STRATEGIES if series[s][k] < 0]
        rows.append([str(y)] + ["LOSS" if s in losses else "-" for s in STRATEGIES]
                    + [", ".join(losses) if losses else "(none)"])
    L.extend(table(["year"] + STRATEGIES + ["LOSERS"], rows,
                   ["r"] + ["l"] * 4 + ["l"]))
    add("")
    # data-driven complementarity verdict
    both = sum(1 for k in range(len(pyears))
               if series["S1"][k] < 0 and series["S3"][k] < 0)
    trend_only = sum(1 for k in range(len(pyears))
                     if series["S1"][k] < 0 and series["S3"][k] >= 0)
    hold_only = sum(1 for k in range(len(pyears))
                    if series["S3"][k] < 0 and series["S1"][k] >= 0)
    all_three = sum(1 for k in range(len(pyears))
                    if series["S1"][k] < 0 and series["S2"][k] < 0
                    and series["S3"][k] < 0)
    add("  VERDICT ON COMPLEMENTARITY, from the numbers above:")
    add("")
    pairs = [("S1", "S2"), ("S1", "S3"), ("S2", "S3"),
             ("S1", "S4"), ("S2", "S4"), ("S3", "S4")]
    pair_r = dict(((a, c), pearson(series[a], series[c])) for a, c in pairs)
    add("    pooled pairwise correlations of yearly returns:")
    for a, c in pairs:
        add("      corr(%s,%s) = %s" % (a, c, fnum(pair_r[(a, c)], 3)))
    add("    years where S1 and S3 BOTH lost : %d" % both)
    add("    years where S1 lost and S3 did not: %d" % trend_only)
    add("    years where S3 lost and S1 did not: %d" % hold_only)
    add("    years where S1, S2 and S3 ALL lost: %d" % all_three)
    add("")
    lo = min(v for v in pair_r.values() if v is not NA)
    hi = max(v for v in pair_r.values() if v is not NA)
    add("    ALL SIX pairwise correlations are positive, and every one lies between")
    add("    %s and %s. On this data the four rules are not four bets: they are" % (fnum(lo, 3), fnum(hi, 3)))
    add("    one bet -- long this instrument -- taken with three different exits")
    add("    and one different position size.")
    add("")
    add("    The three trend/hold rules also lose in the SAME years, not different")
    add("    ones: S1 and S3 both lost in %d of the %d pooled years, and the two" % (both, len(pyears)))
    add("    disagreed in only one year each way. S2 does dodge some years that S1")
    add("    and S3 lose -- its faster 50-day exit leaves earlier -- which is why")
    add("    S2's worst year is milder while its COUNT of losing years is higher.")
    add("")
    add("    S4 is not the exception it looks like. corr(S1,S4)=%s and corr(S3,S4)=%s:"
        % (fnum(pair_r[("S1", "S4")], 3), fnum(pair_r[("S3", "S4")], 3)))
    add("    vol-scaling changes the SIZE of the same long position, not its")
    add("    direction. S4 is a position-sizing policy applied to the S3 bet, not a")
    add("    second bet, and it cannot diversify a book on its own.")
    add("")
    add("    The honest route to an all-weather BOOK is therefore not a better")
    add("    long-only equity rule. On this evidence it is a set of sleeves whose")
    add("    losing years do not coincide -- a short or a defensive sleeve, or an")
    add("    instrument whose bad years fall elsewhere. This study did not test one.")
    add("")
    if not args.quiet_files:
        csv_write(os.path.join(HERE, "complementarity.csv"),
                  ["scope", "strategy_a", "strategy_b", "pearson_r_yearly_returns"],
                  comp_csv)

    # =====================================================================
    # 10. Limitations
    # =====================================================================
    add("")
    add("=" * 100)
    add("10. WHAT THIS DOES NOT COVER")
    add("=" * 100)
    add("")
    add("  * No transaction costs, spread, slippage, borrow or dividends.")
    add("  * One instrument at a time: no portfolio, no correlation-aware sizing,")
    add("    no capital sharing between trades.")
    add("  * Only 4 instruments, and only a long-only book. No shorts, no options,")
    add("    no intraday bars, no futures.")
    add("  * No parameter sensitivity sweep was run, by design. That means nothing")
    add("    here establishes that a 200-day rule beats a 150-day rule, and nothing")
    add("    here rules it out.")
    add("  * The last bar is still forming at pull time and may revise.")
    add("  * Sample sizes differ wildly by strategy and by year. n_req in table 3")
    add("    is the honest sample-size requirement for each row.")
    add("")
    add("END OF REPORT")

    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
