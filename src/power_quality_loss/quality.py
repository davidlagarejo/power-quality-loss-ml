"""Validaciones básicas para exportaciones de analizadores de red."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


PHASE_VOLTAGE_COLUMNS = (
    "Vrms ph-n AN Avg",
    "Vrms ph-n BN Avg",
    "Vrms ph-n CN Avg",
)
PHASE_CURRENT_COLUMNS = (
    "Current A Avg",
    "Current B Avg",
    "Current C Avg",
)
POWER_FACTOR_COLUMNS = (
    "Cos Phi AN Avg",
    "Cos Phi BN Avg",
    "Cos Phi CN Avg",
    "Cos Phi Total Avg",
)
POWER_COLUMNS = (
    "Active Power Total Avg",
    "Apparent Power Total Avg",
    "Reactive Power Total Avg",
)


def _robust_outlier_count(series: pd.Series, threshold: float = 12.0) -> int:
    numeric = pd.to_numeric(series, errors="coerce").dropna()
    if numeric.empty:
        return 0
    median = float(numeric.median())
    mad = float((numeric - median).abs().median())
    if mad == 0.0:
        return 0
    robust_z = 0.6745 * (numeric - median).abs() / mad
    return int((robust_z > threshold).sum())


def audit_measurements(frame: pd.DataFrame) -> dict[str, Any]:
    """Devuelve conteos de problemas sin modificar los datos."""

    required = (
        *PHASE_VOLTAGE_COLUMNS,
        *PHASE_CURRENT_COLUMNS,
        *POWER_FACTOR_COLUMNS,
        *POWER_COLUMNS,
    )
    missing = [column for column in required if column not in frame.columns]
    report: dict[str, Any] = {
        "rows": int(len(frame)),
        "missing_columns": missing,
        "null_values": int(frame.isna().sum().sum()),
        "checks": {},
    }
    checks: dict[str, int] = report["checks"]

    voltage_columns = [column for column in PHASE_VOLTAGE_COLUMNS if column in frame]
    current_columns = [column for column in PHASE_CURRENT_COLUMNS if column in frame]
    factor_columns = [column for column in POWER_FACTOR_COLUMNS if column in frame]
    power_columns = [column for column in POWER_COLUMNS if column in frame]

    if voltage_columns:
        voltage = frame[voltage_columns].apply(pd.to_numeric, errors="coerce")
        checks["nonpositive_phase_voltage_rows"] = int((voltage <= 0).any(axis=1).sum())
    if current_columns:
        current = frame[current_columns].apply(pd.to_numeric, errors="coerce")
        checks["negative_phase_current_rows"] = int((current < 0).any(axis=1).sum())
    if factor_columns:
        factors = frame[factor_columns].apply(pd.to_numeric, errors="coerce")
        checks["power_factor_out_of_range_rows"] = int(
            ((factors < 0) | (factors > 1)).any(axis=1).sum()
        )
    if "Active Power Total Avg" in frame:
        active = pd.to_numeric(frame["Active Power Total Avg"], errors="coerce")
        checks["zero_active_power_rows"] = int(np.isclose(active.fillna(np.nan), 0.0).sum())
    for column in power_columns:
        checks[f"robust_outliers::{column}"] = _robust_outlier_count(frame[column])

    return report
