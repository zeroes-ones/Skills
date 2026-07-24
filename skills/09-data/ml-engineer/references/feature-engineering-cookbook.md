# Feature Engineering Cookbook

## Categorical Encoding

| Feature Type | Cardinality | Unknown in Test | Method |
|-------------|------------|-----------------|--------|
| Ordinal (Low/Med/High) | Any | No | `OrdinalEncoder(categories=[['Low','Med','High']])` |
| Ordinal | Any | Yes | `OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)` |
| Nominal | < 15 | No | `OneHotEncoder(drop='first', sparse_output=False)` |
| Nominal | < 15 | Yes | `OneHotEncoder(handle_unknown='ignore', sparse_output=False)` |
| Nominal | 15-50 | Any | `TargetEncoder(smooth=10)` — use with CV to avoid leakage |
| Nominal | > 50 | Any | `CountEncoder` + `TargetEncoder` with high smoothing, or `CatBoost` native |
| High cardinality (zip code) | 1000+ | Any | Group rare categories (< 1%) → "Other", then TargetEncoder |

### Critical: Never Use `LabelEncoder` for Features

```python
# WRONG — LabelEncoder is for target labels only, fails on unseen categories
le = LabelEncoder()
X['category'] = le.fit_transform(X['category'])  # ValueError on test if new category

# RIGHT — OrdinalEncoder with unknown handling
from sklearn.preprocessing import OrdinalEncoder
enc = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
X_train_enc = enc.fit_transform(X_train[['category']])
X_test_enc = enc.transform(X_test[['category']])  # New categories → -1
```

## Numeric Scaling

| Data Characteristic | Scaler | When |
|--------------------|--------|------|
| Normal-like distribution | `StandardScaler` | PCA, linear models, NNs expecting ~ N(0,1) |
| Heavy outliers | `RobustScaler` | Default for real-world data with outliers |
| Bounded range needed | `MinMaxScaler` | NNs with sigmoid/tanh, image pixels |
| Sparse data | `MaxAbsScaler` | TF-IDF, count vectors (preserves sparsity) |
| Heavy tail, log-normal | `PowerTransformer(method='yeo-johnson')` | Skewed financial data, counts |
| Quantile normalization | `QuantileTransformer` | Non-parametric, forces uniform/normal distribution |

## Missing Value Imputation

| Missing Pattern | Strategy | Code |
|----------------|----------|------|
| < 5% missing, numeric | Median imputation | `SimpleImputer(strategy='median')` |
| < 5% missing, categorical | Mode imputation | `SimpleImputer(strategy='most_frequent')` |
| 5-30% missing | KNN imputation | `KNNImputer(n_neighbors=5)` |
| > 30% missing | Drop or flag | `df['has_X'] = df['X'].isna().astype(int)` + impute |
| Missingness is informative | Indicator column | Add `is_missing` flag, keep missing as NaN for tree models |
| MNAR (missing not at random) | Domain-specific imputation | Model the missingness mechanism |

### Always: Create Missingness Indicators

Even when imputing, create a binary flag. Tree models can use it:
```python
for col in df.columns[df.isnull().any()]:
    df[f'{col}_is_missing'] = df[col].isna().astype(int)
```

## Feature Selection

| Goal | Method | Code |
|------|--------|------|
| Remove constant features | Variance threshold | `VarianceThreshold(threshold=0)` |
| Remove correlated features | Correlation filter | Drop if |r| > 0.95, keep one with higher target correlation |
| Univariate relevance | Mutual information | `mutual_info_classif(X, y)` select top-k |
| Model-based selection | Tree feature importance | `SelectFromModel(XGBClassifier(), threshold='median')` |
| Recursive elimination | RFE with CV | `RFECV(estimator, step=1, cv=5, scoring='f1')` |
| Regularization | L1 penalty | `LogisticRegression(penalty='l1', solver='saga', C=1.0)` |

## When to Engineer Interaction Features

Add interaction features when:
1. Domain knowledge says features interact (e.g., `price_per_sqft = price / area`)
2. Tree model depth is limited and can't discover deep interactions
3. Using linear models (they can't model interactions without explicit features)

```python
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
X_interact = poly.fit_transform(X[['f1', 'f2', 'f3']])
```
