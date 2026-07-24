# Metodología reconstruida

## 1. Fuente

El CSV del analizador contiene tensión fase-neutro, corriente por fase,
ángulos, potencia activa/aparente/reactiva y factor de potencia. El orden del
archivo se conserva como secuencia temporal.

## 2. Desbalance histórico

Para las tres fases:

1. se calcula el promedio de tensión y corriente;
2. se calculan las diferencias absolutas AB, BC y CA;
3. se toma la mayor diferencia de tensión y de corriente;
4. se multiplican ambas y después se aplica un factor de potencia.

En símbolos:

```text
ΔVmax = max(|VA - VB|, |VB - VC|, |VC - VA|)
ΔImax = max(|IA - IB|, |IB - IC|, |IC - IA|)
Sproxy = ΔVmax × ΔImax                  [VA]
Pproxy = Sproxy × FP                    [W]
Pproxy_kW = Pproxy / 1000               [kW]
```

Este cálculo reproduce la hoja histórica, pero no constituye por sí mismo un
modelo eléctrico validado de pérdidas por desbalance.

## 3. Corriente neutra

La ecuación física implementada es:

```text
Pneutro_W = Ineutro² × Rconductor
Pneutro_kW = Pneutro_W / 1000
```

Para un resultado defendible se necesita corriente RMS medida en el neutro y
la resistencia efectiva del conductor a la temperatura/frecuencia aplicable.
La generación aleatoria del Excel se conserva solo como antecedente.

## 4. Armónicos

La hoja original usa valores constantes de 3 % para tensión y 2 % para
corriente. También mezcla términos con dimensiones incompatibles. El módulo
`legacy.py` reproduce el número únicamente para trazabilidad y lo llama
`legacy_harmonic_score`.

Una versión técnica futura necesita al menos:

- espectro de armónicos individuales por fase;
- THDv medido;
- TDD de corriente calculado con la corriente máxima de demanda;
- identificación del PCC;
- tensión nominal y relación de cortocircuito requeridas por la edición
  aplicable de la norma;
- un modelo físico separado para convertir distorsión en pérdidas.

## 5. Conversión económica histórica

Las hojas convierten potencia/energía a costos con coeficientes fijos. El
dataset final contiene valores ya monetizados; por ello el ML no reemplaza las
ecuaciones físicas y no puede corregir sus supuestos.

## 6. Machine learning

La versión reproducible:

- usa las cuatro columnas de costo como entradas;
- excluye siempre `costolineabase` de `X`;
- separa el último 20 % como *holdout* ordenado;
- conserva hiperparámetros cercanos a los históricos;
- usa `eval_metric=rmse` y parada temprana;
- guarda el modelo en formato nativo JSON;
- informa MAE, RMSE, MAPE no nulo, WAPE y sMAPE.

Como el dataset final perdió `Date` y `Time`, el corte ordenado asume que las
filas mantienen el orden del CSV. En una siguiente versión deben conservarse
marcas de tiempo y agrupar las ventanas de evaluación por campaña o instalación.
