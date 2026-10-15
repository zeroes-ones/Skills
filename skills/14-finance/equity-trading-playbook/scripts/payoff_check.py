#!/usr/bin/env python3
"""
payoff_check.py -- WILL THIS EQUITY PAYOFF CORNER MAKE MONEY?

Deterministic. Stdlib only. No network. No third-party imports.

THE QUESTION THIS ANSWERS
    "Will this equity strategy make money?" -- asked BEFORE capital is risked.
    The answer is four numbers on a card: the payoff ratio b, the expectancy
    E in R, the break-even win rate p* = 1/(1+b), and the cost drag c_R. If
    E_net is not positive, no amount of discipline makes the corner pay.

WHAT THIS ENGINE OWNS
    The R-unit payoff arithmetic for an equity or ETF card:
      b          = tp / sl                      (payoff ratio, in R)
      E          = p*b - (1-p)                   (expectancy per trade, in R)
      E_net      = E - c_R                       (the edge you actually keep)
      b*         = (1-p)/p                       (break-even payoff)
      p*         = 1/(1+b)                       (break-even win rate)
      f*         = E/b                           (Kelly fraction)
      sd^2       = p*(b-E)^2 + (1-p)*(-1-E)^2    (two-point sd, in R)
      n_req      = 4*(sd/|E|)^2                  (trades for a 2-sigma mean)
      L          ~ ln(n)/ln(1/(1-p))             (expected longest losing streak)
      R_max      = D_tol/(L*safety)              (risk per trade as % of equity)
      c_R        = round_trip_cost / R_dollars
    and the cohort view of a real ledger read with --from-log, which reports
    the R-unit statistic AND the currency-unit statistic side by side so that
    the contamination of p and b by position size is visible rather than
    argued about.

WHAT THIS ENGINE EXPLICITLY DOES NOT OWN
    Which stock to trade. That is `fundamental-analyst` (screening, valuation)
    and `technical-signals-engineer` (indicators, regime). The definition of
    the regime itself is `technical-signals-engineer` and `macro-strategist`.
    Whether to hold, trim, cut or rotate an OPEN position is
    `equity-position-lifecycle`. Margin, borrow, liquidity and concentration
    are `equity-risk-and-capital-engineer`. Position-sizing BANDS and ladders
    are `trade-sizing-recovery`, `portfolio-signal-manager` and
    `algorithmic-trader`. Expectancy measurement across a whole book, cohort
    attribution and the kill list are `edge-and-payoff-engineering`. This
    engine derives ONE risk-per-trade ceiling from streak survival and refuses
    to place it in a band; the band belongs to those skills.

    THIS ENGINE DOES NOT PROMISE A PROFIT. It identifies a positive-expectancy
    CONFIGURATION of an assumed p and b. The arithmetic can be right and the
    trade still lose money, because p is an estimate with sampling error and
    because the market can change while you are measuring it.

INPUT (--from-log)
    The sibling ledger schema, read BY COLUMN NAME, so a log written for
    `edge-and-payoff-engineering` / `timeframe-performance-statistics` is read
    here without alteration:

        trade_id,close_date,pnl              required (trade_id informational)
        risk, cost, setup, symbol, open_date optional

      * `pnl` is the REALISED P&L of one CLOSED trade; GROSS of `cost`.
      * `risk` is the PLANNED per-trade risk in currency (1R). If absent, or
        non-positive on any row, the log is read in CURRENCY MODE and every
        R-unit field is reported as n/a -- the engine refuses to invent a
        denominator.
      * `cost` is commission + fees + spread for that trade. Absent -> 0, and
        a zero-cost warning fires.
      * `setup` is the cohort key. Absent -> one cohort named `(none)`.
      * Lines beginning with `#` are comments. A `# PROVENANCE:` comment is
        echoed into this engine's own output so an output cannot be detached
        from the label of the data behind it.

USAGE
    py -3 scripts/payoff_check.py --tp 3.0 --sl 1.0 --p 0.40
    py -3 scripts/payoff_check.py --tp 0.5 --sl 1.5 --p 0.62 --cost-r 0.02
    py -3 scripts/payoff_check.py --tp 2.0 --sl 1.0 --p 0.40 --cost-bps 5 --stop-pct 1.0
    py -3 scripts/payoff_check.py --tp 3.0 --sl 1.0 --p 0.40 \
        --atr 2.0 --atr-value 5.00 --price 50.00 --capital 100000
    py -3 scripts/payoff_check.py --from-log examples/logs/equity-book-synthetic.csv
    py -3 scripts/payoff_check.py --tp 3.0 --sl 1.0 --p 0.40 \
        --from-log examples/logs/equity-book-synthetic.csv

    --tp F              profit target in R. REQUIRED unless --from-log only.
    --sl F              stop distance in R. DEFAULT 1.0.
    --p F               expected win rate, 0..1. REQUIRED with --tp.
    --cost-r F          round-trip cost in R units. DEFAULT 0.
    --cost-bps F        round-trip commission+spread in basis points of
                        notional; with --stop-pct this DERIVES c_R.
    --stop-pct F        stop distance as a percent of price. DEFAULT 5.0.
    --n INT             trades in the evaluation window. DEFAULT 250.
    --d-tol F           drawdown tolerated before the method is abandoned,
                        in percent of equity. DEFAULT 20.
    --safety F          streak-survival safety multiple. DEFAULT 1.5.
    --trades-per-year F trades per year, for the pacing line. DEFAULT 250.
    --atr F             stop distance in ATR multiples (enables ATR sizing).
    --atr-value F       the ATR itself, in currency per share. Requires --atr.
    --price F           share price, to express the ATR stop as a percent.
    --capital F         account equity, for share-count sizing.
    --from-log FILE     read a closed-trade ledger and report per-setup
                        cohorts in R units, with the currency-unit statistic
                        beside it as the contamination control.
    --setup TAG         restrict --from-log to one cohort tag, and compare the
                        proposed card against that cohort explicitly.
    --json              machine-readable output
    --csv-out FILE      write the cohort table as CSV, one row per setup.
    --quiet             suppress the sensitivity block
    --version           print the engine version

EXIT CODES
    0  ran (whatever the verdict says)
    2  the input could not be read or parsed, or a required flag is missing
"""

import argparse
import csv
import json
import math
import os
import sys

