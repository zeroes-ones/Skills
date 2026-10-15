#!/usr/bin/env python3
"""study.py - mean-reversion and volatility study on real daily prices.

Stdlib only. Deterministic: no randomness, no wall-clock, no dict-order
dependence, LF output.  Run it twice and diff stdout - it must be identical.

Data: ./data/*.csv, produced by pull_data.py (see its docstring for sources).
Run:  py -3 study.py                 # full report to stdout + tables to ./out/
      py -3 study.py --dump-trades M1:SPY:2020   # one strategy-year's trade list,
                                                 # for hand-checking the metrics
      py -3 study.py --no-tables       # stdout only

WHAT IS PRE-REGISTERED (run once, reported as-is, no iteration)
---------------------------------------------------------------
Long-only, one position at a time.  Signal is read on the close of day t,
entry is the OPEN of day t+1, stop distance is 1 unit of risk R:
  M1 Connors mean reversion : buy when RSI(2) < 10 and close > SMA(200);
                              exit when close > SMA(5) or after 5 trading days;
                              stop = 2 x ATR(14).
  M2 Bollinger reversion    : buy when close < lower Bollinger(20, 2) and
                              close > SMA(200); exit at SMA(20) or after 10
                              days; stop = 2 x ATR(14).
  M3 Dip in an uptrend      : buy when close is >= 5% below its 20-day high and
                              SMA(50) > SMA(200); exit when close makes a new
                              20-day high; stop = 2 x ATR(14).

SIZING / ACCOUNTING CONVENTIONS (fixed, not searched)
  risk_per_share = entry - stop, computed from ATR on the SIGNAL day t (the
  value a trader could actually read before entering).
  R-multiple     = (exit_price - entry_price) / risk_per_share.
  Equity curve   = 1% of equity risked per trade, marked to market daily; the
  daily R is telescoped so it sums to the trade's total R.
  Costs          = ZERO.  No commission, no slippage, no borrow.  This makes
  every figure optimistic and is restated in FINDINGS.md.
  A trade still open at the last bar is closed there and EXCLUDED from trade
  statistics (counted separately) because its outcome is not yet known.

THE VOL-PREMIUM PROXY IS A PROXY (stated here as well as in FINDINGS.md)
  VIX is a 30-day constant-maturity implied-vol index on the S&P 500.  It is
  NOT the implied vol of any particular instrument, and a 21-day realised move
  in the underlying is NOT the P&L of a short option position (which is
  path-dependent, carries gamma/theta, and settles at the option's own strike
  structure).  No options IV history is available here, so the proxy is the
  best available stand-in and its limits are restated wherever it is reported.
"""
import argparse
import csv
import io
import math
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "out")

TRADING_DAYS = 252
FAIR_ABS_FACTOR = math.sqrt(2.0 / math.pi)   # E|Z| for a standard normal
RISK_FRACTION = 0.01     # 1% of equity risked per trade
VOL_WINDOW = 21          # forward horizon for the vol-premium proxy, in sessions

SYMBOLS = ["SPY", "QQQ", "IWM", "EEM"]
STRATEGIES = ["M1", "M2", "M3"]


# ============================================================ helpers ======

def load_series(symbol):
    """-> (dates, o, h, l, c, close_tr) as parallel lists."""
    path = os.path.join(DATA, "{}_1d.csv".format(symbol))
    with io.open(path, encoding="utf-8") as fh:
        lines = [l for l in fh.read().split("\n")
                 if l.strip() and not l.startswith("#")]
    dates, o, h, l, c, tr = [], [], [], [], [], []
    for r in csv.DictReader(lines):
        dates.append(r["date"])
        o.append(float(r["open"]))
        h.append(float(r["high"]))
        l.append(float(r["low"]))
        c.append(float(r["close"]))
        tr.append(float(r["close_tr"]) if r.get("close_tr") else float(r["close"]))
    return dates, o, h, l, c, tr


def sma(vals, n):
    out = [None] * len(vals)
    if len(vals) < n:
        return out
    s = sum(vals[:n])
    out[n - 1] = s / n
    for i in range(n, len(vals)):
        s += vals[i] - vals[i - n]
        out[i] = s / n
    return out


def rolling_max(vals, n):
    out = [None] * len(vals)
    for i in range(len(vals)):
        if i >= n - 1:
            out[i] = max(vals[i - n + 1:i + 1])
    return out


def rolling_sd(vals, n):
    """Population sd of the trailing n values, matching standard Bollinger use."""
    out = [None] * len(vals)
    for i in range(n - 1, len(vals)):
        w = vals[i - n + 1:i + 1]
        m = sum(w) / n
        out[i] = math.sqrt(sum((x - m) ** 2 for x in w) / n)
    return out


def rsi_wilder(closes, n):
    out = [None] * len(closes)
    if len(closes) <= n:
        return out
    g = l = 0.0
    for i in range(1, n + 1):
        ch = closes[i] - closes[i - 1]
        if ch > 0:
            g += ch
        else:
            l -= ch
    ag, al = g / n, l / n
    out[n] = 100.0 if al == 0 else 100.0 - 100.0 / (1.0 + ag / al)
    for i in range(n + 1, len(closes)):
        ch = closes[i] - closes[i - 1]
        gg = ch if ch > 0 else 0.0
        ll = -ch if ch < 0 else 0.0
        ag = (ag * (n - 1) + gg) / n
        al = (al * (n - 1) + ll) / n
        out[i] = 100.0 if al == 0 else 100.0 - 100.0 / (1.0 + ag / al)
    return out


def atr_wilder(highs, lows, closes, n):
    tr = [0.0] * len(closes)
    for i in range(len(closes)):
        if i == 0:
            tr[i] = highs[i] - lows[i]
        else:
            tr[i] = max(highs[i] - lows[i],
                        abs(highs[i] - closes[i - 1]),
                        abs(lows[i] - closes[i - 1]))
    out = [None] * len(closes)
    if len(closes) < n:
        return out
    out[n - 1] = sum(tr[:n]) / n
    for i in range(n, len(closes)):
        out[i] = (out[i - 1] * (n - 1) + tr[i]) / n
    return out


def realised_vol(closes, n):
    """Annualised sd of trailing log returns over n sessions."""
    rets = [None] * len(closes)
    for i in range(1, len(closes)):
        rets[i] = math.log(closes[i] / closes[i - 1])
    out = [None] * len(closes)
    for i in range(n, len(closes)):
        w = [r for r in rets[i - n + 1:i + 1] if r is not None]
        if len(w) < 2:
            continue
        m = sum(w) / len(w)
        var = sum((x - m) ** 2 for x in w) / (len(w) - 1)
        out[i] = math.sqrt(var) * math.sqrt(TRADING_DAYS) * 100.0
    return out


def norm_ppf(p):
    """Acklam's inverse standard-normal CDF (|abs err| < 1.15e-9)."""
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
               ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
                ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    q = p - 0.5
    r = q * q
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
           (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)


def sd_sample(xs):
    n = len(xs)
    if n < 2:
        return 0.0
    m = sum(xs) / n
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))


# ======================================================= trade engine ======

class Trade(object):
    __slots__ = ("entry_i", "exit_i", "entry_date", "exit_date", "entry_px",
                 "exit_px", "stop_px", "risk", "R", "reason", "open_flag")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


