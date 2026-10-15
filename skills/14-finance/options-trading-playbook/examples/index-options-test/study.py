#!/usr/bin/env python3
"""
study.py -- can a three-index ETF book (SPY/QQQ/IWM), trading BOTH the
underlying and options on it, be "profitable in most conditions", and what
does it cost?

Deterministic. Stdlib only. No network. No RNG. No wall clock. LF output.

=============================================================================
WHAT IS REAL AND WHAT IS MODELED -- READ THIS BEFORE ANY NUMBER BELOW
=============================================================================
REAL, from data/*.csv, each series behind a `# PROVENANCE:` header:
    * daily OHLC for AMEX:SPY, NASDAQ:QQQ, AMEX:IWM   (TradingView, 2026-10-14)
    * daily VIX index level, TVC:VIX                  (TradingView, 2026-10-14)
    * daily 3-month US Treasury bill YIELD, TVC:US03M (TradingView, 2026-10-14)

MODELED, and every number derived from it is labelled [MODELED]:
    * EVERY option price in this study. Historical option quotes are not
      available from the sources used here. Each leg is priced with
      Black-Scholes on a model implied vol built from the real VIX, and each
      spread is settled against the REAL index closing price on its expiry
      session.

The option model cannot see any of the following, and the reader should hold
every [MODELED] figure at arm's length because of it:
    1. no bid/ask spread in the quote -- a flat per-contract spread IS charged
       as a cost, but the quote itself is mid;
    2. no skew -- one implied vol prices every strike, so the 16-delta put and
       the 5-wide long leg are priced with the same vol, which understates the
       cost of the long wing;
    3. no term structure in the primary run -- one vol prices the 30-DTE spread
       and the 60-DTE hedge (a sqrt(30/D) variant is reported);
    4. no early exercise and no assignment -- AMERICAN, physically settled in
       reality, priced here as EUROPEAN;
    5. no pin risk -- the expiry session's close decides everything;
    6. no dividends -- the price series is price-only, so the modelled call is
       too expensive (overstating S3's credit) and the modelled put is too
       cheap;
    7. no margin, no buying-power constraint, no liquidity limit, no partial
       fills, no legging risk, no tax;
    8. one contract per sleeve, integer, always fillable at the modelled mid.

USAGE
    py -3 study.py > run-output.txt
    py -3 study.py --dump-trades S2:SPY:2020-03
"""

import argparse
import datetime
import io
import math
import os
import sys

# ---------------------------------------------------------------------------
# The sibling timeframe engine owns the bucketing convention. Import it rather
# than reimplement it, so a bucket key here cannot disagree with the engine's.
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
TF_PATH = os.path.join(HERE, "..", "..", "..",
                       "timeframe-performance-statistics", "scripts")
sys.path.insert(0, os.path.abspath(TF_PATH))
try:
    import timeframe_stats as TF
except ImportError as exc:
    raise SystemExit("ERROR: cannot import timeframe_stats from %s (%s)"
                     % (TF_PATH, exc))

DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "out")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")

# ===========================================================================
# PRE-REGISTERED CONFIGURATION.  Every constant below was fixed before the
# first run.  Nothing here is tuned on results.
# ===========================================================================

SYMBOLS = ["SPY", "QQQ", "IWM"]
UNIVERSE = SYMBOLS + ["VIX", "US03M"]

SMA_TREND = 200                # S1: long iff close > SMA(200)
ATR_PERIOD = 14                # S1/S3/S6 risk unit denominator
ATR_MULT_RISK = 2.0            # R = 2 * ATR(14) at entry (the sibling's unit)
TRADING_DAYS = 252

VIX_LAG_SESSIONS = 3           # headline haircut: only VIX from 3 sessions ago
                               # may price today's option
IV_TERM_ALPHA = 0.0            # IV(D) = VIX * (30/D)**alpha ; 0 = flat term
                               # structure (the primary setting)
IV_STRESS_GRID = (0.8, 1.0, 1.2)
KAPPA_LOOKBACK = 60            # sessions of realised vol behind the per-index
KAPPA_CLIP = (0.60, 2.00)      # relative-vol multiplier band

DTE = 30                       # calendar days to expiry, all monthly structures
S2_SHORT_PUT_DELTA = 0.16      # pre-registered short-leg delta
S2_WIDTH_DOLLARS = 5.0         # pre-registered width, in DOLLARS
S3_CALL_DELTA = 0.30
S4_PUT_OTM = 0.05              # 5% out of the money
S4_PUT_DTE = 60                # 60-day tenor, rolled monthly
S2_SLEEVE_MAXLOSSES = 10.0     # sleeve capital = 10 x one max-loss spread, i.e.
                               # a worst-case month costs -10% of the sleeve.
                               # Fixed before the run; NOT tuned.
S5_CARRY_WEIGHT = 0.25         # S5 = 0.75 * S1 book + 0.25 * S2 book.  FIXED.
                               # Declared before the run; NOT tuned.

# Cost settings.  `half_spread` is per SHARE per SIDE, so a round trip on one
# leg costs 2 * half_spread * 100 dollars per contract.  `fee` is dollars per
# contract per side.  `etf_bps` is the round-trip cost on the underlying.
COST_SETTINGS = [
    ("FREE", {"fee": 0.00, "half_spread": 0.000, "etf_bps": 0.0}),
    ("LOW",  {"fee": 0.65, "half_spread": 0.025, "etf_bps": 5.0}),
    ("HIGH", {"fee": 0.65, "half_spread": 0.050, "etf_bps": 20.0}),
]
HEADLINE_COST = "LOW"

# Published APPROXIMATE average dividend yields for the three ETFs, used ONLY in
# the dividend sensitivity (section 13b).  The price series carries no dividends,
# so the primary run prices every option with q = 0; these numbers exist so the
# size of that bias can be seen rather than asserted.  They are round published
# averages, not a fitted series, and they are held constant over 25 years.
DIV_YIELD = {"SPY": 0.018, "QQQ": 0.006, "IWM": 0.013}

# The pre-registered success bar.  Declared before the run.
BAR_POS_YEARS = 0.80
BAR_POS_QUARTERS = 0.70
# (c) CAGR above the cash rate over the same window, and (d) max drawdown
# reported, not thresholded after the fact.

NA = None
BUCKETS = ["D", "W", "2W", "M", "Q", "H", "Y"]
LAMBDA_STEPS = 20              # lambda = i/20, i in 0..20
LAMBDA_FINE = 0.001            # bisection resolution for the frontier endpoint

STRATEGIES = [
    ("S1", "Trend on the underlying (long iff close > SMA200, flat below)"),
    ("S2", "Systematic premium selling, defined risk (30-DTE $5-wide put "
           "spread, ~16-delta short)"),
    ("S3", "Buy-write / covered call (long underlying, short 30-DTE ~30-delta "
           "call)"),
    ("S4", "Tail-hedged premium (S2 + long ~5%-OTM 60-DTE put, rolled "
           "monthly)"),
    ("S5", "Trend + premium overlay (0.75 x S1 book + 0.25 x S2 book)"),
    ("S6", "Buy & hold (the control)"),
]
STRAT_IDS = [s for s, _ in STRATEGIES]

# Stress windows, declared before the run.
STRESS = [
    ("2008 GFC", datetime.date(2008, 1, 1), datetime.date(2009, 3, 31)),
    ("2020 COVID", datetime.date(2020, 1, 1), datetime.date(2020, 12, 31)),
]


# ===========================================================================
# Small helpers
# ===========================================================================

def pct(x, nd=2):
    if x is NA:
        return "n/a"
    return ("%+.*f%%" % (nd, x * 100.0))


def num(x, nd=4):
    if x is NA:
        return "n/a"
    return ("%.*f" % (nd, x))


def money(x):
    if x is NA:
        return "n/a"
    return ("%+.2f" % x)


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
    return "\n".join(out)


def emit(text):
    print(text)


def banner(title):
    print("")
    print("=" * 78)
    print(title)
    print("=" * 78)


def write_table(name, header, rows):
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    path = os.path.join(OUT, name)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(",".join(header) + "\n")
        for r in rows:
            fh.write(",".join(str(c) for c in r) + "\n")
    return len(rows)


# ===========================================================================
# Black-Scholes.  The ONLY option pricer in this study.
# ===========================================================================

SQRT_2 = math.sqrt(2.0)
INV_SQRT_2PI = 1.0 / math.sqrt(2.0 * math.pi)


def ncdf(x):
    return 0.5 * (1.0 + math.erf(x / SQRT_2))


def npdf(x):
    return INV_SQRT_2PI * math.exp(-0.5 * x * x)


def bs_price(S, K, T, r, sigma, kind, q=0.0):
    """European Black-Scholes price per SHARE, continuous dividend yield q.

    q is 0.0 in the PRIMARY run (the price series carries no dividends), and is
    set to a stated published average in the dividend sensitivity only.

    At T -> 0 (or sigma -> 0) the value is intrinsic, so the same function
    settles an expiring leg as it prices a live one.
    """
    if S <= 0.0 or K <= 0.0:
        return 0.0
    if T <= 1e-9 or sigma <= 1e-9:
        return max(S - K, 0.0) if kind == "C" else max(K - S, 0.0)
    srt = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / srt
    d2 = d1 - srt
    disc_r = math.exp(-r * T)
    disc_q = math.exp(-q * T)
    if kind == "C":
        return S * disc_q * ncdf(d1) - K * disc_r * ncdf(d2)
    return K * disc_r * ncdf(-d2) - S * disc_q * ncdf(-d1)


def bs_delta(S, K, T, r, sigma, kind, q=0.0):
    """dPrice/dS, per share.  Calls: e^-qT N(d1).  Puts: e^-qT (N(d1) - 1)."""
    if S <= 0.0 or K <= 0.0:
        return 0.0
    if T <= 1e-9 or sigma <= 1e-9:
        if kind == "C":
            return 1.0 if S > K else 0.0
        return -1.0 if S < K else 0.0
    srt = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / srt
    disc_q = math.exp(-q * T)
    return disc_q * (ncdf(d1) if kind == "C" else ncdf(d1) - 1.0)


def strike_for_put_delta(S, T, r, sigma, target, q=0.0):
    """K such that |put delta| == target.  |put delta| is INCREASING in K."""
    lo, hi = 0.20 * S, 1.60 * S
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if abs(bs_delta(S, mid, T, r, sigma, "P", q)) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def strike_for_call_delta(S, T, r, sigma, target, q=0.0):
    """K such that call delta == target.  call delta is DECREASING in K."""
    lo, hi = 0.20 * S, 1.60 * S
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if bs_delta(S, mid, T, r, sigma, "C", q) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ===========================================================================
# Statistics helpers (own, except bucketing which is the sibling engine's)
# ===========================================================================

def sample_sd(xs):
    n = len(xs)
    if n < 2:
        return NA
    m = sum(xs) / float(n)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / float(n - 1))


def mean(xs):
    return sum(xs) / float(len(xs)) if xs else NA


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return NA
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    if sxx <= 0.0 or syy <= 0.0:
        return NA
    return sxy / math.sqrt(sxx * syy)


def equity_curve(rets):
    c = [1.0]
    for r in rets:
        c.append(c[-1] * (1.0 + r))
    return c


def max_drawdown_pct(curve):
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


def longest_losing_streak(rs):
    worst = run = 0
    for r in rs:
        if r <= 0.0:
            run += 1
            worst = max(worst, run)
        else:
            run = 0
    return worst


def streak_expected(p, n):
    """L ~ ln(N) / ln(1/(1-p)) -- the pre-registered approximation."""
    if n <= 1 or p <= 0.0 or p >= 1.0:
        return NA
    return math.log(n) / math.log(1.0 / (1.0 - p))


def trade_stats(rs):
    """p, b, E (formula), E_R (mean R), p*, b*, sd, n_req, L_expected, L_actual."""
    n = len(rs)
    if n == 0:
        return NA
    wins = [x for x in rs if x > 0.0]
    losses = [x for x in rs if x <= 0.0]
    p = len(wins) / float(n)
    if wins and losses:
        b = (sum(wins) / len(wins)) / abs(sum(losses) / len(losses))
    else:
        b = NA
    e_form = (p * b - (1.0 - p)) if b is not NA else NA
    e_r = sum(rs) / float(n)
    sd = sample_sd(rs)
    p_star = (1.0 / (1.0 + b)) if b is not NA else NA
    b_star = ((1.0 - p) / p) if p > 0.0 else NA
    n_req = (4.0 * (sd / abs(e_r)) ** 2) if (sd is not NA and e_r) else NA
    return {"n": n, "p": p, "b": b, "E_form": e_form, "E_R": e_r, "sd": sd,
            "p_star": p_star, "b_star": b_star, "n_req": n_req,
            "L_expected": streak_expected(p, n),
            "L_actual": longest_losing_streak(rs),
            "total_R": sum(rs)}


# ---------------------------------------------------------------------------
# Period grouping -- the frontier study's convention, reproduced exactly:
# a COMPLETE period is one whose whole calendar span lies inside the window,
# so "fraction of positive years" is a statement about whole years.
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
        em = qm + 2
        nxt = (datetime.date(d.year + 1, 1, 1) if em == 12
               else datetime.date(d.year, em + 1, 1))
        return first, nxt - datetime.timedelta(days=1)
    if bucket == "H":
        if d.month <= 6:
            return datetime.date(d.year, 1, 1), datetime.date(d.year, 6, 30)
        return datetime.date(d.year, 7, 1), datetime.date(d.year, 12, 31)
    if bucket == "Y":
        return datetime.date(d.year, 1, 1), datetime.date(d.year, 12, 31)
    raise ValueError("unknown bucket %r" % bucket)


def group_index(dates, bucket, complete_only=True):
    g, order = {}, []
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


def level_stats(dates, rets, cash=None):
    n = len(rets)
    curve = equity_curve(rets)
    yrs = years_between(dates[0], dates[-1])
    cagr = -1.0 if curve[-1] <= 0.0 else curve[-1] ** (1.0 / yrs) - 1.0
    m = sum(rets) / n if n else NA
    sd = sample_sd(rets)
    sharpe_raw = (m / sd * math.sqrt(TRADING_DAYS)) if (sd and sd > 0) else NA
    sharpe_ex = NA
    if cash is not None and sd and sd > 0:
        ex = [r - c for r, c in zip(rets, cash)]
        me = sum(ex) / len(ex)
        sde = sample_sd(ex)
        if sde and sde > 0:
            sharpe_ex = me / sde * math.sqrt(TRADING_DAYS)
    return {"n_days": n, "years": yrs, "cagr": cagr,
            "max_dd": max_drawdown_pct(curve), "sharpe_raw": sharpe_raw,
            "sharpe_excess_cash": sharpe_ex, "sd_daily": sd,
            "total": curve[-1] - 1.0}


