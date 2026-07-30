#!/usr/bin/env python3
"""Reproduce the public data audit, legacy formulas, and XGBoost training.

This script is the executable English reconstruction of the code used for the
2021 project. It keeps the historical formulas for traceability while using
the corrected four-feature model, ordered holdout, finite metrics, and native
JSON model format.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from power_quality_loss.legacy import (
    calculate_legacy_harmonic_score,
    calculate_legacy_imbalance,
)
from power_quality_loss.model import train_xgboost
from power_quality_loss.quality import audit_measurements


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW_DATA = ROOT / "data" / "raw" / "power-quality-meter.csv"
DEFAULT_MODEL_DATA = ROOT / "data" / "processed" / "model-features.csv"
DEFAULT_MODEL_OUTPUT = ROOT / "models" / "xgboost_model.json"
DEFAULT_REPORT_OUTPUT = ROOT / "reports" / "model-report.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reproduce the ALUCOL power-quality prototype audit and model."
    )
    parser.add_argument("--raw-data", type=Path, default=DEFAULT_RAW_DATA)
    parser.add_argument("--model-data", type=Path, default=DEFAULT_MODEL_DATA)
    parser.add_argument("--model-output", type=Path, default=DEFAULT_MODEL_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT_OUTPUT)
    parser.add_argument("--test-fraction", type=float, default=0.2)
    return parser


def first_row_reconstruction(frame: pd.DataFrame) -> dict[str, object]:
    """Reproduce the first spreadsheet row from the real analyzer export."""

    row = frame.iloc[0]
    voltages = (
        row["Vrms ph-n AN Avg"],
        row["Vrms ph-n BN Avg"],
        row["Vrms ph-n CN Avg"],
    )
    currents = (
        row["Current A Avg"],
        row["Current B Avg"],
        row["Current C Avg"],
    )

    imbalance = calculate_legacy_imbalance(
        voltages,
        currents,
        row["Cos Phi AN Avg"],
    )
    harmonic = calculate_legacy_harmonic_score(
        voltages,
        currents,
        power_factor=row["Cos Phi BN Avg"],
    )
    return {
        "source_row": 0,
        "imbalance": imbalance.to_dict(),
        "harmonic": harmonic.to_dict(),
        "note": (
            "The harmonic result is a dimensionally inconsistent historical "
            "score, not physical power."
        ),
    }


def main() -> int:
    args = build_parser().parse_args()
    raw = pd.read_csv(args.raw_data)

    result = {
        "project": {
            "company": "Aluminios de Colombia S.A. – ALUCOL",
            "development": "ZION ING / Zircular",
            "measurement_year": 2019,
            "prototype_year": 2021,
            "audit_year": 2026,
        },
        "data_audit": audit_measurements(raw),
        "first_row_reconstruction": first_row_reconstruction(raw),
        "model": train_xgboost(
            data_path=args.model_data,
            model_output=args.model_output,
            report_output=args.report_output,
            test_fraction=args.test_fraction,
        ),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
