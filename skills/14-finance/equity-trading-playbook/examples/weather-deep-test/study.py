#!/usr/bin/env python3
"""
study.py -- weather-deep-test: the widest realistic cross-asset universe, one
pre-registered run.

WHAT THIS ANSWERS
    P(positive period) ~= Phi(annual_Sharpe * sqrt(period_fraction)).  So the
    ONLY honest way to buy positivity is to buy Sharpe, and Sharpe is bought
    with sleeves that are genuinely uncorrelated.  This study pre-registers a
    six-sleeve book over a 31-instrument cross-asset universe, runs it once, and
    reports what the measured positivity frontier actually is.

DISCIPLINE (non-negotiable, stated before anything is computed)
    * The universe, the sleeves and the weights are declared in PREREG below and
      printed before any result.  They were fixed before the first run.
    * NO sleeve was screened on performance.  The only screen is EXISTENCE: a
      series is in the universe iff the data source resolves it and it has
      prints over the window.  Which symbols resolved and which failed is
      recorded in RESULTS.md and in logs/pull-output.txt.
    * Nothing was iterated toward a positive number.  Every losing year, every
      negative regime cell, the worst drawdown and the cost drag are reported.
    * Stdlib only.  Deterministic.  LF output.  No network.

WHAT IS MEASURED vs WHAT IS MODELLED
    MEASURED   price and (estimated) dividend returns of 31 listed instruments.
    MODELLED   every option position: V (short 30-DTE 16-delta SPY put spread),
               H-b (always-on long 60-DTE 5%-OTM SPY put overlay), and BOND10M
               (a duration-approximated long-Treasury total return used only in
               the reduced long-window book).  Every such number carries the
               literal tag [MODELED] in its table header and in the CSVs.

ENGINE REUSE
    The statistics helpers `bucket_key`, `sample_sd`, `max_drawdown`,
    `lag1_autocorr`, `n_effective` and `aggregate_bucket` are IMPORTED from the
    sibling engine
        ../../../timeframe-performance-statistics/scripts/timeframe_stats.py
    rather than re-implemented.  If it is missing this study refuses to run.

USAGE
    set PYTHONIOENCODING=utf-8
    py -3 study.py
"""

import datetime
import math
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
OUT_DIR = os.path.join(HERE, "out")
ENGINE_DIR = os.path.normpath(os.path.join(
    HERE, "..", "..", "..", "timeframe-performance-statistics", "scripts"))


# ===========================================================================
# PRE-REGISTRATION.  Everything in this block was fixed before the first run.
# ===========================================================================

TRADING_DAYS_PER_YEAR = 252

WINDOW_START = datetime.date(2005, 9, 30)   # primary books
REDUCED_START = datetime.date(1998, 12, 22)  # reduced long-window book

# --- T - the trend programme ------------------------------------------------
SMA_TREND = 200          # long when close > SMA(200) on the rebalance close
VOL_WINDOW = 60          # trailing window for the inverse-vol weight

TREND_UNIVERSE = [
    "SPY", "QQQ", "IWM", "MDY", "DIA",                      # equity beta
    "TLT", "TLH", "EDV", "IEF", "SHY", "TIP", "LQD", "HYG", "EMB",  # duration
    "GLD", "SLV", "GDX", "DBC",                             # real assets
    "VNQ",                                                  # property
    "EEM", "EFA", "EWJ", "FXI", "ILF", "EWZ",               # intl equity
    "UUP",                                                  # dollar
    "XLE", "XLU", "XLK", "XLP", "XLV",                      # sectors
]

# --- C - carry / credit -----------------------------------------------------
CARRY_LONG = "HYG"
CARRY_SHORT = "IEF"

# --- V - variance risk premium, MODELLED -----------------------------------
VRP_DELTA = 0.16         # |put delta| of the short strike
VRP_SPREAD_PCT = 0.05    # long strike 5% below the short strike
VRP_DTE = 30             # days to expiry
VRP_VIX_LAG = 3          # trading days of lag applied to VIX before pricing
VRP_SKEW_SHORT = 1.5     # vol points added to ATM vol for the SHORT strike
VRP_SKEW_LONG = 3.0      # vol points added to ATM vol for the LONG strike
VRP_SKEW_SENSITIVITIES = [0.0, 1.5, 3.0]   # 1.5 is the BASE case

# --- H - crisis hedge ------------------------------------------------------
HEDGE_RULE_INSTRUMENTS = ["GLD", "UUP"]
HEDGE_VIX_SMA = 50
HEDGE_PUT_DTE = 60
HEDGE_PUT_OTM = 0.05
HEDGE_PUT_BUDGET_PCT_PER_YEAR = 0.05   # premium budget, spent at 1/12 a month
HEDGE_BLEND = 0.5        # H = 0.5*H_a + 0.5*H_b, fixed

# --- X - cross-sectional momentum ------------------------------------------
XSEC_N = 5
XSEC_LOOKBACK_DAYS = 126   # ~6 months
XSEC_N_SENSITIVITY = 8

# --- B - baseline ----------------------------------------------------------
BASELINE = "SPY"

# --- the books: FIXED weights, declared, never searched --------------------
BOOK_WEIGHTS = {"T": 0.40, "X": 0.15, "C": 0.15, "V": 0.10, "H": 0.10,
                "CASH": 0.10}
BOOK_NOV_WEIGHTS = {"T": 0.45, "X": 0.17, "C": 0.17, "H": 0.11, "CASH": 0.10}
REDUCED_BOOK_WEIGHTS = {"T": 0.40, "X": 0.15, "C": 0.00, "V": 0.10, "H": 0.10,
                        "BOND10M": 0.15, "CASH": 0.10}

# A UNIFORM, DECLARED reporting normalisation -- NOT a search.  It exists
# because the sleeves are NOT naturally comparable in risk (the trend sleeve
# runs at ~4% annualised vol, the [MODELED] variance-risk-premium sleeve at
# ~80%), and a fixed-weight sum of incomparable risks is unreadable.  The rule
# is applied to EVERY sleeve identically, never by inspection of a result:
#   k_s = min(1, VOL_TARGET / annualised_vol_s);  w_s -> w_s * k_s; the released
#   weight goes to CASH.  Scaling cannot create edge; it can only change how
#   much of the same edge you own.
VOL_TARGET = 0.04

BOOK_NAMES = ("BOOK", "BOOK-NOV", "BOOK-VT")

COST_LEVELS_BPS = [0.0, 5.0, 20.0]
REFERENCE_COST_BPS = 5.0

# --- [ESTIMATED] dividend yields ------------------------------------------
# A CONSTANT, annualised, assumed yield credited per trading day.  It is not a
# measured distribution stream.  GLD/SLV/DBC/UUP/BIL are physical/index or
# cash-like vehicles and are assumed to pay nothing; every other figure is an
# order-of-magnitude long-run average for that fund's asset class.
DIV_YIELD_EST = {
    "SPY": 0.0180, "QQQ": 0.0090, "IWM": 0.0140, "MDY": 0.0160, "DIA": 0.0190,
    "TLT": 0.0300, "TLH": 0.0290, "EDV": 0.0360, "IEF": 0.0260, "SHY": 0.0190,
    "TIP": 0.0280, "LQD": 0.0340, "HYG": 0.0560, "EMB": 0.0480, "BIL": 0.0000,
    "GLD": 0.0000, "SLV": 0.0000, "GDX": 0.0120, "DBC": 0.0000, "VNQ": 0.0380,
    "EEM": 0.0230, "EFA": 0.0270, "EWJ": 0.0160, "FXI": 0.0220, "ILF": 0.0430,
    "EWZ": 0.0580, "UUP": 0.0000, "XLE": 0.0340, "XLU": 0.0300, "XLK": 0.0090,
    "XLP": 0.0260, "XLV": 0.0180,
}

# --- [MODELED] BOND10M -----------------------------------------------------
BOND10M_MODIFIED_DURATION = 7.5   # constant, stated; used only in reduced book

# --- success bar -----------------------------------------------------------
SUCCESS_BAR = {"years": 0.90, "quarters": 0.75, "sharpe": 0.80, "vs_cash": True}

BUCKETS = ["D", "W", "2W", "M", "Q", "H", "Y"]
LAMBDA_STEP = 0.001
LAMBDA_MAX = 1.0

PREREG_TEXT = [
    ("window (primary)", "%s .. %s  (%.2f years)"
     % (WINDOW_START.isoformat(), "last data date", 0.0)),
    ("window (reduced)", "%s .. last data date" % REDUCED_START.isoformat()),
    ("T  trend", "every instrument in the verified universe; long when its own "
                 "close > its own SMA(%d) on the rebalance close, else flat; "
                 "portfolio = INVERSE-VOLATILITY weights over the instruments "
                 "that exist at that date, renormalised to 1; rebalanced "
                 "monthly; flat capital earns the cash rate" % SMA_TREND),
    ("   universe", "%d instruments: %s" % (len(TREND_UNIVERSE),
                                            ",".join(TREND_UNIVERSE))),
    ("   vol window", "%d trading days" % VOL_WINDOW),
    ("C  carry/credit", "long %s and short %s at inverse-vol weights summing to "
                        "1; the short leg's proceeds earn the cash rate; the "
                        "long leg is credited its estimated dividend and the "
                        "short leg PAYS the estimated dividend.  Live only when "
                        "BOTH legs exist; cash before that."
                        % (CARRY_LONG, CARRY_SHORT)),
    ("V  VRP [MODELED]", "monthly short %d-DTE put spread on SPY; short strike "
                         "at |delta| = %.2f under IV = VIX(t-%d); long strike "
                         "%.0f%% lower; short strike priced at ATM + %.1f vol "
                         "pt, long at ATM + %.1f vol pt; daily Black-Scholes "
                         "mark, settled at intrinsic vs the real SPY path; "
                         "return is P&L divided by the spread WIDTH (a "
                         "conservative margin proxy)"
                         % (VRP_DTE, VRP_DELTA, VRP_VIX_LAG,
                            100 * VRP_SPREAD_PCT, VRP_SKEW_SHORT,
                            VRP_SKEW_LONG)),
    ("V  sensitivity", "skew steepness re-run at %s vol points; %.1f is the "
                       "BASE case and is the sibling study's break-even"
                       % (VRP_SKEW_SENSITIVITIES, VRP_SKEW_SHORT)),
    ("H  hedge a", "equal-risk long %s when VIX(close) > SMA(%d) of VIX, else "
                   "flat (cash)"
                   % ("/".join(HEDGE_RULE_INSTRUMENTS), HEDGE_VIX_SMA)),
    ("H  hedge b [MODELED]", "always-on long %d-DTE %.0f%%-OTM SPY put overlay "
                             "with a premium budget of %.1f%% of sleeve capital "
                             "PER YEAR, spent at 1/12 a month, rolled monthly"
                             % (HEDGE_PUT_DTE, 100 * HEDGE_PUT_OTM,
                                100 * HEDGE_PUT_BUDGET_PCT_PER_YEAR)),
    ("H  in the book", "%.0f%% H_a + %.0f%% H_b, fixed"
                       % (100 * HEDGE_BLEND, 100 * (1 - HEDGE_BLEND))),
    ("X  x-sec mom", "each month hold the top %d instruments by trailing %d-day "
                     "return, equal-weight, rest cash; NO tuning"
                     % (XSEC_N, XSEC_LOOKBACK_DAYS)),
    ("B  baseline", "100%% %s buy and hold" % BASELINE),
    ("BOOK", " + ".join("%s %.2f" % (k, v) for k, v in
                        sorted(BOOK_WEIGHTS.items()))),
    ("BOOK-NOV", " + ".join("%s %.2f" % (k, v) for k, v in
                            sorted(BOOK_NOV_WEIGHTS.items()))),
    ("REDUCED", " + ".join("%s %.2f" % (k, v) for k, v in
                           sorted(REDUCED_BOOK_WEIGHTS.items()))),
    ("REDUCED screen", "an EXISTENCE screen only: the trend universe restricted "
                       "to the instruments with a print on %s"
                       % REDUCED_START.isoformat()),
    ("cost levels", "round-trip %s bps; one-way = half of that per unit "
                    "notional traded" % ", ".join(str(c) for c in
                                                   COST_LEVELS_BPS)),
    ("dividend", "constant [ESTIMATED] yields applied per trading day; "
                 "SPY %.2f%%/yr, universe mean %.2f%%/yr"
                 % (100 * DIV_YIELD_EST["SPY"],
                    100 * sum(DIV_YIELD_EST[s] for s in TREND_UNIVERSE)
                    / len(TREND_UNIVERSE))),
    ("cash", "[UPPER BOUND] TVC:US03M 3-month T-bill yield accrued at "
             "yield/252 per trading day, no fees, no spread, full quoted yield "
             "credited every business day"),
    ("success bar", ">=%.0f%% of years positive AND >=%.0f%% of quarters "
                    "positive AND Sharpe > %.1f AND CAGR above cash"
                    % (100 * SUCCESS_BAR["years"],
                       100 * SUCCESS_BAR["quarters"], SUCCESS_BAR["sharpe"])),
]


# ===========================================================================
# The sibling engine, imported rather than re-implemented
# ===========================================================================

def load_engine():
    path = os.path.join(ENGINE_DIR, "timeframe_stats.py")
    if not os.path.isfile(path):
        raise SystemExit(
            "ERROR: the sibling engine is missing.\n"
            "  expected: %s\n"
            "  This study imports its bucket_key / aggregate_bucket / sample_sd "
            "/ max_drawdown / lag1_autocorr / n_effective instead of "
            "re-implementing them." % path)
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


