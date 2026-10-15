#!/usr/bin/env python3
"""
edge_engine.py -- expectancy and payoff engineering on a closed-trade ledger.

Deterministic. Stdlib only. No network. No third-party imports.

THE QUESTION THIS ANSWERS
    "How do we make positive and overcome losses?" The honest answer is
    arithmetic, not attitude: a positive EXPECTANCY per trade, sustained long
    enough that it is separable from noise. This engine makes that arithmetic
    measurable and enforceable on a real ledger.

WHAT THIS ENGINE OWNS
    The p/b/E algebra; the break-even payoff b* = (1-p)/p, which is the single
    number that decides whether a trader is structurally profitable; cohort
    attribution with a kill list; the required-sample calculation; the
    payoff-engineering panel; cost drag in R; and risk-per-trade derived from
    streak survival.

WHAT THIS ENGINE EXPLICITLY DOES NOT OWN
    The DEFINITIONS of Sharpe, Sortino, Calmar, maximum drawdown, profit factor
    and every other risk-adjusted return metric. Those belong to
    `trade-performance-analyst`. Timeframe bucketing and significance-by-bucket
    belong to `timeframe-performance-statistics`; this engine consumes that
    skill's close-date convention and does not re-derive it. Position-sizing
    BANDS belong to `trade-sizing-recovery`, `portfolio-signal-manager` and
    `algorithmic-trader`; this engine derives ONE number -- the largest risk per
    trade a streak of length L can be survived at -- and refuses to place it in
    a band or a ladder.

INPUT
    CSV with header:  trade_id,open_date,close_date,pnl
      plus OPTIONAL:  risk, cost, setup, symbol, dte, iv_rank, side
      * Dates are ISO YYYY-MM-DD.
      * `pnl` is the REALISED P&L of one CLOSED trade; may be negative, may be
        zero. A zero-P&L trade is a break-even trade: it is counted in n, it
        contributes 0 to the expectancy, and it is EXCLUDED from the win-rate
        denominator (wins / (wins + losses)), matching the convention already
        used by `timeframe-performance-statistics`.
      * `risk` is the PLANNED per-trade risk unit. If the column exists and
        every row carries a positive value, the engine runs in R MODE and every
        statistic is in R units (r_i = pnl_i / risk_i). Otherwise it runs in
        CURRENCY MODE and says so, loudly, in the output.
      * `cost` is commission + fees + half-spread for that trade, in the same
        currency as `pnl`. Absent -> 0, and the engine says so loudly, because
        every result is flattering at zero cost.
      * Lines beginning with `#` are comments. A comment beginning
        `# PROVENANCE:` is echoed into this engine's own output, so an output
        can never be separated from the label of the data behind it.

BUCKETING CONVENTION
    A trade belongs to the bucket containing its CLOSE date, never its open
    date. This is the convention `timeframe-performance-statistics` states once
    and uses everywhere; it is repeated here rather than re-invented.

USAGE
    py -3 scripts/edge_engine.py --csv examples/logs/<log>.csv
    py -3 scripts/edge_engine.py --csv --capital 250000 --dd-tolerance 50000 log.csv
    py -3 scripts/edge_engine.py --json log.csv
    py -3 scripts/edge_engine.py --cohort-csv cohorts.csv log.csv

    --capital N        account equity, for translating R into dollars
    --dd-tolerance N   currency the account can lose before the method is
                       abandoned. DEFAULT: 20% of --capital.
    --safety F         streak-survival safety multiple. DEFAULT 1.5.
    --json             machine-readable output
    --csv              append the cohort table as a CSV block
    --cohort-csv F     write the cohort table to file F
    --quiet            suppress the pooled and cohort panels
    --version          print the engine version

EXIT CODES
    0  ran
    2  the input could not be read or parsed (the message names the line)
"""

import argparse
import csv
import json
import math
import os
import random
import re
import sys
from datetime import date

ENGINE_VERSION = "1.0.0"

NA = None

# ---------------------------------------------------------------------------
# Named constants. These are the rule, not a preference. A reader who disagrees
# with one should change it here and say so -- that is why they are constants
# with names instead of numbers buried in a comparison.
# ---------------------------------------------------------------------------
MIN_COHORT_N_FOR_VERDICT = 30   # below this, a cohort is INSUFFICIENT, never KILL
FAMILY_ALPHA = 0.05             # family-wise error rate for the cohort screen
STREAK_SAFETY_DEFAULT = 1.5     # survival multiple applied to the streak length
DEFAULT_CAPITAL = 100000.0      # only used to make --dd-tolerance concrete
DD_TOLERANCE_FRACTION = 0.20    # default tolerance = 20% of capital
SIM_SEED = 20261014             # fixed: the streak simulation is reproducible
SIM_TRIALS_MAX = 20000
SIM_DRAW_MAX = 4000000          # cap total draws so runtime stays bounded
PAYOFF_TARGETS = (0.2, 0.3, 0.5)   # E targets, in R, for the payoff panel
PAYOFF_LADDER = (1.0, 1.5, 2.0, 3.0)
DTE_EDGES = ((8, "DTE 0-7"), (22, "DTE 8-21"), (46, "DTE 22-45"),
             (91, "DTE 46-90"), (None, "DTE 91+"))
IVR_EDGES = ((25.0, "IVR 0-25"), (50.0, "IVR 25-50"), (75.0, "IVR 50-75"),
             (None, "IVR 75-100"))

# The claim this engine exists to make honest.
CENTRAL_CLAIM = (
    "CENTRAL CLAIM -- no amount of position management, trimming, rolling or "
    "hedging creates edge. Those manage risk. Expectancy comes from only four "
    "levers: raise p, raise b, cut cost, and trade enough times to know which "
    "of the first three you actually have. The sharpest consequence: most "
    "negative traders have a GOOD win rate and a BAD payoff -- b below "
    "(1-p)/p -- which is the disposition effect, not bad luck."
)

MULTIPLE_TESTING_NOTE = (
    "MULTIPLE TESTING -- every cohort below is a hypothesis test run on the "
    "same ledger. Testing m hypotheses at a two-sided alpha of 0.05 means the "
    "probability that AT LEAST ONE clears the bar by chance alone is roughly "
    "1-(1-0.05)^m. A single significant slice out of 20 is EXPECTED BY CHANCE. "
    "The bar is therefore Bonferroni-adjusted to 0.05/m, and the count of "
    "cohorts that clear the ADJUSTED bar is the only count worth acting on."
)

ZERO_COST_WARNING = (
    "*** COST IS ZERO IN THIS RUN ***  No `cost` column was supplied (or every "
    "row carried 0). Every expectancy figure below is therefore GROSS. Real "
    "commissions, exchange and regulatory fees, and half the bid-ask spread are "
    "not free; on a short-dated option a realistic round trip is a meaningful "
    "fraction of one R. A gross number is a flattering number. Supply `cost` "
    "and re-run before acting on anything here."
)

STREAK_NOTE = (
    "STREAK FORMULA -- L ~= ln(N) / ln(1/(1-p)). This is an APPROXIMATION: it "
    "is the expected longest run of losses in N independent Bernoulli(p) trades, "
    "the standard asymptotic estimate, and it is biased LOW because it ignores "
    "the tendency of losses to cluster. It is reported beside a seeded "
    "simulation of the same quantity so the two can be compared."
)

