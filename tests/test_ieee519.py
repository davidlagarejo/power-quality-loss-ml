import pytest

from power_quality_loss.ieee519 import AssessmentContext, assess_percentage


def test_percentage_assessment_reports_margin():
    result = assess_percentage("voltage_thd_pct", 4.1, 5.0)

    assert result.passes is True
    assert result.margin_pct_points == pytest.approx(0.9)


def test_context_names_missing_pcc_inputs():
    context = AssessmentContext(point_of_common_coupling_identified=False)

    assert "punto de acoplamiento común (PCC)" in context.missing_requirements()
    assert "tensión nominal en el PCC" in context.missing_requirements()