# ===========================================================================
# Small helpers
# ===========================================================================

def pct(v, nd=2):
    if v is NA or v is None:
        return "n/a"
    return ("%." + str(nd) + "f%%") % (100.0 * v)


def num(v, nd=4):
    if v is NA or v is None:
        return "n/a"
    return ("%." + str(nd) + "f") % v


def fnum(v, nd=10):
    """CSV-safe numeric: an empty cell for a missing value, never 'None'."""
    if v is NA or v is None:
        return ""
    if isinstance(v, str):
        return v
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


def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_ppf(p):
    """Inverse standard normal by deterministic bisection.  No tables."""
    lo, hi = -12.0, 12.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if norm_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def bs_put(S, K, T, sigma, r, q):
    """Black-Scholes European put."""
    if T <= 0.0 or sigma <= 0.0:
        return max(0.0, K - S)
    sq = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / sq
    d2 = d1 - sq
    return K * math.exp(-r * T) * norm_cdf(-d2) - \
        S * math.exp(-q * T) * norm_cdf(-d1)


def strike_for_put_delta(S, T, sigma, r, q, delta):
    """Strike at which the put's delta equals -delta, in closed form.

    d1 = (ln(S/K) + (r-q+sigma^2/2)T) / (sigma sqrt T)
    put delta = -e^{-qT} N(-d1)  =>  -d1 = norm_ppf(delta)
    """
    sq = sigma * math.sqrt(T)
    if sq <= 0.0:
        return S
    d1 = -norm_ppf(delta)
    lnSK = d1 * sq - (r - q + 0.5 * sigma * sigma) * T
    return S * math.exp(-lnSK)


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


# ===========================================================================
# Input
# ===========================================================================

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
    if len(dates) < 260:
        raise SystemExit("ERROR: %s has only %d rows; need >= 260"
                         % (path, len(dates)))
    if any(dates[i] >= dates[i + 1] for i in range(len(dates) - 1)):
        raise SystemExit("ERROR: %s dates are not strictly increasing" % path)
    symbol = os.path.basename(path).split("_")[0]
    return Series(symbol, dates, o, h, l, c, v, provenance)


ALL_PRICE_SYMBOLS = TREND_UNIVERSE + ["BIL"]
ALL_OTHER_SYMBOLS = ["VIX", "US03M", "US02Y", "US10Y", "US30Y", "DXY"]


def load_universe():
    out = {}
    missing = []
    for sym in ALL_PRICE_SYMBOLS + ALL_OTHER_SYMBOLS:
        path = os.path.join(DATA_DIR, sym + "_1d.csv")
        if not os.path.isfile(path):
            missing.append(sym)
            continue
        out[sym] = read_bars(path)
    return out, missing


# ===========================================================================
# Alignment: an instrument's returns, SMA and vol measured on the BOOK calendar
# ===========================================================================

class Aligned(object):
    """One instrument's state projected onto the book's own date list.

    A position may only change on a BOOK date.  The return measured on book
    date j is the instrument's own price move from its last bar at or before
    book date j-1 to its last bar at or before book date j, so a bar the book
    calendar does not contain is never lost: its move is counted on the next
    book date.  `sma`, `vol` and `close` are the instrument's values at its last
    bar at or before j -- never a forward-looking value.
    """

    def __init__(self, series, dates, vol_window, sma_window, div_yield):
        self.symbol = series.symbol
        n = len(dates)
        self.ret = [0.0] * n
        self.close = [NA] * n
        self.sma = [NA] * n
        self.vol = [NA] * n
        self.has = [False] * n
        self.live = [False] * n
        self.first_live = None
        avg = sma(series.c, sma_window)
        idx = series.index_of
        rets = [0.0] * len(series.c)
        for i in range(1, len(series.c)):
            prev = series.c[i - 1]
            rets[i] = (series.c[i] / prev - 1.0) if prev > 0 else 0.0
        # rolling sample sd of the instrument's own daily returns
        vol = [NA] * len(series.c)
        for i in range(len(series.c)):
            if i >= vol_window:
                chunk = rets[i - vol_window + 1:i + 1]
                vol[i] = TF.sample_sd(chunk)
        div_daily = div_yield / float(TRADING_DAYS_PER_YEAR)
        last = None
        for j, d in enumerate(dates):
            k = idx.get(d)
            if k is None:
                if last is not None:
                    self.close[j] = series.c[last]
                    self.sma[j] = avg[last]
                    self.vol[j] = vol[last]
                    self.has[j] = True
                    self.live[j] = avg[last] is not NA
                    self.ret[j] = 0.0
                continue
            if last is not None:
                prev = series.c[last]
                self.ret[j] = ((series.c[k] / prev - 1.0) if prev > 0 else 0.0)
            else:
                self.ret[j] = 0.0
            self.ret[j] += div_daily
            self.close[j] = series.c[k]
            self.sma[j] = avg[k]
            self.vol[j] = vol[k]
            self.has[j] = True
            self.live[j] = avg[k] is not NA
            if self.live[j] and self.first_live is None:
                self.first_live = d
            last = k


# ===========================================================================
# CASH -- a yield index, handled explicitly rather than silently
# ===========================================================================

class Cash(object):
    """TVC:US03M is a 3-MONTH T-BILL YIELD INDEX, not a fund.

    r_cash[j] = (yield observed at the close of book date j-1 / 100) / 252

    The rate is the one seen at the PREVIOUS book close, the same no-lookahead
    convention every sleeve uses for its position.  A missing observation
    carries the last known rate forward -- and the count of carried days, the
    longest gap, the rate range and the number of negative-rate days are all
    returned so the handling can be audited rather than assumed.

    *** UPPER BOUND, NOT A TRADABLE RETURN ***  A yield index is not a fund: it
    ignores management fees, the bid/offer and roll of an actual T-bill
    portfolio, and credits the full quoted yield on every business day.
    """

    def __init__(self, dates, us03m):
        idx = us03m.index_of
        self.ret = [0.0] * len(dates)
        self.rate = [NA] * len(dates)
        self.carried = 0
        self.printed = 0
        self.gap_run = 0
        self.gap_max = 0
        self.no_rate_days = 0
        last = NA
        for j, d in enumerate(dates):
            if j == 0:
                k = idx.get(d)
                if k is not None:
                    last = us03m.c[k]
                    self.printed += 1
                continue
            k = idx.get(dates[j - 1])
            if k is not None:
                last = us03m.c[k]
                self.printed += 1
                if self.gap_run > self.gap_max:
                    self.gap_max = self.gap_run
                self.gap_run = 0
            else:
                self.carried += 1
                self.gap_run += 1
            if last is NA:
                self.no_rate_days += 1
                self.ret[j] = 0.0
                continue
            self.rate[j] = last
            self.ret[j] = (last / 100.0) / float(TRADING_DAYS_PER_YEAR)
        if self.gap_run > self.gap_max:
            self.gap_max = self.gap_run

    def diagnostics(self):
        rates = [r for r in self.rate if r is not NA]
        return {
            "n_days": len(self.ret) - 1,
            "printed": self.printed,
            "carried_forward": self.carried,
            "carried_pct": self.carried / float(max(1, len(self.ret) - 1)),
            "longest_gap_days": self.gap_max,
            "no_rate_days": self.no_rate_days,
            "rate_min": min(rates) if rates else NA,
            "rate_max": max(rates) if rates else NA,
            "rate_mean": (sum(rates) / len(rates)) if rates else NA,
            "negative_rate_days": sum(1 for r in rates if r < 0.0),
            "zero_return_days": sum(1 for r in self.ret[1:] if r == 0.0),
        }


def bil_cross_check(dates, bil):
    """Why the BIL ETF is NOT usable as a cash proxy, shown rather than asserted.

    A T-bill ETF distributes essentially all of its yield, so its PRICE is
    approximately flat while its holders earn the distribution.  Compounding
    BIL's price-only return therefore measures the fee drag and the
    distribution, not cash.
    """
    idx = bil.index_of
    last = None
    r = [0.0] * len(dates)
    for j, d in enumerate(dates):
        k = idx.get(d)
        if k is None:
            continue
        if last is not None:
            r[j] = bil.c[k] / bil.c[last] - 1.0
        last = k
    return r


# ===========================================================================
# Sleeves -- each is one pre-registered rule reduced to a daily return series
# ===========================================================================

class SleeveResult(object):
    def __init__(self, name, dates):
        self.name = name
        self.dates = list(dates)
        self.gross = [0.0] * len(dates)
        self.turnover = [0.0] * len(dates)
        self.meta = {}

    def net(self, cost_bps):
        half = (cost_bps / 2.0) / 10000.0
        out = [0.0] * len(self.dates)
        for j in range(len(self.dates)):
            c = half * self.turnover[j]
            if c > 1.0:
                c = 1.0
            out[j] = (1.0 + self.gross[j]) * (1.0 - c) - 1.0
        return out


def month_start_indices(dates):
    out = []
    for j in range(1, len(dates)):
        if dates[j].month != dates[j - 1].month:
            out.append(j)
    return out


def inv_vol_weights(items):
    """items = [(symbol, vol)].  Inverse-volatility, normalised to 1."""
    raw = []
    for sym, vol in items:
        if vol is NA or vol is None or vol <= 0.0:
            continue
        raw.append((sym, 1.0 / vol))
    tot = sum(w for _, w in raw)
    if tot <= 0.0:
        return {}
    return dict((s, w / tot) for s, w in raw)


# --- T ---------------------------------------------------------------------

def sleeve_T(dates, starts, A, cash, universe, tag="T"):
    res = SleeveResult(tag, dates)
    pos = dict((s, 0.0) for s in universe)
    cash_pos = 1.0
    month = iter(starts + [len(dates)])
    nxt = next(month)
    live_hist = []
    for j in range(len(dates)):
        if j == nxt and j >= 1:
            p = j - 1
            items = []
            sig = {}
            for s in universe:
                a = A[s]
                if not a.live[p]:
                    continue
                if a.close[p] is NA or a.sma[p] is NA:
                    continue
                items.append((s, a.vol[p]))
                sig[s] = 1.0 if a.close[p] > a.sma[p] else 0.0
            w = inv_vol_weights(items)
            newpos = {}
            for s in universe:
                newpos[s] = w.get(s, 0.0) * sig.get(s, 0.0)
            newcash = 1.0 - sum(newpos.values())
            turn = sum(abs(newpos[s] - pos[s]) for s in universe) + \
                abs(newcash - cash_pos)
            res.turnover[j] += turn
            pos = newpos
            cash_pos = newcash
            live_hist.append(sum(1 for s in universe if pos[s] > 0.0))
            try:
                nxt = next(month)
            except StopIteration:
                nxt = len(dates) + 1
        g = cash_pos * cash.ret[j]
        for s in universe:
            if pos[s]:
                g += pos[s] * A[s].ret[j]
        res.gross[j] = g
    res.meta["mean_live_instruments"] = (sum(live_hist) / float(len(live_hist))
                                         if live_hist else NA)
    res.meta["rebalances"] = len(live_hist)
    return res


# --- X ---------------------------------------------------------------------

def sleeve_X(dates, starts, A, cash, universe, n_hold, lookback, tag=None):
    tag = tag or ("X%d" % n_hold)
    res = SleeveResult(tag, dates)
    pos = dict((s, 0.0) for s in universe)
    cash_pos = 1.0
    it = iter(starts + [len(dates)])
    nxt = next(it)
    picks_hist = []
    for j in range(len(dates)):
        if j == nxt and j >= 1:
            p = j - 1
            q = p - lookback
            if q >= 0:
                scored = []
                for s in universe:
                    a = A[s]
                    if a.close[p] is NA or a.close[q] is NA or a.close[q] <= 0:
                        continue
                    scored.append((a.close[p] / a.close[q] - 1.0, s))
                scored.sort(key=lambda t: (-t[0], t[1]))
                chosen = [s for _, s in scored[:n_hold]]
                newpos = dict((s, 0.0) for s in universe)
                if chosen:
                    w = 1.0 / len(chosen)
                    for s in chosen:
                        newpos[s] = w
                newcash = 1.0 - sum(newpos.values())
                turn = sum(abs(newpos[s] - pos[s]) for s in universe) + \
                    abs(newcash - cash_pos)
                res.turnover[j] += turn
                pos = newpos
                cash_pos = newcash
                picks_hist.append(",".join(chosen))
            try:
                nxt = next(it)
            except StopIteration:
                nxt = len(dates) + 1
        g = cash_pos * cash.ret[j]
        for s in universe:
            if pos[s]:
                g += pos[s] * A[s].ret[j]
        res.gross[j] = g
    res.meta["n_picks"] = n_hold
    res.meta["lookback_days"] = lookback
    res.meta["rebalances"] = len(picks_hist)
    res.meta["last_picks"] = picks_hist[-1] if picks_hist else ""
    return res


# --- C ---------------------------------------------------------------------

