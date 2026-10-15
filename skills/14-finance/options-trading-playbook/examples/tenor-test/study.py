#!/usr/bin/env python3
"""
study.py -- DOES TENOR BUY EDGE?  One structure, one view, nine DTE buckets.

Holding the STRUCTURE and the VIEW constant, how do expectancy net of cost, the
daily theta yield on risk, tail risk, positivity-by-horizon, sample adequacy and
model (skew) sensitivity change as the time to expiry at entry goes from a week
to a LEAPS -- and is anything monotone in tenor?

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

STANDING LIMITATIONS (inherited from the sibling studies; unchanged here)
    The option model cannot see any of the following, and every [MODELED] figure
    must be held at arm's length because of it:
    1. no bid/ask spread in the QUOTE -- a flat per-contract cost IS charged, but
       the quote itself is a mid;
    2. no skew -- one implied vol prices every strike, so the sold leg is priced
       at the same vol as the wings.  Test 5 sizes this bias by re-pricing with
       the SOLD strikes charged +-1.5 vol points.  A real skew surface IS a
       function of tenor (the term structure of skew), and this model has none;
    3. no TERM STRUCTURE -- one vol (the 3-session-lagged VIX, a ~30-day vol)
       prices EVERY tenor from 7 DTE to 730 DTE.  This is the single largest new
       weakness of a tenor study, because a real 730-DTE implied vol is not the
       30-day VIX.  See LIMITATIONS section L1 in the README and section 11 here;
    4. no early exercise and NO ASSIGNMENT -- SPY/QQQ/IWM options are AMERICAN and
       physically settled; they are priced here as EUROPEAN and cash-settled.  An
       American short put can be assigned early and this model would never show
       it.  For a 730-DTE short leg this is a much larger omission than for a
       7-DTE one: over two years an American short call WILL be exercised
       ex-dividend and a deep-ITM short put can be assigned at any time;
    5. no pin risk -- the expiry session's close decides everything;
    6. no dividends -- the price series is price-only, so the modelled call is
       too expensive and the modelled put too cheap.  The bias compounds with
       tenor: a 730-DTE modelled call omits ~2 years of dividends;
    7. no margin, no buying-power constraint, no liquidity limit, no partial
       fills, no LEGGING RISK, no tax;
    8. strikes are NOT rounded to exchange increments.  A real SPY chain is
       $1-wide; this study's solved strikes may sit up to $0.50 off a listed
       strike.  At 0DTE the listing grid is $1 and the relevant moves are ~0.5%,
       so the rounding error is proportionally WORSE there than anywhere else;
    9. one contract per unit, integer, always fillable at the modelled mid;
   10. the entry is the OPEN of the session after the signal close and the exit
       is the CLOSE of the expiry session, with no management of any kind -- no
       stop, no profit target, no roll.  Every structure is held to expiry.

NEW LIMITATIONS THIS STUDY CREATES -- stated before the first run
   N1. NO INTRADAY PATH.  The bars are DAILY.  0DTE P&L is decided by the
       intraday path, so no multi-year 0DTE backtest is reported here from these
       bars.  0DTE is handled ANALYTICALLY (section 10); the one 0DTE
       computation that IS run is labelled [ILLUSTRATIVE] and is settled
       open-to-close, which is not the intraday path.
   N2. FIXED DOLLAR WING.  Every defined-risk structure uses a $5-wide wing at
       every tenor (the pre-registered convention).  One standard deviation of
       the terminal distribution is S*sigma*sqrt(T), which grows as sqrt(T), so a
       fixed $5 wing is a SHRINKING fraction of one sigma as tenor extends: about
       0.23 sigma at 7 DTE against 0.02 sigma at 730 DTE on a $770 index.  Part
       of any "tenor effect" on a 5-wide structure is therefore this convention,
       not the tenor.  The column W/sig*sqrt(T) is printed in every per-cell
       table so the drift is visible, and APPENDIX A re-runs two structures with
       the wing re-scaled to hold 0.15 sigma constant, which is the only way to
       separate the tenor effect from the width convention.
   N3. SEQUENTIAL NON-OVERLAPPING PROGRAMME.  Trades are entered back to back:
       the first at the start of the window, the next on the session after the
       previous expiry.  This is what makes n_available fall with tenor (the
       point of Test 3) and it means the entry CALENDAR differs by tenor -- the
       7-DTE programme enters ~1300 times, the 730-DTE programme ~12 times, and
       the two do not see the same set of dates.  A tenor difference is therefore
       a difference in BOTH the holding period and the entry dates sampled.
   N4. ONE VOL PER TENOR IS THE VIX, SO THE TENOR COMPARISON IS A COMPARISON AT
       A FIXED INPUT VOL, NOT AT THE VOL THE MARKET WOULD CHARGE.  In reality a
       730-DTE option trades at a different implied vol than a 7-DTE one (and a
       different skew).  Every long-tenor cell here is priced with a ~30-day vol,
       so it is cheap or rich relative to reality by an unknown sign.
   N5. THE RISK BUDGET IS 10 x R, where R is the structure's own modelled maximum
       loss per contract.  For a 1-leg long option R IS the debit, so the budget
       moves with the index and with sqrt(T) across a 25-year window in which SPY
       went 43 -> 770.  The budget is re-set to the position in force (the
       sibling's convention), which keeps the return series meaningful at both
       ends, but "10R" is 10 different dollar amounts on the first and last day.

USAGE
    py -3 study.py > run-output.txt        # stdout is the run log; RESULTS.md is
                                           # written beside this file, and every
                                           # table also lands in out/*.csv
"""

import bisect
import datetime
import io
import math
import os
import sys

# ---------------------------------------------------------------------------
# The timeframe engine owns the bucketing convention.  Import it rather than
# reimplement it, so a bucket key here cannot disagree with the engine's.
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

STUDY_DATE = "2026-10-15"

# ===========================================================================
# PRE-REGISTERED CONFIGURATION -- fixed BEFORE the first run
# ===========================================================================

SYMBOLS = ["SPY", "QQQ", "IWM"]
UNIVERSE = SYMBOLS + ["VIX", "US03M"]

TRADING_DAYS = 252
SMA_TREND = 200                # only used to set the start of the window
VIX_LAG_SESSIONS = 3           # only VIX from 3 sessions ago may price a leg
IV_TERM_ALPHA = 0.0            # IV(D) = VIX * (30/D)**alpha ; 0 = FLAT term
KAPPA_LOOKBACK = 60
KAPPA_CLIP = (0.60, 2.00)

# ---------------------------------------------------------------------------
# THE TENOR GRID, and the bucket each tenor belongs to.
#
# The bucket boundaries are `options-risk-engineer`'s EXACT partition:
#     0DTE (same session) . weeklies 1-7 . gamma shoulder 8-20 . monthlies 21-60
#     . quarterlies 60-120 . annuals 121-365 . LEAPS >365
#
# TWO BOUNDARIES ARE OVERLAPPING IN THE SKILL'S OWN LABELS and the assignment
# below is DECLARED BEFORE THE RUN rather than decided after seeing a result:
#   * 60 DTE is inside "monthlies 21-60" AND "quarterlies 60-120".  Assigned to
#     QUARTERLIES (the later bucket), following the skill's instruction to assign
#     by the position's own gamma and never to round down to the gentler bucket.
#   * 365 DTE is inside "annuals 121-365" and abuts "LEAPS >365".  Assigned to
#     ANNUALS, because >365 is strictly greater than 365.
# These two assignment calls are the only judgement made about the buckets, and
# section 9 reports them back to the owning skill.
# ---------------------------------------------------------------------------
TENORS = [
    (7, "weeklies"),
    (14, "gamma shoulder"),
    (30, "monthlies"),
    (45, "monthlies"),
    (60, "quarterlies"),
    (90, "quarterlies"),
    (180, "annuals"),
    (365, "annuals"),
    (730, "LEAPS"),
]
TENOR_DAYS = [t for t, _ in TENORS]
TENOR_BUCKET = dict(TENORS)

# ---- delta / moneyness rules (pre-registered, identical for every structure
#      that needs them).  Strikes are solved from the SIGNAL close.
D_16 = 0.16
D_25 = 0.25
D_30 = 0.30
D_50 = 0.50
WING = 5.0                     # dollars; every "5-wide" wing, EVERY tenor (N2)

# ---- grid over which a structure's maximum loss is measured
GRID_STEPS = 4000

# ---- capital model.  Every sleeve is a fixed risk budget of SLV_UNITS x one
#      unit of R, and its daily return is dollar P&L / that budget.  Same
#      declared number as the sibling studies, kept for comparability.
SLV_UNITS = 10.0

# ---- cost settings.  per-contract-leg cost on ONE TICKET =
#      fee + half_spread * 100 dollars.  The brief's "per-contract fee x
#      contracts x legs" is exactly this: `contracts` below IS the count of
#      contract-legs (sum of |qty| over option legs), so each option leg of each
#      contract is charged one ticket.  `etf_bps` is the round-trip cost on the
#      UNDERLYING (used only by the covered call's stock leg).
COST_SETTINGS = {
    "FREE": {"fee": 0.00, "half_spread": 0.000, "etf_bps": 0.0, "rt": 1},
    "LOW":  {"fee": 0.65, "half_spread": 0.025, "etf_bps": 5.0, "rt": 1},
    "HIGH": {"fee": 0.65, "half_spread": 0.050, "etf_bps": 20.0, "rt": 1},
    # ROUND TRIP: the skill's `cost-drag-per-leg-and-per-rung.md` convention --
    # two tickets per leg.  A LEG THAT EXPIRES HAS NO CLOSING TICKET, so the
    # headline convention here is ONE ticket per leg; this setting bounds the
    # other reading and is reported in Test 4.
    "RT_LOW": {"fee": 0.65, "half_spread": 0.025, "etf_bps": 10.0, "rt": 2},
}
HEADLINE_COST = "LOW"

# ---- THE PRE-REGISTERED STRUCTURES.  (id, name, option-leg contract count)
#      The brief enumerates SEVEN structures, not six: 2 one-leg, 3 two-leg,
#      2 four-leg.  All seven are run.  See README section 3 for the count
#      reconciliation.
STRUCTS = [
    ("S1", "long call ~50d", 1),
    ("S2", "cash-secured put ~16d", 1),
    ("S3", "short put spread ~16d / 5-wide", 2),
    ("S4", "bull call debit spread ~50d/25d", 2),
    ("S5", "covered call: long underlying + short ~30d call", 2),
    ("S6", "iron condor ~16d shorts / 5-wide wings", 4),
    ("S7", "iron butterfly ATM short / 5-wide wings", 4),
]
STRUCT_IDS = [s[0] for s in STRUCTS]
STRUCT_NAME = dict((s[0], s[1]) for s in STRUCTS)

# ---- the structures that carry a strike WIDTH, and therefore a credit/width
#      number.  W is DECLARED here, not derived per trade:
#        S3, S4, S6, S7 .......... W = $5.00 (the pre-registered wing)
#        S2 (cash-secured put) ... W = the short strike K (the cash secured)
#        S5 (covered call) ....... W = the underlying entry price (the notional)
#        S1 (long call) .......... W = n/a -- a naked long call has no width at
#                                  all, and its "credit" is a DEBIT.  Only the
#                                  debit/notional column is meaningful for it.
WIDTH_FIXED = {"S3": WING, "S4": WING, "S6": WING, "S7": WING}

# ---- the pre-registered variants.  `iv_mode` changes only the PRICING vol of
#      the stated legs; STRIKES ARE HELD FIXED at the base solve, so a
#      difference between two iv_modes is a pure pricing effect.  Both skew
#      DIRECTIONS are run: the sibling studies established that the model cannot
#      say which direction is right, only how much the answer depends on it.
VARIANTS = [
    ("BASE", "LOW", "BASE",
     "headline: $0.65/ticket/leg + $0.025/share half-spread, 5 bps stock"),
    ("SKEW_SOLD_P15", "LOW", "SOLD_P15",
     "SOLD option legs charged +1.5 vol points at pricing (strikes fixed)"),
    ("SKEW_SOLD_M15", "LOW", "SOLD_M15",
     "SOLD option legs charged -1.5 vol points at pricing (strikes fixed)"),
]
VARIANT_IDS = [v[0] for v in VARIANTS]

STRESS_WINDOWS = [
    ("2008 GFC", datetime.date(2008, 1, 1), datetime.date(2009, 3, 31)),
    ("2020 COVID", datetime.date(2020, 1, 1), datetime.date(2020, 12, 31)),
    ("2022 bear", datetime.date(2022, 1, 1), datetime.date(2022, 12, 31)),
]

NA = None
BUCKETS = ["M", "Q", "Y"]

# ---- the 0DTE analytic inputs, declared before the run
ODTE_T_SHORT = 0.25            # days, the "0DTE" holding period
ODTE_T_LONG = 30.0             # days, the reference tenor
ODTE_SIGMA = 0.20              # a stated 20% vol for the analytic block only
ODTE_FEE = 0.65                # $ per ticket, the LOW fee
ODTE_HALF_SPREAD = 0.025       # $ per share per ticket, the LOW half-spread
ODTE_CREDIT_LO = 0.05          # $ per share, the "small credit" band, low end
ODTE_CREDIT_HI = 0.20          # $ per share, the "small credit" band, high end
ODTE_WING_LO = 1.0             # $ strike width for the small-credit case
ODTE_WING_HI = 5.0             # $ strike width for the small-credit case


# ===========================================================================
# Output plumbing.  Every table is printed AND written to RESULTS.md, so the
# markdown a reader sees is the same object the run produced.
# ===========================================================================

MD = []


def emit(text=""):
    print(text)
    MD.append(text)


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


