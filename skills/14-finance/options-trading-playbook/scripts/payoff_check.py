#!/usr/bin/env python3
"""
payoff_check.py -- will this options strategy make money?

Deterministic. Stdlib only. No network. No third-party imports.

THE QUESTION THIS ANSWERS
    Given a planned payoff corner -- a target in R, a stop in R, an expected win
    rate and a per-trade cost in R -- what is the EXPECTANCY per trade, and what
    win rate would this payoff need just to break even? Asked BEFORE capital is
    risked, so that a card can be rejected on arithmetic instead of on P&L.

WHAT THIS ENGINE OWNS
    The forward-looking payoff check: b, E, E_net, b*, p*, the edge, Kelly and
    half-Kelly, the two-point standard deviation, the sample needed, the
    expected longest losing streak, the largest risk per trade a streak of that
    length can be survived at, and a sensitivity panel. Plus the cost
    derivation from per-contract fees, the multi-rung fee-negative threshold,
    and a realised-vs-proposed comparison from a closed-trade log.

WHAT THIS ENGINE EXPLICITLY DOES NOT OWN
    Which structure expresses a given payoff corner (`options-strategist`,
    `advanced-options-structures`). The hold / trim / roll / close decision on an
    OPEN position (`options-position-lifecycle`) and single-leg surgery
    (`options-leg-management`). Position-sizing BANDS and ladders
    (`trade-sizing-recovery`, `portfolio-signal-manager`); this engine derives
    ONE number -- the largest risk per trade a streak of length L can be survived
    at -- and refuses to place it in a band. Portfolio Greeks, margin and the DTE
    calendar (`options-risk-engineer`). Expectancy MEASUREMENT on a realised
    ledger and the cohort kill list (`edge-and-payoff-engineering`). Timeframe
    bucketing and significance-by-bucket (`timeframe-performance-statistics`).
    Order execution (`options-automation-engineer`). Data provenance
    (`trading-decision-data-catalogue`).

R -- STATED ONCE, USED EVERYWHERE
    1R is the money lost per trade when the STOP FIRES. That is the definition
    this engine uses in every mode, and it is the only one that makes b a
    ratio of two things you can write down before the trade.

    * In --tp/--sl mode both are given in the same unit, and b = tp / sl. The
      unit itself is a numeraire: the engine re-bases it so the loss is exactly
      1R. This is why --sl does not appear in the E formula -- b already
      carries it. With the default --sl 1.0 the stop IS the risk unit and --tp
      reads directly as b.
    * In --credit/--width mode R is the structure's MAX LOSS, W - C, and the
      user states the target and stop in MONEY. b = tp_money / sl_money.
    * In --from-log mode R is the log's `risk` column, the planned per-trade
      risk in dollars.

    The two structural readings agree when the stop sits at the structure's
    maximum loss and differ when it does not. This engine always prints which
    one it used (see the R BASIS line).

INPUT
    CLI scalars, or a CSV log with header:
        trade_id,open_date,close_date,pnl,risk[,cost][,setup][,symbol][,dte][,iv_rank][,side]
      * Dates are ISO YYYY-MM-DD.
      * `pnl` is the REALISED P&L of one CLOSED trade; may be negative, may be
        zero. A zero-P&L trade is a break-even trade: it counts in n, it
        contributes 0 to the expectancy, and it is EXCLUDED from the win-rate
        denominator (wins / (wins + losses)), matching the convention already
        used by `timeframe-performance-statistics` and `edge-and-payoff-engineering`.
      * `risk` is the PLANNED per-trade risk unit. If the column exists and
        every row carries a positive value, the engine runs in R MODE and every
        statistic is in R units (r_i = pnl_i / risk_i). Otherwise it runs in
        CURRENCY MODE and says so, loudly, in the output.
      * `cost` is commission + fees + half-spread for that trade, in the same
        currency as `pnl`. Absent -> 0, and the engine says so loudly, because
        every result is flattering at zero cost.
      * `setup` is the cohort tag. It is what makes the comparison against a
        proposed card possible and what makes a kill list possible downstream.
      * Lines beginning with `#` are comments. A comment beginning
        `# PROVENANCE:` is echoed into this engine's own output, so that an
        output can never be separated from the label of the data behind it.

USAGE
    py -3 scripts/payoff_check.py --tp 0.5 --sl 2.0 --p 0.80
    py -3 scripts/payoff_check.py --tp 2.5 --sl 1.0 --p 0.35 --cost-r 0.02 --n 250
    py -3 scripts/payoff_check.py --credit 1.00 --width 5.00 --tp-money 50 --sl-money 200 --p 0.80
    py -3 scripts/payoff_check.py --tp 2.5 --sl 1.0 --p 0.35 \\
        --fee-per-contract 0.65 --legs 2 --r-dollars 200
    py -3 scripts/payoff_check.py --scaling-check --legs 4 --fee-per-contract 0.65 \\
        --rung-split 3 --position-value 5.00
    py -3 scripts/payoff_check.py --from-log examples/logs/synthetic-options-log.csv
    py -3 scripts/payoff_check.py --from-log log.csv --tp 2.5 --sl 1.0 --p 0.35 --json

    --tp FLOAT            target in R (the win, in R)
    --sl FLOAT            stop in R (the loss, in R). Default 1.0
    --p FLOAT             expected win rate, 0..1
    --cost-r FLOAT        cost per trade in R (round trip). Default 0
    --n INT               planned number of trades. Default 250
    --d-tol FLOAT         drawdown tolerance, percent of equity. Default 20
    --safety FLOAT        streak-survival safety multiple. Default 1.5
    --trades-per-year INT trades per year at your pace. Default 250
    --credit FLOAT        --credit/--width mode: credit received per spread, in money
    --width FLOAT         --credit/--width mode: strike width, in money
    --tp-money FLOAT      --credit/--width mode: target in money per spread
    --sl-money FLOAT      --credit/--width mode: stop in money per spread
    --fee-per-contract F  commission + fees per contract per ticket
    --legs INT            legs in the structure (round trip = 2 x legs tickets)
    --r-dollars FLOAT     currency value of 1R, for the fee derivation
    --scaling-check       print the multi-rung fee-negative threshold
    --rung-split INT      rungs in the scale-out (default 3)
    --position-value F    current mark of the whole structure, money per spread
    --from-log PATH       CSV trade log; compute realised p, b, E by cohort
    --setup TAG           restrict --from-log to one cohort tag
    --json                machine-readable output
    --csv-out PATH        write the from-log cohort table as CSV
    --version             print the engine version

EXIT CODES
    0  ran
    2  the input could not be read, parsed or reconciled
"""

import argparse
import csv
import json
import math
import sys

ENGINE_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Named constants. These are the rule, not a preference. A reader who disagrees
# should change them and say so -- that is why they are named here instead of
# being buried in a comparison.
# ---------------------------------------------------------------------------
DEFAULT_N = 250
DEFAULT_TRADES_PER_YEAR = 250
DEFAULT_D_TOL_PCT = 20.0
DEFAULT_SAFETY = 1.5
DEFAULT_SCALING_LEGS = 4
DEFAULT_RUNG_SPLIT = 3
SENS_P_WINDOW = 0.05       # +/- 5 percentage points on p
SENS_B_WINDOW = 0.25       # +/- 0.25 on b
SENS_COST_LOW = 0.5        # cost x 0.5
SENS_COST_HIGH = 2.0       # cost x 2

