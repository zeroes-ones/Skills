#!/usr/bin/env python3
"""
study.py -- the ALL-WEATHER TEST.

Deterministic. Stdlib only. No network. No third-party imports.

WHAT THIS IS
    Two sibling studies already established, on real daily data:

      * equity-trading-playbook/examples/regime-study
            no single rule set is profitable in every year or every regime;
      * options-trading-playbook/examples/regime-study
            the mean-reversion / vol-premium corner, with a corrected
            variance-risk-premium finding.

    Together they also showed that the trend / mean-reversion / buy-and-hold
    sleeves they tested are 0.666-0.887 correlated year to year -- one bet with
    different exits, not several bets -- so combining them cannot diversify.

    This study tests what was NOT tested: a portfolio of sleeves chosen to be
    structurally different from one another, combined at PRE-REGISTERED FIXED
    WEIGHTS with no optimisation, and reported with its worst year and worst
    drawdown in the open.

THE PRE-REGISTERED BOOK (fixed before the first number; do not read a tuned
variant of this anywhere in this file -- there is no loop over these weights
except the explicitly-labelled, separate optimisation comparison in section 12)

    Equal-risk, 20% each, rebalanced monthly, one book:
      A  equity trend       long AMEX:SPY  when close > SMA(200), else flat
      B  bond trend         long NASDAQ:TLT when close > SMA(200), else flat
      C  gold trend         long AMEX:GLD  when close > SMA(200), else flat
      D  ex-US equity trend long AMEX:EEM  when close > SMA(200), else flat
      E  long volatility    long TVC:VIX   when VIX > SMA(50), else flat
    Comparisons, same construction:
      F  the four trend sleeves A-D at 25% each (no vol sleeve)
      G  100% buy-and-hold SPY

WHAT SLEEVE E ACTUALLY IS -- READ THIS BEFORE READING ANY NUMBER FROM IT
    The VIX index is NOT a tradable instrument. There is no price series for
    "long the VIX". Sleeve E is therefore a SIGNAL sleeve: its return is
    approximated by the day-over-day change in the VIX index level while the
    rule is long, and no tradable instrument is modelled. A real long-volatility
    position is taken in VIX futures or a futures-based ETN, whose return is the
    futures return, and which bleeds on roll in contango -- a cost this proxy
    does not have. The proxy therefore OVERSTATES sleeve E. Every number from
    sleeve E is an upper bound on the return of the signal, not an achievable
    return. It is reported because the question "does a crisis sleeve decorrelate
    the book" is worth answering even when the tradable form is unavailable.

EXECUTION MODEL (stated once; every result depends on it)
    * Signal on the CLOSE of day i; the position implied by that signal is held
      through day i+1. No signal is ever executed on the bar that produced it.
      Concretely: return on day t = pos[t-1] * (close[t]/close[t-1] - 1).
    * A sleeve is FLAT, not short, when its rule is off. The instrument's own
      trend cannot produce a negative return except inside a long position.
    * Warm-up: until a sleeve's moving average exists it is FLAT. The book
      therefore starts on the first date on which EVERY sleeve's rule is
      computable, so that day one is a real five-sleeve book.
    * Monthly rebalance to the pre-registered weights: between rebalances each
      sleeve's value drifts with its own return, so the weights drift too; at
      the first day of a new calendar month each sleeve is reset to its target
      share of the book.
    * Costs are OFF by default (as in both sibling studies) and are turned on in
      section 11 at 5 and 20 bps round trip. When on: each position flip
      (flat<->long) costs half the round-trip rate on that sleeve's notional,
      and each monthly rebalance costs half the round-trip rate on one-way
      turnover.
    * No dividends or distributions. Every series is PRICE-ONLY, so any
      always-long sleeve is understated relative to a total-return version.

WHAT THIS ENGINE OWNS, AND WHAT IT DELIBERATELY DOES NOT
    Timeframe bucketing and the significance machinery belong to the sibling
    engine
        skills/14-finance/timeframe-performance-statistics/scripts/timeframe_stats.py
    This script IMPORTS that engine and calls bucket_key(), aggregate_bucket(),
    sample_sd(), max_drawdown(), lag1_autocorr() and n_effective() rather than
    re-implementing them. If that file moves, this script fails loudly.
    Its max_drawdown() is ADDITIVE by design (peak-to-trough of a cumulative
    P&L series, in currency) and is used here for exactly that: the yearly
    cross-check in section 7 and the additive book drawdown quoted alongside the
    headline. The headline max drawdown is the COMPOUNDED peak-to-trough of the
    equity curve, as a negative fraction, which is a stricter and different
    measure; it is computed by max_drawdown_pct() below, using the same
    definition and the same code shape the sibling regime study used, so the two
    studies are comparable number for number.
    Sharpe convention: daily simple returns, full sample, Rf = 0, x sqrt(252).

OUTPUT
    Sections are printed between `===== SECTION ... =====` markers; all the
    tables in RESULTS.md are sliced out of this stdout by make-results.py.
"""

import argparse
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
SMA_VIX = 50

# Pre-registered. Fixed. Not searched anywhere except section 12, which is
# labelled as the fitted comparison and is not the recommendation.
SLEEVE_ORDER = ["A", "B", "C", "D", "E"]
SLEEVE_DEF = {
    "A": ("equity trend", "SPY", SMA_TREND),
    "B": ("bond trend", "TLT", SMA_TREND),
    "C": ("gold trend", "GLD", SMA_TREND),
    "D": ("ex-US equity trend", "EEM", SMA_TREND),
    "E": ("long-volatility (VIX signal, NOT tradable)", "VIX", SMA_VIX),
}
PREREGISTERED_WEIGHTS = {"A": 0.20, "B": 0.20, "C": 0.20, "D": 0.20, "E": 0.20}
WEIGHTS_F = {"A": 0.25, "B": 0.25, "C": 0.25, "D": 0.25}

REBALANCE_COST_FREE = 0.0
GRID_STEP = 0.10
IS_FRACTION = 0.70
ROLLING_LOOKBACKS = {
    "12m": TRADING_DAYS_PER_YEAR,
    "36m": 3 * TRADING_DAYS_PER_YEAR,
}
ALL_WEATHER_HORIZONS = [("1y", 1), ("2y", 2), ("3y", 3), ("5y", 5), ("7y", 7),
                        ("10y", 10)]


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
            "  max_drawdown / lag1_autocorr / n_effective instead of re-implementing\n"
            "  them, and refuses to substitute its own formulae." % path)
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


# The repo requires LF everywhere. Redirected stdout on Windows would otherwise
# translate every newline to CRLF, which fails the file-format gate.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")


# ---------------------------------------------------------------------------
# Small formatting + arithmetic helpers
# ---------------------------------------------------------------------------

def pct(v, nd=2):
    if v is NA:
        return "n/a"
    return ("%+." + str(nd) + "f%%") % (v * 100.0)


def pct_unsigned(v, nd=2):
    if v is NA:
        return "n/a"
    return ("%." + str(nd) + "f%%") % (v * 100.0)


def num(v, nd=4):
    if v is NA:
        return "n/a"
    return ("%." + str(nd) + "f") % v


def mean(xs):
    return sum(xs) / len(xs) if xs else NA


def cov(xs, ys):
    n = min(len(xs), len(ys))
    if n < 2:
        return NA
    mx = sum(xs[:n]) / n
    my = sum(ys[:n]) / n
    return sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / (n - 1)


def pearson_via_engine_sd(xs, ys):
    """Pearson r, with the dispersion taken from the engine's sample_sd().

    r = cov(x,y) / (sd(x) * sd(y)).  sample_sd() is the sibling engine's.
    """
    n = min(len(xs), len(ys))
    if n < 3:
        return NA
    sx = TF.sample_sd(xs[:n])
    sy = TF.sample_sd(ys[:n])
    if sx is NA or sy is NA or sx == 0.0 or sy == 0.0:
        return NA
    return cov(xs, ys) / (sx * sy)


def equity_curve(rets):
    curve = [1.0]
    for r in rets:
        curve.append(curve[-1] * (1.0 + r))
    return curve


def max_drawdown_pct(curve):
    """Peak-to-trough fall of a compounded equity curve, as a NEGATIVE pct.

    Same definition and code shape as the sibling regime study's function of the
    same name, so the two studies' drawdown columns are comparable.
    """
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


def headline(rets, dates):
    """CAGR / compounded max drawdown / daily Sharpe. Conventions in the docstring."""
    n = len(rets)
    curve = equity_curve(rets)
    yrs = years_between(dates[0], dates[-1])
    if curve[-1] <= 0.0:
        cagr = -1.0
    else:
        cagr = curve[-1] ** (1.0 / yrs) - 1.0
    m = sum(rets) / n if n else NA
    sd = TF.sample_sd(rets)
    sharpe = (m / sd * math.sqrt(TRADING_DAYS_PER_YEAR)) if (sd not in (NA, 0)) else NA
    return {
        "n_days": n,
        "years": yrs,
        "total_return": curve[-1] - 1.0,
        "cagr": cagr,
        "max_dd": max_drawdown_pct(curve),
        "max_dd_additive": TF.max_drawdown(rets),
        "sharpe_daily_ann": sharpe,
        "mean_daily": m,
        "sd_daily": sd,
        "equity_end": curve[-1],
    }