def run_strategy(dates, o, h, l, c, strat, rsi_thresh=None, max_hold=None,
                 dip_pct=0.05):
    """Simulate one pre-registered rule set.  Returns (trades, equity_daily_R).

    equity_daily_R: list of per-day R contributions (0.0 when flat), length
    len(dates); telescoping means each trade's contributions sum to its R.
    """
    n = len(c)
    s5, s20, s50, s200 = sma(c, 5), sma(c, 20), sma(c, 50), sma(c, 200)
    rsi2 = rsi_wilder(c, 2)
    atr14 = atr_wilder(h, l, c, 14)
    hi20 = rolling_max(c, 20)
    sd20 = rolling_sd(c, 20)

    # defaults per strategy
    if strat == "M1":
        rsi_thresh = 10.0 if rsi_thresh is None else rsi_thresh
        max_hold = 5 if max_hold is None else max_hold
    elif strat == "M2":
        max_hold = 10 if max_hold is None else max_hold
    elif strat == "M3":
        max_hold = None if max_hold is None else max_hold

    # signals read on the close of day t
    sig = [False] * n
    for t in range(n):
        if s200[t] is None or atr14[t] is None or atr14[t] <= 0:
            continue
        if strat == "M1":
            if rsi2[t] is None or s5[t] is None:
                continue
            sig[t] = (rsi2[t] < rsi_thresh) and (c[t] > s200[t])
        elif strat == "M2":
            if sd20[t] is None:
                continue
            lower = s20[t] - 2.0 * sd20[t]
            sig[t] = (c[t] < lower) and (c[t] > s200[t])
        elif strat == "M3":
            if s50[t] is None or hi20[t] is None:
                continue
            sig[t] = (c[t] <= hi20[t] * (1.0 - dip_pct)) and (s50[t] > s200[t])

    day_R = [0.0] * n
    trades = []
    t = 0
    while t < n - 1:
        if not sig[t]:
            t += 1
            continue

        e = t + 1                      # entry at the next open
        entry_px = o[e]
        risk = 2.0 * atr14[t]          # 2 x ATR(14) read on the signal day
        if risk <= 0 or entry_px <= 0:
            t += 1
            continue
        stop_px = entry_px - risk

        # walk forward to the exit
        j = e
        exit_px, reason, open_flag = None, None, False
        held = 0
        while j < n:
            held += 1
            if l[j] <= stop_px:
                exit_px, reason = stop_px, "stop"
                break
            if strat == "M1":
                if c[j] > s5[j]:
                    exit_px, reason = c[j], "target"
                    break
            elif strat == "M2":
                if c[j] >= s20[j]:
                    exit_px, reason = c[j], "target"
                    break
            elif strat == "M3":
                if j - 1 >= 19 and hi20[j - 1] is not None and c[j] > hi20[j - 1]:
                    exit_px, reason = c[j], "target"
                    break
            if max_hold is not None and held >= max_hold:
                exit_px, reason = c[j], "time"
                break
            j += 1
        if exit_px is None:
            # ran out of data while still holding: close at the last bar and
            # mark the trade open so it is excluded from the statistics
            j = n - 1
            exit_px, reason, open_flag = c[n - 1], "eod", True

        # telescope daily R so it sums to the trade R
        prev = entry_px
        for d in range(e, j + 1):
            mark = exit_px if d == j else c[d]
            day_R[d] += (mark - prev) / risk
            prev = mark

        trades.append(Trade(entry_i=e, exit_i=j, entry_date=dates[e],
                            exit_date=dates[j], entry_px=entry_px,
                            exit_px=exit_px, stop_px=stop_px, risk=risk,
                            R=(exit_px - entry_px) / risk, reason=reason,
                            open_flag=open_flag))
        # no pyramiding: next scan starts after this trade exits
        t = j + 1
    return trades, day_R


# =========================================================== metrics ======

def metrics(trades):
    """Trade-level statistics.  Closed trades only unless stated."""
    closed = [tr for tr in trades if not tr.open_flag]
    n = len(closed)
    if n == 0:
        return None
    Rs = [tr.R for tr in closed]
    wins = [x for x in Rs if x > 0]
    losses = [x for x in Rs if x <= 0]
    p = len(wins) / float(n)
    avg_w = (sum(wins) / len(wins)) if wins else 0.0
    avg_l = (sum(losses) / len(losses)) if losses else 0.0   # <= 0
    b = (avg_w / abs(avg_l)) if avg_l != 0 else float("inf")
    E = p * b - (1.0 - p) if avg_l != 0 else float("inf")
    p_star = 1.0 / (1.0 + b) if b != float("inf") else 0.0
    b_star = ((1.0 - p) / p) if p > 0 else float("inf")
    sd = sd_sample(Rs)
    n_req = (4.0 * (sd / abs(E)) ** 2) if E not in (0.0, float("inf")) else float("inf")

    # longest losing streak: formula and the observed value
    if p < 1.0:
        L_formula = math.log(n) / math.log(1.0 / (1.0 - p)) if n > 1 and p > 0 else float("nan")
    else:
        L_formula = 0.0
    run = best = 0
    for x in Rs:
        if x <= 0:
            run += 1
            best = max(best, run)
        else:
            run = 0
    tstat = (sum(Rs) / n) / (sd / math.sqrt(n)) if sd > 0 and n > 1 else float("nan")
    return {
        "n": n, "n_open": len(trades) - n, "p": p, "b": b, "E": E,
        "p_star": p_star, "b_star": b_star, "sd_R": sd, "n_req": n_req,
        "total_R": sum(Rs), "mean_R": sum(Rs) / n, "E_R": sum(Rs) / n,
        "E_formula": E, "avg_win_R": avg_w, "avg_loss_R": avg_l,
        "L_formula": L_formula, "L_observed": best, "t_stat": tstat,
        "avg_win_R": avg_w, "avg_loss_R": avg_l,
    }


def equity_stats(dates, day_R):
    """CAGR / max drawdown / Sharpe from the 1%-risk daily equity curve."""
    n = len(dates)
    eq = [1.0] * n
    day_ret = [0.0] * n
    for i in range(1, n):
        r = RISK_FRACTION * day_R[i]
        day_ret[i] = r
        eq[i] = eq[i - 1] * (1.0 + r)
    rets = day_ret[1:]
    m = sum(rets) / len(rets) if rets else 0.0
    s = sd_sample(rets)
    sharpe = (m / s) * math.sqrt(TRADING_DAYS) if s > 0 else float("nan")
    peak, mdd = eq[0], 0.0
    for v in eq:
        peak = max(peak, v)
        mdd = max(mdd, (peak - v) / peak)
    d0 = date(*[int(x) for x in dates[0].split("-")])
    d1 = date(*[int(x) for x in dates[-1].split("-")])
    years = (d1 - d0).days / 365.25
    cagr = (eq[-1] ** (1.0 / years) - 1.0) if years > 0 and eq[-1] > 0 else float("nan")
    return {"final_equity": eq[-1], "cagr": cagr, "max_dd": mdd,
            "sharpe": sharpe, "years": years, "days_in_market": sum(1 for r in day_ret if r != 0.0)}


def buy_hold(dates, c, tr):
    """Buy-and-hold over the same window, price-only and total-return."""
    n = len(dates)
    d0 = date(*[int(x) for x in dates[0].split("-")])
    d1 = date(*[int(x) for x in dates[-1].split("-")])
    years = (d1 - d0).days / 365.25
    cagr_px = (c[-1] / c[0]) ** (1.0 / years) - 1.0
    cagr_tr = (tr[-1] / tr[0]) ** (1.0 / years) - 1.0
    peak, mdd = c[0], 0.0
    for v in c:
        peak = max(peak, v)
        mdd = max(mdd, (peak - v) / peak)
    # daily Sharpe on the price series, so it is directly comparable with the
    # strategy Sharpe (the rules risk only 1% of equity per trade, so comparing
    # CAGR alone would flatter buy and hold on a risk-unadjusted basis)
    rets = [c[i] / c[i - 1] - 1.0 for i in range(1, len(c))]
    m = sum(rets) / len(rets)
    sd = sd_sample(rets)
    sharpe = (m / sd) * math.sqrt(TRADING_DAYS) if sd > 0 else float("nan")
    return {"cagr_px": cagr_px, "cagr_tr": cagr_tr, "max_dd": mdd,
            "sharpe": sharpe}


# ============================================================ regimes ======

