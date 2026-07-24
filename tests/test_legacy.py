import pytest

from power_quality_loss.legacy import (
    calculate_legacy_harmonic_score,
    calculate_legacy_imbalance,
    calculate_neutral_conductor_loss,
)


VOLTAGES = (242.58, 241.98, 242.12)
CURRENTS = (596.0, 544.7, 496.3)


def test_first_legacy_imbalance_row_matches_spreadsheet():
    result = calculate_legacy_imbalance(VOLTAGES, CURRENTS, 0.99)

    assert result.average_voltage_v == pytest.approx(242.2266666667)
    assert result.maximum_voltage_deviation_v == pytest.approx(0.60)
    assert result.maximum_current_deviation_a == pytest.approx(99.70)
    assert result.legacy_active_loss_w == pytest.approx(59.2218)
    assert result.legacy_active_loss_kw == pytest.approx(0.0592218)


def test_neutral_loss_reports_watts_and_kilowatts():
    result = calculate_neutral_conductor_loss(9.24, 0.15, 0.99)

    assert result.conductor_loss_w == pytest.approx(12.80664)
    assert result.conductor_loss_kw == pytest.approx(0.01280664)
    assert result.legacy_power_factor_adjusted_w == pytest.approx(12.6785736)


def test_first_legacy_harmonic_row_matches_spreadsheet():
    result = calculate_legacy_harmonic_score(VOLTAGES, CURRENTS, power_factor=0.96)

    assert result.maximum_mixed_voltage_term == pytest.approx(10.9133333333)
    assert result.maximum_mixed_current_term == pytest.approx(0.0009)
    assert result.legacy_active_score == pytest.approx(0.00942912)


def test_invalid_power_factor_is_rejected():
    with pytest.raises(ValueError):
        calculate_legacy_imbalance(VOLTAGES, CURRENTS, 327.67)
