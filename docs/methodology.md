# Reconstructed Methodology

## 1. Source data

The analyzer CSV contains phase-to-neutral voltage, phase current, phase
angles, total active/apparent/reactive power, and power factor. Row order is
preserved as the inherited time sequence.

## 2. Historical imbalance calculation

For the three phases:

1. calculate average voltage and current;
2. calculate absolute AB, BC, and CA differences;
3. select the largest voltage and current differences;
4. multiply both values and then apply power factor.

```text
ΔVmax = max(|VA - VB|, |VB - VC|, |VC - VA|)
ΔImax = max(|IA - IB|, |IB - IC|, |IC - IA|)
Sproxy = ΔVmax × ΔImax                  [VA]
Pproxy = Sproxy × PF                    [W]
Pproxy_kW = Pproxy / 1000               [kW]
```

This calculation reproduces the historical workbook but is not, by itself, a
validated electrical-loss model.

## 3. Neutral current

The implemented physical equation is:

```text
Pneutral_W = Ineutral² × Rconductor
Pneutral_kW = Pneutral_W / 1000
```

A defensible result requires measured neutral RMS current and effective
conductor resistance at the applicable temperature and frequency. The random
spreadsheet generation is retained only as historical context.

## 4. Harmonics

The original workbook uses constant 3% voltage and 2% current values. It also
mixes terms with incompatible dimensions. `legacy.py` reproduces the numeric
result for traceability and names it `legacy_harmonic_score`.

A technical second version needs at least:

- individual harmonic spectra by phase;
- measured voltage THD;
- current TDD calculated with maximum demand current;
- formal PCC identification;
- nominal voltage and short-circuit ratio required by the applicable edition;
- a separate physical model for converting distortion into loss.

## 5. Historical economic conversion

The workbooks convert power/energy proxies into costs using fixed
coefficients. The final dataset contains values that are already monetized, so
ML does not replace or correct the physical assumptions.

## 6. Machine learning

The reproducible version:

- uses four English-named cost columns as inputs;
- always excludes `baseline_active_energy_cost` from `X`;
- reserves the final 20% as an ordered holdout;
- retains parameters close to the historical model;
- uses `eval_metric=rmse` and early stopping;
- saves the model in native JSON format;
- reports MAE, RMSE, R², nonzero-target MAPE, WAPE, and sMAPE.

Because the historical ML dataset dropped `Date` and `Time`, the ordered split
assumes its rows retain CSV order. A future version should retain timestamps
and group evaluation windows by campaign or facility.
