# Hyperparameter Search Spaces

## XGBoost

```python
param_space = {
    'max_depth': trial.suggest_int('max_depth', 3, 12),
    'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
    'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
    'subsample': trial.suggest_float('subsample', 0.6, 1.0),
    'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
    'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
    'gamma': trial.suggest_float('gamma', 0, 5),
    'reg_alpha': trial.suggest_float('reg_alpha', 1e-8, 10, log=True),
    'reg_lambda': trial.suggest_float('reg_lambda', 1e-8, 10, log=True),
}
```

## LightGBM

```python
param_space = {
    'num_leaves': trial.suggest_int('num_leaves', 20, 300),
    'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
    'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
    'min_child_samples': trial.suggest_int('min_child_samples', 5, 100),
    'subsample': trial.suggest_float('subsample', 0.6, 1.0),
    'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
    'reg_alpha': trial.suggest_float('reg_alpha', 1e-8, 10, log=True),
    'reg_lambda': trial.suggest_float('reg_lambda', 1e-8, 10, log=True),
    'min_split_gain': trial.suggest_float('min_split_gain', 0, 0.5),
}
```

## CatBoost

```python
param_space = {
    'depth': trial.suggest_int('depth', 4, 10),
    'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
    'iterations': trial.suggest_int('iterations', 100, 1000),
    'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1, 10, log=True),
    'border_count': trial.suggest_int('border_count', 32, 255),
    'random_strength': trial.suggest_float('random_strength', 0, 10),
}
```

## Random Forest

```python
param_space = {
    'n_estimators': trial.suggest_int('n_estimators', 100, 500),
    'max_depth': trial.suggest_int('max_depth', 5, 30),
    'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
    'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 20),
    'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None]),
}
```

## Neural Network (PyTorch)

```python
param_space = {
    'learning_rate': trial.suggest_float('lr', 1e-5, 1e-2, log=True),
    'batch_size': trial.suggest_categorical('batch_size', [16, 32, 64, 128, 256]),
    'optimizer': trial.suggest_categorical('optimizer', ['Adam', 'AdamW', 'SGD']),
    'weight_decay': trial.suggest_float('weight_decay', 1e-6, 1e-2, log=True),
    'dropout': trial.suggest_float('dropout', 0.0, 0.5),
    'hidden_size': trial.suggest_categorical('hidden_size', [64, 128, 256, 512]),
    'num_layers': trial.suggest_int('num_layers', 1, 5),
}

# Adam-specific
if optimizer in ['Adam', 'AdamW']:
    param_space['betas'] = trial.suggest_categorical(
        'betas', [(0.9, 0.999), (0.9, 0.99), (0.95, 0.999)]
    )

# LR schedule
param_space['lr_schedule'] = trial.suggest_categorical(
    'lr_schedule', ['cosine', 'step', 'plateau', 'constant']
)
```

## SVM

```python
param_space = {
    'C': trial.suggest_float('C', 1e-3, 1e3, log=True),
    'gamma': trial.suggest_float('gamma', 1e-4, 1e1, log=True),
    'kernel': trial.suggest_categorical('kernel', ['rbf', 'poly', 'sigmoid']),
}
```

## Tuning Strategy

| Budget | Method | Configuration |
|--------|--------|--------------|
| < 10 trials | Manual tuning | Expert-guided, one param at a time |
| 10-50 trials | Random search | Wider exploration, lower precision |
| 50-500 trials | Optuna (TPE sampler) | Bayesian optimization, prunes poor trials |
| > 500 trials | Optuna + Hyperband | Combines Bayesian search with early stopping |

**Pruning:** Use `optuna.integration.XGBoostPruningCallback` or `LightGBMPruningCallback` to stop unpromising trials early — cuts tuning time by 40-60%.

**Never:** `GridSearchCV` with > 3 hyperparameters. 10 values × 10 values × 10 values = 1000 combinations. Use Optuna's adaptive exploration instead.
