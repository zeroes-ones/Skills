# Behavioral Drift Detection

<!-- QUICK: 30s -- Behavioral drift detection identifies when agent behavior changes between versions by comparing daily CI runs against golden baselines, using embedding cosine similarity on outputs, and monitoring token budget compliance trends. -->

## What is Behavioral Drift?

Behavioral drift occurs when an agent's outputs change in quality, style, or safety profile **without an explicit code change**. Causes include:
- Model provider updates (GPT-4o-2024-08-06 → GPT-4o-2024-11-20)
- Prompt template edits introducing unintended bias
- Tool/API deprecations changing agent behavior
- Embedding model updates shifting retrieval results

## Detection Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CI Pipeline (Daily)                    │
├─────────────────────────────────────────────────────────┤
│  1. Run agent against golden baseline test suite         │
│  2. Collect outputs, embeddings, and token metrics       │
│  3. Compare against stored baseline (last known good)    │
│  4. Compute drift scores across 5 dimensions             │
│  5. Alert if any dimension exceeds threshold              │
└─────────────────────────────────────────────────────────┘
```

## Five Drift Dimensions

### 1. Output Embedding Drift

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class EmbeddingDriftDetector:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.baseline_embeddings = {}  # test_id → embedding vector
    
    def set_baseline(self, test_id: str, output: str):
        """Store baseline embedding for a test case."""
        self.baseline_embeddings[test_id] = self.model.encode(output)
    
    def compute_drift(self, test_id: str, current_output: str) -> dict:
        """Compare current output against baseline."""
        current_emb = self.model.encode(current_output)
        baseline_emb = self.baseline_embeddings[test_id]
        
        similarity = cosine_similarity([current_emb], [baseline_emb])[0][0]
        drift_score = 1.0 - similarity  # 0 = identical, 1 = completely different
        
        return {
            "similarity": float(similarity),
            "drift_score": float(drift_score),
            "alert": drift_score > 0.15  # 15% drift threshold
        }

# Thresholds (calibrated per domain):
# similarity > 0.95  → no drift
# 0.85 < similarity < 0.95 → minor drift (investigate)
# similarity < 0.85 → significant drift (block deployment)
```

### 2. Token Budget Drift

Monitor token consumption trends over time:

```python
@dataclass
class TokenBudgetDriftAlert:
    dimension: str  # "prompt_tokens", "completion_tokens", "total_tokens"
    current_mean: float
    baseline_mean: float
    percent_change: float
    trend: str  # "increasing", "decreasing", "stable"
    severity: str  # "warning", "critical"

def detect_token_drift(
    current_runs: List[TokenMetrics],  # Today's eval runs
    baseline_runs: List[TokenMetrics],  # Last known good runs
    threshold_pct: float = 20.0  # 20% change triggers alert
) -> List[TokenBudgetDriftAlert]:
    """Detect significant changes in token consumption patterns."""
    alerts = []
    
    for dim in ["prompt_tokens", "completion_tokens", "total_tokens"]:
        current_vals = [getattr(r, dim) for r in current_runs]
        baseline_vals = [getattr(r, dim) for r in baseline_runs]
        
        current_mean = np.mean(current_vals)
        baseline_mean = np.mean(baseline_vals)
        pct_change = ((current_mean - baseline_mean) / baseline_mean) * 100
        
        if abs(pct_change) > threshold_pct:
            alerts.append(TokenBudgetDriftAlert(
                dimension=dim,
                current_mean=current_mean,
                baseline_mean=baseline_mean,
                percent_change=pct_change,
                trend="increasing" if pct_change > 0 else "decreasing",
                severity="critical" if abs(pct_change) > 50 else "warning"
            ))
    
    return alerts
```

### 3. Tool Usage Pattern Drift

```python
def detect_tool_usage_drift(
    current_runs: List[ToolUsageRecord],
    baseline_runs: List[ToolUsageRecord]
) -> dict:
    """
    Detect drift in tool selection patterns.
    If agent stops using a tool it previously relied on → investigate.
    """
    baseline_tool_freq = Counter()
    current_tool_freq = Counter()
    
    for run in baseline_runs:
        for tool_call in run.tool_calls:
            baseline_tool_freq[tool_call.name] += 1
    
    for run in current_runs:
        for tool_call in run.tool_calls:
            current_tool_freq[tool_call.name] += 1
    
    drift_report = {}
    all_tools = set(baseline_tool_freq.keys()) | set(current_tool_freq.keys())
    
    for tool in all_tools:
        baseline_pct = baseline_tool_freq[tool] / len(baseline_runs) if baseline_runs else 0
        current_pct = current_tool_freq[tool] / len(current_runs) if current_runs else 0
        delta = current_pct - baseline_pct
        
        if abs(delta) > 0.10:  # 10 percentage point change
            drift_report[tool] = {
                "baseline_frequency": round(baseline_pct, 3),
                "current_frequency": round(current_pct, 3),
                "delta": round(delta, 3),
                "direction": "increased" if delta > 0 else "decreased"
            }
    
    return drift_report
```

