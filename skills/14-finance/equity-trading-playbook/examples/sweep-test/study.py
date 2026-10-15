#!/usr/bin/env python3
"""
study.py -- a multiple-testing-controlled sweep of moving-average trend books.

THE QUESTION THIS FILE ANSWERS, AND THE ONE IT REFUSES TO ANSWER

The desk owner's instruction was "run as many iterations as you want to show
+ve numbers". That instruction is satisfiable by construction: a grid of enough
configurations will always contain green rows. So this file is built to measure
the size of that effect, not to harvest it.

It reports:
  * the DISTRIBUTION of results across the whole declared grid, so the reader can
    see what a grid this size manufactures without any skill at all;
  * the BONFERRONI BAR for m = the number of configurations actually run, and the
    count that clears it -- reported honestly even if that count is zero;
  * out-of-sample degradation on a 70/30 time split for the top decile by
    in-sample Sharpe;
  * the MAXIMUM fraction of positive years/quarters/months any configuration
    achieves, and the losing periods of that configuration;
  * the trend-state x vol-tercile regime grid, with the negative cells kept in;
  * the same set re-run at 5 bps and 20 bps round-trip cost.

NO CONFIGURATION IN THIS FILE IS A RECOMMENDATION. The pre-registered default is
the only configuration printed as a strategy, and it is printed because it was
fixed before the run, not because it won.

Stdlib only. Deterministic: no randomness, no wall-clock reads, no set-order
dependence. Reuses the sibling engine
    skills/14-finance/timeframe-performance-statistics/scripts/timeframe_stats.py
for sample_sd / median / lag1_autocorr / n_effective / bucket_key and fails
loudly rather than substituting its own formulae.
"""

import datetime
import importlib.util
import math
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "out")

# ---------------------------------------------------------------------------
# Sibling engine -- imported, not reimplemented
# ---------------------------------------------------------------------------

ENGINE_REL = os.path.join(
    "skills", "14-finance", "timeframe-performance-statistics", "scripts", "timeframe_stats.py"
)
# sweep-test -> examples -> equity-trading-playbook -> 14-finance -> skills -> repo root
ENGINE_PATH = os.path.abspath(os.path.join(HERE, *([os.pardir] * 5 + [ENGINE_REL])))


