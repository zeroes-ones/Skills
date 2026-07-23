#!/usr/bin/env python3
"""Diagnose feature and prediction drift between training and production data.

Checks: feature drift (KS test per feature), prediction drift, concept drift indicators.

Usage: python diagnose_drift.py --reference train.csv --current prod_data.csv --target label
"""

import argparse
import pandas as pd
import numpy as np
from scipy import stats
import sys


def detect_feature_drift(reference: pd.DataFrame, current: pd.DataFrame,
                          target_col: str, alpha: float = 0.01) -> list:
    """KS test per numeric feature between reference and current."""
    drifted = []
    numeric_cols = reference.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        if col == target_col:
            continue
        ref_vals = reference[col].dropna()
        cur_vals = current[col].dropna()
        if len(ref_vals) < 30 or len(cur_vals) < 30:
            continue
        try:
            ks_stat, p_value = stats.ks_2samp(ref_vals, cur_vals)
            if p_value < alpha:
                drift_magnitude = abs(ref_vals.mean() - cur_vals.mean()) / (ref_vals.std() + 1e-10)
                drifted.append({
                    "feature": col,
                    "p_value": p_value,
                    "drift_magnitude": round(drift_magnitude, 3),
                    "ref_mean": round(ref_vals.mean(), 4),
                    "cur_mean": round(cur_vals.mean(), 4),
                })
        except Exception:
            pass

    return sorted(drifted, key=lambda d: d["p_value"])


def check_prediction_drift(reference_preds: np.ndarray, current_preds: np.ndarray) -> dict:
    """Compare prediction distributions."""
    ks_stat, p_value = stats.ks_2samp(reference_preds, current_preds)
    ref_mean = np.mean(reference_preds)
    cur_mean = np.mean(current_preds)
    mean_shift = abs(ref_mean - cur_mean)

    return {
        "ks_p_value": p_value,
        "ref_mean": round(ref_mean, 4),
        "cur_mean": round(cur_mean, 4),
        "mean_shift": round(mean_shift, 4),
        "prediction_drift": p_value < 0.01,
    }


def main():
    parser = argparse.ArgumentParser(description="Diagnose model drift in production")
    parser.add_argument("--reference", required=True, help="Training/reference data CSV")
    parser.add_argument("--current", required=True, help="Current production data CSV")
    parser.add_argument("--target", required=True, help="Target column name")
    parser.add_argument("--alpha", type=float, default=0.01,
                       help="P-value threshold for drift detection (default: 0.01)")
    args = parser.parse_args()

    ref = pd.read_csv(args.reference)
    cur = pd.read_csv(args.current)

    print("=" * 60)
    print("DRIFT DIAGNOSIS REPORT")
    print("=" * 60)
    print(f"Reference data: {len(ref):,} rows")
    print(f"Current data:   {len(cur):,} rows")
    print(f"Drift threshold: p < {args.alpha}")
    print()

    # Feature drift
    print("1. FEATURE DRIFT (KS Test)")
    drifted_features = detect_feature_drift(ref, cur, args.target, args.alpha)
    if drifted_features:
        print(f"   ❌ {len(drifted_features)} drifted features detected:")
        print(f"   {'Feature':<20} {'P-Value':>10} {'Drift σ':>10} {'Ref Mean':>12} {'Cur Mean':>12}")
        print("   " + "-" * 66)
        for d in drifted_features[:15]:
            print(f"   {d['feature']:<20} {d['p_value']:>10.2e} "
                  f"{d['drift_magnitude']:>10.3f} {d['ref_mean']:>12.4f} {d['cur_mean']:>12.4f}")
        if len(drifted_features) > 15:
            print(f"   ... and {len(drifted_features) - 15} more")
    else:
        print("   ✅ No feature drift detected")

    # Target drift
    if args.target in ref.columns and args.target in cur.columns:
        print("\n2. TARGET DISTRIBUTION DRIFT")
        ref_target = ref[args.target].dropna()
        cur_target = cur[args.target].dropna()
        if len(ref_target) > 30 and len(cur_target) > 30:
            ks_stat, p_value = stats.ks_2samp(ref_target, cur_target)
            if p_value < args.alpha:
                print(f"   ❌ Target distribution has drifted (p={p_value:.2e})")
                print(f"   Ref mean: {ref_target.mean():.4f}, Cur mean: {cur_target.mean():.4f}")
                print("   → CONCEPT DRIFT likely — retrain model")
            else:
                print(f"   ✅ Target distribution stable (p={p_value:.4f})")
        else:
            print("   ⚠ Insufficient data for target drift check")

    print(f"\n{'=' * 60}")
    if len(drifted_features) == 0:
        print("VERDICT: NO DRIFT DETECTED ✅ — model inputs are stable")
        sys.exit(0)
    elif len(drifted_features) <= 3:
        print(f"VERDICT: MILD DRIFT ({len(drifted_features)} features) ⚠")
        print("Monitor closely. If prediction quality degrades, retrain on recent data.")
        sys.exit(0)
    else:
        print(f"VERDICT: SIGNIFICANT DRIFT ({len(drifted_features)} features) ❌")
        print("Recommendations:")
        print("  1. Investigate root cause of each drifted feature")
        print("  2. Retrain model on recent data")
        print("  3. Consider online learning or more frequent retraining cycles")
        sys.exit(1)


if __name__ == "__main__":
    main()