def table(headers, rows, indent="  "):
    widths = [len(h) for h in headers]
    for r in rows:
        for i, c in enumerate(r):
            widths[i] = max(widths[i], len(str(c)))
    out = []
    out.append(indent + "  ".join(str(h).ljust(widths[i])
                                  for i, h in enumerate(headers)).rstrip())
    out.append(indent + "  ".join("-" * widths[i] for i in range(len(headers))))
    for r in rows:
        out.append(indent + "  ".join(str(c).ljust(widths[i])
                                      for i, c in enumerate(r)).rstrip())
    return out


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
    for sym in ("SPY", "TLT", "GLD", "EEM", "VIX"):
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
# Sleeves
# ---------------------------------------------------------------------------

class Sleeve(object):
    """One pre-registered rule, reduced to a daily return series.

    pos[i]  = 1 if the rule is long on the close of day i, else 0 (or None during
              the moving-average warm-up, which behaves as flat).
    ret[i]  = the return earned on day i = pos[i-1] * (close[i]/close[i-1] - 1).
    flip[i] = the position held on day i differs from the one held on day i-1,
              i.e. a change of state was executed on the close of day i-1.
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
        """(ret, hold, flip) arrays aligned to `dates`.

        THE ONE CONVENTION THAT MATTERS HERE, stated because it is a choice and
        not a fact: **a position may only change on a BOOK date.** The position
        held through book date j is the one the rule established at the close of
        the previous book date's bar, on which this instrument actually traded.
        So

            hold[j] = pos at the previous book date's bar
            ret[j]  = hold[j] * (close[k] / close[previous book date's bar] - 1)

        The equity instruments and the VIX index do not share an identical
        calendar (CBOE trades on Good Friday, NYSE does not; VIX also carries 22
        date stamps inside this window that the equity instruments do not). Two
        consequences, both handled rather than hidden:

          * a date the instrument has no bar for contributes a return of exactly
            0.0 and carries the previous position;
          * a bar of its own that falls between two book dates is NOT allowed to
            change the position, because the book could not have acted on it.
            Its price move is still fully counted: the next book date measures
            the return from that bar's close.

        Nothing is lost and nothing is invented.
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


def build_sleeves(universe):
    out = {}
    for code in SLEEVE_ORDER:
        _, sym, window = SLEEVE_DEF[code]
        out[code] = Sleeve(code, universe[sym], window)
    return out


def book_window(sleeves, universe):
    """Book window = first date on which EVERY sleeve's rule is computable."""
    start = max(sleeves[c].first_live for c in SLEEVE_ORDER)
    sets = [set(s.dates) for s in universe.values()]
    common = set.intersection(*sets)
    dates = sorted(d for d in common if d >= start)
    for d in dates:
        for sym, s in universe.items():
            if d not in s.index_of:
                raise SystemExit("ERROR: %s missing from %s inside the book window"
                                 % (d.isoformat(), sym))
    return dates


# ---------------------------------------------------------------------------
# The book
# ---------------------------------------------------------------------------

class BookResult(object):
    def __init__(self):
        self.dates = []
        self.rets = []
        self.sleeve_rets = {}
        self.sleeve_weights = {}
        self.sleeve_values = {}
        self.flips = {}
        self.rebalances = []
        self.turnover_total = 0.0
        self.flips_total = 0
        self.cost_bps = 0.0


def simulate(dates, aligned, weights, cost_bps=0.0):
    """Run the fixed-weight, monthly-rebalanced book over `dates`.

    `aligned` maps sleeve code -> (ret, hold, flip) arrays already aligned to
    `dates`. The weights are the PRE-REGISTERED shares and are never searched
    here.

    The book is carried in WEIGHT space with an explicit equity level:

        cost_j   = (round_trip/2) * sum of the weights that flipped on day j
                 + (round_trip/2) * one-way turnover on a rebalance day
        gross_j  = sum_c  w_c * r_c(j)
        R_j      = (1 + gross_j) * (1 - cost_j) - 1

    Charging the cost in the RETURN is what makes it bite. Charging it by
    shrinking a sleeve's dollar value does not: the weights are renormalised
    every day, so a haircut on one sleeve's value changes the mix and leaves the
    level untouched.
    """
    codes = [c for c in SLEEVE_ORDER if weights.get(c, 0.0) > 0.0]
    tot = sum(weights[c] for c in codes)
    target = {c: weights[c] / tot for c in codes}
    half = (cost_bps / 2.0) / 10000.0

    res = BookResult()
    res.cost_bps = cost_bps
    res.dates = list(dates)
    if len(dates) < 2:
        raise SystemExit("ERROR: book window has fewer than 2 days")

    w = dict(target)
    month_prev = dates[0].month

    res.rets.append(0.0)
    for c in codes:
        res.sleeve_rets.setdefault(c, []).append(0.0)
        res.sleeve_weights.setdefault(c, []).append(w[c])
        res.sleeve_values.setdefault(c, []).append(w[c])
        res.flips.setdefault(c, []).append(False)

    for j in range(1, len(dates)):
        d = dates[j]

        # --- (1) costs: flips executed on the close of the previous day ------
        cost = 0.0
        day_flips = {}
        for c in codes:
            f = aligned[c][2][j]
            day_flips[c] = f
            if f:
                cost += half * w[c]
                res.flips_total += 1

        # --- (2) the monthly rebalance, at the same close --------------------
        rebalance = (d.month != month_prev)
        turnover = 0.0
        if rebalance:
            turnover = 0.5 * sum(abs(target[c] - w[c]) for c in codes)
            cost += half * turnover
            res.turnover_total += turnover
            res.rebalances.append((d, turnover))
        month_prev = d.month

        # weights actually held through day j
        w_held = dict(target) if rebalance else dict(w)
        if cost >= 1.0:
            cost = 1.0

        # --- (3) the day's return -------------------------------------------
        gross = 0.0
        for c in codes:
            gross += w_held[c] * aligned[c][0][j]
        r_day = (1.0 + gross) * (1.0 - cost) - 1.0
        res.rets.append(r_day)

        # --- (4) drift the weights with the day's own returns ----------------
        denom = 1.0 + gross
        if denom > 0.0:
            nw = {}
            for c in codes:
                nw[c] = w_held[c] * (1.0 + aligned[c][0][j]) / denom
            w = nw
        else:
            w = dict(target)

        for c in codes:
            res.sleeve_rets.setdefault(c, []).append(aligned[c][0][j])
            res.sleeve_weights.setdefault(c, []).append(w_held[c])
            res.sleeve_values.setdefault(c, []).append(w_held[c])
            res.flips.setdefault(c, []).append(day_flips[c])

    for c in codes:
        res.sleeve_rets.setdefault(c, [0.0] * len(dates))
        res.sleeve_weights.setdefault(c, [0.0] * len(dates))
        res.sleeve_values.setdefault(c, [0.0] * len(dates))
        res.flips.setdefault(c, [False] * len(dates))
    return res


def simulate_buy_hold(dates, series, cost_bps=0.0):
    """100% long one instrument, bought at the first close.

    One side of the round trip is charged at entry; the position is never closed
    inside the window, so the exit side is not charged.
    """
    half = (cost_bps / 2.0) / 10000.0
    idx = [series.index_of[d] for d in dates]
    rets = [0.0]
    for j in range(1, len(dates)):
        rets.append(series.c[idx[j]] / series.c[idx[j - 1]] - 1.0)
    if half > 0.0:
        rets[1] -= half
    res = BookResult()
    res.dates = list(dates)
    res.rets = rets
    res.cost_bps = cost_bps
    return res


# ---------------------------------------------------------------------------
# Yearly returns
# ---------------------------------------------------------------------------

def yearly_returns(dates, rets):
    """{year: (compounded return, first date, last date, n_days)} via the engine's bucketer."""
    grouped = {}
    for d, r in zip(dates, rets):
        key, _label = TF.bucket_key("Y", d)
        grouped.setdefault(key, []).append(r)
    out = {}
    for key in sorted(grouped):
        rs = grouped[key]
        curve = 1.0
        for r in rs:
            curve *= (1.0 + r)
        ds = [d for d in dates if TF.bucket_key("Y", d)[0] == key]
        out[int(key)] = (curve - 1.0, ds[0], ds[-1], len(rs))
    return out


def complete_years(yearly, first_full_year, last_full_year):
    return [y for y in sorted(yearly) if first_full_year <= y <= last_full_year]


# ---------------------------------------------------------------------------
# Rolling windows
# ---------------------------------------------------------------------------

def rolling_return_stats(rets, lookback):
    eq = equity_curve(rets)
    vals = []
    for j in range(lookback, len(eq)):
        vals.append(eq[j] / eq[j - lookback] - 1.0)
    if not vals:
        return dict(n=0, worst=NA, best=NA, mean=NA, frac_positive=NA)
    return dict(n=len(vals), worst=min(vals), best=max(vals), mean=mean(vals),
                frac_positive=sum(1 for v in vals if v > 0) / float(len(vals)))


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def sec(title):
    print("")
    print("===== SECTION: %s =====" % title)


def sec_end():
    print("===== END SECTION =====")


def hdr(text):
    print("")
    print(text)


def emit(lines):
    for l in lines:
        print(l)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-grid", action="store_true",
                    help="skip the (slow) 1001-book optimisation comparison")
    args = ap.parse_args(argv)

    os.makedirs(OUT_DIR, exist_ok=True)
    universe = load_universe()
    sleeves = build_sleeves(universe)
    dates = book_window(sleeves, universe)

    # ---------------------------------------------------------------- S0
    sec("0 · METHOD AND PROVENANCE")
    print("  PRICE-ONLY DATA. No dividends, no distributions. Every series is a")
    print("  price series, not a total-return series. Any always-long sleeve is")
    print("  therefore understated relative to a total-return version, and the")
    print("  always-long comparison sleeve G most of all.")
    print("")
    print("  Sharpe convention: daily simple returns, full sample, Rf = 0, x sqrt(252).")
    print("  CAGR: compounded end/start, annualised over calendar time (365.25 d/yr).")
    print("  Max drawdown (headline): COMPOUNDED peak-to-trough of the equity curve,")
    print("    as a negative fraction -- the sibling regime study's definition, so the")
    print("    two studies' drawdown columns compare directly.")
    print("  Max drawdown (additive): the sibling engine's max_drawdown() on the daily")
    print("    return series -- peak-to-trough of the cumulated returns, in return units.")
    print("    Quoted for the book only, and only to show the two measures differ.")
    print("  Execution: signal on close of day i, position held through day i+1.")
    print("  Warm-up: a sleeve is FLAT until its moving average exists.")
    print("  Rebalance: monthly, to the pre-registered weights; weights drift in between.")
    print("  Costs: OFF here; on in section 11.")
    print("")
    print("  Engine imported, not re-implemented: %s"
          % os.path.join(ENGINE_DIR, "timeframe_stats.py"))
    print("    used: bucket_key(), aggregate_bucket(), sample_sd(), max_drawdown(),")
    print("          lag1_autocorr(), n_effective()")
    sec_end()

    # ---------------------------------------------------------------- S1
    sec("1 · DATA INTEGRITY")
    print("  Files under %s" % DATA_DIR)
    print("")
    rows = []
    for sym in ("SPY", "TLT", "GLD", "EEM", "VIX"):
        s = universe[sym]
        weekend = sum(1 for d in s.dates if d.isoweekday() > 5)
        rows.append([sym, len(s), s.dates[0].isoformat(), s.dates[-1].isoformat(),
                     weekend, "strictly increasing", "price-only"])
    emit(table(["symbol", "rows", "first", "last", "weekend_dates", "ordering",
                "series_type"], rows))
    print("")
    print("  No duplicate dates, no weekend dates, no OHLC-invariant violations:")
    for sym in ("SPY", "TLT", "GLD", "EEM", "VIX"):
        s = universe[sym]
        for i in range(len(s.dates)):
            if not (s.l[i] <= s.o[i] <= s.h[i] and s.l[i] <= s.c[i] <= s.h[i]):
                raise SystemExit("ERROR: OHLC invariant broken in %s at %s"
                                 % (sym, s.dates[i]))
    print("    checked all %d bars across 5 series -- all invariants hold"
          % sum(len(universe[s]) for s in universe))
    print("")
    print("  PROVENANCE HEADERS AS WRITTEN (verbatim, one series as an example):")
    for p in universe["VIX"].provenance:
        print("    # PROVENANCE: %s" % p)
    print("")
    print("  Book window = first date on which EVERY sleeve's rule is computable.")
    print("    sleeve warm-up completes on:")
    for c in SLEEVE_ORDER:
        name, sym, win = SLEEVE_DEF[c]
        print("      %s  %-8s SMA(%d) first available %s"
              % (c, sym, win, sleeves[c].first_live.isoformat()))
    print("    -> BOOK WINDOW %s .. %s   (%d trading days)"
          % (dates[0].isoformat(), dates[-1].isoformat(), len(dates)))
    sets = {sym: set(universe[sym].dates) for sym in universe}
    common = set.intersection(*sets.values())
    print("    dates present in all five series inside the window: %d of %d"
          % (sum(1 for d in dates if d in common), len(dates)))
    print("    dropped for calendar mismatch: %d" % (len(dates) - sum(
        1 for d in dates if d in common)))
    print("")
    print("  CALENDAR ALIGNMENT -- the equity instruments and the VIX index do not")
    print("  share an identical calendar (CBOE trades on Good Friday, NYSE does not):")
    for sym in ("SPY", "TLT", "GLD", "EEM", "VIX"):
        s = universe[sym]
        missing = [d for d in dates if d not in s.index_of]
        extra = [d for d in s.dates
                 if dates[0] <= d <= dates[-1] and d not in common]
        print("    %-4s %d of %d window dates have no bar of its own; %d of its own "
              "dates are outside the equity calendar"
              % (sym, len(missing), len(dates), len(extra)))
        if missing:
            raise SystemExit(
                "ERROR: %s has no bar on %d window date(s) -- forward-fill would "
                "be needed and the series is not complete: %s"
                % (sym, len(missing),
                   ",".join(d.isoformat() for d in missing[:10])))
    vix_extra = [d for d in universe["VIX"].dates
                 if dates[0] <= d <= dates[-1] and d not in common]
    print("")
    print("  VIX's %d extra dates (CBOE open, NYSE shut) are excluded from the book"
          % len(vix_extra))
    print("  calendar -- the book cannot be traded on a day the equity instruments do")
    print("  not trade. Their price move is not lost: sleeve E's return is always")
    print("  measured from its own last available bar, so the move across the gap is")
    print("  carried by the next book day. Sample of the extra dates:")
    print("    " + ", ".join(d.isoformat() for d in vix_extra[:8]) + " ...")
    sec_end()

    # ---------------------------------------------------------------- S2
    sec("2 · SLEEVE DEFINITIONS (pre-registered; not searched)")
    rows = []
    for c in SLEEVE_ORDER:
        name, sym, win = SLEEVE_DEF[c]
        w = PREREGISTERED_WEIGHTS[c]
        rows.append([c, name, sym, "close > SMA(%d)" % win, pct_unsigned(w, 0)])
    rows.append(["F", "four trend sleeves, no vol sleeve",
                 "SPY/TLT/GLD/EEM", "same rules as A-D", "25% each"])
    rows.append(["G", "buy & hold SPY (comparison)", "SPY", "always long", "100%"])
    emit(table(["id", "sleeve", "instrument", "rule", "weight"], rows))
    print("")
    print("  Sleeve E models the VIX INDEX LEVEL change, not a tradable instrument.")
    print("  No long-vol futures or ETN is modelled; roll cost is absent, so E is")
    print("  an upper bound on the signal's return and is flagged throughout.")
    sec_end()

    # ---------------------------------------------------------------- build
    aligned = {}
    for c in SLEEVE_ORDER:
        aligned[c] = sleeves[c].align(dates)

    book = simulate(dates, aligned, PREREGISTERED_WEIGHTS, 0.0)
    book_f = simulate(dates, aligned, WEIGHTS_F, 0.0)
    book_g = simulate_buy_hold(dates, universe["SPY"], 0.0)

    # per-sleeve metrics on the BOOK WINDOW (so every sleeve is comparable)
    window_rets = {}
    for c in SLEEVE_ORDER:
        window_rets[c] = aligned[c][0]
    window_rets["G"] = book_g.rets

    def days_long_of(code):
        h = aligned[code][1]
        return sum(h) / float(len(h))

    first_full_year = dates[0].year + 1
    last_full_year = dates[-1].year - 1

    # ---------------------------------------------------------------- S3
    sec("3 · PER-SLEEVE TABLE (all on the same book window, gross of costs)")
    print("  Sleeve F and portfolio rows are in section 8. Sleeve E is an upper bound")
    print("  (VIX index proxy, not tradable) -- see section 2.")
    print("")
    rows = []
    for c in SLEEVE_ORDER + ["G"]:
        h = headline(window_rets[c], dates)
        yr = yearly_returns(dates, window_rets[c])
        cy = complete_years(yr, first_full_year, last_full_year)
        worst_y = min(cy, key=lambda y: yr[y][0]) if cy else NA
        losing = [y for y in cy if yr[y][0] < 0]
        days_long = NA
        if c in SLEEVE_ORDER:
            days_long = days_long_of(c)
        rows.append([c,
                     pct(h["cagr"]),
                     pct(h["max_dd"]),
                     num(h["sharpe_daily_ann"], 3),
                     "%d (%s)" % (worst_y, pct(yr[worst_y][0])) if worst_y is not NA else "n/a",
                     len(losing),
                     pct_unsigned(days_long, 1) if days_long is not NA else "100.0%",
                     h["n_days"]])
    emit(table(["sleeve", "CAGR", "max_dd", "Sharpe", "worst_year",
                "losing_years", "days_long", "n_days"], rows))
    print("")
    print("  Sharpe convention: daily simple returns, %s .. %s, Rf = 0, x sqrt(252)."
          % (dates[0].isoformat(), dates[-1].isoformat()))
    print("  worst_year / losing_years count only COMPLETE calendar years %d-%d;"
          % (first_full_year, last_full_year))
    print("  %d and %d are partial and are shown separately in section 5."
          % (dates[0].year, dates[-1].year))
    print("")
    print("  For reference, the same two rows on their FULL available history")
    print("  (not comparable to the table above -- different window, and this is")
    print("   where the 1993-2026 coverage that the brief mentions lives):")
    print("")
    rows2 = []
    for c, sym, label in (("A", "SPY", "equity trend (SPY)"),
                          ("G", "SPY", "buy & hold SPY")):
        if c == "A":
            idx = list(range(len(sleeves["A"].dates)))
            r = sleeves["A"].ret
            d = sleeves["A"].dates
        else:
            r = [0.0] + [universe["SPY"].c[i] / universe["SPY"].c[i - 1] - 1.0
                         for i in range(1, len(universe["SPY"].c))]
            d = universe["SPY"].dates
        h = headline(r, d)
        yr = yearly_returns(d, r)
        cy = complete_years(yr, d[0].year + 1, d[-1].year - 1)
        losing = [y for y in cy if yr[y][0] < 0]
        worst_y = min(cy, key=lambda y: yr[y][0]) if cy else NA
        rows2.append([c, label, d[0].isoformat(), d[-1].isoformat(),
                      pct(h["cagr"]), pct(h["max_dd"]), num(h["sharpe_daily_ann"], 3),
                      "%d (%s)" % (worst_y, pct(yr[worst_y][0])), len(losing)])
    emit(table(["sleeve", "what", "first", "last", "CAGR", "max_dd", "Sharpe",
                "worst_year", "losing_years"], rows2))
    print("")
    print("  WHY EACH SLEEVE MAKES OR LOSES MONEY -- the return earned on the days the")
    print("  rule is long, compounded and annualised. Flat days return exactly 0.0 by")
    print("  construction, so this IS the sleeve's whole edge.")
    print("")
    print("  Compounded, not arithmetic: the arithmetic mean of daily returns is")
    print("  meaningless on a series this volatile. The VIX index rose over this")
    print("  window while its arithmetic mean daily change was NEGATIVE -- a large up")
    print("  day followed by a large down day contributes a large negative amount to an")
    print("  arithmetic mean and exactly 0 to a compounded one.")
    print("")
    rows3 = []
    for c in SLEEVE_ORDER:
        r = window_rets[c]
        h = aligned[c][1]
        lo = [r[j] for j in range(len(r)) if h[j] == 1]
        curve = 1.0
        for v in lo:
            curve *= (1.0 + v)
        ann = (curve ** (TRADING_DAYS_PER_YEAR / float(len(lo))) - 1.0) if lo else NA
        rows3.append([c, len(lo), pct_unsigned(len(lo) / float(len(r)), 1),
                      pct(curve - 1.0) if lo else "n/a",
                      pct(ann) if ann is not NA else "n/a"])
    emit(table(["sleeve", "days_long", "pct_days_long",
                "total_return_on_long_days", "annualised_on_long_days"], rows3))
    print("")
    print("  Compare the last column with section 3's CAGR. They differ because the")
    print("  sleeve's capital is rebalanced monthly against the other sleeves and")
    print("  because a book-level drawdown changes what a sleeve's own return is worth")
    print("  to the book; they are two different numbers about the same rule and both")
    print("  are printed rather than reconciled away.")
    print("")
    vixs = sleeves["E"]
    vix_idx = [vixs.index_of.get(d) for d in dates]
    first = next(i for i in vix_idx if i is not None)
    last = next(i for i in reversed(vix_idx) if i is not None)
    print("  The VIX index itself over the book window:")
    print("    first close %s on %s, last close %s on %s -> %s"
          % (num(vixs.c[first], 2), vixs.dates[first].isoformat(),
             num(vixs.c[last], 2), vixs.dates[last].isoformat(),
             pct(vixs.c[last] / vixs.c[first] - 1.0)))
    print("    the index ROSE over the window, and sleeve E still lost %s a year."
          % pct(headline(window_rets["E"], dates)["cagr"]))
    print("    The rule is long when the index is ABOVE its own 50-day average, i.e.")
    print("    it buys after the spikes -- and the VIX mean-reverts. The loss is the")
    print("    reversion, not the level.")
    sec_end()

    # ---------------------------------------------------------------- S4
    sec("4 · PER-SLEEVE YEARLY RETURNS (book window; compounded within the year)")
    yrs_all = sorted(yearly_returns(dates, window_rets["A"]).keys())
    cols = SLEEVE_ORDER + ["G"]
    rows = []
    for y in yrs_all:
        row = [y]
        for c in cols:
            yr = yearly_returns(dates, window_rets[c])
            row.append(pct(yr[y][0]))
        partial = (y == dates[0].year or y == dates[-1].year)
        row.append("partial" if partial else "")
        rows.append(row)
    emit(table(["year"] + cols + ["note"], rows))
    print("")
    print("  %d is partial (book begins %s). %d is partial (%s, the last bar)."
          % (dates[0].year, dates[0].isoformat(), dates[-1].year,
             dates[-1].isoformat()))
    print("  Complete calendar years in the window: %d-%d (%d years)."
          % (first_full_year, last_full_year, last_full_year - first_full_year + 1))
    sec_end()

    # ---------------------------------------------------------------- S5
    sec("5 · YEAR-TO-YEAR AGREEMENT BETWEEN SLEEVES (the key output)")
    print("  Pearson correlation of YEARLY returns, complete years %d-%d only."
          % (first_full_year, last_full_year))
    print("  The prior regime study found its four sleeves' six pairwise yearly")
    print("  correlations all positive, between 0.666 and 0.887. This is the same")
    print("  measurement applied to this book's sleeves.")
    print("")
    labels = ["A", "B", "C", "D", "E", "G"]
    series = {}
    for c in labels:
        yr = yearly_returns(dates, window_rets[c])
        cy = complete_years(yr, first_full_year, last_full_year)
        series[c] = ([yr[y][0] for y in cy], cy)
    n_years = len(series["A"][1])
    print("  years used (n=%d): %s" % (n_years,
                                       ",".join(str(y) for y in series["A"][1])))
    print("")
    rows = []
    for a in labels:
        row = [a]
        for b in labels:
            row.append(num(pearson_via_engine_sd(series[a][0], series[b][0]), 3))
        rows.append(row)
    emit(table([""] + labels, rows))
    print("")
    off = []
    for i, a in enumerate(labels):
        for j, b in enumerate(labels):
            if j <= i:
                continue
            rab = pearson_via_engine_sd(series[a][0], series[b][0])
            rba = pearson_via_engine_sd(series[b][0], series[a][0])
            if rab is not NA and rba is not NA and abs(rab - rba) > 1e-12:
                raise SystemExit("ERROR: correlation matrix not symmetric at %s,%s"
                                 % (a, b))
            if rab is not NA:
                off.append((a, b, rab))
    diag_ok = True
    for a in labels:
        r = pearson_via_engine_sd(series[a][0], series[a][0])
        if r is NA or abs(r - 1.0) > 1e-9:
            diag_ok = False
    print("  CHECKS: matrix symmetric: YES (all 15 off-diagonal pairs verified")
    print("          equal in both directions to 1e-12)")
    print("          unit diagonal: %s" % ("YES" if diag_ok else "NO"))
    print("")
    r_min = min(x[2] for x in off)
    r_max = max(x[2] for x in off)
    print("  pairwise yearly correlations, all 15 pairs: %.3f .. %.3f" % (r_min, r_max))
    print("")
    print("  pairs involving the vol sleeve E (the ones the book was built around):")
    for a, b, r in sorted(off, key=lambda x: x[2]):
        if a == "E" or b == "E":
            print("    corr(%s,%s) = %+.3f" % (a, b, r))
    print("")
    print("  lowest five pairs overall:")
    for a, b, r in sorted(off, key=lambda x: x[2])[:5]:
        print("    corr(%s,%s) = %+.3f" % (a, b, r))
    print("  highest five pairs overall:")
    for a, b, r in sorted(off, key=lambda x: -x[2])[:5]:
        print("    corr(%s,%s) = %+.3f" % (a, b, r))
    print("")
    in_pair = [x for x in off if x[0] in "ABCD" and x[1] in "ABCD"]
    if in_pair:
        print("  the six trend-sleeve pairs among A-D only: %.3f .. %.3f"
              % (min(x[2] for x in in_pair), max(x[2] for x in in_pair)))
    with_e = [x for x in off if (x[0] == "E") != (x[1] == "E")]
    print("  the five pairs against the vol sleeve E: %.3f .. %.3f"
          % (min(x[2] for x in with_e), max(x[2] for x in with_e)))
    sec_end()

    # ---------------------------------------------------------------- S6
    sec("6 · ENGINE CROSS-CHECK ON THE YEARLY SERIES (aggregate_bucket, bucket='Y')")
    print("  The sibling engine is fed one pseudo-trade per book day per sleeve:")
    print("  close_date = the day, pnl = that day's sleeve return. Its `net_pnl` is")
    print("  therefore the ADDITIVE sum of daily returns in the year, not the")
    print("  compounded return of section 4 -- the two agree closely in small years")
    print("  and diverge in large ones. Its t_stat tests whether the mean yearly P&L")
    print("  is distinguishable from zero across the years; its lag1/n_eff say how")
    print("  much independent information the yearly series actually carries.")
    print("")
    rows = []
    for c in SLEEVE_ORDER + ["G"]:
        trades = [{"close_date": d, "pnl": r}
                  for d, r in zip(dates, window_rets[c])]
        agg = TF.aggregate_bucket("Y", trades, 1.0)
        rows.append([c, agg["n_periods"], num(agg["mean_period_pnl"], 5),
                     num(agg["sd_period_pnl"], 5), num(agg["t_stat"], 3),
                     num(agg["lag1_autocorrelation"], 3),
                     num(agg["n_eff"], 1),
                     "yes" if (agg["t_stat"] is not NA
                               and abs(agg["t_stat"]) > TF.T_STAT_NOISE_BAND)
                     else "no"])
    emit(table(["sleeve", "n_years", "mean_yr_pnl", "sd_yr_pnl", "t_stat",
                "lag1_autocorr", "n_eff", "beyond +/-2"], rows))
    print("")
    print("  t_stat beyond the engine's own +/-%s noise band means the sleeve's"
          % num(TF.T_STAT_NOISE_BAND, 1))
    print("  yearly mean is large relative to its year-to-year scatter. n_eff below")
    print("  n_years means the yearly series is positively autocorrelated and the")
    print("  evidence is thinner than the year count suggests.")
    sec_end()

    # ---------------------------------------------------------------- S7
    sec("7 · PORTFOLIO RESULTS")
    print("  BOOK_5 = pre-registered A-E at 20% each, monthly rebalance (THE BOOK).")
    print("  F      = A-D at 25% each, no vol sleeve.")
    print("  G      = 100% buy & hold SPY on the same window.")
    print("")
    portfolios = [
        ("BOOK_5 (pre-registered)", book),
        ("F (four trend sleeves)", book_f),
        ("G (buy & hold SPY)", book_g),
    ]
    rows = []
    for label, b in portfolios:
        h = headline(b.rets, b.dates)
        yr = yearly_returns(b.dates, b.rets)
        cy = complete_years(yr, first_full_year, last_full_year)
        losing = [y for y in cy if yr[y][0] < 0]
        worst_y = min(cy, key=lambda y: yr[y][0]) if cy else NA
        r12 = rolling_return_stats(b.rets, ROLLING_LOOKBACKS["12m"])
        r36 = rolling_return_stats(b.rets, ROLLING_LOOKBACKS["36m"])
        rows.append([label, pct(h["cagr"]), pct(h["max_dd"]),
                     num(h["sharpe_daily_ann"], 3),
                     pct(r12["worst"]), pct(r36["worst"]),
                     "%d (%s)" % (worst_y, pct(yr[worst_y][0])) if worst_y is not NA else "n/a",
                     len(losing), h["n_days"]])
    emit(table(["portfolio", "CAGR", "max_dd", "Sharpe", "worst_roll_12m",
                "worst_roll_36m", "worst_year", "losing_years", "n_days"], rows))
    print("")
    print("  Rolling windows are trailing TRADING-DAY windows (252 and 756 book days),")
    print("  measured on the compounded equity curve, over every window ending on a")
    print("  book day.")
    print("")
    h5 = headline(book.rets, book.dates)
    print("  BOOK_5 additive max drawdown (engine max_drawdown() on daily returns):")
    print("    %s in return units -- compare with the compounded %s above, the two"
          % (num(h5["max_dd_additive"], 4), pct(h5["max_dd"])))
    print("    measures are different quantities and are NOT interchangeable.")
    print("")
    print("  BOOK_5 turnover: %d position flips across the five sleeves and %d monthly"
          % (book.flips_total, len(book.rebalances)))
    print("  rebalances over %.1f years -> %.1f flips/sleeve/year, one-way rebalance"
          % (h5["years"], book.flips_total / 5.0 / h5["years"]))
    print("  turnover %.2f x book value per year (sum of one-way turnover / years)."
          % (book.turnover_total / h5["years"]))
    per_sleeve = {}
    for c in SLEEVE_ORDER:
        per_sleeve[c] = sum(1 for f in book.flips[c] if f)
    print("  flips by sleeve: " + ", ".join("%s=%d" % (c, per_sleeve[c])
                                            for c in SLEEVE_ORDER))
    sec_end()

    # ---------------------------------------------------------------- S8
    sec("8 · PORTFOLIO YEARLY RETURNS, LOSING YEARS, AND WHO CAUSED THEM")
    for label, b in portfolios:
        yr = yearly_returns(b.dates, b.rets)
        print("")
        print("  %s" % label)
        rows = []
        for y in sorted(yr):
            partial = (y == b.dates[0].year or y == b.dates[-1].year)
            rows.append([y, pct(yr[y][0]), "partial" if partial else ""])
        emit(table(["year", "return", "note"], rows))
        cy = complete_years(yr, first_full_year, last_full_year)
        losing = [y for y in cy if yr[y][0] < 0]
        print("")
        print("    complete years %d-%d: %d of %d were LOSING."
              % (first_full_year, last_full_year, len(losing), len(cy)))
        if losing:
            for y in losing:
                print("      %d  %s" % (y, pct(yr[y][0])))
        else:
            print("      none")
    print("")
    print("  WHICH SLEEVES WERE NEGATIVE IN EVERY BOOK_5 YEAR, worst return first:")
    book_yr = yearly_returns(book.dates, book.rets)
    cy = complete_years(book_yr, first_full_year, last_full_year)
    ranked = sorted(cy, key=lambda y: book_yr[y][0])
    slev_yr = {c: yearly_returns(dates, window_rets[c]) for c in SLEEVE_ORDER}
    print("")
    rows = []
    for y in ranked:
        neg = [c for c in SLEEVE_ORDER if slev_yr[c][y][0] < 0]
        pos = [c for c in SLEEVE_ORDER if slev_yr[c][y][0] >= 0]
        rows.append([y, pct(book_yr[y][0]),
                     "LOSS" if book_yr[y][0] < 0 else "",
                     ",".join(neg) if neg else "-",
                     ",".join(pos) if pos else "-",
                     "  ".join("%s %s" % (c, pct(slev_yr[c][y][0]))
                               for c in SLEEVE_ORDER)])
    emit(table(["year", "BOOK_5", "", "sleeves_negative", "sleeves_positive",
                "per-sleeve return"], rows))
    print("")
    all_neg = [y for y in ranked
               if all(slev_yr[c][y][0] < 0 for c in SLEEVE_ORDER)]
    print("  years in which ALL FIVE sleeves lost: %s"
          % (", ".join(str(y) for y in sorted(all_neg)) if all_neg else "none"))
    e_neg = [y for y in ranked if slev_yr["E"][y][0] < 0]
    losing_years = [y for y in ranked if book_yr[y][0] < 0]
    print("  years in which sleeve E lost            : %d of %d complete years"
          % (len(e_neg), len(ranked)))
    print("  BOOK_5 losing years in which E lost     : %d of %d"
          % (sum(1 for y in losing_years if slev_yr["E"][y][0] < 0),
             len(losing_years)))
    print("  BOOK_5 losing years in which E did not lose: %s"
          % (", ".join(str(y) for y in losing_years
                       if slev_yr["E"][y][0] >= 0) or "none"))
    sec_end()

    # ---------------------------------------------------------------- S9
    sec("9 · ALL-WEATHER VERDICT -- THE CLOSEST STANDARD THE DATA SUPPORTS")
    print("  Question 1: is the book profitable in EVERY year?")
    book_yr = yearly_returns(book.dates, book.rets)
    cy = complete_years(book_yr, first_full_year, last_full_year)
    losing = [y for y in cy if book_yr[y][0] < 0]
    print("    Complete calendar years tested: %d (%d-%d)."
          % (len(cy), first_full_year, last_full_year))
    if losing:
        print("    Losing years: %d -> %s"
              % (len(losing), ", ".join("%d %s" % (y, pct(book_yr[y][0]))
                                        for y in losing)))
        print("    ANSWER: NO. The book is not profitable in every year.")
    else:
        print("    Losing years: none.")
        print("    ANSWER: YES on this window -- with the caveat that a %d-year"
              % len(cy))
        print("    window contains only a handful of independent episodes (section 6).")
    print("")
    print("  Question 2: what IS the closest standard the data supports? Every")
    print("  rolling N-year window on the compounded equity curve:")
    print("")
    rows = []
    for label, n_years in ALL_WEATHER_HORIZONS:
        lb = n_years * TRADING_DAYS_PER_YEAR
        st = rolling_return_stats(book.rets, lb)
        if st["n"] == 0:
            rows.append([label, "n/a", "n/a", "n/a", "n/a"])
            continue
        rows.append([label, st["n"], pct(st["worst"]), pct(st["mean"]),
                     "%.1f%%" % (st["frac_positive"] * 100.0)])
    emit(table(["window", "windows_tested", "worst_window", "mean_window",
                "windows_positive"], rows))
    print("")
    h5 = headline(book.rets, book.dates)
    print("  Same for the comparison portfolios:")
    print("")
    rows = []
    for label, b in portfolios:
        r = []
        for lbl, n_years in ALL_WEATHER_HORIZONS:
            st = rolling_return_stats(b.rets, n_years * TRADING_DAYS_PER_YEAR)
            r.append(pct(st["worst"]) if st["n"] else "n/a")
        rows.append([label] + r)
    emit(table(["portfolio"] + [h[0] for h in ALL_WEATHER_HORIZONS], rows))
    print("")
    print("  Fraction of rolling windows with a POSITIVE return (BOOK_5):")
    print("")
    rows = []
    for lbl, n_years in ALL_WEATHER_HORIZONS:
        st = rolling_return_stats(book.rets, n_years * TRADING_DAYS_PER_YEAR)
        rows.append([lbl, "%.2f%%" % (st["frac_positive"] * 100.0)
                     if st["n"] else "n/a"])
    emit(table(["window", "windows_positive"], rows))
    print("")
    print("  Worst drawdown of BOOK_5 over the whole window: %s" % pct(h5["max_dd"]))
    print("  Worst drawdown of G (buy & hold SPY):          %s"
          % pct(headline(book_g.rets, book_g.dates)["max_dd"]))
    sec_end()

    # ---------------------------------------------------------------- S10
    sec("10 · COSTS")
    print("  Round-trip rate c bps means each side of a trade costs c/2 bps of the")
    print("  notional traded. Charged on: every position flip (flat<->long), and every")
    print("  monthly rebalance on its one-way turnover. Sleeve E's flips are charged")
    print("  like any other sleeve even though E is not tradable -- see section 2.")
    print("")
    rows = []
    baseline = {}
    for c_bps in (0.0, 5.0, 20.0):
        b = simulate(dates, aligned, PREREGISTERED_WEIGHTS, c_bps)
        h = headline(b.rets, b.dates)
        yr = yearly_returns(b.dates, b.rets)
        cy = complete_years(yr, first_full_year, last_full_year)
        losing = [y for y in cy if yr[y][0] < 0]
        if c_bps == 0.0:
            baseline["cagr"] = h["cagr"]
            baseline["dd"] = h["max_dd"]
            baseline["sharpe"] = h["sharpe_daily_ann"]
        rows.append([num(c_bps, 1), pct(h["cagr"]), pct(h["max_dd"]),
                     num(h["sharpe_daily_ann"], 3),
                     "%+.2fbp" % ((h["cagr"] - baseline["cagr"]) * 10000.0),
                     "%+.2fbp" % ((h["max_dd"] - baseline["dd"]) * 10000.0),
                     num(h["sharpe_daily_ann"] - baseline["sharpe"], 4),
                     len(losing)])
    emit(table(["round_trip_bps", "CAGR", "max_dd", "Sharpe", "CAGR_drag",
                "maxdd_change", "Sharpe_delta", "losing_years"], rows))
    print("")
    print("  The same for the comparison portfolios at 20 bps:")
    print("")
    rows = []
    for label, w, bh in (("BOOK_5", PREREGISTERED_WEIGHTS, None),
                         ("F", WEIGHTS_F, None)):
        b0 = simulate(dates, aligned, w, 0.0)
        b1 = simulate(dates, aligned, w, 20.0)
        h0 = headline(b0.rets, b0.dates)
        h1 = headline(b1.rets, b1.dates)
        rows.append([label, pct(h0["cagr"]), pct(h1["cagr"]),
                     "%+.2fbp" % ((h1["cagr"] - h0["cagr"]) * 10000.0),
                     pct(h0["max_dd"]), pct(h1["max_dd"])])
    b0 = simulate_buy_hold(dates, universe["SPY"], 0.0)
    b1 = simulate_buy_hold(dates, universe["SPY"], 20.0)
    h0 = headline(b0.rets, b0.dates)
    h1 = headline(b1.rets, b1.dates)
    rows.append(["G (SPY buy&hold, one entry)",
                 pct(h0["cagr"]), pct(h1["cagr"]),
                 "%+.2fbp" % ((h1["cagr"] - h0["cagr"]) * 10000.0),
                 pct(h0["max_dd"]), pct(h1["max_dd"])])
    emit(table(["portfolio", "CAGR@0bps", "CAGR@20bps", "CAGR_drag",
                "max_dd@0bps", "max_dd@20bps"], rows))
    print("")
    print("  Neither sibling study charged any cost. Section 12's optimisation grid")
    print("  is run GROSS, like both sibling studies.")
    sec_end()

    # ---------------------------------------------------------------- S11
    sec("11 · PRE-REGISTRATION COMPARISON -- fixed weights vs fitted weights")
    print("  PART 1 is the pre-registered book. PART 2 is a separate, clearly labelled")
    print("  fitted exercise shown ONLY so the difference between a designed book and")
    print("  a fitted one is visible. The fitted weights are NOT the recommendation and")
    print("  are not used anywhere else in this study.")
    print("")
    print("  PART 1 -- PRE-REGISTERED, FIXED AT 20% EACH (no search of any kind)")
    print("")
    h = headline(book.rets, book.dates)
    yr = yearly_returns(book.dates, book.rets)
    cy = complete_years(yr, first_full_year, last_full_year)
    losing = [y for y in cy if yr[y][0] < 0]
    rows = [["BOOK_5", "20/20/20/20/20", pct(h["cagr"]), pct(h["max_dd"]),
             num(h["sharpe_daily_ann"], 3), len(losing)]]
    emit(table(["book", "weights (%)", "CAGR", "max_dd", "Sharpe", "losing_years"],
               rows))
    print("")
    grid = []
    for a in range(11):
        for b in range(11 - a):
            for c in range(11 - a - b):
                for d in range(11 - a - b - c):
                    e = 10 - a - b - c - d
                    grid.append({"A": a / 10.0, "B": b / 10.0, "C": c / 10.0,
                                 "D": d / 10.0, "E": e / 10.0})

    print("  PART 2 -- FITTED ON THE FIRST %d%% OF THE WINDOW (%d%% weight steps,"
          % (int(IS_FRACTION * 100), int(GRID_STEP * 100)))
    print("  every 5-vector summing to 100%; objective = in-sample Sharpe, gross")
    print("  of costs). %d books are evaluated. The last %d%% of the window is"
          % (len(grid), int((1.0 - IS_FRACTION) * 100)))
    print("  held out. A zero weight simply drops that sleeve for that book.")
    print("")

    if args.no_grid:
        print("  (grid skipped by --no-grid)")
    else:
        n_days = len(dates)
        split = int(n_days * IS_FRACTION)
        is_dates = dates[:split]
        oos_dates = dates[split:]
        print("  in-sample  %s .. %s  (%d days)"
              % (is_dates[0].isoformat(), is_dates[-1].isoformat(), len(is_dates)))
        print("  out-sample %s .. %s  (%d days)"
              % (oos_dates[0].isoformat(), oos_dates[-1].isoformat(), len(oos_dates)))
        print("")

        is_aligned = {c: tuple(a[:split] for a in aligned[c])
                      for c in SLEEVE_ORDER}
        oos_aligned = {c: tuple(a[split:] for a in aligned[c])
                       for c in SLEEVE_ORDER}

        def run(w, dts, al):
            b = simulate(dts, al, w, 0.0)
            return headline(b.rets, b.dates), b

        rows_is = []
        for w in grid:
            hh, _b = run(w, is_dates, is_aligned)
            rows_is.append((w, hh))
        ew_is, _ew_book_is = run(PREREGISTERED_WEIGHTS, is_dates, is_aligned)
        ew_oos, _ew_book_oos = run(PREREGISTERED_WEIGHTS, oos_dates, oos_aligned)

        by_sharpe = sorted(
            rows_is,
            key=lambda t: (t[1]["sharpe_daily_ann"]
                           if t[1]["sharpe_daily_ann"] is not NA else -9e9),
            reverse=True)
        best_w, best_is = by_sharpe[0]
        best_oos, _ = run(best_w, oos_dates, oos_aligned)

        sharpes = [t[1]["sharpe_daily_ann"] for t in rows_is
                   if t[1]["sharpe_daily_ann"] is not NA]
        med_sharpe = sorted(sharpes)[len(sharpes) // 2]
        median_vec = None
        median_is = None
        for w, hh in rows_is:
            if (hh["sharpe_daily_ann"] is not NA
                    and abs(hh["sharpe_daily_ann"] - med_sharpe) < 1e-12):
                median_vec, median_is = w, hh
                break
        med_oos, _ = run(median_vec, oos_dates, oos_aligned)

        print("  In-sample Sharpe across the %d books: best %s, median %s, worst %s"
              % (len(grid), num(max(sharpes), 3), num(med_sharpe, 3),
                 num(min(sharpes), 3)))
        print("  In-sample Sharpe of the PRE-REGISTERED equal-weight book: %s"
              % num(ew_is["sharpe_daily_ann"], 3))
        rank = 1 + sum(1 for t in rows_is
                       if t[1]["sharpe_daily_ann"] is not NA
                       and t[1]["sharpe_daily_ann"] > ew_is["sharpe_daily_ann"])
        print("  In-sample Sharpe rank of the pre-registered book: %d of %d"
              % (rank, len(grid)))
        beat_is = [t for t in rows_is
                   if t[1]["sharpe_daily_ann"] is not NA
                   and t[1]["sharpe_daily_ann"] > ew_is["sharpe_daily_ann"]]
        print("  books that beat equal weight IN SAMPLE: %d of %d (%.0f%%)"
              % (len(beat_is), len(grid), 100.0 * len(beat_is) / len(grid)))
        print("")

        print("  The in-sample-optimal weight vector, and how it did out of sample,")
        print("  beside the pre-registered book measured the same way:")
        print("")
        rows = []

        def row_for(label, w, his, oos):
            wv = "/".join("%d" % int(round(w.get(c, 0.0) * 100))
                          for c in SLEEVE_ORDER)
            return [label, wv, pct(his["cagr"]), pct(his["max_dd"]),
                    num(his["sharpe_daily_ann"], 3),
                    pct(oos["cagr"]), pct(oos["max_dd"]),
                    num(oos["sharpe_daily_ann"], 3),
                    num(his["sharpe_daily_ann"] - oos["sharpe_daily_ann"], 3)]

        rows.append(row_for("FITTED BEST (IS-optimal)", best_w, best_is, best_oos))
        rows.append(row_for("PRE-REGISTERED equal weight", PREREGISTERED_WEIGHTS,
                            ew_is, ew_oos))
        f_is, _ = run(WEIGHTS_F, is_dates, is_aligned)
        f_oos, _ = run(WEIGHTS_F, oos_dates, oos_aligned)
        rows.append(row_for("pre-registered F (no vol sleeve)", WEIGHTS_F,
                            f_is, f_oos))
        if median_vec is not None:
            rows.append(row_for("median-IS-Sharpe book", median_vec, median_is,
                                med_oos))
        emit(table(["book", "weights A/B/C/D/E", "IS CAGR", "IS max_dd",
                    "IS Sharpe", "OOS CAGR", "OOS max_dd", "OOS Sharpe",
                    "Sharpe decay"], rows))
        print("")
        print("  'Sharpe decay' = IS Sharpe minus OOS Sharpe. A large decay would be")
        print("  the signature of a fitted book whose in-sample number was luck. NOTE")
        print("  WHAT ACTUALLY HAPPENED HERE: the fitted best did NOT decay. Its Sharpe")
        print("  went UP out of sample. The decay is negative. That is reported as it")
        print("  is, and the reason is diagnosed immediately below rather than dressed")
        print("  up as a validation of fitting.")
        print("")
        zero_e = [t for t in rows_is if t[0]["E"] == 0.0]
        pos_e = [t for t in rows_is if t[0]["E"] > 0.0]
        zs = [t[1]["sharpe_daily_ann"] for t in zero_e
              if t[1]["sharpe_daily_ann"] is not NA]
        ps = [t[1]["sharpe_daily_ann"] for t in pos_e
              if t[1]["sharpe_daily_ann"] is not NA]
        print("  DIAGNOSIS -- how much of the fitted result is just 'get out of E'?")
        print("")
        print("    books with E = 0  : %d,  mean in-sample Sharpe %s"
              % (len(zero_e), num(mean(zs), 3)))
        print("    books with E > 0  : %d,  mean in-sample Sharpe %s"
              % (len(pos_e), num(mean(ps), 3)))
        print("    every one of the top 10 has E = 0 : %s"
              % ("yes" if all(t[0]["E"] == 0.0 for t in by_sharpe[:10])
                 else "no"))
        print("    every one of the top 10 has D = 0 : %s"
              % ("yes" if all(t[0]["D"] == 0.0 for t in by_sharpe[:10])
                 else "no"))
        print("    the best book that still HOLDS E:")
        first_e = next((t for t in by_sharpe if t[0]["E"] > 0.0), None)
        if first_e is not None:
            oo, _ = run(first_e[0], oos_dates, oos_aligned)
            print("      %s  IS Sharpe %s  OOS Sharpe %s"
                  % ("/".join("%d" % int(round(first_e[0][c] * 100))
                              for c in SLEEVE_ORDER),
                     num(first_e[1]["sharpe_daily_ann"], 3),
                     num(oo["sharpe_daily_ann"], 3)))
        print("")
        print("  The fitted optimum is not a subtle reweighting: it is 'drop the")
        print("  volatility sleeve and the ex-US sleeve'. The vol sleeve's negative")
        print("  edge is STRUCTURAL (a rule that buys VIX after its spikes on a series")
        print("  that mean-reverts), not sampling noise, which is why removing it")
        print("  helps out of sample instead of hurting. Choosing to remove it in")
        print("  advance required knowing that -- which is exactly the hindsight this")
        print("  study refuses to sell as a result. It is shown here so the owner can")
        print("  see the difference, and it is NOT the recommendation.")
        print("")
        print("  Top 10 weight vectors by IN-SAMPLE Sharpe, with their OUT-OF-SAMPLE")
        print("  numbers beside them:")
        print("")
        rows = []
        for w, hh in by_sharpe[:10]:
            oo, _ = run(w, oos_dates, oos_aligned)
            wv = "/".join("%d" % int(round(w[c] * 100)) for c in SLEEVE_ORDER)
            rows.append([wv, num(hh["sharpe_daily_ann"], 3), pct(hh["cagr"]),
                         num(oo["sharpe_daily_ann"], 3), pct(oo["cagr"]),
                         pct(oo["max_dd"]),
                         num(hh["sharpe_daily_ann"] - oo["sharpe_daily_ann"], 3)])
        emit(table(["weights A/B/C/D/E", "IS Sharpe", "IS CAGR", "OOS Sharpe",
                    "OOS CAGR", "OOS max_dd", "Sharpe decay"], rows))
        print("")
        beat_oos = 0
        for t in beat_is:
            oo, _ = run(t[0], oos_dates, oos_aligned)
            if oo["sharpe_daily_ann"] is not NA and ew_oos["sharpe_daily_ann"] is not NA \
                    and oo["sharpe_daily_ann"] > ew_oos["sharpe_daily_ann"]:
                beat_oos += 1
        print("  Of the %d books that beat equal weight IN SAMPLE, %d (%.0f%%) also"
              % (len(beat_is), beat_oos, 100.0 * beat_oos / max(1, len(beat_is))))
        print("  beat it OUT OF SAMPLE. A coin would give about half.")

        with open(os.path.join(OUT_DIR, "optimised_weights.csv"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write("# PROVENANCE: generated by study.py section 11; fitted, NOT "
                     "the recommendation\n")
            fh.write("# PROVENANCE: objective = in-sample Sharpe, grid 10%% steps, "
                     "gross of costs\n")
            fh.write("# PROVENANCE: in-sample %s..%s  out-of-sample %s..%s\n"
                     % (is_dates[0], is_dates[-1], oos_dates[0], oos_dates[-1]))
            fh.write("wA,wB,wC,wD,wE,is_cagr,is_max_dd,is_sharpe,oos_cagr,"
                     "oos_max_dd,oos_sharpe\n")
            for w, hh in by_sharpe:
                oo, _ = run(w, oos_dates, oos_aligned)
                fh.write("%d,%d,%d,%d,%d,%.6f,%.6f,%s,%.6f,%.6f,%s\n"
                         % (int(round(w["A"] * 100)), int(round(w["B"] * 100)),
                            int(round(w["C"] * 100)), int(round(w["D"] * 100)),
                            int(round(w["E"] * 100)), hh["cagr"], hh["max_dd"],
                            ("%.6f" % hh["sharpe_daily_ann"])
                            if hh["sharpe_daily_ann"] is not NA else "",
                            oo["cagr"], oo["max_dd"],
                            ("%.6f" % oo["sharpe_daily_ann"])
                            if oo["sharpe_daily_ann"] is not NA else ""))
        print("")
        print("  full grid written to out/optimised_weights.csv")
    sec_end()

    # ---------------------------------------------------------------- S12
    sec("12 · WHAT WAS NOT DONE, AND WHAT REMAINS UNTESTED")
    print("  Stated as limitations, not as caveats to be skipped.")
    print("")
    print("  1. SLEEVE E IS NOT TRADABLE. The VIX index cannot be bought. Its return")
    print("     here is the index level change while the rule is long; a real long-vol")
    print("     position is a VIX futures or futures-ETN position, which bleeds on roll")
    print("     in contango. No roll cost, no ETN fee, no borrow is modelled. Every E")
    print("     number is an UPPER BOUND on the signal and is not an achievable return.")
    print("     Drop E and the book is portfolio F, whose row is above.")
    print("  2. PRICE-ONLY. No dividends or distributions anywhere. TLT's price")
    print("     multiple over 2002-2026 is 0.9561 in the sibling study, i.e. TLT's")
    print("     price is BELOW its start -- so sleeve B's always-long component, and")
    print("     the bond leg generally, is understated versus a total-return version.")
    print("     SPY/GLD/EEM pay distributions too. Buy & hold G is understated most.")
    print("  3. LONG ONLY, NO LEVERAGE, NO SHORTS. The book cannot short a downtrend;")
    print("     it can only stand aside. That is a design choice, not a finding.")
    print("  4. ONE PARAMETER SET. SMA(200) for A-D and SMA(50) for E were fixed")
    print("     before the run. This study does NOT establish that 200 beats 150, nor")
    print("     that 50 beats 20, and does not rule either out. Parameter sensitivity")
    print("     is untested.")
    print("  5. FIVE SLEEVES, ALL TREND-SHAPED except E. A-D are the same rule on four")
    print("     different instruments. Section 5 measures how much that actually")
    print("     diversifies; it is the honest answer to 'is this four bets or one'.")
    print("  6. ONE WINDOW. The book needs all five series, so it starts when gold's")
    print("     SMA(200) exists. It therefore does not cover 1993-2004 at all. Sleeve A")
    print("     and G are also shown on full history for that reason. The window is")
    print("     dominated by the post-2009 bull market, which flatters every long-only")
    print("     sleeve and the always-long comparison most.")
    print("  7. NO REGIME TEST here. The sibling regime study did that; this study only")
    print("     reports years and drawdowns.")
    print("  8. THE LAST BAR WAS STILL FORMING at pull time and may revise.")
    sec_end()

    # ---------------------------------------------------------------- artefacts
    write_artefacts(dates, sleeves, aligned, window_rets, book, book_f, book_g,
                    first_full_year, last_full_year)
    print("")
    print("ARTEFACTS WRITTEN to out/: sleeve_headline.csv, sleeve_yearly.csv,")
    print("corr_matrix.csv, portfolio_headline.csv, portfolio_yearly.csv,")
    print("rolling_windows.csv, costs.csv, book_daily.csv, sleeve_monthly.csv")
    return 0


def write_artefacts(dates, sleeves, aligned, window_rets, book, book_f, book_g,
                    first_full_year, last_full_year):
    os.makedirs(OUT_DIR, exist_ok=True)

    def w(path, header_lines, rows):
        with open(os.path.join(OUT_DIR, path), "w", encoding="utf-8",
                  newline="\n") as fh:
            for l in header_lines:
                fh.write("# PROVENANCE: %s\n" % l)
            fh.write("\n".join(rows) + "\n")

    prov = ["generated by study.py from data/*.csv",
            "book window %s..%s" % (dates[0].isoformat(), dates[-1].isoformat()),
            "price-only data, gross of costs unless stated"]

    # sleeve headline
    rows = ["sleeve,cagr,max_dd,sharpe_daily_ann,worst_year,worst_year_return,"
            "losing_years,n_days,days_long"]
    for c in SLEEVE_ORDER + ["G"]:
        h = headline(window_rets[c], dates)
        yr = yearly_returns(dates, window_rets[c])
        cy = complete_years(yr, first_full_year, last_full_year)
        losing = [y for y in cy if yr[y][0] < 0]
        wy = min(cy, key=lambda y: yr[y][0]) if cy else ""
        dl = ""
        if c in SLEEVE_ORDER:
            hh = aligned[c][1]
            dl = "%.4f" % (sum(hh) / float(len(hh)))
        else:
            dl = "1.0000"
        rows.append("%s,%.6f,%.6f,%s,%s,%s,%d,%d,%s"
                    % (c, h["cagr"], h["max_dd"],
                       ("%.6f" % h["sharpe_daily_ann"])
                       if h["sharpe_daily_ann"] is not NA else "",
                       wy, ("%.6f" % yr[wy][0]) if wy != "" else "",
                       len(losing), h["n_days"], dl))
    w("sleeve_headline.csv", prov, rows)

    # sleeve yearly
    rows = ["sleeve,year,return,partial,first,last,n_days"]
    labels = SLEEVE_ORDER + ["G"]
    for c in labels:
        yr = yearly_returns(dates, window_rets[c])
        for y in sorted(yr):
            r, first, last, n = yr[y]
            rows.append("%s,%d,%.6f,%s,%s,%s,%d"
                        % (c, y, r,
                           "yes" if (y == dates[0].year or y == dates[-1].year)
                           else "no", first.isoformat(), last.isoformat(), n))
    w("sleeve_yearly.csv", prov, rows)

    # correlation matrix
    series = {}
    for c in labels:
        yr = yearly_returns(dates, window_rets[c])
        cy = complete_years(yr, first_full_year, last_full_year)
        series[c] = [yr[y][0] for y in cy]
    rows = ["sleeve," + ",".join(labels)]
    for a in labels:
        cells = []
        for b in labels:
            r = pearson_via_engine_sd(series[a], series[b])
            cells.append("%.6f" % r if r is not NA else "")
        rows.append(a + "," + ",".join(cells))
    w("corr_matrix.csv", prov + ["Pearson correlation of yearly returns, complete "
                                 "years %d..%d only" % (first_full_year,
                                                        last_full_year)], rows)

    # portfolio headline
    rows = ["portfolio,cagr,max_dd,max_dd_additive,sharpe_daily_ann,"
            "worst_year,worst_year_return,losing_years,worst_roll_12m,"
            "worst_roll_36m,n_days"]
    for label, b in (("BOOK_5", book), ("F", book_f), ("G", book_g)):
        h = headline(b.rets, b.dates)
        yr = yearly_returns(b.dates, b.rets)
        cy = complete_years(yr, first_full_year, last_full_year)
        losing = [y for y in cy if yr[y][0] < 0]
        wy = min(cy, key=lambda y: yr[y][0]) if cy else ""
        r12 = rolling_return_stats(b.rets, ROLLING_LOOKBACKS["12m"])
        r36 = rolling_return_stats(b.rets, ROLLING_LOOKBACKS["36m"])
        rows.append("%s,%.6f,%.6f,%.6f,%s,%s,%s,%d,%.6f,%.6f,%d"
                    % (label, h["cagr"], h["max_dd"], h["max_dd_additive"],
                       ("%.6f" % h["sharpe_daily_ann"])
                       if h["sharpe_daily_ann"] is not NA else "",
                       wy, ("%.6f" % yr[wy][0]) if wy != "" else "",
                       len(losing), r12["worst"], r36["worst"], h["n_days"]))
    w("portfolio_headline.csv", prov, rows)

    # portfolio yearly
    rows = ["portfolio,year,return,partial"]
    for label, b in (("BOOK_5", book), ("F", book_f), ("G", book_g)):
        yr = yearly_returns(b.dates, b.rets)
        for y in sorted(yr):
            rows.append("%s,%d,%.6f,%s"
                        % (label, y, yr[y][0],
                           "yes" if (y == b.dates[0].year
                                     or y == b.dates[-1].year) else "no"))
    w("portfolio_yearly.csv", prov, rows)

    # rolling windows
    rows = ["portfolio,window,windows_tested,worst,mean,best,frac_positive"]
    for label, b in (("BOOK_5", book), ("F", book_f), ("G", book_g)):
        for lbl, n_years in ALL_WEATHER_HORIZONS:
            st = rolling_return_stats(b.rets, n_years * TRADING_DAYS_PER_YEAR)
            if st["n"] == 0:
                continue
            rows.append("%s,%s,%d,%.6f,%.6f,%.6f,%.4f"
                        % (label, lbl, st["n"], st["worst"], st["mean"],
                           st["best"], st["frac_positive"]))
    w("rolling_windows.csv", prov + ["trailing TRADING-DAY windows on the "
                                     "compounded equity curve"], rows)

    # costs
    rows = ["portfolio,round_trip_bps,cagr,max_dd,sharpe_daily_ann"]
    for label, wv in (("BOOK_5", PREREGISTERED_WEIGHTS), ("F", WEIGHTS_F)):
        for c_bps in (0.0, 5.0, 20.0):
            b = simulate(dates, aligned, wv, c_bps)
            h = headline(b.rets, b.dates)
            rows.append("%s,%.1f,%.6f,%.6f,%s"
                        % (label, c_bps, h["cagr"], h["max_dd"],
                           ("%.6f" % h["sharpe_daily_ann"])
                           if h["sharpe_daily_ann"] is not NA else ""))
    w("costs.csv", prov + ["flip costs charged per side; rebalance turnover charged "
                           "per one-way turn"], rows)

    # book daily (evidence for the hand-check and the rolling windows)
    rows = ["date,book_return,book_equity,book_total_equity,"
            + ",".join("w%s" % c for c in SLEEVE_ORDER)
            + "," + ",".join("r%s" % c for c in SLEEVE_ORDER)
            + "," + ",".join("f%s" % c for c in SLEEVE_ORDER)]
    eq = 1.0
    for j, d in enumerate(book.dates):
        eq *= (1.0 + book.rets[j])
        rows.append("%s,%.10f,%.10f,%.10f,%s,%s,%s"
                    % (d.isoformat(), book.rets[j], eq, eq,
                       ",".join("%.8f" % book.sleeve_weights[c][j]
                                for c in SLEEVE_ORDER),
                       ",".join("%.10f" % book.sleeve_rets[c][j]
                                for c in SLEEVE_ORDER),
                       ",".join("1" if book.flips[c][j] else "0"
                                for c in SLEEVE_ORDER)))
    w("book_daily.csv", prov + ["book_equity is the compounded book; "
                                "book_total_equity is the same number",
                                "w/r/f are the held weight, the sleeve's own "
                                "return and the flip flag on that day"], rows)

    # sleeve monthly returns (input to the hand-check)
    rows = ["sleeve,month,return,n_days"]
    for c in SLEEVE_ORDER:
        grouped = {}
        for d, r in zip(dates, aligned[c][0]):
            key, _ = TF.bucket_key("M", d)
            grouped.setdefault(key, []).append(r)
        for key in sorted(grouped):
            curve = 1.0
            for r in grouped[key]:
                curve *= (1.0 + r)
            rows.append("%s,%s,%.10f,%d" % (c, key, curve - 1.0,
                                            len(grouped[key])))
    w("sleeve_monthly.csv", prov + ["compounded within each calendar month; "
                                    "input to handcheck.py"], rows)


if __name__ == "__main__":
    sys.exit(main())