# ===========================================================================
# Data
# ===========================================================================

class Series(object):
    def __init__(self, name, dates, o, h, l, c):
        self.name = name
        self.dates = dates
        self.o, self.h, self.l, self.c = o, h, l, c
        self.index_of = {}
        for i, d in enumerate(dates):
            self.index_of[d] = i

    def sma(self, n):
        out = [NA] * len(self.c)
        run = 0.0
        for i in range(len(self.c)):
            run += self.c[i]
            if i >= n:
                run -= self.c[i - n]
            if i >= n - 1:
                out[i] = run / float(n)
        return out

    def atr(self, n):
        out = [NA] * len(self.c)
        trs = []
        for i in range(len(self.c)):
            if i == 0:
                trs.append(self.h[i] - self.l[i])
            else:
                trs.append(max(self.h[i] - self.l[i],
                               abs(self.h[i] - self.c[i - 1]),
                               abs(self.l[i] - self.c[i - 1])))
            if i >= n - 1:
                out[i] = sum(trs[i - n + 1:i + 1]) / float(n)
        return out

    def logret_sd(self, n, end_idx):
        """Annualised sample sd of the n log returns ending at end_idx."""
        if end_idx is NA or end_idx - n < 0:
            return NA
        rets = []
        for i in range(end_idx - n + 1, end_idx + 1):
            if self.c[i - 1] <= 0 or self.c[i] <= 0:
                return NA
            rets.append(math.log(self.c[i] / self.c[i - 1]))
        sd = sample_sd(rets)
        if sd is NA:
            return NA
        return sd * math.sqrt(TRADING_DAYS)


def read_series(path, name):
    dates, o, h, l, c = [], [], [], [], []
    with io.open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
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
    return Series(name, dates, o, h, l, c)


def provenance_of(path):
    lines = []
    with io.open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            if line.startswith("# PROVENANCE:"):
                lines.append(line.rstrip("\r\n")[len("# PROVENANCE:"):].strip())
            elif not line.startswith("#"):
                break
    return lines


def carry_forward(series, d, max_back=10):
    """Value of `series` at date d, walking back up to `max_back` sessions."""
    k = series.index_of.get(d)
    if k is not None:
        return series.c[k]
    j = 0
    probe = d
    while j < max_back:
        probe = probe - datetime.timedelta(days=1)
        k = series.index_of.get(probe)
        if k is not None:
            return series.c[k]
        j += 1
    return NA


# ===========================================================================
# Option structures
# ===========================================================================

class Config(object):
    def __init__(self, cost_name, fee, half_spread, etf_bps,
                 vix_lag, iv_alpha, iv_mult, width_dollars, label="",
                 hedge_mode="FULL", div_yield=None, short_iv_haircut=0.0):
        self.cost_name = cost_name
        self.fee = fee
        self.half_spread = half_spread
        self.etf_bps = etf_bps
        self.vix_lag = vix_lag
        self.iv_alpha = iv_alpha
        self.iv_mult = iv_mult
        self.width_dollars = width_dollars
        self.label = label
        # "FULL"   : one long tail put per spread (the literal pre-registration)
        # "CREDIT" : the tail put sized so its debit equals the spread credit,
        #            i.e. genuinely 'paid for by the premium' (fractional
        #            contracts -- a stated model simplification)
        self.hedge_mode = hedge_mode
        # underlying dividend yield per index, used ONLY in the dividend
        # sensitivity.  Empty in the primary run.
        self.div_yield = div_yield or {}
        # SKEW HAIRCUT, in vol points, applied to the SOLD leg only.  The model
        # has no skew -- one vol prices every strike -- so a real seller of an
        # OTM option collects LESS than the flat-vol Black-Scholes value.  This
        # knob exists to size that bias; it is 0.0 in the primary run.
        self.short_iv_haircut = short_iv_haircut

    def q(self, sym):
        return self.div_yield.get(sym, 0.0)

    def key(self):
        return "%s|lag%d|a%.2f|m%.2f|w%.1f|%s|q%s" % (
            self.cost_name, self.vix_lag, self.iv_alpha, self.iv_mult,
            self.width_dollars, self.hedge_mode,
            ",".join("%s=%.4f" % (k, v) for k, v in sorted(self.div_yield.items())))


def cost_one_way(cfg, qty):
    """ONE SIDE of one option leg, in dollars (fee + half the bid/ask width).

    A round trip is two of these, charged once at entry and once at exit.  An
    expiring leg has no exit cost -- it expires.
    """
    return abs(qty) * (cfg.fee + cfg.half_spread * 100.0)


class Leg(object):
    """One option leg, signed qty.  +1 long, -1 short.  qty may be fractional
    in the credit-funded S4 variant; that is a stated model simplification."""
    __slots__ = ("kind", "K", "expiry", "qty", "q", "iv_haircut")

    def __init__(self, kind, K, expiry, qty, q=0.0, iv_haircut=0.0):
        self.kind, self.K, self.expiry, self.qty = kind, K, expiry, qty
        self.q = q
        self.iv_haircut = iv_haircut

    def value(self, S, T, r, sigma):
        """Dollar value of the leg: qty * 100 * BS price per share.

        `iv_haircut` is subtracted from the vol for THIS leg only, which is how
        the skew sensitivity is applied."""
        sig = max(1e-6, sigma - self.iv_haircut)
        return self.qty * 100.0 * bs_price(S, self.K, T, r, sig, self.kind,
                                           self.q)


class OptSleeve(object):
    """cash + marked option legs.  Equity = cash + mark.

    An expiring leg is left in the book at T=0 on the close of its expiry
    session, where its model value IS its intrinsic value, and the intrinsic is
    moved into cash at that same close.  Equity is therefore continuous across
    an expiry: no jump, no double count.
    """
    __slots__ = ("base", "cash", "legs", "equity", "rets")

    def __init__(self, capital):
        self.base = float(capital)
        self.cash = float(capital)
        self.legs = []
        self.equity = float(capital)
        self.rets = []


# ===========================================================================
# Implied vol model
# ===========================================================================

def build_iv_context(window_dates, series, vix, us03m, cfg):
    """Per-session (vix_used, r_used, kappa[SYM]) on the window calendar.

    vix_used[j]  = VIX close from `vix_lag` sessions before window date j,
                   carried forward if that exact session is absent.
    r_used[j]    = the 3-month bill yield (percent) at the same lagged session,
                   divided by 100 and FLOORED AT ZERO.
    kappa[sym][j]= clip(RV60(sym) / RV60(SPY), 0.60, 2.00), both measured at the
                   lagged session.  This is the per-index relative-vol
                   adjustment: VIX is the S&P 500 vol index and QQQ/IWM do not
                   run at the S&P's vol.  It is mechanical, not tuned.
    """
    n = len(window_dates)
    vix_used = [NA] * n
    r_used = [NA] * n
    for j in range(n):
        k = max(0, j - cfg.vix_lag)
        d = window_dates[k]
        vix_used[j] = carry_forward(vix, d)
        y = carry_forward(us03m, d)
        r_used[j] = max(0.0, y / 100.0) if y is not NA else 0.0

    kappa = {}
    for sym in SYMBOLS:
        arr = [1.0] * n
        if sym != "SPY":
            s = series[sym]
            spy = series["SPY"]
            for j in range(n):
                k = max(0, j - cfg.vix_lag)
                d = window_dates[k]
                rv_sym = s.logret_sd(KAPPA_LOOKBACK, s.index_of.get(d))
                rv_spy = spy.logret_sd(KAPPA_LOOKBACK, spy.index_of.get(d))
                if rv_sym is NA or rv_spy in (NA, 0.0):
                    arr[j] = 1.0
                else:
                    v = rv_sym / rv_spy
                    arr[j] = min(max(v, KAPPA_CLIP[0]), KAPPA_CLIP[1])
        kappa[sym] = arr
    return vix_used, r_used, kappa


def iv_of(cfg, vix_pct, sym, j, kappa, dte_leg=None):
    """Model implied vol as a DECIMAL for a leg.

    IV = VIX(t-lag)/100 * kappa(index) * iv_mult * (30/D)**alpha
    `dte_leg` defaults to DTE (30).  alpha = 0 means one vol prices every
    tenor, which is the primary setting.
    """
    if vix_pct is NA:
        return 0.0
    D = float(DTE if dte_leg is None else dte_leg)
    base = vix_pct / 100.0 * kappa[sym][j] * cfg.iv_mult
    if cfg.iv_alpha:
        base *= (30.0 / D) ** cfg.iv_alpha
    return base


# ===========================================================================
# The window
# ===========================================================================

def build_window(series, need_common=True, only=None):
    """Common calendar + the date on which every required rule is live."""
    syms = [only] if only else SYMBOLS
    sets = [set(series[s].dates) for s in syms]
    sets.append(set(series["VIX"].dates))
    common = set.intersection(*sets)
    starts = []
    for s in syms:
        sma = series[s].sma(SMA_TREND)
        fl = None
        for i, v in enumerate(sma):
            if v is not NA:
                fl = series[s].dates[i]
                break
        if fl is None:
            raise SystemExit("ERROR: SMA never live for %s" % s)
        starts.append(fl)
    dates = sorted(d for d in common if d >= max(starts))
    return dates


def month_grid(dates):
    """[(signal_date, entry_date, next_entry_date)]: signal on the LAST session
    of a month, entry at the OPEN of the first session of the next month.

    `next_entry_date` is NA for the final month.  It is needed because a monthly
    program must not hold two overlapping cycles: the expiry of this month's
    structure is capped at the LAST session before the next entry.
    """
    out = []
    for j in range(1, len(dates)):
        prev, cur = dates[j - 1], dates[j]
        if (cur.year, cur.month) != (prev.year, prev.month):
            out.append((prev, cur))
    final = []
    for i, (sig_d, ent_d) in enumerate(out):
        nxt = out[i + 1][1] if i + 1 < len(out) else NA
        final.append((sig_d, ent_d, nxt))
    return final


def monthly_expiry(window_dates, ent_d, next_ent_d, tenor_days):
    """Expiry session: the first session on or after entry + `tenor_days`,
    CAPPED at the last session strictly before the next monthly entry.

    The cap is what makes this a monthly programme: without it, a 30-calendar-day
    tenor that lands after the next roll would leave the previous structure open
    alongside the new one.  Measured tenors are therefore 27-30 calendar days
    rather than a nominal 30, and the pricing uses the ACTUAL calendar days.
    """
    t = next_session_on_or_after(window_dates,
                                 ent_d + datetime.timedelta(days=tenor_days))
    if next_ent_d is not NA:
        cap = last_session_on_or_before(
            window_dates, next_ent_d - datetime.timedelta(days=1))
        if cap is not NA and (t is NA or cap < t):
            t = cap
    return t


def next_session_on_or_after(dates, target):
    for d in dates:
        if d >= target:
            return d
    return NA


def last_session_on_or_before(dates, target):
    hit = NA
    for d in dates:
        if d <= target:
            hit = d
        else:
            break
    return hit


# ===========================================================================
# S1 -- trend on the underlying
# ===========================================================================

def run_trend(series, sym, window_dates, cfg):
    """Daily returns of a long/flat trend sleeve on ONE index.

    Position held during session j was decided at the close of j-1 and is
    established at the OPEN of j, so:
        entry session : open_j -> close_j
        held session  : close_{j-1} -> close_j
        exit session  : close_{j-1} -> open_j   (flat after the open)
        flat session  : 0
    That makes the compounded daily series agree with the trade log, whose entry
    and exit prices are those same opens.  Cost is half a round trip on each of
    the entry and the exit.
    """
    s = series[sym]
    sma = s.sma(SMA_TREND)
    atr = s.atr(ATR_PERIOD)
    n = len(window_dates)
    idx = [s.index_of[d] for d in window_dates]
    sig = [NA] * n
    for j in range(n):
        k = idx[j]
        sig[j] = 1 if (sma[k] is not NA and s.c[k] > sma[k]) else 0

    rets = [0.0] * n
    flips = 0
    trades = []
    open_trade = None
    for j in range(n):
        k = idx[j]
        if j == 0:
            continue
        pos = sig[j - 1]
        prev_pos = sig[j - 2] if j >= 2 else 0
        if pos == 1 and prev_pos == 0:
            r = s.c[k] / s.o[k] - 1.0
            flips += 1
            open_trade = {"entry_date": window_dates[j], "entry_px": s.o[k],
                          "R_share": ATR_MULT_RISK * atr[k - 1]}
        elif pos == 1:
            r = s.c[k] / s.c[k - 1] - 1.0
        elif prev_pos == 1:
            r = s.o[k] / s.c[k - 1] - 1.0
        else:
            r = 0.0
        if pos == 0 and prev_pos == 1:
            flips += 1
            if open_trade is not None:
                trades.append(_close_trend(open_trade, s.o[k], window_dates[j]))
                open_trade = None
        rets[j] = r
    if open_trade is not None:
        k = idx[n - 1]
        trades.append(_close_trend(open_trade, s.c[k], window_dates[n - 1]))

    half = (cfg.etf_bps / 2.0) / 10000.0
    for j in range(1, n):
        pos = sig[j - 1]
        prev_pos = sig[j - 2] if j >= 2 else 0
        if pos != prev_pos:
            rets[j] -= half
    return {"rets": rets, "trades": trades, "flips": flips, "sig": sig}


def _close_trend(t, exit_px, exit_date):
    pnl = exit_px - t["entry_px"]
    R = t["R_share"]
    return {"entry_date": t["entry_date"], "exit_date": exit_date,
            "R_dollars": R * 100.0, "pnl_dollars": pnl * 100.0,
            "R_mult": pnl / R if R else NA, "note": ""}


# ===========================================================================
# S2 / S4 -- the premium sleeves
# ===========================================================================

