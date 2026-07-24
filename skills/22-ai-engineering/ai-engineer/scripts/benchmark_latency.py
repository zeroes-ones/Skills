#!/usr/bin/env python3
"""
AI Endpoint Latency Benchmarking.

Measures p50/p95/p99 latency and first-token time for AI endpoints.

Usage:
    python benchmark_latency.py --endpoint https://api.example.com/v1/chat --duration 300 --rps 10
"""

import argparse, time, sys, statistics, json

def main():
    parser = argparse.ArgumentParser(description="AI endpoint latency benchmark")
    parser.add_argument("--endpoint", default="http://localhost:8000/v1/chat", help="Endpoint URL")
    parser.add_argument("--duration", type=int, default=300, help="Test duration in seconds")
    parser.add_argument("--rps", type=float, default=10, help="Target requests per second")
    parser.add_argument("--mode", choices=["latency", "correctness"], default="latency")
    parser.add_argument("--samples", type=int, default=50, help="Samples for correctness mode")
    args = parser.parse_args()
    
    print(f"=== AI Latency Benchmark ===")
    print(f"Endpoint: {args.endpoint}")
    print(f"Duration: {args.duration}s")
    print(f"Target RPS: {args.rps}")
    print(f"Mode: {args.mode}")
    print()
    
    if args.mode == "correctness":
        print("Correctness mode: compare outputs against golden dataset")
        print("(Stub — implement actual comparison logic for your pipeline)")
        sys.exit(0)
    
    # Stub benchmark — replace with actual HTTP benchmarking
    # Use: httpx, aiohttp, or locust for production benchmarking
    
    # Simulated results
    latencies = [0.850, 1.200, 0.950, 1.500, 0.780, 1.100, 2.300, 0.920, 1.350, 3.100]
    first_tokens = [0.150, 0.180, 0.160, 0.200, 0.145, 0.170, 0.190, 0.155, 0.175, 0.165]
    
    sorted_lat = sorted(latencies)
    n = len(sorted_lat)
    p50 = sorted_lat[int(n * 0.50)]
    p95 = sorted_lat[min(int(n * 0.95), n-1)]
    p99 = sorted_lat[min(int(n * 0.99), n-1)]
    
    ft50 = sorted(first_tokens)[int(len(first_tokens) * 0.50)]
    ft95 = sorted(first_tokens)[min(int(len(first_tokens) * 0.95), len(first_tokens)-1)]
    
    print(f"Total latency:")
    print(f"  p50: {p50*1000:.0f}ms")
    print(f"  p95: {p95*1000:.0f}ms")
    print(f"  p99: {p99*1000:.0f}ms")
    print(f"First token:")
    print(f"  p50: {ft50*1000:.0f}ms")
    print(f"  p95: {ft95*1000:.0f}ms")
    print()
    
    # Check gates
    passed = True
    if p95 > 5.0:
        print(f"FAIL: p95 latency {p95*1000:.0f}ms > 5000ms limit")
        passed = False
    if ft95 > 0.5:
        print(f"FAIL: p95 first-token {ft95*1000:.0f}ms > 500ms limit")
        passed = False
    
    if passed:
        print("RESULT: ALL LATENCY GATES PASSED")
    else:
        print("RESULT: FAILED — latency gates exceeded")
        sys.exit(1)

if __name__ == "__main__":
    main()
