# Published Real Data

The data in this directory belongs to the prototype performed for
**Aluminios de Colombia S.A. – ALUCOL**, developed by **ZION ING** for the
**Zircular** platform.

## Files

| Path | Content | Period | Rows | SHA-256 |
|---|---|---|---:|---|
| `raw/power-quality-meter.csv` | Real power-analyzer export | 2019-08-31 to 2019-09-01 | 2,343 | `5c837805238d6689ee3b5c8472d3c88447d6567039a14732741ba4b0c8b6e7ad` |
| `processed/model-features.csv` | Real economic features used by XGBoost | Derived from the same dataset | 2,343 | `26763f3d1d01d2c7a29c32ccb052ecca72fd1359dcc9c4368945ab8a254947e6` |

The processed CSV differs from the historical source only in its English
header. All 2,343 numeric rows are unchanged.

The prototype and its workbooks were developed primarily in 2021. Recovery,
audit, and reimplementation were completed in 2026.

The CSV files contain no names, addresses, phone numbers, or email addresses.
They do contain real operational measurements. Publication was authorized by
the project owner.

## Historical-to-English feature mapping

| Historical field | Published field |
|---|---|
| `costoreactiva` | `reactive_energy_cost` |
| `costodesbalance` | `imbalance_cost` |
| `costoarmonicos` | `harmonic_cost` |
| `costocorrienteneutra` | `neutral_current_cost` |
| `costolineabase` | `baseline_active_energy_cost` |

## Reuse

Unless explicitly identified as third-party content, the code, documentation,
and datasets are distributed under the repository’s MIT License. Reuse must
retain the copyright notice and license.

IEEE standards and third-party reports are not part of the dataset and are not
redistributed.