ENGINE_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Named operating constants. These are choices, printed on every run so they
# can be argued with. Changing one changes the verdict.
# ---------------------------------------------------------------------------
MARGINAL_BAND_R = 0.20
"""A corner whose net expectancy is positive but below this many R per trade is
MARGINAL rather than POSITIVE. Why 0.20: at the 0.5%-1.0% risk-per-trade band
this skill's own streak rule usually produces, +0.20R is +0.10% to +0.20% of
equity per trade -- large enough to survive a cost estimate that is wrong by
half, small enough that a p estimated from 30 trades cannot separate it from
zero. Named so a reader who disagrees can move it and see the cards move."""

N_REQ_BASIS = "E_net"
"""n_req is computed from the edge you actually KEEP, not the gross corner. With
the default --cost-r 0 the two are identical and n_req = 4*(sd/E)^2 exactly as
the algebra is usually written; with cost > 0 the net figure is the honest one,
because cost is per trade and hits every trade in the sample."""

COST_INVARIANCE_NOTE = (
    "COST SHIFTS THE MEAN, NOT THE SPREAD. Net outcomes are (b - c_R) and "
    "(-1 - c_R), so sd^2 = p*(b-c_R-E_net)^2 + (1-p)*(-1-c_R-E_net)^2 reduces "
    "algebraically to the same p*(b-E)^2 + (1-p)*(-1-E)^2. A cost increase "
    "moves E down and leaves sd, and therefore n_req's numerator, where it was."
)

SD_GUARD_NOTE = (
    "sd is a TWO-POINT distribution sd -- it knows only {win at +b, loss at -1}. "
    "It is not the sample sd of your realised R-multiples, which is larger "
    "because real exits land between the two points. n_req derived from it is a "
    "FLOOR on the sample you need, never a target."
)

CONTAMINATION_NOTE = (
    "R UNITS OR NOTHING. A payoff ratio computed on currency P&L mixes sizing "
    "skill into entry skill: the numerator is the average of (R_multiple x risk) "
    "and so is the denominator, and the two do not cancel unless every trade "
    "risked the same amount. Convert to R before computing p and b. The "
    "--from-log table prints both views side by side so the gap is visible."
)


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def fnum(v, nd=6):
    """Fixed-point, or n/a for a missing number. inf is printed as inf."""
    if v is None:
        return "n/a"
    if isinstance(v, float):
        if math.isnan(v):
            return "n/a"
        if math.isinf(v):
            return "inf" if v > 0 else "-inf"
    return "{:,.{nd}f}".format(v, nd=nd)


def fsgn(v, nd=6):
    if v is None:
        return "n/a"
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return fnum(v, nd)
    return "{:+,.{nd}f}".format(v, nd=nd)


def fpct(v, nd=3):
    if v is None:
        return "n/a"
    return "{}%".format("{:,.{nd}f}".format(v, nd=nd))


def fmoney(v, nd=2):
    if v is None:
        return "n/a"
    return "${:,.{nd}f}".format(v, nd=nd)


def div(a, b):
    """Division that yields None instead of raising, for every guard path."""
    if b is None or a is None:
        return None
    if b == 0:
        return None
    return a / b


def safe_sqrt(v):
    if v is None or v < 0:
        return None
    return math.sqrt(v)


# ---------------------------------------------------------------------------
# THE CORE. One card in, one dict out. Every branch below exists because a
# caller supplied a degenerate card, and the engine must report a reason rather
# than raise or print a fabricated number.
# ---------------------------------------------------------------------------

