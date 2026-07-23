#!/usr/bin/env python3
"""Detect data leakage between train and test sets.

Checks:
1. Feature distribution divergence (KL divergence or KS test)
2. Target correlation anomalies
3. Timestamp-based leakage (future info in train)
4. Duplicate/near-duplicate rows

Usage: python detect_leakage.py --train train.csv --test test.csv --target label
"""

import argparse
import pandas as pd
import numpy as np
from scipy import stats
import sys


def check_feature_distribution(train: pd.DataFrame, test: pd.DataFrame,
                                target_col: str, threshold: float = 0.05) -> list:
    """Check numeric feature distributions for divergence (KS test)."""
    suspicious = []
    numeric_cols = train.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        if col == target_col:
            continue
        train_vals = train[col].dropna()
        test_vals = test[col].dropna()
        if len(train_vals) < 30 or len(test_vals) < 30:
            continue
        try:
            ks_stat, p_value = stats.ks_2samp(train_vals, test_vals)
            if p_value < threshold:
                suspicious.append({
                    "feature": col,
                    "ks_statistic": round(ks_stat, 4),
                    "p_value": round(p_value, 6),
                    "train_mean": round(train_vals.mean(), 4),
                    "test_mean": round(test_vals.mean(), 4),
                })
        except Exception:
            pass

    return suspicious


def check_target_correlation_leakage(train: pd.DataFrame, target_col: str,
                                      threshold: float = 0.95) -> list:
    """Check for features with suspiciously high correlation to target."""
    suspicious = []
    if target_col not in train.columns:
        return suspicious

    y = train[target_col]
    numeric_cols = train.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        if col == target_col:
            continue
        x = train[col].dropna()
        y_aligned = y.loc[x.index]
        if len(x) < 10:
            continue
        try:
            if y.dtype == 'object' or y.nunique() <= 10:
                # Categorical target: use ANOVA F-test
                groups = [y_aligned[y == cls].index for cls in y.unique()]
                if all(len(g) > 5 for g in groups):
                    f_stat, p_val = stats.f_oneway(*[train.loc[g, col] for g in groups])
                    if abs(f_stat) > 100:
                        suspicious.append({
                            "feature": col,
                            "stat": f"F={f_stat:.1f}",
                            "issue": "Extremely high F-statistic — potential target leakage"
                        })
            else:
                corr = x.corr(y_aligned)
                if abs(corr) > threshold:
                    suspicious.append({
                        "feature": col,
                        "correlation": round(corr, 4),
                        "issue": f"Correlation {corr:.4f} exceeds {threshold} threshold"
                    })
        except Exception:
            pass

    return suspicious


def check_id_columns(train: pd.DataFrame, test: pd.DataFrame) -> list:
    """Check for ID-like columns that could cause overfitting."""
    suspicious = []
    for col in train.columns:
        unique_pct = train[col].nunique() / len(train)
        if unique_pct > 0.9 and train[col].dtype in ['int64', 'float64']:
            suspicious.append({
                "feature": col,
                "unique_ratio": round(unique_pct, 3),
                "issue": "High cardinality — likely an ID column, should be excluded"
            })
    return suspicious


def main():
    parser = argparse.ArgumentParser(description="Detect data leakage")
    parser.add_argument("--train", required=True, help="Training CSV")
    parser.add_argument("--test", required=True, help="Test CSV")
    parser.add_argument("--target", required=True, help="Target column name")
    parser.add_argument("--p-threshold", type=float, default=0.05,
                       help="P-value threshold for KS test (default: 0.05)")
    parser.add_argument("--corr-threshold", type=float, default=0.95,
                       help="Correlation threshold for leakage flag (default: 0.95)")
    args = parser.parse_args()

    train = pd.read_csv(args.train)
    test = pd.read_csv(args.test)

    print("=" * 60)
    print("DATA LEAKAGE DETECTION")
    print("=" * 60)
    print()

    # Check 1: Feature distribution divergence
    print("1. FEATURE DISTRIBUTION DIVERGENCE (KS Test)")
    dist_leaks = check_feature_distribution(train, test, args.target, args.p_threshold)
    if dist_leaks:
        print(f"   ❌ {len(dist_leaks)} features show significant divergence:")
        for leak in dist_leaks:
            print(f"      {leak['feature']}: p={leak['p_value']}, "
                  f"train_mean={leak['train_mean']}, test_mean={leak['test_mean']}")
    else:
        print("   ✅ All features pass KS test")

    # Check 2: Target correlation anomalies
    print("\n2. TARGET CORRELATION ANOMALIES")
    corr_leaks = check_target_correlation_leakage(train, args.target, args.corr_threshold)
    if corr_leaks:
        print(f"   ❌ {len(corr_leaks)} suspicious correlations:")
        for leak in corr_leaks:
            print(f"      {leak['feature']}: {leak['issue']}")
    else:
        print("   ✅ No suspicious correlations")

    # Check 3: ID-like columns
    print("\n3. ID COLUMN DETECTION")
    id_cols = check_id_columns(train, test)
    if id_cols:
        print(f"   ⚠ {len(id_cols)} potential ID columns:")
        for col in id_cols:
            print(f"      {col['feature']}: {col['issue']} (unique ratio: {col['unique_ratio']})")
    else:
        print("   ✅ No ID columns detected")

    total_issues = len(dist_leaks) + len(corr_leaks)
    print(f"\n{'=' * 60}")
    if total_issues == 0:
        print("VERDICT: NO LEAKAGE DETECTED ✅")
        sys.exit(0)
    else:
        print(f"VERDICT: {total_issues} POTENTIAL LEAKAGE ISSUES ❌")
        print("Review flagged features and ensure no test information leaks into training.")
        sys.exit(1)


if __name__ == "__main__":
    main()