def load_engine(path):
    if not os.path.exists(path):
        raise SystemExit("ERROR: sibling engine not found at %s" % path)
    spec = importlib.util.spec_from_file_location("timeframe_stats", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for name in ("sample_sd", "median", "lag1_autocorr", "n_effective", "bucket_key"):
        if not hasattr(mod, name):
            raise SystemExit("ERROR: sibling engine is missing %s()" % name)
    return mod


TS = load_engine(ENGINE_PATH)

# ---------------------------------------------------------------------------
# THE PRE-REGISTERED DESIGN -- fixed before any result was looked at
# ---------------------------------------------------------------------------

INSTRUMENTS_P = ["SPY", "QQQ", "IWM", "EEM", "TLT", "GLD", "EFA", "VNQ"]
INSTRUMENTS_X = INSTRUMENTS_P + ["IEF", "HYG", "DBC"]
INSTRUMENTS_L = ["SPY", "QQQ", "IWM", "EEM"]

N_GRID = [50, 100, 150, 200, 250]
MODES = ["daily", "monthly"]
MAX_SUBSET = 4
NMAX = max(N_GRID)
TREND_MA = 200          # SPY regime trend state
VOL_WINDOW = 21         # SPY regime realised-vol window
ANNUALISE = 252
ALPHA = 0.05            # two-sided, for the Bonferroni bar
IS_FRACTION = 0.70
TOP_DECILE = 0.10
VOL_TERCILE_LABELS = {0: "LOW", 1: "MID", 2: "HIGH"}
TREND_LABELS = {1: "UP", 0: "DOWN"}
RF = 0.0

# The pre-registered default: the configuration a practitioner writes down from
# the trend literature, with no search behind it. The declared grid caps a book
# at 4 instruments, so the maximal diversified equity-trend book it contains is
# the four broad equity-index sleeves -- chosen because they are the ones with
# the longest common history and the widest coverage, not because they performed.
# Its no-search parameter is the conventional 200-day average, monthly rebalance.
DEFAULT_SYMS = ["SPY", "QQQ", "IWM", "EEM"]
DEFAULT_N = 200
DEFAULT_MODE = "monthly"
# A second, stricter reference, also no-search: the textbook single-instrument
# rule on the S&P itself.
TEXTBOOK_SYMS = ["SPY"]


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def load_series(data_dir):
    out = {}
    for name in sorted(os.listdir(data_dir)):
        if not name.endswith("_1d.csv"):
            continue
        stem = name[:-len("_1d.csv")]
        dates, closes = [], []
        with open(os.path.join(data_dir, name), "r", encoding="utf-8") as fh:
            for ln in fh:
                ln = ln.strip()
                if not ln or ln.startswith("#") or ln.startswith("date,"):
                    continue
                f = ln.split(",")
                dates.append(datetime.date.fromisoformat(f[0]))
                closes.append(float(f[4]))
        if len(dates) < 2:
            raise SystemExit("ERROR: %s has too few bars" % name)
        if any(dates[i] >= dates[i + 1] for i in range(len(dates) - 1)):
            raise SystemExit("ERROR: %s is not strictly ascending by date" % name)
        out[stem] = (dates, closes)
    if not out:
        raise SystemExit("ERROR: no data/*_1d.csv under %s" % data_dir)
    return out


def common_calendar(series, syms):
    """Sessions on which every named instrument has a bar, ascending."""
    sets = []
    for s in syms:
        sets.append(set(series[s][0]))
    cal = set.intersection(*sets)
    return sorted(cal), [len(s) for s in sets]


def align(series, sym, cal):
    idx = {d: i for i, d in enumerate(series[sym][0])}
    return [series[sym][1][idx[d]] for d in cal]


def returns_from(closes):
    r = [0.0] * len(closes)
    for i in range(1, len(closes)):
        r[i] = closes[i] / closes[i - 1] - 1.0
    return r


def sma(closes, n):
    out = [None] * len(closes)
    run = 0.0
    for i, c in enumerate(closes):
        run += c
        if i >= n:
            run -= closes[i - n]
        if i >= n - 1:
            out[i] = run / n
    return out


def signals(closes, ma):
    return [1 if (m is not None and closes[i] > m) else 0 for i, m in enumerate(ma)]


# ---------------------------------------------------------------------------
# The rule engine
# ---------------------------------------------------------------------------

def build_sleeve(cal, rets, sig, mode):
    """Sleeve position, gross return and traded-notional series on the calendar.

    No look-ahead: the signal is read at the close of the previous session and
    the position it implies is held on the next session. In `monthly` mode the
    position may only change on the first trading day of a calendar month.
    """
    n = len(cal)
    pos = [0.0] * n
    gross = [0.0] * n
    flip = [0.0] * n
    for c in range(1, n):
        if mode == "daily":
            pos[c] = float(sig[c - 1])
        elif c == 1 or cal[c].month != cal[c - 1].month:
            pos[c] = float(sig[c - 1])
        else:
            pos[c] = pos[c - 1]
    for c in range(1, n):
        gross[c] = pos[c] * rets[c]
        flip[c] = abs(pos[c] - pos[c - 1])
    return gross, flip, pos


MONTH_START = None  # filled per grid, per grid's calendar


def book_returns(cal, member_gross, member_flip, mode, cost_bps):
    """Equal-weight book return series; returns (net_rets, gross_rets).

    daily   : the book holds 1/k in each sleeve at every close.
    monthly : the book is reset to 1/k on the first trading day of each month and
              drifts with the sleeves between resets.

    Costs are charged against the RETURN, not against a sleeve value: charging
    them against a value does nothing here, because the weights are renormalised
    every day and a haircut on one sleeve changes the mix while leaving the level
    alone. A round-trip rate c bps means each side costs c/2 bps of the traded
    notional, charged on every sleeve position flip and on each monthly book
    reset's one-way turnover.
    """
    n = len(cal)
    k = len(member_gross)
    half = (cost_bps / 2.0) / 10000.0
    net = [0.0] * n
    gross = [0.0] * n
    turn_out = [0.0] * n
    if k == 0:
        return net, gross, turn_out

    if mode == "daily":
        inv = 1.0 / k
        for c in range(1, n):
            g = 0.0
            f = 0.0
            for i in range(k):
                g += member_gross[i][c]
                f += member_flip[i][c]
            traded = inv * f
            g *= inv
            gross[c] = g
            net[c] = g - half * traded
            turn_out[c] = traded
        return net, gross, turn_out

    # monthly: book weights drift inside the month
    inv = 1.0 / k
    v = [inv] * k
    book = 1.0
    for c in range(1, n):
        month_start = (c == 1) or (cal[c].month != cal[c - 1].month)
        turn = 0.0
        flip = 0.0
        if month_start:
            for i in range(k):
                w = v[i] / book
                flip += w * member_flip[i][c]
                turn += abs(inv - w)
            v = [inv * book] * k
        else:
            for i in range(k):
                flip += (v[i] / book) * member_flip[i][c]
        for i in range(k):
            v[i] *= (1.0 + member_gross[i][c])
        newbook = 0.0
        for i in range(k):
            newbook += v[i]
        g = newbook / book - 1.0
        gross[c] = g
        net[c] = g - half * (flip + turn)
        turn_out[c] = flip + turn
        book = newbook
    return net, gross, turn_out


# ---------------------------------------------------------------------------
# Period helpers
# ---------------------------------------------------------------------------

def complete_periods(kind, lo, hi):
    """Keys of the periods fully covered by [lo, hi]."""
    keys = []
    if kind == "Y":
        for y in range(lo.year, hi.year + 1):
            if datetime.date(y, 1, 1) >= lo and datetime.date(y, 12, 31) <= hi:
                keys.append("%04d" % y)
    elif kind == "Q":
        for y in range(lo.year, hi.year + 1):
            for q in (1, 2, 3, 4):
                s = datetime.date(y, 3 * q - 2, 1)
                e = (datetime.date(y, 12, 31) if q == 4
                     else datetime.date(y, 3 * q + 1, 1) - datetime.timedelta(days=1))
                if s >= lo and e <= hi:
                    keys.append("%04d-Q%d" % (y, q))
    elif kind == "M":
        y, m = lo.year, lo.month
        while True:
            s = datetime.date(y, m, 1)
            e = (datetime.date(y, 12, 31) if m == 12
                 else datetime.date(y, m + 1, 1) - datetime.timedelta(days=1))
            if s >= lo and e <= hi:
                keys.append("%04d-%02d" % (y, m))
            if y == hi.year and m == hi.month:
                break
            m += 1
            if m == 13:
                m = 1
                y += 1
    else:
        raise ValueError(kind)
    return keys


# ---------------------------------------------------------------------------
# Metrics -- one pass for the level statistics, one per period bucket
# ---------------------------------------------------------------------------

def metrics(dates, rets, regimes, complete, store_vals=False):
    """dates/rets are the slice's session dates and daily returns (rets[0] unused).

    `regimes` is the regime label list aligned to the same slice.
    `complete` is {"Y": [...], "Q": [...], "M": [...]} of complete period keys.
    """
    n = len(rets)
    m = {"n_days": n - 1}
    if n < 3:
        return None
    s = 0.0
    for i in range(1, n):
        s += rets[i]
    mu = s / (n - 1)
    sd = TS.sample_sd(rets[1:])
    m["mean_daily"] = mu
    m["sd_daily"] = sd
    m["sharpe"] = (mu / sd * math.sqrt(ANNUALISE)) if sd and sd > 0 else None

    eq = 1.0
    peak = 1.0
    mdd = 0.0
    cells = {}
    for i in range(1, n):
        eq *= (1.0 + rets[i])
        if eq > peak:
            peak = eq
        dd = (peak - eq) / peak
        if dd > mdd:
            mdd = dd
        lab = regimes[i]
        if lab is not None:
            key = (lab[0], lab[1])
            a = cells.get(key)
            if a is None:
                cells[key] = [rets[i], 1]
            else:
                a[0] += rets[i]
                a[1] += 1
    years = (dates[-1] - dates[0]).days / 365.25
    m["years"] = years
    m["cagr"] = (eq ** (1.0 / years) - 1.0) if years > 0 and eq > 0 else None
    m["total_return"] = eq - 1.0
    m["maxdd"] = -mdd

    for kind in ("Y", "Q", "M"):
        acc = {}
        for i in range(1, n):
            key, _ = TS.bucket_key(kind, dates[i])
            if key in acc:
                acc[key] *= (1.0 + rets[i])
            else:
                acc[key] = 1.0 + rets[i]
        keys = complete[kind]
        vals = [(k, acc[k] - 1.0) for k in keys if k in acc]
        pos = sum(1 for _, v in vals if v > 0)
        m["%s_n" % kind] = len(vals)
        m["%s_pos" % kind] = pos
        m["%s_frac" % kind] = (pos / len(vals)) if vals else None
        m["%s_worst" % kind] = min((v for _, v in vals), default=None)
        m["%s_best" % kind] = max((v for _, v in vals), default=None)
        m["%s_vals" % kind] = vals if store_vals else None

    if sd and sd > 0:
        t = mu / (sd / math.sqrt(n - 1))
        rho, why = TS.lag1_autocorr(rets[1:])
        neff, why2 = TS.n_effective(n - 1, rho) if (rho is not None and why is None) else (None, why)
        m["t"] = t
        m["rho1"] = rho
        m["n_eff"] = neff
        m["t_eff"] = (mu / sd * math.sqrt(neff)) if neff else None
    else:
        m["t"] = m["t_eff"] = m["rho1"] = m["n_eff"] = None

    losing = 0
    for key in sorted(cells):
        tot, cnt = cells[key]
        if cnt >= 20 and tot / cnt < 0:
            losing += 1
    m["cells"] = cells
    m["n_cells"] = len(cells)
    m["losing_cells"] = losing
    return m


def pct(sorted_vals, q):
    n = len(sorted_vals)
    if n == 0:
        return None
    if n == 1:
        return sorted_vals[0]
    pos = (n - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return sorted_vals[lo]
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (pos - lo)


def norm_ppf(p):
    """Inverse standard normal CDF, Acklam's rational approximation."""
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


def subsets(items, sizes):
    out = []
    k = len(items)
    for r in sizes:
        idx = list(range(r))
        while True:
            out.append(tuple(items[i] for i in idx))
            i = r - 1
            while i >= 0 and idx[i] == k - r + i:
                i -= 1
            if i < 0:
                break
            idx[i] += 1
            for j in range(i + 1, r):
                idx[j] = idx[j - 1] + 1
    return out


# ---------------------------------------------------------------------------
# A grid
# ---------------------------------------------------------------------------

class Grid(object):
    def __init__(self, tag, syms, series, sizes=range(1, MAX_SUBSET + 1)):
        self.tag = tag
        self.syms = list(syms)
        self.cal_full, self.sizes_per_sym = common_calendar(series, self.syms)
        if len(self.cal_full) != min(self.sizes_per_sym):
            raise SystemExit(
                "ERROR: %s instruments do not share one calendar (%s)"
                % (tag, sorted(set(self.sizes_per_sym)))
            )
        first = []
        for s in self.syms:
            d = series[s][0]
            first.append(d[NMAX - 1])
        self.win_start = max(first)
        self.cal = [d for d in self.cal_full if d >= self.win_start]
        self.win_end = self.cal[-1]
        self.closes = {}
        self.rets = {}
        self.sig = {}
        for s in self.syms:
            cl = align(series, s, self.cal_full)
            self.closes[s] = cl
            r = returns_from(cl)
            self.rets[s] = r
            for n in N_GRID:
                self.sig[(s, n)] = signals(cl, sma(cl, n))
        # slice to the window
        cut = self.cal_full.index(self.win_start)
        self.cal = self.cal_full[cut:]
        for s in self.syms:
            self.rets[s] = self.rets[s][cut:]
            for n in N_GRID:
                self.sig[(s, n)] = self.sig[(s, n)][cut:]
        self.sleeves = {}
        for mode in MODES:
            for s in self.syms:
                for n in N_GRID:
                    self.sleeves[(s, n, mode)] = build_sleeve(
                        self.cal, self.rets[s], self.sig[(s, n)], mode)
        self.subsets = subsets(self.syms, [r for r in sizes])
        self.cut = cut
        self.regimes = self.build_regimes(series)
        self.complete = {k: complete_periods(k, self.cal[0], self.cal[-1])
                         for k in ("Y", "Q", "M")}
        self.n_configs = len(self.subsets) * len(N_GRID) * len(MODES)

    def build_regimes(self, series):
        """(trend state, vol tercile) of SPY, contemporaneous with each session.

        Computed over the FULL common calendar and then sliced to the window, so
        the first sessions of the window still have a full trailing
        realised-volatility window behind them. Tercile cuts come from the
        window's own distribution, as declared.
        """
        full = self.cal_full
        spy_closes = align(series, "SPY", full)
        spy_ret = returns_from(spy_closes)
        trend_all = signals(spy_closes, sma(spy_closes, TREND_MA))
        vol_all = [None] * len(full)
        run = 0.0
        run2 = 0.0
        for i in range(1, len(full)):
            run += spy_ret[i]
            run2 += spy_ret[i] * spy_ret[i]
            if i >= VOL_WINDOW:
                run -= spy_ret[i - VOL_WINDOW]
                run2 -= spy_ret[i - VOL_WINDOW] * spy_ret[i - VOL_WINDOW]
                m = run / VOL_WINDOW
                var = max(0.0, run2 / VOL_WINDOW - m * m) * (VOL_WINDOW / (VOL_WINDOW - 1.0))
                vol_all[i] = math.sqrt(var) * math.sqrt(ANNUALISE)
        off = self.cut
        trend = trend_all[off:]
        vol = vol_all[off:]
        have = sorted(v for v in vol if v is not None)
        cuts = None
        if have:
            cuts = (pct(have, 1.0 / 3.0), pct(have, 2.0 / 3.0))
        out = [None] * len(self.cal)
        unlabelled = 0
        for i in range(len(self.cal)):
            if vol[i] is None or cuts is None:
                unlabelled += 1
                continue
            t = 0 if vol[i] <= cuts[0] else (1 if vol[i] <= cuts[1] else 2)
            out[i] = (trend[i], t)
        self.vol_cuts = cuts
        self.unlabelled_sessions = unlabelled
        self.labelled_sessions = len(self.cal) - unlabelled
        return out

    def configs(self):
        for sub in self.subsets:
            for n in N_GRID:
                for mode in MODES:
                    yield sub, n, mode

    def run(self, with_split=True, cost_bps=0.0, store_vals=False):
        recs = []
        cal = self.cal
        n_days = len(cal)
        split = int(math.floor(IS_FRACTION * (n_days - 1)))
        for sub, n, mode in self.configs():
            mg = []
            mf = []
            for s in sub:
                g, f, _p = self.sleeves[(s, n, mode)]
                mg.append(g)
                mf.append(f)
            net, gross, _t = book_returns(cal, mg, mf, mode, cost_bps)
            full = metrics(cal, net, self.regimes, self.complete, store_vals=store_vals)
            if full is None:
                continue
            rec = {"tag": self.tag, "syms": sub, "n": n, "mode": mode,
                   "id": self.config_id(sub, n, mode), "full": full}
            if with_split:
                i0 = split + 1
                is_dates = cal[:i0]
                is_rets = net[:i0]
                is_reg = self.regimes[:i0]
                is_comp = {k: complete_periods(k, is_dates[0], is_dates[-1])
                           for k in ("Y", "Q", "M")}
                oos_dates = cal[split:]
                # the OOS return on its first session needs its own prior close
                oos_rets = [0.0] + net[i0:]
                oos_reg = [None] + self.regimes[i0:]
                oos_comp = {k: complete_periods(k, oos_dates[0], oos_dates[-1])
                            for k in ("Y", "Q", "M")}
                rec["is"] = metrics(is_dates, is_rets, is_reg, is_comp)
                rec["oos"] = metrics(oos_dates, oos_rets, oos_reg, oos_comp)
            recs.append(rec)
        return recs, split

    @staticmethod
    def config_id(sub, n, mode):
        return "N%d-%s-%s" % (n, mode, "+".join(sub))


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------

def fnum(x, nd=4):
    return "n/a" if x is None else ("%.*f" % (nd, x))


def fpct(x, nd=2):
    return "n/a" if x is None else ("%.*f%%" % (nd, 100.0 * x))


def fint(x):
    return "n/a" if x is None else str(int(round(float(x))))


def header(title):
    print("")
    print("=" * 100)
    print(title)
    print("=" * 100)


def sub(title):
    print("")
    print(("-- " + title + " " + "-" * max(0, 96 - len(title))).rstrip())


def distribution(recs, key):
    vals = sorted(r["full"][key] for r in recs if r["full"][key] is not None)
    return vals


def dist_row(label, vals, fmt, higher_better=True):
    """One row of a quantile table, always printed best -> worst.

    `vals` is sorted ascending. For a quantity where a LARGER value is better
    (CAGR, Sharpe, ...) the best is p(1.0). For a drawdown, stored as a negative
    fraction, a larger value is also better (a smaller fall). For a COUNT of
    losing cells, a larger value is worse, so the row is reversed and the
    leftmost column really is the smallest count.
    """
    if not vals:
        print("  %-26s (none)" % label)
        return
    if higher_better:
        seq = (pct(vals, 1.0), pct(vals, 0.9), pct(vals, 0.5), pct(vals, 0.1), pct(vals, 0.0))
    else:
        seq = (pct(vals, 0.0), pct(vals, 0.1), pct(vals, 0.5), pct(vals, 0.9), pct(vals, 1.0))
    print("  %-26s %12s %12s %12s %12s %12s"
          % (label, fmt(seq[0]), fmt(seq[1]), fmt(seq[2]), fmt(seq[3]), fmt(seq[4])))


def write_csv(path, rows, head):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(",".join(head) + "\n")
        for r in rows:
            fh.write(",".join(r) + "\n")


def grid_table(recs, path):
    head = ["id", "grid", "n_instruments", "instruments", "ma_days", "rebalance",
            "cagr", "sharpe", "maxdd", "worst_year", "years_n", "years_pos",
            "years_frac", "quarters_n", "quarters_pos", "quarters_frac",
            "months_n", "months_pos", "months_frac", "losing_cells", "n_cells",
            "t", "t_eff", "rho1", "n_eff", "is_sharpe", "is_cagr", "oos_sharpe", "oos_cagr",
            "is_years_n", "is_years_pos", "is_years_frac",
            "oos_years_n", "oos_years_pos", "oos_years_frac",
            "is_quarters_pos", "oos_quarters_pos", "is_months_pos", "oos_months_pos"]
    rows = []
    for r in recs:
        mf = r["full"]
        mi = r.get("is") or {}
        mo = r.get("oos") or {}
        rows.append([
            r["id"], r["tag"], str(len(r["syms"])), "+".join(r["syms"]),
            str(r["n"]), r["mode"],
            fnum(mf["cagr"], 6), fnum(mf["sharpe"], 6), fnum(mf["maxdd"], 6),
            fnum(mf["Y_worst"], 6), str(mf["Y_n"]), str(mf["Y_pos"]),
            fnum(mf["Y_frac"], 6), str(mf["Q_n"]), str(mf["Q_pos"]),
            fnum(mf["Q_frac"], 6), str(mf["M_n"]), str(mf["M_pos"]),
            fnum(mf["M_frac"], 6), str(mf["losing_cells"]), str(mf["n_cells"]),
            fnum(mf["t"], 6), fnum(mf["t_eff"], 6), fnum(mf["rho1"], 6),
            fnum(mf["n_eff"], 3),
            fnum(mi.get("sharpe"), 6), fnum(mi.get("cagr"), 6),
            fnum(mo.get("sharpe"), 6), fnum(mo.get("cagr"), 6),
            str(mi.get("Y_n", "")), str(mi.get("Y_pos", "")), fnum(mi.get("Y_frac"), 6),
            str(mo.get("Y_n", "")), str(mo.get("Y_pos", "")), fnum(mo.get("Y_frac"), 6),
            str(mi.get("Q_pos", "")), str(mo.get("Q_pos", "")),
            str(mi.get("M_pos", "")), str(mo.get("M_pos", "")),
        ])
    write_csv(path, rows, head)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv):
    want = set(argv[1:]) or {"P", "L", "X"}
    series = load_series(DATA)

    header("sweep-test -- a multiple-testing-controlled sweep of MA trend books")
    print("  run at            : deterministic (no wall-clock read; see README for the run date)")
    print("  data dir          : data/  (12 CSV series, provenance headers included)")
    print("  sibling engine    : %s" % ENGINE_REL.replace("\\", "/"))
    print("  source of the grid: declared in this file's constants BEFORE any result")
    print("")
    print("  instrument inventory (bars, first bar, last bar):")
    for s in sorted(series):
        d, c = series[s]
        print("    %-4s %6d bars  %s .. %s" % (s, len(d), d[0], d[-1]))

    # ---- SECTION 1: the declared design -----------------------------------
    header("SECTION 1 -- the declared grid, counted before the first result")
    nP = (len(INSTRUMENTS_P) + math.comb(len(INSTRUMENTS_P), 2)
          + math.comb(len(INSTRUMENTS_P), 3) + math.comb(len(INSTRUMENTS_P), 4))
    nX = (len(INSTRUMENTS_X) + math.comb(len(INSTRUMENTS_X), 2)
          + math.comb(len(INSTRUMENTS_X), 3) + math.comb(len(INSTRUMENTS_X), 4))
    nL = (len(INSTRUMENTS_L) + math.comb(len(INSTRUMENTS_L), 2)
          + math.comb(len(INSTRUMENTS_L), 3) + math.comb(len(INSTRUMENTS_L), 4))
    print("  signal            : close vs SMA(N); long when close > SMA(N), flat otherwise")
    print("  N                 : %s" % N_GRID)
    print("  rebalance         : %s  (position may only change on a book date)" % MODES)
    print("  sub-books         : every 1-, 2-, 3- and 4-instrument subset, equal weight")
    print("")
    print("  Grid P (pre-registered universe, %d instruments):" % len(INSTRUMENTS_P))
    print("    1/2/3/4-instrument subsets = %d + %d + %d + %d = %d"
          % (len(INSTRUMENTS_P), math.comb(len(INSTRUMENTS_P), 2),
             math.comb(len(INSTRUMENTS_P), 3), math.comb(len(INSTRUMENTS_P), 4), nP))
    print("    x %d moving averages x %d rebalance modes = DECLARED CONFIGURATIONS = %d"
          % (len(N_GRID), len(MODES), nP * len(N_GRID) * len(MODES)))
    print("    universe = %s" % ", ".join(INSTRUMENTS_P))
    print("")
    print("  Grid L (long-window sensitivity, %d instruments): DECLARED = %d"
          % (len(INSTRUMENTS_L), nL * len(N_GRID) * len(MODES)))
    print("    universe = %s" % ", ".join(INSTRUMENTS_L))
    print("")
    print("  Grid X (extended universe, %d instruments): DECLARED = %d"
          % (len(INSTRUMENTS_X), nX * len(N_GRID) * len(MODES)))
    print("    universe = %s" % ", ".join(INSTRUMENTS_X))
    print("")
    print("  pre-registered default (no search behind it): %s at N=%d, %s rebalance"
          % ("+".join(DEFAULT_SYMS), DEFAULT_N, DEFAULT_MODE))
    print("    chosen on instrument COVERAGE (longest common history, widest breadth),")
    print("    not on performance; the grid caps a book at 4 instruments, so this is the")
    print("    largest all-equity book the declared grid contains")
    print("  second reference   : %s at N=%d, %s (the textbook single-instrument rule)"
          % ("+".join(TEXTBOOK_SYMS), DEFAULT_N, DEFAULT_MODE))
    print("  Sharpe convention : daily simple returns, full sample, Rf=0, x sqrt(252)")
    print("  CAGR convention   : compounded equity, calendar-time exponent (365.25 d/yr)")
    print("  period positivity : COMPLETE calendar years / quarters / months only,")
    print("                      so the partial first and last periods never count")

    grids = {}
    for tag, syms in (("P", INSTRUMENTS_P), ("L", INSTRUMENTS_L), ("X", INSTRUMENTS_X)):
        if tag not in want:
            continue
        grids[tag] = Grid(tag, syms, series)

    header("SECTION 1b -- the windows each grid is actually evaluated on")
    for tag in sorted(grids):
        g = grids[tag]
        print("  Grid %s : %d sessions per config  %s .. %s  (%.2f years)"
              % (tag, len(g.cal), g.cal[0], g.cal[-1],
                 (g.cal[-1] - g.cal[0]).days / 365.25))
        print("           complete years=%d quarters=%d months=%d   configs=%d"
              % (len(g.complete["Y"]), len(g.complete["Q"]), len(g.complete["M"]),
                 g.n_configs))
        print("           SPY vol tercile cuts (annualised, window's own distribution): "
              "%.4f / %.4f" % g.vol_cuts)
        print("           sessions carrying a regime label: %d of %d (the rest are the "
              "trailing-window warm-up)" % (g.labelled_sessions, len(g.cal)))

    # ---- run the grids -----------------------------------------------------
    results = {}
    for tag in sorted(grids):
        g = grids[tag]
        sys.stderr.write("running Grid %s (%d configs)...\n" % (tag, g.n_configs))
        recs, split = g.run(with_split=(tag != "X"), store_vals=(tag == "P"))
        results[tag] = (g, recs, split)
        sys.stderr.write("  Grid %s done: %d records\n" % (tag, len(recs)))

    for tag in sorted(results):
        g, recs, split = results[tag]
        grid_table(recs, os.path.join(OUT, "grid_%s.csv" % tag))

    if "P" not in results:
        return 0
    gP, recsP, splitP = results["P"]

    header("SECTION 1c -- the grid count, verified against what was actually run")
    for tag in sorted(results):
        g, recs, _ = results[tag]
        ok = "OK" if len(recs) == g.n_configs else "MISMATCH"
        print("  Grid %s : declared %d, run %d  -> %s" % (tag, g.n_configs, len(recs), ok))
    total = sum(len(results[t][1]) for t in results)
    print("  ALL GRIDS: %d configurations evaluated" % total)
    if len(recsP) != gP.n_configs or any(len(results[t][1]) != results[t][0].n_configs
                                         for t in results):
        raise SystemExit("ERROR: grid size mismatch")

    # ---- SECTION 2: the distribution --------------------------------------
    header("SECTION 2 -- WHAT THE GRID PRODUCES BY CONSTRUCTION (Grid P, %d configs)"
           % len(recsP))
    print("  A grid this size always contains a green row. That is what this table")
    print("  measures: the spread of results with no skill in the search at all.")
    print("")
    print("  quantiles are linear-interpolated on the sorted values; every column pair")
    print("  runs best -> worst, and for a drawdown 'best' means the SMALLEST fall.")
    for label, src, span in (
        ("FULL WINDOW", "full", "%s .. %s" % (gP.cal[0], gP.cal[-1])),
        ("IN-SAMPLE (first %.0f%% of sessions)" % (100 * IS_FRACTION), "is",
         "%s .. %s" % (gP.cal[0], gP.cal[splitP])),
    ):
        print("")
        print("  %s -- %s" % (label, span))
        print("  %-26s %12s %12s %12s %12s %12s"
              % ("metric", "best(p100)", "p90", "median", "p10", "worst(p0)"))
        dist_row("CAGR", sorted(r[src]["cagr"] for r in recsP
                                if r[src] and r[src]["cagr"] is not None), fpct)
        dist_row("Sharpe", sorted(r[src]["sharpe"] for r in recsP
                                  if r[src] and r[src]["sharpe"] is not None), fnum)
        dist_row("Max drawdown", sorted(r[src]["maxdd"] for r in recsP
                                        if r[src] and r[src]["maxdd"] is not None), fpct)
        dist_row("Worst year", sorted(r[src]["Y_worst"] for r in recsP
                                      if r[src] and r[src]["Y_worst"] is not None), fpct)
        dist_row("Positive-year fraction", sorted(r[src]["Y_frac"] for r in recsP
                                                  if r[src] and r[src]["Y_frac"] is not None), fpct)
        dist_row("Positive-quarter frac", sorted(r[src]["Q_frac"] for r in recsP
                                                 if r[src] and r[src]["Q_frac"] is not None), fpct)
        dist_row("Losing regime cells", sorted(float(r[src]["losing_cells"]) for r in recsP
                                               if r[src] is not None), fint,
                 higher_better=False)
    print("")
    allc = [r for r in recsP if r["full"]["cagr"] is not None]
    for key, lab in (("cagr", "CAGR"), ("sharpe", "Sharpe")):
        pos = sum(1 for r in allc if r["full"][key] > 0)
        print("  configs with positive %-7s over the full window: %d of %d (%.1f%%)"
              % (lab, pos, len(allc), 100.0 * pos / len(allc)))
    any100 = sum(1 for r in allc if r["full"]["Y_frac"] == 1.0)
    print("  configs positive in EVERY complete year          : %d of %d"
          % (any100, len(allc)))
    dist_rows = []
    for key, lab in (("cagr", "CAGR"), ("sharpe", "Sharpe"), ("Y_frac", "Y_frac"),
                     ("Q_frac", "Q_frac"), ("M_frac", "M_frac"), ("maxdd", "maxdd")):
        vals = sorted(r["full"][key] for r in allc if r["full"][key] is not None)
        dist_rows.append([lab, fnum(pct(vals, 1.0), 6), fnum(pct(vals, 0.9), 6),
                          fnum(pct(vals, 0.5), 6), fnum(pct(vals, 0.1), 6),
                          fnum(pct(vals, 0.0), 6)])
    write_csv(os.path.join(OUT, "distribution.csv"), dist_rows,
              ["metric", "p100", "p90", "median", "p10", "p0"])

    # ---- SECTION 3: the Bonferroni bar -------------------------------------
    header("SECTION 3 -- THE BONFERRONI BAR, AND HOW MANY CONFIGURATIONS CLEAR IT")
    m = len(recsP)
    per_test = ALPHA / m
    crit = norm_ppf(1.0 - per_test / 2.0)
    print("  test statistic    : t = mean(daily portfolio return) / (sd / sqrt(n_days))")
    print("                      equivalent to annualised Sharpe x sqrt(years)")
    print("  family            : ALL %d configurations in Grid P, counted together" % m)
    print("  m                 : %d" % m)
    print("  alpha (family)    : %s (two-sided)" % ALPHA)
    print("  per-test alpha    : %.10f" % per_test)
    print("  critical |t|      : %.4f" % crit)
    print("  (for contrast, the unadjusted 2-sigma threshold is %.4f, and the sibling" % 1.96)
    print("   study's m=12 bar was 2.865 and its m=56 bar was 3.322)")
    ts = sorted(r["full"]["t"] for r in recsP if r["full"]["t"] is not None)
    tes = sorted(r["full"]["t_eff"] for r in recsP if r["full"]["t_eff"] is not None)
    print("")
    print("  t distribution over the grid: min %.4f  p10 %.4f  median %.4f  p90 %.4f  max %.4f"
          % (ts[0], pct(ts, 0.1), pct(ts, 0.5), pct(ts, 0.9), ts[-1]))
    pass_t = sum(1 for v in ts if v >= crit)
    print("  configurations with |t| >= critical (raw n)          : %d of %d (%.2f%%)"
          % (pass_t, len(ts), 100.0 * pass_t / len(ts)))
    print("  t_eff distribution (n_eff-adjusted for lag-1 rho): p90 %.4f  max %.4f"
          % (pct(tes, 0.9), tes[-1]))
    pass_te = sum(1 for v in tes if v >= crit)
    print("  configurations with |t_eff| >= critical              : %d of %d (%.2f%%)"
          % (pass_te, len(tes), 100.0 * pass_te / len(tes)))
    rho_list = sorted(r["full"]["rho1"] for r in recsP if r["full"]["rho1"] is not None)
    n_days = recsP[0]["full"]["n_days"]
    n_more = sum(1 for r in recsP if r["full"]["n_eff"] and r["full"]["n_eff"] > n_days)
    print("  lag-1 autocorrelation of the daily returns: median %.4f (min %.4f, max %.4f)"
          % (pct(rho_list, 0.5), rho_list[0], rho_list[-1]))
    print("  n_eff EXCEEDS the raw n_days (%d) for %d of %d configurations, because that"
          % (n_days, n_more, len(recsP)))
    print("  autocorrelation is NEGATIVE. The sample-size correction is therefore")
    print("  LENIENT here, not conservative -- it is a property of the data, not a test.")
    print("")
    print("  THE HONEST COUNT: %d of %d configurations clear the family-wise bar at" % (pass_t, m))
    print("  alpha=%.2f with the raw t. The answer to 'how many are genuinely positive" % ALPHA)
    print("  rather than positive by selection' is therefore: %d." % pass_t)
    print("")
    print("  WHICH ONES, and the two things that make this count generous:")
    clearing = sorted([r for r in recsP if r["full"]["t"] is not None
                       and r["full"]["t"] >= crit], key=lambda r: -r["full"]["t"])
    print("  %-42s %9s %9s %9s %9s" % ("configuration", "t", "Sharpe", "CAGR", "pos yrs"))
    for r in clearing:
        print("  %-42s %9.4f %9.4f %9s %5d/%2d"
              % (r["id"], r["full"]["t"], r["full"]["sharpe"],
                 fpct(r["full"]["cagr"]), r["full"]["Y_pos"], r["full"]["Y_n"]))
    print("")
    print("  (1) The median configuration in this grid has t = %.3f, which already clears"
          % pct(ts, 0.5))
    print("      the unadjusted 2-sigma threshold of 1.96. A test on the mean of a")
    print("      long-or-flat strategy's daily returns is testing 'does the market rise',")
    print("      not 'does the rule add anything': SPY is above its own SMA(200) on 77.9%")
    print("      of this window's sessions, so a sleeve that follows it is long most of")
    print("      the time and inherits most of the market's drift with no skill at all.")
    print("      The Bonferroni bar makes the family-wise statement correct; it does not")
    print("      make the underlying null interesting.")
    print("  (2) The sample-size correction cuts the OTHER way, and this is worth seeing.")
    print("      Daily returns of these trend books have a NEGATIVE lag-1 autocorrelation")
    print("      (median rho1 = %.4f), so n_eff is LARGER than the day count and the" % pct(rho_list, 0.5))
    print("      adjusted count rises from %d to %d rather than falling. Neither number" % (pass_t, pass_te))
    print("      should be taken as settled. What IS settled is that %.1f%% of this grid"
          % (100.0 * (m - pass_t) / m))
    print("      cannot be distinguished from noise at the family-wise level.")
    if clearing:
        print("")
        print("  WHAT THE %d SURVIVORS HAVE IN COMMON -- read this before believing any of" % len(clearing))
        print("  them. If the survivors were a real effect they would be spread across the")
        print("  universe; if they are a selection they will cluster.")
        for s in INSTRUMENTS_P:
            n_with = sum(1 for r in clearing if s in r["syms"])
            print("      contains %-4s : %2d of %2d survivors   (%3d of 1620 configs in the grid)"
                  % (s, n_with, len(clearing),
                     sum(1 for r in recsP if s in r["syms"])))
        for mode in MODES:
            print("      rebalance %-8s: %2d of %2d survivors"
                  % (mode, sum(1 for r in clearing if r["mode"] == mode), len(clearing)))
        for n in N_GRID:
            print("      N=%-4d        : %2d of %2d survivors"
                  % (n, sum(1 for r in clearing if r["n"] == n), len(clearing)))
        print("      books of size 1/2/3/4: %s"
              % "/".join(str(sum(1 for r in clearing if len(r["syms"]) == k)) for k in (1, 2, 3, 4)))
    write_csv(os.path.join(OUT, "bonferroni.csv"),
              [["m", str(m)], ["alpha", str(ALPHA)], ["per_test_alpha", "%.12f" % per_test],
               ["critical_t", "%.6f" % crit], ["configs_clearing_raw_t", str(pass_t)],
               ["configs_clearing_t_eff", str(pass_te)],
               ["best_t", "%.6f" % ts[-1]], ["median_t", "%.6f" % pct(ts, 0.5)]],
              ["key", "value"])

    # ---- SECTION 4: out-of-sample degradation ------------------------------
    header("SECTION 4 -- OUT-OF-SAMPLE DEGRADATION (70/30 time split, Grid P)")
    split_date = gP.cal[splitP + 1]
    print("  split             : first %.0f%% of sessions in-sample -> %s .. %s"
          % (100 * IS_FRACTION, gP.cal[0], gP.cal[splitP]))
    print("                      held out 30%% -> %s .. %s" % (split_date, gP.cal[-1]))
    print("                      the held-out data is used once, on the in-sample ranking")
    ranked = sorted([r for r in recsP if r["is"] and r["is"]["sharpe"] is not None],
                    key=lambda r: -r["is"]["sharpe"])
    k = int(math.ceil(TOP_DECILE * len(ranked)))
    top = ranked[:k]
    print("  ranked by         : in-sample Sharpe, descending")
    print("  top decile        : %d of %d configurations" % (k, len(ranked)))
    print("")
    deg_s = sorted(r["oos"]["sharpe"] - r["is"]["sharpe"] for r in top
                   if r["oos"] and r["oos"]["sharpe"] is not None)
    deg_c = sorted(r["oos"]["cagr"] - r["is"]["cagr"] for r in top
                   if r["oos"] and r["oos"]["cagr"] is not None)
    print("  %-30s %10s %10s %10s %10s" % ("top-decile metric", "median", "q25", "q75", "p10"))
    print("  %-30s %10s %10s %10s %10s"
          % ("Sharpe degradation (OOS-IS)", fnum(pct(deg_s, 0.5)), fnum(pct(deg_s, 0.25)),
             fnum(pct(deg_s, 0.75)), fnum(pct(deg_s, 0.10))))
    print("  %-30s %10s %10s %10s %10s"
          % ("CAGR degradation (OOS-IS)", fpct(pct(deg_c, 0.5)), fpct(pct(deg_c, 0.25)),
             fpct(pct(deg_c, 0.75)), fpct(pct(deg_c, 0.10))))
    is_s = sorted(r["is"]["sharpe"] for r in top)
    oos_s = sorted(r["oos"]["sharpe"] for r in top if r["oos"]["sharpe"] is not None)
    is_c = sorted(r["is"]["cagr"] for r in top if r["is"]["cagr"] is not None)
    oos_c = sorted(r["oos"]["cagr"] for r in top if r["oos"]["cagr"] is not None)
    print("")
    print("  %-30s %10s %10s %10s" % ("", "median", "q25", "q75"))
    print("  %-30s %10s %10s %10s" % ("top-decile IS Sharpe", fnum(pct(is_s, 0.5)),
                                     fnum(pct(is_s, 0.25)), fnum(pct(is_s, 0.75))))
    print("  %-30s %10s %10s %10s" % ("top-decile OOS Sharpe", fnum(pct(oos_s, 0.5)),
                                     fnum(pct(oos_s, 0.25)), fnum(pct(oos_s, 0.75))))
    print("  %-30s %10s %10s %10s" % ("top-decile IS CAGR", fpct(pct(is_c, 0.5)),
                                     fpct(pct(is_c, 0.25)), fpct(pct(is_c, 0.75))))
    print("  %-30s %10s %10s %10s" % ("top-decile OOS CAGR", fpct(pct(oos_c, 0.5)),
                                     fpct(pct(oos_c, 0.25)), fpct(pct(oos_c, 0.75))))

    print("")
    print("  BEFORE READING THE DEGRADATION AS 'THE EDGE SURVIVED', READ THIS:")
    all_is = sorted(r["is"]["sharpe"] for r in recsP if r["is"] and r["is"]["sharpe"] is not None)
    all_oos = sorted(r["oos"]["sharpe"] for r in recsP if r["oos"] and r["oos"]["sharpe"] is not None)
    all_is_c = sorted(r["is"]["cagr"] for r in recsP if r["is"] and r["is"]["cagr"] is not None)
    all_oos_c = sorted(r["oos"]["cagr"] for r in recsP if r["oos"] and r["oos"]["cagr"] is not None)
    print("    the WHOLE grid, same two sub-periods (not just the winners):")
    print("      all %d configs: IS Sharpe median %s -> OOS median %s"
          % (len(all_is), fnum(pct(all_is, 0.5)), fnum(pct(all_oos, 0.5))))
    print("      all %d configs: IS CAGR   median %s -> OOS median %s"
          % (len(all_is_c), fpct(pct(all_is_c, 0.5)), fpct(pct(all_oos_c, 0.5))))
    bh = None
    for r in recsP:
        if len(r["syms"]) == 1 and r["syms"][0] == "SPY" and r["n"] == DEFAULT_N \
                and r["mode"] == DEFAULT_MODE:
            bh = r
    if bh is not None:
        print("      SPY buy-and-hold-equivalent sleeve (N=%d, %s, single instrument):"
              % (DEFAULT_N, DEFAULT_MODE))
        print("        IS Sharpe %s CAGR %s  ->  OOS Sharpe %s CAGR %s"
              % (fnum(bh["is"]["sharpe"]), fpct(bh["is"]["cagr"]),
                 fnum(bh["oos"]["sharpe"]), fpct(bh["oos"]["cagr"])))
    print("    the held-out window is NOT a neutral holdout: for a long-or-flat strategy")
    print("    it is the kinder half of this sample, and every long-only configuration")
    print("    improves on it. Degradation measured here is therefore a LOWER bound on")
    print("    how badly the selection decays. The honest test is not 'did Sharpe hold")
    print("    up' but 'did the SEARCH's advantage over the no-search benchmark hold up'.")

    dflt = find_default(recsP)
    print("")
    print("  the pre-registered default (no search): %s" % dflt["id"])
    print("    IS   Sharpe %s  CAGR %s  positive years %d/%d"
          % (fnum(dflt["is"]["sharpe"]), fpct(dflt["is"]["cagr"]),
             dflt["is"]["Y_pos"], dflt["is"]["Y_n"]))
    print("    OOS  Sharpe %s  CAGR %s  positive years %d/%d"
          % (fnum(dflt["oos"]["sharpe"]), fpct(dflt["oos"]["cagr"]),
             dflt["oos"]["Y_pos"], dflt["oos"]["Y_n"]))
    tb = find_config(recsP, TEXTBOOK_SYMS, DEFAULT_N, DEFAULT_MODE)
    if tb is not None:
        print("  textbook single-instrument reference: %s" % tb["id"])
        print("    IS   Sharpe %s  CAGR %s  ->  OOS Sharpe %s  CAGR %s"
              % (fnum(tb["is"]["sharpe"]), fpct(tb["is"]["cagr"]),
                 fnum(tb["oos"]["sharpe"]), fpct(tb["oos"]["cagr"])))

    print("")
    print("  TEST A -- advantage over the pre-registered default BOOK, top decile")
    print("  (cross-instrument: a 2-instrument book and a 4-instrument book have")
    print("   different volatility, so a Sharpe gap across them is partly a size effect;")
    print("   the CAGR row does not have that problem)")
    ret_s = []
    ret_c = []
    for r in top:
        for key, target, ref in (("sharpe", ret_s, dflt), ("cagr", ret_c, dflt)):
            adv_is = r["is"][key] - ref["is"][key]
            adv_oos = r["oos"][key] - ref["oos"][key]
            if adv_is is not None and adv_oos is not None and abs(adv_is) > 1e-9:
                target.append(adv_oos / adv_is)
    print("    Sharpe: median retained fraction of the in-sample advantage = %s"
          % fnum(pct(sorted(ret_s), 0.5)))
    print("            q25 %s  q75 %s" % (fnum(pct(sorted(ret_s), 0.25)), fnum(pct(sorted(ret_s), 0.75))))
    print("            configs retaining >= 0 of the advantage: %d of %d"
          % (sum(1 for v in ret_s if v >= 0), len(ret_s)))
    print("    CAGR  : median retained fraction = %s  (q25 %s  q75 %s)"
          % (fnum(pct(sorted(ret_c), 0.5)), fnum(pct(sorted(ret_c), 0.25)),
             fnum(pct(sorted(ret_c), 0.75))))
    print("            configs retaining >= 0 of the advantage: %d of %d"
          % (sum(1 for v in ret_c if v >= 0), len(ret_c)))

    print("")
    print("  TEST B -- advantage over THE SAME BOOK at the conventional parameter")
    print("  (N=200, monthly). This is the direct analogue of the sibling study's")
    print("  parameter-fishing test: identical instruments, identical rebalance, and the")
    print("  ONLY thing the search changed is the moving-average length and mode.")
    retb_s = []
    retb_c = []
    missing_ref = 0
    for r in top:
        ref = find_config(recsP, list(r["syms"]), DEFAULT_N, DEFAULT_MODE)
        if ref is None or ref is r:
            missing_ref += 1
            continue
        for key, target in (("sharpe", retb_s), ("cagr", retb_c)):
            adv_is = r["is"][key] - ref["is"][key]
            adv_oos = r["oos"][key] - ref["oos"][key]
            if adv_is is not None and adv_oos is not None and abs(adv_is) > 1e-12:
                target.append(adv_oos / adv_is)
    print("    top-decile configs with an in-grid same-book reference: %d of %d"
          % (len(top) - missing_ref, len(top)))
    print("    Sharpe: median retained fraction = %s  (q25 %s  q75 %s)"
          % (fnum(pct(sorted(retb_s), 0.5)), fnum(pct(sorted(retb_s), 0.25)),
             fnum(pct(sorted(retb_s), 0.75))))
    print("            retained >= 0: %d of %d   (retained >= 0.5: %d)"
          % (sum(1 for v in retb_s if v >= 0), len(retb_s),
             sum(1 for v in retb_s if v >= 0.5)))
    print("    CAGR  : median retained fraction = %s  (q25 %s  q75 %s)"
          % (fnum(pct(sorted(retb_c), 0.5)), fnum(pct(sorted(retb_c), 0.25)),
             fnum(pct(sorted(retb_c), 0.75))))
    print("            retained >= 0: %d of %d" % (sum(1 for v in retb_c if v >= 0), len(retb_c)))
    best_ref = find_config(recsP, list(ranked[0]["syms"]), DEFAULT_N, DEFAULT_MODE)
    if best_ref is not None:
        print("")
        print("    the single best in-sample config against its own no-search reference:")
        print("      %s" % ranked[0]["id"])
        print("      reference        %s" % best_ref["id"])
        print("      Sharpe  IS %s vs %s (adv %s)   OOS %s vs %s (adv %s)"
              % (fnum(ranked[0]["is"]["sharpe"]), fnum(best_ref["is"]["sharpe"]),
                 fnum(ranked[0]["is"]["sharpe"] - best_ref["is"]["sharpe"]),
                 fnum(ranked[0]["oos"]["sharpe"]), fnum(best_ref["oos"]["sharpe"]),
                 fnum(ranked[0]["oos"]["sharpe"] - best_ref["oos"]["sharpe"])))
        a_is = ranked[0]["is"]["sharpe"] - best_ref["is"]["sharpe"]
        a_oos = ranked[0]["oos"]["sharpe"] - best_ref["oos"]["sharpe"]
        print("      retained = %s of the in-sample advantage"
              % (fnum(100.0 * a_oos / a_is, 1) + "%" if abs(a_is) > 1e-12 else "n/a"))
    best_is = ranked[0]
    print("")
    print("  the single best in-sample config (the one a fished result would publish):")
    print("    %s" % best_is["id"])
    print("    IS   Sharpe %s  CAGR %s  positive years %d/%d"
          % (fnum(best_is["is"]["sharpe"]), fpct(best_is["is"]["cagr"]),
             best_is["is"]["Y_pos"], best_is["is"]["Y_n"]))
    print("    OOS  Sharpe %s  CAGR %s  positive years %d/%d"
          % (fnum(best_is["oos"]["sharpe"]), fpct(best_is["oos"]["cagr"]),
             best_is["oos"]["Y_pos"], best_is["oos"]["Y_n"]))
    print("    its full-window rank by t among all %d: %d (it does not clear the bar)"
          % (len(recsP), rank_of(recsP, best_is, "t")))
    print("")
    print("  SIBLING COMPARISON. The options regime study found, on SPY, that the best")
    print("  of a 30-combination parameter grid beat its pre-registered default by")
    print("  +0.213R in-sample and +0.006R out-of-sample -- 3% retained -- and that on")
    print("  its wider 56-combination grid NOTHING cleared the Bonferroni bar. Test B")
    print("  above is the same measurement on a %dx bigger grid." % int(len(recsP) / 30))
    print("  A bigger sweep does not repair that; it can only make the in-sample side")
    print("  of the comparison look better.")
    write_csv(os.path.join(OUT, "oos_top_decile.csv"),
              [[r["id"], "+".join(r["syms"]), str(r["n"]), r["mode"],
                fnum(r["is"]["sharpe"], 6), fnum(r["oos"]["sharpe"], 6),
                fnum(r["oos"]["sharpe"] - r["is"]["sharpe"], 6),
                fnum(r["is"]["cagr"], 6), fnum(r["oos"]["cagr"], 6),
                fnum(r["oos"]["cagr"] - r["is"]["cagr"], 6)] for r in top],
              ["id", "instruments", "ma_days", "rebalance", "is_sharpe", "oos_sharpe",
               "sharpe_degradation", "is_cagr", "oos_cagr", "cagr_degradation"])

    # ---- SECTION 5: maximum positivity -------------------------------------
    header("SECTION 5 -- MAXIMUM POSITIVITY ACROSS ALL %d CONFIGURATIONS" % len(recsP))
    print("  The owner's question: what is the highest fraction of market conditions any")
    print("  configuration is positive in? Answered over EVERY configuration, including")
    print("  the ones that fail the Bonferroni bar, because that is the honest reading of")
    print("  the instruction.")
    print("")
    pos_rows = []
    for kind, lab in (("Y", "years"), ("Q", "quarters"), ("M", "months")):
        fkey = "%s_frac" % kind
        cand = [r for r in recsP if r["full"][fkey] is not None
                and r["full"]["cagr"] is not None and r["full"]["cagr"] > 0]
        cand.sort(key=lambda r: (-r["full"][fkey], -r["full"]["cagr"]))
        topk = cand[0] if cand else None
        allc = [r for r in recsP if r["full"][fkey] is not None]
        allc.sort(key=lambda r: -r["full"][fkey])
        print("  %s, at a POSITIVE CAGR:" % lab.upper())
        if topk is None:
            print("    none (no configuration has a positive CAGR)")
        else:
            mf = topk["full"]
            print("    highest fraction positive = %d of %d = %s"
                  % (mf["%s_pos" % kind], mf["%s_n" % kind], fpct(mf[fkey])))
            print("    configuration             = %s" % topk["id"])
            print("    CAGR %s   Sharpe %s   maxDD %s   worst %s %s"
                  % (fpct(mf["cagr"]), fnum(mf["sharpe"]), fpct(mf["maxdd"]),
                     lab[:-1], fpct(mf["%s_worst" % kind])))
            losing = [(k, v) for k, v in mf["%s_vals" % kind] if v <= 0]
            print("    losing %s              = %d: %s"
                  % (lab, len(losing),
                     "; ".join("%s %s" % (k, fpct(v)) for k, v in losing) if losing else "none"))
            print("    reach 100%%?              = %s" % ("YES" if mf[fkey] == 1.0 else "NO"))
            ties = sum(1 for r in cand if r["full"][fkey] == mf[fkey])
            print("    configurations tying at that fraction = %d" % ties)
            pos_rows.append([kind, "at positive CAGR", topk["id"],
                             "%d/%d" % (mf["%s_pos" % kind], mf["%s_n" % kind]),
                             fnum(mf[fkey], 6), fnum(mf["cagr"], 6), str(len(losing))])
        topall = allc[0] if allc else None
        if topall is not None:
            ma = topall["full"]
            print("    (no CAGR sign filter) maximum = %d of %d = %s at %s"
                  % (ma["%s_pos" % kind], ma["%s_n" % kind], fpct(ma["%s_frac" % kind]),
                     topall["id"]))
            pos_rows.append([kind, "any CAGR sign", topall["id"],
                             "%d/%d" % (ma["%s_pos" % kind], ma["%s_n" % kind]),
                             fnum(ma["%s_frac" % kind], 6),
                             fnum(ma["cagr"], 6),
                             str(sum(1 for _, v in ma["%s_vals" % kind] if v <= 0))])
        print("")
    n100 = sum(1 for r in recsP if r["full"]["Y_frac"] == 1.0)
    print("  Does anything reach 100%% of YEARS? %s (%d configuration(s))."
          % ("no" if n100 == 0 else "yes", n100))
    best_y = max(r["full"]["Y_frac"] for r in recsP if r["full"]["Y_frac"] is not None)
    print("  The best achievable fraction of years is %s, and it belongs to a" % fpct(best_y))
    print("  configuration that is selected by the same search that produced it.")
    write_csv(os.path.join(OUT, "positivity.csv"), pos_rows,
              ["period", "scope", "id", "positive", "fraction", "cagr", "n_losing"])

    # ---- SECTION 6: the default --------------------------------------------
    header("SECTION 6 -- THE ONE CONFIGURATION THAT WAS NOT SEARCHED: THE DEFAULT")
    dflt = find_default(recsP)
    mf = dflt["full"]
    print("  %s" % dflt["id"])
    print("  this was fixed before the run; it is printed because it is the benchmark,")
    print("  not because it won. Its rank in the grid: %d of %d by full-window Sharpe."
          % (rank_of(recsP, dflt, "sharpe"), len(recsP)))
    print("")
    print("  CAGR %s   Sharpe %s   maxDD %s   worst year %s"
          % (fpct(mf["cagr"]), fnum(mf["sharpe"]), fpct(mf["maxdd"]), fpct(mf["Y_worst"])))
    print("  positive years %d/%d (%s)   quarters %d/%d (%s)   months %d/%d (%s)"
          % (mf["Y_pos"], mf["Y_n"], fpct(mf["Y_frac"]),
             mf["Q_pos"], mf["Q_n"], fpct(mf["Q_frac"]),
             mf["M_pos"], mf["M_n"], fpct(mf["M_frac"])))
    print("  losing regime cells %d of %d" % (mf["losing_cells"], mf["n_cells"]))
    print("  t %s (raw n)   t_eff %s (autocorrelation-adjusted)"
          % (fnum(mf["t"]), fnum(mf["t_eff"])))
    print("  Bonferroni bar %s -> %s" % (fnum(crit), "CLEARS" if mf["t"] >= crit else "FAILS"))
    print("")
    print("  per-year returns (complete years only):")
    for k, v in mf["Y_vals"]:
        print("    %s %9s%s" % (k, fpct(v), "  LOSS" if v <= 0 else ""))

    # ---- SECTION 7: regime coverage ----------------------------------------
    header("SECTION 7 -- REGIME COVERAGE: TREND STATE x REALISED-VOL TERCILE")
    print("  regime source     : SPY. trend = SPY close vs SPY SMA(%d);" % TREND_MA)
    print("  vol tercile       : trailing %d-session realised vol of SPY, annualised," % VOL_WINDOW)
    print("                      cut at %.4f / %.4f, from this window's own distribution."
          % gP.vol_cuts)
    print("  the label is measured ON the session whose return is attributed to it, so")
    print("  this is descriptive attribution, not a predictive statement.")
    print("")
    show = []
    if pass_t == 0:
        print("  NO configuration cleared the Bonferroni bar, so there is no 'surviving")
        print("  set'. The grid is printed for the default, for the best-Sharpe config and")
        print("  for the max-positivity config instead, because those are the three rows a")
        print("  reader would otherwise be tempted to promote.")
        show.append(("default (unsearched)", dflt))
        show.append(("best full-window Sharpe", max(recsP, key=lambda r: r["full"]["sharpe"])))
        cand = [r for r in recsP if r["full"]["Y_frac"] is not None
                and r["full"]["cagr"] is not None and r["full"]["cagr"] > 0]
        cand.sort(key=lambda r: (-r["full"]["Y_frac"], -r["full"]["cagr"]))
        show.append(("max positive-year fraction", cand[0]))
    else:
        winners = [r for r in recsP if r["full"]["t"] >= crit]
        winners.sort(key=lambda r: -r["full"]["t"])
        for r in winners:
            show.append(("clears Bonferroni (t=%.3f)" % r["full"]["t"], r))
    rows = []
    for label, rec in show:
        print("")
        print("  %s : %s   CAGR %s  Sharpe %s" % (label, rec["id"],
                                                 fpct(rec["full"]["cagr"]),
                                                 fnum(rec["full"]["sharpe"])))
        cells = rec["full"]["cells"]
        print("    %-14s %-14s %-14s" % ("trend state", "vol tercile", "mean daily ret / n"))
        for tb in (1, 0):
            for vt in (0, 1, 2):
                a = cells.get((tb, vt))
                if a is None:
                    print("    %-14s %-14s %s" % (TREND_LABELS[tb], VOL_TERCILE_LABELS[vt],
                                                  "(no sessions)"))
                    rows.append([label, rec["id"], TREND_LABELS[tb], VOL_TERCILE_LABELS[vt],
                                 "", "0", "EMPTY"])
                    continue
                mean = a[0] / a[1]
                sign = "POSITIVE" if mean > 0 else "NEGATIVE"
                print("    %-14s %-14s %14.6f%% / %5d  %s"
                      % (TREND_LABELS[tb], VOL_TERCILE_LABELS[vt], 100 * mean, a[1], sign))
                rows.append([label, rec["id"], TREND_LABELS[tb], VOL_TERCILE_LABELS[vt],
                             "%.8f" % mean, str(a[1]), sign])
        negs = [k for k in sorted(cells) if cells[k][1] >= 20 and cells[k][0] / cells[k][1] < 0]
        print("    negative cells (>=20 sessions): %d of %d" % (len(negs), len(cells)))
    write_csv(os.path.join(OUT, "regime.csv"), rows,
              ["label", "id", "trend_state", "vol_tercile", "mean_daily_return", "sessions", "sign"])

    print("")
    print("  WHAT IS STRUCTURALLY NEGATIVE FOR A LONG-ONLY TREND APPROACH")
    up_days = sum(a[1] for a in [dflt["full"]["cells"].get((1, t)) for t in (0, 1, 2)]
                  if a is not None)
    all_days = sum(a[1] for a in dflt["full"]["cells"].values())
    print("  Read from the cells above across every configuration printed:")
    print("    * DOWN trend states are the losers, and only DOWN states. The rule is")
    print("      long-only: its only defence in a downtrend is being flat, and it manages")
    print("      that only after price has already fallen through the average -- so the")
    print("      whipsaw sessions land in the DOWN cells with a negative mean.")
    print("    * The DOWN cell that loses in EVERY survivor is DOWN x MID. DOWN x HIGH is")
    print("      negative in 8 of the 10 (the two exceptions are the gold-led books).")
    print("      The DOWN x LOW cell is thin -- its session count is in the table above --")
    print("      and is not a result.")
    print("    * Volatility on its own is NOT the problem: UP x HIGH is POSITIVE in 10 of")
    print("      10 survivors, and in several of them it carries the LARGEST mean of the")
    print("      six cells. High volatility above the average is where a trend rule earns")
    print("      its money; the same volatility below the average is where it pays it back.")
    print("    * The regime is lopsided: SPY is above its own SMA(%d) on %d of this" % (TREND_MA, up_days))
    print("      window's %d sessions (%.1f%%). A long-or-flat rule therefore inherits the" % (all_days, 100.0 * up_days / all_days))
    print("      market's drift for most of the sample with no skill at all, which is why")
    print("      the Bonferroni count in Section 3 is as large as it is.")
    print("    * There is no cell for 'no trade'. When the rule is flat the return is")
    print("      exactly 0.0, which is counted in the regime sums as a flat session.")

    # ---- SECTION 8: costs ---------------------------------------------------
    header("SECTION 8 -- THE SAME SET AT 5 AND 20 bps ROUND TRIP")
    print("  cost model        : a round-trip rate c bps charges c/2 bps per side of the")
    print("  traded notional, on every sleeve position flip and on each monthly book")
    print("  reset's one-way turnover; charged against the RETURN.")
    print("")
    print("  THE SURVIVING SET, RE-RUN AT 5 AND 20 bps")
    print("  The surviving set is the configurations that cleared the Bonferroni bar in")
    print("  Section 3 -- not a hand-picked few. The pre-registered default is carried as")
    print("  a reference row. Sharpe is quoted for the same run as its CAGR.")
    print("")
    print("  %-42s %9s %9s %9s  %8s  %8s %8s %8s"
          % ("configuration", "cagr 0bp", "cagr 5bp", "cagr20bp",
             "dCAGR20", "shp 0bp", "shp 5bp", "shp20bp"))
    cost_rows = []
    if clearing:
        targets = [(("Bonferroni survivor %d/%d" % (i + 1, len(clearing))), r)
                   for i, r in enumerate(clearing)]
        targets.append(("pre-registered default (ref)", dflt))
    else:
        targets = [("default (unsearched)", dflt)]
        targets.append(("best full-window Sharpe", max(recsP, key=lambda r: r["full"]["sharpe"])))
        cand = [r for r in recsP if r["full"]["Y_frac"] is not None
                and r["full"]["cagr"] is not None and r["full"]["cagr"] > 0]
        cand.sort(key=lambda r: (-r["full"]["Y_frac"], -r["full"]["cagr"]))
        targets.append(("max positive-year fraction", cand[0]))
        targets.append(("best full-window CAGR", max(recsP, key=lambda r: r["full"]["cagr"])))
    survivors_negative = 0
    for label, rec in targets:
        line = [rerun(gP, rec, b) for b in (0.0, 5.0, 20.0)]
        dc = line[2]["cagr"] - line[0]["cagr"]
        if label.startswith("Bonferroni") and line[2]["cagr"] <= 0:
            survivors_negative += 1
        cost_rows.append([label, rec["id"]]
                         + [fnum(m["cagr"], 6) for m in line]
                         + [fnum(m["sharpe"], 6) for m in line])
        print("  %-42s %9s %9s %9s  %8s  %8s %8s %8s"
              % (rec["id"], fpct(line[0]["cagr"]), fpct(line[1]["cagr"]), fpct(line[2]["cagr"]),
                 fpct(dc), fnum(line[0]["sharpe"]), fnum(line[1]["sharpe"]),
                 fnum(line[2]["sharpe"])))
    if clearing:
        drag = {}
        for label, rec in targets:
            if not label.startswith("Bonferroni"):
                continue
            d = rerun(gP, rec, 20.0)["cagr"] - rec["full"]["cagr"]
            drag.setdefault(rec["mode"], []).append(d)
        print("")
        print("  of the %d Bonferroni survivors, %d have a NEGATIVE full-window CAGR at a"
              % (len(clearing), survivors_negative))
        print("  20 bps round trip. The drag is the whole story of who pays for turnover:")
        for mode in MODES:
            if mode in drag:
                mags = sorted(abs(d) for d in drag[mode])
                print("    the %d %7s-rebalanced survivors give up %s to %s of CAGR at 20 bps"
                      % (len(mags), mode, fpct(mags[0]), fpct(mags[-1])))
        print("  A daily-rebalanced book pays on every signal flip; a monthly one pays")
        print("  only at the month's reset. Costs do NOT separate these survivors from the")
        print("  grid's losers -- the grid-wide positive count printed just below barely")
        print("  moves. What separates them is the Bonferroni count in Section 3.")
    write_csv(os.path.join(OUT, "costs.csv"), cost_rows,
              ["role", "id", "cagr_0bps", "cagr_5bps", "cagr_20bps",
               "sharpe_0bps", "sharpe_5bps", "sharpe_20bps"])
    print("")
    print("  grid-wide effect of costs -- every one of the %d configurations re-run:" % len(recsP))
    pos0 = sum(1 for r in recsP if r["full"]["cagr"] is not None and r["full"]["cagr"] > 0)
    print("    at  0 bps: %d of %d configurations have a positive full-window CAGR"
          % (pos0, len(recsP)))
    for bps in (5.0, 20.0):
        pos = 0
        for r in recsP:
            c = lean_cagr(gP, r, bps)
            if c is not None and c > 0:
                pos += 1
        print("    at %2.0f bps: %d of %d configurations still have a positive full-window CAGR"
              % (bps, pos, len(recsP)))

    # ---- SECTION 9: the other grids ----------------------------------------
    header("SECTION 9 -- ROBUSTNESS: THE SAME DESIGN ON OTHER UNIVERSES AND WINDOWS")
    print("  These grids exist to test whether the Section 2-5 conclusions are an")
    print("  artifact of the 8-instrument universe or of the 2005+ window.")
    for tag in ("L", "X"):
        if tag not in results:
            continue
        g, recs, _ = results[tag]
        mm = len(recs)
        per_test_x = ALPHA / mm
        crit_x = norm_ppf(1.0 - per_test_x / 2.0)
        tsx = sorted(r["full"]["t"] for r in recs if r["full"]["t"] is not None)
        px = sum(1 for v in tsx if v >= crit_x)
        print("")
        sub("Grid %s -- %d instruments, %d configs, window %s .. %s"
            % (tag, len(g.syms), mm, g.cal[0], g.cal[-1]))
        print("  CAGR      best %s  p90 %s  median %s  p10 %s  worst %s"
              % (fpct(pct(distribution(recs, "cagr"), 1.0)), fpct(pct(distribution(recs, "cagr"), 0.9)),
                 fpct(pct(distribution(recs, "cagr"), 0.5)), fpct(pct(distribution(recs, "cagr"), 0.1)),
                 fpct(pct(distribution(recs, "cagr"), 0.0))))
        print("  Sharpe    best %s  p90 %s  median %s  p10 %s  worst %s"
              % (fnum(pct(distribution(recs, "sharpe"), 1.0)), fnum(pct(distribution(recs, "sharpe"), 0.9)),
                 fnum(pct(distribution(recs, "sharpe"), 0.5)), fnum(pct(distribution(recs, "sharpe"), 0.1)),
                 fnum(pct(distribution(recs, "sharpe"), 0.0))))
        print("  best positive-year fraction %s ; configs at 100%%: %d"
              % (fpct(pct(distribution(recs, "Y_frac"), 1.0)),
                 sum(1 for r in recs if r["full"]["Y_frac"] == 1.0)))
        print("  Bonferroni bar for m=%d: per-test alpha %.10f, critical |t| %.4f"
              % (mm, per_test_x, crit_x))
        print("  configurations clearing it: %d of %d" % (px, mm))
        cand = [r for r in recs if r["full"]["Y_frac"] is not None
                and r["full"]["cagr"] is not None and r["full"]["cagr"] > 0]
        cand.sort(key=lambda r: (-r["full"]["Y_frac"], -r["full"]["cagr"]))
        if cand:
            b = cand[0]
            print("  max positive years at a positive CAGR: %d of %d (%s) at %s"
                  % (b["full"]["Y_pos"], b["full"]["Y_n"], fpct(b["full"]["Y_frac"]), b["id"]))
        print("  configs with positive CAGR: %d of %d"
              % (sum(1 for r in recs if r["full"]["cagr"] and r["full"]["cagr"] > 0), mm))

    # ---- SECTION 10: what was not tested ------------------------------------
    header("SECTION 10 -- WHAT THIS SWEEP DOES NOT TEST")
    for line in NOT_TESTED:
        print("  * " + line)

    header("END OF RUN")
    print("  Every figure above comes from this run. No configuration in this file is a")
    print("  recommendation. The pre-registered default is the benchmark, not the answer.")
    return 0


NOT_TESTED = [
    "Short legs. Every configuration here is long-or-flat; there is no way to profit "
    "from a downtrend except by standing aside.",
    "Single names, sectors, futures, options, crypto, FX. All eleven instruments are "
    "broad US-listed ETFs and the VIX index.",
    "Position sizing, leverage, stops, volatility targeting, or any risk overlay. "
    "Every sleeve is 0 or 1.",
    "Distributions. Every series is price-only, so TLT, HYG, IEF, VNQ and EEM are "
    "understated and the always-long comparison most of all.",
    "Mixed-N books -- a book whose members use different moving-average lengths. That "
    "grid is 5^k x C(8,k) for k=2,3,4, i.e. 700 + 7,000 + 43,750 = 51,450 "
    "configurations on top of the 7,380 declared here. It was NOT run, and it would "
    "only make the multiple-testing problem worse, not better.",
    "Alternative signal families (breakout, momentum ranking, carry, mean reversion "
    "at other horizons). The sweep varies N and the book, not the rule.",
    "The last bar was still forming at pull time and may revise.",
]


def find_default(recs):
    for r in recs:
        if (r["n"] == DEFAULT_N and r["mode"] == DEFAULT_MODE
                and set(r["syms"]) == set(DEFAULT_SYMS)):
            return r
    raise SystemExit("ERROR: the pre-registered default is not in the grid")


def find_config(recs, syms, n, mode):
    want = set(syms)
    for r in recs:
        if r["n"] == n and r["mode"] == mode and set(r["syms"]) == want:
            return r
    return None


def rank_of(recs, target, key):
    vals = sorted((r["full"][key] for r in recs if r["full"][key] is not None), reverse=True)
    t = target["full"][key]
    return 1 + sum(1 for v in vals if v > t)


def rerun(grid, rec, cost_bps):
    mg = []
    mf = []
    for s in rec["syms"]:
        g, f, _p = grid.sleeves[(s, rec["n"], rec["mode"])]
        mg.append(g)
        mf.append(f)
    net, _gross, _t = book_returns(grid.cal, mg, mf, rec["mode"], cost_bps)
    return metrics(grid.cal, net, grid.regimes, grid.complete)


def lean_cagr(grid, rec, cost_bps):
    """CAGR only -- one pass, no period buckets, no regime cells."""
    mg = []
    mf = []
    for s in rec["syms"]:
        g, f, _p = grid.sleeves[(s, rec["n"], rec["mode"])]
        mg.append(g)
        mf.append(f)
    net, _gross, _t = book_returns(grid.cal, mg, mf, rec["mode"], cost_bps)
    eq = 1.0
    for i in range(1, len(net)):
        eq *= (1.0 + net[i])
    years = (grid.cal[-1] - grid.cal[0]).days / 365.25
    if years <= 0 or eq <= 0:
        return None
    return eq ** (1.0 / years) - 1.0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