def md_table(headers, rows):
    out = ["| " + " | ".join(str(h) for h in headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def banner(title):
    emit("")
    emit("=" * 78)
    emit(title)
    emit("=" * 78)


def show(headers, rows, indent="  "):
    """Print a table AND append it to RESULTS.md as a markdown table."""
    emit(table(headers, rows, indent))
    MD.append("")
    MD.append(md_table(headers, rows))
    MD.append("")


def write_csv(name, header, rows):
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    path = os.path.join(OUT, name)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(",".join(str(h) for h in header) + "\n")
        for r in rows:
            fh.write(",".join(str(c) for c in r) + "\n")
    return len(rows)


def pct(x, nd=2):
    if x is NA:
        return "n/a"
    return ("%+.*f%%" % (nd, x * 100.0))


def pctu(x, nd=2):
    if x is NA:
        return "n/a"
    return ("%.*f%%" % (nd, x * 100.0))


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


def moneyu(x, nd=2):
    if x is NA:
        return "n/a"
    return ("%.*f" % (nd, x))


# ===========================================================================
# Black-Scholes.  The ONLY option pricer in this study.  Byte-identical in
# behaviour to the sibling studies' pricer (same bisection, same iteration
# count), so a hand re-derivation from either study's inputs lands on the same
# number.
# ===========================================================================

SQRT_2 = math.sqrt(2.0)
INV_SQRT_2PI = 1.0 / math.sqrt(2.0 * math.pi)


def ncdf(x):
    return 0.5 * (1.0 + math.erf(x / SQRT_2))


def npdf(x):
    return INV_SQRT_2PI * math.exp(-0.5 * x * x)


def bs_price(S, K, T, r, sigma, kind, q=0.0):
    """European Black-Scholes price per SHARE, continuous dividend yield q.

    q is 0.0 everywhere in this study (the price series carries no dividends,
    limitation 6).  At T -> 0 (or sigma -> 0) the value is intrinsic, so the
    same function settles an expiring leg as it prices a live one.
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


_STRIKE_CACHE = {}


# ---- strike solvers.  Memoised on the exact inputs: the same (S, T, r, iv,
#      target) recurs across every structure that uses that delta, and inside a
#      tenor the signal closes repeat.  Caching removes ~60% of the run time and
#      cannot change a single output digit.
#
#      BRACKET, AND WHY IT IS [0.02 S, 100 S] AND NOT THE SIBLING'S
#      [0.20 S, 1.60 S].  The sibling studies solved strikes on a bracket built
#      for 30-DTE structures.  On a 730-DTE ticket priced at a 2008-style 80%
#      vol, sigma*sqrt(T) is ~1.13 and the 25-delta CALL strike sits at about
#      8.4x spot -- outside the old bracket.  With no straddle check, bisection
#      then converged silently onto the bracket endpoint and returned a wrong
#      strike with no warning.  The independent handcheck.py caught exactly this
#      (it raises instead of converging), which is what it is for.  The bracket
#      is now wide enough for every tenor and vol in this study, and a bracket
#      that does not straddle the target RAISES rather than returning noise.
def _assert_bracket(f_lo, f_hi, kind, target, S, T, sigma):
    if f_lo * f_hi > 0.0:
        raise RuntimeError(
            "strike bracket does not straddle the target: kind=%s target=%s "
            "S=%r T=%r sigma=%r f(lo)=%r f(hi)=%r"
            % (kind, target, S, T, sigma, f_lo, f_hi))


def strike_for_put_delta(S, T, r, sigma, target, q=0.0):
    """K such that |put delta| == target.  |put delta| is INCREASING in K."""
    key = ("P", S, T, r, sigma, target, q)
    hit = _STRIKE_CACHE.get(key)
    if hit is not None:
        return hit
    lo, hi = 0.02 * S, 100.0 * S
    f_lo = abs(bs_delta(S, lo, T, r, sigma, "P", q)) - target
    f_hi = abs(bs_delta(S, hi, T, r, sigma, "P", q)) - target
    _assert_bracket(f_lo, f_hi, "P", target, S, T, sigma)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        f_mid = abs(bs_delta(S, mid, T, r, sigma, "P", q)) - target
        if f_lo * f_mid <= 0.0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    k = 0.5 * (lo + hi)
    _STRIKE_CACHE[key] = k
    return k


def strike_for_call_delta(S, T, r, sigma, target, q=0.0):
    """K such that call delta == target.  Call delta is DECREASING in K."""
    key = ("C", S, T, r, sigma, target, q)
    hit = _STRIKE_CACHE.get(key)
    if hit is not None:
        return hit
    lo, hi = 0.02 * S, 100.0 * S
    f_lo = bs_delta(S, lo, T, r, sigma, "C", q) - target
    f_hi = bs_delta(S, hi, T, r, sigma, "C", q) - target
    _assert_bracket(f_lo, f_hi, "C", target, S, T, sigma)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        f_mid = bs_delta(S, mid, T, r, sigma, "C", q) - target
        if f_lo * f_mid <= 0.0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    k = 0.5 * (lo + hi)
    _STRIKE_CACHE[key] = k
    return k


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
    if n <= 1 or p is NA or p <= 0.0 or p >= 1.0:
        return NA
    return math.log(n) / math.log(1.0 / (1.0 - p))


def trade_stats(rs):
    """p, b, E_form, E_R, p*, b*, sd, n_req, L_expected, L_actual, worst 1%.

    `rs` are GROSS R-multiples (settlement P&L / R, before cost), because the
    brief defines `E_net = E - c_R` and that identity only holds if E is the
    payoff's own expectancy.  `b` is (mean win) / |mean loss| in R units, as the
    skill defines it.  `E_form` is the skill's identity p*b - (1-p); `E_R` is the
    sample mean in R.  The two agree exactly only when the average loss is 1R,
    which it is NOT here: R is the STRUCTURE's maximum loss and most losses are
    smaller.  Both are reported; the gap is reported rather than hidden.
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
            "worst_trade": sorted(rs)[0], "best_trade": sorted(rs)[-1],
            "median_R": median(rs)}


def _period_bounds(bucket, d):
    if bucket == "D":
        return d, d
    if bucket == "W":
        mon = d - datetime.timedelta(days=d.isoweekday() - 1)
        return mon, mon + datetime.timedelta(days=6)
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
    of the FIXED budget.  Not the compounded curve: the sleeve's return is
    dollar P&L / a constant, so it is not compounded."""
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


def window_stat(dates, rets, d0, d1):
    """Total return in R and worst cumulative drawdown in R over [d0,d1], on the
    FIXED budget.  Used by the stress-window test."""
    idx = [j for j, d in enumerate(dates) if d0 <= d <= d1]
    if not idx:
        return NA, NA
    sub = [rets[j] for j in idx]
    return sum(sub) * SLV_UNITS, cum_dd(sub) * SLV_UNITS


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


def carry_forward(series, d, max_back=16):
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
# Implied vol model  (identical construction to the sibling studies)
# ===========================================================================

def build_iv_context(window_dates, series, vix):
    n = len(window_dates)
    vix_used = [NA] * n
    r_used = [NA] * n
    us03m = series["US03M"]
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


def iv_of(vix_pct, sym, j, kappa):
    if vix_pct is NA:
        return 0.0
    return vix_pct / 100.0 * kappa[sym][j]


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


def next_session_on_or_after(dates, target):
    i = bisect.bisect_left(dates, target)
    return dates[i] if i < len(dates) else NA



def last_session_on_or_before(dates, target):
    i = bisect.bisect_right(dates, target) - 1
    return dates[i] if i >= 0 else NA


def tenor_schedule(window_dates, tenor_days):
    """The pre-registered entry programme for ONE tenor.

    SEQUENTIAL AND NON-OVERLAPPING: the first trade opens on the second session
    of the window (the first needs a prior session to be its signal close), it is
    held to its expiry, and the next trade opens on the session AFTER that
    expiry.  The sleeve is therefore always in the market, and n_available falls
    with tenor: ~1300 trades at 7 DTE, ~12 at 730 DTE.

    Returns [(signal_date, entry_date, expiry_date)] with
        entry  = OPEN of entry_date
        signal = CLOSE of signal_date (the session before the entry)
        expiry = CLOSE of expiry_date, the first session on or after
                 entry + tenor_days.
    """
    out = []
    n = len(window_dates)
    j = 1
    while j < n:
        ent = window_dates[j]
        exp = next_session_on_or_after(
            window_dates, ent + datetime.timedelta(days=tenor_days))
        if exp is NA:
            break
        out.append((window_dates[j - 1], ent, exp))
        k = bisect.bisect_right(window_dates, exp)
        if k >= n:
            break
        j = k
    return out


# ===========================================================================
# Structures
# ===========================================================================

class Leg(object):
    """One leg of a structure.  kind: 'C', 'P' or 'S' (the underlying).

    qty is signed: -1 short, +1 long.  It is the number of CONTRACTS for an
    option leg and the number of 100-share units for the underlying.
    iv_off is ADDED to the pricing vol for this leg only (the skew knob), at
    entry AND at every mark, so a skew variant moves the whole trade, not just
    its opening premium.
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
    #    the position is written against, not a premium).
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


def build_legs(sid, S_sig, S_open, T, r, iv, wing=WING):
    """The pre-registered structure `sid`.  Strikes are solved from the SIGNAL
    close and the base implied vol; PRICING happens at the entry open and the
    variant's iv offsets are applied afterwards in run_cell.

    `wing` is $5.00 everywhere except in APPENDIX A's scale control, where it is
    re-solved so that the wing holds 0.15 sigma of the terminal distribution.

    Returns (legs, meta).  `meta` carries the leg count, the contract-leg count,
    the structure's declared WIDTH W (for credit/width), and the flags a reader
    needs: `undefined_up` (net short call slope as S -> infinity) and
    `has_stock`.
    """
    L = []
    if sid == "S1":
        L = [Leg("C", strike_for_call_delta(S_sig, T, r, iv, D_50), +1)]
    elif sid == "S2":
        L = [Leg("P", strike_for_put_delta(S_sig, T, r, iv, D_16), -1)]
    elif sid == "S3":
        K1 = strike_for_put_delta(S_sig, T, r, iv, D_16)
        L = [Leg("P", K1, -1), Leg("P", K1 - wing, +1)]
    elif sid == "S4":
        Kl = strike_for_call_delta(S_sig, T, r, iv, D_50)
        Ks = strike_for_call_delta(S_sig, T, r, iv, D_25)
        L = [Leg("C", Kl, +1), Leg("C", Ks, -1)]
    elif sid == "S5":
        L = [Leg("S", S_open, +1),
             Leg("C", strike_for_call_delta(S_sig, T, r, iv, D_30), -1)]
    elif sid == "S6":
        Kp = strike_for_put_delta(S_sig, T, r, iv, D_16)
        Kc = strike_for_call_delta(S_sig, T, r, iv, D_16)
        L = [Leg("P", Kp, -1), Leg("P", Kp - wing, +1),
             Leg("C", Kc, -1), Leg("C", Kc + wing, +1)]
    elif sid == "S7":
        K = S_sig                     # exactly ATM by construction
        L = [Leg("P", K, -1), Leg("C", K, -1),
             Leg("P", K - wing, +1), Leg("C", K + wing, +1)]
    else:
        raise ValueError("unknown structure %r" % sid)

    opt_legs = [x for x in L if x.is_option()]
    contracts = sum(abs(x.qty) for x in opt_legs)
    slope = 0.0
    for x in L:
        if x.kind == "C":
            slope += x.qty
        elif x.kind == "S":
            slope += x.qty
    # ---- the declared WIDTH W for the credit/width column
    if sid in WIDTH_FIXED:
        width = wing
    elif sid == "S2":
        width = L[0].K                # the cash secured against the short put
    elif sid == "S5":
        width = S_open                # the notional the call is written against
    else:
        width = NA                    # S1: a naked long call has no width
    meta = {"legs": len(L), "opt_legs": len(opt_legs), "contracts": contracts,
            "undefined_up": slope < -1e-12, "slope_up": slope,
            "has_stock": any(x.kind == "S" for x in L),
            "n_sold": sum(1 for x in opt_legs if x.is_short()),
            "n_long": sum(1 for x in opt_legs if not x.is_short()),
            "n_strikes": len(set((x.kind, x.K) for x in opt_legs)),
            "width": width}
    return L, meta


def max_loss_per_share(legs, S_open, sigma, T, unbounded_up):
    """Maximum LOSS per share of the structure over a terminal grid.

    P&L(S) = sum over legs of qty * (terminal value - entry value), which is the
    trade's own P&L per share and is 0 at S = S_open by construction, so the
    grid and the ledger cannot disagree about the payoff.

    BOUNDED structure (no net short call): grid = [0, 3*S_open].  R is a genuine
    structural maximum loss.  UNBOUNDED call side: there is no maximum loss to
    measure, so R is the loss at the STATED stop -- a terminal move of
    +-1.5 sigma*sqrt(T) -- and the structure is flagged.  No structure in THIS
    study is unbounded: S5's short call is covered by the long stock, so its
    slope up is 0.

    The terminal P&L is PIECEWISE LINEAR in S with kinks only at the option
    strikes, so its minimum lies on an endpoint or on an interior strike: a
    finite, exactly-derived candidate set.  The number is EXACT, not gridded.
    """
    if unbounded_up:
        lo = S_open * math.exp(-1.5 * sigma * math.sqrt(T))
        hi = S_open * math.exp(+1.5 * sigma * math.sqrt(T))
        at_boundary = True
    else:
        lo, hi = 0.0, 3.0 * S_open
        at_boundary = False
    cands = set([lo, hi])
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


def trade_greeks(legs, S_open, T, r, iv):
    """Net position Greeks at entry, in SHARE-equivalents per 100 shares."""
    d = g = v = th = 0.0
    for x in legs:
        if not x.is_option():
            d += x.qty * 100.0
            continue
        dl, gm, vg, tq = bs_greeks(S_open, x.K, T, r,
                                   max(1e-6, iv + x.iv_off), x.kind)
        d += x.qty * 100.0 * dl
        g += x.qty * 100.0 * gm
        v += x.qty * 100.0 * vg
        th += x.qty * 100.0 * tq
    return d, g, v, th


def _leg_iv_off(leg, iv_mode):
    """The variant's pricing-vol offset for ONE leg.

    BASE        : 0 for every leg.
    SOLD_P15    : +1.5 vol points on SOLD option legs.
    SOLD_M15    : -1.5 vol points on SOLD option legs -- the conservative
                  direction, and the one that matches "a real seller of an OTM
                  option collects less than the flat-vol Black-Scholes value".
    Strikes never move.
    """
    if not leg.is_option():
        return 0.0
    if iv_mode == "SOLD_P15" and leg.is_short():
        return 0.015
    if iv_mode == "SOLD_M15" and leg.is_short():
        return -0.015
    return 0.0


def entry_cost(legs, meta, cost_name, S_open):
    """Dollars charged at the OPEN for one unit of the structure.

    One ticket per contract-leg, priced at `fee + half_spread*100` (the brief's
    formula).  Under "rt" the charge is doubled to bound the round-trip
    convention of `cost-drag-per-leg-and-per-rung.md`.  The covered call pays a
    round-trip bps cost on its stock leg as well.
    """
    c = COST_SETTINGS[cost_name]
    per_contract = (c["fee"] + c["half_spread"] * 100.0) * c["rt"]
    total = per_contract * meta["contracts"]
    if meta["has_stock"]:
        total += (c["etf_bps"] / 10000.0) * S_open * 100.0
    return total


# ===========================================================================
# The simulation -- one structure, one index, one tenor, one variant
# ===========================================================================

def run_cell(sid, sym, tenor, iv_mode, series, window_dates, iv_ctx,
             wing=WING, wing_mode="FIXED"):
    """Returns {"daily_pnl": [...], "daily_base": [...], "trades": [...]}.

    `wing_mode` "FIXED" uses the pre-registered $5.00 wing at every tenor.
    "SIG015" re-solves the wing per trade so that it holds 0.15 of one standard
    deviation of the terminal distribution, which is APPENDIX A's scale control:
    the only way to separate a tenor effect from the fixed-dollar-wing
    convention (limitation N2).

    Entry at the OPEN of the entry session, strikes solved from the SIGNAL
    close, held to the expiry session and settled at INTRINSIC against the REAL
    close.  Equity is cash + mark; the sleeve is tracked in DOLLARS.

    `daily_base[j]` is the RISK BUDGET IN FORCE that session = SLV_UNITS x the
    maximum loss of the position actually open that day.  A single 25-year
    constant budget would be wrong: a long call's max loss IS its debit, which
    scales with the index level AND with sqrt(T), so one constant dollar figure
    cannot be 10R in 2001 and in 2026, or 10R at 7 DTE and at 730 DTE.
    """
    vix_used, r_used, kappa = iv_ctx
    s = series[sym]
    pos_of = dict((d, j) for j, d in enumerate(window_dates))

    sched = tenor_schedule(window_dates, tenor)
    trades = [{"sym": sym, "sid": sid, "tenor": tenor, "sig": sig_d,
               "entry": ent_d, "expiry": exp_d, "open": False, "closed": False,
               "legs": None, "meta": None, "credit": NA, "iv": NA, "r": NA,
               "S_sig": NA, "S_entry": NA, "S_settle": NA, "K_summary": "",
               "R_dollars": NA, "delta": NA, "gamma": NA, "vega": NA,
               "theta": NA, "T_entry": NA, "costs": {}, "arb_model": False,
               "model_max_loss": NA, "width": NA, "width_over_sigT": NA,
               "at_boundary": False}
              for sig_d, ent_d, exp_d in sched]
    by_entry = dict((t["entry"], t) for t in trades)

    n = len(window_dates)
    cash = 0.0
    prev_eq = 0.0
    daily = [0.0] * n
    daily_base = [0.0] * n
    open_legs = []
    open_tr = [None]

    for j, d in enumerate(window_dates):
        k = s.index_of[d]
        S_open, S_close = s.o[k], s.c[k]
        day_tr = None

        # ---- 1. at the OPEN: enter the trade whose entry date is today
        tr = by_entry.get(d)
        if tr is not None:
            j_sig = pos_of[tr["sig"]]
            k_sig = s.index_of[tr["sig"]]
            T_entry = max(0.0, (tr["expiry"] - d).days) / 365.0
            r_now = r_used[j_sig]
            iv_now = iv_of(vix_used[j_sig], sym, j_sig, kappa)
            if iv_now > 0.0 and T_entry > 0.0:
                S_sig = s.c[k_sig]
                if wing_mode == "SIG015":
                    _w = max(1.0, float(round(0.15 * S_sig * iv_now *
                                              math.sqrt(T_entry))))
                else:
                    _w = wing
                legs, meta = build_legs(sid, S_sig, S_open, T_entry, r_now,
                                        iv_now, _w)
                credit = 0.0
                for x in legs:
                    x.iv_off = _leg_iv_off(x, iv_mode)
                    x.expiry = tr["expiry"]
                    x.T_entry = T_entry
                    if x.kind == "S":
                        x.px_entry = S_open
                    else:
                        x.px_entry = bs_price(S_open, x.K, T_entry, r_now,
                                              max(1e-6, iv_now + x.iv_off),
                                              x.kind)
                    credit += x.entry_cash_dollars()
                costs = dict((cname, entry_cost(legs, meta, cname, S_open))
                             for cname in COST_SETTINGS)
                cash += credit - costs[HEADLINE_COST]
                open_legs.extend(legs)
                open_tr[0] = tr
                day_tr = tr
                dlt, gam, veg, th = trade_greeks(legs, S_open, T_entry,
                                                 r_now, iv_now)
                ks = " ".join("%s%.1f%s%+d" % (x.kind, x.K, "@", x.qty)
                              for x in legs if x.is_option())
                ml, atb = max_loss_per_share(legs, S_open, iv_now, T_entry,
                                             meta["undefined_up"])
                arb = ml <= 0.0
                R = (_w * 100.0) if arb else ml * 100.0
                sig_sqrtT = iv_now * math.sqrt(T_entry)
                w = meta["width"]
                tr.update({"open": True, "legs": legs, "meta": meta,
                           "credit": credit, "iv": iv_now, "r": r_now,
                           "S_sig": S_sig, "S_entry": S_open, "K_summary": ks,
                           "delta": dlt, "gamma": gam, "vega": veg,
                           "theta": th, "T_entry": T_entry, "costs": costs,
                           "R_dollars": R, "arb_model": arb,
                           "model_max_loss": ml, "at_boundary": atb,
                           "width": w,
                           "width_over_sigT": (w / (S_open * sig_sqrtT)
                                               if (w is not NA and
                                                   sig_sqrtT > 0) else NA)})

        # ---- 2. at the CLOSE: settle anything expiring today at INTRINSIC
        for tr2 in trades:
            if not tr2["open"] or tr2["expiry"] != d:
                continue
            tm = 0.0
            fm = 0.0
            for x in tr2["legs"]:
                tm += x.terminal_dollars(S_close)
                fm += x.mark_dollars(S_close, 0.0, r_used[j], 0.0)
                open_legs.remove(x)
            # CASH gets the final MARK, not the terminal P&L: the premium was
            # already paid/received at entry, and the leg's mark at entry is
            # -premium, so equity is continuous.  The trade ledger carries BOTH
            # the gross terminal P&L and the net (gross - cost).
            cash += fm
            tr2["open"] = False
            tr2["closed"] = True
            tr2["S_settle"] = S_close
            tr2["pnl_gross_dollars"] = tm
            tr2["pnl_dollars"] = tm - tr2["costs"][HEADLINE_COST]
            open_tr[0] = None
            day_tr = tr2

        # ---- 3. at the CLOSE: mark whatever is still open
        mark = 0.0
        for x in open_legs:
            T = max(0.0, (x.expiry - d).days) / 365.0
            sig = iv_of(vix_used[j], sym, j, kappa)
            mark += x.mark_dollars(S_close, T, r_used[j], sig)
        eq = cash + mark
        daily[j] = eq - prev_eq
        prev_eq = eq
        if day_tr is None:
            day_tr = open_tr[0]
        if day_tr is not None and day_tr["R_dollars"] is not NA:
            daily_base[j] = SLV_UNITS * day_tr["R_dollars"]

    out_trades = []
    for tr in trades:
        if not tr["closed"]:
            continue
        R = tr["R_dollars"]
        cost_low = tr["costs"][HEADLINE_COST]
        gross = tr["pnl_gross_dollars"]
        out_trades.append({
            "sid": sid, "sym": sym, "tenor": tenor,
            "entry_date": tr["entry"], "exit_date": tr["expiry"],
            "hold_days": (tr["expiry"] - tr["entry"]).days,
            "legs": tr["meta"]["legs"], "contracts": tr["meta"]["contracts"],
            "R_dollars": R, "model_max_loss": tr["model_max_loss"],
            "arb_model": tr["arb_model"], "at_boundary": tr["at_boundary"],
            "undefined_up": tr["meta"]["undefined_up"],
            "credit": tr["credit"], "credit_per_share": tr["credit"] / 100.0,
            "cost": cost_low,
            "cost_free": tr["costs"]["FREE"], "cost_high": tr["costs"]["HIGH"],
            "cost_rt": tr["costs"]["RT_LOW"],
            "pnl_gross_dollars": gross,
            "pnl_dollars": gross - cost_low,
            "R_mult": (gross / R) if R else NA,          # GROSS, per the brief
            "cost_R": (cost_low / R) if R else NA,
            "cost_R_high": (tr["costs"]["HIGH"] / R) if R else NA,
            "cost_R_rt": (tr["costs"]["RT_LOW"] / R) if R else NA,
            "S_entry": tr["S_entry"], "S_sig": tr["S_sig"],
            "S_settle": tr["S_settle"], "iv": tr["iv"], "r": tr["r"],
            "T_entry": tr["T_entry"],
            "delta": tr["delta"], "gamma": tr["gamma"], "vega": tr["vega"],
            "theta": tr["theta"], "width": tr["width"],
            "width_over_sigT": tr["width_over_sigT"],
            "n_sold": tr["meta"]["n_sold"],
            "n_strikes": tr["meta"]["n_strikes"]})
    for t in out_trades:
        t["net_R"] = t["R_mult"] - t["cost_R"]
    return {"daily_pnl": daily, "daily_base": daily_base, "trades": out_trades}


# ===========================================================================
# Aggregation: one cell = one structure x one tenor x one variant, pooled over
# the three indexes.  The book series is the equal-weight mean of the sleeves'
# FIXED-BUDGET return series (the sibling studies' convention).
# ===========================================================================

def book_from_sleeves(sleeve_rets):
    n = len(sleeve_rets[0])
    k = float(len(sleeve_rets))
    return [sum(r[j] for r in sleeve_rets) / k for j in range(n)]


def run_all(series, window_dates, iv_ctx):
    """{variant: {(sid, tenor): cell}} -- cell carries trades, the book series,
    the per-index sleeves and the median risk budget."""
    res = {}
    for vid, cost_name, iv_mode, _blurb in VARIANTS:
        cells = {}
        for sid in STRUCT_IDS:
            for tenor in TENOR_DAYS:
                sys.stderr.write("  [run] %s %s %dd\n" % (vid, sid, tenor))
                sys.stderr.flush()
                sleeve_rets, trades, per_sym, bases = [], [], {}, []
                for sym in SYMBOLS:
                    r = run_cell(sid, sym, tenor, iv_mode, series,
                                 window_dates, iv_ctx)
                    med_r = median([t["R_dollars"] for t in r["trades"]])
                    base = SLV_UNITS * (med_r if med_r is not NA else 1.0)
                    bases.append(base)
                    per_sym[sym] = {"base": base,
                                    "n": len(r["trades"]),
                                    "daily_pnl": r["daily_pnl"],
                                    "daily_base": r["daily_base"]}
                    sleeve_rets.append([(p / b) if b else 0.0
                                        for p, b in zip(r["daily_pnl"],
                                                        r["daily_base"])])
                    trades.extend(r["trades"])
                cells[(sid, tenor)] = {
                    "sid": sid, "tenor": tenor,
                    "book_rets": book_from_sleeves(sleeve_rets),
                    "sleeve_rets": sleeve_rets, "per_sym": per_sym,
                    "trades": trades, "base_median": mean(bases)}
        res[vid] = cells
    return res


def cell_stats(trades, book_rets, window_dates, groups, tenor):
    """Every pre-registered per-cell number.  `trades` are pooled over the three
    indexes; `E` is the GROSS expectancy in R so that E_net = E - c_R holds."""
    st = trade_stats([t["R_mult"] for t in trades])
    st["tenor"] = tenor
    st["n_per_index"] = st["n"] / float(len(SYMBOLS))
    st["p_net"] = (sum(1 for t in trades if t["net_R"] > 0.0) / float(st["n"])
                   if st["n"] else NA)
    st["c_R"] = mean([t["cost_R"] for t in trades])
    st["c_R_high"] = mean([t["cost_R_high"] for t in trades])
    st["c_R_rt"] = mean([t["cost_R_rt"] for t in trades])
    st["c_R_free"] = 0.0
    st["E_net"] = st["E_R"] - st["c_R"]
    st["E_net_high"] = st["E_R"] - st["c_R_high"]
    st["E_net_rt"] = st["E_R"] - st["c_R_rt"]
    st["c_R_star"] = st["E_R"]                      # break-even cost in R units
    st["cost_dollars_med"] = median([t["cost"] for t in trades])
    st["R_dollars_med"] = median([t["R_dollars"] for t in trades])
    st["c_R_star_dollars"] = (st["c_R_star"] * st["R_dollars_med"]
                              if st["c_R_star"] is not NA else NA)
    st["credit_med"] = median([t["credit"] for t in trades])
    st["credit_ps_med"] = median([t["credit_per_share"] for t in trades])
    st["S_entry_med"] = median([t["S_entry"] for t in trades])
    st["iv_med"] = median([t["iv"] for t in trades])
    w = [t["width"] for t in trades if t["width"] is not NA]
    st["width"] = median(w) if w else NA
    st["credit_over_width"] = (median([t["credit_per_share"] / t["width"]
                                      for t in trades
                                      if t["width"] is not NA])
                              if w else NA)
    st["credit_over_notional"] = median([t["credit_per_share"] / t["S_entry"]
                                         for t in trades])
    st["R_over_notional"] = median([t["R_dollars"] / (t["S_entry"] * 100.0)
                                    for t in trades])
    st["width_over_sigT"] = median([t["width_over_sigT"] for t in trades
                                    if t["width_over_sigT"] is not NA]) \
        if any(t["width_over_sigT"] is not NA for t in trades) else NA
    st["hold_days_med"] = median([t["hold_days"] for t in trades])
    # ---- theta-per-day per unit of R.  The brief's derivation: the credit
    #      divided by the tenor in days, divided by R.  Both in dollars, so the
    #      per-share factor cancels.  A DEBIT structure carries a NEGATIVE
    #      credit and therefore a negative (costly) daily yield.
    st["theta_pd_R"] = (st["credit_med"] / (tenor * st["R_dollars_med"])
                        if (st["credit_med"] is not NA and
                            st["R_dollars_med"] not in (NA, 0.0)) else NA)
    # ---- the same number with the REALISED median holding period, as a guard
    st["theta_pd_R_real"] = (st["credit_med"] /
                             (st["hold_days_med"] * st["R_dollars_med"])
                             if (st["credit_med"] is not NA and
                                 st["hold_days_med"] not in (NA, 0.0) and
                                 st["R_dollars_med"] not in (NA, 0.0))
                             else NA)
    st["legs"] = trades[0]["legs"] if trades else NA
    st["contracts"] = trades[0]["contracts"] if trades else NA
    st["n_sold"] = trades[0]["n_sold"] if trades else NA
    st["n_strikes"] = trades[0]["n_strikes"] if trades else NA
    st["undefined_up"] = trades[0]["undefined_up"] if trades else NA
    st["arb_frac"] = (sum(1 for t in trades if t["arb_model"]) /
                      float(st["n"])) if st["n"] else NA
    st["delta"] = mean([t["delta"] for t in trades])
    st["gamma"] = mean([t["gamma"] for t in trades])
    st["vega"] = mean([t["vega"] for t in trades])
    st["bs_theta"] = mean([t["theta"] for t in trades])
    st["tot_R"] = st["total_R"]
    ls = level_stats(window_dates, book_rets)
    st["years"] = ls["years"]
    st["cagr_compounded"] = ls["cagr"]
    st["max_dd_compounded"] = ls["max_dd"]
    st["sharpe"] = ls["sharpe"]
    st["ann_budget"] = sum(book_rets) / ls["years"]
    # ---- CAGR-equivalent: the annualised return on ONE unit of R, with the
    #      sleeve continuously committed (trades are sequential, so a 1R sleeve
    #      is in the market from the first session to the last).  Comparable
    #      across tenors by construction.
    st["ann_R"] = (sum(t["R_mult"] for t in trades) / ls["years"]
                   if trades else NA)
    st["ann_R_net"] = (sum(t["net_R"] for t in trades) / ls["years"]
                       if trades else NA)
    st["dd_budget"] = cum_dd(book_rets)
    st["dd_R"] = st["dd_budget"] * SLV_UNITS
    st["worst_day"] = min(book_rets) if book_rets else NA
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
        st["pos_" + b + "_gap"] = (st["pos_" + b + "_law"] - f1
                                   if st["pos_" + b + "_law"] is not NA and
                                   f1 is not NA else NA)
    st["inverted_MY"] = (st["pos_M"] is not NA and st["pos_Y"] is not NA and
                         st["pos_M"] > st["pos_Y"])
    # ---- tail measures that are NOT pinned at -1R by construction.  For every
    #      defined-risk structure the WORST TRADE is the structural maximum loss,
    #      so |worst trade| is 1.000 at every tenor and says nothing about tenor.
    #      What DOES vary is how OFTEN the tail is realised and how deep the
    #      ordinary bad tail is.
    st["frac_at_max"] = (sum(1 for t in trades if t["R_mult"] <= -0.98) /
                         float(st["n"])) if st["n"] else NA
    rs_sorted = sorted(t["R_mult"] for t in trades)
    nn = len(rs_sorted)
    st["p05"] = rs_sorted[max(0, int(round(0.05 * nn)) - 1)] if nn else NA
    st["p25"] = rs_sorted[max(0, int(round(0.25 * nn)) - 1)] if nn else NA
    st["p50"] = median(rs_sorted)
    st["p75"] = rs_sorted[min(nn - 1, int(round(0.75 * nn)))] if nn else NA
    return st


# ===========================================================================
# Reporting
# ===========================================================================

def fmt_p(x):
    return "n/a" if x is NA else ("%.4f" % x)


def fmt_n_req(x):
    if x is NA:
        return "n/a"
    if x >= 1e6:
        return "%.2ge" % x
    return "%d" % int(round(x))


def stat_at(S, sid, tenor, field, variant="BASE"):
    c = S[variant].get((sid, tenor))
    return NA if c is NA else c.get(field, NA)


def peak_of(S, sid, field, variant="BASE"):
    """The tenor at which `field` peaks for this structure, and the value."""
    best_t, best_v = NA, NA
    for t in TENOR_DAYS:
        v = stat_at(S, sid, t, field, variant)
        if v is NA:
            continue
        if best_v is NA or v > best_v:
            best_t, best_v = t, v
    return best_t, best_v


def pearson(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys)
             if x is not NA and y is not NA]
    n = len(pairs)
    if n < 3:
        return NA
    mx = sum(p[0] for p in pairs) / float(n)
    my = sum(p[1] for p in pairs) / float(n)
    sxy = sum((p[0] - mx) * (p[1] - my) for p in pairs)
    sxx = sum((p[0] - mx) ** 2 for p in pairs)
    syy = sum((p[1] - my) ** 2 for p in pairs)
    if sxx <= 0.0 or syy <= 0.0:
        return NA
    return sxy / math.sqrt(sxx * syy)


