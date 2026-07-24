"""Marco configurable para evaluar límites de distorsión en el PCC.

No se copian tablas normativas. Los límites deben proceder de la edición
aplicable de la norma, adquirida o consultada legítimamente por el usuario.
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
            missing.append("punto de acoplamiento común (PCC)")
        if self.nominal_voltage_v is None:
            missing.append("tensión nominal en el PCC")
        return missing


def assess_percentage(metric: str, measured_pct: float, limit_pct: float) -> LimitAssessment:
    """Compara una medición porcentual con un límite suministrado."""

    measured_pct = float(measured_pct)
    limit_pct = float(limit_pct)
    if measured_pct < 0.0:
        raise ValueError("La medición porcentual no puede ser negativa")
    if limit_pct <= 0.0:
        raise ValueError("El límite debe ser mayor que cero")

    return LimitAssessment(
        metric=metric,
        measured_pct=measured_pct,
        limit_pct=limit_pct,
        margin_pct_points=limit_pct - measured_pct,
        passes=measured_pct <= limit_pct,
    )
