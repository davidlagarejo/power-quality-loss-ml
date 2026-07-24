import numpy as np
import pandas as pd
import pytest

from power_quality_loss.model import FEATURE_COLUMNS, ordered_holdout, regression_metrics


def test_ordered_holdout_preserves_order():
    features = pd.DataFrame({column: range(10) for column in FEATURE_COLUMNS})
    target = pd.Series(range(10), name="costolineabase")

    x_train, x_test, y_train, y_test = ordered_holdout(features, target, 0.2)

    assert list(x_train.index) == list(range(8))
    assert list(x_test.index) == [8, 9]
    assert list(y_train) == list(range(8))
    assert list(y_test) == [8, 9]


def test_metrics_remain_finite_when_target_contains_zero():
    metrics = regression_metrics(np.array([0.0, 100.0]), np.array([5.0, 90.0]))

    assert metrics["zero_target_rows"] == 1
    assert metrics["mape_nonzero_pct"] == pytest.approx(10.0)
    assert all(np.isfinite(value) for value in metrics.values())
