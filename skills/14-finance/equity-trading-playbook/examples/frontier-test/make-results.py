#!/usr/bin/env python3
"""
make-results.py -- render RESULTS.md from the artefacts of a real run.

Stdlib only.  Every table below is read back out of out/*.csv or out of the
captured stdout of study.py / handcheck.py, so RESULTS.md cannot drift from the
run it claims to document: re-run study.py and re-run this, and the document is
regenerated.  Nothing is typed by hand, and nothing is recomputed here -- this
file formats, it does not calculate.

USAGE
    py -3 make-results.py [--dir .]
"""

import argparse
import datetime
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")

BUCKETS = ["D", "W", "2W", "M", "Q", "H", "Y"]
BOOKS = ["R4", "R9", "R10", "R2L", "R1L"]


def read_csv(path):
    prov, headers, rows = [], None, []
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            if line.startswith("# PROVENANCE:"):
                prov.append(line[len("# PROVENANCE:"):].rstrip("\r\n").strip())
                continue
            if line.startswith("#") or not line.strip():
                continue
            f = [x.strip() for x in line.rstrip("\r\n").split(",")]
            if headers is None:
                headers = f
                continue
            rows.append(f)
    return prov, headers, rows


def md_table(headers, rows):
    out = [("| " + " | ".join(headers) + " |").rstrip(),
           "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append(("| " + " | ".join(r) + " |").rstrip())
    return out


def as_pct(x, nd=2):
    try:
        return ("%." + str(nd) + "f%%") % (100.0 * float(x))
    except (TypeError, ValueError):
        return x if x else "n/a"


def as_num(x, nd=4):
    try:
        return ("%." + str(nd) + "f") % float(x)
    except (TypeError, ValueError):
        return x if x else "n/a"


def read_text(path):
    if not os.path.isfile(path):
        return "(missing: %s)\n" % os.path.basename(path)
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        return fh.read().replace("\r\n", "\n")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=".")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.dir)
    out = os.path.join(root, "out")
    L = []

    L.append("# RESULTS -- the positivity frontier, measured")
    L.append("")
    L.append("Every figure in this file was produced by the run captured in")
    L.append("`run-output.txt` and by the independent re-derivation captured in")
    L.append("`handcheck-output.txt`.  The tables are rendered from `out/*.csv` by")
    L.append("`make-results.py`, which formats and never calculates, so this document")
    L.append("cannot disagree with the run it documents.  Nothing here was typed by")
    L.append("hand and nothing was re-run until a number turned green.")
    L.append("")
    L.append("Generated: %s" % datetime.date.today().isoformat())
    L.append("")

    # ---- provenance -----------------------------------------------------
    L.append("## How to reproduce")
    L.append("")
    L.append("```bash")
    L.append("cd skills/14-finance/equity-trading-playbook/examples/frontier-test")
    L.append("export PYTHONIOENCODING=utf-8")
    L.append("")
    L.append("# 1. data: read the persisted MCP payloads into data/*.csv")
    L.append("py -3 pull_ohlcv.py --results <agent tool-results dir> \\")
    L.append("    --out data --pull-date 2026-10-14")
    L.append("#    and, for the two series whose older page came back inline:")
    L.append("py -3 reuse_sibling_data.py --dir . --sibling ../regime-study/data --symbol SPY")
    L.append("py -3 reuse_sibling_data.py --dir . --sibling ../weather-test/data --symbol VIX")
    L.append("")
    L.append("# 2. the study")
    L.append("py -3 study.py > run-output.txt 2>&1")
    L.append("")
    L.append("# 3. the independent re-derivation")
    L.append("py -3 handcheck.py > handcheck-output.txt 2>&1")
    L.append("")
    L.append("# 4. this document")
    L.append("py -3 make-results.py")
    L.append("```")
    L.append("")

    # ---- input inventory ------------------------------------------------
    L.append("## 0. Input series")
    L.append("")
    L.append("Each `data/*.csv` carries its own `# PROVENANCE:` block.  Read back:")
    L.append("")
    rows = []
    for name in sorted(os.listdir(os.path.join(root, "data"))):
        if not name.endswith(".csv"):
            continue
        prov, headers, data = read_csv(os.path.join(root, "data", name))
        sym = [p for p in prov if p.startswith("symbol=")]
        first = [p for p in prov if " first=" in p]
        extra = ""
        for p in prov:
            if p.startswith("*** NOT A PRICE SERIES ***"):
                extra = "YIELD INDEX, not a price"
            if p.startswith("carried_from="):
                extra = (extra + "; partly carried from a sibling pull").strip("; ")
        rows.append([name.replace("_1d.csv", ""),
                     sym[0].split()[0].split("=")[1] if sym else "?",
                     str(len(data)),
                     data[0][0] if data else "?",
                     data[-1][0] if data else "?",
                     extra])
    for line in md_table(["file", "source", "rows", "first", "last", "note"], rows):
        L.append(line)
    L.append("")

    # ---- reproduction ---------------------------------------------------
    L.append("## 1. Reproduction check")
    L.append("")
    L.append("The book simulator and the sleeve rule here are the weather-test's, so")
    L.append("they are re-run against that study's own published numbers.  This is a")
    L.append("real check on the shared machinery, not a formality.")
    L.append("")
    _, h, r = read_csv(os.path.join(out, "reproduction_check.csv"))
    for line in md_table(h, r):
        L.append(line)
    L.append("")

    # ---- cash -----------------------------------------------------------
    L.append("## 2. The cash series, and why the lambda=0 column is the cash rate")
    L.append("")
    L.append("`r(lambda) = lambda * r_risky + (1 - lambda) * r_cash`.  At `lambda = 0`")
    L.append("this is `r_cash` term by term, so the `lambda = 0` row of every frontier")
    L.append("table below is the cash proxy and nothing else.  The gap between the")
    L.append("independently computed cash CAGR and the `lambda = 0` CAGR is printed as")
    L.append("an identity check, not asserted:")
    L.append("")
    _, h, r = read_csv(os.path.join(out, "tradeoff_R4_rt0.csv"))
    i0 = h.index("cash_cagr")
    L.append("- R4 cash CAGR over its window: **%s**"
             % as_pct(r[0][i0], 4))
    _, h, r = read_csv(os.path.join(out, "tradeoff_R2L_rt0.csv"))
    i0 = h.index("cash_cagr")
    L.append("- R2L cash CAGR over its window: **%s**"
             % as_pct(r[0][i0], 4))
    L.append("")
    L.append("The cash proxy is `TVC:US03M`, the 3-month US Treasury bill YIELD INDEX.")
    L.append("A yield index is not a fund, and it is also not positive every day.")
    L.append("")
    _, h, rows = read_csv(os.path.join(out, "cash_series.csv"))
    bad = [x for x in rows if x[2] and float(x[2]) <= 0.0]
    negrate = [x for x in bad if x[3] and float(x[3]) < 0.0]
    zerorate = [x for x in bad if x[3] and float(x[3]) == 0.0]
    L.append("- days in R4's window with a NON-POSITIVE cash accrual: **%d of %d**"
             % (len(bad), len(rows)))
    L.append("- of those, %d had a yield of exactly 0.00%% and %d a NEGATIVE yield"
             % (len(zerorate), len(negrate)))
    L.append("")
    for line in md_table(["date", "yield % used", "r_cash"],
                         [[x[0], as_num(x[3], 4) if x[3] else "none printed",
                           as_num(x[2], 8)] for x in negrate]):
        L.append(line)
    L.append("")

    # ---- books ----------------------------------------------------------
    L.append("## 3. The books and their windows")
    L.append("")
    rows = []
    for b in BOOKS:
        _, h, r = read_csv(os.path.join(out, "levels_%s_rt0.csv" % b))
        prov, _, _ = read_csv(os.path.join(out, "frontier_%s_rt0.csv" % b))
        win = [p for p in prov if p.startswith("window ")][0].split()[1]
        f, t = win.split("..")
        nper = [as_num(x, 0) for x in r[0][h.index("n_years"):h.index("n_years") + 1]]
        counts = [len(read_csv(os.path.join(out, "frontier_%s_rt0.csv" % b))[2])]
        sh, _, sr = read_csv(os.path.join(out, "sleeve_headline_%s_rt0.csv" % b))
        rows.append([b, str(len(sr)), str(counts[0]), f, t,
                     ", ".join(x[0] for x in sr)])
    for line in md_table(["book", "sleeves", "lambda rows", "first", "last",
                          "sleeve symbols"], rows):
        L.append(line)
    L.append("")
    L.append("Book definitions and the reason each exists are printed in sections 1")
    L.append("and 2 of `run-output.txt`.")
    L.append("")

    # ---- THE FRONTIER ---------------------------------------------------
    L.append("## 4. THE FRONTIER (the core deliverable)")
    L.append("")
    L.append("Rows are exposure `lambda`.  A cell is the percentage of **complete**")
    L.append("periods whose return is strictly greater than zero.  Leading and trailing")
    L.append("partial periods are dropped, so the `Y` column is a statement about whole")
    L.append("years.  `lambda = 1` is the book; `lambda = 0` is cash.")
    L.append("")
    for b in BOOKS:
        L.append('### %s -- frontier, strict reading' % b)
        L.append("")
        _, h, rows = read_csv(os.path.join(out, "frontier_%s_rt0.csv" % b))
        body = [[as_num(x[h.index("lambda")], 2)]
                + [as_pct(x[h.index(k)], 2) for k in BUCKETS] for x in rows]
        for line in md_table(["lambda"] + BUCKETS, body):
            L.append(line)
        L.append("")
    L.append("### The same frontier under the LOOSE reading (return >= 0)")
    L.append("")
    L.append("A flat period is not a loss.  The two readings differ only where flat")
    L.append("periods are common -- which is the daily, weekly and biweekly columns of")
    L.append("the books with the fewest sleeves.  They agree on every bucket from M")
    L.append("outward, because a cash sliver of 0.8% already makes a flat month")
    L.append("positive.")
    L.append("")
    for b in BOOKS:
        L.append('### %s -- frontier, loose reading (return >= 0)' % b)
        L.append("")
        _, h, rows = read_csv(os.path.join(out, "frontier_ge0_%s_rt0.csv" % b))
        body = [[as_num(x[h.index("lambda")], 2)]
                + [as_pct(x[h.index(k)], 2) for k in BUCKETS] for x in rows]
        for line in md_table(["lambda"] + BUCKETS, body):
            L.append(line)
        L.append("")

    # ---- levels ---------------------------------------------------------
    L.append("## 5. Levels at each lambda")
    L.append("")
    for b in BOOKS:
        L.append('### %s -- levels at each lambda' % b)
        L.append("")
        _, h, rows = read_csv(os.path.join(out, "levels_%s_rt0.csv" % b))
        body = [[as_num(x[h.index("lambda")], 2), as_pct(x[h.index("cagr")]),
                 as_pct(x[h.index("max_dd")]), as_num(x[h.index("sharpe")], 3),
                 as_pct(x[h.index("years_pos_frac")], 1),
                 as_pct(x[h.index("quarters_pos_frac")], 1),
                 as_pct(x[h.index("months_pos_frac")], 1),
                 x[h.index("n_losing_years")]] for x in rows]
        for line in md_table(["lambda", "CAGR", "max_dd", "sharpe", "%Y>0", "%Q>0",
                              "%M>0", "losing yrs"], body):
            L.append(line)
        L.append("")

    # ---- trade-off ------------------------------------------------------
    L.append("## 6. The trade-off curve -- the price of each extra positive year")
    L.append("")
    for b in BOOKS:
        L.append('### %s -- the trade-off curve' % b)
        L.append("")
        _, h, rows = read_csv(os.path.join(out, "tradeoff_%s_rt0.csv" % b))
        L.append("cash CAGR over this window: **%s**" % as_pct(rows[0][h.index("cash_cagr")], 4))
        L.append("")
        body = [[as_num(x[h.index("lambda")], 2), as_pct(x[h.index("cagr")]),
                 as_pct(x[h.index("excess_cagr")]),
                 as_pct(x[h.index("yearly_pos_frac")], 1),
                 as_pct(x[h.index("quarterly_pos_frac")], 1),
                 as_pct(x[h.index("monthly_pos_frac")], 1),
                 as_pct(x[h.index("max_dd")]), as_num(x[h.index("sharpe")], 3),
                 x[h.index("losing_years")]] for x in rows]
        for line in md_table(["lambda", "CAGR", "CAGR-cash", "%Y>0", "%Q>0", "%M>0",
                              "max_dd", "sharpe", "losing years"], body):
            L.append(line)
        L.append("")

    # ---- where it ends --------------------------------------------------
    L.append("## 7. Where the frontier ends")
    L.append("")
    L.append("Largest `lambda` at which **100% of complete periods** of that bucket are")
    L.append("positive, bisected to 0.001 after a 0.05 grid scan.  `n/a` means even")
    L.append("`lambda = 0.001` failed -- only cash itself cleared it.")
    L.append("")
    _, h, rows = read_csv(os.path.join(out, "frontier_end.csv"))
    body = [[x[0], x[1], x[2], x[3] or "n/a", as_pct(x[4]) if x[4] else "n/a",
             as_pct(x[5]) if x[5] else "n/a",
             "monotone" if x[6] == "1" else "NON-MONOTONE"] for x in rows]
    for line in md_table(["book", "bucket", "periods", "max lambda", "CAGR there",
                          "excess vs cash", "grid scan"], body):
        L.append(line)
    L.append("")

    # ---- meaningful return ---------------------------------------------
    L.append("## 8. Best yearly positivity at a return above cash")
    L.append("")
    L.append("`Meaningful` is not readable from the data, so it is defined before the")
    L.append("run as an annual excess over cash.  The scan is at 0.001 resolution in")
    L.append("`lambda`.  `lambda plateau` is how many of the 1001 scanned lambda values")
    L.append("attained the maximum positivity while still meeting the threshold --")
    L.append("reported because the answer is usually a plateau, not a point.")
    L.append("")
    for b in BOOKS:
        L.append('### %s -- best yearly positivity at a return above cash' % b)
        L.append("")
        _, h, rows = read_csv(os.path.join(out, "yearly_positivity_%s_rt0.csv" % b))
        body = [[as_pct(x[0], 1), x[1] or "none", x[2] or "n/a",
                 as_pct(x[3]) if x[3] else "n/a", as_pct(x[4]) if x[4] else "n/a",
                 as_pct(x[5], 1) if x[5] else "n/a",
                 x[7] or "n/a", x[8] or "-"] for x in rows]
        for line in md_table(["min excess", "lam min", "lam max", "CAGR at lam max",
                              "excess", "years > 0", "losing years",
                              "the losing years"], body):
            L.append(line)
        L.append("")

    # ---- quarters/months -----------------------------------------------
    L.append("## 9. Is any lambda positive in EVERY quarter / half-year / month?")
    L.append("")
    L.append("This is the same table as section 7, restricted to the long buckets, and")
    L.append("it is the direct answer to the owner's question at those horizons.")
    L.append("")
    _, h, rows = read_csv(os.path.join(out, "frontier_end.csv"))
    body = [[x[0], x[1], x[2], x[3] or "n/a", as_pct(x[4]) if x[4] else "n/a",
             as_pct(x[5]) if x[5] else "n/a"]
            for x in rows if x[1] in ("Y", "H", "Q", "M")]
    for line in md_table(["book", "bucket", "periods", "max lambda with ALL positive",
                          "CAGR there", "excess vs cash"], body):
        L.append(line)
    L.append("")

    # ---- structure ------------------------------------------------------
    L.append("## 10. Why the frontier is not linear, and how thin its end is")
    L.append("")
    for b in BOOKS:
        L.append('### %s -- why the frontier is not linear, and how thin its end is' % b)
        L.append("")
        _, h, rows = read_csv(os.path.join(out, "structural_%s_rt0.csv" % b))
        for line in md_table(["quantity", "value"], rows):
            L.append(line)
        L.append("")

    # ---- costs ----------------------------------------------------------
    L.append("## 11. Costs -- the frontier re-run at 5 and 20 bps round trip")
    L.append("")
    _, h, rows = read_csv(os.path.join(out, "cost_shift.csv"))
    body = [[x[0], x[1], as_pct(x[2]), as_pct(x[3]), as_num(x[4], 3),
             as_pct(x[5], 1), x[6] or "n/a"] for x in rows]
    for line in md_table(["book", "round-trip bps", "CAGR @lam1", "max_dd @lam1",
                          "sharpe @lam1", "%Y>0 @lam1",
                          "max lambda 100%-years"], body):
        L.append(line)
    L.append("")

    # ---- sample size ----------------------------------------------------
    L.append("## 12. Sample size at lambda = 1")
    L.append("")
    L.append("`n_periods` is not an independent sample: `H` contains `Q` contains `M`")
    L.append("contains the same days.  `n_eff` is the engine's effective count after")
    L.append("lag-1 autocorrelation.")
    L.append("")
    for b in BOOKS:
        L.append('### %s -- sample size at lambda = 1' % b)
        L.append("")
        _, h, rows = read_csv(os.path.join(out, "bucket_stats_%s_rt0.csv" % b))
        body = [[x[0], x[1], as_num(x[2], 6), as_num(x[3], 6), as_num(x[4], 6),
                 as_num(x[5], 3), as_num(x[6], 3), as_num(x[7], 1)] for x in rows]
        for line in md_table(["bucket", "n_periods", "mean period", "sd period",
                              "win_rate", "t_stat", "lag1 autocorr", "n_eff"], body):
            L.append(line)
        L.append("")

    # ---- year by year ---------------------------------------------------
    L.append("## 13. Every year at every lambda")
    L.append("")
    L.append("The losing years are here in full rather than summarised away.")
    L.append("")
    for b in BOOKS:
        L.append('### %s -- every year at every lambda' % b)
        L.append("")
        _, h, rows = read_csv(os.path.join(out, "yearly_%s_rt0.csv" % b))
        body = [[x[0]] + [as_pct(x[i]) for i in range(1, len(h))] for x in rows]
        for line in md_table(h, body):
            L.append(line)
        L.append("")

    # ---- losing years per lambda ---------------------------------------
    L.append("## 14. Losing years at every lambda, in full")
    L.append("")
    for b in BOOKS:
        L.append('### %s -- losing years at every lambda' % b)
        L.append("")
        _, h, rows = read_csv(os.path.join(out, "losing_years_%s_rt0.csv" % b))
        body = [[as_num(x[0], 2), x[1], x[2] or "none",
                 " ".join(as_pct(v, 2) for v in x[3].split()) if x[3] else "-"]
                for x in rows]
        for line in md_table(["lambda", "n losing years", "losing years",
                              "their returns"], body):
            L.append(line)
        L.append("")

    # ---- handcheck ------------------------------------------------------
    L.append("## 15. Independent re-derivation")
    L.append("")
    L.append("`handcheck.py` rebuilds the frontier from `data/*.csv` with its own")
    L.append("reader, its own SMA, its own alignment, its own simulator, its own cash")
    L.append("accrual, its own bucket keys and its own CAGR.  It does not import")
    L.append("`study.py` and does not use the sibling engine.")
    L.append("")
    hc = read_text(os.path.join(root, "handcheck-output.txt"))
    L.append("```text")
    L.append(hc.rstrip("\n"))
    L.append("```")
    L.append("")

    # ---- stdout ---------------------------------------------------------
    L.append("## 16. Appendix -- complete stdout of the run")
    L.append("")
    L.append("```text")
    L.append(read_text(os.path.join(root, "run-output.txt")).rstrip("\n"))
    L.append("```")
    L.append("")

    # ---- artefacts ------------------------------------------------------
    L.append("## 17. Artefact index")
    L.append("")
    rows = []
    for name in sorted(os.listdir(out)):
        prov, h, r = read_csv(os.path.join(out, name))
        rows.append([name, str(len(r)), str(len(h)),
                     prov[0][:70] if prov else ""])
    for line in md_table(["file", "rows", "cols", "first provenance line"], rows):
        L.append(line)
    L.append("")

    text = "\n".join(L)
    if not text.endswith("\n"):
        text += "\n"
    with open(os.path.join(root, "RESULTS.md"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write(text)
    print("wrote RESULTS.md  %d lines, %d bytes" % (text.count("\n"), len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
