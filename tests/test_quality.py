import pandas as pd

from power_quality_loss.quality import audit_measurements


def test_audit_flags_invalid_power_factor_and_zero_power():
    frame = pd.DataFrame(
        {
            "Vrms ph-n AN Avg": [242.0, 242.0],
            "Vrms ph-n BN Avg": [242.0, 242.0],
            "Vrms ph-n CN Avg": [242.0, 242.0],
            "Current A Avg": [10.0, 10.0],
            "Current B Avg": [10.0, 10.0],
            "Current C Avg": [10.0, 10.0],
            "Cos Phi AN Avg": [0.99, 327.67],
            "Cos Phi BN Avg": [0.99, 0.99],
            "Cos Phi CN Avg": [0.99, 0.99],
            "Cos Phi Total Avg": [0.99, 0.99],
            "Active Power Total Avg": [1000.0, 0.0],
            "Apparent Power Total Avg": [1010.0, 0.0],
            "Reactive Power Total Avg": [100.0, 0.0],
        }
    )

    report = audit_measurements(frame)

    assert report["checks"]["power_factor_out_of_range_rows"] == 1
    assert report["checks"]["zero_active_power_rows"] == 1
