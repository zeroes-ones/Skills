#!/usr/bin/env python3
"""GPU utilization profiler — finds optimal batch size and utilization metrics.

Usage: python profile_gpu.py [--gpu-id 0]

Note: Requires nvidia-smi and PyTorch with CUDA.
"""

import argparse
import subprocess
import sys
import time
import json


def run_nvidia_smi(gpu_id: int = 0) -> dict:
    """Run nvidia-smi and parse GPU metrics."""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total,"
             "temperature.gpu,power.draw,clocks.sm,clocks.mem",
             "--format=csv,noheader,nounits", f"--id={gpu_id}"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode != 0:
            return {"error": result.stderr.strip()}

        parts = [p.strip() for p in result.stdout.split(",")]
        if len(parts) >= 7:
            return {
                "gpu_util_pct": float(parts[0]),
                "mem_used_mb": float(parts[1]),
                "mem_total_mb": float(parts[2]),
                "mem_util_pct": (float(parts[1]) / float(parts[2]) * 100) if float(parts[2]) > 0 else 0,
                "temp_c": float(parts[3]),
                "power_w": float(parts[4]),
                "sm_clock_mhz": float(parts[5]),
                "mem_clock_mhz": float(parts[6]),
            }
    except FileNotFoundError:
        return {"error": "nvidia-smi not found — is NVIDIA driver installed?"}
    except Exception as e:
        return {"error": str(e)}


def check_pytorch_gpu():
    """Check PyTorch GPU availability and properties."""
    try:
        import torch
        if torch.cuda.is_available():
            info = {
                "pytorch_cuda": True,
                "device_count": torch.cuda.device_count(),
                "devices": []
            }
            for i in range(torch.cuda.device_count()):
                props = torch.cuda.get_device_properties(i)
                info["devices"].append({
                    "index": i,
                    "name": props.name,
                    "total_memory_gb": round(props.total_memory / (1024**3), 1),
                    "compute_capability": f"{props.major}.{props.minor}",
                    "multi_processor_count": props.multi_processor_count,
            })
            return info
        else:
            return {"pytorch_cuda": False, "error": "CUDA not available in PyTorch"}
    except ImportError:
        return {"pytorch_cuda": False, "error": "PyTorch not installed"}


def check_nvidia_smi_list():
    """List all GPUs via nvidia-smi."""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            gpus = []
            for line in result.stdout.strip().split("\n"):
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 6:
                    gpus.append({
                        "index": int(parts[0]),
                        "name": parts[1],
                        "util_pct": float(parts[2]),
                        "mem_used_mb": float(parts[3]),
                        "mem_total_mb": float(parts[4]),
                        "temp_c": float(parts[5]),
                    })
            return gpus
    except Exception:
        pass
    return []