def check_card(tp, sl, p, cost_r=0.0, n_window=250, d_tol_pct=20.0,
               safety=1.5, trades_per_year=250.0, cost_bps=None, stop_pct=None):
    """Compute the payoff card. Returns a flat dict of floats/strings/None."""
    out = {}
    notes = []

    out["tp_R"] = tp
    out["sl_R"] = sl
    out["p"] = p
    out["cost_r_given"] = cost_r
    out["n_window"] = n_window
    out["d_tol_pct"] = d_tol_pct
    out["safety"] = safety
    out["trades_per_year"] = trades_per_year

    # ---- guard: stop of zero R is not a stop ----
    if sl is None or sl <= 0:
        out["b"] = None
        out["b_note"] = "sl = {} R. A stop of 0R is not a stop: b = tp/sl is "\
                        "undefined and no payoff corner exists to evaluate."\
                        .format(fnum(sl))
        notes.append(out["b_note"])
    else:
        out["b"] = tp / sl
        out["b_note"] = "b = tp/sl = {}/{} = {}"\
                        .format(fnum(tp, 2), fnum(sl, 2), fnum(tp / sl))

    b = out["b"]

    # ---- cost in R ----
    if cost_bps is not None and stop_pct is not None and stop_pct > 0:
        derived = cost_bps / (100.0 * stop_pct)
        out["cost_r_derived"] = derived
        out["cost_r"] = cost_r if cost_r else derived
        out["cost_r_basis"] = ("derived from {} bps round trip at a {}% stop: "
                               "c_R = bps/(100*stop_pct) = {}/(100*{}) = {}"
                               ).format(fnum(cost_bps, 4), fnum(stop_pct, 4),
                                        fnum(cost_bps, 4), fnum(stop_pct, 4),
                                        fnum(derived))
        if cost_r:
            out["cost_r_basis"] += "  -- overridden by --cost-r {}"\
                                   .format(fnum(cost_r, 4))
    else:
        out["cost_r_derived"] = None
        out["cost_r"] = cost_r
        out["cost_r_basis"] = "c_R = --cost-r = {}".format(fnum(cost_r, 4))
    c_r = out["cost_r"]

    pv = out["p"]
    # ---- guard: p outside [0,1] is not a probability ----
    if pv is None or pv < 0.0 or pv > 1.0:
        out["E"] = None
        out["E_note"] = "p = {} is outside [0,1]. Not a probability; refusing "\
                        "to compute an expectancy from it.".format(fnum(pv))
        notes.append(out["E_note"])
    elif b is None:
        out["E"] = None
        out["E_note"] = "E needs b, and b is undefined (see b_note)."
    else:
        out["E"] = pv * b - (1.0 - pv)
        out["E_note"] = "E = p*b - (1-p) = {}*{} - {} = {}R"\
                        .format(fnum(pv, 6), fnum(b), fnum(1.0 - pv, 6),
                                fsgn(pv * b - (1.0 - pv)))
    E = out["E"]

    # ---- net expectancy ----
    if E is None or c_r is None:
        out["E_net"] = None
        out["E_net_note"] = "E_net needs E and c_R."
    else:
        out["E_net"] = E - c_r
        out["E_net_note"] = "E_net = E - c_R = {} - {} = {}R"\
                            .format(fsgn(E), fnum(c_r), fsgn(E - c_r))
    E_net = out["E_net"]

    # ---- break-even payoff and win rate ----
    if pv is not None and 0.0 < pv <= 1.0:
        out["b_star"] = (1.0 - pv) / pv
        out["b_star_note"] = "b* = (1-p)/p = {}/{} = {}"\
                             .format(fnum(1.0 - pv, 6), fnum(pv, 6),
                                     fnum(out["b_star"]))
    elif pv == 0.0:
        out["b_star"] = None
        out["b_star_note"] = ("b* = (1-0)/0 is undefined: with p = 0 no payoff "
                              "ratio breaks even.")
    else:
        out["b_star"] = None
        out["b_star_note"] = "b* needs p in (0, 1]."

    if b is not None:
        out["p_star"] = 1.0 / (1.0 + b)
        out["p_star_note"] = "p* = 1/(1+b) = 1/(1+{}) = {}"\
                             .format(fnum(b), fnum(out["p_star"]))
    else:
        out["p_star"] = None
        out["p_star_note"] = "p* needs b, and b is undefined (see b_note)."
    p_star = out["p_star"]

    # ---- edge in win-rate points ----
    if pv is not None and p_star is not None and 0.0 <= pv <= 1.0:
        out["edge"] = pv - p_star
        out["edge_note"] = "edge = p - p* = {} - {} = {} (win-rate points)"\
                           .format(fnum(pv, 6), fnum(p_star, 6),
                                   fsgn(pv - p_star))
    else:
        out["edge"] = None
        out["edge_note"] = "edge needs p and p*."

    # ---- Kelly ----
    if E is not None and b is not None and b > 0:
        out["kelly"] = E / b
        out["half_kelly"] = out["kelly"] / 2.0
        out["kelly_note"] = "f* = E/b = {}/{} = {}   (half-Kelly {})"\
                            .format(fsgn(E), fnum(b), fsgn(out["kelly"]),
                                    fsgn(out["half_kelly"]))
        if out["kelly"] <= 0:
            out["kelly_note"] += "  -- NEGATIVE: no fraction of the bankroll "\
                                 "is the right fraction of a negative edge."
    else:
        out["kelly"] = None
        out["half_kelly"] = None
        out["kelly_note"] = "Kelly needs E and a positive b."

    # ---- two-point sd ----
    if E is not None and b is not None and pv is not None and 0.0 <= pv <= 1.0:
        var = pv * (b - E) ** 2 + (1.0 - pv) * (-1.0 - E) ** 2
        out["sd_var"] = var
        out["sd"] = safe_sqrt(var)
        out["sd_note"] = ("sd^2 = p*(b-E)^2 + (1-p)*(-1-E)^2 = {}*({}-({}))^2 "
                          "+ {}*({}-({}))^2 = {}*{} + {}*{} = {}"
                          ).format(fnum(pv, 6), fnum(b), fsgn(E),
                                   fnum(1.0 - pv, 6), fnum(-1.0), fsgn(E),
                                   fnum(pv, 6), fnum((b - E) ** 2),
                                   fnum(1.0 - pv, 6), fnum((-1.0 - E) ** 2),
                                   fnum(var))
    else:
        out["sd_var"] = None
        out["sd"] = None
        out["sd_note"] = "sd needs b, E and p."
    sd = out["sd"]

    # ---- trades to a 2-sigma mean ----
    basis = E_net if (N_REQ_BASIS == "E_net") else E
    if sd is not None and basis is not None and basis > 0:
        out["n_req"] = 4.0 * (sd / basis) ** 2
        out["n_req_note"] = ("n_req = 4*(sd/|{}|)^2 = 4*({}/{})^2 = {} trades"
                             ).format(N_REQ_BASIS, fnum(sd), fnum(basis),
                                      fnum(out["n_req"], 3))
    else:
        out["n_req"] = None
        if basis is None:
            out["n_req_note"] = "n_req needs sd and a positive edge."
        else:
            out["n_req_note"] = ("n_req = n/a. {} = {}R is not positive, so no "
                                 "sample size moves the mean to +2 sigma; more "
                                 "trades carry you further from break-even, not "
                                 "closer.").format(N_REQ_BASIS, fsgn(basis))
    n_req = out["n_req"]

    # ---- pacing ----
    if n_req is not None and trades_per_year and trades_per_year > 0:
        out["years_at_pace"] = n_req / trades_per_year
        out["years_at_pace_note"] = "{} trades / {} per year = {} years"\
                                    .format(fnum(n_req, 3),
                                            fnum(trades_per_year, 1),
                                            fnum(out["years_at_pace"], 3))
    else:
        out["years_at_pace"] = None
        out["years_at_pace_note"] = "pacing needs n_req."

    # ---- expected longest losing streak ----
    if pv is not None and 0.0 < pv < 1.0 and n_window is not None and n_window > 1:
        ratio = 1.0 / (1.0 - pv)
        out["L"] = math.log(n_window) / math.log(ratio)
        out["L_note"] = ("L ~ ln(n)/ln(1/(1-p)) = ln({})/ln({}) = {}/{} = {} "
                         "consecutive losses").format(fnum(n_window, 1),
                                                      fnum(ratio, 6),
                                                      fnum(math.log(n_window)),
                                                      fnum(math.log(ratio)),
                                                      fnum(out["L"], 3))
    elif pv == 0.0 and n_window is not None and n_window > 0:
        out["L"] = float(n_window)
        out["L_note"] = ("p = 0: every one of the {} trades loses, so the "
                         "longest losing streak is {}.").format(n_window, n_window)
    elif pv == 1.0:
        out["L"] = 0.0
        out["L_note"] = "p = 1: nothing loses, so the longest losing streak is 0."
    else:
        out["L"] = None
        out["L_note"] = "L needs p in [0,1] and n >= 2."
    L = out["L"]

    # ---- risk per trade ceiling ----
    if L is not None and L > 0 and safety and safety > 0 and d_tol_pct is not None:
        out["R_max_pct"] = d_tol_pct / (L * safety)
        out["R_max_note"] = ("R_max = D_tol/(L*safety) = {}%/({}*{}) = {}% of "
                             "equity per trade").format(fnum(d_tol_pct, 4),
                                                        fnum(L, 3),
                                                        fnum(safety, 2),
                                                        fnum(out["R_max_pct"], 4))
    else:
        out["R_max_pct"] = None
        if pv == 1.0:
            out["R_max_note"] = ("L = 0 because p = 1: a card with no losing "
                                 "trade has no streak to survive. There is no "
                                 "streak-derived ceiling, which is a statement "
                                 "about the assumption, not about safety.")
        elif n_window is not None and n_window < 2:
            out["R_max_note"] = ("L = 0 because the window holds {} trade(s): "
                                 "with n = 1 there is no streak to size for. "
                                 "Use n >= 2.").format(n_window)
        else:
            out["R_max_note"] = ("R_max needs a positive L and a positive "
                                 "safety.")

    # ---- break-even cost ----
    if E is not None:
        out["cost_breakeven_R"] = E
        if E > 0:
            out["cost_breakeven_note"] = ("c_R* = E = {}R. At or above this "
                                          "round-trip cost in R the corner "
                                          "crosses zero regardless of p and b."
                                          ).format(fnum(E))
            if cost_bps is not None and cost_bps > 0:
                sp = cost_bps / (100.0 * E)
                out["stop_pct_breakeven"] = sp
                out["stop_pct_breakeven_note"] = (
                    "tightest break-even stop at {} bps round trip: "
                    "S* = bps/(100*E) = {}/(100*{}) = {}% of price. "
                    "Below this stop distance the corner is a net loser, "
                    "however good p and b look."
                ).format(fnum(cost_bps, 4), fnum(cost_bps, 4), fnum(E),
                         fnum(sp, 4))
            else:
                out["stop_pct_breakeven"] = None
                out["stop_pct_breakeven_note"] = ("supply --cost-bps and "
                                                  "--stop-pct to see the tightest "
                                                  "break-even stop distance.")
        else:
            out["cost_breakeven_R"] = None
            out["stop_pct_breakeven"] = None
            out["cost_breakeven_note"] = ("E <= 0, so there is no positive cost "
                                          "at which the corner breaks even. Cost "
                                          "only adds to the loss.")
    else:
        out["cost_breakeven_R"] = None
        out["stop_pct_breakeven"] = None
        out["cost_breakeven_note"] = "break-even cost needs E."

    # ---- verdict ----
    out["verdict"], out["verdict_note"] = _verdict(b, E_net, c_r, E, n_req)

    out["atr_block"] = None
    out["notes"] = notes
    return out