def sleeve_C(dates, starts, A, cash, tag="C", hyg_only=False):
    res = SleeveResult(tag, dates)
    long_sym, short_sym = CARRY_LONG, CARRY_SHORT
    wh, wi = 0.0, 0.0
    cash_pos = 1.0
    it = iter(starts + [len(dates)])
    nxt = next(it)
    live_months = 0
    for j in range(len(dates)):
        if j == nxt and j >= 1:
            p = j - 1
            a_h, a_i = A[long_sym], A[short_sym]
            if a_h.live[p] and (hyg_only or a_i.live[p]):
                if hyg_only:
                    nwh, nwi = 1.0, 0.0
                else:
                    w = inv_vol_weights([(long_sym, a_h.vol[p]),
                                         (short_sym, a_i.vol[p])])
                    nwh = w.get(long_sym, 0.0)
                    nwi = w.get(short_sym, 0.0)
                ncash = 1.0 - nwh - nwi
                live_months += 1
            else:
                nwh, nwi, ncash = 0.0, 0.0, 1.0
            turn = abs(nwh - wh) + abs(nwi - wi) + abs(ncash - cash_pos)
            res.turnover[j] += turn
            wh, wi, cash_pos = nwh, nwi, ncash
            try:
                nxt = next(it)
            except StopIteration:
                nxt = len(dates) + 1
        g = cash_pos * cash.ret[j]
        if wh:
            g += wh * A[long_sym].ret[j]
        if wi:
            # short leg: the price move is earned inverted, the ESTIMATED
            # dividend is PAID (it is inside A[].ret), and the short proceeds
            # earn the cash rate.
            g += -wi * A[short_sym].ret[j] + wi * cash.ret[j]
        res.gross[j] = g
    res.meta["long"] = long_sym
    res.meta["short"] = ("none" if hyg_only else "-" + short_sym)
    res.meta["live_months"] = live_months
    return res


# --- V ---------------------------------------------------------------------

def sleeve_V(dates, starts, spy, vix, cash, skew_short, skew_long, tag="V"):
    """[MODELED] monthly short put spread on SPY, marked daily by Black-Scholes.

    Contract per roll period, set from the rebalance close j-1:
        S0      = SPY close
        iv_atm  = VIX close from VRP_VIX_LAG trading days earlier, / 100
        sigma_s = iv_atm + skew_short/100     (the SHORT strike is sold rich)
        sigma_l = iv_atm + skew_long/100      (the LONG  strike is bought)
        K1      = strike at which the put delta is -VRP_DELTA under sigma_s,
                  solved in closed form
        K2      = K1 * (1 - VRP_SPREAD_PCT)
        credit  = bs_put(K1, sigma_s) - bs_put(K2, sigma_l)
        width   = K1 - K2
        expiry  = the first book session at least VRP_DTE calendar days later

    SIZING (declared):  the whole sleeve notional is posted as the spread's
    margin, i.e. units = V_entry / width, so a TOTAL loss on the spread is
    exactly -100% of the sleeve.  This is the most aggressive defensible
    reading of "return on the capital the position ties up" and it is what the
    pre-registration declared; a vol-normalised reporting variant of the BOOK
    is provided separately so the reader can see the effect of sizing alone.

    ACCOUNTING (exact, value-based, no double count):
        V_t = V_entry + units * (credit - L_t)          between entry and expiry
        V_e = V_entry + units * (credit - payoff_e)     at expiry, settled at
                                                        INTRINSIC against the
                                                        real SPY path
        r_t = V_t / V_{t-1} - 1
    Nothing is settled at a model price: the mark is Black-Scholes but the
    terminal value is intrinsic on the real path.
    """
    res = SleeveResult(tag, dates)
    n = len(dates)
    spy_idx = spy.index_of
    vix_idx = vix.index_of
    s_close = [NA] * n
    v_lag = [NA] * n
    last_s = last_v = None
    vhist = []
    for j in range(n):
        k = spy_idx.get(dates[j])
        if k is not None:
            last_s = k
        if last_s is not None:
            s_close[j] = spy.c[last_s]
        k = vix_idx.get(dates[j])
        if k is not None:
            last_v = k
            vhist.append(k)
        if last_v is not None and len(vhist) > VRP_VIX_LAG:
            v_lag[j] = vix.c[vhist[-1 - VRP_VIX_LAG]]

    it = iter(starts + [n + 1])
    nxt = next(it)

    def spread_mark(j):
        """(value per unit) of the live spread at book date j."""
        if k1 is None:
            return 0.0
        T = max(0.0, (dates[exp_i] - dates[j]).days / 365.0)
        S = s_close[j]
        if S is NA:
            return entry_c
        if T <= 0.0:
            return max(0.0, k1 - S) - max(0.0, k2 - S)
        r = cash.rate[j] if cash.rate[j] is not NA else 0.0
        r = max(0.0, r / 100.0)
        q = DIV_YIELD_EST["SPY"]
        return bs_put(S, k1, T, sig_s, r, q) - bs_put(S, k2, T, sig_l, r, q)

    V = 1.0
    base = 1.0          # sleeve value at the start of the live spread
    units = 0.0
    k1 = k2 = None
    sig_s = sig_l = None
    exp_i = None
    entry_c = 0.0
    credit = 0.0
    width = 1.0
    rolls = 0
    total_credit = 0.0
    total_payoff = 0.0
    creds_pct = []
    prev_v = 1.0
    rolls_log = []

    for j in range(n):
        # --- settle on the expiry session, whatever day of the month it is
        if k1 is not None and j >= exp_i:
            payoff = 0.0
            S = s_close[j]
            if S is not NA:
                payoff = max(0.0, k1 - S) - max(0.0, k2 - S)
            V = base + units * (credit - payoff)
            total_payoff += payoff
            k1 = None
            units = 0.0
        # --- roll on the first session of a month, using data at j-1
        if j == nxt and j >= 1:
            p = j - 1
            if s_close[p] is not NA and v_lag[p] is not NA and v_lag[p] > 0.0:
                S0 = s_close[p]
                iv = v_lag[p] / 100.0
                sig_s = iv + skew_short / 100.0
                sig_l = iv + skew_long / 100.0
                r = cash.rate[p] if cash.rate[p] is not NA else 0.0
                r = max(0.0, r / 100.0)
                q = DIV_YIELD_EST["SPY"]
                T = VRP_DTE / 365.0
                k1 = strike_for_put_delta(S0, T, sig_s, r, q, VRP_DELTA)
                k2 = k1 * (1.0 - VRP_SPREAD_PCT)
                credit = (bs_put(S0, k1, T, sig_s, r, q)
                          - bs_put(S0, k2, T, sig_l, r, q))
                width = k1 - k2
                if width <= 0.0:
                    width = 1.0
                exp_i = j
                while exp_i < n - 1 and (dates[exp_i] - dates[p]).days < VRP_DTE:
                    exp_i += 1
                entry_c = credit
                base = V
                units = V / width
                total_credit += credit * units
                rolls += 1
                creds_pct.append(credit / width)
                rolls_log.append((dates[p].isoformat(), dates[j].isoformat(),
                                  dates[exp_i].isoformat(), S0, v_lag[p], iv,
                                  sig_s, sig_l, r, q, k1, k2, width, credit,
                                  credit / width))
                res.turnover[j] += 2.0
            try:
                nxt = next(it)
            except StopIteration:
                nxt = n + 1
        # --- value the sleeve at today's close and record the return
        if k1 is None:
            V = V * (1.0 + cash.ret[j])
        else:
            V = base + units * (credit - spread_mark(j))
        if j > 0:
            res.gross[j] = V / prev_v - 1.0 if prev_v > 0.0 else 0.0
        prev_v = V
    res.meta["rolls"] = rolls
    res.meta["skew_short_volpts"] = skew_short
    res.meta["skew_long_volpts"] = skew_long
    res.meta["mean_credit_pct_of_width"] = (sum(creds_pct) / len(creds_pct)
                                            if creds_pct else NA)
    res.meta["min_credit_pct_of_width"] = min(creds_pct) if creds_pct else NA
    res.meta["max_credit_pct_of_width"] = max(creds_pct) if creds_pct else NA
    res.meta["total_credit_per_unit"] = total_credit
    res.meta["total_payoff_per_unit"] = total_payoff
    res.meta["ending_value"] = V
    res.meta["rolls_log"] = rolls_log
    return res



# --- H ---------------------------------------------------------------------

def sleeve_H_a(dates, starts, A, cash, vix, tag="H_a"):
    """Equal-risk long HEDGE_RULE_INSTRUMENTS when VIX(close) > SMA(VIX), else
    flat (cash).  Deliberately NOT a trend rule on VIX: the sibling study showed
    that buying VIX spikes on a mean-reverting series loses 86.9%/yr
    compounded."""
    res = SleeveResult(tag, dates)
    n = len(dates)
    vix_idx = vix.index_of
    v = [0.0] * n
    have = [False] * n
    last = None
    for j in range(n):
        k = vix_idx.get(dates[j])
        if k is not None:
            last = k
        if last is not None:
            v[j] = vix.c[last]
            have[j] = True
    vs = sma(v, HEDGE_VIX_SMA)
    syms = HEDGE_RULE_INSTRUMENTS
    pos = dict((s, 0.0) for s in syms)
    cash_pos = 1.0
    it = iter(starts + [n + 1])
    nxt = next(it)
    on_months = 0
    rebals = 0
    for j in range(n):
        if j == nxt and j >= 1:
            p = j - 1
            trigger = have[p] and vs[p] is not NA and v[p] > vs[p]
            items = [(s, A[s].vol[p]) for s in syms if A[s].live[p]]
            newpos = dict((s, 0.0) for s in syms)
            if trigger and items:
                w = inv_vol_weights(items)
                for s in syms:
                    newpos[s] = w.get(s, 0.0)
                on_months += 1
            ncash = 1.0 - sum(newpos.values())
            turn = sum(abs(newpos[s] - pos[s]) for s in syms) + \
                abs(ncash - cash_pos)
            res.turnover[j] += turn
            pos, cash_pos = newpos, ncash
            rebals += 1
            try:
                nxt = next(it)
            except StopIteration:
                nxt = n + 1
        g = cash_pos * cash.ret[j]
        for s in syms:
            if pos[s]:
                g += pos[s] * A[s].ret[j]
        res.gross[j] = g
    res.meta["months_long"] = on_months
    res.meta["rebalances"] = rebals
    res.meta["instruments"] = "/".join(syms)
    res.meta["vix_sma"] = HEDGE_VIX_SMA
    return res


def cohort_value(c, j, s_close, cash, dates):
    S = s_close[j]
    if S is NA:
        return 0.0
    T = max(0.0, (dates[c["expiry_index"]] - dates[j]).days / 365.0)
    if T <= 0.0:
        return c["units"] * max(0.0, c["k"] - S)
    r = cash.rate[j] if cash.rate[j] is not NA else 0.0
    r = max(0.0, r / 100.0)
    q = DIV_YIELD_EST["SPY"]
    return c["units"] * bs_put(S, c["k"], T, c["sigma"], r, q)


def sleeve_H_b(dates, starts, spy, vix, cash, tag="H_b"):
    """[MODELED] always-on long-put overlay with a STATED premium budget.

    The accounting is exact and auditable:
        V = cash_part + sum(cohort_value)
    cash_part accrues the cash rate daily.  On each monthly roll a premium budget
    of (HEDGE_PUT_BUDGET_PCT_PER_YEAR / 12) * V is spent: cash_part falls by the
    budget and one new cohort is created holding budget/premium units of a
    HEDGE_PUT_DTE-day, HEDGE_PUT_OTM-strike SPY put priced at ATM + VRP_SKEW_LONG
    vol points.  Each cohort is marked daily by Black-Scholes and settled at
    INTRINSIC on its own expiry day.  The sleeve's daily return is
    V_t / V_{t-1} - 1, so the premium shows up as a real drag.
    """
    res = SleeveResult(tag, dates)
    n = len(dates)
    spy_idx = spy.index_of
    vix_idx = vix.index_of
    s_close = [NA] * n
    v_close = [NA] * n
    last_s = last_v = None
    for j in range(n):
        k = spy_idx.get(dates[j])
        if k is not None:
            last_s = k
        if last_s is not None:
            s_close[j] = spy.c[last_s]
        k = vix_idx.get(dates[j])
        if k is not None:
            last_v = k
        if last_v is not None:
            v_close[j] = vix.c[last_v]

    cohorts = []
    cash_part = 1.0
    V = 1.0
    it = iter(starts + [n + 1])
    nxt = next(it)
    spent = 0.0
    payoffs = 0.0
    rolls = 0
    prev_v = 1.0

    for j in range(n):
        if j > 0:
            cash_part *= (1.0 + cash.ret[j])
        still = []
        for c in cohorts:
            if j >= c["expiry_index"]:
                S = s_close[j]
                payoff = 0.0
                if S is not NA:
                    payoff = c["units"] * max(0.0, c["k"] - S)
                cash_part += payoff
                payoffs += payoff
            else:
                still.append(c)
        cohorts = still
        if j == nxt and j >= 1:
            V = cash_part + sum(cohort_value(c, j, s_close, cash, dates)
                                for c in cohorts)
            budget = V * (HEDGE_PUT_BUDGET_PCT_PER_YEAR / 12.0)
            S = s_close[j - 1]
            iv = NA
            if v_close[j - 1] is not NA and v_close[j - 1] > 0.0:
                iv = v_close[j - 1] / 100.0
            if S is not NA and iv is not NA:
                r = cash.rate[j - 1] if cash.rate[j - 1] is not NA else 0.0
                r = max(0.0, r / 100.0)
                q = DIV_YIELD_EST["SPY"]
                T = HEDGE_PUT_DTE / 365.0
                K = S * (1.0 - HEDGE_PUT_OTM)
                sigma = iv + VRP_SKEW_LONG / 100.0
                prem = bs_put(S, K, T, sigma, r, q)
                if prem > 0.0:
                    units = budget / prem
                    exp_i = j
                    while exp_i < n - 1 and (dates[exp_i] - dates[j - 1]).days \
                            < HEDGE_PUT_DTE:
                        exp_i += 1
                    cohorts.append({"k": K, "units": units,
                                    "expiry_index": exp_i, "sigma": sigma})
                    cash_part -= budget
                    spent += budget
                    rolls += 1
                    res.turnover[j] += 2.0 * (budget / V)
            try:
                nxt = next(it)
            except StopIteration:
                nxt = n + 1
        V = cash_part + sum(cohort_value(c, j, s_close, cash, dates)
                            for c in cohorts)
        if j > 0:
            res.gross[j] = V / prev_v - 1.0
        prev_v = V
    res.meta["rolls"] = rolls
    res.meta["premium_spent_total"] = spent
    res.meta["premium_spent_per_yr"] = spent / years_between(dates[0], dates[-1])
    res.meta["payoffs_total"] = payoffs
    res.meta["ending_value"] = V
    return res


