# Hallazgos de auditoría

Fecha de revisión: 23 de julio de 2026.

## Conclusión

El material recuperado es un prototipo exploratorio valioso, pero no una
calculadora certificada de kW perdidos ni una implementación completa de IEEE
519. El flujo mezcla cálculos determinísticos en Excel con un modelo XGBoost
que predice el costo de la línea base.

## Hallazgos críticos

### 1. El objetivo del modelo no son los kW perdidos

Las cuatro entradas son costos derivados y el objetivo `costolineabase`
representa el costo de energía activa. El modelo aprende una relación
económica entre columnas, no una ley física de pérdidas.

### 2. Fuga de la variable objetivo en un experimento

Una celda del notebook incluye `costolineabase` dentro de `X` y también la usa
como `y`. El puntaje de búsqueda de hiperparámetros asociado a ese experimento
no es válido para medir generalización.

La versión organizada define únicamente estas entradas:

- `costoreactiva`
- `costodesbalance`
- `costoarmonicos`
- `costocorrienteneutra`

### 3. La comparación histórica no implementa IEEE 519

La hoja de armónicos asigna 3 % de THD de tensión y 2 % de THD de corriente a
todas las filas. No son mediciones tomadas del CSV. Además:

- no identifica formalmente el punto de acoplamiento común (PCC);
- no calcula TDD de corriente;
- no incorpora la tensión nominal para seleccionar límites;
- no incorpora `Isc/IL` o el contexto de cortocircuito/demanda;
- no evalúa armónicos individuales.

### 4. Unidades incorrectas

En `desbalance.xlsx`, tensión en V × corriente en A produce VA; después de
aplicar factor de potencia produce W. La hoja rotula directamente el resultado
como kW sin dividir por 1.000.

La hoja de armónicos mezcla magnitudes en V, A y fracciones sin una unidad
física consistente. Su resultado se conserva como un *score* histórico.

### 5. Corriente del neutro sintética

Las hojas de corriente neutra usan `RANDBETWEEN` para generar valores entre
límites observados y después aplican `I²R`. Al no existir semilla ni medición
explícita del neutro, esa parte no es reproducible y no debe presentarse como
medición real.

## Hallazgos de datos

- 2.343 filas en el analizador y en el dataset final.
- 17 filas con potencia activa igual a cero.
- factores de potencia con valor 327,67, fuera del rango físico esperado.
- valores de potencia de 4.915.050 en varias columnas, candidatos a error de
  exportación o a un cambio de escala.
- el costo final de corriente neutra no coincide con el libro de consolidación
  en 2.325 de 2.343 filas; probablemente fue recalculado desde otra versión.
- los libros de consolidación conservan enlaces externos rotos.

## Evaluación original

El notebook dejó registrados:

- MAE: aproximadamente 22.408;
- RMSE: aproximadamente 31.661;
- MAPE: infinito;
- “accuracy”: infinito negativo.

MAPE falla porque hay objetivos iguales a cero. La métrica RMSPE personalizada
también aplica `expm1` a valores que no fueron transformados logarítmicamente.
El código nuevo informa MAPE solo para objetivos no nulos, WAPE y sMAPE.

## Modelo histórico

El archivo `modelo_XGBOOST.joblib` parece haber sido generado con XGBoost 1.4 y
contiene aproximadamente 51 árboles. Cargar artefactos `joblib` no confiables
puede ejecutar código; por eso se archiva, pero la ruta recomendada es volver a
entrenar y guardar el modelo en formato nativo JSON.

## Qué se corrigió en el repositorio público

- nombres y unidades explícitas;
- pruebas que reproducen la primera fila de cada fórmula histórica;
- separación ordenada entrenamiento/prueba;
- ausencia de la variable objetivo entre las entradas;
- métricas finitas cuando existen objetivos iguales a cero;
- evaluación de límites configurable, sin copiar tablas normativas;
- datos, binarios y documentos históricos fuera de Git por defecto.
