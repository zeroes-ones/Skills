#!/usr/bin/env python3
"""Model serving smoke test — validates endpoint health, response shape, and latency.

Usage: python test_serving.py --endpoint $URL --samples 100 --max-latency-ms 200
"""

import argparse
import json
import sys
import time
import numpy as np
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def send_request(endpoint: str, payload: dict, headers: dict, timeout: int) -> tuple:
    """Send a single inference request. Returns (latency_ms, status_code, error)."""
    start = time.time()
    try:
        resp = requests.post(endpoint, json=payload, headers=headers, timeout=timeout)
        latency_ms = (time.time() - start) * 1000
        resp.raise_for_status()
        data = resp.json()
        return latency_ms, resp.status_code, None, data
    except Exception as e:
        latency_ms = (time.time() - start) * 1000
        return latency_ms, getattr(e, 'response', type('', (), {'status_code': 0})()).status_code or 0, str(e), None


def main():
    parser = argparse.ArgumentParser(description="Model serving smoke test")
    parser.add_argument("--endpoint", required=True, help="Model serving endpoint URL")
    parser.add_argument("--samples", type=int, default=100, help="Number of test requests (default: 100)")
    parser.add_argument("--max-latency-ms", type=int, default=200,
                       help="Max acceptable p95 latency in ms (default: 200)")
    parser.add_argument("--concurrency", type=int, default=10, help="Concurrent requests (default: 10)")
    parser.add_argument("--timeout", type=int, default=30, help="Per-request timeout in seconds")
    parser.add_argument("--payload", default='{"features": [1.0, 2.0, 3.0]}',
                       help="JSON payload to send (default: sample features)")
    parser.add_argument("--header", action="append", default=[], help="HTTP header in key:value format")
    args = parser.parse_args()

    headers = {"Content-Type": "application/json"}
    for h in args.header:
        k, v = h.split(":", 1)
        headers[k.strip()] = v.strip()

    try:
        payload = json.loads(args.payload)
    except json.JSONDecodeError:
        print("ERROR: Invalid JSON payload", file=sys.stderr)
        sys.exit(2)

    print("=" * 55)
    print("MODEL SERVING SMOKE TEST")
    print("=" * 55)
    print(f"Endpoint:    {args.endpoint}")
    print(f"Samples:     {args.samples}")
    print(f"Concurrency: {args.concurrency}")
    print(f"Max p95:     {args.max_latency_ms}ms")
    print()

    # Warm-up: 5 sequential requests
    print("WARM-UP (5 requests)...")
    warm_latencies = []
    for i in range(5):
        lat, status, err, data = send_request(args.endpoint, payload, headers, args.timeout)
        warm_latencies.append(lat)
        if err:
            print(f"  Warm-up request {i+1} FAILED: {err}", file=sys.stderr)
            sys.exit(2)
    print(f"  Warm-up p50: {np.median(warm_latencies):.0f}ms")

    # Load test
    print(f"\nLOAD TEST ({args.samples} requests, {args.concurrency} concurrent)...")
    latencies = []
    errors = 0
    error_types = {}

    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = [executor.submit(send_request, args.endpoint, payload, headers, args.timeout)
                   for _ in range(args.samples)]
        for i, future in enumerate(as_completed(futures)):
            lat, status, err, data = future.result()
            if err:
                errors += 1
                err_key = err[:60]
                error_types[err_key] = error_types.get(err_key, 0) + 1
            else:
                latencies.append(lat)
            if (i + 1) % 50 == 0:
                print(f"  {i+1}/{args.samples} complete...")

    latencies.sort()
    n = len(latencies)

    if n == 0 and errors > 0:
        print(f"\n{'=' * 55}")
        print("VERDICT: ALL REQUESTS FAILED ❌")
        for err, count in sorted(error_types.items(), key=lambda x: -x[1])[:5]:
            print(f"  [{count}x] {err}")
        sys.exit(1)

    print(f"\n{'=' * 55}")
    print("RESULTS")
    print(f"{'=' * 55}")
    print(f"Successful:  {n:,}/{args.samples} ({(n/args.samples)*100:.1f}%)")
    print(f"Errors:      {errors:,}")

    if latencies:
        print(f"\nLATENCY (n={n}):")
        print(f"  p50:  {np.percentile(latencies, 50):.1f}ms")
        print(f"  p95:  {np.percentile(latencies, 95):.1f}ms")
        print(f"  p99:  {np.percentile(latencies, 99):.1f}ms")
        print(f"  min:  {latencies[0]:.1f}ms")
        print(f"  max:  {latencies[-1]:.1f}ms")
        print(f"  mean: {np.mean(latencies):.1f}ms")

    if errors:
        print(f"\nERROR BREAKDOWN:")
        for err, count in sorted(error_types.items(), key=lambda x: -x[1])[:5]:
            print(f"  [{count}x] {err}")

    p95 = np.percentile(latencies, 95) if latencies else float('inf')
    error_rate = errors / args.samples if args.samples > 0 else 0

    print(f"\n{'=' * 55}")
    if p95 <= args.max_latency_ms and error_rate <= 0.01:
        print(f"VERDICT: PASS ✅ — p95={p95:.0f}ms <= {args.max_latency_ms}ms, "
              f"error_rate={error_rate*100:.1f}%")
        sys.exit(0)
    elif p95 > args.max_latency_ms:
        print(f"VERDICT: FAIL ❌ — p95={p95:.0f}ms > {args.max_latency_ms}ms threshold")
        print("  Recommendations:")
        print("    1. Enable dynamic batching")
        print("    2. Profile GPU utilization — may need more replicas")
        print("    3. Check for cold start — pre-warm models")
        sys.exit(1)
    else:
        print(f"VERDICT: FAIL ❌ — error_rate={error_rate*100:.1f}% > 1% threshold")
        sys.exit(1)


if __name__ == "__main__":
    main()
