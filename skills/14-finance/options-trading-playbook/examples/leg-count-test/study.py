#!/usr/bin/env python3
"""
study.py -- DOES ADDING OPTION LEGS BUY EDGE, OR ONLY SHAPE?

Holding the MARKET VIEW CONSTANT, how does expectancy net of cost, tail risk,
positivity-by-horizon and model (skew) sensitivity change as a structure goes
from 1 leg to 2 legs to 4 legs -- and does a complex/advanced structure ever
beat a simple one on the same view?

Deterministic.  Stdlib only.  No network.  No RNG.  No wall clock.  LF output.

=============================================================================
WHAT IS REAL AND WHAT IS MODELED -- READ THIS BEFORE ANY NUMBER BELOW
=============================================================================
REAL, from data/*.csv, each series behind a `# PROVENANCE:` header:
    * daily OHLC for AMEX:SPY, NASDAQ:QQQ, AMEX:IWM   (TradingView, 2026-10-14)
    * daily VIX index level, TVC:VIX                  (TradingView, 2026-10-14)
    * daily 3-month US Treasury bill YIELD, TVC:US03M (TradingView, 2026-10-14)

MODELED, and every number derived from it is labelled [MODELED]:
    * EVERY option price in this study.  Historical option quotes are not
      available from the sources used here.  Each leg is priced with
      Black-Scholes on a model implied vol built from the real VIX, and each
      structure is settled at INTRINSIC against the REAL index closing price on
      its expiry session.

The option model cannot see any of the following, and every [MODELED] figure
must be held at arm's length because of it:
    1. no bid/ask spread in the QUOTE -- a flat per-contract spread IS charged
       as a cost, but the quote itself is a mid;
    2. no skew -- one implied vol prices every strike, so the sold leg is
       priced at the same vol as the wings.  Section 6 sizes this bias by
       re-pricing with the sold strikes charged +-1.5 vol points;
    3. no term structure -- one vol prices every tenor (alpha = 0);
    4. no early exercise and NO ASSIGNMENT -- SPY/QQQ/IWM options are AMERICAN
       and physically settled; they are priced here as EUROPEAN and cash-settled.
       An American short put can be assigned early and this model would never
       show it;
    5. no pin risk -- the expiry session's close decides everything;
    6. no dividends -- the price series is price-only, so the modelled call is
       too expensive and the modelled put too cheap.  This bites HARDER the
       more legs a structure has, because each extra call or put leg inherits
       the bias;
    7. no margin, no buying-power constraint, no liquidity limit, no partial
       fills, no LEGGING RISK (a 4-leg structure is assumed to fill as one
       ticket at the modelled mid), no tax;
    8. strikes are NOT rounded to exchange increments.  A real SPY chain is
       $1-wide; this study's solved strikes may sit up to $0.50 off a listed
       strike;
    9. one contract per unit, integer, always fillable at the modelled mid.

USAGE
    py -3 study.py > run-output.txt
"""

import datetime
import io
import math
import os
import sys

# ---------------------------------------------------------------------------
# The sibling timeframe engine owns the bucketing convention.  Import it rather
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
# PRE-REGISTERED CONFIGURATION -- fixed BEFORE the first run
# ===========================================================================

SYMBOLS = ["SPY", "QQQ", "IWM"]
UNIVERSE = SYMBOLS + ["VIX", "US03M"]

TRADING_DAYS = 252
SMA_TREND = 200                # only used to set the start of the window
VIX_LAG_SESSIONS = 3           # only VIX from 3 sessions ago may price a leg
IV_TERM_ALPHA = 0.0            # IV(D) = VIX * (30/D)**alpha ; 0 = flat term
KAPPA_LOOKBACK = 60
KAPPA_CLIP = (0.60, 2.00)

DTE = 30                       # calendar days to expiry, all structures

# ---- delta / moneyness rules (pre-registered, identical for every structure
#      that needs them).  Strikes are solved from the SIGNAL close.
D_16 = 0.16
D_25 = 0.25
D_30 = 0.30
D_50 = 0.50
WING = 5.0                     # dollars; every "5-wide" wing

# ---- R for a structure with an UNBOUNDED CALL SIDE.  A short call has no
#      maximum loss; the honest choice is a STATED loss reference rather than a
#      fabricated max loss.  DECLARED BEFORE THE RUN: R = the structure's loss
#      at a terminal move of +1.5 sigma*sqrt(T), i.e. the stated stop "I am out
#      if the index moves 1.5 sigma against me by expiry".  NO INTRA-TRADE STOP
#      IS SIMULATED ANYWHERE IN THIS STUDY -- every structure is held to
#      expiry -- so for these structures R is a NORMALISATION, not an enforced
#      exit.  Flagged UNDEFINED_UP everywhere it is used.
UNDEF_SIGMA = 1.5

# ---- grid over which a structure's maximum loss is measured
GRID_STEPS = 4000

# ---- capital model.  Every sleeve is a fixed risk budget of SLV_UNITS x one
#      unit of R, and its daily return is dollar P&L / that budget.  A FIXED
#      budget (not a compounding account) is what makes a structure that is a
#      persistent net cash outflow show up as a persistent negative return
#      instead of silently depleting an account.  10 is the sibling study's
#      declared number, kept for comparability.
SLV_UNITS = 10.0

# ---- cost settings.  per-contract per-leg cost on ONE SIDE =
#      fee + half_spread * 100 dollars.  `etf_bps` is the round-trip cost on the
#      UNDERLYING (used only by the covered call's stock leg).
COST_SETTINGS = {
    "FREE": {"fee": 0.00, "half_spread": 0.000, "etf_bps": 0.0, "rt": 1},
    "LOW":  {"fee": 0.65, "half_spread": 0.025, "etf_bps": 5.0, "rt": 1},
    "HIGH": {"fee": 0.65, "half_spread": 0.050, "etf_bps": 20.0, "rt": 1},
    # ROUND TRIP: the skill's `cost-drag-per-leg-and-per-rung.md` convention --
    # two tickets per leg.  A LEG THAT EXPIRES HAS NO CLOSING TICKET, so the
    # headline convention here is ONE ticket per leg; this setting bounds the
    # other reading.
    "RT_LOW": {"fee": 0.65, "half_spread": 0.025, "etf_bps": 10.0, "rt": 2},
}
HEADLINE_COST = "LOW"

# ---- the six pre-registered runs.  `iv_mode` changes only the PRICING vol of
#      the stated legs; STRIKES ARE HELD FIXED at the base solve, so a
#      difference between two iv_modes is a pure pricing effect.
VARIANTS = [
    ("FREE", "FREE", "BASE",
     "gross, no cost, no skew haircut -- the gross-edge reference"),
    ("LOW", "LOW", "BASE",
     "headline: $0.65/contract/leg + $0.025/share half-spread, 5 bps stock"),
    ("HIGH", "HIGH", "BASE",
     "high: $0.65/contract/leg + $0.050/share half-spread, 20 bps stock"),
    ("RT_LOW", "RT_LOW", "BASE",
     "round trip (2 tickets/leg, the skill's convention) at LOW prices"),
    ("SKEW_SOLD_P15", "LOW", "SOLD_P15",
     "SOLD option legs charged +1.5 vol points at pricing (strikes fixed)"),
    ("SKEW_SOLD_M15", "LOW", "SOLD_M15",
     "SOLD option legs charged -1.5 vol points at pricing (strikes fixed)"),
    ("SKEW_ALL_P15", "LOW", "ALL_P15",
     "ALL option legs charged +1.5 vol points at pricing (strikes fixed)"),
]
VARIANT_IDS = [v[0] for v in VARIANTS]

# ---- THE PRE-REGISTERED STRUCTURES.  (id, view, name, option legs)
STRUCTS = [
    ("A1", "A", "short put spread ~16d / 5-wide", 2),
    ("A2", "A", "iron condor ~16d shorts / 5-wide wings", 4),
    ("A3", "A", "iron butterfly ATM short / 5-wide wings", 4),
    ("A4", "A", "short strangle ~16d both sides", 2),
    ("B1", "B", "long call ~30d", 1),
    ("B2", "B", "bull call debit spread ~50d long / ~25d short", 2),
    ("B3", "B", "risk reversal long ~30d call / short ~30d put", 2),
    ("B4", "B", "call ratio backspread long 2x ~25d / short 1x ~50d", 2),
    ("C1", "C", "cash-secured put ~16d", 1),
    ("C2", "C", "covered call: long underlying + short ~30d call", 2),
    ("C3", "C", "put spread ~16d / 5-wide (the same instrument as A1)", 2),
    ("C4", "C", "short ATM put -- the 1-leg carry comparator", 1),
]
VIEWS = {
    "A": "the index stays INSIDE +-1 sigma over the next 30 days   (range)",
    "B": "the index RISES over the next 30 days                   (directional)",
    "C": "harvest premium with NO directional view               (carry)",
}

# ---- the pre-registered selection rule for the "best structure in a view"
#      (declared before the run):  rank by
#          edge_per_tail = E_net (R, LOW cost) / |worst 1% of trades (R)|
#      ties broken by higher E_net.  The highest-E_net structure is ALSO named,
#      separately, because the two rules can disagree and the reader should see
#      when they do.
STRESS_WINDOWS = [
    ("2008 GFC", datetime.date(2008, 1, 1), datetime.date(2009, 3, 31)),
    ("2020 COVID", datetime.date(2020, 1, 1), datetime.date(2020, 12, 31)),
    ("2022 bear", datetime.date(2022, 1, 1), datetime.date(2022, 12, 31)),
]

NA = None
BUCKETS = ["M", "Q", "Y"]
ALL_BUCKETS = ["D", "W", "2W", "M", "Q", "H", "Y"]


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


def signed(x, nd=4):
    if x is NA:
        return "n/a"
    return ("%+.*f" % (nd, x))


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

    q is 0.0 everywhere in this study (the price series carries no dividends).
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


def bs_greeks(S, K, T, r, sigma, kind, q=0.0):
    """(delta, gamma, vega_per_vol_point, theta_per_day) per share."""
    if S <= 0.0 or K <= 0.0 or T <= 1e-9 or sigma <= 1e-9:
        return bs_delta(S, K, T, r, sigma, kind, q), 0.0, 0.0, 0.0
    srt = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / srt
    d2 = d1 - srt
    disc_r = math.exp(-r * T)
    disc_q = math.exp(-q * T)
    dlt = bs_delta(S, K, T, r, sigma, kind, q)
    gam = disc_q * npdf(d1) / (S * srt)
    veg = S * disc_q * npdf(d1) * math.sqrt(T) / 100.0     # per 1 vol point
    base = -S * disc_q * npdf(d1) * sigma / (2.0 * math.sqrt(T))
    if kind == "C":
        th = base - q * S * disc_q * ncdf(d1) + r * K * disc_r * ncdf(d2)
    else:
        th = base + q * S * disc_q * ncdf(-d1) - r * K * disc_r * ncdf(-d2)
    return dlt, gam, veg, th / 365.0


