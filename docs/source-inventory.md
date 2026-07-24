# Inventario de fuentes recuperadas

Todos los archivos siguientes están copiados localmente en
`private/originals/`. Los dos CSV indicados como públicos también se incluyen
en `data/`; los demás permanecen excluidos de Git.

| Archivo | Función | Publicación | SHA-256 |
|---|---|---|---|
| `power-quality-meter.csv` | Exportación del analizador | `data/raw/` | `5c837805…b6e7ad` |
| `desbalance.xlsx` | Cálculo histórico de desbalance | Privado | `3ee6ce21…bad7c` |
| `harmonicos.xlsx` | Cálculo histórico de armónicos | Privado | `d8d1e1ab…27a53` |
| `corrienteneutro.xlsx` | Primera hoja de corriente neutra | Privado | `e40f54fa…1a20` |
| `Copia de corrienteneutro.xlsx` | Versión usada por la consolidación | Privado | `09e221fd…c89c` |
| `Feuturemotor.xlsx` | Consolidación técnica/económica | Privado | `c06ebd8f…53d68` |
| `Feuturefinal.xlsx` | Selección intermedia con enlaces externos | Privado | `4e025038…9f4a0` |
| `Feuturefinall.xlsx` | Dataset final congelado | Privado | `618046d6…5c082` |
| `Feuturefinall.csv` | Dataset usado por Python | `data/processed/` | `8c1faabc…b5d62` |
| `PredictionCost.ipynb` | Entrenamiento y pruebas XGBoost | Privado | `7c267529…9af8` |
| `modelo_XGBOOST.joblib` | Modelo serializado histórico | Privado | `5edeecb7…e2bc` |
| `Untitled.ipynb` | Notebook vacío | Privado | `8bb7898d…b630c` |
| `costo usuario servidor.xlsx` | Estimación AWS, no central al modelo | Privado | `6405b197…df2d` |

## Fuentes relacionadas excluidas

También se localizaron documentos de referencia sobre IEEE 1159, IEEE 1459 y
un informe técnico de terceros. No se copiaron al repositorio porque pueden
estar protegidos por derechos de autor o contener información de cliente.
