"""Herramientas auditables para el prototipo de calidad de energía."""

from .legacy import (
    HarmonicLegacyResult,
    ImbalanceResult,
    NeutralLossResult,
    calculate_legacy_harmonic_score,
    calculate_legacy_imbalance,
    calculate_neutral_conductor_loss,
)

__all__ = [
    "HarmonicLegacyResult",
    "ImbalanceResult",
    "NeutralLossResult",
    "calculate_legacy_harmonic_score",
    "calculate_legacy_imbalance",
    "calculate_neutral_conductor_loss",
]

__version__ = "0.1.0"
