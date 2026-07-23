#!/usr/bin/env python3
"""Audit model fairness across protected attributes.

Checks: disparate impact ratio, equal opportunity difference, per-group metrics.

Usage: python audit_fairness.py --true y_test.csv --preds model_preds.csv
       --protected demography.csv --attr gender
"""

import argparse
import pandas as pd
import numpy as np
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                               f1_score, confusion_matrix)
import sys


def compute_fairness_metrics(y_true: np.ndarray, y_pred: np.ndarray,
                              groups: np.ndarray) -> dict:
    """Compute fairness metrics across groups."""
    unique_groups = sorted(set(groups))
    metrics = {}

    for group in unique_groups:
        mask = groups == group
        y_t = y_true[mask]
        y_p = y_pred[mask]

        if len(y_t) < 10:
            metrics[group] = {"n": len(y_t), "warning": "Too few samples"}
            continue

        cm = confusion_matrix(y_t, y_p)
        tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)

        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0  # recall for positive class
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0

        metrics[group] = {
            "n": len(y_t),
            "positive_rate": (y_p == 1).mean(),
            "precision": precision,
            "recall": tpr,
            "f1": f1_score(y_t, y_p, zero_division=0),
            "accuracy": accuracy_score(y_t, y_p),
        }

    # Disparate impact: P(pred=1 | group) / P(pred=1 | reference)
    if len(unique_groups) >= 2:
        ref_group = unique_groups[0]
        ref_rate = metrics[ref_group]["positive_rate"]
        for group in unique_groups[1:]:
            group_rate = metrics[group]["positive_rate"]
            if ref_rate > 0:
                metrics[group]["disparate_impact"] = group_rate / ref_rate
            else:
                metrics[group]["disparate_impact"] = float("inf") if group_rate > 0 else 1.0

        # Equal opportunity difference: TPR difference
        ref_tpr = metrics[ref_group]["recall"]
        for group in unique_groups[1:]:
            metrics[group]["equal_opp_diff"] = abs(metrics[group]["recall"] - ref_tpr)

    return metrics


def main():
    parser = argparse.ArgumentParser(description="Audit model fairness")
    parser.add_argument("--true", required=True, help="CSV with ground truth (column: target)")
    parser.add_argument("--preds", required=True, help="CSV with predictions (column: prediction)")
    parser.add_argument("--protected", required=True, help="CSV with demographic data")
    parser.add_argument("--attr", required=True, help="Protected attribute column name")
    parser.add_argument("--di-threshold", type=float, default=0.8,
                       help="Disparate impact threshold (default: 0.8, 'four-fifths rule')")
    parser.add_argument("--eod-threshold", type=float, default=0.1,
                       help="Equal opportunity difference threshold (default: 0.1)")
    args = parser.parse_args()

    y_true = pd.read_csv(args.true)["target"].values
    y_pred = pd.read_csv(args.preds)["prediction"].values
    groups = pd.read_csv(args.protected)[args.attr].values

    if len(y_true) != len(groups):
        print(f"ERROR: Mismatched lengths — true={len(y_true)}, protected={len(groups)}")
        sys.exit(2)

    metrics = compute_fairness_metrics(y_true, y_pred, groups)

    print("=" * 60)
    print(f"FAIRNESS AUDIT — Protected Attribute: {args.attr}")
    print("=" * 60)
    print()

    unique_groups = sorted(metrics.keys())
    ref_group = unique_groups[0]

    # Header
    print(f"{'Group':<12} {'N':>6} {'Pos%':>8} {'Prec':>8} {'Recall':>8} {'F1':>8} {'DI':>8} {'EOD':>8} {'Status':>10}")
    print("-" * 82)

    all_pass = True
    for group in unique_groups:
        m = metrics[group]
        if "warning" in m:
            print(f"{group:<12} {m['n']:>6} {'--':>8} {'--':>8} {'--':>8} {'--':>8} {'--':>8} {'--':>8} {'SKIP':>10}")
            continue

        di = m.get("disparate_impact", "-")
        eod = m.get("equal_opp_diff", "-")

        issues = []
        if isinstance(di, float) and di < args.di_threshold:
            issues.append(f"DI={di:.2f}<{args.di_threshold}")
            all_pass = False
        if isinstance(eod, float) and eod > args.eod_threshold:
            issues.append(f"EOD={eod:.2f}>{args.eod_threshold}")
            all_pass = False

        di_str = f"{di:.2f}" if isinstance(di, float) else str(di)
        eod_str = f"{eod:.2f}" if isinstance(eod, float) else str(eod)
        status = "✅" if not issues else "❌ " + ", ".join(issues)

        print(f"{group:<12} {m['n']:>6} {m['positive_rate']:>7.1%} "
              f"{m['precision']:>7.2f} {m['recall']:>7.2f} {m['f1']:>7.2f} "
              f"{di_str:>8} {eod_str:>8} {status:<40}")

    print(f"\n{'=' * 60}")
    if all_pass:
        print("VERDICT: FAIRNESS CHECKS PASSED ✅")
        sys.exit(0)
    else:
        print("VERDICT: FAIRNESS VIOLATIONS DETECTED ❌")
        print("\nMitigations:")
        print("  - Reweigh samples: from fairlearn.reductions import ExponentiatedGradient")
        print("  - Adjust thresholds per group for equal opportunity")
        print("  - Remove or transform biased features")
        print("  - Collect more representative training data")
        sys.exit(1)


if __name__ == "__main__":
    main()
