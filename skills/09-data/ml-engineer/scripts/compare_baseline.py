#!/usr/bin/env python3
"""Compare model performance against a simple baseline.

Must outperform baseline by >= 5% on primary metric to justify complexity.

Usage: python compare_baseline.py --model preds_model.csv --baseline preds_baseline.csv
       --true y_test.csv --metric f1
"""

import argparse
import pandas as pd
import numpy as np
from sklearn.metrics import (accuracy_score, f1_score, roc_auc_score,
                               precision_score, recall_score, mean_squared_error,
                               mean_absolute_error, r2_score)
import sys


METRIC_FNS = {
    "accuracy": (accuracy_score, "higher"),
    "f1": (f1_score, "higher"),
    "precision": (precision_score, "higher"),
    "recall": (recall_score, "higher"),
    "roc_auc": (roc_auc_score, "higher"),
    "rmse": (lambda y, p: np.sqrt(mean_squared_error(y, p)), "lower"),
    "mae": (mean_absolute_error, "lower"),
    "r2": (r2_score, "higher"),
}


def compute_improvement(model_score: float, baseline_score: float, direction: str) -> float:
    """Compute percentage improvement accounting for direction."""
    if direction == "higher":
        if baseline_score == 0:
            return float("inf") if model_score > 0 else 0
        return ((model_score - baseline_score) / abs(baseline_score)) * 100
    else:
        if model_score == 0:
            return float("inf") if baseline_score > 0 else 0
        return ((baseline_score - model_score) / abs(baseline_score)) * 100


def main():
    parser = argparse.ArgumentParser(description="Model vs baseline comparison")
    parser.add_argument("--model", required=True, help="CSV with model predictions (column: prediction)")
    parser.add_argument("--baseline", required=True, help="CSV with baseline predictions (column: prediction)")
    parser.add_argument("--true", required=True, help="CSV with ground truth (column: target)")
    parser.add_argument("--metric", default="f1", choices=list(METRIC_FNS.keys()),
                       help="Primary metric for comparison (default: f1)")
    parser.add_argument("--threshold", type=float, default=5.0,
                       help="Minimum improvement % over baseline (default: 5)")
    args = parser.parse_args()

    y_true = pd.read_csv(args.true)["target"].values
    y_model = pd.read_csv(args.model)["prediction"].values
    y_baseline = pd.read_csv(args.baseline)["prediction"].values

    metric_fn, direction = METRIC_FNS[args.metric]

    print("=" * 55)
    print("MODEL vs BASELINE COMPARISON")
    print("=" * 55)
    print(f"Primary metric: {args.metric} ({direction} is better)")
    print(f"Minimum improvement threshold: {args.threshold}%")
    print()

    # Compute all metrics
    results = {}
    for name, (fn, _) in METRIC_FNS.items():
        try:
            model_val = fn(y_true, y_model)
            base_val = fn(y_true, y_baseline)
            results[name] = (model_val, base_val)
        except Exception:
            results[name] = (None, None)

    print(f"{'Metric':<14} {'Baseline':>10} {'Model':>10} {'Change':>10} {'Status':>8}")
    print("-" * 55)

    primary_model, primary_baseline = results[args.metric]
    improvement = compute_improvement(primary_model, primary_baseline, direction)

    for name, (model_val, base_val) in results.items():
        if model_val is None:
            continue
        _, dirn = METRIC_FNS[name]
        imp = compute_improvement(model_val, base_val, dirn)
        arrow = "↑" if (dirn == "higher" and imp > 0) or (dirn == "lower" and imp < 0) else "↓"
        status = "✅" if name == args.metric and abs(improvement) >= args.threshold else ""
        print(f"{name:<14} {base_val:>10.4f} {model_val:>10.4f} {imp:>+9.1f}% {status:>8}")

    print(f"\n{'=' * 55}")
    if improvement >= args.threshold:
        print(f"PASS: Model improves {args.metric} by {improvement:.1f}% over baseline ✅")
        print("The added complexity is justified.")
        sys.exit(0)
    elif improvement < 0:
        print(f"FAIL: Model is WORSE than baseline by {abs(improvement):.1f}% ❌")
        print("The model adds negative value. Revert to baseline or debug training.")
        sys.exit(1)
    else:
        print(f"FAIL: Model improves {args.metric} by only {improvement:.1f}% (threshold: {args.threshold}%) ❌")
        print("Insufficient improvement. Consider: better features, different architecture, or stick with baseline.")
        sys.exit(1)


if __name__ == "__main__":
    main()
