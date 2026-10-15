#!/usr/bin/env python3
"""
study.py -- THE POSITIVITY FRONTIER.

THE QUESTION THIS ANSWERS.  "Be profitable every time -- in every market
condition, at daily/weekly/biweekly/monthly/quarterly/half-yearly/yearly."

THE ANSWER, MEASURED.  Positivity is bought with return, and the exchange rate
is observable.  Take a book of risky sleeves, mix it with cash at exposure
lambda:

        r(lambda)[j] = lambda * r_risky[j] + (1 - lambda) * r_cash[j]

At lambda = 1 the return is whatever the book earns and the positivity is
whatever the book has.  At lambda = 0 the return IS the cash rate.  In between,
the fraction of positive periods rises as the return falls.  This study MEASURES
that curve on real data at all seven bucket widths and reports where it ends:
the largest lambda at which 100% of periods are still positive, and what return
that lambda actually earns.

Nothing here is searched for a green number.  The books, the sleeve rule, the
weights, the lambda grid and the bucket set are fixed BEFORE the run and are
printed with the results.  Every losing period is reported, not summarised away.

STRICT vs LOOSE "PROFITABLE".  Two readings are reported side by side:
    frac_gt0  -- a period counts only if its return is strictly > 0
    frac_ge0  -- a period counts unless its return is strictly < 0
The gap between them is the "flat period" effect, and it is large here: a trend
book that is out of the market returns EXACTLY zero, and a zero-return month is
not a profitable month under the strict reading.  Reporting only one of the two
would be choosing the answer.

WHAT IS REUSED RATHER THAN RE-DERIVED
  * the sleeve construction and the book simulator are the weather-test's
    (../weather-test/study.py), reproduced with its conventions intact --
    including the one that matters: a position may only change on a BOOK date,
    and cost is charged against the RETURN, not against a sleeve's dollar value;
  * bucket_key / aggregate_bucket / sample_sd / max_drawdown / lag1_autocorr /
    n_effective come from the sibling engine
    (../../timeframe-performance-statistics/scripts/timeframe_stats.py), imported,
    never re-implemented here;
  * a REPRODUCTION CHECK re-runs the weather-test's own published four-sleeve
    book and compares this study's numbers against its published ones.

WHAT IS NEW
  * the cash series (a 3-month T-bill YIELD INDEX, the only long-history cash
    series the data source exposes -- limitation list in README.md);
  * the lambda grid and the frontier, at all seven buckets;
  * the strict/loose pair, the cash-proxy diagnostics, the flat-day count and the
    "first 5% of risk is the expensive part" diagnostic;
  * cost re-runs at 5 and 20 bps round trip;
  * a second, longer-window book that INCLUDES the 2000-2002 dot-com bear.

USAGE
    py -3 study.py            # writes out/*.csv and prints summaries to stdout
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

# --- THE GRID. Fixed before the run. Not searched. -------------------------
LAMBDA_STEPS = 20                      # lambda = i / 20 for i in 0..20
ROUND_TRIPS_BPS = [0.0, 5.0, 20.0]     # cost re-runs
BUCKETS = ["D", "W", "2W", "M", "Q", "H", "Y"]

# --- "MEANINGFUL RETURN" THRESHOLDS. Fixed before the run. -----------------
# The owner asked for a return AND for every-period positivity.  "Meaningful" is
# not defined by the data, so it is defined here, before the run, as an annual
# excess over cash, and three thresholds are reported rather than one.
MEANINGFUL_EXCESS = [0.00, 0.01, 0.02, 0.03]   # 0%, 1%, 2%, 3% per year over cash
FINE_STEP = 0.001                              # lambda resolution for the scan

# --- THE BOOKS. Fixed before the run. -------------------------------------
# name -> (sleeve weights, symbols entering the calendar intersection)
# The weight set is what the book HOLDS; the window set is what the book's
# CALENDAR is.  They are separated only so the weather-test's own published book
# can be reproduced exactly, since that study built its calendar from all five of
# its instruments including the one it later dropped from the weights.
BOOKS = [
    ("R4", {"SPY": 0.25, "TLT": 0.25, "GLD": 0.25, "EEM": 0.25},
     ["SPY", "TLT", "GLD", "EEM"],
     "PRIMARY: the weather-test's four-sleeve book (its F) -- equity, bond, gold "
     "and ex-US-equity trend at 25% each"),
    ("R9", {"SPY": 1 / 9.0, "TLT": 1 / 9.0, "GLD": 1 / 9.0, "EEM": 1 / 9.0,
            "IWM": 1 / 9.0, "DBC": 1 / 9.0, "VNQ": 1 / 9.0, "IEF": 1 / 9.0,
            "EFA": 1 / 9.0},
     ["SPY", "TLT", "GLD", "EEM", "IWM", "DBC", "VNQ", "IEF", "EFA"],
     "R4 plus small-cap, commodity, REIT, 7-10y Treasury and developed-ex-US "
     "trend at 1/9 each"),
    ("R10", {"SPY": 0.1, "TLT": 0.1, "GLD": 0.1, "EEM": 0.1, "IWM": 0.1,
             "DBC": 0.1, "VNQ": 0.1, "IEF": 0.1, "EFA": 0.1, "HYG": 0.1},
     ["SPY", "TLT", "GLD", "EEM", "IWM", "DBC", "VNQ", "IEF", "EFA", "HYG"],
     "R9 plus high-yield credit trend at 10% each -- shortest window, but it "
     "contains 2008"),
    ("R2L", {"SPY": 0.5, "QQQ": 0.5},
     ["SPY", "QQQ"],
     "LONG WINDOW, two sleeves: SPY + Nasdaq-100 trend. Reaches back far enough "
     "to contain the 2000-2002 dot-com bear"),
    ("R1L", {"SPY": 1.0}, ["SPY"],
     "LONGEST WINDOW, one sleeve: SPY trend only. No diversification at all; "
     "reported because it is the longest window the data allows"),
]
PRIMARY = "R4"

# The weather-test's published book, re-run here purely as a REPRODUCTION CHECK.
WEATHER_TEST_PUBLISHED = {
    "cagr": 0.046742, "max_dd": -0.148291, "sharpe_daily_ann": 0.603744,
    "window_first": "2005-09-02", "losing_years": 7, "n_days": 5311,
}
REPRO = ("WEATHER_F", {"SPY": 0.25, "TLT": 0.25, "GLD": 0.25, "EEM": 0.25},
         ["SPY", "TLT", "GLD", "EEM", "VIX"],
         "exact re-run of the weather-test's F, calendar from all five of its "
         "instruments, as that study defined it")

CASH_SYMBOL = "US03M"
CASH_PRICE_CROSSCHECK = "BIL"
ALL_SYMBOLS = sorted(set(
    [s for _, w, _, _ in BOOKS for s in w]
    + [s for _, _, sy, _ in BOOKS for s in sy]
    + [s for s in REPRO[2]]
    + [CASH_SYMBOL, CASH_PRICE_CROSSCHECK]
))

# The repo requires LF everywhere.  Redirected stdout on Windows would otherwise
# translate every newline to CRLF, which fails the file-format gate.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")


# ---------------------------------------------------------------------------
# The sibling engine, imported rather than re-implemented
# ---------------------------------------------------------------------------

def load_engine():
    path = os.path.join(ENGINE_DIR, "timeframe_stats.py")
    if not os.path.isfile(path):
        raise SystemExit(
            "ERROR: the sibling engine is missing.\n"
            "  expected: %s\n"
            "  This study imports its bucket_key / aggregate_bucket / sample_sd /\n"
            "  max_drawdown / lag1_autocorr / n_effective instead of\n"
            "  re-implementing them, and refuses to substitute its own formulae."
            % path)
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
    lines = []
    for p in provenance:
        lines.append("# PROVENANCE: %s" % p)
    lines.append(",".join(headers))
    for r in rows:
        lines.append(",".join("" if v is None else str(v) for v in r))
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
            if line.startswith("date,"):
                continue
            f = line.rstrip("\r\n").split(",")
            dates.append(datetime.date.fromisoformat(f[0]))
            o.append(float(f[1]))
            h.append(float(f[2]))
            l.append(float(f[3]))
            c.append(float(f[4]))
            v.append(float(f[5]) if f[5].strip() else 0.0)
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
# Sleeves -- the weather-test's rule, reproduced
# ---------------------------------------------------------------------------

class Sleeve(object):
    """One pre-registered rule, reduced to a daily return series.

    pos[i]  = 1 if the rule is long on the close of day i, else 0 (None during
              the moving-average warm-up, which behaves as flat).
    ret[i]  = the return earned on day i = pos[i-1] * (close[i]/close[i-1] - 1).
    flip[i] = the position held on day i differs from the one on day i-1, i.e. a
              state change was executed on the close of day i-1.
    """

    def __init__(self, code, bars, window):
        self.code = code
        self.symbol = bars.symbol
        self.dates = bars.dates
        self.index_of = bars.index_of
        self.c = bars.c
        self.provenance = bars.provenance
        avg = sma(bars.c, window)
        self.sma_window = window
        self.sma = avg
        self.pos = [NA] * len(bars.c)
        for i in range(len(bars.c)):
            if avg[i] is NA:
                self.pos[i] = NA
            else:
                self.pos[i] = 1 if bars.c[i] > avg[i] else 0
        self.ret = [0.0] * len(bars.c)
        for i in range(1, len(bars.c)):
            p = self.pos[i - 1]
            held = 0 if p is NA else p
            self.ret[i] = held * (bars.c[i] / bars.c[i - 1] - 1.0)
        self.hold = [0] * len(bars.c)
        for i in range(1, len(bars.c)):
            p = self.pos[i - 1]
            self.hold[i] = 0 if p is NA else p
        self.flip = [False] * len(bars.c)
        for i in range(2, len(bars.c)):
            self.flip[i] = self.hold[i] != self.hold[i - 1]
        self.first_live = None
        for i in range(len(bars.c)):
            if self.pos[i] is not NA:
                self.first_live = bars.dates[i]
                break

    def align(self, dates):
        """(ret, hold, flip) arrays aligned to `dates`, weather-test convention.

        A position may only change on a BOOK date.  The position held through
        book date j is the one the rule established at the close of the previous
        book date's bar.  A book date the instrument has no bar for contributes
        0.0 and carries the previous position; a bar of the instrument's own that
        falls between two book dates cannot change the position (the book could
        not have acted on it) but its price move is still fully counted, because
        the next book date measures the return from that bar's close.
        """
        n = len(dates)
        ret = [0.0] * n
        hold = [0] * n
        flip = [False] * n
        last_bar = None
        carried = 0
        for j, d in enumerate(dates):
            k = self.index_of.get(d)
            if k is None:
                carried += 1
                ret[j] = 0.0
                hold[j] = hold[j - 1] if j else 0
                flip[j] = False
                continue
            if last_bar is not None:
                p = self.pos[last_bar]
                hold[j] = 0 if p is NA else p
                ret[j] = hold[j] * (self.c[k] / self.c[last_bar] - 1.0)
            else:
                hold[j] = 0
            flip[j] = (j > 0 and hold[j] != hold[j - 1])
            last_bar = k
        self.aligned_carried = carried
        return ret, hold, flip


def book_window(universe, sleeve_symbols, window_symbols):
    """Book window = first date on which EVERY sleeve's rule is computable,
    restricted to dates present in every instrument of the calendar set."""
    sleeves = {}
    for sym in sleeve_symbols:
        sleeves[sym] = Sleeve(sym, universe[sym], SMA_TREND)
    start = max(sleeves[s].first_live for s in sleeve_symbols)
    sets = [set(universe[s].dates) for s in window_symbols]
    common = set.intersection(*sets)
    dates = sorted(d for d in common if d >= start)
    for d in dates:
        for sym in window_symbols:
            if d not in universe[sym].index_of:
                raise SystemExit("ERROR: %s missing from %s inside the window"
                                 % (d.isoformat(), sym))
    return dates, sleeves


# ---------------------------------------------------------------------------
# The book -- the weather-test's simulator, reproduced
# ---------------------------------------------------------------------------

class BookResult(object):
    def __init__(self):
        self.dates = []
        self.rets = []
        self.sleeve_rets = {}
        self.flips_total = 0
        self.turnover_total = 0.0
        self.cost_bps = 0.0


def simulate(dates, aligned, weights, cost_bps=0.0):
    """Fixed-weight, monthly-rebalanced book.

        cost_j   = (round_trip/2) * sum of weights that flipped on day j
                 + (round_trip/2) * one-way turnover on a rebalance day
        gross_j  = sum_s  w_s * r_s(j)
        R_j      = (1 + gross_j) * (1 - cost_j) - 1

    Charging the cost in the RETURN is what makes it bite; charging it by
    shrinking a sleeve's dollar value does not, because the weights are
    renormalised every day.
    """
    syms = sorted([s for s in weights if weights[s] > 0.0])
    tot = sum(weights[s] for s in syms)
    target = {s: weights[s] / tot for s in syms}
    half = (cost_bps / 2.0) / 10000.0

    res = BookResult()
    res.cost_bps = cost_bps
    res.dates = list(dates)
    if len(dates) < 2:
        raise SystemExit("ERROR: book window has fewer than 2 days")

    w = dict(target)
    month_prev = dates[0].month

    res.rets.append(0.0)
    for s in syms:
        res.sleeve_rets.setdefault(s, []).append(0.0)

    for j in range(1, len(dates)):
        d = dates[j]
        cost = 0.0
        for s in syms:
            if aligned[s][2][j]:
                cost += half * w[s]
                res.flips_total += 1
        rebalance = (d.month != month_prev)
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
        for s in syms:
            res.sleeve_rets.setdefault(s, []).append(aligned[s][0][j])

    for s in syms:
        res.sleeve_rets.setdefault(s, [0.0] * len(dates))
    return res


def build_book(universe, weights, window_symbols):
    """Return (dates, sleeves, aligned)."""
    sleeve_symbols = sorted([s for s in weights if weights[s] > 0.0])
    dates, sleeves = book_window(universe, sleeve_symbols, window_symbols)
    aligned = {s: sleeves[s].align(dates) for s in sleeve_symbols}
    return dates, sleeves, aligned


# ---------------------------------------------------------------------------
# CASH -- the only long-history cash series the source exposes
# ---------------------------------------------------------------------------

def cash_returns(dates, us03m, annual_fee_bps=0.0):
    """(r_cash, rate_used) from a 3-MONTH T-BILL YIELD INDEX.

    r_cash[j] = (yield at the close of book date j-1 / 100) / 252
                - annual_fee_bps/10000/252

    The rate is the one observed at the close of the PREVIOUS book date, the
    same no-lookahead convention the sleeves use for their position.  A missing
    observation carries the last known rate forward.

    *** THIS IS AN UPPER BOUND, NOT A TRADABLE RETURN. ***  A yield index is not
    a fund: it ignores management fees, the bid/offer and roll of an actual
    T-bill portfolio, and it credits the full quoted yield every business day.
    README.md carries the full limitation list; `annual_fee_bps` exists so the
    study can show the sensitivity to, say, a 15 bp expense ratio.
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
            out[j] = 0.0
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
    """(first calendar day, last calendar day) of the period containing d."""
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
        if d.month == 12:
            nxt = datetime.date(d.year + 1, 1, 1)
        else:
            nxt = datetime.date(d.year, d.month + 1, 1)
        return first, nxt - datetime.timedelta(days=1)
    if bucket == "Q":
        qm = 3 * ((d.month - 1) // 3) + 1
        first = datetime.date(d.year, qm, 1)
        end_m = qm + 2
        if end_m == 12:
            nxt = datetime.date(d.year + 1, 1, 1)
        else:
            nxt = datetime.date(d.year, end_m + 1, 1)
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

    Doing the bucketing once per (book, bucket) rather than once per (lambda,
    bucket) is what makes the 0.001-resolution scan affordable, and it removes
    any chance of two code paths disagreeing about which days form a period.

    A period is COMPLETE when its whole calendar span lies inside the window: the
    leading and trailing partial periods are dropped, so "fraction of positive
    years" is a statement about whole years.
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
    """[{key,label,first,last,n_days,ret}] -- `ret` is the COMPOUNDED return."""
    out = []
    for key, label, first, last, idx in groups:
        curve = 1.0
        for j in idx:
            curve *= (1.0 + rets[j])
        out.append({"key": key, "label": label, "first": first, "last": last,
                    "n_days": len(idx), "ret": curve - 1.0})
    return out


def period_stats(rets, groups):
    """(frac_gt0, frac_ge0, n_pos, n_zero, n_total, periods).

    frac_gt0 is the STRICT reading (a flat period is not profitable); frac_ge0 is
    the LOOSE one (only a loss counts against).  Both are returned so neither can
    be reported alone.
    """
    ps = period_returns(rets, groups)
    n = len(ps)
    if not n:
        return NA, NA, 0, 0, 0, ps
    npos = sum(1 for p in ps if p["ret"] > 0.0)
    nzero = sum(1 for p in ps if p["ret"] == 0.0)
    return npos / float(n), (npos + nzero) / float(n), npos, nzero, n, ps


def periods(dates, rets, bucket, complete_only=True):
    """Convenience wrapper: group_index + period_returns."""
    return period_returns(rets, group_index(dates, bucket, complete_only))


def level_stats(dates, rets):
    """CAGR / compounded max drawdown / daily Sharpe / additive max drawdown."""
    n = len(rets)
    curve = equity_curve(rets)
    yrs = years_between(dates[0], dates[-1])
    cagr = -1.0 if curve[-1] <= 0.0 else curve[-1] ** (1.0 / yrs) - 1.0
    m = sum(rets) / n if n else NA
    sd = TF.sample_sd(rets)
    sharpe = (m / sd * math.sqrt(TRADING_DAYS_PER_YEAR)) if (sd not in (NA, 0)) else NA
    return {"n_days": n, "years": yrs, "cagr": cagr,
            "max_dd": max_drawdown_pct(curve),
            "max_dd_additive": TF.max_drawdown(rets),
            "sharpe": sharpe, "mean_daily": m, "sd_daily": sd}


def bucket_engine_stats(rets, groups, bucket):
    """The engine's aggregate_bucket() over one synthetic trade per period.

    The synthetic trade carries the period's COMPOUNDED return on a $1 base, so
    `win_rate` is exactly the fraction of positive periods and `t_stat` is
    computed across period returns rather than across additive daily sums.  The
    trade's `close_date` is the period's FIRST session, chosen deliberately:
    aggregate_bucket re-derives the bucket key from that date, and the first
    session of a period always re-derives to the same key, so the engine's own
    bucketing cannot disagree with `groups`.
    """
    ps = period_returns(rets, groups)
    trades = [{"close_date": p["first"], "pnl": p["ret"]} for p in ps]
    return TF.aggregate_bucket(bucket, trades, 1.0)


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
        row[b + "_zero"] = nzero
    row.update(level_stats(dates, r))
    return row, r


def max_lambda_all_positive(dates, risky, cash, groups, bucket, ge0=False):
    """Largest lambda at which EVERY complete period of `bucket` is positive.

    A 0.05 grid scan first (which also records whether the positivity fraction is
    monotone non-increasing in lambda -- it need not be, and a non-monotone step
    is reported rather than assumed away), then a 0.001 bisection between the last
    passing grid point and the first failing one.

    Returns (lambda, cagr_at_lambda, n_periods, monotone_flag).
    """
    grid = lambda_grid()
    fracs = []
    for lam in grid:
        f1, f0, _, _, n, _ = period_stats(apply_lambda(risky, cash, lam), groups[bucket])
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
        if not n:
            return False
        return (f0 if ge0 else f1) >= 1.0 - 1e-12

    if hi is None:
        return round(lo, 3), level_stats(dates, apply_lambda(risky, cash, lo))["cagr"], \
            period_stats(apply_lambda(risky, cash, lo), groups[bucket])[4], monotone

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
    """The best positivity obtainable while still earning `min_excess` over cash.

    Returns {frac, lam_min, lam_max, cagr_min, cagr_max, n_ties} or None.

    The maximum positivity is typically attained on a PLATEAU of lambda -- once the
    cash sliver is large enough that a year's book loss can no longer swamp it, the
    count stops changing.  Both ends of that plateau are reported: the least risk
    that reaches the positivity (lam_min) and the most risk that still holds it
    (lam_max, which is also the higher return).  Reporting only one of the two would
    hide how flat the plateau is.
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
# One book, everything computed
# ---------------------------------------------------------------------------

def run_book(universe, name, weights, window_symbols, description, cost_bps,
             cash_fee_bps=0.0):
    dates, sleeves, aligned = build_book(universe, weights, window_symbols)
    book = simulate(dates, aligned, weights, cost_bps)
    cash, cash_used = cash_returns(dates, universe[CASH_SYMBOL], cash_fee_bps)
    groups = {b: group_index(dates, b) for b in BUCKETS}
    rows = []
    rets_by_lam = {}
    for lam in lambda_grid():
        row, r = frontier_row(dates, book.rets, cash, groups, lam)
        rows.append(row)
        rets_by_lam[lam] = r
    return {"name": name, "description": description, "dates": dates,
            "weights": weights, "window_symbols": window_symbols, "book": book,
            "cash": cash, "cash_used": cash_used, "rows": rows, "rets": rets_by_lam,
            "groups": groups, "cost_bps": cost_bps, "cash_fee_bps": cash_fee_bps,
            "sleeves": sleeves}


def rets_at(bookres, lam):
    """r(lambda) for ANY lambda, including off-grid ones."""
    return apply_lambda(bookres["book"].rets, bookres["cash"], lam)


def losing_years(bookres, lam):
    ps = period_returns(rets_at(bookres, lam), bookres["groups"]["Y"])
    return [(p["key"], p["ret"]) for p in ps if p["ret"] <= 0.0]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv=None):
    os.makedirs(OUT_DIR, exist_ok=True)
    universe = load_universe()
    prov = ["generated by study.py from data/*.csv",
            "pull date %s" % PULL_DATE,
            "sleeve rule: close > SMA(%d), equal weight, monthly rebalance"
            % SMA_TREND,
            "cash proxy: %s (3-month T-bill YIELD INDEX, percent per annum)"
            % CASH_SYMBOL,
            "price-only data, not total return",
            "frac_gt0 counts a period only if its return is strictly > 0; "
            "frac_ge0 counts it unless its return is strictly < 0"]

    print("=" * 78)
    print("THE POSITIVITY FRONTIER -- measure it, do not assume it")
    print("=" * 78)
    print("")
    print("INPUT SERIES (TradingView OHLCV, interval 1D, pull date %s)" % PULL_DATE)
    rows = [[s, len(universe[s]), universe[s].dates[0].isoformat(),
             universe[s].dates[-1].isoformat()]
            for s in ALL_SYMBOLS]
    for line in table(["symbol", "bars", "first", "last"], rows):
        print(line)
    print("")

    # ---- (0) REPRODUCTION CHECK -----------------------------------------
    print("-" * 78)
    print("(0) REPRODUCTION CHECK -- this study's simulator vs the weather-test's")
    print("-" * 78)
    repro = run_book(universe, *REPRO[0:4], 0.0)
    rh = level_stats(repro["dates"], repro["book"].rets)
    rly = len(losing_years(repro, 1.0))
    wp = WEATHER_TEST_PUBLISHED
    print("  weather-test published: window %s..%s n_days=%d cagr=%s max_dd=%s "
          "sharpe=%s losing_years=%d"
          % (wp["window_first"], "2026-10-14", wp["n_days"], pct(wp["cagr"]),
             pct(wp["max_dd"]), num(wp["sharpe_daily_ann"]), wp["losing_years"]))
    print("  this study, exact re-run : window %s..%s n_days=%d cagr=%s max_dd=%s "
          "sharpe=%s losing_years=%d"
          % (repro["dates"][0].isoformat(), repro["dates"][-1].isoformat(),
             rh["n_days"], pct(rh["cagr"]), pct(rh["max_dd"]), num(rh["sharpe"]),
             rly))
    d_cagr = abs(rh["cagr"] - wp["cagr"])
    d_dd = abs(rh["max_dd"] - wp["max_dd"])
    print("  absolute gap: cagr %.8f   max_dd %.8f   -> %s"
          % (d_cagr, d_dd,
             "IDENTICAL to 1e-6" if (d_cagr < 1e-6 and d_dd < 1e-6)
             else "DIFFERS -- reported, not hidden"))
    print("")

    # ---- run every book at zero cost -------------------------------------
    zero = {}
    for name, weights, wsy, desc in BOOKS:
        zero[name] = run_book(universe, name, weights, wsy, desc, 0.0)

    # ---- windows ---------------------------------------------------------
    print("-" * 78)
    print("(1) THE BOOKS AND THEIR WINDOWS")
    print("-" * 78)
    rows = [[n, len(zero[n]["weights"]), len(zero[n]["dates"]),
             zero[n]["dates"][0].isoformat(), zero[n]["dates"][-1].isoformat()]
            for n, _, _, _ in BOOKS]
    for line in table(["book", "sleeves", "days", "first", "last"], rows):
        print(line)
    print("")
    for name, weights, wsy, desc in BOOKS:
        print("  %-4s %s" % (name, desc))
        print("       sleeves: %s" % ", ".join(sorted(weights)))
    print("")
    print("  COMPLETE-PERIOD COUNTS (leading/trailing partial periods dropped):")
    rows = [[n] + [len(zero[n]["groups"][b]) for b in BUCKETS] for n, _, _, _ in BOOKS]
    for line in table(["book"] + BUCKETS, rows):
        print(line)
    print("")

    # ---- cash identity ---------------------------------------------------
    print("-" * 78)
    print("(2) THE CASH SERIES AND WHY THE lambda=0 COLUMN IS JUST THE CASH RATE")
    print("-" * 78)
    for name, _, _, _ in BOOKS:
        b = zero[name]
        cc = level_stats(b["dates"], b["cash"])["cagr"]
        print("  %-4s window %s..%s   cash CAGR %s   lambda=0 CAGR %s   "
              "identity gap %.12f"
              % (name, b["dates"][0].isoformat(), b["dates"][-1].isoformat(),
                 pct(cc), pct(b["rows"][0]["cagr"]), abs(cc - b["rows"][0]["cagr"])))
    print("")
    print("  ARITHMETIC, written out:  r(lambda) = lambda*r_risky + (1-lambda)*r_cash")
    print("    at lambda = 0 this is  r(0) = 0*r_risky + 1*r_cash = r_cash, term by")
    print("    term.  So the lambda=0 row of every frontier table below is the cash")
    print("    rate wearing a book's clothes, and its CAGR is exactly the cash CAGR")
    print("    above -- the identity gap column is there to show it, not to assert it.")
    print("")
    rows = [[n] + [pct(zero[n]["rows"][0][b], 1) for b in BUCKETS]
            + [pct(zero[n]["rows"][0][b + "_ge0"], 1) for b in ("D", "Y")]
            for n, _, _, _ in BOOKS]
    print("  lambda = 0 row -- the CASH PROXY ALONE:")
    for line in table(["book"] + ["%s>0" % b for b in BUCKETS]
                      + ["D>=0", "Y>=0"], rows):
        print(line)
    print("")
    print("  *** THE CASH PROXY ITSELF IS NOT POSITIVE EVERY DAY. ***")
    b = zero[PRIMARY]
    used = [u for u in b["cash_used"] if u is not NA]
    nbad = sum(1 for j in range(len(b["dates"])) if b["cash"][j] <= 0.0)
    nzero_rate = sum(1 for j in range(len(b["dates"]))
                     if b["cash_used"][j] is not NA and b["cash_used"][j] == 0.0)
    nneg_rate = sum(1 for j in range(len(b["dates"]))
                    if b["cash_used"][j] is not NA and b["cash_used"][j] < 0.0)
    print("    In %s's window: %d of %d days have a NON-POSITIVE cash accrual."
          % (PRIMARY, nbad, len(b["dates"])))
    print("      %d days the 3-month T-bill yield printed exactly 0.00%%," % nzero_rate)
    print("      %d days it printed NEGATIVE:" % nneg_rate)
    for j in range(len(b["dates"])):
        u = b["cash_used"][j]
        if u is not NA and u < 0.0:
            print("        %s  yield %.4f%%" % (b["dates"][j].isoformat(), u))
    print("      and %d days where the index had no prior print and the carried"
          % (nbad - nzero_rate - nneg_rate))
    print("      rate was zero or negative.")
    print("    US T-bill yields really did print zero (2011-2015) and negative")
    print("    (2015-09-30, 2020-03-25, 2020-03-26).  A cash-only plan fails")
    print("    'profitable every day' by itself; it fails it on 21 days in 21")
    print("    years.  That is the floor the whole frontier is standing on.")
    print("")
    print("    CROSS-CHECK -- why a PRICE series cannot stand in for cash:")
    bil = universe[CASH_PRICE_CROSSCHECK]
    bd = [d for d in b["dates"] if d in bil.index_of]
    if len(bd) > 300:
        br = [0.0] + [bil.c[bil.index_of[bd[j]]] / bil.c[bil.index_of[bd[j - 1]]] - 1.0
                      for j in range(1, len(bd))]
        bh = level_stats(bd, br)
        print("      %s (a 1-3 month T-bill ETF) PRICE-only over %s..%s: CAGR %s, "
              "%% days > 0 = %s"
              % (CASH_PRICE_CROSSCHECK, bd[0].isoformat(), bd[-1].isoformat(),
                 pct(bh["cagr"]),
                 pct(sum(1 for r in br[1:] if r > 0) / float(len(br) - 1), 1)))
        print("      i.e. the fund distributes its yield and the price goes nowhere,")
        print("      which is exactly why the cash series here is a YIELD INDEX and")
        print("      not a price.  The limitation runs the other way too: see README.")
    print("")

    # ---- the frontier ----------------------------------------------------
    for name, _, _, _ in BOOKS:
        b = zero[name]
        print("=" * 78)
        print("(3) FRONTIER -- %s  (round-trip cost 0 bps)" % name)
        print("=" * 78)
        print("  rows = exposure lambda.  cell = % of COMPLETE periods positive.")
        print("  STRICT reading (return > 0); lambda=1 is the book, lambda=0 is cash.")
        rows = [[num(r["lam"], 2)] + [pct(r[bk], 1) for bk in BUCKETS]
                for r in b["rows"]]
        for line in table(["lambda"] + BUCKETS, rows):
            print(line)
        print("")
        print("  LOOSE reading (return >= 0; a flat period is not a loss):")
        rows = [[num(r["lam"], 2)] + [pct(r[bk + "_ge0"], 1) for bk in BUCKETS]
                for r in b["rows"]]
        for line in table(["lambda"] + BUCKETS, rows):
            print(line)
        print("")
        print("  CAGR / max drawdown / Sharpe at the same lambda values:")
        rows = [[num(r["lam"], 2), pct(r["cagr"]), pct(r["max_dd"]), num(r["sharpe"], 3)]
                for r in b["rows"]]
        for line in table(["lambda", "CAGR", "max_dd(compounded)",
                           "sharpe(daily,ann)"], rows):
            print(line)
        print("")

    # ---- the trade-off table --------------------------------------------
    print("-" * 78)
    print("(4) THE TRADE-OFF CURVE -- the price of each extra positive year")
    print("-" * 78)
    for name, _, _, _ in BOOKS:
        b = zero[name]
        cc = level_stats(b["dates"], b["cash"])["cagr"]
        print("  %s   cash CAGR over the same window: %s" % (name, pct(cc)))
        rows = []
        for r in b["rows"]:
            rows.append([num(r["lam"], 2), pct(r["cagr"]), pct(r["cagr"] - cc),
                         pct(r["Y"], 1), pct(r["Q"], 1), pct(r["M"], 1),
                         pct(r["max_dd"]), num(r["sharpe"], 3),
                         r["Y_n"] - r["Y_pos"]])
        for line in table(["lambda", "CAGR", "CAGR-cash", "%Y>0", "%Q>0", "%M>0",
                           "max_dd", "sharpe", "losing_years"], rows):
            print(line)
        print("")

    # ---- where the frontier ends ----------------------------------------
    print("=" * 78)
    print("(5) WHERE THE FRONTIER ENDS")
    print("=" * 78)
    print("  Largest lambda at which 100% of COMPLETE periods are positive,")
    print("  resolved to 0.001 by bisection after a 0.05 grid scan.")
    print("  CAGR-there is compared with the cash rate over the SAME window.")
    print("")
    end_rows = {}
    for name, _, _, _ in BOOKS:
        b = zero[name]
        cc = level_stats(b["dates"], b["cash"])["cagr"]
        for bk in BUCKETS:
            lam, cagr, n, mono = max_lambda_all_positive(
                b["dates"], b["book"].rets, b["cash"], b["groups"], bk)
            end_rows[(name, bk)] = (lam, cagr, n, mono)
    rows = []
    for name, _, _, _ in BOOKS:
        b = zero[name]
        cc = level_stats(b["dates"], b["cash"])["cagr"]
        for bk in BUCKETS:
            lam, cagr, n, mono = end_rows[(name, bk)]
            rows.append([name, bk, n, "n/a" if lam is NA else num(lam, 3),
                         "n/a" if cagr is NA else pct(cagr),
                         "n/a" if cagr is NA else pct(cagr - cc),
                         "monotone" if mono else "NON-MONOTONE"])
    for line in table(["book", "bucket", "periods", "max lambda", "CAGR there",
                       "vs cash", "grid scan"], rows):
        print(line)
    print("")
    print("  Read `periods` first: `max lambda` for D is a claim about ~5000 days,")
    print("  for Y about ~20 years.  They are not the same claim, and none of them")
    print("  is a guarantee.  `n/a` means even lambda = 0.001 failed -- only cash")
    print("  itself cleared it, and at D/W/2W not even cash did (see section 2).")
    print("")

    # ---- the best positivity at a meaningful return ---------------------
    print("=" * 78)
    print("(6) BEST YEARLY POSITIVITY AT A RETURN ABOVE CASH")
    print("=" * 78)
    print("  `Meaningful` cannot be read off the data, so it is defined before the")
    print("  run as an annual excess over cash, and three thresholds are reported.")
    print("  Scan resolution 0.001 in lambda.")
    print("")
    for name, _, _, _ in BOOKS:
        b = zero[name]
        cc = level_stats(b["dates"], b["cash"])["cagr"]
        scan = fine_scan(b["dates"], b["book"].rets, b["cash"], b["groups"], "Y")
        rows = []
        for th in MEANINGFUL_EXCESS:
            got = best_positivity_at_excess(scan, cc, th)
            if got is None:
                rows.append([pct(th, 1), "none", "n/a", "n/a", "n/a", "n/a", "n/a"])
                continue
            ps = period_returns(rets_at(b, got["lam_max"]), b["groups"]["Y"])
            nlose = sum(1 for p in ps if p["ret"] <= 0.0)
            rows.append([pct(th, 1), num(got["lam_min"], 3), num(got["lam_max"], 3),
                         pct(got["cagr_max"]), pct(got["cagr_max"] - cc),
                         pct(got["frac"], 1) + " (%d of %d)"
                         % (len(ps) - nlose, len(ps)), got["n_ties"]])
        print("  %s   cash CAGR %s   complete years in window %d"
              % (name, pct(cc), len(b["groups"]["Y"])))
        for line in table(["min excess", "lam min", "lam max", "CAGR at lam max",
                           "CAGR-cash", "years > 0", "lambda plateau"], rows):
            print(line)
        for th in MEANINGFUL_EXCESS:
            got = best_positivity_at_excess(scan, cc, th)
            if got is None:
                print("    at min excess %-5s no lambda reaches it" % pct(th, 1))
                continue
            ps = period_returns(rets_at(b, got["lam_max"]), b["groups"]["Y"])
            lost = [(p["key"], p["ret"]) for p in ps if p["ret"] <= 0.0]
            print("    at min excess %-5s lambda %s..%s   losing years: %s"
                  % (pct(th, 1), num(got["lam_min"], 3), num(got["lam_max"], 3),
                     ", ".join("%s %s" % (k, pct(v, 2)) for k, v in lost)
                     if lost else "none"))
        print("")

    print("-" * 78)
    print("(6b) THE EFFICIENT YEARLY FRONTIER -- the most exposure that still holds")
    print("     each positivity level")
    print("-" * 78)
    print("  The positivity count is a STEP function of lambda, so most of the grid")
    print("  gives away return for nothing: lambda=0.05 and lambda=0.15 both deliver")
    print("  95% of years for one book, at 1.94% and 2.25%.  For each positivity level")
    print("  the table takes the LARGEST lambda that still attains it, which is the")
    print("  only point on the plateau worth holding.")
    print("")
    for name, _, _, _ in BOOKS:
        b = zero[name]
        cc = level_stats(b["dates"], b["cash"])["cagr"]
        scan = fine_scan(b["dates"], b["book"].rets, b["cash"], b["groups"], "Y")
        best_for = {}
        for lam, f1, f0, cagr in scan:
            if f1 is NA:
                continue
            if f1 not in best_for or lam > best_for[f1][0]:
                best_for[f1] = (lam, cagr)
        levels = sorted(best_for, reverse=True)
        rows = []
        for f in levels:
            lam, cagr = best_for[f]
            rows.append([pct(f, 1), num(lam, 3), pct(cagr), pct(cagr - cc),
                         pct(f, 1) == "100.0%" and "no losing year"
                         or "%d of %d years lost" % (round((1.0 - f)
                                                           * len(b["groups"]["Y"])),
                                                     len(b["groups"]["Y"]))])
        print("  %s   cash CAGR %s   %d complete years"
              % (name, pct(cc), len(b["groups"]["Y"])))
        for line in table(["years > 0", "max lambda there", "CAGR there",
                           "excess vs cash", "note"], rows):
            print(line)
        print("")

    # ---- quarters and months --------------------------------------------
    print("-" * 78)
    print("(7) IS ANY lambda POSITIVE IN EVERY QUARTER / HALF-YEAR / MONTH?")
    print("-" * 78)
    rows = []
    for name, _, _, _ in BOOKS:
        b = zero[name]
        cc = level_stats(b["dates"], b["cash"])["cagr"]
        for bk in ("Y", "H", "Q", "M"):
            lam, cagr, n, mono = end_rows[(name, bk)]
            rows.append([name, bk, n,
                         "n/a" if lam is NA else num(lam, 3),
                         "n/a" if cagr is NA else pct(cagr),
                         "n/a" if cagr is NA else pct(cagr - cc)])
    for line in table(["book", "bucket", "periods", "max lambda with ALL positive",
                       "CAGR there", "excess vs cash"], rows):
        print(line)
    print("")
    print("  Under the LOOSE reading the same question, for the three long buckets:")
    rows = []
    for name, _, _, _ in BOOKS:
        b = zero[name]
        cc = level_stats(b["dates"], b["cash"])["cagr"]
        for bk in ("Y", "H", "Q", "M"):
            lam, cagr, n, mono = max_lambda_all_positive(
                b["dates"], b["book"].rets, b["cash"], b["groups"], bk, ge0=True)
            rows.append([name, bk, n, "n/a" if lam is NA else num(lam, 3),
                         "n/a" if cagr is NA else pct(cagr),
                         "n/a" if cagr is NA else pct(cagr - cc)])
    for line in table(["book", "bucket", "periods", "max lambda (>=0)", "CAGR there",
                       "excess vs cash"], rows):
        print(line)
    print("")

    # ---- where the first step goes --------------------------------------
    print("-" * 78)
    print("(8) THE FIRST 5% OF RISK IS THE EXPENSIVE PART")
    print("-" * 78)
    print("  The frontier is not linear in lambda, and it is not the flat days that")
    print("  make it so.  Almost the whole fall in positivity happens between")
    print("  lambda=0 and lambda=0.05 -- between holding cash and holding 95% cash.")
    print("  At lambda=0.05 the risky term contributes 0.05 of the book's daily swing")
    print("  while cash contributes 0.95 of roughly one daily accrual, so the SIGN of")
    print("  the day's return is decided by the risky sliver.  Measured:")
    print("")
    rows = []
    for name, _, _, _ in BOOKS:
        b = zero[name]
        h1 = level_stats(b["dates"], b["rets"][1.0])
        sd1 = h1["sd_daily"]
        cash_d = sum(b["cash"]) / float(len(b["cash"]))
        ratio = (0.05 * sd1) / cash_d if cash_d else NA
        rows.append([name, pct(sd1), pct(cash_d, 4), num(ratio, 1),
                     pct(b["rows"][0]["D"], 1), pct(b["rows"][1]["D"], 1),
                     pct(b["rows"][-1]["D"], 1)])
    for line in table(["book", "book daily sd", "cash accrual/day",
                       "risky-sd / cash at lam=0.05", "D>0 @lam0", "D>0 @lam0.05",
                       "D>0 @lam1"], rows):
        print(line)
    print("")
    print("  A SEPARATE, ALSO TRUE FACT -- flat days.  A trend book that is out of")
    print("  the market returns EXACTLY zero, and the strict reading cannot count a")
    print("  zero as profitable, so the book's own share of positive days understates")
    print("  its in-market win rate.  Counted:")
    print("")
    rows = []
    for name, _, _, _ in BOOKS:
        b = zero[name]
        r = b["book"].rets
        nz = sum(1 for j in range(1, len(r)) if r[j] == 0.0)
        loose = b["rows"][-1]["D_ge0"]
        rows.append([name, len(r) - 1, nz, pct(nz / float(len(r) - 1), 1),
                     pct(b["rows"][-1]["D"], 1), pct(loose, 1),
                     pct(b["rows"][-1]["Y"], 1), pct(b["rows"][-1]["Y_ge0"], 1)])
    for line in table(["book", "days", "flat days", "% flat", "D>0 @lam1",
                       "D>=0 @lam1", "Y>0 @lam1", "Y>=0 @lam1"], rows):
        print(line)
    print("")
    print("  The loose reading does NOT move the monthly/quarterly/yearly endpoints:")
    print("  a cash sliver of 0.8% already makes any flat month positive, so the two")
    print("  readings agree on every bucket from M outward.  It does not rescue the")
    print("  daily endpoint either, because 2 days in 21 years had a strictly")
    print("  NEGATIVE cash accrual (section 2).")
    print("")
    print("  HOW THIN THE YEAR ENDPOINT IS.  The binding year for the primary book is")
    b = zero[PRIMARY]
    cc = level_stats(b["dates"], b["cash"])["cagr"]
    lamY, cagrY, nY, _ = end_rows[(PRIMARY, "Y")]
    if lamY is not NA:
        y_at = period_returns(rets_at(b, lamY), b["groups"]["Y"])
        worst = min(y_at, key=lambda p: p["ret"])
        nxt = round(lamY + FINE_STEP, 6)
        y_next = period_returns(rets_at(b, nxt), b["groups"]["Y"])
        lost_next = [(p["key"], p["ret"]) for p in y_next if p["ret"] <= 0.0]
        print("  %s, the year with the smallest return at the endpoint:" % worst["key"])
        print("    lambda=%.3f -- %s returns %s; %% of years positive 100%%"
              % (lamY, worst["key"], pct(worst["ret"], 4)))
        print("    lambda=%.3f -- %s" % (nxt, ", ".join(
            "%s %s" % (k, pct(v, 4)) for k, v in lost_next) if lost_next
            else "still all positive"))
        print("    The endpoint is decided by ONE year, and the whole difference")
        print("    between 'positive in every year' and 'not positive in every year'")
        print("    is %.4f percentage points of that one year's return."
              % (abs(worst["ret"] - lost_next[0][1]) * 100.0 if lost_next else 0.0))
    print("")

    # ---- costs -----------------------------------------------------------
    print("=" * 78)
    print("(9) COSTS -- the frontier re-run at 5 and 20 bps round trip")
    print("=" * 78)
    cost_rows = []
    for name, weights, wsy, desc in BOOKS:
        for rt in ROUND_TRIPS_BPS:
            rb = run_book(universe, name, weights, wsy, desc, rt)
            h1 = level_stats(rb["dates"], rb["rets"][1.0])
            lamY, cagrY, nY, _ = max_lambda_all_positive(
                rb["dates"], rb["book"].rets, rb["cash"], rb["groups"], "Y")
            cost_rows.append([name, num(rt, 0), num(h1["cagr"], 6),
                              num(h1["max_dd"], 6), num(h1["sharpe"], 6),
                              num(rb["rows"][-1]["Y"], 6),
                              "" if lamY is NA else num(lamY, 3)])
    for line in table(["book", "rt bps", "CAGR@lam1", "max_dd@lam1",
                       "sharpe@lam1", "%Y>0@lam1", "max lambda 100%-years"],
                      [[r[0], r[1], pct(float(r[2])), pct(float(r[3])),
                        num(float(r[4]), 3), pct(float(r[5]), 1), r[6]]
                       for r in cost_rows]):
        print(line)
    print("")
    print("  SHIFT 0 bps -> 20 bps along the whole frontier at lambda = 1:")
    for name, _, _, _ in BOOKS:
        a = [r for r in cost_rows if r[0] == name and r[1] == "0"][0]
        c = [r for r in cost_rows if r[0] == name and r[1] == "20"][0]
        print("    %-4s CAGR %s -> %s   (%.2f pp)   %%Y>0 %s -> %s   max_dd %s -> %s"
              % (name, pct(float(a[2])), pct(float(c[2])),
                 100.0 * (float(c[2]) - float(a[2])), pct(float(a[5]), 1),
                 pct(float(c[5]), 1), pct(float(a[3])), pct(float(c[3]))))
    print("")

    # ---- bucket statistics at the book itself ---------------------------
    print("-" * 78)
    print("(10) SAMPLE SIZE AT lambda = 1 -- n_periods is NOT an independent sample")
    print("-" * 78)
    rows = []
    for name, _, _, _ in BOOKS:
        b = zero[name]
        for bk in BUCKETS:
            st = bucket_engine_stats(b["book"].rets, b["groups"][bk], bk)
            rho = st["lag1_autocorrelation"]
            rows.append([name, bk, st["n_periods"],
                         num(rho, 3) if rho is not NA else "n/a",
                         num(st["n_eff"], 1) if st["n_eff"] is not NA else "n/a",
                         num(st["t_stat"], 2) if st["t_stat"] is not NA else "n/a"])
    for line in table(["book", "bucket", "n_periods", "lag1 autocorr", "n_effective",
                       "t_stat"], rows):
        print(line)
    print("")
    print("  t_stat here is the engine's across-period statistic on the period's own")
    print("  compounded return.  H contains Q contains M contains the same days, so")
    print("  it is a STABILITY INDICATOR, not a significance test of an edge.")
    print("")

    # ---- year by year ---------------------------------------------------
    print("-" * 78)
    print("(11) EVERY YEAR, EVERY lambda -- losing years are not summarised away")
    print("-" * 78)
    lams = [0.0, 0.05, 0.25, 0.5, 0.75, 1.0]
    for name, _, _, _ in BOOKS:
        b = zero[name]
        ys = [p["key"] for p in period_returns(b["book"].rets, b["groups"]["Y"])]
        rows = []
        for y in ys:
            r = [y]
            for lam in lams:
                ps = [p for p in period_returns(rets_at(b, lam), b["groups"]["Y"])
                      if p["key"] == y]
                r.append(pct(ps[0]["ret"], 1) if ps else "n/a")
            rows.append(r)
        print("  %s" % name)
        for line in table(["year"] + ["lam=%s" % num(l, 2) for l in lams], rows):
            print(line)
        print("")

    # ---- write artefacts -------------------------------------------------
    written = []
    for name, _, _, _ in BOOKS:
        b = zero[name]
        cc = level_stats(b["dates"], b["cash"])["cagr"]
        scan_y = fine_scan(b["dates"], b["book"].rets, b["cash"], b["groups"], "Y")
        base = ["window %s..%s" % (b["dates"][0].isoformat(),
                                  b["dates"][-1].isoformat()),
                "round-trip cost %s bps" % num(b["cost_bps"], 1),
                "cash CAGR over this window %s" % num(cc, 6)] + prov
        written.append(("frontier_%s_rt0.csv" % name,
                        ["rows = lambda; cells = fraction of COMPLETE periods with "
                         "a return STRICTLY > 0"] + base,
                        ["lambda"] + BUCKETS,
                        [[num(r["lam"], 2)] + [num(r[bk], 6) for bk in BUCKETS]
                         for r in b["rows"]]))
        written.append(("frontier_ge0_%s_rt0.csv" % name,
                        ["rows = lambda; cells = fraction of COMPLETE periods with "
                         "a return >= 0 (a flat period is not a loss)"] + base,
                        ["lambda"] + BUCKETS,
                        [[num(r["lam"], 2)] + [num(r[bk + "_ge0"], 6) for bk in BUCKETS]
                         for r in b["rows"]]))
        written.append(("levels_%s_rt0.csv" % name,
                        ["per-lambda level statistics and strict/loose positivity",
                         "n_zero_<bucket> = complete periods whose return is exactly "
                         "0.0, counted as non-positive under the strict reading"]
                        + base,
                        ["lambda", "cagr", "max_dd", "max_dd_additive", "sharpe",
                         "years_pos_frac", "years_nonneg_frac", "quarters_pos_frac",
                         "months_pos_frac", "n_years", "n_losing_years",
                         "n_zero_Y", "n_zero_M", "n_zero_D"],
                        [[num(r["lam"], 2), num(r["cagr"], 6), num(r["max_dd"], 6),
                          num(r["max_dd_additive"], 6), num(r["sharpe"], 6),
                          num(r["Y"], 6), num(r["Y_ge0"], 6), num(r["Q"], 6),
                          num(r["M"], 6), r["Y_n"], r["Y_n"] - r["Y_pos"],
                          r["Y_zero"], r["M_zero"], r["D_zero"]]
                         for r in b["rows"]]))
        written.append(("tradeoff_%s_rt0.csv" % name, base,
                        ["lambda", "cagr", "cash_cagr", "excess_cagr",
                         "yearly_pos_frac", "yearly_nonneg_frac",
                         "quarterly_pos_frac", "monthly_pos_frac", "max_dd",
                         "sharpe", "losing_years"],
                        [[num(r["lam"], 2), num(r["cagr"], 6), num(cc, 6),
                          num(r["cagr"] - cc, 6), num(r["Y"], 6), num(r["Y_ge0"], 6),
                          num(r["Q"], 6), num(r["M"], 6), num(r["max_dd"], 6),
                          num(r["sharpe"], 6), r["Y_n"] - r["Y_pos"]]
                         for r in b["rows"]]))
        lams_all = sorted(b["rets"])
        ys = [p["key"] for p in period_returns(b["book"].rets, b["groups"]["Y"])]
        written.append(("yearly_%s_rt0.csv" % name,
                        ["every complete year, compounded return, at each lambda"]
                        + base,
                        ["year"] + ["lam_%s" % num(l, 2) for l in lams_all],
                        [[y] + [num([p for p in period_returns(rets_at(b, l),
                                                               b["groups"]["Y"])
                                     if p["key"] == y][0]["ret"], 6)
                                for l in lams_all] for y in ys]))
        written.append(("losing_years_%s_rt0.csv" % name,
                        ["years with a return <= 0, per lambda"] + base,
                        ["lambda", "n_losing_years", "losing_years", "losing_returns"],
                        [[num(l, 2), len(losing_years(b, l)),
                          " ".join(k for k, _ in losing_years(b, l)),
                          " ".join(num(v, 6) for _, v in losing_years(b, l))]
                         for l in lams_all]))
        written.append(("yearly_positivity_%s_rt0.csv" % name,
                        ["the frontier's endpoint at the 0.001 resolution, per "
                         "meaningful-return threshold"] + base,
                        ["min_excess", "lambda_min", "lambda_max", "cagr_at_lam_max",
                         "excess_at_lam_max", "yearly_pos_frac", "n_years",
                         "n_losing_years", "losing_years_at_lam_max"],
                        [[num(th, 6)] + (["", "", "", "", "", "", "", "none"]
                                         if best_positivity_at_excess(scan_y, cc, th)
                                         is None
                                         else (lambda g: [
                                             num(g["lam_min"], 3),
                                             num(g["lam_max"], 3),
                                             num(g["cagr_max"], 6),
                                             num(g["cagr_max"] - cc, 6),
                                             num(g["frac"], 6),
                                             len(b["groups"]["Y"]),
                                             len(losing_years(b, g["lam_max"])),
                                             " ".join(k for k, _ in
                                                      losing_years(b, g["lam_max"]))
                                         ])(
                                             best_positivity_at_excess(scan_y, cc, th)))
                         for th in MEANINGFUL_EXCESS]))
        st_rows = []
        for bk in BUCKETS:
            st = bucket_engine_stats(b["book"].rets, b["groups"][bk], bk)
            st_rows.append([bk, st["n_periods"], num(st["mean_period_pnl"], 6),
                            num(st["sd_period_pnl"], 6), num(st["win_rate"], 6),
                            num(st["t_stat"], 6), num(st["lag1_autocorrelation"], 6),
                            num(st["n_eff"], 6)])
        written.append(("bucket_stats_%s_rt0.csv" % name,
                        ["engine aggregate_bucket() at lambda = 1, one synthetic "
                         "trade per period carrying the period's compounded return",
                         "the trade's close_date is the period's FIRST session, so "
                         "the engine's own bucketing reproduces these periods "
                         "exactly"] + base,
                        ["bucket", "n_periods", "mean_period", "sd_period",
                         "win_rate", "t_stat", "lag1_autocorr", "n_eff"], st_rows))
        syms = sorted(b["weights"])
        written.append(("book_daily_%s_rt0.csv" % name,
                        ["audit trail: sleeve returns, the book's own return and "
                         "the cash accrual, per book date",
                         "r(lambda) = lambda*book_ret + (1-lambda)*cash_ret"] + base,
                        ["date"] + syms + ["book_ret", "cash_ret", "cash_rate_used"],
                        [[d.isoformat()] + [num(b["book"].sleeve_rets[s][j], 8)
                                            for s in syms]
                         + [num(b["book"].rets[j], 8), num(b["cash"][j], 8),
                            "" if b["cash_used"][j] is NA
                            else num(b["cash_used"][j], 6)]
                         for j, d in enumerate(b["dates"])]))
        srows = []
        for s in syms:
            h = level_stats(b["dates"], b["book"].sleeve_rets[s])
            srows.append([s, b["weights"][s], num(h["cagr"], 6),
                          num(h["max_dd"], 6), num(h["sharpe"], 6)])
        written.append(("sleeve_headline_%s_rt0.csv" % name, base,
                        ["sleeve", "weight", "cagr", "max_dd", "sharpe"], srows))
        h1 = level_stats(b["dates"], b["rets"][1.0])
        cash_d = sum(b["cash"]) / float(len(b["cash"]))
        nzflat = sum(1 for j in range(1, len(b["book"].rets))
                     if b["book"].rets[j] == 0.0)
        days = len(b["book"].rets) - 1
        written.append(("structural_%s_rt0.csv" % name,
                        ["why the frontier is not linear: the first 5% of risk "
                         "decides the sign of the day, the flat days decide the "
                         "strict reading of the book's own positivity"] + base,
                        ["quantity", "value"],
                        [["days", days],
                         ["flat_days_book_ret_exactly_zero", nzflat],
                         ["flat_day_fraction", num(nzflat / float(days), 6)],
                         ["book_daily_sd", num(h1["sd_daily"], 8)],
                         ["book_daily_mean", num(h1["mean_daily"], 8)],
                         ["cash_daily_mean", num(cash_d, 8)],
                         ["risky_sd_over_cash_at_lam005",
                          num((0.05 * h1["sd_daily"]) / cash_d, 6)
                          if cash_d else ""],
                         ["daily_pos_frac_lam0", num(b["rows"][0]["D"], 6)],
                         ["daily_pos_frac_lam005", num(b["rows"][1]["D"], 6)],
                         ["daily_pos_frac_lam1", num(b["rows"][-1]["D"], 6)],
                         ["daily_nonneg_frac_lam1", num(b["rows"][-1]["D_ge0"], 6)],
                         ["daily_pos_frac_lam0_ge0", num(b["rows"][0]["D_ge0"], 6)]]))

    b0 = zero[PRIMARY]
    written.append(("cash_series.csv",
                    ["the cash proxy, per book date of %s" % PRIMARY,
                     "%s close is a PERCENT-PER-ANNUM YIELD, not a price"
                     % CASH_SYMBOL,
                     "r_cash[j] = yield(close of the previous book date)/100/252",
                     "cash_rate_used is the yield the row's accrual actually used; "
                     "blank when no prior print existed"] + prov,
                    ["date", "us03m_pct", "r_cash_daily", "cash_rate_used"],
                    [[d.isoformat(),
                      num(universe[CASH_SYMBOL].c[universe[CASH_SYMBOL].index_of[d]], 4)
                      if d in universe[CASH_SYMBOL].index_of else "",
                      num(b0["cash"][j], 8),
                      "" if b0["cash_used"][j] is NA
                      else num(b0["cash_used"][j], 6)]
                     for j, d in enumerate(b0["dates"])]))
    written.append(("cost_shift.csv",
                    ["the frontier's endpoint and lambda=1 levels at each round-trip "
                     "cost"] + prov,
                    ["book", "round_trip_bps", "cagr_at_lam1", "max_dd_at_lam1",
                     "sharpe_at_lam1", "yearly_pos_frac_at_lam1",
                     "max_lambda_100pct_years"], cost_rows))
    erows = []
    for name, _, _, _ in BOOKS:
        b = zero[name]
        cc = level_stats(b["dates"], b["cash"])["cagr"]
        for bk in BUCKETS:
            lam, cagr, n, mono = end_rows[(name, bk)]
            erows.append([name, bk, n, "" if lam is NA else num(lam, 3),
                          "" if cagr is NA else num(cagr, 6),
                          "" if cagr is NA else num(cagr - cc, 6), 1 if mono else 0])
    written.append(("frontier_end.csv",
                    ["max lambda at which every COMPLETE period of the bucket is "
                     "positive, bisected to 0.001",
                     "monotone=1 means the 0.05 grid scan never saw the positivity "
                     "fraction rise as lambda rose"] + prov,
                    ["book", "bucket", "n_periods", "max_lambda", "cagr_there",
                     "excess_vs_cash", "monotone"], erows))
    written.append(("reproduction_check.csv",
                    ["this study's re-run of the weather-test's published book, "
                     "against that study's published numbers"] + prov,
                    ["quantity", "weather_test_published", "this_study", "abs_gap"],
                    [["cagr", num(wp["cagr"], 6), num(rh["cagr"], 6), num(d_cagr, 8)],
                     ["max_dd", num(wp["max_dd"], 6), num(rh["max_dd"], 6),
                      num(d_dd, 8)],
                     ["sharpe_daily_ann", num(wp["sharpe_daily_ann"], 6),
                      num(rh["sharpe"], 6),
                      num(abs(rh["sharpe"] - wp["sharpe_daily_ann"]), 8)],
                     ["n_days", wp["n_days"], rh["n_days"],
                      abs(wp["n_days"] - rh["n_days"])],
                     ["window_first", wp["window_first"],
                      repro["dates"][0].isoformat(),
                      0 if repro["dates"][0].isoformat() == wp["window_first"] else 1],
                     ["losing_years", wp["losing_years"], rly,
                      abs(wp["losing_years"] - rly)]]))

    for fname, provenance, headers, rows in written:
        n = write_csv(os.path.join(OUT_DIR, fname), provenance, headers, rows)
        print("  wrote out/%-38s %6d rows" % (fname, n))
    print("")
    print("DONE. out/*.csv holds every table; stdout above is the summary.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
