"""Reproducible training for the cost model."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


FEATURE_COLUMNS = (
    "reactive_energy_cost",
    "imbalance_cost",
    "harmonic_cost",
    "neutral_current_cost",
)
TARGET_COLUMN = "baseline_active_energy_cost"


def load_model_data(path: str | Path) -> tuple[pd.DataFrame, pd.Series]:
    frame = pd.read_csv(path)
    required = [*FEATURE_COLUMNS, TARGET_COLUMN]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    numeric = frame[required].apply(pd.to_numeric, errors="coerce")
    if numeric.isna().any().any():
        raise ValueError("The dataset contains missing or non-numeric values")
    if not np.isfinite(numeric.to_numpy()).all():
        raise ValueError("The dataset contains infinite values")
    return numeric[list(FEATURE_COLUMNS)], numeric[TARGET_COLUMN]


def ordered_holdout(
    features: pd.DataFrame,
    target: pd.Series,
    test_fraction: float = 0.2,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split by row order to preserve the inherited time sequence."""

    if not 0.05 <= test_fraction <= 0.5:
        raise ValueError("test_fraction must be between 0.05 and 0.5")
    if len(features) != len(target) or len(features) < 10:
        raise ValueError("At least 10 aligned rows are required")
    split_index = int(len(features) * (1.0 - test_fraction))
    return (
        features.iloc[:split_index].copy(),
        features.iloc[split_index:].copy(),
        target.iloc[:split_index].copy(),
        target.iloc[split_index:].copy(),
    )


def regression_metrics(actual: np.ndarray | pd.Series, predicted: np.ndarray) -> dict[str, float]:
    actual_array = np.asarray(actual, dtype=float)
    predicted_array = np.asarray(predicted, dtype=float)
    if actual_array.shape != predicted_array.shape:
        raise ValueError("actual and predicted must have the same shape")

    absolute_error = np.abs(actual_array - predicted_array)
    nonzero = actual_array != 0.0
    denominator = np.abs(actual_array).sum()
    symmetric_denominator = np.abs(actual_array) + np.abs(predicted_array)
    smape_terms = np.divide(
        2.0 * absolute_error,
        symmetric_denominator,
        out=np.zeros_like(absolute_error),
        where=symmetric_denominator != 0.0,
    )

    return {
        "mae": float(mean_absolute_error(actual_array, predicted_array)),
        "rmse": float(mean_squared_error(actual_array, predicted_array) ** 0.5),
        "r2": float(r2_score(actual_array, predicted_array)),
        "mape_nonzero_pct": (
            float(np.mean(absolute_error[nonzero] / np.abs(actual_array[nonzero])) * 100.0)
            if nonzero.any()
            else 0.0
        ),
        "wape_pct": float(absolute_error.sum() / denominator * 100.0) if denominator else 0.0,
        "smape_pct": float(smape_terms.mean() * 100.0),
        "zero_target_rows": int((~nonzero).sum()),
    }


def train_xgboost(
    data_path: str | Path,
    model_output: str | Path,
    report_output: str | Path,
    test_fraction: float = 0.2,
) -> dict[str, Any]:
    """Train XGBoost with an ordered holdout and save model plus metrics."""

    try:
        import xgboost as xgb
    except ImportError as exc:  # pragma: no cover - depends on optional installation
        raise RuntimeError(
            'XGBoost is not installed. Run: python -m pip install -e ".[xgboost]"'
        ) from exc

    data_path = Path(data_path)
    features, target = load_model_data(data_path)
    x_train, x_test, y_train, y_test = ordered_holdout(features, target, test_fraction)
    train_matrix = xgb.DMatrix(x_train, label=y_train, feature_names=list(FEATURE_COLUMNS))
    test_matrix = xgb.DMatrix(x_test, label=y_test, feature_names=list(FEATURE_COLUMNS))

    parameters = {
        "booster": "gbtree",
        "objective": "reg:squarederror",
        "eval_metric": "rmse",
        "subsample": 0.7,
        "colsample_bytree": 0.7,
        "eta": 0.08,
        "max_depth": 7,
        "gamma": 1.0,
        "reg_alpha": 23.0,
        "seed": 42,
    }
    booster = xgb.train(
        parameters,
        train_matrix,
        num_boost_round=400,
        evals=[(train_matrix, "train"), (test_matrix, "holdout")],
        early_stopping_rounds=30,
        verbose_eval=False,
    )
    predictions = booster.predict(test_matrix, iteration_range=(0, booster.best_iteration + 1))
    metrics = regression_metrics(y_test, predictions)
    report: dict[str, Any] = {
        "data": {
            "path": str(data_path),
            "sha256": hashlib.sha256(data_path.read_bytes()).hexdigest(),
            "rows": len(features),
        },
        "features": list(FEATURE_COLUMNS),
        "target": TARGET_COLUMN,
        "split": "ordered_holdout",
        "test_fraction": test_fraction,
        "train_rows": len(x_train),
        "test_rows": len(x_test),
        "parameters": parameters,
        "best_iteration": int(booster.best_iteration),
        "metrics": metrics,
        "runtime": {
            "python": platform.python_version(),
            "xgboost": xgb.__version__,
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scikit_learn": importlib.metadata.version("scikit-learn"),
        },
    }

    model_path = Path(model_output)
    report_path = Path(report_output)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    booster.save_model(model_path)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report
