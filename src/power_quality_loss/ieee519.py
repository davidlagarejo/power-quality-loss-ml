"""Configurable framework for evaluating distortion limits at the PCC.

No standards tables are copied. Limits must come from the applicable edition
of the standard, obtained or consulted legitimately by the user.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class LimitAssessment:
    metric: str
    measured_pct: float
    limit_pct: float
    margin_pct_points: float
    passes: bool

    def to_dict(self) -> dict[str, float | bool | str]:
        return asdict(self)


@dataclass(frozen=True)
class AssessmentContext:
    point_of_common_coupling_identified: bool
    nominal_voltage_v: float | None = None
    short_circuit_ratio: float | None = None
    demand_current_a: float | None = None

    def missing_requirements(self) -> list[str]:
        missing: list[str] = []
        if not self.point_of_common_coupling_identified:
            missing.append("point of common coupling (PCC)")
        if self.nominal_voltage_v is None:
            missing.append("nominal voltage at the PCC")
        return missing


def assess_percentage(metric: str, measured_pct: float, limit_pct: float) -> LimitAssessment:
    """Compare a percentage measurement with a user-supplied limit."""

    measured_pct = float(measured_pct)
    limit_pct = float(limit_pct)
    if measured_pct < 0.0:
        raise ValueError("The percentage measurement cannot be negative")
    if limit_pct <= 0.0:
        raise ValueError("The limit must be greater than zero")

    return LimitAssessment(
        metric=metric,
        measured_pct=measured_pct,
        limit_pct=limit_pct,
        margin_pct_points=limit_pct - measured_pct,
        passes=measured_pct <= limit_pct,
    )