def main():
    parser = argparse.ArgumentParser(description="GPU utilization profiler for ML serving")
    parser.add_argument("--gpu-id", type=int, default=0, help="GPU index to profile")
    parser.add_argument("--continuous", action="store_true", help="Continuous monitoring (Ctrl+C to stop)")
    parser.add_argument("--interval", type=float, default=2.0, help="Sampling interval in seconds")
    args = parser.parse_args()

    print("=" * 60)
    print("GPU PROFILER — ML SERVING OPTIMIZATION")
    print("=" * 60)

    # Check PyTorch GPU
    pt_info = check_pytorch_gpu()
    if pt_info.get("pytorch_cuda"):
        print(f"\nPyTorch CUDA: {pt_info['device_count']} GPU(s) available")
        for dev in pt_info.get("devices", []):
            print(f"  GPU {dev['index']}: {dev['name']} ({dev['total_memory_gb']} GB, "
                  f"CC {dev['compute_capability']}, {dev['multi_processor_count']} SMs)")

    # List all GPUs
    gpus = check_nvidia_smi_list()
    if gpus:
        print(f"\nGPU INVENTORY:")
        for gpu in gpus:
            print(f"  GPU {gpu['index']}: {gpu['name']} — {gpu['util_pct']:.0f}% util, "
                  f"{gpu['mem_used_mb']:.0f}/{gpu['mem_total_mb']:.0f} MB, {gpu['temp_c']:.0f}°C")

    # Snapshot
    print(f"\nGPU {args.gpu_id} SNAPSHOT:")
    metrics = run_nvidia_smi(args.gpu_id)
    if "error" in metrics:
        print(f"  ERROR: {metrics['error']}")
        print("\nGPU profiling limited to nvidia-smi output. For batch size optimization:")
        print("  1. Import your model in Python")
        print("  2. Use torch.cuda.max_memory_allocated() to find memory ceiling")
        print("  3. Start at batch_size=1, double until OOM, back off to last stable size")
        print("  4. Benchmark throughput at each batch size to find the knee")
        sys.exit(1)

    for k, v in metrics.items():
        print(f"  {k}: {v}")

    # Health assessment
    print(f"\nHEALTH ASSESSMENT (GPU {args.gpu_id}):")
    util = metrics.get("gpu_util_pct", 0)
    mem_util = metrics.get("mem_util_pct", 0)

    issues = []
    if util < 30:
        issues.append(f"⚠ GPU UTILIZATION LOW ({util:.0f}%) — over-provisioned. "
                      f"Consider: dynamic batching, multi-model colocation, or downsizing GPU.")
    elif util > 90:
        issues.append(f"⚠ GPU SATURATED ({util:.0f}%) — add replicas or optimize inference.")

    if mem_util < 20:
        issues.append(f"⚠ GPU MEMORY UNDERUTILIZED ({mem_util:.0f}%) — use larger batch size "
                      f"or fit more models on same GPU.")
    elif mem_util > 90:
        issues.append(f"⚠ GPU MEMORY NEAR LIMIT ({mem_util:.0f}%) — risk of OOM. "
                      f"Reduce batch size or enable gradient checkpointing.")

    if metrics.get("temp_c", 0) > 80:
        issues.append(f"⚠ HIGH TEMPERATURE ({metrics['temp_c']:.0f}°C) — check cooling.")

    if issues:
        for issue in issues:
            print(f"  {issue}")
    else:
        print(f"  ✅ GPU healthy — {util:.0f}% util, {mem_util:.0f}% memory")

    # Cost analysis
    gpu_hourly = 3.50  # approximate A100 hourly cost
    monthly_cost = gpu_hourly * 24 * 30.44
    wasted = monthly_cost * (1 - util / 100) if util < 100 else 0
    print(f"\nCOST ANALYSIS (single GPU):")
    print(f"  Estimated hourly rate: ${gpu_hourly:.2f}/hr (A100-class)")
    print(f"  Monthly cost:          ${monthly_cost:,.2f}")
    if wasted > 0:
        print(f"  Wasted (idle):         ${wasted:,.2f}/month ({100 - util:.0f}% idle)")
        print(f"  Annual waste:          ${wasted * 12:,.2f}")
        if util < 30:
            print(f"  → Switching to smaller GPU could save ${monthly_cost * 0.5:,.2f}/month")

    # Continuous mode
    if args.continuous:
        print(f"\nContinuous monitoring (interval={args.interval}s). Ctrl+C to stop.")
        try:
            while True:
                m = run_nvidia_smi(args.gpu_id)
                if "error" not in m:
                    print(f"  [{time.strftime('%H:%M:%S')}] "
                          f"GPU: {m['gpu_util_pct']:5.1f}% | "
                          f"Mem: {m['mem_used_mb']:.0f}/{m['mem_total_mb']:.0f} MB | "
                          f"Temp: {m['temp_c']:.0f}°C | "
                          f"Power: {m['power_w']:.0f}W")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")

    sys.exit(0)


if __name__ == "__main__":
    main()