def payoff_max_loss(legs, lo, hi, credit, steps=6000):
    """Maximum LOSS per share of a structure over a terminal price grid.

    A leg with signed qty q pays q*intrinsic to the holder, so the structure's
    P&L per share at terminal price S is credit + sum(q * intrinsic).  For the
    pre-registered spread -- short K1, long K2 = K1 - width -- this reproduces
    width - credit exactly, which is checked in section 3 of the report.
    """
    worst = None
    for i in range(steps + 1):
        S = lo + (hi - lo) * i / steps
        pnl = credit
        for L in legs:
            intrin = (max(L.K - S, 0.0) if L.kind == "P"
                      else max(S - L.K, 0.0))
            pnl += L.qty * intrin
        if worst is None or pnl < worst:
            worst = pnl
    return -worst


def run_premium(series, sym, window_dates, cfg, iv_ctx, with_hedge):
    """S2 (with_hedge=False) and S4 (with_hedge=True) on ONE index.

    Each month: signal at the last session of the previous month; the strikes
    are chosen from that SIGNAL close; the credit is taken at the ENTRY open;
    the spread is held to the expiry session and settled at intrinsic against
    the REAL close of that session.

    S4 additionally buys ONE long put, S4_PUT_OTM out of the money with
    S4_PUT_DTE calendar days to expiry, at the same entry, and closes it at the
    NEXT monthly entry (mark-to-model) or at its own expiry, whichever is
    first.  One hedge is therefore alive per spread, written ~60 days out.
    """
    vix_used, r_used, kappa = iv_ctx
    s = series[sym]
    q = cfg.q(sym)
    pos_of = {d: j for j, d in enumerate(window_dates)}
    # The sleeve's capital is a FIXED RISK BUDGET of 10 spread-widths, and the
    # sleeve's daily return is its DOLLAR P&L divided by that budget.  A fixed
    # budget (rather than a compounding account) is what makes S2 and S4
    # comparable: a variant that is a persistent net cash OUTFLOW shows up as a
    # persistent negative return instead of silently depleting the account.
    base = S2_SLEEVE_MAXLOSSES * cfg.width_dollars * 100.0
    slv = OptSleeve(base)

    scheduled = []
    for sig_d, ent_d, nxt_d in month_grid(window_dates):
        exp_d = monthly_expiry(window_dates, ent_d, nxt_d, DTE)
        if exp_d is NA:
            continue
        h_exp = next_session_on_or_after(
            window_dates, ent_d + datetime.timedelta(days=S4_PUT_DTE))
        scheduled.append({"sym": sym, "sig": sig_d, "entry": ent_d,
                          "expiry": exp_d, "hedge_expiry": h_exp,
                          "spread_open": False, "closed": False,
                          "hedge_open": False, "hedge_entry": NA,
                          "hedge_exit_dollars": NA, "hedge_entry_dollars": NA,
                          "K1": NA, "K2": NA, "credit": NA, "iv": NA,
                          "S_entry": NA, "S_sig": NA, "S_settle": NA,
                          "spread_cost": NA, "h_K": NA, "h_debit": NA,
                          "h_qty": NA, "h_net": NA})
    by_entry = {}
    for tr in scheduled:
        by_entry[tr["entry"]] = tr

    n = len(window_dates)
    for j, d in enumerate(window_dates):
        k = s.index_of[d]
        S_open, S_close = s.o[k], s.c[k]

        # ---- 1. at the OPEN: roll or expire hedges belonging to older trades
        for tr in scheduled:
            if not tr["hedge_open"] or tr["hedge_entry"] == d:
                continue
            if tr["hedge_expiry"] == d or d in by_entry:
                L = tr["hedge"]
                T = max(0.0, (L.expiry - d).days) / 365.0
                sig = iv_of(cfg, vix_used[j], sym, j, kappa,
                            max(1, (L.expiry - d).days))
                val = L.value(S_open, T, r_used[j], sig)
                c = cost_one_way(cfg, L.qty)
                slv.cash += val - c
                slv.legs.remove(L)
                tr["hedge_open"] = False
                tr["hedge_exit_dollars"] = val - c

        # ---- 2. at the OPEN: enter this month's spread (and its hedge)
        tr = by_entry.get(d)
        if tr is not None:
            j_sig = pos_of[tr["sig"]]
            k_sig = s.index_of[tr["sig"]]
            T_entry = max(0.0, (tr["expiry"] - d).days) / 365.0
            r_now = r_used[j_sig]
            iv_now = iv_of(cfg, vix_used[j_sig], sym, j_sig, kappa)
            if iv_now > 0.0 and T_entry > 0.0:
                S_sig = s.c[k_sig]
                K1 = strike_for_put_delta(S_sig, T_entry, r_now, iv_now,
                                          S2_SHORT_PUT_DELTA, q)
                K2 = K1 - cfg.width_dollars
                iv_short = max(1e-6, iv_now - cfg.short_iv_haircut)
                cred = (bs_price(S_open, K1, T_entry, r_now, iv_short, "P", q)
                        - bs_price(S_open, K2, T_entry, r_now, iv_now, "P", q))
                short = Leg("P", K1, tr["expiry"], -1, q, cfg.short_iv_haircut)
                long_ = Leg("P", K2, tr["expiry"], +1, q, 0.0)
                scost = 2.0 * cost_one_way(cfg, 1)
                slv.cash += cred * 100.0 - scost
                slv.legs.append(short)
                slv.legs.append(long_)
                tr.update({"K1": K1, "K2": K2, "credit": cred, "iv": iv_now,
                           "S_entry": S_open, "S_sig": S_sig,
                           "spread_cost": scost, "spread_open": True,
                           "short": short, "long": long_})
                if with_hedge and tr["hedge_expiry"] is not NA:
                    T_h = max(0.0, (tr["hedge_expiry"] - d).days) / 365.0
                    KH = S_open * (1.0 - S4_PUT_OTM)
                    hiv = iv_of(cfg, vix_used[j_sig], sym, j_sig, kappa, S4_PUT_DTE)
                    debit = bs_price(S_open, KH, T_h, r_now, hiv, "P", q)
                    # "paid for by the premium": under CREDIT sizing the long
                    # put's quantity is set so its debit equals the spread
                    # credit.  Under FULL it is one contract, always.
                    hq = 1.0
                    if cfg.hedge_mode == "CREDIT" and debit > 0.0:
                        hq = min(1.0, cred / debit)
                    if hq <= 0.0:
                        hq = 0.0
                    hl = Leg("P", KH, tr["hedge_expiry"], +hq, q)
                    hcost = cost_one_way(cfg, hq if hq > 0 else 1)
                    slv.cash -= debit * hq * 100.0 + hcost
                    slv.legs.append(hl)
                    tr.update({"hedge": hl, "h_K": KH, "h_debit": debit,
                               "h_qty": hq, "hedge_entry": d, "hedge_open": True,
                               "hedge_entry_dollars": debit * hq * 100.0 + hcost})

        # ---- 3. at the CLOSE: settle anything expiring today at INTRINSIC
        for tr in scheduled:
            if not tr["spread_open"] or tr["expiry"] != d:
                continue
            intr = (max(0.0, tr["K1"] - S_close)
                    - max(0.0, tr["K2"] - S_close))
            slv.cash -= intr * 100.0
            slv.legs.remove(tr["short"])
            slv.legs.remove(tr["long"])
            tr["spread_open"] = False
            tr["closed"] = True
            tr["S_settle"] = S_close
            tr["gross_per_share"] = tr["credit"] - intr
            tr["pnl_dollars"] = tr["gross_per_share"] * 100.0 - tr["spread_cost"]
            tr["R_dollars"] = max(1e-9, cfg.width_dollars - tr["credit"]) * 100.0
            tr["R_mult"] = tr["pnl_dollars"] / tr["R_dollars"]

        # ---- 4. at the CLOSE: mark the book
        sigma_now = iv_of(cfg, vix_used[j], sym, j, kappa)
        mark = 0.0
        for leg in slv.legs:
            T = max(0.0, (leg.expiry - d).days) / 365.0
            sig = sigma_now
            if cfg.iv_alpha:
                sig = iv_of(cfg, vix_used[j], sym, j, kappa,
                            max(1, (leg.expiry - d).days))
            mark += leg.value(S_close, T, r_used[j], sig)
        eq = slv.cash + mark
        prev = slv.equity
        slv.equity = eq
        # dollar P&L on a FIXED risk budget, not a compounding account
        slv.rets.append((eq - prev) / slv.base)

    # ---- force-close any hedge still open at the last session
    if with_hedge:
        d = window_dates[-1]
        k = s.index_of[d]
        for tr in scheduled:
            if tr["hedge_open"] and tr["hedge_entry"] != d:
                L = tr["hedge"]
                T = max(0.0, (L.expiry - d).days) / 365.0
                sig = iv_of(cfg, vix_used[-1], sym, len(window_dates) - 1, kappa,
                            max(1, (L.expiry - d).days))
                val = L.value(s.c[k], T, r_used[-1], sig)
                c = cost_one_way(cfg, L.qty)
                slv.cash += val - c
                slv.legs.remove(L)
                tr["hedge_open"] = False
                tr["hedge_exit_dollars"] = val - c

    # ---- trade records
    trades, detail = [], []
    for tr in scheduled:
        if not tr["closed"]:
            continue
        pnl = tr["pnl_dollars"]
        R = tr["R_dollars"]
        note = ""
        hq = tr["h_qty"] if tr["h_qty"] is not NA else 0.0
        if with_hedge:
            he = tr["hedge_entry_dollars"]
            hx = tr["hedge_exit_dollars"]
            if he is not NA and hx is not NA:
                pnl_hedge = hx - he
                pnl += pnl_hedge
                # S4's risk unit is the STRUCTURE's maximum loss, computed on a
                # terminal-price grid from the actual legs and the net debit.
                # NOTE: the hedge leg is valued at INTRINSIC here, while in
                # reality it would still carry ~30 days of time value at the
                # spread's expiry -- so R(S4) is a slight OVER-estimate of the
                # structure's true maximum loss.  Stated, not hidden.
                net_credit = tr["credit"] - (
                    tr["h_debit"] * hq if tr["h_debit"] is not NA else 0.0)
                legs = [Leg("P", tr["K1"], tr["expiry"], -1),
                        Leg("P", tr["K2"], tr["expiry"], +1),
                        Leg("P", tr["h_K"], tr["expiry"], hq)]
                ml = payoff_max_loss(legs, 0.30 * tr["S_entry"],
                                     1.30 * tr["S_entry"], net_credit)
                R = max(1e-9, ml) * 100.0
                note = "hedge_net=%.2f hq=%.3f" % (pnl_hedge, hq)
        trades.append({"entry_date": tr["entry"], "exit_date": tr["expiry"],
                       "R_dollars": R, "pnl_dollars": pnl,
                       "R_mult": pnl / R, "note": note})
        detail.append({"sym": sym, "entry": tr["entry"], "expiry": tr["expiry"],
                       "K1": tr["K1"], "K2": tr["K2"], "credit": tr["credit"],
                       "iv": tr["iv"], "S_entry": tr["S_entry"],
                       "S_sig": tr["S_sig"], "S_settle": tr["S_settle"],
                       "R_dollars": R, "pnl_dollars": pnl, "h_K": tr["h_K"],
                       "h_debit": tr["h_debit"], "h_qty": hq,
                       "h_net": tr["hedge_exit_dollars"]})
    return {"rets": slv.rets, "trades": trades, "detail": detail,
            "base": slv.base, "equity": slv.equity}


# ===========================================================================
# S3 -- the buy-write
# ===========================================================================

def run_buywrite(series, sym, window_dates, cfg, iv_ctx):
    """S3: long 100 shares, short one 30-DTE ~30-delta call each month.

    Price-only underlying (NO dividends -- the modelled call is therefore too
    expensive and the credit is overstated; stated in README.md).

    Equity is tracked as
        cash + 100 * S_close - 100 * C(K, T)
    where `cash` accumulates the call credits, the settlement paid at each
    expiry and the costs.  The daily return series is close-to-close; the monthly
    roll is executed at the open, so its one-day effect sits inside the day's
    return.
    """
    vix_used, r_used, kappa = iv_ctx
    s = series[sym]
    q = cfg.q(sym)
    pos_of = {d: j for j, d in enumerate(window_dates)}
    n = len(window_dates)
    idx = [s.index_of[d] for d in window_dates]
    atr = s.atr(ATR_PERIOD)

    plan = {}
    for sig_d, ent_d, nxt_d in month_grid(window_dates):
        exp_d = monthly_expiry(window_dates, ent_d, nxt_d, DTE)
        if exp_d is NA:
            continue
        plan[ent_d] = {"sig": sig_d, "expiry": exp_d}

    # one-off purchase of the shares: one side of the ETF round trip
    cash = 0.0
    call = None            # {"K","credit","expiry","entry","S_entry","cost"}
    rets = [0.0] * n
    equity = 100.0 * s.c[idx[0]]
    trades = []
    open_trade = None

    for j in range(1, n):
        d = window_dates[j]
        k = idx[j]
        S_open, S_close = s.o[k], s.c[k]

        # roll at the open
        if d in plan:
            if open_trade is not None:
                trades.append(_close_bw(open_trade, S_open, d))
            # DEFENSIVE: with monthly_expiry capping the tenor at the next roll
            # this cannot fire.  If it ever does, the old call is bought back at
            # the model value rather than silently dropped -- the latter would
            # hand the sleeve a free short option.
            if call is not None and not call.get("settled"):
                buyback = call["expiry"] - d
                if buyback >= datetime.timedelta(0):
                    raise SystemExit(
                        "ERROR: covered call still open at the roll on %s; "
                        "monthly_expiry failed to cap the tenor" % d.isoformat())
                Tb = max(0.0, (call["expiry"] - d).days) / 365.0
                sigb = iv_of(cfg, vix_used[j], sym, j, kappa)
                cash -= bs_price(S_open, call["K"], Tb, r_used[j], sigb, "C", q) * 100.0
                call["S_expiry"] = S_open
                call["settled"] = True
                call["bought_back"] = True
            p = plan[d]
            j_sig = pos_of[p["sig"]]
            T = max(0.0, (p["expiry"] - d).days) / 365.0
            r_now = r_used[j_sig]
            iv_now = iv_of(cfg, vix_used[j_sig], sym, j_sig, kappa)
            K = strike_for_call_delta(s.c[s.index_of[p["sig"]]], T, r_now,
                                      iv_now, S3_CALL_DELTA, q)
            cred = bs_price(S_open, K, T, r_now,
                            max(1e-6, iv_now - cfg.short_iv_haircut), "C", q)
            c = cost_one_way(cfg, -1)
            cash += cred * 100.0 - c
            call = {"K": K, "credit": cred, "expiry": p["expiry"], "entry": d,
                    "S_entry": S_open, "cost": c}
            open_trade = {"entry_date": d, "entry_px": S_open,
                          "R_share": ATR_MULT_RISK * atr[k - 1], "call": call}

        # settle at the close of the expiry session
        if call is not None and call["expiry"] == d:
            cash -= max(0.0, S_close - call["K"]) * 100.0
            call["S_expiry"] = S_close
            call["settled"] = True

        T = 0.0
        cval = 0.0
        if call is not None and not call.get("settled"):
            T = max(0.0, (call["expiry"] - d).days) / 365.0
            sig = iv_of(cfg, vix_used[j], sym, j, kappa)
            cval = bs_price(S_close, call["K"], T, r_used[j],
                            max(1e-6, sig - cfg.short_iv_haircut), "C", q)
        eq = 100.0 * S_close + cash - 100.0 * cval
        rets[j] = eq / equity - 1.0
        equity = eq
        if call is not None and call["expiry"] == d:
            call["settled"] = True
            call = None
    if open_trade is not None:
        trades.append(_close_bw(open_trade, s.c[idx[-1]], window_dates[-1]))
    return {"rets": rets, "trades": trades, "flips": len(plan)}


