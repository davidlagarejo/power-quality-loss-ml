# Data Dictionary

## Power-analyzer export

| Field | Interpreted meaning | Unit |
|---|---|---:|
| `Date` | Measurement date | date |
| `Time` | Measurement time | time |
| `Vrms ph-n AN Avg` | Phase A-to-neutral RMS voltage | V |
| `Vrms ph-n BN Avg` | Phase B-to-neutral RMS voltage | V |
| `Vrms ph-n CN Avg` | Phase C-to-neutral RMS voltage | V |
| `Vrms ph-n NG Avg` | Neutral-to-ground RMS voltage | V |
| `Current A Avg` | Phase A RMS current | A |
| `Current B Avg` | Phase B RMS current | A |
| `Current C Avg` | Phase C RMS current | A |
| `Current Phi AN Avg` | Phase A current angle | degrees |
| `Current Phi BN Avg` | Phase B current angle | degrees |
| `Current Phi CN Avg` | Phase C current angle | degrees |
| `Active Power Total Avg` | Total active power | W, inferred |
| `Apparent Power Total Avg` | Total apparent power | VA, inferred |
| `Reactive Power Total Avg` | Total reactive power | var, inferred |
| `Cos Phi AN Avg` | Phase A power factor | dimensionless |
| `Cos Phi BN Avg` | Phase B power factor | dimensionless |
| `Cos Phi CN Avg` | Phase C power factor | dimensionless |
| `Cos Phi Total Avg` | Total power factor | dimensionless |

Power units are inferred from the workbooks’ division by 1,000. They should be
confirmed against the analyzer configuration and manual.

## Machine-learning dataset

| Published field | Historical field | Interpretation | Role |
|---|---|---|---|
| `reactive_energy_cost` | `costoreactiva` | Cost attributed to reactive energy | input |
| `imbalance_cost` | `costodesbalance` | Cost attributed to the imbalance proxy | input |
| `harmonic_cost` | `costoarmonicos` | Cost attributed to the historical harmonic score | input |
| `neutral_current_cost` | `costocorrienteneutra` | Cost attributed to neutral current | input |
| `baseline_active_energy_cost` | `costolineabase` | Baseline active-energy cost | target |

Only the published CSV header was translated; all numeric rows remain
unchanged. Currency is not encoded in the CSV. The workbooks use a rate of 500
and Colombian context, suggesting Colombian pesos, but this should be
confirmed before treating the currency as established fact.
