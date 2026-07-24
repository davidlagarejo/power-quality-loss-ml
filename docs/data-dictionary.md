# Diccionario de datos

## Exportación del analizador

| Campo | Significado interpretado | Unidad |
|---|---|---:|
| `Date` | Fecha de la medición | fecha |
| `Time` | Hora de la medición | hora |
| `Vrms ph-n AN Avg` | Tensión RMS fase A-neutro | V |
| `Vrms ph-n BN Avg` | Tensión RMS fase B-neutro | V |
| `Vrms ph-n CN Avg` | Tensión RMS fase C-neutro | V |
| `Vrms ph-n NG Avg` | Tensión RMS neutro-tierra | V |
| `Current A Avg` | Corriente RMS fase A | A |
| `Current B Avg` | Corriente RMS fase B | A |
| `Current C Avg` | Corriente RMS fase C | A |
| `Current Phi AN Avg` | Ángulo de corriente fase A | grados |
| `Current Phi BN Avg` | Ángulo de corriente fase B | grados |
| `Current Phi CN Avg` | Ángulo de corriente fase C | grados |
| `Active Power Total Avg` | Potencia activa total | W, por inferencia |
| `Apparent Power Total Avg` | Potencia aparente total | VA, por inferencia |
| `Reactive Power Total Avg` | Potencia reactiva total | var, por inferencia |
| `Cos Phi AN Avg` | Factor de potencia fase A | adimensional |
| `Cos Phi BN Avg` | Factor de potencia fase B | adimensional |
| `Cos Phi CN Avg` | Factor de potencia fase C | adimensional |
| `Cos Phi Total Avg` | Factor de potencia total | adimensional |

Las unidades de potencia se infieren de la conversión histórica por 1.000. Se
deben confirmar con la configuración y el manual del analizador.

## Dataset de machine learning

| Campo | Interpretación | Papel |
|---|---|---|
| `costoreactiva` | Costo atribuido a energía reactiva | entrada |
| `costodesbalance` | Costo atribuido al indicador de desbalance | entrada |
| `costoarmonicos` | Costo atribuido al indicador histórico de armónicos | entrada |
| `costocorrienteneutra` | Costo atribuido a corriente neutra | entrada |
| `costolineabase` | Costo base de energía activa | objetivo |

La moneda no está codificada en el CSV. Los libros usan una tarifa de 500 y
metadatos/contexto colombiano, por lo que probablemente son pesos colombianos,
pero esto debe confirmarse antes de publicarlo como hecho.
