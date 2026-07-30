# Audit Findings

Audit date: July 23, 2026.

## Conclusion

The recovered material is a valuable exploratory prototype, but it is not a
certified lost-kW calculator or a complete IEEE 519 implementation. The flow
combines deterministic spreadsheet calculations with an XGBoost model that
predicts baseline cost.

## Critical findings

### 1. The model target is not lost kW

The four inputs are derived costs, and the target represents active-energy
baseline cost. The model learns an economic relationship between derived
columns rather than a physical law of electrical loss.

### 2. Target leakage in one historical experiment

One notebook cell included the target in `X` while also using it as `y`. The
hyperparameter-search score from that experiment does not measure
generalization.

The corrected implementation uses only:

- `reactive_energy_cost`
- `imbalance_cost`
- `harmonic_cost`
- `neutral_current_cost`

### 3. The historical comparison does not implement IEEE 519

The harmonic workbook assigns 3% voltage THD and 2% current THD to every row.
Those values were not measured in the published CSV. It also:

- does not formally identify the point of common coupling (PCC);
- does not calculate current TDD;
- does not retain nominal voltage for limit selection;
- does not retain `Isc/IL` or short-circuit/demand context;
- does not evaluate individual harmonic orders.

### 4. Incorrect units

In the imbalance workbook, voltage in V multiplied by current in A produces
VA; applying power factor produces W. The workbook labels the result as kW
without dividing by 1,000.

The harmonic workbook mixes V, A, and dimensionless ratios. Its result is
preserved as a historical score rather than physical power.

### 5. Synthetic neutral current

The neutral-current workbooks use `RANDBETWEEN` to generate values and then
apply `I²R`. Without a seed or an explicit neutral measurement, this branch is
not reproducible and cannot be presented as measured behavior.

## Data findings

- 2,343 rows in both the analyzer export and final ML dataset.
- 17 rows with zero active power.
- power-factor values of 327.67, outside the expected physical range.
- power values of 4,915,050 in several columns, likely export or scale errors.
- the final neutral-current cost differs from the consolidation workbook in
  2,325 of 2,343 rows, most likely because it was recalculated from another
  version.
- the consolidation workbooks retain broken external links.

## Historical evaluation

The notebook recorded:

- MAE: approximately 22,408;
- RMSE: approximately 31,661;
- MAPE: infinity;
- “accuracy”: negative infinity.

MAPE fails because the target contains zero values. The custom RMSPE also
applies `expm1` to values that were not log-transformed. The new code reports
nonzero-target MAPE, WAPE, and sMAPE.

## Historical model artifact

`modelo_XGBOOST.joblib` appears to have been generated with XGBoost 1.4 and
contains approximately 51 trees. Loading an untrusted `joblib` file can
execute code. The artifact is archived privately; the recommended path is to
retrain and save a native JSON model.

## Corrections in the public repository

- explicit names and units;
- tests that reproduce the first row of each historical formula;
- ordered training/test separation;
- no target among the input features;
- finite metrics when zero targets exist;
- configurable limit assessment without copied standards tables;
- real datasets with English headers;
- private exclusion of binary and third-party source artifacts.