LEVER_NOTE = (
    "LEVER NOTE -- (d) 'more trades' changes nothing per trade. Expectancy per "
    "trade is a property of p, b and cost, not of n. n changes only whether the "
    "edge you have is DISTINGUISHABLE from zero, which is the n_req row."
)


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def fmt_num(v, nd=4):
    if v is NA:
        return "n/a"
    if isinstance(v, str):
        return v
    if isinstance(v, float) and (math.isinf(v) or math.isnan(v)):
        return "inf" if v > 0 else ("-inf" if v < 0 else "n/a")
    return "{:.{nd}f}".format(v, nd=nd)


def fmt_money(v, nd=2):
    if v is NA:
        return "n/a"
    if isinstance(v, str):
        return v
    if isinstance(v, float) and (math.isinf(v) or math.isnan(v)):
        return "inf" if v > 0 else ("-inf" if v < 0 else "n/a")
    return "{:,.{nd}f}".format(v, nd=nd)


def fmt_pct(v, nd=2):
    if v is NA or isinstance(v, str):
        return "n/a" if v is NA else v
    if isinstance(v, float) and math.isnan(v):
        return "n/a"
    return "{:.{nd}f}%".format(v * 100.0, nd=nd)


def jsonable(v):
    if v is NA:
        return None
    if isinstance(v, float):
        if math.isinf(v):
            return "inf" if v > 0 else "-inf"
        if math.isnan(v):
            return None
    return v


def parse_amount(raw, line_no):
    """Parse a currency-ish number: 1,234.50  $1,234.50  (1,234.50)  -1234.5."""
    s = str(raw).strip()
    if s == "":
        raise ValueError("line %d: empty amount" % line_no)
    neg = False
    if s.startswith("(") and s.endswith(")"):
        neg = True
        s = s[1:-1].strip()
    s = s.replace(",", "").replace("$", "").replace(" ", "")
    try:
        val = float(s)
    except ValueError:
        raise ValueError("line %d: cannot parse amount %r as a number" % (line_no, raw))
    return -val if neg else val


def parse_iso_date(raw, line_no, field):
    s = str(raw).strip()
    try:
        return date.fromisoformat(s)
    except ValueError:
        raise ValueError("line %d: %s %r is not ISO YYYY-MM-DD" % (line_no, field, raw))


def sample_sd(values):
    n = len(values)
    if n < 2:
        return NA
    m = sum(values) / n
    var = sum((v - m) ** 2 for v in values) / (n - 1)
    if var < 0:
        var = 0.0
    return math.sqrt(var)


def norm_ppf(q):
    """Inverse standard-normal CDF (Acklam's rational approximation).

    |relative error| < 1.15e-9 over the whole open interval. Stdlib only, so the
    Bonferroni bar is computed here rather than imported from anywhere.
    """
    if q is NA or q <= 0.0 or q >= 1.0:
        return NA
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow = 0.02425
    phigh = 1.0 - plow
    if q < plow:
        x = math.sqrt(-2.0 * math.log(q))
        return (((((c[0] * x + c[1]) * x + c[2]) * x + c[3]) * x + c[4]) * x + c[5]) / \
               ((((d[0] * x + d[1]) * x + d[2]) * x + d[3]) * x + 1.0)
    if q > phigh:
        x = math.sqrt(-2.0 * math.log(1.0 - q))
        return -(((((c[0] * x + c[1]) * x + c[2]) * x + c[3]) * x + c[4]) * x + c[5]) / \
                ((((d[0] * x + d[1]) * x + d[2]) * x + d[3]) * x + 1.0)
    x = q - 0.5
    r = x * x
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * x / \
           (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1.0)


