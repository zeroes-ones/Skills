# Evaluation Metrics Cheatsheet

## Metric Selection by Problem Type

### Binary Classification

| Metric | Use When | Don't Use When |
|--------|----------|---------------|
| Accuracy | Classes balanced (40-60%) | Imbalanced data (minority < 30%) |
| Precision | False positives are costly (fraud alerts, spam) | You care about catching all positives |
| Recall (Sensitivity) | False negatives are costly (disease detection, safety) | You care about alert fatigue |
| F1 Score | Need a balance of precision and recall | Unequal cost of FP vs FN |
| Fβ (beta < 1) | FP more costly than FN | — |
| Fβ (beta > 1) | FN more costly than FP | — |
| ROC-AUC | General ranking quality, balanced data | Imbalanced data (use PR-AUC instead) |
| PR-AUC | Imbalanced data, rare positive class | Balanced data (ROC-AUC is more interpretable) |
| Log Loss / Brier | Probability quality matters (risk scores, betting) | Only ranking matters |
| MCC (Matthews) | Single balanced metric for imbalanced data | Need per-class breakdown |

### Multiclass Classification

| Metric | Macro | Micro | Weighted |
|--------|-------|-------|----------|
| Precision/Recall/F1 | Each class equal weight (minority classes matter) | Aggregate contributions (majority class dominates) | Weighted by class frequency (compromise) |

**Rule of thumb:** Use macro for imbalanced multiclass (you care about all classes). Use weighted when class frequency reflects real-world importance.

### Regression

| Metric | Use When | Don't Use When |
|--------|----------|---------------|
| RMSE | Errors are symmetric, normal distribution | Heavy outliers (RMSE squares errors) |
| MAE | Robust to outliers, interpretable in original units | Larger errors need extra penalty |
| MAPE | Target > 0, interpretable as % error | Target can be zero or negative |
| R² | Comparing models on same data | Comparing across different datasets (R² is data-dependent) |
| MedAE | Heavy outliers, non-normal errors | Need sensitivity to tail errors |

### Ranking

| Metric | Description |
|--------|-------------|
| NDCG@k | Discounted cumulative gain — higher ranks matter more |
| MAP@k | Mean average precision — precision at each relevant position |
| MRR | Mean reciprocal rank — position of first relevant item |
| Hit Rate@k | Fraction of users with at least one relevant item in top-k |

## Per-Class Metrics Are Mandatory

```python
from sklearn.metrics import classification_report, ConfusionMatrixDisplay

# Always run both
print(classification_report(y_test, y_pred, target_names=class_names))
ConfusionMatrixDisplay.from_predictions(y_test, y_pred, display_labels=class_names)
```

## Confidence Intervals via Bootstrap

```python
import numpy as np
from sklearn.utils import resample

def bootstrap_metric(y_true, y_pred, metric_fn, n_iterations=1000, alpha=0.05):
    """Compute 95% CI for any metric via bootstrap."""
    stats = []
    n = len(y_true)
    for _ in range(n_iterations):
        idx = resample(range(n), n_samples=n, random_state=_)
        stat = metric_fn(y_true[idx], y_pred[idx])
        stats.append(stat)
    lower = np.percentile(stats, alpha/2 * 100)
    upper = np.percentile(stats, (1 - alpha/2) * 100)
    return np.mean(stats), (lower, upper)

# Example
from sklearn.metrics import f1_score
mean_f1, (ci_low, ci_high) = bootstrap_metric(y_test, y_pred, f1_score)
print(f"F1: {mean_f1:.3f} [{ci_low:.3f}, {ci_high:.3f}]")
```

## Overfitting Detection

```
|train_f1 - test_f1| < 0.02 → Healthy
|train_f1 - test_f1| 0.02-0.05 → Mild overfitting (add regularization)
|train_f1 - test_f1| 0.05-0.10 → Moderate overfitting (reduce capacity + regularization)
|train_f1 - test_f1| > 0.10 → Severe overfitting (more data, reduce model, stronger regularization)
```
