#!/usr/bin/env python3
"""
timeframe_stats.py -- PnL statistics by REVIEW TIMEFRAME.

Deterministic. Stdlib only. No network. No third-party imports.

THE QUESTION THIS ANSWERS
    At which review timeframe -- daily, weekly, biweekly, monthly, quarterly,
    half-yearly, yearly -- do this book's PnL statistics actually become
    trustworthy, and what do they say about beating losses?

WHAT THIS ENGINE OWNS
    Timeframe bucketing, and the significance (or insignificance) of each
    bucket's statistics.

WHAT THIS ENGINE EXPLICITLY DOES NOT OWN
    The DEFINITIONS of Sharpe, Sortino, Calmar, maximum drawdown and profit
    factor. Those belong to the `trade-performance-analyst` skill. This engine
    computes only the per-period versions it needs in order to compare
    timeframes, and it refuses to annualise a Sharpe or to state a risk-free
    rate, because those are the inputs that skill requires to be declared.

INPUT
    CSV with header:  trade_id,open_date,close_date,pnl[,risk][,symbol]
      * Dates are ISO YYYY-MM-DD.
      * `pnl` is the REALISED P&L in currency for one CLOSED trade; may be
        negative; may be zero.
      * `risk` is optional: the planned per-trade risk unit, so R-multiples
        can be derived downstream. Not used by this engine's maths.
      * `symbol` is optional.
      * Lines beginning with `#` are comments. A comment beginning
        `# PROVENANCE:` is echoed into this engine's own output, so that an
        output can never be separated from the label of the data behind it.

BUCKETING CONVENTION (stated once, used everywhere)
    A trade belongs to the bucket containing its CLOSE date. Not its open
    date. A trade opened in March and closed in April is an April trade.
      D   calendar day                     2026-03-04
      W   ISO week                        2026-W10
      2W  paired ISO weeks                2026-2W05
          -- pairs are anchored so that ODD ISO weeks start each pair, and the
             key is the ISO year + ordinal pair number of the anchor Monday.
      M   calendar month                  2026-03
      Q   calendar quarter                2026-Q1
      H   calendar half-year              2026-H1
      Y   calendar year                   2026

USAGE
    py -3 scripts/timeframe_stats.py --csv examples/logs/<log>.csv
    py -3 scripts/timeframe_stats.py --bucket M,Q --capital 250000 log.csv
    py -3 scripts/timeframe_stats.py --json log.csv
    py -3 scripts/timeframe_stats.py --csv-out periods.csv log.csv

    --capital N   starting equity, for return-based statistics
    --bucket B    one or more of D,W,2W,M,Q,H,Y (comma separated); default: all
    --json        machine-readable output
    --csv         append the per-period series as CSV blocks
    --csv-out F   write the per-period series (all buckets) to file F
    --periods     also print the human-readable per-period table
    --quiet       suppress the transposed summary table
    --version     print the engine version

EXIT CODES
    0  ran
    2  the input could not be read or parsed (message names the line)
"""

import argparse
import csv
import json
import math
import os
import re
import sys
from datetime import date, timedelta

ENGINE_VERSION = "1.0.0"

BUCKET_ORDER = ["D", "W", "2W", "M", "Q", "H", "Y"]

BUCKET_LABEL = {
    "D": "calendar day",
    "W": "ISO week",
    "2W": "paired ISO weeks (odd ISO week starts the pair)",
    "M": "calendar month",
    "Q": "calendar quarter",
    "H": "calendar half-year",
    "Y": "calendar year",
}

# Nominal period length in days. periods_per_year = 365.25 / period_days, so the
# month/quarter/half/year entries land on exactly 12 / 4 / 2 / 1 periods a year,
# while D / W / 2W are the literal calendar counts. Stated here because a reader
# is entitled to disagree with a choice they can see.
BUCKET_PERIOD_DAYS = {
    "D": 1.0,
    "W": 7.0,
    "2W": 14.0,
    "M": 30.4375,   # 365.25 / 12
    "Q": 91.3125,   # 365.25 / 4
    "H": 182.625,   # 365.25 / 2
    "Y": 365.25,
}

NA = None

# ---------------------------------------------------------------------------
# Verdict thresholds. These are the rule, not a preference. A reader who thinks
# they are wrong should change them and say so -- that is why they are named
# constants instead of being buried in the comparison.
# ---------------------------------------------------------------------------
MIN_PERIODS_FOR_VERDICT = 12
MIN_TRADES_PER_PERIOD_FOR_VERDICT = 5
T_STAT_NOISE_BAND = 2.0

DEPENDENCE_CAVEAT = (
    "DEPENDENCE CAVEAT -- these buckets are not independent tests. H literally "
    "contains the M periods, Q contains the M periods, Y contains them all; the "
    "same trades are re-aggregated, not resampled. A t-statistic computed across "
    "a bucket series is therefore a STABILITY INDICATOR for that book, not a "
    "significance test of an edge. Read n_eff next to n_periods: where the period "
    "P&L series is positively autocorrelated, the effective sample is smaller than "
    "the period count suggests, and the t-statistic above is optimistic."
)


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def fmt_money(v, nd=2):
    if v is None:
        return "n/a"
    if isinstance(v, str):
        return v
    if isinstance(v, float) and (math.isinf(v) or math.isnan(v)):
        return "inf" if v > 0 else ("-inf" if v < 0 else "n/a")
    return "{:,.{nd}f}".format(v, nd=nd)


def fmt_num(v, nd=4):
    if v is None:
        return "n/a"
    if isinstance(v, str):
        return v
    if isinstance(v, float) and (math.isinf(v) or math.isnan(v)):
        return "inf" if v > 0 else ("-inf" if v < 0 else "n/a")
    return "{:.{nd}f}".format(v, nd=nd)