def _verdict(b, E_net, c_r, E, n_req):
    if b is None:
        return ("UNDEFINED",
                "b is undefined (sl = 0), so there is no payoff corner to "
                "judge.")
    if E_net is None:
        return ("UNDEFINED", "E_net could not be computed.")
    if E_net <= 0:
        why = []
        if E is not None and E <= 0:
            why.append("the corner is already negative before cost "
                       "(E = {}R)".format(fsgn(E)))
        if E is not None and E > 0 and c_r is not None and c_r >= E:
            why.append("cost alone consumes the edge: c_R = {}R against "
                       "E = {}R, so c_R* = {}R".format(fnum(c_r), fsgn(E),
                                                       fnum(E)))
        return ("NEGATIVE",
                "NEGATIVE. " + ("; ".join(why) if why else "E_net <= 0.") +
                ". Do NOT trade this card at this p. Either the payoff ratio or "
                "the win rate has to change; position size cannot rescue a "
                "negative expectancy, it only scales the loss.")
    if E_net < MARGINAL_BAND_R:
        return ("MARGINAL",
                "MARGINAL. E_net = {}R is positive but below the {}R band. "
                "n_req = {} trades, so a p estimated from a small sample cannot "
                "separate this from zero. Trade it small, or widen b, or do not "
                "trade it.".format(fsgn(E_net), fnum(MARGINAL_BAND_R, 2),
                                   fnum(n_req, 3) if n_req is not None else "n/a"))
    return ("POSITIVE",
            "POSITIVE. E_net = {}R per trade on the assumed card. This is a "
            "statement about the ASSUMED p and b, not about the market: run "
            "--from-log to see what your own record says, and read the "
            "sensitivity block before believing p to the point.".format(
                fsgn(E_net)))


# ---------------------------------------------------------------------------
# Sensitivity block
# ---------------------------------------------------------------------------

def sensitivity(tp, sl, p, cost_r, n_window, d_tol_pct, safety, trades_per_year):
    rows = []
    pv = None if p is None else p

    def card(tp2, sl2, p2, c2, label):
        c = check_card(tp2, sl2, p2, c2, n_window, d_tol_pct, safety,
                       trades_per_year)
        rows.append((label, tp2, sl2, p2, c2, c))

    if pv is not None:
        for delta, tag in ((-0.05, "p - 5pp"), (0.05, "p + 5pp")):
            p2 = pv + delta
            if 0.0 <= p2 <= 1.0:
                card(tp, sl, p2, cost_r, tag)
            else:
                rows.append((tag, tp, sl, p2, cost_r, None))
    if tp is not None and sl is not None and sl > 0:
        b = tp / sl
        for delta, tag in ((-0.25, "b - 0.25"), (0.25, "b + 0.25")):
            b2 = b + delta
            if b2 > 0:
                card(b2 * sl, sl, pv, cost_r, tag)
            else:
                rows.append((tag, b2 * sl, sl, pv, cost_r, None))
    if cost_r is not None:
        card(tp, sl, pv, cost_r * 0.5, "cost x0.5")
        card(tp, sl, pv, cost_r * 2.0, "cost x2")
    return rows


# ---------------------------------------------------------------------------
# Ledger reading (--from-log). Schema shared with edge-and-payoff-engineering
# and timeframe-performance-statistics; every column is read BY NAME.
# ---------------------------------------------------------------------------

REQUIRED_COLS = ("pnl",)
OPTIONAL_COLS = ("trade_id", "open_date", "close_date", "risk", "cost", "setup",
                 "symbol")


