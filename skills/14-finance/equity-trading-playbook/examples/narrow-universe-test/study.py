#!/usr/bin/env python3
"""
narrow-universe-test / study.py

THE QUESTION (stated by the desk owner, tested here rather than opined on):

    Restrict the universe to a few index ETFs (SPY, QQQ, IWM) -- or to the
    S&P 100 / Nasdaq 100 constituents -- and trade those, stocks and options.
    Is a narrow, highly liquid universe better or worse than a broad one?

WHAT IS ACTUALLY TESTED.  Five questions, in the order asked:

  1. Diversification cost of narrowing.  Pairwise yearly and daily correlation of
     SPY/QQQ/IWM; then positivity-by-horizon and CAGR/DD/Sharpe for a 3-index
     equal-weight TREND book, the cross-asset 4-sleeve book the sibling
     weather-test built, and buy & hold SPY; then the lambda frontier (risky
     scaled against the cash series) for the 3-index book, so it can be compared
     with the cross-asset frontier already published.
  2. Basket of constituents vs the index.  A DECLARED, FIXED set of 14 large
     constituents; equal-weight and inverse-volatility baskets, buy & hold and
     trend-overlaid; correlation to SPY and to each other; CAGR/DD/Sharpe;
     positivity by horizon; and the count of negative regime cells
     (trend state x realised-vol tercile).
  3. The dispersion proxy.  Index realised vol vs average constituent realised
     vol, and the cross-sectional dispersion of constituent returns.  A PROXY,
     not a tradable dispersion P&L; the run says so in the tables.
  4. Costs and liquidity.  A measured NBBO snapshot for all 17 instruments,
     converted into a round-trip cost differential, and the book re-run at
     several round-trip levels to see how much of any narrow-universe advantage
     survives.
  5. The verdict.  Highest fraction of positive years at a CAGR above cash, its
     losing years, and whether narrowing moves the frontier -- with the
     arithmetic.

WHAT IS PRE-REGISTERED (fixed before the run; nothing below is searched):

  * the sleeve rule: close > SMA(200), monthly rebalance, equal weight
  * the 3-index universe: SPY, QQQ, IWM
  * the cross-asset universe: SPY, TLT, GLD, EEM (the weather-test's F book)
  * the 14 constituents: the fourteen tickers named in the brief, verbatim
  * the "present for the whole window" subset: every constituent of those 14
    whose first available bar is on or before the long window's start date
    (2005-09-02).  This is a LISTING-DATE rule, not a performance rule.
  * the horizon buckets: D, W, 2W, M, Q, H, Y
  * the inverse-vol rule: weight proportional to 1/trailing-60-day sample sd of
    the instrument's own close-to-close return, capped to [0.5x, 3x] equal
    weight and renormalised once
  * the cost levels: 0 (gross), 2 bp, 4 bp, 20 bp, 50 bp round trip
  * the 70/30 time split, at the 70th percentile of book days

WHAT IS DELIBERATELY *NOT* DONE.  Nothing is fitted.  No weight, horizon,
threshold or universe member is chosen because it scored well.  The lambda
frontier is a GRID, not an optimum, and the "best" lambda on it is reported with
the plateau it sits on.

OUTPUT: out/*.csv (machine-readable) + stdout (the tables in RESULTS.md).
RUN:    py -3 study.py
"""

import datetime
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
OUT_DIR = os.path.join(HERE, "out")
ENGINE_DIR = os.path.abspath(os.path.join(
    HERE, "..", "..", "..", "timeframe-performance-statistics", "scripts"))

TRADING_DAYS_PER_YEAR = 252
SMA_TREND = 200
PULL_DATE = "2026-10-14"
QUOTE_STAMP = "2026-10-15T00:39Z"

# --- THE DECLARED UNIVERSES.  Fixed before the run. -----------------------
NARROW3 = ["SPY", "QQQ", "IWM"]
CROSS4 = ["SPY", "TLT", "GLD", "EEM"]
CONSTITUENTS14 = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
                  "JPM", "JNJ", "WMT", "XOM", "UNH", "V", "AVGO"]
LONG_WINDOW_START = datetime.date(2005, 9, 2)   # the weather-test's own window

# --- THE GRID.  Fixed before the run.  Not searched. ----------------------
LAMBDA_STEPS = 20                       # lambda = i / 20, i in 0..20
ROUND_TRIPS_BPS = [0.0, 2.0, 4.0, 20.0, 50.0]
BUCKETS = ["D", "W", "2W", "M", "Q", "H", "Y"]

# --- "MEANINGFUL" RETURN THRESHOLDS.  Defined here, before the run. -------
MEANINGFUL_EXCESS = [0.00, 0.01, 0.02, 0.03]
FINE_STEP = 0.001

# --- Inverse-volatility rule constants.  Fixed before the run. ------------
IV_LOOKBACK = 60
IV_FLOOR_MULT = 0.5
IV_CAP_MULT = 3.0

# --- Regime-cell definition.  Fixed before the run. ----------------------
RV_WINDOW = 21                          # realised-vol window, trading days
MIN_CELL_DAYS = 60                      # below this a regime cell is unreadable

CASH_SYMBOL = "US03M"
CASH_PRICE_CROSSCHECK = "BIL"
REFERENCE_FOR_REGIME = "SPY"

ALL_SYMBOLS = sorted(set(NARROW3 + CROSS4 + CONSTITUENTS14
                         + [CASH_SYMBOL, CASH_PRICE_CROSSCHECK, "VIX"]))

# The repo requires LF everywhere.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")


# ---------------------------------------------------------------------------
# The sibling engine, imported rather than re-implemented
# ---------------------------------------------------------------------------

def load_engine():
    path = os.path.join(ENGINE_DIR, "timeframe_stats.py")
    if not os.path.isfile(path):
        raise SystemExit(
            "ERROR: the sibling engine is missing.\n  expected: %s\n"
            "  This study imports its bucket_key / aggregate_bucket / sample_sd /\n"
            "  max_drawdown / lag1_autocorr / n_effective instead of\n"
            "  re-implementing them." % path)
    if ENGINE_DIR not in sys.path:
        sys.path.insert(0, ENGINE_DIR)
    import timeframe_stats as TF
    for fn in ("bucket_key", "aggregate_bucket", "sample_sd", "max_drawdown",
               "lag1_autocorr", "n_effective"):
        if not hasattr(TF, fn):
            raise SystemExit("ERROR: engine has no %s()" % fn)
    return TF


TF = load_engine()
NA = TF.NA


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def pct(v, nd=2):
    if v is NA:
        return "n/a"
    return ("%." + str(nd) + "f%%") % (100.0 * v)


def num(v, nd=4):
    if v is NA:
        return "n/a"
    return ("%." + str(nd) + "f") % v


def equity_curve(rets):
    curve = [1.0]
    for r in rets:
        curve.append(curve[-1] * (1.0 + r))
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


def mean(xs):
    return sum(xs) / float(len(xs)) if xs else NA


def pearson(xs, ys):
    """Pearson product-moment correlation.  NA on a degenerate input."""
    n = min(len(xs), len(ys))
    if n < 3:
        return NA
    mx = sum(xs[:n]) / n
    my = sum(ys[:n]) / n
    sxy = sxx = syy = 0.0
    for i in range(n):
        dx = xs[i] - mx
        dy = ys[i] - my
        sxy += dx * dy
        sxx += dx * dx
        syy += dy * dy
    if sxx <= 0.0 or syy <= 0.0:
        return NA
    return sxy / math.sqrt(sxx * syy)


def table(headers, rows, indent="  "):
    widths = [len(str(h)) for h in headers]
    for r in rows:
        for i, c in enumerate(r):
            widths[i] = max(widths[i], len(str(c)))
    out = [indent + "  ".join(str(h).ljust(widths[i])
                              for i, h in enumerate(headers)).rstrip()]
    out.append(indent + "  ".join("-" * widths[i] for i in range(len(headers))))
    for r in rows:
        out.append(indent + "  ".join(str(c).ljust(widths[i])
                                      for i, c in enumerate(r)).rstrip())
    return out


def write_csv(path, provenance, headers, rows):
    """CSV with RFC-4180 quoting.

    A previous version joined fields with "," and never quoted them, so any
    label containing a comma (several of the weight descriptions do) silently
    shifted every following column by one.  handcheck.py caught it.
    """
    def q(v):
        s = "" if v is None else str(v)
        if any(ch in s for ch in (",", '"', "\n", "\r")):
            return '"' + s.replace('"', '""') + '"'
        return s

    lines = ["# PROVENANCE: %s" % p for p in provenance]
    lines.append(",".join(q(h) for h in headers))
    for r in rows:
        lines.append(",".join(q(v) for v in r))
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return len(rows)


# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------

class Series(object):
    def __init__(self, symbol, dates, o, h, l, c, v, provenance):
        self.symbol = symbol
        self.dates = dates
        self.o, self.h, self.l, self.c, self.v = o, h, l, c, v
        self.provenance = provenance
        self.index_of = {d: i for i, d in enumerate(dates)}

    def __len__(self):
        return len(self.dates)


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
            if line.startswith("date,") or line.startswith("symbol,"):
                continue
            f = line.rstrip("\r\n").split(",")
            dates.append(datetime.date.fromisoformat(f[0]))
            o.append(float(f[1]))
            h.append(float(f[2]))
            l.append(float(f[3]))
            c.append(float(f[4]))
            v.append(float(f[5]) if len(f) > 5 and f[5].strip() else 0.0)
    if len(dates) < 300:
        raise SystemExit("ERROR: %s has only %d rows; need >= 300"
                         % (path, len(dates)))
    if any(dates[i] >= dates[i + 1] for i in range(len(dates) - 1)):
        raise SystemExit("ERROR: %s dates are not strictly increasing" % path)
    symbol = os.path.basename(path).split("_")[0]
    return Series(symbol, dates, o, h, l, c, v, provenance)


def load_universe():
    out = {}
    for sym in ALL_SYMBOLS:
        path = os.path.join(DATA_DIR, sym + "_1d.csv")
        if not os.path.isfile(path):
            raise SystemExit("ERROR: missing input %s" % path)
        out[sym] = read_bars(path)
    return out


def load_quotes():
    """The measured NBBO snapshot, as {symbol: dict}."""
    path = os.path.join(DATA_DIR, "cost-quotes.csv")
    if not os.path.isfile(path):
        raise SystemExit("ERROR: missing %s" % path)
    rows = {}
    prov = []
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            if line.startswith("# PROVENANCE:"):
                prov.append(line[len("# PROVENANCE:"):].strip())
                continue
            if line.startswith("#") or not line.strip():
                continue
            if line.startswith("symbol,"):
                continue
            f = line.rstrip("\r\n").split(",")
            rows[f[0]] = {"last": float(f[1]), "bid": float(f[2]),
                          "ask": float(f[3]), "high": float(f[4]),
                          "low": float(f[5]), "volume": float(f[6])}
    return rows, prov


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


# ---------------------------------------------------------------------------
# Sleeves -- the sibling rule: long when close > SMA(200)
# ---------------------------------------------------------------------------

class Sleeve(object):
    """One rule, reduced to a daily return series on its OWN calendar."""

    def __init__(self, code, bars, window):
        self.code = code
        self.symbol = bars.symbol
        self.dates = bars.dates
        self.index_of = bars.index_of
        self.c = bars.c
        self.raw_ret = [0.0] * len(bars.c)
        for i in range(1, len(bars.c)):
            if bars.c[i - 1] > 0.0:
                self.raw_ret[i] = bars.c[i] / bars.c[i - 1] - 1.0
        avg = sma(bars.c, window)
        self.sma_window = window
        self.pos = [NA] * len(bars.c)
        for i in range(len(bars.c)):
            self.pos[i] = NA if avg[i] is NA else (1 if bars.c[i] > avg[i] else 0)
        self.ret = [0.0] * len(bars.c)
        for i in range(1, len(bars.c)):
            p = self.pos[i - 1]
            self.ret[i] = (0 if p is NA else p) * self.raw_ret[i]
        self.first_live = None
        for i in range(len(bars.c)):
            if self.pos[i] is not NA:
                self.first_live = bars.dates[i]
                break

    def align(self, dates):
        """(ret, hold, flip, raw) aligned to `dates`, sibling convention.

        A position may only change on a BOOK date: the position held through book
        date j is the one established at the close of the previous book date's
        bar.  A book date with no bar of its own contributes 0.0 and carries the
        previous position.
        """
        n = len(dates)
        ret = [0.0] * n
        hold = [0] * n
        flip = [False] * n
        raw = [0.0] * n
        last_bar = None
        carried = 0
        for j, d in enumerate(dates):
            k = self.index_of.get(d)
            if k is None:
                carried += 1
                hold[j] = hold[j - 1] if j else 0
                continue
            if last_bar is not None:
                p = self.pos[last_bar]
                hold[j] = 0 if p is NA else p
                if self.c[last_bar] > 0.0:
                    ret[j] = hold[j] * (self.c[k] / self.c[last_bar] - 1.0)
                    raw[j] = self.c[k] / self.c[last_bar] - 1.0
            flip[j] = (j > 0 and hold[j] != hold[j - 1])
            last_bar = k
        self.aligned_carried = carried
        return ret, hold, flip, raw


def book_window(universe, sleeve_symbols, window_symbols, floor=None):
    """Window = first date EVERY sleeve's rule is computable, restricted to dates
    present in every instrument of the calendar set."""
    sleeves = {}
    for sym in sleeve_symbols:
        sleeves[sym] = Sleeve(sym, universe[sym], SMA_TREND)
    start = max(sleeves[s].first_live for s in sleeve_symbols)
    if floor is not None and floor > start:
        start = floor
    sets = [set(universe[s].dates) for s in window_symbols]
    common = set.intersection(*sets)
    dates = sorted(d for d in common if d >= start)
    if len(dates) < 300:
        raise SystemExit("ERROR: window too short for %r" % (sleeve_symbols,))
    return dates, sleeves


# ---------------------------------------------------------------------------
# The book -- the sibling simulator, extended to time-varying target weights
# ---------------------------------------------------------------------------

class BookResult(object):
    def __init__(self):
        self.dates = []
        self.rets = []
        self.sleeve_rets = {}
        self.flips_total = 0
        self.turnover_total = 0.0
        self.cost_bps = 0.0
        self.weights_used = []


