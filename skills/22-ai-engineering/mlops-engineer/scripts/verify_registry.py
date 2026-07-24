#!/usr/bin/env python3
"""Model registry integrity checker — validates registry state matches deployment reality.

Usage: python verify_registry.py --registry-url $MLFLOW_TRACKING_URI --endpoint $SERVING_ENDPOINT
"""

import argparse
import json
import sys
import requests
from datetime import datetime, timezone


def check_mlflow_registry(tracking_uri: str, model_name: str) -> dict:
    """Query MLflow registry for production model version."""
    try:
        # MLflow REST API: get latest versions
        url = f"{tracking_uri}/api/2.0/mlflow/registered-models/get-latest-versions"
        resp = requests.post(url, json={"name": model_name, "stages": ["Production"]}, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        versions = data.get("model_versions", [])
        if not versions:
            return {"error": f"No production version found for '{model_name}'"}

        prod = versions[0]
        return {
            "model_name": model_name,
            "version": prod.get("version"),
            "run_id": prod.get("run_id"),
            "current_stage": prod.get("current_stage"),
            "creation_timestamp": prod.get("creation_timestamp"),
            "source": prod.get("source"),
        }
    except Exception as e:
        return {"error": f"MLflow API error: {e}"}


def check_serving_endpoint(endpoint: str) -> dict:
    """Query serving endpoint for current model version."""
    try:
        # Try /health or /version endpoint
        for path in ["/health", "/version", "/metadata", "/v1/models"]:
            try:
                resp = requests.get(f"{endpoint}{path}", timeout=10)
                if resp.status_code == 200:
                    return {"health": "ok", "version_endpoint": path, "response": resp.json()}
            except Exception:
                continue

        # Try inference
        resp = requests.post(endpoint, json={"features": [1.0]}, timeout=10)
        if resp.status_code == 200:
            headers = dict(resp.headers)
            return {
                "health": "ok",
                "version_endpoint": "inference",
                "model_version_header": headers.get("x-model-version", "NOT SET"),
                "status_code": resp.status_code,
            }

        return {"health": "unknown", "status_code": resp.status_code}
    except Exception as e:
        return {"health": "unreachable", "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Verify model registry integrity")
    parser.add_argument("--registry-url", required=True,
                       help="MLflow tracking URI (e.g., http://mlflow:5000)")
    parser.add_argument("--endpoint", required=True,
                       help="Model serving endpoint URL")
    parser.add_argument("--model-name", required=True,
                       help="Registered model name")
    parser.add_argument("--expected-version", type=int,
                       help="Specific version expected in production")
    args = parser.parse_args()

    print("=" * 60)
    print("MODEL REGISTRY INTEGRITY CHECK")
    print("=" * 60)
    print(f"Model:     {args.model_name}")
    print(f"Registry:  {args.registry_url}")
    print(f"Endpoint:  {args.endpoint}")
    print()

    # Check registry
    print("1. REGISTRY CHECK (MLflow)...")
    registry = check_mlflow_registry(args.registry_url, args.model_name)
    if "error" in registry:
        print(f"   ❌ {registry['error']}")
    else:
        print(f"   ✅ Production version: v{registry['version']}")
        print(f"   Run ID: {registry['run_id']}")
        print(f"   Source: {registry['source']}")
        creation = registry.get("creation_timestamp")
        if creation:
            created = datetime.fromtimestamp(creation / 1000, tz=timezone.utc)
            age_hours = (datetime.now(timezone.utc) - created).total_seconds() / 3600
            print(f"   Promoted: {created.strftime('%Y-%m-%d %H:%M:%S UTC')} ({age_hours:.1f} hours ago)")

    # Check serving
    print("\n2. SERVING CHECK...")
    serving = check_serving_endpoint(args.endpoint)
    print(f"   Health: {serving.get('health', 'unknown')}")
    if serving["health"] == "ok":
        ver = serving.get("model_version_header", "N/A")
        if ver == "NOT SET":
            print(f"   ⚠ Model version header NOT SET — cannot verify which version is serving")
            print(f"   Fix: add 'x-model-version' response header in serving code")
        else:
            print(f"   Serving version: {ver}")
    elif serving["health"] == "unreachable":
        print(f"   ❌ Endpoint unreachable: {serving.get('error', '')}")
    else:
        print(f"   ⚠ Status: {serving.get('status_code')}")

    # Cross-reference
    print(f"\n{'=' * 60}")
    registry_ver = registry.get("version")
    serving_ver = serving.get("model_version_header")

    issues = []
    if "error" in registry:
        issues.append("REGISTRY: Cannot determine production version")
    if serving["health"] == "unreachable":
        issues.append("SERVING: Endpoint unreachable")
    if serving_ver == "NOT SET":
        issues.append("SERVING: No model version header — blind deployment")
    if registry_ver and serving_ver and str(registry_ver) != str(serving_ver):
        issues.append(f"VERSION MISMATCH: Registry={registry_ver}, Serving={serving_ver}")

    if issues:
        print("VERDICT: ISSUES FOUND ❌")
        for issue in issues:
            print(f"  • {issue}")
        print(f"\nImpact: {'stale model serving' if registry_ver != serving_ver else 'unknown production state'}. "
              f"Users may be receiving predictions from wrong model version.")
        sys.exit(1)
    elif serving_ver == "NOT SET" or "error" in registry:
        print("VERDICT: INCONCLUSIVE ⚠ — cannot fully verify. Add version headers and fix registry access.")
        sys.exit(0)
    else:
        print(f"VERDICT: MATCH ✅ — Registry v{registry_ver} == Serving v{serving_ver}")
        print(f"  Users receive predictions from the correct production model.")
        sys.exit(0)


if __name__ == "__main__":
    main()
