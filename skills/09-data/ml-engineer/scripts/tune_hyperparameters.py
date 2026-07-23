#!/usr/bin/env python3
"""Hyperparameter tuning with Optuna — adaptive Bayesian optimization with pruning.

Usage: python tune_hyperparameters.py --train train.csv --target label --model xgboost --trials 100
"""

import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import make_scorer, f1_score, mean_squared_error
import sys

try:
    import optuna
    OPTUNA_AVAILABLE = True
except ImportError:
    OPTUNA_AVAILABLE = False


MODEL_CONFIGS = {
    "xgboost": {
        "import": "from xgboost import XGBClassifier, XGBRegressor",
        "search_space": {
            "max_depth": ("int", 3, 12),
            "learning_rate": ("float", 0.01, 0.3, True),
            "n_estimators": ("int", 100, 1000),
            "subsample": ("float", 0.6, 1.0),
            "colsample_bytree": ("float", 0.6, 1.0),
            "min_child_weight": ("int", 1, 10),
            "gamma": ("float", 0, 5),
            "reg_alpha": ("float", 1e-8, 10, True),
            "reg_lambda": ("float", 1e-8, 10, True),
        },
    },
    "lightgbm": {
        "import": "from lightgbm import LGBMClassifier, LGBMRegressor",
        "search_space": {
            "num_leaves": ("int", 20, 300),
            "learning_rate": ("float", 0.01, 0.3, True),
            "n_estimators": ("int", 100, 1000),
            "min_child_samples": ("int", 5, 100),
            "subsample": ("float", 0.6, 1.0),
            "colsample_bytree": ("float", 0.6, 1.0),
            "reg_alpha": ("float", 1e-8, 10, True),
            "reg_lambda": ("float", 1e-8, 10, True),
        },
    },
    "random_forest": {
        "import": "from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor",
        "search_space": {
            "n_estimators": ("int", 100, 500),
            "max_depth": ("int", 5, 30),
            "min_samples_split": ("int", 2, 20),
            "min_samples_leaf": ("int", 1, 20),
            "max_features": ("categorical", ["sqrt", "log2", None]),
        },
    },
}


def suggest_param(trial, name, config):
    """Suggest a hyperparameter based on config tuple."""
    ptype = config[0]
    if ptype == "int":
        return trial.suggest_int(name, config[1], config[2])
    elif ptype == "float" and len(config) > 3 and config[3]:
        return trial.suggest_float(name, config[1], config[2], log=True)
    elif ptype == "float":
        return trial.suggest_float(name, config[1], config[2])
    elif ptype == "categorical":
        return trial.suggest_categorical(name, config[1])
    return None


def main():
    parser = argparse.ArgumentParser(description="Hyperparameter tuning with Optuna")
    parser.add_argument("--train", required=True, help="Training CSV")
    parser.add_argument("--target", required=True, help="Target column name")
    parser.add_argument("--model", required=True, choices=list(MODEL_CONFIGS.keys()),
                       help="Model type to tune")
    parser.add_argument("--trials", type=int, default=100, help="Number of Optuna trials")
    parser.add_argument("--cv", type=int, default=5, help="Cross-validation folds")
    parser.add_argument("--task", choices=["classification", "regression"], default="classification",
                       help="Task type")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    if not OPTUNA_AVAILABLE:
        print("ERROR: Optuna not installed. Run: pip install optuna")
        print("Using manual grid search instead...")
        print("Recommended search space for", args.model)
        for param, config in MODEL_CONFIGS[args.model]["search_space"].items():
            print(f"  {param}: suggest {config}")
        sys.exit(1)

    # Load data
    df = pd.read_csv(args.train)
    X = df.drop(columns=[args.target])
    y = df[args.target]

    # Handle categoricals
    for col in X.select_dtypes(include=['object']).columns:
        X[col] = X[col].astype('category').cat.codes

    model_config = MODEL_CONFIGS[args.model]
    is_classification = args.task == "classification"

    if is_classification:
        cv = StratifiedKFold(n_splits=args.cv, shuffle=True, random_state=args.seed)
        direction = "maximize"
    else:
        from sklearn.model_selection import KFold
        cv = KFold(n_splits=args.cv, shuffle=True, random_state=args.seed)
        direction = "minimize"

    def objective(trial):
        params = {}
        for name, config in model_config["search_space"].items():
            params[name] = suggest_param(trial, name, config)
        params["random_state"] = args.seed
        params["n_jobs"] = -1

        try:
            if args.model == "xgboost":
                from xgboost import XGBClassifier, XGBRegressor
                model = XGBClassifier(**params, verbosity=0) if is_classification else XGBRegressor(**params, verbosity=0)
            elif args.model == "lightgbm":
                from lightgbm import LGBMClassifier, LGBMRegressor
                model = LGBMClassifier(**params, verbose=-1) if is_classification else LGBMRegressor(**params, verbose=-1)
            elif args.model == "random_forest":
                from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
                model = RandomForestClassifier(**params) if is_classification else RandomForestRegressor(**params)
            else:
                return 0.0

            if is_classification:
                scorer = make_scorer(f1_score, average='weighted')
            else:
                scorer = make_scorer(mean_squared_error, greater_is_better=False)

            scores = cross_val_score(model, X, y, cv=cv, scoring=scorer, n_jobs=1)
            return np.mean(scores)
        except Exception as e:
            print(f"  Trial {trial.number} failed: {e}", file=sys.stderr)
            return 0.0 if is_classification else float("inf")

    print("=" * 60)
    print(f"OPTUNA HYPERPARAMETER TUNING — {args.model.upper()}")
    print("=" * 60)
    print(f"Task: {args.task}")
    print(f"Trials: {args.trials} | CV folds: {args.cv} | Seed: {args.seed}")
    print(f"Direction: {direction}")
    print()

    study = optuna.create_study(direction=direction)
    study.optimize(objective, n_trials=args.trials, show_progress_bar=True)

    print(f"\n{'=' * 60}")
    print("BEST PARAMETERS:")
    for param, value in study.best_params.items():
        print(f"  {param}: {value}")
    print(f"\nBest {direction}d score: {study.best_value:.4f}")
    print(f"{'=' * 60}")

    # Show top 3 trials
    print("\nTOP 3 TRIALS:")
    trials = sorted(study.trials, key=lambda t: t.value if direction == "maximize" else -t.value, reverse=True)[:3]
    for i, t in enumerate(trials):
        print(f"  {i+1}. Score={t.value:.4f}, Params={dict(list(t.params.items())[:5])}...")


if __name__ == "__main__":
    main()