def spearman(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not NA and y is not NA]
    n = len(pairs)
    if n < 4:
        return NA
    rx = _ranks([p[0] for p in pairs])
    ry = _ranks([p[1] for p in pairs])
    return pearson(rx, ry)


def _ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


# ===========================================================================
# main
# ===========================================================================

def main():
    banner("TENOR TEST -- does tenor buy edge, or only change the clock?")
    emit("Pre-registered.  Deterministic.  No RNG, no clock, no network.")
    emit("")
    emit("READ THIS BEFORE ANY NUMBER: every option price below is [MODELED].")
    emit("Historical option quotes are not available from the sources used.")
    emit("Legs are priced with Black-Scholes on a VIX-derived implied vol and")
    emit("settled against the REAL index close on the expiry session.  The")
    emit("model has: no quote spread, NO SKEW, NO TERM STRUCTURE (one vol for")
    emit("every strike AND every tenor), NO EARLY EXERCISE AND NO ASSIGNMENT")
    emit("(SPY/QQQ/IWM options are American and physically settled; they are")
    emit("priced here as European and cash-settled), no pin risk, no dividends,")
    emit("no margin, no liquidity limit, NO LEGGING RISK, unrounded strikes.")
    emit("A flat per-contract cost IS charged; the QUOTE is still a mid.")
    emit("")

    # ---------------------------------------------------------------- data
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
        emit("  %-6s rows=%-6d first=%s last=%s"
             % (sym, len(s.dates), s.dates[0].isoformat(),
                s.dates[-1].isoformat()))
    emit("")
    emit("  Provenance of SPY (verbatim; the other four carry the same chain):")
    for line in prov["SPY"]:
        emit("    %s" % line)

    window_dates = build_window(series)
    iv_ctx = build_iv_context(window_dates, series, series["VIX"])
    years = years_between(window_dates[0], window_dates[-1])
    groups = dict((b, group_index(window_dates, b)) for b in BUCKETS)
    emit("")
    emit("  COMMON WINDOW (identical construction to the sibling studies:")
    emit("  the intersection of the five series, from the first session on")
    emit("  which every index has a 200-session SMA):")
    emit("    %s ... %s   %d sessions   %.2f years"
         % (window_dates[0].isoformat(), window_dates[-1].isoformat(),
            len(window_dates), years))
    emit("    complete months=%d  complete quarters=%d  complete years=%d"
         % (len(groups["M"]), len(groups["Q"]), len(groups["Y"])))

    # ----------------------------------------------------- pre-registration
    banner("1. PRE-REGISTRATION -- declared before the first number was computed")
    emit("")
    emit("TENOR GRID (DTE at entry).  The bucket labels are")
    emit("`options-risk-engineer`'s EXACT partition, not this study's:")
    emit("  0DTE (same session) . weeklies 1-7 . gamma shoulder 8-20 .")
    emit("  monthlies 21-60 . quarterlies 60-120 . annuals 121-365 .")
    emit("  LEAPS >365")
    emit("")
    rows = []
    for t, b in TENORS:
        rows.append([t, b])
    show(["tenor DTE", "skill bucket"], rows)
    emit("BOUNDARY CALLS MADE HERE, DECLARED BEFORE THE RUN (the skill's own")
    emit("labels overlap at two places and an assignment had to be chosen):")
    emit("  * 60 DTE is inside 'monthlies 21-60' AND 'quarterlies 60-120'.")
    emit("    Assigned to QUARTERLIES -- the later bucket, following the")
    emit("    skill's rule to assign by the position's own gamma and never to")
    emit("    round down to the gentler bucket.")
    emit("  * 365 DTE is inside 'annuals 121-365' and abuts 'LEAPS >365'.")
    emit("    Assigned to ANNUALS, because >365 excludes 365.")
    emit("  0DTE is NOT a backtested tenor here.  Daily bars cannot see the")
    emit("  intraday path that decides 0DTE P&L; the 0DTE answer is ANALYTIC")
    emit("  (section 10) plus one clearly-labelled [ILLUSTRATIVE] computation")
    emit("  (section 11) that CANNOT be extrapolated.")
    emit("")
    emit("STRUCTURES -- the brief enumerates SEVEN, not six (2 one-leg, 3")
    emit("two-leg, 2 four-leg).  All seven are run; see README section 3.")
    rows = []
    for sid, name, nlegs in STRUCTS:
        w = WIDTH_FIXED.get(sid)
        rows.append([sid, name, nlegs, (("%.1f" % w) if w is not None
                                        else ("R/share" if sid == "S2"
                                              else ("S_entry" if sid == "S5"
                                                    else "n/a")))])
    show(["id", "structure", "option legs", "declared width W"], rows)
    emit("W is DECLARED, not derived per trade: $5.00 for the four wing")
    emit("structures; for the cash-secured put W is the short strike K (the")
    emit("cash actually secured); for the covered call W is the underlying")
    emit("entry price (the notional the call is written against).  A naked")
    emit("long call has NO width at all -- only its debit/notional is")
    emit("meaningful, and its 'credit' is a DEBIT.")
    emit("")
    emit("ENTRY PROGRAMME: sequential and non-overlapping.  The first trade")
    emit("opens on the second session of the window, exits on the first")
    emit("session on or after entry + tenor days, and the next trade opens on")
    emit("the session after that expiry.  The sleeve is always in the market.")
    emit("Entry is at the OPEN, strikes are solved from the SIGNAL close (the")
    emit("prior session), and settlement is at INTRINSIC against the expiry")
    emit("session's REAL close.  Nothing is managed: no stop, no target, no")
    emit("roll.")
    emit("")
    emit("R = the structure's own modelled MAXIMUM LOSS per contract (exact")
    emit("piecewise-linear minimum, not a grid).  Every structure here is")
    emit("BOUNDED: the covered call's short call is covered by stock, so no")
    emit("stated-stop normalisation is needed anywhere in this study.")
    emit("")
    emit("COST (headline LOW) = ($0.65 + $0.025 x 100) per ticket per")
    emit("contract-leg, one ticket per leg: $3.15 per leg, so $3.15 / $6.30 /")
    emit("$12.60 per unit for 1 / 2 / 4 legs.  The covered call also pays 5 bps")
    emit("round trip on its stock leg.  HIGH doubles the spread widening;")
    emit("RT_LOW doubles every ticket (the round-trip convention of")
    emit("`cost-drag-per-leg-and-per-rung.md`).  A LEG THAT EXPIRES HAS NO")
    emit("CLOSING TICKET, which is why one ticket per leg is the headline.")
    emit("")
    emit("E is the GROSS expectancy in R (settlement P&L / R, before cost), so")
    emit("that the brief's identity E_net = E - c_R holds exactly.  p and b are")
    emit("computed on the same gross series; p_net is reported beside them.")
    emit("")
    emit("n_available = trades POOLED over SPY+QQQ+IWM (the sibling studies'")
    emit("convention); n_per_index = n_available / 3.  n_req = 4 (sd/|E|)^2.")
    emit("")
    emit("THE EXPECTED SAMPLE SIZES, computed from the schedule itself BEFORE")
    emit("any P&L:")
    rows = []
    for t in TENOR_DAYS:
        nsch = len(tenor_schedule(window_dates, t))
        rows.append([t, TENOR_BUCKET[t], nsch, nsch * len(SYMBOLS)])
    show(["DTE", "bucket", "trades / index", "n_available (pooled)"], rows)
    emit("Read the bottom row against the top: a 730-day tenor over a %.1f-year"
         % years)
    emit("window yields about %.0f non-overlapping trades per index.  Every"
         % (years * 365.25 / 730.0))
    emit("long-tenor cell below is graded against that, not against 1000.")
    emit("")

    # ------------------------------------------------------------- the run
    banner("2. THE RUN")
    emit("")
    emit("  %d structures x %d tenors = %d cells per index"
         % (len(STRUCT_IDS), len(TENOR_DAYS),
            len(STRUCT_IDS) * len(TENOR_DAYS)))
    emit("  x %d indexes = %d sleeves, x %d variants = %d simulated sleeves."
         % (len(SYMBOLS), len(STRUCT_IDS) * len(TENOR_DAYS) * len(SYMBOLS),
            len(VARIANTS),
            len(STRUCT_IDS) * len(TENOR_DAYS) * len(SYMBOLS) * len(VARIANTS)))
    emit("")
    res = run_all(series, window_dates, iv_ctx)
    S = {}
    for vid in VARIANT_IDS:
        S[vid] = {}
        for sid in STRUCT_IDS:
            for t in TENOR_DAYS:
                c = res[vid][(sid, t)]
                S[vid][(sid, t)] = cell_stats(c["trades"], c["book_rets"],
                                              window_dates, groups, t)
    n_cells = sum(1 for _ in S["BASE"])
    emit("  CELLS ACTUALLY STATISTICISED (variant BASE): %d" % n_cells)
    emit("  (reported grid = %d structures x %d tenors = %d; matches: %s)"
         % (len(STRUCT_IDS), len(TENOR_DAYS),
            len(STRUCT_IDS) * len(TENOR_DAYS),
            "YES" if n_cells == len(STRUCT_IDS) * len(TENOR_DAYS) else "NO"))
    report(S, res, window_dates, groups, years, series, iv_ctx)