def read_log(path):
    """Return (rows, provenance, warnings). Raises SystemExit(2) on bad input."""
    rows = []
    provenance = []
    warnings = []
    header = None
    with open(path, "r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, start=1):
            line = raw.rstrip("\r\n")
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                if "PROVENANCE:" in stripped:
                    provenance.append(stripped.lstrip("# ").strip())
                continue
            if header is None:
                header = [c.strip().lower() for c in next(csv.reader([stripped]))]
                missing = [c for c in REQUIRED_COLS if c not in header]
                if missing:
                    sys.stderr.write(
                        "ERROR: {}:{}: required column(s) missing: {}. "
                        "Expected a header containing at least pnl; optional: "
                        "{}\n".format(path, lineno, ", ".join(missing),
                                      ", ".join(OPTIONAL_COLS)))
                    sys.exit(2)
                continue
            cells = next(csv.reader([stripped]))
            if len(cells) != len(header):
                sys.stderr.write(
                    "ERROR: {}:{}: {} field(s) against a {} column header. "
                    "Refusing to skip a row silently.\n"
                    .format(path, lineno, len(cells), len(header)))
                sys.exit(2)
            rec = dict(zip(header, [c.strip() for c in cells]))

            def num(key):
                v = rec.get(key)
                if v is None or v == "":
                    return None
                try:
                    return float(v)
                except ValueError:
                    sys.stderr.write(
                        "ERROR: {}:{}: column '{}' is not a number: {!r}\n"
                        .format(path, lineno, key, v))
                    sys.exit(2)

            pnl = num("pnl")
            if pnl is None:
                sys.stderr.write("ERROR: {}:{}: pnl is empty.\n"
                                 .format(path, lineno))
                sys.exit(2)
            rec["_pnl"] = pnl
            rec["_risk"] = num("risk")
            rec["_cost"] = num("cost") or 0.0
            rec["_lineno"] = lineno
            rows.append(rec)

    if header is None:
        sys.stderr.write("ERROR: {}: no header row found.\n".format(path))
        sys.exit(2)
    if not rows:
        sys.stderr.write("ERROR: {}: header found but no trade rows.\n"
                         .format(path))
        sys.exit(2)

    if "risk" not in header:
        warnings.append("no `risk` column: CURRENCY MODE. Every R-unit field "
                        "is reported n/a -- this engine will not invent a "
                        "denominator.")
    elif any(r["_risk"] is None or r["_risk"] <= 0 for r in rows):
        bad = [r["_lineno"] for r in rows
               if r["_risk"] is None or r["_risk"] <= 0]
        warnings.append("`risk` is absent or non-positive on line(s) {}: "
                        "CURRENCY MODE. Every R-unit field is reported n/a."
                        .format(", ".join(str(b) for b in bad)))
    if "cost" not in header:
        warnings.append("no `cost` column: every figure is GROSS of "
                        "commission, fees and spread. Zero cost is flattering; "
                        "supply `cost` before quoting a number.")
    return rows, provenance, warnings


def cohort_stats(rows):
    """One cohort: n, wins, losses, R-unit and currency-unit p/b/E."""
    n = len(rows)
    r_mode = all(r["_risk"] is not None and r["_risk"] > 0 for r in rows)
    wins = [r for r in rows if r["_pnl"] > 0]
    losses = [r for r in rows if r["_pnl"] < 0]
    denom = len(wins) + len(losses)
    p = (len(wins) / denom) if denom else None

    st = {
        "n": n, "wins": len(wins), "losses": len(losses),
        "breakeven": n - len(wins) - len(losses),
        "p": p,
    }

    total_risk = sum(r["_risk"] for r in rows) if r_mode else None
    total_cost = sum(r["_cost"] for r in rows)

    # ---- R-unit view ----
    if r_mode and wins and losses:
        rs = [r["_pnl"] / r["_risk"] for r in rows]
        rw = [r["_pnl"] / r["_risk"] for r in wins]
        rl = [r["_pnl"] / r["_risk"] for r in losses]
        avg_w = sum(rw) / len(rw)
        avg_l = sum(rl) / len(rl)
        b_r = (avg_w / abs(avg_l)) if avg_l != 0 else None
        st["avg_win_R"] = avg_w
        st["avg_loss_R"] = avg_l
        st["b_R"] = b_r
        st["E_R_sample"] = sum(rs) / len(rs)
        st["E_R_ratio"] = (p * b_r - (1.0 - p)) if (b_r is not None and p is not None) else None
        st["c_R"] = (total_cost / total_risk) if total_risk else None
        st["E_net_R"] = (st["E_R_sample"] - st["c_R"]) if st["c_R"] is not None else None
    else:
        for k in ("avg_win_R", "avg_loss_R", "b_R", "E_R_sample", "E_R_ratio",
                  "c_R", "E_net_R"):
            st[k] = None
    st["r_mode"] = r_mode

    # ---- currency view: the contamination control ----
    if wins and losses:
        cw = [r["_pnl"] for r in wins]
        cl = [r["_pnl"] for r in losses]
        c_avg_w = sum(cw) / len(cw)
        c_avg_l = sum(cl) / len(cl)
        b_c = (c_avg_w / abs(c_avg_l)) if c_avg_l != 0 else None
        st["avg_win_cur"] = c_avg_w
        st["avg_loss_cur"] = c_avg_l
        st["b_cur"] = b_c
        st["E_cur"] = (p * b_c - (1.0 - p)) if (b_c is not None and p is not None) else None
    else:
        for k in ("avg_win_cur", "avg_loss_cur", "b_cur", "E_cur"):
            st[k] = None
    st["pnl_gross"] = sum(r["_pnl"] for r in rows)
    st["pnl_net"] = st["pnl_gross"] - total_cost
    st["cost_total"] = total_cost
    st["total_risk"] = total_risk

    # ---- contamination flag: the two RATIO views disagree in SIGN ----
    # Compared like for like: both are expectancy in units of the AVERAGE LOSS,
    # so the only difference is the unit the payoff ratio was measured in.
    flag = ""
    if st["E_R_ratio"] is not None and st["E_cur"] is not None:
        if (st["E_R_ratio"] > 0) != (st["E_cur"] > 0):
            flag = ("CONTAMINATED: currency ratio view {} against R ratio view "
                    "{} -- opposite signs"
                    ).format(fsgn(st["E_cur"], 4), fsgn(st["E_R_ratio"], 4))
    elif not r_mode:
        flag = "CURRENCY MODE: no usable risk column, so the R control cannot run"
    st["flag"] = flag
    return st


def run_log(path, card_args=None, setup_filter=None):
    rows, provenance, warnings = read_log(path)

    if card_args is None:
        card_args = {}

    setups = []
    seen = {}
    for r in rows:
        key = r.get("setup") or "(none)"
        if key not in seen:
            seen[key] = []
            setups.append(key)
        seen[key].append(r)

    if setup_filter is not None:
        if setup_filter not in seen:
            sys.stderr.write(
                "ERROR: --setup {} is not a cohort tag in {}. Tags present: {}\n"
                .format(setup_filter, path, ", ".join(sorted(setups))))
            sys.exit(2)
        kept = seen[setup_filter]
        rows = kept
        seen = {setup_filter: kept}
        warnings = list(warnings) + [
            "--setup {}: pooled figures below describe ONLY this cohort; the "
            "rest of the ledger is excluded. The pooled row is not the book."
            .format(setup_filter)]

    book = cohort_stats(rows)
    cohorts = [(name, cohort_stats(seen[name])) for name in sorted(seen)]

    # ---- proposed card, if one was supplied ----
    proposed = None
    if card_args.get("tp") is not None and card_args.get("p") is not None:
        proposed = check_card(
            card_args.get("tp"), card_args.get("sl", 1.0), card_args["p"],
            card_args.get("cost_r", 0.0), card_args.get("n_window", 250),
            card_args.get("d_tol_pct", 20.0), card_args.get("safety", 1.5),
            card_args.get("trades_per_year", 250.0),
            card_args.get("cost_bps"), card_args.get("stop_pct"))

    return {
        "log": os.path.abspath(path),
        "setup_filter": setup_filter,
        "provenance": provenance,
        "warnings": warnings,
        "rows": len(rows),
        "cohorts": cohorts,
        "book": book,
        "proposed_card": proposed,
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

SEP = "=" * 78


def print_card(c, title="PAYOFF CARD"):
    print(SEP)
    print("{}: tp = {}R   sl = {}R   p = {}   cost = {}R   n = {}   safety = {}"
          .format(title, fnum(c["tp_R"], 2), fnum(c["sl_R"], 2),
                  fnum(c["p"], 4), fnum(c["cost_r"], 4),
                  fnum(c["n_window"], 0), fnum(c["safety"], 2)))
    print(SEP)
    print()
    print("PAYOFF ARITHMETIC (every line prints its own formula)")
    print("  payoff ratio b        : {}".format(fnum(c["b"])))
    print("      {}".format(c["b_note"]))
    print("  expectancy E          : {}"
          .format("n/a" if c["E"] is None else "{}R".format(fsgn(c["E"]))))
    print("      {}".format(c["E_note"]))
    print("  cost drag c_R         : {}R".format(fnum(c["cost_r"], 6)))
    print("      {}".format(c["cost_r_basis"]))
    print("  net expectancy E_net  : {}"
          .format("n/a" if c["E_net"] is None else "{}R".format(fsgn(c["E_net"]))))
    print("      {}".format(c["E_net_note"]))
    print("  break-even payoff b*  : {}".format(fnum(c["b_star"])))
    print("      {}".format(c["b_star_note"]))
    print("  break-even win rate p*: {}".format(fnum(c["p_star"])))
    print("      {}".format(c["p_star_note"]))
    print("  edge (p - p*)         : {}".format(fsgn(c["edge"])))
    print("      {}".format(c["edge_note"]))
    print("  Kelly f* / half       : {} / {}".format(fsgn(c["kelly"]),
                                                     fsgn(c["half_kelly"])))
    print("      {}".format(c["kelly_note"]))
    print()
    print("DISTRIBUTION AND SURVIVAL (in R units)")
    print("  two-point sd          : {}".format(fnum(c["sd"])))
    print("      {}".format(c["sd_note"]))
    print("  trades to a 2-sigma mean : {}".format(
        fnum(c["n_req"], 3) if c["n_req"] is not None else "n/a"))
    print("      {}".format(c["n_req_note"]))
    print("  years at pace         : {}".format(
        fnum(c["years_at_pace"], 3) if c["years_at_pace"] is not None else "n/a"))
    print("      {}".format(c["years_at_pace_note"]))
    print("  expected worst streak L  : {}".format(
        fnum(c["L"], 3) if c["L"] is not None else "n/a"))
    print("      {}".format(c["L_note"]))
    print("  R_max (risk/trade)    : {}".format(fpct(c["R_max_pct"], 4)))
    print("      {}".format(c["R_max_note"]))
    print("  break-even cost c_R*  : {}".format(
        fnum(c["cost_breakeven_R"]) if c["cost_breakeven_R"] is not None else "n/a"))
    print("      {}".format(c["cost_breakeven_note"]))
    if c.get("stop_pct_breakeven_note"):
        print("      {}".format(c["stop_pct_breakeven_note"]))
    print()
    print("  sd guard: {}".format(SD_GUARD_NOTE))
    print("  {}".format(COST_INVARIANCE_NOTE))
    print()
    print("VERDICT: {}".format(c["verdict"]))
    print("  {}".format(c["verdict_note"]))
    if c.get("atr_block"):
        print()
        print(c["atr_block"])
    print()


def print_sensitivity(c, rows):
    print("SENSITIVITY (one lever at a time; everything else held fixed)")
    print("  {:<12} {:>10} {:>10} {:>10} {:>12}  {:<10} {}".format(
        "lever", "b", "p", "c_R", "E_net(R)", "verdict", "n_req"))
    for label, tp2, sl2, p2, c2, cc in rows:
        if cc is None:
            print("  {:<12} {:>10} {:>10} {:>10} {:>12}  {:<10} {}".format(
                label, "n/a", fnum(p2, 4), fnum(c2, 4), "n/a", "OUT OF RANGE",
                "--"))
            continue
        print("  {:<12} {:>10} {:>10} {:>10} {:>12}  {:<10} {}".format(
            label, fnum(cc["b"], 3), fnum(cc["p"], 4), fnum(cc["cost_r"], 4),
            fsgn(cc["E_net"], 4), cc["verdict"],
            fnum(cc["n_req"], 3) if cc["n_req"] is not None else "n/a"))
    print("  Read the SIGN column, not the decimals: if `p - 5pp` is NEGATIVE, "
          "the card rests on a win rate you cannot miss by five points.")
    print()


def print_sizing(c, atr_mult, atr_value, price, capital, cost_bps):
    print("POSITION SIZING (--atr mode)")
    print("  stop distance per share = atr_mult * atr = {} * {} = {}"
          .format(fnum(atr_mult, 2), fmoney(atr_value), fmoney(atr_mult * atr_value)))
    stop_per_share = atr_mult * atr_value
    stop_pct = None
    if price and price > 0:
        stop_pct = 100.0 * stop_per_share / price
        print("  stop distance           = {}/{} = {} of price"
              .format(fmoney(stop_per_share), fmoney(price), fpct(stop_pct, 4)))
    rmax = c["R_max_pct"]
    print("  R_max                   = {} of equity".format(fpct(rmax, 4)))
    if capital and capital > 0 and rmax is not None:
        risk_dollars = capital * rmax / 100.0
        print("  risk dollars per R      = {}% * {} = {}"
              .format(fnum(rmax, 4), fmoney(capital), fmoney(risk_dollars)))
        shares = int(math.floor(risk_dollars / stop_per_share)) \
            if stop_per_share > 0 else None
        if shares is not None:
            print("  share count             = floor({}/{}) = {} shares"
                  .format(fmoney(risk_dollars), fmoney(stop_per_share), shares))
            if price and price > 0:
                notional = shares * price
                print("  position notional       = {} * {} = {}"
                      .format(shares, fmoney(price), fmoney(notional)))
                if cost_bps:
                    cost_d = notional * cost_bps / 10000.0
                    print("  round-trip cost @ {} bps = {} * {}/10000 = {}"
                          .format(fnum(cost_bps, 4), fmoney(notional),
                                  fnum(cost_bps, 4), fmoney(cost_d)))
    else:
        print("  supply --capital to turn R_max into dollars and a share count.")
    print("  This is a CEILING derived from streak survival, not a "
          "recommendation. The sizing BAND belongs to trade-sizing-recovery, "
          "portfolio-signal-manager and algorithmic-trader.")
    print()


def print_log(result):
    print(SEP)
    print("LEDGER VIEW (--from-log): {}".format(result["log"]))
    if result.get("setup_filter"):
        print("R BASIS: --setup {} -- only this cohort is included".format(
            result["setup_filter"]))
    print(SEP)
    for p_ in result["provenance"]:
        print("# {}".format(p_))
    if not result["provenance"]:
        print("# (no `# PROVENANCE:` line in the log -- this output is "
              "untagged and must not be quoted)")
    for w in result["warnings"]:
        print("# WARNING: {}".format(w))
    print()
    print("  rows read : {}".format(result["rows"]))
    print()

    book = result["book"]
    print("POOLED BOOK")
    print("  n = {}   wins = {}   losses = {}   break-even = {}   p = {}"
          .format(book["n"], book["wins"], book["losses"], book["breakeven"],
                  fnum(book["p"], 6)))
    print("  realised mean R-multiple  : {}R   (the truth; sample mean of pnl/risk)"
          .format(fsgn(book["E_R_sample"])))
    print("  cost drag c_R             : {}".format(fnum(book["c_R"], 6)))
    print("  net expectancy E_net      : {}R".format(fsgn(book["E_net_R"])))
    print("  b_R = {}   b_$ = {}   (contamination control)"
          .format(fnum(book["b_R"]), fnum(book["b_cur"])))
    print("  E_R_ratio = {}   E$_ratio = {}   (ratio views, same units)"
          .format(fsgn(book["E_R_ratio"]), fsgn(book["E_cur"])))
    if book["flag"]:
        print("  {}".format(book["flag"]))
    print("  gross P&L = {}   cost = {}   net P&L = {}"
          .format(fmoney(book["pnl_gross"]), fmoney(book["cost_total"]),
                  fmoney(book["pnl_net"])))
    print()

    print("COHORTS (one row per `setup` tag; sorted by name)")
    print("  {:<22} {:>4} {:>5} {:>8} {:>9} {:>9} {:>10} {:>10} {:>8} {:>10}".format(
        "setup", "n", "wins", "p", "b_R", "b_$", "E$_ratio", "E_R_ratio",
        "c_R", "E_net(R)"))
    for name, st in result["cohorts"]:
        print("  {:<22} {:>4} {:>5} {:>8} {:>9} {:>9} {:>10} {:>10} {:>8} {:>10}".format(
            name[:22], st["n"], st["wins"], fnum(st["p"], 4), fnum(st["b_R"], 4),
            fnum(st["b_cur"], 4), fsgn(st["E_cur"], 4), fsgn(st["E_R_ratio"], 4),
            fnum(st["c_R"], 5), fsgn(st["E_net_R"], 4)))
    print()
    print("  E_R_ratio and E$_ratio are the SAME statistic -- p*b - (1-p), in "
          "units of the average loss -- differing only in the unit b was "
          "measured in. E_net(R) is the realised mean R-multiple minus c_R, "
          "which is the truth; it equals E_R_ratio only when the average loss "
          "is exactly 1R.")
    print()
    for name, st in result["cohorts"]:
        if st["b_R"] is not None and st["b_cur"] is not None:
            gap = abs(st["b_cur"] - st["b_R"])
            if gap > 0.001:
                print("  {}: currency b = {} against R b = {} -- a gap of {}. "
                      "The gap IS the sizing, not the strategy."
                      .format(name, fnum(st["b_cur"], 4), fnum(st["b_R"], 4),
                              fnum(gap, 4)))
        if st["flag"]:
            print("  {}: {}".format(name, st["flag"]))
        if not st["r_mode"]:
            print("  {}: CURRENCY MODE -- risk column absent, non-positive or "
                  "zero on some row. No R control available for this cohort."
                  .format(name))
    print()
    print("  {}".format(CONTAMINATION_NOTE))
    print()

    if result["proposed_card"] is not None:
        print_card(result["proposed_card"],
                   title="PROPOSED CARD vs LEDGER")


# ---------------------------------------------------------------------------
# JSON
# ---------------------------------------------------------------------------

COHORT_CSV_COLS = [
    "setup", "n", "wins", "losses", "breakeven", "p", "r_mode",
    "b_R", "avg_win_R", "avg_loss_R", "E_R_sample", "E_R_ratio",
    "b_cur", "avg_win_cur", "avg_loss_cur", "E_cur",
    "c_R", "E_net_R", "total_risk", "cost_total", "pnl_gross", "pnl_net", "flag",
]


def write_cohort_csv(result, path):
    """Write the cohort table as CSV, one row per setup, in deterministic order."""
    def cell(name, st, col):
        v = name if col == "setup" else st.get(col)
        if v is None:
            return "n/a"
        if isinstance(v, bool):
            return "yes" if v else "no"
        if isinstance(v, float):
            return "{:.6f}".format(v)
        return v

    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(COHORT_CSV_COLS)
        for name, st in result["cohorts"]:
            w.writerow([cell(name, st, col) for col in COHORT_CSV_COLS])


def card_json(c):
    keep = [k for k in c if k not in ("notes", "atr_block")]
    return {k: c[k] for k in sorted(keep)}


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="payoff_check.py",
        description="Will this equity payoff corner make money? R-unit payoff "
                    "arithmetic, survival sizing and cost drag, before capital "
                    "is risked. Identifies a positive-expectancy CONFIGURATION; "
                    "it does not promise a profit.")
    ap.add_argument("--tp", type=float, default=None,
                    help="profit target in R (required unless --from-log only)")
    ap.add_argument("--sl", type=float, default=1.0, help="stop distance in R")
    ap.add_argument("--p", type=float, default=None, help="expected win rate 0..1")
    ap.add_argument("--cost-r", type=float, default=0.0, dest="cost_r",
                    help="round-trip cost in R units")
    ap.add_argument("--cost-bps", type=float, default=None, dest="cost_bps",
                    help="round-trip commission+spread in bps of notional")
    ap.add_argument("--stop-pct", type=float, default=5.0, dest="stop_pct",
                    help="stop distance as a percent of price (default 5.0)")
    ap.add_argument("--n", type=int, default=250, dest="n_window",
                    help="trades in the evaluation window (default 250)")
    ap.add_argument("--d-tol", type=float, default=20.0, dest="d_tol_pct",
                    help="drawdown tolerated, percent of equity (default 20)")
    ap.add_argument("--safety", type=float, default=1.5,
                    help="streak-survival safety multiple (default 1.5)")
    ap.add_argument("--trades-per-year", type=float, default=250.0,
                    dest="trades_per_year", help="pacing (default 250)")
    ap.add_argument("--atr", type=float, default=None, dest="atr_mult",
                    help="stop distance in ATR multiples")
    ap.add_argument("--atr-value", type=float, default=None, dest="atr_value",
                    help="the ATR itself, currency per share")
    ap.add_argument("--price", type=float, default=None, help="share price")
    ap.add_argument("--capital", type=float, default=None, help="account equity")
    ap.add_argument("--from-log", default=None, dest="from_log",
                    help="read a closed-trade ledger and print setup cohorts")
    ap.add_argument("--setup", default=None, dest="setup_filter",
                    help="restrict --from-log to one cohort tag")
    ap.add_argument("--csv-out", default=None, dest="csv_out",
                    help="write the cohort table as CSV, one row per setup")
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--quiet", action="store_true", help="suppress sensitivity")
    ap.add_argument("--version", action="store_true")
    args = ap.parse_args(argv)

    if args.version:
        print("payoff_check.py {}".format(ENGINE_VERSION))
        return 0

    # ---- ATR mode resolves the stop distance into a percent of price ----
    stop_pct = args.stop_pct
    atr_mult = args.atr_mult
    atr_value = args.atr_value
    if atr_mult is not None:
        if atr_value is None:
            sys.stderr.write("ERROR: --atr needs --atr-value (the ATR in "
                             "currency per share).\n")
            return 2
        if args.price and args.price > 0:
            stop_pct = 100.0 * (atr_mult * atr_value) / args.price
        else:
            stop_pct = None
            sys.stderr.write("NOTE: --atr without --price: the stop cannot be "
                             "expressed as a percent of price, so c_R cannot be "
                             "derived from --cost-bps.\n")
    elif atr_value is not None:
        sys.stderr.write("ERROR: --atr-value requires --atr.\n")
        return 2

    if args.from_log is None and (args.tp is None or args.p is None):
        sys.stderr.write("ERROR: a card needs --tp and --p. Supply both, or use "
                         "--from-log alone to read a ledger.\n")
        return 2
    if args.from_log is not None and not os.path.isfile(args.from_log):
        sys.stderr.write("ERROR: --from-log file not found: {}\n"
                         .format(args.from_log))
        return 2

    card = None
    sens = []
    if args.tp is not None and args.p is not None:
        card = check_card(args.tp, args.sl, args.p, args.cost_r, args.n_window,
                          args.d_tol_pct, args.safety, args.trades_per_year,
                          args.cost_bps,
                          stop_pct if stop_pct else None)
        card["atr_block"] = None
        if atr_mult is not None:
            import io as _io
            buf = _io.StringIO()
            _stdout = sys.stdout
            sys.stdout = buf
            try:
                print_sizing(card, atr_mult, atr_value, args.price, args.capital,
                             args.cost_bps)
            finally:
                sys.stdout = _stdout
            card["atr_block"] = buf.getvalue().rstrip("\n")
        if not args.quiet:
            sens = sensitivity(args.tp, args.sl, args.p, card["cost_r"],
                               args.n_window, args.d_tol_pct, args.safety,
                               args.trades_per_year)

    if args.setup_filter is not None and args.from_log is None:
        sys.stderr.write("ERROR: --setup requires --from-log.\n")
        return 2

    log_result = None
    if args.from_log is not None:
        log_result = run_log(args.from_log, {
            "tp": args.tp, "sl": args.sl, "p": args.p,
            "cost_r": card["cost_r"] if card else args.cost_r,
            "n_window": args.n_window, "d_tol_pct": args.d_tol_pct,
            "safety": args.safety, "trades_per_year": args.trades_per_year,
            "cost_bps": args.cost_bps,
            "stop_pct": stop_pct if stop_pct else None,
        }, setup_filter=args.setup_filter)
        if args.csv_out:
            write_cohort_csv(log_result, args.csv_out)
            if not args.as_json:
                print("cohort table written to {}".format(args.csv_out))
                print()

    if args.as_json:
        payload = {
            "engine": "payoff_check.py",
            "version": ENGINE_VERSION,
            "constants": {
                "MARGINAL_BAND_R": MARGINAL_BAND_R,
                "N_REQ_BASIS": N_REQ_BASIS,
                "cost_invariance_note": COST_INVARIANCE_NOTE,
                "sd_guard_note": SD_GUARD_NOTE,
                "contamination_note": CONTAMINATION_NOTE,
            },
            "card": card_json(card) if card else None,
            "sensitivity": [
                {"lever": lbl, "b": (None if cc is None else cc["b"]),
                 "p": p2, "cost_r": c2,
                 "E_net": (None if cc is None else cc["E_net"]),
                 "verdict": ("OUT OF RANGE" if cc is None else cc["verdict"]),
                 "n_req": (None if cc is None else cc["n_req"])}
                for lbl, _tp, _sl, p2, c2, cc in sens
            ],
            "log": None,
        }
        if log_result is not None:
            payload["log"] = {
                "path": log_result["log"],
                "setup_filter": log_result.get("setup_filter"),
                "provenance": log_result["provenance"],
                "warnings": log_result["warnings"],
                "rows": log_result["rows"],
                "book": {k: v for k, v in log_result["book"].items()},
                "cohorts": [{"setup": n, **{k: v for k, v in s.items()}}
                            for n, s in log_result["cohorts"]],
            }
        print(json.dumps(payload, indent=2, sort_keys=True,
                         default=lambda o: None))
        return 0

    if card is not None:
        print_card(card)
        if not args.quiet and sens:
            print_sensitivity(card, sens)
        if args.quiet:
            print("(--quiet: sensitivity block suppressed)")
            print()
    if log_result is not None:
        print_log(log_result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