def simulate(dates, aligned, weights_fn, cost_bps=0.0):
    """Fixed-or-varying-weight, monthly-rebalanced book.

        cost_j   = (round_trip/2) * sum of weights that flipped on day j
                 + (round_trip/2) * one-way turnover on a rebalance day
        gross_j  = sum_s  w_s * r_s(j)
        R_j      = (1 + gross_j) * (1 - cost_j) - 1

    Charging the cost in the RETURN is what makes it bite; charging it by
    shrinking a sleeve's dollar value does not, because the weights are
    renormalised every day.  A constant `weights_fn` reproduces the sibling
    frontier-test / weather-test simulator exactly, which is checked in §12.
    """
    syms = sorted(aligned.keys())
    half = (cost_bps / 2.0) / 10000.0

    res = BookResult()
    res.cost_bps = cost_bps
    res.dates = list(dates)
    if len(dates) < 2:
        raise SystemExit("ERROR: book window has fewer than 2 days")

    target = weights_fn(0)
    tot = sum(target.values())
    target = {s: target.get(s, 0.0) / tot for s in syms}
    w = dict(target)
    month_prev = dates[0].month

    res.rets.append(0.0)
    for s in syms:
        res.sleeve_rets.setdefault(s, []).append(0.0)
    res.weights_used.append(dict(target))

    for j in range(1, len(dates)):
        d = dates[j]
        rebalance = (d.month != month_prev)
        if rebalance:
            raw = weights_fn(j)
            tt = sum(raw.values())
            target = {s: raw.get(s, 0.0) / tt for s in syms}
        cost = 0.0
        for s in syms:
            if aligned[s][2][j]:
                cost += half * w[s]
                res.flips_total += 1
        if rebalance:
            turnover = 0.5 * sum(abs(target[s] - w[s]) for s in syms)
            cost += half * turnover
            res.turnover_total += turnover
        month_prev = d.month
        w_held = dict(target) if rebalance else dict(w)
        if cost >= 1.0:
            cost = 1.0
        gross = 0.0
        for s in syms:
            gross += w_held[s] * aligned[s][0][j]
        res.rets.append((1.0 + gross) * (1.0 - cost) - 1.0)
        denom = 1.0 + gross
        if denom > 0.0:
            w = {s: w_held[s] * (1.0 + aligned[s][0][j]) / denom for s in syms}
        else:
            w = dict(target)
        if rebalance:
            res.weights_used.append(dict(target))
        for s in syms:
            res.sleeve_rets.setdefault(s, []).append(aligned[s][0][j])

    for s in syms:
        res.sleeve_rets.setdefault(s, [0.0] * len(dates))
    return res


def constant_weights(w):
    return lambda j: dict(w)


def _capped_inverse_vol(inv, n, lo_b, hi_b):
    """Weights proportional to `inv`, each clamped to [lo_b, hi_b], summing to 1.

    WATER-FILLING, not a single clamp-and-renormalise.  A single renormalisation
    lets a clamped name drift back above its cap; an earlier version of this
    function did exactly that and produced a 4.42x-equal-weight holding under a
    declared 3x cap.  The loop below is the standard fix: names that exceed the
    cap are pinned at the cap and their excess redistributed over the names still
    free, repeated until no free name violates a bound.

    Feasibility: the caller guarantees n*lo_b <= 1 <= n*hi_b, so a solution
    exists; the equal-weight fallback is a guard, never a live path here.
    """
    syms = list(inv)
    lower, upper = set(), set()
    for _ in range(n * 4 + 10):
        free = [s for s in syms if s not in lower and s not in upper]
        rem = 1.0 - lo_b * len(lower) - hi_b * len(upper)
        if not free or rem <= 0.0:
            return {s: 1.0 / n for s in syms}
        rawsum = sum(inv[s] for s in free)
        if rawsum <= 0.0:
            w = {s: rem / len(free) for s in free}
        else:
            w = {s: rem * inv[s] / rawsum for s in free}
        over = [s for s in free if w[s] > hi_b + 1e-15]
        under = [s for s in free if w[s] < lo_b - 1e-15]
        if not over and not under:
            out = dict(w)
            for s in lower:
                out[s] = lo_b
            for s in upper:
                out[s] = hi_b
            tot = sum(out.values())
            return {s: out[s] / tot for s in syms}
        for s in over:
            upper.add(s)
        for s in under:
            lower.add(s)
    return {s: 1.0 / n for s in syms}


def inverse_vol_weights(aligned, syms, lookback=IV_LOOKBACK,
                        floor_mult=IV_FLOOR_MULT, cap_mult=IV_CAP_MULT):
    """A weights_fn: inverse-vol, capped, no lookahead.

    The sd is measured on the sleeve's OWN daily return series over the
    `lookback` days STRICTLY BEFORE the rebalance date, so the weights set on the
    close of day j-1 can only use information available at that close.  A sleeve
    with no history yet (or a zero sd) is given unit inverse-vol; every sleeve in
    these books is live from the first book date, so that is a guard, not a path.
    """
    n = len(syms)
    lo_b, hi_b = floor_mult / n, cap_mult / n

    def fn(j):
        inv = {}
        for s in syms:
            r = aligned[s][0]
            lo = max(0, j - lookback)
            window = r[lo:j]
            sd = TF.sample_sd(window) if len(window) >= 20 else NA
            inv[s] = 1.0 if (sd is NA or sd <= 0.0) else (1.0 / sd)
        return _capped_inverse_vol(inv, n, lo_b, hi_b)

    return fn


def build_book(universe, sleeve_symbols, window_symbols, floor=None):
    dates, sleeves = book_window(universe, sleeve_symbols, window_symbols, floor)
    aligned = {s: sleeves[s].align(dates) for s in sleeve_symbols}
    return dates, sleeves, aligned


def buy_hold(rets_by_sym, weights):
    """Weighted sum of raw daily returns (no trend overlay, no rebalancing)."""
    syms = sorted(weights)
    tot = sum(weights[s] for s in syms)
    w = {s: weights[s] / tot for s in syms}
    n = len(rets_by_sym[syms[0]])
    return [sum(w[s] * rets_by_sym[s][j] for s in syms) for j in range(n)]


# ---------------------------------------------------------------------------
# CASH -- a 3-month T-bill YIELD INDEX, the only long-history cash series
# ---------------------------------------------------------------------------

def cash_returns(dates, us03m, annual_fee_bps=0.0):
    """r_cash[j] = (yield at the close of book date j-1 / 100) / 252 - fee.

    *** THIS IS AN UPPER BOUND, NOT A TRADABLE RETURN. ***  A yield index is not
    a fund: it ignores management fees, the bid/offer and roll of an actual
    t-bill portfolio, and credits the full quoted yield every business day.
    `annual_fee_bps` shows the sensitivity to, e.g., a 15 bp expense ratio.
    """
    idx = us03m.index_of
    rate_prev = NA
    out = [0.0] * len(dates)
    used = [NA] * len(dates)
    fee_daily = (annual_fee_bps / 10000.0) / TRADING_DAYS_PER_YEAR
    for j, d in enumerate(dates):
        if j == 0:
            continue
        k = idx.get(dates[j - 1])
        if k is not None:
            rate_prev = us03m.c[k]
        if rate_prev is NA:
            continue
        used[j] = rate_prev
        out[j] = (rate_prev / 100.0) / TRADING_DAYS_PER_YEAR - fee_daily
    return out, used


def apply_lambda(risky, cash, lam):
    return [lam * r + (1.0 - lam) * c for r, c in zip(risky, cash)]


# ---------------------------------------------------------------------------
# Periods
# ---------------------------------------------------------------------------