# Binary floating point cannot represent 0.8 * 0.25 - 0.2 as exactly zero, so an
# exact break-even card lands at ~1e-17 rather than 0. Left alone, that residue
# would make n_req = 4*(sd/1e-17)^2 -- a number larger than the trade count of the
# universe. Anything inside this band IS zero for every purpose this engine has,
# and is snapped to zero so that the break-even card reports break-even.
EPS_ZERO = 1e-12

NA = None

ALGEBRA_NOTE = (
    "ALL QUANTITIES ARE IN R, where 1R is the money lost when the stop fires.\n"
    "  b     = tp / sl                     the payoff ratio (win / loss)\n"
    "  E     = p*b - (1-p)                 gross expectancy per trade, in R\n"
    "  E_net = E - c_R                     expectancy after cost, in R\n"
    "  b*    = (1-p) / p                   break-even payoff at this p\n"
    "  p*    = 1 / (1+b)                   break-even win rate at this b\n"
    "  edge  = p - p*                      win rate above the break-even rate\n"
    "  f*    = E / b                       Kelly fraction of capital\n"
    "  sd^2  = p*(b-E)^2 + (1-p)*(-1-E)^2  two-point std deviation, in R\n"
    "  n_req = 4 * (sd / |E|)^2            trades needed to see the edge at 2 sigma\n"
    "  L     = ceil( ln(N) / ln(1/(1-p)) ) expected longest losing streak in N\n"
    "  R_max = D_tol / (L * safety)        largest risk per trade a streak survives"
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
    return "{:,.{nd}f}".format(v, nd=nd)


def fmt_pct(v, nd=2):
    if v is NA:
        return "n/a"
    if isinstance(v, str):
        return v
    return "{:.{nd}f}%".format(v * 100.0, nd=nd)


def fmt_years(v):
    if v is NA:
        return "n/a"
    if isinstance(v, str):
        return v
    return "%.2f years" % v


def fmt_int_or_na(v):
    if v is NA:
        return "n/a"
    return str(v)


def jsonable(v):
    """Turn a value into something json.dumps can write, keeping `inf` explicit."""
    if v is NA:
        return None
    if isinstance(v, float):
        if math.isinf(v):
            return "inf"
        if math.isnan(v):
            return None
    return v


def safe_div(a, b):
    """None instead of ZeroDivisionError. The caller must then state a reason."""
    if b == 0 or b is NA or a is NA:
        return NA
    return a / b


class InputError(Exception):
    pass


# ---------------------------------------------------------------------------
# The core algebra. One function, so the CLI and the log path cannot diverge.
# ---------------------------------------------------------------------------

def longest_streak(n, p):
    """
    Expected longest run of CONSECUTIVE LOSSES in n trades, rounded UP.

        L = ceil( ln(n) / ln(1/(1-p)) )

    Ceil, not round: the raw value is the expected maximum, so rounding down
    would under-state the streak you must survive. The raw value is returned
    alongside so a reader can check the rounding for themselves.
    """
    if p is NA or n is NA:
        return NA, NA
    q = 1.0 - p
    if q <= 0.0:
        return 0, 0.0          # p = 1: a loss cannot happen
    if q >= 1.0:
        return n, float(n)     # p = 0: every trade is a loss
    raw = math.log(n) / math.log(1.0 / q)
    if raw < 0:
        raw = 0.0
    return int(math.ceil(raw)), raw


def payoff_profile(b, p, e_gross, sd, cost_r, n, d_tol_frac, safety,
                   trades_per_year):
    """
    Every derived field, from (b, p, E, sd, cost, n, tolerance, safety).

    Kept in one place so the CLI path and the log path report the same
    quantities with the same guards.
    """
    out = {}

    # Snap a floating-point residue to zero before anything divides by E. See EPS_ZERO.
    if e_gross is not NA and not isinstance(e_gross, str) and abs(e_gross) < EPS_ZERO:
        e_gross = 0.0

    out["b"] = b
    out["p"] = p
    out["E"] = e_gross
    out["cost_r"] = cost_r
    out["n"] = n

    out["E_net"] = NA if (e_gross is NA or cost_r is NA) else e_gross - cost_r
    if e_gross is not NA and cost_r is not NA and cost_r >= e_gross and e_gross > 0:
        out["cost_note"] = ("cost %s R >= gross E %s R: after cost this corner pays "
                            "nothing or loses. Cost is not a rounding term here; it "
                            "is the whole result."
                            % (fmt_num(cost_r), fmt_num(e_gross)))
    else:
        out["cost_note"] = NA

    # b* = (1-p)/p. Undefined at p = 0 (a payoff cannot rescue a book that
    # never wins); at p = 1 it is 0, which is the correct statement that any
    # positive payoff breaks even.
    out["b_star"] = NA if (p is NA or p == 0.0) else (1.0 - p) / p
    out["b_star_note"] = ("n/a: p = 0, no payoff breaks even at a zero win rate"
                          if (p is not NA and p == 0.0) else NA)

    # p* = 1/(1+b). b = 0 is legal (a trade that can only lose): p* = 1.
    out["p_star"] = NA if b is NA else safe_div(1.0, 1.0 + b)

    out["edge"] = NA if (p is NA or out["p_star"] is NA) else p - out["p_star"]

    # Kelly. A negative f* means do not bet; it is reported, not clipped,
    # because the sign is the information.
    out["kelly"] = NA if (e_gross is NA or b is NA or b == 0.0) else e_gross / b
    out["kelly_note"] = ("n/a: b = 0, there is no payoff to divide by"
                         if (b is not NA and b == 0.0) else NA)
    out["half_kelly"] = (NA if out["kelly"] is NA or isinstance(out["kelly"], str)
                         else out["kelly"] / 2.0)
    out["kelly_negative_note"] = (
        NA if (out["kelly"] is NA or isinstance(out["kelly"], str) or out["kelly"] >= 0)
        else ("f* is negative: the Kelly criterion says do not bet this corner at "
              "this p and b. A negative fraction is information, not a sizing "
              "instruction -- it is reported un-clipped."))

    # Standard error of the mean expectancy over the PLANNED sample. This is
    # the resolution of the measurement, not of a trade.
    out["sd"] = sd
    out["se_E"] = NA if (sd is NA or n is NA or n <= 0) else sd / math.sqrt(n)

    # n_req = 4*(sd/|E|)^2. Refused outright when E <= 0: there is no edge to
    # see, and a trade count cannot manufacture one.
    if e_gross is NA or sd is NA:
        out["n_req"] = NA
        out["n_req_int"] = NA
        out["n_req_note"] = "n/a: b, p or sd could not be computed"
    elif e_gross <= 0.0:
        out["n_req"] = NA
        out["n_req_int"] = NA
        out["n_req_note"] = ("n/a: E = %s <= 0. You cannot see an edge that is "
                             "not there, and no trade count creates one."
                             % fmt_num(e_gross))
    else:
        val = 4.0 * (sd / abs(e_gross)) ** 2
        out["n_req"] = val
        out["n_req_int"] = int(math.ceil(val))
        out["n_req_note"] = NA

    if out["n_req"] is NA or trades_per_year is NA or trades_per_year <= 0:
        out["years_at_pace"] = NA
        out["years_at_pace_note"] = (
            "n/a: needs a positive E and a positive --trades-per-year"
            if trades_per_year is NA or trades_per_year <= 0
            else "n/a: n_req is undefined")
    else:
        out["years_at_pace"] = out["n_req"] / float(trades_per_year)
        out["years_at_pace_note"] = NA

    L, L_raw = longest_streak(n, p)
    out["L_streak"] = L
    out["L_streak_raw"] = L_raw
    out["L_streak_note"] = (
        "p = 1: a losing trade cannot occur" if (p is not NA and p == 1.0)
        else ("p = 0: every trade is a loss" if (p is not NA and p == 0.0) else NA))

    # R_max = D_tol / (L * safety). L = 0 (p = 1) must not divide by zero.
    if L is NA or L <= 0 or d_tol_frac is NA or safety is NA or safety <= 0:
        out["R_max"] = NA
        out["R_max_note"] = ("n/a: L = 0 (the win rate leaves no losing streak to "
                             "survive)" if (L is not NA and L == 0)
                             else "n/a: streak survival is undefined here")
    else:
        out["R_max"] = d_tol_frac / (L * safety)
        out["R_max_note"] = NA
    out["d_tol_frac"] = d_tol_frac
    out["safety"] = safety

    # --- verdict -----------------------------------------------------------
    # MARGINAL means the mean expectancy cannot be separated from zero at the
    # PLANNED sample: |E_net| < se_E. This is the engine's stated rule.
    e_net = out["E_net"]
    if e_net is NA or out["se_E"] is NA or isinstance(out["se_E"], str):
        out["verdict"] = "INSUFFICIENT INPUT"
        out["verdict_reason"] = "E_net or se_E could not be computed"
    elif abs(e_net) < out["se_E"]:
        out["verdict"] = "MARGINAL"
        out["verdict_reason"] = ("|E_net| = %s < se_E = %s: the expectancy is "
                                 "within one standard error of zero at n = %s, "
                                 "so it is not separable from noise at this sample."
                                 % (fmt_num(abs(e_net)), fmt_num(out["se_E"]), out["n"]))
    elif e_net > 0.0:
        out["verdict"] = "POSITIVE"
        out["verdict_reason"] = ("E_net = %s >= se_E = %s: positive expectancy "
                                 "separable from zero at n = %s."
                                 % (fmt_num(e_net), fmt_num(out["se_E"]), out["n"]))
    else:
        out["verdict"] = "NEGATIVE"
        out["verdict_reason"] = ("E_net = %s <= -se_E = %s: negative expectancy "
                                 "separable from zero at n = %s."
                                 % (fmt_num(e_net), fmt_num(-out["se_E"]), out["n"]))
    return out


def check_from_tp_sl(tp, sl, p, cost_r, n, d_tol_pct, safety, trades_per_year):
    """
    Build a payoff profile from a target and a stop, both in R.

    sl = 0 is NOT an error to crash on: a zero stop means the loss is unbounded
    in R terms, so b and sd are refusals, and the engine says why.
    """
    notes = []

    if sl < 0 or tp < 0:
        raise InputError("--tp and --sl must be >= 0 (got tp=%s sl=%s)" % (tp, sl))
    if not (0.0 <= p <= 1.0):
        raise InputError("--p must be between 0 and 1 (got %s)" % p)
    if cost_r < 0:
        raise InputError("--cost-r must be >= 0 (got %s)" % cost_r)
    if n < 1:
        raise InputError("--n must be >= 1 (got %s)" % n)
    if not (0.0 < d_tol_pct < 100.0):
        raise InputError("--d-tol must be a percent between 0 and 100 (got %s)" % d_tol_pct)
    if safety <= 0:
        raise InputError("--safety must be > 0 (got %s)" % safety)

    if sl == 0.0:
        b = NA
        notes.append("b: n/a -- a stop of 0R means the loss is unbounded, so "
                     "there is no loss to put in the denominator.")
    else:
        b = tp / sl

    if b is NA:
        e_gross = NA
        sd = NA
        notes.append("E: n/a -- it follows b.")
    else:
        e_gross = p * b - (1.0 - p)
        # Two-point sd in units of the stop: loss = -1, win = +b.
        sd = math.sqrt(p * (b - e_gross) ** 2 + (1.0 - p) * (-1.0 - e_gross) ** 2)

    prof = payoff_profile(b, p, e_gross, sd, cost_r, n,
                          d_tol_pct / 100.0, safety, trades_per_year)
    prof["input_mode"] = "TP/SL"
    prof["r_basis"] = ("numeraire: 1R is the money lost when the stop fires; "
                       "--tp and --sl share a unit and b = tp/sl re-bases it")
    prof["tp"] = tp
    prof["sl"] = sl
    prof["notes"] = notes
    return prof


def check_from_credit(credit, width, tp_money, sl_money, p, cost_r, n,
                      d_tol_pct, safety, trades_per_year, multiplier):
    """
    --credit/--width mode.

    --credit and --width are quoted the way an option chain quotes them: PER
    SHARE (per contract, divided by the multiplier). --tp-money and --sl-money
    are PER SPREAD. The contract multiplier reconciles the two, so

        R (max loss, per spread) = (W - C) * multiplier
        b                        = tp_money / sl_money   (scale-free)

    The standard US equity-option multiplier is 100, which is why it defaults to
    100 rather than being assumed silently.
    """
    if width <= credit:
        raise InputError("--width (%s) must exceed --credit (%s): a spread with "
                         "no width has no max loss" % (width, credit))
    if credit <= 0:
        raise InputError("--credit must be > 0 (got %s)" % credit)
    if sl_money <= 0:
        raise InputError("--sl-money must be > 0 (got %s)" % sl_money)
    if tp_money < 0:
        raise InputError("--tp-money must be >= 0 (got %s)" % tp_money)
    if multiplier <= 0:
        raise InputError("--multiplier must be > 0 (got %s)" % multiplier)

    credit_money = credit * multiplier
    width_money = width * multiplier
    max_loss = (width - credit) * multiplier
    b = tp_money / sl_money
    e_gross = p * b - (1.0 - p)
    sd = math.sqrt(p * (b - e_gross) ** 2 + (1.0 - p) * (-1.0 - e_gross) ** 2)

    prof = payoff_profile(b, p, e_gross, sd, cost_r, n,
                          d_tol_pct / 100.0, safety, trades_per_year)
    prof["input_mode"] = "CREDIT/WIDTH"
    prof["r_basis"] = ("structural: 1R = the structure's max loss (W - C) x "
                       "multiplier = %s" % fmt_money(max_loss))
    prof["credit"] = credit
    prof["width"] = width
    prof["multiplier"] = multiplier
    prof["credit_money"] = credit_money
    prof["width_money"] = width_money
    prof["max_loss"] = max_loss
    prof["tp_money"] = tp_money
    prof["sl_money"] = sl_money
    prof["tp_pct_of_credit"] = safe_div(tp_money, credit_money)
    prof["sl_x_credit"] = safe_div(sl_money, credit_money)
    prof["notes"] = [
        "quote units: credit %s and width %s are PER SHARE; x multiplier %d "
        "gives %s credit and %s width per spread"
        % (fmt_money(credit), fmt_money(width), multiplier,
           fmt_money(credit_money), fmt_money(width_money)),
        "R basis: max loss = (width - credit) x multiplier = (%s - %s) x %d = %s"
        % (fmt_money(width), fmt_money(credit), multiplier, fmt_money(max_loss)),
        "target is %s of the credit; stop is %s x the credit"
        % (fmt_pct(safe_div(tp_money, credit_money)),
           fmt_num(safe_div(sl_money, credit_money), 2)),
    ]
    return prof


# ---------------------------------------------------------------------------
# Cost derivation
# ---------------------------------------------------------------------------

def derive_cost(fee_per_contract, legs, r_dollars):
    """
    cost_per_trade = fee_per_contract * legs * 2      (each leg is traded twice)
    c_R            = cost_per_trade / r_dollars

    Per-CONTRACT, per-LEG, round trip. The x2 is the round trip: an opening
    ticket and a closing ticket for every leg. A four-leg structure therefore
    pays eight tickets, not four.
    """
    out = {}
    out["fee_per_contract"] = fee_per_contract
    out["legs"] = legs
    out["tickets_round_trip"] = legs * 2
    out["cost_per_trade"] = fee_per_contract * legs * 2
    out["r_dollars"] = r_dollars
    out["cost_r"] = safe_div(out["cost_per_trade"], r_dollars)
    return out


def scaling_check(legs, fee_per_contract, rung_split, position_value):
    """
    Multi-rung scale-out fee threshold.

    Closing ONE rung pays one ticket per leg: rung_fee = legs * fee.
    Splitting into N rungs pays N rung fees; a single close pays one.
    A rung is FEE-NEGATIVE when the cash it banks is smaller than the fee it
    pays to bank it:  (position_value / N) < (legs * fee).
    Solving for the whole position:

        fee_negative iff   position_value  <  N * legs * fee_per_contract

    The extra cost over a single close is (N-1) * legs * fee -- and for a
    three-rung split of a four-leg structure that is exactly the round-trip fee
    of opening the structure in the first place.
    """
    fee_per_rung = legs * fee_per_contract
    total_fee = rung_split * fee_per_rung
    single_close_fee = fee_per_rung
    extra_fee = total_fee - single_close_fee
    banked_per_rung = safe_div(position_value, rung_split)
    threshold = rung_split * fee_per_rung
    delta = NA if banked_per_rung is NA else banked_per_rung - fee_per_rung
    return {
        "legs": legs,
        "fee_per_contract": fee_per_contract,
        "rung_split": rung_split,
        "position_value": position_value,
        "fee_per_rung": fee_per_rung,
        "fee_per_rung_formula": "legs * fee_per_contract = %d * %s = %s"
                                % (legs, fmt_money(fee_per_contract), fmt_money(fee_per_rung)),
        "total_fee": total_fee,
        "total_fee_formula": "rung_split * fee_per_rung = %d * %s = %s"
                             % (rung_split, fmt_money(fee_per_rung), fmt_money(total_fee)),
        "single_close_fee": single_close_fee,
        "extra_fee": extra_fee,
        "extra_fee_formula": "(rung_split - 1) * legs * fee = %d * %d * %s = %s"
                             % (rung_split - 1, legs, fmt_money(fee_per_contract),
                                fmt_money(extra_fee)),
        "banked_per_rung": banked_per_rung,
        "banked_per_rung_formula": "position_value / rung_split = %s / %d = %s"
                                   % (fmt_money(position_value), rung_split,
                                      fmt_money(banked_per_rung)),
        "threshold": threshold,
        "threshold_formula": "rung_split * legs * fee_per_contract = %d * %d * %s = %s"
                             % (rung_split, legs, fmt_money(fee_per_contract),
                                fmt_money(threshold)),
        "delta_per_rung": delta,
        "fee_negative": (NA if delta is NA else delta < 0.0),
    }


# ---------------------------------------------------------------------------
# Log reading and realised statistics
# ---------------------------------------------------------------------------

LOG_REQUIRED = ["trade_id", "open_date", "close_date", "pnl"]
LOG_OPTIONAL = ["risk", "cost", "setup", "symbol", "dte", "iv_rank", "side"]


def read_log(path):
    """Read the sibling engines' CSV schema. Comments beginning '# PROVENANCE:'
    are returned so they can be echoed into this engine's own output."""
    rows = []
    provenance = []
    comment_count = 0
    header = None
    with open(path, "r", encoding="utf-8", newline="") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.rstrip("\n").rstrip("\r")
            if line.strip() == "":
                continue
            if line.lstrip().startswith("#"):
                comment_count += 1
                body = line.lstrip().lstrip("#").strip()
                if body.upper().startswith("PROVENANCE:"):
                    provenance.append(body.split(":", 1)[1].strip())
                continue
            fields = next(csv.reader([line]))
            if header is None:
                header = [f.strip().lower() for f in fields]
                missing = [c for c in LOG_REQUIRED if c not in header]
                if missing:
                    raise InputError("line %d: log header is missing required "
                                     "column(s): %s" % (lineno, ", ".join(missing)))
                continue
            if len(fields) != len(header):
                raise InputError("line %d: %d fields, header has %d"
                                 % (lineno, len(fields), len(header)))
            rec = dict(zip(header, fields))
            try:
                rec["pnl_f"] = float(rec["pnl"])
            except ValueError:
                raise InputError("line %d: pnl %r is not a number" % (lineno, rec["pnl"]))
            rec["risk_f"] = NA
            if "risk" in header and rec.get("risk", "").strip() != "":
                try:
                    rec["risk_f"] = float(rec["risk"])
                except ValueError:
                    raise InputError("line %d: risk %r is not a number"
                                     % (lineno, rec["risk"]))
            rec["cost_f"] = 0.0
            if "cost" in header and rec.get("cost", "").strip() != "":
                try:
                    rec["cost_f"] = float(rec["cost"])
                except ValueError:
                    raise InputError("line %d: cost %r is not a number"
                                     % (lineno, rec["cost"]))
            rec["setup"] = (rec.get("setup", "") or "").strip() or "(untagged)"
            rows.append(rec)
    if header is None:
        raise InputError("no header row found in %s" % path)
    if not rows:
        raise InputError("no trade rows found in %s" % path)
    return rows, header, provenance, comment_count


def realised_cohort(rows, use_r_mode):
    """
    Realised p, b, E, sd for one cohort, in R units.

    break-even trades (pnl == 0) are counted in n, contribute 0 to expectancy,
    and are EXCLUDED from the win-rate denominator -- the convention the sibling
    engines already use.
    """
    n = len(rows)
    wins = [r for r in rows if r["pnl_f"] > 0.0]
    losses = [r for r in rows if r["pnl_f"] < 0.0]
    be = [r for r in rows if r["pnl_f"] == 0.0]

    def to_r(r):
        return r["pnl_f"] if not use_r_mode else r["pnl_f"] / r["risk_f"]

    def cost_r_of(r):
        return r["cost_f"] if not use_r_mode else r["cost_f"] / r["risk_f"]

    denom = len(wins) + len(losses)
    p_hat = safe_div(float(len(wins)), float(denom)) if denom > 0 else NA
    avg_win = safe_div(sum(to_r(r) for r in wins), float(len(wins))) if wins else NA
    avg_loss = safe_div(sum(abs(to_r(r)) for r in losses), float(len(losses))) if losses else NA
    b_hat = (NA if (avg_win is NA or avg_loss is NA or avg_loss == 0.0)
             else avg_win / avg_loss)
    e_hat = NA if (p_hat is NA or b_hat is NA) else p_hat * b_hat - (1.0 - p_hat)
    cost_hat = sum(cost_r_of(r) for r in rows) / float(n) if n else NA
    e_net_hat = NA if (e_hat is NA or cost_hat is NA) else e_hat - cost_hat

    sd_hat = NA
    if p_hat is not NA and b_hat is not NA and e_hat is not NA:
        sd_hat = math.sqrt(p_hat * (b_hat - e_hat) ** 2
                           + (1.0 - p_hat) * (-1.0 - e_hat) ** 2)

    # se of the win-rate estimate, and of the mean expectancy over n trades.
    se_p = NA
    if p_hat is not NA and denom > 0:
        se_p = math.sqrt(p_hat * (1.0 - p_hat) / denom)
    se_e = NA if (sd_hat is NA or n <= 0) else sd_hat / math.sqrt(n)

    total = sum(r["pnl_f"] - r["cost_f"] for r in rows)
    return {
        "n": n,
        "wins": len(wins),
        "losses": len(losses),
        "breakeven": len(be),
        "p": p_hat,
        "avg_win_R": avg_win,
        "avg_loss_R": avg_loss,
        "b": b_hat,
        "E": e_hat,
        "cost_r": cost_hat,
        "E_net": e_net_hat,
        "sd": sd_hat,
        "se_p": se_p,
        "se_E": se_e,
        "net_currency": total,
    }


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_provenance(path, provenance, n_trades, comment_count):
    lines = ["PROVENANCE", "  input file      : %s" % path,
             "  trade rows      : %d" % n_trades,
             "  comment lines   : %d" % comment_count]
    if provenance:
        for p in provenance:
            lines.append("  declared        : %s" % p)
    else:
        lines.append("  declared        : NONE -- the input declares no provenance.")
        lines.append("                    Tag the source of this log before using "
                     "any number below.")
    return lines


def render_core(prof, sensitivity):
    """The core panel. Every line shows its formula, so a reader can check it."""
    L = []
    L.append("R BASIS")
    L.append("  %s" % prof.get("r_basis", "n/a"))
    L.append("")
    L.append("ALGEBRA  (formulas are literal; substitute and check)")
    L.append(ALGEBRA_NOTE)
    L.append("")
    L.append("INPUTS")
    L.append("  input mode      : %s" % prof.get("input_mode", "n/a"))
    if prof.get("input_mode") == "CREDIT/WIDTH":
        L.append("  credit          : %s (per share)   width: %s (per share)   multiplier: %d"
                 % (fmt_money(prof["credit"]), fmt_money(prof["width"]),
                    int(prof["multiplier"])))
        L.append("  per spread      : credit %s   width %s   max loss (W-C): %s"
                 % (fmt_money(prof["credit_money"]), fmt_money(prof["width_money"]),
                    fmt_money(prof["max_loss"])))
        L.append("  target          : %s (%s of credit)   stop: %s (%s x credit)"
                 % (fmt_money(prof["tp_money"]), fmt_pct(prof["tp_pct_of_credit"]),
                    fmt_money(prof["sl_money"]), fmt_num(prof["sl_x_credit"], 2)))
    else:
        L.append("  tp / sl         : %s / %s  (both in R)"
                 % (fmt_num(prof.get("tp"), 4), fmt_num(prof.get("sl"), 4)))
    L.append("  p (win rate)    : %s" % fmt_pct(prof.get("p")))
    L.append("  cost            : %s R per trade (round trip)" % fmt_num(prof.get("cost_r")))
    L.append("  n (planned)     : %s" % fmt_int_or_na(prof.get("n")))
    L.append("  d-tol / safety  : %s of equity / %s x"
             % (fmt_pct(prof.get("d_tol_frac")), fmt_num(prof.get("safety"), 2)))
    L.append("")

    L.append("PAYOFF")
    L.append("  b       = tp/sl                  : %s" % fmt_num(prof.get("b")))
    L.append("  E       = p*b - (1-p)            : %s R per trade" % fmt_num(prof.get("E")))
    L.append("  E_net   = E - c_R                : %s R per trade" % fmt_num(prof.get("E_net")))
    L.append("")
    L.append("BREAK-EVEN")
    L.append("  b*      = (1-p)/p                : %s" % fmt_num(prof.get("b_star")))
    L.append("  p*      = 1/(1+b)                : %s" % fmt_pct(prof.get("p_star")))
    L.append("  edge    = p - p*                 : %s" % fmt_pct(prof.get("edge")))
    L.append("")
    L.append("SIZE")
    L.append("  f*      = E/b                    : %s of capital" % fmt_pct(prof.get("kelly")))
    L.append("  half-Kelly                       : %s of capital" % fmt_pct(prof.get("half_kelly")))
    L.append("")
    L.append("SAMPLE AND SURVIVAL")
    L.append("  sd      = sqrt(p(b-E)^2+(1-p)(-1-E)^2) : %s R" % fmt_num(prof.get("sd")))
    L.append("  se_E    = sd/sqrt(n)                   : %s R" % fmt_num(prof.get("se_E")))
    L.append("  n_req   = 4*(sd/|E|)^2                 : %s  (ceil: %s)"
             % (fmt_num(prof.get("n_req"), 2), fmt_int_or_na(prof.get("n_req_int"))))
    L.append("  years_at_pace = n_req / trades_per_year: %s"
             % fmt_years(prof.get("years_at_pace")))
    L.append("  L       = ceil(ln(n)/ln(1/(1-p)))      : %s trades  (raw: %s)"
             % (fmt_int_or_na(prof.get("L_streak")), fmt_num(prof.get("L_streak_raw"), 2)))
    L.append("  R_max   = d_tol/(L*safety)             : %s"
             % (fmt_pct(prof.get("R_max")) + " of equity per trade"
                if prof.get("R_max") is not NA else "n/a"))

    for key, label in (("b_star_note", "b*"), ("kelly_note", "f*"),
                       ("kelly_negative_note", "f*"), ("n_req_note", "n_req"),
                       ("years_at_pace_note", "years_at_pace"),
                       ("L_streak_note", "L"), ("R_max_note", "R_max"),
                       ("cost_note", "cost")):
        v = prof.get(key)
        if v is not NA:
            L.append("  NOTE %-14s: %s" % (label, v))
    for note in prof.get("notes", []):
        L.append("  INPUT NOTE      : %s" % note)

    L.append("")
    L.append("SENSITIVITY  (the cost of being wrong about an input)")
    L.append("  %-34s %12s %12s" % ("scenario", "E", "E_net"))
    for label, val, net in sensitivity:
        L.append("  %-34s %12s %12s" % (label, fmt_num(val), fmt_num(net)))
    L.append("")
    L.append("  dE/dp = b + 1 and dE/db = p, so a win-rate improvement is worth")
    L.append("  (b+1)/p times a payoff improvement. Payoff is a rules change you")
    L.append("  can make today; a win rate needs a signal. Fix the payoff first.")
    return L


def render_verdict(prof):
    L = []
    L.append("=" * 78)
    L.append("VERDICT")
    L.append("=" * 78)
    L.append("  RULE (this is the rule; argue with it if you disagree):")
    L.append("    |E_net| <  se_E  ->  MARGINAL  (not separable from zero)")
    L.append("    E_net   >= se_E  ->  POSITIVE")
    L.append("    E_net   <= -se_E ->  NEGATIVE")
    L.append("    se_E = sd / sqrt(n), with n the PLANNED sample.")
    L.append("")
    L.append("  %s: %s" % (prof.get("verdict", "n/a"), prof.get("verdict_reason", "")))
    L.append("")
    L.append("  This is arithmetic on YOUR inputs, not a forecast and not a")
    L.append("  backtest. It says what the corner pays if p and b are what you")
    L.append("  think they are. It cannot tell you whether they are.")
    return L


def render_cost_panel(cost):
    L = []
    L.append("=" * 78)
    L.append("COST DERIVATION  (per contract, per leg, round trip)")
    L.append("=" * 78)
    L.append("  cost_per_trade = fee_per_contract * legs * 2")
    L.append("                 = %s * %d * 2 = %s"
             % (fmt_money(cost["fee_per_contract"]), cost["legs"],
                fmt_money(cost["cost_per_trade"])))
    L.append("  tickets per round trip = legs * 2 = %d" % cost["tickets_round_trip"])
    L.append("  c_R            = cost_per_trade / R_dollars")
    L.append("                 = %s / %s = %s R"
             % (fmt_money(cost["cost_per_trade"]), fmt_money(cost["r_dollars"]),
                fmt_num(cost["cost_r"])))
    L.append("")
    L.append("  The x2 is the round trip: an OPENING ticket and a CLOSING ticket")
    L.append("  for every leg. A four-leg structure pays eight tickets, not four.")
    L.append("  Cost scales with legs AND with tickets; R does not.")
    return L


def render_scaling(sc):
    L = []
    L.append("=" * 78)
    L.append("SCALING CHECK  (multi-rung fee threshold)")
    L.append("=" * 78)
    L.append("  fee_per_rung   = %s" % sc["fee_per_rung_formula"])
    L.append("  banked_per_rung= %s" % sc["banked_per_rung_formula"])
    L.append("  total_fee      = %s" % sc["total_fee_formula"])
    L.append("  single close   = %s (one rung's worth of tickets)"
             % fmt_money(sc["single_close_fee"]))
    L.append("  extra_fee      = %s" % sc["extra_fee_formula"])
    L.append("")
    L.append("  THRESHOLD (derived, not asserted):")
    L.append("    a rung is fee-negative when  position_value / rung_split")
    L.append("    < legs * fee_per_contract. Solving for the whole position:")
    L.append("")
    L.append("      fee_negative  iff  position_value < %s" % sc["threshold_formula"])
    L.append("")
    L.append("    threshold = %s per spread. At position_value = %s the split is"
             % (fmt_money(sc["threshold"]), fmt_money(sc["position_value"])))
    if sc["fee_negative"] is NA:
        L.append("    %s." % "not assessable")
    elif sc["fee_negative"]:
        L.append("    FEE-NEGATIVE: each rung banks %s and pays %s, a shortfall of"
                 % (fmt_money(sc["banked_per_rung"]), fmt_money(sc["fee_per_rung"])))
        L.append("    %s per rung, %s across %d rungs."
                 % (fmt_money(abs(sc["delta_per_rung"])),
                    fmt_money(abs(sc["delta_per_rung"]) * sc["rung_split"]),
                    sc["rung_split"]))
    else:
        L.append("    FEE-POSITIVE: each rung banks %s and pays %s, clearing the "
                 "fee by %s per rung."
                 % (fmt_money(sc["banked_per_rung"]), fmt_money(sc["fee_per_rung"]),
                    fmt_money(sc["delta_per_rung"])))
    L.append("")
    L.append("  Note the shape of this: the threshold is paid per SPREAD, so a")
    L.append("  small structure crosses it never. Scaling rungs multiplies a fixed")
    L.append("  per-spread fee by the rung count while dividing the banked cash by")
    L.append("  the same count -- the fee ratio worsens by rung_split^2.")
    return L


def render_from_log(cohorts, use_r_mode, header, proposed):
    L = []
    L.append("=" * 78)
    L.append("REALISED  (from the log, by cohort)")
    L.append("=" * 78)
    L.append("  R MODE: %s" % ("yes -- risk column is the planned per-trade risk"
                                if use_r_mode
                                else "NO -- no usable risk column; every figure is "
                                     "in CURRENCY, not R, and is not comparable "
                                     "across cohorts"))
    L.append("  break-even trades (pnl = 0) are counted in n and EXCLUDED from the")
    L.append("  win-rate denominator: p = wins / (wins + losses).")
    L.append("")
    hdr = ("  %-28s %5s %5s %5s %4s %8s %8s %8s %9s %9s %10s"
           % ("setup", "n", "win", "los", "be", "p", "avg_win", "avg_los",
              "b", "E", "E_net"))
    L.append(hdr)
    L.append("  " + "-" * (len(hdr) - 2))
    for name, c in cohorts:
        L.append("  %-28s %5d %5d %5d %4d %8s %8s %8s %9s %9s %10s"
                 % (name[:28], c["n"], c["wins"], c["losses"], c["breakeven"],
                    fmt_pct(c["p"], 2), fmt_num(c["avg_win_R"], 3),
                    fmt_num(c["avg_loss_R"], 3), fmt_num(c["b"], 3),
                    fmt_num(c["E"], 4), fmt_num(c["E_net"], 4)))
    L.append("")
    L.append("  per cohort, with the sample the realised edge would need:")
    for name, c in cohorts:
        L.append("")
        L.append("  [%s]" % name)
        L.append("    se_p = sqrt(p(1-p)/n)          : %s  (p = %s, n_wl = %d)"
                 % (fmt_num(c["se_p"]), fmt_pct(c["p"], 2), c["wins"] + c["losses"]))
        L.append("    sd   = two-point sd            : %s R" % fmt_num(c["sd"]))
        L.append("    se_E = sd/sqrt(n)              : %s R" % fmt_num(c["se_E"]))
        if c["E"] is NA or c["sd"] is NA:
            nreq = "n/a: E or sd could not be computed"
        elif c["E"] <= 0.0:
            nreq = ("n/a: realised E = %s <= 0. There is no edge here to see, and "
                    "no trade count creates one." % fmt_num(c["E"]))
        else:
            nreq = "%s trades to see it at 2 sigma" % fmt_int_or_na(
                int(math.ceil(4.0 * (c["sd"] / abs(c["E"])) ** 2)))
        L.append("    n_req                          : %s" % nreq)
        L.append("    net P&L (pnl - cost)           : %s" % fmt_money(c["net_currency"]))
    if proposed is not None:
        pcard = proposed
        L.append("")
        L.append("=" * 78)
        L.append("PROPOSED CARD vs REALISED")
        L.append("=" * 78)
        L.append("  %-14s %12s %12s" % ("field", "proposed", "realised"))
        pooled = cohorts[-1][1] if cohorts else None
        rows = [("p", pcard.get("p"), pooled["p"] if pooled else NA),
                ("b", pcard.get("b"), pooled["b"] if pooled else NA),
                ("E", pcard.get("E"), pooled["E"] if pooled else NA),
                ("E_net", pcard.get("E_net"), pooled["E_net"] if pooled else NA),
                ("sd", pcard.get("sd"), pooled["sd"] if pooled else NA)]
        for label, a, b_ in rows:
            L.append("  %-14s %12s %12s" % (label, fmt_num(a), fmt_num(b_)))
        L.append("")
        L.append("  A gap between these two columns is the whole point of running")
        L.append("  --from-log: a card is a prediction, and this is the score.")
    return L


def render_csv(cohorts):
    lines = ["setup,n,wins,losses,breakeven,p,avg_win_R,avg_loss_R,b,E,cost_r,E_net,sd,se_E,net_currency"]
    for name, c in cohorts:
        lines.append(",".join([
            name, str(c["n"]), str(c["wins"]), str(c["losses"]), str(c["breakeven"]),
            fmt_num(c["p"], 6), fmt_num(c["avg_win_R"], 6), fmt_num(c["avg_loss_R"], 6),
            fmt_num(c["b"], 6), fmt_num(c["E"], 6), fmt_num(c["cost_r"], 6),
            fmt_num(c["E_net"], 6), fmt_num(c["sd"], 6), fmt_num(c["se_E"], 6),
            fmt_money(c["net_currency"], 2),
        ]))
    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args(argv):
    ap = argparse.ArgumentParser(
        prog="payoff_check.py",
        description="Will this options strategy make money? Payoff arithmetic "
                    "before capital is risked.",
        add_help=True,
    )
    ap.add_argument("--tp", type=float, default=None, help="target in R")
    ap.add_argument("--sl", type=float, default=1.0, help="stop in R (default 1.0)")
    ap.add_argument("--p", type=float, default=None, help="expected win rate, 0..1")
    ap.add_argument("--cost-r", type=float, default=0.0, dest="cost_r",
                    help="cost per trade in R, round trip (default 0)")
    ap.add_argument("--n", type=int, default=DEFAULT_N, help="planned trades (default 250)")
    ap.add_argument("--d-tol", type=float, default=DEFAULT_D_TOL_PCT, dest="d_tol",
                    help="drawdown tolerance, percent of equity (default 20)")
    ap.add_argument("--safety", type=float, default=DEFAULT_SAFETY,
                    help="streak-survival safety multiple (default 1.5)")
    ap.add_argument("--trades-per-year", type=int, default=DEFAULT_TRADES_PER_YEAR,
                    dest="trades_per_year", help="trades per year (default 250)")
    ap.add_argument("--credit", type=float, default=None, help="credit per spread, money")
    ap.add_argument("--width", type=float, default=None, help="strike width, money")
    ap.add_argument("--tp-money", type=float, default=None, dest="tp_money",
                    help="target in money per spread (credit mode)")
    ap.add_argument("--sl-money", type=float, default=None, dest="sl_money",
                    help="stop in money per spread (credit mode)")
    ap.add_argument("--multiplier", type=float, default=100.0,
                    help="contract multiplier, reconciling per-share quotes with "
                         "per-spread money (default 100, the US equity-option standard)")
    ap.add_argument("--fee-per-contract", type=float, default=None, dest="fee",
                    help="commission + fees per contract per ticket")
    ap.add_argument("--legs", type=int, default=None, help="legs in the structure")
    ap.add_argument("--r-dollars", type=float, default=None, dest="r_dollars",
                    help="currency value of 1R, for the fee derivation")
    ap.add_argument("--scaling-check", action="store_true", dest="scaling",
                    help="print the multi-rung fee-negative threshold")
    ap.add_argument("--rung-split", type=int, default=DEFAULT_RUNG_SPLIT, dest="rung_split",
                    help="rungs in the scale-out (default 3)")
    ap.add_argument("--position-value", type=float, default=None, dest="position_value",
                    help="current mark of the whole structure, money per spread")
    ap.add_argument("--from-log", default=None, dest="from_log", help="CSV trade log")
    ap.add_argument("--setup", default=None, help="restrict --from-log to one cohort")
    ap.add_argument("--json", action="store_true", dest="as_json",
                    help="machine-readable output")
    ap.add_argument("--csv-out", default=None, dest="csv_out",
                    help="write the from-log cohort table to this file")
    ap.add_argument("--version", action="store_true")
    return ap.parse_args(argv)


def sensitivity_rows(prof, cost_r):
    """E and E_net under +/-5pp on p, +/-0.25 on b, and cost x0.5 / x2."""
    rows = []
    b = prof.get("b")
    p = prof.get("p")
    if b is NA or p is NA:
        return [("sensitivity: n/a (b or p undefined)", NA, NA)]

    def e_of(bb, pp):
        return pp * bb - (1.0 - pp)

    for dp in (-SENS_P_WINDOW, SENS_P_WINDOW):
        pp = min(max(p + dp, 0.0), 1.0)
        e = e_of(b, pp)
        rows.append(("p %+.0fpp -> %s" % (dp * 100, fmt_pct(pp, 1)), e, e - cost_r))
    for db in (-SENS_B_WINDOW, SENS_B_WINDOW):
        bb = max(b + db, 0.0)
        e = e_of(bb, p)
        rows.append(("b %+.2f -> %s" % (db, fmt_num(bb, 3)), e, e - cost_r))
    for mult in (SENS_COST_LOW, SENS_COST_HIGH):
        e = e_of(b, p)
        rows.append(("cost x%.1f -> %s R" % (mult, fmt_num(cost_r * mult)),
                     e, e - cost_r * mult))
    return rows


def main(argv=None):
    # Emit LF on every platform. The repository requires LF, and Python's default
    # text-mode translation would otherwise write CRLF to a redirected stdout on
    # Windows -- making an identical run produce a byte-different file.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(newline="\n")

    args = parse_args(argv if argv is not None else sys.argv[1:])

    if args.version:
        print("payoff_check.py %s" % ENGINE_VERSION)
        return 0

    do_scaling = args.scaling or (args.position_value is not None
                                  and args.fee is not None and args.legs is not None
                                  and args.p is None and args.from_log is None)
    do_cost = args.fee is not None and args.legs is not None and args.p is not None
    want_card = args.p is not None or args.credit is not None

    if not want_card and not do_scaling and not args.from_log:
        print("ERROR: nothing to check. Give --p (with --tp), or --credit/--width, "
              "or --scaling-check, or --from-log.", file=sys.stderr)
        return 2

    # --- cost derivation ---------------------------------------------------
    cost_r = args.cost_r
    cost_panel = NA
    if do_cost:
        r_dollars = args.r_dollars
        if r_dollars is None and args.credit is not None and args.width is not None:
            # In credit mode R is the structural max loss PER SPREAD, so the
            # per-share quote must be scaled by the contract multiplier before it
            # is divided into a per-spread fee. Without this the fee looks 100x
            # larger than it is.
            r_dollars = (args.width - args.credit) * args.multiplier
        if r_dollars is None:
            print("ERROR: --fee-per-contract needs --r-dollars (the currency value "
                  "of 1R), or --credit/--width so it can be derived as (W - C) x "
                  "multiplier.", file=sys.stderr)
            return 2
        if args.legs < 1:
            print("ERROR: --legs must be >= 1", file=sys.stderr)
            return 2
        cost_panel = derive_cost(args.fee, args.legs, r_dollars)
        cost_r = cost_panel["cost_r"]
        if cost_r is NA:
            print("ERROR: --r-dollars must be > 0", file=sys.stderr)
            return 2
        if cost_r > 1.0:
            print("WARNING: c_R = %s R per trade. A cost larger than the risk unit "
                  "itself is almost always a sizing error: the structure is too "
                  "small for the ticket count." % fmt_num(cost_r), file=sys.stderr)

    # --- the card ----------------------------------------------------------
    prof = NA
    try:
        if args.credit is not None or args.width is not None:
            if args.credit is None or args.width is None:
                raise InputError("--credit/--width mode needs BOTH --credit and --width")
            if args.tp_money is None or args.sl_money is None:
                raise InputError("--credit/--width mode needs --tp-money and --sl-money "
                                 "in money terms: the mapping is max loss = W - C, so "
                                 "b = tp_money / sl_money and the target and stop must "
                                 "be stated in money, not as percentages.")
            if args.p is None:
                raise InputError("--p is required in every mode")
            prof = check_from_credit(args.credit, args.width, args.tp_money,
                                     args.sl_money, args.p, cost_r, args.n,
                                     args.d_tol, args.safety, args.trades_per_year,
                                     args.multiplier)
        elif args.p is not None:
            if args.tp is None:
                raise InputError("--tp is required when --p is given (the target in R)")
            prof = check_from_tp_sl(args.tp, args.sl, args.p, cost_r, args.n,
                                    args.d_tol, args.safety, args.trades_per_year)
    except InputError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2

    # --- scaling -----------------------------------------------------------
    scaling_panel = NA
    if do_scaling:
        if args.fee is None or args.legs is None:
            print("ERROR: --scaling-check needs --fee-per-contract and --legs",
                  file=sys.stderr)
            return 2
        if args.position_value is None:
            print("ERROR: --scaling-check needs --position-value (the current mark of "
                  "the whole structure, money per spread)", file=sys.stderr)
            return 2
        if args.rung_split < 2:
            print("ERROR: --rung-split must be >= 2 (1 is a single close, not a split)",
                  file=sys.stderr)
            return 2
        scaling_panel = scaling_check(args.legs, args.fee, args.rung_split,
                                      args.position_value)

    # --- from-log ----------------------------------------------------------
    cohorts = NA
    use_r_mode = False
    header = NA
    provenance = []
    comment_count = 0
    n_rows = NA
    if args.from_log:
        try:
            rows, header, provenance, comment_count = read_log(args.from_log)
        except (InputError, OSError) as e:
            print("ERROR: %s" % e, file=sys.stderr)
            return 2
        n_rows = len(rows)
        use_r_mode = ("risk" in header
                      and all(r["risk_f"] is not NA and r["risk_f"] > 0.0 for r in rows))
        if "cost" not in header:
            print("WARNING: the log has no `cost` column, so cost is 0 on every row "
                  "and every expectancy below is flattering.", file=sys.stderr)
        groups = {}
        for r in rows:
            groups.setdefault(r["setup"], []).append(r)
        if args.setup:
            if args.setup not in groups:
                print("ERROR: no cohort tagged %r. Cohorts present: %s"
                      % (args.setup, ", ".join(sorted(groups))), file=sys.stderr)
                return 2
            groups = {args.setup: groups[args.setup]}
        cohorts = [(name, realised_cohort(groups[name], use_r_mode))
                   for name in sorted(groups)]
        # Only add the pooled row when it says something the cohort rows do not.
        # With --setup the pool IS the selected cohort, and repeating it would let
        # the proposed-vs-realised panel compare a card against its own duplicate.
        if len(cohorts) > 1 and not args.setup:
            cohorts.append(("(ALL COHORTS)", realised_cohort(rows, use_r_mode)))
        if args.csv_out:
            with open(args.csv_out, "w", encoding="utf-8", newline="") as fh:
                fh.write("\n".join(render_csv(cohorts)) + "\n")

    # --- render ------------------------------------------------------------
    if args.as_json:
        payload = {
            "engine": "payoff_check.py",
            "engine_version": ENGINE_VERSION,
            "algebra": {
                "E": "p*b - (1-p)",
                "E_net": "E - c_R",
                "b_star": "(1-p)/p",
                "p_star": "1/(1+b)",
                "kelly": "E/b",
                "sd": "sqrt(p*(b-E)^2 + (1-p)*(-1-E)^2)",
                "n_req": "4*(sd/|E|)^2",
                "L": "ceil(ln(n)/ln(1/(1-p)))",
                "R_max": "d_tol/(L*safety)",
                "cost_per_trade": "fee_per_contract * legs * 2",
            },
            "r_basis": (prof.get("r_basis") if prof is not NA else NA),
            "card": ({k: jsonable(v) for k, v in prof.items()
                      if not isinstance(v, (list, dict))} if prof is not NA else NA),
            "sensitivity": ([{"scenario": scen, "E": jsonable(e_val),
                              "E_net": jsonable(e_net_val)}
                             for scen, e_val, e_net_val in sensitivity_rows(prof, cost_r)]
                            if prof is not NA else NA),
            "cost": ({k: jsonable(v) for k, v in cost_panel.items()
                      if not isinstance(v, (list, dict))}
                     if cost_panel is not NA else NA),
            "scaling": ({k: jsonable(v) for k, v in scaling_panel.items()
                         if not isinstance(v, (list, dict))}
                        if scaling_panel is not NA else NA),
            "from_log": (None if cohorts is NA else {
                "input": args.from_log,
                "provenance": provenance,
                "comments_total": comment_count,
                "rows": n_rows,
                "r_mode": use_r_mode,
                "cohorts": [{"setup": name,
                             **{k: jsonable(v) for k, v in c.items()}}
                            for name, c in cohorts],
            }),
        }
        print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True))
        return 0

    L = []
    L.append("=" * 78)
    L.append("OPTIONS PAYOFF CHECK  --  payoff_check.py %s" % ENGINE_VERSION)
    L.append("=" * 78)
    L.append("")
    if prof is not NA:
        sens = sensitivity_rows(prof, cost_r)
        L.extend(render_core(prof, sens))
        L.append("")
    if cost_panel is not NA:
        L.extend(render_cost_panel(cost_panel))
        L.append("")
    if scaling_panel is not NA:
        L.extend(render_scaling(scaling_panel))
        L.append("")
    if cohorts is not NA:
        L.extend(render_provenance(args.from_log, provenance, n_rows, comment_count))
        L.append("")
        L.extend(render_from_log(cohorts, use_r_mode, header, prof if prof is not NA else None))
        L.append("")
    if prof is not NA:
        L.extend(render_verdict(prof))
    else:
        L.append("=" * 78)
        L.append("VERDICT")
        L.append("=" * 78)
        L.append("  No card was supplied, so there is no verdict. A scaling check or")
        L.append("  a realised-cohort table answers a different question.")
    L.append("")
    L.append("=" * 78)
    L.append("PROVENANCE AND LIMITS")
    L.append("=" * 78)
    L.append("  This output is arithmetic on the inputs above. It is NOT market data,")
    L.append("  NOT a backtest, and NOT a forecast. No result here says a strategy is")
    L.append("  profitable; it says what a corner pays IF p and b are what you think")
    L.append("  they are, and p is an estimate with sampling error you have not")
    L.append("  measured. Sourced from CBOE and OCC exchange rules only for the")
    L.append("  mechanics of ticket counts and contract multipliers; no vendor, no")
    L.append("  network, no third-party dependency anywhere in this engine.")

    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
