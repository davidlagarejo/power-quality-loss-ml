# Notas para una evaluación IEEE 519

La edición activa localizada durante la revisión es IEEE 519-2022, publicada
el 5 de agosto de 2022 y sucesora de IEEE 519-2014. La página oficial la
describe como límites de distorsión de tensión y corriente en estado estable
en el punto de acoplamiento común (PCC):

- [IEEE Standards Association — IEEE 519-2022](https://standards.ieee.org/ieee/519/10677/)

## Diferencia entre el prototipo y una evaluación normativa

El prototipo usa valores constantes de THD y no conoce formalmente el PCC. Una
evaluación trazable debe registrar, como mínimo:

1. edición exacta de la norma y fecha de evaluación;
2. ubicación del PCC;
3. nivel de tensión nominal;
4. THDv e individuales de tensión medidos en el PCC;
5. TDD e individuales de corriente;
6. corriente máxima de demanda `IL`;
7. datos de cortocircuito y relación `Isc/IL` cuando correspondan;
8. ventana estadística y período de observación;
9. límites aplicables obtenidos de una copia autorizada;
10. margen, estado de cumplimiento e incertidumbre de medición.

## Diseño adoptado

El código no incorpora tablas numéricas de la norma. `ieee519.py` recibe el
valor medido y el límite ya seleccionado por un profesional con acceso a la
edición aplicable. Así se evita:

- presentar como universal un límite que depende del contexto;
- confundir THD de corriente con TDD;
- copiar contenido normativo protegido;
- afirmar conformidad sin la información necesaria.

La evaluación de límites y el cálculo de pérdidas deben permanecer separados:
estar dentro o fuera de un límite de distorsión no determina automáticamente
los kW perdidos.