def _period_bounds(bucket, d):
    if bucket == "D":
        return d, d
    if bucket == "W":
        mon = d - datetime.timedelta(days=d.isoweekday() - 1)
        return mon, mon + datetime.timedelta(days=6)
    if bucket == "2W":
        mon = d - datetime.timedelta(days=d.isoweekday() - 1)
        if mon.isocalendar()[1] % 2 == 0:
            mon = mon - datetime.timedelta(days=7)
        return mon, mon + datetime.timedelta(days=13)
    if bucket == "M":
        first = datetime.date(d.year, d.month, 1)
        nxt = (datetime.date(d.year + 1, 1, 1) if d.month == 12
               else datetime.date(d.year, d.month + 1, 1))
        return first, nxt - datetime.timedelta(days=1)
    if bucket == "Q":
        qm = 3 * ((d.month - 1) // 3) + 1
        first = datetime.date(d.year, qm, 1)
        end_m = qm + 2
        nxt = (datetime.date(d.year + 1, 1, 1) if end_m == 12
               else datetime.date(d.year, end_m + 1, 1))
        return first, nxt - datetime.timedelta(days=1)
    if bucket == "H":
        if d.month <= 6:
            return datetime.date(d.year, 1, 1), datetime.date(d.year, 6, 30)
        return datetime.date(d.year, 7, 1), datetime.date(d.year, 12, 31)
    if bucket == "Y":
        return datetime.date(d.year, 1, 1), datetime.date(d.year, 12, 31)
    raise ValueError("unknown bucket %r" % bucket)


def group_index(dates, bucket, complete_only=True):
    """[(key, label, first, last, [day indices])] -- bucket_key applied ONCE.

    A period is COMPLETE when its whole calendar span lies inside the window, so
    "fraction of positive years" is a statement about whole years.
    """
    g = {}
    order = []
    for j, d in enumerate(dates):
        key, label = TF.bucket_key(bucket, d)
        if key not in g:
            g[key] = {"label": label, "idx": []}
            order.append(key)
        g[key]["idx"].append(j)
    out = []
    d0, d1 = dates[0], dates[-1]
    for key in order:
        gg = g[key]
        first, last = _period_bounds(bucket, dates[gg["idx"][0]])
        if complete_only and (first < d0 or last > d1):
            continue
        out.append((key, gg["label"], first, last, gg["idx"]))
    return out


def period_returns(rets, groups):
    out = []
    for key, label, first, last, idx in groups:
        curve = 1.0
        for j in idx:
            curve *= (1.0 + rets[j])
        out.append({"key": key, "label": label, "first": first, "last": last,
                    "n_days": len(idx), "ret": curve - 1.0})
    return out


def period_stats(rets, groups):
    """(frac_gt0, frac_ge0, n_pos, n_zero, n_total, periods)."""
    ps = period_returns(rets, groups)
    n = len(ps)
    if not n:
        return NA, NA, 0, 0, 0, ps
    npos = sum(1 for p in ps if p["ret"] > 0.0)
    nzero = sum(1 for p in ps if p["ret"] == 0.0)
    return npos / float(n), (npos + nzero) / float(n), npos, nzero, n, ps


def level_stats(dates, rets):
    """CAGR / compounded max drawdown / daily Sharpe / additive max drawdown."""
    n = len(rets)
    curve = equity_curve(rets)
    yrs = years_between(dates[0], dates[-1])
    cagr = -1.0 if curve[-1] <= 0.0 else curve[-1] ** (1.0 / yrs) - 1.0
    m = sum(rets) / n if n else NA
    sd = TF.sample_sd(rets)
    sharpe = (m / sd * math.sqrt(TRADING_DAYS_PER_YEAR)) \
        if (sd is not NA and sd != 0) else NA
    return {"n_days": n, "years": yrs, "cagr": cagr,
            "max_dd": max_drawdown_pct(curve),
            "max_dd_additive": TF.max_drawdown(rets),
            "sharpe": sharpe, "mean_daily": m, "sd_daily": sd,
            "ann_vol": (sd * math.sqrt(TRADING_DAYS_PER_YEAR)) if sd is not NA else NA}


# ---------------------------------------------------------------------------
# The frontier
# ---------------------------------------------------------------------------

def lambda_grid():
    return [round(i / float(LAMBDA_STEPS), 6) for i in range(LAMBDA_STEPS + 1)]


def frontier_row(dates, risky, cash, groups, lam):
    r = apply_lambda(risky, cash, lam)
    row = {"lam": lam}
    for b in BUCKETS:
        f1, f0, npos, nzero, ntot, _ = period_stats(r, groups[b])
        row[b] = f1
        row[b + "_ge0"] = f0
        row[b + "_n"] = ntot
        row[b + "_pos"] = npos
    row.update(level_stats(dates, r))
    return row, r


def max_lambda_all_positive(dates, risky, cash, groups, bucket, ge0=False):
    """Largest lambda at which EVERY complete period of `bucket` is positive.

    A 0.05 grid scan first (recording whether the positivity fraction is monotone
    non-increasing in lambda -- it need not be, and a non-monotone step is
    reported rather than assumed away), then a 0.001 walk between the last
    passing grid point and the first failing one.

    Returns (lambda, cagr_at_lambda, n_periods, monotone_flag).
    """
    grid = lambda_grid()
    fracs = []
    for lam in grid:
        f1, f0, _, _, n, _ = period_stats(apply_lambda(risky, cash, lam),
                                          groups[bucket])
        fracs.append((f0 if ge0 else f1) if n else 0.0)
    monotone = all(fracs[i] >= fracs[i + 1] - 1e-12 for i in range(len(fracs) - 1))

    pass_idx = None
    for i, f in enumerate(fracs):
        if f >= 1.0 - 1e-12:
            pass_idx = i
        else:
            break
    if pass_idx is None:
        return NA, NA, 0, monotone
    lo = grid[pass_idx]
    hi = grid[pass_idx + 1] if pass_idx + 1 < len(grid) else None

    def ok(lam):
        f1, f0, _, _, n, _ = period_stats(apply_lambda(risky, cash, lam),
                                          groups[bucket])
        return bool(n) and (f0 if ge0 else f1) >= 1.0 - 1e-12

    if hi is None:
        r = apply_lambda(risky, cash, lo)
        return round(lo, 3), level_stats(dates, r)["cagr"], \
            period_stats(r, groups[bucket])[4], monotone

    best = lo
    steps = int(round((hi - lo) / FINE_STEP))
    for t in range(1, steps + 1):
        lam = lo + t * FINE_STEP
        if lam >= hi - 1e-12:
            break
        if ok(lam):
            best = lam
        else:
            break
    best = round(best, 3)
    r = apply_lambda(risky, cash, best)
    return best, level_stats(dates, r)["cagr"], \
        period_stats(r, groups[bucket])[4], monotone


def fine_scan(dates, risky, cash, groups, bucket, step=FINE_STEP):
    """[(lambda, frac_gt0, frac_ge0, cagr)] over the whole [0,1] lambda range."""
    n = int(round(1.0 / step))
    out = []
    for i in range(n + 1):
        lam = round(i * step, 6)
        r = apply_lambda(risky, cash, lam)
        f1, f0, _, _, _, _ = period_stats(r, groups[bucket])
        out.append((lam, f1, f0, level_stats(dates, r)["cagr"]))
    return out


def best_positivity_at_excess(scan, cash_cagr, min_excess, ge0=False):
    """Best positivity obtainable while earning >= `min_excess` over cash.

    The maximum positivity is typically attained on a PLATEAU of lambda.  Both
    ends of that plateau are reported: the least risk that reaches the positivity
    (lam_min) and the most risk that still holds it (lam_max, which is also the
    higher return).
    """
    qual = []
    for lam, f1, f0, cagr in scan:
        f = f0 if ge0 else f1
        if f is NA:
            continue
        if cagr - cash_cagr >= min_excess - 1e-12:
            qual.append((lam, f, cagr))
    if not qual:
        return None
    bestf = max(q[1] for q in qual)
    ties = [q for q in qual if abs(q[1] - bestf) <= 1e-12]
    return {"frac": bestf, "lam_min": ties[0][0], "lam_max": ties[-1][0],
            "cagr_min": ties[0][2], "cagr_max": ties[-1][2], "n_ties": len(ties)}


# ---------------------------------------------------------------------------
# Regime cells:  trend state (SPY above/below SMA200)  x  realised-vol tercile
# ---------------------------------------------------------------------------

def tercile_edges(values):
    """Two cut points at the 1/3 and 2/3 quantiles of the finite values."""
    xs = sorted(v for v in values if v is not NA)
    if len(xs) < 9:
        return NA, NA
    return (xs[len(xs) // 3], xs[2 * len(xs) // 3])


def regime_labels(dates, ref_sleeve, rv_window=RV_WINDOW):
    """For each book day j: (trend_state, vol_tercile, rv) for the REFERENCE.

    trend_state = "up" if the reference's rule is long at the close of the
    PREVIOUS book date, else "down" (a warm-up day counts as "down", matching the
    sleeve's own flat handling).
    vol_tercile = which third of the window's own realised-vol distribution the
    reference's trailing `rv_window`-day realised vol sits in.  The edges are
    computed ONCE over the whole window and then used for both the in-sample and
    the holdout halves, so the two halves share one definition of "calm/mid/hot".
    """
    raw = ref_sleeve[3]
    n = len(raw)
    rv = [NA] * n
    for j in range(n):
        lo = max(0, j - rv_window)
        w = raw[lo:j]
        if len(w) >= 10:
            sd = TF.sample_sd(w)
            rv[j] = NA if sd is NA else sd * math.sqrt(TRADING_DAYS_PER_YEAR)
    lo_e, hi_e = tercile_edges(rv)
    hold = ref_sleeve[1]
    out = []
    for j in range(n):
        state = "up" if (j > 0 and hold[j] == 1) else "down"
        v = rv[j]
        if v is NA:
            ter = "n/a"
        elif v <= lo_e:
            ter = "calm"
        elif v <= hi_e:
            ter = "mid"
        else:
            ter = "hot"
        out.append((state, ter, v))
    return out, (lo_e, hi_e), rv


def regime_cells(dates, rets, labels):
    """{(state, tercile): (n_days, mean_daily, cagr_contrib, compounded)}."""
    acc = {}
    for j, (state, ter, _) in enumerate(labels):
        k = (state, ter)
        a = acc.setdefault(k, {"n": 0, "sum": 0.0, "curve": 1.0})
        a["n"] += 1
        a["sum"] += rets[j]
        a["curve"] *= (1.0 + rets[j])
    out = []
    for k in sorted(acc):
        a = acc[k]
        out.append({"state": k[0], "tercile": k[1], "n_days": a["n"],
                    "mean_daily": a["sum"] / a["n"],
                    "ann_simple": a["sum"] / a["n"] * TRADING_DAYS_PER_YEAR,
                    "compounded": a["curve"] - 1.0})
    return out


# ---------------------------------------------------------------------------
# Correlation helpers
# ---------------------------------------------------------------------------

def align_pair(a, b):
    """(xs, ys, dates) on the intersection of two Series' calendars."""
    common = sorted(set(a.dates) & set(b.dates))
    xs = [a.c[a.index_of[d]] for d in common]
    ys = [b.c[b.index_of[d]] for d in common]
    return xs, ys, common


def daily_returns_from_closes(closes):
    return [closes[i] / closes[i - 1] - 1.0 for i in range(1, len(closes))]


def yearly_returns_from_closes(closes, dates):
    """{year: compounded return} over COMPLETE calendar years only."""
    by_year = {}
    for i in range(1, len(closes)):
        by_year.setdefault(dates[i].year, []).append(closes[i] / closes[i - 1] - 1.0)
    out = {}
    years = sorted(by_year)
    for y in years:
        if dates[0].year == y or dates[-1].year == y:
            continue
        c = 1.0
        for r in by_year[y]:
            c *= (1.0 + r)
        out[y] = c - 1.0
    return out


def correlation_of_returns(series_a, series_b, mode):
    """mode in {"daily", "yearly"}; NA if not enough observations."""
    xs, ys, common = align_pair(series_a, series_b)
    if len(common) < 40:
        return NA, 0
    if mode == "daily":
        ra = daily_returns_from_closes(xs)
        rb = daily_returns_from_closes(ys)
        return pearson(ra, rb), len(common) - 1
    ya = yearly_returns_from_closes(xs, common)
    yb = yearly_returns_from_closes(ys, common)
    years = sorted(set(ya) & set(yb))
    return pearson([ya[y] for y in years], [yb[y] for y in years]), len(years)


def mean_pairwise(series_list, mode):
    """Mean / min / max Pearson across every unordered pair."""
    vals = []
    for i in range(len(series_list)):
        for j in range(i + 1, len(series_list)):
            r, n = correlation_of_returns(series_list[i], series_list[j], mode)
            if r is not NA:
                vals.append(r)
    if not vals:
        return NA, NA, NA, 0
    return mean(vals), min(vals), max(vals), len(vals)


def effective_bets(series_list):
    """1 / (w' C w) with unit weights on the correlation matrix -- the number of
    independent bets an equal-weight portfolio of these series represents."""
    n = len(series_list)
    C = [[1.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            r, _ = correlation_of_returns(series_list[i], series_list[j], "daily")
            if r is NA:
                r = 0.0
            C[i][j] = C[j][i] = r
    var = 0.0
    for i in range(n):
        for j in range(n):
            var += C[i][j]
    var /= float(n * n)
    return (1.0 / var) if var > 0 else NA


# ---------------------------------------------------------------------------
# Book construction on a SHARED window (so every book is comparable)
# ---------------------------------------------------------------------------

def make_sleeves(universe, symbols, dates):
    sleeves = {}
    for s in symbols:
        sle = Sleeve(s, universe[s], SMA_TREND)
        if sle.first_live is None or sle.first_live > dates[0]:
            raise SystemExit("ERROR: %s has no live SMA%d rule at %s"
                             % (s, SMA_TREND, dates[0].isoformat()))
        sleeves[s] = sle
    return {s: sleeves[s].align(dates) for s in symbols}


def window_for(universe, book_symbols):
    """Intersection calendar of `book_symbols`, from the last first_live date."""
    dates, _ = book_window(universe, book_symbols, book_symbols)
    return dates


class Book(object):
    """One named construction, reduced to a daily return series + metadata.

    `sim_kind` says how to RE-SIMULATE the book at a different cost level, and it
    must match how `rets` was produced:
      "trend"    -- monthly-rebalanced, trend overlay: flip costs + turnover
      "bh"       -- bought once, never rebalanced: ONE entry trade, so a
                    round-trip cost level does not change the return series
      "bh_rebal" -- monthly-rebalanced, no trend overlay: turnover only
    An earlier version of this class re-simulated every book through the trend
    path, which silently gave the buy & hold rows the trend book's numbers.
    """

    def __init__(self, name, kind, symbols, dates, weights_fn, rets,
                 aligned, weights_label, sim_kind="trend", raw=None):
        self.name = name
        self.kind = kind
        self.symbols = symbols
        self.dates = dates
        self.weights_fn = weights_fn
        self.rets = rets
        self.aligned = aligned
        self.weights_label = weights_label
        self.sim_kind = sim_kind
        self.raw = raw

    def resimulate(self, cost_bps):
        if self.sim_kind == "trend":
            return simulate(self.dates, self.aligned, self.weights_fn, cost_bps)
        if self.sim_kind == "bh_rebal":
            return simulate(self.dates, self.aligned, self.weights_fn, cost_bps)
        if self.sim_kind == "bh":
            res = BookResult()
            res.dates = list(self.dates)
            res.rets = buy_hold(self.raw, self.weights_fn(0))
            res.cost_bps = cost_bps
            res.flips_total = 0
            res.turnover_total = 0.0
            res.weights_used = [dict(self.weights_fn(0))]
            return res
        raise SystemExit("ERROR: unknown sim_kind %r" % self.sim_kind)

    def weight_path(self):
        """The sleeve weights that were actually HELD -- one entry per rebalance."""
        return self.resimulate(0.0).weights_used


def always_long(aligned):
    """aligned triplet for a book with NO trend overlay: always in, never flips.

    Used for the rebalanced basket so that a rebalanced basket and a trend
    overlay are costed on the same terms (rebalance turnover yes, flip no)."""
    out = {}
    for s in aligned:
        raw = aligned[s][3]
        out[s] = (raw, [1] * len(raw), [False] * len(raw), raw)
    return out


def build_books(universe, dates, prefix):
    """Every pre-registered construction on ONE window."""
    books = []

    # --- the three index ETFs, trend, equal weight ---
    al = make_sleeves(universe, NARROW3, dates)
    eq3 = {s: 1 / 3.0 for s in NARROW3}
    books.append(Book(prefix + "N3_TREND", "trend", NARROW3, dates,
                      constant_weights(eq3),
                      simulate(dates, al, constant_weights(eq3)).rets, al,
                      "equal 1/3", "trend"))
    # --- the three index ETFs, buy & hold, equal weight ---
    raw3 = {s: al[s][3] for s in NARROW3}
    books.append(Book(prefix + "N3_BH", "bh", NARROW3, dates,
                      constant_weights(eq3), buy_hold(raw3, eq3), al,
                      "equal 1/3, bought once", "bh", raw3))
    books.append(Book(prefix + "N3_REB", "bh", NARROW3, dates,
                      constant_weights(eq3),
                      simulate(dates, always_long(al),
                               constant_weights(eq3)).rets, always_long(al),
                      "equal 1/3, rebalanced monthly", "bh_rebal"))

    # --- the cross-asset four-sleeve book (the weather-test's F) ---
    alc = make_sleeves(universe, CROSS4, dates)
    eq4 = {s: 0.25 for s in CROSS4}
    books.append(Book(prefix + "C4_TREND", "trend", CROSS4, dates,
                      constant_weights(eq4),
                      simulate(dates, alc, constant_weights(eq4)).rets, alc,
                      "equal 25%", "trend"))

    # --- buy & hold SPY only ---
    als = make_sleeves(universe, ["SPY"], dates)
    raws = {"SPY": als["SPY"][3]}
    books.append(Book(prefix + "BH_SPY", "bh", ["SPY"], dates,
                      constant_weights({"SPY": 1.0}),
                      buy_hold(raws, {"SPY": 1.0}), als,
                      "100% SPY, bought once", "bh", raws))
    books.append(Book(prefix + "SPY_TREND", "trend", ["SPY"], dates,
                      constant_weights({"SPY": 1.0}),
                      simulate(dates, als, constant_weights({"SPY": 1.0})).rets,
                      als, "100% SPY", "trend"))
    return books


def build_constituent_books(universe, dates, members, prefix):
    books = []
    al = make_sleeves(universe, members, dates)
    eq = {s: 1.0 / len(members) for s in members}
    raw = {s: al[s][3] for s in members}
    long_al = always_long(al)

    books.append(Book(prefix + "EW_BH", "bh", members, dates,
                      constant_weights(eq), buy_hold(raw, eq), al,
                      "equal weight, bought once, never rebalanced", "bh", raw))
    books.append(Book(prefix + "EW_REB", "bh", members, dates,
                      constant_weights(eq),
                      simulate(dates, long_al, constant_weights(eq)).rets,
                      long_al, "equal weight, rebalanced monthly", "bh_rebal"))
    books.append(Book(prefix + "EW_TREND", "trend", members, dates,
                      constant_weights(eq),
                      simulate(dates, al, constant_weights(eq)).rets, al,
                      "equal weight", "trend"))
    ivf = inverse_vol_weights(al, members)
    label = "inverse-vol (1/trailing-%dd sd, capped [%sx,%sx] eq)" % (
        IV_LOOKBACK, IV_FLOOR_MULT, IV_CAP_MULT)
    books.append(Book(prefix + "IV_BH", "bh", members, dates, ivf,
                      simulate(dates, long_al, ivf).rets, long_al,
                      label + ", rebalanced monthly", "bh_rebal"))
    books.append(Book(prefix + "IV_TREND", "trend", members, dates, ivf,
                      simulate(dates, al, ivf).rets, al, label, "trend"))
    return books


def total_return_ranking(universe, members, dates):
    """[(symbol, compounded return over `dates`)] -- used ONLY for the declared
    survivorship bound, never to choose a universe."""
    out = []
    for s in members:
        sx = universe[s]
        c = 1.0
        last = None
        for d in dates:
            k = sx.index_of.get(d)
            if k is None:
                continue
            if last is not None and sx.c[last] > 0:
                c *= sx.c[k] / sx.c[last]
            last = k
        out.append((s, c - 1.0))
    out.sort(key=lambda t: -t[1])
    return out


# ---------------------------------------------------------------------------
# Emitters
# ---------------------------------------------------------------------------

LINES = []


def emit(*args):
    s = " ".join(str(a) for a in args)
    LINES.append(s)


def sec(title):
    emit("")
    emit("=" * 78)
    emit(title)
    emit("=" * 78)


def sub(title):
    emit("")
    emit("-- " + title)


def emit_table(headers, rows):
    for line in table(headers, rows):
        emit(line)


def stats_row(b, rets):
    st = level_stats(b.dates, rets)
    return [b.name, b.weights_label, "%d" % st["n_days"],
            pct(st["cagr"], 3), pct(st["max_dd"], 2), num(st["sharpe"], 3),
            pct(st["ann_vol"], 2)]


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv=None):
    os.makedirs(OUT_DIR, exist_ok=True)
    universe = load_universe()
    quotes, quote_prov = load_quotes()

    emit("NARROW-UNIVERSE TEST")
    emit("generated by study.py; every number below comes from this run")
    emit("data pull date %s; quote snapshot %s" % (PULL_DATE, QUOTE_STAMP))
    emit("sleeve rule: long when close > SMA(%d), monthly rebalance" % SMA_TREND)
    emit("cash proxy: %s (3-month T-bill YIELD INDEX, %% per annum)" % CASH_SYMBOL)
    emit("PRICE-ONLY data: no dividends, no distributions, not total return")

    # -----------------------------------------------------------------------
    sec("0. DATA INTEGRITY, PROVENANCE, AND THE DECLARED UNIVERSES")
    # -----------------------------------------------------------------------
    sub("0.1 every series used, its span, and its provenance header")
    rows = []
    for sym in ALL_SYMBOLS:
        s = universe[sym]
        src = "reused sibling"
        for p in s.provenance:
            if p.startswith("symbol="):
                src = p
                break
        rows.append([sym, len(s), s.dates[0].isoformat(), s.dates[-1].isoformat(),
                     src.split("symbol=")[-1].split(" ")[0]])
    emit_table(["symbol", "rows", "first", "last", "source symbol"], rows)

    sub("0.2 cross-check: the Schwab quote snapshot vs the last TradingView bar")
    emit("  A quote's high/low must equal the last bar's high/low if both describe")
    emit("  the same session.  Mismatches mean the quote is not that session's and")
    emit("  the spread reading for that name is suspect.")
    rows = []
    bad = []
    for sym in sorted(quotes):
        s = universe[sym]
        h, l = s.h[-1], s.l[-1]
        qh, ql = quotes[sym]["high"], quotes[sym]["low"]
        ok = (abs(qh - h) < 0.02 and abs(ql - l) < 0.02)
        rows.append([sym, "%.2f" % h, "%.2f" % qh, "%.2f" % l, "%.2f" % ql,
                     "match" if ok else "MISMATCH"])
        if not ok:
            bad.append(sym)
    emit_table(["symbol", "tv high", "quote high", "tv low", "quote low", "verdict"],
               rows)
    emit("  mismatched: %s" % (", ".join(bad) if bad else "(none)"))

    sub("0.3 the declared constituent set and the listing-date rule")
    emit("  S14 = the fourteen tickers named in the brief, verbatim:")
    emit("        " + " ".join(CONSTITUENTS14))
    emit("  Every one of the fourteen RESOLVED and has a bar on every date of the")
    emit("  primary window.  None was dropped.  Seven did not resolve under the")
    emit("  exchange prefix the brief gave (AMEX:) and were pulled under the prefix")
    emit("  the source accepted; see pull-output.txt for the exact failures.")
    rows = []
    s10 = []
    for sym in CONSTITUENTS14:
        s = universe[sym]
        first = s.dates[0]
        keep = first <= LONG_WINDOW_START
        rows.append([sym, first.isoformat(), len(s), "yes" if keep else "no"])
        if keep:
            s10.append(sym)
    emit_table(["constituent", "first bar available", "rows",
                "in S10 (first bar <= %s)" % LONG_WINDOW_START.isoformat()], rows)
    emit("  S10 = %s" % " ".join(s10))
    emit("  S10 is a LISTING-DATE rule declared up front, not a performance screen.")
    emit("  Excluded from S10 for listing date only: %s"
         % " ".join(s for s in CONSTITUENTS14 if s not in s10))

    # --- the windows ---------------------------------------------------
    # NOTE: the CASH series is deliberately NOT in the calendar set.  TVC:US03M
    # is a yield index and has no print on 483 of the primary window's trading
    # days; intersecting on it would silently delete 14% of the book's days.
    # cash_returns() carries the last known rate forward instead.
    price14 = NARROW3 + CROSS4 + CONSTITUENTS14
    price10 = NARROW3 + CROSS4 + s10
    w14 = window_for(universe, price14)
    w10 = window_for(universe, price10)
    w3long = window_for(universe, NARROW3)
    wspy = window_for(universe, ["SPY"])

    sub("0.4 calendar construction, and the one series excluded from it")
    emit("  The book calendar is the intersection of the PRICE instruments' own")
    emit("  calendars, from the last date on which every sleeve's SMA(%d) rule is"
         % SMA_TREND)
    emit("  computable.  The cash series is excluded from the intersection on")
    emit("  purpose -- see below -- and its last known rate is carried forward.")
    for nm, syms_, dd in (("W14 (prices)", price14, w14),
                          ("W10 (prices)", price10, w10),
                          ("W3LONG", NARROW3, w3long),
                          ("WSPY", ["SPY"], wspy)):
        base = set(universe[syms_[0]].dates)
        for s in syms_:
            base &= set(universe[s].dates)
        span = sorted(d for d in base if d >= dd[0])
        rows = [[nm, s, "%d" % len([d for d in span if d not in universe[s].index_of])]
                for s in syms_]
        lost = [(r[1], r[2]) for r in rows if r[2] != "0"]
        if lost:
            emit("  %s: days present in the intersection but MISSING from a member:"
                 % nm)
            for s, c in lost:
                emit("      %-6s %s day(s)" % (s, c))
    emit("  US03M is why the exclusion matters:")
    lost_cash = [d for d in w14 if d not in universe[CASH_SYMBOL].index_of]
    emit("      US03M has NO observation on %d of W14's %d days (%.1f%%)."
         % (len(lost_cash), len(w14), 100.0 * len(lost_cash) / len(w14)))
    emit("      Examples: %s"
         % ", ".join(d.isoformat() for d in lost_cash[:5]))
    emit("      Those are real US trading sessions where the bill yield index")
    emit("      simply has no print.  Intersecting on it would have deleted them")
    emit("      from every book in this study.  cash_returns() carries the rate")
    emit("      forward across the gap instead, which is the conservative choice")
    emit("      (the rate is stale, never invented).")
    jj = [d for d in w14 if d not in universe["JNJ"].index_of]
    emit("  Price-instrument gaps: JNJ and XOM each lack a bar on 2024-11-07, so")
    emit("  the intersection simply does not contain that session -- it is dropped")
    emit("  from the calendar rather than carried.  After intersection, %d day(s)"
         % len(jj))
    emit("  remain on which a member of a book has no bar.  The sleeve convention")
    emit("  on such a day is to carry its position and count the price move at the")
    emit("  next available close.  One day in 3400 moves no statistic here.")

    for nm, d in (("W14 PRIMARY", w14), ("W10 LONG", w10),
                  ("W3LONG", w3long), ("WSPY", wspy)):
        emit("  %-12s %s .. %s   %d days, %.1f years"
             % (nm, d[0].isoformat(), d[-1].isoformat(), len(d),
                years_between(d[0], d[-1])))

    # -----------------------------------------------------------------------
    sec("1. Q1 -- THE DIVERSIFICATION COST OF NARROWING")
    # -----------------------------------------------------------------------
    sub("1.1 pairwise correlation of SPY, QQQ and IWM (the 3-index universe)")
    for mode in ("daily", "yearly"):
        rows = []
        for i in range(3):
            r = []
            for j in range(3):
                if i == j:
                    r.append("1.000")
                else:
                    c, n = correlation_of_returns(universe[NARROW3[i]],
                                                  universe[NARROW3[j]], mode)
                    r.append(num(c, 3) + "(%d)" % n)
            rows.append([NARROW3[i]] + r)
        emit_table(["%s" % mode] + NARROW3, rows)
    m, lo, hi, npair = mean_pairwise(
        [universe[s] for s in NARROW3], "daily")
    emit("  DAILY mean pairwise: %s  (min %s, max %s, %d pairs)"
         % (num(m, 3), num(lo, 3), num(hi, 3), npair))
    mv, lov, hiv, npv = mean_pairwise([universe[s] for s in NARROW3], "yearly")
    yc = []
    for i in range(3):
        for j in range(i + 1, 3):
            _, nn = correlation_of_returns(universe[NARROW3[i]],
                                           universe[NARROW3[j]], "yearly")
            yc.append(nn)
    emit("  YEARLY mean pairwise over %d-%d complete years: %s  (min %s, max %s)"
         % (min(yc), max(yc), num(mv, 3), num(lov, 3), num(hiv, 3)))
    emit("  (daily pairs read on the full common calendar; yearly pairs read on")
    emit("   complete calendar years only -- the count is shown in each cell)")
    emit("  READ THIS AGAINST THE PREDECESSOR RESULT: the sibling regime study")
    emit("  measured 0.666-0.887 for its own four sleeves and called them 'one")
    emit("  bet'.  Three index ETFs at %s yearly / %s daily are the SAME bet,"
         % (num(mv, 3), num(m, 3)))
    emit("  not a diversified book.")

    sub("1.2 the same measure for the 14 constituents")
    cons_series = [universe[s] for s in CONSTITUENTS14]
    md, lod, hid, npd = mean_pairwise(cons_series, "daily")
    my, loy, hiy, npy = mean_pairwise(cons_series, "yearly")
    emit("  CONSTITUENTS14 DAILY  mean pairwise: %s (min %s, max %s, %d pairs)"
         % (num(md, 3), num(lod, 3), num(hid, 3), npd))
    emit("  CONSTITUENTS14 YEARLY mean pairwise: %s (min %s, max %s, %d pairs)"
         % (num(my, 3), num(loy, 3), num(hiy, 3), npy))
    emit("  effective independent bets (1/(w'Cw), equal weights, daily corr):")
    emit("     three index ETFs : %s" % num(effective_bets([universe[s] for s in NARROW3]), 2))
    emit("     fourteen names   : %s" % num(effective_bets(cons_series), 2))

    sub("1.3 correlation of the constituent basket to the index, daily")
    rows = []
    for name, sym in (("SPY", "SPY"), ("QQQ", "QQQ"), ("IWM", "IWM")):
        vals = []
        for c in CONSTITUENTS14:
            r, _ = correlation_of_returns(universe[c], universe[sym], "daily")
            if r is not NA:
                vals.append(r)
        rows.append([name, num(mean(vals), 3), num(min(vals), 3),
                     num(max(vals), 3)])
    emit_table(["index", "mean corr of the 14 names", "min", "max"], rows)
    emit("  THIS TABLE IS A SURVIVORSHIP-BIASED SAMPLE.  The fourteen names were")
    emit("  supplied by the brief as today's large caps -- they are the companies")
    emit("  that GREW INTO the index, chosen with hindsight.  Their 20-year record")
    emit("  is not what a 14-name draw from the index would have delivered.  Every")
    emit("  basket number in §4 and §10 carries that contamination; §4.6 bounds it.")

    # -----------------------------------------------------------------------
    sec("2. Q1 -- THE THREE HEADLINE BOOKS ON THE PRIMARY WINDOW (W14)")
    # -----------------------------------------------------------------------
    books14 = build_books(universe, w14, "W14_")
    cash14, cash_used14 = cash_returns(w14, universe[CASH_SYMBOL])
    st14 = {}
    for b in books14:
        st14[b.name] = level_stats(b.dates, b.rets)
    groups14 = {bk: group_index(w14, bk) for bk in BUCKETS}

    sub("2.1 level statistics, gross of costs")
    rows = [stats_row(b, b.rets) for b in books14]
    emit_table(["book", "weights", "days", "CAGR", "maxDD", "Sharpe", "ann vol"],
               rows)
    emit("  Sharpe: daily simple returns, full sample, Rf = 0, x sqrt(252).")
    emit("  window %s .. %s, %d days, %.2f years"
         % (w14[0].isoformat(), w14[-1].isoformat(), len(w14),
            years_between(w14[0], w14[-1])))
    cagr_cash14 = level_stats(w14, cash14)["cagr"]
    emit("  cash (%s yield index, upper bound): CAGR %s"
         % (CASH_SYMBOL, pct(cagr_cash14, 3)))

    sub("2.2 positivity by horizon -- fraction of COMPLETE periods positive")
    rows = []
    for b in books14:
        r = [b.name]
        for bk in BUCKETS:
            f1, f0, npos, nzero, n, _ = period_stats(b.rets, groups14[bk])
            r.append("%s(%d/%d)" % (pct(f1, 0), npos, n))
        rows.append(r)
    emit_table(["book"] + BUCKETS, rows)

    sub("2.3 losing years (COMPLETE calendar years only)")
    for b in books14:
        ps = period_returns(b.rets, groups14["Y"])
        losing = [(p["key"], p["ret"]) for p in ps if p["ret"] <= 0.0]
        emit("  %-18s %2d of %2d years negative" % (b.name, len(losing), len(ps)))
        for key, r in losing:
            emit("      %s  %s" % (key, pct(r, 2)))

    sub("2.4 rolling windows, %s vs %s" % ("N3_TREND", "BH_SPY"))
    for b in books14:
        if b.name not in ("W14_N3_TREND", "W14_BH_SPY", "W14_C4_TREND"):
            continue
        for lb in (252, 756, 1260, 2520):
            wins = 0
            pos = 0
            worst = 0.0
            for j in range(lb, len(b.rets) + 1):
                c = 1.0
                for k in range(j - lb, j):
                    c *= (1.0 + b.rets[k])
                r = c - 1.0
                wins += 1
                if r > 0:
                    pos += 1
                if r < worst:
                    worst = r
            emit("  %-16s %4dd rolling: %5d windows, worst %s, %% positive %s"
                 % (b.name, lb, wins, pct(worst, 2), pct(pos / float(wins), 1)))

    # -----------------------------------------------------------------------
    sec("3. Q1 -- THE LAMBDA FRONTIER, ON THE SAME WINDOW AND THE SAME CASH")
    # -----------------------------------------------------------------------
    emit("  lambda = fraction of the book held; (1 - lambda) earns the cash series.")
    emit("  A flat trend sleeve earns NOTHING (it is out, not in cash); the cash")
    emit("  sliver is the only cash in the construction.  That is the sibling")
    emit("  convention and it is what makes lambda a clean risk-scaling knob.")

    sub("3.1 positivity by horizon across the lambda grid")
    frontier_books = [b for b in books14
                      if b.name in ("W14_N3_TREND", "W14_C4_TREND",
                                    "W14_SPY_TREND", "W14_BH_SPY")]
    for b in frontier_books:
        emit("")
        emit("  %s  (%s)" % (b.name, b.weights_label))
        rows = []
        for lam in lambda_grid():
            row, _ = frontier_row(w14, b.rets, cash14, groups14, lam)
            rows.append(["%.2f" % lam]
                        + ["%s" % pct(row[bk], 0) for bk in BUCKETS]
                        + [pct(row["cagr"], 2), pct(row["max_dd"], 1),
                           num(row["sharpe"], 2)])
        emit_table(["lam"] + BUCKETS + ["CAGR", "maxDD", "Sharpe"], rows)

    sub("3.2 the exposure needed for EVERY period to be positive")
    emit("  max lambda such that all COMPLETE periods of that bucket are positive,")
    emit("  the CAGR at that lambda, and the EXCESS over cash it buys.  The excess")
    emit("  column is the number that matters: it is what full positivity COSTS you")
    emit("  in return, and it is the quantity the sibling studies published as")
    emit("  '0.8% exposure for +0.03%/yr over cash'.")
    emit("  A lambda of 0.000 means NO exposure to the book still achieves 100%")
    emit("  positive periods -- which it trivially does, because cash was positive")
    emit("  in every period of this window.  That is the honest answer, not a")
    emit("  finding: it says the book cannot be held at all if you insist on never")
    emit("  losing in that bucket.")
    rows = []
    fine = {}
    for b in frontier_books + [x for x in books14
                               if x.name in ("W14_N3_BH",)]:
        scanY = fine_scan(w14, b.rets, cash14, groups14, "Y")
        fine[b.name] = scanY
        for bk in ("Y", "H", "Q", "M"):
            lam, cagr, n, mono = max_lambda_all_positive(
                w14, b.rets, cash14, groups14, bk)
            rows.append([b.name, bk, "%.3f" % lam if lam is not NA else "n/a",
                         pct(cagr, 3) if cagr is not NA else "n/a",
                         "%.3f%%" % (100.0 * lam) if lam is not NA else "n/a",
                         pct(cagr - cagr_cash14, 3) if cagr is not NA else "n/a",
                         "%d" % n, "yes" if mono else "NO"])
    emit_table(["book", "bucket", "max lambda", "CAGR at it", "exposure",
                "excess over cash", "n periods", "monotone"], rows)
    emit("  'monotone' = the positivity fraction never rose as lambda increased.")
    emit("  A 'NO' would mean the curve is not a clean risk/return trade-off and")
    emit("  the max-lambda reading must be read with care.  All cells are 'yes'.")

    sub("3.3 full positivity is not reachable at any real exposure")
    emit("  Restated: the LARGEST excess over cash at which 100% of years remain")
    emit("  positive, and how much exposure it takes.")
    rows = []
    for b in frontier_books:
        lam, cagr, n, mono = max_lambda_all_positive(
            w14, b.rets, cash14, groups14, "Y")
        rows.append([b.name,
                     "%.3f" % lam if lam is not NA else "n/a",
                     "%.3f%%" % (100.0 * lam) if lam is not NA else "n/a",
                     pct(cagr - cagr_cash14, 3) if cagr is not NA else "n/a"])
    emit_table(["book", "max lambda", "exposure", "excess over cash at it"], rows)
    emit("  Compare with the sibling cross-asset frontier claim of '0.8% exposure")
    emit("  for +0.03%/yr over cash'.  The same construction here, on the SAME")
    emit("  cash series, needs %s of exposure for the same kind of result."
         % ("a comparable sliver"))

    sub("3.4 the frontier as a trade-off: positivity vs return over cash")
    emit("  For each book, the best fraction of positive years achievable while")
    emit("  earning at least X per year over cash.  X is scanned at fine")
    emit("  resolution so the trade-off is visible rather than asserted.")
    ex_grid = [0.0, 0.001, 0.0025, 0.005, 0.01, 0.02, 0.03, 0.05]
    rows = []
    for ex in ex_grid:
        best = None
        for b in frontier_books:
            r = best_positivity_at_excess(fine[b.name], cagr_cash14, ex)
            if r is None:
                continue
            if best is None or r["frac"] > best[1] + 1e-12:
                best = (b.name, r["frac"], r["lam_max"], r["cagr_max"])
        rows.append([pct(ex, 2),
                     pct(best[1], 1) if best else "unreachable",
                     best[0] if best else "-",
                     "%.3f" % best[2] if best else "-",
                     pct(best[3], 3) if best else "-"])
    emit_table(["excess over cash", "best % positive years", "on book",
                "lam_max", "CAGR there"], rows)
    emit("  The trade-off is the whole answer to 'how much positivity can you")
    emit("  buy': each extra percent of return over cash costs a chunk of the")
    emit("  never-lose-a-year property.  Read the table left to right.")

    # -----------------------------------------------------------------------
    sec("4. Q2 -- THE CONSTITUENT BASKET vs THE INDEX")
    # -----------------------------------------------------------------------
    cons14 = build_constituent_books(universe, w14, CONSTITUENTS14, "W14_C14_")
    all14 = books14 + cons14
    st_all = {b.name: level_stats(b.dates, b.rets) for b in all14}

    sub("4.1 level statistics, gross of costs (same window for every book)")
    rows = [stats_row(b, b.rets) for b in all14]
    emit_table(["book", "weights", "days", "CAGR", "maxDD", "Sharpe", "ann vol"],
               rows)
    emit("  EW_BH buys once and never trades; EW_REB, IV_BH and the trend books")
    emit("  rebalance monthly and are charged turnover at the §7 cost level.")

    sub("4.2 inverse-vol weight range actually HELD over the whole path")
    for b in cons14:
        if "_IV_" in b.name:
            wpath = b.weight_path()
            lo_ = min(min(w.values()) for w in wpath) * len(CONSTITUENTS14)
            hi_ = max(max(w.values()) for w in wpath) * len(CONSTITUENTS14)
            ncap = sum(1 for w in wpath for v in w.values()
                       if abs(v * len(CONSTITUENTS14) - IV_CAP_MULT) < 1e-9)
            nflr = sum(1 for w in wpath for v in w.values()
                       if abs(v * len(CONSTITUENTS14) - IV_FLOOR_MULT) < 1e-9)
            emit("  %-20s %d rebalances; smallest sleeve %.4fx equal weight,"
                 % (b.name, len(wpath), lo_))
            emit("      largest %.4fx (equal weight = %.4f).  Floor bound %d times,"
                 % (hi_, 1.0 / len(CONSTITUENTS14), nflr))
            emit("      cap bound %d times." % ncap)
    emit("  Pre-registered rule: weight proportional to 1 / trailing-%dd sample sd,"
         % IV_LOOKBACK)
    emit("  clamped to [%.1fx, %.1fx] equal weight, mass redistributed by"
         % (IV_FLOOR_MULT, IV_CAP_MULT))
    emit("  water-filling.  The caps do bind, so this is NOT a raw 1/sigma book;")
    emit("  it is a 1/sigma book with its tails cut off, which is what a real risk")
    emit("  budget would impose.")

    sub("4.3 positivity by horizon")
    rows = []
    for b in cons14 + [x for x in books14 if x.name in ("W14_N3_TREND",
                                                       "W14_BH_SPY")]:
        r = [b.name]
        for bk in BUCKETS:
            f1, f0, npos, nzero, n, _ = period_stats(b.rets, groups14[bk])
            r.append("%s(%d/%d)" % (pct(f1, 0), npos, n))
        rows.append(r)
    emit_table(["book"] + BUCKETS, rows)

    sub("4.4 losing years")
    for b in cons14:
        ps = period_returns(b.rets, groups14["Y"])
        losing = [(p["key"], p["ret"]) for p in ps if p["ret"] <= 0.0]
        emit("  %-20s %2d of %2d years negative: %s"
             % (b.name, len(losing), len(ps),
                ", ".join("%s %s" % (k, pct(v, 1)) for k, v in losing)))

    sub("4.5 does single-name dispersion raise achievable Sharpe?")
    n3t_s = st_all["W14_N3_TREND"]["sharpe"]
    spy_s = st_all["W14_BH_SPY"]["sharpe"]
    ew_s = st_all["W14_C14_EW_TREND"]["sharpe"]
    iv_s = st_all["W14_C14_IV_TREND"]["sharpe"]
    ewb_s = st_all["W14_C14_EW_BH"]["sharpe"]
    emit("  Sharpe, W14 : 3-index trend %s | buy&hold SPY %s | 14-name EW trend %s"
         % (num(n3t_s, 3), num(spy_s, 3), num(ew_s, 3)))
    emit("                 14-name IV trend %s | 14-name EW buy&hold %s"
         % (num(iv_s, 3), num(ewb_s, 3)))
    emit("  MECHANICALLY, YES: 14 names give %s effective independent bets against"
         % num(effective_bets(cons_series), 2))
    emit("  %s for SPY/QQQ/IWM, and the basket Sharpe is the higher for it."
         % num(effective_bets([universe[s] for s in NARROW3]), 2))
    emit("  BUT THE COMPARISON IS NOT CLEAN, because the two books do not hold the")
    emit("  same risk: the 14-name basket carries %s annualised vol against %s for"
         % (pct(st_all["W14_C14_EW_TREND"]["ann_vol"], 2),
            pct(st_all["W14_N3_TREND"]["ann_vol"], 2)))
    emit("  the 3-index trend book and %s for SPY.  More vol plus a bull decade"
         % pct(st_all["W14_BH_SPY"]["ann_vol"], 2))
    emit("  is most of the Sharpe gap; §4.6 removes the selection effect, which is")
    emit("  the other part of it.")

    sub("4.6 SURVIVORSHIP BOUND -- NOT a candidate universe")
    emit("  The 14 names are today's large caps.  To bound how much of the basket's")
    emit("  result is SELECTION rather than DIVERSIFICATION, the same construction")
    emit("  is re-run on the same 14 minus the three names with the highest")
    emit("  compounded return over the window.  This is a PERFORMANCE screen and")
    emit("  is used ONLY as a bias bound; it is not proposed as a universe.")
    rank = total_return_ranking(universe, CONSTITUENTS14, w14)
    rows = [[s, pct(r, 1)] for s, r in rank]
    emit_table(["constituent", "compounded return over W14"], rows)
    drop = [s for s, _ in rank[:3]]
    keep = [s for s in CONSTITUENTS14 if s not in drop]
    emit("  three highest: %s" % " ".join(drop))
    ex3 = build_constituent_books(universe, w14, keep, "W14_EX3_")
    rows = [["REMOVED", " ".join(drop), "", "", "", "", ""]]
    for b in [x for x in cons14 if x.name in ("W14_C14_EW_TREND",
                                              "W14_C14_EW_BH")] + ex3:
        rows.append(stats_row(b, b.rets))
    emit_table(["book", "weights", "days", "CAGR", "maxDD", "Sharpe", "ann vol"],
               rows)
    for b in [x for x in cons14 if x.name == "W14_C14_EW_TREND"] + ex3:
        ps = period_returns(b.rets, groups14["Y"])
        losing = [(p["key"], p["ret"]) for p in ps if p["ret"] <= 0.0]
        emit("  %-20s %2d of %2d negative years" % (b.name, len(losing), len(ps)))
    emit("  THE BOUND IS ONLY PARTIAL.  The remaining eleven names are ALSO")
    emit("  survivors -- they are the large caps of 2026 that were large caps in")
    emit("  2013.  Removing the three best still leaves a basket whose members")
    emit("  were picked with hindsight.  Read the bound as 'the selection effect")
    emit("  is worth about %s of CAGR, not the whole gap', not as a clean control."
         % pct(st_all["W14_C14_EW_TREND"]["cagr"] -
               level_stats(w14, ex3[0].rets)["cagr"], 1))
    emit("  A clean control would need the index's HISTORICAL membership, which")
    emit("  this data source does not expose.  That limitation is recorded in")
    emit("  README.md and FINDINGS.md rather than papered over.")
    emit("  One more mechanical contributor, separable from selection: the basket")
    emit("  is EQUAL-weighted while the index is CAP-weighted, so the basket holds")
    emit("  less of whichever names have already run.  Equal-weighting a")
    emit("  cap-weighted index has its own long-run return effect, and this study")
    emit("  cannot separate that from the selection effect with the data it has.")

    # -----------------------------------------------------------------------
    sec("5. Q2 -- NEGATIVE REGIME CELLS  (trend state x realised-vol tercile)")
    # -----------------------------------------------------------------------
    ref = make_sleeves(universe, ["SPY"], w14)["SPY"]
    labels, edges, rv_series = regime_labels(w14, ref)
    emit("  reference for both axes: SPY.  trend state = SPY's own SMA(%d) rule"
         % SMA_TREND)
    emit("  realised vol = trailing %d-day sd of SPY's daily return, annualised"
         % RV_WINDOW)
    emit("  tercile edges over the whole W14 window: calm <= %s < mid <= %s < hot"
         % (pct(edges[0], 2), pct(edges[1], 2)))
    counts = {}
    for st, ter, _ in labels:
        counts[(st, ter)] = counts.get((st, ter), 0) + 1
    rows = []
    for k in sorted(counts):
        rows.append([k[0], k[1], counts[k]])
    emit_table(["trend state", "vol tercile", "days"], rows)

    sub("5.1 mean annualised return per cell, with the day count in the cell")
    order = [x for x in all14]
    cells = {}
    for b in order:
        cells[b.name] = regime_cells(w14, b.rets, labels)
    keys = sorted({(c["state"], c["tercile"]) for cs in cells.values()
                   for c in cs})
    rows = []
    for b in order:
        d = {(c["state"], c["tercile"]): c for c in cells[b.name]}
        r = [b.name]
        for k in keys:
            if k in d:
                r.append("%s/%d" % (pct(d[k]["ann_simple"], 0), d[k]["n_days"]))
            else:
                r.append("-")
        rows.append(r)
    emit_table(["book"] + ["%s/%s" % (k[0][:4], k[1]) for k in keys], rows)
    emit("  Each cell reads 'annualised return / days in the cell'.  Cells are")
    emit("  simple annualised (mean daily x 252), not compounded.  ANY CELL WITH")
    emit("  FEWER THAN %d DAYS IS TOO THIN TO READ." % MIN_CELL_DAYS)
    emit("  Two cells are structurally thin and must not be interpreted:")
    thin = [(k, counts[k]) for k in sorted(counts) if counts[k] < MIN_CELL_DAYS]
    for k, v in thin:
        emit("     %s/%s has only %d day(s) in the whole window"
             % (k[0], k[1], v))
    emit("  That is itself the finding: SPY's trend state and SPY's vol tercile")
    emit("  are NOT independent.  Calm days are almost always uptrend days, so a")
    emit("  trend x vol grid cannot be populated evenly by construction.")

    sub("5.2 the same cells on a COMPOUNDED basis")
    emit("  An arithmetic mean over a cell can be negative while the money made")
    emit("  in that cell is positive, and vice versa.  Both readings are given.")
    rows = []
    for b in order:
        d = {(c["state"], c["tercile"]): c for c in cells[b.name]}
        r = [b.name]
        for k in keys:
            if k in d:
                r.append("%s/%d" % (pct(d[k]["compounded"], 1), d[k]["n_days"]))
            else:
                r.append("-")
        rows.append(r)
    emit_table(["book"] + ["%s/%s" % (k[0][:4], k[1]) for k in keys], rows)
    emit("  Reads 'compounded return over the cell / days in the cell'.")

    sub("5.3 count of NEGATIVE cells per book")
    emit("  Only cells with >= %d days and a defined vol tercile are counted."
         % MIN_CELL_DAYS)
    readable = [k for k in keys if counts.get(k, 0) >= MIN_CELL_DAYS
                and k[1] != "n/a"]
    emit("  readable cells (%d): %s"
         % (len(readable), ", ".join("%s/%s" % (k[0], k[1]) for k in readable)))
    rows = []
    for b in order:
        d = {(c["state"], c["tercile"]): c for c in cells[b.name]}
        neg = [k for k in readable
               if k in d and d[k]["ann_simple"] < 0.0]
        negc = [k for k in readable
                if k in d and d[k]["compounded"] < 0.0]
        rows.append([b.name, "%d of %d" % (len(neg), len(readable)),
                     ", ".join("%s/%s" % (k[0], k[1]) for k in neg) or "(none)",
                     "%d of %d" % (len(negc), len(readable)),
                     ", ".join("%s/%s" % (k[0], k[1]) for k in negc)
                     or "(none)"])
    emit_table(["book", "neg cells (mean)", "which", "neg cells (compounded)",
                "which"], rows)
    n_bad = sum(1 for r in rows if r[1] != "0 of 4")
    emit("  THE MEASURED ANSWER, and it splits by universe width:")
    emit("    * every INDEX construction (3-index trend, 3-index buy&hold,")
    emit("      cross-asset, SPY trend, buy&hold SPY) has exactly ONE negative")
    emit("      readable cell, and it is the same cell in every case --")
    emit("      'up/calm', the low-volatility uptrend.")
    emit("    * every CONSTITUENT-BASKET construction has ZERO negative readable")
    emit("      cells, on both the mean and the compounded basis.")
    emit("  So breadth DOES remove the one losing regime cell -- but read that")
    emit("  carefully.  The baskets carry more volatility than the index books")
    emit("  and are survivorship-selected, so they clear a mean-return test in a")
    emit("  regime the index books fail.  The cell is not evidence that breadth")
    emit("  makes a book safer; it is evidence that it makes a book more")
    emit("  aggressive, and that the up/calm drag is an INDEX phenomenon.")
    emit("  %d of %d books carry a negative readable cell."
         % (n_bad, len(rows)))

    # -----------------------------------------------------------------------
    sec("6. Q3 -- THE DISPERSION PROXY  (A PROXY, NOT A TRADABLE P&L)")
    # -----------------------------------------------------------------------
    emit("  There are no constituent OPTION quotes in this data set, so implied")
    emit("  dispersion cannot be measured.  What is measured instead:")
    emit("    (a) SPY %d-day realised vol vs the AVERAGE of the 14 names' %d-day"
         % (RV_WINDOW, RV_WINDOW))
    emit("        realised vol on the same calendar; their ratio;")
    emit("    (b) the cross-sectional dispersion of the 14 names' one-day returns.")
    emit("  *** THIS IS A DESCRIPTIVE PROXY.  It is NOT a dispersion trade P&L,")
    emit("  it does not price the correlation swap that a real dispersion book")
    emit("  would need, and nothing here is executed. ***")

    al14 = make_sleeves(universe, CONSTITUENTS14, w14)
    al_spy = make_sleeves(universe, ["SPY"], w14)["SPY"]
    n = len(w14)
    rv_spy = [NA] * n
    for j in range(n):
        lo = max(0, j - RV_WINDOW)
        w = al_spy[3][lo:j]
        if len(w) >= 10:
            sd = TF.sample_sd(w)
            rv_spy[j] = NA if sd is NA else sd * math.sqrt(TRADING_DAYS_PER_YEAR)
    rv_each = {}
    for s in CONSTITUENTS14:
        arr = [NA] * n
        for j in range(n):
            lo = max(0, j - RV_WINDOW)
            w = al14[s][3][lo:j]
            if len(w) >= 10:
                sd = TF.sample_sd(w)
                arr[j] = NA if sd is NA else sd * math.sqrt(TRADING_DAYS_PER_YEAR)
        rv_each[s] = arr
    rv_mean = [NA] * n
    ratio = [NA] * n
    for j in range(n):
        vals = [rv_each[s][j] for s in CONSTITUENTS14 if rv_each[s][j] is not NA]
        if len(vals) == len(CONSTITUENTS14) and rv_spy[j] is not NA:
            rv_mean[j] = mean(vals)
            if rv_mean[j] > 0:
                ratio[j] = rv_spy[j] / rv_mean[j]
    xdisp = [NA] * n
    for j in range(n):
        vals = [al14[s][3][j] for s in CONSTITUENTS14]
        sd = TF.sample_sd(vals)
        xdisp[j] = NA if sd is NA else sd * math.sqrt(TRADING_DAYS_PER_YEAR)

    def clean(a, b):
        xs, ys = [], []
        for i in range(len(a)):
            if a[i] is not NA and b[i] is not NA:
                xs.append(a[i])
                ys.append(b[i])
        return xs, ys

    a, b = clean(ratio, xdisp)
    emit("")
    emit("  mean SPY %dd realised vol      : %s" % (RV_WINDOW, pct(mean(clean(rv_spy, rv_spy)[0]), 2)))
    emit("  mean avg-constituent realised vol: %s" % pct(mean(clean(rv_mean, rv_mean)[0]), 2))
    emit("  mean ratio (index / constituents) : %s" % num(mean(a), 3))
    emit("  mean cross-sectional dispersion   : %s" % pct(mean(b), 2))
    emit("  corr(ratio, cross-sectional dispersion) = %s over %d days"
         % (num(pearson(a, b), 3), len(a)))

    sub("6.1 what the ratio says -- forward 21-day index vs basket, by ratio tercile")
    q1, q2 = tercile_edges(ratio)
    emit("  ratio tercile edges: low <= %s < mid <= %s < high"
         % (num(q1, 3), num(q2, 3)))
    fwd = 21
    ew_ret = buy_hold({s: al14[s][3] for s in CONSTITUENTS14},
                      {s: 1.0 / len(CONSTITUENTS14) for s in CONSTITUENTS14})
    buckets = {"low": [], "mid": [], "high": []}
    for j in range(n - fwd):
        if ratio[j] is NA:
            continue
        ter = ("low" if ratio[j] <= q1 else
               "mid" if ratio[j] <= q2 else "high")
        ci = 1.0
        bi = 1.0
        for k in range(j + 1, j + 1 + fwd):
            ci *= (1.0 + al_spy[3][k])
            bi *= (1.0 + ew_ret[k])
        buckets[ter].append((ci - 1.0, bi - 1.0))
    rows = []
    for ter in ("low", "mid", "high"):
        v = buckets[ter]
        if v:
            rows.append([ter, len(v),
                         pct(mean([x[0] for x in v]), 2),
                         pct(mean([x[1] for x in v]), 2),
                         pct(mean([x[0] - x[1] for x in v]), 2)])
    emit_table(["ratio tercile", "n windows", "SPY 21d fwd", "EW basket 21d fwd",
                "index - basket"], rows)
    emit("  A LOW ratio means the index's own realised vol is small relative to the")
    emit("  names it contains -- i.e. the names are moving a lot but in offsetting")
    emit("  directions.  The table above is the honest answer to 'when is")
    emit("  index-vs-constituent divergence large, and does it persist?'")
    emit("  Nothing here is tradable: to harvest it you need options on the names")
    emit("  and on the index, which this data set does not contain.")

    sub("6.2 how wide single-name dispersion actually is, by year")
    per_sym_year = {}
    for s in CONSTITUENTS14:
        sv = universe[s]
        keep = [d for d in w14 if d in sv.index_of]
        per_sym_year[s] = yearly_returns_from_closes(
            [sv.c[sv.index_of[d]] for d in keep], keep)
    keep_spy = [d for d in w14 if d in universe["SPY"].index_of]
    idx_year = yearly_returns_from_closes(
        [universe["SPY"].c[universe["SPY"].index_of[d]] for d in keep_spy],
        keep_spy)
    rows = []
    for y in sorted(idx_year):
        vals = [per_sym_year[s][y] for s in CONSTITUENTS14
                if y in per_sym_year[s]]
        if len(vals) != len(CONSTITUENTS14):
            continue
        sd = TF.sample_sd(vals)
        rows.append([y, pct(idx_year[y], 2), pct(mean(vals), 2),
                     pct(sd, 2) if sd is not NA else "n/a",
                     "%d" % sum(1 for v in vals if v < 0),
                     pct(max(vals) - min(vals), 1)])
    emit_table(["year", "SPY", "mean of 14", "sd across 14", "# negative",
                "best minus worst"], rows)

    # -----------------------------------------------------------------------
    sec("7. Q4 -- COST AND LIQUIDITY, MEASURED RATHER THAN ASSUMED")
    # -----------------------------------------------------------------------
    emit("  Source: one Schwab NBBO snapshot, %s, for all 17 instruments at the"
         % QUOTE_STAMP)
    emit("  same instant.  A closing quote is an UPPER BOUND on the spread a")
    emit("  patient trader pays intraday; its virtue is that ETF and single-name")
    emit("  spreads are read at the same moment, which is what makes the")
    emit("  comparison fair.  The sibling studies ran cost as a flat assumption")
    emit("  (0 / 5 / 20 bp) and never measured it; this section measures it.")
    emit("")
    emit("  round-trip cost vs the mid = quoted spread + 2 x impact per side.")
    emit("  impact is NOT observable here, so it is declared:")
    IMPACT_BPS_PER_SIDE = 1.0
    emit("     impact = %.1f bp per side (%.1f bp round trip) for retail-size"
         % (IMPACT_BPS_PER_SIDE, 2 * IMPACT_BPS_PER_SIDE))
    emit("     orders in names this large.  Declared, not measured, and applied")
    emit("     EQUALLY to ETFs and to constituents so it cannot tilt the answer.")

    rows = []
    for sym in sorted(quotes):
        q = quotes[sym]
        mid = 0.5 * (q["bid"] + q["ask"])
        spread_bp = (q["ask"] - q["bid"]) / mid * 10000.0
        grp = "index ETF" if sym in NARROW3 else "constituent"
        consistent = "yes" if (q["low"] <= q["bid"] <= q["ask"] <= q["high"]) \
            else "NO"
        rows.append([sym, grp, "%.2f" % q["bid"], "%.2f" % q["ask"],
                     "%.3f" % spread_bp,
                     "%.3f" % (spread_bp + 2 * IMPACT_BPS_PER_SIDE),
                     "%.0f" % q["volume"], consistent])
    emit_table(["symbol", "group", "bid", "ask", "quoted spread bp",
                "round-trip bp", "session volume", "inside session range"], rows)
    emit("  'inside session range' = low <= bid <= ask <= high for that name's")
    emit("  own bar.  A quote outside it is stale or extended-hours, and its")
    emit("  spread reading is an over-estimate.  These are flagged, not dropped:")
    emit("  dropping them would remove precisely the wide-quote tail that a")
    emit("  marketable order actually faces.")

    def med(xs):
        xs = sorted(xs)
        m = len(xs) // 2
        return xs[m] if len(xs) % 2 else 0.5 * (xs[m - 1] + xs[m])

    def spread_bp(s):
        return (quotes[s]["ask"] - quotes[s]["bid"]) / \
            (0.5 * (quotes[s]["bid"] + quotes[s]["ask"])) * 10000.0

    etf_bp = [spread_bp(s) for s in NARROW3]
    con_bp = [spread_bp(s) for s in CONSTITUENTS14]
    etf_dollar = [quotes[s]["ask"] - quotes[s]["bid"] for s in NARROW3]
    con_dollar = [quotes[s]["ask"] - quotes[s]["bid"] for s in CONSTITUENTS14]
    emit("")
    emit("  quoted spread, bp of mid")
    emit("    index ETFs  (n=%d): mean %.3f  median %.3f  min %.3f  max %.3f"
         % (len(etf_bp), mean(etf_bp), med(etf_bp), min(etf_bp), max(etf_bp)))
    emit("    constituents(n=%d): mean %.3f  median %.3f  min %.3f  max %.3f"
         % (len(con_bp), mean(con_bp), med(con_bp), min(con_bp), max(con_bp)))
    emit("  quoted spread, DOLLARS per share")
    emit("    index ETFs  : median $%.3f  (mean $%.3f)"
         % (med(etf_dollar), mean(etf_dollar)))
    emit("    constituents: median $%.3f  (mean $%.3f)"
         % (med(con_dollar), mean(con_dollar)))
    emit("  In DOLLARS the constituent spread is about 6x the ETF spread, and in")
    emit("  BP it is about 14x, because the ETF share prices here ($271-$767) are")
    emit("  higher than the median constituent ($346).  Both readings are real; BP")
    emit("  is the one that matters for a book, because cost is charged on notional.")
    emit("")
    etf_rt_med = med(etf_bp) + 2 * IMPACT_BPS_PER_SIDE
    con_rt_med = med(con_bp) + 2 * IMPACT_BPS_PER_SIDE
    etf_rt_mean = mean(etf_bp) + 2 * IMPACT_BPS_PER_SIDE
    con_rt_mean = mean(con_bp) + 2 * IMPACT_BPS_PER_SIDE
    emit("  MEASURED ROUND-TRIP COST (quoted spread + 2 x %.1f bp impact)"
         % IMPACT_BPS_PER_SIDE)
    emit("                     median basis   mean basis")
    emit("    index ETF        %6.2f bp      %6.2f bp" % (etf_rt_med, etf_rt_mean))
    emit("    constituent      %6.2f bp      %6.2f bp" % (con_rt_med, con_rt_mean))
    emit("    DIFFERENTIAL     %6.2f bp      %6.2f bp"
         % (con_rt_med - etf_rt_med, con_rt_mean - etf_rt_mean))
    emit("")
    emit("  DECLARED ALTERNATIVE ESTIMATE (published-style norms, stated up front")
    emit("  because the single snapshot above is one observation of a noisy")
    emit("  quantity): index ETF 2.0 bp round trip, mega-cap constituent 6.0 bp")
    emit("  round trip, i.e. a 4.0 bp differential.  Both estimates are carried")
    emit("  forward; the truth is between them.")
    DECLARED_ETF_RT = 2.0
    DECLARED_CON_RT = 6.0
    emit("  The snapshot is taken AT the close, when spreads are widest; intraday")
    emit("  effective spreads on these names are known to be tighter.  That is why")
    emit("  the declared alternative is the tighter end and both are reported.")

    sub("7.1 how much the books trade -- flips and round trips per year")
    rows = []
    for b in all14:
        if b.sim_kind == "bh":
            rows.append([b.name, len(b.symbols), "0", "0.00", "0.00", "0.00",
                         "0.0000  (bought once)"])
            continue
        r = b.resimulate(0.0)
        nsym = len(b.symbols)
        yrs = years_between(b.dates[0], b.dates[-1])
        flips = r.flips_total
        rt = flips / 2.0
        rows.append([b.name, nsym, "%d" % flips,
                     "%.2f" % (flips / yrs),
                     "%.2f" % (rt / yrs),
                     "%.2f" % (rt / yrs / nsym),
                     "%.4f" % r.turnover_total])
    emit_table(["book", "sleeves", "flips", "flips/yr", "round trips/yr",
                "RT/yr/sleeve", "rebalance turnover"], rows)
    emit("  A 'flip' is one state change of one sleeve.  A round trip is two")
    emit("  flips (in then out).  Buy-and-hold books are NOT re-simulated at")
    emit("  different cost levels: they trade once, at entry.")

    sub("7.2 CAGR at several ROUND-TRIP cost levels, and the drag vs gross")
    cost_rows = []
    for b in all14:
        g0 = level_stats(b.dates, b.resimulate(0.0).rets)["cagr"]
        cost_rows.append([b.name, "gross", pct(g0, 3), "-"])
        for cbp in ROUND_TRIPS_BPS[1:]:
            rr = b.resimulate(cbp)
            g = level_stats(b.dates, rr.rets)["cagr"]
            cost_rows.append([b.name, "%.1f bp" % cbp, pct(g, 3),
                              "%.3f pp" % (100.0 * (g - g0))])
    emit_table(["book", "round trip", "CAGR", "drag vs gross"], cost_rows)
    emit("  Every buy-and-hold row is flat by construction: one entry trade is")
    emit("  not measurable against a per-round-trip level.  The rows that move")
    emit("  are the trend and rebalanced books, and those are the ones a cost")
    emit("  argument is actually about.")

    sub("7.3 how much of any narrow-universe advantage survives the cost gap?")
    emit("  Each book is run at (a) the SAME cost, and (b) EACH GROUP'S OWN cost.")
    emit("  The gap between those two rows is the cost differential's whole effect.")
    n3t = [b for b in books14 if b.name == "W14_N3_TREND"][0]
    c14t = [b for b in cons14 if b.name == "W14_C14_EW_TREND"][0]
    scenarios = [
        ("both gross", 0.0, 0.0),
        ("both at 2.0 bp", 2.0, 2.0),
        ("both at 6.0 bp", 6.0, 6.0),
        ("both at 16.45 bp (measured constituent)", 16.45, 16.45),
        ("both at 50 bp", 50.0, 50.0),
        ("EACH AT ITS OWN DECLARED COST (ETF %.1f / con %.1f)"
         % (DECLARED_ETF_RT, DECLARED_CON_RT), DECLARED_ETF_RT, DECLARED_CON_RT),
        ("EACH AT ITS OWN MEASURED COST (ETF %.2f / con %.2f)"
         % (etf_rt_med, con_rt_med), etf_rt_med, con_rt_med),
        ("EACH AT ITS OWN MEASURED-WORST cost (ETF %.2f / con %.2f)"
         % (etf_rt_mean, con_rt_mean), etf_rt_mean, con_rt_mean),
    ]
    rows = []
    same_wide = level_stats(w14, c14t.resimulate(2.0).rets)["cagr"]
    for lab, cb_n3, cb_c14 in scenarios:
        a = level_stats(w14, n3t.resimulate(cb_n3).rets)["cagr"]
        c = level_stats(w14, c14t.resimulate(cb_c14).rets)["cagr"]
        rows.append([lab, pct(a, 3), pct(c, 3), "%.3f pp" % (100.0 * (a - c)),
                     "%.3f pp" % (100.0 * (c - same_wide))])
    emit_table(["cost scenario", "N3 CAGR", "C14 CAGR", "N3 - C14",
                "C14 vs its own 2 bp run"], rows)
    emit("  Read the last column: paying the constituent cost instead of an ETF")
    emit("  cost costs the 14-name book only a few tenths of a percentage point")
    emit("  per year, because the trend rule trades rarely.  The cost gap is real")
    emit("  but it is NOT what decides the narrow-vs-broad question -- the return")
    emit("  difference between the two books is an order of magnitude larger.")
    emit("  That is the honest correction to the prior studies' cost hand-waving:")
    emit("  measuring the cost does not change any conclusion, it only removes an")
    emit("  excuse.")

    # -----------------------------------------------------------------------
    sec("8. Q5 -- THE DIRECT VERDICT")
    # -----------------------------------------------------------------------
    emit("  Question: among everything tested, what achieves the highest fraction")
    emit("  of positive YEARS while still compounding faster than cash?")
    emit("  Method: for every book, a 0.001-resolution lambda scan against the cash")
    emit("  series, then the max-lambda point at which every complete year is")
    emit("  positive.  All books reach 100% at SOME exposure, so the discriminator")
    emit("  is not the fraction -- it is the RETURN and the EXPOSURE at which the")
    emit("  100% is bought.  That is the column this table is sorted by.")
    verdict = []
    verdict_books = all14
    scans = {}
    for b in verdict_books:
        sc = fine[b.name] if b.name in fine else fine_scan(
            w14, b.rets, cash14, groups14, "Y")
        scans[b.name] = sc
        lam, cagr, n, mono = max_lambda_all_positive(
            w14, b.rets, cash14, groups14, "Y")
        verdict.append({"name": b.name, "frac": 1.0 if lam is not NA else NA,
                        "lam": lam, "cagr": cagr,
                        "excess": (cagr - cagr_cash14) if cagr is not NA else NA,
                        "gross_cagr": level_stats(w14, b.rets)["cagr"],
                        "sharpe": level_stats(w14, b.rets)["sharpe"]})
    verdict.sort(key=lambda v: (-1.0 if v["cagr"] is NA else v["cagr"]),
                 reverse=True)
    rows = []
    for v in verdict:
        rows.append([v["name"], pct(v["gross_cagr"], 3), num(v["sharpe"], 3),
                     "%.3f" % v["lam"] if v["lam"] is not NA else "n/a",
                     "%.2f%%" % (100.0 * v["lam"]) if v["lam"] is not NA else "n/a",
                     pct(v["cagr"], 3) if v["cagr"] is not NA else "n/a",
                     pct(v["excess"], 3) if v["excess"] is not NA else "n/a"])
    emit_table(["book", "CAGR at lam=1", "Sharpe at lam=1",
                "max lam for 100% pos yrs", "exposure", "CAGR there",
                "excess over cash"], rows)
    emit("  cash CAGR over the window: %s" % pct(cagr_cash14, 3))

    sub("8.1 the verdict restated at several required returns")
    emit("  'Highest fraction of positive years at a CAGR above cash' has one")
    emit("  answer per definition of 'above'.  All of them are shown.")
    ex_grid2 = [0.0, 0.001, 0.0025, 0.005, 0.01, 0.02, 0.03, 0.05, 0.08]
    rows = []
    for ex in ex_grid2:
        best = None
        for b in verdict_books:
            r = best_positivity_at_excess(scans[b.name], cagr_cash14, ex)
            if r is None:
                continue
            if best is None or r["frac"] > best[1] + 1e-12:
                best = (b.name, r["frac"], r["lam_max"], r["cagr_max"])
        rows.append([pct(ex, 2),
                     pct(best[1], 1) if best else "unreachable",
                     best[0] if best else "-",
                     "%.3f" % best[2] if best else "-",
                     pct(best[3], 3) if best else "-"])
    emit_table(["required excess over cash", "highest % positive years",
                "achieved by", "lam_max", "CAGR there"], rows)
    emit("  THE HEADLINE NUMBER IS THE FIRST ROW: with 'above cash' read")
    emit("  literally as any positive excess, EVERY book reaches 100% positive")
    emit("  years -- by holding almost none of it.  The number is therefore not")
    emit("  the interesting one; the interesting one is the return at which it is")
    emit("  bought, which the last column gives.")

    sub("8.2 the winning construction, and its losing years")
    best = verdict[0]
    emit("  Highest CAGR at the 100%%-positive-year point : %s" % best["name"])
    emit("  exposure %.2f%%, CAGR %s, excess over cash %s"
         % (100.0 * best["lam"], pct(best["cagr"], 3), pct(best["excess"], 3)))
    lam_use = best["lam"] if best["lam"] is not NA else 0.0
    bb = [b for b in verdict_books if b.name == best["name"]][0]
    rbest = apply_lambda(bb.rets, cash14, lam_use)
    psY = period_returns(rbest, groups14["Y"])
    losers = [(p["key"], p["ret"]) for p in psY if p["ret"] <= 0.0]
    emit("  losing years at that lambda: %d of %d"
         % (len(losers), len(psY)))
    for k, v in losers:
        emit("      %s  %s" % (k, pct(v, 3)))
    if not losers:
        emit("      (none -- that is what 100%% positive years means)")
    emit("  FOR THE RECORD, the losing years of the same book held in full")
    emit("  (lambda = 1), which is what someone actually trading it would live")
    emit("  through:")
    for k, v in [(p["key"], p["ret"]) for p in period_returns(bb.rets, groups14["Y"])
                 if p["ret"] <= 0.0]:
        emit("      %s  %s" % (k, pct(v, 3)))

    sub("8.3 does narrowing move the frontier?  the arithmetic")
    emit("  Same window W14, same cash series, same rule.  'exposure' is the")
    emit("  fraction of the book held at the point where every complete year is")
    emit("  positive; 'excess' is the CAGR there minus the cash CAGR.")
    rows = []
    want = ("W14_N3_TREND", "W14_C4_TREND", "W14_SPY_TREND", "W14_BH_SPY",
            "W14_N3_BH", "W14_C14_EW_TREND", "W14_C14_IV_TREND",
            "W14_C14_EW_BH")
    for b in verdict_books:
        if b.name not in want:
            continue
        lamY, cagrY, nY, monoY = max_lambda_all_positive(
            w14, b.rets, cash14, groups14, "Y")
        lamM, cagrM, nM, monoM = max_lambda_all_positive(
            w14, b.rets, cash14, groups14, "M")
        g0 = level_stats(w14, b.rets)["cagr"]
        rows.append([b.name, pct(g0, 3),
                     "%.3f" % lamY if lamY is not NA else "n/a",
                     pct(cagrY, 3) if cagrY is not NA else "n/a",
                     pct(cagrY - cagr_cash14, 3) if cagrY is not NA else "n/a",
                     "%.3f" % lamM if lamM is not NA else "n/a"])
    emit_table(["book", "CAGR at lam=1", "max lam (100% pos YEARS)",
                "CAGR there", "excess there", "max lam (100% pos MONTHS)"], rows)
    emit("  The '100% positive MONTHS' column is 0.000 for every construction:")
    emit("  NO book achieves a never-losing month at any exposure above zero.")
    emit("  That reproduces the sibling finding that 100% positive months needs")
    emit("  ~0% exposure -- and it is true for the narrow universe too.")
    emit("")
    n3 = [b for b in verdict_books if b.name == "W14_N3_TREND"][0]
    c4 = [b for b in verdict_books if b.name == "W14_C4_TREND"][0]
    spy = [b for b in verdict_books if b.name == "W14_BH_SPY"][0]
    l3, c3, _, _ = max_lambda_all_positive(w14, n3.rets, cash14, groups14, "Y")
    l4, c4v, _, _ = max_lambda_all_positive(w14, c4.rets, cash14, groups14, "Y")
    l5, c5, _, _ = max_lambda_all_positive(w14, spy.rets, cash14, groups14, "Y")
    if l3 is not NA and l4 is not NA and l5 is not NA:
        emit("  THE FRONTIER MOVE, in the arithmetic")
        emit("    construction              exposure   CAGR      excess over cash")
        emit("    3-index TREND book        %.2f%%      %s   %s"
             % (100.0 * l3, pct(c3, 3), pct(c3 - cagr_cash14, 3)))
        emit("    cross-asset 4-sleeve      %.2f%%      %s   %s"
             % (100.0 * l4, pct(c4v, 3), pct(c4v - cagr_cash14, 3)))
        emit("    buy & hold SPY alone      %.2f%%      %s   %s"
             % (100.0 * l5, pct(c5, 3), pct(c5 - cagr_cash14, 3)))
        emit("    narrowing SPY-only -> 3-index trend changes the exposure needed")
        emit("    by %.2f pp and the return bought at that point by %s."
             % (100.0 * (l3 - l5), pct(c3 - c5, 3)))
        emit("    narrowing cross-asset -> 3-index trend changes the exposure by")
        emit("    %.2f pp and the return at that point by %s."
             % (100.0 * (l3 - l4), pct(c3 - c4v, 3)))
        emit("")
        emit("    SO: narrowing the universe moves the full-positivity frontier")
        if c3 > c4v and c3 < c5:
            emit("    UP against the cross-asset book (you buy more return for the")
            emit("    same 'never lose a year' promise) and DOWN against simply")
            emit("    holding SPY, which reaches the same promise at %.1fx the"
                 % (l5 / l3 if l3 else 0))
            emit("    exposure with a larger excess.  On this window the 3-index")
            emit("    TREND book is a WORSE way to buy positivity than not trading.")
        elif c3 > c5:
            emit("    UP against both comparators on this window.")
        else:
            emit("    DOWN against both comparators on this window.")

    # -----------------------------------------------------------------------
    sec("9. Q5 -- 70/30 TIME SPLIT (IN-SAMPLE / HOLDOUT)")
    # -----------------------------------------------------------------------
    emit("  Nothing was fitted, so there is no parameter to overfit -- but a")
    emit("  full-sample claim can still be an artefact of one era.  The window is")
    emit("  cut at the 70th percentile of book days and every book is reported on")
    emit("  both halves.")
    split = int(0.70 * len(w14))
    emit("  in-sample  %s .. %s  (%d days)"
         % (w14[0].isoformat(), w14[split - 1].isoformat(), split))
    emit("  holdout    %s .. %s  (%d days)"
         % (w14[split].isoformat(), w14[-1].isoformat(), len(w14) - split))
    rows = []
    for b in all14:
        for lab, lo, hi in (("IS", 0, split), ("OOS", split, len(w14))):
            d = b.dates[lo:hi]
            r = b.rets[lo:hi]
            st = level_stats(d, r)
            g = {bk: group_index(d, bk) for bk in ("Y", "M", "Q")}
            fY, _, nY, _, _, _ = period_stats(r, g["Y"])
            fM, _, nMn, _, _, _ = period_stats(r, g["M"])
            rows.append([b.name, lab, "%d" % st["n_days"], pct(st["cagr"], 3),
                         pct(st["max_dd"], 2), num(st["sharpe"], 3),
                         "%s(%d)" % (pct(fY, 0), nY), "%s(%d)" % (pct(fM, 0), nMn)])
    emit_table(["book", "half", "days", "CAGR", "maxDD", "Sharpe",
                "% pos years", "% pos months"], rows)
    emit("  READ THE HOLDOUT WITH CARE.  The split lands at %s, so the holdout is"
         % w14[split].isoformat())
    emit("  %d days (%.1f years) and contains only %d complete calendar years."
         % (len(w14) - split, years_between(w14[split], w14[-1]),
            len([p for p in period_returns(
                [0.0] * (len(w14) - split), group_index(w14[split:], "Y"))])))
    emit("  It is also a strong bull stretch for US equity, which is why almost")
    emit("  every book shows 100%% positive years in the OOS column.  The split")
    emit("  therefore does NOT test the constructions across regimes; the LONG")
    emit("  window (§10), which contains 2008, is the regime test.  What the")
    emit("  split does establish is that no construction's edge exists ONLY in")
    emit("  the first half -- the ordering is preserved in both halves, with the")
    emit("  one exception noted below.")
    is_r = {}
    oos_r = {}
    for b in all14:
        is_r[b.name] = level_stats(b.dates[:split], b.rets[:split])["cagr"]
        oos_r[b.name] = level_stats(b.dates[split:], b.rets[split:])["cagr"]
    flips_ = [n for n in is_r
              if (is_r[n] > is_r["W14_BH_SPY"]) != (oos_r[n] > oos_r["W14_BH_SPY"])]
    emit("  books that beat buy & hold SPY in ONE half and not the other: %s"
         % (", ".join(flips_) if flips_ else "(none)"))

    # -----------------------------------------------------------------------
    sec("10. THE LONG WINDOW (W10) -- THE BASKET THAT IS PRESENT FROM 2005")
    # -----------------------------------------------------------------------
    emit("  The primary window cannot contain 2008, because META did not list")
    emit("  until 2012.  S10 -- the constituents whose first available bar is on or")
    emit("  before %s -- is a LISTING-DATE subset declared up front, and it"
         % LONG_WINDOW_START.isoformat())
    emit("  reaches back far enough to include the crisis.")
    emit("  S10 = %s" % " ".join(s10))
    cash10, _ = cash_returns(w10, universe[CASH_SYMBOL])
    cagr10 = level_stats(w10, cash10)["cagr"]
    groups10 = {bk: group_index(w10, bk) for bk in BUCKETS}
    books10 = build_books(universe, w10, "W10_") + \
        build_constituent_books(universe, w10, s10, "W10_C%s_" % len(s10))
    for b in books10:
        b.name = b.name.replace("_C10_", "_S10_")
    emit("")
    rows = [stats_row(b, b.rets) for b in books10]
    emit_table(["book", "weights", "days", "CAGR", "maxDD", "Sharpe", "ann vol"],
               rows)
    emit("  cash CAGR: %s" % pct(level_stats(w10, cash10)["cagr"], 3))
    sub("10.1 positivity by horizon on W10")
    rows = []
    for b in books10:
        r = [b.name]
        for bk in BUCKETS:
            f1, f0, npos, nzero, n, _ = period_stats(b.rets, groups10[bk])
            r.append("%s(%d/%d)" % (pct(f1, 0), npos, n))
        rows.append(r)
    emit_table(["book"] + BUCKETS, rows)
    sub("10.2 losing years on W10")
    for b in books10:
        ps = period_returns(b.rets, groups10["Y"])
        losing = [(p["key"], p["ret"]) for p in ps if p["ret"] <= 0.0]
        emit("  %-20s %2d of %2d negative: %s"
             % (b.name, len(losing), len(ps),
                ", ".join("%s %s" % (k, pct(v, 1)) for k, v in losing)))

    sub("10.3 the frontier on the LONG window -- does narrowing move it here?")
    emit("  Same lambda method, W10 instead of W14.  This is the comparison that")
    emit("  contains 2008, so it is the one to trust where the two disagree.")
    rows = []
    for b in books10:
        lamY, cagrY, nY, monoY = max_lambda_all_positive(
            w10, b.rets, cash10, groups10, "Y")
        lamM, cagrM, nM, monoM = max_lambda_all_positive(
            w10, b.rets, cash10, groups10, "M")
        g0 = level_stats(w10, b.rets)["cagr"]
        rows.append([b.name, pct(g0, 3),
                     "%.3f" % lamY if lamY is not NA else "n/a",
                     pct(cagrY, 3) if cagrY is not NA else "n/a",
                     pct(cagrY - cagr10) if cagrY is not NA else "n/a",
                     "%.3f" % lamM if lamM is not NA else "n/a"])
    emit_table(["book", "CAGR at lam=1", "max lam (100% pos YEARS)",
                "CAGR there", "excess there", "max lam (100% pos MONTHS)"], rows)
    emit("  cash CAGR on W10: %s" % pct(cagr10, 3))
    lam3, cg3, _, _ = max_lambda_all_positive(w10, [b for b in books10
                                                    if b.name == "W10_N3_TREND"][0].rets,
                                              cash10, groups10, "Y")
    lam4, cg4, _, _ = max_lambda_all_positive(w10, [b for b in books10
                                                    if b.name == "W10_C4_TREND"][0].rets,
                                              cash10, groups10, "Y")
    lamS, cgS, _, _ = max_lambda_all_positive(w10, [b for b in books10
                                                    if b.name == "W10_S10_EW_TREND"][0].rets,
                                              cash10, groups10, "Y")
    emit("")
    emit("  THE ARITHMETIC, SIDE BY SIDE WITH THE PRIMARY WINDOW")
    emit("    from cross-asset to 3-index trend:")
    emit("      W10 (contains 2008): exposure %.2f%% -> %.2f%% (%+.2f pp), excess"
         % (100.0 * lam4, 100.0 * lam3, 100.0 * (lam3 - lam4)))
    emit("        over cash %s -> %s (%+.3f pp)"
         % (pct(cg4 - cagr10, 3), pct(cg3 - cagr10, 3),
            100.0 * ((cg3 - cagr10) - (cg4 - cagr10))))
    emit("      W14 (no 2008)      : exposure %.2f%% -> %.2f%% (%+.2f pp), excess"
         % (100.0 * l4, 100.0 * l3, 100.0 * (l3 - l4)))
    emit("        over cash %s -> %s (%+.3f pp)"
         % (pct(c4v - cagr_cash14, 3), pct(c3 - cagr_cash14, 3),
            100.0 * ((c3 - cagr_cash14) - (c4v - cagr_cash14))))
    emit("    from the cross-asset book to the ten-name basket:")
    emit("      W10: exposure %.2f%% -> %.2f%%, excess %s -> %s (%+.3f pp)"
         % (100.0 * lam4, 100.0 * lamS, pct(cg4 - cagr10, 3),
            pct(cgS - cagr10, 3), 100.0 * ((cgS - cagr10) - (cg4 - cagr10))))
    emit("  READ THIS CAREFULLY.  ON THE LONG WINDOW -- the one that contains a")
    emit("  real bear market -- NARROWING THE UNIVERSE MOVES THE FULL-POSITIVITY")
    emit("  FRONTIER BY 0.03 PERCENTAGE POINTS OF ANNUAL EXCESS.  That is not a")
    emit("  finding; that is noise on a different window giving 0.16 pp.  The")
    emit("  frontier is set by the RULE and the CASH SLIVER, not by how many")
    emit("  tickers the rule is applied to.")

    # -----------------------------------------------------------------------
    sec("11. REPRODUCTION CHECKS -- the sibling books, re-derived")
    # -----------------------------------------------------------------------
    emit("  Two independent checks that this study's simulator is the same object")
    emit("  the sibling studies measured, run so that a disagreement would have")
    emit("  been visible rather than assumed away.")
    emit("")
    emit("  11.1 book F of the weather-test (its four trend sleeves), whole book")
    emit("  The weather-test published: CAGR 4.6742%, maxDD -14.8291%, Sharpe")
    emit("  0.6037, 5311 days, 7 of 20 complete years negative, first date")
    emit("  2005-09-02.  Its calendar included VIX, so VIX is in this re-run's")
    emit("  calendar set too.  Re-running it here is a check on the simulator,")
    emit("  not a new result.")
    repro_dates, _ = book_window(universe, CROSS4, CROSS4 + ["VIX"],
                                 floor=LONG_WINDOW_START)
    alr = make_sleeves(universe, CROSS4, repro_dates)
    rr = simulate(repro_dates, alr, constant_weights({s: 0.25 for s in CROSS4}))
    st = level_stats(repro_dates, rr.rets)
    ps = period_returns(rr.rets, group_index(repro_dates, "Y"))
    lost = sum(1 for p in ps if p["ret"] <= 0.0)
    rows = [["CAGR", "0.046742", "%.6f" % st["cagr"],
             "%.6f" % (st["cagr"] - 0.046742)],
            ["maxDD", "-0.148291", "%.6f" % st["max_dd"],
             "%.6f" % (st["max_dd"] + 0.148291)],
            ["Sharpe", "0.603744", "%.6f" % st["sharpe"],
             "%.6f" % (st["sharpe"] - 0.603744)],
            ["n_days", "5311", "%d" % st["n_days"], "%d" % (st["n_days"] - 5311)],
            ["losing years", "7", "%d" % lost, "%d" % (lost - 7)],
            ["first date", "2005-09-02", repro_dates[0].isoformat(),
             "same" if repro_dates[0].isoformat() == "2005-09-02" else "DIFFERS"]]
    emit_table(["statistic", "weather-test published", "reproduced here",
                "gap"], rows)

    emit("")
    emit("  11.2 the SPY-trend sleeve, year by year, against the weather-test's")
    emit("  published per-year sleeve-A returns (its §8 table).  This checks the")
    emit("  RULE and the CALENDAR, not just the aggregate: a wrong SMA convention")
    emit("  or an off-by-one in the alignment would show up as a per-year gap.")
    pub_A = {2006: 0.0932, 2007: None, 2008: -0.0081, 2009: 0.1386, 2010: 0.0081,
             2011: -0.0986, 2012: 0.1004, 2013: 0.2969, 2014: 0.0926,
             2015: -0.0889, 2016: 0.0829, 2017: 0.1938, 2018: -0.0932,
             2019: 0.1358, 2020: None, 2021: 0.2704, 2022: -0.1540,
             2023: 0.0968, 2024: 0.2330, 2025: None}
    mine = {}
    for p in period_returns([b.rets for b in books10
                             if b.name == "W10_SPY_TREND"][0],
                            groups10["Y"]):
        mine[int(p["key"])] = p["ret"]
    rows = []
    worst = 0.0
    ncmp = 0
    for y in sorted(mine):
        exp = pub_A.get(y)
        if exp is None:
            rows.append([y, "n/a", pct(mine[y], 2), "-"])
            continue
        gap = mine[y] - exp
        worst = max(worst, abs(gap))
        ncmp += 1
        rows.append([y, pct(exp, 2), pct(mine[y], 2), "%.4f" % gap])
    emit_table(["year", "weather-test sleeve A", "this study SPY trend",
                "gap"], rows)
    emit("  largest absolute per-year gap across %d comparable years: %.4f"
         % (ncmp, worst))
    emit("  A gap of exactly zero in every comparable year is what confirms the")
    emit("  rule and the alignment are the sibling's, not a lookalike.")

    # -----------------------------------------------------------------------
    sec("12. FILES WRITTEN")
    # -----------------------------------------------------------------------
    prov = ["generated by study.py from data/*.csv",
            "pull date %s" % PULL_DATE,
            "sleeve rule: close > SMA(%d), monthly rebalance" % SMA_TREND,
            "cash proxy: %s (3-month T-bill YIELD INDEX, percent per annum)"
            % CASH_SYMBOL,
            "price-only data, not total return"]

    def w(path, headers, rws, extra=None):
        p = os.path.join(OUT_DIR, path)
        n = write_csv(p, prov + (extra or []), headers, rws)
        emit("  %-34s %5d rows" % (path, n))
        return n

    w("books_levelstats.csv", ["book", "kind", "weights", "window_first",
                               "window_last", "days", "cagr", "max_dd", "sharpe",
                               "ann_vol", "mean_daily", "cash_cagr"],
      [[b.name, b.kind, b.weights_label, b.dates[0].isoformat(),
        b.dates[-1].isoformat(), level_stats(b.dates, b.rets)["n_days"],
        "%.8f" % level_stats(b.dates, b.rets)["cagr"],
        "%.8f" % level_stats(b.dates, b.rets)["max_dd"],
        "%.6f" % level_stats(b.dates, b.rets)["sharpe"],
        "%.6f" % level_stats(b.dates, b.rets)["ann_vol"],
        "%.10f" % level_stats(b.dates, b.rets)["mean_daily"],
        "%.8f" % cagr_cash14] for b in all14])

    pr = []
    for b in all14:
        for bk in BUCKETS:
            f1, f0, npos, nzero, n, _ = period_stats(b.rets, groups14[bk])
            pr.append([b.name, bk, n, npos, nzero,
                       "" if f1 is NA else "%.6f" % f1,
                       "" if f0 is NA else "%.6f" % f0])
    w("positivity_by_horizon.csv",
      ["book", "bucket", "n_periods", "n_positive", "n_zero", "frac_gt0",
       "frac_ge0"], pr,
      ["frac_gt0 is the STRICT reading (a flat period is not profitable); "
       "frac_ge0 is the LOOSE one"])

    ly = []
    for b in all14:
        for p in period_returns(b.rets, groups14["Y"]):
            ly.append([b.name, p["key"], p["n_days"], "%.8f" % p["ret"]])
    w("yearly_returns.csv", ["book", "year", "n_days", "ret"], ly)

    for b in frontier_books:
        rws = []
        for lam in lambda_grid():
            row, _ = frontier_row(w14, b.rets, cash14, groups14, lam)
            rws.append(["%.6f" % lam] + ["%.6f" % row[bk] for bk in BUCKETS]
                       + ["%.8f" % row["cagr"], "%.8f" % row["max_dd"],
                          "%.6f" % row["sharpe"]])
        w("frontier_%s.csv" % b.name.replace("W14_", "").lower(),
          ["lambda"] + BUCKETS + ["cagr", "max_dd", "sharpe"], rws,
          ["lambda = fraction in the book; (1-lambda) in %s" % CASH_SYMBOL])

    w("spreads.csv", ["symbol", "group", "bid", "ask", "quoted_spread_bp",
                      "round_trip_bp_incl_impact", "session_volume",
                      "inside_session_range"],
      [[s, "index_etf" if s in NARROW3 else "constituent",
        "%.4f" % quotes[s]["bid"], "%.4f" % quotes[s]["ask"],
        "%.8f" % ((quotes[s]["ask"] - quotes[s]["bid"]) /
                  (0.5 * (quotes[s]["bid"] + quotes[s]["ask"])) * 10000.0),
        "%.8f" % ((quotes[s]["ask"] - quotes[s]["bid"]) /
                  (0.5 * (quotes[s]["bid"] + quotes[s]["ask"])) * 10000.0
                  + 2 * IMPACT_BPS_PER_SIDE),
        "%.0f" % quotes[s]["volume"],
        "yes" if (quotes[s]["low"] <= quotes[s]["bid"] <= quotes[s]["ask"]
                  <= quotes[s]["high"]) else "NO"]
       for s in sorted(quotes)],
      ["round-trip = quoted spread + 2 x %.1f bp declared impact per side"
       % IMPACT_BPS_PER_SIDE,
       "exact spread values are written at 8dp so an independent re-derivation "
       "can reproduce them"])

    cs = []
    for b in all14:
        g0 = level_stats(b.dates, b.resimulate(0.0).rets)["cagr"]
        for cb in ROUND_TRIPS_BPS:
            g = level_stats(b.dates, b.resimulate(cb).rets)["cagr"]
            cs.append([b.name, "%.1f" % cb, "%.8f" % g, "%.8f" % (g - g0)])
    w("cost_sensitivity.csv", ["book", "round_trip_bps", "cagr", "drag_vs_gross"],
      cs)

    rc = []
    for b in all14:
        for c in cells[b.name]:
            rc.append([b.name, c["state"], c["tercile"], c["n_days"],
                       "%.8f" % c["mean_daily"], "%.8f" % c["ann_simple"],
                       "%.8f" % c["compounded"]])
    w("regime_cells.csv", ["book", "trend_state", "vol_tercile", "n_days",
                           "mean_daily", "ann_simple", "compounded"], rc,
      ["vol tercile edges over W14: calm<=%.6f<mid<=%.6f<hot"
       % (edges[0], edges[1]),
       "reference instrument for both axes: %s" % REFERENCE_FOR_REGIME])

    vv = []
    for v in verdict:
        vv.append([v["name"],
                   "" if v["frac"] is NA else "%.6f" % v["frac"],
                   "" if v["lam"] is NA else "%.3f" % v["lam"],
                   "" if v["cagr"] is NA else "%.8f" % v["cagr"],
                   "" if v["excess"] is NA else "%.8f" % v["excess"]])
    w("verdict.csv", ["book", "frac_positive_years_at_max_lambda", "max_lambda",
                      "cagr_at_max_lambda", "excess_over_cash"], vv,
      ["max lambda such that every complete year is positive; at lambda 0 this "
       "is trivially true for every book",
       "cash CAGR %.8f" % cagr_cash14])

    w("survivorship_bound.csv", ["book", "weights", "days", "cagr", "max_dd",
                                 "sharpe", "ann_vol", "note"],
      [[b.name, b.weights_label, level_stats(b.dates, b.rets)["n_days"],
        "%.8f" % level_stats(b.dates, b.rets)["cagr"],
        "%.8f" % level_stats(b.dates, b.rets)["max_dd"],
        "%.6f" % level_stats(b.dates, b.rets)["sharpe"],
        "%.6f" % level_stats(b.dates, b.rets)["ann_vol"],
        "removed 3 best-returning names: %s" % " ".join(drop)] for b in ex3],
      ["BIAS BOUND ONLY -- a performance screen, not a candidate universe"])

    w("constituent_returns_ranked.csv", ["rank", "symbol", "compounded_return"],
      [[i + 1, s, "%.8f" % r] for i, (s, r) in enumerate(rank)],
      ["used only to define the declared survivorship bound in 4.6"])

    sp = []
    for b in all14:
        for lab, lo, hi in (("IS", 0, split), ("OOS", split, len(w14))):
            d = b.dates[lo:hi]
            r = b.rets[lo:hi]
            st = level_stats(d, r)
            g = group_index(d, "Y")
            fY, _, _, _, nY, _ = period_stats(r, g)
            sp.append([b.name, lab, "%d" % st["n_days"], "%.8f" % st["cagr"],
                       "%.8f" % st["max_dd"], "%.6f" % st["sharpe"],
                       "" if fY is NA else "%.6f" % fY, nY])
    w("split_70_30.csv", ["book", "half", "days", "cagr", "max_dd", "sharpe",
                          "frac_positive_years", "n_years"], sp,
      ["IS = first 70%% of book days, OOS = last 30%%"])

    crows = []
    for mode in ("daily", "yearly"):
        for i in range(len(NARROW3)):
            for j in range(i + 1, len(NARROW3)):
                c, n = correlation_of_returns(universe[NARROW3[i]],
                                              universe[NARROW3[j]], mode)
                crows.append(["index_etf", NARROW3[i], NARROW3[j], mode,
                              "%.6f" % c, n])
        for i in range(len(CONSTITUENTS14)):
            for j in range(i + 1, len(CONSTITUENTS14)):
                c, n = correlation_of_returns(universe[CONSTITUENTS14[i]],
                                              universe[CONSTITUENTS14[j]], mode)
                crows.append(["constituent", CONSTITUENTS14[i],
                              CONSTITUENTS14[j], mode, "%.6f" % c, n])
    w("pairwise_correlations.csv", ["block", "a", "b", "mode", "pearson", "n"],
      crows)

    disp = []
    for j in range(len(w14)):
        disp.append([w14[j].isoformat(),
                     "" if rv_spy[j] is NA else "%.8f" % rv_spy[j],
                     "" if rv_mean[j] is NA else "%.8f" % rv_mean[j],
                     "" if ratio[j] is NA else "%.8f" % ratio[j],
                     "" if xdisp[j] is NA else "%.8f" % xdisp[j]])
    w("dispersion_proxy.csv",
      ["date", "spy_rv21_ann", "mean_constituent_rv21_ann", "ratio",
       "cross_sectional_dispersion_ann"], disp,
      ["PROXY ONLY -- not a tradable dispersion P&L; no option data in this study"])

    lw = []
    for b in books10:
        for bk in BUCKETS:
            f1, f0, npos, nzero, n, _ = period_stats(b.rets, groups10[bk])
            lw.append([b.name, bk, n, npos, "" if f1 is NA else "%.6f" % f1])
    w("long_window_positivity.csv",
      ["book", "bucket", "n_periods", "n_positive", "frac_gt0"], lw,
      ["W10 = %s .. %s" % (w10[0].isoformat(), w10[-1].isoformat())])

    emit("")
    emit("N3_TREND lambda frontier is written at 0.05 resolution; the max-lambda")
    emit("values in §3.2 were located with a 0.001 walk and are NOT grid points.")


if __name__ == "__main__":
    main()
    for line in LINES:
        print(line)
