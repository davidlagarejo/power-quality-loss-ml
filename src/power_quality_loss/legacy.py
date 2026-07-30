"""Explicit reconstruction of the historical formulas.

The functions in this module reproduce the prototype while exposing the
actual units. They do not turn the results into an IEEE 519 compliance
assessment.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable


def _three(values: Iterable[float], name: str) -> tuple[float, float, float]:
    result = tuple(float(value) for value in values)
    if len(result) != 3:
        raise ValueError(f"{name} must contain exactly three phases")
    return result  # type: ignore[return-value]


def _power_factor(value: float) -> float:
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError("Power factor must be between 0 and 1")
    return value


@dataclass(frozen=True)
class ImbalanceResult:
    average_voltage_v: float
    average_current_a: float
    maximum_voltage_deviation_v: float
    maximum_current_deviation_a: float
    voltage_imbalance_pct: float
    current_imbalance_pct: float
    legacy_apparent_loss_va: float
    legacy_active_loss_w: float
    legacy_active_loss_kw: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def calculate_legacy_imbalance(
    phase_voltages_v: Iterable[float],
    phase_currents_a: Iterable[float],
    power_factor: float,
) -> ImbalanceResult:
    """Reproduce ``desbalance.xlsx`` with corrected units.

    The workbook multiplied the largest phase-to-phase voltage difference by
    the largest phase-to-phase current difference and by power factor. The
    result was labeled as kW, although its dimensional unit is W; both units
    are therefore reported explicitly.
    """

    voltages = _three(phase_voltages_v, "phase_voltages_v")
    currents = _three(phase_currents_a, "phase_currents_a")
    power_factor = _power_factor(power_factor)

    average_voltage = sum(voltages) / 3.0
    average_current = sum(currents) / 3.0
    if average_voltage == 0.0 or average_current == 0.0:
        raise ValueError("Average voltage and current must be nonzero")

    voltage_pair_differences = (
        abs(voltages[0] - voltages[1]),
        abs(voltages[1] - voltages[2]),
        abs(voltages[2] - voltages[0]),
    )
    current_pair_differences = (
        abs(currents[0] - currents[1]),
        abs(currents[1] - currents[2]),
        abs(currents[2] - currents[0]),
    )
    maximum_voltage_deviation = max(voltage_pair_differences)
    maximum_current_deviation = max(current_pair_differences)
    apparent_loss_va = maximum_voltage_deviation * maximum_current_deviation
    active_loss_w = apparent_loss_va * power_factor

    return ImbalanceResult(
        average_voltage_v=average_voltage,
        average_current_a=average_current,
        maximum_voltage_deviation_v=maximum_voltage_deviation,
        maximum_current_deviation_a=maximum_current_deviation,
        voltage_imbalance_pct=100.0 * maximum_voltage_deviation / average_voltage,
        current_imbalance_pct=100.0 * maximum_current_deviation / average_current,
        legacy_apparent_loss_va=apparent_loss_va,
        legacy_active_loss_w=active_loss_w,
        legacy_active_loss_kw=active_loss_w / 1_000.0,
    )


@dataclass(frozen=True)
class NeutralLossResult:
    neutral_current_a: float
    conductor_resistance_ohm: float
    conductor_loss_w: float
    conductor_loss_kw: float
    legacy_power_factor_adjusted_w: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def calculate_neutral_conductor_loss(
    neutral_current_a: float,
    conductor_resistance_ohm: float,
    power_factor: float = 1.0,
) -> NeutralLossResult:
    """Calculate resistive ``I²R`` loss from a measured current.

    The historical workbook generated neutral current randomly and then
    multiplied the result by power factor. This function requires an explicit
    measurement and retains the adjusted value only for comparison.
    """

    neutral_current_a = float(neutral_current_a)
    conductor_resistance_ohm = float(conductor_resistance_ohm)
    power_factor = _power_factor(power_factor)
    if neutral_current_a < 0.0:
        raise ValueError("Neutral current cannot be negative")
    if conductor_resistance_ohm < 0.0:
        raise ValueError("Resistance cannot be negative")

    loss_w = neutral_current_a**2 * conductor_resistance_ohm
    return NeutralLossResult(
        neutral_current_a=neutral_current_a,
        conductor_resistance_ohm=conductor_resistance_ohm,
        conductor_loss_w=loss_w,
        conductor_loss_kw=loss_w / 1_000.0,
        legacy_power_factor_adjusted_w=loss_w * power_factor,
    )


@dataclass(frozen=True)
class HarmonicLegacyResult:
    maximum_mixed_voltage_term: float
    maximum_mixed_current_term: float
    legacy_apparent_score: float
    legacy_active_score: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def calculate_legacy_harmonic_score(
    phase_voltages_v: Iterable[float],
    phase_currents_a: Iterable[float],
    voltage_thd_fraction: Iterable[float] = (0.03, 0.03, 0.03),
    current_thd_fraction: Iterable[float] = (0.02, 0.02, 0.02),
    power_factor: float = 1.0,
) -> HarmonicLegacyResult:
    """Reproduce the indicator from ``harmonicos.xlsx``.

    The original formula mixes V, A, and dimensionless fractions, so its
    result is a historical score rather than physical power in kW.
    """

    voltages = _three(phase_voltages_v, "phase_voltages_v")
    currents = _three(phase_currents_a, "phase_currents_a")
    voltage_thd = _three(voltage_thd_fraction, "voltage_thd_fraction")
    current_thd = _three(current_thd_fraction, "current_thd_fraction")
    power_factor = _power_factor(power_factor)

    if any(value < 0.0 for value in (*voltage_thd, *current_thd)):
        raise ValueError("THD values cannot be negative")

    average_voltage = sum(voltages) / 3.0
    average_current = sum(currents) / 3.0

    # Order and references reconstructed from spreadsheet columns P:V.
    mixed_voltage_terms = (
        average_voltage * voltage_thd[0],
        average_current * current_thd[0],
        voltage_thd[1] * voltage_thd[2],
    )
    mixed_current_terms = (
        current_thd[0] * current_thd[1],
        voltage_thd[1] * voltage_thd[2],
        current_thd[1] * current_thd[2],
    )
    maximum_voltage_term = max(mixed_voltage_terms)
    maximum_current_term = max(mixed_current_terms)
    apparent_score = maximum_voltage_term * maximum_current_term

    return HarmonicLegacyResult(
        maximum_mixed_voltage_term=maximum_voltage_term,
        maximum_mixed_current_term=maximum_current_term,
        legacy_apparent_score=apparent_score,
        legacy_active_score=apparent_score * power_factor,
    )