# --- B and BOND10M ---------------------------------------------------------

def sleeve_B(dates, A, sym, tag=None):
    tag = tag or ("B_" + sym)
    res = SleeveResult(tag, dates)
    for j in range(len(dates)):
        res.gross[j] = A[sym].ret[j]
    if len(dates):
        res.turnover[0] += 1.0
    res.meta["symbol"] = sym
    return res


def sleeve_bond10m(dates, y10, tag="BOND10M"):
    """[MODELED] long-Treasury total return from the 10-year yield:

        r_j = -D * (y_j - y_{j-1}) + y_{j-1}/252,   D = 7.5 (constant)

    This exists ONLY so the reduced long-window book has a duration leg before
    IEF/TLT list in 2002.  A constant modified duration is wrong in the tails --
    convexity, roll-down and the maturity drift of a real bond are all ignored --
    and every number from it is tagged [MODELED].
    """
    res = SleeveResult(tag, dates)
    n = len(dates)
    idx = y10.index_of
    y = [NA] * n
    last = None
    for j in range(n):
        k = idx.get(dates[j])
        if k is not None:
            last = k
        if last is not None:
            y[j] = y10.c[last]
    D = BOND10M_MODIFIED_DURATION
    for j in range(2, n):
        if y[j] is NA or y[j - 1] is NA:
            continue
        dy = (y[j] - y[j - 1]) / 100.0
        res.gross[j] = -D * dy + (y[j - 1] / 100.0) / float(
            TRADING_DAYS_PER_YEAR)
    res.meta["modified_duration"] = D
    return res


# ===========================================================================
# Periods -- the same bucketing the sibling engine uses, applied to returns
# ===========================================================================

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
    ps = period_returns(rets, groups)
    n = len(ps)
    if not n:
        return NA, NA, 0, 0, 0, ps
    npos = sum(1 for p in ps if p["ret"] > 0.0)
    nzero = sum(1 for p in ps if p["ret"] == 0.0)
    return npos / float(n), (npos + nzero) / float(n), npos, nzero, n, ps


def level_stats(dates, rets):
    n = len(rets)
    curve = equity_curve(rets)
    yrs = years_between(dates[0], dates[-1])
    cagr = -1.0 if curve[-1] <= 0.0 else curve[-1] ** (1.0 / yrs) - 1.0
    m = sum(rets) / n if n else NA
    sd = TF.sample_sd(rets)
    sharpe = (m / sd * math.sqrt(TRADING_DAYS_PER_YEAR)) if (sd not in (NA, 0)) \
        else NA
    return {"n_days": n, "years": yrs, "cagr": cagr,
            "max_dd": max_drawdown_pct(curve),
            "max_dd_additive": TF.max_drawdown(rets),
            "sharpe": sharpe, "mean_daily": m, "sd_daily": sd,
            "ann_vol": sd * math.sqrt(TRADING_DAYS_PER_YEAR) if sd is not NA
            else NA}


def sharpe_excess(dates, rets, cash_ret):
    ex = [r - c for r, c in zip(rets, cash_ret)]
    m = sum(ex) / len(ex)
    sd = TF.sample_sd(ex)
    if sd is NA or sd == 0:
        return NA
    return m / sd * math.sqrt(TRADING_DAYS_PER_YEAR)


def month_end_curve(dates, rets, bucket="M"):
    """[(label, first_date, compounded_return_of_that_month)] for complete months."""
    groups = group_index(dates, bucket, complete_only=True)
    ps = period_returns(rets, groups)
    return ps


def worst_rolling(ps, n_months):
    """Worst overlapping compounded return over n_months consecutive months."""
    if len(ps) < n_months:
        return NA, None
    worst = None
    worst_win = None
    for i in range(len(ps) - n_months + 1):
        curve = 1.0
        for k in range(i, i + n_months):
            curve *= (1.0 + ps[k]["ret"])
        r = curve - 1.0
        if worst is None or r < worst:
            worst = r
            worst_win = "%s..%s" % (ps[i]["label"], ps[i + n_months - 1]["label"])
    return worst, worst_win


def metrics(dates, rets, cash_ret):
    ls = level_stats(dates, rets)
    out = dict(ls)
    out["sharpe_excess"] = sharpe_excess(dates, rets, cash_ret)
    # horizon positivity
    for b in BUCKETS:
        groups = group_index(dates, b, complete_only=True)
        f1, f0, npos, nzero, ntot, ps = period_stats(rets, groups)
        out["pos_" + b] = f1
        out["pos_" + b + "_ge0"] = f0
        out["n_" + b] = ntot
        if b == "M":
            out["months"] = ps
    out["worst_month"] = min((p["ret"] for p in out["months"]), default=NA)
    out["worst_month_label"] = (min(out["months"], key=lambda p: p["ret"])["label"]
                                if out["months"] else "n/a")
    out["best_month"] = max((p["ret"] for p in out["months"]), default=NA)
    # years
    ygroups = group_index(dates, "Y", complete_only=True)
    yps = period_returns(rets, ygroups)
    out["years"] = yps
    if yps:
        out["worst_year"] = min(p["ret"] for p in yps)
        out["worst_year_label"] = min(yps, key=lambda p: p["ret"])["label"]
        out["losing_years"] = [p["label"] for p in yps if p["ret"] <= 0.0]
        out["n_years"] = len(yps)
        out["n_pos_years"] = sum(1 for p in yps if p["ret"] > 0.0)
    out["worst_r12"], out["worst_r12_win"] = worst_rolling(out["months"], 12)
    out["worst_r36"], out["worst_r36_win"] = worst_rolling(out["months"], 36)
    return out


# ===========================================================================
# The book
# ===========================================================================

class BookResult(object):
    def __init__(self):
        self.dates = []
        self.rets = []
        self.turnover_total = 0.0
        self.sleeve_rets = {}
        self.weights_log = []


def simulate_book(dates, sleeve_rets, weights, cost_bps=0.0):
    """Fixed-weight book of SLEEVES, rebalanced monthly, weights drifting
    within the month.

        cost_j = (round_trip/2) * one-way notional traded on day j
        R_j    = (1 + sum w_s r_s) * (1 - cost_j) - 1

    Charging the cost in the RETURN is what makes it bite; shrinking a sleeve's
    dollar value would not, because the weights are renormalised at the next
    rebalance.
    """
    syms = sorted([s for s in weights if weights[s] > 0.0])
    tot = sum(weights[s] for s in syms)
    target = dict((s, weights[s] / tot) for s in syms)
    half = (cost_bps / 2.0) / 10000.0

    res = BookResult()
    res.dates = list(dates)
    w = dict(target)
    month_prev = dates[0].month
    res.rets.append(0.0)
    for s in syms:
        res.sleeve_rets.setdefault(s, []).append(0.0)
    res.weights_log.append((dates[0].isoformat(), dict(target)))

    for j in range(1, len(dates)):
        d = dates[j]
        cost = 0.0
        rebalance = (d.month != month_prev)
        if rebalance:
            turn = sum(abs(target[s] - w[s]) for s in syms)
            cost += half * turn
            res.turnover_total += turn
            res.weights_log.append((d.isoformat(), dict(target)))
        month_prev = d.month
        w_held = dict(target) if rebalance else dict(w)
        if cost >= 1.0:
            cost = 1.0
        gross = 0.0
        for s in syms:
            gross += w_held[s] * sleeve_rets[s][j]
        res.rets.append((1.0 + gross) * (1.0 - cost) - 1.0)
        denom = 1.0 + gross
        if denom > 0.0:
            w = dict((s, w_held[s] * (1.0 + sleeve_rets[s][j]) / denom)
                     for s in syms)
        else:
            w = dict(target)
        for s in syms:
            res.sleeve_rets.setdefault(s, []).append(sleeve_rets[s][j])
    return res


def apply_lambda(risky, cash, lam):
    return [lam * r + (1.0 - lam) * c for r, c in zip(risky, cash)]


def vol_scale(dates, rets, target=VOL_TARGET):
    """k = min(1, target / annualised vol).  Uniform, in-sample, declared."""
    v = level_stats(dates, rets)["ann_vol"]
    if v is NA or v <= 0.0:
        return 1.0
    return min(1.0, target / v)


def book_source(bname, mode, cst, NET, cash, dates):
    """(sleeve return dict, weights) for one book, one mode, one cost level."""
    nr = dict(NET[(mode, cst)])
    nr["CASH"] = cash.ret
    if bname != "BOOK-VT":
        w = dict(BOOK_WEIGHTS) if bname == "BOOK" else dict(BOOK_NOV_WEIGHTS)
        return nr, w
    scaled = {}
    w = {}
    for k, wt in BOOK_WEIGHTS.items():
        if k == "CASH" or wt <= 0.0:
            continue
        ks = vol_scale(dates, nr[k])
        scaled[k] = [x * ks for x in nr[k]]
        w[k] = wt * ks
    scaled["CASH"] = cash.ret
    w["CASH"] = 1.0 - sum(w.values())
    return scaled, w


def yearly_return_map(dates, rets):
    """{year label: compounded return of that COMPLETE year}."""
    return dict((p["label"], p["ret"])
                for p in month_end_curve(dates, rets, bucket="Y"))


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return NA
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 0.0 or syy <= 0.0:
        return NA
    return sxy / math.sqrt(sxx * syy)


def corr_matrix(names, yearmaps):
    m = {}
    for a in names:
        for b in names:
            xs, ys = [], []
            for y in sorted(yearmaps[a]):
                if y in yearmaps[b]:
                    xs.append(yearmaps[a][y])
                    ys.append(yearmaps[b][y])
            m[(a, b)] = pearson(xs, ys)
    return m


def corr_check(m, names):
    problems = []
    for a in names:
        if m[(a, a)] is NA or abs(m[(a, a)] - 1.0) > 1e-9:
            problems.append("diagonal %s = %r (expected 1.0)" % (a, m[(a, a)]))
        for b in names:
            va, vb = m[(a, b)], m[(b, a)]
            if va is NA and vb is NA:
                continue
            if va is NA or vb is NA or abs(va - vb) > 1e-12:
                problems.append("asymmetric %s/%s: %r vs %r"
                                % (a, b, va, vb))
    return problems


# ===========================================================================
# Regime grid: trend state x realised-vol tercile
# ===========================================================================

def tercile_breaks(values, n=3):
    xs = sorted(v for v in values if v is not NA)
    if len(xs) < n:
        return []
    return [xs[int(len(xs) * k / float(n))] for k in range(1, n)]


def regime_cells(dates, book_rets, spy_close, spy_sma, spy_vol20, months):
    """Assign each COMPLETE month to a (trend state, vol tercile) cell.

    State and tercile are read from the CLOSE OF THE PREVIOUS MONTH, so nothing
    in a cell's assignment uses that month's own outcome.  The tercile
    breakpoints themselves are computed over the whole window -- an in-sample
    descriptive partition, which is why the grid is reported as a description of
    the weather and not as a tradable signal.
    """
    month_groups = month_end_curve(dates, book_rets)
    # map first day of each complete month -> index
    groups = group_index(dates, "M", complete_only=True)
    brk = tercile_breaks([spy_vol20[j] for j in range(len(dates))])
    cells = {}
    for (key, label, first, last, idx) in groups:
        j0 = idx[0]
        p = j0 - 1
        if p < 0:
            continue
        if spy_close[p] is NA or spy_sma[p] is NA or spy_vol20[p] is NA:
            continue
        state = "UP" if spy_close[p] > spy_sma[p] else "DOWN"
        v = spy_vol20[p]
        if len(brk) == 2:
            tier = "LOW" if v < brk[0] else ("MID" if v < brk[1] else "HIGH")
        else:
            tier = "ALL"
        curve = 1.0
        for j in idx:
            curve *= (1.0 + book_rets[j])
        r = curve - 1.0
        cell = (state, tier)
        d = cells.setdefault(cell, {"n": 0, "sum": 0.0, "pos": 0, "rets": []})
        d["n"] += 1
        d["sum"] += r
        d["pos"] += 1 if r > 0.0 else 0
        d["rets"].append((label, r))
    return cells, brk