# ===========================================================================
# The tests
# ===========================================================================

def monotone_note(vals_by_tenor):
    """'increasing' / 'decreasing' / 'NOT monotone (k sign changes)'."""
    v = [(t, x) for t, x in vals_by_tenor if x is not NA]
    if len(v) < 2:
        return "n/a"
    diffs = [v[i + 1][1] - v[i][1] for i in range(len(v) - 1)]
    pos = sum(1 for d in diffs if d > 0)
    neg = sum(1 for d in diffs if d < 0)
    zero = sum(1 for d in diffs if d == 0)
    if pos == 0 and neg == 0:
        return "flat"
    if pos == 0:
        return "DECREASING (%d down, %d flat)" % (neg, zero)
    if neg == 0:
        return "INCREASING (%d up, %d flat)" % (pos, zero)
    k = 0
    sgn = 0
    for d in diffs:
        s = 1 if d > 0 else (-1 if d < 0 else 0)
        if s == 0:
            continue
        if sgn and s != sgn:
            k += 1
        sgn = s
    return "NOT monotone (%d sign changes)" % k


def report(S, res, window_dates, groups, years, series, iv_ctx):
    # ============================================================== TEST 1
    banner("3. TEST 1 -- is anything monotone in tenor?")
    emit("")
    emit("Cells ordered by DTE.  E is GROSS (settlement P&L / R); c_R is the")
    emit("headline LOW cost / R; E_net = E - c_R; cr/W is the net premium per")
    emit("share as a fraction of the structure's declared width W; theta/day/R")
    emit("is the credit divided by the tenor in days divided by R -- the daily")
    emit("yield on the risk actually carried; ann_R_net is the annualised")
    emit("return on one unit of R continuously committed.  Everything is")
    emit("[MODELED].")
    summary = []
    for sid in STRUCT_IDS:
        emit("")
        emit("--- %s  %s  (%d option legs, %d contract-legs per unit)"
             % (sid, STRUCT_NAME[sid],
                S["BASE"][(sid, TENOR_DAYS[0])]["legs"],
                S["BASE"][(sid, TENOR_DAYS[0])]["contracts"]))
        rows = []
        evals = []
        for t in TENOR_DAYS:
            c = S["BASE"][(sid, t)]
            evals.append((t, c["E_net"]))
            rows.append([
                t, TENOR_BUCKET[t], c["n"], fmt_n_req(c["n_req"]),
                signed(c["E_R"]), num(c["c_R"], 4), signed(c["E_net"]),
                ("n/a" if c["credit_over_width"] is NA
                 else signed(c["credit_over_width"], 4)),
                ("n/a" if c["theta_pd_R"] is NA
                 else signed(c["theta_pd_R"], 5)),
                signed(c["ann_R_net"], 3)])
        show(["DTE", "bucket", "n_avail", "n_req", "E", "c_R", "E_net",
              "cr/W", "theta/day/R", "ann_R_net"], rows)
        pk_t, pk_v = peak_of(S, sid, "E_net")
        note = monotone_note(evals)
        interior = (pk_t not in (NA, TENOR_DAYS[0], TENOR_DAYS[-1]))
        emit("  MONOTONE IN TENOR?  %s.  Peak E_net = %s at DTE %s (%s)."
             % (note, signed(pk_v), pk_t,
                "INTERIOR" if interior else "AT AN ENDPOINT"))
        summary.append([sid, note, pk_t, signed(pk_v),
                        "INTERIOR" if interior else "ENDPOINT",
                        "n/a" if stat_at(S, sid, 7, "credit_over_width") is NA
                        else signed(stat_at(S, sid, 7, "credit_over_width"), 3),
                        "n/a" if stat_at(S, sid, 730, "credit_over_width") is NA
                        else signed(stat_at(S, sid, 730,
                                            "credit_over_width"), 3),
                        signed(stat_at(S, sid, 7, "theta_pd_R"), 5),
                        signed(stat_at(S, sid, 730, "theta_pd_R"), 5)])
    emit("")
    emit("--- the whole grid in one view: E_net by structure x DTE")
    rows = []
    for sid in STRUCT_IDS:
        rows.append([sid] + [signed(stat_at(S, sid, t, "E_net"), 4)
                             for t in TENOR_DAYS])
    show(["E_net"] + TENOR_DAYS, rows)
    emit("--- the same grid at HIGH cost")
    rows = []
    for sid in STRUCT_IDS:
        rows.append([sid] + [signed(stat_at(S, sid, t, "E_net_high"), 4)
                             for t in TENOR_DAYS])
    show(["E_net HIGH"] + TENOR_DAYS, rows)
    emit("--- the same grid at round-trip cost (2 tickets per leg)")
    rows = []
    for sid in STRUCT_IDS:
        rows.append([sid] + [signed(stat_at(S, sid, t, "E_net_rt"), 4)
                             for t in TENOR_DAYS])
    show(["E_net RT"] + TENOR_DAYS, rows)
    emit("")
    show(["id", "monotone in tenor?", "peak DTE", "peak E_net", "where",
          "cr/W @7", "cr/W @730", "theta/day/R @7", "theta/day/R @730"],
         summary)
    write_csv("test1_enet_by_tenor.csv",
              ["sid", "tenor", "bucket", "n_available", "n_req", "E_gross",
               "c_R", "E_net", "E_net_high", "E_net_rt", "credit_over_width",
               "theta_pd_R", "ann_R_net"],
              [[sid, t, TENOR_BUCKET[t], S["BASE"][(sid, t)]["n"],
                S["BASE"][(sid, t)]["n_req"], S["BASE"][(sid, t)]["E_R"],
                S["BASE"][(sid, t)]["c_R"], S["BASE"][(sid, t)]["E_net"],
                S["BASE"][(sid, t)]["E_net_high"],
                S["BASE"][(sid, t)]["E_net_rt"],
                S["BASE"][(sid, t)]["credit_over_width"],
                S["BASE"][(sid, t)]["theta_pd_R"],
                S["BASE"][(sid, t)]["ann_R_net"]]
               for sid in STRUCT_IDS for t in TENOR_DAYS])

    # ============================================================== TEST 2
    banner("4. TEST 2 -- the risk-efficiency curve: theta per day per unit of R")
    emit("")
    emit("The pre-registered hypothesis: SHORT tenor is better paid per day but")
    emit("carries the fatter tail and the worse execution assumption, so E_net")
    emit("peaks at an INTERIOR tenor.  The first half of that is a measurement,")
    emit("the second half is what the tail and cost sections test.")
    emit("")
    emit("theta/day/R = median credit (dollars) / (tenor days x median R).  It")
    emit("is the fraction of the risk budget the position earns (or pays) each")
    emit("calendar day.  Ordered by DTE across the columns.")
    rows = []
    for sid in STRUCT_IDS:
        rows.append([sid] + [signed(stat_at(S, sid, t, "theta_pd_R"), 5)
                             for t in TENOR_DAYS])
    show(["theta/day/R"] + TENOR_DAYS, rows)
    emit("THE SAME NUMBER MULTIPLIED BY sqrt(DTE) -- the test of whether the")
    emit("daily yield really scales as 1/sqrt(T), which is what a fixed-moneyness")
    emit("credit would give.  A FLAT row means 1/sqrt(T) holds; a FALLING row")
    emit("means the yield decays FASTER than 1/sqrt(T), which is what a fixed")
    emit("DOLLAR wing does: the wing is a shrinking fraction of one sigma, so")
    emit("the credit does not keep up with sqrt(T).")
    rows = []
    for sid in STRUCT_IDS:
        r = [sid]
        for t in TENOR_DAYS:
            v = stat_at(S, sid, t, "theta_pd_R")
            r.append("n/a" if v is NA else signed(v * math.sqrt(t), 5))
        rows.append(r)
    show(["theta/day/R x sqrt(DTE)"] + TENOR_DAYS, rows)
    emit("--- and the reason, printed as a column: the wing as a fraction of")
    emit("one standard deviation of the terminal distribution, W/(S sigma sqrt(T))")
    rows = []
    for sid in STRUCT_IDS:
        r = [sid]
        for t in TENOR_DAYS:
            v = stat_at(S, sid, t, "width_over_sigT")
            r.append("n/a" if v is NA else num(v, 4))
        rows.append(r)
    show(["W / sigma*sqrt(T)"] + TENOR_DAYS, rows)
    emit("")
    emit("WHERE THE PEAK ACTUALLY IS:")
    rows = []
    for sid in STRUCT_IDS:
        thr_t, thr_v = peak_of(S, sid, "theta_pd_R")
        en_t, en_v = peak_of(S, sid, "E_net")
        a_t, a_v = peak_of(S, sid, "ann_R_net")
        rows.append([sid, thr_t, signed(thr_v, 5), en_t, signed(en_v),
                     a_t, signed(a_v, 3)])
    show(["id", "peak theta/day/R @DTE", "value", "peak E_net @DTE", "value",
          "peak ann_R_net @DTE", "value"], rows)
    emit("")
    emit("  THE SHAPE OF THIS CURVE IS THE CLEANEST RESULT IN THE STUDY, and it")
    emit("  splits the grid in two:")
    emit("    * the two DEBIT structures (S1 long call, S4 debit spread) have")
    emit("      theta/day/R = -1/D EXACTLY, at every tenor.  That is not a")
    emit("      modelled accident: their credit IS -1 x their R, so the ratio is")
    emit("      the reciprocal of the day count and nothing else.  A fully-debit")
    emit("      position bleeds one day's worth of its own maximum loss per day,")
    emit("      and only the tenor sets how big that is.");
    emit("    * the five CREDIT structures are all monotone DECREASING in tenor,")
    emit("      by 6.8x (S2) to 32.4x (S6) between 7 DTE and 730 DTE.")
    for sid in STRUCT_IDS:
        vals = [(t, stat_at(S, sid, t, "theta_pd_R")) for t in TENOR_DAYS]
        emit("    %-3s  %-28s  ratio @7 / @730 = %s"
             % (sid, monotone_note(vals),
                (lambda a, b: "n/a" if (a is NA or b in (NA, 0.0))
                 else "%.1fx" % (a / b))(stat_at(S, sid, 7, "theta_pd_R"),
                                         stat_at(S, sid, 730, "theta_pd_R"))))
    rho = []
    for sid in STRUCT_IDS:
        rho.append(spearman([t for t in TENOR_DAYS],
                            [stat_at(S, sid, t, "theta_pd_R")
                             for t in TENOR_DAYS]))
    emit("")
    emit("  Spearman(tenor, theta/day/R) per structure: %s"
         % ", ".join("%s=%s" % (sid, ("n/a" if r is NA else "%.2f" % r))
                     for sid, r in zip(STRUCT_IDS, rho)))
    credit_ids = [s for s in STRUCT_IDS if s not in ("S1", "S4")]
    xs, ys = [], []
    for sid in credit_ids:
        for t in TENOR_DAYS:
            xs.append(t)
            ys.append(stat_at(S, sid, t, "theta_pd_R"))
    xs2, ys2 = [], []
    for sid in ("S1", "S4"):
        for t in TENOR_DAYS:
            xs2.append(t)
            ys2.append(stat_at(S, sid, t, "theta_pd_R"))
    emit("  pooled Spearman over the %d CREDIT cells = %s ; over the %d DEBIT"
         % (len(xs), "n/a" if spearman(xs, ys) is NA
            else "%.2f" % spearman(xs, ys), len(xs2)))
    emit("  cells = %s.  A pooled number across both families would be"
         % ("n/a" if spearman(xs2, ys2) is NA else "%.2f" % spearman(xs2, ys2)))
    emit("  meaningless -- the two families have opposite signs -- so it is not")
    emit("  reported as a headline.")
    emit("")
    emit("  A NOTE ON THE W/sigma*sqrt(T) COLUMN: it is the wing as a fraction of")
    emit("  one standard deviation ONLY where W is a WING (the four 5-wide")
    emit("  structures, S3/S4/S6/S7: 1.44 sigma at 7 DTE against 0.15 sigma at")
    emit("  730 DTE).  For S2 and S5 the declared W is the notional (the cash")
    emit("  secured / the stock), so their entry is 1/(sigma sqrt(T)) and is not")
    emit("  comparable with the wing rows.  For S1 there is no W at all.")
    write_csv("test2_risk_efficiency.csv",
              ["sid", "tenor", "theta_pd_R", "theta_pd_R_x_sqrtT",
               "width_over_sigT", "credit_over_width", "R_dollars_med",
               "credit_med"],
              [[sid, t, stat_at(S, sid, t, "theta_pd_R"),
                (lambda v, tt: NA if v is NA else v * math.sqrt(tt))(
                    stat_at(S, sid, t, "theta_pd_R"), t),
                stat_at(S, sid, t, "width_over_sigT"),
                stat_at(S, sid, t, "credit_over_width"),
                stat_at(S, sid, t, "R_dollars_med"),
                stat_at(S, sid, t, "credit_med")]
               for sid in STRUCT_IDS for t in TENOR_DAYS])

    # ============================================================== TEST 3
    banner("5. TEST 3 -- sample adequacy by tenor: is the edge measurable at all?")
    emit("")
    emit("n_req = 4 (sd/|E|)^2 is the number of trades a two-sigma verdict on")
    emit("this cell's own mean needs.  n_available is what the window actually")
    emit("produced.  A cell with n_req > n_available has an E that is")
    emit("INDISTINGUISHABLE FROM ZERO at two sigma and is flagged UNMEASURABLE")
    emit("-- it is reported, but it is not a result.")
    emit("")
    for sid in STRUCT_IDS:
        rows = []
        for t in TENOR_DAYS:
            c = S["BASE"][(sid, t)]
            ok = (c["n_req"] is not NA and c["n_req"] <= c["n"])
            rows.append([t, TENOR_BUCKET[t], c["n_per_index"], c["n"],
                         fmt_n_req(c["n_req"]),
                         "yes" if ok else ("UNMEASURABLE" if
                                           c["n_req"] is not NA else "n/a"),
                         "" if ok else ("" if c["n_req"] is NA else
                                        "%.2fx short" % (c["n"] /
                                                         c["n_req"]))])
        emit("")
        emit("--- %s  %s" % (sid, STRUCT_NAME[sid]))
        show(["DTE", "bucket", "n/index", "n_avail", "n_req", "measurable?",
              "shortfall"], rows)
    tot = len(STRUCT_IDS) * len(TENOR_DAYS)
    bad = 0
    by_bucket = {}
    for sid in STRUCT_IDS:
        for t in TENOR_DAYS:
            c = S["BASE"][(sid, t)]
            b = TENOR_BUCKET[t]
            by_bucket.setdefault(b, [0, 0])
            by_bucket[b][1] += 1
            if c["n_req"] is NA or c["n_req"] > c["n"]:
                bad += 1
                by_bucket[b][0] += 1
    emit("")
    emit("  UNMEASURABLE CELLS: %d of %d (%.0f%%)"
         % (bad, tot, 100.0 * bad / tot))
    rows = []
    for b in ["weeklies", "gamma shoulder", "monthlies", "quarterlies",
              "annuals", "LEAPS"]:
        if b in by_bucket:
            rows.append([b, by_bucket[b][0], by_bucket[b][1],
                         "%.0f%%" % (100.0 * by_bucket[b][0] /
                                     by_bucket[b][1])])
    show(["bucket", "unmeasurable cells", "cells", "share"], rows)
    write_csv("test3_sample_adequacy.csv",
              ["sid", "tenor", "bucket", "n_per_index", "n_available", "n_req",
               "measurable", "sd", "E_gross"],
              [[sid, t, TENOR_BUCKET[t], S["BASE"][(sid, t)]["n_per_index"],
                S["BASE"][(sid, t)]["n"], S["BASE"][(sid, t)]["n_req"],
                (1 if (S["BASE"][(sid, t)]["n_req"] is not NA and
                       S["BASE"][(sid, t)]["n_req"] <=
                       S["BASE"][(sid, t)]["n"]) else 0),
                S["BASE"][(sid, t)]["sd"], S["BASE"][(sid, t)]["E_R"]]
               for sid in STRUCT_IDS for t in TENOR_DAYS])

    # ============================================================== TEST 4
    banner("6. TEST 4 -- cost by tenor, and where cost consumes the edge")
    emit("")
    emit("c_R = cost / R in dollars.  The pre-registered expectation was that")
    emit("credit/width and R move in OPPOSITE directions as tenor extends, so")
    emit("c_R falls with tenor.  Both columns are printed, so the expectation")
    emit("can be checked rather than asserted.")
    emit("")
    emit("--- c_R at the headline LOW cost (one ticket per contract-leg)")
    rows = []
    for sid in STRUCT_IDS:
        rows.append([sid] + [num(stat_at(S, sid, t, "c_R"), 4)
                             for t in TENOR_DAYS])
    show(["c_R"] + TENOR_DAYS, rows)
    emit("--- cost in DOLLARS per trade (flat in tenor by construction -- a")
    emit("ticket costs what it costs -- so any c_R movement is R moving)")
    rows = []
    for sid in STRUCT_IDS:
        rows.append([sid] + [moneyu(stat_at(S, sid, t, "cost_dollars_med"))
                             for t in TENOR_DAYS])
    show(["cost $"] + TENOR_DAYS, rows)
    emit("--- R in DOLLARS per contract (median over the window).  This is the")
    emit("quantity that moves.")
    rows = []
    for sid in STRUCT_IDS:
        rows.append([sid] + [moneyu(stat_at(S, sid, t, "R_dollars_med"))
                             for t in TENOR_DAYS])
    show(["R $"] + TENOR_DAYS, rows)
    emit("--- credit per share, dollars (negative = a net DEBIT)")
    rows = []
    for sid in STRUCT_IDS:
        rows.append([sid] + [signed(stat_at(S, sid, t, "credit_ps_med"), 3)
                             for t in TENOR_DAYS])
    show(["credit $/share"] + TENOR_DAYS, rows)
    emit("--- break-even cost c_R* = E per cell (the cost, in R units, at which")
    emit("the GROSS edge is exactly consumed)")
    rows = []
    for sid in STRUCT_IDS:
        rows.append([sid] + [signed(stat_at(S, sid, t, "c_R_star"), 4)
                             for t in TENOR_DAYS])
    show(["c_R* = E"] + TENOR_DAYS, rows)
    emit("--- the SAME break-even expressed in DOLLARS per trade, against the")
    emit("actual cost column above (c_R* x R$/med)")
    rows = []
    for sid in STRUCT_IDS:
        rows.append([sid] + [moneyu(stat_at(S, sid, t, "c_R_star_dollars"))
                             for t in TENOR_DAYS])
    show(["c_R* $"] + TENOR_DAYS, rows)
    emit("--- c_R / c_R* : > 1 means COST EXCEEDS THE GROSS EDGE in that cell")
    rows = []
    for sid in STRUCT_IDS:
        r = [sid]
        for t in TENOR_DAYS:
            cr = stat_at(S, sid, t, "c_R")
            st = stat_at(S, sid, t, "c_R_star")
            if cr is NA or st in (NA, 0.0):
                r.append("n/a")
            else:
                r.append("%.2f" % (cr / abs(st)))
        rows.append(r)
    show(["c_R / |c_R*|"] + TENOR_DAYS, rows)
    emit("")
    emit("  WHERE COST CONSUMES THE EDGE (c_R > |E|), at LOW cost:")
    hits = []
    for sid in STRUCT_IDS:
        for t in TENOR_DAYS:
            cr = stat_at(S, sid, t, "c_R")
            st = stat_at(S, sid, t, "c_R_star")
            if cr is not NA and st is not NA and cr > abs(st):
                hits.append((sid, t, TENOR_BUCKET[t], cr, st))
    if hits:
        for sid, t, b, cr, st in hits:
            emit("    %-3s DTE %-3d (%-15s): c_R=%.4f  vs  E=%+.4f"
                 % (sid, t, b, cr, st))
    else:
        emit("    NONE.  At LOW cost no cell in this grid has its gross edge")
        emit("    consumed by the ticket cost.")
    emit("")
    emit("  At HIGH cost (double the spread widening):")
    hits = []
    for sid in STRUCT_IDS:
        best = None
        for t in TENOR_DAYS:
            cr = stat_at(S, sid, t, "c_R_high")
            st = stat_at(S, sid, t, "c_R_star")
            if cr is not NA and st is not NA and cr > abs(st):
                hits.append((sid, t))
                if best is None:
                    best = t
        emit("    %-3s  first DTE where cost exceeds the gross edge: %s"
             % (sid, ("none" if best is None else str(best))))
    emit("  At round-trip cost (2 tickets per contract-leg):")
    for sid in STRUCT_IDS:
        best = None
        for t in TENOR_DAYS:
            cr = stat_at(S, sid, t, "c_R_rt")
            st = stat_at(S, sid, t, "c_R_star")
            if cr is not NA and st is not NA and cr > abs(st):
                if best is None:
                    best = t
        emit("    %-3s  first DTE where cost exceeds the gross edge: %s"
             % (sid, ("none" if best is None else str(best))))
    emit("")
    emit("  MONOTONE IN TENOR?")
    for field, label in (("c_R", "c_R (LOW)"), ("credit_over_width", "cr/W"),
                         ("R_dollars_med", "R $"),
                         ("width_over_sigT", "W/sigma sqrt(T)")):
        line = []
        for sid in STRUCT_IDS:
            if field == "width_over_sigT" and sid == "S1":
                line.append("%s=n/a" % sid)
                continue
            vals = [(t, stat_at(S, sid, t, field)) for t in TENOR_DAYS]
            line.append("%s=%s" % (sid, monotone_note(vals).split(" (")[0]))
        emit("    %-16s %s" % (label, "  ".join(line)))
    emit("")
    emit("  HOW TO READ THAT TABLE.  The grid splits cleanly, and the split is")
    emit("  NOT the one the brief anticipated:")
    emit("    * for the four 5-WIDE structures (S3, S4, S6, S7) the credit RISES")
    emit("      with tenor as a fraction of the width (S3: 0.055 -> 0.211; S6:")
    emit("      0.119 -> 0.303) while R = width - credit FALLS (S3: $472 -> $394;")
    emit("      S6: $441 -> $349).  The brief's mechanism -- credit/width and R")
    emit("      moving in OPPOSITE directions -- is CONFIRMED.  Its implied")
    emit("      conclusion is CONTRADICTED: c_R RISES with tenor (S3: 0.0136 ->")
    emit("      0.0163; S6: 0.0294 -> 0.0379), because the credit grows faster")
    emit("      than R shrinks.  The mechanism is the fixed-dollar wing: at 7 DTE")
    emit("      a $5 wing is 1.44 sigma of the terminal distribution and sits far")
    emit("      out in the tail where density is low; at 730 DTE it is 0.15 sigma")
    emit("      and sits near the money where density is high, so the same $5")
    emit("      captures far more premium per dollar of width.");
    emit("    * for the structures whose R is NOT a wing and DOES scale with the")
    emit("      index and with sqrt(T) -- S1 and S4 (R = the debit) and weakly S2")
    emit("      and S5 (R = the cash secured / the notional) -- c_R FALLS with")
    emit("      tenor, by up to 8.5x (S4: 0.0877 -> 0.0140; S1: 0.0276 ->")
    emit("      0.0034), because the ticket cost is a constant $3.15-$6.30 while")
    emit("      R grows.");
    emit("  Cost is NOT flat in tenor.  It rises for the width-defined structures")
    emit("  and falls for the index-scaled ones, and the reason is the same in")
    emit("  both cases: cost is a fixed dollar amount and R is not.")
    write_csv("test4_cost_by_tenor.csv",
              ["sid", "tenor", "cost_dollars_med", "R_dollars_med", "c_R",
               "c_R_high", "c_R_rt", "c_R_star", "c_R_star_dollars",
               "credit_ps_med", "credit_over_width", "credit_over_notional",
               "R_over_notional", "width_over_sigT"],
              [[sid, t, stat_at(S, sid, t, "cost_dollars_med"),
                stat_at(S, sid, t, "R_dollars_med"),
                stat_at(S, sid, t, "c_R"), stat_at(S, sid, t, "c_R_high"),
                stat_at(S, sid, t, "c_R_rt"), stat_at(S, sid, t, "c_R_star"),
                stat_at(S, sid, t, "c_R_star_dollars"),
                stat_at(S, sid, t, "credit_ps_med"),
                stat_at(S, sid, t, "credit_over_width"),
                stat_at(S, sid, t, "credit_over_notional"),
                stat_at(S, sid, t, "R_over_notional"),
                stat_at(S, sid, t, "width_over_sigT")]
               for sid in STRUCT_IDS for t in TENOR_DAYS])

    # ============================================================== TEST 5
    banner("7. TEST 5 -- skew sensitivity by tenor (SOLD strikes +-1.5 vol points)")
    emit("")
    emit("Strikes are HELD FIXED; only the pricing vol of the SOLD legs moves.")
    emit("dE is the change in the GROSS E_R; and both directions are reported")
    emit("because the model cannot say which is right -- the sibling studies")
    emit("established that, and this study does not contradict it.  dDD is the")
    emit("change in the fixed-budget drawdown (R units, negative = worse).")
    emit("")
    emit("--- dE (R units): SOLD +1.5 vol points minus BASE.  The seller")
    emit("collects MORE in this direction.")
    rows = []
    for sid in STRUCT_IDS:
        r = [sid]
        for t in TENOR_DAYS:
            a = stat_at(S, sid, t, "E_R")
            b = stat_at(S, sid, t, "E_R", "SKEW_SOLD_P15")
            r.append(signed(b - a, 4) if (a is not NA and b is not NA)
                     else "n/a")
        rows.append(r)
    show(["dE (+1.5)"] + TENOR_DAYS, rows)
    emit("--- dE (R units): SOLD -1.5 vol points minus BASE.  The conservative")
    emit("direction -- a real seller of an OTM option collects LESS than the")
    emit("flat-vol value.")
    rows = []
    for sid in STRUCT_IDS:
        r = [sid]
        for t in TENOR_DAYS:
            a = stat_at(S, sid, t, "E_R")
            b = stat_at(S, sid, t, "E_R", "SKEW_SOLD_M15")
            r.append(signed(b - a, 4) if (a is not NA and b is not NA)
                     else "n/a")
        rows.append(r)
    show(["dE (-1.5)"] + TENOR_DAYS, rows)
    emit("--- dDD (R units): fixed-budget worst drawdown, BASE -> SOLD -1.5")
    rows = []
    for sid in STRUCT_IDS:
        r = [sid]
        for t in TENOR_DAYS:
            a = stat_at(S, sid, t, "dd_R")
            b = stat_at(S, sid, t, "dd_R", "SKEW_SOLD_M15")
            r.append(signed(b - a, 2) if (a is not NA and b is not NA)
                     else "n/a")
        rows.append(r)
    show(["dDD (-1.5)"] + TENOR_DAYS, rows)
    emit("--- E_net under the conservative direction (E from SOLD -1.5, cost at")
    emit("the same headline LOW setting)")
    rows = []
    for sid in STRUCT_IDS:
        r = [sid]
        for t in TENOR_DAYS:
            a = stat_at(S, sid, t, "E_net", "SKEW_SOLD_M15")
            r.append(signed(a, 4))
        rows.append(r)
    show(["E_net (-1.5)"] + TENOR_DAYS, rows)
    emit("")
    emit("  THE BAND OF MODEL AMBIGUITY, in E_net units (SOLD +1.5 minus SOLD")
    emit("  -1.5).  This is how much of the answer lives INSIDE the skew the")
    emit("  model cannot see:")
    rows = []
    for sid in STRUCT_IDS:
        r = [sid]
        for t in TENOR_DAYS:
            a = stat_at(S, sid, t, "E_net", "SKEW_SOLD_P15")
            b = stat_at(S, sid, t, "E_net", "SKEW_SOLD_M15")
            r.append(signed(a - b, 4) if (a is not NA and b is not NA)
                     else "n/a")
        rows.append(r)
    show(["E_net band (P15 - M15)"] + TENOR_DAYS, rows)
    emit("")
    emit("  DOES SKEW SENSITIVITY RISE WITH TENOR?  |dE| in R against DTE,")
    emit("  pooled over every structure x tenor cell:")
    xs, y1, y2, y3 = [], [], [], []
    for sid in STRUCT_IDS:
        for t in TENOR_DAYS:
            a = stat_at(S, sid, t, "E_R")
            p = stat_at(S, sid, t, "E_R", "SKEW_SOLD_P15")
            m = stat_at(S, sid, t, "E_R", "SKEW_SOLD_M15")
            if a is NA or p is NA or m is NA:
                continue
            xs.append(t)
            y1.append(abs(p - a))
            y2.append(abs(m - a))
            y3.append(max(abs(p - a), abs(m - a)))
    emit("    Pearson(DTE, |dE| +1.5) = %s"
         % ("n/a" if pearson(xs, y1) is NA else "%.3f" % pearson(xs, y1)))
    emit("    Pearson(DTE, |dE| -1.5) = %s"
         % ("n/a" if pearson(xs, y2) is NA else "%.3f" % pearson(xs, y2)))
    emit("    Spearman(DTE, max|dE|)   = %s"
         % ("n/a" if spearman(xs, y3) is NA else "%.3f" % spearman(xs, y3)))
    emit("")
    emit("  Mean max|dE| by bucket (R units), which is the readable form:")
    byb = {}
    for sid in STRUCT_IDS:
        for t in TENOR_DAYS:
            a = stat_at(S, sid, t, "E_R")
            p = stat_at(S, sid, t, "E_R", "SKEW_SOLD_P15")
            m = stat_at(S, sid, t, "E_R", "SKEW_SOLD_M15")
            if a is NA or p is NA or m is NA:
                continue
            byb.setdefault(TENOR_BUCKET[t], []).append(
                max(abs(p - a), abs(m - a)))
    rows = []
    for b in ["weeklies", "gamma shoulder", "monthlies", "quarterlies",
              "annuals", "LEAPS"]:
        if b in byb:
            rows.append([b, num(mean(byb[b]), 4),
                         num(max(byb[b]), 4), len(byb[b])])
    show(["bucket", "mean max|dE|", "max max|dE|", "cells"], rows)
    write_csv("test5_skew_by_tenor.csv",
              ["sid", "tenor", "E_base", "E_p15", "E_m15", "dE_p15", "dE_m15",
               "dd_base", "dd_m15", "dd_p15", "E_net_base", "E_net_m15",
               "E_net_p15"],
              [[sid, t, stat_at(S, sid, t, "E_R"),
                stat_at(S, sid, t, "E_R", "SKEW_SOLD_P15"),
                stat_at(S, sid, t, "E_R", "SKEW_SOLD_M15"),
                (lambda a, b: NA if (a is NA or b is NA) else b - a)(
                    stat_at(S, sid, t, "E_R"),
                    stat_at(S, sid, t, "E_R", "SKEW_SOLD_P15")),
                (lambda a, b: NA if (a is NA or b is NA) else b - a)(
                    stat_at(S, sid, t, "E_R"),
                    stat_at(S, sid, t, "E_R", "SKEW_SOLD_M15")),
                stat_at(S, sid, t, "dd_R"),
                stat_at(S, sid, t, "dd_R", "SKEW_SOLD_M15"),
                stat_at(S, sid, t, "dd_R", "SKEW_SOLD_P15"),
                stat_at(S, sid, t, "E_net"),
                stat_at(S, sid, t, "E_net", "SKEW_SOLD_M15"),
                stat_at(S, sid, t, "E_net", "SKEW_SOLD_P15")]
               for sid in STRUCT_IDS for t in TENOR_DAYS])

    # ============================================================== TEST 6
    banner("8. TEST 6 -- the tail by tenor")
    emit("")
    emit("Did a longer tenor buy tail protection?  All figures in R units,")
    emit("comparable across structures because R is the structure's own maximum")
    emit("loss.  WorstM / WorstY are the SUM of fixed-budget returns inside the")
    emit("period.  2008 / 2020 / 2022 are the total return in R over the")
    emit("pre-registered stress windows.")
    emit("")
    emit("READ THE 'worst trade' COLUMN CAREFULLY: for every defined-risk")
    emit("structure it is the STRUCTURAL MAXIMUM LOSS, i.e. exactly -1.000R at")
    emit("every tenor, because a 7-DTE move and a 730-DTE move both eventually")
    emit("cross a 5-wide wing.  It is a statement about the structure, not about")
    emit("the tenor.  The columns that DO move are '% at -1R' (how often the tail")
    emit("is actually realised) and '5th pct' (the ordinary bad trade).")
    for sid in STRUCT_IDS:
        emit("")
        emit("--- %s  %s" % (sid, STRUCT_NAME[sid]))
        rows = []
        for t in TENOR_DAYS:
            c = S["BASE"][(sid, t)]
            br = res["BASE"][(sid, t)]["book_rets"]
            st = []
            for _lbl, d0, d1 in STRESS_WINDOWS:
                v, dd = window_stat(window_dates, br, d0, d1)
                st.append(v)
            rows.append([t, TENOR_BUCKET[t], signed(c["worst_trade"], 3),
                         pctu(c["frac_at_max"], 1), signed(c["p05"], 3),
                         signed(c["p25"], 3), signed(c["dd_R"], 2),
                         signed(c["worst_month"], 3),
                         signed(c["worst_year"], 3),
                         (c["worst_year_key"] or "n/a"),
                         signed(st[0], 2), signed(st[1], 2),
                         signed(st[2], 2)])
        show(["DTE", "bucket", "worst trade", "% at -1R", "5th pct", "25th pct",
              "dd (R)", "worst M", "worst Y", "worst Y year", "2008", "2020",
              "2022"], rows)
    emit("")
    emit("  WORST TRADE and 2008, ordered by DTE -- the tail question in two")
    emit("  columns:")
    rows = []
    for sid in STRUCT_IDS:
        r = [sid]
        for t in TENOR_DAYS:
            v = stat_at(S, sid, t, "worst_trade")
            r.append(signed(v, 2))
        rows.append([sid] + [x for x in r[1:]])
    show(["worst single trade (R)"] + TENOR_DAYS, rows)
    rows = []
    for sid in STRUCT_IDS:
        r = [sid]
        for t in TENOR_DAYS:
            br = res["BASE"][(sid, t)]["book_rets"]
            v, dd = window_stat(window_dates, br, *STRESS_WINDOWS[0][1:])
            r.append(signed(v, 2))
        rows.append(r)
    show(["2008 GFC total (R)"] + TENOR_DAYS, rows)
    rows = []
    for sid in STRUCT_IDS:
        r = [sid]
        for t in TENOR_DAYS:
            br = res["BASE"][(sid, t)]["book_rets"]
            v, dd = window_stat(window_dates, br, *STRESS_WINDOWS[1][1:])
            r.append(signed(v, 2))
        rows.append(r)
    show(["2020 COVID total (R)"] + TENOR_DAYS, rows)
    emit("")
    emit("  Does the WORST TRADE get shallower as tenor extends?  (A tail that")
    emit("  is genuinely bought by time must show |worst trade| falling.)")
    for sid in STRUCT_IDS:
        xs = TENOR_DAYS
        ys = [abs(stat_at(S, sid, t, "worst_trade"))
              for t in TENOR_DAYS]
        emit("    %-3s  Spearman(DTE, |worst trade|) = %s ; @7=%s  @730=%s"
             % (sid,
                "n/a" if spearman(xs, ys) is NA else "%.2f" % spearman(xs, ys),
                signed(stat_at(S, sid, 7, "worst_trade"), 2),
                signed(stat_at(S, sid, 730, "worst_trade"), 2)))
    write_csv("test6_tail_by_tenor.csv",
              ["sid", "tenor", "worst_trade", "worst1", "dd_R", "worst_month",
               "worst_month_key", "worst_year", "worst_year_key", "best_year",
               "s2008", "s2020", "s2022"],
              [[sid, t, stat_at(S, sid, t, "worst_trade"),
                stat_at(S, sid, t, "worst1"), stat_at(S, sid, t, "dd_R"),
                stat_at(S, sid, t, "worst_month"),
                stat_at(S, sid, t, "worst_month_key"),
                stat_at(S, sid, t, "worst_year"),
                stat_at(S, sid, t, "worst_year_key"),
                stat_at(S, sid, t, "best_year")]
               + [window_stat(window_dates,
                              res["BASE"][(sid, t)]["book_rets"], d0, d1)[0]
                  for _l, d0, d1 in STRESS_WINDOWS]
               for sid in STRUCT_IDS for t in TENOR_DAYS])

    # ============================================================== TEST 7
    banner("9. TEST 7 -- positivity by tenor and horizon (M / Q / Y)")
    emit("")
    emit("`law` is the normal null Phi(Sharpe_annual x sqrt(period in years)).")
    emit("A POSITIVE gap (law - observed) is the signature of negative skew: the")
    emit("normal law says the horizon should be positive more often than it is.")
    emit("The sibling study found premium selling at 89% of months against 79%")
    emit("of years -- the INVERTED order.  The question here is whether TENOR")
    emit("changes that inversion.")
    emit("")
    for sid in STRUCT_IDS:
        emit("")
        emit("--- %s  %s" % (sid, STRUCT_NAME[sid]))
        rows = []
        for t in TENOR_DAYS:
            c = S["BASE"][(sid, t)]
            rows.append([t, TENOR_BUCKET[t],
                         pctu(c["pos_M"], 1), pctu(c["pos_M_law"], 1),
                         signed(c["pos_M_gap"], 3),
                         pctu(c["pos_Q"], 1), pctu(c["pos_Q_law"], 1),
                         signed(c["pos_Q_gap"], 3),
                         pctu(c["pos_Y"], 1), pctu(c["pos_Y_law"], 1),
                         signed(c["pos_Y_gap"], 3),
                         num(c["sharpe"], 2),
                         "INVERTED" if c["inverted_MY"] else ""])
        show(["DTE", "bucket", "M", "M_law", "M_gap", "Q", "Q_law", "Q_gap",
              "Y", "Y_law", "Y_gap", "Sharpe", "M>Y?"], rows)
    emit("")
    emit("  THE INVERSION COUNTED BY BUCKET -- cells where monthly positivity")
    emit("  exceeds yearly positivity:")
    cnt = {}
    for sid in STRUCT_IDS:
        for t in TENOR_DAYS:
            c = S["BASE"][(sid, t)]
            b = TENOR_BUCKET[t]
            cnt.setdefault(b, [0, 0, 0.0, 0.0])
            cnt[b][1] += 1
            if c["inverted_MY"]:
                cnt[b][0] += 1
            if c["pos_M"] is not NA and c["pos_Y"] is not NA:
                cnt[b][2] += c["pos_M"]
                cnt[b][3] += c["pos_Y"]
    rows = []
    for b in ["weeklies", "gamma shoulder", "monthlies", "quarterlies",
              "annuals", "LEAPS"]:
        if b in cnt:
            k, n, sm, sy = cnt[b]
            rows.append([b, k, n, "%.1f%%" % (100.0 * sm / n),
                         "%.1f%%" % (100.0 * sy / n),
                         "%+.1f pp" % (100.0 * (sm - sy) / n)])
    show(["bucket", "inverted cells", "cells", "mean M", "mean Y",
          "mean M - Y"], rows)
    emit("")
    emit("  Mean yearly gap (law - observed) by bucket -- how far from the")
    emit("  normal law each tenor's yearly positivity sits:")
    rows = []
    for b in ["weeklies", "gamma shoulder", "monthlies", "quarterlies",
              "annuals", "LEAPS"]:
        if b in cnt:
            vals = []
            mvals = []
            for sid in STRUCT_IDS:
                for t in TENOR_DAYS:
                    if TENOR_BUCKET[t] != b:
                        continue
                    c = S["BASE"][(sid, t)]
                    if c["pos_Y_gap"] is not NA:
                        vals.append(c["pos_Y_gap"])
                    if c["pos_M_gap"] is not NA:
                        mvals.append(c["pos_M_gap"])
            if vals:
                rows.append([b, num(mean(mvals), 4), num(mean(vals), 4)])
    show(["bucket", "mean M gap", "mean Y gap"], rows)
    write_csv("test7_positivity.csv",
              ["sid", "tenor", "sharpe", "pos_M", "pos_M_law", "pos_M_gap",
               "pos_Q", "pos_Q_law", "pos_Q_gap", "pos_Y", "pos_Y_law",
               "pos_Y_gap", "inverted_MY"],
              [[sid, t, S["BASE"][(sid, t)]["sharpe"],
                S["BASE"][(sid, t)]["pos_M"], S["BASE"][(sid, t)]["pos_M_law"],
                S["BASE"][(sid, t)]["pos_M_gap"], S["BASE"][(sid, t)]["pos_Q"],
                S["BASE"][(sid, t)]["pos_Q_law"], S["BASE"][(sid, t)]["pos_Q_gap"],
                S["BASE"][(sid, t)]["pos_Y"], S["BASE"][(sid, t)]["pos_Y_law"],
                S["BASE"][(sid, t)]["pos_Y_gap"],
                1 if S["BASE"][(sid, t)]["inverted_MY"] else 0]
               for sid in STRUCT_IDS for t in TENOR_DAYS])

    # ============================================================== TEST 8
    banner("10. TEST 8 -- the verdict: which tenor, for which structure")
    emit("")
    emit("edge_per_tail = E_net / |mean of the worst 1% of trades (R)|, the")
    emit("pre-registered selection metric -- expectancy per unit of realised")
    emit("tail.  The highest-E_net tenor is named separately, because the two")
    emit("rules can disagree and the reader should see when they do.")
    emit("")
    rows = []
    details = []
    for sid in STRUCT_IDS:
        best_t, best_v = NA, NA
        for t in TENOR_DAYS:
            en = stat_at(S, sid, t, "E_net")
            w1 = stat_at(S, sid, t, "worst1")
            if en is NA or w1 in (NA, 0.0):
                continue
            v = en / abs(w1)
            if best_v is NA or v > best_v:
                best_t, best_v = t, v
        en_t, en_v = peak_of(S, sid, "E_net")
        rows.append([sid, best_t, signed(best_v, 4),
                     signed(stat_at(S, sid, best_t, "E_net")),
                     signed(stat_at(S, sid, best_t, "worst1"), 3),
                     signed(stat_at(S, sid, best_t, "dd_R"), 2),
                     en_t, signed(en_v),
                     signed(stat_at(S, sid, best_t, "ann_R_net"), 3),
                     stat_at(S, sid, best_t, "n")])
        details.append((sid, best_t, best_v))
    show(["id", "best DTE by edge/tail", "edge/tail", "E_net", "worst 1%",
          "dd (R)", "best DTE by E_net", "E_net", "ann_R_net", "n_avail"],
         rows)
    emit("")
    emit("  The same ranking restricted to cells whose edge is MEASURABLE")
    emit("  (n_req <= n_available), so a verdict is never awarded to a cell the")
    emit("  window cannot resolve:")
    rows = []
    for sid in STRUCT_IDS:
        best_t, best_v = NA, NA
        for t in TENOR_DAYS:
            c = S["BASE"][(sid, t)]
            if c["n_req"] is NA or c["n_req"] > c["n"]:
                continue
            en, w1 = c["E_net"], c["worst1"]
            if en is NA or w1 in (NA, 0.0):
                continue
            v = en / abs(w1)
            if best_v is NA or v > best_v:
                best_t, best_v = t, v
        r = [sid, "none" if best_t is NA else best_t,
             signed(best_v, 4),
             signed(stat_at(S, sid, best_t, "E_net")) if best_t is not NA
             else "n/a",
             signed(stat_at(S, sid, best_t, "ann_R_net")) if best_t is not NA
             else "n/a"]
        nmeas = sum(1 for t in TENOR_DAYS
                    if S["BASE"][(sid, t)]["n_req"] is not NA and
                    S["BASE"][(sid, t)]["n_req"] <= S["BASE"][(sid, t)]["n"])
        r.append(nmeas)
        rows.append(r)
    show(["id", "best measurable DTE", "edge/tail", "E_net", "ann_R_net",
          "measurable tenors"], rows)
    write_csv("test8_verdict.csv",
              ["sid", "tenor", "E_net", "worst1", "edge_per_tail", "dd_R",
               "ann_R_net", "n_available", "n_req", "measurable"],
              [[sid, t, S["BASE"][(sid, t)]["E_net"],
                S["BASE"][(sid, t)]["worst1"],
                (lambda e, w: NA if (e is NA or w in (NA, 0.0))
                 else e / abs(w))(S["BASE"][(sid, t)]["E_net"],
                                  S["BASE"][(sid, t)]["worst1"]),
                S["BASE"][(sid, t)]["dd_R"],
                S["BASE"][(sid, t)]["ann_R_net"],
                S["BASE"][(sid, t)]["n"], S["BASE"][(sid, t)]["n_req"],
                (1 if (S["BASE"][(sid, t)]["n_req"] is not NA and
                       S["BASE"][(sid, t)]["n_req"] <=
                       S["BASE"][(sid, t)]["n"]) else 0)]
               for sid in STRUCT_IDS for t in TENOR_DAYS])

    # ============================================================== TEST 9
    banner("11. TEST 9 -- reconciliation with `options-risk-engineer`'s calendar")
    emit("")
    emit("The owning skill's partition and force, quoted from its own files")
    emit("(`SKILL.md` Phase 8 / DT6 and `references/dte-close-roll-calendar.md`")
    emit("section 2).  Its bucket boundaries are the boundaries used above,")
    emit("verbatim:")
    emit("  0DTE (same session) . weeklies 1-7 . gamma shoulder 8-20 .")
    emit("  monthlies 21-60 . quarterlies 60-120 . annuals 121-365 . LEAPS >365")
    emit("")
    rows = [
        ["weeklies", "1-7", "close at 50% of max profit or 3 DTE",
         "T-7 -> T-5", "T-0 15:00 ET"],
        ["gamma shoulder", "8-20", "hold; resting orders at 50% of max profit",
         "14-21", "7 DTE"],
        ["monthlies", "21-60", "roll expiring monthlies into the next monthly",
         "21-30", "21 short premium / 7 defined-risk"],
        ["quarterlies", "60-120", "hold; harvest 50-75%", "60-75", "45 DTE"],
        ["annuals", "121-365", "hold; manage by delta and vega, not theta",
         "120-150", "90 DTE"],
        ["LEAPS", ">365", "hold as a capital-efficient stock substitute",
         "120-90", "60 DTE"],
    ]
    show(["bucket", "DTE zone", "default action window", "roll window",
          "hard deadline"], rows)
    emit("")
    emit("WHAT THIS STUDY CAN AND CANNOT SAY ABOUT IT.  It is important to be")
    emit("precise here: this study ENTERS at a DTE and HOLDS TO EXPIRY, with no")
    emit("stop, no target and no roll.  It therefore cannot test any rule whose")
    emit("content is an EXIT trigger or a roll window.  It can test the")
    emit("QUANTITATIVE claims the calendar's boundaries rest on.")
    emit("")
    rows = [
        ["0DTE: close by 14:45 ET, hard stop 15:00 ET",
         "CANNOT TEST",
         "daily bars have no intraday path; the close is the only 0DTE moment "
         "this data sees"],
        ["weeklies: close at 50% of max profit or 3 DTE",
         "CANNOT TEST",
         "there is no profit target in this design -- every trade runs to "
         "expiry, so the 3-DTE exit is never taken"],
        ["weeklies: 'theta is large but no longer compensates the gamma you "
         "accept'",
         "SUPPORTS (direction)", "theta/day/R is highest at 7 DTE by a wide "
         "margin in every structure (Test 2)"],
        ["gamma shoulder 8-20: 'hold; add no new credit'",
         "CANNOT TEST", "a hold/no-add instruction is a portfolio rule, not a "
         "payoff"],
        ["monthlies 21-60: 'the open and scale zone'",
         "TESTABLE -- see below", "the 30/45-DTE cells are the un-managed "
         "counterpart of that claim"],
        ["quarterlies 60-120: 'vega is the only live Greek of size'",
         "SUPPORTS (direction)", "the modelled entry vega is the largest "
         "relative to R in this band for the credit structures"],
        ["quarterlies: 'this bucket has no other owner'",
         "NO EVIDENCE EITHER WAY", "an ownership convention is not a "
         "measurable claim"],
        ["annuals 121-365: 'manage by delta and vega, not theta'",
         "SUPPORTS (direction)", "theta/day/R at 180-365 DTE is 1-2 orders of "
         "magnitude below the weeklies band"],
        ["LEAPS >365: 'capital-efficient stock substitute'",
         "SUPPORTS (direction), with a cost caveat", "the 730-DTE long call's "
         "R is a fraction of the underlying notional; but its c_R and its "
         "E_net are measured below"],
        ["Gamma_ATM ~ 1/sqrt(T); 45 DTE -> 21/11/6/3 double-ladder",
         "SUPPORTS (analytically)", "verifiable directly against this study's "
         "own pricer -- see section 12"],
        ["roll windows and hard deadlines as FORCING DATES",
         "CANNOT TEST", "untested evidence: the study never rolls, never "
         "closes early, and never observes a broker's margin or assignment "
         "behaviour"],
    ]
    show(["claim in the owning skill", "verdict", "why"], rows)
    emit("")
    emit("  WHICH CLAIMS REMAIN UNTESTED EVIDENCE, stated plainly: every roll")
    emit("  window (T-7->T-5, 14-21, 21-30, 60-75, 120-150, 120-90); every hard")
    emit("  deadline (T-0 15:00, 7, 21, 45, 90, 60); the 0DTE 14:45/15:00")
    emit("  clock; the expiry-week T-5..T+1 rungs; the 'two rolls per cycle'")
    emit("  cap; the 'credit-or-flat' roll rule (owned by")
    emit("  `options-position-lifecycle`); and every assignment, ex-dividend")
    emit("  and pin-risk consequence of holding an American short option,")
    emit("  because this model is European, cash-settled and dividend-free.")
    emit("")
    emit("  THE ONE THING THIS STUDY ADDS TO THAT CALENDAR, and it is a")
    emit("  boundary finding rather than a rule finding: the skill's own labels")
    emit("  overlap at 60 DTE (monthlies 21-60 / quarterlies 60-120) and abut at")
    emit("  365 DTE.  A position at exactly 60 DTE therefore resolves to two")
    emit("  different buckets under the skill's own two tables, and the two")
    emit("  buckets carry different hard deadlines (21 DTE vs 45 DTE) and")
    emit("  different roll windows (21-30 vs 60-75).  This is a real ambiguity")
    emit("  in the owning skill, not in this study; section 1 declares the")
    emit("  assignment used here (60 -> quarterlies).")

    # ======================================================= 0DTE ANALYTIC
    banner("12. THE 0DTE QUESTION -- ANALYTIC, NOT BACKTESTED")
    emit("")
    emit("NO multi-year 0DTE backtest is reported from these bars, and none")
    emit("should be believed from daily bars: 0DTE P&L is decided by the")
    emit("INTRADAY PATH, and a daily open/high/low/close cannot see it.  What")
    emit("CAN be derived exactly is the scaling.")
    emit("")
    t_short = ODTE_T_SHORT / 365.0
    t_long = ODTE_T_LONG / 365.0
    S0 = 100.0
    sig = ODTE_SIGMA
    r0 = 0.0                                  # stated: the reduced form needs r=0
    d1, g1, v1, th1 = bs_greeks(S0, S0, t_long, r0, sig, "C")
    d2, g2, v2, th2 = bs_greeks(S0, S0, t_short, r0, sig, "C")
    p1 = bs_price(S0, S0, t_long, r0, sig, "C")
    p2 = bs_price(S0, S0, t_short, r0, sig, "C")
    ratio_g = g2 / g1
    ratio_th = abs(th2) / abs(th1)
    emit("Stated inputs for the analytic block only: S = K = %.0f (at the "
         "money), sigma = %.0f%%, r = q = 0 (the reduced form the owning skill "
         "derives its ladder from).  T_long = %.0f days, T_short = %s days."
         % (S0, sig * 100.0, ODTE_T_LONG, num(ODTE_T_SHORT, 2)))
    emit("")
    rows = [
        ["gamma (dDelta per $1)",
         num(g1, 6), num(g2, 6), "%.3fx" % ratio_g, "sqrt(30/0.25) = %.3f"
         % math.sqrt(ODTE_T_LONG / ODTE_T_SHORT)],
        ["|theta| per DAY ($)",
         num(abs(th1), 6), num(abs(th2), 6), "%.3fx" % ratio_th, "same 1/sqrt(T)"],
        ["ATM option value ($)",
         num(p1, 4), num(p2, 4), "%.3fx" % (p2 / p1), "1/sqrt(T) the other way"],
        ["|theta| per day / value",
         num(abs(th1) / p1, 6), num(abs(th2) / p2, 6),
         "%.3fx" % ((abs(th2) / p2) / (abs(th1) / p1)),
         "T_long/T_short = %.1f" % (ODTE_T_LONG / ODTE_T_SHORT)],
    ]
    show(["quantity", "30 DTE", "0.25 DTE", "ratio", "derived expectation"],
         rows)
    emit("")
    emit("  [COMPUTED]  Gamma_ATM ~ 1/sqrt(T), so moving from 30 DTE to 0.25 DTE")
    emit("  multiplies the ATM gamma by sqrt(%g/%g) = %.3f.  The model returns"
         % (ODTE_T_LONG, ODTE_T_SHORT, math.sqrt(ODTE_T_LONG / ODTE_T_SHORT)))
    emit("  %.3f -- an exact match, because the pricer IS Black-Scholes."
         % ratio_g)
    emit("  [COMPUTED]  |theta| per day carries the same 1/sqrt(T), so the same")
    emit("  %.3f multiplies the DAILY DECAY IN DOLLARS.  But the position's VALUE"
         % ratio_th)
    emit("  falls by the same factor, so the daily decay as a FRACTION OF THE")
    emit("  PREMIUM scales as 1/T: %.1fx, i.e. %s%% per day at 30 DTE against"
         % (ODTE_T_LONG / ODTE_T_SHORT,
            num(100.0 * abs(th1) / p1, 3)))
    emit("  %s%% per day at 0.25 DTE.  A 0.25-DTE option that is worth anything"
         % num(100.0 * abs(th2) / p2, 1))
    emit("  at all is worth it for hours, not days.  That is the honest 0DTE")
    emit("  statement: it is not 'more theta', it is 'the same theta in a tenth")
    emit("  of the time, at ten times the gamma'.")
    emit("")
    emit("  [COMPUTED]  The same identity fixes the shape of the risk: one 1% move"
         " in the underlying")
    emit("  changes the position's delta by %.2f at 0.25 DTE against %.2f at"
         % (g2 * S0 * 0.01, g1 * S0 * 0.01))
    emit("  30 DTE -- the same move re-writes ten times as much of the hedge at")
    emit("  0.25 DTE.  A delta band that is wide enough at 30 DTE is crossed by")
    emit("  an ordinary morning move at 0.25 DTE.")
    emit("")
    emit("THE COST-PER-TICKET ARITHMETIC AGAINST A SMALL CREDIT.  A 0DTE ticket")
    emit("is the same ticket as any other -- the fee does not shrink with the")
    emit("credit.  At the headline LOW setting a 2-leg ticket costs")
    emit("2 x ($0.65 + $0.025 x 100) = $%.2f, and a sub-$0.20 credit is the"
         % (2 * (ODTE_FEE + ODTE_HALF_SPREAD * 100.0)))
    emit("regime a 0DTE trader is actually in whenever the strikes are far enough")
    emit("out to have any room:")
    emit("")
    rows = []
    for credit in (ODTE_CREDIT_LO, 0.10, ODTE_CREDIT_HI):
        for wing in (ODTE_WING_LO, ODTE_WING_HI):
            cost = 2 * (ODTE_FEE + ODTE_HALF_SPREAD * 100.0)
            r_ps = wing - credit
            cR = cost / (r_ps * 100.0)
            costhi = 2 * (ODTE_FEE + 0.050 * 100.0)
            rows.append(["%.2f" % credit, "%.2f" % wing, "%.2f" % (credit * 100),
                         "%.0f" % (r_ps * 100.0), "%.2f" % cost,
                         "%.1f%%" % (100.0 * cost / (credit * 100.0)),
                         num(cR, 4), num(costhi / (r_ps * 100.0), 4)])
    show(["credit $/sh", "wing $", "credit $", "R $", "cost $ LOW",
          "cost / credit", "c_R LOW", "c_R HIGH"], rows)
    emit("")
    emit("  [COMPUTED]  Read the 'cost / credit' column: on a $0.05 credit the")
    emit("  round-trip ticket is %.0f%% of the ENTIRE premium at LOW prices and"
         % (100.0 * 2 * (ODTE_FEE + ODTE_HALF_SPREAD * 100.0) / 5.0))
    emit("  %.0f%% at HIGH prices.  On a $0.20 credit it is %.0f%% / %.0f%%."
         % (100.0 * 2 * (ODTE_FEE + 0.050 * 100.0) / 5.0,
            100.0 * 2 * (ODTE_FEE + ODTE_HALF_SPREAD * 100.0) / 20.0,
            100.0 * 2 * (ODTE_FEE + 0.050 * 100.0) / 20.0))
    emit("  [COMPUTED]  The c_R column is much kinder (1.3% to 7.9% of R) because")
    emit("  a 1-to-5-wide wing makes R large relative to the cost.  BOTH views")
    emit("  are true and they answer different questions: cost as a share of")
    emit("  PREMIUM is what a high-frequency 0DTE seller pays; cost as a share")
    emit("  of R is what a risk-budget comparison pays.")
    emit("")
    emit("  [MODELED]  And what the model itself says the credit is at 16 delta")
    emit("  0.25 DTE, so the $0.05-$0.20 band above is not a straw man: on a")
    emit("  $%.0f index at sigma=%.0f%%, the 0.25-DTE 16-delta put is at"
         % (770.0, sig * 100.0))
    kp = 770.0 * math.exp(-0.99 * sig * math.sqrt(t_short))
    kf = kp - 5.0
    pk = bs_price(770.0, kp, t_short, r0, sig, "P")
    pw = bs_price(770.0, kf, t_short, r0, sig, "P")
    emit("  $%.2f and the 5-wide wing at $%.2f, for a credit of $%.2f per share"
         % (kp, kf, pk - pw))
    emit("  = $%.2f per contract on a $%.0f R.  A CREDIT THAT SMALL IS THE"
         % ((pk - pw) * 100.0, (5.0 - (pk - pw)) * 100.0))
    emit("  MODEL'S OWN ARTEFACT: the model has no skew, so an OTM put is priced")
    emit("  at the same vol as the ATM one.  A real 0DTE 16-delta put carries a")
    emit("  much higher implied vol.  Nothing in this section should be used to")
    emit("  price a real 0DTE ticket.")
    emit("")
    emit("  [ESTIMATED -- UNDATED VENDOR MARKETING PAGE]  The widely quoted")
    emit("  '0DTE = 59% of SPX volume' figure has NO AS-OF DATE.  Per")
    emit("  `trading-decision-data-catalogue` (SKILL.md line 163 and")
    emit("  `references/options-positioning-data.md` section 3.1): an undated")
    emit("  market-share statistic is not a statistic, it can be neither right")
    emit("  nor wrong, and it must NOT be put in a chart -- with the reason")
    emit("  stated when asked.  This study therefore reports NO 0DTE")
    emit("  share-of-volume number at all, dated or not.")

    # =================================================== 0DTE ILLUSTRATIVE
    banner("13. 0DTE, [ILLUSTRATIVE] ONLY -- and it CANNOT BE EXTRAPOLATED")
    emit("")
    emit("This section exists because leaving 0DTE out entirely would hide what")
    emit("the data CAN and CANNOT say.  It is NOT a result:")
    emit("")
    emit("  * it enters at the session OPEN and settles at the session CLOSE.")
    emit("    A real 0DTE trader's P&L is dominated by the INTRADAY PATH -- the")
    emit("    open, the lunchtime drift, whether the strike was touched at 11:00")
    emit("    or at 15:55 -- and NONE of that is in these bars;")
    emit("  * there is no intraday stop, no profit target, no roll, and no")
    emit("    intraday marking, so the daily high and low are never used;")
    emit("  * strikes are solved from the OPEN with a vol built from the 3-session")
    emit("    lagged VIX, which is a ~30-day vol.  A real 0DTE chain is priced off")
    emit("    an intraday, term-structured surface this study does not have;")
    emit("  * strikes are unrounded, and at 0DTE the listing grid ($1 on SPY) is")
    emit("    the same size as the whole modelled move;")
    emit("  * the model's own 0.25-DTE credit is an artefact of flat-vol pricing.")
    emit("")
    emit("It is printed once, it is not carried into any verdict, and nothing in")
    emit("it may be scaled up, annualised or compared with a real 0DTE book.")
    emit("")
    rows = []
    for sid in ("S3", "S6"):
        sleeve_rets, trades, bases = [], [], []
        for sym in SYMBOLS:
            r = run_odte_illustrative(sid, sym, series, window_dates, iv_ctx)
            med_r = median([t["R_dollars"] for t in r["trades"]])
            base = SLV_UNITS * (med_r if med_r is not NA else 1.0)
            bases.append(base)
            sleeve_rets.append([(p / b) if b else 0.0
                                for p, b in zip(r["daily_pnl"],
                                                r["daily_base"])])
            trades.extend(r["trades"])
        st = trade_stats([t["R_mult"] for t in trades])
        c_R = mean([t["cost_R"] for t in trades])
        cred = median([t["credit"] for t in trades])
        rows.append([sid, STRUCT_NAME[sid], st["n"], fmt_p(st["p"]),
                     signed(st["b"], 3), signed(st["E_R"]),
                     num(c_R, 4), signed(st["E_R"] - c_R),
                     moneyu(cred), moneyu(median([t["R_dollars"]
                                                  for t in trades])),
                     fmt_n_req(st["n_req"]),
                     signed(st["worst_trade"], 3),
                     ("yes" if (st["n_req"] is not NA and
                                st["n_req"] <= st["n"]) else "UNMEASURABLE")])
    show(["id", "structure", "n_avail", "p", "b", "E", "c_R", "E_net",
          "credit $", "R $", "n_req", "worst trade", "measurable?"], rows)
    emit("")
    emit("  [ILLUSTRATIVE]  Read the credit column in the right units: $5.52 PER")
    emit("  CONTRACT is 5.5 CENTS PER SHARE on a $5-wide, at a window-median")
    emit("  index price near $130.  Against that 5.5-cent credit the round-trip")
    emit("  ticket is $6.30 -- 114% of the entire premium at LOW prices, before")
    emit("  any spread widening at all.  That is the analytic cost arithmetic of")
    emit("  section 12 arriving as a measurement, and it is the one 0DTE number")
    emit("  here that would survive a real intraday simulator.")
    emit("")
    emit("  [ILLUSTRATIVE]  The gross E is NEGATIVE for both structures")
    emit("  (-0.0201R for S3 gross, -0.0353R for S6 gross), which says the flat")
    emit("  VIX vol used to price a 0.25-day option is too rich for the open-to-")
    emit("  close move actually realised -- but that is a statement about the")
    emit("  pricing model at 0.25 DTE, not about 0DTE trading.")
    emit("")
    emit("  [ILLUSTRATIVE]  Even taken at face value this table is a 0DTE")
    emit("  HELD-TO-SETTLEMENT result, which is a different instrument from the")
    emit("  0DTE strategies the owning skills describe.  It is reported so that")
    emit("  the absence of a 0DTE column everywhere else in this study is a")
    emit("  stated gap rather than a hidden one.")

    # ============================================================ APPENDIX A
    banner("14. APPENDIX A -- the scale control: is the tenor effect real, or the")
    emit("    fixed-dollar-wing convention? (limitation N2)")
    emit("")
    emit("A $5.00 wing is 1.44 standard deviations of the terminal")
    emit("distribution at 7 DTE and 0.15 at 730 DTE (at the window-median index")
    emit("price), because sigma*sqrt(T) grows as sqrt(T) while the wing does")
    emit("not.  The control below re-runs the")
    emit("short put spread (S3) and the iron condor (S6) with the wing")
    emit("RE-SOLVED AT EVERY TRADE so it holds 0.15 sigma, rounded to the")
    emit("nearest dollar with a $1 floor.  Everything else -- delta rules, entry")
    emit("programme, vol, cost, settlement -- is unchanged.")
    emit("")
    rows_fixed, rows_scaled = [], []
    rows_scaled_by_sid = {}
    for sid in ("S3", "S6"):
        rows_scaled_by_sid[sid] = []
        for t in TENOR_DAYS:
            rs_f, rs_s = [], []
            for sym in SYMBOLS:
                rf = run_cell(sid, sym, t, "BASE", series, window_dates, iv_ctx,
                              wing_mode="FIXED")
                rsc = run_cell(sid, sym, t, "BASE", series, window_dates,
                               iv_ctx, wing_mode="SIG015")
                rs_f.extend(rf["trades"])
                rs_s.extend(rsc["trades"])
            sf = trade_stats([x["R_mult"] for x in rs_f])
            ss = trade_stats([x["R_mult"] for x in rs_s])
            cf = mean([x["cost_R"] for x in rs_f])
            cs = mean([x["cost_R"] for x in rs_s])
            crwf = median([x["credit_per_share"] / x["width"] for x in rs_f
                           if x["width"] is not NA])
            crws = median([x["credit_per_share"] / x["width"] for x in rs_s
                           if x["width"] is not NA])
            wf = median([x["width"] for x in rs_f if x["width"] is not NA])
            ws = median([x["width"] for x in rs_s if x["width"] is not NA])
            ef = sf["E_R"] - cf
            es = ss["E_R"] - cs
            rows_fixed.append([sid, t, moneyu(wf), num(crwf, 4),
                               signed(sf["E_R"]), num(cf, 4), signed(ef),
                               fmt_n_req(sf["n_req"]), sf["n"]])
            rows_scaled.append([sid, t, moneyu(ws), num(crws, 4),
                                signed(ss["E_R"]), num(cs, 4), signed(es),
                                fmt_n_req(ss["n_req"]), ss["n"]])
            rows_scaled_by_sid[sid].append((t, es))
    emit("--- FIXED $5.00 wing (the pre-registered grid, repeated here)")
    show(["id", "DTE", "W $", "cr/W", "E", "c_R", "E_net", "n_req", "n_avail"],
         rows_fixed)
    emit("--- ADAPTIVE 0.15-sigma wing (the scale control)")
    show(["id", "DTE", "W $", "cr/W", "E", "c_R", "E_net", "n_req", "n_avail"],
         rows_scaled)
    emit("")
    emit("  What the control is FOR: if tenor's apparent advantage were purely")
    emit("  the shrinking wing, the adaptive rows would flatten.  Compare the")
    emit("  E_net columns row by row.")
    for sid in ("S3", "S6"):
        emit("")
        emit("  %s: E_net peaks at DTE %s with the fixed wing."
             % (sid, peak_of(S, sid, "E_net")[0]))
        bt, bv = NA, NA
        for t, v in rows_scaled_by_sid[sid]:
            if bv is NA or v > bv:
                bt, bv = t, v
        emit("      adaptive 0.15-sigma wing: E_net peaks at DTE %s (%+.4f)."
             % (bt, bv))
    emit("")
    emit("  [MODELED]  Both series are reported; neither is privileged.  The")
    emit("  fixed wing is the pre-registered grid and every headline uses it.")
    write_csv("appendixA_scale_control.csv",
              ["wing_mode", "sid", "tenor", "W_dollars", "credit_over_width",
               "E", "c_R", "E_net", "n_req", "n_available"],
              [["FIXED"] + r for r in rows_fixed] +
              [["SIG015"] + r for r in rows_scaled])

    # ============================================================ LIMITATIONS
    banner("15. WHAT THIS STUDY CANNOT SEE, STATED PLAINLY")
    emit("")
    emit("  1. NO TERM STRUCTURE.  One vol -- the 3-session-lagged VIX, a ~30-day")
    emit("     vol -- prices 7 DTE and 730 DTE alike.  A real 730-DTE option has")
    emit("     its own implied vol, its own skew and its own dividend assumptions.")
    emit("     This is the single largest weakness of a study whose subject IS")
    emit("     tenor, and it is not repairable from these feeds.")
    emit("  2. NO SKEW SURFACE, and a skew surface is itself a function of tenor.")
    emit("     Test 5 sizes the direction-ambiguous part of it (+-1.5 vol points")
    emit("     on the sold legs).  It cannot size the tenor-dependent part.")
    emit("  3. FIXED DOLLAR WING (N2).  Appendix A is the control; read every")
    emit("     5-wide number beside it.")
    emit("  4. NO ASSIGNMENT, NO EARLY EXERCISE, NO DIVIDENDS.  SPY/QQQ/IWM are")
    emit("     American and physically settled; every leg here is European and")
    emit("     cash-settled.  This omits an EXERCISE EVENT whose annual")
    emit("     probability is roughly proportional to the holding period, so a")
    emit("     730-DTE short call's real risk is understated by far more than a")
    emit("     7-DTE one's.  The model also pays no dividend, so a 730-DTE")
    emit("     modelled call is too expensive and a 730-DTE modelled put too")
    emit("     cheap -- and the covered call's whole economics turn on dividends.")
    emit("  5. NO INTRADAY PATH, so no 0DTE result and no intra-trade stop.")
    emit("  6. NO VEGA P&L PATH.  Vol is a function of the lagged VIX close, so a")
    emit("     position does experience some mark-to-market vol movement -- but")
    emit("     this is a 3-session-lagged series, not a live surface, and the")
    emit("     long-tenor cells' vega exposure is therefore not measured.")
    emit("  7. NO ROLL, NO MARGIN, NO BUYING-POWER CONSTRAINT, NO LEVERAGE LIMIT.")
    emit("     The 730-DTE cells would in reality tie up margin for two years.")
    emit("  8. THE ENTRY CALENDAR DIFFERS BY TENOR (N3).  The 7-DTE programme")
    emit("     enters ~1300 times and the 730-DTE programme ~12 times, at")
    emit("     different dates.  A tenor difference is a difference in holding")
    emit("     period AND in which dates were sampled.")
    emit("  9. ONE WINDOW.  %.1f years, %d complete months, %d complete years,"
         % (years, len(groups["M"]), len(groups["Y"])))
    emit("     and two crashes.  That is enough to see a tail, not enough to")
    emit("     grade every corner -- which is exactly what Test 3 measures.")
    emit(" 10. SEVEN STRUCTURES, PRE-REGISTERED, AND NO OTHERS.  In particular")
    emit("     nothing here speaks to calendars, diagonals, ratios, jade lizards")
    emit("     or any 3-leg structure.")
    emit("")

    # ------------------------------------------------------------ the verdict
    banner("16. THE ONE-PARAGRAPH ANSWER")
    emit("")
    emit("  Every number in this study is [MODELED], and the tenor axis is the")
    emit("  worst axis to study without a term structure.  Within those limits")
    emit("  the measured answer is below; the narrative is in FINDINGS.md.")
    emit("")
    best_rows = []
    for sid in STRUCT_IDS:
        en_t, en_v = peak_of(S, sid, "E_net")
        thr_t, thr_v = peak_of(S, sid, "theta_pd_R")
        # the best E_net among measurable cells
        mt, mv = NA, NA
        for t in TENOR_DAYS:
            c = S["BASE"][(sid, t)]
            if c["n_req"] is NA or c["n_req"] > c["n"]:
                continue
            if mv is NA or c["E_net"] > mv:
                mt, mv = t, c["E_net"]
        best_rows.append([sid, thr_t, en_t, signed(en_v), mt, signed(mv),
                          monotone_note([(t, stat_at(S, sid, t, "E_net"))
                                         for t in TENOR_DAYS])])
    show(["id", "best-paid DTE (theta/R)", "peak E_net DTE", "peak E_net",
          "best MEASURABLE DTE", "E_net there", "E_net vs DTE"],
         best_rows)
    write_csv("cells_summary.csv",
              ["sid", "tenor", "bucket", "n_available", "n_per_index", "n_req",
               "measurable", "p_gross", "p_net", "b", "E_form", "E_gross",
               "sd", "p_star", "b_star", "c_R", "E_net", "E_net_high",
               "E_net_rt", "c_R_star", "credit_over_width",
               "credit_over_notional", "R_dollars_med", "credit_med",
               "credit_ps_med", "frac_at_max", "p05", "p25", "p50", "p75",
               "R_over_notional",
               "width_over_sigT", "theta_pd_R", "ann_R", "ann_R_net", "cagr",
               "dd_R", "worst_day", "worst_trade", "worst1", "L_actual",
               "L_expected", "worst_month", "worst_year", "pos_M", "pos_Q",
               "pos_Y", "inverted_MY", "delta", "gamma", "vega", "bs_theta",
               "arb_frac"],
              [[sid, t, TENOR_BUCKET[t], S["BASE"][(sid, t)]["n"],
                S["BASE"][(sid, t)]["n_per_index"],
                S["BASE"][(sid, t)]["n_req"],
                (1 if (S["BASE"][(sid, t)]["n_req"] is not NA and
                       S["BASE"][(sid, t)]["n_req"] <=
                       S["BASE"][(sid, t)]["n"]) else 0),
                S["BASE"][(sid, t)]["p"], S["BASE"][(sid, t)]["p_net"],
                S["BASE"][(sid, t)]["b"], S["BASE"][(sid, t)]["E_form"],
                S["BASE"][(sid, t)]["E_R"], S["BASE"][(sid, t)]["sd"],
                S["BASE"][(sid, t)]["p_star"], S["BASE"][(sid, t)]["b_star"],
                S["BASE"][(sid, t)]["c_R"], S["BASE"][(sid, t)]["E_net"],
                S["BASE"][(sid, t)]["E_net_high"],
                S["BASE"][(sid, t)]["E_net_rt"], S["BASE"][(sid, t)]["c_R_star"],
                S["BASE"][(sid, t)]["credit_over_width"],
                S["BASE"][(sid, t)]["credit_over_notional"],
                S["BASE"][(sid, t)]["R_dollars_med"],
                S["BASE"][(sid, t)]["credit_med"],
                S["BASE"][(sid, t)]["credit_ps_med"],
                S["BASE"][(sid, t)]["frac_at_max"],
                S["BASE"][(sid, t)]["p05"], S["BASE"][(sid, t)]["p25"],
                S["BASE"][(sid, t)]["p50"], S["BASE"][(sid, t)]["p75"],
                S["BASE"][(sid, t)]["R_over_notional"],
                S["BASE"][(sid, t)]["width_over_sigT"],
                S["BASE"][(sid, t)]["theta_pd_R"],
                S["BASE"][(sid, t)]["ann_R"], S["BASE"][(sid, t)]["ann_R_net"],
                S["BASE"][(sid, t)]["cagr_compounded"],
                S["BASE"][(sid, t)]["dd_R"], S["BASE"][(sid, t)]["worst_day"],
                S["BASE"][(sid, t)]["worst_trade"], S["BASE"][(sid, t)]["worst1"],
                S["BASE"][(sid, t)]["L_actual"],
                S["BASE"][(sid, t)]["L_expected"],
                S["BASE"][(sid, t)]["worst_month"],
                S["BASE"][(sid, t)]["worst_year"], S["BASE"][(sid, t)]["pos_M"],
                S["BASE"][(sid, t)]["pos_Q"], S["BASE"][(sid, t)]["pos_Y"],
                (1 if S["BASE"][(sid, t)]["inverted_MY"] else 0),
                S["BASE"][(sid, t)]["delta"], S["BASE"][(sid, t)]["gamma"],
                S["BASE"][(sid, t)]["vega"], S["BASE"][(sid, t)]["bs_theta"],
                S["BASE"][(sid, t)]["arb_frac"]]
               for sid in STRUCT_IDS for t in TENOR_DAYS])
    emit("")
    emit("  Tables written to out/ as CSV; RESULTS.md written beside this file.")
    emit("  Run `py -3 handcheck.py` for the independent re-derivation, which")
    emit("  imports NOTHING from this file.")
    write_results_md()
    return S