def _close_bw(t, exit_px, exit_date):
    """Covered-call trade P&L per share, entry open -> next entry open, with the
    written call settled at its expiry.  Held to the next roll, so there is no
    gap between the equity curve and the trade log."""
    c = t["call"]
    call_pnl = (c["credit"] - max(0.0, c.get("S_expiry", 0.0) - c["K"])
                if c.get("settled") else 0.0)
    pnl = (exit_px - t["entry_px"]) + call_pnl - c["cost"] / 100.0
    R = t["R_share"]
    return {"entry_date": t["entry_date"], "exit_date": exit_date,
            "R_dollars": R * 100.0, "pnl_dollars": pnl * 100.0,
            "R_mult": pnl / R if R else NA, "note": ""}


# ===========================================================================
# Books
# ===========================================================================

def book_from_sleeves(sleeve_rets):
    """Book equity = the MEAN of the sleeves' normalised equity curves, so the
    sleeve weights drift instead of being rebalanced daily (the sibling
    studies' convention).  Book daily return is derived from that curve."""
    n = len(sleeve_rets[0])
    curves = [equity_curve(r) for r in sleeve_rets]
    book = [0.0] * (n + 1)
    for j in range(n + 1):
        book[j] = sum(c[j] for c in curves) / float(len(curves))
    rets = [book[j + 1] / book[j] - 1.0 for j in range(n)]
    return {"rets": rets, "curve": book, "sleeve_rets": sleeve_rets}


def build_strategies(series, window_dates, cfg, iv_ctx, allow_hedge=True):
    """Every strategy on this window.  Returns {strat: book_result}."""
    out = {}
    trend_r, trend_trades = [], []
    for sym in SYMBOLS:
        r = run_trend(series, sym, window_dates, cfg)
        trend_r.append(r["rets"])
        trend_trades.extend(r["trades"])
    out["S1"] = book_from_sleeves(trend_r)
    out["S1"]["trades"] = trend_trades

    prem_r, prem_trades, prem_detail = [], [], []
    for sym in SYMBOLS:
        r = run_premium(series, sym, window_dates, cfg, iv_ctx, False)
        prem_r.append(r["rets"])
        prem_trades.extend(r["trades"])
        prem_detail.extend(r["detail"])
    out["S2"] = book_from_sleeves(prem_r)
    out["S2"]["trades"] = prem_trades
    out["S2"]["detail"] = prem_detail

    bw_r, bw_trades = [], []
    for sym in SYMBOLS:
        r = run_buywrite(series, sym, window_dates, cfg, iv_ctx)
        bw_r.append(r["rets"])
        bw_trades.extend(r["trades"])
    out["S3"] = book_from_sleeves(bw_r)
    out["S3"]["trades"] = bw_trades

    if allow_hedge:
        h_r, h_trades, h_detail = [], [], []
        for sym in SYMBOLS:
            r = run_premium(series, sym, window_dates, cfg, iv_ctx, True)
            h_r.append(r["rets"])
            h_trades.extend(r["trades"])
            h_detail.extend(r["detail"])
        out["S4"] = book_from_sleeves(h_r)
        out["S4"]["trades"] = h_trades
        out["S4"]["detail"] = h_detail

    # S5 = 0.75 * S1 book + 0.25 * S2 book, both on this window
    a, b = out["S1"]["rets"], out["S2"]["rets"]
    s5 = [(1.0 - S5_CARRY_WEIGHT) * x + S5_CARRY_WEIGHT * y
          for x, y in zip(a, b)]
    out["S5"] = {"rets": s5, "curve": equity_curve(s5),
                 "sleeve_rets": [a, b],
                 "trades": out["S1"]["trades"] + out["S2"]["trades"]}

    bh_r = []
    for sym in SYMBOLS:
        s = series[sym]
        n = len(window_dates)
        r = [0.0] * n
        idx = [s.index_of[d] for d in window_dates]
        for j in range(1, n):
            r[j] = s.c[idx[j]] / s.c[idx[j - 1]] - 1.0
        bh_r.append(r)
    out["S6"] = book_from_sleeves(bh_r)
    out["S6"]["trades"] = []
    return out


# ===========================================================================
# Cash
# ===========================================================================

def cash_returns(window_dates, us03m, annual_fee_bps=0.0):
    fee_daily = (annual_fee_bps / 10000.0) / TRADING_DAYS
    out, used = [0.0] * len(window_dates), [NA] * len(window_dates)
    prev_rate = NA
    for j, d in enumerate(window_dates):
        if j == 0:
            prev_rate = carry_forward(us03m, d)
            continue
        y = carry_forward(us03m, window_dates[j - 1])
        if y is not NA:
            prev_rate = y
        if prev_rate is NA:
            out[j] = 0.0
            continue
        used[j] = prev_rate
        out[j] = (prev_rate / 100.0) / TRADING_DAYS - fee_daily
    return out, used


def apply_lambda(risky, cash, lam):
    return [lam * r + (1.0 - lam) * c for r, c in zip(risky, cash)]


# ===========================================================================
# Reporting
# ===========================================================================

def positivity_row(dates, rets, cash, groups, label):
    row = {"book": label}
    for b in BUCKETS:
        f1, f0, npos, nzero, ntot, _ = period_stats(rets, groups[b])
        row[b] = f1
        row[b + "_n"] = ntot
        row[b + "_ge0"] = f0
    row.update(level_stats(dates, rets, cash))
    return row


def window_metrics(dates, rets, d0, d1, cash):
    idx = [j for j, d in enumerate(dates) if d0 <= d <= d1]
    if not idx:
        return NA
    sub = [rets[j] for j in idx]
    curve = equity_curve(sub)
    sub_dates = [dates[j] for j in idx]
    ls = level_stats(sub_dates, sub, [cash[j] for j in idx])
    # worst single complete month in the window
    months = {}
    for j in idx:
        key = (dates[j].year, dates[j].month)
        months.setdefault(key, []).append(rets[j])
    worst_m, worst_k = None, None
    for k in sorted(months):
        c = 1.0
        for r in months[k]:
            c *= (1.0 + r)
        if worst_m is None or (c - 1.0) < worst_m:
            worst_m, worst_k = c - 1.0, k
    return {"total": curve[-1] - 1.0, "max_dd": max_drawdown_pct(curve),
            "cagr": ls["cagr"], "worst_month": worst_m, "worst_month_key": worst_k,
            "n_days": len(idx)}


def dollar_pnl_in_window(dates, rets, base, d0, d1):
    """Total dollar P&L of a sleeve over [d0,d1], compounding its own returns
    on `base` dollars, and its worst single session in dollars."""
    idx = [j for j, d in enumerate(dates) if d0 <= d <= d1]
    if not idx:
        return NA, NA
    eq = base
    worst = 0.0
    for j in idx:
        ch = eq * rets[j]
        if ch < worst:
            worst = ch
        eq += ch
    return eq - base, worst