def spy_trend_vol(dates, spy):
    idx = spy.index_of
    c = [NA] * len(dates)
    last = None
    for j, d in enumerate(dates):
        k = idx.get(d)
        if k is not None:
            last = k
        if last is not None:
            c[j] = spy.c[last]
    s = sma(c, SMA_TREND)
    rets = [0.0] * len(dates)
    for j in range(1, len(dates)):
        if c[j] is not NA and c[j - 1] is not NA and c[j - 1] > 0:
            rets[j] = c[j] / c[j - 1] - 1.0
    v = [NA] * len(dates)
    for j in range(len(dates)):
        if j >= 20:
            v[j] = TF.sample_sd(rets[j - 19:j + 1])
    return c, s, v


# ===========================================================================
# The lambda frontier: scale exposure against cash
# ===========================================================================

def lambda_grid(step):
    n = int(round(LAMBDA_MAX / step))
    return [round(i * step, 6) for i in range(n + 1)]


def frontier_scan(dates, risky, cash_ret, step):
    rows = []
    gY = group_index(dates, "Y", complete_only=True)
    gQ = group_index(dates, "Q", complete_only=True)
    gM = group_index(dates, "M", complete_only=True)
    for lam in lambda_grid(step):
        r = apply_lambda(risky, cash_ret, lam)
        fY, _, nY, zY, tY, _ = period_stats(r, gY)
        fQ, _, nQ, zQ, tQ, _ = period_stats(r, gQ)
        fM, _, nM, zM, tM, _ = period_stats(r, gM)
        ls = level_stats(dates, r)
        rows.append({"lam": lam, "pos_Y": fY, "Y_pos": nY, "Y_n": tY,
                     "pos_Q": fQ, "Q_pos": nQ, "Q_n": tQ,
                     "pos_M": fM, "M_pos": nM, "M_n": tM,
                     "cagr": ls["cagr"], "max_dd": ls["max_dd"],
                     "sharpe": ls["sharpe"]})
    return rows


def largest_lambda_all_positive(scan, key):
    best = None
    for row in scan:
        if row[key] is not NA and row[key] >= 1.0 - 1e-12:
            best = row
        else:
            break
    return best


# ===========================================================================
# MAIN
# ===========================================================================

def hdr(s):
    print("")
    print("=" * 78)
    print(s)
    print("=" * 78)


def main(argv=None):
    os.makedirs(OUT_DIR, exist_ok=True)
    universe, missing = load_universe()

    hdr("WEATHER-DEEP-TEST -- PRE-REGISTRATION (declared before any result)")
    for k, v in PREREG_TEXT:
        print("  %-18s %s" % (k, v))
    print("")
    print("  The universe is screened on EXISTENCE ONLY (does the source resolve "
          "the symbol and does it have history over the window).  No sleeve, "
          "weight or rule below was chosen by looking at a result.")

    # ---- data inventory -------------------------------------------------
    hdr("DATA INVENTORY -- what resolved, what did not")
    spy = universe["SPY"]
    dates_all = [d for d in spy.dates if d >= WINDOW_START]
    print("  Master calendar = SPY sessions >= %s : %d days, %s .. %s  (%.2f years)"
          % (WINDOW_START.isoformat(), len(dates_all), dates_all[0].isoformat(),
             dates_all[-1].isoformat(), years_between(dates_all[0], dates_all[-1])))
    print("")
    inv_rows = []
    sset = set(dates_all)
    for sym in ALL_PRICE_SYMBOLS + ALL_OTHER_SYMBOLS:
        s = universe.get(sym)
        if s is None:
            inv_rows.append([sym, "MISSING", "", "", "", ""])
            continue
        span = [d for d in dates_all if s.dates[0] <= d <= s.dates[-1]]
        have = set(s.dates)
        miss = sum(1 for d in span if d not in have)
        inv_rows.append([sym, len(s.dates), s.dates[0].isoformat(),
                         s.dates[-1].isoformat(),
                         ("%.1f%%" % (100.0 * miss / len(span))) if span else "-",
                         s.provenance[1].split("symbol=")[-1].split()[0]
                         if len(s.provenance) > 1 else ""])
    print("\n".join(table(["symbol", "rows", "first", "last",
                           "no-PRINT on book cal", "source symbol"], inv_rows)))
    print("")
    print("  SYMBOLS THAT FAILED TO RESOLVE (recorded, never substituted):")
    for line in [
        "AMEX:SHY    -> error: invalid symbol            "
        "=> resolved instead as NASDAQ:SHY   (same fund, different exchange code)",
        "AMEX:TLT    -> error: invalid symbol            "
        "=> resolved instead as NASDAQ:TLT",
        "AMEX:EMB    -> error: invalid symbol            "
        "=> resolved instead as NASDAQ:EMB",
        "AMEX:TLH    -> resolved.  AMEX:SHY/EMB/TLT were retried on NASDAQ and "
        "succeeded; the prices are the same fund, but the exchange code differs, "
        "so the provenance records which one was actually used.",
    ]:
        print("    " + line)
    if missing:
        print("    also absent from disk: %s" % ",".join(missing))
    print("")
    print("  Cross-check against the sibling studies' independent pulls on the "
          "same date -- run separately by verify_sources.py.")

    # ---- cash -----------------------------------------------------------
    hdr("CASH PROXY -- a yield index, handled explicitly")
    cash_full = Cash(dates_all, universe["US03M"])
    cd = cash_full.diagnostics()
    print("  source: TVC:US03M, the 3-month US Treasury bill YIELD in percent "
          "per annum")
    print("  accrual: r_j = (yield at the close of the PREVIOUS book date / 100) "
          "/ 252")
    for k in ["n_days", "printed", "carried_forward", "carried_pct",
              "longest_gap_days", "no_rate_days", "rate_min", "rate_max",
              "rate_mean", "negative_rate_days", "zero_return_days"]:
        v = cd[k]
        if k == "carried_pct":
            print("  %-20s %s" % (k, pct(v)))
        elif k in ("rate_min", "rate_max", "rate_mean"):
            print("  %-20s %.4f%% p.a." % (k, v))
        else:
            print("  %-20s %s" % (k, v))
    print("")
    cagr_cash = None
    cash_curve = equity_curve(cash_full.ret)
    yrs = years_between(dates_all[0], dates_all[-1])
    cagr_cash = cash_curve[-1] ** (1.0 / yrs) - 1.0
    print("  cash CAGR over the window (upper bound): %.4f%%/yr" % (100 * cagr_cash))
    print("  days on which the CASH itself was negative: %d of %d (%.2f%%)"
          % (sum(1 for r in cash_full.ret[1:] if r < 0), len(cash_full.ret) - 1,
             100.0 * sum(1 for r in cash_full.ret[1:] if r < 0)
             / (len(cash_full.ret) - 1)))
    bil = bil_cross_check(dates_all, universe["BIL"])
    bil_curve = equity_curve(bil)
    bil_start = [d for d in dates_all if d >= universe["BIL"].dates[0]][0]
    print("  BIL price-only cross-check: %.4f%%/yr over %s..%s -- shown to "
          "demonstrate that a T-bill ETF's PRICE is not its return (the yield is "
          "distributed away), so BIL cannot be used as the cash series."
          % (100 * (bil_curve[-1] ** (1.0 / years_between(bil_start,
                                                         dates_all[-1])) - 1.0),
             bil_start.isoformat(), dates_all[-1].isoformat()))
    return run_engine(dates_all, universe, cash_full)

# ===========================================================================
# The engine proper
# ===========================================================================

def build_window(universe, start):
    """(dates, {mode: {sym: Aligned}}, Cash) for the SPY sessions >= start."""
    spy = universe["SPY"]
    dates = [d for d in spy.dates if d >= start]
    cash = Cash(dates, universe["US03M"])
    A = {}
    for mode, div in (("price", False), ("div", True)):
        A[mode] = {}
        for sym in ALL_PRICE_SYMBOLS:
            A[mode][sym] = Aligned(universe[sym], dates, VOL_WINDOW, SMA_TREND,
                                   DIV_YIELD_EST.get(sym, 0.0) if div else 0.0)
    return dates, A, cash


def blend_sleeves(a, b, w, tag):
    """w*a + (1-w)*b, on gross returns and on turnover separately."""
    out = SleeveResult(tag, a.dates)
    for j in range(len(a.dates)):
        out.gross[j] = w * a.gross[j] + (1.0 - w) * b.gross[j]
        out.turnover[j] = w * a.turnover[j] + (1.0 - w) * b.turnover[j]
    out.meta["blend"] = "%s %.2f + %s %.2f" % (a.name, w, b.name, 1.0 - w)
    return out


def build_sleeves(dates, A, cash, universe, tag_suffix=""):
    """Every pre-registered sleeve, plus the declared sensitivities."""
    starts = month_start_indices(dates)
    S = {}
    S["T"] = sleeve_T(dates, starts, A, cash, TREND_UNIVERSE)
    S["C"] = sleeve_C(dates, starts, A, cash, tag="C")
    S["C_hyg"] = sleeve_C(dates, starts, A, cash, tag="C_hyg", hyg_only=True)
    S["V"] = sleeve_V(dates, starts, universe["SPY"], universe["VIX"], cash,
                      VRP_SKEW_SHORT, VRP_SKEW_LONG, tag="V")
    for s in VRP_SKEW_SENSITIVITIES:
        if s == VRP_SKEW_SHORT:
            continue
        S["V_s%g" % s] = sleeve_V(dates, starts, universe["SPY"], universe["VIX"],
                                  cash, s, 2.0 * s, tag="V_s%g" % s)
    S["H_a"] = sleeve_H_a(dates, starts, A, cash, universe["VIX"])
    S["H_b"] = sleeve_H_b(dates, starts, universe["SPY"], universe["VIX"], cash)
    S["H"] = blend_sleeves(S["H_a"], S["H_b"], HEDGE_BLEND, "H")
    S["X"] = sleeve_X(dates, starts, A, cash, TREND_UNIVERSE, XSEC_N,
                      XSEC_LOOKBACK_DAYS, tag="X")
    S["X%d" % XSEC_N_SENSITIVITY] = sleeve_X(
        dates, starts, A, cash, TREND_UNIVERSE, XSEC_N_SENSITIVITY,
        XSEC_LOOKBACK_DAYS)
    S["B"] = sleeve_B(dates, A, BASELINE, tag="B")
    return S



def mrow(name, m):
    return [name,
            pct(m["cagr"]),
            pct(m["max_dd"]),
            num(m["sharpe_excess"], 2),
            ("%.1f%%" % (100 * m["ann_vol"])) if m["ann_vol"] is not NA else "n/a",
            "%d/%d" % (m["n_pos_years"], m["n_years"]),
            pct(m["pos_Y"]),
            pct(m["pos_Q"]),
            pct(m["pos_M"]),
            "%s %s" % (pct(m["worst_year"]), m["worst_year_label"]),
            pct(m["worst_month"]),
            pct(m["worst_r12"]),
            pct(m["worst_r36"])]


METRIC_HEAD = ["", "CAGR", "maxDD", "Sharpe", "annvol", "pos yrs",
               "pos Y", "pos Q", "pos M", "worst yr", "worst mo",
               "worst 12m", "worst 36m"]


