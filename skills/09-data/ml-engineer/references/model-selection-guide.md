# Model Selection Guide
## When to Use Each Algorithm

### Decision Framework

```
data type? → tabular → sample size? → < 1K → LogisticRegression / DecisionTree (max_depth=3)
                                    → 1K-100K → XGBoost (robust default)
                                    → 100K-1M → LightGBM (fastest)
                                    → > 1M → LightGBM + GPU
           → images → pretrained CNN (ResNet50, EfficientNet-B3)
           → text → transformer (BERT-base, RoBERTa-base) for classification
                      → sparse (TF-IDF + LinearSVC) for keyword-heavy tasks
           → time series → statistical (ARIMA, Prophet) for trend/seasonality
                         → deep (LSTM, TFT) for complex patterns, multivariate
```

### Algorithm Comparison Matrix

| Algorithm | Data Size | Interpretability | Speed | Handles Missing | GPU | Best For |
|-----------|-----------|-----------------|-------|----------------|-----|----------|
| LogisticRegression | Any | ★★★★★ | ★★★★★ | No | No | Baseline, interpretability-critical |
| Decision Tree (depth ≤ 3) | < 100K | ★★★★★ | ★★★★★ | Yes | No | Medical, credit, legal decisions |
| Random Forest | < 500K | ★★★ | ★★★ | Yes | Partial | Robust default, wide feature sets |
| XGBoost | < 1M | ★★★ | ★★★★ | Yes | Yes | Competition winner, tabular gold standard |
| LightGBM | 1K-10M+ | ★★★ | ★★★★★ | Yes | Yes | Large datasets, many features |
| CatBoost | < 1M | ★★★ | ★★★ | Yes | Yes | Many categorical features (50+) |
| SVM (RBF) | < 10K | ★★ | ★ | No | No | Clear margins, few samples, many features |
| KNN | < 50K | ★ | ★★ | No | No | Simple, non-parametric baseline |
| MLP (2-3 layers) | > 10K | ★ | ★★ | No | Yes | Tabular deep learning, complex interactions |
| TabNet | > 50K | ★★ | ★★ | No | Yes | Attention-based tabular, interpretable |
| ResNet/EfficientNet | > 1K images | ★ | ★★★ | N/A | Yes | Image classification (transfer learning) |
| BERT/RoBERTa | > 1K texts | ★ | ★★ | N/A | Yes | Text classification, NER |
| LSTM/GRU | > 5K sequences | ★ | ★★ | N/A | Yes | Sequence prediction, time series |
| XGBoost + embedding | Any tabular | ★★ | ★★★ | Yes | Yes | Combined structured + unstructured features |

### When to Upgrade from LogisticRegression

Only move to a more complex model when:
1. You've exhausted feature engineering (interactions, polynomial features, domain-specific transforms)
2. The logistic regression residuals show systematic patterns (not random noise)
3. The simpler model's performance is below business requirements
4. You have enough data to support the more complex model (rule of thumb: 50× number of parameters)

### Neural Network Checklist

Before using a neural network:
- [ ] Is dataset > 10K samples? (NNs are data-hungry)
- [ ] Do features have non-linear interactions not capturable by tree ensembles?
- [ ] Is interpretability not a hard requirement?
- [ ] Do you have GPU access for training?
- [ ] Have you tried XGBoost/LightGBM first? (Often equal or better on tabular data)
