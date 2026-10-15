#!/usr/bin/env python3
"""verify_metrics.py - hand-check the trade statistics.

Takes the R-multiple list for one strategy-year (printed by
`py -3 study.py --dump-trades M1:SPY:2018`) and recomputes p, b, E, p*, b*,
sd, n_req and the longest losing streak with plain arithmetic, written out
longhand.  Then feeds the same R values through study.metrics() and asserts the
two agree.

  py -3 verify_metrics.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import study  # noqa: E402

try:
    sys.stdout.reconfigure(newline="\n", encoding="utf-8")
except (AttributeError, ValueError):
    pass


# ---- the dumped R-multiples for M1 on SPY over entry-year 2018 -----------------
# from: py -3 study.py --dump-trades M1:SPY:2018
R = [-1.0000, 0.5318, 0.6948, -1.0000, 0.4048, 0.3735, -1.0000,
     0.2800, 0.5359, -1.0000, -1.0000]

print("=" * 78)
print("HAND CHECK - M1 on SPY, entry year 2018, {} closed trades".format(len(R)))
print("=" * 78)

# ---------------------------------------------------------------- longhand ----
n = len(R)
wins = [x for x in R if x > 0]
losses = [x for x in R if x <= 0]
print("\n1. split the trades")
print("   n            = {}".format(n))
print("   wins  (R > 0)= {}  -> {}".format(len(wins), ", ".join("{:.4f}".format(x) for x in wins)))
print("   losses(R<= 0)= {}  -> {}".format(len(losses), ", ".join("{:.4f}".format(x) for x in losses)))

p = len(wins) / float(n)
print("\n2. win rate")
print("   p            = {}/{} = {:.10f}".format(len(wins), n, p))

sum_w = sum(wins)
avg_w = sum_w / len(wins)
print("\n3. average win")
print("   sum(wins)    = {}".format(
    " + ".join("{:.4f}".format(x) for x in wins) + " = {:.6f}".format(sum_w)))
print("   avg_win      = {:.6f} / {} = {:.10f}".format(sum_w, len(wins), avg_w))

sum_l = sum(losses)
avg_l = sum_l / len(losses)
print("\n4. average loss")
print("   sum(losses)  = {:.6f}".format(sum_l))
print("   avg_loss     = {:.6f} / {} = {:.10f}".format(sum_l, len(losses), avg_l))

b = avg_w / abs(avg_l)
print("\n5. payoff ratio")
print("   b            = avg_win / |avg_loss| = {:.10f} / {:.10f} = {:.10f}".format(
    avg_w, abs(avg_l), b))

E_formula = p * b - (1.0 - p)
print("\n6. expectancy, the pre-registered formula")
print("   E = p*b - (1-p) = {:.10f}*{:.10f} - {:.10f} = {:.10f}".format(
    p, b, 1.0 - p, E_formula))

total_R = sum(R)
E_R = total_R / n
print("\n7. expectancy in R, the direct mean")
print("   sum(R)       = {}".format(
    " ".join("{:+.4f}".format(x) for x in R)))
print("                = {:.6f}".format(total_R))
print("   E_R = mean R = {:.6f} / {} = {:.10f}".format(total_R, n, E_R))
print("   note: E_formula == E_R here because every loss is exactly -1R,")
print("         i.e. |avg_loss| = 1.  In general E_formula = E_R / |avg_loss|:")
print("         check        = {:.10f} / {:.10f} = {:.10f}".format(
    E_R, abs(avg_l), E_R / abs(avg_l)))

p_star = 1.0 / (1.0 + b)
print("\n8. breakeven win rate")
print("   p* = 1/(1+b) = 1/(1+{:.10f}) = {:.10f}".format(b, p_star))

b_star = (1.0 - p) / p
print("\n9. required payoff at the observed win rate")
print("   b* = (1-p)/p = {:.10f}/{:.10f} = {:.10f}".format(1.0 - p, p, b_star))

mean = total_R / n
ss = sum((x - mean) ** 2 for x in R)
var = ss / (n - 1)
sd = math.sqrt(var)
print("\n10. dispersion of the R-multiples")
print("    deviations^2 = {}".format(", ".join("{:.6f}".format((x - mean) ** 2) for x in R)))
print("    sum(dev^2)   = {:.6f}".format(ss))
print("    var (n-1)    = {:.6f} / {} = {:.10f}".format(ss, n - 1, var))
print("    sd           = sqrt({:.10f}) = {:.10f}".format(var, sd))

n_req = 4.0 * (sd / abs(E_R)) ** 2
print("\n11. sample size needed for ~2 sigma")
print("    n_req = 4*(sd/|E_R|)^2 = 4*({:.10f}/{:.10f})^2 = 4*{:.6f} = {:.4f}".format(
    sd, abs(E_R), (sd / abs(E_R)) ** 2, n_req))

Lf = math.log(n) / math.log(1.0 / (1.0 - p))
run = best = 0
for x in R:
    if x <= 0:
        run += 1
        best = max(best, run)
    else:
        run = 0
print("\n12. losing streaks")
print("    formula L = ln(N)/ln(1/(1-p)) = ln({})/ln(1/{:.10f}) = {:.6f}/{:.6f} = {:.6f}".format(
    n, 1.0 - p, math.log(n), math.log(1.0 / (1.0 - p)), Lf))
print("    observed longest losing run  = {}".format(best))

tstat = mean / (sd / math.sqrt(n))
print("\n13. t-statistic of the mean R")
print("    t = mean/(sd/sqrt(n)) = {:.10f}/({:.10f}/{:.6f}) = {:.6f}".format(
    mean, sd, math.sqrt(n), tstat))

# ------------------------------------------------- through study.metrics() ----
print("\n" + "=" * 78)
print("SAME VALUES THROUGH study.metrics()")
print("=" * 78)
trades = [study.Trade(R=x, open_flag=False) for x in R]
m = study.metrics(trades)
rows = [
    ("n", n, m["n"]),
    ("p", p, m["p"]),
    ("b", b, m["b"]),
    ("E_formula", E_formula, m["E_formula"]),
    ("E_R", E_R, m["E_R"]),
    ("p_star", p_star, m["p_star"]),
    ("b_star", b_star, m["b_star"]),
    ("sd_R", sd, m["sd_R"]),
    ("n_req", n_req, m["n_req"]),
    ("total_R", total_R, m["total_R"]),
    ("L_formula", Lf, m["L_formula"]),
    ("L_observed", float(best), float(m["L_observed"])),
    ("t_stat", tstat, m["t_stat"]),
]
print("{:<12} {:>20} {:>20} {:>8}".format("quantity", "hand", "study.py", "match"))
ok = True
for name, hv, sv in rows:
    same = abs(hv - sv) < 1e-9 if isinstance(sv, float) else hv == sv
    ok &= bool(same)
    print("{:<12} {:>20.10f} {:>20.10f} {:>8}".format(name, hv, sv, "OK" if same else "MISMATCH"))
print("\n{}".format("HAND CHECK PASSES - hand arithmetic and study.py agree"
                    if ok else "HAND CHECK FAILED"))
sys.exit(0 if ok else 1)
