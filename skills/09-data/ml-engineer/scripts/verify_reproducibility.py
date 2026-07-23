#!/usr/bin/env python3
"""Verify ML training reproducibility by comparing two training runs.

Usage: python verify_reproducibility.py --preds1 run1.csv --preds2 run2.csv --tolerance 1e-10
"""

import argparse
import pandas as pd
import numpy as np
import sys


def main():
    parser = argparse.ArgumentParser(description="Check training reproducibility")
    parser.add_argument("--preds1", required=True, help="CSV with predictions from run 1 (column: prediction)")
    parser.add_argument("--preds2", required=True, help="CSV with predictions from run 2 (column: prediction)")
    parser.add_argument("--tolerance", type=float, default=1e-10,
                       help="Maximum allowed absolute difference (default: 1e-10)")
    args = parser.parse_args()

    p1 = pd.read_csv(args.preds1)["prediction"].values.astype(np.float64)
    p2 = pd.read_csv(args.preds2)["prediction"].values.astype(np.float64)

    if len(p1) != len(p2):
        print(f"ERROR: Different lengths — run1={len(p1)}, run2={len(p2)}")
        sys.exit(2)

    abs_diff = np.abs(p1 - p2)
    max_diff = abs_diff.max()
    mean_diff = abs_diff.mean()
    identical = np.sum(abs_diff <= args.tolerance)
    different = np.sum(abs_diff > args.tolerance)

    print("=" * 55)
    print("REPRODUCIBILITY VERIFICATION")
    print("=" * 55)
    print(f"Predictions compared: {len(p1):,}")
    print(f"Tolerance: {args.tolerance}")
    print()
    print(f"Max absolute difference:  {max_diff:.2e}")
    print(f"Mean absolute difference: {mean_diff:.2e}")
    print(f"Identical (≤tolerance):   {identical:,} ({identical/len(p1)*100:.1f}%)")
    print(f"Different (>tolerance):   {different:,} ({different/len(p1)*100:.1f}%)")

    print(f"\n{'=' * 55}")
    if identical == len(p1):
        print("VERDICT: TRAINING IS FULLY REPRODUCIBLE ✅")
        sys.exit(0)
    elif different / len(p1) < 0.001:
        print("VERDICT: NEARLY REPRODUCIBLE (minor float differences) ⚠")
        print(f"  {different} predictions differ — verify random seeds are set deterministically")
        sys.exit(0)
    else:
        print("VERDICT: NOT REPRODUCIBLE ❌")
        print(f"  {different} predictions differ significantly.")
        print("  Check: random seeds, OMP_NUM_THREADS=1, MKL_NUM_THREADS=1")
        print("  For PyTorch: torch.backends.cudnn.deterministic = True")
        sys.exit(1)


if __name__ == "__main__":
    main()