def longest_loss_streak_sim(p, n, seed=SIM_SEED):
    """Seeded, deterministic simulation of the mean longest losing streak.

    Returns (mean_max_streak, trials, note). Deterministic for a given (p, n):
    the RNG is seeded from SIM_SEED and n, so two runs agree byte for byte.
    """
    if n <= 0:
        return NA, 0, "n = 0: nothing to simulate"
    if p is NA:
        return NA, 0, "win rate not computable"
    if p >= 1.0:
        return 0.0, 0, "p = 1: no losing trades can occur"
    if p <= 0.0:
        return float(n), 0, "p = 0: every trade loses, so the streak is n"
    trials = int(SIM_DRAW_MAX // max(n, 1))
    if trials > SIM_TRIALS_MAX:
        trials = SIM_TRIALS_MAX
    if trials < 1000:
        trials = 1000
    rng = random.Random(seed + n)
    total = 0
    for _ in range(trials):
        run = 0
        best = 0
        for _ in range(n):
            if rng.random() < p:
                run = 0
            else:
                run += 1
                if run > best:
                    best = run
        total += best
    return total / float(trials), trials, ""


# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------

class InputError(Exception):
    pass


OPTIONAL_COLUMNS = ("risk", "cost", "setup", "symbol", "dte", "iv_rank", "side")


def read_log(path):
    """Return (trades, provenance, comment_count, columns_present).

    Comment lines beginning `# PROVENANCE:` are returned so the caller can echo
    them. A header-only CSV is legal and yields an empty trade list: n = 0 is a
    real state a ledger can be in, and it must not crash the engine.
    """
    if not os.path.isfile(path):
        raise InputError("no such file: %s" % path)

    provenance = []
    comments = 0
    data_lines = []
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for i, raw in enumerate(fh, 1):
            line = raw.rstrip("\n").rstrip("\r")
            if line.strip() == "":
                continue
            if line.lstrip().startswith("#"):
                comments += 1
                stripped = line.lstrip()[1:].strip()
                m = re.match(r"provenance\s*:\s*(.+)$", stripped, re.IGNORECASE)
                if m:
                    provenance.append(m.group(1).strip())
                continue
            data_lines.append((i, line))

    if not data_lines:
        raise InputError("no CSV header in %s (comment-only file)" % path)

    reader = csv.DictReader([l for _, l in data_lines])
    if reader.fieldnames is None:
        raise InputError("no CSV header in %s" % path)
    fieldnames = [f.strip() for f in reader.fieldnames]
    for required in ("close_date", "pnl"):
        if required not in fieldnames:
            raise InputError(
                "%s: header must contain '%s' (got: %s)"
                % (path, required, ",".join(fieldnames)))
    present = [c for c in OPTIONAL_COLUMNS if c in fieldnames]

    trades = []
    for idx, row in enumerate(reader):
        line_no = data_lines[idx + 1][0]
        if row is None:
            continue
        if all((v is None or str(v).strip() == "") for v in row.values()):
            continue
        close = parse_iso_date(row.get("close_date"), line_no, "close_date")
        open_raw = (row.get("open_date") or "").strip()
        opn = parse_iso_date(open_raw, line_no, "open_date") if open_raw else close
        pnl = parse_amount(row.get("pnl"), line_no)

        risk = NA
        risk_raw = (row.get("risk") or "").strip()
        if risk_raw:
            risk = parse_amount(risk_raw, line_no)

        cost = 0.0
        cost_raw = (row.get("cost") or "").strip()
        if cost_raw:
            cost = parse_amount(cost_raw, line_no)

        dte = NA
        dte_raw = (row.get("dte") or "").strip()
        if dte_raw:
            try:
                dte = float(dte_raw.replace(",", ""))
            except ValueError:
                raise ValueError("line %d: dte %r is not a number" % (line_no, dte_raw))

        ivr = NA
        ivr_raw = (row.get("iv_rank") or "").strip()
        if ivr_raw:
            try:
                ivr = float(ivr_raw.replace(",", "").replace("%", ""))
            except ValueError:
                raise ValueError("line %d: iv_rank %r is not a number" % (line_no, ivr_raw))

        trades.append({
            "trade_id": (row.get("trade_id") or "").strip() or "row%d" % line_no,
            "open_date": opn,
            "close_date": close,
            "pnl": pnl,
            "risk": risk,
            "cost": cost,
            "cost_given": bool(cost_raw),
            "setup": (row.get("setup") or "").strip() or NA,
            "symbol": (row.get("symbol") or "").strip() or NA,
            "dte": dte,
            "iv_rank": ivr,
            "side": (row.get("side") or "").strip() or NA,
            "line": line_no,
        })

    trades.sort(key=lambda t: (t["close_date"], t["trade_id"]))
    return trades, provenance, comments, present


# ---------------------------------------------------------------------------
# Units mode
# ---------------------------------------------------------------------------

def decide_units_mode(trades, present):
    """Return (mode, reason, r_dollars).

    R MODE requires the `risk` column AND a positive risk on every row: a
    partial risk column would mix two units inside one mean, which is worse than
    either unit alone.
    """
    if "risk" not in present:
        return "CURRENCY", ("no `risk` column: every figure below is in currency "
                            "per trade, and position size therefore contaminates "
                            "the payoff ratio"), NA
    bad = [t for t in trades if t["risk"] is NA or t["risk"] <= 0]
    if bad:
        return "CURRENCY", ("`risk` column present but %d of %d rows carry no "
                            "positive risk (first: line %d). Mixing units inside "
                            "one mean is worse than either unit alone, so the run "
                            "falls back to CURRENCY"
                            % (len(bad), len(trades), bad[0]["line"])), NA
    if not trades:
        return "R", "`risk` column present and no rows to contradict it", NA
    return "R", "`risk` column present and positive on every row", NA


def r_multiples(trades, mode):
    """Per-trade value in the run's unit: R-multiples in R MODE, currency else."""
    if mode == "R":
        return [t["pnl"] / t["risk"] for t in trades]
    return [t["pnl"] for t in trades]


def unit_r_dollars(trades, mode):
    """Currency value of one unit, so cost drag can be expressed in that unit.

    R MODE: the mean planned risk in currency.
    CURRENCY MODE: there is no planned R, so the mean absolute loss is used as
    the proxy and the output says so.
    """
    if mode == "R":
        vals = [t["risk"] for t in trades if t["risk"] is not NA and t["risk"] > 0]
        return (sum(vals) / len(vals)) if vals else NA
    losses = [-t["pnl"] for t in trades if t["pnl"] < 0]
    return (sum(losses) / len(losses)) if losses else NA


# ---------------------------------------------------------------------------
# Core statistics
# ---------------------------------------------------------------------------

def panel_stats(trades, mode, r_dollars, cost_per_trade, label="panel"):
    """Every scalar this engine owns, computed defensively.

    Never raises for a degenerate sample: n=0, all wins (avg_loss=0 -> b=inf),
    all losses, one trade, sd=0, a single-member cohort. Each of those sets a
    field to n/a or inf and leaves the rest of the panel intact.
    """
    vals = r_multiples(trades, mode)
    n = len(vals)
    out = {
        "label": label,
        "n": n,
        "n_decided": 0,
        "wins": 0,
        "losses": 0,
        "breakeven_trades": 0,
        "p": NA,
        "avg_win": NA,
        "avg_loss": NA,
        "b": NA,
        "E": NA,
        "E_formula": NA,
        "E_net": NA,
        "p_star": NA,
        "b_star": NA,
        "edge_p": NA,
        "kelly": NA,
        "half_kelly": NA,
        "sd_R": NA,
        "mean_R": NA,
        "n_req": NA,
        "trades_per_year": NA,
        "years_at_pace": NA,
        "L_formula": NA,
        "L_sim": NA,
        "L_sim_trials": 0,
        "L_note": "",
        "R_max_frac": NA,
        "R_max_dollars": NA,
        "c_R": NA,
        "gross_profit": 0.0,
        "gross_loss": 0.0,
        "net": 0.0,
        "verdict": "INSUFFICIENT SAMPLE",
        "verdict_detail": "",
    }

    if n == 0:
        out["verdict_detail"] = "no trades in this panel: every statistic is undefined"
        out["L_note"] = "n = 0"
        return out

    wins = len([v for v in vals if v > 0])
    losses = len([v for v in vals if v < 0])
    breakeven = n - wins - losses
    decided = wins + losses

    # A currency P&L of exactly 0 is a break-even trade in either mode; in R MODE
    # the sign of r is the sign of pnl because risk > 0 by construction.
    gp_vals = [v for v in vals if v > 0]
    gl_vals = [-v for v in vals if v < 0]
    gross_profit = sum(gp_vals)
    gross_loss = sum(gl_vals)

    mean_val = sum(vals) / n
    sd_val = sample_sd(vals)

    p = (wins / decided) if decided > 0 else NA
    avg_win = (gross_profit / wins) if wins > 0 else NA
    avg_loss = (gross_loss / losses) if losses > 0 else NA

    if avg_win is NA and avg_loss is NA:
        b = NA
    elif avg_loss is NA:
        b = float("inf")          # all wins: a defined infinite payoff ratio
    elif avg_loss == 0:
        b = float("inf")
    else:
        b = (avg_win / avg_loss) if avg_win is not NA else 0.0

    if p is NA or b is NA:
        E_formula = NA
    elif math.isinf(b):
        E_formula = float("inf") if p > 0 else NA
    else:
        E_formula = p * b - (1.0 - p)

    # The engine's primary expectancy is the SAMPLE MEAN of the per-trade
    # values, because that is the quantity n_req = 4*(sd/|E|)^2 is about. The
    # closed form p*b-(1-p) equals it exactly when the mean loss is 1R (in R
    # mode) or 1 unit (in currency mode); both are printed so the gap is visible.
    E = mean_val

    if b is NA:
        p_star = NA
        b_star = NA
        kelly = NA
    elif math.isinf(b):
        p_star = 0.0
        b_star = (1.0 - p) / p if (p is not NA and p > 0) else float("inf")
        kelly = p                      # limit of (p*b-(1-p))/b as b -> inf
    else:
        p_star = 1.0 / (1.0 + b) if (1.0 + b) != 0 else NA
        b_star = ((1.0 - p) / p) if (p is not NA and p > 0) else float("inf")
        kelly = ((p * b - (1.0 - p)) / b) if b != 0 else NA

    edge_p = (p - p_star) if (p is not NA and p_star is not NA) else NA

    c_R = NA
    if cost_per_trade is not NA:
        if r_dollars is not NA and r_dollars > 0:
            c_R = cost_per_trade / r_dollars
        elif r_dollars is NA:
            c_R = NA
    E_net = (E - c_R) if (E is not NA and c_R is not NA) else E

    # --- how many trades before the edge is distinguishable from zero ---------
    n_req = NA
    n_req_note = ""
    if E is NA:
        n_req_note = "expectancy undefined"
    elif sd_val is NA:
        n_req_note = "sample sd undefined (fewer than 2 trades)"
    elif E == 0:
        n_req_note = "expectancy is exactly zero: no sample size separates zero from zero"
    elif sd_val == 0:
        n_req = 0.0
        n_req_note = "zero dispersion: every trade is identical, so E is known exactly"
    else:
        n_req = 4.0 * (sd_val / abs(E)) ** 2

    out.update({
        "n_decided": decided,
        "wins": wins,
        "losses": losses,
        "breakeven_trades": breakeven,
        "p": p,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "b": b,
        "E": E,
        "E_formula": E_formula,
        "E_net": E_net,
        "p_star": p_star,
        "b_star": b_star,
        "edge_p": edge_p,
        "kelly": kelly,
        "half_kelly": (kelly / 2.0) if kelly is not NA else NA,
        "sd_R": sd_val,
        "mean_R": mean_val,
        "n_req": n_req,
        "c_R": c_R,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "net": gross_profit - gross_loss,
    })

    # --- streak length and the survival-derived risk per trade ---------------
    L_formula = NA
    if p is NA:
        out["L_note"] = "win rate not computable"
    elif p >= 1.0:
        L_formula = 0.0
        out["L_note"] = "p = 1: no losing trades can occur"
    elif p <= 0.0:
        L_formula = float(n)
        out["L_note"] = "p = 0: every trade loses, so the streak is n"
    else:
        denom = math.log(1.0 / (1.0 - p))
        L_formula = math.log(n) / denom if (n > 1 and denom > 0) else NA
        if n <= 1:
            out["L_note"] = "n <= 1: ln(N) has nothing to work with"
    L_sim, trials, sim_note = longest_loss_streak_sim(p, n)
    if sim_note and sim_note != out["L_note"]:
        out["L_note"] = (out["L_note"] + "; " if out["L_note"] else "") + sim_note
    out["L_formula"] = L_formula
    out["L_sim"] = L_sim
    out["L_sim_trials"] = trials
    return out


def apply_survival(out, dd_tolerance, safety, capital):
    """R_max = D_tolerance / (L * safety). The only defensible way to pick it."""
    L = out.get("L_sim")
    if L is NA or L == 0:
        L = out.get("L_formula")
    out["L_used"] = L
    out["dd_tolerance"] = dd_tolerance
    out["safety"] = safety
    out["capital"] = capital
    if L is NA or L <= 0:
        out["R_max_frac"] = NA
        out["R_max_dollars"] = NA
        out["R_max_note"] = "no usable streak length: survival risk cannot be derived"
        return out
    if capital is NA or capital <= 0:
        out["R_max_frac"] = NA
        out["R_max_dollars"] = NA
        out["R_max_note"] = "no positive capital supplied"
        return out
    frac = (dd_tolerance / capital) / (L * safety)
    out["R_max_frac"] = frac
    out["R_max_dollars"] = frac * capital
    out["R_max_note"] = ""
    return out


def pace_stats(out, trades):
    """Observed trades per year, and years of trading to reach n_req."""
    if len(trades) >= 1:
        span_days = (trades[-1]["close_date"] - trades[0]["close_date"]).days
    else:
        span_days = 0
    out["span_days"] = span_days
    if span_days <= 0 or not trades:
        out["trades_per_year"] = NA
    else:
        out["trades_per_year"] = len(trades) / (span_days / 365.25)
    if out["n_req"] is NA or out["trades_per_year"] is NA or out["trades_per_year"] <= 0:
        out["years_at_pace"] = NA
    else:
        out["years_at_pace"] = out["n_req"] / out["trades_per_year"]
    return out


def decide_pooled_verdict(out):
    E_net = out.get("E_net")
    n = out.get("n", 0)
    n_req = out.get("n_req")
    if n == 0 or E_net is NA:
        out["verdict"] = "INSUFFICIENT SAMPLE"
        out["verdict_detail"] = "no expectancy is computable from this ledger"
        return out
    if E_net <= 0:
        out["verdict"] = "NEGATIVE EDGE"
        out["verdict_detail"] = (
            "net expectancy is %.4f per trade. No sample size fixes this: more "
            "trades of a negative-expectancy process lose more money, more "
            "reliably." % E_net)
        return out
    if n_req is NA:
        out["verdict"] = "POSITIVE EDGE"
        out["verdict_detail"] = (
            "net expectancy is %+.4f per trade and the required sample is not "
            "computable, so the edge is asserted on dispersion grounds alone. "
            "Treat that as unproven." % E_net)
        return out
    if n < n_req:
        out["verdict"] = "INSUFFICIENT SAMPLE (< n_req trades)"
        out["verdict_detail"] = (
            "net expectancy is %+.4f per trade, but %d trades is short of the "
            "%.0f needed for the edge to be 2 standard errors from zero. The "
            "sign is promising; it is not yet a finding." % (E_net, n, n_req))
        return out
    out["verdict"] = "POSITIVE EDGE"
    out["verdict_detail"] = (
        "net expectancy is %+.4f per trade over %d trades, at or beyond the "
        "%.0f trades needed for a 2-sigma separation from zero." % (E_net, n, n_req))
    return out


# ---------------------------------------------------------------------------
# Cohorts
# ---------------------------------------------------------------------------

def dte_bucket(v):
    if v is NA:
        return NA
    for edge, name in DTE_EDGES:
        if edge is None or v < edge:
            return name
    return NA


def iv_bucket(v):
    if v is NA:
        return NA
    x = v * 100.0 if v <= 1.0 else v     # accept a fraction or a percentage
    for edge, name in IVR_EDGES:
        if edge is None or x < edge:
            return name
    return NA


def month_bucket(d):
    return "%04d-%02d" % (d.year, d.month)


COHORT_DIMENSIONS = (
    ("setup", lambda t: t["setup"]),
    ("symbol", lambda t: t["symbol"]),
    ("dte", lambda t: dte_bucket(t["dte"])),
    ("iv_rank", lambda t: iv_bucket(t["iv_rank"])),
    ("side", lambda t: t["side"]),
    ("month", lambda t: month_bucket(t["close_date"])),
)


def build_cohorts(trades, mode, r_dollars, cost_per_trade, z_bar):
    cohorts = []
    m = 0
    for dim, keyfn in COHORT_DIMENSIONS:
        if dim == "setup" and not any(t["setup"] is not NA for t in trades):
            continue
        if dim == "symbol" and not any(t["symbol"] is not NA for t in trades):
            continue
        if dim == "side" and not any(t["side"] is not NA for t in trades):
            continue
        if dim == "dte" and not any(t["dte"] is not NA for t in trades):
            continue
        if dim == "iv_rank" and not any(t["iv_rank"] is not NA for t in trades):
            continue
        groups = {}
        for t in trades:
            k = keyfn(t)
            if k is NA:
                continue
            groups.setdefault(k, []).append(t)
        for k in sorted(groups.keys()):
            m += 1
            st = panel_stats(groups[k], mode, r_dollars, cost_per_trade,
                             label="%s=%s" % (dim, k))
            sd = st["sd_R"]
            n = st["n"]
            E = st["E"]
            if sd is NA or n < 2 or E is NA:
                t_stat = NA
            elif sd == 0:
                t_stat = NA
            else:
                se = sd / math.sqrt(n)
                t_stat = (E / se) if se > 0 else NA
            E_net = st["E_net"]
            if n < MIN_COHORT_N_FOR_VERDICT:
                verdict = "INSUFFICIENT (n<30)"
            elif E_net is NA:
                verdict = "INSUFFICIENT (n<30)"
            elif E_net <= 0:
                verdict = "KILL (E_net<=0 with n>=30)"
            else:
                verdict = "KEEP"
            clears = (t_stat is not NA and z_bar is not NA and abs(t_stat) > z_bar)
            cohorts.append({
                "dimension": dim,
                "cohort": k,
                "n": n,
                "p": st["p"],
                "b": st["b"],
                "E": E,
                "E_net": E_net,
                "sd_R": sd,
                "t_stat": t_stat,
                "clears_adjusted_bar": clears,
                "verdict": verdict,
                "b_star": st["b_star"],
            })
    return cohorts, m


# ---------------------------------------------------------------------------
# Payoff engineering and lever sensitivity
# ---------------------------------------------------------------------------

def payoff_panel(out):
    p = out.get("p")
    b_actual = out.get("b")
    c_R = out.get("c_R")
    rows_needed = []
    if p is not NA and p > 0:
        for target in PAYOFF_TARGETS:
            b_need = (target + 1.0 - p) / p
            p_star = 1.0 / (1.0 + b_need) if b_need is not NA else NA
            # the payoff needed to clear the target AFTER cost
            b_need_net = ((target + (c_R if c_R is not NA else 0.0)) + 1.0 - p) / p
            rows_needed.append({
                "E_target": target,
                "b_needed": b_need,
                "p_star_at_that_b": p_star,
                "b_needed_net_of_cost": b_need_net,
            })
    rows_actual = []
    if p is not NA:
        for b in PAYOFF_LADDER:
            E_at_b = p * b - (1.0 - p)
            rows_actual.append({
                "b": b,
                "E": E_at_b,
                "E_net": (E_at_b - c_R) if c_R is not NA else E_at_b,
                "is_actual": (b_actual is not NA and not math.isinf(b_actual)
                              and abs(b - b_actual) < 1e-9),
            })
        if b_actual is not NA:
            if math.isinf(b_actual):
                rows_actual.append({"b": float("inf"), "E": float("inf"),
                                    "E_net": float("inf"), "is_actual": True})
            else:
                rows_actual.append({
                    "b": b_actual,
                    "E": p * b_actual - (1.0 - p),
                    "E_net": p * b_actual - (1.0 - p) - (c_R if c_R is not NA else 0.0),
                    "is_actual": True,
                })
        rows_actual.sort(key=lambda r: r["b"])
    return {"rows_needed": rows_needed, "rows_actual": rows_actual}


def lever_panel(out):
    p = out.get("p")
    b = out.get("b")
    E_net = out.get("E_net")
    c_R = out.get("c_R")
    n = out.get("n", 0)
    n_req = out.get("n_req")
    levers = []

    def add(name, delta, detail):
        levers.append({"lever": name, "delta_E_net": delta, "detail": detail})

    if p is NA or b is NA or E_net is NA or math.isinf(b):
        return levers

    p2 = min(p + 0.05, 1.0)
    E2 = p2 * b - (1.0 - p2)
    add("(a) +5pp on p", E2 - (p * b - (1.0 - p)),
        "p %.4f -> %.4f; dE = +0.05 x (b+1) = %+.4f before cost" % (p, p2, E2 - (p * b - (1.0 - p))))

    dE_b = 0.25 * p
    add("(b) +0.25 on b", dE_b,
        "b %.4f -> %.4f; dE = +0.25 x p = %+.4f before cost" % (b, b + 0.25, dE_b))

    if c_R is NA or c_R == 0:
        add("(c) -25% on cost", 0.0,
            "cost drag is 0 in this run, so there is nothing to cut (see the cost warning)")
    else:
        add("(c) -25% on cost", 0.25 * c_R,
            "c_R %.4f -> %.4f; +%.4f to E_net per trade" % (c_R, 0.75 * c_R, 0.25 * c_R))

    cov_before = (n / n_req) if (n_req is not NA and n_req and n_req > 0) else NA
    cov_after = ((1.5 * n) / n_req) if (n_req is not NA and n_req and n_req > 0) else NA
    add("(d) +50% on n", 0.0,
        "per-trade expectancy is UNCHANGED (delta = 0 by construction). n_req "
        "coverage goes from %s to %s of the required sample"
        % (fmt_pct(cov_before, 1) if cov_before is not NA else "n/a",
           fmt_pct(cov_after, 1) if cov_after is not NA else "n/a"))
    levers.sort(key=lambda r: -abs(r["delta_E_net"]))
    return levers


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_provenance(path, provenance, n_trades, comment_count):
    lines = ["PROVENANCE"]
    lines.append("  input file      : %s" % path)
    lines.append("  trade rows      : %d" % n_trades)
    lines.append("  comment lines   : %d" % comment_count)
    if provenance:
        for p in provenance:
            lines.append("  declared        : %s" % p)
    else:
        lines.append("  declared        : NONE -- the input declares no provenance.")
        lines.append("                    Tag the source of this ledger before using "
                     "any number below.")
    return lines


def units_block(mode, reason, r_dollars, present, trades):
    lines = ["UNITS MODE"]
    if mode == "R":
        lines.append("  R MODE -- every row is divided by that row's `risk`, so every")
        lines.append("  figure below is in R units. One R = one planned unit of risk, and")
        lines.append("  the mean planned risk in this ledger is %s in currency."
                     % fmt_money(r_dollars))
        lines.append("  WHY THIS MATTERS: in currency, a bigger position makes a trade")
        lines.append("  look better and the payoff ratio silently measures position")
        lines.append("  size instead of the strategy. In R it cannot.")
    else:
        lines.append("  CURRENCY MODE -- figures below are in currency per trade.")
        lines.append("  REASON: %s" % reason)
        lines.append("  CONSEQUENCE: position size contaminates the payoff ratio, and")
        lines.append("  r_dollars is proxied by the mean absolute loss (%s)."
                     % fmt_money(r_dollars))
    lines.append("  optional columns present: %s"
                 % (", ".join(present) if present else "none"))
    return lines


def cost_block(cost_per_trade, given_rows, n, c_R, r_dollars):
    lines = ["COST INPUT"]
    lines.append("  rows carrying a `cost` value : %d of %d" % (given_rows, n))
    lines.append("  mean cost per trade          : %s" % fmt_money(cost_per_trade))
    lines.append("  cost drag c_R                : %s (of one R)"
                 % (fmt_num(c_R, 4) if c_R is not NA else "n/a"))
    if c_R is NA or c_R == 0:
        lines.append("")
        lines.append("  " + ZERO_COST_WARNING)
    else:
        lines.append("  Cost is non-zero, so E_net below is the number to act on.")
        lines.append("  c_R is expressed in the same unit as E, so `E - c_R` is a")
        lines.append("  like-for-like subtraction and never a currency-vs-R mistake.")
    return lines


def pooled_block(out):
    L = []
    L.append("  %-34s %s" % ("trades (n)", str(out["n"])))
    L.append("  %-34s %d wins / %d losses / %d break-even"
             % ("decision mix", out["wins"], out["losses"], out["breakeven_trades"]))
    L.append("  %-34s %s" % ("win rate p = wins/(wins+losses)", fmt_num(out["p"], 6)))
    L.append("  %-34s %s" % ("avg win (in unit)", fmt_num(out["avg_win"], 6)))
    L.append("  %-34s %s" % ("avg loss (in unit)", fmt_num(out["avg_loss"], 6)))
    L.append("  %-34s %s   = avg_win / avg_loss" % ("payoff ratio b", fmt_num(out["b"], 6)))
    L.append("")
    L.append("  %-34s %s   = mean of the per-trade values" % ("expectancy E", fmt_num(out["E"], 6)))
    L.append("  %-34s %s   = p*b-(1-p); equal to E when avg loss = 1 unit"
             % ("E (closed form)", fmt_num(out["E_formula"], 6)))
    recon = NA
    if (out["E_formula"] is not NA and out["avg_loss"] is not NA
            and not math.isinf(out["E_formula"]) and not math.isinf(out["avg_loss"])):
        recon = out["E_formula"] * out["avg_loss"]
    L.append("  %-34s %s   = that closed form x avg_loss: the same number as E"
             % ("E (closed form x avg_loss)", fmt_num(recon, 6)))
    L.append("  %-34s %s" % ("cost drag c_R", fmt_num(out["c_R"], 6)))
    L.append("  %-34s %s   <-- THE NUMBER TO ACT ON" % ("net expectancy E_net", fmt_num(out["E_net"], 6)))
    L.append("")
    L.append("  %-34s %s   = 1/(1+b); the win rate you must beat"
             % ("break-even win rate p*", fmt_num(out["p_star"], 6)))
    L.append("  %-34s %s   = (1-p)/p; the payoff you must beat"
             % ("break-even payoff b*", fmt_num(out["b_star"], 6)))
    L.append("  %-34s %s   = p - p*" % ("edge in win-rate terms", fmt_num(out["edge_p"], 6)))
    L.append("  %-34s %s   = (p*b-(1-p))/b" % ("Kelly fraction f*", fmt_num(out["kelly"], 6)))
    L.append("  %-34s %s" % ("half Kelly", fmt_num(out["half_kelly"], 6)))
    L.append("")
    L.append("  %-34s %s   = sample sd of the per-trade values" % ("sd_R", fmt_num(out["sd_R"], 6)))
    L.append("  %-34s %s   = 4*(sd_R/|E|)^2" % ("n_req (2-sigma)", fmt_num(out["n_req"], 2)))
    L.append("  %-34s %s" % ("trades per year (observed)", fmt_num(out["trades_per_year"], 2)))
    L.append("  %-34s %s   = n_req / trades_per_year" % ("years_at_current_pace", fmt_num(out["years_at_pace"], 2)))
    L.append("  %-34s %s   = ln(N)/ln(1/(1-p)), N = %d (approximation)"
             % ("expected longest losing streak L", fmt_num(out["L_formula"], 3), out["n"]))
    L.append("  %-34s %s   (%d seeded trials -- sanity check on the formula)"
             % ("  same L, simulated", fmt_num(out["L_sim"], 3), out["L_sim_trials"]))
    if out.get("L_note"):
        L.append("  %-34s %s" % ("  streak note", out["L_note"]))
    L.append("")
    L.append("  %-34s %s of capital = %s"
             % ("R_max (survival-derived risk/trade)",
                fmt_num(out["R_max_frac"], 6), fmt_money(out["R_max_dollars"])))
    L.append("  %-34s D_tolerance %s / (L %s x safety %s)"
             % ("  derivation", fmt_money(out["dd_tolerance"]),
                fmt_num(out.get("L_used"), 3), fmt_num(out.get("safety"), 2)))
    if out.get("R_max_note"):
        L.append("  %-34s %s" % ("  note", out["R_max_note"]))
    return L


def cohort_table(cohorts):
    cols = ["dimension", "cohort", "n", "p", "b", "E", "E_net", "t_stat", "verdict"]
    rows = []
    for c in cohorts:
        rows.append([
            c["dimension"], c["cohort"], str(c["n"]),
            fmt_num(c["p"], 4), fmt_num(c["b"], 4), fmt_num(c["E"], 4),
            fmt_num(c["E_net"], 4), fmt_num(c["t_stat"], 3), c["verdict"],
        ])
    widths = [len(x) for x in cols]
    for r in rows:
        for i, v in enumerate(r):
            widths[i] = max(widths[i], len(v))

    def line(r):
        return "  " + "  ".join(r[i].ljust(widths[i]) for i in range(len(r))).rstrip()

    out = [line(cols), "  " + "-" * (sum(widths) + 2 * (len(cols) - 1))]
    for r in rows:
        out.append(line(r))
    return out


def cohort_csv(cohorts):
    cols = ["dimension", "cohort", "n", "p", "b", "E", "E_net", "sd_R",
            "t_stat", "clears_adjusted_bar", "verdict"]
    out = [",".join(cols)]
    for c in cohorts:
        out.append(",".join([
            c["dimension"], c["cohort"], str(c["n"]),
            fmt_num(c["p"], 6), fmt_num(c["b"], 6), fmt_num(c["E"], 6),
            fmt_num(c["E_net"], 6), fmt_num(c["sd_R"], 6),
            fmt_num(c["t_stat"], 4),
            "yes" if c["clears_adjusted_bar"] else "no",
            c["verdict"].split(" ")[0],
        ]))
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args(argv):
    ap = argparse.ArgumentParser(prog="edge_engine.py",
                                 description="expectancy and payoff engineering",
                                 add_help=True)
    ap.add_argument("log", nargs="?", help="CSV trade ledger")
    ap.add_argument("--csv", action="store_true", dest="as_csv",
                    help="append the cohort table as a CSV block")
    ap.add_argument("--cohort-csv", default=None, dest="cohort_csv",
                    help="write the cohort table to this file")
    ap.add_argument("--json", action="store_true", dest="as_json",
                    help="machine-readable output")
    ap.add_argument("--capital", type=float, default=None,
                    help="account equity, for translating R into dollars")
    ap.add_argument("--dd-tolerance", type=float, default=None, dest="dd_tolerance",
                    help="currency the account can lose before the method is "
                         "abandoned; default 20%% of --capital")
    ap.add_argument("--safety", type=float, default=STREAK_SAFETY_DEFAULT,
                    help="streak-survival safety multiple (default %.1f)"
                         % STREAK_SAFETY_DEFAULT)
    ap.add_argument("--quiet", action="store_true", help="suppress the panels")
    ap.add_argument("--version", action="store_true")
    return ap.parse_args(argv)


def main(argv=None):
    # LF on every platform: Python's text-mode translation would otherwise write
    # CRLF to a redirected stdout on Windows, making an identical run produce a
    # byte-different file.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(newline="\n")

    args = parse_args(argv if argv is not None else sys.argv[1:])

    if args.version:
        print("edge_engine.py %s" % ENGINE_VERSION)
        return 0

    if not args.log:
        print("ERROR: no input ledger given. Usage: edge_engine.py [options] <log.csv>",
              file=sys.stderr)
        return 2

    capital = args.capital if args.capital is not None else DEFAULT_CAPITAL
    if capital <= 0:
        print("ERROR: --capital must be positive", file=sys.stderr)
        return 2
    dd_tolerance = (args.dd_tolerance if args.dd_tolerance is not None
                    else DD_TOLERANCE_FRACTION * capital)
    if dd_tolerance <= 0:
        print("ERROR: --dd-tolerance must be positive", file=sys.stderr)
        return 2
    if args.safety <= 0:
        print("ERROR: --safety must be positive", file=sys.stderr)
        return 2

    try:
        trades, provenance, comment_count, present = read_log(args.log)
    except (InputError, ValueError) as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2

    mode, mode_reason, _ = decide_units_mode(trades, present)
    r_dollars = unit_r_dollars(trades, mode)

    given_rows = len([t for t in trades if t["cost_given"]])
    cost_per_trade = ((sum(t["cost"] for t in trades) / len(trades))
                      if trades else 0.0)
    cost_is_zero = (cost_per_trade == 0.0)

    pooled = panel_stats(trades, mode, r_dollars, cost_per_trade, label="pooled")
    pace_stats(pooled, trades)
    apply_survival(pooled, dd_tolerance, args.safety, capital)
    decide_pooled_verdict(pooled)

    # The Bonferroni bar must be known before cohorts are screened, but m is the
    # number of cohorts tested -- so count first with a placeholder bar of None,
    # then re-screen each cohort's t against the adjusted bar.
    cohorts, m = build_cohorts(trades, mode, r_dollars, cost_per_trade, NA)
    if m > 0:
        alpha_adj = FAMILY_ALPHA / m
        z_bar = norm_ppf(1.0 - alpha_adj / 2.0)
    else:
        alpha_adj = NA
        z_bar = NA
    for c in cohorts:
        c["clears_adjusted_bar"] = bool(
            c["t_stat"] is not NA and z_bar is not NA and abs(c["t_stat"]) > z_bar)
    clearing = len([c for c in cohorts if c["clears_adjusted_bar"]])
    naive_clearing = len([c for c in cohorts
                          if c["t_stat"] is not NA and abs(c["t_stat"]) > 1.959964])

    payoffs = payoff_panel(pooled)
    levers = lever_panel(pooled)

    if args.cohort_csv:
        with open(args.cohort_csv, "w", encoding="utf-8", newline="") as fh:
            fh.write("\n".join(cohort_csv(cohorts)) + "\n")

    if args.as_json:
        payload = {
            "engine": "edge_engine.py",
            "engine_version": ENGINE_VERSION,
            "input": args.log,
            "units_mode": mode,
            "units_reason": mode_reason,
            "r_dollars": jsonable(r_dollars),
            "optional_columns": present,
            "provenance": provenance,
            "comments_total": comment_count,
            "settings": {
                "capital": capital,
                "dd_tolerance": dd_tolerance,
                "safety": args.safety,
                "min_cohort_n": MIN_COHORT_N_FOR_VERDICT,
                "family_alpha": FAMILY_ALPHA,
                "sim_seed": SIM_SEED,
            },
            "cost": {
                "rows_with_cost": given_rows,
                "mean_cost_per_trade": jsonable(cost_per_trade),
                "cost_is_zero": cost_is_zero,
                "c_R": jsonable(pooled["c_R"]),
            },
            "pooled": {k: jsonable(v) for k, v in pooled.items()
                       if not isinstance(v, (list, dict))},
            "multiple_testing": {
                "m_cohorts_tested": m,
                "family_alpha": FAMILY_ALPHA,
                "adjusted_alpha": jsonable(alpha_adj),
                "z_bar": jsonable(z_bar),
                "cohorts_clearing_adjusted_bar": clearing,
                "cohorts_clearing_naive_1p96": naive_clearing,
            },
            "cohorts": [{k: jsonable(v) for k, v in c.items()} for c in cohorts],
            "payoff_panel": payoffs,
            "levers": levers,
            "close_date_min": trades[0]["close_date"].isoformat() if trades else NA,
            "close_date_max": trades[-1]["close_date"].isoformat() if trades else NA,
        }
        print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True))
        return 0

    L = []
    L.append("=" * 78)
    L.append("EDGE AND PAYOFF ENGINEERING  --  edge_engine.py %s" % ENGINE_VERSION)
    L.append("=" * 78)
    L.extend(render_provenance(args.log, provenance, len(trades), comment_count))
    L.append("")
    L.extend(units_block(mode, mode_reason, r_dollars, present, trades))
    L.append("")
    L.extend(cost_block(cost_per_trade, given_rows, len(trades), pooled["c_R"], r_dollars))
    L.append("")
    L.append("SETTINGS")
    L.append("  capital          : %s" % fmt_money(capital))
    L.append("  D_tolerance      : %s  (%.0f%% of capital unless overridden)"
             % (fmt_money(dd_tolerance), DD_TOLERANCE_FRACTION * 100.0))
    L.append("  safety multiple  : %s" % fmt_num(args.safety, 2))
    L.append("  cohort min n     : %d" % MIN_COHORT_N_FOR_VERDICT)
    L.append("  streak sim seed  : %d (fixed -- byte-identical reruns)" % SIM_SEED)
    L.append("")
    L.append("-" * 78)
    L.append(CENTRAL_CLAIM)
    L.append("-" * 78)

    if not args.quiet:
        L.append("")
        L.append("=" * 78)
        L.append("1. POOLED PANEL")
        L.append("=" * 78)
        if pooled["n"] == 0:
            L.append("  n = 0. This ledger holds no closed trades, so nothing here is")
            L.append("  computable. That is a refusal, not a zero: a strategy with no")
            L.append("  trades has no measured expectancy, positive or negative.")
        else:
            L.extend(pooled_block(pooled))
        L.append("")
        L.append("  VERDICT: %s" % pooled["verdict"])
        L.append("           %s" % pooled["verdict_detail"])
        L.append("")
        L.append("  Read the verdict with the trap in mind: p and b are POOLED. A good")
        L.append("  cohort can hide a fatal one, and one outlier win can manufacture a")
        L.append("  payoff ratio. Panel 2 is where that gets tested.")

        L.append("")
        L.append("=" * 78)
        L.append("2. COHORT ATTRIBUTION  (sorted by E_net, worst last)")
        L.append("=" * 78)
        if not cohorts:
            if pooled["n"] == 0:
                L.append("  n = 0: there are no trades to split into cohorts.")
            else:
                L.append("  No cohort columns were supplied (setup / symbol / dte /")
                L.append("  iv_rank / side are all absent). Cohort attribution is the")
                L.append("  single highest-value thing to add to a ledger: without a")
                L.append("  `setup` tag, a fatal slice hides inside the pooled mean.")
        else:
            ranked = sorted(cohorts, key=lambda c: (
                -1e30 if c["E_net"] is NA else c["E_net"]))
            L.extend(cohort_table(ranked))
            L.append("")
            L.append("  Verdict rule (this is the rule; argue with it if you disagree):")
            L.append("    INSUFFICIENT (n<30)  : n < %d, whatever the sign" % MIN_COHORT_N_FOR_VERDICT)
            L.append("    KILL (E_net<=0 with n>=30) : n >= %d and E_net <= 0" % MIN_COHORT_N_FOR_VERDICT)
            L.append("    KEEP                 : n >= %d and E_net > 0" % MIN_COHORT_N_FOR_VERDICT)
            L.append("")
            kills = [c for c in cohorts if c["verdict"].startswith("KILL")]
            L.append("  KILL LIST (%d cohort(s) with n>=%d and E_net<=0):"
                     % (len(kills), MIN_COHORT_N_FOR_VERDICT))
            if kills:
                for c in sorted(kills, key=lambda c: c["E_net"]):
                    L.append("    %-8s %-14s n=%-4d p=%s b=%s E_net=%s"
                             % (c["dimension"], c["cohort"], c["n"],
                                fmt_num(c["p"], 4), fmt_num(c["b"], 4),
                                fmt_num(c["E_net"], 4)))
                L.append("")
                L.append("  A KILL is evidence that THIS SLICE is negative over a")
                L.append("  sample big enough to say so. It is not proof the slice can")
                L.append("  never work -- only that you have no evidence it does today.")
                L.append("  Stopping a slice is the cheapest lever in this entire skill.")
            else:
                L.append("    (none)")
            L.append("")
            mean_cohort = (pooled["n"] / len(cohorts)) if len(cohorts) else 0.0
            L.append("  COHORT MIX: %d trades across %d tested cohorts, mean cohort size"
                     % (pooled["n"], len(cohorts)))
            L.append("  %.1f. Any cohort far above that mean is a small sample wearing"
                     % mean_cohort)
            L.append("  a confident verdict.")

        L.append("")
        L.append("=" * 78)
        L.append("3. MULTIPLE-TESTING GUARD")
        L.append("=" * 78)
        L.append("  cohorts tested (m)            : %d" % m)
        L.append("  family-wise alpha             : %.4f" % FAMILY_ALPHA)
        L.append("  Bonferroni-adjusted alpha     : %s"
                 % (fmt_num(alpha_adj, 8) if alpha_adj is not NA else "n/a"))
        L.append("  adjusted two-sided |t| bar z  : %s"
                 % (fmt_num(z_bar, 4) if z_bar is not NA else "n/a"))
        L.append("  cohorts clearing ADJUSTED bar : %d of %d" % (clearing, m))
        L.append("  cohorts clearing a naive 1.96 : %d of %d" % (naive_clearing, m))
        L.append("")
        L.append("  Naive bar 1.96 corresponds to a two-sided 5%% test. At m = %d" % m)
        L.append("  tests, the family-wise false-positive rate at that bar is about")
        L.append("  %s -- which is to say the screen finds something about that"
                 % fmt_pct(1.0 - (1.0 - 0.05) ** max(m, 1), 1))
        L.append("  often whether or not any edge exists.")
        L.append("")
        L.append("  cohorts clearing the ADJUSTED bar, with their n:")
        clearers = [c for c in cohorts if c["clears_adjusted_bar"]]
        if clearers:
            for c in sorted(clearers, key=lambda c: -abs(c["t_stat"])):
                L.append("    %-8s %-14s n=%-4d t=%s"
                         % (c["dimension"], c["cohort"], c["n"],
                            fmt_num(c["t_stat"], 3)))
            L.append("")
            L.append("  READ n NEXT TO t. A cohort with a handful of observations can")
            L.append("  post an enormous |t| -- two losses out of two trades gives a t")
            L.append("  of tens -- and the Bonferroni bar does not repair a cohort with")
            L.append("  almost no data in it. The bar answers 'how many slices did I")
            L.append("  test?'. It does not answer 'was this slice big enough to test?'.")
        else:
            L.append("    (none -- no cohort's |t| exceeds the adjusted bar)")
        L.append("")
        L.append("  " + MULTIPLE_TESTING_NOTE)

        L.append("")
        L.append("=" * 78)
        L.append("4. PAYOFF-ENGINEERING PANEL  (the actionable table)")
        L.append("=" * 78)
        if pooled["p"] is NA:
            L.append("  No win rate is computable, so the payoff question has no answer.")
        else:
            L.append("  Observed p = %s, observed b = %s, b* = %s, c_R = %s"
                     % (fmt_num(pooled["p"], 4), fmt_num(pooled["b"], 4),
                        fmt_num(pooled["b_star"], 4), fmt_num(pooled["c_R"], 4)))
            L.append("")
            L.append("  (4a) At the OBSERVED p, the payoff you would need:")
            L.append("")
            L.append("  %-12s %-14s %-14s %-16s %s"
                     % ("E target", "b needed", "p* at that b", "b net of cost", "rule of thumb"))
            for r in payoffs["rows_needed"]:
                L.append("  %-12s %-14s %-14s %-16s %s"
                         % ("%+.2fR" % r["E_target"],
                            fmt_num(r["b_needed"], 4),
                            fmt_num(r["p_star_at_that_b"], 4),
                            fmt_num(r["b_needed_net_of_cost"], 4),
                            "b_needed = (E_target + 1 - p) / p"))
            L.append("")
            L.append("  (4b) At the trader's ACTUAL b and at a ladder of b:")
            L.append("")
            L.append("  %-12s %-14s %-14s %s" % ("b", "E", "E_net", "note"))
            for r in payoffs["rows_actual"]:
                note = "ACTUAL b" if r["is_actual"] else ""
                L.append("  %-12s %-14s %-14s %s"
                         % (fmt_num(r["b"], 4), fmt_num(r["E"], 4),
                            fmt_num(r["E_net"], 4), note))
            L.append("")
            b_star = pooled["b_star"]
            b_act = pooled["b"]
            if b_star is not NA and b_act is not NA and not math.isinf(b_act):
                if math.isinf(b_star):
                    L.append("  b* is infinite here (p = 0): no payoff makes this positive.")
                elif b_act < b_star:
                    L.append("  *** b = %s is BELOW b* = %s. This book is structurally"
                             % (fmt_num(b_act, 4), fmt_num(b_star, 4)))
                    L.append("      unprofitable at its current win rate: it is winning")
                    L.append("      trades and losing money. That is the disposition")
                    L.append("      effect expressed as arithmetic, not psychology. ***")
                else:
                    L.append("  b = %s is at or above b* = %s, so the payoff is not the"
                             % (fmt_num(b_act, 4), fmt_num(b_star, 4)))
                    L.append("  binding constraint.")
                    E_gross = pooled["E"]
                    c_R_here = pooled["c_R"]
                    if (E_gross is not NA and c_R_here is not NA
                            and E_gross <= c_R_here):
                        L.append("  *** COST IS THE BINDING CONSTRAINT: gross E = %s is"
                                 % fmt_num(E_gross, 4))
                        L.append("      smaller than c_R = %s, so the book pays more to"
                                 % fmt_num(c_R_here, 4))
                        L.append("      trade than it earns before costs. It does not have")
                        L.append("      an edge; it has a rounding error and a bill. ***")
                    else:
                        L.append("  Both clear on this sample, so the binding constraint")
                        L.append("  is whichever of p, b or cost moves most -- see panel 5.")
            L.append("")
            L.append("  This table converts 'make more money' into 'raise b from X to Y'.")
            L.append("  It is the only form of that instruction a trader can execute.")

        L.append("")
        L.append("=" * 78)
        L.append("5. LEVER SENSITIVITY  (ranked by effect on E_net, largest first)")
        L.append("=" * 78)
        if not levers:
            L.append("  No lever can be evaluated: p, b or E_net is undefined here.")
        else:
            L.append("  %-22s %-16s %s" % ("lever", "delta E_net", "detail"))
            for r in levers:
                L.append("  %-22s %-16s %s"
                         % (r["lever"], "%+.4f" % r["delta_E_net"], r["detail"]))
            L.append("")
            L.append("  " + LEVER_NOTE)

        L.append("")
        L.append("=" * 78)
        L.append("6. WHAT THE ENGINE CANNOT TELL YOU")
        L.append("=" * 78)
        for ln in [
            "  * It cannot tell you WHY a cohort is negative. It can only tell you",
            "    that it is, on this sample.",
            "  * It cannot see an open position, an assignment, or a roll that has",
            "    not been booked as a closed trade. Unrealised P&L is invisible here.",
            "  * It cannot detect a regime change. b* and n_req are properties of the",
            "    sample you handed it; a strategy that stopped working yesterday is",
            "    still summarised as it worked.",
            "  * It cannot tell a normal losing streak from a broken edge -- that is",
            "    exactly why L is reported: a streak of length L is EXPECTED, and a",
            "    streak materially longer than L is the first real evidence.",
            "  * It has no idea whether your `risk` column is honest. A risk that was",
            "    never enforced at entry makes every R in this report a fiction.",
            "  * The streak formula is an approximation and the simulation is seeded.",
            "    Both are estimates of an expectation, not a forecast of your next N",
            "    trades.",
        ]:
            L.append(ln)

    if args.as_csv:
        L.append("")
        L.append("=" * 78)
        L.append("COHORT TABLE (CSV)")
        L.append("=" * 78)
        L.extend(cohort_csv(cohorts))

    L.append("")
    L.append("-" * 78)
    L.append(STREAK_NOTE)
    L.append("-" * 78)

    print("\n".join(l.rstrip() for l in L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
