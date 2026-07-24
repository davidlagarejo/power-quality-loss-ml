# Estado de publicación en GitHub

## Obligatorio

- [x] Confirmar el propietario y la autorización de publicación de las
  mediciones del analizador.
- [x] Publicar el repositorio como público.
- [x] Aplicar licencia MIT para permitir reutilización.
- [ ] Confirmar la moneda y la tarifa usadas en 2021.
- [ ] Identificar el modelo/marca del analizador y las unidades exportadas.
- [x] Revisar nombres de personas y empresas en metadatos de Office.
- [x] Mantener fuera del repositorio normas IEEE e informes de terceros.
- [x] No publicar `modelo_XGBOOST.joblib`; volver a entrenar y usar JSON nativo.
- [x] Publicar los CSV reales sin datos personales.

## Recomendado

- [x] Publicar los datos reales autorizados y conservar una muestra sintética.
- [ ] Añadir fecha/hora al dataset de ML.
- [ ] Medir corriente del neutro en lugar de generarla.
- [ ] Capturar THD/TDD y armónicos individuales reales.
- [ ] Documentar PCC, tensión nominal, `IL` e `Isc`.
- [ ] Validar las ecuaciones de pérdidas con un ingeniero electricista.
- [ ] Añadir una campaña independiente para evaluación fuera de muestra.
- [ ] Crear una ficha del modelo con población, límites y riesgos.

## Estado actual

El código, la documentación y los CSV reales están aprobados para publicación.
`private/`, `models/` y `reports/` continúan excluidos salvo sus archivos
README.
