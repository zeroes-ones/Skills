#!/usr/bin/env python3
"""Check probability calibration of a classification model.

Computes Brier score and calibration curve. Thresholds: Brier < 0.1, curve within 10% of diagonal.

Usage: python check_calibration.py --true y_test.csv --probs model_probs.csv
"""

import argparse
import pandas as pd
import numpy as np
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss
import sys


def check_calibration(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> dict:
    """Compute calibration metrics."""
    brier = brier_score_loss(y_true, y_prob)
    prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=n_bins, strategy='uniform')

    # Max deviation from diagonal (perfect calibration)
    max_deviation = max(abs(prob_true - prob_pred)) * 100
    mean_deviation = np.mean(abs(prob_true - prob_pred)) * 100

    return {
        "brier_score": round(brier, 4),
        "max_deviation_pct": round(max_deviation, 2),
        "mean_deviation_pct": round(mean_deviation, 2),
        "prob_true": prob_true.tolist(),
        "prob_pred": prob_pred.tolist(),
        "n_bins": n_bins,
    }


def main():
    parser = argparse.ArgumentParser(description="Check probability calibration")
    parser.add_argument("--true", required=True, help="CSV with ground truth (column: target)")
    parser.add_argument("--probs", required=True, help="CSV with predicted probabilities (column: prob)")
    parser.add_argument("--n-bins", type=int, default=10, help="Number of bins for calibration curve")
    parser.add_argument("--brier-threshold", type=float, default=0.1,
                       help="Brier score threshold (default: 0.1)")
    parser.add_argument("--deviation-threshold", type=float, default=10.0,
                       help="Max acceptable calibration deviation in %% (default: 10)")
    args = parser.parse_args()

    y_true = pd.read_csv(args.true)["target"].values
    y_prob = pd.read_csv(args.probs)["prob"].values

    if len(np.unique(y_true)) != 2:
        print("ERROR: Calibration check requires binary classification.")
        sys.exit(2)

    result = check_calibration(y_true, y_prob, args.n_bins)

    print("=" * 55)
    print("PROBABILITY CALIBRATION AUDIT")
    print("=" * 55)
    print(f"Brier Score: {result['brier_score']:.4f} ({'✅' if result['brier_score'] < args.brier_threshold else '❌'} threshold: {args.brier_threshold})")
    print(f"Max Deviation from Diagonal: {result['max_deviation_pct']:.1f}% ({'✅' if result['max_deviation_pct'] < args.deviation_threshold else '❌'} threshold: {args.deviation_threshold}%)")
    print(f"Mean Deviation from Diagonal: {result['mean_deviation_pct']:.1f}%")
    print()

    print("Calibration Curve (binned):")
    print(f"{'Predicted':>10} {'Actual':>10} {'Gap':>10}")
    print("-" * 32)
    for pp, pt in zip(result["prob_pred"], result["prob_true"]):
        gap = (pt - pp) * 100
        print(f"{pp:>10.3f} {pt:>10.3f} {gap:>+9.1f}%")

    print(f"\n{'=' * 55}")
    brier_pass = result["brier_score"] < args.brier_threshold
    dev_pass = result["max_deviation_pct"] < args.deviation_threshold

    if brier_pass and dev_pass:
        print("VERDICT: MODEL IS WELL CALIBRATED ✅")
        sys.exit(0)
    elif not brier_pass:
        print("FAIL: Brier score too high ❌")
        print("Fix: Wrap model in CalibratedClassifierCV(method='isotonic', cv=5)")
        sys.exit(1)
    else:
        print("FAIL: Calibration curve deviates from diagonal ❌")
        print("Fix: CalibratedClassifierCV with Platt scaling or isotonic regression")
        sys.exit(1)


if __name__ == "__main__":
    main()