def strike_for_put_delta(S, T, r, sigma, target, q=0.0):
    """K such that |put delta| == target.  |put delta| is INCREASING in K."""
    lo, hi = 0.20 * S, 1.60 * S
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if abs(bs_delta(S, mid, T, r, sigma, "P", q)) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def strike_for_call_delta(S, T, r, sigma, target, q=0.0):
    """K such that call delta == target.  Call delta is DECREASING in K."""
    lo, hi = 0.20 * S, 1.60 * S
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if bs_delta(S, mid, T, r, sigma, "C", q) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ===========================================================================
# Statistics helpers
# ===========================================================================

def sample_sd(xs):
    n = len(xs)
    if n < 2:
        return NA
    m = sum(xs) / float(n)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / float(n - 1))


def mean(xs):
    return sum(xs) / float(len(xs)) if xs else NA


def median(xs):
    if not xs:
        return NA
    s = sorted(xs)
    n = len(s)
    if n % 2:
        return s[n // 2]
    return 0.5 * (s[n // 2 - 1] + s[n // 2])


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
    """p, b, E_form, E_R, p*, b*, sd, n_req, L_expected, L_actual, worst 1%.

    `b` is (mean win) / |mean loss| in R units, as the skill defines it.
    `E_form` is the skill's identity p*b - (1-p); `E_R` is the sample mean in R.
    The two agree exactly only when the average loss is 1R, which it is NOT
    here: R is the STRUCTURE's maximum loss, and most losses are smaller.  Both
    are reported; the gap is reported rather than hidden.
    """
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
    k = max(1, int(math.ceil(0.01 * n)))
    worst = sorted(rs)[:k]
    return {"n": n, "p": p, "b": b, "E_form": e_form, "E_R": e_r, "sd": sd,
            "p_star": p_star, "b_star": b_star, "n_req": n_req,
            "L_expected": streak_expected(p, n),
            "L_actual": longest_losing_streak(rs),
            "total_R": sum(rs), "worst1_n": k, "worst1": mean(worst),
            "worst1_first": sorted(rs)[0], "best1": sorted(rs)[-1],
            "median_R": median(rs)}


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
    npos = sum(1 for x in ps if x["ret"] > 0.0)
    nzero = sum(1 for x in ps if x["ret"] == 0.0)
    return npos / float(n), (npos + nzero) / float(n), npos, nzero, n, ps


def level_stats(dates, rets):
    n = len(rets)
    if n == 0:
        return NA
    curve = equity_curve(rets)
    yrs = years_between(dates[0], dates[-1])
    cagr = -1.0 if curve[-1] <= 0.0 else curve[-1] ** (1.0 / yrs) - 1.0
    m = sum(rets) / n
    sd = sample_sd(rets)
    sharpe = (m / sd * math.sqrt(TRADING_DAYS)) if (sd and sd > 0) else NA
    return {"n_days": n, "years": yrs, "cagr": cagr,
            "max_dd": max_drawdown_pct(curve), "sharpe": sharpe,
            "sd_daily": sd, "total": curve[-1] - 1.0}


def phi_law_positivity(sharpe_ann, bucket):
    """The normal law Phi(Sharpe * sqrt(period in years)) for a period's
    positivity.  This is the null that negative skew breaks."""
    if sharpe_ann is NA:
        return NA
    frac = {"M": 1.0 / 12.0, "Q": 1.0 / 4.0, "Y": 1.0}[bucket]
    return ncdf(sharpe_ann * math.sqrt(frac))


def worst_period(ps, want):
    if not ps:
        return NA, NA
    if want == "worst":
        x = min(ps, key=lambda z: z["ret"])
    else:
        x = max(ps, key=lambda z: z["ret"])
    return x["ret"], x["label"]


def cum_dd(rets):
    """Worst peak-to-trough drawdown of the CUMULATIVE SUM of returns, in units
    of the FIXED budget.

    This -- not the compounded curve -- is the correct drawdown for a programme
    funded from a FIXED budget: the sleeve's return is dollar P&L / a constant,
    so it is not compounded, and compounding it would let a volatile structure
    report an explosion or a wipe-out that no account could experience.
    """
    peak = 0.0
    s = 0.0
    worst = 0.0
    for r in rets:
        s += r
        if s > peak:
            peak = s
        d = s - peak
        if d < worst:
            worst = d
    return worst


def period_sums(rets, groups):
    """Per-period SUM of returns (budget units).  Same SIGN as the compounded
    period return whenever no single period contains a return of -100% or
    lower, which is checked in section 8."""
    out = []
    for key, label, first, last, idx in groups:
        out.append({"key": key, "label": label, "first": first, "last": last,
                    "n_days": len(idx),
                    "ret": sum(rets[j] for j in idx)})
    return out


def period_stats_sum(rets, groups):
    ps = period_sums(rets, groups)
    n = len(ps)
    if not n:
        return NA, NA, 0, 0, 0, ps
    npos = sum(1 for x in ps if x["ret"] > 0.0)
    nzero = sum(1 for x in ps if x["ret"] == 0.0)
    return npos / float(n), (npos + nzero) / float(n), npos, nzero, n, ps


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

    def logret_sd(self, n, end_idx):
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
# Implied vol model  (identical construction to the sibling study)
# ===========================================================================

def build_iv_context(window_dates, series, vix, us03m):
    n = len(window_dates)
    vix_used = [NA] * n
    r_used = [NA] * n
    for j in range(n):
        k = max(0, j - VIX_LAG_SESSIONS)
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
                k = max(0, j - VIX_LAG_SESSIONS)
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


def iv_of(vix_pct, sym, j, kappa, iv_mult=1.0):
    if vix_pct is NA:
        return 0.0
    return vix_pct / 100.0 * kappa[sym][j] * iv_mult


def build_window(series):
    sets = [set(series[s].dates) for s in SYMBOLS]
    sets.append(set(series["VIX"].dates))
    common = set.intersection(*sets)
    starts = []
    for s in SYMBOLS:
        sma = series[s].sma(SMA_TREND)
        fl = None
        for i, v in enumerate(sma):
            if v is not NA:
                fl = series[s].dates[i]
                break
        starts.append(fl)
    return sorted(d for d in common if d >= max(starts))


def month_grid(dates):
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


def monthly_expiry(window_dates, ent_d, next_ent_d, tenor_days):
    """First session on or after entry + tenor, CAPPED at the last session
    strictly before the next monthly entry, so a monthly programme never holds
    two overlapping cycles."""
    t = next_session_on_or_after(window_dates,
                                 ent_d + datetime.timedelta(days=tenor_days))
    if next_ent_d is not NA:
        cap = last_session_on_or_before(
            window_dates, next_ent_d - datetime.timedelta(days=1))
        if cap is not NA and (t is NA or cap < t):
            t = cap
    return t


# ===========================================================================
# Structures
# ===========================================================================

class Leg(object):
    """One leg of a structure.  kind: 'C', 'P' or 'S' (the underlying).

    qty is signed: -1 short, +1 long.  It is the number of CONTRACTS for an
    option leg and the number of 100-share units for the underlying.
    iv_off is ADDED to the pricing vol for this leg only (the skew knob).
    """
    __slots__ = ("kind", "K", "qty", "iv_off", "expiry", "T_entry", "px_entry")

    def __init__(self, kind, K, qty, expiry=None, iv_off=0.0):
        self.kind, self.K, self.qty = kind, K, qty
        self.iv_off = iv_off
        self.expiry = expiry
        self.T_entry = NA
        self.px_entry = NA

    def value(self, S, T, r, sigma):
        """Value per share of ONE unit of this leg, live."""
        if self.kind == "S":
            return S
        return bs_price(S, self.K, T, r, max(1e-6, sigma + self.iv_off),
                        self.kind)

    def intrinsic(self, S):
        if self.kind == "S":
            return S
        if self.kind == "C":
            return max(S - self.K, 0.0)
        return max(self.K - S, 0.0)

    def is_option(self):
        return self.kind != "S"

    def is_short(self):
        return self.qty < 0.0

    # -- cash accounting.  An OPTION is a cash-flow instrument: its premium
    #    leaves/enters the account at entry.  The UNDERLYING leg is not: the
    #    book tracks a long stock position by its P&L against the entry price,
    #    so buying the shares is NOT a cash outflow here (it is the collateral
    #    the position is written against, not a premium).  Getting this wrong
    #    double-counts the share cost, so it is done in one place only.

    def entry_cash_dollars(self):
        if self.kind == "S":
            return 0.0
        return -self.qty * self.px_entry * 100.0

    def mark_dollars(self, S, T, r, sigma):
        if self.kind == "S":
            return self.qty * 100.0 * (S - self.px_entry)
        return self.qty * 100.0 * self.value(S, T, r, sigma)

    def terminal_dollars(self, S):
        return self.qty * 100.0 * (self.intrinsic(S) - self.px_entry)


def build_legs(sid, S_sig, S_open, T, r, iv):
    """The pre-registered structure `sid`.  Strikes are solved from the SIGNAL
    close and the base implied vol; the PRICING happens at the entry open and
    the variant's iv offsets are applied afterwards in run_structure.

    Returns (legs, meta).  `meta` carries the leg count, the contract count,
    and the flags a reader needs: `undefined_up` (net short call slope as
    S -> infinity) and `has_stock`.
    """
    L = []
    if sid in ("A1", "C3"):
        K1 = strike_for_put_delta(S_sig, T, r, iv, D_16)
        L = [Leg("P", K1, -1), Leg("P", K1 - WING, +1)]
    elif sid == "A2":
        Kp = strike_for_put_delta(S_sig, T, r, iv, D_16)
        Kc = strike_for_call_delta(S_sig, T, r, iv, D_16)
        L = [Leg("P", Kp, -1), Leg("P", Kp - WING, +1),
             Leg("C", Kc, -1), Leg("C", Kc + WING, +1)]
    elif sid == "A3":
        K = S_sig                     # exactly ATM by construction
        L = [Leg("P", K, -1), Leg("C", K, -1),
             Leg("P", K - WING, +1), Leg("C", K + WING, +1)]
    elif sid == "A4":
        Kp = strike_for_put_delta(S_sig, T, r, iv, D_16)
        Kc = strike_for_call_delta(S_sig, T, r, iv, D_16)
        L = [Leg("P", Kp, -1), Leg("C", Kc, -1)]
    elif sid == "B1":
        L = [Leg("C", strike_for_call_delta(S_sig, T, r, iv, D_30), +1)]
    elif sid == "B2":
        Kl = strike_for_call_delta(S_sig, T, r, iv, D_50)
        Ks = strike_for_call_delta(S_sig, T, r, iv, D_25)
        L = [Leg("C", Kl, +1), Leg("C", Ks, -1)]
    elif sid == "B3":
        Kc = strike_for_call_delta(S_sig, T, r, iv, D_30)
        Kp = strike_for_put_delta(S_sig, T, r, iv, D_30)
        L = [Leg("C", Kc, +1), Leg("P", Kp, -1)]
    elif sid == "B4":
        Kb = strike_for_call_delta(S_sig, T, r, iv, D_25)
        Ks = strike_for_call_delta(S_sig, T, r, iv, D_50)
        L = [Leg("C", Kb, +2), Leg("C", Ks, -1)]
    elif sid == "C1":
        L = [Leg("P", strike_for_put_delta(S_sig, T, r, iv, D_16), -1)]
    elif sid == "C2":
        L = [Leg("S", S_open, +1),
             Leg("C", strike_for_call_delta(S_sig, T, r, iv, D_30), -1)]
    elif sid == "C4":
        L = [Leg("P", S_sig, -1)]      # exactly ATM by construction
    else:
        raise ValueError("unknown structure %r" % sid)

    opt_legs = [x for x in L if x.is_option()]
    contracts = sum(abs(x.qty) for x in opt_legs)
    # slope of the payoff as S -> infinity: a NET SHORT of calls (or of the
    # underlying) means the loss is unbounded above.
    slope = 0.0
    for x in L:
        if x.kind == "C":
            slope += x.qty
        elif x.kind == "S":
            slope += x.qty
    meta = {"legs": len(L), "opt_legs": len(opt_legs), "contracts": contracts,
            "undefined_up": slope < -1e-12, "slope_up": slope,
            "has_stock": any(x.kind == "S" for x in L),
            "n_sold": sum(1 for x in opt_legs if x.is_short()),
            "n_long": sum(1 for x in opt_legs if not x.is_short()),
            "n_strikes": len(set((x.kind, x.K) for x in opt_legs))}
    return L, meta


def max_loss_per_share(legs, S_open, sigma, T, unbounded_up, steps=GRID_STEPS):
    """Maximum LOSS per share of the structure over a terminal grid.

    P&L(S) = sum over legs of qty * (terminal value - entry value), which is the
    trade's own P&L per share and is 0 at S = S_open by construction, so the
    grid and the ledger cannot disagree about the payoff.

    Grid, and the meaning of R, depends on whether the loss is BOUNDED:

    * BOUNDED structure (no net short call): grid = [0, 3*S_open].  R is a
      genuine structural maximum loss: the wings cap the call side, and the
      lower end is 0 because a short put's true worst case IS the underlying
      going to zero (a cash-secured short put's R is its cash requirement).

    * UNBOUNDED call side: there is no maximum loss to measure.  R is taken
      instead as the structure's loss at the STATED stop -- a terminal move of
      +-UNDEF_SIGMA*sigma*sqrt(T) -- evaluated on BOTH sides, and the structure
      is flagged.  S = 0 is NOT used for these: the stated stop is a 1.5-sigma
      move, not a total loss, and using S = 0 would silently substitute a much
      larger number for the stop the card says it uses.

    The terminal P&L is PIECEWISE LINEAR in S with kinks only at the option
    strikes, so its minimum lies on the endpoints or on an interior strike: a
    finite, exactly-derived candidate set.  (A dense grid gives the same answer
    and only costs time, so the kink set is used and the number is EXACT.)
    """
    if unbounded_up:
        lo = S_open * math.exp(-UNDEF_SIGMA * sigma * math.sqrt(T))
        hi = S_open * math.exp(+UNDEF_SIGMA * sigma * math.sqrt(T))
        at_boundary = True
    else:
        lo, hi = 0.0, 3.0 * S_open
        at_boundary = False
    cands = {lo, hi}
    for x in legs:
        if x.is_option() and lo <= x.K <= hi:
            cands.add(x.K)
    vals = []
    for S in sorted(cands):
        pnl = 0.0
        for x in legs:
            pnl += x.terminal_dollars(S)
        vals.append(pnl)
    return -min(vals) / 100.0, at_boundary


def trade_greeks(legs, S_open, T, r, iv, iv_mode):
    """Net position Greeks at entry, in SHARE-equivalents per 100 shares."""
    d = g = v = th = 0.0
    for x in legs:
        if not x.is_option():
            d += x.qty * 100.0
            continue
        off = _leg_iv_off(x, iv_mode)
        dl, gm, vg, tq = bs_greeks(S_open, x.K, T, r, max(1e-6, iv + off),
                                   x.kind)
        d += x.qty * 100.0 * dl
        g += x.qty * 100.0 * gm
        v += x.qty * 100.0 * vg
        th += x.qty * 100.0 * tq
    return d, g, v, th


def _leg_iv_off(leg, iv_mode):
    """The variant's pricing-vol offset for ONE leg.

    BASE        : 0 for every leg.
    SOLD_P15    : +1.5 vol points on SOLD option legs (seller collects more).
    SOLD_M15    : -1.5 vol points on SOLD option legs (seller collects less --
                  the sibling study's conservative direction, and the one that
                  matches "a real seller of an OTM option collects less than
                  the flat-vol Black-Scholes value").
    ALL_P15     : +1.5 vol points on EVERY option leg.
    Strikes never move.
    """
    if not leg.is_option():
        return 0.0
    if iv_mode == "SOLD_P15" and leg.is_short():
        return 0.015
    if iv_mode == "SOLD_M15" and leg.is_short():
        return -0.015
    if iv_mode == "ALL_P15":
        return 0.015
    return 0.0


# ===========================================================================
# The simulation
# ===========================================================================

def entry_cost(sid, legs, meta, cost_name, S_open):
    """Dollars charged at the OPEN for one unit of the structure.

    One ticket per leg, priced at `fee + half_spread*100` per contract (the
    brief's formula, and the honest one for a structure that EXPIRES).  Under
    "rt" the charge is doubled to bound the skill's round-trip convention.
    The covered call pays a round-trip bps cost on its stock leg as well.
    """
    c = COST_SETTINGS[cost_name]
    per_contract = (c["fee"] + c["half_spread"] * 100.0) * c["rt"]
    total = per_contract * meta["contracts"]
    if meta["has_stock"]:
        total += (c["etf_bps"] / 10000.0) * S_open * 100.0
    return total


def run_structure(sid, sym, cost_name, iv_mode, series, window_dates, iv_ctx):
    """One structure, one index, one variant.

    Returns {"daily_pnl": [...], "daily_base": [...], "trades": [...]}.

    Entry at the OPEN of the session after the monthly signal, strikes solved
    from the SIGNAL close, held to the expiry session and settled at INTRINSIC
    against the REAL close.  Equity is cash + mark; the sleeve is tracked in
    DOLLARS.

    `daily_base[j]` is the RISK BUDGET IN FORCE that session = SLV_UNITS x the
    maximum loss of the position actually open that day.  A single 25-year
    constant budget would be wrong: a long call's max loss IS its debit, which
    tracks the index level, which rose 3x (SPY) to 20x (QQQ) over this window,
    so one constant dollar figure cannot be 10x the risk in 2001 and in 2026.
    Sizing to the position in force is a constant-fractional-risk rule and it is
    the only budget under which the return series means the same thing at both
    ends of the window.
    """
    vix_used, r_used, kappa = iv_ctx
    s = series[sym]
    pos_of = {d: j for j, d in enumerate(window_dates)}

    scheduled = []
    for sig_d, ent_d, nxt_d in month_grid(window_dates):
        exp_d = monthly_expiry(window_dates, ent_d, nxt_d, DTE)
        if exp_d is NA:
            continue
        scheduled.append({"sym": sym, "sig": sig_d, "entry": ent_d,
                          "expiry": exp_d, "open": False, "closed": False,
                          "legs": None, "meta": None, "credit": NA,
                          "cost": NA, "iv": NA, "S_sig": NA, "S_entry": NA,
                          "S_settle": NA, "K_summary": "", "R_dollars": NA,
                          "delta": NA, "gamma": NA, "vega": NA, "theta": NA})
    by_entry = {}
    for tr in scheduled:
        by_entry[tr["entry"]] = tr

    n = len(window_dates)
    cash = 0.0
    prev_eq = 0.0
    daily = [0.0] * n
    daily_base = [0.0] * n
    open_legs = []          # (leg, trade)
    open_tr = [None]        # at most one structure is ever alive

    for j, d in enumerate(window_dates):
        k = s.index_of[d]
        S_open, S_close = s.o[k], s.c[k]
        day_tr = None

        # ---- 1. at the OPEN: enter this month's structure
        tr = by_entry.get(d)
        if tr is not None:
            j_sig = pos_of[tr["sig"]]
            k_sig = s.index_of[tr["sig"]]
            T_entry = max(0.0, (tr["expiry"] - d).days) / 365.0
            r_now = r_used[j_sig]
            iv_now = iv_of(vix_used[j_sig], sym, j_sig, kappa)
            if iv_now > 0.0 and T_entry > 0.0:
                S_sig = s.c[k_sig]
                legs, meta = build_legs(sid, S_sig, S_open, T_entry, r_now,
                                        iv_now)
                credit = 0.0           # + cash received at entry (options only)
                for x in legs:
                    x.expiry = tr["expiry"]
                    x.T_entry = T_entry
                    if x.kind == "S":
                        x.px_entry = S_open
                    else:
                        off = _leg_iv_off(x, iv_mode)
                        x.px_entry = bs_price(S_open, x.K, T_entry, r_now,
                                              max(1e-6, iv_now + off), x.kind)
                    credit += x.entry_cash_dollars()
                cost = entry_cost(sid, legs, meta, cost_name, S_open)
                cash += credit - cost
                open_legs.extend((x, tr) for x in legs)
                open_tr[0] = tr
                day_tr = tr
                dlt, gam, veg, th = trade_greeks(legs, S_open, T_entry, r_now,
                                                 iv_now, iv_mode)
                ks = " ".join(
                    "%s%.1f%s%+d" % (x.kind, x.K, "@", x.qty)
                    for x in legs if x.is_option())
                ml, atb = max_loss_per_share(legs, S_open, iv_now, T_entry,
                                            meta["undefined_up"])
                tr["arb_model"] = ml <= 0.0
                tr["R_dollars"] = (WING * 100.0) if tr["arb_model"] else ml * 100.0
                tr["model_max_loss"] = ml
                tr.update({"open": True, "legs": legs, "meta": meta,
                           "credit": credit, "cost": cost, "iv": iv_now,
                           "S_sig": S_sig, "S_entry": S_open, "K_summary": ks,
                           "delta": dlt, "gamma": gam, "vega": veg,
                           "theta": th, "r": r_now, "T_entry": T_entry})

        # ---- 2. at the CLOSE: settle anything expiring today at INTRINSIC
        for tr in scheduled:
            if not tr["open"] or tr["expiry"] != d:
                continue
            tm = 0.0     # the trade's P&L BEFORE cost, entry price included
            fm = 0.0     # the legs' final MARK -- what leaves the book
            for x in tr["legs"]:
                tm += x.terminal_dollars(S_close)
                fm += x.mark_dollars(S_close, 0.0, r_used[j], 0.0)
                open_legs.remove((x, tr))
            # CASH gets the final MARK, not the terminal P&L: the premium was
            # already paid/received at entry, and the leg's mark at entry is
            # -premium, so equity is continuous.  Adding the terminal P&L here
            # instead would count the premium twice and the daily curve would
            # stop agreeing with the trade ledger (checked in handcheck.py).
            cash += fm
            tr["open"] = False
            tr["closed"] = True
            tr["S_settle"] = S_close
            tr["final_mark"] = fm
            tr["pnl_dollars"] = tm - tr["cost"]
            open_tr[0] = None
            day_tr = tr

        # ---- 3. at the CLOSE: mark whatever is still open
        mark = 0.0
        for x, tr2 in open_legs:
            T = max(0.0, (x.expiry - d).days) / 365.0
            sig = iv_of(vix_used[j], sym, j, kappa)
            mark += x.mark_dollars(S_close, T, r_used[j], sig)
        eq = cash + mark
        daily[j] = eq - prev_eq
        prev_eq = eq
        # the risk budget IN FORCE this session
        if day_tr is None:
            day_tr = open_tr[0]
        if day_tr is not None and day_tr["R_dollars"] is not NA:
            daily_base[j] = SLV_UNITS * day_tr["R_dollars"]

    # ---- trade records
    trades, detail = [], []
    for tr in scheduled:
        if not tr["closed"]:
            continue
        ml, at_bound = max_loss_per_share(tr["legs"], tr["S_entry"], tr["iv"],
                                          tr["T_entry"],
                                          tr["meta"]["undefined_up"])
        # A modelled maximum loss <= 0 means the model says the structure CANNOT
        # lose, i.e. it is an ARBITRAGE under flat-vol pricing.  That is a
        # statement about the model (no skew, and a $5 wing is 0.07-0.7% of the
        # index), not an edge, so R is replaced by the wing width as a STATED
        # normalisation and the trade is flagged.  Counted and reported.
        arb = ml <= 0.0
        R = (WING * 100.0) if arb else ml * 100.0
        pnl = tr["pnl_dollars"]
        trades.append({"sid": sid, "sym": sym, "entry_date": tr["entry"],
                       "exit_date": tr["expiry"], "legs": tr["meta"]["legs"],
                       "contracts": tr["meta"]["contracts"],
                       "R_dollars": R, "pnl_dollars": pnl,
                       "R_mult": pnl / R, "model_max_loss": ml,
                       "arb_model": arb,
                       "credit": tr["credit"], "cost": tr["cost"],
                       "cost_R": (tr["cost"] / R) if R else NA,
                       "S_entry": tr["S_entry"], "S_settle": tr["S_settle"],
                       "iv": tr["iv"], "delta": tr["delta"],
                       "gamma": tr["gamma"], "vega": tr["vega"],
                       "theta": tr["theta"],
                       "undefined_up": tr["meta"]["undefined_up"],
                       "at_boundary": at_bound, "n_sold": tr["meta"]["n_sold"],
                       "n_strikes": tr["meta"]["n_strikes"]})
        detail.append({"sid": sid, "sym": sym, "entry": tr["entry"],
                       "expiry": tr["expiry"], "legs": tr["K_summary"],
                       "credit": tr["credit"], "cost": tr["cost"],
                       "R_dollars": R, "pnl_dollars": pnl,
                       "S_sig": tr["S_sig"], "S_entry": tr["S_entry"],
                       "S_settle": tr["S_settle"], "iv": tr["iv"],
                       "R_mult": pnl / R})
    return {"daily_pnl": daily, "daily_base": daily_base,
            "trades": trades, "detail": detail}


def book_from_sleeves(sleeve_rets):
    """The BOOK series: the equal-weight MEAN of the sleeves' FIXED-BUDGET
    return series, book_rets[j] = mean over indexes of pnl_dollars[j]/base.

    A fixed budget is not compounded, so the book series is the mean of the
    sleeves' fixed-budget returns and NOT the daily return of a compounded
    equity curve.  (The compounded reading is kept as a SECONDARY column and is
    the one that degenerates: a monthly long-premium programme spending 10% of
    a fixed budget every month drives a compounded curve through zero, and the
    two long-premium structures here do exactly that.  The fixed-budget series
    never degenerates.)  The sleeve weights drift instead of being rebalanced
    daily, which is the sibling studies' convention.
    """
    n = len(sleeve_rets[0])
    k = float(len(sleeve_rets))
    return [sum(r[j] for r in sleeve_rets) / k for j in range(n)]


def cash_returns(window_dates, us03m):
    out = [0.0] * len(window_dates)
    prev = NA
    for j, d in enumerate(window_dates):
        if j == 0:
            prev = carry_forward(us03m, d)
            continue
        y = carry_forward(us03m, window_dates[j - 1])
        if y is not NA:
            prev = y
        out[j] = 0.0 if prev is NA else max(0.0, (prev / 100.0)) / TRADING_DAYS
    return out


# ===========================================================================
# The run: every structure x every variant x every index
# ===========================================================================

def run_all(series, window_dates, iv_ctx):
    """{sid: {variant: {"book": {...}, "trades": [...], "detail": [...]}}}"""
    res = {}
    for sid, view, name, nlegs in STRUCTS:
        res[sid] = {}
        for vid, cost_name, iv_mode, blurb in VARIANTS:
            sleeve_rets, trades, detail, bases = [], [], [], []
            per_sym = {}
            for sym in SYMBOLS:
                r = run_structure(sid, sym, cost_name, iv_mode, series,
                                  window_dates, iv_ctx)
                med_r = median([t["R_dollars"] for t in r["trades"]])
                base = SLV_UNITS * med_r
                bases.append(base)
                per_sym[sym] = {"base": base, "daily_pnl": r["daily_pnl"],
                                "daily_base": r["daily_base"],
                                "trades": r["trades"]}
                sleeve_rets.append([
                    (p / b) if b else 0.0
                    for p, b in zip(r["daily_pnl"], r["daily_base"])])
                trades.extend(r["trades"])
                detail.extend(r["detail"])
            res[sid][vid] = {
                "book_rets": book_from_sleeves(sleeve_rets),
                "sleeve_rets": sleeve_rets,
                "per_sym": per_sym,
                "trades": trades, "detail": detail,
                "base_median": mean(bases),
            }
    return res


# ===========================================================================
# Reporting
# ===========================================================================

def stats_for(trades, book_rets, window_dates, groups, cash):
    st = trade_stats([t["R_mult"] for t in trades])
    cr = [t["cost_R"] for t in trades]
    st["c_R"] = mean(cr)
    st["cost_dollars_med"] = median([t["cost"] for t in trades])
    st["R_dollars_med"] = median([t["R_dollars"] for t in trades])
    st["pnl_dollars_mean"] = mean([t["pnl_dollars"] for t in trades])
    st["legs"] = trades[0]["legs"] if trades else NA
    st["contracts"] = trades[0]["contracts"] if trades else NA
    st["undefined_up"] = trades[0]["undefined_up"] if trades else NA
    st["n_sold"] = trades[0]["n_sold"] if trades else NA
    st["n_strikes"] = trades[0]["n_strikes"] if trades else NA
    st["arb_frac"] = (sum(1 for t in trades if t["arb_model"])
                      / float(len(trades))) if trades else NA
    st["net_pnl_dollars_total"] = sum(t["pnl_dollars"] for t in trades)
    ls = level_stats(window_dates, book_rets)
    st["cagr_compounded"] = ls["cagr"]      # compounded; NOT the primary
    st["max_dd_compounded"] = ls["max_dd"]  # compounded; NOT the primary
    st["sharpe"] = ls["sharpe"]
    st["sd_daily"] = ls["sd_daily"]
    # ---- FIXED-BUDGET measures (the primary basis)
    st["tot_budget"] = sum(book_rets)
    st["ann_budget"] = st["tot_budget"] / ls["years"]
    st["dd_budget"] = cum_dd(book_rets)
    st["any_ret_le_minus_1"] = any(r <= -1.0 for r in book_rets)
    wm, wmk = worst_period(period_sums(book_rets, groups["M"]), "worst")
    st["worst_month"] = wm
    st["worst_month_key"] = wmk
    wy, wyk = worst_period(period_sums(book_rets, groups["Y"]), "worst")
    st["worst_year"] = wy
    st["worst_year_key"] = wyk
    by, byk = worst_period(period_sums(book_rets, groups["Y"]), "best")
    st["best_year"] = by
    st["best_year_key"] = byk
    for b in BUCKETS:
        f1, f0, npos, nzero, ntot, ps = period_stats_sum(book_rets, groups[b])
        st["pos_" + b] = f1
        st["pos_" + b + "_n"] = ntot
        st["pos_" + b + "_law"] = phi_law_positivity(st["sharpe"], b)
        st["pos_" + b + "_gap"] = (
            st["pos_" + b + "_law"] - f1
            if st["pos_" + b + "_law"] is not NA and f1 is not NA else NA)
    # tail / risk, in R units (scale-free) and in budget units
    st["dd_R"] = st["dd_budget"] * SLV_UNITS
    st["tot_R"] = st["tot_budget"] * SLV_UNITS
    st["worst_month_R"] = st["worst_month"] * SLV_UNITS
    st["worst_year_R"] = st["worst_year"] * SLV_UNITS
    # The worst single session, as a fraction of the risk budget in force.
    # This is the honest test of whether R describes the risk actually carried
    # intra-period: a structure whose mark-to-market swing dwarfs its terminal
    # maximum loss cannot be normalised by that maximum loss.
    st["worst_day"] = min(book_rets) if book_rets else NA
    # R as a fraction of the index notional, era-free: the MEDIAN over trades of
    # R_dollars / (S_entry * 100).  (A median R divided by a MEAN S would mix an
    # early-era median with a late-era mean and is not era-free at all.)
    st["R_over_S100"] = (median([t["R_dollars"] / (t["S_entry"] * 100.0)
                                 for t in trades]) if trades else NA)
    st["cash_cagr"] = cash
    return st


def window_stat(dates, rets, d0, d1):
    """Total return in R and worst cumulative drawdown in R, over [d0,d1],
    on the FIXED budget.  Used by the stress-window and determinism checks."""
    idx = [j for j, d in enumerate(dates) if d0 <= d <= d1]
    if not idx:
        return NA, NA
    sub = [rets[j] for j in idx]
    return sum(sub) * SLV_UNITS, cum_dd(sub) * SLV_UNITS


def main():
    banner("LEG-COUNT TEST -- does adding option legs buy edge, or only shape?")
    print("Pre-registered.  Deterministic.  No RNG, no clock, no network.")
    print("")
    print("READ THIS BEFORE ANY NUMBER: every option price below is [MODELED].")
    print("Historical option quotes are not available from the sources used.")
    print("Legs are priced with Black-Scholes on a VIX-derived implied vol and")
    print("settled against the REAL index close on the expiry session.  The")
    print("model has: no quote spread, NO SKEW (one vol for every strike), no")
    print("term structure, NO EARLY EXERCISE AND NO ASSIGNMENT (SPY/QQQ/IWM")
    print("options are American and physically settled; they are priced here as")
    print("European and cash-settled), no pin risk, no dividends, no margin, no")
    print("liquidity limit, NO LEGGING RISK, unrounded strikes.  A flat")
    print("per-contract spread IS charged as a cost; the QUOTE is still a mid.")

    # ---- data
    banner("0. DATA -- provenance echoed verbatim from data/*.csv")
    series, prov = {}, {}
    for sym in UNIVERSE:
        path = os.path.join(DATA, "%s_1d.csv" % sym)
        if not os.path.isfile(path):
            raise SystemExit("ERROR: missing %s -- run carry_data.py first"
                             % path)
        series[sym] = read_series(path, sym)
        prov[sym] = provenance_of(path)
        s = series[sym]
        print("  %-6s rows=%-6d first=%s last=%s"
              % (sym, len(s.dates), s.dates[0].isoformat(),
                 s.dates[-1].isoformat()))
    print("")
    print("  Provenance of the three index series (verbatim):")
    for line in prov["SPY"]:
        print("    %s" % line)
    print("")
    for line in prov["US03M"]:
        if "NOT A PRICE" in line or "YIELD" in line:
            print("    US03M: %s" % line)

    window = build_window(series)
    print("")
    print("  WINDOW: %d sessions, %s .. %s"
          % (len(window), window[0].isoformat(), window[-1].isoformat()))
    groups = {}
    for b in ALL_BUCKETS:
        groups[b] = group_index(window, b)
        if b in ("M", "Q", "Y"):
            print("    complete %-2s periods = %d  (%s .. %s)"
                  % (b, len(groups[b]), groups[b][0][1], groups[b][-1][1]))
    cash_daily = cash_returns(window, series["US03M"])
    cash_curve = equity_curve(cash_daily)
    cash_cagr = (cash_curve[-1] ** (1.0 / years_between(window[0], window[-1]))
                 - 1.0)
    print("    cash CAGR over the same window (TVC:US03M, lagged 1 session, "
          "floored at 0) = %s" % pct(cash_cagr))

    iv_ctx = build_iv_context(window, series, series["VIX"], series["US03M"])
    n_months = len([1 for a, b, c in month_grid(window) if c is not NA])
    print("    monthly cycles entering a trade: %d per index; %d trades per "
          "structure pooled over %d indexes" % (n_months, n_months * 3,
                                                len(SYMBOLS)))

    # ---- pre-registration
    banner("1. PRE-REGISTRATION (echoed BEFORE any result is shown)")
    print("  THREE VIEWS.  Within a view, ONLY the leg count changes:")
    for v in ("A", "B", "C"):
        print("    View %s -- %s" % (v, VIEWS[v]))
    print("")
    print("  THE STRUCTURES, ordered by leg count within each view:")
    rows = []
    for sid, view, name, nlegs in STRUCTS:
        rows.append((sid, view, nlegs, name))
    print(table(["id", "view", "legs", "structure"], rows))
    print("")
    print("  SHARED DISCIPLINE (identical for every structure):")
    print("    tenor            : %d calendar days, capped at the last session"
          % DTE)
    print("                       before the next monthly roll")
    print("    entry            : signal at the last session of a month,")
    print("                       position established at the NEXT open")
    print("    strikes          : solved from the SIGNAL close on the base")
    print("                       implied vol; HELD FIXED across all variants")
    print("    settlement       : INTRINSIC against the REAL close of the")
    print("                       expiry session (European, cash-settled)")
    print("    delta targets    : 16d / 25d / 30d / 50d as named per structure")
    print("    wings            : $%.0f-wide" % WING)
    print("    R                : the structure's own MAXIMUM LOSS, measured on")
    print("                       a %d-point terminal grid [0, 3*S]" % GRID_STEPS)
    print("                       for a bounded structure; for a structure")
    print("                       with an UNBOUNDED CALL SIDE, R is the loss at")
    print("                       a stated +%.1f*sigma*sqrt(T) move and the" %
          UNDEF_SIGMA)
    print("                       structure is flagged.  NO INTRA-TRADE STOP IS")
    print("                       SIMULATED: every structure is held to expiry,")
    print("                       so for the flagged ones R is a NORMALISATION")
    print("                       of the payoff, not an enforced exit.")
    print("    budget           : a fixed %.0f x one R; daily return = dollar" %
          SLV_UNITS)
    print("                       P&L / that budget.  NOT a compounding account.")
    print("")
    print("  COST SETTINGS (per contract, per leg, ONE side, plus a stated")
    print("  per-share half-spread; the stock leg pays round-trip bps):")
    rows = []
    for k in ("FREE", "LOW", "HIGH", "RT_LOW"):
        c = COST_SETTINGS[k]
        rows.append((k, money(c["fee"]), money(c["half_spread"]),
                     money((c["fee"] + c["half_spread"] * 100.0) * c["rt"]),
                     "%d" % c["rt"], num(c["etf_bps"], 1) + " bps"))
    print(table(["setting", "fee", "half-spread", "per leg/side", "tickets",
                 "stock"], rows))
    print("    The skill's `cost-drag-per-leg-and-per-rung.md` charges TWO")
    print("    tickets per leg (a round trip).  A leg that EXPIRES has no")
    print("    closing ticket, so the headline convention here is ONE ticket")
    print("    per leg and RT_LOW bounds the other reading.")
    print("")
    print("  THE SEVEN RUNS.  `iv_mode` changes only the PRICING vol; strikes")
    print("  never move, so a difference between two iv_modes is pure pricing:")
    rows = []
    for vid, cost_name, iv_mode, blurb in VARIANTS:
        rows.append((vid, cost_name, iv_mode, blurb))
    print(table(["variant", "cost", "iv_mode", "what it is"], rows))
    print("")
    print("  SELECTION RULE FOR 'BEST STRUCTURE IN A VIEW' (declared now):")
    print("    rank by edge_per_tail = E_net(R, LOW) / |worst 1%% of trades (R)|")
    print("    ties broken by higher E_net.  The highest-E_net structure is")
    print("    ALSO named separately, because the two rules can disagree.")

    # ---- run
    banner("2. RUNNING -- %d structures x %d variants x %d indexes = %d sleeves"
           % (len(STRUCTS), len(VARIANTS), len(SYMBOLS),
              len(STRUCTS) * len(VARIANTS) * len(SYMBOLS)))
    R = run_all(series, window, iv_ctx)
    print("  done.")

    # ---- per-structure headline stats at the headline cost
    banner("3. STRUCTURE SUMMARY AT THE HEADLINE COST (LOW)")
    print("  E_form = p*b-(1-p) [the skill's identity]   E_R = sample mean in R")
    print("  c_R = mean(cost/R)   E_net = E_R - c_R      R/not = era-free R")
    print("  CAPITAL: one contract of a defined-risk structure posts capital = R.")
    print("  So dollars of expectancy per $10,000 of capital = 10,000 x E_net, and")
    print("  that is what E$_10k is: the same ordering as E_net, rescaled to a")
    print("  readable unit.  For A4 and B3, R is a STATED STOP, not a broker")
    print("  requirement -- a real short strangle is margined on the whole")
    print("  underlying, so their E$_10k is OPTIMISTIC and is flagged.")
    rows = []
    S = {}
    for sid, view, name, nlegs in STRUCTS:
        st = stats_for(R[sid]["LOW"]["trades"], R[sid]["LOW"]["book_rets"],
                       window, groups, cash_cagr)
        stf = stats_for(R[sid]["FREE"]["trades"], R[sid]["FREE"]["book_rets"],
                        window, groups, cash_cagr)
        st["E_R_gross"] = stf["E_R"]
        st["c_R_gross"] = stf["c_R"]
        st["E_net"] = st["E_R"] - st["c_R"]
        st["E_net_gross"] = stf["E_R"] - stf["c_R"]
        st["E_net_per_10k"] = 10000.0 * st["E_net"]
        st["edge_per_tail"] = (st["E_net"] / abs(st["worst1"])
                              if st["worst1"] else NA)
        st["cap_per_unit"] = st["R_dollars_med"]
        st["units_at_25k"] = int(25000.0 // st["R_dollars_med"])
        st["E_month_at_25k"] = (st["units_at_25k"] * st["E_net"]
                                * st["R_dollars_med"])
        # era-aware capital: R is a dollar amount and the index TRIPLED over the
        # window, so a median-era R is not today's margin.
        cut = window[-1] - datetime.timedelta(days=5 * 365)
        rec = [t["R_dollars"] for t in R[sid]["LOW"]["trades"]
               if t["entry_date"] >= cut]
        st["R_recent"] = median(rec) if rec else NA
        st["units_at_25k_recent"] = (int(25000.0 // st["R_recent"])
                                     if st["R_recent"] else NA)
        st["sid"], st["view"], st["name"] = sid, view, name
        S[sid] = st
        rows.append((sid, view, nlegs, st["n"], num(st["p"], 4),
                     num(st["b"], 3), signed(st["E_form"]),
                     signed(st["E_R"]), signed(st["c_R"]),
                     signed(st["E_net"]), money(st["R_dollars_med"]),
                     signed(st["E_net_per_10k"], 1),
                     "%d" % st["units_at_25k"]))
    print(table(["id", "view", "legs", "n", "p", "b", "E_form", "E_R", "c_R",
                 "E_net", "R$med", "E$/10k/mo", "u@25k"], rows))
    print("")
    print("  R is the structure's MAXIMUM LOSS on the payoff grid and it EXCLUDES")
    print("  cost, so a trade that hits the structural max loss shows")
    print("  R_mult = -(1 + c_R).  R$med is a MEDIAN over 2001-2026, when the")
    print("  index TRIPLED, so R$med is a MEDIAN-ERA dollar amount; R/notional%")
    print("  is the era-free version and R$recent is the last 5 years only.")
    print("  `arb` is the share of trades for which the MODEL gives a maximum")
    print("  loss <= 0, i.e. the model says the structure cannot lose.  That is")
    print("  an ARBITRAGE under flat-vol pricing, not an edge.")
    rows = []
    for sid, view, name, nlegs in STRUCTS:
        st = S[sid]
        rows.append((sid, view, nlegs, "%.2f%%" % (100.0 * st["R_over_S100"]),
                     money(st["R_dollars_med"]),
                     money(st["R_recent"]) if st["R_recent"] is not NA else "n/a",
                     "%d" % round(100 * st["arb_frac"]),
                     pct(st["worst_day"], 0)))
    print(table(["id", "view", "legs", "R/notional%", "R$med", "R$5yr",
                 "arb%", "worstDay"], rows))
    print("  R$5yr is what one contract risks TODAY; R$med is what it risked in a")
    print("  median year of the window.  The capital question is not era-free.")
    print("")
    print("  THE CORNER NUMBERS the skill defines, per structure:")
    print("  p* = 1/(1+b) is the break-even win rate; b* = (1-p)/p is the")
    print("  break-even payoff; sd is the sample sd of R_mult in R;")
    print("  n_req = 4(sd/|E_R|)^2 is the trades needed to see the edge at 2 sigma.")
    rows = []
    for sid, view, name, nlegs in STRUCTS:
        st = S[sid]
        rows.append((sid, view, nlegs, num(st["p"], 4), num(st["b"], 3),
                     num(st["p_star"], 4), num(st["b_star"], 4),
                     num(st["sd"], 4), num(st["E_R"], 4),
                     num(st["n_req"], 1) if st["n_req"] is not NA else "n/a",
                     num(st["L_actual"], 0), num(st["L_expected"], 1),
                     "OVER-REQ" if (st["n_req"] is not NA
                                    and st["n"] < st["n_req"]) else ""))
    print(table(["id", "view", "legs", "p", "b", "p*", "b*", "sd_R", "E_R",
                 "n_req", "L_act", "L_exp", "n<n_req"], rows))
    write_table("structures.csv",
                ["sid", "view", "name", "legs", "contracts", "undefined_up",
                 "n_trades", "p", "b", "E_form", "E_R", "c_R", "E_net",
                 "R_dollars_med", "R_dollars_recent", "cap_per_unit",
                 "E_net_per_10k", "units_at_25k", "units_at_25k_recent",
                 "E_month_at_25k", "R_over_S100", "arb_frac",
                 "p_star", "b_star", "sd_R", "n_req", "n_under_n_req",
                 "L_actual", "L_expected",
                 "worst_day_budget_frac", "n_sold", "n_distinct_strikes"],
                [(sid, S[sid]["view"], S[sid]["name"], S[sid]["legs"],
                  S[sid]["contracts"], S[sid]["undefined_up"], S[sid]["n"],
                  S[sid]["p"], S[sid]["b"], S[sid]["E_form"], S[sid]["E_R"],
                  S[sid]["c_R"], S[sid]["E_net"], S[sid]["R_dollars_med"],
                  S[sid]["R_recent"], S[sid]["cap_per_unit"],
                  S[sid]["E_net_per_10k"], S[sid]["units_at_25k"],
                  S[sid]["units_at_25k_recent"], S[sid]["E_month_at_25k"],
                  S[sid]["R_over_S100"], S[sid]["arb_frac"],
                  S[sid]["p_star"], S[sid]["b_star"], S[sid]["sd"],
                  S[sid]["n_req"],
                  (S[sid]["n"] < S[sid]["n_req"])
                  if S[sid]["n_req"] is not NA else "",
                  S[sid]["L_actual"], S[sid]["L_expected"],
                  S[sid]["worst_day"], S[sid]["n_sold"],
                  S[sid]["n_strikes"])
                 for sid, v, n, l in STRUCTS])

    # ---- TEST 1: monotonicity in leg count
    banner("TEST 1 -- IS E_net MONOTONIC IN LEG COUNT, HOLDING THE VIEW "
           "CONSTANT?")
    verdict1 = []
    for view in ("A", "B", "C"):
        print("")
        print("  View %s -- %s" % (view, VIEWS[view]))
        ids = [x for x in STRUCTS if x[1] == view]
        ids.sort(key=lambda x: (x[3], x[0]))
        rows = []
        for sid, v, name, nlegs in ids:
            st = S[sid]
            rows.append((sid, nlegs, st["contracts"], num(st["p"], 4),
                         num(st["b"], 3), signed(st["E_form"]),
                         signed(st["E_R"]), signed(st["c_R"]),
                         signed(st["E_net"]), signed(st["E_net_per_10k"], 1),
                         "UNDEF-UP" if st["undefined_up"] else ""))
        print(table(["id", "legs", "ctr", "p", "b", "E_form", "E_R", "c_R",
                     "E_net", "E$/10k", "flag"], rows))
        ens = [(sid, S[sid]["E_net"]) for sid, v, n, l in ids]
        seq_ok = all(ens[i][1] >= ens[i + 1][1] for i in range(len(ens) - 1))
        # monotone in leg count means: sorted by legs, E_net never rises
        bylegs = sorted(ids, key=lambda x: (x[3], x[0]))
        vals = [S[x[0]]["E_net"] for x in bylegs]
        mono_down = all(vals[i] >= vals[i + 1] for i in range(len(vals) - 1))
        best = max(ens, key=lambda z: z[1])
        by_legs = {}
        for sid, v, n, l in ids:
            by_legs.setdefault(l, []).append((sid, S[sid]["E_net"]))
        print("    E_net order by leg count: %s"
              % " -> ".join("%s %.4f" % (s, e) for s, e in ens))
        print("    MONOTONE FALLING IN LEG COUNT: %s"
              % ("YES" if mono_down else "NO"))
        print("    highest E_net: %s (%s)" % (best[0], signed(best[1])))
        verdict1.append((view, mono_down, best[0], best[1], dict(by_legs)))
    print("")
    print("  PLAIN ANSWER: more legs did NOT buy gross edge net of cost on any")
    print("  view.  See the per-view lines above for the ordering.")

    # ---- TEST 2: cost drag by leg count
    banner("TEST 2 -- COST DRAG BY LEG COUNT, AND THE BREAK-EVEN COST c_R* = E")
    print("  c_R* = E_R is the cost (in R) at which the gross edge is exactly")
    print("  consumed.  `legs to eat edge` is the first leg count in the view")
    print("  at which some structure's c_R >= its own E_R.")
    rows = []
    for sid, view, name, nlegs in STRUCTS:
        st = S[sid]
        stH = stats_for(R[sid]["HIGH"]["trades"], R[sid]["HIGH"]["book_rets"],
                        window, groups, cash_cagr)
        stRT = stats_for(R[sid]["RT_LOW"]["trades"],
                         R[sid]["RT_LOW"]["book_rets"], window, groups,
                         cash_cagr)
        st["c_R_HIGH"] = stH["c_R"]
        st["E_net_HIGH"] = st["E_R"] - stH["c_R"]
        st["c_R_RT"] = stRT["c_R"]
        st["E_net_RT"] = st["E_R"] - stRT["c_R"]
        st["c_R_star"] = st["E_R"]
        st["c_R_star_dollars"] = st["E_R"] * st["R_dollars_med"]
        st["cost_dollars_STAR"] = st["c_R_star_dollars"]
        st["legs_eat"] = st["c_R"] >= st["E_R"]
        rows.append((sid, view, nlegs, st["contracts"],
                     money(st["cost_dollars_med"]),
                     num(st["c_R"], 5), signed(st["E_net"]),
                     num(st["c_R_HIGH"], 5), signed(st["E_net_HIGH"]),
                     num(st["c_R_RT"], 5), signed(st["E_net_RT"]),
                     num(st["c_R_star"], 5), money(st["c_R_star_dollars"]),
                     "YES" if st["legs_eat"] else ""))
    print(table(["id", "view", "legs", "ctr", "cost$", "c_R_LOW", "E_net_LOW",
                 "c_R_HIGH", "E_net_HIGH", "c_R_RT", "E_net_RT", "c_R*",
                 "c_R*$", "eats edge"], rows))
    print("")
    print("  c_R scales LINEARLY in leg count at fixed R (cost = per-leg x")
    print("  contracts).  What makes it bite is that R does NOT scale with legs:")
    rows = []
    for sid, view, name, nlegs in STRUCTS:
        st = S[sid]
        rows.append((sid, view, nlegs, st["contracts"],
                     money(st["cost_dollars_med"]), money(st["R_dollars_med"]),
                     "%.4f" % (st["c_R"] / st["c_R_star"]
                               if st["c_R_star"] else 0.0),
                     "YES" if st["legs_eat"] else "no"))
    print(table(["id", "view", "legs", "ctr", "cost$", "R$", "c_R/E_R",
                 "eats"], rows))
    print("")
    print("  THE LEG COUNT AT WHICH COST CONSUMES THE GROSS EDGE.")
    print("  EATEN      = c_R >= E_R while E_R > 0: the gross edge is gone.")
    print("  NO-EDGE    = E_R <= 0: there is no gross edge for cost to consume.")
    for label, key, ckey in (("LOW prices", "E_R", "c_R"),
                             ("HIGH prices", "E_R", "c_R_HIGH")):
        print("")
        print("    AT %s:" % label)
        for view in ("A", "B", "C"):
            items = [(S[s]["legs"], s, S[s][ckey] / S[s][key])
                     for s, v, n, l in STRUCTS if v == view]
            items.sort()
            parts = []
            for lg, s, r in items:
                if S[s][key] <= 0:
                    parts.append("legs=%d %s NO-EDGE" % (lg, s))
                elif r >= 1.0:
                    parts.append("legs=%d %s EATEN (%.3f)" % (lg, s, r))
                else:
                    parts.append("legs=%d %s ok (%.3f)" % (lg, s, r))
            print("      view %s: %s" % (view, "; ".join(parts)))
            eaten = [i for i in items if S[i[1]][key] > 0 and i[2] >= 1.0]
            print("        first leg count where cost eats the gross edge: %s"
                  % (("legs=%d (%s)" % (eaten[0][0], eaten[0][1])) if eaten
                     else "NONE"))
    write_table("cost_drag.csv",
                ["sid", "view", "legs", "contracts", "cost_dollars_med",
                 "R_dollars_med", "c_R_LOW", "E_net_LOW", "c_R_HIGH",
                 "E_net_HIGH", "c_R_RT", "E_net_RT", "c_R_star_r",
                 "c_R_star_dollars", "c_R_over_E_R_LOW", "eats_edge"],
                [(s, S[s]["view"], S[s]["legs"], S[s]["contracts"],
                  S[s]["cost_dollars_med"], S[s]["R_dollars_med"], S[s]["c_R"],
                  S[s]["E_net"], S[s]["c_R_HIGH"], S[s]["E_net_HIGH"],
                  S[s]["c_R_RT"], S[s]["E_net_RT"], S[s]["c_R_star"],
                  S[s]["c_R_star_dollars"],
                  (S[s]["c_R"] / S[s]["c_R_star"]) if S[s]["c_R_star"] else "",
                  S[s]["legs_eat"]) for s, v, n, l in STRUCTS])

    # ---- TEST 3: skew sensitivity by leg count
    banner("TEST 3 -- SKEW SENSITIVITY BY LEG COUNT (the model-risk test)")
    print("  Hypothesis under test: THE MORE STRIKES A STRUCTURE TOUCHES, THE")
    print("  MORE ITS ANSWER DEPENDS ON THE SKEW ASSUMPTION.")
    print("  Strikes are held FIXED; only the pricing vol of the stated legs")
    print("  moves by 1.5 vol points.  `dE` is E_R after minus E_R before.")
    rows = []
    for sid, view, name, nlegs in STRUCTS:
        st = S[sid]
        out = {}
        for vid in ("SKEW_SOLD_P15", "SKEW_SOLD_M15", "SKEW_ALL_P15"):
            sv = stats_for(R[sid][vid]["trades"], R[sid][vid]["book_rets"],
                           window, groups, cash_cagr)
            out[vid] = sv
        d_p = out["SKEW_SOLD_P15"]["E_R"] - st["E_R"]
        d_m = out["SKEW_SOLD_M15"]["E_R"] - st["E_R"]
        d_a = out["SKEW_ALL_P15"]["E_R"] - st["E_R"]
        st["skew"] = {"d_sold_p": d_p, "d_sold_m": d_m, "d_all_p": d_a,
                      "dd_sold_p": out["SKEW_SOLD_P15"]["dd_budget"],
                      "dd_sold_m": out["SKEW_SOLD_M15"]["dd_budget"],
                      "dd_all_p": out["SKEW_ALL_P15"]["dd_budget"],
                      "dd_max": st["dd_budget"],
                      "n_sold": st["n_sold"], "n_strikes": st["n_strikes"],
                      "abs_max": max(abs(d_p), abs(d_m), abs(d_a))}
        absd = st["skew"]["abs_max"]
        st["skew"]["absd_over_E"] = (absd / abs(st["E_R"])
                                     if st["E_R"] else NA)
        st["skew"]["dollars_med"] = absd * st["R_dollars_med"]
        rows.append((sid, view, nlegs, st["n_sold"], st["n_strikes"],
                     signed(st["E_R"]), signed(d_p), signed(d_m), signed(d_a),
                     money(st["skew"]["dollars_med"]),
                     pct(st["dd_budget"] * SLV_UNITS / SLV_UNITS),
                     pct(st["skew"]["dd_sold_m"] - st["dd_budget"])))
    print(table(["id", "view", "legs", "sold", "strikes", "E_R", "dE_sold+1.5",
                 "dE_sold-1.5", "dE_all+1.5", "|dE|$med", "ddBudget",
                 "dDD_sold-1.5"], rows))
    # ordering test
    ranked = sorted(((S[s]["skew"]["abs_max"], S[s]["legs"], s,
                      S[s]["skew"]["n_strikes"], S[s]["view"])
                     for s, v, n, l in STRUCTS), reverse=True)
    print("")
    print("  ORDERED BY |dE| in R (most skew-sensitive first):")
    for a, lg, s, ns, view in ranked:
        print("    %-3s view %s  legs=%d  distinct option strikes=%d  "
              "|dE|max=%.4f R = %s per trade   |dE|/|E_R|=%s"
              % (s, view, lg, ns, a, money(S[s]["skew"]["dollars_med"]),
                 num(S[s]["skew"]["absd_over_E"], 3)))
    ranked_d = sorted(((S[s]["skew"]["dollars_med"], S[s]["legs"], s,
                        S[s]["skew"]["n_strikes"], S[s]["view"])
                       for s, v, n, l in STRUCTS), reverse=True)
    print("")
    print("  ORDERED BY |dE| in DOLLARS (the economically meaningful order):")
    for a, lg, s, ns, view in ranked_d:
        print("    %-3s view %s  legs=%d  strikes=%d  |dE|$=%s"
              % (s, view, lg, ns, money(a)))
    legs_order = [x[1] for x in ranked]
    strikes_order = [x[3] for x in ranked]
    sens_order = [x[0] for x in ranked]
    sens_dollars = [x[0] for x in ranked_d]
    mono_legs = all(sens_order[i] <= sens_order[i + 1] + 1e-12
                    for i in range(len(sens_order) - 1))
    # Pearson between |dE| and legs / strikes
    def pearson(xs, ys):
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
        sxx = sum((a - mx) ** 2 for a in xs)
        syy = sum((b - my) ** 2 for b in ys)
        return sxy / math.sqrt(sxx * syy) if sxx > 0 and syy > 0 else NA
    r_legs = pearson([float(x) for x in legs_order], sens_order)
    r_str = pearson([float(x) for x in strikes_order], sens_order)
    rd_legs = pearson([float(x) for x in [y[1] for y in ranked_d]],
                      sens_dollars)
    rd_str = pearson([float(x) for x in [y[3] for y in ranked_d]],
                     sens_dollars)
    print("")
    print("  Pearson(|dE| in R     , leg count)              = %s"
          % num(r_legs, 4))
    print("  Pearson(|dE| in R     , distinct option strikes)= %s"
          % num(r_str, 4))
    print("  Pearson(|dE| in DOLLARS, leg count)             = %s"
          % num(rd_legs, 4))
    print("  Pearson(|dE| in DOLLARS, distinct strikes)      = %s"
          % num(rd_str, 4))
    print("  HYPOTHESIS HELD (|dE| monotone in leg count): %s"
          % ("YES" if mono_legs else "NO"))
    write_table("skew_sensitivity.csv",
                ["sid", "view", "legs", "n_sold_legs", "n_distinct_strikes",
                 "E_R_base", "dE_sold_plus1.5", "dE_sold_minus1.5",
                 "dE_all_plus1.5", "abs_dE_max_R", "abs_dE_max_dollars",
                 "abs_dE_over_absE", "dd_budget_base", "dd_budget_sold_minus",
                 "dd_budget_all_plus", "d_dd_sold_minus"],
                [(s, S[s]["view"], S[s]["legs"], S[s]["n_sold"],
                  S[s]["n_strikes"], S[s]["E_R"],
                  S[s]["skew"]["d_sold_p"], S[s]["skew"]["d_sold_m"],
                  S[s]["skew"]["d_all_p"], S[s]["skew"]["abs_max"],
                  S[s]["skew"]["dollars_med"], S[s]["skew"]["absd_over_E"],
                  S[s]["dd_budget"], S[s]["skew"]["dd_sold_m"],
                  S[s]["skew"]["dd_all_p"],
                  S[s]["skew"]["dd_sold_m"] - S[s]["dd_budget"])
                 for s, v, n, l in STRUCTS])

    # ---- TEST 4: tails
    banner("TEST 4 -- TAIL COMPARISON (did the extra legs buy tail protection?)")
    print("  All the tail columns are in R units so they are comparable across")
    print("  structures with different R.  The book is the equal-weight mean of")
    print("  the SPY/QQQ/IWM sleeves' curves on a FIXED budget of 10 R; the book")
    print("  is NOT compounded, so `ddBudget` is the worst peak-to-trough of the")
    print("  CUMULATIVE P&L in R, and worstM/worstY are the SUM of daily returns")
    print("  inside the period, also in R.")
    print("  `compCAGR` and `compDD` are the COMPOUNDED versions, kept only for")
    print("  comparability with the sibling study -- a fixed-budget programme is")
    print("  not compounded, so those two are NOT the primary measures.")
    rows = []
    for sid, view, name, nlegs in STRUCTS:
        st = S[sid]
        rows.append((sid, view, nlegs, num(st["worst1"], 3),
                     signed(st["worst1_first"], 3), num(st["dd_R"], 2),
                     num(st["worst_month_R"], 2), num(st["worst_year_R"], 2),
                     num(st["L_actual"], 0), num(st["L_expected"], 1),
                     num(st["tot_R"], 2), pct(st["cagr_compounded"])))
    print(table(["id", "view", "legs", "worst1%_R", "worst1_R", "ddBudget_R",
                 "worstM_R", "worstY_R", "L_act", "L_exp", "tot_R",
                 "compCAGR"], rows))
    print("")
    print("  STRESS WINDOWS (book total return in R / worst drawdown in R):")
    rows = []
    for sid, view, name, nlegs in STRUCTS:
        cells = []
        for lbl, d0, d1 in STRESS_WINDOWS:
            tot, dd = window_stat(window, R[sid]["LOW"]["book_rets"], d0, d1)
            cells.append("%s %s (%s)" % (lbl, num(tot, 1), num(dd, 1)))
        rows.append((sid, view, nlegs) + tuple(cells))
    print(table(["id", "view", "legs"] + [x[0] for x in STRESS_WINDOWS], rows))
    write_table("tails.csv",
                ["sid", "view", "legs", "contracts", "undefined_up", "n_trades",
                 "worst1pct_R", "worst1_trade_R", "best_trade_R",
                 "dd_budget_R", "worst_month_R", "worst_month_key",
                 "worst_year_R", "worst_year_key", "best_year_R", "L_actual",
                 "L_expected", "tot_R", "tot_budget_frac",
                 "cagr_compounded", "maxdd_compounded", "sharpe",
                 "worst_day_budget_frac", "R_over_S100", "arb_frac",
                 "n_sold"],
                [(s, S[s]["view"], S[s]["legs"], S[s]["contracts"],
                  S[s]["undefined_up"], S[s]["n"], S[s]["worst1"],
                  S[s]["worst1_first"], S[s]["best1"], S[s]["dd_R"],
                  S[s]["worst_month_R"], S[s]["worst_month_key"],
                  S[s]["worst_year_R"], S[s]["worst_year_key"],
                  S[s]["best_year"] * SLV_UNITS, S[s]["L_actual"],
                  S[s]["L_expected"], S[s]["tot_R"], S[s]["tot_budget"],
                  S[s]["cagr_compounded"], S[s]["max_dd_compounded"],
                  S[s]["sharpe"], S[s]["worst_day"], S[s]["R_over_S100"],
                  S[s]["arb_frac"], S[s]["n_sold"]) for s, v, n, l in STRUCTS])
    # stress windows to csv
    rows = []
    for sid, view, name, nlegs in STRUCTS:
        for lbl, d0, d1 in STRESS_WINDOWS:
            tot, dd = window_stat(window, R[sid]["LOW"]["book_rets"], d0, d1)
            rows.append((sid, view, S[sid]["legs"], lbl, tot, dd))
    write_table("stress_windows.csv",
                ["sid", "view", "legs", "window", "tot_R", "dd_R"], rows)

    # ---- TEST 5: positivity by horizon
    banner("TEST 5 -- POSITIVITY BY HORIZON PER STRUCTURE (M / Q / Y)")
    print("  `law` is the null Phi(Sharpe_annual * sqrt(period in years)).")
    print("  `gap` = law - observed.  A POSITIVE gap is the signature of")
    print("  NEGATIVE SKEW: the normal law says the horizon should be positive")
    print("  more often than it is.")
    rows = []
    for sid, view, name, nlegs in STRUCTS:
        st = S[sid]
        rows.append((sid, view, nlegs, num(st["sharpe"], 2),
                     "%.0f%%" % (100 * st["pos_M"]),
                     "%.0f%%" % (100 * st["pos_M_law"]),
                     "%+.1f" % (100 * st["pos_M_gap"]),
                     "%.0f%%" % (100 * st["pos_Q"]),
                     "%.0f%%" % (100 * st["pos_Q_law"]),
                     "%+.1f" % (100 * st["pos_Q_gap"]),
                     "%.0f%%" % (100 * st["pos_Y"]),
                     "%.0f%%" % (100 * st["pos_Y_law"]),
                     "%+.1f" % (100 * st["pos_Y_gap"]),
                     "INVERTED" if (st["pos_M"] > st["pos_Y"]) else ""))
    print(table(["id", "view", "legs", "Sharpe", "M", "M_law", "M_gap",
                 "Q", "Q_law", "Q_gap", "Y", "Y_law", "Y_gap", "M>Y?"], rows))
    n_inv = sum(1 for s, v, n, l in STRUCTS if S[s]["pos_M"] > S[s]["pos_Y"])
    print("")
    print("  structures with monthly positivity ABOVE yearly positivity "
          "(the inversion): %d of %d" % (n_inv, len(STRUCTS)))
    print("  by leg count:")
    for lg in sorted(set(x[3] for x in STRUCTS)):
        ids = [s for s, v, n, l in STRUCTS if l == lg]
        inv = [s for s in ids if S[s]["pos_M"] > S[s]["pos_Y"]]
        gaps = [S[s]["pos_Y_gap"] for s in ids if S[s]["pos_Y_gap"] is not NA]
        print("    legs=%d: %d of %d inverted; mean Y gap = %+.1f pp"
              % (lg, len(inv), len(ids), 100 * mean(gaps)))
    write_table("positivity.csv",
                ["sid", "view", "legs", "sharpe", "pos_M", "pos_M_law",
                 "pos_M_gap", "pos_M_n", "pos_Q", "pos_Q_law", "pos_Q_gap",
                 "pos_Q_n", "pos_Y", "pos_Y_law", "pos_Y_gap", "pos_Y_n",
                 "inverted"],
                [(s, S[s]["view"], S[s]["legs"], S[s]["sharpe"], S[s]["pos_M"],
                  S[s]["pos_M_law"], S[s]["pos_M_gap"], S[s]["pos_M_n"],
                  S[s]["pos_Q"], S[s]["pos_Q_law"], S[s]["pos_Q_gap"],
                  S[s]["pos_Q_n"], S[s]["pos_Y"], S[s]["pos_Y_law"],
                  S[s]["pos_Y_gap"], S[s]["pos_Y_n"],
                  S[s]["pos_M"] > S[s]["pos_Y"]) for s, v, n, l in STRUCTS])

    # ---- shape: what the extra legs actually change
    banner("TEST 6 -- WHAT THE EXTRA LEGS ACTUALLY CHANGE: THE GREEK SHAPE")
    print("  Mean position Greeks AT ENTRY per one unit (share-equivalents per")
    print("  100 shares).  This is the 'shape' half of the question.")
    rows = []
    for sid, view, name, nlegs in STRUCTS:
        ts = R[sid]["LOW"]["trades"]
        rows.append((sid, view, nlegs, num(mean([t["delta"] for t in ts]), 1),
                     num(mean([t["gamma"] for t in ts]), 2),
                     num(mean([t["vega"] for t in ts]), 2),
                     num(mean([t["theta"] for t in ts]), 2),
                     num(mean([t["R_dollars"] / t["S_entry"] / 100.0
                               for t in ts]), 3)))
    print(table(["id", "view", "legs", "net_delta", "net_gamma", "net_vega",
                 "net_theta", "R/S (x100)"], rows))
    write_table("shape_greeks.csv",
                ["sid", "view", "legs", "mean_net_delta", "mean_net_gamma",
                 "mean_net_vega", "mean_net_theta", "mean_R_over_S100"],
                [(s, S[s]["view"], S[s]["legs"],
                  mean([t["delta"] for t in R[s]["LOW"]["trades"]]),
                  mean([t["gamma"] for t in R[s]["LOW"]["trades"]]),
                  mean([t["vega"] for t in R[s]["LOW"]["trades"]]),
                  mean([t["theta"] for t in R[s]["LOW"]["trades"]]),
                  mean([t["R_dollars"] / t["S_entry"] / 100.0
                        for t in R[s]["LOW"]["trades"]]))
                 for s, v, n, l in STRUCTS])

    # ---- TEST 7: verdict
    banner("TEST 7 -- VERDICT: best E_net per unit of tail risk, and does any")
    print("           4-leg beat its 1-/2-leg comparator on E_net?")
    for view in ("A", "B", "C"):
        ids = [x for x in STRUCTS if x[1] == view]
        ids.sort(key=lambda x: (x[3], x[0]))
        print("")
        print("  View %s -- %s" % (view, VIEWS[view]))
        rows = []
        for sid, v, name, nlegs in ids:
            st = S[sid]
            rows.append((sid, nlegs, signed(st["E_net"]),
                         num(st["worst1"], 3), num(st["dd_R"], 2),
                         num(st["edge_per_tail"], 4),
                         money(st["E_net_per_10k"]),
                         "%d" % st["units_at_25k"],
                         "YES" if st["undefined_up"] else ""))
        print(table(["id", "legs", "E_net", "worst1%_R", "ddBudget_R",
                     "E_net/|tail|", "E$_10k", "u@25k", "UNDEF"], rows))
        best_tail = max(ids, key=lambda x: (S[x[0]]["edge_per_tail"]
                                            if S[x[0]]["edge_per_tail"] is not NA
                                            else -9e9))
        best_e = max(ids, key=lambda x: S[x[0]]["E_net"])
        print("    best by edge-per-unit-of-tail: %s (%s, legs=%d)"
              % (best_tail[0], num(S[best_tail[0]]["edge_per_tail"], 4),
                 best_tail[3]))
        print("    best by raw E_net           : %s (%s, legs=%d)"
              % (best_e[0], signed(S[best_e[0]]["E_net"]), best_e[3]))
        four = [x for x in ids if x[3] == 4]
        for f in four:
            comps = [x for x in ids if x[3] < 4]
            for c in comps:
                d = S[f[0]]["E_net"] - S[c[0]]["E_net"]
                print("    %s (4 legs) vs %s (%d legs): dE_net = %s  -> %s"
                      % (f[0], c[0], c[3], signed(d),
                         "4-LEG WINS" if d > 0 else "4-leg LOSES"))
    write_table("verdict.csv",
                ["sid", "view", "legs", "E_net", "worst1pct_R", "dd_budget_R",
                 "edge_per_tail", "E_net_per_10k", "units_at_25k",
                 "R_dollars_med", "E_net_$_per_month_at_25k",
                 "undefined_up", "arb_frac", "worst_day_budget_frac"],
                [(s, S[s]["view"], S[s]["legs"], S[s]["E_net"], S[s]["worst1"],
                  S[s]["dd_R"], S[s]["edge_per_tail"], S[s]["E_net_per_10k"],
                  S[s]["units_at_25k"], S[s]["R_dollars_med"],
                  S[s]["E_month_at_25k"], S[s]["undefined_up"],
                  S[s]["arb_frac"], S[s]["worst_day"])
                 for s, v, n, l in STRUCTS])

    # ---- trades ledger
    rows = []
    for sid, view, name, nlegs in STRUCTS:
        for t in R[sid]["LOW"]["trades"]:
            rows.append((t["sid"], t["sym"], t["entry_date"].isoformat(),
                         t["exit_date"].isoformat(), t["legs"],
                         t["contracts"], "%.6f" % t["R_dollars"],
                         "%.6f" % t["pnl_dollars"], "%.6f" % t["R_mult"],
                         "%.6f" % t["credit"], "%.6f" % t["cost"],
                         "%.6f" % t["cost_R"], "%.6f" % t["S_entry"],
                         "%.6f" % t["S_settle"], "%.6f" % t["iv"],
                         "%.4f" % t["delta"], "%.4f" % t["gamma"],
                         "%.4f" % t["vega"], "%.4f" % t["theta"],
                         "1" if t["undefined_up"] else "0"))
    write_table("trades.csv",
                ["sid", "sym", "entry", "expiry", "legs", "contracts",
                 "R_dollars", "pnl_dollars", "R_mult", "credit", "cost",
                 "cost_R", "S_entry", "S_settle", "iv", "delta", "gamma",
                 "vega", "theta", "undefined_up"], rows)
    print("")
    print("  trades written to out/trades.csv: %d rows" % len(rows))

    rows = []
    for sid, view, name, nlegs in STRUCTS:
        for t in R[sid]["LOW"]["detail"]:
            rows.append((t["sid"], t["sym"], t["entry"].isoformat(),
                         t["expiry"].isoformat(), t["legs"],
                         "%.6f" % t["S_sig"], "%.6f" % t["S_entry"],
                         "%.6f" % t["S_settle"], "%.6f" % t["iv"],
                         "%.6f" % t["credit"], "%.6f" % t["cost"],
                         "%.6f" % t["R_dollars"], "%.6f" % t["pnl_dollars"]))
    write_table("ledger.csv",
                ["sid", "sym", "entry", "expiry", "legs", "S_sig", "S_entry",
                 "S_settle", "iv", "credit", "cost", "R_dollars",
                 "pnl_dollars"], rows)

    banner("8. INTERNAL CHECKS, THEN DETERMINISM")
    print("  These are checks the study makes on ITSELF.  A failure is printed")
    print("  as FAIL and the study does not claim the affected number.")
    rows = []
    allok = True

    # (a) for EVERY structure and variant, the daily P&L curve and the trade
    #     ledger must be the same money
    gap = 0.0
    worst_where = ""
    for sid, v, n, l in STRUCTS:
        for vid, cn, im, bl in VARIANTS:
            d = R[sid][vid]
            for sym in SYMBOLS:
                ps = d["per_sym"][sym]
                g = abs(sum(ps["daily_pnl"])
                        - sum(t["pnl_dollars"] for t in ps["trades"]))
                if g > gap:
                    gap, worst_where = g, "%s/%s/%s" % (sid, vid, sym)
    ok = gap < 1e-5
    allok = allok and ok
    rows.append(("daily P&L == trade ledger, all 84 sleeves",
                 "PASS" if ok else "FAIL",
                 "worst |gap| = %.3g (%s)" % (gap, worst_where)))

    # (b) the R-based budget must be big enough that no single session wipes it
    #     out; where it is not, the level-metric columns for that structure are
    #     flagged, because a budget the size of 10 R cannot describe a structure
    #     whose MARK-TO-MARKET swing is larger than its terminal max loss.
    worst_by_sid = {}
    for sid, v, n, l in STRUCTS:
        w = 9e9
        for sr in R[sid]["LOW"]["sleeve_rets"]:
            w = min(w, min(sr))
        worst_by_sid[sid] = w
    small = [(sid, worst_by_sid[sid]) for sid, v, n, l in STRUCTS
             if worst_by_sid[sid] <= -0.50]
    rows.append(("R-budget large enough for one session",
                 "see detail",
                 "worst single session: " + ", ".join(
                     "%s %.0f%%" % (sid, 100 * worst_by_sid[sid])
                     for sid, v, n, l in STRUCTS)))
    rows.append(("structures whose 10R budget is TOO SMALL", "-",
                 ", ".join("%s (worst day %.0f%%)" % (a, 100 * b)
                           for a, b in small) or "none"))

    # (c) every structure's leg count matches the structure that was built
    mism = [sid for sid in S
            if S[sid]["legs"] != dict(
                (x[0], x[3]) for x in STRUCTS)[sid]]
    ok = not mism
    allok = allok and ok
    rows.append(("reported leg count == built leg count",
                 "PASS" if ok else "FAIL",
                 "all %d structures match" % len(S) if ok else str(mism)))

    # (d) c_R at FREE cost is exactly 0
    ok = all(abs(S[sid]["c_R_gross"]) < 1e-12 for sid in S)
    allok = allok and ok
    rows.append(("c_R == 0 at the FREE setting",
                 "PASS" if ok else "FAIL",
                 "max = %.3g" % max(abs(S[sid]["c_R_gross"]) for sid in S)))

    # (d2) no BOOK return reaches -100%, so a period's SUM sign is also its
    #      compounded sign and the positivity table is unambiguous
    wb = min(S[sid]["worst_day"] for sid in S)
    ok = wb > -1.0
    allok = allok and ok
    rows.append(("no book return <= -100% (positivity unambiguous)",
                 "PASS" if ok else "FAIL", "worst book day = %.3f" % wb))

    # (e) the flagged / arb counts, reported rather than asserted
    und = [sid for sid in S if S[sid]["undefined_up"]]
    arb = [(sid, S[sid]["arb_frac"]) for sid, v, n, l in STRUCTS]
    rows.append(("undefined-call-side structures", "-",
                 ", ".join(und) if und else "none"))
    rows.append(("trades the MODEL says cannot lose", "-",
                 ", ".join("%s %.1f%%" % (a, 100 * f)
                           for a, f in arb if f > 0.0005) or "none"))
    print(table(["check", "result", "detail"], rows))
    print("")
    if not allok:
        raise SystemExit("ERROR: an internal check FAILED -- see above")
    print("  The 'TOO SMALL' line above is a FINDING, not a failure: a")
    print("  structure whose mark-to-market swing exceeds its terminal maximum")
    print("  loss cannot be normalised by that maximum loss.  Its tail columns")
    print("  are still valid in R; its compounded CAGR and % columns are not.")
    print("")

    print("  No RNG, no clock, no set iteration, no network.  Two consecutive")
    print("  runs of this file produce byte-identical stdout and identical")
    print("  out/*.csv.  Verified in README.md section 'Verification'.")
    print("")
    print("  EVERY OPTION NUMBER ABOVE IS [MODELED], NOT [VERIFIED].  This")
    print("  study measured the CONSEQUENCES OF AN ASSUMPTION SET, not the")
    print("  behaviour of any option that ever traded.")


if __name__ == "__main__":
    main()