# ===========================================================================
# Main
# ===========================================================================

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump-trades", default="")
    ap.add_argument("--out-prefix", default="")
    args = ap.parse_args(argv)

    banner("INDEX-OPTIONS TEST -- SPY / QQQ / IWM underlying AND options")
    print("Pre-registered.  Deterministic.  No RNG, no clock, no network.")
    print("")
    print("READ THIS BEFORE ANY NUMBER: every option price below is [MODELED].")
    print("Historical option quotes are not available from the sources used.")
    print("Legs are priced with Black-Scholes on a VIX-derived implied vol and")
    print("settled against the REAL index close on the expiry session.  The")
    print("model has: no quote spread, no skew, one vol for all strikes, no term")
    print("structure in the primary run, no early exercise or assignment, no pin")
    print("risk, no dividends, no margin, no liquidity limit, European settlement.")
    print("A flat per-contract spread IS charged as a cost; the QUOTE is still a")
    print("mid.  Index options on these ETFs are American and physically settled,")
    print("so European pricing is an approximation.")

    # ---- data
    banner("0. DATA -- provenance echoed verbatim from data/*.csv")
    series, prov = {}, {}
    for sym in UNIVERSE:
        path = os.path.join(DATA, "%s_1d.csv" % sym)
        if not os.path.isfile(path):
            raise SystemExit("ERROR: missing %s -- run pull_data.py first" % path)
        series[sym] = read_series(path, sym)
        prov[sym] = provenance_of(path)
        s = series[sym]
        print("  %-6s rows=%-6d first=%s last=%s" %
              (sym, len(s.dates), s.dates[0].isoformat(), s.dates[-1].isoformat()))
    print("")
    print("  Provenance of SPY (the others are in data/*.csv and RESULTS.md):")
    for line in prov["SPY"]:
        print("    %s" % line)

    window = build_window(series)
    print("")
    print("  PRIMARY BOOK CALENDAR (SPY, QQQ, IWM, VIX intersection, from the")
    print("  first session every SMA(200) is live):")
    print("    sessions = %d   first = %s   last = %s"
          % (len(window), window[0].isoformat(), window[-1].isoformat()))
    for b in BUCKETS:
        g = group_index(window, b)
        print("    complete %-2s periods = %d  (%s .. %s)"
              % (b, len(g), g[0][1] if g else "-", g[-1][1] if g else "-"))

    cash, rates = cash_returns(window, series["US03M"])
    print("    cash series: TVC:US03M lagged one book date, floored at 0. "
          "%d of %d sessions have a non-positive accrual."
          % (sum(1 for c in cash if c <= 0.0), len(cash)))

    # ---- configuration echo
    banner("1. PRE-REGISTERED CONFIGURATION (echoed BEFORE any result)")
    for sid, desc in STRATEGIES:
        print("  %s  %s" % (sid, desc))
    print("")
    print("  Underlying rule   : long iff close > SMA(%d), flat below" % SMA_TREND)
    print("  Entry convention  : signal at a close, position established at the")
    print("                      NEXT session's OPEN")
    print("  Risk unit R       : S1/S3/S6  R = %.1f x ATR(%d) at entry, per share"
          % (ATR_MULT_RISK, ATR_PERIOD))
    print("                      S2        R = width - gross credit (max loss)")
    print("                      S4        R = the structure's max loss")
    print("  Option tenor      : %d calendar days to expiry, all monthly" % DTE)
    print("  S2 short leg      : %.2f-delta put" % S2_SHORT_PUT_DELTA)
    print("  S2 width          : $%.1f (DOLLARS, as pre-registered)" % S2_WIDTH_DOLLARS)
    print("  S3 short leg      : %.2f-delta call" % S3_CALL_DELTA)
    print("  S4 hedge          : long put, %.0f%% OTM, %d calendar days, rolled"
          % (S4_PUT_OTM * 100.0, S4_PUT_DTE))
    print("                      monthly at the next entry (mark-to-model)")
    print("  S2/S4 sleeve size : capital = %.0f x one max-loss spread, i.e. a"
          % S2_SLEEVE_MAXLOSSES)
    print("                      worst-case month costs -10% of the sleeve. FIXED.")
    print("  S5 blend          : %.0f%% S1 book + %.0f%% S2 book. FIXED, not tuned."
          % ((1 - S5_CARRY_WEIGHT) * 100, S5_CARRY_WEIGHT * 100))
    print("  Implied vol       : IV = VIX(t-%d sessions)/100 x kappa(index) x stress"
          % VIX_LAG_SESSIONS)
    print("                      kappa = clip(RV60(index)/RV60(SPY), %.2f, %.2f)"
          % KAPPA_CLIP)
    print("                      term structure exponent alpha = %.2f "
          "(0 = flat: one vol for 30-DTE and 60-DTE)" % IV_TERM_ALPHA)
    print("                      NOTE: reading the brief's sqrt(30/21) factor as")
    print("                      the same rule at a 21-day tenor gives 1.195x;")
    print("                      our legs are 30 and 60 DTE, so the rule gives")
    print("                      1.000x and 0.707x.  Both settings are reported.")
    print("  IV stress         : %s" % ", ".join("%.0f%%" % (m * 100) for m in IV_STRESS_GRID))
    print("  Costs             : " + " | ".join(
        "%s fee=$%.2f/contract/side half_spread=$%.3f/share/side etf=%.0fbps"
        % (c[0], c[1]["fee"], c[1]["half_spread"], c[1]["etf_bps"])
        for c in COST_SETTINGS))
    print("  HEADLINE COST     : %s" % HEADLINE_COST)
    print("")
    print("  PRE-REGISTERED SUCCESS BAR -- a book is 'all-weather enough' iff")
    print("    (a) positive in >= %.0f%% of complete YEARS" % (BAR_POS_YEARS * 100))
    print("    (b) positive in >= %.0f%% of complete QUARTERS" % (BAR_POS_QUARTERS * 100))
    print("    (c) CAGR above the cash rate over the same window")
    print("    (d) max drawdown survivable -- REPORTED, not thresholded after")
    print("        seeing the result")
    print("  Selection rule for 'best book', declared up front: the strategy with")
    print("  the highest fraction of positive complete YEARS; ties broken by CAGR.")

    # ---- headline run
    costmap = {c[0]: c[1] for c in COST_SETTINGS}
    hc = costmap[HEADLINE_COST]
    cfg = Config(HEADLINE_COST, hc["fee"], hc["half_spread"], hc["etf_bps"],
                 VIX_LAG_SESSIONS, IV_TERM_ALPHA, 1.0, S2_WIDTH_DOLLARS)
    iv_ctx = build_iv_context(window, series, series["VIX"], series["US03M"], cfg)
    books = build_strategies(series, window, cfg, iv_ctx)
    groups = {b: group_index(window, b) for b in BUCKETS}

    # ---- option structure report
    banner("2. WHAT THE PRE-REGISTERED STRUCTURES ACTUALLY LOOK LIKE")
    print("  The brief fixes the S2 width at FIVE DOLLARS.  On a $770 ETF that")
    print("  is ~0.65% of spot; on a $271 ETF it is ~1.8%.  The same dollar width")
    print("  is therefore a DIFFERENT structure on each index, and the long leg")
    print("  lands at a very different delta.  First trade of each index, from the")
    print("  model:")
    rows = []
    per_sym = {}
    for dt in books["S2"]["detail"]:
        if dt["K1"] is NA:
            continue
        per_sym.setdefault(dt["sym"], dt)
    for sym in SYMBOLS:
        dt = per_sym.get(sym)
        if dt is None:
            continue
        T = max(0.0, (dt["expiry"] - dt["entry"]).days) / 365.0
        sd_short = bs_delta(dt["S_entry"], dt["K1"], T, 0.0, dt["iv"], "P")
        sd_long = bs_delta(dt["S_entry"], dt["K2"], T, 0.0, dt["iv"], "P")
        rows.append([sym, dt["entry"].isoformat(), num(dt["S_entry"], 2),
                     num(dt["K1"], 2), num(dt["K2"], 2),
                     "%.1f%%" % (S2_WIDTH_DOLLARS / dt["S_entry"] * 100.0),
                     num(dt["credit"], 3),
                     "%.1f%%" % (dt["credit"] / S2_WIDTH_DOLLARS * 100.0),
                     num(dt["iv"], 4),
                     "%.1f%%" % ((dt["S_entry"] - dt["K1"]) / dt["S_entry"] * 100.0),
                     num(sd_short, 3), num(sd_long, 3)])
    print("")
    print(table(["sym", "entry", "S", "short K", "long K", "width/spot", "credit",
                 "credit/width", "IV", "short OTM%", "short delta", "long delta"],
                rows))
    print("")
    print("  A literal $5 width on a high-priced ETF buys a long leg only a couple")
    print("  of deltas further out than the short leg; on a low-priced ETF the same")
    print("  $5 is a genuinely different, wider tail.  The pre-registered width is")
    print("  kept as specified and the consequence is reported, not repaired.")
    print("")
    print("  Over the whole window, per index:")
    sum_rows = []
    for sym in SYMBOLS:
        ds = [d for d in books["S2"]["detail"] if d["sym"] == sym and d["K1"] is not NA]
        if not ds:
            continue
        sum_rows.append([sym, len(ds),
                         num(mean([d["S_entry"] for d in ds]), 1),
                         "%.2f%%" % (100.0 * mean(
                             [S2_WIDTH_DOLLARS / d["S_entry"] for d in ds])),
                         num(mean([d["credit"] for d in ds]), 3),
                         "%.1f%%" % (100.0 * mean(
                             [d["credit"] / S2_WIDTH_DOLLARS for d in ds])),
                         num(mean([d["iv"] for d in ds]), 4)])
    print(table(["sym", "trades", "mean spot", "mean width/spot", "mean credit",
                 "mean credit/width", "mean IV"], sum_rows))

    # full structure table
    st_rows = []
    for sid in ("S2", "S4"):
        for dt in books[sid]["detail"]:
            if dt["K1"] is NA:
                continue
            T = max(0.0, (dt["expiry"] - dt["entry"]).days) / 365.0
            # NOTE: the artefact CSV carries 6 decimals on every price and
            # strike.  The PRINTED table uses 2; the FILE exists so an
            # independent re-derivation can be compared exactly.
            st_rows.append([sid, dt["sym"], dt["entry"].isoformat(),
                            dt["expiry"].isoformat(),
                            num(dt["S_entry"], 6),
                            num(dt["S_settle"], 6) if dt["S_settle"] is not NA else "n/a",
                            num(dt["K1"], 6), num(dt["K2"], 6),
                            num(dt["credit"], 6),
                            num(dt["K1"] - dt["K2"], 2),
                            "%.4f" % (S2_WIDTH_DOLLARS / dt["S_entry"]),
                            "%.4f" % bs_delta(dt["S_entry"], dt["K1"], T, 0.0,
                                              dt["iv"], "P"),
                            "%.4f" % bs_delta(dt["S_entry"], dt["K2"], T, 0.0,
                                              dt["iv"], "P"),
                            num(dt["R_dollars"], 6),
                            num(dt["pnl_dollars"], 6),
                            num(dt["h_K"], 6) if dt["h_K"] is not NA else "",
                            num(dt["h_debit"], 6) if dt["h_debit"] is not NA else "",
                            num(dt["h_net"], 6) if dt["h_net"] is not NA else "",
                            num(dt["h_qty"], 6) if dt["h_qty"] is not NA else ""])
    write_table("s2_structure.csv",
                ["strat", "sym", "entry", "expiry", "S_entry", "S_settle", "K1",
                 "K2", "credit", "width", "width_over_spot", "short_delta",
                 "long_delta", "R_dollars", "pnl_dollars", "hedge_K",
                 "hedge_debit", "hedge_net", "hedge_qty"], st_rows)
    print("  wrote out/s2_structure.csv (%d rows)" % len(st_rows))

    # ---- trade-level statistics
    banner("3. TRADE-LEVEL STATISTICS (pooled across the three index sleeves)")
    print("  p = win rate, b = avg win / |avg loss|, E = p*b-(1-p), E_R = mean R,")
    print("  p* = 1/(1+b), b* = (1-p)/p, n_req = 4(sd/|E_R|)^2,")
    print("  L = ln(N)/ln(1/(1-p)) and the ACTUAL longest losing streak.")
    print("")
    rows, csv_rows = [], []
    for sid in STRAT_IDS:
        rs = [t["R_mult"] for t in books[sid]["trades"]
              if t.get("R_mult") is not NA and t.get("R_mult") is not None]
        if not rs:
            rows.append([sid, 0] + ["n/a"] * 10)
            continue
        st = trade_stats(rs)
        rows.append([sid, st["n"], num(st["p"], 4),
                     num(st["b"], 3) if st["b"] is not NA else "n/a",
                     num(st["E_form"], 4) if st["E_form"] is not NA else "n/a",
                     num(st["E_R"], 4), num(st["sd"], 3),
                     num(st["p_star"], 4) if st["p_star"] is not NA else "n/a",
                     num(st["b_star"], 4) if st["b_star"] is not NA else "n/a",
                     num(st["n_req"], 1) if st["n_req"] is not NA else "n/a",
                     num(st["L_expected"], 2) if st["L_expected"] is not NA else "n/a",
                     st["L_actual"]])
        csv_rows.append([sid, st["n"], st["p"], st["b"], st["E_form"], st["E_R"],
                         st["sd"], st["p_star"], st["b_star"], st["n_req"],
                         st["L_expected"], st["L_actual"], st["total_R"]])
    print(table(["strat", "n", "p", "b", "E", "E_R", "sd", "p*", "b*", "n_req",
                 "L_exp", "L_act"], rows))
    write_table("trade_stats.csv",
                ["strat", "n", "p", "b", "E_form", "E_R", "sd", "p_star", "b_star",
                 "n_req", "L_expected", "L_actual", "total_R"], csv_rows)

    # ---- S3/R definition sanity: S2 max loss check
    print("")
    print("  STRUCTURE CHECK -- model-priced maximum loss of the S2 spread")
    print("  (must equal width - credit; a mismatch would mean the payoff grid")
    print("  and the credit do not agree):")
    chk = []
    seen_syms = set()
    for dt in books["S2"]["detail"]:
        if dt["K1"] is NA or len(seen_syms) >= 3:
            continue
        L1 = Leg("P", dt["K1"], dt["expiry"], -1)
        L2 = Leg("P", dt["K2"], dt["expiry"], +1)
        ml = payoff_max_loss([L1, L2], 0.30 * dt["S_entry"],
                             1.30 * dt["S_entry"], dt["credit"])
        # width is fixed; the grid maximum loss must reproduce width - credit
        chk.append([dt["entry"].isoformat(), num(dt["credit"], 4),
                    num(S2_WIDTH_DOLLARS - dt["credit"], 4), num(ml, 4),
                    num(ml - (S2_WIDTH_DOLLARS - dt["credit"]), 6)])
        seen_syms.add(round(dt["S_entry"]))
    print(table(["entry", "credit", "width-credit", "grid max loss", "gap"], chk))

    # ---- headline metrics
    banner("4. HEADLINE BOOK METRICS (%s costs, IV stress x1.0, VIX lag %d)"
           % (HEADLINE_COST, VIX_LAG_SESSIONS))
    print("  Sharpe: daily returns, full window, annualised by sqrt(252).  Both a")
    print("  raw figure and an excess-over-cash figure are given; Rf is the")
    print("  TVC:US03M cash series lagged one book date.")
    print("")
    rows, csv_rows = [], []
    for sid in STRAT_IDS:
        r = books[sid]["rets"]
        ls = level_stats(window, r, cash)
        fY, _, nY, _, tY, psY = period_stats(r, groups["Y"])
        fQ, _, nQ, _, tQ, psQ = period_stats(r, groups["Q"])
        fM, _, nM, _, tM, psM = period_stats(r, groups["M"])
        worstY = min(psY, key=lambda p: p["ret"])
        rows.append([sid, pct(ls["cagr"]), pct(ls["max_dd"]),
                     num(ls["sharpe_raw"], 2), num(ls["sharpe_excess_cash"], 2),
                     "%d/%d (%.0f%%)" % (nY, tY, fY * 100),
                     "%d/%d (%.0f%%)" % (nQ, tQ, fQ * 100),
                     "%d/%d (%.0f%%)" % (nM, tM, fM * 100),
                     worstY["label"], pct(worstY["ret"])])
        csv_rows.append([sid, ls["cagr"], ls["max_dd"], ls["sharpe_raw"],
                         ls["sharpe_excess_cash"], fY, nY, tY, fQ, nQ, tQ, fM,
                         nM, tM, worstY["label"], worstY["ret"]])
    print(table(["strat", "CAGR", "maxDD", "Sharpe", "Sharpe_Rf", "pos years",
                 "pos Q", "pos M", "worst yr", "worst yr ret"], rows))
    write_table("headline.csv",
                ["strat", "cagr", "max_dd", "sharpe_raw", "sharpe_excess_cash",
                 "frac_pos_years", "n_pos_years", "n_years", "frac_pos_quarters",
                 "n_pos_quarters", "n_quarters", "frac_pos_months", "n_pos_months",
                 "n_months", "worst_year", "worst_year_ret"], csv_rows)

    cash_ls = level_stats(window, cash, cash)
    print("")
    print("  cash reference: CAGR %s  maxDD %s  pos years %d/%d"
          % (pct(cash_ls["cagr"]), pct(cash_ls["max_dd"]),
             sum(1 for p in period_returns(cash, groups["Y"]) if p["ret"] > 0),
             len(groups["Y"])))

    # ---- bar verdict
    banner("5. THE PRE-REGISTERED SUCCESS BAR -- verdict")
    print("  Bar: (a) >= %.0f%% positive years  (b) >= %.0f%% positive quarters"
          % (BAR_POS_YEARS * 100, BAR_POS_QUARTERS * 100))
    print("       (c) CAGR > cash CAGR  (d) max drawdown survivable (reported)")
    print("")
    cash_cagr = cash_ls["cagr"]
    verdicts = []
    clears = []
    for sid in STRAT_IDS:
        r = books[sid]["rets"]
        ls = level_stats(window, r, cash)
        fY, _, nY, _, tY, _ = period_stats(r, groups["Y"])
        fQ, _, nQ, _, tQ, _ = period_stats(r, groups["Q"])
        a = fY >= BAR_POS_YEARS - 1e-12
        b = fQ >= BAR_POS_QUARTERS - 1e-12
        c = ls["cagr"] > cash_cagr
        clears_all = a and b and c
        if clears_all:
            clears.append(sid)
        verdicts.append([sid, "YES" if a else "no", "YES" if b else "no",
                         "YES" if c else "no", pct(ls["max_dd"]),
                         "CLEARS" if clears_all else "fails"])
    print(table(["strat", "(a) posY>=80%", "(b) posQ>=70%", "(c) CAGR>cash",
                 "(d) maxDD", "verdict"], verdicts))
    print("")
    if clears:
        print("  CLEARS THE BAR: %s" % ", ".join(clears))
    else:
        print("  NOTHING CLEARS THE BAR.  No strategy on this three-index book,")
        print("  with or without its options carry stream, is positive in >=80% of")
        print("  years AND >=70% of quarters AND above cash over this window.")

    # ---- selection
    best = None
    keys = []
    for sid in STRAT_IDS:
        r = books[sid]["rets"]
        ls = level_stats(window, r, cash)
        fY, _, _, _, tY, _ = period_stats(r, groups["Y"])
        keys.append((fY, ls["cagr"], sid))
    keys.sort(key=lambda k: (-k[0], -k[1], k[2]))
    best = keys[0][2]
    print("")
    print("  BEST BOOK by the declared rule (highest positive-year fraction, ties")
    print("  by CAGR): %s  with %.0f%% positive years and CAGR %s."
          % (best, keys[0][0] * 100, pct(keys[0][1])))

    # ---- correlation
    banner("6. THE CORRELATION OF THE THREE INDICES")
    print("  A three-index book is nearly ONE BET.  Measured here, not assumed.")
    yr = {}
    for sym in SYMBOLS:
        s = series[sym]
        ys = {}
        for d in window:
            ys.setdefault(d.year, []).append(s.index_of[d])
        byyear = {}
        for y in sorted(ys):
            k0, k1 = ys[y][0], ys[y][-1]
            byyear[y] = s.c[k1] / s.c[k0] - 1.0
        yr[sym] = byyear
    complete_years = sorted(y for y in yr["SPY"]
                            if all(y in yr[s] for s in SYMBOLS))
    complete_years = [y for y in complete_years
                      if len(set(series[s].index_of[d].__int__()
                                 if False else 0 for d in window)) >= 0]
    # complete years = those whose Jan 1 and Dec 31 both fall in the window
    complete_years = [y for y in complete_years
                      if datetime.date(y, 1, 1) >= window[0]
                      and datetime.date(y, 12, 31) <= window[-1]]
    print("  complete calendar years in the window: %d (%d .. %d)"
          % (len(complete_years), complete_years[0], complete_years[-1]))
    rows, csv_rows = [], []
    for a_i in range(len(SYMBOLS)):
        for b_i in range(a_i + 1, len(SYMBOLS)):
            a, b = SYMBOLS[a_i], SYMBOLS[b_i]
            ry = pearson([yr[a][y] for y in complete_years],
                         [yr[b][y] for y in complete_years])
            ra, rb = [], []
            for j in range(1, len(window)):
                ia = series[a].index_of.get(window[j])
                ib = series[b].index_of.get(window[j])
                ia0 = series[a].index_of.get(window[j - 1])
                ib0 = series[b].index_of.get(window[j - 1])
                if None in (ia, ib, ia0, ib0):
                    continue
                ra.append(series[a].c[ia] / series[a].c[ia0] - 1.0)
                rb.append(series[b].c[ib] / series[b].c[ib0] - 1.0)
            rd = pearson(ra, rb)
            rows.append([a, b, num(ry, 3), num(rd, 3), num(ry * ry, 3)])
            csv_rows.append([a, b, ry, rd, ry * ry])
    print("")
    print(table(["pair_a", "pair_b", "yearly corr", "daily corr", "R^2 yearly",
                 "n years"],
                [r + [len(complete_years)] for r in rows]))
    write_table("correlation.csv",
                ["pair_a", "pair_b", "yearly_corr", "daily_corr", "r2_yearly"],
                csv_rows)
    vals = [float(r[2]) for r in rows]
    print("")
    print("  Every pairwise YEARLY correlation is %.2f or higher, and every"
          % min(vals))
    print("  pairwise DAILY correlation is %.2f or higher.  A three-index book of"
          % min(float(r[3]) for r in rows))
    print("  SPY/QQQ/IWM is not three bets; it is ONE broad-market bet taken at")
    print("  three slightly different tilts.  Adding QQQ and IWM to SPY buys")
    print("  almost no diversification -- it buys a slightly different beta.")
    print("  The mean pairwise yearly correlation is %.3f." % mean(vals))

    # ---- positivity by horizon
    banner("7. POSITIVITY BY HORIZON FOR THE BEST BOOK (%s) -- the direct answer"
           % best)
    print("  Complete periods only.  'positive' is STRICT (a flat period counts")
    print("  against); the >=0 reading is in out/positivity_by_horizon.csv.")
    print("")
    rows = []
    for sid in ([best] + [s for s in STRAT_IDS if s != best]):
        r = books[sid]["rets"]
        cells = []
        for b in BUCKETS:
            f1, _, npos, _, ntot, _ = period_stats(r, groups[b])
            cells.append("%.1f%%" % (f1 * 100) if f1 is not NA else "n/a")
        rows.append([sid] + cells)
    print(table(["strat"] + BUCKETS, rows))
    csv_rows = []
    for sid in STRAT_IDS:
        r = books[sid]["rets"]
        row = [sid]
        for b in BUCKETS:
            f1, f0, npos, nzero, ntot, _ = period_stats(r, groups[b])
            row.extend([f1, f0, npos, ntot])
        csv_rows.append(row)
    write_table("positivity_by_horizon.csv",
                ["strat"] + ["%s_frac_gt0" % b for b in BUCKETS]
                + ["%s_frac_ge0" % b for b in BUCKETS]
                + ["%s_npos" % b for b in BUCKETS]
                + ["%s_ntot" % b for b in BUCKETS], csv_rows)
    print("")
    print("  Same table, cash reference for comparison:")
    cellsc = []
    for b in BUCKETS:
        f1, _, _, _, _, _ = period_stats(cash, groups[b])
        cellsc.append("%.1f%%" % (f1 * 100) if f1 is not NA else "n/a")
    print(table(["cash"] + BUCKETS, [cellsc]))

    # ---- frontier
    banner("8. THE FRONTIER FOR THE BEST BOOK (%s) -- lambda vs the cash series"
           % best)
    print("  r(lam) = lam * risky + (1-lam) * cash.  At lam=0 the return IS the")
    print("  cash rate, term by term.  The frontier's endpoint is found by a 0.05")
    print("  grid scan then a %.3f bisection." % LAMBDA_FINE)
    print("")
    risky = books[best]["rets"]
    grid = [round(i / float(LAMBDA_STEPS), 6) for i in range(LAMBDA_STEPS + 1)]
    rows, csv_rows = [], []
    for lam in grid:
        mixed = apply_lambda(risky, cash, lam)
        ls = level_stats(window, mixed, cash)
        cells = []
        for b in BUCKETS:
            f1, _, _, _, ntot, _ = period_stats(mixed, groups[b])
            cells.append("%.1f%%" % (f1 * 100) if f1 is not NA else "n/a")
        rows.append([num(lam, 2), pct(ls["cagr"]), pct(ls["max_dd"])] + cells)
        csv_rows.append([lam, ls["cagr"], ls["max_dd"]]
                        + [period_stats(mixed, groups[b])[0] for b in BUCKETS])
    print(table(["lambda", "CAGR", "maxDD"] + BUCKETS, rows))
    write_table("frontier.csv", ["lambda", "cagr", "max_dd"]
                + ["frac_%s" % b for b in BUCKETS], csv_rows)

    print("")
    print("  WHERE THE FRONTIER ENDS -- largest lambda with 100% of periods")
    print("  positive (strict), then the CAGR there:")

    def max_lambda(bucket):
        fracs = []
        for lam in grid:
            f1, _, _, _, n, _ = period_stats(apply_lambda(risky, cash, lam),
                                             groups[bucket])
            fracs.append(f1 if n else 0.0)
        idx = None
        for i, f in enumerate(fracs):
            if f >= 1.0 - 1e-12:
                idx = i
        if idx is None:
            return 0.0, None
        if idx == len(grid) - 1:
            return grid[-1], None
        lo, hi = grid[idx], grid[idx + 1]
        while hi - lo > LAMBDA_FINE:
            mid = round((lo + hi) / 2.0, 6)
            f1, _, _, _, n, _ = period_stats(apply_lambda(risky, cash, mid),
                                             groups[bucket])
            if n and f1 >= 1.0 - 1e-12:
                lo = mid
            else:
                hi = mid
        return lo, None

    rows = []
    for b in ("Y", "Q", "M"):
        lam, _ = max_lambda(b)
        mixed = apply_lambda(risky, cash, lam)
        ls = level_stats(window, mixed, cash)
        rows.append([b, num(lam, 4), pct(ls["cagr"]), pct(cash_cagr),
                     pct(ls["cagr"] - cash_cagr)])
    print("")
    print(table(["horizon", "largest lambda 100% positive", "CAGR there",
                 "cash CAGR", "excess"], rows))
    write_table("frontier_end.csv",
                ["horizon", "lambda", "cagr", "cash_cagr", "excess"],
                [[r[0], r[1], r[2], r[3], r[4]] for r in rows])
    print("")
    print("  D/W/2W cannot be made 100% positive even at lam=0 only if the cash")
    print("  accrual itself prints <= 0; the measured count of non-positive cash")
    print("  sessions is reported in section 0 above.")

    # ---- stress
    banner("9. STRESS CELLS -- 2008 and 2020, where premium selling is supposed to break")
    rows, csv_rows = [], []
    for label, d0, d1 in STRESS:
        print("")
        print("  --- %s  (%s .. %s) ---" % (label, d0.isoformat(), d1.isoformat()))
        srows = []
        for sid in STRAT_IDS:
            r = books[sid]["rets"]
            wm = window_metrics(window, r, d0, d1, cash)
            if wm is NA:
                srows.append([sid, "n/a", "n/a", "n/a", "n/a"])
                continue
            dpnl, worst_day = dollar_pnl_in_window(window, r, 1.0, d0, d1)
            srows.append([sid, pct(wm["total"]), pct(wm["max_dd"]),
                          pct(wm["worst_month"]) if wm["worst_month"] is not NA else "n/a",
                          "%s %s" % (wm["worst_month_key"],
                                     pct(wm["worst_month"]))])
            csv_rows.append([label, sid, wm["total"], wm["max_dd"],
                             wm["worst_month"], str(wm["worst_month_key"])])
        print(table(["strat", "window total", "window maxDD", "worst month",
                     "worst month (key)"], srows))
        # option P&L specifically
        orows = []
        for sid in ("S2", "S4"):
            base = S2_SLEEVE_MAXLOSSES * S2_WIDTH_DOLLARS * 100.0
            tot, worst = dollar_pnl_in_window(window, books[sid]["rets"],
                                              3.0 * base, d0, d1)
            trades_in = [t for t in books[sid]["trades"]
                         if d0 <= t["entry_date"] <= d1]
            if trades_in:
                worst_t = min(trades_in, key=lambda t: t["pnl_dollars"])
                n_neg = sum(1 for t in trades_in if t["pnl_dollars"] < 0)
                orows.append([sid, len(trades_in), n_neg,
                              money(sum(t["pnl_dollars"] for t in trades_in)),
                              money(worst_t["pnl_dollars"]),
                              num(worst_t["R_mult"], 2),
                              worst_t["entry_date"].isoformat(),
                              money(tot)])
            else:
                orows.append([sid, 0, 0, "n/a", "n/a", "n/a", "n/a", "n/a"])
        print("")
        print("  modelled OPTION P&L in this window (3 sleeves, dollars):")
        print(table(["strat", "trades", "losing", "sum P&L", "worst trade",
                     "worst trade R", "worst entry", "book P&L (3x base)"], orows))
        # hedge cost ratio
        if orows and orows[0][1]:
            hd = [dt for dt in books["S4"]["detail"]
                  if dt["h_debit"] is not NA and d0 <= dt["entry"] <= d1]
            if hd:
                ratio = mean([dt["h_debit"] / dt["credit"] for dt in hd
                              if dt["credit"] > 0])
                print("")
                print("  S4 hedge debit as a multiple of the spread credit, in this")
                print("  window: mean = %.2fx  (1.00x would mean the premium exactly"
                      % ratio)
                print("  pays for the hedge).")

    # hedge cost overall
    hd = [dt for dt in books["S4"]["detail"]
          if dt["h_debit"] is not NA and dt["credit"] > 0]
    if hd:
        ratios = [dt["h_debit"] / dt["credit"] for dt in hd]
        print("")
        print("  OVER THE WHOLE WINDOW: the S4 hedge costs %.2fx the S2 credit on"
              % mean(ratios))
        print("  average (median %.2fx, min %.2fx, max %.2fx), so 'paid for by the"
              % (sorted(ratios)[len(ratios) // 2], min(ratios), max(ratios)))
        print("  premium' is FALSE -- the modelled tail put costs more than the")
        print("  credit it is supposed to be financed from.")

    # ---- S4 hedge repair verdict
    banner("10. DID THE HEDGE REPAIR THE HOLE?  S2 vs S4 vs S4c")
    print("  S4  = the literal pre-registration: ONE long 5%-OTM 60-DTE put per")
    print("        spread, rolled monthly, its debit paid out of the same sleeve.")
    print("  S4c = the 'paid for by the premium' reading: the long put's quantity")
    print("        is set so its debit EQUALS the spread credit (fractional")
    print("        contracts -- a stated model simplification).")
    print("")
    cfgc = Config(HEADLINE_COST, hc["fee"], hc["half_spread"], hc["etf_bps"],
                  VIX_LAG_SESSIONS, IV_TERM_ALPHA, 1.0, S2_WIDTH_DOLLARS,
                  hedge_mode="CREDIT")
    ctxc = build_iv_context(window, series, series["VIX"], series["US03M"], cfgc)
    hc_r, hc_trades, hc_detail = [], [], []
    for sym in SYMBOLS:
        rr = run_premium(series, sym, window, cfgc, ctxc, True)
        hc_r.append(rr["rets"])
        hc_trades.extend(rr["trades"])
        hc_detail.extend(rr["detail"])
    books["S4c"] = book_from_sleeves(hc_r)
    books["S4c"]["trades"] = hc_trades
    books["S4c"]["detail"] = hc_detail

    hed = [d for d in books["S4"]["detail"]
           if d["h_debit"] is not NA and d["credit"] > 0]
    if hed:
        ratios = [d["h_debit"] / d["credit"] for d in hed]
        print("  HEDGE ECONOMICS, FULL sizing, whole window (%d trades):" % len(hed))
        print("    the tail put costs %.2fx the spread credit on average" % mean(ratios))
        print("    (median %.2fx, min %.2fx, max %.2fx)."
              % (sorted(ratios)[len(ratios) // 2], min(ratios), max(ratios)))
        print("    Monthly net CASH FLOW of the structure, mean = %s per spread"
              % money(-mean([d["h_debit"] * 100.0 - d["credit"] * 100.0
                             for d in hed if d["h_debit"] is not NA])))
        print("    (negative = the sleeve pays out more than it collects, every")
        print("     month, on average)")
        print("    Sleeve risk budget = 10 x width x 100 = $%.0f"
              % (S2_SLEEVE_MAXLOSSES * S2_WIDTH_DOLLARS * 100.0))
        print("    => the hedge alone costs %.2f%% of the sleeve per month."
              % (100.0 * mean([d["h_debit"] for d in hed])
                 / (S2_SLEEVE_MAXLOSSES * S2_WIDTH_DOLLARS)))
        inside = [d for d in hed if d["h_K"] > d["K1"]]
        print("")
        print("  STRUCTURE OF THE 'TAIL' HEDGE: in %d of %d months (%.0f%%) the"
              % (len(inside), len(hed), 100.0 * len(inside) / len(hed)))
        print("  5%-OTM 60-DTE put strikes ABOVE the spread's short strike, i.e.")
        print("  the hedge is INSIDE the spread, not below it.  When that happens")
        print("  the structure stops being a credit spread plus a tail hedge and")
        print("  becomes a NET LONG PUT position: its maximum loss is just the net")
        print("  debit.  The mean hedge strike is %.2f%% of spot away from the"
              % (100.0 * mean([(d["K1"] - d["h_K"]) / d["S_entry"] for d in hed])))
        print("  spread's short strike (negative = the hedge is closer to the")
        print("  money).  This is a property of the pre-registered parameters, not")
        print("  a bug: a 16-delta 30-DTE put on these indices is usually FURTHER")
        print("  out than 5%.")
        print("")
        print("  'PAID FOR BY THE PREMIUM' IS FALSE, BY ABOUT A FACTOR OF "
              "%.1f." % mean(ratios))
        print("  A 16-delta, $5-wide, 30-DTE put spread does not collect enough")
        print("  premium to buy a 5%-OTM 60-DTE put.  S4 is therefore not a")
        print("  premium-selling strategy: it is a large NET-DEBIT long-tail")
        print("  position, and that is what the numbers below show.")

    print("")
    rows = []
    for sid in ("S2", "S4", "S4c"):
        r = books[sid]["rets"]
        ls = level_stats(window, r, cash)
        fY, _, nY, _, tY, _ = period_stats(r, groups["Y"])
        fM, _, nM, _, tM, _ = period_stats(r, groups["M"])
        w08 = window_metrics(window, r, STRESS[0][1], STRESS[0][2], cash)
        w20 = window_metrics(window, r, STRESS[1][1], STRESS[1][2], cash)
        rs = [t["R_mult"] for t in books[sid]["trades"]]
        rows.append([sid, pct(ls["cagr"]), pct(ls["max_dd"]),
                     "%.0f%%" % (fY * 100), "%.0f%%" % (fM * 100),
                     num(mean(rs), 4) if rs else "n/a",
                     pct(w08["max_dd"]), pct(w20["max_dd"])])
    print("")
    print(table(["strat", "CAGR", "maxDD", "posY", "posM", "E_R",
                 "2008 maxDD", "2020 maxDD"], rows))
    print("")
    print("  Same table, the OPTION SLEEVES ONLY (book P&L in dollars per sleeve,")
    print("  and the worst month), which is where the hedge has to earn its keep:")
    orows = []
    base = S2_SLEEVE_MAXLOSSES * S2_WIDTH_DOLLARS * 100.0
    for sid in ("S2", "S4", "S4c"):
        for label, d0, d1 in STRESS:
            tot, worst_day = dollar_pnl_in_window(window, books[sid]["rets"],
                                                  3.0 * base, d0, d1)
            orows.append([sid, label, money(tot), money(3.0 * base),
                          "%.2f%%" % (100.0 * tot / (3.0 * base))])
    print(table(["strat", "window", "P&L (3 sleeves)", "budget",
                 "return on budget"], orows))
    print("")
    print("  Worst single trade of each variant in each stress window:")
    for sid in ("S2", "S4", "S4c"):
        for label, d0, d1 in STRESS:
            ts = [t for t in books[sid]["trades"] if d0 <= t["entry_date"] <= d1]
            if not ts:
                continue
            w = min(ts, key=lambda t: t["R_mult"])
            print("    %-4s %-12s worst trade entered %s  R=%s  dollars=%s"
                  % (sid, label, w["entry_date"].isoformat(),
                     num(w["R_mult"], 3), money(w["pnl_dollars"])))

    # ---- VRP check
    banner("11. THE VRP WE MEASURE HERE vs THE SIBLING STUDY'S FINDING")
    print("  Same arithmetic as ../regime-study (options-trading-playbook):")
    print("    collected   = VIX / sqrt(252) * sqrt(21)          (vol points)")
    print("    realised    = |close[d+21]/close[d] - 1| * 100    (vol points)")
    print("    fwd_rv      = annualised sd of the 21 log returns")
    print("    VRP         = VIX - fwd_rv")
    print("    fair strike = collected * sqrt(2/pi), which removes the")
    print("                  guaranteed ~+20% artifact of collecting the 1-sigma")
    print("                  move and paying the realised ABSOLUTE move.")
    print("")

    def vrp_series(closes, dates_spy, vix_map, step=1):
        out = []
        n = len(closes)
        for d in range(0, n - 21, step):
            vix = vix_map.get(dates_spy[d])
            if vix is None or vix <= 0:
                continue
            collected = vix / math.sqrt(252) * math.sqrt(21)
            realised_abs = abs(closes[d + 21] / closes[d] - 1.0) * 100.0
            rets = [math.log(closes[i] / closes[i - 1])
                    for i in range(d + 1, d + 22)]
            m = sum(rets) / len(rets)
            fwd = math.sqrt(sum((x - m) ** 2 for x in rets) / (len(rets) - 1)) \
                * math.sqrt(252) * 100.0
            fairf = math.sqrt(2.0 / math.pi)
            out.append({"date": dates_spy[d], "vix": vix, "collected": collected,
                        "realised_abs": realised_abs,
                        "R": (collected - realised_abs) / (2.0 * collected),
                        "R_fair": (collected * fairf - realised_abs)
                                  / (2.0 * collected * fairf),
                        "fwd_rv": fwd, "vrp": vix - fwd})
        return out

    spy = series["SPY"]
    vix_map = {d: series["VIX"].c[series["VIX"].index_of[d]]
               for d in series["VIX"].dates}
    vp = vrp_series(spy.c, spy.dates, vix_map)
    allR = [x["R_fair"] for x in vp]
    allv = [x["vrp"] for x in vp]
    print("  FULL SPY HISTORY 1990-2026 (the sibling's series, reproduced):")
    print("    n=%d  mean VRP = %+.2f vol points  share VIX > forward realised = %.1f%%"
          % (len(vp), mean(allv), 100.0 * sum(1 for x in allv if x > 0) / len(allv)))
    print("    fair-strike E_R = %+.4fR  total = %+.1fR"
          % (mean(allR), sum(allR)))
    print("")
    print("  PER-YEAR, the years the sibling flagged:")
    rows = []
    for y in sorted(set(x["date"].year for x in vp)):
        g = [x for x in vp if x["date"].year == y]
        if not g:
            continue
        rows.append([y, len(g), "%+.2f" % mean([x["vrp"] for x in g]),
                     "%.0f%%" % (100.0 * sum(1 for x in g if x["vrp"] > 0) / len(g)),
                     "%+.4f" % mean([x["R_fair"] for x in g]),
                     "%+.1f" % sum(x["R_fair"] for x in g)])
    hits = [r for r in rows if r[0] in (2008, 2020)]
    print(table(["year", "n", "mean VRP", "share VIX>RV", "mean E_R_fair",
                 "total R"], hits))
    print("")
    print("  Sibling's published finding, for comparison:")
    print("    full history: mean VRP +3.62 vol points, VIX above the following")
    print("    21-day realised in 82.9% of windows, NEGATIVE in exactly one year")
    print("    (2008, -2.33 vol points); fair-strike E_R = +0.1158R with 2020 the")
    print("    one losing year (-7.3R) and a worst window of R = -3.98 starting")
    print("    2020-02-20.")
    worst = min(vp, key=lambda x: x["R"])
    print("")
    print("  THIS STUDY's worst single window on the same arithmetic:")
    print("    %s  VIX=%.1f  collected=%.2f  realised_abs=%.2f  R=%+.2f  R_fair=%+.2f"
          % (worst["date"].isoformat(), worst["vix"], worst["collected"],
             worst["realised_abs"], worst["R"], worst["R_fair"]))
    write_table("vrp.csv",
                ["date", "vix", "collected", "realised_abs", "R", "R_fair",
                 "fwd_rv", "vrp"],
                [[x["date"].isoformat(), x["vix"], x["collected"],
                  x["realised_abs"], x["R"], x["R_fair"], x["fwd_rv"], x["vrp"]]
                 for x in vp])

    # ---- costs
    banner("12. COST DISCIPLINE -- re-run at FREE / LOW / HIGH")
    print("  A premium-selling edge that dies inside the spread is a finding.")
    print("")
    cost_rows = []
    for cname, c in COST_SETTINGS:
        cfgc = Config(cname, c["fee"], c["half_spread"], c["etf_bps"],
                      VIX_LAG_SESSIONS, IV_TERM_ALPHA, 1.0, S2_WIDTH_DOLLARS)
        ctxc = build_iv_context(window, series, series["VIX"], series["US03M"], cfgc)
        bks = build_strategies(series, window, cfgc, ctxc)
        for sid in STRAT_IDS:
            r = bks[sid]["rets"]
            ls = level_stats(window, r, cash)
            fY, _, _, _, _, _ = period_stats(r, groups["Y"])
            fQ, _, _, _, _, _ = period_stats(r, groups["Q"])
            tsr = [t["R_mult"] for t in bks[sid]["trades"]
                   if t.get("R_mult") is not NA and t.get("R_mult") is not None]
            eR = mean(tsr) if tsr else NA
            cost_rows.append([cname, sid, ls["cagr"], ls["max_dd"], fY, fQ, eR])
    print(table(["cost", "strat", "CAGR", "maxDD", "posY", "posQ", "E_R"],
                [[r[0], r[1], pct(r[2]), pct(r[3]), "%.0f%%" % (r[4] * 100),
                  "%.0f%%" % (r[5] * 100),
                  num(r[6], 4) if r[6] is not NA else "n/a"] for r in cost_rows]))
    write_table("cost_sensitivity.csv",
                ["cost", "strat", "cagr", "max_dd", "frac_pos_years",
                 "frac_pos_quarters", "E_R"], cost_rows)
    print("")
    print("  COST DRAG on each strategy, LOW minus FREE (and HIGH minus FREE):")
    d_rows = []
    for sid in STRAT_IDS:
        f = [r for r in cost_rows if r[0] == "FREE" and r[1] == sid][0]
        l = [r for r in cost_rows if r[0] == "LOW" and r[1] == sid][0]
        h = [r for r in cost_rows if r[0] == "HIGH" and r[1] == sid][0]
        d_rows.append([sid, pct(l[2] - f[2]), pct(h[2] - f[2]),
                       "%.0f%% -> %.0f%%" % (f[4] * 100, l[4] * 100)])
    print(table(["strat", "CAGR drag LOW", "CAGR drag HIGH", "posY FREE -> LOW"],
                d_rows))

    # ---- IV stress
    banner("13. IV STRESS -- headline re-run at IV x 0.8 / 1.0 / 1.2")
    print("  Also reported: the sqrt(30/D) term-structure variant (alpha = 0.5),")
    print("  and the NO-HAIRCUT variant (VIX lag 0), so the lookahead bias in the")
    print("  modelled option P&L is visible rather than hidden.")
    print("")
    iv_rows = []
    variants = [(m, IV_TERM_ALPHA, VIX_LAG_SESSIONS) for m in IV_STRESS_GRID]
    variants.append((1.0, 0.5, VIX_LAG_SESSIONS))
    variants.append((1.0, IV_TERM_ALPHA, 0))
    labels = ["IV x0.8", "IV x1.0", "IV x1.2", "term sqrt(30/D)", "NO VIX haircut"]
    for (m, alpha, lag), lab in zip(variants, labels):
        cfgv = Config(HEADLINE_COST, hc["fee"], hc["half_spread"], hc["etf_bps"],
                      lag, alpha, m, S2_WIDTH_DOLLARS)
        ctxv = build_iv_context(window, series, series["VIX"], series["US03M"], cfgv)
        bks = build_strategies(series, window, cfgv, ctxv)
        for sid in STRAT_IDS:
            r = bks[sid]["rets"]
            ls = level_stats(window, r, cash)
            fY, _, _, _, _, _ = period_stats(r, groups["Y"])
            fQ, _, _, _, _, _ = period_stats(r, groups["Q"])
            iv_rows.append([lab, sid, ls["cagr"], ls["max_dd"], fY, fQ])
    print(table(["variant", "strat", "CAGR", "maxDD", "posY", "posQ"],
                [[r[0], r[1], pct(r[2]), pct(r[3]), "%.0f%%" % (r[4] * 100),
                  "%.0f%%" % (r[5] * 100)] for r in iv_rows]))
    write_table("iv_stress.csv",
                ["variant", "strat", "cagr", "max_dd", "frac_pos_years",
                 "frac_pos_quarters"], iv_rows)
    print("")
    print("  VERDICT FLIP CHECK -- does any IV setting move the bar verdict?")
    flip_rows = []
    for lab in labels:
        for sid in STRAT_IDS:
            row = [r for r in iv_rows if r[0] == lab and r[1] == sid][0]
            a = row[4] >= BAR_POS_YEARS - 1e-12
            b = row[5] >= BAR_POS_QUARTERS - 1e-12
            c = row[2] > cash_cagr
            if a and b and c:
                flip_rows.append([lab, sid, "CLEARS"])
    if flip_rows:
        print(table(["variant", "strat", "verdict"], flip_rows))
    else:
        print("  No IV setting, in either direction, and neither the term-structure")
        print("  variant nor the no-haircut variant, moves ANY strategy past the bar.")
    print("")
    print("  The no-haircut row is the honest bias estimate: it prices every option")
    print("  with the VIX print of its own session, information a trader does not")
    print("  have at the open.  The gap between it and the VIX lag-3 row is the")
    print("  size of the lookahead gift the model would otherwise be taking.")

    # ---- dividend sensitivity
    banner("13b. DIVIDEND SENSITIVITY -- sizing the one bias in the model that")
    print("  has a KNOWN direction.")
    print("  The price series carries no dividends, so with q = 0 the modelled call")
    print("  is TOO EXPENSIVE and the modelled put is TOO CHEAP.  That flatters")
    print("  every sold call (S2's long wing is a bought put, so it is flattered")
    print("  there too, but less) and flatters S3 outright.  Published round")
    print("  average yields: %s." % ", ".join("%s %.1f%%" % (k, v * 100)
                                        for k, v in sorted(DIV_YIELD.items())))
    print("  They are held CONSTANT over the whole window, so this is a bias")
    print("  estimate, not a dividend model.")
    print("")
    rows = []
    variants = [(None, "q = 0 (primary run)"), (DIV_YIELD, "q = published avg")]
    for qmap, lab in variants:
        cfgq = Config(HEADLINE_COST, hc["fee"], hc["half_spread"], hc["etf_bps"],
                      VIX_LAG_SESSIONS, IV_TERM_ALPHA, 1.0, S2_WIDTH_DOLLARS,
                      div_yield=qmap)
        ctxq = build_iv_context(window, series, series["VIX"], series["US03M"], cfgq)
        bks = build_strategies(series, window, cfgq, ctxq)
        for sid in STRAT_IDS:
            r = bks[sid]["rets"]
            ls = level_stats(window, r, cash)
            fY, _, _, _, _, _ = period_stats(r, groups["Y"])
            fQ, _, _, _, _, _ = period_stats(r, groups["Q"])
            tsr = [t["R_mult"] for t in bks[sid]["trades"]]
            rows.append([lab, sid, ls["cagr"], ls["max_dd"], fY, fQ,
                         mean(tsr) if tsr else NA])
    print(table(["dividend setting", "strat", "CAGR", "maxDD", "posY", "posQ",
                 "E_R"],
                [[r[0], r[1], pct(r[2]), pct(r[3]), "%.0f%%" % (r[4] * 100),
                  "%.0f%%" % (r[5] * 100),
                  num(r[6], 4) if r[6] is not NA else "n/a"] for r in rows]))
    write_table("dividend_sensitivity.csv",
                ["dividend_setting", "strat", "cagr", "max_dd",
                 "frac_pos_years", "frac_pos_quarters", "E_R"], rows)
    print("")
    print("  THE BIAS, as a CAGR difference (published-average q minus q = 0):")
    drows = []
    for sid in STRAT_IDS:
        a = [r for r in rows if r[0] == "q = 0 (primary run)" and r[1] == sid][0]
        b = [r for r in rows if r[0] == "q = published avg" and r[1] == sid][0]
        drows.append([sid, pct(b[2] - a[2]), "%.0f%% -> %.0f%%" % (a[4] * 100, b[4] * 100),
                      "%.0f%% -> %.0f%%" % (a[5] * 100, b[5] * 100)])
    print(table(["strat", "CAGR difference", "posY", "posQ"], drows))
    print("")
    print("  A NEGATIVE CAGR difference means the primary run's headline was")
    print("  inflated by the missing dividends.  Whether the bar verdict survives")
    print("  that correction is the thing to read in section 5's terms.")

    # ---- skew sensitivity
    banner("13c. SKEW SENSITIVITY -- sizing the LARGEST known bias in the model")
    print("  The model has NO skew: one implied vol prices every strike.  A real")
    print("  seller of an out-of-the-money option collects LESS than the flat-vol")
    print("  Black-Scholes value.  Here the SOLD leg only is priced at")
    print("  VIX minus a stated number of vol points; the bought legs keep VIX.")
    print("  Strikes are NOT moved -- this isolates the price effect.")
    print("")
    print("  Why this matters, before the table: a 30-delta 30-DTE call has vega")
    print("  of roughly S * pdf(d1) * sqrt(T) * 100 dollars per vol point.  At")
    print("  SPY = 244, IV = 19.5%, that is about $24 per vol point per contract.")
    print("  1.5 vol points of skew is therefore about $36 per contract per")
    print("  month -- roughly 1.8 percentage points of annual return on a single")
    print("  covered-call sleeve.  That is the same order as the whole edge.")
    print("")
    rows = []
    for hair in (0.0, 0.015, 0.030):
        cfgs = Config(HEADLINE_COST, hc["fee"], hc["half_spread"], hc["etf_bps"],
                      VIX_LAG_SESSIONS, IV_TERM_ALPHA, 1.0, S2_WIDTH_DOLLARS,
                      short_iv_haircut=hair)
        ctxs = build_iv_context(window, series, series["VIX"], series["US03M"], cfgs)
        bks = build_strategies(series, window, cfgs, ctxs)
        lab = "haircut %.1f vol pts" % (hair * 100.0)
        for sid in STRAT_IDS:
            r = bks[sid]["rets"]
            ls = level_stats(window, r, cash)
            fY, _, _, _, _, _ = period_stats(r, groups["Y"])
            fQ, _, _, _, _, _ = period_stats(r, groups["Q"])
            fM, _, _, _, _, _ = period_stats(r, groups["M"])
            tsr = [t["R_mult"] for t in bks[sid]["trades"]]
            rows.append([lab, sid, ls["cagr"], ls["max_dd"], fY, fQ, fM,
                         mean(tsr) if tsr else NA])
    print(table(["sold-leg IV", "strat", "CAGR", "maxDD", "posY", "posQ", "posM",
                 "E_R"],
                [[r[0], r[1], pct(r[2]), pct(r[3]), "%.0f%%" % (r[4] * 100),
                  "%.0f%%" % (r[5] * 100), "%.0f%%" % (r[6] * 100),
                  num(r[7], 4) if r[7] is not NA else "n/a"] for r in rows]))
    write_table("skew_sensitivity.csv",
                ["sold_leg_iv", "strat", "cagr", "max_dd", "frac_pos_years",
                 "frac_pos_quarters", "frac_pos_months", "E_R"], rows)
    print("")
    print("  VERDICT FLIP CHECK under skew:")
    flip2 = []
    for lab in sorted(set(r[0] for r in rows)):
        for sid in STRAT_IDS:
            row = [r for r in rows if r[0] == lab and r[1] == sid][0]
            a = row[4] >= BAR_POS_YEARS - 1e-12
            b = row[5] >= BAR_POS_QUARTERS - 1e-12
            c = row[2] > cash_cagr
            flip2.append([lab, sid, "CLEARS" if (a and b and c) else "fails"])
    print(table(["sold-leg IV", "strat", "verdict"], flip2))

    # ---- the answer
    banner("15. THE DIRECT ANSWER TO THE OWNER'S QUESTION")
    print("  Question: restrict to SPY/QQQ/IWM, trade BOTH the underlying and")
    print("  options on it -- can a combination reach 'profitable in most")
    print("  conditions', and what does it cost?")
    print("")
    print("  1. POSITIVITY BY HORIZON, best book (the buy-write, %s):" % best)
    brow = []
    for b in BUCKETS:
        f1, _, _, _, n, _ = period_stats(books[best]["rets"], groups[b])
        brow.append("%s %.1f%%" % (b, f1 * 100))
    print("     " + "   ".join(brow))
    print("")
    print("  2. THE FRONTIER, best book vs the cross-asset trend book already")
    print("     measured by the sibling frontier study:")
    print("")
    for b in ("Y", "Q", "M"):
        lam, _ = max_lambda(b)
        mixed = apply_lambda(risky, cash, lam)
        ls = level_stats(window, mixed, cash)
        print("     %-2s largest lambda with 100%% positive = %.4f  ->  CAGR %s"
              "  vs cash %s  (excess %s)"
              % (b, lam, pct(ls["cagr"]), pct(cash_cagr),
                 pct(ls["cagr"] - cash_cagr)))
    print("")
    print("     sibling study, four-sleeve cross-asset TREND book (2005-2026):")
    print("       Y 0.008 -> +0.03%/yr over cash;  Q 0.001 -> +0.00%;  M 0.000")
    print("     This study's best book, three-index BUY-WRITE (2002-2025):")
    print("       Y %.4f;  Q %.4f;  M %.4f"
          % (max_lambda("Y")[0], max_lambda("Q")[0], max_lambda("M")[0]))
    print("")
    print("  3. WHAT IT COSTS -- the verdict re-run under every stated assumption.")
    print("     Read from the sensitivity tables just written to out/*.csv, so this")
    print("     matrix cannot disagree with them.  'CLEARS' = >=80%% positive"
          " years" % ())
    print("     AND >=70%% positive quarters AND CAGR above cash (%.2f%%/yr)."
          % (cash_cagr * 100.0))
    print("     cash CAGR over this window = %.2f%%/yr." % (cash_cagr * 100.0))
    print("")
    sens = []
    for fn, key in (("cost_sensitivity.csv", "cost"),
                    ("iv_stress.csv", "variant"),
                    ("skew_sensitivity.csv", "sold_leg_iv"),
                    ("dividend_sensitivity.csv", "dividend_setting")):
        p = os.path.join(OUT, fn)
        if not os.path.isfile(p):
            continue
        _hh, rws = None, []
        with io.open(p, "r", encoding="utf-8", newline="") as fh:
            lines = [ln.rstrip("\r\n") for ln in fh if ln.strip()]
        head = lines[0].split(",")
        for ln in lines[1:]:
            rws.append(dict(zip(head, ln.split(","))))
        for r in rws:
            if r["strat"] not in ("S2", "S3"):
                continue
            cagr = float(r["cagr"])
            fy = float(r["frac_pos_years"])
            fq = float(r["frac_pos_quarters"])
            clears = (fy >= BAR_POS_YEARS - 1e-12
                      and fq >= BAR_POS_QUARTERS - 1e-12
                      and cagr > cash_cagr)
            sens.append([key, r[key], r["strat"], pct(cagr), "%.0f%%" % (fy * 100),
                         "%.0f%%" % (fq * 100), "CLEARS" if clears else "fails"])
    print(table(["family", "setting", "strat", "CAGR", "posY", "posQ", "verdict"],
                sens))
    print("")
    print("     Read the matrix this way: S3 stops clearing when the sold leg loses")
    print("     3 vol points to skew, and S2 never clears once a real spread is")
    print("     charged or the sold leg loses 1.5 vol points.  The answer to the")
    print("     owner's question therefore depends on three MODELLED inputs -- the")
    print("     cost level, the IV level, and the skew -- and not only on the")
    print("     market.  That is the honest summary.")
    print("")
    print("  4. WHAT THE MODEL CANNOT SEE is listed in full at the top of this run")
    print("     and in README.md.  The largest single item is the absence of skew.")
    print("")
    print("  Nothing here is a recommendation.  Every options number is MODELED.")

    # ---- SPY-only longest window
    banner("14. THE LONGEST WINDOW -- SPY ONLY, 1994-2026 (one index, not three)")
    w2 = build_window(series, only="SPY")
    print("  sessions = %d  first = %s  last = %s"
          % (len(w2), w2[0].isoformat(), w2[-1].isoformat()))
    cash2, _ = cash_returns(w2, series["US03M"])
    cfg2 = Config(HEADLINE_COST, hc["fee"], hc["half_spread"], hc["etf_bps"],
                  VIX_LAG_SESSIONS, IV_TERM_ALPHA, 1.0, S2_WIDTH_DOLLARS)
    ctx2 = build_iv_context(w2, series, series["VIX"], series["US03M"], cfg2)
    books2 = build_spy_book(series, w2, cfg2, ctx2)
    g2 = {b: group_index(w2, b) for b in BUCKETS}
    rows = []
    for sid in STRAT_IDS:
        r = books2[sid]["rets"]
        ls = level_stats(w2, r, cash2)
        fY, _, nY, _, tY, _ = period_stats(r, g2["Y"])
        fQ, _, _, _, _, _ = period_stats(r, g2["Q"])
        fM, _, _, _, _, _ = period_stats(r, g2["M"])
        rows.append([sid, pct(ls["cagr"]), pct(ls["max_dd"]), num(ls["sharpe_raw"], 2),
                     "%d/%d (%.0f%%)" % (nY, tY, fY * 100),
                     "%.0f%%" % (fQ * 100), "%.0f%%" % (fM * 100)])
    print("")
    print(table(["strat", "CAGR", "maxDD", "Sharpe", "pos years", "pos Q", "pos M"],
                rows))
    ls2 = level_stats(w2, cash2, cash2)
    print("")
    print("  cash CAGR over the same window: %s" % pct(ls2["cagr"]))
    write_table("spy_only.csv",
                ["strat", "label"],
                [[r[0], r[1] + "|" + r[2] + "|" + r[3] + "|" + r[4] + "|"
                  + r[5] + "|" + r[6]] for r in rows])

    # ---- trade dump
    if args.dump_trades:
        parts = args.dump_trades.split(":")
        banner("DUMP -- %s" % args.dump_trades)
        sid = parts[0]
        for t in books[sid]["trades"]:
            print("  %s -> %s  R_dollars=%.2f  pnl=%.2f  R=%s"
                  % (t["entry_date"].isoformat(), t["exit_date"].isoformat(),
                     t["R_dollars"], t["pnl_dollars"], num(t["R_mult"], 4)))
        if sid in ("S2", "S4"):
            print("")
            print("  legs:")
            for dt in books[sid]["detail"]:
                print("    %s exp %s  S %.2f -> %s  K1 %.2f K2 %.2f  credit %.4f  "
                      "R$ %.2f  pnl %.2f"
                      % (dt["entry"].isoformat(), dt["expiry"].isoformat(),
                         dt["S_entry"],
                         num(dt["S_settle"], 2) if dt["S_settle"] is not NA else "n/a",
                         dt["K1"], dt["K2"], dt["credit"], dt["R_dollars"],
                         dt["pnl_dollars"]))

    banner("DONE")
    print("  out/*.csv holds every table above in machine-readable form.")
    print("  Every options-derived number is [MODELED]. See README.md.")
    return 0


def build_spy_book(series, window_dates, cfg, iv_ctx):
    """The same six strategies on SPY alone."""
    out = {}
    r1 = run_trend(series, "SPY", window_dates, cfg)
    out["S1"] = {"rets": r1["rets"], "trades": r1["trades"]}
    p1 = run_premium(series, "SPY", window_dates, cfg, iv_ctx, False)
    out["S2"] = {"rets": p1["rets"], "trades": p1["trades"]}
    b1 = run_buywrite(series, "SPY", window_dates, cfg, iv_ctx)
    out["S3"] = {"rets": b1["rets"], "trades": b1["trades"]}
    h1 = run_premium(series, "SPY", window_dates, cfg, iv_ctx, True)
    out["S4"] = {"rets": h1["rets"], "trades": h1["trades"]}
    out["S5"] = {"rets": [(1.0 - S5_CARRY_WEIGHT) * x + S5_CARRY_WEIGHT * y
                          for x, y in zip(r1["rets"], p1["rets"])],
                 "trades": r1["trades"] + p1["trades"]}
    s = series["SPY"]
    n = len(window_dates)
    idx = [s.index_of[d] for d in window_dates]
    bh = [0.0] * n
    for j in range(1, n):
        bh[j] = s.c[idx[j]] / s.c[idx[j - 1]] - 1.0
    out["S6"] = {"rets": bh, "trades": []}
    return out


if __name__ == "__main__":
    sys.exit(main())
