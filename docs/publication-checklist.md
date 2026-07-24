# Lista antes de publicar en GitHub

## Obligatorio

- [ ] Confirmar el propietario y la autorización de publicación de las
  mediciones del analizador.
- [ ] Decidir si el repositorio será público o privado.
- [ ] Elegir una licencia de software. Mientras no exista una, se reservan por
  defecto todos los derechos.
- [ ] Confirmar la moneda y la tarifa usadas en 2021.
- [ ] Identificar el modelo/marca del analizador y las unidades exportadas.
- [ ] Revisar nombres de personas y empresas en metadatos de Office.
- [ ] Mantener fuera del repositorio normas IEEE e informes de terceros.
- [ ] No publicar `modelo_XGBOOST.joblib`; volver a entrenar y usar JSON nativo.

## Recomendado

- [ ] Publicar únicamente datos sintéticos o un conjunto anonimizado aprobado.
- [ ] Añadir fecha/hora al dataset de ML.
- [ ] Medir corriente del neutro en lugar de generarla.
- [ ] Capturar THD/TDD y armónicos individuales reales.
- [ ] Documentar PCC, tensión nominal, `IL` e `Isc`.
- [ ] Validar las ecuaciones de pérdidas con un ingeniero electricista.
- [ ] Añadir una campaña independiente para evaluación fuera de muestra.
- [ ] Crear una ficha del modelo con población, límites y riesgos.

## Estado actual

El repositorio está preparado de forma conservadora: el código y la
documentación se pueden versionar; `private/`, `models/` y `reports/` se
excluyen salvo sus archivos README.