def fmt_pct(v, nd=2):
    if v is None:
        return "n/a"
    if isinstance(v, str):
        return v
    return "{:.{nd}f}%".format(v * 100.0, nd=nd)


def jsonable(v):
    """Turn a value into something json.dumps can write, keeping `inf` explicit."""
    if v is None:
        return None
    if isinstance(v, float):
        if math.isinf(v):
            return "inf"
        if math.isnan(v):
            return None
    return v


def parse_amount(raw, line_no):
    """Parse a currency-ish number. Accepts 1,234.50  $1,234.50  (1,234.50)  -1234.5."""
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


# ---------------------------------------------------------------------------
# Bucketing
# ---------------------------------------------------------------------------

def bucket_key(bucket, d):
    """Return (sortable_key, human_label) for the bucket containing date `d`."""
    if bucket == "D":
        return d.isoformat(), d.isoformat()

    if bucket == "W":
        iso = d.isocalendar()
        key = "%04d-W%02d" % (iso[0], iso[1])
        return key, key

    if bucket == "2W":
        # Monday of this trade's week, then step back to the odd week that anchors
        # the pair. ISO weeks are odd/even by number within the ISO year.
        monday = d - timedelta(days=d.isoweekday() - 1)
        iso = monday.isocalendar()
        if iso[1] % 2 == 0:
            anchor = monday - timedelta(days=7)
            iso = anchor.isocalendar()
        else:
            anchor = monday
        ordinal = (iso[1] + 1) // 2
        key = anchor.isoformat()
        label = "%04d-2W%02d (from %s)" % (iso[0], ordinal, anchor.isoformat())
        return key, label

    if bucket == "M":
        key = "%04d-%02d" % (d.year, d.month)
        return key, key

    if bucket == "Q":
        key = "%04d-Q%d" % (d.year, (d.month - 1) // 3 + 1)
        return key, key

    if bucket == "H":
        key = "%04d-H%d" % (d.year, 1 if d.month <= 6 else 2)
        return key, key

    if bucket == "Y":
        key = "%04d" % d.year
        return key, key

    raise ValueError("unknown bucket %r" % bucket)


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def sample_sd(values):
    n = len(values)
    if n < 2:
        return NA
    m = sum(values) / n
    var = sum((v - m) ** 2 for v in values) / (n - 1)
    if var < 0:
        var = 0.0
    return math.sqrt(var)


def median(values):
    if not values:
        return NA
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2.0


def lag1_autocorr(xs):
    """Pearson lag-1 autocorrelation of a series. Returns (rho, reason_if_na)."""
    n = len(xs)
    if n < 3:
        return NA, "fewer than 3 periods"
    a = xs[:-1]
    b = xs[1:]
    ma = sum(a) / len(a)
    mb = sum(b) / len(b)
    sa = sum((v - ma) ** 2 for v in a)
    sb = sum((v - mb) ** 2 for v in b)
    if sa <= 0.0 or sb <= 0.0:
        return NA, "zero variance in a lagged sub-series"
    cov = sum((a[i] - ma) * (b[i] - mb) for i in range(len(a)))
    rho = cov / math.sqrt(sa * sb)
    if rho < -1.0:
        rho = -1.0
    if rho > 1.0:
        rho = 1.0
    return rho, None


def n_effective(n_periods, rho):
    """n_eff = n_periods * (1 - rho) / (1 + rho). Returns (n_eff, reason_if_na)."""
    if rho is NA or rho is None:
        return NA, "autocorrelation not computable"
    if n_periods < 2:
        return NA, "fewer than 2 periods"
    if rho >= 0.999 or rho <= -0.999:
        return NA, "rho too close to +/-1 for this formula"
    return n_periods * (1.0 - rho) / (1.0 + rho), None


def max_drawdown(series):
    """Peak-to-trough fall of a cumulative series, in currency, as a NEGATIVE number.

    The running equity starts at 0 (before the first period), and 0 is the initial
    peak -- so a loss in the very first period registers as a drawdown. Negative
    because it is a fall; the magnitude is the depth.
    """
    if not series:
        return NA
    peak = 0.0
    cum = 0.0
    worst = 0.0
    for v in series:
        cum += v
        if cum > peak:
            peak = cum
        dd = cum - peak
        if dd < worst:
            worst = dd
    return worst


def safe_div(a, b):
    if a is NA or b is NA:
        return NA
    if b == 0:
        return NA
    return a / b


def profit_factor(gross_profit, gross_loss):
    if gross_loss == 0:
        if gross_profit > 0:
            return float("inf")
        return NA
    return gross_profit / gross_loss


# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------

class InputError(Exception):
    pass


def read_log(path):
    """Return (trades, provenance, comment_count).

    `trades` is a list of dicts sorted by (close_date, trade_id). Comment lines
    beginning `# PROVENANCE:` are returned so the caller can echo them.
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
        raise InputError("no data rows in %s" % path)

    reader = csv.DictReader([l for _, l in data_lines])
    if reader.fieldnames is None:
        raise InputError("no CSV header in %s" % path)
    fieldnames = [f.strip() for f in reader.fieldnames]
    if "close_date" not in fieldnames:
        raise InputError(
            "%s: header must contain 'close_date' (got: %s)" % (path, ",".join(fieldnames)))
    if "pnl" not in fieldnames:
        raise InputError(
            "%s: header must contain 'pnl' (got: %s)" % (path, ",".join(fieldnames)))

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
        risk_raw = (row.get("risk") or "").strip()
        risk = parse_amount(risk_raw, line_no) if risk_raw else NA
        ticker = (row.get("symbol") or "").strip()
        tid = (row.get("trade_id") or "").strip() or "row%d" % line_no
        trades.append({
            "trade_id": tid,
            "open_date": opn,
            "close_date": close,
            "pnl": pnl,
            "risk": risk,
            "symbol": ticker,
            "line": line_no,
        })

    if not trades:
        raise InputError("%s: no parsable trade rows" % path)

    trades.sort(key=lambda t: (t["close_date"], t["trade_id"]))
    return trades, provenance, comments


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def aggregate_period(bucket, key, label, trades):
    pnls = [t["pnl"] for t in trades]
    n = len(pnls)
    gross_profit = sum(p for p in pnls if p > 0)
    gross_loss = -sum(p for p in pnls if p < 0)   # positive magnitude
    net = gross_profit - gross_loss
    wins = len([p for p in pnls if p > 0])
    losses = len([p for p in pnls if p < 0])
    breakeven = n - wins - losses
    decided = wins + losses
    win_rate = (wins / decided) if decided > 0 else NA
    avg_win = (gross_profit / wins) if wins > 0 else NA
    avg_loss = (gross_loss / losses) if losses > 0 else NA
    payoff = safe_div(avg_win, avg_loss)
    be_wr = (1.0 / (1.0 + payoff)) if payoff is not NA else NA
    edge = (win_rate - be_wr) if (win_rate is not NA and be_wr is not NA) else NA
    return {
        "bucket": bucket,
        "period": key,
        "period_label": label,
        "n_trades": n,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "net_pnl": net,
        "wins": wins,
        "losses": losses,
        "breakeven_trades": breakeven,
        "win_rate": win_rate,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "payoff_ratio": payoff,
        "expectancy_per_trade": net / n if n else NA,
        "profit_factor": profit_factor(gross_profit, gross_loss),
        "break_even_win_rate": be_wr,
        "edge": edge,
    }


def aggregate_bucket(bucket, trades, capital):
    """Bucket-level statistics: the per-period series plus the across-period answer."""
    grouped = {}
    labels = {}
    for t in trades:
        key, label = bucket_key(bucket, t["close_date"])
        grouped.setdefault(key, []).append(t)
        labels[key] = label

    period_keys = sorted(grouped.keys())
    periods = [aggregate_period(bucket, k, labels[k], grouped[k]) for k in period_keys]
    series = [p["net_pnl"] for p in periods]

    n_periods = len(periods)
    total_trades = sum(p["n_trades"] for p in periods)

    out = {
        "bucket": bucket,
        "bucket_label": BUCKET_LABEL[bucket],
        "n_periods": n_periods,
        "n_trades": total_trades,
        "first_period": period_keys[0] if period_keys else NA,
        "last_period": period_keys[-1] if period_keys else NA,
        "periods": periods,
    }

    if n_periods == 0:
        for f in ("mean_period_pnl", "median_period_pnl", "sd_period_pnl", "t_stat",
                  "period_sharpe", "trades_per_period", "se_win_rate",
                  "cumulative_pnl", "max_drawdown", "lag1_autocorrelation", "n_eff",
                  "win_rate", "payoff_ratio", "break_even_win_rate", "edge",
                  "avg_win", "avg_loss", "expectancy_per_trade", "profit_factor",
                  "gross_profit", "gross_loss", "wins", "losses", "breakeven_trades"):
            out[f] = NA
        out["periods_per_year"] = 365.25 / BUCKET_PERIOD_DAYS[bucket]
        out["n_eff_capped"] = NA
        out["n_eff_note"] = "no periods in this bucket"
        out["t_stat_note"] = "no periods in this bucket"
        out["autocorr_note"] = "no periods in this bucket"
        return out

    # --- across the periods of this bucket ---------------------------------
    mean_p = sum(series) / n_periods
    median_p = median(series)
    sd_p = sample_sd(series)
    ppy = 365.25 / BUCKET_PERIOD_DAYS[bucket]
    trades_per_period = total_trades / n_periods

    if n_periods < 2:
        t_stat = NA
        t_note = "n/a (a single period: no across-period variance exists)"
    elif sd_p is NA or sd_p == 0:
        t_stat = NA
        t_note = "n/a (zero standard deviation across periods)"
    else:
        t_stat = mean_p / (sd_p / math.sqrt(n_periods))
        t_note = ""

    if sd_p is NA or sd_p == 0:
        period_sharpe = NA
    else:
        period_sharpe = mean_p / sd_p

    rho, rho_reason = lag1_autocorr(series)
    neff, neff_reason = n_effective(n_periods, rho)
    if neff is NA:
        neff_capped = NA
        neff_note = "n/a (%s)" % neff_reason
    else:
        neff_capped = min(neff, float(total_trades)) if total_trades else neff
        if neff > total_trades:
            neff_note = ("raw formula gives %.2f, which exceeds the %d trades in the "
                         "bucket; capped at the trade count" % (neff, total_trades))
        else:
            neff_note = ""

    # --- pooled trade-level statistics (the "beat losses" test) -------------
    pnls = [t["pnl"] for t in trades]
    wins = len([p for p in pnls if p > 0])
    losses = len([p for p in pnls if p < 0])
    breakeven = len(pnls) - wins - losses
    gross_profit = sum(p for p in pnls if p > 0)
    gross_loss = -sum(p for p in pnls if p < 0)
    decided = wins + losses
    win_rate = (wins / decided) if decided > 0 else NA
    avg_win = (gross_profit / wins) if wins > 0 else NA
    avg_loss = (gross_loss / losses) if losses > 0 else NA
    payoff = safe_div(avg_win, avg_loss)
    be_wr = (1.0 / (1.0 + payoff)) if payoff is not NA else NA
    edge = (win_rate - be_wr) if (win_rate is not NA and be_wr is not NA) else NA
    se_wr = (math.sqrt(win_rate * (1.0 - win_rate) / decided)
             if (win_rate is not NA and decided > 0) else NA)

    out.update({
        "mean_period_pnl": mean_p,
        "median_period_pnl": median_p,
        "sd_period_pnl": sd_p,
        "t_stat": t_stat,
        "t_stat_note": t_note,
        "period_sharpe": period_sharpe,
        "trades_per_period": trades_per_period,
        "periods_per_year": ppy,
        "se_win_rate": se_wr,
        "cumulative_pnl": sum(series),
        "max_drawdown": max_drawdown(series),
        "lag1_autocorrelation": rho,
        "autocorr_note": "" if rho is not NA else ("n/a (%s)" % rho_reason),
        "n_eff": neff,
        "n_eff_capped": neff_capped,
        "n_eff_note": neff_note,
        "n_trades": total_trades,
        "wins": wins,
        "losses": losses,
        "breakeven_trades": breakeven,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "net_pnl": gross_profit - gross_loss,
        "win_rate": win_rate,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "payoff_ratio": payoff,
        "expectancy_per_trade": (gross_profit - gross_loss) / total_trades if total_trades else NA,
        "profit_factor": profit_factor(gross_profit, gross_loss),
        "break_even_win_rate": be_wr,
        "edge": edge,
    })

    # how many individual periods had a positive edge
    pos_edge = len([p for p in periods if p["edge"] is not NA and p["edge"] > 0])
    decidable = len([p for p in periods if p["edge"] is not NA])
    out["periods_positive_edge"] = pos_edge
    out["periods_with_decidable_edge"] = decidable

    # --- verdict-relevant flags -------------------------------------------
    out["verdict_failures"] = []
    if n_periods < MIN_PERIODS_FOR_VERDICT:
        out["verdict_failures"].append(
            "n_periods=%d < %d" % (n_periods, MIN_PERIODS_FOR_VERDICT))
    if trades_per_period < MIN_TRADES_PER_PERIOD_FOR_VERDICT:
        out["verdict_failures"].append(
            "trades_per_period=%.2f < %d" % (trades_per_period,
                                             MIN_TRADES_PER_PERIOD_FOR_VERDICT))
    if t_stat is NA:
        out["verdict_failures"].append("t_stat not computable")
    out["qualifies"] = len(out["verdict_failures"]) == 0
    if t_stat is NA:
        out["noise_flag"] = "t_stat not computable"
    elif abs(t_stat) < T_STAT_NOISE_BAND:
        out["noise_flag"] = "NOT DISTINGUISHABLE FROM NOISE"
    else:
        out["noise_flag"] = "beyond the +/-2 noise band"

    # --- the beat-losses test ---------------------------------------------
    if edge is NA or se_wr is NA:
        out["edge_test"] = "n/a"
        out["edge_test_detail"] = (
            "win rate or break-even win rate is not computable in this bucket "
            "(a bucket with no losing trades has no payoff ratio and therefore "
            "no break-even win rate)")
    elif edge > 2.0 * se_wr:
        out["edge_test"] = "PASS"
        out["edge_test_detail"] = (
            "edge of %.4f exceeds 2 x se_win_rate (%.4f), so the win rate is "
            "distinguishable from its break-even at roughly the 95%% level"
            % (edge, 2.0 * se_wr))
    else:
        out["edge_test"] = "FAIL"
        out["edge_test_detail"] = (
            "edge of %.4f is inside 2 x se_win_rate (%.4f): the win rate is NOT "
            "distinguishable from its own break-even. More periods will not fix "
            "this; more INDEPENDENT trades will."
            % (edge, 2.0 * se_wr))

    # --- optional return-based statistics ---------------------------------
    if capital:
        out["capital"] = capital
        out["cumulative_return_pct"] = 100.0 * out["cumulative_pnl"] / capital
        out["max_drawdown_pct"] = (100.0 * out["max_drawdown"] / capital
                                   if out["max_drawdown"] is not NA else NA)
        out["mean_period_return_pct"] = 100.0 * mean_p / capital
        out["annualised_return_simple_pct"] = 100.0 * mean_p * ppy / capital
        out["annualised_return_note"] = (
            "simple (not compounded) mean-period return x periods_per_year; shown "
            "only because --capital was supplied; annualising a short sample is a "
            "trap, not a result")
    return out


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------

def decide_verdict(buckets):
    eligible = [b for b in buckets if b["qualifies"]]
    if not eligible:
        return {
            "bucket": NA,
            "status": "INSUFFICIENT DATA",
            "reason": ("no bucket satisfies n_periods >= %d AND trades_per_period >= %d"
                       % (MIN_PERIODS_FOR_VERDICT, MIN_TRADES_PER_PERIOD_FOR_VERDICT)),
            "failures": {b["bucket"]: list(b["verdict_failures"]) for b in buckets},
        }
    eligible.sort(key=lambda b: (-abs(b["t_stat"]), BUCKET_ORDER.index(b["bucket"])))
    best = eligible[0]
    out = {
        "bucket": best["bucket"],
        "status": ("NOT DISTINGUISHABLE FROM NOISE"
                   if best["noise_flag"] == "NOT DISTINGUISHABLE FROM NOISE"
                   else "most reliable of the qualifying buckets"),
        "reason": ("highest |t_stat| (%.3f) among the %d bucket(s) satisfying "
                   "n_periods >= %d and trades_per_period >= %d"
                   % (best["t_stat"], len(eligible), MIN_PERIODS_FOR_VERDICT,
                      MIN_TRADES_PER_PERIOD_FOR_VERDICT)),
        "t_stat": best["t_stat"],
        "n_periods": best["n_periods"],
        "n_eff": best["n_eff"],
        "n_eff_capped": best["n_eff_capped"],
        "n_eff_note": best["n_eff_note"],
        "trades_per_period": best["trades_per_period"],
        "noise_flag": best["noise_flag"],
        "failures": {b["bucket"]: list(b["verdict_failures"])
                     for b in buckets if not b["qualifies"]},
        "also_eligible": [b["bucket"] for b in eligible[1:]],
    }
    return out


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_provenance(path, provenance, n_trades, comment_count):
    lines = []
    lines.append("PROVENANCE")
    lines.append("  input file      : %s" % path)
    lines.append("  trade rows      : %d" % n_trades)
    lines.append("  comment lines   : %d" % comment_count)
    if provenance:
        for p in provenance:
            lines.append("  declared        : %s" % p)
    else:
        lines.append("  declared        : NONE -- the input declares no provenance.")
        lines.append("                    Tag the source of this log before using "
                     "any number below.")
    return lines


def transposed_table(buckets, rows, capital):
    """rows: list of (label, key, kind). kind in {money, num, pct, int, raw, plain}."""
    SHORT = {
        "NOT DISTINGUISHABLE FROM NOISE": "NOISE (|t|<2)",
        "beyond the +/-2 noise band": "beyond +/-2",
        "t_stat not computable": "n/a",
    }
    headers = ["field"] + [b["bucket"] for b in buckets]
    cells = []
    for label, key, kind in rows:
        row = [label]
        for b in buckets:
            v = b.get(key)
            if kind == "money":
                row.append(fmt_money(v))
            elif kind == "num":
                row.append(fmt_num(v, 3))
            elif kind == "ratio":
                row.append(fmt_num(v, 4))
            elif kind == "pct":
                row.append(fmt_pct(v))
            elif kind == "int":
                row.append("n/a" if v is NA else str(v))
            else:
                cell = "n/a" if v is NA else str(v)
                row.append(SHORT.get(cell, cell))
        cells.append(row)

    label_w = max(len(r[0]) for r in cells)
    label_w = max(label_w, len("field"))
    col_w = []
    for ci in range(len(buckets)):
        w = len(headers[ci + 1])
        for r in cells:
            w = max(w, len(r[ci + 1]))
        col_w.append(w)

    def line(cells_row):
        parts = [cells_row[0].ljust(label_w)]
        for ci in range(len(buckets)):
            parts.append(cells_row[ci + 1].rjust(col_w[ci]))
        return "  " + "  ".join(parts).rstrip()

    out = [line(headers)]
    out.append("  " + "-" * (label_w + 2 * (len(buckets) - 1) + sum(col_w)))
    prev_group = None
    for (label, key, kind), r in zip(rows, cells):
        group = GROUP_OF.get(label)
        if group and group != prev_group:
            out.append("")
            out.append("  [%s]" % group)
            prev_group = group
        out.append(line(r))
    return out


GROUP_OF = {
    "n_periods": "coverage",
    "n_trades": "coverage",
    "trades_per_period": "coverage",
    "periods_per_year": "coverage",
    "first_period": "coverage",
    "last_period": "coverage",
    "gross_profit": "trade totals",
    "gross_loss": "trade totals",
    "net_pnl": "trade totals",
    "wins": "trade totals",
    "losses": "trade totals",
    "breakeven_trades": "trade totals",
    "win_rate": "trade totals",
    "avg_win": "trade totals",
    "avg_loss": "trade totals",
    "payoff_ratio": "trade totals",
    "expectancy_per_trade": "trade totals",
    "profit_factor": "trade totals",
    "break_even_win_rate": "beat losses",
    "edge": "beat losses",
    "se_win_rate": "beat losses",
    "2 x se_win_rate": "beat losses",
    "edge > 2 x se?": "beat losses",
    "periods_positive_edge": "beat losses",
    "mean_period_pnl": "across periods",
    "median_period_pnl": "across periods",
    "sd_period_pnl": "across periods",
    "t_stat": "across periods",
    "period_sharpe": "across periods",
    "cumulative_pnl": "across periods",
    "max_drawdown": "across periods",
    "lag1_autocorrelation": "across periods",
    "n_eff": "across periods",
    "n_eff_capped": "across periods",
    "verdict eligible": "verdict inputs",
    "noise flag": "verdict inputs",
    "capital (return basis)": "return basis (--capital)",
    "cumulative_return_pct": "return basis (--capital)",
    "max_drawdown_pct (of capital)": "return basis (--capital)",
    "annualised_return_simple_pct": "return basis (--capital)",
}


def summary_rows(capital):
    rows = [
        ("n_periods", "n_periods", "int"),
        ("n_trades", "n_trades", "int"),
        ("trades_per_period", "trades_per_period", "num"),
        ("periods_per_year", "periods_per_year", "num"),
        ("first_period", "first_period", "plain"),
        ("last_period", "last_period", "plain"),
        ("gross_profit", "gross_profit", "money"),
        ("gross_loss", "gross_loss", "money"),
        ("net_pnl", "net_pnl", "money"),
        ("wins", "wins", "int"),
        ("losses", "losses", "int"),
        ("breakeven_trades", "breakeven_trades", "int"),
        ("win_rate", "win_rate", "pct"),
        ("avg_win", "avg_win", "money"),
        ("avg_loss", "avg_loss", "money"),
        ("payoff_ratio", "payoff_ratio", "num"),
        ("expectancy_per_trade", "expectancy_per_trade", "money"),
        ("profit_factor", "profit_factor", "num"),
        ("break_even_win_rate", "break_even_win_rate", "pct"),
        ("edge", "edge", "pct"),
        ("se_win_rate", "se_win_rate", "ratio"),
        ("2 x se_win_rate", "_two_se", "ratio"),
        ("edge > 2 x se?", "edge_test", "plain"),
        ("periods_positive_edge", "periods_positive_edge", "plain"),
        ("mean_period_pnl", "mean_period_pnl", "money"),
        ("median_period_pnl", "median_period_pnl", "money"),
        ("sd_period_pnl", "sd_period_pnl", "money"),
        ("t_stat", "t_stat", "num"),
        ("period_sharpe", "period_sharpe", "ratio"),
        ("cumulative_pnl", "cumulative_pnl", "money"),
        ("max_drawdown", "max_drawdown", "money"),
        ("lag1_autocorrelation", "lag1_autocorrelation", "ratio"),
        ("n_eff", "n_eff", "num"),
        ("n_eff_capped", "n_eff_capped", "num"),
        ("verdict eligible", "_eligible", "plain"),
        ("noise flag", "noise_flag", "plain"),
    ]
    if capital:
        rows += [
            ("capital (return basis)", "capital", "money"),
            ("cumulative_return_pct", "cumulative_return_pct", "num"),
            ("max_drawdown_pct (of capital)", "max_drawdown_pct", "num"),
            ("annualised_return_simple_pct", "annualised_return_simple_pct", "num"),
        ]
    return rows


def enrich(buckets):
    for b in buckets:
        if b.get("se_win_rate") is not NA and b.get("se_win_rate") is not None:
            b["_two_se"] = 2.0 * b["se_win_rate"]
        else:
            b["_two_se"] = NA
        if b.get("qualifies"):
            b["_eligible"] = "yes"
        else:
            b["_eligible"] = "no" if b.get("n_periods") is not NA else "no"
    return buckets


def csv_for_bucket(b):
    cols = ["bucket", "period", "period_label", "n_trades", "gross_profit",
            "gross_loss", "net_pnl", "wins", "losses", "breakeven_trades",
            "win_rate", "avg_win", "avg_loss", "payoff_ratio",
            "expectancy_per_trade", "profit_factor", "break_even_win_rate",
            "edge", "cumulative_pnl", "drawdown_from_peak"]
    out = [",".join(cols)]
    cum = 0.0
    peak = 0.0
    for p in b["periods"]:
        cum += p["net_pnl"]
        if cum > peak:
            peak = cum
        dd = cum - peak
        vals = [
            b["bucket"], p["period"], p["period_label"], str(p["n_trades"]),
            fmt_money(p["gross_profit"]), fmt_money(p["gross_loss"]),
            fmt_money(p["net_pnl"]), str(p["wins"]), str(p["losses"]),
            str(p["breakeven_trades"]),
            ("%.6f" % p["win_rate"]) if p["win_rate"] is not NA else "",
            fmt_money(p["avg_win"]), fmt_money(p["avg_loss"]),
            fmt_num(p["payoff_ratio"], 6),
            fmt_money(p["expectancy_per_trade"]),
            fmt_num(p["profit_factor"], 6),
            ("%.6f" % p["break_even_win_rate"]) if p["break_even_win_rate"] is not NA else "",
            ("%.6f" % p["edge"]) if p["edge"] is not NA else "",
            fmt_money(cum), fmt_money(dd),
        ]
        out.append(",".join(vals))
    return out


def period_table(b):
    cols = ["period", "n", "gross_profit", "gross_loss", "net_pnl", "W", "L",
            "BE", "win_rate", "payoff", "P_factor", "be_win_rate", "edge",
            "cumulative", "dd_from_peak"]
    rows = []
    cum = 0.0
    peak = 0.0
    for p in b["periods"]:
        cum += p["net_pnl"]
        if cum > peak:
            peak = cum
        rows.append([
            p["period"], str(p["n_trades"]), fmt_money(p["gross_profit"]),
            fmt_money(p["gross_loss"]), fmt_money(p["net_pnl"]), str(p["wins"]),
            str(p["losses"]), str(p["breakeven_trades"]),
            fmt_pct(p["win_rate"], 2), fmt_num(p["payoff_ratio"], 3),
            fmt_num(p["profit_factor"], 3), fmt_pct(p["break_even_win_rate"], 2),
            fmt_pct(p["edge"], 2), fmt_money(cum), fmt_money(cum - peak),
        ])
    widths = [len(c) for c in cols]
    for r in rows:
        for i, v in enumerate(r):
            widths[i] = max(widths[i], len(v))

    def line(r):
        return "  " + "  ".join(r[i].ljust(widths[i]) for i in range(len(r))).rstrip()

    out = [line(cols), "  " + "-" * (sum(widths) + 2 * (len(cols) - 1))]
    for r in rows:
        out.append(line(r))
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args(argv):
    ap = argparse.ArgumentParser(
        prog="timeframe_stats.py",
        description="PnL statistics by review timeframe",
        add_help=True,
    )
    ap.add_argument("log", nargs="?", help="CSV trade log")
    ap.add_argument("--capital", type=float, default=None,
                    help="starting equity, for return-based statistics")
    ap.add_argument("--bucket", default=None,
                    help="one or more of D,W,2W,M,Q,H,Y (comma separated); default all")
    ap.add_argument("--json", action="store_true", dest="as_json",
                    help="machine-readable output")
    ap.add_argument("--csv", action="store_true", dest="as_csv",
                    help="append the per-period series as CSV blocks")
    ap.add_argument("--csv-out", default=None, dest="csv_out",
                    help="write the per-period series (all buckets) to this file")
    ap.add_argument("--periods", action="store_true",
                    help="also print the human-readable per-period table")
    ap.add_argument("--quiet", action="store_true", help="suppress the summary table")
    ap.add_argument("--version", action="store_true")
    return ap.parse_args(argv)


def main(argv=None):
    # Emit LF on every platform. The repository requires LF, and Python's default
    # text-mode translation would otherwise write CRLF to a redirected stdout on
    # Windows -- making an identical run produce a byte-different file.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(newline="\n")

    args = parse_args(argv if argv is not None else sys.argv[1:])

    if args.version:
        print("timeframe_stats.py %s" % ENGINE_VERSION)
        return 0

    if not args.log:
        print("ERROR: no input log given. Usage: timeframe_stats.py [options] <log.csv>",
              file=sys.stderr)
        return 2

    if args.bucket:
        wanted = [x.strip().upper() for x in args.bucket.split(",") if x.strip()]
        bad = [b for b in wanted if b not in BUCKET_ORDER]
        if bad:
            print("ERROR: --bucket must be one of %s (got: %s)"
                  % (",".join(BUCKET_ORDER), ",".join(bad)), file=sys.stderr)
            return 2
        chosen = [b for b in BUCKET_ORDER if b in wanted]
    else:
        chosen = list(BUCKET_ORDER)

    if args.capital is not None and args.capital <= 0:
        print("ERROR: --capital must be positive", file=sys.stderr)
        return 2

    try:
        trades, provenance, comment_count = read_log(args.log)
    except InputError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    except ValueError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2

    buckets = [aggregate_bucket(b, trades, args.capital) for b in chosen]
    enrich(buckets)
    verdict = decide_verdict(buckets)

    if args.csv_out:
        with open(args.csv_out, "w", encoding="utf-8", newline="") as fh:
            first = True
            for b in buckets:
                block = csv_for_bucket(b)
                if first:
                    fh.write("\n".join(block) + "\n")
                    first = False
                else:
                    fh.write("\n".join(block[1:]) + "\n")

    if args.as_json:
        payload = {
            "engine": "timeframe_stats.py",
            "engine_version": ENGINE_VERSION,
            "input": args.log,
            "capital": args.capital,
            "provenance": provenance,
            "comments_total": comment_count,
            "rows": len(trades),
            "bucketing_convention": "a trade belongs to the bucket containing its close_date",
            "close_date_min": trades[0]["close_date"].isoformat(),
            "close_date_max": trades[-1]["close_date"].isoformat(),
            "verdict": verdict,
            "verdict_rule": {
                "rank": "descending |t_stat|",
                "gate_periods": "n_periods >= %d" % MIN_PERIODS_FOR_VERDICT,
                "gate_trades": "trades_per_period >= %d" % MIN_TRADES_PER_PERIOD_FOR_VERDICT,
                "noise_band": "|t_stat| < %s" % T_STAT_NOISE_BAND,
            },
            "dependence_caveat": DEPENDENCE_CAVEAT,
            "buckets": [],
        }
        for b in buckets:
            d = {k: v for k, v in b.items()
                 if k not in ("periods",)}
            d = {k: (jsonable(v) if not isinstance(v, (dict, list)) else v)
                 for k, v in d.items()}
            d["periods"] = [
                {k: jsonable(v) for k, v in p.items()} for p in b["periods"]
            ]
            payload["buckets"].append(d)
        print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True))
        return 0

    L = []
    L.append("=" * 78)
    L.append("TIMEFRAME PnL STATISTICS  --  timeframe_stats.py %s" % ENGINE_VERSION)
    L.append("=" * 78)
    L.extend(render_provenance(args.log, provenance, len(trades), comment_count))
    L.append("")
    L.append("BUCKETING CONVENTION")
    L.append("  A trade belongs to the bucket containing its CLOSE date, never its")
    L.append("  open date. A trade opened in March and closed in April is an April")
    L.append("  trade. 2W pairs are anchored so that ODD ISO weeks start each pair.")
    L.append("  Close dates in this log span %s to %s."
             % (trades[0]["close_date"].isoformat(), trades[-1]["close_date"].isoformat()))
    L.append("")
    L.append("METRIC PROVENANCE")
    L.append("  The definitions of Sharpe, Sortino, Calmar, maximum drawdown and")
    L.append("  profit factor belong to the `trade-performance-analyst` skill. This")
    L.append("  engine computes per-period versions only, in order to compare")
    L.append("  timeframes. It does not redefine them, and it does NOT annualise a")
    L.append("  Sharpe: the lookback period, the return frequency and the risk-free")
    L.append("  rate are required inputs and none of them are guessed here.")
    L.append("")

    if not args.quiet:
        rows = summary_rows(args.capital)
        L.append("PER-BUCKET SUMMARY  (columns are timeframes; rows are every field)")
        if args.capital:
            L.append("  --capital %.2f supplied: return-based rows are on that basis."
                     % args.capital)
        L.append("")
        L.extend(transposed_table(buckets, rows, args.capital))
        L.append("")

    if args.periods:
        for b in buckets:
            L.append("PER-PERIOD SERIES -- %s (%s)" % (b["bucket"], b["bucket_label"]))
            L.append("")
            L.extend(period_table(b))
            L.append("")

    # --- verdict -----------------------------------------------------------
    L.append("=" * 78)
    L.append("VERDICT")
    L.append("=" * 78)
    L.append("  RULE (this is the rule; argue with it if you disagree):")
    L.append("    rank buckets by descending |t_stat|, but ONLY among buckets with")
    L.append("      n_periods        >= %d" % MIN_PERIODS_FOR_VERDICT)
    L.append("      trades_per_period >= %d" % MIN_TRADES_PER_PERIOD_FOR_VERDICT)
    L.append("    if no bucket qualifies: INSUFFICIENT DATA, and name the constraint")
    L.append("    that failed.")
    L.append("    any bucket with |t_stat| < %s is marked" % T_STAT_NOISE_BAND)
    L.append("      NOT DISTINGUISHABLE FROM NOISE")
    L.append("")
    if verdict["bucket"] is NA:
        L.append("  VERDICT: INSUFFICIENT DATA -- %s" % verdict["reason"])
        L.append("")
        L.append("  Constraint that failed, per bucket:")
        for b in buckets:
            if b["verdict_failures"]:
                L.append("    %-4s : %s" % (b["bucket"], "; ".join(b["verdict_failures"])))
            else:
                L.append("    %-4s : qualifies" % b["bucket"])
    else:
        L.append("  VERDICT: %s is the most reliable review timeframe for this book."
                 % verdict["bucket"])
        L.append("           %s" % verdict["reason"])
        L.append("           t_stat = %s over n_periods = %d; trades_per_period = %s"
                 % (fmt_num(verdict["t_stat"], 3), verdict["n_periods"],
                    fmt_num(verdict["trades_per_period"], 2)))
        L.append("           status: %s" % verdict["status"])
        L.append("")
        L.append("  CONFIDENCE IS CAPPED BY DEPENDENCE -- n_periods = %d, "
                 "n_eff = %s (capped: %s)"
                 % (verdict["n_periods"], fmt_num(verdict["n_eff"], 2),
                    fmt_num(verdict["n_eff_capped"], 2)))
        if verdict.get("n_eff_note"):
            L.append("           note: %s" % verdict["n_eff_note"])
        if verdict.get("also_eligible"):
            L.append("           other qualifying bucket(s), in |t_stat| order: %s"
                     % ", ".join(verdict["also_eligible"]))
        if verdict["failures"]:
            L.append("")
            L.append("  Buckets that did NOT qualify:")
            for k, v in verdict["failures"].items():
                L.append("    %-4s : %s" % (k, "; ".join(v)))
    L.append("")
    L.append("  Per-bucket noise band (|t_stat| < %s):" % T_STAT_NOISE_BAND)
    for b in buckets:
        L.append("    %-4s : %s" % (b["bucket"], b["noise_flag"]))
    L.append("")
    L.append("-" * 78)
    L.append(DEPENDENCE_CAVEAT)
    L.append("-" * 78)

    # --- beat losses -------------------------------------------------------
    L.append("")
    L.append("=" * 78)
    L.append("BEAT LOSSES TEST  (win_rate vs break_even_win_rate, per bucket)")
    L.append("=" * 78)
    L.append("  break_even_win_rate = 1 / (1 + payoff_ratio), with payoff_ratio =")
    L.append("  avg_win / avg_loss, both pooled across every trade in the bucket.")
    L.append("  win_rate is wins / (wins + losses): break-even trades are reported")
    L.append("  and EXCLUDED from the denominator.")
    L.append("")
    L.append("  NOTE: this test is bucketing-INVARIANT by construction. Every trade")
    L.append("  falls in exactly one period of every bucket, so the pooled win rate,")
    L.append("  payoff ratio and edge are identical in every column below. Reviewing")
    L.append("  the same book weekly instead of monthly cannot move this test. It")
    L.append("  moves the t_statistic, which is a different question.")
    L.append("")
    L.append("  %-4s %10s %10s %10s %10s %10s  %s"
             % ("bk", "win_rate", "be_wr", "edge", "se_wr", "2xse", "result"))
    for b in buckets:
        L.append("  %-4s %10s %10s %10s %10s %10s  %s"
                 % (b["bucket"], fmt_pct(b["win_rate"], 2),
                    fmt_pct(b["break_even_win_rate"], 2),
                    fmt_pct(b["edge"], 2), fmt_num(b["se_win_rate"], 4),
                    fmt_num(b["_two_se"], 4), b["edge_test"]))
    L.append("")
    for b in buckets:
        L.append("  %-4s %s" % (b["bucket"], b["edge_test_detail"]))
    L.append("")
    L.append("  A 'PASS' here is about the TRADE-LEVEL win rate, and it is a")
    L.append("  different question from the across-period t_statistic above. Neither")
    L.append("  one certifies the strategy; both are bounds on being fooled by it.")

    if args.as_csv:
        L.append("")
        L.append("=" * 78)
        L.append("PERIOD SERIES (CSV)  --  one block per bucket")
        L.append("=" * 78)
        for b in buckets:
            L.append("")
            L.append("# bucket=%s  %s  (%d period rows)"
                     % (b["bucket"], b["bucket_label"], b["n_periods"]))
            L.extend(csv_for_bucket(b))

    if args.capital:
        L.append("")
        L.append("RETURN-BASED NOTE")
        L.append("  --capital %.2f was supplied, so the return-based rows above are"
                 % args.capital)
        L.append("  on that basis. They are SIMPLE (not compounded) and they are only")
        L.append("  as honest as the capital figure you supplied: a starting equity")
        L.append("  that ignores deposits, withdrawals and concurrent positions makes")
        L.append("  every return figure below it fiction.")

    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
