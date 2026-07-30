from pathlib import Path

import pandas as pd

from power_quality_loss.model import FEATURE_COLUMNS, TARGET_COLUMN, load_model_data


ROOT = Path(__file__).resolve().parents[1]


def test_published_model_data_uses_english_schema_and_preserves_row_count():
    data_path = ROOT / "data" / "processed" / "model-features.csv"

    features, target = load_model_data(data_path)

    assert tuple(features.columns) == FEATURE_COLUMNS
    assert target.name == TARGET_COLUMN
    assert len(features) == 2_343


def test_published_raw_data_contains_expected_measurement_count():
    raw_path = ROOT / "data" / "raw" / "power-quality-meter.csv"

    frame = pd.read_csv(raw_path)

    assert len(frame) == 2_343
    assert "Active Power Total Avg" in frame.columns