def run_engine(dates_all, universe, cash_full):
    dates, A, cash = build_window(universe, WINDOW_START)
    print("")
    print("  book calendar: %d sessions, %s .. %s (%.2f years)"
          % (len(dates), dates[0].isoformat(), dates[-1].isoformat(),
             years_between(dates[0], dates[-1])))
    print("  cash diagnostics on this window:")
    cd = cash.diagnostics()
    for k in ["n_days", "carried_forward", "carried_pct", "longest_gap_days",
              "rate_min", "rate_max", "negative_rate_days"]:
        v = cd[k]
        print("    %-20s %s" % (k, pct(v) if k == "carried_pct" else
                                ("%.4f%%" % v if k in ("rate_min", "rate_max")
                                 else v)))

    SLEEVES = {}
    for mode in ("price", "div"):
        SLEEVES[mode] = build_sleeves(dates, A[mode], cash, universe)

    NET = {}
    for mode in ("price", "div"):
        for cst in COST_LEVELS_BPS:
            NET[(mode, cst)] = dict(
                (k, SLEEVES[mode][k].net(cst)) for k in SLEEVES[mode])

    # ---- sleeve metrics -------------------------------------------------
    hdr("SLEEVE METRICS -- dividend-adjusted and price-only, at %g bps "
        "round-trip" % REFERENCE_COST_BPS)
    names = ["T", "C", "C_hyg", "V", "H_a", "H_b", "H", "X", "B"]
    for mode in ("div", "price"):
        print("")
        print("  --- %s ---" % ("DIVIDEND-ADJUSTED [ESTIMATED]"
                                if mode == "div" else "PRICE-ONLY (as measured)"))
        rows = []
        MET = {}
        for n in names:
            r = NET[(mode, REFERENCE_COST_BPS)][n]
            m = metrics(dates, r, cash.ret)
            MET[n] = m
            rows.append(mrow(n, m))
        m = metrics(dates, cash.ret, cash.ret)
        MET["CASH"] = m
        rows.append(mrow("CASH", m))
        m = metrics(dates, apply_lambda(NET[(mode, REFERENCE_COST_BPS)]["B"],
                                        cash.ret, 0.0), cash.ret)
        rows.append(mrow("CASHx(lam=0)", m))
        print("\n".join(table(METRIC_HEAD, rows, indent="  ")))

    # ---- cost x dividend grid -------------------------------------------
    hdr("COST AND DIVIDEND GRID -- CAGR% / Sharpe(excess) per sleeve")
    rows = []
    for n in names + ["CASH"]:
        row = [n]
        for mode in ("price", "div"):
            for cst in COST_LEVELS_BPS:
                r = (cash.ret if n == "CASH"
                     else NET[(mode, cst)][n])
                m = metrics(dates, r, cash.ret)
                row.append("%s / %s" % (pct(m["cagr"]), num(m["sharpe_excess"], 2)))
        rows.append(row)
    h = ["sleeve"]
    for mode in ("price", "div"):
        for cst in COST_LEVELS_BPS:
            h.append("%s %gbps" % (mode, cst))
    print("\n".join(table(h, rows, indent="  ")))
    print("")
    print("  cost drag (CAGR lost from 0 -> %g bps round trip, "
          "dividend-adjusted):" % COST_LEVELS_BPS[-1])
    drag_rows = []
    for n in names:
        c0 = metrics(dates, NET[("div", 0.0)][n], cash.ret)["cagr"]
        c5 = metrics(dates, NET[("div", 5.0)][n], cash.ret)["cagr"]
        c20 = metrics(dates, NET[("div", 20.0)][n], cash.ret)["cagr"]
        drag_rows.append([n, pct(c0), pct(c5), pct(c20),
                          "%.3f pp" % (100 * (c0 - c5)),
                          "%.3f pp" % (100 * (c0 - c20))])
    print("\n".join(table(["sleeve", "CAGR 0bps", "CAGR 5bps", "CAGR 20bps",
                           "drag@5", "drag@20"], drag_rows, indent="  ")))

    # ---- the books ------------------------------------------------------
    hdr("THE BOOKS -- fixed pre-registered sleeve weights")
    print("  BOOK      : " + " + ".join("%s %.2f" % (k, v) for k, v in
                                        sorted(BOOK_WEIGHTS.items())))
    print("  BOOK-NOV  : " + " + ".join("%s %.2f" % (k, v) for k, v in
                                        sorted(BOOK_NOV_WEIGHTS.items())))
    print("  BOOK-VT   : the same BOOK weights passed through ONE uniform, "
          "declared normalisation -- every sleeve scaled by")
    print("              k = min(1, %.0f%% / its own annualised vol), released "
          "weight to CASH.  Not searched, not sleeve-specific."
          % (100 * VOL_TARGET))

    BOOKS = {}
    VT_WEIGHTS = {}
    for mode in ("price", "div"):
        for cst in COST_LEVELS_BPS:
            for bname in BOOK_NAMES:
                src, w = book_source(bname, mode, cst, NET, cash, dates)
                if bname == "BOOK-VT" and mode == "div":
                    VT_WEIGHTS[cst] = dict(w)
                BOOKS[(bname, mode, cst)] = simulate_book(dates, src, w, cst)

    hdr("BOOK METRICS -- every cost level, both dividend treatments")
    rows = []
    BMET = {}
    for bname in BOOK_NAMES:
        for mode in ("div", "price"):
            for cst in COST_LEVELS_BPS:
                br = BOOKS[(bname, mode, cst)]
                m = metrics(dates, br.rets, cash.ret)
                BMET[(bname, mode, cst)] = m
                rows.append(["%s %s %gbps" % (bname, mode, cst)]
                            + mrow("", m)[1:])
    brb = BOOKS[("BOOK", "div", REFERENCE_COST_BPS)]
    m = metrics(dates, NET[("div", REFERENCE_COST_BPS)]["B"], cash.ret)
    rows.append(["B (SPY buy&hold) div"] + mrow("", m)[1:])
    m = metrics(dates, NET[("price", REFERENCE_COST_BPS)]["B"], cash.ret)
    rows.append(["B (SPY buy&hold) price"] + mrow("", m)[1:])
    m = metrics(dates, cash.ret, cash.ret)
    rows.append(["CASH"] + mrow("", m)[1:])
    print("\n".join(table(METRIC_HEAD, rows, indent="  ")))
    print("")
    print("  BOOK-VT resolved weights at %g bps (dividend-adjusted): %s"
          % (REFERENCE_COST_BPS,
             "  ".join("%s=%.4f" % (k, VT_WEIGHTS[REFERENCE_COST_BPS][k])
                       for k in sorted(VT_WEIGHTS[REFERENCE_COST_BPS]))))
    print("  sleeve vol-scaling k = min(1, %.0f%%/vol):"
          % (100 * VOL_TARGET))
    for k in ["T", "X", "C", "V", "H"]:
        ls = level_stats(dates, NET[("div", REFERENCE_COST_BPS)][k])
        print("    %-4s vol %5.2f%%  k=%.4f" % (k, 100 * ls["ann_vol"],
                                                vol_scale(dates,
                                                          NET[("div",
                                                               REFERENCE_COST_BPS)][k])))

    # ---- positivity by horizon -----------------------------------------
    hdr("POSITIVITY BY HORIZON -- fraction of complete periods with a POSITIVE "
        "compounded return")
    rows = []
    for bname in BOOK_NAMES:
        for mode in ("div", "price"):
            for cst in COST_LEVELS_BPS:
                m = BMET[(bname, mode, cst)]
                label = "%s %s %gbps" % (bname, mode, cst)
                row = [label]
                for b in BUCKETS:
                    row.append("%s (%d/%d)"
                               % (pct(m["pos_" + b]),
                                  int(round(m["pos_" + b] * m["n_" + b])),
                                  m["n_" + b]))
                rows.append(row)
    for label, r in [("T div 5bps", NET[("div", 5.0)]["T"]),
                     ("B SPY div 5bps", NET[("div", 5.0)]["B"]),
                     ("CASH", cash.ret)]:
        m = metrics(dates, r, cash.ret)
        row = [label]
        for b in BUCKETS:
            row.append("%s (%d/%d)" % (pct(m["pos_" + b]),
                                       int(round(m["pos_" + b] * m["n_" + b])),
                                       m["n_" + b]))
        rows.append(row)
    print("\n".join(table(["series"] + BUCKETS, rows, indent="  ")))
    print("")
    print("  A flat period counts as NOT positive (strict reading).  The loose "
          "reading (a loss is the only failure) is in the CSVs.")

    # ---- lambda frontier ------------------------------------------------
    hdr("LAMBDA FRONTIER -- scaling exposure against cash")
    print("  r = lam * book + (1 - lam) * cash.  lam is the fraction of capital "
          "at risk.")
    frontier_rows = []
    FRONT = {}
    for bname in BOOK_NAMES:
        for mode in ("div", "price"):
            risky = BOOKS[(bname, mode, REFERENCE_COST_BPS)].rets
            scan = frontier_scan(dates, risky, cash.ret, LAMBDA_STEP)
            FRONT[(bname, mode)] = scan
            y = largest_lambda_all_positive(scan, "pos_Y")
            q = largest_lambda_all_positive(scan, "pos_Q")
            mo = largest_lambda_all_positive(scan, "pos_M")
            frontier_rows.append([
                "%s %s" % (bname, mode),
                "%s (%s)" % (num(y["lam"], 3) if y else "none",
                             pct(y["cagr"]) if y else "n/a"),
                "%s (%s)" % (num(q["lam"], 3) if q else "none",
                             pct(q["cagr"]) if q else "n/a"),
                "%s (%s)" % (num(mo["lam"], 3) if mo else "none",
                             pct(mo["cagr"]) if mo else "n/a"),
                "%.4f" % LAMBDA_STEP])
    print("\n".join(table(["book", "largest lam with 100% positive YEARS "
                           "(CAGR there)", "100% positive QUARTERS (CAGR)",
                           "100% positive MONTHS (CAGR)", "lam resolution"],
                          frontier_rows, indent="  ")))
    print("")
    print("  frontier in detail (lam, CAGR, posY, posQ, posM):")
    for bname in ("BOOK",):
        scan = FRONT[(bname, "div")]
        picks = [0.0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.10, 0.20, 0.35,
                 0.50, 0.75, 1.0]
        rows = []
        for lam in picks:
            row = min(scan, key=lambda r: abs(r["lam"] - lam))
            rows.append([num(row["lam"], 3), pct(row["cagr"]),
                         num(row["sharpe"], 2), pct(row["pos_Y"]),
                         "%d/%d" % (row["Y_pos"], row["Y_n"]),
                         pct(row["pos_Q"]), pct(row["pos_M"]),
                         pct(row["max_dd"])])
        print("\n".join(table(["lam", "CAGR", "Sharpe", "posY", "Y pos",
                               "posQ", "posM", "maxDD"], rows, indent="    ")))

    # ---- regime grid ----------------------------------------------------
    hdr("REGIME GRID -- trend state x realised-vol tercile, on the MONTHLY book "
        "return")
    sc, ss, sv = spy_trend_vol(dates, universe["SPY"])
    print("  trend state  : SPY close > SPY SMA(%d), read at the PREVIOUS "
          "month-end" % SMA_TREND)
    print("  vol terciles : trailing 20-day realised SPY vol read at the "
          "PREVIOUS month-end")
    reg_rows = []
    REG = {}
    for bname in BOOK_NAMES:
        for mode in ("div",):
            br = BOOKS[(bname, mode, REFERENCE_COST_BPS)]
            cells, brk = regime_cells(dates, br.rets, sc, ss, sv, None)
            REG[(bname, mode)] = cells
            print("")
            print("  %s -- tercile breakpoints (annualised vol): %.4f / %.4f"
                  % (bname, 100 * brk[0] if len(brk) > 1 else -1,
                     100 * brk[1] if len(brk) > 1 else -1))
            rows = []
            neg = 0
            for state in ("UP", "DOWN"):
                for tier in ("LOW", "MID", "HIGH"):
                    c = cells.get((state, tier))
                    if c is None or c["n"] == 0:
                        rows.append([state, tier, 0, "n/a", "n/a"])
                        continue
                    mean = c["sum"] / c["n"]
                    if mean <= 0.0:
                        neg += 1
                    rows.append([state, tier, c["n"], pct(mean),
                                 pct(c["pos"] / float(c["n"]))])
            print("\n".join(table(["trend", "vol", "months",
                                   "mean monthly", "frac positive"],
                                  rows, indent="    ")))
            print("    NEGATIVE CELLS: %d of 6" % neg)
            reg_rows.append("%s: %d/6 negative" % (bname, neg))
    print("")
    for line in reg_rows:
        print("  " + line)

    # ---- correlations ---------------------------------------------------
    hdr("CORRELATION MATRIX OF YEARLY RETURNS -- the key output")
    yearmaps = {}
    for n in ["T", "C", "V", "H_a", "H_b", "H", "X", "B"]:
        yearmaps[n] = yearly_return_map(dates, NET[("div", REFERENCE_COST_BPS)][n])
    for bname in BOOK_NAMES:
        yearmaps[bname] = yearly_return_map(
            dates, BOOKS[(bname, "div", REFERENCE_COST_BPS)].rets)
    yearmaps["CASH"] = yearly_return_map(dates, cash.ret)
    cm_names = ["T", "C", "V", "H_a", "H_b", "H", "X", "B", "BOOK", "BOOK-NOV",
                "BOOK-VT", "CASH"]
    CM = corr_matrix(cm_names, yearmaps)
    print("")
    print("  years used: %s" % ",".join(sorted(yearmaps["BOOK"])))
    rows = []
    for a in cm_names:
        rows.append([a] + [num(CM[(a, b)], 2) for b in cm_names])
    print("\n".join(table([""] + cm_names, rows, indent="  ")))
    problems = corr_check(CM, cm_names)
    print("")
    print("  symmetry + unit-diagonal check: %s"
          % ("PASS (symmetric, diagonal exactly 1.0)" if not problems
             else "FAIL: " + "; ".join(problems[:5])))
    print("")
    print("  pairwise correlations with the BOOK, lowest first (the whole point "
          "of the exercise):")
    pr = sorted(((CM[("BOOK", n)], n) for n in cm_names if n != "BOOK"),
                key=lambda t: (t[0] is NA, t[0]))
    for v, n in pr:
        print("    %-9s %s" % (n, num(v, 3)))
    print("")
    print("  HOW MANY INDEPENDENT BETS IS THE BOOK ACTUALLY?")
    print("  for n sleeves with mean pairwise yearly correlation rho_bar, the"
          " effective count is n / (1 + (n-1) * rho_bar)")
    for group, label in [(["T", "C", "V", "H", "X"], "the 5 sleeves of BOOK"),
                         (["T", "X"], "T and X"),
                         (["T", "C", "V", "H", "X", "B"],
                          "the 5 sleeves plus SPY buy&hold")]:
        pairs = [(a, b) for i, a in enumerate(group) for b in group[i + 1:]]
        vals = [CM[(a, b)] for a, b in pairs]
        vals = [v for v in vals if v is not NA]
        rho = sum(vals) / len(vals) if vals else 0.0
        n = len(group)
        eff = n / (1.0 + (n - 1) * rho) if rho > -1.0 / (n - 1) else float("inf")
        print("    %-28s n=%d  mean rho=%+.3f  independent bets ~ %.2f"
              % (label, n, rho, eff))
    print("    (the predecessor's SPY/QQQ/IWM measurement was 0.875 yearly -> "
          "1.12 bets; a 14-name equity basket gave 2.53)")

    # ---- cross-sectional momentum N sensitivity -------------------------
    hdr("DECLARED SENSITIVITIES -- not used anywhere in the books")
    rows = []
    for nm in ["X", "X%d" % XSEC_N_SENSITIVITY]:
        for mode in ("div", "price"):
            m = metrics(dates, NET[(mode, REFERENCE_COST_BPS)][nm], cash.ret)
            rows.append([nm, mode] + mrow("", m)[1:])
    for nm in [k for k in SLEEVES["div"] if k.startswith("V_s")]:
        m = metrics(dates, NET[("div", REFERENCE_COST_BPS)][nm], cash.ret)
        rows.append([nm, "div"] + mrow("", m)[1:])
    m = metrics(dates, NET[("div", REFERENCE_COST_BPS)]["V"], cash.ret)
    rows.append(["V (base)", "div"] + mrow("", m)[1:])
    m = metrics(dates, NET[("div", REFERENCE_COST_BPS)]["C_hyg"], cash.ret)
    rows.append(["C_hyg", "div"] + mrow("", m)[1:])
    m = metrics(dates, NET[("div", REFERENCE_COST_BPS)]["C"], cash.ret)
    rows.append(["C (pair)", "div"] + mrow("", m)[1:])
    print("\n".join(table(["variant", "mode"] + METRIC_HEAD[1:], rows,
                          indent="  ")))
    print("")
    print("  V sleeve internals:")
    vm = SLEEVES["div"]["V"].meta
    for k in ["rolls", "mean_credit_pct_of_width", "min_credit_pct_of_width",
              "max_credit_pct_of_width", "skew_short_volpts"]:
        print("    %-30s %s" % (k, num(vm[k], 4) if not isinstance(vm[k], str)
                                else vm[k]))
    hm = SLEEVES["div"]["H_b"].meta
    print("  H_b sleeve internals [MODELED]:")
    for k in ["rolls", "premium_spent_total", "premium_spent_per_yr",
              "payoffs_total", "ending_value"]:
        print("    %-30s %s" % (k, num(hm[k], 4)))
    print("  H_a sleeve internals:")
    print("    %-30s %d of %d months long"
          % ("months_long", SLEEVES["div"]["H_a"].meta["months_long"],
             SLEEVES["div"]["H_a"].meta["rebalances"]))
    print("  T sleeve internals:")
    print("    mean instruments live per rebalance: %s"
          % num(SLEEVES["div"]["T"].meta["mean_live_instruments"], 2))
    print("  X sleeve last month's picks: %s"
          % SLEEVES["div"]["X"].meta["last_picks"])

    # ---- reduced long-window book ---------------------------------------
    hdr("REDUCED LONG-WINDOW BOOK -- covering the 2000-2002 dot-com bear")
    rdates, rA, rcash = build_window(universe, REDUCED_START)
    reduced_univ = []
    for s in ALL_PRICE_SYMBOLS:
        if s == "BIL":
            continue
        if universe[s].index_of.get(REDUCED_START) is not None:
            reduced_univ.append(s)
    print("  window: %s .. %s (%.2f years)"
          % (rdates[0].isoformat(), rdates[-1].isoformat(),
             years_between(rdates[0], rdates[-1])))
    print("  EXISTENCE screen -- instruments with a print on %s : %d"
          % (REDUCED_START.isoformat(), len(reduced_univ)))
    print("    %s" % ",".join(reduced_univ))
    print("  instruments NOT present at that date (so absent from this book "
          "until they list): %s"
          % ",".join(s for s in ALL_PRICE_SYMBOLS
                     if s != "BIL" and s not in reduced_univ))
    print("  CARRY weight is set to 0.00 in this book because neither %s nor %s "
          "lists before 2002/2007; that capital earns cash instead."
          % (CARRY_LONG, CARRY_SHORT))
    print("  BOND10M [MODELED] supplies the duration leg: r = -%.1f * dy10 + "
          "y10/252" % BOND10M_MODIFIED_DURATION)

    rS = {}
    rNET = {}
    for mode in ("price", "div"):
        starts_r = month_start_indices(rdates)
        S = {}
        S["T"] = sleeve_T(rdates, starts_r, rA[mode], rcash, reduced_univ)
        S["X"] = sleeve_X(rdates, starts_r, rA[mode], rcash, reduced_univ,
                          XSEC_N, XSEC_LOOKBACK_DAYS)
        S["V"] = sleeve_V(rdates, starts_r, universe["SPY"], universe["VIX"],
                          rcash, VRP_SKEW_SHORT, VRP_SKEW_LONG)
        S["H_a"] = sleeve_H_a(rdates, starts_r, rA[mode], rcash, universe["VIX"])
        S["H_b"] = sleeve_H_b(rdates, starts_r, universe["SPY"], universe["VIX"],
                              rcash)
        S["H"] = blend_sleeves(S["H_a"], S["H_b"], HEDGE_BLEND, "H")
        S["BOND10M"] = sleeve_bond10m(rdates, universe["US10Y"])
        S["B"] = sleeve_B(rdates, rA[mode], BASELINE)
        rS[mode] = S
        rNET[mode] = dict((k, S[k].net(REFERENCE_COST_BPS)) for k in S)
        for cst in COST_LEVELS_BPS:
            rNET[(mode, cst)] = dict((k, S[k].net(cst)) for k in S)
    rNET[("div", 5.0)] = rNET[("div", REFERENCE_COST_BPS)]

    rrows = []
    rBMET = {}
    for mode in ("div", "price"):
        for cst in COST_LEVELS_BPS:
            src = dict(rNET[(mode, cst)])
            src["CASH"] = rcash.ret
            br = simulate_book(rdates, src, REDUCED_BOOK_WEIGHTS, cst)
            m = metrics(rdates, br.rets, rcash.ret)
            rBMET[(mode, cst)] = m
            rrows.append(["REDUCED %s %gbps" % (mode, cst)] + mrow("", m)[1:])
    m = metrics(rdates, rNET[("div", REFERENCE_COST_BPS)]["B"], rcash.ret)
    rrows.append(["B (SPY buy&hold) div"] + mrow("", m)[1:])
    m = metrics(rdates, rNET[("price", REFERENCE_COST_BPS)]["B"], rcash.ret)
    rrows.append(["B (SPY buy&hold) price"] + mrow("", m)[1:])
    print("")
    print("\n".join(table(METRIC_HEAD, rrows, indent="  ")))

    src = dict(rNET[("div", REFERENCE_COST_BPS)])
    src["CASH"] = rcash.ret
    rbook = simulate_book(rdates, src, REDUCED_BOOK_WEIGHTS,
                          REFERENCE_COST_BPS)
    hdr("REDUCED LONG-WINDOW BOOK -- year by year (dividend-adjusted, %g bps)"
        % REFERENCE_COST_BPS)
    ygroups_r = group_index(rdates, "Y", complete_only=True)
    ry = {}
    ry["REDUCED BOOK"] = period_returns(rbook.rets, ygroups_r)
    for n in ["T", "X", "V", "H_a", "H_b", "H", "BOND10M", "B"]:
        ry[n] = period_returns(rNET[("div", REFERENCE_COST_BPS)][n], ygroups_r)
    ry["CASH"] = period_returns(rcash.ret, ygroups_r)
    order = ["REDUCED BOOK", "T", "X", "V", "H_a", "H_b", "H", "BOND10M", "B",
             "CASH"]
    ylabels = [p["label"] for p in ry["REDUCED BOOK"]]
    rows = []
    for i, lbl in enumerate(ylabels):
        rows.append([lbl] + [pct(ry[n][i]["ret"]) for n in order])
    print("\n".join(table(["year"] + order, rows, indent="  ")))
    print("")
    print("  dot-com bear years inside this window: 2000, 2001, 2002 "
          "(all three are complete years here)")
    print("  the reduced book's worst year: %s %s; losing years: %s"
          % (pct(rBMET[("div", REFERENCE_COST_BPS)]["worst_year"]),
             rBMET[("div", REFERENCE_COST_BPS)]["worst_year_label"],
             ",".join(rBMET[("div", REFERENCE_COST_BPS)]["losing_years"]) or "none"))

    rym = {}
    for n in ["T", "X", "V", "H_a", "H_b", "H", "BOND10M", "B"]:
        rym[n] = yearly_return_map(rdates, rNET[("div", REFERENCE_COST_BPS)][n])
    rym["REDUCED"] = yearly_return_map(rdates, rbook.rets)
    rym["CASH"] = yearly_return_map(rdates, rcash.ret)
    rnames = ["T", "X", "V", "H_a", "H_b", "H", "BOND10M", "B", "REDUCED",
              "CASH"]
    RCM = corr_matrix(rnames, rym)
    print("")
    print("  correlation matrix of YEARLY returns over the reduced window "
          "(%d complete years: %s)"
          % (len(rym["REDUCED"]), ",".join(sorted(rym["REDUCED"]))))
    rows = []
    for a in rnames:
        rows.append([a] + [num(RCM[(a, b)], 2) for b in rnames])
    print("\n".join(table([""] + rnames, rows, indent="  ")))
    rproblems = corr_check(RCM, rnames)
    print("  symmetry + unit-diagonal check: %s"
          % ("PASS" if not rproblems else "FAIL: " + "; ".join(rproblems[:3])))
    rr = sorted(((RCM[("REDUCED", n)], n) for n in rnames if n != "REDUCED"),
                key=lambda t: (t[0] is NA, t[0]))
    print("  pairwise correlation with the REDUCED book, lowest first:")
    for v, n in rr:
        print("    %-9s %s" % (n, num(v, 3)))
    write_csv(os.path.join(OUT_DIR, "corr_yearly_reduced.csv"),
              ["study=weather-deep-test study.py",
               "table=Pearson correlation of YEARLY returns over the REDUCED "
               "long-window book window",
               "window=%s..%s" % (rdates[0].isoformat(), rdates[-1].isoformat()),
               "pull_date=2026-10-14",
               "dividends=constant [ESTIMATED] yields",
               "cash=TVC:US03M yield index accrued at yield/252, UPPER BOUND"],
              [""] + rnames,
              [[a] + ["%.10f" % RCM[(a, b)] for b in rnames] for a in rnames])

    # ---- success bar ----------------------------------------------------
    hdr("THE PRE-REGISTERED SUCCESS BAR -- declared before the run, reported "
        "honestly")
    print("  bar: >=%.0f%% of years positive AND >=%.0f%% of quarters positive "
          "AND Sharpe > %.1f AND CAGR above cash"
          % (100 * SUCCESS_BAR["years"], 100 * SUCCESS_BAR["quarters"],
             SUCCESS_BAR["sharpe"]))
    print("")
    cash_cagr = metrics(dates, cash.ret, cash.ret)["cagr"]
    verdict_rows = []
    clears = []
    for bname in BOOK_NAMES:
        for mode in ("div", "price"):
            for cst in COST_LEVELS_BPS:
                m = BMET[(bname, mode, cst)]
                ok_y = m["pos_Y"] >= SUCCESS_BAR["years"] - 1e-12
                ok_q = m["pos_Q"] >= SUCCESS_BAR["quarters"] - 1e-12
                ok_s = (m["sharpe_excess"] is not NA
                        and m["sharpe_excess"] > SUCCESS_BAR["sharpe"])
                ok_c = m["cagr"] > cash_cagr
                passed = ok_y and ok_q and ok_s and ok_c
                if passed:
                    clears.append("%s %s %gbps" % (bname, mode, cst))
                verdict_rows.append(["%s %s %gbps" % (bname, mode, cst),
                                     "Y" if ok_y else "n", "Y" if ok_q else "n",
                                     "Y" if ok_s else "n", "Y" if ok_c else "n",
                                     "PASS" if passed else "fail",
                                     pct(m["pos_Y"]), pct(m["pos_Q"]),
                                     num(m["sharpe_excess"], 2),
                                     pct(m["cagr"])])
    for mode in ("div", "price"):
        for cst in COST_LEVELS_BPS:
            m = rBMET[(mode, cst)]
            ok_y = m["pos_Y"] >= SUCCESS_BAR["years"] - 1e-12
            ok_q = m["pos_Q"] >= SUCCESS_BAR["quarters"] - 1e-12
            ok_s = (m["sharpe_excess"] is not NA
                    and m["sharpe_excess"] > SUCCESS_BAR["sharpe"])
            ok_c = m["cagr"] > cash_cagr
            passed = ok_y and ok_q and ok_s and ok_c
            if passed:
                clears.append("REDUCED %s %gbps" % (mode, cst))
            verdict_rows.append(["REDUCED %s %gbps" % (mode, cst),
                                 "Y" if ok_y else "n", "Y" if ok_q else "n",
                                 "Y" if ok_s else "n", "Y" if ok_c else "n",
                                 "PASS" if passed else "fail",
                                 pct(m["pos_Y"]), pct(m["pos_Q"]),
                                 num(m["sharpe_excess"], 2), pct(m["cagr"])])
    print("\n".join(table(["book", "posY>=90", "posQ>=75", "S>0.8",
                           "CAGR>cash", "verdict", "posY", "posQ", "Sharpe",
                           "CAGR"], verdict_rows, indent="  ")))
    print("")
    if clears:
        print("  VERDICT: %d configuration(s) clear the bar: %s"
              % (len(clears), "; ".join(clears)))
    else:
        print("  VERDICT: NOTHING CLEARS THE BAR.  No book, at any cost level, "
              "in either dividend treatment, is simultaneously positive in >=90% "
              "of years, positive in >=75% of quarters, Sharpe > 0.8 and above "
              "cash.")
        best = max(verdict_rows, key=lambda r: (r[1] == "Y", r[2] == "Y"))
        print("  the closest cell above: %s" % best[0])

    # ---- best point on the trade-off ------------------------------------
    hdr("BEST POINT ACTUALLY ACHIEVED ON THE RETURN-vs-POSITIVITY TRADE-OFF")
    scan = FRONT[("BOOK", "div")]
    print("  BOOK, dividend-adjusted, %g bps, lam scan (lam = fraction at risk):"
          % REFERENCE_COST_BPS)
    cand = [r for r in scan if r["pos_Y"] is not NA]
    allpos = [r for r in cand if r["pos_Y"] >= 1.0 - 1e-12]
    if allpos:
        b = max(allpos, key=lambda r: r["cagr"])
        print("  highest CAGR with 100%% of YEARS positive: lam=%.3f  CAGR %s"
              % (b["lam"], pct(b["cagr"])))
    else:
        print("  highest CAGR with 100%% of YEARS positive: NONE -- there is no "
              "lam on the grid at which every year is positive")
    best90 = max((r for r in cand if r["pos_Y"] >= 0.90 - 1e-12),
                 key=lambda r: r["cagr"]) if any(
        r["pos_Y"] >= 0.90 - 1e-12 for r in cand) else None
    if best90:
        r = apply_lambda(BOOKS[("BOOK", "div", REFERENCE_COST_BPS)].rets,
                         cash.ret, best90["lam"])
        m = metrics(dates, r, cash.ret)
        print("")
        print("  BEST >=90%%-of-years point: lam = %.3f" % best90["lam"])
        print("    CAGR                       %s" % pct(m["cagr"]))
        print("    max drawdown               %s" % pct(m["max_dd"]))
        print("    Sharpe (excess of cash)    %s" % num(m["sharpe_excess"], 2))
        print("    years positive             %d/%d"
              % (m["n_pos_years"], m["n_years"]))
        print("    Losing years               %s"
              % (", ".join("%s %s" % (pct(p["ret"]), p["label"])
                           for p in m["years"] if p["ret"] <= 0.0) or "none"))
        print("    quarters positive          %s" % pct(m["pos_Q"]))
        print("    months positive            %s" % pct(m["pos_M"]))
        print("    worst month                %s (%s)"
              % (pct(m["worst_month"]), m["worst_month_label"]))
    print("")
    print("  full-scale (lam=1.0) BOOK, dividend-adjusted, %g bps:"
          % REFERENCE_COST_BPS)
    m = BMET[("BOOK", "div", REFERENCE_COST_BPS)]
    print("    CAGR %s, maxDD %s, Sharpe %s" % (pct(m["cagr"]), pct(m["max_dd"]),
                                               num(m["sharpe_excess"], 2)))
    print("    vs SPY buy&hold (div): CAGR %s"
          % pct(metrics(dates, NET[("div", REFERENCE_COST_BPS)]["B"],
                        cash.ret)["cagr"]))
    print("    Losing years: %s"
          % (", ".join("%s %s" % (pct(p["ret"]), p["label"])
                       for p in m["years"] if p["ret"] <= 0.0) or "none"))

    # ---- CSV outputs ----------------------------------------------------
    prov = [
        "study=weather-deep-test study.py",
        "window=%s..%s" % (dates[0].isoformat(), dates[-1].isoformat()),
        "pull_date=2026-10-14 (date of the MCP get_ohlcv pull behind data/)",
        "engine=../../timeframe-performance-statistics/scripts/timeframe_stats.py"
        " (bucket_key / sample_sd / max_drawdown imported)",
        "costs=0/5/20 bps round trip",
        "dividends=constant [ESTIMATED] yields, see README.md",
        "cash=TVC:US03M yield index accrued at yield/252, UPPER BOUND",
    ]

    def wm(path, extra_prov, headers, rows):
        write_csv(os.path.join(OUT_DIR, path), prov + extra_prov, headers, rows)

    mon_labels = [p["label"] for p in BMET[("BOOK", "div", 5.0)]["months"]]
    for mode in ("div", "price"):
        for cst in COST_LEVELS_BPS:
            h = ["month"] + names
            rows = []
            for i, lbl in enumerate(mon_labels):
                row = [lbl]
                for n in names:
                    row.append("%.10f" % month_end_curve(
                        dates, NET[(mode, cst)][n])[i]["ret"])
                rows.append(row)
            wm("sleeve_monthly_%s_%gbps.csv" % (mode, cst),
               ["table=monthly compounded sleeve returns, %s, %g bps round trip"
                % (mode, cst)], h, rows)
            h = ["date"] + names
            rows = []
            for j in range(len(dates)):
                rows.append([dates[j].isoformat()]
                            + ["%.10f" % NET[(mode, cst)][n][j] for n in names])
            wm("sleeve_daily_%s_%gbps.csv" % (mode, cst),
               ["table=daily net sleeve returns, %s, %g bps round trip"
                % (mode, cst)], h, rows)

    for mode in ("div", "price"):
        for cst in COST_LEVELS_BPS:
            h = ["date", "BOOK", "BOOK-NOV", "CASH"]
            rows = []
            for j, d in enumerate(dates):
                rows.append([d.isoformat(),
                             "%.10f" % BOOKS[("BOOK", mode, cst)].rets[j],
                             "%.10f" % BOOKS[("BOOK-NOV", mode, cst)].rets[j],
                             "%.10f" % cash.ret[j]])
            wm("book_daily_%s_%gbps.csv" % (mode, cst),
               ["table=daily net book returns, %s, %g bps round trip"
                % (mode, cst)], h, rows)
            brow = []
            for i, lbl in enumerate(mon_labels):
                brow.append([lbl,
                             "%.10f" % month_end_curve(
                                 dates, BOOKS[("BOOK", mode, cst)].rets)[i]["ret"],
                             "%.10f" % month_end_curve(
                                 dates,
                                 BOOKS[("BOOK-NOV", mode, cst)].rets)[i]["ret"]])
            wm("book_monthly_%s_%gbps.csv" % (mode, cst),
               ["table=monthly compounded book returns, %s, %g bps"
                % (mode, cst)], ["month", "BOOK", "BOOK-NOV"], brow)

    weights = BOOKS[("BOOK", "div", 5.0)].weights_log
    wm("book_weights.csv",
       ["table=BOOK sleeve weights at each monthly rebalance (fixed target)"],
       ["date"] + sorted(BOOK_WEIGHTS), [[d] + ["%.6f" % w[k]
                                                for k in sorted(BOOK_WEIGHTS)]
                                         for d, w in weights])

    yh = ["year"] + ["%s_div" % n for n in cm_names]
    yrows = []
    for lbl in sorted(yearmaps["BOOK"]):
        row = [lbl]
        for n in cm_names:
            row.append("%.10f" % yearmaps[n].get(lbl, float("nan")))
        yrows.append(row)
    wm("years.csv", ["table=yearly returns, dividend-adjusted, 5 bps"], yh, yrows)

    ch = [""] + cm_names
    crows = [[a] + ["%.10f" % CM[(a, b)] for b in cm_names] for a in cm_names]
    wm("corr_yearly.csv",
       ["table=Pearson correlation of YEARLY returns across %d complete years"
        % len(yearmaps["BOOK"])], ch, crows)

    hrows = []
    for bname in BOOK_NAMES:
        for mode in ("div", "price"):
            for cst in COST_LEVELS_BPS:
                m = BMET[(bname, mode, cst)]
                hrows.append(["%s_%s_%gbps" % (bname, mode, cst), "strict"]
                             + ["%.10f" % m["pos_" + b] for b in BUCKETS])
                hrows.append(["%s_%s_%gbps" % (bname, mode, cst), "loose"]
                             + ["%.10f" % m["pos_" + b + "_ge0"]
                                for b in BUCKETS])
    wm("horizon.csv", ["table=fraction of complete periods positive"],
       ["series", "reading"] + BUCKETS, hrows)

    lrows = []
    for bname in BOOK_NAMES:
        for mode in ("div", "price"):
            for r in FRONT[(bname, mode)]:
                lrows.append([bname, mode, "%.4f" % r["lam"],
                              "%.10f" % r["cagr"], "%.10f" % r["max_dd"],
                              fnum(r["sharpe"]), "%.10f" % r["pos_Y"],
                              "%.10f" % r["pos_Q"], "%.10f" % r["pos_M"]])
    wm("lambda_frontier.csv",
       ["table=lam grid: r = lam*book + (1-lam)*cash, 5 bps"],
       ["book", "mode", "lam", "cagr", "max_dd", "sharpe", "pos_Y", "pos_Q",
        "pos_M"], lrows)

    rrows2 = []
    for bname in BOOK_NAMES:
        cells = REG[(bname, "div")]
        for state in ("UP", "DOWN"):
            for tier in ("LOW", "MID", "HIGH"):
                c = cells.get((state, tier))
                if c is None:
                    rrows2.append([bname, state, tier, 0, "", "", ""])
                    continue
                rrows2.append([bname, state, tier, c["n"],
                               "%.10f" % (c["sum"] / c["n"]),
                               "%.10f" % (c["pos"] / float(c["n"])),
                               "%.10f" % (1.0 - c["pos"] / float(c["n"]))])
    wm("regime.csv",
       ["table=monthly book return by trend state x realised-vol tercile "
        "(dividend-adjusted, 5 bps); terciles are an IN-SAMPLE partition"],
       ["book", "trend_state", "vol_tercile", "months", "mean_monthly_return",
        "frac_positive", "frac_negative"], rrows2)

    srows = []
    for n in names + ["CASH"]:
        for mode in ("price", "div"):
            for cst in COST_LEVELS_BPS:
                r = cash.ret if n == "CASH" else NET[(mode, cst)][n]
                m = metrics(dates, r, cash.ret)
                srows.append(["sleeve", n, mode, "%g" % cst,
                              "%.10f" % m["cagr"], "%.10f" % m["max_dd"],
                              fnum(m["sharpe_excess"]),
                              "%.10f" % m["pos_Y"], "%.10f" % m["pos_Q"],
                              "%.10f" % m["pos_M"], "%d" % m["n_pos_years"],
                              "%d" % m["n_years"]])
    for bname in BOOK_NAMES:
        for mode in ("div", "price"):
            for cst in COST_LEVELS_BPS:
                m = BMET[(bname, mode, cst)]
                srows.append(["book", bname, mode, "%g" % cst,
                              "%.10f" % m["cagr"], "%.10f" % m["max_dd"],
                              fnum(m["sharpe_excess"]),
                              "%.10f" % m["pos_Y"], "%.10f" % m["pos_Q"],
                              "%.10f" % m["pos_M"], "%d" % m["n_pos_years"],
                              "%d" % m["n_years"]])
    for mode in ("div", "price"):
        for cst in COST_LEVELS_BPS:
            m = rBMET[(mode, cst)]
            srows.append(["book", "REDUCED", mode, "%g" % cst,
                          "%.10f" % m["cagr"], "%.10f" % m["max_dd"],
                          fnum(m["sharpe_excess"]),
                          "%.10f" % m["pos_Y"], "%.10f" % m["pos_Q"],
                          "%.10f" % m["pos_M"], "%d" % m["n_pos_years"],
                          "%d" % m["n_years"]])
    wm("summary.csv", ["table=headline metrics for every series/mode/cost"],
       ["kind", "name", "mode", "cost_bps", "cagr", "max_dd", "sharpe_excess",
        "pos_Y", "pos_Q", "pos_M", "n_pos_years", "n_years"], srows)

    drowsp = []
    for j, d in enumerate(dates):
        drowsp.append([d.isoformat(), "%.10f" % cash.ret[j],
                       ("%.6f" % cash.rate[j]) if cash.rate[j] is not NA else ""])
    wm("cash_daily.csv", ["table=daily cash accrual and the rate used"],
       ["date", "cash_return", "annual_rate_pct"], drowsp)

    vlog = SLEEVES["div"]["V"].meta["rolls_log"]
    wm("vrp_rolls.csv",
       ["table=[MODELED] every VRP roll: the exact inputs the sleeve priced "
        "from and the resulting contract",
        "S0/vix_lag/r/q/K1/K2/width/credit are in SPY price units",
        "iv/sig_s/sig_l are annualised decimals"],
       ["signal_date", "roll_date", "expiry_date", "S0", "vix_lag", "iv",
        "sig_s", "sig_l", "r", "q", "K1", "K2", "width", "credit",
        "credit_over_width"],
       [[r[0], r[1], r[2]] + ["%.6f" % r[i] for i in range(3, len(r))]
        for r in vlog])

    inv = []
    sset = set(dates)
    for sym in ALL_PRICE_SYMBOLS + ALL_OTHER_SYMBOLS:
        s = universe[sym]
        span = [d for d in dates if s.dates[0] <= d <= s.dates[-1]]
        have = set(s.dates)
        miss = sum(1 for d in span if d not in have)
        inv.append([sym, len(s.dates), s.dates[0].isoformat(),
                    s.dates[-1].isoformat(), len(span), miss, len(span) - miss,
                    "%.6f" % (miss / float(len(span))) if span else ""])
    wm("data_inventory.csv", ["table=every series loaded, its span and how many "
                              "book sessions it has no print on"],
       ["symbol", "rows", "first", "last", "book_sessions_in_span",
        "no_print_sessions", "printed_sessions", "no_print_fraction"],
       inv)

    with open(os.path.join(OUT_DIR, "preregistration.txt"), "w",
              encoding="utf-8", newline="\n") as fh:
        for k, v in PREREG_TEXT:
            fh.write("%-18s %s\n" % (k, v))
    print("")
    print("  wrote %d CSV/text artefacts to %s"
          % (len([f for f in os.listdir(OUT_DIR)]), OUT_DIR))
    return 0


if __name__ == "__main__":
    sys.exit(main())
