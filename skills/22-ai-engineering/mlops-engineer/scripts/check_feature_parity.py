#!/usr/bin/env python3
"""Training-serving feature parity checker — detects skew between online and offline features.

Usage: python check_feature_parity.py --offline offline_features.csv --online online_features.csv --tolerance 1e-6
"""

import argparse
import pandas as pd
import numpy as np
import sys


def main():
    parser = argparse.ArgumentParser(description="Check training-serving feature parity")
    parser.add_argument("--offline", required=True, help="CSV of features computed in training (offline store)")
    parser.add_argument("--online", required=True, help="CSV of features computed at serving (online store)")
    parser.add_argument("--tolerance", type=float, default=1e-6,
                       help="Maximum allowed per-value difference (default: 1e-6)")
    parser.add_argument("--key", default="id", help="Join key column (default: id)")
    args = parser.parse_args()

    offline = pd.read_csv(args.offline).set_index(args.key).sort_index()
    online = pd.read_csv(args.online).set_index(args.key).sort_index()

    # Find common keys
    common_keys = offline.index.intersection(online.index)
    if len(common_keys) == 0:
        print("ERROR: No common keys between offline and online datasets. Check --key.", file=sys.stderr)
        sys.exit(2)

    offline_aligned = offline.loc[common_keys]
    online_aligned = online.loc[common_keys]

    # Find common feature columns
    feature_cols = sorted(set(offline_aligned.columns) & set(online_aligned.columns))
    if not feature_cols:
        print("ERROR: No common feature columns found.", file=sys.stderr)
        sys.exit(2)

    print("=" * 60)
    print("TRAINING-SERVING FEATURE PARITY CHECK")
    print("=" * 60)
    print(f"Common keys:      {len(common_keys):,}")
    print(f"Feature columns:  {len(feature_cols)}")
    print(f"Tolerance:        {args.tolerance}")
    print()

    mismatched_features = []
    total_comparisons = len(common_keys) * len(feature_cols)
    mismatches = 0

    for col in feature_cols:
        off_vals = offline_aligned[col].values.astype(np.float64)
        on_vals = online_aligned[col].values.astype(np.float64)

        # Handle NaN: both NaN = match
        both_nan = np.isnan(off_vals) & np.isnan(on_vals)
        one_nan = np.isnan(off_vals) ^ np.isnan(on_vals)
        numeric_mask = ~np.isnan(off_vals) & ~np.isnan(on_vals)

        nan_mismatches = one_nan.sum()
        if nan_mismatches > 0:
            mismatched_features.append({
                "feature": col,
                "mismatches": int(nan_mismatches),
                "type": "NaN mismatch",
                "max_diff": float('nan'),
                "mean_diff": float('nan'),
            })
            mismatches += nan_mismatches

        if numeric_mask.sum() > 0:
            abs_diff = np.abs(off_vals[numeric_mask] - on_vals[numeric_mask])
            significant = abs_diff > args.tolerance
            sig_count = significant.sum()
            if sig_count > 0:
                mismatched_features.append({
                    "feature": col,
                    "mismatches": int(sig_count),
                    "type": "value mismatch",
                    "max_diff": float(abs_diff.max()),
                    "mean_diff": float(abs_diff.mean()),
                })
                mismatches += sig_count

    mismatched_features.sort(key=lambda x: x["mismatches"], reverse=True)

    print("FEATURE-BY-FEATURE:")
    print(f"  {'Feature':<30} {'Mismatches':>10} {'Type':<15} {'Max Diff':>12} {'Mean Diff':>12}")
    print("  " + "-" * 82)
    for mf in mismatched_features[:20]:
        print(f"  {mf['feature']:<30} {mf['mismatches']:>10,} {mf['type']:<15} "
              f"{mf['max_diff']:>12.6f} {mf['mean_diff']:>12.6f}")
    if len(mismatched_features) > 20:
        print(f"  ... and {len(mismatched_features) - 20} more features")

    parity_pct = (1 - mismatches / total_comparisons) * 100 if total_comparisons > 0 else 100

    print(f"\n{'=' * 60}")
    print(f"Total comparisons: {total_comparisons:,}")
    print(f"Mismatches:        {mismatches:,}")
    print(f"Parity:            {parity_pct:.4f}%")

    if mismatches == 0:
        print("VERDICT: FULL PARITY ✅ — no training-serving skew detected")
        sys.exit(0)
    elif parity_pct >= 99.99:
        print(f"VERDICT: NEAR-PERFECT PARITY ⚠ — {mismatches} minor differences")
        print("  Verify: floating-point precision, timestamp rounding, aggregation boundary conditions")
        sys.exit(0)
    else:
        print(f"VERDICT: SKEW DETECTED ❌ — {mismatches:,} mismatches ({len(mismatched_features)} features affected)")
        print(f"  Impact: model predictions use features {100 - parity_pct:.2f}% different from training")
        print(f"  Root cause suspects:")
        print(f"    1. Different aggregation logic (Spark batch vs Redis real-time)")
        print(f"    2. Time boundary differences (training uses end-of-day, serving uses current)")
        print(f"    3. Default/fill values differ between offline and online pipelines")
        sys.exit(1)


if __name__ == "__main__":
    main()