def run_odte_illustrative(sid, sym, series, window_dates, iv_ctx):
    """[ILLUSTRATIVE] 0DTE held to settlement.  Enters at the session OPEN with
    T = 0.25/365 and settles at the session CLOSE.  It uses NO intraday path, so
    it is NOT a 0DTE result and cannot be extrapolated.  Kept separate from
    run_cell so it can never be confused with the backtested grid."""
    vix_used, r_used, kappa = iv_ctx
    s = series[sym]
    n = len(window_dates)
    T = ODTE_T_SHORT / 365.0
    per_day = [0.0] * n
    trades = []
    for j, d in enumerate(window_dates):
        k = s.index_of[d]
        S_open, S_close = s.o[k], s.c[k]
        iv = iv_of(vix_used[j], sym, j, kappa)
        if iv <= 0.0:
            continue
        r = r_used[j]
        legs, meta = build_legs(sid, S_open, S_open, T, r, iv, WING)
        credit = 0.0
        for x in legs:
            x.expiry = d
            x.T_entry = T
            x.px_entry = (S_open if x.kind == "S"
                          else bs_price(S_open, x.K, T, r, iv, x.kind))
            credit += x.entry_cash_dollars()
        cost = entry_cost(legs, meta, HEADLINE_COST, S_open)
        tm = sum(x.terminal_dollars(S_close) for x in legs)
        ml, _atb = max_loss_per_share(legs, S_open, iv, T, False)
        R = ml * 100.0 if ml > 0.0 else WING * 100.0
        per_day[j] = tm - cost
        trades.append({"sid": sid, "sym": sym, "tenor": 0, "legs": meta["legs"],
                       "contracts": meta["contracts"], "R_dollars": R,
                       "credit": credit, "cost": cost,
                       "cost_R": cost / R, "R_mult": tm / R,
                       "net_R": (tm - cost) / R, "width": meta["width"],
                       "credit_per_share": credit / 100.0,
                       "S_entry": S_open})
    med_r = median([t["R_dollars"] for t in trades])
    base = SLV_UNITS * (med_r if med_r is not NA else 1.0)
    daily = [0.0] * n
    daily_base = [0.0] * n
    for j in range(n):
        if per_day[j] != 0.0:
            daily[j] = per_day[j] / base
            daily_base[j] = base
    return {"daily_pnl": per_day, "daily_base": [base] * n,
            "daily_ret": daily, "trades": trades}


def write_results_md():
    path = os.path.join(HERE, "RESULTS.md")
    head = []
    head.append("# RESULTS -- tenor test (every table verbatim from a real run)")
    head.append("")
    head.append("Produced by `py -3 study.py` on the %s checkout.  Window "
                "2001-03-13 ... 2026-10-14." % STUDY_DATE)
    head.append("")
    head.append("**Every option number below is `[MODELED]`.**  No historical "
                "option quotes exist in `data/*.csv`.  See `README.md` section 4 "
                "for the full limitations list, including the 0DTE reasoning.")
    head.append("")
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        for line in head:
            fh.write(line + "\n")
        for line in MD:
            fh.write(line + "\n")
    return len(MD)


if __name__ == "__main__":
    main()
