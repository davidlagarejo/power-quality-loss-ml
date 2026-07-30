# Recovered Source Inventory

All artifacts below are preserved locally under `private/originals/`. The two
public CSV files are also included under `data/`; all other artifacts remain
excluded from Git.

| Historical file | Purpose | Publication | SHA-256 |
|---|---|---|---|
| `power-quality-meter.csv` | Power-analyzer export | `data/raw/` | `5c837805…b6e7ad` |
| `desbalance.xlsx` | Historical imbalance calculation | Private | `3ee6ce21…bad7c` |
| `harmonicos.xlsx` | Historical harmonic calculation | Private | `d8d1e1ab…27a53` |
| `corrienteneutro.xlsx` | First neutral-current workbook | Private | `e40f54fa…1a20` |
| `Copia de corrienteneutro.xlsx` | Neutral-current version used in consolidation | Private | `09e221fd…c89c` |
| `Feuturemotor.xlsx` | Technical/economic consolidation | Private | `c06ebd8f…53d68` |
| `Feuturefinal.xlsx` | Intermediate selection with external links | Private | `4e025038…9f4a0` |
| `Feuturefinall.xlsx` | Frozen final dataset | Private | `618046d6…5c082` |
| `Feuturefinall.csv` | Dataset used by the historical notebook | `data/processed/` with translated header | `26763f3d…947e6` published; `8c1faabc…b5d62` original |
| `PredictionCost.ipynb` | Historical XGBoost experiments | Private | `7c267529…9af8` |
| `modelo_XGBOOST.joblib` | Historical serialized model | Private | `5edeecb7…e2bc` |
| `Untitled.ipynb` | Empty notebook | Private | `8bb7898d…b630c` |
| `costo usuario servidor.xlsx` | AWS estimate; not central to the model | Private | `6405b197…df2d` |

## Related excluded sources

The project archive also contains IEEE 1159, IEEE 1459-2010, and a third-party
power-quality report. These files are not redistributed because they may be
copyrighted or contain client information.