def regime_labels(dates, c, h, l):
    """Per-day trend state and realised-vol tercile."""
    s200 = sma(c, 200)
    rv20 = realised_vol(c, 20)
    trend = [None] * len(c)
    for i in range(len(c)):
        if s200[i] is None:
            continue
        if i < 20 or s200[i - 20] is None:
            continue
        state = "UP" if c[i] > s200[i] else "DOWN"
        slope = "rising" if s200[i] > s200[i - 20] else "falling"
        trend[i] = "{}_{}".format(state, slope)
    vals = sorted(v for v in rv20 if v is not None)
    terc = [None] * len(c)
    t1 = t2 = None
    if vals:
        t1 = vals[len(vals) // 3]
        t2 = vals[(2 * len(vals)) // 3]
        for i in range(len(c)):
            if rv20[i] is None:
                continue
            terc[i] = "LOW" if rv20[i] <= t1 else ("MID" if rv20[i] <= t2 else "HIGH")
    return trend, terc, rv20, t1, t2


# ================================================== vol-premium proxy ======

def vol_premium(dates_spy, c_spy, vix_by_date, step=1):
    """Short-vol proxy on the S&P 500.

    Entry on day d, hold VOL_WINDOW sessions.  VIX on day d is read as the
    implied-vol proxy; the realised absolute move over the next 21 sessions is
    what the short-vol proxy 'pays'.  Risk unit R is 2x the collected premium,
    so a move beyond 3x the implied move loses more than 1R - that fat left
    tail is the whole point of the exercise.
    """
    rows = []
    n = len(dates_spy)
    for d in range(0, n - VOL_WINDOW, step):
        vix = vix_by_date.get(dates_spy[d])
        if vix is None or vix <= 0:
            continue
        collected = vix / math.sqrt(TRADING_DAYS) * math.sqrt(VOL_WINDOW)
        realised_abs = abs(c_spy[d + VOL_WINDOW] / c_spy[d] - 1.0) * 100.0
        # forward realised vol (annualised) over the same 21 sessions
        rets = [math.log(c_spy[i] / c_spy[i - 1])
                for i in range(d + 1, d + VOL_WINDOW + 1)]
        m = sum(rets) / len(rets)
        fwd_rv = math.sqrt(sum((x - m) ** 2 for x in rets) / (len(rets) - 1)) \
            * math.sqrt(TRADING_DAYS) * 100.0
        rows.append({
            "date": dates_spy[d], "d": d, "vix": vix,
            "collected": collected, "realised_abs": realised_abs,
            "payoff": collected - realised_abs,
            "R": (collected - realised_abs) / (2.0 * collected),
            # fair-strike variant: a straddle's fair value is the EXPECTED absolute
            # move, E|Z| = sqrt(2/pi) = 0.798, not the 1-sigma move.  Collecting
            # the 1-sigma move and paying the realised absolute move therefore
            # books a guaranteed ~+20% edge with no skill in it.  This variant
            # removes that artifact so the only edge left is VIX vs realised vol.
            "collected_fair": collected * FAIR_ABS_FACTOR,
            "R_fair": (collected * FAIR_ABS_FACTOR - realised_abs)
                      / (2.0 * collected * FAIR_ABS_FACTOR),
            "fwd_rv": fwd_rv, "vrp": vix - fwd_rv,
        })
    return rows


# ======================================================= table output ======

def write_table(name, header, rows):
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    path = os.path.join(OUT, name)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return len(rows)


def _num(x, fmt):
    if isinstance(x, float):
        if math.isnan(x) or math.isinf(x):
            return str(x)
        return fmt.format(x)
    return str(x)


def f1(x):
    return _num(x, "{:.1f}")


def f2(x):
    return _num(x, "{:.2f}")


def f3(x):
    return _num(x, "{:.3f}")


def pct(x):
    return _num(x, "{:.1%}")


def banner(txt):
    print("\n" + "=" * 100)
    print(txt)
    print("=" * 100)


# ============================================================== main ======

def main():
    # emit LF only: on Windows stdout would otherwise translate LF to CRLF,
    # and the captured report is meant to be byte-stable across platforms
    try:
        sys.stdout.reconfigure(newline="\n", encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--dump-trades", default=None,
                    help="STRAT:SYMBOL:YEAR - print that strategy-year's trades")
    ap.add_argument("--no-tables", action="store_true")
    args = ap.parse_args()

    series = {}
    for sym in SYMBOLS:
        series[sym] = load_series(sym)
    vd, vo, vh, vl, vc, vtr = load_series("VIX")
    vix_by_date = {vd[i]: vc[i] for i in range(len(vd))}

    # ---------------------------------------------------------- data section
    banner("1. DATA - real daily bars, sources and windows")
    print("{:<5} {:>7} {:<12} {:<12}  {}".format(
        "sym", "rows", "first", "last", "study window (needs SMA200 + 20d slope)"))
    for sym in SYMBOLS:
        d, o, h, l, c, tr = series[sym]
        warm = 220
        print("{:<5} {:>7} {:<12} {:<12}  {} -> {}  ({} sessions)".format(
            sym, len(d), d[0], d[-1], d[warm], d[-1], len(d) - warm))
    print("{:<5} {:>7} {:<12} {:<12}".format("VIX", len(vd), vd[0], vd[-1]))
    print("\nR = 2 x ATR(14) read on the signal day. Entry = next open. Long only,")
    print("one position at a time. Costs = ZERO. Open-at-end trades excluded from")
    print("trade stats. Equity curve risks 1% of equity per trade, marked daily.")

    if args.dump_trades:
        s, sym, yr = args.dump_trades.split(":")
        d, o, h, l, c, tr = series[sym]
        trades, _ = run_strategy(d, o, h, l, c, s)
        sel = [t for t in trades if t.entry_date[:4] == yr]
        banner("TRADE DUMP {} {} {} - {} closed trades".format(
            s, sym, yr, len([t for t in sel if not t.open_flag])))
        print("{:<12} {:<12} {:>9} {:>9} {:>9} {:>8} {:<7}".format(
            "entry", "exit", "entry_px", "exit_px", "stop_px", "R", "reason"))
        for t in sel:
            print("{:<12} {:<12} {:>9.3f} {:>9.3f} {:>9.3f} {:>8.3f} {:<7}".format(
                t.entry_date, t.exit_date, t.entry_px, t.exit_px, t.stop_px,
                t.R, t.reason + ("*" if t.open_flag else "")))
        Rs = [t.R for t in sel if not t.open_flag]
        print("\nR list ({}):".format(len(Rs)))
        print("  " + ", ".join("{:.4f}".format(x) for x in Rs))
        print("\n* = still open at the last bar, excluded from statistics")
        return 0

    # ------------------------------------------------- headline metrics
    banner("2. PRE-REGISTERED STRATEGIES - headline trade and equity metrics")
    print("p = win rate | b = avg-win/avg-loss")
    print("E = p*b-(1-p)  -- the pre-registered formula.  It is expectancy in units")
    print("                 of the AVERAGE LOSS, not in R: E = E_R / |avg_loss|.")
    print("                 The two coincide only when every loss is exactly -1R.")
    print("E_R = mean R   -- true expectancy per trade in R.  This is the honest one.")
    print("p* = breakeven win rate 1/(1+b) | b* = required payoff (1-p)/p (both exact)")
    print("sd = sd of R | n_req = 4*(sd/|E|)^2 trades needed for ~2 sigma")
    print("L = expected longest losing streak ln(N)/ln(1/(1-p)); Lobs = observed")
    print("CAGR/DD/Sharpe from the 1%-risk daily equity curve; Sharpe = daily")
    print("mean/sd x sqrt(252), Rf = 0, full sample as lookback.")
    print("B&H = buy and hold over the same window (price-only / total return).")
    print()

    table_rows, summary_rows, all_trades, regime_cache = [], [], {}, {}
    for sym in SYMBOLS:
        d, o, h, l, c, tr = series[sym]
        regime_cache[sym] = regime_labels(d, c, h, l)
        for strat in STRATEGIES:
            trades, dayR = run_strategy(d, o, h, l, c, strat)
            all_trades[(strat, sym)] = trades
            m = metrics(trades)
            if m is None:
                print("  {} {}: no trades".format(strat, sym))
                continue
            eq = equity_stats(d, dayR)
            bh = buy_hold(d, c, tr)
            table_rows.append([
                strat, sym, m["n"], m["n_open"], f3(m["p"]), f2(m["b"]),
                f3(m["E_formula"]), f3(m["E_R"]), f3(m["p_star"]),
                f2(m["b_star"]), f2(m["sd_R"]),
                "{:.0f}".format(m["n_req"]) if m["n_req"] != float("inf") else "inf",
                f2(m["L_formula"]), m["L_observed"], f1(m["total_R"]),
                f2(m["t_stat"]), pct(eq["cagr"]), pct(eq["max_dd"]),
                f2(eq["sharpe"]), f2(bh["sharpe"]),
            ])
            summary_rows.append({
                "strat": strat, "sym": sym, "n": m["n"], "n_open": m["n_open"],
                "p": m["p"], "b": m["b"], "E": m["E"], "p_star": m["p_star"],
                "b_star": m["b_star"], "sd_R": m["sd_R"], "n_req": m["n_req"],
                "L_formula": m["L_formula"], "L_observed": m["L_observed"],
                "total_R": m["total_R"], "t_stat": m["t_stat"],
                "E_R": m["E_R"], "E_formula": m["E_formula"],
                "avg_loss_R": m["avg_loss_R"],
                "cagr": eq["cagr"], "max_dd": eq["max_dd"], "sharpe": eq["sharpe"],
                "bh_cagr_px": bh["cagr_px"], "bh_cagr_tr": bh["cagr_tr"],
                "bh_sharpe": bh["sharpe"],
            })

    hdr = ["stra", "sym", "n", "open", "p", "b", "E_form", "E_R", "p*", "b*",
           "sd", "n_req", "L", "Lobs", "totalR", "t", "CAGR", "maxDD", "Shrp",
           "BHsh"]
    print("{:<4} {:<5} {:>5} {:>4} {:>7} {:>6} {:>7} {:>7} {:>7} {:>6} {:>6} {:>7} {:>6} {:>4} {:>8} {:>6} {:>8} {:>7} {:>6} {:>6}".format(*hdr))
    print("(Shrp = strategy Sharpe, BHsh = buy-and-hold Sharpe over the same window)")
    for r in table_rows:
        print("{:<4} {:<5} {:>5} {:>4} {:>7} {:>6} {:>7} {:>7} {:>7} {:>6} {:>6} {:>7} {:>6} {:>4} {:>8} {:>6} {:>8} {:>7} {:>6} {:>6}".format(*r))
    print("\nexposure and the risk unit - both matter for reading the CAGR comparison")
    print("{:<4} {:<5} {:>10} {:>12} {:>14} {:>16}".format(
        "stra", "sym", "days in mkt", "exposure", "median risk", "risk % of px"))
    for sym in SYMBOLS:
        d, o, h, l, c, tr = series[sym]
        _, atr14 = None, None
        a14 = atr_wilder(h, l, c, 14)
        for strat in STRATEGIES:
            trades, dayR = run_strategy(d, o, h, l, c, strat)
            eq = equity_stats(d, dayR)
            dim = eq["days_in_market"]
            risks = sorted(t.risk / t.entry_px * 100.0 for t in trades)
            med = risks[len(risks) // 2] if risks else float("nan")
            print("{:<4} {:<5} {:>10} {:>11} {:>13} {:>15}".format(
                strat, sym, dim, pct(dim / float(len(d))), f2(med) + "%",
                "1R = " + f2(med) + "%"))
    print("\nA round-trip cost of c basis points of price costs the trade")
    print("c/100/(risk% of price) in R.  With costs set to ZERO in this study, the")
    print("per-trade expectancies above are the gross, pre-cost figures.")

    print("\nbuy and hold over the same window, for reference (not traded by the rules):")
    for sym in SYMBOLS:
        d, o, h, l, c, tr = series[sym]
        bh = buy_hold(d, c, tr)
        print("  {:<4} price-only CAGR {:>7}  total-return CAGR {:>7}  max DD {:>7}  "
              "(dividend drag {:>6})".format(
                  sym, pct(bh["cagr_px"]), pct(bh["cagr_tr"]), pct(bh["max_dd"]),
                  pct(bh["cagr_tr"] - bh["cagr_px"])))
    if not args.no_tables:
        write_table("headline.csv",
                    ["strat", "sym", "n", "n_open", "p", "b", "E", "p_star",
                     "b_star", "sd_R", "n_req", "L_formula", "L_observed",
                     "total_R", "t_stat", "E_R", "avg_loss_R",
                     "cagr", "max_dd", "sharpe",
                     "bh_cagr_px", "bh_cagr_tr", "bh_sharpe"],
                    [[r["strat"], r["sym"], r["n"], r["n_open"],
                      "%.6f" % r["p"], "%.6f" % r["b"], "%.6f" % r["E"],
                      "%.6f" % r["p_star"], "%.6f" % r["b_star"],
                      "%.6f" % r["sd_R"], "%.2f" % r["n_req"],
                      "%.4f" % r["L_formula"], r["L_observed"],
                      "%.4f" % r["total_R"], "%.4f" % r["t_stat"],
                      "%.6f" % r["E_R"], "%.6f" % r["avg_loss_R"],
                      "%.6f" % r["cagr"], "%.6f" % r["max_dd"],
                      "%.4f" % r["sharpe"], "%.6f" % r["bh_cagr_px"],
                      "%.6f" % r["bh_cagr_tr"], "%.4f" % r["bh_sharpe"]]
                     for r in summary_rows])

    # ------------------------------------------------- per-year tables
    banner("3. PER-YEAR - does any rule set make money every year?")
    print("total R by entry year, with n and win rate.  '-' = no trades that year.")
    year_rows = []
    for strat in STRATEGIES:
        print("\n{}".format(strat))
        years = sorted(set(t.entry_date[:4] for sym in SYMBOLS
                           for t in all_trades[(strat, sym)] if not t.open_flag))
        print("  {:<6} {}".format("year", "  ".join("{:>16}".format(s) for s in SYMBOLS)))
        for yr in years:
            cells = []
            for sym in SYMBOLS:
                sel = [t for t in all_trades[(strat, sym)]
                       if not t.open_flag and t.entry_date[:4] == yr]
                if not sel:
                    cells.append("{:>16}".format("-"))
                    continue
                Rs = [t.R for t in sel]
                nn = len(Rs)
                pp = sum(1 for x in Rs if x > 0) / float(nn)
                mm = metrics(sel)
                cells.append("{:>16}".format("{:+.1f}R n{} p{}".format(
                    sum(Rs), nn, f2(pp))))
                year_rows.append([strat, sym, yr, nn, "%.6f" % pp,
                                  "%.6f" % mm["E"], "%.6f" % mm["b"],
                                  "%.4f" % sum(Rs)])
            print("  {:<6} {}".format(yr, "  ".join(cells)))

    banner("3b. LOSING-YEAR LEDGER - the honest count")
    print("{:<4} {:<5} {:>6} {:>7} {:>24} {:>10}".format(
        "stra", "sym", "years", "losing", "worst year (total R)", "worst R"))
    for strat in STRATEGIES:
        for sym in SYMBOLS:
            by_yr = {}
            for t in all_trades[(strat, sym)]:
                if t.open_flag:
                    continue
                by_yr.setdefault(t.entry_date[:4], []).append(t.R)
            if not by_yr:
                continue
            tot = {y: sum(v) for y, v in by_yr.items()}
            losing = [y for y, v in tot.items() if v < 0]
            wy = min(tot, key=lambda y: tot[y])
            print("{:<4} {:<5} {:>6} {:>7} {:>24} {:>10}".format(
                strat, sym, len(tot), len(losing),
                "{} ({:+.2f}R)".format(wy, tot[wy]), "{:+.2f}".format(tot[wy])))
    if not args.no_tables:
        write_table("yearly.csv",
                    ["strat", "sym", "year", "n", "p", "E", "b", "total_R"],
                    year_rows)

    # ------------------------------------------------- regime grid
    banner("4. REGIME GRID - trend state x realised-vol tercile")
    print("Trend state from close vs SMA(200) and the 20-day sign of SMA(200).")
    print("Vol tercile from trailing 20-day realised vol, cut per instrument.")
    print("Trades are assigned the regime of their ENTRY day.")
    regime_rows, neg_cells = [], []
    for sym in SYMBOLS:
        trend, terc, rv20, t1, t2 = regime_cache[sym]
        print("\n{}  (vol tercile cuts: LOW<= {:.1f} < MID <= {:.1f} < HIGH, annualised %)".format(
            sym, t1, t2))
        print("  {:<16} {:<6} {:>4} {:>7} {:>7} {:>8} {:>9}".format(
            "strategy", "regime", "n", "p", "b", "E", "total_R"))
        for strat in STRATEGIES:
            for st in ["UP_rising", "UP_falling", "DOWN_rising", "DOWN_falling"]:
                for tv in ["LOW", "MID", "HIGH"]:
                    sel = [t for t in all_trades[(strat, sym)]
                           if not t.open_flag
                           and trend[t.entry_i] == st and terc[t.entry_i] == tv]
                    if not sel:
                        continue
                    mm = metrics(sel)
                    tot = sum(t.R for t in sel)
                    print("  {:<16} {:<6} {:>4} {:>7} {:>7} {:>8} {:>9}".format(
                        strat, st + "|" + tv, mm["n"], f3(mm["p"]),
                        f2(mm["b"]), f3(mm["E"]), "{:+.2f}".format(tot)))
                    regime_rows.append([strat, sym, st, tv, mm["n"],
                                        "%.6f" % mm["p"], "%.6f" % mm["b"],
                                        "%.6f" % mm["E"], "%.4f" % tot])
                    if mm["E"] < 0:
                        neg_cells.append((strat, sym, st, tv, mm["n"], mm["E"], tot))
            for st in ["UP_rising", "UP_falling", "DOWN_rising", "DOWN_falling"]:
                sel = [t for t in all_trades[(strat, sym)]
                       if not t.open_flag and trend[t.entry_i] == st]
                if not sel:
                    continue
                mm = metrics(sel)
                tot = sum(t.R for t in sel)
                regime_rows.append([strat, sym, st, "ALL", mm["n"],
                                    "%.6f" % mm["p"], "%.6f" % mm["b"],
                                    "%.6f" % mm["E"], "%.4f" % tot])
                if mm["E"] < 0:
                    neg_cells.append((strat, sym, st, "ALL", mm["n"], mm["E"], tot))

    print("\nPOOLED ACROSS ALL FOUR INSTRUMENTS - regime profitability")
    print("Totals pool by summing R and n across instruments (valid); E_R = total_R/n.")
    print("{:<4} {:<16} {:>6} {:>8} {:>10} {:>9}".format(
        "stra", "trend state", "n", "p", "E_R", "total_R"))
    for strat in STRATEGIES:
        for st in ["UP_rising", "UP_falling", "DOWN_rising", "DOWN_falling"]:
            nsum, rsum, wsum = 0, 0.0, 0.0
            for sym in SYMBOLS:
                for t in all_trades[(strat, sym)]:
                    if t.open_flag:
                        continue
                    tr_lab, tc_lab, _, _, _ = regime_cache[sym]
                    if tr_lab[t.entry_i] != st:
                        continue
                    nsum += 1
                    rsum += t.R
                    if t.R > 0:
                        wsum += 1
            if not nsum:
                continue
            print("{:<4} {:<16} {:>6} {:>8} {:>10} {:>9}".format(
                strat, st, nsum, f3(wsum / nsum), f3(rsum / nsum),
                "{:+.2f}".format(rsum)))
    print("\n{:<4} {:<16} {:>6} {:>8} {:>10} {:>9}".format(
        "stra", "vol tercile", "n", "p", "E_R", "total_R"))
    for strat in STRATEGIES:
        for tv in ["LOW", "MID", "HIGH"]:
            nsum, rsum, wsum = 0, 0.0, 0.0
            for sym in SYMBOLS:
                for t in all_trades[(strat, sym)]:
                    if t.open_flag:
                        continue
                    _, tc_lab, _, _, _ = regime_cache[sym]
                    if tc_lab[t.entry_i] != tv:
                        continue
                    nsum += 1
                    rsum += t.R
                    if t.R > 0:
                        wsum += 1
            if not nsum:
                continue
            print("{:<4} {:<16} {:>6} {:>8} {:>10} {:>9}".format(
                strat, tv, nsum, f3(wsum / nsum), f3(rsum / nsum),
                "{:+.2f}".format(rsum)))
    print("\nNEGATIVE REGIME CELLS (strategy x instrument x trend x vol tercile):")
    if not neg_cells:
        print("  none")
    for strat, sym, st, tv, n, E, tot in neg_cells:
        print("  {:<3} {:<4} {:<14} vol {:<5} n={:<4} E={:+.3f} totalR={:+.2f}".format(
            strat, sym, st, tv, n, E, tot))
    print("\nTotal negative cells: {}".format(len(neg_cells)))
    if not args.no_tables:
        write_table("regime_grid.csv",
                    ["strat", "sym", "trend", "vol_tercile", "n", "p", "b", "E",
                     "total_R"], regime_rows)

    # ------------------------------------------------- vol premium
    banner("5. VOL-PREMIUM PROXY - selling premium on the S&P 500, 1990-2026")
    print("PROXY, not an option P&L.  VIX is a 30-day constant-maturity implied-vol")
    print("index on the S&P 500: it is not the IV of any traded instrument, and a")
    print("realised move is not the P&L of a short option position.  Collect")
    print("VIX/sqrt(252)*sqrt(21) in vol points at entry, pay the realised ABSOLUTE")
    print("move over the next 21 sessions.  R = payoff / (2 * collected), so a move")
    print("beyond 3x the implied move loses more than 1R.  Overlapping windows (every")
    print("session) give each year enough samples; the every-21st-session subset is")
    print("reported separately for independence.")
    print()
    d, o, h, l, c, tr = series["SPY"]
    vp = vol_premium(d, c, vix_by_date)
    Rs = [x["R"] for x in vp]
    n = len(Rs)
    wins = [x for x in Rs if x > 0]
    losses = [x for x in Rs if x <= 0]
    p = len(wins) / float(n)
    aw = sum(wins) / len(wins)
    al = sum(losses) / len(losses)
    b = aw / abs(al)
    mean_R = sum(Rs) / n
    print("as specified : n={} p={:.4f} b={:.3f} E_formula={:+.4f} E_R={:+.4f}R "
          "p*={:.4f} b*={:.4f} totalR={:+.1f}".format(
              n, p, b, p * b - (1 - p), mean_R, 1.0 / (1.0 + b), (1 - p) / p, sum(Rs)))
    print("               E_formula is inflated: it counts expectancy in units of the")
    print("               average loss (here {:.3f}R), and this payoff has a fat left".format(abs(al)))
    print("               tail, so the honest per-trade figure is E_R = {:+0.4f}R".format(mean_R))
    Rf = [x["R_fair"] for x in vp]
    wf = [x for x in Rf if x > 0]
    lf = [x for x in Rf if x <= 0]
    pf = len(wf) / float(n)
    bf = (sum(wf) / len(wf)) / abs(sum(lf) / len(lf))
    print("fair strike  : n={} p={:.4f} b={:.3f} E_R={:+.4f}R totalR={:+.1f}   "
          "<- the same series with the sqrt(2/pi) artifact removed".format(
              n, pf, bf, sum(Rf) / n, sum(Rf)))
    print("               (collecting the 1-sigma move and paying the realised ABSOLUTE")
    print("               move guarantees a positive mean on its own, because the mean")
    print("               absolute value of a normal is sqrt(2/pi) = 0.798, not 1.)")
    print("mean VRP (VIX minus forward 21-day realised vol) = {:+.2f} vol points".format(
        sum(x["vrp"] for x in vp) / n))
    print("share of windows with VIX above subsequent realised vol = {:.1%}".format(
        sum(1 for x in vp if x["vrp"] > 0) / float(n)))
    wt = min(vp, key=lambda x: x["R"])
    bt = max(vp, key=lambda x: x["R"])
    print("worst single trade: R={:+.2f} on {} (VIX {:.1f}, implied move {:.2f}%, "
          "realised abs move {:.2f}%)".format(
              wt["R"], wt["date"], wt["vix"], wt["collected"], wt["realised_abs"]))
    print("best  single trade: R={:+.2f} on {} (VIX {:.1f}, realised abs move {:.2f}%)".format(
        bt["R"], bt["date"], bt["vix"], bt["realised_abs"]))

    banner("5b. VOL-PREMIUM BY CALENDAR YEAR")
    print("{:<6} {:>5} {:>7} {:>7} {:>9} {:>8} {:>8} {:>9} {:>10} {:>10}".format(
        "year", "n", "p", "b", "E_form", "E_R", "p*", "total_R", "mean_VRP", "worst_R"))
    vp_year_rows = []
    by_year = {}
    for r in vp:
        by_year.setdefault(r["date"][:4], []).append(r)
    for yr in sorted(by_year):
        g = by_year[yr]
        rr = [x["R"] for x in g]
        w = [x for x in rr if x > 0]
        lo = [x for x in rr if x <= 0]
        pp = len(w) / float(len(rr))
        bb = (sum(w) / len(w)) / abs(sum(lo) / len(lo)) if w and lo else float("nan")
        ee = pp * bb - (1 - pp) if w and lo else float("nan")
        print("{:<6} {:>5} {:>7} {:>7} {:>9} {:>8} {:>8} {:>9} {:>10} {:>10}".format(
            yr, len(rr), f3(pp), f2(bb), f3(ee), f3(sum(rr) / len(rr)),
            f3(1.0 / (1.0 + bb)) if not math.isnan(bb) else "n/a",
            "{:+.1f}".format(sum(rr)),
            "{:+.2f}".format(sum(x["vrp"] for x in g) / len(g)),
            "{:+.2f}".format(min(rr))))
        vp_year_rows.append([yr, len(rr), "%.6f" % pp,
                             "" if math.isnan(bb) else "%.6f" % bb,
                             "" if math.isnan(ee) else "%.6f" % ee,
                             "%.6f" % (sum(rr) / len(rr)),
                             "%.4f" % sum(rr),
                             "%.4f" % (sum(x["vrp"] for x in g) / len(g)),
                             "%.4f" % min(rr)])
    tot_by_year = {y: sum(x["R"] for x in g) for y, g in by_year.items()}
    losing_years = sorted(y for y, v in tot_by_year.items() if v < 0)
    wy = min(tot_by_year, key=lambda y: tot_by_year[y])
    print("\nlosing years: {} of {}  ({})".format(
        len(losing_years), len(tot_by_year),
        ", ".join(losing_years) if losing_years else "none"))
    print("worst year: {} at {:+.1f}R ({} windows)".format(
        wy, tot_by_year[wy], len(by_year[wy])))

    banner("5c. VOL-PREMIUM BY REGIME (S&P 500 regime on the entry date)")
    trend, terc, rv20, t1, t2 = regime_cache["SPY"]
    print("vol tercile cuts on SPY: LOW<= {:.1f} < MID <= {:.1f} < HIGH".format(t1, t2))
    print("{:<16} {:<8} {:>5} {:>7} {:>7} {:>9} {:>8} {:>9} {:>10}".format(
        "trend", "vol", "n", "p", "b", "E_form", "E_R", "total_R", "mean_VRP"))
    vp_regime_rows = []
    for st in ["UP_rising", "UP_falling", "DOWN_rising", "DOWN_falling"]:
        for tv in ["LOW", "MID", "HIGH"]:
            g = [r for r in vp if trend[r["d"]] == st and terc[r["d"]] == tv]
            if len(g) < 5:
                continue
            rr = [x["R"] for x in g]
            w = [x for x in rr if x > 0]
            lo = [x for x in rr if x <= 0]
            pp = len(w) / float(len(rr))
            bb = (sum(w) / len(w)) / abs(sum(lo) / len(lo)) if w and lo else float("nan")
            ee = pp * bb - (1 - pp) if w and lo else float("nan")
            print("{:<16} {:<8} {:>5} {:>7} {:>7} {:>9} {:>8} {:>9} {:>10}".format(
                st, tv, len(rr), f3(pp), f2(bb), f3(ee), f3(sum(rr) / len(rr)),
                "{:+.1f}".format(sum(rr)),
                "{:+.2f}".format(sum(x["vrp"] for x in g) / len(g))))
            vp_regime_rows.append([st, tv, len(rr), "%.6f" % pp,
                                   "" if math.isnan(bb) else "%.6f" % bb,
                                   "" if math.isnan(ee) else "%.6f" % ee,
                                   "%.6f" % (sum(rr) / len(rr)),
                                   "%.4f" % sum(rr),
                                   "%.4f" % (sum(x["vrp"] for x in g) / len(g))])

    vp_nov = vol_premium(d, c, vix_by_date, step=VOL_WINDOW)
    rr = [x["R"] for x in vp_nov]
    w = [x for x in rr if x > 0]
    lo = [x for x in rr if x <= 0]
    pp = len(w) / float(len(rr))
    bb = (sum(w) / len(w)) / abs(sum(lo) / len(lo))
    print("\nnon-overlapping subset (every 21st session): n={} p={:.4f} b={:.3f} "
          "E={:+.4f}R totalR={:+.1f}".format(len(rr), pp, bb, pp * bb - (1 - pp), sum(rr)))
    banner("5d. FAIR-STRIKE VARIANT - the same years, the sqrt(2/pi) artifact removed")
    print("Collect the expected absolute move (0.798 x implied) instead of the")
    print("1-sigma move.  Now the payoff is unbiased and the only edge left is")
    print("whether VIX really exceeded the vol that followed.")
    print("{:<6} {:>5} {:>7} {:>7} {:>9} {:>9} {:>10} {:>10}".format(
        "year", "n", "p", "b", "E_R", "total_R", "mean_VRP", "worst_R"))
    f_year_rows = []
    by_year_f = {}
    for x in vp:
        by_year_f.setdefault(x["date"][:4], []).append(x)
    for yr in sorted(by_year_f):
        g = by_year_f[yr]
        rr_f = [x["R_fair"] for x in g]
        w = [x for x in rr_f if x > 0]
        lo = [x for x in rr_f if x <= 0]
        ppf = len(w) / float(len(rr_f))
        bbf = (sum(w) / len(w)) / abs(sum(lo) / len(lo)) if w and lo else float("nan")
        print("{:<6} {:>5} {:>7} {:>7} {:>9} {:>9} {:>10} {:>10}".format(
            yr, len(rr_f), f3(ppf), f2(bbf), f3(sum(rr_f) / len(rr_f)),
            "{:+.1f}".format(sum(rr_f)),
            "{:+.2f}".format(sum(x["vrp"] for x in g) / len(g)),
            "{:+.2f}".format(min(rr_f))))
        f_year_rows.append([yr, len(rr_f), "%.6f" % ppf,
                            "" if math.isnan(bbf) else "%.6f" % bbf,
                            "%.6f" % (sum(rr_f) / len(rr_f)),
                            "%.4f" % sum(rr_f),
                            "%.4f" % (sum(x["vrp"] for x in g) / len(g)),
                            "%.4f" % min(rr_f)])
    tot_f = {y: sum(x["R_fair"] for x in g) for y, g in by_year_f.items()}
    losing_f = sorted(y for y, v in tot_f.items() if v < 0)
    wyf = min(tot_f, key=lambda y: tot_f[y])
    wtf = min(vp, key=lambda x: x["R_fair"])
    print("\nFAIR-STRIKE losing years: {} of {}  ({})".format(
        len(losing_f), len(tot_f), ", ".join(losing_f) if losing_f else "none"))
    print("FAIR-STRIKE worst year: {} at {:+.1f}R".format(wyf, tot_f[wyf]))
    print("FAIR-STRIKE worst single trade: R={:+.2f} on {} (VIX {:.1f}, implied "
          "expected abs move {:.2f}%, realised {:.2f}%)".format(
              wtf["R_fair"], wtf["date"], wtf["vix"], wtf["collected_fair"],
              wtf["realised_abs"]))
    print("\nThis is the honest answer to \"is selling premium worth it?\": on average")
    print("the premium is real, but it is not free - the loss years and the single")
    print("worst window above are the price of it.")
    if not args.no_tables:
        write_table("volpremium_year.csv",
                    ["year", "n", "p", "b", "E_formula", "E_R", "total_R",
                     "mean_VRP", "worst_R"], vp_year_rows)
        write_table("volpremium_regime.csv",
                    ["trend", "vol_tercile", "n", "p", "b", "E_formula", "E_R",
                     "total_R", "mean_VRP"], vp_regime_rows)
        write_table("volpremium_fair_year.csv",
                    ["year", "n", "p", "b", "E_R", "total_R", "mean_VRP", "worst_R"],
                    f_year_rows)

    # ------------------------------------------------- parameter fishing
    banner("6. TASK 5 - PARAMETER FISHING ON M1 (the honesty centrepiece)")
    print("Pre-registered M1 is RSI(2)<10 with a 5-day cap.  Here we deliberately")
    print("search instead.  First 70% of sessions = in-sample, last 30% = held out.")
    print("The in-sample winner is then evaluated once on the held-out data.")
    print()

    def grid_search(sym, thresholds, holds, label):
        dd, oo, hh, ll, cc, tt = series[sym]
        cut = int(len(dd) * 0.70)
        cut_date = dd[cut]
        rows = []
        for th in thresholds:
            for hd in holds:
                trades, _ = run_strategy(dd, oo, hh, ll, cc, "M1",
                                         rsi_thresh=th, max_hold=hd)
                is_tr = [t for t in trades if not t.open_flag and t.entry_i < cut]
                oos_tr = [t for t in trades if not t.open_flag and t.entry_i >= cut]
                rows.append({"th": th, "hd": hd, "is": metrics(is_tr),
                             "oos": metrics(oos_tr)})
        print("{} GRID - {}: {} combinations, in-sample {} -> {}, held-out {} -> {}".format(
            label, sym, len(rows), dd[0], cut_date, cut_date, dd[-1]))
        print("{:<6} {:<6} {:>5} {:>8} {:>8} {:>9} {:>9} | {:>5} {:>8} {:>8} {:>9}".format(
            "RSI<", "hold", "n_is", "p_is", "b_is", "E_is", "totR_is",
            "n_oos", "p_oos", "b_oos", "E_oos"))
        for r in sorted(rows, key=lambda r: (r["th"], r["hd"])):
            mi, mo = r["is"], r["oos"]
            print("{:<6} {:<6} {:>5} {:>8} {:>8} {:>9} {:>9} | {:>5} {:>8} {:>8} {:>9}".format(
                r["th"], r["hd"], mi["n"] if mi else 0,
                f3(mi["p"]) if mi else "-", f2(mi["b"]) if mi else "-",
                f3(mi["E"]) if mi else "-", f1(mi["total_R"]) if mi else "-",
                mo["n"] if mo else 0, f3(mo["p"]) if mo else "-",
                f2(mo["b"]) if mo else "-", f3(mo["E"]) if mo else "-"))
        with_is = [r for r in rows if r["is"]]
        best = max(with_is, key=lambda r: r["is"]["E"])
        es = sorted(r["is"]["E"] for r in with_is)
        npos = sum(1 for e in es if e > 0)
        print("\n  in-sample E distribution over {} tried: best {:+.3f} | median {:+.3f} | worst {:+.3f}".format(
            len(with_is), es[-1], es[len(es) // 2], es[0]))
        print("  in-sample positive-E combinations: {} of {} ({:.0%})".format(
            npos, len(es), npos / float(len(es))))
        m = len(with_is)
        alpha = 0.05
        crit = norm_ppf(1.0 - alpha / (2.0 * m))
        clear = [r for r in with_is
                 if not math.isnan(r["is"]["t_stat"]) and abs(r["is"]["t_stat"]) > crit]
        clear_oos = [r for r in clear if r["oos"] and r["oos"]["E"] > 0]
        print("  Bonferroni bar for m={} at alpha=0.05: per-test alpha={:.6f}, "
              "critical |t| = {:.3f}".format(m, alpha / m, crit))
        print("  combinations clearing the bar in-sample: {} of {}".format(len(clear), m))
        print("  of those, still positive out-of-sample: {} of {}".format(
            len(clear_oos), len(clear)))
        print("\n  --- the winner, in-sample vs held out ---")
        print("  best in-sample: RSI<{} hold={} | IS  n={} p={} b={} E={:+.3f} totalR={:+.1f}".format(
            best["th"], best["hd"], best["is"]["n"], f3(best["is"]["p"]),
            f2(best["is"]["b"]), best["is"]["E"], best["is"]["total_R"]))
        if best["oos"]:
            mo = best["oos"]
            print("  same rule held out:                    | OOS n={} p={} b={} E={:+.3f} totalR={:+.1f}".format(
                mo["n"], f3(mo["p"]), f2(mo["b"]), mo["E"], mo["total_R"]))
            drag = mo["E"] - best["is"]["E"]
            rel = (drag / best["is"]["E"]) if best["is"]["E"] else float("nan")
            print("  expectancy change IS -> OOS: {:+.3f}R ({:+.0%} of the in-sample value)".format(
                drag, rel))
            print("  VERDICT: {}".format(
                "the edge SURVIVES the holdout" if mo["E"] > 0
                else "the edge VANISHES out-of-sample - it was a fitted number"))
        else:
            print("  no held-out trades at all")
        # the pre-registered default is RSI<10 with a 5-day cap; it sits inside
        # every grid, so the comparison is like-for-like on the same split
        default = None
        for r in rows:
            if r["th"] == 10 and r["hd"] == 5:
                default = r
                break
        if default and default["is"] and default["oos"] and best["oos"]:
            tuned_gain_is = best["is"]["E"] - default["is"]["E"]
            tuned_gain_oos = best["oos"]["E"] - default["oos"]["E"]
            print("\n  --- tuned winner vs the PRE-REGISTERED default (RSI<10 hold=5) ---")
            print("  in-sample, the search beat the default by {:+.3f}R per trade".format(
                tuned_gain_is))
            print("  out-of-sample, the same search beat the default by {:+.3f}R per trade".format(
                tuned_gain_oos))
            if tuned_gain_is != 0:
                print("  the tuned advantage retained: {:.0%} of what it looked like in-sample".format(
                    tuned_gain_oos / tuned_gain_is))
            print("  IS  default E={:+.3f}  winner E={:+.3f}".format(
                default["is"]["E"], best["is"]["E"]))
            print("  OOS default E={:+.3f}  winner E={:+.3f}".format(
                default["oos"]["E"], best["oos"]["E"]))
        rows_for_csv = []
        for r in sorted(rows, key=lambda r: (r["th"], r["hd"])):
            mi, mo = r["is"], r["oos"]
            rows_for_csv.append([
                r["th"], r["hd"],
                mi["n"] if mi else 0,
                "%.6f" % mi["p"] if mi else "", "%.6f" % mi["b"] if mi else "",
                "%.6f" % mi["E"] if mi else "", "%.4f" % mi["total_R"] if mi else "",
                "%.4f" % mi["t_stat"] if mi else "",
                mo["n"] if mo else 0,
                "%.6f" % mo["p"] if mo else "", "%.6f" % mo["b"] if mo else "",
                "%.6f" % mo["E"] if mo else "", "%.4f" % mo["total_R"] if mo else "",
            ])
        if not args.no_tables:
            write_table("fishing_{}.csv".format(label.lower()),
                        ["rsi_thresh", "hold", "is_n", "is_p", "is_b", "is_E",
                         "is_total_R", "is_t", "oos_n", "oos_p", "oos_b",
                         "oos_E", "oos_total_R"], rows_for_csv)
        return {"m": m, "crit": crit, "clear": len(clear),
                "clear_oos": len(clear_oos), "best": best, "npos": npos}

    res_a = grid_search("SPY", [5, 10, 15, 20, 25, 30], [2, 3, 5, 8, 10], "GRID-A")
    print()
    res_b = grid_search("QQQ", [5, 10, 15, 20, 25, 30, 35, 40],
                        [2, 3, 4, 5, 8, 10, 15], "GRID-B")

    banner("6b. PARAMETER-FISHING CONCLUSION (stated plainly)")
    print("Grid A searched {} M1 variants on SPY; grid B searched {} on QQQ.".format(
        res_a["m"], res_b["m"]))
    print("Grid A best in-sample: RSI<{} hold={} at E={:+.3f}R".format(
        res_a["best"]["th"], res_a["best"]["hd"], res_a["best"]["is"]["E"]))
    if res_a["best"]["oos"]:
        print("  held out, the same combination scores E={:+.3f}R".format(
            res_a["best"]["oos"]["E"]))
    print("Grid B best in-sample: RSI<{} hold={} at E={:+.3f}R".format(
        res_b["best"]["th"], res_b["best"]["hd"], res_b["best"]["is"]["E"]))
    if res_b["best"]["oos"]:
        print("  held out, the same combination scores E={:+.3f}R".format(
            res_b["best"]["oos"]["E"]))
    print("Bonferroni grid A: m={} -> |t|>{:.3f}; {} cleared, {} of those held up".format(
        res_a["m"], res_a["crit"], res_a["clear"], res_a["clear_oos"]))
    print("Bonferroni grid B: m={} -> |t|>{:.3f}; {} cleared, {} of those held up".format(
        res_b["m"], res_b["crit"], res_b["clear"], res_b["clear_oos"]))
    print("\nIterating until a backtest turns green produces a number fitted to that")
    print("sample.  The out-of-sample gap above is the evidence, and the in-sample")
    print("distribution shows the best of many tries is expected to look good by luck.")
    banner("7. HOW MANY OF THE PRE-REGISTERED CELLS SURVIVE MULTIPLE COMPARISONS?")
    m_cells = len([r for r in table_rows])
    crit_cells = norm_ppf(1.0 - 0.05 / (2.0 * m_cells))
    print("The study tested {} pre-registered cells (3 rule sets x 4 instruments).".format(m_cells))
    print("Bonferroni bar at alpha=0.05 for m={}: per-test alpha={:.6f}, |t| > {:.3f}".format(
        m_cells, 0.05 / m_cells, crit_cells))
    print("{:<4} {:<5} {:>7} {:>6} {:>9} {:>9}".format(
        "stra", "sym", "t", "n", "E_R", "verdict"))
    cleared = []
    for r in sorted(summary_rows, key=lambda r: -abs(r["t_stat"])):
        ok = abs(r["t_stat"]) > crit_cells
        if ok:
            cleared.append(r)
        print("{:<4} {:<5} {:>7} {:>6} {:>9} {:>9}".format(
            r["strat"], r["sym"], f2(r["t_stat"]), r["n"], f3(r["E_R"]),
            "CLEARS" if ok else "fails"))
    print("\n{} of {} cells clear the bar after correcting for the search.".format(
        len(cleared), m_cells))
    if cleared:
        print("{}".format(", ".join("{}/{}".format(r["strat"], r["sym"])
                                    for r in cleared)))

    banner("7b. ROBUSTNESS OF THE SURVIVING EDGE")
    for r in cleared:
        sym = r["sym"]
        strat = r["strat"]
        d, o, h, l, c, tr = series[sym]
        trades = all_trades[(strat, sym)]
        n = len(d)
        print("\n{} on {}: {} closed trades, E_R={:+.4f}, t={:.2f}".format(
            strat, sym, r["n"], r["E_R"], r["t_stat"]))
        by_yr = {}
        for t in trades:
            if t.open_flag:
                continue
            by_yr.setdefault(t.entry_date[:4], []).append(t.R)
        pos = sum(1 for y, v in by_yr.items() if sum(v) > 0)
        print("  calendar years with trades: {} | positive: {} ({:.0%}) | negative: {}".format(
            len(by_yr), pos, pos / float(len(by_yr)), len(by_yr) - pos))
        for lab, lo, hi in [("first half", 0, n // 2), ("second half", n // 2, n)]:
            sel = [t for t in trades if not t.open_flag and lo <= t.entry_i < hi]
            mm = metrics(sel)
            if mm:
                print("  {:<12} n={:>3} p={:.3f} E_R={:+.4f} t={:+.2f} totalR={:+.1f}".format(
                    lab, mm["n"], mm["p"], mm["E_R"], mm["t_stat"], mm["total_R"]))
        dec = {}
        for t in trades:
            if t.open_flag:
                continue
            dec.setdefault(t.entry_date[:3] + "0s", []).append(t.R)
        print("  by decade:")
        for k in sorted(dec):
            v = dec[k]
            print("    {:<6} n={:>3} E_R={:+.4f} totalR={:+.1f}".format(
                k, len(v), sum(v) / len(v), sum(v)))
        print("  A fished parameter would not survive all four decades; this does or does")
        print("  not - read the numbers above rather than the claim.")

    banner("8. EXIT MIX AND COST SENSITIVITY - sizing the zero-cost assumption")
    print("Every expectancy in this study is GROSS: no commission, no slippage, no")
    print("borrow.  These two tables let a reader size that omission instead of just")
    print("noting it.")
    print("\n8a. How each trade ended")
    print("{:<4} {:<5} {:>6} {:>10} {:>10} {:>10}".format(
        "stra", "sym", "n", "stop", "target", "time/eod"))
    exit_rows = []
    for strat in STRATEGIES:
        for sym in SYMBOLS:
            closed = [t for t in all_trades[(strat, sym)] if not t.open_flag]
            if not closed:
                continue
            ns = sum(1 for t in closed if t.reason == "stop")
            nt = sum(1 for t in closed if t.reason == "target")
            nx = len(closed) - ns - nt
            print("{:<4} {:<5} {:>6} {:>10} {:>10} {:>10}".format(
                strat, sym, len(closed),
                "{} ({:.0f}%)".format(ns, 100.0 * ns / len(closed)),
                "{} ({:.0f}%)".format(nt, 100.0 * nt / len(closed)),
                "{} ({:.0f}%)".format(nx, 100.0 * nx / len(closed))))
            exit_rows.append([strat, sym, len(closed), ns, nt, nx])
    print("\n8b. Cost sensitivity: a round trip of c basis points of price costs")
    print("    c/100 / (1R as a percent of price) in R, because 1R is 2 x ATR(14).")
    print("{:<4} {:<5} {:>9} {:>10} {:>10} {:>12} {:>12}".format(
        "stra", "sym", "1R %px", "gross E_R", "b/e bps", "cost@1bp", "cost@5bp"))
    cost_rows = []
    for strat in STRATEGIES:
        for sym in SYMBOLS:
            closed = [t for t in all_trades[(strat, sym)] if not t.open_flag]
            if not closed:
                continue
            mm = metrics(closed)
            risks = sorted(t.risk / t.entry_px * 100.0 for t in closed)
            r = risks[len(risks) // 2]
            breakeven_bps = mm["E_R"] * r * 100.0 if mm["E_R"] > 0 else 0.0
            c1 = (1.0 / 100.0) / r
            c5 = (5.0 / 100.0) / r
            print("{:<4} {:<5} {:>9} {:>10} {:>12} {:>12} {:>12}".format(
                strat, sym, f2(r) + "%", f3(mm["E_R"]),
                f1(breakeven_bps) if breakeven_bps else "n/a",
                "{:.4f}R".format(c1), "{:.4f}R".format(c5)))
            cost_rows.append([strat, sym, "%.4f" % r, "%.6f" % mm["E_R"],
                              "%.4f" % breakeven_bps, "%.6f" % c1, "%.6f" % c5])
    print("\n'b/e bps' is the round-trip cost at which that cell's gross edge is")
    print("exactly consumed.  A cell whose b/e is below the instrument's real spread")
    print("has no net edge at all.")
    if not args.no_tables:
        write_table("exit_mix.csv",
                    ["strat", "sym", "n", "stop", "target", "time_or_eod"],
                    exit_rows)
        write_table("cost_sensitivity.csv",
                    ["strat", "sym", "risk_pct_of_price", "gross_E_R",
                     "breakeven_roundtrip_bps", "cost_at_1bp_R", "cost_at_5bp_R"],
                    cost_rows)

    print("\nwritten tables: {}".format(OUT if not args.no_tables else "(stdout only)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