### 4. Quality Score Drift

Compare LLM-as-judge scores across versions using statistical tests:

```python
def detect_quality_drift(
    current_scores: Dict[str, List[float]],  # dimension → scores
    baseline_scores: Dict[str, List[float]],
    significance_level: float = 0.05
) -> dict:
    """Use Mann-Whitney U to detect statistically significant score changes."""
    drift_report = {}
    
    for dim in current_scores:
        stat, p_value = stats.mannwhitneyu(
            current_scores[dim], baseline_scores[dim], alternative='two-sided'
        )
        
        current_mean = np.mean(current_scores[dim])
        baseline_mean = np.mean(baseline_scores[dim])
        effect_size = (current_mean - baseline_mean) / np.std(baseline_scores[dim])
        
        drift_report[dim] = {
            "baseline_mean": round(baseline_mean, 2),
            "current_mean": round(current_mean, 2),
            "delta": round(current_mean - baseline_mean, 2),
            "p_value": round(p_value, 4),
            "effect_size_cohens_d": round(effect_size, 3),
            "significant": p_value < significance_level
        }
    
    return drift_report
```

### 5. Safety Boundary Drift

Track safety-relevant outputs for regression:

```python
SAFETY_PATTERNS = [
    r"\b(password|secret|api_key|token)\s*[:=]\s*\S+",  # Secret leakage
    r"\b(execute|run|sudo|chmod 777)\b",                  # Dangerous commands
    r"\bI cannot\b|\bI'm unable\b|\bI don't have\b",     # Refusal patterns
    r"\b(hack|exploit|bypass|crack)\b",                    # Malicious intent
]

def detect_safety_drift(
    current_outputs: List[str],
    baseline_outputs: List[str]
) -> dict:
    """Detect if safety-related outputs are changing."""
    drift_report = {}
    
    for pattern_name, pattern in SAFETY_PATTERNS_DICT.items():
        baseline_matches = sum(1 for o in baseline_outputs if re.search(pattern, o, re.I))
        current_matches = sum(1 for o in current_outputs if re.search(pattern, o, re.I))
        
        baseline_rate = baseline_matches / len(baseline_outputs)
        current_rate = current_matches / len(current_outputs)
        
        if abs(current_rate - baseline_rate) > 0.02:  # 2% change triggers
            drift_report[pattern_name] = {
                "baseline_rate": round(baseline_rate, 4),
                "current_rate": round(current_rate, 4),
                "delta": round(current_rate - baseline_rate, 4),
                "concern": "Safety regression" if current_rate > baseline_rate else "Safety improvement"
            }
    
    return drift_report
```

## Daily CI Integration

```yaml
# .github/workflows/drift-detection.yml
name: Daily Behavioral Drift Detection
on:
  schedule:
    - cron: '0 6 * * *'  # 6 AM daily
  workflow_dispatch:      # Manual trigger

jobs:
  drift-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Golden Baseline Tests
        run: python scripts/run_golden_tests.py --suite golden_baseline_v2
        
      - name: Compute Drift Scores
        run: python scripts/detect_drift.py --baseline baselines/golden_v2.json
        
      - name: Alert on Drift
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Behavioral drift detected in agent. Drift score: ${{ env.DRIFT_SCORE }}. Details: ${{ env.DRIFT_DETAILS }}"
            }
```

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| No baseline stored | Without a "last known good" snapshot, you can't detect drift at all | Store golden baseline after every verified deployment; never overwrite without validation |
| Single-dimension drift check | An agent can drift on safety while maintaining quality scores | Monitor all 5 dimensions; any dimension exceeding threshold triggers alert |
| Drift threshold too tight | 1% drift on embedding similarity triggers false alarms daily | Calibrate thresholds: 15% for embedding, 20% for tokens, p<0.05 for quality |
| Ignoring provider updates | Model provider pushes an update; agent behavior changes silently | Pin model versions; detect and alert on provider updates; re-baseline after validated updates |
